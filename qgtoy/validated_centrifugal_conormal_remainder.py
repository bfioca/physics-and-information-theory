"""Validated finite-cell remainder bounds for the conormal origin system.

The exact conormal system is ``2 t X_t=A(t)X+q(t)``.  This module combines
the authenticated cellwise quintic profile family with rational degree-two
Taylor arithmetic to enclose

``delta=sup ||A(t)-A(0)||_w``

and the three scaled residuals ``E_j(t)/t^3`` of the two homogeneous and one
forced Frobenius columns.  No derivative of the profile remainder is used:
the independently validated variables are ``u=(pi-F)/x`` and ``rho=-F'``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
    regular_rotational_source_from_kernels,
)
from .validated_centrifugal_origin_transfer import (
    DEFAULT_STATE_WEIGHTS,
    _formal_branches,
    _rational_function_interval,
    leading_green_majorant,
)
from .validated_interval import RationalInterval
from .validated_skyrmion_quintic_family import (
    ValidatedSkyrmionQuinticFamily,
    ValidatedSkyrmionQuinticFamilyCell,
    _TaylorModelFamilyTwo,
    _kernel_model,
)


TM = _TaylorModelFamilyTwo
Matrix2 = tuple[tuple[TM, TM], tuple[TM, TM]]
Matrix4 = tuple[
    tuple[TM, TM, TM, TM],
    tuple[TM, TM, TM, TM],
    tuple[TM, TM, TM, TM],
    tuple[TM, TM, TM, TM],
]
Vector2 = tuple[TM, TM]
Vector4 = tuple[TM, TM, TM, TM]


def _abs_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _cosine_model(
    argument: TM,
    *,
    argument_rate_upper: Fraction,
    terms: int,
) -> TM:
    """Enclose ``cos(sqrt(argument))`` through quadratic Taylor order."""
    if terms < 3:
        raise ValueError("quadratic cosine model requires at least three terms")
    total = TM.point(0, argument.horizon)
    power = TM.point(1, argument.horizon)
    for index in range(terms):
        total = total + power.scale(Fraction((-1) ** index, factorial(2 * index)))
        power = power * argument
    ratio = argument_rate_upper * argument.horizon / ((2 * terms + 1) * (2 * terms + 2))
    if ratio >= 1:
        raise ValueError("cosine geometric-tail ratio must be below one")
    tail = (
        argument_rate_upper**terms
        * argument.horizon ** (terms - 3)
        / (factorial(2 * terms) * (1 - ratio))
    )
    return TM(
        total.constant,
        total.linear,
        total.quadratic,
        total.remainder + RationalInterval(-tail, tail),
        total.horizon,
    )


def _matrix_two_inverse(value: Matrix2) -> Matrix2:
    determinant = value[0][0] * value[1][1] - value[0][1] * value[1][0]
    return (
        (value[1][1] / determinant, value[0][1].scale(-1) / determinant),
        (value[1][0].scale(-1) / determinant, value[0][0] / determinant),
    )


def _matrix_two_multiply(left: Matrix2, right: Matrix2) -> Matrix2:
    zero = TM.point(0, left[0][0].horizon)
    return tuple(
        tuple(
            sum(
                (left[row][index] * right[index][column] for index in range(2)),
                zero,
            )
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_two_add(left: Matrix2, right: Matrix2) -> Matrix2:
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_two_scale(value: Matrix2, factor: int | Fraction) -> Matrix2:
    return tuple(
        tuple(value[row][column].scale(factor) for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_two_transpose(value: Matrix2) -> Matrix2:
    return tuple(tuple(value[column][row] for column in range(2)) for row in range(2))  # type: ignore[return-value]


def _fuchs_matrix(coordinate: Matrix2, mixed: Matrix2, principal: Matrix2) -> Matrix4:
    inverse = _matrix_two_inverse(principal)
    transpose = _matrix_two_transpose(mixed)
    identity = (
        (TM.point(1, principal[0][0].horizon), TM.point(0, principal[0][0].horizon)),
        (TM.point(0, principal[0][0].horizon), TM.point(1, principal[0][0].horizon)),
    )
    upper_left = _matrix_two_scale(
        _matrix_two_multiply(inverse, _matrix_two_add(principal, transpose)), -1
    )
    upper_right = inverse
    lower_left = _matrix_two_add(
        coordinate,
        _matrix_two_scale(
            _matrix_two_multiply(_matrix_two_multiply(mixed, inverse), transpose),
            -1,
        ),
    )
    lower_right = _matrix_two_add(
        _matrix_two_multiply(mixed, inverse), _matrix_two_scale(identity, -2)
    )
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
    )  # type: ignore[return-value]


def _fuchs_source(
    mixed: Matrix2,
    principal: Matrix2,
    derivative_source: Vector2,
    coordinate_source: Vector2,
) -> Vector4:
    inverse = _matrix_two_inverse(principal)
    zero = TM.point(0, principal[0][0].horizon)
    upper = tuple(
        sum(
            (inverse[row][column] * derivative_source[column] for column in range(2)),
            zero,
        )
        for row in range(2)
    )
    lower = tuple(
        sum((mixed[row][column] * upper[column] for column in range(2)), zero)
        - coordinate_source[row]
        for row in range(2)
    )
    return upper[0], upper[1], lower[0], lower[1]


def _coefficient_model(
    family: ValidatedSkyrmionQuinticFamily,
    cell: ValidatedSkyrmionQuinticFamilyCell,
    *,
    kernel_terms: int,
) -> tuple[Matrix4, Vector4, Matrix2, Matrix2, Vector2]:
    horizon = family.cutoff**2
    zero = RationalInterval.point(0)
    profile_remainder = RationalInterval(
        -family.remainder_radius, family.remainder_radius
    )
    rho = TM(
        cell.shooting_slopes,
        cell.cubic_coefficient.scale(-3),
        cell.quintic_coefficient.scale(-5),
        profile_remainder,
        horizon,
    )
    u = TM(
        cell.shooting_slopes,
        cell.cubic_coefficient.scale(-1),
        cell.quintic_coefficient.scale(-1),
        profile_remainder.scale(Fraction(1, 7)),
        horizon,
    )
    time = TM(zero, RationalInterval.point(1), zero, zero, horizon)
    argument = time * u.power(2)
    argument_rate = _abs_upper(u.range()) ** 2
    sine_over_radius = u * _kernel_model(
        argument,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    cosine = _cosine_model(
        argument,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    metric = TM.point(1, horizon) - time.scale(family.curvature)
    blocks = regular_conormal_blocks_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine,
        pion_mass_squared=TM.point(family.pion_mass_squared, horizon),
    )
    source = regular_rotational_source_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine,
    )
    coordinate = blocks["coordinate"]
    mixed = blocks["mixed"]
    principal = blocks["principal"]
    derivative_source = source["derivative_source"]
    if not all(
        isinstance(entry, TM)
        for matrix in (coordinate, mixed, principal)
        for row in matrix
        for entry in row
    ) or not all(isinstance(entry, TM) for entry in derivative_source):
        raise TypeError("conormal Taylor construction returned an unexpected scalar")
    return (
        _fuchs_matrix(coordinate, mixed, principal),
        _fuchs_source(
            mixed,
            principal,
            derivative_source,
            source["coordinate_source"],
        ),
        principal,
        mixed,
        derivative_source,
    )


def _variation_bound(matrix: Matrix4, weights: tuple[Fraction, ...]) -> Fraction:
    horizon = matrix[0][0].horizon
    time = RationalInterval(Fraction(0), horizon)
    return max(
        sum(
            _abs_upper(
                time * matrix[row][column].linear
                + time.power(2) * matrix[row][column].quadratic
                + time.power(3) * matrix[row][column].remainder
            )
            * weights[column]
            / weights[row]
            for column in range(4)
        )
        for row in range(4)
    )


def _polynomial_model(
    coefficients: tuple[RationalInterval, RationalInterval, RationalInterval],
    horizon: Fraction,
) -> TM:
    return TM(*coefficients, RationalInterval.point(0), horizon)


def _branch_residual_bound(
    branch: dict[str, object],
    slopes: RationalInterval,
    matrix: Matrix4,
    source: Vector4,
    principal: Matrix2,
    mixed: Matrix2,
    derivative_source: Vector2,
    weights: tuple[Fraction, ...],
) -> Fraction:
    names = ("u0", "v0", "v1", "u1", "v2")
    coefficients = tuple(branch[name] for name in names)
    if not all(hasattr(value, "numerator") for value in coefficients):
        raise TypeError("formal branch coefficients must be rational functions")
    u0, v0, v1, u1, v2 = (
        _rational_function_interval(value, slopes) for value in coefficients
    )
    horizon = matrix[0][0].horizon
    fields = (
        _polynomial_model((-v0, u0 - v1, u1 - v2), horizon),
        _polynomial_model((v0, v1, v2), horizon),
    )
    derivatives = (
        _polynomial_model((-v0, (u0 - v1).scale(3), (u1 - v2).scale(5)), horizon),
        _polynomial_model((v0, v1.scale(3), v2.scale(5)), horizon),
    )
    sigma = int(branch["sigma"])
    zero = TM.point(0, horizon)
    z_full = tuple(
        sum((principal[row][column] * derivatives[column] for column in range(2)), zero)
        + sum((mixed[column][row] * fields[column] for column in range(2)), zero)
        - derivative_source[row].scale(sigma)
        for row in range(2)
    )
    state: Vector4 = (
        fields[0],
        fields[1],
        _polynomial_model(
            (z_full[0].constant, z_full[0].linear, z_full[0].quadratic), horizon
        ),
        _polynomial_model(
            (z_full[1].constant, z_full[1].linear, z_full[1].quadratic), horizon
        ),
    )
    derivative = tuple(
        TM(
            RationalInterval.point(0),
            item.linear.scale(2),
            item.quadratic.scale(4),
            RationalInterval.point(0),
            horizon,
        )
        for item in state
    )
    residual = tuple(
        derivative[row]
        - sum((matrix[row][column] * state[column] for column in range(4)), zero)
        - source[row].scale(sigma)
        for row in range(4)
    )
    # The exact p=1,3,5 recurrence proves the first three coefficients vanish.
    # The Taylor arithmetic's remainder component therefore encloses E/t^3.
    return max(_abs_upper(residual[row].remainder) / weights[row] for row in range(4))


@dataclass(frozen=True)
class ValidatedConormalRemainderCell:
    shooting_slopes: RationalInterval
    green_majorant: Fraction
    coefficient_variation_bound: Fraction
    contraction_bound: Fraction
    branch_residual_bounds: tuple[Fraction, Fraction, Fraction]
    branch_remainder_radii: tuple[Fraction, Fraction, Fraction]
    branch_endpoint_state_error_bounds: tuple[
        tuple[Fraction, Fraction, Fraction, Fraction],
        tuple[Fraction, Fraction, Fraction, Fraction],
        tuple[Fraction, Fraction, Fraction, Fraction],
    ]


@dataclass(frozen=True)
class ValidatedConormalRemainder:
    shooting_slopes: RationalInterval
    cutoff: Fraction
    state_weights: tuple[Fraction, Fraction, Fraction, Fraction]
    cells: tuple[ValidatedConormalRemainderCell, ...]
    maximum_green_majorant: Fraction
    maximum_coefficient_variation_bound: Fraction
    maximum_contraction_bound: Fraction
    maximum_branch_residual_bounds: tuple[Fraction, Fraction, Fraction]
    maximum_branch_remainder_radii: tuple[Fraction, Fraction, Fraction]
    maximum_branch_endpoint_state_error_bounds: tuple[
        tuple[Fraction, Fraction, Fraction, Fraction],
        tuple[Fraction, Fraction, Fraction, Fraction],
        tuple[Fraction, Fraction, Fraction, Fraction],
    ]
    branch_order: tuple[str, str, str]
    closes: bool


def validate_centrifugal_conormal_remainder(
    profile_family: ValidatedSkyrmionQuinticFamily,
    *,
    state_weights: tuple[Fraction, Fraction, Fraction, Fraction] = (
        DEFAULT_STATE_WEIGHTS
    ),
    kernel_terms: int = 5,
    green_slope_cells: int = 4,
) -> ValidatedConormalRemainder:
    """Validate coefficient drift and all three affine-column remainders."""
    if not isinstance(profile_family, ValidatedSkyrmionQuinticFamily):
        raise TypeError("profile_family must be a ValidatedSkyrmionQuinticFamily")
    if len(state_weights) != 4 or any(
        not isinstance(value, Fraction) or value <= 0 for value in state_weights
    ):
        raise ValueError("state_weights must contain four positive Fractions")
    if kernel_terms < 3:
        raise ValueError("kernel_terms must be at least three")
    branches = _formal_branches()
    cells: list[ValidatedConormalRemainderCell] = []
    for profile_cell in profile_family.cells:
        matrix, source, principal, mixed, derivative_source = _coefficient_model(
            profile_family, profile_cell, kernel_terms=kernel_terms
        )
        delta = _variation_bound(matrix, state_weights)
        gamma = leading_green_majorant(
            profile_cell.shooting_slopes,
            state_weights=state_weights,
            slope_cells=green_slope_cells,
        )
        contraction = gamma * delta
        if contraction >= 1:
            raise ValueError("conormal Green contraction does not close")
        residuals = tuple(
            _branch_residual_bound(
                branch,
                profile_cell.shooting_slopes,
                matrix,
                source,
                principal,
                mixed,
                derivative_source,
                state_weights,
            )
            for branch in branches
        )
        radii = tuple(
            2 * gamma * residual / (1 - contraction) for residual in residuals
        )
        if any(
            gamma * residual + contraction * radius > radius
            for residual, radius in zip(residuals, radii, strict=True)
        ):
            raise ValueError("conormal branch radii inequality does not close")
        endpoint_factor = profile_family.cutoff**6
        endpoint_errors = tuple(
            tuple(endpoint_factor * radius * weight for weight in state_weights)
            for radius in radii
        )
        cells.append(
            ValidatedConormalRemainderCell(
                shooting_slopes=profile_cell.shooting_slopes,
                green_majorant=gamma,
                coefficient_variation_bound=delta,
                contraction_bound=contraction,
                branch_residual_bounds=residuals,
                branch_remainder_radii=radii,
                branch_endpoint_state_error_bounds=endpoint_errors,
            )
        )
    result = tuple(cells)
    return ValidatedConormalRemainder(
        shooting_slopes=profile_family.shooting_slopes,
        cutoff=profile_family.cutoff,
        state_weights=state_weights,
        cells=result,
        maximum_green_majorant=max(cell.green_majorant for cell in result),
        maximum_coefficient_variation_bound=max(
            cell.coefficient_variation_bound for cell in result
        ),
        maximum_contraction_bound=max(cell.contraction_bound for cell in result),
        maximum_branch_residual_bounds=tuple(
            max(cell.branch_residual_bounds[index] for cell in result)
            for index in range(3)
        ),
        maximum_branch_remainder_radii=tuple(
            max(cell.branch_remainder_radii[index] for cell in result)
            for index in range(3)
        ),
        maximum_branch_endpoint_state_error_bounds=tuple(
            tuple(
                max(
                    cell.branch_endpoint_state_error_bounds[branch][component]
                    for cell in result
                )
                for component in range(4)
            )
            for branch in range(3)
        ),
        branch_order=(
            "linear_homogeneous",
            "cubic_homogeneous",
            "forced_particular",
        ),
        closes=True,
    )
