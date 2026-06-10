"""Physical and collective normalization of the Skyrmion master response.

Natural units ``hbar=c=1`` are used.  The frozen response table is computed in
``x=e f_pi r`` with unit dimensionless Einstein coupling and per unit
``q_hat=(Omega_hat_a Omega_hat_b-delta_ab Omega_hat^2/3)n_a n_b``.  For the
rigid collective band,

``Omega_hat_a=e^2 J_a/c_I`` and ``kappa_hat=8 pi G f_pi^2``.

Consequently the physical master tensor is

``Psi_ab=(8 pi G e^3 f_pi/c_I^2) psi_0(x) Q^J_ab``.
"""

from __future__ import annotations

from math import isfinite, pi, sqrt

import numpy as np

from .centrifugal_skyrmion_master_response import (
    centrifugal_skyrmion_master_response_record,
)
from .massive_skyrmion_worldtube import hard_wall_equilibrium_record


Matrix3 = tuple[tuple[float, float, float], ...]


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _fixed_spin_second_moment(
    spin: float,
    state_density_matrix: object,
) -> tuple[Matrix3, float, tuple[float, ...]]:
    spin = float(spin)
    doubled_spin = round(2.0 * spin)
    if (
        not isfinite(spin)
        or spin < 0.0
        or abs(2.0 * spin - doubled_spin) > 1.0e-12
    ):
        raise ValueError("spin must be a nonnegative integer or half-integer")
    dimension = doubled_spin + 1
    density = np.asarray(state_density_matrix, dtype=complex)
    if density.shape != (dimension, dimension):
        raise ValueError("state_density_matrix has the wrong fixed-spin dimension")
    if not np.all(np.isfinite(density.real)) or not np.all(np.isfinite(density.imag)):
        raise ValueError("state_density_matrix entries must be finite")
    if float(np.max(np.abs(density - density.conj().T))) > 1.0e-12:
        raise ValueError("state_density_matrix must be Hermitian")
    trace = np.trace(density)
    if abs(float(trace.imag)) > 1.0e-12 or abs(float(trace.real) - 1.0) > 1.0e-12:
        raise ValueError("state_density_matrix must have unit trace")
    eigenvalues = np.linalg.eigvalsh(density)
    if float(eigenvalues[0]) < -1.0e-12:
        raise ValueError("state_density_matrix must be positive semidefinite")

    magnetic = np.linspace(-spin, spin, dimension)
    raising = np.zeros((dimension, dimension), dtype=complex)
    for index, value in enumerate(magnetic[:-1]):
        raising[index + 1, index] = sqrt(spin * (spin + 1.0) - value * (value + 1.0))
    lowering = raising.conj().T
    generators = (
        (raising + lowering) / 2.0,
        (raising - lowering) / (2.0j),
        np.diag(magnetic),
    )
    second = tuple(
        tuple(
            float(
                np.trace(
                    density
                    @ (
                        generators[row] @ generators[column]
                        + generators[column] @ generators[row]
                    )
                    / 2.0
                ).real
            )
            for column in range(3)
        )
        for row in range(3)
    )
    casimir = spin * (spin + 1.0)
    if abs(sum(second[index][index] for index in range(3)) - casimir) > 1.0e-10:
        raise AssertionError("fixed-spin generators failed the Casimir identity")
    return second, casimir, tuple(float(value) for value in eigenvalues)


def skyrme_physical_unit_record(
    *,
    skyrme_coupling: float,
    pion_decay_constant: float,
    newton_constant: float,
    pion_mass_mu: float,
    curvature_lambda: float,
    wall_radius: float,
) -> dict[str, float | str]:
    """Return the physical scales associated with one dimensionless model."""
    coupling = _positive("skyrme_coupling", skyrme_coupling)
    decay = _positive("pion_decay_constant", pion_decay_constant)
    newton = _positive("newton_constant", newton_constant)
    pion_mass = _positive("pion_mass_mu", pion_mass_mu)
    curvature = _positive("curvature_lambda", curvature_lambda)
    wall = _positive("wall_radius", wall_radius)
    inverse_length = coupling * decay
    length = 1.0 / inverse_length
    return {
        "skyrme_coupling_e": coupling,
        "pion_decay_constant_f_pi": decay,
        "newton_constant_G": newton,
        "inverse_length_scale_e_f_pi": inverse_length,
        "length_unit_L0": length,
        "bulk_stress_unit_T0": coupling**2 * decay**4,
        "membrane_tension_unit_sigma0": coupling * decay**3,
        "dimensionless_einstein_coupling_kappa_hat": 8.0 * pi * newton * decay**2,
        "physical_pion_mass": pion_mass * inverse_length,
        "physical_static_patch_radius": length / sqrt(curvature),
        "physical_wall_radius": wall * length,
        "convention": (
            "natural units; x=e f_pi r, tau=e f_pi t, "
            "kappa_hat=8 pi G f_pi^2"
        ),
    }


def collective_quadrupole_normalization_record(
    *,
    skyrme_coupling: float,
    inertia_constant: float,
    spin: float,
    state_density_matrix: object,
) -> dict[str, object]:
    """Compute a fixed-spin state's physical second moment and normalization."""
    coupling = _positive("skyrme_coupling", skyrme_coupling)
    inertia = _positive("inertia_constant", inertia_constant)
    second, casimir, density_spectrum = _fixed_spin_second_moment(
        spin, state_density_matrix
    )
    quadrupole = tuple(
        tuple(
            second[row][column] - (casimir / 3.0 if row == column else 0.0)
            for column in range(3)
        )
        for row in range(3)
    )
    quadrupole_norm_squared = sum(
        value**2 for row in quadrupole for value in row
    )
    if quadrupole_norm_squared <= 1.0e-24:
        quadrupole = ((0.0, 0.0, 0.0),) * 3
        quadrupole_norm_squared = 0.0
    conversion = coupling**4 / inertia**2
    dimensionless_quadrupole = tuple(
        tuple(conversion * value for value in row) for row in quadrupole
    )
    slow_rotation = coupling**2 * sqrt(casimir) / inertia
    return {
        "fixed_spin_j": float(spin),
        "state_density_matrix_spectrum": density_spectrum,
        "state_second_moment_S_ab": second,
        "state_casimir_expectation_C": casimir,
        "state_traceless_quadrupole_QJ_ab": quadrupole,
        "state_quadrupole_frobenius_norm_squared": quadrupole_norm_squared,
        "dimensionless_angular_velocity_quadrupole_Qhat_ab": (
            dimensionless_quadrupole
        ),
        "Qhat_over_QJ_factor": conversion,
        "slow_rotation_parameter_e_squared_sqrt_j_jplus1_over_c_I": slow_rotation,
        "leading_quadrupole_response_vanishes": quadrupole_norm_squared == 0.0,
        "quantization": (
            "Omega_hat=e^2 J/c_I; QJ_ab=<J_(a J_b)>-delta_ab<J^2>/3"
        ),
    }


def normalize_skyrmion_master_response(
    response: dict[str, object],
    *,
    skyrme_coupling: float,
    pion_decay_constant: float,
    newton_constant: float,
    inertia_constant: float,
    spin: float,
    state_density_matrix: object,
    maximum_slow_rotation: float | None = None,
) -> dict[str, object]:
    """Apply physical units and a collective state to a frozen response record."""
    parameters = response["parameters"]
    units = skyrme_physical_unit_record(
        skyrme_coupling=skyrme_coupling,
        pion_decay_constant=pion_decay_constant,
        newton_constant=newton_constant,
        pion_mass_mu=float(parameters["pion_mass_mu"]),
        curvature_lambda=float(parameters["curvature_lambda"]),
        wall_radius=float(parameters["wall_radius"]),
    )
    collective = collective_quadrupole_normalization_record(
        skyrme_coupling=skyrme_coupling,
        inertia_constant=inertia_constant,
        spin=spin,
        state_density_matrix=state_density_matrix,
    )
    if maximum_slow_rotation is not None:
        maximum = _positive("maximum_slow_rotation", maximum_slow_rotation)
        if (
            collective[
                "slow_rotation_parameter_e_squared_sqrt_j_jplus1_over_c_I"
            ]
            > maximum
        ):
            raise ValueError("state exceeds the declared slow-rotation budget")
    quadrupole = collective["state_traceless_quadrupole_QJ_ab"]
    norm_squared = float(collective["state_quadrupole_frobenius_norm_squared"])
    casimir = float(collective["state_casimir_expectation_C"])
    coupling = float(units["skyrme_coupling_e"])
    decay = float(units["pion_decay_constant_f_pi"])
    newton = float(units["newton_constant_G"])
    physical_prefactor = 8.0 * pi * newton * coupling**3 * decay / inertia_constant**2
    length = float(units["length_unit_L0"])
    samples = []
    for sample in response["response_samples"]:
        coefficient = float(sample["total_master_response_over_kappa"])
        tensor_prefactor = physical_prefactor * coefficient
        master_tensor = tuple(
            tuple(tensor_prefactor * value for value in row) for row in quadrupole
        )
        angular_integral = (
            tensor_prefactor**2 * 8.0 * pi * norm_squared / 15.0
        )
        angular_rms = abs(tensor_prefactor) * sqrt(2.0 * norm_squared / 15.0)
        physical_radius = float(sample["radius"]) * length
        samples.append(
            {
                "dimensionless_radius_x": sample["radius"],
                "physical_radius": physical_radius,
                "dimensionless_master_coefficient_psi0": coefficient,
                "physical_master_tensor_Psi_ab": master_tensor,
                "physical_master_angular_integral": angular_integral,
                "physical_master_angular_rms": angular_rms,
                "dimensionless_master_signal_rms_Psi_over_r": (
                    angular_rms / physical_radius
                ),
                "universal_pointwise_absolute_upper_bound": (
                    abs(tensor_prefactor) * 2.0 * casimir / 3.0
                ),
            }
        )
    return {
        "physical_units": units,
        "collective_state": collective,
        "inertia_constant_c_I": inertia_constant,
        "physical_rotor_inertia": (
            inertia_constant / (coupling**3 * decay)
        ),
        "physical_master_prefactor_per_psi0_and_QJ": physical_prefactor,
        "response_samples": tuple(samples),
        "normalization_identity": (
            "Psi_phys=(8 pi G e^3 f_pi/c_I^2) psi0(x) QJ_ab n_a n_b"
        ),
        "claim_boundary": (
            "Physical normalization of the frozen O(Omega^2), linear-gravity "
            "master amplitude. It is not an Israel-matched metric, a local "
            "Weyl observable, or a controlled collective-band truncation."
        ),
    }


def physical_skyrmion_master_response_record(
    *,
    skyrme_coupling: float,
    pion_decay_constant: float,
    newton_constant: float,
    spin: float,
    state_density_matrix: object,
    node_count: int = 401,
    origin_radius: float = 0.02,
    profile_step: float = 0.002,
    observation_radii: tuple[float, ...] = (1.0, 2.0, 3.0, 5.0, 10.0),
    maximum_slow_rotation: float | None = None,
) -> dict[str, object]:
    """Generate and physically normalize the completed default-model response."""
    response = centrifugal_skyrmion_master_response_record(
        node_count=node_count,
        origin_radius=origin_radius,
        profile_step=profile_step,
        observation_radii=observation_radii,
    )
    parameters = response["parameters"]
    worldtube = hard_wall_equilibrium_record(
        pion_mass=float(parameters["pion_mass_mu"]),
        curvature=float(parameters["curvature_lambda"]),
        wall_radius=float(parameters["wall_radius"]),
        step=float(parameters["profile_step"]),
    )
    inertia = float(
        worldtube["profile_integrals"]["interior_dimensionless_inertia_c_I"]
    )
    normalized = normalize_skyrmion_master_response(
        response,
        skyrme_coupling=skyrme_coupling,
        pion_decay_constant=pion_decay_constant,
        newton_constant=newton_constant,
        inertia_constant=inertia,
        spin=spin,
        state_density_matrix=state_density_matrix,
        maximum_slow_rotation=maximum_slow_rotation,
    )
    return {
        **normalized,
        "dimensionless_response_provenance": {
            "pion_mass_mu": parameters["pion_mass_mu"],
            "curvature_lambda": parameters["curvature_lambda"],
            "wall_radius": parameters["wall_radius"],
            "profile_step": parameters["profile_step"],
            "node_count": parameters["node_count"],
            "inertia_source": "same hard-wall background profile and action",
        },
    }
