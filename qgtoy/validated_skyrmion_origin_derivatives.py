"""Validated regular-origin derivative norms for the Skyrmion tail theorem.

The AU.1 origin theorem controls a cubic-centred ``L-infinity`` remainder; it
does not license differentiating that remainder.  This module instead
differentiates the Volterra equation itself.  With ``delta=t*d/dt`` it gives
an analytic vector field in ``(t,u,p)`` whose Lie derivatives recover the
needed spatial derivatives without any derivative assumption on the stored
remainder.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import factorial

from .validated_interval import (
    RationalInterval,
    atanh_fraction_interval,
    pi_machin_interval,
)
from .validated_skyrmion_bvp import (
    ValidatedSkyrmionNewtonPhysicalObservables,
    _absolute_interval_upper,
    _outward_round_interval,
    _upward_round_fraction,
)
from .validated_skyrmion_origin import ValidatedSkyrmionOriginFamily
from .validated_skyrmion_spectral_ledger import (
    ValidatedSkyrmionSpectralEndpointLedger,
    validate_skyrmion_tail_endpoint_data,
)


_VARIABLE_COUNT = 3
_TIME_AXIS = 0
_PROFILE_AXIS = 1
_MOMENTUM_AXIS = 2


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _multiindices(order: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (first, second, total - first - second)
        for total in range(order + 1)
        for first in range(total + 1)
        for second in range(total - first + 1)
    )


class _MultivariateIntervalJet:
    """Normalized total-degree interval jet in ``(t,u,p)``."""

    def __init__(
        self,
        coefficients: dict[tuple[int, int, int], RationalInterval],
        order: int,
        rounding_denominator: int,
    ) -> None:
        if isinstance(order, bool) or not isinstance(order, int) or order < 0:
            raise ValueError("jet order must be a nonnegative integer")
        denominator = _positive_integer(
            "rounding_denominator",
            rounding_denominator,
        )
        indices = _multiindices(order)
        if any(index not in indices for index in coefficients):
            raise ValueError("jet coefficient index exceeds the total order")
        if not all(
            isinstance(value, RationalInterval) for value in coefficients.values()
        ):
            raise TypeError("jet coefficients must be RationalInterval values")
        zero = RationalInterval.point(0)
        self.order = order
        self.rounding_denominator = denominator
        self.coefficients = {
            index: _outward_round_interval(
                coefficients.get(index, zero),
                denominator,
            )
            for index in indices
        }

    @classmethod
    def point(
        cls,
        value: RationalInterval | int | Fraction,
        order: int,
        rounding_denominator: int,
    ) -> _MultivariateIntervalJet:
        interval = (
            value
            if isinstance(value, RationalInterval)
            else RationalInterval.point(value)
        )
        return cls({(0, 0, 0): interval}, order, rounding_denominator)

    @classmethod
    def variable(
        cls,
        value: RationalInterval,
        axis: int,
        order: int,
        rounding_denominator: int,
    ) -> _MultivariateIntervalJet:
        if axis not in range(_VARIABLE_COUNT):
            raise ValueError("jet variable axis is invalid")
        unit = [0, 0, 0]
        unit[axis] = 1
        return cls(
            {
                (0, 0, 0): value,
                tuple(unit): RationalInterval.point(1),
            },
            order,
            rounding_denominator,
        )

    def coefficient(self, index: tuple[int, int, int]) -> RationalInterval:
        return self.coefficients[index]

    def _check(self, other: _MultivariateIntervalJet) -> None:
        if self.order != other.order:
            raise ValueError("multivariate jet orders must agree")
        if self.rounding_denominator != other.rounding_denominator:
            raise ValueError("multivariate jet rounding grids must agree")

    def _coerce(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        return (
            other
            if isinstance(other, _MultivariateIntervalJet)
            else self.point(other, self.order, self.rounding_denominator)
        )

    def __add__(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        value = self._coerce(other)
        self._check(value)
        return _MultivariateIntervalJet(
            {
                index: self.coefficients[index] + value.coefficients[index]
                for index in _multiindices(self.order)
            },
            self.order,
            self.rounding_denominator,
        )

    def __radd__(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        return self + other

    def __neg__(self) -> _MultivariateIntervalJet:
        return self.scale(-1)

    def __sub__(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        return self + (-self._coerce(other))

    def __rsub__(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        return self._coerce(other) - self

    def __mul__(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        value = self._coerce(other)
        self._check(value)
        result: dict[tuple[int, int, int], RationalInterval] = {}
        for alpha in _multiindices(self.order):
            coefficient = RationalInterval.point(0)
            for first in range(alpha[0] + 1):
                for second in range(alpha[1] + 1):
                    for third in range(alpha[2] + 1):
                        beta = (first, second, third)
                        gamma = tuple(
                            alpha[axis] - beta[axis]
                            for axis in range(_VARIABLE_COUNT)
                        )
                        coefficient += (
                            self.coefficients[beta] * value.coefficients[gamma]
                        )
            result[alpha] = coefficient
        return _MultivariateIntervalJet(
            result,
            self.order,
            self.rounding_denominator,
        )

    def __rmul__(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        return self * other

    def scale(self, factor: int | Fraction) -> _MultivariateIntervalJet:
        return _MultivariateIntervalJet(
            {
                index: value.scale(factor)
                for index, value in self.coefficients.items()
            },
            self.order,
            self.rounding_denominator,
        )

    def reciprocal(self) -> _MultivariateIntervalJet:
        constant = self.coefficients[(0, 0, 0)]
        if constant.contains_zero():
            raise ZeroDivisionError("multivariate jet constant contains zero")
        result = {(0, 0, 0): RationalInterval.point(1) / constant}
        for alpha in _multiindices(self.order)[1:]:
            numerator = RationalInterval.point(0)
            for first in range(alpha[0] + 1):
                for second in range(alpha[1] + 1):
                    for third in range(alpha[2] + 1):
                        beta = (first, second, third)
                        if beta == (0, 0, 0):
                            continue
                        gamma = tuple(
                            alpha[axis] - beta[axis]
                            for axis in range(_VARIABLE_COUNT)
                        )
                        numerator += self.coefficients[beta] * result[gamma]
            result[alpha] = -numerator / constant
        return _MultivariateIntervalJet(
            result,
            self.order,
            self.rounding_denominator,
        )

    def __truediv__(
        self,
        other: _MultivariateIntervalJet | RationalInterval | int | Fraction,
    ) -> _MultivariateIntervalJet:
        return self * self._coerce(other).reciprocal()

    def power(self, exponent: int) -> _MultivariateIntervalJet:
        if isinstance(exponent, bool) or not isinstance(exponent, int):
            raise TypeError("jet exponent must be an integer")
        if exponent < 0:
            return self.power(-exponent).reciprocal()
        result = self.point(1, self.order, self.rounding_denominator)
        factor = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * factor
            factor = factor * factor
            remaining //= 2
        return result

    def derivative(self, axis: int) -> _MultivariateIntervalJet:
        if self.order == 0:
            raise ValueError("cannot differentiate a zero-order jet")
        if axis not in range(_VARIABLE_COUNT):
            raise ValueError("jet derivative axis is invalid")
        result = {}
        for alpha in _multiindices(self.order - 1):
            source = list(alpha)
            source[axis] += 1
            result[alpha] = self.coefficients[tuple(source)].scale(
                alpha[axis] + 1
            )
        return _MultivariateIntervalJet(
            result,
            self.order - 1,
            self.rounding_denominator,
        )

    def truncate(self, order: int) -> _MultivariateIntervalJet:
        if order < 0 or order > self.order:
            raise ValueError("invalid multivariate jet truncation order")
        return _MultivariateIntervalJet(
            {
                index: self.coefficients[index]
                for index in _multiindices(order)
            },
            order,
            self.rounding_denominator,
        )

    def with_constant(
        self,
        value: RationalInterval,
    ) -> _MultivariateIntervalJet:
        coefficients = dict(self.coefficients)
        coefficients[(0, 0, 0)] = value
        return _MultivariateIntervalJet(
            coefficients,
            self.order,
            self.rounding_denominator,
        )


def _entire_even_kernel_derivative_interval(
    argument: RationalInterval,
    *,
    scale_squared: int,
    derivative_order: int,
    terms: int,
) -> RationalInterval:
    """Enclose a derivative of ``sinc(scale*sqrt(w))`` for ``w>=0``."""

    if argument.lower < 0:
        raise ValueError("even-kernel argument must be nonnegative")
    if derivative_order < 0 or terms <= derivative_order:
        raise ValueError("too few terms for the kernel derivative")
    total = RationalInterval.point(0)
    for index in range(derivative_order, terms):
        falling = 1
        for offset in range(derivative_order):
            falling *= index - offset
        coefficient = Fraction(
            (-1) ** index * scale_squared**index * falling,
            factorial(2 * index + 1),
        )
        total += argument.power(index - derivative_order).scale(coefficient)
    falling = 1
    for offset in range(derivative_order):
        falling *= terms - offset
    first = (
        Fraction(scale_squared**terms * falling, factorial(2 * terms + 1))
        * argument.upper ** (terms - derivative_order)
    )
    ratio = (
        Fraction(scale_squared)
        * argument.upper
        * Fraction(terms + 1, terms + 1 - derivative_order)
        / ((2 * terms + 2) * (2 * terms + 3))
    )
    if ratio >= 1:
        raise ValueError("kernel derivative geometric-tail ratio must be below one")
    tail = first / (1 - ratio)
    return total + RationalInterval(-tail, tail)


def _compose_even_kernel(
    argument: _MultivariateIntervalJet,
    *,
    scale_squared: int,
    base_derivative_order: int,
    terms: int,
) -> _MultivariateIntervalJet:
    argument_box = argument.coefficient((0, 0, 0))
    derivatives = tuple(
        _entire_even_kernel_derivative_interval(
            argument_box,
            scale_squared=scale_squared,
            derivative_order=base_derivative_order + order,
            terms=terms,
        )
        for order in range(argument.order + 1)
    )
    result = argument.point(
        derivatives[0],
        argument.order,
        argument.rounding_denominator,
    )
    delta = argument.with_constant(RationalInterval.point(0))
    power = argument.point(1, argument.order, argument.rounding_denominator)
    for order in range(1, argument.order + 1):
        power = power * delta
        result += power * derivatives[order].scale(Fraction(1, factorial(order)))
    return result


def _origin_variables(
    time_box: RationalInterval,
    profile_box: RationalInterval,
    momentum_box: RationalInterval,
    *,
    order: int,
    rounding_denominator: int,
) -> tuple[
    _MultivariateIntervalJet,
    _MultivariateIntervalJet,
    _MultivariateIntervalJet,
]:
    return (
        _MultivariateIntervalJet.variable(
            time_box,
            _TIME_AXIS,
            order,
            rounding_denominator,
        ),
        _MultivariateIntervalJet.variable(
            profile_box,
            _PROFILE_AXIS,
            order,
            rounding_denominator,
        ),
        _MultivariateIntervalJet.variable(
            momentum_box,
            _MOMENTUM_AXIS,
            order,
            rounding_denominator,
        ),
    )


def _origin_weight_jet(
    time: _MultivariateIntervalJet,
    profile: _MultivariateIntervalJet,
    momentum: _MultivariateIntervalJet,
    *,
    curvature: Fraction,
    kernel_terms: int,
) -> _MultivariateIntervalJet:
    argument = time * profile.power(2)
    sinc = _compose_even_kernel(
        argument,
        scale_squared=1,
        base_derivative_order=0,
        terms=kernel_terms,
    )
    sine_over_radius = profile * sinc
    lapse = 1 - time.scale(curvature)
    return (
        sine_over_radius.power(2)
        * (1 + (lapse * momentum.power(2)).scale(4))
        + sine_over_radius.power(4).scale(4)
    )


def _origin_vector_field(
    time: _MultivariateIntervalJet,
    profile: _MultivariateIntervalJet,
    momentum: _MultivariateIntervalJet,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    kernel_terms: int,
) -> tuple[
    tuple[
        _MultivariateIntervalJet,
        _MultivariateIntervalJet,
        _MultivariateIntervalJet,
    ],
    RationalInterval,
]:
    argument = time * profile.power(2)
    sinc = _compose_even_kernel(
        argument,
        scale_squared=1,
        base_derivative_order=0,
        terms=kernel_terms,
    )
    sinc_prime = _compose_even_kernel(
        argument,
        scale_squared=1,
        base_derivative_order=1,
        terms=kernel_terms,
    )
    sinc_twice = _compose_even_kernel(
        argument,
        scale_squared=4,
        base_derivative_order=0,
        terms=kernel_terms,
    )
    sine_over_radius = profile * sinc
    lapse = 1 - time.scale(curvature)
    denominator_factor = 1 + sine_over_radius.power(2).scale(8)
    denominator = lapse * denominator_factor
    delta_profile = (momentum - profile).scale(Fraction(1, 2))
    delta_argument = time * profile * momentum
    delta_sine_over_radius = (
        delta_profile * sinc
        + profile * sinc_prime * delta_argument
    )
    delta_denominator = (
        time.scale(-curvature) * denominator_factor
        + (
            lapse * sine_over_radius * delta_sine_over_radius
        ).scale(16)
    )
    bracket = (
        1
        + sine_over_radius.power(2).scale(4)
        + (lapse * momentum.power(2)).scale(4)
    )
    source = (profile * sinc_twice * bracket).scale(2) - (
        time * sine_over_radius
    ).scale(pion_mass_squared)
    delta_momentum = (
        source.scale(Fraction(1, 2))
        - denominator * momentum
        - delta_denominator * momentum
    ) / denominator
    return (
        (time, delta_profile, delta_momentum),
        denominator.coefficient((0, 0, 0)),
    )


def _lie_derivative(
    value: _MultivariateIntervalJet,
    vector_field: tuple[
        _MultivariateIntervalJet,
        _MultivariateIntervalJet,
        _MultivariateIntervalJet,
    ],
) -> _MultivariateIntervalJet:
    if value.order == 0:
        raise ValueError("Lie derivative requires a positive-order jet")
    target_order = value.order - 1
    result = _MultivariateIntervalJet.point(
        0,
        target_order,
        value.rounding_denominator,
    )
    for axis in range(_VARIABLE_COUNT):
        result += (
            vector_field[axis].truncate(target_order)
            * value.derivative(axis)
        )
    return result


def _absolute_gradient_upper_bounds(
    value: _MultivariateIntervalJet,
) -> tuple[Fraction, Fraction, Fraction]:
    result = []
    for axis in range(_VARIABLE_COUNT):
        unit = [0, 0, 0]
        unit[axis] = 1
        result.append(_absolute_interval_upper(value.coefficient(tuple(unit))))
    return tuple(result)


@dataclass(frozen=True)
class ValidatedSkyrmionOriginDerivativeNorms:
    """Certified origin pieces of the six AU.2 derivative norms."""

    certificate_id: str
    origin_cutoff: Fraction
    optical_cutoff_upper_bound: Fraction
    time_box: RationalInterval
    profile_box: RationalInterval
    momentum_box: RationalInterval
    volterra_denominator_enclosure: RationalInterval
    weight_factor_absolute_upper_bound: Fraction
    lie_derivative_over_time_upper_bounds: tuple[Fraction, Fraction, Fraction]
    w_optical_derivative_upper_bounds: tuple[Fraction, Fraction, Fraction]
    a_optical_derivative_upper_bounds: tuple[Fraction, Fraction, Fraction]
    w_origin_l1_upper_bounds: tuple[Fraction, Fraction, Fraction]
    a_origin_l1_upper_bounds: tuple[Fraction, Fraction, Fraction]
    conclusion_scope: str


def _optical_derivative_upper_bounds(
    spatial_derivatives: tuple[Fraction, Fraction, Fraction],
    *,
    scale: Fraction,
    curvature: Fraction,
    root_curvature_lower: Fraction,
    cutoff: Fraction,
    rounding_denominator: int,
) -> tuple[Fraction, Fraction, Fraction]:
    first, second, third = spatial_derivatives
    lapse_derivative = 2 * curvature * cutoff
    lapse_second_derivative = 2 * curvature
    optical_first = scale * first / root_curvature_lower
    optical_second = scale * (
        second + lapse_derivative * first
    ) / curvature
    optical_third = scale * (
        third
        + 3 * lapse_derivative * second
        + (lapse_derivative**2 + lapse_second_derivative) * first
    ) / (curvature * root_curvature_lower)
    return tuple(
        _upward_round_fraction(value, rounding_denominator)
        for value in (optical_first, optical_second, optical_third)
    )


def _origin_moment_l1_bounds(
    optical_derivatives: tuple[Fraction, Fraction, Fraction],
    *,
    optical_cutoff: Fraction,
    rounding_denominator: int,
) -> tuple[Fraction, Fraction, Fraction]:
    first, second, third = optical_derivatives
    bounds = (
        optical_cutoff * third,
        optical_cutoff**2 * third / 2 + 3 * optical_cutoff * second,
        optical_cutoff**3 * third / 3
        + 3 * optical_cutoff**2 * second
        + 6 * optical_cutoff * first,
    )
    return tuple(
        _upward_round_fraction(value, rounding_denominator) for value in bounds
    )


def validate_skyrmion_origin_derivative_norms(
    physical_observables: ValidatedSkyrmionNewtonPhysicalObservables,
    *,
    kernel_terms: int = 20,
    atanh_terms: int = 80,
    pi_terms: int = 80,
    rounding_denominator: int = 10**18,
) -> ValidatedSkyrmionOriginDerivativeNorms:
    """Certify the six AU.2 derivative-norm contributions at the origin."""

    if not isinstance(
        physical_observables,
        ValidatedSkyrmionNewtonPhysicalObservables,
    ):
        raise TypeError("physical_observables must be validated AU.1 observables")
    kernel_count = _positive_integer("kernel_terms", kernel_terms)
    if kernel_count <= 4:
        raise ValueError("kernel_terms must exceed the AD derivative order")
    atanh_count = _positive_integer("atanh_terms", atanh_terms)
    pi_count = _positive_integer("pi_terms", pi_terms)
    denominator_grid = _positive_integer(
        "rounding_denominator",
        rounding_denominator,
    )
    endpoint: ValidatedSkyrmionSpectralEndpointLedger = (
        validate_skyrmion_tail_endpoint_data(
            physical_observables,
            atanh_terms=atanh_count,
            pi_terms=pi_count,
        )
    )
    origin = physical_observables.origin_family
    tube = physical_observables.newton_tube
    if not isinstance(origin, ValidatedSkyrmionOriginFamily):
        raise TypeError("physical observables do not contain an origin family")
    if origin.shooting_slopes != tube.shooting_slope_interval:
        raise ValueError("origin family does not match the Newton slope tube")
    if origin.cutoff != tube.origin_cutoff:
        raise ValueError("origin family cutoff does not match the Newton tube")
    if (
        origin.pion_mass_squared != tube.pion_mass_squared
        or origin.curvature != tube.curvature
        or origin.remainder_radius != tube.origin_remainder_radius
    ):
        raise ValueError("origin family provenance does not match the Newton tube")

    horizon = origin.cutoff**2
    time_box = RationalInterval(Fraction(0), horizon)
    remainder_box = RationalInterval(
        -origin.remainder_radius,
        origin.remainder_radius,
    )
    profile_box = (
        origin.shooting_slopes
        - time_box * origin.cubic_coefficient
        + time_box.power(2) * remainder_box.scale(Fraction(1, 5))
    )
    momentum_box = (
        origin.shooting_slopes
        - (time_box * origin.cubic_coefficient).scale(3)
        + time_box.power(2) * remainder_box
    )
    variables_four = _origin_variables(
        time_box,
        profile_box,
        momentum_box,
        order=4,
        rounding_denominator=denominator_grid,
    )
    weight = _origin_weight_jet(
        *variables_four,
        curvature=origin.curvature,
        kernel_terms=kernel_count,
    )
    variables_three = tuple(value.truncate(3) for value in variables_four)
    vector_field, volterra_denominator = _origin_vector_field(
        *variables_three,
        pion_mass_squared=origin.pion_mass_squared,
        curvature=origin.curvature,
        kernel_terms=kernel_count,
    )
    if volterra_denominator.lower <= 0:
        raise ValueError("origin Volterra denominator enclosure is not positive")
    first_lie = _lie_derivative(weight, vector_field)
    second_lie = _lie_derivative(first_lie, vector_field)
    third_lie = _lie_derivative(second_lie, vector_field)

    cubic_absolute = _absolute_interval_upper(origin.cubic_coefficient)
    profile_rate = cubic_absolute + origin.remainder_radius * horizon / 5
    momentum_rate = 3 * cubic_absolute + origin.remainder_radius * horizon
    lie_over_time = []
    for lie_derivative in (first_lie, second_lie, third_lie):
        gradient = _absolute_gradient_upper_bounds(lie_derivative)
        lie_over_time.append(
            _upward_round_fraction(
                gradient[_TIME_AXIS]
                + profile_rate * gradient[_PROFILE_AXIS]
                + momentum_rate * gradient[_MOMENTUM_AXIS],
                denominator_grid,
            )
        )
    first_rate, second_rate, third_rate = lie_over_time
    weight_upper = _absolute_interval_upper(weight.coefficient((0, 0, 0)))

    w_spatial = (
        origin.cutoff * (2 * weight_upper + 2 * horizon * first_rate),
        2 * weight_upper
        + 6 * horizon * first_rate
        + 4 * horizon * second_rate,
        origin.cutoff * (
            4 * first_rate + 12 * second_rate + 8 * third_rate
        ),
    )
    a_spatial = (
        weight_upper + 2 * horizon * first_rate,
        origin.cutoff * (2 * first_rate + 4 * second_rate),
        2 * first_rate + 8 * third_rate,
    )
    pi_interval = pi_machin_interval(terms=pi_count)
    root_lower = endpoint.root_curvature.lower
    w_scale = pi_interval.upper * 2 / (3 * root_lower)
    a_scale = pi_interval.upper * 2 / (3 * origin.curvature)
    w_optical = _optical_derivative_upper_bounds(
        w_spatial,
        scale=w_scale,
        curvature=origin.curvature,
        root_curvature_lower=root_lower,
        cutoff=origin.cutoff,
        rounding_denominator=denominator_grid,
    )
    a_optical = _optical_derivative_upper_bounds(
        a_spatial,
        scale=a_scale,
        curvature=origin.curvature,
        root_curvature_lower=root_lower,
        cutoff=origin.cutoff,
        rounding_denominator=denominator_grid,
    )
    optical_argument = endpoint.root_curvature.upper * origin.cutoff
    optical_cutoff = _upward_round_fraction(
        atanh_fraction_interval(
            optical_argument,
            terms=atanh_count,
        ).upper,
        denominator_grid,
    )
    w_l1 = _origin_moment_l1_bounds(
        w_optical,
        optical_cutoff=optical_cutoff,
        rounding_denominator=denominator_grid,
    )
    a_l1 = _origin_moment_l1_bounds(
        a_optical,
        optical_cutoff=optical_cutoff,
        rounding_denominator=denominator_grid,
    )
    return ValidatedSkyrmionOriginDerivativeNorms(
        certificate_id=endpoint.certificate_id,
        origin_cutoff=origin.cutoff,
        optical_cutoff_upper_bound=optical_cutoff,
        time_box=time_box,
        profile_box=profile_box,
        momentum_box=momentum_box,
        volterra_denominator_enclosure=volterra_denominator,
        weight_factor_absolute_upper_bound=weight_upper,
        lie_derivative_over_time_upper_bounds=tuple(lie_over_time),
        w_optical_derivative_upper_bounds=w_optical,
        a_optical_derivative_upper_bounds=a_optical,
        w_origin_l1_upper_bounds=w_l1,
        a_origin_l1_upper_bounds=a_l1,
        conclusion_scope=(
            "exact-rational regular-origin bounds for the six third-optical-"
            "derivative L1 contributions, derived from the AU.1 Volterra "
            "identity without differentiating its L-infinity remainder"
        ),
    )
