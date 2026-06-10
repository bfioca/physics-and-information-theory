"""Weak completed-square dual bound on the regular-origin cell.

With ``t=x^2`` and ``y=x a(t)``, the Fuchs-form residual coefficients are

``r0=x r0_hat(t)`` and ``r1=t r1_hat(t)``.

The Liouville square uses ``x d=x v'+T v`` with
``T=I/2-Pbar^-1 antisym(Mbar)``.  Therefore

``R(v)=integral x [r1_hat dot (x d)
                    +(r0_hat-T^T r1_hat) dot v] dx``.

Both terms have the exact weight ``integral_0^x0 x^2 dx=x0^3/3``.  This weak
representation joins the positive-radius weak adjoint residual without an
artificial cutoff conormal trace.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Literal

from .centrifugal_skyrmion_rational_response_trials import RationalResponseTrial
from .validated_centrifugal_origin_adjoint_load import (
    validated_origin_weak_master_load_cell,
)
from .validated_centrifugal_origin_profile_jets import (
    rational_origin_trial_cell_from_archive,
    validated_authenticated_origin_profile_kernel_cells,
)
from .validated_centrifugal_origin_response_residual import (
    RationalOriginTrialCell,
    ValidatedOriginConormalCell,
    validated_origin_conormal_cell_from_profile,
)
from .validated_centrifugal_response_residual import IntervalMatrix2, IntervalVector2
from .validated_interval import RationalInterval, sqrt_fraction_interval
from .validated_skyrmion_quintic_family import ValidatedSkyrmionQuinticFamily


OriginWeakLoad = Literal["rotational", "master"]


def _absolute_upper(value: RationalInterval) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def _transpose(matrix: IntervalMatrix2) -> IntervalMatrix2:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def _matrix_vector(
    matrix: IntervalMatrix2, vector: IntervalVector2
) -> IntervalVector2:
    return tuple(
        row[0] * vector[0] + row[1] * vector[1] for row in matrix
    )  # type: ignore[return-value]


def _matrix_subtract(
    left: IntervalMatrix2, right: IntervalMatrix2
) -> IntervalMatrix2:
    return tuple(
        tuple(left[row][column] - right[row][column] for column in range(2))
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_scale(
    matrix: IntervalMatrix2, scalar: Fraction
) -> IntervalMatrix2:
    return tuple(
        tuple(entry.scale(scalar) for entry in row) for row in matrix
    )  # type: ignore[return-value]


def _matrix_multiply(
    left: IntervalMatrix2, right: IntervalMatrix2
) -> IntervalMatrix2:
    zero = RationalInterval.point(0)
    return tuple(
        tuple(
            sum(
                (left[row][inner] * right[inner][column] for inner in range(2)),
                zero,
            )
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def _matrix_inverse(matrix: IntervalMatrix2) -> IntervalMatrix2:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant.contains_zero():
        raise ValueError("origin principal determinant contains zero")
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


@dataclass(frozen=True)
class ValidatedOriginWeakEnergyDualCell:
    """One authenticated slope-cell weak origin residual bound."""

    time: RationalInterval
    radius_cutoff: Fraction
    residual_value_hat: IntervalVector2
    residual_derivative_hat: IntervalVector2
    completed_value_hat: IntervalVector2
    completed_multiplier: IntervalMatrix2
    principal_shifted_first_minor_lower: Fraction
    principal_shifted_determinant_lower: Fraction
    derivative_squared_dual_upper: Fraction
    value_squared_dual_upper: Fraction
    squared_dual_upper: Fraction


def validated_origin_weak_energy_dual_cell(
    coefficients: ValidatedOriginConormalCell,
    trial: RationalOriginTrialCell,
    *,
    principal_lower_bound: Fraction,
    completed_potential_lower_bound: Fraction,
) -> ValidatedOriginWeakEnergyDualCell:
    """Lift one regular-origin weak residual in the completed-square norm."""
    if principal_lower_bound <= 0 or completed_potential_lower_bound <= 0:
        raise ValueError("completed-square lower bounds must be positive")
    horizon = trial.time_horizon
    if coefficients.time != RationalInterval(Fraction(0), horizon):
        raise ValueError("coefficient and trial time cells do not agree")
    radius = sqrt_fraction_interval(horizon).lower
    if radius * radius != horizon:
        raise ValueError("time horizon must be a rational square")

    (u, v), (u_t, v_t), _ = trial.jet_range()
    time = coefficients.time
    a = (-v + time * u, v)
    physical_derivative = (
        -v + time * u * 3 - time * v_t * 2 + time.power(2) * u_t * 2,
        v + time * v_t * 2,
    )
    residual_value_hat = tuple(
        source - coordinate - mixed
        for source, coordinate, mixed in zip(
            coefficients.coordinate_source_hat,
            _matrix_vector(coefficients.coordinate, a),
            _matrix_vector(coefficients.mixed, physical_derivative),
            strict=True,
        )
    )
    residual_derivative_hat = tuple(
        source - mixed - principal
        for source, mixed, principal in zip(
            coefficients.derivative_source_hat,
            _matrix_vector(_transpose(coefficients.mixed), a),
            _matrix_vector(coefficients.principal, physical_derivative),
            strict=True,
        )
    )

    point = RationalInterval.point
    shifted = (
        (
            coefficients.principal[0][0] - principal_lower_bound,
            coefficients.principal[0][1],
        ),
        (
            coefficients.principal[1][0],
            coefficients.principal[1][1] - principal_lower_bound,
        ),
    )
    shifted_determinant = (
        shifted[0][0] * shifted[1][1] - shifted[0][1] * shifted[1][0]
    )
    if shifted[0][0].lower <= 0 or shifted_determinant.lower <= 0:
        raise ValueError("Pbar-principal_lower_bound*I is not certified positive")
    antisymmetric_mixed = _matrix_scale(
        _matrix_subtract(coefficients.mixed, _transpose(coefficients.mixed)),
        Fraction(1, 2),
    )
    identity_half: IntervalMatrix2 = (
        (point(Fraction(1, 2)), point(0)),
        (point(0), point(Fraction(1, 2))),
    )
    multiplier = _matrix_subtract(
        identity_half,
        _matrix_multiply(
            _matrix_inverse(coefficients.principal), antisymmetric_mixed
        ),
    )
    completed_value_hat = tuple(
        left - right
        for left, right in zip(
            residual_value_hat,
            _matrix_vector(_transpose(multiplier), residual_derivative_hat),
            strict=True,
        )
    )
    weight = radius**3 / 3
    derivative_square = weight * sum(
        _absolute_upper(entry) ** 2 for entry in residual_derivative_hat
    ) / principal_lower_bound
    value_square = weight * sum(
        _absolute_upper(entry) ** 2 for entry in completed_value_hat
    ) / completed_potential_lower_bound
    return ValidatedOriginWeakEnergyDualCell(
        time=coefficients.time,
        radius_cutoff=radius,
        residual_value_hat=residual_value_hat,  # type: ignore[arg-type]
        residual_derivative_hat=residual_derivative_hat,  # type: ignore[arg-type]
        completed_value_hat=completed_value_hat,  # type: ignore[arg-type]
        completed_multiplier=multiplier,
        principal_shifted_first_minor_lower=shifted[0][0].lower,
        principal_shifted_determinant_lower=shifted_determinant.lower,
        derivative_squared_dual_upper=derivative_square,
        value_squared_dual_upper=value_square,
        squared_dual_upper=derivative_square + value_square,
    )


@dataclass(frozen=True)
class ValidatedOriginWeakEnergyDualFamily:
    """Weak residual bound over every authenticated shooting-slope cell."""

    trial_name: str
    load: OriginWeakLoad
    cells: tuple[ValidatedOriginWeakEnergyDualCell, ...]
    maximum_squared_dual_upper: Fraction
    maximum_energy_dual_upper: Fraction


def validated_archived_origin_weak_energy_dual_family(
    family: ValidatedSkyrmionQuinticFamily,
    trial: RationalResponseTrial,
    *,
    load: OriginWeakLoad,
    principal_lower_bound: Fraction = Fraction(1, 100),
    completed_potential_lower_bound: Fraction = Fraction(1, 100),
    kernel_terms: int = 4,
    green_terms: int = 8,
    gravitational_coupling: Fraction = Fraction(1),
) -> ValidatedOriginWeakEnergyDualFamily:
    """Certify a primal rotational or loaded-adjoint origin weak residual."""
    if load not in ("rotational", "master"):
        raise ValueError("load must be 'rotational' or 'master'")
    trial.validate()
    if trial.origin.cutoff != family.cutoff:
        raise ValueError("trial and profile-family origin cutoffs differ")
    regular_trial = rational_origin_trial_cell_from_archive(trial.origin)
    authenticated = validated_authenticated_origin_profile_kernel_cells(
        family, kernel_terms=kernel_terms
    )
    output = []
    for profile in authenticated:
        coefficients = validated_origin_conormal_cell_from_profile(
            profile.kernels,
            pion_mass_squared=family.pion_mass_squared,
        )
        if load == "master":
            master = validated_origin_weak_master_load_cell(
                profile.kernels,
                curvature=family.curvature,
                pion_mass_squared=family.pion_mass_squared,
                gravitational_coupling=gravitational_coupling,
                patch_radius=Fraction(20),
                green_terms=green_terms,
            )
            coefficients = replace(
                coefficients,
                coordinate_source_hat=master.coordinate_source_hat,
                coordinate_source_hat_time_derivative=(
                    master.coordinate_source_hat_time_derivative
                ),
                derivative_source_hat=master.derivative_source_hat,
                derivative_source_hat_time_derivative=(
                    master.derivative_source_hat_time_derivative
                ),
            )
        output.append(
            validated_origin_weak_energy_dual_cell(
                coefficients,
                regular_trial,
                principal_lower_bound=principal_lower_bound,
                completed_potential_lower_bound=completed_potential_lower_bound,
            )
        )
    maximum_square = max(cell.squared_dual_upper for cell in output)
    return ValidatedOriginWeakEnergyDualFamily(
        trial_name=trial.name,
        load=load,
        cells=tuple(output),
        maximum_squared_dual_upper=maximum_square,
        maximum_energy_dual_upper=sqrt_fraction_interval(maximum_square).upper,
    )
