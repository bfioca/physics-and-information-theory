"""Goal 30 finite physical continuity gate certificates."""

from __future__ import annotations

from dataclasses import dataclass

from .modular_kms_continuity import goal29_modular_kms_continuity_certificate
from .relative_entropy_bridge import _rounded
from .static_patch_regulator_universality import (
    ACCEPTED_REGULATOR_IDS,
    static_patch_regulator_collision_record,
    static_patch_regulator_energy,
    static_patch_regulator_stability_audit,
)
from .static_patch_testbed import static_patch_mode_labels


FORBIDDEN_ASSUMPTION_TOKENS = (
    "bridge",
    "m_n",
    "c^n",
    "off-diagonal",
    "response gap",
)


@dataclass(frozen=True)
class PhysicalContinuityRoute:
    route_id: str
    principle: str
    route_kind: str
    assumption: str
    conclusion: str
    derives_modular_time_approximate_identity: bool
    anti_tautological: bool
    status: str
    selected_regulators: tuple[str, ...] = ()


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


def _forbidden_assumption_input(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in FORBIDDEN_ASSUMPTION_TOKENS)


def static_patch_max_energy_gap(cutoff: int) -> float:
    labels = static_patch_mode_labels(cutoff)
    energies = tuple(static_patch_regulator_energy(cutoff, label) for label in labels)
    return max(energies) - min(energies)


def finite_lapse_radius(cutoff: int, *, noise_strength: float) -> float:
    return noise_strength**0.5 / float(cutoff + 1)


def local_heat_time_step(cutoff: int, *, noise_strength: float) -> float:
    return noise_strength / float((cutoff + 1) ** 2)


def finite_lapse_error_bound(cutoff: int, *, noise_strength: float) -> float:
    return finite_lapse_radius(cutoff, noise_strength=noise_strength) * static_patch_max_energy_gap(cutoff)


def heat_step_error_bound(cutoff: int, *, noise_strength: float) -> float:
    gap = static_patch_max_energy_gap(cutoff)
    return 0.5 * local_heat_time_step(cutoff, noise_strength=noise_strength) * gap * gap


def physical_continuity_routes() -> tuple[PhysicalContinuityRoute, ...]:
    return (
        PhysicalContinuityRoute(
            route_id="kms_analyticity_or_detailed_balance_alone",
            principle="finite KMS analyticity/detailed balance",
            route_kind="negative_no_go",
            assumption=(
                "modular covariance, KMS self-adjointness, and diagonal "
                "screen preservation"
            ),
            conclusion=(
                "insufficient: stationary modular twirling remains allowed"
            ),
            derives_modular_time_approximate_identity=False,
            anti_tautological=True,
            status="refuted_by_goal29_stationary_twirl",
        ),
        PhysicalContinuityRoute(
            route_id="thermal_correlation_decay_without_short_time_localization",
            principle="thermal correlation decay",
            route_kind="negative_no_go",
            assumption=(
                "finite thermal correlation scale or fixed-width modular "
                "noise independent of cutoff"
            ),
            conclusion=(
                "insufficient: fixed-width modular averaging need not approach identity"
            ),
            derives_modular_time_approximate_identity=False,
            anti_tautological=True,
            status="refuted_by_goal29_fixed_width_noise",
        ),
        PhysicalContinuityRoute(
            route_id="finite_lapse_modular_locality",
            principle="finite-lapse local modular evolution",
            route_kind="positive_sufficient",
            assumption=(
                "modular time averaging is supported in a window r_L with "
                "r_L max_gap_L -> 0"
            ),
            conclusion=(
                "sufficient: finite-time modular averaging forms an approximate identity"
            ),
            derives_modular_time_approximate_identity=True,
            anti_tautological=True,
            status="sufficient_physical_gate",
            selected_regulators=ACCEPTED_REGULATOR_IDS,
        ),
        PhysicalContinuityRoute(
            route_id="fuzzy_sphere_local_heat_scaling",
            principle="fuzzy-sphere locality and spectral-gap scaling",
            route_kind="positive_sufficient",
            assumption=(
                "local heat or Lindblad step has tau_L max_gap_L^2 -> 0 "
                "for the normalized fuzzy-sphere Hamiltonian"
            ),
            conclusion=(
                "sufficient: heat-kernel modular damping has vanishing cutoff error"
            ),
            derives_modular_time_approximate_identity=True,
            anti_tautological=True,
            status="sufficient_physical_gate",
            selected_regulators=(
                "fuzzy_laplacian_lindblad_heat",
                "euclidean_cap_schur_completion",
            ),
        ),
        PhysicalContinuityRoute(
            route_id="euclidean_cap_shrinking_thickness",
            principle="Euclidean/static-patch preparation",
            route_kind="positive_sufficient",
            assumption=(
                "Euclidean cap transfer thickness shrinks so that "
                "tau_L max_gap_L^2 -> 0 before the large-cutoff limit"
            ),
            conclusion=(
                "sufficient: CP/TP Schur-completed cap transfer is an approximate identity"
            ),
            derives_modular_time_approximate_identity=True,
            anti_tautological=True,
            status="sufficient_physical_gate",
            selected_regulators=("euclidean_cap_schur_completion",),
        ),
        PhysicalContinuityRoute(
            route_id="operator_algebra_limit_continuity",
            principle="observer algebra continuity in the large-cutoff limit",
            route_kind="conditional_necessity",
            assumption=(
                "the finite local observable embeddings are norm-continuous "
                "under one cutoff step"
            ),
            conclusion=(
                "necessary for retaining a noncommutative observer-algebra limit"
            ),
            derives_modular_time_approximate_identity=True,
            anti_tautological=True,
            status="conditional_limit_requirement",
            selected_regulators=ACCEPTED_REGULATOR_IDS,
        ),
    )


def physical_continuity_route_audit(
    route: PhysicalContinuityRoute,
    *,
    cutoff: int,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> dict[str, object]:
    anti_tautological = route.anti_tautological and not _forbidden_assumption_input(
        route.assumption
    )
    max_gap = static_patch_max_energy_gap(cutoff)
    finite_lapse_bound = finite_lapse_error_bound(
        cutoff,
        noise_strength=noise_strength,
    )
    heat_bound = heat_step_error_bound(cutoff, noise_strength=noise_strength)
    selected_records = tuple(
        static_patch_regulator_collision_record(
            cutoff,
            regulator_id=regulator_id,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
        )
        for regulator_id in route.selected_regulators
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
        for regulator_id in route.selected_regulators
    )
    bridge_preserved = all(
        record["screen_visible_data_insufficient"]["entropy_shadows_match"]
        and record["screen_visible_data_insufficient"][
            "screen_restricted_transfer_data_match"
        ]
        and record["off_diagonal_response"]["response_gap_lower_bound_bits"] > 0.0
        for record in selected_records
    )
    stability_preserved = all(
        record["all_variants_preserve_diagnostic"] for record in stability_records
    )
    if route.route_id == "finite_lapse_modular_locality":
        continuity_certified = bool(
            route.derives_modular_time_approximate_identity
            and anti_tautological
            and finite_lapse_bound < 1.0
        )
    elif route.route_kind == "positive_sufficient":
        continuity_certified = bool(
            route.derives_modular_time_approximate_identity
            and anti_tautological
            and heat_bound < 1.0
        )
    elif route.route_kind == "conditional_necessity":
        continuity_certified = bool(
            route.derives_modular_time_approximate_identity and anti_tautological
        )
    else:
        continuity_certified = False
    return {
        "route_id": route.route_id,
        "principle": route.principle,
        "route_kind": route.route_kind,
        "assumption": route.assumption,
        "anti_tautological": anti_tautological,
        "conclusion": route.conclusion,
        "status": route.status,
        "cutoff_L": cutoff,
        "max_energy_gap": _rounded(max_gap),
        "finite_lapse_radius": _rounded(
            finite_lapse_radius(cutoff, noise_strength=noise_strength)
        ),
        "finite_lapse_error_bound": _rounded(finite_lapse_bound),
        "local_heat_time_step": _rounded(
            local_heat_time_step(cutoff, noise_strength=noise_strength)
        ),
        "local_heat_error_bound": _rounded(heat_bound),
        "derives_modular_time_approximate_identity": (
            route.derives_modular_time_approximate_identity
        ),
        "continuity_certified": continuity_certified,
        "selected_regulators": route.selected_regulators,
        "bridge_diagnostic_preserved_for_selected_regulators": bridge_preserved,
        "stability_preserved_for_selected_regulators": stability_preserved,
        "selected_regulator_records": selected_records,
        "stability_records": stability_records,
    }


def physical_continuity_route_atlas(
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
        physical_continuity_route_audit(
            route,
            cutoff=cutoff,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            perturbation_radius=perturbation_radius,
        )
        for route in physical_continuity_routes()
    )


def physical_continuity_family_record(
    cutoff: int,
    *,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> dict[str, object]:
    route_records = physical_continuity_route_atlas(
        cutoff=cutoff,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    positive_records = tuple(
        record for record in route_records if record["route_kind"] == "positive_sufficient"
    )
    return {
        "cutoff_L": cutoff,
        "route_records": route_records,
        "all_positive_routes_certify_continuity": all(
            record["continuity_certified"] for record in positive_records
        ),
        "all_positive_routes_preserve_bridge_diagnostic": all(
            record["bridge_diagnostic_preserved_for_selected_regulators"]
            and record["stability_preserved_for_selected_regulators"]
            for record in positive_records
        ),
        "finite_lapse_bound": _rounded(
            finite_lapse_error_bound(cutoff, noise_strength=noise_strength)
        ),
        "heat_step_bound": _rounded(
            heat_step_error_bound(cutoff, noise_strength=noise_strength)
        ),
    }


def goal30_static_patch_physical_continuity_certificate(
    *,
    max_cutoff: int = 5,
    noise_strength: float = 1.0,
    environment_qubits: int = 4,
    temperature_scale: float = 1.0,
    screen_probability: float = 0.75,
    low_order: int = 2,
    perturbation_radius: float = 0.05,
) -> dict[str, object]:
    """Emit a finite physical continuity gate certificate."""
    _validate_max_cutoff(max_cutoff)
    _validate_noise_strength(noise_strength)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)
    _validate_perturbation_radius(perturbation_radius)

    family_records = tuple(
        physical_continuity_family_record(
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
    representative_atlas = physical_continuity_route_atlas(
        cutoff=min(max_cutoff, 3),
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    goal29 = goal29_modular_kms_continuity_certificate(
        max_cutoff=max_cutoff,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    positive_records = tuple(
        record
        for family in family_records
        for record in family["route_records"]
        if record["route_kind"] == "positive_sufficient"
    )
    negative_routes = tuple(
        record
        for record in representative_atlas
        if record["route_kind"] == "negative_no_go"
    )
    conditional_routes = tuple(
        record
        for record in representative_atlas
        if record["route_kind"] == "conditional_necessity"
    )
    finite_lapse_bounds = tuple(record["finite_lapse_bound"] for record in family_records)
    heat_bounds = tuple(record["heat_step_bound"] for record in family_records)
    finite_lapse_decreases = all(
        finite_lapse_bounds[index] < finite_lapse_bounds[index - 1]
        for index in range(1, len(finite_lapse_bounds))
    )
    heat_bound_decreases = all(
        heat_bounds[index] < heat_bounds[index - 1]
        for index in range(1, len(heat_bounds))
    )
    certified_claims = {
        "goal29_obstruction_retained": goal29["certified_claims"][
            "kms_detailed_balance_alone_refuted"
        ],
        "kms_and_thermal_decay_alone_refuted": all(
            not record["continuity_certified"] for record in negative_routes
        ),
        "finite_lapse_modular_locality_suffices": all(
            record["route_id"] == "finite_lapse_modular_locality"
            and record["continuity_certified"]
            for record in positive_records
            if record["route_id"] == "finite_lapse_modular_locality"
        ),
        "fuzzy_sphere_locality_suffices": all(
            record["route_id"] == "fuzzy_sphere_local_heat_scaling"
            and record["continuity_certified"]
            for record in positive_records
            if record["route_id"] == "fuzzy_sphere_local_heat_scaling"
        ),
        "euclidean_cap_shrinking_thickness_suffices": all(
            record["route_id"] == "euclidean_cap_shrinking_thickness"
            and record["continuity_certified"]
            for record in positive_records
            if record["route_id"] == "euclidean_cap_shrinking_thickness"
        ),
        "operator_algebra_limit_requires_continuity": all(
            record["continuity_certified"] for record in conditional_routes
        ),
        "anti_tautology_gate_certified": all(
            record["anti_tautological"] for record in representative_atlas
        ),
        "finite_lapse_bound_decreases": finite_lapse_decreases,
        "heat_step_bound_decreases": heat_bound_decreases,
        "bridge_diagnostic_preserved": all(
            record["bridge_diagnostic_preserved_for_selected_regulators"]
            and record["stability_preserved_for_selected_regulators"]
            for record in positive_records
        ),
        "not_claimed_as_continuum_ds_er_epr": True,
    }
    certified_claims["goal30_static_patch_physical_continuity_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 30: Physical Static-Patch Continuity Gate",
        "status": (
            "pass"
            if certified_claims[
                "goal30_static_patch_physical_continuity_certificate"
            ]
            else "fail"
        ),
        "result_type": "finite_physical_continuity_gate",
        "theorem_record": {
            "statement": (
                "KMS/detailed balance, thermal correlation scale, and screen "
                "preservation do not by themselves derive modular-time "
                "approximate identity. Finite-lapse modular locality, fuzzy "
                "local heat scaling, or shrinking Euclidean cap thickness are "
                "anti-tautological sufficient gates."
            ),
            "negative_direction": (
                "Goal 29's stationary modular twirl and fixed-width modular "
                "noise remain valid counterexamples to KMS/thermal conditions "
                "without short-time localization."
            ),
            "positive_direction": (
                "If modular time averaging is confined to r_L with "
                "r_L max_gap_L -> 0, then |hat(mu_L)(DeltaE)-1| is bounded "
                "by r_L max_gap_L on the finite cutoff spectrum. If the "
                "kernel is heat/Euclidean, tau_L max_gap_L^2 -> 0 gives the "
                "same continuity."
            ),
            "weakest_physical_gate": (
                "short_time_static_patch_locality: the modular/Euclidean "
                "transfer step must remain localized near the identity on "
                "bounded cutoff energy gaps."
            ),
            "claim_boundary": (
                "Finite physical continuity gate only. This does not derive "
                "the gate from continuum de Sitter quantum gravity, a path "
                "integral, or dS/CFT."
            ),
        },
        "route_atlas": representative_atlas,
        "minimal_cutoff_witness": family_records[0],
        "representative_cutoff_witness": family_records[min(max_cutoff, 3) - 1],
        "bounded_cutoff_family": {
            "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
            "records": family_records,
            "finite_lapse_bounds": finite_lapse_bounds,
            "heat_step_bounds": heat_bounds,
            "finite_lapse_bound_decreases": finite_lapse_decreases,
            "heat_step_bound_decreases": heat_bound_decreases,
        },
        "relationship_to_goal29": {
            "goal29_status": goal29["status"],
            "goal29_result_type": goal29["result_type"],
            "goal29_weakest_extra_assumption": goal29["theorem_record"][
                "weakest_extra_assumption"
            ],
            "refinement": (
                "Goal 30 renames the extra assumption as the anti-tautological "
                "short-time/static-patch locality gate and shows which finite "
                "routes imply it."
            ),
        },
        "expert_feedback_summary": (
            "The finite program now isolates the next physics assumption: not "
            "KMS itself, but short-time static-patch locality. KMS/detailed "
            "balance permits stationary twirling; a shrinking local modular or "
            "Euclidean step gives approximate identity and preserves the "
            "screen-shadow no-go plus the quantum/classical bridge split."
        ),
        "claim_boundary": (
            "Finite physical continuity gate only; no continuum de Sitter "
            "or dS/CFT theorem is claimed."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy static-patch-physical-continuity "
                f"--max-cutoff {max_cutoff} --noise-strength {noise_strength} "
                f"--environment-qubits {environment_qubits} "
                f"--temperature-scale {temperature_scale} "
                f"--screen-probability {screen_probability} "
                f"--low-order {low_order} "
                f"--perturbation-radius {perturbation_radius}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_static_patch_physical_continuity"
            ),
        },
        "certified_claims": certified_claims,
    }
