from fractions import Fraction

import pytest

from qgtoy.paper_r_response_certificate import certify_paper_r_response
from qgtoy.validated_interval import RationalInterval


def _certificate(relative_product: Fraction, *, estimator_radius: Fraction = Fraction(0)):
    center = Fraction(-1)
    estimator = RationalInterval(
        center - estimator_radius, center + estimator_radius
    )
    return certify_paper_r_response(
        corrected_estimator=estimator,
        primal_energy_dual_residual_upper=relative_product,
        adjoint_energy_dual_residual_upper=Fraction(1),
        interval_wrapping_is_dominant=True,
    )


@pytest.mark.parametrize(
    ("radius", "decision"),
    (
        (Fraction(3, 4), "GO"),
        (Fraction(4, 5), "TECHNICAL_NOTE"),
        (Fraction(1), "REASSESS"),
        (Fraction(3), "REASSESS"),
        (Fraction(4), "INCONCLUSIVE_STOP"),
        (Fraction(10), "INCONCLUSIVE_STOP"),
        (Fraction(11), "PIVOT"),
    ),
)
def test_predeclared_decision_thresholds(radius: Fraction, decision: str) -> None:
    result = _certificate(radius)
    assert result.relative_radius == radius
    assert result.decision == decision
    assert result.standalone_paper_margin_certified == (decision == "GO")


def test_estimator_width_and_product_both_enter_relative_radius() -> None:
    result = _certificate(Fraction(1, 2), estimator_radius=Fraction(1, 10))

    assert result.dual_weighted.residual_product_error_upper == Fraction(1, 2)
    assert result.dual_weighted.estimator_radius == Fraction(1, 10)
    assert result.relative_radius == Fraction(3, 5)
    assert result.decision == "GO"
    assert result.leading_coefficient_theorem_certified
    assert result.state_transfer.state_sensitive_nonzero_conclusion


def test_physical_ambiguity_forces_pivot_even_for_narrow_interval() -> None:
    result = certify_paper_r_response(
        corrected_estimator=RationalInterval.point(Fraction(-1)),
        primal_energy_dual_residual_upper=Fraction(1, 10),
        adjoint_energy_dual_residual_upper=Fraction(1, 10),
        interval_wrapping_is_dominant=False,
        physical_ambiguity_is_dominant=True,
    )

    assert result.dual_weighted.excludes_zero
    assert result.decision == "PIVOT"
    assert not result.standalone_paper_margin_certified


def test_reassess_requires_demonstrated_wrapping() -> None:
    result = certify_paper_r_response(
        corrected_estimator=RationalInterval.point(Fraction(-1)),
        primal_energy_dual_residual_upper=Fraction(3, 2),
        adjoint_energy_dual_residual_upper=Fraction(1),
        interval_wrapping_is_dominant=False,
    )

    assert result.relative_radius == Fraction(3, 2)
    assert result.decision == "PIVOT"
