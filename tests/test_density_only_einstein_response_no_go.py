from math import pi

import pytest

from qgtoy.density_only_einstein_response_no_go import (
    density_only_curvature_counterexample_record,
    density_only_einstein_response_no_go_certificate,
    pure_gauge_metric_norm_no_go_record,
)


def test_pure_gauge_metric_norm_is_unbounded_at_zero_source() -> None:
    small = pure_gauge_metric_norm_no_go_record(1.0)
    large = pure_gauge_metric_norm_no_go_record(100.0)
    assert small["linearized_einstein_source_norm"] == 0.0
    assert large["linearized_einstein_source_norm"] == 0.0
    assert large["coordinate_metric_component_scale"] == 100.0


def test_conserved_spatial_stress_has_zero_density_and_nonzero_curvature() -> None:
    record = density_only_curvature_counterexample_record(
        stress_amplitude=2.0,
        potential_laplacian=3.0,
        newton_constant=0.5,
    )
    assert record["energy_density_norm"] == 0.0
    assert record["four_divergence_vanishes"]
    assert record["spatial_stress_trace"] == 12.0
    assert record["linearized_scalar_curvature"] == pytest.approx(-48.0 * pi)
    assert record["nonzero_curvature_at_zero_energy_density"]


def test_stress_scaling_is_uncontrolled_by_energy_density() -> None:
    first = density_only_curvature_counterexample_record(
        stress_amplitude=1.0,
        potential_laplacian=-4.0,
        newton_constant=1.0,
    )
    second = density_only_curvature_counterexample_record(
        stress_amplitude=7.0,
        potential_laplacian=-4.0,
        newton_constant=1.0,
    )
    assert first["energy_density_norm"] == second["energy_density_norm"] == 0.0
    assert second["linearized_scalar_curvature"] == pytest.approx(
        7.0 * first["linearized_scalar_curvature"]
    )


def test_certificate_passes() -> None:
    certificate = density_only_einstein_response_no_go_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())


@pytest.mark.parametrize(
    ("keyword", "value"),
    (("stress_amplitude", float("inf")), ("newton_constant", 0.0)),
)
def test_invalid_counterexample_inputs_are_rejected(keyword: str, value: float) -> None:
    arguments = {
        "stress_amplitude": 1.0,
        "potential_laplacian": 1.0,
        "newton_constant": 1.0,
    }
    arguments[keyword] = value
    with pytest.raises(ValueError):
        density_only_curvature_counterexample_record(**arguments)
