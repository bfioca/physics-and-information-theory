"""Quantitative mismatch between local noise and an ideal common rotation.

The finite-time heat-twirl theorem assumes the same stochastic angular motion
acts on target and reference.  This module tests that assumption rather than
silently identifying it with a generic local bath.

For two axial charges with normalized covariance

    C = [[1, c], [c, 1]],

the relational coherence between ``|1,0>`` and ``|0,1>`` has visibility

    v(s,c) = exp[-2 s Delta^2 (1-c)],       s = gamma T.

It is exactly decoherence free only at perfect common mode ``c=1``.  The witness
gives a normalized diamond-distance lower bound ``(1-v)/2`` from the ideal
common-mode channel.  A complementary bounded-generator Duhamel estimate gives
an upper bound for finite spatial covariance matrices.
"""

from __future__ import annotations

from math import exp, isfinite, log, log1p, sqrt
from typing import Sequence


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_correlation(correlation: float) -> None:
    if not isfinite(correlation) or not -1.0 <= correlation <= 1.0:
        raise ValueError("correlation must lie in [-1,1]")


def _validate_dimension(dimension: int) -> None:
    if (
        isinstance(dimension, bool)
        or not isinstance(dimension, int)
        or dimension < 3
    ):
        raise ValueError("dimension must be an integer at least three")


def _validate_axis_count(number_of_axes: int) -> None:
    if (
        isinstance(number_of_axes, bool)
        or not isinstance(number_of_axes, int)
        or number_of_axes < 1
    ):
        raise ValueError("number_of_axes must be a positive integer")


def axial_relational_visibility(
    dimensionless_time: float,
    *,
    correlation: float,
    charge_gap: float = 1.0,
) -> float:
    """Return visibility of ``(|1,0>+|0,1>)/sqrt(2)`` under correlated noise."""
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    _validate_correlation(correlation)
    _validate_positive("charge_gap", charge_gap)
    return exp(
        -2.0
        * dimensionless_time
        * charge_gap**2
        * (1.0 - correlation)
    )


def axial_common_mode_mismatch_lower_bound(
    dimensionless_time: float,
    *,
    correlation: float,
    charge_gap: float = 1.0,
) -> float:
    """Lower-bound normalized diamond distance from perfect common mode.

    The trace distance between the actual and ideal outputs on the relational
    coherence witness is ``(1-v)/2``.  Optimizing over all inputs and ancillas
    can only increase the channel distance.
    """
    visibility = axial_relational_visibility(
        dimensionless_time,
        correlation=correlation,
        charge_gap=charge_gap,
    )
    return 0.5 * (1.0 - visibility)


def maximum_correlation_defect_for_mismatch(
    target_mismatch: float,
    *,
    dimensionless_time: float,
    charge_gap: float = 1.0,
) -> float:
    """Necessary upper bound on ``1-c`` for a target common-mode mismatch.

    A returned value of two means the witness imposes no restriction beyond the
    physical correlation interval.  The target must be smaller than ``1/2``.
    """
    _validate_nonnegative("target_mismatch", target_mismatch)
    if target_mismatch >= 0.5:
        raise ValueError("target_mismatch must be smaller than one half")
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    _validate_positive("charge_gap", charge_gap)
    if dimensionless_time == 0.0:
        return 2.0
    defect = -log1p(-2.0 * target_mismatch) / (
        2.0 * dimensionless_time * charge_gap**2
    )
    return min(2.0, defect)


def minimum_exponential_correlation_length(
    separation: float,
    *,
    target_mismatch: float,
    dimensionless_time: float,
    charge_gap: float = 1.0,
) -> float:
    """Necessary correlation length for ``c(r)=exp(-r/ell_B)``.

    This is a model-specific translation of the exact witness.  Zero means the
    requested error is loose enough that the witness supplies no positive lower
    bound; infinity means perfect correlation is required.
    """
    _validate_nonnegative("separation", separation)
    defect = maximum_correlation_defect_for_mismatch(
        target_mismatch,
        dimensionless_time=dimensionless_time,
        charge_gap=charge_gap,
    )
    if separation == 0.0:
        return 0.0
    if defect >= 1.0:
        return 0.0
    if defect == 0.0:
        return float("inf")
    return separation / (-log1p(-defect))


def logarithmic_schedule_correlation_record(
    dimension: int,
    *,
    mismatch_coefficient: float = 1.0,
    separation: float = 1.0,
    charge_gap: float = 1.0,
) -> dict[str, object]:
    """Audit correlation demands under ``s=(1/2)log d`` and ``eta=A/d``."""
    _validate_dimension(dimension)
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    _validate_nonnegative("separation", separation)
    _validate_positive("charge_gap", charge_gap)
    target_mismatch = mismatch_coefficient / float(dimension)
    if target_mismatch >= 0.5:
        raise ValueError("mismatch_coefficient/dimension must be smaller than one half")
    dimensionless_time = 0.5 * log(float(dimension))
    maximum_defect = maximum_correlation_defect_for_mismatch(
        target_mismatch,
        dimensionless_time=dimensionless_time,
        charge_gap=charge_gap,
    )
    minimum_length = minimum_exponential_correlation_length(
        separation,
        target_mismatch=target_mismatch,
        dimensionless_time=dimensionless_time,
        charge_gap=charge_gap,
    )
    return {
        "dimension_d": dimension,
        "dimensionless_time_s": dimensionless_time,
        "target_common_mode_mismatch_A_over_d": target_mismatch,
        "mismatch_coefficient_A": mismatch_coefficient,
        "axial_charge_gap_Delta": charge_gap,
        "maximum_correlation_defect_1_minus_c": maximum_defect,
        "scaled_defect_d_log_d": (
            maximum_defect * dimension * log(float(dimension))
        ),
        "separation_r": separation,
        "minimum_exponential_correlation_length": minimum_length,
        "minimum_correlation_length_over_separation": (
            0.0 if separation == 0.0 else minimum_length / separation
        ),
        "necessary_scaling": (
            "for fixed nonzero Delta and eta=A/d, 1-c=O(1/(Delta^2 d log d)); "
            "for c(r)=exp(-r/ell_B), ell_B/r=Omega(Delta^2 d log d)"
        ),
    }


def _validated_symmetric_psd_matrix(
    covariance: Sequence[Sequence[float]],
) -> tuple[tuple[float, ...], ...]:
    rows = tuple(tuple(float(value) for value in row) for row in covariance)
    if not rows or any(len(row) != len(rows) for row in rows):
        raise ValueError("covariance must be a nonempty square matrix")
    if any(not isfinite(value) for row in rows for value in row):
        raise ValueError("covariance entries must be finite")
    tolerance = 1.0e-12
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            if abs(value - rows[j][i]) > tolerance:
                raise ValueError("covariance must be symmetric")

    # Cholesky with explicit handling of zero pivots certifies positive
    # semidefiniteness for the small finite-cell covariance matrices used here.
    factor = [[0.0 for _ in rows] for _ in rows]
    for i in range(len(rows)):
        for j in range(i + 1):
            residual = rows[i][j] - sum(
                factor[i][k] * factor[j][k] for k in range(j)
            )
            if i == j:
                if residual < -tolerance:
                    raise ValueError("covariance must be positive semidefinite")
                factor[i][j] = sqrt(max(0.0, residual))
            elif factor[j][j] > tolerance:
                factor[i][j] = residual / factor[j][j]
            elif abs(residual) > tolerance:
                raise ValueError("covariance must be positive semidefinite")
    return rows


def finite_cell_covariance_distance_record(
    covariance: Sequence[Sequence[float]],
    *,
    generator_norm_bounds: Sequence[float],
    dimensionless_time: float,
    number_of_axes: int = 3,
) -> dict[str, object]:
    """Bound distance from rank-one common-mode diffusion on finite cells.

    For bounded local charges ``q_(a,i)`` with supplied norm bounds and

        L_C=-gamma sum_(a,i,j) C_ij [q_(a,i),[q_(a,j),.]],

    the commutator estimate and Duhamel formula give

        (1/2)||exp(T L_C)-exp(T L_*)||_diamond
        <= 2 s n_axes sum_(i,j)|C_ij-1| ||q_i|| ||q_j||,

    capped by one.  Here ``L_*`` has the ideal all-ones rank-one covariance.
    """
    rows = _validated_symmetric_psd_matrix(covariance)
    norms = tuple(float(value) for value in generator_norm_bounds)
    if len(norms) != len(rows):
        raise ValueError("generator_norm_bounds must match covariance dimension")
    if any(not isfinite(value) or value < 0.0 for value in norms):
        raise ValueError("generator norm bounds must be finite and nonnegative")
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    _validate_axis_count(number_of_axes)
    weighted_defect = sum(
        abs(rows[i][j] - 1.0) * norms[i] * norms[j]
        for i in range(len(rows))
        for j in range(len(rows))
    )
    generator_difference_diamond_bound = 4.0 * number_of_axes * weighted_defect
    normalized_channel_distance_bound = min(
        1.0,
        0.5 * dimensionless_time * generator_difference_diamond_bound,
    )
    return {
        "number_of_cells": len(rows),
        "number_of_axes": number_of_axes,
        "dimensionless_time_s": dimensionless_time,
        "covariance": rows,
        "ideal_common_mode_covariance": tuple(
            tuple(1.0 for _ in rows) for _ in rows
        ),
        "generator_norm_bounds": norms,
        "weighted_covariance_l1_defect": weighted_defect,
        "generator_difference_diamond_bound_per_gamma": (
            generator_difference_diamond_bound
        ),
        "normalized_channel_distance_upper_bound": (
            normalized_channel_distance_bound
        ),
        "proof_mechanism": (
            "||[A,[B,.]]||_diamond<=4||A||||B|| and the Duhamel formula "
            "between CPTP contraction semigroups"
        ),
        "scope": "finite cells with bounded charge generators and PSD covariance",
    }


def common_mode_locality_mismatch_certificate(
    *,
    correlation: float = 0.95,
    maximum_dimension: int = 4096,
    mismatch_coefficient: float = 1.0,
    separation: float = 1.0,
    charge_gap: float = 1.0,
) -> dict[str, object]:
    """Audit the common-mode locality-mismatch witness and scaling law."""
    _validate_correlation(correlation)
    _validate_dimension(maximum_dimension)
    if maximum_dimension < 8:
        raise ValueError("maximum_dimension must be at least eight for the scaling audit")
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    _validate_nonnegative("separation", separation)
    _validate_positive("charge_gap", charge_gap)

    times = (0.0, 0.5, 1.0, 2.0, 8.0)
    mismatch_records = tuple(
        {
            "dimensionless_time_s": time,
            "visibility": axial_relational_visibility(
                time,
                correlation=correlation,
                charge_gap=charge_gap,
            ),
            "normalized_diamond_mismatch_lower_bound": (
                axial_common_mode_mismatch_lower_bound(
                    time,
                    correlation=correlation,
                    charge_gap=charge_gap,
                )
            ),
        }
        for time in times
    )
    dimensions = tuple(
        sorted(
            {
                dimension
                for dimension in (8, 32, 128, 512, maximum_dimension)
                if dimension <= maximum_dimension
            }
            | {maximum_dimension}
        )
    )
    scaling_records = tuple(
        logarithmic_schedule_correlation_record(
            dimension,
            mismatch_coefficient=mismatch_coefficient,
            separation=separation,
            charge_gap=charge_gap,
        )
        for dimension in dimensions
    )
    two_cell_covariance = ((1.0, correlation), (correlation, 1.0))
    finite_cell = finite_cell_covariance_distance_record(
        two_cell_covariance,
        generator_norm_bounds=(1.0, 1.0),
        dimensionless_time=1.0,
        number_of_axes=1,
    )
    witness_at_unit_time = axial_common_mode_mismatch_lower_bound(
        1.0,
        correlation=correlation,
        charge_gap=charge_gap,
    )
    mismatch_bounds = tuple(
        record["normalized_diamond_mismatch_lower_bound"]
        for record in mismatch_records
    )
    defect_scales = tuple(
        record["scaled_defect_d_log_d"] for record in scaling_records
    )
    length_ratios = tuple(
        record["minimum_correlation_length_over_separation"]
        for record in scaling_records
    )
    if correlation == 1.0:
        fixed_imperfect_limit_check = True
    else:
        late_time = 10.0 / ((1.0 - correlation) * charge_gap**2)
        fixed_imperfect_limit_check = (
            axial_common_mode_mismatch_lower_bound(
                late_time,
                correlation=correlation,
                charge_gap=charge_gap,
            )
            > 0.499999
        )
    certified_claims = {
        "perfect_common_mode_preserves_relational_coherence": (
            axial_relational_visibility(
                100.0,
                correlation=1.0,
                charge_gap=charge_gap,
            )
            == 1.0
        ),
        "imperfect_common_mode_mismatch_grows_with_time": all(
            right >= left for left, right in zip(mismatch_bounds, mismatch_bounds[1:])
        ),
        "fixed_imperfect_correlation_has_half_distance_witness_limit": (
            fixed_imperfect_limit_check
        ),
        "A_over_d_accuracy_forces_inverse_d_log_d_defect": all(
            2.0 * mismatch_coefficient
            <= scale
            <= 3.0 * mismatch_coefficient
            for scale in (
                defect_scale * charge_gap**2 for defect_scale in defect_scales
            )
        ),
        "exponential_bath_correlation_length_requirement_grows": all(
            right > left for left, right in zip(length_ratios, length_ratios[1:])
        ),
        "finite_cell_duhamel_bound_dominates_axial_witness": (
            finite_cell["normalized_channel_distance_upper_bound"]
            >= witness_at_unit_time
        ),
        "ideal_rank_one_covariance_has_zero_duhamel_error": (
            finite_cell_covariance_distance_record(
                ((1.0, 1.0), (1.0, 1.0)),
                generator_norm_bounds=(1.0, 1.0),
                dimensionless_time=5.0,
                number_of_axes=3,
            )["normalized_channel_distance_upper_bound"]
            == 0.0
        ),
    }
    return {
        "goal": "Common-Mode Locality Mismatch",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "finite_correlation_vs_common_mode_obstruction",
        "central_result": (
            "A relational axial coherence lower-bounds the normalized diamond "
            "distance from ideal common-mode diffusion by "
            "(1-exp[-2 gamma T Delta^2(1-c)])/2. Under gamma T=(1/2)log d, "
            "keeping this mismatch at A/d for fixed Delta requires "
            "1-c=O(1/(Delta^2 d log d))."
        ),
        "spatial_consequence": (
            "For the model c(r)=exp(-r/ell_B), fixed target-reference separation "
            "and A/d mismatch require ell_B/r=Omega(Delta^2 d log d). A fixed finite "
            "correlation length cannot approximate the rank-one common mode along "
            "the logarithmic protocol schedule."
        ),
        "claim_boundary": (
            "the exact lower witness is an axial two-charge Markov model; the "
            "axial charge gap Delta must be specified and the finite-cell upper bound "
            "assumes bounded generators. This is a finite-correlation/common-mode "
            "test, not a generic locality no-go: local baths can have long-range "
            "correlations. It does not derive a static-patch bath, control extra "
            "transverse dynamics, establish isotropic SO(3) covariance, a Davies "
            "limit, or gravitational stress-energy."
        ),
        "certified_claims": certified_claims,
        "axial_charge_gap_Delta": charge_gap,
        "mismatch_records": mismatch_records,
        "logarithmic_schedule_records": scaling_records,
        "finite_cell_covariance_record": finite_cell,
        "next_physics_gate": (
            "compute the target-reference noise covariance from a named local "
            "static-patch field/worldtube interaction and test whether its "
            "correlation defect can satisfy the derived scaling window"
        ),
    }
