"""Certify the completed Liouville potential on the AU.1 outer Newton tube."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.validated_centrifugal_liouville_tube import (
    CentrifugalProfileTubeRadii,
    validate_centrifugal_liouville_outer_tube,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import SkyrmionPolynomialCell
from qgtoy.validated_skyrmion_origin import validate_skyrmion_origin_family


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json"
TUBE = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
OUTPUT = ROOT / "experiments/centrifugal_skyrmion_liouville_outer_tube_certificate.json"
SOURCES = (
    "qgtoy/validated_centrifugal_liouville_tube.py",
    "qgtoy/validated_centrifugal_liouville_taylor.py",
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/validated_interval.py",
    "qgtoy/validated_skyrmion_origin.py",
    "experiments/centrifugal_skyrmion_liouville_outer_tube_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _absolute_upper(interval: RationalInterval) -> Fraction:
    return max(abs(interval.lower), abs(interval.upper))


def _interval_record(interval: RationalInterval) -> dict[str, str]:
    return {"lower": str(interval.lower), "upper": str(interval.upper)}


def _round_upper(value: Fraction, denominator: int = 10**18) -> Fraction:
    numerator = (
        value.numerator * denominator + value.denominator - 1
    ) // value.denominator
    return Fraction(numerator, denominator)


def _load_inputs() -> tuple[
    tuple[SkyrmionPolynomialCell, ...],
    tuple[CentrifugalProfileTubeRadii, ...],
    dict[str, object],
]:
    profile_record = json.loads(PROFILE.read_text(encoding="ascii"))
    tube_record = json.loads(TUBE.read_text(encoding="ascii"))
    if not tube_record["canonical_mathematical_outputs_reproduced_exactly"]:
        raise ValueError("sharp tube snapshot did not reproduce the canonical outputs")
    recipe = tube_record["sharp_profile_recipe"]
    profile_cells = tuple(
        SkyrmionPolynomialCell(
            RationalInterval(
                Fraction(item["radius"]["lower"]),
                Fraction(item["radius"]["upper"]),
            ),
            RationalPolynomial(
                tuple(Fraction(value) for value in item["coefficients"])
            ),
        )
        for item in profile_record["profile_cells"]
    )
    left_correction = RationalInterval(
        Fraction(recipe["left_value_correction"]["lower"]),
        Fraction(recipe["left_value_correction"]["upper"]),
    )
    correction_radius = _absolute_upper(left_correction) + abs(
        Fraction(recipe["right_value_correction"])
    )
    domain_length = Fraction(recipe["wall_radius"]) - Fraction(
        recipe["origin_cutoff"]
    )
    radii: list[CentrifugalProfileTubeRadii] = []
    for index, (profile_cell, item) in enumerate(
        zip(profile_cells, recipe["cells"], strict=True)
    ):
        item_radius = RationalInterval(
            Fraction(item["radius"]["lower"]),
            Fraction(item["radius"]["upper"]),
        )
        if item["source_cell_index"] != index or item_radius != profile_cell.radius:
            raise ValueError("profile and sharp-tube cells are not exactly aligned")
        # The raw spline is used as center. The complete affine endpoint
        # correction is conservatively absorbed into these uniform radii.
        radii.append(
            CentrifugalProfileTubeRadii(
                Fraction(item["profile_error_radius"]) + correction_radius,
                Fraction(item["derivative_error_radius"])
                + correction_radius / domain_length,
                Fraction(item["second_derivative_error_radius"]),
            )
        )
    return profile_cells, tuple(radii), recipe


def build_record() -> dict[str, object]:
    profile_cells, tube_radii, recipe = _load_inputs()
    origin_cutoff = Fraction(3, 16)
    slopes = RationalInterval(
        Fraction(recipe["shooting_slope_interval"]["lower"]),
        Fraction(recipe["shooting_slope_interval"]["upper"]),
    )
    origin = validate_skyrmion_origin_family(
        slopes,
        cutoff=origin_cutoff,
        remainder_radius=Fraction(recipe["origin_remainder_radius"]),
        pion_mass_squared=Fraction(recipe["pion_mass_squared"]),
        curvature=Fraction(recipe["curvature"]),
        kernel_terms=12,
    )
    first_source_cell_index = next(
        index
        for index, cell in enumerate(profile_cells)
        if cell.radius.lower == origin_cutoff
    )
    target = Fraction(1, 100)
    validation = validate_centrifugal_liouville_outer_tube(
        profile_cells,
        tube_radii,
        first_source_cell_index=first_source_cell_index,
        target_lower_bound=target,
        maximum_refinement_depth=4,
        degree_limit=8,
        rounding_denominator=10**16,
        trigonometric_terms=5,
    )
    return {
        "result_type": "centrifugal_skyrmion_liouville_outer_newton_tube_audit",
        "input_artifacts": {
            str(PROFILE.relative_to(ROOT)): _sha256(PROFILE),
            str(TUBE.relative_to(ROOT)): _sha256(TUBE),
        },
        "parameters": {
            "origin_split_radius": str(origin_cutoff),
            "first_source_cell_index": first_source_cell_index,
            "target_lower_bound": str(target),
            "maximum_refinement_depth": 4,
            "degree_limit": 8,
            "rounding_denominator": 10**16,
            "trigonometric_terms": 5,
        },
        "extended_origin_family": {
            "shooting_slopes": _interval_record(origin.shooting_slopes),
            "cutoff": str(origin.cutoff),
            "remainder_radius": str(origin.remainder_radius),
            "residual_bound_upper": str(_round_upper(origin.residual_bound)),
            "contraction_bound_upper": str(
                _round_upper(origin.contraction_bound)
            ),
        },
        "summary": {
            "source_cell_count": validation.source_cell_count,
            "validation_cell_count": len(validation.validation_cells),
            "maximum_refinement_depth_used": (
                validation.maximum_refinement_depth_used
            ),
            "minimum_principal_radial": str(
                validation.minimum_principal_radial
            ),
            "minimum_principal_tangential": str(
                validation.minimum_principal_tangential
            ),
            "minimum_scaled_first_minor": str(
                validation.minimum_scaled_first_minor
            ),
            "minimum_scaled_second_minor": str(
                validation.minimum_scaled_second_minor
            ),
            "minimum_scaled_determinant": str(
                validation.minimum_scaled_determinant
            ),
            "coercivity_verified": validation.coercivity_verified,
        },
        "validation_cells": [
            {
                "source_cell_index": cell.source_cell_index,
                "radius": _interval_record(cell.radius),
                "scaled_first_minor": _interval_record(cell.scaled_first_minor),
                "scaled_second_minor": _interval_record(cell.scaled_second_minor),
                "scaled_determinant": _interval_record(cell.scaled_determinant),
            }
            for cell in validation.validation_cells
        ],
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "next_certificate": (
            "range the completed Liouville potential directly on the extended "
            "regular origin family over [0,3/16], then join the two form cores"
        ),
        "claim_boundary": (
            "The authenticated nonlinear Newton tube satisfies W_K >= 1/100 I "
            "on [3/16,4], and the regular nonlinear origin family exists on "
            "[0,3/16]. Positivity of W_K on that origin family, the global "
            "closed-form theorem, and a two-sided inverse remain open."
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
