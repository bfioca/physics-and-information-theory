"""Validated fixed-wall radial gap for the authenticated Skyrmion branch.

The positive-radius AU.1 Barta audit applies to the rational center spline.
This module propagates the same witness through the exact-solution Newton tube
by replaying correlated polynomial subcells and adding the local Newton radii.
It also evaluates the Jacobi quotient at the regular origin in variables that
remove all apparent inverse powers of the radius.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_interval import (
    RationalInterval,
    cos_center_lipschitz_interval,
)
from .validated_skyrmion_bvp import (
    SkyrmionJacobiCoefficientBox,
    SkyrmionJetBox,
    skyrmion_barta_quotient_box,
)
from .validated_skyrmion_origin import (
    ValidatedSkyrmionOriginFamily,
    _entire_even_kernel_interval,
)
from .validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpProfileTube,
    _endpoint_family_jet,
)


@dataclass(frozen=True)
class ValidatedSkyrmionExactTubeBartaCell:
    """One accepted correlated Newton-tube Barta leaf."""

    source_cell_index: int
    depth: int
    normalized_left: Fraction
    normalized_right: Fraction
    jet: SkyrmionJetBox
    coefficients: SkyrmionJacobiCoefficientBox
    quotient: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionExactTubeBartaBound:
    """Adaptive Barta validation for the exact solution on positive radii."""

    certificate_id: str
    origin_cutoff: Fraction
    wall_radius: Fraction
    declared_lower_bound: Fraction
    recomputed_lower_bound: Fraction
    maximum_depth_used: int
    cells: tuple[ValidatedSkyrmionExactTubeBartaCell, ...]


@dataclass(frozen=True)
class ValidatedSkyrmionOriginBartaBound:
    """Cancellation-preserving Barta validation on the regular origin patch."""

    radius: RationalInterval
    coefficients: SkyrmionJacobiCoefficientBox
    quotient: RationalInterval
    declared_lower_bound: Fraction
    regular_mode_boundary_term_vanishes: bool


@dataclass(frozen=True)
class ValidatedSkyrmionFixedWallRadialGap:
    """Full origin-to-wall form and generalized-frequency lower bounds."""

    certificate_id: str
    static_form_gap: Fraction
    kinetic_weight_upper_bound: Fraction
    dimensionless_frequency_squared_lower_bound: Fraction
    positive_radius: ValidatedSkyrmionExactTubeBartaBound
    origin: ValidatedSkyrmionOriginBartaBound
    fixed_wall_dirichlet_boundary_term_vanishes: bool
    conclusion_scope: str


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _fraction(name: str, value: Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def validate_skyrmion_exact_solution_tube_barta(
    tube: ValidatedSkyrmionSharpProfileTube,
    *,
    declared_lower_bound: Fraction = Fraction(1),
    maximum_refinement_depth: int = 6,
    trigonometric_terms: int = 24,
) -> ValidatedSkyrmionExactTubeBartaBound:
    """Propagate the Barta quotient through the exact-solution Newton tube."""

    if not isinstance(tube, ValidatedSkyrmionSharpProfileTube):
        raise TypeError("tube must be a validated sharp profile tube")
    declared = _fraction("declared_lower_bound", declared_lower_bound)
    if declared <= 0:
        raise ValueError("declared_lower_bound must be positive")
    depth_limit = _positive_integer(
        "maximum_refinement_depth", maximum_refinement_depth
    )
    terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    accepted: list[ValidatedSkyrmionExactTubeBartaCell] = []

    def check_leaf(
        source_cell_index: int,
        normalized_left: Fraction,
        normalized_right: Fraction,
        depth: int,
    ) -> None:
        profile_cell = tube.profile_cells[source_cell_index]
        parent = tube.parents[source_cell_index]
        family = _endpoint_family_jet(
            profile_cell,
            normalized_left,
            normalized_right,
            domain_left=tube.origin_cutoff,
            domain_right=tube.wall_radius,
            left_value_correction=tube.left_value_correction,
            right_value_correction=tube.right_value_correction,
        )
        jet = SkyrmionJetBox(
            radius=family.radius,
            profile=family.profile
            + RationalInterval(-parent.profile_error_radius, parent.profile_error_radius),
            derivative=family.derivative
            + RationalInterval(
                -parent.derivative_error_radius,
                parent.derivative_error_radius,
            ),
            second_derivative=family.second_derivative
            + RationalInterval(
                -parent.second_derivative_error_radius,
                parent.second_derivative_error_radius,
            ),
        )
        if (
            not jet.profile.is_subset_of(parent.archived_tube_jet.profile)
            or not jet.derivative.is_subset_of(parent.archived_tube_jet.derivative)
            or not jet.second_derivative.is_subset_of(
                parent.archived_tube_jet.second_derivative
            )
        ):
            raise ValueError("refined Barta jet escaped its authenticated parent tube")
        coefficients, quotient = skyrmion_barta_quotient_box(
            jet,
            pion_mass_squared=tube.pion_mass_squared,
            curvature=tube.curvature,
            trigonometric_terms=terms,
        )
        if coefficients.principal.lower > 0 and quotient.lower >= declared:
            accepted.append(
                ValidatedSkyrmionExactTubeBartaCell(
                    source_cell_index=source_cell_index,
                    depth=depth,
                    normalized_left=normalized_left,
                    normalized_right=normalized_right,
                    jet=jet,
                    coefficients=coefficients,
                    quotient=quotient,
                )
            )
            return
        if depth >= depth_limit:
            raise ValueError(
                "exact-solution Barta target failed at maximum refinement depth"
            )
        midpoint = (normalized_left + normalized_right) / 2
        check_leaf(source_cell_index, normalized_left, midpoint, depth + 1)
        check_leaf(source_cell_index, midpoint, normalized_right, depth + 1)

    for source_cell_index in range(len(tube.profile_cells)):
        check_leaf(source_cell_index, Fraction(0), Fraction(1), 0)

    for left, right in zip(accepted, accepted[1:]):
        if left.jet.radius.upper != right.jet.radius.lower:
            raise ValueError("accepted exact-solution Barta leaves are not contiguous")
    if (
        not accepted
        or accepted[0].jet.radius.lower != tube.origin_cutoff
        or accepted[-1].jet.radius.upper != tube.wall_radius
    ):
        raise ValueError("accepted exact-solution Barta leaves do not cover the domain")
    return ValidatedSkyrmionExactTubeBartaBound(
        certificate_id=tube.certificate_id,
        origin_cutoff=tube.origin_cutoff,
        wall_radius=tube.wall_radius,
        declared_lower_bound=declared,
        recomputed_lower_bound=min(cell.quotient.lower for cell in accepted),
        maximum_depth_used=max(cell.depth for cell in accepted),
        cells=tuple(accepted),
    )


def validate_skyrmion_regular_origin_barta(
    origin: ValidatedSkyrmionOriginFamily,
    *,
    declared_lower_bound: Fraction = Fraction(1),
    kernel_terms: int = 20,
    trigonometric_terms: int = 24,
) -> ValidatedSkyrmionOriginBartaBound:
    """Validate ``Lv/v`` at the origin without separately ranging ``x^-2``."""

    if not isinstance(origin, ValidatedSkyrmionOriginFamily):
        raise TypeError("origin must be a validated origin family")
    declared = _fraction("declared_lower_bound", declared_lower_bound)
    if declared <= 0:
        raise ValueError("declared_lower_bound must be positive")
    terms = _positive_integer("kernel_terms", kernel_terms)
    trig_terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    if origin.contraction_bound >= 1 or (
        origin.residual_bound
        + origin.contraction_bound * origin.remainder_radius
        > origin.remainder_radius
    ):
        raise ValueError("origin family does not carry a closed contraction proof")

    cutoff = origin.cutoff
    radius = RationalInterval(Fraction(0), cutoff)
    time = RationalInterval(Fraction(0), cutoff**2)
    remainder = RationalInterval(
        -origin.remainder_radius,
        origin.remainder_radius,
    )
    momentum = (
        origin.shooting_slopes
        + origin.cubic_coefficient.scale(-3) * time
        + remainder * time.power(2)
    )
    profile_rate = (
        origin.shooting_slopes
        - origin.cubic_coefficient * time
        + remainder.scale(Fraction(1, 5)) * time.power(2)
    )
    if profile_rate.lower <= 0 or momentum.lower <= 0:
        raise ValueError("origin family does not preserve the regular positive branch")

    kernel_argument = time * profile_rate.power(2)
    sinc = _entire_even_kernel_interval(
        kernel_argument,
        scale_squared=1,
        derivative_order=0,
        terms=terms,
    )
    sinc_twice = _entire_even_kernel_interval(
        kernel_argument,
        scale_squared=4,
        derivative_order=0,
        terms=terms,
    )
    sine_rate = profile_rate * sinc
    double_sine_rate = profile_rate * sinc_twice
    sine_rate_squared = sine_rate.power(2)
    denominator_factor = RationalInterval.point(1) + sine_rate_squared.scale(8)
    angular_factor = RationalInterval.point(1) + sine_rate_squared.scale(4)
    cosine_twice = RationalInterval.point(1) - (
        time * sine_rate_squared
    ).scale(2)
    profile_angle = radius * profile_rate
    cosine_profile_angle = cos_center_lipschitz_interval(
        profile_angle,
        terms=trig_terms,
    )
    lapse = RationalInterval(1 - origin.curvature * cutoff**2, 1)

    principal = lapse * time * denominator_factor
    principal_derivative = radius * (
        (time * denominator_factor).scale(-2 * origin.curvature)
        + lapse
        * (RationalInterval.point(2) + (double_sine_rate * momentum).scale(16))
    )
    potential = (
        double_sine_rate.power(2).scale(16)
        + (angular_factor * cosine_twice).scale(2)
        - (time * cosine_profile_angle).scale(origin.pion_mass_squared)
        - (
            angular_factor * double_sine_rate.power(2) / denominator_factor
        ).scale(32)
        + (
            time
            * sine_rate
            * double_sine_rate
            / denominator_factor
        ).scale(16 * origin.pion_mass_squared)
        + (
            lapse * double_sine_rate * momentum / denominator_factor
        ).scale(32)
        + lapse
        * (
            cosine_twice.scale(-8)
            + (double_sine_rate.power(2) / denominator_factor).scale(128)
        )
        * momentum.power(2)
    )
    coefficients = SkyrmionJacobiCoefficientBox(
        principal=principal,
        principal_derivative=principal_derivative,
        potential=potential,
    )
    z = radius - Fraction(33, 16)
    witness_denominator = z.power(2) + 4
    quotient = (
        potential
        + z * principal_derivative * 2 / witness_denominator
        + principal
        * (RationalInterval.point(8) - z.power(2).scale(6))
        / witness_denominator.power(2)
    )
    if quotient.lower < declared:
        raise ValueError("regular-origin Barta target is not verified")
    return ValidatedSkyrmionOriginBartaBound(
        radius=radius,
        coefficients=coefficients,
        quotient=quotient,
        declared_lower_bound=declared,
        regular_mode_boundary_term_vanishes=True,
    )


def validate_skyrmion_fixed_wall_radial_gap(
    tube: ValidatedSkyrmionSharpProfileTube,
    origin: ValidatedSkyrmionOriginFamily,
    *,
    declared_lower_bound: Fraction = Fraction(1),
    maximum_refinement_depth: int = 6,
) -> ValidatedSkyrmionFixedWallRadialGap:
    """Certify the physical regular-origin-to-fixed-wall radial mode gap."""

    if (
        origin.shooting_slopes != tube.shooting_slope_interval
        or origin.cutoff != tube.origin_cutoff
        or origin.pion_mass_squared != tube.pion_mass_squared
        or origin.curvature != tube.curvature
        or origin.remainder_radius != tube.origin_remainder_radius
    ):
        raise ValueError("origin family and positive-radius Newton tube do not match")
    positive = validate_skyrmion_exact_solution_tube_barta(
        tube,
        declared_lower_bound=declared_lower_bound,
        maximum_refinement_depth=maximum_refinement_depth,
    )
    origin_bound = validate_skyrmion_regular_origin_barta(
        origin,
        declared_lower_bound=declared_lower_bound,
    )
    wall_lapse = Fraction(1) - tube.curvature * tube.wall_radius**2
    if wall_lapse <= 0:
        raise ValueError("fixed wall must lie strictly inside the static-patch horizon")
    weight_upper = (tube.wall_radius**2 + 8) / wall_lapse
    alpha = _fraction("declared_lower_bound", declared_lower_bound)
    return ValidatedSkyrmionFixedWallRadialGap(
        certificate_id=tube.certificate_id,
        static_form_gap=alpha,
        kinetic_weight_upper_bound=weight_upper,
        dimensionless_frequency_squared_lower_bound=alpha / weight_upper,
        positive_radius=positive,
        origin=origin_bound,
        fixed_wall_dirichlet_boundary_term_vanishes=True,
        conclusion_scope=(
            "Full physical regular-origin-to-fixed-wall l=0 profile fluctuation "
            "gap. The wall is ideal and nondynamical; membrane, anchor, "
            "nonspherical, and rotational collective channels are not included."
        ),
    )
