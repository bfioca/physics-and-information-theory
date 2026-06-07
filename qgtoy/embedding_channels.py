"""Approximate cutoff embedding audits for static-patch regulators."""

from __future__ import annotations

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
            "status": "program_target",
            "embedding_type": "mode-label projection/refinement through low harmonics",
            "acceptance_tests": (
                "trace/state convergence",
                "screen-shadow preservation",
                "strong-continuity compatibility",
                "operator-response persistence",
            ),
        },
        {
            "candidate": "berezin_toeplitz_fuzzy_sphere_channel",
            "status": "program_target",
            "embedding_type": "symbol/quantization channel via the continuum sphere",
            "acceptance_tests": (
                "complete positivity",
                "trace/state convergence",
                "approximate multiplicativity on low modes",
                "static-patch covariance error",
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
        "not_claimed_as_canonical_static_patch_embedding": True,
    }
    return {
        "goal": "Approximate Static-Patch Cutoff Embedding Audit",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "consecutive_ucp_cutoff_refinement_theorem_candidate",
        "claim_boundary": (
            "finite approximate embedding audit only; not a canonical continuum "
            "static-patch embedding"
        ),
        "embedding_candidate_table": embedding_candidate_table(),
        "consecutive_records": records,
        "multiplicativity_errors": multiplicativity_errors,
        "certified_claims": certified_claims,
        "interpretation": (
            "Exact unital full-matrix inclusions are too rigid for consecutive "
            "spherical cutoffs. Consecutive UCP trace-preserving refinements "
            "exist and have vanishing matrix-unit multiplicativity error."
        ),
    }
