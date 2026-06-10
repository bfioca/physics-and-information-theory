import unittest
from math import tanh

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_skyrmion_tail import (
    skyrmion_optical_endpoint_record,
    skyrmion_sharp_form_factor_tail_envelope,
    static_patch_skyrmion_tail_certificate,
)


class StaticPatchSkyrmionTailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = static_patch_skyrmion_tail_certificate()

    def test_endpoint_record_is_pinned(self):
        endpoint = self.certificate["endpoint_record"]
        self.assertAlmostEqual(endpoint["optical_wall"], 0.202732554054)
        self.assertAlmostEqual(
            endpoint["wall_profile_slope_magnitude"],
            0.08787579979,
            places=8,
        )
        self.assertAlmostEqual(
            endpoint["wall_weight_second_derivative"],
            245.5560092,
            places=4,
        )
        self.assertAlmostEqual(
            endpoint["leading_form_factor_tail_amplitude"],
            8599.3544,
            places=2,
        )

    def test_exact_envelope_formula_and_radius_scaling(self):
        envelope = skyrmion_sharp_form_factor_tail_envelope(
            prefactor=2.0,
            optical_wall=0.2,
            wall_weight_second=3.0,
            a_third_derivative_l1=(5.0, 7.0, 11.0),
            w_third_derivative_l1=(13.0, 17.0, 19.0),
            tail_start=4.0,
            radius=2.0,
        )
        self.assertEqual(
            envelope["result_type"],
            "float_evaluation_of_exact_p_minus_five_envelope",
        )
        self.assertEqual(len(envelope["form_factor_derivative_coefficients"]), 3)
        b_bounds = envelope["b_transform_bounds"]
        d_bounds = envelope["d_transform_bounds"]
        self.assertEqual(b_bounds, (16.0, 17.6, 19.12))
        self.assertAlmostEqual(d_bounds[0], 3.0 / tanh(0.2) + 5.0)
        self.assertAlmostEqual(d_bounds[1], 0.6 / tanh(0.2) + 7.0)
        self.assertAlmostEqual(d_bounds[2], 0.12 / tanh(0.2) + 11.0)
        numerator = envelope["numerator_derivative_coefficients"]
        self.assertAlmostEqual(numerator[0], b_bounds[0] + d_bounds[0] / 4.0)
        self.assertAlmostEqual(
            numerator[1],
            b_bounds[1] + d_bounds[1] / 4.0 + d_bounds[0] / 16.0,
        )
        self.assertAlmostEqual(
            numerator[2],
            b_bounds[2]
            + d_bounds[2] / 4.0
            + 2.0 * d_bounds[1] / 16.0
            + 2.0 * d_bounds[0] / 64.0,
        )
        expected_sequences = {
            "form_factor_derivative_coefficients": (
                42.099734345159206,
                63.79474762790125,
                106.34871043622354,
            ),
            "positive_signed_factor_coefficients": (
                7.016622390859867,
                17.736788108729158,
                57.67414617312775,
            ),
            "negative_signed_factor_coefficients": (
                7.016622390859867,
                39.78015746486817,
                238.36895984406507,
            ),
            "squared_dimensionless_h2_tail_bounds": (
                0.004006590964836917,
                0.07719134848403576,
                2.447349778399284,
            ),
        }
        for key, expected in expected_sequences.items():
            for actual, target in zip(envelope[key], expected):
                self.assertAlmostEqual(actual, target)
        dimensionless = envelope["squared_dimensionless_h2_tail_bounds"]
        physical = envelope["squared_physical_h2_tail_bounds"]
        self.assertAlmostEqual(physical[0], dimensionless[0] / 16.0)
        self.assertAlmostEqual(physical[1], dimensionless[1] / 4.0)
        self.assertAlmostEqual(physical[2], dimensionless[2])
        self.assertTrue(all(value > 0.0 for value in physical))

    def test_certificate_and_cli(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["executable_checks"].values()))
        self.assertEqual(len(self.certificate["analytic_theorem_results"]), 3)
        self.assertEqual(self.certificate["required_derivative_norm_count"], 6)
        args = build_parser().parse_args(["static-patch-skyrmion-tail"])
        self.assertEqual(args.curvature, 0.0025)
        self.assertEqual(args.wall_radius, 4.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            skyrmion_optical_endpoint_record(curvature=0.0)
        with self.assertRaises(ValueError):
            skyrmion_sharp_form_factor_tail_envelope(
                prefactor=1.0,
                optical_wall=0.2,
                wall_weight_second=1.0,
                a_third_derivative_l1=(1.0, 2.0, 3.0),
                w_third_derivative_l1=(1.0, 2.0, 3.0),
                tail_start=0.5,
            )


if __name__ == "__main__":
    unittest.main()
