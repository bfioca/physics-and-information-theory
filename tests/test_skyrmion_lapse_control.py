import pytest

from qgtoy.skyrmion_lapse_control import (
    skyrmion_dimensionless_enthalpy,
    skyrmion_enthalpy_identity,
    static_bulk_lapse_metric_record,
)


def test_static_skyrmion_enthalpy_identity() -> None:
    parameters = {
        "radius": 1.25,
        "profile": 1.1,
        "derivative": -0.7,
        "curvature": 1.0 / 400.0,
    }
    direct = skyrmion_dimensionless_enthalpy(
        **parameters,
        pion_mass=1.0,
    )
    simplified = skyrmion_enthalpy_identity(**parameters)
    assert direct == pytest.approx(simplified)


def test_radial_budget_controls_static_bulk_lapse() -> None:
    record = static_bulk_lapse_metric_record(
        radial_metric_budget=0.5,
        lapse_coefficient_upper=35.0,
        radial_shape_upper=30.0,
    )
    assert record["maximum_log_lapse_drop"] == pytest.approx(7.0 / 12.0)
    assert 0.0 < record["minimum_gtt_magnitude_relative_to_de_sitter"] < 0.5


@pytest.mark.parametrize("budget", [0.0, 1.0])
def test_invalid_lapse_budget_is_rejected(budget) -> None:
    with pytest.raises(ValueError):
        static_bulk_lapse_metric_record(
            radial_metric_budget=budget,
            lapse_coefficient_upper=35.0,
            radial_shape_upper=30.0,
        )
