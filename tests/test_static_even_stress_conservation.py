import pytest

from qgtoy.static_even_stress_conservation import (
    hard_wall_traction_jump_record,
    static_even_stress_conservation_certificate,
    static_even_stress_conservation_residuals,
    zero_momentum_static_relation,
)


def test_manufactured_quadrupole_source_is_conserved() -> None:
    record = static_even_stress_conservation_residuals(
        ell=2,
        radius=2.0,
        metric_factor=0.8,
        metric_factor_derivative=-0.2,
        energy_density=3.0,
        radial_pressure=1.0,
        radial_pressure_derivative=0.5,
        tangential_pressure=1.0,
        radial_angular_shear=0.0,
        radial_angular_shear_derivative=0.0,
        angular_tracefree_stress=0.5,
    )
    assert record["radial_conservation_residual"] == pytest.approx(0.0)
    assert record["angular_conservation_residual"] == pytest.approx(0.0)
    assert record["bulk_source_is_conserved"]


def test_zero_momentum_quadrupole_requires_p_perp_equals_two_pi() -> None:
    passing = zero_momentum_static_relation(
        ell=2,
        tangential_pressure=6.0,
        angular_tracefree_stress=3.0,
    )
    failing = zero_momentum_static_relation(
        ell=2,
        tangential_pressure=5.0,
        angular_tracefree_stress=3.0,
    )
    assert passing["zero_momentum_source_is_angularly_conserved"]
    assert not failing["zero_momentum_source_is_angularly_conserved"]
    assert failing["angular_conservation_residual"] == pytest.approx(-1.0)


def test_hard_wall_requires_traction_completion() -> None:
    open_jump = hard_wall_traction_jump_record(
        wall_radius=4.0,
        interior_radial_pressure=2.0,
        interior_radial_angular_shear=-0.25,
    )
    closed_jump = hard_wall_traction_jump_record(
        wall_radius=4.0,
        interior_radial_pressure=0.0,
        interior_radial_angular_shear=0.0,
    )
    assert open_jump["radial_conservation_delta_coefficient"] == -2.0
    assert open_jump["angular_conservation_delta_coefficient"] == 0.25
    assert not open_jump["bulk_truncation_is_distributionally_conserved"]
    assert closed_jump["bulk_truncation_is_distributionally_conserved"]


def test_certificate_passes() -> None:
    certificate = static_even_stress_conservation_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())


@pytest.mark.parametrize("ell", (0, 1, 2.5, True))
def test_invalid_multipole_is_rejected(ell: object) -> None:
    with pytest.raises(ValueError):
        zero_momentum_static_relation(
            ell=ell,  # type: ignore[arg-type]
            tangential_pressure=1.0,
            angular_tracefree_stress=0.5,
        )
