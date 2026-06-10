"""Audit the nonlinear residual of the endpoint-corrected graded profile."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from time import perf_counter

from qgtoy.skyrmion_global_bvp_certificate_generator import (
    generate_global_bvp_certificate_candidate,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_bvp import (
    SkyrmionPolynomialCell,
    validate_skyrmion_endpoint_corrected_residual,
)
from qgtoy.validated_skyrmion_origin import (
    validate_skyrmion_origin_quintic_branch_identification,
    validate_skyrmion_origin_quintic_patch,
    validate_skyrmion_origin_sensitivity,
)

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
    origin = validate_skyrmion_origin_quintic_patch(
        candidate.shooting_slope,
        cutoff=candidate.radius_start,
    )
    sensitivity = validate_skyrmion_origin_sensitivity(
        RationalInterval(
            candidate.shooting_slope - Fraction(1, 10**5),
            candidate.shooting_slope + Fraction(1, 10**5),
        ),
        cutoff=candidate.radius_start,
    )
    branch_identification = validate_skyrmion_origin_quintic_branch_identification(
        origin,
        sensitivity,
    )
    validation_start = perf_counter()
    validation = validate_skyrmion_endpoint_corrected_residual(
        profile_cells,
        origin.profile_at_cutoff,
        origin.derivative_at_cutoff,
        phi_sensitivity_at_cutoff=sensitivity.phi_b,
        gamma_sensitivity_at_cutoff=sensitivity.gamma_b,
        subdivisions_per_source_cell=1,
        trigonometric_terms=24,
        residual_taylor_terms=4,
    )
    validation_seconds = perf_counter() - validation_start
    worst = max(
        validation.cells,
        key=lambda cell: max(abs(cell.residual.lower), abs(cell.residual.upper)),
    )
    report = {
        "result_type": "trusted_endpoint_corrected_nonlinear_residual_audit",
        "mesh_cell_count": len(profile_cells),
        "origin_branch_identified": (
            branch_identification.identified_with_cubic_sensitivity_branch
        ),
        "generation_seconds": generation_seconds,
        "validation_seconds": validation_seconds,
        "origin_profile_at_cutoff": interval_summary(origin.profile_at_cutoff),
        "origin_derivative_at_cutoff": interval_summary(
            origin.derivative_at_cutoff
        ),
        "left_value_correction": interval_summary(
            validation.left_value_correction
        ),
        "right_value_correction": fraction_summary(
            validation.right_value_correction
        ),
        "boundary_slope_residual": interval_summary(
            validation.boundary_slope_residual
        ),
        "nonlinear_residual_supremum": fraction_summary(
            validation.residual_supremum_upper_bound
        ),
        "worst_residual_source_cell": worst.source_cell_index,
        "worst_residual_radius": [
            float(worst.radius.lower),
            float(worst.radius.upper),
        ],
        "worst_midpoint_residual": interval_summary(worst.midpoint_residual),
        "worst_family_error": fraction_summary(
            worst.family_residual_error_upper_bound
        ),
        "scope": validation.conclusion_scope,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="ascii")
    print(rendered)


if __name__ == "__main__":
    main()
