"""Cancellation-safe origin residual for the centrifugal weak response.

Set ``t=x^2``, ``g=x v(t)``, and ``f=x[-v(t)+t u(t)]``.  With regular
conormal blocks

``C=Cbar``, ``M=x Mbar``, ``P=t Pbar``, ``s0=x shat0``, ``s1=t shat1``,

the physical strong residual factorizes as ``r(x)=x rhat(t)``.  This module
ranges ``rhat`` directly and uses

``integral_0^x0 |r|^2 dx <= x0^3 sup|rhat|^2/3``.

No reciprocal of an interval containing the origin is formed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TypeAlias

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
    regular_rotational_source_from_kernels,
)
from .validated_centrifugal_response_residual import (
    IntervalMatrix2,
    IntervalVector2,
    ValidatedResidualNorm,
    ValidatedStrongResidualCell,
    certify_energy_dual_residual_upper,
)
from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    sqrt_fraction_interval,
)


MatrixJet2: TypeAlias = tuple[
    tuple["_IntervalTimeJet", "_IntervalTimeJet"],
    tuple["_IntervalTimeJet", "_IntervalTimeJet"],
]


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


@dataclass(frozen=True)
class _IntervalTimeJet:
    value: RationalInterval
    derivative: RationalInterval

    @classmethod
    def constant(
        cls, value: RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        interval = (
            value if isinstance(value, RationalInterval) else RationalInterval.point(value)
        )
        return cls(interval, RationalInterval.point(0))

    def _coerce(
        self, other: _IntervalTimeJet | RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        return other if isinstance(other, _IntervalTimeJet) else self.constant(other)

    def __add__(
        self, other: _IntervalTimeJet | RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        right = self._coerce(other)
        return _IntervalTimeJet(
            self.value + right.value, self.derivative + right.derivative
        )

    __radd__ = __add__

    def __neg__(self) -> _IntervalTimeJet:
        return _IntervalTimeJet(-self.value, -self.derivative)

    def __sub__(
        self, other: _IntervalTimeJet | RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        return self + (-self._coerce(other))

    def __rsub__(
        self, other: _IntervalTimeJet | RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        return self._coerce(other) - self

    def __mul__(
        self, other: _IntervalTimeJet | RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        right = self._coerce(other)
        return _IntervalTimeJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(
        self, other: _IntervalTimeJet | RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        right = self._coerce(other)
        return _IntervalTimeJet(
            self.value / right.value,
            (
                self.derivative * right.value
                - self.value * right.derivative
            )
            / right.value.power(2),
        )

    def __rtruediv__(
        self, other: _IntervalTimeJet | RationalInterval | int | Fraction
    ) -> _IntervalTimeJet:
        return self._coerce(other) / self


@dataclass(frozen=True)
class ValidatedOriginProfileKernelCell:
    """Regular profile-kernel boxes and their ``t`` derivatives."""

    time: RationalInterval
    metric_factor: RationalInterval
    metric_factor_time_derivative: RationalInterval
    profile_deficit_radial_derivative: RationalInterval
    profile_deficit_radial_derivative_time_derivative: RationalInterval
    sine_over_radius: RationalInterval
    sine_over_radius_time_derivative: RationalInterval
    cosine_of_profile_deficit: RationalInterval
    cosine_of_profile_deficit_time_derivative: RationalInterval

    def __post_init__(self) -> None:
        if self.time.lower != 0 or self.time.upper <= 0:
            raise ValueError("origin time cell must be [0,h] with h>0")
        if self.metric_factor.lower <= 0:
            raise ValueError("metric factor must remain positive")


@dataclass(frozen=True)
class ValidatedOriginConormalCell:
    time: RationalInterval
    coordinate: IntervalMatrix2
    coordinate_time_derivative: IntervalMatrix2
    mixed: IntervalMatrix2
    mixed_time_derivative: IntervalMatrix2
    principal: IntervalMatrix2
    principal_time_derivative: IntervalMatrix2
    coordinate_source_hat: IntervalVector2
    coordinate_source_hat_time_derivative: IntervalVector2
    derivative_source_hat: IntervalVector2
    derivative_source_hat_time_derivative: IntervalVector2


def _matrix_value(matrix: MatrixJet2) -> IntervalMatrix2:
    return tuple(tuple(entry.value for entry in row) for row in matrix)  # type: ignore[return-value]


def _matrix_derivative(matrix: MatrixJet2) -> IntervalMatrix2:
    return tuple(
        tuple(entry.derivative for entry in row) for row in matrix
    )  # type: ignore[return-value]


def validated_origin_conormal_cell_from_profile(
    profile: ValidatedOriginProfileKernelCell,
    *,
    pion_mass_squared: Fraction = Fraction(1),
) -> ValidatedOriginConormalCell:
    """Propagate regular profile boxes through the conormal coefficient map."""
    if pion_mass_squared < 0:
        raise ValueError("pion_mass_squared must be nonnegative")
    time = _IntervalTimeJet(profile.time, RationalInterval.point(1))
    metric = _IntervalTimeJet(
        profile.metric_factor, profile.metric_factor_time_derivative
    )
    rho = _IntervalTimeJet(
        profile.profile_deficit_radial_derivative,
        profile.profile_deficit_radial_derivative_time_derivative,
    )
    sine = _IntervalTimeJet(
        profile.sine_over_radius, profile.sine_over_radius_time_derivative
    )
    cosine = _IntervalTimeJet(
        profile.cosine_of_profile_deficit,
        profile.cosine_of_profile_deficit_time_derivative,
    )
    blocks = regular_conormal_blocks_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine,
        cosine_of_profile_deficit=cosine,
        pion_mass_squared=_IntervalTimeJet.constant(pion_mass_squared),
    )
    source = regular_rotational_source_from_kernels(
        t=time,
        metric_factor=metric,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine,
        cosine_of_profile_deficit=cosine,
    )
    coordinate = blocks["coordinate"]
    mixed = blocks["mixed"]
    principal = blocks["principal"]
    source_zero = source["coordinate_source"]
    source_one = source["derivative_source"]
    return ValidatedOriginConormalCell(
        time=profile.time,
        coordinate=_matrix_value(coordinate),
        coordinate_time_derivative=_matrix_derivative(coordinate),
        mixed=_matrix_value(mixed),
        mixed_time_derivative=_matrix_derivative(mixed),
        principal=_matrix_value(principal),
        principal_time_derivative=_matrix_derivative(principal),
        coordinate_source_hat=tuple(entry.value for entry in source_zero),  # type: ignore[arg-type]
        coordinate_source_hat_time_derivative=tuple(
            entry.derivative for entry in source_zero
        ),  # type: ignore[arg-type]
        derivative_source_hat=tuple(entry.value for entry in source_one),  # type: ignore[arg-type]
        derivative_source_hat_time_derivative=tuple(
            entry.derivative for entry in source_one
        ),  # type: ignore[arg-type]
    )


@dataclass(frozen=True)
class RationalOriginTrialCell:
    """Exact regular fields ``u(t),v(t)`` in normalized time ``tau=t/h``."""

    time_horizon: Fraction
    u: RationalPolynomial
    v: RationalPolynomial

    def __post_init__(self) -> None:
        if self.time_horizon <= 0:
            raise ValueError("time_horizon must be positive")

    def jet_range(
        self,
    ) -> tuple[IntervalVector2, IntervalVector2, IntervalVector2]:
        unit = RationalInterval(Fraction(0), Fraction(1))
        fields = (self.u, self.v)
        value = tuple(field.evaluate(unit) for field in fields)
        derivative = tuple(
            field.derivative().evaluate(unit).scale(1 / self.time_horizon)
            for field in fields
        )
        second = tuple(
            field.derivative()
            .derivative()
            .evaluate(unit)
            .scale(1 / self.time_horizon**2)
            for field in fields
        )
        return value, derivative, second  # type: ignore[return-value]

    def physical_endpoint_jet(
        self,
    ) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
        """Return ``(f,g)`` and ``(f',g')`` at ``x=sqrt(h)`` if rational."""
        root = sqrt_fraction_interval(self.time_horizon).lower
        if root * root != self.time_horizon:
            raise ValueError("time_horizon must be a rational square")
        argument = Fraction(1)
        u = self.u.evaluate(argument).lower
        v = self.v.evaluate(argument).lower
        u_t = self.u.derivative().evaluate(argument).lower / self.time_horizon
        v_t = self.v.derivative().evaluate(argument).lower / self.time_horizon
        t = self.time_horizon
        a = -v + t * u
        f_p = -v + 3 * t * u - 2 * t * v_t + 2 * t**2 * u_t
        g_p = v + 2 * t * v_t
        return (root * a, root * v), (f_p, g_p)


def _matrix_vector(
    matrix: IntervalMatrix2, vector: IntervalVector2
) -> IntervalVector2:
    return tuple(
        row[0] * vector[0] + row[1] * vector[1] for row in matrix
    )  # type: ignore[return-value]


def _transpose(matrix: IntervalMatrix2) -> IntervalMatrix2:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


@dataclass(frozen=True)
class ValidatedOriginStrongResidual:
    time: RationalInterval
    radius_cutoff: Fraction
    residual_hat: IntervalVector2
    l2_squared_upper: Fraction


def validated_origin_strong_residual_cell(
    coefficients: ValidatedOriginConormalCell,
    trial: RationalOriginTrialCell,
) -> ValidatedOriginStrongResidual:
    """Range ``r/x`` and integrate its exact origin weight."""
    horizon = trial.time_horizon
    if coefficients.time != RationalInterval(Fraction(0), horizon):
        raise ValueError("coefficient and trial time cells do not agree")
    root = sqrt_fraction_interval(horizon).lower
    if root * root != horizon:
        raise ValueError("time_horizon must be a rational square")
    (u, v), (u_t, v_t), (u_tt, v_tt) = trial.jet_range()
    t = coefficients.time
    a = (-v + t * u, v)
    a_t = (-v_t + u + t * u_t, v_t)
    d = (
        -v + t * u * 3 - t * v_t * 2 + t.power(2) * u_t * 2,
        v + t * v_t * 2,
    )
    d_t = (
        u * 3
        - v_t * 3
        + t * u_t * 7
        - t * v_tt * 2
        + t.power(2) * u_tt * 2,
        v_t * 3 + t * v_tt * 2,
    )
    mixed_t = _transpose(coefficients.mixed)
    mixed_derivative_t = _transpose(coefficients.mixed_time_derivative)
    z = tuple(
        principal + mixed - source
        for principal, mixed, source in zip(
            _matrix_vector(coefficients.principal, d),
            _matrix_vector(mixed_t, a),
            coefficients.derivative_source_hat,
            strict=True,
        )
    )
    z_t = tuple(
        principal_t_d
        + principal_d_t
        + mixed_t_a
        + mixed_a_t
        - source_t
        for principal_t_d, principal_d_t, mixed_t_a, mixed_a_t, source_t in zip(
            _matrix_vector(coefficients.principal_time_derivative, d),
            _matrix_vector(coefficients.principal, d_t),
            _matrix_vector(mixed_derivative_t, a),
            _matrix_vector(mixed_t, a_t),
            coefficients.derivative_source_hat_time_derivative,
            strict=True,
        )
    )
    residual_hat = tuple(
        source - coordinate - mixed + (z_value + t * z_derivative) * 2
        for source, coordinate, mixed, z_value, z_derivative in zip(
            coefficients.coordinate_source_hat,
            _matrix_vector(coefficients.coordinate, a),
            _matrix_vector(coefficients.mixed, d),
            z,
            z_t,
            strict=True,
        )
    )
    weight_integral = horizon * root / 3
    square_upper = weight_integral * sum(
        _absolute_upper(entry) ** 2 for entry in residual_hat
    )
    return ValidatedOriginStrongResidual(
        time=coefficients.time,
        radius_cutoff=root,
        residual_hat=residual_hat,  # type: ignore[arg-type]
        l2_squared_upper=square_upper,
    )


def certify_full_domain_energy_dual_residual_upper(
    origin: ValidatedOriginStrongResidual,
    positive_radius_cells: tuple[ValidatedStrongResidualCell, ...],
    *,
    wall_radius: Fraction,
    interface_distribution_free: bool,
    operator_lower_bound: Fraction,
    wall_trace_margin_lower_bound: Fraction,
    wall_residual: RationalInterval = RationalInterval.point(0),
) -> ValidatedResidualNorm:
    """Join the origin weight bound to contiguous positive-radius residuals."""
    if not positive_radius_cells:
        raise ValueError("positive-radius residual cells are required")
    if positive_radius_cells[0].radius.lower != origin.radius_cutoff:
        raise ValueError("origin and positive-radius residuals do not meet")
    synthetic_origin = ValidatedStrongResidualCell(
        radius=RationalInterval(Fraction(0), origin.radius_cutoff),
        residual=(RationalInterval.point(0), RationalInterval.point(0)),
        l2_squared_upper=origin.l2_squared_upper,
    )
    return certify_energy_dual_residual_upper(
        (synthetic_origin, *positive_radius_cells),
        residual_domain=RationalInterval(Fraction(0), wall_radius),
        interface_distribution_free=interface_distribution_free,
        operator_lower_bound=operator_lower_bound,
        wall_trace_margin_lower_bound=wall_trace_margin_lower_bound,
        wall_residual=wall_residual,
    )
