#!/usr/bin/env python3
"""Audit authenticated origin profile jets and archived trial residuals."""

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
from qgtoy.validated_centrifugal_origin_profile_jets import (  # noqa: E402
    validated_archived_origin_trial_residual_family,
    validated_authenticated_origin_profile_kernel_cells,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_quintic_family import (  # noqa: E402
    validate_skyrmion_origin_quintic_family,
)

OUTPUT = ROOT / "experiments/validated_centrifugal_origin_profile_jets.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
SOURCES = (
    "qgtoy/validated_centrifugal_origin_profile_jets.py",
    "qgtoy/validated_centrifugal_origin_response_residual.py",
    "qgtoy/validated_skyrmion_quintic_family.py",
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "experiments/validated_centrifugal_origin_profile_jets_audit.py",
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


def _outward_interval(
    value: RationalInterval,
    *,
    places: int = 18,
) -> dict[str, str]:
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
    profiles = validated_authenticated_origin_profile_kernel_cells(
        family,
        kernel_terms=4,
    )
    primal = validated_archived_origin_trial_residual_family(
        family,
        pair.primal,
        load="rotational",
        kernel_terms=4,
    )
    adjoint_operator = validated_archived_origin_trial_residual_family(
        family,
        pair.adjoint,
        load="zero",
        kernel_terms=4,
    )
    slope_cover = (
        profiles[0].shooting_slopes.lower == AUTHENTICATED_SLOPES.lower
        and profiles[-1].shooting_slopes.upper == AUTHENTICATED_SLOPES.upper
        and all(
            left.shooting_slopes.upper == right.shooting_slopes.lower
            for left, right in zip(profiles, profiles[1:])
        )
    )
    center_limits = all(
        profile.cubic_coefficient.scale(-3).is_subset_of(
            profile.kernels.profile_deficit_radial_derivative_time_derivative
        )
        and (
            -profile.cubic_coefficient
            - profile.shooting_slopes.power(3).scale(Fraction(1, 6))
        ).is_subset_of(profile.kernels.sine_over_radius_time_derivative)
        and profile.shooting_slopes.power(2).scale(Fraction(-1, 2)).is_subset_of(
            profile.kernels.cosine_of_profile_deficit_time_derivative
        )
        for profile in profiles
    )
    claims = {
        "two_cells_cover_authenticated_slope_family": slope_cover,
        "volterra_division_contains_exact_center_limits": center_limits,
        "archived_primal_origin_trial_is_evaluated": len(primal.residuals) == 2,
        "archived_adjoint_shape_operator_action_is_evaluated": len(
            adjoint_operator.residuals
        )
        == 2,
        "primal_origin_l2_squared_upper_below_1e_minus_3": (
            primal.maximum_l2_squared_upper < Fraction(1, 1_000)
        ),
        "adjoint_shape_operator_l2_squared_upper_below_1e_minus_6": (
            adjoint_operator.maximum_l2_squared_upper < Fraction(1, 1_000_000)
        ),
    }
    if not all(claims.values()):
        raise ValueError("authenticated origin profile-jet audit failed")
    rho_t = RationalInterval(
        min(
            item.kernels.profile_deficit_radial_derivative_time_derivative.lower
            for item in profiles
        ),
        max(
            item.kernels.profile_deficit_radial_derivative_time_derivative.upper
            for item in profiles
        ),
    )
    sine_t = RationalInterval(
        min(item.kernels.sine_over_radius_time_derivative.lower for item in profiles),
        max(item.kernels.sine_over_radius_time_derivative.upper for item in profiles),
    )
    cosine_t = RationalInterval(
        min(
            item.kernels.cosine_of_profile_deficit_time_derivative.lower
            for item in profiles
        ),
        max(
            item.kernels.cosine_of_profile_deficit_time_derivative.upper
            for item in profiles
        ),
    )
    return {
        "goal": "Authenticated Regular-Origin Profile Jets and Trial Residuals",
        "status": "pass",
        "result_type": "validated_origin_kernel_t_jets_and_primal_residual",
        "parameters": {
            "origin_cutoff": str(family.cutoff),
            "time_horizon": str(family.cutoff**2),
            "slope_cells": len(profiles),
            "entire_kernel_terms": 4,
        },
        "authenticated_inputs": {
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "kernel_time_derivative_hulls": {
            "rho_time_derivative": _outward_interval(rho_t),
            "sine_over_radius_time_derivative": _outward_interval(sine_t),
            "cosine_of_deficit_time_derivative": _outward_interval(cosine_t),
        },
        "origin_residual_l2_squared_upper": {
            "primal_rotational_load": _outward(
                primal.maximum_l2_squared_upper
            ),
            "adjoint_shape_zero_load_operator_action": _outward(
                adjoint_operator.maximum_l2_squared_upper
            ),
        },
        "certified_claims": claims,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies the authenticated origin kernel t-jets and the "
            "rotational-load primal origin residual. The adjoint-shaped zero-load "
            "quantity encloses only the homogeneous operator action, not the "
            "adjoint residual: the exterior-amplitude load is still missing. "
            "No conormal interface match, wall residual, full-domain response "
            "interval, or zero exclusion is claimed."
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
