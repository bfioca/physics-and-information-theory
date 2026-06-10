"""Centered hard-wall radial stability and finite-pinning topology gate."""

from __future__ import annotations

from math import isfinite, pi, sqrt

from .massive_skyrmion_profile import static_patch_lapse
from .massive_skyrmion_worldtube import (
    dimensionless_radial_pressure,
    hard_wall_equilibrium_record,
    solve_hard_wall_skyrmion_profile,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def shell_mean_curvature_derivative(
    wall_radius: float,
    *,
    curvature: float,
) -> float:
    """Return ``dK_bar/dx_w`` for a centered static spherical shell."""
    _validate_positive("wall_radius", wall_radius)
    _validate_nonnegative("curvature", curvature)
    lapse = static_patch_lapse(wall_radius, curvature)
    if lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    root_lapse = sqrt(lapse)
    return (
        -2.0 * root_lapse / wall_radius**2
        - 3.0 * curvature / root_lapse
        - curvature**2 * wall_radius**2 / lapse**1.5
    )


def _dirichlet_branch_pressure(
    wall_radius: float,
    *,
    pion_mass: float,
    curvature: float,
    step: float,
) -> float:
    _, points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    _, wall_profile, wall_derivative = points[-1]
    return dimensionless_radial_pressure(
        wall_radius,
        wall_profile,
        wall_derivative,
        pion_mass=pion_mass,
        curvature=curvature,
    )


def centered_radial_stability_record(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
    radius_difference: float = 0.005,
) -> dict[str, float | bool | None]:
    """Audit the fixed-tension adiabatic spherical-radius energy curvature."""
    _validate_positive("pion_mass", pion_mass)
    _validate_nonnegative("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("step", step)
    _validate_positive("radius_difference", radius_difference)
    if wall_radius <= radius_difference:
        raise ValueError("radius_difference must be smaller than wall_radius")
    if static_patch_lapse(wall_radius + radius_difference, curvature) <= 0.0:
        raise ValueError("finite-difference branch must remain inside the horizon")

    equilibrium = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    pressure_minus = _dirichlet_branch_pressure(
        wall_radius - radius_difference,
        pion_mass=pion_mass,
        curvature=curvature,
        step=step,
    )
    pressure_plus = _dirichlet_branch_pressure(
        wall_radius + radius_difference,
        pion_mass=pion_mass,
        curvature=curvature,
        step=step,
    )
    pressure_derivative = (pressure_plus - pressure_minus) / (
        2.0 * radius_difference
    )
    tension = equilibrium["dimensionless_equilibrium_tension"]
    curvature_derivative = shell_mean_curvature_derivative(
        wall_radius,
        curvature=curvature,
    )
    energy_second_derivative = (
        4.0
        * pi
        * wall_radius**2
        * (-pressure_derivative + tension * curvature_derivative)
    )
    lapse = static_patch_lapse(wall_radius, curvature)
    wall_kinetic_mass = 4.0 * pi * tension * wall_radius**2 / lapse**1.5
    shell_only_frequency_squared = energy_second_derivative / wall_kinetic_mass
    shell_only_frequency = (
        sqrt(shell_only_frequency_squared)
        if shell_only_frequency_squared >= 0.0
        else None
    )
    return {
        "dimensionless_radial_pressure": equilibrium[
            "dimensionless_interior_radial_pressure"
        ],
        "dimensionless_equilibrium_tension": tension,
        "dimensionless_pressure_derivative_along_dirichlet_branch": (
            pressure_derivative
        ),
        "dimensionless_shell_mean_curvature_derivative": curvature_derivative,
        "dimensionless_energy_second_derivative_at_fixed_tension": (
            energy_second_derivative
        ),
        "dimensionless_wall_kinetic_mass": wall_kinetic_mass,
        "dimensionless_shell_only_frequency_squared": shell_only_frequency_squared,
        "dimensionless_shell_only_frequency": shell_only_frequency,
        "adiabatic_spherical_local_minimum": energy_second_derivative > 0.0,
    }


def finite_pinning_asymptotic_record(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, float | bool | str]:
    """Return large-stiffness coefficients for a cosine boundary pinning term."""
    equilibrium = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    derivative = equilibrium["wall_profile_derivative_F_prime_w"]
    lapse = static_patch_lapse(wall_radius, curvature)
    root_lapse = sqrt(lapse)
    boundary_profile_coefficient = -root_lapse * derivative / 4.0
    baryon_deficit_coefficient = (
        lapse**1.5 * abs(derivative) ** 3 / (96.0 * pi)
    )
    pinning_energy_coefficient = (
        pi * wall_radius**2 * lapse**1.5 * derivative**2 / 8.0
    )
    hard_wall_robin_derivative_term = (
        lapse * wall_radius**2 * derivative / 4.0
    )
    return {
        "hard_wall_derivative_F_prime_w": derivative,
        "hard_wall_robin_derivative_term_at_F_w_zero": (
            hard_wall_robin_derivative_term
        ),
        "boundary_profile_coefficient_in_inverse_stiffness": (
            boundary_profile_coefficient
        ),
        "baryon_deficit_coefficient_in_inverse_stiffness_cubed": (
            baryon_deficit_coefficient
        ),
        "pinning_energy_coefficient_in_inverse_stiffness": (
            pinning_energy_coefficient
        ),
        "total_soft_minus_hard_energy_coefficient_in_inverse_stiffness": (
            -pinning_energy_coefficient
        ),
        "finite_cosine_pinning_cannot_preserve_exact_unit_baryon_number": (
            abs(hard_wall_robin_derivative_term) > 0.0
        ),
        "reason": (
            "Exact B=1 requires F_w=0. The finite-stiffness Robin condition "
            "then also requires F'_w=0; uniqueness of the profile ODE gives "
            "the trivial solution, contradicting F(0)=pi."
        ),
    }


def skyrmion_worldtube_stability_certificate(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
    radius_difference: float = 0.005,
) -> dict[str, object]:
    """Certify the centered l=0 gate and simple finite-pinning no-go."""
    stability = centered_radial_stability_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        radius_difference=radius_difference,
    )
    refined_difference = radius_difference / 2.0
    refined = centered_radial_stability_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
        radius_difference=refined_difference,
    )
    pinning = finite_pinning_asymptotic_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    curvature_relative_change = abs(
        refined["dimensionless_energy_second_derivative_at_fixed_tension"]
        / stability["dimensionless_energy_second_derivative_at_fixed_tension"]
        - 1.0
    )
    certified_claims = {
        "young_laplace_point_is_a_local_minimum_along_the_relaxed_l0_branch": (
            stability["adiabatic_spherical_local_minimum"]
        ),
        "radial_energy_curvature_is_difference_stable": (
            curvature_relative_change < 1.0e-3
        ),
        "nambu_goto_wall_supplies_positive_radial_kinetic_mass": (
            stability["dimensionless_wall_kinetic_mass"] > 0.0
        ),
        "simple_finite_pinning_cannot_preserve_exact_B1": pinning[
            "finite_cosine_pinning_cannot_preserve_exact_unit_baryon_number"
        ],
        "large_stiffness_topology_defect_starts_at_cubic_order": (
            pinning[
                "baryon_deficit_coefficient_in_inverse_stiffness_cubed"
            ]
            > 0.0
        ),
    }
    return {
        "goal": "Centered Skyrmion Worldtube Stability And Pinning Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "conditional_l0_stability_plus_finite_pinning_no_go",
        "central_result": (
            "The default Young-Laplace solution is a converged local minimum "
            "along the re-solved centered spherical Dirichlet branch at fixed "
            "membrane tension. A smooth finite cosine pinning term cannot "
            "simultaneously preserve exact B=1 and a nontrivial profile."
        ),
        "profile": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius_x_w": wall_radius,
            "step": step,
            "radius_difference": radius_difference,
        },
        "radial_stability": stability,
        "refined_energy_second_derivative": refined[
            "dimensionless_energy_second_derivative_at_fixed_tension"
        ],
        "energy_curvature_relative_difference_change": curvature_relative_change,
        "finite_pinning": pinning,
        "certified_claims": certified_claims,
        "claim_boundary": (
            "The stability result is conditional on the fixed-background, "
            "centered, adiabatically re-solved l=0 Dirichlet family and fixed "
            "membrane tension. It is not a full coupled profile-wall spectrum, "
            "an l>=1 stability theorem, an off-center support construction, or "
            "an Einstein-Skyrme junction analysis. The topology no-go applies "
            "to the stated simple finite pinning potential; boundary topological "
            "degrees of freedom can evade it."
        ),
        "next_physics_gate": (
            "solve the coupled l=1 off-center matter-membrane-anchor system and "
            "test its current dipole, stress, and spectral stability"
        ),
    }
