"""Smooth compact optical-worldtube profile and profile-specific ULE moments.

Choose a radial ``C_c^infinity`` seed on optical ``H^3_R`` supported in half
the requested worldtube radius and convolve it with its reflection.  The field
profile is then supported in the requested radius and has nonnegative spherical
multiplier ``F(p)^2``.  The regulated gradient spectrum is
``j_0(w) F(Rw)^4``.

This module differentiates the spherical transform analytically and evaluates
the frequency Sobolev norms entering rigorous bounds on the Nathan--Rudner jump
correlator moments. Tight quadrature values remain step/window converged rather
than interval certified. A separate repeated-integration-by-parts argument
gives conservative closed-form upper enclosures for the exact integral profile
and its infinite-frequency tails; it never extrapolates the finite Simpson sum.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import (
    cos,
    exp,
    expm1,
    inf,
    isfinite,
    isqrt,
    log,
    nextafter,
    pi,
    sin,
    sinh,
    sqrt,
)

from .static_patch_overlapping_ule import (
    smeared_gradient_zero_frequency_spectrum,
)
from .static_patch_worldtube_ule import (
    logarithmic_heat_ule_coupling_cap,
    optimal_sobolev_jump_correlator_moment_bounds,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def smooth_compact_seed_shape(scaled_radius: float) -> float:
    """Return the standard bump ``exp[1-1/(1-x^2)]`` on ``0<=x<1``."""
    _validate_nonnegative("scaled_radius", scaled_radius)
    if scaled_radius >= 1.0:
        return 0.0
    squared = scaled_radius * scaled_radius
    return exp(1.0 - 1.0 / (1.0 - squared))


def _sinc(value: float) -> float:
    absolute = abs(value)
    if absolute < 1.0e-4:
        squared = value * value
        return 1.0 - squared / 6.0 + squared**2 / 120.0 - squared**3 / 5_040.0
    return sin(value) / value


def _sinc_first(value: float) -> float:
    absolute = abs(value)
    if absolute < 1.0e-4:
        squared = value * value
        return value * (
            -1.0 / 3.0
            + squared / 30.0
            - squared**2 / 840.0
            + squared**3 / 45_360.0
        )
    return (value * cos(value) - sin(value)) / value**2


def _sinc_second(value: float) -> float:
    absolute = abs(value)
    if absolute < 1.0e-3:
        squared = value * value
        return (
            -1.0 / 3.0
            + squared / 10.0
            - squared**2 / 168.0
            + squared**3 / 6_480.0
        )
    return (
        -sin(value) / value
        - 2.0 * cos(value) / value**2
        + 2.0 * sin(value) / value**3
    )


@lru_cache(maxsize=32)
def _smooth_seed_quadrature_data(
    support_radius_ratio: float,
    radial_steps: int,
) -> tuple[tuple[float, float], ...]:
    """Return normalized Simpson nodes for the seed spherical transform."""
    _validate_positive("support_radius_ratio", support_radius_ratio)
    _validate_positive_integer("radial_steps", radial_steps)
    if radial_steps % 2:
        raise ValueError("radial_steps must be even")
    seed_radius = 0.5 * support_radius_ratio
    spacing = seed_radius / radial_steps
    raw: list[tuple[float, float]] = []
    normalization = 0.0
    for index in range(radial_steps + 1):
        y_value = index * spacing
        if index == 0 or index == radial_steps:
            simpson_weight = 1.0
        elif index % 2:
            simpson_weight = 4.0
        else:
            simpson_weight = 2.0
        shape = smooth_compact_seed_shape(y_value / seed_radius)
        radial_weight = shape * y_value * sinh(y_value)
        weighted = simpson_weight * radial_weight
        raw.append((y_value, weighted))
        normalization += weighted
    normalization *= spacing / 3.0
    if normalization <= 0.0:
        raise ValueError("smooth seed normalization must be positive")
    scale = spacing / (3.0 * normalization)
    return tuple((y_value, scale * weighted) for y_value, weighted in raw)


def smooth_seed_spherical_transform_derivatives(
    spectral_parameter: float,
    *,
    support_radius_ratio: float = 0.2,
    radial_steps: int = 400,
) -> tuple[float, float, float]:
    """Approximate ``F(p)``, ``F'(p)``, and ``F''(p)`` on a finite window.

    The seed is supported in dimensionless radius ``A/2``. Its normalization is
    chosen so ``F(0)=1``.  Convolution with its reflection has support ``A`` and
    field-amplitude multiplier ``F(p)^2``.  The returned finite Simpson sum is a
    quadrature approximation to the exact integral; it must not be extrapolated
    to infinite frequency because a fixed sinc sum has an artificial ``p^-1``
    tail.  Use :func:`smooth_seed_transform_tail_envelope` for the exact tail.
    """
    if not isfinite(spectral_parameter):
        raise ValueError("spectral_parameter must be finite")
    data = _smooth_seed_quadrature_data(
        support_radius_ratio,
        radial_steps,
    )
    value = 0.0
    first = 0.0
    second = 0.0
    for y_value, weight in data:
        argument = spectral_parameter * y_value
        value += weight * _sinc(argument)
        first += weight * y_value * _sinc_first(argument)
        second += weight * y_value**2 * _sinc_second(argument)
    return value, first, second


def smooth_worldtube_amplitude_multiplier(
    frequency: float,
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
    radial_steps: int = 400,
) -> float:
    """Return the convolution-square field-amplitude multiplier ``F(Rw)^2``."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    transform, _, _ = smooth_seed_spherical_transform_derivatives(
        radius * frequency,
        support_radius_ratio=support_radius / radius,
        radial_steps=radial_steps,
    )
    return transform * transform


def _positive_bare_sqrt_spectrum_derivatives(
    frequency: float,
    *,
    radius: float,
) -> tuple[float, float, float]:
    """Return ``sqrt(j_0)`` and two derivatives for positive frequency."""
    dimensionless = radius * frequency
    if dimensionless < 1.0e-3:
        two_pi = 2.0 * pi
        thermal_coefficients = (
            1.0 / two_pi,
            0.5,
            two_pi / 12.0,
            0.0,
            -(two_pi**3) / 720.0,
            0.0,
            two_pi**5 / 30_240.0,
        )
        coefficients = (
            thermal_coefficients[0],
            thermal_coefficients[1],
            thermal_coefficients[2] + thermal_coefficients[0],
            thermal_coefficients[3] + thermal_coefficients[1],
            thermal_coefficients[4] + thermal_coefficients[2],
            thermal_coefficients[5] + thermal_coefficients[3],
            thermal_coefficients[6] + thermal_coefficients[4],
        )
        squared_root = sum(
            coefficient * dimensionless**order
            for order, coefficient in enumerate(coefficients)
        )
        squared_first = sum(
            order * coefficient * dimensionless ** (order - 1)
            for order, coefficient in enumerate(coefficients)
            if order >= 1
        )
        squared_second = sum(
            order
            * (order - 1)
            * coefficient
            * dimensionless ** (order - 2)
            for order, coefficient in enumerate(coefficients)
            if order >= 2
        )
        dimensionless_root = sqrt(squared_root)
        dimensionless_first = squared_first / (2.0 * dimensionless_root)
        dimensionless_second = (
            squared_second / (2.0 * dimensionless_root)
            - squared_first**2 / (4.0 * dimensionless_root**3)
        )
        scale = 1.0 / (sqrt(12.0) * pi)
        return (
            scale * dimensionless_root / radius**1.5,
            scale * dimensionless_first / radius**0.5,
            scale * dimensionless_second * radius**0.5,
        )
    beta = 2.0 * pi * radius
    thermal_denominator = -expm1(-beta * frequency)
    spectrum = (
        frequency
        * (1.0 + (radius * frequency) ** 2)
        / (12.0 * pi**2 * radius**2 * thermal_denominator)
    )
    root = sqrt(spectrum)
    scaled = beta * frequency
    if scaled > 50.0:
        bose = 0.0
    else:
        bose = 1.0 / expm1(scaled)
    log_first = (
        1.0 / frequency
        + 2.0 * radius**2 * frequency
        / (1.0 + radius**2 * frequency**2)
        - beta * bose
    )
    log_second = (
        -1.0 / frequency**2
        + 2.0
        * radius**2
        * (1.0 - radius**2 * frequency**2)
        / (1.0 + radius**2 * frequency**2) ** 2
        + beta**2 * bose * (1.0 + bose)
    )
    first = 0.5 * log_first * root
    second = (0.5 * log_second + 0.25 * log_first**2) * root
    return root, first, second


def bare_sqrt_spectrum_derivatives(
    frequency: float,
    *,
    radius: float = 1.0,
) -> tuple[float, float, float]:
    """Return ``sqrt(j_0(w))`` and its first two derivatives on the real line."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    if frequency >= 0.0:
        return _positive_bare_sqrt_spectrum_derivatives(
            frequency,
            radius=radius,
        )
    positive_frequency = -frequency
    root, first, second = _positive_bare_sqrt_spectrum_derivatives(
        positive_frequency,
        radius=radius,
    )
    thermal = exp(-pi * radius * positive_frequency)
    rate = pi * radius
    return (
        thermal * root,
        thermal * (rate * root - first),
        thermal * (second - 2.0 * rate * first + rate**2 * root),
    )


def smooth_worldtube_sqrt_spectrum_derivatives(
    frequency: float,
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
    radial_steps: int = 400,
) -> tuple[float, float, float]:
    """Return the regulated principal square root and its first two derivatives."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    transform, transform_first, transform_second = (
        smooth_seed_spherical_transform_derivatives(
            radius * frequency,
            support_radius_ratio=support_radius / radius,
            radial_steps=radial_steps,
        )
    )
    transform_first *= radius
    transform_second *= radius**2
    amplitude = transform**2
    amplitude_first = 2.0 * transform * transform_first
    amplitude_second = 2.0 * (
        transform_first**2 + transform * transform_second
    )
    root, root_first, root_second = bare_sqrt_spectrum_derivatives(
        frequency,
        radius=radius,
    )
    return (
        root * amplitude,
        root_first * amplitude + root * amplitude_first,
        root_second * amplitude
        + 2.0 * root_first * amplitude_first
        + root * amplitude_second,
    )


def smooth_worldtube_gradient_spectrum(
    frequency: float,
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
    radial_steps: int = 400,
) -> float:
    """Return ``j_0(w)F(Rw)^4`` for the named smooth compact profile."""
    root = smooth_worldtube_sqrt_spectrum_derivatives(
        frequency,
        radius=radius,
        support_radius=support_radius,
        radial_steps=radial_steps,
    )[0]
    return root * root


def smooth_worldtube_sobolev_norms(
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
    frequency_window: float = 160.0,
    frequency_steps: int = 3_200,
    radial_steps: int = 400,
) -> tuple[float, float, float]:
    """Return truncated ``L2`` norms of ``q``, ``q'``, and ``q''`` by Simpson."""
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    _validate_positive("frequency_window", frequency_window)
    _validate_positive_integer("frequency_steps", frequency_steps)
    _validate_positive_integer("radial_steps", radial_steps)
    if frequency_steps % 2:
        raise ValueError("frequency_steps must be even")
    if radial_steps % 2:
        raise ValueError("radial_steps must be even")
    spacing = frequency_window / frequency_steps
    totals = [0.0, 0.0, 0.0]
    for index in range(frequency_steps + 1):
        frequency = index * spacing
        if index == 0 or index == frequency_steps:
            weight = 1.0
        elif index % 2:
            weight = 4.0
        else:
            weight = 2.0
        positive = smooth_worldtube_sqrt_spectrum_derivatives(
            frequency,
            radius=radius,
            support_radius=support_radius,
            radial_steps=radial_steps,
        )
        negative = smooth_worldtube_sqrt_spectrum_derivatives(
            -frequency,
            radius=radius,
            support_radius=support_radius,
            radial_steps=radial_steps,
        )
        for order in range(3):
            totals[order] += weight * (
                positive[order] ** 2 + negative[order] ** 2
            )
    return tuple(sqrt(spacing * total / 3.0) for total in totals)


def smooth_worldtube_moment_record(
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
    frequency_window: float = 160.0,
    frequency_steps: int = 3_200,
    radial_steps: int = 400,
) -> dict[str, float]:
    """Return profile-specific Sobolev norms and jump-moment upper estimates."""
    norms = smooth_worldtube_sobolev_norms(
        radius=radius,
        support_radius=support_radius,
        frequency_window=frequency_window,
        frequency_steps=frequency_steps,
        radial_steps=radial_steps,
    )
    jump_l1, jump_first = optimal_sobolev_jump_correlator_moment_bounds(
        *norms,
    )
    return {
        "sqrt_spectrum_l2": norms[0],
        "sqrt_spectrum_first_derivative_l2": norms[1],
        "sqrt_spectrum_second_derivative_l2": norms[2],
        "jump_l1_sobolev_estimate": jump_l1,
        "jump_first_moment_sobolev_estimate": jump_first,
        "frequency_window": frequency_window,
        "frequency_steps": float(frequency_steps),
        "radial_steps": float(radial_steps),
    }


def _fraction_sqrt_upper(
    value: Fraction,
    *,
    decimal_places: int = 12,
) -> Fraction:
    """Return a decimal rational that is provably at least ``sqrt(value)``."""
    if value < 0:
        raise ValueError("value must be nonnegative")
    scale = 10**decimal_places
    scaled_numerator = value.numerator * scale**2
    root = isqrt(scaled_numerator // value.denominator)
    if root * root * value.denominator < scaled_numerator:
        root += 1
    return Fraction(root, scale)


def _fraction_upper_float(value: Fraction) -> float:
    """Render an exact rational endpoint as a float without rounding downward."""
    rendered = float(value)
    if Fraction.from_float(rendered) < value:
        rendered = nextafter(rendered, inf)
    return rendered


def _fraction_lower_float(value: Fraction) -> float:
    """Render an exact rational lower endpoint without rounding upward."""
    rendered = float(value)
    if Fraction.from_float(rendered) > value:
        rendered = nextafter(rendered, -inf)
    return rendered


def _smooth_seed_tail_envelope_fractions(
    support_radius_ratio: Fraction,
) -> dict[str, Fraction]:
    seed_radius = support_radius_ratio / 2
    bump_first_derivative_upper = Fraction(80, 27)
    bump_second_derivative_upper = (
        4 * Fraction(256_000, 19_683)
        + 2 * Fraction(40, 27)
        + 8 * Fraction(100, 27)
    )
    sinh_upper = Fraction(8, 7) * seed_radius
    cosh_upper = Fraction(8, 7)
    u_upper = sinh_upper
    u_first_upper = (
        bump_first_derivative_upper * sinh_upper / seed_radius
        + cosh_upper
    )
    u_second_upper = (
        bump_second_derivative_upper * sinh_upper / seed_radius**2
        + 2
        * bump_first_derivative_upper
        * cosh_upper
        / seed_radius
        + sinh_upper
    )
    normalization_lower = seed_radius**3 / 36
    numerator_envelopes = (
        u_second_upper,
        2 * u_first_upper + seed_radius * u_second_upper,
        2 * u_upper
        + 4 * seed_radius * u_first_upper
        + seed_radius**2 * u_second_upper,
    )
    h_envelopes = tuple(
        seed_radius * upper / normalization_lower
        for upper in numerator_envelopes
    )
    return {
        "seed_radius_ratio": seed_radius,
        "normalization_lower": normalization_lower,
        "bump_first_upper": bump_first_derivative_upper,
        "bump_second_upper": bump_second_derivative_upper,
        "h0": h_envelopes[0],
        "h1": h_envelopes[1],
        "h2": h_envelopes[2],
        "f0": h_envelopes[0],
        "f1": h_envelopes[1] + h_envelopes[0],
        "f2": h_envelopes[2] + 2 * h_envelopes[1] + 2 * h_envelopes[0],
    }


def smooth_seed_transform_tail_envelope(
    *,
    support_radius_ratio: float = 0.2,
) -> dict[str, float]:
    """Return analytic ``p^-3`` envelopes for the exact seed transform.

    This function bounds the exact radial integral, not the finite Simpson sum
    used by :func:`smooth_seed_spherical_transform_derivatives`.  Write
    ``s=A/2`` and ``u(y)=b_A(y)sinh(y)``.  Twice integrating each half-interval
    transform of ``y^j u(y)`` by parts gives ``|H^(j)(p)|<=C_j/p^2`` for
    ``j=0,1,2``.  The required endpoint data vanish directly; no common smooth
    odd-extension claim is used.  The returned constants then bound ``F``,
    ``F'``, and ``F''`` by ``p^-3``.

    All elementary estimates are deliberately rational and conservative.  They
    use ``A<=1/4``, hence ``s<=1/8`` and ``exp(s)<8/7``; the bump derivative
    bounds follow by maximizing ``t^-m exp(1-1/t)`` on ``0<t<=1``.
    """
    _validate_positive("support_radius_ratio", support_radius_ratio)
    if support_radius_ratio < 0.1 or support_radius_ratio > 0.25:
        raise ValueError(
            "analytic envelope requires 0.1 <= support_radius_ratio <= 0.25"
        )
    ratio_fraction = Fraction.from_float(support_radius_ratio)
    exact = _smooth_seed_tail_envelope_fractions(ratio_fraction)

    def upper(name: str) -> float:
        return _fraction_upper_float(exact[name])

    return {
        "support_radius_ratio": support_radius_ratio,
        "seed_radius_ratio": upper("seed_radius_ratio"),
        "seed_normalization_lower_bound": _fraction_lower_float(
            exact["normalization_lower"]
        ),
        "seed_normalization_lower_bound_exact": str(exact["normalization_lower"]),
        "bump_first_derivative_upper_bound": upper("bump_first_upper"),
        "bump_second_derivative_upper_bound": upper("bump_second_upper"),
        "h_l2_fourier_numerator_envelope": upper("h0"),
        "h_first_fourier_numerator_envelope": upper("h1"),
        "h_second_fourier_numerator_envelope": upper("h2"),
        "transform_p_cubed_envelope": upper("f0"),
        "transform_first_p_cubed_envelope": upper("f1"),
        "transform_second_p_cubed_envelope": upper("f2"),
        "transform_p_cubed_envelope_exact": str(exact["f0"]),
        "transform_first_p_cubed_envelope_exact": str(exact["f1"]),
        "transform_second_p_cubed_envelope_exact": str(exact["f2"]),
    }


def smooth_worldtube_analytic_sobolev_upper_bounds(
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
) -> dict[str, object]:
    """Return rigorous closed-form Sobolev upper bounds for the exact profile.

    The proof splits dimensionless frequency ``p=R|w|`` into ``[0,1]``,
    ``[1,P]``, and ``[P,infinity)`` with ``P=ceil(32R/a)``.  On the first two
    intervals, positivity of the seed measure gives global sinc-derivative
    bounds.  On the tail, :func:`smooth_seed_transform_tail_envelope` supplies
    ``F,F',F''=O(p^-3)``, so every derivative of the regulated square root
    through second order is bounded by a constant times ``p^-9/2``.

    The constants intentionally use ``pi<22/7``, ``pi>3``, ``2pi<7``, and
    ``exp(2pi)>400``.  They are much looser than the finite-window quadrature,
    but they enclose the exact continuum integrals without extrapolating a
    discrete transform.
    """
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    ratio = support_radius / radius
    ratio_fraction = Fraction.from_float(ratio)
    radius_fraction = Fraction.from_float(radius)
    tail = smooth_seed_transform_tail_envelope(
        support_radius_ratio=ratio,
    )
    exact_tail = _smooth_seed_tail_envelope_fractions(ratio_fraction)
    seed_radius = ratio_fraction / 2
    pi_upper = Fraction(22, 7)

    # Dimensionless bare-root bounds on 0<=p<=1.  For
    # h=p/(1-exp(-2pi p)), h' lies in [1/2,1] and
    # 0<=h''<=2pi/6.  The latter follows from the partial-fraction expansion
    # of coth.  Rational relaxations avoid dependence on transcendental
    # floating-point values in the proof constants.
    bare_low = Fraction(2, 9)
    bare_first_low = Fraction(13, 18)
    bare_second_low = Fraction(25, 2)
    low_positive = (
        bare_low,
        bare_first_low + bare_low * seed_radius,
        bare_second_low
        + 2 * bare_first_low * seed_radius
        + bare_low * 7 * seed_radius**2 / 6,
    )

    # On p>=1, sqrt(j_0)<=p^(3/2)/6 and its first two logarithmic
    # derivative coefficients are bounded by 81/80 and 21/8.
    bare_tail_prefactor = Fraction(1, 6)
    bare_first_log_coefficient = Fraction(81, 80)
    bare_second_coefficient = Fraction(21, 8)
    middle_positive = (
        bare_tail_prefactor,
        bare_tail_prefactor
        * (bare_first_log_coefficient + seed_radius),
        bare_tail_prefactor
        * (
            bare_second_coefficient
            + 2 * bare_first_log_coefficient * seed_radius
            + 7 * seed_radius**2 / 6
        ),
    )

    transform = exact_tail["f0"]
    transform_first = exact_tail["f1"]
    transform_second = exact_tail["f2"]
    amplitude = transform**2
    amplitude_first = 2 * transform * transform_first
    amplitude_second = 2 * (
        transform_first**2 + transform * transform_second
    )
    tail_positive = (
        bare_tail_prefactor * amplitude,
        bare_tail_prefactor
        * (
            bare_first_log_coefficient * amplitude + amplitude_first
        ),
        bare_tail_prefactor
        * (
            bare_second_coefficient * amplitude
            + 2 * bare_first_log_coefficient * amplitude_first
            + amplitude_second
        ),
    )

    def negative_coefficients(
        positive: tuple[Fraction, Fraction, Fraction],
    ) -> tuple[Fraction, Fraction, Fraction]:
        return (
            positive[0],
            pi_upper * positive[0] + positive[1],
            positive[2]
            + 2 * pi_upper * positive[1]
            + pi_upper**2 * positive[0],
        )

    low_negative = negative_coefficients(low_positive)
    middle_negative = negative_coefficients(middle_positive)
    tail_negative = negative_coefficients(tail_positive)
    split = (
        32 * ratio_fraction.denominator + ratio_fraction.numerator - 1
    ) // ratio_fraction.numerator
    middle_integral = Fraction(split**4 - 1, 4)
    tail_integral = Fraction(1, 8 * split**8)
    squared_dimensionless_bounds = tuple(
        low_positive[order] ** 2
        + low_negative[order] ** 2
        + (
            middle_positive[order] ** 2
            + middle_negative[order] ** 2
        )
        * middle_integral
        + (tail_positive[order] ** 2 + tail_negative[order] ** 2)
        * tail_integral
        for order in range(3)
    )
    squared_norm_bounds = tuple(
        squared_dimensionless_bounds[order]
        * radius_fraction ** (2 * order - 4)
        for order in range(3)
    )
    norm_bounds = tuple(
        _fraction_sqrt_upper(value) for value in squared_norm_bounds
    )
    jump_l1 = _fraction_sqrt_upper(
        2 * pi_upper * norm_bounds[0] * norm_bounds[1]
    )
    jump_first = _fraction_sqrt_upper(
        2 * pi_upper * norm_bounds[1] * norm_bounds[2]
    )
    return {
        "result_type": "closed_form_exact_profile_sobolev_upper_enclosure",
        "radius": radius,
        "support_radius": support_radius,
        "dimensionless_tail_split": split,
        "transform_tail_envelope": tail,
        "sqrt_spectrum_l2_upper_bound": _fraction_upper_float(norm_bounds[0]),
        "sqrt_spectrum_first_derivative_l2_upper_bound": (
            _fraction_upper_float(norm_bounds[1])
        ),
        "sqrt_spectrum_second_derivative_l2_upper_bound": (
            _fraction_upper_float(norm_bounds[2])
        ),
        "jump_l1_sobolev_upper_bound": _fraction_upper_float(jump_l1),
        "jump_first_moment_sobolev_upper_bound": (
            _fraction_upper_float(jump_first)
        ),
        "sqrt_spectrum_l2_upper_bound_exact": str(norm_bounds[0]),
        "sqrt_spectrum_first_derivative_l2_upper_bound_exact": str(
            norm_bounds[1]
        ),
        "sqrt_spectrum_second_derivative_l2_upper_bound_exact": str(
            norm_bounds[2]
        ),
        "jump_l1_sobolev_upper_bound_exact": str(jump_l1),
        "jump_first_moment_sobolev_upper_bound_exact": str(jump_first),
        "exact_integral_profile_enclosed": True,
        "finite_simpson_transform_extrapolated_to_infinity": False,
        "proof_constants_are_deliberately_conservative": True,
    }


def static_patch_smooth_worldtube_ule_certificate(
    *,
    maximum_spin: int = 4096,
    radius: float = 1.0,
    support_radius: float = 0.2,
) -> dict[str, object]:
    """Audit the named compact smooth profile and its numerical ULE constants."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 64:
        raise ValueError("maximum_spin must be at least sixty-four")
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    ratio = support_radius / radius
    if ratio < 0.1 or ratio > 0.25:
        raise ValueError(
            "certificate requires 0.1 <= support_radius/radius <= 0.25"
        )

    base_window = 80.0 / support_radius
    coarse = smooth_worldtube_moment_record(
        radius=radius,
        support_radius=support_radius,
        frequency_window=base_window,
        frequency_steps=1_600,
        radial_steps=200,
    )
    refined = smooth_worldtube_moment_record(
        radius=radius,
        support_radius=support_radius,
        frequency_window=base_window,
        frequency_steps=3_200,
        radial_steps=400,
    )
    wider = smooth_worldtube_moment_record(
        radius=radius,
        support_radius=support_radius,
        frequency_window=2.0 * base_window,
        frequency_steps=6_400,
        radial_steps=400,
    )
    norm_keys = (
        "sqrt_spectrum_l2",
        "sqrt_spectrum_first_derivative_l2",
        "sqrt_spectrum_second_derivative_l2",
    )
    discretization_changes = tuple(
        abs(refined[key] / coarse[key] - 1.0) for key in norm_keys
    )
    window_changes = tuple(
        abs(wider[key] / refined[key] - 1.0) for key in norm_keys
    )
    numerical_margin = 1.0 + 10.0 * max(
        max(discretization_changes),
        max(window_changes),
        1.0e-6,
    )
    jump_l1_input = wider["jump_l1_sobolev_estimate"] * numerical_margin
    jump_first_input = (
        wider["jump_first_moment_sobolev_estimate"] * numerical_margin
    )
    analytic_enclosure = smooth_worldtube_analytic_sobolev_upper_bounds(
        radius=radius,
        support_radius=support_radius,
    )
    analytic_jump_l1 = analytic_enclosure["jump_l1_sobolev_upper_bound"]
    analytic_jump_first = analytic_enclosure[
        "jump_first_moment_sobolev_upper_bound"
    ]
    dimension = 2 * maximum_spin + 1
    lapse = 1.0 / dimension
    constant_cap = logarithmic_heat_ule_coupling_cap(
        maximum_spin,
        lapse,
        1.0 / (4.0 * dimension),
        jump_l1_input,
        jump_first_input,
        radius=radius,
    )
    heat_cap = logarithmic_heat_ule_coupling_cap(
        maximum_spin,
        lapse,
        1.0 / (4.0 * dimension**2),
        jump_l1_input,
        jump_first_input,
        radius=radius,
    )
    analytic_cap_float_guard = 0.999999
    analytic_constant_cap = (
        analytic_cap_float_guard
        * logarithmic_heat_ule_coupling_cap(
            maximum_spin,
            lapse,
            1.0 / (4.0 * dimension),
            analytic_jump_l1,
            analytic_jump_first,
            radius=radius,
        )
    )
    analytic_heat_cap = analytic_cap_float_guard * logarithmic_heat_ule_coupling_cap(
        maximum_spin,
        lapse,
        1.0 / (4.0 * dimension**2),
        analytic_jump_l1,
        analytic_jump_first,
        radius=radius,
    )
    comparison_support = 2.0 * support_radius
    narrower_support = 0.5 * support_radius
    localization_penalty: dict[str, object] | None = None
    if comparison_support <= 0.5 * radius:
        comparison = smooth_worldtube_moment_record(
            radius=radius,
            support_radius=comparison_support,
            frequency_window=160.0 / comparison_support,
            frequency_steps=3_200,
            radial_steps=400,
        )
        narrower = smooth_worldtube_moment_record(
            radius=radius,
            support_radius=narrower_support,
            frequency_window=160.0 / narrower_support,
            frequency_steps=3_200,
            radial_steps=400,
        )
        scale_factor = comparison_support / support_radius

        def exponent(comparison_value: float, base_value: float) -> float:
            return log(comparison_value / base_value) / log(scale_factor)

        comparison_cap = logarithmic_heat_ule_coupling_cap(
            maximum_spin,
            lapse,
            1.0 / (4.0 * dimension),
            comparison["jump_l1_sobolev_estimate"] * numerical_margin,
            comparison["jump_first_moment_sobolev_estimate"] * numerical_margin,
            radius=radius,
        )
        narrower_cap = logarithmic_heat_ule_coupling_cap(
            maximum_spin,
            lapse,
            1.0 / (4.0 * dimension),
            narrower["jump_l1_sobolev_estimate"] * numerical_margin,
            narrower["jump_first_moment_sobolev_estimate"] * numerical_margin,
            radius=radius,
        )
        wide_log_slope = (
            wider["sqrt_spectrum_second_derivative_l2"] ** 2
            - comparison["sqrt_spectrum_second_derivative_l2"] ** 2
        ) / log(comparison_support / support_radius)
        narrow_log_slope = (
            narrower["sqrt_spectrum_second_derivative_l2"] ** 2
            - wider["sqrt_spectrum_second_derivative_l2"] ** 2
        ) / log(support_radius / narrower_support)
        predicted_log_slope = 3.0 / (64.0 * pi**2)

        def corrected_cap_amplitude(cap: float, support: float) -> float:
            logarithm = log(radius / support)
            return cap * logarithm ** (1.0 / 8.0) / support**2.5

        localization_penalty = {
            "narrower_support_radius": narrower_support,
            "base_support_radius": support_radius,
            "comparison_support_radius": comparison_support,
            "narrower_moment_record": narrower,
            "comparison_moment_record": comparison,
            "sqrt_spectrum_l2_exponent": exponent(
                comparison["sqrt_spectrum_l2"],
                wider["sqrt_spectrum_l2"],
            ),
            "first_derivative_l2_exponent": exponent(
                comparison["sqrt_spectrum_first_derivative_l2"],
                wider["sqrt_spectrum_first_derivative_l2"],
            ),
            "second_derivative_l2_exponent": exponent(
                comparison["sqrt_spectrum_second_derivative_l2"],
                wider["sqrt_spectrum_second_derivative_l2"],
            ),
            "second_derivative_squared_log_slope_wide": wide_log_slope,
            "second_derivative_squared_log_slope_narrow": narrow_log_slope,
            "predicted_second_derivative_squared_log_slope": (
                predicted_log_slope
            ),
            "relative_log_slope_change": abs(
                narrow_log_slope / wide_log_slope - 1.0
            ),
            "jump_l1_estimate_exponent": exponent(
                comparison["jump_l1_sobolev_estimate"],
                wider["jump_l1_sobolev_estimate"],
            ),
            "jump_first_moment_estimate_exponent": exponent(
                comparison["jump_first_moment_sobolev_estimate"],
                wider["jump_first_moment_sobolev_estimate"],
            ),
            "sufficient_coupling_cap_exponent": exponent(
                comparison_cap,
                constant_cap,
            ),
            "comparison_constant_obstruction_coupling_cap": comparison_cap,
            "narrower_constant_obstruction_coupling_cap": narrower_cap,
            "log_corrected_cap_amplitudes": (
                corrected_cap_amplitude(narrower_cap, narrower_support),
                corrected_cap_amplitude(constant_cap, support_radius),
                corrected_cap_amplitude(comparison_cap, comparison_support),
            ),
            "asymptotic_prediction": (
                "small-support UV scaling predicts Q0~a^-2, Q1~a^-1, "
                "Q2~sqrt(log(R/a)), G~a^-3/2, "
                "M1~a^-1/2 log(R/a)^1/4, and the sufficient cap "
                "a^5/2 log(R/a)^-1/8"
            ),
        }
    test_p = 1.7
    transform, first, second = smooth_seed_spherical_transform_derivatives(
        test_p,
        support_radius_ratio=ratio,
        radial_steps=400,
    )
    spacing = 1.0e-2
    plus_two = smooth_seed_spherical_transform_derivatives(
        test_p + 2.0 * spacing,
        support_radius_ratio=ratio,
        radial_steps=400,
    )[0]
    plus = smooth_seed_spherical_transform_derivatives(
        test_p + spacing,
        support_radius_ratio=ratio,
        radial_steps=400,
    )[0]
    minus = smooth_seed_spherical_transform_derivatives(
        test_p - spacing,
        support_radius_ratio=ratio,
        radial_steps=400,
    )[0]
    minus_two = smooth_seed_spherical_transform_derivatives(
        test_p - 2.0 * spacing,
        support_radius_ratio=ratio,
        radial_steps=400,
    )[0]
    finite_first = (
        minus_two - 8.0 * minus + 8.0 * plus - plus_two
    ) / (12.0 * spacing)
    finite_second = (
        -plus_two + 16.0 * plus - 30.0 * transform + 16.0 * minus - minus_two
    ) / (12.0 * spacing**2)
    numerical_consistency_checks = {
        "seed_formula_has_compact_support_values": (
            smooth_compact_seed_shape(0.0) == 1.0
            and smooth_compact_seed_shape(1.0) == 0.0
            and smooth_compact_seed_shape(2.0) == 0.0
        ),
        "spherical_transform_is_normalized": abs(
            smooth_seed_spherical_transform_derivatives(
                0.0,
                support_radius_ratio=ratio,
                radial_steps=400,
            )[0]
            - 1.0
        )
        < 1.0e-14,
        "sampled_transform_first_derivative_matches_finite_difference": abs(
            first - finite_first
        )
        < 1.0e-8,
        "sampled_transform_second_derivative_matches_finite_difference": abs(
            second - finite_second
        )
        < 2.0e-7,
        "sobolev_norms_are_positive": all(wider[key] > 0.0 for key in norm_keys),
        "radial_and_frequency_refinement_is_stable": max(
            discretization_changes
        )
        < 2.0e-4,
        "frequency_window_doubling_is_stable": max(window_changes) < 2.0e-4,
        "finite_window_norm_estimates_lie_below_analytic_enclosures": all(
            wider[key] <= analytic_enclosure[upper_key]
            for key, upper_key in zip(
                norm_keys,
                (
                    "sqrt_spectrum_l2_upper_bound",
                    "sqrt_spectrum_first_derivative_l2_upper_bound",
                    "sqrt_spectrum_second_derivative_l2_upper_bound",
                ),
            )
        ),
        "analytic_exact_profile_enclosure_has_positive_moment_bounds": (
            analytic_jump_l1 > 0.0 and analytic_jump_first > 0.0
        ),
        "numerical_candidate_constant_obstruction_cap_is_positive": constant_cap
        > 0.0,
        "numerical_candidate_heat_matching_cap_is_positive": heat_cap > 0.0,
    }
    if localization_penalty is not None:
        numerical_consistency_checks.update(
            {
                "finite_support_data_is_consistent_with_q0_a_minus_two": abs(
                    localization_penalty["sqrt_spectrum_l2_exponent"] + 2.0
                )
                < 0.05,
                "finite_support_data_is_consistent_with_q1_a_minus_one": abs(
                    localization_penalty["first_derivative_l2_exponent"] + 1.0
                )
                < 0.05,
                "finite_support_data_is_consistent_with_q2_squared_logarithm": (
                    localization_penalty["second_derivative_squared_log_slope_wide"]
                    > 0.0
                    and localization_penalty[
                        "second_derivative_squared_log_slope_narrow"
                    ]
                    > 0.0
                    and localization_penalty["relative_log_slope_change"]
                    < 0.12
                    and abs(
                        localization_penalty[
                            "second_derivative_squared_log_slope_narrow"
                        ]
                        / localization_penalty[
                            "predicted_second_derivative_squared_log_slope"
                        ]
                        - 1.0
                    )
                    < 0.1
                ),
                "finite_support_data_is_consistent_with_g_a_minus_three_halves": abs(
                    localization_penalty["jump_l1_estimate_exponent"] + 1.5
                )
                < 0.08,
                "finite_support_m1_effective_exponent_is_consistent_with_log": (
                    -0.65
                    < localization_penalty[
                        "jump_first_moment_estimate_exponent"
                    ]
                    < -0.5
                ),
                "finite_support_cap_exponent_is_consistent_with_five_halves": abs(
                    localization_penalty["sufficient_coupling_cap_exponent"]
                    - 2.5
                )
                < 0.12,
            }
        )
    return {
        "goal": "Smooth Compact Worldtube Profile-Specific ULE Gate",
        "status": "pass" if all(numerical_consistency_checks.values()) else "fail",
        "result_type": "step_converged_smooth_profile_ule_constants",
        "central_result": (
            "A named C-infinity radial seed supported in half the optical "
            "worldtube radius has normalized spherical transform F. Its "
            "convolution square is supported in the full worldtube radius, has "
            "nonnegative amplitude multiplier F^2, and gives spectrum j0 F^4. "
            "Analytic transform derivatives and frequency Sobolev quadrature "
            "produce profile-specific numerical ULE moment estimates and "
            "candidate coupling schedules."
        ),
        "support_radius": support_radius,
        "seed_support_radius": 0.5 * support_radius,
        "coarse_moment_record": coarse,
        "refined_moment_record": refined,
        "wide_moment_record": wider,
        "relative_discretization_changes": discretization_changes,
        "relative_window_changes": window_changes,
        "numerical_safety_margin": numerical_margin,
        "profile_specific_jump_l1_input": jump_l1_input,
        "profile_specific_jump_first_moment_input": jump_first_input,
        "analytic_exact_profile_enclosure": analytic_enclosure,
        "maximum_spin": maximum_spin,
        "dimension": dimension,
        "numerical_constant_obstruction_coupling_cap": constant_cap,
        "numerical_heat_matching_coupling_cap": heat_cap,
        "analytic_enclosure_constant_obstruction_guarded_float_cap": (
            analytic_constant_cap
        ),
        "analytic_enclosure_heat_matching_guarded_float_cap": analytic_heat_cap,
        "analytic_enclosure_cap_formula_is_symbolically_sufficient": True,
        "analytic_enclosure_cap_float_evaluation_directed": False,
        "analytic_enclosure_cap_float_guard": analytic_cap_float_guard,
        "scaled_constant_cap": (
            constant_cap * dimension**3.5 * sqrt(log(float(dimension)))
        ),
        "scaled_heat_cap": (
            heat_cap * dimension**4 * sqrt(log(float(dimension)))
        ),
        "profile_specific_constants_interval_certified": False,
        "exact_profile_sobolev_norms_analytically_enclosed": True,
        "frequency_tails_rigorously_enclosed": True,
        "localization_penalty_record": localization_penalty,
        "numerical_consistency_checks": numerical_consistency_checks,
        "claim_boundary": (
            "The spatial seed is C-infinity and compact, but exact stationarity "
            "means the interaction is not compact in time. The tight reported "
            "norm estimates are step- and window-converged floating-point "
            "quadratures, not interval enclosures. A separate closed-form "
            "integration-by-parts argument now gives conservative upper "
            "enclosures for the exact profile and its infinite-frequency tails. "
            "It does not extrapolate the finite Simpson transform. The optical "
            "weight is engineered and has not yet been derived from a Skyrmion "
            "or other finite matter current. Derivation of the prescribed "
            "switch from the matter action, direct "
            "interactions, stress, lifetime, and gravity remain open."
        ),
        "candidate_prediction": (
            "In the small-support UV regime, the optimized Sobolev-ULE "
            "sufficient coupling cap carries an additional "
            "a^(5/2)[log(R/a)]^(-1/8) penalty. This is a derived candidate "
            "tradeoff for this sufficient error-control route, not a lower "
            "bound excluding stronger non-Markov or profile-adapted methods."
        ),
        "next_physics_gate": (
            "sharpen the conservative analytic Sobolev enclosures by certified "
            "finite-window quadrature, and derive the smooth optical weight and "
            "switching function from a finite covariant matter-worldtube action"
        ),
    }
