#!/usr/bin/env python3
"""Write the physically normalized Skyrmion master-response certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from math import sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_master_response import (  # noqa: E402
    centrifugal_skyrmion_master_response_record,
)
from qgtoy.centrifugal_skyrmion_physical_response import (  # noqa: E402
    normalize_skyrmion_master_response,
)
from qgtoy.massive_skyrmion_worldtube import (  # noqa: E402
    hard_wall_equilibrium_record,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_physical_response_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_physical_response_audit.py",
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


def _spin_two_cat_density() -> tuple[tuple[complex, ...], ...]:
    return _pure_density((1.0 / sqrt(2.0), 0.0, 0.0, 0.0, 1.0 / sqrt(2.0)))


def _spin_two_anticoherent_density() -> tuple[tuple[complex, ...], ...]:
    return _pure_density((0.5, 0.0, 1.0j / sqrt(2.0), 0.0, 0.5))


def main() -> None:
    starting_hashes = _source_hashes()
    response = centrifugal_skyrmion_master_response_record(node_count=401)
    parameters = response["parameters"]
    worldtube = hard_wall_equilibrium_record(
        pion_mass=parameters["pion_mass_mu"],
        curvature=parameters["curvature_lambda"],
        wall_radius=parameters["wall_radius"],
        step=parameters["profile_step"],
    )
    inertia = worldtube["profile_integrals"][
        "interior_dimensionless_inertia_c_I"
    ]
    anisotropic = normalize_skyrmion_master_response(
        response,
        skyrme_coupling=1.0,
        pion_decay_constant=1.0,
        newton_constant=1.0e-6,
        inertia_constant=inertia,
        spin=2.0,
        state_density_matrix=_spin_two_cat_density(),
        maximum_slow_rotation=0.1,
    )
    anticoherent = normalize_skyrmion_master_response(
        response,
        skyrme_coupling=1.0,
        pion_decay_constant=1.0,
        newton_constant=1.0e-6,
        inertia_constant=inertia,
        spin=2.0,
        state_density_matrix=_spin_two_anticoherent_density(),
        maximum_slow_rotation=0.1,
    )
    rescaled = normalize_skyrmion_master_response(
        response,
        skyrme_coupling=2.0,
        pion_decay_constant=1.0,
        newton_constant=1.0e-6,
        inertia_constant=inertia,
        spin=2.0,
        state_density_matrix=_spin_two_cat_density(),
    )
    first = anisotropic["response_samples"][0]
    first_rescaled = rescaled["response_samples"][0]
    tensor_norm_squared = sum(
        value**2 for row in first["physical_master_tensor_Psi_ab"] for value in row
    )
    claims = {
        "dimensionless_einstein_coupling_is_eight_pi_G_f_pi_squared": (
            abs(
                anisotropic["physical_units"][
                    "dimensionless_einstein_coupling_kappa_hat"
                ]
                - 8.0 * 3.141592653589793e-6
            )
            < 1.0e-20
        ),
        "same_profile_inertia_is_positive_and_finite": inertia > 34.0,
        "spin_cat_is_inside_declared_slow_rotation_budget": (
            anisotropic["collective_state"][
                "slow_rotation_parameter_e_squared_sqrt_j_jplus1_over_c_I"
            ]
            < 0.1
        ),
        "anisotropic_state_has_nonzero_physical_master_rms": all(
            sample["physical_master_angular_rms"] > 0.0
            for sample in anisotropic["response_samples"]
        ),
        "anticoherent_state_has_zero_quadrupole_response": all(
            sample["physical_master_angular_rms"] == 0.0
            for sample in anticoherent["response_samples"]
        ),
        "master_amplitude_scales_as_e_cubed_at_fixed_dimensionless_model": abs(
            rescaled["physical_master_prefactor_per_psi0_and_QJ"]
            / anisotropic["physical_master_prefactor_per_psi0_and_QJ"]
            - 8.0
        )
        < 1.0e-14,
        "master_over_radius_scales_as_e_fourth_at_fixed_dimensionless_model": abs(
            first_rescaled["dimensionless_master_signal_rms_Psi_over_r"]
            / first["dimensionless_master_signal_rms_Psi_over_r"]
            - 16.0
        )
        < 1.0e-13,
        "angular_integral_uses_exact_traceless_tensor_norm": abs(
            first["physical_master_angular_integral"]
            - 8.0 * 3.141592653589793 * tensor_norm_squared / 15.0
        )
        < 1.0e-30,
    }
    record = {
        "goal": "Physical Collective Normalization Of The Skyrmion Master Response",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "physical_state_dependent_skyrmion_master_amplitude",
        "dimensionless_response_parameters": parameters,
        "dimensionless_inertia_c_I": inertia,
        "anisotropic_spin_two_cat": anisotropic,
        "anticoherent_spin_two": anticoherent,
        "coupling_rescaled_spin_two_cat": rescaled,
        "certified_claims": claims,
        "claim_boundary": (
            "Source-hashed physical and collective normalization of the frozen "
            "fixed-background master response. The state-dependent master "
            "amplitude is not yet an Israel-matched metric or local Weyl "
            "detector observable, and collective-band errors remain open. "
            "The e-scaling audit holds fixed the dimensionless model, so it "
            "co-varies physical masses and radii."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("physical-response sources changed during audit")
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered, encoding="ascii")
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": hashlib.sha256(rendered.encode("ascii")).hexdigest(),
                "status": record["status"],
                "dimensionless_inertia_c_I": inertia,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
