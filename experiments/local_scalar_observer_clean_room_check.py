#!/usr/bin/env python3
"""Independent numerical checks for the final-support thermal kernel.

This checker deliberately does not import ``qgtoy`` or the production
Galerkin implementation.  It uses midpoint Nystr\u00f6m sampling with a separate
product-integration rule for the logarithmic diagonal.  Its output is
adversarial numerical evidence, not a computer-assisted proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import asinh, pi
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "experiments/local_scalar_observer_clean_room_check.json"
Y_GRID = (
    0.005,
    0.01,
    0.03,
    0.1,
    0.3,
    1.0,
    3.0,
    5.0,
    10.0,
    30.0,
    100.0,
)
SMALL_Y = (0.005, 0.01, 0.03, 0.1, 0.3)
LARGE_Y = (1.0, 3.0, 5.0, 10.0, 30.0, 100.0)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rounded(value: float) -> float:
    return float(f"{value:.14g}")


def _log_sinh_over_argument(values: np.ndarray) -> np.ndarray:
    """Evaluate ``log(sinh(z)/z)`` stably for nonnegative ``z``."""
    values = np.asarray(values, dtype=float)
    if np.any(values < 0.0):
        raise ValueError("arguments must be nonnegative")
    result = np.zeros_like(values)
    small = (values > 0.0) & (values < 0.25)
    z = values[small]
    result[small] = (
        z**2 / 6.0 - z**4 / 180.0 + z**6 / 2835.0 - z**8 / 37800.0 + z**10 / 467775.0
    )
    large = values >= 0.25
    z = values[large]
    result[large] = z - np.log(2.0) + np.log1p(-np.exp(-2.0 * z)) - np.log(z)
    return result


def reflected_thermal_kernel(
    u: np.ndarray,
    v: np.ndarray,
    thermal_support_ratio: float,
) -> np.ndarray:
    """Evaluate the dimensionless kernel away from its diagonal."""
    if thermal_support_ratio < 0.0:
        raise ValueError("thermal_support_ratio must be nonnegative")
    u_values, v_values = np.broadcast_arrays(
        np.asarray(u, dtype=float),
        np.asarray(v, dtype=float),
    )
    separation = np.abs(u_values - v_values)
    if np.any(u_values <= 0.0) or np.any(v_values <= 0.0):
        raise ValueError("kernel coordinates must be positive")
    if np.any(separation == 0.0):
        raise ValueError("use product integration on the diagonal")
    summed = u_values + v_values
    vacuum = np.log(summed / separation) / pi
    tau = thermal_support_ratio
    if tau == 0.0:
        return vacuum
    correction = (
        _log_sinh_over_argument(tau * summed)
        - _log_sinh_over_argument(tau * separation)
    ) / pi
    return vacuum + correction


def _diagonal_cell_integral(
    midpoint: float,
    cell_width: float,
    thermal_support_ratio: float,
    *,
    quadrature_order: int,
) -> float:
    """Integrate the singular kernel across the cell containing ``midpoint``."""
    nodes, weights = np.polynomial.legendre.leggauss(quadrature_order)
    z = 0.5 * (nodes + 1.0)
    local_weights = 0.5 * weights
    offset = 0.5 * cell_width * z**2
    upper = reflected_thermal_kernel(
        np.full_like(offset, midpoint),
        midpoint + offset,
        thermal_support_ratio,
    )
    lower = reflected_thermal_kernel(
        np.full_like(offset, midpoint),
        midpoint - offset,
        thermal_support_ratio,
    )
    # With offset=(h/2)z^2, d(offset)=h*z*dz.
    return float(cell_width * np.dot(local_weights, z * (upper + lower)))


def midpoint_product_matrix(
    cell_count: int,
    thermal_support_ratio: float,
    *,
    diagonal_order: int,
) -> np.ndarray:
    """Build an independent symmetric midpoint/product-integration matrix."""
    if isinstance(cell_count, bool) or cell_count < 16:
        raise ValueError("cell_count must be an integer at least 16")
    if isinstance(diagonal_order, bool) or diagonal_order < 8:
        raise ValueError("diagonal_order must be an integer at least 8")
    cell_width = 1.0 / cell_count
    points = (np.arange(cell_count, dtype=float) + 0.5) * cell_width
    u = points[:, None]
    v = points[None, :]
    separation = np.abs(u - v)
    mask = separation > 0.0
    matrix = np.zeros((cell_count, cell_count), dtype=float)
    matrix[mask] = cell_width * reflected_thermal_kernel(
        np.broadcast_to(u, separation.shape)[mask],
        np.broadcast_to(v, separation.shape)[mask],
        thermal_support_ratio,
    )
    for index, midpoint in enumerate(points):
        matrix[index, index] = _diagonal_cell_integral(
            float(midpoint),
            cell_width,
            thermal_support_ratio,
            quadrature_order=diagonal_order,
        )
    return 0.5 * (matrix + matrix.T)


def _top_eigenpair(matrix: np.ndarray) -> tuple[float, np.ndarray]:
    values, vectors = np.linalg.eigh(matrix)
    vector = vectors[:, -1]
    if float(np.sum(vector)) < 0.0:
        vector = -vector
    return float(values[-1]), vector


def _analytic_bracket(support_ratio: float) -> tuple[float, float]:
    y = support_ratio
    lower = max(3.0 * y / pi, 8.0 * y**2 / pi**3)
    vacuum_thermal_upper = 4.0 * asinh(1.0) * y / pi + 8.0 * y**2 / pi**3
    small_support_upper = 4.0 * asinh(1.0) * y / pi + y**3 / (6.0 * pi)
    large_support_upper = 8.0 * y**2 / pi**3 + 2.0 * pi / 3.0
    return lower, min(
        vacuum_thermal_upper,
        small_support_upper,
        large_support_upper,
    )


def build_record(*, cell_count: int, diagonal_order: int) -> dict[str, object]:
    """Run the independent grid and return a deterministic audit record."""
    if cell_count < 64 or cell_count % 2:
        raise ValueError("cell_count must be an even integer at least 64")
    coarse_count = cell_count // 2
    cache: dict[tuple[int, float], tuple[np.ndarray, float, np.ndarray]] = {}

    def solve(n: int, y: float) -> tuple[np.ndarray, float, np.ndarray]:
        key = (n, y)
        if key not in cache:
            matrix = midpoint_product_matrix(
                n,
                0.5 * y,
                diagonal_order=diagonal_order,
            )
            eigenvalue, vector = _top_eigenpair(matrix)
            cache[key] = matrix, eigenvalue, vector
        return cache[key]

    vacuum: dict[int, tuple[np.ndarray, float, np.ndarray]] = {}
    for n in (coarse_count, cell_count):
        matrix = midpoint_product_matrix(
            n,
            0.0,
            diagonal_order=diagonal_order,
        )
        eigenvalue, vector = _top_eigenpair(matrix)
        vacuum[n] = matrix, eigenvalue, vector

    grid: list[dict[str, float]] = []
    bracket_pass = True
    profile_pass = True
    symmetry_pass = True
    maximum_resolution_step = 0.0
    for y in Y_GRID:
        coarse_matrix, coarse_lambda, _ = solve(coarse_count, y)
        matrix, eigenvalue, vector = solve(cell_count, y)
        coarse_cost = 2.0 * y * coarse_lambda
        cost = 2.0 * y * eigenvalue
        lower, upper = _analytic_bracket(y)
        tolerance = 2.0e-4 * max(1.0, upper)
        inside = lower - tolerance <= cost <= upper + tolerance
        bracket_pass = bracket_pass and inside
        profile_pass = profile_pass and float(np.min(vector)) > 0.0
        symmetry_pass = symmetry_pass and (
            float(np.max(np.abs(matrix - matrix.T))) < 1.0e-13
            and float(np.max(np.abs(coarse_matrix - coarse_matrix.T))) < 1.0e-13
        )
        relative_step = abs(cost - coarse_cost) / max(abs(cost), 1.0e-15)
        maximum_resolution_step = max(maximum_resolution_step, relative_step)
        grid.append(
            {
                "support_ratio_y": y,
                "coarse_cost": _rounded(coarse_cost),
                "fine_cost": _rounded(cost),
                "rigorous_lower": _rounded(lower),
                "rigorous_explicit_upper": _rounded(upper),
                "relative_resolution_step": _rounded(relative_step),
            }
        )

    small_rows: list[dict[str, float]] = []
    small_pass = True
    fine_vacuum_lambda = vacuum[cell_count][1]
    for y in SMALL_Y:
        cost = 2.0 * y * solve(cell_count, y)[1]
        vacuum_cost = 2.0 * y * fine_vacuum_lambda
        remainder = cost - vacuum_cost
        upper = y**3 / (6.0 * pi)
        tolerance = 2.0e-7 * max(1.0, vacuum_cost)
        small_pass = small_pass and -tolerance <= remainder <= upper + tolerance
        small_rows.append(
            {
                "support_ratio_y": y,
                "computed_remainder": _rounded(remainder),
                "analytic_upper_y3_over_6pi": _rounded(upper),
            }
        )

    large_rows: list[dict[str, float]] = []
    large_pass = True
    for y in LARGE_Y:
        cost = 2.0 * y * solve(cell_count, y)[1]
        leading = 8.0 * y**2 / pi**3
        remainder = cost - leading
        upper = 2.0 * pi / 3.0
        tolerance = 2.0e-4 * max(1.0, cost)
        large_pass = large_pass and -tolerance <= remainder <= upper + tolerance
        large_rows.append(
            {
                "support_ratio_y": y,
                "computed_remainder": _rounded(remainder),
                "analytic_upper_2pi_over_3": _rounded(upper),
            }
        )

    increment_rows: list[dict[str, float]] = []
    increment_pass = True
    for y in (0.03, 1.0, 30.0):
        thermal_eigenvalue = solve(cell_count, y)[1]
        vacuum_eigenvalue = vacuum[cell_count][1]
        increment = thermal_eigenvalue - vacuum_eigenvalue
        increment_pass = increment_pass and increment > 0.0
        increment_rows.append(
            {
                "support_ratio_y": y,
                "top_eigenvalue_increment": _rounded(increment),
            }
        )

    sector_y = np.geomspace(1.0e-6, 1.0e6, 2001)
    coordinate_upper = 2.0 * sector_y / pi + 2.0 * sector_y**2 / pi**3
    momentum_lower = np.maximum(
        3.0 * sector_y / pi,
        8.0 * sector_y**2 / pi**3,
    )
    sector_margin = momentum_lower - coordinate_upper
    sector_pass = bool(np.all(sector_margin > 0.0))

    checks = {
        "all_grid_estimates_inside_analytic_bracket": bracket_pass,
        "all_top_vectors_strictly_positive": profile_pass,
        "all_matrices_symmetric": symmetry_pass,
        "small_support_remainder_bound_holds_on_grid": small_pass,
        "large_support_remainder_bound_holds_on_grid": large_pass,
        "thermal_top_eigenvalue_strictly_exceeds_vacuum": increment_pass,
        "coordinate_bound_strictly_below_momentum_lower_envelope": sector_pass,
        "maximum_coarse_to_fine_relative_step": _rounded(maximum_resolution_step),
    }
    passed = (
        bracket_pass
        and profile_pass
        and symmetry_pass
        and small_pass
        and large_pass
        and increment_pass
        and sector_pass
        and maximum_resolution_step < 6.0e-3
    )
    return {
        "artifact": "local_scalar_observer_clean_room_numerical_check",
        "status": ("pass_independent_computation_nonrigorous" if passed else "fail"),
        "independence_boundary": (
            "This script imports neither qgtoy nor the production Galerkin "
            "implementation. It is an author-side numerical audit, not an "
            "analytic proof or external review."
        ),
        "method": {
            "discretization": (
                "uniform midpoint Nystrom matrix with transformed "
                "Gauss-Legendre product integration on each logarithmic "
                "diagonal cell"
            ),
            "coarse_cell_count": coarse_count,
            "fine_cell_count": cell_count,
            "diagonal_quadrature_order": diagonal_order,
            "production_imports": [],
        },
        "checks": checks,
        "grid": grid,
        "small_support": small_rows,
        "large_support": large_rows,
        "thermal_increment": increment_rows,
        "coordinate_sector": {
            "grid_minimum_y": _rounded(float(sector_y[0])),
            "grid_maximum_y": _rounded(float(sector_y[-1])),
            "minimum_sampled_margin": _rounded(float(np.min(sector_margin))),
        },
        "source_sha256": {
            "experiments/local_scalar_observer_clean_room_check.py": _sha256(
                Path(__file__).resolve()
            )
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, default=160)
    parser.add_argument("--diagonal-order", type=int, default=32)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    record = build_record(
        cell_count=args.cells,
        diagonal_order=args.diagonal_order,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record["status"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
