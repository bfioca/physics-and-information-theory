#!/usr/bin/env python3
"""Write the source-hashed first Frobenius-recurrence certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_frobenius import (  # noqa: E402
    centrifugal_skyrmion_first_frobenius_recurrence_certificate,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_frobenius_certificate.json"
AUTHENTICATED_PROFILE = (
    ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_frobenius_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_frobenius.py",
        ROOT / "qgtoy/centrifugal_skyrmion_transformed_origin.py",
        ROOT / "qgtoy/validated_skyrmion_origin.py",
        AUTHENTICATED_PROFILE,
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    record = centrifugal_skyrmion_first_frobenius_recurrence_certificate()
    snapshot = json.loads(AUTHENTICATED_PROFILE.read_text(encoding="ascii"))
    slope_box = snapshot["sharp_profile_recipe"]["shooting_slope_interval"]
    reference = Fraction(record["reference_slope"])
    if not Fraction(slope_box["lower"]) <= reference <= Fraction(slope_box["upper"]):
        raise ValueError("reference slope lies outside the authenticated profile box")
    record["authenticated_profile_dependency"] = {
        "path": str(AUTHENTICATED_PROFILE.relative_to(ROOT)),
        "sha256": _sha256(AUTHENTICATED_PROFILE),
        "shooting_slope_interval": slope_box,
        "reference_slope_is_inside": True,
    }
    record["source_sha256"] = starting_hashes
    if _source_hashes() != starting_hashes:
        raise ValueError("Frobenius-recurrence sources changed during audit")
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
