"""Exact interval checker for the explicit centrifugal Liouville witness.

The checker consumes authenticated profile jet boxes and evaluates the regular
conormal potential associated with

``K=sym(M)-P/(2x)``.

It deliberately does not construct profile boxes itself.  Physical provenance
is supplied by the AU.1 Newton tube; synthetic or unlinked boxes prove only a
conditional coefficient statement.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TypeVar

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
)
from .validated_interval import (
    RationalInterval,
    cos_center_lipschitz_interval,
    sin_center_lipschitz_interval,
    sqrt_fraction_interval,
)
from .validated_skyrmion_bvp import SkyrmionJetBox


Scalar = TypeVar("Scalar")
Matrix2 = tuple[tuple[Scalar, Scalar], tuple[Scalar, Scalar]]


def _interval(value: RationalInterval | int | Fraction) -> RationalInterval:
    return value if isinstance(value, RationalInterval) else RationalInterval.point(value)


def _outward_round_interval(
    value: RationalInterval,
    denominator: int,
) -> RationalInterval:
    if isinstance(denominator, bool) or not isinstance(denominator, int) or denominator < 1:
        raise ValueError("rounding denominator must be a positive integer")
    lower_numerator = value.lower.numerator * denominator // value.lower.denominator
    upper_numerator = -(
        (-value.upper.numerator * denominator) // value.upper.denominator
    )
    return RationalInterval(
        Fraction(lower_numerator, denominator),
        Fraction(upper_numerator, denominator),
    )


@dataclass(frozen=True)
class _IntervalJet:
    value: RationalInterval
    derivative: RationalInterval

    @classmethod
    def constant(
        cls,
        value: RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return cls(_interval(value), RationalInterval.point(0))

    def _coerce(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return other if isinstance(other, _IntervalJet) else self.constant(other)

    def __add__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        right = self._coerce(other)
        return _IntervalJet(
            self.value + right.value,
            self.derivative + right.derivative,
        )

    __radd__ = __add__

    def __neg__(self) -> _IntervalJet:
        return _IntervalJet(-self.value, -self.derivative)

    def __sub__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return self + (-self._coerce(other))

    def __rsub__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return self._coerce(other) - self

    def __mul__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        right = self._coerce(other)
        return _IntervalJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        right = self._coerce(other)
        return _IntervalJet(
            self.value / right.value,
            (
                self.derivative * right.value
                - self.value * right.derivative
            )
            / right.value.power(2),
        )

    def __rtruediv__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return self._coerce(other) / self


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


def _matrix_scale(matrix: Matrix2, scalar: int | Fraction | RationalInterval) -> Matrix2:
    return tuple(
        tuple(matrix[row][column] * scalar for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _transpose(matrix: Matrix2) -> Matrix2:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _symmetric_part(matrix: Matrix2) -> Matrix2:
    return _matrix_scale(_matrix_add(matrix, _transpose(matrix)), Fraction(1, 2))


def _matrix_mul(left: Matrix2, right: Matrix2) -> Matrix2:
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(2)),
                RationalInterval.point(0),
            )
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_inverse(matrix: Matrix2) -> Matrix2:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant.contains_zero():
        raise ValueError("principal determinant enclosure contains zero")
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def _value_matrix(matrix: Matrix2) -> Matrix2:
    return tuple(
        tuple(matrix[row][column].value for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _derivative_matrix(matrix: Matrix2) -> Matrix2:
    return tuple(
        tuple(matrix[row][column].derivative for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


@dataclass(frozen=True)
class ValidatedCentrifugalLiouvilleCell:
    source_cell_index: int
    radius: RationalInterval
    principal_bar: Matrix2
    shifted_potential: Matrix2
    principal_first_minor: RationalInterval
    principal_determinant: RationalInterval
    potential_first_minor: RationalInterval
    potential_determinant: RationalInterval
    principal_positive: bool
    shifted_potential_positive: bool


@dataclass(frozen=True)
class ValidatedCentrifugalLiouvilleCoercivity:
    cells: tuple[ValidatedCentrifugalLiouvilleCell, ...]
    target_lower_bound: Fraction
    principal_positive_on_every_cell: bool
    shifted_potential_positive_on_every_cell: bool
    coefficient_coercivity_verified: bool
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedCentrifugalWallTrace:
    wall_profile_derivative: RationalInterval
    wall_robin_multiplier: RationalInterval
    wall_trace_margin: RationalInterval
    wall_trace_positive: bool
    conclusion_scope: str


def centrifugal_liouville_cell(
    jet: SkyrmionJetBox,
    *,
    source_cell_index: int,
    target_lower_bound: Fraction = Fraction(1, 20),
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 24,
    rounding_denominator: int | None = 10**18,
) -> ValidatedCentrifugalLiouvilleCell:
    """Validate the two principal minors on one positive-radius jet box."""
    if not isinstance(jet, SkyrmionJetBox):
        raise TypeError("jet must be a SkyrmionJetBox")
    if jet.radius.lower <= 0:
        raise ValueError("Liouville cells must lie at positive radius")
    if target_lower_bound <= 0:
        raise ValueError("target_lower_bound must be positive")
    if rounding_denominator is not None and (
        isinstance(rounding_denominator, bool)
        or not isinstance(rounding_denominator, int)
        or rounding_denominator < 1
    ):
        raise ValueError("rounding_denominator must be a positive integer or None")

    def rounded(value: RationalInterval) -> RationalInterval:
        return (
            value
            if rounding_denominator is None
            else _outward_round_interval(value, rounding_denominator)
        )

    radius = rounded(jet.radius)
    profile = rounded(jet.profile)
    profile_derivative = rounded(jet.derivative)
    profile_second_derivative = rounded(jet.second_derivative)
    time_value = radius.power(2)
    time = _IntervalJet(time_value, RationalInterval.point(1))
    metric = _IntervalJet(
        RationalInterval.point(1) - time_value.scale(curvature),
        RationalInterval.point(-curvature),
    )
    if metric.value.lower <= 0:
        raise ValueError("cell must lie strictly inside the static-patch horizon")
    sine = sin_center_lipschitz_interval(
        profile,
        terms=trigonometric_terms,
    )
    cosine = cos_center_lipschitz_interval(
        profile,
        terms=trigonometric_terms,
    )
    sine = rounded(sine)
    cosine = rounded(cosine)
    two_radius = radius.scale(2)
    rho = _IntervalJet(
        -profile_derivative,
        -profile_second_derivative / two_radius,
    )
    sine_over_radius = _IntervalJet(
        sine / radius,
        (radius * cosine * profile_derivative - sine)
        / radius.power(3).scale(2),
    )
    cosine_deficit = _IntervalJet(
        -cosine,
        sine * profile_derivative / two_radius,
    )
    blocks = regular_conormal_blocks_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_deficit,
        pion_mass_squared=_IntervalJet.constant(pion_mass_squared),
    )
    def rounded_matrix(matrix: Matrix2) -> Matrix2:
        return tuple(
            tuple(rounded(matrix[row][column]) for column in range(2))
            for row in range(2)
        )  # type: ignore[return-value]

    coordinate = rounded_matrix(_value_matrix(blocks["coordinate"]))
    mixed = rounded_matrix(_value_matrix(blocks["mixed"]))
    mixed_derivative = rounded_matrix(_derivative_matrix(blocks["mixed"]))
    principal = _symmetric_part(
        rounded_matrix(_value_matrix(blocks["principal"]))
    )
    principal_derivative = _symmetric_part(
        rounded_matrix(_derivative_matrix(blocks["principal"]))
    )
    symmetric_mixed = _symmetric_part(mixed)
    symmetric_mixed_derivative = _symmetric_part(mixed_derivative)
    antisymmetric_mixed = _matrix_scale(
        _matrix_sub(mixed, _transpose(mixed)),
        Fraction(1, 2),
    )
    potential = _matrix_add(
        _matrix_add(
            _matrix_sub(
                _matrix_add(
                    _matrix_sub(coordinate, symmetric_mixed),
                    _matrix_scale(principal, Fraction(1, 4)),
                ),
                _matrix_scale(
                    symmetric_mixed_derivative,
                    time_value.scale(2),
                ),
            ),
            _matrix_scale(principal_derivative, time_value),
        ),
        _matrix_mul(
            _matrix_mul(antisymmetric_mixed, _matrix_inverse(principal)),
            antisymmetric_mixed,
        ),
    )
    potential = rounded_matrix(_symmetric_part(potential))
    shifted = tuple(
        tuple(
            potential[row][column]
            - (target_lower_bound if row == column else 0)
            for column in range(2)
        )
        for row in range(2)
    )
    principal_determinant = (
        principal[0][0] * principal[1][1]
        - principal[0][1] * principal[1][0]
    )
    potential_determinant = (
        shifted[0][0] * shifted[1][1]
        - shifted[0][1] * shifted[1][0]
    )
    principal_positive = (
        principal[0][0].lower > 0 and principal_determinant.lower > 0
    )
    potential_positive = (
        shifted[0][0].lower > 0 and potential_determinant.lower > 0
    )
    return ValidatedCentrifugalLiouvilleCell(
        source_cell_index=source_cell_index,
        radius=jet.radius,
        principal_bar=principal,
        shifted_potential=shifted,
        principal_first_minor=principal[0][0],
        principal_determinant=principal_determinant,
        potential_first_minor=shifted[0][0],
        potential_determinant=potential_determinant,
        principal_positive=principal_positive,
        shifted_potential_positive=potential_positive,
    )


def validate_centrifugal_liouville_coercivity(
    jets: tuple[SkyrmionJetBox, ...],
    *,
    target_lower_bound: Fraction = Fraction(1, 20),
    trigonometric_terms: int = 24,
    rounding_denominator: int | None = 10**18,
) -> ValidatedCentrifugalLiouvilleCoercivity:
    """Check a contiguous family of authenticated positive-radius jets."""
    if not jets:
        raise ValueError("at least one profile jet is required")
    for left, right in zip(jets, jets[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("profile jet cells must be exactly contiguous")
    cells = tuple(
        centrifugal_liouville_cell(
            jet,
            source_cell_index=index,
            target_lower_bound=target_lower_bound,
            trigonometric_terms=trigonometric_terms,
            rounding_denominator=rounding_denominator,
        )
        for index, jet in enumerate(jets)
    )
    principal = all(cell.principal_positive for cell in cells)
    potential = all(cell.shifted_potential_positive for cell in cells)
    verified = principal and potential
    return ValidatedCentrifugalLiouvilleCoercivity(
        cells=cells,
        target_lower_bound=target_lower_bound,
        principal_positive_on_every_cell=principal,
        shifted_potential_positive_on_every_cell=potential,
        coefficient_coercivity_verified=verified,
        conclusion_scope=(
            "coefficient part of the explicit Liouville coercivity certificate "
            "verified on the supplied profile jets; physical coercivity also "
            "requires authenticated jet provenance, the wall trace, and closure "
            "of the smooth Friedrichs core"
            if verified
            else "exact Liouville coefficient diagnostic only; at least one "
            "strict principal-minor inequality does not close"
        ),
    )


def validate_centrifugal_wall_trace(
    wall_profile_derivative: RationalInterval,
    *,
    wall_radius: Fraction = Fraction(4),
    curvature: Fraction = Fraction(1, 400),
    membrane_tension: Fraction = Fraction(1931779647, 10**12),
    square_root_steps: int = 160,
) -> ValidatedCentrifugalWallTrace:
    """Certify the allowed `g(a)=0` wall remainder for the explicit witness."""
    if not isinstance(wall_profile_derivative, RationalInterval):
        raise TypeError("wall_profile_derivative must be a RationalInterval")
    if wall_profile_derivative.contains_zero():
        raise ValueError("wall profile derivative must exclude zero")
    lapse = Fraction(1) - curvature * wall_radius**2
    if lapse <= 0:
        raise ValueError("wall must lie strictly inside the horizon")
    root = sqrt_fraction_interval(lapse, bisection_steps=square_root_steps)
    centered_derivative = (
        root.scale(Fraction(-2, wall_radius**2))
        - RationalInterval.point(3 * curvature) / root
        - RationalInterval.point(curvature**2 * wall_radius**2)
        / (root * root * root)
    )
    angular = RationalInterval.point(Fraction(6, wall_radius**2)) / root
    shape = centered_derivative + angular
    lapse_derivative = -2 * curvature * wall_radius
    beta = (
        RationalInterval.point(Fraction(-2, wall_radius))
        - RationalInterval.point(Fraction(lapse_derivative, 2 * lapse))
        - shape.scale(Fraction(4 * membrane_tension, lapse))
        / wall_profile_derivative.power(2)
    )
    principal_ff = Fraction(wall_radius**2 * lapse, 45)
    margin = (-beta - Fraction(1, 2 * wall_radius)).scale(principal_ff)
    return ValidatedCentrifugalWallTrace(
        wall_profile_derivative=wall_profile_derivative,
        wall_robin_multiplier=beta,
        wall_trace_margin=margin,
        wall_trace_positive=margin.lower > 0,
        conclusion_scope=(
            "exact allowed-wall Liouville trace remainder is positive, "
            "conditional on the supplied wall-slope enclosure and the derived "
            "pure-tension Robin coefficient"
            if margin.lower > 0
            else "wall trace diagnostic only; positivity is not verified"
        ),
    )
