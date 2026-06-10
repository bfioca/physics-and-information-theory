import unittest
from fractions import Fraction

from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_origin import validate_skyrmion_origin_quintic_patch
from qgtoy.validated_skyrmion_quintic_family import (
    validate_skyrmion_origin_quintic_family,
)


AUTHENTICATED_SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
)


class ValidatedSkyrmionQuinticFamilyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.family = validate_skyrmion_origin_quintic_family(
            AUTHENTICATED_SLOPES,
            slope_cells=16,
        )

    def test_authenticated_family_closes_with_margin(self) -> None:
        family = self.family
        self.assertEqual(family.shooting_slopes, AUTHENTICATED_SLOPES)
        self.assertEqual(family.cutoff, Fraction(1, 16))
        self.assertEqual(family.remainder_radius, Fraction(13, 10))
        self.assertEqual(len(family.cells), 16)
        self.assertLess(family.maximum_contraction_bound, Fraction(3, 5))
        self.assertLess(
            family.maximum_residual_bound
            + family.maximum_contraction_bound * family.remainder_radius,
            Fraction(9, 10),
        )
        self.assertGreater(family.minimum_volterra_denominator, 20)

    def test_cells_cover_the_slope_box_without_gaps(self) -> None:
        cells = self.family.cells
        self.assertEqual(cells[0].shooting_slopes.lower, AUTHENTICATED_SLOPES.lower)
        self.assertEqual(cells[-1].shooting_slopes.upper, AUTHENTICATED_SLOPES.upper)
        for left, right in zip(cells, cells[1:]):
            self.assertEqual(
                left.shooting_slopes.upper,
                right.shooting_slopes.lower,
            )

    def test_cutoff_orientation_is_uniform(self) -> None:
        self.assertGreater(self.family.profile_at_cutoff.lower, 3)
        self.assertLess(self.family.profile_at_cutoff.upper, Fraction(31, 10))
        self.assertLess(self.family.derivative_at_cutoff.upper, 0)

    def test_family_contains_pointwise_quintic_certificates(self) -> None:
        for slope in (
            AUTHENTICATED_SLOPES.lower,
            AUTHENTICATED_SLOPES.midpoint,
            AUTHENTICATED_SLOPES.upper,
        ):
            point = validate_skyrmion_origin_quintic_patch(slope)
            self.assertTrue(
                point.profile_at_cutoff.is_subset_of(
                    self.family.profile_at_cutoff
                )
            )
            self.assertTrue(
                point.derivative_at_cutoff.is_subset_of(
                    self.family.derivative_at_cutoff
                )
            )

    def test_rejects_a_radius_that_does_not_close(self) -> None:
        with self.assertRaisesRegex(ValueError, "radii inequality"):
            validate_skyrmion_origin_quintic_family(
                AUTHENTICATED_SLOPES,
                remainder_radius=Fraction(1, 10),
                slope_cells=16,
            )


if __name__ == "__main__":
    unittest.main()
