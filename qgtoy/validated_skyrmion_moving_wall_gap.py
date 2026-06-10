"""Validated radial gap for the Skyrmion coupled to a spherical membrane.

The moving ideal-mirror condition identifies the membrane displacement with
the field trace.  A positive Barta witness with a compatible wall logarithmic
derivative then controls the bulk and membrane kinetic terms directly.  This
avoids introducing an uncertified static-branch curvature or branch tangent.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_interval import RationalInterval
from .validated_skyrmion_bvp import (
    SkyrmionJacobiCoefficientBox,
    SkyrmionJetBox,
    skyrmion_jacobi_coefficient_box,
)
from .validated_skyrmion_origin import ValidatedSkyrmionOriginFamily
from .validated_skyrmion_radial_gap import (
    validate_skyrmion_regular_origin_barta,
)
from .validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpProfileTube,
    _endpoint_family_jet,
)


@dataclass(frozen=True)
class ValidatedSkyrmionMovingWallBartaCell:
    """One accepted exact-solution leaf for the moving-wall witness."""

    source_cell_index: int
    depth: int
    normalized_left: Fraction
    normalized_right: Fraction
    jet: SkyrmionJetBox
    coefficients: SkyrmionJacobiCoefficientBox
    quotient: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionMovingWallBartaBound:
    """Positive-radius Barta replay for a rational Lorentzian witness."""

    certificate_id: str
    witness_center: Fraction
    witness_width_squared: Fraction
    declared_lower_bound: Fraction
    recomputed_lower_bound: Fraction
    maximum_depth_used: int
    cells: tuple[ValidatedSkyrmionMovingWallBartaCell, ...]


@dataclass(frozen=True)
class ValidatedSkyrmionMovingWallOriginBound:
    """Cancellation-preserving origin quotient for the same witness."""

    radius: RationalInterval
    coefficients: SkyrmionJacobiCoefficientBox
    quotient: RationalInterval
    declared_lower_bound: Fraction
    regular_boundary_term_vanishes: bool


@dataclass(frozen=True)
class SkyrmionYoungLaplaceCoefficients:
    """Wall coefficients after eliminating the equilibrium tension."""

    compactness: Fraction
    lapse_at_wall: Fraction
    normalized_wall_mass_per_slope_squared: Fraction
    normalized_boundary_stiffness_per_slope_squared: Fraction
    jacobi_principal_at_wall: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionMovingWallRadialGap:
    """Full regular-origin moving-membrane radial frequency certificate."""

    certificate_id: str
    witness_center: Fraction
    witness_width_squared: Fraction
    bulk_form_lower_bound: Fraction
    bulk_kinetic_weight_upper_bound: Fraction
    boundary_form_lower_bound: Fraction
    boundary_kinetic_weight: Fraction
    dimensionless_frequency_squared_lower_bound: Fraction
    positive_radius: ValidatedSkyrmionMovingWallBartaBound
    origin: ValidatedSkyrmionMovingWallOriginBound
    young_laplace: SkyrmionYoungLaplaceCoefficients
    conclusion_scope: str


def _fraction(name: str, value: Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def skyrmion_lorentzian_barta_quotient(
    coefficients: SkyrmionJacobiCoefficientBox,
    radius: RationalInterval,
    *,
    center: Fraction,
    width_squared: Fraction,
) -> RationalInterval:
    """Return ``Lv/v`` for ``v=1/((x-center)^2+width_squared)``."""

    if not isinstance(coefficients, SkyrmionJacobiCoefficientBox):
        raise TypeError("coefficients must be a SkyrmionJacobiCoefficientBox")
    if not isinstance(radius, RationalInterval):
        raise TypeError("radius must be a RationalInterval")
    center_value = _fraction("center", center)
    width = _fraction("width_squared", width_squared)
    if width <= 0:
        raise ValueError("width_squared must be positive")
    z = radius - center_value
    denominator = z.power(2) + width
    return (
        coefficients.potential
        + z * coefficients.principal_derivative * 2 / denominator
        + coefficients.principal
        * (RationalInterval.point(2 * width) - z.power(2).scale(6))
        / denominator.power(2)
    )


def validate_skyrmion_moving_wall_positive_radius_barta(
    tube: ValidatedSkyrmionSharpProfileTube,
    *,
    center: Fraction = Fraction(9, 4),
    width_squared: Fraction = Fraction(8),
    declared_lower_bound: Fraction = Fraction(1, 100),
    maximum_refinement_depth: int = 7,
    trigonometric_terms: int = 24,
) -> ValidatedSkyrmionMovingWallBartaBound:
    """Replay the moving-wall Barta witness through the exact Newton tube."""

    if not isinstance(tube, ValidatedSkyrmionSharpProfileTube):
        raise TypeError("tube must be a validated sharp profile tube")
    center_value = _fraction("center", center)
    width = _fraction("width_squared", width_squared)
    declared = _fraction("declared_lower_bound", declared_lower_bound)
    depth_limit = _positive_integer(
        "maximum_refinement_depth", maximum_refinement_depth
    )
    terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    if width <= 0 or declared <= 0:
        raise ValueError("witness width and declared lower bound must be positive")

    accepted: list[ValidatedSkyrmionMovingWallBartaCell] = []

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
            + RationalInterval(
                -parent.profile_error_radius,
                parent.profile_error_radius,
            ),
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
            or not jet.derivative.is_subset_of(
                parent.archived_tube_jet.derivative
            )
            or not jet.second_derivative.is_subset_of(
                parent.archived_tube_jet.second_derivative
            )
        ):
            raise ValueError("refined Barta jet escaped its authenticated parent")
        coefficients = skyrmion_jacobi_coefficient_box(
            jet,
            pion_mass_squared=tube.pion_mass_squared,
            curvature=tube.curvature,
            trigonometric_terms=terms,
        )
        quotient = skyrmion_lorentzian_barta_quotient(
            coefficients,
            jet.radius,
            center=center_value,
            width_squared=width,
        )
        if coefficients.principal.lower > 0 and quotient.lower >= declared:
            accepted.append(
                ValidatedSkyrmionMovingWallBartaCell(
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
                "moving-wall Barta target failed at maximum refinement depth"
            )
        midpoint = (normalized_left + normalized_right) / 2
        check_leaf(source_cell_index, normalized_left, midpoint, depth + 1)
        check_leaf(source_cell_index, midpoint, normalized_right, depth + 1)

    for source_cell_index in range(len(tube.profile_cells)):
        check_leaf(source_cell_index, Fraction(0), Fraction(1), 0)

    if not accepted:
        raise ValueError("moving-wall Barta replay accepted no cells")
    for left, right in zip(accepted, accepted[1:]):
        if left.jet.radius.upper != right.jet.radius.lower:
            raise ValueError("moving-wall Barta leaves are not contiguous")
    if (
        accepted[0].jet.radius.lower != tube.origin_cutoff
        or accepted[-1].jet.radius.upper != tube.wall_radius
    ):
        raise ValueError("moving-wall Barta leaves do not cover the domain")
    return ValidatedSkyrmionMovingWallBartaBound(
        certificate_id=tube.certificate_id,
        witness_center=center_value,
        witness_width_squared=width,
        declared_lower_bound=declared,
        recomputed_lower_bound=min(cell.quotient.lower for cell in accepted),
        maximum_depth_used=max(cell.depth for cell in accepted),
        cells=tuple(accepted),
    )


def validate_skyrmion_moving_wall_origin_barta(
    origin: ValidatedSkyrmionOriginFamily,
    *,
    center: Fraction = Fraction(9, 4),
    width_squared: Fraction = Fraction(8),
    declared_lower_bound: Fraction = Fraction(1, 100),
) -> ValidatedSkyrmionMovingWallOriginBound:
    """Evaluate the moving-wall witness on the regular-origin coefficient box."""

    declared = _fraction("declared_lower_bound", declared_lower_bound)
    if declared <= 0:
        raise ValueError("declared_lower_bound must be positive")
    # This existing validator constructs P, P', and Q with every apparent
    # inverse power of x cancelled before interval evaluation.
    regular = validate_skyrmion_regular_origin_barta(origin)
    quotient = skyrmion_lorentzian_barta_quotient(
        regular.coefficients,
        regular.radius,
        center=center,
        width_squared=width_squared,
    )
    if quotient.lower < declared:
        raise ValueError("moving-wall origin Barta target is not verified")
    return ValidatedSkyrmionMovingWallOriginBound(
        radius=regular.radius,
        coefficients=regular.coefficients,
        quotient=quotient,
        declared_lower_bound=declared,
        regular_boundary_term_vanishes=True,
    )


def skyrmion_young_laplace_coefficients(
    *,
    wall_radius: Fraction,
    curvature: Fraction,
) -> SkyrmionYoungLaplaceCoefficients:
    """Eliminate membrane tension using exact spherical force balance."""

    radius = _fraction("wall_radius", wall_radius)
    kappa = _fraction("curvature", curvature)
    if radius <= 0 or kappa < 0:
        raise ValueError("wall radius must be positive and curvature nonnegative")
    compactness = kappa * radius**2
    lapse = 1 - compactness
    denominator = 2 - 3 * compactness
    if lapse <= 0 or denominator <= 0:
        raise ValueError("positive-tension wall equilibrium is unavailable")
    wall_mass = radius**3 / (2 * denominator)
    boundary_stiffness = radius * (1 - 2 * compactness) + (
        radius
        * (2 - 9 * compactness + 6 * compactness**2)
        / (2 * denominator)
    )
    return SkyrmionYoungLaplaceCoefficients(
        compactness=compactness,
        lapse_at_wall=lapse,
        normalized_wall_mass_per_slope_squared=wall_mass,
        normalized_boundary_stiffness_per_slope_squared=boundary_stiffness,
        jacobi_principal_at_wall=lapse * radius**2,
    )


def validate_skyrmion_moving_wall_radial_gap(
    tube: ValidatedSkyrmionSharpProfileTube,
    origin: ValidatedSkyrmionOriginFamily,
    *,
    center: Fraction = Fraction(9, 4),
    width_squared: Fraction = Fraction(8),
    declared_bulk_lower_bound: Fraction = Fraction(1, 100),
    declared_frequency_squared_lower_bound: Fraction = Fraction(1, 2500),
    maximum_refinement_depth: int = 7,
) -> ValidatedSkyrmionMovingWallRadialGap:
    """Certify the coupled field-membrane ``l=0`` normal-mode gap."""

    if (
        origin.shooting_slopes != tube.shooting_slope_interval
        or origin.cutoff != tube.origin_cutoff
        or origin.pion_mass_squared != tube.pion_mass_squared
        or origin.curvature != tube.curvature
        or origin.remainder_radius != tube.origin_remainder_radius
    ):
        raise ValueError("origin family and positive-radius Newton tube do not match")
    bulk_lower = _fraction(
        "declared_bulk_lower_bound", declared_bulk_lower_bound
    )
    frequency_lower = _fraction(
        "declared_frequency_squared_lower_bound",
        declared_frequency_squared_lower_bound,
    )
    if bulk_lower <= 0 or frequency_lower <= 0:
        raise ValueError("declared lower bounds must be positive")
    geometry = skyrmion_young_laplace_coefficients(
        wall_radius=tube.wall_radius,
        curvature=tube.curvature,
    )
    center_value = _fraction("center", center)
    width = _fraction("width_squared", width_squared)
    wall_offset = tube.wall_radius - center_value
    witness_log_derivative = -2 * wall_offset / (wall_offset**2 + width)
    boundary_lower = (
        geometry.normalized_boundary_stiffness_per_slope_squared
        + geometry.jacobi_principal_at_wall * witness_log_derivative
    )
    if boundary_lower <= 0:
        raise ValueError("moving-wall witness has a nonpositive boundary term")
    bulk_weight = (tube.wall_radius**2 + 8) / geometry.lapse_at_wall
    derived_frequency_lower = min(
        bulk_lower / bulk_weight,
        boundary_lower
        / geometry.normalized_wall_mass_per_slope_squared,
    )
    if derived_frequency_lower < frequency_lower:
        raise ValueError("declared moving-wall frequency lower bound is not verified")
    positive = validate_skyrmion_moving_wall_positive_radius_barta(
        tube,
        center=center_value,
        width_squared=width,
        declared_lower_bound=bulk_lower,
        maximum_refinement_depth=maximum_refinement_depth,
    )
    origin_bound = validate_skyrmion_moving_wall_origin_barta(
        origin,
        center=center_value,
        width_squared=width,
        declared_lower_bound=bulk_lower,
    )
    return ValidatedSkyrmionMovingWallRadialGap(
        certificate_id=tube.certificate_id,
        witness_center=center_value,
        witness_width_squared=width,
        bulk_form_lower_bound=bulk_lower,
        bulk_kinetic_weight_upper_bound=bulk_weight,
        boundary_form_lower_bound=boundary_lower,
        boundary_kinetic_weight=(
            geometry.normalized_wall_mass_per_slope_squared
        ),
        dimensionless_frequency_squared_lower_bound=frequency_lower,
        positive_radius=positive,
        origin=origin_bound,
        young_laplace=geometry,
        conclusion_scope=(
            "Full regular-origin coupled l=0 profile-membrane fluctuation gap "
            "for a positive-tension spherical Nambu-Goto wall in static "
            "Young-Laplace equilibrium. Anchor, nonspherical membrane/profile, "
            "and rotational collective channels are excluded."
        ),
    )
