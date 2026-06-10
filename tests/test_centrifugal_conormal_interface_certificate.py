import json
from pathlib import Path

import pytest

from qgtoy.centrifugal_conormal_interface_certificate import (
    certify_internal_conormal_cancellation,
)
from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    rational_response_trial_pair_from_record,
    refine_rational_response_trial,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    reconstruct_validated_skyrmion_sharp_profile,
)


ROOT = Path(__file__).resolve().parents[1]


def _inputs(subdivisions: int = 8):
    au2 = json.loads(
        (ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json").read_text(
            encoding="ascii"
        )
    )
    sharp = json.loads(
        (ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json").read_text(
            encoding="ascii"
        )
    )
    archive = json.loads(
        (ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json").read_text(
            encoding="ascii"
        )
    )
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=subdivisions
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    primal = refine_rational_response_trial(
        pair.primal, subdivisions_per_cell=subdivisions
    )
    return profile, primal


def test_exact_internal_conormal_cancellation() -> None:
    profile, primal = _inputs()
    certificate = certify_internal_conormal_cancellation(profile, primal)
    assert certificate.interface_count == 344
    assert certificate.origin_join_is_c1
    assert certificate.positive_radius_trial_is_c1
    assert certificate.profile_is_one_global_c1_solution
    assert certificate.coefficient_map_uses_only_profile_value_and_first_derivative
    assert certificate.internal_conormal_jump_is_exactly_zero


def test_partition_mismatch_is_rejected() -> None:
    profile, _ = _inputs()
    _, primal = _inputs(subdivisions=4)
    with pytest.raises(ValueError, match="partitions differ"):
        certify_internal_conormal_cancellation(profile, primal)
