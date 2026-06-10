from fractions import Fraction

import pytest

from qgtoy.validated_centrifugal_origin_response_residual import (
    RationalOriginTrialCell,
    ValidatedOriginConormalCell,
    ValidatedOriginProfileKernelCell,
    certify_full_domain_energy_dual_residual_upper,
    validated_origin_conormal_cell_from_profile,
    validated_origin_strong_residual_cell,
)
from qgtoy.validated_centrifugal_response_residual import (
    ValidatedStrongResidualCell,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial


def _point(value: int | Fraction) -> RationalInterval:
    return RationalInterval.point(value)


def _zero_matrix():
    zero = _point(0)
    return ((zero, zero), (zero, zero))


def _identity_matrix():
    zero = _point(0)
    one = _point(1)
    return ((one, zero), (zero, one))


def test_origin_residual_has_exact_x_cubed_weight() -> None:
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
    result = validated_origin_strong_residual_cell(coefficients, trial)
    assert result.radius_cutoff == Fraction(1, 2)
    assert result.residual_hat == (_point(-2), _point(2))
    assert result.l2_squared_upper == Fraction(1, 3)


def test_regular_profile_kernels_build_center_containing_coefficients() -> None:
    horizon = Fraction(1, 256)
    profile = ValidatedOriginProfileKernelCell(
        time=RationalInterval(0, horizon),
        metric_factor=RationalInterval(Fraction(399, 400), 1),
        metric_factor_time_derivative=_point(Fraction(-1, 400)),
        profile_deficit_radial_derivative=_point(Fraction(3, 2)),
        profile_deficit_radial_derivative_time_derivative=RationalInterval(-2, 1),
        sine_over_radius=_point(Fraction(3, 2)),
        sine_over_radius_time_derivative=RationalInterval(-2, 1),
        cosine_of_profile_deficit=RationalInterval(Fraction(9, 10), 1),
        cosine_of_profile_deficit_time_derivative=RationalInterval(-2, 0),
    )
    result = validated_origin_conormal_cell_from_profile(profile)
    assert result.time == profile.time
    assert result.principal[0][0].lower > 0
    assert result.principal[1][1].lower > 0


def test_origin_trial_exports_exact_physical_endpoint_jet() -> None:
    trial = RationalOriginTrialCell(
        time_horizon=Fraction(1, 256),
        u=RationalPolynomial((2, 1)),
        v=RationalPolynomial((3, -1)),
    )
    fields, derivatives = trial.physical_endpoint_jet()
    assert fields == (Fraction(-509, 4096), Fraction(1, 8))
    assert derivatives == (Fraction(11, 256), Fraction(0))


def test_full_domain_composition_requires_exact_origin_join() -> None:
    origin = validated_origin_strong_residual_cell(
        ValidatedOriginConormalCell(
            time=RationalInterval(0, Fraction(1, 4)),
            coordinate=_zero_matrix(),
            coordinate_time_derivative=_zero_matrix(),
            mixed=_zero_matrix(),
            mixed_time_derivative=_zero_matrix(),
            principal=_identity_matrix(),
            principal_time_derivative=_zero_matrix(),
            coordinate_source_hat=(_point(0), _point(0)),
            coordinate_source_hat_time_derivative=(_point(0), _point(0)),
            derivative_source_hat=(_point(0), _point(0)),
            derivative_source_hat_time_derivative=(_point(0), _point(0)),
        ),
        RationalOriginTrialCell(
            time_horizon=Fraction(1, 4),
            u=RationalPolynomial((0,)),
            v=RationalPolynomial((0,)),
        ),
    )
    outer = ValidatedStrongResidualCell(
        radius=RationalInterval(Fraction(1, 2), 1),
        residual=(_point(0), _point(0)),
        l2_squared_upper=Fraction(4),
    )
    bound = certify_full_domain_energy_dual_residual_upper(
        origin,
        (outer,),
        wall_radius=Fraction(1),
        interface_distribution_free=True,
        operator_lower_bound=Fraction(1, 100),
        wall_trace_margin_lower_bound=Fraction(1, 4),
    )
    assert bound.l2_squared_upper == 4
    assert bound.bulk_energy_dual_upper == 20

    shifted = ValidatedStrongResidualCell(
        radius=RationalInterval(Fraction(3, 5), 1),
        residual=(_point(0), _point(0)),
        l2_squared_upper=Fraction(0),
    )
    with pytest.raises(ValueError, match="do not meet"):
        certify_full_domain_energy_dual_residual_upper(
            origin,
            (shifted,),
            wall_radius=Fraction(1),
            interface_distribution_free=True,
            operator_lower_bound=Fraction(1, 100),
            wall_trace_margin_lower_bound=Fraction(1, 4),
        )
