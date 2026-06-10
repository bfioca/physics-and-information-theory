#!/usr/bin/env python3
"""Write the source-hashed exact conormal-origin scaffold certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.validated_centrifugal_origin_transfer import (  # noqa: E402
    DEFAULT_STATE_WEIGHTS,
    centrifugal_origin_conormal_certificate,
    formal_affine_endpoint_transfer,
    leading_green_majorant,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402


OUTPUT = ROOT / "experiments/validated_centrifugal_origin_transfer_certificate.json"
PROFILE_CERTIFICATE = (
    ROOT / "experiments/validated_skyrmion_quintic_family_certificate.json"
)
SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/validated_centrifugal_origin_transfer_audit.py",
        ROOT / "qgtoy/validated_centrifugal_origin_transfer.py",
        ROOT / "qgtoy/centrifugal_skyrmion_frobenius.py",
        ROOT / "qgtoy/centrifugal_skyrmion_origin.py",
        ROOT / "qgtoy/validated_interval.py",
        PROFILE_CERTIFICATE,
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def _ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _decimal_text(integer: int, places: int) -> str:
    sign = "-" if integer < 0 else ""
    digits = str(abs(integer)).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


def _outward_scalar(value: Fraction, *, places: int = 15) -> dict[str, str]:
    scale = 10**places
    return {
        "representation": f"outward_decimal_enclosure_{places}_places",
        "lower": _decimal_text(_floor_fraction(value * scale), places),
        "upper": _decimal_text(_ceil_fraction(value * scale), places),
    }


def main() -> None:
    starting_hashes = _source_hashes()
    profile_record = json.loads(PROFILE_CERTIFICATE.read_text(encoding="ascii"))
    expected_slopes = {
        "lower": _fraction_text(SLOPES.lower),
        "upper": _fraction_text(SLOPES.upper),
    }
    if profile_record["authenticated_slope_interval"] != expected_slopes:
        raise ValueError("quintic profile and conormal slope intervals differ")

    theorem = centrifugal_origin_conormal_certificate(SLOPES)
    transfer = formal_affine_endpoint_transfer(SLOPES)
    gamma = leading_green_majorant(SLOPES)
    checks = {
        "four_shifted_spectrum_checks": all(
            theorem["leading_spectrum_checks"].values()
        ),
        "weighted_green_majorant_below_9_over_20": gamma < Fraction(9, 20),
        "two_homogeneous_columns_preserved": (
            len(transfer.homogeneous_field_columns) == 2
            and len(transfer.homogeneous_derivative_columns) == 2
        ),
        "forced_affine_column_preserved": (
            len(transfer.forced_field) == 2 and len(transfer.forced_derivative) == 2
        ),
        "finite_cell_enclosure_not_claimed": (
            not transfer.is_finite_cell_enclosure
            and not theorem["finite_cell_enclosure"]
        ),
    }
    if not all(checks.values()):
        raise ValueError("conormal origin scaffold audit failed")

    record = {
        "result_type": "exact_conormal_fuchs_origin_transfer_scaffold",
        "status": "pass",
        "authenticated_slope_interval": expected_slopes,
        "conormal_variables": theorem["conormal_variables"],
        "fuchs_system": theorem["fuchs_system"],
        "source_blocks": theorem["source_blocks"],
        "leading_spectrum": theorem["leading_spectrum"],
        "projector_construction": theorem["projector_construction"],
        "weighted_green_majorant": _outward_scalar(gamma),
        "green_majorant_state_weights": tuple(
            _fraction_text(value) for value in DEFAULT_STATE_WEIGHTS
        ),
        "green_majorant_slope_cells": 128,
        "degree_two_field_germ": theorem["degree_two_field_germ"],
        "executable_checks": checks,
        "validated_profile_dependency": {
            "path": str(PROFILE_CERTIFICATE.relative_to(ROOT)),
            "sha256": _sha256(PROFILE_CERTIFICATE),
        },
        "claim_boundary": theorem["claim_boundary"],
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("conormal-origin sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "result_type": record["result_type"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
