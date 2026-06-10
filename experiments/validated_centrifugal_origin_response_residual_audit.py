"""Write the source-hashed cancellation-safe origin-residual audit."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

from qgtoy.validated_centrifugal_origin_response_residual import (
    RationalOriginTrialCell,
    ValidatedOriginConormalCell,
    certify_full_domain_energy_dual_residual_upper,
    validated_origin_strong_residual_cell,
)
from qgtoy.validated_centrifugal_response_residual import (
    ValidatedStrongResidualCell,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "experiments/validated_centrifugal_origin_response_residual_certificate.json"
)
SOURCES = (
    "qgtoy/validated_centrifugal_origin_response_residual.py",
    "experiments/validated_centrifugal_origin_response_residual_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _point(value: int | Fraction) -> RationalInterval:
    return RationalInterval.point(value)


def _zero_matrix():
    zero = _point(0)
    return ((zero, zero), (zero, zero))


def _identity_matrix():
    zero = _point(0)
    one = _point(1)
    return ((one, zero), (zero, one))


def build_record() -> dict[str, object]:
    horizon = Fraction(1, 4)
    zero_matrix = _zero_matrix()
    coefficients = ValidatedOriginConormalCell(
        time=RationalInterval(0, horizon),
        coordinate=zero_matrix,
        coordinate_time_derivative=zero_matrix,
        mixed=zero_matrix,
        mixed_time_derivative=zero_matrix,
        principal=_identity_matrix(),
        principal_time_derivative=zero_matrix,
        coordinate_source_hat=(_point(0), _point(0)),
        coordinate_source_hat_time_derivative=(_point(0), _point(0)),
        derivative_source_hat=(_point(0), _point(0)),
        derivative_source_hat_time_derivative=(_point(0), _point(0)),
    )
    trial = RationalOriginTrialCell(
        time_horizon=horizon,
        u=RationalPolynomial((0,)),
        v=RationalPolynomial((1,)),
    )
    origin = validated_origin_strong_residual_cell(coefficients, trial)
    outer = ValidatedStrongResidualCell(
        radius=RationalInterval(origin.radius_cutoff, 1),
        residual=(_point(0), _point(0)),
        l2_squared_upper=Fraction(0),
    )
    full = certify_full_domain_energy_dual_residual_upper(
        origin,
        (outer,),
        wall_radius=Fraction(1),
        interface_distribution_free=True,
        operator_lower_bound=Fraction(1, 100),
        wall_trace_margin_lower_bound=Fraction(1, 4),
    )
    claims = {
        "regular_residual_factor_is_exact": origin.residual_hat
        == (_point(-2), _point(2)),
        "origin_x_cubed_weight_is_exact": origin.l2_squared_upper
        == Fraction(1, 3),
        "origin_and_outer_norms_compose": full.l2_squared_upper
        == Fraction(1, 3),
        "coercivity_lift_is_positive_and_finite": 0
        < full.bulk_energy_dual_upper
        < 6,
        "zero_wall_mismatch_stays_zero": full.wall_energy_dual_upper == 0,
    }
    return {
        "goal": "Cancellation-Safe Origin Response Residual",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_origin_factorization_and_weighted_residual_norm",
        "certified_claims": claims,
        "residual_hat": [
            [str(value.lower), str(value.upper)] for value in origin.residual_hat
        ],
        "radius_cutoff": str(origin.radius_cutoff),
        "origin_l2_squared_upper": str(origin.l2_squared_upper),
        "full_bulk_energy_dual_upper": str(full.bulk_energy_dual_upper),
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies the cancellation-safe origin residual theorem and "
            "its exact composition rule on supplied regular coefficients and "
            "trials. It does not construct authenticated physical origin "
            "profile boxes, matched primal/adjoint trials, or a nonzero "
            "exterior response interval."
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
