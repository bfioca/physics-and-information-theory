"""Operational tidal discriminator for fixed-spin rotational references.

For an infinitesimal Jacobi separation ``xi`` between neighboring freely
falling worldlines, the source-dependent initial geodesic-deviation signal is

``delta(ddot(xi)/xi)=-delta E_rr``.

The convention is signature ``(-+++)`` and ``E_ij=C_(i t j t)`` with the
repository Riemann sign, so ``D_tau^2 xi^i=-E^i_j xi^j``.

The module contracts the physical electric-Weyl tensor with an observation
direction and compares semiclassical expectation-value fields for two spin-two
states with identical Casimir and leading rotor energy but different
quadrupole tensors.
"""

from __future__ import annotations

from math import isfinite, sqrt

from .static_patch_l2_weyl_reconstruction import (
    physical_skyrmion_exterior_weyl_record,
)


Matrix3 = tuple[tuple[float, float, float], ...]
Vector3 = tuple[float, float, float]


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _weyl_tensor(tensor: Matrix3) -> Matrix3:
    if len(tensor) != 3 or any(len(row) != 3 for row in tensor):
        raise ValueError("radial_electric_weyl_tensor must be 3 by 3")
    matrix = tuple(tuple(float(value) for value in row) for row in tensor)
    if any(not isfinite(value) for row in matrix for value in row):
        raise ValueError("radial_electric_weyl_tensor entries must be finite")
    scale = max(1.0, max(abs(value) for row in matrix for value in row))
    tolerance = 1.0e-12 * scale
    if any(
        abs(matrix[row][column] - matrix[column][row]) > tolerance
        for row in range(3)
        for column in range(row)
    ):
        raise ValueError("radial_electric_weyl_tensor must be symmetric")
    if abs(sum(matrix[index][index] for index in range(3))) > tolerance:
        raise ValueError("radial_electric_weyl_tensor must be traceless")
    return matrix


def _unit_direction(direction: Vector3) -> Vector3:
    vector = tuple(float(value) for value in direction)
    if len(vector) != 3 or any(not isfinite(value) for value in vector):
        raise ValueError("observation_direction must have three finite entries")
    norm = sqrt(sum(value**2 for value in vector))
    if abs(norm - 1.0) > 1.0e-12:
        raise ValueError("observation_direction must be a unit vector")
    return vector


def radial_tidal_gradiometer_record(
    *,
    radial_electric_weyl_tensor: Matrix3,
    observation_direction: Vector3,
    physical_proof_mass_separation: float,
) -> dict[str, float | str]:
    """Return the instantaneous radial gradiometer signal in the Jacobi limit."""
    tensor = _weyl_tensor(radial_electric_weyl_tensor)
    direction = _unit_direction(observation_direction)
    separation = _positive(
        "physical_proof_mass_separation", physical_proof_mass_separation
    )
    tidal_curvature = sum(
        direction[row] * tensor[row][column] * direction[column]
        for row in range(3)
        for column in range(3)
    )
    fractional_acceleration = -tidal_curvature
    relative_acceleration = fractional_acceleration * separation
    return {
        "radial_electric_weyl_contraction": tidal_curvature,
        "fractional_relative_acceleration": fractional_acceleration,
        "physical_proof_mass_separation": separation,
        "linearized_relative_acceleration": relative_acceleration,
        "fractional_acceleration_dimension": "inverse_length_squared",
        "relative_acceleration_dimension": "inverse_length",
        "equation": "delta(ddot(xi)/xi)=-delta E_rr",
        "scope": (
            "Jacobi limit, first order in proof-mass separation, relative to "
            "pure de Sitter in natural units; no finite-time detector transfer "
            "function"
        ),
    }


def _pure_density(state: tuple[complex, ...]) -> tuple[tuple[complex, ...], ...]:
    return tuple(
        tuple(left * right.conjugate() for right in state) for left in state
    )


def spin_two_tidal_reference_discriminator_record(
    *,
    skyrme_coupling: float,
    pion_decay_constant: float,
    newton_constant: float,
    physical_proof_mass_separation: float,
    observation_radius: float = 5.0,
    observation_direction: Vector3 = (0.0, 0.0, 1.0),
    node_count: int = 401,
    maximum_slow_rotation: float | None = None,
) -> dict[str, object]:
    """Compare equal-leading-rotor-energy spin-two reference states."""
    direction = _unit_direction(observation_direction)
    separation = _positive(
        "physical_proof_mass_separation", physical_proof_mass_separation
    )
    radius = _positive("observation_radius", observation_radius)
    cat_density = _pure_density(
        (1.0 / sqrt(2.0), 0.0, 0.0, 0.0, 1.0 / sqrt(2.0))
    )
    anticoherent_density = _pure_density(
        (0.5, 0.0, 1.0j / sqrt(2.0), 0.0, 0.5)
    )
    common = {
        "skyrme_coupling": skyrme_coupling,
        "pion_decay_constant": pion_decay_constant,
        "newton_constant": newton_constant,
        "spin": 2.0,
        "node_count": node_count,
        "observation_radii": (radius,),
        "maximum_slow_rotation": maximum_slow_rotation,
    }
    cat = physical_skyrmion_exterior_weyl_record(
        **common,
        state_density_matrix=cat_density,
    )
    anticoherent = physical_skyrmion_exterior_weyl_record(
        **common,
        state_density_matrix=anticoherent_density,
    )
    cat_sample = cat["response_samples"][0]
    anticoherent_sample = anticoherent["response_samples"][0]
    cat_signal = radial_tidal_gradiometer_record(
        radial_electric_weyl_tensor=cat_sample[
            "physical_radial_electric_weyl_tensor_Err_ab"
        ],
        observation_direction=direction,
        physical_proof_mass_separation=separation,
    )
    anticoherent_signal = radial_tidal_gradiometer_record(
        radial_electric_weyl_tensor=anticoherent_sample[
            "physical_radial_electric_weyl_tensor_Err_ab"
        ],
        observation_direction=direction,
        physical_proof_mass_separation=separation,
    )
    cat_collective = cat["collective_state"]
    anticoherent_collective = anticoherent["collective_state"]
    # Recover I from the shared prefactors without duplicating the profile solve.
    physical_inertia = float(cat["physical_units"]["length_unit_L0"]) * (
        float(cat_collective["Qhat_over_QJ_factor"])
        ** (-0.5)
    )
    anticoherent_inertia = float(
        anticoherent["physical_units"]["length_unit_L0"]
    ) * (
        float(anticoherent_collective["Qhat_over_QJ_factor"])
        ** (-0.5)
    )
    rotor_energy = float(cat_collective["state_casimir_expectation_C"]) / (
        2.0 * physical_inertia
    )
    anticoherent_energy = float(
        anticoherent_collective["state_casimir_expectation_C"]
    ) / (2.0 * anticoherent_inertia)
    contrast = float(cat_signal["linearized_relative_acceleration"]) - float(
        anticoherent_signal["linearized_relative_acceleration"]
    )
    return {
        "observation_radius_x": radius,
        "observation_direction": direction,
        "physical_proof_mass_separation": separation,
        "shared_spin": 2.0,
        "shared_casimir_expectation": cat_collective[
            "state_casimir_expectation_C"
        ],
        "shared_physical_rotor_inertia": physical_inertia,
        "shared_leading_rigid_rotor_energy": rotor_energy,
        "spin_cat_quadrupole": cat_collective[
            "state_traceless_quadrupole_QJ_ab"
        ],
        "anticoherent_quadrupole": anticoherent_collective[
            "state_traceless_quadrupole_QJ_ab"
        ],
        "spin_cat_gradiometer": cat_signal,
        "anticoherent_gradiometer": anticoherent_signal,
        "linearized_relative_acceleration_contrast": contrast,
        "same_casimir_check": (
            cat_collective["state_casimir_expectation_C"]
            == anticoherent_collective["state_casimir_expectation_C"]
        ),
        "same_inertia_and_energy_check": (
            abs(physical_inertia - anticoherent_inertia)
            <= 1.0e-14 * max(1.0, physical_inertia)
            and abs(rotor_energy - anticoherent_energy)
            <= 1.0e-14 * max(1.0, rotor_energy)
        ),
        "observable_statement": (
            "Semiclassical mean fields of equal-Casimir, equal-leading-rotor-"
            "energy fixed-spin references can have different exterior tidal "
            "signals because gravity resolves <QJ_ab>, not Casimir alone."
        ),
        "claim_boundary": (
            "Instantaneous Jacobi-limit geodesic deviation on the "
            "fixed-background exterior branch. Finite-separation gradients, "
            "preparation, readout noise, finite interrogation time, Omega^4 "
            "energy, stress/metric fluctuations, single-shot quantum response, "
            "self-gravity, and tensorial Israel matching remain open."
        ),
    }
