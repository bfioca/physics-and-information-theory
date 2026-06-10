#!/usr/bin/env python3
"""Write the exact static-patch quadrupole master-source certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.static_patch_l2_master_source import (  # noqa: E402
    canonical_l2_master_source_distribution,
    contact_free_wall_response,
    rw_metric_master_identity_record,
    static_l2_master_source_density,
    static_patch_l2_green_source_derivative,
    traceless_quadrupole_harmonic_norm_squared,
)
from qgtoy.static_patch_l2_response import (  # noqa: E402
    static_patch_l2_green_kernel,
)


OUTPUT = ROOT / "experiments/static_patch_l2_master_source_certificate.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/static_patch_l2_master_source_audit.py",
        ROOT / "qgtoy/static_patch_l2_master_source.py",
        ROOT / "qgtoy/static_patch_l2_response.py",
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _polynomial_jet(
    coefficients: tuple[float, ...], radius: float, maximum_order: int
) -> tuple[float, ...]:
    values = []
    current = coefficients
    for _ in range(maximum_order + 1):
        values.append(sum(value * radius**index for index, value in enumerate(current)))
        current = tuple(index * current[index] for index in range(1, len(current)))
    return tuple(values)


def main() -> None:
    starting_hashes = _source_hashes()
    radius = 1.3
    coupling = 0.7
    h0 = _polynomial_jet((0.2, -0.1, 0.03), radius, 1)
    h2 = _polynomial_jet((-0.3, 0.2, -0.04, 0.01), radius, 2)
    angular = _polynomial_jet((0.1, 0.05, -0.02, 0.004), radius, 3)
    metric_identity = rw_metric_master_identity_record(
        radius=radius,
        static_patch_radius=10.0,
        temporal_metric_amplitude=h0[0],
        temporal_metric_amplitude_derivative=h0[1],
        radial_metric_amplitude=h2[0],
        radial_metric_amplitude_derivative=h2[1],
        radial_metric_amplitude_second_derivative=h2[2],
        angular_metric_amplitude=angular[0],
        angular_metric_amplitude_derivative=angular[1],
        angular_metric_amplitude_second_derivative=angular[2],
        angular_metric_amplitude_third_derivative=angular[3],
    )
    stress_source = static_l2_master_source_density(
        radius=radius,
        static_patch_radius=10.0,
        energy_density=(-metric_identity["einstein_time_time_amplitude"] / coupling),
        energy_density_derivative=(
            -metric_identity["einstein_time_time_amplitude_derivative"] / coupling
        ),
        radial_pressure=(
            metric_identity["einstein_radial_pressure_amplitude"] / coupling
        ),
        radial_angular_shear=(
            metric_identity["einstein_radial_angular_amplitude"] / coupling
        ),
        angular_tracefree_stress=(
            metric_identity["einstein_angular_tracefree_amplitude"] / coupling
        ),
        gravitational_coupling=coupling,
    )
    distribution = canonical_l2_master_source_distribution(
        wall_radius=4.0,
        static_patch_radius=20.0,
        bulk_energy_density_at_wall=0.2,
        energy_density_delta=-0.03,
        energy_density_delta_prime=0.04,
        radial_pressure_delta=0.05,
        radial_pressure_delta_prime=-0.01,
        radial_angular_shear_delta=-0.02,
        radial_angular_shear_delta_prime=0.006,
        angular_tracefree_stress_delta=0.008,
        angular_tracefree_stress_delta_prime=-0.004,
        gravitational_coupling=coupling,
    )
    contact_checks = []
    for observation in (2.0, 6.0):
        green = static_patch_l2_green_kernel(observation, 4.0, static_patch_radius=20.0)
        green_p = static_patch_l2_green_source_derivative(
            observation, 4.0, static_patch_radius=20.0
        )
        lapse = 0.96
        lapse_p = -0.02
        green_pp = (-lapse_p * green_p + 6.0 * green / 16.0) / lapse
        raw = (
            distribution["master_source_delta_coefficient"] * green
            - distribution["master_source_delta_prime_coefficient"] * green_p
            + distribution["master_source_delta_second_coefficient"] * green_pp
        )
        contact_free = contact_free_wall_response(
            observation,
            wall_radius=4.0,
            static_patch_radius=20.0,
            contact_free_delta_coefficient=distribution[
                "contact_free_delta_coefficient"
            ],
            contact_free_delta_prime_coefficient=distribution[
                "contact_free_delta_prime_coefficient"
            ],
        )
        contact_checks.append(
            {
                "observation_radius": observation,
                "raw_distribution_response": raw,
                "contact_free_response": contact_free,
                "difference": contact_free - raw,
            }
        )
    claims = {
        "direct_einstein_elimination_identity_closes": (
            abs(metric_identity["identity_residual"]) < 1.0e-14
        ),
        "stress_source_matches_metric_master_operator": (
            abs(stress_source - metric_identity["master_operator"]) < 1.0e-14
        ),
        "general_delta_jet_projection_matches_frozen_oracle": (
            abs(distribution["master_source_delta_second_coefficient"] + 0.07168)
            < 1.0e-14
            and abs(
                distribution["master_source_delta_prime_coefficient"]
                - 0.13150666666666666
            )
            < 1.0e-14
            and abs(distribution["master_source_delta_coefficient"] - 0.2933) < 1.0e-14
        ),
        "contact_subtraction_preserves_both_off_wall_branches": all(
            abs(item["difference"]) < 1.0e-14 for item in contact_checks
        ),
        "quadratic_rotation_harmonic_norm_is_sixteen_pi_over_forty_five": (
            abs(
                traceless_quadrupole_harmonic_norm_squared(2.0 / 3.0)
                - 16.0 * 3.141592653589793 / 45.0
            )
            < 1.0e-14
        ),
    }
    record = {
        "goal": "Conserved Stress To Static-Patch Quadrupole Master Source",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_rw_zerilli_moncrief_source_and_contact_map",
        "metric_identity": metric_identity,
        "stress_source": stress_source,
        "canonical_distribution_example": distribution,
        "contact_subtraction_checks": contact_checks,
        "master_source_formula": (
            "F=kappa[-r^2 N rho'/6+r(1+4r^2/R^2)rho/6-r p_r/2-j+2r pi]"
        ),
        "certified_claims": claims,
        "claim_boundary": (
            "Exact direct Regge--Wheeler-gauge Einstein elimination in fixed "
            "pure de Sitter and the declared Zerilli--Moncrief normalization. "
            "A separate Kodama--Ishibashi convention cross-check, self-gravity, "
            "Israel matching, physical collective normalization, and an "
            "invariant curvature reconstruction remain open."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("master-source files changed during audit")
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
