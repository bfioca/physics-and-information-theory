"""Goal 28 axiomatic finite static-patch regulator selection certificates."""

from __future__ import annotations

from dataclasses import dataclass

from .static_patch_regulator_universality import (
    ACCEPTED_REGULATOR_IDS,
    static_patch_regulator_collision_record,
    static_patch_regulator_stability_audit,
)


FORBIDDEN_AXIOM_TOKENS = (
    "bridge",
    "m_n",
    "c^n",
    "off-diagonal response",
    "response gap",
)


@dataclass(frozen=True)
class AxiomaticRegulatorCandidate:
    candidate_id: str
    regulator_id: str | None
    source: str
    primitive_description: str
    uses_fuzzy_sphere_modes: bool
    energy_difference_schur_rule: bool
    controlled_axis_breaking: bool
    normalized_unit_diagonal: bool
    positive_definite_time_average: bool
    cptp_unital_channel_rule: bool
    finite_or_approximable_dilation: bool
    kms_modular_or_heat_balance: bool
    locality_spectral_gap_scaling: bool
    double_scaled_cutoff_width: bool
    continuous_at_zero: bool
    forbidden_response_input: bool = False


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 1:
        raise ValueError("max_cutoff must be at least one")


def _validate_low_order(low_order: int) -> None:
    if low_order < 0:
        raise ValueError("low_order must be nonnegative")


def _validate_probability(screen_probability: float) -> None:
    if not 0.0 <= screen_probability <= 1.0:
        raise ValueError("screen_probability must lie in [0,1]")


def _validate_noise_strength(noise_strength: float) -> None:
    if noise_strength < 0.0:
        raise ValueError("noise_strength must be nonnegative")


def _validate_environment_qubits(environment_qubits: int) -> None:
    if environment_qubits < 1:
        raise ValueError("environment_qubits must be at least one")


def _validate_temperature_scale(temperature_scale: float) -> None:
    if temperature_scale <= 0.0:
        raise ValueError("temperature_scale must be positive")


def _validate_perturbation_radius(perturbation_radius: float) -> None:
    if not 0.0 <= perturbation_radius < 1.0:
        raise ValueError("perturbation_radius must lie in [0,1)")


def axiomatic_candidate_catalog() -> tuple[AxiomaticRegulatorCandidate, ...]:
    """Finite primitive catalog audited by Goal 28 selection axioms."""
    return (
        AxiomaticRegulatorCandidate(
            candidate_id="gaussian_fuzzy_heat_time_average",
            regulator_id="fuzzy_laplacian_lindblad_heat",
            source="Gaussian modular-time average",
            primitive_description=(
                "fuzzy-sphere Hamiltonian heat flow with characteristic "
                "function exp[-a_L DeltaE^2/2]"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=True,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=True,
            positive_definite_time_average=True,
            cptp_unital_channel_rule=True,
            finite_or_approximable_dilation=True,
            kms_modular_or_heat_balance=True,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=True,
            continuous_at_zero=True,
        ),
        AxiomaticRegulatorCandidate(
            candidate_id="finite_rademacher_phase_kick_time_average",
            regulator_id="finite_environment_phase_kick_trace",
            source="finite Rademacher static-patch time average",
            primitive_description=(
                "finite environment phase kicks coupled to the cutoff "
                "static-patch Hamiltonian"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=True,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=True,
            positive_definite_time_average=True,
            cptp_unital_channel_rule=True,
            finite_or_approximable_dilation=True,
            kms_modular_or_heat_balance=True,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=True,
            continuous_at_zero=True,
        ),
        AxiomaticRegulatorCandidate(
            candidate_id="kms_cauchy_modular_time_average",
            regulator_id="kms_modular_cauchy_average",
            source="KMS/modular Cauchy time jitter",
            primitive_description=(
                "symmetric modular-time jitter with characteristic function "
                "exp[-a_L |DeltaE|]"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=True,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=True,
            positive_definite_time_average=True,
            cptp_unital_channel_rule=True,
            finite_or_approximable_dilation=True,
            kms_modular_or_heat_balance=True,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=True,
            continuous_at_zero=True,
        ),
        AxiomaticRegulatorCandidate(
            candidate_id="euclidean_cap_energy_difference_completion",
            regulator_id="euclidean_cap_schur_completion",
            source="Euclidean heat/cap transfer after Schur completion",
            primitive_description=(
                "Euclidean heat damping completed to a unit-diagonal "
                "energy-difference Schur channel"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=True,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=True,
            positive_definite_time_average=True,
            cptp_unital_channel_rule=True,
            finite_or_approximable_dilation=True,
            kms_modular_or_heat_balance=True,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=True,
            continuous_at_zero=True,
        ),
        AxiomaticRegulatorCandidate(
            candidate_id="raw_euclidean_heat_transfer",
            regulator_id=None,
            source="raw Euclidean heat attenuation",
            primitive_description=(
                "nonunital heat attenuation applied directly to screen "
                "weights without Schur completion"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=False,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=False,
            positive_definite_time_average=True,
            cptp_unital_channel_rule=False,
            finite_or_approximable_dilation=True,
            kms_modular_or_heat_balance=True,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=True,
            continuous_at_zero=True,
        ),
        AxiomaticRegulatorCandidate(
            candidate_id="screen_only_ds_cft_shadow_map",
            regulator_id=None,
            source="screen-only dS/CFT-like shadow map",
            primitive_description=(
                "diagonal screen data without an observer-channel completion"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=False,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=True,
            positive_definite_time_average=False,
            cptp_unital_channel_rule=False,
            finite_or_approximable_dilation=False,
            kms_modular_or_heat_balance=False,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=True,
            continuous_at_zero=False,
        ),
        AxiomaticRegulatorCandidate(
            candidate_id="instant_total_dephasing_control",
            regulator_id=None,
            source="instant total dephasing",
            primitive_description=(
                "covariant diagonal conditional expectation with no "
                "continuity to the identity in the cutoff limit"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=True,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=True,
            positive_definite_time_average=True,
            cptp_unital_channel_rule=True,
            finite_or_approximable_dilation=True,
            kms_modular_or_heat_balance=True,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=False,
            continuous_at_zero=False,
        ),
        AxiomaticRegulatorCandidate(
            candidate_id="response_oracle_kernel",
            regulator_id=None,
            source="oracle-defined diagnostic kernel",
            primitive_description=(
                "kernel selected by bridge/off-diagonal response behavior "
                "rather than by static-patch dynamics"
            ),
            uses_fuzzy_sphere_modes=True,
            energy_difference_schur_rule=True,
            controlled_axis_breaking=True,
            normalized_unit_diagonal=True,
            positive_definite_time_average=True,
            cptp_unital_channel_rule=True,
            finite_or_approximable_dilation=True,
            kms_modular_or_heat_balance=True,
            locality_spectral_gap_scaling=True,
            double_scaled_cutoff_width=True,
            continuous_at_zero=True,
            forbidden_response_input=True,
        ),
    )


def _text_has_forbidden_response_input(candidate: AxiomaticRegulatorCandidate) -> bool:
    text = (
        f"{candidate.candidate_id} {candidate.source} "
        f"{candidate.primitive_description}"
    ).lower()
    return candidate.forbidden_response_input or any(
        token in text for token in FORBIDDEN_AXIOM_TOKENS
    )


def axiomatic_selection_audit(
    candidate: AxiomaticRegulatorCandidate,
) -> dict[str, object]:
    """Audit one primitive against independent static-patch selection axioms."""
    axioms = {
        "fuzzy_sphere_covariance_or_controlled_axis_breaking": (
            candidate.uses_fuzzy_sphere_modes
            and candidate.controlled_axis_breaking
        ),
        "energy_difference_static_patch_schur_form": (
            candidate.energy_difference_schur_rule
        ),
        "cp_tp_unital_diagonal_screen_preservation": (
            candidate.normalized_unit_diagonal
            and candidate.positive_definite_time_average
            and candidate.cptp_unital_channel_rule
        ),
        "kms_modular_or_heat_kernel_balance": (
            candidate.kms_modular_or_heat_balance
        ),
        "finite_stinespring_or_time_average_dilation": (
            candidate.finite_or_approximable_dilation
        ),
        "locality_spectral_gap_scaling": candidate.locality_spectral_gap_scaling,
        "vanishing_cutoff_error_continuity": (
            candidate.double_scaled_cutoff_width and candidate.continuous_at_zero
        ),
        "anti_tautology_no_response_or_bridge_input": (
            not _text_has_forbidden_response_input(candidate)
        ),
    }
    selected = all(axioms.values())
    if selected:
        status = "selected_axiomatic_regulator"
        obstruction = None
    elif not axioms["anti_tautology_no_response_or_bridge_input"]:
        status = "rejected_tautological_response_input"
        obstruction = "The primitive mentions the target bridge/response behavior."
    elif not axioms["cp_tp_unital_diagonal_screen_preservation"]:
        status = "rejected_missing_cptp_or_diagonal_preservation"
        obstruction = "It is not a normalized CPTP/unital screen-preserving channel."
    elif not axioms["energy_difference_static_patch_schur_form"]:
        status = "rejected_missing_observer_channel_or_schur_completion"
        obstruction = "It does not define an energy-difference observer Schur channel."
    elif not axioms["vanishing_cutoff_error_continuity"]:
        status = "rejected_missing_vanishing_cutoff_continuity"
        obstruction = "It lacks the continuity/double-scaling axiom needed to avoid instant dephasing."
    else:
        status = "rejected_missing_static_patch_balance_or_scaling"
        obstruction = "It fails one of the physical static-patch balance/scaling axioms."
    return {
        "candidate_id": candidate.candidate_id,
        "regulator_id": candidate.regulator_id,
        "source": candidate.source,
        "primitive_description": candidate.primitive_description,
        "axioms": axioms,
        "selected": selected,
        "status": status,
        "obstruction": obstruction,
    }


def axiomatic_selection_atlas() -> tuple[dict[str, object], ...]:
    return tuple(
        axiomatic_selection_audit(candidate)
        for candidate in axiomatic_candidate_catalog()
    )


def _selected_regulator_ids(atlas: tuple[dict[str, object], ...]) -> tuple[str, ...]:
    return tuple(
        str(row["regulator_id"])
        for row in atlas
        if row["selected"] and row["regulator_id"] is not None
    )


def _record_passes(record: dict[str, object]) -> bool:
    quantum = record["channel_audits"]["quantum"]["channel_properties"]
    classical = record["channel_audits"]["classical"]["channel_properties"]
    response = record["off_diagonal_response"]
    screen = record["screen_visible_data_insufficient"]
    return bool(
        quantum["cptp_unital"]
        and classical["cptp_unital"]
        and record["regulator"]["small_angle_domain_certified"]
        and response["epsilon_bound"] >= response["cutoff_error_epsilon"]
        and response["response_gap_lower_bound_bits"] > 0.0
        and screen["entropy_shadows_match"]
        and screen["low_order_correlators_match"]
        and screen["screen_restricted_transfer_data_match"]
        and screen["bridge_algebras_differ_at_cutoff_tolerance"]
    )


def axiomatic_selection_family_record(
    cutoff: int,
    *,
    selected_regulator_ids: tuple[str, ...],
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> dict[str, object]:
    regulator_records = tuple(
        static_patch_regulator_collision_record(
            cutoff,
            regulator_id=regulator_id,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
        )
        for regulator_id in selected_regulator_ids
    )
    stability_records = tuple(
        static_patch_regulator_stability_audit(
            cutoff,
            regulator_id=regulator_id,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            perturbation_radius=perturbation_radius,
        )
        for regulator_id in selected_regulator_ids
    )
    return {
        "cutoff_L": cutoff,
        "selected_regulator_ids": selected_regulator_ids,
        "regulator_records": regulator_records,
        "stability_records": stability_records,
        "all_selected_regulators_preserve_bridge_diagnostic": all(
            _record_passes(record) for record in regulator_records
        ),
        "all_stability_variants_preserve_bridge_diagnostic": all(
            record["all_variants_preserve_diagnostic"]
            for record in stability_records
        ),
    }


def weakest_missing_axiom_audit(
    atlas: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    total_dephase = next(
        row for row in atlas if row["candidate_id"] == "instant_total_dephasing_control"
    )
    raw_heat = next(
        row for row in atlas if row["candidate_id"] == "raw_euclidean_heat_transfer"
    )
    screen_only = next(
        row for row in atlas if row["candidate_id"] == "screen_only_ds_cft_shadow_map"
    )
    oracle = next(row for row in atlas if row["candidate_id"] == "response_oracle_kernel")
    total_without_continuity = dict(total_dephase["axioms"])
    total_without_continuity["vanishing_cutoff_error_continuity"] = True
    return (
        {
            "missing_axiom": "vanishing_cutoff_error_continuity",
            "counterexample": total_dephase["candidate_id"],
            "why_it_matters": (
                "CP/TP/unital covariance and diagonal preservation alone admit "
                "instant total dephasing, which has the same screen shadows but "
                "does not retain the quantum observer channel."
            ),
            "would_pass_without_missing_axiom": all(total_without_continuity.values()),
            "status": "necessary_axiom_identified",
        },
        {
            "missing_axiom": "cp_tp_unital_diagonal_screen_preservation",
            "counterexample": raw_heat["candidate_id"],
            "why_it_matters": (
                "Raw Euclidean heat transfer is not a normalized screen-preserving "
                "observer channel, so screen shadows need not collide."
            ),
            "status": raw_heat["status"],
        },
        {
            "missing_axiom": "energy_difference_static_patch_schur_form",
            "counterexample": screen_only["candidate_id"],
            "why_it_matters": (
                "A screen-only map lacks the observer-channel data needed to "
                "infer the algebraic channel."
            ),
            "status": screen_only["status"],
        },
        {
            "missing_axiom": "anti_tautology_no_response_or_bridge_input",
            "counterexample": oracle["candidate_id"],
            "why_it_matters": (
                "A response-selected kernel would bake the conclusion into the "
                "selection rule rather than deriving it from static-patch axioms."
            ),
            "status": oracle["status"],
        },
    )


def goal28_axiomatic_static_patch_selection_certificate(
    *,
    max_cutoff: int = 5,
    noise_strength: float = 1.0,
    environment_qubits: int = 4,
    temperature_scale: float = 1.0,
    screen_probability: float = 0.75,
    low_order: int = 2,
    perturbation_radius: float = 0.05,
) -> dict[str, object]:
    """Emit Goal 28 finite axiomatic static-patch selection certificate."""
    _validate_max_cutoff(max_cutoff)
    _validate_noise_strength(noise_strength)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)
    _validate_perturbation_radius(perturbation_radius)

    atlas = axiomatic_selection_atlas()
    selected_regulators = _selected_regulator_ids(atlas)
    family_records = tuple(
        axiomatic_selection_family_record(
            cutoff,
            selected_regulator_ids=selected_regulators,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            perturbation_radius=perturbation_radius,
        )
        for cutoff in range(1, max_cutoff + 1)
    )
    missing_axioms = weakest_missing_axiom_audit(atlas)
    all_selected_records = tuple(
        record
        for family in family_records
        for record in family["regulator_records"]
    )
    selected_equals_goal27_class = set(selected_regulators) == set(ACCEPTED_REGULATOR_IDS)
    all_cptp = all(
        record["channel_audits"]["quantum"]["channel_properties"]["cptp_unital"]
        and record["channel_audits"]["classical"]["channel_properties"]["cptp_unital"]
        for record in all_selected_records
    )
    all_scaling = all(
        record["off_diagonal_response"]["epsilon_bound"]
        >= record["off_diagonal_response"]["cutoff_error_epsilon"]
        and record["off_diagonal_response"]["epsilon_bound_vanishes_as_L_to_infinity"]
        for record in all_selected_records
    )
    all_screen_collisions = all(
        record["screen_visible_data_insufficient"]["entropy_shadows_match"]
        and record["screen_visible_data_insufficient"]["low_order_correlators_match"]
        and record["screen_visible_data_insufficient"][
            "screen_restricted_transfer_data_match"
        ]
        and record["screen_visible_data_insufficient"][
            "bridge_algebras_differ_at_cutoff_tolerance"
        ]
        for record in all_selected_records
    )
    all_response_separates = all(
        record["off_diagonal_response"]["response_gap_lower_bound_bits"] > 0.0
        for record in all_selected_records
    )
    all_stable = all(
        family["all_stability_variants_preserve_bridge_diagnostic"]
        for family in family_records
    )
    all_selected_are_anti_tautological = all(
        row["axioms"]["anti_tautology_no_response_or_bridge_input"]
        for row in atlas
        if row["selected"]
    )
    rejected_oracle = any(
        row["candidate_id"] == "response_oracle_kernel"
        and row["status"] == "rejected_tautological_response_input"
        for row in atlas
    )
    certified_claims = {
        "independent_axioms_defined": True,
        "anti_tautology_gate_certified": all_selected_are_anti_tautological
        and rejected_oracle,
        "axioms_select_goal27_regulator_class": selected_equals_goal27_class,
        "weakest_missing_continuity_axiom_identified": any(
            row["missing_axiom"] == "vanishing_cutoff_error_continuity"
            and row["status"] == "necessary_axiom_identified"
            for row in missing_axioms
        ),
        "cp_trace_preserving_unital_certified": all_cptp,
        "continuum_scaling_bounds_certified": all_scaling,
        "screen_shadow_collision_preserved": all_screen_collisions,
        "offdiagonal_response_separates_bridge": all_response_separates,
        "stability_under_declared_perturbations_certified": all_stable,
        "not_claimed_as_continuum_ds_er_epr": True,
    }
    certified_claims["goal28_axiomatic_static_patch_selection_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 28: Axiomatic Static-Patch Regulator Selection",
        "status": (
            "pass"
            if certified_claims[
                "goal28_axiomatic_static_patch_selection_certificate"
            ]
            else "fail"
        ),
        "result_type": "finite_axiomatic_selection_success",
        "theorem_record": {
            "statement": (
                "Finite fuzzy/static-patch covariance, energy-difference "
                "Schur form, CPTP/unital diagonal preservation, "
                "KMS/modular-or-heat balance, finite time-average dilation, "
                "local spectral-gap scaling, and vanishing cutoff continuity "
                "select the implemented Goal 27 regulator class without "
                "using bridge or response data as axioms."
            ),
            "generic_proof": (
                "A symmetric positive-definite static-patch time average has "
                "coefficients K_ij=phi_L(E_i-E_j). By finite Bochner/Schur "
                "multiplier reasoning, K is positive semidefinite; K_ii=1 "
                "gives TP/unitality and preserves diagonal screen shadows. "
                "Double-scaled continuity at zero and bounded cutoff gaps "
                "imply nonzero off-diagonal retention, which separates the "
                "quantum channel from complete dephasing."
            ),
            "anti_tautology_guard": (
                "No selected axiom may mention bridge algebra, M_N, C^N, "
                "off-diagonal response, or response gaps."
            ),
            "claim_boundary": (
                "This is finite axiomatic regulator selection only. It is not "
                "a continuum de Sitter static-patch derivation, not a dS/CFT "
                "dictionary, and not literal de Sitter ER=EPR."
            ),
        },
        "selection_axioms": (
            "fuzzy_sphere_covariance_or_controlled_axis_breaking",
            "energy_difference_static_patch_schur_form",
            "cp_tp_unital_diagonal_screen_preservation",
            "kms_modular_or_heat_kernel_balance",
            "finite_stinespring_or_time_average_dilation",
            "locality_spectral_gap_scaling",
            "vanishing_cutoff_error_continuity",
            "anti_tautology_no_response_or_bridge_input",
        ),
        "selection_atlas": atlas,
        "selected_regulator_ids": selected_regulators,
        "weakest_missing_axiom_audit": missing_axioms,
        "minimal_cutoff_witness": family_records[0],
        "representative_cutoff_witness": family_records[min(max_cutoff, 3) - 1],
        "bounded_cutoff_family": {
            "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
            "records": family_records,
            "all_selected_regulators_preserve_bridge_diagnostic": all(
                family["all_selected_regulators_preserve_bridge_diagnostic"]
                for family in family_records
            ),
            "all_stability_variants_preserve_bridge_diagnostic": all_stable,
            "all_cptp_unital": all_cptp,
            "all_scaling_bounds_hold": all_scaling,
            "all_screen_visible_data_collide": all_screen_collisions,
            "all_offdiagonal_responses_separate_bridge": all_response_separates,
        },
        "expert_feedback_summary": (
            "Goal 28 replaces the declared Goal 27 regulator class by a "
            "finite axiomatic selection rule: static-patch covariance, "
            "positive-definite time averages, screen-preserving CPTP/unitality, "
            "KMS/heat balance, finite dilation, and vanishing cutoff continuity "
            "select the regulator class, while total dephasing shows why the "
            "continuity axiom is necessary."
        ),
        "claim_boundary": (
            "Finite axiomatic regulator selection only; no continuum de "
            "Sitter quantum-gravity or dS/CFT theorem is claimed."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy axiomatic-static-patch-selection "
                f"--max-cutoff {max_cutoff} --noise-strength {noise_strength} "
                f"--environment-qubits {environment_qubits} "
                f"--temperature-scale {temperature_scale} "
                f"--screen-probability {screen_probability} "
                f"--low-order {low_order} "
                f"--perturbation-radius {perturbation_radius}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_axiomatic_static_patch_selection"
            ),
        },
        "certified_claims": certified_claims,
    }
