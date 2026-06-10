"""Variational spectral probe for the centrifugal Skyrmion quadrupole.

The exploratory finite-difference solver differentiates sampled coefficient
blocks.  This module instead assembles the quadratic form defined directly by
the local Hessian in ``(f,g,f',g')``.  Piecewise-linear trial functions impose
the regular-origin trace ``f(0)=g(0)=0`` and the ideal-mirror trace ``g(a)=0``.
The free wall value ``f(a)`` receives the boundary quadratic term whose natural
condition is the moving pure-tension Robin law.

The calculation is a floating-point Galerkin probe. It identifies a coercivity
target and removes numerical coefficient differentiation, but floating profile
interpolation and quadrature prevent any one-sided relation to the continuum
spectrum. Equivalence of its trace space with the smooth Frobenius domain also
remains to be proved.
"""

from __future__ import annotations

from math import isfinite

import numpy as np

from .centrifugal_skyrmion_bvp import solve_centrifugal_quadrupole_bvp
from .centrifugal_skyrmion_deformation import (
    quadrupole_static_hessian_matrix,
    rotational_quadrupole_source_covector,
    static_patch_shell_shape_curvature_coefficient,
)
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def _integer_at_least(name: str, value: int, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer at least {minimum}")
    return value


def _wall_robin_multiplier(
    *,
    wall_radius: float,
    curvature: float,
    membrane_tension: float,
    wall_profile_derivative: float,
) -> float:
    lapse = 1.0 - curvature * wall_radius**2
    lapse_derivative = -2.0 * curvature * wall_radius
    shape = float(
        static_patch_shell_shape_curvature_coefficient(
            wall_radius=wall_radius,
            curvature=curvature,
            ell=2,
        )["shape_curvature_coefficient"]
    )
    return (
        -2.0 / wall_radius
        - lapse_derivative / (2.0 * lapse)
        - 4.0 * membrane_tension * shape / (lapse * wall_profile_derivative**2)
    )


def _degree_of_freedom_map(node_count: int) -> np.ndarray:
    indices = np.full((node_count, 2), -1, dtype=int)
    next_index = 0
    for node in range(1, node_count):
        for component in range(2):
            if node == node_count - 1 and component == 1:
                continue
            indices[node, component] = next_index
            next_index += 1
    return indices


def assemble_centrifugal_quadrupole_variational_system(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    membrane_tension: float = 0.001931779647,
    node_count: int = 81,
    quadrature_order: int = 5,
    profile_step: float = 0.001,
) -> dict[str, object]:
    """Assemble the trace-constrained Galerkin stiffness, mass, and source."""
    pion_mass = _nonnegative("pion_mass", pion_mass)
    curvature = _nonnegative("curvature", curvature)
    wall_radius = _positive("wall_radius", wall_radius)
    membrane_tension = _positive("membrane_tension", membrane_tension)
    profile_step = _positive("profile_step", profile_step)
    node_count = _integer_at_least("node_count", node_count, 5)
    quadrature_order = _integer_at_least("quadrature_order", quadrature_order, 2)
    if 1.0 - curvature * wall_radius**2 <= 0.0:
        raise ValueError("wall must lie strictly inside the static-patch horizon")

    shooting_slope, profile_points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=profile_step,
    )
    profile_radii = np.asarray([point[0] for point in profile_points], dtype=float)
    profile_values = np.asarray([point[1] for point in profile_points], dtype=float)
    profile_derivatives = np.asarray(
        [point[2] for point in profile_points], dtype=float
    )
    radii = np.linspace(0.0, wall_radius, node_count)
    dof_map = _degree_of_freedom_map(node_count)
    dimension = int(np.max(dof_map)) + 1
    stiffness = np.zeros((dimension, dimension), dtype=float)
    mass = np.zeros((dimension, dimension), dtype=float)
    load = np.zeros(dimension, dtype=float)
    gauss_nodes, gauss_weights = np.polynomial.legendre.leggauss(quadrature_order)

    for element in range(node_count - 1):
        left = float(radii[element])
        right = float(radii[element + 1])
        width = right - left
        local_indices = tuple(
            (node, component, int(dof_map[node, component]))
            for node in (element, element + 1)
            for component in range(2)
            if dof_map[node, component] >= 0
        )
        for gauss_node, gauss_weight in zip(
            gauss_nodes, gauss_weights, strict=True
        ):
            radius = (left + right + width * float(gauss_node)) / 2.0
            weight = width * float(gauss_weight) / 2.0
            profile = float(np.interp(radius, profile_radii, profile_values))
            derivative = float(
                np.interp(radius, profile_radii, profile_derivatives)
            )
            hessian = np.asarray(
                quadrupole_static_hessian_matrix(
                    radius=radius,
                    metric_factor=1.0 - curvature * radius**2,
                    profile=profile,
                    profile_derivative=derivative,
                    pion_mass=pion_mass,
                )["symmetric_hessian_matrix"],
                dtype=float,
            )
            source_record = rotational_quadrupole_source_covector(
                radius=radius,
                metric_factor=1.0 - curvature * radius**2,
                profile=profile,
                profile_derivative=derivative,
            )
            source = np.asarray(
                (
                    source_record["radial_field_coefficient"],
                    source_record["tangential_field_coefficient"],
                    source_record["radial_field_derivative_coefficient"],
                    source_record["tangential_field_derivative_coefficient"],
                ),
                dtype=float,
            )
            shape_values = (
                (right - radius) / width,
                (radius - left) / width,
            )
            shape_derivatives = (-1.0 / width, 1.0 / width)
            basis: dict[tuple[int, int], np.ndarray] = {}
            for node, component, _ in local_indices:
                side = node - element
                vector = np.zeros(4, dtype=float)
                vector[component] = shape_values[side]
                vector[2 + component] = shape_derivatives[side]
                basis[(node, component)] = vector
            for node, component, global_index in local_indices:
                vector = basis[(node, component)]
                load[global_index] += weight * float(vector @ source)
                for other_node, other_component, other_index in local_indices:
                    other = basis[(other_node, other_component)]
                    stiffness[global_index, other_index] += weight * float(
                        vector @ hessian @ other
                    )
                    mass[global_index, other_index] += weight * (
                        vector[component] * other[other_component]
                        if component == other_component
                        else 0.0
                    )

    wall_profile_derivative = float(profile_derivatives[-1])
    wall_hessian = np.asarray(
        quadrupole_static_hessian_matrix(
            radius=wall_radius,
            metric_factor=1.0 - curvature * wall_radius**2,
            profile=0.0,
            profile_derivative=wall_profile_derivative,
            pion_mass=pion_mass,
        )["symmetric_hessian_matrix"],
        dtype=float,
    )
    wall_robin = _wall_robin_multiplier(
        wall_radius=wall_radius,
        curvature=curvature,
        membrane_tension=membrane_tension,
        wall_profile_derivative=wall_profile_derivative,
    )
    wall_principal = float(wall_hessian[2, 2])
    wall_mixed = float(wall_hessian[0, 2])
    boundary_form_coefficient = -(wall_principal * wall_robin + wall_mixed)
    wall_index = int(dof_map[-1, 0])
    stiffness[wall_index, wall_index] += boundary_form_coefficient
    return {
        "radii": radii,
        "degree_of_freedom_map": dof_map,
        "stiffness_matrix": stiffness,
        "mass_matrix": mass,
        "load_vector": load,
        "shooting_slope": shooting_slope,
        "wall_profile_derivative": wall_profile_derivative,
        "wall_robin_multiplier": wall_robin,
        "wall_principal_coefficient": wall_principal,
        "wall_mixed_coefficient": wall_mixed,
        "wall_boundary_form_coefficient": boundary_form_coefficient,
        "parameters": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius": wall_radius,
            "membrane_tension": membrane_tension,
            "node_count": node_count,
            "quadrature_order": quadrature_order,
            "profile_step": profile_step,
        },
    }


def centrifugal_quadrupole_variational_record(
    *,
    node_count: int = 81,
    quadrature_order: int = 5,
    profile_step: float = 0.001,
) -> dict[str, object]:
    """Solve the Galerkin system and report its floating spectral margin."""
    assembled = assemble_centrifugal_quadrupole_variational_system(
        node_count=node_count,
        quadrature_order=quadrature_order,
        profile_step=profile_step,
    )
    stiffness = assembled["stiffness_matrix"]
    mass = assembled["mass_matrix"]
    load = assembled["load_vector"]
    symmetry_defect = float(np.max(np.abs(stiffness - stiffness.T)))
    mass_factor = np.linalg.cholesky(mass)
    transformed = np.linalg.solve(mass_factor, stiffness)
    transformed = np.linalg.solve(mass_factor, transformed.T).T
    transformed = (transformed + transformed.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(transformed)
    solution = np.linalg.solve(stiffness, load)
    radii = assembled["radii"]
    dof_map = assembled["degree_of_freedom_map"]
    fields = np.zeros((len(radii), 2), dtype=float)
    for node in range(len(radii)):
        for component in range(2):
            index = int(dof_map[node, component])
            if index >= 0:
                fields[node, component] = solution[index]
    work = float(solution @ load)
    energy = float(solution @ stiffness @ solution)
    wall_slope = float((fields[-1, 0] - fields[-2, 0]) / (radii[-1] - radii[-2]))
    wall_shape = -float(fields[-1, 0]) / float(
        assembled["wall_profile_derivative"]
    )
    return {
        "parameters": assembled["parameters"],
        "shooting_slope": assembled["shooting_slope"],
        "matrix_dimension": int(stiffness.shape[0]),
        "stiffness_symmetry_defect": symmetry_defect,
        "smallest_generalized_ritz_value": float(eigenvalues[0]),
        "second_generalized_ritz_value": float(eigenvalues[1]),
        "wall_robin_multiplier": assembled["wall_robin_multiplier"],
        "wall_boundary_form_coefficient": assembled[
            "wall_boundary_form_coefficient"
        ],
        "wall_radial_field": float(fields[-1, 0]),
        "wall_radial_field_derivative": wall_slope,
        "wall_robin_residual_from_last_element": wall_slope
        - float(assembled["wall_robin_multiplier"]) * float(fields[-1, 0]),
        "wall_shape_coefficient": wall_shape,
        "maximum_absolute_radial_field": float(np.max(np.abs(fields[:, 0]))),
        "maximum_absolute_tangential_field": float(np.max(np.abs(fields[:, 1]))),
        "quadratic_form_at_solution": energy,
        "source_work_at_solution": work,
        "stationarity_work_defect": abs(energy - work),
        "sample_radii": tuple(float(value) for value in radii),
        "radial_field_samples": tuple(float(value) for value in fields[:, 0]),
        "tangential_field_samples": tuple(float(value) for value in fields[:, 1]),
        "claim_boundary": (
            "Floating-point piecewise-linear weak-form calculation with origin "
            "and wall trace conditions. It preserves matrix symmetry and the "
            "Robin-equivalent boundary form, but profile interpolation and "
            "quadrature prevent any certified one-sided relation to the "
            "continuum spectrum. Equivalence with the smooth Frobenius origin "
            "domain also remains open."
        ),
    }


def centrifugal_quadrupole_variational_convergence_record() -> dict[str, object]:
    """Compare the variational solution and Ritz spectrum across three meshes."""
    records = tuple(
        centrifugal_quadrupole_variational_record(node_count=count)
        for count in (41, 81, 161)
    )
    probes = np.asarray((0.25, 0.5, 1.0, 2.0, 3.0, 4.0), dtype=float)

    def sample(record: dict[str, object]) -> np.ndarray:
        radii = np.asarray(record["sample_radii"])
        radial = np.interp(probes, radii, record["radial_field_samples"])
        tangential = np.interp(probes, radii, record["tangential_field_samples"])
        return np.concatenate((radial, tangential))

    medium = sample(records[-2])
    fine = sample(records[-1])
    scaled_difference = float(
        np.max(np.abs(fine - medium)) / max(1.0, float(np.max(np.abs(fine))))
    )
    ritz_values = tuple(
        float(record["smallest_generalized_ritz_value"]) for record in records
    )
    strong_form = solve_centrifugal_quadrupole_bvp(
        node_count=401,
        origin_radius=0.01,
        profile_step=0.001,
    )
    strong_radii = np.asarray(strong_form["sample_radii"])
    strong_sample = np.concatenate(
        (
            np.interp(probes, strong_radii, strong_form["radial_field_samples"]),
            np.interp(
                probes,
                strong_radii,
                strong_form["tangential_field_samples"],
            ),
        )
    )
    cross_formulation_difference = float(
        np.max(np.abs(fine - strong_sample))
        / max(1.0, float(np.max(np.abs(fine))))
    )
    claims = {
        "assembled_forms_are_symmetric": all(
            float(record["stiffness_symmetry_defect"]) < 1.0e-12
            for record in records
        ),
        "all_sampled_ritz_values_are_positive": min(ritz_values) > 0.0,
        "ritz_values_decrease_under_nested_refinement": all(
            ritz_values[index + 1] <= ritz_values[index] + 1.0e-10
            for index in range(len(ritz_values) - 1)
        ),
        "two_finest_solutions_agree": scaled_difference < 0.01,
        "weak_and_strong_formulations_agree": cross_formulation_difference < 0.002,
        "stationarity_identity_closes": all(
            float(record["stationarity_work_defect"]) < 1.0e-10
            for record in records
        ),
        "wall_boundary_form_is_positive": all(
            float(record["wall_boundary_form_coefficient"]) > 0.0
            for record in records
        ),
    }
    return {
        "goal": "Variational Centrifugal Quadrupole Coercivity Target",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "floating_weak_form_spectral_probe",
        "mesh_records": records,
        "smallest_generalized_ritz_values": ritz_values,
        "fine_over_medium_maximum_scaled_solution_difference": scaled_difference,
        "weak_over_strong_maximum_scaled_solution_difference": (
            cross_formulation_difference
        ),
        "strong_form_comparison": {
            "node_count": strong_form["parameters"]["node_count"],
            "origin_radius": strong_form["parameters"]["origin_radius"],
            "profile_step": strong_form["parameters"]["profile_step"],
            "wall_shape_coefficient": strong_form["wall_shape_coefficient"],
        },
        "verified_numerical_properties": claims,
        "required_validation_step": (
            "Enclose the authenticated profile tube, Hessian blocks, wall "
            "coefficient, source, and quadrature defects by rational intervals; "
            "prove the origin form-domain/Frobenius equivalence; then combine a "
            "validated low-mode space with a complement estimate to prove a "
            "strict continuum lower spectral bound and an a posteriori response "
            "error enclosure."
        ),
        "claim_boundary": (
            "The positive generalized eigenvalue estimates have no certified "
            "one-sided relation to the continuum spectrum and therefore do not "
            "prove coercivity. This audit selects and tests the symmetric weak "
            "formulation that the interval proof must validate."
        ),
    }
