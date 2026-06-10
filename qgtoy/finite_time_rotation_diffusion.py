"""Finite-time rotational diffusion toward the prepared-reference twirl.

The model uses the collective rotation generators

    Q_a = J_a^(target) + J_a^(reference)

and the isotropic random-unitary semigroup

    d rho/d tau = -gamma sum_a [Q_a,[Q_a,rho]].

Its channel is convolution with the ``SO(3)`` heat kernel.  At finite proper
time it is identity-starting; at long time it converges to Haar twirling.  The
total-variation distance of the heat-kernel density gives a representation-
independent normalized diamond-distance bound.  This lets the finite-time
error be subtracted from the existing mean-Casimir recovery obstruction without
introducing a hard Peter-Weyl cutoff.

The open-system generator is time-local/Markovian in observer proper time but
collective in the target angular charge.  It is not yet a spatially local
field-top derivation.
"""

from __future__ import annotations

from math import exp, expm1, isfinite, log, sqrt

from .finite_size_static_patch_observer import (
    energy_constrained_rotor_recovery_bound_record,
)


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_system_spin(system_spin: int) -> None:
    if (
        isinstance(system_spin, bool)
        or not isinstance(system_spin, int)
        or system_spin < 1
    ):
        raise ValueError("system_spin must be a positive integer")


def _validate_tensor_rank(tensor_rank: int) -> None:
    if (
        isinstance(tensor_rank, bool)
        or not isinstance(tensor_rank, int)
        or tensor_rank < 0
    ):
        raise ValueError("tensor_rank must be a nonnegative integer")


def so3_heat_multiplier(tensor_rank: int, dimensionless_time: float) -> float:
    """Return the central heat-semigroup multiplier on rank ``tensor_rank``.

    Peter-Weyl rank ``ell`` carries the scalar multiplier

        exp[-s ell(ell+1)].

    The formula makes the identity start, semigroup law, and nontrivial-rank
    Haar limit directly testable without treating prose flags as certificates.
    """
    _validate_tensor_rank(tensor_rank)
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    return exp(-dimensionless_time * tensor_rank * (tensor_rank + 1))


def so3_heat_kernel_l2_distance_upper_bound(dimensionless_time: float) -> float:
    """Bound ``||k_s-1||_2`` for the central ``SO(3)`` heat kernel.

    With the convention

        k_s(g)=sum_(j>=0) (2j+1) exp[-s j(j+1)] chi_j(g),

    Peter-Weyl orthogonality gives

        ||k_s-1||_2^2=sum_(j>=1)(2j+1)^2 exp[-2s j(j+1)].

    Since ``j(j+1)>=2j``, putting ``q=exp(-4s)`` bounds this series by

        q(9-2q+q^2)/(1-q)^3.
    """
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    if dimensionless_time == 0.0:
        return float("inf")
    q = exp(-4.0 * dimensionless_time)
    one_minus_q = -expm1(-4.0 * dimensionless_time)
    denominator = one_minus_q**3
    if denominator == 0.0:
        return float("inf")
    squared_bound = q * (9.0 - 2.0 * q + q * q) / denominator
    return sqrt(squared_bound)


def finite_time_twirl_distance_record(
    proper_time: float,
    *,
    diffusion_rate: float,
) -> dict[str, object]:
    """Return a normalized diamond bound from finite-time diffusion to Haar.

    The difference of two random-unitary channels is bounded in diamond norm by
    the ``L1`` distance of their probability densities. Haar normalization and
    Cauchy-Schwarz give

        (1/2)||N_T-N_Haar||_diamond
          <= (1/2)||k_(gamma T)-1||_1
          <= (1/2)||k_(gamma T)-1||_2.

    The bound is independent of target/reference representation and state.
    """
    _validate_nonnegative("proper_time", proper_time)
    _validate_positive("diffusion_rate", diffusion_rate)
    dimensionless_time = diffusion_rate * proper_time
    if dimensionless_time == 0.0:
        l2_bound = float("inf")
        normalized_diamond_bound = 1.0
        q = 1.0
    else:
        l2_bound = so3_heat_kernel_l2_distance_upper_bound(dimensionless_time)
        normalized_diamond_bound = min(1.0, 0.5 * l2_bound)
        q = exp(-4.0 * dimensionless_time)
    return {
        "proper_time_T": proper_time,
        "diffusion_rate_gamma": diffusion_rate,
        "dimensionless_diffusion_time_s": dimensionless_time,
        "heat_kernel_q_exp_minus_4s": q,
        "heat_kernel_l2_distance_upper_bound": l2_bound,
        "normalized_diamond_distance_to_haar_upper_bound": (
            normalized_diamond_bound
        ),
        "channel": (
            "N_(eta,T)(rho)=integral_SO3 dg k_(gamma T)(g) "
            "U_L(g)rho U_L(g)^* tensor U_R(g)eta U_R(g)^*"
        ),
        "haar_limit": (
            "N_(eta,infinity)(rho)=integral_SO3 dg U_L(g)rho U_L(g)^* "
            "tensor U_R(g)eta U_R(g)^*"
        ),
        "bound_formula": (
            "min(1,0.5*sqrt(q*(9-2q+q^2)/(1-q)^3)), q=exp(-4 gamma T)"
        ),
        "representation_independent": True,
    }


def minimum_diffusion_time_for_twirl_distance(
    target_distance: float,
    *,
    diffusion_rate: float,
) -> float:
    """Smallest time certified by the analytic heat-kernel distance bound."""
    _validate_positive("target_distance", target_distance)
    if target_distance >= 1.0:
        raise ValueError("target_distance must be smaller than one")
    _validate_positive("diffusion_rate", diffusion_rate)

    low = 0.0
    high = 1.0 / diffusion_rate
    while (
        finite_time_twirl_distance_record(
            high,
            diffusion_rate=diffusion_rate,
        )["normalized_diamond_distance_to_haar_upper_bound"]
        > target_distance
    ):
        high *= 2.0
    for _ in range(96):
        middle = 0.5 * (low + high)
        bound = finite_time_twirl_distance_record(
            middle,
            diffusion_rate=diffusion_rate,
        )["normalized_diamond_distance_to_haar_upper_bound"]
        if bound <= target_distance:
            high = middle
        else:
            low = middle
    return high


def finite_time_energy_constrained_recovery_record(
    system_spin: int,
    *,
    maximum_mean_casimir: float,
    proper_time: float,
    diffusion_rate: float,
) -> dict[str, object]:
    """Transfer the Haar recovery obstruction to finite diffusion time."""
    _validate_system_spin(system_spin)
    _validate_nonnegative("maximum_mean_casimir", maximum_mean_casimir)
    twirl = finite_time_twirl_distance_record(
        proper_time,
        diffusion_rate=diffusion_rate,
    )
    haar = energy_constrained_rotor_recovery_bound_record(
        system_spin,
        maximum_mean_casimir=maximum_mean_casimir,
    )
    finite_time_correction = twirl[
        "normalized_diamond_distance_to_haar_upper_bound"
    ]
    corrected = max(
        0.0,
        haar["normalized_diamond_error_lower_bound"] - finite_time_correction,
    )
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": 2 * system_spin + 1,
        "maximum_mean_left_casimir": maximum_mean_casimir,
        "proper_time_T": proper_time,
        "diffusion_rate_gamma": diffusion_rate,
        "haar_energy_constrained_error_lower_bound": haar[
            "normalized_diamond_error_lower_bound"
        ],
        "finite_time_twirl_distance_upper_bound": finite_time_correction,
        "finite_time_any_decoder_error_lower_bound": corrected,
        "haar_optimizer_record": haar["optimizer_record"],
        "transfer_formula": "max(0,epsilon_Haar(Cbar,L)-eta_heat(gamma T))",
        "proof_mechanism": (
            "decoder contractivity and the triangle inequality transfer the "
            "Haar append-and-twirl lower bound to the finite-time heat channel"
        ),
        "scope": (
            "all prepared L2(SO(3)) rotor states with mean Casimir at most Cbar, "
            "the collective SO(3) diffusion channel, and every deterministic "
            "CPTP decoder acting only on the target-plus-rotor output; no bath "
            "purification, Brownian record, pre-correlated encoder, or postselection"
        ),
    }


def logarithmic_diffusion_schedule_record(
    system_spin: int,
    *,
    maximum_mean_casimir: float,
    diffusion_rate: float,
) -> dict[str, object]:
    """Choose ``gamma T=(1/2)log d`` and record the resulting correction."""
    _validate_system_spin(system_spin)
    _validate_nonnegative("maximum_mean_casimir", maximum_mean_casimir)
    _validate_positive("diffusion_rate", diffusion_rate)
    dimension = 2 * system_spin + 1
    proper_time = log(float(dimension)) / (2.0 * diffusion_rate)
    record = finite_time_energy_constrained_recovery_record(
        system_spin,
        maximum_mean_casimir=maximum_mean_casimir,
        proper_time=proper_time,
        diffusion_rate=diffusion_rate,
    )
    elementary_distance_bound = (
        1.5
        / float(dimension)
        / (1.0 - 1.0 / float(dimension**2)) ** 1.5
    )
    return {
        **record,
        "schedule": "gamma T=(1/2)log d",
        "scheduled_proper_time": proper_time,
        "elementary_O_1_over_d_distance_bound": elementary_distance_bound,
        "computed_bound_respects_elementary_schedule_bound": (
            record["finite_time_twirl_distance_upper_bound"]
            <= elementary_distance_bound
        ),
        "static_patch_scaling": (
            "if gamma is cutoff independent, the sufficient choice for "
            "d_delta=Theta(sqrt(R/delta)) is T_delta="
            "Theta(gamma^-1 log(R/delta))"
        ),
    }


def collective_rotation_diffusion_model_record() -> dict[str, object]:
    """State the open-system model and its precise physical boundary."""
    return {
        "collective_generators": "Q_a=J_a^(target)+J_a^(rotor,left)",
        "proper_time_master_equation": (
            "d rho/d tau=-gamma sum_(a=1)^3 [Q_a,[Q_a,rho]]"
        ),
        "gksl_operators": "L_a=sqrt(2 gamma) Q_a",
        "stochastic_hamiltonian_realization": (
            "Stratonovich H_noise(tau)=sum_a xi_a(tau)Q_a with isotropic white-noise "
            "covariance E[xi_a(tau)xi_b(tau')]=2 gamma delta_ab delta(tau-tau')"
        ),
        "finite_time_channel_is_so3_heat_kernel_twirling": True,
        "identity_starting_strongly_continuous_semigroup": True,
        "conserves_rotational_covariance": True,
        "picture": (
            "interaction picture relative to the free target and spherical-top "
            "Hamiltonians, assuming [H_target+H_rot,Q_a]=0 or a specified "
            "toggling control that makes Q_a interaction-picture constant"
        ),
        "environment_record_is_inaccessible": True,
        "locality_status": (
            "time-local/Markovian in observer proper time but collective in the "
            "target angular charge; a spatially local current coupling and bath "
            "derivation remain open"
        ),
        "bath_assumptions": (
            "isotropic Markov noise, Born/white-noise limit, initially uncorrelated "
            "bath, perfectly correlated equal-strength common-mode torque on target "
            "and rotor, and no finite-memory or dissipative energy exchange term"
        ),
        "common_mode_spatial_kernel": (
            "rank-one covariance on target and rotor support, producing the same "
            "active discarded-bath stochastic rotation on both subsystems"
        ),
        "passive_frame_uncertainty_is_not_this_dynamics": (
            "averaging over an unknown frame is epistemic coarse graining rather "
            "than a physical open-system interaction"
        ),
        "unbounded_rotor_generator_scope": (
            "the random-unitary heat channel is the mild semigroup on full "
            "L2(SO(3)); the displayed double-commutator equation holds on its "
            "natural strong-generator domain"
        ),
        "finite_bath_derivation_status": (
            "an approximate quantum-bath derivation would additionally require "
            "finite correlation time, an isotropic zero-frequency spectrum, Lamb-"
            "shift control, and an explicit Davies/Markov approximation error"
        ),
        "ordinary_local_rotor_bath_is_not_sufficient": (
            "rotor-only torque generates J_a^(rotor) diffusion rather than the "
            "collective Q_a heat twirl"
        ),
    }


def finite_time_rotation_diffusion_certificate(
    *,
    maximum_system_spin: int = 512,
    maximum_mean_casimir: float = 10.0,
    diffusion_rate: float = 1.0,
    target_twirl_distance: float = 0.05,
) -> dict[str, object]:
    """Audit the finite-time collective-diffusion recovery theorem."""
    _validate_system_spin(maximum_system_spin)
    _validate_nonnegative("maximum_mean_casimir", maximum_mean_casimir)
    _validate_positive("diffusion_rate", diffusion_rate)
    _validate_positive("target_twirl_distance", target_twirl_distance)
    if target_twirl_distance >= 1.0:
        raise ValueError("target_twirl_distance must be smaller than one")

    mixing_time = minimum_diffusion_time_for_twirl_distance(
        target_twirl_distance,
        diffusion_rate=diffusion_rate,
    )
    time_records = tuple(
        finite_time_energy_constrained_recovery_record(
            maximum_system_spin,
            maximum_mean_casimir=maximum_mean_casimir,
            proper_time=scale * mixing_time,
            diffusion_rate=diffusion_rate,
        )
        for scale in (0.0, 0.5, 1.0, 2.0)
    )
    schedule_spins = tuple(
        spin
        for spin in (2, 8, 32, 128, maximum_system_spin)
        if spin <= maximum_system_spin
    )
    if maximum_system_spin not in schedule_spins:
        schedule_spins = (*schedule_spins, maximum_system_spin)
    schedule_records = tuple(
        logarithmic_diffusion_schedule_record(
            spin,
            maximum_mean_casimir=maximum_mean_casimir,
            diffusion_rate=diffusion_rate,
        )
        for spin in schedule_spins
    )
    distances = tuple(
        record["finite_time_twirl_distance_upper_bound"] for record in time_records
    )
    recovery_bounds = tuple(
        record["finite_time_any_decoder_error_lower_bound"]
        for record in time_records
    )
    sample_ranks = tuple(range(5))
    first_time = 0.23
    second_time = 0.41
    identity_multipliers = tuple(
        so3_heat_multiplier(rank, 0.0) for rank in sample_ranks
    )
    semigroup_residuals = tuple(
        abs(
            so3_heat_multiplier(rank, first_time + second_time)
            - so3_heat_multiplier(rank, first_time)
            * so3_heat_multiplier(rank, second_time)
        )
        for rank in sample_ranks
    )
    late_multipliers = tuple(
        so3_heat_multiplier(rank, 20.0) for rank in sample_ranks[1:]
    )
    certified_claims = {
        "heat_multipliers_certify_identity_semigroup_and_haar_limit": (
            all(multiplier == 1.0 for multiplier in identity_multipliers)
            and max(semigroup_residuals) < 1.0e-14
            and all(0.0 <= multiplier < 1.0e-16 for multiplier in late_multipliers)
        ),
        "heat_kernel_distance_bound_decreases_with_time": all(
            right <= left for left, right in zip(distances, distances[1:])
        ),
        "certified_mixing_time_meets_target": distances[2]
        <= target_twirl_distance,
        "finite_time_recovery_obstruction_strengthens_with_time": all(
            right >= left
            for left, right in zip(recovery_bounds, recovery_bounds[1:])
        ),
        "longer_sample_recovers_nontrivial_haar_obstruction": (
            recovery_bounds[-1] > 0.0
        ),
        "logarithmic_schedule_has_O_1_over_d_twirl_correction": all(
            record["computed_bound_respects_elementary_schedule_bound"]
            for record in schedule_records
        ),
        "logarithmic_schedule_lower_bound_improves_with_target_dimension": all(
            right["finite_time_any_decoder_error_lower_bound"]
            >= left["finite_time_any_decoder_error_lower_bound"]
            for left, right in zip(schedule_records, schedule_records[1:])
        ),
    }
    return {
        "goal": "Finite-Time Rotation Diffusion Toward Haar Twirling",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "finite_time_collective_rotation_diffusion_recovery_bound",
        "central_result": (
            "Collective isotropic SO(3) diffusion is an identity-starting "
            "random-unitary semigroup converging to Haar append-and-twirl. Its "
            "normalized diamond distance is at most half the heat-kernel L2 "
            "distance, yielding epsilon_T>=max(0,epsilon_Haar-eta_heat)."
        ),
        "sufficient_protocol_time_scaling": (
            "Choosing gamma T=(1/2)log(2L+1) makes the finite-time correction "
            "O(1/L). If gamma is cutoff independent, then on "
            "L_delta=Theta(sqrt(R/delta)) this sufficient choice grows as "
            "Theta(gamma^-1 log(R/delta)); no matching mixing lower bound is claimed."
        ),
        "model": collective_rotation_diffusion_model_record(),
        "claim_boundary": (
            "conditional Markovian collective-charge open-system model, time-local "
            "in proper time but not yet derived from a spatially local static-patch "
            "field-top interaction; compact SO(3), deterministic decoders after "
            "the finite-time channel acting only on target plus rotor, inaccessible "
            "Brownian environment record and bath purification, constant interaction-"
            "picture Q_a from rotational invariance or toggling control, no boosts, "
            "bath memory, "
            "postselection, or controlled gravitational stress tensor"
        ),
        "certified_claims": certified_claims,
        "target_twirl_distance": target_twirl_distance,
        "certified_mixing_time": mixing_time,
        "time_records": time_records,
        "logarithmic_schedule_records": schedule_records,
        "heat_multiplier_audit": {
            "sample_ranks": sample_ranks,
            "identity_multipliers": identity_multipliers,
            "semigroup_residuals": semigroup_residuals,
            "late_nontrivial_multipliers": late_multipliers,
        },
        "next_physics_gate": (
            "derive the isotropic noise kernel and collective charge coupling from "
            "a spatially local static-patch current interaction, then control bath "
            "memory, observer lifetime, and stress-energy backreaction"
        ),
    }
