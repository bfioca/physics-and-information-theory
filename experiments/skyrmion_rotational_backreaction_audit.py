#!/usr/bin/env python3
"""Authenticate the spherical collective gravity-to-risk elimination."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.spherical_rotational_backreaction import (  # noqa: E402
    collective_rotational_backreaction_record,
)


INPUT = ROOT / "experiments/skyrmion_au3b_sharp_global_exact_certificate.json"
OUTPUT = ROOT / "experiments/skyrmion_rotational_backreaction_exact_certificate.json"
EXPECTED_INPUT_SHA256 = (
    "bc6cf2ea21f44c122001fcc3f7fa6cffb9983d4ec4e35591323aa2d29b25c529"
)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest()


def _verify_source_hashes(record: Mapping[str, object]) -> dict[str, str]:
    hashes = record.get("source_sha256")
    if not isinstance(hashes, Mapping) or not hashes:
        raise ValueError("input source hashes are missing")
    actual_hashes = {}
    for relative, expected in hashes.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise TypeError("input source hashes must map strings to strings")
        actual = _sha256(ROOT / relative)
        if actual != expected:
            raise ValueError(f"input source hash mismatch for {relative}")
        actual_hashes[relative] = actual
    return actual_hashes


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_rotational_backreaction_audit.py",
        ROOT / "qgtoy/spherical_rotational_backreaction.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _floor_fraction(value: Fraction, denominator: int) -> Fraction:
    return Fraction((value * denominator).numerator // (value * denominator).denominator, denominator)


def _ceil_fraction(value: Fraction, denominator: int) -> Fraction:
    scaled = value * denominator
    return Fraction(-((-scaled.numerator) // scaled.denominator), denominator)


def main() -> None:
    input_sha = _sha256(INPUT)
    if input_sha != EXPECTED_INPUT_SHA256:
        raise ValueError(f"AU.3b artifact hash mismatch: {input_sha}")
    source = json.loads(INPUT.read_text(encoding="ascii"))
    input_source_hashes = _verify_source_hashes(source)
    starting_source_hashes = _source_hashes()

    mass_text = source["profile"]["interior_mass_enclosure"]["lower"]
    inertia_text = source["profile"]["sharp_inertia_enclosure"]["upper"]
    if not isinstance(mass_text, str) or not isinstance(inertia_text, str):
        raise TypeError("authenticated mass and inertia endpoints must be strings")
    mass_exact = Fraction(mass_text)
    inertia_exact = Fraction(inertia_text)
    denominator = 10**6
    mass_lower = _floor_fraction(mass_exact, denominator)
    inertia_upper = _ceil_fraction(inertia_exact, denominator)
    if mass_lower > mass_exact or inertia_upper < inertia_exact:
        raise AssertionError("directed decimal compression failed")

    result = collective_rotational_backreaction_record(
        metric_budget=Fraction(1, 2),
        wall_radius=Fraction(4),
        curvature=Fraction(1, 400),
        static_patch_radius_squared_over_newton=Fraction(10**6),
        static_mass_lower=mass_lower,
        inertia_upper=inertia_upper,
    )
    record = {
        "goal": "Authenticated Spherical Collective Gravity-To-Risk Bound",
        "status": "complete_conditional_collective_backreaction_certificate",
        "result_type": "authenticated_spherical_collective_casimir_risk_bound",
        "source_sha256": starting_source_hashes,
        "authenticated_input": {
            "path": str(INPUT.relative_to(ROOT)),
            "sha256": input_sha,
            "input_sources_rehashed": True,
            "interior_mass_lower_text_sha256": _text_sha256(mass_text),
            "inertia_upper_text_sha256": _text_sha256(inertia_text),
        },
        "directed_decimal_compression": {
            "denominator": str(denominator),
            "static_bulk_mass_lower": str(mass_lower),
            "static_bulk_mass_lower_float": float(mass_lower),
            "bulk_inertia_upper": str(inertia_upper),
            "bulk_inertia_upper_float": float(inertia_upper),
        },
        "theorem_result": result,
        "derivation": (
            "q<=beta implies A>=(1-beta)N. For the certified field held fixed, "
            "c_M[A]>=(1-beta)c_M[N] and c_I[A]<=c_I[N]/(1-beta). "
            "The wall constraint therefore contains positive e^-2 rest and "
            "e^2 Cbar rotational terms. AM-GM eliminates e."
        ),
        "claim_boundary": result["claim_boundary"],
    }
    if _sha256(INPUT) != input_sha:
        raise ValueError("authenticated AU.3b input changed during audit")
    if _verify_source_hashes(source) != input_source_hashes:
        raise ValueError("AU.3b dependency source changed during audit")
    if _source_hashes() != starting_source_hashes:
        raise ValueError("rotational audit source changed during execution")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "static_bulk_mass_lower": float(mass_lower),
                "bulk_inertia_upper": float(inertia_upper),
                "maximum_mean_casimir": result["maximum_mean_casimir_float"],
                "global_orientation_risk_lower_bound": result[
                    "global_orientation_risk_lower_bound_float"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
