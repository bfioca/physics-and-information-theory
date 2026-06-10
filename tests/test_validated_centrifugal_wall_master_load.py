from fractions import Fraction
from math import atanh

import pytest

from qgtoy.validated_centrifugal_wall_master_load import (
    DEFAULT_WALL_SLOPE,
    _l2_center_regular_wall_intervals,
    validated_wall_master_load,
)
from qgtoy.validated_interval import RationalInterval


def test_exact_wall_green_inputs_contain_floating_closed_form() -> None:
    x = Fraction(1, 5)
    center, derivative = _l2_center_regular_wall_intervals(x, atanh_terms=48)
    floating_center = 15 * (3 - float(x) ** 2) * atanh(float(x)) / (
        4 * float(x) ** 2
    ) - 45 / (4 * float(x))
    floating_derivative = 15 / 4 * (
        -6 * atanh(float(x)) / float(x) ** 3
        + (3 / float(x) ** 2 - 1) / (1 - float(x) ** 2)
    ) + 45 / (4 * float(x) ** 2)
    assert float(center.midpoint) == pytest.approx(floating_center, abs=2.0e-14)
    assert float(derivative.midpoint) == pytest.approx(
        floating_derivative, abs=2.0e-13
    )
    assert center.lower > 0
    assert derivative.lower > 0


def test_correlated_wall_load_is_positive_and_tight() -> None:
    result = validated_wall_master_load()
    assert result.wall_ratio == Fraction(1, 5)
    assert result.wall_profile_derivative == DEFAULT_WALL_SLOPE
    assert result.wall_displacement_per_radial_field.lower > 10
    assert result.wall_displacement_per_radial_field.upper < 12
    assert result.gamma_b.lower > Fraction(1, 400)
    assert result.gamma_b.upper < Fraction(3, 1000)
    assert result.gamma_b.width < Fraction(1, 5000)
    assert float(result.gamma_b.lower) <= 0.00282575297583 <= float(
        result.gamma_b.upper
    )


def test_wall_load_rejects_nonnegative_slope() -> None:
    with pytest.raises(ValueError, match="strictly negative"):
        validated_wall_master_load(RationalInterval(Fraction(-1), Fraction(0)))
