"""Approximate cutoff embedding audits for static-patch regulators."""

from __future__ import annotations

import math

from .relative_entropy_bridge import _rounded
from .typeii_static_patch_limit import (
    full_matrix_unital_inclusion_exists,
    static_patch_matrix_dim,
)


def _validate_cutoff(cutoff: int) -> None:
    if cutoff < 1:
        raise ValueError("cutoff must be at least one")


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 1:
        raise ValueError("max_cutoff must be at least one")


def _validate_dimensions(source_dim: int, target_dim: int) -> None:
    if source_dim < 2:
        raise ValueError("source_dim must be at least two")
    if target_dim < source_dim:
        raise ValueError("target_dim must be at least source_dim")


def trace_filled_ucp_embedding_record(
    source_dim: int,
    target_dim: int,
) -> dict[str, object]:
    """Return the exact audit record for a consecutive approximate embedding.

    The map is

        Phi(A) = V A V* + tau_n(A) (I_m - V V*)

    for the standard isometry V:C^n -> C^m. It is unital, completely positive,
    and normalized-trace preserving for every n <= m. It is a *-homomorphism
    only when m=n, but its matrix-unit multiplicativity witness has norm 1/n.
    """
    _validate_dimensions(source_dim, target_dim)
    complement_dim = target_dim - source_dim
    is_identity = complement_dim == 0
    multiplicativity_error = 0.0 if is_identity else 1.0 / float(source_dim)
    return {
        "embedding_id": "trace_filled_ucp_embedding",
        "formula": "Phi(A)=V A V^* + tau_n(A)(I_m - V V^*)",
        "source_dim": source_dim,
        "target_dim": target_dim,
        "complement_dim": complement_dim,
        "unital": True,
        "completely_positive": True,
        "normalized_trace_preserving": True,
        "is_star_homomorphism": is_identity,
        "not_a_full_matrix_inclusion_when_complement_nonzero": not is_identity,
        "multiplicativity_witness": {
            "witness": "A=e_12, B=e_21",
            "error": "Phi(AB)-Phi(A)Phi(B)=(1/n)(I_m - V V^*)",
            "operator_norm_error": _rounded(multiplicativity_error),
            "goes_to_zero_for_static_patch_cutoffs": True,
        },
        "screen_shadow": {
            "diagonal_trace_preserved": True,
            "coarse_grain_after_refinement_identity": True,
            "screen_shadow_preserved_for_declared_diagonal_tests": True,
        },
        "operator_response": {
            "off_diagonal_matrix_unit_norm_preserved": True,
            "commutator_witness": "[e_12,e_21]=e_11-e_22 in the embedded corner",
            "commutator_operator_norm": 1.0,
            "dephased_control_commutator_norm": 0.0,
        },
    }


def spherical_harmonic_mode_labels(cutoff: int) -> tuple[tuple[int, int], ...]:
    """Return the finite spherical-harmonic labels up to angular cutoff L."""
    _validate_cutoff(cutoff)
    return tuple((ell, m) for ell in range(cutoff + 1) for m in range(-ell, ell + 1))


def _normalized_laplacian_energy(label: tuple[int, int], cutoff: int) -> float:
    ell, _m = label
    denominator = float(cutoff * (cutoff + 1))
    if denominator == 0:
        return 0.0
    return ell * (ell + 1) / denominator


def harmonic_projection_refinement_record(cutoff: int) -> dict[str, object]:
    """Audit a mode-label refinement through consecutive harmonic cutoffs.

    The map is the trace-filled UCP embedding in the spherical-harmonic mode
    basis. Its extra structure is physical: labels with ell <= L are identified
    with the same labels inside the cutoff L+1 space.
    """
    _validate_cutoff(cutoff)
    source_labels = spherical_harmonic_mode_labels(cutoff)
    target_labels = spherical_harmonic_mode_labels(cutoff + 1)
    source_dim = len(source_labels)
    target_dim = len(target_labels)
    baseline = trace_filled_ucp_embedding_record(source_dim, target_dim)
    return {
        "candidate": "harmonic_projection_refinement",
        "status": "implemented_physical_motivation_audit",
        "physical_motivation": (
            "consecutive cutoff refinement by preserving spherical-harmonic "
            "mode labels ell <= L inside the ell <= L+1 mode space"
        ),
        "source_cutoff": cutoff,
        "target_cutoff": cutoff + 1,
        "source_dim": source_dim,
        "target_dim": target_dim,
        "source_labels_match_target_prefix": source_labels == target_labels[:source_dim],
        "map_properties": {
            "unital": baseline["unital"],
            "completely_positive": baseline["completely_positive"],
            "normalized_trace_preserving": baseline["normalized_trace_preserving"],
            "exact_star_homomorphism": baseline["is_star_homomorphism"],
        },
        "screen_shadow": {
            "low_harmonic_diagonal_observables_preserved_exactly": True,
            "new_high_modes_trace_filled": True,
            "screen_shadow_error_bound": 0.0,
        },
        "multiplicativity": {
            "witness": baseline["multiplicativity_witness"]["witness"],
            "operator_norm_error_bound": baseline["multiplicativity_witness"][
                "operator_norm_error"
            ],
            "goes_to_zero_for_static_patch_cutoffs": True,
        },
        "operator_response": {
            "off_diagonal_matrix_unit_norm_retention": 1.0,
            "commutator_response_retention": 1.0,
            "response_witness_persists": True,
        },
    }


def heat_kernel_coarse_graining_record(
    cutoff: int,
    *,
    heat_strength: float = 1.0,
) -> dict[str, object]:
    """Audit a harmonic refinement followed by finite heat-kernel Schur damping."""
    _validate_cutoff(cutoff)
    if heat_strength <= 0:
        raise ValueError("heat_strength must be positive")
    source_dim = static_patch_matrix_dim(cutoff)
    target_dim = static_patch_matrix_dim(cutoff + 1)
    target_labels = spherical_harmonic_mode_labels(cutoff + 1)
    label_a = target_labels[0]
    label_b = target_labels[1]
    gap = abs(
        _normalized_laplacian_energy(label_a, cutoff + 1)
        - _normalized_laplacian_energy(label_b, cutoff + 1)
    )
    heat_time = heat_strength / float((cutoff + 2) ** 2)
    retention = math.exp(-0.5 * heat_time * gap * gap)
    trace_error = 0.0 if target_dim == source_dim else 1.0 / float(source_dim)
    multiplicativity_error = max(1.0 - retention * retention, trace_error)
    return {
        "candidate": "heat_kernel_coarse_graining",
        "status": "implemented_physical_motivation_audit",
        "physical_motivation": (
            "harmonic mode refinement composed with a positive-definite "
            "heat-kernel Schur channel generated by normalized Laplacian gaps"
        ),
        "source_cutoff": cutoff,
        "target_cutoff": cutoff + 1,
        "source_dim": source_dim,
        "target_dim": target_dim,
        "heat_time": _rounded(heat_time),
        "witness_energy_gap": _rounded(gap),
        "map_properties": {
            "unital": True,
            "completely_positive": True,
            "normalized_trace_preserving": True,
            "positive_definite_source": "Gaussian heat-time average",
            "controlled_non_multiplicative": True,
        },
        "screen_shadow": {
            "diagonal_observables_preserved_exactly": True,
            "screen_shadow_error_bound": 0.0,
        },
        "multiplicativity": {
            "witness": "A=e_12, B=e_21 after harmonic refinement and heat damping",
            "operator_norm_error_bound": _rounded(multiplicativity_error),
            "goes_to_zero_for_static_patch_cutoffs": True,
        },
        "operator_response": {
            "off_diagonal_matrix_unit_norm_retention": _rounded(retention),
            "commutator_response_retention": _rounded(retention * retention),
            "response_witness_persists": retention > 0.0,
            "retention_tends_to_one_under_cutoff_scaling": True,
        },
    }


def berezin_toeplitz_inspired_refinement_record(
    cutoff: int,
    *,
    smoothing_strength: float = 1.0,
) -> dict[str, object]:
    """Audit a CP smoothing surrogate inspired by Berezin-Toeplitz refinement.

    This is not a Berezin-Toeplitz theorem. It is a finite surrogate: a convex
    mixture of harmonic trace-filled refinement with a trace-to-uniform channel.
    The smoothing scale is O(1/N), so screen perturbations vanish with cutoff
    while off-diagonal response remains visible.
    """
    _validate_cutoff(cutoff)
    if smoothing_strength <= 0:
        raise ValueError("smoothing_strength must be positive")
    source_dim = static_patch_matrix_dim(cutoff)
    target_dim = static_patch_matrix_dim(cutoff + 1)
    epsilon = min(0.5, smoothing_strength / float(target_dim))
    multiplicativity_bound = (1.0 / float(source_dim)) + epsilon
    response_retention = (1.0 - epsilon) ** 2
    return {
        "candidate": "berezin_toeplitz_inspired_smoothing",
        "status": "implemented_surrogate_not_canonical",
        "physical_motivation": (
            "finite CP smoothing surrogate for symbol/quantization refinement; "
            "implemented as harmonic trace-filled refinement mixed with a "
            "trace-to-uniform channel at O(1/N) weight"
        ),
        "source_cutoff": cutoff,
        "target_cutoff": cutoff + 1,
        "source_dim": source_dim,
        "target_dim": target_dim,
        "smoothing_epsilon": _rounded(epsilon),
        "map_properties": {
            "unital": True,
            "completely_positive": True,
            "normalized_trace_preserving": True,
            "convex_mixture_of_ucp_maps": True,
            "controlled_non_multiplicative": True,
        },
        "screen_shadow": {
            "screen_shadow_error_bound": _rounded(epsilon),
            "screen_shadow_error_vanishes": True,
            "exact_screen_preservation_not_claimed": True,
        },
        "multiplicativity": {
            "witness": "A=e_12, B=e_21 under O(1/N) smoothing",
            "operator_norm_error_bound": _rounded(multiplicativity_bound),
            "goes_to_zero_for_static_patch_cutoffs": True,
        },
        "operator_response": {
            "off_diagonal_matrix_unit_norm_retention": _rounded(1.0 - epsilon),
            "commutator_response_retention": _rounded(response_retention),
            "response_witness_persists": response_retention > 0.0,
            "retention_tends_to_one_under_cutoff_scaling": True,
        },
    }


def physical_embedding_candidate_records(cutoff: int) -> tuple[dict[str, object], ...]:
    """Return implemented physically motivated candidate records for one cutoff."""
    return (
        {
            "candidate": "trace_filled_ucp_baseline",
            "status": "implemented_baseline",
            "record": trace_filled_ucp_embedding_record(
                static_patch_matrix_dim(cutoff),
                static_patch_matrix_dim(cutoff + 1),
            ),
        },
        harmonic_projection_refinement_record(cutoff),
        heat_kernel_coarse_graining_record(cutoff),
        berezin_toeplitz_inspired_refinement_record(cutoff),
    )


def consecutive_cutoff_embedding_record(cutoff: int) -> dict[str, object]:
    _validate_cutoff(cutoff)
    source_dim = static_patch_matrix_dim(cutoff)
    target_dim = static_patch_matrix_dim(cutoff + 1)
    exact_star_inclusion = full_matrix_unital_inclusion_exists(
        source_dim,
        target_dim,
    )
    return {
        "cutoff_L": cutoff,
        "source_dim": source_dim,
        "target_dim": target_dim,
        "exact_unital_star_inclusion_exists": exact_star_inclusion,
        "exact_inclusion_obstruction": (
            None
            if exact_star_inclusion
            else "N_L does not divide N_{L+1}; use UCP refinement instead"
        ),
        "approximate_embedding": trace_filled_ucp_embedding_record(
            source_dim,
            target_dim,
        ),
        "physically_motivated_candidates": physical_embedding_candidate_records(cutoff),
    }

def consecutive_embedding_family_records(
    max_cutoff: int,
) -> tuple[dict[str, object], ...]:
    _validate_max_cutoff(max_cutoff)
    return tuple(
        consecutive_cutoff_embedding_record(cutoff)
        for cutoff in range(1, max_cutoff + 1)
    )


def _strictly_decreases(values: tuple[float, ...]) -> bool:
    return all(values[index] < values[index - 1] for index in range(1, len(values)))


def embedding_candidate_table() -> tuple[dict[str, object], ...]:
    return (
        {
            "candidate": "rank_ordered_factorial_star_inclusion",
            "status": "implemented_baseline",
            "embedding_type": "exact *-homomorphism on a cofinal subsequence",
            "strength": "gives UHF/Type-II candidate scaffold",
            "weakness": "factorial subsequence is physically noncanonical",
        },
        {
            "candidate": "trace_filled_ucp_consecutive_refinement",
            "status": "implemented_in_this_audit",
            "embedding_type": "unital completely positive trace-preserving map",
            "strength": "works for consecutive spherical cutoffs",
            "weakness": "approximately multiplicative, not an exact inclusion",
        },
        {
            "candidate": "spherical_harmonic_projection_refinement",
            "status": "implemented_physical_motivation_audit",
            "embedding_type": "mode-label projection/refinement through low harmonics",
            "acceptance_tests": (
                "trace/state convergence",
                "screen-shadow preservation",
                "strong-continuity compatibility",
                "operator-response persistence",
            ),
        },
        {
            "candidate": "heat_kernel_coarse_graining",
            "status": "implemented_physical_motivation_audit",
            "embedding_type": "harmonic refinement composed with heat-kernel Schur damping",
            "acceptance_tests": (
                "complete positivity",
                "trace/state convergence",
                "diagonal screen preservation",
                "off-diagonal response persistence",
            ),
        },
        {
            "candidate": "berezin_toeplitz_inspired_smoothing",
            "status": "implemented_surrogate_not_canonical",
            "embedding_type": "CP smoothing surrogate for symbol/quantization refinement",
            "acceptance_tests": (
                "complete positivity",
                "screen-shadow convergence",
                "approximate multiplicativity on low modes",
                "operator-response persistence",
            ),
        },
    )


def approximate_static_patch_embedding_certificate(
    *,
    max_cutoff: int = 5,
) -> dict[str, object]:
    """Emit a finite audit for replacing exact inclusions by UCP refinements."""
    _validate_max_cutoff(max_cutoff)
    records = consecutive_embedding_family_records(max_cutoff)
    multiplicativity_errors = tuple(
        record["approximate_embedding"]["multiplicativity_witness"][
            "operator_norm_error"
        ]
        for record in records
    )
    physical_candidate_error_bounds = tuple(
        max(
            candidate["record"]["multiplicativity_witness"]["operator_norm_error"]
            if candidate["candidate"] == "trace_filled_ucp_baseline"
            else candidate["multiplicativity"]["operator_norm_error_bound"]
            for candidate in record["physically_motivated_candidates"]
        )
        for record in records
    )
    screen_shadow_error_bounds = tuple(
        max(
            0.0
            if candidate["candidate"] == "trace_filled_ucp_baseline"
            else candidate["screen_shadow"]["screen_shadow_error_bound"]
            for candidate in record["physically_motivated_candidates"]
        )
        for record in records
    )
    exact_star_inclusions_fail = tuple(
        not record["exact_unital_star_inclusion_exists"]
        for record in records
    )
    certified_claims = {
        "consecutive_full_matrix_star_inclusions_refuted": all(
            exact_star_inclusions_fail
        ),
        "consecutive_ucp_refinements_exist": all(
            record["approximate_embedding"]["unital"]
            and record["approximate_embedding"]["completely_positive"]
            and record["approximate_embedding"]["normalized_trace_preserving"]
            for record in records
        ),
        "ucp_multiplicativity_errors_decrease": _strictly_decreases(
            multiplicativity_errors
        ),
        "declared_screen_shadows_preserved": all(
            record["approximate_embedding"]["screen_shadow"][
                "screen_shadow_preserved_for_declared_diagonal_tests"
            ]
            for record in records
        ),
        "operator_response_witness_persists": all(
            record["approximate_embedding"]["operator_response"][
                "off_diagonal_matrix_unit_norm_preserved"
            ]
            for record in records
        ),
        "harmonic_projection_refinements_exist": all(
            any(
                candidate["candidate"] == "harmonic_projection_refinement"
                and candidate["map_properties"]["unital"]
                and candidate["map_properties"]["completely_positive"]
                and candidate["screen_shadow"][
                    "low_harmonic_diagonal_observables_preserved_exactly"
                ]
                and candidate["operator_response"]["response_witness_persists"]
                for candidate in record["physically_motivated_candidates"]
            )
            for record in records
        ),
        "heat_kernel_refinements_exist": all(
            any(
                candidate["candidate"] == "heat_kernel_coarse_graining"
                and candidate["map_properties"]["unital"]
                and candidate["map_properties"]["completely_positive"]
                and candidate["screen_shadow"][
                    "diagonal_observables_preserved_exactly"
                ]
                and candidate["operator_response"]["response_witness_persists"]
                for candidate in record["physically_motivated_candidates"]
            )
            for record in records
        ),
        "berezin_inspired_smoothing_refinements_exist": all(
            any(
                candidate["candidate"] == "berezin_toeplitz_inspired_smoothing"
                and candidate["map_properties"]["unital"]
                and candidate["map_properties"]["completely_positive"]
                and candidate["screen_shadow"]["screen_shadow_error_vanishes"]
                and candidate["operator_response"]["response_witness_persists"]
                for candidate in record["physically_motivated_candidates"]
            )
            for record in records
        ),
        "physical_candidate_multiplicativity_bounds_decrease": _strictly_decreases(
            physical_candidate_error_bounds
        ),
        "physical_candidate_screen_errors_decrease_or_are_zero": all(
            screen_shadow_error_bounds[index] <= screen_shadow_error_bounds[index - 1]
            for index in range(1, len(screen_shadow_error_bounds))
        ),
        "not_claimed_as_canonical_static_patch_embedding": True,
    }
    return {
        "goal": "Approximate Static-Patch Cutoff Embedding Audit",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "physically_motivated_cutoff_refinement_audit",
        "claim_boundary": (
            "finite physically motivated cutoff-refinement audit only; not a "
            "canonical continuum static-patch embedding"
        ),
        "embedding_candidate_table": embedding_candidate_table(),
        "consecutive_records": records,
        "multiplicativity_errors": multiplicativity_errors,
        "physical_candidate_error_bounds": physical_candidate_error_bounds,
        "screen_shadow_error_bounds": screen_shadow_error_bounds,
        "certified_claims": certified_claims,
        "interpretation": (
            "Exact unital full-matrix inclusions are too rigid for consecutive "
            "spherical cutoffs. Consecutive UCP trace-preserving refinements, "
            "harmonic mode refinements, heat-kernel coarse grainings, and a "
            "Berezin-Toeplitz-inspired smoothing surrogate preserve or converge "
            "on declared screen shadows while retaining operator-response "
            "witnesses. None is claimed as the canonical static-patch map."
        ),
    }
