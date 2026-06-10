import unittest
from fractions import Fraction

from qgtoy.skyrmion_taylor_certificate_generator import (
    generate_skyrmion_taylor_track,
)


class SkyrmionTaylorCertificateGeneratorTest(unittest.TestCase):
    def test_short_exact_rational_track_is_fully_validated(self):
        result = generate_skyrmion_taylor_track(
            Fraction(1_579_953, 1_000_000),
            requested_radius=Fraction(17, 256),
            minimum_step=Fraction(1, 1024),
            maximum_step=Fraction(1, 1024),
        )

        self.assertEqual(result.status, "pass")
        self.assertEqual(result.reached_radius, Fraction(17, 256))
        self.assertIsNone(result.obstruction)
        self.assertEqual(len(result.cells), 4)
        self.assertIsNotNone(result.validated_track)
        track = result.validated_track
        assert track is not None
        self.assertEqual(track.cells[-1].radius_end, result.reached_radius)
        for index, cell in enumerate(result.cells):
            self.assertEqual(cell.profile_polynomial.degree, 3)
            self.assertIsInstance(cell.profile_radius, Fraction)
            self.assertIsInstance(cell.derivative_radius, Fraction)
            if index:
                self.assertEqual(
                    track.cells[index].initial,
                    track.cells[index - 1].endpoint,
                )
            self.assertLess(track.cells[index].contraction_bound, 1)

    def test_requested_radius_must_lie_on_exact_grid(self):
        with self.assertRaisesRegex(ValueError, "minimum-step grid"):
            generate_skyrmion_taylor_track(
                Fraction(1_579_953, 1_000_000),
                requested_radius=Fraction(1, 10),
                minimum_step=Fraction(1, 1024),
            )


if __name__ == "__main__":
    unittest.main()
