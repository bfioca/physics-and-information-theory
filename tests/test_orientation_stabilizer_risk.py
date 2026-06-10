from math import pi

import pytest

from qgtoy.orientation_stabilizer_risk import (
    half_turn_stabilizer_risk_lower_bound,
    orientation_stabilizer_risk_certificate,
    spin_two_anticoherent_stabilizer_record,
    stabilizer_chordal_risk_lower_bound,
)


def test_general_stabilizer_floor_endpoints_and_monotonicity() -> None:
    angles = tuple(index * pi / 20.0 for index in range(21))
    floors = tuple(stabilizer_chordal_risk_lower_bound(angle) for angle in angles)
    assert floors[0] == 0.0
    assert floors[-1] == pytest.approx(0.5)
    assert all(left <= right for left, right in zip(floors, floors[1:]))


def test_half_turn_floor_is_exact() -> None:
    assert half_turn_stabilizer_risk_lower_bound().numerator == 1
    assert half_turn_stabilizer_risk_lower_bound().denominator == 2


def test_spin_two_anticoherent_state_has_global_ambiguity() -> None:
    record = spin_two_anticoherent_stabilizer_record()
    assert record["occupied_magnetic_labels"] == (-2, 0, 2)
    assert record["z_half_turn_phases"] == (1, 1, 1)
    assert record["density_operator_is_half_turn_invariant"]
    assert record["local_qfi_rank"] == 3
    assert record["leading_spin_two_stress_vanishes"]
    assert record["global_chordal_risk_lower_bound_exact"] == "1/2"


def test_certificate_passes() -> None:
    certificate = orientation_stabilizer_risk_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())


@pytest.mark.parametrize("angle", (-1.0, pi + 1.0e-6, float("inf")))
def test_invalid_rotation_angle_is_rejected(angle: float) -> None:
    with pytest.raises(ValueError):
        stabilizer_chordal_risk_lower_bound(angle)
