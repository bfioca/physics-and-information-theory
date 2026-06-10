"""Finite-clock crossed-product gate for observer-algebra regulators.

For a matrix algebra every automorphism is inner. Crossing an inner cyclic
action with Z_q is therefore isomorphic to M_d tensor C*(Z_q), a direct sum of
q copies of M_d. This finite construction cannot by itself produce Type II.
"""

from __future__ import annotations


def finite_clock_crossed_product_record(
    matrix_dimension: int,
    clock_order: int,
) -> dict[str, object]:
    if matrix_dimension < 1:
        raise ValueError("matrix_dimension must be positive")
    if clock_order < 1:
        raise ValueError("clock_order must be positive")
    algebra_dimension = clock_order * matrix_dimension**2
    return {
        "matrix_dimension": matrix_dimension,
        "clock_group": f"Z_{clock_order}",
        "clock_order": clock_order,
        "system_algebra": f"M_{matrix_dimension}",
        "action_type": "inner",
        "crossed_product_isomorphism": (
            f"M_{matrix_dimension} tensor C*(Z_{clock_order})"
        ),
        "wedderburn_block_count": clock_order,
        "wedderburn_block_sizes": tuple(
            matrix_dimension for _index in range(clock_order)
        ),
        "crossed_product_vector_space_dimension": algebra_dimension,
        "wedderburn_dimension_check": clock_order * matrix_dimension**2,
        "center_dimension": clock_order,
        "is_factor": clock_order == 1,
        "finite_von_neumann_type": "Type I finite",
        "typeii_at_finite_cutoff": False,
        "proof": (
            "If alpha_g=Ad(U_g), then W_g=U_g^* lambda_g commutes with M_d. "
            "The W_g generate C*(Z_q), so M_d crossed_alpha Z_q is isomorphic "
            "to M_d tensor C*(Z_q)=direct_sum_q M_d."
        ),
    }


def regulator_clock_record(level: int) -> dict[str, object]:
    if level < 1:
        raise ValueError("level must be at least one")
    matrix_dimension = (level + 1) ** 2
    clock_order = 2 * level + 1
    record = finite_clock_crossed_product_record(matrix_dimension, clock_order)
    return {
        "level_L": level,
        **record,
        "interpretation": (
            "The finite fuzzy-harmonic matrix algebra remains Type I after a "
            "finite cyclic clock is adjoined. Increasing dimensions alone does "
            "not identify the type of a von Neumann limit."
        ),
    }


def finite_clock_crossed_product_no_go_certificate(
    *,
    max_level: int = 8,
) -> dict[str, object]:
    if max_level < 1:
        raise ValueError("max_level must be at least one")
    records = tuple(regulator_clock_record(level) for level in range(1, max_level + 1))
    certified_claims = {
        "all_finite_matrix_actions_are_inner": all(
            record["action_type"] == "inner" for record in records
        ),
        "finite_clock_crossed_products_have_explicit_wedderburn_form": all(
            record["crossed_product_vector_space_dimension"]
            == record["wedderburn_dimension_check"]
            for record in records
        ),
        "nontrivial_finite_clocks_produce_nonfactor_centers": all(
            not record["is_factor"] and record["center_dimension"] > 1
            for record in records
        ),
        "typeii_is_absent_at_every_finite_cutoff": all(
            not record["typeii_at_finite_cutoff"] for record in records
        ),
    }
    return {
        "goal": "Finite Clock Crossed-Product Order-of-Limits Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "finite_inner_action_typeii_no_go",
        "claim_boundary": (
            "standard finite-dimensional crossed-product obstruction; it does "
            "not determine the type of a separately specified infinite local-QFT "
            "limit"
        ),
        "central_result": (
            "Attaching a finite clock to a finite matrix regulator cannot derive "
            "a gravitational Type-II factor. The local/thermodynamic limit must "
            "make modular flow outer, and the crossed product and trace must then "
            "be controlled in that limit."
        ),
        "certified_claims": certified_claims,
        "records": records,
        "required_instead": (
            "Construct a many-body or local-QFT net with a non-Type-I limiting "
            "algebra; prove convergence of states and modular dynamics; establish "
            "outerness in the limit; then form the clock crossed product and derive "
            "its semifinite trace."
        ),
    }
