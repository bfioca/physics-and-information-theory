from fractions import Fraction
from math import pi

import numpy as np
import pytest

from qgtoy.centrifugal_skyrmion_deformation import (
    quadrupole_static_hessian_matrix,
)
from qgtoy.centrifugal_skyrmion_origin import (
    centrifugal_origin_indicial_certificate,
    centrifugal_origin_leading_hessian,
    centrifugal_origin_leading_robin_enclosure,
)


def test_exact_origin_indicial_roots_and_linear_mode():
    record = centrifugal_origin_indicial_certificate()
    assert all(record["root_determinant_polynomials_vanish"].values())
    assert record["quartic_factorization_verified"]
    assert record["principal_block_positive_for_every_real_slope"]
    assert record["indicial_roots"] == (1, 3, -2, -4)
    assert record["linear_regular_mode"] == "(f,g)=(-1,1)x"
    assert all(
        coefficients == ("0",)
        for coefficients in record["linear_mode_polynomial_residuals"]
    )
    assert all(
        coefficients == ("0",)
        for coefficients in record["cubic_mode_polynomial_residuals"]
    )


def test_leading_principal_block_is_symmetric_and_nonzero():
    hessian = centrifugal_origin_leading_hessian()
    assert hessian[2][3] == hessian[3][2]
    assert hessian[2][2] != (Fraction(0),)
    assert hessian[3][3] != (Fraction(0),)


def test_exact_cubic_mode_matches_the_floating_probe():
    record = centrifugal_origin_indicial_certificate()
    ratio = float(Fraction(record["reference_cubic_mode_f_over_g"]))
    assert ratio == pytest.approx(0.04172747, rel=2.0e-4)


def test_exact_leading_hessian_matches_small_radius_density_generator():
    slope = float(Fraction(1462763601523, 925827031517))
    radius = 1.0e-5
    floating = np.asarray(
        quadrupole_static_hessian_matrix(
            radius=radius,
            metric_factor=1.0 - 0.0025 * radius**2,
            profile=pi - slope * radius,
            profile_derivative=-slope,
            pion_mass=1.0,
        )["symmetric_hessian_matrix"]
    )
    rescaling = np.diag((1.0, 1.0, 1.0 / radius, 1.0 / radius))
    scaled = rescaling @ floating @ rescaling
    exact = centrifugal_origin_leading_hessian()
    evaluated = np.asarray(
        [
            [
                sum(float(coefficient) * slope**power for power, coefficient in enumerate(entry))
                for entry in row
            ]
            for row in exact
        ]
    )
    assert np.max(np.abs(scaled - evaluated)) < 2.0e-8


def test_origin_certificate_rejects_nonpositive_or_nonrational_slope():
    with pytest.raises(ValueError):
        centrifugal_origin_indicial_certificate(reference_slope=Fraction(0))
    with pytest.raises(ValueError):
        centrifugal_origin_indicial_certificate(reference_slope=1.0)  # type: ignore[arg-type]


def test_leading_robin_enclosure_is_positive_and_narrow():
    matrix = centrifugal_origin_leading_robin_enclosure()
    assert all(entry.lower > 0 for row in matrix for entry in row)
    assert max(entry.width for row in matrix for entry in row) < Fraction(1, 20)


@pytest.mark.parametrize(
    "kwargs",
    (
        {"cutoff": Fraction(0)},
        {"cutoff": 0.1},
        {"slope_lower": Fraction(2), "slope_upper": Fraction(1)},
        {"slope_lower": 1.0},
    ),
)
def test_leading_robin_enclosure_rejects_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        centrifugal_origin_leading_robin_enclosure(**kwargs)
