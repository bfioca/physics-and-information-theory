"""Certify sharp Green-parametrix resolvent norms on the graded AU.1 mesh."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from time import perf_counter

from qgtoy.skyrmion_global_bvp_certificate_generator import (
    generate_global_bvp_certificate_candidate,
)
from qgtoy.validated_interval import RationalPolynomial
from qgtoy.validated_skyrmion_bvp import (
    SkyrmionPolynomialCell,
    validate_skyrmion_green_resolvent_bounds,
)

from experiments.skyrmion_graded_trace_audit import (
    fraction_summary,
    representative_graded_mesh,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generation_start = perf_counter()
    candidate = generate_global_bvp_certificate_candidate(
        mesh_nodes=representative_graded_mesh(),
        integration_step=1 / 512,
        trigonometric_terms=8,
        residual_subdivisions=1,
    )
    generation_seconds = perf_counter() - generation_start
    profile_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.profile_polynomial)
        for cell in candidate.cells
    )
    fundamental_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.function_polynomial)
        for cell in candidate.fundamental_cells
    )
    auxiliary_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.function_polynomial)
        for cell in candidate.schur_auxiliary_cells
    )
    auxiliary_left = auxiliary_cells[0].profile_polynomial.evaluate(0).lower
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
    validation_start = perf_counter()
    validation = validate_skyrmion_green_resolvent_bounds(
        profile_cells,
        fundamental_cells,
        representer_cells,
        Fraction(1),
        Fraction(81_575, 1_000_000),
        subdivisions_per_source_cell=1,
        barta_initial_subdivisions=2,
        barta_maximum_refinement_depth=5,
        trigonometric_terms=24,
        residual_taylor_terms=4,
    )
    validation_seconds = perf_counter() - validation_start
    worst_defect = max(
        validation.cells,
        key=lambda cell: cell.operator_defect_upper_bound,
    )
    report = {
        "result_type": "trusted_skyrmion_green_resolvent_audit",
        "mesh_cell_count": len(profile_cells),
        "generation_seconds": generation_seconds,
        "validation_seconds": validation_seconds,
        "wronskian_normalization": fraction_summary(
            validation.wronskian_normalization
        ),
        "initial_wronskian_lower": fraction_summary(
            validation.initial_wronskian_enclosure.lower
        ),
        "initial_wronskian_upper": fraction_summary(
            validation.initial_wronskian_enclosure.upper
        ),
        "operator_defect_upper_bound": fraction_summary(
            validation.operator_defect_upper_bound
        ),
        "approximate_c0_upper_bound": fraction_summary(
            validation.approximate_c0_upper_bound
        ),
        "approximate_c1_upper_bound": fraction_summary(
            validation.approximate_c1_upper_bound
        ),
        "approximate_c2_upper_bound": fraction_summary(
            validation.approximate_c2_upper_bound
        ),
        "c0_upper_bound": fraction_summary(validation.c0_upper_bound),
        "c1_upper_bound": fraction_summary(validation.c1_upper_bound),
        "c2_upper_bound": fraction_summary(validation.c2_upper_bound),
        "worst_defect_source_cell": worst_defect.source_cell_index,
        "worst_defect_radius": [
            float(worst_defect.radius.lower),
            float(worst_defect.radius.upper),
        ],
        "scope": validation.conclusion_scope,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="ascii")
    print(rendered)


if __name__ == "__main__":
    main()
