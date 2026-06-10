#!/usr/bin/env python3
"""Write signed regular-origin corrected-estimator contributions."""

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
from qgtoy.validated_centrifugal_origin_corrected_estimator import (  # noqa: E402
    validated_archived_origin_corrected_estimator_family,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_quintic_family import (  # noqa: E402
    validate_skyrmion_origin_quintic_family,
)


OUTPUT = ROOT / "experiments/validated_centrifugal_origin_corrected_estimator.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
SOURCES = (
    "qgtoy/validated_centrifugal_origin_corrected_estimator.py",
    "qgtoy/validated_centrifugal_origin_adjoint_load.py",
    "qgtoy/validated_centrifugal_origin_profile_jets.py",
    "qgtoy/validated_centrifugal_origin_response_residual.py",
    "experiments/validated_centrifugal_origin_corrected_estimator_audit.py",
)
AUTHENTICATED_SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
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


def _outward_interval(value: RationalInterval, *, places: int = 18) -> dict[str, str]:
    scale = 10**places
    return {
        "lower": _decimal(_floor(value.lower * scale), places),
        "upper": _decimal(_ceil(value.upper * scale), places),
        "representation": f"outward_decimal_enclosure_{places}_places",
    }


def build_record() -> dict[str, object]:
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    expected_slopes = {
        "lower": str(AUTHENTICATED_SLOPES.lower),
        "upper": str(AUTHENTICATED_SLOPES.upper),
    }
    if sharp["sharp_profile_recipe"]["shooting_slope_interval"] != expected_slopes:
        raise ValueError("sharp-profile and origin-family slope intervals differ")
    archived = json.loads(TRIALS.read_text(encoding="ascii"))
    pair = rational_response_trial_pair_from_record(archived["trial_archive"])
    family = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )
    result = validated_archived_origin_corrected_estimator_family(
        family,
        pair.primal,
        pair.adjoint,
        kernel_terms=4,
        green_terms=8,
    )
    slope_cover = (
        result.cells[0].shooting_slopes.lower == AUTHENTICATED_SLOPES.lower
        and result.cells[-1].shooting_slopes.upper == AUTHENTICATED_SLOPES.upper
        and all(
            left.shooting_slopes.upper == right.shooting_slopes.lower
            for left, right in zip(result.cells, result.cells[1:])
        )
    )
    claims = {
        "two_cells_cover_authenticated_slope_family": (
            len(result.cells) == 2 and slope_cover
        ),
        "archived_primal_and_adjoint_origin_trials_are_used": (
            result.primal_trial_name == "primal"
            and result.adjoint_trial_name == "adjoint"
        ),
        "rigid_plus_primal_origin_contribution_below_1e_minus_9": (
            result.master_functional_hull.lower > Fraction(-1, 10**9)
            and result.master_functional_hull.upper < Fraction(1, 10**9)
        ),
        "signed_complete_primal_residual_action_below_1e_minus_6": (
            result.residual_action_hull.lower > Fraction(-1, 1_000_000)
            and result.residual_action_hull.upper < Fraction(1, 1_000_000)
        ),
        "origin_cutoff_trace_is_included": all(
            cell.residual_action.action
            == cell.residual_action.volume_action + cell.residual_action.cutoff_trace
            for cell in result.cells
        ),
        "signed_origin_corrected_contribution_is_directly_enclosed": all(
            cell.corrected_contribution.is_subset_of(result.corrected_contribution_hull)
            for cell in result.cells
        ),
        "origin_interval_alone_does_not_exclude_zero": (
            result.corrected_contribution_hull.contains_zero()
        ),
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"origin corrected-estimator audit failed: {failed}")
    return {
        "goal": "Signed Regular-Origin Corrected-Estimator Contributions",
        "status": "pass",
        "result_type": "validated_origin_corrected_estimator_terms",
        "parameters": {
            "origin_cutoff": str(family.cutoff),
            "time_horizon": str(family.cutoff**2),
            "slope_cells": len(result.cells),
            "profile_kernel_terms": 4,
            "green_series_terms": 8,
            "master_radial_weight_x4": str(
                result.cells[0].master_functional.radial_weight
            ),
            "residual_action_radial_weight_x2": str(
                result.cells[0].residual_action.radial_weight
            ),
        },
        "authenticated_inputs": {
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "signed_origin_hulls": {
            "J_rigid_plus_B_y_h": _outward_interval(result.master_functional_hull),
            "R_y_of_z_h_strong_volume": _outward_interval(
                result.residual_volume_action_hull
            ),
            "R_y_of_z_h_cutoff_trace": _outward_interval(
                result.residual_cutoff_trace_hull
            ),
            "R_y_of_z_h": _outward_interval(result.residual_action_hull),
            "corrected_sum": _outward_interval(result.corrected_contribution_hull),
        },
        "slope_cells": [
            {
                "shooting_slopes": {
                    "lower": str(cell.shooting_slopes.lower),
                    "upper": str(cell.shooting_slopes.upper),
                },
                "J_rigid_plus_B_y_h": _outward_interval(
                    cell.master_functional.contribution
                ),
                "R_y_of_z_h_strong_volume": _outward_interval(
                    cell.residual_action.volume_action
                ),
                "R_y_of_z_h_cutoff_trace": _outward_interval(
                    cell.residual_action.cutoff_trace
                ),
                "R_y_of_z_h": _outward_interval(cell.residual_action.action),
                "corrected_sum": _outward_interval(cell.corrected_contribution),
            }
            for cell in result.cells
        ],
        "certified_claims": claims,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies only the two signed regular-origin contributions "
            "to J_rigid+B(y_h)+R_y(z_h), including the r1(x0) dot z_h(x0) "
            "cutoff trace required when the outer residual remains in weak form. "
            "The interval is intentionally reported "
            "even though it contains zero. Positive-radius and wall estimator "
            "terms, residual-product error, collective normalization, and "
            "response zero exclusion are not claimed."
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
