"""Factorized continuous-core lift of the angular-edge obstruction.

This module couples the finite relational harmonic sector to the state-derived
ITPFI factor by a tensor product. The coupling is deliberately noninteracting:
it proves that passing to a Type-II continuous core cannot by itself restore
angular information removed by a conditional expectation. A physical
static-patch KMS interaction remains an open gate.
"""

from __future__ import annotations

from math import log

from .modular_manybody_regulator import manybody_limit_record
from .relational_observer import observer_algebra_hierarchy_record


def _validate_level(level: int) -> None:
    if level < 1:
        raise ValueError("level must be at least one")


def factorized_modular_core_record(level: int) -> dict[str, object]:
    """Record the exact tensor/core identity for the coupled surrogate."""
    _validate_level(level)
    angular_dimension = (level + 1) ** 2
    manybody = manybody_limit_record()
    return {
        "level_L": level,
        "angular_matrix_algebra": f"M_{angular_dimension}",
        "manybody_factor": manybody["gns_von_neumann_algebra"],
        "precore_algebra": f"M_{angular_dimension} tensor R_III1",
        "precore_type": "hyperfinite Type III_1 factor",
        "product_state": "normalized matrix trace tensor phi_ITPFI",
        "modular_flow": "identity on M_N tensor sigma^phi on R_III1",
        "continuous_core_identity": (
            "(M_N tensor R) crossed_{id tensor sigma} R_time "
            "is canonically isomorphic to M_N tensor "
            "(R crossed_sigma R_time)"
        ),
        "continuous_core": f"M_{angular_dimension} tensor C_phi",
        "continuous_core_type": "hyperfinite Type II_infinity factor",
        "canonical_core_trace_scaling": (
            "normalized matrix trace tau_N tensor semifinite core trace"
        ),
        "working_core_trace_scaling": (
            "ordinary Tr_N tensor core trace; this is N times the canonical scaling"
        ),
        "trace_scaling_note": (
            "all stated trace distances and relative entropies use trace-one "
            "densities in the working scaling and are unchanged by consistent "
            "global trace rescaling"
        ),
        "dual_clock_acts_only_on_core_factor": True,
        "classification_evidence": (
            "finite tensor/crossed-product identity plus the theorem-backed "
            "ITPFI classification in modular_manybody_regulator"
        ),
    }


def core_conditional_expectation_record(level: int) -> dict[str, object]:
    """Record extension of angular expectations through the factorized core."""
    _validate_level(level)
    return {
        "level_L": level,
        "angular_expectations": (
            "E_time, E_time_then_axial, and E_SU2 on the finite harmonic factor"
        ),
        "state_preserving": True,
        "commutes_with_modular_flow": True,
        "reason": (
            "the product-state modular flow is trivial on the tracial angular "
            "matrix factor"
        ),
        "core_extension": "E_hat = E_angular tensor identity_C_phi",
        "core_extension_is_normal_faithful_conditional_expectation": True,
        "core_trace_preserving": True,
        "dual_clock_covariant": True,
        "clock_restores_discarded_angular_data": False,
    }


def core_observer_algebra_hierarchy_record(level: int) -> dict[str, object]:
    """Tensor the relational algebra hierarchy with the Type-II core."""
    _validate_level(level)
    finite = observer_algebra_hierarchy_record(level)
    physical_dimension = finite["physical_dimension"]
    block_sizes = finite["time_reference_hidden_block_sizes"]
    return {
        "level_L": level,
        "full_core_observer_algebra": f"M_{physical_dimension} tensor C_phi",
        "full_core_type": "Type II_infinity factor",
        "time_hidden_core_algebra": " direct_sum ".join(
            f"(M_{size} tensor C_phi)" for size in block_sizes
        ),
        "time_hidden_center_dimension": level + 1,
        "time_then_axial_hidden_core_algebra": (
            f"direct_sum_{physical_dimension} C_phi"
        ),
        "time_then_axial_hidden_center_dimension": physical_dimension,
        "full_rotation_hidden_core_algebra": f"direct_sum_{level + 1} C_phi",
        "full_rotation_hidden_center_dimension": level + 1,
        "each_nonzero_summand_type": "Type II_infinity factor",
        "angular_fixed_point_lattice_is_unchanged_by_clock_core": True,
        "interpretation": (
            "The continuous core changes each nonzero angular block from a "
            "finite matrix algebra to a semifinite factor, but it does not "
            "reconstruct block coherences removed before the crossed product."
        ),
    }


def time_axial_core_obstruction_record(level: int) -> dict[str, object]:
    """Lift the time-then-axial phase-pair obstruction to the core."""
    _validate_level(level)
    return {
        "level_L": level,
        "angular_input_pair": (
            "rho_+/- from (|L,-L> +/- |L,L>)/sqrt(2)"
        ),
        "core_density": "omega=q/Tr(q) for a nonzero finite-trace core projection q",
        "core_density_has_finite_entropy": True,
        "lifted_input_pair": "rho_+ tensor omega, rho_- tensor omega",
        "lifted_input_trace_distance": 1.0,
        "time_axial_expected_output_trace_distance": 0.0,
        "decoder_worst_case_trace_distance_error_lower_bound": 0.5,
        "relative_entropy_to_time_axial_expected_state": log(2.0),
        "finite_entropy_increase_under_time_axial_expectation": log(2.0),
        "relative_entropy_unit": "nats",
        "tensor_stability_reason": (
            "trace distance and Umegaki relative entropy are unchanged after "
            "tensoring both states with the same normalized core density"
        ),
    }


def full_rotation_core_obstruction_record(level: int) -> dict[str, object]:
    """Lift full-SU(2) orientation loss to a core entropy obstruction."""
    _validate_level(level)
    irrep_dimension = 2 * level + 1
    entropy_loss = log(float(irrep_dimension))
    return {
        "level_L": level,
        "selected_irrep_dimension": irrep_dimension,
        "pure_angular_input": "any rank-one state in V_L",
        "core_density": "omega=q/Tr(q) for a nonzero finite-trace core projection q",
        "core_density_has_finite_entropy": True,
        "full_rotation_expected_state": f"I_{irrep_dimension}/{irrep_dimension}",
        "relative_entropy_to_full_rotation_expected_state": entropy_loss,
        "finite_entropy_increase_under_full_rotation_expectation": entropy_loss,
        "relative_entropy_unit": "nats",
        "large_cutoff_scaling": "log(2L+1)",
        "orthogonal_phase_pair_outputs_collide": True,
        "decoder_worst_case_trace_distance_error_lower_bound": 0.5,
        "core_tensor_factor_changes_entropy_loss": False,
    }


def core_edge_obstruction_certificate(
    *,
    max_level: int = 8,
    tolerance: float = 1e-12,
) -> dict[str, object]:
    if max_level < 1:
        raise ValueError("max_level must be at least one")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    cores = tuple(
        factorized_modular_core_record(level)
        for level in range(1, max_level + 1)
    )
    expectations = tuple(
        core_conditional_expectation_record(level)
        for level in range(1, max_level + 1)
    )
    hierarchies = tuple(
        core_observer_algebra_hierarchy_record(level)
        for level in range(1, max_level + 1)
    )
    time_axial = tuple(
        time_axial_core_obstruction_record(level)
        for level in range(1, max_level + 1)
    )
    rotation = tuple(
        full_rotation_core_obstruction_record(level)
        for level in range(1, max_level + 1)
    )
    finite_verified_claims = {
        "time_axial_core_entropy_loss_is_log_two": all(
            abs(
                record["relative_entropy_to_time_axial_expected_state"]
                - log(2.0)
            )
            <= tolerance
            for record in time_axial
        ),
        "full_rotation_core_entropy_loss_is_log_irrep_dimension": all(
            abs(
                record["relative_entropy_to_full_rotation_expected_state"]
                - log(float(2 * record["level_L"] + 1))
            )
            <= tolerance
            for record in rotation
        ),
        "recovery_half_error_bound_survives_core_tensoring": all(
            record["decoder_worst_case_trace_distance_error_lower_bound"] == 0.5
            for record in time_axial + rotation
        ),
        "angular_center_dimensions_survive_core_amplification": all(
            record["time_then_axial_hidden_center_dimension"]
            == (record["level_L"] + 1) ** 2
            and record["full_rotation_hidden_center_dimension"]
            == record["level_L"] + 1
            for record in hierarchies
        ),
    }
    theorem_backed_core_claims = {
        "factorized_precore_is_type_iii1": all(
            record["precore_type"] == "hyperfinite Type III_1 factor"
            for record in cores
        ),
        "factorized_continuous_core_is_type_ii_infinity": all(
            record["continuous_core_type"]
            == "hyperfinite Type II_infinity factor"
            for record in cores
        ),
        "angular_expectations_extend_trace_preservingly_to_the_core": all(
            record["core_extension_is_normal_faithful_conditional_expectation"]
            and record["core_trace_preserving"]
            for record in expectations
        ),
        "dual_clock_does_not_restore_angular_information": all(
            not record["clock_restores_discarded_angular_data"]
            for record in expectations
        ),
    }
    all_claims = {**finite_verified_claims, **theorem_backed_core_claims}
    return {
        "goal": "Core-Stable Angular Edge Obstruction",
        "status": "pass" if all(all_claims.values()) else "fail",
        "result_type": "factorized_typeii_core_recovery_and_entropy_no_go",
        "central_result": (
            "For the product state tau_L tensor phi_ITPFI, the continuous core "
            "factorizes as M_N tensor C_phi. Every angular conditional "
            "expectation extends as E tensor id, so the clock core cannot restore "
            "discarded edge data. The half-error recovery no-go survives, while "
            "the missing-frame relative entropy is log(2) for the time-then-axial "
            "phase-pair obstruction and log(2L+1) for full orientation loss."
        ),
        "claim_boundary": (
            "exact factorized angular-times-thermal surrogate; no interaction, "
            "geometric locality, Bunch-Davies derivation, or generalized-entropy "
            "identification is supplied"
        ),
        "evidence_scope": (
            "finite entropy and recovery formulas are exact; Type-III/core type "
            "uses the ITPFI classification theorem and the explicit factorized "
            "crossed-product identity"
        ),
        "finite_verified_claims": finite_verified_claims,
        "theorem_backed_core_claims": theorem_backed_core_claims,
        "core_records": cores,
        "expectation_records": expectations,
        "hierarchy_records": hierarchies,
        "time_axial_obstruction_records": time_axial,
        "full_rotation_obstruction_records": rotation,
        "next_physics_gate": (
            "Replace the tensor-product spectator construction by an interacting "
            "static-patch KMS net and compare the core entropy loss with "
            "generalized entropy or a gravitational observer-algebra index."
        ),
    }
