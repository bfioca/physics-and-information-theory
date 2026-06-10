"""Same-target clock-only versus charged-rotation-reference achievability bound.

The finite-wall conformal scalar supplies target spins
``L_delta=Theta(sqrt(R/delta))`` in a hard static-energy window.  On a fixed
spin sector, the clock-only compact expectation is completely depolarizing.
By contrast, the truncated SO(3) Peter-Weyl reference has an explicit covariant
measure-and-correct decoder.  This module combines the two exact results and
records a sufficient reference-cutoff and rigid-rotor Casimir cost.
"""

from __future__ import annotations

from math import ceil, isfinite

from .operational_su2_reference import (
    peter_weyl_closed_deficit_fraction,
    peter_weyl_mean_casimir_fraction,
    peter_weyl_reference_dimension,
)
from .redshifted_frame_capacity import (
    finite_wall_ground_frequency_upper_bound,
    maximum_bounded_energy_angular_momentum,
)
from .scalar_clock_rotation_no_go import (
    fixed_spin_replacer_optimal_normalized_diamond_error,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_spin(system_spin: int) -> None:
    if (
        isinstance(system_spin, bool)
        or not isinstance(system_spin, int)
        or system_spin < 1
    ):
        raise ValueError("system_spin must be a positive integer")


def peter_weyl_constructive_diamond_upper_bound(
    system_spin: int,
    reference_cutoff: int,
) -> float:
    """Closed constructive diamond bound for ``J>=L``."""
    _validate_spin(system_spin)
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < system_spin
    ):
        raise ValueError("reference_cutoff must be an integer at least system_spin")
    dimension = 2 * system_spin + 1
    maximum_deficit = peter_weyl_closed_deficit_fraction(
        reference_cutoff,
        2 * system_spin,
    )
    return min(1.0, dimension * float(maximum_deficit) / 2.0)


def peter_weyl_simple_diamond_bound(
    system_spin: int,
    reference_cutoff: int,
) -> float:
    """Elementary upper bound ``3(2L+1)^2/(8J)`` for ``J>=L``."""
    _validate_spin(system_spin)
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < system_spin
    ):
        raise ValueError("reference_cutoff must be an integer at least system_spin")
    dimension = 2 * system_spin + 1
    return min(1.0, 3.0 * dimension * dimension / (8.0 * reference_cutoff))


def sufficient_peter_weyl_reference_cutoff(
    system_spin: int,
    target_error: float,
) -> int:
    """Cutoff ensuring the constructive diamond upper bound is ``<=epsilon``."""
    _validate_spin(system_spin)
    _validate_positive("target_error", target_error)
    if target_error >= 1.0:
        raise ValueError("target_error must be smaller than one")
    dimension = 2 * system_spin + 1
    return max(
        system_spin,
        ceil(3.0 * dimension * dimension / (8.0 * target_error)),
    )


def peter_weyl_rotor_mean_energy(
    reference_cutoff: int,
    *,
    moment_of_inertia: float,
) -> float:
    """Mean energy for ``H_ref=C_left/(2 I)`` in the canonical token."""
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    _validate_positive("moment_of_inertia", moment_of_inertia)
    mean_casimir = peter_weyl_mean_casimir_fraction(reference_cutoff)
    return float(mean_casimir) / (2.0 * moment_of_inertia)


def redshifted_rotation_reference_tradeoff_record(
    *,
    radius: float,
    stretched_distance: float,
    field_energy_budget: float,
    inner_offset: float,
    outer_offset: float,
    target_recovery_error: float,
    rotor_moment_of_inertia: float,
) -> dict[str, object]:
    """Compare clock-only and Peter-Weyl reference recovery at one wall."""
    maximum_spin = maximum_bounded_energy_angular_momentum(
        radius=radius,
        stretched_distance=stretched_distance,
        energy_budget=field_energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    if maximum_spin < 1:
        raise ValueError("parameters must certify at least one nontrivial spin sector")
    reference_cutoff = sufficient_peter_weyl_reference_cutoff(
        maximum_spin,
        target_recovery_error,
    )
    constructive_upper_bound = peter_weyl_constructive_diamond_upper_bound(
        maximum_spin,
        reference_cutoff,
    )
    simple_bound = peter_weyl_simple_diamond_bound(
        maximum_spin,
        reference_cutoff,
    )
    mean_casimir = peter_weyl_mean_casimir_fraction(reference_cutoff)
    rotor_energy = peter_weyl_rotor_mean_energy(
        reference_cutoff,
        moment_of_inertia=rotor_moment_of_inertia,
    )
    return {
        "de_sitter_radius_R": radius,
        "stretched_horizon_gap_delta": stretched_distance,
        "field_static_energy_budget_E0": field_energy_budget,
        "maximum_hard_energy_target_spin_L_delta": maximum_spin,
        "target_dimension_d": 2 * maximum_spin + 1,
        "variational_ground_frequency_upper_bound": (
            finite_wall_ground_frequency_upper_bound(
                maximum_spin,
                radius=radius,
                stretched_distance=stretched_distance,
                inner_offset=inner_offset,
                outer_offset=outer_offset,
            )
        ),
        "clock_only_optimal_normalized_diamond_error": (
            fixed_spin_replacer_optimal_normalized_diamond_error(maximum_spin)
        ),
        "target_charged_reference_error_epsilon": target_recovery_error,
        "sufficient_peter_weyl_cutoff_J": reference_cutoff,
        "peter_weyl_reference_dimension": peter_weyl_reference_dimension(
            reference_cutoff
        ),
        "charged_reference_constructive_diamond_error_upper_bound": (
            constructive_upper_bound
        ),
        "elementary_diamond_error_upper_bound": simple_bound,
        "mean_left_casimir_exact": str(mean_casimir),
        "mean_left_casimir": float(mean_casimir),
        "rotor_moment_of_inertia_I": rotor_moment_of_inertia,
        "rotor_inertia_scaling_assumption": (
            "I is fixed independently of delta and target error epsilon"
        ),
        "mean_rigid_rotor_reference_energy": rotor_energy,
        "scaled_reference_cutoff_J_epsilon_delta_over_R": (
            reference_cutoff
            * target_recovery_error
            * stretched_distance
            / radius
        ),
        "scaled_rotor_energy_I_epsilon_squared_delta_squared_over_R_squared": (
            rotor_energy
            * rotor_moment_of_inertia
            * target_recovery_error**2
            * (stretched_distance / radius) ** 2
        ),
        "reference_hamiltonian": "H_ref=C_left/(2 I)",
        "reference_lifetime_status": (
            "instantaneous channel benchmark; coherent rotor phase evolution and "
            "observer-time tracking are not controlled"
        ),
        "decoder": "canonical SO(3) Peter-Weyl covariant measure-and-correct channel",
        "exact_recovery_at_finite_reference_cutoff": False,
    }


def redshifted_rotation_reference_tradeoff_certificate(
    *,
    radius: float = 1.0,
    field_energy_budget: float = 4.0,
    inner_offset: float = 0.5,
    outer_offset: float = 1.5,
    target_recovery_error: float = 0.1,
    rotor_moment_of_inertia: float = 1.0,
    minimum_power: int = 64,
    steps: int = 6,
) -> dict[str, object]:
    """Audit the same-target redshifted clock/reference comparison."""
    _validate_positive("radius", radius)
    _validate_positive("field_energy_budget", field_energy_budget)
    _validate_positive("target_recovery_error", target_recovery_error)
    _validate_positive("rotor_moment_of_inertia", rotor_moment_of_inertia)
    if target_recovery_error >= 1.0:
        raise ValueError("target_recovery_error must be smaller than one")
    if (
        isinstance(minimum_power, bool)
        or not isinstance(minimum_power, int)
        or minimum_power < 8
    ):
        raise ValueError("minimum_power must be an integer at least eight")
    if (
        isinstance(steps, bool)
        or not isinstance(steps, int)
        or steps < 3
        or steps > 64
    ):
        raise ValueError("steps must be an integer from three through sixty-four")
    records = tuple(
        redshifted_rotation_reference_tradeoff_record(
            radius=radius,
            stretched_distance=radius / float(minimum_power * 4**index),
            field_energy_budget=field_energy_budget,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
            target_recovery_error=target_recovery_error,
            rotor_moment_of_inertia=rotor_moment_of_inertia,
        )
        for index in range(steps)
    )
    cutoff_scalings = tuple(
        record["scaled_reference_cutoff_J_epsilon_delta_over_R"]
        for record in records
    )
    energy_scalings = tuple(
        record[
            "scaled_rotor_energy_I_epsilon_squared_delta_squared_over_R_squared"
        ]
        for record in records
    )
    certified_claims = {
        "hard_field_energy_target_exists_at_every_wall": all(
            record["variational_ground_frequency_upper_bound"]
            <= field_energy_budget
            for record in records
        ),
        "clock_only_error_approaches_one": (
            all(
                right > left
                for left, right in zip(
                    (
                        record["clock_only_optimal_normalized_diamond_error"]
                        for record in records
                    ),
                    (
                        record["clock_only_optimal_normalized_diamond_error"]
                        for record in records[1:]
                    ),
                )
            )
            and records[-1]["clock_only_optimal_normalized_diamond_error"] > 0.9999
        ),
        "charged_reference_meets_target_error": all(
            record["charged_reference_constructive_diamond_error_upper_bound"]
            <= target_recovery_error
            for record in records
        ),
        "elementary_bound_dominates_closed_constructive_upper_bound": all(
            record["charged_reference_constructive_diamond_error_upper_bound"]
            <= record["elementary_diamond_error_upper_bound"]
            <= target_recovery_error
            for record in records
        ),
        "sampled_cutoff_scaling_is_consistent_with_R_over_epsilon_delta": (
            max(cutoff_scalings[-3:]) - min(cutoff_scalings[-3:])
            < 0.08 * max(cutoff_scalings[-3:])
        ),
        "sampled_fixed_inertia_energy_scaling_is_consistent_with_inverse_delta_squared": (
            max(energy_scalings[-3:]) - min(energy_scalings[-3:])
            < 0.12 * max(energy_scalings[-3:])
        ),
    }
    return {
        "goal": "Redshifted Rotation-Reference Achievability Bound",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "status_scope": (
            "exact algebraic inequalities plus sampled asymptotic consistency; "
            "the asymptotic laws follow analytically, not from the sample thresholds"
        ),
        "result_type": "same_target_clock_only_and_charged_so3_achievability_bound",
        "central_result": (
            "For hard-energy horizon spins L_delta=Theta(sqrt(R/delta)), the "
            "clock-only compact expectation has exact optimal recovery error "
            "1-1/(2L_delta+1)^2. The canonical charged SO(3) Peter-Weyl reference "
            "achieves error at most epsilon with the sufficient cutoff "
            "J=ceil(3(2L_delta+1)^2/(8 epsilon)). Its rigid-rotor mean Casimir "
            "energy scales as R^2/(I epsilon^2 delta^2) when I is held fixed "
            "independently of delta and epsilon."
        ),
        "claim_boundary": (
            "free conformal one-particle target at a finite Dirichlet wall, compact "
            "SO(3) only, chosen rigid-rotor Hamiltonian H_ref=C_left/(2I), and a "
            "constructive decoder not proved optimal, with I fixed independently "
            "of delta and epsilon; no lifetime or coherent phase-tracking bound, "
            "no local coupling of the "
            "reference to the Bunch-Davies net, noncompact SO(1,4) boosts, physical "
            "gravitational constraint, backreaction bound, Type-II trace, or "
            "generalized-entropy identity"
        ),
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "derive the reference inertia and coupling from a covariant static-"
            "patch observer, extend the compact decoder to regulated SO(1,d), and "
            "test whether backreaction enforces or changes the inverse-delta cost"
        ),
    }
