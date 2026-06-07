"""Continuum-lift obstruction schemas for static-patch observer diagnostics."""

from __future__ import annotations

from .embedding_channels import approximate_static_patch_embedding_certificate
from .lift_diagnostics import (
    finite_lift_decision_record,
    response_witness_gap,
    screen_shadow_equal_for_quantum_dephased,
)


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 1:
        raise ValueError("max_cutoff must be at least one")


def continuum_lift_conditions() -> tuple[dict[str, object], ...]:
    return (
        {
            "condition": "embedding_or_coarse_graining_structure",
            "meaning": (
                "finite algebras must be related by exact inclusions or "
                "approximate UCP/coarse-graining maps"
            ),
        },
        {
            "condition": "trace_state_convergence",
            "meaning": "finite normalized traces or states converge under the chosen maps",
        },
        {
            "condition": "screen_shadow_convergence",
            "meaning": "declared screen-visible diagnostics converge through the screen maps",
        },
        {
            "condition": "strong_continuity_or_generator_control",
            "meaning": "finite dynamics obey a continuity gate such as delta_L Gamma_L -> 0",
        },
        {
            "condition": "operator_response_persistence",
            "meaning": "some commutator/off-diagonal response witness has nonzero limit",
        },
        {
            "condition": "observer_algebra_limit_compatibility",
            "meaning": "the limiting algebra interpretation is compatible with the finite maps",
        },
    )


def screen_only_dictionary_obstruction(
    *,
    screen_shadow_distance: float,
    response_witness_gap: float,
) -> dict[str, object]:
    if screen_shadow_distance < 0.0:
        raise ValueError("screen_shadow_distance must be nonnegative")
    if response_witness_gap < 0.0:
        raise ValueError("response_witness_gap must be nonnegative")
    return {
        "assumption": "dictionary_factors_through_screen_shadow",
        "screen_shadow_distance": screen_shadow_distance,
        "response_witness_gap": response_witness_gap,
        "screen_only_dictionary_incomplete": (
            screen_shadow_distance == 0.0 and response_witness_gap > 0.0
        ),
        "reason": (
            "equal screen shadows identify the two sequences for any "
            "screen-factored dictionary, while a nonzero response gap separates "
            "their observer algebras"
        ),
    }


def continuum_lift_obstruction_certificate(
    *,
    max_cutoff: int = 5,
) -> dict[str, object]:
    """Emit the conditional continuum-lift obstruction theorem schema."""
    _validate_max_cutoff(max_cutoff)
    embedding = approximate_static_patch_embedding_certificate(
        max_cutoff=max_cutoff,
    )
    source_dim = embedding["consecutive_records"][0]["source_dim"]
    obstruction = screen_only_dictionary_obstruction(
        screen_shadow_distance=0.0,
        response_witness_gap=response_witness_gap(source_dim),
    )
    decision = finite_lift_decision_record(max_cutoff=max_cutoff)
    errors = embedding["multiplicativity_errors"]
    certified_claims = {
        "lift_conditions_are_explicit": len(continuum_lift_conditions()) == 6,
        "approximate_consecutive_embedding_available": embedding["certified_claims"][
            "consecutive_ucp_refinements_exist"
        ],
        "embedding_errors_decrease": embedding["certified_claims"][
            "ucp_multiplicativity_errors_decrease"
        ],
        "screen_shadow_collision_persists_in_schema": (
            obstruction["screen_shadow_distance"] == 0.0
            and screen_shadow_equal_for_quantum_dephased(source_dim)
        ),
        "operator_response_gap_persists_in_schema": (
            obstruction["response_witness_gap"] > 0.0
        ),
        "screen_only_dictionary_is_incomplete_under_lift_conditions": obstruction[
            "screen_only_dictionary_incomplete"
        ],
        "not_claimed_as_continuum_static_patch_theorem": True,
    }
    return {
        "goal": "Continuum Lift Conditions and Screen-Only Dictionary Obstruction",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "proof_ready_conditional_continuum_lift_obstruction_theorem",
        "claim_boundary": (
            "proof-ready obstruction theorem under explicit lift hypotheses; "
            "it does not construct continuum de Sitter, dS/CFT, or ER=EPR"
        ),
        "lift_conditions": continuum_lift_conditions(),
        "embedding_certificate": embedding,
        "finite_lift_decision_record": decision,
        "screen_only_dictionary_obstruction": obstruction,
        "multiplicativity_error_limit_gate": {
            "errors": errors,
            "bounded_family_decreases": embedding["certified_claims"][
                "ucp_multiplicativity_errors_decrease"
            ],
            "candidate_limit": "0 as cutoff L -> infinity",
        },
        "theorem": (
            "If finite regulator sequences converge under the listed lift "
            "conditions, and if a proposed continuum dictionary factors only "
            "through the limiting screen-shadow data, then that dictionary "
            "cannot determine the observer algebra whenever a response witness "
            "gap persists."
        ),
        "certified_claims": certified_claims,
    }
