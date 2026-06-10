from fractions import Fraction

import pytest

from qgtoy.paper_r_weyl_observable import (
    annular_weyl_rms_interval,
    horizon_regular_mode_annular_rms,
    horizon_regular_mode_squared_annular_average,
)
from qgtoy.validated_interval import RationalInterval


def test_frozen_annulus_has_exact_rms_factor() -> None:
    squared = horizon_regular_mode_squared_annular_average(
        Fraction(5), Fraction(10), patch_radius=Fraction(20)
    )
    rms = horizon_regular_mode_annular_rms(
        Fraction(5), Fraction(10), patch_radius=Fraction(20)
    )

    assert squared == Fraction(625, 4)
    assert rms == RationalInterval.point(Fraction(25, 2))


def test_amplitude_interval_excluding_zero_gives_positive_weyl_floor() -> None:
    result = annular_weyl_rms_interval(
        RationalInterval(Fraction(-3, 1000), Fraction(-2, 1000))
    )

    assert result == RationalInterval(Fraction(1, 40), Fraction(3, 80))


def test_amplitude_interval_containing_zero_has_zero_weyl_floor() -> None:
    result = annular_weyl_rms_interval(
        RationalInterval(Fraction(-1, 1000), Fraction(2, 1000))
    )

    assert result.lower == 0
    assert result.upper == Fraction(1, 40)


@pytest.mark.parametrize(
    ("inner", "outer", "patch"),
    (
        (0, 10, 20),
        (5, 5, 20),
        (5, 20, 20),
        (10, 5, 20),
    ),
)
def test_invalid_annulus_is_rejected(inner: int, outer: int, patch: int) -> None:
    with pytest.raises(ValueError, match="annulus"):
        horizon_regular_mode_squared_annular_average(
            Fraction(inner), Fraction(outer), patch_radius=Fraction(patch)
        )

