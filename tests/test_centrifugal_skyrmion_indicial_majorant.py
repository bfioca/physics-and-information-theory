from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_indicial_majorant import (
    centrifugal_indicial_inverse_majorant_certificate,
)


def test_uniform_post_germ_inverse_bound_is_strict():
    record = centrifugal_indicial_inverse_majorant_certificate()
    assert record["uniform_bound_below_79_over_1000"]
    assert record["uniform_inverse_infinity_norm_upper_bound_decimal"] == pytest.approx(
        0.07832423329415064
    )
    uniform = Fraction(record["uniform_inverse_infinity_norm_upper_bound"])
    assert uniform == Fraction(record["p7_inverse_infinity_norm_upper_bound"])
    assert uniform > Fraction(record["p9_inverse_infinity_norm_upper_bound"])
    assert uniform > Fraction(record["p_ge_11_inverse_infinity_norm_upper_bound"])


@pytest.mark.parametrize(
    "kwargs",
    (
        {"slope_lower": Fraction(0)},
        {"slope_lower": Fraction(2), "slope_upper": Fraction(1)},
        {"slope_lower": 1.0},
    ),
)
def test_majorant_rejects_invalid_slope_boxes(kwargs):
    with pytest.raises((TypeError, ValueError)):
        centrifugal_indicial_inverse_majorant_certificate(**kwargs)
