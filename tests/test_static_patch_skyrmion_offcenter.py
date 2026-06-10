import unittest
from math import exp, sqrt

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_gradient_torque import (
    gradient_zero_frequency_correlations,
)
from qgtoy.static_patch_skyrmion_offcenter import (
    axis_translation_first_order_source_change,
    gradient_spectral_correlations,
    inverse_axis_transvection_coordinates,
    spectral_spherical_function_derivatives,
    skyrmion_two_center_kossakowski_matrix,
    static_patch_skyrmion_offcenter_certificate,
)


class StaticPatchSkyrmionOffcenterTest(unittest.TestCase):
    def test_first_order_translation_matches_exact_boost(self):
        y = 0.4
        cosine = 0.3
        sine = sqrt(1.0 - cosine * cosine)
        source = y * exp(-0.7 * y)
        derivative = exp(-0.7 * y) * (1.0 - 0.7 * y)
        delta_z, delta_x = axis_translation_first_order_source_change(
            source,
            derivative,
            y,
            cosine,
        )
        spacing = 1.0e-6
        translated_y, translated_x, translated_z = (
            inverse_axis_transvection_coordinates(y, cosine, spacing)
        )
        translated_source = translated_y * exp(-0.7 * translated_y)
        numerical_z = (translated_source * translated_z - source * cosine) / spacing
        numerical_x = (translated_source * translated_x - source * sine) / spacing
        self.assertAlmostEqual(delta_z, numerical_z, places=5)
        self.assertAlmostEqual(delta_x, numerical_x, places=5)

    def test_origin_limit_and_large_collinear_translation(self):
        self.assertEqual(
            axis_translation_first_order_source_change(
                0.0, 2.5, 0.0, 0.4
            ),
            (-2.5, 0.0),
        )
        with self.assertRaises(ValueError):
            axis_translation_first_order_source_change(
                1.0, 0.0, 0.0, 0.4
            )
        translated_y, translated_x, translated_z = (
            inverse_axis_transvection_coordinates(19.0, 1.0, 20.0)
        )
        self.assertAlmostEqual(translated_y, 1.0)
        self.assertAlmostEqual(translated_x, 0.0)
        self.assertAlmostEqual(translated_z, -1.0)
        at_origin = inverse_axis_transvection_coordinates(10.0, 1.0, 10.0)
        self.assertAlmostEqual(at_origin[0], 0.0)
        self.assertEqual(at_origin[1:], (0.0, 0.0))

    def test_zero_frequency_reduces_to_existing_theorem(self):
        for distance in (0.0, 0.01, 0.2, 1.0, 711.0):
            actual = gradient_spectral_correlations(0.0, distance)
            expected = gradient_zero_frequency_correlations(distance)
            self.assertAlmostEqual(actual[0], expected[0], places=9)
            self.assertAlmostEqual(actual[1], expected[1], places=9)

    def test_arbitrary_frequency_derivatives_against_finite_differences(self):
        p = 1.3
        y = 0.8
        value, first, second = spectral_spherical_function_derivatives(p, y)
        spacing = 1.0e-4

        def phi(radius):
            return spectral_spherical_function_derivatives(p, radius)[0]

        finite_first = (phi(y + spacing) - phi(y - spacing)) / (2.0 * spacing)
        finite_second = (
            phi(y + spacing) - 2.0 * value + phi(y - spacing)
        ) / spacing**2
        self.assertAlmostEqual(first, finite_first, places=7)
        self.assertAlmostEqual(second, finite_second, places=6)
        self.assertEqual(
            gradient_spectral_correlations(10.0, 1.0e308),
            (0.0, 0.0),
        )

    def test_small_distance_coefficients(self):
        p = 1.7
        y = 1.0e-5
        longitudinal, transverse = gradient_spectral_correlations(p, y)
        self.assertAlmostEqual(
            (1.0 - longitudinal) / y**2,
            (3.0 * p**2 + 7.0) / 10.0,
            places=5,
        )
        self.assertAlmostEqual(
            (1.0 - transverse) / y**2,
            (p**2 + 4.0) / 10.0,
            places=5,
        )

    def test_two_center_matrix_is_symmetric_with_isotropic_auto_blocks(self):
        matrix = skyrmion_two_center_kossakowski_matrix(0.7, 0.2)
        for row in range(6):
            for column in range(6):
                self.assertEqual(matrix[row][column], matrix[column][row])
        self.assertEqual(matrix[0][0], matrix[1][1])
        self.assertEqual(matrix[1][1], matrix[2][2])
        self.assertEqual(matrix[3][3], matrix[4][4])
        self.assertEqual(matrix[4][4], matrix[5][5])
        self.assertLessEqual(abs(matrix[0][3]), matrix[0][0])
        self.assertLessEqual(abs(matrix[2][5]), matrix[2][2])

    def test_certificate_and_cli(self):
        certificate = static_patch_skyrmion_offcenter_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["executable_checks"].values()))
        args = build_parser().parse_args(["static-patch-skyrmion-offcenter"])
        self.assertEqual(args.frequency, 0.7)
        self.assertEqual(args.center_distance, 0.2)

    def test_validation(self):
        with self.assertRaises(ValueError):
            gradient_spectral_correlations(-1.0, 0.2)
        with self.assertRaises(ValueError):
            inverse_axis_transvection_coordinates(0.2, 2.0, 0.1)
        with self.assertRaises(ValueError):
            inverse_axis_transvection_coordinates(500.0, 0.0, 300.0)
        with self.assertRaises(ValueError):
            gradient_spectral_correlations(1.0e151, 0.2)
        with self.assertRaises(ValueError):
            gradient_spectral_correlations(1.0e7, 0.2)
        with self.assertRaises(ValueError):
            static_patch_skyrmion_offcenter_certificate(
                center_distance_over_radius=0.0
            )


if __name__ == "__main__":
    unittest.main()
