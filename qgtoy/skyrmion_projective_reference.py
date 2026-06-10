"""Odd Peter-Weyl orientation reference for a fermionic B=1 Skyrmion.

The Finkelstein-Rubinstein odd sector is

    direct_sum_{a=0}^J V_{a+1/2} tensor V_{a+1/2}^*.

Its state vector changes sign under the center of SU(2), but its density
operator, covariant POVM effects, and orientation kernel are center invariant.
It therefore gives a projective, center-blind SO(3) reference for an integer-
spin target while retaining the right-regular isospin multiplicities.
"""

from __future__ import annotations

from fractions import Fraction
from math import isfinite, sqrt

from .massive_skyrmion_worldtube import hard_wall_equilibrium_record
from .global_so3_reference_risk import (
    projective_hard_cutoff_orientation_risk_lower_bound,
    projective_mean_casimir_orientation_risk_lower_bound,
)
from .skyrmion_joint_scaling_no_go import (
    skyrmion_joint_scaling_no_go_certificate,
)


def _validate_nonnegative_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def odd_peter_weyl_reference_dimension(reference_cutoff: int) -> int:
    """Return ``sum_{a=0}^J (2a+2)^2``."""
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    return (
        2
        * (reference_cutoff + 1)
        * (reference_cutoff + 2)
        * (2 * reference_cutoff + 3)
        // 3
    )


def odd_peter_weyl_multiplier_fraction(
    reference_cutoff: int,
    tensor_rank: int,
) -> Fraction:
    """Return the exact multiplier on an integer tensor rank."""
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    _validate_nonnegative_integer("tensor_rank", tensor_rank)
    dimension = odd_peter_weyl_reference_dimension(reference_cutoff)
    numerator = sum(
        (2 * left_index + 2) * (2 * right_index + 2)
        for left_index in range(reference_cutoff + 1)
        for right_index in range(reference_cutoff + 1)
        if abs(left_index - right_index) <= tensor_rank
        <= left_index + right_index + 1
    )
    return Fraction(numerator, (2 * tensor_rank + 1) * dimension)


def odd_peter_weyl_closed_deficit_fraction(
    reference_cutoff: int,
    tensor_rank: int,
) -> Fraction:
    """Return the closed ``1-lambda_k`` formula on ``k<=2J+2``."""
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    _validate_nonnegative_integer("tensor_rank", tensor_rank)
    if tensor_rank > 2 * reference_cutoff + 2:
        raise ValueError("closed formula requires tensor_rank <= 2J+2")
    dimension = odd_peter_weyl_reference_dimension(reference_cutoff)
    casimir = tensor_rank * (tensor_rank + 1)
    numerator = casimir * (
        12 * (reference_cutoff + 1) * (reference_cutoff + 2)
        + 2
        - casimir
    )
    denominator = 6 * (2 * tensor_rank + 1) * dimension
    return Fraction(numerator, denominator)


def odd_peter_weyl_mean_casimir_fraction(reference_cutoff: int) -> Fraction:
    """Return the canonical token's exact mean left Casimir."""
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    return Fraction(
        3
        * (
            4 * (reference_cutoff + 1) * (reference_cutoff + 2)
            - 3
        ),
        20,
    )


def odd_peter_weyl_global_orientation_risk_record(
    reference_cutoff: int,
) -> dict[str, object]:
    """Global chordal-risk audit for the fermionic projective token."""
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    mean_casimir = odd_peter_weyl_mean_casimir_fraction(reference_cutoff)
    canonical_exact_risk = 3.0 / (2.0 * (2.0 * reference_cutoff + 3.0))
    hard_cutoff_floor = projective_hard_cutoff_orientation_risk_lower_bound(
        reference_cutoff
    )
    casimir_floor = projective_mean_casimir_orientation_risk_lower_bound(
        float(mean_casimir)
    )
    return {
        "odd_reference_cutoff_J": reference_cutoff,
        "maximum_physical_spin": reference_cutoff + 0.5,
        "mean_left_casimir_exact": str(mean_casimir),
        "canonical_token_exact_chordal_orientation_risk": canonical_exact_risk,
        "projective_hard_cutoff_risk_lower_bound": hard_cutoff_floor,
        "projective_mean_casimir_risk_lower_bound": casimir_floor,
        "bounds_respected": (
            canonical_exact_risk + 1.0e-14 >= hard_cutoff_floor
            and canonical_exact_risk + 1.0e-14 >= casimir_floor
        ),
    }


def skyrmion_joint_orientation_risk_record(
    *,
    static_patch_radius: float = 1.0,
    newton_constant: float = 1.0e-6,
    maximum_compactness: float = 0.5,
    maximum_slow_rotation: float = 0.1,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
) -> dict[str, object]:
    """Insert the fixed-profile joint-control cutoff into global risk."""
    joint = skyrmion_joint_scaling_no_go_certificate(
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
        maximum_compactness=maximum_compactness,
        maximum_slow_rotation=maximum_slow_rotation,
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
    )
    cutoff = int(joint["maximum_admissible_odd_reference_cutoff_J"])
    risk_floor = projective_hard_cutoff_orientation_risk_lower_bound(cutoff)
    return {
        "joint_scaling_status": joint["status"],
        "maximum_admissible_odd_reference_cutoff_J": cutoff,
        "maximum_admissible_physical_spin": cutoff + 0.5,
        "global_chordal_orientation_risk_lower_bound": risk_floor,
        "joint_scaling_record": joint,
        "scope": (
            "fixed certified worldtube profile, fermionic odd Peter-Weyl "
            "sector, and simultaneous compactness/slow-rotation budgets; "
            "profile-changing scalings and dynamical bath errors are excluded"
        ),
    }


def odd_peter_weyl_entanglement_fidelity_fraction(
    system_spin: int,
    reference_cutoff: int,
) -> Fraction:
    """Return the exact entanglement fidelity of measure-and-correct decoding."""
    _validate_positive_integer("system_spin", system_spin)
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    dimension = 2 * system_spin + 1
    superoperator_trace = sum(
        (2 * tensor_rank + 1)
        * odd_peter_weyl_multiplier_fraction(reference_cutoff, tensor_rank)
        for tensor_rank in range(2 * system_spin + 1)
    )
    return superoperator_trace / dimension**2


def su2_center_phase_from_twice_spin(twice_spin: int) -> int:
    """Return the exact action of ``-I`` on spin ``twice_spin/2``."""
    _validate_nonnegative_integer("twice_spin", twice_spin)
    return -1 if twice_spin % 2 else 1


def odd_peter_weyl_center_action_record(
    reference_cutoff: int,
) -> dict[str, object]:
    """Compute center action on the odd token and its projector/kernel."""
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    twice_spins = tuple(2 * index + 1 for index in range(reference_cutoff + 1))
    phases = tuple(
        su2_center_phase_from_twice_spin(twice_spin)
        for twice_spin in twice_spins
    )
    common_phase = phases[0] if all(value == phases[0] for value in phases) else 0
    return {
        "twice_spin_labels": twice_spins,
        "center_phases": phases,
        "token_center_phase": common_phase,
        "density_operator_center_invariant": common_phase * common_phase == 1,
        "povm_effect_center_invariant": common_phase * common_phase == 1,
        "orientation_kernel_center_invariant": common_phase * common_phase == 1,
        "resolves_opposite_center_parity": common_phase == 1,
    }


def odd_peter_weyl_closed_fidelity_fraction(
    system_spin: int,
    reference_cutoff: int,
) -> Fraction:
    """Return the closed fidelity formula when ``J+1>=L``."""
    _validate_positive_integer("system_spin", system_spin)
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    if reference_cutoff + 1 < system_spin:
        raise ValueError("closed fidelity formula requires J+1 >= L")
    dimension = odd_peter_weyl_reference_dimension(reference_cutoff)
    spin_casimir = system_spin * (system_spin + 1)
    deficit = Fraction(
        2
        * spin_casimir
        * (
            20 * (reference_cutoff + 1) * (reference_cutoff + 2)
            - 4 * spin_casimir
            + 3
        ),
        15 * dimension * (2 * system_spin + 1),
    )
    return Fraction(1, 1) - deficit


def odd_peter_weyl_recovery_record(
    system_spin: int,
    reference_cutoff: int,
) -> dict[str, object]:
    """Return the projective-reference channel and recovery bounds."""
    _validate_positive_integer("system_spin", system_spin)
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    target_dimension = 2 * system_spin + 1
    ranks = tuple(range(2 * system_spin + 1))
    multipliers = tuple(
        odd_peter_weyl_multiplier_fraction(reference_cutoff, rank)
        for rank in ranks
    )
    deficits = tuple(Fraction(1, 1) - value for value in multipliers)
    maximum_deficit = max(deficits)
    fidelity = odd_peter_weyl_entanglement_fidelity_fraction(
        system_spin,
        reference_cutoff,
    )
    closed_formula_available = reference_cutoff + 1 >= system_spin
    center_action = odd_peter_weyl_center_action_record(reference_cutoff)
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": target_dimension,
        "odd_reference_cutoff_J": reference_cutoff,
        "maximum_reference_spin": reference_cutoff + 0.5,
        "reference_dimension_D_minus": odd_peter_weyl_reference_dimension(
            reference_cutoff
        ),
        "reference_representation": (
            "direct_sum_{a=0}^J V_{a+1/2} tensor V_{a+1/2}^*"
        ),
        "finkelstein_rubinstein_sector": "psi(-A)=-psi(A)",
        "right_multiplicity_interpretation": "Skyrmion isospin register",
        "prepared_state": (
            "D^-1/2 sum_{a=0}^J (2a+2)|Phi_{a+1/2}>"
        ),
        "orientation_kernel": (
            "D^-1 |sum_{a=0}^J (2a+2)chi_{a+1/2}(g)|^2"
        ),
        "center_action": center_action,
        "center_blind_density_povm_and_kernel": (
            center_action["density_operator_center_invariant"]
            and center_action["povm_effect_center_invariant"]
            and center_action["orientation_kernel_center_invariant"]
        ),
        "faithful_for_opposite_center_parity_coherences": center_action[
            "resolves_opposite_center_parity"
        ],
        "tensor_ranks": ranks,
        "tensor_rank_multiplier_fractions": tuple(
            str(value) for value in multipliers
        ),
        "tensor_rank_multipliers": tuple(float(value) for value in multipliers),
        "tensor_rank_deficits": tuple(float(value) for value in deficits),
        "closed_deficit_formula_available": all(
            rank <= 2 * reference_cutoff + 2 for rank in ranks
        ),
        "closed_deficit_formula_agrees": all(
            Fraction(1, 1) - multipliers[rank]
            == odd_peter_weyl_closed_deficit_fraction(reference_cutoff, rank)
            for rank in ranks
            if rank <= 2 * reference_cutoff + 2
        ),
        "deficits_are_nondecreasing_with_rank": all(
            right >= left for left, right in zip(deficits, deficits[1:])
        ),
        "entanglement_fidelity": float(fidelity),
        "entanglement_fidelity_exact": str(fidelity),
        "closed_fidelity_formula_available": closed_formula_available,
        "closed_fidelity_formula_agrees": (
            fidelity
            == odd_peter_weyl_closed_fidelity_fraction(
                system_spin,
                reference_cutoff,
            )
            if closed_formula_available
            else None
        ),
        "normalized_diamond_error_lower_bound": float(1 - fidelity),
        "normalized_diamond_error_upper_bound": min(
            1.0,
            target_dimension * float(maximum_deficit) / 2.0,
        ),
        "mean_left_casimir": float(
            odd_peter_weyl_mean_casimir_fraction(reference_cutoff)
        ),
        "mean_left_casimir_exact": str(
            odd_peter_weyl_mean_casimir_fraction(reference_cutoff)
        ),
        "operational_gate": (
            "the right/isospin multiplicity must be coherently preparable and "
            "accessible to the decoder"
        ),
    }


def skyrmion_slow_rotation_record(
    reference_cutoff: int,
    *,
    skyrme_coupling: float,
    pion_decay_constant: float,
    mass_constant: float = 48.6317632,
    inertia_constant: float = 34.3539730,
) -> dict[str, float | int | str]:
    """Return the rigid-rotor and cross-sector phase scales."""
    _validate_nonnegative_integer("reference_cutoff", reference_cutoff)
    _validate_positive("skyrme_coupling", skyrme_coupling)
    _validate_positive("pion_decay_constant", pion_decay_constant)
    _validate_positive("mass_constant", mass_constant)
    _validate_positive("inertia_constant", inertia_constant)
    maximum_spin = reference_cutoff + 0.5
    maximum_casimir = maximum_spin * (maximum_spin + 1.0)
    slow_parameter = (
        skyrme_coupling**2 * sqrt(maximum_casimir) / inertia_constant
    )
    rotational_mass_fraction = (
        skyrme_coupling**4
        * maximum_casimir
        / (2.0 * inertia_constant * mass_constant)
    )
    sector_count = reference_cutoff + 1
    phase_span = sector_count**2 - 1
    coherence_time = (
        float("inf")
        if phase_span == 0
        else 2.0
        * inertia_constant
        / (
            skyrme_coupling**3
            * pion_decay_constant
            * phase_span
        )
    )
    return {
        "odd_reference_cutoff_J": reference_cutoff,
        "maximum_spin_K": maximum_spin,
        "maximum_spin_casimir": maximum_casimir,
        "slow_rotation_parameter_epsilon_rot": slow_parameter,
        "rotational_energy_to_mass_ratio": rotational_mass_fraction,
        "free_rotor_phase_span_coherence_time": coherence_time,
        "uniform_large_cutoff_condition": (
            "e^2 J/c_I(mu,lambda,x_w) -> 0; for a fixed dimensionless profile "
            "this reduces to e^2 J -> 0"
        ),
        "timing_condition": (
            "known free evolution can be absorbed into the POVM seed; otherwise "
            "protocol time, or after compensation timing uncertainty, must be "
            "small compared with the phase-span coherence time"
        ),
    }


def skyrmion_projective_reference_certificate(
    *,
    maximum_system_spin: int = 6,
    maximum_reference_cutoff: int = 8,
    skyrme_coupling: float = 0.1,
    pion_decay_constant: float = 1.0,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
) -> dict[str, object]:
    """Certify the odd Peter-Weyl theorem and the slow-rotation gate."""
    _validate_positive_integer("maximum_system_spin", maximum_system_spin)
    _validate_nonnegative_integer(
        "maximum_reference_cutoff",
        maximum_reference_cutoff,
    )
    records = tuple(
        odd_peter_weyl_recovery_record(system_spin, reference_cutoff)
        for reference_cutoff in range(maximum_reference_cutoff + 1)
        for system_spin in range(
            1,
            min(maximum_system_spin, reference_cutoff + 1) + 1,
        )
    )
    worldtube = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
    )
    mass_constant = worldtube["dimensionless_total_mass_c_M"]
    inertia_constant = worldtube["profile_integrals"][
        "interior_dimensionless_inertia_c_I"
    ]
    slow = skyrmion_slow_rotation_record(
        maximum_reference_cutoff,
        skyrme_coupling=skyrme_coupling,
        pion_decay_constant=pion_decay_constant,
        mass_constant=mass_constant,
        inertia_constant=inertia_constant,
    )
    certified_claims = {
        "odd_reference_dimensions_match_direct_sum": all(
            odd_peter_weyl_reference_dimension(cutoff)
            == sum((2 * index + 2) ** 2 for index in range(cutoff + 1))
            for cutoff in range(maximum_reference_cutoff + 1)
        ),
        "closed_multiplier_formula_matches_exact_counting": all(
            record["closed_deficit_formula_agrees"] for record in records
        ),
        "closed_fidelity_formula_matches_exact_counting": all(
            record["closed_fidelity_formula_agrees"] for record in records
        ),
        "all_reference_kernels_are_center_blind": all(
            record["center_action"]["token_center_phase"] == -1
            and record["center_blind_density_povm_and_kernel"]
            and not record["faithful_for_opposite_center_parity_coherences"]
            for record in records
        ),
        "all_tensor_rank_deficits_are_monotone": all(
            record["deficits_are_nondecreasing_with_rank"] for record in records
        ),
        "finite_cutoffs_have_nonzero_recovery_error": all(
            record["normalized_diamond_error_lower_bound"] > 0.0
            for record in records
        ),
        "default_slow_rotation_example_is_perturbative": (
            slow["slow_rotation_parameter_epsilon_rot"] < 0.01
            and slow["rotational_energy_to_mass_ratio"] < 1.0e-4
        ),
    }
    return {
        "goal": "Fermionic B=1 Skyrmion Projective Orientation Reference",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "odd_peter_weyl_center_blind_recovery_theorem",
        "central_result": (
            "The fermionic Finkelstein-Rubinstein B=1 rotor supplies the odd "
            "Peter-Weyl regular representation. Its state ray and POVM are "
            "center blind and give exact recovery multipliers for integer-spin "
            "targets, provided Skyrmion isospin is an accessible multiplicity "
            "register."
        ),
        "certified_claims": certified_claims,
        "records": records,
        "worldtube_profile_constants": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius_x_w": wall_radius,
            "mass_constant_c_M_total": mass_constant,
            "inertia_constant_c_I": inertia_constant,
        },
        "slow_rotation_record": slow,
        "claim_boundary": (
            "This is a kinematic rotor theorem plus a parametric slow-rotation "
            "audit. It does not construct the coherent cross-spin state, prove "
            "isospin access, include Omega^4 coefficients, radiation, wall "
            "support, bath decoherence, or gravitational backreaction."
        ),
        "next_physics_gate": (
            "construct the odd-sector token and covariant decoder from the "
            "finite-worldtube Skyrmion action, and prove a joint e^2 J -> 0, "
            "localization, lifetime, and backreaction scaling path"
        ),
    }
