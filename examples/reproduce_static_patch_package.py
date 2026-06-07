"""Reproduce the packaged static-patch observer-algebra certificate summary.

This script is intentionally small: it gives reviewers a clean executable path
without reading the long goal-by-goal CLI list.
"""

from __future__ import annotations

import json
from typing import Any

from qgtoy.inclusion_covariant_dynamics import (
    inclusion_covariant_static_patch_dynamics_certificate,
)
from qgtoy.static_patch_strong_continuity import (
    goal31_static_patch_strong_continuity_certificate,
)
from qgtoy.typeii_static_patch_limit import (
    major_goal_finite_to_typeii_static_patch_certificate,
)


def compact_status(name: str, certificate: dict[str, Any]) -> dict[str, Any]:
    claims = certificate.get("certified_claims", {})
    return {
        "name": name,
        "status": certificate.get("status"),
        "result_type": certificate.get("result_type"),
        "all_certified_claims_true": bool(claims) and all(claims.values()),
        "claim_boundary": certificate.get("claim_boundary"),
    }


def main() -> None:
    strong = goal31_static_patch_strong_continuity_certificate(
        max_cutoff=5,
        noise_strength=1.0,
        fixed_lapse=1.0,
        environment_qubits=4,
        temperature_scale=1.0,
        screen_probability=0.75,
        low_order=2,
        perturbation_radius=0.05,
    )
    typeii = major_goal_finite_to_typeii_static_patch_certificate(
        max_level=4,
        max_consecutive_cutoff=5,
        bridge_cert_max_cutoff=5,
        noise_strength=1.0,
        fixed_lapse=1.0,
        environment_qubits=4,
        temperature_scale=1.0,
        screen_probability=0.75,
        low_order=2,
        perturbation_radius=0.05,
    )
    dynamics = inclusion_covariant_static_patch_dynamics_certificate(
        max_level=4,
        max_consecutive_cutoff=5,
        bridge_cert_max_cutoff=5,
        noise_strength=1.0,
        fixed_lapse=1.0,
        environment_qubits=4,
        temperature_scale=1.0,
        screen_probability=0.75,
        low_order=2,
        perturbation_radius=0.05,
    )
    payload = {
        "package": "static_patch_observer_algebra",
        "claim_boundary": (
            "finite certificate suite; not continuum de Sitter, dS/CFT, "
            "or literal ER=EPR"
        ),
        "certificates": [
            compact_status("strong_continuity_gate", strong),
            compact_status("finite_to_typeii_scaffold", typeii),
            compact_status("inclusion_covariant_dynamics", dynamics),
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

