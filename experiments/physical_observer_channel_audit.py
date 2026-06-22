#!/usr/bin/env python3
"""Replay the finite physical observer-channel and ER=EPR gate audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from math import pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.physical_observer_channel import (  # noqa: E402
    physical_observer_channel_certificate,
)


DEFAULT_OUTPUT = ROOT / "experiments/physical_observer_channel_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/physical_observer_channel_audit.py",
        ROOT / "qgtoy/physical_observer_channel.py",
        ROOT / "qgtoy/spherical_static_patch_constraint.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--environment-qubits", type=int, default=4)
    parser.add_argument("--acquisition-coupling", type=float, default=1.0)
    parser.add_argument("--environment-coupling", type=float, default=1.0)
    parser.add_argument("--environment-phase", type=float, default=pi / 3.0)
    parser.add_argument("--support-radius", type=float, default=0.2)
    parser.add_argument("--static-patch-radius", type=float, default=1.0)
    parser.add_argument("--newton-constant", type=float, default=0.001)
    parser.add_argument("--backreaction-budget", type=float, default=0.25)
    args = parser.parse_args()

    starting_hashes = _source_hashes()
    record = physical_observer_channel_certificate(
        environment_qubits=args.environment_qubits,
        acquisition_coupling=args.acquisition_coupling,
        environment_coupling=args.environment_coupling,
        environment_phase=args.environment_phase,
        support_radius=args.support_radius,
        static_patch_radius=args.static_patch_radius,
        newton_constant=args.newton_constant,
        backreaction_control_budget=args.backreaction_budget,
    )
    record["source_sha256"] = starting_hashes
    record["replay"] = {
        "environment_qubits": args.environment_qubits,
        "acquisition_coupling": args.acquisition_coupling,
        "environment_coupling": args.environment_coupling,
        "environment_phase": args.environment_phase,
        "support_radius": args.support_radius,
        "static_patch_radius": args.static_patch_radius,
        "newton_constant": args.newton_constant,
        "backreaction_budget": args.backreaction_budget,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("hashed observer-channel source changed during replay")

    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "normalized_diamond_distance": record["channel"][
                    "normalized_diamond_distance"
                ],
                "maximum_constraint_ratio": record[
                    "localization_and_backreaction_ledger"
                ]["maximum_constraint_ratio_q"],
                "observer_channel_decision": record["decision"][
                    "observer_channel_theorem"
                ],
                "er_epr_decision": record["decision"]["er_epr_extension"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
