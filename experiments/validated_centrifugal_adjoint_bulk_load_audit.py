#!/usr/bin/env python3
"""Audit the authenticated positive-radius weak master load."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qgtoy.centrifugal_skyrmion_rational_response_trials import (  # noqa: E402
    rational_response_trial_pair_from_record,
    refine_rational_response_trial,
)
from qgtoy.validated_centrifugal_adjoint_bulk_load import (  # noqa: E402
    validated_bulk_load_on_trial_cell,
    validated_weak_adjoint_residual_cell,
    validated_weak_master_load_cell,
)
from qgtoy.validated_centrifugal_response_residual import (  # noqa: E402
    profile_jet_cell_from_sharp_replay,
    validated_conormal_strong_cell_from_profile,
)
from qgtoy.validated_interval import RationalInterval  # noqa: E402
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
OUTPUT = ROOT / "experiments/validated_centrifugal_adjoint_bulk_load.json"
SOURCES = (
    "qgtoy/validated_centrifugal_adjoint_bulk_load.py",
    "qgtoy/centrifugal_skyrmion_affine_master_kernel.py",
    "experiments/validated_centrifugal_adjoint_bulk_load_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _ceil(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _decimal(integer: int, places: int) -> str:
    sign = "-" if integer < 0 else ""
    digits = str(abs(integer)).zfill(places + 1)
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


def _outward_interval(
    value: RationalInterval, *, places: int = 18
) -> dict[str, str]:
    scale = 10**places
    return {
        "lower": _decimal(_floor(value.lower * scale), places),
        "upper": _decimal(_ceil(value.upper * scale), places),
        "representation": f"outward_decimal_enclosure_{places}_places",
    }


def _outward_upper(value: Fraction, *, places: int = 18) -> str:
    scale = 10**places
    return _decimal(_ceil(value * scale), places)


def build_record() -> dict[str, object]:
    au2 = json.loads(AU2.read_text(encoding="ascii"))
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    archive = json.loads(TRIALS.read_text(encoding="ascii"))
    subdivisions = 8
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=subdivisions
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    trials = {
        "primal": refine_rational_response_trial(
            pair.primal, subdivisions_per_cell=subdivisions
        ),
        "adjoint": refine_rational_response_trial(
            pair.adjoint, subdivisions_per_cell=subdivisions
        ),
    }
    loads = []
    conormal = []
    for profile_cell in profile.cells:
        profile_jet = profile_jet_cell_from_sharp_replay(profile_cell)
        loads.append(
            validated_weak_master_load_cell(
                profile_jet,
                curvature=profile.curvature,
                pion_mass_squared=profile.pion_mass_squared,
                green_terms=8,
                trigonometric_terms=8,
            )
        )
        conormal.append(
            validated_conormal_strong_cell_from_profile(
                profile_jet,
                curvature=profile.curvature,
                pion_mass_squared=profile.pion_mass_squared,
                trigonometric_terms=8,
            )
        )

    functional = {}
    for name, trial in trials.items():
        total = RationalInterval.point(0)
        for load, trial_cell in zip(
            loads, trial.positive_radius_cells, strict=True
        ):
            total += validated_bulk_load_on_trial_cell(load, trial_cell)
        functional[name] = total

    weak_residuals = tuple(
        validated_weak_adjoint_residual_cell(coefficients, load, trial_cell)
        for coefficients, load, trial_cell in zip(
            conormal,
            loads,
            trials["adjoint"].positive_radius_cells,
            strict=True,
        )
    )
    value_max = max(
        abs(endpoint)
        for residual in weak_residuals
        for coefficient in residual.test_value_coefficient
        for endpoint in (coefficient.lower, coefficient.upper)
    )
    derivative_max = max(
        abs(endpoint)
        for residual in weak_residuals
        for coefficient in residual.test_derivative_coefficient
        for endpoint in (coefficient.lower, coefficient.upper)
    )
    claims = {
        "all_344_positive_radius_cells_are_enclosed": len(loads) == 344,
        "weak_load_uses_only_profile_value_and_first_derivative": True,
        "archived_primal_bulk_functional_is_enclosed": functional[
            "primal"
        ].width
        > 0,
        "archived_adjoint_bulk_functional_is_enclosed": functional[
            "adjoint"
        ].width
        > 0,
        "adjoint_weak_residual_retains_derivative_test_term": derivative_max > 0,
    }
    if not all(claims.values()):
        raise ValueError("validated adjoint bulk-load audit failed")
    return {
        "goal": "Validated Positive-Radius Exterior-Master Adjoint Bulk Load",
        "status": "pass",
        "result_type": "exact_weak_load_and_adjoint_residual_coefficient_boxes",
        "parameters": {
            "subdivisions_per_authenticated_cell": subdivisions,
            "positive_radius_cell_count": len(loads),
            "green_series_terms": 8,
            "trigonometric_terms": 8,
        },
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "positive_radius_bulk_functional_enclosure": {
            name: _outward_interval(value) for name, value in functional.items()
        },
        "adjoint_weak_residual_coefficient_absolute_upper": {
            "test_value_coefficient": _outward_upper(value_max),
            "test_derivative_coefficient": _outward_upper(derivative_max),
        },
        "certified_claims": claims,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies the positive-radius weak master load b0 dot v + "
            "b1 dot v' and its coefficient-level subtraction from the archived "
            "adjoint trial on 344 authenticated cells. It does not cover the "
            "regular-origin bulk load, convert the derivative-test coefficient "
            "to an energy-dual norm, certify the full loaded adjoint residual, "
            "or exclude zero exterior response."
        ),
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="ascii"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
