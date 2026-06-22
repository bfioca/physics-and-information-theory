#!/usr/bin/env python3
"""Replay the local scalar observer-cost theorem candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.local_scalar_observer_cost import (  # noqa: E402
    local_scalar_observer_cost_certificate,
)


DEFAULT_OUTPUT = ROOT / "experiments/local_scalar_observer_cost_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/local_scalar_observer_cost_audit.py",
        ROOT / "qgtoy/local_scalar_observer_cost.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--observer-error", type=float, default=1.0e-6)
    parser.add_argument("--source-areal-radius", type=float, default=0.2)
    parser.add_argument("--switching-duration", type=float, default=0.1)
    parser.add_argument("--static-patch-radius", type=float, default=1.0)
    parser.add_argument("--newton-constant", type=float, default=1.0e-6)
    parser.add_argument("--maximum-constraint-ratio", type=float, default=0.25)
    args = parser.parse_args()

    starting_hashes = _source_hashes()
    record = local_scalar_observer_cost_certificate(
        observer_error=args.observer_error,
        source_areal_radius=args.source_areal_radius,
        switching_duration=args.switching_duration,
        static_patch_radius=args.static_patch_radius,
        newton_constant=args.newton_constant,
        maximum_constraint_ratio=args.maximum_constraint_ratio,
    )
    record["source_sha256"] = starting_hashes
    record["replay"] = {
        "observer_error": args.observer_error,
        "source_areal_radius": args.source_areal_radius,
        "switching_duration": args.switching_duration,
        "static_patch_radius": args.static_patch_radius,
        "newton_constant": args.newton_constant,
        "maximum_constraint_ratio": args.maximum_constraint_ratio,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("hashed observer-cost source changed during replay")

    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "exact_cost_formula": record["optimality_bracket"][
                    "sharp_characterization"
                ]["exact_optimal_coefficient_formula"],
                "explicit_C_upper": record["optimality_bracket"][
                    "uniform_upper_coefficient"
                ],
                "minimum_E_R": record["observer_cost_bound"][
                    "dimensionless_minimum_energy_E_R"
                ],
                "minimum_wall_q": record["observer_cost_bound"][
                    "minimum_wall_constraint_ratio_q"
                ],
                "explicit_weak_gravity_window": record["explicit_window"][
                    "target_has_certified_weak_gravity_window"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
