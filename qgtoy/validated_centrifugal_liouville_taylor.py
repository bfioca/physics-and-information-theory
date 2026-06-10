"""Cancellation-preserving Taylor models for the Liouville coercivity minor."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
)
from .validated_centrifugal_global_form import (
    _outward_round_interval,
)
from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    cos_fraction_interval,
    sin_fraction_interval,
)
from .validated_skyrmion_bvp import (
    SkyrmionPolynomialCell,
    _affine_restrict_polynomial,
)


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _monomial_range(power: int) -> RationalInterval:
    return (
        RationalInterval(Fraction(0), Fraction(1))
        if power % 2 == 0
        else RationalInterval(Fraction(-1), Fraction(1))
    )


@dataclass(frozen=True)
class _CenteredTaylorModel:
    coefficients: tuple[RationalInterval, ...]
    remainder: RationalInterval
    degree_limit: int = 24
    rounding_denominator: int = 10**16

    def __post_init__(self) -> None:
        if not self.coefficients:
            raise ValueError("Taylor model must have at least one coefficient")
        if self.degree_limit < 1:
            raise ValueError("degree_limit must be positive")
        if self.rounding_denominator < 1:
            raise ValueError("rounding_denominator must be positive")
        coefficients = tuple(
            _outward_round_interval(value, self.rounding_denominator)
            for value in self.coefficients[: self.degree_limit + 1]
        )
        while len(coefficients) > 1 and coefficients[-1] == RationalInterval.point(0):
            coefficients = coefficients[:-1]
        object.__setattr__(self, "coefficients", coefficients)
        object.__setattr__(
            self,
            "remainder",
            _outward_round_interval(self.remainder, self.rounding_denominator),
        )

    @classmethod
    def constant(
        cls,
        value: RationalInterval | int | Fraction,
        *,
        degree_limit: int = 24,
        rounding_denominator: int = 10**16,
    ) -> _CenteredTaylorModel:
        interval = (
            value if isinstance(value, RationalInterval) else RationalInterval.point(value)
        )
        return cls(
            (interval,),
            RationalInterval.point(0),
            degree_limit,
            rounding_denominator,
        )

    @classmethod
    def from_polynomial(
        cls,
        polynomial: RationalPolynomial,
        *,
        error_radius: Fraction = Fraction(0),
        degree_limit: int = 24,
        rounding_denominator: int = 10**16,
    ) -> _CenteredTaylorModel:
        if error_radius < 0:
            raise ValueError("Taylor-model error radius must be nonnegative")
        return cls(
            tuple(RationalInterval.point(value) for value in polynomial.coefficients),
            RationalInterval(-error_radius, error_radius),
            degree_limit,
            rounding_denominator,
        )

    def _coerce(
        self,
        other: _CenteredTaylorModel | RationalInterval | int | Fraction,
    ) -> _CenteredTaylorModel:
        if isinstance(other, _CenteredTaylorModel):
            if (
                other.degree_limit != self.degree_limit
                or other.rounding_denominator != self.rounding_denominator
            ):
                raise ValueError("Taylor-model configurations differ")
            return other
        return self.constant(
            other,
            degree_limit=self.degree_limit,
            rounding_denominator=self.rounding_denominator,
        )

    def polynomial_range(self) -> RationalInterval:
        result = self.coefficients[0]
        for power, coefficient in enumerate(self.coefficients[1:], start=1):
            result = result + coefficient * _monomial_range(power)
        return result

    def range(self) -> RationalInterval:
        return self.polynomial_range() + self.remainder

    def symmetric_integral(self) -> RationalInterval:
        """Enclose the integral over the normalized coordinate ``[-1, 1]``.

        Polynomial coefficients are constant intervals, so odd monomials
        integrate to zero exactly. The pointwise Taylor remainder contributes
        twice its interval enclosure.
        """
        total = RationalInterval.point(0)
        for power, coefficient in enumerate(self.coefficients):
            if power % 2 == 0:
                total += coefficient.scale(Fraction(2, power + 1))
        return total + self.remainder.scale(2)

    def with_added_remainder(self, radius: Fraction) -> _CenteredTaylorModel:
        if radius < 0:
            raise ValueError("remainder radius must be nonnegative")
        return _CenteredTaylorModel(
            self.coefficients,
            self.remainder + RationalInterval(-radius, radius),
            self.degree_limit,
            self.rounding_denominator,
        )

    def __add__(
        self,
        other: _CenteredTaylorModel | RationalInterval | int | Fraction,
    ) -> _CenteredTaylorModel:
        right = self._coerce(other)
        size = max(len(self.coefficients), len(right.coefficients))
        zero = RationalInterval.point(0)
        coefficients = tuple(
            (self.coefficients[index] if index < len(self.coefficients) else zero)
            + (right.coefficients[index] if index < len(right.coefficients) else zero)
            for index in range(size)
        )
        return _CenteredTaylorModel(
            coefficients,
            self.remainder + right.remainder,
            self.degree_limit,
            self.rounding_denominator,
        )

    __radd__ = __add__

    def __neg__(self) -> _CenteredTaylorModel:
        return _CenteredTaylorModel(
            tuple(-value for value in self.coefficients),
            -self.remainder,
            self.degree_limit,
            self.rounding_denominator,
        )

    def __sub__(
        self,
        other: _CenteredTaylorModel | RationalInterval | int | Fraction,
    ) -> _CenteredTaylorModel:
        return self + (-self._coerce(other))

    def __rsub__(
        self,
        other: _CenteredTaylorModel | RationalInterval | int | Fraction,
    ) -> _CenteredTaylorModel:
        return self._coerce(other) - self

    def __mul__(
        self,
        other: _CenteredTaylorModel | RationalInterval | int | Fraction,
    ) -> _CenteredTaylorModel:
        right = self._coerce(other)
        zero = RationalInterval.point(0)
        coefficients = [zero] * (self.degree_limit + 1)
        discarded = zero
        for left_power, left_value in enumerate(self.coefficients):
            for right_power, right_value in enumerate(right.coefficients):
                power = left_power + right_power
                product = left_value * right_value
                if power <= self.degree_limit:
                    coefficients[power] = coefficients[power] + product
                else:
                    discarded = discarded + product * _monomial_range(power)
        while len(coefficients) > 1 and coefficients[-1] == zero:
            coefficients.pop()
        remainder = (
            discarded
            + self.polynomial_range() * right.remainder
            + right.polynomial_range() * self.remainder
            + self.remainder * right.remainder
        )
        return _CenteredTaylorModel(
            tuple(coefficients),
            remainder,
            self.degree_limit,
            self.rounding_denominator,
        )

    __rmul__ = __mul__

    def power(self, exponent: int) -> _CenteredTaylorModel:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Taylor-model power must be a nonnegative integer")
        result = self.constant(
            1,
            degree_limit=self.degree_limit,
            rounding_denominator=self.rounding_denominator,
        )
        base = self
        power = exponent
        while power:
            if power % 2:
                result = result * base
            power //= 2
            if power:
                base = base * base
        return result

    def reciprocal(self, *, terms: int = 10) -> _CenteredTaylorModel:
        enclosure = self.range()
        if enclosure.contains_zero():
            raise ZeroDivisionError("Taylor-model reciprocal contains zero")
        center = enclosure.midpoint
        delta = (self - center) * Fraction(1, center)
        ratio = _absolute_upper(delta.range())
        if ratio >= 1:
            raise ValueError("Taylor-model reciprocal Neumann ratio is not below one")
        result = self.constant(
            1,
            degree_limit=self.degree_limit,
            rounding_denominator=self.rounding_denominator,
        )
        power = result
        for index in range(1, terms + 1):
            power = power * delta
            result = result + power * ((-1) ** index)
        result = result * Fraction(1, center)
        tail = ratio ** (terms + 1) / ((1 - ratio) * abs(center))
        return result.with_added_remainder(tail)

    def __truediv__(
        self,
        other: _CenteredTaylorModel | RationalInterval | int | Fraction,
    ) -> _CenteredTaylorModel:
        return self * self._coerce(other).reciprocal()

    def __rtruediv__(
        self,
        other: _CenteredTaylorModel | RationalInterval | int | Fraction,
    ) -> _CenteredTaylorModel:
        return self._coerce(other) / self

    def sin_cos(self, *, terms: int = 8) -> tuple[_CenteredTaylorModel, _CenteredTaylorModel]:
        center = self.coefficients[0].midpoint
        delta = self - center
        delta_range = _absolute_upper(delta.range())
        delta_squared = delta * delta
        even_power = self.constant(
            1,
            degree_limit=self.degree_limit,
            rounding_denominator=self.rounding_denominator,
        )
        sine_delta = self.constant(
            0,
            degree_limit=self.degree_limit,
            rounding_denominator=self.rounding_denominator,
        )
        cosine_delta = even_power
        for index in range(terms):
            sine_delta = sine_delta + (
                delta * even_power * Fraction((-1) ** index, factorial(2 * index + 1))
            )
            if index > 0:
                cosine_delta = cosine_delta + (
                    even_power * Fraction((-1) ** index, factorial(2 * index))
                )
            even_power = even_power * delta_squared
        sine_delta = sine_delta.with_added_remainder(
            delta_range ** (2 * terms + 1) / factorial(2 * terms + 1)
        )
        cosine_delta = cosine_delta.with_added_remainder(
            delta_range ** (2 * terms) / factorial(2 * terms)
        )
        sine_center = sin_fraction_interval(center, terms=32)
        cosine_center = cos_fraction_interval(center, terms=32)
        sine = sine_delta * cosine_center + cosine_delta * sine_center
        cosine = cosine_delta * cosine_center - sine_delta * sine_center
        return sine, cosine


@dataclass(frozen=True)
class _ModelJet:
    value: _CenteredTaylorModel
    derivative: _CenteredTaylorModel

    def _coerce(self, other: _ModelJet | int | Fraction) -> _ModelJet:
        if isinstance(other, _ModelJet):
            return other
        constant = self.value._coerce(other)
        return _ModelJet(constant, self.value._coerce(0))

    def __add__(self, other: _ModelJet | int | Fraction) -> _ModelJet:
        right = self._coerce(other)
        return _ModelJet(
            self.value + right.value,
            self.derivative + right.derivative,
        )

    __radd__ = __add__

    def __neg__(self) -> _ModelJet:
        return _ModelJet(-self.value, -self.derivative)

    def __sub__(self, other: _ModelJet | int | Fraction) -> _ModelJet:
        return self + (-self._coerce(other))

    def __rsub__(self, other: _ModelJet | int | Fraction) -> _ModelJet:
        return self._coerce(other) - self

    def __mul__(self, other: _ModelJet | int | Fraction) -> _ModelJet:
        right = self._coerce(other)
        return _ModelJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: _ModelJet | int | Fraction) -> _ModelJet:
        right = self._coerce(other)
        return _ModelJet(
            self.value / right.value,
            (
                self.derivative * right.value - self.value * right.derivative
            )
            / (right.value * right.value),
        )

    def __rtruediv__(self, other: _ModelJet | int | Fraction) -> _ModelJet:
        return self._coerce(other) / self


def _matrix_add(left, right):
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(2))
        for row in range(2)
    )


def _matrix_sub(left, right):
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(2))
        for row in range(2)
    )


def _matrix_scale(matrix, scalar):
    return tuple(
        tuple(matrix[row][column] * scalar for column in range(2))
        for row in range(2)
    )


def _transpose(matrix):
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _symmetric_part(matrix):
    return _matrix_scale(_matrix_add(matrix, _transpose(matrix)), Fraction(1, 2))


def _matrix_mul(left, right):
    zero = left[0][0] * 0
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(2)),
                zero,
            )
            for column in range(2)
        )
        for row in range(2)
    )


def _matrix_inverse(matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def _value_matrix(matrix):
    return tuple(
        tuple(matrix[row][column].value for column in range(2))
        for row in range(2)
    )


def _derivative_matrix(matrix):
    return tuple(
        tuple(matrix[row][column].derivative for column in range(2))
        for row in range(2)
    )


def _scale_polynomial(polynomial: RationalPolynomial, scalar: Fraction) -> RationalPolynomial:
    return RationalPolynomial(tuple(value * scalar for value in polynomial.coefficients))


@dataclass(frozen=True)
class ValidatedCentrifugalLiouvilleTaylorCell:
    source_cell_index: int
    radius: RationalInterval
    principal_radial: RationalInterval
    principal_tangential: RationalInterval
    scaled_first_minor: RationalInterval
    scaled_second_minor: RationalInterval
    scaled_determinant: RationalInterval
    principal_positive: bool
    shifted_potential_positive: bool
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedCentrifugalLiouvilleTaylorSpline:
    profile_cell_count: int
    validation_cells: tuple[ValidatedCentrifugalLiouvilleTaylorCell, ...]
    target_lower_bound: Fraction
    minimum_principal_radial: Fraction
    minimum_principal_tangential: Fraction
    minimum_scaled_first_minor: Fraction
    minimum_scaled_second_minor: Fraction
    minimum_scaled_determinant: Fraction
    maximum_refinement_depth: int
    maximum_refinement_depth_used: int
    coercivity_verified: bool
    conclusion_scope: str


def centrifugal_liouville_taylor_cell(
    profile_cell: SkyrmionPolynomialCell,
    left: Fraction,
    right: Fraction,
    *,
    source_cell_index: int,
    profile_error_radius: Fraction = Fraction(0),
    derivative_error_radius: Fraction = Fraction(0),
    second_derivative_error_radius: Fraction = Fraction(0),
    target_lower_bound: Fraction = Fraction(1, 20),
    degree_limit: int = 24,
    rounding_denominator: int = 10**16,
    trigonometric_terms: int = 8,
) -> ValidatedCentrifugalLiouvilleTaylorCell:
    """Range one centered spline subcell after assembling both minors."""
    if not isinstance(profile_cell, SkyrmionPolynomialCell):
        raise TypeError("profile_cell must be a SkyrmionPolynomialCell")
    if not (0 <= left < right <= 1):
        raise ValueError("subcell coordinates must satisfy 0<=left<right<=1")
    if min(
        profile_error_radius,
        derivative_error_radius,
        second_derivative_error_radius,
    ) < 0:
        raise ValueError("profile error radii must be nonnegative")
    midpoint = (left + right) / 2
    normalized_half_width = (right - left) / 2
    physical_half_width = profile_cell.radius.width * normalized_half_width
    profile = _affine_restrict_polynomial(
        profile_cell.profile_polynomial,
        midpoint,
        normalized_half_width,
    )
    derivative = _scale_polynomial(profile.derivative(), 1 / physical_half_width)
    second_derivative = _scale_polynomial(
        profile.derivative().derivative(),
        1 / physical_half_width**2,
    )
    radius_center = profile_cell.radius.lower + profile_cell.radius.width * midpoint
    radius = RationalPolynomial((radius_center, physical_half_width))
    model_options = {
        "degree_limit": degree_limit,
        "rounding_denominator": rounding_denominator,
    }
    x = _CenteredTaylorModel.from_polynomial(radius, **model_options)
    field = _CenteredTaylorModel.from_polynomial(
        profile,
        error_radius=profile_error_radius,
        **model_options,
    )
    field_derivative = _CenteredTaylorModel.from_polynomial(
        derivative,
        error_radius=derivative_error_radius,
        **model_options,
    )
    field_second_derivative = _CenteredTaylorModel.from_polynomial(
        second_derivative,
        error_radius=second_derivative_error_radius,
        **model_options,
    )
    sine, cosine = field.sin_cos(terms=trigonometric_terms)
    time_value = x * x
    one = x._coerce(1)
    time = _ModelJet(time_value, one)
    metric = _ModelJet(one - time_value * Fraction(1, 400), x._coerce(Fraction(-1, 400)))
    rho = _ModelJet(-field_derivative, -field_second_derivative / (2 * x))
    sine_over_radius = _ModelJet(
        sine / x,
        (x * cosine * field_derivative - sine) / (2 * x.power(3)),
    )
    cosine_deficit = _ModelJet(
        -cosine,
        sine * field_derivative / (2 * x),
    )
    blocks = regular_conormal_blocks_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_deficit,
        pion_mass_squared=_ModelJet(x._coerce(1), x._coerce(0)),
    )
    coordinate = _value_matrix(blocks["coordinate"])
    mixed = _value_matrix(blocks["mixed"])
    mixed_derivative = _derivative_matrix(blocks["mixed"])
    principal = _symmetric_part(_value_matrix(blocks["principal"]))
    principal_derivative = _symmetric_part(_derivative_matrix(blocks["principal"]))
    symmetric_mixed = _symmetric_part(mixed)
    symmetric_mixed_derivative = _symmetric_part(mixed_derivative)
    antisymmetric_alpha = (mixed[0][1] - mixed[1][0]) * Fraction(1, 2)
    p = principal[0][0]
    r = principal[1][1]
    u = (
        coordinate[0][0]
        - symmetric_mixed[0][0]
        + p * Fraction(1, 4)
        - symmetric_mixed_derivative[0][0] * time_value * 2
        + principal_derivative[0][0] * time_value
        - target_lower_bound
    )
    v = (
        coordinate[1][1]
        - symmetric_mixed[1][1]
        + r * Fraction(1, 4)
        - symmetric_mixed_derivative[1][1] * time_value * 2
        + principal_derivative[1][1] * time_value
        - target_lower_bound
    )
    z = (
        coordinate[0][1]
        - symmetric_mixed[0][1]
        - symmetric_mixed_derivative[0][1] * time_value * 2
    )
    alpha_squared = antisymmetric_alpha * antisymmetric_alpha
    first_minor = r * u - alpha_squared
    second_minor = p * v - alpha_squared
    determinant = first_minor * second_minor - p * r * z * z
    p_range = p.range()
    r_range = r.range()
    first_range = first_minor.range()
    second_range = second_minor.range()
    determinant_range = determinant.range()
    radius_interval = RationalInterval(
        radius_center - physical_half_width,
        radius_center + physical_half_width,
    )
    principal_positive = p_range.lower > 0 and r_range.lower > 0
    potential_positive = first_range.lower > 0 and determinant_range.lower > 0
    return ValidatedCentrifugalLiouvilleTaylorCell(
        source_cell_index=source_cell_index,
        radius=radius_interval,
        principal_radial=p_range,
        principal_tangential=r_range,
        scaled_first_minor=first_range,
        scaled_second_minor=second_range,
        scaled_determinant=determinant_range,
        principal_positive=principal_positive,
        shifted_potential_positive=potential_positive,
        conclusion_scope=(
            "division-free centered Taylor-model Liouville minors are positive "
            "on this subcell"
            if principal_positive and potential_positive
            else "Taylor-model coefficient diagnostic only; a strict scaled "
            "minor inequality did not close"
        ),
    )


def validate_centrifugal_liouville_taylor_spline(
    profile_cells: tuple[SkyrmionPolynomialCell, ...],
    *,
    target_lower_bound: Fraction = Fraction(1, 20),
    maximum_refinement_depth: int = 2,
    degree_limit: int = 8,
    rounding_denominator: int = 10**16,
    trigonometric_terms: int = 5,
) -> ValidatedCentrifugalLiouvilleTaylorSpline:
    """Adaptively certify the division-free minors on an exact spline."""
    if not profile_cells:
        raise ValueError("profile_cells must be nonempty")
    if isinstance(maximum_refinement_depth, bool) or maximum_refinement_depth < 0:
        raise ValueError("maximum_refinement_depth must be nonnegative")
    for index, cell in enumerate(profile_cells):
        if not isinstance(cell, SkyrmionPolynomialCell):
            raise TypeError("profile_cells must contain SkyrmionPolynomialCell values")
        if cell.radius.lower <= 0 or cell.radius.lower >= cell.radius.upper:
            raise ValueError("profile cells must have positive nonempty radii")
        if index and profile_cells[index - 1].radius.upper != cell.radius.lower:
            raise ValueError("profile cells must form a contiguous partition")

    validation_cells: list[ValidatedCentrifugalLiouvilleTaylorCell] = []
    maximum_depth_used = 0

    def validate_subcell(
        source_cell_index: int,
        left: Fraction,
        right: Fraction,
        depth: int,
    ) -> None:
        nonlocal maximum_depth_used
        result = centrifugal_liouville_taylor_cell(
            profile_cells[source_cell_index],
            left,
            right,
            source_cell_index=source_cell_index,
            target_lower_bound=target_lower_bound,
            degree_limit=degree_limit,
            rounding_denominator=rounding_denominator,
            trigonometric_terms=trigonometric_terms,
        )
        maximum_depth_used = max(maximum_depth_used, depth)
        if result.principal_positive and result.shifted_potential_positive:
            validation_cells.append(result)
            return
        if depth >= maximum_refinement_depth:
            raise ValueError(
                "Liouville minor validation failed on profile cell "
                f"{source_cell_index} subcell [{left}, {right}]"
            )
        midpoint = (left + right) / 2
        validate_subcell(source_cell_index, left, midpoint, depth + 1)
        validate_subcell(source_cell_index, midpoint, right, depth + 1)

    for source_cell_index in range(len(profile_cells)):
        validate_subcell(source_cell_index, Fraction(0), Fraction(1), 0)

    cells = tuple(validation_cells)
    return ValidatedCentrifugalLiouvilleTaylorSpline(
        profile_cell_count=len(profile_cells),
        validation_cells=cells,
        target_lower_bound=target_lower_bound,
        minimum_principal_radial=min(cell.principal_radial.lower for cell in cells),
        minimum_principal_tangential=min(
            cell.principal_tangential.lower for cell in cells
        ),
        minimum_scaled_first_minor=min(
            cell.scaled_first_minor.lower for cell in cells
        ),
        minimum_scaled_second_minor=min(
            cell.scaled_second_minor.lower for cell in cells
        ),
        minimum_scaled_determinant=min(
            cell.scaled_determinant.lower for cell in cells
        ),
        maximum_refinement_depth=maximum_refinement_depth,
        maximum_refinement_depth_used=maximum_depth_used,
        coercivity_verified=True,
        conclusion_scope=(
            "the exact supplied positive-radius spline satisfies the completed "
            f"Liouville potential bound W_K >= {target_lower_bound} I"
        ),
    )
