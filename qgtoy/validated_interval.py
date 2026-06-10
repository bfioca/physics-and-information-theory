"""Dependency-free rational interval primitives for validated numerics.

This module deliberately avoids floating-point transcendental functions.  Its
endpoints are exact :class:`fractions.Fraction` values, while transcendental
constants and point evaluations are enclosed by rational series remainders.
It is infrastructure for the Skyrmion validated-profile program, not itself a
validated ODE solver.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial, isqrt


def _as_fraction(value: int | Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError("interval endpoints must be integers or Fractions")
    return Fraction(value)


@dataclass(frozen=True)
class RationalInterval:
    """Closed interval with exact rational endpoints."""

    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        lower = _as_fraction(self.lower)
        upper = _as_fraction(self.upper)
        if lower > upper:
            raise ValueError("interval endpoints must be ordered")
        object.__setattr__(self, "lower", lower)
        object.__setattr__(self, "upper", upper)

    @classmethod
    def point(cls, value: int | Fraction) -> RationalInterval:
        fraction = _as_fraction(value)
        return cls(fraction, fraction)

    @property
    def width(self) -> Fraction:
        return self.upper - self.lower

    @property
    def midpoint(self) -> Fraction:
        return (self.lower + self.upper) / 2

    def contains(self, value: int | Fraction) -> bool:
        fraction = _as_fraction(value)
        return self.lower <= fraction <= self.upper

    def contains_zero(self) -> bool:
        return self.lower <= 0 <= self.upper

    def is_subset_of(self, other: RationalInterval) -> bool:
        return other.lower <= self.lower and self.upper <= other.upper

    def __add__(
        self,
        other: RationalInterval | int | Fraction,
    ) -> RationalInterval:
        interval = _as_interval(other)
        return RationalInterval(
            self.lower + interval.lower,
            self.upper + interval.upper,
        )

    def __sub__(
        self,
        other: RationalInterval | int | Fraction,
    ) -> RationalInterval:
        interval = _as_interval(other)
        return RationalInterval(
            self.lower - interval.upper,
            self.upper - interval.lower,
        )

    def __mul__(
        self,
        other: RationalInterval | int | Fraction,
    ) -> RationalInterval:
        interval = _as_interval(other)
        products = (
            self.lower * interval.lower,
            self.lower * interval.upper,
            self.upper * interval.lower,
            self.upper * interval.upper,
        )
        return RationalInterval(min(products), max(products))

    def __truediv__(
        self,
        other: RationalInterval | int | Fraction,
    ) -> RationalInterval:
        interval = _as_interval(other)
        if interval.contains_zero():
            raise ZeroDivisionError("cannot divide by an interval containing zero")
        reciprocal = RationalInterval(
            1 / interval.upper,
            1 / interval.lower,
        )
        return self * reciprocal

    def __neg__(self) -> RationalInterval:
        return RationalInterval(-self.upper, -self.lower)

    def scale(self, factor: int | Fraction) -> RationalInterval:
        fraction = _as_fraction(factor)
        if fraction >= 0:
            return RationalInterval(
                fraction * self.lower,
                fraction * self.upper,
            )
        return RationalInterval(
            fraction * self.upper,
            fraction * self.lower,
        )

    def power(self, exponent: int) -> RationalInterval:
        if isinstance(exponent, bool) or not isinstance(exponent, int):
            raise TypeError("exponent must be an integer")
        if exponent < 0:
            return RationalInterval.point(1) / self.power(-exponent)
        if exponent == 0:
            return RationalInterval.point(1)
        if exponent % 2 == 1:
            return RationalInterval(
                self.lower**exponent,
                self.upper**exponent,
            )
        maximum = max(abs(self.lower), abs(self.upper)) ** exponent
        minimum = 0 if self.contains_zero() else min(
            self.lower**exponent,
            self.upper**exponent,
        )
        return RationalInterval(minimum, maximum)

    def hull(self, other: RationalInterval) -> RationalInterval:
        """Return the smallest interval containing both intervals."""
        return RationalInterval(
            min(self.lower, other.lower),
            max(self.upper, other.upper),
        )

    def interior_contains(self, other: RationalInterval) -> bool:
        """Return whether ``other`` lies strictly inside this interval."""
        return self.lower < other.lower and other.upper < self.upper


def _as_interval(
    value: RationalInterval | int | Fraction,
) -> RationalInterval:
    if isinstance(value, RationalInterval):
        return value
    return RationalInterval.point(value)


def arctan_fraction_interval(
    value: Fraction,
    *,
    terms: int = 80,
) -> RationalInterval:
    """Enclose ``atan(value)`` for an exact rational ``|value|<=1``."""
    value = _as_fraction(value)
    if abs(value) > 1:
        raise ValueError("arctan series requires |value|<=1")
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    if value < 0:
        return -arctan_fraction_interval(-value, terms=terms)
    total = Fraction(0)
    squared = value * value
    power = value
    sign = 1
    for index in range(terms):
        total += sign * power / (2 * index + 1)
        power *= squared
        sign = -sign
    next_term = sign * power / (2 * terms + 1)
    return RationalInterval(min(total, total + next_term), max(total, total + next_term))


def pi_machin_interval(*, terms: int = 80) -> RationalInterval:
    """Enclose ``pi`` using Machin's exact arctangent identity."""
    first = arctan_fraction_interval(Fraction(1, 5), terms=terms)
    second = arctan_fraction_interval(Fraction(1, 239), terms=terms)
    return first.scale(16) - second.scale(4)


def sin_fraction_interval(
    value: Fraction,
    *,
    terms: int = 40,
) -> RationalInterval:
    """Enclose ``sin(value)`` by a rational Taylor polynomial and remainder."""
    value = _as_fraction(value)
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    total = Fraction(0)
    for index in range(terms):
        total += (-1) ** index * value ** (2 * index + 1) / factorial(
            2 * index + 1
        )
    remainder = abs(value) ** (2 * terms + 1) / factorial(2 * terms + 1)
    return RationalInterval(total - remainder, total + remainder)


def cos_fraction_interval(
    value: Fraction,
    *,
    terms: int = 40,
) -> RationalInterval:
    """Enclose ``cos(value)`` by a rational Taylor polynomial and remainder."""
    value = _as_fraction(value)
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    total = Fraction(0)
    for index in range(terms):
        total += (-1) ** index * value ** (2 * index) / factorial(2 * index)
    remainder = abs(value) ** (2 * terms) / factorial(2 * terms)
    return RationalInterval(total - remainder, total + remainder)


def sin_center_lipschitz_interval(
    value: RationalInterval,
    *,
    terms: int = 40,
) -> RationalInterval:
    """Enclose sine from its midpoint value and global Lipschitz constant."""
    if not isinstance(value, RationalInterval):
        raise TypeError("value must be a RationalInterval")
    center_value = sin_fraction_interval(value.midpoint, terms=terms)
    radius = value.width / 2
    expanded = center_value + RationalInterval(-radius, radius)
    return RationalInterval(
        max(Fraction(-1), expanded.lower),
        min(Fraction(1), expanded.upper),
    )


def cos_center_lipschitz_interval(
    value: RationalInterval,
    *,
    terms: int = 40,
) -> RationalInterval:
    """Enclose cosine from its midpoint value and global Lipschitz constant."""
    if not isinstance(value, RationalInterval):
        raise TypeError("value must be a RationalInterval")
    center_value = cos_fraction_interval(value.midpoint, terms=terms)
    radius = value.width / 2
    expanded = center_value + RationalInterval(-radius, radius)
    return RationalInterval(
        max(Fraction(-1), expanded.lower),
        min(Fraction(1), expanded.upper),
    )


def sin_interval(
    value: RationalInterval,
    *,
    terms: int = 40,
) -> RationalInterval:
    """Enclose ``sin(x)`` for every ``x`` in a rational interval.

    The Taylor polynomial is evaluated by interval arithmetic and the global
    Lagrange remainder uses ``|sin^(n)(x)|<=1``.  This is intentionally broad
    but dependency free; later Taylor models can recenter it when needed.
    """
    if not isinstance(value, RationalInterval):
        raise TypeError("value must be a RationalInterval")
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    total = RationalInterval.point(0)
    for index in range(terms):
        term = value.power(2 * index + 1).scale(
            Fraction((-1) ** index, factorial(2 * index + 1))
        )
        total = total + term
    maximum = max(abs(value.lower), abs(value.upper))
    remainder = maximum ** (2 * terms + 1) / factorial(2 * terms + 1)
    return total + RationalInterval(-remainder, remainder)


def cos_interval(
    value: RationalInterval,
    *,
    terms: int = 40,
) -> RationalInterval:
    """Enclose ``cos(x)`` for every ``x`` in a rational interval."""
    if not isinstance(value, RationalInterval):
        raise TypeError("value must be a RationalInterval")
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    total = RationalInterval.point(0)
    for index in range(terms):
        term = value.power(2 * index).scale(
            Fraction((-1) ** index, factorial(2 * index))
        )
        total = total + term
    maximum = max(abs(value.lower), abs(value.upper))
    remainder = maximum ** (2 * terms) / factorial(2 * terms)
    return total + RationalInterval(-remainder, remainder)


@dataclass(frozen=True)
class RationalPolynomial:
    """Polynomial with exact rational coefficients in ascending order."""

    coefficients: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if not self.coefficients:
            raise ValueError("polynomial must contain at least one coefficient")
        normalized = tuple(_as_fraction(value) for value in self.coefficients)
        while len(normalized) > 1 and normalized[-1] == 0:
            normalized = normalized[:-1]
        object.__setattr__(self, "coefficients", normalized)

    @property
    def degree(self) -> int:
        return len(self.coefficients) - 1

    def evaluate(
        self,
        value: RationalInterval | int | Fraction,
    ) -> RationalInterval:
        interval = _as_interval(value)
        result = RationalInterval.point(0)
        for coefficient in reversed(self.coefficients):
            result = result * interval + coefficient
        return result

    def derivative(self) -> RationalPolynomial:
        if self.degree == 0:
            return RationalPolynomial((Fraction(0),))
        return RationalPolynomial(
            tuple(
                index * coefficient
                for index, coefficient in enumerate(self.coefficients)
                if index > 0
            )
        )

    def integral(self, constant: int | Fraction = 0) -> RationalPolynomial:
        return RationalPolynomial(
            (_as_fraction(constant),)
            + tuple(
                coefficient / (index + 1)
                for index, coefficient in enumerate(self.coefficients)
            )
        )

    def shift(self, center: int | Fraction) -> RationalPolynomial:
        """Return coefficients of ``p(x+center)`` exactly."""
        center_fraction = _as_fraction(center)
        result = [Fraction(0)] * len(self.coefficients)
        for power, coefficient in enumerate(self.coefficients):
            binomial = 1
            for shifted_power in range(power + 1):
                if shifted_power > 0:
                    binomial = binomial * (power - shifted_power + 1) // shifted_power
                result[shifted_power] += (
                    coefficient
                    * binomial
                    * center_fraction ** (power - shifted_power)
                )
        return RationalPolynomial(tuple(result))


def atanh_fraction_interval(
    value: Fraction,
    *,
    terms: int = 80,
) -> RationalInterval:
    """Enclose ``atanh(value)`` for an exact rational ``|value|<1``."""
    value = _as_fraction(value)
    if abs(value) >= 1:
        raise ValueError("atanh series requires |value|<1")
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    if value < 0:
        return -atanh_fraction_interval(-value, terms=terms)
    total = Fraction(0)
    squared = value * value
    power = value
    for index in range(terms):
        total += power / (2 * index + 1)
        power *= squared
    tail_upper = power / ((2 * terms + 1) * (1 - squared))
    return RationalInterval(total, total + tail_upper)


def sqrt_fraction_interval(
    value: Fraction,
    *,
    bisection_steps: int = 160,
) -> RationalInterval:
    """Enclose the nonnegative square root of an exact rational."""
    value = _as_fraction(value)
    if value < 0:
        raise ValueError("square root requires a nonnegative value")
    if (
        isinstance(bisection_steps, bool)
        or not isinstance(bisection_steps, int)
        or bisection_steps < 1
    ):
        raise ValueError("bisection_steps must be a positive integer")
    numerator_root = isqrt(value.numerator)
    denominator_root = isqrt(value.denominator)
    if (
        numerator_root * numerator_root == value.numerator
        and denominator_root * denominator_root == value.denominator
    ):
        return RationalInterval.point(Fraction(numerator_root, denominator_root))
    low = Fraction(0)
    high = max(Fraction(1), value)
    for _ in range(bisection_steps):
        middle = (low + high) / 2
        if middle * middle <= value:
            low = middle
        else:
            high = middle
    return RationalInterval(low, high)


def _interval_record(interval: RationalInterval) -> dict[str, str]:
    return {
        "lower": str(interval.lower),
        "upper": str(interval.upper),
        "width": str(interval.width),
    }


def validated_interval_foundation_certificate() -> dict[str, object]:
    """Audit executable consistency of the AU rational interval foundation."""
    pi_coarse = pi_machin_interval(terms=48)
    pi_refined = pi_machin_interval(terms=64)
    atanh_coarse = atanh_fraction_interval(Fraction(1, 5), terms=32)
    atanh_refined = atanh_fraction_interval(Fraction(1, 5), terms=48)
    sine = sin_fraction_interval(Fraction(1, 5), terms=24)
    cosine = cos_fraction_interval(Fraction(1, 5), terms=24)
    pythagorean = sine.power(2) + cosine.power(2)
    root_two = sqrt_fraction_interval(Fraction(2), bisection_steps=160)
    checks = {
        "machin_pi_refinement_is_nested": pi_refined.is_subset_of(pi_coarse),
        "machin_pi_width_is_below_1e_minus_80": (
            pi_refined.width < Fraction(1, 10**80)
        ),
        "atanh_one_fifth_refinement_is_nested": (
            atanh_refined.is_subset_of(atanh_coarse)
        ),
        "atanh_one_fifth_width_is_below_1e_minus_60": (
            atanh_refined.width < Fraction(1, 10**60)
        ),
        "rational_trig_enclosures_contain_pythagorean_identity": (
            pythagorean.contains(1)
        ),
        "sqrt_two_endpoint_bracket_is_ordered_and_nonnegative": (
            root_two.lower >= 0
            and root_two.lower**2 <= 2
            and root_two.upper**2 >= 2
        ),
    }
    return {
        "goal": "Validated Skyrmion Interval Foundation",
        "status": "pass" if all(checks.values()) else "fail",
        "result_type": (
            "analytic_rational_enclosures_with_executable_consistency_checks"
        ),
        "central_result": (
            "Exact Fraction endpoints plus analytically justified series "
            "remainders provide a libm-independent foundation for the future "
            "validated Skyrmion profile certificate checker."
        ),
        "analytic_theorem_results": (
            "Machin's identity plus alternating arctangent remainders encloses pi",
            "Taylor's theorem with globally bounded derivatives encloses sine and cosine",
            "the positive atanh series has the implemented geometric tail bound",
            "exact rational bisection preserves the nonnegative square-root bracket",
        ),
        "executable_checks": checks,
        "pi_interval": _interval_record(pi_refined),
        "atanh_one_fifth_interval": _interval_record(atanh_refined),
        "sqrt_two_interval": _interval_record(root_two),
        "claim_boundary": (
            "The enclosure formulas are analytic results justified by their "
            "documented remainder theorems; the executable checks consistency "
            "and refinement rather than independently reproving those theorems. "
            "The module does not yet validate the singular origin patch, the "
            "nonlinear ODE tube, the shooting bracket, inertia, or the six "
            "derivative norms required for rigorous ULE constants."
        ),
        "next_physics_gate": (
            "check a rational origin patch and piecewise Taylor-defect ODE "
            "certificate for the default hard-wall Skyrmion branch"
        ),
    }
