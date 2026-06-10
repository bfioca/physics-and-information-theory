from math import sqrt

import pytest

from qgtoy.static_patch_l2_weyl_reconstruction import (
    direct_rw_radial_electric_weyl_coefficient,
    horizon_regular_l2_weyl_record,
    physical_skyrmion_exterior_weyl_record,
    vacuum_l2_rw_reconstruction_record,
)


def _pure_density(state):
    return tuple(
        tuple(left * right.conjugate() for right in state) for left in state
    )


def _spin_two_cat_density():
    return _pure_density((1.0 / sqrt(2.0), 0.0, 0.0, 0.0, 1.0 / sqrt(2.0)))


def test_vacuum_master_reconstructs_rw_metric_and_einstein_constraints():
    record = horizon_regular_l2_weyl_record(
        radius=6.0,
        static_patch_radius=20.0,
        exterior_master_amplitude=-0.1,
    )
    assert record["master_roundtrip_error"] == pytest.approx(0.0, abs=2.0e-16)
    assert record["radial_angular_einstein_residual"] == pytest.approx(
        0.0, abs=2.0e-16
    )
    assert record["radial_einstein_residual"] == pytest.approx(0.0, abs=2.0e-16)
    assert record["radial_electric_weyl_coefficient"] == pytest.approx(
        -6.0 * record["master_field"] / 6.0**3
    )


def test_direct_metric_curvature_matches_master_weyl_identity():
    radius = 7.0
    patch = 20.0
    amplitude = 0.13
    step = 1.0e-4

    def temporal(point):
        return horizon_regular_l2_weyl_record(
            radius=point,
            static_patch_radius=patch,
            exterior_master_amplitude=amplitude,
        )["temporal_metric_amplitude_H0"]

    center = temporal(radius)
    plus = temporal(radius + step)
    minus = temporal(radius - step)
    direct = direct_rw_radial_electric_weyl_coefficient(
        radius=radius,
        static_patch_radius=patch,
        temporal_metric_amplitude=center,
        temporal_metric_amplitude_derivative=(plus - minus) / (2.0 * step),
        temporal_metric_amplitude_second_derivative=(plus - 2.0 * center + minus)
        / step**2,
    )
    expected = horizon_regular_l2_weyl_record(
        radius=radius,
        static_patch_radius=patch,
        exterior_master_amplitude=amplitude,
    )["radial_electric_weyl_coefficient"]
    assert direct == pytest.approx(expected, rel=2.0e-6)


def test_general_vacuum_reconstruction_accepts_master_jet():
    record = vacuum_l2_rw_reconstruction_record(
        radius=5.0,
        static_patch_radius=20.0,
        master_field=-0.06,
        master_field_derivative=0.01,
    )
    assert record["temporal_metric_amplitude_H0"] == pytest.approx(-0.026)
    assert record["radial_metric_amplitude_H2"] == pytest.approx(-0.026)
    assert record["radial_electric_weyl_coefficient"] == pytest.approx(0.00288)


def test_completed_skyrmion_has_nonzero_exterior_tidal_curvature():
    record = physical_skyrmion_exterior_weyl_record(
        skyrme_coupling=1.0,
        pion_decay_constant=1.0,
        newton_constant=1.0e-6,
        spin=2.0,
        state_density_matrix=_spin_two_cat_density(),
        node_count=101,
        maximum_slow_rotation=0.1,
    )
    assert record["exterior_master_amplitude_spread"] < 1.0e-14
    assert all(
        sample["physical_radial_electric_weyl_angular_rms"] > 0.0
        for sample in record["response_samples"]
    )


@pytest.mark.parametrize(
    "kwargs",
    (
        {"radius": 0.0},
        {"radius": 20.0},
        {"static_patch_radius": 0.0},
        {"master_field": float("nan")},
    ),
)
def test_vacuum_reconstruction_rejects_invalid_inputs(kwargs):
    values = {
        "radius": 5.0,
        "static_patch_radius": 20.0,
        "master_field": 0.1,
        "master_field_derivative": 0.02,
    }
    values.update(kwargs)
    with pytest.raises(ValueError):
        vacuum_l2_rw_reconstruction_record(**values)
