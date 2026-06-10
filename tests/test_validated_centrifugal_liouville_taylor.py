from fractions import Fraction

from qgtoy.validated_centrifugal_liouville_taylor import (
    _CenteredTaylorModel,
    centrifugal_liouville_taylor_cell,
    validate_centrifugal_liouville_taylor_spline,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import SkyrmionPolynomialCell


def test_centered_taylor_model_integrates_odd_terms_exactly() -> None:
    model = _CenteredTaylorModel(
        coefficients=tuple(
            RationalInterval.point(value)
            for value in (Fraction(3), Fraction(7), Fraction(5), Fraction(-11))
        ),
        remainder=RationalInterval(Fraction(-1, 10), Fraction(1, 5)),
    )

    assert model.symmetric_integral() == RationalInterval(
        Fraction(3) * 2 + Fraction(5) * Fraction(2, 3) - Fraction(1, 5),
        Fraction(3) * 2 + Fraction(5) * Fraction(2, 3) + Fraction(2, 5),
    )


def test_centered_model_multiplication_contains_endpoint_products() -> None:
    model = _CenteredTaylorModel.from_polynomial(
        RationalPolynomial((Fraction(2), Fraction(1), Fraction(-1, 3))),
        degree_limit=8,
    )
    square = model * model
    for point in (Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1)):
        value = model.coefficients[0]
        direct = Fraction(2) + point - point**2 / 3
        assert square.range().contains(direct**2)
        assert model.range().contains(direct)
        assert value.contains(2)


def test_centered_model_reciprocal_and_trigonometry_contain_points() -> None:
    model = _CenteredTaylorModel.from_polynomial(
        RationalPolynomial((Fraction(3, 5), Fraction(1, 100))),
        degree_limit=16,
    )
    reciprocal = model.reciprocal(terms=8)
    sine, cosine = model.sin_cos(terms=7)
    assert reciprocal.range().contains(Fraction(5, 3))
    assert sine.range().lower < sine.range().upper
    assert cosine.range().lower < cosine.range().upper


def test_local_profile_polynomial_closes_liouville_minor() -> None:
    # Centered quadratic approximation at x=2, rewritten in s in [0,1].
    width = Fraction(1, 50)
    f0 = Fraction(6295, 10_000)
    fp = Fraction(-8114, 10_000)
    fpp = Fraction(6433, 10_000)
    # x-2=width*(s-1/2).
    coefficients = (
        f0 - fp * width / 2 + fpp * width**2 / 8,
        fp * width - fpp * width**2 / 2,
        fpp * width**2 / 2,
    )
    cell = SkyrmionPolynomialCell(
        RationalInterval(Fraction(199, 100), Fraction(201, 100)),
        RationalPolynomial(coefficients),
    )
    result = centrifugal_liouville_taylor_cell(
        cell,
        Fraction(0),
        Fraction(1),
        source_cell_index=0,
        degree_limit=20,
    )
    assert result.principal_positive is True
    assert result.shifted_potential_positive is True
    assert result.scaled_first_minor.lower > 0
    assert result.scaled_determinant.lower > 0


def test_adaptive_spline_validator_records_global_minima() -> None:
    width = Fraction(1, 50)
    f0 = Fraction(6295, 10_000)
    fp = Fraction(-8114, 10_000)
    fpp = Fraction(6433, 10_000)
    cell = SkyrmionPolynomialCell(
        RationalInterval(Fraction(199, 100), Fraction(201, 100)),
        RationalPolynomial(
            (
                f0 - fp * width / 2 + fpp * width**2 / 8,
                fp * width - fpp * width**2 / 2,
                fpp * width**2 / 2,
            )
        ),
    )
    result = validate_centrifugal_liouville_taylor_spline(
        (cell,),
        degree_limit=12,
        trigonometric_terms=6,
    )
    assert result.coercivity_verified is True
    assert result.profile_cell_count == 1
    assert result.maximum_refinement_depth_used == 0
    assert result.minimum_scaled_first_minor > 0
    assert result.minimum_scaled_determinant > 0
