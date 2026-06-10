"""Compose the trusted AU.1 linear and Newton-center audits through ``Z0``."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter

from qgtoy.skyrmion_global_bvp_certificate_generator import (
    generate_global_bvp_certificate_candidate,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import (
    SkyrmionPolynomialCell,
    reweight_skyrmion_augmented_operator_mismatch,
    sharpen_skyrmion_schur_with_green_resolvent,
    validate_skyrmion_augmented_newton_tube,
    validate_skyrmion_augmented_operator_mismatch,
    validate_skyrmion_endpoint_corrected_residual,
    validate_skyrmion_green_resolvent_bounds,
    validate_skyrmion_newton_physical_observables,
    validate_skyrmion_trace_sharpened_schur_bound,
)
from qgtoy.validated_skyrmion_origin import (
    validate_skyrmion_origin_family,
    validate_skyrmion_origin_quintic_branch_identification,
    validate_skyrmion_origin_quintic_patch,
    validate_skyrmion_origin_second_sensitivity,
    validate_skyrmion_origin_sensitivity,
)
from qgtoy.validated_skyrmion_spectral_derivatives import (
    ValidatedSkyrmionGlobalDerivativeNorms,
    ValidatedSkyrmionPositiveDerivativeNorms,
    validate_skyrmion_global_derivative_norms,
)

from experiments.skyrmion_graded_trace_audit import (
    fraction_summary,
    representative_graded_mesh,
)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--exact-certificate-output",
        type=Path,
        help="archive exact rational inputs, outputs, and provenance",
    )
    parser.add_argument(
        "--stop-after-mismatch",
        action="store_true",
        help="write the exact linearized audit without evaluating Newton tubes",
    )
    parser.add_argument(
        "--omega",
        type=Fraction,
        help="use one exact augmented-norm weight, for example 1 or 3/2",
    )
    parser.add_argument(
        "--tube-radius",
        action="append",
        type=Fraction,
        help="evaluate one exact tube radius; repeat to request a small sweep",
    )
    parser.add_argument(
        "--tube-trigonometric-terms",
        type=int,
        default=16,
        help="Taylor terms for exact tube trigonometric enclosures",
    )
    parser.add_argument(
        "--tube-rounding-denominator",
        type=int,
        default=10**18,
        help="outward-round tube intermediates to this rational grid",
    )
    parser.add_argument(
        "--spectral-trigonometric-terms",
        type=int,
        default=24,
        help="Taylor terms for positive-radius AU.2 trigonometric jets",
    )
    parser.add_argument(
        "--spectral-atanh-terms",
        type=int,
        default=80,
        help="Taylor terms for directed optical-radius enclosures",
    )
    parser.add_argument(
        "--spectral-pi-terms",
        type=int,
        default=80,
        help="Machin-series terms for directed AU.2 pi enclosures",
    )
    parser.add_argument(
        "--origin-kernel-terms",
        type=int,
        default=20,
        help="entire-kernel terms for the regular-origin AU.2 Lie bounds",
    )
    return parser.parse_args()


def admissible_newton_tube_radii(
    radii: tuple[Fraction, ...],
    *,
    newton_defect_upper_bound: Fraction,
    z0_upper_bound: Fraction,
    maximum_radius: Fraction | None = None,
) -> tuple[Fraction, ...]:
    """Remove radii that cannot satisfy the exact radii inequalities."""

    if z0_upper_bound >= 1:
        return ()
    minimum_radius = newton_defect_upper_bound / (1 - z0_upper_bound)
    return tuple(
        radius
        for radius in radii
        if radius > minimum_radius
        and (maximum_radius is None or radius <= maximum_radius)
    )


def newton_tube_feasibility_margin(result: object) -> Fraction:
    """Return a dimensionless joint margin for the two Newton inequalities."""

    radius = result.radius
    if radius <= 0:
        raise ValueError("Newton tube radius must be positive")
    return max(
        result.radii_polynomial_upper_bound / radius,
        result.contraction_upper_bound - 1,
    )


def _exact_interval_record(value: RationalInterval) -> dict[str, str]:
    return {"lower": str(value.lower), "upper": str(value.upper)}


def _exact_polynomial_cell_record(
    cell: SkyrmionPolynomialCell,
) -> dict[str, object]:
    return {
        "radius": _exact_interval_record(cell.radius),
        "coefficients": tuple(
            str(coefficient)
            for coefficient in cell.profile_polynomial.coefficients
        ),
    }


def _exact_positive_derivative_record(
    result: ValidatedSkyrmionPositiveDerivativeNorms,
) -> dict[str, object]:
    return {
        "certificate_id": result.certificate_id,
        "origin_cutoff": str(result.origin_cutoff),
        "wall_radius": str(result.wall_radius),
        "positive_optical_domain": _exact_interval_record(
            result.positive_optical_domain
        ),
        "optical_wall": _exact_interval_record(result.optical_wall),
        "w_positive_l1_upper_bounds": tuple(
            str(value) for value in result.w_positive_l1_upper_bounds
        ),
        "a_positive_l1_upper_bounds": tuple(
            str(value) for value in result.a_positive_l1_upper_bounds
        ),
        "origin_norms_required": result.origin_norms_required,
        "global_norms_certified": result.global_norms_certified,
        "conclusion_scope": result.conclusion_scope,
        "cells": tuple(
            {
                "source_cell_index": cell.source_cell_index,
                "radius": _exact_interval_record(cell.radius),
                "optical_radius": _exact_interval_record(cell.optical_radius),
                "w_third_derivative_enclosures": tuple(
                    _exact_interval_record(value)
                    for value in cell.w_third_derivative_enclosures
                ),
                "a_third_derivative_enclosures": tuple(
                    _exact_interval_record(value)
                    for value in cell.a_third_derivative_enclosures
                ),
                "w_l1_contribution_upper_bounds": tuple(
                    str(value)
                    for value in cell.w_l1_contribution_upper_bounds
                ),
                "a_l1_contribution_upper_bounds": tuple(
                    str(value)
                    for value in cell.a_l1_contribution_upper_bounds
                ),
            }
            for cell in result.cells
        ),
    }


def _exact_global_derivative_record(
    result: ValidatedSkyrmionGlobalDerivativeNorms,
) -> dict[str, object]:
    origin = result.origin
    return {
        "certificate_id": result.certificate_id,
        "global_norms_certified": result.global_norms_certified,
        "w_third_derivative_l1_upper_bounds": tuple(
            str(value) for value in result.w_third_derivative_l1_upper_bounds
        ),
        "a_third_derivative_l1_upper_bounds": tuple(
            str(value) for value in result.a_third_derivative_l1_upper_bounds
        ),
        "origin": {
            "origin_cutoff": str(origin.origin_cutoff),
            "optical_cutoff_upper_bound": str(
                origin.optical_cutoff_upper_bound
            ),
            "time_box": _exact_interval_record(origin.time_box),
            "profile_box": _exact_interval_record(origin.profile_box),
            "momentum_box": _exact_interval_record(origin.momentum_box),
            "volterra_denominator_enclosure": _exact_interval_record(
                origin.volterra_denominator_enclosure
            ),
            "weight_factor_absolute_upper_bound": str(
                origin.weight_factor_absolute_upper_bound
            ),
            "lie_derivative_over_time_upper_bounds": tuple(
                str(value)
                for value in origin.lie_derivative_over_time_upper_bounds
            ),
            "w_optical_derivative_upper_bounds": tuple(
                str(value)
                for value in origin.w_optical_derivative_upper_bounds
            ),
            "a_optical_derivative_upper_bounds": tuple(
                str(value)
                for value in origin.a_optical_derivative_upper_bounds
            ),
            "w_origin_l1_upper_bounds": tuple(
                str(value) for value in origin.w_origin_l1_upper_bounds
            ),
            "a_origin_l1_upper_bounds": tuple(
                str(value) for value in origin.a_origin_l1_upper_bounds
            ),
            "conclusion_scope": origin.conclusion_scope,
        },
        "spectral_ledger": result.spectral_ledger.to_record(),
        "conclusion_scope": result.conclusion_scope,
    }


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        Path("experiments/skyrmion_newton_linearization_audit.py"),
        Path("experiments/skyrmion_graded_trace_audit.py"),
        Path("qgtoy/skyrmion_global_bvp_certificate_generator.py"),
        Path("qgtoy/validated_interval.py"),
        Path("qgtoy/validated_skyrmion_bvp.py"),
        Path("qgtoy/validated_skyrmion_origin.py"),
        Path("qgtoy/validated_skyrmion_origin_derivatives.py"),
        Path("qgtoy/validated_skyrmion_spectral_derivatives.py"),
        Path("qgtoy/validated_skyrmion_spectral_ledger.py"),
    )
    return {str(path): _sha256_bytes(path.read_bytes()) for path in paths}


def _dependency_versions() -> dict[str, str]:
    result = {"python": sys.version}
    for package in ("numpy", "scipy"):
        try:
            result[package] = version(package)
        except PackageNotFoundError:
            result[package] = "not-installed"
    return result


def select_best_newton_tube(results: tuple[object, ...]) -> object | None:
    """Select the tube with the strongest joint self-map/contraction margin."""

    if not results:
        return None
    return min(
        results,
        key=lambda result: (
            newton_tube_feasibility_margin(result),
            result.radii_polynomial_upper_bound / result.radius,
            result.contraction_upper_bound,
        ),
    )


def main() -> None:
    args = parse_args()
    if args.tube_trigonometric_terms < 1:
        raise ValueError("tube trigonometric terms must be positive")
    if args.tube_rounding_denominator < 1:
        raise ValueError("tube rounding denominator must be positive")
    if args.spectral_trigonometric_terms < 1:
        raise ValueError("spectral trigonometric terms must be positive")
    if args.spectral_atanh_terms < 1:
        raise ValueError("spectral atanh terms must be positive")
    if args.spectral_pi_terms < 1:
        raise ValueError("spectral pi terms must be positive")
    if args.origin_kernel_terms <= 4:
        raise ValueError("origin kernel terms must exceed four")
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
    auxiliary_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.function_polynomial)
        for cell in candidate.schur_auxiliary_cells
    )
    fundamental_cells = tuple(
        SkyrmionPolynomialCell(cell.radius, cell.function_polynomial)
        for cell in candidate.fundamental_cells
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
    phase_seconds: dict[str, float] = {}
    phase_start = perf_counter()
    schur = validate_skyrmion_trace_sharpened_schur_bound(
        profile_cells,
        auxiliary_cells,
        representer_cells,
        sensitivity.phi_b,
        sensitivity.gamma_b,
        Fraction(1),
        Fraction(20),
        Fraction(14, 5),
        barta_initial_subdivisions=2,
        barta_maximum_refinement_depth=5,
        trace_residual_initial_subdivisions=1,
        trace_residual_maximum_refinement_depth=0,
        schur_residual_initial_subdivisions=1,
        schur_residual_maximum_refinement_depth=0,
        trigonometric_terms=24,
        residual_taylor_terms=4,
    )
    phase_seconds["schur"] = perf_counter() - phase_start
    phase_start = perf_counter()
    green = validate_skyrmion_green_resolvent_bounds(
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
        barta_validation=schur.trace_validation.barta_validation,
    )
    phase_seconds["green"] = perf_counter() - phase_start
    phase_start = perf_counter()
    schur = sharpen_skyrmion_schur_with_green_resolvent(schur, green)
    endpoint = validate_skyrmion_endpoint_corrected_residual(
        profile_cells,
        origin.profile_at_cutoff,
        origin.derivative_at_cutoff,
        phi_sensitivity_at_cutoff=sensitivity.phi_b,
        gamma_sensitivity_at_cutoff=sensitivity.gamma_b,
        subdivisions_per_source_cell=1,
        trigonometric_terms=24,
        residual_taylor_terms=4,
    )
    phase_seconds["green_sharpening_and_endpoint"] = (
        perf_counter() - phase_start
    )
    phase_start = perf_counter()
    omega_candidates = (
        (args.omega,)
        if args.omega is not None
        else (
            Fraction(1),
            Fraction(1, 2),
            Fraction(1, 3),
            Fraction(4, 15),
            Fraction(1, 4),
            Fraction(1, 5),
            Fraction(1, 10),
        )
    )
    if any(omega <= 0 for omega in omega_candidates):
        raise ValueError("omega must be positive")
    base_mismatch = validate_skyrmion_augmented_operator_mismatch(
        schur,
        endpoint,
        omega=omega_candidates[0],
    )
    mismatches = (base_mismatch,) + tuple(
        reweight_skyrmion_augmented_operator_mismatch(
            schur,
            endpoint,
            base_mismatch,
            omega=omega,
        )
        for omega in omega_candidates[1:]
    )
    mismatch = min(mismatches, key=lambda result: result.z0_upper_bound)
    phase_seconds["operator_mismatch_and_reweighting"] = (
        perf_counter() - phase_start
    )
    phase_start = perf_counter()
    wide_second_sensitivity = (
        None
        if args.stop_after_mismatch
        else validate_skyrmion_origin_second_sensitivity(
            RationalInterval(
                candidate.shooting_slope - Fraction(1, 50),
                candidate.shooting_slope + Fraction(1, 50),
            ),
            cutoff=candidate.radius_start,
            remainder_radius=Fraction(20),
        )
    )
    phase_seconds["origin_second_sensitivity"] = perf_counter() - phase_start
    phase_start = perf_counter()
    tube_radii = (
        tuple(args.tube_radius)
        if args.tube_radius is not None
        else (
            Fraction(1, 1000),
            Fraction(1, 500),
            Fraction(1, 400),
            Fraction(1, 300),
            Fraction(1, 250),
        )
    )
    if any(radius <= 0 for radius in tube_radii):
        raise ValueError("tube radii must be positive")
    slope_room = min(
        candidate.shooting_slope - wide_second_sensitivity.shooting_slopes.lower,
        wide_second_sensitivity.shooting_slopes.upper - candidate.shooting_slope,
    ) if wide_second_sensitivity is not None else Fraction(0)
    mismatch_tube_results = tuple(
        (candidate_mismatch, result)
        for candidate_mismatch in mismatches
        for radius in (
            ()
            if args.stop_after_mismatch
            else admissible_newton_tube_radii(
                tube_radii,
                newton_defect_upper_bound=(
                    candidate_mismatch.newton_defect_upper_bound
                ),
                z0_upper_bound=candidate_mismatch.z0_upper_bound,
                maximum_radius=candidate_mismatch.omega * slope_room,
            )
        )
        for result in (
            validate_skyrmion_augmented_newton_tube(
                schur,
                endpoint,
                candidate_mismatch,
                branch_identification,
                wide_second_sensitivity,
                radius,
                trigonometric_terms=args.tube_trigonometric_terms,
                rounding_denominator=args.tube_rounding_denominator,
            ),
        )
    )
    tube_results = tuple(result for _, result in mismatch_tube_results)
    phase_seconds["newton_tube_sweep"] = perf_counter() - phase_start
    best_tube = select_best_newton_tube(tube_results)
    if best_tube is not None:
        mismatch = next(
            candidate_mismatch
            for candidate_mismatch, result in mismatch_tube_results
            if result is best_tube
        )
    physical_observables = None
    physical_failures: list[dict[str, str]] = []
    phase_start = perf_counter()
    physical_candidates = []
    for candidate_tube in sorted(
        (
            result
            for result in tube_results
            if result.self_map_verified and result.contraction_verified
        ),
        key=newton_tube_feasibility_margin,
    ):
        try:
            tube_origin_family = validate_skyrmion_origin_family(
                candidate_tube.shooting_slope_interval,
                cutoff=candidate_tube.origin_cutoff,
                remainder_radius=candidate_tube.origin_remainder_radius,
                pion_mass_squared=candidate_tube.pion_mass_squared,
                curvature=candidate_tube.curvature,
            )
            candidate_observables = (
                validate_skyrmion_newton_physical_observables(
                    candidate_tube,
                    tube_origin_family,
                )
            )
        except ValueError as exc:
            physical_failures.append(
                {
                    "omega": str(candidate_tube.omega),
                    "radius": str(candidate_tube.radius),
                    "reason": str(exc),
                }
            )
        else:
            physical_candidates.append(
                (candidate_tube, candidate_observables)
            )
    if physical_candidates:
        best_tube, physical_observables = min(
            physical_candidates,
            key=lambda item: newton_tube_feasibility_margin(item[0]),
        )
        mismatch = next(
            candidate_mismatch
            for candidate_mismatch, result in mismatch_tube_results
            if result is best_tube
        )
    phase_seconds["physical_observables"] = perf_counter() - phase_start
    positive_derivative_norms = None
    global_derivative_norms = None
    phase_start = perf_counter()
    if physical_observables is not None:
        global_derivative_norms = validate_skyrmion_global_derivative_norms(
            physical_observables,
            positive_trigonometric_terms=args.spectral_trigonometric_terms,
            origin_kernel_terms=args.origin_kernel_terms,
            atanh_terms=args.spectral_atanh_terms,
            pi_terms=args.spectral_pi_terms,
            rounding_denominator=args.tube_rounding_denominator,
        )
        positive_derivative_norms = global_derivative_norms.positive_radius
    phase_seconds["global_derivative_norms"] = perf_counter() - phase_start
    validation_seconds = perf_counter() - validation_start
    worst = max(
        mismatch.cells,
        key=lambda cell: cell.interior_operator_mismatch_upper_bound,
    )
    worst_tube_cells = {
        (result.omega, result.radius): max(
            result.cells,
            key=lambda cell: cell.interior_augmented_hessian_upper_bound,
        )
        for result in tube_results
    }
    exact_certificate_path = args.exact_certificate_output
    if exact_certificate_path is None and args.output is not None:
        exact_certificate_path = args.output.with_name(
            f"{args.output.stem}_exact_certificate.json"
        )
    exact_certificate_sha256 = None
    if best_tube is not None:
        exact_outputs = {
            "omega": str(best_tube.omega),
            "radius": str(best_tube.radius),
            "newton_defect_upper_bound": str(
                mismatch.newton_defect_upper_bound
            ),
            "z0_upper_bound": str(mismatch.z0_upper_bound),
            "interior_hessian_upper_bound": str(
                best_tube.interior_hessian_upper_bound
            ),
            "interior_hessian_trace_upper_bound": str(
                best_tube.interior_hessian_trace_upper_bound
            ),
            "schur_composed_hessian_upper_bound": str(
                best_tube.schur_composed_hessian_upper_bound
            ),
            "radii_polynomial_upper_bound": str(
                best_tube.radii_polynomial_upper_bound
            ),
            "contraction_upper_bound": str(
                best_tube.contraction_upper_bound
            ),
            "self_map_verified": best_tube.self_map_verified,
            "contraction_verified": best_tube.contraction_verified,
        }
        if physical_observables is not None:
            exact_outputs.update(
                {
                    "wall_slope_enclosure": _exact_interval_record(
                        physical_observables.wall_slope_enclosure
                    ),
                    "inertia_enclosure": _exact_interval_record(
                        physical_observables.inertia_enclosure
                    ),
                    "strict_monotonicity_verified": (
                        physical_observables.strict_monotonicity_verified
                    ),
                    "negative_wall_slope_verified": (
                        physical_observables.negative_wall_slope_verified
                    ),
                    "positive_finite_inertia_verified": (
                        physical_observables.positive_finite_inertia_verified
                    ),
                }
            )
        if positive_derivative_norms is not None:
            exact_outputs["au2_positive_derivative_norms"] = (
                _exact_positive_derivative_record(positive_derivative_norms)
            )
        if global_derivative_norms is not None:
            exact_outputs["au2_global_derivative_norms_and_tail"] = (
                _exact_global_derivative_record(global_derivative_norms)
            )
        exact_certificate = {
            "result_type": (
                "exact_rational_skyrmion_au1_and_au2_global_tail_certificate"
            ),
            "command": tuple(sys.argv),
            "dependency_versions": _dependency_versions(),
            "source_sha256": _source_hashes(),
            "parameters": {
                "pion_mass_squared": str(best_tube.pion_mass_squared),
                "curvature": str(best_tube.curvature),
                "origin_cutoff": str(best_tube.origin_cutoff),
                "wall_radius": str(best_tube.wall_radius),
                "tube_trigonometric_terms": args.tube_trigonometric_terms,
                "tube_rounding_denominator": (
                    args.tube_rounding_denominator
                ),
                "spectral_trigonometric_terms": (
                    args.spectral_trigonometric_terms
                ),
                "spectral_atanh_terms": args.spectral_atanh_terms,
                "spectral_pi_terms": args.spectral_pi_terms,
                "origin_kernel_terms": args.origin_kernel_terms,
                "shooting_slope": str(candidate.shooting_slope),
            },
            "profile_cells": tuple(
                _exact_polynomial_cell_record(cell) for cell in profile_cells
            ),
            "auxiliary_cells": tuple(
                _exact_polynomial_cell_record(cell) for cell in auxiliary_cells
            ),
            "fundamental_cells": tuple(
                _exact_polynomial_cell_record(cell) for cell in fundamental_cells
            ),
            "representer_cells": tuple(
                _exact_polynomial_cell_record(cell) for cell in representer_cells
            ),
            "exact_outputs": exact_outputs,
        }
        exact_rendered = json.dumps(
            exact_certificate,
            indent=2,
            sort_keys=True,
        ) + "\n"
        exact_certificate_sha256 = _sha256_bytes(exact_rendered.encode("ascii"))
        if exact_certificate_path is not None:
            exact_certificate_path.write_text(exact_rendered, encoding="ascii")
    report = {
        "result_type": "trusted_skyrmion_newton_linearization_audit",
        "mesh_cell_count": len(profile_cells),
        "tube_trigonometric_terms": args.tube_trigonometric_terms,
        "tube_rounding_denominator": args.tube_rounding_denominator,
        "exact_certificate_archive": (
            None
            if exact_certificate_path is None
            else str(exact_certificate_path)
        ),
        "exact_certificate_sha256": exact_certificate_sha256,
        "generation_seconds": generation_seconds,
        "validation_seconds": validation_seconds,
        "phase_seconds": phase_seconds,
        "barta_lower_bound": fraction_summary(
            schur.trace_validation.barta_validation.recomputed_lower_bound
        ),
        "origin_branch_identified": (
            branch_identification.identified_with_cubic_sensitivity_branch
        ),
        "origin_momentum_nesting_bound": fraction_summary(
            branch_identification.normalized_momentum_offset_upper_bound
        ),
        "origin_profile_nesting_bound": fraction_summary(
            branch_identification.normalized_profile_offset_upper_bound
        ),
        "trace_upper_bound": fraction_summary(
            schur.derivative_trace_upper_bound
        ),
        "green_operator_defect": fraction_summary(
            green.operator_defect_upper_bound
        ),
        "green_c0_upper_bound": fraction_summary(green.c0_upper_bound),
        "green_c1_upper_bound": fraction_summary(green.c1_upper_bound),
        "green_c2_upper_bound": fraction_summary(green.c2_upper_bound),
        "green_corrected_auxiliary_c0": fraction_summary(
            schur.auxiliary_norm_bounds.corrected_c0_upper_bound
        ),
        "green_corrected_auxiliary_c1": fraction_summary(
            schur.auxiliary_norm_bounds.corrected_c1_upper_bound
        ),
        "green_corrected_auxiliary_c2": fraction_summary(
            schur.auxiliary_norm_bounds.corrected_c2_upper_bound
        ),
        "schur_lower_bound": fraction_summary(
            schur.corrected_schur_enclosure.lower
        ),
        "augmented_inverse_upper_bound": fraction_summary(
            mismatch.augmented_inverse_upper_bound
        ),
        "nonlinear_residual_supremum": fraction_summary(
            mismatch.nonlinear_residual_supremum_upper_bound
        ),
        "nonlinear_residual_trace": fraction_summary(
            mismatch.nonlinear_residual_trace_upper_bound
        ),
        "boundary_slope_residual_absolute_upper_bound": fraction_summary(
            mismatch.boundary_slope_residual_absolute_upper_bound
        ),
        "newton_defect_upper_bound": fraction_summary(
            mismatch.newton_defect_upper_bound
        ),
        "interior_operator_mismatch_upper_bound": fraction_summary(
            mismatch.interior_operator_mismatch_upper_bound
        ),
        "operator_mismatch_trace_upper_bound": fraction_summary(
            mismatch.operator_mismatch_trace_upper_bound
        ),
        "z0_upper_bound": fraction_summary(mismatch.z0_upper_bound),
        "selected_omega": fraction_summary(mismatch.omega),
        "omega_sweep": [
            {
                "omega": fraction_summary(result.omega),
                "augmented_inverse_upper_bound": fraction_summary(
                    result.augmented_inverse_upper_bound
                ),
                "interior_operator_mismatch_upper_bound": fraction_summary(
                    result.interior_operator_mismatch_upper_bound
                ),
                "z0_upper_bound": fraction_summary(result.z0_upper_bound),
            }
            for result in mismatches
        ],
        "newton_tube_skip_reason": (
            "requested_stop_after_mismatch"
            if args.stop_after_mismatch
            else (
                "z0_not_contracting"
                if mismatch.z0_upper_bound >= 1
                else (
                    "all_candidate_radii_pruned"
                    if best_tube is None
                    else (
                        "no_joint_newton_closure"
                        if not (
                            best_tube.self_map_verified
                            and best_tube.contraction_verified
                        )
                        else (
                            "physical_observables_not_certified"
                            if physical_observables is None
                            else None
                        )
                    )
                )
            )
        ),
        "physical_observable_failures": physical_failures,
        "newton_tube_minimum_linearized_radius": (
            None
            if mismatch.z0_upper_bound >= 1
            else fraction_summary(
                mismatch.newton_defect_upper_bound
                / (1 - mismatch.z0_upper_bound)
            )
        ),
        "newton_tube_best_radius": (
            fraction_summary(best_tube.radius) if best_tube is not None else None
        ),
        "newton_tube_interior_hessian": (
            fraction_summary(best_tube.interior_hessian_upper_bound)
            if best_tube is not None
            else None
        ),
        "newton_tube_schur_composed_hessian": (
            fraction_summary(best_tube.schur_composed_hessian_upper_bound)
            if best_tube is not None
            else None
        ),
        "newton_tube_interior_hessian_trace": (
            fraction_summary(best_tube.interior_hessian_trace_upper_bound)
            if best_tube is not None
            else None
        ),
        "newton_tube_radii_polynomial": (
            fraction_summary(best_tube.radii_polynomial_upper_bound)
            if best_tube is not None
            else None
        ),
        "newton_tube_contraction_bound": (
            fraction_summary(best_tube.contraction_upper_bound)
            if best_tube is not None
            else None
        ),
        "newton_tube_self_map_verified": (
            best_tube.self_map_verified if best_tube is not None else False
        ),
        "newton_tube_contraction_verified": (
            best_tube.contraction_verified if best_tube is not None else False
        ),
        "strict_monotonicity_verified": (
            physical_observables.strict_monotonicity_verified
            if physical_observables is not None
            else False
        ),
        "negative_wall_slope_verified": (
            physical_observables.negative_wall_slope_verified
            if physical_observables is not None
            else False
        ),
        "wall_slope_enclosure": (
            {
                "lower": fraction_summary(
                    physical_observables.wall_slope_enclosure.lower
                ),
                "upper": fraction_summary(
                    physical_observables.wall_slope_enclosure.upper
                ),
            }
            if physical_observables is not None
            else None
        ),
        "positive_finite_inertia_verified": (
            physical_observables.positive_finite_inertia_verified
            if physical_observables is not None
            else False
        ),
        "dimensionless_rotor_inertia_enclosure": (
            {
                "lower": fraction_summary(
                    physical_observables.inertia_enclosure.lower
                ),
                "upper": fraction_summary(
                    physical_observables.inertia_enclosure.upper
                ),
            }
            if physical_observables is not None
            else None
        ),
        "au2_positive_derivative_norm_status": (
            "positive_radius_certified"
            if positive_derivative_norms is not None
            else "not_evaluated"
        ),
        "au2_positive_w_l1_upper_bounds": (
            tuple(
                fraction_summary(value)
                for value in positive_derivative_norms.w_positive_l1_upper_bounds
            )
            if positive_derivative_norms is not None
            else None
        ),
        "au2_positive_a_l1_upper_bounds": (
            tuple(
                fraction_summary(value)
                for value in positive_derivative_norms.a_positive_l1_upper_bounds
            )
            if positive_derivative_norms is not None
            else None
        ),
        "au2_global_derivative_norms_certified": (
            global_derivative_norms.global_norms_certified
            if global_derivative_norms is not None
            else False
        ),
        "au2_global_w_l1_upper_bounds": (
            tuple(
                fraction_summary(value)
                for value in (
                    global_derivative_norms.w_third_derivative_l1_upper_bounds
                )
            )
            if global_derivative_norms is not None
            else None
        ),
        "au2_global_a_l1_upper_bounds": (
            tuple(
                fraction_summary(value)
                for value in (
                    global_derivative_norms.a_third_derivative_l1_upper_bounds
                )
            )
            if global_derivative_norms is not None
            else None
        ),
        "au2_tail_status": (
            global_derivative_norms.spectral_ledger.au2_status
            if global_derivative_norms is not None
            else "not_evaluated"
        ),
        "newton_tube_sweep": [
            {
                "omega": fraction_summary(result.omega),
                "radius": fraction_summary(result.radius),
                "interior_hessian": fraction_summary(
                    result.interior_hessian_upper_bound
                ),
                "interior_hessian_trace": fraction_summary(
                    result.interior_hessian_trace_upper_bound
                ),
                "scalar_hessian": fraction_summary(
                    result.scalar_hessian_upper_bound
                ),
                "schur_composed_hessian": fraction_summary(
                    result.schur_composed_hessian_upper_bound
                ),
                "joint_feasibility_margin": fraction_summary(
                    newton_tube_feasibility_margin(result)
                ),
                "radii_polynomial": fraction_summary(
                    result.radii_polynomial_upper_bound
                ),
                "contraction_bound": fraction_summary(
                    result.contraction_upper_bound
                ),
                "self_map_verified": result.self_map_verified,
                "contraction_verified": result.contraction_verified,
                "worst_hessian_source_cell": worst_tube_cells[
                    (result.omega, result.radius)
                ].source_cell_index,
                "worst_hessian_radius": [
                    float(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].radius.lower
                    ),
                    float(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].radius.upper
                    ),
                ],
                "worst_hessian_components": {
                    "local_graph_c0": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].local_graph_c0_upper_bound
                    ),
                    "local_graph_c1": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].local_graph_c1_upper_bound
                    ),
                    "local_graph_c2": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].local_graph_c2_upper_bound
                    ),
                    "local_auxiliary_c0": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].local_auxiliary_c0_upper_bound
                    ),
                    "local_auxiliary_c1": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].local_auxiliary_c1_upper_bound
                    ),
                    "local_auxiliary_c2": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].local_auxiliary_c2_upper_bound
                    ),
                    "nonlinear": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].nonlinear_hessian_upper_bound
                    ),
                    "direct_nonlinear": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].direct_nonlinear_hessian_upper_bound
                    ),
                    "center_equation": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].center_equation_hessian_upper_bound
                    ),
                    "center_equation_forcing": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].center_equation_forcing_upper_bound
                    ),
                    "affine_lift_jacobi": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].affine_lift_jacobi_upper_bound
                    ),
                    "augmented": fraction_summary(
                        worst_tube_cells[
                            (result.omega, result.radius)
                        ].interior_augmented_hessian_upper_bound
                    ),
                },
            }
            for result in tube_results
        ],
        "worst_mismatch_source_cell": worst.source_cell_index,
        "worst_mismatch_radius": [
            float(worst.radius.lower),
            float(worst.radius.upper),
        ],
        "worst_coefficient_differences": {
            "principal": fraction_summary(
                worst.principal_difference_upper_bound
            ),
            "principal_derivative": fraction_summary(
                worst.principal_derivative_difference_upper_bound
            ),
            "potential": fraction_summary(
                worst.potential_difference_upper_bound
            ),
        },
        "scope": (
            physical_observables.conclusion_scope
            if physical_observables is not None
            else (
                best_tube.conclusion_scope
                if best_tube is not None
                else mismatch.conclusion_scope
            )
        ),
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(rendered + "\n", encoding="ascii")
    print(rendered)


if __name__ == "__main__":
    main()
