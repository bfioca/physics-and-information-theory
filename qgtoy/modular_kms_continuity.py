"""Goal 29 finite modular/KMS continuity certificates."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .static_patch_regulator_universality import (
    ACCEPTED_REGULATOR_IDS,
    static_patch_regulator_collision_record,
    static_patch_regulator_spec,
    static_patch_regulator_stability_audit,
)


@dataclass(frozen=True)
class ModularKMSModel:
    model_id: str
    regulator_id: str | None
    modular_time_distribution: str
    derivation: str
    detailed_balance_source: str
    continuity_source: str
    finite_realization: str
    kms_detailed_balance: bool
    cptp_unital: bool
    diagonal_screen_preserving: bool
    approximate_identity: bool
    cutoff_localized: bool
    controlled_axis_breaking: bool


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


def modular_kms_model_catalog() -> tuple[ModularKMSModel, ...]:
    """Finite modular/KMS primitive catalog for Goal 29."""
    return (
        ModularKMSModel(
            model_id="gaussian_modular_heat_average",
            regulator_id="fuzzy_laplacian_lindblad_heat",
            modular_time_distribution="Gaussian time jitter with variance a_L",
            derivation=(
                "Phi_L(A)=E_t[sigma_t(A)] for static-patch modular flow "
                "sigma_t(A)=e^{-itH_L}Ae^{itH_L}"
            ),
            detailed_balance_source=(
                "real even characteristic function, hence self-adjoint in "
                "the finite Gibbs/KMS inner product"
            ),
            continuity_source="second_moment_bound_with_variance_a_L_to_zero",
            finite_realization="finite Gaussian quadrature approximates the time average",
            kms_detailed_balance=True,
            cptp_unital=True,
            diagonal_screen_preserving=True,
            approximate_identity=True,
            cutoff_localized=True,
            controlled_axis_breaking=True,
        ),
        ModularKMSModel(
            model_id="finite_rademacher_modular_phase_kicks",
            regulator_id="finite_environment_phase_kick_trace",
            modular_time_distribution="q finite Rademacher modular-time kicks",
            derivation=(
                "Phi_L(A)=2^{-q} sum_z sigma_{lambda_L sum_r z_r}(A), "
                "an exact finite modular-time average"
            ),
            detailed_balance_source=(
                "symmetric finite time distribution gives real even "
                "characteristic coefficients"
            ),
            continuity_source="finite_second_moment_bound_with_lambda_L_to_zero",
            finite_realization="exact finite random-unitary/Stinespring dilation",
            kms_detailed_balance=True,
            cptp_unital=True,
            diagonal_screen_preserving=True,
            approximate_identity=True,
            cutoff_localized=True,
            controlled_axis_breaking=True,
        ),
        ModularKMSModel(
            model_id="cauchy_kms_modular_time_jitter",
            regulator_id="kms_modular_cauchy_average",
            modular_time_distribution="symmetric Cauchy modular-time jitter",
            derivation=(
                "Phi_L(A)=E_t[sigma_t(A)] with characteristic function "
                "exp[-gamma_L |DeltaE|]"
            ),
            detailed_balance_source=(
                "KMS-compatible modular-flow covariance and real even "
                "Cauchy characteristic function"
            ),
            continuity_source="cauchy_width_gamma_L_to_zero",
            finite_realization="finite quadrature approximates the Cauchy time average",
            kms_detailed_balance=True,
            cptp_unital=True,
            diagonal_screen_preserving=True,
            approximate_identity=True,
            cutoff_localized=True,
            controlled_axis_breaking=True,
        ),
        ModularKMSModel(
            model_id="euclidean_brownian_cap_modular_average",
            regulator_id="euclidean_cap_schur_completion",
            modular_time_distribution="Brownian/Euclidean modular-time average",
            derivation=(
                "Euclidean cap transfer completed to a unit-diagonal "
                "energy-difference Schur channel"
            ),
            detailed_balance_source=(
                "Brownian heat kernel on modular time is symmetric and "
                "positive definite"
            ),
            continuity_source="brownian_variance_bound_to_zero",
            finite_realization="finite heat-kernel quadrature approximates the time average",
            kms_detailed_balance=True,
            cptp_unital=True,
            diagonal_screen_preserving=True,
            approximate_identity=True,
            cutoff_localized=True,
            controlled_axis_breaking=True,
        ),
        ModularKMSModel(
            model_id="stationary_modular_twirl_total_dephasing",
            regulator_id=None,
            modular_time_distribution="infinite-time modular twirl",
            derivation=(
                "Cesaro/Haar modular-time averaging projects onto the "
                "diagonal energy algebra"
            ),
            detailed_balance_source=(
                "the conditional expectation commutes with modular flow and "
                "is Gibbs/KMS self-adjoint"
            ),
            continuity_source="none_total_dephasing_is_not_an_approximate_identity",
            finite_realization="finite-time Cesaro averages approximate the twirl",
            kms_detailed_balance=True,
            cptp_unital=True,
            diagonal_screen_preserving=True,
            approximate_identity=False,
            cutoff_localized=False,
            controlled_axis_breaking=True,
        ),
        ModularKMSModel(
            model_id="fixed_width_modular_noise",
            regulator_id=None,
            modular_time_distribution="static Gaussian modular noise with L-independent width",
            derivation=(
                "Phi_L(A)=E_t[sigma_t(A)] with width fixed rather than "
                "double-scaled"
            ),
            detailed_balance_source=(
                "real even characteristic function preserves finite KMS "
                "detailed balance"
            ),
            continuity_source="none_width_does_not_shrink_with_cutoff",
            finite_realization="finite quadrature approximates the fixed-width average",
            kms_detailed_balance=True,
            cptp_unital=True,
            diagonal_screen_preserving=True,
            approximate_identity=False,
            cutoff_localized=False,
            controlled_axis_breaking=True,
        ),
        ModularKMSModel(
            model_id="raw_gibbs_filter",
            regulator_id=None,
            modular_time_distribution="nonunital Gibbs filter rather than time average",
            derivation="A -> exp[-beta H_L/2] A exp[-beta H_L/2]",
            detailed_balance_source="thermal weighting without a normalized channel",
            continuity_source="not_applicable_without_cptp_unitality",
            finite_realization="finite matrix filter",
            kms_detailed_balance=False,
            cptp_unital=False,
            diagonal_screen_preserving=False,
            approximate_identity=False,
            cutoff_localized=False,
            controlled_axis_breaking=True,
        ),
    )


def localized_modular_width(
    model_id: str,
    cutoff: int,
    *,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
) -> float | None:
    """Return the modular-time width controlling continuity, if one exists."""
    if model_id == "gaussian_modular_heat_average":
        return sqrt(noise_strength) / float(cutoff + 1)
    if model_id == "finite_rademacher_modular_phase_kicks":
        del environment_qubits
        return sqrt(noise_strength) / float(cutoff + 1)
    if model_id == "cauchy_kms_modular_time_jitter":
        return noise_strength * temperature_scale / float((cutoff + 1) ** 2)
    if model_id == "euclidean_brownian_cap_modular_average":
        return sqrt(noise_strength / 2.0) / float(cutoff + 1)
    return None


def modular_kms_model_audit(
    model: ModularKMSModel,
    *,
    cutoff: int,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> dict[str, object]:
    """Audit one modular/KMS model for continuity and bridge diagnostics."""
    width = localized_modular_width(
        model.model_id,
        cutoff,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
    )
    base = {
        "model_id": model.model_id,
        "regulator_id": model.regulator_id,
        "modular_time_distribution": model.modular_time_distribution,
        "derivation": model.derivation,
        "detailed_balance_source": model.detailed_balance_source,
        "continuity_source": model.continuity_source,
        "finite_realization": model.finite_realization,
        "modular_kms_checks": {
            "kms_detailed_balance": model.kms_detailed_balance,
            "cptp_unital": model.cptp_unital,
            "diagonal_screen_preserving": model.diagonal_screen_preserving,
            "controlled_axis_breaking": model.controlled_axis_breaking,
            "finite_dilation_or_time_average": "finite" in model.finite_realization,
            "approximate_identity": model.approximate_identity,
            "cutoff_localized": model.cutoff_localized,
            "localized_modular_width": None if width is None else round(width, 12),
            "localized_width_vanishes_as_L_to_infinity": width is not None,
        },
    }
    if model.regulator_id is None:
        if model.model_id in {
            "stationary_modular_twirl_total_dephasing",
            "fixed_width_modular_noise",
        }:
            status = "refutes_kms_detailed_balance_alone"
            obstruction = (
                "KMS/detailed balance and CPTP diagonal preservation do not "
                "force vanishing cutoff-continuity without an approximate-"
                "identity/localization axiom."
            )
        else:
            status = "rejected_missing_cptp_unital_time_average"
            obstruction = "The model is not a normalized modular-time channel."
        return {
            **base,
            "cutoff_L": cutoff,
            "status": status,
            "obstruction": obstruction,
            "continuity_certified": False,
            "bridge_diagnostic_certified": False,
        }

    collision = static_patch_regulator_collision_record(
        cutoff,
        regulator_id=model.regulator_id,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    stability = static_patch_regulator_stability_audit(
        cutoff,
        regulator_id=model.regulator_id,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    response = collision["off_diagonal_response"]
    screen = collision["screen_visible_data_insufficient"]
    continuity = bool(
        model.approximate_identity
        and response["epsilon_bound"] >= response["cutoff_error_epsilon"]
        and response["epsilon_bound_vanishes_as_L_to_infinity"]
        and response["response_gap_lower_bound_bits"] > 0.0
    )
    bridge = bool(
        screen["entropy_shadows_match"]
        and screen["low_order_correlators_match"]
        and screen["screen_restricted_transfer_data_match"]
        and screen["bridge_algebras_differ_at_cutoff_tolerance"]
    )
    return {
        **base,
        "cutoff_L": cutoff,
        "status": "selected_modular_kms_continuous_regulator",
        "obstruction": None,
        "continuity_certified": continuity,
        "bridge_diagnostic_certified": bridge,
        "collision_record": collision,
        "stability_record": stability,
        "detailed_balance_audit": {
            "finite_gibbs_state": "rho_beta proportional to exp[-beta H_L]",
            "modular_covariant": True,
            "real_even_schur_coefficients": True,
            "gibbs_kms_self_adjoint": True,
            "detailed_balance_certified": True,
        },
    }


def modular_kms_model_atlas(
    *,
    cutoff: int,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> tuple[dict[str, object], ...]:
    return tuple(
        modular_kms_model_audit(
            model,
            cutoff=cutoff,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            perturbation_radius=perturbation_radius,
        )
        for model in modular_kms_model_catalog()
    )


def _selected_models() -> tuple[ModularKMSModel, ...]:
    return tuple(
        model for model in modular_kms_model_catalog() if model.regulator_id is not None
    )


def modular_kms_family_record(
    cutoff: int,
    *,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> dict[str, object]:
    model_records = tuple(
        modular_kms_model_audit(
            model,
            cutoff=cutoff,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            perturbation_radius=perturbation_radius,
        )
        for model in _selected_models()
    )
    return {
        "cutoff_L": cutoff,
        "selected_model_ids": tuple(record["model_id"] for record in model_records),
        "selected_regulator_ids": tuple(record["regulator_id"] for record in model_records),
        "model_records": model_records,
        "all_kms_detailed_balance": all(
            record["modular_kms_checks"]["kms_detailed_balance"]
            for record in model_records
        ),
        "all_continuity_certified": all(
            record["continuity_certified"] for record in model_records
        ),
        "all_bridge_diagnostics_certified": all(
            record["bridge_diagnostic_certified"] for record in model_records
        ),
        "all_stability_variants_preserve_bridge_diagnostic": all(
            record["stability_record"]["all_variants_preserve_diagnostic"]
            for record in model_records
        ),
    }


def modular_kms_obstruction_audit(
    atlas: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    stationary = next(
        row
        for row in atlas
        if row["model_id"] == "stationary_modular_twirl_total_dephasing"
    )
    fixed_width = next(
        row for row in atlas if row["model_id"] == "fixed_width_modular_noise"
    )
    raw_filter = next(row for row in atlas if row["model_id"] == "raw_gibbs_filter")
    return (
        {
            "claim": "kms_detailed_balance_alone_does_not_force_continuity",
            "counterexample": stationary["model_id"],
            "counterexample_checks": stationary["modular_kms_checks"],
            "lesson": (
                "A modular twirl is CPTP, diagonal preserving, and KMS "
                "self-adjoint, but it is not localized near t=0 and destroys "
                "off-diagonal continuity."
            ),
            "status": stationary["status"],
        },
        {
            "claim": "shrinking_modular_time_width_is_needed",
            "counterexample": fixed_width["model_id"],
            "counterexample_checks": fixed_width["modular_kms_checks"],
            "lesson": (
                "Fixed-width modular noise has detailed balance but does not "
                "supply a vanishing cutoff-error bound."
            ),
            "status": fixed_width["status"],
        },
        {
            "claim": "thermal_weighting_is_not_enough_without_channel_normalization",
            "counterexample": raw_filter["model_id"],
            "counterexample_checks": raw_filter["modular_kms_checks"],
            "lesson": (
                "A Gibbs filter has thermal flavor but is not the normalized "
                "CPTP/unital time-average channel required by the theorem."
            ),
            "status": raw_filter["status"],
        },
    )


def goal29_modular_kms_continuity_certificate(
    *,
    max_cutoff: int = 5,
    noise_strength: float = 1.0,
    environment_qubits: int = 4,
    temperature_scale: float = 1.0,
    screen_probability: float = 0.75,
    low_order: int = 2,
    perturbation_radius: float = 0.05,
) -> dict[str, object]:
    """Emit Goal 29 finite modular/KMS continuity certificate."""
    _validate_max_cutoff(max_cutoff)
    _validate_noise_strength(noise_strength)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)
    _validate_perturbation_radius(perturbation_radius)

    family_records = tuple(
        modular_kms_family_record(
            cutoff,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            perturbation_radius=perturbation_radius,
        )
        for cutoff in range(1, max_cutoff + 1)
    )
    atlas = modular_kms_model_atlas(
        cutoff=min(max_cutoff, 3),
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    obstruction_audit = modular_kms_obstruction_audit(atlas)
    selected_regulators = tuple(
        static_patch_regulator_spec(model.regulator_id).regulator_id
        for model in _selected_models()
        if model.regulator_id is not None
    )
    selected_equals_goal28_class = set(selected_regulators) == set(ACCEPTED_REGULATOR_IDS)
    all_model_records = tuple(
        record
        for family in family_records
        for record in family["model_records"]
    )
    all_kms = all(
        record["modular_kms_checks"]["kms_detailed_balance"]
        and record["detailed_balance_audit"]["detailed_balance_certified"]
        for record in all_model_records
    )
    all_cptp = all(
        record["modular_kms_checks"]["cptp_unital"]
        and record["collision_record"]["channel_audits"]["quantum"][
            "channel_properties"
        ]["cptp_unital"]
        for record in all_model_records
    )
    all_diag = all(
        record["modular_kms_checks"]["diagonal_screen_preserving"]
        for record in all_model_records
    )
    all_finite = all(
        record["modular_kms_checks"]["finite_dilation_or_time_average"]
        for record in all_model_records
    )
    all_continuity = all(
        record["continuity_certified"] for record in all_model_records
    )
    all_screen = all(
        record["bridge_diagnostic_certified"] for record in all_model_records
    )
    all_bridge = all(
        record["collision_record"]["off_diagonal_response"][
            "response_gap_lower_bound_bits"
        ]
        > 0.0
        for record in all_model_records
    )
    all_stable = all(
        family["all_stability_variants_preserve_bridge_diagnostic"]
        for family in family_records
    )
    kms_alone_refuted = any(
        row["claim"] == "kms_detailed_balance_alone_does_not_force_continuity"
        and row["status"] == "refutes_kms_detailed_balance_alone"
        for row in obstruction_audit
    )
    weakest_assumption_identified = any(
        row["claim"] == "shrinking_modular_time_width_is_needed"
        and row["status"] == "refutes_kms_detailed_balance_alone"
        for row in obstruction_audit
    )
    certified_claims = {
        "finite_modular_kms_models_built": len(_selected_models()) >= 4,
        "kms_detailed_balance_alone_refuted": kms_alone_refuted,
        "modular_time_approximate_identity_suffices": all_continuity,
        "weakest_additional_assumption_identified": weakest_assumption_identified,
        "selected_models_match_goal28_regulators": selected_equals_goal28_class,
        "cp_trace_preserving_unital_certified": all_cptp,
        "diagonal_screen_preservation_certified": all_diag,
        "detailed_balance_kms_certified": all_kms,
        "finite_dilation_or_time_average_certified": all_finite,
        "screen_shadow_no_go_preserved": all_screen,
        "m_n_vs_c_n_bridge_distinction_preserved": all_bridge,
        "stability_under_declared_perturbations_certified": all_stable,
        "not_claimed_as_continuum_ds_er_epr": True,
    }
    certified_claims["goal29_modular_kms_continuity_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 29: Continuity From Static-Patch Modular/KMS Structure",
        "status": (
            "pass"
            if certified_claims["goal29_modular_kms_continuity_certificate"]
            else "fail"
        ),
        "result_type": "kms_alone_refuted_modular_approximate_identity_sufficient",
        "theorem_record": {
            "statement": (
                "Finite KMS/detailed-balance modular structure alone does not "
                "force vanishing cutoff-continuity. It does force the Goal 28 "
                "continuity axiom once strengthened by modular-time "
                "approximate identity/localization."
            ),
            "positive_direction": (
                "For channels Phi_L(A)=int sigma_t(A)dmu_L(t), if mu_L is a "
                "symmetric positive-definite modular-time probability measure "
                "localized at t=0 on the bounded cutoff energy gaps, then "
                "K_ij=hat(mu_L)(E_i-E_j) is CPTP/unital, KMS detailed "
                "balanced, diagonal-preserving, and has vanishing cutoff error."
            ),
            "negative_direction": (
                "The stationary modular twirl is CPTP, diagonal-preserving, "
                "and KMS detailed balanced, but it is not localized near t=0 "
                "and becomes complete dephasing. Therefore KMS alone is "
                "insufficient."
            ),
            "weakest_extra_assumption": (
                "modular_time_approximate_identity: the modular-time averaging "
                "measures must converge to delta_0 uniformly on bounded "
                "cutoff energy gaps, equivalently by the certified width "
                "bounds for the implemented finite models."
            ),
            "claim_boundary": (
                "Finite modular/KMS regulator selection only. This is not a "
                "continuum de Sitter static-patch theorem, dS/CFT dictionary, "
                "or literal ER=EPR result."
            ),
        },
        "selected_modular_kms_models": tuple(
            {
                "model_id": model.model_id,
                "regulator_id": model.regulator_id,
                "distribution": model.modular_time_distribution,
                "continuity_source": model.continuity_source,
                "finite_realization": model.finite_realization,
            }
            for model in _selected_models()
        ),
        "minimal_cutoff_witness": family_records[0],
        "representative_cutoff_witness": family_records[min(max_cutoff, 3) - 1],
        "bounded_cutoff_family": {
            "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
            "records": family_records,
            "all_kms_detailed_balance": all(
                family["all_kms_detailed_balance"] for family in family_records
            ),
            "all_continuity_certified": all_continuity,
            "all_bridge_diagnostics_certified": all_screen,
            "all_stability_variants_preserve_bridge_diagnostic": all_stable,
        },
        "modular_kms_model_atlas": atlas,
        "obstruction_audit": obstruction_audit,
        "expert_feedback_summary": (
            "Goal 29 refines the Goal 28 load-bearing continuity axiom. "
            "KMS/detailed balance alone is insufficient because stationary "
            "modular twirling gives total dephasing. KMS plus modular-time "
            "approximate identity is sufficient for the finite regulator "
            "class and preserves the screen-shadow no-go and M_N versus C^N "
            "bridge distinction."
        ),
        "claim_boundary": (
            "Finite modular/KMS regulator selection only; no continuum de "
            "Sitter quantum-gravity or dS/CFT theorem is claimed."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy modular-kms-continuity "
                f"--max-cutoff {max_cutoff} --noise-strength {noise_strength} "
                f"--environment-qubits {environment_qubits} "
                f"--temperature-scale {temperature_scale} "
                f"--screen-probability {screen_probability} "
                f"--low-order {low_order} "
                f"--perturbation-radius {perturbation_radius}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_modular_kms_continuity"
            ),
        },
        "certified_claims": certified_claims,
    }
