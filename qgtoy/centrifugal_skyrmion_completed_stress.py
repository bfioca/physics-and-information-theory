"""Exploratory completed stress for the centrifugal Skyrmion quadrupole.

The static deformation fields ``(f,g)`` solve the two-channel variational
problem in ``centrifugal_skyrmion_bvp``.  This module takes their first
variation of the sigma-model plus Skyrme stress, adds the rigid rotational
quadrupole, and evaluates the exact static even-parity conservation identities.

The calculation is floating and finite-difference based.  It is intended to
test the same-action completion before a validated stress certificate.
"""

from __future__ import annotations

from math import cos, isfinite, sin

import numpy as np

from .centrifugal_skyrmion_bvp import solve_centrifugal_quadrupole_bvp
from .massive_skyrmion_profile import static_patch_lapse
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile
from .static_even_stress_conservation import (
    static_even_stress_conservation_residuals,
)


def _finite(name: str, value: float) -> float:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(name: str, value: float) -> float:
    value = _finite(name, value)
    if value <= 0.0:
        raise ValueError(f"{name} must be positive")
    return value


def centrifugal_quadrupole_stress_amplitudes(
    *,
    radius: float,
    metric_factor: float,
    profile: float,
    profile_derivative: float,
    radial_field: float,
    radial_field_derivative: float,
    tangential_field: float,
    tangential_field_derivative: float,
    pion_mass: float,
) -> dict[str, float | str]:
    """Return rigid, deformation, and total ``ell=2`` stress amplitudes.

    The amplitudes multiply ``q=Q_ab n_a n_b`` in the ``(-+++)`` mixed-stress
    convention used by the static conservation checker.  Dimensionless Skyrme
    units set ``e=f_pi=1``; the fields are coefficients per quadratic angular
    velocity tensor.
    """
    radius = _positive("radius", radius)
    metric_factor = _positive("metric_factor", metric_factor)
    profile = _finite("profile", profile)
    profile_derivative = _finite("profile_derivative", profile_derivative)
    radial_field = _finite("radial_field", radial_field)
    radial_field_derivative = _finite(
        "radial_field_derivative", radial_field_derivative
    )
    tangential_field = _finite("tangential_field", tangential_field)
    tangential_field_derivative = _finite(
        "tangential_field_derivative", tangential_field_derivative
    )
    pion_mass = _finite("pion_mass", pion_mass)
    if pion_mass < 0.0:
        raise ValueError("pion_mass must be nonnegative")

    sine = sin(profile)
    cosine = cos(profile)
    radius_squared = radius**2
    sine_squared = sine**2
    radial_strain_squared = metric_factor * profile_derivative**2
    tangential_strain_squared = sine_squared / radius_squared
    sigma_rotation = sine_squared / (8.0 * metric_factor)
    skyrme_rotation = sine_squared / (2.0 * metric_factor)

    rigid_energy = -(
        sigma_rotation
        + skyrme_rotation * (radial_strain_squared + tangential_strain_squared)
    )
    rigid_radial_pressure = -(
        sigma_rotation
        + skyrme_rotation * (tangential_strain_squared - radial_strain_squared)
    )
    rigid_tangential_pressure = -(
        sigma_rotation + skyrme_rotation * radial_strain_squared
    )
    rigid_tracefree = -(skyrme_rotation * tangential_strain_squared)

    radial_strain_variation = (
        2.0 * metric_factor * profile_derivative * radial_field_derivative
    )
    angular_strain_trace_variation = (
        2.0
        * sine
        / radius_squared
        * (2.0 * radial_field * cosine - 3.0 * tangential_field)
    )
    total_strain_trace_variation = (
        radial_strain_variation + angular_strain_trace_variation
    )
    deformation_energy = (
        total_strain_trace_variation / 8.0
        + tangential_strain_squared * radial_strain_variation
        + (radial_strain_squared + tangential_strain_squared)
        * angular_strain_trace_variation
        / 2.0
        + pion_mass**2 * radial_field * sine / 4.0
    )
    deformation_radial_pressure = (
        radial_strain_variation
        * (0.25 - radial_strain_squared + 2.0 * tangential_strain_squared)
        + radial_strain_squared * total_strain_trace_variation
        - deformation_energy
    )
    angular_isotropic_strain_variation = (
        sine / radius_squared * (2.0 * radial_field * cosine - 3.0 * tangential_field)
    )
    deformation_tangential_pressure = (
        (0.25 + radial_strain_squared) * angular_isotropic_strain_variation
        + tangential_strain_squared * total_strain_trace_variation
        - deformation_energy
    )
    deformation_tracefree = (
        (0.25 + radial_strain_squared) * sine * tangential_field / radius_squared
    )
    radial_angular_strain = sine * tangential_field_derivative + profile_derivative * (
        2.0 * radial_field - cosine * tangential_field
    )
    deformation_radial_angular = (
        metric_factor * radial_angular_strain * (0.25 + tangential_strain_squared) / 2.0
    )
    return {
        "rigid_energy_density": rigid_energy,
        "rigid_radial_pressure": rigid_radial_pressure,
        "rigid_tangential_pressure": rigid_tangential_pressure,
        "rigid_radial_angular_shear": 0.0,
        "rigid_angular_tracefree_stress": rigid_tracefree,
        "deformation_energy_density": deformation_energy,
        "deformation_radial_pressure": deformation_radial_pressure,
        "deformation_tangential_pressure": deformation_tangential_pressure,
        "deformation_radial_angular_shear": deformation_radial_angular,
        "deformation_angular_tracefree_stress": deformation_tracefree,
        "total_energy_density": rigid_energy + deformation_energy,
        "total_radial_pressure": (rigid_radial_pressure + deformation_radial_pressure),
        "total_tangential_pressure": (
            rigid_tangential_pressure + deformation_tangential_pressure
        ),
        "total_radial_angular_shear": deformation_radial_angular,
        "total_angular_tracefree_stress": (rigid_tracefree + deformation_tracefree),
        "convention": (
            "coefficients of q in delta T^t_t=-rho q, delta T^r_r=p_r q, "
            "delta T^r_A=j D_Aq, and delta T^A_B=p_perp q delta+pi Y^A_B"
        ),
    }


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


def centrifugal_quadrupole_conservation_residuals(
    *,
    radius: float,
    metric_factor: float,
    metric_factor_derivative: float,
    energy_density: float,
    radial_pressure: float,
    radial_pressure_derivative: float,
    tangential_pressure: float,
    radial_angular_shear: float,
    radial_angular_shear_derivative: float,
    angular_tracefree_stress: float,
) -> dict[str, float | bool | str]:
    """Apply the independently certified static-even gate at ``ell=2``."""
    return static_even_stress_conservation_residuals(
        ell=2,
        radius=radius,
        metric_factor=metric_factor,
        metric_factor_derivative=metric_factor_derivative,
        energy_density=energy_density,
        radial_pressure=radial_pressure,
        radial_pressure_derivative=radial_pressure_derivative,
        tangential_pressure=tangential_pressure,
        radial_angular_shear=radial_angular_shear,
        radial_angular_shear_derivative=radial_angular_shear_derivative,
        angular_tracefree_stress=angular_tracefree_stress,
    )


def completed_stress_conservation_record(
    *,
    node_count: int = 401,
    origin_radius: float = 0.02,
    profile_step: float = 0.002,
    interior_cutoff: float = 0.1,
) -> dict[str, object]:
    """Solve the default branch and audit its smooth-bulk conservation."""
    interior_cutoff = _positive("interior_cutoff", interior_cutoff)
    solution = solve_centrifugal_quadrupole_bvp(
        node_count=node_count,
        origin_radius=origin_radius,
        profile_step=profile_step,
    )
    parameters = solution["parameters"]
    pion_mass = float(parameters["pion_mass_mu"])
    curvature = float(parameters["curvature_lambda"])
    wall_radius = float(parameters["wall_radius"])
    if 2.0 * interior_cutoff >= wall_radius:
        raise ValueError("interior_cutoff leaves no audit interval")
    radii = np.asarray(solution["sample_radii"], dtype=float)
    radial_field = np.asarray(solution["radial_field_samples"], dtype=float)
    tangential_field = np.asarray(solution["tangential_field_samples"], dtype=float)
    radial_field_derivative = np.gradient(radial_field, radii, edge_order=2)
    tangential_field_derivative = np.gradient(tangential_field, radii, edge_order=2)
    _, points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=profile_step,
    )
    profile, profile_derivative = _interpolate_profile(points, radii)

    names = (
        "energy_density",
        "radial_pressure",
        "tangential_pressure",
        "radial_angular_shear",
        "angular_tracefree_stress",
    )
    rigid = {name: np.zeros_like(radii) for name in names}
    total = {name: np.zeros_like(radii) for name in names}
    for index, radius in enumerate(radii):
        record = centrifugal_quadrupole_stress_amplitudes(
            radius=float(radius),
            metric_factor=static_patch_lapse(float(radius), curvature),
            profile=float(profile[index]),
            profile_derivative=float(profile_derivative[index]),
            radial_field=float(radial_field[index]),
            radial_field_derivative=float(radial_field_derivative[index]),
            tangential_field=float(tangential_field[index]),
            tangential_field_derivative=float(tangential_field_derivative[index]),
            pion_mass=pion_mass,
        )
        for name in names:
            rigid[name][index] = float(record[f"rigid_{name}"])
            total[name][index] = float(record[f"total_{name}"])

    metric_factor = 1.0 - curvature * radii**2
    metric_derivative = -2.0 * curvature * radii

    def residuals(amplitudes: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
        radial_pressure_derivative = np.gradient(
            amplitudes["radial_pressure"], radii, edge_order=2
        )
        shear_derivative = np.gradient(
            amplitudes["radial_angular_shear"], radii, edge_order=2
        )
        radial = np.zeros_like(radii)
        angular = np.zeros_like(radii)
        for index, radius in enumerate(radii):
            record = centrifugal_quadrupole_conservation_residuals(
                radius=float(radius),
                metric_factor=float(metric_factor[index]),
                metric_factor_derivative=float(metric_derivative[index]),
                energy_density=float(amplitudes["energy_density"][index]),
                radial_pressure=float(amplitudes["radial_pressure"][index]),
                radial_pressure_derivative=float(radial_pressure_derivative[index]),
                tangential_pressure=float(amplitudes["tangential_pressure"][index]),
                radial_angular_shear=float(amplitudes["radial_angular_shear"][index]),
                radial_angular_shear_derivative=float(shear_derivative[index]),
                angular_tracefree_stress=float(
                    amplitudes["angular_tracefree_stress"][index]
                ),
            )
            radial[index] = float(record["radial_conservation_residual"])
            angular[index] = float(record["angular_conservation_residual"])
        return radial, angular

    rigid_radial, rigid_angular = residuals(rigid)
    total_radial, total_angular = residuals(total)
    mask = (radii >= interior_cutoff) & (radii <= wall_radius - interior_cutoff)

    def maximum(values: np.ndarray) -> float:
        return float(np.max(np.abs(values[mask])))

    rigid_maximum = max(maximum(rigid_radial), maximum(rigid_angular))
    total_maximum = max(maximum(total_radial), maximum(total_angular))
    return {
        "parameters": {
            **parameters,
            "interior_cutoff": interior_cutoff,
        },
        "rigid_radial_residual_maximum": maximum(rigid_radial),
        "rigid_angular_residual_maximum": maximum(rigid_angular),
        "completed_radial_residual_maximum": maximum(total_radial),
        "completed_angular_residual_maximum": maximum(total_angular),
        "rigid_combined_residual_maximum": rigid_maximum,
        "completed_combined_residual_maximum": total_maximum,
        "residual_reduction_factor": (
            total_maximum / rigid_maximum if rigid_maximum > 0.0 else None
        ),
        "bulk_conservation_is_numerically_improved": total_maximum < rigid_maximum,
        "sample_radii": tuple(float(value) for value in radii),
        "completed_radial_residual_samples": tuple(
            float(value) for value in total_radial
        ),
        "completed_angular_residual_samples": tuple(
            float(value) for value in total_angular
        ),
        "claim_boundary": (
            "Floating finite-difference stress reconstruction on the exploratory "
            "BVP solution. No interval enclosure, wall distribution, Israel "
            "junction, or master-source projection is included."
        ),
    }
