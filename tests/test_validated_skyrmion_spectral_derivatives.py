from fractions import Fraction

from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_profile import curved_skyrmion_acceleration_box
from qgtoy.validated_skyrmion_spectral_derivatives import (
    _IntervalJet,
    _curved_acceleration_jet,
    _curved_flux_terms_jet,
    _optical_radius_jet,
    _profile_four_jet,
    _sin_cos_jet,
    _third_optical_derivative,
)
from types import SimpleNamespace


def test_interval_jet_product_and_derivative_enclose_exact_polynomial() -> None:
    denominator = 10**12
    x = _IntervalJet(
        (
            RationalInterval.point(Fraction(2)),
            RationalInterval.point(1),
            RationalInterval.point(0),
            RationalInterval.point(0),
        ),
        denominator,
    )
    polynomial = x.power(3) + x.scale(2) + 1

    assert polynomial.coefficients[0].contains(13)
    assert polynomial.derivative().coefficients[0].contains(14)
    assert polynomial.derivative().derivative().coefficients[0].contains(12)
    assert (
        polynomial.derivative().derivative().derivative().coefficients[0]
        .contains(6)
    )


def test_interval_jet_reciprocal_multiplies_to_one() -> None:
    denominator = 10**12
    value = _IntervalJet(
        (
            RationalInterval.point(2),
            RationalInterval.point(1),
            RationalInterval.point(0),
            RationalInterval.point(0),
        ),
        denominator,
    )
    product = value * value.reciprocal()

    assert product.coefficients[0].contains(1)
    for coefficient in product.coefficients[1:]:
        assert coefficient.contains(0)


def test_interval_sine_cosine_jets_enclose_origin_derivatives() -> None:
    denominator = 10**12
    x = _IntervalJet(
        (
            RationalInterval.point(0),
            RationalInterval.point(1),
            RationalInterval.point(0),
            RationalInterval.point(0),
        ),
        denominator,
    )
    sine, cosine = _sin_cos_jet(x, terms=8)

    assert sine.coefficients[0].contains(0)
    assert sine.coefficients[1].contains(1)
    assert sine.coefficients[2].contains(0)
    assert sine.coefficients[3].contains(Fraction(-1, 6))
    assert cosine.coefficients[0].contains(1)
    assert cosine.coefficients[1].contains(0)
    assert cosine.coefficients[2].contains(Fraction(-1, 2))


def test_acceleration_jet_constant_term_encloses_trusted_ode_box() -> None:
    denominator = 10**15
    radius_box = RationalInterval(Fraction(1), Fraction(101, 100))
    profile_box = RationalInterval(Fraction(1, 2), Fraction(51, 100))
    derivative_box = RationalInterval(Fraction(-4, 5), Fraction(-3, 4))
    radius = _IntervalJet(
        (
            radius_box,
            RationalInterval.point(1),
            RationalInterval.point(0),
            RationalInterval.point(0),
        ),
        denominator,
    )
    profile = _IntervalJet(
        (
            profile_box,
            derivative_box,
            RationalInterval.point(0),
            RationalInterval.point(0),
        ),
        denominator,
    )

    acceleration = _curved_acceleration_jet(
        radius,
        profile,
        pion_mass_squared=Fraction(1),
        curvature=Fraction(1, 400),
        trigonometric_terms=24,
    ).coefficients[0]
    trusted = curved_skyrmion_acceleration_box(
        radius_box,
        profile_box,
        derivative_box,
        pion_mass_squared=Fraction(1),
        curvature=Fraction(1, 400),
        trigonometric_terms=24,
    )

    assert acceleration.lower <= trusted.upper
    assert trusted.lower <= acceleration.upper

    for radius_value, profile_value, derivative_value in (
        (Fraction(1), Fraction(1, 2), Fraction(-4, 5)),
        (Fraction(101, 100), Fraction(51, 100), Fraction(-3, 4)),
    ):
        point_radius = _IntervalJet(
            (
                RationalInterval.point(radius_value),
                RationalInterval.point(1),
                RationalInterval.point(0),
                RationalInterval.point(0),
            ),
            denominator,
        )
        point_profile = _IntervalJet(
            (
                RationalInterval.point(profile_value),
                RationalInterval.point(derivative_value),
                RationalInterval.point(0),
                RationalInterval.point(0),
            ),
            denominator,
        )
        point_acceleration = _curved_acceleration_jet(
            point_radius,
            point_profile,
            pion_mass_squared=Fraction(1),
            curvature=Fraction(1, 400),
            trigonometric_terms=24,
        ).coefficients[0]
        trusted_point = curved_skyrmion_acceleration_box(
            RationalInterval.point(radius_value),
            RationalInterval.point(profile_value),
            RationalInterval.point(derivative_value),
            pion_mass_squared=Fraction(1),
            curvature=Fraction(1, 400),
            trigonometric_terms=24,
        )
        assert point_acceleration.lower <= trusted_point.lower
        assert point_acceleration.upper >= trusted_point.upper


def test_profile_recurrence_and_optical_chain_are_exact_on_vacuum() -> None:
    denominator = 10**15
    radius, profile = _profile_four_jet(
        RationalInterval.point(1),
        RationalInterval.point(0),
        RationalInterval.point(0),
        RationalInterval.point(0),
        pion_mass_squared=Fraction(1),
        curvature=Fraction(1, 400),
        trigonometric_terms=24,
        rounding_denominator=denominator,
    )
    for coefficient in profile.coefficients:
        assert coefficient.contains(0)

    endpoint = SimpleNamespace(
        root_curvature=RationalInterval.point(Fraction(1, 20)),
        curvature=Fraction(1, 400),
    )
    radius_three = radius.truncate(3)
    optical = _optical_radius_jet(
        radius_three,
        endpoint=endpoint,
        atanh_terms=80,
    )
    lapse = 1 - radius_three.power(2).scale(Fraction(1, 400))
    velocity = lapse.scale(20)

    assert _third_optical_derivative(optical, velocity).contains(0)


def test_profile_recurrence_annihilates_flux_coefficients_through_order_two() -> None:
    denominator = 10**18
    radius, profile = _profile_four_jet(
        RationalInterval.point(1),
        RationalInterval.point(Fraction(1, 2)),
        RationalInterval.point(Fraction(-4, 5)),
        RationalInterval(Fraction(-10), Fraction(10)),
        pion_mass_squared=Fraction(1),
        curvature=Fraction(1, 400),
        trigonometric_terms=32,
        rounding_denominator=denominator,
    )
    profile_three = profile.truncate(3)
    derivative_three = profile.derivative()
    principal, forcing = _curved_flux_terms_jet(
        radius.truncate(3),
        profile_three,
        derivative_three,
        pion_mass_squared=Fraction(1),
        curvature=Fraction(1, 400),
        trigonometric_terms=32,
    )
    residual = (principal * derivative_three).derivative() - forcing.truncate(2)

    for coefficient in residual.coefficients:
        assert coefficient.contains(0)
