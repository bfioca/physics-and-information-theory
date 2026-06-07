"""Physical static-patch lift hinge audits."""

from __future__ import annotations

from .embedding_channels import approximate_static_patch_embedding_certificate
from .lift_diagnostics import finite_lift_decision_record
from .relative_entropy_bridge import _rounded


MINIMAL_ASSUMPTION = (
    "there exists a screen-compatible, trace-compatible, approximately "
    "covariant cutoff refinement into a noncommutative observer algebra that "
    "is norm-faithful on a fixed finite nonabelian operator subsystem and "
    "compatible with short-time modular/heat locality"
)

FORBIDDEN_TAUTOLOGY_TOKENS = (
    "response gap",
    "screen-shadow obstruction",
    "m_n",
    "c^n",
    "off-diagonal witness survives",
)

GATE_KEYS = (
    "cp_unital_trace",
    "low_mode_multiplicativity",
    "covariance",
    "screen_shadow",
    "operator_response",
    "strong_continuity",
    "typeii_route",
)

GATE_STATUSES = ("pass", "conditional", "fail")


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 1:
        raise ValueError("max_cutoff must be at least one")


def _anti_tautological(text: str) -> bool:
    lowered = text.lower()
    return not any(token in lowered for token in FORBIDDEN_TAUTOLOGY_TOKENS)


def _gate_statuses(
    *,
    cp_unital_trace: str,
    low_mode_multiplicativity: str,
    covariance: str,
    screen_shadow: str,
    operator_response: str,
    strong_continuity: str,
    typeii_route: str,
) -> dict[str, str]:
    statuses = {
        "cp_unital_trace": cp_unital_trace,
        "low_mode_multiplicativity": low_mode_multiplicativity,
        "covariance": covariance,
        "screen_shadow": screen_shadow,
        "operator_response": operator_response,
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


def _all_gates_declared(candidates: tuple[dict[str, object], ...]) -> bool:
    return all(
        set(candidate["gate_status"].keys()) == set(GATE_KEYS)
        and all(status in GATE_STATUSES for status in candidate["gate_status"].values())
        for candidate in candidates
    )


def _candidate(
    *,
    candidate_id: str,
    canonical_structure: str,
    map_status: str,
    cp_unital_trace: str,
    multiplicativity: str,
    covariance: str,
    screen_shadow: str,
    response_survival: str,
    strong_continuity: str,
    typeii_route: str,
    verdict: str,
    obstruction_or_gap: str,
    gate_status: dict[str, str],
) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "canonical_structure": canonical_structure,
        "map_status": map_status,
        "questions": {
            "cp_unital_trace_or_controlled_nonunitarity": cp_unital_trace,
            "approximate_multiplicativity_on_low_modes": multiplicativity,
            "approximate_static_patch_covariance": covariance,
            "screen_shadow_equivalence": screen_shadow,
            "operator_response_large_cutoff_survival": response_survival,
            "cutoff_compatible_strong_continuity": strong_continuity,
            "typeii_static_patch_limit_route": typeii_route,
        },
        "gate_status": gate_status,
        "verdict": verdict,
        "obstruction_or_gap": obstruction_or_gap,
    }


def physical_lift_candidate_records(*, max_cutoff: int = 5) -> tuple[dict[str, object], ...]:
    """Classify canonical-ish static-patch lift candidates."""
    _validate_max_cutoff(max_cutoff)
    embedding = approximate_static_patch_embedding_certificate(max_cutoff=max_cutoff)
    decision = finite_lift_decision_record(max_cutoff=max_cutoff)
    minimum_retention = decision["minimum_embedding_response_lower_bound"]
    finite_screen_error = embedding["screen_shadow_error_bounds"][-1]
    finite_mult_error = embedding["physical_candidate_error_bounds"][-1]
    return (
        _candidate(
            candidate_id="berezin_toeplitz_symbol_quantization",
            canonical_structure="fuzzy-sphere Berezin symbol and Toeplitz quantization",
            map_status=(
                "conditional canonical candidate; current implementation is only "
                "a CP smoothing surrogate"
            ),
            cp_unital_trace=(
                "plausible/standard for normalized finite quantization maps, "
                "but not proved by the current repo"
            ),
            multiplicativity=(
                "conditional on a Toeplitz asymptotic-multiplicativity theorem; "
                f"surrogate bound at cutoff {max_cutoff}: {_rounded(finite_mult_error)}"
            ),
            covariance=(
                "conditional on rotation/static-patch covariance of the chosen "
                "coherent-state quantization"
            ),
            screen_shadow=(
                "bounded surrogate has vanishing screen perturbation; final "
                f"audited error {_rounded(finite_screen_error)}"
            ),
            response_survival=(
                "pure symbol maps to a commutative screen lose commutators; "
                "quantization-side noncommutative operator data must remain in "
                "the dictionary"
            ),
            strong_continuity=(
                "requires short-time heat/modular scaling from the physical "
                "continuity gate"
            ),
            typeii_route=(
                "possible only if the large-cutoff quantization is organized as "
                "a noncommutative observer-algebra limit, not only C(S^2)"
            ),
            verdict="C_minimal_missing_assumption",
            obstruction_or_gap=(
                "the missing proof is a canonical quantization/refinement that "
                "is screen-compatible and norm-faithful on a finite nonabelian "
                "operator subsystem"
            ),
            gate_status=_gate_statuses(
                cp_unital_trace="conditional",
                low_mode_multiplicativity="conditional",
                covariance="conditional",
                screen_shadow="conditional",
                operator_response="conditional",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
        ),
        _candidate(
            candidate_id="spherical_harmonic_projection_refinement",
            canonical_structure="mode-label refinement ell<=L inside ell<=L+1",
            map_status="implemented bounded physical-motivation audit",
            cp_unital_trace="finite proved by trace-filled UCP complement",
            multiplicativity="bounded by the 1/N_L trace-filled witness",
            covariance=(
                "mode-label covariance is plausible for rotations, but full "
                "static-patch generator covariance remains bounded/conditional"
            ),
            screen_shadow="low-harmonic diagonal data preserved exactly",
            response_survival="operator-norm witness retained in the preserved low-mode corner",
            strong_continuity="inherits the finite strong-continuity gate if dynamics are compatible",
            typeii_route="not by itself a Type-II route; needs compatible noncommutative limit maps",
            verdict="bounded_positive_not_canonical",
            obstruction_or_gap="physical naturalness is better than rank-ordering, but still not a canonical static-patch embedding",
            gate_status=_gate_statuses(
                cp_unital_trace="pass",
                low_mode_multiplicativity="pass",
                covariance="conditional",
                screen_shadow="pass",
                operator_response="pass",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
        ),
        _candidate(
            candidate_id="heat_kernel_coarse_graining",
            canonical_structure="harmonic refinement followed by heat-kernel Schur damping",
            map_status="implemented bounded physical-motivation audit",
            cp_unital_trace="finite proved for the declared positive-definite Schur heat kernel",
            multiplicativity="bounded/decreasing in the implemented audit",
            covariance="compatible with Laplacian/heat structure inside the finite model",
            screen_shadow="diagonal screen data fixed exactly",
            response_survival=(
                "positive retention tends to one under the declared cutoff scaling; "
                f"minimum audited retention {minimum_retention}"
            ),
            strong_continuity="positive if heat time obeys tau_L max_gap_L^2 -> 0",
            typeii_route="requires the heat maps to converge as dynamics on a noncommutative limit",
            verdict="bounded_positive_not_canonical",
            obstruction_or_gap="good finite route, but canonical static-patch heat/coarse-graining derivation is still missing",
            gate_status=_gate_statuses(
                cp_unital_trace="pass",
                low_mode_multiplicativity="pass",
                covariance="pass",
                screen_shadow="pass",
                operator_response="pass",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
        ),
        _candidate(
            candidate_id="modular_kms_conditional_expectations",
            canonical_structure="KMS/modular conditional expectations or modular-time averaging",
            map_status="partly implemented through modular/KMS continuity audits",
            cp_unital_trace="yes for modular-time averages and conditional expectations; raw Gibbs filters can fail unitality",
            multiplicativity="conditional expectations are not multiplicative outside the fixed algebra",
            covariance="KMS/modular covariance can hold",
            screen_shadow="diagonal/screen data can be preserved",
            response_survival=(
                "fails for stationary modular twirling or full conditional "
                "expectation onto the diagonal/fixed algebra"
            ),
            strong_continuity="KMS alone fails; short-time approximate identity is required",
            typeii_route="possible only for short-time/local modular dynamics, not stationary twirling",
            verdict="B_no_go_for_kms_alone__C_with_short_time_locality",
            obstruction_or_gap="KMS/detailed balance is too weak; the missing physical input is cutoff-local modular time localization",
            gate_status=_gate_statuses(
                cp_unital_trace="conditional",
                low_mode_multiplicativity="fail",
                covariance="pass",
                screen_shadow="pass",
                operator_response="fail",
                strong_continuity="fail",
                typeii_route="conditional",
            ),
        ),
        _candidate(
            candidate_id="coherent_state_fuzzy_sphere_refinement",
            canonical_structure="coherent-state POVM/symbol refinement on the fuzzy sphere",
            map_status="not implemented as a canonical map in this repo",
            cp_unital_trace="conditional; coherent-state measurement is CP, quantization normalization must be specified",
            multiplicativity="conditional on coherent-state/fuzzy-sphere asymptotics",
            covariance="plausible under rotation-covariant coherent states",
            screen_shadow="plausible for low-mode diagonal/symbol data",
            response_survival=(
                "fails if only the commutative symbol is kept; can work only if "
                "the quantized noncommutative operator system remains accessible"
            ),
            strong_continuity="conditional on short-time heat/modular locality",
            typeii_route="conditional noncommutative operator-system route",
            verdict="C_minimal_missing_assumption",
            obstruction_or_gap="needs a specified coherent-state refinement that is norm-faithful on finite nonabelian subsystems",
            gate_status=_gate_statuses(
                cp_unital_trace="conditional",
                low_mode_multiplicativity="conditional",
                covariance="conditional",
                screen_shadow="conditional",
                operator_response="conditional",
                strong_continuity="conditional",
                typeii_route="conditional",
            ),
        ),
        _candidate(
            candidate_id="common_continuum_l2_s2_screen_embedding",
            canonical_structure="embed finite data into a common commutative L2(S^2)/screen algebra",
            map_status="natural for screen data, not for observer algebra",
            cp_unital_trace="can be positive/trace-compatible as a symbol or measurement map",
            multiplicativity="as a commutative target, it cannot preserve matrix multiplication",
            covariance="can be rotation covariant for spherical harmonics",
            screen_shadow="yes, this is the natural home for screen shadows",
            response_survival="no: commutative L2/C(S^2) targets erase commutators",
            strong_continuity="irrelevant to observer algebra unless noncommutative lift data are also retained",
            typeii_route="no Type-II observer-algebra route from screen-only commutative data",
            verdict="B_no_go_for_screen_only_common_continuum",
            obstruction_or_gap="a common commutative continuum screen can calibrate shadows but cannot determine the noncommutative observer algebra",
            gate_status=_gate_statuses(
                cp_unital_trace="pass",
                low_mode_multiplicativity="fail",
                covariance="pass",
                screen_shadow="pass",
                operator_response="fail",
                strong_continuity="fail",
                typeii_route="fail",
            ),
        ),
    )


def physical_static_patch_lift_certificate(*, max_cutoff: int = 5) -> dict[str, object]:
    """Emit the physics-hinge audit for static-patch continuum lifts."""
    _validate_max_cutoff(max_cutoff)
    candidates = physical_lift_candidate_records(max_cutoff=max_cutoff)
    decision = finite_lift_decision_record(max_cutoff=max_cutoff)
    candidate_by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    positive_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate["verdict"] == "bounded_positive_not_canonical"
    )
    no_go_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate["verdict"].startswith("B_no_go")
    )
    missing_assumption_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate["verdict"].startswith("C_")
        or "__C_" in candidate["verdict"]
    )
    gate_status_by_candidate = {
        candidate["candidate_id"]: candidate["gate_status"]
        for candidate in candidates
    }
    certified_claims = {
        "all_requested_candidate_classes_audited": len(candidates) == 6,
        "all_gate_statuses_declared": _all_gates_declared(candidates),
        "finite_lift_theorem_engine_remains_valid": decision[
            "finite_requirements_satisfied"
        ],
        "no_unconditional_canonical_lift_found": not any(
            all(status == "pass" for status in candidate["gate_status"].values())
            and candidate["verdict"] == "A_theorem_candidate"
            for candidate in candidates
        ),
        "harmonic_and_heat_are_bounded_positive_but_not_canonical": (
            len(positive_candidates) == 2
        ),
        "bounded_positive_routes_retain_response_but_leave_typeii_conditional": all(
            candidate["gate_status"]["operator_response"] == "pass"
            and candidate["gate_status"]["typeii_route"] == "conditional"
            for candidate in positive_candidates
        ),
        "kms_alone_no_go_identified": candidate_by_id[
            "modular_kms_conditional_expectations"
        ]["verdict"].startswith("B_no_go"),
        "kms_no_go_is_response_and_continuity_failure": (
            gate_status_by_candidate["modular_kms_conditional_expectations"][
                "operator_response"
            ]
            == "fail"
            and gate_status_by_candidate["modular_kms_conditional_expectations"][
                "strong_continuity"
            ]
            == "fail"
        ),
        "commutative_l2_screen_no_go_identified": candidate_by_id[
            "common_continuum_l2_s2_screen_embedding"
        ]["verdict"]
        == "B_no_go_for_screen_only_common_continuum",
        "commutative_screen_no_go_is_response_and_typeii_failure": (
            gate_status_by_candidate["common_continuum_l2_s2_screen_embedding"][
                "screen_shadow"
            ]
            == "pass"
            and gate_status_by_candidate["common_continuum_l2_s2_screen_embedding"][
                "operator_response"
            ]
            == "fail"
            and gate_status_by_candidate["common_continuum_l2_s2_screen_embedding"][
                "typeii_route"
            ]
            == "fail"
        ),
        "berezin_and_coherent_need_missing_assumption": {
            candidate_by_id["berezin_toeplitz_symbol_quantization"]["verdict"],
            candidate_by_id["coherent_state_fuzzy_sphere_refinement"]["verdict"],
        }
        == {"C_minimal_missing_assumption"},
        "minimal_assumption_is_non_tautological": _anti_tautological(
            MINIMAL_ASSUMPTION
        ),
        "not_claimed_as_continuum_static_patch_theorem": True,
    }
    certified_claims["physical_static_patch_lift_hinge_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Physical Static-Patch Continuum-Lift Hinge",
        "status": (
            "pass"
            if certified_claims["physical_static_patch_lift_hinge_certificate"]
            else "fail"
        ),
        "result_type": "minimal_missing_assumption_for_physical_static_patch_lift",
        "selected_outcome": "C_minimal_missing_assumption",
        "minimal_missing_assumption": MINIMAL_ASSUMPTION,
        "candidate_records": candidates,
        "gate_status_by_candidate": gate_status_by_candidate,
        "positive_bounded_candidates": tuple(
            candidate["candidate_id"] for candidate in positive_candidates
        ),
        "no_go_candidates": tuple(
            candidate["candidate_id"] for candidate in no_go_candidates
        ),
        "missing_assumption_candidates": tuple(
            candidate["candidate_id"] for candidate in missing_assumption_candidates
        ),
        "relationship_to_existing_continuum_lift": {
            "finite_decision": decision["selected_outcome"],
            "finite_requirements_satisfied": decision[
                "finite_requirements_satisfied"
            ],
            "minimum_embedding_response_lower_bound": decision[
                "minimum_embedding_response_lower_bound"
            ],
            "refinement": (
                "the finite theorem engine is intact, but physically natural "
                "static-patch promotion requires a canonical noncommutative "
                "cutoff refinement rather than a screen-only common continuum"
            ),
        },
        "theorem_candidate": (
            "If a physically natural static-patch cutoff refinement satisfies "
            "the minimal missing assumption, then the continuum-lift "
            "obstruction theorem applies: screen-only data cannot determine "
            "the observer algebra when noncommutative operator response is "
            "retained."
        ),
        "no_go_statement": (
            "KMS/modular covariance alone and common commutative L2(S^2) "
            "screen embeddings are insufficient: they can preserve screen "
            "data while erasing the noncommutative observer-algebra witness."
        ),
        "claim_boundary": (
            "physics-hinge audit and minimal-assumption result only; not a "
            "continuum de Sitter theorem, dS/CFT construction, or ER=EPR proof"
        ),
        "certified_claims": certified_claims,
    }
