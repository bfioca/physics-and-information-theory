#!/usr/bin/env python3
"""Authenticate the local spherical-constraint replay of the Skyrmion source."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.validated_skyrmion_constraint import (  # noqa: E402
    build_validated_skyrmion_constraint_shape,
    validated_constraint_coupling_record,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)


DEFAULT_AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
DEFAULT_SNAPSHOT = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
DEFAULT_OUTPUT = ROOT / "experiments/skyrmion_spherical_constraint_exact_certificate.json"
EXPECTED_AU2_SHA256 = (
    "1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9"
)
EXPECTED_SHARP_SNAPSHOT_SHA256 = (
    "1781a2ff357f3b165d23e290eb403552d77d099a72b9e90920735e6a80b30431"
)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_source_hashes(record: Mapping[str, object]) -> dict[str, str]:
    hashes = record.get("source_sha256")
    if not isinstance(hashes, Mapping) or not hashes:
        raise ValueError("snapshot source hashes are missing")
    actual_hashes = {}
    for relative, expected in hashes.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise TypeError("snapshot source hashes must map strings to strings")
        actual = _sha256(ROOT / relative)
        if actual != expected:
            raise ValueError(f"snapshot source hash mismatch for {relative}")
        actual_hashes[relative] = actual
    return actual_hashes


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_spherical_constraint_audit.py",
        ROOT / "qgtoy/spherical_static_patch_constraint.py",
        ROOT / "qgtoy/validated_skyrmion_constraint.py",
        ROOT / "qgtoy/validated_skyrmion_sharp_profile.py",
        ROOT / "qgtoy/validated_skyrmion_origin.py",
        ROOT / "qgtoy/validated_interval.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--au2", type=Path, default=DEFAULT_AU2)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--radial-subdivisions", type=int, default=2)
    parser.add_argument("--origin-subdivisions", type=int, default=64)
    args = parser.parse_args()

    au2_path = args.au2.resolve()
    snapshot_path = args.snapshot.resolve()
    au2_sha = _sha256(au2_path)
    snapshot_sha = _sha256(snapshot_path)
    if au2_sha != EXPECTED_AU2_SHA256:
        raise ValueError(f"AU.2 archive hash mismatch: {au2_sha}")
    if snapshot_sha != EXPECTED_SHARP_SNAPSHOT_SHA256:
        raise ValueError(f"sharp snapshot hash mismatch: {snapshot_sha}")
    archive = json.loads(au2_path.read_text(encoding="ascii"))
    snapshot = json.loads(snapshot_path.read_text(encoding="ascii"))
    snapshot_source_hashes = _verify_source_hashes(snapshot)
    if snapshot.get("canonical_au2_sha256") != au2_sha:
        raise ValueError("sharp snapshot does not reference the pinned AU.2 archive")
    starting_source_hashes = _source_hashes()

    profile = reconstruct_validated_skyrmion_sharp_profile(
        archive,
        snapshot,
        subdivisions_per_parent=args.radial_subdivisions,
    )
    origin = reconstruct_validated_skyrmion_sharp_origin_family(snapshot)
    shape = build_validated_skyrmion_constraint_shape(
        profile,
        origin,
        origin_subdivisions=args.origin_subdivisions,
    )
    coupling = validated_constraint_coupling_record(
        shape,
        control_budget=Fraction(1, 2),
        static_patch_radius_squared_over_newton=Fraction(10**6),
    )
    record = {
        "goal": "Authenticated Skyrmion Spherical Hamiltonian-Constraint Margin",
        "status": "complete_directed_bulk_supersolution_certificate",
        "result_type": "authenticated_local_mass_function_constraint_bound",
        "source_sha256": starting_source_hashes,
        "authenticated_inputs": {
            "au2_archive": str(au2_path.relative_to(ROOT)),
            "au2_sha256": au2_sha,
            "sharp_snapshot": str(snapshot_path.relative_to(ROOT)),
            "sharp_snapshot_sha256": snapshot_sha,
            "snapshot_sources_rehashed": True,
        },
        "replay": {
            "radial_subdivisions_per_parent": args.radial_subdivisions,
            "origin_subdivisions": args.origin_subdivisions,
        },
        "constraint_shape": shape.to_record(),
        "default_coupling_window": coupling,
        "bulk_bootstrap_theorem": (
            "With the certified field F(x) held fixed, replacing the background "
            "factor N by A=N-alpha*c/x makes the bulk mass equation linear: its "
            "gradient contribution is no larger than the fixed-background one "
            "while A is nonnegative. The certified fixed-background cumulative "
            "mass is therefore a supersolution. If alpha*H_bulk_upper<1, a first "
            "zero of A is impossible and the spherical radial constraint closes."
        ),
        "claim_boundary": (
            "This certifies the spherical Hamiltonian mass equation and radial "
            "metric for the fixed authenticated field configuration. It does not "
            "solve the self-gravitating Skyrme field equation or lapse equation. "
            "The membrane entries are fixed-background test-source diagnostics, "
            "not an Israel-junction solution. Rotation, nonspherical modes, and "
            "off-center support remain outside the certificate."
        ),
    }
    if _sha256(au2_path) != au2_sha or _sha256(snapshot_path) != snapshot_sha:
        raise ValueError("authenticated input changed during constraint audit")
    if _source_hashes() != starting_source_hashes:
        raise ValueError("hashed constraint-audit source changed during execution")
    if _verify_source_hashes(snapshot) != snapshot_source_hashes:
        raise ValueError("snapshot dependency source changed during constraint audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "bulk_shape_upper": shape.to_record()[
                    "sufficient_bulk_shape_upper_float"
                ],
                "test_source_global_shape_upper": shape.to_record()[
                    "sufficient_test_source_global_shape_upper_float"
                ],
                "fixed_background_exterior_shape_lower": shape.to_record()[
                    "fixed_background_exterior_shape_lower_float"
                ],
                "maximum_upper_region": shape.maximum_upper_region,
                "maximum_upper_source_cell_index": (
                    shape.maximum_upper_source_cell_index
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
