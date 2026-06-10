#!/usr/bin/env python3
"""Write the exterior static-quadrupole Weyl reconstruction certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from math import pi, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.static_patch_l2_weyl_reconstruction import (  # noqa: E402
    direct_rw_radial_electric_weyl_coefficient,
    horizon_regular_l2_weyl_record,
    physical_skyrmion_exterior_weyl_record,
)


OUTPUT = ROOT / "experiments/static_patch_l2_weyl_reconstruction_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/static_patch_l2_weyl_reconstruction_audit.py",
        ROOT / "qgtoy/static_patch_l2_weyl_reconstruction.py",
        ROOT / "qgtoy/centrifugal_skyrmion_physical_response.py",
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


def _pure_density(state: tuple[complex, ...]) -> tuple[tuple[complex, ...], ...]:
    return tuple(
        tuple(left * right.conjugate() for right in state) for left in state
    )


def main() -> None:
    starting_hashes = _source_hashes()
    radius = 7.0
    patch = 20.0
    amplitude = -0.13
    reconstruction = horizon_regular_l2_weyl_record(
        radius=radius,
        static_patch_radius=patch,
        exterior_master_amplitude=amplitude,
    )
    temporal = 1.5 * amplitude * (patch**2 / radius**3 - 1.0 / radius)
    temporal_p = 1.5 * amplitude * (-3.0 * patch**2 / radius**4 + 1.0 / radius**2)
    temporal_pp = 1.5 * amplitude * (
        12.0 * patch**2 / radius**5 - 2.0 / radius**3
    )
    direct_weyl = direct_rw_radial_electric_weyl_coefficient(
        radius=radius,
        static_patch_radius=patch,
        temporal_metric_amplitude=temporal,
        temporal_metric_amplitude_derivative=temporal_p,
        temporal_metric_amplitude_second_derivative=temporal_pp,
    )
    cat = _pure_density((1.0 / sqrt(2.0), 0.0, 0.0, 0.0, 1.0 / sqrt(2.0)))
    skyrmion = physical_skyrmion_exterior_weyl_record(
        skyrme_coupling=1.0,
        pion_decay_constant=1.0,
        newton_constant=1.0e-6,
        spin=2.0,
        state_density_matrix=cat,
        node_count=401,
        maximum_slow_rotation=0.1,
    )
    first = skyrmion["response_samples"][0]
    tensor_norm_squared = sum(
        value**2
        for row in first["physical_radial_electric_weyl_tensor_Err_ab"]
        for value in row
    )
    claims = {
        "vacuum_rw_reconstruction_roundtrips_master": (
            abs(reconstruction["master_roundtrip_error"]) < 1.0e-14
        ),
        "vacuum_radial_and_radial_angular_equations_close": (
            abs(reconstruction["radial_einstein_residual"]) < 1.0e-14
            and abs(reconstruction["radial_angular_einstein_residual"]) < 1.0e-14
        ),
        "direct_metric_weyl_matches_minus_six_master_over_r_cubed": (
            abs(direct_weyl - reconstruction["radial_electric_weyl_coefficient"])
            < 1.0e-14
        ),
        "completed_exterior_response_is_one_horizon_regular_mode": (
            skyrmion["exterior_master_amplitude_spread"] < 1.0e-14
        ),
        "spin_cat_has_nonzero_exterior_tidal_curvature": all(
            sample["physical_radial_electric_weyl_angular_rms"] > 0.0
            for sample in skyrmion["response_samples"]
        ),
        "weyl_angular_integral_uses_exact_tensor_norm": abs(
            first["physical_radial_electric_weyl_angular_integral"]
            - 8.0 * pi * tensor_norm_squared / 15.0
        )
        < 1.0e-30,
    }
    record = {
        "goal": "Exterior Gauge-Invariant Skyrmion Tidal Curvature",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "physical_exterior_radial_electric_weyl_quadrupole",
        "analytic_horizon_regular_check": {
            "reconstruction": reconstruction,
            "direct_metric_weyl_coefficient": direct_weyl,
        },
        "physical_skyrmion_exterior_weyl": skyrmion,
        "certified_claims": claims,
        "claim_boundary": (
            "Source-hashed floating exterior linearized Weyl reconstruction on "
            "fixed pure de Sitter. It is gauge invariant and physically "
            "normalized, but not interval validated, tensorially Israel "
            "matched, self-gravitating, or composed with detector dynamics."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("Weyl reconstruction sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "exterior_master_amplitude_spread": skyrmion[
                    "exterior_master_amplitude_spread"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
