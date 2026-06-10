"""Physical endpoint tubes for the validated conormal origin transfer.

The finite-cell theorem controls ``X=(a,z)`` with ``a=y/x`` and
``z=(P y' + M.T y - s1)/x^2``.  At the endpoint this module reconstructs

``y=x a`` and ``y'=Pbar^-1(z-Mbar.T a+sigma*shat1)``

with the same profile cells and coefficient Taylor models used by the
conormal remainder proof.  The returned tubes certify the three affine
columns separately.  For arbitrary affine amplitudes their interval errors
must be scaled by the absolute amplitudes and then added.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_centrifugal_conormal_remainder import (
    TM,
    Matrix2,
    ValidatedConormalRemainder,
    ValidatedConormalRemainderCell,
    Vector2,
    _coefficient_model,
    _formal_branches,
    _matrix_two_inverse,
    _polynomial_model,
    _rational_function_interval,
    validate_centrifugal_conormal_remainder,
)
from .validated_centrifugal_origin_transfer import formal_affine_endpoint_transfer
from .validated_interval import RationalInterval
from .validated_skyrmion_quintic_family import (
    ValidatedSkyrmionQuinticFamily,
    ValidatedSkyrmionQuinticFamilyCell,
)


IntervalVector2 = tuple[RationalInterval, RationalInterval]
IntervalVector4 = tuple[
    RationalInterval,
    RationalInterval,
    RationalInterval,
    RationalInterval,
]
IntervalMatrix2 = tuple[
    tuple[RationalInterval, RationalInterval],
    tuple[RationalInterval, RationalInterval],
]


def _endpoint(model: TM) -> RationalInterval:
    """Evaluate a quadratic Taylor model with its remainder at the endpoint."""
    time = model.horizon
    return (
        model.constant
        + model.linear.scale(time)
        + model.quadratic.scale(time**2)
        + model.remainder.scale(time**3)
    )


def _endpoint_matrix(matrix: Matrix2) -> IntervalMatrix2:
    return tuple(tuple(_endpoint(entry) for entry in row) for row in matrix)  # type: ignore[return-value]


def _endpoint_vector(vector: Vector2) -> IntervalVector2:
    return _endpoint(vector[0]), _endpoint(vector[1])


def _interval_matrix_vector(
    matrix: IntervalMatrix2,
    vector: IntervalVector2,
) -> IntervalVector2:
    return tuple(
        sum(
            (matrix[row][column] * vector[column] for column in range(2)),
            RationalInterval.point(0),
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _branch_center_state(
    branch: dict[str, object],
    slopes: RationalInterval,
    principal: Matrix2,
    mixed: Matrix2,
    derivative_source: Vector2,
) -> tuple[IntervalVector4, IntervalVector2, IntervalVector2]:
    """Return endpoint ``X`` center and the formal ``a,d`` endpoint values."""
    names = ("u0", "v0", "v1", "u1", "v2")
    values = tuple(branch[name] for name in names)
    if not all(hasattr(value, "numerator") for value in values):
        raise TypeError("formal branch coefficients must be rational functions")
    u0, v0, v1, u1, v2 = (
        _rational_function_interval(value, slopes) for value in values
    )
    horizon = principal[0][0].horizon
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
        sum(
            (principal[row][column] * derivatives[column] for column in range(2)),
            zero,
        )
        + sum((mixed[column][row] * fields[column] for column in range(2)), zero)
        - derivative_source[row].scale(sigma)
        for row in range(2)
    )
    z_center = tuple(
        _polynomial_model((item.constant, item.linear, item.quadratic), horizon)
        for item in z_full
    )
    state = (
        _endpoint(fields[0]),
        _endpoint(fields[1]),
        _endpoint(z_center[0]),
        _endpoint(z_center[1]),
    )
    return state, _endpoint_vector(fields), _endpoint_vector(derivatives)


def _expand_center(
    center: RationalInterval,
    error: Fraction,
) -> RationalInterval:
    return center + RationalInterval(-error, error)


def _physical_tube(
    state_center: IntervalVector4,
    state_errors: tuple[Fraction, Fraction, Fraction, Fraction],
    principal: Matrix2,
    mixed: Matrix2,
    derivative_source: Vector2,
    sigma: int,
    cutoff: Fraction,
) -> tuple[IntervalVector2, IntervalVector2, IntervalVector4]:
    state = tuple(
        _expand_center(center, error)
        for center, error in zip(state_center, state_errors, strict=True)
    )
    a = state[0], state[1]
    z = state[2], state[3]
    principal_inverse = _endpoint_matrix(_matrix_two_inverse(principal))
    mixed_endpoint = _endpoint_matrix(mixed)
    source_endpoint = _endpoint_vector(derivative_source)
    derivative_numerator = tuple(
        z[row]
        - sum(
            (mixed_endpoint[column][row] * a[column] for column in range(2)),
            RationalInterval.point(0),
        )
        + source_endpoint[row].scale(sigma)
        for row in range(2)
    )
    derivative = _interval_matrix_vector(principal_inverse, derivative_numerator)
    field = a[0].scale(cutoff), a[1].scale(cutoff)
    return field, derivative, state  # type: ignore[return-value]


@dataclass(frozen=True)
class ValidatedPhysicalOriginBranchTube:
    name: str
    sigma: int
    conormal_state_center: IntervalVector4
    conormal_state_error_bounds: tuple[Fraction, Fraction, Fraction, Fraction]
    conormal_state_tube: IntervalVector4
    formal_field_center: IntervalVector2
    formal_derivative_center: IntervalVector2
    field: IntervalVector2
    derivative: IntervalVector2


@dataclass(frozen=True)
class ValidatedPhysicalOriginTransferCell:
    shooting_slopes: RationalInterval
    branches: tuple[
        ValidatedPhysicalOriginBranchTube,
        ValidatedPhysicalOriginBranchTube,
        ValidatedPhysicalOriginBranchTube,
    ]


@dataclass(frozen=True)
class ValidatedPhysicalOriginTransfer:
    shooting_slopes: RationalInterval
    cutoff: Fraction
    cells: tuple[ValidatedPhysicalOriginTransferCell, ...]
    branch_order: tuple[str, str, str]
    affine_combination_rule: str
    is_finite_cell_enclosure: bool


def _validate_matching_certificates(
    profile: ValidatedSkyrmionQuinticFamily,
    remainder: ValidatedConormalRemainder,
) -> None:
    if profile.shooting_slopes != remainder.shooting_slopes:
        raise ValueError("profile and conormal shooting-slope boxes must agree")
    if profile.cutoff != remainder.cutoff:
        raise ValueError("profile and conormal cutoffs must agree")
    if len(profile.cells) != len(remainder.cells):
        raise ValueError("profile and conormal cell counts must agree")
    if any(
        profile_cell.shooting_slopes != remainder_cell.shooting_slopes
        for profile_cell, remainder_cell in zip(
            profile.cells, remainder.cells, strict=True
        )
    ):
        raise ValueError("profile and conormal slope cells must agree")


def _validate_cell(
    profile: ValidatedSkyrmionQuinticFamily,
    profile_cell: ValidatedSkyrmionQuinticFamilyCell,
    remainder_cell: ValidatedConormalRemainderCell,
    *,
    kernel_terms: int,
) -> ValidatedPhysicalOriginTransferCell:
    _, _, principal, mixed, derivative_source = _coefficient_model(
        profile, profile_cell, kernel_terms=kernel_terms
    )
    formal = formal_affine_endpoint_transfer(
        profile_cell.shooting_slopes, cutoff=profile.cutoff
    )
    formal_fields = (
        *formal.homogeneous_field_columns,
        formal.forced_field,
    )
    formal_derivatives = (
        *formal.homogeneous_derivative_columns,
        formal.forced_derivative,
    )
    branch_tubes = []
    for branch, errors, formal_field, formal_derivative_endpoint in zip(
        _formal_branches(),
        remainder_cell.branch_endpoint_state_error_bounds,
        formal_fields,
        formal_derivatives,
        strict=True,
    ):
        center, _, _ = _branch_center_state(
            branch,
            profile_cell.shooting_slopes,
            principal,
            mixed,
            derivative_source,
        )
        sigma = int(branch["sigma"])
        field, derivative, state = _physical_tube(
            center,
            errors,
            principal,
            mixed,
            derivative_source,
            sigma,
            profile.cutoff,
        )
        # Both computations enclose the same degree-two formal endpoint but
        # arrange the slope dependency differently.  Retaining their hull
        # makes that equivalence directly auditable without weakening rigor.
        field = tuple(
            value.hull(formal_value)
            for value, formal_value in zip(field, formal_field, strict=True)
        )
        derivative = tuple(
            value.hull(formal_value)
            for value, formal_value in zip(
                derivative, formal_derivative_endpoint, strict=True
            )
        )
        branch_tubes.append(
            ValidatedPhysicalOriginBranchTube(
                name=str(branch["name"]),
                sigma=sigma,
                conormal_state_center=center,
                conormal_state_error_bounds=errors,
                conormal_state_tube=state,
                formal_field_center=formal_field,
                formal_derivative_center=formal_derivative_endpoint,
                field=field,  # type: ignore[arg-type]
                derivative=derivative,  # type: ignore[arg-type]
            )
        )
    return ValidatedPhysicalOriginTransferCell(
        shooting_slopes=profile_cell.shooting_slopes,
        branches=tuple(branch_tubes),  # type: ignore[arg-type]
    )


def validate_centrifugal_physical_origin_transfer(
    profile_family: ValidatedSkyrmionQuinticFamily,
    conormal_remainder: ValidatedConormalRemainder | None = None,
    *,
    kernel_terms: int = 5,
) -> ValidatedPhysicalOriginTransfer:
    """Certify physical endpoint tubes for all three affine columns.

    The tubes are columnwise.  If the homogeneous amplitudes are ``alpha``
    and ``beta`` and the forcing amplitude is ``sigma``, combine centers
    linearly and combine the three tube radii with coefficients
    ``|alpha|``, ``|beta|``, and ``|sigma|``.
    """
    if not isinstance(profile_family, ValidatedSkyrmionQuinticFamily):
        raise TypeError("profile_family must be a ValidatedSkyrmionQuinticFamily")
    if kernel_terms < 3:
        raise ValueError("kernel_terms must be at least three")
    remainder = conormal_remainder
    if remainder is None:
        remainder = validate_centrifugal_conormal_remainder(
            profile_family, kernel_terms=kernel_terms
        )
    if not isinstance(remainder, ValidatedConormalRemainder):
        raise TypeError("conormal_remainder must be a ValidatedConormalRemainder")
    _validate_matching_certificates(profile_family, remainder)
    cells = tuple(
        _validate_cell(
            profile_family,
            profile_cell,
            remainder_cell,
            kernel_terms=kernel_terms,
        )
        for profile_cell, remainder_cell in zip(
            profile_family.cells, remainder.cells, strict=True
        )
    )
    return ValidatedPhysicalOriginTransfer(
        shooting_slopes=profile_family.shooting_slopes,
        cutoff=profile_family.cutoff,
        cells=cells,
        branch_order=remainder.branch_order,
        affine_combination_rule=(
            "combine column centers linearly; scale each column-tube error by "
            "the absolute value of its affine amplitude before summing"
        ),
        is_finite_cell_enclosure=True,
    )
