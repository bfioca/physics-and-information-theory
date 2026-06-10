import pytest

from qgtoy.centrifugal_skyrmion_completed_stress import (
    centrifugal_quadrupole_conservation_residuals,
    centrifugal_quadrupole_stress_amplitudes,
    completed_stress_conservation_record,
)
from qgtoy.rigid_skyrmion_stress_conservation import (
    rigid_skyrmion_l2_stress_amplitudes,
)
from qgtoy.static_even_stress_conservation import (
    static_even_stress_conservation_residuals,
)


def test_zero_deformation_recovers_rigid_stress():
    record = centrifugal_quadrupole_stress_amplitudes(
        radius=1.2,
        metric_factor=0.95,
        profile=1.0,
        profile_derivative=-0.4,
        radial_field=0.0,
        radial_field_derivative=0.0,
        tangential_field=0.0,
        tangential_field_derivative=0.0,
        pion_mass=1.0,
    )
    for name in (
        "energy_density",
        "radial_pressure",
        "tangential_pressure",
        "radial_angular_shear",
        "angular_tracefree_stress",
    ):
        assert record[f"total_{name}"] == pytest.approx(record[f"rigid_{name}"])


def test_rigid_piece_matches_independent_certified_formula():
    values = {
        "radius": 1.2,
        "metric_factor": 0.95,
        "profile": 1.0,
        "profile_derivative": -0.4,
    }
    record = centrifugal_quadrupole_stress_amplitudes(
        **values,
        radial_field=0.0,
        radial_field_derivative=0.0,
        tangential_field=0.0,
        tangential_field_derivative=0.0,
        pion_mass=1.0,
    )
    independent = rigid_skyrmion_l2_stress_amplitudes(
        **values,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=1.0,
    )
    names = {
        "energy_density": "energy_density_coefficient",
        "radial_pressure": "radial_pressure_coefficient",
        "tangential_pressure": "tangential_pressure_coefficient",
        "radial_angular_shear": "radial_angular_shear_coefficient",
        "angular_tracefree_stress": ("angular_tracefree_stress_coefficient"),
    }
    for local_name, independent_name in names.items():
        assert record[f"rigid_{local_name}"] == pytest.approx(
            independent[independent_name]
        )


def test_tangential_field_generates_radial_angular_shear():
    record = centrifugal_quadrupole_stress_amplitudes(
        radius=1.2,
        metric_factor=0.95,
        profile=1.0,
        profile_derivative=-0.4,
        radial_field=0.1,
        radial_field_derivative=-0.05,
        tangential_field=0.2,
        tangential_field_derivative=0.3,
        pion_mass=1.0,
    )
    expected = {
        "deformation_energy_density": -0.21244251528621338,
        "deformation_radial_pressure": 0.17192301107463823,
        "deformation_tangential_pressure": -0.16713949849683274,
        "deformation_radial_angular_shear": 0.07598237431124184,
        "deformation_angular_tracefree_stress": 0.04698212998510756,
    }
    for name, value in expected.items():
        assert record[name] == pytest.approx(value, abs=1.0e-14)


def test_quadrupole_residual_uses_independent_static_even_gate():
    values = {
        "radius": 1.3,
        "metric_factor": 0.91,
        "metric_factor_derivative": -0.13,
        "energy_density": 0.7,
        "radial_pressure": -0.2,
        "radial_pressure_derivative": 0.11,
        "tangential_pressure": 0.31,
        "radial_angular_shear": -0.04,
        "radial_angular_shear_derivative": 0.03,
        "angular_tracefree_stress": 0.08,
    }
    specialized = centrifugal_quadrupole_conservation_residuals(**values)
    independent = static_even_stress_conservation_residuals(ell=2, **values)
    assert specialized["radial_conservation_residual"] == pytest.approx(
        independent["radial_conservation_residual"]
    )
    assert specialized["angular_conservation_residual"] == pytest.approx(
        independent["angular_conservation_residual"]
    )


def test_completed_default_stress_reduces_conservation_residual():
    record = completed_stress_conservation_record(node_count=201)
    assert record["bulk_conservation_is_numerically_improved"]
    assert record["residual_reduction_factor"] < 0.02


def test_completed_conservation_residual_converges_at_second_order():
    coarse = completed_stress_conservation_record(node_count=101)
    fine = completed_stress_conservation_record(node_count=201)
    assert fine["completed_radial_residual_maximum"] < (
        0.35 * coarse["completed_radial_residual_maximum"]
    )
    assert fine["completed_angular_residual_maximum"] < (
        0.35 * coarse["completed_angular_residual_maximum"]
    )


@pytest.mark.parametrize(
    "kwargs",
    (
        {"radius": 0.0},
        {"metric_factor": 0.0},
        {"pion_mass": -1.0},
    ),
)
def test_stress_amplitudes_reject_invalid_parameters(kwargs):
    values = {
        "radius": 1.0,
        "metric_factor": 0.95,
        "profile": 1.0,
        "profile_derivative": -0.4,
        "radial_field": 0.1,
        "radial_field_derivative": 0.2,
        "tangential_field": 0.1,
        "tangential_field_derivative": -0.2,
        "pion_mass": 1.0,
    }
    values.update(kwargs)
    with pytest.raises(ValueError):
        centrifugal_quadrupole_stress_amplitudes(**values)
