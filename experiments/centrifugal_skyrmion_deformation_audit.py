#!/usr/bin/env python3
"""Write the centrifugal Skyrmion deformation and wall certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_deformation import (  # noqa: E402
    centrifugal_deformation_kinematics_certificate,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_deformation_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_deformation_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_deformation.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    record = centrifugal_deformation_kinematics_certificate()
    record["source_sha256"] = starting_hashes
    if _source_hashes() != starting_hashes:
        raise ValueError("centrifugal deformation sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "result_type": record["result_type"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
