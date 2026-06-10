#!/usr/bin/env python3
"""Write the source-hashed regular conormal-block certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from math import pi
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_conormal_blocks import (  # noqa: E402
    exact_formal_conormal_checks,
    regular_conormal_data,
)
from qgtoy.centrifugal_skyrmion_deformation import (  # noqa: E402
    quadrupole_static_hessian_matrix,
    rotational_quadrupole_source_covector,
)


OUTPUT = ROOT / "experiments/centrifugal_skyrmion_conormal_blocks_certificate.json"
TRANSFER_CERTIFICATE = (
    ROOT / "experiments/validated_centrifugal_origin_transfer_certificate.json"
)
PROFILE_CERTIFICATE = (
    ROOT / "experiments/validated_skyrmion_quintic_family_certificate.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hashes() -> dict[str, str]:
    paths = (
        ROOT / "experiments/centrifugal_skyrmion_conormal_blocks_audit.py",
        ROOT / "qgtoy/centrifugal_skyrmion_conormal_blocks.py",
        ROOT / "qgtoy/centrifugal_skyrmion_deformation.py",
        ROOT / "qgtoy/centrifugal_skyrmion_frobenius.py",
        ROOT / "qgtoy/centrifugal_skyrmion_origin.py",
        ROOT / "qgtoy/validated_centrifugal_origin_transfer.py",
        TRANSFER_CERTIFICATE,
        PROFILE_CERTIFICATE,
    )
    return {str(path.relative_to(ROOT)): _sha256(path) for path in paths}


def _floating_replay_error() -> tuple[float, float]:
    maximum_hessian_error = 0.0
    maximum_source_error = 0.0
    probes = (
        (0.07, 1 / 400, 1.58, -0.31, 1.0),
        (0.19, 0.01, 1.21, 0.08, 0.7),
        (0.41, 0.04, 0.83, -0.14, 0.0),
    )
    for radius, curvature, w, w_t, pion_mass in probes:
        t = radius**2
        metric = 1 - curvature * t
        rho = w + 2 * t * w_t
        regular = regular_conormal_data(
            t=t,
            curvature=curvature,
            profile_deficit_over_radius=w,
            profile_deficit_time_derivative=w_t,
            pion_mass=pion_mass,
        )
        physical = quadrupole_static_hessian_matrix(
            radius=radius,
            metric_factor=metric,
            profile=pi - radius * w,
            profile_derivative=-rho,
            pion_mass=pion_mass,
        )["symmetric_hessian_matrix"]
        reconstructed = (
            (
                *regular["coordinate"][0],
                *(radius * value for value in regular["mixed"][0]),
            ),
            (
                *regular["coordinate"][1],
                *(radius * value for value in regular["mixed"][1]),
            ),
            (
                radius * regular["mixed"][0][0],
                radius * regular["mixed"][1][0],
                *(t * value for value in regular["principal"][0]),
            ),
            (
                radius * regular["mixed"][0][1],
                radius * regular["mixed"][1][1],
                *(t * value for value in regular["principal"][1]),
            ),
        )
        maximum_hessian_error = max(
            maximum_hessian_error,
            *(
                abs(float(left) - float(right))
                for left_row, right_row in zip(physical, reconstructed, strict=True)
                for left, right in zip(left_row, right_row, strict=True)
            ),
        )

        source = rotational_quadrupole_source_covector(
            radius=radius,
            metric_factor=metric,
            profile=pi - radius * w,
            profile_derivative=-rho,
        )
        reconstructed_source = (
            radius * regular["coordinate_source"][0],
            radius * regular["coordinate_source"][1],
            t * regular["derivative_source"][0],
            t * regular["derivative_source"][1],
        )
        physical_source = (
            source["radial_field_coefficient"],
            source["tangential_field_coefficient"],
            source["radial_field_derivative_coefficient"],
            source["tangential_field_derivative_coefficient"],
        )
        maximum_source_error = max(
            maximum_source_error,
            *(
                abs(float(left) - float(right))
                for left, right in zip(
                    physical_source, reconstructed_source, strict=True
                )
            ),
        )
    return maximum_hessian_error, maximum_source_error


def main() -> None:
    starting_hashes = _source_hashes()
    formal = exact_formal_conormal_checks()
    hessian_error, source_error = _floating_replay_error()
    checks = {
        "regular_blocks_match_established_origin_matrix": formal[
            "fuchs_constant_matches_established_a0"
        ],
        "hatted_source_vanishes_at_origin": formal["source_constant_vanishes"],
        "all_three_conormal_residuals_divisible_by_t_cubed": all(
            formal["conormal_residual_divisible_by_t_cubed"].values()
        ),
        "positive_radius_hessian_replay_below_1e_11": hessian_error < 1e-11,
        "positive_radius_source_replay_below_1e_11": source_error < 1e-11,
    }
    if not all(checks.values()):
        raise ValueError("regular conormal-block audit failed")

    record = {
        "result_type": "exact_regular_conormal_blocks_and_residual_divisibility",
        "status": "pass",
        "regular_density": (
            "H_static/t=a^T Cbar a+2a^T Mbar d+d^T Pbar d, with a=y/x and d=y'"
        ),
        "physical_block_scaling": "C=Cbar, M=x Mbar, P=t Pbar",
        "fuchs_variation_order": formal["fuchs_variation_order"],
        "source_order": formal["source_order"],
        "residual_transfer_identity": formal["residual_transfer_identity"],
        "euler_residual_order": formal["euler_residual_order"],
        "conormal_residual_checks": formal["conormal_residual_divisible_by_t_cubed"],
        "floating_replay_diagnostics": {
            "maximum_absolute_hessian_error": hessian_error,
            "maximum_absolute_source_error": source_error,
        },
        "executable_checks": checks,
        "validated_transfer_dependency": {
            "path": str(TRANSFER_CERTIFICATE.relative_to(ROOT)),
            "sha256": _sha256(TRANSFER_CERTIFICATE),
        },
        "validated_profile_dependency": {
            "path": str(PROFILE_CERTIFICATE.relative_to(ROOT)),
            "sha256": _sha256(PROFILE_CERTIFICATE),
        },
        "claim_boundary": (
            "Exact regular blocks, source factorization, A-A0 order, and "
            "t^3 conormal residual divisibility. Quantitative interval bounds "
            "on A-A0 and the scaled residual e are still required for the "
            "finite-cell radii inequality."
        ),
        "source_sha256": starting_hashes,
    }
    if _source_hashes() != starting_hashes:
        raise ValueError("regular conormal-block sources changed during audit")
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
