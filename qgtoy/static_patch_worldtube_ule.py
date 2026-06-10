"""Stationary optical-worldtube regulators and a stabilized ULE bound.

The Gaussian frequency factor used by :mod:`static_patch_overlapping_ule` is
the exact spherical multiplier of a shifted heat kernel on optical ``H^3_R``.
That kernel has Gaussian tails and is therefore quasilocal, not supported in a
bounded worldtube.  This module also gives an explicit compact radial
replacement, proves the relevant UV improvement, and records the
Nathan--Rudner operator-norm estimate after adjoining an arbitrary inert
ancilla.

The stationary ULE statement is conditional on a zero-mean Gaussian bath and
finite jump-correlator moments.  A companion module replaces remote-past
factorization by a finite amplitude ramp, plateau, and burn-in.  The result is
an ancilla-stable spectral-state estimate, not a trace- or diamond-norm bound.
"""

from __future__ import annotations

from math import cos, cosh, exp, expm1, isfinite, log, pi, sin, sinh, sqrt

from .static_patch_overlapping_ule import (
    smeared_gradient_zero_frequency_spectrum,
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


def _scaled_ball_normalization(radius_ratio: float) -> float:
    """Return ``(A cosh(A)-sinh(A))/A^3`` without small-``A`` loss."""
    if radius_ratio < 1.0e-2:
        squared = radius_ratio * radius_ratio
        return (
            1.0 / 3.0
            + squared / 30.0
            + squared**2 / 840.0
            + squared**3 / 45_360.0
        )
    return (
        radius_ratio * cosh(radius_ratio) - sinh(radius_ratio)
    ) / radius_ratio**3


def _hyperbolic_sinc(radius_ratio: float) -> float:
    """Return ``sinh(A)/A`` with a stable origin expansion."""
    if radius_ratio < 1.0e-2:
        squared = radius_ratio * radius_ratio
        return (
            1.0
            + squared / 6.0
            + squared**2 / 120.0
            + squared**3 / 5_040.0
        )
    return sinh(radius_ratio) / radius_ratio


def _cosh_minus_hyperbolic_sinc(radius_ratio: float) -> float:
    """Return ``cosh(A)-sinh(A)/A`` stably near the origin."""
    if radius_ratio < 1.0e-2:
        squared = radius_ratio * radius_ratio
        return (
            squared / 3.0
            + squared**2 / 30.0
            + squared**3 / 840.0
            + squared**4 / 45_360.0
        )
    return cosh(radius_ratio) - sinh(radius_ratio) / radius_ratio


def shifted_hyperbolic_heat_profile(
    optical_radius: float,
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
) -> float:
    """Return the DC-normalized shifted heat kernel on optical ``H^3_R``.

    At heat time ``t=sigma^2/2`` the shifted semigroup
    ``exp[t(Delta_H+R^-2)]`` has multiplier ``exp(-sigma^2 w^2/2)``.
    Squaring that field-amplitude multiplier gives the Gaussian spectral
    factor used by the earlier overlapping-sector module.
    """
    _validate_nonnegative("optical_radius", optical_radius)
    _validate_positive("radius", radius)
    _validate_positive("smearing_width", smearing_width)
    if optical_radius == 0.0:
        radial_factor = 1.0
    else:
        scaled_radius = optical_radius / radius
        radial_factor = scaled_radius / sinh(scaled_radius)
    normalization = (2.0 * pi * smearing_width**2) ** -1.5
    return (
        normalization
        * radial_factor
        * exp(-(optical_radius / smearing_width) ** 2 / 2.0)
    )


def shifted_hyperbolic_heat_multiplier(
    frequency: float,
    *,
    smearing_width: float = 0.2,
) -> float:
    """Return the exact field-amplitude heat multiplier."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("smearing_width", smearing_width)
    return exp(-0.5 * (smearing_width * frequency) ** 2)


def numerical_shifted_hyperbolic_heat_multiplier(
    frequency: float,
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
    radial_standard_deviations: float = 10.0,
    steps: int = 20_000,
) -> float:
    """Independently integrate the heat kernel against the ``H^3`` mode."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    _validate_positive("smearing_width", smearing_width)
    _validate_positive("radial_standard_deviations", radial_standard_deviations)
    _validate_positive_integer("steps", steps)
    if steps % 2:
        raise ValueError("steps must be even")
    p = abs(radius * frequency)
    upper_y = radial_standard_deviations * smearing_width / radius
    spacing = upper_y / steps
    normalization = 4.0 * pi * radius**3 * (
        2.0 * pi * smearing_width**2
    ) ** -1.5

    def integrand(y_value: float) -> float:
        gaussian = exp(
            -0.5 * (radius * y_value / smearing_width) ** 2
        )
        if p == 0.0:
            return y_value * y_value * gaussian
        return y_value * sin(p * y_value) * gaussian / p

    total = integrand(0.0) + integrand(upper_y)
    total += 4.0 * sum(
        integrand(index * spacing) for index in range(1, steps, 2)
    )
    total += 2.0 * sum(
        integrand(index * spacing) for index in range(2, steps, 2)
    )
    return normalization * spacing * total / 3.0


def compact_ball_spherical_multiplier(
    spectral_parameter: float,
    *,
    support_radius_ratio: float = 0.2,
) -> float:
    """Return the normalized ``H^3`` ball multiplier ``q_A(p)``.

    ``A=a/R`` is the radius of the seed ball.  Convolving two such radial
    profiles gives a field smearing supported in optical radius ``2a`` and
    amplitude multiplier ``q_A(p)^2``.  The associated spectrum is multiplied
    by ``q_A(p)^4``.
    """
    if not isfinite(spectral_parameter):
        raise ValueError("spectral_parameter must be finite")
    _validate_positive("support_radius_ratio", support_radius_ratio)
    p = abs(spectral_parameter)
    a = support_radius_ratio
    x = a * p
    hyperbolic_cosine = cosh(a)
    hyperbolic_sinc = _hyperbolic_sinc(a)
    scaled_normalization = _scaled_ball_normalization(a)
    if x < 1.0e-4:
        numerator_over_x = (
            _cosh_minus_hyperbolic_sinc(a)
            + x * x * (-hyperbolic_cosine / 6.0 + hyperbolic_sinc / 2.0)
            + x**4 * (hyperbolic_cosine / 120.0 - hyperbolic_sinc / 24.0)
            + x**6 * (-hyperbolic_cosine / 5_040.0 + hyperbolic_sinc / 720.0)
        )
        return numerator_over_x / (
            (a * a + x * x) * scaled_normalization
        )
    numerator = hyperbolic_cosine * sin(x) - x * hyperbolic_sinc * cos(x)
    denominator = x * (a * a + x * x) * scaled_normalization
    return numerator / denominator


def numerical_compact_ball_spherical_multiplier(
    spectral_parameter: float,
    *,
    support_radius_ratio: float = 0.2,
    steps: int = 4_000,
) -> float:
    """Independently integrate the normalized ``H^3`` ball transform."""
    if not isfinite(spectral_parameter):
        raise ValueError("spectral_parameter must be finite")
    _validate_positive("support_radius_ratio", support_radius_ratio)
    _validate_positive_integer("steps", steps)
    if steps % 2:
        raise ValueError("steps must be even")
    p = abs(spectral_parameter)
    a = support_radius_ratio
    normalization = a**3 * _scaled_ball_normalization(a)
    spacing = a / steps

    def integrand(y_value: float) -> float:
        if p == 0.0:
            return y_value * sinh(y_value)
        return sinh(y_value) * sin(p * y_value) / p

    total = integrand(0.0) + integrand(a)
    total += 4.0 * sum(
        integrand(index * spacing) for index in range(1, steps, 2)
    )
    total += 2.0 * sum(
        integrand(index * spacing) for index in range(2, steps, 2)
    )
    return spacing * total / (3.0 * normalization)


def compact_worldtube_amplitude_multiplier(
    frequency: float,
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
) -> float:
    """Return the double-ball field-amplitude multiplier ``q_A(Rw)^2``."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    ratio = support_radius / radius
    q_value = compact_ball_spherical_multiplier(
        radius * frequency,
        support_radius_ratio=ratio,
    )
    return q_value * q_value


def compact_worldtube_gradient_spectrum(
    frequency: float,
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
) -> float:
    """Return the strictly supported double-ball gradient spectrum.

    The double-ball profile is supported in optical radius ``2a``.  It is an
    idealized finite-regularity source.  A compact ``C-infinity`` radial bump
    convolved with its reflection gives the same positivity, KMS, support, and
    rapid-decay conclusions, but not this elementary closed multiplier.
    """
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    if frequency == 0.0:
        return smeared_gradient_zero_frequency_spectrum(radius=radius)
    if frequency < 0.0:
        return exp(2.0 * pi * radius * frequency) * (
            compact_worldtube_gradient_spectrum(
                -frequency,
                radius=radius,
                support_radius=support_radius,
            )
        )
    bare = (
        frequency
        * (1.0 + (radius * frequency) ** 2)
        / (
            12.0
            * pi**2
            * radius**2
            * (-expm1(-2.0 * pi * radius * frequency))
        )
    )
    amplitude = compact_worldtube_amplitude_multiplier(
        frequency,
        radius=radius,
        support_radius=support_radius,
    )
    return bare * amplitude * amplitude


def compact_ball_uv_envelope_constant(
    *, support_radius_ratio: float = 0.2
) -> float:
    """Return ``C_A`` such that ``|q_A(p)|<=C_A/p^2`` for ``p>=1``."""
    _validate_positive("support_radius_ratio", support_radius_ratio)
    a = support_radius_ratio
    return (cosh(a) + sinh(a)) / (
        a**3 * _scaled_ball_normalization(a)
    )


def compact_worldtube_lamb_shift_coefficient(
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
    upper_spectral_parameter: float = 400.0,
    steps: int = 40_000,
) -> float:
    """Numerically evaluate the compact-filter zero-Bohr Lamb coefficient.

    The omitted positive tail of the dimensionless integral is bounded by
    ``(2/5) C_A^4 p_max^-5`` once ``p_max>=1``.  The returned value is the
    Simpson estimate; use :func:`compact_worldtube_lamb_tail_bound` to report
    the separate analytic tail certificate.
    """
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    _validate_positive("upper_spectral_parameter", upper_spectral_parameter)
    _validate_positive_integer("steps", steps)
    if upper_spectral_parameter < 1.0:
        raise ValueError("upper_spectral_parameter must be at least one")
    if steps % 2:
        raise ValueError("steps must be even")
    ratio = support_radius / radius
    spacing = upper_spectral_parameter / steps

    def integrand(p_value: float) -> float:
        q_value = compact_ball_spherical_multiplier(
            p_value,
            support_radius_ratio=ratio,
        )
        return (1.0 + p_value * p_value) * q_value**4

    total = integrand(0.0) + integrand(upper_spectral_parameter)
    total += 4.0 * sum(
        integrand(index * spacing) for index in range(1, steps, 2)
    )
    total += 2.0 * sum(
        integrand(index * spacing) for index in range(2, steps, 2)
    )
    integral = spacing * total / 3.0
    return -integral / (12.0 * pi**2 * radius**3)


def compact_worldtube_lamb_tail_bound(
    *,
    radius: float = 1.0,
    support_radius: float = 0.2,
    lower_spectral_parameter: float = 400.0,
) -> float:
    """Bound the magnitude of the omitted Lamb-shift tail."""
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    _validate_positive("lower_spectral_parameter", lower_spectral_parameter)
    if lower_spectral_parameter < 1.0:
        raise ValueError("lower_spectral_parameter must be at least one")
    envelope = compact_ball_uv_envelope_constant(
        support_radius_ratio=support_radius / radius
    )
    dimensionless_tail = (
        2.0 * envelope**4 / (5.0 * lower_spectral_parameter**5)
    )
    return dimensionless_tail / (12.0 * pi**2 * radius**3)


def gaussian_compact_support_growth_gap(
    imaginary_spectral_parameter: float,
    *,
    radius: float = 1.0,
    smearing_width: float = 0.2,
    compact_support_radius: float = 0.4,
) -> float:
    """Return the quadratic-minus-linear Paley--Wiener growth exponent.

    A compact radial profile of support ``a`` has an entire spherical transform
    of exponential type at most ``a`` (up to polynomial factors), whereas the
    analytic continuation of the Gaussian amplitude grows quadratically on the
    imaginary axis.  A growing positive gap certifies incompatibility.
    """
    _validate_positive(
        "imaginary_spectral_parameter", imaginary_spectral_parameter
    )
    _validate_positive("radius", radius)
    _validate_positive("smearing_width", smearing_width)
    _validate_positive("compact_support_radius", compact_support_radius)
    eta = imaginary_spectral_parameter
    return (
        smearing_width**2 * eta**2 / (2.0 * radius**2)
        - compact_support_radius * eta / radius
    )


def sobolev_jump_correlator_moment_bounds(
    sqrt_spectrum_l2: float,
    first_derivative_l2: float,
    second_derivative_l2: float,
    *,
    time_scale: float = 1.0,
) -> tuple[float, float]:
    """Bound ``G=int|g|`` and ``M1=int|t g|`` by frequency Sobolev norms.

    For the unitary Fourier convention used by Nathan--Rudner,

    ``g(t)=(2pi)^(-1/2) int sqrt(j(w)) exp(-iwt) dw``.

    Weighted Cauchy--Schwarz and Plancherel give the returned rigorous bounds.
    The free ``time_scale`` keeps the inequalities dimensionally homogeneous.
    """
    _validate_nonnegative("sqrt_spectrum_l2", sqrt_spectrum_l2)
    _validate_nonnegative("first_derivative_l2", first_derivative_l2)
    _validate_nonnegative("second_derivative_l2", second_derivative_l2)
    _validate_positive("time_scale", time_scale)
    g_bound = sqrt(pi * time_scale) * sqrt(
        sqrt_spectrum_l2**2
        + first_derivative_l2**2 / time_scale**2
    )
    first_moment_bound = sqrt(pi * time_scale) * sqrt(
        first_derivative_l2**2
        + second_derivative_l2**2 / time_scale**2
    )
    return g_bound, first_moment_bound


def optimal_sobolev_jump_correlator_moment_bounds(
    sqrt_spectrum_l2: float,
    first_derivative_l2: float,
    second_derivative_l2: float,
) -> tuple[float, float]:
    """Return the separately optimized weighted-Sobolev moment bounds.

    Minimizing the two Cauchy--Schwarz estimates over their independent time
    scales gives ``G<=sqrt(2pi ||q||_2 ||q'||_2)`` and
    ``M1<=sqrt(2pi ||q'||_2 ||q''||_2)``.
    """
    _validate_positive("sqrt_spectrum_l2", sqrt_spectrum_l2)
    _validate_positive("first_derivative_l2", first_derivative_l2)
    _validate_positive("second_derivative_l2", second_derivative_l2)
    return (
        sqrt(2.0 * pi * sqrt_spectrum_l2 * first_derivative_l2),
        sqrt(2.0 * pi * first_derivative_l2 * second_derivative_l2),
    )


def three_channel_ule_parameters(
    spin: int,
    lapse: float,
    coupling: float,
    jump_l1: float,
    jump_first_moment: float,
) -> tuple[float, float]:
    """Return exact ``Gamma`` and ``tau`` from exact bath moments.

    Independent upper bounds on ``G`` and ``M_1`` do not upper-bound their
    ratio.  Use :func:`ancilla_stable_ule_spectral_residual_bound` to insert
    independent moment bounds safely through the products ``G M_1`` and
    ``G^3 M_1``.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_nonnegative("coupling", coupling)
    _validate_positive("jump_l1", jump_l1)
    _validate_nonnegative("jump_first_moment", jump_first_moment)
    gamma = 144.0 * coupling**2 * spin**2 * jump_l1**2 / lapse**2
    tau = jump_first_moment / jump_l1
    return gamma, tau


def ancilla_stable_ule_spectral_residual_bound(
    spin: int,
    lapse: float,
    coupling: float,
    elapsed_time: float,
    jump_l1_bound: float,
    jump_first_moment_bound: float,
) -> float:
    """Return ``2 Gamma tau + 2 Gamma^2 tau t``.

    This compares the exact Gaussian-bath reduced state to the zero-Bohr ULE
    semigroup initialized at the physical state.  It remains valid after
    adjoining an arbitrary inert memory because ``X_a tensor I`` has the same
    operator norm and the ULE is unital.  Remote-past preparation or a separate
    finite-switching transient estimate is required.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_nonnegative("coupling", coupling)
    _validate_nonnegative("elapsed_time", elapsed_time)
    _validate_positive("jump_l1_bound", jump_l1_bound)
    _validate_nonnegative(
        "jump_first_moment_bound", jump_first_moment_bound
    )
    prefactor = 144.0 * coupling**2 * spin**2 / lapse**2
    return (
        2.0 * prefactor * jump_l1_bound * jump_first_moment_bound
        + 2.0
        * prefactor**2
        * jump_l1_bound**3
        * jump_first_moment_bound
        * elapsed_time
    )


def logarithmic_heat_ule_residual_bound(
    spin: int,
    lapse: float,
    coupling: float,
    jump_l1_bound: float,
    jump_first_moment_bound: float,
    *,
    radius: float = 1.0,
) -> float:
    """Return the stabilized residual at heat time ``s=log(d)/2``."""
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_nonnegative("coupling", coupling)
    _validate_positive("jump_l1_bound", jump_l1_bound)
    _validate_nonnegative(
        "jump_first_moment_bound", jump_first_moment_bound
    )
    _validate_positive("radius", radius)
    dimension = 2 * spin + 1
    zero_spectrum = smeared_gradient_zero_frequency_spectrum(radius=radius)
    first = (
        288.0
        * jump_l1_bound
        * jump_first_moment_bound
        * coupling**2
        * spin**2
        / lapse**2
    )
    second = (
        20_736.0
        / (pi * zero_spectrum)
        * jump_l1_bound**3
        * jump_first_moment_bound
        * coupling**2
        * spin**4
        * log(float(dimension))
        / lapse**2
    )
    return first + second


def logarithmic_heat_ule_coupling_cap(
    spin: int,
    lapse: float,
    spectral_residual_budget: float,
    jump_l1_bound: float,
    jump_first_moment_bound: float,
    *,
    radius: float = 1.0,
) -> float:
    """Return the exact sufficient coupling cap for a spectral budget."""
    _validate_positive_integer("spin", spin)
    _validate_positive("lapse", lapse)
    _validate_positive("spectral_residual_budget", spectral_residual_budget)
    _validate_positive("jump_l1_bound", jump_l1_bound)
    _validate_positive(
        "jump_first_moment_bound", jump_first_moment_bound
    )
    _validate_positive("radius", radius)
    dimension = 2 * spin + 1
    zero_spectrum = smeared_gradient_zero_frequency_spectrum(radius=radius)
    coefficient = (
        288.0
        * spin**2
        * jump_l1_bound
        * jump_first_moment_bound
        + 20_736.0
        / (pi * zero_spectrum)
        * spin**4
        * jump_l1_bound**3
        * jump_first_moment_bound
        * log(float(dimension))
    )
    return lapse * sqrt(spectral_residual_budget / coefficient)


def static_patch_worldtube_ule_certificate(
    *,
    maximum_spin: int = 4096,
    radius: float = 1.0,
    support_radius: float = 0.2,
) -> dict[str, object]:
    """Certify the local-filter theorem and stabilized ULE scaling law."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 64:
        raise ValueError("maximum_spin must be at least sixty-four")
    _validate_positive("radius", radius)
    _validate_positive("support_radius", support_radius)
    ratio = support_radius / radius
    if ratio > 20.0:
        raise ValueError("support_radius/radius must be at most twenty")
    test_frequency = 0.7 / radius
    positive = compact_worldtube_gradient_spectrum(
        test_frequency,
        radius=radius,
        support_radius=support_radius,
    )
    negative = compact_worldtube_gradient_spectrum(
        -test_frequency,
        radius=radius,
        support_radius=support_radius,
    )
    heat_multiplier = shifted_hyperbolic_heat_multiplier(
        test_frequency,
        smearing_width=support_radius,
    )
    numerical_heat_multiplier = numerical_shifted_hyperbolic_heat_multiplier(
        test_frequency,
        radius=radius,
        smearing_width=support_radius,
    )
    envelope = compact_ball_uv_envelope_constant(
        support_radius_ratio=ratio
    )
    large_p = 40.0 / ratio
    q_large = abs(
        compact_ball_spherical_multiplier(
            large_p,
            support_radius_ratio=ratio,
        )
    )
    lamb_cutoff = max(200.0 / ratio, 200.0)
    lamb_coefficient = compact_worldtube_lamb_shift_coefficient(
        radius=radius,
        support_radius=support_radius,
        upper_spectral_parameter=lamb_cutoff,
        steps=20_000,
    )
    lamb_tail = compact_worldtube_lamb_tail_bound(
        radius=radius,
        support_radius=support_radius,
        lower_spectral_parameter=lamb_cutoff,
    )

    # These are illustrative finite moment inputs for the scaling audit.  The
    # theorem above maps profile-specific Sobolev norms to rigorous bounds.
    jump_l1_bound = 3.0 / radius**1.5
    jump_first_moment_bound = 1.0 / radius**0.5
    spins = tuple(
        sorted(
            {
                spin
                for spin in (64, 256, 1024, maximum_spin)
                if spin <= maximum_spin
            }
            | {maximum_spin}
        )
    )
    records = []
    for spin in spins:
        dimension = 2 * spin + 1
        lapse = 1.0 / dimension
        constant_cap = logarithmic_heat_ule_coupling_cap(
            spin,
            lapse,
            1.0 / (4.0 * dimension),
            jump_l1_bound,
            jump_first_moment_bound,
            radius=radius,
        )
        heat_cap = logarithmic_heat_ule_coupling_cap(
            spin,
            lapse,
            1.0 / (4.0 * dimension**2),
            jump_l1_bound,
            jump_first_moment_bound,
            radius=radius,
        )
        records.append(
            {
                "spin_L": spin,
                "dimension_d": dimension,
                "lapse_N": lapse,
                "illustrative_constant_obstruction_scaling_cap": constant_cap,
                "scaled_constant_cap": (
                    constant_cap
                    * dimension**3.5
                    * sqrt(log(float(dimension)))
                ),
                "illustrative_heat_matching_scaling_cap": heat_cap,
                "scaled_heat_cap": (
                    heat_cap
                    * dimension**4
                    * sqrt(log(float(dimension)))
                ),
            }
        )
    first_record = records[0]
    last_record = records[-1]
    certified_claims = {
        "heat_kernel_profile_has_declared_spherical_multiplier": abs(
            numerical_heat_multiplier - heat_multiplier
        )
        < 1.0e-10,
        "closed_ball_multiplier_matches_independent_radial_quadrature": abs(
            compact_ball_spherical_multiplier(
                1.3,
                support_radius_ratio=ratio,
            )
            - numerical_compact_ball_spherical_multiplier(
                1.3,
                support_radius_ratio=ratio,
            )
        )
        < 1.0e-12,
        "compact_filter_is_normalized_at_zero": abs(
            compact_ball_spherical_multiplier(
                0.0,
                support_radius_ratio=ratio,
            )
            - 1.0
        )
        < 1.0e-15,
        "compact_filter_preserves_exact_kms_balance": abs(
            negative / positive - exp(-2.0 * pi * radius * test_frequency)
        )
        < 1.0e-12,
        "compact_filter_preserves_zero_frequency_rate": abs(
            compact_worldtube_gradient_spectrum(
                0.0,
                radius=radius,
                support_radius=support_radius,
            )
            - smeared_gradient_zero_frequency_spectrum(radius=radius)
        )
        < 1.0e-15,
        "double_ball_filter_has_p_minus_four_amplitude_envelope": (
            q_large * large_p**2 <= envelope
        ),
        "compact_lamb_shift_is_finite_with_small_certified_tail": (
            lamb_coefficient < 0.0 and lamb_tail < abs(lamb_coefficient) * 1.0e-6
        ),
        "exact_gaussian_exceeds_every_fixed_exponential_type": (
            gaussian_compact_support_growth_gap(
                200.0 / ratio,
                radius=radius,
                smearing_width=support_radius,
                compact_support_radius=2.0 * support_radius,
            )
            > 0.0
        ),
        "illustrative_constant_budget_schedule_has_d_minus_seven_halves_scaling": abs(
            last_record["scaled_constant_cap"]
            / first_record["scaled_constant_cap"]
            - 1.0
        )
        < 0.08,
        "illustrative_heat_matching_schedule_has_d_minus_four_scaling": abs(
            last_record["scaled_heat_cap"] / first_record["scaled_heat_cap"]
            - 1.0
        )
        < 0.08,
    }
    return {
        "goal": "Local Worldtube Filter And Ancilla-Stable ULE Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "local_filter_and_conditional_stabilized_ule_theorem",
        "central_result": (
            "The declared Gaussian is exactly a shifted optical-H3 heat-kernel "
            "smearing and therefore quasilocal. A double-ball convolution gives "
            "an explicit finite-worldtube replacement with exact KMS balance, "
            "the same zero mode, p^-8 spectral suppression, and finite bath "
            "moments. Under the Nathan-Rudner Gaussian-bath and remote-past "
            "hypotheses, adjoining any inert memory leaves Gamma and tau "
            "unchanged and proves the spectral residual "
            "2 Gamma tau+2 Gamma^2 tau t."
        ),
        "support_statement": (
            "The elementary double-ball field profile is supported in optical "
            f"radius {2.0 * support_radius:g}. It has finite regularity; replace "
            "the seed balls by compact smooth radial bumps for a smooth compact "
            "spatial profile, preserving support, positivity, KMS, and rapid "
            "decay but losing the elementary closed multiplier. A compact "
            "spacetime AQFT test function additionally requires switching."
        ),
        "claim_boundary": (
            "The ULE result is an ancilla-stable operator-norm state estimate, "
            "not a diamond bound. It assumes a stationary zero-mean quasifree "
            "bath and system-memory factorization from the bath in the remote "
            "past; the companion finite-switching theorem supplies an explicit "
            "amplitude-ramp and burn-in transient. "
            "The illustrative moment inputs in this certificate audit the "
            "dimension scaling; the companion smooth-worldtube certificate "
            "supplies profile-specific step-converged Sobolev integrals, but not "
            "interval enclosures. The engineered optical profile is not yet "
            "derived from a Skyrmion current."
        ),
        "compact_lamb_shift_coefficient": lamb_coefficient,
        "compact_lamb_tail_bound": lamb_tail,
        "illustrative_jump_l1_input": jump_l1_bound,
        "illustrative_jump_first_moment_input": jump_first_moment_bound,
        "profile_specific_ule_constants_certified": False,
        "certified_claims": certified_claims,
        "records": tuple(records),
        "next_physics_gate": (
            "derive the compact smooth optical profile and its coupling from a "
            "finite matter worldtube action, replace the numerical Sobolev "
            "margin by interval enclosures, derive the prescribed switch from "
            "the matter action, and control direct target-"
            "reference interactions, support stress, lifetime, and gravity"
        ),
    }
