import pytest

from qgtoy.spherical_static_patch_constraint import (
    concentrated_core_counterexample_record,
    de_sitter_static_factor,
    radial_metric_relative_distortion,
    spherical_constraint_margin_record,
    spherical_constraint_ratio,
    spherical_static_patch_constraint_certificate,
)


def test_constraint_ratio_and_metric_identity() -> None:
    ratio = spherical_constraint_ratio(
        0.1,
        0.5,
        static_patch_radius=1.0,
        newton_constant=1.0,
    )
    assert ratio == pytest.approx(8.0 / 15.0)
    assert radial_metric_relative_distortion(ratio) == pytest.approx(8.0 / 7.0)


def test_uniform_constraint_budget_controls_radial_metric() -> None:
    record = spherical_constraint_margin_record(0.2, control_budget=0.25)
    assert record["controlled_radial_metric"]
    assert record["areal_coordinate_horizon_excluded"]
    assert record["minimum_metric_factor_relative_to_de_sitter"] == pytest.approx(
        0.8
    )
    assert record["maximum_relative_radial_metric_distortion"] == pytest.approx(0.25)


def test_small_wall_compactness_can_hide_supercritical_core() -> None:
    record = concentrated_core_counterexample_record()
    assert record["wall_constraint_ratio"] < 0.02
    assert record["core_constraint_ratio"] > 1.0
    assert record["endpoint_compactness_fails_to_control_interior"]


def test_constraint_certificate_passes() -> None:
    certificate = spherical_static_patch_constraint_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())


@pytest.mark.parametrize(
    ("function", "kwargs"),
    [
        (de_sitter_static_factor, {"radius": 1.0, "static_patch_radius": 1.0}),
        (
            spherical_constraint_ratio,
            {
                "enclosed_mass": -1.0,
                "radius": 0.5,
                "static_patch_radius": 1.0,
                "newton_constant": 1.0,
            },
        ),
        (
            concentrated_core_counterexample_record,
            {"core_radius": 0.5, "support_radius": 0.5},
        ),
    ],
)
def test_invalid_constraint_inputs_are_rejected(function, kwargs) -> None:
    with pytest.raises(ValueError):
        function(**kwargs)
