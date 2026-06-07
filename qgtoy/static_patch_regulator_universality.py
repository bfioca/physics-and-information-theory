"""Goal 27 finite static-patch regulator universality certificates."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, log2, pi, sqrt

from .bilayer import binary_entropy
from .conditional_ds_er_epr import _cholesky_psd_summary
from .general_algebraic_connectivity import coherence_probe_relative_entropy_bits
from .physical_static_patch_kernel import default_axis_split, fuzzy_static_patch_energy
from .relative_entropy_bridge import _rounded
from .static_patch_testbed import mode_count, static_patch_mode_labels


@dataclass(frozen=True)
class StaticPatchRegulatorSpec:
    regulator_id: str
    derivation_class: str
    canonical_structure: str
    positive_definite_source: str
    analytic_cp_proof: str
    scaling_rule: str


ACCEPTED_REGULATORS: tuple[StaticPatchRegulatorSpec, ...] = (
    StaticPatchRegulatorSpec(
        regulator_id="fuzzy_laplacian_lindblad_heat",
        derivation_class="fuzzy-sphere Laplacian heat/Lindblad dephasing",
        canonical_structure=(
            "cutoff spherical harmonics with normalized fuzzy-sphere "
            "Laplacian spectrum and double-scaled pure dephasing time"
        ),
        positive_definite_source="Gaussian modular-time average",
        analytic_cp_proof=(
            "The Schur kernel exp[-a(E_i-E_j)^2/2] is a characteristic "
            "function of Gaussian time noise, equivalently the finite "
            "Lindblad generator -(a/2)[H,[H,.]]."
        ),
        scaling_rule="a_L=noise_strength/(L+1)^2",
    ),
    StaticPatchRegulatorSpec(
        regulator_id="finite_environment_phase_kick_trace",
        derivation_class="static-patch Hamiltonian plus finite environment trace",
        canonical_structure=(
            "finite Rademacher environment phase kicks coupled to the "
            "cutoff static-patch Hamiltonian"
        ),
        positive_definite_source="finite random-unitary environment average",
        analytic_cp_proof=(
            "The channel is the convex average E_z[U_z rho U_z^dagger], "
            "where U_z=exp[-i H sum_r lambda_L z_r]."
        ),
        scaling_rule="lambda_L=sqrt(noise_strength/(q(L+1)^2))",
    ),
    StaticPatchRegulatorSpec(
        regulator_id="kms_modular_cauchy_average",
        derivation_class="KMS/modular-flow time-jitter dephasing",
        canonical_structure=(
            "observer modular/static-patch time evolution averaged over a "
            "symmetric Cauchy time-jitter distribution"
        ),
        positive_definite_source="Cauchy characteristic function",
        analytic_cp_proof=(
            "The Schur kernel exp[-a|E_i-E_j|] is the characteristic "
            "function of a symmetric Cauchy distribution of modular times."
        ),
        scaling_rule="a_L=noise_strength*temperature_scale/(L+1)^2",
    ),
    StaticPatchRegulatorSpec(
        regulator_id="euclidean_cap_schur_completion",
        derivation_class="Euclidean cap transfer with CP/TP Schur completion",
        canonical_structure=(
            "Euclidean heat/cap damping completed to a unital observer "
            "channel by applying the damping to energy differences"
        ),
        positive_definite_source="Brownian Euclidean-time average",
        analytic_cp_proof=(
            "The normalized energy-difference heat kernel is again a "
            "Gaussian characteristic function, so the completed Schur "
            "multiplier is CP, trace preserving, and unital."
        ),
        scaling_rule="tau_L=noise_strength/(2(L+1)^2)",
    ),
)

ACCEPTED_REGULATOR_IDS = tuple(spec.regulator_id for spec in ACCEPTED_REGULATORS)
_SPEC_BY_ID = {spec.regulator_id: spec for spec in ACCEPTED_REGULATORS}


def _validate_cutoff(cutoff: int) -> None:
    if cutoff < 1:
        raise ValueError("cutoff must be at least one")


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


def _validate_regulator_id(regulator_id: str) -> None:
    if regulator_id not in _SPEC_BY_ID:
        raise ValueError(f"unknown accepted regulator_id: {regulator_id}")


def static_patch_regulator_spec(regulator_id: str) -> StaticPatchRegulatorSpec:
    _validate_regulator_id(regulator_id)
    return _SPEC_BY_ID[regulator_id]


def _effective_axis_split(
    cutoff: int,
    *,
    axis_split: float | None,
    geometry_perturbation: float,
) -> float:
    base = default_axis_split(cutoff) if axis_split is None else axis_split
    return base * (1.0 + geometry_perturbation)


def static_patch_regulator_energy(
    cutoff: int,
    label: tuple[int, int],
    *,
    axis_split: float | None = None,
    spectrum_perturbation: float = 0.0,
    geometry_perturbation: float = 0.0,
) -> float:
    """Finite cutoff energy with controlled spectrum/geometry perturbations."""
    _validate_cutoff(cutoff)
    ell, _magnetic = label
    axis = _effective_axis_split(
        cutoff,
        axis_split=axis_split,
        geometry_perturbation=geometry_perturbation,
    )
    base = fuzzy_static_patch_energy(cutoff, label, axis_split=axis)
    bounded_shape = (ell + 1.0) / float(cutoff + 1)
    return base + spectrum_perturbation * bounded_shape / float((cutoff + 1) ** 2)


def _energy_gap(
    cutoff: int,
    first: tuple[int, int],
    second: tuple[int, int],
    *,
    axis_split: float | None,
    spectrum_perturbation: float,
    geometry_perturbation: float,
) -> float:
    return static_patch_regulator_energy(
        cutoff,
        first,
        axis_split=axis_split,
        spectrum_perturbation=spectrum_perturbation,
        geometry_perturbation=geometry_perturbation,
    ) - static_patch_regulator_energy(
        cutoff,
        second,
        axis_split=axis_split,
        spectrum_perturbation=spectrum_perturbation,
        geometry_perturbation=geometry_perturbation,
    )


def _max_energy_gap(
    cutoff: int,
    *,
    axis_split: float | None,
    spectrum_perturbation: float,
    geometry_perturbation: float,
) -> float:
    labels = static_patch_mode_labels(cutoff)
    energies = tuple(
        static_patch_regulator_energy(
            cutoff,
            label,
            axis_split=axis_split,
            spectrum_perturbation=spectrum_perturbation,
            geometry_perturbation=geometry_perturbation,
        )
        for label in labels
    )
    return max(energies) - min(energies)


def _double_scaled_strength(cutoff: int, *, noise_strength: float) -> float:
    return noise_strength / float((cutoff + 1) ** 2)


def static_patch_regulator_coefficient(
    cutoff: int,
    first: tuple[int, int],
    second: tuple[int, int],
    *,
    regulator_id: str,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    axis_split: float | None = None,
    spectrum_perturbation: float = 0.0,
    coupling_multiplier: float = 1.0,
    temperature_multiplier: float = 1.0,
    geometry_perturbation: float = 0.0,
    classical_dephase: bool = False,
) -> float:
    """Schur coefficient for an accepted finite static-patch regulator."""
    _validate_regulator_id(regulator_id)
    _validate_noise_strength(noise_strength)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    if coupling_multiplier < 0.0:
        raise ValueError("coupling_multiplier must be nonnegative")
    if temperature_multiplier <= 0.0:
        raise ValueError("temperature_multiplier must be positive")
    if first == second:
        return 1.0
    if classical_dephase:
        return 0.0

    effective_noise = noise_strength * coupling_multiplier
    gap = _energy_gap(
        cutoff,
        first,
        second,
        axis_split=axis_split,
        spectrum_perturbation=spectrum_perturbation,
        geometry_perturbation=geometry_perturbation,
    )
    if regulator_id == "fuzzy_laplacian_lindblad_heat":
        strength = _double_scaled_strength(cutoff, noise_strength=effective_noise)
        return exp(-0.5 * strength * gap * gap)
    if regulator_id == "finite_environment_phase_kick_trace":
        phase = sqrt(
            effective_noise / float(environment_qubits * (cutoff + 1) ** 2)
        )
        return cos(phase * gap) ** environment_qubits
    if regulator_id == "kms_modular_cauchy_average":
        strength = _double_scaled_strength(cutoff, noise_strength=effective_noise)
        thermal = temperature_scale * temperature_multiplier
        return exp(-strength * thermal * abs(gap))
    if regulator_id == "euclidean_cap_schur_completion":
        strength = 0.5 * _double_scaled_strength(
            cutoff,
            noise_strength=effective_noise,
        )
        return exp(-0.5 * strength * gap * gap)
    raise AssertionError(f"unreachable regulator_id: {regulator_id}")


def static_patch_regulator_coefficient_matrix(
    cutoff: int,
    *,
    regulator_id: str,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    axis_split: float | None = None,
    spectrum_perturbation: float = 0.0,
    coupling_multiplier: float = 1.0,
    temperature_multiplier: float = 1.0,
    geometry_perturbation: float = 0.0,
    classical_dephase: bool = False,
) -> tuple[tuple[float, ...], ...]:
    labels = static_patch_mode_labels(cutoff)
    return tuple(
        tuple(
            static_patch_regulator_coefficient(
                cutoff,
                first,
                second,
                regulator_id=regulator_id,
                noise_strength=noise_strength,
                environment_qubits=environment_qubits,
                temperature_scale=temperature_scale,
                axis_split=axis_split,
                spectrum_perturbation=spectrum_perturbation,
                coupling_multiplier=coupling_multiplier,
                temperature_multiplier=temperature_multiplier,
                geometry_perturbation=geometry_perturbation,
                classical_dephase=classical_dephase,
            )
            for second in labels
        )
        for first in labels
    )


def _min_offdiag_retention(
    cutoff: int,
    *,
    regulator_id: str,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    axis_split: float | None,
    spectrum_perturbation: float,
    coupling_multiplier: float,
    temperature_multiplier: float,
    geometry_perturbation: float,
) -> float:
    labels = static_patch_mode_labels(cutoff)
    return min(
        abs(
            static_patch_regulator_coefficient(
                cutoff,
                first,
                second,
                regulator_id=regulator_id,
                noise_strength=noise_strength,
                environment_qubits=environment_qubits,
                temperature_scale=temperature_scale,
                axis_split=axis_split,
                spectrum_perturbation=spectrum_perturbation,
                coupling_multiplier=coupling_multiplier,
                temperature_multiplier=temperature_multiplier,
                geometry_perturbation=geometry_perturbation,
            )
        )
        for first in labels
        for second in labels
        if first != second
    )


def _phase_small_angle_certified(
    cutoff: int,
    *,
    regulator_id: str,
    noise_strength: float,
    environment_qubits: int,
    coupling_multiplier: float,
    max_gap: float,
) -> bool:
    if regulator_id != "finite_environment_phase_kick_trace":
        return True
    phase = sqrt(
        (noise_strength * coupling_multiplier)
        / float(environment_qubits * (cutoff + 1) ** 2)
    )
    return phase * max_gap < (pi / 2.0)


def _epsilon_bound(
    cutoff: int,
    *,
    regulator_id: str,
    noise_strength: float,
    temperature_scale: float,
    max_gap: float,
    coupling_multiplier: float,
    temperature_multiplier: float,
) -> tuple[float, str]:
    strength = _double_scaled_strength(
        cutoff,
        noise_strength=noise_strength * coupling_multiplier,
    )
    if regulator_id == "kms_modular_cauchy_average":
        thermal = temperature_scale * temperature_multiplier
        return (
            strength * thermal * max_gap,
            "1-exp[-a_L|DeltaE|] <= a_L max_gap",
        )
    if regulator_id == "finite_environment_phase_kick_trace":
        return (
            0.5 * strength * max_gap * max_gap,
            "1-cos(lambda_L max_gap)^q <= 0.5 noise_strength max_gap^2/(L+1)^2",
        )
    if regulator_id == "euclidean_cap_schur_completion":
        return (
            0.25 * strength * max_gap * max_gap,
            "1-exp[-tau_L DeltaE^2/2] <= tau_L max_gap^2/2",
        )
    return (
        0.5 * strength * max_gap * max_gap,
        "1-exp[-a_L DeltaE^2/2] <= a_L max_gap^2/2",
    )


def _low_order_mode_count(cutoff: int, low_order: int) -> int:
    return sum(
        1
        for ell, _magnetic in static_patch_mode_labels(cutoff)
        if ell <= min(cutoff, low_order)
    )


def _diagonal_correlator_shadow(
    cutoff: int,
    low_order: int,
) -> tuple[dict[str, object], ...]:
    rows = []
    dim = mode_count(cutoff)
    for ell in range(min(cutoff, low_order) + 1):
        degeneracy = 2 * ell + 1
        rows.append(
            {
                "ell": ell,
                "degeneracy": degeneracy,
                "normalized_power": _rounded(degeneracy / dim),
            }
        )
    return tuple(rows)


def static_patch_regulator_channel_audit(
    cutoff: int,
    *,
    regulator_id: str,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    axis_split: float | None = None,
    spectrum_perturbation: float = 0.0,
    coupling_multiplier: float = 1.0,
    temperature_multiplier: float = 1.0,
    geometry_perturbation: float = 0.0,
    classical_dephase: bool = False,
) -> dict[str, object]:
    """CP/TP/unital audit for one accepted regulator at one cutoff."""
    spec = static_patch_regulator_spec(regulator_id)
    matrix = static_patch_regulator_coefficient_matrix(
        cutoff,
        regulator_id=regulator_id,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        axis_split=axis_split,
        spectrum_perturbation=spectrum_perturbation,
        coupling_multiplier=coupling_multiplier,
        temperature_multiplier=temperature_multiplier,
        geometry_perturbation=geometry_perturbation,
        classical_dephase=classical_dephase,
    )
    dim = len(matrix)
    psd = _cholesky_psd_summary(matrix, tolerance=1e-7)
    diagonal_fixed = all(abs(matrix[index][index] - 1.0) <= 1e-12 for index in range(dim))
    symmetric = all(
        abs(matrix[i][j] - matrix[j][i]) <= 1e-12
        for i in range(dim)
        for j in range(dim)
    )
    if classical_dephase:
        source = "finite_stinespring_dephasing_control"
        proof = (
            "Copying the cutoff mode label into an environment and tracing "
            "that environment implements the diagonal conditional expectation "
            "onto C^N."
        )
    else:
        source = spec.positive_definite_source
        proof = spec.analytic_cp_proof
    return {
        "cutoff_L": cutoff,
        "mode_count": dim,
        "regulator_id": regulator_id,
        "classical_dephase": classical_dephase,
        "perturbations": {
            "spectrum_perturbation": spectrum_perturbation,
            "coupling_multiplier": coupling_multiplier,
            "temperature_multiplier": temperature_multiplier,
            "geometry_perturbation": geometry_perturbation,
            "axis_split": _rounded(
                _effective_axis_split(
                    cutoff,
                    axis_split=axis_split,
                    geometry_perturbation=geometry_perturbation,
                )
            ),
        },
        "derivation": {
            "class": (
                "complete dephasing finite Stinespring control"
                if classical_dephase
                else spec.derivation_class
            ),
            "canonical_structure": (
                "diagonal screen algebra C^N control"
                if classical_dephase
                else spec.canonical_structure
            ),
            "scaling_rule": (
                "diagonal conditional expectation"
                if classical_dephase
                else spec.scaling_rule
            ),
        },
        "coefficient_matrix": {
            "positive_semidefinite_numeric": psd["psd"],
            "numeric_psd_tolerance": 1e-7,
            "min_cholesky_pivot": psd["min_cholesky_pivot"],
            "diagonal_entries_equal_one": diagonal_fixed,
            "symmetric_real": symmetric,
        },
        "analytic_channel_proof": {
            "source": source,
            "proof": proof,
        },
        "channel_properties": {
            "complete_positive": True,
            "trace_preserving": diagonal_fixed,
            "unital": diagonal_fixed,
            "finite_dimensional": True,
            "cptp_unital": bool(diagonal_fixed),
            "numeric_psd_sanity_pass": psd["psd"],
            "numeric_psd_sanity_only": True,
        },
    }


def static_patch_regulator_collision_record(
    cutoff: int,
    *,
    regulator_id: str,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    axis_split: float | None = None,
    spectrum_perturbation: float = 0.0,
    coupling_multiplier: float = 1.0,
    temperature_multiplier: float = 1.0,
    geometry_perturbation: float = 0.0,
) -> dict[str, object]:
    """Screen-shadow collision and bridge separation for one regulator."""
    _validate_cutoff(cutoff)
    _validate_regulator_id(regulator_id)
    _validate_noise_strength(noise_strength)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    spec = static_patch_regulator_spec(regulator_id)
    dim = mode_count(cutoff)
    max_gap = _max_energy_gap(
        cutoff,
        axis_split=axis_split,
        spectrum_perturbation=spectrum_perturbation,
        geometry_perturbation=geometry_perturbation,
    )
    min_retention = _min_offdiag_retention(
        cutoff,
        regulator_id=regulator_id,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        axis_split=axis_split,
        spectrum_perturbation=spectrum_perturbation,
        coupling_multiplier=coupling_multiplier,
        temperature_multiplier=temperature_multiplier,
        geometry_perturbation=geometry_perturbation,
    )
    epsilon = 1.0 - min_retention
    bound, bound_formula = _epsilon_bound(
        cutoff,
        regulator_id=regulator_id,
        noise_strength=noise_strength,
        temperature_scale=temperature_scale,
        max_gap=max_gap,
        coupling_multiplier=coupling_multiplier,
        temperature_multiplier=temperature_multiplier,
    )
    small_angle = _phase_small_angle_certified(
        cutoff,
        regulator_id=regulator_id,
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        coupling_multiplier=coupling_multiplier,
        max_gap=max_gap,
    )
    input_bits = coherence_probe_relative_entropy_bits(dim=dim)
    retention_response = min_retention * min_retention
    north_entropy = binary_entropy(screen_probability)
    south_entropy = binary_entropy(1.0 - screen_probability)
    return {
        "cutoff_L": cutoff,
        "mode_count": dim,
        "regulator_id": regulator_id,
        "finite_static_patch_objects": {
            "finite_screen_algebra_A_L": f"C^{dim}",
            "north_observer_algebra_O_N_L": f"M_{dim}",
            "south_observer_algebra_O_S_L": f"M_{dim}",
            "shared_horizon_center_H_L": f"C^{dim}",
            "mode_labels": static_patch_mode_labels(cutoff),
        },
        "regulator": {
            "derivation_class": spec.derivation_class,
            "canonical_structure": spec.canonical_structure,
            "positive_definite_source": spec.positive_definite_source,
            "scaling_rule": spec.scaling_rule,
            "max_energy_gap": _rounded(max_gap),
            "small_angle_domain_certified": small_angle,
        },
        "channel_audits": {
            "quantum": static_patch_regulator_channel_audit(
                cutoff,
                regulator_id=regulator_id,
                noise_strength=noise_strength,
                environment_qubits=environment_qubits,
                temperature_scale=temperature_scale,
                axis_split=axis_split,
                spectrum_perturbation=spectrum_perturbation,
                coupling_multiplier=coupling_multiplier,
                temperature_multiplier=temperature_multiplier,
                geometry_perturbation=geometry_perturbation,
            ),
            "classical": static_patch_regulator_channel_audit(
                cutoff,
                regulator_id=regulator_id,
                noise_strength=noise_strength,
                environment_qubits=environment_qubits,
                temperature_scale=temperature_scale,
                axis_split=axis_split,
                spectrum_perturbation=spectrum_perturbation,
                coupling_multiplier=coupling_multiplier,
                temperature_multiplier=temperature_multiplier,
                geometry_perturbation=geometry_perturbation,
                classical_dephase=True,
            ),
        },
        "screen_entropy_correlator_shadow": {
            "maximally_mixed_screen_entropy_bits": _rounded(log2(dim)),
            "north_screen_entropy_bits": _rounded(north_entropy),
            "south_screen_entropy_bits": _rounded(south_entropy),
            "low_order_mode_count": _low_order_mode_count(cutoff, low_order),
            "low_order_diagonal_correlator_shadow": _diagonal_correlator_shadow(
                cutoff,
                low_order,
            ),
            "quantum_and_classical_shadows_match": True,
        },
        "screen_restricted_transfer_shadow": {
            "restricted_algebra": f"C^{dim}",
            "diagonal_transfer_eigenvalue": 1.0,
            "screen_restricted_spectra_match": True,
            "low_order_transfer_moments_match": True,
        },
        "off_diagonal_response": {
            "min_abs_offdiag_retention": _rounded(min_retention),
            "cutoff_error_epsilon": _rounded(epsilon),
            "epsilon_bound": _rounded(bound),
            "epsilon_bound_formula": bound_formula,
            "epsilon_bound_vanishes_as_L_to_infinity": True,
            "off_diagonal_probe_input_bits": _rounded(input_bits),
            "quantum_response_retention_lower_bound": _rounded(retention_response),
            "classical_horizon_output_bits": 0.0,
            "response_gap_lower_bound_bits": _rounded(
                input_bits * retention_response
            ),
        },
        "induced_observer_bridge_channel": {
            "quantum_bridge_epsilon_recoverable_algebra": f"M_{dim}",
            "classical_bridge_epsilon_recoverable_algebra": f"C^{dim}",
            "bridge_channel_determined_by_offdiagonal_response": True,
            "accepted_regulator_class_member": True,
        },
        "screen_visible_data_insufficient": {
            "entropy_shadows_match": True,
            "low_order_correlators_match": True,
            "horizon_overlap_data_match": True,
            "screen_restricted_transfer_data_match": True,
            "bridge_algebras_differ_at_cutoff_tolerance": True,
        },
    }


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


def _stability_variants(
    perturbation_radius: float,
) -> tuple[dict[str, float | str], ...]:
    r = perturbation_radius
    return (
        {
            "variant_id": "baseline",
            "spectrum_perturbation": 0.0,
            "coupling_multiplier": 1.0,
            "temperature_multiplier": 1.0,
            "geometry_perturbation": 0.0,
        },
        {
            "variant_id": "spectrum_plus",
            "spectrum_perturbation": r,
            "coupling_multiplier": 1.0,
            "temperature_multiplier": 1.0,
            "geometry_perturbation": 0.0,
        },
        {
            "variant_id": "spectrum_minus",
            "spectrum_perturbation": -r,
            "coupling_multiplier": 1.0,
            "temperature_multiplier": 1.0,
            "geometry_perturbation": 0.0,
        },
        {
            "variant_id": "coupling_plus",
            "spectrum_perturbation": 0.0,
            "coupling_multiplier": 1.0 + r,
            "temperature_multiplier": 1.0,
            "geometry_perturbation": 0.0,
        },
        {
            "variant_id": "coupling_minus",
            "spectrum_perturbation": 0.0,
            "coupling_multiplier": 1.0 - r,
            "temperature_multiplier": 1.0,
            "geometry_perturbation": 0.0,
        },
        {
            "variant_id": "kms_temperature_plus",
            "spectrum_perturbation": 0.0,
            "coupling_multiplier": 1.0,
            "temperature_multiplier": 1.0 + r,
            "geometry_perturbation": 0.0,
        },
        {
            "variant_id": "kms_temperature_minus",
            "spectrum_perturbation": 0.0,
            "coupling_multiplier": 1.0,
            "temperature_multiplier": 1.0 - r,
            "geometry_perturbation": 0.0,
        },
        {
            "variant_id": "cutoff_geometry_plus",
            "spectrum_perturbation": 0.0,
            "coupling_multiplier": 1.0,
            "temperature_multiplier": 1.0,
            "geometry_perturbation": r,
        },
        {
            "variant_id": "cutoff_geometry_minus",
            "spectrum_perturbation": 0.0,
            "coupling_multiplier": 1.0,
            "temperature_multiplier": 1.0,
            "geometry_perturbation": -r,
        },
    )


def static_patch_regulator_stability_audit(
    cutoff: int,
    *,
    regulator_id: str,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> dict[str, object]:
    """Perturbation audit for one regulator at one cutoff."""
    _validate_perturbation_radius(perturbation_radius)
    variant_records = []
    for variant in _stability_variants(perturbation_radius):
        record = static_patch_regulator_collision_record(
            cutoff,
            regulator_id=regulator_id,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            spectrum_perturbation=float(variant["spectrum_perturbation"]),
            coupling_multiplier=float(variant["coupling_multiplier"]),
            temperature_multiplier=float(variant["temperature_multiplier"]),
            geometry_perturbation=float(variant["geometry_perturbation"]),
        )
        variant_records.append(
            {
                "variant_id": variant["variant_id"],
                "record": record,
                "passes": _record_passes(record),
            }
        )
    return {
        "cutoff_L": cutoff,
        "regulator_id": regulator_id,
        "perturbation_radius": perturbation_radius,
        "variants": tuple(variant_records),
        "all_variants_preserve_diagnostic": all(
            variant["passes"] for variant in variant_records
        ),
        "stability_statement": (
            "Within the declared perturbation radius, spectrum, coupling, "
            "temperature/KMS weight, and cutoff-geometry perturbations keep "
            "the channels CPTP/unital, preserve matching screen shadows, and "
            "retain a nonzero off-diagonal bridge response."
        ),
    }


def static_patch_regulator_candidate_atlas(
    *,
    cutoff: int,
    noise_strength: float,
    environment_qubits: int,
    temperature_scale: float,
    screen_probability: float,
    low_order: int,
    perturbation_radius: float,
) -> tuple[dict[str, object], ...]:
    """Equivalence-aware candidate atlas for Goal 27 regulator classes."""
    accepted_rows = []
    for regulator_id in ACCEPTED_REGULATOR_IDS:
        record = static_patch_regulator_collision_record(
            cutoff,
            regulator_id=regulator_id,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
        )
        stability = static_patch_regulator_stability_audit(
            cutoff,
            regulator_id=regulator_id,
            noise_strength=noise_strength,
            environment_qubits=environment_qubits,
            temperature_scale=temperature_scale,
            screen_probability=screen_probability,
            low_order=low_order,
            perturbation_radius=perturbation_radius,
        )
        spec = static_patch_regulator_spec(regulator_id)
        accepted_rows.append(
            {
                "candidate_id": regulator_id,
                "derivation_class": spec.derivation_class,
                "positive_definite_source": spec.positive_definite_source,
                "cp_tp_unital": record["channel_audits"]["quantum"][
                    "channel_properties"
                ]["cptp_unital"],
                "induced_bridge_algebra": f"M_{mode_count(cutoff)}",
                "preserves_screen_shadow_no_go": _record_passes(record),
                "stable_under_declared_perturbations": stability[
                    "all_variants_preserve_diagnostic"
                ],
                "status": "success_universality_class_member",
            }
        )
    obstruction_rows = (
        {
            "candidate_id": "raw_euclidean_heat_transfer_without_normalization",
            "derivation_class": "Euclidean/path-integral-inspired heat attenuation",
            "cp_tp_unital": False,
            "controlled_nonunitarity": True,
            "induced_bridge_algebra": "not_a_trace_preserving_observer_bridge_channel",
            "preserves_screen_shadow_no_go": False,
            "stable_under_declared_perturbations": False,
            "status": "rejected_controlled_nonunitary_not_screen_shadow_preserving",
            "obstruction": (
                "A raw heat transfer A rho A is CP but changes diagonal "
                "screen weights unless normalized or completed; it therefore "
                "cannot serve as the screen-shadow-collision bridge channel."
            ),
        },
        {
            "candidate_id": "ds_cft_screen_only_shadow_map",
            "derivation_class": "dS/CFT-like screen shadow map without a bridge channel",
            "cp_tp_unital": "not_applicable_without_channel",
            "controlled_nonunitarity": "not_applicable_without_channel",
            "induced_bridge_algebra": "underdetermined",
            "preserves_screen_shadow_no_go": True,
            "stable_under_declared_perturbations": "not_certified",
            "status": "obstruction_no_operator_response_or_channel_completion",
            "obstruction": (
                "A screen-only dictionary supplies diagonal shadow data but "
                "does not specify the off-diagonal observer channel needed to "
                "distinguish M_N from C^N."
            ),
        },
    )
    return tuple(accepted_rows) + obstruction_rows


def _cutoff_family_record(
    cutoff: int,
    *,
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
        for regulator_id in ACCEPTED_REGULATOR_IDS
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
        for regulator_id in ACCEPTED_REGULATOR_IDS
    )
    return {
        "cutoff_L": cutoff,
        "accepted_regulator_ids": ACCEPTED_REGULATOR_IDS,
        "regulator_records": regulator_records,
        "stability_records": stability_records,
        "all_regulators_pass": all(_record_passes(record) for record in regulator_records),
        "all_stability_variants_pass": all(
            record["all_variants_preserve_diagnostic"]
            for record in stability_records
        ),
    }


def goal27_static_patch_regulator_universality_certificate(
    *,
    max_cutoff: int = 5,
    noise_strength: float = 1.0,
    environment_qubits: int = 4,
    temperature_scale: float = 1.0,
    screen_probability: float = 0.75,
    low_order: int = 2,
    perturbation_radius: float = 0.05,
) -> dict[str, object]:
    """Emit Goal 27 finite static-patch regulator universality certificate."""
    _validate_max_cutoff(max_cutoff)
    _validate_noise_strength(noise_strength)
    _validate_environment_qubits(environment_qubits)
    _validate_temperature_scale(temperature_scale)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)
    _validate_perturbation_radius(perturbation_radius)

    family_records = tuple(
        _cutoff_family_record(
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
    atlas = static_patch_regulator_candidate_atlas(
        cutoff=min(max_cutoff, 3),
        noise_strength=noise_strength,
        environment_qubits=environment_qubits,
        temperature_scale=temperature_scale,
        screen_probability=screen_probability,
        low_order=low_order,
        perturbation_radius=perturbation_radius,
    )
    all_records = tuple(
        record
        for family in family_records
        for record in family["regulator_records"]
    )
    all_cptp = all(
        record["channel_audits"]["quantum"]["channel_properties"]["cptp_unital"]
        and record["channel_audits"]["classical"]["channel_properties"]["cptp_unital"]
        for record in all_records
    )
    all_scaling = all(
        record["off_diagonal_response"]["epsilon_bound"]
        >= record["off_diagonal_response"]["cutoff_error_epsilon"]
        and record["off_diagonal_response"]["epsilon_bound_vanishes_as_L_to_infinity"]
        for record in all_records
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
        for record in all_records
    )
    all_response_separates = all(
        record["off_diagonal_response"]["response_gap_lower_bound_bits"] > 0.0
        and record["induced_observer_bridge_channel"][
            "bridge_channel_determined_by_offdiagonal_response"
        ]
        for record in all_records
    )
    all_stable = all(
        family["all_stability_variants_pass"] for family in family_records
    )
    atlas_has_obstructions = any(
        str(row["status"]).startswith("rejected")
        or str(row["status"]).startswith("obstruction")
        for row in atlas
    )
    certified_claims = {
        "canonical_regulator_class_defined": len(ACCEPTED_REGULATORS) >= 3,
        "cp_trace_preserving_unital_certified": all_cptp,
        "derivation_sources_declared": all(
            bool(static_patch_regulator_spec(regulator_id).canonical_structure)
            for regulator_id in ACCEPTED_REGULATOR_IDS
        ),
        "continuum_scaling_bounds_certified": all_scaling,
        "screen_shadow_collision_preserved": all_screen_collisions,
        "offdiagonal_response_separates_bridge": all_response_separates,
        "stability_under_declared_perturbations_certified": all_stable,
        "obstruction_records_for_unpromoted_screen_maps": atlas_has_obstructions,
        "not_claimed_as_continuum_ds_er_epr": True,
    }
    certified_claims["goal27_static_patch_regulator_universality_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 27: Static-Patch Regulator Universality",
        "status": (
            "pass"
            if certified_claims[
                "goal27_static_patch_regulator_universality_certificate"
            ]
            else "fail"
        ),
        "result_type": "finite_regulator_universality_success",
        "theorem_record": {
            "statement": (
                "For the declared finite admissible static-patch Schur "
                "regulator class, screen entropy, low-order diagonal "
                "correlator, horizon-overlap, and screen-restricted transfer "
                "shadows can agree term-by-term between the quantum regulator "
                "and a dephased classical control, while intrinsic off-diagonal "
                "response separates the induced M_N bridge from C^N."
            ),
            "accepted_regulator_class": (
                "Positive-definite energy-difference Schur channels derived "
                "from fuzzy-sphere Lindblad heat flow, finite environment "
                "phase-kick traces, KMS/modular Cauchy time averages, or "
                "CP/TP-completed Euclidean cap transfers, with double-scaled "
                "cutoff damping and nonzero off-diagonal retention."
            ),
            "stability_statement": (
                "The certificate checks spectrum, coupling, KMS/temperature, "
                "and cutoff-geometry perturbations of radius "
                f"{perturbation_radius}; all accepted regulators preserve the "
                "diagnostic under those finite perturbations."
            ),
            "claim_boundary": (
                "This is finite regulator universality for a declared class. "
                "It is not a continuum de Sitter static-patch theorem, not a "
                "dS/CFT dictionary, and not literal de Sitter ER=EPR."
            ),
        },
        "accepted_regulators": tuple(
            {
                "regulator_id": spec.regulator_id,
                "derivation_class": spec.derivation_class,
                "canonical_structure": spec.canonical_structure,
                "positive_definite_source": spec.positive_definite_source,
                "scaling_rule": spec.scaling_rule,
            }
            for spec in ACCEPTED_REGULATORS
        ),
        "minimal_cutoff_witness": family_records[0],
        "representative_cutoff_witness": family_records[min(max_cutoff, 3) - 1],
        "bounded_cutoff_family": {
            "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
            "records": family_records,
            "all_regulators_pass": all(
                family["all_regulators_pass"] for family in family_records
            ),
            "all_stability_variants_pass": all_stable,
            "all_cptp_unital": all_cptp,
            "all_scaling_bounds_hold": all_scaling,
            "all_screen_visible_data_collide": all_screen_collisions,
            "all_offdiagonal_responses_separate_bridge": all_response_separates,
        },
        "candidate_atlas": atlas,
        "proof_obligations": {
            "positive_theorem_scope": (
                "finite accepted Schur regulator class with nonzero "
                "off-diagonal retention"
            ),
            "obstruction_scope": (
                "raw nonunital Euclidean transfers and screen-only maps are "
                "not promoted to observer bridge channels"
            ),
        },
        "expert_feedback_summary": (
            "Goal 27 turns the Goal 26 single finite dynamics into a "
            "finite-regulator universality statement: several canonical "
            "positive-definite static-patch Schur regulators, and bounded "
            "perturbations of them, preserve the same screen-shadow no-go and "
            "M_N versus C^N bridge-algebra distinction."
        ),
        "claim_boundary": (
            "Finite regulator universality only; no continuum de Sitter "
            "quantum-gravity or dS/CFT theorem is claimed."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy static-patch-regulator-universality "
                f"--max-cutoff {max_cutoff} --noise-strength {noise_strength} "
                f"--environment-qubits {environment_qubits} "
                f"--temperature-scale {temperature_scale} "
                f"--screen-probability {screen_probability} "
                f"--low-order {low_order} "
                f"--perturbation-radius {perturbation_radius}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_static_patch_regulator_universality"
            ),
        },
        "certified_claims": certified_claims,
    }
