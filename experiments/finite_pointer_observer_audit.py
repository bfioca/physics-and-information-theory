#!/usr/bin/env python3
"""Replay the finite-pointer observer-entropy four-gate algebra."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.finite_pointer_observer import (  # noqa: E402
    finite_pointer_observer_certificate,
)


DEFAULT_OUTPUT = ROOT / "experiments/finite_pointer_observer_certificate.json"
SPECTRUM = (
    ROOT
    / "paper"
    / "local_scalar_observer_cost"
    / "data"
    / "observer_cost_spectrum.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments" / "finite_pointer_observer_audit.py",
        ROOT / "qgtoy" / "finite_pointer_observer.py",
        ROOT / "qgtoy" / "local_scalar_observer_cost.py",
        SPECTRUM,
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _illustrative_cost_at_unit_support() -> float:
    record = json.loads(SPECTRUM.read_text(encoding="ascii"))
    matches = [
        float(row["galerkin_cost"])
        for row in record["curve"]
        if float(row["support_ratio_y"]) == 1.0
    ]
    if len(matches) != 1:
        raise ValueError("expected one y=1 spectrum row")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    starting_hashes = _source_hashes()
    record = finite_pointer_observer_certificate(
        illustrative_cost_coefficient=_illustrative_cost_at_unit_support(),
    )
    record["source_sha256"] = starting_hashes
    record["replay"] = {
        "unit_support_cost_source": str(SPECTRUM.relative_to(ROOT)),
        "unit_support_cost_status": "nonrigorous_numerical_illustration",
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("hashed observer-entropy source changed during replay")

    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    output = args.output.resolve()
    output.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "finite_pointer_purity_bound": record["finite_pointer_example"][
                    "renyi_bound"
                ]["purity_formula"],
                "harlow_gate_three_closed": record["harlow_code_insertion"][
                    "gate_three_closed"
                ],
                "illustrative_area_coefficient": record[
                    "branchwise_gravity_example"
                ]["dimensionless_area_coefficient"],
                "rigorous_area_coefficient_upper": record[
                    "branchwise_gravity_rigorous_bound"
                ]["dimensionless_area_coefficient"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
