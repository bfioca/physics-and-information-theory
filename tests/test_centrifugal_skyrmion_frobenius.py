from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_frobenius import (
    centrifugal_skyrmion_first_frobenius_recurrence_certificate,
)


def test_exact_first_frobenius_recurrence_closes():
    record = centrifugal_skyrmion_first_frobenius_recurrence_certificate()
    assert record["p5_recurrence_determinant_identity_verified"]
    assert record["all_exact_recurrence_checks_pass"]
    for branch in record["branches"].values():
        assert branch["leading_equation_residual_vanishes"]
        assert all(branch["p5_recurrence_residuals_vanish"])


def test_reference_coefficients_match_independent_derivation():
    branches = centrifugal_skyrmion_first_frobenius_recurrence_certificate()[
        "branches"
    ]
    expected = {
        "linear_homogeneous": (0.3279577054, -0.1494623983, 0.04710453574),
        "cubic_homogeneous": (3.195336901, -1.251770645, -0.6521074264),
        "forced_particular": (-0.09477191097, 0.1353338744, 0.08724110619),
    }
    for name, (v1, u1, v2) in expected.items():
        assert branches[name]["v1"]["reference_decimal"] == pytest.approx(v1)
        assert branches[name]["u1"]["reference_decimal"] == pytest.approx(u1)
        assert branches[name]["v2"]["reference_decimal"] == pytest.approx(v2)


def test_reference_slope_validation():
    with pytest.raises(ValueError):
        centrifugal_skyrmion_first_frobenius_recurrence_certificate(
            reference_slope=Fraction(0)
        )
    with pytest.raises(ValueError):
        centrifugal_skyrmion_first_frobenius_recurrence_certificate(
            reference_slope=1.0  # type: ignore[arg-type]
        )
