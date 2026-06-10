import pytest

from qgtoy.centrifugal_skyrmion_membrane_stress import (
    default_membrane_distributional_conservation_record,
    distributional_wall_conservation_coefficients,
    pure_tension_shell_divergence_coefficients,
    pure_tension_shell_singular_amplitudes,
)


def test_moving_pure_tension_shell_has_required_delta_prime_pair():
    record = pure_tension_shell_singular_amplitudes(
        wall_radius=2.0,
        wall_metric_factor=0.8,
        wall_metric_factor_derivative=-0.1,
        membrane_tension=0.03,
        wall_displacement_coefficient=0.2,
    )
    assert record["energy_density_delta_prime"] == pytest.approx(
        record["radial_angular_shear_delta"]
    )
    assert record["tangential_pressure_delta_prime"] == pytest.approx(
        -record["energy_density_delta_prime"]
    )
    assert record["radial_pressure_delta"] == 0.0
    assert record["angular_tracefree_stress_delta"] == 0.0


def test_shell_divergence_is_exactly_the_curvature_force():
    record = pure_tension_shell_divergence_coefficients(
        ell=2,
        wall_radius=2.0,
        wall_metric_factor=0.8,
        wall_metric_factor_derivative=-0.1,
        wall_metric_factor_second_derivative=-0.05,
        membrane_tension=0.03,
        wall_displacement_coefficient=0.2,
    )
    assert record["curvature_factorization_maximum_error"] < 1.0e-16
    assert record["radial_delta_prime_coefficient"] == pytest.approx(
        record["expected_radial_delta_prime_coefficient"]
    )
    assert record["radial_delta_coefficient"] == pytest.approx(
        record["expected_radial_delta_coefficient"]
    )
    assert record["angular_delta_coefficient"] == pytest.approx(
        record["expected_angular_delta_coefficient"]
    )


def test_distributional_identity_factorizes_into_wall_force_balances():
    radius = 2.0
    lapse = 0.8
    lapse_derivative = -0.1
    lapse_second_derivative = -0.05
    tension = 0.03
    displacement = 0.2
    root_lapse = lapse**0.5
    mean_curvature = 2.0 * root_lapse / radius + lapse_derivative / (2.0 * root_lapse)
    radial = tension * mean_curvature
    energy = 0.4
    tangential = -0.05
    connection = lapse_derivative / (2.0 * lapse)
    radial_derivative = -(
        connection * (energy + radial) + 2.0 * (radial - tangential) / radius
    )
    mean_curvature_derivative = (
        lapse_derivative / (root_lapse * radius)
        - 2.0 * root_lapse / radius**2
        + lapse_second_derivative / (2.0 * root_lapse)
        - lapse_derivative**2 / (4.0 * lapse**1.5)
    )
    shape = mean_curvature_derivative + 6.0 / (radius**2 * root_lapse)
    intrinsic_radial = (
        -displacement * radial_derivative + tension * shape * displacement
    )
    intrinsic_shear = displacement * (tangential - radial)
    record = distributional_wall_conservation_coefficients(
        ell=2,
        wall_radius=radius,
        wall_metric_factor=lapse,
        wall_metric_factor_derivative=lapse_derivative,
        wall_metric_factor_second_derivative=lapse_second_derivative,
        membrane_tension=tension,
        wall_displacement_coefficient=displacement,
        background_energy_density=energy,
        background_radial_pressure=radial,
        background_radial_pressure_derivative=radial_derivative,
        background_tangential_pressure=tangential,
        intrinsic_radial_pressure_multipole=intrinsic_radial,
        intrinsic_radial_angular_shear_multipole=intrinsic_shear,
    )
    assert record["factorization_maximum_error"] < 1.0e-15
    assert record["maximum_distributional_conservation_coefficient"] < 1.0e-15
    assert record["distributional_conservation_closes"]


def test_default_membrane_closes_bulk_plus_shell_distribution():
    record = default_membrane_distributional_conservation_record(node_count=201)
    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())


@pytest.mark.parametrize(
    "kwargs",
    (
        {"ell": 1},
        {"wall_radius": 0.0},
        {"wall_metric_factor": 0.0},
        {"membrane_tension": 0.0},
    ),
)
def test_distributional_checker_rejects_invalid_inputs(kwargs):
    values = {
        "ell": 2,
        "wall_radius": 2.0,
        "wall_metric_factor": 0.8,
        "wall_metric_factor_derivative": -0.1,
        "wall_metric_factor_second_derivative": -0.05,
        "membrane_tension": 0.03,
        "wall_displacement_coefficient": 0.2,
        "background_energy_density": 0.4,
        "background_radial_pressure": 0.1,
        "background_radial_pressure_derivative": -0.2,
        "background_tangential_pressure": -0.05,
        "intrinsic_radial_pressure_multipole": 0.01,
        "intrinsic_radial_angular_shear_multipole": -0.02,
    }
    values.update(kwargs)
    with pytest.raises(ValueError):
        distributional_wall_conservation_coefficients(**values)
