"""Regular-origin Liouville coercivity for the authenticated profile family."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
)
from .validated_interval import RationalInterval
from .validated_centrifugal_global_form import (
    _derivative_matrix,
    _outward_round_interval,
    _value_matrix,
)
from .validated_skyrmion_origin import (
    ValidatedSkyrmionOriginFamily,
    _TaylorModelFamily,
    _cubic_coefficient_interval,
    _entire_even_kernel_family_model,
)


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


@dataclass(frozen=True)
class _RoundedInterval:
    interval: RationalInterval
    denominator: int = 10**16

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "interval",
            _outward_round_interval(self.interval, self.denominator),
        )

    @classmethod
    def point(
        cls,
        value: int | Fraction,
        denominator: int = 10**16,
    ) -> _RoundedInterval:
        return cls(RationalInterval.point(value), denominator)

    @property
    def lower(self) -> Fraction:
        return self.interval.lower

    @property
    def upper(self) -> Fraction:
        return self.interval.upper

    def _coerce(
        self,
        other: _RoundedInterval | RationalInterval | int | Fraction,
    ) -> _RoundedInterval:
        if isinstance(other, _RoundedInterval):
            if other.denominator != self.denominator:
                raise ValueError("rounded-interval denominators differ")
            return other
        interval = (
            other
            if isinstance(other, RationalInterval)
            else RationalInterval.point(other)
        )
        return _RoundedInterval(interval, self.denominator)

    def __add__(
        self,
        other: _RoundedInterval | RationalInterval | int | Fraction,
    ) -> _RoundedInterval:
        right = self._coerce(other)
        return _RoundedInterval(
            self.interval + right.interval,
            self.denominator,
        )

    __radd__ = __add__

    def __neg__(self) -> _RoundedInterval:
        return _RoundedInterval(-self.interval, self.denominator)

    def __sub__(
        self,
        other: _RoundedInterval | RationalInterval | int | Fraction,
    ) -> _RoundedInterval:
        return self + (-self._coerce(other))

    def __rsub__(
        self,
        other: _RoundedInterval | RationalInterval | int | Fraction,
    ) -> _RoundedInterval:
        return self._coerce(other) - self

    def __mul__(
        self,
        other: _RoundedInterval | RationalInterval | int | Fraction,
    ) -> _RoundedInterval:
        right = self._coerce(other)
        return _RoundedInterval(
            self.interval * right.interval,
            self.denominator,
        )

    __rmul__ = __mul__

    def __truediv__(
        self,
        other: _RoundedInterval | RationalInterval | int | Fraction,
    ) -> _RoundedInterval:
        right = self._coerce(other)
        return _RoundedInterval(
            self.interval / right.interval,
            self.denominator,
        )

    def __rtruediv__(
        self,
        other: _RoundedInterval | RationalInterval | int | Fraction,
    ) -> _RoundedInterval:
        return self._coerce(other) / self

    def scale(self, factor: int | Fraction) -> _RoundedInterval:
        return self * factor

    def power(self, exponent: int) -> _RoundedInterval:
        if exponent < 0:
            raise ValueError("rounded-interval power must be nonnegative")
        result = self.point(1, self.denominator)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            power //= 2
            if power:
                base = base * base
        return result


@dataclass(frozen=True)
class _RoundedJet:
    value: _RoundedInterval
    derivative: _RoundedInterval

    def _coerce(self, other: _RoundedJet | int | Fraction) -> _RoundedJet:
        if isinstance(other, _RoundedJet):
            return other
        return _RoundedJet(
            self.value.point(other, self.value.denominator),
            self.value.point(0, self.value.denominator),
        )

    def __add__(self, other: _RoundedJet | int | Fraction) -> _RoundedJet:
        right = self._coerce(other)
        return _RoundedJet(
            self.value + right.value,
            self.derivative + right.derivative,
        )

    __radd__ = __add__

    def __neg__(self) -> _RoundedJet:
        return _RoundedJet(-self.value, -self.derivative)

    def __sub__(self, other: _RoundedJet | int | Fraction) -> _RoundedJet:
        return self + (-self._coerce(other))

    def __rsub__(self, other: _RoundedJet | int | Fraction) -> _RoundedJet:
        return self._coerce(other) - self

    def __mul__(self, other: _RoundedJet | int | Fraction) -> _RoundedJet:
        right = self._coerce(other)
        return _RoundedJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__


@dataclass(frozen=True)
class _DualInterval:
    value: _RoundedInterval
    derivatives: tuple[_RoundedInterval, ...]

    @classmethod
    def constant(
        cls,
        value: RationalInterval | int | Fraction,
        *,
        dimension: int,
        denominator: int,
    ) -> _DualInterval:
        interval = (
            value
            if isinstance(value, RationalInterval)
            else RationalInterval.point(value)
        )
        rounded = _RoundedInterval(interval, denominator)
        zero = _RoundedInterval.point(0, denominator)
        return cls(rounded, (zero,) * dimension)

    @classmethod
    def variable(
        cls,
        value: RationalInterval,
        *,
        index: int,
        dimension: int,
        denominator: int,
    ) -> _DualInterval:
        zero = _RoundedInterval.point(0, denominator)
        one = _RoundedInterval.point(1, denominator)
        derivatives = tuple(one if offset == index else zero for offset in range(dimension))
        return cls(_RoundedInterval(value, denominator), derivatives)

    def _coerce(
        self,
        other: _DualInterval | RationalInterval | int | Fraction,
    ) -> _DualInterval:
        if isinstance(other, _DualInterval):
            return other
        return self.constant(
            other,
            dimension=len(self.derivatives),
            denominator=self.value.denominator,
        )

    def __add__(
        self,
        other: _DualInterval | RationalInterval | int | Fraction,
    ) -> _DualInterval:
        right = self._coerce(other)
        return _DualInterval(
            self.value + right.value,
            tuple(
                left_derivative + right_derivative
                for left_derivative, right_derivative in zip(
                    self.derivatives,
                    right.derivatives,
                    strict=True,
                )
            ),
        )

    __radd__ = __add__

    def __neg__(self) -> _DualInterval:
        return _DualInterval(
            -self.value,
            tuple(-derivative for derivative in self.derivatives),
        )

    def __sub__(
        self,
        other: _DualInterval | RationalInterval | int | Fraction,
    ) -> _DualInterval:
        return self + (-self._coerce(other))

    def __rsub__(
        self,
        other: _DualInterval | RationalInterval | int | Fraction,
    ) -> _DualInterval:
        return self._coerce(other) - self

    def __mul__(
        self,
        other: _DualInterval | RationalInterval | int | Fraction,
    ) -> _DualInterval:
        right = self._coerce(other)
        return _DualInterval(
            self.value * right.value,
            tuple(
                left_derivative * right.value + self.value * right_derivative
                for left_derivative, right_derivative in zip(
                    self.derivatives,
                    right.derivatives,
                    strict=True,
                )
            ),
        )

    __rmul__ = __mul__

    def reciprocal(self) -> _DualInterval:
        reciprocal_value = 1 / self.value
        factor = -(reciprocal_value * reciprocal_value)
        return _DualInterval(
            reciprocal_value,
            tuple(factor * derivative for derivative in self.derivatives),
        )

    def __truediv__(
        self,
        other: _DualInterval | RationalInterval | int | Fraction,
    ) -> _DualInterval:
        return self * self._coerce(other).reciprocal()

    def __rtruediv__(
        self,
        other: _DualInterval | RationalInterval | int | Fraction,
    ) -> _DualInterval:
        return self._coerce(other) / self

    def scale(self, factor: int | Fraction) -> _DualInterval:
        return self * factor

    def power(self, exponent: int) -> _DualInterval:
        if exponent < 0:
            raise ValueError("dual-interval power must be nonnegative")
        result = self._coerce(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            power //= 2
            if power:
                base = base * base
        return result


@dataclass(frozen=True)
class _DualJet:
    value: _DualInterval
    derivative: _DualInterval

    def _coerce(self, other: _DualJet | int | Fraction) -> _DualJet:
        if isinstance(other, _DualJet):
            return other
        constant = self.value._coerce(other)
        return _DualJet(constant, self.value._coerce(0))

    def __add__(self, other: _DualJet | int | Fraction) -> _DualJet:
        right = self._coerce(other)
        return _DualJet(
            self.value + right.value,
            self.derivative + right.derivative,
        )

    __radd__ = __add__

    def __neg__(self) -> _DualJet:
        return _DualJet(-self.value, -self.derivative)

    def __sub__(self, other: _DualJet | int | Fraction) -> _DualJet:
        return self + (-self._coerce(other))

    def __rsub__(self, other: _DualJet | int | Fraction) -> _DualJet:
        return self._coerce(other) - self

    def __mul__(self, other: _DualJet | int | Fraction) -> _DualJet:
        right = self._coerce(other)
        return _DualJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__


def _symmetric_part(matrix):
    return tuple(
        tuple(
            (matrix[row][column] + matrix[column][row]).scale(Fraction(1, 2))
            for column in range(2)
        )
        for row in range(2)
    )


@dataclass(frozen=True)
class _OriginJet:
    value: _TaylorModelFamily
    derivative: _TaylorModelFamily

    def _coerce(self, other: _OriginJet | int | Fraction) -> _OriginJet:
        if isinstance(other, _OriginJet):
            return other
        constant = _TaylorModelFamily.point(other, self.value.horizon)
        return _OriginJet(
            constant,
            _TaylorModelFamily.point(0, self.value.horizon),
        )

    def __add__(self, other: _OriginJet | int | Fraction) -> _OriginJet:
        right = self._coerce(other)
        return _OriginJet(
            self.value + right.value,
            self.derivative + right.derivative,
        )

    __radd__ = __add__

    def __neg__(self) -> _OriginJet:
        return _OriginJet(self.value.scale(-1), self.derivative.scale(-1))

    def __sub__(self, other: _OriginJet | int | Fraction) -> _OriginJet:
        return self + (-self._coerce(other))

    def __rsub__(self, other: _OriginJet | int | Fraction) -> _OriginJet:
        return self._coerce(other) - self

    def __mul__(self, other: _OriginJet | int | Fraction) -> _OriginJet:
        right = self._coerce(other)
        return _OriginJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__


def _series_model(
    argument: _TaylorModelFamily,
    coefficients: tuple[Fraction, ...],
    *,
    tail_remainder_radius: Fraction,
) -> _TaylorModelFamily:
    result = _TaylorModelFamily.point(0, argument.horizon)
    power = _TaylorModelFamily.point(1, argument.horizon)
    for coefficient in coefficients:
        result = result + power.scale(coefficient)
        power = power * argument
    return _TaylorModelFamily(
        result.constant,
        result.linear,
        result.remainder
        + RationalInterval(-tail_remainder_radius, tail_remainder_radius),
        result.horizon,
    )


def _cosine_kernel_model(
    argument: _TaylorModelFamily,
    *,
    argument_rate_upper: Fraction,
    terms: int,
) -> _TaylorModelFamily:
    coefficients = tuple(
        Fraction((-1) ** index, factorial(2 * index))
        for index in range(terms)
    )
    maximum = argument_rate_upper * argument.horizon
    ratio = maximum / ((2 * terms + 1) * (2 * terms + 2))
    if ratio >= 1:
        raise ValueError("cosine-kernel tail ratio is not below one")
    tail = (
        argument_rate_upper**terms
        * argument.horizon ** (terms - 2)
        / factorial(2 * terms)
        / (1 - ratio)
    )
    return _series_model(
        argument,
        coefficients,
        tail_remainder_radius=tail,
    )


def _one_minus_sinc_over_time_model(
    argument: _TaylorModelFamily,
    profile_over_radius: _TaylorModelFamily,
    *,
    scale_squared: int,
    argument_rate_upper: Fraction,
    terms: int,
) -> _TaylorModelFamily:
    coefficients = tuple(
        Fraction(
            (-1) ** index * scale_squared ** (index + 1),
            factorial(2 * index + 3),
        )
        for index in range(terms)
    )
    maximum = argument_rate_upper * argument.horizon
    ratio = (
        Fraction(scale_squared)
        * maximum
        / ((2 * terms + 4) * (2 * terms + 5))
    )
    if ratio >= 1:
        raise ValueError("sinc-quotient tail ratio is not below one")
    tail = (
        Fraction(scale_squared ** (terms + 1), factorial(2 * terms + 3))
        * argument_rate_upper ** (terms + 1)
        * argument.horizon ** (terms - 2)
        / (1 - ratio)
    )
    return profile_over_radius.power(2) * _series_model(
        argument,
        coefficients,
        tail_remainder_radius=tail / argument_rate_upper,
    )


def _cosine_minus_sinc_over_time_model(
    argument: _TaylorModelFamily,
    profile_over_radius: _TaylorModelFamily,
    *,
    argument_rate_upper: Fraction,
    terms: int,
) -> _TaylorModelFamily:
    coefficients = tuple(
        Fraction(
            (-1) ** (index + 1) * 2 * (index + 1),
            factorial(2 * index + 3),
        )
        for index in range(terms)
    )
    maximum = argument_rate_upper * argument.horizon
    ratio = (
        Fraction(terms + 2, terms + 1)
        * maximum
        / ((2 * terms + 4) * (2 * terms + 5))
    )
    if ratio >= 1:
        raise ValueError("cosine-minus-sinc tail ratio is not below one")
    first_omitted = Fraction(
        2 * (terms + 1), factorial(2 * terms + 3)
    )
    tail = (
        first_omitted
        * argument_rate_upper ** (terms + 1)
        * argument.horizon ** (terms - 2)
        / (1 - ratio)
    )
    return profile_over_radius.power(2) * _series_model(
        argument,
        coefficients,
        tail_remainder_radius=tail / argument_rate_upper,
    )


@dataclass(frozen=True)
class ValidatedCentrifugalOriginLiouville:
    cutoff: Fraction
    target_lower_bound: Fraction
    principal_radial: RationalInterval
    principal_tangential: RationalInterval
    scaled_first_minor: RationalInterval
    scaled_second_minor: RationalInterval
    scaled_determinant: RationalInterval
    principal_positive: bool
    shifted_potential_positive: bool
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedCentrifugalOriginLiouvilleCell:
    time: RationalInterval
    shooting_slopes: RationalInterval
    principal_radial: RationalInterval
    principal_tangential: RationalInterval
    scaled_first_minor: RationalInterval
    scaled_second_minor: RationalInterval
    scaled_determinant: RationalInterval
    shifted_potential_positive: bool


@dataclass(frozen=True)
class ValidatedCentrifugalOriginLiouvillePartition:
    cutoff: Fraction
    target_lower_bound: Fraction
    time_subdivisions: int
    slope_subdivisions: int
    cells: tuple[ValidatedCentrifugalOriginLiouvilleCell, ...]
    minimum_principal_radial: Fraction
    minimum_principal_tangential: Fraction
    minimum_scaled_first_minor: Fraction
    minimum_scaled_second_minor: Fraction
    minimum_scaled_determinant: Fraction
    coefficient_coercivity_verified: bool
    conclusion_scope: str


def validate_centrifugal_origin_liouville(
    origin: ValidatedSkyrmionOriginFamily,
    *,
    target_lower_bound: Fraction = Fraction(1, 100),
    kernel_terms: int = 12,
) -> ValidatedCentrifugalOriginLiouville:
    """Certify the completed potential without differentiating a remainder."""
    if not isinstance(origin, ValidatedSkyrmionOriginFamily):
        raise TypeError("origin must be a ValidatedSkyrmionOriginFamily")
    if target_lower_bound <= 0:
        raise ValueError("target_lower_bound must be positive")
    if kernel_terms < 3:
        raise ValueError("kernel_terms must be at least three")

    horizon = origin.cutoff**2
    zero = RationalInterval.point(0)
    remainder = origin.remainder_radius
    u = _TaylorModelFamily(
        origin.shooting_slopes,
        -origin.cubic_coefficient,
        RationalInterval(-remainder / 5, remainder / 5),
        horizon,
    )
    p = _TaylorModelFamily(
        origin.shooting_slopes,
        origin.cubic_coefficient.scale(-3),
        RationalInterval(-remainder, remainder),
        horizon,
    )
    delta = _TaylorModelFamily(
        origin.cubic_coefficient.scale(-2),
        RationalInterval(-6 * remainder / 5, 6 * remainder / 5),
        zero,
        horizon,
    )
    time = _TaylorModelFamily(zero, RationalInterval.point(1), zero, horizon)
    one = _TaylorModelFamily.point(1, horizon)
    argument_rate = _absolute_upper(u.range()) ** 2
    argument = time * u.power(2)
    sinc = _entire_even_kernel_family_model(
        argument,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    cosine = _cosine_kernel_model(
        argument,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    one_minus_sinc_over_time = _one_minus_sinc_over_time_model(
        argument,
        u,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    cosine_minus_sinc_over_time = _cosine_minus_sinc_over_time_model(
        argument,
        u,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )

    sine_over_radius = u * sinc
    metric = one - time.scale(origin.curvature)
    denominator = one + sine_over_radius.power(2).scale(8)
    profile_time_derivative = delta.scale(Fraction(1, 2))
    profile_kernel_offset = (u * one_minus_sinc_over_time).scale(-1)
    cosine_kernel_offset = (
        cosine_minus_sinc_over_time - one_minus_sinc_over_time
    )
    sine_over_radius_time_derivative = (
        cosine * delta + u * cosine_minus_sinc_over_time
    ).scale(Fraction(1, 2))
    p_time_numerator = (
        denominator
        * (
            cosine * profile_kernel_offset
            + u * cosine_kernel_offset
            - profile_time_derivative.scale(2)
        )
        + (sine_over_radius * cosine).scale(4)
        * (
            (profile_time_derivative.scale(2) - profile_kernel_offset)
            * (p + sine_over_radius)
        )
        - (sine_over_radius * cosine * p.power(2)).scale(
            4 * origin.curvature
        )
        + (denominator * p).scale(2 * origin.curvature)
        - (metric * sine_over_radius * sine_over_radius_time_derivative * p).scale(16)
        - sine_over_radius.scale(origin.pion_mass_squared * Fraction(1, 2))
    )
    p_time_derivative = p_time_numerator / (metric * denominator)
    cosine_time_derivative = (sine_over_radius * p).scale(Fraction(-1, 2))

    blocks = regular_conormal_blocks_from_kernels(
        t=_OriginJet(time, one),
        metric_factor=_OriginJet(metric, _TaylorModelFamily.point(-origin.curvature, horizon)),
        profile_deficit_radial_derivative=_OriginJet(p, p_time_derivative),
        sine_over_radius=_OriginJet(
            sine_over_radius,
            sine_over_radius_time_derivative,
        ),
        cosine_of_profile_deficit=_OriginJet(cosine, cosine_time_derivative),
        pion_mass_squared=_OriginJet(
            _TaylorModelFamily.point(origin.pion_mass_squared, horizon),
            _TaylorModelFamily.point(0, horizon),
        ),
    )
    coordinate = tuple(
        tuple(blocks["coordinate"][row][column].value for column in range(2))
        for row in range(2)
    )
    mixed = tuple(
        tuple(blocks["mixed"][row][column].value for column in range(2))
        for row in range(2)
    )
    mixed_derivative = tuple(
        tuple(blocks["mixed"][row][column].derivative for column in range(2))
        for row in range(2)
    )
    principal = _symmetric_part(
        tuple(
            tuple(blocks["principal"][row][column].value for column in range(2))
            for row in range(2)
        )
    )
    principal_derivative = _symmetric_part(
        tuple(
            tuple(
                blocks["principal"][row][column].derivative
                for column in range(2)
            )
            for row in range(2)
        )
    )
    symmetric_mixed = _symmetric_part(mixed)
    symmetric_mixed_derivative = _symmetric_part(mixed_derivative)
    alpha = (mixed[0][1] - mixed[1][0]).scale(Fraction(1, 2))
    radial = principal[0][0]
    tangential = principal[1][1]
    shifted_radial = (
        coordinate[0][0]
        - symmetric_mixed[0][0]
        + radial.scale(Fraction(1, 4))
        - time * symmetric_mixed_derivative[0][0].scale(2)
        + time * principal_derivative[0][0]
        - target_lower_bound
    )
    shifted_tangential = (
        coordinate[1][1]
        - symmetric_mixed[1][1]
        + tangential.scale(Fraction(1, 4))
        - time * symmetric_mixed_derivative[1][1].scale(2)
        + time * principal_derivative[1][1]
        - target_lower_bound
    )
    coupling = (
        coordinate[0][1]
        - symmetric_mixed[0][1]
        - time * symmetric_mixed_derivative[0][1].scale(2)
    )
    alpha_squared = alpha * alpha
    first_minor = tangential * shifted_radial - alpha_squared
    second_minor = radial * shifted_tangential - alpha_squared
    determinant = (
        first_minor * second_minor
        - radial * tangential * coupling.power(2)
    )
    radial_range = radial.range()
    tangential_range = tangential.range()
    first_range = first_minor.range()
    second_range = second_minor.range()
    determinant_range = determinant.range()
    principal_positive = radial_range.lower > 0 and tangential_range.lower > 0
    shifted_positive = first_range.lower > 0 and determinant_range.lower > 0
    return ValidatedCentrifugalOriginLiouville(
        cutoff=origin.cutoff,
        target_lower_bound=target_lower_bound,
        principal_radial=radial_range,
        principal_tangential=tangential_range,
        scaled_first_minor=first_range,
        scaled_second_minor=second_range,
        scaled_determinant=determinant_range,
        principal_positive=principal_positive,
        shifted_potential_positive=shifted_positive,
        conclusion_scope=(
            "the completed Liouville potential is positive on the full "
            "authenticated regular origin family"
            if principal_positive and shifted_positive
            else "regular-origin coefficient diagnostic only; the interval "
            "minor enclosure did not close"
        ),
    )


def _entire_interval_series(
    argument: RationalInterval,
    coefficients: tuple[Fraction, ...],
    *,
    first_omitted_absolute: Fraction,
    tail_ratio: Fraction,
) -> RationalInterval:
    if argument.lower < 0:
        raise ValueError("entire-kernel argument must be nonnegative")
    if tail_ratio >= 1:
        raise ValueError("entire-kernel tail ratio is not below one")
    total = RationalInterval.point(0)
    power = RationalInterval.point(1)
    for coefficient in coefficients:
        total = total + power.scale(coefficient)
        power = power * argument
    tail = first_omitted_absolute * argument.upper ** len(coefficients) / (
        1 - tail_ratio
    )
    return total + RationalInterval(-tail, tail)


def _regular_entire_intervals(
    argument: RationalInterval,
    *,
    terms: int,
) -> tuple[
    RationalInterval,
    RationalInterval,
    RationalInterval,
    RationalInterval,
    RationalInterval,
]:
    maximum = argument.upper
    sinc = _entire_interval_series(
        argument,
        tuple(
            Fraction((-1) ** index, factorial(2 * index + 1))
            for index in range(terms)
        ),
        first_omitted_absolute=Fraction(1, factorial(2 * terms + 1)),
        tail_ratio=maximum / ((2 * terms + 2) * (2 * terms + 3)),
    )
    cosine = _entire_interval_series(
        argument,
        tuple(
            Fraction((-1) ** index, factorial(2 * index))
            for index in range(terms)
        ),
        first_omitted_absolute=Fraction(1, factorial(2 * terms)),
        tail_ratio=maximum / ((2 * terms + 1) * (2 * terms + 2)),
    )
    phi = _entire_interval_series(
        argument,
        tuple(
            Fraction((-1) ** (index + 1), factorial(2 * index + 3))
            for index in range(terms)
        ),
        first_omitted_absolute=Fraction(1, factorial(2 * terms + 3)),
        tail_ratio=maximum / ((2 * terms + 4) * (2 * terms + 5)),
    )
    chi = _entire_interval_series(
        argument,
        tuple(
            Fraction((-1) ** (index + 1), factorial(2 * index + 2))
            for index in range(terms)
        ),
        first_omitted_absolute=Fraction(1, factorial(2 * terms + 2)),
        tail_ratio=maximum / ((2 * terms + 3) * (2 * terms + 4)),
    )
    psi = _entire_interval_series(
        argument,
        tuple(
            Fraction(
                (-1) ** (index + 1) * 2 * (index + 1),
                factorial(2 * index + 3),
            )
            for index in range(terms)
        ),
        first_omitted_absolute=Fraction(
            2 * (terms + 1), factorial(2 * terms + 3)
        ),
        tail_ratio=(
            Fraction(terms + 2, terms + 1)
            * maximum
            / ((2 * terms + 4) * (2 * terms + 5))
        ),
    )
    return sinc, cosine, phi, chi, psi


def _series_interval_with_derivative(
    argument: RationalInterval,
    coefficient,
    *,
    terms: int,
    derivative_order: int,
) -> RationalInterval:
    total = RationalInterval.point(0)
    for index in range(derivative_order, terms):
        falling = 1
        for offset in range(derivative_order):
            falling *= index - offset
        total = total + argument.power(index - derivative_order).scale(
            coefficient(index) * falling
        )
    omitted_falling = 1
    next_falling = 1
    for offset in range(derivative_order):
        omitted_falling *= terms - offset
        next_falling *= terms + 1 - offset
    first = (
        abs(coefficient(terms))
        * omitted_falling
        * argument.upper ** (terms - derivative_order)
    )
    coefficient_ratio = abs(coefficient(terms + 1) / coefficient(terms))
    ratio = (
        coefficient_ratio
        * Fraction(next_falling, omitted_falling)
        * argument.upper
    )
    if ratio >= 1:
        raise ValueError("entire dual-kernel tail ratio is not below one")
    tail = first / (1 - ratio)
    return total + RationalInterval(-tail, tail)


def _dual_entire_kernel(
    argument: _DualInterval,
    coefficient,
    *,
    terms: int,
) -> _DualInterval:
    value = _RoundedInterval(
        _series_interval_with_derivative(
            argument.value.interval,
            coefficient,
            terms=terms,
            derivative_order=0,
        ),
        argument.value.denominator,
    )
    derivative = _RoundedInterval(
        _series_interval_with_derivative(
            argument.value.interval,
            coefficient,
            terms=terms,
            derivative_order=1,
        ),
        argument.value.denominator,
    )
    return _DualInterval(
        value,
        tuple(derivative * item for item in argument.derivatives),
    )


def _origin_liouville_dual_targets(
    origin: ValidatedSkyrmionOriginFamily,
    time: _DualInterval,
    shooting_slope: _DualInterval,
    momentum_remainder: _DualInterval,
    profile_remainder: _DualInterval,
    *,
    target_lower_bound: Fraction,
    kernel_terms: int,
) -> tuple[
    _DualInterval,
    _DualInterval,
    _DualInterval,
    _DualInterval,
    _DualInterval,
]:
    slope_squared = shooting_slope.power(2)
    cubic = (
        shooting_slope
        * (
            origin.pion_mass_squared
            - 4 * origin.curvature
            + slope_squared.scale(Fraction(4, 3) - 24 * origin.curvature)
            + slope_squared.power(2).scale(Fraction(8, 3))
        )
        / (10 * (1 + slope_squared.scale(8)))
    )
    time_squared = time.power(2)
    profile_over_radius = (
        shooting_slope - cubic * time + profile_remainder * time_squared
    )
    momentum = (
        shooting_slope
        - cubic * time.scale(3)
        + momentum_remainder * time_squared
    )
    profile_time_derivative = (
        -cubic
        + time
        * (momentum_remainder - profile_remainder).scale(Fraction(1, 2))
    )
    argument = time * profile_over_radius.power(2)
    sinc = _dual_entire_kernel(
        argument,
        lambda index: Fraction((-1) ** index, factorial(2 * index + 1)),
        terms=kernel_terms,
    )
    cosine = _dual_entire_kernel(
        argument,
        lambda index: Fraction((-1) ** index, factorial(2 * index)),
        terms=kernel_terms,
    )
    phi = _dual_entire_kernel(
        argument,
        lambda index: Fraction(
            (-1) ** (index + 1),
            factorial(2 * index + 3),
        ),
        terms=kernel_terms,
    )
    chi = _dual_entire_kernel(
        argument,
        lambda index: Fraction(
            (-1) ** (index + 1),
            factorial(2 * index + 2),
        ),
        terms=kernel_terms,
    )
    psi = _dual_entire_kernel(
        argument,
        lambda index: Fraction(
            (-1) ** (index + 1) * 2 * (index + 1),
            factorial(2 * index + 3),
        ),
        terms=kernel_terms,
    )
    sine_over_radius = profile_over_radius * sinc
    profile_kernel_offset = profile_over_radius.power(3) * phi
    cosine_kernel_offset = profile_over_radius.power(2) * chi
    sine_time_derivative = (
        cosine * profile_time_derivative
        + profile_over_radius.power(3) * psi.scale(Fraction(1, 2))
    )
    metric = 1 - time.scale(origin.curvature)
    denominator = 1 + sine_over_radius.power(2).scale(8)
    momentum_time_numerator = (
        denominator
        * (
            cosine * profile_kernel_offset
            + profile_over_radius * cosine_kernel_offset
            - profile_time_derivative.scale(2)
        )
        + (sine_over_radius * cosine).scale(4)
        * (
            (profile_time_derivative.scale(2) - profile_kernel_offset)
            * (momentum + sine_over_radius)
        )
        - (sine_over_radius * cosine * momentum.power(2)).scale(
            4 * origin.curvature
        )
        + (denominator * momentum).scale(2 * origin.curvature)
        - (metric * sine_over_radius * sine_time_derivative * momentum).scale(16)
        - sine_over_radius.scale(origin.pion_mass_squared * Fraction(1, 2))
    )
    momentum_time_derivative = momentum_time_numerator / (metric * denominator)
    blocks = regular_conormal_blocks_from_kernels(
        t=_DualJet(time, time._coerce(1)),
        metric_factor=_DualJet(metric, time._coerce(-origin.curvature)),
        profile_deficit_radial_derivative=_DualJet(
            momentum,
            momentum_time_derivative,
        ),
        sine_over_radius=_DualJet(sine_over_radius, sine_time_derivative),
        cosine_of_profile_deficit=_DualJet(
            cosine,
            (sine_over_radius * momentum).scale(Fraction(-1, 2)),
        ),
        pion_mass_squared=_DualJet(
            time._coerce(origin.pion_mass_squared),
            time._coerce(0),
        ),
    )
    coordinate = _value_matrix(blocks["coordinate"])
    mixed = _value_matrix(blocks["mixed"])
    mixed_derivative = _derivative_matrix(blocks["mixed"])
    principal = _symmetric_part(_value_matrix(blocks["principal"]))
    principal_derivative = _symmetric_part(
        _derivative_matrix(blocks["principal"])
    )
    symmetric_mixed = _symmetric_part(mixed)
    symmetric_mixed_derivative = _symmetric_part(mixed_derivative)
    alpha = (mixed[0][1] - mixed[1][0]).scale(Fraction(1, 2))
    radial = principal[0][0]
    tangential = principal[1][1]
    shifted_radial = (
        coordinate[0][0]
        - symmetric_mixed[0][0]
        + radial.scale(Fraction(1, 4))
        - time * symmetric_mixed_derivative[0][0].scale(2)
        + time * principal_derivative[0][0]
        - target_lower_bound
    )
    shifted_tangential = (
        coordinate[1][1]
        - symmetric_mixed[1][1]
        + tangential.scale(Fraction(1, 4))
        - time * symmetric_mixed_derivative[1][1].scale(2)
        + time * principal_derivative[1][1]
        - target_lower_bound
    )
    coupling = (
        coordinate[0][1]
        - symmetric_mixed[0][1]
        - time * symmetric_mixed_derivative[0][1].scale(2)
    )
    alpha_squared = alpha.power(2)
    first_minor = tangential * shifted_radial - alpha_squared
    second_minor = radial * shifted_tangential - alpha_squared
    determinant = (
        first_minor * second_minor
        - radial * tangential * coupling.power(2)
    )
    return radial, tangential, first_minor, second_minor, determinant


def centrifugal_origin_liouville_interval_cell(
    origin: ValidatedSkyrmionOriginFamily,
    time: RationalInterval,
    shooting_slopes: RationalInterval,
    *,
    target_lower_bound: Fraction = Fraction(1, 100),
    kernel_terms: int = 12,
    rounding_denominator: int = 10**16,
) -> ValidatedCentrifugalOriginLiouvilleCell:
    """Evaluate one regular `(t,b,r_p,r_u)` interval cell."""
    if time.lower < 0 or time.upper > origin.cutoff**2:
        raise ValueError("time cell lies outside the authenticated origin family")
    if not shooting_slopes.is_subset_of(origin.shooting_slopes):
        raise ValueError("shooting-slope cell lies outside the origin family")
    remainder = origin.remainder_radius
    cubic = _cubic_coefficient_interval(
        shooting_slopes,
        origin.pion_mass_squared,
        origin.curvature,
    )
    profile_remainder = RationalInterval(-remainder / 5, remainder / 5)
    momentum_remainder = RationalInterval(-remainder, remainder)
    time_squared = time.power(2)
    profile_over_radius = (
        shooting_slopes - cubic * time + profile_remainder * time_squared
    )
    momentum = (
        shooting_slopes
        - cubic * time.scale(3)
        + momentum_remainder * time_squared
    )
    profile_time_derivative = (
        -cubic
        + time
        * (momentum_remainder - profile_remainder).scale(Fraction(1, 2))
    )
    argument = time * profile_over_radius.power(2)
    sinc, cosine, phi, chi, psi = _regular_entire_intervals(
        argument,
        terms=kernel_terms,
    )
    rounded_time = _RoundedInterval(time, rounding_denominator)
    rounded_profile = _RoundedInterval(profile_over_radius, rounding_denominator)
    rounded_momentum = _RoundedInterval(momentum, rounding_denominator)
    rounded_profile_time = _RoundedInterval(
        profile_time_derivative,
        rounding_denominator,
    )
    rounded_sinc = _RoundedInterval(sinc, rounding_denominator)
    rounded_cosine = _RoundedInterval(cosine, rounding_denominator)
    rounded_phi = _RoundedInterval(phi, rounding_denominator)
    rounded_chi = _RoundedInterval(chi, rounding_denominator)
    rounded_psi = _RoundedInterval(psi, rounding_denominator)
    sine_over_radius = rounded_profile * rounded_sinc
    profile_kernel_offset = rounded_profile.power(3) * rounded_phi
    cosine_kernel_offset = rounded_profile.power(2) * rounded_chi
    sine_time_derivative = (
        rounded_cosine * rounded_profile_time
        + rounded_profile.power(3) * rounded_psi.scale(Fraction(1, 2))
    )
    one = _RoundedInterval.point(1, rounding_denominator)
    metric = one - rounded_time.scale(origin.curvature)
    denominator = one + sine_over_radius.power(2).scale(8)
    momentum_time_numerator = (
        denominator
        * (
            rounded_cosine * profile_kernel_offset
            + rounded_profile * cosine_kernel_offset
            - rounded_profile_time.scale(2)
        )
        + (sine_over_radius * rounded_cosine).scale(4)
        * (
            (rounded_profile_time.scale(2) - profile_kernel_offset)
            * (rounded_momentum + sine_over_radius)
        )
        - (sine_over_radius * rounded_cosine * rounded_momentum.power(2)).scale(
            4 * origin.curvature
        )
        + (denominator * rounded_momentum).scale(2 * origin.curvature)
        - (
            metric
            * sine_over_radius
            * sine_time_derivative
            * rounded_momentum
        ).scale(16)
        - sine_over_radius.scale(origin.pion_mass_squared * Fraction(1, 2))
    )
    momentum_time_derivative = momentum_time_numerator / (metric * denominator)
    blocks = regular_conormal_blocks_from_kernels(
        t=_RoundedJet(rounded_time, one),
        metric_factor=_RoundedJet(
            metric,
            _RoundedInterval.point(-origin.curvature, rounding_denominator),
        ),
        profile_deficit_radial_derivative=_RoundedJet(
            rounded_momentum,
            momentum_time_derivative,
        ),
        sine_over_radius=_RoundedJet(
            sine_over_radius,
            sine_time_derivative,
        ),
        cosine_of_profile_deficit=_RoundedJet(
            rounded_cosine,
            (sine_over_radius * rounded_momentum).scale(Fraction(-1, 2)),
        ),
        pion_mass_squared=_RoundedJet(
            _RoundedInterval.point(
                origin.pion_mass_squared,
                rounding_denominator,
            ),
            _RoundedInterval.point(0, rounding_denominator),
        ),
    )
    coordinate = _value_matrix(blocks["coordinate"])
    mixed = _value_matrix(blocks["mixed"])
    mixed_derivative = _derivative_matrix(blocks["mixed"])
    principal = _symmetric_part(_value_matrix(blocks["principal"]))
    principal_derivative = _symmetric_part(
        _derivative_matrix(blocks["principal"])
    )
    symmetric_mixed = _symmetric_part(mixed)
    symmetric_mixed_derivative = _symmetric_part(mixed_derivative)
    alpha = (mixed[0][1] - mixed[1][0]).scale(Fraction(1, 2))
    radial = principal[0][0]
    tangential = principal[1][1]
    shifted_radial = (
        coordinate[0][0]
        - symmetric_mixed[0][0]
        + radial.scale(Fraction(1, 4))
        - rounded_time * symmetric_mixed_derivative[0][0].scale(2)
        + rounded_time * principal_derivative[0][0]
        - target_lower_bound
    )
    shifted_tangential = (
        coordinate[1][1]
        - symmetric_mixed[1][1]
        + tangential.scale(Fraction(1, 4))
        - rounded_time * symmetric_mixed_derivative[1][1].scale(2)
        + rounded_time * principal_derivative[1][1]
        - target_lower_bound
    )
    coupling = (
        coordinate[0][1]
        - symmetric_mixed[0][1]
        - rounded_time * symmetric_mixed_derivative[0][1].scale(2)
    )
    alpha_squared = alpha.power(2)
    first_minor = tangential * shifted_radial - alpha_squared
    second_minor = radial * shifted_tangential - alpha_squared
    determinant = (
        first_minor * second_minor
        - radial * tangential * coupling.power(2)
    )
    positive = (
        radial.lower > 0
        and tangential.lower > 0
        and first_minor.lower > 0
        and determinant.lower > 0
    )
    return ValidatedCentrifugalOriginLiouvilleCell(
        time=time,
        shooting_slopes=shooting_slopes,
        principal_radial=radial.interval,
        principal_tangential=tangential.interval,
        scaled_first_minor=first_minor.interval,
        scaled_second_minor=second_minor.interval,
        scaled_determinant=determinant.interval,
        shifted_potential_positive=positive,
    )


def centrifugal_origin_liouville_mean_value_cell(
    origin: ValidatedSkyrmionOriginFamily,
    time: RationalInterval,
    shooting_slopes: RationalInterval,
    *,
    target_lower_bound: Fraction = Fraction(1, 100),
    kernel_terms: int = 12,
    rounding_denominator: int = 10**16,
) -> ValidatedCentrifugalOriginLiouvilleCell:
    """Range assembled minors by a four-variable interval mean-value form."""
    if time.lower < 0 or time.upper > origin.cutoff**2:
        raise ValueError("time cell lies outside the authenticated origin family")
    if not shooting_slopes.is_subset_of(origin.shooting_slopes):
        raise ValueError("shooting-slope cell lies outside the origin family")
    dimension = 4

    def variable(value: RationalInterval, index: int) -> _DualInterval:
        return _DualInterval.variable(
            value,
            index=index,
            dimension=dimension,
            denominator=rounding_denominator,
        )

    box_targets = _origin_liouville_dual_targets(
        origin,
        variable(time, 0),
        variable(shooting_slopes, 1),
        variable(
            RationalInterval(-origin.remainder_radius, origin.remainder_radius),
            2,
        ),
        variable(
            RationalInterval(
                -origin.remainder_radius / 5,
                origin.remainder_radius / 5,
            ),
            3,
        ),
        target_lower_bound=target_lower_bound,
        kernel_terms=kernel_terms,
    )

    def constant(value: Fraction) -> _DualInterval:
        return _DualInterval.constant(
            value,
            dimension=dimension,
            denominator=rounding_denominator,
        )

    center_targets = _origin_liouville_dual_targets(
        origin,
        constant(time.midpoint),
        constant(shooting_slopes.midpoint),
        constant(Fraction(0)),
        constant(Fraction(0)),
        target_lower_bound=target_lower_bound,
        kernel_terms=kernel_terms,
    )
    radii = (
        time.width / 2,
        shooting_slopes.width / 2,
        origin.remainder_radius,
        origin.remainder_radius / 5,
    )

    def mean_value(
        center: _DualInterval,
        box: _DualInterval,
    ) -> RationalInterval:
        error = sum(
            _absolute_upper(derivative.interval) * radius
            for derivative, radius in zip(box.derivatives, radii, strict=True)
        )
        return center.value.interval + RationalInterval(-error, error)

    ranges = tuple(
        mean_value(center, box)
        for center, box in zip(center_targets, box_targets, strict=True)
    )
    radial, tangential, first_minor, second_minor, determinant = ranges
    positive = (
        radial.lower > 0
        and tangential.lower > 0
        and first_minor.lower > 0
        and determinant.lower > 0
    )
    return ValidatedCentrifugalOriginLiouvilleCell(
        time=time,
        shooting_slopes=shooting_slopes,
        principal_radial=radial,
        principal_tangential=tangential,
        scaled_first_minor=first_minor,
        scaled_second_minor=second_minor,
        scaled_determinant=determinant,
        shifted_potential_positive=positive,
    )


def validate_centrifugal_origin_liouville_partition(
    origin: ValidatedSkyrmionOriginFamily,
    *,
    target_lower_bound: Fraction = Fraction(1, 100),
    time_subdivisions: int = 64,
    slope_subdivisions: int = 16,
    kernel_terms: int = 12,
) -> ValidatedCentrifugalOriginLiouvillePartition:
    """Certify the origin family by direct regular interval subdivision."""
    if min(time_subdivisions, slope_subdivisions) < 1:
        raise ValueError("subdivision counts must be positive")
    horizon = origin.cutoff**2
    slope_width = origin.shooting_slopes.width
    cells = tuple(
        centrifugal_origin_liouville_mean_value_cell(
            origin,
            RationalInterval(
                horizon * time_index / time_subdivisions,
                horizon * (time_index + 1) / time_subdivisions,
            ),
            RationalInterval(
                origin.shooting_slopes.lower
                + slope_width * slope_index / slope_subdivisions,
                origin.shooting_slopes.lower
                + slope_width * (slope_index + 1) / slope_subdivisions,
            ),
            target_lower_bound=target_lower_bound,
            kernel_terms=kernel_terms,
        )
        for slope_index in range(slope_subdivisions)
        for time_index in range(time_subdivisions)
    )
    verified = all(cell.shifted_potential_positive for cell in cells)
    return ValidatedCentrifugalOriginLiouvillePartition(
        cutoff=origin.cutoff,
        target_lower_bound=target_lower_bound,
        time_subdivisions=time_subdivisions,
        slope_subdivisions=slope_subdivisions,
        cells=cells,
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
        coefficient_coercivity_verified=verified,
        conclusion_scope=(
            "the authenticated regular origin family satisfies the completed "
            f"Liouville potential bound W_K >= {target_lower_bound} I"
            if verified
            else "regular-origin interval diagnostic only; at least one "
            "subcell failed the division-free minor test"
        ),
    )
