"""Hamiltonian-identifiability no-go for a covariant rotation reference.

The Peter-Weyl token, orientation POVM, and recovery channel depend on the
``SO(3)`` representation and prepared state, not on a separately assigned
reference Hamiltonian.  On a cutoff ``J`` reference, every positive multiple
of the left Casimir is rotation invariant.  Its coefficient can therefore be
chosen to realize any positive ground-subtracted token energy without changing
recovery.

This is a no-go for inferring an energy or backreaction law from covariance and
channel accuracy alone.  It is not a claim that a specified physical observer
action permits arbitrary energy assignments.
"""

from __future__ import annotations

from math import isfinite

from .operational_su2_reference import peter_weyl_mean_casimir_fraction
from .redshifted_frame_capacity import maximum_bounded_energy_angular_momentum
from .redshifted_rotation_reference_tradeoff import (
    peter_weyl_constructive_diamond_upper_bound,
    peter_weyl_rotor_mean_energy,
    sufficient_peter_weyl_reference_cutoff,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nontrivial_cutoff(reference_cutoff: int) -> None:
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 1
    ):
        raise ValueError("reference_cutoff must be a positive integer")


def casimir_hamiltonian_assignment(
    reference_cutoff: int,
    *,
    prescribed_token_excitation_energy: float,
) -> dict[str, object]:
    """Assign ``H=a C_left`` to realize prescribed ground-subtracted energy.

    The canonical cutoff token has exact mean Casimir ``3J(J+2)/5``.  Thus
    ``a=E/<C_left>`` and the equivalent rotor inertia is ``I=1/(2a)``.
    """
    _validate_nontrivial_cutoff(reference_cutoff)
    _validate_positive(
        "prescribed_token_excitation_energy",
        prescribed_token_excitation_energy,
    )
    mean_casimir = peter_weyl_mean_casimir_fraction(reference_cutoff)
    coefficient = prescribed_token_excitation_energy / float(mean_casimir)
    moment_of_inertia = 1.0 / (2.0 * coefficient)
    realized_energy = coefficient * float(mean_casimir)
    return {
        "reference_cutoff_J": reference_cutoff,
        "mean_left_casimir_exact": str(mean_casimir),
        "mean_left_casimir": float(mean_casimir),
        "hamiltonian": "H_ref=a_J C_left",
        "casimir_coefficient_a_J": coefficient,
        "equivalent_rotor_moment_of_inertia_I_J": moment_of_inertia,
        "ground_energy": 0.0,
        "prescribed_token_excitation_energy": prescribed_token_excitation_energy,
        "realized_token_excitation_energy": realized_energy,
        "rotation_invariance": "[H_ref,U_left(g)]=0",
    }


def covariant_observer_energy_no_go_record(
    *,
    radius: float,
    stretched_distance: float,
    field_energy_budget: float,
    inner_offset: float,
    outer_offset: float,
    target_recovery_error: float,
    energy_scale: float,
    fixed_moment_of_inertia: float,
) -> dict[str, object]:
    """Keep one target/reference channel fixed and vary only its Hamiltonian."""
    _validate_positive("radius", radius)
    _validate_positive("stretched_distance", stretched_distance)
    _validate_positive("field_energy_budget", field_energy_budget)
    _validate_positive("target_recovery_error", target_recovery_error)
    _validate_positive("energy_scale", energy_scale)
    _validate_positive("fixed_moment_of_inertia", fixed_moment_of_inertia)
    if target_recovery_error >= 1.0:
        raise ValueError("target_recovery_error must be smaller than one")

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
    recovery_bound = peter_weyl_constructive_diamond_upper_bound(
        maximum_spin,
        reference_cutoff,
    )
    inverse_gap = radius / stretched_distance
    prescribed_profiles = {
        "constant": energy_scale,
        "inverse_gap": energy_scale * inverse_gap,
        "inverse_gap_squared": energy_scale * inverse_gap * inverse_gap,
    }
    assignments = {
        name: casimir_hamiltonian_assignment(
            reference_cutoff,
            prescribed_token_excitation_energy=energy,
        )
        for name, energy in prescribed_profiles.items()
    }
    return {
        "de_sitter_radius_R": radius,
        "stretched_horizon_gap_delta": stretched_distance,
        "inverse_gap_R_over_delta": inverse_gap,
        "maximum_hard_energy_target_spin_L_delta": maximum_spin,
        "sufficient_peter_weyl_cutoff_J": reference_cutoff,
        "charged_reference_constructive_diamond_error_upper_bound": recovery_bound,
        "fixed_inertia_comparison": {
            "moment_of_inertia_I": fixed_moment_of_inertia,
            "token_excitation_energy": peter_weyl_rotor_mean_energy(
                reference_cutoff,
                moment_of_inertia=fixed_moment_of_inertia,
            ),
        },
        "prescribed_energy_hamiltonians": assignments,
        "shared_channel_data": (
            "same target spin, Peter-Weyl cutoff, canonical token, orientation "
            "POVM, and measure-and-correct decoder"
        ),
    }


def covariant_observer_energy_no_go_certificate(
    *,
    radius: float = 1.0,
    field_energy_budget: float = 4.0,
    inner_offset: float = 0.5,
    outer_offset: float = 1.5,
    target_recovery_error: float = 0.1,
    energy_scale: float = 1.0,
    fixed_moment_of_inertia: float = 1.0,
    minimum_power: int = 64,
    steps: int = 6,
) -> dict[str, object]:
    """Certify that recovery data do not identify a reference energy law."""
    _validate_positive("radius", radius)
    _validate_positive("field_energy_budget", field_energy_budget)
    _validate_positive("target_recovery_error", target_recovery_error)
    _validate_positive("energy_scale", energy_scale)
    _validate_positive("fixed_moment_of_inertia", fixed_moment_of_inertia)
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
        covariant_observer_energy_no_go_record(
            radius=radius,
            stretched_distance=radius / float(minimum_power * 4**index),
            field_energy_budget=field_energy_budget,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
            target_recovery_error=target_recovery_error,
            energy_scale=energy_scale,
            fixed_moment_of_inertia=fixed_moment_of_inertia,
        )
        for index in range(steps)
    )

    realized_profiles_match = True
    for record in records:
        for assignment in record["prescribed_energy_hamiltonians"].values():
            prescribed = assignment["prescribed_token_excitation_energy"]
            realized = assignment["realized_token_excitation_energy"]
            realized_profiles_match = realized_profiles_match and abs(
                realized - prescribed
            ) <= 1e-12 * max(1.0, prescribed)

    fixed_energies = tuple(
        record["fixed_inertia_comparison"]["token_excitation_energy"]
        for record in records
    )
    constant_energies = tuple(
        record["prescribed_energy_hamiltonians"]["constant"][
            "realized_token_excitation_energy"
        ]
        for record in records
    )
    certified_claims = {
        "same_recovery_target_met_for_every_hamiltonian_assignment": all(
            record["charged_reference_constructive_diamond_error_upper_bound"]
            <= target_recovery_error
            for record in records
        ),
        "arbitrary_prescribed_positive_token_energies_are_realized_exactly": (
            realized_profiles_match
        ),
        "constant_energy_assignment_stays_constant_across_wall_removal": (
            max(constant_energies) - min(constant_energies) <= 1e-12 * energy_scale
        ),
        "sampled_fixed_inertia_energy_grows_while_assigned_energy_stays_constant": (
            all(
                right > left
                for left, right in zip(fixed_energies, fixed_energies[1:])
            )
            and abs(constant_energies[-1] - constant_energies[0])
            <= 1e-12 * energy_scale
        ),
    }
    return {
        "goal": "Covariant Observer Hamiltonian-Identifiability No-Go",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "symmetry_and_recovery_do_not_determine_reference_energy",
        "central_result": (
            "For the same truncated SO(3) Peter-Weyl representation, canonical "
            "token, POVM, and recovery channel, every H_J=a_J C_left with a_J>0 "
            "is rotation invariant. Because <C_left>=3J(J+2)/5, choosing "
            "a_J=5 E_J/[3J(J+2)] realizes any prescribed positive ground-"
            "subtracted token-energy profile E_J without changing recovery."
        ),
        "chen_xu_scope": (
            "Chen-Xu arXiv:2511.00622v2 supplies a first-order conserved-charge "
            "action in dS2 and a kinematical higher-dimensional orthogonal frame "
            "on L2(SO(1,d)); it does not specify a rotational kinetic term, frame "
            "inertia, or positive compact-frame Hamiltonian in higher dimensions."
        ),
        "claim_boundary": (
            "This proves non-identifiability from symmetry representation and "
            "recovery data alone. It does not assert that a fixed finite-size "
            "observer action permits arbitrary Hamiltonians, nor does it derive "
            "SO(1,d) boost recovery, lifetime, local coupling, stress energy, "
            "backreaction, a Type-II trace, or generalized entropy."
        ),
        "certified_claims": certified_claims,
        "records": records,
        "required_physics_replacement": (
            "Specify a finite-size worldline/tetrad action with rotational and "
            "boost dynamics, derive its positive Hamiltonian and inertia from "
            "mass and size, couple it locally to the static-patch net, and impose "
            "a stress-energy/backreaction budget before optimizing recovery."
        ),
    }
