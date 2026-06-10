"""Run the trusted trace-sharpened Schur audit on the graded candidate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from time import perf_counter

from qgtoy.skyrmion_global_bvp_certificate_generator import (
    generate_global_bvp_certificate_candidate,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import (
    SkyrmionPolynomialCell,
    validate_skyrmion_trace_sharpened_schur_bound,
)
from qgtoy.validated_skyrmion_origin import validate_skyrmion_origin_sensitivity

from experiments.skyrmion_graded_trace_audit import (
    fraction_summary,
    representative_graded_mesh,
)


def interval_summary(value: RationalInterval) -> dict[str, object]:
    return {
        "lower": fraction_summary(value.lower),
        "upper": fraction_summary(value.upper),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integration-step", type=float, default=1 / 512)
    parser.add_argument("--declared-trace", type=int, default=20)
    parser.add_argument("--declared-schur", type=Fraction, default=Fraction(14, 5))
    parser.add_argument("--trigonometric-terms", type=int, default=24)
    parser.add_argument("--residual-taylor-terms", type=int, default=4)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generation_start = perf_counter()
    candidate = generate_global_bvp_certificate_candidate(
        mesh_nodes=representative_graded_mesh(),
        integration_step=args.integration_step,
        trigonometric_terms=8,
        residual_subdivisions=1,
    )
    generation_seconds = perf_counter() - generation_start
    profile_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.profile_polynomial)
        for cell in candidate.cells
    )
    auxiliary_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.function_polynomial)
        for cell in candidate.schur_auxiliary_cells
    )
    auxiliary_left = auxiliary_cells[0].profile_polynomial.evaluate(
        Fraction(0)
    ).lower
    if auxiliary_left == 0:
        raise ValueError("the proposed Schur auxiliary has zero left trace")
    representer_cells = tuple(
        SkyrmionPolynomialCell(
            cell.radius,
            RationalPolynomial(
                tuple(
                    coefficient / auxiliary_left
                    for coefficient in cell.profile_polynomial.coefficients
                )
            ),
        )
        for cell in auxiliary_cells
    )
    sensitivity_width = Fraction(1, 10**5)
    origin = validate_skyrmion_origin_sensitivity(
        RationalInterval(
            candidate.shooting_slope - sensitivity_width,
            candidate.shooting_slope + sensitivity_width,
        ),
        cutoff=candidate.radius_start,
    )

    validation_start = perf_counter()
    validation = validate_skyrmion_trace_sharpened_schur_bound(
        profile_cells,
        auxiliary_cells,
        representer_cells,
        origin.phi_b,
        origin.gamma_b,
        declared_barta_lower_bound=Fraction(1),
        declared_trace_upper_bound=Fraction(args.declared_trace),
        declared_schur_lower_bound=args.declared_schur,
        barta_initial_subdivisions=2,
        barta_maximum_refinement_depth=5,
        trace_residual_initial_subdivisions=1,
        trace_residual_maximum_refinement_depth=0,
        schur_residual_initial_subdivisions=1,
        schur_residual_maximum_refinement_depth=0,
        trigonometric_terms=args.trigonometric_terms,
        residual_taylor_terms=args.residual_taylor_terms,
    )
    validation_seconds = perf_counter() - validation_start
    worst_residual = max(
        validation.residual_cells,
        key=lambda cell: max(abs(cell.residual.lower), abs(cell.residual.upper)),
    )
    trace = validation.trace_validation
    graph = validation.graph_resolvent_bounds
    auxiliary_norms = validation.auxiliary_norm_bounds
    report = {
        "result_type": "trusted_graded_trace_sharpened_schur_audit",
        "mesh_cell_count": len(profile_cells),
        "generation_seconds": generation_seconds,
        "validation_seconds": validation_seconds,
        "barta_lower_bound": fraction_summary(
            trace.barta_validation.recomputed_lower_bound
        ),
        "certified_trace_upper_bound": fraction_summary(
            validation.derivative_trace_upper_bound
        ),
        "trace_residual_supremum": fraction_summary(
            trace.residual_supremum_upper_bound
        ),
        "raw_schur_enclosure": interval_summary(validation.raw_schur_enclosure),
        "schur_residual_supremum": fraction_summary(
            validation.residual_supremum_upper_bound
        ),
        "boundary_derivative_error": fraction_summary(
            validation.boundary_derivative_error_bound
        ),
        "graph_resolvent_bounds": {
            "principal_lower_bound": fraction_summary(
                graph.principal_lower_bound
            ),
            "principal_derivative_supremum": fraction_summary(
                graph.principal_derivative_supremum_upper_bound
            ),
            "potential_l1": fraction_summary(graph.potential_l1_upper_bound),
            "potential_supremum": fraction_summary(
                graph.potential_supremum_upper_bound
            ),
            "c0": fraction_summary(graph.c0_upper_bound),
            "c1": fraction_summary(graph.c1_upper_bound),
            "c2": fraction_summary(graph.c2_upper_bound),
        },
        "auxiliary_norm_bounds": {
            "approximate_c0": fraction_summary(
                auxiliary_norms.approximate_c0_upper_bound
            ),
            "approximate_c1": fraction_summary(
                auxiliary_norms.approximate_c1_upper_bound
            ),
            "approximate_c2": fraction_summary(
                auxiliary_norms.approximate_c2_upper_bound
            ),
            "corrected_c0": fraction_summary(
                auxiliary_norms.corrected_c0_upper_bound
            ),
            "corrected_c1": fraction_summary(
                auxiliary_norms.corrected_c1_upper_bound
            ),
            "corrected_c2": fraction_summary(
                auxiliary_norms.corrected_c2_upper_bound
            ),
        },
        "corrected_schur_enclosure": interval_summary(
            validation.corrected_schur_enclosure
        ),
        "declared_schur_lower_bound": fraction_summary(
            validation.declared_schur_lower_bound
        ),
        "worst_schur_residual_source_cell": worst_residual.source_cell_index,
        "worst_schur_residual_radius": [
            float(worst_residual.radius.lower),
            float(worst_residual.radius.upper),
        ],
        "scope": validation.conclusion_scope,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="ascii")
    print(rendered)


if __name__ == "__main__":
    main()
