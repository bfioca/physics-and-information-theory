"""Massive-Skyrmion profile equations and the static-patch inertia gate.

The convention is metric signature ``(+---)`` and the pion-mass term is
normalized so that the parameter ``m_pi`` is the physical small-fluctuation
mass.  Dimensionless variables are

    x = e f_pi r,  mu = m_pi/(e f_pi),  lambda = 1/(e f_pi R)^2.

The executable flat-space profile is a dependency-free shooting calculation.
The fixed-de-Sitter part is an analytic gate: regular horizon data with
``sin(F_c) != 0`` give a logarithmically divergent global rigid-rotor inertia.
A finite supported worldtube is the selected controlled remedy; this module
does not prove that every nontrivial global horizon-regular profile has such
boundary data.
"""

from __future__ import annotations

from math import asin, cos, isfinite, pi, sin, sqrt


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def static_patch_lapse(dimensionless_radius: float, curvature: float) -> float:
    """Return ``N(x)=1-lambda x^2`` in the fixed static patch."""
    _validate_nonnegative("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("curvature", curvature)
    return 1.0 - curvature * dimensionless_radius**2


def reduced_energy_density(
    dimensionless_radius: float,
    profile: float,
    profile_derivative: float,
    *,
    pion_mass: float,
    curvature: float = 0.0,
) -> float:
    """Return the dimensionless static hedgehog energy density.

    The mass term has coefficient ``mu^2 x^2 (1-cos(F))/4``.  This corresponds
    to ``f_pi^2 m_pi^2 Tr(U+U^dagger-2)/16`` in the ``(+---)`` action.
    """
    _validate_positive("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(dimensionless_radius, curvature)
    if lapse < 0.0:
        raise ValueError("dimensionless_radius lies outside the static patch")
    sine = sin(profile)
    u = dimensionless_radius**2 + 8.0 * sine**2
    return (
        lapse * u * profile_derivative**2 / 8.0
        + sine**2 / 4.0
        + sine**4 / (2.0 * dimensionless_radius**2)
        + pion_mass**2
        * dimensionless_radius**2
        * (1.0 - cos(profile))
        / 4.0
    )


def profile_flux_source(
    dimensionless_radius: float,
    profile: float,
    profile_derivative: float,
    *,
    pion_mass: float,
    curvature: float = 0.0,
) -> float:
    """Return the source in ``(N u F')'=source``."""
    _validate_positive("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(dimensionless_radius, curvature)
    if lapse < 0.0:
        raise ValueError("dimensionless_radius lies outside the static patch")
    sine = sin(profile)
    return (
        (
            4.0 * lapse * profile_derivative**2
            + 1.0
            + 4.0 * sine**2 / dimensionless_radius**2
        )
        * sin(2.0 * profile)
        + pion_mass**2 * dimensionless_radius**2 * sine
    )


def flat_profile_acceleration(
    dimensionless_radius: float,
    profile: float,
    profile_derivative: float,
    *,
    pion_mass: float,
) -> float:
    """Return ``F''`` for the flat-space massive hedgehog equation."""
    _validate_positive("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("pion_mass", pion_mass)
    sine = sin(profile)
    u = dimensionless_radius**2 + 8.0 * sine**2
    return (
        -2.0 * dimensionless_radius * profile_derivative
        - 4.0 * sin(2.0 * profile) * profile_derivative**2
        + (1.0 + 4.0 * sine**2 / dimensionless_radius**2)
        * sin(2.0 * profile)
        + pion_mass**2 * dimensionless_radius**2 * sine
    ) / u


def flat_tail_log_derivative(
    dimensionless_radius: float,
    *,
    pion_mass: float,
) -> float:
    """Return the linear massive ``l=1`` tail value ``F'/F``."""
    _validate_positive("dimensionless_radius", dimensionless_radius)
    _validate_positive("pion_mass", pion_mass)
    scaled = pion_mass * dimensionless_radius
    return (
        -pion_mass
        + pion_mass / (scaled + 1.0)
        - 2.0 / dimensionless_radius
    )


def baryon_number_inside_boundary(boundary_profile: float) -> float:
    """Return the hedgehog baryon number between ``F(0)=pi`` and ``F_*``."""
    if not isfinite(boundary_profile):
        raise ValueError("boundary_profile must be finite")
    return 1.0 - (
        2.0 * boundary_profile - sin(2.0 * boundary_profile)
    ) / (2.0 * pi)


def de_sitter_horizon_profile_derivative(
    horizon_profile: float,
    *,
    horizon_radius: float,
    pion_mass: float,
) -> float:
    """Return the derivative selected by regularity at the Killing horizon."""
    if not isfinite(horizon_profile):
        raise ValueError("horizon_profile must be finite")
    _validate_positive("horizon_radius", horizon_radius)
    _validate_nonnegative("pion_mass", pion_mass)
    sine = sin(horizon_profile)
    u = horizon_radius**2 + 8.0 * sine**2
    source = (
        (1.0 + 4.0 * sine**2 / horizon_radius**2)
        * sin(2.0 * horizon_profile)
        + pion_mass**2 * horizon_radius**2 * sine
    )
    lapse_derivative = -2.0 / horizon_radius
    return source / (lapse_derivative * u)


def dimensionless_inertia_density(
    dimensionless_radius: float,
    profile: float,
    profile_derivative: float,
    *,
    curvature: float = 0.0,
) -> float:
    """Return the integrand of ``c_I`` including its ``2 pi/3`` factor."""
    _validate_positive("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(dimensionless_radius, curvature)
    if lapse <= 0.0:
        raise ValueError("inertia density requires a point inside the horizon")
    sine = sin(profile)
    return (
        2.0
        * pi
        / 3.0
        * dimensionless_radius**2
        * sine**2
        * (
            1.0 / lapse
            + 4.0 * profile_derivative**2
            + 4.0 * sine**2 / (lapse * dimensionless_radius**2)
        )
    )


def de_sitter_inertia_log_coefficient(
    horizon_profile: float,
    *,
    horizon_radius: float,
) -> float:
    """Return ``C`` in ``c_I(epsilon)=C log(1/epsilon)+O(1)``."""
    if not isfinite(horizon_profile):
        raise ValueError("horizon_profile must be finite")
    _validate_positive("horizon_radius", horizon_radius)
    sine = sin(horizon_profile)
    return (
        pi
        * horizon_radius
        / 3.0
        * (horizon_radius**2 * sine**2 + 4.0 * sine**4)
    )


def proper_radius_from_dimensionless(
    dimensionless_radius: float,
    *,
    inverse_length_scale: float,
    curvature: float,
) -> float:
    """Convert ``x`` to static-slice proper radial distance."""
    _validate_nonnegative("dimensionless_radius", dimensionless_radius)
    _validate_positive("inverse_length_scale", inverse_length_scale)
    _validate_nonnegative("curvature", curvature)
    if curvature == 0.0:
        return dimensionless_radius / inverse_length_scale
    argument = sqrt(curvature) * dimensionless_radius
    if argument > 1.0:
        raise ValueError("dimensionless_radius lies outside the static patch")
    return asin(argument) / (inverse_length_scale * sqrt(curvature))


def _rk4_flat_profile(
    shooting_slope: float,
    *,
    pion_mass: float,
    maximum_radius: float,
    step: float,
    origin_cutoff: float,
) -> tuple[tuple[float, float, float], ...]:
    radius = origin_cutoff
    profile = pi - shooting_slope * radius
    derivative = -shooting_slope
    points = [(radius, profile, derivative)]
    while radius < maximum_radius:
        width = min(step, maximum_radius - radius)

        def rhs(x: float, value: float, slope: float) -> tuple[float, float]:
            return slope, flat_profile_acceleration(
                x,
                value,
                slope,
                pion_mass=pion_mass,
            )

        k1 = rhs(radius, profile, derivative)
        k2 = rhs(
            radius + width / 2.0,
            profile + width * k1[0] / 2.0,
            derivative + width * k1[1] / 2.0,
        )
        k3 = rhs(
            radius + width / 2.0,
            profile + width * k2[0] / 2.0,
            derivative + width * k2[1] / 2.0,
        )
        k4 = rhs(
            radius + width,
            profile + width * k3[0],
            derivative + width * k3[1],
        )
        profile += width * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]) / 6.0
        derivative += width * (
            k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]
        ) / 6.0
        radius += width
        points.append((radius, profile, derivative))
    return tuple(points)


def _flat_tail_residual(
    shooting_slope: float,
    *,
    pion_mass: float,
    maximum_radius: float,
    step: float,
    origin_cutoff: float,
) -> float:
    radius, profile, derivative = _rk4_flat_profile(
        shooting_slope,
        pion_mass=pion_mass,
        maximum_radius=maximum_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )[-1]
    return derivative - flat_tail_log_derivative(
        radius,
        pion_mass=pion_mass,
    ) * profile


def _find_flat_shooting_bracket(
    *,
    pion_mass: float,
    maximum_radius: float,
    step: float,
    origin_cutoff: float,
) -> tuple[float, float]:
    """Find the first positive-slope tail-residual sign change."""
    scan_width = 0.05
    maximum_slope = max(6.0, 2.0 + 2.0 * pion_mass)
    low = scan_width
    low_residual = _flat_tail_residual(
        low,
        pion_mass=pion_mass,
        maximum_radius=maximum_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )
    while low < maximum_slope:
        high = low + scan_width
        high_residual = _flat_tail_residual(
            high,
            pion_mass=pion_mass,
            maximum_radius=maximum_radius,
            step=step,
            origin_cutoff=origin_cutoff,
        )
        if low_residual * high_residual <= 0.0:
            return low, high
        low = high
        low_residual = high_residual
    raise ValueError("could not auto-bracket the physical tail root")


def solve_flat_skyrmion_profile(
    *,
    pion_mass: float = 1.0,
    maximum_radius: float = 10.0,
    step: float = 0.002,
    lower_shooting_slope: float = 1.5,
    upper_shooting_slope: float = 1.65,
    origin_cutoff: float = 1.0e-4,
    bisection_steps: int = 52,
    auto_bracket: bool = True,
) -> tuple[float, tuple[tuple[float, float, float], ...]]:
    """Solve the flat massive profile by shooting to the linear tail Robin data.

    The default bracket selects the monotone unit-baryon solution at ``mu=1``.
    If it does not straddle a root, a positive-slope scan finds the first tail
    residual sign change.
    """
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("maximum_radius", maximum_radius)
    _validate_positive("step", step)
    _validate_positive("lower_shooting_slope", lower_shooting_slope)
    _validate_positive("upper_shooting_slope", upper_shooting_slope)
    _validate_positive("origin_cutoff", origin_cutoff)
    if lower_shooting_slope >= upper_shooting_slope:
        raise ValueError("shooting-slope bracket must be ordered")
    if maximum_radius <= origin_cutoff:
        raise ValueError("maximum_radius must exceed origin_cutoff")
    if isinstance(bisection_steps, bool) or not isinstance(bisection_steps, int):
        raise ValueError("bisection_steps must be an integer")
    if bisection_steps < 1:
        raise ValueError("bisection_steps must be positive")
    if not isinstance(auto_bracket, bool):
        raise ValueError("auto_bracket must be boolean")

    low = lower_shooting_slope
    high = upper_shooting_slope
    low_residual = _flat_tail_residual(
        low,
        pion_mass=pion_mass,
        maximum_radius=maximum_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )
    high_residual = _flat_tail_residual(
        high,
        pion_mass=pion_mass,
        maximum_radius=maximum_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )
    if low_residual * high_residual > 0.0:
        if not auto_bracket:
            raise ValueError("shooting-slope bracket does not straddle a tail root")
        low, high = _find_flat_shooting_bracket(
            pion_mass=pion_mass,
            maximum_radius=maximum_radius,
            step=step,
            origin_cutoff=origin_cutoff,
        )
        low_residual = _flat_tail_residual(
            low,
            pion_mass=pion_mass,
            maximum_radius=maximum_radius,
            step=step,
            origin_cutoff=origin_cutoff,
        )
    for _ in range(bisection_steps):
        middle = 0.5 * (low + high)
        middle_residual = _flat_tail_residual(
            middle,
            pion_mass=pion_mass,
            maximum_radius=maximum_radius,
            step=step,
            origin_cutoff=origin_cutoff,
        )
        if low_residual * middle_residual <= 0.0:
            high = middle
        else:
            low = middle
            low_residual = middle_residual
    slope = 0.5 * (low + high)
    points = _rk4_flat_profile(
        slope,
        pion_mass=pion_mass,
        maximum_radius=maximum_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )
    radius, profile, derivative = points[-1]
    tail_residual = derivative - flat_tail_log_derivative(
        radius,
        pion_mass=pion_mass,
    ) * profile
    residual_tolerance = 1.0e-5
    profile_is_resolved = (
        abs(tail_residual) <= residual_tolerance
        and all(
            -residual_tolerance <= value <= pi + residual_tolerance
            and slope_value <= residual_tolerance
            for _, value, slope_value in points
        )
    )
    if not profile_is_resolved:
        raise ValueError(
            "outward shooting did not resolve the monotone massive-tail branch; "
            "reduce the step/matching radius or use collocation"
        )
    return slope, points


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


def flat_profile_integrals(
    points: tuple[tuple[float, float, float], ...],
    *,
    pion_mass: float,
) -> dict[str, float]:
    """Return mass, inertia, baryon, and Derrick diagnostics for a profile."""
    _validate_positive("pion_mass", pion_mass)
    if len(points) < 2:
        raise ValueError("points must contain at least two profile samples")
    sigma_values = []
    skyrme_values = []
    mass_values = []
    inertia_values = []
    baryon_values = []
    for radius, profile, derivative in points:
        _validate_positive("profile radius", radius)
        sine = sin(profile)
        sigma_values.append(radius**2 * derivative**2 / 8.0 + sine**2 / 4.0)
        skyrme_values.append(
            sine**2 * derivative**2 + sine**4 / (2.0 * radius**2)
        )
        mass_values.append(
            pion_mass**2 * radius**2 * (1.0 - cos(profile)) / 4.0
        )
        inertia_values.append(
            dimensionless_inertia_density(radius, profile, derivative)
        )
        baryon_values.append(-2.0 * sine**2 * derivative / pi)
    sigma_energy = _trapezoid(points, tuple(sigma_values))
    skyrme_energy = _trapezoid(points, tuple(skyrme_values))
    mass_energy = _trapezoid(points, tuple(mass_values))
    baryon_integral = _trapezoid(points, tuple(baryon_values))
    boundary_baryon = baryon_number_inside_boundary(points[-1][1])
    return {
        "sigma_energy_E2": sigma_energy,
        "skyrme_energy_E4": skyrme_energy,
        "mass_energy_E0": mass_energy,
        "derrick_residual_E2_minus_E4_plus_3E0": (
            sigma_energy - skyrme_energy + 3.0 * mass_energy
        ),
        "dimensionless_mass_c_M": 4.0
        * pi
        * (sigma_energy + skyrme_energy + mass_energy),
        "dimensionless_inertia_c_I": _trapezoid(points, tuple(inertia_values)),
        "baryon_number_integral": baryon_integral,
        "baryon_number_from_outer_boundary": boundary_baryon,
    }


def massive_skyrmion_profile_certificate(
    *,
    pion_mass: float = 1.0,
    maximum_radius: float = 10.0,
    step: float = 0.002,
) -> dict[str, object]:
    """Certify the flat profile and the fixed-de-Sitter inertia obstruction."""
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("maximum_radius", maximum_radius)
    _validate_positive("step", step)
    effective_maximum_radius = min(maximum_radius, 10.0 / pion_mass)
    slope, points = solve_flat_skyrmion_profile(
        pion_mass=pion_mass,
        maximum_radius=effective_maximum_radius,
        step=step,
    )
    integrals = flat_profile_integrals(points, pion_mass=pion_mass)
    _, refined_points = solve_flat_skyrmion_profile(
        pion_mass=pion_mass,
        maximum_radius=effective_maximum_radius,
        step=step / 2.0,
    )
    refined_integrals = flat_profile_integrals(
        refined_points,
        pion_mass=pion_mass,
    )
    _, extended_points = solve_flat_skyrmion_profile(
        pion_mass=pion_mass,
        maximum_radius=effective_maximum_radius + 2.0 / pion_mass,
        step=step,
    )
    extended_integrals = flat_profile_integrals(
        extended_points,
        pion_mass=pion_mass,
    )
    total_reduced_energy = (
        integrals["sigma_energy_E2"]
        + integrals["skyrme_energy_E4"]
        + integrals["mass_energy_E0"]
    )
    outer_radius, outer_profile, outer_derivative = points[-1]
    tail_residual = outer_derivative - flat_tail_log_derivative(
        outer_radius,
        pion_mass=pion_mass,
    ) * outer_profile

    horizon_radius = 10.0
    horizon_profile = 0.7
    curvature = 1.0 / horizon_radius**2
    horizon_epsilon = 1.0e-6
    near_horizon_radius = horizon_radius - horizon_epsilon
    asymptotic_density_coefficient = horizon_epsilon * dimensionless_inertia_density(
        near_horizon_radius,
        horizon_profile,
        0.0,
        curvature=curvature,
    )
    analytic_density_coefficient = de_sitter_inertia_log_coefficient(
        horizon_profile,
        horizon_radius=horizon_radius,
    )
    certified_claims = {
        "flat_tail_robin_condition_is_satisfied": abs(tail_residual) < 1.0e-7,
        "flat_profile_is_monotone_and_in_physical_range": all(
            0.0 <= profile <= pi and derivative <= 1.0e-7
            for _, profile, derivative in points
        ),
        "baryon_number_is_one_within_truncation_error": abs(
            integrals["baryon_number_integral"] - 1.0
        )
        < 2.0e-5,
        "boundary_and_integrated_baryon_numbers_agree": abs(
            integrals["baryon_number_integral"]
            - integrals["baryon_number_from_outer_boundary"]
        )
        < 2.0e-5,
        "flat_derrick_identity_is_satisfied": abs(
            integrals["derrick_residual_E2_minus_E4_plus_3E0"]
        )
        < 2.0e-6 * total_reduced_energy,
        "flat_mass_and_inertia_are_step_stable": max(
            abs(
                refined_integrals["dimensionless_mass_c_M"]
                / integrals["dimensionless_mass_c_M"]
                - 1.0
            ),
            abs(
                refined_integrals["dimensionless_inertia_c_I"]
                / integrals["dimensionless_inertia_c_I"]
                - 1.0
            ),
        )
        < 1.0e-7,
        "flat_mass_and_inertia_are_outer_radius_stable": max(
            abs(
                extended_integrals["dimensionless_mass_c_M"]
                / integrals["dimensionless_mass_c_M"]
                - 1.0
            ),
            abs(
                extended_integrals["dimensionless_inertia_c_I"]
                / integrals["dimensionless_inertia_c_I"]
                - 1.0
            ),
        )
        < 1.0e-7,
        "generic_de_sitter_inertia_has_predicted_logarithmic_coefficient": abs(
            asymptotic_density_coefficient / analytic_density_coefficient - 1.0
        )
        < 2.0e-6,
        "vacuum_horizon_data_force_zero_regular_slope": (
            de_sitter_horizon_profile_derivative(
                0.0,
                horizon_radius=horizon_radius,
                pion_mass=pion_mass,
            )
            == 0.0
        ),
    }
    return {
        "goal": "Massive-Skyrmion Profile And Static-Patch Inertia Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "flat_profile_plus_fixed_de_sitter_worldtube_obstruction",
        "central_result": (
            "The physical-mass convention gives a dependency-free monotone "
            "unit-baryon flat profile with verified tail, Derrick, mass, and "
            "inertia integrals and step/radius convergence. In a fixed de "
            "Sitter patch, regular horizon data with sin(F_c) nonzero make the "
            "global rigid-rotor inertia diverge logarithmically. A finite "
            "supported worldtube is the selected controlled remedy."
        ),
        "metric_signature": "+---",
        "mass_term_convention": (
            "f_pi^2 m_pi^2 Tr(U+U^dagger-2)/16; m_pi is the physical pion mass"
        ),
        "dimensionless_pion_mass_mu": pion_mass,
        "requested_maximum_flat_radius": maximum_radius,
        "effective_tail_matching_radius": effective_maximum_radius,
        "shooting_slope_b": slope,
        "outer_profile_F": outer_profile,
        "outer_tail_residual": tail_residual,
        "profile_integrals": integrals,
        "profile_convergence": {
            "half_step_mass_c_M": refined_integrals["dimensionless_mass_c_M"],
            "half_step_inertia_c_I": refined_integrals[
                "dimensionless_inertia_c_I"
            ],
            "extended_radius_mass_c_M": extended_integrals[
                "dimensionless_mass_c_M"
            ],
            "extended_radius_inertia_c_I": extended_integrals[
                "dimensionless_inertia_c_I"
            ],
        },
        "de_sitter_gate": {
            "horizon_radius_x_c": horizon_radius,
            "sample_regular_horizon_profile_F_c": horizon_profile,
            "horizon_regular_derivative_F_prime_c": (
                de_sitter_horizon_profile_derivative(
                    horizon_profile,
                    horizon_radius=horizon_radius,
                    pion_mass=pion_mass,
                )
            ),
            "inertia_log_coefficient": analytic_density_coefficient,
            "divergence_condition": "sin(F_c) != 0",
            "worldtube_selected_as_controlled_remedy": True,
            "all_nontrivial_global_profiles_are_proved_to_diverge": False,
        },
        "collective_coupling_gate": (
            "A covariant worldline B_mu S^mu coupling exists after collective-"
            "coordinate reduction, with the dynamical orientation matrix "
            "soldering isospin to physical spin. A point-local coupling written "
            "only in the bare Skyrme field remains unproved."
        ),
        "claim_boundary": (
            "The flat profile calculation is numerical and the fixed-de-Sitter "
            "horizon/inertia statement is conditional on sin(F_c) nonzero for "
            "the rigid collective ansatz. This does not prove a horizon "
            "uniqueness theorem, construct the finite support action, solve "
            "Einstein-Skyrme backreaction, derive the current multipoles, prove "
            "the Omega^4 slow-rotation window, or derive the open-system channel."
        ),
        "certified_claims": certified_claims,
        "next_physics_gate": (
            "introduce a finite covariant supported worldtube, solve the profile "
            "with its boundary action, and project B_mu S^mu onto the collective "
            "band with controlled multipole and slow-rotation errors"
        ),
    }
