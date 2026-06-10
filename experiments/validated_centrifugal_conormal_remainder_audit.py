#!/usr/bin/env python3
"""Write the source-hashed finite-cell conormal remainder certificate."""

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
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_quintic_family import (  # noqa: E402
    validate_skyrmion_origin_quintic_family,
)


OUTPUT = ROOT / "experiments/validated_centrifugal_conormal_remainder_certificate.json"
BLOCK_CERTIFICATE = (
    ROOT / "experiments/centrifugal_skyrmion_conormal_blocks_certificate.json"
)
TRANSFER_CERTIFICATE = (
    ROOT / "experiments/validated_centrifugal_origin_transfer_certificate.json"
)
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
        ROOT / "experiments/validated_centrifugal_conormal_remainder_audit.py",
        ROOT / "qgtoy/validated_centrifugal_conormal_remainder.py",
        ROOT / "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
        ROOT / "qgtoy/validated_centrifugal_origin_transfer.py",
        ROOT / "qgtoy/validated_skyrmion_quintic_family.py",
        ROOT / "qgtoy/validated_interval.py",
        BLOCK_CERTIFICATE,
        TRANSFER_CERTIFICATE,
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
    result = validate_centrifugal_conormal_remainder(profile)
    maximum_endpoint_error = max(
        value
        for branch in result.maximum_branch_endpoint_state_error_bounds
        for value in branch
    )
    cellwise_radii_close = all(
        cell.green_majorant * residual + cell.contraction_bound * radius <= radius
        for cell in result.cells
        for residual, radius in zip(
            cell.branch_residual_bounds,
            cell.branch_remainder_radii,
            strict=True,
        )
    )
    checks = {
        "two_cells_cover_authenticated_slope_interval": (
            len(result.cells) == 2
            and result.cells[0].shooting_slopes.lower == SLOPES.lower
            and result.cells[-1].shooting_slopes.upper == SLOPES.upper
            and result.cells[0].shooting_slopes.upper
            == result.cells[1].shooting_slopes.lower
        ),
        "green_majorant_below_51_over_100": (
            result.maximum_green_majorant < Fraction(51, 100)
        ),
        "coefficient_variation_below_3_over_20": (
            result.maximum_coefficient_variation_bound < Fraction(3, 20)
        ),
        "contraction_below_3_over_40": (
            result.maximum_contraction_bound < Fraction(3, 40)
        ),
        "all_branch_radii_inequalities_close": cellwise_radii_close,
        "maximum_endpoint_state_error_below_1_over_10000": (
            maximum_endpoint_error < Fraction(1, 10_000)
        ),
    }
    if not all(checks.values()):
        raise ValueError("finite-cell conormal remainder audit failed")

    record = {
        "result_type": "validated_finite_cell_conormal_origin_transfer",
        "status": "pass",
        "authenticated_slope_interval": {
            "lower": _fraction_text(SLOPES.lower),
            "upper": _fraction_text(SLOPES.upper),
        },
        "parameters": {
            "cutoff": _fraction_text(result.cutoff),
            "profile_slope_cells": len(result.cells),
            "kernel_terms": 5,
            "green_subcells_per_profile_cell": 4,
            "state_weights": tuple(
                _fraction_text(value) for value in result.state_weights
            ),
        },
        "maximum_green_majorant": _outward_scalar(result.maximum_green_majorant),
        "maximum_coefficient_variation_bound": _outward_scalar(
            result.maximum_coefficient_variation_bound
        ),
        "maximum_contraction_bound": _outward_scalar(result.maximum_contraction_bound),
        "branch_order": result.branch_order,
        "maximum_branch_residual_bounds": tuple(
            _outward_scalar(value) for value in result.maximum_branch_residual_bounds
        ),
        "maximum_branch_remainder_radii": tuple(
            _outward_scalar(value) for value in result.maximum_branch_remainder_radii
        ),
        "maximum_branch_endpoint_state_error_bounds": tuple(
            tuple(_outward_scalar(value) for value in branch)
            for branch in result.maximum_branch_endpoint_state_error_bounds
        ),
        "maximum_endpoint_state_error": _outward_scalar(maximum_endpoint_error),
        "executable_checks": checks,
        "dependencies": {
            "regular_blocks": {
                "path": str(BLOCK_CERTIFICATE.relative_to(ROOT)),
                "sha256": _sha256(BLOCK_CERTIFICATE),
            },
            "conormal_scaffold": {
                "path": str(TRANSFER_CERTIFICATE.relative_to(ROOT)),
                "sha256": _sha256(TRANSFER_CERTIFICATE),
            },
            "quintic_profile_family": {
                "path": str(PROFILE_CERTIFICATE.relative_to(ROOT)),
                "sha256": _sha256(PROFILE_CERTIFICATE),
            },
        },
        "claim_boundary": (
            "Validated affine conormal-state transfer through t=1/256 for "
            "the two homogeneous and one forced columns. Export to a direct "
            "physical (f,g,f',g') endpoint tube, Friedrichs-domain "
            "equivalence, and the global continuum inverse remain open."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("conormal-remainder sources changed during audit")
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
