"""Floating primal-adjoint feasibility for the exterior master amplitude.

The centrifugal matter form is symmetric.  On one piecewise-linear Galerkin
space write its matrix equation as ``K y = ell`` and the exterior static-patch
master amplitude as

``J(y) = J_rigid + B(y) = J_rigid + b.T @ y``.

This module constructs ``b`` by applying the existing completed-stress and
Zerilli source pipeline to the Galerkin basis, solves ``K z = b``, and tests a
dual-weighted residual estimate after lifting a coarse primal/adjoint pair to a
nested fine space.  The resulting product bound is an exact floating-point
identity for the assembled fine system, but it is not an interval enclosure of
the continuum problem.
"""

from __future__ import annotations

from math import cos, isfinite, sin, sqrt

import numpy as np

from .centrifugal_skyrmion_completed_stress import (
    centrifugal_quadrupole_stress_amplitudes,
)
from .centrifugal_skyrmion_membrane_stress import (
    moving_interface_singular_amplitudes,
)
from .centrifugal_skyrmion_variational import (
    assemble_centrifugal_quadrupole_variational_system,
)
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile
from .static_patch_l2_master_source import (
    canonical_l2_master_source_distribution,
    static_l2_master_source_density,
)
from .static_patch_l2_response import (
    l2_center_regular_solution,
    l2_center_regular_solution_derivative,
)


def _integer_at_least(name: str, value: int, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer at least {minimum}")
    return value


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _fields_from_vector(
    vector: np.ndarray,
    degree_of_freedom_map: np.ndarray,
) -> np.ndarray:
    fields = np.zeros(degree_of_freedom_map.shape, dtype=float)
    for node in range(degree_of_freedom_map.shape[0]):
        for component in range(2):
            index = int(degree_of_freedom_map[node, component])
            if index >= 0:
                fields[node, component] = float(vector[index])
    return fields


def _vector_from_fields(
    fields: np.ndarray,
    degree_of_freedom_map: np.ndarray,
) -> np.ndarray:
    dimension = int(np.max(degree_of_freedom_map)) + 1
    vector = np.zeros(dimension, dtype=float)
    for node in range(degree_of_freedom_map.shape[0]):
        for component in range(2):
            index = int(degree_of_freedom_map[node, component])
            if index >= 0:
                vector[index] = float(fields[node, component])
    return vector


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


class _ExteriorAmplitudeFunctional:
    """Affine exterior-amplitude functional on one assembled FE space."""

    def __init__(self, assembled: dict[str, object]) -> None:
        parameters = assembled["parameters"]
        self.radii = np.asarray(assembled["radii"], dtype=float)
        self.dof_map = np.asarray(assembled["degree_of_freedom_map"], dtype=int)
        self.pion_mass = float(parameters["pion_mass_mu"])
        self.curvature = _positive(
            "curvature_lambda", float(parameters["curvature_lambda"])
        )
        self.wall_radius = float(parameters["wall_radius"])
        self.membrane_tension = float(parameters["membrane_tension"])
        self.patch_radius = 1.0 / sqrt(self.curvature)
        self.wall_profile_derivative = float(assembled["wall_profile_derivative"])
        self.wall_displacement_per_f = -1.0 / self.wall_profile_derivative

        _, points = solve_hard_wall_skyrmion_profile(
            pion_mass=self.pion_mass,
            curvature=self.curvature,
            wall_radius=self.wall_radius,
            step=float(parameters["profile_step"]),
        )
        profile_radii = np.asarray([point[0] for point in points], dtype=float)
        profile_values = np.asarray([point[1] for point in points], dtype=float)
        profile_derivatives = np.asarray([point[2] for point in points], dtype=float)
        self.profile = np.interp(self.radii, profile_radii, profile_values)
        self.profile_derivative = np.interp(
            self.radii, profile_radii, profile_derivatives
        )

    def evaluate(self, vector: np.ndarray) -> float:
        """Return the horizon-regular exterior amplitude per unit kappa."""
        fields = _fields_from_vector(np.asarray(vector, dtype=float), self.dof_map)
        radial_derivative = np.gradient(fields[:, 0], self.radii, edge_order=2)
        tangential_derivative = np.gradient(fields[:, 1], self.radii, edge_order=2)

        # The r=0 stress formulas contain removable radius denominators.  As in
        # the exploratory master-response module, omit the unresolved first
        # interval and expose that omission in the claim boundary.
        active = np.arange(1, len(self.radii))
        radii = self.radii[active]
        names = (
            "energy_density",
            "radial_pressure",
            "radial_angular_shear",
            "angular_tracefree_stress",
        )
        amplitudes = {name: np.zeros(len(active), dtype=float) for name in names}
        for local, index in enumerate(active):
            radius = float(self.radii[index])
            stress = centrifugal_quadrupole_stress_amplitudes(
                radius=radius,
                metric_factor=1.0 - self.curvature * radius**2,
                profile=float(self.profile[index]),
                profile_derivative=float(self.profile_derivative[index]),
                radial_field=float(fields[index, 0]),
                radial_field_derivative=float(radial_derivative[index]),
                tangential_field=float(fields[index, 1]),
                tangential_field_derivative=float(tangential_derivative[index]),
                pion_mass=self.pion_mass,
            )
            for name in names:
                amplitudes[name][local] = float(stress[f"total_{name}"])

        energy_derivative = np.gradient(
            amplitudes["energy_density"], radii, edge_order=2
        )
        bulk_source = np.asarray(
            [
                static_l2_master_source_density(
                    radius=float(radius),
                    static_patch_radius=self.patch_radius,
                    energy_density=float(amplitudes["energy_density"][index]),
                    energy_density_derivative=float(energy_derivative[index]),
                    radial_pressure=float(amplitudes["radial_pressure"][index]),
                    radial_angular_shear=float(
                        amplitudes["radial_angular_shear"][index]
                    ),
                    angular_tracefree_stress=float(
                        amplitudes["angular_tracefree_stress"][index]
                    ),
                )
                for index, radius in enumerate(radii)
            ],
            dtype=float,
        )
        regular = np.asarray(
            [
                l2_center_regular_solution(float(radius) / self.patch_radius)
                for radius in radii
            ],
            dtype=float,
        )
        bulk_amplitude = float(
            np.trapezoid(
                2.0 * self.patch_radius * regular * bulk_source / 15.0,
                radii,
            )
        )

        lapse = 1.0 - self.curvature * self.wall_radius**2
        lapse_derivative = -2.0 * self.curvature * self.wall_radius
        background = _background_wall_stress(
            radius=self.wall_radius,
            lapse=lapse,
            profile=float(self.profile[-1]),
            profile_derivative=float(self.profile_derivative[-1]),
            pion_mass=self.pion_mass,
        )
        displacement = self.wall_displacement_per_f * float(fields[-1, 0])
        singular = moving_interface_singular_amplitudes(
            wall_radius=self.wall_radius,
            wall_metric_factor=lapse,
            wall_metric_factor_derivative=lapse_derivative,
            membrane_tension=self.membrane_tension,
            wall_displacement_coefficient=displacement,
            background_energy_density=background[0],
            background_radial_pressure=background[1],
            background_tangential_pressure=background[2],
        )
        distribution = canonical_l2_master_source_distribution(
            wall_radius=self.wall_radius,
            static_patch_radius=self.patch_radius,
            bulk_energy_density_at_wall=float(amplitudes["energy_density"][-1]),
            energy_density_delta=float(singular["energy_density_delta"]),
            energy_density_delta_prime=float(
                singular["energy_density_delta_prime"]
            ),
            radial_pressure_delta=float(singular["radial_pressure_delta"]),
            radial_angular_shear_delta=float(
                singular["radial_angular_shear_delta"]
            ),
        )
        ratio = self.wall_radius / self.patch_radius
        center = l2_center_regular_solution(ratio)
        center_derivative = l2_center_regular_solution_derivative(ratio)
        shell_amplitude = (
            float(distribution["contact_free_delta_coefficient"])
            * 2.0
            * self.patch_radius
            * center
            / 15.0
            - float(distribution["contact_free_delta_prime_coefficient"])
            * 2.0
            * center_derivative
            / 15.0
        )
        return bulk_amplitude + shell_amplitude

    def affine_data(self) -> tuple[float, np.ndarray, float]:
        """Return ``J_rigid``, the vector representing ``B``, and a defect."""
        dimension = int(np.max(self.dof_map)) + 1
        zero = np.zeros(dimension, dtype=float)
        rigid = self.evaluate(zero)
        output = np.empty(dimension, dtype=float)
        for index in range(dimension):
            basis = np.zeros(dimension, dtype=float)
            basis[index] = 1.0
            output[index] = self.evaluate(basis) - rigid
        probe = np.linspace(-0.25, 0.25, dimension)
        defect = abs(self.evaluate(probe) - rigid - float(output @ probe))
        return rigid, output, defect


def _energy_dual_norm(stiffness: np.ndarray, residual: np.ndarray) -> float:
    value = float(residual @ np.linalg.solve(stiffness, residual))
    return sqrt(max(0.0, value))


def _lift_to_nested_space(
    coarse_vector: np.ndarray,
    coarse: dict[str, object],
    fine: dict[str, object],
) -> np.ndarray:
    coarse_radii = np.asarray(coarse["radii"], dtype=float)
    fine_radii = np.asarray(fine["radii"], dtype=float)
    coarse_map = np.asarray(coarse["degree_of_freedom_map"], dtype=int)
    fine_map = np.asarray(fine["degree_of_freedom_map"], dtype=int)
    coarse_fields = _fields_from_vector(coarse_vector, coarse_map)
    fine_fields = np.column_stack(
        tuple(
            np.interp(fine_radii, coarse_radii, coarse_fields[:, component])
            for component in range(2)
        )
    )
    return _vector_from_fields(fine_fields, fine_map)


def centrifugal_master_adjoint_feasibility_record(
    *,
    coarse_node_count: int = 41,
    refinement_factor: int = 2,
    quadrature_order: int = 5,
    profile_step: float = 0.001,
) -> dict[str, object]:
    """Return a nested-space primal-adjoint master-amplitude feasibility test."""
    coarse_node_count = _integer_at_least(
        "coarse_node_count", coarse_node_count, 5
    )
    refinement_factor = _integer_at_least("refinement_factor", refinement_factor, 2)
    quadrature_order = _integer_at_least("quadrature_order", quadrature_order, 2)
    profile_step = _positive("profile_step", profile_step)
    fine_node_count = refinement_factor * (coarse_node_count - 1) + 1

    common = {
        "quadrature_order": quadrature_order,
        "profile_step": profile_step,
    }
    coarse = assemble_centrifugal_quadrupole_variational_system(
        node_count=coarse_node_count, **common
    )
    fine = assemble_centrifugal_quadrupole_variational_system(
        node_count=fine_node_count, **common
    )
    coarse_functional = _ExteriorAmplitudeFunctional(coarse)
    fine_functional = _ExteriorAmplitudeFunctional(fine)
    coarse_rigid, coarse_output, coarse_affine_defect = (
        coarse_functional.affine_data()
    )
    fine_rigid, fine_output, fine_affine_defect = fine_functional.affine_data()

    coarse_stiffness = np.asarray(coarse["stiffness_matrix"], dtype=float)
    fine_stiffness = np.asarray(fine["stiffness_matrix"], dtype=float)
    coarse_load = np.asarray(coarse["load_vector"], dtype=float)
    fine_load = np.asarray(fine["load_vector"], dtype=float)
    coarse_primal = np.linalg.solve(coarse_stiffness, coarse_load)
    coarse_adjoint = np.linalg.solve(coarse_stiffness, coarse_output)
    fine_primal = np.linalg.solve(fine_stiffness, fine_load)
    fine_adjoint = np.linalg.solve(fine_stiffness, fine_output)
    lifted_primal = _lift_to_nested_space(coarse_primal, coarse, fine)
    lifted_adjoint = _lift_to_nested_space(coarse_adjoint, coarse, fine)

    primal_residual = fine_load - fine_stiffness @ lifted_primal
    adjoint_residual = fine_output - fine_stiffness @ lifted_adjoint
    primal_indicator = _energy_dual_norm(fine_stiffness, primal_residual)
    adjoint_indicator = _energy_dual_norm(fine_stiffness, adjoint_residual)
    product_bound = primal_indicator * adjoint_indicator
    coarse_total = coarse_rigid + float(coarse_output @ coarse_primal)
    lifted_deformation = float(fine_output @ lifted_primal)
    lifted_total = fine_rigid + lifted_deformation
    residual_correction = float(primal_residual @ lifted_adjoint)
    corrected = lifted_total + residual_correction
    fine_total = fine_rigid + float(fine_output @ fine_primal)
    actual_corrected_error = abs(fine_total - corrected)
    distance_to_zero = abs(corrected) - product_bound
    feasibility_ratio = (
        product_bound / abs(corrected) if corrected != 0.0 else float("inf")
    )

    coarse_algebraic_primal = coarse_load - coarse_stiffness @ coarse_primal
    coarse_algebraic_adjoint = coarse_output - coarse_stiffness @ coarse_adjoint
    fine_primal_difference = fine_primal - lifted_primal
    fine_adjoint_difference = fine_adjoint - lifted_adjoint
    exact_primal_indicator = sqrt(
        max(
            0.0,
            float(fine_primal_difference @ fine_stiffness @ fine_primal_difference),
        )
    )
    exact_adjoint_indicator = sqrt(
        max(
            0.0,
            float(fine_adjoint_difference @ fine_stiffness @ fine_adjoint_difference),
        )
    )
    identity_defect = max(
        abs(primal_indicator - exact_primal_indicator),
        abs(adjoint_indicator - exact_adjoint_indicator),
    )
    claims = {
        "master_output_is_affine_on_both_spaces": max(
            coarse_affine_defect, fine_affine_defect
        )
        < 1.0e-10,
        "primal_and_adjoint_algebraic_solves_close": max(
            float(np.max(np.abs(coarse_algebraic_primal))),
            float(np.max(np.abs(coarse_algebraic_adjoint))),
        )
        < 1.0e-10,
        "nested_residual_indicators_match_exact_fine_energy_errors": (
            identity_defect < 1.0e-9
        ),
        "dual_weighted_product_bounds_fine_discrete_error": (
            actual_corrected_error <= product_bound + 1.0e-12
        ),
        "floating_product_margin_excludes_zero": distance_to_zero > 0.0,
    }
    return {
        "goal": "Exterior Master Amplitude Primal-Adjoint Feasibility",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "floating_nested_galerkin_dual_weighted_residual_probe",
        "parameters": {
            "coarse_node_count": coarse_node_count,
            "fine_node_count": fine_node_count,
            "refinement_factor": refinement_factor,
            "quadrature_order": quadrature_order,
            "profile_step": profile_step,
        },
        "functional_decomposition": {
            "definition": "J(y)=J_rigid+B(y)",
            "coarse_J_rigid": coarse_rigid,
            "fine_J_rigid": fine_rigid,
            "coarse_B_y": float(coarse_output @ coarse_primal),
            "fine_space_B_of_lifted_y": lifted_deformation,
            "wall_displacement_per_f_at_wall": (
                fine_functional.wall_displacement_per_f
            ),
            "coarse_total_amplitude": coarse_total,
            "fine_total_amplitude": fine_total,
            "output_functional_l2_norm_on_fine_coefficients": float(
                np.linalg.norm(fine_output)
            ),
            "maximum_affine_superposition_defect": max(
                coarse_affine_defect, fine_affine_defect
            ),
        },
        "adjoint_solve": {
            "equation": "K z=b for B(v)=b.T@v",
            "coarse_adjoint_energy_norm": sqrt(
                max(0.0, float(coarse_adjoint @ coarse_output))
            ),
            "fine_adjoint_energy_norm": sqrt(
                max(0.0, float(fine_adjoint @ fine_output))
            ),
            "coarse_adjoint_maximum_absolute_coefficient": float(
                np.max(np.abs(coarse_adjoint))
            ),
        },
        "dual_weighted_estimator": {
            "fine_space_output_of_lifted_primal": lifted_total,
            "primal_residual_on_lifted_adjoint": residual_correction,
            "corrected_estimator": corrected,
            "fine_discrete_reference_amplitude": fine_total,
            "actual_corrected_error_against_fine_system": actual_corrected_error,
            "primal_energy_dual_residual_indicator": primal_indicator,
            "adjoint_energy_dual_residual_indicator": adjoint_indicator,
            "residual_product_error_bound": product_bound,
            "product_over_corrected_amplitude": feasibility_ratio,
            "floating_distance_from_zero_after_product_bound": distance_to_zero,
        },
        "verified_numerical_properties": claims,
        "validation_target": (
            "Replace the floating profile, quadrature, affine output vector, and "
            "both energy-dual residual indicators by outward-rounded interval "
            "enclosures; then apply the exact dual-weighted product theorem."
        ),
        "claim_boundary": (
            "Floating evidence only. The product bound is exact only relative to "
            "the assembled fine Galerkin system. It omits the first radial "
            "element in the master-source integral and does not enclose profile "
            "interpolation, quadrature, continuum truncation, Israel matching, "
            "metric backreaction, or any interval quantity."
        ),
    }
