#!/usr/bin/env python3
"""Write the source-hashed physical origin-transfer certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.validated_centrifugal_conormal_remainder import (  # noqa: E402
    validate_centrifugal_conormal_remainder,
)
from qgtoy.validated_centrifugal_physical_origin_transfer import (  # noqa: E402
    validate_centrifugal_physical_origin_transfer,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_quintic_family import (  # noqa: E402
    validate_skyrmion_origin_quintic_family,
)


OUTPUT = (
    ROOT / "experiments/validated_centrifugal_physical_origin_transfer_certificate.json"
)
REMAINDER_CERTIFICATE = (
    ROOT / "experiments/validated_centrifugal_conormal_remainder_certificate.json"
)
SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/validated_centrifugal_physical_origin_transfer_audit.py",
        ROOT / "qgtoy/validated_centrifugal_physical_origin_transfer.py",
        ROOT / "qgtoy/validated_centrifugal_conormal_remainder.py",
        ROOT / "qgtoy/validated_centrifugal_origin_transfer.py",
        ROOT / "qgtoy/validated_skyrmion_quintic_family.py",
        ROOT / "qgtoy/validated_interval.py",
        REMAINDER_CERTIFICATE,
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


def _outward_scalar(value: Fraction, *, places: int = 12) -> dict[str, str]:
    scale = 10**places
    return {
        "representation": f"outward_decimal_enclosure_{places}_places",
        "lower": _decimal_text(_floor_fraction(value * scale), places),
        "upper": _decimal_text(_ceil_fraction(value * scale), places),
    }


def main() -> None:
    starting_hashes = _source_hashes()
    profile = validate_skyrmion_origin_quintic_family(SLOPES, slope_cells=2)
    remainder = validate_centrifugal_conormal_remainder(profile)
    result = validate_centrifugal_physical_origin_transfer(profile, remainder)
    maximum_field_width = max(
        value.width
        for cell in result.cells
        for branch in cell.branches
        for value in branch.field
    )
    maximum_derivative_width = max(
        value.width
        for cell in result.cells
        for branch in cell.branches
        for value in branch.derivative
    )
    formal_centers_contained = all(
        center.is_subset_of(tube)
        for cell in result.cells
        for branch in cell.branches
        for centers, tubes in (
            (branch.formal_field_center, branch.field),
            (branch.formal_derivative_center, branch.derivative),
        )
        for center, tube in zip(centers, tubes, strict=True)
    )
    checks = {
        "two_cells_cover_authenticated_slope_interval": (
            len(result.cells) == 2
            and result.cells[0].shooting_slopes.lower == SLOPES.lower
            and result.cells[-1].shooting_slopes.upper == SLOPES.upper
            and result.cells[0].shooting_slopes.upper
            == result.cells[1].shooting_slopes.lower
        ),
        "all_three_affine_columns_present": all(
            len(cell.branches) == 3 for cell in result.cells
        ),
        "formal_field_and_derivative_centers_contained": (formal_centers_contained),
        "maximum_field_width_below_3_over_50": (maximum_field_width < Fraction(3, 50)),
        "maximum_derivative_width_below_3_over_2": (
            maximum_derivative_width < Fraction(3, 2)
        ),
        "finite_cell_enclosure": result.is_finite_cell_enclosure,
    }
    if not all(checks.values()):
        raise ValueError("physical origin-transfer audit failed")

    record = {
        "result_type": "validated_physical_centrifugal_origin_transfer",
        "status": "pass",
        "authenticated_slope_interval": {
            "lower": _fraction_text(SLOPES.lower),
            "upper": _fraction_text(SLOPES.upper),
        },
        "cutoff": _fraction_text(result.cutoff),
        "branch_order": result.branch_order,
        "maximum_field_interval_width": _outward_scalar(maximum_field_width),
        "maximum_derivative_interval_width": _outward_scalar(maximum_derivative_width),
        "affine_combination_rule": result.affine_combination_rule,
        "executable_checks": checks,
        "validated_conormal_dependency": {
            "path": str(REMAINDER_CERTIFICATE.relative_to(ROOT)),
            "sha256": _sha256(REMAINDER_CERTIFICATE),
        },
        "claim_boundary": (
            "Validated columnwise physical (f,g,f',g') endpoint tubes at "
            "x=1/16. Friedrichs trace-space equivalence, the global continuum "
            "inverse, and a validated nonzero exterior response remain open."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("physical origin-transfer sources changed during audit")
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
