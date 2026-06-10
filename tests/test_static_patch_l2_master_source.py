import pytest

from qgtoy.static_patch_l2_master_source import (
    canonical_l2_master_source_distribution,
    contact_free_wall_response,
    l2_zerilli_moncrief_master,
    rw_metric_master_identity_record,
    static_l2_master_source_density,
    static_patch_l2_green_source_derivative,
    traceless_quadrupole_harmonic_norm_squared,
)
from qgtoy.static_patch_l2_response import static_patch_l2_green_kernel


def _polynomial_jet(coefficients, radius, maximum_order):
    values = []
    current = tuple(float(value) for value in coefficients)
    for _ in range(maximum_order + 1):
        values.append(sum(value * radius**index for index, value in enumerate(current)))
        current = tuple(index * current[index] for index in range(1, len(current)))
    return values


def test_direct_rw_einstein_elimination_gives_master_source_identity():
    radius = 1.3
    h0 = _polynomial_jet((0.2, -0.1, 0.03), radius, 1)
    h2 = _polynomial_jet((-0.3, 0.2, -0.04, 0.01), radius, 2)
    angular = _polynomial_jet((0.1, 0.05, -0.02, 0.004), radius, 3)
    record = rw_metric_master_identity_record(
        radius=radius,
        static_patch_radius=10.0,
        temporal_metric_amplitude=h0[0],
        temporal_metric_amplitude_derivative=h0[1],
        radial_metric_amplitude=h2[0],
        radial_metric_amplitude_derivative=h2[1],
        radial_metric_amplitude_second_derivative=h2[2],
        angular_metric_amplitude=angular[0],
        angular_metric_amplitude_derivative=angular[1],
        angular_metric_amplitude_second_derivative=angular[2],
        angular_metric_amplitude_third_derivative=angular[3],
    )
    assert record["identity_residual"] == pytest.approx(0.0, abs=2.0e-15)
    independent_component_oracle = {
        "master_field": 0.03735999769666667,
        "master_operator": 0.0845111609428564,
        "einstein_time_time_amplitude": -0.04391689443786986,
        "einstein_time_time_amplitude_derivative": -0.36081049376422386,
        "einstein_radial_pressure_amplitude": 0.12691715727810648,
        "einstein_radial_angular_amplitude": -0.09804413630769229,
        "einstein_angular_tracefree_amplitude": 0.06104437869822484,
    }
    for name, expected in independent_component_oracle.items():
        assert record[name] == pytest.approx(expected, abs=2.0e-15)
    assert record["master_field"] == pytest.approx(
        l2_zerilli_moncrief_master(
            radius=radius,
            static_patch_radius=10.0,
            angular_metric_amplitude=angular[0],
            angular_metric_amplitude_derivative=angular[1],
            radial_metric_amplitude=h2[0],
        )
    )


def test_stress_source_formula_matches_direct_einstein_identity():
    radius = 1.3
    coupling = 0.7
    h0 = _polynomial_jet((0.2, -0.1, 0.03), radius, 1)
    h2 = _polynomial_jet((-0.3, 0.2, -0.04, 0.01), radius, 2)
    angular = _polynomial_jet((0.1, 0.05, -0.02, 0.004), radius, 3)
    record = rw_metric_master_identity_record(
        radius=radius,
        static_patch_radius=10.0,
        temporal_metric_amplitude=h0[0],
        temporal_metric_amplitude_derivative=h0[1],
        radial_metric_amplitude=h2[0],
        radial_metric_amplitude_derivative=h2[1],
        radial_metric_amplitude_second_derivative=h2[2],
        angular_metric_amplitude=angular[0],
        angular_metric_amplitude_derivative=angular[1],
        angular_metric_amplitude_second_derivative=angular[2],
        angular_metric_amplitude_third_derivative=angular[3],
    )
    source = static_l2_master_source_density(
        radius=radius,
        static_patch_radius=10.0,
        energy_density=-record["einstein_time_time_amplitude"] / coupling,
        energy_density_derivative=(
            -record["einstein_time_time_amplitude_derivative"] / coupling
        ),
        radial_pressure=record["einstein_radial_pressure_amplitude"] / coupling,
        radial_angular_shear=(record["einstein_radial_angular_amplitude"] / coupling),
        angular_tracefree_stress=(
            record["einstein_angular_tracefree_amplitude"] / coupling
        ),
        gravitational_coupling=coupling,
    )
    assert source == pytest.approx(record["master_operator"], abs=2.0e-15)


def test_contact_subtraction_preserves_off_wall_green_response():
    wall_radius = 4.0
    patch_radius = 20.0
    record = canonical_l2_master_source_distribution(
        wall_radius=wall_radius,
        static_patch_radius=patch_radius,
        bulk_energy_density_at_wall=0.2,
        energy_density_delta=-0.03,
        energy_density_delta_prime=0.04,
        radial_pressure_delta=0.05,
        radial_angular_shear_delta=-0.02,
        radial_pressure_delta_prime=-0.01,
        radial_angular_shear_delta_prime=0.006,
        angular_tracefree_stress_delta=0.008,
        angular_tracefree_stress_delta_prime=-0.004,
        gravitational_coupling=0.7,
    )
    assert record["master_source_delta_second_coefficient"] == pytest.approx(-0.07168)
    assert record["master_source_delta_prime_coefficient"] == pytest.approx(
        0.13150666666666666
    )
    assert record["master_source_delta_coefficient"] == pytest.approx(0.2933)
    assert record["contact_free_delta_prime_coefficient"] == pytest.approx(0.133)
    assert record["contact_free_delta_coefficient"] == pytest.approx(0.2653)
    for radius in (2.0, 6.0):
        green = static_patch_l2_green_kernel(
            radius, wall_radius, static_patch_radius=patch_radius
        )
        green_p = static_patch_l2_green_source_derivative(
            radius, wall_radius, static_patch_radius=patch_radius
        )
        lapse = 1.0 - wall_radius**2 / patch_radius**2
        lapse_p = -2.0 * wall_radius / patch_radius**2
        potential = 6.0 / wall_radius**2
        green_pp = (-lapse_p * green_p + potential * green) / lapse
        raw = (
            record["master_source_delta_coefficient"] * green
            - record["master_source_delta_prime_coefficient"] * green_p
            + record["master_source_delta_second_coefficient"] * green_pp
        )
        contact_free = contact_free_wall_response(
            radius,
            wall_radius=wall_radius,
            static_patch_radius=patch_radius,
            contact_free_delta_coefficient=record["contact_free_delta_coefficient"],
            contact_free_delta_prime_coefficient=record[
                "contact_free_delta_prime_coefficient"
            ],
        )
        assert contact_free == pytest.approx(raw, abs=1.0e-15)


@pytest.mark.parametrize(("radius", "source"), ((2.0, 4.0), (6.0, 4.0)))
def test_green_source_derivative_matches_finite_difference(radius, source):
    patch = 20.0
    step = 1.0e-5
    finite_difference = (
        static_patch_l2_green_kernel(radius, source + step, static_patch_radius=patch)
        - static_patch_l2_green_kernel(radius, source - step, static_patch_radius=patch)
    ) / (2.0 * step)
    assert static_patch_l2_green_source_derivative(
        radius, source, static_patch_radius=patch
    ) == pytest.approx(finite_difference, rel=1.0e-8)


def test_quadratic_rotation_tensor_harmonic_normalization():
    # Q=Omega Omega-delta Omega^2/3 has Tr(Q^2)=2 Omega^4/3.
    assert traceless_quadrupole_harmonic_norm_squared(2.0 / 3.0) == pytest.approx(
        16.0 * 3.141592653589793 / 45.0
    )


@pytest.mark.parametrize(
    "kwargs",
    (
        {"radius": 0.0},
        {"static_patch_radius": 1.0},
        {"gravitational_coupling": 0.0},
    ),
)
def test_smooth_source_rejects_invalid_inputs(kwargs):
    values = {
        "radius": 1.0,
        "static_patch_radius": 10.0,
        "energy_density": 0.2,
        "energy_density_derivative": -0.1,
        "radial_pressure": 0.03,
        "radial_angular_shear": -0.02,
        "angular_tracefree_stress": 0.01,
        "gravitational_coupling": 1.0,
    }
    values.update(kwargs)
    with pytest.raises(ValueError):
        static_l2_master_source_density(**values)
