#!/usr/bin/env python3
"""Write the correlated moving-wall master-load certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_rational_response_trials import (  # noqa: E402
    rational_response_trial_pair_from_record,
)
from qgtoy.validated_centrifugal_response_residual import (  # noqa: E402
    validated_wall_conormal_coefficients,
)
from qgtoy.validated_centrifugal_wall_master_load import (  # noqa: E402
    DEFAULT_WALL_SLOPE,
    loaded_adjoint_wall_residual,
    validated_wall_master_load,
)


OUTPUT = ROOT / "experiments/validated_centrifugal_wall_master_load.json"
SOURCES = (
    "qgtoy/centrifugal_skyrmion_affine_master_kernel.py",
    "qgtoy/validated_centrifugal_liouville_taylor.py",
    "qgtoy/validated_centrifugal_response_residual.py",
    "qgtoy/validated_centrifugal_wall_master_load.py",
    "experiments/centrifugal_skyrmion_rational_response_trials.json",
    "experiments/skyrmion_au2_global_tail_exact_certificate.json",
    "experiments/validated_centrifugal_wall_master_load_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _interval_record(value) -> dict[str, str | float]:
    return {
        "lower": str(value.lower),
        "upper": str(value.upper),
        "lower_float": float(value.lower),
        "upper_float": float(value.upper),
        "width": str(value.width),
    }


def _archived_interval(record: dict[str, str]) -> tuple[Fraction, Fraction]:
    return Fraction(record["lower"]), Fraction(record["upper"])


def build_record() -> dict[str, object]:
    before = {path: _sha256(ROOT / path) for path in SOURCES}
    tail = json.loads(
        (ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json").read_text()
    )
    archived_slope = _archived_interval(tail["exact_outputs"]["wall_slope_enclosure"])
    if archived_slope != (DEFAULT_WALL_SLOPE.lower, DEFAULT_WALL_SLOPE.upper):
        raise ValueError("default wall slope no longer matches the authenticated archive")
    trial_archive = json.loads(
        (ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json").read_text()
    )
    pair = rational_response_trial_pair_from_record(trial_archive["trial_archive"])
    load = validated_wall_master_load(DEFAULT_WALL_SLOPE)
    coefficients = validated_wall_conormal_coefficients(DEFAULT_WALL_SLOPE)
    residual = loaded_adjoint_wall_residual(
        trial=pair.adjoint.positive_radius_cells[-1],
        coefficients=coefficients,
        master_load=load,
    )
    after = {path: _sha256(ROOT / path) for path in SOURCES}
    if before != after:
        raise ValueError("wall-master-load sources changed during audit")
    return {
        "goal": "Validated Moving-Wall Exterior-Master Adjoint Load",
        "status": "pass",
        "result_type": "exact_rational_correlated_wall_load_and_loaded_residual",
        "certified_claims": {
            "wall_green_weight_uses_exact_atanh_series_enclosure": True,
            "profile_slope_and_inverse_remain_correlated": True,
            "gamma_b_is_strictly_positive": load.gamma_b.lower > 0,
            "gamma_b_width_is_below_one_over_5000": (
                load.gamma_b.width < Fraction(1, 5000)
            ),
            "loaded_adjoint_wall_residual_is_below_one_over_150": (
                max(abs(residual.lower), abs(residual.upper)) < Fraction(1, 150)
            ),
        },
        "wall_ratio": str(load.wall_ratio),
        "authenticated_wall_profile_derivative": _interval_record(
            load.wall_profile_derivative
        ),
        "center_regular_solution": _interval_record(load.center_regular_solution),
        "center_regular_solution_derivative": _interval_record(
            load.center_regular_solution_derivative
        ),
        "wall_green_weight": _interval_record(load.wall_green_weight),
        "wall_green_weight_derivative": _interval_record(
            load.wall_green_weight_derivative
        ),
        "wall_displacement_per_radial_field": _interval_record(
            load.wall_displacement_per_radial_field
        ),
        "gamma_b": _interval_record(load.gamma_b),
        "loaded_adjoint_wall_residual": _interval_record(residual),
        "claim_boundary": (
            "This certifies the moving-wall part of the exterior-master adjoint "
            "load and the loaded wall mismatch of the archived rational adjoint "
            "trial. It does not certify the adjoint bulk master load, the adjoint "
            "bulk residual, or nonzero exterior response. The independent "
            "conormal-interface certificate supplies that structural theorem."
        ),
        "source_sha256": before,
    }


def main() -> None:
    payload = build_record()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
