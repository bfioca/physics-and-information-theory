#!/usr/bin/env python3
"""Replay AU.2 and archive the local Newton recipe needed by sharp AU.3b."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import experiments.skyrmion_newton_linearization_audit as au2_audit  # noqa: E402
from qgtoy.validated_interval import RationalInterval  # noqa: E402


CANONICAL_AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
DEFAULT_OUTPUT = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
EXPECTED_AU2_SHA256 = (
    "1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9"
)
ROUNDING_DENOMINATOR = 10**18


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _interval(value: RationalInterval) -> dict[str, str]:
    return {"lower": str(value.lower), "upper": str(value.upper)}


def _ceil_fraction(value: Fraction, denominator: int) -> Fraction:
    scaled = value * denominator
    numerator = -((-scaled.numerator) // scaled.denominator)
    return Fraction(numerator, denominator)


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_au3b_sharp_snapshot_audit.py",
        ROOT / "experiments/skyrmion_newton_linearization_audit.py",
        ROOT / "qgtoy/skyrmion_global_bvp_certificate_generator.py",
        ROOT / "qgtoy/validated_interval.py",
        ROOT / "qgtoy/validated_skyrmion_bvp.py",
        ROOT / "qgtoy/validated_skyrmion_origin.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _sharp_snapshot(observables: object, endpoint: object) -> dict[str, object]:
    tube = observables.newton_tube
    origin = observables.origin_family
    domain_length = tube.wall_radius - tube.origin_cutoff
    cells = []
    if len(tube.cells) != len(endpoint.cells):
        raise ValueError("Newton and endpoint cell counts differ")
    for tube_cell, endpoint_cell in zip(tube.cells, endpoint.cells):
        if (
            tube_cell.source_cell_index != endpoint_cell.source_cell_index
            or tube_cell.radius != endpoint_cell.radius
        ):
            raise ValueError("Newton and endpoint cells are misaligned")
        base_c0 = (
            tube_cell.local_graph_c0_upper_bound
            + tube_cell.local_auxiliary_c0_upper_bound / tube.omega
        )
        base_c1 = (
            tube_cell.local_graph_c1_upper_bound
            + tube_cell.local_auxiliary_c1_upper_bound / tube.omega
        )
        base_c2 = (
            tube_cell.local_graph_c2_upper_bound
            + tube_cell.local_auxiliary_c2_upper_bound / tube.omega
        )
        delta0 = _ceil_fraction(
            base_c0 * tube.radius
            + tube.profile_second_sensitivity_upper_bound
            * tube.radius**2
            / (2 * tube.omega**2),
            ROUNDING_DENOMINATOR,
        )
        delta1 = _ceil_fraction(
            base_c1 * tube.radius
            + tube.profile_second_sensitivity_upper_bound
            * tube.radius**2
            / (2 * domain_length * tube.omega**2),
            ROUNDING_DENOMINATOR,
        )
        delta2 = _ceil_fraction(
            base_c2 * tube.radius,
            ROUNDING_DENOMINATOR,
        )
        expected = endpoint_cell.family_profile_jet
        if not (
            (expected.profile + RationalInterval(-delta0, delta0)).is_subset_of(
                tube_cell.tube_jet.profile
            )
            and (
                expected.derivative + RationalInterval(-delta1, delta1)
            ).is_subset_of(tube_cell.tube_jet.derivative)
            and (
                expected.second_derivative + RationalInterval(-delta2, delta2)
            ).is_subset_of(tube_cell.tube_jet.second_derivative)
        ):
            raise ValueError("recomputed local Newton radius misses archived tube")
        cells.append(
            {
                "source_cell_index": tube_cell.source_cell_index,
                "radius": _interval(tube_cell.radius),
                "endpoint_family_profile": _interval(expected.profile),
                "endpoint_family_derivative": _interval(expected.derivative),
                "endpoint_family_second_derivative": _interval(
                    expected.second_derivative
                ),
                "profile_error_radius": str(delta0),
                "derivative_error_radius": str(delta1),
                "second_derivative_error_radius": str(delta2),
                "local_graph_c0_upper_bound": str(
                    tube_cell.local_graph_c0_upper_bound
                ),
                "local_graph_c1_upper_bound": str(
                    tube_cell.local_graph_c1_upper_bound
                ),
                "local_graph_c2_upper_bound": str(
                    tube_cell.local_graph_c2_upper_bound
                ),
                "local_auxiliary_c0_upper_bound": str(
                    tube_cell.local_auxiliary_c0_upper_bound
                ),
                "local_auxiliary_c1_upper_bound": str(
                    tube_cell.local_auxiliary_c1_upper_bound
                ),
                "local_auxiliary_c2_upper_bound": str(
                    tube_cell.local_auxiliary_c2_upper_bound
                ),
                "archived_tube_profile": _interval(tube_cell.tube_jet.profile),
                "archived_tube_derivative": _interval(
                    tube_cell.tube_jet.derivative
                ),
                "archived_tube_second_derivative": _interval(
                    tube_cell.tube_jet.second_derivative
                ),
            }
        )
    return {
        "omega": str(tube.omega),
        "newton_radius": str(tube.radius),
        "rounding_denominator": str(ROUNDING_DENOMINATOR),
        "curvature": str(tube.curvature),
        "pion_mass_squared": str(tube.pion_mass_squared),
        "origin_cutoff": str(tube.origin_cutoff),
        "wall_radius": str(tube.wall_radius),
        "origin_remainder_radius": str(tube.origin_remainder_radius),
        "shooting_slope_interval": _interval(tube.shooting_slope_interval),
        "profile_second_sensitivity_upper_bound": str(
            tube.profile_second_sensitivity_upper_bound
        ),
        "left_value_correction": _interval(endpoint.left_value_correction),
        "right_value_correction": str(endpoint.right_value_correction),
        "origin_family": {
            "shooting_slopes": _interval(origin.shooting_slopes),
            "cutoff": str(origin.cutoff),
            "pion_mass_squared": str(origin.pion_mass_squared),
            "curvature": str(origin.curvature),
            "cubic_coefficient": _interval(origin.cubic_coefficient),
            "remainder_radius": str(origin.remainder_radius),
            "residual_bound": str(origin.residual_bound),
            "contraction_bound": str(origin.contraction_bound),
            "volterra_denominator_lower_bound": str(
                origin.volterra_denominator_lower_bound
            ),
            "profile_at_cutoff": _interval(origin.profile_at_cutoff),
            "derivative_at_cutoff": _interval(origin.derivative_at_cutoff),
        },
        "cells": tuple(cells),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-au2", type=Path, default=CANONICAL_AU2)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    canonical_path = args.canonical_au2.resolve()
    canonical_sha = _sha256(canonical_path)
    if canonical_sha != EXPECTED_AU2_SHA256:
        raise ValueError(f"canonical AU.2 hash mismatch: {canonical_sha}")
    canonical = json.loads(canonical_path.read_text(encoding="ascii"))
    starting_source_hashes = _source_hashes()

    endpoint_by_tube: dict[int, object] = {}
    physical_results: list[object] = []
    original_tube = au2_audit.validate_skyrmion_augmented_newton_tube
    original_physical = au2_audit.validate_skyrmion_newton_physical_observables

    def capture_tube(*call_args: object, **call_kwargs: object) -> object:
        result = original_tube(*call_args, **call_kwargs)
        endpoint_by_tube[id(result)] = call_args[1]
        return result

    def capture_physical(*call_args: object, **call_kwargs: object) -> object:
        result = original_physical(*call_args, **call_kwargs)
        physical_results.append(result)
        return result

    au2_audit.validate_skyrmion_augmented_newton_tube = capture_tube
    au2_audit.validate_skyrmion_newton_physical_observables = capture_physical
    old_argv = sys.argv
    try:
        with TemporaryDirectory(prefix="skyrmion-au3b-sharp-") as temporary:
            temporary_root = Path(temporary)
            exact_path = temporary_root / "exact.json"
            sys.argv = [
                "experiments/skyrmion_newton_linearization_audit.py",
                "--omega", "3/4",
                "--tube-radius", "1/250",
                "--tube-trigonometric-terms", "12",
                "--tube-rounding-denominator", str(ROUNDING_DENOMINATOR),
                "--spectral-trigonometric-terms", "24",
                "--spectral-atanh-terms", "80",
                "--spectral-pi-terms", "80",
                "--origin-kernel-terms", "20",
                "--exact-certificate-output", str(exact_path),
            ]
            au2_audit.main()
            reproduced = json.loads(exact_path.read_text(encoding="ascii"))
    finally:
        sys.argv = old_argv
        au2_audit.validate_skyrmion_augmented_newton_tube = original_tube
        au2_audit.validate_skyrmion_newton_physical_observables = original_physical

    for key in (
        "parameters",
        "profile_cells",
        "auxiliary_cells",
        "fundamental_cells",
        "representer_cells",
        "exact_outputs",
    ):
        if reproduced[key] != canonical[key]:
            raise ValueError(f"canonical AU.2 reproduction mismatch in {key}")
    expected = canonical["exact_outputs"]
    selected = tuple(
        result
        for result in physical_results
        if _interval(result.inertia_enclosure) == expected["inertia_enclosure"]
        and _interval(result.wall_slope_enclosure) == expected["wall_slope_enclosure"]
    )
    if len(selected) != 1:
        raise ValueError(f"expected one canonical physical result, found {len(selected)}")
    observables = selected[0]
    endpoint = endpoint_by_tube.get(id(observables.newton_tube))
    if endpoint is None:
        raise ValueError("selected Newton tube has no captured endpoint proof")
    global_record = expected["au2_global_derivative_norms_and_tail"]
    record = {
        "result_type": "authenticated_skyrmion_au3b_sharp_tube_snapshot",
        "canonical_au2_archive": str(canonical_path.relative_to(ROOT)),
        "canonical_au2_sha256": canonical_sha,
        "certificate_id": global_record["certificate_id"],
        "canonical_mathematical_outputs_reproduced_exactly": True,
        "source_sha256": starting_source_hashes,
        "sharp_profile_recipe": _sharp_snapshot(observables, endpoint),
        "claim_boundary": (
            "This exact snapshot authenticates the endpoint-corrected spline, "
            "origin family, and local Newton radii needed for sharp radial "
            "replay. It does not itself certify a frequency integral."
        ),
    }
    if _sha256(canonical_path) != canonical_sha:
        raise ValueError("canonical AU.2 archive changed during sharp replay")
    if _source_hashes() != starting_source_hashes:
        raise ValueError("hashed sharp-snapshot source changed during execution")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "sharp_cell_count": len(record["sharp_profile_recipe"]["cells"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
