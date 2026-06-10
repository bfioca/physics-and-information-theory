"""Exact conormal Fuchs algebra for the centrifugal origin transfer.

For a weak-form density with blocks ``C, M, P`` and source ``(s0,s1)``, set

``a=y/x``, ``p=P y' + M.T y - s1``, ``z=p/x^2``, and ``t=x^2``.

When ``C=Cbar(t)``, ``M=x Mbar(t)``, ``P=x^2 Pbar(t)``,
``s0=x shat0(t)``, and ``s1=x^2 shat1(t)``, the Euler equation is equivalent
to the regular singular first-order system ``2 t X_t=A(t)X+q(t)`` for
``X=(a,z)``.  The physical rotational source is more regular:
``s0=O(x^3)`` and ``s1=O(x^4)``, so both hatted sources vanish at least as
``t`` and the first forced branch is cubic.  This module proves the exact
leading spectrum, constructs its Green projectors, and preserves the exact
degree-two affine Frobenius endpoint map.

The profile has a validated quintic family on the finite origin cell, but a
Taylor-model enclosure of every entry of ``A(t)`` and ``q(t)`` is not yet
available.  Consequently the radii validator below is a conditional theorem:
its inputs must be supplied by such coefficient enclosures before it becomes
a validated finite-cell transfer.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from itertools import permutations

from .centrifugal_skyrmion_frobenius import (
    _leading_coefficients,
    _profile_coefficients,
    _recurrence_data,
    _solve_branch,
)
from .centrifugal_skyrmion_origin import (
    Polynomial,
    centrifugal_origin_leading_hessian,
)
from .validated_interval import RationalInterval
from .validated_skyrmion_origin import RationalPolynomial, _RationalFunction


RF = _RationalFunction
Matrix = tuple[tuple[RF, ...], ...]
IntervalMatrix = tuple[tuple[RationalInterval, ...], ...]
Vector = tuple[RF, RF]
DEFAULT_STATE_WEIGHTS = (
    Fraction(36, 25),
    Fraction(73, 50),
    Fraction(13, 20),
    Fraction(73, 100),
)


def _rf(value: int | Fraction | Polynomial | RF) -> RF:
    if isinstance(value, _RationalFunction):
        return value
    if isinstance(value, tuple):
        return RF(RationalPolynomial(value), RationalPolynomial((Fraction(1),)))
    return RF.constant(value)


def _matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(len(left[0])))
        for row in range(len(left))
    )


def _matrix_scale(value: Matrix, factor: int | Fraction) -> Matrix:
    return tuple(tuple(entry.scale(factor) for entry in row) for row in value)


def _matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(
                (
                    left[row][index] * right[index][column]
                    for index in range(len(right))
                ),
                RF.constant(0),
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def _identity(size: int) -> Matrix:
    return tuple(
        tuple(_rf(1 if row == column else 0) for column in range(size))
        for row in range(size)
    )


def _matrix_shift(value: Matrix, scalar: int | Fraction) -> Matrix:
    return _matrix_add(value, _matrix_scale(_identity(len(value)), -Fraction(scalar)))


def _inverse_two(value: Matrix) -> Matrix:
    determinant = value[0][0] * value[1][1] - value[0][1] * value[1][0]
    return (
        (value[1][1] / determinant, value[0][1].scale(-1) / determinant),
        (value[1][0].scale(-1) / determinant, value[0][0] / determinant),
    )


def _transpose(value: Matrix) -> Matrix:
    return tuple(
        tuple(value[column][row] for column in range(len(value)))
        for row in range(len(value[0]))
    )


def _block_matrix(
    upper_left: Matrix,
    upper_right: Matrix,
    lower_left: Matrix,
    lower_right: Matrix,
) -> Matrix:
    return tuple(
        tuple(
            (
                upper_left
                if row < 2 and column < 2
                else upper_right
                if row < 2
                else lower_left
                if column < 2
                else lower_right
            )[row % 2][column % 2]
            for column in range(4)
        )
        for row in range(4)
    )


def conormal_fuchs_matrix(
    coordinate: Matrix,
    mixed: Matrix,
    principal: Matrix,
) -> Matrix:
    """Return the exact block matrix ``A`` from ``Cbar,Mbar,Pbar``.

    The source-independent identity is

    ``A11=-P^-1(P+M.T)``, ``A12=P^-1``,

    ``A21=C-M P^-1 M.T``, ``A22=M P^-1-2I``.
    """
    if any(
        len(value) != 2 or any(len(row) != 2 for row in value)
        for value in (coordinate, mixed, principal)
    ):
        raise ValueError("all conormal blocks must be 2 by 2")
    principal_inverse = _inverse_two(principal)
    mixed_transpose = _transpose(mixed)
    upper_left = _matrix_scale(
        _matrix_multiply(
            principal_inverse,
            _matrix_add(principal, mixed_transpose),
        ),
        -1,
    )
    upper_right = principal_inverse
    lower_left = _matrix_add(
        coordinate,
        _matrix_scale(
            _matrix_multiply(
                _matrix_multiply(mixed, principal_inverse), mixed_transpose
            ),
            -1,
        ),
    )
    lower_right = _matrix_add(
        _matrix_multiply(mixed, principal_inverse),
        _matrix_scale(_identity(2), -2),
    )
    return _block_matrix(upper_left, upper_right, lower_left, lower_right)


def conormal_fuchs_source(
    mixed: Matrix,
    principal: Matrix,
    derivative_source: Vector,
    coordinate_source: Vector,
) -> tuple[RF, RF, RF, RF]:
    """Return ``q=(P^-1 shat1, M P^-1 shat1-shat0)`` exactly."""
    if any(
        len(value) != 2 or any(len(row) != 2 for row in value)
        for value in (mixed, principal)
    ):
        raise ValueError("mixed and principal blocks must be 2 by 2")
    principal_inverse = _inverse_two(principal)
    upper = tuple(
        sum(
            (
                principal_inverse[row][column] * derivative_source[column]
                for column in range(2)
            ),
            RF.constant(0),
        )
        for row in range(2)
    )
    lower = tuple(
        sum(
            (mixed[row][column] * upper[column] for column in range(2)),
            RF.constant(0),
        )
        - coordinate_source[row]
        for row in range(2)
    )
    return upper[0], upper[1], lower[0], lower[1]


@cache
def centrifugal_origin_leading_fuchs_matrix() -> Matrix:
    """Build ``A_b(0)`` from the exact leading Hessian blocks."""
    hessian = centrifugal_origin_leading_hessian()
    coordinate = tuple(
        tuple(_rf(hessian[row][column]) for column in range(2)) for row in range(2)
    )
    mixed = tuple(
        tuple(_rf(hessian[row][2 + column]) for column in range(2)) for row in range(2)
    )
    principal = tuple(
        tuple(_rf(hessian[2 + row][2 + column]) for column in range(2))
        for row in range(2)
    )
    return conormal_fuchs_matrix(coordinate, mixed, principal)


def _determinant(value: Matrix) -> RF:
    size = len(value)
    total = RF.constant(0)
    for ordering in permutations(range(size)):
        inversions = sum(
            ordering[left] > ordering[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = RF.constant((-1) ** inversions)
        for row, column in enumerate(ordering):
            term = term * value[row][column]
        total = total + term
    return total


@cache
def leading_spectrum_checks() -> dict[int, bool]:
    """Verify the four shifted indicial eigenvalues over ``Q(b)``."""
    matrix = centrifugal_origin_leading_fuchs_matrix()
    return {
        eigenvalue: _determinant(_matrix_shift(matrix, eigenvalue)).exactly_equals(
            _rf(0)
        )
        for eigenvalue in (0, 2, -3, -5)
    }


def _polynomial_interval(
    polynomial: RationalPolynomial,
    argument: RationalInterval,
) -> RationalInterval:
    value = RationalInterval.point(0)
    for coefficient in reversed(polynomial.coefficients):
        value = value * argument + coefficient
    return value


def _rational_function_interval(
    value: RF, argument: RationalInterval
) -> RationalInterval:
    numerator = _polynomial_interval(value.numerator, argument)
    denominator = _polynomial_interval(value.denominator, argument)
    if denominator.contains_zero():
        raise ZeroDivisionError("rational-function denominator enclosure contains zero")
    return numerator / denominator


@cache
def leading_green_projectors() -> dict[int, Matrix]:
    """Return exact spectral projectors of ``A_b(0)`` over ``Q(b)``."""
    matrix = centrifugal_origin_leading_fuchs_matrix()
    eigenvalues = (0, 2, -3, -5)
    projectors: dict[int, Matrix] = {}
    for eigenvalue in eigenvalues:
        projector = _identity(4)
        denominator = Fraction(1)
        for other in eigenvalues:
            if other == eigenvalue:
                continue
            projector = _matrix_multiply(projector, _matrix_shift(matrix, other))
            denominator *= eigenvalue - other
        projectors[eigenvalue] = _matrix_scale(projector, Fraction(1, denominator))
    return projectors


@cache
def _interval_matrix_multiply(
    left: IntervalMatrix,
    right: IntervalMatrix,
) -> IntervalMatrix:
    return tuple(
        tuple(
            sum(
                (
                    left[row][index] * right[index][column]
                    for index in range(len(right))
                ),
                RationalInterval.point(0),
            )
            for column in range(len(right[0]))
        )
        for row in range(len(left))
    )


def _interval_matrix_shift(
    value: IntervalMatrix,
    scalar: int,
) -> IntervalMatrix:
    return tuple(
        tuple(
            value[row][column] - (scalar if row == column else 0)
            for column in range(len(value))
        )
        for row in range(len(value))
    )


def _green_majorant_on_cell(
    shooting_slopes: RationalInterval,
    state_weights: tuple[Fraction, Fraction, Fraction, Fraction],
) -> Fraction:
    matrix = centrifugal_origin_leading_fuchs_matrix()
    interval_matrix = tuple(
        tuple(_rational_function_interval(entry, shooting_slopes) for entry in row)
        for row in matrix
    )
    identity = tuple(
        tuple(RationalInterval.point(1 if row == column else 0) for column in range(4))
        for row in range(4)
    )
    row_bounds = [Fraction(0) for _ in range(4)]
    for eigenvalue in (0, 2, -3, -5):
        projector = identity
        projector_denominator = Fraction(1)
        for other in (0, 2, -3, -5):
            if other == eigenvalue:
                continue
            projector = _interval_matrix_multiply(
                projector,
                _interval_matrix_shift(interval_matrix, other),
            )
            projector_denominator *= eigenvalue - other
        for row in range(4):
            for column in range(4):
                enclosure = projector[row][column].scale(
                    Fraction(1, projector_denominator)
                )
                row_bounds[row] += (
                    max(abs(enclosure.lower), abs(enclosure.upper))
                    * state_weights[column]
                    / (state_weights[row] * Fraction(6 - eigenvalue))
                )
    return max(row_bounds)


@cache
def leading_green_majorant(
    shooting_slopes: RationalInterval,
    *,
    state_weights: tuple[Fraction, Fraction, Fraction, Fraction] = (
        DEFAULT_STATE_WEIGHTS
    ),
    slope_cells: int = 128,
) -> Fraction:
    """Bound the degree-three Green operator in a weighted infinity norm.

    For ``2t R_t=(A0-6I)R+H``, the integral denominator is
    ``6-lambda`` on the ``lambda`` eigenspace. Cellwise interval evaluation
    of the exact Lagrange formula gives a rigorous uniform bound while
    controlling repeated-parameter inflation. The norm is
    ``max_i |X_i|/state_weights[i]``.
    """
    if not isinstance(shooting_slopes, RationalInterval):
        raise TypeError("shooting_slopes must be a RationalInterval")
    if (
        not isinstance(state_weights, tuple)
        or len(state_weights) != 4
        or any(not isinstance(value, Fraction) or value <= 0 for value in state_weights)
    ):
        raise ValueError("state_weights must contain four positive Fractions")
    if (
        isinstance(slope_cells, bool)
        or not isinstance(slope_cells, int)
        or slope_cells < 1
    ):
        raise ValueError("slope_cells must be a positive integer")
    width = shooting_slopes.width / slope_cells
    return max(
        _green_majorant_on_cell(
            RationalInterval(
                shooting_slopes.lower + index * width,
                shooting_slopes.lower + (index + 1) * width,
            ),
            state_weights,
        )
        for index in range(slope_cells)
    )


@dataclass(frozen=True)
class ConditionalRadiiCertificate:
    green_majorant: Fraction
    coefficient_variation_bound: Fraction
    residual_bound: Fraction
    remainder_radius: Fraction
    contraction_bound: Fraction
    radii_left_hand_side: Fraction
    closes: bool


def validate_conditional_radii_inequality(
    *,
    green_majorant: Fraction,
    coefficient_variation_bound: Fraction,
    residual_bound: Fraction,
    remainder_radius: Fraction,
) -> ConditionalRadiiCertificate:
    """Check the exact Fuchs fixed-point radii inequality.

    This proves a transfer only when ``coefficient_variation_bound`` encloses
    ``sup ||A(t)-A(0)||_infinity`` and ``residual_bound`` encloses the scaled
    degree-two residual ``e`` on the full cell.
    """
    values = (
        green_majorant,
        coefficient_variation_bound,
        residual_bound,
        remainder_radius,
    )
    if any(not isinstance(value, Fraction) or value < 0 for value in values):
        raise ValueError("radii inputs must be nonnegative Fractions")
    if remainder_radius == 0:
        raise ValueError("remainder_radius must be positive")
    contraction = green_majorant * coefficient_variation_bound
    left_hand_side = green_majorant * residual_bound + contraction * remainder_radius
    return ConditionalRadiiCertificate(
        green_majorant=green_majorant,
        coefficient_variation_bound=coefficient_variation_bound,
        residual_bound=residual_bound,
        remainder_radius=remainder_radius,
        contraction_bound=contraction,
        radii_left_hand_side=left_hand_side,
        closes=contraction < 1 and left_hand_side <= remainder_radius,
    )


@dataclass(frozen=True)
class FormalAffineEndpointTransfer:
    cutoff: Fraction
    shooting_slopes: RationalInterval
    homogeneous_field_columns: tuple[tuple[RationalInterval, RationalInterval], ...]
    homogeneous_derivative_columns: tuple[
        tuple[RationalInterval, RationalInterval], ...
    ]
    forced_field: tuple[RationalInterval, RationalInterval]
    forced_derivative: tuple[RationalInterval, RationalInterval]
    residual_order: str
    is_finite_cell_enclosure: bool


def _formal_branches() -> tuple[dict[str, object], ...]:
    b = RF.variable()
    q = b.power(2)
    cubic, quintic = _profile_coefficients()
    leading = _leading_coefficients(cubic)
    matrix, lower, force = _recurrence_data(cubic, quintic)
    return (
        _solve_branch(
            name="linear_homogeneous",
            sigma=0,
            u0=_rf(0),
            v0=_rf(1),
            v1=leading[1] / leading[2],
            leading=leading,
            matrix=matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="cubic_homogeneous",
            sigma=0,
            u0=(_rf(10) + q.scale(56)).scale(Fraction(1, 45)),
            v0=_rf(0),
            v1=(_rf(4) + q.scale(56)).scale(Fraction(1, 45)),
            leading=leading,
            matrix=matrix,
            lower=lower,
            force=force,
        ),
        _solve_branch(
            name="forced_particular",
            sigma=1,
            u0=_rf(0),
            v0=_rf(0),
            v1=b * (_rf(1) - q.scale(4)) / (_rf(10) + q.scale(56)),
            leading=leading,
            matrix=matrix,
            lower=lower,
            force=force,
        ),
    )


def _endpoint_column(
    branch: dict[str, object],
    cutoff: Fraction,
    slopes: RationalInterval,
) -> tuple[
    tuple[RationalInterval, RationalInterval],
    tuple[RationalInterval, RationalInterval],
]:
    u0 = branch["u0"]
    v0 = branch["v0"]
    v1 = branch["v1"]
    u1 = branch["u1"]
    v2 = branch["v2"]
    if not all(isinstance(value, RF) for value in (u0, v0, v1, u1, v2)):
        raise TypeError("formal branch coefficients must be rational functions")
    time = cutoff**2
    radial = v0.scale(-1) + (u0 - v1).scale(time) + (u1 - v2).scale(time**2)
    tangential = v0 + v1.scale(time) + v2.scale(time**2)
    radial_derivative = (
        v0.scale(-1) + (u0 - v1).scale(3 * time) + (u1 - v2).scale(5 * time**2)
    )
    tangential_derivative = v0 + v1.scale(3 * time) + v2.scale(5 * time**2)
    field = tuple(
        _rational_function_interval(value.scale(cutoff), slopes)
        for value in (radial, tangential)
    )
    derivative = tuple(
        _rational_function_interval(value, slopes)
        for value in (radial_derivative, tangential_derivative)
    )
    return field, derivative


def formal_affine_endpoint_transfer(
    shooting_slopes: RationalInterval,
    *,
    cutoff: Fraction = Fraction(1, 16),
) -> FormalAffineEndpointTransfer:
    """Return the exact degree-two affine endpoint map through ``x^5``.

    The two homogeneous columns multiply the free regular amplitudes.  The
    forced vector has unit rotational forcing.  This map is exact as a formal
    truncation; it is deliberately not labeled a finite-cell enclosure.
    """
    if not isinstance(shooting_slopes, RationalInterval):
        raise TypeError("shooting_slopes must be a RationalInterval")
    if not isinstance(cutoff, Fraction) or cutoff <= 0:
        raise ValueError("cutoff must be a positive Fraction")
    branches = _formal_branches()
    endpoints = tuple(
        _endpoint_column(branch, cutoff, shooting_slopes) for branch in branches
    )
    return FormalAffineEndpointTransfer(
        cutoff=cutoff,
        shooting_slopes=shooting_slopes,
        homogeneous_field_columns=(endpoints[0][0], endpoints[1][0]),
        homogeneous_derivative_columns=(endpoints[0][1], endpoints[1][1]),
        forced_field=endpoints[2][0],
        forced_derivative=endpoints[2][1],
        residual_order=(
            "field Euler recurrence solved through x^5; t^3 divisibility "
            "of the conormal X residual remains to be checked"
        ),
        is_finite_cell_enclosure=False,
    )


def centrifugal_origin_conormal_certificate(
    shooting_slopes: RationalInterval,
) -> dict[str, object]:
    """Summarize the exact theorem and the remaining validation boundary."""
    checks = leading_spectrum_checks()
    gamma = leading_green_majorant(shooting_slopes)
    transfer = formal_affine_endpoint_transfer(shooting_slopes)
    return {
        "result_type": "exact_conormal_fuchs_origin_transfer_scaffold",
        "conormal_variables": "a=y/x, p=P y'+M^T y-s1, z=p/x^2, X=(a,z)",
        "fuchs_system": "2t X_t=A_b(t)X+q_b(t)",
        "source_blocks": "q1=Pbar^-1 shat1; q2=Mbar Pbar^-1 shat1-shat0",
        "leading_spectrum": (0, 2, -3, -5),
        "leading_spectrum_checks": checks,
        "projector_construction": (
            "exact Lagrange polynomials in A0 over the four distinct "
            "verified eigenvalues"
        ),
        "green_majorant_exact": str(gamma),
        "green_majorant_decimal": float(gamma),
        "green_majorant_state_weights": tuple(
            str(value) for value in DEFAULT_STATE_WEIGHTS
        ),
        "green_majorant_slope_cells": 128,
        "degree_two_field_germ": transfer.residual_order,
        "affine_endpoint_map_preserved": True,
        "finite_cell_enclosure": False,
        "claim_boundary": (
            "The conormal identity, leading spectrum, Green projectors, and "
            "degree-two affine germ are exact. A finite-cell transfer still "
            "requires rational Taylor-model bounds for A(t)-A(0) and the "
            "scaled residual e(t) using the validated quintic profile family."
        ),
    }
