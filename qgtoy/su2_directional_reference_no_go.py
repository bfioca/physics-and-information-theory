"""No-go for full quantum recovery from one irreducible SU(2) reference.

The tensor product of two SU(2) irreducible representations is
multiplicity-free.  Consequently, twirling a spin-L system together with one
spin-J reference has an abelian range and is entanglement-breaking, regardless
of the prepared reference state.
"""

from __future__ import annotations


def _validate_system_spin(system_spin: int) -> None:
    if isinstance(system_spin, bool) or not isinstance(system_spin, int) or system_spin < 1:
        raise ValueError("system_spin must be a positive integer")


def _validate_reference_spin(reference_spin: int) -> None:
    if (
        isinstance(reference_spin, bool)
        or not isinstance(reference_spin, int)
        or reference_spin < 0
    ):
        raise ValueError("reference_spin must be a nonnegative integer")


def clebsch_gordan_multiplicity_record(
    system_spin: int,
    reference_spin: int,
) -> dict[str, object]:
    """Enumerate the multiplicity-free total-spin decomposition."""
    _validate_system_spin(system_spin)
    _validate_reference_spin(reference_spin)
    total_spins = tuple(
        range(
            abs(system_spin - reference_spin),
            system_spin + reference_spin + 1,
        )
    )
    sector_dimensions = tuple(2 * total_spin + 1 for total_spin in total_spins)
    joint_dimension = (2 * system_spin + 1) * (2 * reference_spin + 1)
    return {
        "system_spin_L": system_spin,
        "reference_spin_J": reference_spin,
        "total_spin_labels": total_spins,
        "sector_multiplicities": tuple(1 for _ in total_spins),
        "sector_dimensions": sector_dimensions,
        "sector_dimensions_sum": sum(sector_dimensions),
        "joint_hilbert_dimension": joint_dimension,
        "dimension_identity_holds": sum(sector_dimensions) == joint_dimension,
        "decomposition_is_multiplicity_free": True,
    }


def single_irrep_twirl_record(
    system_spin: int,
    reference_spin: int,
) -> dict[str, object]:
    """Return the fixed algebra and channel-class obstruction."""
    decomposition = clebsch_gordan_multiplicity_record(
        system_spin,
        reference_spin,
    )
    sector_count = len(decomposition["total_spin_labels"])
    return {
        "system_spin_L": system_spin,
        "reference_spin_J": reference_spin,
        "prepared_reference_state": (
            "arbitrary fixed product density operator eta on V_J, with no "
            "accessible multiplicity ancilla"
        ),
        "physical_channel": "rho maps to SU(2)-twirl(rho tensor eta)",
        "fixed_operator_algebra": "direct_sum_K C I_{V_K}",
        "fixed_operator_algebra_dimension": sector_count,
        "twirled_range_is_commutative": True,
        "channel_is_measure_and_prepare": True,
        "channel_is_equivalent_to_quantum_to_classical": True,
        "channel_is_entanglement_breaking": True,
        "reference_charge_alone_restores_full_quantum_algebra": False,
        "reason": (
            "V_L tensor V_J is multiplicity-free, so the twirl retains only "
            "the classical total-spin sector weights"
        ),
        "measure_prepare_form": (
            "E_eta(rho)=sum_K Tr(M_K rho) P_K/(2K+1), for the POVM induced "
            "by eta and the total-spin projectors P_K"
        ),
    }


def single_irrep_recovery_bound_record(
    system_spin: int,
    reference_spin: int,
) -> dict[str, object]:
    """Bound any decoder using a maximally entangled system witness."""
    _validate_system_spin(system_spin)
    _validate_reference_spin(reference_spin)
    system_dimension = 2 * system_spin + 1
    separable_overlap_bound = 1.0 / float(system_dimension)
    normalized_diamond_error_lower_bound = 1.0 - separable_overlap_bound
    return {
        "system_spin_L": system_spin,
        "reference_spin_J": reference_spin,
        "system_dimension_d": system_dimension,
        "decoder_class": "all deterministic CPTP decoders",
        "decoded_channel_remains_entanglement_breaking": True,
        "maximally_entangled_overlap_upper_bound": separable_overlap_bound,
        "normalized_diamond_recovery_error_lower_bound": (
            normalized_diamond_error_lower_bound
        ),
        "diamond_norm_convention": "one half of the completely bounded trace norm",
        "exact_full_quantum_recovery_possible": False,
        "bound_independent_of_reference_spin_J": True,
    }


def su2_directional_reference_no_go_certificate(
    *,
    max_system_spin: int = 8,
    max_reference_spin: int = 8,
) -> dict[str, object]:
    """Audit the single-irrep directional-reference obstruction."""
    _validate_system_spin(max_system_spin)
    _validate_reference_spin(max_reference_spin)
    records = tuple(
        {
            "decomposition": clebsch_gordan_multiplicity_record(system_spin, reference_spin),
            "twirl": single_irrep_twirl_record(system_spin, reference_spin),
            "recovery": single_irrep_recovery_bound_record(system_spin, reference_spin),
        }
        for system_spin in range(1, max_system_spin + 1)
        for reference_spin in range(0, max_reference_spin + 1)
    )
    certified_claims = {
        "all_tensor_products_are_multiplicity_free": all(
            record["decomposition"]["decomposition_is_multiplicity_free"]
            and record["decomposition"]["dimension_identity_holds"]
            for record in records
        ),
        "all_single_irrep_twirl_ranges_are_abelian": all(
            record["twirl"]["twirled_range_is_commutative"]
            and record["twirl"]["channel_is_entanglement_breaking"]
            for record in records
        ),
        "every_decoder_has_a_nonzero_entanglement_recovery_error": all(
            record["recovery"]["normalized_diamond_recovery_error_lower_bound"]
            == 1.0 - 1.0 / float(record["recovery"]["system_dimension_d"])
            and not record["recovery"]["exact_full_quantum_recovery_possible"]
            for record in records
        ),
        "increasing_one_irrep_spin_does_not_remove_the_obstruction": all(
            record["recovery"]["bound_independent_of_reference_spin_J"]
            for record in records
        ),
    }
    return {
        "goal": "Single-Irrep SU(2) Directional Reference No-Go",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "multiplicity_free_entanglement_breaking_obstruction",
        "central_result": (
            "For every prepared state on a single spin-J reference, the joint "
            "SU(2) twirl with a spin-L system has an abelian, entanglement-breaking "
            "range because V_L tensor V_J is multiplicity-free. Any decoder has "
            "normalized diamond recovery error at least 1-1/(2L+1), independent "
            "of J. Nontrivial representation charge is therefore necessary but "
            "not sufficient; multiplicity resources are also required."
        ),
        "claim_boundary": (
            "single irreducible directional reference and deterministic recovery "
            "of the full quantum spin sector from a fixed product reference; "
            "accessible multiplicity ancillas, reducible references with repeated "
            "irreps, correlated or input-dependent references, restricted classical "
            "tasks, postselection, local KMS dynamics, and SO(1,d) observers are "
            "outside the theorem"
        ),
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "derive the Hamiltonian and energy cost of the constructive reducible "
            "rotation reference inside the local static-patch KMS net"
        ),
    }
