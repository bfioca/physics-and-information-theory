"""Matrix-Riccati route to centrifugal Skyrmion coercivity.

For the symmetric weak density

``q[y]=y.T C y+2 y.T M y'+y'.T P y'``

and a symmetric matrix field ``K``, put ``D=M-K``.  Direct completion gives

``q[y]-alpha |y|^2``
``=(y'+P^-1 D.T y).T P (y'+P^-1 D.T y)``
`` +(y.T K y)' + y.T R_alpha y``,

where

``R_alpha=C-alpha I-D P^-1 D.T-K'``.

Thus positive ``P`` and ``R_alpha``, a nonnegative wall trace
``B+K(a)``, and a vanishing Friedrichs-origin trace prove a continuum lower
bound without differentiating the physical coefficient blocks.  This module
contains the exact algebraic identity and a floating candidate generator.  It
does not interval-certify the candidate or identify the completed form domain.
"""

from __future__ import annotations

from fractions import Fraction
from math import isfinite
from typing import TypeVar

import numpy as np

from .centrifugal_skyrmion_deformation import (
    quadrupole_static_hessian_matrix,
    static_patch_shell_shape_curvature_coefficient,
)
from .centrifugal_skyrmion_origin import centrifugal_origin_leading_hessian
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile


Scalar = TypeVar("Scalar")
Vector2 = tuple[Scalar, Scalar]
Matrix2 = tuple[tuple[Scalar, Scalar], tuple[Scalar, Scalar]]


def _transpose(matrix: Matrix2) -> Matrix2:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _matrix_add(left: Matrix2, right: Matrix2) -> Matrix2:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_sub(left: Matrix2, right: Matrix2) -> Matrix2:
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_mul(left: Matrix2, right: Matrix2) -> Matrix2:
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(2))
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_scale(matrix: Matrix2, scalar: Scalar) -> Matrix2:
    return tuple(
        tuple(matrix[row][column] * scalar for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_symmetric_part(matrix: Matrix2) -> Matrix2:
    return _matrix_scale(_matrix_add(matrix, _transpose(matrix)), Fraction(1, 2))


def _matrix_vector(matrix: Matrix2, vector: Vector2) -> Vector2:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_inverse(matrix: Matrix2) -> Matrix2:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant == 0:
        raise ValueError("principal matrix must be invertible")
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def _dot(left: Vector2, right: Vector2) -> Scalar:
    return sum(left[index] * right[index] for index in range(2))  # type: ignore[return-value]


def riccati_completion_identity_defect(
    *,
    principal: Matrix2,
    mixed: Matrix2,
    coordinate: Matrix2,
    multiplier: Matrix2,
    multiplier_derivative: Matrix2,
    field: Vector2,
    derivative: Vector2,
    spectral_target: Scalar,
) -> Scalar:
    """Return the exact pointwise completion defect.

    The result is identically zero for exact scalar arithmetic when
    ``principal`` and ``multiplier`` are symmetric.  Keeping this as an
    executable identity prevents a sign convention in the boundary derivative
    from being hidden in the later interval checker.
    """
    if principal != _transpose(principal):
        raise ValueError("principal must be symmetric")
    if multiplier != _transpose(multiplier):
        raise ValueError("multiplier must be symmetric")
    zero = spectral_target * 0
    identity = ((zero + 1, zero), (zero, zero + 1))
    shifted_coordinate = _matrix_sub(
        coordinate,
        tuple(
            tuple(spectral_target * identity[row][column] for column in range(2))
            for row in range(2)
        ),  # type: ignore[arg-type]
    )
    difference = _matrix_sub(mixed, multiplier)
    inverse = _matrix_inverse(principal)
    completed_potential = _matrix_mul(
        _matrix_mul(difference, inverse),
        _transpose(difference),
    )
    residual = _matrix_sub(
        _matrix_sub(shifted_coordinate, completed_potential),
        multiplier_derivative,
    )
    correction = _matrix_vector(
        inverse,
        _matrix_vector(_transpose(difference), field),
    )
    completed_derivative = tuple(
        derivative[index] + correction[index] for index in range(2)
    )
    left = (
        _dot(derivative, _matrix_vector(principal, derivative))
        + 2 * _dot(field, _matrix_vector(mixed, derivative))
        + _dot(field, _matrix_vector(shifted_coordinate, field))
    )
    square = _dot(
        completed_derivative,
        _matrix_vector(principal, completed_derivative),
    )
    boundary_derivative = (
        2 * _dot(field, _matrix_vector(multiplier, derivative))
        + _dot(field, _matrix_vector(multiplier_derivative, field))
    )
    right = square + boundary_derivative + _dot(
        field,
        _matrix_vector(residual, field),
    )
    return left - right


def regular_liouville_potential_identity_defect(
    *,
    time: Scalar,
    principal_bar: Matrix2,
    principal_bar_derivative: Matrix2,
    mixed_bar: Matrix2,
    mixed_bar_derivative: Matrix2,
    coordinate: Matrix2,
) -> Matrix2:
    """Compare the direct and regular Liouville multiplier potentials.

    For ``P=x^2 Pbar``, ``M=x Mbar`` and
    ``K=sym(M)-P/(2x)``, the direct completed potential has no origin
    singularity.  This function returns the exact matrix defect between the
    direct algebra and

    ``C-sym(Mbar)+Pbar/4-2t sym(Mbar)_t+t Pbar_t``
    ``+Abar Pbar^-1 Abar``.
    """
    symmetric_mixed = _matrix_symmetric_part(mixed_bar)
    symmetric_mixed_derivative = _matrix_symmetric_part(
        mixed_bar_derivative
    )
    antisymmetric_mixed = _matrix_scale(
        _matrix_sub(mixed_bar, _transpose(mixed_bar)),
        Fraction(1, 2),
    )
    multiplier_bar = _matrix_sub(
        symmetric_mixed,
        _matrix_scale(principal_bar, Fraction(1, 2)),
    )
    multiplier_radial_derivative = _matrix_add(
        multiplier_bar,
        _matrix_scale(
            _matrix_sub(
                symmetric_mixed_derivative,
                _matrix_scale(principal_bar_derivative, Fraction(1, 2)),
            ),
            2 * time,
        ),
    )
    difference_left = _matrix_sub(multiplier_bar, mixed_bar)
    difference_right = _matrix_sub(multiplier_bar, _transpose(mixed_bar))
    direct = _matrix_sub(
        _matrix_sub(coordinate, multiplier_radial_derivative),
        _matrix_mul(
            _matrix_mul(difference_left, _matrix_inverse(principal_bar)),
            difference_right,
        ),
    )
    regular = _matrix_add(
        _matrix_add(
            _matrix_sub(
                _matrix_add(
                    _matrix_sub(coordinate, symmetric_mixed),
                    _matrix_scale(principal_bar, Fraction(1, 4)),
                ),
                _matrix_scale(symmetric_mixed_derivative, 2 * time),
            ),
            _matrix_scale(principal_bar_derivative, time),
        ),
        _matrix_mul(
            _matrix_mul(
                antisymmetric_mixed,
                _matrix_inverse(principal_bar),
            ),
            antisymmetric_mixed,
        ),
    )
    return _matrix_sub(direct, regular)


def _evaluate_origin_polynomial(
    coefficients: tuple[Fraction, ...],
    slope: float,
) -> float:
    result = 0.0
    for coefficient in reversed(coefficients):
        result = result * slope + float(coefficient)
    return result


def _shifted_origin_data(
    shooting_slope: float,
    spectral_shift: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    hessian = np.asarray(
        tuple(
            tuple(
                _evaluate_origin_polynomial(entry, shooting_slope)
                for entry in row
            )
            for row in centrifugal_origin_leading_hessian()
        ),
        dtype=float,
    )
    coordinate = hessian[:2, :2]
    mixed = hessian[:2, 2:]
    principal = hessian[2:, 2:]
    exponent = np.polynomial.Polynomial((0.0, 1.0))
    pencil = np.empty((2, 2), dtype=object)
    for row in range(2):
        for column in range(2):
            pencil[row, column] = (
                -exponent * (exponent + 1.0) * principal[row, column]
                - (exponent + 1.0) * mixed.T[row, column]
                + exponent * mixed[row, column]
                + coordinate[row, column]
                - (spectral_shift if row == column else 0.0)
            )
    determinant = (
        pencil[0, 0] * pencil[1, 1] - pencil[0, 1] * pencil[1, 0]
    )
    roots = np.sort(np.asarray(determinant.roots(), dtype=complex).real)
    if np.max(np.abs(np.asarray(determinant.roots(), dtype=complex).imag)) > 1e-8:
        raise ValueError("shifted indicial roots are not numerically real")
    regular = roots[roots > -0.5]
    if regular.shape != (2,):
        raise ValueError("shifted pencil does not have two finite-energy roots")
    vectors: list[np.ndarray] = []
    flux_vectors: list[np.ndarray] = []
    for root in regular:
        matrix = np.asarray(
            tuple(
                tuple(float(pencil[row, column](root)) for column in range(2))
                for row in range(2)
            )
        )
        _, _, right = np.linalg.svd(matrix)
        vector = right[-1]
        vectors.append(vector)
        flux_vectors.append((root * principal + mixed.T) @ vector)
    leading_multiplier = np.column_stack(flux_vectors) @ np.linalg.inv(
        np.column_stack(vectors)
    )
    return roots, regular, (leading_multiplier + leading_multiplier.T) / 2.0


def _hermite_matrix(
    left_value: np.ndarray,
    left_derivative: np.ndarray,
    right_value: np.ndarray,
    right_derivative: np.ndarray,
    width: float,
    coordinate: float,
) -> tuple[np.ndarray, np.ndarray]:
    s = coordinate
    value = (
        (2 * s**3 - 3 * s**2 + 1) * left_value
        + width * (s**3 - 2 * s**2 + s) * left_derivative
        + (-2 * s**3 + 3 * s**2) * right_value
        + width * (s**3 - s**2) * right_derivative
    )
    derivative = (
        (6 * s**2 - 6 * s) * left_value / width
        + (3 * s**2 - 4 * s + 1) * left_derivative
        + (-6 * s**2 + 6 * s) * right_value / width
        + (3 * s**2 - 2 * s) * right_derivative
    )
    return value, derivative


def centrifugal_riccati_coercivity_probe(
    *,
    target_lower_bound: float = 0.1,
    construction_shift: float = 0.2,
    origin_radius: float = 1.0 / 1024.0,
    mesh_width: float = 1.0 / 512.0,
    residual_samples_per_cell: int = 5,
    profile_step: float = 0.001,
) -> dict[str, object]:
    """Build a floating Riccati multiplier and report proof-target margins."""
    values = (
        target_lower_bound,
        construction_shift,
        origin_radius,
        mesh_width,
        profile_step,
    )
    if not all(isfinite(value) for value in values):
        raise ValueError("all probe parameters must be finite")
    if target_lower_bound <= 0 or construction_shift <= target_lower_bound:
        raise ValueError("construction_shift must exceed a positive target")
    if origin_radius <= 0 or mesh_width <= 0 or profile_step <= 0:
        raise ValueError("radii and steps must be positive")
    if (
        isinstance(residual_samples_per_cell, bool)
        or not isinstance(residual_samples_per_cell, int)
        or residual_samples_per_cell < 3
    ):
        raise ValueError("residual_samples_per_cell must be an integer at least 3")

    curvature = 0.0025
    wall_radius = 4.0
    membrane_tension = 0.001931779647
    shooting_slope, profile_points = solve_hard_wall_skyrmion_profile(
        pion_mass=1.0,
        curvature=curvature,
        wall_radius=wall_radius,
        step=profile_step,
    )
    profile_radii = np.asarray([point[0] for point in profile_points])
    profile_values = np.asarray([point[1] for point in profile_points])
    profile_derivatives = np.asarray([point[2] for point in profile_points])

    def blocks(radius: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
                pion_mass=1.0,
            )["symmetric_hessian_matrix"],
            dtype=float,
        )
        return hessian[:2, :2], hessian[:2, 2:], hessian[2:, 2:]

    roots, regular_roots, leading_multiplier = _shifted_origin_data(
        shooting_slope,
        construction_shift,
    )
    identity = np.eye(2)

    def riccati_rhs(radius: float, multiplier: np.ndarray) -> np.ndarray:
        coordinate, mixed, principal = blocks(radius)
        difference = mixed - multiplier
        result = (
            coordinate
            - construction_shift * identity
            - difference @ np.linalg.solve(principal, difference.T)
        )
        return (result + result.T) / 2.0

    def rk4_step(radius: float, multiplier: np.ndarray, width: float) -> np.ndarray:
        first = riccati_rhs(radius, multiplier)
        second = riccati_rhs(
            radius + width / 2.0,
            multiplier + width * first / 2.0,
        )
        third = riccati_rhs(
            radius + width / 2.0,
            multiplier + width * second / 2.0,
        )
        fourth = riccati_rhs(radius + width, multiplier + width * third)
        result = multiplier + width * (
            first + 2.0 * second + 2.0 * third + fourth
        ) / 6.0
        return (result + result.T) / 2.0

    radii = [origin_radius]
    multipliers = [origin_radius * leading_multiplier]
    multiplier_derivatives = [riccati_rhs(origin_radius, multipliers[0])]
    while radii[-1] < wall_radius:
        width = min(mesh_width, wall_radius - radii[-1])
        next_multiplier = rk4_step(radii[-1], multipliers[-1], width)
        next_radius = radii[-1] + width
        if not np.all(np.isfinite(next_multiplier)):
            raise ValueError("Riccati candidate lost finite continuation")
        radii.append(next_radius)
        multipliers.append(next_multiplier)
        multiplier_derivatives.append(
            riccati_rhs(next_radius, next_multiplier)
        )

    minimum_residual = float("inf")
    minimum_residual_radius = origin_radius
    maximum_symmetry_defect = 0.0
    minimum_principal_eigenvalue = float("inf")
    for index, (left, right) in enumerate(zip(radii, radii[1:])):
        width = right - left
        for coordinate in np.linspace(0.0, 1.0, residual_samples_per_cell):
            multiplier, derivative = _hermite_matrix(
                multipliers[index],
                multiplier_derivatives[index],
                multipliers[index + 1],
                multiplier_derivatives[index + 1],
                width,
                float(coordinate),
            )
            radius = left + float(coordinate) * width
            coordinate_block, mixed, principal = blocks(radius)
            difference = mixed - multiplier
            residual = (
                coordinate_block
                - target_lower_bound * identity
                - difference @ np.linalg.solve(principal, difference.T)
                - derivative
            )
            residual = (residual + residual.T) / 2.0
            eigenvalue = float(np.linalg.eigvalsh(residual)[0])
            if eigenvalue < minimum_residual:
                minimum_residual = eigenvalue
                minimum_residual_radius = radius
            minimum_principal_eigenvalue = min(
                minimum_principal_eigenvalue,
                float(np.linalg.eigvalsh(principal)[0]),
            )
            maximum_symmetry_defect = max(
                maximum_symmetry_defect,
                float(np.max(np.abs(multiplier - multiplier.T))),
            )

    coordinate_wall, mixed_wall, principal_wall = blocks(wall_radius)
    del coordinate_wall
    lapse = 1.0 - curvature * wall_radius**2
    lapse_derivative = -2.0 * curvature * wall_radius
    shape = float(
        static_patch_shell_shape_curvature_coefficient(
            wall_radius=wall_radius,
            curvature=curvature,
            ell=2,
        )["shape_curvature_coefficient"]
    )
    wall_profile_derivative = float(profile_derivatives[-1])
    wall_robin = (
        -2.0 / wall_radius
        - lapse_derivative / (2.0 * lapse)
        - 4.0
        * membrane_tension
        * shape
        / (lapse * wall_profile_derivative**2)
    )
    wall_form = -(
        principal_wall[0, 0] * wall_robin + mixed_wall[0, 0]
    )
    wall_margin = float(wall_form + multipliers[-1][0, 0])
    return {
        "result_type": "floating_matrix_riccati_coercivity_probe",
        "target_lower_bound": target_lower_bound,
        "construction_shift": construction_shift,
        "formal_bulk_margin": construction_shift - target_lower_bound,
        "shooting_slope": shooting_slope,
        "shifted_indicial_roots": tuple(float(value) for value in roots),
        "shifted_finite_energy_roots": tuple(
            float(value) for value in regular_roots
        ),
        "leading_multiplier": tuple(
            tuple(float(value) for value in row) for row in leading_multiplier
        ),
        "origin_radius": origin_radius,
        "mesh_width": mesh_width,
        "mesh_cell_count": len(radii) - 1,
        "residual_samples_per_cell": residual_samples_per_cell,
        "minimum_sampled_principal_eigenvalue": minimum_principal_eigenvalue,
        "minimum_sampled_riccati_residual_eigenvalue": minimum_residual,
        "minimum_residual_radius": minimum_residual_radius,
        "maximum_multiplier_norm": max(
            float(np.linalg.norm(value, 2)) for value in multipliers
        ),
        "maximum_multiplier_symmetry_defect": maximum_symmetry_defect,
        "wall_robin_multiplier": wall_robin,
        "wall_form_coefficient": float(wall_form),
        "allowed_wall_trace_margin": wall_margin,
        "candidate_passes_sampled_preflight": (
            minimum_residual > 0.0
            and minimum_principal_eigenvalue > 0.0
            and wall_margin > 0.0
        ),
        "theorem_route": (
            "interval-enclose P and the Riccati residual on every profile-tube "
            "cell; prove the allowed wall trace margin; then close the first-"
            "order factor form from the smooth Friedrichs core"
        ),
        "claim_boundary": (
            "Floating profile, RK4 multiplier, cubic-Hermite interpolation, "
            "and sampled residuals select a high-margin continuum coercivity "
            "certificate. They do not prove a one-sided spectral bound, "
            "global form closedness, or invertibility of the physical BVP."
        ),
    }


def centrifugal_liouville_coercivity_probe(
    *,
    target_lower_bound: float = 0.05,
    profile_step: float = 0.001,
) -> dict[str, object]:
    """Probe the explicit ``K=sym(M)-P/(2x)`` multiplier globally."""
    if not isfinite(target_lower_bound) or target_lower_bound <= 0:
        raise ValueError("target_lower_bound must be finite and positive")
    if not isfinite(profile_step) or profile_step <= 0:
        raise ValueError("profile_step must be finite and positive")
    curvature = 0.0025
    wall_radius = 4.0
    membrane_tension = 0.001931779647
    shooting_slope, profile_points = solve_hard_wall_skyrmion_profile(
        pion_mass=1.0,
        curvature=curvature,
        wall_radius=wall_radius,
        step=profile_step,
    )
    radii = np.asarray([point[0] for point in profile_points[1:]], dtype=float)
    coordinates: list[np.ndarray] = []
    mixed_blocks: list[np.ndarray] = []
    principal_blocks: list[np.ndarray] = []
    multipliers: list[np.ndarray] = []
    for radius, profile, derivative in profile_points[1:]:
        hessian = np.asarray(
            quadrupole_static_hessian_matrix(
                radius=radius,
                metric_factor=1.0 - curvature * radius**2,
                profile=profile,
                profile_derivative=derivative,
                pion_mass=1.0,
            )["symmetric_hessian_matrix"],
            dtype=float,
        )
        coordinate = hessian[:2, :2]
        mixed = hessian[:2, 2:]
        principal = hessian[2:, 2:]
        coordinates.append(coordinate)
        mixed_blocks.append(mixed)
        principal_blocks.append(principal)
        multipliers.append((mixed + mixed.T) / 2.0 - principal / (2.0 * radius))
    coordinate_array = np.asarray(coordinates)
    mixed_array = np.asarray(mixed_blocks)
    principal_array = np.asarray(principal_blocks)
    multiplier_array = np.asarray(multipliers)
    multiplier_derivative = np.gradient(
        multiplier_array,
        radii,
        axis=0,
        edge_order=2,
    )
    minimum_potential = float("inf")
    minimum_potential_radius = 0.0
    minimum_scaled_principal = float("inf")
    for index, radius in enumerate(radii):
        difference = mixed_array[index] - multiplier_array[index]
        potential = (
            coordinate_array[index]
            - multiplier_derivative[index]
            - difference
            @ np.linalg.solve(principal_array[index], difference.T)
        )
        potential = (potential + potential.T) / 2.0
        eigenvalue = float(np.linalg.eigvalsh(potential)[0])
        if eigenvalue < minimum_potential:
            minimum_potential = eigenvalue
            minimum_potential_radius = float(radius)
        minimum_scaled_principal = min(
            minimum_scaled_principal,
            float(
                np.linalg.eigvalsh(principal_array[index] / radius**2)[0]
            ),
        )
    lapse = 1.0 - curvature * wall_radius**2
    lapse_derivative = -2.0 * curvature * wall_radius
    shape = float(
        static_patch_shell_shape_curvature_coefficient(
            wall_radius=wall_radius,
            curvature=curvature,
            ell=2,
        )["shape_curvature_coefficient"]
    )
    wall_profile_derivative = float(profile_points[-1][2])
    wall_robin = (
        -2.0 / wall_radius
        - lapse_derivative / (2.0 * lapse)
        - 4.0
        * membrane_tension
        * shape
        / (lapse * wall_profile_derivative**2)
    )
    wall_principal = float(principal_array[-1, 0, 0])
    wall_mixed = float(mixed_array[-1, 0, 0])
    wall_form = -(wall_principal * wall_robin + wall_mixed)
    wall_margin = wall_form + float(multiplier_array[-1, 0, 0])
    return {
        "result_type": "floating_explicit_liouville_coercivity_probe",
        "multiplier": "K=sym(M)-P/(2x)",
        "target_lower_bound": target_lower_bound,
        "shooting_slope": shooting_slope,
        "profile_step": profile_step,
        "sample_count": len(radii),
        "minimum_sampled_scaled_principal_eigenvalue": (
            minimum_scaled_principal
        ),
        "minimum_sampled_completed_potential_eigenvalue": minimum_potential,
        "minimum_completed_potential_radius": minimum_potential_radius,
        "sampled_margin_above_target": (
            minimum_potential - target_lower_bound
        ),
        "wall_robin_multiplier": wall_robin,
        "wall_form_coefficient": wall_form,
        "allowed_wall_trace_margin": wall_margin,
        "candidate_passes_sampled_preflight": (
            minimum_scaled_principal > 0
            and minimum_potential > target_lower_bound
            and wall_margin > 0
        ),
        "preferred_certificate": (
            "enclose the exact regular conormal potential W_K-(1/20)I over "
            "the authenticated nonlinear profile tube and prove its two "
            "Sylvester minors positive"
        ),
        "claim_boundary": (
            "Floating profile values and numerical differentiation of K only. "
            "The stable positive margin selects an explicit interval witness "
            "but does not certify continuum coercivity or form closedness."
        ),
    }


def exact_riccati_identity_certificate() -> dict[str, object]:
    """Exercise the completion with exact rational, non-diagonal data."""
    defect = riccati_completion_identity_defect(
        principal=((Fraction(3), Fraction(1)), (Fraction(1), Fraction(2))),
        mixed=((Fraction(1, 3), Fraction(-2, 5)), (Fraction(4, 7), Fraction(1, 6))),
        coordinate=((Fraction(5), Fraction(2, 3)), (Fraction(2, 3), Fraction(4))),
        multiplier=((Fraction(1, 2), Fraction(-1, 4)), (Fraction(-1, 4), Fraction(2, 3))),
        multiplier_derivative=((Fraction(1, 7), Fraction(1, 9)), (Fraction(1, 9), Fraction(-1, 8))),
        field=(Fraction(2, 5), Fraction(-3, 7)),
        derivative=(Fraction(5, 11), Fraction(7, 13)),
        spectral_target=Fraction(1, 10),
    )
    regular_defect = regular_liouville_potential_identity_defect(
        time=Fraction(3, 5),
        principal_bar=(
            (Fraction(3), Fraction(1, 4)),
            (Fraction(1, 4), Fraction(2)),
        ),
        principal_bar_derivative=(
            (Fraction(1, 3), Fraction(-1, 7)),
            (Fraction(-1, 7), Fraction(2, 5)),
        ),
        mixed_bar=(
            (Fraction(2, 3), Fraction(1, 5)),
            (Fraction(-2, 7), Fraction(4, 9)),
        ),
        mixed_bar_derivative=(
            (Fraction(1, 8), Fraction(-1, 6)),
            (Fraction(2, 11), Fraction(3, 10)),
        ),
        coordinate=(
            (Fraction(5), Fraction(2, 3)),
            (Fraction(2, 3), Fraction(4)),
        ),
    )
    regular_verified = all(entry == 0 for row in regular_defect for entry in row)
    return {
        "result_type": "exact_matrix_riccati_completion_identity",
        "identity_defect": str(defect),
        "identity_verified": defect == 0,
        "regular_liouville_identity_defect": tuple(
            tuple(str(entry) for entry in row) for row in regular_defect
        ),
        "regular_liouville_identity_verified": regular_verified,
        "continuum_implication": (
            "P>0, R_alpha>=0, nonnegative allowed wall trace, and vanishing "
            "origin trace imply q[y]>=alpha ||y||_L2^2 on the smooth core"
        ),
    }
