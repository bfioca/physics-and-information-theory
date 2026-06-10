from fractions import Fraction

import pytest

from qgtoy.validated_centrifugal_origin_transfer import (
    conormal_fuchs_source,
    centrifugal_origin_conormal_certificate,
    formal_affine_endpoint_transfer,
    leading_green_majorant,
    leading_spectrum_checks,
    validate_conditional_radii_inequality,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_origin import _RationalFunction


SLOPES = RationalInterval(
    Fraction(546684696508091, 347185136818875),
    Fraction(550388004634159, 347185136818875),
)


def test_exact_shifted_indicial_spectrum() -> None:
    assert leading_spectrum_checks() == {0: True, 2: True, -3: True, -5: True}


def test_exact_source_block_identity() -> None:
    rf = _RationalFunction.constant
    mixed = ((rf(1), rf(2)), (rf(0), rf(-1)))
    principal = ((rf(2), rf(0)), (rf(0), rf(4)))
    source = conormal_fuchs_source(
        mixed,
        principal,
        (rf(6), rf(8)),
        (rf(5), rf(7)),
    )
    expected = (rf(3), rf(2), rf(2), rf(-9))
    assert all(
        left.exactly_equals(right) for left, right in zip(source, expected, strict=True)
    )


def test_green_majorant_is_rational_and_small() -> None:
    majorant = leading_green_majorant(SLOPES)
    assert majorant > 0
    assert majorant < Fraction(9, 20)


def test_conditional_radii_inequality_uses_exact_arithmetic() -> None:
    majorant = leading_green_majorant(SLOPES)
    certificate = validate_conditional_radii_inequality(
        green_majorant=majorant,
        coefficient_variation_bound=Fraction(11, 200),
        residual_bound=Fraction(1, 2),
        remainder_radius=Fraction(1),
    )
    assert certificate.contraction_bound == majorant * Fraction(11, 200)
    assert (
        certificate.radii_left_hand_side == majorant / 2 + certificate.contraction_bound
    )
    assert certificate.closes


def test_formal_affine_endpoint_map_keeps_two_free_columns_and_force() -> None:
    transfer = formal_affine_endpoint_transfer(SLOPES)
    assert transfer.cutoff == Fraction(1, 16)
    assert len(transfer.homogeneous_field_columns) == 2
    assert len(transfer.homogeneous_derivative_columns) == 2
    assert len(transfer.forced_field) == 2
    assert len(transfer.forced_derivative) == 2
    assert not transfer.is_finite_cell_enclosure
    assert "remains to be checked" in transfer.residual_order
    linear_tangential = transfer.homogeneous_field_columns[0][1]
    assert linear_tangential.lower > 0


def test_certificate_states_the_validation_boundary() -> None:
    certificate = centrifugal_origin_conormal_certificate(SLOPES)
    assert all(certificate["leading_spectrum_checks"].values())
    assert "Lagrange" in certificate["projector_construction"]
    assert certificate["affine_endpoint_map_preserved"]
    assert not certificate["finite_cell_enclosure"]
    assert "A(t)-A(0)" in certificate["claim_boundary"]


def test_radii_input_validation() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        validate_conditional_radii_inequality(
            green_majorant=Fraction(-1),
            coefficient_variation_bound=Fraction(0),
            residual_bound=Fraction(0),
            remainder_radius=Fraction(1),
        )
