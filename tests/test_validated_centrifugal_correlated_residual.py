import json
from fractions import Fraction
from pathlib import Path

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    rational_response_trial_pair_from_record,
    refine_rational_response_trial,
)
from qgtoy.validated_centrifugal_correlated_residual import (
    correlated_primal_residual_cells,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    reconstruct_validated_skyrmion_sharp_profile,
)


ROOT = Path(__file__).resolve().parents[1]


def test_correlated_primal_residual_improves_independent_box_bound() -> None:
    au2 = json.loads(
        (ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json").read_text()
    )
    sharp = json.loads(
        (ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json").read_text()
    )
    archive = json.loads(
        (ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json").read_text()
    )
    subdivisions = 1
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=subdivisions
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    primal = refine_rational_response_trial(
        pair.primal, subdivisions_per_cell=subdivisions
    )
    residuals = correlated_primal_residual_cells(profile, primal)
    assert len(residuals) == 43
    total = sum((cell.l2_squared_upper for cell in residuals), start=Fraction(0))
    assert total < Fraction(11, 1000), float(total)
