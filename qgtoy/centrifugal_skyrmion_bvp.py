"""Exploratory global solver for the centrifugal Skyrmion quadrupole.

This module consumes the source-hashed local Hessian/source generator from
``centrifugal_skyrmion_deformation`` and reduces its variational equation to a
two-field radial boundary-value problem.  The discretization is deliberately
dependency-light: centered second differences in the bulk and a 2x2 block
Thomas solver.

The result is numerical evidence, not validated numerics.  Its main purpose is
to test whether the correct two-channel and moving-wall problem has a regular,
moderate default solution before investing in an interval certificate.
"""

from __future__ import annotations

from math import isfinite, pi

import numpy as np

from .centrifugal_skyrmion_deformation import (
    quadrupole_static_hessian_matrix,
    rotational_quadrupole_source_covector,
    static_patch_shell_shape_curvature_coefficient,
)
from .massive_skyrmion_profile import static_patch_lapse
from .massive_skyrmion_worldtube import (
    origin_cubic_coefficient,
    solve_hard_wall_skyrmion_profile,
)


def _positive(name: str, value: float) -> float:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _nonnegative(name: str, value: float) -> float:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def _node_count(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 5:
        raise ValueError("node_count must be an integer at least five")
    return value


def _block_tridiagonal_solve(
    lower: np.ndarray,
    diagonal: np.ndarray,
    upper: np.ndarray,
    right_hand_side: np.ndarray,
) -> np.ndarray:
    """Solve a nonsymmetric block-tridiagonal system with 2x2 blocks."""
    node_count = diagonal.shape[0]
    if lower.shape != (node_count, 2, 2):
        raise ValueError("lower has the wrong shape")
    if upper.shape != (node_count, 2, 2):
        raise ValueError("upper has the wrong shape")
    if diagonal.shape != (node_count, 2, 2):
        raise ValueError("diagonal has the wrong shape")
    if right_hand_side.shape != (node_count, 2):
        raise ValueError("right_hand_side has the wrong shape")

    reduced_upper = np.zeros_like(upper)
    reduced_rhs = np.zeros_like(right_hand_side)
    reduced_upper[0] = np.linalg.solve(diagonal[0], upper[0])
    reduced_rhs[0] = np.linalg.solve(diagonal[0], right_hand_side[0])
    for index in range(1, node_count):
        pivot = diagonal[index] - lower[index] @ reduced_upper[index - 1]
        rhs = right_hand_side[index] - lower[index] @ reduced_rhs[index - 1]
        if index + 1 < node_count:
            reduced_upper[index] = np.linalg.solve(pivot, upper[index])
        reduced_rhs[index] = np.linalg.solve(pivot, rhs)

    solution = np.zeros_like(right_hand_side)
    solution[-1] = reduced_rhs[-1]
    for index in range(node_count - 2, -1, -1):
        solution[index] = (
            reduced_rhs[index] - reduced_upper[index] @ solution[index + 1]
        )
    return solution


def _regular_origin_robin_matrix(
    *,
    shooting_slope: float,
    pion_mass: float,
    curvature: float,
    origin_radius: float,
) -> tuple[np.ndarray, dict[str, object]]:
    """Return ``y'=R y`` for the leading regular ``p=1,3`` subspace."""
    probe = min(1.0e-4, origin_radius / 20.0)
    cubic = origin_cubic_coefficient(
        shooting_slope,
        pion_mass=pion_mass,
        curvature=curvature,
    )
    profile = pi - shooting_slope * probe + cubic * probe**3
    derivative = -shooting_slope + 3.0 * cubic * probe**2
    matrix = np.asarray(
        quadrupole_static_hessian_matrix(
            radius=probe,
            metric_factor=static_patch_lapse(probe, curvature),
            profile=profile,
            profile_derivative=derivative,
            pion_mass=pion_mass,
        )["symmetric_hessian_matrix"],
        dtype=float,
    )
    coordinate = matrix[:2, :2]
    mixed = matrix[:2, 2:] / probe
    principal = matrix[2:, 2:] / probe**2

    vectors: list[np.ndarray] = []
    singular_values: list[float] = []
    for exponent in (1.0, 3.0):
        indicial = (
            -exponent * (exponent + 1.0) * principal
            - (exponent + 1.0) * mixed.T
            + exponent * mixed
            + coordinate
        )
        _, values, right = np.linalg.svd(indicial)
        vector = right[-1]
        if vector[1] < 0.0:
            vector = -vector
        vectors.append(vector)
        singular_values.append(float(values[-1]))
    basis = np.column_stack(vectors)
    robin = (
        basis
        @ np.diag((1.0 / origin_radius, 3.0 / origin_radius))
        @ np.linalg.inv(basis)
    )
    return robin, {
        "probe_radius": probe,
        "regular_exponents": (1.0, 3.0),
        "regular_vectors": tuple(
            tuple(float(value) for value in vector) for vector in vectors
        ),
        "indicial_smallest_singular_values": tuple(singular_values),
        "linear_mode_f_over_g": float(vectors[0][0] / vectors[0][1]),
        "cubic_mode_f_over_g": float(vectors[1][0] / vectors[1][1]),
    }


def _wall_radial_field_robin_multiplier(
    *,
    wall_radius: float,
    curvature: float,
    membrane_tension: float,
    wall_profile_derivative: float,
) -> float:
    lapse = static_patch_lapse(wall_radius, curvature)
    lapse_derivative = -2.0 * curvature * wall_radius
    shape = static_patch_shell_shape_curvature_coefficient(
        wall_radius=wall_radius,
        curvature=curvature,
        ell=2,
    )["shape_curvature_coefficient"]
    return (
        -2.0 / wall_radius
        - lapse_derivative / (2.0 * lapse)
        - 4.0 * membrane_tension * float(shape) / (lapse * wall_profile_derivative**2)
    )


def _interpolate_profile(
    points: tuple[tuple[float, float, float], ...],
    radii: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    source_radii = np.asarray([point[0] for point in points], dtype=float)
    source_profile = np.asarray([point[1] for point in points], dtype=float)
    source_derivative = np.asarray([point[2] for point in points], dtype=float)
    return (
        np.interp(radii, source_radii, source_profile),
        np.interp(radii, source_radii, source_derivative),
    )


def solve_centrifugal_quadrupole_bvp(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    membrane_tension: float = 0.001931779647,
    node_count: int = 201,
    origin_radius: float = 0.02,
    profile_step: float = 0.002,
) -> dict[str, object]:
    """Solve the default two-channel quadrupole problem by finite differences."""
    pion_mass = _nonnegative("pion_mass", pion_mass)
    curvature = _nonnegative("curvature", curvature)
    wall_radius = _positive("wall_radius", wall_radius)
    membrane_tension = _positive("membrane_tension", membrane_tension)
    node_count = _node_count(node_count)
    origin_radius = _positive("origin_radius", origin_radius)
    profile_step = _positive("profile_step", profile_step)
    if origin_radius >= wall_radius:
        raise ValueError("origin_radius must be smaller than wall_radius")
    if static_patch_lapse(wall_radius, curvature) <= 0.0:
        raise ValueError("wall must lie strictly inside the horizon")

    shooting_slope, points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=profile_step,
    )
    radii = np.linspace(origin_radius, wall_radius, node_count)
    width = float(radii[1] - radii[0])
    profile, profile_derivative = _interpolate_profile(points, radii)

    coordinate = np.zeros((node_count, 2, 2), dtype=float)
    mixed = np.zeros((node_count, 2, 2), dtype=float)
    principal = np.zeros((node_count, 2, 2), dtype=float)
    source_coordinate = np.zeros((node_count, 2), dtype=float)
    source_derivative = np.zeros((node_count, 2), dtype=float)
    for index, radius in enumerate(radii):
        hessian = np.asarray(
            quadrupole_static_hessian_matrix(
                radius=float(radius),
                metric_factor=static_patch_lapse(float(radius), curvature),
                profile=float(profile[index]),
                profile_derivative=float(profile_derivative[index]),
                pion_mass=pion_mass,
            )["symmetric_hessian_matrix"],
            dtype=float,
        )
        source = rotational_quadrupole_source_covector(
            radius=float(radius),
            metric_factor=static_patch_lapse(float(radius), curvature),
            profile=float(profile[index]),
            profile_derivative=float(profile_derivative[index]),
        )
        coordinate[index] = hessian[:2, :2]
        mixed[index] = hessian[:2, 2:]
        principal[index] = hessian[2:, 2:]
        source_coordinate[index] = (
            float(source["radial_field_coefficient"]),
            float(source["tangential_field_coefficient"]),
        )
        source_derivative[index] = (
            float(source["radial_field_derivative_coefficient"]),
            float(source["tangential_field_derivative_coefficient"]),
        )

    principal_derivative = np.gradient(principal, radii, axis=0, edge_order=2)
    mixed_derivative = np.gradient(mixed, radii, axis=0, edge_order=2)
    source_derivative_radial = np.gradient(
        source_derivative,
        radii,
        axis=0,
        edge_order=2,
    )
    first_derivative = -principal_derivative + mixed - np.swapaxes(mixed, 1, 2)
    zeroth_order = coordinate - np.swapaxes(mixed_derivative, 1, 2)
    forcing = source_coordinate - source_derivative_radial

    lower = np.zeros((node_count, 2, 2), dtype=float)
    diagonal = np.zeros((node_count, 2, 2), dtype=float)
    upper = np.zeros((node_count, 2, 2), dtype=float)
    rhs = np.zeros((node_count, 2), dtype=float)
    identity = np.eye(2)

    origin_robin, origin_record = _regular_origin_robin_matrix(
        shooting_slope=shooting_slope,
        pion_mass=pion_mass,
        curvature=curvature,
        origin_radius=origin_radius,
    )
    diagonal[0] = -identity / width - origin_robin
    upper[0] = identity / width

    for index in range(1, node_count - 1):
        lower[index] = -principal[index] / width**2 - first_derivative[index] / (
            2.0 * width
        )
        diagonal[index] = 2.0 * principal[index] / width**2 + zeroth_order[index]
        upper[index] = -principal[index] / width**2 + first_derivative[index] / (
            2.0 * width
        )
        rhs[index] = forcing[index]

    wall_profile_derivative = float(profile_derivative[-1])
    wall_robin = _wall_radial_field_robin_multiplier(
        wall_radius=wall_radius,
        curvature=curvature,
        membrane_tension=membrane_tension,
        wall_profile_derivative=wall_profile_derivative,
    )
    lower[-1] = np.asarray(((-1.0 / width, 0.0), (0.0, 0.0)))
    diagonal[-1] = np.asarray(((1.0 / width - wall_robin, 0.0), (0.0, 1.0)))

    solution = _block_tridiagonal_solve(lower, diagonal, upper, rhs)

    residual = np.zeros_like(rhs)
    for index in range(node_count):
        residual[index] = diagonal[index] @ solution[index] - rhs[index]
        if index > 0:
            residual[index] += lower[index] @ solution[index - 1]
        if index + 1 < node_count:
            residual[index] += upper[index] @ solution[index + 1]
    radial_field = solution[:, 0]
    tangential_field = solution[:, 1]
    wall_radial_derivative = (radial_field[-1] - radial_field[-2]) / width
    wall_shape = -radial_field[-1] / wall_profile_derivative
    response_norm = float(np.trapezoid(radial_field**2 + tangential_field**2, radii))
    return {
        "parameters": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius": wall_radius,
            "membrane_tension": membrane_tension,
            "node_count": node_count,
            "origin_radius": origin_radius,
            "profile_step": profile_step,
            "mesh_width": width,
        },
        "shooting_slope": shooting_slope,
        "origin_regular_subspace": origin_record,
        "wall_radial_field_robin_multiplier": wall_robin,
        "maximum_absolute_radial_field": float(np.max(np.abs(radial_field))),
        "maximum_absolute_tangential_field": float(np.max(np.abs(tangential_field))),
        "response_l2_norm_squared": response_norm,
        "wall_radial_field": float(radial_field[-1]),
        "wall_tangential_field": float(tangential_field[-1]),
        "wall_radial_field_derivative": float(wall_radial_derivative),
        "wall_robin_residual": float(
            wall_radial_derivative - wall_robin * radial_field[-1]
        ),
        "wall_shape_coefficient": float(wall_shape),
        "linear_system_maximum_residual": float(np.max(np.abs(residual))),
        "sample_radii": tuple(float(value) for value in radii),
        "radial_field_samples": tuple(float(value) for value in radial_field),
        "tangential_field_samples": tuple(float(value) for value in tangential_field),
        "claim_boundary": (
            "Unvalidated finite-difference solve using numerically differentiated "
            "coefficient blocks and leading Frobenius data. It is evidence for "
            "the default branch, not a proof of existence, uniqueness, or "
            "stress conservation."
        ),
    }


def centrifugal_quadrupole_mesh_convergence_record() -> dict[str, object]:
    """Compare mesh, origin-cutoff, and background-profile refinements."""
    records = tuple(
        solve_centrifugal_quadrupole_bvp(node_count=count) for count in (101, 201, 401)
    )
    sample_radii = np.asarray((0.25, 0.5, 1.0, 2.0, 3.0, 4.0))
    sampled: list[dict[str, object]] = []
    for record in records:
        radii = np.asarray(record["sample_radii"])
        radial = np.asarray(record["radial_field_samples"])
        tangential = np.asarray(record["tangential_field_samples"])
        sampled.append(
            {
                "node_count": record["parameters"]["node_count"],
                "radial_field": tuple(
                    float(value) for value in np.interp(sample_radii, radii, radial)
                ),
                "tangential_field": tuple(
                    float(value) for value in np.interp(sample_radii, radii, tangential)
                ),
                "wall_shape_coefficient": record["wall_shape_coefficient"],
                "response_l2_norm_squared": record["response_l2_norm_squared"],
            }
        )
    coarse = np.asarray(sampled[-2]["radial_field"] + sampled[-2]["tangential_field"])
    fine = np.asarray(sampled[-1]["radial_field"] + sampled[-1]["tangential_field"])
    scale = max(1.0, float(np.max(np.abs(fine))))
    difference = float(np.max(np.abs(fine - coarse)) / scale)
    origin_records = (
        solve_centrifugal_quadrupole_bvp(node_count=401, origin_radius=0.04),
        records[-1],
        solve_centrifugal_quadrupole_bvp(node_count=401, origin_radius=0.01),
    )
    profile_records = (
        solve_centrifugal_quadrupole_bvp(node_count=401, profile_step=0.004),
        records[-1],
        solve_centrifugal_quadrupole_bvp(node_count=401, profile_step=0.001),
    )

    def convergence_vector(record: dict[str, object]) -> np.ndarray:
        radii = np.asarray(record["sample_radii"])
        radial = np.asarray(record["radial_field_samples"])
        tangential = np.asarray(record["tangential_field_samples"])
        return np.concatenate(
            (
                np.interp(sample_radii, radii, radial),
                np.interp(sample_radii, radii, tangential),
                np.asarray(
                    (
                        record["wall_shape_coefficient"],
                        record["response_l2_norm_squared"],
                    )
                ),
            )
        )

    origin_middle = convergence_vector(origin_records[1])
    origin_fine = convergence_vector(origin_records[2])
    origin_difference = float(
        np.max(np.abs(origin_fine - origin_middle))
        / max(1.0, float(np.max(np.abs(origin_fine))))
    )
    profile_middle = convergence_vector(profile_records[1])
    profile_fine = convergence_vector(profile_records[2])
    profile_difference = float(
        np.max(np.abs(profile_fine - profile_middle))
        / max(1.0, float(np.max(np.abs(profile_fine))))
    )
    claims = {
        "linear_systems_close": all(
            record["linear_system_maximum_residual"] < 1.0e-8 for record in records
        ),
        "wall_conditions_close": all(
            abs(record["wall_robin_residual"]) < 1.0e-10
            and abs(record["wall_tangential_field"]) < 1.0e-12
            for record in records
        ),
        "regular_indicial_modes_are_one_and_three": all(
            record["origin_regular_subspace"]["regular_exponents"] == (1.0, 3.0)
            for record in records
        ),
        "two_finest_meshes_agree_at_sample_points": difference < 0.05,
        "origin_cutoff_refinement_is_stable": origin_difference < 0.005,
        "background_profile_refinement_is_stable": profile_difference < 0.005,
    }
    return {
        "goal": "Exploratory Global Centrifugal Quadrupole Solve",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "unvalidated_two_channel_bvp_mesh_convergence",
        "sample_radii": tuple(float(value) for value in sample_radii),
        "mesh_samples": tuple(sampled),
        "fine_over_medium_maximum_scaled_difference": difference,
        "origin_cutoff_samples": tuple(
            {
                "origin_radius": record["parameters"]["origin_radius"],
                "wall_shape_coefficient": record["wall_shape_coefficient"],
                "response_l2_norm_squared": record["response_l2_norm_squared"],
                "maximum_absolute_radial_field": record[
                    "maximum_absolute_radial_field"
                ],
                "maximum_absolute_tangential_field": record[
                    "maximum_absolute_tangential_field"
                ],
            }
            for record in origin_records
        ),
        "fine_over_medium_origin_maximum_scaled_difference": origin_difference,
        "background_profile_step_samples": tuple(
            {
                "profile_step": record["parameters"]["profile_step"],
                "shooting_slope": record["shooting_slope"],
                "wall_shape_coefficient": record["wall_shape_coefficient"],
                "response_l2_norm_squared": record["response_l2_norm_squared"],
            }
            for record in profile_records
        ),
        "fine_over_medium_profile_maximum_scaled_difference": profile_difference,
        "finest_record": records[-1],
        "certified_claims": claims,
        "claim_boundary": (
            "Step-converged exploratory numerics only. The profile is the "
            "floating hard-wall solution, coefficient derivatives are finite "
            "differences, the origin Frobenius data are leading order, and no "
            "interval enclosure or completed-stress audit is supplied."
        ),
    }
