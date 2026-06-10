"""Write the source-hashed validated response-residual theorem audit."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.validated_centrifugal_response_residual import (
    RationalC1TrialCell,
    ValidatedConormalStrongCell,
    certify_energy_dual_residual_upper,
    validate_rational_c1_trial_cells,
    validated_strong_residual_cell,
    wall_conormal_residual,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "experiments/validated_centrifugal_response_residual_certificate.json"
SOURCES = (
    "qgtoy/validated_centrifugal_response_residual.py",
    "experiments/validated_centrifugal_response_residual_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _point(value: int | Fraction) -> RationalInterval:
    return RationalInterval.point(value)


def build_record() -> dict[str, object]:
    zero = _point(0)
    one = _point(1)
    zero_matrix = ((zero, zero), (zero, zero))
    identity_matrix = ((one, zero), (zero, one))
    radius = RationalInterval(1, 2)
    coefficients = ValidatedConormalStrongCell(
        radius=radius,
        coordinate=zero_matrix,
        mixed=zero_matrix,
        principal=identity_matrix,
        mixed_derivative=zero_matrix,
        principal_derivative=zero_matrix,
        strong_source=(zero, zero),
    )
    trial = RationalC1TrialCell(
        radius=radius,
        radial_field=RationalPolynomial((0, 1, -1)),
        tangential_field=RationalPolynomial((0,)),
    )
    validate_rational_c1_trial_cells((trial,))
    residual = validated_strong_residual_cell(coefficients, trial)
    wall = wall_conormal_residual(
        coefficients=coefficients,
        trial=trial,
        wall_form_coefficient=_point(3),
        wall_load=_point(-4),
    )
    bound = certify_energy_dual_residual_upper(
        (residual,),
        residual_domain=radius,
        interface_distribution_free=True,
        operator_lower_bound=Fraction(1, 100),
        wall_trace_margin_lower_bound=Fraction(1, 4),
        wall_residual=wall,
    )
    claims = {
        "analytic_cell_residual_is_exact": residual.residual
        == (_point(-2), _point(0)),
        "analytic_l2_square_upper_is_exact": residual.l2_squared_upper
        == Fraction(4),
        "bulk_coercivity_lift_is_exact": bound.bulk_energy_dual_upper
        == Fraction(20),
        "wall_mismatch_is_kept_outside_bulk_l2": bound.wall_residual_absolute_upper
        == Fraction(3),
        "energy_dual_bound_composes_bulk_and_wall": bound.energy_dual_upper
        == Fraction(26),
    }
    return {
        "goal": "Validated Positive-Radius Centrifugal Response Residual",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_rational_C1_residual_and_energy_dual_composition",
        "certified_claims": claims,
        "analytic_residual": [
            [str(value.lower), str(value.upper)] for value in residual.residual
        ],
        "l2_squared_upper": str(bound.l2_squared_upper),
        "l2_norm_upper": str(bound.l2_norm_upper),
        "bulk_energy_dual_upper": str(bound.bulk_energy_dual_upper),
        "wall_energy_dual_upper": str(bound.wall_energy_dual_upper),
        "total_energy_dual_upper": str(bound.energy_dual_upper),
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies the residual theorem on supplied positive-radius "
            "cells. It does not provide authenticated physical primal/adjoint "
            "trials, the origin residual, or a nonzero response interval."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
