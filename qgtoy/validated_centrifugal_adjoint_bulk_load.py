"""Validated weak exterior-master load on positive-radius cells.

The smooth master source contains a radial derivative of the completed energy
density.  Differentiating an interval profile tube would destroy the available
regularity and introduce a second derivative of the trial.  Instead this
module performs the exact integration by parts first and exposes

``B_bulk(v) = integral (b0 dot v + b1 dot v') dx``.

The resulting algebra needs only ``F`` and ``F'``.  It accepts generic scalar
arithmetic, and the validated wrapper evaluates it with exact rational
intervals on each authenticated positive-radius cell.  The cell integral uses
the elementary range-times-width enclosure; no quadrature samples are treated
as rigorous data.

The weak residual coefficients returned here are not, by themselves, an
energy-dual residual norm.  A Riesz or strong-residual lift still has to be
certified before using them in the dual-weighted zero-exclusion theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Generic, TypeVar

from .centrifugal_skyrmion_affine_master_kernel import (
    StressAmplitudes,
    centrifugal_completed_stress_affine_kernel,
)
from .validated_centrifugal_response_residual import (
    IntervalVector2,
    RationalC1TrialCell,
    ValidatedConormalStrongCell,
    ValidatedProfileJetCell,
    reduced_profile_trigonometric_intervals,
)
from .validated_interval import RationalInterval


Scalar = TypeVar("Scalar")


@dataclass(frozen=True)
class WeakMasterLoadKernel(Generic[Scalar]):
    """Affine weak-load density in ``(f,g,f',g')``."""

    rigid: Scalar
    radial_field: Scalar
    tangential_field: Scalar
    radial_field_derivative: Scalar
    tangential_field_derivative: Scalar

    @property
    def b0(self) -> tuple[Scalar, Scalar]:
        return self.radial_field, self.tangential_field

    @property
    def b1(self) -> tuple[Scalar, Scalar]:
        return self.radial_field_derivative, self.tangential_field_derivative

    def evaluate(
        self,
        *,
        radial_field: Scalar,
        radial_field_derivative: Scalar,
        tangential_field: Scalar,
        tangential_field_derivative: Scalar,
    ) -> Scalar:
        return (  # type: ignore[return-value]
            self.rigid
            + self.radial_field * radial_field  # type: ignore[operator]
            + self.tangential_field * tangential_field
            + self.radial_field_derivative * radial_field_derivative
            + self.tangential_field_derivative * tangential_field_derivative
        )


def _contract_master_weights(
    stress: StressAmplitudes[Scalar],
    *,
    energy_weight: Scalar,
    radial_pressure_weight: Scalar,
    shear_weight: Scalar,
    tracefree_weight: Scalar,
) -> Scalar:
    return (  # type: ignore[return-value]
        energy_weight * stress.energy_density  # type: ignore[operator]
        + radial_pressure_weight * stress.radial_pressure
        + shear_weight * stress.radial_angular_shear
        + tracefree_weight * stress.angular_tracefree_stress
    )


def centrifugal_weak_master_load_affine_kernel(
    *,
    radius: Scalar,
    metric_factor: Scalar,
    metric_factor_derivative: Scalar,
    inverse_patch_radius_squared: Scalar,
    sine_profile: Scalar,
    cosine_profile: Scalar,
    profile_derivative: Scalar,
    pion_mass_squared: Scalar,
    green_weight: Scalar,
    green_weight_derivative: Scalar,
    gravitational_coupling: Scalar,
) -> WeakMasterLoadKernel[Scalar]:
    """Return exact weak coefficients after integrating ``rho'`` by parts.

    If ``A=x^2 N/6`` and ``D=x(1+4 lambda x^2)/6``, the four stress weights
    are ``((wA)'+wD, -wx/2, -w, 2wx)`` times the gravitational coupling.
    The omitted boundary term is handled by the independently validated
    moving-wall load and vanishes at the regular center.
    """
    one = radius - radius + 1  # type: ignore[operator]
    radius_squared = radius * radius  # type: ignore[operator]
    coefficient_a = radius_squared * metric_factor / 6  # type: ignore[operator]
    coefficient_a_derivative = (  # type: ignore[operator]
        radius * metric_factor / 3
        + radius_squared * metric_factor_derivative / 6
    )
    coefficient_d = (  # type: ignore[operator]
        radius * (one + radius_squared * inverse_patch_radius_squared * 4) / 6
    )
    energy_weight = gravitational_coupling * (  # type: ignore[operator]
        green_weight_derivative * coefficient_a
        + green_weight * coefficient_a_derivative
        + green_weight * coefficient_d
    )
    radial_pressure_weight = -(  # type: ignore[operator]
        gravitational_coupling * green_weight * radius / 2
    )
    shear_weight = -(gravitational_coupling * green_weight)  # type: ignore[operator]
    tracefree_weight = (  # type: ignore[operator]
        gravitational_coupling * green_weight * radius * 2
    )
    stress = centrifugal_completed_stress_affine_kernel(
        radius=radius,
        metric_factor=metric_factor,
        sine_profile=sine_profile,
        cosine_profile=cosine_profile,
        profile_derivative=profile_derivative,
        pion_mass_squared=pion_mass_squared,
    )
    contract = lambda value: _contract_master_weights(  # noqa: E731
        value,
        energy_weight=energy_weight,
        radial_pressure_weight=radial_pressure_weight,
        shear_weight=shear_weight,
        tracefree_weight=tracefree_weight,
    )
    return WeakMasterLoadKernel(
        rigid=contract(stress.rigid),
        radial_field=contract(stress.radial_field),
        tangential_field=contract(stress.tangential_field),
        radial_field_derivative=contract(stress.radial_field_derivative),
        tangential_field_derivative=contract(stress.tangential_field_derivative),
    )


def _center_regular_green_intervals(
    radius: RationalInterval,
    *,
    patch_radius: Fraction,
    terms: int,
) -> tuple[RationalInterval, RationalInterval]:
    """Enclose ``w=(2R/15)u(x/R)`` and ``w'`` by positive series.

    On the physical domain ``x/R <= 1/5`` all coefficients are positive.
    Successive value terms are bounded by ``1/25`` and successive derivative
    terms by ``2/25``.  The first omitted term therefore gives a geometric
    tail enclosure without transcendental endpoint evaluation.
    """
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    ratio = radius / patch_radius
    if ratio.lower < 0 or ratio.upper > Fraction(1, 5):
        raise ValueError("green series requires 0 <= radius/patch_radius <= 1/5")
    value = RationalInterval.point(0)
    derivative = RationalInterval.point(0)
    coefficient = Fraction(1)
    power = 3
    for _ in range(terms):
        value += ratio.power(power).scale(coefficient)
        derivative += ratio.power(power - 1).scale(coefficient * power)
        coefficient *= Fraction(power * (power + 1), (power + 4) * (power - 1))
        power += 2
    next_value_upper = coefficient * ratio.upper**power
    next_derivative_upper = coefficient * power * ratio.upper ** (power - 1)
    value += RationalInterval(0, next_value_upper / (1 - Fraction(1, 25)))
    derivative += RationalInterval(
        0, next_derivative_upper / (1 - Fraction(2, 25))
    )
    return (
        value.scale(2 * patch_radius / 15),
        derivative.scale(Fraction(2, 15)),
    )


@dataclass(frozen=True)
class ValidatedWeakMasterLoadCell:
    """Interval weak-load coefficients on one positive-radius cell."""

    radius: RationalInterval
    green_weight: RationalInterval
    green_weight_derivative: RationalInterval
    rigid: RationalInterval
    b0: IntervalVector2
    b1: IntervalVector2


def validated_weak_master_load_cell(
    profile: ValidatedProfileJetCell,
    *,
    curvature: Fraction = Fraction(1, 400),
    pion_mass_squared: Fraction = Fraction(1),
    gravitational_coupling: Fraction = Fraction(1),
    patch_radius: Fraction = Fraction(20),
    green_terms: int = 12,
    trigonometric_terms: int = 12,
) -> ValidatedWeakMasterLoadCell:
    """Enclose ``b0,b1`` on one authenticated positive-radius profile box."""
    if patch_radius * patch_radius * curvature != 1:
        raise ValueError("patch radius and curvature are inconsistent")
    point = RationalInterval.point
    radius = profile.radius
    metric = point(1) - radius.power(2).scale(curvature)
    if metric.lower <= 0:
        raise ValueError("profile cell must lie strictly inside the horizon")
    sine, cosine_deficit = reduced_profile_trigonometric_intervals(
        profile.profile,
        trigonometric_terms=trigonometric_terms,
    )
    green, green_derivative = _center_regular_green_intervals(
        radius,
        patch_radius=patch_radius,
        terms=green_terms,
    )
    kernel = centrifugal_weak_master_load_affine_kernel(
        radius=radius,
        metric_factor=metric,
        metric_factor_derivative=radius.scale(-2 * curvature),
        inverse_patch_radius_squared=point(curvature),
        sine_profile=sine,
        cosine_profile=-cosine_deficit,
        profile_derivative=profile.derivative,
        pion_mass_squared=point(pion_mass_squared),
        green_weight=green,
        green_weight_derivative=green_derivative,
        gravitational_coupling=point(gravitational_coupling),
    )
    return ValidatedWeakMasterLoadCell(
        radius=radius,
        green_weight=green,
        green_weight_derivative=green_derivative,
        rigid=kernel.rigid,
        b0=kernel.b0,
        b1=kernel.b1,
    )


def validated_bulk_load_on_trial_cell(
    load: ValidatedWeakMasterLoadCell,
    trial: RationalC1TrialCell,
) -> RationalInterval:
    """Enclose the deformation bulk functional on one exact trial cell."""
    if load.radius != trial.radius:
        raise ValueError("load and trial cells use different radial intervals")
    value, derivative, _ = trial.jet_range()
    density = RationalInterval.point(0)
    for coefficient, field in zip(load.b0, value, strict=True):
        density += coefficient * field
    for coefficient, field in zip(load.b1, derivative, strict=True):
        density += coefficient * field
    return density.scale(load.radius.width)


@dataclass(frozen=True)
class ValidatedWeakAdjointResidualCell:
    """Coefficient box ``r0 dot v+r1 dot v'`` for the adjoint residual."""

    radius: RationalInterval
    test_value_coefficient: IntervalVector2
    test_derivative_coefficient: IntervalVector2


def _matrix_vector(
    matrix: tuple[tuple[RationalInterval, RationalInterval], ...],
    vector: IntervalVector2,
) -> IntervalVector2:
    return tuple(
        row[0] * vector[0] + row[1] * vector[1] for row in matrix
    )  # type: ignore[return-value]


def _transpose(
    matrix: tuple[tuple[RationalInterval, RationalInterval], ...],
) -> tuple[tuple[RationalInterval, RationalInterval], ...]:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def validated_weak_adjoint_residual_cell(
    coefficients: ValidatedConormalStrongCell,
    load: ValidatedWeakMasterLoadCell,
    adjoint_trial: RationalC1TrialCell,
) -> ValidatedWeakAdjointResidualCell:
    """Enclose ``B(v)-q(v,z_h)`` without differentiating ``b1``.

    This is a rigorous weak coefficient representation.  It is intentionally
    not assigned an ``L2`` norm because the derivative-test term requires a
    form-dual lift, not the strong-residual estimate used for pure ``L2``
    loads.
    """
    if coefficients.radius != load.radius or load.radius != adjoint_trial.radius:
        raise ValueError("coefficient, load, and trial cells must coincide")
    value, derivative, _ = adjoint_trial.jet_range()
    coordinate_value = _matrix_vector(coefficients.coordinate, value)
    mixed_derivative = _matrix_vector(coefficients.mixed, derivative)
    mixed_transpose_value = _matrix_vector(_transpose(coefficients.mixed), value)
    principal_derivative = _matrix_vector(coefficients.principal, derivative)
    return ValidatedWeakAdjointResidualCell(
        radius=load.radius,
        test_value_coefficient=tuple(
            load_value - coordinate - mixed
            for load_value, coordinate, mixed in zip(
                load.b0, coordinate_value, mixed_derivative, strict=True
            )
        ),  # type: ignore[arg-type]
        test_derivative_coefficient=tuple(
            load_value - mixed - principal
            for load_value, mixed, principal in zip(
                load.b1, mixed_transpose_value, principal_derivative, strict=True
            )
        ),  # type: ignore[arg-type]
    )
