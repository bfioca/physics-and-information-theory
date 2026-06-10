#!/usr/bin/env python3
"""Write the floating completed-stress conservation certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_completed_stress import (  # noqa: E402
    completed_stress_conservation_record,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_completed_stress_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_completed_stress_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_completed_stress.py",
        ROOT / "qgtoy/centrifugal_skyrmion_bvp.py",
        ROOT / "qgtoy/centrifugal_skyrmion_deformation.py",
        ROOT / "qgtoy/massive_skyrmion_profile.py",
        ROOT / "qgtoy/massive_skyrmion_worldtube.py",
        ROOT / "qgtoy/static_even_stress_conservation.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _summary(node_count: int) -> dict[str, float | int]:
    record = completed_stress_conservation_record(node_count=node_count)
    return {
        "node_count": node_count,
        "rigid_radial_residual_maximum": record["rigid_radial_residual_maximum"],
        "rigid_angular_residual_maximum": record["rigid_angular_residual_maximum"],
        "completed_radial_residual_maximum": record[
            "completed_radial_residual_maximum"
        ],
        "completed_angular_residual_maximum": record[
            "completed_angular_residual_maximum"
        ],
        "residual_reduction_factor": record["residual_reduction_factor"],
    }


def main() -> None:
    starting_hashes = _source_hashes()
    mesh_records = [_summary(count) for count in (101, 201, 401, 801)]
    radial_ratios = [
        fine["completed_radial_residual_maximum"]
        / coarse["completed_radial_residual_maximum"]
        for coarse, fine in zip(mesh_records[:-1], mesh_records[1:], strict=True)
    ]
    angular_ratios = [
        fine["completed_angular_residual_maximum"]
        / coarse["completed_angular_residual_maximum"]
        for coarse, fine in zip(mesh_records[:-1], mesh_records[1:], strict=True)
    ]
    finest = mesh_records[-1]
    claims = {
        "rigid_source_has_nonzero_bulk_residual": (
            finest["rigid_radial_residual_maximum"] > 1.0
            and finest["rigid_angular_residual_maximum"] > 0.1
        ),
        "same_action_deformation_reduces_bulk_residual": (
            finest["residual_reduction_factor"] < 1.0e-3
        ),
        "radial_residual_shows_second_order_decay": all(
            ratio < 0.35 for ratio in radial_ratios
        ),
        "angular_residual_shows_second_order_decay": all(
            ratio < 0.35 for ratio in angular_ratios
        ),
    }
    record = {
        "goal": "Same-Action Centrifugal Skyrmion Bulk Stress Closure",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "floating_bulk_conservation_mesh_closure",
        "mesh_records": mesh_records,
        "successive_radial_residual_ratios": radial_ratios,
        "successive_angular_residual_ratios": angular_ratios,
        "certified_claims": claims,
        "claim_boundary": (
            "Floating finite-difference evidence for smooth-bulk conservation "
            "on the default same-action centrifugal branch. It is not an "
            "interval proof and does not include the distributional membrane "
            "stress, Israel junction conditions, collective quantization, or "
            "a Zerilli master-source projection."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("completed-stress sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
