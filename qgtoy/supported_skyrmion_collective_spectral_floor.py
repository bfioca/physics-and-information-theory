"""Uniform collective-sector floors for hard-supported Skyrme hedgehogs.

The static hedgehog mass and inertia densities imply, pointwise and for every
profile inside a radius-``a`` worldtube,

    I <= [4/(3 N_w)] M a^2,

where ``N_w`` is the minimum static-patch lapse on the support.  Combining this
with ``E_j=M+j(j+1)/(2I)`` and AM-GM gives a profile-uniform sector floor

    E_j >= sqrt(3 N_w j(j+1)/2) / a.

This is an adiabatic collective-coordinate theorem.  It does not control
noncollective rotating field modes or collective-band projection errors.
"""

from __future__ import annotations

from math import exp, expm1, isfinite, log, log1p, pi, sqrt

from .global_so3_reference_risk import (
    asymmetry_orientation_risk_lower_bound,
)
from .massive_skyrmion_profile import (
    dimensionless_inertia_density,
    reduced_energy_density,
    static_patch_lapse,
)
from .massive_skyrmion_worldtube import hard_wall_equilibrium_record


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def supported_hedgehog_inertia_coefficient(
    *,
    wall_radius: float,
    curvature: float,
) -> float:
    """Return ``kappa=4/(3N_w)`` in ``I<=kappa M a^2``."""
    _validate_positive("wall_radius", wall_radius)
    _validate_nonnegative("curvature", curvature)
    wall_lapse = static_patch_lapse(wall_radius, curvature)
    if wall_lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")
    return 4.0 / (3.0 * wall_lapse)


def supported_hedgehog_linear_spin_energy_slope(
    *,
    physical_support_radius: float,
    wall_lapse: float,
) -> float:
    """Return ``sqrt(3N_w/2)/a`` in ``E_j>=s sqrt(j(j+1))``."""
    _validate_positive("physical_support_radius", physical_support_radius)
    _validate_positive("wall_lapse", wall_lapse)
    if wall_lapse > 1.0:
        raise ValueError("wall_lapse must be at most one")
    return sqrt(1.5 * wall_lapse) / physical_support_radius


def supported_hedgehog_sector_energy_floor(
    spin: float,
    *,
    physical_support_radius: float,
    wall_lapse: float,
) -> float:
    """Return the profile-relaxed collective total-energy floor at spin ``j``."""
    _validate_nonnegative("spin", spin)
    slope = supported_hedgehog_linear_spin_energy_slope(
        physical_support_radius=physical_support_radius,
        wall_lapse=wall_lapse,
    )
    return slope * sqrt(spin * (spin + 1.0))


def supported_hedgehog_density_bound_slack(
    dimensionless_radius: float,
    profile: float,
    profile_derivative: float,
    *,
    pion_mass: float,
    curvature: float,
    wall_radius: float,
) -> float:
    """Evaluate the pointwise slack proving ``c_I<=kappa x_w^2 c_M``."""
    _validate_positive("dimensionless_radius", dimensionless_radius)
    if dimensionless_radius > wall_radius:
        raise ValueError("dimensionless_radius must not exceed wall_radius")
    coefficient = supported_hedgehog_inertia_coefficient(
        wall_radius=wall_radius,
        curvature=curvature,
    )
    mass_density = 4.0 * pi * reduced_energy_density(
        dimensionless_radius,
        profile,
        profile_derivative,
        pion_mass=pion_mass,
        curvature=curvature,
    )
    inertia_density = dimensionless_inertia_density(
        dimensionless_radius,
        profile,
        profile_derivative,
        curvature=curvature,
    )
    return coefficient * wall_radius**2 * mass_density - inertia_density


def linear_sector_log_partition_upper_bound(
    *,
    dual_parameter: float,
    physical_support_radius: float,
    wall_lapse: float,
    projective: bool = False,
) -> float:
    """Bound the rotational log partition using ``E_j>=s j``.

    Integer sectors use ``j=0,1,...``.  Projective sectors use
    ``j=1/2,3/2,...`` and remain center blind at the density-operator level.
    """
    _validate_positive("dual_parameter", dual_parameter)
    slope = supported_hedgehog_linear_spin_energy_slope(
        physical_support_radius=physical_support_radius,
        wall_lapse=wall_lapse,
    )
    scaled_dual = dual_parameter * slope
    x = exp(-scaled_dual)
    log_one_minus_x = log(-expm1(-scaled_dual))
    if projective:
        return (
            log(4.0)
            - 0.5 * scaled_dual
            + log1p(x)
            - 3.0 * log_one_minus_x
        )
    return log(1.0 + 6.0 * x + x * x) - 3.0 * log_one_minus_x


def supported_hedgehog_orientation_risk_lower_bound(
    *,
    mean_total_energy: float,
    dual_parameter: float,
    physical_support_radius: float,
    wall_lapse: float,
    projective: bool = False,
) -> float:
    """Apply the spectral Gibbs theorem to the supported collective family."""
    _validate_nonnegative("mean_total_energy", mean_total_energy)
    log_partition_upper = linear_sector_log_partition_upper_bound(
        dual_parameter=dual_parameter,
        physical_support_radius=physical_support_radius,
        wall_lapse=wall_lapse,
        projective=projective,
    )
    asymmetry_capacity = dual_parameter * mean_total_energy + log_partition_upper
    return asymmetry_orientation_risk_lower_bound(asymmetry_capacity)


def supported_hedgehog_high_spin_tail_upper_bound(
    *,
    mean_total_energy: float,
    reference_cutoff: int,
    physical_support_radius: float,
    wall_lapse: float,
    projective: bool = False,
) -> float:
    """Markov-bound the first sector beyond an integer cutoff index."""
    _validate_nonnegative("mean_total_energy", mean_total_energy)
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    first_excluded_spin = reference_cutoff + (1.5 if projective else 1.0)
    floor = supported_hedgehog_sector_energy_floor(
        first_excluded_spin,
        physical_support_radius=physical_support_radius,
        wall_lapse=wall_lapse,
    )
    return min(1.0, mean_total_energy / floor)


def supported_skyrmion_collective_spectral_floor_certificate(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
    skyrme_coupling: float = 1.0,
    pion_decay_constant: float = 1.0,
    energy_multiplier: float = 1.1,
    dual_parameter: float = 0.1,
) -> dict[str, object]:
    """Audit the uniform collective-sector floor on the supported baseline."""
    _validate_positive("skyrme_coupling", skyrme_coupling)
    _validate_positive("pion_decay_constant", pion_decay_constant)
    _validate_positive("energy_multiplier", energy_multiplier)
    record = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    wall_lapse = static_patch_lapse(wall_radius, curvature)
    coefficient = supported_hedgehog_inertia_coefficient(
        wall_radius=wall_radius,
        curvature=curvature,
    )
    physical_radius = wall_radius / (skyrme_coupling * pion_decay_constant)
    mass = (
        float(record["dimensionless_total_mass_c_M"])
        * pion_decay_constant
        / skyrme_coupling
    )
    inertia = (
        float(
            record["profile_integrals"]["interior_dimensionless_inertia_c_I"]
        )
        / (skyrme_coupling**3 * pion_decay_constant)
    )
    mean_energy = energy_multiplier * mass
    projective_risk = supported_hedgehog_orientation_risk_lower_bound(
        mean_total_energy=mean_energy,
        dual_parameter=dual_parameter,
        physical_support_radius=physical_radius,
        wall_lapse=wall_lapse,
        projective=True,
    )
    sampled_spins = (0.5, 1.5, 5.5, 20.5, 100.5, 500.5)
    floors = tuple(
        {
            "spin": spin,
            "total_energy_floor": supported_hedgehog_sector_energy_floor(
                spin,
                physical_support_radius=physical_radius,
                wall_lapse=wall_lapse,
            ),
        }
        for spin in sampled_spins
    )
    inertia_ratio = inertia / (mass * physical_radius**2)
    claims = {
        "certified_profile_respects_uniform_inertia_mass_radius_bound": (
            inertia_ratio <= coefficient
        ),
        "sector_floors_are_positive_and_increasing": all(
            right["total_energy_floor"] > left["total_energy_floor"]
            for left, right in zip(floors, floors[1:])
        ),
        "linear_partition_upper_bound_is_finite": isfinite(
            linear_sector_log_partition_upper_bound(
                dual_parameter=dual_parameter,
                physical_support_radius=physical_radius,
                wall_lapse=wall_lapse,
                projective=True,
            )
        ),
        "projective_global_risk_floor_is_strictly_positive": projective_risk > 0.0,
    }
    return {
        "goal": "Supported Skyrmion Collective Spectral Floor",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "profile_uniform_adiabatic_collective_sector_energy_floor",
        "central_result": (
            "For every hard-supported hedgehog profile, the Skyrme densities "
            "give I<=[4/(3N_w)]Ma^2. Therefore adiabatic collective sectors "
            "obey E_j>=sqrt(3N_w j(j+1)/2)/a even after profile relaxation."
        ),
        "parameters": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius_x_w": wall_radius,
            "wall_lapse_N_w": wall_lapse,
            "skyrme_coupling_e": skyrme_coupling,
            "pion_decay_constant_f_pi": pion_decay_constant,
            "dual_parameter_beta": dual_parameter,
        },
        "physical_baseline": {
            "support_radius": physical_radius,
            "total_static_mass": mass,
            "collective_inertia": inertia,
            "actual_inertia_over_mass_radius_squared": inertia_ratio,
            "uniform_ratio_upper_bound": coefficient,
            "mean_total_energy_for_risk_audit": mean_energy,
        },
        "sampled_projective_sector_floors": floors,
        "projective_orientation_risk_lower_bound": projective_risk,
        "certified_claims": claims,
        "claim_boundary": (
            "The theorem is uniform over hard-supported hedgehog profile "
            "relaxation inside the adiabatic collective-coordinate family. It "
            "does not prove that this family exhausts the full field-theory "
            "spin sectors, control noncollective modes or band projection, "
            "establish coherent isospin access, or derive the wall, metric, "
            "readout, and lifetime from one finite-coupling action."
        ),
    }
