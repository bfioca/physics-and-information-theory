"""Certify the completed Liouville potential on the regular origin family."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.validated_centrifugal_global_form import (
    validate_centrifugal_wall_trace,
)
from qgtoy.validated_centrifugal_origin_liouville import (
    validate_centrifugal_origin_liouville_partition,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_origin import validate_skyrmion_origin_family


ROOT = Path(__file__).resolve().parents[1]
TUBE = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
OUTER = ROOT / "experiments/centrifugal_skyrmion_liouville_outer_tube_certificate.json"
OUTPUT = ROOT / "experiments/centrifugal_skyrmion_liouville_origin_certificate.json"
SOURCES = (
    "qgtoy/validated_centrifugal_origin_liouville.py",
    "qgtoy/validated_centrifugal_global_form.py",
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/validated_interval.py",
    "qgtoy/validated_skyrmion_origin.py",
    "experiments/centrifugal_skyrmion_liouville_origin_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _interval_record(interval: RationalInterval) -> dict[str, str]:
    return {"lower": str(interval.lower), "upper": str(interval.upper)}


def _round_upper(value: Fraction, denominator: int = 10**18) -> Fraction:
    numerator = (
        value.numerator * denominator + value.denominator - 1
    ) // value.denominator
    return Fraction(numerator, denominator)


def build_record() -> dict[str, object]:
    tube = json.loads(TUBE.read_text(encoding="ascii"))
    outer = json.loads(OUTER.read_text(encoding="ascii"))
    recipe = tube["sharp_profile_recipe"]
    if not tube["canonical_mathematical_outputs_reproduced_exactly"]:
        raise ValueError("sharp tube snapshot is not canonical")
    if not outer["summary"]["coercivity_verified"]:
        raise ValueError("outer Newton-tube coefficient certificate is not closed")
    split = Fraction(outer["parameters"]["origin_split_radius"])
    target = Fraction(outer["parameters"]["target_lower_bound"])
    slopes = RationalInterval(
        Fraction(recipe["shooting_slope_interval"]["lower"]),
        Fraction(recipe["shooting_slope_interval"]["upper"]),
    )
    origin = validate_skyrmion_origin_family(
        slopes,
        cutoff=split,
        remainder_radius=Fraction(8),
        pion_mass_squared=Fraction(recipe["pion_mass_squared"]),
        curvature=Fraction(recipe["curvature"]),
        kernel_terms=12,
    )
    validation = validate_centrifugal_origin_liouville_partition(
        origin,
        target_lower_bound=target,
        time_subdivisions=16,
        slope_subdivisions=4,
        kernel_terms=12,
    )
    wall = validate_centrifugal_wall_trace(
        RationalInterval(Fraction(-89, 1000), Fraction(-87, 1000))
    )
    if not validation.coefficient_coercivity_verified:
        raise ValueError("regular-origin Liouville coefficient certificate failed")
    if not wall.wall_trace_positive:
        raise ValueError("wall trace remainder is not positive")
    return {
        "result_type": "centrifugal_skyrmion_liouville_origin_family_audit",
        "input_artifacts": {
            str(TUBE.relative_to(ROOT)): _sha256(TUBE),
            str(OUTER.relative_to(ROOT)): _sha256(OUTER),
        },
        "parameters": {
            "target_lower_bound": str(target),
            "origin_split_radius": str(split),
            "origin_remainder_radius": str(origin.remainder_radius),
            "time_subdivisions": validation.time_subdivisions,
            "slope_subdivisions": validation.slope_subdivisions,
            "kernel_terms": 12,
        },
        "origin_family": {
            "shooting_slopes": _interval_record(origin.shooting_slopes),
            "residual_bound_upper": str(_round_upper(origin.residual_bound)),
            "contraction_bound_upper": str(
                _round_upper(origin.contraction_bound)
            ),
        },
        "summary": {
            "cell_count": len(validation.cells),
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
            "coercivity_verified": validation.coefficient_coercivity_verified,
        },
        "wall_trace": {
            "margin": _interval_record(wall.wall_trace_margin),
            "positive": wall.wall_trace_positive,
        },
        "cells": [
            {
                "time": _interval_record(cell.time),
                "shooting_slopes": _interval_record(cell.shooting_slopes),
                "scaled_first_minor": _interval_record(
                    cell.scaled_first_minor
                ),
                "scaled_second_minor": _interval_record(
                    cell.scaled_second_minor
                ),
                "scaled_determinant": _interval_record(
                    cell.scaled_determinant
                ),
            }
            for cell in validation.cells
        ],
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "next_certificate": (
            "prove closability and density of the common weighted smooth core, "
            "join the origin and outer coefficient bounds, and apply the "
            "representation theorem to obtain the Friedrichs inverse"
        ),
        "claim_boundary": (
            "Together with the source-hashed outer-tube and wall artifacts, "
            "this proves the coefficient inequalities required for a global "
            "1/100 coercivity theorem. Form closability, the operator domain, "
            "the two-sided inverse, and a nonzero forced response remain open."
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
