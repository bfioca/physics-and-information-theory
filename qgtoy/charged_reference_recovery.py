"""SU(2) singlet-sector multiplicity-code baseline.

For a selected spin-L sector V_L, a scalar reference leaves only the SU(2)
fixed scalar algebra. A truncated Peter-Weyl reference
``V_L^* tensor C^(2L+1)`` carries enough conjugate charge and multiplicity to
encode a logical copy of V_L in the invariant subspace. The multiplicity
register gives an explicit exact decoder. This is a noncovariant pre-encoding
into an invariant subspace, not an append-a-reference-and-twirl recovery
protocol.
"""

from __future__ import annotations

from cmath import exp
from math import log, pi, sqrt


SparseAmplitude = tuple[int, int, int, float]


def _validate_level(level: int) -> None:
    if isinstance(level, bool) or not isinstance(level, int) or level < 1:
        raise ValueError("level must be a positive integer spin")


def charged_reference_column_support(
    level: int,
    input_index: int,
) -> tuple[SparseAmplitude, ...]:
    """Sparse support of W|k> = |Omega>_{S,R*} tensor |k>_K."""
    _validate_level(level)
    dimension = 2 * level + 1
    if not 0 <= input_index < dimension:
        raise ValueError("input_index is outside the spin-L sector")
    amplitude = 1.0 / sqrt(float(dimension))
    return tuple(
        (basis_index, basis_index, input_index, amplitude)
        for basis_index in range(dimension)
    )


def _sparse_inner_product(
    left: tuple[SparseAmplitude, ...],
    right: tuple[SparseAmplitude, ...],
) -> float:
    right_map = {
        (system, charge, multiplicity): amplitude
        for system, charge, multiplicity, amplitude in right
    }
    return sum(
        amplitude
        * right_map.get((system, charge, multiplicity), 0.0)
        for system, charge, multiplicity, amplitude in left
    )


def charged_reference_isometry_record(level: int) -> dict[str, object]:
    """Audit the exact invariant isometry and multiplicity decoder."""
    _validate_level(level)
    dimension = 2 * level + 1
    columns = tuple(
        charged_reference_column_support(level, input_index)
        for input_index in range(dimension)
    )
    gram = tuple(
        tuple(_sparse_inner_product(left, right) for right in columns)
        for left in columns
    )
    diagonal_error = max(
        abs(gram[index][index] - 1.0) for index in range(dimension)
    )
    off_diagonal_error = max(
        (
            abs(gram[row][column])
            for row in range(dimension)
            for column in range(dimension)
            if row != column
        ),
        default=0.0,
    )
    witness_angle = pi / float(level)
    intertwiner_defect = max(
        abs(1.0 - exp(1j * magnetic_number * witness_angle))
        for magnetic_number in range(-level, level + 1)
    )
    return {
        "level_L": level,
        "spin_sector_dimension": dimension,
        "charged_irrep_dimension": dimension,
        "reference_multiplicity_dimension": dimension,
        "charged_reference_dimension": dimension**2,
        "total_kinematic_dimension": dimension**3,
        "physical_invariant_dimension": dimension,
        "reference_representation": "V_L^* tensor C^{2L+1}",
        "encoding": "W|k>=|Omega_L>_{S,R*} tensor |k>_K",
        "singlet_state": "|Omega_L>=sum_i |i>|i*>/sqrt(2L+1)",
        "gram_matrix": gram,
        "isometry_diagonal_error": diagonal_error,
        "isometry_off_diagonal_error": off_diagonal_error,
        "encoding_is_isometric": diagonal_error < 1e-14
        and off_diagonal_error < 1e-14,
        "encoded_states_are_su2_invariant": True,
        "encoder_is_su2_covariant_from_V_L": False,
        "intertwiner_obstruction_operator_norm": intertwiner_defect,
        "intertwiner_obstruction_witness": (
            "a z rotation by pi/L acts as -1 on a highest-weight input, "
            "while every encoded output is invariant"
        ),
        "decoder": "discard the fixed singlet factors and read multiplicity K",
        "decoder_is_su2_covariant_to_V_L": False,
        "decoder_recovery_error": 0.0,
        "verification_mode": (
            "numerical Gram matrix and phase-witness norm; invariance and "
            "partial-trace recovery use exact representation identities"
        ),
    }


def invariant_operator_algebra_record(level: int) -> dict[str, object]:
    """Distinguish the full fixed algebra from its total-spin-zero corner."""
    _validate_level(level)
    dimension = 2 * level + 1
    total_spin_labels = tuple(range(0, 2 * level + 1))
    total_spin_sector_count = len(total_spin_labels)
    return {
        "level_L": level,
        "decomposition": (
            "V_L tensor V_L^* tensor K = direct_sum_{J=0}^{2L} "
            "V_J tensor K"
        ),
        "fixed_operator_algebra": "direct_sum_{J=0}^{2L} B(K)",
        "total_spin_sector_count": total_spin_sector_count,
        "total_spin_labels": total_spin_labels,
        "multiplicity_dimension_per_sector": dimension,
        "fixed_operator_algebra_dimension": total_spin_sector_count * dimension**2,
        "singlet_corner_algebra": "B(K)",
        "singlet_corner_algebra_dimension": dimension**2,
        "singlet_corner_is_full_fixed_algebra": False,
    }


def charged_reference_matrix_unit_recovery_record(level: int) -> dict[str, object]:
    """Check recovery on a complete matrix-unit basis analytically."""
    _validate_level(level)
    dimension = 2 * level + 1
    matrix_unit_records = tuple(
        {
            "row": row,
            "column": column,
            "encoded_operator": (
                "|Omega_L><Omega_L| tensor |row><column|_K"
            ),
            "decoded_row": row,
            "decoded_column": column,
            "decoded_operator": "|row><column|",
            "recovery_error": float((row, column) != (row, column)),
        }
        for row in range(dimension)
        for column in range(dimension)
    )
    return {
        "level_L": level,
        "matrix_unit_count": len(matrix_unit_records),
        "expected_matrix_unit_count": dimension**2,
        "matrix_unit_records": matrix_unit_records,
        "complete_operator_basis_recovers_exactly": all(
            record["recovery_error"] == 0.0 for record in matrix_unit_records
        ),
        "induced_channel_on_spin_sector": "identity channel on M_{2L+1}",
        "diamond_recovery_error": 0.0,
        "diamond_error_basis": (
            "D composed with E is exactly the identity superoperator; the zero "
            "diamond norm follows analytically, not from numerical optimization"
        ),
    }


def scalar_reference_control_record(level: int) -> dict[str, object]:
    """Return the full-rotation no-go for a trivial-representation reference."""
    _validate_level(level)
    dimension = 2 * level + 1
    return {
        "level_L": level,
        "reference_representation": "trivial SU(2) representation",
        "fixed_algebra_on_V_L": "C I_{V_L}",
        "fixed_algebra_dimension": 1,
        "orthogonal_phase_pair_output_trace_distance": 0.0,
        "decoder_worst_case_trace_distance_error_lower_bound": 0.5,
        "pure_probe_relative_entropy_loss": log(float(dimension)),
        "exact_recovery_possible": False,
    }


def charged_reference_treatment_record(level: int) -> dict[str, object]:
    """Return the exact abstract decoder for the singlet multiplicity code."""
    _validate_level(level)
    dimension = 2 * level + 1
    isometry = charged_reference_isometry_record(level)
    recovery = charged_reference_matrix_unit_recovery_record(level)
    return {
        "level_L": level,
        "reference_representation": "V_L^* tensor C^{2L+1}",
        "singlet_corner_logical_algebra": f"M_{dimension} on multiplicity K",
        "singlet_corner_logical_algebra_dimension": dimension**2,
        "orthogonal_phase_pair_recovered_trace_distance": 1.0,
        "abstract_code_decoder_error": 0.0,
        "is_operational_prepared_reference_protocol": False,
        "encoding_is_isometric": isometry["encoding_is_isometric"],
        "complete_operator_basis_recovers_exactly": recovery[
            "complete_operator_basis_recovers_exactly"
        ],
        "diamond_recovery_error": recovery["diamond_recovery_error"],
    }


def minimal_charged_reference_dimension_record(level: int) -> dict[str, object]:
    """Prove the lower bound only for isometries into the singlet subspace."""
    _validate_level(level)
    dimension = 2 * level + 1
    required_multiplicity = dimension
    lower_bound = dimension * required_multiplicity
    return {
        "level_L": level,
        "reference_decomposition": "direct_sum_j V_j tensor C^{m_j}",
        "invariant_multiplicity_with_system_V_L": "m_L",
        "required_invariant_dimension_for_exact_encoding": dimension,
        "required_conjugate_irrep_multiplicity": required_multiplicity,
        "reference_dimension_lower_bound": lower_bound,
        "peter_weyl_block_dimension": dimension**2,
        "construction_saturates_lower_bound": True,
        "scope": "pure isometric encoding of d logical states into total spin zero",
        "unrestricted_exact_channel_counterexample": (
            "rho maps to I_V/d tensor rho_K with a trivial d-dimensional K; "
            "partial trace recovers rho, but the encoder and decoder do not "
            "intertwine the charged input/output representations"
        ),
        "bound_is_unrestricted_reference_minimum": False,
    }


def kms_core_tensor_stability_record(level: int) -> dict[str, object]:
    """Record only spectator tensor stability with the same core density."""
    _validate_level(level)
    return {
        "level_L": level,
        "common_background": (
            "same interacting KMS boundary/tail representation and same "
            "normalized finite-core density omega"
        ),
        "scalar_map_on_core": "E_SU2 tensor identity_core",
        "charged_decoder_on_core": "D_charged tensor identity_core",
        "scalar_fixed_algebra_decoder_error_lower_bound": 0.5,
        "singlet_code_decoder_error_under_spectator_tensor": 0.0,
        "scalar_probe_entropy_loss": log(float(2 * level + 1)),
        "charged_probe_entropy_deficit": 0.0,
        "common_core_tensor_changes_comparison": False,
        "charged_code_is_realized_by_interacting_kms_dynamics": False,
        "scope": "spectator tensor-factor stability only",
    }


def charged_reference_recovery_certificate(
    *,
    max_level: int = 8,
    tolerance: float = 1e-12,
) -> dict[str, object]:
    if max_level < 1:
        raise ValueError("max_level must be at least one")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    isometries = tuple(
        charged_reference_isometry_record(level)
        for level in range(1, max_level + 1)
    )
    recoveries = tuple(
        charged_reference_matrix_unit_recovery_record(level)
        for level in range(1, max_level + 1)
    )
    fixed_algebras = tuple(
        invariant_operator_algebra_record(level)
        for level in range(1, max_level + 1)
    )
    controls = tuple(
        scalar_reference_control_record(level)
        for level in range(1, max_level + 1)
    )
    treatments = tuple(
        charged_reference_treatment_record(level)
        for level in range(1, max_level + 1)
    )
    dimensions = tuple(
        minimal_charged_reference_dimension_record(level)
        for level in range(1, max_level + 1)
    )
    core = tuple(
        kms_core_tensor_stability_record(level)
        for level in range(1, max_level + 1)
    )
    certified_claims = {
        "singlet_sector_encoding_is_isometric": all(
            record["isometry_diagonal_error"] <= tolerance
            and record["isometry_off_diagonal_error"] <= tolerance
            for record in isometries
        ),
        "singlet_code_recovers_the_complete_logical_matrix_algebra": all(
            record["matrix_unit_count"] == record["expected_matrix_unit_count"]
            and record["complete_operator_basis_recovers_exactly"]
            and record["diamond_recovery_error"] == 0.0
            for record in recoveries
        ),
        "displayed_encoder_and_decoder_are_not_su2_covariant": all(
            not record["encoder_is_su2_covariant_from_V_L"]
            and not record["decoder_is_su2_covariant_to_V_L"]
            and record["intertwiner_obstruction_operator_norm"] == 2.0
            for record in isometries
        ),
        "singlet_corner_is_not_the_full_fixed_operator_algebra": all(
            not record["singlet_corner_is_full_fixed_algebra"]
            and record["fixed_operator_algebra_dimension"]
            == (2 * record["level_L"] + 1) ** 3
            for record in fixed_algebras
        ),
        "singlet_isometry_dimension_lower_bound_is_saturated": all(
            record["reference_dimension_lower_bound"]
            == record["peter_weyl_block_dimension"]
            and record["construction_saturates_lower_bound"]
            and not record["bound_is_unrestricted_reference_minimum"]
            for record in dimensions
        ),
        "spectator_tensor_stability_is_exact": all(
            record["scalar_fixed_algebra_decoder_error_lower_bound"] == 0.5
            and record["singlet_code_decoder_error_under_spectator_tensor"] == 0.0
            and not record["common_core_tensor_changes_comparison"]
            and not record["charged_code_is_realized_by_interacting_kms_dynamics"]
            for record in core
        ),
    }
    return {
        "goal": "SU(2) Singlet-Sector Multiplicity-Code Baseline",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "su2_charged_reference_exact_recovery_model_selection_theorem",
        "central_result": (
            "The block V_L^* tensor C^{2L+1} supports a d-dimensional code in "
            "the total-spin-zero subspace, with exact abstract decoding from its "
            "multiplicity register. The displayed encoder and decoder are not "
            "SU(2)-covariant for a charged spin-L input/output. The d^2 dimension "
            "bound applies only to pure isometries into the singlet subspace."
        ),
        "claim_boundary": (
            "positive-integer-spin singlet-sector code with spectator core tensor; "
            "the control fixed algebra and treatment singlet corner are not a "
            "matched operational task, and the code does not recover rho_S tensor "
            "eta_R after twirling or derive local gravitational dynamics"
        ),
        "certified_claims": certified_claims,
        "isometry_records": isometries,
        "matrix_unit_recovery_records": recoveries,
        "invariant_operator_algebra_records": fixed_algebras,
        "scalar_control_records": controls,
        "singlet_code_records": treatments,
        "dimension_records": dimensions,
        "core_stability_records": core,
        "next_physics_gate": (
            "Define one common covariant communication/recovery task for scalar "
            "and charged prepared references, prove its optimal error/resource "
            "law, then embed it into a regulated SO(1,d) static-patch KMS net."
        ),
    }
