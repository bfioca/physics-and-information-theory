#!/usr/bin/env python3
"""Write the centered signed positive-radius corrected-estimator artifact."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_rational_response_trials import (  # noqa: E402
    rational_response_trial_pair_from_record,
)
from qgtoy.validated_centrifugal_correlated_estimator import (  # noqa: E402
    correlated_positive_radius_corrected_estimator,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
OUTPUT = ROOT / "experiments/validated_centrifugal_correlated_estimator.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/centrifugal_skyrmion_rational_response_trials.py",
    "qgtoy/validated_centrifugal_adjoint_bulk_load.py",
    "qgtoy/validated_centrifugal_correlated_adjoint.py",
    "qgtoy/validated_centrifugal_correlated_residual.py",
    "qgtoy/validated_centrifugal_correlated_estimator.py",
    "qgtoy/validated_centrifugal_liouville_taylor.py",
    "qgtoy/validated_interval.py",
    "qgtoy/validated_skyrmion_sharp_profile.py",
    "experiments/validated_centrifugal_correlated_estimator_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _ceil(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _decimal(integer: int, places: int) -> str:
    sign = "-" if integer < 0 else ""
    digits = str(abs(integer)).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


def _outward_interval(value: RationalInterval, *, places: int = 18) -> dict[str, object]:
    scale = 10**places
    return {
        "lower": _decimal(_floor(value.lower * scale), places),
        "upper": _decimal(_ceil(value.upper * scale), places),
        "lower_float": float(value.lower),
        "upper_float": float(value.upper),
        "width_upper": _decimal(_ceil(value.width * scale), places),
        "representation": f"outward_decimal_enclosure_{places}_places",
    }


def build_record() -> dict[str, object]:
    au2 = json.loads(AU2.read_text(encoding="ascii"))
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    archive = json.loads(TRIALS.read_text(encoding="ascii"))
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=1
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    result = correlated_positive_radius_corrected_estimator(
        profile,
        pair.primal,
        pair.adjoint,
    )
    claims = {
        "all_43_authenticated_positive_radius_cells_are_enclosed": (
            len(result.cells) == 43
        ),
        "profile_primal_and_adjoint_partitions_match": (
            result.profile_primal_adjoint_partitions_match
        ),
        "all_fields_and_loads_share_each_centered_cell_coordinate": (
            result.profile_green_trials_form_and_loads_share_coordinate
            and all(cell.shared_centered_coordinate for cell in result.cells)
        ),
        "symmetric_taylor_integration_is_used": (
            result.centered_symmetric_integration_used
        ),
        "every_correlated_cell_is_inside_its_naive_range_enclosure": all(
            cell.correlated_total_integral.is_subset_of(cell.naive_total_integral)
            for cell in result.cells
        ),
        "correlated_width_is_less_than_one_third_of_naive_width": (
            3 * result.correlated_estimator_total.width
            < result.naive_estimator_total.width
        ),
        "positive_radius_signed_total_is_directed_negative": (
            result.correlated_estimator_total.upper < 0
        ),
        "component_sum_and_joint_density_integral_agree": (
            result.component_sum_total == result.correlated_estimator_total
        ),
        "origin_wall_and_global_zero_exclusion_are_not_claimed": (
            not result.origin_included
            and not result.wall_included
            and not result.zero_exclusion_claimed
        ),
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"correlated estimator audit failed: {failed}")
    return {
        "goal": "Centered Signed Positive-Radius Corrected Estimator",
        "status": "pass",
        "result_type": "exact_rational_centered_taylor_signed_outer_estimator",
        "parameters": {
            "positive_radius_domain": {
                "lower": str(result.positive_radius_domain.lower),
                "upper": str(result.positive_radius_domain.upper),
            },
            "positive_radius_cell_count": len(result.cells),
            "profile_subdivisions_per_parent": result.profile_subdivisions_per_parent,
            "degree_limit": 8,
            "rounding_denominator": 10**16,
            "trigonometric_terms": 6,
            "green_terms": 8,
            "pion_mass_squared": str(profile.pion_mass_squared),
        },
        "signed_outer_totals": {
            "J_rigid": _outward_interval(result.rigid_total),
            "B_y_h": _outward_interval(result.deformation_total),
            "R_y_of_z_h": _outward_interval(
                result.primal_residual_correction_total
            ),
            "component_sum": _outward_interval(result.component_sum_total),
            "joint_correlated_integral": _outward_interval(
                result.correlated_estimator_total
            ),
            "naive_range_times_width": _outward_interval(
                result.naive_estimator_total
            ),
        },
        "representation_contract": {
            "bulk_residual": "weak form retaining the derivative residual r1*z'",
            "compatible_wall_completion": "y_f(a)*(gamma_B-k*z_f(a))",
            "incompatible_all_strong_wall_term": "-eta_y*z_f(a)",
        },
        "certified_claims": claims,
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This is an exact-rational signed corrected-estimator enclosure only "
            "on the authenticated positive-radius cells [1/16,4]. Its directed "
            "negative interval is useful input to the global composer, but the "
            "regular-origin contribution, wall term, residual-product remainder, "
            "Weyl transfer, and full-response zero exclusion are not claimed. "
            "Since the bulk keeps r1*z', its compatible wall completion is "
            "y_f(a)*(gamma_B-k*z_f(a)); -eta_y*z_f(a) is reserved for the "
            "all-strong representation."
        ),
    }


def main() -> None:
    record = build_record()
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
