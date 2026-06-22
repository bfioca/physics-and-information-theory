#!/usr/bin/env python3
"""Numerically realize the exact compact KMS observer-cost kernel.

The zero-temperature logarithmic kernel is integrated exactly against a
piecewise-constant Galerkin basis. Only the smooth finite-temperature
correction is evaluated by Gauss-Legendre quadrature. The resulting values are
numerical Rayleigh-Ritz estimates, not replacements for the analytic theorem
or its rigorous lower and upper bounds.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from math import asinh, log, pi
from pathlib import Path
from typing import Iterable

import numpy as np

from qgtoy.local_scalar_observer_cost import (
    sharp_observer_cost_characterization,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = (
    ROOT / "paper/local_scalar_observer_cost/data/observer_cost_spectrum.json"
)
DEFAULT_FIGURE = (
    ROOT / "paper/local_scalar_observer_cost/figures/observer_cost_spectrum.pdf"
)
DEFAULT_PREVIEW = (
    ROOT / "paper/local_scalar_observer_cost/figures/observer_cost_spectrum.svg"
)
Y_GRID = (
    0.03,
    0.04,
    0.06,
    0.08,
    0.1,
    0.15,
    0.2,
    0.3,
    0.5,
    0.7,
    1.0,
    1.5,
    2.0,
    3.0,
    5.0,
    7.0,
    10.0,
    15.0,
    20.0,
)
PROFILE_Y = (0.1, 1.0, 10.0)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _second_log_primitive(values: np.ndarray) -> np.ndarray:
    """Return F with F''(z)=log|z| and continuous value F(0)=0."""
    result = np.zeros_like(values, dtype=float)
    mask = np.abs(values) > 0.0
    selected = values[mask]
    result[mask] = 0.5 * selected**2 * np.log(np.abs(selected)) - 0.75 * (
        selected**2
    )
    return result


def vacuum_piecewise_constant_matrix(cell_count: int) -> np.ndarray:
    """Exact Galerkin matrix of pi^-1 log[(u+v)/|u-v|] on (0,1)."""
    if isinstance(cell_count, bool) or cell_count < 2:
        raise ValueError("cell_count must be an integer at least two")
    edges = np.linspace(0.0, 1.0, cell_count + 1)
    left = edges[:-1]
    right = edges[1:]
    ai = left[:, None]
    bi = right[:, None]
    aj = left[None, :]
    bj = right[None, :]
    plus = (
        _second_log_primitive(bi + bj)
        - _second_log_primitive(ai + bj)
        - _second_log_primitive(bi + aj)
        + _second_log_primitive(ai + aj)
    )
    difference_corner = (
        _second_log_primitive(bi - bj)
        - _second_log_primitive(ai - bj)
        - _second_log_primitive(bi - aj)
        + _second_log_primitive(ai - aj)
    )
    cell_width = 1.0 / cell_count
    matrix = (plus + difference_corner) / (pi * cell_width)
    return 0.5 * (matrix + matrix.T)


def _log_sinh_over_argument(values: np.ndarray) -> np.ndarray:
    """Stable log[sinh(z)/z] for nonnegative arrays, with value zero at z=0."""
    result = np.zeros_like(values, dtype=float)
    small = (values > 0.0) & (values < 0.25)
    z = values[small]
    result[small] = (
        z**2 / 6.0
        - z**4 / 180.0
        + z**6 / 2835.0
        - z**8 / 37800.0
        + z**10 / 467775.0
    )
    large = values >= 0.25
    z = values[large]
    result[large] = (
        z - log(2.0) + np.log1p(-np.exp(-2.0 * z)) - np.log(z)
    )
    return result


def thermal_correction_piecewise_constant_matrix(
    cell_count: int,
    thermal_support_ratio: float,
    *,
    quadrature_order: int,
) -> np.ndarray:
    """Galerkin matrix of the smooth correction k_tau-k_0."""
    if thermal_support_ratio < 0.0:
        raise ValueError("thermal_support_ratio must be nonnegative")
    if isinstance(quadrature_order, bool) or quadrature_order < 2:
        raise ValueError("quadrature_order must be an integer at least two")
    if thermal_support_ratio == 0.0:
        return np.zeros((cell_count, cell_count), dtype=float)
    nodes, weights = np.polynomial.legendre.leggauss(quadrature_order)
    cell_width = 1.0 / cell_count
    centers = (np.arange(cell_count, dtype=float) + 0.5) * cell_width
    points = centers[:, None] + 0.5 * cell_width * nodes[None, :]
    local_weights = 0.5 * cell_width * weights
    flat = points.reshape(-1)
    tau = thermal_support_ratio
    summed = tau * (flat[:, None] + flat[None, :])
    separated = tau * np.abs(flat[:, None] - flat[None, :])
    kernel = (
        _log_sinh_over_argument(summed)
        - _log_sinh_over_argument(separated)
    ) / pi
    blocks = kernel.reshape(
        cell_count,
        quadrature_order,
        cell_count,
        quadrature_order,
    )
    integrals = np.einsum(
        "a,iajb,b->ij",
        local_weights,
        blocks,
        local_weights,
        optimize=True,
    )
    matrix = integrals / cell_width
    return 0.5 * (matrix + matrix.T)


def kms_piecewise_constant_matrix(
    cell_count: int,
    support_ratio: float,
    *,
    quadrature_order: int,
) -> np.ndarray:
    """Return the dimensionless K_{y/2} Galerkin matrix."""
    if support_ratio <= 0.0:
        raise ValueError("support_ratio must be positive")
    return vacuum_piecewise_constant_matrix(cell_count) + (
        thermal_correction_piecewise_constant_matrix(
            cell_count,
            0.5 * support_ratio,
            quadrature_order=quadrature_order,
        )
    )


def galerkin_cost_estimate(
    support_ratio: float,
    *,
    cell_count: int,
    quadrature_order: int,
) -> tuple[float, np.ndarray]:
    """Return 2y times the top matrix eigenvalue and its positive vector."""
    matrix = kms_piecewise_constant_matrix(
        cell_count,
        support_ratio,
        quadrature_order=quadrature_order,
    )
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    vector = eigenvectors[:, -1]
    if float(np.sum(vector)) < 0.0:
        vector = -vector
    return 2.0 * support_ratio * float(eigenvalues[-1]), vector


def _rigorous_bounds(support_ratio: float) -> tuple[float, float, float]:
    y = support_ratio
    lower = max(3.0 * y / pi, 8.0 * y**2 / pi**3)
    record = sharp_observer_cost_characterization(y, static_patch_radius=1.0)
    row_upper = float(record["exact_row_schur_upper_coefficient"])
    legacy_upper = 4.0 * asinh(1.0) * y / pi + 8.0 * y**2 / pi**3
    return lower, row_upper, legacy_upper


def _rounded(value: float) -> float:
    return float(f"{value:.14g}")


def build_spectrum_record(
    *,
    cell_count: int,
    quadrature_order: int,
) -> dict[str, object]:
    """Build the frozen convergence and profile record."""
    if cell_count < 32 or cell_count % 4:
        raise ValueError("cell_count must be a multiple of four and at least 32")
    cache: dict[tuple[int, float, int], tuple[float, np.ndarray]] = {}

    def estimate(n: int, y: float, q: int) -> tuple[float, np.ndarray]:
        key = (n, y, q)
        if key not in cache:
            cache[key] = galerkin_cost_estimate(
                y,
                cell_count=n,
                quadrature_order=q,
            )
        return cache[key]

    curve: list[dict[str, float]] = []
    bracket_pass = True
    for y in Y_GRID:
        cost, _ = estimate(cell_count, y, quadrature_order)
        lower, row_upper, legacy_upper = _rigorous_bounds(y)
        bracket_pass = bracket_pass and lower <= cost <= row_upper
        curve.append(
            {
                "support_ratio_y": y,
                "galerkin_cost": _rounded(cost),
                "rigorous_lower": _rounded(lower),
                "rigorous_row_schur_upper": _rounded(row_upper),
                "legacy_F_upper": _rounded(legacy_upper),
            }
        )

    resolutions = (cell_count // 4, cell_count // 2, cell_count)
    convergence: list[dict[str, object]] = []
    maximum_relative_step = 0.0
    monotone_pass = True
    for y in PROFILE_Y:
        values = [estimate(n, y, quadrature_order)[0] for n in resolutions]
        monotone = all(
            right >= left - 2.0e-12 * max(1.0, abs(right))
            for left, right in zip(values, values[1:])
        )
        relative_step = abs(values[-1] - values[-2]) / values[-1]
        maximum_relative_step = max(maximum_relative_step, relative_step)
        monotone_pass = monotone_pass and monotone
        convergence.append(
            {
                "support_ratio_y": y,
                "cell_counts": list(resolutions),
                "cost_estimates": [_rounded(value) for value in values],
                "nested_estimates_monotone": monotone,
                "last_relative_step": _rounded(relative_step),
            }
        )

    quadrature_comparison: list[dict[str, float]] = []
    maximum_quadrature_relative_difference = 0.0
    comparison_cells = cell_count // 2
    comparison_order = max(4, quadrature_order - 4)
    for y in PROFILE_Y:
        lower_order = estimate(comparison_cells, y, comparison_order)[0]
        main_order = estimate(comparison_cells, y, quadrature_order)[0]
        difference = abs(main_order - lower_order) / main_order
        maximum_quadrature_relative_difference = max(
            maximum_quadrature_relative_difference,
            difference,
        )
        quadrature_comparison.append(
            {
                "support_ratio_y": y,
                "cell_count": comparison_cells,
                "lower_quadrature_order": comparison_order,
                "main_quadrature_order": quadrature_order,
                "relative_difference": _rounded(difference),
            }
        )

    profiles: list[dict[str, object]] = []
    centers = (np.arange(cell_count, dtype=float) + 0.5) / cell_count
    for y in PROFILE_Y:
        _, vector = estimate(cell_count, y, quadrature_order)
        normalized = vector / float(np.max(vector))
        profiles.append(
            {
                "support_ratio_y": y,
                "cell_centers_u": [_rounded(value) for value in centers],
                "profile_relative_to_maximum": [
                    _rounded(value) for value in normalized
                ],
                "minimum_component": _rounded(float(np.min(normalized))),
            }
        )

    checks = {
        "all_curve_estimates_inside_rigorous_bracket": bracket_pass,
        "nested_resolution_estimates_monotone": monotone_pass,
        "maximum_last_resolution_relative_step": _rounded(
            maximum_relative_step
        ),
        "maximum_quadrature_relative_difference": _rounded(
            maximum_quadrature_relative_difference
        ),
        "all_profile_components_positive": all(
            float(profile["minimum_component"]) > 0.0 for profile in profiles
        ),
    }
    passed = (
        bracket_pass
        and monotone_pass
        and maximum_relative_step < 5.0e-4
        and maximum_quadrature_relative_difference < 1.0e-8
        and bool(checks["all_profile_components_positive"])
    )
    return {
        "artifact": "local_scalar_observer_cost_spectrum",
        "status": "numerical_convergence_pass_nonrigorous" if passed else "fail",
        "method": {
            "basis": "normalized piecewise constants on a uniform partition",
            "vacuum_kernel": (
                "cell integrals of pi^-1*log((u+v)/abs(u-v)) evaluated "
                "exactly from F''(z)=log(abs(z))"
            ),
            "thermal_correction": (
                "Gauss-Legendre quadrature of the smooth difference "
                "log(sinh(z)/z)"
            ),
            "spectral_method": "symmetric Rayleigh-Ritz matrix eigenproblem",
            "scope": (
                "Numerical realization only. Rigorous claims use the analytic "
                "lower and Schur upper bounds in the manuscript."
            ),
            "cell_count": cell_count,
            "quadrature_order": quadrature_order,
        },
        "checks": checks,
        "curve": curve,
        "convergence": convergence,
        "quadrature_comparison": quadrature_comparison,
        "profiles": profiles,
        "source_sha256": {
            "experiments/local_scalar_observer_spectrum.py": _sha256(
                Path(__file__).resolve()
            ),
            "qgtoy/local_scalar_observer_cost.py": _sha256(
                ROOT / "qgtoy/local_scalar_observer_cost.py"
            ),
        },
    }


def _pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _polyline(
    commands: list[str],
    points: Iterable[tuple[float, float]],
    *,
    color: tuple[float, float, float],
    width: float,
    dash: str = "[] 0 d",
) -> None:
    coordinates = list(points)
    if len(coordinates) < 2:
        return
    commands.append(f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} RG")
    commands.append(f"{width:.2f} w {dash}")
    commands.append(f"{coordinates[0][0]:.2f} {coordinates[0][1]:.2f} m")
    commands.extend(f"{x:.2f} {y:.2f} l" for x, y in coordinates[1:])
    commands.append("S")


def _text(
    commands: list[str],
    x: float,
    y: float,
    value: str,
    *,
    size: float = 8.0,
    bold: bool = False,
) -> None:
    font = "F2" if bold else "F1"
    commands.append(
        f"0 0 0 rg BT /{font} {size:.1f} Tf {x:.2f} {y:.2f} Td "
        f"({_pdf_escape(value)}) Tj ET"
    )


def _write_simple_pdf(path: Path, commands: list[str]) -> None:
    stream = ("\n".join(commands) + "\n").encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 720 330] "
            b"/Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> "
            b"/Contents 4 0 R >>"
        ),
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n"
        + stream
        + b"endstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    ]
    payload = bytearray(b"%PDF-1.4\n% deterministic vector figure\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{index} 0 obj\n".encode("ascii"))
        payload.extend(obj)
        payload.extend(b"\nendobj\n")
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n"
        ).encode("ascii")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _write_svg_preview(path: Path, commands: list[str]) -> None:
    """Translate the small drawing-command subset into an inspectable SVG."""
    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="660" '
        'viewBox="0 0 720 330">',
        '<rect width="720" height="330" fill="white"/>',
    ]
    stroke = (0, 0, 0)
    width = 1.0
    dash = ""
    points: list[tuple[float, float]] = []
    for command in commands:
        color_match = re.fullmatch(
            r"([0-9.]+) ([0-9.]+) ([0-9.]+) RG",
            command,
        )
        if color_match:
            stroke = tuple(
                round(255.0 * float(value)) for value in color_match.groups()
            )
            continue
        style_match = re.fullmatch(
            r"([0-9.]+) w \[([^]]*)\] 0 d",
            command,
        )
        if style_match:
            width = float(style_match.group(1))
            dash = style_match.group(2).strip().replace(" ", ",")
            continue
        move_match = re.fullmatch(r"([0-9.]+) ([0-9.]+) m", command)
        if move_match:
            points = [(float(move_match.group(1)), float(move_match.group(2)))]
            continue
        line_match = re.fullmatch(r"([0-9.]+) ([0-9.]+) l", command)
        if line_match:
            points.append((float(line_match.group(1)), float(line_match.group(2))))
            continue
        if command == "S" and len(points) >= 2:
            coordinates = " ".join(f"{x:.2f},{330.0-y:.2f}" for x, y in points)
            dash_attribute = (
                f' stroke-dasharray="{html.escape(dash)}"' if dash else ""
            )
            elements.append(
                f'<polyline points="{coordinates}" fill="none" '
                f'stroke="rgb{stroke}" stroke-width="{width:.2f}"'
                f'{dash_attribute} stroke-linecap="round" '
                'stroke-linejoin="round"/>'
            )
            points = []
            continue
        text_match = re.fullmatch(
            r"0 0 0 rg BT /(F[12]) ([0-9.]+) Tf ([0-9.]+) ([0-9.]+) "
            r"Td \((.*)\) Tj ET",
            command,
        )
        if text_match:
            font, size, x_value, y_value, value = text_match.groups()
            value = value.replace("\\(", "(").replace("\\)", ")")
            value = value.replace("\\\\", "\\")
            weight = "bold" if font == "F2" else "normal"
            elements.append(
                f'<text x="{float(x_value):.2f}" y="{330.0-float(y_value):.2f}" '
                f'font-family="Helvetica,Arial,sans-serif" '
                f'font-size="{float(size):.1f}" font-weight="{weight}" '
                f'fill="black">{html.escape(value)}</text>'
            )
    elements.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(elements) + "\n", encoding="ascii")


def render_spectrum_figure(
    record: dict[str, object],
    output: Path,
) -> list[str]:
    """Render the frozen curve and optimizer profiles as a vector PDF."""
    commands: list[str] = ["1 J 1 j"]
    left_x, left_y, left_w, left_h = 54.0, 48.0, 304.0, 230.0
    right_x, right_y, right_w, right_h = 412.0, 48.0, 270.0, 230.0
    black = (0.12, 0.12, 0.12)
    gray = (0.45, 0.45, 0.45)
    light = (0.68, 0.68, 0.68)
    blue = (0.10, 0.32, 0.68)
    orange = (0.88, 0.35, 0.10)
    green = (0.15, 0.55, 0.32)

    _text(commands, 54, 307, "(a) Sharp cost and rigorous bracket", size=10, bold=True)
    _text(commands, 412, 307, "(b) Normalized optimal momentum profile", size=10, bold=True)

    x_min, x_max = log(0.03, 10), log(20.0, 10)
    y_min, y_max = log(0.02, 10), log(140.0, 10)

    def left_map(x_value: float, y_value: float) -> tuple[float, float]:
        x = left_x + left_w * (log(x_value, 10) - x_min) / (x_max - x_min)
        y = left_y + left_h * (log(y_value, 10) - y_min) / (y_max - y_min)
        return x, y

    _polyline(
        commands,
        ((left_x, left_y), (left_x + left_w, left_y)),
        color=black,
        width=0.8,
    )
    _polyline(
        commands,
        ((left_x, left_y), (left_x, left_y + left_h)),
        color=black,
        width=0.8,
    )
    for value in (0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 20.0):
        x, _ = left_map(value, 0.02)
        _polyline(commands, ((x, left_y), (x, left_y - 4)), color=black, width=0.5)
        label = f"{value:g}"
        _text(commands, x - 5.0, left_y - 15.0, label, size=7)
    for value in (0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0):
        _, y = left_map(0.03, value)
        _polyline(commands, ((left_x - 4, y), (left_x, y)), color=black, width=0.5)
        _text(commands, left_x - 29.0, y - 2.5, f"{value:g}", size=7)
    _text(commands, left_x + 132, 20, "support ratio y=L/R", size=8)

    curve = record["curve"]
    if not isinstance(curve, list):
        raise TypeError("curve data missing")
    _polyline(
        commands,
        (
            left_map(float(row["support_ratio_y"]), float(row["legacy_F_upper"]))
            for row in curve
        ),
        color=light,
        width=1.0,
        dash="[2 3] 0 d",
    )
    _polyline(
        commands,
        (
            left_map(
                float(row["support_ratio_y"]),
                float(row["rigorous_row_schur_upper"]),
            )
            for row in curve
        ),
        color=orange,
        width=1.4,
    )
    _polyline(
        commands,
        (
            left_map(float(row["support_ratio_y"]), float(row["galerkin_cost"]))
            for row in curve
        ),
        color=blue,
        width=2.0,
    )
    _polyline(
        commands,
        (
            left_map(float(row["support_ratio_y"]), float(row["rigorous_lower"]))
            for row in curve
        ),
        color=gray,
        width=1.0,
        dash="[5 3] 0 d",
    )
    legend_y = 292.0
    for x0, color, width, dash, label in (
        (58, blue, 2.0, "[] 0 d", "Galerkin N=128"),
        (151, orange, 1.4, "[] 0 d", "Schur upper"),
        (231, gray, 1.0, "[5 3] 0 d", "rigorous lower"),
        (314, light, 1.0, "[2 3] 0 d", "F(y)"),
    ):
        _polyline(commands, ((x0, legend_y), (x0 + 15, legend_y)), color=color, width=width, dash=dash)
        _text(commands, x0 + 18, legend_y - 2.5, label, size=6.5)

    _polyline(
        commands,
        ((right_x, right_y), (right_x + right_w, right_y)),
        color=black,
        width=0.8,
    )
    _polyline(
        commands,
        ((right_x, right_y), (right_x, right_y + right_h)),
        color=black,
        width=0.8,
    )

    def right_map(u: float, value: float) -> tuple[float, float]:
        return right_x + right_w * u, right_y + right_h * value / 1.05

    for value in (0.0, 0.25, 0.5, 0.75, 1.0):
        x, _ = right_map(value, 0.0)
        _polyline(commands, ((x, right_y), (x, right_y - 4)), color=black, width=0.5)
        _text(commands, x - 5, right_y - 15, f"{value:g}", size=7)
        _, y = right_map(0.0, value)
        _polyline(commands, ((right_x - 4, y), (right_x, y)), color=black, width=0.5)
        _text(commands, right_x - 25, y - 2.5, f"{value:g}", size=7)
    _text(commands, right_x + 124, 20, "u=x/L", size=8)

    profiles = record["profiles"]
    if not isinstance(profiles, list):
        raise TypeError("profile data missing")
    for profile, color in zip(profiles, (blue, green, orange)):
        centers = profile["cell_centers_u"]
        values = profile["profile_relative_to_maximum"]
        _polyline(
            commands,
            (right_map(float(u), float(value)) for u, value in zip(centers, values)),
            color=color,
            width=1.8,
        )
    for x0, color, label in (
        (430, blue, "y=0.1"),
        (510, green, "y=1"),
        (575, orange, "y=10"),
    ):
        _polyline(commands, ((x0, 292), (x0 + 18, 292)), color=color, width=1.8)
        _text(commands, x0 + 22, 289.5, label, size=7)
    _text(
        commands,
        390,
        6,
        "Numerical Rayleigh-Ritz realization; theorem bounds remain analytic.",
        size=6.5,
    )
    _write_simple_pdf(output, commands)
    return commands


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cells", type=int, default=128)
    parser.add_argument("--quadrature-order", type=int, default=12)
    parser.add_argument("--output-data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output-figure", type=Path, default=DEFAULT_FIGURE)
    parser.add_argument("--output-preview", type=Path, default=DEFAULT_PREVIEW)
    args = parser.parse_args()
    record = build_spectrum_record(
        cell_count=args.cells,
        quadrature_order=args.quadrature_order,
    )
    figure = args.output_figure.resolve()
    commands = render_spectrum_figure(record, figure)
    preview = args.output_preview.resolve()
    _write_svg_preview(preview, commands)
    record["figure"] = {
        "path": str(figure.relative_to(ROOT)),
        "sha256": _sha256(figure),
        "preview_path": str(preview.relative_to(ROOT)),
        "preview_sha256": _sha256(preview),
    }
    data = args.output_data.resolve()
    data.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    data.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "status": record["status"],
                "data": str(data),
                "data_sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "figure": str(figure),
                "figure_sha256": record["figure"]["sha256"],
                "preview": str(preview),
                "preview_sha256": record["figure"]["preview_sha256"],
                "maximum_last_resolution_relative_step": record["checks"][
                    "maximum_last_resolution_relative_step"
                ],
                "maximum_quadrature_relative_difference": record["checks"][
                    "maximum_quadrature_relative_difference"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
