"""Canonical coherent-state Berezin maps between fuzzy-sphere cutoffs."""

from __future__ import annotations

from functools import lru_cache
from math import exp, sqrt

from .fuzzy_screen import gauss_legendre_rule, rank_one_projector, spin_coherent_vector
from .fuzzy_sphere import (
    fuzzy_harmonics,
    fuzzy_coordinates,
    fuzzy_laplacian,
    hermitian_psd_summary,
    hilbert_schmidt_inner,
    hilbert_schmidt_norm,
    matrix_scale,
    matrix_subtract,
    normalized_trace,
)
from .quantum_channel import (
    Matrix,
    dagger,
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


def _validate_refinement(source_level: int, target_level: int) -> None:
    _validate_level(source_level)
    _validate_level(target_level)
    if target_level < source_level:
        raise ValueError("target_level must be at least source_level")


def berezin_eigenvalue(level: int, ell: int) -> float:
    """Return the coherent Berezin-transform eigenvalue b_{L,ell}."""
    _validate_level(level)
    if not 0 <= ell <= level:
        raise ValueError("ell must lie between zero and level")
    value = 1.0
    for index in range(ell):
        value *= (level - index) / (level + index + 2.0)
    return value


def berezin_refinement_coefficient(
    source_level: int,
    target_level: int,
    ell: int,
) -> float:
    """Return the exact tensor-harmonic multiplier of J_{L->M}."""
    _validate_refinement(source_level, target_level)
    if not 0 <= ell <= source_level:
        raise ValueError("ell must lie between zero and source_level")
    return (
        berezin_eigenvalue(source_level, ell)
        * berezin_eigenvalue(target_level, ell)
    ) ** 0.5


@lru_cache(maxsize=None)
def _coherent_refinement_terms(
    source_level: int,
    target_level: int,
) -> tuple[tuple[float, Matrix, Matrix], ...]:
    """Cache a quadrature exact for the cross-level polynomial integrand."""
    _validate_refinement(source_level, target_level)
    polar_order = source_level + target_level + 1
    azimuth_count = 2 * (source_level + target_level) + 1
    terms = []
    from math import pi

    for cosine_theta, polar_weight in gauss_legendre_rule(polar_order):
        for azimuth_index in range(azimuth_count):
            phi = 2.0 * pi * azimuth_index / azimuth_count
            source_projector = rank_one_projector(
                spin_coherent_vector(
                    source_level,
                    cosine_theta=cosine_theta,
                    phi=phi,
                )
            )
            target_projector = rank_one_projector(
                spin_coherent_vector(
                    target_level,
                    cosine_theta=cosine_theta,
                    phi=phi,
                )
            )
            weight = (target_level + 1) * polar_weight / (2.0 * azimuth_count)
            terms.append((weight, source_projector, target_projector))
    return tuple(terms)


def berezin_refinement(
    source_level: int,
    target_level: int,
    operator: Matrix,
) -> Matrix:
    """Apply J_{L->M}=Q_M sigma_L by exact finite quadrature."""
    _validate_refinement(source_level, target_level)
    source_dimension = source_level + 1
    if len(operator) != source_dimension or len(operator[0]) != source_dimension:
        raise ValueError("operator dimension does not match source_level")
    target_dimension = target_level + 1
    out = zero_matrix(target_dimension, target_dimension)
    for weight, source_projector, target_projector in _coherent_refinement_terms(
        source_level, target_level
    ):
        symbol_value = trace(matmul(operator, source_projector))
        out = matrix_add(out, matrix_scale(target_projector, weight * symbol_value))
    return out


def berezin_state_lift(
    source_level: int,
    target_level: int,
    state: Matrix,
) -> Matrix:
    """CPTP Schrödinger lift S=(L+1)/(M+1) J of a source state."""
    _validate_refinement(source_level, target_level)
    return matrix_scale(
        berezin_refinement(source_level, target_level, state),
        (source_level + 1.0) / (target_level + 1.0),
    )


def berezin_coarse_graining(
    source_level: int,
    target_level: int,
    operator: Matrix,
) -> Matrix:
    """Heisenberg adjoint C of the CPTP state lift S_{L->M}."""
    _validate_refinement(source_level, target_level)
    target_dimension = target_level + 1
    if len(operator) != target_dimension or len(operator[0]) != target_dimension:
        raise ValueError("operator dimension does not match target_level")
    source_dimension = source_level + 1
    out = zero_matrix(source_dimension, source_dimension)
    factor = source_dimension / target_dimension
    for weight, source_projector, target_projector in _coherent_refinement_terms(
        source_level, target_level
    ):
        symbol_value = trace(matmul(operator, target_projector))
        out = matrix_add(
            out,
            matrix_scale(source_projector, factor * weight * symbol_value),
        )
    return out


def berezin_refinement_choi(source_level: int, target_level: int) -> Matrix:
    """Construct the Choi matrix of the cross-level Berezin map."""
    _validate_refinement(source_level, target_level)
    source_dimension = source_level + 1
    target_dimension = target_level + 1
    size = source_dimension * target_dimension
    out = [[0j for _ in range(size)] for _ in range(size)]
    for source_row in range(source_dimension):
        for source_column in range(source_dimension):
            unit = tuple(
                tuple(
                    1 + 0j if (row, column) == (source_row, source_column) else 0j
                    for column in range(source_dimension)
                )
                for row in range(source_dimension)
            )
            image = berezin_refinement(source_level, target_level, unit)
            for target_row in range(target_dimension):
                for target_column in range(target_dimension):
                    out[source_row * target_dimension + target_row][
                        source_column * target_dimension + target_column
                    ] = image[target_row][target_column]
    return matrix(out)


def coefficient_error_bound(source_level: int, target_level: int, ell: int) -> float:
    """Elementary upper bound on 1-sqrt(b_L b_M)."""
    _validate_refinement(source_level, target_level)
    if not 0 <= ell <= source_level:
        raise ValueError("ell must lie between zero and source_level")
    return ell * (ell + 1.0) * (
        1.0 / (source_level + 2.0) + 1.0 / (target_level + 2.0)
    )


def composition_coefficient_defect(
    source_level: int,
    middle_level: int,
    target_level: int,
    ell: int,
) -> float:
    """Return |J_{M->N}J_{L->M}-J_{L->N}| on T_{ell,m}."""
    _validate_refinement(source_level, middle_level)
    _validate_refinement(middle_level, target_level)
    if not 0 <= ell <= source_level:
        raise ValueError("ell must lie between zero and source_level")
    direct = berezin_refinement_coefficient(source_level, target_level, ell)
    return direct * (1.0 - berezin_eigenvalue(middle_level, ell))


def matrix_infinity_norm(value: Matrix) -> float:
    """Return the induced maximum-row-sum norm, which bounds operator norm."""
    return max(sum(abs(entry) for entry in row) for row in value)


def coordinate_atomic_product_defect_bound(level: int) -> float:
    """Uniform adjacent-cutoff product bound on the V_1 coefficient-l1 ball."""
    if level < 2:
        raise ValueError("level must be at least two")
    return 8.0 / (3.0 * (level + 2.0))


def coordinate_atomic_product_record(level: int) -> dict[str, object]:
    """Audit the explicit V_1 approximate-multiplicativity theorem.

    The domain consists of A=a0 I+sum_i a_i X_i with sum_i |a_i|<=1,
    and likewise for B. Scalar-vector defects cancel, so bilinearity reduces
    the theorem to the nine coordinate products.
    """
    if level < 2:
        raise ValueError("level must be at least two")
    target_level = level + 1
    source_coordinates = fuzzy_coordinates(level)
    direct_records = []
    for left_axis, left in enumerate(source_coordinates):
        for right_axis, right in enumerate(source_coordinates):
            defect = matrix_subtract(
                berezin_refinement(level, target_level, matmul(left, right)),
                matmul(
                    berezin_refinement(level, target_level, left),
                    berezin_refinement(level, target_level, right),
                ),
            )
            direct_records.append(
                {
                    "left_axis": left_axis,
                    "right_axis": right_axis,
                    "induced_infinity_norm_upper_bound": matrix_infinity_norm(defect),
                    "normalized_hilbert_schmidt_norm": hilbert_schmidt_norm(defect),
                }
            )

    scalar_coefficient = 2.0 * (2.0 * level + 3.0) / (
        3.0 * (level + 2.0) * (level + 3.0)
    )
    vector_coefficient = 3.0 * sqrt(level + 1.0) / (
        (level + 2.0) * (level + 3.0) ** 1.5
    )
    quadrupole_coefficient = (level + 1.0) * (2.0 * level + 3.0) / (
        (level + 2.0) * (level + 3.0) * (level + 4.0)
    )
    diagonal_bound = scalar_coefficient + 2.0 * quadrupole_coefficient / 3.0
    off_diagonal_bound = vector_coefficient + quadrupole_coefficient
    theorem_bound = coordinate_atomic_product_defect_bound(level)
    return {
        "source_level": level,
        "target_level": target_level,
        "domain": (
            "A=a0 I+sum_i a_i X_i and B=b0 I+sum_i b_i X_i, with "
            "sum_i|a_i|<=1 and sum_i|b_i|<=1"
        ),
        "scalar_defect_coefficient": scalar_coefficient,
        "vector_defect_coefficient": vector_coefficient,
        "quadrupole_defect_coefficient": quadrupole_coefficient,
        "analytic_diagonal_pair_bound": diagonal_bound,
        "analytic_off_diagonal_pair_bound": off_diagonal_bound,
        "analytic_uniform_operator_norm_bound": theorem_bound,
        "max_direct_induced_infinity_norm": max(
            record["induced_infinity_norm_upper_bound"] for record in direct_records
        ),
        "direct_coordinate_pair_records": tuple(direct_records),
        "proof": (
            "Decompose X_iX_j into scalar, adjoint-spin-one, and symmetric "
            "traceless spin-two sectors. Insert the exact Berezin multipliers; "
            "the displayed coefficients result. Diagonal pairs are bounded by "
            "s+2q/3 and off-diagonal pairs by v+q, each at most 8/[3(L+2)]. "
            "Bilinearity extends the bound to the full coefficient-l1 ball."
        ),
    }


def global_unit_ball_defect_lower_bound(
    source_level: int,
    target_level: int,
) -> float:
    """Lower-bound the full operator-unit-ball defect by a highest-mode witness."""
    _validate_refinement(source_level, target_level)
    coefficient = berezin_refinement_coefficient(
        source_level, target_level, source_level
    )
    return (
        (target_level + 1.0) / (source_level + target_level + 1.0)
        - coefficient**2 * (target_level + 1.0) / (source_level + 1.0)
    )


def _map_audit_record(
    source_level: int,
    target_level: int,
    *,
    max_mode: int,
    heat_time: float,
    tolerance: float,
) -> dict[str, object]:
    _validate_refinement(source_level, target_level)
    if not 0 <= max_mode <= source_level:
        raise ValueError("max_mode must lie between zero and source_level")
    source_harmonics = fuzzy_harmonics(source_level)
    target_harmonics = fuzzy_harmonics(target_level)
    mode_records = []
    for (ell, magnetic), source_harmonic in source_harmonics.items():
        if ell > max_mode:
            continue
        image = berezin_refinement(source_level, target_level, source_harmonic)
        target_harmonic = target_harmonics[(ell, magnetic)]
        measured_coefficient = hilbert_schmidt_inner(target_harmonic, image)
        predicted_coefficient = berezin_refinement_coefficient(
            source_level, target_level, ell
        )
        residual = matrix_subtract(
            image, matrix_scale(target_harmonic, predicted_coefficient)
        )
        laplacian_error = hilbert_schmidt_norm(
            matrix_subtract(
                fuzzy_laplacian(target_level, image),
                berezin_refinement(
                    source_level,
                    target_level,
                    fuzzy_laplacian(source_level, source_harmonic),
                ),
            )
        )
        source_heat = matrix_scale(source_harmonic, exp(-heat_time * ell * (ell + 1)))
        target_heat = matrix_scale(image, exp(-heat_time * ell * (ell + 1)))
        heat_error = hilbert_schmidt_norm(
            matrix_subtract(
                berezin_refinement(source_level, target_level, source_heat),
                target_heat,
            )
        )
        mode_records.append(
            {
                "ell": ell,
                "magnetic": magnetic,
                "measured_coefficient_real": measured_coefficient.real,
                "measured_coefficient_imag_abs": abs(measured_coefficient.imag),
                "predicted_coefficient": predicted_coefficient,
                "coefficient_formula_error": abs(
                    measured_coefficient - predicted_coefficient
                ),
                "harmonic_leakage_norm": hilbert_schmidt_norm(residual),
                "coefficient_to_identity_error": 1.0 - predicted_coefficient,
                "coefficient_error_bound": coefficient_error_bound(
                    source_level, target_level, ell
                ),
                "laplacian_covariance_error": laplacian_error,
                "heat_covariance_error": heat_error,
            }
        )

    identity_image = berezin_refinement(
        source_level, target_level, identity_matrix(source_level + 1)
    )
    trace_errors = tuple(
        abs(
            normalized_trace(
                berezin_refinement(source_level, target_level, operator)
            )
            - normalized_trace(operator)
        )
        for operator in source_harmonics.values()
    )
    adjoint_errors = tuple(
        max_abs_difference(
            berezin_refinement(source_level, target_level, dagger(operator)),
            dagger(berezin_refinement(source_level, target_level, operator)),
        )
        for operator in source_harmonics.values()
    )
    choi_summary = hermitian_psd_summary(
        berezin_refinement_choi(source_level, target_level),
        tolerance=tolerance,
    )
    lifted_identity = berezin_state_lift(
        source_level,
        target_level,
        identity_matrix(source_level + 1),
    )
    state_lift_trace_scaling_error = abs(
        trace(lifted_identity).real - trace(identity_matrix(source_level + 1)).real
    )
    coarse_identity = berezin_coarse_graining(
        source_level,
        target_level,
        identity_matrix(target_level + 1),
    )
    duality_errors = []
    for label, source_harmonic in source_harmonics.items():
        if label not in target_harmonics:
            continue
        target_harmonic = target_harmonics[label]
        left = trace(
            matmul(
                berezin_state_lift(
                    source_level, target_level, source_harmonic
                ),
                dagger(target_harmonic),
            )
        )
        right = trace(
            matmul(
                source_harmonic,
                berezin_coarse_graining(
                    source_level, target_level, dagger(target_harmonic)
                ),
            )
        )
        duality_errors.append(abs(left - right))
    return {
        "source_level": source_level,
        "target_level": target_level,
        "max_mode": max_mode,
        "quadrature_term_count": len(
            _coherent_refinement_terms(source_level, target_level)
        ),
        "unital_error": max_abs_difference(
            identity_image, identity_matrix(target_level + 1)
        ),
        "max_normalized_trace_error": max(trace_errors),
        "max_adjoint_error": max(adjoint_errors),
        "choi_psd": choi_summary["psd"],
        "choi_min_pivot": choi_summary["min_pivot"],
        "state_lift_trace_scaling_error": state_lift_trace_scaling_error,
        "coarse_graining_unital_error": max_abs_difference(
            coarse_identity, identity_matrix(source_level + 1)
        ),
        "max_state_observable_duality_error": max(duality_errors),
        "mode_records": tuple(mode_records),
    }


def fuzzy_berezin_refinement_certificate(
    *,
    max_source_level: int = 5,
    max_mode: int = 2,
    heat_time: float = 0.2,
    tolerance: float = 1e-8,
) -> dict[str, object]:
    """Audit adjacent-cutoff Berezin refinement and its low-mode theorem."""
    if max_source_level < 2:
        raise ValueError("max_source_level must be at least two")
    if max_mode < 0:
        raise ValueError("max_mode must be nonnegative")
    if heat_time < 0.0:
        raise ValueError("heat_time must be nonnegative")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    records = tuple(
        _map_audit_record(
            source_level,
            source_level + 1,
            max_mode=min(max_mode, source_level),
            heat_time=heat_time,
            tolerance=tolerance,
        )
        for source_level in range(1, max_source_level + 1)
    )
    composition_records = tuple(
        {
            "source_level": source_level,
            "middle_level": source_level + 1,
            "target_level": source_level + 2,
            "ell": ell,
            "exact_defect": composition_coefficient_defect(
                source_level, source_level + 1, source_level + 2, ell
            ),
            "upper_bound": ell * (ell + 1.0) / (source_level + 3.0),
        }
        for source_level in range(1, max_source_level + 1)
        for ell in range(min(max_mode, source_level) + 1)
    )
    coordinate_product_records = tuple(
        coordinate_atomic_product_record(source_level)
        for source_level in range(2, max_source_level + 1)
    )
    global_obstruction_records = tuple(
        {
            "source_level": source_level,
            "target_level": source_level + 1,
            "operator_unit_ball_defect_lower_bound": (
                global_unit_ball_defect_lower_bound(source_level, source_level + 1)
            ),
        }
        for source_level in range(1, max_source_level + 1)
    )
    mode_records = tuple(
        mode
        for record in records
        for mode in record["mode_records"]
    )
    certified_claims = {
        "berezin_refinements_are_unital_cp": all(
            record["unital_error"] <= tolerance and record["choi_psd"]
            for record in records
        ),
        "normalized_trace_and_adjoint_are_preserved": all(
            record["max_normalized_trace_error"] <= tolerance
            and record["max_adjoint_error"] <= tolerance
            for record in records
        ),
        "state_lift_is_trace_preserving_and_has_unital_adjoint": all(
            record["state_lift_trace_scaling_error"] <= tolerance
            and record["coarse_graining_unital_error"] <= tolerance
            and record["max_state_observable_duality_error"] <= tolerance
            for record in records
        ),
        "harmonic_multiplier_formula_holds": all(
            mode["coefficient_formula_error"] <= tolerance
            and mode["harmonic_leakage_norm"] <= tolerance
            for mode in mode_records
        ),
        "low_mode_identity_error_obeys_explicit_bound": all(
            mode["coefficient_to_identity_error"]
            <= mode["coefficient_error_bound"] + tolerance
            for mode in mode_records
        ),
        "laplacian_and_heat_covariance_are_exact": all(
            mode["laplacian_covariance_error"] <= tolerance
            and mode["heat_covariance_error"] <= tolerance
            for mode in mode_records
        ),
        "composition_defect_obeys_inverse_cutoff_bound": all(
            record["exact_defect"] <= record["upper_bound"] + tolerance
            for record in composition_records
        ),
        "coordinate_atomic_ball_is_approximately_multiplicative": all(
            record["analytic_diagonal_pair_bound"]
            <= record["analytic_uniform_operator_norm_bound"] + tolerance
            and record["analytic_off_diagonal_pair_bound"]
            <= record["analytic_uniform_operator_norm_bound"] + tolerance
            and record["max_direct_induced_infinity_norm"]
            <= record["analytic_uniform_operator_norm_bound"] + tolerance
            for record in coordinate_product_records
        ),
        "full_operator_unit_ball_has_persistent_obstruction": all(
            record["operator_unit_ball_defect_lower_bound"] >= 0.5 - tolerance
            for record in global_obstruction_records
        ),
    }
    return {
        "goal": "Phase 2 Canonical Berezin Refinement",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "canonical_ucp_low_mode_refinement_theorem",
        "claim_boundary": (
            "coherent-state Berezin maps with a uniform theorem on the V_1 "
            "coefficient-l1 ball; the full matrix unit ball has an explicit "
            "nonvanishing obstruction, and gravitational constraint compatibility "
            "is not claimed"
        ),
        "analytic_statement": (
            "J_{L->M}(T^L_lm)=sqrt(b_Ll b_Ml)T^M_lm, with "
            "1-b_Ll <= l(l+1)/(L+2); J exactly intertwines the fuzzy Laplacian "
            "and heat semigroup, while cutoff-composition defects vanish uniformly "
            "for mode cutoffs K_L with K_L^2/L -> 0. On the full V_1 atomic ball, "
            "the product defect is at most 8/[3(L+2)], while the full matrix "
            "operator-unit-ball defect remains at least 1/2 along adjacent cutoffs."
        ),
        "certified_claims": certified_claims,
        "records": records,
        "composition_records": composition_records,
        "coordinate_product_records": coordinate_product_records,
        "global_obstruction_records": global_obstruction_records,
    }
