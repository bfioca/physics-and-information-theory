"""Directed lapse-coefficient replay for the authenticated Skyrmion profile."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_interval import (
    RationalInterval,
    pi_machin_interval,
    sin_center_lipschitz_interval,
)
from .validated_skyrmion_origin import (
    ValidatedSkyrmionOriginFamily,
    _entire_even_kernel_interval,
)
from .validated_skyrmion_sharp_profile import ValidatedSkyrmionSharpProfileTube


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


@dataclass(frozen=True)
class ValidatedSkyrmionLapseCoefficient:
    certificate_id: str
    coefficient: RationalInterval
    origin_cell_count: int
    positive_radius_cell_count: int
    claim_boundary: str


def build_validated_skyrmion_lapse_coefficient(
    profile: ValidatedSkyrmionSharpProfileTube,
    origin_family: ValidatedSkyrmionOriginFamily,
    *,
    origin_subdivisions: int = 32,
    trigonometric_terms: int = 24,
    origin_kernel_terms: int = 20,
    pi_terms: int = 80,
) -> ValidatedSkyrmionLapseCoefficient:
    """Bound ``D=2pi int x F'^2(1/4+2sin^2(F)/x^2) dx``."""
    origin_parts = _positive_integer("origin_subdivisions", origin_subdivisions)
    trig_terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    kernel_terms = _positive_integer("origin_kernel_terms", origin_kernel_terms)
    pi_count = _positive_integer("pi_terms", pi_terms)
    if (
        origin_family.cutoff != profile.origin_cutoff
        or origin_family.curvature != profile.curvature
        or origin_family.pion_mass_squared != profile.pion_mass_squared
        or origin_family.shooting_slopes != profile.shooting_slope_interval
    ):
        raise ValueError("origin family does not match the sharp profile")
    two_pi = pi_machin_interval(terms=pi_count).scale(2)
    integral = RationalInterval.point(0)

    origin_step = profile.origin_cutoff / origin_parts
    remainder_box = RationalInterval(
        -origin_family.remainder_radius,
        origin_family.remainder_radius,
    )
    for index in range(origin_parts):
        radius = RationalInterval(index * origin_step, (index + 1) * origin_step)
        time = radius.power(2)
        time_squared = time.power(2)
        u = (
            origin_family.shooting_slopes
            - origin_family.cubic_coefficient * time
            + (remainder_box * time_squared).scale(Fraction(1, 5))
        )
        momentum = (
            origin_family.shooting_slopes
            - (origin_family.cubic_coefficient * time).scale(3)
            + remainder_box * time_squared
        )
        sinc = _entire_even_kernel_interval(
            time * u.power(2),
            scale_squared=1,
            derivative_order=0,
            terms=kernel_terms,
        )
        sine_over_radius_squared = (u * sinc).power(2)
        density = (
            two_pi
            * radius
            * momentum.power(2)
            * (
                RationalInterval.point(Fraction(1, 4))
                + sine_over_radius_squared.scale(2)
            )
        )
        if density.lower < 0:
            raise AssertionError("origin lapse density became negative")
        integral += density.scale(radius.width)

    for cell in profile.cells:
        sine_squared = sin_center_lipschitz_interval(
            cell.solution_profile,
            terms=trig_terms,
        ).power(2)
        density = (
            two_pi
            * cell.radius
            * cell.solution_derivative.power(2)
            * (
                RationalInterval.point(Fraction(1, 4))
                + sine_squared.scale(2) / cell.radius.power(2)
            )
        )
        if density.lower < 0:
            raise AssertionError("positive-radius lapse density became negative")
        integral += density.scale(cell.radius.width)
    if integral.lower <= 0:
        raise AssertionError("lapse coefficient must be strictly positive")
    return ValidatedSkyrmionLapseCoefficient(
        certificate_id=profile.certificate_id,
        coefficient=integral,
        origin_cell_count=origin_parts,
        positive_radius_cell_count=len(profile.cells),
        claim_boundary=(
            "Directed fixed-profile coefficient for the static spherical lapse "
            "equation. It excludes collective rotation, the membrane junction, "
            "field deformation, and nonspherical stress."
        ),
    )
