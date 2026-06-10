"""Direct form-dual bound for weak centrifugal adjoint residuals.

The adjoint residual on a positive-radius cell has the natural weak form

``R(v)=integral (r0 dot v+r1 dot v') dx``.

It is incorrect to assign ``r1`` an ``L2`` strong-residual norm.  Instead use
the Liouville square completion

``d=v'+P^-1(M^T-K)v`` and
``x d=x v'+T v``, ``T=I/2-Pbar^-1 Abar``.

Then

``R(v)=integral [(r1/x) dot (x d)+(r0-T^T r1/x) dot v] dx``.

If ``Pbar >= p0 I`` and the completed potential is at least ``alpha I``,
Cauchy--Schwarz in the direct-sum completed-square norm gives a rigorous
energy-dual bound.  A wall residual is added in the same quadratic sum using
the positive wall trace margin.

This module deliberately does not manufacture the missing regular-origin
master load.  Its physical certificate is therefore a
positive-radius-plus-wall partial bound until a loaded origin residual is
supplied independently.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_centrifugal_adjoint_bulk_load import (
    ValidatedWeakAdjointResidualCell,
)
from .validated_centrifugal_response_residual import (
    IntervalMatrix2,
    IntervalVector2,
    ValidatedConormalStrongCell,
)
from .validated_interval import RationalInterval, sqrt_fraction_interval


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _transpose(matrix: IntervalMatrix2) -> IntervalMatrix2:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _matrix_subtract(
    left: IntervalMatrix2, right: IntervalMatrix2
) -> IntervalMatrix2:
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_scale(
    matrix: IntervalMatrix2, scalar: RationalInterval | Fraction
) -> IntervalMatrix2:
    return tuple(
        tuple(matrix[row][column] * scalar for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_multiply(
    left: IntervalMatrix2, right: IntervalMatrix2
) -> IntervalMatrix2:
    zero = RationalInterval.point(0)
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(2)),
                zero,
            )
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_inverse(matrix: IntervalMatrix2) -> IntervalMatrix2:
    determinant = (
        matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    )
    if determinant.contains_zero():
        raise ValueError("principal determinant enclosure contains zero")
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def _matrix_vector(
    matrix: IntervalMatrix2, vector: IntervalVector2
) -> IntervalVector2:
    return tuple(
        row[0] * vector[0] + row[1] * vector[1] for row in matrix
    )  # type: ignore[return-value]


@dataclass(frozen=True)
class ValidatedAdjointEnergyDualCell:
    """One positive-radius completed-square residual enclosure."""

    radius: RationalInterval
    completed_derivative_coefficient: IntervalVector2
    completed_value_coefficient: IntervalVector2
    completed_multiplier: IntervalMatrix2
    principal_shifted_first_minor_lower: Fraction
    principal_shifted_determinant_lower: Fraction
    derivative_squared_dual_upper: Fraction
    value_squared_dual_upper: Fraction
    squared_dual_upper: Fraction


def validated_adjoint_energy_dual_cell(
    residual: ValidatedWeakAdjointResidualCell,
    coefficients: ValidatedConormalStrongCell,
    *,
    principal_lower_bound: Fraction,
    completed_potential_lower_bound: Fraction,
) -> ValidatedAdjointEnergyDualCell:
    """Lift one weak coefficient box into the completed-square dual norm."""
    if residual.radius != coefficients.radius:
        raise ValueError("residual and conormal coefficient cells differ")
    if principal_lower_bound <= 0 or completed_potential_lower_bound <= 0:
        raise ValueError("completed-square lower bounds must be positive")

    point = RationalInterval.point
    radius = residual.radius
    principal = coefficients.principal
    principal_bar = tuple(
        tuple(principal[row][column] / radius.power(2) for column in range(2))
        for row in range(2)
    )
    shifted = (
        (
            principal_bar[0][0] - principal_lower_bound,
            principal_bar[0][1],
        ),
        (
            principal_bar[1][0],
            principal_bar[1][1] - principal_lower_bound,
        ),
    )
    shifted_determinant = (
        shifted[0][0] * shifted[1][1] - shifted[0][1] * shifted[1][0]
    )
    if shifted[0][0].lower <= 0 or shifted_determinant.lower <= 0:
        raise ValueError("Pbar-principal_lower_bound*I is not certified positive")

    antisymmetric_mixed = _matrix_scale(
        _matrix_subtract(coefficients.mixed, _transpose(coefficients.mixed)),
        Fraction(1, 2),
    )
    identity_half: IntervalMatrix2 = (
        (point(Fraction(1, 2)), point(0)),
        (point(0), point(Fraction(1, 2))),
    )
    # x P^-1 A = Pbar^-1 Abar.  The physical blocks retain useful shared
    # scaling on the narrow authenticated radial cells.
    multiplier = _matrix_subtract(
        identity_half,
        _matrix_scale(
            _matrix_multiply(_matrix_inverse(principal), antisymmetric_mixed),
            radius,
        ),
    )
    derivative_coefficient = tuple(
        entry / radius for entry in residual.test_derivative_coefficient
    )
    multiplier_term = _matrix_vector(
        _transpose(multiplier), derivative_coefficient  # type: ignore[arg-type]
    )
    value_coefficient = tuple(
        left - right
        for left, right in zip(
            residual.test_value_coefficient, multiplier_term, strict=True
        )
    )
    width = radius.width
    derivative_squared = width * sum(
        _absolute_upper(entry) ** 2 for entry in derivative_coefficient
    ) / principal_lower_bound
    value_squared = width * sum(
        _absolute_upper(entry) ** 2 for entry in value_coefficient
    ) / completed_potential_lower_bound
    return ValidatedAdjointEnergyDualCell(
        radius=radius,
        completed_derivative_coefficient=derivative_coefficient,  # type: ignore[arg-type]
        completed_value_coefficient=value_coefficient,  # type: ignore[arg-type]
        completed_multiplier=multiplier,
        principal_shifted_first_minor_lower=shifted[0][0].lower,
        principal_shifted_determinant_lower=shifted_determinant.lower,
        derivative_squared_dual_upper=derivative_squared,
        value_squared_dual_upper=value_squared,
        squared_dual_upper=derivative_squared + value_squared,
    )


@dataclass(frozen=True)
class ValidatedPositiveRadiusWallAdjointDualBound:
    """Partial adjoint dual bound with the regular-origin load omitted."""

    cells: tuple[ValidatedAdjointEnergyDualCell, ...]
    positive_radius_domain: RationalInterval
    principal_lower_bound: Fraction
    completed_potential_lower_bound: Fraction
    wall_trace_margin_lower_bound: Fraction
    bulk_derivative_squared_upper: Fraction
    bulk_value_squared_upper: Fraction
    wall_squared_upper: Fraction
    partial_squared_dual_upper: Fraction
    partial_energy_dual_upper: Fraction
    dominant_cell_index: int
    dominant_cell_radius: RationalInterval
    regular_origin_master_load_included: bool
    full_loaded_adjoint_residual_certified: bool


def certify_positive_radius_wall_adjoint_dual_bound(
    cells: tuple[ValidatedAdjointEnergyDualCell, ...],
    *,
    wall_residual: RationalInterval,
    wall_trace_margin_lower_bound: Fraction,
    principal_lower_bound: Fraction,
    completed_potential_lower_bound: Fraction,
    sqrt_bisection_steps: int = 160,
) -> ValidatedPositiveRadiusWallAdjointDualBound:
    """Compose bulk weak cells and the wall trace in one quadratic estimate.

    The regular-origin master load is intentionally absent.  Consequently the
    returned norm is a partial bound and must not be passed to the full
    dual-weighted response enclosure as ``delta_z``.
    """
    if not cells:
        raise ValueError("at least one positive-radius residual cell is required")
    if min(
        principal_lower_bound,
        completed_potential_lower_bound,
        wall_trace_margin_lower_bound,
    ) <= 0:
        raise ValueError("all completed-square and wall bounds must be positive")
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("positive-radius residual cells are not contiguous")
    derivative = sum(
        (cell.derivative_squared_dual_upper for cell in cells), Fraction(0)
    )
    value = sum((cell.value_squared_dual_upper for cell in cells), Fraction(0))
    wall_absolute = _absolute_upper(wall_residual)
    wall = wall_absolute**2 / wall_trace_margin_lower_bound
    squared = derivative + value + wall
    norm = sqrt_fraction_interval(
        squared, bisection_steps=sqrt_bisection_steps
    ).upper
    dominant_index = max(
        range(len(cells)), key=lambda index: cells[index].squared_dual_upper
    )
    return ValidatedPositiveRadiusWallAdjointDualBound(
        cells=cells,
        positive_radius_domain=RationalInterval(
            cells[0].radius.lower, cells[-1].radius.upper
        ),
        principal_lower_bound=principal_lower_bound,
        completed_potential_lower_bound=completed_potential_lower_bound,
        wall_trace_margin_lower_bound=wall_trace_margin_lower_bound,
        bulk_derivative_squared_upper=derivative,
        bulk_value_squared_upper=value,
        wall_squared_upper=wall,
        partial_squared_dual_upper=squared,
        partial_energy_dual_upper=norm,
        dominant_cell_index=dominant_index,
        dominant_cell_radius=cells[dominant_index].radius,
        regular_origin_master_load_included=False,
        full_loaded_adjoint_residual_certified=False,
    )


def combine_loaded_origin_squared_dual_upper(
    partial: ValidatedPositiveRadiusWallAdjointDualBound,
    *,
    loaded_origin_l2_squared_upper: Fraction,
    sqrt_bisection_steps: int = 160,
) -> Fraction:
    """Show the valid final composition once a loaded origin bound exists.

    A strong loaded origin residual contributes ``||r||_2^2/alpha`` to the
    same direct-sum squared dual estimate.  The current physical audit does not
    call this function because only the *zero-load* origin operator action has
    been certified.
    """
    if loaded_origin_l2_squared_upper < 0:
        raise ValueError("loaded origin L2-square bound must be nonnegative")
    squared = (
        partial.partial_squared_dual_upper
        + loaded_origin_l2_squared_upper
        / partial.completed_potential_lower_bound
    )
    return sqrt_fraction_interval(
        squared, bisection_steps=sqrt_bisection_steps
    ).upper
