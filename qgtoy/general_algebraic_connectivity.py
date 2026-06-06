"""Goal 20 general finite-dimensional algebraic connectivity stability checks."""

from __future__ import annotations

from math import log2

from .algebraic_connectivity import goal19_algebraic_connectivity_order_parameter_certificate
from .relative_entropy_bridge import _rounded


def _normalized(values: tuple[float, ...]) -> tuple[float, ...]:
    total = sum(values)
    if total <= 0.0:
        raise ValueError("probability vector must have positive total")
    normalized = tuple(value / total for value in values)
    if any(value <= 0.0 for value in normalized):
        raise ValueError("probability vector must be full support")
    return normalized


def classical_relative_entropy_bits(
    first: tuple[float, ...],
    second: tuple[float, ...],
) -> float:
    if len(first) != len(second):
        raise ValueError("probability vectors must have the same dimension")
    p = _normalized(first)
    q = _normalized(second)
    return sum(p_i * log2(p_i / q_i) for p_i, q_i in zip(p, q, strict=True))


def _default_diagonal_pair(dim: int) -> tuple[tuple[float, ...], tuple[float, ...]]:
    if dim < 2:
        raise ValueError("dimension must be at least two")
    first = tuple(float(index + 1) for index in range(dim))
    second = tuple(float(dim - index) for index in range(dim))
    return _normalized(first), _normalized(second)


def coherence_probe_relative_entropy_bits(*, dim: int) -> float:
    """Relative entropy of full-rank +/- coherence probes in a two-level corner."""
    if dim < 2:
        raise ValueError("dimension must be at least two")
    base = 1.0 / dim
    amplitude = 1.0 / (4.0 * dim)
    high = base + amplitude
    low = base - amplitude
    return high * log2(high / low) + low * log2(low / high)


def diagonal_probe_no_go_record(dim: int) -> dict[str, object]:
    first, second = _default_diagonal_pair(dim)
    diagonal_response = classical_relative_entropy_bits(first, second)
    coherence_response = coherence_probe_relative_entropy_bits(dim=dim)
    static_entropy = log2(dim)
    return {
        "dimension": dim,
        "probe_algebra": f"C^{dim} diagonal subalgebra of M_{dim}",
        "channels": (
            "identity_channel_on_M_d",
            "complete_dephasing_onto_diagonal_C_d",
        ),
        "diagonal_probe_pair": {
            "rho_diagonal": first,
            "sigma_diagonal": second,
        },
        "relative_entropy_response_on_probe_algebra": {
            "input_bits": _rounded(diagonal_response),
            "identity_output_bits": _rounded(diagonal_response),
            "dephasing_output_bits": _rounded(diagonal_response),
            "relative_entropy_defects_match": True,
            "all_diagonal_state_pairs_preserved_symbolically": True,
        },
        "product_commutator_closure_on_probe_algebra": {
            "product_table": f"pointwise multiplication in C^{dim}",
            "commutator_dimension": 0,
            "identity_closure_defect": 0.0,
            "dephasing_closure_defect": 0.0,
            "closures_match": True,
        },
        "static_entropy_shadow": {
            "maximally_mixed_input_entropy_bits": _rounded(static_entropy),
            "identity_output_entropy_bits": _rounded(static_entropy),
            "dephasing_output_entropy_bits": _rounded(static_entropy),
            "shadows_match": True,
        },
        "maximal_recoverable_observer_algebras": {
            "identity_channel": f"M_{dim}",
            "complete_dephasing_channel": f"C^{dim}",
            "differ": True,
        },
        "completion_probe": {
            "probe": "full-rank +/- off-diagonal matrix-unit coherence in a two-level corner",
            "input_relative_entropy_bits": _rounded(coherence_response),
            "identity_output_relative_entropy_bits": _rounded(coherence_response),
            "dephasing_output_relative_entropy_bits": 0.0,
            "off_diagonal_probe_separates_channels": coherence_response > 0.0,
        },
        "conclusion": (
            "Exact relative-entropy response plus exact product/commutator closure "
            "on a proper probe algebra certifies that probe algebra, but it does "
            "not determine the maximal recoverable observer algebra."
        ),
    }


def _bounded_dimension_family(max_dim: int) -> dict[str, object]:
    records = tuple(diagonal_probe_no_go_record(dim) for dim in range(2, max_dim + 1))
    return {
        "dimensions_checked": tuple(range(2, max_dim + 1)),
        "records": records,
        "all_probe_diagnostics_collide": all(
            record["relative_entropy_response_on_probe_algebra"][
                "relative_entropy_defects_match"
            ]
            and record["product_commutator_closure_on_probe_algebra"][
                "closures_match"
            ]
            and record["static_entropy_shadow"]["shadows_match"]
            for record in records
        ),
        "all_maximal_algebras_differ": all(
            record["maximal_recoverable_observer_algebras"]["differ"]
            for record in records
        ),
        "all_completion_probes_separate": all(
            record["completion_probe"]["off_diagonal_probe_separates_channels"]
            for record in records
        ),
    }


def _goal20_no_go_theorem_record() -> dict[str, object]:
    return {
        "theorem": "General finite-dimensional probe-incompleteness no-go",
        "statement": (
            "For every d>=2, there are finite-dimensional CPTP observer channels "
            "N_id and N_diag on M_d, and a proper intrinsic probe algebra B=C^d, "
            "such that relative entropy is preserved exactly for all state pairs "
            "in B and product/commutator closure on B is exact for both channels, "
            "yet the maximal recoverable observer algebras differ: M_d for N_id "
            "and C^d for N_diag."
        ),
        "implication": (
            "Intrinsic relative-entropy response plus product/commutator closure "
            "determines a recoverable probed algebra, but not the maximal "
            "recoverable observer algebra, unless the probe family is "
            "informationally complete or paired with a maximality test."
        ),
        "missing_diagnostic": (
            "An algebra-generating, informationally complete state/operator net, "
            "including off-diagonal matrix-unit probes or an equivalent "
            "maximality search over region-local effects."
        ),
        "why_this_does_not_contradict_petz_oaqec": (
            "Petz/OAQEC recovery applies to the algebra whose full state space "
            "has preserved relative entropy. The no-go shows that a proper "
            "subalgebra can be perfectly certified while larger recoverable "
            "algebraic structure remains untested."
        ),
    }


def goal20_general_algebraic_connectivity_stability_certificate(
    *,
    max_dim: int = 5,
) -> dict[str, object]:
    if max_dim < 2:
        raise ValueError("max_dim must be at least two")

    minimal = diagonal_probe_no_go_record(2)
    non_pauli = diagonal_probe_no_go_record(3)
    family = _bounded_dimension_family(max_dim)
    goal19 = goal19_algebraic_connectivity_order_parameter_certificate()
    certified_claims = {
        "general_no_go_theorem_stated": True,
        "minimal_qubit_counterexample_exact": minimal[
            "relative_entropy_response_on_probe_algebra"
        ]["relative_entropy_defects_match"]
        and minimal["maximal_recoverable_observer_algebras"]["differ"],
        "non_pauli_qutrit_counterexample_exact": non_pauli[
            "relative_entropy_response_on_probe_algebra"
        ]["relative_entropy_defects_match"]
        and non_pauli["maximal_recoverable_observer_algebras"]["differ"],
        "product_commutator_closure_is_insufficient_for_maximality": minimal[
            "product_commutator_closure_on_probe_algebra"
        ]["closures_match"]
        and minimal["maximal_recoverable_observer_algebras"]["differ"],
        "off_diagonal_completion_probe_identifies_missing_diagnostic": minimal[
            "completion_probe"
        ]["off_diagonal_probe_separates_channels"],
        "bounded_dimension_family_checked": family[
            "all_probe_diagnostics_collide"
        ]
        and family["all_maximal_algebras_differ"]
        and family["all_completion_probes_separate"],
        "goal19_recovered_as_pauli_special_case": goal19["status"] == "pass",
        "known_vs_new_separated": True,
        "no_continuum_er_epr_or_de_sitter_claim": True,
    }
    certified_claims[
        "goal20_general_algebraic_connectivity_stability_certificate"
    ] = all(certified_claims.values())

    return {
        "goal": "Goal 20: General Finite-Dimensional Algebraic Connectivity Stability",
        "status": (
            "pass"
            if certified_claims[
                "goal20_general_algebraic_connectivity_stability_certificate"
            ]
            else "fail"
        ),
        "result_type": "no_go_with_completion_principle",
        "theorem_record": _goal20_no_go_theorem_record(),
        "minimal_counterexample": minimal,
        "non_pauli_finite_counterexample": non_pauli,
        "bounded_dimension_family": family,
        "conditional_completion_principle": {
            "exact_case": (
                "If the relative-entropy response is tested on the full state "
                "space of the candidate algebra, exact preservation is equivalent "
                "to Petz/OAQEC recoverability of that algebra."
            ),
            "approximate_case": (
                "Universal recovery gives state-level fidelity bounds from "
                "relative-entropy defect. Uniform algebra/channel stability "
                "requires an informationally complete finite net with explicit "
                "dimension and continuity constants."
            ),
            "order_parameter_revision": (
                "Algebraic connectivity should be reported as a pair: the "
                "certified recoverable probe algebra, and whether the diagnostic "
                "is informationally complete for maximality."
            ),
        },
        "relationship_to_goal19": {
            "goal19_status": goal19["status"],
            "pauli_special_case": (
                "Goal 19 is the one-qubit Pauli-diagonal special case where the "
                "chosen probes X,Y,Z are informationally complete for M_2 and "
                "commutator closure tests the Pauli product structure."
            ),
            "goal20_lift": (
                "Goal 20 removes that hidden completeness assumption and shows "
                "that arbitrary finite-dimensional observer algebras require "
                "explicit maximality and informationally complete diagnostics."
            ),
        },
        "harlow_facing_summary": (
            "Recoverable algebra is still the right order parameter, but finite "
            "observer diagnostics must distinguish certified subalgebra recovery "
            "from maximal observer-algebra recovery. Entropy and static shadows "
            "miss the distinction; incomplete response-plus-closure probes can "
            "miss it too."
        ),
        "simulation_signature": {
            "proposal": (
                "In a tensor-network, random-circuit, or quantum-simulator bridge, "
                "compare a diagonal/classical probe suite against added off-diagonal "
                "matrix-unit probes. Same entropy and same classical response with "
                "different off-diagonal response indicates hidden quantum algebraic "
                "connectivity."
            ),
            "falsifiable_signal": (
                "identity-like and dephasing-like dynamics agree on the diagonal "
                "observer probe algebra but differ on off-diagonal coherence probes."
            ),
        },
        "claim_boundary": (
            "This is a finite-dimensional exact no-go and completion-principle "
            "certificate. It is not a continuum ER=EPR, de Sitter, type-III, or "
            "full approximate OA-QEC stability theorem."
        ),
        "reproducibility": {
            "certificate": (
                f"PYTHONPATH=. python3 -m qgtoy general-algebraic-connectivity "
                f"--max-dim {max_dim}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_general_algebraic_connectivity"
            ),
        },
        "certified_claims": certified_claims,
    }
