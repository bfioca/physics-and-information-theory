"""Uniform cellwise quintic validation of the regular Skyrmion origin family.

This combines the degree-two Taylor arithmetic used by the pointwise quintic
origin theorem with the interval-parameter contraction used by the cubic
family theorem. Each slope cell proves a uniform ball

``p=b-3c(b)t-5d(b)t^2+t^3 r_p``, ``|r_p|<=R``,

``u=b-c(b)t-d(b)t^2+t^3 r_u``, ``|r_u|<=R/7``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

from .validated_interval import RationalInterval, pi_machin_interval
from .validated_skyrmion_origin import (
    _abs_upper,
    _assert_uniform_origin_quintic_center_identity,
    _cubic_coefficient_interval,
    _entire_even_kernel_interval,
)


@dataclass(frozen=True)
class _TaylorModelFamilyTwo:
    """Enclose ``c0+c1*t+c2*t^2+t^3*r`` over a parameter cell."""

    constant: RationalInterval
    linear: RationalInterval
    quadratic: RationalInterval
    remainder: RationalInterval
    horizon: Fraction

    def __post_init__(self) -> None:
        for name in ("constant", "linear", "quadratic", "remainder"):
            if not isinstance(getattr(self, name), RationalInterval):
                raise TypeError(f"{name} must be a RationalInterval")
        if not isinstance(self.horizon, Fraction) or self.horizon <= 0:
            raise ValueError("horizon must be a positive Fraction")

    @classmethod
    def point(
        cls,
        value: RationalInterval | int | Fraction,
        horizon: Fraction,
    ) -> _TaylorModelFamilyTwo:
        interval = value if isinstance(value, RationalInterval) else RationalInterval.point(value)
        zero = RationalInterval.point(0)
        return cls(interval, zero, zero, zero, horizon)

    def _coerce(
        self,
        other: _TaylorModelFamilyTwo | RationalInterval | int | Fraction,
    ) -> _TaylorModelFamilyTwo:
        value = other if isinstance(other, _TaylorModelFamilyTwo) else self.point(other, self.horizon)
        if value.horizon != self.horizon:
            raise ValueError("Taylor-model horizons must agree")
        return value

    def __add__(
        self,
        other: _TaylorModelFamilyTwo | RationalInterval | int | Fraction,
    ) -> _TaylorModelFamilyTwo:
        value = self._coerce(other)
        return _TaylorModelFamilyTwo(
            self.constant + value.constant,
            self.linear + value.linear,
            self.quadratic + value.quadratic,
            self.remainder + value.remainder,
            self.horizon,
        )

    def __sub__(
        self,
        other: _TaylorModelFamilyTwo | RationalInterval | int | Fraction,
    ) -> _TaylorModelFamilyTwo:
        return self + self._coerce(other).scale(-1)

    def scale(self, factor: int | Fraction) -> _TaylorModelFamilyTwo:
        scalar = Fraction(factor)
        return _TaylorModelFamilyTwo(
            self.constant.scale(scalar),
            self.linear.scale(scalar),
            self.quadratic.scale(scalar),
            self.remainder.scale(scalar),
            self.horizon,
        )

    def __mul__(
        self,
        other: _TaylorModelFamilyTwo | RationalInterval | int | Fraction,
    ) -> _TaylorModelFamilyTwo:
        value = self._coerce(other)
        time = RationalInterval(Fraction(0), self.horizon)
        time_squared = RationalInterval(Fraction(0), self.horizon**2)
        time_cubed = RationalInterval(Fraction(0), self.horizon**3)
        remainder = (
            self.linear * value.quadratic
            + self.quadratic * value.linear
            + (time * self.quadratic * value.quadratic)
            + value.remainder * self.constant
            + time * value.remainder * self.linear
            + time_squared * value.remainder * self.quadratic
            + self.remainder * value.constant
            + time * self.remainder * value.linear
            + time_squared * self.remainder * value.quadratic
            + time_cubed * self.remainder * value.remainder
        )
        return _TaylorModelFamilyTwo(
            self.constant * value.constant,
            self.constant * value.linear + self.linear * value.constant,
            self.constant * value.quadratic
            + self.linear * value.linear
            + self.quadratic * value.constant,
            remainder,
            self.horizon,
        )

    def power(self, exponent: int) -> _TaylorModelFamilyTwo:
        if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
            raise ValueError("Taylor-model exponent must be nonnegative")
        result = self.point(1, self.horizon)
        factor = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * factor
            factor = factor * factor
            remaining //= 2
        return result

    def range(self) -> RationalInterval:
        time = RationalInterval(Fraction(0), self.horizon)
        return (
            self.constant
            + time * self.linear
            + time.power(2) * self.quadratic
            + time.power(3) * self.remainder
        )

    def reciprocal(self) -> _TaylorModelFamilyTwo:
        value_range = self.range()
        if value_range.contains_zero() or self.constant.contains_zero():
            raise ZeroDivisionError("Taylor-model range contains zero")
        one = RationalInterval.point(1)
        q0 = one / self.constant
        q1 = -self.linear / self.constant.power(2)
        q2 = (
            self.linear.power(2) - self.constant * self.quadratic
        ) / self.constant.power(3)
        time = RationalInterval(Fraction(0), self.horizon)
        numerator_remainder = -(
            self.linear * q2
            + self.quadratic * q1
            + time * self.quadratic * q2
            + self.remainder * q0
            + time * self.remainder * q1
            + time.power(2) * self.remainder * q2
        )
        return _TaylorModelFamilyTwo(
            q0,
            q1,
            q2,
            numerator_remainder / value_range,
            self.horizon,
        )

    def __truediv__(self, other: _TaylorModelFamilyTwo) -> _TaylorModelFamilyTwo:
        return self * other.reciprocal()


def _kernel_model(
    argument: _TaylorModelFamilyTwo,
    *,
    scale_squared: int,
    argument_rate_upper: Fraction,
    terms: int,
) -> _TaylorModelFamilyTwo:
    if terms < 3:
        raise ValueError("quadratic kernel model requires at least three terms")
    total = _TaylorModelFamilyTwo.point(0, argument.horizon)
    power = _TaylorModelFamilyTwo.point(1, argument.horizon)
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
    return _TaylorModelFamilyTwo(
        total.constant,
        total.linear,
        total.quadratic,
        total.remainder + RationalInterval(-tail, tail),
        total.horizon,
    )


def _quintic_coefficient_interval(
    slopes: RationalInterval,
    cubic: RationalInterval,
    mass_squared: Fraction,
    curvature: Fraction,
) -> RationalInterval:
    slope_squared = slopes.power(2)
    numerator = (
        (slopes * cubic.power(2)).scale(192)
        + cubic
        * (
            RationalInterval.point(18 * curvature - mass_squared)
            + slope_squared.scale(184 * curvature - 4)
            + slope_squared.power(2).scale(24)
        )
        - slopes.power(3).scale(mass_squared / 6)
        + slopes.power(5).scale(
            Fraction(32, 3) * curvature - Fraction(4, 15)
        )
        - slopes.power(7).scale(Fraction(32, 15))
    )
    denominator = (RationalInterval.point(1) + slope_squared.scale(8)).scale(28)
    return numerator / denominator


@dataclass(frozen=True)
class ValidatedSkyrmionQuinticFamilyCell:
    shooting_slopes: RationalInterval
    cubic_coefficient: RationalInterval
    quintic_coefficient: RationalInterval
    residual_bound: Fraction
    contraction_bound: Fraction
    volterra_denominator_lower_bound: Fraction
    profile_at_cutoff: RationalInterval
    derivative_at_cutoff: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionQuinticFamily:
    shooting_slopes: RationalInterval
    cutoff: Fraction
    pion_mass_squared: Fraction
    curvature: Fraction
    remainder_radius: Fraction
    cells: tuple[ValidatedSkyrmionQuinticFamilyCell, ...]
    maximum_residual_bound: Fraction
    maximum_contraction_bound: Fraction
    minimum_volterra_denominator: Fraction
    profile_at_cutoff: RationalInterval
    derivative_at_cutoff: RationalInterval


def _validate_cell(
    slopes: RationalInterval,
    *,
    cutoff: Fraction,
    remainder: Fraction,
    mass_squared: Fraction,
    curvature: Fraction,
    kernel_terms: int,
    pi_terms: int,
) -> ValidatedSkyrmionQuinticFamilyCell:
    horizon = cutoff**2
    cubic = _cubic_coefficient_interval(slopes, mass_squared, curvature)
    quintic = _quintic_coefficient_interval(slopes, cubic, mass_squared, curvature)
    zero = RationalInterval.point(0)
    p0 = _TaylorModelFamilyTwo(
        slopes,
        cubic.scale(-3),
        quintic.scale(-5),
        zero,
        horizon,
    )
    u0 = _TaylorModelFamilyTwo(
        slopes,
        cubic.scale(-1),
        quintic.scale(-1),
        zero,
        horizon,
    )
    time = _TaylorModelFamilyTwo(
        zero,
        RationalInterval.point(1),
        zero,
        zero,
        horizon,
    )
    u_abs = _abs_upper(u0.range())
    argument = time * u0.power(2)
    argument_rate = u_abs**2
    sinc = _kernel_model(
        argument,
        scale_squared=1,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    sinc_twice = _kernel_model(
        argument,
        scale_squared=4,
        argument_rate_upper=argument_rate,
        terms=kernel_terms,
    )
    a = u0 * sinc
    lapse = _TaylorModelFamilyTwo.point(1, horizon) - time.scale(curvature)
    denominator = _TaylorModelFamilyTwo.point(1, horizon) + a.power(2).scale(8)
    bracket = (
        _TaylorModelFamilyTwo.point(1, horizon)
        + a.power(2).scale(4)
        + (lapse * p0.power(2)).scale(4)
    )
    source = (u0 * sinc_twice * bracket).scale(2) - (
        time * a
    ).scale(mass_squared)
    integrated = _TaylorModelFamilyTwo(
        source.constant.scale(Fraction(1, 2)),
        source.linear.scale(Fraction(1, 4)),
        source.quadratic.scale(Fraction(1, 6)),
        source.remainder.scale(Fraction(1, 8)),
        horizon,
    )
    image = integrated / (lapse * denominator)
    if not slopes.is_subset_of(image.constant):
        raise ValueError("constant coefficient enclosure failed")
    if not cubic.scale(-3).is_subset_of(image.linear):
        raise ValueError("cubic coefficient enclosure failed")
    if not quintic.scale(-5).is_subset_of(image.quadratic):
        raise ValueError("quintic coefficient enclosure failed")
    residual_bound = _abs_upper(image.remainder)

    remainder_box = RationalInterval(-remainder, remainder)
    p_ball = _TaylorModelFamilyTwo(
        slopes,
        cubic.scale(-3),
        quintic.scale(-5),
        remainder_box,
        horizon,
    ).range()
    u_ball = _TaylorModelFamilyTwo(
        slopes,
        cubic.scale(-1),
        quintic.scale(-1),
        remainder_box.scale(Fraction(1, 7)),
        horizon,
    ).range()
    t_box = RationalInterval(Fraction(0), horizon)
    lapse_box = RationalInterval(1 - curvature * horizon, 1)
    u_abs_ball = _abs_upper(u_ball)
    argument_box = RationalInterval(Fraction(0), horizon * u_abs_ball**2)
    s_box = _entire_even_kernel_interval(
        argument_box, scale_squared=1, derivative_order=0, terms=kernel_terms
    )
    sp_box = _entire_even_kernel_interval(
        argument_box, scale_squared=1, derivative_order=1, terms=kernel_terms
    )
    c_box = _entire_even_kernel_interval(
        argument_box, scale_squared=4, derivative_order=0, terms=kernel_terms
    )
    cp_box = _entire_even_kernel_interval(
        argument_box, scale_squared=4, derivative_order=1, terms=kernel_terms
    )
    a_box = u_ball * s_box
    a_u = s_box + (argument_box * sp_box).scale(2)
    c_u = (t_box * u_ball * cp_box).scale(2)
    e_box = lapse_box * (RationalInterval.point(1) + a_box.power(2).scale(8))
    if e_box.lower <= 0:
        raise ValueError("Volterra denominator is not positive")
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
        (c_box + u_ball * c_u) * h_box + u_ball * c_box * h_u
    ).scale(2) - (t_box * a_u).scale(mass_squared)
    q_p = (lapse_box * u_ball * c_box * p_ball).scale(16)
    e_u = (lapse_box * a_box * a_u).scale(16)
    contraction = (
        (_abs_upper(q_p) + _abs_upper(q_u) / 7) / (8 * e_box.lower)
        + _abs_upper(q_box) * _abs_upper(e_u) / (14 * e_box.lower**2)
    )
    if contraction >= 1:
        raise ValueError("uniform quintic contraction is not below one")
    if residual_bound + contraction * remainder > remainder:
        raise ValueError("uniform quintic radii inequality does not close")

    p_center = (
        slopes
        + cubic.scale(-3 * horizon)
        + quintic.scale(-5 * horizon**2)
    )
    u_center = slopes - cubic.scale(horizon) - quintic.scale(horizon**2)
    p_endpoint = p_center + RationalInterval(
        -remainder * horizon**3, remainder * horizon**3
    )
    u_endpoint = u_center + RationalInterval(
        -remainder * horizon**3 / 7, remainder * horizon**3 / 7
    )
    profile = pi_machin_interval(terms=pi_terms) - u_endpoint.scale(cutoff)
    return ValidatedSkyrmionQuinticFamilyCell(
        shooting_slopes=slopes,
        cubic_coefficient=cubic,
        quintic_coefficient=quintic,
        residual_bound=residual_bound,
        contraction_bound=contraction,
        volterra_denominator_lower_bound=e_box.lower,
        profile_at_cutoff=profile,
        derivative_at_cutoff=-p_endpoint,
    )


def validate_skyrmion_origin_quintic_family(
    shooting_slopes: RationalInterval,
    *,
    cutoff: Fraction = Fraction(1, 16),
    remainder_radius: Fraction = Fraction(13, 10),
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    slope_cells: int = 16,
    kernel_terms: int = 8,
    pi_terms: int = 64,
) -> ValidatedSkyrmionQuinticFamily:
    """Validate one uniform quintic origin family on a slope partition."""
    if not isinstance(shooting_slopes, RationalInterval):
        raise TypeError("shooting_slopes must be a RationalInterval")
    if shooting_slopes.lower <= 0:
        raise ValueError("shooting slopes must be positive")
    if not isinstance(cutoff, Fraction) or cutoff <= 0:
        raise ValueError("cutoff must be a positive Fraction")
    if not isinstance(remainder_radius, Fraction) or remainder_radius <= 0:
        raise ValueError("remainder_radius must be a positive Fraction")
    if isinstance(slope_cells, bool) or not isinstance(slope_cells, int) or slope_cells < 1:
        raise ValueError("slope_cells must be a positive integer")
    if kernel_terms < 3:
        raise ValueError("kernel_terms must be at least three")
    if curvature * cutoff**2 >= 1:
        raise ValueError("origin patch must lie inside the horizon")
    _assert_uniform_origin_quintic_center_identity(pion_mass_squared, curvature)
    width = shooting_slopes.width / slope_cells
    cells = tuple(
        _validate_cell(
            RationalInterval(
                shooting_slopes.lower + index * width,
                shooting_slopes.lower + (index + 1) * width,
            ),
            cutoff=cutoff,
            remainder=remainder_radius,
            mass_squared=pion_mass_squared,
            curvature=curvature,
            kernel_terms=kernel_terms,
            pi_terms=pi_terms,
        )
        for index in range(slope_cells)
    )
    profile = RationalInterval(
        min(cell.profile_at_cutoff.lower for cell in cells),
        max(cell.profile_at_cutoff.upper for cell in cells),
    )
    derivative = RationalInterval(
        min(cell.derivative_at_cutoff.lower for cell in cells),
        max(cell.derivative_at_cutoff.upper for cell in cells),
    )
    return ValidatedSkyrmionQuinticFamily(
        shooting_slopes=shooting_slopes,
        cutoff=cutoff,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        remainder_radius=remainder_radius,
        cells=cells,
        maximum_residual_bound=max(cell.residual_bound for cell in cells),
        maximum_contraction_bound=max(cell.contraction_bound for cell in cells),
        minimum_volterra_denominator=min(
            cell.volterra_denominator_lower_bound for cell in cells
        ),
        profile_at_cutoff=profile,
        derivative_at_cutoff=derivative,
    )
