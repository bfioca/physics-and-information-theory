import pytest

from qgtoy.israel_junction_gate import (
    de_sitter_kottler_static_shell_benchmark,
    identical_geometry_pure_tension_no_go_record,
    linearized_constant_tension_israel_gate,
    pure_tension_spherical_israel_record,
    spherical_mixed_extrinsic_curvature,
)


def test_spherical_extrinsic_curvature_for_de_sitter() -> None:
    record = spherical_mixed_extrinsic_curvature(
        radius=2.0,
        lapse=0.75,
        lapse_derivative=-0.25,
    )
    assert record["temporal_mixed_extrinsic_curvature"] == pytest.approx(
        -(3.0**0.5) / 12.0
    )
    assert record["angular_mixed_extrinsic_curvature"] == pytest.approx(
        (3.0**0.5) / 4.0
    )


def test_identical_geometry_has_exact_positive_tension_obstruction() -> None:
    record = identical_geometry_pure_tension_no_go_record(
        radius=4.0,
        lapse=0.96,
        lapse_derivative=-0.02,
        surface_tension=0.003,
        gravitational_coupling=0.2,
    )
    assert record["temporal_extrinsic_curvature_jump"] == 0.0
    assert record["angular_extrinsic_curvature_jump"] == 0.0
    assert record["exact_reduced_obstruction"] == pytest.approx(0.0003)
    assert record["nonzero_tension_is_obstructed"] is True
    assert record["israel_matching_closes"] is False


@pytest.mark.parametrize("u", [0.34, 0.4, 0.5, 0.6, 0.66])
def test_exact_de_sitter_kottler_benchmark_closes_both_equations(u: float) -> None:
    record = de_sitter_kottler_static_shell_benchmark(
        radius=4.0,
        compact_radius_ratio_squared=u,
        gravitational_coupling=0.7,
    )
    assert record["outer_lapse_is_positive"] is True
    assert record["benchmark_closes"] is True
    assert record["israel"]["maximum_israel_residual"] < 1.0e-12


def test_reduced_and_tensor_equations_agree() -> None:
    benchmark = de_sitter_kottler_static_shell_benchmark(
        radius=3.0,
        compact_radius_ratio_squared=0.5,
        gravitational_coupling=1.0,
    )
    record = pure_tension_spherical_israel_record(
        radius=3.0,
        inner_lapse=benchmark["inner_lapse_at_wall"],
        inner_lapse_derivative=-1.0 / 3.0,
        outer_lapse=benchmark["outer_lapse_at_wall"],
        outer_lapse_derivative=(
            2.0 * benchmark["kottler_mass_length_GM"] / 9.0 - 1.0 / 3.0
        ),
        surface_tension=benchmark["surface_tension"],
        gravitational_coupling=1.0,
    )
    assert record["maximum_israel_residual"] < 2.0e-14


def test_linearized_gate_checks_all_six_tensorial_amplitudes() -> None:
    closed = linearized_constant_tension_israel_gate(
        inner_induced_metric_amplitudes=(1.0, 2.0, 3.0),
        outer_induced_metric_amplitudes=(1.0, 2.0, 3.0),
        inner_mixed_extrinsic_curvature_amplitudes=(4.0, 5.0, 6.0),
        outer_mixed_extrinsic_curvature_amplitudes=(4.0, 5.0, 6.0),
    )
    assert closed["tensorial_linearized_israel_matching_closes"] is True

    failed = linearized_constant_tension_israel_gate(
        inner_induced_metric_amplitudes=(1.0, 2.0, 3.0),
        outer_induced_metric_amplitudes=(1.0, 2.0, 3.0 + 1.0e-4),
        inner_mixed_extrinsic_curvature_amplitudes=(4.0, 5.0, 6.0),
        outer_mixed_extrinsic_curvature_amplitudes=(4.0, 5.0, 6.0),
    )
    assert failed["tensorial_linearized_israel_matching_closes"] is False
    assert failed["maximum_tensorial_junction_residual"] == pytest.approx(1.0e-4)


def test_invalid_benchmark_range_is_rejected() -> None:
    with pytest.raises(ValueError, match="must lie"):
        de_sitter_kottler_static_shell_benchmark(
            radius=4.0,
            compact_radius_ratio_squared=0.2,
        )
