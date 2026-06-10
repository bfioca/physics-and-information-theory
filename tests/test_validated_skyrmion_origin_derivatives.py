from fractions import Fraction
from types import SimpleNamespace

import pytest

from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_bvp import (
    ValidatedSkyrmionNewtonPhysicalObservables,
)
from qgtoy.validated_skyrmion_origin import validate_skyrmion_origin_family
import qgtoy.validated_skyrmion_origin_derivatives as origin_derivatives
from qgtoy.validated_skyrmion_origin_derivatives import (
    _MultivariateIntervalJet,
    _entire_even_kernel_derivative_interval,
    _lie_derivative,
    _origin_variables,
    _origin_vector_field,
    _origin_weight_jet,
    validate_skyrmion_origin_derivative_norms,
)


def test_multivariate_interval_jet_uses_normalized_mixed_coefficients() -> None:
    denominator = 10**15
    time = _MultivariateIntervalJet.variable(
        RationalInterval.point(2), 0, 2, denominator
    )
    profile = _MultivariateIntervalJet.variable(
        RationalInterval.point(3), 1, 2, denominator
    )
    momentum = _MultivariateIntervalJet.variable(
        RationalInterval.point(4), 2, 2, denominator
    )
    value = time * profile + momentum.power(2)

    assert value.coefficient((0, 0, 0)).contains(22)
    assert value.coefficient((1, 0, 0)).contains(3)
    assert value.coefficient((0, 1, 0)).contains(2)
    assert value.coefficient((0, 0, 1)).contains(8)
    assert value.coefficient((1, 1, 0)).contains(1)
    assert value.coefficient((0, 0, 2)).contains(1)

    product = value * value.reciprocal()
    assert product.coefficient((0, 0, 0)).contains(1)
    for index, coefficient in product.coefficients.items():
        if index != (0, 0, 0):
            assert coefficient.contains(0)


def test_entire_even_kernel_derivatives_at_zero_are_exactly_enclosed() -> None:
    zero = RationalInterval.point(0)

    assert _entire_even_kernel_derivative_interval(
        zero,
        scale_squared=1,
        derivative_order=0,
        terms=12,
    ).contains(1)
    assert _entire_even_kernel_derivative_interval(
        zero,
        scale_squared=1,
        derivative_order=1,
        terms=12,
    ).contains(Fraction(-1, 6))
    assert _entire_even_kernel_derivative_interval(
        zero,
        scale_squared=1,
        derivative_order=2,
        terms=12,
    ).contains(Fraction(1, 60))


def test_origin_lie_vector_field_vanishes_on_regular_fixed_line() -> None:
    variables = _origin_variables(
        RationalInterval.point(0),
        RationalInterval.point(Fraction(3, 2)),
        RationalInterval.point(Fraction(3, 2)),
        order=3,
        rounding_denominator=10**15,
    )
    vector_field, denominator = _origin_vector_field(
        *variables,
        pion_mass_squared=Fraction(1),
        curvature=Fraction(1, 400),
        kernel_terms=16,
    )

    assert denominator.lower > 0
    for component in vector_field:
        assert component.coefficient((0, 0, 0)).contains(0)

    weight = _origin_weight_jet(
        *tuple(value.truncate(4) for value in _origin_variables(
            RationalInterval.point(0),
            RationalInterval.point(Fraction(3, 2)),
            RationalInterval.point(Fraction(3, 2)),
            order=4,
            rounding_denominator=10**15,
        )),
        curvature=Fraction(1, 400),
        kernel_terms=16,
    )
    lie = weight
    for _ in range(3):
        lie = _lie_derivative(lie, vector_field)
        assert lie.coefficient((0, 0, 0)).contains(0)


def _synthetic_physical_observables():
    slopes = RationalInterval(Fraction(1579, 1000), Fraction(1581, 1000))
    origin = validate_skyrmion_origin_family(
        slopes,
        remainder_radius=Fraction(20),
    )
    tube = SimpleNamespace(
        shooting_slope_interval=slopes,
        origin_cutoff=origin.cutoff,
        pion_mass_squared=origin.pion_mass_squared,
        curvature=origin.curvature,
        origin_remainder_radius=origin.remainder_radius,
    )
    physical = object.__new__(ValidatedSkyrmionNewtonPhysicalObservables)
    object.__setattr__(physical, "origin_family", origin)
    object.__setattr__(physical, "newton_tube", tube)
    endpoint = SimpleNamespace(
        certificate_id="origin-test",
        root_curvature=RationalInterval.point(Fraction(1, 20)),
        curvature=Fraction(1, 400),
    )
    return physical, endpoint


def test_origin_derivative_norms_close_without_remainder_derivatives(
    monkeypatch,
) -> None:
    physical, endpoint = _synthetic_physical_observables()
    monkeypatch.setattr(
        origin_derivatives,
        "validate_skyrmion_tail_endpoint_data",
        lambda *args, **kwargs: endpoint,
    )

    result = validate_skyrmion_origin_derivative_norms(
        physical,
        kernel_terms=16,
    )

    assert result.certificate_id == "origin-test"
    assert result.volterra_denominator_enclosure.lower > 0
    assert all(value > 0 for value in result.lie_derivative_over_time_upper_bounds)
    assert all(value > 0 for value in result.w_origin_l1_upper_bounds)
    assert all(value > 0 for value in result.a_origin_l1_upper_bounds)
    assert result.w_origin_l1_upper_bounds[0] < Fraction(1_000_000)
    assert result.a_origin_l1_upper_bounds[0] < Fraction(100_000_000)


def test_origin_derivative_norms_reject_mismatched_cutoff(monkeypatch) -> None:
    physical, endpoint = _synthetic_physical_observables()
    physical.newton_tube.origin_cutoff = Fraction(1, 32)
    monkeypatch.setattr(
        origin_derivatives,
        "validate_skyrmion_tail_endpoint_data",
        lambda *args, **kwargs: endpoint,
    )

    with pytest.raises(ValueError, match="cutoff"):
        validate_skyrmion_origin_derivative_norms(physical, kernel_terms=16)
