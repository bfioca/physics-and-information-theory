from fractions import Fraction

import pytest

from qgtoy.validated_centrifugal_global_form import (
    _IntervalJet,
    centrifugal_liouville_cell,
    validate_centrifugal_liouville_coercivity,
    validate_centrifugal_wall_trace,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_bvp import SkyrmionJetBox


def _point(value: int | Fraction) -> RationalInterval:
    return RationalInterval.point(value)


def test_interval_jet_quotient_rule_is_exact_on_points() -> None:
    left = _IntervalJet(_point(3), _point(5))
    right = _IntervalJet(_point(7), _point(11))
    quotient = left / right
    assert quotient.value == _point(Fraction(3, 7))
    assert quotient.derivative == _point(Fraction(2, 49))


def test_exact_wall_trace_margin_is_positive() -> None:
    result = validate_centrifugal_wall_trace(
        RationalInterval(Fraction(-89, 1000), Fraction(-87, 1000))
    )
    assert result.wall_trace_positive is True
    assert result.wall_trace_margin.lower > Fraction(1, 5)
    assert result.wall_robin_multiplier.upper < Fraction(-7, 10)


def test_wall_trace_rejects_slope_interval_containing_zero() -> None:
    with pytest.raises(ValueError, match="exclude zero"):
        validate_centrifugal_wall_trace(
            RationalInterval(Fraction(-1), Fraction(1))
        )


def test_liouville_cell_returns_exact_minor_enclosures() -> None:
    jet = SkyrmionJetBox(
        radius=RationalInterval(Fraction(199, 100), Fraction(201, 100)),
        profile=RationalInterval(Fraction(62, 100), Fraction(65, 100)),
        derivative=RationalInterval(Fraction(-48, 100), Fraction(-44, 100)),
        second_derivative=RationalInterval(Fraction(20, 100), Fraction(25, 100)),
    )
    result = centrifugal_liouville_cell(
        jet,
        source_cell_index=0,
        target_lower_bound=Fraction(1, 100),
    )
    assert result.principal_first_minor.lower > 0
    assert result.principal_determinant.lower > 0
    assert result.radius == jet.radius


def test_validator_requires_exactly_contiguous_cells() -> None:
    first = SkyrmionJetBox(
        radius=RationalInterval(Fraction(1), Fraction(2)),
        profile=_point(1),
        derivative=_point(-1),
        second_derivative=_point(0),
    )
    second = SkyrmionJetBox(
        radius=RationalInterval(Fraction(3), Fraction(4)),
        profile=_point(Fraction(1, 2)),
        derivative=_point(Fraction(-1, 2)),
        second_derivative=_point(0),
    )
    with pytest.raises(ValueError, match="exactly contiguous"):
        validate_centrifugal_liouville_coercivity((first, second))
