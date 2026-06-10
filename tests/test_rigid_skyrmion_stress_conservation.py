import pytest

from qgtoy.rigid_skyrmion_stress_conservation import (
    hard_wall_angular_residual_asymptotic,
    rigid_skyrmion_l2_conservation_residuals,
    rigid_skyrmion_l2_stress_amplitudes,
    rigid_skyrmion_stress_conservation_certificate,
)


def test_exact_sample_amplitudes() -> None:
    record = rigid_skyrmion_l2_stress_amplitudes(
        radius=1.0,
        metric_factor=1.0,
        profile=1.5707963267948966,
        profile_derivative=0.0,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=1.0,
    )
    assert record["sigma_coefficient_k2"] == pytest.approx(0.125)
    assert record["skyrme_coefficient_k4"] == pytest.approx(0.5)
    assert record["energy_density_coefficient"] == pytest.approx(-0.625)
    assert record["radial_pressure_coefficient"] == pytest.approx(-0.625)
    assert record["tangential_pressure_coefficient"] == pytest.approx(-0.125)
    assert record["angular_tracefree_stress_coefficient"] == pytest.approx(-0.5)
    assert record["radial_angular_shear_coefficient"] == 0.0


def test_fixed_profile_source_fails_angular_conservation() -> None:
    record = rigid_skyrmion_l2_conservation_residuals(
        radius=1.0,
        metric_factor=1.0,
        profile=1.5707963267948966,
        profile_derivative=0.0,
        profile_second_derivative=0.0,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=1.0,
    )
    assert record["radial_conservation_residual_coefficient"] == pytest.approx(0.0)
    assert record["angular_conservation_residual_coefficient"] == pytest.approx(0.875)
    assert record["angular_residual_from_amplitudes"] == pytest.approx(0.875)
    assert not record["fixed_profile_source_is_bulk_conserved"]


def test_nontrivial_hard_wall_has_strict_collar_obstruction() -> None:
    record = hard_wall_angular_residual_asymptotic(
        wall_metric_factor=0.96,
        wall_profile_slope=-1.25,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=2.0,
    )
    assert record["angular_residual_quadratic_coefficient"] < 0.0
    assert record["strictly_negative_for_nonzero_slope"]


def test_zero_wall_slope_removes_this_obstruction() -> None:
    record = hard_wall_angular_residual_asymptotic(
        wall_metric_factor=0.96,
        wall_profile_slope=0.0,
        pion_decay_constant=1.0,
        skyrme_coupling=1.0,
        moment_of_inertia=2.0,
    )
    assert record["angular_residual_quadratic_coefficient"] == 0.0
    assert not record["strictly_negative_for_nonzero_slope"]


def test_certificate_passes() -> None:
    certificate = rigid_skyrmion_stress_conservation_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())


def test_bulk_residual_rejects_profile_zero() -> None:
    with pytest.raises(ValueError):
        rigid_skyrmion_l2_conservation_residuals(
            radius=1.0,
            metric_factor=1.0,
            profile=0.0,
            profile_derivative=-1.0,
            profile_second_derivative=0.0,
            pion_decay_constant=1.0,
            skyrme_coupling=1.0,
            moment_of_inertia=1.0,
        )
