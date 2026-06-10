#!/usr/bin/env python3
"""Write the distributional centrifugal-membrane conservation certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_membrane_stress import (  # noqa: E402
    default_membrane_distributional_conservation_record,
    pure_tension_shell_divergence_coefficients,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_membrane_stress_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_membrane_stress_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_membrane_stress.py",
        ROOT / "qgtoy/centrifugal_skyrmion_completed_stress.py",
        ROOT / "qgtoy/centrifugal_skyrmion_bvp.py",
        ROOT / "qgtoy/centrifugal_skyrmion_deformation.py",
        ROOT / "qgtoy/massive_skyrmion_profile.py",
        ROOT / "qgtoy/massive_skyrmion_worldtube.py",
        ROOT / "qgtoy/static_even_stress_conservation.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _mesh_summary(node_count: int) -> dict[str, float | int | str]:
    record = default_membrane_distributional_conservation_record(node_count=node_count)
    conservation = record["distributional_conservation"]
    return {
        "node_count": node_count,
        "status": record["status"],
        "wall_displacement_coefficient": record["wall_displacement_coefficient"],
        "background_young_laplace_residual": conservation[
            "background_young_laplace_residual"
        ],
        "linearized_normal_force_residual": conservation[
            "linearized_normal_force_residual"
        ],
        "linearized_tangential_force_residual": conservation[
            "linearized_tangential_force_residual"
        ],
        "factorization_maximum_error": conservation["factorization_maximum_error"],
        "maximum_distributional_conservation_coefficient": conservation[
            "maximum_distributional_conservation_coefficient"
        ],
    }


def main() -> None:
    starting_hashes = _source_hashes()
    shell_identity = pure_tension_shell_divergence_coefficients(
        ell=2,
        wall_radius=2.0,
        wall_metric_factor=0.8,
        wall_metric_factor_derivative=-0.1,
        wall_metric_factor_second_derivative=-0.05,
        membrane_tension=0.03,
        wall_displacement_coefficient=0.2,
    )
    mesh_records = [_mesh_summary(count) for count in (101, 201, 401, 801)]
    claims = {
        "pure_tension_shell_divergence_factors_into_curvature_force": (
            shell_identity["curvature_factorization_maximum_error"] < 1.0e-15
        ),
        "background_young_laplace_balance_closes": all(
            abs(record["background_young_laplace_residual"]) < 1.0e-10
            for record in mesh_records
        ),
        "linearized_normal_force_balance_closes": all(
            abs(record["linearized_normal_force_residual"]) < 2.0e-12
            for record in mesh_records
        ),
        "linearized_tangential_force_balance_closes": all(
            abs(record["linearized_tangential_force_residual"]) < 1.0e-12
            for record in mesh_records
        ),
        "bulk_plus_shell_distribution_is_conserved": all(
            record["maximum_distributional_conservation_coefficient"] < 2.0e-12
            for record in mesh_records
        ),
    }
    record = {
        "goal": "Distributional Centrifugal Skyrmion Membrane Completion",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": ("exact_distributional_factorization_and_floating_wall_closure"),
        "shell_curvature_identity": shell_identity,
        "mesh_records": mesh_records,
        "certified_claims": claims,
        "claim_boundary": (
            "The distributional factorization is analytic and the default "
            "wall closure is source-hashed floating evidence. The profile and "
            "BVP are not interval enclosed. Self-gravity, Israel matching, "
            "surface elasticity, exterior matter, and the Zerilli projection "
            "are excluded."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("membrane-stress sources changed during audit")
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
