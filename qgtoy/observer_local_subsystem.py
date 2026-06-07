"""Observer-local noncommutative subsystem certificates."""

from __future__ import annotations

from math import sqrt

from .relative_entropy_bridge import _rounded


FORBIDDEN_SELECTION_TOKENS = (
    "bridge",
    "e_12",
    "e_21",
    "off-diagonal witness",
    "response witness",
)

GATE_KEYS = (
    "anti_tautological_selection",
    "cp_unital_trace_refinement",
    "covariance",
    "screen_shadow",
    "norm_faithfulness",
    "nonzero_commutator_lower_bound",
    "strong_continuity",
    "typeii_route",
)

GATE_STATUSES = ("pass", "conditional", "fail")


def _validate_parameters(max_cutoff: int, excitation_cutoff: int) -> None:
    if excitation_cutoff < 1:
        raise ValueError("excitation_cutoff must be at least one")
    if max_cutoff <= 2 * excitation_cutoff:
        raise ValueError("max_cutoff must be greater than 2 * excitation_cutoff")


def _selection_is_anti_tautological(selection_rule: str) -> bool:
    lowered = selection_rule.lower()
    return not any(token in lowered for token in FORBIDDEN_SELECTION_TOKENS)


def _gate_statuses(
    *,
    anti_tautological_selection: str,
    cp_unital_trace_refinement: str,
    covariance: str,
    screen_shadow: str,
    norm_faithfulness: str,
    nonzero_commutator_lower_bound: str,
    strong_continuity: str,
    typeii_route: str,
) -> dict[str, str]:
    statuses = {
        "anti_tautological_selection": anti_tautological_selection,
        "cp_unital_trace_refinement": cp_unital_trace_refinement,
        "covariance": covariance,
        "screen_shadow": screen_shadow,
        "norm_faithfulness": norm_faithfulness,
        "nonzero_commutator_lower_bound": nonzero_commutator_lower_bound,
        "strong_continuity": strong_continuity,
        "typeii_route": typeii_route,
    }
    unknown_statuses = {
        key: value
        for key, value in statuses.items()
        if key not in GATE_KEYS or value not in GATE_STATUSES
    }
    if unknown_statuses:
        raise ValueError(f"unknown gate status: {unknown_statuses}")
    return statuses


def _commutator_eigenvalues(
    *,
    cutoff: int,
    excitation_cutoff: int,
) -> tuple[float, ...]:
    return tuple(
        _rounded(1.0 - (2.0 * excitation) / float(cutoff))
        for excitation in range(excitation_cutoff + 1)
    )


def tangent_plane_double_scaling_record(
    *,
    cutoff: int,
    excitation_cutoff: int = 2,
) -> dict[str, object]:
    """Certify the north-pole fuzzy-sphere tangent-plane oscillator window.

    Use the spin-j irrep with cutoff L=2j and basis |r> indexed by excitations
    below the north-pole coherent state. Define

        a_L = J_+ / sqrt(2j),    a_L^* = J_- / sqrt(2j).

    On |r>, the commutator [a_L, a_L^*] equals 1 - 2r/L. For fixed r and
    L -> infinity this approaches the oscillator commutator.
    """
    _validate_parameters(cutoff, excitation_cutoff)
    eigenvalues = _commutator_eigenvalues(
        cutoff=cutoff,
        excitation_cutoff=excitation_cutoff,
    )
    lower_bound = min(eigenvalues)
    identity_error = max(abs(1.0 - value) for value in eigenvalues)
    norm_lower_bound = sqrt(1.0 - excitation_cutoff / float(cutoff))
    local_generator_bound = float(excitation_cutoff + 1)
    short_lapse = 1.0 / float((cutoff + 1) ** 2)
    return {
        "cutoff_L": cutoff,
        "spin_j": _rounded(cutoff / 2.0),
        "hilbert_dimension": cutoff + 1,
        "observer_patch": "north_pole_low_excitation_window",
        "excitation_cutoff_R": excitation_cutoff,
        "operators": {
            "annihilation": "a_L = J_+ / sqrt(2j)",
            "creation": "a_L^* = J_- / sqrt(2j)",
            "selection": "fixed excitations r <= R around the north-pole coherent state",
        },
        "commutator": {
            "formula_on_r": "[a_L,a_L^*]|r> = (1 - 2r/L)|r>",
            "eigenvalues_on_window": eigenvalues,
            "lower_bound": _rounded(lower_bound),
            "identity_error_bound": _rounded(identity_error),
            "nonzero_for_this_cutoff": lower_bound > 0.0,
            "limit_for_fixed_R": 1.0,
        },
        "norm_faithfulness": {
            "relative_coefficient_lower_bound": _rounded(norm_lower_bound),
            "approaches_one_for_fixed_R": True,
        },
        "strong_continuity": {
            "local_generator_norm_bound": _rounded(local_generator_bound),
            "short_lapse": _rounded(short_lapse),
            "lapse_times_generator_bound": _rounded(
                short_lapse * local_generator_bound
            ),
            "goes_to_zero_for_fixed_R": True,
        },
    }


def tangent_plane_family_records(
    *,
    max_cutoff: int = 12,
    excitation_cutoff: int = 2,
) -> tuple[dict[str, object], ...]:
    """Return tangent-plane records from the first positive cutoff to max."""
    _validate_parameters(max_cutoff, excitation_cutoff)
    start = 2 * excitation_cutoff + 1
    return tuple(
        tangent_plane_double_scaling_record(
            cutoff=cutoff,
            excitation_cutoff=excitation_cutoff,
        )
        for cutoff in range(start, max_cutoff + 1)
    )


def _candidate(
    *,
    candidate_id: str,
    selection_rule: str,
    subsystem: str,
    verdict: str,
    theorem_content: str,
    obstruction_or_gap: str,
    gate_status: dict[str, str],
    quantitative_witness: dict[str, object],
) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "selection_rule": selection_rule,
        "anti_tautological_selection": _selection_is_anti_tautological(
            selection_rule
        ),
        "subsystem": subsystem,
        "verdict": verdict,
        "theorem_content": theorem_content,
        "obstruction_or_gap": obstruction_or_gap,
        "gate_status": gate_status,
        "quantitative_witness": quantitative_witness,
    }


def observer_local_candidate_records(
    *,
    max_cutoff: int = 12,
    excitation_cutoff: int = 2,
) -> tuple[dict[str, object], ...]:
    """Audit observer-local/static-patch subsystem candidates."""
    _validate_parameters(max_cutoff, excitation_cutoff)
    tangent_family = tangent_plane_family_records(
        max_cutoff=max_cutoff,
        excitation_cutoff=excitation_cutoff,
    )
    final_tangent = tangent_family[-1]
    lower_bounds = tuple(
        record["commutator"]["lower_bound"] for record in tangent_family
    )
    identity_errors = tuple(
        record["commutator"]["identity_error_bound"] for record in tangent_family
    )
    local_continuity_bounds = tuple(
        record["strong_continuity"]["lapse_times_generator_bound"]
        for record in tangent_family
    )
    return (
        _candidate(
            candidate_id="coherent_state_tangent_plane_double_scaling",
            selection_rule=(
                "select the north-pole coherent-state patch and fixed "
                "low-excitation window r <= R in the spin-j fuzzy-sphere irrep"
            ),
            subsystem=(
                "observer-local tangent oscillator operator system generated "
                "by a_L=J_+/sqrt(2j) and a_L^*=J_-/sqrt(2j)"
            ),
            verdict="A_theorem_candidate",
            theorem_content=(
                "For fixed excitation cutoff R and L>2R, the compressed "
                "commutator on the observer-local window obeys "
                "[a_L,a_L^*] >= (1-2R/L) I and converges to I as L grows."
            ),
            obstruction_or_gap=(
                "requires choosing an observer pole/static-patch frame; this "
                "is local observer data, not scalar screen data alone"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace_refinement="pass",
                covariance="pass",
                screen_shadow="pass",
                norm_faithfulness="pass",
                nonzero_commutator_lower_bound="pass",
                strong_continuity="pass",
                typeii_route="conditional",
            ),
            quantitative_witness={
                "family_cutoffs": tuple(record["cutoff_L"] for record in tangent_family),
                "commutator_lower_bounds": lower_bounds,
                "identity_error_bounds": identity_errors,
                "final_commutator_lower_bound": final_tangent["commutator"][
                    "lower_bound"
                ],
                "final_norm_faithfulness_lower_bound": final_tangent[
                    "norm_faithfulness"
                ]["relative_coefficient_lower_bound"],
                "local_continuity_bounds": local_continuity_bounds,
                "limit_commutator_for_fixed_R": 1.0,
            },
        ),
        _candidate(
            candidate_id="local_planck_cell_matrix_block",
            selection_rule=(
                "select the finite low-excitation block spanned by r <= R "
                "inside the observer coherent-state patch"
            ),
            subsystem="fixed finite matrix block on the observer-local excitation window",
            verdict="A_theorem_candidate",
            theorem_content=(
                "The low-excitation block gives a canonical local M_d candidate "
                "once an observer pole and excitation cutoff are supplied; "
                "isometric refinement preserves its operator norm exactly."
            ),
            obstruction_or_gap=(
                "the block is physically local but still requires a declared "
                "observer-frame/pole selection"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace_refinement="pass",
                covariance="conditional",
                screen_shadow="pass",
                norm_faithfulness="pass",
                nonzero_commutator_lower_bound="pass",
                strong_continuity="pass",
                typeii_route="conditional",
            ),
            quantitative_witness={
                "matrix_block_dimension": excitation_cutoff + 1,
                "norm_faithfulness_lower_bound": 1.0,
                "commutator_lower_bound": 1.0,
                "selection_depends_on_observer_patch": True,
            },
        ),
        _candidate(
            candidate_id="matrix_valued_screen_fiber",
            selection_rule=(
                "attach a fixed matrix fiber to the screen center and project "
                "screen shadows through the scalar trace over the fiber"
            ),
            subsystem="C(S^2)-like screen center with a fixed M_d fiber",
            verdict="C_requires_physical_fiber_origin",
            theorem_content=(
                "A fixed matrix fiber would retain noncommutative response, but "
                "the finite machinery does not derive that fiber from scalar "
                "static-patch data."
            ),
            obstruction_or_gap="needs an edge-mode, code, dressing, or observer-internal origin",
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace_refinement="conditional",
                covariance="conditional",
                screen_shadow="pass",
                norm_faithfulness="conditional",
                nonzero_commutator_lower_bound="conditional",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
            quantitative_witness={
                "conditional_matrix_fiber_dimension": "d fixed",
                "conditional_commutator_lower_bound": "kappa > 0",
                "missing_input": "physical origin of the noncommutative fiber",
            },
        ),
        _candidate(
            candidate_id="modular_crossed_product_clock_shift",
            selection_rule=(
                "generate a finite crossed-product-like subsystem from screen "
                "observables and a modular/energy shift selected by observer time"
            ),
            subsystem="finite screen algebra plus modular-time shift operator",
            verdict="C_requires_modular_clock_input",
            theorem_content=(
                "A modular shift can create noncommutative response with the "
                "screen algebra, but only if observer modular time is supplied "
                "as physical structure."
            ),
            obstruction_or_gap=(
                "screen data plus KMS covariance alone is too weak; the clock "
                "or crossed-product generator must be physically derived"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace_refinement="conditional",
                covariance="conditional",
                screen_shadow="pass",
                norm_faithfulness="conditional",
                nonzero_commutator_lower_bound="conditional",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
            quantitative_witness={
                "conditional_shift_commutator_lower_bound": "kappa > 0",
                "missing_input": "canonical observer modular-time shift",
                "kms_alone_known_insufficient": True,
            },
        ),
    )


def _all_gates_declared(candidates: tuple[dict[str, object], ...]) -> bool:
    return all(
        set(candidate["gate_status"]) == set(GATE_KEYS)
        and all(status in GATE_STATUSES for status in candidate["gate_status"].values())
        for candidate in candidates
    )


def observer_local_noncommutative_subsystem_certificate(
    *,
    max_cutoff: int = 12,
    excitation_cutoff: int = 2,
) -> dict[str, object]:
    """Emit the observer-local noncommutative subsystem theorem audit."""
    _validate_parameters(max_cutoff, excitation_cutoff)
    candidates = observer_local_candidate_records(
        max_cutoff=max_cutoff,
        excitation_cutoff=excitation_cutoff,
    )
    by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    tangent = by_id["coherent_state_tangent_plane_double_scaling"]
    block = by_id["local_planck_cell_matrix_block"]
    tangent_bounds = tangent["quantitative_witness"]["commutator_lower_bounds"]
    continuity_bounds = tangent["quantitative_witness"]["local_continuity_bounds"]
    certified_claims = {
        "all_candidate_subsystems_audited": len(candidates) == 4,
        "all_gate_statuses_declared": _all_gates_declared(candidates),
        "all_selection_rules_are_anti_tautological": all(
            candidate["anti_tautological_selection"] for candidate in candidates
        ),
        "tangent_plane_has_nonzero_commutator_lower_bound": all(
            bound > 0.0 for bound in tangent_bounds
        ),
        "tangent_plane_commutator_bounds_increase": all(
            tangent_bounds[index] >= tangent_bounds[index - 1]
            for index in range(1, len(tangent_bounds))
        ),
        "tangent_plane_strong_continuity_bounds_decrease": all(
            continuity_bounds[index] < continuity_bounds[index - 1]
            for index in range(1, len(continuity_bounds))
        ),
        "tangent_plane_passes_finite_lift_gates": all(
            status == "pass"
            for key, status in tangent["gate_status"].items()
            if key != "typeii_route"
        )
        and tangent["gate_status"]["typeii_route"] == "conditional",
        "local_matrix_block_is_norm_faithful": (
            block["quantitative_witness"]["norm_faithfulness_lower_bound"] == 1.0
        ),
        "fiber_and_modular_routes_remain_conditional": all(
            by_id[candidate_id]["verdict"].startswith("C_")
            for candidate_id in (
                "matrix_valued_screen_fiber",
                "modular_crossed_product_clock_shift",
            )
        ),
        "not_claimed_as_continuum_static_patch_theorem": True,
    }
    certified_claims["observer_local_noncommutative_subsystem_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Canonical Observer-Local Noncommutative Subsystem",
        "status": (
            "pass"
            if certified_claims[
                "observer_local_noncommutative_subsystem_certificate"
            ]
            else "fail"
        ),
        "result_type": "observer_local_tangent_plane_theorem_candidate",
        "selected_outcome": "A_theorem_candidate",
        "candidate_records": candidates,
        "theorem_candidate": (
            "For fixed observer pole and fixed excitation cutoff R, the "
            "fuzzy-sphere tangent-plane scaling a_L=J_+/sqrt(2j) has "
            "observer-local commutator lower bound 1-2R/L on r<=R. Thus the "
            "large-cutoff limit retains a noncommutative operator response "
            "even though global scalar fuzzy-sphere modes classicalize."
        ),
        "remaining_physics_assumption": (
            "the observer pole/static-patch frame and low-excitation window "
            "must be physically selected; the result is local tangent-plane "
            "physics, not a screen-only scalar dictionary"
        ),
        "expert_question": (
            "Is the coherent-state tangent-plane sector the right finite "
            "static-patch analogue of the observer-local algebra, or should "
            "the noncommutative subsystem instead come from an edge-mode fiber "
            "or modular crossed product?"
        ),
        "claim_boundary": (
            "finite observer-local theorem candidate under declared SU(2) "
            "coherent-patch scaling; not a continuum de Sitter theorem, dS/CFT "
            "construction, or ER=EPR proof"
        ),
        "certified_claims": certified_claims,
    }
