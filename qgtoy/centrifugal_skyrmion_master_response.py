"""Exploratory Zerilli--Moncrief response of the completed Skyrmion source.

This module composes the floating centrifugal BVP, the same-action bulk stress,
the moving Nambu--Goto membrane distribution, the exact stress-to-master map,
and the fixed-de Sitter Green kernel.  Results are coefficients per unit
Einstein coupling and per quadratic rotational tensor ``q=Q_ab n_a n_b``.
"""

from __future__ import annotations

from math import cos, isfinite, sin, sqrt

import numpy as np

from .centrifugal_skyrmion_bvp import solve_centrifugal_quadrupole_bvp
from .centrifugal_skyrmion_completed_stress import (
    centrifugal_quadrupole_stress_amplitudes,
)
from .centrifugal_skyrmion_membrane_stress import (
    moving_interface_singular_amplitudes,
)
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile
from .static_patch_l2_master_source import (
    canonical_l2_master_source_distribution,
    contact_free_wall_response,
    static_l2_master_source_density,
)
from .static_patch_l2_response import static_patch_l2_green_kernel


def _positive(name: str, value: float) -> float:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _interpolate_profile(
    points: tuple[tuple[float, float, float], ...],
    radii: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    source_radius = np.asarray([point[0] for point in points])
    source_profile = np.asarray([point[1] for point in points])
    source_derivative = np.asarray([point[2] for point in points])
    return (
        np.interp(radii, source_radius, source_profile),
        np.interp(radii, source_radius, source_derivative),
    )


def _background_wall_stress(
    *,
    radius: float,
    lapse: float,
    profile: float,
    profile_derivative: float,
    pion_mass: float,
) -> tuple[float, float, float]:
    sine = sin(profile)
    radial_strain = lapse * profile_derivative**2
    tangential_strain = sine**2 / radius**2
    potential = pion_mass**2 * (1.0 - cos(profile)) / 4.0
    energy = (
        radial_strain / 8.0
        + tangential_strain / 4.0
        + radial_strain * tangential_strain
        + tangential_strain**2 / 2.0
        + potential
    )
    radial = (
        radial_strain / 8.0
        - tangential_strain / 4.0
        + radial_strain * tangential_strain
        - tangential_strain**2 / 2.0
        - potential
    )
    tangential = -radial_strain / 8.0 + tangential_strain**2 / 2.0 - potential
    return energy, radial, tangential


def centrifugal_skyrmion_master_response_record(
    *,
    node_count: int = 401,
    origin_radius: float = 0.02,
    profile_step: float = 0.002,
    observation_radii: tuple[float, ...] = (1.0, 2.0, 3.0, 5.0, 10.0),
) -> dict[str, object]:
    """Return the default bulk, shell, and total off-wall master response."""
    origin_radius = _positive("origin_radius", origin_radius)
    profile_step = _positive("profile_step", profile_step)
    if isinstance(node_count, bool) or not isinstance(node_count, int):
        raise ValueError("node_count must be an integer")
    if node_count < 5:
        raise ValueError("node_count must be at least five")
    solution = solve_centrifugal_quadrupole_bvp(
        node_count=node_count,
        origin_radius=origin_radius,
        profile_step=profile_step,
    )
    parameters = solution["parameters"]
    pion_mass = float(parameters["pion_mass_mu"])
    curvature = float(parameters["curvature_lambda"])
    wall_radius = float(parameters["wall_radius"])
    tension = float(parameters["membrane_tension"])
    patch_radius = 1.0 / sqrt(curvature)
    observations = tuple(
        _positive("observation_radius", value) for value in observation_radii
    )
    if any(value >= patch_radius for value in observations):
        raise ValueError("observation radii must lie strictly inside the patch")
    if any(value == wall_radius for value in observations):
        raise ValueError("off-wall response cannot be evaluated on the membrane")

    radii = np.asarray(solution["sample_radii"], dtype=float)
    radial_field = np.asarray(solution["radial_field_samples"], dtype=float)
    tangential_field = np.asarray(solution["tangential_field_samples"], dtype=float)
    radial_field_derivative = np.gradient(radial_field, radii, edge_order=2)
    tangential_field_derivative = np.gradient(tangential_field, radii, edge_order=2)
    _, profile_points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=profile_step,
    )
    profile, profile_derivative = _interpolate_profile(profile_points, radii)
    names = (
        "energy_density",
        "radial_pressure",
        "radial_angular_shear",
        "angular_tracefree_stress",
    )
    amplitudes = {name: np.zeros_like(radii) for name in names}
    for index, radius in enumerate(radii):
        stress = centrifugal_quadrupole_stress_amplitudes(
            radius=float(radius),
            metric_factor=1.0 - curvature * float(radius) ** 2,
            profile=float(profile[index]),
            profile_derivative=float(profile_derivative[index]),
            radial_field=float(radial_field[index]),
            radial_field_derivative=float(radial_field_derivative[index]),
            tangential_field=float(tangential_field[index]),
            tangential_field_derivative=float(tangential_field_derivative[index]),
            pion_mass=pion_mass,
        )
        for name in names:
            amplitudes[name][index] = float(stress[f"total_{name}"])
    energy_derivative = np.gradient(amplitudes["energy_density"], radii, edge_order=2)
    bulk_source = np.asarray(
        [
            static_l2_master_source_density(
                radius=float(radius),
                static_patch_radius=patch_radius,
                energy_density=float(amplitudes["energy_density"][index]),
                energy_density_derivative=float(energy_derivative[index]),
                radial_pressure=float(amplitudes["radial_pressure"][index]),
                radial_angular_shear=float(amplitudes["radial_angular_shear"][index]),
                angular_tracefree_stress=float(
                    amplitudes["angular_tracefree_stress"][index]
                ),
            )
            for index, radius in enumerate(radii)
        ]
    )

    lapse = 1.0 - curvature * wall_radius**2
    lapse_derivative = -2.0 * curvature * wall_radius
    wall_profile = float(profile[-1])
    wall_profile_derivative = float(profile_derivative[-1])
    background_energy, background_radial, background_tangential = (
        _background_wall_stress(
            radius=wall_radius,
            lapse=lapse,
            profile=wall_profile,
            profile_derivative=wall_profile_derivative,
            pion_mass=pion_mass,
        )
    )
    singular = moving_interface_singular_amplitudes(
        wall_radius=wall_radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_derivative,
        membrane_tension=tension,
        wall_displacement_coefficient=float(solution["wall_shape_coefficient"]),
        background_energy_density=background_energy,
        background_radial_pressure=background_radial,
        background_tangential_pressure=background_tangential,
    )
    master_distribution = canonical_l2_master_source_distribution(
        wall_radius=wall_radius,
        static_patch_radius=patch_radius,
        bulk_energy_density_at_wall=float(amplitudes["energy_density"][-1]),
        energy_density_delta=float(singular["energy_density_delta"]),
        energy_density_delta_prime=float(singular["energy_density_delta_prime"]),
        radial_pressure_delta=float(singular["radial_pressure_delta"]),
        radial_angular_shear_delta=float(singular["radial_angular_shear_delta"]),
    )

    response_samples = []
    for observation in observations:
        green_values = np.asarray(
            [
                static_patch_l2_green_kernel(
                    observation,
                    float(source_radius),
                    static_patch_radius=patch_radius,
                )
                for source_radius in radii
            ]
        )
        bulk_response = float(np.trapezoid(green_values * bulk_source, radii))
        wall_response = contact_free_wall_response(
            observation,
            wall_radius=wall_radius,
            static_patch_radius=patch_radius,
            contact_free_delta_coefficient=float(
                master_distribution["contact_free_delta_coefficient"]
            ),
            contact_free_delta_prime_coefficient=float(
                master_distribution["contact_free_delta_prime_coefficient"]
            ),
        )
        response_samples.append(
            {
                "radius": observation,
                "bulk_master_response_over_kappa": bulk_response,
                "wall_master_response_over_kappa": wall_response,
                "total_master_response_over_kappa": (bulk_response + wall_response),
            }
        )
    return {
        "parameters": {
            **parameters,
            "static_patch_radius": patch_radius,
        },
        "normalization": (
            "Psi coefficient per kappa=8pi G and per q=Q_ab n_a n_b; "
            "dimensionless Skyrme radius x and stress normalization"
        ),
        "master_source_distribution_over_kappa": master_distribution,
        "bulk_master_source_maximum_absolute": float(np.max(np.abs(bulk_source))),
        "bulk_master_source_l1_on_resolved_interval": float(
            np.trapezoid(np.abs(bulk_source), radii)
        ),
        "response_samples": tuple(response_samples),
        "claim_boundary": (
            "Floating fixed-background response with finite-difference bulk "
            "derivatives and a contact-subtracted ideal thin shell. The "
            "unresolved origin interval, interval validation, physical "
            "collective normalization, Israel matching, and invariant Weyl "
            "reconstruction remain open."
        ),
    }
