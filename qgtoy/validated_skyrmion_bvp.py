"""Conditional exact-rational checks for the Skyrmion Jacobi operator.

For a positive-radius profile jet ``(x, F, F', F'')``, the linearization of

    (P F')' = B,

with ``P=N(x^2+8 sin(F)^2)`` can be written as ``-D R = L``, where

    L v = -(P v')' + Q v,
    Q = partial_F B - (8 N sin(2F) F')'.

The routines below enclose ``P``, its total profile derivative ``P'``, ``Q``,
and the Barta quotient for one fixed positive witness.  Independent jet-box
checks infer no common profile or coverage.  A separate adaptive routine takes
an exact contiguous globally ``C2`` polynomial spline, recomputes its jet boxes,
and proves coverage for that spline only; neither route proves a nearby
nonlinear boundary-value solution.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from math import comb, factorial

from .validated_interval import (
    RationalInterval,
    RationalPolynomial,
    cos_fraction_interval,
    cos_center_lipschitz_interval,
    pi_machin_interval,
    sin_fraction_interval,
    sin_center_lipschitz_interval,
)
from .validated_skyrmion_origin import (
    ValidatedSkyrmionOriginFamily,
    ValidatedSkyrmionOriginQuinticBranchIdentification,
    ValidatedSkyrmionOriginSecondSensitivity,
)


def _nonnegative_fraction(name: str, value: Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    fraction = Fraction(value)
    if fraction < 0:
        raise ValueError(f"{name} must be nonnegative")
    return fraction


def _fraction(name: str, value: Fraction) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be an integer or Fraction")
    return Fraction(value)


def _upward_round_fraction(value: Fraction, denominator: int) -> Fraction:
    """Round a rational upward to a fixed positive denominator."""

    if isinstance(denominator, bool) or not isinstance(denominator, int):
        raise TypeError("rounding denominator must be an integer")
    if denominator <= 0:
        raise ValueError("rounding denominator must be positive")
    rational = Fraction(value)
    scaled_ceiling = -((-rational.numerator * denominator) // rational.denominator)
    return Fraction(scaled_ceiling, denominator)


def _outward_round_interval(
    value: RationalInterval,
    denominator: int,
) -> RationalInterval:
    """Enclose an interval on a fixed rational grid."""

    if not isinstance(value, RationalInterval):
        raise TypeError("value must be a RationalInterval")
    lower_scaled = value.lower.numerator * denominator // value.lower.denominator
    return RationalInterval(
        Fraction(lower_scaled, denominator),
        _upward_round_fraction(value.upper, denominator),
    )


def _downward_decimal(value: Fraction, *, places: int = 18) -> str:
    """Format a certified decimal lower bound without printing huge integers."""
    scale = 10**places
    scaled = value.numerator * scale // value.denominator
    sign = "-" if scaled < 0 else ""
    integer, fractional = divmod(abs(scaled), scale)
    return f"{sign}{integer}.{fractional:0{places}d}"


@dataclass(frozen=True)
class SkyrmionJetBox:
    """Independent interval enclosure of ``(x,F,F',F'')`` on one cell."""

    radius: RationalInterval
    profile: RationalInterval
    derivative: RationalInterval
    second_derivative: RationalInterval


@dataclass(frozen=True)
class SkyrmionJacobiCoefficientBox:
    """Trusted coefficient enclosure recomputed from one profile jet box."""

    principal: RationalInterval
    principal_derivative: RationalInterval
    potential: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionBartaCell:
    """One checked conditional Barta cell."""

    jet: SkyrmionJetBox
    coefficients: SkyrmionJacobiCoefficientBox
    quotient: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionBartaBound:
    """Recomputed lower bound over the union of supplied independent cells."""

    cells: tuple[ValidatedSkyrmionBartaCell, ...]
    declared_lower_bound: Fraction
    recomputed_lower_bound: Fraction


@dataclass(frozen=True)
class SkyrmionPolynomialCell:
    """One exact normalized-coordinate profile polynomial on a radius cell."""

    radius: RationalInterval
    profile_polynomial: RationalPolynomial


@dataclass(frozen=True)
class ValidatedSkyrmionPolynomialBartaBound:
    """Adaptive Barta validation for one contiguous globally C2 spline."""

    profile_cells: tuple[SkyrmionPolynomialCell, ...]
    pion_mass_squared: Fraction
    curvature: Fraction
    cells: tuple[ValidatedSkyrmionBartaCell, ...]
    declared_lower_bound: Fraction
    recomputed_lower_bound: Fraction
    source_cell_count: int
    initial_subdivisions: int
    maximum_refinement_depth: int
    maximum_refinement_depth_used: int


@dataclass(frozen=True)
class ValidatedSkyrmionSchurResidualCell:
    """One exact-interval residual box for the lifted auxiliary family."""

    source_cell_index: int
    radius: RationalInterval
    auxiliary: RationalInterval
    derivative: RationalInterval
    second_derivative: RationalInterval
    coefficients: SkyrmionJacobiCoefficientBox
    residual: RationalInterval
    refinement_depth: int


@dataclass(frozen=True)
class ValidatedSkyrmionNonlinearResidualCell:
    """One endpoint-corrected nonlinear residual enclosure."""

    source_cell_index: int
    radius: RationalInterval
    midpoint_profile: RationalInterval
    family_profile_jet: SkyrmionJetBox
    family_jacobi_coefficients: SkyrmionJacobiCoefficientBox
    midpoint_residual: RationalInterval
    family_residual_error_upper_bound: Fraction
    residual: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionEndpointCorrectedResidual:
    """Trusted residual of the origin/wall endpoint-corrected profile family."""

    profile_cells: tuple[SkyrmionPolynomialCell, ...]
    cells: tuple[ValidatedSkyrmionNonlinearResidualCell, ...]
    pion_mass_squared: Fraction
    curvature: Fraction
    phi_at_cutoff: RationalInterval
    gamma_at_cutoff: RationalInterval
    phi_sensitivity_at_cutoff: RationalInterval | None
    gamma_sensitivity_at_cutoff: RationalInterval | None
    left_value_correction: RationalInterval
    right_value_correction: Fraction
    boundary_slope_residual: RationalInterval
    residual_supremum_upper_bound: Fraction
    source_cell_count: int
    subdivisions_per_source_cell: int
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionPolynomialSchurBound:
    """Conditional Schur bound for one exact approximate profile/operator.

    The result concerns the Jacobi operator recomputed from ``profile_cells``
    and the interval family obtained by affinely lifting ``auxiliary_cells``.
    It does not prove that the profile spline solves the nonlinear BVP.
    """

    barta_validation: ValidatedSkyrmionPolynomialBartaBound
    residual_cells: tuple[ValidatedSkyrmionSchurResidualCell, ...]
    phi_b: RationalInterval
    gamma_b: RationalInterval
    affine_left_lift_coefficient: RationalInterval
    affine_left_lift_derivative: RationalInterval
    raw_schur_enclosure: RationalInterval
    residual_supremum_upper_bound: Fraction
    principal_lower_bound: Fraction
    potential_l1_upper_bound: Fraction
    inverse_c0_bound: Fraction
    boundary_derivative_c1_bound: Fraction
    boundary_derivative_error_bound: Fraction
    corrected_schur_enclosure: RationalInterval
    declared_schur_lower_bound: Fraction
    maximum_residual_refinement_depth: int
    maximum_residual_refinement_depth_used: int
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionRepresenterL1Cell:
    """One exact cell contribution to an approximate representer L1 bound."""

    source_cell_index: int
    radius: RationalInterval
    bernstein_range: RationalInterval
    l1_upper_bound: Fraction
    integrated_with_fixed_sign: bool


@dataclass(frozen=True)
class ValidatedSkyrmionDerivativeTraceBound:
    """Trusted derivative-trace bound for one approximate Dirichlet representer.

    The exact rational spline ``kappa_hat`` approximates the solution of
    ``L kappa=0`` with ``kappa(a)=1`` and ``kappa(c)=0``.  Barta coercivity and
    the recomputed residual turn its exact spline L1 bound into an L1 bound for
    the exact representer of the approximate-profile Jacobi operator.
    """

    barta_validation: ValidatedSkyrmionPolynomialBartaBound
    l1_cells: tuple[ValidatedSkyrmionRepresenterL1Cell, ...]
    residual_cells: tuple[ValidatedSkyrmionSchurResidualCell, ...]
    barta_witness_range: RationalInterval
    barta_witness_ratio_upper_bound: Fraction
    inverse_c0_bound: Fraction
    domain_length: Fraction
    approximate_representer_l1_upper_bound: Fraction
    residual_supremum_upper_bound: Fraction
    representer_error_l1_upper_bound: Fraction
    representer_l1_upper_bound: Fraction
    principal_left_enclosure: RationalInterval
    principal_left_lower_bound: Fraction
    recomputed_trace_upper_bound: Fraction
    declared_trace_upper_bound: Fraction
    maximum_residual_refinement_depth: int
    maximum_residual_refinement_depth_used: int
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionGraphResolventBounds:
    """Same-operator ``C0,C1,C2`` inverse bounds from one Barta partition."""

    barta_lower_bound: Fraction
    barta_witness_ratio_upper_bound: Fraction
    domain_length: Fraction
    principal_lower_bound: Fraction
    principal_derivative_supremum_upper_bound: Fraction
    potential_l1_upper_bound: Fraction
    potential_supremum_upper_bound: Fraction
    c0_upper_bound: Fraction
    c1_upper_bound: Fraction
    c2_upper_bound: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionGreenParametrixCell:
    """One cell of a certified two-solution Green parametrix."""

    source_cell_index: int
    radius: RationalInterval
    left_residual: RationalInterval
    right_residual: RationalInterval
    left_l1_upper_bound: Fraction
    right_l1_upper_bound: Fraction
    left_prefix_l1_upper_bound: Fraction
    right_suffix_l1_upper_bound: Fraction
    relative_wronskian_error_upper_bound: Fraction
    operator_defect_upper_bound: Fraction
    principal_lower_bound: Fraction
    approximate_c0_row_upper_bound: Fraction
    approximate_c1_row_upper_bound: Fraction
    approximate_c2_row_upper_bound: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionGreenResolventBounds:
    """Cellwise Green-parametrix bounds for the Dirichlet Jacobi inverse."""

    profile_cells: tuple[SkyrmionPolynomialCell, ...]
    left_fundamental_cells: tuple[SkyrmionPolynomialCell, ...]
    right_representer_cells: tuple[SkyrmionPolynomialCell, ...]
    pion_mass_squared: Fraction
    curvature: Fraction
    barta_validation: ValidatedSkyrmionPolynomialBartaBound
    cells: tuple[ValidatedSkyrmionGreenParametrixCell, ...]
    wronskian_normalization: Fraction
    initial_wronskian_enclosure: RationalInterval
    initial_wronskian_error_upper_bound: Fraction
    operator_defect_upper_bound: Fraction
    approximate_c0_upper_bound: Fraction
    approximate_c1_upper_bound: Fraction
    approximate_c2_upper_bound: Fraction
    c0_upper_bound: Fraction
    c1_upper_bound: Fraction
    c2_upper_bound: Fraction
    source_cell_count: int
    subdivisions_per_source_cell: int
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionAuxiliaryNormBounds:
    """Uniform lifted-auxiliary norms corrected to the exact Jacobi solution."""

    approximate_c0_upper_bound: Fraction
    approximate_c1_upper_bound: Fraction
    approximate_c2_upper_bound: Fraction
    residual_supremum_upper_bound: Fraction
    corrected_c0_upper_bound: Fraction
    corrected_c1_upper_bound: Fraction
    corrected_c2_upper_bound: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionTraceSharpenedSchurBound:
    """Conditional Schur bound corrected by a separately certified trace."""

    profile_cells: tuple[SkyrmionPolynomialCell, ...]
    auxiliary_cells: tuple[SkyrmionPolynomialCell, ...]
    pion_mass_squared: Fraction
    curvature: Fraction
    trace_validation: ValidatedSkyrmionDerivativeTraceBound
    graph_resolvent_bounds: (
        ValidatedSkyrmionGraphResolventBounds
        | ValidatedSkyrmionGreenResolventBounds
    )
    auxiliary_norm_bounds: ValidatedSkyrmionAuxiliaryNormBounds
    residual_cells: tuple[ValidatedSkyrmionSchurResidualCell, ...]
    phi_b: RationalInterval
    gamma_b: RationalInterval
    affine_left_lift_coefficient: RationalInterval
    affine_left_lift_derivative: RationalInterval
    raw_schur_enclosure: RationalInterval
    residual_supremum_upper_bound: Fraction
    derivative_trace_upper_bound: Fraction
    boundary_derivative_error_bound: Fraction
    corrected_schur_enclosure: RationalInterval
    declared_schur_lower_bound: Fraction
    maximum_residual_refinement_depth: int
    maximum_residual_refinement_depth_used: int
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionOperatorMismatchCell:
    """One coefficient-Lipschitz bound for ``A_Fbar-A_Fhat``."""

    source_cell_index: int
    radius: RationalInterval
    profile_correction_supremum_upper_bound: Fraction
    derivative_correction_supremum_upper_bound: Fraction
    principal_difference_upper_bound: Fraction
    principal_derivative_difference_upper_bound: Fraction
    potential_difference_upper_bound: Fraction
    graph_operator_mismatch_upper_bound: Fraction
    auxiliary_operator_mismatch_upper_bound: Fraction
    interior_operator_mismatch_upper_bound: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionAugmentedOperatorMismatch:
    """Approximate-inverse derivative mismatch for the augmented Newton map."""

    profile_cells: tuple[SkyrmionPolynomialCell, ...]
    cells: tuple[ValidatedSkyrmionOperatorMismatchCell, ...]
    pion_mass_squared: Fraction
    curvature: Fraction
    phi_at_cutoff: RationalInterval
    gamma_at_cutoff: RationalInterval
    phi_sensitivity_at_cutoff: RationalInterval
    gamma_sensitivity_at_cutoff: RationalInterval
    left_value_correction: RationalInterval
    right_value_correction: Fraction
    omega: Fraction
    scalar_weight: Fraction
    augmented_inverse_upper_bound: Fraction
    nonlinear_residual_supremum_upper_bound: Fraction
    nonlinear_residual_trace_upper_bound: Fraction
    boundary_slope_residual_absolute_upper_bound: Fraction
    newton_defect_upper_bound: Fraction
    interior_operator_mismatch_upper_bound: Fraction
    operator_mismatch_trace_upper_bound: Fraction
    z0_upper_bound: Fraction
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionNewtonTubeCell:
    """One cellwise nonlinear Hessian bound on an augmented Newton tube."""

    source_cell_index: int
    radius: RationalInterval
    tube_jet: SkyrmionJetBox
    local_graph_c0_upper_bound: Fraction
    local_graph_c1_upper_bound: Fraction
    local_graph_c2_upper_bound: Fraction
    local_auxiliary_c0_upper_bound: Fraction
    local_auxiliary_c1_upper_bound: Fraction
    local_auxiliary_c2_upper_bound: Fraction
    first_variation_c0_upper_bound: Fraction
    first_variation_c1_upper_bound: Fraction
    first_variation_c2_upper_bound: Fraction
    center_equation_forcing_upper_bound: Fraction
    direct_nonlinear_hessian_upper_bound: Fraction
    center_equation_hessian_upper_bound: Fraction
    nonlinear_hessian_upper_bound: Fraction
    affine_lift_jacobi_upper_bound: Fraction
    interior_augmented_hessian_upper_bound: Fraction


@dataclass(frozen=True)
class ValidatedSkyrmionAugmentedNewtonTubeBound:
    """Exact radii-polynomial diagnostic for the augmented Skyrmion BVP."""

    cells: tuple[ValidatedSkyrmionNewtonTubeCell, ...]
    pion_mass_squared: Fraction
    curvature: Fraction
    origin_cutoff: Fraction
    wall_radius: Fraction
    shooting_slope_interval: RationalInterval
    origin_remainder_radius: Fraction
    radius: Fraction
    omega: Fraction
    profile_second_sensitivity_upper_bound: Fraction
    derivative_second_sensitivity_upper_bound: Fraction
    first_variation_c0_upper_bound: Fraction
    first_variation_c1_upper_bound: Fraction
    first_variation_c2_upper_bound: Fraction
    profile_tube_c0_radius: Fraction
    profile_tube_c1_radius: Fraction
    profile_tube_c2_radius: Fraction
    interior_hessian_upper_bound: Fraction
    interior_hessian_trace_upper_bound: Fraction
    scalar_hessian_upper_bound: Fraction
    schur_composed_hessian_upper_bound: Fraction
    newton_defect_upper_bound: Fraction
    z0_upper_bound: Fraction
    radii_polynomial_upper_bound: Fraction
    contraction_upper_bound: Fraction
    self_map_verified: bool
    contraction_verified: bool
    conclusion_scope: str


@dataclass(frozen=True)
class ValidatedSkyrmionInertiaCell:
    """One interval contribution to the dimensionless rotor inertia."""

    source_cell_index: int
    radius: RationalInterval
    sine_squared: RationalInterval
    density_enclosure: RationalInterval
    integral_enclosure: RationalInterval


@dataclass(frozen=True)
class ValidatedSkyrmionNewtonPhysicalObservables:
    """Monotonicity, wall-slope, and inertia consequences of a closed tube."""

    origin_family: ValidatedSkyrmionOriginFamily
    newton_tube: ValidatedSkyrmionAugmentedNewtonTubeBound
    origin_momentum_enclosure: RationalInterval
    positive_radius_derivative_upper_bound: Fraction
    wall_slope_enclosure: RationalInterval
    inertia_cells: tuple[ValidatedSkyrmionInertiaCell, ...]
    origin_inertia_upper_bound: Fraction
    inertia_enclosure: RationalInterval
    strict_monotonicity_verified: bool
    negative_wall_slope_verified: bool
    positive_finite_inertia_verified: bool
    conclusion_scope: str


def _positive_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _nonnegative_integer(name: str, value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _affine_restrict_polynomial(
    polynomial: RationalPolynomial,
    center: Fraction,
    half_width: Fraction,
) -> RationalPolynomial:
    """Return the exact polynomial ``p(center+half_width*z)``."""
    shifted = polynomial.shift(center)
    return RationalPolynomial(
        tuple(
            coefficient * half_width**power
            for power, coefficient in enumerate(shifted.coefficients)
        )
    )


def _centered_polynomial_range(
    polynomial: RationalPolynomial,
    left: Fraction,
    right: Fraction,
) -> RationalInterval:
    center = (left + right) / 2
    restricted = _affine_restrict_polynomial(
        polynomial,
        center,
        (right - left) / 2,
    )
    return restricted.evaluate(RationalInterval(Fraction(-1), Fraction(1)))


def _polynomial_subcell_jet(
    cell: SkyrmionPolynomialCell,
    left: Fraction,
    right: Fraction,
) -> SkyrmionJetBox:
    width = cell.radius.width
    derivative = cell.profile_polynomial.derivative()
    second_derivative = derivative.derivative()
    return SkyrmionJetBox(
        radius=RationalInterval(
            cell.radius.lower + width * left,
            cell.radius.lower + width * right,
        ),
        profile=_centered_polynomial_range(
            cell.profile_polynomial, left, right
        ),
        derivative=_centered_polynomial_range(
            derivative, left, right
        ).scale(1 / width),
        second_derivative=_centered_polynomial_range(
            second_derivative, left, right
        ).scale(1 / width**2),
    )


def _validate_globally_c2_polynomial_cells(
    cells: Sequence[SkyrmionPolynomialCell],
) -> None:
    for cell in cells:
        if not isinstance(cell, SkyrmionPolynomialCell):
            raise TypeError(
                "cells must contain only SkyrmionPolynomialCell values"
            )
        if cell.radius.lower <= 0 or cell.radius.width <= 0:
            raise ValueError("polynomial radius cells must be positive and nonempty")
        if not isinstance(cell.profile_polynomial, RationalPolynomial):
            raise TypeError("profile_polynomial must be a RationalPolynomial")
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("polynomial cells must be exactly contiguous")
        left_polynomial = left.profile_polynomial
        right_polynomial = right.profile_polynomial
        for derivative_order in range(3):
            if derivative_order:
                left_polynomial = left_polynomial.derivative()
                right_polynomial = right_polynomial.derivative()
            left_value = left_polynomial.evaluate(Fraction(1)).scale(
                1 / left.radius.width**derivative_order
            )
            right_value = right_polynomial.evaluate(Fraction(0)).scale(
                1 / right.radius.width**derivative_order
            )
            if left_value != right_value:
                raise ValueError("polynomial cells must join globally C2")


def _default_conditional_barta_cells() -> tuple[SkyrmionJetBox, ...]:
    """Return the packaged independent jet boxes near the limiting quotient."""
    denominator = 10_000_000

    def interval(lower: int, upper: int) -> RationalInterval:
        return RationalInterval(
            Fraction(lower, denominator),
            Fraction(upper, denominator),
        )

    return (
        SkyrmionJetBox(
            interval(8_700_000, 8_720_000),
            interval(18_495_680, 18_520_800),
            interval(-13_195_650, -13_187_290),
            interval(4_363_490, 4_364_360),
        ),
        SkyrmionJetBox(
            interval(8_720_000, 8_740_000),
            interval(18_469_310, 18_494_420),
            interval(-13_186_930, -13_178_560),
            interval(4_362_620, 4_363_530),
        ),
        SkyrmionJetBox(
            interval(8_740_000, 8_760_000),
            interval(18_442_950, 18_468_060),
            interval(-13_178_200, -13_169_840),
            interval(4_361_720, 4_362_660),
        ),
        SkyrmionJetBox(
            interval(8_760_000, 8_780_000),
            interval(18_416_620, 18_441_710),
            interval(-13_169_480, -13_161_110),
            interval(4_360_790, 4_361_760),
        ),
        SkyrmionJetBox(
            interval(8_780_000, 8_800_000),
            interval(18_390_300, 18_415_380),
            interval(-13_160_760, -13_152_390),
            interval(4_359_820, 4_360_820),
        ),
    )


def skyrmion_jacobi_coefficient_box(
    jet: SkyrmionJetBox,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> SkyrmionJacobiCoefficientBox:
    """Enclose ``P``, total ``P'``, and ``Q`` for ``L=-(P v')'+Qv``.

    No derivative or coefficient data are accepted from the caller.  The
    formulas are evaluated directly on the supplied exact-rational jet box.
    """
    if not isinstance(jet, SkyrmionJetBox):
        raise TypeError("jet must be a SkyrmionJetBox")
    if not all(
        isinstance(value, RationalInterval)
        for value in (
            jet.radius,
            jet.profile,
            jet.derivative,
            jet.second_derivative,
        )
    ):
        raise TypeError("all jet components must be RationalInterval values")
    if jet.radius.lower <= 0:
        raise ValueError("radius box must be strictly positive")
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)

    radius = jet.radius
    profile = jet.profile
    derivative = jet.derivative
    second_derivative = jet.second_derivative
    radius_squared = radius.power(2)
    lapse = RationalInterval.point(1) - radius_squared.scale(curvature_value)
    if lapse.lower <= 0:
        raise ValueError("radius box must lie strictly inside the horizon")
    lapse_derivative = radius.scale(-2 * curvature_value)

    sine = sin_center_lipschitz_interval(
        profile, terms=trigonometric_terms
    )
    cosine = cos_center_lipschitz_interval(
        profile, terms=trigonometric_terms
    )
    sine_twice = sin_center_lipschitz_interval(
        profile.scale(2), terms=trigonometric_terms
    )
    cosine_twice = cos_center_lipschitz_interval(
        profile.scale(2), terms=trigonometric_terms
    )
    sine_squared = sine.power(2)
    profile_factor = radius_squared + sine_squared.scale(8)

    principal = lapse * profile_factor
    principal_derivative = (
        lapse_derivative * profile_factor
        + lapse
        * (radius.scale(2) + sine_twice * derivative.scale(8))
    )

    # Q = partial_F B - d/dx(8 N sin(2F) F').  The displayed form has
    # already combined the two cos(2F) F'^2 contributions, reducing interval
    # dependency without changing the exact coefficient.
    potential = (
        sine_twice.power(2).scale(4) / radius_squared
        + (
            RationalInterval.point(1)
            + sine_squared.scale(4) / radius_squared
        )
        * cosine_twice.scale(2)
        - lapse * cosine_twice * derivative.power(2).scale(8)
        + radius_squared.scale(mass_squared) * cosine
        - lapse_derivative * sine_twice * derivative.scale(8)
        - lapse * sine_twice * second_derivative.scale(8)
    )
    return SkyrmionJacobiCoefficientBox(
        principal=principal,
        principal_derivative=principal_derivative,
        potential=potential,
    )


def skyrmion_barta_quotient_box(
    jet: SkyrmionJetBox,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> tuple[SkyrmionJacobiCoefficientBox, RationalInterval]:
    """Enclose ``L v/v`` for ``v=8/((x-33/16)^2+4)``."""
    coefficients = skyrmion_jacobi_coefficient_box(
        jet,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    z = jet.radius - Fraction(33, 16)
    denominator = z.power(2) + 4
    quotient = (
        coefficients.potential
        + z
        * coefficients.principal_derivative
        * 2
        / denominator
        + coefficients.principal
        * (RationalInterval.point(8) - z.power(2).scale(6))
        / denominator.power(2)
    )
    return coefficients, quotient


def validate_skyrmion_barta_cells(
    cells: Sequence[SkyrmionJetBox],
    declared_lower_bound: Fraction,
    *,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> ValidatedSkyrmionBartaBound:
    """Validate ellipticity and a declared Barta lower bound on all cells.

    Cells are intentionally treated independently: no contiguity, common
    solution, boundary condition, or interval coverage is inferred.
    """
    if not isinstance(cells, Sequence) or isinstance(cells, (str, bytes)):
        raise TypeError("cells must be a sequence of SkyrmionJetBox values")
    if not cells:
        raise ValueError("at least one jet cell is required")
    declared = _fraction("declared_lower_bound", declared_lower_bound)
    checked: list[ValidatedSkyrmionBartaCell] = []
    for jet in cells:
        if not isinstance(jet, SkyrmionJetBox):
            raise TypeError("cells must contain only SkyrmionJetBox values")
        coefficients, quotient = skyrmion_barta_quotient_box(
            jet,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
            trigonometric_terms=trigonometric_terms,
        )
        if coefficients.principal.lower <= 0:
            raise ValueError("Jacobi principal coefficient is not positive")
        if quotient.lower < declared:
            raise ValueError("declared Barta lower bound is not verified")
        checked.append(
            ValidatedSkyrmionBartaCell(
                jet=jet,
                coefficients=coefficients,
                quotient=quotient,
            )
        )
    recomputed = min(cell.quotient.lower for cell in checked)
    return ValidatedSkyrmionBartaBound(
        cells=tuple(checked),
        declared_lower_bound=declared,
        recomputed_lower_bound=recomputed,
    )


def validate_skyrmion_polynomial_barta_spline(
    cells: Sequence[SkyrmionPolynomialCell],
    declared_lower_bound: Fraction,
    *,
    initial_subdivisions: int = 4,
    maximum_refinement_depth: int = 3,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
) -> ValidatedSkyrmionPolynomialBartaBound:
    """Validate Barta coercivity for one exact contiguous globally C2 spline.

    The caller supplies only exact radius cells and normalized-coordinate
    profile polynomials.  This routine verifies all joins, recomputes every jet
    box, and bisects only quotient boxes that do not yet prove the declared
    lower bound.  The conclusion concerns this exact spline, not a nearby
    nonlinear BVP solution.
    """
    if not isinstance(cells, Sequence) or isinstance(cells, (str, bytes)):
        raise TypeError("cells must be a sequence of polynomial cells")
    if not cells:
        raise ValueError("at least one polynomial cell is required")
    subdivisions = _positive_integer(
        "initial_subdivisions", initial_subdivisions
    )
    depth_limit = _nonnegative_integer(
        "maximum_refinement_depth", maximum_refinement_depth
    )
    declared = _fraction("declared_lower_bound", declared_lower_bound)
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)
    _validate_globally_c2_polynomial_cells(cells)

    checked: list[ValidatedSkyrmionBartaCell] = []
    maximum_depth_used = 0
    for source_index, cell in enumerate(cells):
        pending = [
            (
                Fraction(index, subdivisions),
                Fraction(index + 1, subdivisions),
                0,
            )
            for index in reversed(range(subdivisions))
        ]
        while pending:
            left, right, depth = pending.pop()
            jet = _polynomial_subcell_jet(cell, left, right)
            coefficients, quotient = skyrmion_barta_quotient_box(
                jet,
                pion_mass_squared=mass_squared,
                curvature=curvature_value,
                trigonometric_terms=trigonometric_terms,
            )
            if coefficients.principal.lower <= 0:
                raise ValueError(
                    "Jacobi principal coefficient is not positive on the spline"
                )
            if quotient.lower < declared:
                if depth >= depth_limit:
                    raise ValueError(
                        "declared Barta lower bound is not verified for "
                        f"source cell {source_index} on normalized interval "
                        f"[{left},{right}]"
                    )
                midpoint = (left + right) / 2
                pending.append((midpoint, right, depth + 1))
                pending.append((left, midpoint, depth + 1))
                continue
            maximum_depth_used = max(maximum_depth_used, depth)
            checked.append(
                ValidatedSkyrmionBartaCell(
                    jet=jet,
                    coefficients=coefficients,
                    quotient=quotient,
                )
            )

    recomputed = min(cell.quotient.lower for cell in checked)
    return ValidatedSkyrmionPolynomialBartaBound(
        profile_cells=tuple(cells),
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        cells=tuple(checked),
        declared_lower_bound=declared,
        recomputed_lower_bound=recomputed,
        source_cell_count=len(cells),
        initial_subdivisions=subdivisions,
        maximum_refinement_depth=depth_limit,
        maximum_refinement_depth_used=maximum_depth_used,
    )


def _absolute_interval_upper(interval: RationalInterval) -> Fraction:
    return max(abs(interval.lower), abs(interval.upper))


IntervalPolynomial = tuple[RationalInterval, ...]


def _rational_polynomial_add(
    *polynomials: RationalPolynomial,
) -> RationalPolynomial:
    degree = max(polynomial.degree for polynomial in polynomials)
    coefficients = [Fraction(0)] * (degree + 1)
    for polynomial in polynomials:
        for index, coefficient in enumerate(polynomial.coefficients):
            coefficients[index] += coefficient
    return RationalPolynomial(tuple(coefficients))


def _rational_polynomial_scale(
    polynomial: RationalPolynomial,
    factor: Fraction,
) -> RationalPolynomial:
    return RationalPolynomial(
        tuple(Fraction(factor) * value for value in polynomial.coefficients)
    )


def _rational_polynomial_multiply(
    left: RationalPolynomial,
    right: RationalPolynomial,
) -> RationalPolynomial:
    coefficients = [Fraction(0)] * (left.degree + right.degree + 1)
    for left_index, left_value in enumerate(left.coefficients):
        for right_index, right_value in enumerate(right.coefficients):
            coefficients[left_index + right_index] += left_value * right_value
    return RationalPolynomial(tuple(coefficients))


def _rational_polynomial_power(
    polynomial: RationalPolynomial,
    exponent: int,
) -> RationalPolynomial:
    if exponent < 0:
        raise ValueError("polynomial exponent must be nonnegative")
    result = RationalPolynomial((Fraction(1),))
    base = polynomial
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = _rational_polynomial_multiply(result, base)
        remaining //= 2
        if remaining:
            base = _rational_polynomial_multiply(base, base)
    return result


def _interval_polynomial_from_rational(
    polynomial: RationalPolynomial,
) -> IntervalPolynomial:
    return tuple(
        RationalInterval.point(value) for value in polynomial.coefficients
    )


def _interval_polynomial_add(
    *polynomials: IntervalPolynomial,
) -> IntervalPolynomial:
    degree = max(len(polynomial) for polynomial in polynomials)
    coefficients = [RationalInterval.point(0) for _ in range(degree)]
    for polynomial in polynomials:
        for index, coefficient in enumerate(polynomial):
            coefficients[index] = coefficients[index] + coefficient
    while len(coefficients) > 1 and coefficients[-1] == RationalInterval.point(0):
        coefficients.pop()
    return tuple(coefficients)


def _interval_polynomial_scale(
    polynomial: IntervalPolynomial,
    factor: RationalInterval | Fraction,
) -> IntervalPolynomial:
    interval = (
        factor if isinstance(factor, RationalInterval) else RationalInterval.point(factor)
    )
    result = []
    for coefficient in polynomial:
        if coefficient.lower == coefficient.upper:
            result.append(interval.scale(coefficient.lower))
        elif interval.lower == interval.upper:
            result.append(coefficient.scale(interval.lower))
        else:
            result.append(coefficient * interval)
    return tuple(result)


def _interval_polynomial_multiply_rational(
    interval_polynomial: IntervalPolynomial,
    rational_polynomial: RationalPolynomial,
) -> IntervalPolynomial:
    degree = len(interval_polynomial) + rational_polynomial.degree
    lower_coefficients = [Fraction(0) for _ in range(degree)]
    upper_coefficients = [Fraction(0) for _ in range(degree)]
    for left_index, left_value in enumerate(interval_polynomial):
        for right_index, right_value in enumerate(
            rational_polynomial.coefficients
        ):
            target = left_index + right_index
            if right_value >= 0:
                lower_coefficients[target] += left_value.lower * right_value
                upper_coefficients[target] += left_value.upper * right_value
            else:
                lower_coefficients[target] += left_value.upper * right_value
                upper_coefficients[target] += left_value.lower * right_value
    return tuple(
        RationalInterval(lower, upper)
        for lower, upper in zip(lower_coefficients, upper_coefficients)
    )


def _interval_polynomial_bernstein_range(
    polynomial: IntervalPolynomial,
) -> RationalInterval:
    """Enclose an interval-coefficient polynomial on ``[-1,1]``.

    The affine substitution ``z=2t-1`` is performed coefficientwise, then the
    power coefficients on ``[0,1]`` are converted exactly to Bernstein form.
    Every admissible coefficient selection is enclosed because both transforms
    are linear and use outward interval arithmetic.
    """
    degree = len(polynomial) - 1
    shifted = [RationalInterval.point(0) for _ in range(degree + 1)]
    for source_power, source_coefficient in enumerate(polynomial):
        for target_power in range(source_power + 1):
            shifted[target_power] = shifted[target_power] + source_coefficient.scale(
                comb(source_power, target_power)
                * 2**target_power
                * (-1) ** (source_power - target_power)
            )
    bernstein = []
    for index in range(degree + 1):
        coefficient = RationalInterval.point(0)
        for power in range(index + 1):
            coefficient = coefficient + shifted[power].scale(
                Fraction(comb(index, power), comb(degree, power))
            )
        bernstein.append(coefficient)
    return RationalInterval(
        min(value.lower for value in bernstein),
        max(value.upper for value in bernstein),
    )


def _interval_polynomial_centered_range(
    polynomial: IntervalPolynomial,
) -> RationalInterval:
    """Enclose an interval-coefficient polynomial on ``[-1,1]`` linearly.

    Cancellation has already occurred in the monomial coefficients.  Even
    powers range over ``[0,1]`` and odd powers over ``[-1,1]``.  This enclosure
    is usually a little broader than the Bernstein hull, but avoids its
    quadratic exact-rational transform for the high-degree residual model.
    """
    result = polynomial[0]
    for power, coefficient in enumerate(polynomial[1:], start=1):
        monomial_range = (
            RationalInterval(Fraction(0), Fraction(1))
            if power % 2 == 0
            else RationalInterval(Fraction(-1), Fraction(1))
        )
        result = result + coefficient * monomial_range
    return result


def _rational_polynomial_bernstein_range(
    polynomial: RationalPolynomial,
) -> RationalInterval:
    return _interval_polynomial_bernstein_range(
        _interval_polynomial_from_rational(polynomial)
    )


def _normalized_polynomial_l1_upper_bound(
    polynomial: RationalPolynomial,
) -> tuple[RationalInterval, Fraction, bool]:
    """Bound ``integral_0^1 |p(t)| dt`` using an exact Bernstein sign test."""
    centered = _affine_restrict_polynomial(
        polynomial,
        Fraction(1, 2),
        Fraction(1, 2),
    )
    bernstein_range = _rational_polynomial_bernstein_range(centered)
    if bernstein_range.lower >= 0 or bernstein_range.upper <= 0:
        antiderivative = polynomial.integral()
        signed_integral = (
            antiderivative.evaluate(Fraction(1)).lower
            - antiderivative.evaluate(Fraction(0)).lower
        )
        return bernstein_range, abs(signed_integral), True
    return (
        bernstein_range,
        _absolute_interval_upper(bernstein_range),
        False,
    )


def _polynomial_subcell_l1_upper_bound(
    cell: SkyrmionPolynomialCell,
    left: Fraction,
    right: Fraction,
) -> Fraction:
    """Bound the physical ``L1`` norm of one spline on a normalized subcell."""
    restricted = _affine_restrict_polynomial(
        cell.profile_polynomial,
        left,
        right - left,
    )
    _, normalized_l1, _ = _normalized_polynomial_l1_upper_bound(restricted)
    return cell.radius.width * (right - left) * normalized_l1


def _trigonometric_polynomial_model(
    profile: RationalPolynomial,
    *,
    harmonic: int,
    sine: bool,
    center_terms: int,
    model_terms: int,
) -> tuple[IntervalPolynomial, Fraction]:
    """Return a centered Taylor model and uniform remainder on ``[-1,1]``."""
    center = profile.coefficients[0]
    delta_coefficients = list(profile.coefficients)
    delta_coefficients[0] = Fraction(0)
    delta = _rational_polynomial_scale(
        RationalPolynomial(tuple(delta_coefficients)), harmonic
    )
    delta_range = _rational_polynomial_bernstein_range(delta)
    delta_absolute_upper = _absolute_interval_upper(delta_range)

    sine_delta = RationalPolynomial((Fraction(0),))
    cosine_delta = RationalPolynomial((Fraction(0),))
    delta_squared = _rational_polynomial_power(delta, 2)
    even_power = RationalPolynomial((Fraction(1),))
    for index in range(model_terms):
        sine_delta = _rational_polynomial_add(
            sine_delta,
            _rational_polynomial_scale(
                _rational_polynomial_multiply(delta, even_power),
                Fraction((-1) ** index, factorial(2 * index + 1)),
            ),
        )
        cosine_delta = _rational_polynomial_add(
            cosine_delta,
            _rational_polynomial_scale(
                even_power,
                Fraction((-1) ** index, factorial(2 * index)),
            ),
        )
        even_power = _rational_polynomial_multiply(even_power, delta_squared)
    sine_tail = delta_absolute_upper ** (2 * model_terms + 1) / factorial(
        2 * model_terms + 1
    )
    cosine_tail = delta_absolute_upper ** (2 * model_terms) / factorial(
        2 * model_terms
    )

    center_argument = harmonic * center
    center_sine = sin_fraction_interval(center_argument, terms=center_terms)
    center_cosine = cos_fraction_interval(center_argument, terms=center_terms)
    center_sine = RationalInterval(
        max(Fraction(-1), center_sine.lower),
        min(Fraction(1), center_sine.upper),
    )
    center_cosine = RationalInterval(
        max(Fraction(-1), center_cosine.lower),
        min(Fraction(1), center_cosine.upper),
    )
    sine_delta_interval = _interval_polynomial_from_rational(sine_delta)
    cosine_delta_interval = _interval_polynomial_from_rational(cosine_delta)
    if sine:
        model = _interval_polynomial_add(
            _interval_polynomial_scale(cosine_delta_interval, center_sine),
            _interval_polynomial_scale(sine_delta_interval, center_cosine),
        )
        remainder = (
            _absolute_interval_upper(center_sine) * cosine_tail
            + _absolute_interval_upper(center_cosine) * sine_tail
        )
    else:
        model = _interval_polynomial_add(
            _interval_polynomial_scale(cosine_delta_interval, center_cosine),
            _interval_polynomial_scale(sine_delta_interval, -center_sine),
        )
        remainder = (
            _absolute_interval_upper(center_cosine) * cosine_tail
            + _absolute_interval_upper(center_sine) * sine_tail
        )
    return model, remainder


def _combined_trigonometric_models(
    profile: RationalPolynomial,
    *,
    trigonometric_terms: int,
    residual_taylor_terms: int,
) -> tuple[
    tuple[IntervalPolynomial, Fraction],
    tuple[IntervalPolynomial, Fraction],
    tuple[IntervalPolynomial, Fraction],
    tuple[IntervalPolynomial, Fraction],
]:
    return (
        _trigonometric_polynomial_model(
            profile,
            harmonic=2,
            sine=False,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
        _trigonometric_polynomial_model(
            profile,
            harmonic=4,
            sine=False,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
        _trigonometric_polynomial_model(
            profile,
            harmonic=2,
            sine=True,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
        _trigonometric_polynomial_model(
            profile,
            harmonic=1,
            sine=False,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
    )


def _combined_jacobi_numerator_model(
    profile: RationalPolynomial,
    auxiliary: RationalPolynomial,
    radius: RationalPolynomial,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_taylor_terms: int,
    physical_half_width: Fraction,
    trigonometric_models: tuple[
        tuple[IntervalPolynomial, Fraction],
        tuple[IntervalPolynomial, Fraction],
        tuple[IntervalPolynomial, Fraction],
        tuple[IntervalPolynomial, Fraction],
    ]
    | None = None,
) -> tuple[IntervalPolynomial, Fraction]:
    """Model ``x^2 L_F auxiliary`` without splitting Jacobi coefficients.

    The five-harmonic identity keeps all polynomial cancellations exact before
    the final centered monomial range operation. Only the four transcendental
    Taylor remainders are ranged separately.
    """
    one = RationalPolynomial((Fraction(1),))
    four = RationalPolynomial((Fraction(4),))
    x2 = _rational_polynomial_power(radius, 2)
    x4 = _rational_polynomial_power(radius, 4)
    lapse = _rational_polynomial_add(
        one, _rational_polynomial_scale(x2, -curvature)
    )
    lapse_derivative = _rational_polynomial_scale(radius, -2 * curvature)
    derivative = _rational_polynomial_scale(
        auxiliary.derivative(), 1 / physical_half_width
    )
    second_derivative = _rational_polynomial_scale(
        auxiliary.derivative().derivative(), 1 / physical_half_width**2
    )
    profile_derivative = _rational_polynomial_scale(
        profile.derivative(), 1 / physical_half_width
    )
    profile_second_derivative = _rational_polynomial_scale(
        profile.derivative().derivative(), 1 / physical_half_width**2
    )
    x2_plus_four = _rational_polynomial_add(x2, four)

    b0 = _rational_polynomial_add(
        _rational_polynomial_scale(
            _rational_polynomial_multiply(
                _rational_polynomial_multiply(x2, lapse),
                _rational_polynomial_multiply(x2_plus_four, second_derivative),
            ),
            -1,
        ),
        _rational_polynomial_scale(
            _rational_polynomial_multiply(
                x2,
                _rational_polynomial_multiply(
                    _rational_polynomial_add(
                        _rational_polynomial_multiply(
                            lapse_derivative, x2_plus_four
                        ),
                        _rational_polynomial_scale(
                            _rational_polynomial_multiply(lapse, radius), 2
                        ),
                    ),
                    derivative,
                ),
            ),
            -1,
        ),
    )
    bc2 = _rational_polynomial_add(
        _rational_polynomial_scale(
            _rational_polynomial_multiply(
                _rational_polynomial_multiply(lapse, x2), second_derivative
            ),
            4,
        ),
        _rational_polynomial_scale(
            _rational_polynomial_multiply(
                _rational_polynomial_multiply(lapse_derivative, x2), derivative
            ),
            4,
        ),
        _rational_polynomial_multiply(
            _rational_polynomial_add(
                _rational_polynomial_scale(x2, 2),
                four,
                _rational_polynomial_scale(
                    _rational_polynomial_multiply(
                        _rational_polynomial_multiply(lapse, x2),
                        _rational_polynomial_power(profile_derivative, 2),
                    ),
                    -8,
                ),
            ),
            auxiliary,
        ),
    )
    bc4 = _rational_polynomial_scale(auxiliary, -4)
    bs2 = _rational_polynomial_scale(
        _rational_polynomial_multiply(
            x2,
            _rational_polynomial_add(
                _rational_polynomial_multiply(
                    _rational_polynomial_multiply(lapse, profile_derivative),
                    derivative,
                ),
                _rational_polynomial_multiply(
                    _rational_polynomial_multiply(
                        lapse_derivative, profile_derivative
                    ),
                    auxiliary,
                ),
                _rational_polynomial_multiply(
                    _rational_polynomial_multiply(lapse, profile_second_derivative),
                    auxiliary,
                ),
            ),
        ),
        -8,
    )
    bc1 = _rational_polynomial_scale(
        _rational_polynomial_multiply(x4, auxiliary), pion_mass_squared
    )

    models = trigonometric_models or _combined_trigonometric_models(
        profile,
        trigonometric_terms=trigonometric_terms,
        residual_taylor_terms=residual_taylor_terms,
    )
    (
        (cosine_two, cosine_two_tail),
        (cosine_four, cosine_four_tail),
        (sine_two, sine_two_tail),
        (cosine_one, cosine_one_tail),
    ) = models
    model = _interval_polynomial_add(
        _interval_polynomial_from_rational(b0),
        _interval_polynomial_multiply_rational(cosine_two, bc2),
        _interval_polynomial_multiply_rational(cosine_four, bc4),
        _interval_polynomial_multiply_rational(sine_two, bs2),
        _interval_polynomial_multiply_rational(cosine_one, bc1),
    )
    tail = sum(
        _absolute_interval_upper(_rational_polynomial_bernstein_range(coefficient))
        * trigonometric_tail
        for coefficient, trigonometric_tail in (
            (bc2, cosine_two_tail),
            (bc4, cosine_four_tail),
            (bs2, sine_two_tail),
            (bc1, cosine_one_tail),
        )
    )
    return model, tail


def _combined_nonlinear_numerator_model(
    profile: RationalPolynomial,
    radius: RationalPolynomial,
    *,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_taylor_terms: int,
    physical_half_width: Fraction,
) -> tuple[IntervalPolynomial, Fraction]:
    """Model ``x^2 R(F)`` with cancellation before interval ranging.

    Here ``R(F)=(P(F)F')'-source(F)`` is the nonlinear profile residual used
    by the global candidate generator.  The exact five-harmonic identity is

        x^2 R = A0 + Ac2 cos(2F) + As2 sin(2F)
                  + sin(4F) - m^2 x^4 sin(F).
    """
    one = RationalPolynomial((Fraction(1),))
    two = RationalPolynomial((Fraction(2),))
    four = RationalPolynomial((Fraction(4),))
    x2 = _rational_polynomial_power(radius, 2)
    x4 = _rational_polynomial_power(radius, 4)
    lapse = _rational_polynomial_add(
        one, _rational_polynomial_scale(x2, -curvature)
    )
    lapse_derivative = _rational_polynomial_scale(radius, -2 * curvature)
    derivative = _rational_polynomial_scale(
        profile.derivative(), 1 / physical_half_width
    )
    second_derivative = _rational_polynomial_scale(
        profile.derivative().derivative(), 1 / physical_half_width**2
    )
    x2_plus_four = _rational_polynomial_add(x2, four)
    a0 = _rational_polynomial_add(
        _rational_polynomial_multiply(
            _rational_polynomial_multiply(x2, lapse),
            _rational_polynomial_multiply(x2_plus_four, second_derivative),
        ),
        _rational_polynomial_multiply(
            x2,
            _rational_polynomial_multiply(
                _rational_polynomial_add(
                    _rational_polynomial_multiply(
                        lapse_derivative, x2_plus_four
                    ),
                    _rational_polynomial_scale(
                        _rational_polynomial_multiply(lapse, radius), 2
                    ),
                ),
                derivative,
            ),
        ),
    )
    ac2 = _rational_polynomial_scale(
        _rational_polynomial_add(
            _rational_polynomial_multiply(
                _rational_polynomial_multiply(lapse, x2), second_derivative
            ),
            _rational_polynomial_multiply(
                _rational_polynomial_multiply(lapse_derivative, x2), derivative
            ),
        ),
        -4,
    )
    as2 = _rational_polynomial_add(
        _rational_polynomial_scale(
            _rational_polynomial_multiply(
                _rational_polynomial_multiply(lapse, x2),
                _rational_polynomial_power(derivative, 2),
            ),
            4,
        ),
        _rational_polynomial_scale(x2, -1),
        _rational_polynomial_scale(two, -1),
    )
    as4 = one
    as1 = _rational_polynomial_scale(x4, -pion_mass_squared)
    models = (
        _trigonometric_polynomial_model(
            profile,
            harmonic=2,
            sine=False,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
        _trigonometric_polynomial_model(
            profile,
            harmonic=2,
            sine=True,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
        _trigonometric_polynomial_model(
            profile,
            harmonic=4,
            sine=True,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
        _trigonometric_polynomial_model(
            profile,
            harmonic=1,
            sine=True,
            center_terms=trigonometric_terms,
            model_terms=residual_taylor_terms,
        ),
    )
    (
        (cosine_two, cosine_two_tail),
        (sine_two, sine_two_tail),
        (sine_four, sine_four_tail),
        (sine_one, sine_one_tail),
    ) = models
    model = _interval_polynomial_add(
        _interval_polynomial_from_rational(a0),
        _interval_polynomial_multiply_rational(cosine_two, ac2),
        _interval_polynomial_multiply_rational(sine_two, as2),
        _interval_polynomial_multiply_rational(sine_four, as4),
        _interval_polynomial_multiply_rational(sine_one, as1),
    )
    tail = sum(
        _absolute_interval_upper(_rational_polynomial_bernstein_range(coefficient))
        * trigonometric_tail
        for coefficient, trigonometric_tail in (
            (ac2, cosine_two_tail),
            (as2, sine_two_tail),
            (as4, sine_four_tail),
            (as1, sine_one_tail),
        )
    )
    return model, tail


def _endpoint_corrected_nonlinear_residual_cell(
    profile_cell: SkyrmionPolynomialCell,
    *,
    source_cell_index: int,
    normalized_left: Fraction,
    normalized_right: Fraction,
    domain_left: Fraction,
    domain_right: Fraction,
    left_value_correction: RationalInterval,
    right_value_correction: Fraction,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_taylor_terms: int,
) -> ValidatedSkyrmionNonlinearResidualCell:
    normalized_center = (normalized_left + normalized_right) / 2
    normalized_half_width = (normalized_right - normalized_left) / 2
    physical_half_width = profile_cell.radius.width * normalized_half_width
    physical_center = (
        profile_cell.radius.lower
        + profile_cell.radius.width * normalized_center
    )
    radius_polynomial = RationalPolynomial(
        (physical_center, physical_half_width)
    )
    profile_polynomial = _affine_restrict_polynomial(
        profile_cell.profile_polynomial,
        normalized_center,
        normalized_half_width,
    )
    domain_length = domain_right - domain_left
    chi_left = RationalPolynomial(
        (
            (domain_right - physical_center) / domain_length,
            -physical_half_width / domain_length,
        )
    )
    chi_right = RationalPolynomial(
        (
            (physical_center - domain_left) / domain_length,
            physical_half_width / domain_length,
        )
    )
    left_center = (
        Fraction(0)
        if left_value_correction.lower <= 0 <= left_value_correction.upper
        else left_value_correction.midpoint
    )
    left_deviation = left_value_correction - left_center
    midpoint_profile_polynomial = _rational_polynomial_add(
        profile_polynomial,
        _rational_polynomial_scale(chi_left, left_center),
        _rational_polynomial_scale(chi_right, right_value_correction),
    )
    midpoint_model, midpoint_tail = _combined_nonlinear_numerator_model(
        midpoint_profile_polynomial,
        radius_polynomial,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
        residual_taylor_terms=residual_taylor_terms,
        physical_half_width=physical_half_width,
    )
    numerator = _interval_polynomial_centered_range(midpoint_model) + (
        RationalInterval(-midpoint_tail, midpoint_tail)
    )
    radius_squared = _rational_polynomial_bernstein_range(
        _rational_polynomial_power(radius_polynomial, 2)
    )
    midpoint_residual = numerator / radius_squared

    midpoint_profile = _rational_polynomial_bernstein_range(
        midpoint_profile_polynomial
    )
    midpoint_derivative = _rational_polynomial_bernstein_range(
        _rational_polynomial_scale(
            midpoint_profile_polynomial.derivative(),
            1 / physical_half_width,
        )
    )
    midpoint_second_derivative = _rational_polynomial_bernstein_range(
        _rational_polynomial_scale(
            midpoint_profile_polynomial.derivative().derivative(),
            1 / physical_half_width**2,
        )
    )
    chi_left_range = _rational_polynomial_bernstein_range(chi_left)
    family_jet = SkyrmionJetBox(
        radius=_rational_polynomial_bernstein_range(radius_polynomial),
        profile=midpoint_profile + left_deviation * chi_left_range,
        derivative=(
            midpoint_derivative
            + left_deviation.scale(-1 / domain_length)
        ),
        second_derivative=midpoint_second_derivative,
    )
    family_coefficients = skyrmion_jacobi_coefficient_box(
        family_jet,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    chi_jacobi = (
        family_coefficients.principal_derivative.scale(1 / domain_length)
        + family_coefficients.potential * chi_left_range
    )
    family_error = (
        _absolute_interval_upper(left_deviation)
        * _absolute_interval_upper(chi_jacobi)
    )
    residual = midpoint_residual + RationalInterval(-family_error, family_error)
    return ValidatedSkyrmionNonlinearResidualCell(
        source_cell_index=source_cell_index,
        radius=family_jet.radius,
        midpoint_profile=midpoint_profile,
        family_profile_jet=family_jet,
        family_jacobi_coefficients=family_coefficients,
        midpoint_residual=midpoint_residual,
        family_residual_error_upper_bound=family_error,
        residual=residual,
    )


def validate_skyrmion_endpoint_corrected_residual(
    profile_cells: Sequence[SkyrmionPolynomialCell],
    phi_at_cutoff: RationalInterval,
    gamma_at_cutoff: RationalInterval,
    *,
    phi_sensitivity_at_cutoff: RationalInterval | None = None,
    gamma_sensitivity_at_cutoff: RationalInterval | None = None,
    subdivisions_per_source_cell: int = 1,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
    residual_taylor_terms: int = 8,
) -> ValidatedSkyrmionEndpointCorrectedResidual:
    """Recompute the nonlinear residual after exact endpoint correction.

    The midpoint of the interval origin-value correction is folded into one
    exact rational spline.  The remaining one-parameter affine uncertainty is
    bounded by integrating the Jacobi derivative over the full family.  This
    validates a residual family at the selected shooting slope; it does not
    prove that any member is an exact nonlinear solution.
    """
    if not isinstance(profile_cells, Sequence) or isinstance(
        profile_cells, (str, bytes)
    ):
        raise TypeError("profile_cells must be a sequence of polynomial cells")
    if not profile_cells:
        raise ValueError("at least one profile polynomial cell is required")
    if not isinstance(phi_at_cutoff, RationalInterval):
        raise TypeError("phi_at_cutoff must be a RationalInterval")
    if not isinstance(gamma_at_cutoff, RationalInterval):
        raise TypeError("gamma_at_cutoff must be a RationalInterval")
    if (phi_sensitivity_at_cutoff is None) != (
        gamma_sensitivity_at_cutoff is None
    ):
        raise ValueError(
            "origin profile and derivative sensitivities must be supplied together"
        )
    if phi_sensitivity_at_cutoff is not None and not isinstance(
        phi_sensitivity_at_cutoff, RationalInterval
    ):
        raise TypeError("phi_sensitivity_at_cutoff must be a RationalInterval")
    if gamma_sensitivity_at_cutoff is not None and not isinstance(
        gamma_sensitivity_at_cutoff, RationalInterval
    ):
        raise TypeError("gamma_sensitivity_at_cutoff must be a RationalInterval")
    subdivisions = _positive_integer(
        "subdivisions_per_source_cell", subdivisions_per_source_cell
    )
    model_terms = _positive_integer(
        "residual_taylor_terms", residual_taylor_terms
    )
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)
    _validate_globally_c2_polynomial_cells(profile_cells)
    domain_left = profile_cells[0].radius.lower
    domain_right = profile_cells[-1].radius.upper
    domain_length = domain_right - domain_left
    left_value = profile_cells[0].profile_polynomial.evaluate(Fraction(0))
    right_value = profile_cells[-1].profile_polynomial.evaluate(Fraction(1))
    left_correction = phi_at_cutoff - left_value
    right_correction = -right_value.lower
    left_derivative = (
        profile_cells[0]
        .profile_polynomial.derivative()
        .evaluate(Fraction(0))
        .scale(1 / profile_cells[0].radius.width)
    )
    boundary_slope_residual = (
        left_derivative
        + left_correction.scale(-1 / domain_length)
        + RationalInterval.point(right_correction / domain_length)
        - gamma_at_cutoff
    )
    checked = tuple(
        _endpoint_corrected_nonlinear_residual_cell(
            profile_cell,
            source_cell_index=source_index,
            normalized_left=Fraction(index, subdivisions),
            normalized_right=Fraction(index + 1, subdivisions),
            domain_left=domain_left,
            domain_right=domain_right,
            left_value_correction=left_correction,
            right_value_correction=right_correction,
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
            trigonometric_terms=trigonometric_terms,
            residual_taylor_terms=model_terms,
        )
        for source_index, profile_cell in enumerate(profile_cells)
        for index in range(subdivisions)
    )
    residual_supremum = max(
        _absolute_interval_upper(cell.residual) for cell in checked
    )
    return ValidatedSkyrmionEndpointCorrectedResidual(
        profile_cells=tuple(profile_cells),
        cells=checked,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        phi_at_cutoff=phi_at_cutoff,
        gamma_at_cutoff=gamma_at_cutoff,
        phi_sensitivity_at_cutoff=phi_sensitivity_at_cutoff,
        gamma_sensitivity_at_cutoff=gamma_sensitivity_at_cutoff,
        left_value_correction=left_correction,
        right_value_correction=right_correction,
        boundary_slope_residual=boundary_slope_residual,
        residual_supremum_upper_bound=residual_supremum,
        source_cell_count=len(profile_cells),
        subdivisions_per_source_cell=subdivisions,
        conclusion_scope=(
            "endpoint-corrected approximate-profile family at one selected "
            "shooting slope only; no nonlinear BVP existence conclusion"
        ),
    )


def _validate_matching_auxiliary_cells(
    profile_cells: Sequence[SkyrmionPolynomialCell],
    auxiliary_cells: Sequence[SkyrmionPolynomialCell],
) -> None:
    if not isinstance(auxiliary_cells, Sequence) or isinstance(
        auxiliary_cells, (str, bytes)
    ):
        raise TypeError("auxiliary_cells must be a sequence of polynomial cells")
    if not auxiliary_cells:
        raise ValueError("at least one auxiliary polynomial cell is required")
    _validate_globally_c2_polynomial_cells(auxiliary_cells)
    if len(profile_cells) != len(auxiliary_cells):
        raise ValueError("profile and auxiliary cell counts must agree")
    for profile, auxiliary in zip(profile_cells, auxiliary_cells):
        if profile.radius != auxiliary.radius:
            raise ValueError("profile and auxiliary meshes must coincide exactly")
    if auxiliary_cells[-1].profile_polynomial.evaluate(Fraction(1)) != (
        RationalInterval.point(0)
    ):
        raise ValueError("auxiliary spline must vanish exactly at the right wall")


def _lifted_auxiliary_residual_cell(
    profile_cell: SkyrmionPolynomialCell,
    auxiliary_cell: SkyrmionPolynomialCell,
    *,
    source_cell_index: int,
    normalized_left: Fraction,
    normalized_right: Fraction,
    refinement_depth: int,
    domain_right: Fraction,
    domain_length: Fraction,
    lift_coefficient: RationalInterval,
    pion_mass_squared: Fraction,
    curvature: Fraction,
    trigonometric_terms: int,
    residual_taylor_terms: int,
) -> ValidatedSkyrmionSchurResidualCell:
    normalized_center = (normalized_left + normalized_right) / 2
    normalized_half_width = (normalized_right - normalized_left) / 2
    physical_half_width = profile_cell.radius.width * normalized_half_width
    profile_polynomial = _affine_restrict_polynomial(
        profile_cell.profile_polynomial,
        normalized_center,
        normalized_half_width,
    )
    auxiliary_polynomial = _affine_restrict_polynomial(
        auxiliary_cell.profile_polynomial,
        normalized_center,
        normalized_half_width,
    )
    physical_center = (
        profile_cell.radius.lower
        + profile_cell.radius.width * normalized_center
    )
    radius_polynomial = RationalPolynomial(
        (physical_center, physical_half_width)
    )
    affine_lift_polynomial = RationalPolynomial(
        (
            (domain_right - physical_center) / domain_length,
            -physical_half_width / domain_length,
        )
    )
    lift_midpoint = lift_coefficient.midpoint
    lift_deviation = lift_coefficient - lift_midpoint
    midpoint_auxiliary = _rational_polynomial_add(
        auxiliary_polynomial,
        _rational_polynomial_scale(affine_lift_polynomial, lift_midpoint),
    )
    trigonometric_models = _combined_trigonometric_models(
        profile_polynomial,
        trigonometric_terms=trigonometric_terms,
        residual_taylor_terms=residual_taylor_terms,
    )
    midpoint_model, midpoint_tail = _combined_jacobi_numerator_model(
        profile_polynomial,
        midpoint_auxiliary,
        radius_polynomial,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
        residual_taylor_terms=residual_taylor_terms,
        physical_half_width=physical_half_width,
        trigonometric_models=trigonometric_models,
    )
    if lift_deviation == RationalInterval.point(0):
        combined_model = midpoint_model
        tail = midpoint_tail
    else:
        lift_model, lift_tail = _combined_jacobi_numerator_model(
            profile_polynomial,
            affine_lift_polynomial,
            radius_polynomial,
            pion_mass_squared=pion_mass_squared,
            curvature=curvature,
            trigonometric_terms=trigonometric_terms,
            residual_taylor_terms=residual_taylor_terms,
            physical_half_width=physical_half_width,
            trigonometric_models=trigonometric_models,
        )
        combined_model = _interval_polynomial_add(
            midpoint_model,
            _interval_polynomial_scale(lift_model, lift_deviation),
        )
        tail = midpoint_tail + _absolute_interval_upper(lift_deviation) * lift_tail
    numerator = _interval_polynomial_centered_range(combined_model) + (
        RationalInterval(-tail, tail)
    )
    radius_squared = _rational_polynomial_bernstein_range(
        _rational_polynomial_power(radius_polynomial, 2)
    )
    if radius_squared.lower <= 0:
        raise ValueError("combined residual requires a positive radius cell")

    profile_jet = _polynomial_subcell_jet(
        profile_cell, normalized_left, normalized_right
    )
    auxiliary_jet = _polynomial_subcell_jet(
        auxiliary_cell, normalized_left, normalized_right
    )
    coefficients = skyrmion_jacobi_coefficient_box(
        profile_jet,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    affine_factor = (
        RationalInterval.point(domain_right) - profile_jet.radius
    ).scale(1 / domain_length)
    lift_derivative = lift_coefficient.scale(-1 / domain_length)
    auxiliary = auxiliary_jet.profile + lift_coefficient * affine_factor
    derivative = auxiliary_jet.derivative + lift_derivative
    second_derivative = auxiliary_jet.second_derivative
    residual = numerator / radius_squared
    return ValidatedSkyrmionSchurResidualCell(
        source_cell_index=source_cell_index,
        radius=profile_jet.radius,
        auxiliary=auxiliary,
        derivative=derivative,
        second_derivative=second_derivative,
        coefficients=coefficients,
        residual=residual,
        refinement_depth=refinement_depth,
    )


def validate_skyrmion_polynomial_schur_bound(
    profile_cells: Sequence[SkyrmionPolynomialCell],
    auxiliary_cells: Sequence[SkyrmionPolynomialCell],
    phi_b: RationalInterval,
    gamma_b: RationalInterval,
    declared_barta_lower_bound: Fraction,
    declared_schur_lower_bound: Fraction,
    *,
    barta_initial_subdivisions: int = 4,
    barta_maximum_refinement_depth: int = 3,
    residual_initial_subdivisions: int = 4,
    residual_maximum_refinement_depth: int = 3,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
    residual_taylor_terms: int = 8,
) -> ValidatedSkyrmionPolynomialSchurBound:
    """Validate a positive wall-Dirichlet Schur margin conditionally.

    Both splines are exact rational polynomials in normalized cell
    coordinates.  The auxiliary is required to vanish exactly at the right
    wall.  It is replaced by the interval family

        H(x) = H_hat(x) + (phi_b - H_hat(a)) (c-x)/(c-a),

    so every member has the required left value and right-wall value.  The
    routine recomputes ``L H`` on adaptive exact-rational interval subcells;
    no residual boxes supplied by a proposal generator are accepted.

    Barta coercivity ``alpha`` gives ``C0=2/alpha``.  With ``p0`` the checked
    lower bound for ``P`` and ``q1`` an interval upper bound for
    ``integral |Q|``, the Dirichlet trace estimate used here is

        C1 = ((c-a) + q1*C0)/p0.

    The conclusion is only for the Jacobi operator of the exact approximate
    profile spline.  It does not establish a nearby nonlinear BVP solution.
    """
    if not isinstance(profile_cells, Sequence) or isinstance(
        profile_cells, (str, bytes)
    ):
        raise TypeError("profile_cells must be a sequence of polynomial cells")
    if not profile_cells:
        raise ValueError("at least one profile polynomial cell is required")
    if not isinstance(phi_b, RationalInterval):
        raise TypeError("phi_b must be a RationalInterval")
    if not isinstance(gamma_b, RationalInterval):
        raise TypeError("gamma_b must be a RationalInterval")
    alpha = _fraction(
        "declared_barta_lower_bound", declared_barta_lower_bound
    )
    if alpha <= 0:
        raise ValueError("declared_barta_lower_bound must be positive")
    declared_schur = _fraction(
        "declared_schur_lower_bound", declared_schur_lower_bound
    )
    if declared_schur <= 0:
        raise ValueError("declared_schur_lower_bound must be positive")
    residual_subdivisions = _positive_integer(
        "residual_initial_subdivisions", residual_initial_subdivisions
    )
    residual_depth_limit = _nonnegative_integer(
        "residual_maximum_refinement_depth",
        residual_maximum_refinement_depth,
    )
    residual_model_terms = _positive_integer(
        "residual_taylor_terms", residual_taylor_terms
    )

    _validate_globally_c2_polynomial_cells(profile_cells)
    _validate_matching_auxiliary_cells(profile_cells, auxiliary_cells)
    domain_left = profile_cells[0].radius.lower
    domain_right = profile_cells[-1].radius.upper
    domain_length = domain_right - domain_left
    witness_range = RationalInterval.point(8) / (
        (RationalInterval(domain_left, domain_right) - Fraction(33, 16)).power(2)
        + 4
    )
    if witness_range.lower <= 0 or (
        witness_range.upper > 2 * witness_range.lower
    ):
        raise ValueError(
            "the fixed Barta witness must have max/min ratio at most two "
            "to use C0=2/alpha"
        )

    barta = validate_skyrmion_polynomial_barta_spline(
        profile_cells,
        alpha,
        initial_subdivisions=barta_initial_subdivisions,
        maximum_refinement_depth=barta_maximum_refinement_depth,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    principal_lower_bound = min(
        cell.coefficients.principal.lower for cell in barta.cells
    )
    potential_l1_upper_bound = sum(
        cell.jet.radius.width
        * _absolute_interval_upper(cell.coefficients.potential)
        for cell in barta.cells
    )
    inverse_c0_bound = Fraction(2, 1) / alpha
    boundary_derivative_c1_bound = (
        domain_length + potential_l1_upper_bound * inverse_c0_bound
    ) / principal_lower_bound

    auxiliary_left = auxiliary_cells[0].profile_polynomial.evaluate(Fraction(0))
    auxiliary_left_derivative = (
        auxiliary_cells[0]
        .profile_polynomial.derivative()
        .evaluate(Fraction(0))
        .scale(1 / auxiliary_cells[0].radius.width)
    )
    lift_coefficient = phi_b - auxiliary_left
    lift_derivative = lift_coefficient.scale(-1 / domain_length)
    raw_schur = auxiliary_left_derivative + lift_derivative - gamma_b
    residual_budget = (
        (raw_schur.lower - declared_schur) / boundary_derivative_c1_bound
        if raw_schur.lower > declared_schur
        else Fraction(0)
    )

    checked_residuals: list[ValidatedSkyrmionSchurResidualCell] = []
    maximum_depth_used = 0
    for source_index, (profile_cell, auxiliary_cell) in enumerate(
        zip(profile_cells, auxiliary_cells)
    ):
        pending = [
            (
                Fraction(index, residual_subdivisions),
                Fraction(index + 1, residual_subdivisions),
                0,
            )
            for index in reversed(range(residual_subdivisions))
        ]
        while pending:
            left, right, depth = pending.pop()
            checked = _lifted_auxiliary_residual_cell(
                profile_cell,
                auxiliary_cell,
                source_cell_index=source_index,
                normalized_left=left,
                normalized_right=right,
                refinement_depth=depth,
                domain_right=domain_right,
                domain_length=domain_length,
                lift_coefficient=lift_coefficient,
                pion_mass_squared=pion_mass_squared,
                curvature=curvature,
                trigonometric_terms=trigonometric_terms,
                residual_taylor_terms=residual_model_terms,
            )
            if (
                _absolute_interval_upper(checked.residual) > residual_budget
                and depth < residual_depth_limit
            ):
                midpoint = (left + right) / 2
                pending.append((midpoint, right, depth + 1))
                pending.append((left, midpoint, depth + 1))
                continue
            maximum_depth_used = max(maximum_depth_used, depth)
            checked_residuals.append(checked)

    residual_supremum = max(
        _absolute_interval_upper(cell.residual) for cell in checked_residuals
    )
    derivative_error = boundary_derivative_c1_bound * residual_supremum
    corrected_schur = RationalInterval(
        raw_schur.lower - derivative_error,
        raw_schur.upper + derivative_error,
    )
    if corrected_schur.lower < declared_schur:
        raise ValueError(
            "declared positive Schur lower bound is not verified after the "
            "trusted residual and boundary-trace correction"
        )

    return ValidatedSkyrmionPolynomialSchurBound(
        barta_validation=barta,
        residual_cells=tuple(checked_residuals),
        phi_b=phi_b,
        gamma_b=gamma_b,
        affine_left_lift_coefficient=lift_coefficient,
        affine_left_lift_derivative=lift_derivative,
        raw_schur_enclosure=raw_schur,
        residual_supremum_upper_bound=residual_supremum,
        principal_lower_bound=principal_lower_bound,
        potential_l1_upper_bound=potential_l1_upper_bound,
        inverse_c0_bound=inverse_c0_bound,
        boundary_derivative_c1_bound=boundary_derivative_c1_bound,
        boundary_derivative_error_bound=derivative_error,
        corrected_schur_enclosure=corrected_schur,
        declared_schur_lower_bound=declared_schur,
        maximum_residual_refinement_depth=residual_depth_limit,
        maximum_residual_refinement_depth_used=maximum_depth_used,
        conclusion_scope=(
            "exact approximate profile Jacobi operator and affinely lifted "
            "auxiliary family only; no nonlinear BVP existence conclusion"
        ),
    )


def validate_skyrmion_derivative_trace_representer(
    profile_cells: Sequence[SkyrmionPolynomialCell],
    representer_cells: Sequence[SkyrmionPolynomialCell],
    declared_barta_lower_bound: Fraction,
    declared_trace_upper_bound: Fraction,
    *,
    barta_initial_subdivisions: int = 4,
    barta_maximum_refinement_depth: int = 3,
    residual_initial_subdivisions: int = 4,
    residual_maximum_refinement_depth: int = 3,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
    residual_taylor_terms: int = 8,
) -> ValidatedSkyrmionDerivativeTraceBound:
    """Validate an independent Dirichlet derivative-trace constant.

    ``representer_cells`` is an exact rational approximation ``kappa_hat`` to
    the Dirichlet representer with exact endpoint values
    ``kappa_hat(a)=1`` and ``kappa_hat(c)=0``.  The routine independently
    recomputes Barta coercivity and ``rho=||L kappa_hat||_infinity``.  If ``v``
    is the fixed positive Barta witness, then

        C0 = (max(v)/min(v))/alpha,
        ||kappa||_1 <= ||kappa_hat||_1 + (c-a) C0 rho,
        C_tau <= ||kappa||_1 / P(a).

    The L1 norm of ``kappa_hat`` is integrated exactly on cells whose exact
    Bernstein hull has fixed sign.  Sign-indefinite cells use the rigorous
    cell-width times supremum bound.  The conclusion concerns only the Jacobi
    operator of the exact approximate profile spline; it does not validate a
    nearby nonlinear boundary-value solution.
    """
    if not isinstance(profile_cells, Sequence) or isinstance(
        profile_cells, (str, bytes)
    ):
        raise TypeError("profile_cells must be a sequence of polynomial cells")
    if not profile_cells:
        raise ValueError("at least one profile polynomial cell is required")
    alpha = _fraction(
        "declared_barta_lower_bound", declared_barta_lower_bound
    )
    if alpha <= 0:
        raise ValueError("declared_barta_lower_bound must be positive")
    declared_trace = _fraction(
        "declared_trace_upper_bound", declared_trace_upper_bound
    )
    if declared_trace <= 0:
        raise ValueError("declared_trace_upper_bound must be positive")
    residual_subdivisions = _positive_integer(
        "residual_initial_subdivisions", residual_initial_subdivisions
    )
    residual_depth_limit = _nonnegative_integer(
        "residual_maximum_refinement_depth",
        residual_maximum_refinement_depth,
    )
    residual_model_terms = _positive_integer(
        "residual_taylor_terms", residual_taylor_terms
    )

    _validate_globally_c2_polynomial_cells(profile_cells)
    _validate_matching_auxiliary_cells(profile_cells, representer_cells)
    representer_left = representer_cells[0].profile_polynomial.evaluate(
        Fraction(0)
    )
    if representer_left != RationalInterval.point(1):
        raise ValueError(
            "representer spline must equal one exactly at the left endpoint"
        )

    domain_left = profile_cells[0].radius.lower
    domain_right = profile_cells[-1].radius.upper
    domain_length = domain_right - domain_left
    witness_range = RationalInterval.point(8) / (
        (RationalInterval(domain_left, domain_right) - Fraction(33, 16)).power(2)
        + 4
    )
    if witness_range.lower <= 0:
        raise ValueError("the fixed Barta witness must remain positive")
    witness_ratio = witness_range.upper / witness_range.lower
    if witness_ratio > 2:
        raise ValueError(
            "the fixed Barta witness must have max/min ratio at most two"
        )
    inverse_c0_bound = witness_ratio / alpha

    barta = validate_skyrmion_polynomial_barta_spline(
        profile_cells,
        alpha,
        initial_subdivisions=barta_initial_subdivisions,
        maximum_refinement_depth=barta_maximum_refinement_depth,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )

    l1_cells: list[ValidatedSkyrmionRepresenterL1Cell] = []
    approximate_l1 = Fraction(0)
    for source_index, cell in enumerate(representer_cells):
        bernstein_range, normalized_l1, fixed_sign = (
            _normalized_polynomial_l1_upper_bound(cell.profile_polynomial)
        )
        contribution = cell.radius.width * normalized_l1
        approximate_l1 += contribution
        l1_cells.append(
            ValidatedSkyrmionRepresenterL1Cell(
                source_cell_index=source_index,
                radius=cell.radius,
                bernstein_range=bernstein_range,
                l1_upper_bound=contribution,
                integrated_with_fixed_sign=fixed_sign,
            )
        )

    left_jet = _polynomial_subcell_jet(
        profile_cells[0], Fraction(0), Fraction(0)
    )
    left_coefficients = skyrmion_jacobi_coefficient_box(
        left_jet,
        pion_mass_squared=pion_mass_squared,
        curvature=curvature,
        trigonometric_terms=trigonometric_terms,
    )
    principal_left = left_coefficients.principal
    if principal_left.lower <= 0:
        raise ValueError(
            "left endpoint Jacobi principal coefficient is not positive"
        )

    residual_budget_numerator = (
        declared_trace * principal_left.lower - approximate_l1
    )
    residual_budget = (
        residual_budget_numerator / (domain_length * inverse_c0_bound)
        if residual_budget_numerator > 0
        else Fraction(0)
    )
    checked_residuals: list[ValidatedSkyrmionSchurResidualCell] = []
    maximum_depth_used = 0
    zero_lift = RationalInterval.point(0)
    for source_index, (profile_cell, representer_cell) in enumerate(
        zip(profile_cells, representer_cells)
    ):
        pending = [
            (
                Fraction(index, residual_subdivisions),
                Fraction(index + 1, residual_subdivisions),
                0,
            )
            for index in reversed(range(residual_subdivisions))
        ]
        while pending:
            left, right, depth = pending.pop()
            checked = _lifted_auxiliary_residual_cell(
                profile_cell,
                representer_cell,
                source_cell_index=source_index,
                normalized_left=left,
                normalized_right=right,
                refinement_depth=depth,
                domain_right=domain_right,
                domain_length=domain_length,
                lift_coefficient=zero_lift,
                pion_mass_squared=pion_mass_squared,
                curvature=curvature,
                trigonometric_terms=trigonometric_terms,
                residual_taylor_terms=residual_model_terms,
            )
            if (
                _absolute_interval_upper(checked.residual) > residual_budget
                and depth < residual_depth_limit
            ):
                midpoint = (left + right) / 2
                pending.append((midpoint, right, depth + 1))
                pending.append((left, midpoint, depth + 1))
                continue
            maximum_depth_used = max(maximum_depth_used, depth)
            checked_residuals.append(checked)

    residual_supremum = max(
        _absolute_interval_upper(cell.residual) for cell in checked_residuals
    )
    representer_error_l1 = domain_length * inverse_c0_bound * residual_supremum
    representer_l1 = approximate_l1 + representer_error_l1
    trace_upper = representer_l1 / principal_left.lower
    if trace_upper > declared_trace:
        raise ValueError(
            "declared derivative-trace upper bound is not verified after the "
            "trusted representer residual correction"
        )

    return ValidatedSkyrmionDerivativeTraceBound(
        barta_validation=barta,
        l1_cells=tuple(l1_cells),
        residual_cells=tuple(checked_residuals),
        barta_witness_range=witness_range,
        barta_witness_ratio_upper_bound=witness_ratio,
        inverse_c0_bound=inverse_c0_bound,
        domain_length=domain_length,
        approximate_representer_l1_upper_bound=approximate_l1,
        residual_supremum_upper_bound=residual_supremum,
        representer_error_l1_upper_bound=representer_error_l1,
        representer_l1_upper_bound=representer_l1,
        principal_left_enclosure=principal_left,
        principal_left_lower_bound=principal_left.lower,
        recomputed_trace_upper_bound=trace_upper,
        declared_trace_upper_bound=declared_trace,
        maximum_residual_refinement_depth=residual_depth_limit,
        maximum_residual_refinement_depth_used=maximum_depth_used,
        conclusion_scope=(
            "exact approximate profile Jacobi operator and exact rational "
            "approximate Dirichlet representer only; no nonlinear BVP "
            "existence conclusion"
        ),
    )


def validate_skyrmion_green_resolvent_bounds(
    profile_cells: Sequence[SkyrmionPolynomialCell],
    left_fundamental_cells: Sequence[SkyrmionPolynomialCell],
    right_representer_cells: Sequence[SkyrmionPolynomialCell],
    declared_barta_lower_bound: Fraction,
    wronskian_normalization: Fraction,
    *,
    subdivisions_per_source_cell: int = 1,
    barta_initial_subdivisions: int = 4,
    barta_maximum_refinement_depth: int = 3,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
    residual_taylor_terms: int = 8,
    barta_validation: ValidatedSkyrmionPolynomialBartaBound | None = None,
) -> ValidatedSkyrmionGreenResolventBounds:
    """Certify sharp Dirichlet inverse bounds from a Green parametrix.

    The supplied exact splines approximate a left fundamental solution ``u``
    with ``u(a)=0`` and a right representer ``v`` with ``v(c)=0``.  With

        Ghat(x,s) = u(min(x,s)) v(max(x,s)) / w0,

    direct differentiation gives ``A Ghat = I+E``.  The residuals ``A u`` and
    ``A v``, together with the propagated Wronskian defect, bound ``||E||``.
    A defect strictly below one and a same-operator Barta audit then certify
    the exact inverse by a Neumann correction.  A supplied ``barta_validation``
    is reused only after exact spline, parameter, and declared-bound checks;
    otherwise the Barta audit is run here.  No pre-existing derivative
    resolvent estimate is used.
    """
    if not isinstance(profile_cells, Sequence) or isinstance(
        profile_cells, (str, bytes)
    ):
        raise TypeError("profile_cells must be a sequence of polynomial cells")
    if not profile_cells:
        raise ValueError("at least one profile polynomial cell is required")
    _validate_globally_c2_polynomial_cells(profile_cells)
    if not isinstance(left_fundamental_cells, Sequence) or isinstance(
        left_fundamental_cells, (str, bytes)
    ):
        raise TypeError(
            "left_fundamental_cells must be a sequence of polynomial cells"
        )
    if not isinstance(right_representer_cells, Sequence) or isinstance(
        right_representer_cells, (str, bytes)
    ):
        raise TypeError(
            "right_representer_cells must be a sequence of polynomial cells"
        )
    if not left_fundamental_cells or not right_representer_cells:
        raise ValueError("both Green-parametrix spline families are required")
    _validate_globally_c2_polynomial_cells(left_fundamental_cells)
    _validate_globally_c2_polynomial_cells(right_representer_cells)
    if not (
        len(profile_cells)
        == len(left_fundamental_cells)
        == len(right_representer_cells)
    ):
        raise ValueError("profile and Green-parametrix cell counts must agree")
    for profile, left, right in zip(
        profile_cells, left_fundamental_cells, right_representer_cells
    ):
        if profile.radius != left.radius or profile.radius != right.radius:
            raise ValueError(
                "profile and Green-parametrix meshes must coincide exactly"
            )
    if left_fundamental_cells[0].profile_polynomial.evaluate(Fraction(0)) != (
        RationalInterval.point(0)
    ):
        raise ValueError(
            "left Green fundamental spline must vanish exactly at the left endpoint"
        )
    if right_representer_cells[-1].profile_polynomial.evaluate(Fraction(1)) != (
        RationalInterval.point(0)
    ):
        raise ValueError(
            "right Green representer spline must vanish exactly at the right endpoint"
        )

    alpha = _fraction(
        "declared_barta_lower_bound", declared_barta_lower_bound
    )
    if alpha <= 0:
        raise ValueError("declared_barta_lower_bound must be positive")
    w0 = _fraction("wronskian_normalization", wronskian_normalization)
    if w0 <= 0:
        raise ValueError("wronskian_normalization must be positive")
    subdivisions = _positive_integer(
        "subdivisions_per_source_cell", subdivisions_per_source_cell
    )
    residual_model_terms = _positive_integer(
        "residual_taylor_terms", residual_taylor_terms
    )
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)

    if barta_validation is None:
        barta = validate_skyrmion_polynomial_barta_spline(
            profile_cells,
            alpha,
            initial_subdivisions=barta_initial_subdivisions,
            maximum_refinement_depth=barta_maximum_refinement_depth,
            pion_mass_squared=mass_squared,
            curvature=curvature_value,
            trigonometric_terms=trigonometric_terms,
        )
    else:
        if not isinstance(
            barta_validation, ValidatedSkyrmionPolynomialBartaBound
        ):
            raise TypeError(
                "barta_validation must be a polynomial Barta validation"
            )
        if (
            barta_validation.profile_cells != tuple(profile_cells)
            or barta_validation.pion_mass_squared != mass_squared
            or barta_validation.curvature != curvature_value
        ):
            raise ValueError(
                "Barta validation must use the same exact profile and operator"
            )
        if barta_validation.declared_lower_bound != alpha:
            raise ValueError(
                "Barta validation must use the same declared lower bound"
            )
        barta = barta_validation
    domain_left = profile_cells[0].radius.lower
    domain_right = profile_cells[-1].radius.upper
    domain_length = domain_right - domain_left
    profile_left_jet = _polynomial_subcell_jet(
        profile_cells[0], Fraction(0), Fraction(0)
    )
    principal_left = skyrmion_jacobi_coefficient_box(
        profile_left_jet,
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        trigonometric_terms=trigonometric_terms,
    ).principal
    left_jet = _polynomial_subcell_jet(
        left_fundamental_cells[0], Fraction(0), Fraction(0)
    )
    right_jet = _polynomial_subcell_jet(
        right_representer_cells[0], Fraction(0), Fraction(0)
    )
    initial_wronskian = principal_left * (
        left_jet.derivative * right_jet.profile
        - left_jet.profile * right_jet.derivative
    )
    if initial_wronskian.lower <= 0:
        raise ValueError(
            "initial Green-parametrix Wronskian is not certified positive"
        )
    initial_wronskian_error = _absolute_interval_upper(
        initial_wronskian - w0
    )

    leaves: list[
        tuple[
            int,
            ValidatedSkyrmionSchurResidualCell,
            ValidatedSkyrmionSchurResidualCell,
            Fraction,
            Fraction,
        ]
    ] = []
    zero_lift = RationalInterval.point(0)
    for source_index, (profile_cell, left_cell, right_cell) in enumerate(
        zip(
            profile_cells,
            left_fundamental_cells,
            right_representer_cells,
        )
    ):
        for subdivision in range(subdivisions):
            normalized_left = Fraction(subdivision, subdivisions)
            normalized_right = Fraction(subdivision + 1, subdivisions)
            left_residual = _lifted_auxiliary_residual_cell(
                profile_cell,
                left_cell,
                source_cell_index=source_index,
                normalized_left=normalized_left,
                normalized_right=normalized_right,
                refinement_depth=0,
                domain_right=domain_right,
                domain_length=domain_length,
                lift_coefficient=zero_lift,
                pion_mass_squared=mass_squared,
                curvature=curvature_value,
                trigonometric_terms=trigonometric_terms,
                residual_taylor_terms=residual_model_terms,
            )
            right_residual = _lifted_auxiliary_residual_cell(
                profile_cell,
                right_cell,
                source_cell_index=source_index,
                normalized_left=normalized_left,
                normalized_right=normalized_right,
                refinement_depth=0,
                domain_right=domain_right,
                domain_length=domain_length,
                lift_coefficient=zero_lift,
                pion_mass_squared=mass_squared,
                curvature=curvature_value,
                trigonometric_terms=trigonometric_terms,
                residual_taylor_terms=residual_model_terms,
            )
            left_l1 = _polynomial_subcell_l1_upper_bound(
                left_cell, normalized_left, normalized_right
            )
            right_l1 = _polynomial_subcell_l1_upper_bound(
                right_cell, normalized_left, normalized_right
            )
            leaves.append(
                (
                    source_index,
                    left_residual,
                    right_residual,
                    left_l1,
                    right_l1,
                )
            )

    left_prefixes: list[Fraction] = []
    accumulated = Fraction(0)
    for _, _, _, left_l1, _ in leaves:
        accumulated += left_l1
        left_prefixes.append(accumulated)
    right_suffixes = [Fraction(0)] * len(leaves)
    accumulated = Fraction(0)
    for index in reversed(range(len(leaves))):
        accumulated += leaves[index][4]
        right_suffixes[index] = accumulated

    checked: list[ValidatedSkyrmionGreenParametrixCell] = []
    wronskian_error = initial_wronskian_error
    for index, (
        source_index,
        left_residual,
        right_residual,
        left_l1,
        right_l1,
    ) in enumerate(leaves):
        left_residual_upper = _absolute_interval_upper(left_residual.residual)
        right_residual_upper = _absolute_interval_upper(right_residual.residual)
        wronskian_error += (
            left_residual_upper * right_l1
            + right_residual_upper * left_l1
        )
        relative_wronskian_error = wronskian_error / w0
        left_prefix = left_prefixes[index]
        right_suffix = right_suffixes[index]
        operator_defect = (
            relative_wronskian_error
            + left_residual_upper * right_suffix / w0
            + right_residual_upper * left_prefix / w0
        )
        left_c0 = _absolute_interval_upper(left_residual.auxiliary)
        left_c1 = _absolute_interval_upper(left_residual.derivative)
        left_c2 = _absolute_interval_upper(left_residual.second_derivative)
        right_c0 = _absolute_interval_upper(right_residual.auxiliary)
        right_c1 = _absolute_interval_upper(right_residual.derivative)
        right_c2 = _absolute_interval_upper(right_residual.second_derivative)
        approximate_c0 = (
            right_c0 * left_prefix + left_c0 * right_suffix
        ) / w0
        approximate_c1 = (
            right_c1 * left_prefix + left_c1 * right_suffix
        ) / w0
        principal_lower = left_residual.coefficients.principal.lower
        if principal_lower <= 0:
            raise ValueError(
                "Green-parametrix principal coefficient is not positive"
            )
        approximate_c2 = (
            (1 + relative_wronskian_error) / principal_lower
            + (right_c2 * left_prefix + left_c2 * right_suffix) / w0
        )
        checked.append(
            ValidatedSkyrmionGreenParametrixCell(
                source_cell_index=source_index,
                radius=left_residual.radius,
                left_residual=left_residual.residual,
                right_residual=right_residual.residual,
                left_l1_upper_bound=left_l1,
                right_l1_upper_bound=right_l1,
                left_prefix_l1_upper_bound=left_prefix,
                right_suffix_l1_upper_bound=right_suffix,
                relative_wronskian_error_upper_bound=(
                    relative_wronskian_error
                ),
                operator_defect_upper_bound=operator_defect,
                principal_lower_bound=principal_lower,
                approximate_c0_row_upper_bound=approximate_c0,
                approximate_c1_row_upper_bound=approximate_c1,
                approximate_c2_row_upper_bound=approximate_c2,
            )
        )

    defect = max(cell.operator_defect_upper_bound for cell in checked)
    if defect >= 1:
        raise ValueError(
            "Green-parametrix operator defect is not strictly below one"
        )
    approximate_c0 = max(
        cell.approximate_c0_row_upper_bound for cell in checked
    )
    approximate_c1 = max(
        cell.approximate_c1_row_upper_bound for cell in checked
    )
    approximate_c2 = max(
        cell.approximate_c2_row_upper_bound for cell in checked
    )
    neumann_factor = 1 / (1 - defect)
    return ValidatedSkyrmionGreenResolventBounds(
        profile_cells=tuple(profile_cells),
        left_fundamental_cells=tuple(left_fundamental_cells),
        right_representer_cells=tuple(right_representer_cells),
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        barta_validation=barta,
        cells=tuple(checked),
        wronskian_normalization=w0,
        initial_wronskian_enclosure=initial_wronskian,
        initial_wronskian_error_upper_bound=initial_wronskian_error,
        operator_defect_upper_bound=defect,
        approximate_c0_upper_bound=approximate_c0,
        approximate_c1_upper_bound=approximate_c1,
        approximate_c2_upper_bound=approximate_c2,
        c0_upper_bound=approximate_c0 * neumann_factor,
        c1_upper_bound=approximate_c1 * neumann_factor,
        c2_upper_bound=approximate_c2 * neumann_factor,
        source_cell_count=len(profile_cells),
        subdivisions_per_source_cell=subdivisions,
        conclusion_scope=(
            "exact approximate-profile Jacobi operator and exact rational "
            "Green-parametrix splines only; no nonlinear BVP existence conclusion"
        ),
    )


def _skyrmion_graph_resolvent_bounds(
    barta: ValidatedSkyrmionPolynomialBartaBound,
) -> ValidatedSkyrmionGraphResolventBounds:
    alpha = barta.recomputed_lower_bound
    if alpha <= 0:
        raise ValueError("Barta lower bound must be positive")
    domain_left = min(cell.jet.radius.lower for cell in barta.cells)
    domain_right = max(cell.jet.radius.upper for cell in barta.cells)
    domain_length = domain_right - domain_left
    witness_range = RationalInterval.point(8) / (
        (RationalInterval(domain_left, domain_right) - Fraction(33, 16)).power(2)
        + 4
    )
    witness_ratio = witness_range.upper / witness_range.lower
    principal_lower = min(
        cell.coefficients.principal.lower for cell in barta.cells
    )
    principal_derivative_supremum = max(
        _absolute_interval_upper(cell.coefficients.principal_derivative)
        for cell in barta.cells
    )
    potential_l1 = sum(
        cell.jet.radius.width
        * _absolute_interval_upper(cell.coefficients.potential)
        for cell in barta.cells
    )
    potential_supremum = max(
        _absolute_interval_upper(cell.coefficients.potential)
        for cell in barta.cells
    )
    c0 = witness_ratio / alpha
    c1 = (domain_length + potential_l1 * c0) / principal_lower
    c2 = (
        1
        + principal_derivative_supremum * c1
        + potential_supremum * c0
    ) / principal_lower
    return ValidatedSkyrmionGraphResolventBounds(
        barta_lower_bound=alpha,
        barta_witness_ratio_upper_bound=witness_ratio,
        domain_length=domain_length,
        principal_lower_bound=principal_lower,
        principal_derivative_supremum_upper_bound=(
            principal_derivative_supremum
        ),
        potential_l1_upper_bound=potential_l1,
        potential_supremum_upper_bound=potential_supremum,
        c0_upper_bound=c0,
        c1_upper_bound=c1,
        c2_upper_bound=c2,
    )


def _skyrmion_lifted_auxiliary_norm_bounds(
    auxiliary_cells: Sequence[SkyrmionPolynomialCell],
    *,
    lift_coefficient: RationalInterval,
    domain_right: Fraction,
    domain_length: Fraction,
    residual_supremum: Fraction,
    graph_bounds: (
        ValidatedSkyrmionGraphResolventBounds
        | ValidatedSkyrmionGreenResolventBounds
    ),
) -> ValidatedSkyrmionAuxiliaryNormBounds:
    approximate_c0 = Fraction(0)
    approximate_c1 = Fraction(0)
    approximate_c2 = Fraction(0)
    lift_derivative = lift_coefficient.scale(-1 / domain_length)
    for cell in auxiliary_cells:
        jet = _polynomial_subcell_jet(cell, Fraction(0), Fraction(1))
        affine_factor = (
            RationalInterval.point(domain_right) - jet.radius
        ).scale(1 / domain_length)
        lifted_function = jet.profile + lift_coefficient * affine_factor
        lifted_derivative = jet.derivative + lift_derivative
        approximate_c0 = max(
            approximate_c0, _absolute_interval_upper(lifted_function)
        )
        approximate_c1 = max(
            approximate_c1, _absolute_interval_upper(lifted_derivative)
        )
        approximate_c2 = max(
            approximate_c2, _absolute_interval_upper(jet.second_derivative)
        )
    return ValidatedSkyrmionAuxiliaryNormBounds(
        approximate_c0_upper_bound=approximate_c0,
        approximate_c1_upper_bound=approximate_c1,
        approximate_c2_upper_bound=approximate_c2,
        residual_supremum_upper_bound=residual_supremum,
        corrected_c0_upper_bound=(
            approximate_c0 + graph_bounds.c0_upper_bound * residual_supremum
        ),
        corrected_c1_upper_bound=(
            approximate_c1 + graph_bounds.c1_upper_bound * residual_supremum
        ),
        corrected_c2_upper_bound=(
            approximate_c2 + graph_bounds.c2_upper_bound * residual_supremum
        ),
    )


def validate_skyrmion_trace_sharpened_schur_bound(
    profile_cells: Sequence[SkyrmionPolynomialCell],
    auxiliary_cells: Sequence[SkyrmionPolynomialCell],
    representer_cells: Sequence[SkyrmionPolynomialCell],
    phi_b: RationalInterval,
    gamma_b: RationalInterval,
    declared_barta_lower_bound: Fraction,
    declared_trace_upper_bound: Fraction,
    declared_schur_lower_bound: Fraction,
    *,
    barta_initial_subdivisions: int = 4,
    barta_maximum_refinement_depth: int = 3,
    trace_residual_initial_subdivisions: int = 4,
    trace_residual_maximum_refinement_depth: int = 3,
    schur_residual_initial_subdivisions: int = 4,
    schur_residual_maximum_refinement_depth: int = 3,
    pion_mass_squared: Fraction = Fraction(1),
    curvature: Fraction = Fraction(1, 400),
    trigonometric_terms: int = 40,
    residual_taylor_terms: int = 8,
) -> ValidatedSkyrmionTraceSharpenedSchurBound:
    """Validate a Schur margin using an independently ordered trace audit.

    The representer is certified first using only Barta coercivity and the
    maximum-principle ``C0`` residual correction.  Its recomputed ``C_tau`` is
    then used to bound the derivative error of the lifted Schur auxiliary.
    The ordering remains valid even when both approximations are derived from
    the same proposal spline because ``C_tau`` is not used to certify itself.

    As with the component validators, the conclusion concerns the exact
    approximate-profile Jacobi operator and does not prove nonlinear BVP
    existence.
    """
    if not isinstance(phi_b, RationalInterval):
        raise TypeError("phi_b must be a RationalInterval")
    if not isinstance(gamma_b, RationalInterval):
        raise TypeError("gamma_b must be a RationalInterval")
    declared_schur = _fraction(
        "declared_schur_lower_bound", declared_schur_lower_bound
    )
    if declared_schur <= 0:
        raise ValueError("declared_schur_lower_bound must be positive")
    residual_subdivisions = _positive_integer(
        "schur_residual_initial_subdivisions",
        schur_residual_initial_subdivisions,
    )
    residual_depth_limit = _nonnegative_integer(
        "schur_residual_maximum_refinement_depth",
        schur_residual_maximum_refinement_depth,
    )
    residual_model_terms = _positive_integer(
        "residual_taylor_terms", residual_taylor_terms
    )
    mass_squared = _nonnegative_fraction(
        "pion_mass_squared", pion_mass_squared
    )
    curvature_value = _nonnegative_fraction("curvature", curvature)

    trace_validation = validate_skyrmion_derivative_trace_representer(
        profile_cells,
        representer_cells,
        declared_barta_lower_bound,
        declared_trace_upper_bound,
        barta_initial_subdivisions=barta_initial_subdivisions,
        barta_maximum_refinement_depth=barta_maximum_refinement_depth,
        residual_initial_subdivisions=trace_residual_initial_subdivisions,
        residual_maximum_refinement_depth=(
            trace_residual_maximum_refinement_depth
        ),
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        trigonometric_terms=trigonometric_terms,
        residual_taylor_terms=residual_model_terms,
    )
    _validate_matching_auxiliary_cells(profile_cells, auxiliary_cells)
    domain_left = profile_cells[0].radius.lower
    domain_right = profile_cells[-1].radius.upper
    domain_length = domain_right - domain_left
    auxiliary_left = auxiliary_cells[0].profile_polynomial.evaluate(Fraction(0))
    auxiliary_left_derivative = (
        auxiliary_cells[0]
        .profile_polynomial.derivative()
        .evaluate(Fraction(0))
        .scale(1 / auxiliary_cells[0].radius.width)
    )
    lift_coefficient = phi_b - auxiliary_left
    lift_derivative = lift_coefficient.scale(-1 / domain_length)
    raw_schur = auxiliary_left_derivative + lift_derivative - gamma_b
    trace_upper = trace_validation.recomputed_trace_upper_bound
    residual_budget = (
        (raw_schur.lower - declared_schur) / trace_upper
        if raw_schur.lower > declared_schur
        else Fraction(0)
    )

    checked_residuals: list[ValidatedSkyrmionSchurResidualCell] = []
    maximum_depth_used = 0
    for source_index, (profile_cell, auxiliary_cell) in enumerate(
        zip(profile_cells, auxiliary_cells)
    ):
        pending = [
            (
                Fraction(index, residual_subdivisions),
                Fraction(index + 1, residual_subdivisions),
                0,
            )
            for index in reversed(range(residual_subdivisions))
        ]
        while pending:
            left, right, depth = pending.pop()
            checked = _lifted_auxiliary_residual_cell(
                profile_cell,
                auxiliary_cell,
                source_cell_index=source_index,
                normalized_left=left,
                normalized_right=right,
                refinement_depth=depth,
                domain_right=domain_right,
                domain_length=domain_length,
                lift_coefficient=lift_coefficient,
                pion_mass_squared=mass_squared,
                curvature=curvature_value,
                trigonometric_terms=trigonometric_terms,
                residual_taylor_terms=residual_model_terms,
            )
            if (
                _absolute_interval_upper(checked.residual) > residual_budget
                and depth < residual_depth_limit
            ):
                midpoint = (left + right) / 2
                pending.append((midpoint, right, depth + 1))
                pending.append((left, midpoint, depth + 1))
                continue
            maximum_depth_used = max(maximum_depth_used, depth)
            checked_residuals.append(checked)

    residual_supremum = max(
        _absolute_interval_upper(cell.residual) for cell in checked_residuals
    )
    derivative_error = trace_upper * residual_supremum
    corrected_schur = RationalInterval(
        raw_schur.lower - derivative_error,
        raw_schur.upper + derivative_error,
    )
    if corrected_schur.lower < declared_schur:
        raise ValueError(
            "declared positive trace-sharpened Schur lower bound is not "
            "verified after the trusted residual correction"
        )
    graph_bounds = _skyrmion_graph_resolvent_bounds(
        trace_validation.barta_validation
    )
    auxiliary_norm_bounds = _skyrmion_lifted_auxiliary_norm_bounds(
        auxiliary_cells,
        lift_coefficient=lift_coefficient,
        domain_right=domain_right,
        domain_length=domain_length,
        residual_supremum=residual_supremum,
        graph_bounds=graph_bounds,
    )

    return ValidatedSkyrmionTraceSharpenedSchurBound(
        profile_cells=tuple(profile_cells),
        auxiliary_cells=tuple(auxiliary_cells),
        pion_mass_squared=mass_squared,
        curvature=curvature_value,
        trace_validation=trace_validation,
        graph_resolvent_bounds=graph_bounds,
        auxiliary_norm_bounds=auxiliary_norm_bounds,
        residual_cells=tuple(checked_residuals),
        phi_b=phi_b,
        gamma_b=gamma_b,
        affine_left_lift_coefficient=lift_coefficient,
        affine_left_lift_derivative=lift_derivative,
        raw_schur_enclosure=raw_schur,
        residual_supremum_upper_bound=residual_supremum,
        derivative_trace_upper_bound=trace_upper,
        boundary_derivative_error_bound=derivative_error,
        corrected_schur_enclosure=corrected_schur,
        declared_schur_lower_bound=declared_schur,
        maximum_residual_refinement_depth=residual_depth_limit,
        maximum_residual_refinement_depth_used=maximum_depth_used,
        conclusion_scope=(
            "exact approximate profile Jacobi operator, certified derivative "
            "trace representer, and affinely lifted auxiliary family only; "
            "no nonlinear BVP existence conclusion"
        ),
    )


def sharpen_skyrmion_schur_with_green_resolvent(
    schur_validation: ValidatedSkyrmionTraceSharpenedSchurBound,
    green_validation: ValidatedSkyrmionGreenResolventBounds,
) -> ValidatedSkyrmionTraceSharpenedSchurBound:
    """Replace elementary graph norms by a same-operator Green certificate."""
    if not isinstance(
        schur_validation, ValidatedSkyrmionTraceSharpenedSchurBound
    ):
        raise TypeError("schur_validation must be trace-sharpened")
    if not isinstance(green_validation, ValidatedSkyrmionGreenResolventBounds):
        raise TypeError("green_validation must be a Green resolvent bound")
    if schur_validation.profile_cells != green_validation.profile_cells:
        raise ValueError("Schur and Green validations must use the same profile")
    if (
        schur_validation.pion_mass_squared
        != green_validation.pion_mass_squared
        or schur_validation.curvature != green_validation.curvature
    ):
        raise ValueError("Schur and Green operator parameters must agree")
    domain_left = schur_validation.profile_cells[0].radius.lower
    domain_right = schur_validation.profile_cells[-1].radius.upper
    domain_length = domain_right - domain_left
    auxiliary_norms = _skyrmion_lifted_auxiliary_norm_bounds(
        schur_validation.auxiliary_cells,
        lift_coefficient=schur_validation.affine_left_lift_coefficient,
        domain_right=domain_right,
        domain_length=domain_length,
        residual_supremum=schur_validation.residual_supremum_upper_bound,
        graph_bounds=green_validation,
    )
    return replace(
        schur_validation,
        graph_resolvent_bounds=green_validation,
        auxiliary_norm_bounds=auxiliary_norms,
        conclusion_scope=(
            "exact approximate-profile Jacobi operator, certified derivative "
            "trace and Schur bounds, and certified Green-parametrix resolvent "
            "norms only; no nonlinear BVP existence conclusion"
        ),
    )


def _skyrmion_weighted_trace_upper_bound(
    trace_validation: ValidatedSkyrmionDerivativeTraceBound,
    source_cell_bounds: Sequence[tuple[int, Fraction]],
    *,
    inverse_c0_upper_bound: Fraction | None = None,
) -> Fraction:
    """Bound the derivative trace using certified cellwise forcing bounds."""

    bounds: dict[int, Fraction] = {}
    for source_cell_index, value in source_cell_bounds:
        bound = _fraction("source_cell_bound", value)
        if bound < 0:
            raise ValueError("source cell bounds must be nonnegative")
        bounds[source_cell_index] = max(
            bounds.get(source_cell_index, Fraction(0)),
            bound,
        )
    expected = {cell.source_cell_index for cell in trace_validation.l1_cells}
    if set(bounds) != expected:
        raise ValueError("weighted trace bounds must cover every source cell")
    approximate = sum(
        cell.l1_upper_bound * bounds[cell.source_cell_index]
        for cell in trace_validation.l1_cells
    )
    correction_c0 = (
        trace_validation.inverse_c0_bound
        if inverse_c0_upper_bound is None
        else _fraction("inverse_c0_upper_bound", inverse_c0_upper_bound)
    )
    if correction_c0 <= 0:
        raise ValueError("inverse C0 upper bound must be positive")
    representer_error_supremum = (
        correction_c0 * trace_validation.residual_supremum_upper_bound
    )
    correction = representer_error_supremum * sum(
        cell.radius.width * bounds[cell.source_cell_index]
        for cell in trace_validation.l1_cells
    )
    return (
        approximate + correction
    ) / trace_validation.principal_left_lower_bound


def validate_skyrmion_augmented_operator_mismatch(
    schur_validation: ValidatedSkyrmionTraceSharpenedSchurBound,
    endpoint_validation: ValidatedSkyrmionEndpointCorrectedResidual,
    *,
    omega: Fraction = Fraction(1),
    scalar_weight: Fraction = Fraction(1),
) -> ValidatedSkyrmionAugmentedOperatorMismatch:
    """Bound the Newton derivative mismatch between ``F_hat`` and ``F_bar``.

    The coefficient differences are bounded by integrating exact analytic
    derivatives of ``P``, ``P'``, and ``Q`` over the endpoint-corrected profile
    family.  The resulting operator bound is composed with the same validated
    graph and auxiliary norms and the exact augmented block-inverse estimate.
    """
    if not isinstance(
        schur_validation, ValidatedSkyrmionTraceSharpenedSchurBound
    ):
        raise TypeError(
            "schur_validation must be a trace-sharpened Schur validation"
        )
    if not isinstance(
        endpoint_validation, ValidatedSkyrmionEndpointCorrectedResidual
    ):
        raise TypeError(
            "endpoint_validation must be an endpoint-corrected residual"
        )
    if schur_validation.profile_cells != endpoint_validation.profile_cells:
        raise ValueError(
            "Schur and endpoint validations must use the same exact profile spline"
        )
    if (
        schur_validation.pion_mass_squared
        != endpoint_validation.pion_mass_squared
        or schur_validation.curvature != endpoint_validation.curvature
    ):
        raise ValueError(
            "Schur and endpoint validations must use the same operator parameters"
        )
    if (
        endpoint_validation.phi_sensitivity_at_cutoff is None
        or endpoint_validation.gamma_sensitivity_at_cutoff is None
    ):
        raise ValueError(
            "endpoint validation must carry the origin sensitivities used by Schur"
        )
    if (
        endpoint_validation.phi_sensitivity_at_cutoff != schur_validation.phi_b
        or endpoint_validation.gamma_sensitivity_at_cutoff
        != schur_validation.gamma_b
    ):
        raise ValueError(
            "Schur and endpoint validations must use identical origin sensitivities"
        )
    omega_value = _fraction("omega", omega)
    scalar_weight_value = _fraction("scalar_weight", scalar_weight)
    if omega_value <= 0 or scalar_weight_value <= 0:
        raise ValueError("omega and scalar_weight must be positive")
    mass_squared = schur_validation.pion_mass_squared
    curvature_value = schur_validation.curvature
    graph = schur_validation.graph_resolvent_bounds
    auxiliary = schur_validation.auxiliary_norm_bounds
    domain_left = endpoint_validation.profile_cells[0].radius.lower
    domain_right = endpoint_validation.profile_cells[-1].radius.upper
    domain_length = domain_right - domain_left
    left_correction = endpoint_validation.left_value_correction
    right_correction = endpoint_validation.right_value_correction
    derivative_correction = (
        left_correction.scale(-1 / domain_length)
        + RationalInterval.point(right_correction / domain_length)
    )
    derivative_correction_upper = _absolute_interval_upper(
        derivative_correction
    )
    checked: list[ValidatedSkyrmionOperatorMismatchCell] = []
    for cell in endpoint_validation.cells:
        radius = cell.radius
        chi_left = (
            RationalInterval.point(domain_right) - radius
        ).scale(1 / domain_length)
        chi_right = (
            radius - RationalInterval.point(domain_left)
        ).scale(1 / domain_length)
        profile_correction = (
            left_correction * chi_left
            + RationalInterval.point(right_correction) * chi_right
        )
        profile_correction_upper = _absolute_interval_upper(
            profile_correction
        )
        lapse_upper = Fraction(1) - curvature_value * radius.lower**2
        lapse_derivative_upper = 2 * curvature_value * radius.upper
        derivative_upper = _absolute_interval_upper(
            cell.family_profile_jet.derivative
        ) + derivative_correction_upper
        second_derivative_upper = _absolute_interval_upper(
            cell.family_profile_jet.second_derivative
        )
        principal_difference = (
            8 * lapse_upper * profile_correction_upper
        )
        principal_derivative_difference = (
            (
                8 * lapse_derivative_upper
                + 16 * lapse_upper * derivative_upper
            )
            * profile_correction_upper
            + 8 * lapse_upper * derivative_correction_upper
        )
        q_f_upper = (
            4
            + Fraction(40, 1) / radius.lower**2
            + 16 * lapse_upper * derivative_upper**2
            + mass_squared * radius.upper**2
            + 16 * lapse_derivative_upper * derivative_upper
            + 16 * lapse_upper * second_derivative_upper
        )
        q_f_prime_upper = (
            16 * lapse_upper * derivative_upper
            + 8 * lapse_derivative_upper
        )
        potential_difference = (
            q_f_upper * profile_correction_upper
            + q_f_prime_upper * derivative_correction_upper
        )
        graph_mismatch = (
            principal_difference * graph.c2_upper_bound
            + principal_derivative_difference * graph.c1_upper_bound
            + potential_difference * graph.c0_upper_bound
        )
        auxiliary_mismatch = (
            principal_difference * auxiliary.corrected_c2_upper_bound
            + principal_derivative_difference
            * auxiliary.corrected_c1_upper_bound
            + potential_difference * auxiliary.corrected_c0_upper_bound
        )
        interior_mismatch = graph_mismatch + auxiliary_mismatch / omega_value
        checked.append(
            ValidatedSkyrmionOperatorMismatchCell(
                source_cell_index=cell.source_cell_index,
                radius=radius,
                profile_correction_supremum_upper_bound=(
                    profile_correction_upper
                ),
                derivative_correction_supremum_upper_bound=(
                    derivative_correction_upper
                ),
                principal_difference_upper_bound=principal_difference,
                principal_derivative_difference_upper_bound=(
                    principal_derivative_difference
                ),
                potential_difference_upper_bound=potential_difference,
                graph_operator_mismatch_upper_bound=graph_mismatch,
                auxiliary_operator_mismatch_upper_bound=auxiliary_mismatch,
                interior_operator_mismatch_upper_bound=interior_mismatch,
            )
        )
    interior_mismatch = max(
        cell.interior_operator_mismatch_upper_bound for cell in checked
    )
    schur_lower = schur_validation.corrected_schur_enclosure.lower
    inverse_upper = max(
        Fraction(1),
        omega_value
        / schur_lower
        * (
            schur_validation.derivative_trace_upper_bound
            + Fraction(1, 1) / scalar_weight_value
        ),
    )
    nonlinear_residual = endpoint_validation.residual_supremum_upper_bound
    residual_trace = _skyrmion_weighted_trace_upper_bound(
        schur_validation.trace_validation,
        tuple(
            (
                cell.source_cell_index,
                _absolute_interval_upper(cell.residual),
            )
            for cell in endpoint_validation.cells
        ),
        inverse_c0_upper_bound=(
            schur_validation.graph_resolvent_bounds.c0_upper_bound
        ),
    )
    mismatch_trace = _skyrmion_weighted_trace_upper_bound(
        schur_validation.trace_validation,
        tuple(
            (
                cell.source_cell_index,
                cell.interior_operator_mismatch_upper_bound,
            )
            for cell in checked
        ),
        inverse_c0_upper_bound=(
            schur_validation.graph_resolvent_bounds.c0_upper_bound
        ),
    )
    boundary_slope_residual = _absolute_interval_upper(
        endpoint_validation.boundary_slope_residual
    )
    newton_defect = max(
        nonlinear_residual,
        omega_value
        / schur_lower
        * (
            boundary_slope_residual
            + residual_trace
        ),
    )
    z0 = max(
        interior_mismatch,
        omega_value / schur_lower * mismatch_trace,
    )
    return ValidatedSkyrmionAugmentedOperatorMismatch(
        profile_cells=endpoint_validation.profile_cells,
        cells=tuple(checked),
        pion_mass_squared=endpoint_validation.pion_mass_squared,
        curvature=endpoint_validation.curvature,
        phi_at_cutoff=endpoint_validation.phi_at_cutoff,
        gamma_at_cutoff=endpoint_validation.gamma_at_cutoff,
        phi_sensitivity_at_cutoff=(
            endpoint_validation.phi_sensitivity_at_cutoff
        ),
        gamma_sensitivity_at_cutoff=(
            endpoint_validation.gamma_sensitivity_at_cutoff
        ),
        left_value_correction=endpoint_validation.left_value_correction,
        right_value_correction=endpoint_validation.right_value_correction,
        omega=omega_value,
        scalar_weight=scalar_weight_value,
        augmented_inverse_upper_bound=inverse_upper,
        nonlinear_residual_supremum_upper_bound=nonlinear_residual,
        nonlinear_residual_trace_upper_bound=residual_trace,
        boundary_slope_residual_absolute_upper_bound=(
            boundary_slope_residual
        ),
        newton_defect_upper_bound=newton_defect,
        interior_operator_mismatch_upper_bound=interior_mismatch,
        operator_mismatch_trace_upper_bound=mismatch_trace,
        z0_upper_bound=z0,
        conclusion_scope=(
            "derivative mismatch between the exact approximate-profile "
            "operator and its endpoint-corrected center family only; no "
            "nonlinear Newton-radius conclusion"
        ),
    )


def reweight_skyrmion_augmented_operator_mismatch(
    schur_validation: ValidatedSkyrmionTraceSharpenedSchurBound,
    endpoint_validation: ValidatedSkyrmionEndpointCorrectedResidual,
    mismatch_validation: ValidatedSkyrmionAugmentedOperatorMismatch,
    *,
    omega: Fraction,
    scalar_weight: Fraction = Fraction(1),
) -> ValidatedSkyrmionAugmentedOperatorMismatch:
    """Recompose validated coefficient differences in another product norm."""
    if not isinstance(
        mismatch_validation, ValidatedSkyrmionAugmentedOperatorMismatch
    ):
        raise TypeError("mismatch_validation must be validated")
    if schur_validation.profile_cells != endpoint_validation.profile_cells:
        raise ValueError("Schur and endpoint profile splines must agree")
    if (
        schur_validation.pion_mass_squared
        != endpoint_validation.pion_mass_squared
        or schur_validation.curvature != endpoint_validation.curvature
    ):
        raise ValueError("Schur and endpoint operator parameters must agree")
    if (
        endpoint_validation.phi_sensitivity_at_cutoff
        != schur_validation.phi_b
        or endpoint_validation.gamma_sensitivity_at_cutoff
        != schur_validation.gamma_b
    ):
        raise ValueError("Schur and endpoint origin sensitivities must agree")
    if len(mismatch_validation.cells) != len(endpoint_validation.cells):
        raise ValueError("mismatch cells do not cover the endpoint audit")
    if (
        mismatch_validation.profile_cells != endpoint_validation.profile_cells
        or mismatch_validation.pion_mass_squared
        != endpoint_validation.pion_mass_squared
        or mismatch_validation.curvature != endpoint_validation.curvature
        or mismatch_validation.phi_at_cutoff
        != endpoint_validation.phi_at_cutoff
        or mismatch_validation.gamma_at_cutoff
        != endpoint_validation.gamma_at_cutoff
        or mismatch_validation.phi_sensitivity_at_cutoff
        != endpoint_validation.phi_sensitivity_at_cutoff
        or mismatch_validation.gamma_sensitivity_at_cutoff
        != endpoint_validation.gamma_sensitivity_at_cutoff
        or mismatch_validation.left_value_correction
        != endpoint_validation.left_value_correction
        or mismatch_validation.right_value_correction
        != endpoint_validation.right_value_correction
    ):
        raise ValueError("mismatch endpoint provenance does not match")
    for mismatch_cell, endpoint_cell in zip(
        mismatch_validation.cells,
        endpoint_validation.cells,
    ):
        if (
            mismatch_cell.source_cell_index != endpoint_cell.source_cell_index
            or mismatch_cell.radius != endpoint_cell.radius
        ):
            raise ValueError("mismatch cell provenance does not match")
    omega_value = _fraction("omega", omega)
    scalar_weight_value = _fraction("scalar_weight", scalar_weight)
    if omega_value <= 0 or scalar_weight_value <= 0:
        raise ValueError("omega and scalar_weight must be positive")
    graph = schur_validation.graph_resolvent_bounds
    auxiliary = schur_validation.auxiliary_norm_bounds
    checked = tuple(
        ValidatedSkyrmionOperatorMismatchCell(
            source_cell_index=cell.source_cell_index,
            radius=cell.radius,
            profile_correction_supremum_upper_bound=(
                cell.profile_correction_supremum_upper_bound
            ),
            derivative_correction_supremum_upper_bound=(
                cell.derivative_correction_supremum_upper_bound
            ),
            principal_difference_upper_bound=(
                cell.principal_difference_upper_bound
            ),
            principal_derivative_difference_upper_bound=(
                cell.principal_derivative_difference_upper_bound
            ),
            potential_difference_upper_bound=(
                cell.potential_difference_upper_bound
            ),
            graph_operator_mismatch_upper_bound=(
                cell.graph_operator_mismatch_upper_bound
            ),
            auxiliary_operator_mismatch_upper_bound=(
                cell.auxiliary_operator_mismatch_upper_bound
            ),
            interior_operator_mismatch_upper_bound=(
                cell.graph_operator_mismatch_upper_bound
                + cell.auxiliary_operator_mismatch_upper_bound / omega_value
            ),
        )
        for cell in mismatch_validation.cells
    )
    interior_mismatch = max(
        cell.interior_operator_mismatch_upper_bound for cell in checked
    )
    schur_lower = schur_validation.corrected_schur_enclosure.lower
    inverse_upper = max(
        Fraction(1),
        omega_value
        / schur_lower
        * (
            schur_validation.derivative_trace_upper_bound
            + Fraction(1) / scalar_weight_value
        ),
    )
    nonlinear_residual = endpoint_validation.residual_supremum_upper_bound
    residual_trace = _skyrmion_weighted_trace_upper_bound(
        schur_validation.trace_validation,
        tuple(
            (
                cell.source_cell_index,
                _absolute_interval_upper(cell.residual),
            )
            for cell in endpoint_validation.cells
        ),
        inverse_c0_upper_bound=(
            schur_validation.graph_resolvent_bounds.c0_upper_bound
        ),
    )
    mismatch_trace = _skyrmion_weighted_trace_upper_bound(
        schur_validation.trace_validation,
        tuple(
            (
                cell.source_cell_index,
                cell.interior_operator_mismatch_upper_bound,
            )
            for cell in checked
        ),
        inverse_c0_upper_bound=(
            schur_validation.graph_resolvent_bounds.c0_upper_bound
        ),
    )
    boundary_slope_residual = _absolute_interval_upper(
        endpoint_validation.boundary_slope_residual
    )
    newton_defect = max(
        nonlinear_residual,
        omega_value
        / schur_lower
        * (
            boundary_slope_residual
            + residual_trace
        ),
    )
    z0 = max(
        interior_mismatch,
        omega_value / schur_lower * mismatch_trace,
    )
    return ValidatedSkyrmionAugmentedOperatorMismatch(
        profile_cells=mismatch_validation.profile_cells,
        cells=checked,
        pion_mass_squared=mismatch_validation.pion_mass_squared,
        curvature=mismatch_validation.curvature,
        phi_at_cutoff=mismatch_validation.phi_at_cutoff,
        gamma_at_cutoff=mismatch_validation.gamma_at_cutoff,
        phi_sensitivity_at_cutoff=(
            mismatch_validation.phi_sensitivity_at_cutoff
        ),
        gamma_sensitivity_at_cutoff=(
            mismatch_validation.gamma_sensitivity_at_cutoff
        ),
        left_value_correction=mismatch_validation.left_value_correction,
        right_value_correction=mismatch_validation.right_value_correction,
        omega=omega_value,
        scalar_weight=scalar_weight_value,
        augmented_inverse_upper_bound=inverse_upper,
        nonlinear_residual_supremum_upper_bound=nonlinear_residual,
        nonlinear_residual_trace_upper_bound=residual_trace,
        boundary_slope_residual_absolute_upper_bound=boundary_slope_residual,
        newton_defect_upper_bound=newton_defect,
        interior_operator_mismatch_upper_bound=interior_mismatch,
        operator_mismatch_trace_upper_bound=mismatch_trace,
        z0_upper_bound=z0,
        conclusion_scope=mismatch_validation.conclusion_scope,
    )


def _skyrmion_local_newton_norm_bounds(
    schur_validation: ValidatedSkyrmionTraceSharpenedSchurBound,
    source_cell_index: int,
) -> tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]:
    """Return rigorous row-local graph and corrected auxiliary norms."""

    graph = schur_validation.graph_resolvent_bounds
    auxiliary = schur_validation.auxiliary_norm_bounds
    if not isinstance(graph, ValidatedSkyrmionGreenResolventBounds):
        return (
            graph.c0_upper_bound,
            graph.c1_upper_bound,
            graph.c2_upper_bound,
            auxiliary.corrected_c0_upper_bound,
            auxiliary.corrected_c1_upper_bound,
            auxiliary.corrected_c2_upper_bound,
        )

    rows = tuple(
        cell
        for cell in graph.cells
        if cell.source_cell_index == source_cell_index
    )
    if not rows:
        raise ValueError("Green certificate does not cover the Newton source cell")
    neumann_factor = Fraction(1) / (1 - graph.operator_defect_upper_bound)
    local_c0 = max(
        cell.approximate_c0_row_upper_bound for cell in rows
    ) * neumann_factor
    local_c1 = max(
        cell.approximate_c1_row_upper_bound for cell in rows
    ) * neumann_factor
    local_c2 = max(
        cell.approximate_c2_row_upper_bound for cell in rows
    ) * neumann_factor

    auxiliary_cell = schur_validation.auxiliary_cells[source_cell_index]
    jet = _polynomial_subcell_jet(auxiliary_cell, Fraction(0), Fraction(1))
    domain_right = schur_validation.profile_cells[-1].radius.upper
    domain_left = schur_validation.profile_cells[0].radius.lower
    domain_length = domain_right - domain_left
    affine_factor = (
        RationalInterval.point(domain_right) - jet.radius
    ).scale(1 / domain_length)
    lifted_profile = (
        jet.profile
        + schur_validation.affine_left_lift_coefficient * affine_factor
    )
    lifted_derivative = (
        jet.derivative + schur_validation.affine_left_lift_derivative
    )
    residual = schur_validation.residual_supremum_upper_bound
    local_h0 = _absolute_interval_upper(lifted_profile) + local_c0 * residual
    local_h1 = _absolute_interval_upper(lifted_derivative) + local_c1 * residual
    local_h2 = (
        _absolute_interval_upper(jet.second_derivative) + local_c2 * residual
    )
    return local_c0, local_c1, local_c2, local_h0, local_h1, local_h2


def validate_skyrmion_augmented_newton_tube(
    schur_validation: ValidatedSkyrmionTraceSharpenedSchurBound,
    endpoint_validation: ValidatedSkyrmionEndpointCorrectedResidual,
    mismatch_validation: ValidatedSkyrmionAugmentedOperatorMismatch,
    branch_identification: ValidatedSkyrmionOriginQuinticBranchIdentification,
    second_sensitivity: ValidatedSkyrmionOriginSecondSensitivity,
    radius: Fraction,
    *,
    trigonometric_terms: int = 24,
    rounding_denominator: int | None = None,
) -> ValidatedSkyrmionAugmentedNewtonTubeBound:
    """Evaluate the exact augmented Newton radii inequalities at ``radius``.

    The Hessian is composed directly with the certified Schur block inverse.
    A returned object proves a nearby nonlinear BVP solution only when both
    ``self_map_verified`` and ``contraction_verified`` are true.
    """
    if not isinstance(
        branch_identification,
        ValidatedSkyrmionOriginQuinticBranchIdentification,
    ):
        raise TypeError("branch_identification must be a validated origin link")
    if not isinstance(
        second_sensitivity,
        ValidatedSkyrmionOriginSecondSensitivity,
    ):
        raise TypeError("second_sensitivity must be validated")
    radius_value = _fraction("radius", radius)
    if radius_value <= 0:
        raise ValueError("radius must be positive")
    terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    if rounding_denominator is not None:
        rounding_denominator = _positive_integer(
            "rounding_denominator",
            rounding_denominator,
        )

    def round_interval(value: RationalInterval) -> RationalInterval:
        return (
            value
            if rounding_denominator is None
            else _outward_round_interval(value, rounding_denominator)
        )

    def round_upper(value: Fraction) -> Fraction:
        if value < 0:
            raise ValueError("upper-bound rounding requires a nonnegative value")
        return (
            value
            if rounding_denominator is None
            else _upward_round_fraction(value, rounding_denominator)
        )
    expected_mismatch = reweight_skyrmion_augmented_operator_mismatch(
        schur_validation,
        endpoint_validation,
        mismatch_validation,
        omega=mismatch_validation.omega,
        scalar_weight=mismatch_validation.scalar_weight,
    )
    if mismatch_validation != expected_mismatch:
        raise ValueError("mismatch validation does not match the supplied audits")
    patch = branch_identification.quintic_patch
    narrow_sensitivity = branch_identification.cubic_sensitivity
    if not branch_identification.identified_with_cubic_sensitivity_branch:
        raise ValueError("quintic and cubic origin branches are not identified")
    if endpoint_validation.phi_at_cutoff != patch.profile_at_cutoff:
        raise ValueError("endpoint profile data do not match the quintic branch")
    if endpoint_validation.gamma_at_cutoff != patch.derivative_at_cutoff:
        raise ValueError("endpoint derivative data do not match the quintic branch")
    if (
        patch.pion_mass_squared != schur_validation.pion_mass_squared
        or patch.curvature != schur_validation.curvature
    ):
        raise ValueError("origin and positive-radius operator parameters differ")
    if (
        endpoint_validation.phi_sensitivity_at_cutoff
        != narrow_sensitivity.phi_b
        or endpoint_validation.gamma_sensitivity_at_cutoff
        != narrow_sensitivity.gamma_b
    ):
        raise ValueError("endpoint sensitivities do not match the identified branch")
    if (
        second_sensitivity.cutoff != patch.cutoff
        or second_sensitivity.pion_mass_squared != patch.pion_mass_squared
        or second_sensitivity.curvature != patch.curvature
    ):
        raise ValueError("second-sensitivity operator provenance does not match")
    if not narrow_sensitivity.shooting_slopes.is_subset_of(
        second_sensitivity.shooting_slopes
    ):
        raise ValueError("second-sensitivity slope family misses the center branch")
    if second_sensitivity.remainder_radius < narrow_sensitivity.remainder_radius:
        raise ValueError("second-sensitivity cubic ball does not contain the branch")
    omega = mismatch_validation.omega
    slope_tube = RationalInterval(
        patch.shooting_slope - radius_value / omega,
        patch.shooting_slope + radius_value / omega,
    )
    if not slope_tube.is_subset_of(second_sensitivity.shooting_slopes):
        raise ValueError("Newton slope tube exceeds the second-sensitivity family")

    phi2 = round_upper(_absolute_interval_upper(
        second_sensitivity.profile_second_sensitivity_at_cutoff
    ))
    gamma2 = round_upper(_absolute_interval_upper(
        second_sensitivity.derivative_second_sensitivity_at_cutoff
    ))
    graph = schur_validation.graph_resolvent_bounds
    auxiliary = schur_validation.auxiliary_norm_bounds
    domain_left = endpoint_validation.profile_cells[0].radius.lower
    domain_right = endpoint_validation.profile_cells[-1].radius.upper
    if patch.cutoff != domain_left:
        raise ValueError("origin cutoff does not match the positive-radius domain")
    domain_length = domain_right - domain_left
    checked: list[ValidatedSkyrmionNewtonTubeCell] = []
    maximum_delta0 = Fraction(0)
    maximum_delta1 = Fraction(0)
    maximum_delta2 = Fraction(0)
    for cell in endpoint_validation.cells:
        (
            local_graph_c0,
            local_graph_c1,
            local_graph_c2,
            local_auxiliary_c0,
            local_auxiliary_c1,
            local_auxiliary_c2,
        ) = _skyrmion_local_newton_norm_bounds(
            schur_validation,
            cell.source_cell_index,
        )
        local_graph_c0 = round_upper(local_graph_c0)
        local_graph_c1 = round_upper(local_graph_c1)
        local_graph_c2 = round_upper(local_graph_c2)
        local_auxiliary_c0 = round_upper(local_auxiliary_c0)
        local_auxiliary_c1 = round_upper(local_auxiliary_c1)
        local_auxiliary_c2 = round_upper(local_auxiliary_c2)
        base_c0 = local_graph_c0 + local_auxiliary_c0 / omega
        base_c1 = local_graph_c1 + local_auxiliary_c1 / omega
        base_c2 = local_graph_c2 + local_auxiliary_c2 / omega
        first_c0 = round_upper(base_c0 + phi2 * radius_value / omega**2)
        first_c1 = round_upper(
            base_c1
            + phi2 * radius_value / (domain_length * omega**2)
        )
        first_c2 = round_upper(base_c2)
        delta0 = round_upper(
            base_c0 * radius_value
            + phi2 * radius_value**2 / (2 * omega**2)
        )
        delta1 = round_upper(
            base_c1 * radius_value
            + phi2 * radius_value**2
            / (2 * domain_length * omega**2)
        )
        delta2 = round_upper(base_c2 * radius_value)
        maximum_delta0 = max(maximum_delta0, delta0)
        maximum_delta1 = max(maximum_delta1, delta1)
        maximum_delta2 = max(maximum_delta2, delta2)
        tube_jet = SkyrmionJetBox(
            radius=cell.family_profile_jet.radius,
            profile=round_interval(
                cell.family_profile_jet.profile
                + RationalInterval(-delta0, delta0)
            ),
            derivative=round_interval(
                cell.family_profile_jet.derivative
                + RationalInterval(-delta1, delta1)
            ),
            second_derivative=round_interval(
                cell.family_profile_jet.second_derivative
                + RationalInterval(-delta2, delta2)
            ),
        )
        radius_box = tube_jet.radius
        radius_squared = radius_box.power(2)
        lapse = RationalInterval.point(1) - radius_squared.scale(
            schur_validation.curvature
        )
        lapse_derivative = radius_box.scale(
            -2 * schur_validation.curvature
        )
        sine = round_interval(sin_center_lipschitz_interval(
            tube_jet.profile,
            terms=terms,
        ))
        sine_twice = round_interval(sin_center_lipschitz_interval(
            tube_jet.profile.scale(2),
            terms=terms,
        ))
        cosine_twice = round_interval(cos_center_lipschitz_interval(
            tube_jet.profile.scale(2),
            terms=terms,
        ))
        p_f_interval = (lapse * sine_twice).scale(8)
        p_ff_interval = (lapse * cosine_twice).scale(16)
        p_fff_interval = (lapse * sine_twice).scale(-32)
        p_xf_interval = (lapse_derivative * sine_twice).scale(8)
        p_xff_interval = (lapse_derivative * cosine_twice).scale(16)
        w_fff = (
            sine_twice.scale(-4)
            + (
                sine_twice
                * (cosine_twice.scale(4) - RationalInterval.point(1))
            ).scale(8)
            / radius_squared
            - (radius_squared * sine).scale(
                schur_validation.pion_mass_squared
            )
        )
        mixed_coefficient = (
            p_ff_interval * tube_jet.derivative + p_xf_interval
        )
        zeroth_coefficient = (
            w_fff
            - p_ff_interval * tube_jet.second_derivative
            - p_xff_interval * tube_jet.derivative
            - p_fff_interval * tube_jet.derivative.power(2) / 2
        )
        direct_nonlinear_hessian = (
            _absolute_interval_upper(p_f_interval)
            * (2 * first_c0 * first_c2 + first_c1**2)
            + 2
            * _absolute_interval_upper(mixed_coefficient)
            * first_c0
            * first_c1
            + _absolute_interval_upper(zeroth_coefficient) * first_c0**2
        )
        center_jet_raw = _polynomial_subcell_jet(
            endpoint_validation.profile_cells[cell.source_cell_index],
            Fraction(0),
            Fraction(1),
        )
        center_jet = SkyrmionJetBox(
            radius=center_jet_raw.radius,
            profile=round_interval(center_jet_raw.profile),
            derivative=round_interval(center_jet_raw.derivative),
            second_derivative=round_interval(center_jet_raw.second_derivative),
        )
        center_coefficients_raw = skyrmion_jacobi_coefficient_box(
            center_jet,
            pion_mass_squared=schur_validation.pion_mass_squared,
            curvature=schur_validation.curvature,
            trigonometric_terms=terms,
        )
        center_coefficients = SkyrmionJacobiCoefficientBox(
            principal=round_interval(center_coefficients_raw.principal),
            principal_derivative=round_interval(
                center_coefficients_raw.principal_derivative
            ),
            potential=round_interval(center_coefficients_raw.potential),
        )
        if center_coefficients.principal.lower <= 0:
            raise ValueError("center Jacobi principal coefficient is not positive")
        chi_interval = (
            RationalInterval.point(domain_right) - radius_box
        ).scale(1 / domain_length)
        center_affine_jacobi = (
            center_coefficients.principal_derivative.scale(1 / domain_length)
            + center_coefficients.potential * chi_interval
        )
        first_variation_forcing = (
            Fraction(1)
            + phi2
            * radius_value
            / omega**2
            * _absolute_interval_upper(center_affine_jacobi)
        )
        p_f_over_center = p_f_interval / center_coefficients.principal
        reduced_mixed_coefficient = (
            p_f_over_center * center_coefficients.principal_derivative
            - mixed_coefficient
        )
        reduced_zeroth_coefficient = (
            zeroth_coefficient
            - (
                p_f_over_center * center_coefficients.potential
            ).scale(2)
        )
        center_equation_hessian = (
            2
            * _absolute_interval_upper(p_f_over_center)
            * first_c0
            * first_variation_forcing
            + _absolute_interval_upper(p_f_interval) * first_c1**2
            + 2
            * _absolute_interval_upper(reduced_mixed_coefficient)
            * first_c0
            * first_c1
            + _absolute_interval_upper(reduced_zeroth_coefficient)
            * first_c0**2
        )
        nonlinear_hessian = min(
            direct_nonlinear_hessian,
            center_equation_hessian,
        )
        tube_coefficients_raw = skyrmion_jacobi_coefficient_box(
            tube_jet,
            pion_mass_squared=schur_validation.pion_mass_squared,
            curvature=schur_validation.curvature,
            trigonometric_terms=terms,
        )
        tube_coefficients = SkyrmionJacobiCoefficientBox(
            principal=round_interval(tube_coefficients_raw.principal),
            principal_derivative=round_interval(
                tube_coefficients_raw.principal_derivative
            ),
            potential=round_interval(tube_coefficients_raw.potential),
        )
        chi_upper = (domain_right - radius_box.lower) / domain_length
        affine_lift_jacobi = (
            _absolute_interval_upper(tube_coefficients.principal_derivative)
            / domain_length
            + _absolute_interval_upper(tube_coefficients.potential) * chi_upper
        )
        interior_hessian = round_upper(
            nonlinear_hessian + affine_lift_jacobi * phi2 / omega**2
        )
        checked.append(
            ValidatedSkyrmionNewtonTubeCell(
                source_cell_index=cell.source_cell_index,
                radius=radius_box,
                tube_jet=tube_jet,
                local_graph_c0_upper_bound=local_graph_c0,
                local_graph_c1_upper_bound=local_graph_c1,
                local_graph_c2_upper_bound=local_graph_c2,
                local_auxiliary_c0_upper_bound=local_auxiliary_c0,
                local_auxiliary_c1_upper_bound=local_auxiliary_c1,
                local_auxiliary_c2_upper_bound=local_auxiliary_c2,
                first_variation_c0_upper_bound=first_c0,
                first_variation_c1_upper_bound=first_c1,
                first_variation_c2_upper_bound=first_c2,
                center_equation_forcing_upper_bound=(
                    first_variation_forcing
                ),
                direct_nonlinear_hessian_upper_bound=(
                    direct_nonlinear_hessian
                ),
                center_equation_hessian_upper_bound=(
                    center_equation_hessian
                ),
                nonlinear_hessian_upper_bound=nonlinear_hessian,
                affine_lift_jacobi_upper_bound=affine_lift_jacobi,
                interior_augmented_hessian_upper_bound=interior_hessian,
            )
        )
    interior_hessian = max(
        cell.interior_augmented_hessian_upper_bound for cell in checked
    )
    first_c0 = max(
        cell.first_variation_c0_upper_bound for cell in checked
    )
    first_c1 = max(
        cell.first_variation_c1_upper_bound for cell in checked
    )
    first_c2 = max(
        cell.first_variation_c2_upper_bound for cell in checked
    )
    delta0 = maximum_delta0
    delta1 = maximum_delta1
    delta2 = maximum_delta2
    interior_hessian_trace = _skyrmion_weighted_trace_upper_bound(
        schur_validation.trace_validation,
        tuple(
            (
                cell.source_cell_index,
                cell.interior_augmented_hessian_upper_bound,
            )
            for cell in checked
        ),
        inverse_c0_upper_bound=(
            schur_validation.graph_resolvent_bounds.c0_upper_bound
        ),
    )
    scalar_hessian = (gamma2 + phi2 / domain_length) / omega**2
    schur_lower = schur_validation.corrected_schur_enclosure.lower
    z2 = max(
        interior_hessian,
        omega
        / schur_lower
        * (
            scalar_hessian
            + interior_hessian_trace
        ),
    )
    radii_polynomial = (
        mismatch_validation.newton_defect_upper_bound
        + (mismatch_validation.z0_upper_bound - 1) * radius_value
        + z2 * radius_value**2 / 2
    )
    contraction = mismatch_validation.z0_upper_bound + z2 * radius_value
    self_map_verified = radii_polynomial < 0
    contraction_verified = contraction < 1
    conclusion = (
        "augmented Newton self-map and contraction verified on the declared "
        "radius; a unique nonlinear BVP solution exists in this Newton ball"
        if self_map_verified and contraction_verified
        else "exact augmented Newton-tube diagnostic only; the radii "
        "self-map and contraction inequalities do not both close"
    )
    return ValidatedSkyrmionAugmentedNewtonTubeBound(
        cells=tuple(checked),
        pion_mass_squared=schur_validation.pion_mass_squared,
        curvature=schur_validation.curvature,
        origin_cutoff=domain_left,
        wall_radius=domain_right,
        shooting_slope_interval=slope_tube,
        origin_remainder_radius=second_sensitivity.remainder_radius,
        radius=radius_value,
        omega=omega,
        profile_second_sensitivity_upper_bound=phi2,
        derivative_second_sensitivity_upper_bound=gamma2,
        first_variation_c0_upper_bound=first_c0,
        first_variation_c1_upper_bound=first_c1,
        first_variation_c2_upper_bound=first_c2,
        profile_tube_c0_radius=delta0,
        profile_tube_c1_radius=delta1,
        profile_tube_c2_radius=delta2,
        interior_hessian_upper_bound=interior_hessian,
        interior_hessian_trace_upper_bound=interior_hessian_trace,
        scalar_hessian_upper_bound=scalar_hessian,
        schur_composed_hessian_upper_bound=z2,
        newton_defect_upper_bound=mismatch_validation.newton_defect_upper_bound,
        z0_upper_bound=mismatch_validation.z0_upper_bound,
        radii_polynomial_upper_bound=radii_polynomial,
        contraction_upper_bound=contraction,
        self_map_verified=self_map_verified,
        contraction_verified=contraction_verified,
        conclusion_scope=conclusion,
    )


def validate_skyrmion_newton_physical_observables(
    newton_tube: ValidatedSkyrmionAugmentedNewtonTubeBound,
    origin_family: ValidatedSkyrmionOriginFamily,
    *,
    trigonometric_terms: int = 24,
    pi_terms: int = 64,
) -> ValidatedSkyrmionNewtonPhysicalObservables:
    """Certify profile signs and rotor inertia from a closed Newton tube.

    The origin estimate uses the same cubic weighted ball as the Newton slope
    family.  On the positive-radius mesh the already-certified tube jets give
    direct derivative signs and interval ranges for the exact inertia density.
    """
    if not isinstance(
        newton_tube,
        ValidatedSkyrmionAugmentedNewtonTubeBound,
    ):
        raise TypeError("newton_tube must be a validated augmented tube")
    if not isinstance(origin_family, ValidatedSkyrmionOriginFamily):
        raise TypeError("origin_family must be a validated origin family")
    terms = _positive_integer("trigonometric_terms", trigonometric_terms)
    pi_count = _positive_integer("pi_terms", pi_terms)
    if not (
        newton_tube.self_map_verified
        and newton_tube.contraction_verified
    ):
        raise ValueError("physical observables require a closed Newton tube")
    if origin_family.shooting_slopes != newton_tube.shooting_slope_interval:
        raise ValueError("origin family does not match the Newton slope tube")
    if origin_family.cutoff != newton_tube.origin_cutoff:
        raise ValueError("origin family cutoff does not match the Newton tube")
    if (
        origin_family.pion_mass_squared != newton_tube.pion_mass_squared
        or origin_family.curvature != newton_tube.curvature
    ):
        raise ValueError("origin and Newton operator parameters differ")
    if (
        origin_family.remainder_radius
        != newton_tube.origin_remainder_radius
    ):
        raise ValueError("origin remainder ball does not match the Newton tube")
    if not newton_tube.cells:
        raise ValueError("Newton tube must contain positive-radius cells")
    if newton_tube.cells[0].radius.lower != newton_tube.origin_cutoff:
        raise ValueError("Newton tube does not begin at the origin cutoff")
    if newton_tube.cells[-1].radius.upper != newton_tube.wall_radius:
        raise ValueError("Newton tube does not reach the wall")
    for left, right in zip(newton_tube.cells, newton_tube.cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("Newton tube cells must form a contiguous cover")

    cutoff = origin_family.cutoff
    t_box = RationalInterval(Fraction(0), cutoff**2)
    origin_center = origin_family.shooting_slopes - (
        origin_family.cubic_coefficient * t_box
    ).scale(3)
    origin_remainder = origin_family.remainder_radius * cutoff**4
    origin_momentum = origin_center + RationalInterval(
        -origin_remainder,
        origin_remainder,
    )
    if origin_momentum.lower <= 0:
        raise ValueError("origin momentum does not prove a negative derivative")

    derivative_upper = max(
        cell.tube_jet.derivative.upper for cell in newton_tube.cells
    )
    if derivative_upper >= 0:
        raise ValueError("positive-radius tube does not prove monotonicity")
    wall_slope = newton_tube.cells[-1].tube_jet.derivative
    if wall_slope.upper >= 0:
        raise ValueError("wall-slope enclosure is not strictly negative")

    pi_interval = pi_machin_interval(terms=pi_count)
    inertia_factor = pi_interval.scale(Fraction(2, 3))
    checked_cells: list[ValidatedSkyrmionInertiaCell] = []
    positive_radius_inertia = RationalInterval.point(0)
    for cell in newton_tube.cells:
        radius_squared = cell.radius.power(2)
        lapse = RationalInterval.point(1) - radius_squared.scale(
            newton_tube.curvature
        )
        if lapse.lower <= 0:
            raise ValueError("inertia cell reaches or crosses the horizon")
        sine_squared = sin_center_lipschitz_interval(
            cell.tube_jet.profile,
            terms=terms,
        ).power(2)
        derivative_squared = cell.tube_jet.derivative.power(2)
        density = inertia_factor * (
            radius_squared * sine_squared / lapse
            + (radius_squared * sine_squared * derivative_squared).scale(4)
            + sine_squared.power(2).scale(4) / lapse
        )
        integral = density.scale(cell.radius.width)
        checked_cells.append(
            ValidatedSkyrmionInertiaCell(
                source_cell_index=cell.source_cell_index,
                radius=cell.radius,
                sine_squared=sine_squared,
                density_enclosure=density,
                integral_enclosure=integral,
            )
        )
        positive_radius_inertia += integral

    origin_lapse_lower = 1 - newton_tube.curvature * cutoff**2
    if origin_lapse_lower <= 0:
        raise ValueError("origin patch reaches or crosses the horizon")
    origin_momentum_abs = _absolute_interval_upper(origin_momentum)
    origin_density_upper = inertia_factor.upper * (
        cutoff**2 / origin_lapse_lower
        + 4 * cutoff**2 * origin_momentum_abs**2
        + 4 / origin_lapse_lower
    )
    origin_inertia_upper = cutoff * origin_density_upper
    inertia = RationalInterval(
        positive_radius_inertia.lower,
        positive_radius_inertia.upper + origin_inertia_upper,
    )
    if inertia.lower <= 0:
        raise ValueError("inertia quadrature does not prove strict positivity")

    return ValidatedSkyrmionNewtonPhysicalObservables(
        origin_family=origin_family,
        newton_tube=newton_tube,
        origin_momentum_enclosure=origin_momentum,
        positive_radius_derivative_upper_bound=derivative_upper,
        wall_slope_enclosure=wall_slope,
        inertia_cells=tuple(checked_cells),
        origin_inertia_upper_bound=origin_inertia_upper,
        inertia_enclosure=inertia,
        strict_monotonicity_verified=True,
        negative_wall_slope_verified=True,
        positive_finite_inertia_verified=True,
        conclusion_scope=(
            "the unique nonlinear hard-wall solution in the Newton ball is "
            "strictly decreasing, has strictly negative wall slope, and has "
            "finite strictly positive dimensionless rotor inertia"
        ),
    )


def conditional_skyrmion_barta_foundation_certificate() -> dict[str, object]:
    """Audit the packaged conditional Barta cells with exact arithmetic."""
    validation = validate_skyrmion_barta_cells(
        _default_conditional_barta_cells(),
        Fraction(1),
    )
    principal_lower_bound = min(
        cell.coefficients.principal.lower for cell in validation.cells
    )
    checks = {
        "all_independent_jet_boxes_recomputed": len(validation.cells) == 5,
        "principal_coefficient_is_positive_on_each_box": (
            principal_lower_bound > 0
        ),
        "fixed_witness_barta_quotient_is_at_least_one_on_each_box": (
            validation.recomputed_lower_bound >= 1
        ),
    }
    return {
        "goal": "Conditional Skyrmion Jacobi Barta Foundation",
        "status": "pass" if all(checks.values()) else "fail",
        "result_type": "conditional_exact_rational_barta_jet_box_audit",
        "central_result": (
            "For each of five supplied independent exact-rational profile-jet "
            "boxes, the checker recomputes P, P', Q and verifies P>0 and "
            "(L v)/v>=1 for v=8/((x-33/16)^2+4)."
        ),
        "executable_checks": checks,
        "cell_count": len(validation.cells),
        "declared_barta_lower_bound": str(validation.declared_lower_bound),
        "recomputed_barta_lower_bound": _downward_decimal(
            validation.recomputed_lower_bound
        ),
        "recomputed_principal_lower_bound": _downward_decimal(
            principal_lower_bound
        ),
        "numeric_representation": (
            "The two recomputed lower bounds are certified downward-rounded "
            "decimal rationals with 18 places; all checker arithmetic is exact."
        ),
        "claim_limit": (
            "The supplied boxes are independent conditional inputs. This "
            "certificate proves neither that they cover a full interval nor "
            "that one common Skyrmion profile satisfies them, and it does not "
            "establish origin matching, a wall condition, or a Newton radius."
        ),
    }
