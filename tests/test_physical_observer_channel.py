import hashlib
import json
from math import log, pi, sqrt
from pathlib import Path

import pytest

from qgtoy.physical_observer_channel import (
    finite_environment_decoherence_factor,
    harlow_pointer_channel_record,
    matched_two_region_control_record,
    minimum_environment_qubits_for_error,
    observer_action_resource_record,
    physical_observer_channel_certificate,
    pointer_environment_entropy_record,
    relational_patch_measurement_record,
    uniform_density_worldtube_backreaction_record,
)


ROOT = Path(__file__).resolve().parents[1]


def test_finite_environment_gives_exact_dephasing_factor_and_distance() -> None:
    coherence = finite_environment_decoherence_factor(
        4,
        environment_phase=pi / 3.0,
    )
    channel = harlow_pointer_channel_record(
        4,
        environment_phase=pi / 3.0,
    )
    assert coherence == pytest.approx(1.0 / 16.0)
    assert channel["diamond_norm_difference"] == pytest.approx(1.0 / 16.0)
    assert channel["normalized_diamond_distance"] == pytest.approx(1.0 / 32.0)
    assert channel[
        "premeasurement_instrument_normalized_diamond_distance"
    ] == pytest.approx(1.0 / 32.0)
    assert finite_environment_decoherence_factor(
        1,
        environment_phase=pi / 2.0,
    ) == 0.0


def test_environment_resource_law_inverts_the_channel_error() -> None:
    assert minimum_environment_qubits_for_error(
        1.0 / 32.0,
        environment_phase=pi / 3.0,
    ) == 4
    assert minimum_environment_qubits_for_error(
        0.0,
        environment_phase=pi / 2.0,
    ) == 1
    assert (
        minimum_environment_qubits_for_error(
            0.0,
            environment_phase=pi / 3.0,
        )
        is None
    )
    assert (
        minimum_environment_qubits_for_error(
            0.1,
            environment_phase=0.0,
        )
        is None
    )


def test_entropy_ledger_matches_binary_schmidt_spectrum() -> None:
    record = pointer_environment_entropy_record(
        4,
        environment_phase=pi / 3.0,
    )
    assert record["pointer_eigenvalues"] == pytest.approx((17.0 / 32.0, 15.0 / 32.0))
    assert record["pointer_purity"] == pytest.approx(257.0 / 512.0)
    assert record["pointer_second_renyi_entropy_nats"] == pytest.approx(
        -log(257.0 / 512.0)
    )
    assert record["environment_dimension"] == 16
    assert record["harlow_observer_entropy_identification"] == "not_made"


def test_action_prices_parallel_and_serial_schedules() -> None:
    record = observer_action_resource_record(
        4,
        acquisition_coupling=1.0,
        environment_coupling=1.0,
        environment_phase=pi / 3.0,
    )
    parallel = record["parallel_schedule"]
    serial = record["serial_two_body_schedule"]
    complexity = record["complexity"]
    assert isinstance(parallel, dict)
    assert isinstance(serial, dict)
    assert isinstance(complexity, dict)
    assert record["acquisition_duration_tau"] == pytest.approx(pi / 2.0)
    assert parallel["total_duration"] == pytest.approx(5.0 * pi / 6.0)
    assert parallel["peak_interaction_operator_norm"] == pytest.approx(4.0)
    assert serial["total_duration"] == pytest.approx(11.0 * pi / 6.0)
    assert serial["peak_interaction_operator_norm"] == pytest.approx(1.0)
    assert record["integrated_interaction_norm_both_schedules"] == pytest.approx(
        11.0 * pi / 6.0
    )
    assert complexity["two_body_gate_count_realized_branch"] == 5
    assert complexity["parallel_commuting_depth"] == 2


def test_relational_patch_is_sectorwise_local_and_swap_covariant() -> None:
    record = relational_patch_measurement_record()
    assert record["exact_binary_acquisition"]
    assert record["sectorwise_local"]
    assert record["simultaneous_A_B_swap_covariant"]
    assert "direct sum" in record["observer_location_space"]


def test_uniform_mass_profile_has_controlled_exact_constraint_ratio() -> None:
    record = uniform_density_worldtube_backreaction_record(
        mass_energy_envelope=7.0,
        support_radius=0.2,
        static_patch_radius=1.0,
        newton_constant=0.001,
        control_budget=0.25,
    )
    expected_ratio = 2.0 * 0.001 * 7.0 / (0.2 * 0.96)
    assert record["maximum_constraint_ratio_q"] == pytest.approx(expected_ratio)
    assert record["supremum_occurs_at_support_wall"]
    assert record["controlled_backreaction"]
    assert record["background_wall_redshift_sqrt_N"] == pytest.approx(sqrt(0.96))
    assert record["background_proper_energy_lower_bound"] == pytest.approx(7.0)
    assert record["background_proper_energy_upper_bound"] == pytest.approx(
        7.0 / sqrt(0.96)
    )


def test_matched_controls_separate_entanglement_from_connectivity() -> None:
    record = matched_two_region_control_record()
    matching = record["matching_conditions"]
    single = record["single_Z_setting"]
    witness = record["two_setting_entanglement_witness"]
    connectivity = record["connectivity_test"]
    assert isinstance(matching, dict)
    assert isinstance(single, dict)
    assert isinstance(witness, dict)
    assert isinstance(connectivity, dict)
    assert matching["identical_maximally_mixed_local_marginals"]
    assert matching["ZZ_record_distributions_identical"]
    assert single["entanglement_specific_contrast"] == pytest.approx(0.0)
    assert witness["entangled_value"] == pytest.approx(1.0)
    assert witness["matched_separable_value"] == pytest.approx(0.5)
    assert witness["entanglement_witness_gap"] == pytest.approx(0.5)
    assert not connectivity["connectivity_observable_defined_by_action"]
    assert not connectivity["nonzero_connectivity_contrast_survives"]


def test_default_certificate_retains_observer_theorem_and_stops_er_epr() -> None:
    certificate = physical_observer_channel_certificate()
    assert certificate["status"] == "pass_observer_channel_stop_er_epr"
    assert all(certificate["certified_observer_claims"].values())
    assert certificate["decision"]["observer_channel_theorem"] == "RETAIN"
    assert certificate["decision"]["er_epr_extension"] == (
        "STOP_NO_DERIVED_CONNECTIVITY_CONTRAST"
    )
    geometry = certificate["localization_and_backreaction_ledger"]
    assert "duration_ledger" in geometry


def test_frozen_certificate_authenticates_current_sources() -> None:
    path = ROOT / "experiments/physical_observer_channel_certificate.json"
    record = json.loads(path.read_text(encoding="ascii"))
    assert record["status"] == "pass_observer_channel_stop_er_epr"
    for relative, expected in record["source_sha256"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


@pytest.mark.parametrize(
    ("function", "kwargs"),
    [
        (
            finite_environment_decoherence_factor,
            {"environment_qubits": 0, "environment_phase": 0.1},
        ),
        (
            finite_environment_decoherence_factor,
            {"environment_qubits": 1, "environment_phase": pi},
        ),
        (
            minimum_environment_qubits_for_error,
            {
                "maximum_normalized_diamond_distance": 0.6,
                "environment_phase": 0.1,
            },
        ),
        (
            uniform_density_worldtube_backreaction_record,
            {
                "mass_energy_envelope": 1.0,
                "support_radius": 1.0,
                "static_patch_radius": 1.0,
                "newton_constant": 1.0,
                "control_budget": 0.25,
            },
        ),
    ],
)
def test_invalid_physical_observer_inputs_are_rejected(function, kwargs) -> None:
    with pytest.raises(ValueError):
        function(**kwargs)
