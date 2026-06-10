"""Signed jump-correlator factor for the centered Skyrmion bath.

Nathan--Rudner factor the scalar bath spectrum through ``J=2 pi g^2`` and
then use the exact time-domain self-convolution ``J=g*g``.  Positivity selects
one convenient real square root, but the scalar algebra also permits a real
sign choice.  For ``j_Sky=j_0 H_Sky^2``, choosing

``q_signed(omega)=sqrt(j_0(omega)) H_Sky(R |omega|)``

removes the absolute-value cusps of the principal factor while preserving the
same spectrum and the Hermitian symmetry of the jump correlator.  This module
computes finite-window Sobolev inputs.  It does not extrapolate the finite
profile quadrature to infinite frequency.
"""

from __future__ import annotations

from functools import lru_cache
from math import atanh, cos, exp, isfinite, log, pi, sin, sqrt, tanh

from .massive_skyrmion_profile import dimensionless_inertia_density
from .static_patch_skyrmion_bath import (
    _centered_profile,
    skyrmion_current_bath_record,
    skyrmion_current_gradient_spectrum,
)
from .static_patch_smooth_worldtube_ule import bare_sqrt_spectrum_derivatives
from .static_patch_worldtube_ule import (
    optimal_sobolev_jump_correlator_moment_bounds,
)
from .static_patch_overlapping_ule import (
    smeared_gradient_zero_frequency_spectrum,
)
from .static_patch_finite_switching_ule import (
    finite_switch_logarithmic_heat_ule_coupling_cap,
    required_effective_age_for_bounded_heat_coefficient,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def _sinc_derivatives(value: float) -> tuple[float, float, float]:
    """Return sinc and its first two derivatives with a stable origin series."""
    if abs(value) < 1.0e-3:
        squared = value * value
        sinc = (
            1.0
            - squared / 6.0
            + squared**2 / 120.0
            - squared**3 / 5_040.0
            + squared**4 / 362_880.0
        )
        first = (
            -value / 3.0
            + value**3 / 30.0
            - value**5 / 840.0
            + value**7 / 45_360.0
        )
        second = (
            -1.0 / 3.0
            + squared / 10.0
            - squared**2 / 168.0
            + squared**3 / 6_480.0
        )
        return sinc, first, second
    sinc = sin(value) / value
    first = (value * cos(value) - sin(value)) / value**2
    second = (
        (2.0 - value**2) * sin(value) - 2.0 * value * cos(value)
    ) / value**3
    return sinc, first, second


def _y_coth_minus_one(value: float) -> float:
    if value < 1.0e-3:
        squared = value * value
        return squared / 3.0 - squared**2 / 45.0 + 2.0 * squared**3 / 945.0
    return value / tanh(value) - 1.0


def _sinc_minus_cos(value: float) -> float:
    if abs(value) < 1.0e-3:
        squared = value * value
        return squared / 3.0 - squared**2 / 30.0 + squared**3 / 840.0
    return sin(value) / value - cos(value)


def optical_dipole_kernel_derivatives(
    spectral_parameter: float,
    optical_radius_ratio: float,
) -> tuple[float, float, float]:
    """Return the optical dipole kernel and two ``p`` derivatives."""
    if not isfinite(spectral_parameter):
        raise ValueError("spectral_parameter must be finite")
    _validate_nonnegative("optical_radius_ratio", optical_radius_ratio)
    y = optical_radius_ratio
    phase = spectral_parameter * y
    sinc, sinc_first, sinc_second = _sinc_derivatives(phase)
    y_coth_correction = _y_coth_minus_one(y)
    y_coth_y = 1.0 + y_coth_correction
    return (
        y_coth_correction * sinc + _sinc_minus_cos(phase),
        y * (y_coth_y * sinc_first + sin(phase)),
        y**2 * (y_coth_y * sinc_second + cos(phase)),
    )


@lru_cache(maxsize=16)
def _form_factor_quadrature(
    pion_mass: float,
    curvature: float,
    wall_radius: float,
    step: float,
) -> tuple[float, tuple[tuple[float, float, float], ...]]:
    points = _centered_profile(pion_mass, curvature, wall_radius, step)
    count = len(points)
    trapezoid_weights = []
    for index, (radius_value, _, _) in enumerate(points):
        if index == 0:
            weight = 0.5 * (points[1][0] - radius_value)
        elif index == count - 1:
            weight = 0.5 * (radius_value - points[index - 1][0])
        else:
            weight = 0.5 * (points[index + 1][0] - points[index - 1][0])
        trapezoid_weights.append(weight)
    densities = tuple(
        dimensionless_inertia_density(
            radius_value,
            profile,
            derivative,
            curvature=curvature,
        )
        for radius_value, profile, derivative in points
    )
    inertia = sum(
        weight * density
        for weight, density in zip(trapezoid_weights, densities)
    )
    root_curvature = sqrt(curvature)
    rows = []
    for weight, density, (radius_value, _, _) in zip(
        trapezoid_weights,
        densities,
        points,
    ):
        z = root_curvature * radius_value
        if z >= 1.0:
            raise ValueError("profile support must lie strictly inside the horizon")
        y = atanh(z)
        rows.append((weight * density / radius_value**2, y, z))
    return 3.0 / (curvature * inertia), tuple(rows)


def skyrmion_current_optical_form_factor_derivatives(
    spectral_parameter: float,
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> tuple[float, float, float]:
    """Return ``H_Sky(p)`` and its first two derivatives for ``p>=0``."""
    _validate_nonnegative("spectral_parameter", spectral_parameter)
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("step", step)
    prefactor, rows = _form_factor_quadrature(
        pion_mass,
        curvature,
        wall_radius,
        step,
    )
    numerator = 0.0
    numerator_first = 0.0
    numerator_second = 0.0
    for weight, y, _ in rows:
        kernel, kernel_first, kernel_second = optical_dipole_kernel_derivatives(
            spectral_parameter,
            y,
        )
        numerator += weight * kernel
        numerator_first += weight * kernel_first
        numerator_second += weight * kernel_second
    p = spectral_parameter
    denominator = 1.0 + p * p
    return (
        prefactor * numerator / denominator,
        prefactor
        * (
            numerator_first / denominator
            - 2.0 * p * numerator / denominator**2
        ),
        prefactor
        * (
            numerator_second / denominator
            - 4.0 * p * numerator_first / denominator**2
            + (6.0 * p * p - 2.0) * numerator / denominator**3
        ),
    )


def skyrmion_signed_sqrt_spectrum_derivatives(
    frequency: float,
    *,
    radius: float = 1.0,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> tuple[float, float, float]:
    """Return the smooth signed factor ``sqrt(j_0) H_Sky`` and derivatives."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    p = radius * abs(frequency)
    form, form_first, form_second = (
        skyrmion_current_optical_form_factor_derivatives(
            p,
            pion_mass=pion_mass,
            curvature=curvature,
            wall_radius=wall_radius,
            step=step,
        )
    )
    if frequency < 0.0:
        form_frequency_first = -radius * form_first
    elif frequency > 0.0:
        form_frequency_first = radius * form_first
    else:
        form_frequency_first = 0.0
    form_frequency_second = radius**2 * form_second
    root, root_first, root_second = bare_sqrt_spectrum_derivatives(
        frequency,
        radius=radius,
    )
    return (
        root * form,
        root_first * form + root * form_frequency_first,
        root_second * form
        + 2.0 * root_first * form_frequency_first
        + root * form_frequency_second,
    )


def centered_skyrmion_spectral_matrix(
    frequency: float,
    **parameters: float,
) -> tuple[tuple[float, float, float], ...]:
    """Return ``delta_ab j_Sky`` for the centered isotropic ``l=1`` block."""
    spectrum = skyrmion_current_gradient_spectrum(frequency, **parameters)
    return (
        (spectrum, 0.0, 0.0),
        (0.0, spectrum, 0.0),
        (0.0, 0.0, spectrum),
    )


def centered_skyrmion_signed_factor_matrix(
    frequency: float,
    **parameters: float,
) -> tuple[tuple[float, float, float], ...]:
    """Return the diagonal real signed root of the centered spectral matrix."""
    factor = skyrmion_signed_sqrt_spectrum_derivatives(
        frequency,
        **parameters,
    )[0]
    return (
        (factor, 0.0, 0.0),
        (0.0, factor, 0.0),
        (0.0, 0.0, factor),
    )


def skyrmion_signed_sobolev_norms(
    *,
    radius: float = 1.0,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
    frequency_window: float = 400.0,
    frequency_steps: int = 3_200,
) -> tuple[float, float, float]:
    """Return truncated ``L2`` norms of the signed factor and two derivatives."""
    _validate_positive("radius", radius)
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("step", step)
    _validate_positive("frequency_window", frequency_window)
    _validate_positive_integer("frequency_steps", frequency_steps)
    if frequency_steps % 2:
        raise ValueError("frequency_steps must be even")
    horizon_margin = 1.0 - curvature * wall_radius**2
    if horizon_margin <= 0.0:
        raise ValueError("wall must lie strictly inside the horizon")
    maximum_optical_spacing = sqrt(curvature) * step / horizon_margin
    if radius * frequency_window * maximum_optical_spacing > 0.25:
        raise ValueError(
            "frequency window is not resolved by the radial profile spacing"
        )
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
        form, form_first, form_second = (
            skyrmion_current_optical_form_factor_derivatives(
                radius * frequency,
                pion_mass=pion_mass,
                curvature=curvature,
                wall_radius=wall_radius,
                step=step,
            )
        )
        form_frequency_first = radius * form_first
        form_frequency_second = radius**2 * form_second
        positive_root = bare_sqrt_spectrum_derivatives(
            frequency,
            radius=radius,
        )
        negative_root = bare_sqrt_spectrum_derivatives(
            -frequency,
            radius=radius,
        )

        def combine(
            root_data: tuple[float, float, float],
            signed_form_first: float,
        ) -> tuple[float, float, float]:
            root, root_first, root_second = root_data
            return (
                root * form,
                root_first * form + root * signed_form_first,
                root_second * form
                + 2.0 * root_first * signed_form_first
                + root * form_frequency_second,
            )

        positive = combine(positive_root, form_frequency_first)
        negative = combine(negative_root, -form_frequency_first)
        for order in range(3):
            totals[order] += weight * (
                positive[order] ** 2 + negative[order] ** 2
            )
    return tuple(sqrt(spacing * total / 3.0) for total in totals)


def skyrmion_signed_moment_record(
    *,
    radius: float = 1.0,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
    frequency_window: float = 400.0,
    frequency_steps: int = 3_200,
) -> dict[str, float]:
    """Return signed-factor Sobolev norms and optimized time-moment bounds."""
    norms = skyrmion_signed_sobolev_norms(
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        frequency_window=frequency_window,
        frequency_steps=frequency_steps,
    )
    jump_l1, jump_first = optimal_sobolev_jump_correlator_moment_bounds(
        *norms
    )
    return {
        "signed_sqrt_spectrum_l2": norms[0],
        "signed_sqrt_spectrum_first_derivative_l2": norms[1],
        "signed_sqrt_spectrum_second_derivative_l2": norms[2],
        "jump_l1_sobolev_estimate": jump_l1,
        "jump_first_moment_sobolev_estimate": jump_first,
        "frequency_window": frequency_window,
        "frequency_steps": float(frequency_steps),
        "profile_step": step,
    }


def _matter_logarithmic_heat_coupling_cap(
    maximum_spin: int,
    radius: float,
    zero_mode_form_factor: float,
    residual_budget: float,
    jump_l1_bound: float,
    jump_first_moment_bound: float,
) -> float:
    dimension = 2 * maximum_spin + 1
    lapse = 1.0 / dimension
    zero_spectrum = (
        smeared_gradient_zero_frequency_spectrum(radius=radius)
        * zero_mode_form_factor**2
    )
    coefficient = (
        288.0
        * maximum_spin**2
        * jump_l1_bound
        * jump_first_moment_bound
        + 20_736.0
        / (pi * zero_spectrum)
        * maximum_spin**4
        * jump_l1_bound**3
        * jump_first_moment_bound
        * log(float(dimension))
    )
    return lapse * sqrt(residual_budget / coefficient)


def static_patch_skyrmion_signed_ule_certificate(
    *,
    maximum_spin: int = 4096,
    radius: float = 1.0,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, object]:
    """Audit the signed-factor escape from the principal-root cusp."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    _validate_positive("radius", radius)
    matter_record = skyrmion_current_bath_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    coarse = skyrmion_signed_moment_record(
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=2.0 * step,
        frequency_window=200.0 / radius,
        frequency_steps=1_600,
    )
    refined = skyrmion_signed_moment_record(
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        frequency_window=200.0 / radius,
        frequency_steps=1_600,
    )
    mesh_refined = skyrmion_signed_moment_record(
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        frequency_window=200.0 / radius,
        frequency_steps=3_200,
    )
    coarse_wide = skyrmion_signed_moment_record(
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=2.0 * step,
        frequency_window=400.0 / radius,
        frequency_steps=3_200,
    )
    wide = skyrmion_signed_moment_record(
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        frequency_window=400.0 / radius,
        frequency_steps=3_200,
    )
    norm_keys = (
        "signed_sqrt_spectrum_l2",
        "signed_sqrt_spectrum_first_derivative_l2",
        "signed_sqrt_spectrum_second_derivative_l2",
    )
    radial_changes = tuple(
        abs(refined[key] / coarse[key] - 1.0) for key in norm_keys
    )
    mesh_changes = tuple(
        abs(mesh_refined[key] / refined[key] - 1.0) for key in norm_keys
    )
    window_changes = tuple(
        abs(wide[key] / refined[key] - 1.0) for key in norm_keys
    )
    wide_radial_changes = tuple(
        abs(wide[key] / coarse_wide[key] - 1.0) for key in norm_keys
    )
    numerical_margin = 1.0 + 10.0 * max(
        max(radial_changes),
        max(mesh_changes),
        max(window_changes),
        max(wide_radial_changes),
        1.0e-6,
    )
    jump_l1_input = wide["jump_l1_sobolev_estimate"] * numerical_margin
    jump_first_input = (
        wide["jump_first_moment_sobolev_estimate"] * numerical_margin
    )
    dimension = 2 * maximum_spin + 1
    constant_cap = _matter_logarithmic_heat_coupling_cap(
        maximum_spin,
        radius,
        matter_record["zero_mode_form_factor"],
        1.0 / (4.0 * dimension),
        jump_l1_input,
        jump_first_input,
    )
    heat_cap = _matter_logarithmic_heat_coupling_cap(
        maximum_spin,
        radius,
        matter_record["zero_mode_form_factor"],
        1.0 / (4.0 * dimension**2),
        jump_l1_input,
        jump_first_input,
    )
    matter_zero_spectrum = (
        smeared_gradient_zero_frequency_spectrum(radius=radius)
        * matter_record["zero_mode_form_factor"] ** 2
    )
    finite_switch_beta = 10.0
    finite_switch_constant_cap = (
        finite_switch_logarithmic_heat_ule_coupling_cap(
            maximum_spin,
            1.0 / dimension,
            1.0 / (4.0 * dimension),
            jump_l1_input,
            jump_first_input,
            burnin_rate_multiples=finite_switch_beta,
            radius=radius,
            zero_frequency_spectrum=matter_zero_spectrum,
        )
    )
    finite_switch_heat_cap = finite_switch_logarithmic_heat_ule_coupling_cap(
        maximum_spin,
        1.0 / dimension,
        1.0 / (4.0 * dimension**2),
        jump_l1_input,
        jump_first_input,
        burnin_rate_multiples=finite_switch_beta,
        radius=radius,
        zero_frequency_spectrum=matter_zero_spectrum,
    )
    finite_switch_constant_required_age = (
        required_effective_age_for_bounded_heat_coefficient(
            maximum_spin,
            1.0 / dimension,
            finite_switch_constant_cap,
            jump_l1_input,
            burnin_rate_multiples=finite_switch_beta,
        )
    )
    finite_switch_heat_required_age = (
        required_effective_age_for_bounded_heat_coefficient(
            maximum_spin,
            1.0 / dimension,
            finite_switch_heat_cap,
            jump_l1_input,
            burnin_rate_multiples=finite_switch_beta,
        )
    )
    first_zero = matter_record["first_form_factor_zero"] / radius
    root_spacing = 1.0e-3 / radius
    def signed_derivative(offset: float) -> float:
        return skyrmion_signed_sqrt_spectrum_derivatives(
            first_zero + offset,
            radius=radius,
            pion_mass=pion_mass,
            curvature=curvature,
            wall_radius=wall_radius,
            step=step,
        )[1]

    signed_center = signed_derivative(0.0)
    signed_left = signed_derivative(-root_spacing)
    signed_right = signed_derivative(root_spacing)
    far_spacing = 10.0 * root_spacing
    signed_far_left = signed_derivative(-far_spacing)
    signed_far_right = signed_derivative(far_spacing)
    samples = (-0.7 / radius, 0.0, 0.7 / radius, first_zero + root_spacing)
    reference_spectrum = skyrmion_current_gradient_spectrum(
        0.0,
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    factorization_scaled_errors = []
    for frequency in samples:
        factor = skyrmion_signed_sqrt_spectrum_derivatives(
                frequency,
                radius=radius,
                pion_mass=pion_mass,
                curvature=curvature,
                wall_radius=wall_radius,
                step=step,
            )[0]
        spectrum = skyrmion_current_gradient_spectrum(
            frequency,
            radius=radius,
            pion_mass=pion_mass,
            curvature=curvature,
            wall_radius=wall_radius,
            step=step,
        )
        factorization_scaled_errors.append(
            abs(factor * factor - spectrum)
            / max(abs(spectrum), 1.0e-12 * reference_spectrum)
        )
    signed_derivative_near_change = max(
        abs(signed_left - signed_center),
        abs(signed_right - signed_center),
    ) / max(
        abs(signed_center),
        1.0e-300,
    )
    signed_derivative_far_change = max(
        abs(signed_far_left - signed_center),
        abs(signed_far_right - signed_center),
    ) / max(abs(signed_center), 1.0e-300)
    derivative_change_contraction = (
        signed_derivative_near_change / signed_derivative_far_change
        if signed_derivative_far_change > 0.0
        else 0.0
    )
    factor_matrix = centered_skyrmion_signed_factor_matrix(
        0.7 / radius,
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    spectrum_matrix = centered_skyrmion_spectral_matrix(
        0.7 / radius,
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    matrix_factorization_error = max(
        abs(
            sum(
                factor_matrix[row][inner] * factor_matrix[inner][column]
                for inner in range(3)
            )
            - spectrum_matrix[row][column]
        )
        for row in range(3)
        for column in range(3)
    )
    half_kms_positive = skyrmion_signed_sqrt_spectrum_derivatives(
        0.7 / radius,
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )[0]
    half_kms_negative = skyrmion_signed_sqrt_spectrum_derivatives(
        -0.7 / radius,
        radius=radius,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )[0]
    claims = {
        "signed_factor_squares_to_the_matter_spectrum": max(
            factorization_scaled_errors
        )
        < 1.0e-10,
        "centered_three_axis_factor_is_diagonal_and_squares_to_spectrum": (
            matrix_factorization_error < 1.0e-14 / radius**3
        ),
        "signed_factor_obeys_half_kms_balance": abs(
            half_kms_negative / half_kms_positive - exp(-0.7 * pi)
        )
        < 1.0e-13,
        "signed_factor_derivative_is_locally_continuous_at_first_zero": (
            signed_derivative_near_change < 1.0e-2
            and derivative_change_contraction < 0.2
        ),
        "principal_absolute_factor_has_a_nonzero_derivative_jump": (
            matter_record["form_factor_absolute_value_derivative_jump"]
            > 1.0e-10
        ),
        "signed_factor_has_stable_finite_window_h2_data": all(
            isfinite(wide[key]) and wide[key] > 0.0 for key in norm_keys
        ),
        "profile_mesh_and_window_refinement_are_stable": (
            max(radial_changes) < 2.0e-4
            and max(mesh_changes) < 2.0e-6
            and max(window_changes) < 2.0e-6
            and max(wide_radial_changes) < 2.0e-4
        ),
        "matter_adjusted_candidate_caps_are_positive": (
            constant_cap > 0.0 and heat_cap > 0.0
        ),
    }
    return {
        "goal": "Signed Skyrmion Jump-Correlator ULE Recovery Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "signed_scalar_factor_lemma_and_finite_window_ule_gate",
        "central_result": (
            "The principal nonnegative square root is not the only real scalar "
            "factor compatible with the Nathan-Rudner self-convolution. Taking "
            "q=sqrt(j0) H_Sky preserves q^2=j_Sky and Hermitian time symmetry "
            "and removes the zero cusps. Stable finite-window H2 data support "
            "the route. A separate exact-profile theorem proves global H2 "
            "membership, and AU.3a supplies conservative certified global "
            "norm constants. Sharp profile-specific constants remain open."
        ),
        "factor_gauge_lemma": (
            "For a scalar spectrum J and any real signed factor q with q^2=J, "
            "the inverse Fourier transform obeys g(t)=g*(-t) and the exact "
            "self-convolution used in the ULE derivation is unchanged. General "
            "complex phases are not allowed by this q^2 factorization."
        ),
        "matter_record": matter_record,
        "coarse_moment_record": coarse,
        "refined_moment_record": refined,
        "mesh_refined_moment_record": mesh_refined,
        "coarse_wide_moment_record": coarse_wide,
        "wide_moment_record": wide,
        "relative_profile_step_changes": radial_changes,
        "relative_frequency_mesh_changes": mesh_changes,
        "relative_frequency_window_changes": window_changes,
        "relative_wide_window_profile_step_changes": wide_radial_changes,
        "maximum_scaled_factorization_error": max(
            factorization_scaled_errors
        ),
        "first_zero_signed_derivative_near_relative_change": (
            signed_derivative_near_change
        ),
        "first_zero_signed_derivative_change_contraction": (
            derivative_change_contraction
        ),
        "numerical_safety_margin": numerical_margin,
        "candidate_constant_obstruction_coupling_cap": constant_cap,
        "candidate_heat_matching_coupling_cap": heat_cap,
        "candidate_finite_switch_constant_obstruction_coupling_cap": (
            finite_switch_constant_cap
        ),
        "candidate_finite_switch_heat_matching_coupling_cap": (
            finite_switch_heat_cap
        ),
        "finite_switch_bound_level_beta": finite_switch_beta,
        "finite_switch_constant_required_bound_level_effective_age": (
            finite_switch_constant_required_age
        ),
        "finite_switch_heat_required_bound_level_effective_age": (
            finite_switch_heat_required_age
        ),
        "finite_switch_condition_status": (
            "conditional candidate caps: the executable reports beta/Gamma_bar "
            "but does not assert a physical preparation with that age"
        ),
        "finite_switch_to_stationary_candidate_cap_ratio": (
            finite_switch_heat_cap / heat_cap
        ),
        "audit_checks": claims,
        "claim_boundary": (
            "The scalar signed-factor lemma follows by substitution into the "
            "Nathan-Rudner convolution proof; it is not a claim of arbitrary "
            "complex phase freedom or a multi-channel matrix theorem. The "
            "profile-specific finite-window H2 values and coupling caps are "
            "step- and window-converged floating-point candidates, not global "
            "norms or interval enclosures. The finite trapezoid form factor is "
            "never extrapolated to infinite frequency. The separate continuum "
            "tail theorem proves global H2 membership and interval-certifies "
            "its six derivative-norm inputs. AU.3a supplies conservative "
            "global moment bounds, but does not certify these much tighter "
            "floating candidates. Collective-current compression remains a conditional "
            "matter-model input. For the "
            "declared h(J^2) sector, all collective charges are zero-Bohr and "
            "the zero-Bohr Lamb shift is proportional to J^2, hence dynamically "
            "scalar on a fixed irrep. The finite-switch caps additionally "
            "require the displayed bound-level effective preparation ages."
        ),
        "candidate_prediction": (
            "A physically derived compact hard-wall current may satisfy the "
            "ULE time-moment gate without replacing its oscillatory form "
            "factor by an engineered nonnegative regulator: the signed scalar "
            "factor removes the zero obstruction, and the exact continuum "
            "endpoint theorem proves global H2 membership."
        ),
        "next_physics_gate": (
            "replace the conservative AU.3a finite-band envelope by sharp "
            "profile-resolving interval quadrature, derive the prescribed "
            "switch from the action, and solve off-center current deformation"
        ),
    }
