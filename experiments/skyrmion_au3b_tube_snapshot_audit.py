#!/usr/bin/env python3
"""Capture AU.3b cell data without changing the canonical AU.2 archive.

The trusted AU.1/AU.2 audit builds exact Newton-tube physical observables but
does not serialize their cellwise inertia data.  This wrapper instruments that
unchanged audit, reruns the canonical command in a temporary directory, checks
that every mathematical output reproduces the pinned AU.2 archive exactly,
and writes a small companion snapshot for profile-resolving frequency bounds.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import experiments.skyrmion_newton_linearization_audit as au2_audit
from qgtoy.validated_interval import RationalInterval


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
DEFAULT_OUTPUT = ROOT / "experiments/skyrmion_au3b_tube_snapshot_exact.json"
EXPECTED_AU2_SHA256 = (
    "1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _interval(value: RationalInterval) -> dict[str, str]:
    return {"lower": str(value.lower), "upper": str(value.upper)}


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_au3b_tube_snapshot_audit.py",
        ROOT / "experiments/skyrmion_newton_linearization_audit.py",
        ROOT / "qgtoy/skyrmion_global_bvp_certificate_generator.py",
        ROOT / "qgtoy/validated_interval.py",
        ROOT / "qgtoy/validated_skyrmion_bvp.py",
        ROOT / "qgtoy/validated_skyrmion_origin.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _physical_snapshot(observables: object) -> dict[str, object]:
    tube = observables.newton_tube
    return {
        "omega": str(tube.omega),
        "newton_radius": str(tube.radius),
        "curvature": str(tube.curvature),
        "origin_cutoff": str(tube.origin_cutoff),
        "wall_radius": str(tube.wall_radius),
        "inertia_enclosure": _interval(observables.inertia_enclosure),
        "origin_inertia_upper_bound": str(
            observables.origin_inertia_upper_bound
        ),
        "origin_momentum_enclosure": _interval(
            observables.origin_momentum_enclosure
        ),
        "wall_slope_enclosure": _interval(observables.wall_slope_enclosure),
        "strict_monotonicity_verified": observables.strict_monotonicity_verified,
        "negative_wall_slope_verified": observables.negative_wall_slope_verified,
        "positive_finite_inertia_verified": (
            observables.positive_finite_inertia_verified
        ),
        "tube_cells": tuple(
            {
                "source_cell_index": cell.source_cell_index,
                "radius": _interval(cell.radius),
                "profile": _interval(cell.tube_jet.profile),
                "derivative": _interval(cell.tube_jet.derivative),
                "second_derivative": _interval(
                    cell.tube_jet.second_derivative
                ),
            }
            for cell in tube.cells
        ),
        "inertia_cells": tuple(
            {
                "source_cell_index": cell.source_cell_index,
                "radius": _interval(cell.radius),
                "sine_squared": _interval(cell.sine_squared),
                "density_enclosure": _interval(cell.density_enclosure),
                "integral_enclosure": _interval(cell.integral_enclosure),
            }
            for cell in observables.inertia_cells
        ),
        "conclusion_scope": observables.conclusion_scope,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical-au2", type=Path, default=CANONICAL_AU2)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    canonical_path = args.canonical_au2.resolve()
    canonical_sha = _sha256(canonical_path)
    if canonical_sha != EXPECTED_AU2_SHA256:
        raise ValueError(
            f"canonical AU.2 hash mismatch: {canonical_sha}"
        )
    canonical = json.loads(canonical_path.read_text(encoding="ascii"))

    captured: list[object] = []
    original_validator = au2_audit.validate_skyrmion_newton_physical_observables

    def capture(*validator_args: object, **validator_kwargs: object) -> object:
        result = original_validator(*validator_args, **validator_kwargs)
        captured.append(result)
        return result

    au2_audit.validate_skyrmion_newton_physical_observables = capture
    old_argv = sys.argv
    try:
        with TemporaryDirectory(prefix="skyrmion-au3b-") as temporary:
            temporary_root = Path(temporary)
            report_path = temporary_root / "audit.json"
            exact_path = temporary_root / "exact.json"
            sys.argv = [
                "experiments/skyrmion_newton_linearization_audit.py",
                "--omega",
                "3/4",
                "--tube-radius",
                "1/250",
                "--tube-trigonometric-terms",
                "12",
                "--tube-rounding-denominator",
                "1000000000000000000",
                "--spectral-trigonometric-terms",
                "24",
                "--spectral-atanh-terms",
                "80",
                "--spectral-pi-terms",
                "80",
                "--origin-kernel-terms",
                "20",
                "--output",
                str(report_path),
                "--exact-certificate-output",
                str(exact_path),
            ]
            au2_audit.main()
            reproduced = json.loads(exact_path.read_text(encoding="ascii"))
    finally:
        sys.argv = old_argv
        au2_audit.validate_skyrmion_newton_physical_observables = (
            original_validator
        )

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
    expected_outputs = canonical["exact_outputs"]
    selected = tuple(
        observables
        for observables in captured
        if _interval(observables.inertia_enclosure)
        == expected_outputs["inertia_enclosure"]
        and _interval(observables.wall_slope_enclosure)
        == expected_outputs["wall_slope_enclosure"]
    )
    if len(selected) != 1:
        raise ValueError(
            f"expected one reproduced physical observable, found {len(selected)}"
        )
    global_record = expected_outputs["au2_global_derivative_norms_and_tail"]
    record = {
        "result_type": "authenticated_skyrmion_au3b_tube_snapshot",
        "canonical_au2_archive": str(canonical_path.relative_to(ROOT)),
        "canonical_au2_sha256": canonical_sha,
        "certificate_id": global_record["certificate_id"],
        "canonical_mathematical_outputs_reproduced_exactly": True,
        "source_sha256": _source_hashes(),
        "physical_observables": _physical_snapshot(selected[0]),
        "claim_boundary": (
            "This snapshot authenticates cellwise Newton-tube and inertia "
            "enclosures for AU.3b. It does not itself evaluate a frequency "
            "integral or prove a reduced-dynamics approximation."
        ),
    }
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(json.dumps({
        "output": str(output),
        "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
        "tube_cell_count": len(record["physical_observables"]["tube_cells"]),
        "inertia_cell_count": len(
            record["physical_observables"]["inertia_cells"]
        ),
    }, indent=2))


if __name__ == "__main__":
    main()
