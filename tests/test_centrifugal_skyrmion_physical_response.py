from math import pi, sqrt

import pytest

from qgtoy.centrifugal_skyrmion_master_response import (
    centrifugal_skyrmion_master_response_record,
)
from qgtoy.centrifugal_skyrmion_physical_response import (
    collective_quadrupole_normalization_record,
    normalize_skyrmion_master_response,
    physical_skyrmion_master_response_record,
    skyrme_physical_unit_record,
)


def _pure_density(state):
    return tuple(
        tuple(left * right.conjugate() for right in state) for left in state
    )


def _spin_two_cat_density():
    return _pure_density((1.0 / sqrt(2.0), 0.0, 0.0, 0.0, 1.0 / sqrt(2.0)))


def _spin_two_anticoherent_density():
    return _pure_density((0.5, 0.0, 1.0j / sqrt(2.0), 0.0, 0.5))


def test_physical_units_follow_the_action_scaling():
    record = skyrme_physical_unit_record(
        skyrme_coupling=2.0,
        pion_decay_constant=3.0,
        newton_constant=0.01,
        pion_mass_mu=1.0,
        curvature_lambda=0.0025,
        wall_radius=4.0,
    )
    assert record["length_unit_L0"] == pytest.approx(1.0 / 6.0)
    assert record["bulk_stress_unit_T0"] == pytest.approx(324.0)
    assert record["membrane_tension_unit_sigma0"] == pytest.approx(54.0)
    assert record["dimensionless_einstein_coupling_kappa_hat"] == pytest.approx(
        8.0 * pi * 0.01 * 9.0
    )
    assert record["physical_static_patch_radius"] == pytest.approx(10.0 / 3.0)


def test_spin_cat_collective_tensor_has_expected_normalization():
    inertia = 10.0
    record = collective_quadrupole_normalization_record(
        skyrme_coupling=2.0,
        inertia_constant=inertia,
        spin=2.0,
        state_density_matrix=_spin_two_cat_density(),
    )
    assert record["state_casimir_expectation_C"] == pytest.approx(6.0)
    assert tuple(
        value
        for row in record["state_traceless_quadrupole_QJ_ab"]
        for value in row
    ) == pytest.approx((-1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 2.0))
    assert record["Qhat_over_QJ_factor"] == pytest.approx(16.0 / 100.0)
    assert record[
        "slow_rotation_parameter_e_squared_sqrt_j_jplus1_over_c_I"
    ] == (
        pytest.approx(4.0 * 6.0**0.5 / 10.0)
    )


def test_anticoherent_second_moment_has_zero_leading_master_response():
    record = physical_skyrmion_master_response_record(
        skyrme_coupling=1.0,
        pion_decay_constant=1.0,
        newton_constant=1.0e-6,
        spin=2.0,
        state_density_matrix=_spin_two_anticoherent_density(),
        node_count=101,
    )
    assert record["collective_state"]["leading_quadrupole_response_vanishes"]
    assert all(
        sample["physical_master_angular_rms"] == 0.0
        for sample in record["response_samples"]
    )


def test_physical_master_scaling_and_sphere_norm():
    response = centrifugal_skyrmion_master_response_record(node_count=101)
    inertia = 34.26620155247604
    first = normalize_skyrmion_master_response(
        response,
        skyrme_coupling=2.0,
        pion_decay_constant=3.0,
        newton_constant=0.01,
        inertia_constant=inertia,
        spin=2.0,
        state_density_matrix=_spin_two_cat_density(),
    )
    second = normalize_skyrmion_master_response(
        response,
        skyrme_coupling=4.0,
        pion_decay_constant=3.0,
        newton_constant=0.01,
        inertia_constant=inertia,
        spin=2.0,
        state_density_matrix=_spin_two_cat_density(),
    )
    assert second["physical_master_prefactor_per_psi0_and_QJ"] == pytest.approx(
        8.0 * first["physical_master_prefactor_per_psi0_and_QJ"]
    )
    sample = first["response_samples"][0]
    tensor = sample["physical_master_tensor_Psi_ab"]
    norm_squared = sum(value**2 for row in tensor for value in row)
    assert sample["physical_master_angular_integral"] == pytest.approx(
        8.0 * pi * norm_squared / 15.0
    )


@pytest.mark.parametrize(
    "density",
    (
        ((1.0, 0.0), (0.0, 1.0)),
        ((1.0, 1.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        ((1.2, 0.0, 0.0), (0.0, -0.2, 0.0), (0.0, 0.0, 0.0)),
    ),
)
def test_collective_normalization_rejects_invalid_density_matrices(density):
    with pytest.raises(ValueError):
        collective_quadrupole_normalization_record(
            skyrme_coupling=1.0,
            inertia_constant=1.0,
            spin=1.0,
            state_density_matrix=density,
        )


def test_collective_normalization_rejects_non_half_integer_spin():
    with pytest.raises(ValueError, match="half-integer"):
        collective_quadrupole_normalization_record(
            skyrme_coupling=1.0,
            inertia_constant=1.0,
            spin=0.7,
            state_density_matrix=((1.0,),),
        )


def test_declared_slow_rotation_budget_is_enforced():
    response = centrifugal_skyrmion_master_response_record(node_count=101)
    with pytest.raises(ValueError, match="slow-rotation"):
        normalize_skyrmion_master_response(
            response,
            skyrme_coupling=5.0,
            pion_decay_constant=1.0,
            newton_constant=1.0e-6,
            inertia_constant=34.26620155247604,
            spin=2.0,
            state_density_matrix=_spin_two_cat_density(),
            maximum_slow_rotation=0.1,
        )
