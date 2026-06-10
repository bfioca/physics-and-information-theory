"""Exact rational validation of the regular Skyrmion origin branch.

The apparent singularity at ``x=0`` is removed by writing

``g=pi-F=x u(t)``, ``t=x^2``, and ``p(t)=g'(x)``.

The resulting Volterra map is analytic in ``t`` and uses the entire even
functions ``sin(sqrt(w))/sqrt(w)`` and ``sin(2 sqrt(w))/(2 sqrt(w))``.  This
module validates a cubic-centred weighted ball with exact Fraction endpoints;
it never calls a floating-point transcendental function.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import factorial

from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    pi_machin_interval,
)


def _fraction(name: str, value: int | Fraction, *, positive: bool = False) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    result = Fraction(value)
    if positive and result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _abs_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _format_scaled_decimal(value: int, places: int) -> str:
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    scale = 10**places
    integer, fractional = divmod(magnitude, scale)
    return f"{sign}{integer}.{fractional:0{places}d}"


def _outward_decimal_interval(
    value: RationalInterval,
    *,
    places: int = 18,
) -> dict[str, str]:
    """Return a compact rational decimal enclosure without printing huge integers."""
    scale = 10**places
    lower_scaled = value.lower.numerator * scale // value.lower.denominator
    upper_scaled = -(
        (-value.upper.numerator * scale) // value.upper.denominator
    )
    return {
        "lower": _format_scaled_decimal(lower_scaled, places),
        "upper": _format_scaled_decimal(upper_scaled, places),
        "representation": f"outward_decimal_enclosure_{places}_places",
    }


def _as_interval(
    value: RationalInterval | int | Fraction,
) -> RationalInterval:
    if isinstance(value, RationalInterval):
        return value
    return RationalInterval.point(value)


def _polynomial_add(
    left: RationalPolynomial,
    right: RationalPolynomial,
) -> RationalPolynomial:
    length = max(len(left.coefficients), len(right.coefficients))
    coefficients = [Fraction(0)] * length
    for index, value in enumerate(left.coefficients):
        coefficients[index] += value
    for index, value in enumerate(right.coefficients):
        coefficients[index] += value
    return RationalPolynomial(tuple(coefficients))


def _polynomial_multiply(
    left: RationalPolynomial,
    right: RationalPolynomial,
) -> RationalPolynomial:
    coefficients = [Fraction(0)] * (
        len(left.coefficients) + len(right.coefficients) - 1
    )
    for left_index, left_value in enumerate(left.coefficients):
        for right_index, right_value in enumerate(right.coefficients):
            coefficients[left_index + right_index] += left_value * right_value
    return RationalPolynomial(tuple(coefficients))


@dataclass(frozen=True)
class _RationalFunction:
    """Small exact formal rational function used for coefficient identities."""

    numerator: RationalPolynomial
    denominator: RationalPolynomial

    def __post_init__(self) -> None:
        if self.denominator.coefficients == (Fraction(0),):
            raise ZeroDivisionError("formal rational-function denominator is zero")

    @classmethod
    def constant(cls, value: int | Fraction) -> _RationalFunction:
        return cls(
            RationalPolynomial((Fraction(value),)),
            RationalPolynomial((Fraction(1),)),
        )

    @classmethod
    def variable(cls) -> _RationalFunction:
        return cls(
            RationalPolynomial((Fraction(0), Fraction(1))),
            RationalPolynomial((Fraction(1),)),
        )

    def __add__(
        self,
        other: _RationalFunction | int | Fraction,
    ) -> _RationalFunction:
        value = other if isinstance(other, _RationalFunction) else self.constant(other)
        return _RationalFunction(
            _polynomial_add(
                _polynomial_multiply(self.numerator, value.denominator),
                _polynomial_multiply(value.numerator, self.denominator),
            ),
            _polynomial_multiply(self.denominator, value.denominator),
        )

    def __radd__(self, other: int | Fraction) -> _RationalFunction:
        return self + other

    def __sub__(
        self,
        other: _RationalFunction | int | Fraction,
    ) -> _RationalFunction:
        value = other if isinstance(other, _RationalFunction) else self.constant(other)
        return self + value.scale(-1)

    def __rsub__(self, other: int | Fraction) -> _RationalFunction:
        return self.constant(other) - self

    def __mul__(
        self,
        other: _RationalFunction | int | Fraction,
    ) -> _RationalFunction:
        value = other if isinstance(other, _RationalFunction) else self.constant(other)
        return _RationalFunction(
            _polynomial_multiply(self.numerator, value.numerator),
            _polynomial_multiply(self.denominator, value.denominator),
        )

    def __rmul__(self, other: int | Fraction) -> _RationalFunction:
        return self * other

    def scale(self, factor: int | Fraction) -> _RationalFunction:
        scalar = Fraction(factor)
        return _RationalFunction(
            RationalPolynomial(
                tuple(scalar * value for value in self.numerator.coefficients)
            ),
            self.denominator,
        )

    def reciprocal(self) -> _RationalFunction:
        if self.numerator.coefficients == (Fraction(0),):
            raise ZeroDivisionError("formal rational function is zero")
        return _RationalFunction(self.denominator, self.numerator)

    def __truediv__(self, other: _RationalFunction) -> _RationalFunction:
        return self * other.reciprocal()

    def power(self, exponent: int) -> _RationalFunction:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("formal exponent must be a nonnegative integer")
        result = self.constant(1)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result

    def exactly_equals(self, other: _RationalFunction) -> bool:
        return _polynomial_multiply(
            self.numerator,
            other.denominator,
        ).coefficients == _polynomial_multiply(
            other.numerator,
            self.denominator,
        ).coefficients


@dataclass(frozen=True)
class _FormalTaylorOne:
    """Exact constant and linear coefficients in formal time ``t``."""

    constant: _RationalFunction
    linear: _RationalFunction

    @classmethod
    def point(
        cls,
        value: _RationalFunction | int | Fraction,
    ) -> _FormalTaylorOne:
        constant = (
            value
            if isinstance(value, _RationalFunction)
            else _RationalFunction.constant(value)
        )
        return cls(constant, _RationalFunction.constant(0))

    def __add__(
        self,
        other: _FormalTaylorOne | _RationalFunction | int | Fraction,
    ) -> _FormalTaylorOne:
        value = other if isinstance(other, _FormalTaylorOne) else self.point(other)
        return _FormalTaylorOne(
            self.constant + value.constant,
            self.linear + value.linear,
        )

    def __sub__(
        self,
        other: _FormalTaylorOne | _RationalFunction | int | Fraction,
    ) -> _FormalTaylorOne:
        value = other if isinstance(other, _FormalTaylorOne) else self.point(other)
        return self + value.scale(-1)

    def __mul__(
        self,
        other: _FormalTaylorOne | _RationalFunction | int | Fraction,
    ) -> _FormalTaylorOne:
        value = other if isinstance(other, _FormalTaylorOne) else self.point(other)
        return _FormalTaylorOne(
            self.constant * value.constant,
            self.constant * value.linear + self.linear * value.constant,
        )

    def scale(self, factor: int | Fraction) -> _FormalTaylorOne:
        return _FormalTaylorOne(
            self.constant.scale(factor),
            self.linear.scale(factor),
        )

    def reciprocal(self) -> _FormalTaylorOne:
        return _FormalTaylorOne(
            self.constant.reciprocal(),
            self.linear.scale(-1) / self.constant.power(2),
        )

    def __truediv__(self, other: _FormalTaylorOne) -> _FormalTaylorOne:
        return self * other.reciprocal()

    def power(self, exponent: int) -> _FormalTaylorOne:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("formal exponent must be a nonnegative integer")
        result = self.point(1)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result


@dataclass(frozen=True)
class _FormalTaylorTwo:
    """Exact coefficients through quadratic order in formal time ``t``."""

    constant: _RationalFunction
    linear: _RationalFunction
    quadratic: _RationalFunction

    @classmethod
    def point(
        cls,
        value: _RationalFunction | int | Fraction,
    ) -> _FormalTaylorTwo:
        constant = (
            value
            if isinstance(value, _RationalFunction)
            else _RationalFunction.constant(value)
        )
        zero = _RationalFunction.constant(0)
        return cls(constant, zero, zero)

    def __add__(
        self,
        other: _FormalTaylorTwo | _RationalFunction | int | Fraction,
    ) -> _FormalTaylorTwo:
        value = other if isinstance(other, _FormalTaylorTwo) else self.point(other)
        return _FormalTaylorTwo(
            self.constant + value.constant,
            self.linear + value.linear,
            self.quadratic + value.quadratic,
        )

    def __sub__(
        self,
        other: _FormalTaylorTwo | _RationalFunction | int | Fraction,
    ) -> _FormalTaylorTwo:
        value = other if isinstance(other, _FormalTaylorTwo) else self.point(other)
        return self + value.scale(-1)

    def __mul__(
        self,
        other: _FormalTaylorTwo | _RationalFunction | int | Fraction,
    ) -> _FormalTaylorTwo:
        value = other if isinstance(other, _FormalTaylorTwo) else self.point(other)
        return _FormalTaylorTwo(
            self.constant * value.constant,
            self.constant * value.linear + self.linear * value.constant,
            self.constant * value.quadratic
            + self.linear * value.linear
            + self.quadratic * value.constant,
        )

    def scale(self, factor: int | Fraction) -> _FormalTaylorTwo:
        return _FormalTaylorTwo(
            self.constant.scale(factor),
            self.linear.scale(factor),
            self.quadratic.scale(factor),
        )

    def reciprocal(self) -> _FormalTaylorTwo:
        q0 = self.constant.reciprocal()
        q1 = self.linear.scale(-1) / self.constant.power(2)
        q2 = (
            self.linear.power(2) - self.constant * self.quadratic
        ) / self.constant.power(3)
        return _FormalTaylorTwo(q0, q1, q2)

    def __truediv__(self, other: _FormalTaylorTwo) -> _FormalTaylorTwo:
        return self * other.reciprocal()

    def power(self, exponent: int) -> _FormalTaylorTwo:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("formal exponent must be a nonnegative integer")
        result = self.point(1)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result


def _assert_uniform_origin_center_identity(
    mass_squared: Fraction,
    curvature: Fraction,
) -> None:
    """Verify the exact ``t^0`` and ``t^1`` Volterra identities in formal ``b``."""
    slope = _RationalFunction.variable()
    slope_squared = slope.power(2)
    cubic = slope * (
        mass_squared
        - 4 * curvature
        + slope_squared.scale(Fraction(4, 3) - 24 * curvature)
        + slope_squared.power(2).scale(Fraction(8, 3))
    ) / (_RationalFunction.constant(10) * (1 + slope_squared.scale(8)))
    p0 = _FormalTaylorOne(slope, cubic.scale(-3))
    u0 = _FormalTaylorOne(slope, cubic.scale(-1))
    time = _FormalTaylorOne(
        _RationalFunction.constant(0),
        _RationalFunction.constant(1),
    )
    w = time * u0.power(2)
    sinc = _FormalTaylorOne.point(1) - w.scale(Fraction(1, 6))
    sinc_twice = _FormalTaylorOne.point(1) - w.scale(Fraction(2, 3))
    a = u0 * sinc
    lapse = _FormalTaylorOne.point(1) - time.scale(curvature)
    denominator = _FormalTaylorOne.point(1) + a.power(2).scale(8)
    bracket = (
        _FormalTaylorOne.point(1)
        + a.power(2).scale(4)
        + (lapse * p0.power(2)).scale(4)
    )
    source = (u0 * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _FormalTaylorOne(
        source.constant.scale(Fraction(1, 2)),
        source.linear.scale(Fraction(1, 4)),
    )
    image = integrated / (lapse * denominator)
    if not image.constant.exactly_equals(slope):
        raise AssertionError("formal origin constant coefficient identity failed")
    if not image.linear.exactly_equals(cubic.scale(-3)):
        raise AssertionError("formal origin cubic coefficient identity failed")


@lru_cache(maxsize=None)
def _assert_uniform_origin_quintic_center_identity(
    mass_squared: Fraction,
    curvature: Fraction,
) -> None:
    """Verify the exact ``t^0``, ``t^1``, and ``t^2`` Volterra identities."""
    slope = _RationalFunction.variable()
    slope_squared = slope.power(2)
    cubic = slope * (
        mass_squared
        - 4 * curvature
        + slope_squared.scale(Fraction(4, 3) - 24 * curvature)
        + slope_squared.power(2).scale(Fraction(8, 3))
    ) / (_RationalFunction.constant(10) * (1 + slope_squared.scale(8)))
    quintic = (
        slope * cubic.power(2).scale(192)
        + cubic
        * (
            18 * curvature
            - mass_squared
            + slope_squared.scale(184 * curvature - 4)
            + slope_squared.power(2).scale(24)
        )
        - slope.power(3).scale(mass_squared / 6)
        + slope.power(5).scale(Fraction(32, 3) * curvature - Fraction(4, 15))
        - slope.power(7).scale(Fraction(32, 15))
    ) / (_RationalFunction.constant(28) * (1 + slope_squared.scale(8)))
    momentum_quadratic = quintic.scale(-5)
    p0 = _FormalTaylorTwo(
        slope,
        cubic.scale(-3),
        momentum_quadratic,
    )
    u0 = _FormalTaylorTwo(
        slope,
        cubic.scale(-1),
        momentum_quadratic.scale(Fraction(1, 5)),
    )
    zero = _RationalFunction.constant(0)
    time = _FormalTaylorTwo(zero, _RationalFunction.constant(1), zero)
    w = time * u0.power(2)
    sinc = (
        _FormalTaylorTwo.point(1)
        - w.scale(Fraction(1, 6))
        + w.power(2).scale(Fraction(1, 120))
    )
    sinc_twice = (
        _FormalTaylorTwo.point(1)
        - w.scale(Fraction(2, 3))
        + w.power(2).scale(Fraction(2, 15))
    )
    a = u0 * sinc
    lapse = _FormalTaylorTwo.point(1) - time.scale(curvature)
    denominator = _FormalTaylorTwo.point(1) + a.power(2).scale(8)
    bracket = (
        _FormalTaylorTwo.point(1)
        + a.power(2).scale(4)
        + (lapse * p0.power(2)).scale(4)
    )
    source = (u0 * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _FormalTaylorTwo(
        source.constant.scale(Fraction(1, 2)),
        source.linear.scale(Fraction(1, 4)),
        source.quadratic.scale(Fraction(1, 6)),
    )
    image = integrated / (lapse * denominator)
    if not image.constant.exactly_equals(slope):
        raise AssertionError("formal origin constant coefficient identity failed")
    if not image.linear.exactly_equals(cubic.scale(-3)):
        raise AssertionError("formal origin cubic coefficient identity failed")
    if not image.quadratic.exactly_equals(momentum_quadratic):
        raise AssertionError("formal origin quintic coefficient identity failed")


@dataclass(frozen=True)
class _TaylorModelOne:
    """Represent ``c0+c1*t+t^2*r(t)``, with ``r(t)`` in ``remainder``."""

    constant: Fraction
    linear: Fraction
    remainder: RationalInterval
    horizon: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "constant", Fraction(self.constant))
        object.__setattr__(self, "linear", Fraction(self.linear))
        if not isinstance(self.remainder, RationalInterval):
            raise TypeError("remainder must be a RationalInterval")
        horizon = _fraction("horizon", self.horizon, positive=True)
        object.__setattr__(self, "horizon", horizon)

    @classmethod
    def point(
        cls,
        value: int | Fraction,
        horizon: Fraction,
    ) -> _TaylorModelOne:
        return cls(Fraction(value), Fraction(0), RationalInterval.point(0), horizon)

    def _check(self, other: _TaylorModelOne) -> None:
        if self.horizon != other.horizon:
            raise ValueError("Taylor-model horizons must agree")

    def __add__(self, other: _TaylorModelOne | int | Fraction) -> _TaylorModelOne:
        value = other if isinstance(other, _TaylorModelOne) else self.point(other, self.horizon)
        self._check(value)
        return _TaylorModelOne(
            self.constant + value.constant,
            self.linear + value.linear,
            self.remainder + value.remainder,
            self.horizon,
        )

    def __sub__(self, other: _TaylorModelOne | int | Fraction) -> _TaylorModelOne:
        value = other if isinstance(other, _TaylorModelOne) else self.point(other, self.horizon)
        return self + value.scale(-1)

    def scale(self, factor: int | Fraction) -> _TaylorModelOne:
        scalar = Fraction(factor)
        return _TaylorModelOne(
            scalar * self.constant,
            scalar * self.linear,
            self.remainder.scale(scalar),
            self.horizon,
        )

    def __mul__(self, other: _TaylorModelOne | int | Fraction) -> _TaylorModelOne:
        value = other if isinstance(other, _TaylorModelOne) else self.point(other, self.horizon)
        self._check(value)
        time = RationalInterval(Fraction(0), self.horizon)
        time_squared = RationalInterval(Fraction(0), self.horizon**2)
        remainder = (
            self.remainder.scale(value.constant)
            + value.remainder.scale(self.constant)
            + self.linear * value.linear
            + time
            * (
                value.remainder.scale(self.linear)
                + self.remainder.scale(value.linear)
            )
            + time_squared * self.remainder * value.remainder
        )
        return _TaylorModelOne(
            self.constant * value.constant,
            self.constant * value.linear + self.linear * value.constant,
            remainder,
            self.horizon,
        )

    def power(self, exponent: int) -> _TaylorModelOne:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Taylor-model exponent must be a nonnegative integer")
        result = self.point(1, self.horizon)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result

    def range(self) -> RationalInterval:
        time = RationalInterval(Fraction(0), self.horizon)
        return (
            RationalInterval.point(self.constant)
            + time.scale(self.linear)
            + RationalInterval(Fraction(0), self.horizon**2) * self.remainder
        )

    def reciprocal(self) -> _TaylorModelOne:
        value_range = self.range()
        if value_range.contains_zero():
            raise ZeroDivisionError("Taylor-model range contains zero")
        q0 = 1 / self.constant
        q1 = -self.linear / self.constant**2
        time = RationalInterval(Fraction(0), self.horizon)
        numerator_remainder = -(
            RationalInterval.point(self.linear * q1)
            + self.remainder.scale(q0)
            + time * self.remainder.scale(q1)
        )
        return _TaylorModelOne(
            q0,
            q1,
            numerator_remainder / value_range,
            self.horizon,
        )

    def __truediv__(self, other: _TaylorModelOne) -> _TaylorModelOne:
        return self * other.reciprocal()


@dataclass(frozen=True)
class _TaylorModelTwo:
    """Represent ``c0+c1*t+c2*t^2+t^3*r(t)`` exactly."""

    constant: Fraction
    linear: Fraction
    quadratic: Fraction
    remainder: RationalInterval
    horizon: Fraction

    def __post_init__(self) -> None:
        object.__setattr__(self, "constant", Fraction(self.constant))
        object.__setattr__(self, "linear", Fraction(self.linear))
        object.__setattr__(self, "quadratic", Fraction(self.quadratic))
        if not isinstance(self.remainder, RationalInterval):
            raise TypeError("remainder must be a RationalInterval")
        object.__setattr__(
            self,
            "horizon",
            _fraction("horizon", self.horizon, positive=True),
        )

    @classmethod
    def point(
        cls,
        value: int | Fraction,
        horizon: Fraction,
    ) -> _TaylorModelTwo:
        return cls(
            Fraction(value),
            Fraction(0),
            Fraction(0),
            RationalInterval.point(0),
            horizon,
        )

    def _check(self, other: _TaylorModelTwo) -> None:
        if self.horizon != other.horizon:
            raise ValueError("Taylor-model horizons must agree")

    def __add__(self, other: _TaylorModelTwo | int | Fraction) -> _TaylorModelTwo:
        value = other if isinstance(other, _TaylorModelTwo) else self.point(other, self.horizon)
        self._check(value)
        return _TaylorModelTwo(
            self.constant + value.constant,
            self.linear + value.linear,
            self.quadratic + value.quadratic,
            self.remainder + value.remainder,
            self.horizon,
        )

    def __sub__(self, other: _TaylorModelTwo | int | Fraction) -> _TaylorModelTwo:
        value = other if isinstance(other, _TaylorModelTwo) else self.point(other, self.horizon)
        return self + value.scale(-1)

    def scale(self, factor: int | Fraction) -> _TaylorModelTwo:
        scalar = Fraction(factor)
        return _TaylorModelTwo(
            scalar * self.constant,
            scalar * self.linear,
            scalar * self.quadratic,
            self.remainder.scale(scalar),
            self.horizon,
        )

    def __mul__(self, other: _TaylorModelTwo | int | Fraction) -> _TaylorModelTwo:
        value = other if isinstance(other, _TaylorModelTwo) else self.point(other, self.horizon)
        self._check(value)
        time = RationalInterval(Fraction(0), self.horizon)
        time_squared = RationalInterval(Fraction(0), self.horizon**2)
        time_cubed = RationalInterval(Fraction(0), self.horizon**3)
        remainder = (
            RationalInterval.point(
                self.linear * value.quadratic
                + self.quadratic * value.linear
            )
            + time.scale(self.quadratic * value.quadratic)
            + value.remainder.scale(self.constant)
            + time * value.remainder.scale(self.linear)
            + time_squared * value.remainder.scale(self.quadratic)
            + self.remainder.scale(value.constant)
            + time * self.remainder.scale(value.linear)
            + time_squared * self.remainder.scale(value.quadratic)
            + time_cubed * self.remainder * value.remainder
        )
        return _TaylorModelTwo(
            self.constant * value.constant,
            self.constant * value.linear + self.linear * value.constant,
            self.constant * value.quadratic
            + self.linear * value.linear
            + self.quadratic * value.constant,
            remainder,
            self.horizon,
        )

    def power(self, exponent: int) -> _TaylorModelTwo:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Taylor-model exponent must be a nonnegative integer")
        result = self.point(1, self.horizon)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result

    def range(self) -> RationalInterval:
        time = RationalInterval(Fraction(0), self.horizon)
        return (
            RationalInterval.point(self.constant)
            + time.scale(self.linear)
            + RationalInterval(Fraction(0), self.horizon**2).scale(
                self.quadratic
            )
            + RationalInterval(Fraction(0), self.horizon**3) * self.remainder
        )

    def reciprocal(self) -> _TaylorModelTwo:
        value_range = self.range()
        if value_range.contains_zero():
            raise ZeroDivisionError("Taylor-model range contains zero")
        q0 = 1 / self.constant
        q1 = -self.linear / self.constant**2
        q2 = (self.linear**2 - self.constant * self.quadratic) / self.constant**3
        time = RationalInterval(Fraction(0), self.horizon)
        time_squared = RationalInterval(Fraction(0), self.horizon**2)
        numerator_remainder = -(
            RationalInterval.point(
                self.linear * q2 + self.quadratic * q1
            )
            + time.scale(self.quadratic * q2)
            + self.remainder.scale(q0)
            + time * self.remainder.scale(q1)
            + time_squared * self.remainder.scale(q2)
        )
        return _TaylorModelTwo(
            q0,
            q1,
            q2,
            numerator_remainder / value_range,
            self.horizon,
        )

    def __truediv__(self, other: _TaylorModelTwo) -> _TaylorModelTwo:
        return self * other.reciprocal()


@dataclass(frozen=True)
class _TaylorModelFamily:
    """Uniformly enclose ``c0(b)+c1(b)*t+t^2*r(b,t)``."""

    constant: RationalInterval
    linear: RationalInterval
    remainder: RationalInterval
    horizon: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.constant, RationalInterval):
            raise TypeError("constant must be a RationalInterval")
        if not isinstance(self.linear, RationalInterval):
            raise TypeError("linear must be a RationalInterval")
        if not isinstance(self.remainder, RationalInterval):
            raise TypeError("remainder must be a RationalInterval")
        horizon = _fraction("horizon", self.horizon, positive=True)
        object.__setattr__(self, "horizon", horizon)

    @classmethod
    def point(
        cls,
        value: RationalInterval | int | Fraction,
        horizon: Fraction,
    ) -> _TaylorModelFamily:
        return cls(
            _as_interval(value),
            RationalInterval.point(0),
            RationalInterval.point(0),
            horizon,
        )

    def _check(self, other: _TaylorModelFamily) -> None:
        if self.horizon != other.horizon:
            raise ValueError("Taylor-model horizons must agree")

    def __add__(
        self,
        other: _TaylorModelFamily | RationalInterval | int | Fraction,
    ) -> _TaylorModelFamily:
        value = (
            other
            if isinstance(other, _TaylorModelFamily)
            else self.point(other, self.horizon)
        )
        self._check(value)
        return _TaylorModelFamily(
            self.constant + value.constant,
            self.linear + value.linear,
            self.remainder + value.remainder,
            self.horizon,
        )

    def __sub__(
        self,
        other: _TaylorModelFamily | RationalInterval | int | Fraction,
    ) -> _TaylorModelFamily:
        value = (
            other
            if isinstance(other, _TaylorModelFamily)
            else self.point(other, self.horizon)
        )
        return self + value.scale(-1)

    def scale(self, factor: int | Fraction) -> _TaylorModelFamily:
        scalar = Fraction(factor)
        return _TaylorModelFamily(
            self.constant.scale(scalar),
            self.linear.scale(scalar),
            self.remainder.scale(scalar),
            self.horizon,
        )

    def __mul__(
        self,
        other: _TaylorModelFamily | RationalInterval | int | Fraction,
    ) -> _TaylorModelFamily:
        value = (
            other
            if isinstance(other, _TaylorModelFamily)
            else self.point(other, self.horizon)
        )
        self._check(value)
        time = RationalInterval(Fraction(0), self.horizon)
        time_squared = RationalInterval(Fraction(0), self.horizon**2)
        remainder = (
            self.remainder * value.constant
            + value.remainder * self.constant
            + self.linear * value.linear
            + time
            * (
                value.remainder * self.linear
                + self.remainder * value.linear
            )
            + time_squared * self.remainder * value.remainder
        )
        return _TaylorModelFamily(
            self.constant * value.constant,
            self.constant * value.linear + self.linear * value.constant,
            remainder,
            self.horizon,
        )

    def power(self, exponent: int) -> _TaylorModelFamily:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Taylor-model exponent must be a nonnegative integer")
        result = self.point(1, self.horizon)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result

    def range(self) -> RationalInterval:
        time = RationalInterval(Fraction(0), self.horizon)
        return (
            self.constant
            + time * self.linear
            + RationalInterval(Fraction(0), self.horizon**2) * self.remainder
        )

    def reciprocal(self) -> _TaylorModelFamily:
        value_range = self.range()
        if self.constant.contains_zero() or value_range.contains_zero():
            raise ZeroDivisionError("Taylor-model range contains zero")
        q0 = RationalInterval.point(1) / self.constant
        q1 = -(self.linear / self.constant.power(2))
        time = RationalInterval(Fraction(0), self.horizon)
        numerator_remainder = -(
            self.linear * q1
            + self.remainder * q0
            + time * self.remainder * q1
        )
        return _TaylorModelFamily(
            q0,
            q1,
            numerator_remainder / value_range,
            self.horizon,
        )

    def __truediv__(self, other: _TaylorModelFamily) -> _TaylorModelFamily:
        return self * other.reciprocal()


def _entire_even_kernel_model(
    argument: _TaylorModelOne,
    *,
    scale_squared: int,
    argument_rate_upper: Fraction,
    terms: int,
) -> _TaylorModelOne:
    """Enclose ``sinc(scale*sqrt(w))`` as a first-order Taylor model."""
    if terms < 2:
        raise ValueError("kernel Taylor model requires at least two terms")
    total = _TaylorModelOne.point(0, argument.horizon)
    power = _TaylorModelOne.point(1, argument.horizon)
    for index in range(terms):
        coefficient = Fraction(
            (-1) ** index * scale_squared**index,
            factorial(2 * index + 1),
        )
        total = total + power.scale(coefficient)
        power = power * argument
    ratio = Fraction(scale_squared) * argument_rate_upper * argument.horizon / (
        (2 * terms + 2) * (2 * terms + 3)
    )
    if ratio >= 1:
        raise ValueError("kernel geometric-tail ratio must be below one")
    tail = (
        Fraction(scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper**terms
        * argument.horizon ** (terms - 2)
        / (1 - ratio)
    )
    return _TaylorModelOne(
        total.constant,
        total.linear,
        total.remainder + RationalInterval(-tail, tail),
        total.horizon,
    )


def _entire_even_kernel_model_two(
    argument: _TaylorModelTwo,
    *,
    scale_squared: int,
    argument_rate_upper: Fraction,
    terms: int,
) -> _TaylorModelTwo:
    """Enclose ``sinc(scale*sqrt(w))`` through quadratic order in ``t``."""
    if terms < 3:
        raise ValueError("quadratic kernel Taylor model requires at least three terms")
    total = _TaylorModelTwo.point(0, argument.horizon)
    power = _TaylorModelTwo.point(1, argument.horizon)
    for index in range(terms):
        coefficient = Fraction(
            (-1) ** index * scale_squared**index,
            factorial(2 * index + 1),
        )
        total = total + power.scale(coefficient)
        power = power * argument
    ratio = Fraction(scale_squared) * argument_rate_upper * argument.horizon / (
        (2 * terms + 2) * (2 * terms + 3)
    )
    if ratio >= 1:
        raise ValueError("kernel geometric-tail ratio must be below one")
    tail = (
        Fraction(scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper**terms
        * argument.horizon ** (terms - 3)
        / (1 - ratio)
    )
    return _TaylorModelTwo(
        total.constant,
        total.linear,
        total.quadratic,
        total.remainder + RationalInterval(-tail, tail),
        total.horizon,
    )


def _entire_even_kernel_family_model(
    argument: _TaylorModelFamily,
    *,
    scale_squared: int,
    argument_rate_upper: Fraction,
    terms: int,
) -> _TaylorModelFamily:
    """Uniformly enclose ``sinc(scale*sqrt(w))`` over a slope interval."""
    if terms < 2:
        raise ValueError("kernel Taylor model requires at least two terms")
    total = _TaylorModelFamily.point(0, argument.horizon)
    power = _TaylorModelFamily.point(1, argument.horizon)
    for index in range(terms):
        coefficient = Fraction(
            (-1) ** index * scale_squared**index,
            factorial(2 * index + 1),
        )
        total = total + power.scale(coefficient)
        power = power * argument
    ratio = Fraction(scale_squared) * argument_rate_upper * argument.horizon / (
        (2 * terms + 2) * (2 * terms + 3)
    )
    if ratio >= 1:
        raise ValueError("kernel geometric-tail ratio must be below one")
    tail = (
        Fraction(scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper**terms
        * argument.horizon ** (terms - 2)
        / (1 - ratio)
    )
    return _TaylorModelFamily(
        total.constant,
        total.linear,
        total.remainder + RationalInterval(-tail, tail),
        total.horizon,
    )


def _entire_even_kernel_interval(
    argument: RationalInterval,
    *,
    scale_squared: int,
    derivative_order: int,
    terms: int,
) -> RationalInterval:
    """Enclose a ``w`` derivative of ``sinc(scale*sqrt(w))``."""
    if argument.lower < 0:
        raise ValueError("even-kernel argument must be nonnegative")
    if derivative_order not in (0, 1):
        raise ValueError("only derivative orders zero and one are required")
    if terms <= derivative_order:
        raise ValueError("too few terms for requested kernel derivative")
    total = RationalInterval.point(0)
    for index in range(derivative_order, terms):
        falling = 1
        for offset in range(derivative_order):
            falling *= index - offset
        coefficient = Fraction(
            (-1) ** index * scale_squared**index * falling,
            factorial(2 * index + 1),
        )
        total = total + argument.power(index - derivative_order).scale(coefficient)
    maximum = argument.upper
    first_falling = 1
    for offset in range(derivative_order):
        first_falling *= terms - offset
    first = (
        Fraction(scale_squared**terms * first_falling, factorial(2 * terms + 1))
        * maximum ** (terms - derivative_order)
    )
    ratio = (
        Fraction(scale_squared)
        * maximum
        * Fraction(terms + 1, terms + 1 - derivative_order)
        / ((2 * terms + 2) * (2 * terms + 3))
    )
    if ratio >= 1:
        raise ValueError("kernel derivative geometric-tail ratio must be below one")
    tail = first / (1 - ratio)
    return total + RationalInterval(-tail, tail)


def _cubic_coefficient(
    slope: Fraction,
    mass_squared: Fraction,
    curvature: Fraction,
) -> Fraction:
    slope_squared = slope**2
    return slope * (
        mass_squared
        - 4 * curvature
        + (Fraction(4, 3) - 24 * curvature) * slope_squared
        + Fraction(8, 3) * slope_squared**2
    ) / (10 * (1 + 8 * slope_squared))


def _quintic_coefficient(
    slope: Fraction,
    cubic: Fraction,
    mass_squared: Fraction,
    curvature: Fraction,
) -> Fraction:
    """Return ``d`` in ``F=pi-b*x+c*x^3+d*x^5+O(x^7)``."""
    slope_squared = slope**2
    numerator = (
        192 * slope * cubic**2
        + cubic
        * (
            18 * curvature
            - mass_squared
            + (184 * curvature - 4) * slope_squared
            + 24 * slope_squared**2
        )
        - mass_squared * slope**3 / 6
        + (Fraction(32, 3) * curvature - Fraction(4, 15)) * slope**5
        - Fraction(32, 15) * slope**7
    )
    return numerator / (28 * (1 + 8 * slope_squared))


def _cubic_coefficient_interval(
    slopes: RationalInterval,
    mass_squared: Fraction,
    curvature: Fraction,
) -> RationalInterval:
    slope_squared = slopes.power(2)
    numerator = slopes * (
        RationalInterval.point(mass_squared - 4 * curvature)
        + slope_squared.scale(Fraction(4, 3) - 24 * curvature)
        + slope_squared.power(2).scale(Fraction(8, 3))
    )
    denominator = RationalInterval.point(10) * (
        RationalInterval.point(1) + slope_squared.scale(8)
    )
    return numerator / denominator


def _cubic_coefficient_derivative_interval(
    slopes: RationalInterval,
    mass_squared: Fraction,
    curvature: Fraction,
) -> RationalInterval:
    """Enclose ``dc/db`` directly from the exact rational formula."""
    slope_squared = slopes.power(2)
    slope_fourth = slope_squared.power(2)
    constant = mass_squared - 4 * curvature
    quadratic = Fraction(4, 3) - 24 * curvature
    quartic = Fraction(8, 3)
    numerator = slopes * (
        RationalInterval.point(constant)
        + slope_squared.scale(quadratic)
        + slope_fourth.scale(quartic)
    )
    numerator_derivative = (
        RationalInterval.point(constant)
        + slope_squared.scale(3 * quadratic)
        + slope_fourth.scale(5 * quartic)
    )
    denominator = (
        RationalInterval.point(1) + slope_squared.scale(8)
    ).scale(10)
    denominator_derivative = slopes.scale(160)
    return (
        numerator_derivative * denominator
        - numerator * denominator_derivative
    ) / denominator.power(2)


def _cubic_coefficient_second_derivative_interval(
    slopes: RationalInterval,
    mass_squared: Fraction,
    curvature: Fraction,
) -> RationalInterval:
    """Enclose ``d^2 c/db^2`` from the exact rational center coefficient."""
    slope_squared = slopes.power(2)
    slope_cubed = slope_squared * slopes
    slope_fourth = slope_squared.power(2)
    constant = mass_squared - 4 * curvature
    quadratic = Fraction(4, 3) - 24 * curvature
    quartic = Fraction(8, 3)
    numerator = slopes * (
        RationalInterval.point(constant)
        + slope_squared.scale(quadratic)
        + slope_fourth.scale(quartic)
    )
    numerator_derivative = (
        RationalInterval.point(constant)
        + slope_squared.scale(3 * quadratic)
        + slope_fourth.scale(5 * quartic)
    )
    numerator_second_derivative = (
        slopes.scale(6 * quadratic)
        + slope_cubed.scale(20 * quartic)
    )
    denominator = (
        RationalInterval.point(1) + slope_squared.scale(8)
    ).scale(10)
    denominator_derivative = slopes.scale(160)
    denominator_second_derivative = RationalInterval.point(160)
    return (
        numerator_second_derivative / denominator
        - numerator * denominator_second_derivative / denominator.power(2)
        - (
            numerator_derivative * denominator_derivative
        ).scale(2) / denominator.power(2)
        + numerator * denominator_derivative.power(2).scale(2)
        / denominator.power(3)
    )


@dataclass(frozen=True)
class _TaylorModelFamilySensitivity:
    """A family Taylor model and its derivative with respect to ``b``."""

    value: _TaylorModelFamily
    slope_derivative: _TaylorModelFamily

    def __post_init__(self) -> None:
        self.value._check(self.slope_derivative)

    @classmethod
    def point(
        cls,
        value: RationalInterval | int | Fraction,
        derivative: RationalInterval | int | Fraction,
        horizon: Fraction,
    ) -> _TaylorModelFamilySensitivity:
        return cls(
            _TaylorModelFamily.point(value, horizon),
            _TaylorModelFamily.point(derivative, horizon),
        )

    def __add__(
        self,
        other: _TaylorModelFamilySensitivity,
    ) -> _TaylorModelFamilySensitivity:
        return _TaylorModelFamilySensitivity(
            self.value + other.value,
            self.slope_derivative + other.slope_derivative,
        )

    def __sub__(
        self,
        other: _TaylorModelFamilySensitivity,
    ) -> _TaylorModelFamilySensitivity:
        return _TaylorModelFamilySensitivity(
            self.value - other.value,
            self.slope_derivative - other.slope_derivative,
        )

    def scale(self, factor: int | Fraction) -> _TaylorModelFamilySensitivity:
        return _TaylorModelFamilySensitivity(
            self.value.scale(factor),
            self.slope_derivative.scale(factor),
        )

    def __mul__(
        self,
        other: _TaylorModelFamilySensitivity,
    ) -> _TaylorModelFamilySensitivity:
        return _TaylorModelFamilySensitivity(
            self.value * other.value,
            self.slope_derivative * other.value
            + self.value * other.slope_derivative,
        )

    def power(self, exponent: int) -> _TaylorModelFamilySensitivity:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("sensitivity exponent must be a nonnegative integer")
        result = self.point(1, 0, self.value.horizon)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result

    def reciprocal(self) -> _TaylorModelFamilySensitivity:
        inverse = self.value.reciprocal()
        return _TaylorModelFamilySensitivity(
            inverse,
            (self.slope_derivative * inverse.power(2)).scale(-1),
        )

    def __truediv__(
        self,
        other: _TaylorModelFamilySensitivity,
    ) -> _TaylorModelFamilySensitivity:
        return self * other.reciprocal()


@dataclass(frozen=True)
class _TaylorModelFamilySecondSensitivity:
    """A family Taylor model with its first two ``b`` derivatives."""

    value: _TaylorModelFamily
    slope_derivative: _TaylorModelFamily
    slope_second_derivative: _TaylorModelFamily

    def __post_init__(self) -> None:
        self.value._check(self.slope_derivative)
        self.value._check(self.slope_second_derivative)

    @classmethod
    def point(
        cls,
        value: RationalInterval | int | Fraction,
        derivative: RationalInterval | int | Fraction,
        second_derivative: RationalInterval | int | Fraction,
        horizon: Fraction,
    ) -> _TaylorModelFamilySecondSensitivity:
        return cls(
            _TaylorModelFamily.point(value, horizon),
            _TaylorModelFamily.point(derivative, horizon),
            _TaylorModelFamily.point(second_derivative, horizon),
        )

    def __add__(
        self,
        other: _TaylorModelFamilySecondSensitivity,
    ) -> _TaylorModelFamilySecondSensitivity:
        return _TaylorModelFamilySecondSensitivity(
            self.value + other.value,
            self.slope_derivative + other.slope_derivative,
            self.slope_second_derivative + other.slope_second_derivative,
        )

    def __sub__(
        self,
        other: _TaylorModelFamilySecondSensitivity,
    ) -> _TaylorModelFamilySecondSensitivity:
        return _TaylorModelFamilySecondSensitivity(
            self.value - other.value,
            self.slope_derivative - other.slope_derivative,
            self.slope_second_derivative - other.slope_second_derivative,
        )

    def scale(
        self,
        factor: int | Fraction,
    ) -> _TaylorModelFamilySecondSensitivity:
        return _TaylorModelFamilySecondSensitivity(
            self.value.scale(factor),
            self.slope_derivative.scale(factor),
            self.slope_second_derivative.scale(factor),
        )

    def __mul__(
        self,
        other: _TaylorModelFamilySecondSensitivity,
    ) -> _TaylorModelFamilySecondSensitivity:
        return _TaylorModelFamilySecondSensitivity(
            self.value * other.value,
            self.slope_derivative * other.value
            + self.value * other.slope_derivative,
            self.slope_second_derivative * other.value
            + (self.slope_derivative * other.slope_derivative).scale(2)
            + self.value * other.slope_second_derivative,
        )

    def power(self, exponent: int) -> _TaylorModelFamilySecondSensitivity:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("second-sensitivity exponent must be nonnegative")
        result = self.point(1, 0, 0, self.value.horizon)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            factor = factor * factor
            power //= 2
        return result

    def reciprocal(self) -> _TaylorModelFamilySecondSensitivity:
        inverse = self.value.reciprocal()
        inverse_squared = inverse.power(2)
        return _TaylorModelFamilySecondSensitivity(
            inverse,
            (self.slope_derivative * inverse_squared).scale(-1),
            (self.slope_derivative.power(2) * inverse.power(3)).scale(2)
            - self.slope_second_derivative * inverse_squared,
        )

    def __truediv__(
        self,
        other: _TaylorModelFamilySecondSensitivity,
    ) -> _TaylorModelFamilySecondSensitivity:
        return self * other.reciprocal()


def _entire_even_kernel_family_sensitivity_model(
    argument: _TaylorModelFamilySensitivity,
    *,
    scale_squared: int,
    argument_rate_upper: Fraction,
    argument_rate_derivative_upper: Fraction,
    terms: int,
) -> _TaylorModelFamilySensitivity:
    """Differentiate the entire even-kernel Taylor model rigorously.

    The series tail and its slope derivative are bounded separately.  If
    ``|w| <= alpha*t`` and ``|d_b w| <= beta*t``, the differentiated first
    omitted term, divided by the Taylor-model weight ``t^2``, is bounded by
    ``N*s^(N)*alpha^(N-1)*beta*h^(N-2)/(2N+1)!``.
    """
    if terms < 2:
        raise ValueError("kernel Taylor model requires at least two terms")
    total = argument.point(0, 0, argument.value.horizon)
    power = argument.point(1, 0, argument.value.horizon)
    for index in range(terms):
        coefficient = Fraction(
            (-1) ** index * scale_squared**index,
            factorial(2 * index + 1),
        )
        total = total + power.scale(coefficient)
        power = power * argument
    ratio = Fraction(scale_squared) * argument_rate_upper * argument.value.horizon / (
        (2 * terms + 2) * (2 * terms + 3)
    )
    derivative_ratio = ratio * Fraction(terms + 1, terms)
    if ratio >= 1 or derivative_ratio >= 1:
        raise ValueError("kernel sensitivity geometric-tail ratio must be below one")
    value_tail = (
        Fraction(scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper**terms
        * argument.value.horizon ** (terms - 2)
        / (1 - ratio)
    )
    derivative_tail = (
        Fraction(terms * scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper ** (terms - 1)
        * argument_rate_derivative_upper
        * argument.value.horizon ** (terms - 2)
        / (1 - derivative_ratio)
    )
    return _TaylorModelFamilySensitivity(
        _TaylorModelFamily(
            total.value.constant,
            total.value.linear,
            total.value.remainder + RationalInterval(-value_tail, value_tail),
            total.value.horizon,
        ),
        _TaylorModelFamily(
            total.slope_derivative.constant,
            total.slope_derivative.linear,
            total.slope_derivative.remainder
            + RationalInterval(-derivative_tail, derivative_tail),
            total.value.horizon,
        ),
    )


def _entire_even_kernel_family_second_sensitivity_model(
    argument: _TaylorModelFamilySecondSensitivity,
    *,
    scale_squared: int,
    argument_rate_upper: Fraction,
    argument_rate_derivative_upper: Fraction,
    argument_rate_second_derivative_upper: Fraction,
    terms: int,
) -> _TaylorModelFamilySecondSensitivity:
    """Differentiate the entire even kernel twice with rigorous tails.

    For ``|w| <= alpha*t``, ``|w_b| <= beta*t``, and
    ``|w_bb| <= gamma*t``, the second derivative of ``w^n`` is bounded by
    ``n(n-1) alpha^(n-2) beta^2 t^n + n alpha^(n-1) gamma t^n``.
    The two resulting tails are summed with their separate geometric ratios.
    """
    if terms < 2:
        raise ValueError("kernel Taylor model requires at least two terms")
    total = argument.point(0, 0, 0, argument.value.horizon)
    power = argument.point(1, 0, 0, argument.value.horizon)
    for index in range(terms):
        coefficient = Fraction(
            (-1) ** index * scale_squared**index,
            factorial(2 * index + 1),
        )
        total = total + power.scale(coefficient)
        power = power * argument

    base_ratio = (
        Fraction(scale_squared)
        * argument_rate_upper
        * argument.value.horizon
        / ((2 * terms + 2) * (2 * terms + 3))
    )
    first_ratio = base_ratio * Fraction(terms + 1, terms)
    second_quadratic_ratio = base_ratio * Fraction(terms + 1, terms - 1)
    if (
        base_ratio >= 1
        or first_ratio >= 1
        or second_quadratic_ratio >= 1
    ):
        raise ValueError(
            "kernel second-sensitivity geometric-tail ratio must be below one"
        )
    value_tail = (
        Fraction(scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper**terms
        * argument.value.horizon ** (terms - 2)
        / (1 - base_ratio)
    )
    derivative_tail = (
        Fraction(terms * scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper ** (terms - 1)
        * argument_rate_derivative_upper
        * argument.value.horizon ** (terms - 2)
        / (1 - first_ratio)
    )
    quadratic_second_tail = (
        Fraction(
            terms * (terms - 1) * scale_squared**terms,
            factorial(2 * terms + 1),
        )
        * argument_rate_upper ** (terms - 2)
        * argument_rate_derivative_upper**2
        * argument.value.horizon ** (terms - 2)
        / (1 - second_quadratic_ratio)
    )
    linear_second_tail = (
        Fraction(terms * scale_squared**terms, factorial(2 * terms + 1))
        * argument_rate_upper ** (terms - 1)
        * argument_rate_second_derivative_upper
        * argument.value.horizon ** (terms - 2)
        / (1 - first_ratio)
    )
    second_derivative_tail = quadratic_second_tail + linear_second_tail
    return _TaylorModelFamilySecondSensitivity(
        _TaylorModelFamily(
            total.value.constant,
            total.value.linear,
            total.value.remainder + RationalInterval(-value_tail, value_tail),
            total.value.horizon,
        ),
        _TaylorModelFamily(
            total.slope_derivative.constant,
            total.slope_derivative.linear,
            total.slope_derivative.remainder
            + RationalInterval(-derivative_tail, derivative_tail),
            total.value.horizon,
        ),
        _TaylorModelFamily(
            total.slope_second_derivative.constant,
            total.slope_second_derivative.linear,
            total.slope_second_derivative.remainder
            + RationalInterval(-second_derivative_tail, second_derivative_tail),
            total.value.horizon,
        ),
    )


@dataclass(frozen=True)
class ValidatedSkyrmionOriginPatch:
    shooting_slope: Fraction
    cutoff: Fraction
    cubic_coefficient: Fraction
    remainder_radius: Fraction
    residual_bound: Fraction
    contraction_bound: Fraction
    profile_at_cutoff: RationalInterval
    derivative_at_cutoff: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionOriginQuinticPatch:
    shooting_slope: Fraction
    cutoff: Fraction
    pion_mass_squared: Fraction
    curvature: Fraction
    cubic_coefficient: Fraction
    quintic_coefficient: Fraction
    remainder_radius: Fraction
    residual_bound: Fraction
    contraction_bound: Fraction
    profile_at_cutoff: RationalInterval
    derivative_at_cutoff: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionOriginFamily:
    shooting_slopes: RationalInterval
    cutoff: Fraction
    pion_mass_squared: Fraction
    curvature: Fraction
    cubic_coefficient: RationalInterval
    remainder_radius: Fraction
    residual_bound: Fraction
    contraction_bound: Fraction
    volterra_denominator_lower_bound: Fraction
    profile_at_cutoff: RationalInterval
    derivative_at_cutoff: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionOriginSensitivity:
    shooting_slopes: RationalInterval
    cutoff: Fraction
    remainder_radius: Fraction
    pion_mass_squared: Fraction
    curvature: Fraction
    cubic_coefficient_derivative: RationalInterval
    contraction_bound: Fraction
    partial_map_sensitivity_bound: Fraction
    fixed_point_sensitivity_bound: Fraction
    continuously_differentiable: bool
    profile_sensitivity_at_cutoff: RationalInterval
    derivative_sensitivity_at_cutoff: RationalInterval

    @property
    def phi_b(self) -> RationalInterval:
        """Return ``dF_b(cutoff)/db``."""
        return self.profile_sensitivity_at_cutoff

    @property
    def gamma_b(self) -> RationalInterval:
        """Return ``dF'_b(cutoff)/db``."""
        return self.derivative_sensitivity_at_cutoff


@dataclass(frozen=True)
class ValidatedSkyrmionOriginSecondSensitivity:
    shooting_slopes: RationalInterval
    cutoff: Fraction
    remainder_radius: Fraction
    pion_mass_squared: Fraction
    curvature: Fraction
    cubic_coefficient_second_derivative: RationalInterval
    contraction_bound: Fraction
    first_fixed_point_sensitivity_bound: Fraction
    partial_second_sensitivity_bound: Fraction
    fixed_point_second_sensitivity_bound: Fraction
    twice_continuously_differentiable: bool
    profile_second_sensitivity_at_cutoff: RationalInterval
    derivative_second_sensitivity_at_cutoff: RationalInterval

    @property
    def phi_bb(self) -> RationalInterval:
        """Return ``d^2 F_b(cutoff)/db^2``."""
        return self.profile_second_sensitivity_at_cutoff

    @property
    def gamma_bb(self) -> RationalInterval:
        """Return ``d^2 F'_b(cutoff)/db^2``."""
        return self.derivative_second_sensitivity_at_cutoff


@dataclass(frozen=True)
class ValidatedSkyrmionOriginQuinticBranchIdentification:
    quintic_patch: ValidatedSkyrmionOriginQuinticPatch
    cubic_sensitivity: ValidatedSkyrmionOriginSensitivity
    normalized_momentum_offset_upper_bound: Fraction
    normalized_profile_offset_upper_bound: Fraction
    identified_with_cubic_sensitivity_branch: bool


DEFAULT_SHOOTING_SLOPE_FAMILY = RationalInterval(
    Fraction(1_579_953, 1_000_000),
    Fraction(1_579_954, 1_000_000),
)


def validate_skyrmion_origin_quintic_patch(
    shooting_slope: Fraction,
    *,
    cutoff: Fraction = Fraction(1, 16),
    remainder_radius: Fraction = Fraction(13, 10),
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    kernel_terms: int = 8,
    pi_terms: int = 64,
) -> ValidatedSkyrmionOriginQuinticPatch:
    """Validate a point origin patch centered through the ``x^5`` term.

    With ``t=x^2``, the checked ball is

    ``|p-(b-3*c*t-5*d*t^2)| <= R*t^3`` and
    ``|u-(b-c*t-d*t^2)| <= R*t^3/7``.

    This point theorem narrows the initial box for global integration.  The
    separate uniform slope-sensitivity theorems remain cubic-centered.
    """
    slope = _fraction("shooting_slope", shooting_slope, positive=True)
    radius = _fraction("cutoff", cutoff, positive=True)
    remainder = _fraction("remainder_radius", remainder_radius, positive=True)
    mass_squared = _fraction("pion_mass_squared", pion_mass_squared)
    curvature_value = _fraction("curvature", curvature)
    if mass_squared < 0 or curvature_value < 0:
        raise ValueError("mass squared and curvature must be nonnegative")
    if (
        isinstance(kernel_terms, bool)
        or not isinstance(kernel_terms, int)
        or kernel_terms < 3
    ):
        raise ValueError("kernel_terms must be an integer at least three")
    horizon = radius**2
    if curvature_value * horizon >= 1:
        raise ValueError("origin patch must remain strictly inside the horizon")

    _assert_uniform_origin_quintic_center_identity(
        mass_squared,
        curvature_value,
    )
    cubic = _cubic_coefficient(slope, mass_squared, curvature_value)
    quintic = _quintic_coefficient(
        slope,
        cubic,
        mass_squared,
        curvature_value,
    )
    linear = -3 * cubic
    quadratic = -5 * quintic
    zero = RationalInterval.point(0)
    p0 = _TaylorModelTwo(slope, linear, quadratic, zero, horizon)
    u0 = _TaylorModelTwo(
        slope,
        linear / 3,
        quadratic / 5,
        zero,
        horizon,
    )
    time = _TaylorModelTwo(
        Fraction(0),
        Fraction(1),
        Fraction(0),
        zero,
        horizon,
    )
    u_abs = _abs_upper(u0.range())
    w = time * u0.power(2)
    argument_rate = u_abs**2
    sinc = _entire_even_kernel_model_two(
        w,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    sinc_twice = _entire_even_kernel_model_two(
        w,
        scale_squared=4,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    a = u0 * sinc
    lapse = _TaylorModelTwo.point(1, horizon) - time.scale(curvature_value)
    denominator = _TaylorModelTwo.point(1, horizon) + a.power(2).scale(8)
    bracket = (
        _TaylorModelTwo.point(1, horizon)
        + a.power(2).scale(4)
        + (lapse * p0.power(2)).scale(4)
    )
    source = (u0 * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _TaylorModelTwo(
        source.constant / 2,
        source.linear / 4,
        source.quadratic / 6,
        source.remainder.scale(Fraction(1, 8)),
        horizon,
    )
    image = integrated / (lapse * denominator)
    if (
        image.constant != slope
        or image.linear != linear
        or image.quadratic != quadratic
    ):
        raise AssertionError("origin quintic center coefficient identity failed")
    residual_bound = _abs_upper(image.remainder)

    p_ball = _TaylorModelTwo(
        slope,
        linear,
        quadratic,
        RationalInterval(-remainder, remainder),
        horizon,
    ).range()
    u_ball = _TaylorModelTwo(
        slope,
        linear / 3,
        quadratic / 5,
        RationalInterval(-remainder / 7, remainder / 7),
        horizon,
    ).range()
    t_box = RationalInterval(Fraction(0), horizon)
    lapse_box = RationalInterval(1 - curvature_value * horizon, 1)
    u_abs_ball = _abs_upper(u_ball)
    w_box = RationalInterval(Fraction(0), horizon * u_abs_ball**2)
    s_box = _entire_even_kernel_interval(
        w_box, scale_squared=1, derivative_order=0, terms=kernel_terms
    )
    sp_box = _entire_even_kernel_interval(
        w_box, scale_squared=1, derivative_order=1, terms=kernel_terms
    )
    c_box = _entire_even_kernel_interval(
        w_box, scale_squared=4, derivative_order=0, terms=kernel_terms
    )
    cp_box = _entire_even_kernel_interval(
        w_box, scale_squared=4, derivative_order=1, terms=kernel_terms
    )
    a_box = u_ball * s_box
    a_u = s_box + (w_box * sp_box).scale(2)
    c_u = (t_box * u_ball * cp_box).scale(2)
    d_box = RationalInterval.point(1) + a_box.power(2).scale(8)
    e_box = lapse_box * d_box
    if e_box.lower <= 0:
        raise ValueError("Volterra denominator enclosure must be positive")
    h_box = (
        RationalInterval.point(1)
        + a_box.power(2).scale(4)
        + (lapse_box * p_ball.power(2)).scale(4)
    )
    q_box = (u_ball * c_box * h_box).scale(2) - (
        t_box * a_box
    ).scale(mass_squared)
    h_u = (a_box * a_u).scale(8)
    q_u = (
        (c_box + u_ball * c_u) * h_box
        + u_ball * c_box * h_u
    ).scale(2) - (t_box * a_u).scale(mass_squared)
    q_p = (lapse_box * u_ball * c_box * p_ball).scale(16)
    e_u = (lapse_box * a_box * a_u).scale(16)
    q_max = _abs_upper(q_box)
    ju = _abs_upper(q_u)
    jp = _abs_upper(q_p)
    eu = _abs_upper(e_u)
    contraction_bound = (
        (jp + ju / 7) / (8 * e_box.lower)
        + q_max * eu / (14 * e_box.lower**2)
    )
    if contraction_bound >= 1:
        raise ValueError("weighted Volterra contraction bound is not below one")
    if residual_bound + contraction_bound * remainder > remainder:
        raise ValueError("origin radii inequality does not close")

    p_center = slope + linear * horizon + quadratic * horizon**2
    u_center = slope + linear * horizon / 3 + quadratic * horizon**2 / 5
    p_error = remainder * horizon**3
    u_error = remainder * horizon**3 / 7
    p_endpoint = RationalInterval(p_center - p_error, p_center + p_error)
    u_endpoint = RationalInterval(u_center - u_error, u_center + u_error)
    profile = pi_machin_interval(terms=pi_terms) - u_endpoint.scale(radius)
    derivative = -p_endpoint
    return ValidatedSkyrmionOriginQuinticPatch(
        shooting_slope=slope,
        cutoff=radius,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        cubic_coefficient=cubic,
        quintic_coefficient=quintic,
        remainder_radius=remainder,
        residual_bound=residual_bound,
        contraction_bound=contraction_bound,
        profile_at_cutoff=profile,
        derivative_at_cutoff=derivative,
    )


def validate_skyrmion_origin_patch(
    shooting_slope: Fraction,
    *,
    cutoff: Fraction = Fraction(1, 16),
    remainder_radius: Fraction = Fraction(13, 10),
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    kernel_terms: int = 8,
    pi_terms: int = 64,
) -> ValidatedSkyrmionOriginPatch:
    """Validate one regular origin solution through a rational cutoff.

    The checked ball is

    ``|p(t) - (b-3*c(b)*t)| <= R*t^2``, ``0<=t<=cutoff^2``.

    A returned value proves existence and uniqueness inside this weighted ball.
    It is not a shooting or wall-boundary certificate.
    """
    slope = _fraction("shooting_slope", shooting_slope, positive=True)
    radius = _fraction("cutoff", cutoff, positive=True)
    remainder = _fraction("remainder_radius", remainder_radius, positive=True)
    mass_squared = _fraction("pion_mass_squared", pion_mass_squared)
    curvature_value = _fraction("curvature", curvature)
    if mass_squared < 0 or curvature_value < 0:
        raise ValueError("mass squared and curvature must be nonnegative")
    if (
        isinstance(kernel_terms, bool)
        or not isinstance(kernel_terms, int)
        or kernel_terms < 3
    ):
        raise ValueError("kernel_terms must be an integer at least three")
    horizon = radius**2
    if curvature_value * horizon >= 1:
        raise ValueError("origin patch must remain strictly inside the horizon")

    cubic = _cubic_coefficient(slope, mass_squared, curvature_value)
    linear = -3 * cubic
    zero = RationalInterval.point(0)
    p0 = _TaylorModelOne(slope, linear, zero, horizon)
    u0 = _TaylorModelOne(slope, linear / 3, zero, horizon)
    time = _TaylorModelOne(Fraction(0), Fraction(1), zero, horizon)
    u_range = u0.range()
    u_abs = _abs_upper(u_range)
    w = time * u0.power(2)
    argument_rate = u_abs**2
    sinc = _entire_even_kernel_model(
        w,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    sinc_twice = _entire_even_kernel_model(
        w,
        scale_squared=4,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    a = u0 * sinc
    lapse = _TaylorModelOne.point(1, horizon) - time.scale(curvature_value)
    denominator = _TaylorModelOne.point(1, horizon) + a.power(2).scale(8)
    bracket = (
        _TaylorModelOne.point(1, horizon)
        + a.power(2).scale(4)
        + (lapse * p0.power(2)).scale(4)
    )
    source = (u0 * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _TaylorModelOne(
        source.constant / 2,
        source.linear / 4,
        source.remainder.scale(Fraction(1, 6)),
        horizon,
    )
    image = integrated / (lapse * denominator)
    if image.constant != slope or image.linear != linear:
        raise AssertionError("origin constant/cubic coefficient identity failed")
    residual_bound = _abs_upper(image.remainder)

    p_ball = _TaylorModelOne(
        slope,
        linear,
        RationalInterval(-remainder, remainder),
        horizon,
    ).range()
    u_ball = _TaylorModelOne(
        slope,
        linear / 3,
        RationalInterval(-remainder / 5, remainder / 5),
        horizon,
    ).range()
    t_box = RationalInterval(Fraction(0), horizon)
    lapse_box = RationalInterval(1 - curvature_value * horizon, 1)
    u_abs_ball = _abs_upper(u_ball)
    w_box = RationalInterval(Fraction(0), horizon * u_abs_ball**2)
    s_box = _entire_even_kernel_interval(
        w_box, scale_squared=1, derivative_order=0, terms=kernel_terms
    )
    sp_box = _entire_even_kernel_interval(
        w_box, scale_squared=1, derivative_order=1, terms=kernel_terms
    )
    c_box = _entire_even_kernel_interval(
        w_box, scale_squared=4, derivative_order=0, terms=kernel_terms
    )
    cp_box = _entire_even_kernel_interval(
        w_box, scale_squared=4, derivative_order=1, terms=kernel_terms
    )
    a_box = u_ball * s_box
    a_u = s_box + (w_box * sp_box).scale(2)
    c_u = (t_box * u_ball * cp_box).scale(2)
    d_box = RationalInterval.point(1) + a_box.power(2).scale(8)
    e_box = lapse_box * d_box
    if e_box.lower <= 0:
        raise ValueError("Volterra denominator enclosure must be positive")
    h_box = (
        RationalInterval.point(1)
        + a_box.power(2).scale(4)
        + (lapse_box * p_ball.power(2)).scale(4)
    )
    q_box = (u_ball * c_box * h_box).scale(2) - (
        t_box * a_box
    ).scale(mass_squared)
    h_u = (a_box * a_u).scale(8)
    q_u = (
        (c_box + u_ball * c_u) * h_box
        + u_ball * c_box * h_u
    ).scale(2) - (t_box * a_u).scale(mass_squared)
    q_p = (lapse_box * u_ball * c_box * p_ball).scale(16)
    e_u = (lapse_box * a_box * a_u).scale(16)
    q_max = _abs_upper(q_box)
    ju = _abs_upper(q_u)
    jp = _abs_upper(q_p)
    eu = _abs_upper(e_u)
    contraction_bound = (
        (jp + ju / 5) / (6 * e_box.lower)
        + q_max * eu / (10 * e_box.lower**2)
    )
    if contraction_bound >= 1:
        raise ValueError("weighted Volterra contraction bound is not below one")
    if residual_bound + contraction_bound * remainder > remainder:
        raise ValueError("origin radii inequality does not close")

    p_center = slope + linear * horizon
    u_center = slope + linear * horizon / 3
    p_endpoint = RationalInterval(
        p_center - remainder * horizon**2,
        p_center + remainder * horizon**2,
    )
    u_endpoint = RationalInterval(
        u_center - remainder * horizon**2 / 5,
        u_center + remainder * horizon**2 / 5,
    )
    profile = pi_machin_interval(terms=pi_terms) - u_endpoint.scale(radius)
    derivative = -p_endpoint
    return ValidatedSkyrmionOriginPatch(
        shooting_slope=slope,
        cutoff=radius,
        cubic_coefficient=cubic,
        remainder_radius=remainder,
        residual_bound=residual_bound,
        contraction_bound=contraction_bound,
        profile_at_cutoff=profile,
        derivative_at_cutoff=derivative,
    )


def validate_skyrmion_origin_family(
    shooting_slopes: RationalInterval = DEFAULT_SHOOTING_SLOPE_FAMILY,
    *,
    cutoff: Fraction = Fraction(1, 16),
    remainder_radius: Fraction = Fraction(13, 10),
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    kernel_terms: int = 8,
    pi_terms: int = 64,
) -> ValidatedSkyrmionOriginFamily:
    """Validate every slope in a rational interval by one uniform proof.

    For each ``b`` in ``shooting_slopes``, the ball has the parameter-dependent
    center

    ``p_b(t)=b-3*c(b)*t+t^2*r(t)``, ``||r||_infinity <= R``.

    All Taylor coefficients, nonlinear ranges, and derivative bounds below are
    evaluated over the full parameter interval.  The cutoff enclosure is
    therefore not inferred from endpoint solutions.  Exact coefficient
    extraction in the Volterra equation gives the constant coefficient ``b``;
    solving its linear identity gives ``-3*c(b)`` with ``c`` as defined by
    :func:`_cubic_coefficient`.  The interval Taylor model bounds the remaining
    ``t^2`` coefficient uniformly.

    The returned uniform contraction proves a unique fixed point in every
    displayed ball.  In the translated remainder coordinates the Volterra map
    is jointly analytic in ``b`` and the remainder while its denominator stays
    uniformly positive.  The parameterized contraction theorem consequently
    makes the fixed point, and hence the reconstructed profile, continuous in
    ``b`` on the whole interval.
    """
    if not isinstance(shooting_slopes, RationalInterval):
        raise TypeError("shooting_slopes must be a RationalInterval")
    if shooting_slopes.lower <= 0:
        raise ValueError("shooting slopes must be positive")
    radius = _fraction("cutoff", cutoff, positive=True)
    remainder = _fraction("remainder_radius", remainder_radius, positive=True)
    mass_squared = _fraction("pion_mass_squared", pion_mass_squared)
    curvature_value = _fraction("curvature", curvature)
    if mass_squared < 0 or curvature_value < 0:
        raise ValueError("mass squared and curvature must be nonnegative")
    if (
        isinstance(kernel_terms, bool)
        or not isinstance(kernel_terms, int)
        or kernel_terms < 3
    ):
        raise ValueError("kernel_terms must be an integer at least three")
    horizon = radius**2
    if curvature_value * horizon >= 1:
        raise ValueError("origin patch must remain strictly inside the horizon")

    _assert_uniform_origin_center_identity(mass_squared, curvature_value)
    cubic_box = _cubic_coefficient_interval(
        shooting_slopes,
        mass_squared,
        curvature_value,
    )
    linear_box = cubic_box.scale(-3)
    zero = RationalInterval.point(0)
    p0 = _TaylorModelFamily(
        shooting_slopes,
        linear_box,
        zero,
        horizon,
    )
    u0 = _TaylorModelFamily(
        shooting_slopes,
        cubic_box.scale(-1),
        zero,
        horizon,
    )
    time = _TaylorModelFamily(zero, RationalInterval.point(1), zero, horizon)
    u_range = u0.range()
    u_abs = _abs_upper(u_range)
    w = time * u0.power(2)
    argument_rate = u_abs**2
    sinc = _entire_even_kernel_family_model(
        w,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    sinc_twice = _entire_even_kernel_family_model(
        w,
        scale_squared=4,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    a = u0 * sinc
    lapse = _TaylorModelFamily.point(1, horizon) - time.scale(curvature_value)
    denominator = _TaylorModelFamily.point(1, horizon) + a.power(2).scale(8)
    bracket = (
        _TaylorModelFamily.point(1, horizon)
        + a.power(2).scale(4)
        + (lapse * p0.power(2)).scale(4)
    )
    source = (u0 * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _TaylorModelFamily(
        source.constant.scale(Fraction(1, 2)),
        source.linear.scale(Fraction(1, 4)),
        source.remainder.scale(Fraction(1, 6)),
        horizon,
    )
    image = integrated / (lapse * denominator)
    if not shooting_slopes.is_subset_of(image.constant):
        raise AssertionError("uniform origin constant coefficient enclosure failed")
    if not linear_box.is_subset_of(image.linear):
        raise AssertionError("uniform cubic coefficient enclosure failed")
    residual_bound = _abs_upper(image.remainder)

    p_ball = _TaylorModelFamily(
        shooting_slopes,
        linear_box,
        RationalInterval(-remainder, remainder),
        horizon,
    ).range()
    u_ball = _TaylorModelFamily(
        shooting_slopes,
        cubic_box.scale(-1),
        RationalInterval(-remainder / 5, remainder / 5),
        horizon,
    ).range()
    t_box = RationalInterval(Fraction(0), horizon)
    lapse_box = RationalInterval(1 - curvature_value * horizon, 1)
    u_abs_ball = _abs_upper(u_ball)
    w_box = RationalInterval(Fraction(0), horizon * u_abs_ball**2)
    s_box = _entire_even_kernel_interval(
        w_box, scale_squared=1, derivative_order=0, terms=kernel_terms
    )
    sp_box = _entire_even_kernel_interval(
        w_box, scale_squared=1, derivative_order=1, terms=kernel_terms
    )
    c_box = _entire_even_kernel_interval(
        w_box, scale_squared=4, derivative_order=0, terms=kernel_terms
    )
    cp_box = _entire_even_kernel_interval(
        w_box, scale_squared=4, derivative_order=1, terms=kernel_terms
    )
    a_box = u_ball * s_box
    a_u = s_box + (w_box * sp_box).scale(2)
    c_u = (t_box * u_ball * cp_box).scale(2)
    d_box = RationalInterval.point(1) + a_box.power(2).scale(8)
    e_box = lapse_box * d_box
    if e_box.lower <= 0:
        raise ValueError("Volterra denominator enclosure must be positive")
    h_box = (
        RationalInterval.point(1)
        + a_box.power(2).scale(4)
        + (lapse_box * p_ball.power(2)).scale(4)
    )
    q_box = (u_ball * c_box * h_box).scale(2) - (
        t_box * a_box
    ).scale(mass_squared)
    h_u = (a_box * a_u).scale(8)
    q_u = (
        (c_box + u_ball * c_u) * h_box
        + u_ball * c_box * h_u
    ).scale(2) - (t_box * a_u).scale(mass_squared)
    q_p = (lapse_box * u_ball * c_box * p_ball).scale(16)
    e_u = (lapse_box * a_box * a_u).scale(16)
    q_max = _abs_upper(q_box)
    ju = _abs_upper(q_u)
    jp = _abs_upper(q_p)
    eu = _abs_upper(e_u)
    contraction_bound = (
        (jp + ju / 5) / (6 * e_box.lower)
        + q_max * eu / (10 * e_box.lower**2)
    )
    if contraction_bound >= 1:
        raise ValueError("uniform weighted Volterra contraction bound is not below one")
    if residual_bound + contraction_bound * remainder > remainder:
        raise ValueError("uniform origin radii inequality does not close")

    p_endpoint = (
        shooting_slopes
        + linear_box.scale(horizon)
        + RationalInterval(-remainder * horizon**2, remainder * horizon**2)
    )
    u_endpoint = (
        shooting_slopes
        + cubic_box.scale(-horizon)
        + RationalInterval(
            -remainder * horizon**2 / 5,
            remainder * horizon**2 / 5,
        )
    )
    profile = pi_machin_interval(terms=pi_terms) - u_endpoint.scale(radius)
    derivative = -p_endpoint
    return ValidatedSkyrmionOriginFamily(
        shooting_slopes=shooting_slopes,
        cutoff=radius,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        cubic_coefficient=cubic_box,
        remainder_radius=remainder,
        residual_bound=residual_bound,
        contraction_bound=contraction_bound,
        volterra_denominator_lower_bound=e_box.lower,
        profile_at_cutoff=profile,
        derivative_at_cutoff=derivative,
    )


def validate_skyrmion_origin_sensitivity(
    shooting_slopes: RationalInterval = DEFAULT_SHOOTING_SLOPE_FAMILY,
    *,
    cutoff: Fraction = Fraction(1, 16),
    remainder_radius: Fraction = Fraction(13, 10),
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    kernel_terms: int = 8,
) -> ValidatedSkyrmionOriginSensitivity:
    """Certify ``C^1`` slope dependence and the two cutoff sensitivities.

    Write the fixed point in translated coordinates as

    ``p_b(t)=b-3*c(b)*t+t^2*r_b(t)``.

    Exact interval automatic differentiation of the parameterized Volterra
    map, with ``r`` held fixed in the already validated common ball, gives the
    bound ``M`` returned as ``partial_map_sensitivity_bound``.  If ``q`` is the
    uniform contraction constant, the differentiated contraction equation
    gives ``||d_b r_b|| <= M/(1-q)``.  Thus the endpoint intervals below are
    direct derivative enclosures, not finite differences of endpoint boxes.
    """
    family = validate_skyrmion_origin_family(
        shooting_slopes,
        cutoff=cutoff,
        remainder_radius=remainder_radius,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        kernel_terms=kernel_terms,
    )
    radius = family.cutoff
    horizon = radius**2
    remainder = family.remainder_radius
    mass_squared = _fraction("pion_mass_squared", pion_mass_squared)
    curvature_value = _fraction("curvature", curvature)
    cubic_derivative = _cubic_coefficient_derivative_interval(
        family.shooting_slopes,
        mass_squared,
        curvature_value,
    )
    zero = RationalInterval.point(0)
    one = RationalInterval.point(1)
    p = _TaylorModelFamilySensitivity(
        _TaylorModelFamily(
            family.shooting_slopes,
            family.cubic_coefficient.scale(-3),
            RationalInterval(-remainder, remainder),
            horizon,
        ),
        _TaylorModelFamily(
            one,
            cubic_derivative.scale(-3),
            zero,
            horizon,
        ),
    )
    u = _TaylorModelFamilySensitivity(
        _TaylorModelFamily(
            family.shooting_slopes,
            family.cubic_coefficient.scale(-1),
            RationalInterval(-remainder / 5, remainder / 5),
            horizon,
        ),
        _TaylorModelFamily(
            one,
            cubic_derivative.scale(-1),
            zero,
            horizon,
        ),
    )
    time = _TaylorModelFamilySensitivity(
        _TaylorModelFamily(zero, one, zero, horizon),
        _TaylorModelFamily.point(0, horizon),
    )
    u_abs = _abs_upper(u.value.range())
    u_derivative_abs = _abs_upper(u.slope_derivative.range())
    argument = time * u.power(2)
    argument_rate = u_abs**2
    argument_rate_derivative = 2 * u_abs * u_derivative_abs
    sinc = _entire_even_kernel_family_sensitivity_model(
        argument,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        argument_rate_derivative_upper=argument_rate_derivative,
        terms=kernel_terms,
    )
    sinc_twice = _entire_even_kernel_family_sensitivity_model(
        argument,
        scale_squared=4,
        argument_rate_upper=argument_rate,
        argument_rate_derivative_upper=argument_rate_derivative,
        terms=kernel_terms,
    )
    constant_one = _TaylorModelFamilySensitivity.point(1, 0, horizon)
    a = u * sinc
    lapse = constant_one - time.scale(curvature_value)
    denominator = constant_one + a.power(2).scale(8)
    bracket = (
        constant_one
        + a.power(2).scale(4)
        + (lapse * p.power(2)).scale(4)
    )
    source = (u * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _TaylorModelFamilySensitivity(
        _TaylorModelFamily(
            source.value.constant.scale(Fraction(1, 2)),
            source.value.linear.scale(Fraction(1, 4)),
            source.value.remainder.scale(Fraction(1, 6)),
            horizon,
        ),
        _TaylorModelFamily(
            source.slope_derivative.constant.scale(Fraction(1, 2)),
            source.slope_derivative.linear.scale(Fraction(1, 4)),
            source.slope_derivative.remainder.scale(Fraction(1, 6)),
            horizon,
        ),
    )
    image = integrated / (lapse * denominator)
    if not one.is_subset_of(image.slope_derivative.constant):
        raise AssertionError("origin sensitivity constant identity failed")
    if not cubic_derivative.scale(-3).is_subset_of(
        image.slope_derivative.linear
    ):
        raise AssertionError("origin sensitivity cubic identity failed")
    partial_bound = _abs_upper(image.slope_derivative.remainder)
    fixed_point_bound = partial_bound / (1 - family.contraction_bound)

    p_sensitivity = (
        one
        + cubic_derivative.scale(-3 * horizon)
        + RationalInterval(
            -fixed_point_bound * horizon**2,
            fixed_point_bound * horizon**2,
        )
    )
    u_sensitivity = (
        one
        + cubic_derivative.scale(-horizon)
        + RationalInterval(
            -fixed_point_bound * horizon**2 / 5,
            fixed_point_bound * horizon**2 / 5,
        )
    )
    return ValidatedSkyrmionOriginSensitivity(
        shooting_slopes=family.shooting_slopes,
        cutoff=radius,
        remainder_radius=remainder,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        cubic_coefficient_derivative=cubic_derivative,
        contraction_bound=family.contraction_bound,
        partial_map_sensitivity_bound=partial_bound,
        fixed_point_sensitivity_bound=fixed_point_bound,
        continuously_differentiable=True,
        profile_sensitivity_at_cutoff=u_sensitivity.scale(-radius),
        derivative_sensitivity_at_cutoff=-p_sensitivity,
    )


def validate_skyrmion_origin_second_sensitivity(
    shooting_slopes: RationalInterval = DEFAULT_SHOOTING_SLOPE_FAMILY,
    *,
    cutoff: Fraction = Fraction(1, 16),
    remainder_radius: Fraction = Fraction(13, 10),
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    kernel_terms: int = 8,
) -> ValidatedSkyrmionOriginSecondSensitivity:
    """Certify ``C^2`` slope dependence and cutoff second derivatives.

    For the translated fixed point ``r_b=T(b,r_b)``, differentiating twice
    gives

    ``(I-T_r) r_bb = T_bb + 2 T_br r_b + T_rr[r_b,r_b]``.

    The first sensitivity proof supplies a common ball for ``r_b``.  Exact
    second-order interval automatic differentiation evaluates the right-hand
    side with ``r_bb`` set to zero, thereby bounding the full forcing term.
    Division by ``1-q`` then bounds ``r_bb``.  No finite differences or
    endpoint interpolation enter the calculation.
    """
    first = validate_skyrmion_origin_sensitivity(
        shooting_slopes,
        cutoff=cutoff,
        remainder_radius=remainder_radius,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        kernel_terms=kernel_terms,
    )
    family = validate_skyrmion_origin_family(
        shooting_slopes,
        cutoff=cutoff,
        remainder_radius=remainder_radius,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        kernel_terms=kernel_terms,
    )
    radius = family.cutoff
    horizon = radius**2
    remainder = family.remainder_radius
    first_remainder_bound = first.fixed_point_sensitivity_bound
    mass_squared = _fraction("pion_mass_squared", pion_mass_squared)
    curvature_value = _fraction("curvature", curvature)
    cubic_derivative = first.cubic_coefficient_derivative
    cubic_second_derivative = _cubic_coefficient_second_derivative_interval(
        family.shooting_slopes,
        mass_squared,
        curvature_value,
    )
    zero = RationalInterval.point(0)
    one = RationalInterval.point(1)
    p = _TaylorModelFamilySecondSensitivity(
        _TaylorModelFamily(
            family.shooting_slopes,
            family.cubic_coefficient.scale(-3),
            RationalInterval(-remainder, remainder),
            horizon,
        ),
        _TaylorModelFamily(
            one,
            cubic_derivative.scale(-3),
            RationalInterval(-first_remainder_bound, first_remainder_bound),
            horizon,
        ),
        _TaylorModelFamily(
            zero,
            cubic_second_derivative.scale(-3),
            zero,
            horizon,
        ),
    )
    u = _TaylorModelFamilySecondSensitivity(
        _TaylorModelFamily(
            family.shooting_slopes,
            family.cubic_coefficient.scale(-1),
            RationalInterval(-remainder / 5, remainder / 5),
            horizon,
        ),
        _TaylorModelFamily(
            one,
            cubic_derivative.scale(-1),
            RationalInterval(
                -first_remainder_bound / 5,
                first_remainder_bound / 5,
            ),
            horizon,
        ),
        _TaylorModelFamily(
            zero,
            cubic_second_derivative.scale(-1),
            zero,
            horizon,
        ),
    )
    time = _TaylorModelFamilySecondSensitivity(
        _TaylorModelFamily(zero, one, zero, horizon),
        _TaylorModelFamily.point(0, horizon),
        _TaylorModelFamily.point(0, horizon),
    )
    u_abs = _abs_upper(u.value.range())
    u_derivative_abs = _abs_upper(u.slope_derivative.range())
    u_second_derivative_abs = _abs_upper(u.slope_second_derivative.range())
    argument = time * u.power(2)
    argument_rate = u_abs**2
    argument_rate_derivative = 2 * u_abs * u_derivative_abs
    argument_rate_second_derivative = 2 * (
        u_derivative_abs**2 + u_abs * u_second_derivative_abs
    )
    sinc = _entire_even_kernel_family_second_sensitivity_model(
        argument,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        argument_rate_derivative_upper=argument_rate_derivative,
        argument_rate_second_derivative_upper=argument_rate_second_derivative,
        terms=kernel_terms,
    )
    sinc_twice = _entire_even_kernel_family_second_sensitivity_model(
        argument,
        scale_squared=4,
        argument_rate_upper=argument_rate,
        argument_rate_derivative_upper=argument_rate_derivative,
        argument_rate_second_derivative_upper=argument_rate_second_derivative,
        terms=kernel_terms,
    )
    constant_one = _TaylorModelFamilySecondSensitivity.point(1, 0, 0, horizon)
    a = u * sinc
    lapse = constant_one - time.scale(curvature_value)
    denominator = constant_one + a.power(2).scale(8)
    bracket = (
        constant_one
        + a.power(2).scale(4)
        + (lapse * p.power(2)).scale(4)
    )
    source = (u * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _TaylorModelFamilySecondSensitivity(
        _TaylorModelFamily(
            source.value.constant.scale(Fraction(1, 2)),
            source.value.linear.scale(Fraction(1, 4)),
            source.value.remainder.scale(Fraction(1, 6)),
            horizon,
        ),
        _TaylorModelFamily(
            source.slope_derivative.constant.scale(Fraction(1, 2)),
            source.slope_derivative.linear.scale(Fraction(1, 4)),
            source.slope_derivative.remainder.scale(Fraction(1, 6)),
            horizon,
        ),
        _TaylorModelFamily(
            source.slope_second_derivative.constant.scale(Fraction(1, 2)),
            source.slope_second_derivative.linear.scale(Fraction(1, 4)),
            source.slope_second_derivative.remainder.scale(Fraction(1, 6)),
            horizon,
        ),
    )
    image = integrated / (lapse * denominator)
    if not zero.is_subset_of(image.slope_second_derivative.constant):
        raise AssertionError("origin second-sensitivity constant identity failed")
    if not cubic_second_derivative.scale(-3).is_subset_of(
        image.slope_second_derivative.linear
    ):
        raise AssertionError("origin second-sensitivity cubic identity failed")
    partial_second_bound = _abs_upper(
        image.slope_second_derivative.remainder
    )
    fixed_point_second_bound = partial_second_bound / (
        1 - family.contraction_bound
    )

    p_second_sensitivity = (
        cubic_second_derivative.scale(-3 * horizon)
        + RationalInterval(
            -fixed_point_second_bound * horizon**2,
            fixed_point_second_bound * horizon**2,
        )
    )
    u_second_sensitivity = (
        cubic_second_derivative.scale(-horizon)
        + RationalInterval(
            -fixed_point_second_bound * horizon**2 / 5,
            fixed_point_second_bound * horizon**2 / 5,
        )
    )
    return ValidatedSkyrmionOriginSecondSensitivity(
        shooting_slopes=family.shooting_slopes,
        cutoff=radius,
        remainder_radius=remainder,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        cubic_coefficient_second_derivative=cubic_second_derivative,
        contraction_bound=family.contraction_bound,
        first_fixed_point_sensitivity_bound=first_remainder_bound,
        partial_second_sensitivity_bound=partial_second_bound,
        fixed_point_second_sensitivity_bound=fixed_point_second_bound,
        twice_continuously_differentiable=True,
        profile_second_sensitivity_at_cutoff=u_second_sensitivity.scale(-radius),
        derivative_second_sensitivity_at_cutoff=-p_second_sensitivity,
    )


def validate_skyrmion_origin_quintic_branch_identification(
    quintic_patch: ValidatedSkyrmionOriginQuinticPatch,
    cubic_sensitivity: ValidatedSkyrmionOriginSensitivity,
) -> ValidatedSkyrmionOriginQuinticBranchIdentification:
    """Identify the quintic point fixed point with the cubic sensitivity branch.

    The quintic weighted ball is proved to lie strictly inside the cubic ball
    at the same slope.  Uniqueness in the cubic fiber then identifies the two
    Banach fixed points without claiming unrestricted origin uniqueness.
    """
    if not isinstance(quintic_patch, ValidatedSkyrmionOriginQuinticPatch):
        raise TypeError("quintic_patch must be a validated quintic patch")
    if not isinstance(cubic_sensitivity, ValidatedSkyrmionOriginSensitivity):
        raise TypeError("cubic_sensitivity must be a validated sensitivity")
    if not cubic_sensitivity.shooting_slopes.contains(
        quintic_patch.shooting_slope
    ):
        raise ValueError("quintic slope is outside the sensitivity family")
    if quintic_patch.cutoff != cubic_sensitivity.cutoff:
        raise ValueError("origin cutoff values must agree")
    if (
        quintic_patch.pion_mass_squared
        != cubic_sensitivity.pion_mass_squared
        or quintic_patch.curvature != cubic_sensitivity.curvature
    ):
        raise ValueError("origin operator parameters must agree")
    expected_cubic = _cubic_coefficient(
        quintic_patch.shooting_slope,
        quintic_patch.pion_mass_squared,
        quintic_patch.curvature,
    )
    if quintic_patch.cubic_coefficient != expected_cubic:
        raise ValueError("quintic patch carries an inconsistent cubic center")
    horizon = quintic_patch.cutoff**2
    momentum_offset = (
        5 * abs(quintic_patch.quintic_coefficient)
        + quintic_patch.remainder_radius * horizon
    )
    profile_offset = (
        abs(quintic_patch.quintic_coefficient)
        + quintic_patch.remainder_radius * horizon / 7
    )
    if momentum_offset > cubic_sensitivity.remainder_radius:
        raise ValueError("quintic momentum ball is not inside the cubic ball")
    if profile_offset > cubic_sensitivity.remainder_radius / 5:
        raise ValueError("quintic profile ball is not inside the cubic ball")
    return ValidatedSkyrmionOriginQuinticBranchIdentification(
        quintic_patch=quintic_patch,
        cubic_sensitivity=cubic_sensitivity,
        normalized_momentum_offset_upper_bound=momentum_offset,
        normalized_profile_offset_upper_bound=profile_offset,
        identified_with_cubic_sensitivity_branch=True,
    )


def validated_skyrmion_origin_certificate() -> dict[str, object]:
    """Validate the full default rational shooting-slope interval."""
    family = validate_skyrmion_origin_family()
    sensitivity = validate_skyrmion_origin_sensitivity()
    second_sensitivity = validate_skyrmion_origin_second_sensitivity()
    quintic = validate_skyrmion_origin_quintic_patch(
        family.shooting_slopes.lower
    )
    branch_identification = validate_skyrmion_origin_quintic_branch_identification(
        quintic,
        sensitivity,
    )
    checks = {
        "formal_center_identities_hold_exactly": True,
        "uniform_family_radii_inequality_closes": (
            family.residual_bound
            + family.contraction_bound * family.remainder_radius
            <= family.remainder_radius
        ),
        "uniform_family_map_is_a_contraction": family.contraction_bound < 1,
        "volterra_denominator_is_uniformly_positive": (
            family.volterra_denominator_lower_bound > 0
        ),
        "fixed_point_depends_continuously_on_slope": (
            family.contraction_bound < 1
            and family.volterra_denominator_lower_bound > 0
        ),
        "origin_map_is_continuously_differentiable": (
            sensitivity.continuously_differentiable
        ),
        "origin_map_is_twice_continuously_differentiable": (
            second_sensitivity.twice_continuously_differentiable
        ),
        "quintic_point_patch_is_identified_with_family_branch": (
            branch_identification.identified_with_cubic_sensitivity_branch
        ),
        "origin_value_and_derivative_sensitivities_are_negative": (
            sensitivity.phi_b.upper < 0
            and sensitivity.gamma_b.upper < 0
        ),
        "cutoff_profile_is_strictly_between_zero_and_pi": (
            family.profile_at_cutoff.lower > 0
            and family.profile_at_cutoff.upper
            < pi_machin_interval(terms=64).lower
        ),
        "cutoff_derivative_is_strictly_negative": (
            family.derivative_at_cutoff.upper < 0
        ),
    }
    return {
        "goal": "Validated Skyrmion Uniform Regular Origin Family",
        "status": "pass" if all(checks.values()) else "fail",
        "result_type": "uniform_exact_rational_parameter_volterra_contraction",
        "central_result": (
            "For every rational or irrational shooting slope b in the displayed "
            "closed rational interval, one uniform weighted Volterra contraction "
            "proves a unique fixed point in the parameter-dependent cubic ball. "
            "The fixed point depends continuously on b and reconstructs a "
            "regular curved-Skyrmion solution through the rational cutoff. "
            "Exact interval differentiation also certifies two derivatives "
            "with respect to b on the full family."
        ),
        "executable_checks": checks,
        "shooting_slopes": [
            str(family.shooting_slopes.lower),
            str(family.shooting_slopes.upper),
        ],
        "shooting_slope_interval": {
            "lower": str(family.shooting_slopes.lower),
            "upper": str(family.shooting_slopes.upper),
        },
        "cutoff": str(family.cutoff),
        "remainder_radius": str(family.remainder_radius),
        "uniform_residual_bound": str(family.residual_bound),
        "uniform_contraction_bound": str(family.contraction_bound),
        "volterra_denominator_lower_bound": str(
            family.volterra_denominator_lower_bound
        ),
        "profile_at_cutoff": {
            "lower": str(family.profile_at_cutoff.lower),
            "upper": str(family.profile_at_cutoff.upper),
        },
        "derivative_at_cutoff": {
            "lower": str(family.derivative_at_cutoff.lower),
            "upper": str(family.derivative_at_cutoff.upper),
        },
        "profile_sensitivity_at_cutoff": _outward_decimal_interval(
            sensitivity.phi_b
        ),
        "derivative_sensitivity_at_cutoff": _outward_decimal_interval(
            sensitivity.gamma_b
        ),
        "profile_second_sensitivity_at_cutoff": _outward_decimal_interval(
            second_sensitivity.phi_bb
        ),
        "derivative_second_sensitivity_at_cutoff": _outward_decimal_interval(
            second_sensitivity.gamma_bb
        ),
        "quintic_point_slope": str(quintic.shooting_slope),
        "quintic_coefficient": str(quintic.quintic_coefficient),
        "quintic_profile_at_cutoff": _outward_decimal_interval(
            quintic.profile_at_cutoff
        ),
        "quintic_derivative_at_cutoff": _outward_decimal_interval(
            quintic.derivative_at_cutoff
        ),
        "quintic_to_cubic_momentum_nesting_bound": str(
            branch_identification.normalized_momentum_offset_upper_bound
        ),
        "quintic_to_cubic_profile_nesting_bound": str(
            branch_identification.normalized_profile_offset_upper_bound
        ),
        "analytic_remainder": (
            "Uniformly for every b in B, "
            "|F_b-(pi-b*x+c(b)*x^3)| <= R*x^5/5 and "
            "|F_b'-(-b+3*c(b)*x^2)| <= R*x^4 on the full patch."
        ),
        "continuous_dependence": (
            "After translating by the analytic cubic center, the Volterra map "
            "is jointly analytic in b and the weighted remainder on a common "
            "closed ball, has a uniformly positive denominator, and has the "
            "displayed contraction constant q<1. The parameterized contraction "
            "theorem and its twice-differentiated fixed-point equation therefore "
            "give C^2 dependence of the fixed point on b throughout B."
        ),
        "cutoff_box_method": (
            "The cutoff profile and derivative boxes are direct exact interval "
            "evaluations of b, c(b), and the uniform weighted remainder over "
            "the full parameter interval B; they are not endpoint hulls."
        ),
        "claim_boundary": (
            "This validates the complete displayed slope family only within "
            "the declared parameter-dependent weighted balls. It does not prove "
            "unrestricted uniqueness, propagate the family to the wall, or "
            "prove opposite wall signs."
        ),
    }
