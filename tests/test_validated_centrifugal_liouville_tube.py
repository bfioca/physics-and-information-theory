from fractions import Fraction

from qgtoy.validated_centrifugal_liouville_tube import (
    CentrifugalProfileTubeRadii,
    validate_centrifugal_liouville_outer_tube,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import SkyrmionPolynomialCell


def test_outer_tube_validator_closes_a_local_profile_ball() -> None:
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
    result = validate_centrifugal_liouville_outer_tube(
        (cell,),
        (
            CentrifugalProfileTubeRadii(
                Fraction(1, 1_000_000),
                Fraction(1, 1_000_000),
                Fraction(1, 1_000_000),
            ),
        ),
        first_source_cell_index=0,
        degree_limit=12,
        trigonometric_terms=6,
    )
    assert result.coercivity_verified is True
    assert result.minimum_scaled_first_minor > 0
    assert result.minimum_scaled_determinant > 0
