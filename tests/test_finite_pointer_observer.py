import hashlib
import json
from math import cosh, exp, log, tanh
from pathlib import Path

import pytest

from qgtoy.finite_pointer_observer import (
    branchwise_gravity_renyi_bound,
    classical_pointer_purity,
    conditional_profile_energy_record,
    finite_pointer_cost_composition_record,
    finite_pointer_dephasing_record,
    finite_pointer_observer_certificate,
    finite_pointer_renyi_bound,
    harlow_orthogonal_code_fluctuation_record,
    renyi_two_entropy_from_purity,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "experiments" / "finite_pointer_observer_certificate.json"
CLEAN_ROOM = (
    ROOT / "experiments" / "finite_pointer_observer_clean_room_check.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_finite_pointer_channel_reproduces_binary_normalization() -> None:
    record = finite_pointer_dephasing_record(
        (0.5, 0.5),
        ((-2.0,), (2.0,)),
        ((0.75,),),
    )
    gamma = record["pairwise_dephasing_exponents"]
    assert gamma[0][0] == 0.0
    assert gamma[1][1] == 0.0
    assert gamma[0][1] == pytest.approx(3.0)
    assert record["gram_magnitudes"][0][1] == pytest.approx(exp(-3.0))
    assert record["physical_pointer_purity"] == pytest.approx(
        0.5 + 0.5 * exp(-6.0)
    )


def test_pairwise_variance_and_centering_identities_are_exact() -> None:
    record = conditional_profile_energy_record(
        (0.5, 0.3, 0.2),
        ((-1.0, 2.0), (0.5, -0.5), (3.0, 1.0)),
    )
    assert record["pairwise_squared_distance_average"] == pytest.approx(
        record["pairwise_variance_identity_rhs"]
    )
    assert record["centered_energy_Ebar"] == pytest.approx(
        record["centering_identity_rhs"]
    )
    assert record["centered_energy_Ebar"] <= record["mean_branch_energy"]


def test_common_displacement_changes_absolute_energy_but_not_channel_or_ebar() -> None:
    weights = (0.5, 0.3, 0.2)
    profiles = ((-1.0, 0.0), (0.5, 0.0), (2.0, 0.0))
    shifted = tuple((left + 7.0, right - 4.0) for left, right in profiles)
    covariance = ((1.0, 0.0), (0.0, 0.25))
    original_channel = finite_pointer_dephasing_record(
        weights,
        profiles,
        covariance,
    )
    shifted_channel = finite_pointer_dephasing_record(
        weights,
        shifted,
        covariance,
    )
    original_energy = conditional_profile_energy_record(weights, profiles)
    shifted_energy = conditional_profile_energy_record(weights, shifted)
    for shifted_row, original_row in zip(
        shifted_channel["pairwise_dephasing_exponents"],
        original_channel["pairwise_dephasing_exponents"],
        strict=True,
    ):
        assert shifted_row == pytest.approx(original_row)
    assert shifted_channel["physical_pointer_purity"] == pytest.approx(
        original_channel["physical_pointer_purity"]
    )
    assert shifted_energy["centered_energy_Ebar"] == pytest.approx(
        original_energy["centered_energy_Ebar"]
    )
    assert shifted_energy["mean_branch_energy"] > original_energy[
        "mean_branch_energy"
    ]


def test_finite_pointer_renyi_bound_holds_for_a_three_state_channel() -> None:
    record = finite_pointer_cost_composition_record(
        (0.5, 0.3, 0.2),
        ((-1.0, 0.0), (0.5, 0.0), (2.0, 0.0)),
        ((1.0, 0.0), (0.0, 0.25)),
        cost_coefficient=2.0,
    )
    assert record["pairwise_cost_bound_holds"]
    assert record["purity_bound_holds"]
    assert record["renyi_bound_holds"]
    bound = record["renyi_bound"]
    assert bound["physical_renyi_upper_bound"] <= bound[
        "simplified_renyi_upper_bound"
    ]
    assert record["channel"]["physical_pointer_purity"] > bound[
        "physical_purity_lower_bound"
    ]


def test_binary_top_mode_saturates_the_jensen_bound() -> None:
    record = finite_pointer_cost_composition_record(
        (0.5, 0.5),
        ((-1.0,), (1.0,)),
        ((1.0,),),
        cost_coefficient=2.0,
    )
    assert record["channel"]["physical_pointer_purity"] == pytest.approx(
        record["renyi_bound"]["physical_purity_lower_bound"]
    )
    assert record["channel"]["physical_pointer_renyi_two"] == pytest.approx(
        record["renyi_bound"]["physical_renyi_upper_bound"]
    )


def test_zero_energy_and_deterministic_pointer_limits_are_regular() -> None:
    mixed = finite_pointer_renyi_bound(
        (0.5, 0.3, 0.2),
        centered_field_energy=0.0,
        cost_coefficient=3.0,
    )
    assert mixed["physical_purity_lower_bound"] == pytest.approx(1.0)
    assert mixed["physical_renyi_upper_bound"] == pytest.approx(0.0)
    deterministic = finite_pointer_renyi_bound(
        (1.0, 0.0),
        centered_field_energy=100.0,
        cost_coefficient=3.0,
    )
    assert deterministic["physical_purity_lower_bound"] == pytest.approx(1.0)
    assert deterministic["physical_renyi_upper_bound"] == pytest.approx(0.0)


def test_harlow_insertion_gives_exact_orthogonal_state_fluctuation_floor() -> None:
    purity = 0.07
    lower = 0.05
    dimension = 998
    record = harlow_orthogonal_code_fluctuation_record(
        observer_purity=purity,
        observer_purity_lower_bound=lower,
        encoding_dimension=dimension,
    )
    factor = dimension / (dimension + 2.0)
    assert record["exact_orthogonal_state_mean_square_fluctuation"] == pytest.approx(
        factor * purity
    )
    assert record["certified_mean_square_fluctuation_floor"] == pytest.approx(
        factor * lower
    )
    assert record["gate_three_closed"]
    assert "Haar-ensemble" in record["scope"]


def test_branchwise_gravity_bound_has_area_scaling_and_correct_lapse() -> None:
    y = 1.0
    cost = 1.0295979905445
    delta = 0.25
    radius = 3.0
    newton = 2.0e-5
    record = branchwise_gravity_renyi_bound(
        support_ratio=y,
        dimensionless_cost_coefficient=cost,
        maximum_constraint_ratio=delta,
        static_patch_radius=radius,
        newton_constant=newton,
    )
    expected_coefficient = 0.5 * cost * tanh(y) / cosh(y) ** 2
    assert record["de_sitter_N_at_b"] == pytest.approx(1.0 / cosh(y) ** 2)
    assert record["dimensionless_area_coefficient"] == pytest.approx(
        expected_coefficient
    )
    assert expected_coefficient == pytest.approx(0.1646584608126553)
    assert record["observer_renyi_upper_bound"] == pytest.approx(
        delta * radius**2 * expected_coefficient / newton
    )
    assert "Every conditional" in record["branchwise_hypothesis"]
    assert "not rederived" in record["scope"]


def test_four_gate_algebra_certificate_passes_with_explicit_boundaries() -> None:
    certificate = finite_pointer_observer_certificate()
    assert certificate["status"] == "pass_four_gate_algebra"
    assert all(certificate["certified_claims"].values())
    assert "General-d global sharpness" in certificate["claim_boundary"]
    assert "not certified" in certificate["claim_boundary"]


def test_frozen_four_gate_certificate_is_source_bound() -> None:
    record = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    assert record["status"] == "pass_four_gate_algebra"
    assert all(record["certified_claims"].values())
    for relative, expected in record["source_sha256"].items():
        assert _sha256(ROOT / relative) == expected


def test_independent_four_gate_replay_passes_and_is_source_bound() -> None:
    record = json.loads(CLEAN_ROOM.read_text(encoding="ascii"))
    assert record["status"] == "pass_independent_computation_nonrigorous"
    assert record["case_count"] == 64
    checks = record["checks"]
    assert checks["all_pairwise_cost_bounds_hold"]
    assert checks["all_purity_bounds_hold"]
    assert checks["all_entropy_bounds_hold"]
    assert checks["binary_bound_saturates"]
    assert checks["harlow_floor_below_exact_fluctuation"]
    assert checks["branchwise_budget_controls_weighted_energy"]
    assert checks["rigorous_area_coefficient_dominates_numerical"]
    assert checks["maximum_pairwise_identity_error"] < 1.0e-12
    for relative, expected in record["source_sha256"].items():
        assert _sha256(ROOT / relative) == expected


@pytest.mark.parametrize(
    ("function", "kwargs"),
    (
        (classical_pointer_purity, {"weights": ()}),
        (classical_pointer_purity, {"weights": (0.2, 0.2)}),
        (renyi_two_entropy_from_purity, {"purity": 0.0}),
        (
            finite_pointer_renyi_bound,
            {
                "weights": (0.5, 0.5),
                "centered_field_energy": -1.0,
                "cost_coefficient": 2.0,
            },
        ),
        (
            harlow_orthogonal_code_fluctuation_record,
            {
                "observer_purity": 0.1,
                "observer_purity_lower_bound": 0.2,
                "encoding_dimension": 10,
            },
        ),
        (
            branchwise_gravity_renyi_bound,
            {
                "support_ratio": 1.0,
                "dimensionless_cost_coefficient": 1.0,
                "maximum_constraint_ratio": 1.0,
                "static_patch_radius": 1.0,
                "newton_constant": 1.0,
            },
        ),
    ),
)
def test_invalid_finite_pointer_inputs_are_rejected(function, kwargs) -> None:
    with pytest.raises(ValueError):
        function(**kwargs)


def test_entropy_bound_is_never_weaker_than_basic_limits() -> None:
    weights = (0.4, 0.3, 0.2, 0.1)
    record = finite_pointer_renyi_bound(
        weights,
        centered_field_energy=0.4,
        cost_coefficient=1.7,
    )
    assert record["physical_renyi_upper_bound"] <= -log(
        classical_pointer_purity(weights)
    )
    assert record["physical_renyi_upper_bound"] <= 1.7 * 0.4
