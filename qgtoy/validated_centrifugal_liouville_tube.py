"""Adaptive Liouville-minor validation over a certified profile tube."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .validated_centrifugal_liouville_taylor import (
    ValidatedCentrifugalLiouvilleTaylorCell,
    centrifugal_liouville_taylor_cell,
)
from .validated_skyrmion_bvp import SkyrmionPolynomialCell


@dataclass(frozen=True)
class CentrifugalProfileTubeRadii:
    profile: Fraction
    derivative: Fraction
    second_derivative: Fraction

    def __post_init__(self) -> None:
        if min(self.profile, self.derivative, self.second_derivative) < 0:
            raise ValueError("profile-tube radii must be nonnegative")


@dataclass(frozen=True)
class ValidatedCentrifugalLiouvilleOuterTube:
    first_source_cell_index: int
    source_cell_count: int
    validation_cells: tuple[ValidatedCentrifugalLiouvilleTaylorCell, ...]
    target_lower_bound: Fraction
    minimum_principal_radial: Fraction
    minimum_principal_tangential: Fraction
    minimum_scaled_first_minor: Fraction
    minimum_scaled_second_minor: Fraction
    minimum_scaled_determinant: Fraction
    maximum_refinement_depth: int
    maximum_refinement_depth_used: int
    coercivity_verified: bool
    conclusion_scope: str


def validate_centrifugal_liouville_outer_tube(
    profile_cells: tuple[SkyrmionPolynomialCell, ...],
    tube_radii: tuple[CentrifugalProfileTubeRadii, ...],
    *,
    first_source_cell_index: int,
    target_lower_bound: Fraction = Fraction(1, 100),
    maximum_refinement_depth: int = 4,
    degree_limit: int = 8,
    rounding_denominator: int = 10**16,
    trigonometric_terms: int = 5,
) -> ValidatedCentrifugalLiouvilleOuterTube:
    """Validate a uniform C2 tube outside a separately handled origin patch."""
    if not profile_cells or len(profile_cells) != len(tube_radii):
        raise ValueError("profile cells and tube radii must be nonempty and aligned")
    if not 0 <= first_source_cell_index < len(profile_cells):
        raise ValueError("first_source_cell_index is outside the profile partition")
    if isinstance(maximum_refinement_depth, bool) or maximum_refinement_depth < 0:
        raise ValueError("maximum_refinement_depth must be nonnegative")
    if target_lower_bound <= 0:
        raise ValueError("target_lower_bound must be positive")
    for index, cell in enumerate(profile_cells):
        if not isinstance(cell, SkyrmionPolynomialCell):
            raise TypeError("profile_cells must contain SkyrmionPolynomialCell values")
        if index and profile_cells[index - 1].radius.upper != cell.radius.lower:
            raise ValueError("profile cells must form a contiguous partition")

    validation_cells: list[ValidatedCentrifugalLiouvilleTaylorCell] = []
    maximum_depth_used = 0

    def validate_subcell(
        source_cell_index: int,
        left: Fraction,
        right: Fraction,
        depth: int,
    ) -> None:
        nonlocal maximum_depth_used
        radii = tube_radii[source_cell_index]
        result = centrifugal_liouville_taylor_cell(
            profile_cells[source_cell_index],
            left,
            right,
            source_cell_index=source_cell_index,
            profile_error_radius=radii.profile,
            derivative_error_radius=radii.derivative,
            second_derivative_error_radius=radii.second_derivative,
            target_lower_bound=target_lower_bound,
            degree_limit=degree_limit,
            rounding_denominator=rounding_denominator,
            trigonometric_terms=trigonometric_terms,
        )
        maximum_depth_used = max(maximum_depth_used, depth)
        if result.principal_positive and result.shifted_potential_positive:
            validation_cells.append(result)
            return
        if depth >= maximum_refinement_depth:
            raise ValueError(
                "tube Liouville validation failed on profile cell "
                f"{source_cell_index} subcell [{left}, {right}]"
            )
        midpoint = (left + right) / 2
        validate_subcell(source_cell_index, left, midpoint, depth + 1)
        validate_subcell(source_cell_index, midpoint, right, depth + 1)

    for source_cell_index in range(first_source_cell_index, len(profile_cells)):
        validate_subcell(source_cell_index, Fraction(0), Fraction(1), 0)

    cells = tuple(validation_cells)
    return ValidatedCentrifugalLiouvilleOuterTube(
        first_source_cell_index=first_source_cell_index,
        source_cell_count=len(profile_cells) - first_source_cell_index,
        validation_cells=cells,
        target_lower_bound=target_lower_bound,
        minimum_principal_radial=min(cell.principal_radial.lower for cell in cells),
        minimum_principal_tangential=min(
            cell.principal_tangential.lower for cell in cells
        ),
        minimum_scaled_first_minor=min(
            cell.scaled_first_minor.lower for cell in cells
        ),
        minimum_scaled_second_minor=min(
            cell.scaled_second_minor.lower for cell in cells
        ),
        minimum_scaled_determinant=min(
            cell.scaled_determinant.lower for cell in cells
        ),
        maximum_refinement_depth=maximum_refinement_depth,
        maximum_refinement_depth_used=maximum_depth_used,
        coercivity_verified=True,
        conclusion_scope=(
            "the supplied C2 profile tube satisfies the completed Liouville "
            f"potential bound W_K >= {target_lower_bound} I outside the "
            "separately certified origin interval"
        ),
    )
