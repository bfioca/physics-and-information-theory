import pytest

from qgtoy.centrifugal_skyrmion_master_response import (
    centrifugal_skyrmion_master_response_record,
)


def test_default_master_response_is_finite_and_nonzero():
    record = centrifugal_skyrmion_master_response_record(node_count=201)
    distribution = record["master_source_distribution_over_kappa"]
    assert abs(distribution["master_source_delta_second_coefficient"]) > 0.0
    assert distribution["contact_free_delta_second_coefficient"] == 0.0
    assert record["bulk_master_source_maximum_absolute"] > 0.0
    assert all(
        abs(sample["total_master_response_over_kappa"]) > 0.0
        for sample in record["response_samples"]
    )


def test_master_response_is_mesh_stable_at_sample_points():
    coarse = centrifugal_skyrmion_master_response_record(node_count=101)
    fine = centrifugal_skyrmion_master_response_record(node_count=201)
    coarse_values = [
        sample["total_master_response_over_kappa"]
        for sample in coarse["response_samples"]
    ]
    fine_values = [
        sample["total_master_response_over_kappa"]
        for sample in fine["response_samples"]
    ]
    assert (
        max(
            abs(first - second) / max(1.0e-12, abs(second))
            for first, second in zip(coarse_values, fine_values, strict=True)
        )
        < 0.05
    )


@pytest.mark.parametrize(
    "kwargs",
    (
        {"node_count": 4},
        {"origin_radius": 0.0},
        {"profile_step": 0.0},
        {"observation_radii": (4.0,)},
        {"observation_radii": (20.0,)},
    ),
)
def test_master_response_rejects_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        centrifugal_skyrmion_master_response_record(**kwargs)
