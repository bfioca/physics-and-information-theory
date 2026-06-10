"""Run the trusted graded-mesh derivative-trace audit.

The floating BVP solver is used only to propose exact-rational splines.  The
reported Barta, residual, and trace bounds are recomputed by the trusted
interval checker from those splines.  Large exact fractions are summarized by
their floating value and numerator/denominator bit lengths so reporting does
not depend on Python's decimal integer conversion limit.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from time import perf_counter

from qgtoy.skyrmion_global_bvp_certificate_generator import (
    generate_global_bvp_certificate_candidate,
)
from qgtoy.validated_interval import RationalPolynomial
from qgtoy.validated_skyrmion_bvp import (
    SkyrmionPolynomialCell,
    validate_skyrmion_derivative_trace_representer,
)


def representative_graded_mesh() -> tuple[Fraction, ...]:
    """Return the exact 43-cell mesh selected by the residual scaling study."""
    nodes = [Fraction(1, 16)]
    for segment_end, width in (
        (Fraction(1, 8), Fraction(1, 128)),
        (Fraction(1, 4), Fraction(1, 64)),
        (Fraction(1, 2), Fraction(1, 32)),
    ):
        while nodes[-1] < segment_end:
            nodes.append(nodes[-1] + width)
        if nodes[-1] != segment_end:
            raise AssertionError("graded mesh width must divide its segment")
    while nodes[-1] + Fraction(3, 16) < 4:
        nodes.append(nodes[-1] + Fraction(3, 16))
    nodes.append(Fraction(4))
    result = tuple(nodes)
    if len(result) != 44:
        raise AssertionError("representative graded mesh must have 43 cells")
    return result


def fraction_summary(value: Fraction) -> dict[str, float | int]:
    return {
        "value": float(value),
        "numerator_bits": value.numerator.bit_length(),
        "denominator_bits": value.denominator.bit_length(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integration-step", type=float, default=1 / 512)
    parser.add_argument("--declared-trace", type=int, default=20)
    parser.add_argument("--trigonometric-terms", type=int, default=24)
    parser.add_argument("--residual-taylor-terms", type=int, default=4)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mesh = representative_graded_mesh()
    generation_start = perf_counter()
    candidate = generate_global_bvp_certificate_candidate(
        mesh_nodes=mesh,
        integration_step=args.integration_step,
        trigonometric_terms=8,
        residual_subdivisions=1,
    )
    generation_seconds = perf_counter() - generation_start

    profile_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.profile_polynomial)
        for cell in candidate.cells
    )
    auxiliary_left = candidate.schur_auxiliary_cells[
        0
    ].function_polynomial.evaluate(Fraction(0)).lower
    if auxiliary_left == 0:
        raise ValueError("the proposed Schur auxiliary has zero left trace")
    representer_cells = tuple(
        SkyrmionPolynomialCell(
            cell.radius,
            RationalPolynomial(
                tuple(
                    coefficient / auxiliary_left
                    for coefficient in cell.function_polynomial.coefficients
                )
            ),
        )
        for cell in candidate.schur_auxiliary_cells
    )

    validation_start = perf_counter()
    validation = validate_skyrmion_derivative_trace_representer(
        profile_cells,
        representer_cells,
        declared_barta_lower_bound=Fraction(1),
        declared_trace_upper_bound=Fraction(args.declared_trace),
        barta_initial_subdivisions=2,
        barta_maximum_refinement_depth=5,
        residual_initial_subdivisions=1,
        residual_maximum_refinement_depth=0,
        trigonometric_terms=args.trigonometric_terms,
        residual_taylor_terms=args.residual_taylor_terms,
    )
    validation_seconds = perf_counter() - validation_start
    worst_residual = max(
        validation.residual_cells,
        key=lambda cell: max(abs(cell.residual.lower), abs(cell.residual.upper)),
    )
    report = {
        "result_type": "trusted_graded_derivative_trace_audit",
        "mesh_cell_count": len(profile_cells),
        "generation_seconds": generation_seconds,
        "validation_seconds": validation_seconds,
        "barta_lower_bound": fraction_summary(
            validation.barta_validation.recomputed_lower_bound
        ),
        "barta_leaf_count": len(validation.barta_validation.cells),
        "barta_maximum_depth_used": (
            validation.barta_validation.maximum_refinement_depth_used
        ),
        "approximate_representer_l1": fraction_summary(
            validation.approximate_representer_l1_upper_bound
        ),
        "residual_supremum": fraction_summary(
            validation.residual_supremum_upper_bound
        ),
        "representer_error_l1": fraction_summary(
            validation.representer_error_l1_upper_bound
        ),
        "certified_trace_upper_bound": fraction_summary(
            validation.recomputed_trace_upper_bound
        ),
        "worst_residual_source_cell": worst_residual.source_cell_index,
        "worst_residual_radius": [
            float(worst_residual.radius.lower),
            float(worst_residual.radius.upper),
        ],
        "fixed_sign_l1_cell_count": sum(
            cell.integrated_with_fixed_sign for cell in validation.l1_cells
        ),
        "scope": validation.conclusion_scope,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
