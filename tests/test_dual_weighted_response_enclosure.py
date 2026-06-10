from fractions import Fraction

import pytest

from qgtoy.dual_weighted_response_enclosure import (
    certify_dual_weighted_response_interval,
    l2_residual_product_upper,
)


def test_dual_weighted_product_certifies_negative_response() -> None:
    result = certify_dual_weighted_response_interval(
        corrected_estimate=Fraction(-3, 1000),
        primal_energy_dual_residual_upper=Fraction(1, 25),
        adjoint_energy_dual_residual_upper=Fraction(1, 25),
    )
    assert result.error_upper == Fraction(1, 625)
    assert result.response_upper == Fraction(-7, 5000)
    assert result.excludes_zero is True
    assert result.sign == -1


def test_dual_weighted_product_keeps_unresolved_interval_honest() -> None:
    result = certify_dual_weighted_response_interval(
        corrected_estimate=Fraction(1, 1000),
        primal_energy_dual_residual_upper=Fraction(1, 20),
        adjoint_energy_dual_residual_upper=Fraction(1, 20),
    )
    assert result.excludes_zero is False
    assert result.sign == 0


def test_l2_residual_product_uses_coercivity_once() -> None:
    assert l2_residual_product_upper(
        primal_l2_residual_upper=Fraction(1, 100),
        adjoint_l2_residual_upper=Fraction(1, 200),
        operator_lower_bound=Fraction(1, 100),
    ) == Fraction(1, 200)


def test_residual_enclosure_rejects_negative_bounds() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        certify_dual_weighted_response_interval(
            corrected_estimate=Fraction(0),
            primal_energy_dual_residual_upper=Fraction(-1),
            adjoint_energy_dual_residual_upper=Fraction(0),
        )
