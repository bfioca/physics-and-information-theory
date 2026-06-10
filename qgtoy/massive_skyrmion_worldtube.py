"""Centered hard-wall worldtube baseline for the massive Skyrmion.

The wall is a spherical covariant ideal mirror imposing ``U=1`` at
``x=x_w``.  The interior profile therefore obeys ``F(0)=pi`` and ``F(x_w)=0``,
which keeps the hedgehog baryon number exactly one.  A Nambu-Goto membrane
tension is then chosen to satisfy the centered Young-Laplace equation.

This is a controlled WP1 baseline, not the off-center accelerated observer.
Wall stability, a finite-stiffness UV completion, and gravitational junction
conditions remain open.
"""

from __future__ import annotations

from math import cos, isfinite, pi, sin, sqrt

from .massive_skyrmion_profile import (
    baryon_number_inside_boundary,
    dimensionless_inertia_density,
    reduced_energy_density,
    static_patch_lapse,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def origin_cubic_coefficient(
    shooting_slope: float,
    *,
    pion_mass: float,
    curvature: float,
) -> float:
    """Return ``c`` in ``F=pi-bx+cx^3+O(x^5)``."""
    _validate_positive("shooting_slope", shooting_slope)
    _validate_nonnegative("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    slope_squared = shooting_slope**2
    return shooting_slope * (
        pion_mass**2
        - 4.0 * curvature
        + (4.0 / 3.0 - 24.0 * curvature) * slope_squared
        + 8.0 * slope_squared**2 / 3.0
    ) / (10.0 * (1.0 + 8.0 * slope_squared))


def curved_profile_acceleration(
    dimensionless_radius: float,
    profile: float,
    profile_derivative: float,
    *,
    pion_mass: float,
    curvature: float,
) -> float:
    """Return ``F''`` for the fixed-static-patch hedgehog equation."""
    _validate_positive("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(dimensionless_radius, curvature)
    if lapse <= 0.0:
        raise ValueError("profile point must lie strictly inside the horizon")
    lapse_derivative = -2.0 * curvature * dimensionless_radius
    sine = sin(profile)
    u = dimensionless_radius**2 + 8.0 * sine**2
    return (
        (1.0 + 4.0 * sine**2 / dimensionless_radius**2)
        * sin(2.0 * profile)
        + pion_mass**2 * dimensionless_radius**2 * sine
        - (lapse_derivative * u + 2.0 * lapse * dimensionless_radius)
        * profile_derivative
        - 4.0 * lapse * sin(2.0 * profile) * profile_derivative**2
    ) / (lapse * u)


def _rk4_hard_wall_profile(
    shooting_slope: float,
    *,
    pion_mass: float,
    curvature: float,
    wall_radius: float,
    step: float,
    origin_cutoff: float,
) -> tuple[tuple[float, float, float], ...]:
    radius = origin_cutoff
    cubic = origin_cubic_coefficient(
        shooting_slope,
        pion_mass=pion_mass,
        curvature=curvature,
    )
    profile = pi - shooting_slope * radius + cubic * radius**3
    derivative = -shooting_slope + 3.0 * cubic * radius**2
    points = [(radius, profile, derivative)]
    while radius < wall_radius:
        width = min(step, wall_radius - radius)

        def rhs(x: float, value: float, slope: float) -> tuple[float, float]:
            return slope, curved_profile_acceleration(
                x,
                value,
                slope,
                pion_mass=pion_mass,
                curvature=curvature,
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


def _find_hard_wall_bracket(
    *,
    pion_mass: float,
    curvature: float,
    wall_radius: float,
    step: float,
    origin_cutoff: float,
) -> tuple[float, float]:
    width = 0.05
    maximum_slope = max(8.0, 2.0 + 2.0 * pion_mass)
    low = width
    low_value = _rk4_hard_wall_profile(
        low,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )[-1][1]
    while low < maximum_slope:
        high = low + width
        high_value = _rk4_hard_wall_profile(
            high,
            pion_mass=pion_mass,
            curvature=curvature,
            wall_radius=wall_radius,
            step=step,
            origin_cutoff=origin_cutoff,
        )[-1][1]
        if low_value * high_value <= 0.0:
            return low, high
        low = high
        low_value = high_value
    raise ValueError("could not bracket the hard-wall profile")


def solve_hard_wall_skyrmion_profile(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
    origin_cutoff: float = 1.0e-4,
    bisection_steps: int = 52,
) -> tuple[float, tuple[tuple[float, float, float], ...]]:
    """Solve ``F(0)=pi, F(x_w)=0`` by shooting in a fixed static patch."""
    _validate_positive("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("step", step)
    _validate_positive("origin_cutoff", origin_cutoff)
    if static_patch_lapse(wall_radius, curvature) <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    if wall_radius <= origin_cutoff:
        raise ValueError("wall_radius must exceed origin_cutoff")
    if isinstance(bisection_steps, bool) or not isinstance(bisection_steps, int):
        raise ValueError("bisection_steps must be an integer")
    if bisection_steps < 1:
        raise ValueError("bisection_steps must be positive")
    low, high = _find_hard_wall_bracket(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )
    low_value = _rk4_hard_wall_profile(
        low,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )[-1][1]
    for _ in range(bisection_steps):
        middle = 0.5 * (low + high)
        middle_value = _rk4_hard_wall_profile(
            middle,
            pion_mass=pion_mass,
            curvature=curvature,
            wall_radius=wall_radius,
            step=step,
            origin_cutoff=origin_cutoff,
        )[-1][1]
        if low_value * middle_value <= 0.0:
            high = middle
        else:
            low = middle
            low_value = middle_value
    slope = 0.5 * (low + high)
    points = _rk4_hard_wall_profile(
        slope,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        origin_cutoff=origin_cutoff,
    )
    residual_tolerance = 1.0e-6
    wall_residual = abs(points[-1][1])
    profile_is_resolved = (
        wall_residual <= residual_tolerance
        and all(
            -residual_tolerance <= profile <= pi + residual_tolerance
            and derivative <= residual_tolerance
            for _, profile, derivative in points
        )
    )
    if not profile_is_resolved:
        raise ValueError(
            "outward shooting did not resolve the monotone hard-wall branch; "
            "reduce the step or use collocation/multiple shooting"
        )
    return slope, points


def dimensionless_radial_pressure(
    dimensionless_radius: float,
    profile: float,
    profile_derivative: float,
    *,
    pion_mass: float,
    curvature: float,
) -> float:
    """Return the fixed-background radial pressure in ``e^2 f_pi^4`` units."""
    _validate_positive("dimensionless_radius", dimensionless_radius)
    _validate_nonnegative("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(dimensionless_radius, curvature)
    if lapse <= 0.0:
        raise ValueError("pressure point must lie strictly inside the horizon")
    sine = sin(profile)
    return (
        lapse * profile_derivative**2 / 8.0
        + lapse * sine**2 * profile_derivative**2 / dimensionless_radius**2
        - sine**2 / (4.0 * dimensionless_radius**2)
        - sine**4 / (2.0 * dimensionless_radius**4)
        - pion_mass**2 * (1.0 - cos(profile)) / 4.0
    )


def dimensionless_shell_mean_curvature(
    wall_radius: float,
    *,
    curvature: float,
) -> float:
    """Return the centered static-shell mean curvature ``K/(e f_pi)``."""
    _validate_positive("wall_radius", wall_radius)
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(wall_radius, curvature)
    if lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the horizon")
    root_lapse = sqrt(lapse)
    return 2.0 * root_lapse / wall_radius - curvature * wall_radius / root_lapse


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


def hard_wall_profile_integrals(
    points: tuple[tuple[float, float, float], ...],
    *,
    pion_mass: float,
    curvature: float,
) -> dict[str, float]:
    """Return truncated mass, inertia, and baryon diagnostics."""
    if len(points) < 2:
        raise ValueError("points must contain at least two profile samples")
    energy_values = tuple(
        reduced_energy_density(
            radius,
            profile,
            derivative,
            pion_mass=pion_mass,
            curvature=curvature,
        )
        for radius, profile, derivative in points
    )
    inertia_values = tuple(
        dimensionless_inertia_density(
            radius,
            profile,
            derivative,
            curvature=curvature,
        )
        for radius, profile, derivative in points
    )
    baryon_values = tuple(
        -2.0 * sin(profile) ** 2 * derivative / pi
        for _, profile, derivative in points
    )
    return {
        "interior_dimensionless_mass_c_M": 4.0
        * pi
        * _trapezoid(points, energy_values),
        "interior_dimensionless_inertia_c_I": _trapezoid(
            points,
            inertia_values,
        ),
        "baryon_number_integral": _trapezoid(points, baryon_values),
        "baryon_number_from_wall_value": baryon_number_inside_boundary(
            points[-1][1]
        ),
    }


def hard_wall_equilibrium_record(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, object]:
    """Solve the profile and choose the membrane tension from force balance."""
    slope, points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    integrals = hard_wall_profile_integrals(
        points,
        pion_mass=pion_mass,
        curvature=curvature,
    )
    _, wall_profile, wall_derivative = points[-1]
    lapse = static_patch_lapse(wall_radius, curvature)
    pressure = dimensionless_radial_pressure(
        wall_radius,
        wall_profile,
        wall_derivative,
        pion_mass=pion_mass,
        curvature=curvature,
    )
    mean_curvature = dimensionless_shell_mean_curvature(
        wall_radius,
        curvature=curvature,
    )
    positive_tension_supported = mean_curvature > 0.0 and pressure >= 0.0
    tension = pressure / mean_curvature if positive_tension_supported else float("nan")
    wall_mass = (
        4.0 * pi * wall_radius**2 * sqrt(lapse) * tension
        if positive_tension_supported
        else float("nan")
    )
    return {
        "pion_mass_mu": pion_mass,
        "curvature_lambda": curvature,
        "horizon_radius_x_c": (
            1.0 / sqrt(curvature) if curvature > 0.0 else float("inf")
        ),
        "wall_radius_x_w": wall_radius,
        "shooting_slope_b": slope,
        "wall_profile_F_w": wall_profile,
        "wall_profile_derivative_F_prime_w": wall_derivative,
        "minimum_profile_F": min(profile for _, profile, _ in points),
        "maximum_profile_F": max(profile for _, profile, _ in points),
        "maximum_profile_derivative_F_prime": max(
            derivative for _, _, derivative in points
        ),
        "profile_integrals": integrals,
        "dimensionless_interior_radial_pressure": pressure,
        "dimensionless_shell_mean_curvature": mean_curvature,
        "dimensionless_equilibrium_tension": tension,
        "dimensionless_wall_mass_c_M": wall_mass,
        "dimensionless_total_mass_c_M": (
            integrals["interior_dimensionless_mass_c_M"] + wall_mass
        ),
        "wall_to_interior_mass_ratio": (
            wall_mass / integrals["interior_dimensionless_mass_c_M"]
        ),
        "positive_tension_supported": positive_tension_supported,
        "positive_tension_radius_condition": (
            "x_w < sqrt(2/(3 lambda)) = sqrt(2/3) x_c"
        ),
        "force_balance_residual": (
            pressure - tension * mean_curvature
            if positive_tension_supported
            else float("nan")
        ),
    }


def massive_skyrmion_worldtube_certificate(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, object]:
    """Certify the centered ideal-mirror worldtube baseline."""
    record = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    refined = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step / 2.0,
    )
    integrals = record["profile_integrals"]
    refined_integrals = refined["profile_integrals"]
    certified_claims = {
        "hard_wall_enforces_unit_baryon_number": abs(
            integrals["baryon_number_integral"] - 1.0
        )
        < 2.0e-5
        and abs(integrals["baryon_number_from_wall_value"] - 1.0) < 1.0e-8,
        "profile_is_monotone_inside_the_wall": (
            record["maximum_profile_derivative_F_prime"] <= 1.0e-6
            and record["minimum_profile_F"] >= -1.0e-6
            and record["maximum_profile_F"] <= pi + 1.0e-6
            and abs(record["wall_profile_F_w"]) < 1.0e-7
        ),
        "positive_tension_centered_equilibrium_exists": record[
            "positive_tension_supported"
        ],
        "selected_equilibrium_tension_is_finite_and_positive": (
            isfinite(record["dimensionless_equilibrium_tension"])
            and record["dimensionless_equilibrium_tension"] > 0.0
        ),
        "wall_mass_is_subdominant_for_the_default_example": record[
            "wall_to_interior_mass_ratio"
        ]
        < 0.02,
        "profile_mass_and_inertia_are_step_stable": max(
            abs(
                refined_integrals["interior_dimensionless_mass_c_M"]
                / integrals["interior_dimensionless_mass_c_M"]
                - 1.0
            ),
            abs(
                refined_integrals["interior_dimensionless_inertia_c_I"]
                / integrals["interior_dimensionless_inertia_c_I"]
                - 1.0
            ),
        )
        < 1.0e-6,
    }
    return {
        "goal": "Centered Massive-Skyrmion Hard-Wall Worldtube Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "conditional_centered_membrane_supported_unit_baryon_source",
        "central_result": (
            "A covariant ideal-mirror spherical membrane gives an exact B=1 "
            "finite Skyrmion profile. For the declared centered fixed-background "
            "example, a positive Nambu-Goto tension satisfies Young-Laplace "
            "balance and its wall mass is subdominant."
        ),
        "boundary_action": (
            "Nambu-Goto membrane plus a covariant Lagrange multiplier imposing "
            "Y^A=(1,0,0,0), equivalently U=1, on the wall"
        ),
        "record": record,
        "certified_claims": certified_claims,
        "claim_boundary": (
            "The membrane tension is selected by centered force balance on a "
            "fixed de Sitter background. No radial/nonspherical stability, "
            "finite-stiffness UV completion, wall-mode gap, Einstein junction "
            "condition, off-center acceleration, or near-horizon support theorem "
            "is proved."
        ),
        "next_physics_gate": (
            "derive a finite-stiffness wall or top-form pressure completion, "
            "test wall/profile Hessian modes, and repeat the stress calculation "
            "for the off-center accelerated worldtube"
        ),
    }
