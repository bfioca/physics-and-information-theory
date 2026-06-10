"""Authenticated regular-origin profile jets for response residuals.

The uniform quintic theorem controls the profile variables

``rho=-F'=b-3ct-5dt^2+t^3 r_p`` and
``u=(pi-F)/x=b-ct-dt^2+t^3 r_u``

only in ``L-infinity``.  This module never differentiates ``r_p`` or ``r_u``.
Instead it obtains ``u_t`` from ``rho=u+2t u_t`` and obtains ``rho_t`` from
the exact Volterra vector field after cancelling its identically zero center
coefficient.  Entire even kernels then give rigorous ``t`` jets for
``sin(F)/x`` and ``cos(pi-F)`` on the full origin cell.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from math import factorial
from typing import Literal

from .centrifugal_skyrmion_rational_response_trials import (
    RationalResponseTrial,
    RegularOriginTrial,
)
from .validated_centrifugal_origin_response_residual import (
    RationalOriginTrialCell,
    ValidatedOriginConormalCell,
    ValidatedOriginProfileKernelCell,
    ValidatedOriginStrongResidual,
    validated_origin_conormal_cell_from_profile,
    validated_origin_strong_residual_cell,
)
from .validated_interval import RationalInterval, RationalPolynomial
from .validated_skyrmion_origin import _entire_even_kernel_interval
from .validated_skyrmion_quintic_family import (
    ValidatedSkyrmionQuinticFamily,
    ValidatedSkyrmionQuinticFamilyCell,
)


OriginLoad = Literal["rotational", "zero"]


def _sinc_centered_quotient_interval(
    argument: RationalInterval,
    *,
    scale_squared: int,
    terms: int,
) -> RationalInterval:
    """Enclose ``(sinc(scale*sqrt(w))-1)/w``, including at ``w=0``."""
    if argument.lower < 0:
        raise ValueError("centered-kernel argument must be nonnegative")
    if terms < 2:
        raise ValueError("centered-kernel quotient requires at least two terms")
    total = RationalInterval.point(0)
    for index in range(1, terms):
        total += argument.power(index - 1).scale(
            Fraction(
                (-1) ** index * scale_squared**index,
                factorial(2 * index + 1),
            )
        )
    ratio = (
        Fraction(scale_squared)
        * argument.upper
        / ((2 * terms + 2) * (2 * terms + 3))
    )
    if ratio >= 1:
        raise ValueError("centered-kernel tail ratio must be below one")
    tail = (
        Fraction(scale_squared**terms, factorial(2 * terms + 1))
        * argument.upper ** (terms - 1)
        / (1 - ratio)
    )
    return total + RationalInterval(-tail, tail)


def _cosine_kernel_interval(
    argument: RationalInterval,
    *,
    derivative_order: int,
    terms: int,
) -> RationalInterval:
    """Enclose a ``w`` derivative of ``cos(sqrt(w))``."""
    if argument.lower < 0:
        raise ValueError("cosine-kernel argument must be nonnegative")
    if derivative_order not in (0, 1):
        raise ValueError("only cosine derivative orders zero and one are supported")
    if terms <= derivative_order:
        raise ValueError("too few cosine terms")
    total = RationalInterval.point(0)
    for index in range(derivative_order, terms):
        falling = index if derivative_order else 1
        total += argument.power(index - derivative_order).scale(
            Fraction((-1) ** index * falling, factorial(2 * index))
        )
    first_falling = terms if derivative_order else 1
    first = (
        Fraction(first_falling, factorial(2 * terms))
        * argument.upper ** (terms - derivative_order)
    )
    ratio = (
        argument.upper
        * Fraction(terms + 1, terms + 1 - derivative_order)
        / ((2 * terms + 1) * (2 * terms + 2))
    )
    if ratio >= 1:
        raise ValueError("cosine geometric-tail ratio must be below one")
    tail = first / (1 - ratio)
    return total + RationalInterval(-tail, tail)


def _profile_ranges(
    family: ValidatedSkyrmionQuinticFamily,
    cell: ValidatedSkyrmionQuinticFamilyCell,
) -> tuple[RationalInterval, RationalInterval, RationalInterval]:
    horizon = family.cutoff**2
    time = RationalInterval(Fraction(0), horizon)
    remainder = RationalInterval(
        -family.remainder_radius,
        family.remainder_radius,
    )
    rho = (
        cell.shooting_slopes
        + time * cell.cubic_coefficient.scale(-3)
        + time.power(2) * cell.quintic_coefficient.scale(-5)
        + time.power(3) * remainder
    )
    profile = (
        cell.shooting_slopes
        - time * cell.cubic_coefficient
        - time.power(2) * cell.quintic_coefficient
        + time.power(3) * remainder.scale(Fraction(1, 7))
    )
    profile_t = (
        -cell.cubic_coefficient
        + time * cell.quintic_coefficient.scale(-2)
        + time.power(2)
        * (remainder - remainder.scale(Fraction(1, 7))).scale(Fraction(1, 2))
    )
    return profile, rho, profile_t


def _rho_time_derivative_range(
    family: ValidatedSkyrmionQuinticFamily,
    profile: RationalInterval,
    rho: RationalInterval,
    profile_t: RationalInterval,
    *,
    kernel_terms: int,
) -> RationalInterval:
    """Range ``rho_t`` through an explicitly divided Volterra identity."""
    time = RationalInterval(Fraction(0), family.cutoff**2)
    argument = time * profile.power(2)
    sinc = _entire_even_kernel_interval(
        argument,
        scale_squared=1,
        derivative_order=0,
        terms=kernel_terms,
    )
    sinc_prime = _entire_even_kernel_interval(
        argument,
        scale_squared=1,
        derivative_order=1,
        terms=kernel_terms,
    )
    sine_over_radius = profile * sinc
    argument_t = profile * rho
    sine_t = profile_t * sinc + profile * sinc_prime * argument_t
    lapse = RationalInterval(1 - family.curvature * family.cutoff**2, 1)
    denominator_factor = RationalInterval.point(1) + sine_over_radius.power(2).scale(8)
    denominator = lapse * denominator_factor
    denominator_t = denominator_factor.scale(-family.curvature) + (
        lapse * sine_over_radius * sine_t
    ).scale(16)
    bracket = (
        RationalInterval.point(1)
        + sine_over_radius.power(2).scale(4)
        + (lapse * rho.power(2)).scale(4)
    )
    quotient_sinc = _sinc_centered_quotient_interval(
        argument,
        scale_squared=1,
        terms=kernel_terms,
    )
    quotient_sinc_twice = _sinc_centered_quotient_interval(
        argument,
        scale_squared=4,
        terms=kernel_terms,
    )
    bracket_minus_denominator_over_time = (
        RationalInterval.point(family.curvature)
        * (RationalInterval.point(1) + sine_over_radius.power(2).scale(4))
        + (
            lapse
            * (profile_t.scale(2) - profile.power(3) * quotient_sinc)
            * (rho + sine_over_radius)
        ).scale(4)
    )
    source_minus_denominator_rho_over_time = (
        profile.power(3) * quotient_sinc_twice * bracket
        + profile * bracket_minus_denominator_over_time
        - denominator * profile_t.scale(2)
        - sine_over_radius.scale(family.pion_mass_squared / 2)
    )
    return (
        source_minus_denominator_rho_over_time - denominator_t * rho
    ) / denominator


@dataclass(frozen=True)
class ValidatedAuthenticatedOriginProfileKernelCell:
    """One shooting-slope cell and its regular profile-kernel jet box."""

    shooting_slopes: RationalInterval
    cubic_coefficient: RationalInterval
    quintic_coefficient: RationalInterval
    kernels: ValidatedOriginProfileKernelCell


def validated_authenticated_origin_profile_kernel_cells(
    family: ValidatedSkyrmionQuinticFamily,
    *,
    kernel_terms: int = 12,
) -> tuple[ValidatedAuthenticatedOriginProfileKernelCell, ...]:
    """Extract response-ready kernel ``t`` jets from a quintic family."""
    if not isinstance(family, ValidatedSkyrmionQuinticFamily):
        raise TypeError("family must be a ValidatedSkyrmionQuinticFamily")
    if isinstance(kernel_terms, bool) or not isinstance(kernel_terms, int):
        raise TypeError("kernel_terms must be an integer")
    if kernel_terms < 4:
        raise ValueError("kernel_terms must be at least four")
    horizon = family.cutoff**2
    time = RationalInterval(Fraction(0), horizon)
    result = []
    for cell in family.cells:
        profile, rho, profile_t = _profile_ranges(family, cell)
        argument = time * profile.power(2)
        sinc = _entire_even_kernel_interval(
            argument,
            scale_squared=1,
            derivative_order=0,
            terms=kernel_terms,
        )
        sinc_prime = _entire_even_kernel_interval(
            argument,
            scale_squared=1,
            derivative_order=1,
            terms=kernel_terms,
        )
        argument_t = profile * rho
        sine = profile * sinc
        sine_t = profile_t * sinc + profile * sinc_prime * argument_t
        rho_t = _rho_time_derivative_range(
            family,
            profile,
            rho,
            profile_t,
            kernel_terms=kernel_terms,
        )
        cosine = _cosine_kernel_interval(
            argument,
            derivative_order=0,
            terms=kernel_terms,
        )
        cosine_prime = _cosine_kernel_interval(
            argument,
            derivative_order=1,
            terms=kernel_terms,
        )
        cosine_t = cosine_prime * argument_t
        result.append(
            ValidatedAuthenticatedOriginProfileKernelCell(
                shooting_slopes=cell.shooting_slopes,
                cubic_coefficient=cell.cubic_coefficient,
                quintic_coefficient=cell.quintic_coefficient,
                kernels=ValidatedOriginProfileKernelCell(
                    time=time,
                    metric_factor=RationalInterval(
                        1 - family.curvature * horizon,
                        1,
                    ),
                    metric_factor_time_derivative=RationalInterval.point(
                        -family.curvature
                    ),
                    profile_deficit_radial_derivative=rho,
                    profile_deficit_radial_derivative_time_derivative=rho_t,
                    sine_over_radius=sine,
                    sine_over_radius_time_derivative=sine_t,
                    cosine_of_profile_deficit=cosine,
                    cosine_of_profile_deficit_time_derivative=cosine_t,
                ),
            )
        )
    return tuple(result)


def rational_origin_trial_cell_from_archive(
    trial: RegularOriginTrial,
) -> RationalOriginTrialCell:
    """Convert a polynomial in physical ``t`` to one in ``tau=t/h``."""
    if not isinstance(trial, RegularOriginTrial):
        raise TypeError("trial must be a RegularOriginTrial")
    horizon = trial.cutoff**2

    def normalized(polynomial: RationalPolynomial) -> RationalPolynomial:
        return RationalPolynomial(
            tuple(
                coefficient * horizon**degree
                for degree, coefficient in enumerate(polynomial.coefficients)
            )
        )

    result = RationalOriginTrialCell(
        time_horizon=horizon,
        u=normalized(trial.u_polynomial),
        v=normalized(trial.v_polynomial),
    )
    if result.physical_endpoint_jet() != trial.physical_endpoint_jet():
        raise AssertionError("normalized origin trial changed its endpoint jet")
    return result


def _zero_load(coefficients: ValidatedOriginConormalCell) -> ValidatedOriginConormalCell:
    zero = RationalInterval.point(0)
    vector = (zero, zero)
    return replace(
        coefficients,
        coordinate_source_hat=vector,
        coordinate_source_hat_time_derivative=vector,
        derivative_source_hat=vector,
        derivative_source_hat_time_derivative=vector,
    )


@dataclass(frozen=True)
class ValidatedOriginTrialResidualFamily:
    """Residual enclosures over every authenticated shooting-slope cell."""

    trial_name: str
    load: OriginLoad
    residuals: tuple[ValidatedOriginStrongResidual, ...]
    maximum_l2_squared_upper: Fraction


def validated_archived_origin_trial_residual_family(
    family: ValidatedSkyrmionQuinticFamily,
    trial: RationalResponseTrial,
    *,
    load: OriginLoad = "rotational",
    kernel_terms: int = 12,
) -> ValidatedOriginTrialResidualFamily:
    """Evaluate one archived origin trial over the authenticated profile family.

    ``load="rotational"`` is the physical primal residual.  ``load="zero"``
    encloses the homogeneous operator action on an adjoint-shaped trial; it is
    not an adjoint residual until the exterior-amplitude load is supplied.
    """
    if not isinstance(trial, RationalResponseTrial):
        raise TypeError("trial must be a RationalResponseTrial")
    trial.validate()
    if trial.origin.cutoff != family.cutoff:
        raise ValueError("trial and profile-family origin cutoffs differ")
    if load not in ("rotational", "zero"):
        raise ValueError("load must be 'rotational' or 'zero'")
    regular_trial = rational_origin_trial_cell_from_archive(trial.origin)
    profile_cells = validated_authenticated_origin_profile_kernel_cells(
        family,
        kernel_terms=kernel_terms,
    )
    residuals = []
    for profile in profile_cells:
        coefficients = validated_origin_conormal_cell_from_profile(
            profile.kernels,
            pion_mass_squared=family.pion_mass_squared,
        )
        if load == "zero":
            coefficients = _zero_load(coefficients)
        residuals.append(
            validated_origin_strong_residual_cell(coefficients, regular_trial)
        )
    return ValidatedOriginTrialResidualFamily(
        trial_name=trial.name,
        load=load,
        residuals=tuple(residuals),
        maximum_l2_squared_upper=max(
            residual.l2_squared_upper for residual in residuals
        ),
    )
