"""Certify the Liouville coercivity minors on the archived exact spline."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.validated_centrifugal_liouville_taylor import (
    validate_centrifugal_liouville_taylor_spline,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import SkyrmionPolynomialCell


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json"
OUTPUT = ROOT / "experiments/centrifugal_skyrmion_liouville_spline_certificate.json"
SOURCES = (
    "qgtoy/validated_centrifugal_liouville_taylor.py",
    "qgtoy/validated_centrifugal_global_form.py",
    "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
    "qgtoy/validated_interval.py",
    "qgtoy/validated_skyrmion_bvp.py",
    "experiments/centrifugal_skyrmion_liouville_spline_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _interval_record(interval: RationalInterval) -> dict[str, str]:
    return {"lower": str(interval.lower), "upper": str(interval.upper)}


def _profile_cells() -> tuple[SkyrmionPolynomialCell, ...]:
    record = json.loads(PROFILE.read_text(encoding="ascii"))
    return tuple(
        SkyrmionPolynomialCell(
            RationalInterval(
                Fraction(item["radius"]["lower"]),
                Fraction(item["radius"]["upper"]),
            ),
            RationalPolynomial(
                tuple(Fraction(value) for value in item["coefficients"])
            ),
        )
        for item in record["profile_cells"]
    )


def build_record() -> dict[str, object]:
    target = Fraction(1, 20)
    validation = validate_centrifugal_liouville_taylor_spline(
        _profile_cells(),
        target_lower_bound=target,
        maximum_refinement_depth=2,
        degree_limit=8,
        rounding_denominator=10**16,
        trigonometric_terms=5,
    )
    if not validation.coercivity_verified:
        raise ValueError("exact-spline Liouville validation did not close")
    if validation.minimum_scaled_first_minor <= 0:
        raise ValueError("scaled first-minor margin is not positive")
    if validation.minimum_scaled_determinant <= 0:
        raise ValueError("scaled determinant margin is not positive")
    return {
        "result_type": "centrifugal_skyrmion_liouville_exact_spline_audit",
        "parameters": {
            "target_lower_bound": str(target),
            "maximum_refinement_depth": 2,
            "degree_limit": 8,
            "rounding_denominator": 10**16,
            "trigonometric_terms": 5,
        },
        "profile_artifact": {
            "path": str(PROFILE.relative_to(ROOT)),
            "sha256": _sha256(PROFILE),
        },
        "summary": {
            "profile_cell_count": validation.profile_cell_count,
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
                "principal_radial": _interval_record(cell.principal_radial),
                "principal_tangential": _interval_record(
                    cell.principal_tangential
                ),
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
            for cell in validation.validation_cells
        ],
        "source_sha256": {
            relative: _sha256(ROOT / relative) for relative in SOURCES
        },
        "next_certificate": (
            "reconstruct the endpoint-corrected Newton-tube center, propagate "
            "its correlated C2 radii into the two division-free minors, and "
            "join this positive-radius result to the authenticated origin family"
        ),
        "claim_boundary": (
            "This is a continuum interval proof for the archived exact "
            "piecewise-polynomial approximate profile on its positive-radius "
            "domain. It does not yet include the nonlinear Newton-tube radius, "
            "the origin interval, or by itself prove coercivity for the exact "
            "Skyrmion solution."
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
