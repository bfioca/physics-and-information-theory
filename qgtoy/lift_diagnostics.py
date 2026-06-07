"""Finite screen-shadow and response witnesses for continuum-lift audits."""

from __future__ import annotations

import math

from .embedding_channels import consecutive_embedding_family_records
from .relative_entropy_bridge import _rounded


def _validate_dimension(dimension: int) -> None:
    if dimension < 2:
        raise ValueError("dimension must be at least two")


def _validate_low_order(low_order: int) -> None:
    if low_order < 0:
        raise ValueError("low_order must be nonnegative")


def _validate_algebra_kind(algebra_kind: str) -> None:
    if algebra_kind not in {"matrix", "abelian"}:
        raise ValueError("algebra_kind must be 'matrix' or 'abelian'")


def declared_screen_shadow_record(
    dimension: int,
    *,
    algebra_kind: str,
    low_order: int = 2,
) -> dict[str, object]:
    """Return the declared finite screen shadow.

    The shadow intentionally contains only diagonal/screen data. The source
    algebra kind is validated but not included in the returned record, because
    a screen-factored dictionary is not allowed to read it.
    """
    _validate_dimension(dimension)
    _validate_low_order(low_order)
    _validate_algebra_kind(algebra_kind)
    diagonal_mass = _rounded(1.0 / float(dimension))
    return {
        "screen_shadow_id": f"diagonal_screen_dim_{dimension}_order_{low_order}",
        "screen_algebra": f"C^{dimension}",
        "screen_dimension": dimension,
        "diagonal_state": tuple(diagonal_mass for _ in range(dimension)),
        "diagonal_observable_orders": tuple(range(1, low_order + 1)),
        "horizon_overlap_count": dimension,
        "screen_restricted_transfer": "diagonal_identity_transfer",
        "allowed_data": (
            "diagonal_observables",
            "low_order_diagonal_correlators",
            "horizon_overlap_data",
            "screen_restricted_transfer_records",
            "certificate_emitted_screen_shadow_fields",
        ),
    }


def screen_shadow_equal_for_quantum_dephased(
    dimension: int,
    *,
    low_order: int = 2,
) -> bool:
    return declared_screen_shadow_record(
        dimension,
        algebra_kind="matrix",
        low_order=low_order,
    ) == declared_screen_shadow_record(
        dimension,
        algebra_kind="abelian",
        low_order=low_order,
    )


def response_witness_record(
    dimension: int,
    *,
    algebra_kind: str,
) -> dict[str, object]:
    """Return a norm-stable finite noncommutativity witness."""
    _validate_dimension(dimension)
    _validate_algebra_kind(algebra_kind)
    if algebra_kind == "abelian":
        return {
            "algebra_kind": "abelian",
            "chosen_topology": "operator_norm",
            "witness": "all commutators vanish in C^N",
            "nu_lower_bound": 0.0,
            "commutator_operator_norm": 0.0,
            "rank_one_trace_l2_norm": 0.0,
            "persists_in_operator_norm": False,
        }
    rank_one_l2 = math.sqrt(2.0 / float(dimension))
    return {
        "algebra_kind": "matrix",
        "chosen_topology": "operator_norm",
        "witness": "a=e_12, b=e_21, [a,b]=e_11-e_22",
        "nu_lower_bound": 1.0,
        "commutator_operator_norm": 1.0,
        "rank_one_trace_l2_norm": _rounded(rank_one_l2),
        "rank_one_l2_warning": (
            "the rank-one trace-L2 witness can vanish with dimension; the "
            "lift theorem uses operator-norm persistence"
        ),
        "persists_in_operator_norm": True,
    }


def response_witness_gap(dimension: int) -> float:
    matrix = response_witness_record(dimension, algebra_kind="matrix")
    abelian = response_witness_record(dimension, algebra_kind="abelian")
    return _rounded(
        float(matrix["nu_lower_bound"]) - float(abelian["nu_lower_bound"])
    )


def _candidate_response_retention(candidate: dict[str, object]) -> float:
    if candidate["candidate"] == "trace_filled_ucp_baseline":
        return float(
            candidate["record"]["operator_response"]["commutator_operator_norm"]
        )
    response = candidate["operator_response"]
    if "commutator_response_retention" in response:
        return float(response["commutator_response_retention"])
    return float(response["off_diagonal_matrix_unit_norm_retention"])


def _candidate_screen_error(candidate: dict[str, object]) -> float:
    if candidate["candidate"] == "trace_filled_ucp_baseline":
        return 0.0
    return float(candidate["screen_shadow"]["screen_shadow_error_bound"])


def embedding_response_witness_records(
    *,
    max_cutoff: int = 5,
) -> tuple[dict[str, object], ...]:
    """Return direct finite witness records for implemented lift maps."""
    records = []
    for cutoff_record in consecutive_embedding_family_records(max_cutoff):
        for candidate in cutoff_record["physically_motivated_candidates"]:
            retention = _candidate_response_retention(candidate)
            screen_error = _candidate_screen_error(candidate)
            records.append(
                {
                    "cutoff_L": cutoff_record["cutoff_L"],
                    "candidate": candidate["candidate"],
                    "response_lower_bound": _rounded(retention),
                    "response_witness_persists": retention > 0.0,
                    "screen_shadow_error_bound": _rounded(screen_error),
                    "screen_shadow_convergent_or_exact": (
                        screen_error == 0.0
                        or bool(
                            candidate["screen_shadow"].get(
                                "screen_shadow_error_vanishes",
                                False,
                            )
                        )
                    )
                    if candidate["candidate"] != "trace_filled_ucp_baseline"
                    else True,
                }
            )
    return tuple(records)


def finite_lift_decision_record(
    *,
    max_cutoff: int = 5,
) -> dict[str, object]:
    """Classify the current branch against the A/B/C execution target."""
    _validate_dimension(max_cutoff + 1)
    witness_records = embedding_response_witness_records(max_cutoff=max_cutoff)
    response_persists = all(
        bool(record["response_witness_persists"]) for record in witness_records
    )
    screen_converges = all(
        bool(record["screen_shadow_convergent_or_exact"])
        for record in witness_records
    )
    conditions = (
        {
            "condition": "screen_shadow_equality",
            "status": "finite_proved",
            "evidence": "declared_screen_shadow_record ignores source algebra after validation",
        },
        {
            "condition": "operator_norm_response_separation",
            "status": "finite_proved",
            "evidence": "nu(M_N)>=1 from e_12/e_21, while nu(C^N)=0",
        },
        {
            "condition": "implemented_lift_map_response_persistence",
            "status": "bounded_certified" if response_persists else "failed",
            "evidence": "embedding_response_witness_records",
        },
        {
            "condition": "implemented_lift_map_screen_convergence",
            "status": "bounded_certified" if screen_converges else "failed",
            "evidence": "embedding_response_witness_records",
        },
        {
            "condition": "canonical_static_patch_embedding",
            "status": "conditional_assumption",
            "evidence": (
                "harmonic, heat-kernel, and Berezin-inspired maps are audited "
                "but not claimed canonical"
            ),
        },
        {
            "condition": "continuum_observer_algebra_compatibility",
            "status": "conditional_assumption",
            "evidence": "requires external operator-algebra/static-patch input",
        },
    )
    failed = tuple(
        condition for condition in conditions if condition["status"] == "failed"
    )
    return {
        "selected_outcome": "A_theorem_candidate" if not failed else "B_no_go",
        "conditions": conditions,
        "failed_conditions": failed,
        "screen_shadow_equal_for_quantum_dephased": screen_shadow_equal_for_quantum_dephased(
            4
        ),
        "response_witness_gap": response_witness_gap(4),
        "minimum_embedding_response_lower_bound": _rounded(
            min(float(record["response_lower_bound"]) for record in witness_records)
        ),
        "finite_requirements_satisfied": (
            not failed
            and screen_shadow_equal_for_quantum_dephased(4)
            and response_witness_gap(4) > 0.0
        ),
        "claim_boundary": (
            "proof-ready obstruction theorem under explicit lift hypotheses; "
            "canonical static-patch realization remains conditional"
        ),
    }
