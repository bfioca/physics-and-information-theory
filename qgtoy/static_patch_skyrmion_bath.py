"""Matter-derived stationary bath form factor for the centered Skyrmion.

The leading rigid-hedgehog current already used by
``skyrmion_current_moments`` can be coupled locally to the acceleration-improved
conformal pseudoscalar gradient. Angular integration projects the interaction
onto the optical ``l=1`` channel and produces a radial form factor fixed by the
Skyrmion inertia density. The interaction is the declared Killing-time
charge-flux coupling ``V=g sum_i int_Sigma dSigma_mu ell_i^mu B_i``; a coupling
to the local density ``u_mu ell_i^mu`` would carry a different lapse weight. No
external convolution-square regulator is inserted.

The centered hard-wall current is compact and strongly UV suppressing, but its
real form factor has simple zeros. With the principal spectral square root this
creates absolute-value cusps, so the existing ``H^2`` Sobolev route to the ULE
moment bound does not apply. This is a no-go for that sufficient proof route,
not for reduced dynamics or Markovian approximation in general.
"""

from __future__ import annotations

from functools import lru_cache
from math import asin, atanh, cos, exp, expm1, isfinite, pi, sin, sqrt, tanh

from .massive_skyrmion_profile import dimensionless_inertia_density
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile
from .static_patch_overlapping_ule import (
    smeared_gradient_zero_frequency_spectrum,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _trapezoid(
    points: tuple[tuple[float, float, float], ...],
    values: tuple[float, ...],
) -> float:
    return sum(
        (values[index] + values[index + 1])
        * (points[index + 1][0] - points[index][0])
        / 2.0
        for index in range(len(points) - 1)
    )


@lru_cache(maxsize=16)
def _centered_profile(
    pion_mass: float,
    curvature: float,
    wall_radius: float,
    step: float,
) -> tuple[tuple[float, float, float], ...]:
    return solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )[1]


def _sinc(value: float) -> float:
    if abs(value) < 1.0e-3:
        squared = value * value
        return 1.0 - squared / 6.0 + squared**2 / 120.0 - squared**3 / 5_040.0
    return sin(value) / value


def _y_coth_minus_one(value: float) -> float:
    if abs(value) < 1.0e-3:
        squared = value * value
        return squared / 3.0 - squared**2 / 45.0 + 2.0 * squared**3 / 945.0
    return value / tanh(value) - 1.0


def _sinc_minus_cos(value: float) -> float:
    if abs(value) < 1.0e-3:
        squared = value * value
        return squared / 3.0 - squared**2 / 30.0 + squared**3 / 840.0
    return _sinc(value) - cos(value)


def optical_dipole_kernel(
    spectral_parameter: float,
    optical_radius_ratio: float,
) -> float:
    """Return ``y coth(y)sinc(py)-cos(py)`` without origin cancellation."""
    if not isfinite(spectral_parameter):
        raise ValueError("spectral_parameter must be finite")
    _validate_nonnegative("optical_radius_ratio", optical_radius_ratio)
    phase = spectral_parameter * optical_radius_ratio
    return (
        _y_coth_minus_one(optical_radius_ratio) * _sinc(phase)
        + _sinc_minus_cos(phase)
    )


def dipole_angular_projection_coefficients(
    *,
    optical_radius_ratio: float,
) -> tuple[float, float]:
    """Return both sides of the ``l=1`` angular integration identity.

    For ``chi=n_j`` on an optical sphere, both the directly projected gradient
    and the integration-by-parts expression have coefficient
    ``8pi/[3 R sinh(y)]``. Radius is suppressed from both returned values.
    """
    _validate_positive("optical_radius_ratio", optical_radius_ratio)
    coefficient = 8.0 * pi / (3.0 * sinh_stable(optical_radius_ratio))
    integrated_by_parts = (
        2.0
        / sinh_stable(optical_radius_ratio)
        * (4.0 * pi / 3.0)
    )
    return coefficient, integrated_by_parts


def numerical_dipole_angular_projection_coefficient(
    *,
    optical_radius_ratio: float,
    steps: int = 4_000,
) -> float:
    """Independently integrate ``int sin(theta)^2 dOmega/sinh(y)``."""
    _validate_positive("optical_radius_ratio", optical_radius_ratio)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 2:
        raise ValueError("steps must be an even integer at least two")
    if steps % 2:
        raise ValueError("steps must be even")
    width = pi / steps

    def integrand(theta: float) -> float:
        return sin(theta) ** 3

    total = integrand(0.0) + integrand(pi)
    total += 4.0 * sum(integrand(index * width) for index in range(1, steps, 2))
    total += 2.0 * sum(integrand(index * width) for index in range(2, steps, 2))
    return 2.0 * pi * width * total / (
        3.0 * sinh_stable(optical_radius_ratio)
    )


def sinh_stable(value: float) -> float:
    """Return ``sinh(value)`` with a short origin series."""
    _validate_nonnegative("value", value)
    if value < 1.0e-4:
        squared = value * value
        return value * (1.0 + squared / 6.0 + squared**2 / 120.0)
    return 0.5 * (exp(value) - exp(-value))


def skyrmion_current_optical_form_factor_from_profile(
    spectral_parameter: float,
    points: tuple[tuple[float, float, float], ...],
    *,
    curvature: float,
) -> float:
    """Return the exact centered-current ``l=1`` form-factor quadrature.

    ``curvature=(e f_pi R)^-2`` and ``p=R|omega|``. The inertia density already
    contains the radial ``x^2`` factor, so the numerator divides it by ``x^2``
    before inserting the optical dipole kernel.
    """
    if not isfinite(spectral_parameter):
        raise ValueError("spectral_parameter must be finite")
    _validate_positive("curvature", curvature)
    if len(points) < 2:
        raise ValueError("points must contain at least two profile samples")
    p = abs(spectral_parameter)
    root_curvature = sqrt(curvature)
    inertia_values = tuple(
        dimensionless_inertia_density(
            radius_value,
            profile,
            derivative,
            curvature=curvature,
        )
        for radius_value, profile, derivative in points
    )
    inertia = _trapezoid(points, inertia_values)
    numerator_values = []
    for (radius_value, _, _), density in zip(points, inertia_values):
        z = root_curvature * radius_value
        if z >= 1.0:
            raise ValueError("profile support must lie strictly inside the horizon")
        y = atanh(z)
        numerator_values.append(
            density * optical_dipole_kernel(p, y) / radius_value**2
        )
    numerator = _trapezoid(points, tuple(numerator_values))
    return 3.0 * numerator / (curvature * (1.0 + p * p) * inertia)


def skyrmion_current_optical_form_factor(
    spectral_parameter: float,
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> float:
    """Solve the centered hard-wall profile and return its matter form factor."""
    points = _centered_profile(pion_mass, curvature, wall_radius, step)
    return skyrmion_current_optical_form_factor_from_profile(
        spectral_parameter,
        points,
        curvature=curvature,
    )


def skyrmion_current_gradient_spectrum(
    frequency: float,
    *,
    radius: float = 1.0,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> float:
    """Return ``j_0(w) H_Sky(R|w|)^2`` for the matter-derived current."""
    if not isfinite(frequency):
        raise ValueError("frequency must be finite")
    _validate_positive("radius", radius)
    form_factor = skyrmion_current_optical_form_factor(
        radius * abs(frequency),
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    zero = smeared_gradient_zero_frequency_spectrum(radius=radius)
    if frequency == 0.0:
        return zero * form_factor**2
    if frequency < 0.0:
        return exp(2.0 * pi * radius * frequency) * (
            skyrmion_current_gradient_spectrum(
                -frequency,
                radius=radius,
                pion_mass=pion_mass,
                curvature=curvature,
                wall_radius=wall_radius,
                step=step,
            )
        )
    denominator = -expm1(-2.0 * pi * radius * frequency)
    bare = (
        frequency
        * (1.0 + (radius * frequency) ** 2)
        / (12.0 * pi**2 * radius**2 * denominator)
    )
    return bare * form_factor**2


def _first_form_factor_zero(
    points: tuple[tuple[float, float, float], ...],
    *,
    curvature: float,
    search_start: float = 0.0,
    search_stop: float | None = None,
    search_step: float | None = None,
) -> tuple[float, float]:
    wall_optical_radius = atanh(sqrt(curvature) * points[-1][0])
    if search_stop is None:
        search_stop = max(300.0, 100.0 / wall_optical_radius)
    if search_step is None:
        search_step = min(0.5, pi / (16.0 * wall_optical_radius))
    previous_p = search_start
    previous = skyrmion_current_optical_form_factor_from_profile(
        previous_p,
        points,
        curvature=curvature,
    )
    count = int((search_stop - search_start) / search_step)
    for index in range(1, count + 1):
        current_p = search_start + index * search_step
        current = skyrmion_current_optical_form_factor_from_profile(
            current_p,
            points,
            curvature=curvature,
        )
        if previous * current <= 0.0:
            low = previous_p
            high = current_p
            low_value = previous
            for _ in range(52):
                middle = 0.5 * (low + high)
                middle_value = skyrmion_current_optical_form_factor_from_profile(
                    middle,
                    points,
                    curvature=curvature,
                )
                if low_value * middle_value <= 0.0:
                    high = middle
                else:
                    low = middle
                    low_value = middle_value
            zero = 0.5 * (low + high)
            spacing = 1.0e-3
            derivative = (
                skyrmion_current_optical_form_factor_from_profile(
                    zero + spacing,
                    points,
                    curvature=curvature,
                )
                - skyrmion_current_optical_form_factor_from_profile(
                    zero - spacing,
                    points,
                    curvature=curvature,
                )
            ) / (2.0 * spacing)
            return zero, derivative
        previous_p = current_p
        previous = current
    raise ValueError("no form-factor zero found in the declared search window")


def skyrmion_current_bath_record(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, float]:
    """Return the matter form factor, curvature enhancement, and first zero."""
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("step", step)
    points = _centered_profile(pion_mass, curvature, wall_radius, step)
    root_curvature = sqrt(curvature)
    z_wall = root_curvature * wall_radius
    if z_wall >= 1.0:
        raise ValueError("wall must lie strictly inside the horizon")
    inertia_values = tuple(
        dimensionless_inertia_density(
            radius_value,
            profile,
            derivative,
            curvature=curvature,
        )
        for radius_value, profile, derivative in points
    )
    inertia = _trapezoid(points, inertia_values)

    def moment(power: int) -> float:
        return _trapezoid(
            points,
            tuple(
                density * (root_curvature * point[0]) ** power
                for point, density in zip(points, inertia_values)
            ),
        ) / inertia

    zero_mode = skyrmion_current_optical_form_factor_from_profile(
        0.0,
        points,
        curvature=curvature,
    )
    series_through_six = (
        1.0
        + 3.0 * moment(2) / 5.0
        + 3.0 * moment(4) / 7.0
        + moment(6) / 3.0
    )
    first_zero, zero_derivative = _first_form_factor_zero(
        points,
        curvature=curvature,
    )
    return {
        "optical_wall_radius_over_de_sitter_radius": atanh(z_wall),
        "proper_wall_radius_in_inverse_e_fpi": (
            asin(z_wall) / root_curvature
        ),
        "zero_mode_form_factor": zero_mode,
        "zero_frequency_rate_ratio": zero_mode**2,
        "zero_mode_series_through_sixth_moment": series_through_six,
        "zero_mode_series_remainder": zero_mode - series_through_six,
        "form_factor_at_p_1": skyrmion_current_optical_form_factor_from_profile(
            1.0,
            points,
            curvature=curvature,
        ),
        "form_factor_at_p_100": skyrmion_current_optical_form_factor_from_profile(
            100.0,
            points,
            curvature=curvature,
        ),
        "first_form_factor_zero": first_zero,
        "form_factor_derivative_at_first_zero": zero_derivative,
        "form_factor_absolute_value_derivative_jump": 2.0
        * abs(zero_derivative),
    }


def static_patch_skyrmion_bath_certificate(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, object]:
    """Audit the centered matter-derived spectrum and Sobolev obstruction."""
    record = skyrmion_current_bath_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    refined = skyrmion_current_bath_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step / 2.0,
    )
    zero_change = abs(
        refined["zero_mode_form_factor"] / record["zero_mode_form_factor"] - 1.0
    )
    root_change = abs(
        refined["first_form_factor_zero"]
        / record["first_form_factor_zero"]
        - 1.0
    )
    claims = {
        "matter_form_factor_is_even_in_spectral_parameter": abs(
            skyrmion_current_optical_form_factor(
                5.0,
                pion_mass=pion_mass,
                curvature=curvature,
                wall_radius=wall_radius,
                step=step,
            )
            - skyrmion_current_optical_form_factor(
                -5.0,
                pion_mass=pion_mass,
                curvature=curvature,
                wall_radius=wall_radius,
                step=step,
            )
        )
        < 1.0e-14,
        "extended_positive_current_enhances_zero_mode": (
            record["zero_mode_form_factor"] > 1.0
            and record["zero_frequency_rate_ratio"] > 1.0
        ),
        "zero_mode_moment_series_converges_from_below": (
            0.0 < record["zero_mode_series_remainder"] < 1.0e-7
        ),
        "zero_mode_is_step_stable": zero_change < 1.0e-9,
        "first_simple_zero_is_step_stable": (
            root_change < 1.0e-8
            and abs(record["form_factor_derivative_at_first_zero"]) > 1.0e-10
        ),
        "matter_spectrum_is_positive_and_kms_balanced": (
            skyrmion_current_gradient_spectrum(
                0.7,
                pion_mass=pion_mass,
                curvature=curvature,
                wall_radius=wall_radius,
                step=step,
            )
            > 0.0
            and abs(
                skyrmion_current_gradient_spectrum(
                    -0.7,
                    pion_mass=pion_mass,
                    curvature=curvature,
                    wall_radius=wall_radius,
                    step=step,
                )
                / skyrmion_current_gradient_spectrum(
                    0.7,
                    pion_mass=pion_mass,
                    curvature=curvature,
                    wall_radius=wall_radius,
                    step=step,
                )
                - exp(-2.0 * pi * 0.7)
            )
            < 1.0e-13
        ),
    }
    return {
        "goal": "Centered Skyrmion Matter-Derived Bath Form-Factor Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "matter_derived_stationary_spectrum_and_principal_root_no_go",
        "central_result": (
            "The centered leading Skyrmion current fixes a compact optical l=1 "
            "form factor without an engineered regulator. Curvature enhances "
            "the zero-frequency rate, while a step-stable simple form-factor "
            "zero makes the principal spectral square root fail the H2 "
            "regularity required by the current Sobolev-ULE moment route."
        ),
        "profile": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius_x_w": wall_radius,
            "step": step,
        },
        "record": record,
        "refined_record": refined,
        "relative_zero_mode_step_change": zero_change,
        "relative_first_zero_step_change": root_change,
        "matter_source_identity": (
            "For V=g sum_i int_Sigma dSigma_mu ell_i^mu B_i, "
            "f_j(X,Omega)=2 kappa(r) N^3 n_j/[I r] after angular "
            "integration of the improved pseudoscalar gradient"
        ),
        "zero_mode_prediction": (
            "H_Sky(0)=<3(artanh z-z)/z^3>_I>1, so the finite centered "
            "current enhances the zero-frequency gradient rate"
        ),
        "principal_root_no_go": (
            "A simple real zero of H_Sky makes sqrt(j)=sqrt(j0)|H_Sky| "
            "cusped and therefore not H2. The existing Q2/M1 Sobolev ULE "
            "certificate cannot be imported for this hard-wall matter profile."
        ),
        "certified_claims": claims,
        "claim_boundary": (
            "The derivation assumes the standard leading collective-current "
            "compression, a centered rigid hard-wall Skyrmion, no wall rotation "
            "current, scalar h(J^2) target Hamiltonian, stationary Killing-time "
            "charge-flux coupling, and the acceleration-improved conformal "
            "pseudoscalar. A local u_mu ell_i^mu density coupling would have a "
            "different lapse weight. "
            "The simple zero is step-converged numerical evidence; the cusp "
            "conclusion is analytic conditional on that zero. Off-center "
            "deformation, finite switching, collective-band errors, wall modes, "
            "stress, lifetime, and gravity remain open."
        ),
        "next_physics_gate": (
            "complete the signed real-factor route with interval-certified "
            "global Sobolev constants, or derive a reduced-dynamics bound "
            "controlled directly by j rather than the principal sqrt(j)"
        ),
    }
