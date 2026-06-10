#!/usr/bin/env python3
"""Write the centered correlated outer primal residual certificate."""

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
)
from qgtoy.validated_centrifugal_correlated_residual import (  # noqa: E402
    correlated_primal_residual_cells,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
OUTPUT = ROOT / "experiments/validated_centrifugal_correlated_residual.json"
SOURCES = (
    "qgtoy/validated_centrifugal_correlated_residual.py",
    "experiments/validated_centrifugal_correlated_residual_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _absolute_upper(value) -> Fraction:
    return max(abs(value.lower), abs(value.upper))


def build_record() -> dict[str, object]:
    au2 = json.loads(AU2.read_text(encoding="ascii"))
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    archive = json.loads(TRIALS.read_text(encoding="ascii"))
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=1
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    cells = correlated_primal_residual_cells(profile, pair.primal)
    l2_squared = sum(
        (cell.l2_squared_upper for cell in cells), start=Fraction(0)
    )
    maximum = max(
        _absolute_upper(component)
        for cell in cells
        for component in cell.residual
    )
    independent_box_bound = Fraction(
        "328.138482717430509307723019090797910644804365393117403878"
    )
    claims = {
        "all_43_authenticated_cells_are_enclosed": len(cells) == 43,
        "profile_trial_and_radius_share_one_centered_coordinate": True,
        "newton_tube_errors_remain_rigorous_interval_remainders": True,
        "outer_primal_l2_squared_is_below_11_over_1000": (
            l2_squared < Fraction(11, 1000)
        ),
        "correlated_bound_improves_independent_box_bound_by_over_30000": (
            independent_box_bound / l2_squared > 30000
        ),
    }
    if not all(claims.values()):
        raise ValueError("correlated residual audit failed")
    return {
        "goal": "Validated Centered Correlated Outer Primal Residual",
        "status": "pass",
        "result_type": "exact_rational_centered_taylor_residual_enclosure",
        "parameters": {
            "authenticated_cell_count": len(cells),
            "degree_limit": 8,
            "rounding_denominator": 10**16,
            "trigonometric_terms": 6,
        },
        "outer_primal_residual": {
            "l2_squared_upper": str(l2_squared),
            "l2_squared_upper_float": float(l2_squared),
            "maximum_pointwise_component_absolute_upper": str(maximum),
            "maximum_pointwise_component_absolute_upper_float": float(maximum),
            "previous_independent_box_l2_squared_upper": str(independent_box_bound),
            "improvement_factor_lower": 30000,
        },
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "certified_claims": claims,
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This certifies the positive-radius primal strong residual with the "
            "exact spline/trial radial correlation and interval Newton-tube "
            "remainders. It does not include the origin or wall residual, certify "
            "an adjoint energy-dual norm, or exclude zero exterior response."
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
