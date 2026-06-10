from fractions import Fraction

from qgtoy.validated_centrifugal_origin_liouville import (
    validate_centrifugal_origin_liouville_partition,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_origin import validate_skyrmion_origin_family


def test_authenticated_extended_origin_family_closes_liouville_minor() -> None:
    origin = validate_skyrmion_origin_family(
        RationalInterval(
            Fraction(546684696508091, 347185136818875),
            Fraction(550388004634159, 347185136818875),
        ),
        cutoff=Fraction(3, 16),
        remainder_radius=Fraction(8),
        kernel_terms=12,
    )
    result = validate_centrifugal_origin_liouville_partition(
        origin,
        time_subdivisions=16,
        slope_subdivisions=4,
    )
    assert result.coefficient_coercivity_verified is True
    assert result.minimum_scaled_first_minor > 0
    assert result.minimum_scaled_determinant > 0
