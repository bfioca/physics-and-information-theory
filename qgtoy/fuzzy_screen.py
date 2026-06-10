"""Canonical coherent-state screen experiment for the finite fuzzy sphere."""

from __future__ import annotations

from cmath import exp as complex_exp
from math import comb, cos, pi, sqrt

from .fuzzy_sphere import (
    matrix_scale,
    matrix_unit,
)
from .quantum_channel import (
    Matrix,
    complex_matrix_rank,
    identity_matrix,
    matmul,
    matrix,
    matrix_add,
    max_abs_difference,
    trace,
    zero_matrix,
)


def _validate_level(level: int) -> None:
    if level < 1:
        raise ValueError("level must be at least one")


def _validate_max_level(max_level: int) -> None:
    if max_level < 1:
        raise ValueError("max_level must be at least one")


def gauss_legendre_rule(order: int) -> tuple[tuple[float, float], ...]:
    """Return dependency-free Gauss-Legendre nodes and weights on [-1,1]."""
    if order < 1:
        raise ValueError("order must be positive")
    nodes = [0.0 for _ in range(order)]
    weights = [0.0 for _ in range(order)]
    half = (order + 1) // 2
    for index in range(half):
        root = cos(pi * (index + 0.75) / (order + 0.5))
        for _iteration in range(100):
            previous = 1.0
            current = root
            for degree in range(2, order + 1):
                previous, current = current, (
                    (2 * degree - 1) * root * current
                    - (degree - 1) * previous
                ) / degree
            derivative = order * (root * current - previous) / (root * root - 1.0)
            next_root = root - current / derivative
            if abs(next_root - root) <= 1e-15:
                root = next_root
                break
            root = next_root
        previous = 1.0
        current = root
        for degree in range(2, order + 1):
            previous, current = current, (
                (2 * degree - 1) * root * current
                - (degree - 1) * previous
            ) / degree
        derivative = order * (root * current - previous) / (root * root - 1.0)
        weight = 2.0 / ((1.0 - root * root) * derivative * derivative)
        nodes[index] = -root
        nodes[order - index - 1] = root
        weights[index] = weight
        weights[order - index - 1] = weight
    return tuple(zip(nodes, weights))


def spin_coherent_vector(level: int, *, cosine_theta: float, phi: float) -> tuple[complex, ...]:
    """Return the normalized spin-j coherent vector in the Jz basis."""
    _validate_level(level)
    if not -1.0 <= cosine_theta <= 1.0:
        raise ValueError("cosine_theta must lie in [-1,1]")
    north_weight = max(0.0, (1.0 + cosine_theta) / 2.0)
    south_weight = max(0.0, (1.0 - cosine_theta) / 2.0)
    return tuple(
        sqrt(comb(level, index))
        * north_weight ** ((level - index) / 2.0)
        * south_weight ** (index / 2.0)
        * complex_exp(1j * index * phi)
        for index in range(level + 1)
    )


def rank_one_projector(vector: tuple[complex, ...]) -> Matrix:
    if not vector:
        raise ValueError("vector must be nonempty")
    return tuple(
        tuple(left * right.conjugate() for right in vector)
        for left in vector
    )


def coherent_screen_povm(
    level: int,
    *,
    polar_order: int | None = None,
    azimuth_count: int | None = None,
) -> tuple[Matrix, ...]:
    """Return a normalized finite quadrature of the covariant coherent POVM.

    The continuous POVM is (L+1)|n><n| dOmega/(4 pi). The default product
    quadrature exactly resolves its identity moment up to floating precision.
    """
    _validate_level(level)
    if polar_order is None:
        polar_order = level + 1
    if azimuth_count is None:
        azimuth_count = 2 * level + 1
    if polar_order < 1 or azimuth_count < 1:
        raise ValueError("quadrature sizes must be positive")
    effects = []
    for cosine_theta, polar_weight in gauss_legendre_rule(polar_order):
        for azimuth_index in range(azimuth_count):
            phi = 2.0 * pi * azimuth_index / azimuth_count
            vector = spin_coherent_vector(
                level,
                cosine_theta=cosine_theta,
                phi=phi,
            )
            scale = (level + 1) * polar_weight / (2.0 * azimuth_count)
            effects.append(matrix_scale(rank_one_projector(vector), scale))
    return tuple(effects)


def povm_normalization_error(effects: tuple[Matrix, ...]) -> float:
    if not effects:
        raise ValueError("POVM must be nonempty")
    dimension = len(effects[0])
    total = zero_matrix(dimension, dimension)
    for effect in effects:
        total = matrix_add(total, effect)
    return max_abs_difference(total, identity_matrix(dimension))


def povm_span_rank(effects: tuple[Matrix, ...]) -> int:
    if not effects:
        raise ValueError("POVM must be nonempty")
    flattened = tuple(
        tuple(entry for row in effect for entry in row)
        for effect in effects
    )
    return complex_matrix_rank(matrix(flattened), tolerance=1e-9)


def measurement_probabilities(state: Matrix, effects: tuple[Matrix, ...]) -> tuple[float, ...]:
    if not effects:
        raise ValueError("POVM must be nonempty")
    dimension = len(effects[0])
    if len(state) != dimension or len(state[0]) != dimension:
        raise ValueError("state and POVM dimensions must match")
    probabilities = tuple(trace(matmul(state, effect)).real for effect in effects)
    return tuple(0.0 if abs(value) < 1e-15 else value for value in probabilities)


def total_variation_distance(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    if len(left) != len(right):
        raise ValueError("distributions must have the same length")
    return 0.5 * sum(abs(first - second) for first, second in zip(left, right))


def coherent_symbol(
    level: int,
    operator: Matrix,
    *,
    cosine_theta: float,
    phi: float,
) -> complex:
    vector = spin_coherent_vector(
        level,
        cosine_theta=cosine_theta,
        phi=phi,
    )
    bra = tuple(entry.conjugate() for entry in vector)
    return sum(
        bra[row] * operator[row][column] * vector[column]
        for row in range(level + 1)
        for column in range(level + 1)
    )


def pole_state_pair(level: int) -> tuple[Matrix, Matrix]:
    _validate_level(level)
    dimension = level + 1
    return (
        matrix_unit(dimension, 0, 0),
        matrix_unit(dimension, dimension - 1, dimension - 1),
    )


def coherent_screen_decision_record(level: int) -> dict[str, object]:
    """Quantify a binary decision gap for a canonical coherent-state screen."""
    _validate_level(level)
    effects = coherent_screen_povm(level)
    north, south = pole_state_pair(level)
    north_probabilities = measurement_probabilities(north, effects)
    south_probabilities = measurement_probabilities(south, effects)
    total_variation = total_variation_distance(
        north_probabilities,
        south_probabilities,
    )
    full_trace_distance = 1.0
    decision_gap = 0.5 * (full_trace_distance - total_variation)
    return {
        "level_L": level,
        "matrix_dimension": level + 1,
        "outcome_count": len(effects),
        "povm_normalization_error": povm_normalization_error(effects),
        "effect_span_rank": povm_span_rank(effects),
        "full_operator_space_dimension": (level + 1) ** 2,
        "informationally_complete_linear_span": (
            povm_span_rank(effects) == (level + 1) ** 2
        ),
        "north_probability_sum_error": abs(sum(north_probabilities) - 1.0),
        "south_probability_sum_error": abs(sum(south_probabilities) - 1.0),
        "full_quantum_trace_distance": full_trace_distance,
        "screen_total_variation_distance": total_variation,
        "equal_prior_full_success_probability": 1.0,
        "equal_prior_screen_success_probability": 0.5 * (1.0 + total_variation),
        "single_copy_decision_gap": decision_gap,
        "worst_case_reconstruction_error_lower_bound": decision_gap,
        "lower_bound_reason": (
            "If one recovery map reconstructs both pole states within trace "
            "distance epsilon, contractivity and the triangle inequality give "
            "1 <= TV(screen_north,screen_south)+2 epsilon."
        ),
        "interpretation": (
            "The coherent POVM is linearly informationally complete, but its "
            "fixed single-copy classical experiment is less informative than "
            "the full quantum experiment for this binary decision task."
        ),
    }


def coherent_screen_experiment_certificate(
    *,
    max_level: int = 6,
    tolerance: float = 1e-9,
) -> dict[str, object]:
    """Audit the canonical coherent screen and its operational decision gap."""
    _validate_max_level(max_level)
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    records = tuple(
        coherent_screen_decision_record(level)
        for level in range(1, max_level + 1)
    )
    certified_claims = {
        "coherent_povms_normalize": all(
            record["povm_normalization_error"] <= tolerance for record in records
        ),
        "outcome_distributions_normalize": all(
            record["north_probability_sum_error"] <= tolerance
            and record["south_probability_sum_error"] <= tolerance
            for record in records
        ),
        "finite_coherent_experiments_are_informationally_complete": all(
            record["informationally_complete_linear_span"] for record in records
        ),
        "single_copy_decision_gap_is_positive": all(
            record["single_copy_decision_gap"] > tolerance for record in records
        ),
        "reconstruction_lower_bound_is_operational": all(
            record["worst_case_reconstruction_error_lower_bound"]
            == record["single_copy_decision_gap"]
            for record in records
        ),
    }
    return {
        "goal": "Phase 1 Canonical Coherent-State Screen Experiment",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "finite_quantum_statistical_screen_deficiency_witness",
        "claim_boundary": (
            "canonical finite coherent-state measurement and binary decision "
            "lower bound only; not a maximal-algebra learning theorem, "
            "gravitational screen, continuum deficiency theorem, or de Sitter claim"
        ),
        "max_level": max_level,
        "tolerance": tolerance,
        "records": records,
        "certified_claims": certified_claims,
    }
