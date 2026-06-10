import unittest
from math import asin, sqrt

from qgtoy.__main__ import build_parser
from qgtoy.skyrmion_current_moments import (
    centered_current_moment_record,
    proper_radial_coordinate,
    signed_second_moment_tensor_coefficients,
    skyrmion_current_moments_certificate,
)


class SkyrmionCurrentMomentsTest(unittest.TestCase):
    def test_proper_radial_coordinate(self):
        self.assertEqual(proper_radial_coordinate(2.0, curvature=0.0), 2.0)
        self.assertAlmostEqual(
            proper_radial_coordinate(4.0, curvature=0.0025),
            asin(0.2) / sqrt(0.0025),
            places=14,
        )

    def test_signed_second_moment_trace(self):
        mean_square = 2.5
        for current_component in range(3):
            trace = [0.0, 0.0, 0.0]
            for coordinate in range(3):
                coefficients = signed_second_moment_tensor_coefficients(
                    current_component,
                    coordinate,
                    coordinate,
                    proper_mean_square_radius=mean_square,
                )
                trace = [left + right for left, right in zip(trace, coefficients)]
            expected = [0.0, 0.0, 0.0]
            expected[current_component] = mean_square
            for left, right in zip(trace, expected):
                self.assertAlmostEqual(left, right, places=14)

    def test_default_moments_match_centered_profile(self):
        record = centered_current_moment_record()
        self.assertAlmostEqual(record["dimensionless_inertia_c_I"], 34.26620155, places=6)
        self.assertAlmostEqual(
            record["dimensionless_areal_mean_square_radius"],
            2.18432069,
            places=6,
        )
        self.assertAlmostEqual(
            record["dimensionless_proper_mean_square_radius"],
            2.19023555,
            places=6,
        )
        self.assertAlmostEqual(
            record["dimensionless_proper_rms_radius"],
            1.47994444,
            places=6,
        )
        self.assertGreater(
            record["absolute_first_moment_bound_coefficient_per_spin"], 0.0
        )

    def test_certificate(self):
        certificate = skyrmion_current_moments_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertLess(certificate["relative_step_change"], 1.0e-6)

    def test_cli_defaults(self):
        args = build_parser().parse_args(["skyrmion-current-moments"])
        self.assertEqual(args.pion_mass, 1.0)
        self.assertEqual(args.curvature, 0.0025)
        self.assertEqual(args.wall_radius, 4.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            centered_current_moment_record(pion_mass=0.0)
        with self.assertRaises(ValueError):
            proper_radial_coordinate(20.0, curvature=0.0025)
        with self.assertRaises(ValueError):
            signed_second_moment_tensor_coefficients(
                3,
                0,
                0,
                proper_mean_square_radius=1.0,
            )


if __name__ == "__main__":
    unittest.main()
