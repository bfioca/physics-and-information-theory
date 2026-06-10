#!/usr/bin/env python3
"""Authenticate the fixed-field spherical Skyrmion bulk lapse coefficient."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from math import exp
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.validated_skyrmion_lapse import (  # noqa: E402
    build_validated_skyrmion_lapse_coefficient,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SNAPSHOT = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
CONSTRAINT = ROOT / "experiments/skyrmion_spherical_constraint_exact_certificate.json"
OUTPUT = ROOT / "experiments/skyrmion_static_lapse_exact_certificate.json"
EXPECTED_AU2_SHA256 = (
    "1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9"
)
EXPECTED_SNAPSHOT_SHA256 = (
    "1781a2ff357f3b165d23e290eb403552d77d099a72b9e90920735e6a80b30431"
)
EXPECTED_CONSTRAINT_SHA256 = (
    "a180610fbdea4eecd75cdc7628216adab9289d5561704f60f750f7105fcaca47"
)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_source_hashes(record: Mapping[str, object]) -> dict[str, str]:
    hashes = record.get("source_sha256")
    if not isinstance(hashes, Mapping) or not hashes:
        raise ValueError("source hashes are missing")
    actual_hashes = {}
    for relative, expected in hashes.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise TypeError("source hashes must map strings to strings")
        actual = _sha256(ROOT / relative)
        if actual != expected:
            raise ValueError(f"source hash mismatch for {relative}")
        actual_hashes[relative] = actual
    return actual_hashes


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_static_lapse_audit.py",
        ROOT / "qgtoy/skyrmion_lapse_control.py",
        ROOT / "qgtoy/validated_skyrmion_lapse.py",
        ROOT / "qgtoy/validated_skyrmion_sharp_profile.py",
        ROOT / "qgtoy/validated_skyrmion_origin.py",
        ROOT / "qgtoy/validated_interval.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _ceil_fraction(value: Fraction, denominator: int) -> Fraction:
    scaled = value * denominator
    return Fraction(-((-scaled.numerator) // scaled.denominator), denominator)


def main() -> None:
    expected = (
        (AU2, EXPECTED_AU2_SHA256),
        (SNAPSHOT, EXPECTED_SNAPSHOT_SHA256),
        (CONSTRAINT, EXPECTED_CONSTRAINT_SHA256),
    )
    for path, digest in expected:
        actual = _sha256(path)
        if actual != digest:
            raise ValueError(f"authenticated input mismatch for {path.name}: {actual}")
    archive = json.loads(AU2.read_text(encoding="ascii"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="ascii"))
    constraint = json.loads(CONSTRAINT.read_text(encoding="ascii"))
    snapshot_hashes = _verify_source_hashes(snapshot)
    constraint_hashes = _verify_source_hashes(constraint)
    starting_hashes = _source_hashes()

    profile = reconstruct_validated_skyrmion_sharp_profile(
        archive,
        snapshot,
        subdivisions_per_parent=2,
    )
    origin = reconstruct_validated_skyrmion_sharp_origin_family(snapshot)
    lapse = build_validated_skyrmion_lapse_coefficient(
        profile,
        origin,
        origin_subdivisions=64,
    )
    denominator = 10**6
    lapse_upper = _ceil_fraction(lapse.coefficient.upper, denominator)
    radial_shape_exact = Fraction(
        constraint["constraint_shape"]["sufficient_bulk_shape_upper_exact"]
    )
    radial_shape_upper = _ceil_fraction(radial_shape_exact, denominator)
    beta = Fraction(1, 2)
    maximum_log_lapse_drop = beta * lapse_upper / radial_shape_upper
    minimum_gtt_ratio_diagnostic = float(1 - beta) * exp(
        -2.0 * float(maximum_log_lapse_drop)
    )
    record = {
        "goal": "Authenticated Static Skyrmion Bulk Lapse Control",
        "status": "complete_fixed_field_static_bulk_lapse_certificate",
        "result_type": "authenticated_spherical_static_lapse_bound",
        "source_sha256": starting_hashes,
        "authenticated_inputs": {
            "au2_sha256": EXPECTED_AU2_SHA256,
            "snapshot_sha256": EXPECTED_SNAPSHOT_SHA256,
            "spherical_constraint_sha256": EXPECTED_CONSTRAINT_SHA256,
            "snapshot_sources_rehashed": True,
            "constraint_sources_rehashed": True,
        },
        "replay": {
            "radial_subdivisions_per_parent": 2,
            "origin_subdivisions": 64,
            "positive_radius_cell_count": lapse.positive_radius_cell_count,
        },
        "directed_bounds": {
            "rounding_denominator": str(denominator),
            "lapse_coefficient_D_upper": str(lapse_upper),
            "lapse_coefficient_D_upper_float": float(lapse_upper),
            "radial_shape_H_upper": str(radial_shape_upper),
            "radial_shape_H_upper_float": float(radial_shape_upper),
            "radial_metric_budget_beta": str(beta),
            "maximum_log_lapse_drop_exact": str(maximum_log_lapse_drop),
            "maximum_log_lapse_drop_float": float(maximum_log_lapse_drop),
            "minimum_gtt_ratio_float_diagnostic": minimum_gtt_ratio_diagnostic,
        },
        "theorem": (
            "For the fixed static Skyrmion field, rho+p_r=A F'^2"
            "(1/4+2sin^2(F)/x^2), so A cancels from the spherical lapse equation. "
            "Under the sufficient alpha H<=beta radial constraint, the bulk log "
            "lapse drop is at most beta D/H."
        ),
        "claim_boundary": lapse.claim_boundary,
    }
    for path, digest in expected:
        if _sha256(path) != digest:
            raise ValueError(f"authenticated input changed during audit: {path.name}")
    if _verify_source_hashes(snapshot) != snapshot_hashes:
        raise ValueError("snapshot dependency changed during lapse audit")
    if _verify_source_hashes(constraint) != constraint_hashes:
        raise ValueError("constraint dependency changed during lapse audit")
    if _source_hashes() != starting_hashes:
        raise ValueError("lapse audit source changed during execution")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "lapse_coefficient_upper": float(lapse_upper),
                "maximum_log_lapse_drop": float(maximum_log_lapse_drop),
                "minimum_gtt_ratio_diagnostic": minimum_gtt_ratio_diagnostic,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
