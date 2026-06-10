from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_forced_response import (
    certify_centrifugal_weak_response,
)


def test_exact_tangential_source_forces_nonzero_weak_response() -> None:
    result = certify_centrifugal_weak_response(
        shooting_slope_lower=Fraction(3, 2),
        shooting_slope_upper=Fraction(8, 5),
        form_coercivity_lower_bound=Fraction(1, 100),
    )
    assert result.tangential_source_leading_lower == Fraction(2, 5)
    assert result.source_is_nonzero is True
    assert result.weak_solution_is_nonzero is True
    assert result.source_conjugate_susceptibility_positive is True
    assert result.derivative_source_vanishes_at_endpoints is True
    assert result.l2_inverse_bound_applies_directly is True
    assert result.master_or_weyl_response_certified is False


def test_nonzero_response_requires_slope_above_source_threshold() -> None:
    with pytest.raises(ValueError, match="above 1/2"):
        certify_centrifugal_weak_response(
            shooting_slope_lower=Fraction(1, 2),
            shooting_slope_upper=Fraction(3, 2),
            form_coercivity_lower_bound=Fraction(1, 100),
        )
