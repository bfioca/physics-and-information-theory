"""Validated positive-radius derivative norms for the Skyrmion tail theorem.

The six AU.2 norms split into a regular-origin contribution and a
positive-radius contribution.  This module certifies the latter directly from
a closed AU.1 Newton tube.  It reconstructs higher profile derivatives from
the exact ODE with interval Taylor jets, then differentiates the optical
weights with ``D_y=N(x)/sqrt(lambda) D_x``.

The result deliberately does not claim the origin contribution.  A supremum
bound on the Volterra remainder is not a derivative bound, so the interval
``[0,1/16]`` must be certified by a separate origin-regular argument.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction

from .validated_interval import (
    RationalInterval,
    atanh_fraction_interval,
    cos_center_lipschitz_interval,
    pi_machin_interval,
    sin_center_lipschitz_interval,
)
from .validated_skyrmion_bvp import (
    ValidatedSkyrmionNewtonPhysicalObservables,
    _absolute_interval_upper,
    _outward_round_interval,
    _upward_round_fraction,
)
from .validated_skyrmion_spectral_ledger import (
    ValidatedSkyrmionDerivativeNormUpperBound,
    ValidatedSkyrmionSpectralEndpointLedger,
    ValidatedSkyrmionSpectralInput,
    ValidatedSkyrmionSpectralLedger,
    build_validated_skyrmion_spectral_ledger,
    validate_skyrmion_tail_endpoint_data,
)
from .validated_skyrmion_origin_derivatives import (
    ValidatedSkyrmionOriginDerivativeNorms,
    validate_skyrmion_origin_derivative_norms,
)


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _intersection(
    left: RationalInterval,
    right: RationalInterval,
) -> RationalInterval:
    lower = max(left.lower, right.lower)
    upper = min(left.upper, right.upper)
    if lower > upper:
        raise ValueError("independent derivative enclosures do not overlap")
    return RationalInterval(lower, upper)


@dataclass(frozen=True)
class _IntervalJet:
    """Normalized interval Taylor coefficients through a fixed order."""

    coefficients: tuple[RationalInterval, ...]
    rounding_denominator: int

    def __post_init__(self) -> None:
        denominator = _positive_integer(
            "rounding_denominator",
            self.rounding_denominator,
        )
        if not self.coefficients:
            raise ValueError("an interval jet must have at least one coefficient")
        if not all(
            isinstance(value, RationalInterval) for value in self.coefficients
        ):
            raise TypeError("jet coefficients must be RationalInterval values")
        object.__setattr__(
            self,
            "coefficients",
            tuple(
                _outward_round_interval(value, denominator)
                for value in self.coefficients
            ),
        )

    @classmethod
    def point(
        cls,
        value: RationalInterval | int | Fraction,
        order: int,
        rounding_denominator: int,
    ) -> _IntervalJet:
        interval = (
            value
            if isinstance(value, RationalInterval)
            else RationalInterval.point(value)
        )
        return cls(
            (interval,) + (RationalInterval.point(0),) * order,
            rounding_denominator,
        )

    @property
    def order(self) -> int:
        return len(self.coefficients) - 1

    def _check(self, other: _IntervalJet) -> None:
        if self.order != other.order:
            raise ValueError("interval jet orders must agree")
        if self.rounding_denominator != other.rounding_denominator:
            raise ValueError("interval jet rounding grids must agree")

    def _coerce(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return (
            other
            if isinstance(other, _IntervalJet)
            else self.point(other, self.order, self.rounding_denominator)
        )

    def __add__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        value = self._coerce(other)
        self._check(value)
        return _IntervalJet(
            tuple(
                left + right
                for left, right in zip(self.coefficients, value.coefficients)
            ),
            self.rounding_denominator,
        )

    def __radd__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return self + other

    def __neg__(self) -> _IntervalJet:
        return _IntervalJet(
            tuple(-value for value in self.coefficients),
            self.rounding_denominator,
        )

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
        value = self._coerce(other)
        self._check(value)
        coefficients = []
        for degree in range(self.order + 1):
            coefficient = RationalInterval.point(0)
            for index in range(degree + 1):
                coefficient += (
                    self.coefficients[index]
                    * value.coefficients[degree - index]
                )
            coefficients.append(coefficient)
        return _IntervalJet(tuple(coefficients), self.rounding_denominator)

    def __rmul__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return self * other

    def scale(self, factor: int | Fraction) -> _IntervalJet:
        return _IntervalJet(
            tuple(value.scale(factor) for value in self.coefficients),
            self.rounding_denominator,
        )

    def reciprocal(self) -> _IntervalJet:
        if self.coefficients[0].contains_zero():
            raise ZeroDivisionError("interval jet constant contains zero")
        coefficients = [RationalInterval.point(1) / self.coefficients[0]]
        for degree in range(1, self.order + 1):
            numerator = RationalInterval.point(0)
            for index in range(1, degree + 1):
                numerator += self.coefficients[index] * coefficients[degree - index]
            next_coefficient = -numerator / self.coefficients[0]
            coefficients.append(
                _outward_round_interval(
                    next_coefficient,
                    self.rounding_denominator,
                )
            )
        return _IntervalJet(tuple(coefficients), self.rounding_denominator)

    def __truediv__(
        self,
        other: _IntervalJet | RationalInterval | int | Fraction,
    ) -> _IntervalJet:
        return self * self._coerce(other).reciprocal()

    def power(self, exponent: int) -> _IntervalJet:
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

    def derivative(self) -> _IntervalJet:
        if self.order == 0:
            raise ValueError("cannot differentiate a zero-order interval jet")
        return _IntervalJet(
            tuple(
                self.coefficients[index].scale(index)
                for index in range(1, self.order + 1)
            ),
            self.rounding_denominator,
        )

    def truncate(self, order: int) -> _IntervalJet:
        if order < 0 or order > self.order:
            raise ValueError("invalid interval jet truncation order")
        return _IntervalJet(
            self.coefficients[: order + 1],
            self.rounding_denominator,
        )


def _sin_cos_jet(
    value: _IntervalJet,
    *,
    terms: int,
) -> tuple[_IntervalJet, _IntervalJet]:
    sine = [
        _outward_round_interval(
            sin_center_lipschitz_interval(value.coefficients[0], terms=terms),
            value.rounding_denominator,
        )
    ]
    cosine = [
        _outward_round_interval(
            cos_center_lipschitz_interval(value.coefficients[0], terms=terms),
            value.rounding_denominator,
        )
    ]
    for degree in range(1, value.order + 1):
        sine_numerator = RationalInterval.point(0)
        cosine_numerator = RationalInterval.point(0)
        for index in range(degree):
            derivative_coefficient = value.coefficients[index + 1].scale(
                index + 1
            )
            sine_numerator += derivative_coefficient * cosine[degree - 1 - index]
            cosine_numerator -= derivative_coefficient * sine[degree - 1 - index]
        sine.append(
            _outward_round_interval(
                sine_numerator.scale(Fraction(1, degree)),
                value.rounding_denominator,
            )
        )
        cosine.append(
            _outward_round_interval(
                cosine_numerator.scale(Fraction(1, degree)),
                value.rounding_denominator,
            )
        )
    return (
        _IntervalJet(tuple(sine), value.rounding_denominator),
        _IntervalJet(tuple(cosine), value.rounding_denominator),
    )


def _curved_acceleration_jet(
    radius: _IntervalJet,
    profile: _IntervalJet,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
) -> _IntervalJet:
    derivative = profile.derivative()
    radius_for_derivative = radius.truncate(derivative.order)
    profile_for_derivative = profile.truncate(derivative.order)
    radius_squared = radius_for_derivative.power(2)
    lapse = 1 - radius_squared.scale(curvature)
    lapse_derivative = radius_for_derivative.scale(-2 * curvature)
    sine, _ = _sin_cos_jet(
        profile_for_derivative,
        terms=trigonometric_terms,
    )
    sine_twice, _ = _sin_cos_jet(
        profile_for_derivative.scale(2),
        terms=trigonometric_terms,
    )
    sine_squared = sine.power(2)
    profile_factor = radius_squared + sine_squared.scale(8)
    first = (1 + sine_squared.scale(4) / radius_squared) * sine_twice
    mass = sine * radius_squared.scale(pion_mass_squared)
    drift = (
        lapse_derivative * profile_factor + lapse * radius_for_derivative.scale(2)
    ) * derivative
    nonlinear = (lapse * sine_twice * derivative.power(2)).scale(4)
    return (first + mass - drift - nonlinear) / (lapse * profile_factor)


def _curved_flux_terms_jet(
    radius: _IntervalJet,
    profile: _IntervalJet,
    derivative: _IntervalJet,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
) -> tuple[_IntervalJet, _IntervalJet]:
    """Return ``P`` and ``B`` in the conservative equation ``(P F')'=B``."""

    radius._check(profile)
    radius._check(derivative)
    radius_squared = radius.power(2)
    lapse = 1 - radius_squared.scale(curvature)
    sine, _ = _sin_cos_jet(profile, terms=trigonometric_terms)
    sine_twice, _ = _sin_cos_jet(
        profile.scale(2),
        terms=trigonometric_terms,
    )
    sine_squared = sine.power(2)
    principal = lapse * (radius_squared + sine_squared.scale(8))
    forcing = (
        1
        + (lapse * derivative.power(2)).scale(4)
        + (sine_squared / radius_squared).scale(4)
    ) * sine_twice + sine * radius_squared.scale(pion_mass_squared)
    return principal, forcing


def _profile_four_jet(
    radius: RationalInterval,
    profile: RationalInterval,
    derivative: RationalInterval,
    second_derivative: RationalInterval,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    rounding_denominator: int,
) -> tuple[_IntervalJet, _IntervalJet]:
    radius_jet = _IntervalJet(
        (
            radius,
            RationalInterval.point(1),
            RationalInterval.point(0),
            RationalInterval.point(0),
            RationalInterval.point(0),
        ),
        rounding_denominator,
    )
    coefficients: list[RationalInterval] = [
        profile,
        derivative,
        RationalInterval.point(0),
        RationalInterval.point(0),
        RationalInterval.point(0),
    ]

    initial_profile = _IntervalJet(tuple(coefficients), rounding_denominator)
    acceleration = _curved_acceleration_jet(
        radius_jet,
        initial_profile,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    coefficients[2] = _intersection(
        acceleration.coefficients[0].scale(Fraction(1, 2)),
        second_derivative.scale(Fraction(1, 2)),
    )

    profile_two = _IntervalJet(tuple(coefficients[:3]), rounding_denominator)
    derivative_two = _IntervalJet(
        (
            coefficients[1],
            coefficients[2].scale(2),
            RationalInterval.point(0),
        ),
        rounding_denominator,
    )
    principal_two, forcing_two = _curved_flux_terms_jet(
        radius_jet.truncate(2),
        profile_two,
        derivative_two,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    third_derivative = (
        forcing_two.coefficients[1]
        - (
            principal_two.coefficients[1]
            * derivative_two.coefficients[1]
        ).scale(2)
        - (
            principal_two.coefficients[2]
            * derivative_two.coefficients[0]
        ).scale(2)
    ) / principal_two.coefficients[0]
    coefficients[3] = third_derivative.scale(Fraction(1, 6))

    profile_three = _IntervalJet(tuple(coefficients[:4]), rounding_denominator)
    derivative_three = _IntervalJet(
        (
            coefficients[1],
            coefficients[2].scale(2),
            coefficients[3].scale(3),
            RationalInterval.point(0),
        ),
        rounding_denominator,
    )
    principal_three, forcing_three = _curved_flux_terms_jet(
        radius_jet.truncate(3),
        profile_three,
        derivative_three,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    fourth_derivative = (
        forcing_three.coefficients[2]
        - (
            principal_three.coefficients[1]
            * third_derivative
        ).scale(Fraction(3, 2))
        - (
            principal_three.coefficients[2]
            * derivative_three.coefficients[1]
        ).scale(3)
        - (
            principal_three.coefficients[3]
            * derivative_three.coefficients[0]
        ).scale(3)
    ).scale(2) / principal_three.coefficients[0]
    coefficients[4] = fourth_derivative.scale(Fraction(1, 24))
    return radius_jet, _IntervalJet(tuple(coefficients), rounding_denominator)


def _optical_radius_jet(
    radius: _IntervalJet,
    *,
    endpoint: ValidatedSkyrmionSpectralEndpointLedger,
    atanh_terms: int,
) -> _IntervalJet:
    root = endpoint.root_curvature
    argument = root * radius.coefficients[0]
    if argument.lower <= 0 or argument.upper >= 1:
        raise ValueError("positive-radius cell must lie inside the horizon")
    optical_zero = RationalInterval(
        atanh_fraction_interval(argument.lower, terms=atanh_terms).lower,
        atanh_fraction_interval(argument.upper, terms=atanh_terms).upper,
    )
    derivative = (
        _IntervalJet.point(root, radius.order - 1, radius.rounding_denominator)
        / (
            1
            - radius.truncate(radius.order - 1).power(2).scale(
                endpoint.curvature
            )
        )
    )
    coefficients = [optical_zero]
    coefficients.extend(
        derivative.coefficients[index].scale(Fraction(1, index + 1))
        for index in range(radius.order)
    )
    return _IntervalJet(tuple(coefficients), radius.rounding_denominator)


def _dy(value: _IntervalJet, velocity: _IntervalJet) -> _IntervalJet:
    derivative = value.derivative()
    return derivative * velocity.truncate(derivative.order)


def _third_optical_derivative(
    value: _IntervalJet,
    velocity: _IntervalJet,
) -> RationalInterval:
    result = value
    for _ in range(3):
        result = _dy(result, velocity)
    return result.coefficients[0]


@dataclass(frozen=True)
class ValidatedSkyrmionPositiveDerivativeCell:
    """One positive-radius contribution to all six AU.2 norms."""

    source_cell_index: int
    radius: RationalInterval
    optical_radius: RationalInterval
    w_third_derivative_enclosures: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]
    a_third_derivative_enclosures: tuple[
        RationalInterval,
        RationalInterval,
        RationalInterval,
    ]
    w_l1_contribution_upper_bounds: tuple[Fraction, Fraction, Fraction]
    a_l1_contribution_upper_bounds: tuple[Fraction, Fraction, Fraction]


@dataclass(frozen=True)
class ValidatedSkyrmionPositiveDerivativeNorms:
    """Certified ``[a,4]`` pieces of the six AU.2 derivative norms."""

    certificate_id: str
    origin_cutoff: Fraction
    wall_radius: Fraction
    positive_optical_domain: RationalInterval
    optical_wall: RationalInterval
    cells: tuple[ValidatedSkyrmionPositiveDerivativeCell, ...]
    w_positive_l1_upper_bounds: tuple[Fraction, Fraction, Fraction]
    a_positive_l1_upper_bounds: tuple[Fraction, Fraction, Fraction]
    origin_norms_required: bool
    global_norms_certified: bool
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionGlobalDerivativeNorms:
    """Six global AU.2 norms and their evaluated continuum tail ledger."""

    certificate_id: str
    positive_radius: ValidatedSkyrmionPositiveDerivativeNorms
    origin: ValidatedSkyrmionOriginDerivativeNorms
    w_third_derivative_l1_upper_bounds: tuple[Fraction, Fraction, Fraction]
    a_third_derivative_l1_upper_bounds: tuple[Fraction, Fraction, Fraction]
    spectral_ledger: ValidatedSkyrmionSpectralLedger
    global_norms_certified: bool
    conclusion_scope: str


def validate_skyrmion_positive_derivative_norms(
    physical_observables: ValidatedSkyrmionNewtonPhysicalObservables,
    *,
    trigonometric_terms: int = 24,
    atanh_terms: int = 80,
    pi_terms: int = 80,
    rounding_denominator: int = 10**18,
) -> ValidatedSkyrmionPositiveDerivativeNorms:
    """Certify all six derivative-norm contributions away from the origin."""

    if not isinstance(
        physical_observables,
        ValidatedSkyrmionNewtonPhysicalObservables,
    ):
        raise TypeError("physical_observables must be validated AU.1 observables")
    trig_count = _positive_integer("trigonometric_terms", trigonometric_terms)
    atanh_count = _positive_integer("atanh_terms", atanh_terms)
    pi_count = _positive_integer("pi_terms", pi_terms)
    denominator = _positive_integer(
        "rounding_denominator",
        rounding_denominator,
    )
    endpoint = validate_skyrmion_tail_endpoint_data(physical_observables)
    tube = physical_observables.newton_tube
    if not (tube.self_map_verified and tube.contraction_verified):
        raise ValueError("positive derivative norms require a closed Newton tube")
    if tube.origin_cutoff <= 0:
        raise ValueError("positive derivative norms require a positive cutoff")
    if not tube.cells:
        raise ValueError("positive derivative norms require Newton-tube cells")
    if tube.cells[0].radius.lower != tube.origin_cutoff:
        raise ValueError("Newton-tube cells do not begin at the origin cutoff")
    if tube.cells[-1].radius.upper != tube.wall_radius:
        raise ValueError("Newton-tube cells do not reach the wall")
    for cell in tube.cells:
        if cell.radius != cell.tube_jet.radius:
            raise ValueError("Newton-tube cell and jet radii do not agree")
        if cell.radius.lower <= 0:
            raise ValueError("positive derivative cell reaches the origin")
    for left, right in zip(tube.cells, tube.cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("Newton-tube cells must form a contiguous cover")
    pi_interval = pi_machin_interval(terms=pi_count)
    root = endpoint.root_curvature
    factor = pi_interval.scale(Fraction(2, 3)) / root
    checked: list[ValidatedSkyrmionPositiveDerivativeCell] = []
    w_totals = [Fraction(0), Fraction(0), Fraction(0)]
    a_totals = [Fraction(0), Fraction(0), Fraction(0)]
    for cell in tube.cells:
        radius, profile = _profile_four_jet(
            cell.radius,
            cell.tube_jet.profile,
            cell.tube_jet.derivative,
            cell.tube_jet.second_derivative,
            pion_mass_squared=tube.pion_mass_squared,
            curvature=tube.curvature,
            trigonometric_terms=trig_count,
            rounding_denominator=denominator,
        )
        radius_three = radius.truncate(3)
        profile_three = profile.truncate(3)
        derivative = profile.derivative().truncate(3)
        sine, _ = _sin_cos_jet(profile_three, terms=trig_count)
        sine_squared = sine.power(2)
        lapse = 1 - radius_three.power(2).scale(tube.curvature)
        weight = (
            sine_squared
            + (lapse * sine_squared * derivative.power(2)).scale(4)
            + (sine_squared.power(2) / radius_three.power(2)).scale(4)
        ) * factor
        optical = _optical_radius_jet(
            radius_three,
            endpoint=endpoint,
            atanh_terms=atanh_count,
        )
        a_weight = weight / (radius_three * root)
        velocity = lapse / root
        w_enclosures = []
        a_enclosures = []
        w_contributions = []
        a_contributions = []
        optical_width = optical.coefficients[0].width
        for moment in range(3):
            w_third = _third_optical_derivative(
                optical.power(moment) * weight,
                velocity,
            )
            a_third = _third_optical_derivative(
                optical.power(moment) * a_weight,
                velocity,
            )
            w_bound = _upward_round_fraction(
                _absolute_interval_upper(w_third) * optical_width,
                denominator,
            )
            a_bound = _upward_round_fraction(
                _absolute_interval_upper(a_third) * optical_width,
                denominator,
            )
            w_enclosures.append(w_third)
            a_enclosures.append(a_third)
            w_contributions.append(w_bound)
            a_contributions.append(a_bound)
            w_totals[moment] += w_bound
            a_totals[moment] += a_bound
        checked.append(
            ValidatedSkyrmionPositiveDerivativeCell(
                source_cell_index=cell.source_cell_index,
                radius=cell.radius,
                optical_radius=optical.coefficients[0],
                w_third_derivative_enclosures=tuple(w_enclosures),
                a_third_derivative_enclosures=tuple(a_enclosures),
                w_l1_contribution_upper_bounds=tuple(w_contributions),
                a_l1_contribution_upper_bounds=tuple(a_contributions),
            )
        )
    return ValidatedSkyrmionPositiveDerivativeNorms(
        certificate_id=endpoint.certificate_id,
        origin_cutoff=tube.origin_cutoff,
        wall_radius=tube.wall_radius,
        positive_optical_domain=RationalInterval(
            checked[0].optical_radius.lower,
            endpoint.optical_wall.upper,
        ),
        optical_wall=endpoint.optical_wall,
        cells=tuple(checked),
        w_positive_l1_upper_bounds=tuple(w_totals),
        a_positive_l1_upper_bounds=tuple(a_totals),
        origin_norms_required=True,
        global_norms_certified=False,
        conclusion_scope=(
            "exact-rational upper bounds for the six third-optical-derivative "
            "L1 contributions on the positive-radius Newton-tube cells only; "
            "the regular-origin contribution remains required"
        ),
    )


def validate_skyrmion_global_derivative_norms(
    physical_observables: ValidatedSkyrmionNewtonPhysicalObservables,
    *,
    positive_trigonometric_terms: int = 24,
    origin_kernel_terms: int = 20,
    atanh_terms: int = 80,
    pi_terms: int = 80,
    rounding_denominator: int = 10**18,
    tail_start: int | Fraction = 1,
    physical_radius: ValidatedSkyrmionSpectralInput | None = None,
) -> ValidatedSkyrmionGlobalDerivativeNorms:
    """Certify all six global norms and evaluate the AU.2 tail envelope."""

    positive = validate_skyrmion_positive_derivative_norms(
        physical_observables,
        trigonometric_terms=positive_trigonometric_terms,
        atanh_terms=atanh_terms,
        pi_terms=pi_terms,
        rounding_denominator=rounding_denominator,
    )
    origin = validate_skyrmion_origin_derivative_norms(
        physical_observables,
        kernel_terms=origin_kernel_terms,
        atanh_terms=atanh_terms,
        pi_terms=pi_terms,
        rounding_denominator=rounding_denominator,
    )
    if positive.certificate_id != origin.certificate_id:
        raise ValueError("origin and positive-radius certificate ids do not agree")
    if positive.origin_cutoff != origin.origin_cutoff:
        raise ValueError("origin and positive-radius cutoffs do not agree")
    denominator = _positive_integer(
        "rounding_denominator",
        rounding_denominator,
    )
    w_totals = tuple(
        _upward_round_fraction(
            positive.w_positive_l1_upper_bounds[index]
            + origin.w_origin_l1_upper_bounds[index],
            denominator,
        )
        for index in range(3)
    )
    a_totals = tuple(
        _upward_round_fraction(
            positive.a_positive_l1_upper_bounds[index]
            + origin.a_origin_l1_upper_bounds[index],
            denominator,
        )
        for index in range(3)
    )
    provenance = (
        "exact-rational sum of the regular-origin Volterra-Lie bound and "
        "the positive-radius AU.1 Newton-tube interval-jet upper sum"
    )
    w_bounds = tuple(
        ValidatedSkyrmionDerivativeNormUpperBound(
            total,
            provenance,
            positive.certificate_id,
        )
        for total in w_totals
    )
    a_bounds = tuple(
        ValidatedSkyrmionDerivativeNormUpperBound(
            total,
            provenance,
            positive.certificate_id,
        )
        for total in a_totals
    )
    endpoint = validate_skyrmion_tail_endpoint_data(
        physical_observables,
        atanh_terms=atanh_terms,
        pi_terms=pi_terms,
    )
    ledger = build_validated_skyrmion_spectral_ledger(
        endpoint,
        a_third_derivative_l1=a_bounds,
        w_third_derivative_l1=w_bounds,
        tail_start=tail_start,
        physical_radius=physical_radius,
        pi_terms=pi_terms,
    )
    if ledger.tail_envelope is None:
        raise AssertionError("six certified norms did not produce a tail envelope")
    ledger = replace(
        ledger,
        au2_status="validated_global_derivative_norms_and_tail_envelope",
        claim_boundary=(
            "AU.2 certifies all six global third-derivative L1 norms and "
            "their exact continuum tail envelope from one AU.1 solution. "
            "AU.3 finite-frequency quadrature and global Q0, Q1, Q2, G, "
            "and M1 remain open."
        ),
    )
    return ValidatedSkyrmionGlobalDerivativeNorms(
        certificate_id=positive.certificate_id,
        positive_radius=positive,
        origin=origin,
        w_third_derivative_l1_upper_bounds=w_totals,
        a_third_derivative_l1_upper_bounds=a_totals,
        spectral_ledger=ledger,
        global_norms_certified=True,
        conclusion_scope=(
            "exact-rational certification of all six global AU.2 derivative "
            "norms and the boundary-aware p^-5 continuum tail envelope"
        ),
    )
