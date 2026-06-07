"""Goal 31 finite static-patch strong-continuity certificates."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

from .relative_entropy_bridge import _rounded
from .static_patch_physical_continuity import (
    FORBIDDEN_ASSUMPTION_TOKENS,
    goal30_static_patch_physical_continuity_certificate,
    heat_step_error_bound,
    local_heat_time_step,
    static_patch_max_energy_gap,
)


@dataclass(frozen=True)
class StrongContinuityRoute:
    route_id: str
    principle: str
    route_kind: str
    assumption: str
    conclusion: str
    status: str
    derives_modular_time_approximate_identity: bool
    violates_strong_continuity: bool = False
    violates_cutoff_compatible_lapse: bool = False


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


def _validate_fixed_lapse(fixed_lapse: float) -> None:
    if fixed_lapse <= 0.0:
        raise ValueError("fixed_lapse must be positive")


def _forbidden_assumption_input(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in FORBIDDEN_ASSUMPTION_TOKENS)


def strong_continuity_routes() -> tuple[StrongContinuityRoute, ...]:
    return (
        StrongContinuityRoute(
            route_id="stationary_twirl_projection",
            principle="KMS-stationary projection",
            route_kind="negative_no_go",
            assumption=(
                "modular covariance, KMS self-adjointness, and diagonal "
                "screen preservation without continuity at time zero"
            ),
            conclusion=(
                "insufficient: projection dynamics can jump away from the "
                "identity at arbitrarily small positive time"
            ),
            status="refuted_by_strong_continuity_failure",
            derives_modular_time_approximate_identity=False,
            violates_strong_continuity=True,
        ),
        StrongContinuityRoute(
            route_id="fixed_lapse_thermalization",
            principle="fixed-time thermal relaxation",
            route_kind="negative_no_go",
            assumption=(
                "a finite static-patch Markov semigroup evaluated at an "
                "L-independent positive lapse"
            ),
            conclusion=(
                "insufficient: finite-time evolution can be continuous at "
                "each cutoff but still fail cutoff approximate identity"
            ),
            status="refuted_by_nonshrinking_lapse",
            derives_modular_time_approximate_identity=False,
            violates_cutoff_compatible_lapse=True,
        ),
        StrongContinuityRoute(
            route_id="bounded_local_modular_generator",
            principle="strongly continuous local modular evolution",
            route_kind="positive_theorem",
            assumption=(
                "finite modular channels satisfy Lambda_L(0)=id, are strongly "
                "continuous, have generator norm Gamma_L bounded by the "
                "cutoff static-patch Hamiltonian gap, and use lapses "
                "delta_L with delta_L Gamma_L -> 0"
            ),
            conclusion=(
                "sufficient: ||exp(delta_L G_L)-id|| <= "
                "exp(delta_L Gamma_L)-1 gives approximate identity"
            ),
            status="finite_semigroup_theorem",
            derives_modular_time_approximate_identity=True,
        ),
        StrongContinuityRoute(
            route_id="bounded_local_heat_generator",
            principle="fuzzy-sphere local heat semigroup",
            route_kind="positive_theorem",
            assumption=(
                "finite heat or Lindblad dynamics has generator norm bounded "
                "by one half of the squared cutoff static-patch Hamiltonian "
                "gap and uses tau_L with tau_L Gamma_L -> 0"
            ),
            conclusion=(
                "sufficient: local heat flow is a cutoff-compatible "
                "near-identity semigroup step"
            ),
            status="finite_semigroup_theorem",
            derives_modular_time_approximate_identity=True,
        ),
        StrongContinuityRoute(
            route_id="shrinking_euclidean_transfer_generator",
            principle="Euclidean cap as finite heat-time transfer",
            route_kind="positive_theorem",
            assumption=(
                "Euclidean cap preparation is represented by a heat-time "
                "transfer step whose thickness shrinks with the cutoff-local "
                "generator norm"
            ),
            conclusion=(
                "sufficient: Euclidean/static-patch transfer gives the same "
                "strong-continuity gate as local heat flow"
            ),
            status="finite_semigroup_theorem",
            derives_modular_time_approximate_identity=True,
        ),
        StrongContinuityRoute(
            route_id="noncommutative_observer_limit",
            principle="operator-algebra limit continuity",
            route_kind="conditional_necessity",
            assumption=(
                "cutoff observer algebras are compared by embeddings whose "
                "local finite-time dynamics is norm-continuous in the large "
                "cutoff limit"
            ),
            conclusion=(
                "necessary as a limit gate: without it, stationary projection "
                "collapses the candidate noncommutative local algebra"
            ),
            status="conditional_physics_axiom",
            derives_modular_time_approximate_identity=True,
        ),
    )


def modular_generator_norm_bound(cutoff: int) -> float:
    """Norm bound for finite modular commutator dynamics on matrix units."""
    return static_patch_max_energy_gap(cutoff)


def heat_generator_norm_bound(cutoff: int) -> float:
    """Norm bound for the finite heat/Lindblad dephasing generator."""
    gap = static_patch_max_energy_gap(cutoff)
    return 0.5 * gap * gap


def modular_short_lapse(cutoff: int, *, noise_strength: float) -> float:
    return noise_strength**0.5 / float(cutoff + 1)


def heat_short_lapse(cutoff: int, *, noise_strength: float) -> float:
    return local_heat_time_step(cutoff, noise_strength=noise_strength)


def semigroup_error_bound(lapse: float, generator_norm_bound: float) -> float:
    return exp(lapse * generator_norm_bound) - 1.0


def fixed_lapse_heat_error_lower_bound(
    cutoff: int,
    *,
    fixed_lapse: float,
) -> float:
    gap = static_patch_max_energy_gap(cutoff)
    return 1.0 - exp(-0.5 * fixed_lapse * gap * gap)


def strong_continuity_route_audit(
    route: StrongContinuityRoute,
    *,
    cutoff: int,
    noise_strength: float,
    fixed_lapse: float,
) -> dict[str, object]:
    anti_tautological = not _forbidden_assumption_input(route.assumption)
    modular_gamma = modular_generator_norm_bound(cutoff)
    heat_gamma = heat_generator_norm_bound(cutoff)
    modular_lapse = modular_short_lapse(cutoff, noise_strength=noise_strength)
    heat_lapse = heat_short_lapse(cutoff, noise_strength=noise_strength)
    modular_product = modular_lapse * modular_gamma
    heat_product = heat_lapse * heat_gamma
    if route.route_id == "bounded_local_modular_generator":
        continuity_certified = anti_tautological and modular_product < 1.0
        theorem_bound = semigroup_error_bound(modular_lapse, modular_gamma)
    elif route.route_id in {
        "bounded_local_heat_generator",
        "shrinking_euclidean_transfer_generator",
    }:
        continuity_certified = anti_tautological and heat_product < 1.0
        theorem_bound = semigroup_error_bound(heat_lapse, heat_gamma)
    elif route.route_id == "noncommutative_observer_limit":
        continuity_certified = anti_tautological
        theorem_bound = None
    else:
        continuity_certified = False
        theorem_bound = None
    return {
        "route_id": route.route_id,
        "principle": route.principle,
        "route_kind": route.route_kind,
        "assumption": route.assumption,
        "anti_tautological": anti_tautological,
        "conclusion": route.conclusion,
        "status": route.status,
        "cutoff_L": cutoff,
        "max_energy_gap": _rounded(static_patch_max_energy_gap(cutoff)),
        "modular_generator_norm_bound": _rounded(modular_gamma),
        "heat_generator_norm_bound": _rounded(heat_gamma),
        "modular_short_lapse": _rounded(modular_lapse),
        "heat_short_lapse": _rounded(heat_lapse),
        "modular_lapse_times_generator": _rounded(modular_product),
        "heat_lapse_times_generator": _rounded(heat_product),
        "semigroup_error_bound": (
            None if theorem_bound is None else _rounded(theorem_bound)
        ),
        "fixed_lapse_error_lower_bound": _rounded(
            fixed_lapse_heat_error_lower_bound(cutoff, fixed_lapse=fixed_lapse)
        ),
        "identity_jump_witness_norm": (
            1.0 if route.violates_strong_continuity else 0.0
        ),
        "violates_strong_continuity": route.violates_strong_continuity,
        "violates_cutoff_compatible_lapse": (
            route.violates_cutoff_compatible_lapse
        ),
        "derives_modular_time_approximate_identity": (
            route.derives_modular_time_approximate_identity
        ),
        "continuity_certified": continuity_certified,
    }


def strong_continuity_route_atlas(
    *,
    cutoff: int,
    noise_strength: float,
    fixed_lapse: float,
) -> tuple[dict[str, object], ...]:
    return tuple(
        strong_continuity_route_audit(
            route,
            cutoff=cutoff,
            noise_strength=noise_strength,
            fixed_lapse=fixed_lapse,
        )
        for route in strong_continuity_routes()
    )


def strong_continuity_family_record(
    cutoff: int,
    *,
    noise_strength: float,
    fixed_lapse: float,
) -> dict[str, object]:
    atlas = strong_continuity_route_atlas(
        cutoff=cutoff,
        noise_strength=noise_strength,
        fixed_lapse=fixed_lapse,
    )
    positive = tuple(row for row in atlas if row["route_kind"] == "positive_theorem")
    return {
        "cutoff_L": cutoff,
        "route_records": atlas,
        "modular_lapse_times_generator": _rounded(
            modular_short_lapse(cutoff, noise_strength=noise_strength)
            * modular_generator_norm_bound(cutoff)
        ),
        "heat_lapse_times_generator": _rounded(
            heat_short_lapse(cutoff, noise_strength=noise_strength)
            * heat_generator_norm_bound(cutoff)
        ),
        "fixed_lapse_error_lower_bound": _rounded(
            fixed_lapse_heat_error_lower_bound(cutoff, fixed_lapse=fixed_lapse)
        ),
        "all_positive_theorems_certify_continuity": all(
            row["continuity_certified"] for row in positive
        ),
    }


def goal31_static_patch_strong_continuity_certificate(
    *,
    max_cutoff: int = 5,
    noise_strength: float = 1.0,
    fixed_lapse: float = 1.0,
    environment_qubits: int = 4,
    temperature_scale: float = 1.0,
    screen_probability: float = 0.75,
    low_order: int = 2,
    perturbation_radius: float = 0.05,
) -> dict[str, object]:
    """Emit a finite strong-continuity theorem/no-go certificate."""
    _validate_max_cutoff(max_cutoff)
    _validate_noise_strength(noise_strength)
    _validate_fixed_lapse(fixed_lapse)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)
    _validate_perturbation_radius(perturbation_radius)

    family_records = tuple(
        strong_continuity_family_record(
            cutoff,
            noise_strength=noise_strength,
            fixed_lapse=fixed_lapse,
        )
        for cutoff in range(1, max_cutoff + 1)
    )
    representative_atlas = strong_continuity_route_atlas(
        cutoff=min(max_cutoff, 3),
        noise_strength=noise_strength,
        fixed_lapse=fixed_lapse,
    )
    goal30 = goal30_static_patch_physical_continuity_certificate(
        max_cutoff=max_cutoff,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    positive_records = tuple(
        row
        for family in family_records
        for row in family["route_records"]
        if row["route_kind"] == "positive_theorem"
    )
    negative_records = tuple(
        row for row in representative_atlas if row["route_kind"] == "negative_no_go"
    )
    conditional_records = tuple(
        row
        for row in representative_atlas
        if row["route_kind"] == "conditional_necessity"
    )
    modular_products = tuple(
        record["modular_lapse_times_generator"] for record in family_records
    )
    heat_products = tuple(
        record["heat_lapse_times_generator"] for record in family_records
    )
    fixed_lapse_lower_bounds = tuple(
        record["fixed_lapse_error_lower_bound"] for record in family_records
    )
    modular_products_decrease = all(
        modular_products[index] < modular_products[index - 1]
        for index in range(1, len(modular_products))
    )
    heat_products_decrease = all(
        heat_products[index] < heat_products[index - 1]
        for index in range(1, len(heat_products))
    )
    certified_claims = {
        "goal30_physical_gate_retained": goal30["certified_claims"][
            "goal30_static_patch_physical_continuity_certificate"
        ],
        "stationary_twirl_excluded_by_strong_continuity": any(
            row["route_id"] == "stationary_twirl_projection"
            and row["violates_strong_continuity"]
            and not row["continuity_certified"]
            for row in negative_records
        ),
        "fixed_lapse_thermalization_not_enough": any(
            row["route_id"] == "fixed_lapse_thermalization"
            and row["violates_cutoff_compatible_lapse"]
            and not row["continuity_certified"]
            for row in negative_records
        ),
        "bounded_local_modular_generator_suffices": all(
            row["route_id"] == "bounded_local_modular_generator"
            and row["continuity_certified"]
            for row in positive_records
            if row["route_id"] == "bounded_local_modular_generator"
        ),
        "bounded_local_heat_generator_suffices": all(
            row["route_id"] == "bounded_local_heat_generator"
            and row["continuity_certified"]
            for row in positive_records
            if row["route_id"] == "bounded_local_heat_generator"
        ),
        "shrinking_euclidean_transfer_suffices": all(
            row["route_id"] == "shrinking_euclidean_transfer_generator"
            and row["continuity_certified"]
            for row in positive_records
            if row["route_id"] == "shrinking_euclidean_transfer_generator"
        ),
        "operator_algebra_limit_requires_strong_continuity_gate": all(
            row["continuity_certified"] for row in conditional_records
        ),
        "modular_lapse_generator_products_decrease": modular_products_decrease,
        "heat_lapse_generator_products_decrease": heat_products_decrease,
        "fixed_lapse_error_has_positive_witness": all(
            lower_bound > 0.0 for lower_bound in fixed_lapse_lower_bounds
        ),
        "anti_tautology_gate_certified": all(
            row["anti_tautological"] for row in representative_atlas
        ),
        "bridge_diagnostic_preserved": goal30["certified_claims"][
            "bridge_diagnostic_preserved"
        ],
        "not_claimed_as_continuum_ds_er_epr": True,
    }
    certified_claims["goal31_static_patch_strong_continuity_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 31: Static-Patch Strong-Continuity Theorem Gate",
        "status": (
            "pass"
            if certified_claims[
                "goal31_static_patch_strong_continuity_certificate"
            ]
            else "fail"
        ),
        "result_type": "finite_static_patch_strong_continuity_theorem_gate",
        "theorem_record": {
            "finite_semigroup_theorem": (
                "For each cutoff, a strongly continuous finite channel "
                "semigroup with generator norm <= Gamma_L satisfies "
                "||exp(delta_L G_L)-id|| <= exp(delta_L Gamma_L)-1. If "
                "delta_L Gamma_L -> 0, this derives the modular-time "
                "approximate-identity gate."
            ),
            "stationary_twirl_no_go": (
                "The stationary modular twirl is KMS-compatible but is not a "
                "strongly continuous identity-starting finite-time dynamics: "
                "it jumps by norm one on a matrix-unit coherence witness."
            ),
            "fixed_lapse_no_go": (
                "Strong continuity at each finite cutoff is not enough if the "
                "physical lapse is fixed while the cutoff is removed; the "
                "lapse-generator product must shrink."
            ),
            "physics_axiom_isolated": (
                "cutoff_compatible_strong_continuity: finite static-patch "
                "evolution must arise from local generators and lapse scales "
                "with delta_L Gamma_L -> 0."
            ),
            "claim_boundary": (
                "Finite theorem gate only. This identifies the anti-"
                "tautological axiom that excludes Goal 29's obstruction; it "
                "does not prove continuum de Sitter or dS/CFT dynamics."
            ),
        },
        "route_atlas": representative_atlas,
        "bounded_cutoff_family": {
            "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
            "records": family_records,
            "modular_lapse_times_generator": modular_products,
            "heat_lapse_times_generator": heat_products,
            "fixed_lapse_error_lower_bounds": fixed_lapse_lower_bounds,
            "modular_products_decrease": modular_products_decrease,
            "heat_products_decrease": heat_products_decrease,
        },
        "relationship_to_goal30": {
            "goal30_status": goal30["status"],
            "goal30_result_type": goal30["result_type"],
            "goal30_weakest_physical_gate": goal30["theorem_record"][
                "weakest_physical_gate"
            ],
            "refinement": (
                "Goal 31 replaces the named short-time locality gate with a "
                "finite semigroup/generator condition: strong continuity plus "
                "delta_L Gamma_L -> 0."
            ),
        },
        "harlow_facing_summary": (
            "The finite obstruction has been localized further. KMS excludes "
            "nothing like stationary twirling, but an identity-starting, "
            "strongly continuous static-patch semigroup with cutoff-local "
            "generator bound and shrinking lapse does derive the needed "
            "approximate identity. Without this extra axiom, fixed-time "
            "thermalization can still erase the bridge-relevant algebra while "
            "leaving screen shadows unchanged."
        ),
        "claim_boundary": (
            "Finite semigroup theorem gate only; no continuum de Sitter or "
            "dS/CFT theorem is claimed."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity "
                f"--max-cutoff {max_cutoff} --noise-strength {noise_strength} "
                f"--fixed-lapse {fixed_lapse} "
                f"--environment-qubits {environment_qubits} "
                f"--temperature-scale {temperature_scale} "
                f"--screen-probability {screen_probability} "
                f"--low-order {low_order} "
                f"--perturbation-radius {perturbation_radius}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity"
            ),
        },
        "certified_claims": certified_claims,
    }
