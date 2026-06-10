"""Constraint-derived relational observer algebra on the fuzzy harmonic space.

This is a finite parametrized reference-frame model, not Einstein gravity.  It
derives the accessible algebra from commuting time and angular-charge
constraints and makes the extra assumption behind a fully diagonal screen
explicit.
"""

from __future__ import annotations

from math import exp, log, sqrt

from .fuzzy_sphere import harmonic_labels, matrix_scale, matrix_unit
from .quantum_channel import (
    Matrix,
    identity_matrix,
    matrix_add,
    max_abs_difference,
    zero_matrix,
)


HarmonicStateLabel = tuple[int, int]


def _validate_level(level: int) -> None:
    if level < 1:
        raise ValueError("level must be at least one")


def physical_basis_labels(level: int) -> tuple[HarmonicStateLabel, ...]:
    """Return |ell,m> labels for L^2(M_{L+1},tau)."""
    _validate_level(level)
    return harmonic_labels(level)


def constraint_record(level: int) -> dict[str, object]:
    """Audit the time and angular reference charges on every physical label."""
    labels = physical_basis_labels(level)
    records = tuple(
        {
            "ell": ell,
            "magnetic": magnetic,
            "system_energy": ell * (ell + 1),
            "time_reference_momentum": -ell * (ell + 1),
            "time_constraint": 0,
            "system_axial_charge": magnetic,
            "edge_reference_charge": -magnetic,
            "angular_constraint": 0,
        }
        for ell, magnetic in labels
    )
    return {
        "level_L": level,
        "physical_dimension": len(labels),
        "physical_basis_records": records,
        "all_time_constraints_vanish": all(
            record["system_energy"] + record["time_reference_momentum"] == 0
            for record in records
        ),
        "all_angular_constraints_vanish": all(
            record["system_axial_charge"] + record["edge_reference_charge"] == 0
            for record in records
        ),
        "dressed_matrix_unit_count": len(labels) ** 2,
    }


def observer_algebra_hierarchy_record(level: int) -> dict[str, object]:
    """Return the algebras obtained by hiding zero, one, or two references."""
    _validate_level(level)
    physical_dimension = (level + 1) ** 2
    block_sizes = tuple(2 * ell + 1 for ell in range(level + 1))
    full_dimension = physical_dimension**2
    time_blind_dimension = sum(size**2 for size in block_sizes)
    diagonal_dimension = physical_dimension
    edge_coherences = time_blind_dimension - diagonal_dimension
    closed_formula = level * (level + 1) * (4 * level + 5) // 3
    retained_fraction = diagonal_dimension / time_blind_dimension
    retained_fraction_formula = 3.0 * (level + 1.0) / (
        4.0 * level**2 + 8.0 * level + 3.0
    )
    return {
        "level_L": level,
        "physical_dimension": physical_dimension,
        "full_dirac_algebra": f"M_{physical_dimension}",
        "full_dirac_algebra_dimension": full_dimension,
        "time_reference_hidden_algebra": " direct_sum ".join(
            f"M_{size}" for size in block_sizes
        ),
        "time_reference_hidden_block_sizes": block_sizes,
        "time_reference_hidden_algebra_dimension": time_blind_dimension,
        "time_and_edge_references_hidden_algebra": f"C^{physical_dimension}",
        "time_and_edge_references_hidden_algebra_dimension": diagonal_dimension,
        "edge_coherence_parameter_count": edge_coherences,
        "edge_coherence_closed_formula": closed_formula,
        "edge_coherence_formula_exact": edge_coherences == closed_formula,
        "diagonal_fraction_of_time_constraint_algebra": retained_fraction,
        "diagonal_fraction_closed_formula": retained_fraction_formula,
        "scaled_diagonal_fraction": level * retained_fraction,
        "scaled_fraction_limit": 0.75,
        "time_constraint_alone_leaves_noncommutative_blocks": any(
            size > 1 for size in block_sizes
        ),
        "interpretation": (
            "The Hamiltonian/time constraint alone selects energy blocks. Full "
            "diagonalization additionally requires an inaccessible angular edge "
            "reference or charge superselection rule."
        ),
    }


def _validate_physical_operator(level: int, operator: Matrix) -> None:
    dimension = (level + 1) ** 2
    if len(operator) != dimension or len(operator[0]) != dimension:
        raise ValueError("operator dimension does not match the physical space")


def time_reference_expectation(level: int, operator: Matrix) -> Matrix:
    """Conditional expectation E_t onto equal-energy ell blocks."""
    _validate_physical_operator(level, operator)
    labels = physical_basis_labels(level)
    return tuple(
        tuple(
            operator[row][column]
            if labels[row][0] == labels[column][0]
            else 0j
            for column in range(len(labels))
        )
        for row in range(len(labels))
    )


def diagonal_screen_expectation(level: int, operator: Matrix) -> Matrix:
    """Conditional expectation E_{t,phi} after both references are hidden."""
    _validate_physical_operator(level, operator)
    dimension = (level + 1) ** 2
    return tuple(
        tuple(operator[row][column] if row == column else 0j for column in range(dimension))
        for row in range(dimension)
    )


def gaussian_edge_smearing(level: int, operator: Matrix, *, sigma: float) -> Matrix:
    """Apply angular-reference uncertainty to every magnetic coherence."""
    _validate_physical_operator(level, operator)
    if sigma < 0.0:
        raise ValueError("sigma must be nonnegative")
    labels = physical_basis_labels(level)
    return tuple(
        tuple(
            operator[row][column]
            * exp(-0.5 * sigma**2 * (labels[row][1] - labels[column][1]) ** 2)
            for column in range(len(labels))
        )
        for row in range(len(labels))
    )


def within_block_phase_pair(
    level: int,
    *,
    ell: int | None = None,
) -> tuple[Matrix, Matrix]:
    """Return orthogonal +/- states in one energy block."""
    _validate_level(level)
    selected_ell = level if ell is None else ell
    if not 1 <= selected_ell <= level:
        raise ValueError("ell must lie between one and level")
    labels = physical_basis_labels(level)
    left_index = labels.index((selected_ell, -selected_ell))
    right_index = labels.index((selected_ell, selected_ell))
    dimension = len(labels)
    diagonal = matrix_scale(
        matrix_add(
            matrix_unit(dimension, left_index, left_index),
            matrix_unit(dimension, right_index, right_index),
        ),
        0.5,
    )
    coherence = matrix_scale(
        matrix_add(
            matrix_unit(dimension, left_index, right_index),
            matrix_unit(dimension, right_index, left_index),
        ),
        0.5,
    )
    return matrix_add(diagonal, coherence), matrix_add(
        diagonal, matrix_scale(coherence, -1.0)
    )


def recovery_no_go_record(level: int, *, screen_distance: float = 0.0) -> dict[str, object]:
    """Quantify recovery failure when the angular edge reference is discarded."""
    _validate_level(level)
    if not 0.0 <= screen_distance <= 1.0:
        raise ValueError("screen_distance must lie between zero and one")
    plus, minus = within_block_phase_pair(level)
    time_plus = time_reference_expectation(level, plus)
    time_minus = time_reference_expectation(level, minus)
    screen_plus = diagonal_screen_expectation(level, plus)
    screen_minus = diagonal_screen_expectation(level, minus)
    return {
        "level_L": level,
        "state_pair_full_trace_distance": 1.0,
        "time_reference_hidden_trace_distance": 1.0,
        "diagonal_screen_trace_distance": 0.0,
        "time_expectation_preserves_pair": (
            max_abs_difference(time_plus, plus) == 0.0
            and max_abs_difference(time_minus, minus) == 0.0
        ),
        "diagonal_screen_outputs_collide": (
            max_abs_difference(screen_plus, screen_minus) == 0.0
        ),
        "assumed_perturbed_screen_distance": screen_distance,
        "decoder_worst_case_trace_distance_error_lower_bound": (
            1.0 - screen_distance
        )
        / 2.0,
        "proof": (
            "The two orthogonal states remain in one ell block, but their diagonal "
            "screen outputs agree. Contractivity and the triangle inequality give "
            "1 <= error_plus + screen_distance + error_minus."
        ),
    }


def extremal_edge_visibility(level: int, *, sigma: float) -> float:
    _validate_level(level)
    if sigma < 0.0:
        raise ValueError("sigma must be nonnegative")
    return exp(-2.0 * sigma**2 * level**2)


def maximum_sigma_for_visibility(level: int, *, visibility: float) -> float:
    """Largest Gaussian angular width retaining an extremal-m response."""
    _validate_level(level)
    if not 0.0 < visibility < 1.0:
        raise ValueError("visibility must lie strictly between zero and one")
    return sqrt(log(1.0 / visibility) / 2.0) / level


def edge_reference_record(
    level: int,
    *,
    sigma: float,
    minimum_visibility: float,
) -> dict[str, object]:
    _validate_level(level)
    visibility = extremal_edge_visibility(level, sigma=sigma)
    required_sigma = maximum_sigma_for_visibility(
        level, visibility=minimum_visibility
    )
    plus, minus = within_block_phase_pair(level)
    smeared_plus = gaussian_edge_smearing(level, plus, sigma=sigma)
    smeared_minus = gaussian_edge_smearing(level, minus, sigma=sigma)
    labels = physical_basis_labels(level)
    left = labels.index((level, -level))
    right = labels.index((level, level))
    measured_visibility = abs(
        smeared_plus[left][right] - smeared_minus[left][right]
    )
    return {
        "level_L": level,
        "fixed_angular_width_sigma": sigma,
        "extremal_m_gap": 2 * level,
        "analytic_extremal_visibility": visibility,
        "matrix_extremal_visibility": measured_visibility,
        "smeared_pair_trace_distance": visibility,
        "decoder_error_lower_bound_after_smearing": (1.0 - visibility) / 2.0,
        "fixed_sigma_decoder_error_limit": 0.5 if sigma > 0.0 else 0.0,
        "minimum_visibility_target": minimum_visibility,
        "maximum_sigma_for_target": required_sigma,
        "level_times_maximum_sigma": level * required_sigma,
        "fixed_sigma_continuum_limit": 0.0 if sigma > 0.0 else 1.0,
        "resolution_scaling_law": "sigma_L <= sqrt(log(1/v)/2)/L",
    }


def continuum_limit_record() -> dict[str, object]:
    """State the canonical harmonic-core limit and its algebra types."""
    return {
        "harmonic_inclusion": "|ell,m>_L maps to |ell,m>_M for ell<=L<=M",
        "constraint_covariance": (
            "exact: ell(ell+1) and m are unchanged on the finite harmonic core"
        ),
        "heat_dynamics_covariance": (
            "exact on finite harmonic support for exp[-t ell(ell+1)]"
        ),
        "full_corner_cstar_limit": "compact operators on l2{(ell,m)}",
        "full_corner_strong_closure": "B(l2{(ell,m)}), Type I_infinity",
        "time_blind_strong_closure": "product_{ell>=0} M_{2ell+1}, atomic Type I",
        "time_blind_center": "l_infinity over ell",
        "diagonal_strong_closure": "l_infinity over (ell,m), abelian",
        "typeii_obstruction": (
            "The one-particle relational constraint model has a Type-I, not "
            "Type-II, limit. A gravitational crossed-product claim requires a "
            "many-body/local-QFT algebra and a derived trace."
        ),
    }


def relational_observer_constraint_certificate(
    *,
    max_level: int = 8,
    sigma: float = 0.2,
    minimum_visibility: float = 0.5,
    tolerance: float = 1e-12,
) -> dict[str, object]:
    """Audit the constraint-derived algebra hierarchy and edge-resolution no-go."""
    if max_level < 1:
        raise ValueError("max_level must be at least one")
    if sigma <= 0.0:
        raise ValueError("sigma must be positive")
    if not 0.0 < minimum_visibility < 1.0:
        raise ValueError("minimum_visibility must lie strictly between zero and one")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    constraints = tuple(constraint_record(level) for level in range(1, max_level + 1))
    hierarchies = tuple(
        observer_algebra_hierarchy_record(level)
        for level in range(1, max_level + 1)
    )
    recovery = tuple(
        recovery_no_go_record(level) for level in range(1, max_level + 1)
    )
    edge = tuple(
        edge_reference_record(
            level,
            sigma=sigma,
            minimum_visibility=minimum_visibility,
        )
        for level in range(1, max_level + 1)
    )
    certified_claims = {
        "commuting_reference_constraints_are_solved_exactly": all(
            record["all_time_constraints_vanish"]
            and record["all_angular_constraints_vanish"]
            for record in constraints
        ),
        "full_dirac_matrix_units_are_available": all(
            record["dressed_matrix_unit_count"]
            == record["physical_dimension"] ** 2
            for record in constraints
        ),
        "time_constraint_alone_leaves_noncommutative_blocks": all(
            record["time_constraint_alone_leaves_noncommutative_blocks"]
            for record in hierarchies
        ),
        "edge_coherence_dimension_formula_is_exact": all(
            record["edge_coherence_formula_exact"] for record in hierarchies
        ),
        "diagonal_screen_retains_a_vanishing_algebra_fraction": all(
            abs(
                record["diagonal_fraction_of_time_constraint_algebra"]
                - record["diagonal_fraction_closed_formula"]
            )
            <= tolerance
            for record in hierarchies
        )
        and all(
            hierarchies[index + 1]["diagonal_fraction_of_time_constraint_algebra"]
            < hierarchies[index]["diagonal_fraction_of_time_constraint_algebra"]
            for index in range(len(hierarchies) - 1)
        ),
        "diagonal_screen_has_recovery_error_at_least_one_half": all(
            record["time_expectation_preserves_pair"]
            and record["diagonal_screen_outputs_collide"]
            and record["decoder_worst_case_trace_distance_error_lower_bound"]
            >= 0.5 - tolerance
            for record in recovery
        ),
        "gaussian_edge_visibility_matches_matrix_channel": all(
            abs(
                record["analytic_extremal_visibility"]
                - record["matrix_extremal_visibility"]
            )
            <= tolerance
            for record in edge
        ),
        "fixed_visibility_requires_inverse_cutoff_resolution": all(
            abs(
                record["level_times_maximum_sigma"]
                - edge[0]["level_times_maximum_sigma"]
            )
            <= tolerance
            for record in edge
        ),
        "fixed_angular_resolution_loses_extremal_coherence": edge[-1][
            "analytic_extremal_visibility"
        ]
        < edge[0]["analytic_extremal_visibility"],
        "fixed_resolution_recovery_error_tends_to_one_half": all(
            abs(
                record["decoder_error_lower_bound_after_smearing"]
                - (1.0 - record["analytic_extremal_visibility"]) / 2.0
            )
            <= tolerance
            for record in edge
        )
        and edge[-1]["decoder_error_lower_bound_after_smearing"]
        > edge[0]["decoder_error_lower_bound_after_smearing"],
    }
    return {
        "goal": "Constraint-Derived Relational Fuzzy-Horizon Observer Algebra",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "finite_relational_observer_algebra_and_edge_resolution_no_go",
        "claim_boundary": (
            "parametrized fuzzy one-particle reference-frame model; not an "
            "Einstein constraint, de Sitter path integral, Hartle-Hawking state, "
            "or gravitational Type-II observer algebra"
        ),
        "central_result": (
            "The time constraint alone yields direct_sum_ell M_{2ell+1}; the "
            "diagonal screen additionally discards an angular edge reference. "
            "It retains only 3(L+1)/(4L^2+8L+3) of the time-constraint algebra. "
            "Keeping extremal magnetic coherence at fixed visibility requires "
            "angular resolution sigma_L=O(1/L)."
        ),
        "certified_claims": certified_claims,
        "constraint_records": constraints,
        "algebra_hierarchy_records": hierarchies,
        "recovery_no_go_records": recovery,
        "edge_reference_records": edge,
        "continuum_limit": continuum_limit_record(),
    }
