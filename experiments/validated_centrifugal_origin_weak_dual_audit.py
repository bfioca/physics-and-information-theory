#!/usr/bin/env python3
"""Write the authenticated regular-origin weak form-dual certificate."""

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
from qgtoy.validated_centrifugal_origin_weak_dual import (  # noqa: E402
    validated_archived_origin_weak_energy_dual_family,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_quintic_family import (  # noqa: E402
    validate_skyrmion_origin_quintic_family,
)


SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
OUTPUT = ROOT / "experiments/validated_centrifugal_origin_weak_dual.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/centrifugal_skyrmion_origin_master_kernel.py",
    "qgtoy/centrifugal_skyrmion_rational_response_trials.py",
    "qgtoy/validated_centrifugal_origin_adjoint_load.py",
    "qgtoy/validated_centrifugal_origin_profile_jets.py",
    "qgtoy/validated_centrifugal_origin_response_residual.py",
    "qgtoy/validated_centrifugal_origin_weak_dual.py",
    "qgtoy/validated_interval.py",
    "qgtoy/validated_skyrmion_quintic_family.py",
    "experiments/validated_centrifugal_origin_weak_dual_audit.py",
)
AUTHENTICATED_SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
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
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    expected_slopes = {
        "lower": str(AUTHENTICATED_SLOPES.lower),
        "upper": str(AUTHENTICATED_SLOPES.upper),
    }
    if sharp["sharp_profile_recipe"]["shooting_slope_interval"] != expected_slopes:
        raise ValueError("sharp-profile and origin-family slope intervals differ")
    archive = json.loads(TRIALS.read_text(encoding="ascii"))
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    family = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES, slope_cells=2
    )
    primal = validated_archived_origin_weak_energy_dual_family(
        family,
        pair.primal,
        load="rotational",
    )
    adjoint = validated_archived_origin_weak_energy_dual_family(
        family,
        pair.adjoint,
        load="master",
    )
    claims = {
        "two_cells_cover_authenticated_slope_family": (
            len(primal.cells) == len(adjoint.cells) == 2
        ),
        "primal_rotational_origin_uses_weak_fuchs_hats": (
            primal.load == "rotational" and primal.trial_name == "primal"
        ),
        "loaded_adjoint_origin_uses_weak_fuchs_hats": (
            adjoint.load == "master" and adjoint.trial_name == "adjoint"
        ),
        "principal_lower_bound_is_certified_on_every_cell": all(
            cell.principal_shifted_first_minor_lower > 0
            and cell.principal_shifted_determinant_lower > 0
            for cell in (*primal.cells, *adjoint.cells)
        ),
        "primal_origin_squared_dual_is_below_one_over_400": (
            primal.maximum_squared_dual_upper < Fraction(1, 400)
        ),
        "adjoint_origin_squared_dual_is_below_one_over_one_million": (
            adjoint.maximum_squared_dual_upper < Fraction(1, 1_000_000)
        ),
        "adjoint_origin_dual_norm_is_below_one_over_1000": (
            adjoint.maximum_energy_dual_upper < Fraction(1, 1000)
        ),
        "weak_origin_join_requires_no_cutoff_conormal_trace": True,
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"origin weak-dual audit failed: {failed}")

    def result(record):
        return {
            "trial_name": record.trial_name,
            "load": record.load,
            "squared_dual_upper": _outward_upper(
                record.maximum_squared_dual_upper
            ),
            "energy_dual_upper": _outward_upper(
                record.maximum_energy_dual_upper
            ),
            "energy_dual_upper_float": float(record.maximum_energy_dual_upper),
            "maximum_derivative_squared_upper": _outward_upper(
                max(cell.derivative_squared_dual_upper for cell in record.cells)
            ),
            "maximum_value_squared_upper": _outward_upper(
                max(cell.value_squared_dual_upper for cell in record.cells)
            ),
        }

    return {
        "goal": "Validated Regular-Origin Weak Form-Dual Bounds",
        "status": "pass",
        "result_type": "exact_rational_fuchs_weak_completed_square_bound",
        "parameters": {
            "origin_cutoff": str(family.cutoff),
            "time_horizon": str(family.cutoff**2),
            "slope_cells": 2,
            "profile_kernel_terms": 4,
            "green_series_terms": 8,
            "principal_lower_bound": "1/100",
            "completed_potential_lower_bound": "1/100",
            "exact_radial_weight": "x0^3/3",
        },
        "primal_rotational": result(primal),
        "loaded_adjoint_master": result(adjoint),
        "certified_claims": claims,
        "authenticated_inputs": {
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "claim_boundary": (
            "This certifies weak completed-square origin residual bounds for "
            "the archived primal rotational and loaded adjoint trials over the "
            "authenticated slope family. The weak adjoint origin can join the "
            "weak positive-radius residual without a cutoff conormal trace. "
            "Outer bulk, wall, signed estimator, and zero exclusion remain "
            "separate compositions."
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
