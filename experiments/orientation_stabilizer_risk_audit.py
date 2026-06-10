#!/usr/bin/env python3
"""Write the exact global orientation-stabilizer risk certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.orientation_stabilizer_risk import (  # noqa: E402
    orientation_stabilizer_risk_certificate,
)


OUTPUT = ROOT / "experiments/orientation_stabilizer_risk_exact_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/orientation_stabilizer_risk_audit.py",
        ROOT / "qgtoy/orientation_stabilizer_risk.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    record = orientation_stabilizer_risk_certificate()
    record["source_sha256"] = starting_hashes
    if _source_hashes() != starting_hashes:
        raise ValueError("orientation stabilizer sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "global_risk_floor": record["spin_two_anticoherent_example"][
                    "global_chordal_risk_lower_bound_exact"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
