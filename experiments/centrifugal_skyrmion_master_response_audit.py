#!/usr/bin/env python3
"""Write the completed Skyrmion quadrupole master-response certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_master_response import (  # noqa: E402
    centrifugal_skyrmion_master_response_record,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_master_response_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_master_response_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_master_response.py",
        ROOT / "qgtoy/static_patch_l2_master_source.py",
        ROOT / "qgtoy/static_patch_l2_response.py",
        ROOT / "qgtoy/centrifugal_skyrmion_membrane_stress.py",
        ROOT / "qgtoy/centrifugal_skyrmion_completed_stress.py",
        ROOT / "qgtoy/centrifugal_skyrmion_bvp.py",
        ROOT / "qgtoy/centrifugal_skyrmion_deformation.py",
        ROOT / "qgtoy/massive_skyrmion_profile.py",
        ROOT / "qgtoy/massive_skyrmion_worldtube.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _summary(record: dict[str, object], label: float | int) -> dict[str, object]:
    distribution = record["master_source_distribution_over_kappa"]
    return {
        "label": label,
        "bulk_master_source_maximum_absolute": record[
            "bulk_master_source_maximum_absolute"
        ],
        "bulk_master_source_l1_on_resolved_interval": record[
            "bulk_master_source_l1_on_resolved_interval"
        ],
        "raw_delta_second_coefficient": distribution[
            "master_source_delta_second_coefficient"
        ],
        "contact_free_delta_prime_coefficient": distribution[
            "contact_free_delta_prime_coefficient"
        ],
        "contact_free_delta_coefficient": distribution[
            "contact_free_delta_coefficient"
        ],
        "response_samples": record["response_samples"],
    }


def _response_values(record: dict[str, object]) -> tuple[float, ...]:
    return tuple(
        float(sample["total_master_response_over_kappa"])
        for sample in record["response_samples"]
    )


def _maximum_relative_difference(
    first: dict[str, object], second: dict[str, object]
) -> float:
    return max(
        abs(left - right) / max(1.0e-14, abs(right))
        for left, right in zip(
            _response_values(first), _response_values(second), strict=True
        )
    )


def main() -> None:
    starting_hashes = _source_hashes()
    mesh = [
        centrifugal_skyrmion_master_response_record(node_count=count)
        for count in (101, 201, 401, 801)
    ]
    origin = [
        centrifugal_skyrmion_master_response_record(
            node_count=401, origin_radius=cutoff
        )
        for cutoff in (0.04, 0.02, 0.01)
    ]
    profile = [
        centrifugal_skyrmion_master_response_record(node_count=401, profile_step=step)
        for step in (0.004, 0.002, 0.001)
    ]
    mesh_difference = _maximum_relative_difference(mesh[-2], mesh[-1])
    origin_difference = _maximum_relative_difference(origin[-2], origin[-1])
    profile_difference = _maximum_relative_difference(profile[-2], profile[-1])
    finest_values = _response_values(mesh[-1])
    claims = {
        "master_response_is_nonzero_in_the_fixed_convention": all(
            abs(value) > 1.0e-4 for value in finest_values
        ),
        "response_sign_is_stable_at_declared_sample_points": all(
            value < 0.0 for record in mesh for value in _response_values(record)
        ),
        "two_finest_meshes_agree": mesh_difference < 1.0e-3,
        "origin_cutoff_refinement_is_stable": origin_difference < 1.0e-3,
        "background_profile_refinement_is_stable": profile_difference < 1.0e-4,
        "thin_shell_contact_is_explicitly_removed_off_wall": all(
            abs(
                record["master_source_distribution_over_kappa"][
                    "master_source_delta_second_coefficient"
                ]
            )
            > 1.0e-4
            and record["master_source_distribution_over_kappa"][
                "contact_free_delta_second_coefficient"
            ]
            == 0.0
            for record in mesh
        ),
    }
    record = {
        "goal": "Completed Skyrmion Static Quadrupole Master Response",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "floating_conserved_skyrmion_zerilli_moncrief_response",
        "normalization": mesh[-1]["normalization"],
        "observation_radii": tuple(
            sample["radius"] for sample in mesh[-1]["response_samples"]
        ),
        "mesh_records": tuple(
            _summary(item, count)
            for item, count in zip(mesh, (101, 201, 401, 801), strict=True)
        ),
        "origin_records": tuple(
            _summary(item, cutoff)
            for item, cutoff in zip(origin, (0.04, 0.02, 0.01), strict=True)
        ),
        "profile_records": tuple(
            _summary(item, step)
            for item, step in zip(profile, (0.004, 0.002, 0.001), strict=True)
        ),
        "fine_mesh_maximum_relative_difference": mesh_difference,
        "fine_origin_maximum_relative_difference": origin_difference,
        "fine_profile_maximum_relative_difference": profile_difference,
        "certified_claims": claims,
        "claim_boundary": (
            "Source-hashed floating fixed-background response per kappa and "
            "per q=Q_ab n_a n_b. Bulk derivatives are finite differences and "
            "the origin interval is truncated. No interval enclosure, "
            "physical collective normalization, Israel matching, deformed "
            "background, or Weyl/worldtube reconstruction is supplied."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("master-response files changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "fine_mesh_maximum_relative_difference": mesh_difference,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
