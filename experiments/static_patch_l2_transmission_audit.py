#!/usr/bin/env python3
"""Write the static ``ell=2`` shell-transmission certificate."""

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
from qgtoy.static_patch_l2_transmission import (  # noqa: E402
    l2_green_wall_transmission_record,
    l2_master_distribution_transmission_record,
)


OUTPUT = ROOT / "experiments/static_patch_l2_transmission_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/static_patch_l2_transmission_audit.py",
        ROOT / "qgtoy/static_patch_l2_transmission.py",
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


def main() -> None:
    starting_hashes = _source_hashes()
    response = centrifugal_skyrmion_master_response_record(node_count=401)
    parameters = response["parameters"]
    source = response["master_source_distribution_over_kappa"]
    distribution = l2_master_distribution_transmission_record(
        wall_radius=parameters["wall_radius"],
        static_patch_radius=parameters["static_patch_radius"],
        delta_coefficient=source["master_source_delta_coefficient"],
        delta_prime_coefficient=source["master_source_delta_prime_coefficient"],
        delta_second_coefficient=source[
            "master_source_delta_second_coefficient"
        ],
    )
    green = l2_green_wall_transmission_record(
        wall_radius=parameters["wall_radius"],
        static_patch_radius=parameters["static_patch_radius"],
        contact_free_delta_coefficient=source["contact_free_delta_coefficient"],
        contact_free_delta_prime_coefficient=source[
            "contact_free_delta_prime_coefficient"
        ],
    )
    claims = {
        "literal_delta_jet_recomposes_from_contact_and_jumps": (
            distribution["distribution_recomposition_maximum_error"] < 1.0e-16
        ),
        "green_response_has_predicted_field_jump": (
            abs(green["field_jump_error"]) < 1.0e-14
        ),
        "green_response_has_predicted_flux_jump": (
            abs(green["flux_jump_error"]) < 1.0e-14
        ),
        "completed_skyrmion_field_jump_is_nonzero": (
            abs(distribution["off_wall_master_field_jump"]) > 1.0e-4
        ),
        "completed_skyrmion_flux_jump_is_nonzero": (
            abs(distribution["off_wall_master_flux_jump"]) > 1.0e-4
        ),
    }
    record = {
        "goal": "Static-Patch Quadrupole Shell Transmission",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_master_contact_and_off_wall_jump_identity",
        "source_distribution_over_kappa": source,
        "distribution_transmission_over_kappa": distribution,
        "green_transmission_over_kappa": green,
        "certified_claims": claims,
        "claim_boundary": (
            "Exact transmission identity for the frozen fixed-de-Sitter master "
            "operator and source convention. It checks the master equation but "
            "does not replace tensorial Israel matching, metric reconstruction, "
            "or a finite-thickness membrane limit."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("transmission sources changed during audit")
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
