"""Validated regular-origin exterior-master adjoint load.

The positive-radius exterior functional is first integrated by parts as

``B(y)=integral (b0 dot y+b1 dot y') dx``.

At the regular center, write ``t=x^2``, ``y=x a`` and use the center-regular
Green solution ``W=x^3 W_hat(t)``.  All completed-stress cancellations then
occur before interval evaluation and give

``b0=x b0_hat(t)``, ``b1=t b1_hat(t)``.

In fact both hatted loads retain one more factor of ``t``.  This module
computes the hats and their time derivatives without dividing by ``x`` or
``t`` and inserts them into the existing cancellation-safe origin residual.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Generic, TypeVar

from .centrifugal_skyrmion_affine_master_kernel import _AffineScalar
from .centrifugal_skyrmion_origin_master_kernel import (
    _origin_regular_completed_stress,
)
from .centrifugal_skyrmion_rational_response_trials import (
    RationalResponseTrial,
)
from .validated_centrifugal_origin_profile_jets import (
    rational_origin_trial_cell_from_archive,
    validated_authenticated_origin_profile_kernel_cells,
)
from .validated_centrifugal_origin_response_residual import (
    _IntervalTimeJet,
    RationalOriginTrialCell,
    ValidatedOriginProfileKernelCell,
    ValidatedOriginStrongResidual,
    validated_origin_conormal_cell_from_profile,
    validated_origin_strong_residual_cell,
)
from .validated_interval import RationalInterval
from .validated_skyrmion_quintic_family import ValidatedSkyrmionQuinticFamily


Scalar = TypeVar("Scalar")


@dataclass(frozen=True)
class OriginWeakMasterLoadKernel(Generic[Scalar]):
    """Regular master-functional density and physical Fuchs load."""

    rigid_density_hat: Scalar
    field_over_radius_coefficient: tuple[Scalar, Scalar]
    physical_derivative_coefficient: tuple[Scalar, Scalar]
    coordinate_source_hat: tuple[Scalar, Scalar]
    derivative_source_hat: tuple[Scalar, Scalar]


def centrifugal_weak_master_load_origin_affine_kernel(
    *,
    t: Scalar,
    metric_factor: Scalar,
    metric_factor_time_derivative: Scalar,
    inverse_patch_radius_squared: Scalar,
    profile_deficit_radial_derivative: Scalar,
    sine_over_radius: Scalar,
    cosine_of_profile_deficit: Scalar,
    green_weight_hat: Scalar,
    green_weight_derivative_hat: Scalar,
    pion_mass_squared: Scalar,
    gravitational_coupling: Scalar,
) -> OriginWeakMasterLoadKernel[Scalar]:
    """Return ``b0/x`` and ``b1/t`` after exact center cancellation.

    ``green_weight_hat`` and ``green_weight_derivative_hat`` are defined by
    ``W=x^3 green_weight_hat`` and
    ``W'=x^2 green_weight_derivative_hat``.  The four affine stress variables
    are ``(f/x,f',g/x,g')``.
    """
    zero = t - t  # type: ignore[operator]
    one = zero + 1  # type: ignore[operator]
    dimension = 4
    lift = lambda value: _AffineScalar.lifted(value, dimension)  # noqa: E731
    fields = tuple(_AffineScalar.basis(t, dimension, index) for index in range(4))
    stress = _origin_regular_completed_stress(
        t=lift(t),
        metric_factor=lift(metric_factor),
        sine_over_radius=lift(sine_over_radius),
        cosine_of_profile_deficit=lift(cosine_of_profile_deficit),
        profile_deficit_radial_derivative=lift(profile_deficit_radial_derivative),
        radial_field_over_radius=fields[0],
        radial_field_derivative=fields[1],
        tangential_field_over_radius=fields[2],
        tangential_field_derivative=fields[3],
        pion_mass_squared=lift(pion_mass_squared),
    )

    # If A=x^2 N/6 and D=x(1+4 lambda x^2)/6, then the weak energy
    # weight is (WA)'+WD.  Factoring W=x^3 W_hat leaves x^4 times the
    # following regular coefficient.
    energy_weight_hat = gravitational_coupling * (  # type: ignore[operator]
        green_weight_derivative_hat * metric_factor / 6
        + green_weight_hat * (metric_factor + t * metric_factor_time_derivative) / 3
        + green_weight_hat * (one + t * inverse_patch_radius_squared * 4) / 6
    )
    radial_pressure_weight_hat = -(  # type: ignore[operator]
        gravitational_coupling * green_weight_hat / 2
    )
    shear_weight_hat = -(  # type: ignore[operator]
        gravitational_coupling * green_weight_hat
    )
    tracefree_weight_hat = (  # type: ignore[operator]
        gravitational_coupling * green_weight_hat * 2
    )
    contracted = (
        stress.energy_density * energy_weight_hat
        + stress.radial_pressure * radial_pressure_weight_hat
        + stress.radial_angular_shear_over_radius * shear_weight_hat
        + stress.angular_tracefree_stress * tracefree_weight_hat
    )

    # x^4 K_a (f/x)=x^3 K_a f=x (t K_a) f, while
    # x^4 K_d f'=t (t K_d) f'.  The same identities hold for g.
    coefficients = contracted.coefficients
    return OriginWeakMasterLoadKernel(
        rigid_density_hat=contracted.constant,
        field_over_radius_coefficient=(coefficients[0], coefficients[2]),
        physical_derivative_coefficient=(coefficients[1], coefficients[3]),
        coordinate_source_hat=(
            t * coefficients[0],  # type: ignore[operator]
            t * coefficients[2],  # type: ignore[operator]
        ),
        derivative_source_hat=(
            t * coefficients[1],  # type: ignore[operator]
            t * coefficients[3],  # type: ignore[operator]
        ),
    )


def _center_regular_green_hat_jets(
    time: RationalInterval,
    *,
    patch_radius: Fraction,
    terms: int,
) -> tuple[_IntervalTimeJet, _IntervalTimeJet]:
    """Enclose ``W/x^3`` and ``W'/x^2`` with their ``t`` derivatives."""
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("terms must be a positive integer")
    if patch_radius <= 0:
        raise ValueError("patch_radius must be positive")
    if time.lower != 0 or time.upper <= 0:
        raise ValueError("time must be an origin interval [0,h]")
    radius_squared = patch_radius**2
    quotient = time / radius_squared
    if quotient.upper > Fraction(1, 25):
        raise ValueError("green series requires sqrt(t)/patch_radius <= 1/5")

    value = RationalInterval.point(0)
    value_derivative = RationalInterval.point(0)
    radial_derivative = RationalInterval.point(0)
    radial_derivative_time_derivative = RationalInterval.point(0)
    coefficient = Fraction(1)
    power = 3
    for index in range(terms):
        value += quotient.power(index).scale(coefficient)
        radial_derivative += quotient.power(index).scale(coefficient * power)
        if index:
            common = quotient.power(index - 1).scale(
                coefficient * index / radius_squared
            )
            value_derivative += common
            radial_derivative_time_derivative += common.scale(power)
        coefficient *= Fraction(power * (power + 1), (power + 4) * (power - 1))
        power += 2

    # ``coefficient`` and ``power`` now describe the first omitted term.
    upper = quotient.upper
    value += RationalInterval(0, coefficient * upper**terms / (1 - Fraction(1, 25)))
    radial_derivative += RationalInterval(
        0,
        coefficient * power * upper**terms / (1 - Fraction(1, 15)),
    )
    value_derivative += RationalInterval(
        0,
        coefficient
        * terms
        * upper ** (terms - 1)
        / radius_squared
        / (1 - Fraction(2, 25)),
    )
    radial_derivative_time_derivative += RationalInterval(
        0,
        coefficient
        * terms
        * power
        * upper ** (terms - 1)
        / radius_squared
        / (1 - Fraction(1, 5)),
    )
    scale = Fraction(2, 15 * radius_squared)
    return (
        _IntervalTimeJet(value.scale(scale), value_derivative.scale(scale)),
        _IntervalTimeJet(
            radial_derivative.scale(scale),
            radial_derivative_time_derivative.scale(scale),
        ),
    )


@dataclass(frozen=True)
class ValidatedOriginWeakMasterLoadCell:
    """Origin master-load hats and their time derivatives."""

    time: RationalInterval
    green_weight_hat: RationalInterval
    green_weight_hat_time_derivative: RationalInterval
    green_weight_derivative_hat: RationalInterval
    green_weight_derivative_hat_time_derivative: RationalInterval
    rigid_density_hat: RationalInterval
    field_over_radius_coefficient: tuple[RationalInterval, RationalInterval]
    physical_derivative_coefficient: tuple[RationalInterval, RationalInterval]
    coordinate_source_hat: tuple[RationalInterval, RationalInterval]
    coordinate_source_hat_time_derivative: tuple[RationalInterval, RationalInterval]
    derivative_source_hat: tuple[RationalInterval, RationalInterval]
    derivative_source_hat_time_derivative: tuple[RationalInterval, RationalInterval]


def validated_origin_weak_master_load_cell(
    profile: ValidatedOriginProfileKernelCell,
    *,
    curvature: Fraction = Fraction(1, 400),
    pion_mass_squared: Fraction = Fraction(1),
    gravitational_coupling: Fraction = Fraction(1),
    patch_radius: Fraction = Fraction(20),
    green_terms: int = 12,
) -> ValidatedOriginWeakMasterLoadCell:
    """Propagate an authenticated origin profile box through the weak load."""
    if patch_radius**2 * curvature != 1:
        raise ValueError("patch radius and curvature are inconsistent")
    point = RationalInterval.point
    green, green_derivative = _center_regular_green_hat_jets(
        profile.time,
        patch_radius=patch_radius,
        terms=green_terms,
    )
    kernel = centrifugal_weak_master_load_origin_affine_kernel(
        t=_IntervalTimeJet(profile.time, point(1)),
        metric_factor=_IntervalTimeJet(
            profile.metric_factor, profile.metric_factor_time_derivative
        ),
        metric_factor_time_derivative=_IntervalTimeJet.constant(
            profile.metric_factor_time_derivative
        ),
        inverse_patch_radius_squared=_IntervalTimeJet.constant(curvature),
        profile_deficit_radial_derivative=_IntervalTimeJet(
            profile.profile_deficit_radial_derivative,
            profile.profile_deficit_radial_derivative_time_derivative,
        ),
        sine_over_radius=_IntervalTimeJet(
            profile.sine_over_radius,
            profile.sine_over_radius_time_derivative,
        ),
        cosine_of_profile_deficit=_IntervalTimeJet(
            profile.cosine_of_profile_deficit,
            profile.cosine_of_profile_deficit_time_derivative,
        ),
        green_weight_hat=green,
        green_weight_derivative_hat=green_derivative,
        pion_mass_squared=_IntervalTimeJet.constant(pion_mass_squared),
        gravitational_coupling=_IntervalTimeJet.constant(gravitational_coupling),
    )
    coordinate = kernel.coordinate_source_hat
    derivative = kernel.derivative_source_hat
    return ValidatedOriginWeakMasterLoadCell(
        time=profile.time,
        green_weight_hat=green.value,
        green_weight_hat_time_derivative=green.derivative,
        green_weight_derivative_hat=green_derivative.value,
        green_weight_derivative_hat_time_derivative=(green_derivative.derivative),
        rigid_density_hat=kernel.rigid_density_hat.value,
        field_over_radius_coefficient=tuple(
            entry.value for entry in kernel.field_over_radius_coefficient
        ),  # type: ignore[arg-type]
        physical_derivative_coefficient=tuple(
            entry.value for entry in kernel.physical_derivative_coefficient
        ),  # type: ignore[arg-type]
        coordinate_source_hat=tuple(entry.value for entry in coordinate),  # type: ignore[arg-type]
        coordinate_source_hat_time_derivative=tuple(
            entry.derivative for entry in coordinate
        ),  # type: ignore[arg-type]
        derivative_source_hat=tuple(entry.value for entry in derivative),  # type: ignore[arg-type]
        derivative_source_hat_time_derivative=tuple(
            entry.derivative for entry in derivative
        ),  # type: ignore[arg-type]
    )


def validated_loaded_origin_adjoint_residual_cell(
    profile: ValidatedOriginProfileKernelCell,
    trial: RationalOriginTrialCell,
    *,
    curvature: Fraction = Fraction(1, 400),
    pion_mass_squared: Fraction = Fraction(1),
    gravitational_coupling: Fraction = Fraction(1),
    patch_radius: Fraction = Fraction(20),
    green_terms: int = 12,
) -> tuple[ValidatedOriginWeakMasterLoadCell, ValidatedOriginStrongResidual]:
    """Certify ``B-Az_h`` on one authenticated regular-origin cell."""
    coefficients = validated_origin_conormal_cell_from_profile(
        profile,
        pion_mass_squared=pion_mass_squared,
    )
    load = validated_origin_weak_master_load_cell(
        profile,
        curvature=curvature,
        pion_mass_squared=pion_mass_squared,
        gravitational_coupling=gravitational_coupling,
        patch_radius=patch_radius,
        green_terms=green_terms,
    )
    loaded = replace(
        coefficients,
        coordinate_source_hat=load.coordinate_source_hat,
        coordinate_source_hat_time_derivative=(
            load.coordinate_source_hat_time_derivative
        ),
        derivative_source_hat=load.derivative_source_hat,
        derivative_source_hat_time_derivative=(
            load.derivative_source_hat_time_derivative
        ),
    )
    return load, validated_origin_strong_residual_cell(loaded, trial)


@dataclass(frozen=True)
class ValidatedLoadedOriginAdjointResidualFamily:
    """Loaded adjoint origin residual over every authenticated slope cell."""

    trial_name: str
    loads: tuple[ValidatedOriginWeakMasterLoadCell, ...]
    residuals: tuple[ValidatedOriginStrongResidual, ...]
    maximum_l2_squared_upper: Fraction


def validated_archived_loaded_origin_adjoint_residual_family(
    family: ValidatedSkyrmionQuinticFamily,
    trial: RationalResponseTrial,
    *,
    kernel_terms: int = 12,
    green_terms: int = 12,
    gravitational_coupling: Fraction = Fraction(1),
) -> ValidatedLoadedOriginAdjointResidualFamily:
    """Certify the loaded origin residual for an archived adjoint trial."""
    if not isinstance(family, ValidatedSkyrmionQuinticFamily):
        raise TypeError("family must be a ValidatedSkyrmionQuinticFamily")
    if not isinstance(trial, RationalResponseTrial):
        raise TypeError("trial must be a RationalResponseTrial")
    trial.validate()
    if trial.origin.cutoff != family.cutoff:
        raise ValueError("trial and profile-family origin cutoffs differ")
    regular_trial = rational_origin_trial_cell_from_archive(trial.origin)
    profiles = validated_authenticated_origin_profile_kernel_cells(
        family,
        kernel_terms=kernel_terms,
    )
    loads = []
    residuals = []
    for authenticated in profiles:
        load, residual = validated_loaded_origin_adjoint_residual_cell(
            authenticated.kernels,
            regular_trial,
            curvature=family.curvature,
            pion_mass_squared=family.pion_mass_squared,
            gravitational_coupling=gravitational_coupling,
            patch_radius=Fraction(20),
            green_terms=green_terms,
        )
        loads.append(load)
        residuals.append(residual)
    return ValidatedLoadedOriginAdjointResidualFamily(
        trial_name=trial.name,
        loads=tuple(loads),
        residuals=tuple(residuals),
        maximum_l2_squared_upper=max(
            residual.l2_squared_upper for residual in residuals
        ),
    )
