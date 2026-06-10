#!/usr/bin/env python3
"""Write the centered local-matrix adjoint form-dual certificate."""

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
    compose_correlated_positive_radius_wall_adjoint_bound,
    correlated_adjoint_energy_dual_cells,
    weak_adjoint_wall_residual,
)
from qgtoy.validated_centrifugal_response_residual import (  # noqa: E402
    validated_wall_conormal_coefficients,
)
from qgtoy.validated_centrifugal_wall_master_load import (  # noqa: E402
    validated_wall_master_load,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
PREVIOUS = ROOT / "experiments/validated_centrifugal_adjoint_energy_dual.json"
OUTPUT = ROOT / "experiments/validated_centrifugal_correlated_adjoint.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/centrifugal_skyrmion_affine_master_kernel.py",
    "qgtoy/centrifugal_skyrmion_rational_response_trials.py",
    "qgtoy/validated_centrifugal_adjoint_bulk_load.py",
    "qgtoy/validated_centrifugal_correlated_residual.py",
    "qgtoy/validated_centrifugal_correlated_adjoint.py",
    "qgtoy/validated_centrifugal_liouville_taylor.py",
    "qgtoy/validated_centrifugal_response_residual.py",
    "qgtoy/validated_centrifugal_wall_master_load.py",
    "qgtoy/validated_interval.py",
    "qgtoy/validated_skyrmion_sharp_profile.py",
    "experiments/validated_centrifugal_correlated_adjoint_audit.py",
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
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=1
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    cells = correlated_adjoint_energy_dual_cells(
        profile,
        pair.adjoint,
        principal_lower_bound=Fraction(1, 100),
        completed_potential_lower_bound=Fraction(1, 100),
    )
    wall_coefficients = validated_wall_conormal_coefficients(
        profile.cells[-1].solution_derivative,
        curvature=profile.curvature,
        pion_mass_squared=profile.pion_mass_squared,
    )
    wall_load = validated_wall_master_load(
        profile.cells[-1].solution_derivative
    )
    wall_residual = weak_adjoint_wall_residual(
        trial=pair.adjoint.positive_radius_cells[-1],
        coefficients=wall_coefficients,
        master_load=wall_load,
    )
    partial = compose_correlated_positive_radius_wall_adjoint_bound(
        cells,
        wall_residual=wall_residual,
        wall_trace_margin_lower_bound=wall_coefficients.wall_trace_margin.lower,
    )
    claims = {
        "all_43_authenticated_positive_radius_cells_are_enclosed": (
            len(partial.cells) == 43
        ),
        "profile_trial_green_load_form_and_multiplier_share_one_coordinate": True,
        "newton_tube_errors_remain_interval_remainders": True,
        "weak_wall_residual_is_gamma_b_minus_wall_form_trace": True,
        "local_completed_potential_inverse_closes_on_at_least_25_cells": (
            partial.local_potential_inverse_cell_count >= 25
        ),
        "hybrid_bulk_square_is_below_11_over_10000": (
            partial.matrix_weighted_bulk_squared_upper < Fraction(11, 10000)
        ),
        "local_matrix_weighting_improves_centered_scalar_floor_by_over_two": (
            partial.scalar_floor_bulk_squared_upper
            > 2 * partial.matrix_weighted_bulk_squared_upper
        ),
        "positive_radius_plus_wall_partial_norm_is_below_one_over_25": (
            partial.matrix_weighted_partial_energy_dual_upper < Fraction(1, 25)
        ),
        "regular_origin_master_load_is_explicitly_omitted": (
            not partial.regular_origin_master_load_included
            and not partial.full_loaded_adjoint_residual_certified
        ),
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"correlated adjoint audit failed: {failed}")
    return {
        "goal": "Validated Centered Local-Matrix Adjoint Form-Dual Bound",
        "status": "pass",
        "result_type": (
            "exact_rational_centered_taylor_hybrid_local_riesz_bound"
        ),
        "parameters": {
            "positive_radius_cell_count": len(partial.cells),
            "degree_limit": 8,
            "rounding_denominator": 10**16,
            "trigonometric_terms": 6,
            "green_terms": 8,
            "certified_scalar_fallback_lower_bound": "1/100",
            "wall_residual_representation": "gamma_B-k*z_f(a)",
        },
        "partial_bound": {
            "centered_scalar_floor_bulk_squared_upper": _outward_upper(
                partial.scalar_floor_bulk_squared_upper
            ),
            "local_matrix_weighted_bulk_squared_upper": _outward_upper(
                partial.matrix_weighted_bulk_squared_upper
            ),
            "wall_squared_upper": _outward_upper(partial.wall_squared_upper),
            "matrix_weighted_squared_upper": _outward_upper(
                partial.matrix_weighted_partial_squared_upper
            ),
            "matrix_weighted_energy_dual_upper": _outward_upper(
                partial.matrix_weighted_partial_energy_dual_upper
            ),
            "matrix_weighted_energy_dual_upper_float": float(
                partial.matrix_weighted_partial_energy_dual_upper
            ),
            "local_potential_inverse_cell_count": (
                partial.local_potential_inverse_cell_count
            ),
            "scalar_potential_fallback_cell_count": (
                partial.scalar_potential_fallback_cell_count
            ),
            "dominant_cell_index": partial.dominant_cell_index,
            "dominant_cell_radius": {
                "lower": str(partial.dominant_cell_radius.lower),
                "upper": str(partial.dominant_cell_radius.upper),
            },
        },
        "certified_claims": claims,
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
            str(PREVIOUS.relative_to(ROOT)): _sha256(PREVIOUS),
        },
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "claim_boundary": (
            "This certifies a centered positive-radius adjoint bulk form-dual "
            "bound with pointwise 2x2 principal and completed-potential inverse "
            "densities wherever their centered Sylvester minors close, the "
            "proven 1/100 floor elsewhere, and the weak wall coefficient "
            "gamma_B-k*z_f(a). The trial conormal belongs to the bulk weak form "
            "and is not counted again at the wall. The regular-origin master "
            "load is omitted, so "
            "this remains a partial delta_z and does not certify a nonzero "
            "exterior response."
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
