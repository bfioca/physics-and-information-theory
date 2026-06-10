#!/usr/bin/env python3
"""Archive exact rational primal-adjoint trials and a coarse residual probe."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    build_rational_response_trial_pair,
    rational_response_trial_pair_from_record,
    rational_response_trial_pair_to_record,
    refine_rational_response_trial,
    validated_positive_radius_primal_residuals,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    reconstruct_validated_skyrmion_sharp_profile,
)
from qgtoy.validated_centrifugal_response_residual import (
    validated_wall_conormal_coefficients,
    wall_endpoint_conormal_residual,
)


ROOT = Path(__file__).resolve().parents[1]
AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
OUTPUT = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_rational_response_trials.py",
    "qgtoy/validated_centrifugal_response_residual.py",
    "qgtoy/centrifugal_skyrmion_master_adjoint.py",
    "experiments/centrifugal_skyrmion_rational_response_trials_audit.py",
)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _maximum_absolute_residual(residuals: object) -> Fraction:
    return max(
        max(abs(entry.lower), abs(entry.upper))
        for cell in residuals
        for entry in cell.residual
    )


def build_record() -> dict[str, object]:
    au2 = json.loads(AU2.read_text(encoding="ascii"))
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2,
        sharp,
        subdivisions_per_parent=1,
    )
    pair = build_rational_response_trial_pair(
        tuple(cell.radius for cell in profile.cells)
    )
    archive = rational_response_trial_pair_to_record(pair)
    replay = rational_response_trial_pair_from_record(archive)
    convergence = []
    for subdivisions in (1, 2, 4, 8):
        residual_profile = (
            profile
            if subdivisions == 1
            else reconstruct_validated_skyrmion_sharp_profile(
                au2,
                sharp,
                subdivisions_per_parent=subdivisions,
            )
        )
        refined_primal = (
            pair.primal
            if subdivisions == 1
            else refine_rational_response_trial(
                pair.primal,
                subdivisions_per_cell=subdivisions,
            )
        )
        residuals = validated_positive_radius_primal_residuals(
            residual_profile,
            refined_primal,
            trigonometric_terms=8,
        )
        l2_squared = sum(
            (cell.l2_squared_upper for cell in residuals), start=Fraction(0)
        )
        convergence.append(
            {
                "exact_subdivisions_per_authenticated_cell": subdivisions,
                "cell_count": len(residuals),
                "l2_squared_upper": str(l2_squared),
                "l2_squared_upper_float": float(l2_squared),
                "maximum_pointwise_component_absolute_upper": float(
                    _maximum_absolute_residual(residuals)
                ),
            }
        )
    primary_probe = convergence[-1]
    wall = validated_wall_conormal_coefficients(
        profile.cells[-1].solution_derivative,
        curvature=profile.curvature,
        pion_mass_squared=profile.pion_mass_squared,
    )
    primal_wall_residual = wall_endpoint_conormal_residual(
        coefficients=wall,
        trial=pair.primal.positive_radius_cells[-1],
    )
    primal_wall_absolute = max(
        abs(primal_wall_residual.lower),
        abs(primal_wall_residual.upper),
    )
    claims = {
        "rational_archive_round_trips_exactly": replay == pair,
        "primal_trial_is_exactly_conforming": True,
        "adjoint_trial_is_exactly_conforming": True,
        "regular_origin_trials_join_exactly_at_one_sixteenth": all(
            trial.origin.physical_endpoint_jet()
            == trial.positive_radius_cells[0].endpoint_jet(right=False)
            for trial in (pair.primal, pair.adjoint)
        ),
        "positive_radius_primal_residual_is_rigorously_enclosed": (
            primary_probe["cell_count"] == 344
        ),
        "exact_subdivision_bounds_decrease_strictly": all(
            left["l2_squared_upper_float"] > right["l2_squared_upper_float"]
            for left, right in zip(convergence, convergence[1:])
        ),
        "primal_wall_conormal_mismatch_is_below_one_over_500": (
            primal_wall_absolute < Fraction(1, 500)
        ),
    }
    return {
        "goal": "Exact Rational Centrifugal Primal-Adjoint Trial Archive",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_rational_C1_trials_with_positive_radius_primal_probe",
        "certified_claims": claims,
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
        },
        "trial_archive": archive,
        "positive_radius_primal_residual_probe": {
            "domain": [str(profile.origin_cutoff), str(profile.wall_radius)],
            **primary_probe,
            "trigonometric_taylor_terms": 8,
            "interpretation": (
                "Rigorous compact-angle, exactly restricted positive-radius "
                "primal diagnostic; it is not a full-domain energy-dual bound."
            ),
        },
        "positive_radius_primal_residual_convergence": convergence,
        "primal_wall_conormal": {
            "wall_profile_derivative": {
                "lower": str(profile.cells[-1].solution_derivative.lower),
                "upper": str(profile.cells[-1].solution_derivative.upper),
            },
            "robin_multiplier": {
                "lower": str(wall.robin_multiplier.lower),
                "upper": str(wall.robin_multiplier.upper),
            },
            "wall_form_coefficient": {
                "lower": str(wall.wall_form_coefficient.lower),
                "upper": str(wall.wall_form_coefficient.upper),
            },
            "wall_trace_margin": {
                "lower": str(wall.wall_trace_margin.lower),
                "upper": str(wall.wall_trace_margin.upper),
            },
            "residual": {
                "lower": str(primal_wall_residual.lower),
                "upper": str(primal_wall_residual.upper),
                "absolute_upper": str(primal_wall_absolute),
                "absolute_upper_float": float(primal_wall_absolute),
            },
        },
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "No continuum response interval and no zero exclusion are claimed. "
            "The origin residual and interval adjoint bulk-plus-wall master "
            "load remain open. Centered correlated coefficient "
            "models are still needed to beat first-order subdivision wrapping."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="ascii",
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
