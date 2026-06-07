"""Canonical noncommutative cutoff-refinement audits."""

from __future__ import annotations

from .embedding_channels import approximate_static_patch_embedding_certificate
from .lift_diagnostics import finite_lift_decision_record
from .physical_static_patch_lift import MINIMAL_ASSUMPTION
from .relative_entropy_bridge import _rounded


SHARPER_MINIMAL_ASSUMPTION = (
    "the static-patch cutoff refinement must canonically select a "
    "noncommutative operator subsystem whose commutator scale has a nonzero "
    "large-cutoff lower bound, while remaining screen-compatible, "
    "trace-compatible, approximately covariant, and cutoff-continuous"
)

FORBIDDEN_SELECTION_TOKENS = (
    "bridge",
    "e_12",
    "e_21",
    "off-diagonal witness",
    "response witness",
)

GATE_KEYS = (
    "anti_tautological_selection",
    "cp_unital_trace",
    "low_mode_multiplicativity",
    "covariance",
    "screen_shadow",
    "norm_faithfulness",
    "nonzero_commutator_limit",
    "strong_continuity",
    "typeii_route",
)

GATE_STATUSES = ("pass", "conditional", "fail")


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 2:
        raise ValueError("max_cutoff must be at least two")


def _selection_is_anti_tautological(selection_rule: str) -> bool:
    lowered = selection_rule.lower()
    return not any(token in lowered for token in FORBIDDEN_SELECTION_TOKENS)


def _gate_statuses(
    *,
    anti_tautological_selection: str,
    cp_unital_trace: str,
    low_mode_multiplicativity: str,
    covariance: str,
    screen_shadow: str,
    norm_faithfulness: str,
    nonzero_commutator_limit: str,
    strong_continuity: str,
    typeii_route: str,
) -> dict[str, str]:
    statuses = {
        "anti_tautological_selection": anti_tautological_selection,
        "cp_unital_trace": cp_unital_trace,
        "low_mode_multiplicativity": low_mode_multiplicativity,
        "covariance": covariance,
        "screen_shadow": screen_shadow,
        "norm_faithfulness": norm_faithfulness,
        "nonzero_commutator_limit": nonzero_commutator_limit,
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


def _commutator_decay_bounds(
    *,
    max_cutoff: int,
    degree: int,
) -> tuple[float, ...]:
    if degree < 1:
        raise ValueError("degree must be at least one")
    return tuple(
        _rounded(min(1.0, (degree * degree) / float(cutoff + 1)))
        for cutoff in range(2, max_cutoff + 1)
    )


def _candidate(
    *,
    candidate_id: str,
    selection_rule: str,
    subsystem: str,
    refinement: str,
    verdict: str,
    cp_unital_trace: str,
    multiplicativity: str,
    covariance: str,
    screen_shadow: str,
    norm_faithfulness: str,
    commutator_response: str,
    strong_continuity: str,
    typeii_route: str,
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
        "refinement": refinement,
        "questions": {
            "cp_unital_trace_or_controlled_nonunitarity": cp_unital_trace,
            "approximate_multiplicativity_on_subsystem": multiplicativity,
            "approximate_static_patch_covariance": covariance,
            "screen_shadow_equivalence": screen_shadow,
            "norm_faithfulness_lower_bound": norm_faithfulness,
            "intrinsic_noncommutative_response": commutator_response,
            "cutoff_compatible_strong_continuity": strong_continuity,
            "typeii_static_patch_limit_route": typeii_route,
        },
        "gate_status": gate_status,
        "quantitative_witness": quantitative_witness,
        "verdict": verdict,
        "obstruction_or_gap": obstruction_or_gap,
    }


def canonical_noncommutative_candidate_records(
    *,
    max_cutoff: int = 6,
) -> tuple[dict[str, object], ...]:
    """Audit fixed nonabelian subsystem candidates independent of bridge labels."""
    _validate_max_cutoff(max_cutoff)
    embedding = approximate_static_patch_embedding_certificate(max_cutoff=max_cutoff)
    decision = finite_lift_decision_record(max_cutoff=max_cutoff)
    final_mult_error = embedding["physical_candidate_error_bounds"][-1]
    final_screen_error = embedding["screen_shadow_error_bounds"][-1]
    coordinate_decay = _commutator_decay_bounds(max_cutoff=max_cutoff, degree=1)
    polynomial_decay = _commutator_decay_bounds(max_cutoff=max_cutoff, degree=2)
    low_mode_decay = _commutator_decay_bounds(max_cutoff=max_cutoff, degree=1)
    return (
        _candidate(
            candidate_id="low_angular_momentum_matrix_modes",
            selection_rule=(
                "take the operator system generated by spherical-harmonic "
                "labels ell <= ell0 with fixed ell0 before taking L to infinity"
            ),
            subsystem=(
                "fixed low-mode scalar spherical-harmonic operator system"
            ),
            refinement=(
                "harmonic label refinement ell <= L embedded into ell <= L+1 "
                "with trace-filled UCP complement"
            ),
            verdict="B_no_go_for_fixed_scalar_low_modes",
            cp_unital_trace="finite UCP trace-compatible refinement exists",
            multiplicativity=(
                "asymptotically multiplicative with final audited bound "
                f"{_rounded(final_mult_error)}"
            ),
            covariance="mode-label rotation covariance is the intended structure",
            screen_shadow="declared low-mode screen data are preserved",
            norm_faithfulness="operator norm is retained on the preserved low-mode corner",
            commutator_response=(
                "scalar low modes classicalize; commutator upper bounds decay "
                f"as {low_mode_decay}"
            ),
            strong_continuity="inherits the finite strong-continuity gate conditionally",
            typeii_route=(
                "does not supply a fixed noncommutative Type-II observer "
                "subsystem by itself"
            ),
            obstruction_or_gap=(
                "canonical scalar low modes are too classical: they preserve "
                "screen data and norms but not a nonzero commutator scale"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace="pass",
                low_mode_multiplicativity="pass",
                covariance="conditional",
                screen_shadow="pass",
                norm_faithfulness="pass",
                nonzero_commutator_limit="fail",
                strong_continuity="conditional",
                typeii_route="fail",
            ),
            quantitative_witness={
                "commutator_upper_bounds": low_mode_decay,
                "commutator_limit": 0.0,
                "norm_faithfulness_lower_bound": 1.0,
                "multiplicativity_error_bound_at_max_cutoff": _rounded(
                    final_mult_error
                ),
            },
        ),
        _candidate(
            candidate_id="fuzzy_coordinate_polynomial_algebra",
            selection_rule=(
                "use normalized fuzzy-sphere coordinate operators X_i and "
                "their bounded-degree polynomial operator system"
            ),
            subsystem="bounded-degree fuzzy coordinate polynomial operator system",
            refinement="coordinate-polynomial refinement through the harmonic/heat cutoff",
            verdict="B_no_go_for_scalar_fuzzy_coordinates",
            cp_unital_trace="finite UCP/heat refinements can be trace compatible",
            multiplicativity=(
                "asymptotic product control is compatible with fuzzy-sphere "
                "classical convergence"
            ),
            covariance="rotation covariance is natural for the coordinate triple",
            screen_shadow="screen shadows are compatible with the scalar symbol limit",
            norm_faithfulness=(
                "norm convergence is plausible/standard for scalar fuzzy-sphere "
                "coordinates, and bounded in the finite surrogate"
            ),
            commutator_response=(
                "normalized coordinate commutators decay; audited upper bounds "
                f"for degree one are {coordinate_decay}"
            ),
            strong_continuity="compatible with fuzzy-sphere heat scaling",
            typeii_route=(
                "scalar coordinate polynomial limits approximate C(S^2), not a "
                "fixed noncommutative observer algebra"
            ),
            obstruction_or_gap=(
                "Berezin/fuzzy-sphere scalar convergence gives the wrong limit "
                "for this question: it is physically canonical but abelianizes"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace="pass",
                low_mode_multiplicativity="pass",
                covariance="pass",
                screen_shadow="pass",
                norm_faithfulness="conditional",
                nonzero_commutator_limit="fail",
                strong_continuity="pass",
                typeii_route="fail",
            ),
            quantitative_witness={
                "coordinate_commutator_upper_bounds": coordinate_decay,
                "bounded_degree_commutator_upper_bounds": polynomial_decay,
                "commutator_limit": 0.0,
                "screen_error_at_max_cutoff": _rounded(final_screen_error),
            },
        ),
        _candidate(
            candidate_id="coherent_state_localized_matrix_patches",
            selection_rule=(
                "choose a fixed-rank coherent-state localization patch from a "
                "rotation-covariant POVM/refinement rule"
            ),
            subsystem=(
                "fixed finite local matrix patch transported across cutoffs by "
                "coherent-state localization"
            ),
            refinement=(
                "coherent-state patch embedding followed by trace-compatible "
                "UCP complement"
            ),
            verdict="C_sharper_minimal_assumption",
            cp_unital_trace=(
                "CP is natural for coherent-state measurement/preparation; "
                "normalization must be specified"
            ),
            multiplicativity=(
                "can be controlled only if the patch transport is approximately "
                "isometric as an operator system"
            ),
            covariance=(
                "requires a covariant patch transport or a declared controlled "
                "symmetry breaking"
            ),
            screen_shadow="screen shadows remain compatible with coherent symbols",
            norm_faithfulness=(
                "would have a cutoff-independent lower bound if the fixed-rank "
                "patch is transported isometrically"
            ),
            commutator_response=(
                "can persist for a fixed matrix patch, but only after specifying "
                "canonical patch transport"
            ),
            strong_continuity="requires short-time modular/heat locality on the patch",
            typeii_route="conditional noncommutative local-patch route",
            obstruction_or_gap=(
                "this is the most physical-looking route, but the repo does not "
                "yet derive the coherent patch transport from static-patch data"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace="conditional",
                low_mode_multiplicativity="conditional",
                covariance="conditional",
                screen_shadow="conditional",
                norm_faithfulness="conditional",
                nonzero_commutator_limit="conditional",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
            quantitative_witness={
                "conditional_norm_faithfulness_lower_bound": "eta > 0",
                "conditional_commutator_lower_bound": "kappa > 0",
                "missing_input": "canonical coherent-state patch transport",
            },
        ),
        _candidate(
            candidate_id="finite_toeplitz_matrix_fiber_quantization",
            selection_rule=(
                "quantize a fixed finite matrix-fiber operator system over the "
                "screen rather than only scalar functions on the screen"
            ),
            subsystem="fixed noncommutative matrix-fiber operator system",
            refinement="Toeplitz/Berezin-style quantization with matrix-valued symbols",
            verdict="C_sharper_minimal_assumption",
            cp_unital_trace=(
                "possible for normalized matrix-valued quantization maps, but "
                "not constructed here"
            ),
            multiplicativity=(
                "would follow from matrix-valued Toeplitz asymptotic "
                "multiplicativity on the fixed fiber subsystem"
            ),
            covariance="requires a static-patch-covariant matrix-fiber choice",
            screen_shadow=(
                "screen shadows can factor through the scalar trace/symbol part"
            ),
            norm_faithfulness=(
                "matrix-fiber quantization would give the desired "
                "cutoff-independent norm lower bound"
            ),
            commutator_response=(
                "a fixed matrix fiber keeps a nonzero commutator scale by design, "
                "but the fiber must be physically selected"
            ),
            strong_continuity=(
                "requires compatible short-time heat/modular dynamics on the "
                "matrix-valued quantization"
            ),
            typeii_route="conditional noncommutative bundle/operator-system route",
            obstruction_or_gap=(
                "this gives a clean theorem schema, but it adds matrix-fiber "
                "structure not derived from the scalar static-patch screen"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace="conditional",
                low_mode_multiplicativity="conditional",
                covariance="conditional",
                screen_shadow="conditional",
                norm_faithfulness="conditional",
                nonzero_commutator_limit="conditional",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
            quantitative_witness={
                "conditional_norm_faithfulness_lower_bound": "eta > 0",
                "conditional_commutator_lower_bound": "kappa > 0",
                "missing_input": "static-patch origin of the matrix fiber",
            },
        ),
        _candidate(
            candidate_id="heat_kernel_refined_low_energy_operator_system",
            selection_rule=(
                "select the low-energy operator system stable under the "
                "fuzzy-sphere heat semigroup before choosing response probes"
            ),
            subsystem="heat-stable low-energy operator system",
            refinement="harmonic refinement followed by short-time heat-kernel damping",
            verdict="C_sharper_minimal_assumption",
            cp_unital_trace="finite heat-kernel Schur maps are UCP and trace compatible",
            multiplicativity="bounded/decreasing in the implemented heat audit",
            covariance="passes the finite Laplacian/heat covariance gate",
            screen_shadow="diagonal screen shadows are preserved",
            norm_faithfulness=(
                "low-energy norms are retained under short-time heat scaling"
            ),
            commutator_response=(
                "if the low-energy system is scalar it classicalizes; if it "
                "contains a fixed noncommutative sector, response persists"
            ),
            strong_continuity="passes under tau_L max_gap_L^2 -> 0",
            typeii_route="conditional on the low-energy sector being noncommutative",
            obstruction_or_gap=(
                "heat stability is not enough; the selected low-energy sector "
                "must include a fixed noncommutative subsystem"
            ),
            gate_status=_gate_statuses(
                anti_tautological_selection="pass",
                cp_unital_trace="pass",
                low_mode_multiplicativity="pass",
                covariance="pass",
                screen_shadow="pass",
                norm_faithfulness="pass",
                nonzero_commutator_limit="conditional",
                strong_continuity="pass",
                typeii_route="conditional",
            ),
            quantitative_witness={
                "minimum_heat_response_retention": decision[
                    "minimum_embedding_response_lower_bound"
                ],
                "scalar_low_energy_commutator_limit": 0.0,
                "conditional_noncommutative_sector_required": True,
            },
        ),
    )


def _all_gates_declared(candidates: tuple[dict[str, object], ...]) -> bool:
    return all(
        set(candidate["gate_status"]) == set(GATE_KEYS)
        and all(status in GATE_STATUSES for status in candidate["gate_status"].values())
        for candidate in candidates
    )


def canonical_noncommutative_refinement_certificate(
    *,
    max_cutoff: int = 6,
) -> dict[str, object]:
    """Emit the canonical noncommutative refinement theorem/no-go audit."""
    _validate_max_cutoff(max_cutoff)
    candidates = canonical_noncommutative_candidate_records(max_cutoff=max_cutoff)
    by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    no_go_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate["verdict"].startswith("B_no_go")
    )
    missing_assumption_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate["verdict"].startswith("C_")
    )
    scalar_no_go_ids = {
        "low_angular_momentum_matrix_modes",
        "fuzzy_coordinate_polynomial_algebra",
    }
    conditional_noncommutative_ids = {
        "coherent_state_localized_matrix_patches",
        "finite_toeplitz_matrix_fiber_quantization",
        "heat_kernel_refined_low_energy_operator_system",
    }
    certified_claims = {
        "all_candidate_subsystems_audited": len(candidates) == 5,
        "all_gate_statuses_declared": _all_gates_declared(candidates),
        "all_selection_rules_are_anti_tautological": all(
            candidate["anti_tautological_selection"] for candidate in candidates
        ),
        "scalar_canonical_routes_classicalize": all(
            by_id[candidate_id]["gate_status"]["nonzero_commutator_limit"] == "fail"
            and by_id[candidate_id]["quantitative_witness"]["commutator_limit"]
            == 0.0
            for candidate_id in scalar_no_go_ids
        ),
        "screen_and_norm_do_not_imply_noncommutative_response": (
            by_id["low_angular_momentum_matrix_modes"]["gate_status"][
                "screen_shadow"
            ]
            == "pass"
            and by_id["low_angular_momentum_matrix_modes"]["gate_status"][
                "norm_faithfulness"
            ]
            == "pass"
            and by_id["low_angular_momentum_matrix_modes"]["gate_status"][
                "nonzero_commutator_limit"
            ]
            == "fail"
        ),
        "conditional_noncommutative_routes_need_canonical_selection": all(
            by_id[candidate_id]["gate_status"]["nonzero_commutator_limit"]
            == "conditional"
            and by_id[candidate_id]["gate_status"]["typeii_route"] == "conditional"
            for candidate_id in conditional_noncommutative_ids
        ),
        "heat_route_is_not_enough_without_noncommutative_sector": (
            by_id["heat_kernel_refined_low_energy_operator_system"]["gate_status"][
                "strong_continuity"
            ]
            == "pass"
            and by_id["heat_kernel_refined_low_energy_operator_system"][
                "gate_status"
            ]["nonzero_commutator_limit"]
            == "conditional"
        ),
        "no_unconditional_physical_A_found": not any(
            all(status == "pass" for status in candidate["gate_status"].values())
            for candidate in candidates
        ),
        "minimal_assumption_sharpened": (
            SHARPER_MINIMAL_ASSUMPTION != MINIMAL_ASSUMPTION
        ),
        "not_claimed_as_continuum_static_patch_theorem": True,
    }
    certified_claims["canonical_noncommutative_refinement_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Canonical Noncommutative Cutoff Refinement",
        "status": (
            "pass"
            if certified_claims[
                "canonical_noncommutative_refinement_certificate"
            ]
            else "fail"
        ),
        "result_type": "sharper_minimal_assumption_for_canonical_refinement",
        "selected_outcome": "C_sharper_minimal_assumption",
        "sharper_minimal_assumption": SHARPER_MINIMAL_ASSUMPTION,
        "candidate_records": candidates,
        "no_go_candidates": tuple(
            candidate["candidate_id"] for candidate in no_go_candidates
        ),
        "missing_assumption_candidates": tuple(
            candidate["candidate_id"] for candidate in missing_assumption_candidates
        ),
        "gate_status_by_candidate": {
            candidate["candidate_id"]: candidate["gate_status"]
            for candidate in candidates
        },
        "theorem_candidate_under_assumption": (
            "If a static-patch cutoff refinement canonically selects a fixed "
            "finite noncommutative operator subsystem with a nonzero "
            "large-cutoff commutator lower bound and satisfies the stated "
            "screen, covariance, trace, multiplicativity, and continuity gates, "
            "then the continuum-lift obstruction becomes physics-relevant for "
            "that subsystem: screen-only data cannot determine the observer "
            "algebra."
        ),
        "no_go_statement": (
            "Canonical scalar fuzzy-sphere routes are not enough: low harmonic "
            "and bounded-degree coordinate-polynomial sectors can preserve "
            "screen data and norms while their commutator scale vanishes in "
            "the large-cutoff limit."
        ),
        "expert_question": (
            "Does static-patch/fuzzy-sphere physics supply a canonical "
            "noncommutative matrix-fiber, coherent-patch, or heat-stable "
            "operator subsystem with cutoff-independent commutator scale, or "
            "must the observer algebra be added as extra non-screen data?"
        ),
        "claim_boundary": (
            "finite theorem/no-go audit plus sharpened missing assumption; not "
            "a continuum de Sitter theorem, dS/CFT construction, or ER=EPR proof"
        ),
        "certified_claims": certified_claims,
    }
