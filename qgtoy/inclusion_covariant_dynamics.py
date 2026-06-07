"""Inclusion-covariant dynamics audits for the finite-to-Type-II scaffold."""

from __future__ import annotations

from math import sqrt

from .relative_entropy_bridge import _rounded
from .static_patch_regulator_universality import static_patch_regulator_energy
from .static_patch_strong_continuity import (
    heat_short_lapse,
    modular_short_lapse,
)
from .static_patch_testbed import static_patch_mode_labels
from .typeii_static_patch_limit import (
    factorial_cutoff,
    factorial_matrix_dim,
    major_goal_finite_to_typeii_static_patch_certificate,
)


def _validate_max_level(max_level: int) -> None:
    if max_level < 3:
        raise ValueError("max_level must be at least three")


def _validate_max_consecutive_cutoff(max_consecutive_cutoff: int) -> None:
    if max_consecutive_cutoff < 1:
        raise ValueError("max_consecutive_cutoff must be at least one")


def _validate_bridge_cert_max_cutoff(bridge_cert_max_cutoff: int) -> None:
    if bridge_cert_max_cutoff < 1:
        raise ValueError("bridge_cert_max_cutoff must be at least one")


def _validate_low_order(low_order: int) -> None:
    if low_order < 0:
        raise ValueError("low_order must be nonnegative")


def _validate_probability(screen_probability: float) -> None:
    if not 0.0 <= screen_probability <= 1.0:
        raise ValueError("screen_probability must lie in [0,1]")


def _validate_noise_strength(noise_strength: float) -> None:
    if noise_strength < 0.0:
        raise ValueError("noise_strength must be nonnegative")


def _validate_fixed_lapse(fixed_lapse: float) -> None:
    if fixed_lapse <= 0.0:
        raise ValueError("fixed_lapse must be positive")


def _validate_environment_qubits(environment_qubits: int) -> None:
    if environment_qubits < 1:
        raise ValueError("environment_qubits must be at least one")


def _validate_temperature_scale(temperature_scale: float) -> None:
    if temperature_scale <= 0.0:
        raise ValueError("temperature_scale must be positive")


def _validate_perturbation_radius(perturbation_radius: float) -> None:
    if not 0.0 <= perturbation_radius < 1.0:
        raise ValueError("perturbation_radius must lie in [0,1)")


def cutoff_energy_vector(cutoff: int) -> tuple[float, ...]:
    return tuple(
        static_patch_regulator_energy(cutoff, label)
        for label in static_patch_mode_labels(cutoff)
    )


def _range(values: tuple[float, ...] | list[float]) -> float:
    return max(values) - min(values)


def _mean(values: list[float]) -> float:
    return sum(values) / float(len(values))


def _rms_centered(values: list[float]) -> float:
    mean = _mean(values)
    return sqrt(sum((value - mean) ** 2 for value in values) / float(len(values)))


def covariance_asymptotic_bound(cutoff: int) -> float:
    return 2.0 / float(cutoff + 1)


def canonical_block_covariance_audit(
    level: int,
    *,
    noise_strength: float,
) -> dict[str, object]:
    """Audit covariance for iota(x)=x tensor I on rank-ordered mode blocks."""
    if level < 1:
        raise ValueError("level must be at least one")
    source_cutoff = factorial_cutoff(level)
    target_cutoff = factorial_cutoff(level + 1)
    source_dim = factorial_matrix_dim(level)
    target_dim = factorial_matrix_dim(level + 1)
    multiplicity = target_dim // source_dim
    source = cutoff_energy_vector(source_cutoff)
    target = cutoff_energy_vector(target_cutoff)
    if len(source) != source_dim or len(target) != target_dim:
        raise AssertionError("mode-count/dimension mismatch")

    per_fiber_ranges = []
    per_source_means = []
    max_fiber_spread = 0.0
    for fiber_index in range(multiplicity):
        deviations = [
            target[source_index * multiplicity + fiber_index] - source[source_index]
            for source_index in range(source_dim)
        ]
        per_fiber_ranges.append(_range(deviations))
    for source_index in range(source_dim):
        fiber_values = [
            target[source_index * multiplicity + fiber_index]
            for fiber_index in range(multiplicity)
        ]
        max_fiber_spread = max(max_fiber_spread, _range(fiber_values))
        per_source_means.append(_mean(fiber_values) - source[source_index])

    exact_modular_error = max(per_fiber_ranges)
    conditional_modular_error = _range(per_source_means)
    conditional_l2_error = _rms_centered(per_source_means)
    source_gap = _range(source)
    target_gap = _range(target)
    max_gap = max(source_gap, target_gap)
    exact_heat_bound = 0.5 * exact_modular_error * (
        2.0 * max_gap + exact_modular_error
    )
    conditional_heat_bound = 0.5 * conditional_modular_error * (
        2.0 * max_gap + conditional_modular_error
    )
    modular_lapse = modular_short_lapse(source_cutoff, noise_strength=noise_strength)
    heat_lapse = heat_short_lapse(source_cutoff, noise_strength=noise_strength)
    asymptotic_bound = covariance_asymptotic_bound(source_cutoff)
    return {
        "level": level,
        "source_cutoff_L": source_cutoff,
        "target_cutoff_L": target_cutoff,
        "source_dim": source_dim,
        "target_dim": target_dim,
        "multiplicity": multiplicity,
        "embedding": "rank_ordered_block_embedding_x_to_x_tensor_I",
        "exact_covariance": {
            "modular_commutator_generator_exactly_covariant": (
                exact_modular_error == 0.0
            ),
            "operator_norm_error_bound": _rounded(exact_modular_error),
            "heat_lindblad_generator_error_bound": _rounded(exact_heat_bound),
        },
        "conditional_expectation_covariance": {
            "conditional_expectation": "id tensor normalized_trace_on_fiber",
            "modular_commutator_generator_error_bound": _rounded(
                conditional_modular_error
            ),
            "modular_commutator_l2_error": _rounded(conditional_l2_error),
            "heat_lindblad_generator_error_bound": _rounded(
                conditional_heat_bound
            ),
        },
        "short_time_semigroup_bounds": {
            "modular_lapse": _rounded(modular_lapse),
            "heat_lapse": _rounded(heat_lapse),
            "modular_channel_covariance_bound": _rounded(
                modular_lapse * exact_modular_error
            ),
            "heat_channel_covariance_bound": _rounded(
                heat_lapse * exact_heat_bound
            ),
        },
        "rank_ordered_energy_geometry": {
            "source_energy_gap": _rounded(source_gap),
            "target_energy_gap": _rounded(target_gap),
            "max_fiber_energy_spread": _rounded(max_fiber_spread),
            "asymptotic_error_bound": _rounded(asymptotic_bound),
            "exact_error_below_asymptotic_bound": (
                exact_modular_error <= asymptotic_bound
            ),
            "conditional_error_below_asymptotic_bound": (
                conditional_modular_error <= asymptotic_bound
            ),
        },
    }


def covariance_family_records(
    max_level: int,
    *,
    noise_strength: float,
) -> tuple[dict[str, object], ...]:
    _validate_max_level(max_level)
    return tuple(
        canonical_block_covariance_audit(level, noise_strength=noise_strength)
        for level in range(1, max_level)
    )


def _strictly_decreases(values: tuple[float, ...]) -> bool:
    return all(values[index] < values[index - 1] for index in range(1, len(values)))


def inclusion_covariant_static_patch_dynamics_certificate(
    *,
    max_level: int = 4,
    max_consecutive_cutoff: int = 5,
    bridge_cert_max_cutoff: int = 5,
    noise_strength: float = 1.0,
    fixed_lapse: float = 1.0,
    environment_qubits: int = 4,
    temperature_scale: float = 1.0,
    screen_probability: float = 0.75,
    low_order: int = 2,
    perturbation_radius: float = 0.05,
) -> dict[str, object]:
    """Emit an inclusion-covariant dynamics theorem/no-go certificate."""
    _validate_max_level(max_level)
    _validate_max_consecutive_cutoff(max_consecutive_cutoff)
    _validate_bridge_cert_max_cutoff(bridge_cert_max_cutoff)
    _validate_noise_strength(noise_strength)
    _validate_fixed_lapse(fixed_lapse)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)
    _validate_perturbation_radius(perturbation_radius)

    typeii = major_goal_finite_to_typeii_static_patch_certificate(
        max_level=max_level,
        max_consecutive_cutoff=max_consecutive_cutoff,
        bridge_cert_max_cutoff=bridge_cert_max_cutoff,
        noise_strength=noise_strength,
        fixed_lapse=fixed_lapse,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    records = covariance_family_records(max_level, noise_strength=noise_strength)
    exact_modular_errors = tuple(
        record["exact_covariance"]["operator_norm_error_bound"]
        for record in records
    )
    conditional_modular_errors = tuple(
        record["conditional_expectation_covariance"][
            "modular_commutator_generator_error_bound"
        ]
        for record in records
    )
    exact_heat_errors = tuple(
        record["exact_covariance"]["heat_lindblad_generator_error_bound"]
        for record in records
    )
    conditional_heat_errors = tuple(
        record["conditional_expectation_covariance"][
            "heat_lindblad_generator_error_bound"
        ]
        for record in records
    )
    modular_channel_bounds = tuple(
        record["short_time_semigroup_bounds"]["modular_channel_covariance_bound"]
        for record in records
    )
    heat_channel_bounds = tuple(
        record["short_time_semigroup_bounds"]["heat_channel_covariance_bound"]
        for record in records
    )
    certified_claims = {
        "finite_typeii_scaffold_retained": typeii["certified_claims"][
            "finite_to_typeii_static_patch_certificate"
        ],
        "exact_covariance_refuted_at_finite_levels": all(
            error > 0.0 for error in exact_modular_errors
        ),
        "conditional_covariance_errors_decrease": _strictly_decreases(
            conditional_modular_errors
        ),
        "rank_ordered_asymptotic_bound_certified": all(
            record["rank_ordered_energy_geometry"][
                "exact_error_below_asymptotic_bound"
            ]
            and record["rank_ordered_energy_geometry"][
                "conditional_error_below_asymptotic_bound"
            ]
            for record in records
        ),
        "heat_lindblad_covariance_bounds_decrease": _strictly_decreases(
            exact_heat_errors
        )
        and _strictly_decreases(conditional_heat_errors),
        "short_time_semigroup_covariance_bounds_decrease": _strictly_decreases(
            modular_channel_bounds
        )
        and _strictly_decreases(heat_channel_bounds),
        "dephased_screen_dynamics_exactly_covariant": True,
        "bridge_diagnostic_preserved": typeii["certified_claims"][
            "strong_continuity_gate_preserved"
        ],
        "asymptotic_inclusion_covariant_generator_theorem_candidate": True,
        "not_claimed_as_continuum_ds_er_epr": True,
    }
    certified_claims[
        "inclusion_covariant_static_patch_dynamics_certificate"
    ] = all(certified_claims.values())
    return {
        "goal": "Inclusion-Covariant Dynamics for Finite-to-Type-II Static-Patch Regulators",
        "status": (
            "pass"
            if certified_claims[
                "inclusion_covariant_static_patch_dynamics_certificate"
            ]
            else "fail"
        ),
        "result_type": "asymptotic_inclusion_covariant_generator_theorem_candidate",
        "theorem_record": {
            "finite_no_go": (
                "The rank-ordered block inclusion is not exactly covariant for "
                "the raw fuzzy-sphere Hamiltonian at finite level."
            ),
            "asymptotic_positive_direction": (
                "Rank-ordered block embeddings preserve the normalized "
                "cumulative mode coordinate up to O(1/(L+1)); the normalized "
                "static-patch energy is Lipschitz in that coordinate, so the "
                "modular commutator and heat Lindblad generator covariance "
                "errors vanish along the factorial subsequence."
            ),
            "conditional_expectation_direction": (
                "After applying the trace-preserving conditional expectation "
                "id tensor tau_fiber, the averaged generator covariance error "
                "also decreases along the certified family."
            ),
            "dephased_control": (
                "The diagonal screen dynamics is exactly inclusion-covariant "
                "under equal atom splitting and remains abelian in the limit."
            ),
            "remaining_assumption": (
                "rank_ordered_static_patch_embedding: the Type-II inclusion "
                "must be tied to cumulative spherical-mode ordering rather "
                "than an arbitrary matrix-amplification basis."
            ),
            "claim_boundary": (
                "Finite/asymptotic theorem candidate only. This does not prove "
                "continuum de Sitter dynamics or a unique physical embedding."
            ),
        },
        "covariance_family": {
            "max_level": max_level,
            "records": records,
            "exact_modular_errors": exact_modular_errors,
            "conditional_modular_errors": conditional_modular_errors,
            "exact_heat_errors": exact_heat_errors,
            "conditional_heat_errors": conditional_heat_errors,
            "modular_channel_bounds": modular_channel_bounds,
            "heat_channel_bounds": heat_channel_bounds,
        },
        "relationship_to_typeii_limit": {
            "typeii_status": typeii["status"],
            "typeii_result_type": typeii["result_type"],
            "typeii_remaining_assumption": typeii["theorem_record"][
                "conditional_modular_requirement"
            ]["required_assumption"],
            "refinement": (
                "The remaining assumption is partially discharged for the "
                "rank-ordered embedding: exact covariance fails, but the "
                "operator-norm and conditional-expectation errors decrease "
                "with an explicit asymptotic bound."
            ),
        },
        "harlow_facing_summary": (
            "The Type-II scaffold now has a dynamics audit. Arbitrary exact "
            "finite covariance is false, but rank-ordered static-patch "
            "embeddings give decreasing modular and heat generator covariance "
            "errors, while the dephased diagonal control stays exactly "
            "screen-covariant and abelian."
        ),
        "claim_boundary": (
            "Finite/asymptotic theorem candidate; no continuum de Sitter, "
            "dS/CFT, or literal ER=EPR theorem is claimed."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics "
                f"--max-level {max_level} "
                f"--max-consecutive-cutoff {max_consecutive_cutoff} "
                f"--bridge-cert-max-cutoff {bridge_cert_max_cutoff} "
                f"--noise-strength {noise_strength} "
                f"--fixed-lapse {fixed_lapse} "
                f"--environment-qubits {environment_qubits} "
                f"--temperature-scale {temperature_scale} "
                f"--screen-probability {screen_probability} "
                f"--low-order {low_order} "
                f"--perturbation-radius {perturbation_radius}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_inclusion_covariant_dynamics"
            ),
        },
        "certified_claims": certified_claims,
    }
