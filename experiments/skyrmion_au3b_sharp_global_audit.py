#!/usr/bin/env python3
"""Authenticate and evaluate the sharp AU.3b radial/frequency certificate."""

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

from qgtoy.validated_skyrmion_au3b import (  # noqa: E402
    build_validated_skyrmion_au3b_sharp_certificate,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    build_validated_skyrmion_sharp_measure,
    build_validated_skyrmion_sharp_worldtube_constants,
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)
from qgtoy.validated_skyrmion_ule import (  # noqa: E402
    validated_centered_skyrmion_ule_heat_window,
)
from qgtoy.skyrmion_observer_capacity import (  # noqa: E402
    validated_fixed_profile_projective_capacity_record,
)


DEFAULT_AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
DEFAULT_SNAPSHOT = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
DEFAULT_OUTPUT = ROOT / "experiments/skyrmion_au3b_sharp_global_exact_certificate.json"
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


def _interval_record(value: object) -> dict[str, str]:
    return {"lower": str(value.lower), "upper": str(value.upper)}


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_au3b_sharp_global_audit.py",
        ROOT / "qgtoy/validated_skyrmion_au3b.py",
        ROOT / "qgtoy/validated_skyrmion_sharp_profile.py",
        ROOT / "qgtoy/validated_skyrmion_ule.py",
        ROOT / "qgtoy/skyrmion_observer_capacity.py",
        ROOT / "qgtoy/skyrmion_joint_scaling_no_go.py",
        ROOT / "qgtoy/global_so3_reference_risk.py",
        ROOT / "qgtoy/validated_skyrmion_au3.py",
        ROOT / "qgtoy/validated_skyrmion_spectral_ledger.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--au2", type=Path, default=DEFAULT_AU2)
    parser.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--radial-subdivisions", type=int, default=1)
    parser.add_argument("--origin-subdivisions", type=int, default=2)
    parser.add_argument("--band-split", type=int, default=64)
    parser.add_argument("--frequency-step", type=int, default=1)
    parser.add_argument("--frequency-workers", type=int, default=16)
    args = parser.parse_args()
    starting_audit_source_hashes = _source_hashes()

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
    starting_snapshot_source_hashes = _verify_source_hashes(snapshot)
    print("authenticated AU.2 and sharp snapshot inputs", flush=True)
    if snapshot.get("canonical_au2_sha256") != au2_sha:
        raise ValueError("sharp snapshot does not reference the pinned AU.2 archive")
    ledger_record = archive["exact_outputs"][
        "au2_global_derivative_norms_and_tail"
    ]["spectral_ledger"]
    profile = reconstruct_validated_skyrmion_sharp_profile(
        archive,
        snapshot,
        subdivisions_per_parent=args.radial_subdivisions,
    )
    print("reconstructed sharp profile", flush=True)
    origin = reconstruct_validated_skyrmion_sharp_origin_family(snapshot)
    measure = build_validated_skyrmion_sharp_measure(
        profile,
        origin,
        origin_subdivisions=args.origin_subdivisions,
    )
    print("certified directed inertia measure", flush=True)
    constants = build_validated_skyrmion_sharp_worldtube_constants(
        profile,
        origin,
        measure=measure,
        origin_subdivisions=args.origin_subdivisions,
    )
    print("certified directed worldtube constants", flush=True)
    certificate = build_validated_skyrmion_au3b_sharp_certificate(
        ledger_record,
        measure,
        band_split=args.band_split,
        frequency_step=args.frequency_step,
        parallel_frequency_workers=args.frequency_workers,
        authenticated_au2_sha256=au2_sha,
        authenticated_snapshot_sha256=snapshot_sha,
    )
    print("certified sharp finite band and AU.2 tail join", flush=True)
    record = certificate.to_record()
    capacity_record = validated_fixed_profile_projective_capacity_record(
        constants,
        maximum_compactness=Fraction(1, 2),
        maximum_slow_rotation=Fraction(1, 10),
        static_patch_radius_squared_over_newton=Fraction(10**6),
    )
    projective_cutoff = capacity_record["maximum_odd_reference_cutoff_J"]
    if not isinstance(projective_cutoff, int):
        raise ValueError("default directed observer-capacity sector is empty")
    projective_spin = Fraction(2 * projective_cutoff + 1, 2)
    projective_dimension = int(2 * projective_spin + 1)
    ule_upper_caps = {
        "constant_obstruction": validated_centered_skyrmion_ule_heat_window(
            certificate,
            spin=projective_spin,
            residual_budget=Fraction(1, 4 * projective_dimension),
            burnin_rate_multiples=Fraction(10),
        ),
        "heat_matching": validated_centered_skyrmion_ule_heat_window(
            certificate,
            spin=projective_spin,
            residual_budget=Fraction(1, 4 * projective_dimension**2),
            burnin_rate_multiples=Fraction(10),
        ),
    }
    record.update(
        {
            "au3b_status": "complete_entrypoint_authenticated_sharp_radial_upper_certificate",
            "result_type": "authenticated_skyrmion_au3b_sharp_global_certificate",
            "source_sha256": starting_audit_source_hashes,
            "profile": {
                "radial_subdivisions_per_parent": profile.subdivisions_per_parent,
                "positive_radius_cell_count": len(profile.cells),
                "origin_cell_count": len(measure.origin_cells),
                "sharp_inertia_enclosure": _interval_record(measure.inertia),
                "interior_mass_enclosure": _interval_record(
                    constants.interior_mass
                ),
                "shell_mass_enclosure": _interval_record(constants.shell_mass),
                "total_mass_enclosure": _interval_record(constants.total_mass),
                "worldtube_constants_claim_boundary": constants.claim_boundary,
            },
            "centered_prescribed_switch_ule_upper_caps": {
                "status": (
                    "normalized_upper_caps_only; no positive observation-"
                    "deadline or preparation-age coupling bound supplied"
                ),
                "positive_coupling_lower_bound_supplied": False,
                "caps": ule_upper_caps,
            },
            "conditional_fixed_profile_observer_capacity": capacity_record,
            "provenance": {
                "au2_archive": str(au2_path.relative_to(ROOT)),
                "au2_sha256": au2_sha,
                "sharp_snapshot": str(snapshot_path.relative_to(ROOT)),
                "sharp_snapshot_sha256": snapshot_sha,
                "snapshot_sources_rehashed": True,
            },
        }
    )
    if _sha256(au2_path) != au2_sha or _sha256(snapshot_path) != snapshot_sha:
        raise ValueError("authenticated input archive changed during global audit")
    if _source_hashes() != starting_audit_source_hashes:
        raise ValueError("hashed global-audit source changed during execution")
    if _verify_source_hashes(snapshot) != starting_snapshot_source_hashes:
        raise ValueError("snapshot dependency source changed during global audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "q_norm_upper_bounds": record["q_norm_upper_bounds"],
                "sharp_inertia_enclosure": record["profile"][
                    "sharp_inertia_enclosure"
                ],
                "total_mass_enclosure": record["profile"]["total_mass_enclosure"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
