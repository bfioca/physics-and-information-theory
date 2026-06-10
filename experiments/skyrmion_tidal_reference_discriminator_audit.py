#!/usr/bin/env python3
"""Write the equal-energy rotational-reference tidal certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.skyrmion_tidal_reference_discriminator import (  # noqa: E402
    spin_two_tidal_reference_discriminator_record,
)


OUTPUT = ROOT / "experiments/skyrmion_tidal_reference_discriminator_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/skyrmion_tidal_reference_discriminator_audit.py",
        ROOT / "qgtoy/skyrmion_tidal_reference_discriminator.py",
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


def main() -> None:
    starting_hashes = _source_hashes()
    common = {
        "skyrme_coupling": 1.0,
        "pion_decay_constant": 1.0,
        "newton_constant": 1.0e-6,
        "physical_proof_mass_separation": 1.0,
        "observation_radius": 5.0,
        "node_count": 401,
        "maximum_slow_rotation": 0.1,
    }
    axial = spin_two_tidal_reference_discriminator_record(
        **common,
        observation_direction=(0.0, 0.0, 1.0),
    )
    transverse = spin_two_tidal_reference_discriminator_record(
        **common,
        observation_direction=(1.0, 0.0, 0.0),
    )
    axial_signal = axial["spin_cat_gradiometer"]["linearized_relative_acceleration"]
    transverse_signal = transverse["spin_cat_gradiometer"][
        "linearized_relative_acceleration"
    ]
    claims = {
        "states_have_identical_fixed_spin_casimir": (
            axial["same_casimir_check"]
            and axial["shared_casimir_expectation"] == 6.0
        ),
        "states_have_identical_inertia_and_rotor_energy": (
            axial["same_inertia_and_energy_check"]
            and axial["shared_physical_rotor_inertia"] > 34.0
            and axial["shared_leading_rigid_rotor_energy"] > 0.0
        ),
        "spin_cat_has_nonzero_axial_gradiometer_signal": abs(axial_signal) > 1.0e-12,
        "anticoherent_state_has_zero_leading_gradiometer_signal": (
            axial["anticoherent_gradiometer"][
                "linearized_relative_acceleration"
            ]
            == 0.0
            and transverse["anticoherent_gradiometer"][
                "linearized_relative_acceleration"
            ]
            == 0.0
        ),
        "cat_tidal_tensor_has_expected_axis_ratio": abs(
            axial_signal / transverse_signal + 2.0
        )
        < 1.0e-12,
        "equal_leading_rotor_energy_mean_fields_are_tidally_distinguishable": (
            axial["linearized_relative_acceleration_contrast"] != 0.0
        ),
    }
    record = {
        "goal": "Operational Equal-Leading-Rotor-Energy Reference Discriminator",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "instantaneous_exterior_tidal_gradiometer_contrast",
        "axial_observation": axial,
        "transverse_observation": transverse,
        "certified_claims": claims,
        "claim_boundary": (
            "Source-hashed floating Jacobi-limit geodesic-deviation contrast on "
            "the fixed-background exterior branch. It is a semiclassical mean "
            "signal at leading rigid-rotor order, not a single-shot quantum "
            "metric prediction. No finite-time detector transfer function, "
            "Omega^4 energy, noise/fluctuation model, interval validation, "
            "self-gravity, or tensorial Israel matching is supplied."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("tidal discriminator sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "axial_linearized_relative_acceleration_contrast": axial[
                    "linearized_relative_acceleration_contrast"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
