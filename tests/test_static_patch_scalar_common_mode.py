from math import pi
import unittest

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_scalar_common_mode import (
    analytic_optical_distance_necessary_bound,
    maximum_optical_distance_for_correlation_defect,
    optical_radius_from_horizon_proper_distance,
    maximum_same_shell_angular_separation,
    same_shell_optical_distance_over_radius,
    static_patch_scalar_common_mode_certificate,
    static_patch_scalar_common_mode_record,
    zero_frequency_scalar_correlation,
)


class StaticPatchScalarCommonModeTest(unittest.TestCase):
    def test_zero_frequency_correlation(self):
        self.assertEqual(zero_frequency_scalar_correlation(0.0), 1.0)
        values = tuple(
            zero_frequency_scalar_correlation(value)
            for value in (0.1, 0.5, 1.0, 2.0, 10.0)
        )
        self.assertTrue(all(0.0 < value < 1.0 for value in values))
        self.assertTrue(all(right < left for left, right in zip(values, values[1:])))
        self.assertAlmostEqual(
            zero_frequency_scalar_correlation(1.0e-5),
            1.0 - 1.0e-10 / 6.0,
            places=14,
        )

    def test_static_slice_geometry(self):
        radius = 2.0
        self.assertAlmostEqual(
            optical_radius_from_horizon_proper_distance(
                0.5 * pi * radius / 2.0,
                radius=radius,
            ),
            radius * 0.881373587019543,
        )
        self.assertEqual(
            same_shell_optical_distance_over_radius(
                0.1,
                0.0,
                radius=1.0,
            ),
            0.0,
        )
        self.assertAlmostEqual(
            optical_radius_from_horizon_proper_distance(
                0.5 * pi * radius,
                radius=radius,
            ),
            0.0,
            places=14,
        )
        self.assertGreater(
            same_shell_optical_distance_over_radius(
                0.5 * pi - 1.0e-10,
                0.1,
                radius=1.0,
            ),
            0.0,
        )

    def test_angular_inversion_uses_log_domain(self):
        maximum_angle = maximum_same_shell_angular_separation(
            5.0e-324,
            1401.0,
            radius=1.0,
        )
        self.assertGreater(maximum_angle, 0.0)
        self.assertLess(maximum_angle, pi)

    def test_exact_correlation_inversion_and_analytic_bound(self):
        for defect in (1.0e-4, 0.01, 0.1, 0.5):
            exact = maximum_optical_distance_for_correlation_defect(defect)
            self.assertAlmostEqual(
                1.0 - zero_frequency_scalar_correlation(exact),
                defect,
                places=12,
            )
            self.assertLessEqual(
                exact,
                analytic_optical_distance_necessary_bound(defect),
            )

    def test_fixed_angular_separation_fails_at_large_dimension(self):
        record = static_patch_scalar_common_mode_record(
            4096,
            radius=1.0,
            stretched_distance=0.05,
            angular_separation=0.1,
        )
        self.assertFalse(record["passes_axial_common_mode_error_allocation"])
        self.assertGreater(
            record["actual_axial_common_mode_mismatch_lower_bound"],
            0.1,
        )
        self.assertLess(
            record["maximum_allowed_same_shell_angular_separation"],
            1.0e-3,
        )

    def test_certificate(self):
        certificate = static_patch_scalar_common_mode_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("does not derive", certificate["claim_boundary"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-scalar-common-mode"])
        self.assertEqual(args.radius, 1.0)
        self.assertEqual(args.stretched_distance, 0.05)
        self.assertEqual(args.angular_separation, 0.1)
        self.assertEqual(args.maximum_dimension, 4096)

    def test_validation(self):
        with self.assertRaises(ValueError):
            zero_frequency_scalar_correlation(-1.0)
        with self.assertRaises(ValueError):
            same_shell_optical_distance_over_radius(
                0.1,
                pi + 0.1,
                radius=1.0,
            )
        with self.assertRaises(ValueError):
            static_patch_scalar_common_mode_certificate(maximum_dimension=4)


if __name__ == "__main__":
    unittest.main()
