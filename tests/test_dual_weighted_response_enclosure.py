from fractions import Fraction

import pytest

from qgtoy.dual_weighted_response_enclosure import (
    certify_directed_dual_weighted_response_interval,
    certify_dual_weighted_response_interval,
    l2_residual_product_upper,
)
from qgtoy.validated_interval import RationalInterval


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


def test_directed_estimator_width_is_kept_separate_from_product_error() -> None:
    result = certify_directed_dual_weighted_response_interval(
        corrected_estimate=RationalInterval(
            Fraction(-31, 10_000), Fraction(-29, 10_000)
        ),
        primal_energy_dual_residual_upper=Fraction(1, 20),
        adjoint_energy_dual_residual_upper=Fraction(1, 50),
    )

    assert result.corrected_center == Fraction(-3, 1000)
    assert result.estimator_radius == Fraction(1, 10_000)
    assert result.residual_product_error_upper == Fraction(1, 1000)
    assert result.total_radius == Fraction(11, 10_000)
    assert result.response == RationalInterval(
        Fraction(-41, 10_000), Fraction(-19, 10_000)
    )
    assert result.excludes_zero
    assert result.sign == -1


def test_directed_estimator_rejects_nonexact_or_negative_inputs() -> None:
    with pytest.raises(TypeError, match="RationalInterval"):
        certify_directed_dual_weighted_response_interval(
            corrected_estimate=(-0.0031, -0.0029),  # type: ignore[arg-type]
            primal_energy_dual_residual_upper=Fraction(0),
            adjoint_energy_dual_residual_upper=Fraction(0),
        )
    with pytest.raises(ValueError, match="nonnegative"):
        certify_directed_dual_weighted_response_interval(
            corrected_estimate=RationalInterval.point(0),
            primal_energy_dual_residual_upper=Fraction(-1),
            adjoint_energy_dual_residual_upper=Fraction(0),
        )


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
