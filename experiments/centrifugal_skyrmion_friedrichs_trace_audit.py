#!/usr/bin/env python3
"""Write the source-hashed local Friedrichs-admissibility certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_friedrichs_trace import (  # noqa: E402
    centrifugal_friedrichs_origin_trace_certificate,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_friedrichs_trace_certificate.json"
PHYSICAL_TRANSFER = (
    ROOT / "experiments/validated_centrifugal_physical_origin_transfer_certificate.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_friedrichs_trace_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_friedrichs_trace.py",
        ROOT / "qgtoy/centrifugal_skyrmion_origin.py",
        ROOT / "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
        ROOT / "qgtoy/validated_centrifugal_physical_origin_transfer.py",
        PHYSICAL_TRANSFER,
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def main() -> None:
    starting_hashes = _source_hashes()
    theorem = centrifugal_friedrichs_origin_trace_certificate()
    physical = json.loads(PHYSICAL_TRANSFER.read_text(encoding="ascii"))
    branch_checks = theorem["branch_checks"]
    checks = {
        "all_indicial_modes_solve_leading_pencil": all(
            branch_checks[power]["indicial_residual_vanishes"]
            for power in (1, 3, -2, -4)
        ),
        "all_branch_leading_energies_strictly_positive": all(
            branch_checks[power]["leading_energy_positive_for_every_real_slope"]
            for power in (1, 3, -2, -4)
        ),
        "exact_finite_energy_classification": (
            theorem["finite_energy_homogeneous_powers"] == (1, 3)
            and theorem["excluded_singular_powers"] == (-2, -4)
            and theorem["homogeneous_solution_trace_dimension"] == 2
        ),
        "forced_cubic_column_is_finite_energy": theorem[
            "forced_affine_column_is_finite_energy"
        ],
        "physical_endpoint_columns_are_certified": (
            physical["status"] == "pass"
            and physical["branch_order"]
            == [
                "linear_homogeneous",
                "cubic_homogeneous",
                "forced_particular",
            ]
        ),
    }
    if not all(checks.values()):
        raise ValueError("local Friedrichs-admissibility audit failed")

    record = {
        **theorem,
        "status": "pass",
        "executable_checks": checks,
        "validated_physical_transfer_dependency": {
            "path": str(PHYSICAL_TRANSFER.relative_to(ROOT)),
            "sha256": _sha256(PHYSICAL_TRANSFER),
        },
        "claim_boundary": theorem["scope"],
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("Friedrichs-trace sources changed during audit")
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
