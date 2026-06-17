import json
from math import isclose, log
from pathlib import Path

import pytest

from qgtoy.information_exposure_control import (
    SO3_HAAR_RANDOM_RISK,
    finite_entropy_continuity_envelope,
    finite_record_ksw_control_record,
    inverse_finite_entropy_continuity_envelope,
    ksw_channel_recovery_error_lower_bound,
    ksw_postselected_channel_recovery_error_lower_bound,
    marvian_spekkens_pure_orbit_recovery_floor,
    postselected_unconditional_risk,
    redundant_transfer_recovery_error_upper_bound,
    symmetric_subspace_dimension,
    universal_cloner_global_recovery_fidelity,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "experiments" / "information_exposure_small_spin_sdp.json"


def test_ksw_direct_risk_control_and_postselection() -> None:
    assert ksw_channel_recovery_error_lower_bound(0.75) == 0.0
    assert ksw_channel_recovery_error_lower_bound(0.5) == 0.25**2
    unconditional = postselected_unconditional_risk(
        success_probability=0.2,
        success_risk=0.25,
    )
    assert isclose(unconditional, 0.65)
    assert isclose(
        ksw_postselected_channel_recovery_error_lower_bound(
            success_probability=0.2,
            success_risk=0.25,
        ),
        (0.2 * (0.75 - 0.25)) ** 2,
    )


@pytest.mark.parametrize("dimension", (2, 4, 10))
@pytest.mark.parametrize("distance", (1e-6, 0.01, 0.1, 0.25))
def test_finite_entropy_envelope_inverse(dimension: int, distance: float) -> None:
    information = finite_entropy_continuity_envelope(distance, dimension)
    recovered = inverse_finite_entropy_continuity_envelope(
        information,
        dimension,
    )
    assert recovered <= distance + 1e-10
    assert isclose(
        finite_entropy_continuity_envelope(recovered, dimension),
        information,
        rel_tol=1e-10,
        abs_tol=1e-10,
    )


def test_finite_record_control_detects_dimension_incompatibility() -> None:
    record = finite_record_ksw_control_record(
        record_risk=0.1,
        record_dimension=2,
        information_lower_bound_nats=log(2.0) + 0.01,
    )
    assert record["finite_record_excluded"] is True
    assert record["combined_diamond_error_floor"] == float("inf")


def test_pure_orbit_control_is_positive_below_random_risk() -> None:
    assert (
        marvian_spekkens_pure_orbit_recovery_floor(
            record_risk=SO3_HAAR_RANDOM_RISK,
            minimum_source_orbit_fidelity=0.5,
        )
        == 0.0
    )
    assert (
        marvian_spekkens_pure_orbit_recovery_floor(
            record_risk=0.6,
            minimum_source_orbit_fidelity=0.5,
        )
        > 0.0
    )


def test_redundant_transfer_defeats_capacity_independent_floor() -> None:
    errors = [
        redundant_transfer_recovery_error_upper_bound(
            state_dimension=4,
            retained_copies=scale**2,
            transferred_copies=scale,
        )
        for scale in (4, 8, 16, 32)
    ]
    assert all(left > right for left, right in zip(errors, errors[1:]))
    assert errors[-1] < 0.1


def test_universal_cloner_dimension_formula() -> None:
    assert symmetric_subspace_dimension(2, 3) == 4
    assert universal_cloner_global_recovery_fidelity(
        state_dimension=2,
        input_copies=2,
        output_copies=3,
    ) == 3 / 4


def test_small_spin_sdp_record() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    assert record["schema"] == "information-exposure-small-spin-sdp-v1"
    assert record["model"]["group"] == "SO(3)"
    assert record["model"]["orbit_stabilizer"] == "trivial"
    assert record["model"]["koashi_imoto_nondisturbing_information_nats"] == 0.0
    assert record["model"]["minimum_source_orbit_fidelity"] == 0.0

    diagnostics = record["quadrature_diagnostics"]
    assert max(diagnostics.values()) < 1e-12

    endpoints = record["endpoints"]
    minimum = endpoints["minimum_record_risk"]
    identity = endpoints["identity_source_channel"]
    assert isclose(minimum["risk"], 0.53794331, rel_tol=0.0, abs_tol=2e-7)
    assert isclose(minimum["optimal_orbit_recovery_infidelity"], 0.75, abs_tol=2e-7)
    assert isclose(identity["risk"], 0.75, abs_tol=2e-7)
    assert identity["optimal_orbit_recovery_infidelity"] < 2e-7
    assert isclose(endpoints["single_marker_full_frame_risk"], 2 / 3)

    for point in record["frontier"]:
        assert point["status"] in {"optimal", "optimal_inaccurate"}
        assert point["risk_ceiling_violation"] < 2e-7
        assert point["trace_preserving_max_error"] < 2e-7
        assert point["minimum_seed_eigenvalue"] > -2e-7
        assert point["optimal_orbit_recovery_infidelity"] >= (
            point["marvian_spekkens_control_floor"]
        )
        assert point["marvian_spekkens_control_floor"] == 0.0
        assert point["optimal_orbit_recovery_infidelity"] < (
            point["generic_u4_cloner_infidelity"]
        )

    assert "KNOWN-FRAMEWORK SPECIALIZATION" in (
        record["novelty_audit"]["verdict"]
    )
