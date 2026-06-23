#!/usr/bin/env python3
"""Independent numerical replay of the finite-pointer observer inequalities.

This script intentionally does not import ``qgtoy.finite_pointer_observer``.
It recomputes the channel purity, Jensen bound, Harlow orthogonal-state floor,
and branchwise gravity composition from their defining formulas.
"""

from __future__ import annotations

import hashlib
import json
from math import cos, cosh, exp, log, sin, tanh
from pathlib import Path
from random import Random


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments" / "finite_pointer_observer_clean_room_check.json"
CERTIFICATE = ROOT / "experiments" / "finite_pointer_observer_certificate.json"
TOLERANCE = 2.0e-12


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _difference(left: list[float], right: list[float]) -> list[float]:
    return [a - b for a, b in zip(left, right, strict=True)]


def _diagonal_form(vector: list[float], diagonal: list[float]) -> float:
    return sum(weight * value * value for weight, value in zip(
        diagonal,
        vector,
        strict=True,
    ))


def _case(seed: int) -> dict[str, float | int | bool]:
    rng = Random(seed)
    pointer_dimension = 2 + seed % 7
    profile_dimension = 1 + seed % 4
    raw_weights = [0.2 + rng.random() for _ in range(pointer_dimension)]
    total_weight = sum(raw_weights)
    weights = [value / total_weight for value in raw_weights]
    profiles = [
        [
            sin((state + 1) * (coordinate + 1) * 0.37)
            + 0.3 * cos((seed + 1) * (coordinate + 1) * 0.11)
            for coordinate in range(profile_dimension)
        ]
        for state in range(pointer_dimension)
    ]
    cost = 0.7 + 0.03 * seed
    covariance_diagonal = [
        0.5 * cost * (coordinate + 1) / profile_dimension
        for coordinate in range(profile_dimension)
    ]
    mean = [
        sum(weights[state] * profiles[state][coordinate] for state in range(
            pointer_dimension
        ))
        for coordinate in range(profile_dimension)
    ]
    centered_energy = 0.5 * sum(
        weights[state]
        * _dot(
            _difference(profiles[state], mean),
            _difference(profiles[state], mean),
        )
        for state in range(pointer_dimension)
    )
    pairwise_distance_average = 0.0
    purity = 0.0
    maximum_pairwise_cost_ratio = 0.0
    for left in range(pointer_dimension):
        for right in range(pointer_dimension):
            difference = _difference(profiles[left], profiles[right])
            norm_squared = _dot(difference, difference)
            quadratic = _diagonal_form(difference, covariance_diagonal)
            gamma = 0.25 * quadratic
            pair_weight = weights[left] * weights[right]
            pairwise_distance_average += pair_weight * norm_squared
            purity += pair_weight * exp(-2.0 * gamma)
            if norm_squared > 0.0:
                maximum_pairwise_cost_ratio = max(
                    maximum_pairwise_cost_ratio,
                    2.0 * quadratic / norm_squared,
                )
    classical_purity = sum(weight * weight for weight in weights)
    off_diagonal_weight = 1.0 - classical_purity
    purity_lower = classical_purity + off_diagonal_weight * exp(
        -cost * centered_energy / off_diagonal_weight
    )
    physical_entropy = -log(purity)
    entropy_upper = -log(purity_lower)
    return {
        "seed": seed,
        "pointer_dimension": pointer_dimension,
        "profile_dimension": profile_dimension,
        "centered_energy": centered_energy,
        "pairwise_distance_average": pairwise_distance_average,
        "pairwise_identity_error": abs(
            pairwise_distance_average - 4.0 * centered_energy
        ),
        "maximum_pairwise_cost_ratio": maximum_pairwise_cost_ratio,
        "cost_coefficient": cost,
        "physical_purity": purity,
        "purity_lower_bound": purity_lower,
        "physical_entropy": physical_entropy,
        "entropy_upper_bound": entropy_upper,
        "pairwise_cost_bound_holds": (
            maximum_pairwise_cost_ratio <= cost + TOLERANCE
        ),
        "purity_bound_holds": purity + TOLERANCE >= purity_lower,
        "entropy_bound_holds": physical_entropy <= entropy_upper + TOLERANCE,
    }


def main() -> None:
    cases = [_case(seed) for seed in range(1, 65)]

    binary_cost = 2.0
    binary_energy = 0.5
    binary_actual_purity = 0.5 + 0.5 * exp(-2.0)
    binary_lower_purity = 0.5 + 0.5 * exp(
        -binary_cost * binary_energy / 0.5
    )

    encoding_dimension = 1000
    physical_purity = 0.07
    purity_lower = 0.05
    finite_dimension_factor = encoding_dimension / (encoding_dimension + 2.0)
    exact_harlow_fluctuation = finite_dimension_factor * physical_purity
    harlow_floor = finite_dimension_factor * purity_lower

    support_ratio = 1.0
    numerical_cost = 1.0295979905445
    rigorous_cost_upper = 1.1594713304692
    geometric_factor = tanh(support_ratio) / cosh(support_ratio) ** 2 / 2.0
    numerical_area_coefficient = numerical_cost * geometric_factor
    rigorous_area_coefficient = rigorous_cost_upper * geometric_factor

    branch_weights = [0.5, 0.3, 0.2]
    branch_energies = [0.7, 0.9, 0.4]
    maximum_branch_energy = max(branch_energies)
    weighted_branch_energy = sum(
        weight * energy
        for weight, energy in zip(branch_weights, branch_energies, strict=True)
    )

    source_hashes = {
        str(Path(__file__).resolve().relative_to(ROOT)): _sha256(
            Path(__file__).resolve()
        ),
        str(CERTIFICATE.relative_to(ROOT)): _sha256(CERTIFICATE),
    }
    checks = {
        "all_pairwise_cost_bounds_hold": all(
            bool(case["pairwise_cost_bound_holds"]) for case in cases
        ),
        "all_purity_bounds_hold": all(
            bool(case["purity_bound_holds"]) for case in cases
        ),
        "all_entropy_bounds_hold": all(
            bool(case["entropy_bound_holds"]) for case in cases
        ),
        "maximum_pairwise_identity_error": max(
            float(case["pairwise_identity_error"]) for case in cases
        ),
        "binary_bound_saturates": abs(
            binary_actual_purity - binary_lower_purity
        )
        <= TOLERANCE,
        "harlow_floor_below_exact_fluctuation": (
            harlow_floor <= exact_harlow_fluctuation
        ),
        "branchwise_budget_controls_weighted_energy": (
            weighted_branch_energy <= maximum_branch_energy
        ),
        "rigorous_area_coefficient_dominates_numerical": (
            rigorous_area_coefficient >= numerical_area_coefficient
        ),
    }
    passed = (
        checks["all_pairwise_cost_bounds_hold"]
        and checks["all_purity_bounds_hold"]
        and checks["all_entropy_bounds_hold"]
        and checks["maximum_pairwise_identity_error"] <= TOLERANCE
        and checks["binary_bound_saturates"]
        and checks["harlow_floor_below_exact_fluctuation"]
        and checks["branchwise_budget_controls_weighted_energy"]
        and checks["rigorous_area_coefficient_dominates_numerical"]
    )
    record = {
        "artifact": "finite_pointer_observer_clean_room_check",
        "status": "pass_independent_computation_nonrigorous" if passed else "fail",
        "case_count": len(cases),
        "cases": cases,
        "checks": checks,
        "binary_saturation": {
            "actual_purity": binary_actual_purity,
            "lower_bound": binary_lower_purity,
        },
        "harlow_orthogonal_pair": {
            "encoding_dimension": encoding_dimension,
            "physical_purity": physical_purity,
            "purity_lower_bound": purity_lower,
            "exact_mean_square_fluctuation": exact_harlow_fluctuation,
            "certified_floor": harlow_floor,
        },
        "gravity_coefficients_at_y_one": {
            "numerical_nonrigorous": numerical_area_coefficient,
            "rigorous_upper": rigorous_area_coefficient,
        },
        "source_sha256": source_hashes,
        "scope": (
            "Independent finite-dimensional arithmetic replay only. The "
            "analytic proof establishes the continuum statement; this check "
            "does not certify literature novelty or coupled gravity."
        ),
    }
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "case_count": len(cases),
                "maximum_pairwise_identity_error": checks[
                    "maximum_pairwise_identity_error"
                ],
                "numerical_area_coefficient": numerical_area_coefficient,
                "rigorous_area_coefficient_upper": rigorous_area_coefficient,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
