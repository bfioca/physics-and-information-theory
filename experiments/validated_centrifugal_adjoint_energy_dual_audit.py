#!/usr/bin/env python3
"""Write the positive-radius-plus-wall adjoint form-dual certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from qgtoy.centrifugal_skyrmion_rational_response_trials import (  # noqa: E402
    rational_response_trial_pair_from_record,
    refine_rational_response_trial,
)
from qgtoy.validated_centrifugal_adjoint_bulk_load import (  # noqa: E402
    validated_weak_adjoint_residual_cell,
    validated_weak_master_load_cell,
)
from qgtoy.validated_centrifugal_adjoint_energy_dual import (  # noqa: E402
    certify_positive_radius_wall_adjoint_dual_bound,
    validated_adjoint_energy_dual_cell,
)
from qgtoy.validated_centrifugal_response_residual import (  # noqa: E402
    profile_jet_cell_from_sharp_replay,
    validated_conormal_strong_cell_from_profile,
    validated_wall_conormal_coefficients,
)
from qgtoy.validated_centrifugal_wall_master_load import (  # noqa: E402
    loaded_adjoint_wall_residual,
    validated_wall_master_load,
)
from qgtoy.validated_skyrmion_sharp_profile import (  # noqa: E402
    reconstruct_validated_skyrmion_sharp_profile,
)


AU2 = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
SHARP = ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json"
TRIALS = ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
OUTPUT = ROOT / "experiments/validated_centrifugal_adjoint_energy_dual.json"
SOURCES = (
    "qgtoy/validated_centrifugal_adjoint_bulk_load.py",
    "qgtoy/validated_centrifugal_adjoint_energy_dual.py",
    "qgtoy/validated_centrifugal_wall_master_load.py",
    "experiments/validated_centrifugal_adjoint_energy_dual_audit.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _ceil(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def _outward_upper(value: Fraction, *, places: int = 18) -> str:
    scale = 10**places
    integer = _ceil(value * scale)
    digits = str(integer).zfill(places + 1)
    return f"{digits[:-places]}.{digits[-places:]}"


def build_record() -> dict[str, object]:
    au2 = json.loads(AU2.read_text(encoding="ascii"))
    sharp = json.loads(SHARP.read_text(encoding="ascii"))
    archive = json.loads(TRIALS.read_text(encoding="ascii"))
    subdivisions = 8
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=subdivisions
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    adjoint = refine_rational_response_trial(
        pair.adjoint, subdivisions_per_cell=subdivisions
    )
    dual_cells = []
    for profile_cell, trial_cell in zip(
        profile.cells, adjoint.positive_radius_cells, strict=True
    ):
        profile_jet = profile_jet_cell_from_sharp_replay(profile_cell)
        coefficients = validated_conormal_strong_cell_from_profile(
            profile_jet,
            curvature=profile.curvature,
            pion_mass_squared=profile.pion_mass_squared,
            trigonometric_terms=8,
        )
        load = validated_weak_master_load_cell(
            profile_jet,
            curvature=profile.curvature,
            pion_mass_squared=profile.pion_mass_squared,
            green_terms=8,
            trigonometric_terms=8,
        )
        weak = validated_weak_adjoint_residual_cell(
            coefficients, load, trial_cell
        )
        dual_cells.append(
            validated_adjoint_energy_dual_cell(
                weak,
                coefficients,
                principal_lower_bound=Fraction(1, 100),
                completed_potential_lower_bound=Fraction(1, 100),
            )
        )
    wall_coefficients = validated_wall_conormal_coefficients(
        profile.cells[-1].solution_derivative,
        curvature=profile.curvature,
        pion_mass_squared=profile.pion_mass_squared,
    )
    wall_load = validated_wall_master_load(
        profile.cells[-1].solution_derivative
    )
    wall_residual = loaded_adjoint_wall_residual(
        trial=adjoint.positive_radius_cells[-1],
        coefficients=wall_coefficients,
        master_load=wall_load,
    )
    partial = certify_positive_radius_wall_adjoint_dual_bound(
        tuple(dual_cells),
        wall_residual=wall_residual,
        wall_trace_margin_lower_bound=wall_coefficients.wall_trace_margin.lower,
        principal_lower_bound=Fraction(1, 100),
        completed_potential_lower_bound=Fraction(1, 100),
    )
    claims = {
        "all_344_positive_radius_cells_are_lifted_in_v_star": (
            len(partial.cells) == 344
        ),
        "derivative_test_term_uses_completed_square_not_l2_shortcut": True,
        "positive_radius_plus_wall_partial_norm_is_below_four_fifths": (
            partial.partial_energy_dual_upper < Fraction(4, 5)
        ),
        "wall_contribution_is_below_one_over_5000_in_squared_norm": (
            partial.wall_squared_upper < Fraction(1, 5000)
        ),
        "regular_origin_master_load_is_explicitly_omitted": (
            not partial.regular_origin_master_load_included
            and not partial.full_loaded_adjoint_residual_certified
        ),
    }
    if not all(claims.values()):
        failed = tuple(name for name, passed in claims.items() if not passed)
        raise ValueError(f"adjoint energy-dual audit failed: {failed}")
    return {
        "goal": "Validated Partial Adjoint Form-Dual Bound",
        "status": "pass",
        "result_type": "positive_radius_plus_wall_completed_square_v_star_bound",
        "parameters": {
            "positive_radius_cell_count": len(partial.cells),
            "principal_lower_bound": "1/100",
            "completed_potential_lower_bound": "1/100",
            "wall_trace_margin_lower_bound": str(
                partial.wall_trace_margin_lower_bound
            ),
        },
        "partial_bound": {
            "bulk_derivative_squared_upper": _outward_upper(
                partial.bulk_derivative_squared_upper
            ),
            "bulk_value_squared_upper": _outward_upper(
                partial.bulk_value_squared_upper
            ),
            "wall_squared_upper": _outward_upper(partial.wall_squared_upper),
            "squared_dual_upper": _outward_upper(
                partial.partial_squared_dual_upper
            ),
            "squared_dual_upper_float": float(partial.partial_squared_dual_upper),
            "energy_dual_upper": _outward_upper(partial.partial_energy_dual_upper),
            "energy_dual_upper_float": float(partial.partial_energy_dual_upper),
            "dominant_cell_index": partial.dominant_cell_index,
            "dominant_cell_radius": {
                "lower": str(partial.dominant_cell_radius.lower),
                "upper": str(partial.dominant_cell_radius.upper),
            },
        },
        "certified_claims": claims,
        "authenticated_inputs": {
            str(AU2.relative_to(ROOT)): _sha256(AU2),
            str(SHARP.relative_to(ROOT)): _sha256(SHARP),
            str(TRIALS.relative_to(ROOT)): _sha256(TRIALS),
        },
        "source_sha256": {relative: _sha256(ROOT / relative) for relative in SOURCES},
        "claim_boundary": (
            "This is a direct completed-square V* bound for the authenticated "
            "positive-radius weak adjoint residual plus its loaded wall trace. "
            "The regular-origin master load is omitted, so this is not a full "
            "delta_z and cannot be used for exterior-response zero exclusion."
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
