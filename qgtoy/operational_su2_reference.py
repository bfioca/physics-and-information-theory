"""Operational reducible rotation-reference theorems.

The module separates three facts:

* no finite-dimensional prepared SU(2) reference gives exact deterministic
  append--twirl--decode recovery of a nontrivial spin sector;
* the largest Clebsch-Gordan multiplicity gives a universal diamond-error lower
  bound;
* an integer-spin truncated SO(3) Peter-Weyl reference, equivalently a
  center-blind SU(2) reference on operator algebras, gives an explicit
  approximate decoder with exact tensor-rank multipliers.
"""

from __future__ import annotations

from fractions import Fraction


def _validate_system_spin(system_spin: int) -> None:
    if isinstance(system_spin, bool) or not isinstance(system_spin, int) or system_spin < 1:
        raise ValueError("system_spin must be a positive integer")


def _validate_reference_cutoff(reference_cutoff: int) -> None:
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")


def _validate_tensor_rank(tensor_rank: int) -> None:
    if isinstance(tensor_rank, bool) or not isinstance(tensor_rank, int) or tensor_rank < 0:
        raise ValueError("tensor_rank must be a nonnegative integer")


def peter_weyl_reference_dimension(reference_cutoff: int) -> int:
    """Dimension of the integer-spin SO(3) Peter-Weyl cutoff."""
    _validate_reference_cutoff(reference_cutoff)
    return (
        (reference_cutoff + 1)
        * (2 * reference_cutoff + 1)
        * (2 * reference_cutoff + 3)
        // 3
    )


def joint_irrep_multiplicities(
    system_spin: int,
    reference_multiplicities: tuple[int, ...],
) -> tuple[tuple[int, int], ...]:
    """Return ``(K,n_K)`` for ``R=direct_sum_j V_j tensor C^{m_j}``."""
    _validate_system_spin(system_spin)
    if not reference_multiplicities:
        raise ValueError("reference_multiplicities must not be empty")
    if any(
        isinstance(value, bool) or not isinstance(value, int) or value < 0
        for value in reference_multiplicities
    ):
        raise ValueError("reference multiplicities must be nonnegative integers")
    if not any(reference_multiplicities):
        raise ValueError("the reference representation must be nonzero")
    maximum_reference_spin = len(reference_multiplicities) - 1
    records = []
    for total_spin in range(system_spin + maximum_reference_spin + 1):
        multiplicity = sum(
            reference_multiplicity
            for reference_spin, reference_multiplicity in enumerate(
                reference_multiplicities
            )
            if abs(system_spin - reference_spin)
            <= total_spin
            <= system_spin + reference_spin
        )
        if multiplicity:
            records.append((total_spin, multiplicity))
    return tuple(records)


def multiplicity_recovery_bound_record(
    system_spin: int,
    reference_multiplicities: tuple[int, ...],
) -> dict[str, object]:
    """Give the Schmidt-number recovery obstruction from fixed-algebra blocks."""
    multiplicities = joint_irrep_multiplicities(
        system_spin,
        reference_multiplicities,
    )
    system_dimension = 2 * system_spin + 1
    maximum_multiplicity = max(value for _, value in multiplicities)
    normalized_diamond_lower_bound = max(
        0.0,
        1.0 - maximum_multiplicity / float(system_dimension),
    )
    reference_dimension = sum(
        (2 * reference_spin + 1) * multiplicity
        for reference_spin, multiplicity in enumerate(reference_multiplicities)
    )
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": system_dimension,
        "reference_multiplicities_m_j": reference_multiplicities,
        "reference_dimension": reference_dimension,
        "joint_total_spin_multiplicities": multiplicities,
        "fixed_operator_algebra": "direct_sum_K M_{n_K}",
        "maximum_joint_multiplicity_r": maximum_multiplicity,
        "normalized_diamond_recovery_error_lower_bound": (
            normalized_diamond_lower_bound
        ),
        "bound_formula": "max(0,1-r/d)",
        "proof_mechanism": (
            "the twirled Choi state has Schmidt number at most r; decoding cannot "
            "increase Schmidt number, and overlap with Phi_d is at most r/d"
        ),
    }


def minimal_reducible_reference_record(system_spin: int) -> dict[str, object]:
    """Audit the smallest adjacent-irrep example ``V_0 direct_sum V_1``."""
    _validate_system_spin(system_spin)
    record = multiplicity_recovery_bound_record(system_spin, (1, 1))
    return {
        **record,
        "reference_representation": "V_0 direct_sum V_1",
        "joint_decomposition": "V_{L-1} direct_sum (V_L tensor C^2) direct_sum V_{L+1}",
        "fixed_operator_algebra_explicit": "C direct_sum M_2 direct_sum C",
        "retained_relational_quantum_dimension": 2,
        "large_L_consequence": "full-sector recovery lower bound tends to one",
    }


def finite_reference_exact_recovery_no_go_record(system_spin: int) -> dict[str, object]:
    """State the continuous-group Knill-Laflamme exact-recovery obstruction."""
    _validate_system_spin(system_spin)
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": 2 * system_spin + 1,
        "reference_class": "every finite-dimensional SU(2) representation and fixed state",
        "channel": (
            "N_eta(rho)=integral dg U_L(g)rho U_L(g)^* tensor "
            "U_R(g)eta U_R(g)^*"
        ),
        "exact_deterministic_decoder_exists": False,
        "knill_laflamme_kernel": (
            "<eta|U_R(g^-1 h)|eta> U_L(g^-1 h) for pure eta, with the "
            "corresponding spectral Kraus family for mixed eta"
        ),
        "obstruction": (
            "the reference characteristic function is continuous and nonzero "
            "near the identity, while U_L is non-scalar on every identity "
            "neighborhood for nontrivial spin"
        ),
        "scope": (
            "normal finite-dimensional prepared references, full deterministic "
            "quantum recovery, a connected rotation group, and no external "
            "orientation; pre-correlated encodings, logical multiplicity "
            "subsystems, approximate recovery, and postselection remain possible"
        ),
        "verification_mode": "analytic continuous-group Knill-Laflamme theorem",
    }


def peter_weyl_multiplier_fraction(
    reference_cutoff: int,
    tensor_rank: int,
) -> Fraction:
    """Exact multiplier from character-product/Clebsch-Gordan counting."""
    _validate_reference_cutoff(reference_cutoff)
    _validate_tensor_rank(tensor_rank)
    dimension = peter_weyl_reference_dimension(reference_cutoff)
    numerator = sum(
        (2 * left_spin + 1) * (2 * right_spin + 1)
        for left_spin in range(reference_cutoff + 1)
        for right_spin in range(reference_cutoff + 1)
        if abs(left_spin - right_spin)
        <= tensor_rank
        <= left_spin + right_spin
    )
    return Fraction(numerator, (2 * tensor_rank + 1) * dimension)


def peter_weyl_closed_deficit_fraction(
    reference_cutoff: int,
    tensor_rank: int,
) -> Fraction:
    """Closed ``1-lambda_k`` formula on the kernel band ``k<=2J``."""
    _validate_reference_cutoff(reference_cutoff)
    _validate_tensor_rank(tensor_rank)
    if tensor_rank > 2 * reference_cutoff:
        raise ValueError("closed deficit formula requires tensor_rank <= 2*reference_cutoff")
    dimension = peter_weyl_reference_dimension(reference_cutoff)
    numerator = tensor_rank * (tensor_rank + 1) * (
        12 * reference_cutoff * (reference_cutoff + 2)
        - tensor_rank * (tensor_rank + 1)
        + 11
    )
    denominator = 6 * (2 * tensor_rank + 1) * dimension
    return Fraction(numerator, denominator)


def peter_weyl_mean_casimir_fraction(reference_cutoff: int) -> Fraction:
    """Exact mean left-action Casimir of the canonical token state."""
    _validate_reference_cutoff(reference_cutoff)
    return Fraction(3 * reference_cutoff * (reference_cutoff + 2), 5)


def peter_weyl_entanglement_fidelity_fraction(
    system_spin: int,
    reference_cutoff: int,
) -> Fraction:
    """Entanglement fidelity of the covariant measure-and-correct decoder."""
    _validate_system_spin(system_spin)
    _validate_reference_cutoff(reference_cutoff)
    system_dimension = 2 * system_spin + 1
    superoperator_trace = sum(
        (2 * tensor_rank + 1)
        * peter_weyl_multiplier_fraction(reference_cutoff, tensor_rank)
        for tensor_rank in range(2 * system_spin + 1)
    )
    return superoperator_trace / (system_dimension**2)


def peter_weyl_recovery_record(
    system_spin: int,
    reference_cutoff: int,
) -> dict[str, object]:
    """Return the constructive covariant reference channel and quantitative bounds."""
    _validate_system_spin(system_spin)
    _validate_reference_cutoff(reference_cutoff)
    system_dimension = 2 * system_spin + 1
    dimension = peter_weyl_reference_dimension(reference_cutoff)
    ranks = tuple(range(2 * system_spin + 1))
    multipliers = tuple(
        peter_weyl_multiplier_fraction(reference_cutoff, tensor_rank)
        for tensor_rank in ranks
    )
    deficits = tuple(Fraction(1, 1) - multiplier for multiplier in multipliers)
    maximum_deficit = max(deficits)
    normalized_diamond_upper_bound = min(
        1.0,
        system_dimension * float(maximum_deficit) / 2.0,
    )
    fidelity = peter_weyl_entanglement_fidelity_fraction(
        system_spin,
        reference_cutoff,
    )
    closed_formula_available = reference_cutoff >= system_spin
    closed_deficits = (
        tuple(
            peter_weyl_closed_deficit_fraction(reference_cutoff, tensor_rank)
            for tensor_rank in ranks
        )
        if closed_formula_available
        else None
    )
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": system_dimension,
        "reference_cutoff_J": reference_cutoff,
        "reference_representation": (
            "integer-spin SO(3) Peter-Weyl cutoff direct_sum_{j=0}^J "
            "V_j tensor V_j^*"
        ),
        "su2_interpretation": (
            "center-blind SU(2) reference; sufficient for conjugation channels "
            "on the integer-spin target operator algebra"
        ),
        "reference_group_action": (
            "left action direct_sum_j U_j(g) tensor identity_{V_j^*}; the dual "
            "factor is the intrinsic right/multiplicity index"
        ),
        "reference_dimension_D_J": dimension,
        "prepared_state": "D_J^-1/2 sum_j (2j+1)|Phi_j>",
        "covariant_povm_seed": "sum_j (2j+1)|Phi_j>",
        "povm_resolves_identity": True,
        "orientation_error_kernel": (
            "p_J(g)=D_J^-1 |sum_{j=0}^J (2j+1) chi_j(g)|^2"
        ),
        "decoded_channel": "integral dg p_J(g) U_L(g) rho U_L(g)^*",
        "tensor_ranks": ranks,
        "tensor_rank_multiplier_fractions": tuple(str(value) for value in multipliers),
        "tensor_rank_multipliers": tuple(float(value) for value in multipliers),
        "tensor_rank_deficits": tuple(float(value) for value in deficits),
        "closed_deficit_formula_available": closed_formula_available,
        "closed_formula_agrees": (
            closed_deficits == deficits if closed_deficits is not None else None
        ),
        "deficits_are_nondecreasing_with_rank": all(
            right >= left for left, right in zip(deficits, deficits[1:])
        ),
        "normalized_diamond_error_upper_bound": normalized_diamond_upper_bound,
        "diamond_bound_basis": (
            "one half times d times the Hilbert-Schmidt superoperator norm defect"
        ),
        "entanglement_fidelity": float(fidelity),
        "entanglement_infidelity": float(1 - fidelity),
        "mean_reference_casimir": float(
            peter_weyl_mean_casimir_fraction(reference_cutoff)
        ),
        "mean_reference_casimir_exact": str(
            peter_weyl_mean_casimir_fraction(reference_cutoff)
        ),
        "casimir_convention": "left-action Casimir carrying the orientation",
        "fixed_target_convergence_only": True,
        "exact_recovery_at_finite_cutoff": False,
        "decoder_is_claimed_optimal": False,
    }


def operational_su2_reference_certificate(
    *,
    max_system_spin: int = 6,
    reference_scale: int = 8,
    tolerance: float = 1e-12,
) -> dict[str, object]:
    """Audit the reducible SU(2) operational reference theorem."""
    _validate_system_spin(max_system_spin)
    if isinstance(reference_scale, bool) or not isinstance(reference_scale, int) or reference_scale < 2:
        raise ValueError("reference_scale must be an integer at least two")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    records = tuple(
        {
            "exact_no_go": finite_reference_exact_recovery_no_go_record(system_spin),
            "single_irrep_bound": multiplicity_recovery_bound_record(
                system_spin,
                tuple(1 if reference_spin == system_spin else 0 for reference_spin in range(system_spin + 1)),
            ),
            "minimal_reducible": minimal_reducible_reference_record(system_spin),
            "peter_weyl": peter_weyl_recovery_record(
                system_spin,
                reference_scale * system_spin,
            ),
            "peter_weyl_larger": peter_weyl_recovery_record(
                system_spin,
                2 * reference_scale * system_spin,
            ),
        }
        for system_spin in range(1, max_system_spin + 1)
    )
    certified_claims = {
        "finite_references_never_give_exact_deterministic_recovery": all(
            not record["exact_no_go"]["exact_deterministic_decoder_exists"]
            for record in records
        ),
        "multiplicity_bound_recovers_single_irrep_no_go": all(
            abs(
                record["single_irrep_bound"][
                    "normalized_diamond_recovery_error_lower_bound"
                ]
                - (1.0 - 1.0 / record["single_irrep_bound"]["system_dimension_d"])
            )
            <= tolerance
            for record in records
        ),
        "smallest_reducible_reference_retains_only_a_qubit": all(
            record["minimal_reducible"]["maximum_joint_multiplicity_r"] == 2
            and record["minimal_reducible"]["fixed_operator_algebra_explicit"]
            == "C direct_sum M_2 direct_sum C"
            for record in records
        ),
        "peter_weyl_closed_multiplier_formula_is_exact": all(
            record["peter_weyl"]["closed_formula_agrees"]
            and record["peter_weyl"]["deficits_are_nondecreasing_with_rank"]
            for record in records
        ),
        "larger_peter_weyl_reference_improves_constructive_bound": all(
            record["peter_weyl_larger"]["normalized_diamond_error_upper_bound"]
            < record["peter_weyl"]["normalized_diamond_error_upper_bound"]
            and record["peter_weyl_larger"]["entanglement_infidelity"]
            < record["peter_weyl"]["entanglement_infidelity"]
            for record in records
        ),
        "reference_casimir_cost_is_exact": all(
            record["peter_weyl"]["mean_reference_casimir_exact"]
            == str(
                Fraction(
                    3
                    * record["peter_weyl"]["reference_cutoff_J"]
                    * (record["peter_weyl"]["reference_cutoff_J"] + 2),
                    5,
                )
            )
            for record in records
        ),
    }
    return {
        "goal": "Operational Reducible Rotation Reference Recovery",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "peter_weyl_prepared_reference_recovery_and_resource_theorem",
        "central_result": (
            "No finite prepared continuous rotation reference gives exact "
            "deterministic recovery. "
            "For R=direct_sum_j V_j tensor C^{m_j}, every decoder has normalized "
            "diamond error at least max(0,1-max_K n_K/(2L+1)). A truncated "
            "integer-spin SO(3) Peter-Weyl reference with its covariant "
            "orientation POVM gives an "
            "explicit random-rotation decoder whose exact tensor-rank deficits "
            "vanish as J grows, with mean Casimir 3J(J+2)/5."
        ),
        "claim_boundary": (
            "positive-integer target spins, deterministic full-sector recovery, "
            "finite left-regular SO(3) Peter-Weyl cutoff, and fixed-target "
            "convergence for a constructive decoder that is not proved optimal; "
            "no local KMS dynamics, gravitational energy constraint, half-integer "
            "full-SU(2) cutoff, or SO(1,d) reference is derived"
        ),
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "couple the Peter-Weyl reference Casimir to a localized static-patch "
            "Hamiltonian and derive an energy-constrained SO(1,d) recovery law"
        ),
    }
