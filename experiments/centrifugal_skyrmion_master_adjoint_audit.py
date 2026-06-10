#!/usr/bin/env python3
"""Write the floating centrifugal master primal-adjoint feasibility audit."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_master_adjoint import (  # noqa: E402
    centrifugal_master_adjoint_feasibility_record,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_master_adjoint_feasibility.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_master_adjoint.py",
    "qgtoy/centrifugal_skyrmion_variational.py",
    "qgtoy/centrifugal_skyrmion_completed_stress.py",
    "qgtoy/centrifugal_skyrmion_membrane_stress.py",
    "qgtoy/static_patch_l2_master_source.py",
    "qgtoy/static_patch_l2_response.py",
    "experiments/centrifugal_skyrmion_master_adjoint_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_record() -> dict[str, object]:
    before = {path: _sha256(ROOT / path) for path in SOURCES}
    record = centrifugal_master_adjoint_feasibility_record()
    after = {path: _sha256(ROOT / path) for path in SOURCES}
    if before != after:
        raise ValueError("master-adjoint sources changed during audit")
    return {**record, "source_sha256": before}


def main() -> None:
    payload = build_record()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
