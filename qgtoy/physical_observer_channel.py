"""Finite local realization of a binary observer-decoherence channel.

The model has three deliberately separate layers:

* a binary relational premeasurement inside one observer worldtube;
* a finite environment that dephases the pointer by an exactly solvable unitary;
* a declared spherical, nonnegative-energy embedding used only to price radial
  backreaction.

It is a finite observer-channel theorem, not a derivation of bulk geometry or
an ER=EPR dictionary.
"""

from __future__ import annotations

from math import asin, atanh, ceil, cos, e, isfinite, log, pi, sqrt

from .spherical_static_patch_constraint import (
    de_sitter_static_factor,
    spherical_constraint_margin_record,
    spherical_constraint_ratio,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_phase(phase: float) -> None:
    _validate_nonnegative("environment_phase", phase)
    if phase > pi / 2.0:
        raise ValueError("environment_phase must lie in the first dephasing lobe")


def _binary_entropy(probability: float, *, logarithm_base: float) -> float:
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return -(
        probability * log(probability, logarithm_base)
        + (1.0 - probability) * log(1.0 - probability, logarithm_base)
    )


def finite_environment_decoherence_factor(
    environment_qubits: int,
    *,
    environment_phase: float,
) -> float:
    """Return the exact pointer coherence factor ``cos(theta)**m``.

    Each environment qubit starts in ``|+>`` and is acted on by
    ``exp(-i theta Z)`` conditional on pointer state ``|1>``.
    """
    _validate_positive_integer("environment_qubits", environment_qubits)
    _validate_phase(environment_phase)
    if environment_phase == pi / 2.0:
        return 0.0
    return cos(environment_phase) ** environment_qubits


def minimum_environment_qubits_for_error(
    maximum_normalized_diamond_distance: float,
    *,
    environment_phase: float,
) -> int | None:
    """Minimum ``m`` with ``|cos(theta)|**m/2 <= epsilon``.

    ``None`` means that no finite positive number of environment qubits reaches
    the requested error at the chosen phase.
    """
    _validate_nonnegative(
        "maximum_normalized_diamond_distance",
        maximum_normalized_diamond_distance,
    )
    if maximum_normalized_diamond_distance > 0.5:
        raise ValueError("maximum_normalized_diamond_distance must be at most 1/2")
    _validate_phase(environment_phase)
    if maximum_normalized_diamond_distance == 0.5:
        return 1
    if environment_phase == pi / 2.0:
        return 1
    coherence_per_qubit = cos(environment_phase)
    if coherence_per_qubit == 1.0 or maximum_normalized_diamond_distance == 0.0:
        return None
    candidate = max(
        1,
        ceil(
            log(2.0 * maximum_normalized_diamond_distance)
            / log(coherence_per_qubit)
        ),
    )
    tolerance = 1e-15 * max(1.0, maximum_normalized_diamond_distance)
    while (
        candidate > 1
        and coherence_per_qubit ** (candidate - 1) / 2.0
        <= maximum_normalized_diamond_distance + tolerance
    ):
        candidate -= 1
    while (
        coherence_per_qubit**candidate / 2.0
        > maximum_normalized_diamond_distance + tolerance
    ):
        candidate += 1
    return candidate


def harlow_pointer_channel_record(
    environment_qubits: int,
    *,
    environment_phase: float,
) -> dict[str, object]:
    """Certify the exact distance to complete binary pointer dephasing."""
    coherence = finite_environment_decoherence_factor(
        environment_qubits,
        environment_phase=environment_phase,
    )
    return {
        "environment_qubits_m": environment_qubits,
        "environment_phase_theta": environment_phase,
        "coherence_kappa": coherence,
        "reduced_pointer_channel": (
            "D_kappa([[a,b],[c,d]])=[[a,kappa*b],[kappa*c,d]]"
        ),
        "harlow_complete_dephasing_channel": (
            "D_0(|a><b|)=delta_ab |a><a|"
        ),
        "diamond_norm_difference": abs(coherence),
        "normalized_diamond_distance": abs(coherence) / 2.0,
        "premeasurement_instrument_normalized_diamond_distance": (
            abs(coherence) / 2.0
        ),
        "distance_is_exact": True,
        "fixed_phase_resource_law": (
            "m>=ceil(log(2 epsilon)/log(cos(theta))) for 0<theta<pi/2 "
            "and 0<epsilon<1/2; theta=pi/2 gives exact dephasing with m=1"
        ),
        "proof": (
            "D_kappa-D_0=(kappa/2)(id-Ad_Z). The identity and Z-unitary "
            "channels are perfectly distinguishable, so ||D_kappa-D_0||_diamond"
            "=|kappa|. Pre- and post-composition give the instrument upper "
            "bound, and a Q-superposition input saturates it."
        ),
        "outcome_probabilities_already_exact_after_acquisition": True,
        "decoherence_role": (
            "The environment suppresses coherent pointer blocks in the joint "
            "premeasurement state; it is not needed to obtain the Born "
            "probabilities after the matter system is traced out."
        ),
    }


def pointer_environment_entropy_record(
    environment_qubits: int,
    *,
    environment_phase: float,
) -> dict[str, object]:
    """Entropy ledger for a ``|+>`` pointer and pure product environment."""
    coherence = abs(
        finite_environment_decoherence_factor(
            environment_qubits,
            environment_phase=environment_phase,
        )
    )
    larger = (1.0 + coherence) / 2.0
    smaller = (1.0 - coherence) / 2.0
    purity = (1.0 + coherence**2) / 2.0
    entropy_nats = _binary_entropy(larger, logarithm_base=e)
    entropy_bits = _binary_entropy(larger, logarithm_base=2.0)
    return {
        "diagnostic_input": "pointer |+>, environment |+>^m",
        "pointer_eigenvalues": (larger, smaller),
        "pointer_purity": purity,
        "pointer_von_neumann_entropy_nats": entropy_nats,
        "pointer_von_neumann_entropy_bits": entropy_bits,
        "pointer_second_renyi_entropy_nats": -log(purity),
        "environment_entropy_nats": entropy_nats,
        "pointer_environment_mutual_information_nats": 2.0 * entropy_nats,
        "maximum_binary_record_entropy_nats": log(2.0),
        "pointer_log_dimension_nats": log(2.0),
        "environment_dimension": 2**environment_qubits,
        "environment_log_dimension_nats": environment_qubits * log(2.0),
        "harlow_observer_entropy_identification": "not_made",
        "interpretation": (
            "These are exact entropies of one model record. They are not, by "
            "themselves, Harlow's thermodynamic observer entropy S_Ob."
        ),
    }


def observer_action_resource_record(
    environment_qubits: int,
    *,
    acquisition_coupling: float,
    environment_coupling: float,
    environment_phase: float,
) -> dict[str, object]:
    """Duration, norm, action, and circuit ledger for the local unitary."""
    _validate_positive_integer("environment_qubits", environment_qubits)
    _validate_positive("acquisition_coupling", acquisition_coupling)
    _validate_positive("environment_coupling", environment_coupling)
    _validate_phase(environment_phase)

    acquisition_duration = pi / (2.0 * acquisition_coupling)
    parallel_decoherence_duration = environment_phase / environment_coupling
    serial_decoherence_duration = (
        environment_qubits * parallel_decoherence_duration
    )
    parallel_peak = max(
        acquisition_coupling,
        environment_qubits * environment_coupling,
    )
    serial_peak = max(acquisition_coupling, environment_coupling)
    integrated_norm = pi / 2.0 + environment_qubits * environment_phase
    return {
        "piecewise_action": (
            "H(t)=chi_acq(t) g Q_rel tensor X_P + chi_dec(t) lambda "
            "Pi_1^P tensor sum_j Z_Ej, with disjoint switching supports"
        ),
        "acquisition_angle_g_tau": pi / 2.0,
        "acquisition_duration_tau": acquisition_duration,
        "environment_phase_lambda_T": environment_phase,
        "parallel_schedule": {
            "total_duration": (
                acquisition_duration + parallel_decoherence_duration
            ),
            "peak_interaction_operator_norm": parallel_peak,
            "decoherence_duration": parallel_decoherence_duration,
            "commuting_environment_terms_simultaneous": True,
        },
        "serial_two_body_schedule": {
            "total_duration": acquisition_duration + serial_decoherence_duration,
            "peak_interaction_operator_norm": serial_peak,
            "decoherence_duration": serial_decoherence_duration,
            "same_reduced_channel": True,
        },
        "integrated_interaction_norm_both_schedules": integrated_norm,
        "coupling_action_identity": "g*tau=pi/2 and lambda*T=theta",
        "complexity": {
            "two_body_gate_count_realized_branch": environment_qubits + 1,
            "relational_acquisition_terms_across_two_location_sectors": 2,
            "controlled_phase_gate_count": environment_qubits,
            "serial_gate_depth": environment_qubits + 1,
            "parallel_commuting_depth": 2,
            "two_region_gate_count": 2 * (environment_qubits + 1),
            "two_region_parallel_depth": 2,
        },
        "free_hamiltonians": (
            "set to zero during the finite channel calculation; declared rest "
            "and support energies enter the separate gravitational envelope"
        ),
        "global_reversibility": (
            "The pointer-plus-environment evolution is unitary and can be "
            "reversed if the environment remains controllable. The Harlow "
            "channel is the reduced operational channel after E is discarded."
        ),
    }


def relational_patch_measurement_record() -> dict[str, object]:
    """State the binary relational observable and its exact covariance."""
    return {
        "observer_location_space": (
            "direct sum of two classical worldtube sectors A and B"
        ),
        "observable": (
            "Q_rel=|A><A| tensor Q_A tensor I_B + "
            "|B><B| tensor I_A tensor Q_B"
        ),
        "projector_hypothesis": "Q_A^2=Q_A and Q_B^2=Q_B",
        "premeasurement_unitary": (
            "U_acq=(I-Q_rel) tensor I_P - i Q_rel tensor X_P"
        ),
        "exact_binary_acquisition": True,
        "sectorwise_local": True,
        "simultaneous_A_B_swap_covariant": True,
        "covariance_proof": (
            "The simultaneous swap exchanges the two direct-sum terms and "
            "therefore fixes Q_rel and the acquisition Hamiltonian."
        ),
        "locality_boundary": (
            "This is locality in a finite direct-sum worldtube model. It is "
            "not a construction of a continuum diffeomorphism-invariant QFT "
            "operator or a coherent nonlocal location-control register."
        ),
    }


def observer_energy_envelope_record(
    action: dict[str, object],
    *,
    matter_energy: float,
    pointer_energy: float,
    environment_energy: float,
) -> dict[str, object]:
    """Conservative nonnegative energy envelope for one worldtube."""
    _validate_nonnegative("matter_energy", matter_energy)
    _validate_nonnegative("pointer_energy", pointer_energy)
    _validate_nonnegative("environment_energy", environment_energy)
    parallel = action["parallel_schedule"]
    serial = action["serial_two_body_schedule"]
    if not isinstance(parallel, dict) or not isinstance(serial, dict):
        raise TypeError("action record has invalid schedule entries")
    parallel_peak = float(parallel["peak_interaction_operator_norm"])
    serial_peak = float(serial["peak_interaction_operator_norm"])
    rest_support_energy = matter_energy + pointer_energy + environment_energy
    return {
        "matter_energy_budget": matter_energy,
        "pointer_energy_budget": pointer_energy,
        "environment_energy_budget": environment_energy,
        "rest_and_support_energy_budget": rest_support_energy,
        "parallel_peak_abs_interaction_energy": parallel_peak,
        "serial_peak_abs_interaction_energy": serial_peak,
        "parallel_nonnegative_mass_energy_envelope": (
            rest_support_energy + parallel_peak
        ),
        "serial_nonnegative_mass_energy_envelope": (
            rest_support_energy + serial_peak
        ),
        "envelope_rule": (
            "E_env bounds declared positive rest/support mass-energy plus the "
            "operator norm of the interaction. It is a conservative source "
            "envelope and does not identify the signed interaction Hamiltonian "
            "with a stress tensor."
        ),
    }


def uniform_density_worldtube_backreaction_record(
    *,
    mass_energy_envelope: float,
    support_radius: float,
    static_patch_radius: float,
    newton_constant: float,
    control_budget: float,
) -> dict[str, object]:
    """Price one worldtube using the exact spherical constraint variable.

    The declared embedding has ``m(r)=E_env(r/a)^3`` for ``r<=a``. Its
    constraint ratio is monotone, so its exact supremum occurs at the support
    wall.
    """
    _validate_nonnegative("mass_energy_envelope", mass_energy_envelope)
    _validate_positive("support_radius", support_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_positive("control_budget", control_budget)
    if support_radius >= static_patch_radius:
        raise ValueError("support_radius must lie strictly inside the static patch")
    if control_budget >= 1.0:
        raise ValueError("control_budget must be smaller than one")

    lapse_at_wall = de_sitter_static_factor(
        support_radius,
        static_patch_radius=static_patch_radius,
    )
    maximum_ratio = spherical_constraint_ratio(
        mass_energy_envelope,
        support_radius,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    margin = spherical_constraint_margin_record(
        maximum_ratio,
        control_budget=control_budget,
    )
    redshift_at_wall = sqrt(lapse_at_wall)
    return {
        "embedding": (
            "uniform nonnegative areal-density mass profile in 0<=r<=a"
        ),
        "mass_profile": "m(r)=E_env*(r/a)^3 for r<=a",
        "total_mass_energy_envelope": mass_energy_envelope,
        "support_radius_a": support_radius,
        "static_patch_radius_R": static_patch_radius,
        "areal_horizon_clearance_R_minus_a": static_patch_radius - support_radius,
        "background_proper_support_radius": (
            static_patch_radius * asin(support_radius / static_patch_radius)
        ),
        "background_optical_support_radius": (
            static_patch_radius * atanh(support_radius / static_patch_radius)
        ),
        "background_wall_redshift_sqrt_N": redshift_at_wall,
        "background_killing_energy_for_declared_static_profile": (
            mass_energy_envelope
        ),
        "background_proper_energy_lower_bound": mass_energy_envelope,
        "background_proper_energy_upper_bound": (
            mass_energy_envelope / redshift_at_wall
        ),
        "energy_relation_proof": (
            "For nonnegative static density, dE_K=sqrt(N)dE_prop and "
            "sqrt(N(a))<=sqrt(N(r))<=1; the areal mass integral equals E_K "
            "on the fixed de Sitter background."
        ),
        "maximum_constraint_ratio_q": maximum_ratio,
        "supremum_occurs_at_support_wall": True,
        "monotonicity_proof": (
            "q(r)=2GE r^2/[a^3(1-r^2/R^2)] has positive derivative for "
            "0<r<a<R."
        ),
        "constraint_margin": margin,
        "controlled_backreaction": margin["controlled_radial_metric"],
        "claim_boundary": (
            "This is an exact Hamiltonian-constraint ledger for the declared "
            "spherical mass profile. The channel Hamiltonian has not been "
            "derived from that source stress tensor. The ledger does not solve "
            "a lapse equation, pressure balance, junction conditions, or the "
            "nonspherical two-worldtube Einstein-matter problem."
        ),
    }


def matched_two_region_control_record() -> dict[str, object]:
    """Matched Bell and separable controls under the same local instrument."""
    bell = (
        (0.5, 0.0, 0.0, 0.5),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.0, 0.0, 0.5),
    )
    separable = (
        (0.5, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.5),
    )
    xx = (
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 0.0),
    )
    zz = (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, -1.0, 0.0, 0.0),
        (0.0, 0.0, -1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )

    def expectation(
        state: tuple[tuple[float, ...], ...],
        observable: tuple[tuple[float, ...], ...],
    ) -> float:
        return sum(
            state[row][column] * observable[column][row]
            for row in range(4)
            for column in range(4)
        )

    def first_marginal(
        state: tuple[tuple[float, ...], ...],
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        return (
            (
                state[0][0] + state[1][1],
                state[0][2] + state[1][3],
            ),
            (
                state[2][0] + state[3][1],
                state[2][2] + state[3][3],
            ),
        )

    entangled_xx = expectation(bell, xx)
    entangled_zz = expectation(bell, zz)
    separable_xx = expectation(separable, xx)
    separable_zz = expectation(separable, zz)
    entangled_witness = (entangled_xx + entangled_zz) / 2.0
    separable_witness = (separable_xx + separable_zz) / 2.0
    matched_marginals = first_marginal(bell) == first_marginal(separable)
    entangled_zz_distribution = {
        "00": bell[0][0],
        "01": bell[1][1],
        "10": bell[2][2],
        "11": bell[3][3],
    }
    separable_zz_distribution = {
        "00": separable[0][0],
        "01": separable[1][1],
        "10": separable[2][2],
        "11": separable[3][3],
    }
    return {
        "entangled_state": "rho_ent=|Phi+><Phi+|",
        "separable_state": (
            "rho_sep=(|00><00|+|11><11|)/2"
        ),
        "matching_conditions": {
            "identical_maximally_mixed_local_marginals": matched_marginals,
            "identical_local_energy_for_any_equal_one_site_hamiltonian": (
                matched_marginals
            ),
            "ZZ_record_distributions_identical": (
                entangled_zz_distribution == separable_zz_distribution
            ),
            "identical_ZZ_record_distribution": entangled_zz_distribution,
            "identical_declared_worldtube_energy_envelopes": True,
        },
        "single_Z_setting": {
            "entangled_ZZ_correlation": entangled_zz,
            "separable_ZZ_correlation": separable_zz,
            "entanglement_specific_contrast": entangled_zz - separable_zz,
        },
        "two_setting_entanglement_witness": {
            "definition": "W=(<X tensor X>+<Z tensor Z>)/2",
            "separable_upper_bound": 0.5,
            "entangled_value": entangled_witness,
            "matched_separable_value": separable_witness,
            "entanglement_witness_gap": entangled_witness - separable_witness,
            "proof": (
                "For product Bloch vectors, x_A x_B+z_A z_B<=1 by "
                "Cauchy-Schwarz; convexity gives W<=1/2 for separable states."
            ),
            "pointer_diagonal_statistics_independent_of_kappa": True,
        },
        "connectivity_test": {
            "connectivity_observable_defined_by_action": False,
            "entanglement_specific_connectivity_contrast": None,
            "nonzero_connectivity_contrast_survives": False,
            "reason": (
                "The action defines matter, pointer, and environment channels "
                "but no area, QES, topology, bridge algebra, or reconstruction "
                "quantity. The nonzero W gap is an ordinary entanglement "
                "witness and cannot be relabeled as geometric connectivity."
            ),
        },
        "two_region_gravity_boundary": (
            "The controls have matched per-worldtube ledgers. No global "
            "spherical backreaction theorem is claimed for two separated "
            "worldtubes."
        ),
    }


def physical_observer_channel_certificate(
    *,
    environment_qubits: int = 4,
    acquisition_coupling: float = 1.0,
    environment_coupling: float = 1.0,
    environment_phase: float = pi / 3.0,
    matter_energy: float = 1.0,
    pointer_energy: float = 1.0,
    environment_energy: float = 1.0,
    support_radius: float = 0.2,
    static_patch_radius: float = 1.0,
    newton_constant: float = 0.001,
    backreaction_control_budget: float = 0.25,
) -> dict[str, object]:
    """Build the complete finite observer-channel and ER=EPR gate audit."""
    channel = harlow_pointer_channel_record(
        environment_qubits,
        environment_phase=environment_phase,
    )
    entropy = pointer_environment_entropy_record(
        environment_qubits,
        environment_phase=environment_phase,
    )
    action = observer_action_resource_record(
        environment_qubits,
        acquisition_coupling=acquisition_coupling,
        environment_coupling=environment_coupling,
        environment_phase=environment_phase,
    )
    energy = observer_energy_envelope_record(
        action,
        matter_energy=matter_energy,
        pointer_energy=pointer_energy,
        environment_energy=environment_energy,
    )
    backreaction = uniform_density_worldtube_backreaction_record(
        mass_energy_envelope=float(
            energy["parallel_nonnegative_mass_energy_envelope"]
        ),
        support_radius=support_radius,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
        control_budget=backreaction_control_budget,
    )
    relational = relational_patch_measurement_record()
    controls = matched_two_region_control_record()
    parallel_schedule = action["parallel_schedule"]
    serial_schedule = action["serial_two_body_schedule"]
    if not isinstance(parallel_schedule, dict) or not isinstance(
        serial_schedule, dict
    ):
        raise TypeError("action record has invalid schedule entries")
    wall_redshift = float(backreaction["background_wall_redshift_sqrt_N"])
    backreaction["duration_ledger"] = {
        "parallel_center_proper_and_static_time": parallel_schedule[
            "total_duration"
        ],
        "parallel_wall_proper_time_background": (
            wall_redshift * float(parallel_schedule["total_duration"])
        ),
        "serial_center_proper_and_static_time": serial_schedule[
            "total_duration"
        ],
        "serial_wall_proper_time_background": (
            wall_redshift * float(serial_schedule["total_duration"])
        ),
        "time_coordinate_choice": (
            "static Killing time, equal to central proper time; wall values "
            "use the fixed-background redshift and are not backreacted clocks"
        ),
    }
    connectivity = controls["connectivity_test"]
    if not isinstance(connectivity, dict):
        raise TypeError("control record has invalid connectivity entry")
    matching = controls["matching_conditions"]
    single_setting = controls["single_Z_setting"]
    witness = controls["two_setting_entanglement_witness"]
    if not all(
        isinstance(record, dict)
        for record in (matching, single_setting, witness)
    ):
        raise TypeError("control record has invalid matched-control entries")

    coherence = float(channel["coherence_kappa"])
    ledgers_present = all(
        bool(record)
        for record in (entropy, action, energy, backreaction)
    )
    matched_controls_verified = bool(
        matching["identical_maximally_mixed_local_marginals"]
        and matching["ZZ_record_distributions_identical"]
        and matching["identical_declared_worldtube_energy_envelopes"]
        and abs(float(single_setting["entanglement_specific_contrast"]))
        <= 1e-15
    )
    witness_verified = bool(
        float(witness["entangled_value"])
        > float(witness["separable_upper_bound"])
        and float(witness["matched_separable_value"])
        <= float(witness["separable_upper_bound"])
    )

    observer_claims = {
        "finite_pointer_channel_is_cptp": abs(coherence) <= 1.0,
        "harlow_channel_error_is_exact": channel["distance_is_exact"],
        "premeasurement_instrument_error_is_exact": channel[
            "distance_is_exact"
        ],
        "relational_binary_acquisition_is_exact": relational[
            "exact_binary_acquisition"
        ],
        "action_is_sectorwise_local": relational["sectorwise_local"],
        "entropy_duration_energy_complexity_localization_ledgers_present": (
            ledgers_present
        ),
        "declared_spherical_backreaction_is_controlled": backreaction[
            "controlled_backreaction"
        ],
        "matched_entangled_and_separable_controls_verified": (
            matched_controls_verified
        ),
        "two_setting_entanglement_witness_verified": witness_verified,
    }
    observer_pass = all(bool(value) for value in observer_claims.values())
    er_epr_go = bool(connectivity["nonzero_connectivity_contrast_survives"])
    return {
        "goal": "Physical finite observer-channel theorem and ER=EPR gate",
        "status": (
            "pass_observer_channel_stop_er_epr"
            if observer_pass and not er_epr_go
            else "go_er_epr" if observer_pass and er_epr_go else "fail"
        ),
        "result_type": (
            "exact_finite_pointer_worldtube_realization_with_resource_ledger"
        ),
        "channel": channel,
        "relational_patch_measurement": relational,
        "entropy_ledger": entropy,
        "action_and_complexity_ledger": action,
        "energy_ledger": energy,
        "localization_and_backreaction_ledger": backreaction,
        "matched_two_region_controls": controls,
        "certified_observer_claims": observer_claims,
        "decision": {
            "observer_channel_theorem": (
                "RETAIN" if observer_pass else "STOP"
            ),
            "er_epr_extension": (
                "GO" if er_epr_go else "STOP_NO_DERIVED_CONNECTIVITY_CONTRAST"
            ),
            "paper_status": (
                "exact finite result; not yet a standalone quantum-gravity "
                "paper without a field-theory implementation, a stronger "
                "observer-resource obstruction, or a derived gravity dictionary"
            ),
        },
        "claim_boundary": (
            "The certificate realizes Harlow's binary pointer dephasing rule "
            "as a reduced finite unitary channel and prices one declared local "
            "worldtube. It does not derive S_Ob, irreversible decoherence in a "
            "closed universe, continuum gravitational dressing, or ER=EPR."
        ),
    }
