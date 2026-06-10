"""Conserved static quadrupole stress to Zerilli--Moncrief source.

Conventions are fixed by

``delta(G^mu_nu+Lambda delta^mu_nu)=kappa delta T^mu_nu``

on ``N=1-r^2/R^2`` and the Regge--Wheeler-gauge metric amplitudes

``h_tt=N H0 Y``, ``h_rr=H2 Y/N``, and ``h_AB=r^2 K Y gamma_AB``.

For ``ell=2`` the master field is

``Psi=r/3 [K+N(H2-r K')/2]``.

Direct elimination of the sourced linearized Einstein equations gives

``F=kappa[-r^2 N rho'/6+r(1+4r^2/R^2)rho/6-r p_r/2-j+2r pi]``

in ``[-(N Psi')'+6 Psi/r^2]=F``.  A moving thin membrane generally creates a
``delta''`` contact term in this literal metric-defined master source.  The
module also supplies the equivalent contact-subtracted source used for
off-wall Green-function observables.
"""

from __future__ import annotations

from math import isfinite, pi

from .static_patch_l2_response import (
    l2_center_regular_solution,
    l2_center_regular_solution_derivative,
    l2_horizon_regular_solution,
    l2_horizon_regular_solution_derivative,
    static_patch_l2_green_kernel,
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


def _geometry(radius: float, static_patch_radius: float) -> tuple[float, ...]:
    radius = _positive("radius", radius)
    patch_radius = _positive("static_patch_radius", static_patch_radius)
    if radius >= patch_radius:
        raise ValueError("radius must lie strictly inside the static patch")
    inverse_radius_squared = 1.0 / patch_radius**2
    lapse = 1.0 - radius**2 * inverse_radius_squared
    lapse_derivative = -2.0 * radius * inverse_radius_squared
    lapse_second_derivative = -2.0 * inverse_radius_squared
    return patch_radius, lapse, lapse_derivative, lapse_second_derivative


def traceless_quadrupole_harmonic_norm_squared(
    tensor_frobenius_norm_squared: float,
) -> float:
    """Return ``integral_S2 (Q_ab n_a n_b)^2 dOmega`` for traceless ``Q``."""
    norm_squared = _finite(
        "tensor_frobenius_norm_squared", tensor_frobenius_norm_squared
    )
    if norm_squared < 0.0:
        raise ValueError("tensor_frobenius_norm_squared must be nonnegative")
    return 8.0 * pi * norm_squared / 15.0


def l2_zerilli_moncrief_master(
    *,
    radius: float,
    static_patch_radius: float,
    angular_metric_amplitude: float,
    angular_metric_amplitude_derivative: float,
    radial_metric_amplitude: float,
) -> float:
    """Return the fixed Zerilli--Moncrief normalization for ``ell=2``."""
    _, lapse, _, _ = _geometry(radius, static_patch_radius)
    angular = _finite("angular_metric_amplitude", angular_metric_amplitude)
    angular_derivative = _finite(
        "angular_metric_amplitude_derivative",
        angular_metric_amplitude_derivative,
    )
    radial = _finite("radial_metric_amplitude", radial_metric_amplitude)
    return (
        radius * (angular + lapse * (radial - radius * angular_derivative) / 2.0) / 3.0
    )


def rw_metric_master_identity_record(
    *,
    radius: float,
    static_patch_radius: float,
    temporal_metric_amplitude: float,
    temporal_metric_amplitude_derivative: float,
    radial_metric_amplitude: float,
    radial_metric_amplitude_derivative: float,
    radial_metric_amplitude_second_derivative: float,
    angular_metric_amplitude: float,
    angular_metric_amplitude_derivative: float,
    angular_metric_amplitude_second_derivative: float,
    angular_metric_amplitude_third_derivative: float,
) -> dict[str, float | str]:
    """Audit the direct Regge--Wheeler-gauge Einstein elimination identity."""
    patch_radius, lapse, lapse_derivative, lapse_second_derivative = _geometry(
        radius, static_patch_radius
    )
    h0 = _finite("temporal_metric_amplitude", temporal_metric_amplitude)
    h0p = _finite(
        "temporal_metric_amplitude_derivative",
        temporal_metric_amplitude_derivative,
    )
    h2 = _finite("radial_metric_amplitude", radial_metric_amplitude)
    h2p = _finite(
        "radial_metric_amplitude_derivative",
        radial_metric_amplitude_derivative,
    )
    h2pp = _finite(
        "radial_metric_amplitude_second_derivative",
        radial_metric_amplitude_second_derivative,
    )
    angular = _finite("angular_metric_amplitude", angular_metric_amplitude)
    angular_p = _finite(
        "angular_metric_amplitude_derivative",
        angular_metric_amplitude_derivative,
    )
    angular_pp = _finite(
        "angular_metric_amplitude_second_derivative",
        angular_metric_amplitude_second_derivative,
    )
    angular_ppp = _finite(
        "angular_metric_amplitude_third_derivative",
        angular_metric_amplitude_third_derivative,
    )
    radius_ratio_squared = radius**2 / patch_radius**2
    coefficient_c = 3.0 - 4.0 * radius_ratio_squared
    coefficient_d = 4.0 - 3.0 * radius_ratio_squared
    coefficient_c_derivative = -8.0 * radius / patch_radius**2
    coefficient_d_derivative = -6.0 * radius / patch_radius**2
    einstein_tt = (
        lapse * angular_pp
        - lapse * h2p / radius
        + coefficient_c * angular_p / radius
        - coefficient_d * h2 / radius**2
        - 2.0 * angular / radius**2
    )
    einstein_tt_derivative = (
        lapse_derivative * angular_pp
        + lapse * angular_ppp
        - lapse_derivative * h2p / radius
        - lapse * h2pp / radius
        + lapse * h2p / radius**2
        + coefficient_c_derivative * angular_p / radius
        + coefficient_c * angular_pp / radius
        - coefficient_c * angular_p / radius**2
        - coefficient_d_derivative * h2 / radius**2
        - coefficient_d * h2p / radius**2
        + 2.0 * coefficient_d * h2 / radius**3
        - 2.0 * angular_p / radius**2
        + 4.0 * angular / radius**3
    )
    einstein_rr = (
        -lapse * h0p / radius
        + (1.0 - 2.0 * radius_ratio_squared) * angular_p / radius
        + 3.0 * h0 / radius**2
        + (-1.0 + 3.0 * radius_ratio_squared) * h2 / radius**2
        - 2.0 * angular / radius**2
    )
    einstein_radial_angular = lapse * (h0p - angular_p) / 2.0 + (
        -h0 + (1.0 - 2.0 * radius_ratio_squared) * h2
    ) / (2.0 * radius)
    einstein_tracefree = (h0 - h2) / (2.0 * radius**2)

    difference = h2 - radius * angular_p
    difference_p = h2p - angular_p - radius * angular_pp
    difference_pp = h2pp - 2.0 * angular_pp - radius * angular_ppp
    bracket = angular + lapse * difference / 2.0
    bracket_p = (
        angular_p + lapse_derivative * difference / 2.0 + lapse * difference_p / 2.0
    )
    bracket_pp = (
        angular_pp
        + lapse_second_derivative * difference / 2.0
        + lapse_derivative * difference_p
        + lapse * difference_pp / 2.0
    )
    master = radius * bracket / 3.0
    master_p = (bracket + radius * bracket_p) / 3.0
    master_pp = (2.0 * bracket_p + radius * bracket_pp) / 3.0
    master_operator = (
        -lapse_derivative * master_p - lapse * master_pp + 6.0 * master / radius**2
    )
    einstein_combination = (
        radius**2 * lapse * einstein_tt_derivative / 6.0
        - radius * (1.0 + 4.0 * radius_ratio_squared) * einstein_tt / 6.0
        - radius * einstein_rr / 2.0
        - einstein_radial_angular
        + 2.0 * radius * einstein_tracefree
    )
    return {
        "master_field": master,
        "master_operator": master_operator,
        "einstein_time_time_amplitude": einstein_tt,
        "einstein_time_time_amplitude_derivative": einstein_tt_derivative,
        "einstein_radial_pressure_amplitude": einstein_rr,
        "einstein_radial_angular_amplitude": einstein_radial_angular,
        "einstein_angular_tracefree_amplitude": einstein_tracefree,
        "einstein_source_combination": einstein_combination,
        "identity_residual": master_operator - einstein_combination,
        "identity": (
            "A2 Psi=(r^2 N/6)(delta G^t_t)'"
            "-r(1+4r^2/R^2)delta G^t_t/6"
            "-r delta G^r_r/2-delta G^r_A+2r delta G_TF"
        ),
    }


def static_l2_master_source_density(
    *,
    radius: float,
    static_patch_radius: float,
    energy_density: float,
    energy_density_derivative: float,
    radial_pressure: float,
    radial_angular_shear: float,
    angular_tracefree_stress: float,
    gravitational_coupling: float = 1.0,
) -> float:
    """Return the smooth Zerilli--Moncrief source density ``F``."""
    patch_radius, lapse, _, _ = _geometry(radius, static_patch_radius)
    energy = _finite("energy_density", energy_density)
    energy_derivative = _finite("energy_density_derivative", energy_density_derivative)
    radial = _finite("radial_pressure", radial_pressure)
    shear = _finite("radial_angular_shear", radial_angular_shear)
    tracefree = _finite("angular_tracefree_stress", angular_tracefree_stress)
    coupling = _positive("gravitational_coupling", gravitational_coupling)
    return coupling * (
        -(radius**2) * lapse * energy_derivative / 6.0
        + radius * (1.0 + 4.0 * radius**2 / patch_radius**2) * energy / 6.0
        - radius * radial / 2.0
        - shear
        + 2.0 * radius * tracefree
    )


def canonical_l2_master_source_distribution(
    *,
    wall_radius: float,
    static_patch_radius: float,
    bulk_energy_density_at_wall: float,
    energy_density_delta: float,
    energy_density_delta_prime: float,
    radial_pressure_delta: float,
    radial_angular_shear_delta: float,
    radial_pressure_delta_prime: float = 0.0,
    radial_angular_shear_delta_prime: float = 0.0,
    angular_tracefree_stress_delta: float = 0.0,
    angular_tracefree_stress_delta_prime: float = 0.0,
    gravitational_coupling: float = 1.0,
) -> dict[str, float | str]:
    """Map canonical stress ``delta`` jets to the literal master source.

    ``energy_density_delta_prime`` multiplies ``delta'(r-a)``.  The output can
    contain ``delta''`` because the metric-defined master field contains a
    source contact term for an infinitesimally thin displaced shell.
    """
    patch_radius, lapse, lapse_p, lapse_pp = _geometry(wall_radius, static_patch_radius)
    wall_energy = _finite("bulk_energy_density_at_wall", bulk_energy_density_at_wall)
    rho_delta = _finite("energy_density_delta", energy_density_delta)
    rho_delta_p = _finite("energy_density_delta_prime", energy_density_delta_prime)
    pressure_delta = _finite("radial_pressure_delta", radial_pressure_delta)
    pressure_delta_p = _finite(
        "radial_pressure_delta_prime", radial_pressure_delta_prime
    )
    shear_delta = _finite("radial_angular_shear_delta", radial_angular_shear_delta)
    shear_delta_p = _finite(
        "radial_angular_shear_delta_prime",
        radial_angular_shear_delta_prime,
    )
    tracefree_delta = _finite(
        "angular_tracefree_stress_delta", angular_tracefree_stress_delta
    )
    tracefree_delta_p = _finite(
        "angular_tracefree_stress_delta_prime",
        angular_tracefree_stress_delta_prime,
    )
    coupling = _positive("gravitational_coupling", gravitational_coupling)
    radius = wall_radius
    coefficient_a = radius**2 * lapse / 6.0
    coefficient_a_p = radius * lapse / 3.0 + radius**2 * lapse_p / 6.0
    coefficient_a_pp = (
        lapse / 3.0 + 2.0 * radius * lapse_p / 3.0 + radius**2 * lapse_pp / 6.0
    )
    coefficient_b = radius * (1.0 + 4.0 * radius**2 / patch_radius**2) / 6.0
    coefficient_b_p = (1.0 + 12.0 * radius**2 / patch_radius**2) / 6.0
    delta_second = coupling * (-coefficient_a * rho_delta_p)
    delta_prime = coupling * (
        -coefficient_a * rho_delta
        + 2.0 * coefficient_a_p * rho_delta_p
        + coefficient_b * rho_delta_p
        - radius * pressure_delta_p / 2.0
        - shear_delta_p
        + 2.0 * radius * tracefree_delta_p
    )
    delta = coupling * (
        coefficient_a * wall_energy
        + coefficient_a_p * rho_delta
        - coefficient_a_pp * rho_delta_p
        + coefficient_b * rho_delta
        - coefficient_b_p * rho_delta_p
        - radius * pressure_delta / 2.0
        + pressure_delta_p / 2.0
        - shear_delta
        + 2.0 * radius * tracefree_delta
        - 2.0 * tracefree_delta_p
    )
    potential = 6.0 / radius**2
    contact_coefficient = -delta_second / lapse
    contact_free_delta_prime = delta_prime + delta_second * lapse_p / lapse
    contact_free_delta = delta + potential * delta_second / lapse
    return {
        "master_source_delta_second_coefficient": delta_second,
        "master_source_delta_prime_coefficient": delta_prime,
        "master_source_delta_coefficient": delta,
        "master_field_contact_delta_coefficient": contact_coefficient,
        "contact_free_delta_prime_coefficient": contact_free_delta_prime,
        "contact_free_delta_coefficient": contact_free_delta,
        "contact_free_delta_second_coefficient": 0.0,
        "contact_definition": (
            "Psi=Psi_offwall+contact*delta(r-a); subtract A2(contact*delta) "
            "from F to obtain the contact-free source"
        ),
    }


def static_patch_l2_green_source_derivative(
    radius: float,
    source_radius: float,
    *,
    static_patch_radius: float,
) -> float:
    """Return ``partial G_2(r,s)/partial s`` away from ``r=s``."""
    _geometry(radius, static_patch_radius)
    _geometry(source_radius, static_patch_radius)
    if radius == source_radius:
        raise ValueError("source derivative requires radius != source_radius")
    radius_ratio = radius / static_patch_radius
    source_ratio = source_radius / static_patch_radius
    if radius < source_radius:
        return (
            2.0
            / 15.0
            * l2_center_regular_solution(radius_ratio)
            * l2_horizon_regular_solution_derivative(source_ratio)
        )
    return (
        2.0
        / 15.0
        * l2_center_regular_solution_derivative(source_ratio)
        * l2_horizon_regular_solution(radius_ratio)
    )


def contact_free_wall_response(
    radius: float,
    *,
    wall_radius: float,
    static_patch_radius: float,
    contact_free_delta_coefficient: float,
    contact_free_delta_prime_coefficient: float,
) -> float:
    """Return the shell-jet contribution to ``Psi`` away from the wall."""
    delta = _finite("contact_free_delta_coefficient", contact_free_delta_coefficient)
    delta_prime = _finite(
        "contact_free_delta_prime_coefficient",
        contact_free_delta_prime_coefficient,
    )
    green = static_patch_l2_green_kernel(
        radius,
        wall_radius,
        static_patch_radius=static_patch_radius,
    )
    green_derivative = static_patch_l2_green_source_derivative(
        radius,
        wall_radius,
        static_patch_radius=static_patch_radius,
    )
    return delta * green - delta_prime * green_derivative
