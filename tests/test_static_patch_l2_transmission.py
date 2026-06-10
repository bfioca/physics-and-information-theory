import pytest

from qgtoy.centrifugal_skyrmion_master_response import (
    centrifugal_skyrmion_master_response_record,
)
from qgtoy.static_patch_l2_transmission import (
    l2_green_wall_transmission_record,
    l2_master_distribution_transmission_record,
)


def test_literal_distribution_recomposes_from_contact_and_jumps():
    record = l2_master_distribution_transmission_record(
        wall_radius=4.0,
        static_patch_radius=20.0,
        delta_coefficient=-0.0018179198616,
        delta_prime_coefficient=0.0024220397459,
        delta_second_coefficient=-0.0013923102731,
    )
    assert record["distribution_recomposition_maximum_error"] < 1.0e-18
    assert record["off_wall_master_field_jump"] < 0.0
    assert record["off_wall_master_flux_jump"] > 0.0


def test_green_limits_realize_exact_transmission_conditions():
    record = l2_green_wall_transmission_record(
        wall_radius=4.0,
        static_patch_radius=20.0,
        contact_free_delta_coefficient=-0.0023617910621,
        contact_free_delta_prime_coefficient=0.0024510462099,
    )
    assert record["field_jump_error"] == pytest.approx(0.0, abs=2.0e-16)
    assert record["flux_jump_error"] == pytest.approx(0.0, abs=2.0e-16)


def test_completed_skyrmion_shell_obeys_master_transmission_law():
    response = centrifugal_skyrmion_master_response_record(node_count=201)
    source = response["master_source_distribution_over_kappa"]
    distribution = l2_master_distribution_transmission_record(
        wall_radius=4.0,
        static_patch_radius=20.0,
        delta_coefficient=source["master_source_delta_coefficient"],
        delta_prime_coefficient=source["master_source_delta_prime_coefficient"],
        delta_second_coefficient=source[
            "master_source_delta_second_coefficient"
        ],
    )
    green = l2_green_wall_transmission_record(
        wall_radius=4.0,
        static_patch_radius=20.0,
        contact_free_delta_coefficient=source["contact_free_delta_coefficient"],
        contact_free_delta_prime_coefficient=source[
            "contact_free_delta_prime_coefficient"
        ],
    )
    assert distribution["distribution_recomposition_maximum_error"] < 1.0e-18
    assert green["off_wall_master_field_jump"] == pytest.approx(
        distribution["off_wall_master_field_jump"], abs=2.0e-16
    )
    assert green["off_wall_master_flux_jump"] == pytest.approx(
        distribution["off_wall_master_flux_jump"], abs=2.0e-16
    )


@pytest.mark.parametrize(
    "kwargs",
    (
        {"wall_radius": 0.0},
        {"wall_radius": 20.0},
        {"static_patch_radius": 0.0},
        {"delta_coefficient": float("nan")},
    ),
)
def test_transmission_rejects_invalid_inputs(kwargs):
    values = {
        "wall_radius": 4.0,
        "static_patch_radius": 20.0,
        "delta_coefficient": 0.1,
        "delta_prime_coefficient": 0.2,
        "delta_second_coefficient": 0.3,
    }
    values.update(kwargs)
    with pytest.raises(ValueError):
        l2_master_distribution_transmission_record(**values)
