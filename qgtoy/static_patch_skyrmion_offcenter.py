"""Kinematic off-center gate for the matter-derived Skyrmion bath.

A genuine optical-H3 transvection of a centered radial vector source is a
symmetry of the conformal stationary bath.  Re-expanding the translated source
about the old origin mixes its ``l=1`` form into ``l=0`` and ``l=2`` at first
order, but cannot create an auto-Kossakowski polarization splitting.  Any such
splitting must come from intrinsic held-off-center matter or boundary response.
"""

from __future__ import annotations

from math import acosh, cos, cosh, exp, isfinite, sin, sinh, sqrt

from .static_patch_gradient_torque import (
    gradient_zero_frequency_correlations,
)
from .static_patch_skyrmion_bath import (
    skyrmion_current_gradient_spectrum,
)


_MAXIMUM_RESOLVED_PHASE = 1.0e6
_MAXIMUM_SPECTRAL_PARAMETER = 1.0e150


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_unit_interval(name: str, value: float) -> None:
    if not isfinite(value) or value < -1.0 or value > 1.0:
        raise ValueError(f"{name} must lie in [-1,1]")


def translated_l1_first_order_coefficients(
    source_value: float,
    source_radial_derivative: float,
    optical_radius: float,
) -> tuple[float, float]:
    """Return the scalar and quadrupole radial coefficients ``u0,u2``.

    For ``f_j=F(y)n_j`` translated by rapidity ``epsilon`` along ``a``,

    ``delta f_j=-epsilon a_i[u0 delta_ij+u2 Q_ij]``.
    """
    if not isfinite(source_value) or not isfinite(source_radial_derivative):
        raise ValueError("source data must be finite")
    _validate_nonnegative("optical_radius", optical_radius)
    if optical_radius == 0.0:
        if source_value != 0.0:
            raise ValueError("a smooth centered source must vanish at the origin")
        return source_radial_derivative, 0.0
    coth = cosh(optical_radius) / sinh(optical_radius)
    return (
        (source_radial_derivative + 2.0 * coth * source_value) / 3.0,
        source_radial_derivative - coth * source_value,
    )


def axis_translation_first_order_source_change(
    source_value: float,
    source_radial_derivative: float,
    optical_radius: float,
    polar_cosine: float,
) -> tuple[float, float]:
    """Return first-order changes of the ``z`` and meridional ``x`` components."""
    _validate_unit_interval("polar_cosine", polar_cosine)
    u0, u2 = translated_l1_first_order_coefficients(
        source_value,
        source_radial_derivative,
        optical_radius,
    )
    cosine = polar_cosine
    sine = sqrt(max(0.0, 1.0 - cosine * cosine))
    return (
        -(u0 + u2 * (cosine * cosine - 1.0 / 3.0)),
        -u2 * cosine * sine,
    )


def inverse_axis_transvection_coordinates(
    optical_radius: float,
    polar_cosine: float,
    rapidity: float,
) -> tuple[float, float, float]:
    """Return ``y',n'_x,n'_z`` under an inverse transvection along ``z``."""
    _validate_nonnegative("optical_radius", optical_radius)
    _validate_unit_interval("polar_cosine", polar_cosine)
    if not isfinite(rapidity):
        raise ValueError("rapidity must be finite")
    if optical_radius + abs(rapidity) > 700.0:
        raise ValueError("translation lies outside the stable floating domain")
    cosine = polar_cosine
    sine = sqrt(max(0.0, 1.0 - cosine * cosine))
    radial_sinh = sinh(optical_radius)
    lower_weight = (1.0 + cosine) / 2.0
    upper_weight = (1.0 - cosine) / 2.0
    difference = optical_radius - rapidity
    sum_value = optical_radius + rapidity
    time_component = (
        lower_weight * cosh(difference)
        + upper_weight * cosh(sum_value)
    )
    translated_radius = acosh(max(1.0, time_component))
    translated_sinh = sinh(translated_radius)
    x_component = radial_sinh * sine
    z_component = (
        lower_weight * sinh(difference)
        - upper_weight * sinh(sum_value)
    )
    if translated_sinh < 1.0e-15:
        return translated_radius, 0.0, 0.0
    return (
        translated_radius,
        x_component / translated_sinh,
        z_component / translated_sinh,
    )


def _csch_coth(value: float) -> tuple[float, float]:
    if value < 20.0:
        radial_sinh = sinh(value)
        return 1.0 / radial_sinh, cosh(value) / radial_sinh
    decay = exp(-value)
    decay_squared = decay * decay
    denominator = 1.0 - decay_squared
    return 2.0 * decay / denominator, (1.0 + decay_squared) / denominator


def _resolved_phase(spectral_parameter: float, optical_distance: float) -> float:
    if spectral_parameter > _MAXIMUM_SPECTRAL_PARAMETER:
        raise ValueError("spectral_parameter exceeds the floating evaluation domain")
    phase = spectral_parameter * optical_distance
    if not isfinite(phase) or abs(phase) > _MAXIMUM_RESOLVED_PHASE:
        raise ValueError("spectral phase exceeds the floating evaluation domain")
    return phase


def spectral_spherical_function_derivatives(
    spectral_parameter: float,
    center_distance_over_radius: float,
) -> tuple[float, float, float]:
    """Return ``phi_p(y)=sin(py)/(p sinh y)`` and two ``y`` derivatives."""
    _validate_nonnegative("spectral_parameter", spectral_parameter)
    _validate_nonnegative(
        "center_distance_over_radius", center_distance_over_radius
    )
    p = spectral_parameter
    y = center_distance_over_radius
    if p > _MAXIMUM_SPECTRAL_PARAMETER:
        raise ValueError("spectral_parameter exceeds the floating evaluation domain")
    if y == 0.0:
        return 1.0, 0.0, -(1.0 + p * p) / 3.0
    csch, coth = _csch_coth(y)
    if csch == 0.0:
        return 0.0, 0.0, 0.0
    if p == 0.0:
        numerator = y
        numerator_first = 1.0
        numerator_second = 0.0
    else:
        phase = _resolved_phase(p, y)
        numerator = sin(phase) / p
        numerator_first = cos(phase)
        numerator_second = -p * sin(phase)
    value = numerator * csch
    first = csch * (numerator_first - numerator * coth)
    second = csch * (
        numerator_second
        - 2.0 * numerator_first * coth
        + numerator * (1.0 + 2.0 * csch * csch)
    )
    return value, first, second


def gradient_spectral_correlations(
    spectral_parameter: float,
    center_distance_over_radius: float,
) -> tuple[float, float]:
    """Return longitudinal and transverse gradient correlations at any ``p``."""
    _validate_nonnegative("spectral_parameter", spectral_parameter)
    _validate_nonnegative(
        "center_distance_over_radius", center_distance_over_radius
    )
    p = spectral_parameter
    y = center_distance_over_radius
    if y == 0.0:
        return 1.0, 1.0
    if p == 0.0:
        return gradient_zero_frequency_correlations(y)
    csch, _ = _csch_coth(y)
    if csch == 0.0:
        return 0.0, 0.0
    _resolved_phase(p, y)
    if y < 1.0e-3 / (1.0 + p):
        y2 = y * y
        return (
            1.0 - (3.0 * p * p + 7.0) * y2 / 10.0,
            1.0 - (p * p + 4.0) * y2 / 10.0,
        )
    _, first, second = spectral_spherical_function_derivatives(p, y)
    denominator = 1.0 + p * p
    return (
        -3.0 * second / denominator,
        -3.0 * first * csch / denominator,
    )


def skyrmion_two_center_kossakowski_matrix(
    frequency: float,
    center_distance_over_radius: float,
    **parameters: float,
) -> tuple[tuple[float, ...], ...]:
    """Return the six-axis auto/cross block for translated identical sources."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_nonnegative(
        "center_distance_over_radius", center_distance_over_radius
    )
    radius = parameters.get("radius", 1.0)
    _validate_positive("radius", radius)
    spectrum = skyrmion_current_gradient_spectrum(frequency, **parameters)
    longitudinal, transverse = gradient_spectral_correlations(
        radius * abs(frequency),
        center_distance_over_radius,
    )
    correlations = (transverse, transverse, longitudinal)
    rows = []
    for row in range(6):
        values = []
        for column in range(6):
            if row == column:
                value = spectrum
            elif row < 3 and column == row + 3:
                value = spectrum * correlations[row]
            elif row >= 3 and column == row - 3:
                value = spectrum * correlations[column]
            else:
                value = 0.0
            values.append(value)
        rows.append(tuple(values))
    return tuple(rows)


def static_patch_skyrmion_offcenter_certificate(
    *,
    radius: float = 1.0,
    frequency: float = 0.7,
    center_distance_over_radius: float = 0.2,
) -> dict[str, object]:
    """Audit the translation no-go and arbitrary-frequency cross prediction."""
    _validate_positive("radius", radius)
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive(
        "center_distance_over_radius", center_distance_over_radius
    )
    p = radius * abs(frequency)
    longitudinal, transverse = gradient_spectral_correlations(
        p,
        center_distance_over_radius,
    )
    zero_longitudinal, zero_transverse = gradient_spectral_correlations(
        0.0,
        center_distance_over_radius,
    )
    reference_zero = gradient_zero_frequency_correlations(
        center_distance_over_radius
    )
    matrix = skyrmion_two_center_kossakowski_matrix(
        frequency,
        center_distance_over_radius,
        radius=radius,
    )
    sample_radius = 0.4
    sample_cosine = 0.3
    sample_source = sample_radius * exp(-0.7 * sample_radius)
    sample_derivative = exp(-0.7 * sample_radius) * (
        1.0 - 0.7 * sample_radius
    )
    predicted_z, predicted_x = axis_translation_first_order_source_change(
        sample_source,
        sample_derivative,
        sample_radius,
        sample_cosine,
    )
    spacing = 1.0e-6
    translated_y, translated_x, translated_z = (
        inverse_axis_transvection_coordinates(
            sample_radius,
            sample_cosine,
            spacing,
        )
    )
    translated_source = translated_y * exp(-0.7 * translated_y)
    sample_sine = sqrt(1.0 - sample_cosine**2)
    numerical_z = (
        translated_source * translated_z - sample_source * sample_cosine
    ) / spacing
    numerical_x = (
        translated_source * translated_x - sample_source * sample_sine
    ) / spacing
    executable_checks = {
        "arbitrary_frequency_correlations_are_bounded": (
            abs(longitudinal) <= 1.0 and abs(transverse) <= 1.0
        ),
        "zero_frequency_reduces_to_existing_gradient_theorem": max(
            abs(zero_longitudinal - reference_zero[0]),
            abs(zero_transverse - reference_zero[1]),
        )
        < 1.0e-12,
        "first_order_formula_matches_exact_transvection_difference": max(
            abs(predicted_z - numerical_z),
            abs(predicted_x - numerical_x),
        )
        < 1.0e-5,
        "two_center_matrix_constructor_is_symmetric": all(
            matrix[row][column] == matrix[column][row]
            for row in range(6)
            for column in range(6)
        ),
    }
    return {
        "goal": "Off-Center Skyrmion Translation And Deformation Gate",
        "status": "pass" if all(executable_checks.values()) else "fail",
        "result_type": "analytic_translation_no_go_with_executable_kinematic_checks",
        "central_result": (
            "A pure optical-H3 translation of the matter-derived source leaves "
            "its auto Kossakowski tensor exactly isotropic. The old-origin "
            "harmonic expansion mixes l=1 only into l=0 plus l=2 at first "
            "order. Therefore any auto polarization splitting diagnoses "
            "intrinsic held-off-center matter or boundary deformation."
        ),
        "spectral_parameter": p,
        "center_distance_over_radius": center_distance_over_radius,
        "longitudinal_cross_correlation": longitudinal,
        "transverse_cross_correlation": transverse,
        "small_distance_longitudinal_defect_coefficient": (
            3.0 * p * p + 7.0
        )
        / 10.0,
        "small_distance_transverse_defect_coefficient": (p * p + 4.0) / 10.0,
        "executable_checks": executable_checks,
        "analytic_theorem_results": (
            "bath homogeneity makes pure H3 translation incapable of generating auto polarization splitting at any order",
            "first-order central harmonics contain l=0 and l=2 but no l=1",
            "the matter form factor cancels from normalized two-center correlations away from its zeros",
        ),
        "claim_boundary": (
            "The translation theorem uses Killing-time optical sources and "
            "parallel-transported center frames. A held off-center Skyrmion is "
            "not an optical translate because the mass, lapse, membrane, and "
            "anchor break transvection symmetry. Its intrinsic l=1 boundary-"
            "value problem and quadratic auto splitting remain to be solved. "
            "The any-order isotropy statement is analytic; the executable "
            "checks only coordinate, derivative, and matrix formulas on its "
            "declared resolved-phase floating domain."
        ),
        "next_physics_gate": (
            "solve the coupled l=1 Skyrmion-membrane-anchor response and extract "
            "the quadratic longitudinal/transverse auto splitting"
        ),
    }
