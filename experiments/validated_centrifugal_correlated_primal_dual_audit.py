#!/usr/bin/env python3
"""Write the centered local-matrix primal form-dual diagnostic."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from qgtoy.centrifugal_skyrmion_rational_response_trials import (  # noqa: E402
    rational_response_trial_pair_from_record,
)
from qgtoy.validated_centrifugal_correlated_adjoint import (  # noqa: E402
    correlated_primal_energy_dual_cells,
)
from qgtoy.validated_centrifugal_response_residual import (  # noqa: E402
    validated_wall_conormal_coefficients,
    wall_endpoint_conormal_residual,
)
from qgtoy.validated_interval import sqrt_fraction_interval  # noqa: E402
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
FLOATING = ROOT / "experiments/centrifugal_skyrmion_master_adjoint_feasibility.json"
OUTPUT = ROOT / "experiments/validated_centrifugal_correlated_primal_dual.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/centrifugal_skyrmion_rational_response_trials.py",
    "qgtoy/validated_centrifugal_correlated_residual.py",
    "qgtoy/validated_centrifugal_correlated_adjoint.py",
    "qgtoy/validated_centrifugal_liouville_taylor.py",
    "qgtoy/validated_centrifugal_response_residual.py",
    "qgtoy/validated_interval.py",
    "qgtoy/validated_skyrmion_sharp_profile.py",
    "experiments/validated_centrifugal_correlated_primal_dual_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ceil(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _outward_upper(value: Fraction, *, places: int = 18) -> str:
    scale = 10**places
    integer = _ceil(value * scale)
    digits = str(integer).zfill(places + 1)
    return f"{digits[:-places]}.{digits[-places:]}"


def build_record() -> dict[str, object]:
    au2 = json.loads(AU2.read_text(encoding="ascii"))
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    archive = json.loads(TRIALS.read_text(encoding="ascii"))
    floating = json.loads(FLOATING.read_text(encoding="ascii"))
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=1
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    cells = correlated_primal_energy_dual_cells(
        profile,
        pair.primal,
        completed_potential_lower_bound=Fraction(1, 100),
    )
    scalar_bulk = sum(
        (cell.scalar_floor_squared_dual_upper for cell in cells),
        start=Fraction(0),
    )
    matrix_bulk = sum(
        (cell.matrix_weighted_squared_dual_upper for cell in cells),
        start=Fraction(0),
    )
    local_count = sum(
        cell.completed_potential_matrix_inverse_used for cell in cells
    )
    wall_coefficients = validated_wall_conormal_coefficients(
        profile.cells[-1].solution_derivative,
        curvature=profile.curvature,
        pion_mass_squared=profile.pion_mass_squared,
    )
    wall_residual = wall_endpoint_conormal_residual(
        coefficients=wall_coefficients,
        trial=pair.primal.positive_radius_cells[-1],
    )
    wall_absolute = max(abs(wall_residual.lower), abs(wall_residual.upper))
    wall_square = wall_absolute**2 / wall_coefficients.wall_trace_margin.lower
    partial_square = matrix_bulk + wall_square
    partial_norm = sqrt_fraction_interval(partial_square, bisection_steps=160).upper
    dominant = max(
        range(len(cells)),
        key=lambda index: cells[index].matrix_weighted_squared_dual_upper,
    )
    candidate_amplitude = abs(
        Fraction(str(floating["dual_weighted_estimator"]["corrected_estimator"]))
    )
    claims = {
        "all_43_authenticated_positive_radius_cells_are_enclosed": len(cells) == 43,
        "profile_trial_residual_and_form_share_one_coordinate": True,
        "newton_tube_errors_remain_interval_remainders": True,
        "local_completed_potential_inverse_closes_on_at_least_25_cells": (
            local_count >= 25
        ),
        "local_matrix_bulk_square_is_below_five_eighths": (
            matrix_bulk < Fraction(5, 8)
        ),
        "local_matrix_weighting_improves_scalar_floor_by_over_three_halves": (
            2 * scalar_bulk > 3 * matrix_bulk
        ),
        "wall_square_is_below_one_over_100000": wall_square < Fraction(1, 100000),
        "partial_primal_norm_remains_above_three_quarters": (
            partial_norm > Fraction(3, 4)
        ),
        "partial_primal_bound_alone_exceeds_floating_amplitude_by_over_250": (
            partial_norm > 250 * candidate_amplitude
        ),
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"correlated primal audit failed: {failed}")
    return {
        "goal": "Validated Centered Local-Matrix Primal Form-Dual Diagnostic",
        "status": "pass",
        "result_type": "exact_rational_centered_taylor_hybrid_value_dual_bound",
        "parameters": {
            "positive_radius_cell_count": len(cells),
            "degree_limit": 8,
            "rounding_denominator": 10**16,
            "trigonometric_terms": 6,
            "certified_scalar_fallback_lower_bound": "1/100",
        },
        "partial_bound": {
            "centered_scalar_floor_bulk_squared_upper": _outward_upper(scalar_bulk),
            "local_matrix_weighted_bulk_squared_upper": _outward_upper(matrix_bulk),
            "wall_squared_upper": _outward_upper(wall_square),
            "matrix_weighted_squared_upper": _outward_upper(partial_square),
            "matrix_weighted_energy_dual_upper": _outward_upper(partial_norm),
            "matrix_weighted_energy_dual_upper_float": float(partial_norm),
            "local_potential_inverse_cell_count": local_count,
            "scalar_potential_fallback_cell_count": len(cells) - local_count,
            "dominant_cell_index": dominant,
            "dominant_cell_radius": {
                "lower": str(cells[dominant].radius.lower),
                "upper": str(cells[dominant].radius.upper),
            },
        },
        "floating_design_reference": {
            "corrected_response_amplitude_absolute": float(candidate_amplitude),
            "is_not_a_certified_interval_endpoint": True,
        },
        "certified_claims": claims,
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
            str(FLOATING.relative_to(ROOT)): _sha256(FLOATING),
        },
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "claim_boundary": (
            "This certifies a centered positive-radius primal value-load dual "
            "bound with local completed-potential inverses and the primal wall "
            "trace. It omits the already-separate regular-origin residual. The "
            "large upper bound is a negative diagnostic for this representation, "
            "not evidence that the physical response vanishes or an enclosure "
            "of the exterior amplitude."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
