from math import sqrt

import pytest

from qgtoy.rotational_stress_multipole import (
    hedgehog_rotational_stress_multipole_record,
    integrated_hedgehog_quadrupole_energy_record,
    rotational_stress_multipole_certificate,
    spin_cat_quadrupole_record,
    spin_two_tetrahedral_anticoherent_record,
    universal_quadrupole_norm_bounds,
)


def test_universal_quadrupole_bounds() -> None:
    bounds = universal_quadrupole_norm_bounds(12.0)
    assert bounds["quadrupole_operator_norm_upper_bound"] == pytest.approx(8.0)
    assert bounds["quadrupole_frobenius_norm_upper_bound"] == pytest.approx(
        12.0 * sqrt(2.0 / 3.0)
    )
    assert bounds["angular_rms_nQn_upper_bound"] == pytest.approx(
        8.0 / sqrt(5.0)
    )


def test_spin_cat_quadrupole_is_exact_and_asymptotically_sharp() -> None:
    record = spin_cat_quadrupole_record(20)
    assert record["quadrupole_trace"]["exact"] == "0"
    assert record["quadrupole_eigenvalues"][0]["exact"] == "-95/3"
    assert record["quadrupole_eigenvalues"][2]["exact"] == "190/3"
    assert record["operator_norm_to_casimir_ratio"]["exact"] == "19/33"


def test_explicit_spin_two_state_is_second_order_anticoherent() -> None:
    record = spin_two_tetrahedral_anticoherent_record()
    assert record["normalization_squared"]["exact"] == "1"
    assert all(value["exact"] == "0" for value in record["mean_angular_momentum"])
    assert all(
        value["exact"] == "2"
        for value in record["symmetric_second_moment_eigenvalues"]
    )
    assert all(value["exact"] == "0" for value in record["quadrupole_eigenvalues"])
    assert record["rotational_qfi_rank"] == 3


def test_anticoherent_branch_removes_leading_spin_two_source() -> None:
    record = hedgehog_rotational_stress_multipole_record(
        mean_casimir=6.0,
        radial_quadrupole_coefficient=-3.0,
        quadrupole_frobenius_norm=0.0,
    )
    assert record["leading_l2_source_vanishes"]
    assert record["pointwise_l2_source_upper_bound"] == 0.0
    assert record["angular_rms_l2_source"] == 0.0


def test_impossible_quadrupole_norm_is_rejected() -> None:
    with pytest.raises(ValueError, match="exceeds"):
        hedgehog_rotational_stress_multipole_record(
            mean_casimir=6.0,
            radial_quadrupole_coefficient=1.0,
            quadrupole_frobenius_norm=6.0,
        )


def test_integrated_spin_two_energy_is_bounded_by_total_rotor_energy() -> None:
    cat = spin_cat_quadrupole_record(20)
    q_norm = sqrt(float(cat["quadrupole_frobenius_norm_squared"]["value"]))
    record = integrated_hedgehog_quadrupole_energy_record(
        mean_casimir=cat["mean_casimir"]["value"],
        moment_of_inertia=7.0,
        quadrupole_frobenius_norm=q_norm,
    )
    assert record["spin_two_to_total_energy_ratio_upper_bound"] < 1.0 / sqrt(5.0)
    assert record["universal_l1_spin_two_energy_upper_bound"] == pytest.approx(
        record["total_leading_rotor_energy"] / sqrt(5.0)
    )


def test_anticoherent_integrated_spin_two_energy_vanishes() -> None:
    record = integrated_hedgehog_quadrupole_energy_record(
        mean_casimir=6.0,
        moment_of_inertia=3.0,
        quadrupole_frobenius_norm=0.0,
    )
    assert record["leading_spin_two_energy_vanishes"]
    assert record["radially_integrated_l1_spin_two_energy_upper_bound"] == 0.0


def test_rotational_stress_certificate_passes() -> None:
    certificate = rotational_stress_multipole_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())
