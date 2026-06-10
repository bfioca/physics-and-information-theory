"""Centered form-dual enclosure for the outer centrifugal adjoint residual.

The box form-dual certificate constructs the weak residual and the Liouville
multiplier from independently ranged coefficient boxes.  That loses the
shared dependence of the profile, exact rational adjoint trial, Green weight,
and form coefficients on one radial coordinate.  This module carries those
quantities through one centered Taylor algebra and ranges only the two final
completed-square coefficients

``r1/x`` and ``r0 - T^T(r1/x)``.

Authenticated Newton-tube errors remain interval remainders.  The resulting
bound is rigorous for the positive-radius bulk; the wall and regular-origin
loads are deliberately composed elsewhere.
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
from .validated_centrifugal_correlated_residual import (
    _ModelRadialJet,
    _corrected_profile_polynomials,
    _model_matrix_derivative,
    _model_matrix_value,
)
from .validated_centrifugal_liouville_taylor import _CenteredTaylorModel
from .validated_centrifugal_response_residual import (
    RationalC1TrialCell,
    ValidatedWallConormalCoefficients,
)
from .validated_centrifugal_wall_master_load import ValidatedWallMasterLoad
from .validated_interval import RationalInterval, RationalPolynomial
from .validated_interval import sqrt_fraction_interval
from .validated_skyrmion_bvp import (
    _affine_restrict_polynomial,
    _rational_polynomial_scale,
)
from .validated_skyrmion_sharp_profile import ValidatedSkyrmionSharpProfileTube


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _constant_radial_jet(
    template: _CenteredTaylorModel, value: Fraction
) -> _ModelRadialJet:
    """Lift a physical parameter without silently resetting it to one."""
    return _ModelRadialJet(template._coerce(value), template._coerce(0))


def _transpose(matrix):
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _matrix_vector(matrix, vector):
    return tuple(row[0] * vector[0] + row[1] * vector[1] for row in matrix)


def _matrix_subtract(left, right):
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(2))
        for row in range(2)
    )


def _matrix_add(left, right):
    return tuple(
        tuple(left[row][column] + right[row][column] for column in range(2))
        for row in range(2)
    )


def _matrix_scale(matrix, scalar):
    return tuple(tuple(entry * scalar for entry in row) for row in matrix)


def _matrix_multiply(left, right):
    return tuple(
        tuple(
            left[row][0] * right[0][column]
            + left[row][1] * right[1][column]
            for column in range(2)
        )
        for row in range(2)
    )


def _symmetric_part(matrix):
    return _matrix_scale(_matrix_add(matrix, _transpose(matrix)), Fraction(1, 2))


def _model_quadratic_form(vector, matrix):
    product = _matrix_vector(matrix, vector)
    return vector[0] * product[0] + vector[1] * product[1]


def _matrix_inverse(matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant.range().contains_zero():
        raise ValueError("centered principal determinant contains zero")
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def _green_models(
    radius: _CenteredTaylorModel,
    *,
    patch_radius: Fraction,
    terms: int,
) -> tuple[_CenteredTaylorModel, _CenteredTaylorModel]:
    """Enclose the center-regular Green weight and physical derivative."""
    if isinstance(terms, bool) or not isinstance(terms, int) or terms < 1:
        raise ValueError("green terms must be a positive integer")
    ratio = radius / patch_radius
    ratio_range = ratio.range()
    if ratio_range.lower < 0 or ratio_range.upper > Fraction(1, 5):
        raise ValueError("green series requires 0 <= radius/patch_radius <= 1/5")
    value = radius._coerce(0)
    derivative = radius._coerce(0)
    coefficient = Fraction(1)
    power = 3
    for _ in range(terms):
        value = value + ratio.power(power) * coefficient
        derivative = derivative + ratio.power(power - 1) * (coefficient * power)
        coefficient *= Fraction(power * (power + 1), (power + 4) * (power - 1))
        power += 2
    next_value = coefficient * ratio_range.upper**power
    next_derivative = coefficient * power * ratio_range.upper ** (power - 1)
    value_tail = next_value / (1 - Fraction(1, 25))
    derivative_tail = next_derivative / (1 - Fraction(2, 25))
    value = _CenteredTaylorModel(
        value.coefficients,
        value.remainder + RationalInterval(0, value_tail),
        value.degree_limit,
        value.rounding_denominator,
    )
    derivative = _CenteredTaylorModel(
        derivative.coefficients,
        derivative.remainder + RationalInterval(0, derivative_tail),
        derivative.degree_limit,
        derivative.rounding_denominator,
    )
    return value * (2 * patch_radius / 15), derivative * Fraction(2, 15)


def _trial_models(
    polynomial: RationalPolynomial,
    *,
    radius_half_width: Fraction,
    options: dict[str, int],
) -> tuple[_CenteredTaylorModel, _CenteredTaylorModel, _CenteredTaylorModel]:
    centered = _affine_restrict_polynomial(
        polynomial, Fraction(1, 2), Fraction(1, 2)
    )
    value = _CenteredTaylorModel.from_polynomial(centered, **options)
    derivative = _CenteredTaylorModel.from_polynomial(
        _rational_polynomial_scale(centered.derivative(), 1 / radius_half_width),
        **options,
    )
    second = _CenteredTaylorModel.from_polynomial(
        _rational_polynomial_scale(
            centered.derivative().derivative(), 1 / radius_half_width**2
        ),
        **options,
    )
    return value, derivative, second


@dataclass(frozen=True)
class CorrelatedAdjointEnergyDualCell:
    """One centered positive-radius completed-square residual enclosure."""

    radius: RationalInterval
    weak_value_coefficient: tuple[RationalInterval, RationalInterval]
    weak_derivative_coefficient: tuple[RationalInterval, RationalInterval]
    completed_derivative_coefficient: tuple[RationalInterval, RationalInterval]
    completed_value_coefficient: tuple[RationalInterval, RationalInterval]
    principal_first_minor_lower: Fraction
    principal_determinant_lower: Fraction
    completed_potential_first_minor_lower: Fraction
    completed_potential_determinant_lower: Fraction
    completed_potential_matrix_inverse_used: bool
    derivative_squared_dual_upper: Fraction
    value_squared_dual_upper: Fraction
    squared_dual_upper: Fraction
    matrix_weighted_derivative_squared_dual_upper: Fraction
    matrix_weighted_value_squared_dual_upper: Fraction
    matrix_weighted_squared_dual_upper: Fraction


@dataclass(frozen=True)
class CorrelatedPositiveRadiusWallAdjointDualBound:
    """Hybrid local-matrix/scalar-floor adjoint bound outside the origin."""

    cells: tuple[CorrelatedAdjointEnergyDualCell, ...]
    positive_radius_domain: RationalInterval
    scalar_floor_bulk_squared_upper: Fraction
    matrix_weighted_bulk_squared_upper: Fraction
    wall_squared_upper: Fraction
    matrix_weighted_partial_squared_upper: Fraction
    matrix_weighted_partial_energy_dual_upper: Fraction
    local_potential_inverse_cell_count: int
    scalar_potential_fallback_cell_count: int
    dominant_cell_index: int
    dominant_cell_radius: RationalInterval
    regular_origin_master_load_included: bool
    full_loaded_adjoint_residual_certified: bool


def compose_correlated_positive_radius_wall_adjoint_bound(
    cells: tuple[CorrelatedAdjointEnergyDualCell, ...],
    *,
    wall_residual: RationalInterval,
    wall_trace_margin_lower_bound: Fraction,
    sqrt_bisection_steps: int = 160,
) -> CorrelatedPositiveRadiusWallAdjointDualBound:
    """Add the exact wall trace to the centered positive-radius bulk bound."""
    if not cells:
        raise ValueError("at least one positive-radius residual cell is required")
    if wall_trace_margin_lower_bound <= 0:
        raise ValueError("wall trace margin lower bound must be positive")
    for left, right in zip(cells, cells[1:]):
        if left.radius.upper != right.radius.lower:
            raise ValueError("positive-radius residual cells are not contiguous")
    scalar_bulk = sum(
        (cell.squared_dual_upper for cell in cells), start=Fraction(0)
    )
    matrix_bulk = sum(
        (cell.matrix_weighted_squared_dual_upper for cell in cells),
        start=Fraction(0),
    )
    wall = _absolute_upper(wall_residual) ** 2 / wall_trace_margin_lower_bound
    squared = matrix_bulk + wall
    local_count = sum(
        cell.completed_potential_matrix_inverse_used for cell in cells
    )
    dominant = max(
        range(len(cells)),
        key=lambda index: cells[index].matrix_weighted_squared_dual_upper,
    )
    return CorrelatedPositiveRadiusWallAdjointDualBound(
        cells=cells,
        positive_radius_domain=RationalInterval(
            cells[0].radius.lower, cells[-1].radius.upper
        ),
        scalar_floor_bulk_squared_upper=scalar_bulk,
        matrix_weighted_bulk_squared_upper=matrix_bulk,
        wall_squared_upper=wall,
        matrix_weighted_partial_squared_upper=squared,
        matrix_weighted_partial_energy_dual_upper=sqrt_fraction_interval(
            squared, bisection_steps=sqrt_bisection_steps
        ).upper,
        local_potential_inverse_cell_count=local_count,
        scalar_potential_fallback_cell_count=len(cells) - local_count,
        dominant_cell_index=dominant,
        dominant_cell_radius=cells[dominant].radius,
        regular_origin_master_load_included=False,
        full_loaded_adjoint_residual_certified=False,
    )


def weak_adjoint_wall_residual(
    *,
    trial: RationalC1TrialCell,
    coefficients: ValidatedWallConormalCoefficients,
    master_load: ValidatedWallMasterLoad,
) -> RationalInterval:
    """Return the wall coefficient in the weak adjoint residual.

    The outer bulk residual is kept in weak form, so the trial conormal is
    already part of the bulk form ``q(v,z_h)`` and must not be inserted again.
    Only ``gamma_B v_f(a)-k z_f(a)v_f(a)`` remains at the wall.
    """
    if coefficients.wall_radius != trial.radius.upper:
        raise ValueError("adjoint trial does not terminate at the certified wall")
    value, _ = trial.endpoint_jet(right=True)
    return master_load.gamma_b - coefficients.wall_form_coefficient.scale(value[0])


def correlated_adjoint_energy_dual_cells(
    profile: ValidatedSkyrmionSharpProfileTube,
    trial: RationalResponseTrial,
    *,
    principal_lower_bound: Fraction,
    completed_potential_lower_bound: Fraction,
    patch_radius: Fraction = Fraction(20),
    gravitational_coupling: Fraction = Fraction(1),
    degree_limit: int = 8,
    rounding_denominator: int = 10**16,
    trigonometric_terms: int = 6,
    green_terms: int = 8,
) -> tuple[CorrelatedAdjointEnergyDualCell, ...]:
    """Enclose the outer adjoint residual with shared radial correlation."""
    if principal_lower_bound <= 0 or completed_potential_lower_bound <= 0:
        raise ValueError("completed-square lower bounds must be positive")
    if patch_radius * patch_radius * profile.curvature != 1:
        raise ValueError("patch radius and profile curvature are inconsistent")
    trial.validate()
    if tuple(cell.radius for cell in profile.cells) != tuple(
        cell.radius for cell in trial.positive_radius_cells
    ):
        raise ValueError("profile and trial partitions differ")
    options = {
        "degree_limit": degree_limit,
        "rounding_denominator": rounding_denominator,
    }
    output = []
    counters: dict[int, int] = {}
    for profile_cell, trial_cell in zip(
        profile.cells, trial.positive_radius_cells, strict=True
    ):
        parent_index = profile_cell.parent_cell_index
        subdivision = counters.get(parent_index, 0)
        counters[parent_index] = subdivision + 1
        if subdivision >= profile.subdivisions_per_parent:
            raise ValueError("profile subdivision ordering is inconsistent")
        field_poly, derivative_poly, second_poly, error0, error1, error2 = (
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
        one = x._coerce(1)
        field = _CenteredTaylorModel.from_polynomial(
            field_poly, error_radius=error0, **options
        )
        field_derivative = _CenteredTaylorModel.from_polynomial(
            derivative_poly, error_radius=error1, **options
        )
        field_second = _CenteredTaylorModel.from_polynomial(
            second_poly, error_radius=error2, **options
        )
        sine, cosine = field.sin_cos(terms=trigonometric_terms)
        x_jet = _ModelRadialJet(x, one)
        time = x_jet * x_jet
        metric_jet = 1 - time * profile.curvature
        rho = _ModelRadialJet(-field_derivative, -field_second)
        sine_over_radius = _ModelRadialJet(
            sine / x,
            (cosine * field_derivative * x - sine) / x.power(2),
        )
        cosine_deficit = _ModelRadialJet(-cosine, sine * field_derivative)
        blocks = regular_conormal_blocks_from_kernels(
            t=time,
            metric_factor=metric_jet,
            profile_deficit_radial_derivative=rho,
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_deficit,
            pion_mass_squared=_constant_radial_jet(
                x, profile.pion_mass_squared
            ),
        )
        coordinate = _model_matrix_value(blocks["coordinate"])
        regular_mixed = _model_matrix_value(blocks["mixed"])
        regular_mixed_derivative = tuple(
            tuple(entry.derivative for entry in row) for row in blocks["mixed"]
        )
        regular_principal = _symmetric_part(
            _model_matrix_value(blocks["principal"])
        )
        regular_principal_derivative = _symmetric_part(
            tuple(
                tuple(entry.derivative for entry in row)
                for row in blocks["principal"]
            )
        )
        mixed = _model_matrix_value(
            tuple(tuple(x_jet * entry for entry in row) for row in blocks["mixed"])
        )
        principal = _model_matrix_value(
            tuple(tuple(time * entry for entry in row) for row in blocks["principal"])
        )

        green, green_derivative = _green_models(
            x, patch_radius=patch_radius, terms=green_terms
        )
        metric = metric_jet.value
        load = centrifugal_weak_master_load_affine_kernel(
            radius=x,
            metric_factor=metric,
            metric_factor_derivative=-2 * profile.curvature * x,
            inverse_patch_radius_squared=x._coerce(profile.curvature),
            sine_profile=sine,
            cosine_profile=cosine,
            profile_derivative=field_derivative,
            pion_mass_squared=x._coerce(profile.pion_mass_squared),
            green_weight=green,
            green_weight_derivative=green_derivative,
            gravitational_coupling=x._coerce(gravitational_coupling),
        )
        radial = _trial_models(
            trial_cell.radial_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        tangential = _trial_models(
            trial_cell.tangential_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        value = (radial[0], tangential[0])
        derivative = (radial[1], tangential[1])
        weak_value = tuple(
            load_value - coordinate_value - mixed_value
            for load_value, coordinate_value, mixed_value in zip(
                load.b0,
                _matrix_vector(coordinate, value),
                _matrix_vector(mixed, derivative),
                strict=True,
            )
        )
        weak_derivative = tuple(
            load_value - mixed_value - principal_value
            for load_value, mixed_value, principal_value in zip(
                load.b1,
                _matrix_vector(_transpose(mixed), value),
                _matrix_vector(principal, derivative),
                strict=True,
            )
        )

        antisymmetric_mixed = _matrix_scale(
            _matrix_subtract(mixed, _transpose(mixed)), Fraction(1, 2)
        )
        identity_half = (
            (x._coerce(Fraction(1, 2)), x._coerce(0)),
            (x._coerce(0), x._coerce(Fraction(1, 2))),
        )
        multiplier = _matrix_subtract(
            identity_half,
            _matrix_scale(
                _matrix_multiply(_matrix_inverse(principal), antisymmetric_mixed),
                x,
            ),
        )
        completed_derivative = tuple(entry / x for entry in weak_derivative)
        completed_value = tuple(
            left - right
            for left, right in zip(
                weak_value,
                _matrix_vector(_transpose(multiplier), completed_derivative),
                strict=True,
            )
        )
        symmetric_regular_mixed = _symmetric_part(regular_mixed)
        antisymmetric_regular_mixed = _matrix_scale(
            _matrix_subtract(regular_mixed, _transpose(regular_mixed)),
            Fraction(1, 2),
        )
        # The completed potential in the logarithmic Liouville square is
        # W=C-sym(Mbar)+Pbar/4-x sym(Mbar)_x+(x/2)Pbar_x
        #   +Abar Pbar^-1 Abar.
        completed_potential = _symmetric_part(
            _matrix_add(
                _matrix_add(
                    _matrix_subtract(
                        _matrix_add(
                            _matrix_subtract(coordinate, symmetric_regular_mixed),
                            _matrix_scale(regular_principal, Fraction(1, 4)),
                        ),
                        _matrix_scale(
                            _symmetric_part(regular_mixed_derivative), x
                        ),
                    ),
                    _matrix_scale(regular_principal_derivative, x * Fraction(1, 2)),
                ),
                _matrix_multiply(
                    _matrix_multiply(
                        antisymmetric_regular_mixed,
                        _matrix_inverse(regular_principal),
                    ),
                    antisymmetric_regular_mixed,
                ),
            )
        )
        principal_determinant = (
            regular_principal[0][0] * regular_principal[1][1]
            - regular_principal[0][1] * regular_principal[1][0]
        )
        potential_determinant = (
            completed_potential[0][0] * completed_potential[1][1]
            - completed_potential[0][1] * completed_potential[1][0]
        )
        principal_first_lower = regular_principal[0][0].range().lower
        principal_determinant_lower = principal_determinant.range().lower
        potential_first_lower = completed_potential[0][0].range().lower
        potential_determinant_lower = potential_determinant.range().lower
        if principal_first_lower <= 0 or principal_determinant_lower <= 0:
            raise ValueError(
                "centered principal matrix is not certified positive on "
                f"{profile_cell.radius}: first={principal_first_lower}, "
                f"determinant={principal_determinant_lower}"
            )
        derivative_density = _model_quadratic_form(
            completed_derivative, _matrix_inverse(regular_principal)
        )
        weak_value_range = tuple(entry.range() for entry in weak_value)
        weak_derivative_range = tuple(entry.range() for entry in weak_derivative)
        derivative_range = tuple(entry.range() for entry in completed_derivative)
        value_range = tuple(entry.range() for entry in completed_value)
        width = profile_cell.radius.width
        derivative_squared = width * sum(
            _absolute_upper(entry) ** 2 for entry in derivative_range
        ) / principal_lower_bound
        value_squared = width * sum(
            _absolute_upper(entry) ** 2 for entry in value_range
        ) / completed_potential_lower_bound
        matrix_derivative_squared = (
            radius_half_width * derivative_density.symmetric_integral().upper
        )
        potential_inverse_used = (
            potential_first_lower > 0 and potential_determinant_lower > 0
        )
        matrix_value_squared = (
            radius_half_width
            * _model_quadratic_form(
                completed_value, _matrix_inverse(completed_potential)
            ).symmetric_integral().upper
            if potential_inverse_used
            else value_squared
        )
        if matrix_derivative_squared < 0 or matrix_value_squared < 0:
            raise ValueError("matrix-weighted dual density has negative upper bound")
        output.append(
            CorrelatedAdjointEnergyDualCell(
                radius=profile_cell.radius,
                weak_value_coefficient=weak_value_range,  # type: ignore[arg-type]
                weak_derivative_coefficient=weak_derivative_range,  # type: ignore[arg-type]
                completed_derivative_coefficient=derivative_range,  # type: ignore[arg-type]
                completed_value_coefficient=value_range,  # type: ignore[arg-type]
                principal_first_minor_lower=principal_first_lower,
                principal_determinant_lower=principal_determinant_lower,
                completed_potential_first_minor_lower=potential_first_lower,
                completed_potential_determinant_lower=potential_determinant_lower,
                completed_potential_matrix_inverse_used=potential_inverse_used,
                derivative_squared_dual_upper=derivative_squared,
                value_squared_dual_upper=value_squared,
                squared_dual_upper=derivative_squared + value_squared,
                matrix_weighted_derivative_squared_dual_upper=(
                    matrix_derivative_squared
                ),
                matrix_weighted_value_squared_dual_upper=matrix_value_squared,
                matrix_weighted_squared_dual_upper=(
                    matrix_derivative_squared + matrix_value_squared
                ),
            )
        )
    return tuple(output)


@dataclass(frozen=True)
class CorrelatedPrimalEnergyDualCell:
    """One centered positive-radius value-load residual enclosure."""

    radius: RationalInterval
    strong_residual: tuple[RationalInterval, RationalInterval]
    completed_potential_first_minor_lower: Fraction
    completed_potential_determinant_lower: Fraction
    completed_potential_matrix_inverse_used: bool
    scalar_floor_squared_dual_upper: Fraction
    matrix_weighted_squared_dual_upper: Fraction


def correlated_primal_energy_dual_cells(
    profile: ValidatedSkyrmionSharpProfileTube,
    trial: RationalResponseTrial,
    *,
    completed_potential_lower_bound: Fraction,
    degree_limit: int = 8,
    rounding_denominator: int = 10**16,
    trigonometric_terms: int = 6,
) -> tuple[CorrelatedPrimalEnergyDualCell, ...]:
    """Lift the centered outer primal strong residual in the local form metric.

    The strong residual is a value-only functional.  Where the centered
    completed-potential matrix is directly positive, its exact ``2x2`` inverse
    supplies the pointwise dual density.  Remaining cells use the declared
    globally certified scalar floor.
    """
    if completed_potential_lower_bound <= 0:
        raise ValueError("completed-potential lower bound must be positive")
    trial.validate()
    if tuple(cell.radius for cell in profile.cells) != tuple(
        cell.radius for cell in trial.positive_radius_cells
    ):
        raise ValueError("profile and trial partitions differ")
    options = {
        "degree_limit": degree_limit,
        "rounding_denominator": rounding_denominator,
    }
    output = []
    counters: dict[int, int] = {}
    for profile_cell, trial_cell in zip(
        profile.cells, trial.positive_radius_cells, strict=True
    ):
        parent_index = profile_cell.parent_cell_index
        subdivision = counters.get(parent_index, 0)
        counters[parent_index] = subdivision + 1
        if subdivision >= profile.subdivisions_per_parent:
            raise ValueError("profile subdivision ordering is inconsistent")
        field_poly, derivative_poly, second_poly, error0, error1, error2 = (
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
        one = x._coerce(1)
        field = _CenteredTaylorModel.from_polynomial(
            field_poly, error_radius=error0, **options
        )
        field_derivative = _CenteredTaylorModel.from_polynomial(
            derivative_poly, error_radius=error1, **options
        )
        field_second = _CenteredTaylorModel.from_polynomial(
            second_poly, error_radius=error2, **options
        )
        sine, cosine = field.sin_cos(terms=trigonometric_terms)
        x_jet = _ModelRadialJet(x, one)
        time = x_jet * x_jet
        metric_jet = 1 - time * profile.curvature
        rho = _ModelRadialJet(-field_derivative, -field_second)
        sine_over_radius = _ModelRadialJet(
            sine / x,
            (cosine * field_derivative * x - sine) / x.power(2),
        )
        cosine_deficit = _ModelRadialJet(-cosine, sine * field_derivative)
        blocks = regular_conormal_blocks_from_kernels(
            t=time,
            metric_factor=metric_jet,
            profile_deficit_radial_derivative=rho,
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_deficit,
            pion_mass_squared=_constant_radial_jet(
                x, profile.pion_mass_squared
            ),
        )
        source = regular_rotational_source_from_kernels(
            t=time,
            metric_factor=metric_jet,
            profile_deficit_radial_derivative=rho,
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_deficit,
        )
        coordinate = _model_matrix_value(blocks["coordinate"])
        regular_mixed = _model_matrix_value(blocks["mixed"])
        regular_mixed_derivative = tuple(
            tuple(entry.derivative for entry in row) for row in blocks["mixed"]
        )
        regular_principal = _symmetric_part(
            _model_matrix_value(blocks["principal"])
        )
        regular_principal_derivative = _symmetric_part(
            tuple(
                tuple(entry.derivative for entry in row)
                for row in blocks["principal"]
            )
        )
        mixed_jets = tuple(
            tuple(x_jet * entry for entry in row) for row in blocks["mixed"]
        )
        principal_jets = tuple(
            tuple(time * entry for entry in row) for row in blocks["principal"]
        )
        mixed = _model_matrix_value(mixed_jets)
        mixed_derivative = _model_matrix_derivative(mixed_jets)
        principal = _model_matrix_value(principal_jets)
        principal_derivative = _model_matrix_derivative(principal_jets)
        coordinate_source = tuple(
            x_jet * entry for entry in source["coordinate_source"]
        )
        derivative_source = tuple(
            time * entry for entry in source["derivative_source"]
        )
        strong_source = tuple(
            left.value - right.derivative
            for left, right in zip(
                coordinate_source, derivative_source, strict=True
            )
        )
        radial = _trial_models(
            trial_cell.radial_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        tangential = _trial_models(
            trial_cell.tangential_field,
            radius_half_width=radius_half_width,
            options=options,
        )
        value = (radial[0], tangential[0])
        derivative = (radial[1], tangential[1])
        second = (radial[2], tangential[2])
        operator = tuple(
            coordinate_value + derivative_value - principal_value
            for coordinate_value, derivative_value, principal_value in zip(
                _matrix_vector(
                    _matrix_subtract(coordinate, _transpose(mixed_derivative)),
                    value,
                ),
                _matrix_vector(
                    _matrix_subtract(
                        _matrix_subtract(mixed, _transpose(mixed)),
                        principal_derivative,
                    ),
                    derivative,
                ),
                _matrix_vector(principal, second),
                strict=True,
            )
        )
        residual = tuple(
            load - action
            for load, action in zip(strong_source, operator, strict=True)
        )

        symmetric_regular_mixed = _symmetric_part(regular_mixed)
        antisymmetric_regular_mixed = _matrix_scale(
            _matrix_subtract(regular_mixed, _transpose(regular_mixed)),
            Fraction(1, 2),
        )
        completed_potential = _symmetric_part(
            _matrix_add(
                _matrix_add(
                    _matrix_subtract(
                        _matrix_add(
                            _matrix_subtract(coordinate, symmetric_regular_mixed),
                            _matrix_scale(regular_principal, Fraction(1, 4)),
                        ),
                        _matrix_scale(
                            _symmetric_part(regular_mixed_derivative), x
                        ),
                    ),
                    _matrix_scale(regular_principal_derivative, x * Fraction(1, 2)),
                ),
                _matrix_multiply(
                    _matrix_multiply(
                        antisymmetric_regular_mixed,
                        _matrix_inverse(regular_principal),
                    ),
                    antisymmetric_regular_mixed,
                ),
            )
        )
        potential_determinant = (
            completed_potential[0][0] * completed_potential[1][1]
            - completed_potential[0][1] * completed_potential[1][0]
        )
        potential_first_lower = completed_potential[0][0].range().lower
        potential_determinant_lower = potential_determinant.range().lower
        inverse_used = potential_first_lower > 0 and potential_determinant_lower > 0
        residual_range = tuple(entry.range() for entry in residual)
        scalar_square = profile_cell.radius.width * sum(
            _absolute_upper(entry) ** 2 for entry in residual_range
        ) / completed_potential_lower_bound
        matrix_square = (
            radius_half_width
            * _model_quadratic_form(
                residual, _matrix_inverse(completed_potential)
            ).symmetric_integral().upper
            if inverse_used
            else scalar_square
        )
        if matrix_square < 0:
            raise ValueError("matrix-weighted primal dual density is negative")
        output.append(
            CorrelatedPrimalEnergyDualCell(
                radius=profile_cell.radius,
                strong_residual=residual_range,  # type: ignore[arg-type]
                completed_potential_first_minor_lower=potential_first_lower,
                completed_potential_determinant_lower=potential_determinant_lower,
                completed_potential_matrix_inverse_used=inverse_used,
                scalar_floor_squared_dual_upper=scalar_square,
                matrix_weighted_squared_dual_upper=matrix_square,
            )
        )
    return tuple(output)
