#!/usr/bin/env python3
"""Derive the conservative AU.3 certificate from the exact AU.2 archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from qgtoy.validated_skyrmion_au3 import (
    build_validated_skyrmion_au3_from_au2_record,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
DEFAULT_OUTPUT = (
    ROOT / "experiments/skyrmion_au3_global_sobolev_exact_certificate.json"
)
EXPECTED_AU2_SHA256 = (
    "1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "qgtoy/validated_interval.py",
        ROOT / "qgtoy/validated_skyrmion_spectral_ledger.py",
        ROOT / "qgtoy/validated_skyrmion_au3.py",
        ROOT / "experiments/skyrmion_au3_global_sobolev_audit.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def build_audit_record(input_path: Path) -> dict[str, object]:
    input_sha = _sha256(input_path)
    if input_sha != EXPECTED_AU2_SHA256:
        raise ValueError(
            "AU.2 archive hash mismatch: expected "
            f"{EXPECTED_AU2_SHA256}, received {input_sha}"
        )
    archive = json.loads(input_path.read_text(encoding="ascii"))
    try:
        ledger_record = archive["exact_outputs"][
            "au2_global_derivative_norms_and_tail"
        ]["spectral_ledger"]
    except (KeyError, TypeError) as error:
        raise ValueError("input archive does not contain the completed AU.2 ledger") from error
    certificate = build_validated_skyrmion_au3_from_au2_record(
        ledger_record,
        authenticated_input_sha256=input_sha,
    )
    result = certificate.to_record()
    numerical_candidates = (
        62.2644668852,
        2.16015691289,
        0.168156611337,
    )
    rigorous = result["q_norm_upper_bounds"]
    conditioning = {
        "finite_window_candidate_q_norms": numerical_candidates,
        "rigorous_to_candidate_q_ratios": tuple(
            bound / candidate
            for bound, candidate in zip(rigorous, numerical_candidates)
        ),
        "interpretation": (
            "The exact certificate proves finiteness, but the AU.2 global "
            "derivative envelope loses many orders of magnitude. Directed "
            "finite-frequency quadrature is required before using these "
            "constants to decide a physical parameter window."
        ),
    }
    return {
        "result_type": "trusted_skyrmion_au3_global_sobolev_audit",
        "input_archive": str(input_path.relative_to(ROOT)),
        "input_archive_sha256": input_sha,
        "source_sha256": _source_hashes(),
        "exact_outputs": result,
        "conditioning_diagnostic": conditioning,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    record = build_audit_record(args.input.resolve())
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    args.output.resolve().write_text(rendered, encoding="ascii")
    print(json.dumps({
        "output": str(args.output.resolve()),
        "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
        "q_norm_upper_bounds": record["exact_outputs"]["q_norm_upper_bounds"],
        "jump_l1_upper_bound": record["exact_outputs"]["jump_l1_upper_bound"],
        "jump_first_moment_upper_bound": record["exact_outputs"][
            "jump_first_moment_upper_bound"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
