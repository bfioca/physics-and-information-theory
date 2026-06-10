import math
import unittest

from qgtoy.__main__ import build_parser
from qgtoy.skyrmion_radial_dynamical_gap import (
    generalized_radial_frequency_squared_lower_bound,
    radial_fluctuation_kinetic_weight,
    skyrmion_radial_dynamical_gap_certificate,
    supported_radial_frequency_squared_lower_bound,
    unbounded_kinetic_weight_counterexample,
    uniform_radial_kinetic_weight_upper_bound,
)


class SkyrmionRadialDynamicalGapTest(unittest.TestCase):
    def test_exact_radial_kinetic_weight(self):
        self.assertAlmostEqual(
            radial_fluctuation_kinetic_weight(
                2.0,
                math.pi / 2.0,
                curvature=0.0025,
            ),
            12.0 / 0.99,
        )

    def test_hard_support_weight_bound_dominates_samples(self):
        upper = uniform_radial_kinetic_weight_upper_bound(
            wall_radius=4.0,
            curvature=0.0025,
        )
        self.assertAlmostEqual(upper, 25.0)
        for radius, profile in (
            (0.0, math.pi),
            (0.1, math.pi / 2.0),
            (2.0, math.pi / 2.0),
            (3.999, 1.3),
            (4.0, 0.0),
        ):
            self.assertLessEqual(
                radial_fluctuation_kinetic_weight(
                    radius,
                    profile,
                    curvature=0.0025,
                ),
                upper + 1e-12,
            )

    def test_generalized_gap_conversion(self):
        self.assertAlmostEqual(
            generalized_radial_frequency_squared_lower_bound(
                static_jacobi_form_gap=2.0,
                kinetic_weight_upper_bound=8.0,
            ),
            0.25,
        )
        self.assertAlmostEqual(
            supported_radial_frequency_squared_lower_bound(
                static_jacobi_form_gap=1.0,
                wall_radius=4.0,
                curvature=0.0025,
            ),
            0.04,
        )

    def test_static_gap_without_weight_bound_has_no_frequency_floor(self):
        records = tuple(
            unbounded_kinetic_weight_counterexample(
                static_jacobi_form_gap=1.0,
                kinetic_weight_scale=scale,
            )
            for scale in (1.0, 10.0, 1000.0, 1e6)
        )
        self.assertTrue(
            all(
                right["generalized_frequency_squared"]
                < left["generalized_frequency_squared"]
                for left, right in zip(records, records[1:])
            )
        )
        self.assertEqual(records[-1]["generalized_frequency_squared"], 1e-6)

    def test_certificate_preserves_domain_caveat(self):
        certificate = skyrmion_radial_dynamical_gap_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertEqual(
            certificate["current_evidence"]["physical_radial_dynamic_gap"],
            "open",
        )
        self.assertAlmostEqual(
            certificate["clean_truncated_frequency_from_au1_target_one"],
            0.2,
        )
        self.assertAlmostEqual(
            certificate[
                "certified_truncated_approximate_profile_frequency_squared"
            ],
            1.0235900944571767 / 25.0,
        )
        self.assertIn("conditional", certificate["claim_boundary"])

    def test_cli_registration(self):
        args = build_parser().parse_args(["skyrmion-radial-dynamical-gap"])
        self.assertEqual(args.wall_radius, 4.0)
        self.assertAlmostEqual(args.barta_lower_bound, 1.0235900944571767)

    def test_validation(self):
        with self.assertRaises(ValueError):
            radial_fluctuation_kinetic_weight(
                20.0,
                0.0,
                curvature=0.0025,
            )
        with self.assertRaises(ValueError):
            uniform_radial_kinetic_weight_upper_bound(
                wall_radius=20.0,
                curvature=0.0025,
            )
        with self.assertRaises(ValueError):
            generalized_radial_frequency_squared_lower_bound(
                static_jacobi_form_gap=1.0,
                kinetic_weight_upper_bound=0.0,
            )


if __name__ == "__main__":
    unittest.main()
