"""Centered correlated outer residual for the centrifugal response problem.

The box residual validator ranges ``x``, the profile jet, and the rational
trial jet independently.  This module instead carries their common normalized
subcell coordinate through one Taylor algebra.  The authenticated Newton-tube
errors remain interval remainders, while the exact corrected profile spline,
trial polynomial, trigonometric kernels, and conormal derivatives retain their
deterministic radial correlation.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .centrifugal_skyrmion_conormal_blocks import (
    regular_conormal_blocks_from_kernels,
    regular_rotational_source_from_kernels,
)
from .centrifugal_skyrmion_rational_response_trials import RationalResponseTrial
from .validated_centrifugal_liouville_taylor import _CenteredTaylorModel
from .validated_interval import RationalInterval, RationalPolynomial
from .validated_skyrmion_bvp import (
    _affine_restrict_polynomial,
    _rational_polynomial_add,
    _rational_polynomial_scale,
)
from .validated_skyrmion_sharp_profile import ValidatedSkyrmionSharpProfileTube


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


@dataclass(frozen=True)
class _ModelRadialJet:
    value: _CenteredTaylorModel
    derivative: _CenteredTaylorModel

    def _coerce(self, other):
        if isinstance(other, _ModelRadialJet):
            return other
        return _ModelRadialJet(self.value._coerce(other), self.value._coerce(0))

    def __add__(self, other):
        right = self._coerce(other)
        return _ModelRadialJet(
            self.value + right.value,
            self.derivative + right.derivative,
        )

    __radd__ = __add__

    def __neg__(self):
        return _ModelRadialJet(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        right = self._coerce(other)
        return _ModelRadialJet(
            self.value * right.value,
            self.derivative * right.value + self.value * right.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        right = self._coerce(other)
        return _ModelRadialJet(
            self.value / right.value,
            (
                self.derivative * right.value
                - self.value * right.derivative
            )
            / right.value.power(2),
        )

    def __rtruediv__(self, other):
        return self._coerce(other) / self


def _model_matrix_value(matrix):
    return tuple(tuple(entry.value for entry in row) for row in matrix)


def _model_matrix_derivative(matrix):
    return tuple(tuple(entry.derivative for entry in row) for row in matrix)


def _transpose(matrix):
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _matrix_vector(matrix, vector):
    return tuple(row[0] * vector[0] + row[1] * vector[1] for row in matrix)


def _matrix_subtract(left, right):
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(2))
        for row in range(2)
    )


def _corrected_profile_polynomials(
    profile: ValidatedSkyrmionSharpProfileTube,
    *,
    parent_index: int,
    subdivision: int,
) -> tuple[RationalPolynomial, RationalPolynomial, RationalPolynomial, Fraction, Fraction, Fraction]:
    parent_cell = profile.profile_cells[parent_index]
    parent = profile.parents[parent_index]
    subdivisions = profile.subdivisions_per_parent
    midpoint = Fraction(2 * subdivision + 1, 2 * subdivisions)
    half_width = Fraction(1, 2 * subdivisions)
    physical_center = parent_cell.radius.lower + parent_cell.radius.width * midpoint
    physical_half_width = parent_cell.radius.width * half_width
    base = _affine_restrict_polynomial(
        parent_cell.profile_polynomial, midpoint, half_width
    )
    domain_length = profile.wall_radius - profile.origin_cutoff
    left_center = (
        Fraction(0)
        if profile.left_value_correction.lower <= 0 <= profile.left_value_correction.upper
        else profile.left_value_correction.midpoint
    )
    left_deviation = profile.left_value_correction - left_center
    chi_left = RationalPolynomial(
        (
            (profile.wall_radius - physical_center) / domain_length,
            -physical_half_width / domain_length,
        )
    )
    chi_right = RationalPolynomial(
        (
            (physical_center - profile.origin_cutoff) / domain_length,
            physical_half_width / domain_length,
        )
    )
    corrected = _rational_polynomial_add(
        base,
        _rational_polynomial_scale(chi_left, left_center),
        _rational_polynomial_scale(chi_right, profile.right_value_correction),
    )
    derivative = _rational_polynomial_scale(
        corrected.derivative(), 1 / physical_half_width
    )
    second = _rational_polynomial_scale(
        corrected.derivative().derivative(), 1 / physical_half_width**2
    )
    deviation = _absolute_upper(left_deviation)
    chi_left_size = sum(abs(value) for value in chi_left.coefficients)
    return (
        corrected,
        derivative,
        second,
        parent.profile_error_radius + deviation * chi_left_size,
        parent.derivative_error_radius + deviation / domain_length,
        parent.second_derivative_error_radius,
    )


@dataclass(frozen=True)
class CorrelatedResidualCell:
    radius: RationalInterval
    residual: tuple[RationalInterval, RationalInterval]
    l2_squared_upper: Fraction


def correlated_primal_residual_cells(
    profile: ValidatedSkyrmionSharpProfileTube,
    trial: RationalResponseTrial,
    *,
    degree_limit: int = 8,
    rounding_denominator: int = 10**16,
    trigonometric_terms: int = 6,
) -> tuple[CorrelatedResidualCell, ...]:
    """Enclose the outer primal residual with shared radial correlation."""
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
        metric = 1 - time * profile.curvature
        rho = _ModelRadialJet(-field_derivative, -field_second)
        sine_over_radius = _ModelRadialJet(
            sine / x,
            (cosine * field_derivative * x - sine) / x.power(2),
        )
        cosine_deficit = _ModelRadialJet(-cosine, sine * field_derivative)
        blocks = regular_conormal_blocks_from_kernels(
            t=time,
            metric_factor=metric,
            profile_deficit_radial_derivative=rho,
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_deficit,
            pion_mass_squared=_ModelRadialJet(one, x._coerce(0)),
        )
        source = regular_rotational_source_from_kernels(
            t=time,
            metric_factor=metric,
            profile_deficit_radial_derivative=rho,
            sine_over_radius=sine_over_radius,
            cosine_of_profile_deficit=cosine_deficit,
        )
        coordinate = _model_matrix_value(blocks["coordinate"])
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
        coordinate_source = tuple(x_jet * entry for entry in source["coordinate_source"])
        derivative_source = tuple(time * entry for entry in source["derivative_source"])
        strong_source = tuple(
            left.value - right.derivative
            for left, right in zip(coordinate_source, derivative_source, strict=True)
        )

        def trial_models(polynomial: RationalPolynomial):
            centered = _affine_restrict_polynomial(
                polynomial, Fraction(1, 2), Fraction(1, 2)
            )
            value = _CenteredTaylorModel.from_polynomial(centered, **options)
            derivative = _CenteredTaylorModel.from_polynomial(
                _rational_polynomial_scale(
                    centered.derivative(), 1 / radius_half_width
                ),
                **options,
            )
            second = _CenteredTaylorModel.from_polynomial(
                _rational_polynomial_scale(
                    centered.derivative().derivative(), 1 / radius_half_width**2
                ),
                **options,
            )
            return value, derivative, second

        radial = trial_models(trial_cell.radial_field)
        tangential = trial_models(trial_cell.tangential_field)
        value = (radial[0], tangential[0])
        derivative = (radial[1], tangential[1])
        second = (radial[2], tangential[2])
        mixed_transpose = _transpose(mixed)
        operator = tuple(
            coordinate_value + derivative_value - principal_value
            for coordinate_value, derivative_value, principal_value in zip(
                _matrix_vector(
                    _matrix_subtract(coordinate, _transpose(mixed_derivative)),
                    value,
                ),
                _matrix_vector(
                    _matrix_subtract(
                        _matrix_subtract(mixed, mixed_transpose),
                        principal_derivative,
                    ),
                    derivative,
                ),
                _matrix_vector(principal, second),
                strict=True,
            )
        )
        residual = tuple(
            (load - action).range()
            for load, action in zip(strong_source, operator, strict=True)
        )
        square = profile_cell.radius.width * sum(
            _absolute_upper(entry) ** 2 for entry in residual
        )
        output.append(CorrelatedResidualCell(profile_cell.radius, residual, square))
    return tuple(output)
