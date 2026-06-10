import unittest
from math import exp, pi

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_skyrmion_bath import (
    dipole_angular_projection_coefficients,
    numerical_dipole_angular_projection_coefficient,
    optical_dipole_kernel,
    skyrmion_current_gradient_spectrum,
    skyrmion_current_optical_form_factor,
    static_patch_skyrmion_bath_certificate,
)


class StaticPatchSkyrmionBathTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = static_patch_skyrmion_bath_certificate()

    def test_angular_projection_identity(self):
        direct, integrated = dipole_angular_projection_coefficients(
            optical_radius_ratio=0.2
        )
        self.assertAlmostEqual(direct, integrated)
        numerical = numerical_dipole_angular_projection_coefficient(
            optical_radius_ratio=0.2
        )
        self.assertAlmostEqual(direct, numerical, places=10)

    def test_kernel_has_regular_origin(self):
        self.assertEqual(optical_dipole_kernel(2.0, 0.0), 0.0)
        small = optical_dipole_kernel(2.0, 1.0e-6)
        self.assertGreater(small, 0.0)

    def test_form_factor_is_even(self):
        self.assertAlmostEqual(
            skyrmion_current_optical_form_factor(5.0),
            skyrmion_current_optical_form_factor(-5.0),
        )

    def test_matter_spectrum_is_kms_and_positive(self):
        positive = skyrmion_current_gradient_spectrum(0.7)
        negative = skyrmion_current_gradient_spectrum(-0.7)
        self.assertGreater(positive, 0.0)
        self.assertAlmostEqual(negative / positive, exp(-2.0 * pi * 0.7))

    def test_default_prediction_and_simple_zero(self):
        record = self.certificate["record"]
        self.assertAlmostEqual(
            record["optical_wall_radius_over_de_sitter_radius"],
            0.2027325540540822,
        )
        self.assertAlmostEqual(
            record["proper_wall_radius_in_inverse_e_fpi"],
            4.027158415806616,
        )
        self.assertAlmostEqual(record["zero_mode_form_factor"], 1.0032955447330436)
        self.assertAlmostEqual(
            record["zero_frequency_rate_ratio"],
            1.0066019500811747,
        )
        self.assertAlmostEqual(
            record["first_form_factor_zero"],
            275.0092203709643,
            places=6,
        )
        self.assertLess(record["form_factor_derivative_at_first_zero"], 0.0)
        self.assertGreater(
            record["form_factor_absolute_value_derivative_jump"],
            0.0,
        )

    def test_nondefault_certificate_forwards_profile_parameters(self):
        certificate = static_patch_skyrmion_bath_certificate(curvature=0.001)
        self.assertEqual(certificate["status"], "pass")
        self.assertGreater(certificate["record"]["first_form_factor_zero"], 300.0)
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_certificate_and_cli(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        args = build_parser().parse_args(["static-patch-skyrmion-bath"])
        self.assertEqual(args.pion_mass, 1.0)
        self.assertEqual(args.curvature, 0.0025)
        self.assertEqual(args.wall_radius, 4.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            dipole_angular_projection_coefficients(optical_radius_ratio=0.0)
        with self.assertRaises(ValueError):
            skyrmion_current_optical_form_factor(1.0, curvature=0.0)
        with self.assertRaises(ValueError):
            skyrmion_current_gradient_spectrum(0.1, radius=0.0)


if __name__ == "__main__":
    unittest.main()
