"""Centered signed outer estimator for the centrifugal master response.

The corrected estimator is

``J_rigid + B(y_h) + R_y(z_h)``,

where ``R_y(z_h)=ell(z_h)-q(y_h,z_h)``.  This module carries the common
normalized cell coordinate through the authenticated profile tube, Green
weight, exact rational primal and adjoint trials, conormal form coefficients,
and both weak loads.  The three signed densities are added before integration,
so deterministic radial cancellation is retained.

Only the authenticated positive-radius bulk is included.  Regular-origin and
wall terms are deliberately absent, and no zero-exclusion claim is made.
Because the bulk residual retains its weak derivative term, its compatible
wall completion is ``y_f(a) * (gamma_B - k * z_f(a))``.  The alternative
``-eta_y * z_f(a)`` belongs to the all-strong representation and must not be
combined with this estimator.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
    regular_rotational_source_from_kernels,
)
from .centrifugal_skyrmion_rational_response_trials import RationalResponseTrial
from .validated_centrifugal_adjoint_bulk_load import (
    centrifugal_weak_master_load_affine_kernel,
)
from .validated_centrifugal_correlated_adjoint import _green_models, _trial_models
from .validated_centrifugal_correlated_residual import (
    _corrected_profile_polynomials,
)
from .validated_centrifugal_liouville_taylor import _CenteredTaylorModel
from .validated_interval import RationalInterval, RationalPolynomial
from .validated_skyrmion_sharp_profile import ValidatedSkyrmionSharpProfileTube


def _transpose(matrix):
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _matrix_vector(matrix, vector):
    return tuple(row[0] * vector[0] + row[1] * vector[1] for row in matrix)


def _dot(left, right):
    return left[0] * right[0] + left[1] * right[1]


def _sum_intervals(values) -> RationalInterval:
    total = RationalInterval.point(0)
    for value in values:
        total += value
    return total


@dataclass(frozen=True)
class _CenteredDensityIntegral:
    integral: RationalInterval
    naive_range_times_width: RationalInterval
    center_density: RationalInterval


def _integrate_centered_density(
    density: _CenteredTaylorModel,
    *,
    physical_half_width: Fraction,
) -> _CenteredDensityIntegral:
    """Integrate one density over its physical cell.

    The Taylor coordinate lies in ``[-1,1]``, so ``dx`` is the physical
    half-width times the normalized differential.  The center enclosure is
    returned as a point-evaluation diagnostic; it is not used as quadrature.
    """
    if physical_half_width <= 0:
        raise ValueError("physical_half_width must be positive")
    return _CenteredDensityIntegral(
        integral=density.symmetric_integral().scale(physical_half_width),
        naive_range_times_width=density.range().scale(2 * physical_half_width),
        center_density=density.coefficients[0] + density.remainder,
    )


@dataclass(frozen=True)
class CorrelatedEstimatorCell:
    radius: RationalInterval
    parent_cell_index: int
    parent_subdivision_index: int
    physical_half_width: Fraction
    rigid_integral: RationalInterval
    deformation_integral: RationalInterval
    primal_residual_correction_integral: RationalInterval
    correlated_total_integral: RationalInterval
    naive_total_integral: RationalInterval
    center_total_density: RationalInterval
    total_taylor_degree: int
    shared_centered_coordinate: bool


@dataclass(frozen=True)
class CorrelatedPositiveRadiusEstimator:
    cells: tuple[CorrelatedEstimatorCell, ...]
    positive_radius_domain: RationalInterval
    radius_partition: tuple[RationalInterval, ...]
    rigid_total: RationalInterval
    deformation_total: RationalInterval
    primal_residual_correction_total: RationalInterval
    component_sum_total: RationalInterval
    correlated_estimator_total: RationalInterval
    naive_estimator_total: RationalInterval
    profile_subdivisions_per_parent: int
    authenticated_positive_radius_cell_count: int
    profile_primal_adjoint_partitions_match: bool
    profile_green_trials_form_and_loads_share_coordinate: bool
    centered_symmetric_integration_used: bool
    origin_included: bool
    wall_included: bool
    zero_exclusion_claimed: bool
    conclusion_scope: str


def correlated_positive_radius_corrected_estimator(
    profile: ValidatedSkyrmionSharpProfileTube,
    primal_trial: RationalResponseTrial,
    adjoint_trial: RationalResponseTrial,
    *,
    patch_radius: Fraction = Fraction(20),
    gravitational_coupling: Fraction = Fraction(1),
    degree_limit: int = 8,
    rounding_denominator: int = 10**16,
    trigonometric_terms: int = 6,
    green_terms: int = 8,
) -> CorrelatedPositiveRadiusEstimator:
    """Enclose the signed corrected estimator on ``[x0,a]`` only."""
    if patch_radius * patch_radius * profile.curvature != 1:
        raise ValueError("patch radius and profile curvature are inconsistent")
    if not isinstance(gravitational_coupling, Fraction):
        raise TypeError("gravitational_coupling must be an exact Fraction")
    primal_trial.validate()
    adjoint_trial.validate()
    partition = tuple(cell.radius for cell in profile.cells)
    if partition != tuple(cell.radius for cell in primal_trial.positive_radius_cells):
        raise ValueError("profile and primal trial partitions differ")
    if partition != tuple(cell.radius for cell in adjoint_trial.positive_radius_cells):
        raise ValueError("profile and adjoint trial partitions differ")
    options = {
        "degree_limit": degree_limit,
        "rounding_denominator": rounding_denominator,
    }
    cells: list[CorrelatedEstimatorCell] = []
    counters: dict[int, int] = {}

    for profile_cell, primal_cell, adjoint_cell in zip(
        profile.cells,
        primal_trial.positive_radius_cells,
        adjoint_trial.positive_radius_cells,
        strict=True,
    ):
        parent_index = profile_cell.parent_cell_index
        subdivision = counters.get(parent_index, 0)
        counters[parent_index] = subdivision + 1
        if subdivision >= profile.subdivisions_per_parent:
            raise ValueError("profile subdivision ordering is inconsistent")
        field_poly, derivative_poly, _, error0, error1, _ = (
            _corrected_profile_polynomials(
                profile,
                parent_index=parent_index,
                subdivision=subdivision,
            )
        )
        radius_center = profile_cell.radius.midpoint
        radius_half_width = profile_cell.radius.width / 2
        x = _CenteredTaylorModel.from_polynomial(
            RationalPolynomial((radius_center, radius_half_width)), **options
        )
        field = _CenteredTaylorModel.from_polynomial(
            field_poly, error_radius=error0, **options
        )
        field_derivative = _CenteredTaylorModel.from_polynomial(
            derivative_poly, error_radius=error1, **options
        )
        pion_mass_squared = x._coerce(profile.pion_mass_squared)
        sine, cosine = field.sin_cos(terms=trigonometric_terms)
        time = x * x
        metric = 1 - time * profile.curvature
        rho = -field_derivative
        sine_over_radius = sine / x
        cosine_deficit = -cosine
        blocks = regular_conormal_blocks_from_kernels(
            t=time,
            metric_factor=metric,
            profile_deficit_radial_derivative=rho,
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_deficit,
            pion_mass_squared=pion_mass_squared,
        )
        source = regular_rotational_source_from_kernels(
            t=time,
            metric_factor=metric,
            profile_deficit_radial_derivative=rho,
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_deficit,
        )
        coordinate = blocks["coordinate"]
        mixed = tuple(
            tuple(x * entry for entry in row) for row in blocks["mixed"]
        )
        principal = tuple(
            tuple(time * entry for entry in row) for row in blocks["principal"]
        )
        rotational_value_load = tuple(
            x * entry for entry in source["coordinate_source"]
        )
        rotational_derivative_load = tuple(
            time * entry for entry in source["derivative_source"]
        )

        green, green_derivative = _green_models(
            x, patch_radius=patch_radius, terms=green_terms
        )
        master_load = centrifugal_weak_master_load_affine_kernel(
            radius=x,
            metric_factor=metric,
            metric_factor_derivative=-2 * profile.curvature * x,
            inverse_patch_radius_squared=x._coerce(profile.curvature),
            sine_profile=sine,
            cosine_profile=cosine,
            profile_derivative=field_derivative,
            pion_mass_squared=pion_mass_squared,
            green_weight=green,
            green_weight_derivative=green_derivative,
            gravitational_coupling=x._coerce(gravitational_coupling),
        )

        primal_radial = _trial_models(
            primal_cell.radial_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        primal_tangential = _trial_models(
            primal_cell.tangential_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        adjoint_radial = _trial_models(
            adjoint_cell.radial_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        adjoint_tangential = _trial_models(
            adjoint_cell.tangential_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        primal_value = (primal_radial[0], primal_tangential[0])
        primal_derivative = (primal_radial[1], primal_tangential[1])
        adjoint_value = (adjoint_radial[0], adjoint_tangential[0])
        adjoint_derivative = (adjoint_radial[1], adjoint_tangential[1])

        weak_value_residual = tuple(
            load - coordinate_action - mixed_action
            for load, coordinate_action, mixed_action in zip(
                rotational_value_load,
                _matrix_vector(coordinate, primal_value),
                _matrix_vector(mixed, primal_derivative),
                strict=True,
            )
        )
        weak_derivative_residual = tuple(
            load - mixed_action - principal_action
            for load, mixed_action, principal_action in zip(
                rotational_derivative_load,
                _matrix_vector(_transpose(mixed), primal_value),
                _matrix_vector(principal, primal_derivative),
                strict=True,
            )
        )
        rigid_density = master_load.rigid
        deformation_density = _dot(master_load.b0, primal_value) + _dot(
            master_load.b1, primal_derivative
        )
        correction_density = _dot(weak_value_residual, adjoint_value) + _dot(
            weak_derivative_residual, adjoint_derivative
        )
        total_density = rigid_density + deformation_density + correction_density

        rigid_integral = _integrate_centered_density(
            rigid_density, physical_half_width=radius_half_width
        )
        deformation_integral = _integrate_centered_density(
            deformation_density, physical_half_width=radius_half_width
        )
        correction_integral = _integrate_centered_density(
            correction_density, physical_half_width=radius_half_width
        )
        total_integral = _integrate_centered_density(
            total_density, physical_half_width=radius_half_width
        )
        cells.append(
            CorrelatedEstimatorCell(
                radius=profile_cell.radius,
                parent_cell_index=parent_index,
                parent_subdivision_index=subdivision,
                physical_half_width=radius_half_width,
                rigid_integral=rigid_integral.integral,
                deformation_integral=deformation_integral.integral,
                primal_residual_correction_integral=correction_integral.integral,
                correlated_total_integral=total_integral.integral,
                naive_total_integral=total_integral.naive_range_times_width,
                center_total_density=total_integral.center_density,
                total_taylor_degree=len(total_density.coefficients) - 1,
                shared_centered_coordinate=True,
            )
        )

    rigid_total = _sum_intervals(cell.rigid_integral for cell in cells)
    deformation_total = _sum_intervals(
        cell.deformation_integral for cell in cells
    )
    correction_total = _sum_intervals(
        cell.primal_residual_correction_integral for cell in cells
    )
    component_sum = rigid_total + deformation_total + correction_total
    correlated_total = _sum_intervals(
        cell.correlated_total_integral for cell in cells
    )
    naive_total = _sum_intervals(cell.naive_total_integral for cell in cells)
    return CorrelatedPositiveRadiusEstimator(
        cells=tuple(cells),
        positive_radius_domain=RationalInterval(
            partition[0].lower, partition[-1].upper
        ),
        radius_partition=partition,
        rigid_total=rigid_total,
        deformation_total=deformation_total,
        primal_residual_correction_total=correction_total,
        component_sum_total=component_sum,
        correlated_estimator_total=correlated_total,
        naive_estimator_total=naive_total,
        profile_subdivisions_per_parent=profile.subdivisions_per_parent,
        authenticated_positive_radius_cell_count=len(cells),
        profile_primal_adjoint_partitions_match=True,
        profile_green_trials_form_and_loads_share_coordinate=True,
        centered_symmetric_integration_used=True,
        origin_included=False,
        wall_included=False,
        zero_exclusion_claimed=False,
        conclusion_scope=(
            "Exact-rational centered enclosure of the signed corrected "
            "positive-radius bulk estimator only; regular-origin and wall "
            "terms are absent. A global weak-form composer must add "
            "y_f(a)*(gamma_B-k*z_f(a)), not the all-strong -eta_y*z_f(a); "
            "no exterior-response zero exclusion is claimed."
        ),
    )
