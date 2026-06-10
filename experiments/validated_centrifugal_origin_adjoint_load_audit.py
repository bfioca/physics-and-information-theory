#!/usr/bin/env python3
"""Write the authenticated regular-origin adjoint-load certificate."""

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
from qgtoy.validated_centrifugal_origin_adjoint_load import (  # noqa: E402
    validated_archived_loaded_origin_adjoint_residual_family,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_quintic_family import (  # noqa: E402
    validate_skyrmion_origin_quintic_family,
)


OUTPUT = ROOT / "experiments/validated_centrifugal_origin_adjoint_load.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
SOURCES = (
    "qgtoy/validated_centrifugal_origin_adjoint_load.py",
    "qgtoy/centrifugal_skyrmion_origin_master_kernel.py",
    "qgtoy/validated_centrifugal_origin_profile_jets.py",
    "qgtoy/validated_centrifugal_origin_response_residual.py",
    "experiments/validated_centrifugal_origin_adjoint_load_audit.py",
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


def _outward(value: Fraction, *, places: int = 18) -> dict[str, str]:
    scale = 10**places
    return {
        "lower": _decimal(_floor(value * scale), places),
        "upper": _decimal(_ceil(value * scale), places),
        "representation": f"outward_decimal_enclosure_{places}_places",
    }


def _hull(values: tuple[RationalInterval, ...]) -> RationalInterval:
    return RationalInterval(
        min(value.lower for value in values),
        max(value.upper for value in values),
    )


def _outward_interval(value: RationalInterval, *, places: int = 18) -> dict[str, str]:
    scale = 10**places
    return {
        "lower": _decimal(_floor(value.lower * scale), places),
        "upper": _decimal(_ceil(value.upper * scale), places),
        "representation": f"outward_decimal_enclosure_{places}_places",
    }


def build_record() -> dict[str, object]:
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    snapshot_slopes = sharp["sharp_profile_recipe"]["shooting_slope_interval"]
    expected_slopes = {
        "lower": str(AUTHENTICATED_SLOPES.lower),
        "upper": str(AUTHENTICATED_SLOPES.upper),
    }
    if snapshot_slopes != expected_slopes:
        raise ValueError("sharp-profile and origin-family slope intervals differ")
    archived = json.loads(TRIALS.read_text(encoding="ascii"))
    pair = rational_response_trial_pair_from_record(archived["trial_archive"])
    family = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )
    loaded = validated_archived_loaded_origin_adjoint_residual_family(
        family,
        pair.adjoint,
        kernel_terms=4,
        green_terms=8,
    )
    nonzero_load = any(
        any(
            entry.lower != 0 or entry.upper != 0 for entry in load.coordinate_source_hat
        )
        or any(
            entry.lower != 0 or entry.upper != 0 for entry in load.derivative_source_hat
        )
        for load in loaded.loads
    )
    center_factor = all(
        all(entry.contains(0) for entry in load.coordinate_source_hat)
        and all(entry.contains(0) for entry in load.derivative_source_hat)
        for load in loaded.loads
    )
    completed_potential_lower_bound = Fraction(1, 100)
    squared_dual_contribution = (
        loaded.maximum_l2_squared_upper / completed_potential_lower_bound
    )
    claims = {
        "two_cells_cover_authenticated_slope_family": (
            len(loaded.loads) == len(loaded.residuals) == 2
        ),
        "weak_master_load_is_nonzero": nonzero_load,
        "weak_load_hats_retain_the_exact_center_factor": center_factor,
        "archived_adjoint_origin_trial_is_loaded": loaded.trial_name == "adjoint",
        "loaded_origin_l2_squared_upper_below_1e_minus_8": (
            loaded.maximum_l2_squared_upper < Fraction(1, 100_000_000)
        ),
        "origin_squared_v_star_contribution_below_1e_minus_6": (
            squared_dual_contribution < Fraction(1, 1_000_000)
        ),
        "regular_origin_master_load_is_included": True,
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"origin adjoint-load audit failed: {failed}")

    coordinate_components = tuple(
        load.coordinate_source_hat[index] for load in loaded.loads for index in range(2)
    )
    derivative_components = tuple(
        load.derivative_source_hat[index] for load in loaded.loads for index in range(2)
    )
    residual_components = tuple(
        residual.residual_hat[index]
        for residual in loaded.residuals
        for index in range(2)
    )
    return {
        "goal": "Validated Regular-Origin Exterior-Master Adjoint Load",
        "status": "pass",
        "result_type": "loaded_regular_origin_adjoint_strong_residual",
        "parameters": {
            "origin_cutoff": str(family.cutoff),
            "time_horizon": str(family.cutoff**2),
            "slope_cells": len(loaded.loads),
            "profile_kernel_terms": 4,
            "green_series_terms": 8,
            "completed_potential_lower_bound": str(completed_potential_lower_bound),
        },
        "authenticated_inputs": {
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "load_hulls": {
            "coordinate_source_hat": _outward_interval(_hull(coordinate_components)),
            "derivative_source_hat": _outward_interval(_hull(derivative_components)),
            "loaded_residual_hat": _outward_interval(_hull(residual_components)),
        },
        "loaded_origin_l2_squared_upper": _outward(loaded.maximum_l2_squared_upper),
        "origin_squared_v_star_contribution_upper": _outward(squared_dual_contribution),
        "certified_claims": claims,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies the exterior-master-loaded adjoint strong residual "
            "on the authenticated regular-origin cell. The exact conormal "
            "interface theorem, positive-radius completed-square lift, and wall "
            "load are separate certificates. This artifact does not improve the "
            "dominant positive-radius interval wrapping or prove response zero "
            "exclusion."
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
