from fractions import Fraction

import pytest

from qgtoy.validated_centrifugal_origin_response_residual import (
    RationalOriginTrialCell,
    ValidatedOriginConormalCell,
)
from qgtoy.validated_centrifugal_origin_weak_dual import (
    validated_origin_weak_energy_dual_cell,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial


def _synthetic_inputs():
    point = RationalInterval.point
    zero = point(0)
    identity = ((point(1), zero), (zero, point(1)))
    zero_matrix = ((zero, zero), (zero, zero))
    zero_vector = (zero, zero)
    coefficients = ValidatedOriginConormalCell(
        time=RationalInterval(Fraction(0), Fraction(1, 4)),
        coordinate=zero_matrix,
        coordinate_time_derivative=zero_matrix,
        mixed=zero_matrix,
        mixed_time_derivative=zero_matrix,
        principal=identity,
        principal_time_derivative=zero_matrix,
        coordinate_source_hat=(point(2), zero),
        coordinate_source_hat_time_derivative=zero_vector,
        derivative_source_hat=(point(3), zero),
        derivative_source_hat_time_derivative=zero_vector,
    )
    trial = RationalOriginTrialCell(
        time_horizon=Fraction(1, 4),
        u=RationalPolynomial((Fraction(0),)),
        v=RationalPolynomial((Fraction(0),)),
    )
    return coefficients, trial


def test_origin_weak_dual_uses_exact_x_squared_weight() -> None:
    cell = validated_origin_weak_energy_dual_cell(
        *_synthetic_inputs(),
        principal_lower_bound=Fraction(1, 2),
        completed_potential_lower_bound=Fraction(1, 4),
    )
    assert cell.completed_multiplier[0][0] == RationalInterval.point(
        Fraction(1, 2)
    )
    assert cell.completed_value_hat[0] == RationalInterval.point(Fraction(1, 2))
    assert cell.derivative_squared_dual_upper == Fraction(3, 4)
    assert cell.value_squared_dual_upper == Fraction(1, 24)
    assert cell.squared_dual_upper == Fraction(19, 24)


def test_origin_weak_dual_rejects_uncertified_principal_floor() -> None:
    with pytest.raises(ValueError, match="not certified positive"):
        validated_origin_weak_energy_dual_cell(
            *_synthetic_inputs(),
            principal_lower_bound=Fraction(2),
            completed_potential_lower_bound=Fraction(1, 4),
        )

