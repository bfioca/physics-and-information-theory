#!/usr/bin/env python3
"""Write the exact centrifugal-origin indicial certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_origin import (  # noqa: E402
    centrifugal_origin_indicial_certificate,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_origin_certificate.json"
AUTHENTICATED_PROFILE = (
    ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_origin_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_origin.py",
        ROOT / "qgtoy/centrifugal_skyrmion_deformation.py",
        AUTHENTICATED_PROFILE,
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    record = centrifugal_origin_indicial_certificate()
    profile_snapshot = json.loads(AUTHENTICATED_PROFILE.read_text(encoding="ascii"))
    snapshot_slopes = profile_snapshot["sharp_profile_recipe"][
        "shooting_slope_interval"
    ]
    if snapshot_slopes != record["authenticated_slope_interval"]:
        raise ValueError("authenticated profile slope interval does not match")
    record["authenticated_profile_dependency"] = {
        "path": str(AUTHENTICATED_PROFILE.relative_to(ROOT)),
        "sha256": _sha256(AUTHENTICATED_PROFILE),
    }
    record["source_sha256"] = starting_hashes
    if _source_hashes() != starting_hashes:
        raise ValueError("centrifugal-origin sources changed during audit")
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
