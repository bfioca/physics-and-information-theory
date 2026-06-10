from fractions import Fraction

import pytest

from qgtoy.paper_r_state_transfer import (
    certify_paper_r_state_transfer,
    exact_spin_two_state_data,
)
from qgtoy.validated_interval import RationalInterval


def test_exact_spin_two_states_have_equal_energy_and_distinct_qj() -> None:
    cat, anticoherent = exact_spin_two_state_data()

    assert cat.normalization == anticoherent.normalization == Fraction(1)
    assert cat.casimir == anticoherent.casimir == Fraction(6)
    assert (
        cat.leading_rotor_energy_coefficient
        == anticoherent.leading_rotor_energy_coefficient
        == Fraction(3)
    )
    assert cat.quadrupole_qj == (
        (Fraction(-1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(-1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(2)),
    )
    assert anticoherent.quadrupole_qj == (
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    assert cat.quadrupole_frobenius_norm_squared == Fraction(6)
    assert cat.quadrupole_frobenius_norm_symbolic == "sqrt(6)"
    assert anticoherent.quadrupole_frobenius_norm_squared == Fraction(0)
    assert anticoherent.quadrupole_frobenius_norm_symbolic == "0"


def test_signed_amplitude_certifies_nonzero_state_sensitive_footprint() -> None:
    certificate = certify_paper_r_state_transfer(
        exterior_amplitude=RationalInterval(Fraction(-3, 1000), Fraction(-2, 1000)),
        annular_rms_factor=Fraction(25, 2),
    )

    assert certificate.exterior_amplitude_excludes_zero
    assert certificate.exterior_amplitude_sign == -1
    assert certificate.unit_tensor_weyl_footprint == RationalInterval(
        Fraction(1, 40), Fraction(3, 80)
    )
    assert certificate.cat_weyl_footprint_squared == RationalInterval(
        Fraction(3, 800), Fraction(27, 3200)
    )
    assert certificate.cat_weyl_footprint.lower > 0
    assert certificate.cat_weyl_footprint.lower**2 <= Fraction(3, 800)
    assert certificate.cat_weyl_footprint.upper**2 >= Fraction(27, 3200)
    assert certificate.anticoherent_weyl_footprint == RationalInterval.point(0)
    assert certificate.equal_casimir_and_leading_energy
    assert certificate.state_sensitive_nonzero_conclusion
    assert "Leading O(Omega^2)" in certificate.claim_scope


def test_positive_amplitude_preserves_signed_interval_conclusion() -> None:
    certificate = certify_paper_r_state_transfer(
        exterior_amplitude=RationalInterval(Fraction(1, 500), Fraction(1, 400))
    )

    assert certificate.exterior_amplitude_sign == 1
    assert certificate.exterior_amplitude_excludes_zero
    assert certificate.state_sensitive_nonzero_conclusion
    assert certificate.unit_tensor_weyl_footprint.lower == Fraction(1, 40)
    assert certificate.unit_tensor_weyl_footprint.upper == Fraction(1, 32)


def test_amplitude_interval_containing_zero_does_not_claim_nonzero() -> None:
    certificate = certify_paper_r_state_transfer(
        exterior_amplitude=RationalInterval(Fraction(-1, 1000), Fraction(1, 500))
    )

    assert not certificate.exterior_amplitude_excludes_zero
    assert certificate.exterior_amplitude_sign == 0
    assert certificate.unit_tensor_weyl_footprint == RationalInterval(
        Fraction(0), Fraction(1, 40)
    )
    assert certificate.cat_weyl_footprint.lower == 0
    assert certificate.anticoherent_weyl_footprint == RationalInterval.point(0)
    assert not certificate.state_sensitive_nonzero_conclusion
    assert certificate.conclusion.startswith("not certified")


@pytest.mark.parametrize(
    ("amplitude", "factor", "error"),
    (
        ((Fraction(-1), Fraction(1)), Fraction(25, 2), TypeError),
        (RationalInterval(Fraction(-2), Fraction(-1)), 12.5, TypeError),
        (RationalInterval(Fraction(-2), Fraction(-1)), Fraction(0), ValueError),
    ),
)
def test_transfer_requires_exact_validated_inputs(amplitude, factor, error) -> None:
    with pytest.raises(error):
        certify_paper_r_state_transfer(
            exterior_amplitude=amplitude,
            annular_rms_factor=factor,
        )
