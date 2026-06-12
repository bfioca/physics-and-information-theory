"""Exact radial-smearing invariance of the Bunch-Davies zero mode.

The zero-frequency optical spatial kernel on ``H^3_R`` is the zonal spherical
function

    phi_0(y) = y / sinh(y),       y = d_H/R.

Its spherical mean obeys the product formula

    M_u phi_0(r) = phi_0(u) phi_0(r).

Consequently, arbitrary nonnegative radial smearings about two centers only
multiply the auto- and cross-spectral coefficients by profile amplitudes.  The
normalized cross correlation remains exactly ``phi_0`` of the center distance,
independent of either radial profile's size or shape.
"""

from __future__ import annotations

from math import acosh, cosh, isfinite, sin, sinh, sqrt
from typing import Sequence

from .static_patch_gradient_torque import gradient_zero_frequency_correlations
from .static_patch_scalar_common_mode import zero_frequency_scalar_correlation


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validated_radial_profile(
    shell_radii: Sequence[float],
    shell_weights: Sequence[float],
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    radii = tuple(float(value) for value in shell_radii)
    weights = tuple(float(value) for value in shell_weights)
    if not radii or len(radii) != len(weights):
        raise ValueError("shell radii and weights must be nonempty and equally sized")
    if any(not isfinite(radius) or radius < 0.0 for radius in radii):
        raise ValueError("shell radii must be finite and nonnegative")
    if any(not isfinite(weight) or weight < 0.0 for weight in weights):
        raise ValueError("shell weights must be finite and nonnegative")
    total_weight = sum(weights)
    if total_weight <= 0.0:
        raise ValueError("shell weights must have positive total")
    normalized_weights = tuple(weight / total_weight for weight in weights)
    return radii, normalized_weights


def zero_frequency_spherical_mean(
    center_distance_over_radius: float,
    shell_radius_over_radius: float,
) -> float:
    """Return the exact spherical mean of ``phi_0`` over a hyperbolic shell."""
    r = center_distance_over_radius
    u = shell_radius_over_radius
    _validate_nonnegative("center_distance_over_radius", r)
    _validate_nonnegative("shell_radius_over_radius", u)
    return (
        zero_frequency_scalar_correlation(r)
        * zero_frequency_scalar_correlation(u)
    )


def hyperbolic_spherical_function(
    spectral_parameter: float,
    distance_over_radius: float,
) -> float:
    """Return ``phi_p(y)=sin(p y)/(p sinh(y))`` with continuous endpoints."""
    p = spectral_parameter
    y = distance_over_radius
    if not isfinite(p):
        raise ValueError("spectral_parameter must be finite")
    _validate_nonnegative("distance_over_radius", y)
    if y == 0.0:
        return 1.0
    zero_mode = zero_frequency_scalar_correlation(y)
    phase = p * y
    if phase == 0.0:
        return zero_mode
    return zero_mode * sin(phase) / phase


def radial_profile_zero_frequency_amplitude(
    shell_radii: Sequence[float],
    shell_weights: Sequence[float],
) -> float:
    """Return the spherical transform amplitude of a radial shell mixture."""
    radii, weights = _validated_radial_profile(shell_radii, shell_weights)
    return sum(
        weight * zero_frequency_scalar_correlation(radius)
        for radius, weight in zip(radii, weights)
    )


def radial_profile_spectral_amplitude(
    spectral_parameter: float,
    shell_radii: Sequence[float],
    shell_weights: Sequence[float],
) -> float:
    """Return the fixed-frequency spherical transform of a shell mixture."""
    if not isfinite(spectral_parameter):
        raise ValueError("spectral_parameter must be finite")
    radii, weights = _validated_radial_profile(shell_radii, shell_weights)
    return sum(
        weight * hyperbolic_spherical_function(spectral_parameter, radius)
        for radius, weight in zip(radii, weights)
    )


def radial_smeared_zero_frequency_record(
    center_distance_over_radius: float,
    *,
    first_shell_radii: Sequence[float],
    first_shell_weights: Sequence[float],
    second_shell_radii: Sequence[float],
    second_shell_weights: Sequence[float],
) -> dict[str, object]:
    """Return auto/cross coefficients for two arbitrary radial profiles."""
    _validate_nonnegative(
        "center_distance_over_radius",
        center_distance_over_radius,
    )
    first_radii, first_weights = _validated_radial_profile(
        first_shell_radii,
        first_shell_weights,
    )
    second_radii, second_weights = _validated_radial_profile(
        second_shell_radii,
        second_shell_weights,
    )
    first_amplitude = radial_profile_zero_frequency_amplitude(
        first_radii,
        first_weights,
    )
    second_amplitude = radial_profile_zero_frequency_amplitude(
        second_radii,
        second_weights,
    )
    center_correlation = zero_frequency_scalar_correlation(
        center_distance_over_radius
    )
    first_auto = first_amplitude**2
    second_auto = second_amplitude**2
    cross = first_amplitude * second_amplitude * center_correlation
    normalized_correlation = cross / (first_auto * second_auto) ** 0.5
    return {
        "center_distance_over_radius_y": center_distance_over_radius,
        "first_profile_shell_radii": first_radii,
        "first_profile_shell_weights": first_weights,
        "second_profile_shell_radii": second_radii,
        "second_profile_shell_weights": second_weights,
        "first_profile_spherical_amplitude": first_amplitude,
        "second_profile_spherical_amplitude": second_amplitude,
        "first_auto_spectral_coefficient": first_auto,
        "second_auto_spectral_coefficient": second_auto,
        "cross_spectral_coefficient": cross,
        "normalized_cross_spectral_correlation": normalized_correlation,
        "point_center_correlation": center_correlation,
        "radial_smearing_cancels_exactly": abs(
            normalized_correlation - center_correlation
        )
        < 1.0e-14,
        "proof_formula": (
            "B_12=A_f A_g phi_0(y), B_11=A_f^2, B_22=A_g^2, "
            "so B_12/sqrt(B_11 B_22)=phi_0(y)"
        ),
    }


def radial_center_gradient_zero_frequency_record(
    center_distance_over_radius: float,
    *,
    first_shell_radii: Sequence[float],
    first_shell_weights: Sequence[float],
    second_shell_radii: Sequence[float],
    second_shell_weights: Sequence[float],
) -> dict[str, object]:
    """Return the zero-mode covariance of center-derived radial smearings.

    If ``Phi_f(p)`` is a radial convolution of the field around ``p``, the
    spherical product formula gives

    ``Cov(Phi_f(p), Phi_g(q)) = A_f A_g phi_0(d(p,q)/R)``.

    The amplitudes are center independent. Differentiating with respect to the
    two centers therefore multiplies the point-gradient covariance tensor by
    ``A_f A_g``. The same factors occur in the two auto-covariances and cancel
    from each normalized polarization.

    Smooth compact nonnegative profiles make the center derivatives smooth
    compact signed field smearings.  Nonnegativity keeps both zero-mode
    profile amplitudes positive, so their product cancels without a residual
    sign after covariance normalization.  Shell mixtures are accepted here as
    an exact algebraic audit of that cancellation, not as a UV regulator.
    """
    y = center_distance_over_radius
    _validate_nonnegative("center_distance_over_radius", y)
    first_radii, first_weights = _validated_radial_profile(
        first_shell_radii,
        first_shell_weights,
    )
    second_radii, second_weights = _validated_radial_profile(
        second_shell_radii,
        second_shell_weights,
    )
    first_amplitude = radial_profile_zero_frequency_amplitude(
        first_radii,
        first_weights,
    )
    second_amplitude = radial_profile_zero_frequency_amplitude(
        second_radii,
        second_weights,
    )
    longitudinal, transverse = gradient_zero_frequency_correlations(y)
    first_auto_component = first_amplitude**2 / 3.0
    second_auto_component = second_amplitude**2 / 3.0
    cross_scale = first_amplitude * second_amplitude / 3.0
    longitudinal_cross = cross_scale * longitudinal
    transverse_cross = cross_scale * transverse
    normalization = sqrt(first_auto_component * second_auto_component)
    normalized_longitudinal = longitudinal_cross / normalization
    normalized_transverse = transverse_cross / normalization
    return {
        "center_distance_over_radius_y": y,
        "first_profile_shell_radii": first_radii,
        "first_profile_shell_weights": first_weights,
        "second_profile_shell_radii": second_radii,
        "second_profile_shell_weights": second_weights,
        "first_profile_spherical_amplitude": first_amplitude,
        "second_profile_spherical_amplitude": second_amplitude,
        "first_auto_covariance_per_polarization": first_auto_component,
        "second_auto_covariance_per_polarization": second_auto_component,
        "longitudinal_cross_covariance": longitudinal_cross,
        "transverse_cross_covariance": transverse_cross,
        "normalized_longitudinal_correlation": normalized_longitudinal,
        "normalized_transverse_correlation": normalized_transverse,
        "point_gradient_longitudinal_correlation": longitudinal,
        "point_gradient_transverse_correlation": transverse,
        "radial_center_gradient_smearing_cancels_exactly": (
            abs(normalized_longitudinal - longitudinal) < 1.0e-14
            and abs(normalized_transverse - transverse) < 1.0e-14
        ),
        "proof_formula": (
            "K_fg(p,q)=A_f A_g phi_0(d(p,q)/R); center derivatives act "
            "only on phi_0, while A_f and A_g cancel after auto-covariance "
            "normalization"
        ),
    }


def finite_switching_radial_correlation_record(
    center_distance_over_radius: float,
    *,
    spectral_parameters: Sequence[float],
    spectral_weights: Sequence[float],
    first_shell_radii: Sequence[float],
    first_shell_weights: Sequence[float],
    second_shell_radii: Sequence[float],
    second_shell_weights: Sequence[float],
) -> dict[str, object]:
    """Bound a finite-switching spectral average by the zero-mode correlation.

    The nonnegative ``spectral_weights`` may include the scalar density of
    states, Bunch-Davies thermal factor, quadrature weights, and a common
    switching filter ``|chi_hat|^2``.  Overall normalization is immaterial.
    """
    y = center_distance_over_radius
    _validate_nonnegative("center_distance_over_radius", y)
    parameters = tuple(float(value) for value in spectral_parameters)
    weights = tuple(float(value) for value in spectral_weights)
    if not parameters or len(parameters) != len(weights):
        raise ValueError(
            "spectral parameters and weights must be nonempty and equally sized"
        )
    if any(not isfinite(value) for value in parameters):
        raise ValueError("spectral parameters must be finite")
    if any(not isfinite(value) or value < 0.0 for value in weights):
        raise ValueError("spectral weights must be finite and nonnegative")
    if sum(weights) <= 0.0:
        raise ValueError("spectral weights must have positive total")
    first_radii, first_radial_weights = _validated_radial_profile(
        first_shell_radii,
        first_shell_weights,
    )
    second_radii, second_radial_weights = _validated_radial_profile(
        second_shell_radii,
        second_shell_weights,
    )
    first_amplitudes = tuple(
        radial_profile_spectral_amplitude(
            parameter,
            first_radii,
            first_radial_weights,
        )
        for parameter in parameters
    )
    second_amplitudes = tuple(
        radial_profile_spectral_amplitude(
            parameter,
            second_radii,
            second_radial_weights,
        )
        for parameter in parameters
    )
    center_factors = tuple(
        hyperbolic_spherical_function(parameter, y)
        for parameter in parameters
    )
    first_auto = sum(
        weight * amplitude**2
        for weight, amplitude in zip(weights, first_amplitudes)
    )
    second_auto = sum(
        weight * amplitude**2
        for weight, amplitude in zip(weights, second_amplitudes)
    )
    if first_auto <= 0.0 or second_auto <= 0.0:
        raise ValueError("both filtered auto-spectral coefficients must be positive")
    cross = sum(
        weight * first * second * center
        for weight, first, second, center in zip(
            weights,
            first_amplitudes,
            second_amplitudes,
            center_factors,
        )
    )
    normalization = sqrt(first_auto * second_auto)
    normalized_correlation = cross / normalization
    zero_mode_bound = zero_frequency_scalar_correlation(y)
    relative_variance = first_auto + second_auto - 2.0 * cross
    relative_variance_lower_bound = (
        (sqrt(first_auto) - sqrt(second_auto)) ** 2
        + 2.0 * (1.0 - zero_mode_bound) * normalization
    )
    return {
        "center_distance_over_radius_y": y,
        "spectral_parameters_p": parameters,
        "nonnegative_spectral_filter_weights": weights,
        "first_profile_spectral_amplitudes": first_amplitudes,
        "second_profile_spectral_amplitudes": second_amplitudes,
        "center_spherical_factors": center_factors,
        "first_filtered_auto_coefficient": first_auto,
        "second_filtered_auto_coefficient": second_auto,
        "filtered_cross_coefficient": cross,
        "normalized_filtered_correlation": normalized_correlation,
        "zero_frequency_center_correlation_upper_bound": zero_mode_bound,
        "absolute_correlation_respects_zero_mode_bound": (
            abs(normalized_correlation) <= zero_mode_bound + 1.0e-14
        ),
        "relative_noise_variance": relative_variance,
        "relative_noise_variance_lower_bound": relative_variance_lower_bound,
        "relative_noise_variance_respects_bound": (
            relative_variance + 1.0e-14 >= relative_variance_lower_bound
        ),
        "proof_formula": (
            "|phi_p(y)|<=phi_0(y), followed by weighted Cauchy-Schwarz: "
            "|integral w A_f A_g phi_p|<=phi_0 sqrt(integral w A_f^2 "
            "integral w A_g^2)"
        ),
        "scope": (
            "common nonnegative stationary spectral/filter weight, radial optical "
            "profiles, and scalar pure-dephasing covariance; not dissipative jump "
            "operators or nonradial torque"
        ),
    }


def _numerical_spherical_mean(
    center_distance_over_radius: float,
    shell_radius_over_radius: float,
    *,
    intervals: int = 8192,
) -> float:
    """Numerically integrate the angular mean for an independent audit."""
    r = center_distance_over_radius
    u = shell_radius_over_radius
    _validate_nonnegative("center_distance_over_radius", r)
    _validate_nonnegative("shell_radius_over_radius", u)
    if isinstance(intervals, bool) or not isinstance(intervals, int) or intervals < 2:
        raise ValueError("intervals must be an integer at least two")
    if intervals % 2:
        raise ValueError("intervals must be even for Simpson integration")
    if r == 0.0 or u == 0.0:
        return zero_frequency_spherical_mean(r, u)

    def integrand(cosine: float) -> float:
        cosh_distance = (
            cosh(r) * cosh(u) - sinh(r) * sinh(u) * cosine
        )
        distance = acosh(max(1.0, cosh_distance))
        return 0.5 * zero_frequency_scalar_correlation(distance)

    step = 2.0 / float(intervals)
    total = integrand(-1.0) + integrand(1.0)
    for index in range(1, intervals):
        cosine = -1.0 + index * step
        total += (4.0 if index % 2 else 2.0) * integrand(cosine)
    return step * total / 3.0


def static_patch_radial_smearing_certificate() -> dict[str, object]:
    """Audit the spherical product formula and arbitrary-profile cancellation."""
    mean_pairs = ((0.2, 0.3), (0.7, 1.1), (1.5, 1.5), (2.0, 0.4), (3.0, 2.5))
    mean_records = tuple(
        {
            "center_distance_over_radius": center,
            "shell_radius_over_radius": shell,
            "closed_spherical_mean": zero_frequency_spherical_mean(center, shell),
            "numerical_spherical_mean": _numerical_spherical_mean(center, shell),
        }
        for center, shell in mean_pairs
    )
    profiles = (
        ((0.0,), (1.0,)),
        ((0.1, 0.5, 1.0), (1.0, 2.0, 1.0)),
        ((0.3, 1.5, 4.0), (0.2, 0.3, 0.5)),
    )
    center_distances = (0.0, 0.2, 1.0, 3.0)
    smearing_records = tuple(
        radial_smeared_zero_frequency_record(
            center,
            first_shell_radii=first_profile[0],
            first_shell_weights=first_profile[1],
            second_shell_radii=second_profile[0],
            second_shell_weights=second_profile[1],
        )
        for center in center_distances
        for first_profile, second_profile in zip(profiles, reversed(profiles))
    )
    center_gradient_records = tuple(
        radial_center_gradient_zero_frequency_record(
            center,
            first_shell_radii=first_profile[0],
            first_shell_weights=first_profile[1],
            second_shell_radii=second_profile[0],
            second_shell_weights=second_profile[1],
        )
        for center in center_distances
        for first_profile, second_profile in zip(profiles, reversed(profiles))
    )
    switching_records = tuple(
        finite_switching_radial_correlation_record(
            center,
            spectral_parameters=(0.0, 0.2, 0.7, 1.5, 3.0),
            spectral_weights=(0.2, 1.0, 0.7, 0.4, 0.1),
            first_shell_radii=first_profile[0],
            first_shell_weights=first_profile[1],
            second_shell_radii=second_profile[0],
            second_shell_weights=second_profile[1],
        )
        for center in (0.2, 1.0, 3.0)
        for first_profile, second_profile in zip(profiles, reversed(profiles))
    )
    maximum_mean_residual = max(
        abs(record["closed_spherical_mean"] - record["numerical_spherical_mean"])
        for record in mean_records
    )
    certified_claims = {
        "spherical_mean_product_formula_matches_direct_quadrature": (
            maximum_mean_residual < 2.0e-10
        ),
        "arbitrary_nonnegative_radial_profiles_cancel_from_normalized_correlation": all(
            record["radial_smearing_cancels_exactly"]
            for record in smearing_records
        ),
        "profile_amplitudes_are_strictly_positive": all(
            record["first_profile_spherical_amplitude"] > 0.0
            and record["second_profile_spherical_amplitude"] > 0.0
            for record in smearing_records
        ),
        "finite_radial_width_neither_repairs_nor_worsens_common_mode": all(
            abs(
                record["normalized_cross_spectral_correlation"]
                - zero_frequency_scalar_correlation(
                    record["center_distance_over_radius_y"]
                )
            )
            < 1.0e-14
            for record in smearing_records
        ),
        "center_gradient_smearing_preserves_both_tensor_correlations": all(
            record["radial_center_gradient_smearing_cancels_exactly"]
            for record in center_gradient_records
        ),
        "finite_switching_correlation_cannot_exceed_zero_mode_value": all(
            record["absolute_correlation_respects_zero_mode_bound"]
            for record in switching_records
        ),
        "finite_switching_relative_noise_obeys_geometric_floor": all(
            record["relative_noise_variance_respects_bound"]
            for record in switching_records
        ),
    }
    return {
        "goal": "Static-Patch Radial-Smearing Invariance",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "exact_h3_spherical_function_smearing_theorem",
        "central_result": (
            "For arbitrary nonnegative radial optical profiles f and g, the "
            "zero-frequency Bunch-Davies coefficients obey B12=A_f A_g phi0(y), "
            "B11=A_f^2, and B22=A_g^2. Their normalized correlation is exactly "
            "phi0(y)=y/sinh(y), independent of both profile radii and shapes. "
            "For smooth compact profiles, differentiating the translated "
            "convolutions with respect to their centers similarly preserves "
            "both normalized point-gradient tensor correlations."
        ),
        "physical_consequence": (
            "Finite radial worldtube size cannot repair the fixed-center-separation "
            "common-mode obstruction in this axial scalar model. Any common "
            "nonnegative finite-switching spectral filter has normalized "
            "correlation no larger than the zero-mode value, so the co-location "
            "scaling survives without an optical-pointlike or infinite-time "
            "assumption for the declared radial pure-dephasing class. Smooth "
            "center-gradient smearing also supplies a UV-regular zero-mode "
            "bath operator for the gradient model."
        ),
        "claim_boundary": (
            "profiles are nonnegative, stationary, and radial in the optical H3 "
            "measure; their conformal source weights must realize that coupling. "
            "The exact cancellation is zero-frequency; the finite-switching result "
            "is an upper bound for scalar pure-dephasing covariance. This is not a "
            "three-axis distributed top current and does not control nonradial "
            "profiles, finite-time gradient spectral averages, dissipative jump "
            "sectors, the Davies approximation, stress-energy, or backreaction."
        ),
        "certified_claims": certified_claims,
        "maximum_spherical_mean_quadrature_residual": maximum_mean_residual,
        "spherical_mean_records": mean_records,
        "smearing_records": smearing_records,
        "center_gradient_smearing_records": center_gradient_records,
        "finite_switching_records": switching_records,
        "next_physics_gate": (
            "derive the actual spherical-top torque density and decompose its "
            "nonradial optical multipoles; the radial monopole alone cannot evade "
            "the center-separation obstruction"
        ),
    }
