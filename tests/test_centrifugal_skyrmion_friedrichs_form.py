from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_friedrichs_form import (
    certify_centrifugal_friedrichs_form,
)


def test_friedrichs_form_composition_returns_two_sided_inverse_bound() -> None:
    result = certify_centrifugal_friedrichs_form(
        wall_radius=Fraction(4),
        coefficient_split_radius=Fraction(3, 16),
        origin_coercivity_lower_bound=Fraction(1, 100),
        outer_coercivity_lower_bound=Fraction(1, 100),
        origin_principal_lower_bound=Fraction(2, 5),
        outer_principal_lower_bound=Fraction(1, 50),
        wall_trace_margin_lower_bound=Fraction(1, 5),
    )
    assert result.closed is True
    assert result.two_sided_inverse_exists is True
    assert result.coercivity_lower_bound == Fraction(1, 100)
    assert result.inverse_norm_upper_bound == 100
    assert result.compact_resolvent_claimed is False
    assert result.kinetic_mode_gap_claimed is False
    assert result.dual_space_source_response_certified is False


def test_friedrichs_form_rejects_nonpositive_trace_margin() -> None:
    with pytest.raises(ValueError, match="margin"):
        certify_centrifugal_friedrichs_form(
            wall_radius=Fraction(4),
            coefficient_split_radius=Fraction(3, 16),
            origin_coercivity_lower_bound=Fraction(1, 100),
            outer_coercivity_lower_bound=Fraction(1, 100),
            origin_principal_lower_bound=Fraction(2, 5),
            outer_principal_lower_bound=Fraction(1, 50),
            wall_trace_margin_lower_bound=Fraction(0),
        )
