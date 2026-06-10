#!/usr/bin/env python3
"""Write the source-hashed uniform quintic origin-family certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_quintic_family import (  # noqa: E402
    validate_skyrmion_origin_quintic_family,
)


OUTPUT = ROOT / "experiments/validated_skyrmion_quintic_family_certificate.json"
AUTHENTICATED_PROFILE = (
    ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
)
SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/validated_skyrmion_quintic_family_audit.py",
        ROOT / "qgtoy/validated_skyrmion_quintic_family.py",
        ROOT / "qgtoy/validated_skyrmion_origin.py",
        ROOT / "qgtoy/validated_interval.py",
        AUTHENTICATED_PROFILE,
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


def _outward_interval(
    value: RationalInterval,
    *,
    places: int = 15,
) -> dict[str, str]:
    scale = 10**places
    return {
        "representation": f"outward_decimal_enclosure_{places}_places",
        "lower": _decimal_text(_floor_fraction(value.lower * scale), places),
        "upper": _decimal_text(_ceil_fraction(value.upper * scale), places),
    }


def main() -> None:
    starting_hashes = _source_hashes()
    snapshot = json.loads(AUTHENTICATED_PROFILE.read_text(encoding="ascii"))
    snapshot_slopes = snapshot["sharp_profile_recipe"]["shooting_slope_interval"]
    expected_slopes = {
        "lower": _fraction_text(SLOPES.lower),
        "upper": _fraction_text(SLOPES.upper),
    }
    if snapshot_slopes != expected_slopes:
        raise ValueError("authenticated profile slope interval does not match")

    family = validate_skyrmion_origin_quintic_family(SLOPES, slope_cells=16)
    radii_left = family.maximum_residual_bound + (
        family.maximum_contraction_bound * family.remainder_radius
    )
    cells_contiguous = all(
        left.shooting_slopes.upper == right.shooting_slopes.lower
        for left, right in zip(family.cells, family.cells[1:])
    )
    checks = {
        "sixteen_cells": len(family.cells) == 16,
        "cells_cover_authenticated_slope_interval": (
            family.cells[0].shooting_slopes.lower == SLOPES.lower
            and family.cells[-1].shooting_slopes.upper == SLOPES.upper
            and cells_contiguous
        ),
        "contraction_below_3_over_5": (
            family.maximum_contraction_bound < Fraction(3, 5)
        ),
        "radii_left_below_9_over_10": radii_left < Fraction(9, 10),
        "radii_inequality_closes": radii_left <= family.remainder_radius,
        "volterra_denominator_above_20": (
            family.minimum_volterra_denominator > 20
        ),
        "profile_at_cutoff_positive": family.profile_at_cutoff.lower > 0,
        "derivative_at_cutoff_negative": family.derivative_at_cutoff.upper < 0,
    }
    if not all(checks.values()):
        raise ValueError("uniform quintic family audit failed")

    record = {
        "result_type": "validated_uniform_skyrmion_quintic_origin_family",
        "status": "pass",
        "authenticated_slope_interval": expected_slopes,
        "parameters": {
            "cutoff": _fraction_text(family.cutoff),
            "pion_mass_squared": _fraction_text(family.pion_mass_squared),
            "curvature": _fraction_text(family.curvature),
            "remainder_radius": _fraction_text(family.remainder_radius),
            "slope_cells": len(family.cells),
        },
        "maximum_contraction_bound": _outward_scalar(
            family.maximum_contraction_bound
        ),
        "maximum_residual_bound": _outward_scalar(
            family.maximum_residual_bound
        ),
        "radii_left_side": _outward_scalar(radii_left),
        "minimum_volterra_denominator": _outward_scalar(
            family.minimum_volterra_denominator
        ),
        "profile_at_cutoff": _outward_interval(family.profile_at_cutoff),
        "derivative_at_cutoff": _outward_interval(
            family.derivative_at_cutoff
        ),
        "executable_checks": checks,
        "authenticated_profile_dependency": {
            "path": str(AUTHENTICATED_PROFILE.relative_to(ROOT)),
            "sha256": _sha256(AUTHENTICATED_PROFILE),
        },
        "claim_boundary": (
            "Uniform exact-rational quintic profile tube on the finite origin "
            "cell. This does not yet validate the centrifugal field transfer, "
            "the global continuum inverse, or a nonzero tidal response."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("uniform quintic family sources changed during audit")
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
