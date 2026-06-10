import pytest

from qgtoy.centrifugal_skyrmion_master_adjoint import (
    centrifugal_master_adjoint_feasibility_record,
)


def test_floating_master_adjoint_product_has_nonzero_margin() -> None:
    record = centrifugal_master_adjoint_feasibility_record(
        coarse_node_count=9,
        quadrature_order=3,
        profile_step=0.004,
    )
    assert record["status"] == "pass"
    claims = record["verified_numerical_properties"]
    assert all(claims.values())
    estimator = record["dual_weighted_estimator"]
    assert estimator["residual_product_error_bound"] > 0.0
    assert estimator["floating_distance_from_zero_after_product_bound"] > 0.0
    assert estimator["actual_corrected_error_against_fine_system"] <= (
        estimator["residual_product_error_bound"] + 1.0e-12
    )


@pytest.mark.parametrize(
    ("name", "value", "message"),
    (
        ("coarse_node_count", 4, "at least 5"),
        ("refinement_factor", 1, "at least 2"),
        ("quadrature_order", 1, "at least 2"),
        ("profile_step", 0.0, "positive"),
    ),
)
def test_master_adjoint_rejects_invalid_inputs(
    name: str, value: int | float, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        centrifugal_master_adjoint_feasibility_record(**{name: value})
