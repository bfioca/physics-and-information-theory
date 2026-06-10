from math import exp
import unittest

from qgtoy.__main__ import build_parser
from qgtoy.finite_time_rotation_diffusion import (
    finite_time_energy_constrained_recovery_record,
    finite_time_rotation_diffusion_certificate,
    finite_time_twirl_distance_record,
    logarithmic_diffusion_schedule_record,
    minimum_diffusion_time_for_twirl_distance,
    so3_heat_multiplier,
    so3_heat_kernel_l2_distance_upper_bound,
)


class FiniteTimeRotationDiffusionTest(unittest.TestCase):
    def test_heat_kernel_distance_bound_decreases(self):
        values = tuple(
            finite_time_twirl_distance_record(time, diffusion_rate=0.7)[
                "normalized_diamond_distance_to_haar_upper_bound"
            ]
            for time in (0.0, 0.5, 1.0, 2.0, 4.0)
        )
        self.assertEqual(values[0], 1.0)
        self.assertTrue(all(right <= left for left, right in zip(values, values[1:])))
        self.assertLess(values[-1], 0.01)

    def test_closed_l2_bound_dominates_partial_peter_weyl_sum(self):
        dimensionless_time = 0.4
        partial_squared = sum(
            (2 * spin + 1) ** 2
            * exp(
                -2.0 * dimensionless_time * spin * (spin + 1)
            )
            for spin in range(1, 100)
        )
        self.assertLessEqual(
            partial_squared**0.5,
            so3_heat_kernel_l2_distance_upper_bound(dimensionless_time),
        )

    def test_heat_multipliers_obey_semigroup_law_and_haar_limit(self):
        for rank in range(6):
            self.assertEqual(so3_heat_multiplier(rank, 0.0), 1.0)
            self.assertAlmostEqual(
                so3_heat_multiplier(rank, 0.7),
                so3_heat_multiplier(rank, 0.2)
                * so3_heat_multiplier(rank, 0.5),
                places=14,
            )
        self.assertEqual(so3_heat_multiplier(0, 50.0), 1.0)
        self.assertTrue(
            all(so3_heat_multiplier(rank, 50.0) < 1.0e-30 for rank in range(1, 6))
        )

    def test_tiny_positive_time_returns_infinite_bound_without_overflow(self):
        self.assertEqual(
            so3_heat_kernel_l2_distance_upper_bound(1.0e-300),
            float("inf"),
        )

    def test_mixing_time_meets_requested_distance(self):
        target = 0.03
        rate = 0.8
        mixing_time = minimum_diffusion_time_for_twirl_distance(
            target,
            diffusion_rate=rate,
        )
        at_time = finite_time_twirl_distance_record(
            mixing_time,
            diffusion_rate=rate,
        )["normalized_diamond_distance_to_haar_upper_bound"]
        before = finite_time_twirl_distance_record(
            0.999 * mixing_time,
            diffusion_rate=rate,
        )["normalized_diamond_distance_to_haar_upper_bound"]
        self.assertLessEqual(at_time, target)
        self.assertGreater(before, target)

    def test_finite_time_correction_transfers_haar_bound(self):
        early = finite_time_energy_constrained_recovery_record(
            200,
            maximum_mean_casimir=10.0,
            proper_time=0.0,
            diffusion_rate=1.0,
        )
        late = finite_time_energy_constrained_recovery_record(
            200,
            maximum_mean_casimir=10.0,
            proper_time=4.0,
            diffusion_rate=1.0,
        )
        self.assertEqual(early["finite_time_any_decoder_error_lower_bound"], 0.0)
        self.assertGreater(late["finite_time_any_decoder_error_lower_bound"], 0.4)
        self.assertLessEqual(
            late["finite_time_any_decoder_error_lower_bound"],
            late["haar_energy_constrained_error_lower_bound"],
        )

    def test_logarithmic_schedule_has_inverse_dimension_correction(self):
        for spin in (2, 10, 100, 1000):
            record = logarithmic_diffusion_schedule_record(
                spin,
                maximum_mean_casimir=5.0,
                diffusion_rate=2.0,
            )
            self.assertTrue(
                record["computed_bound_respects_elementary_schedule_bound"]
            )
            self.assertLess(
                record["finite_time_twirl_distance_upper_bound"],
                2.0 / record["system_dimension_d"],
            )

    def test_certificate(self):
        certificate = finite_time_rotation_diffusion_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("not yet derived", certificate["claim_boundary"])
        self.assertIn("spatially local", certificate["next_physics_gate"])
        self.assertIn("sufficient_protocol_time_scaling", certificate)
        self.assertNotIn("observable_scaling_consequence", certificate)

    def test_cli_defaults(self):
        args = build_parser().parse_args(["finite-time-rotation-diffusion"])
        self.assertEqual(args.maximum_system_spin, 512)
        self.assertEqual(args.maximum_mean_casimir, 10.0)
        self.assertEqual(args.diffusion_rate, 1.0)
        self.assertEqual(args.target_twirl_distance, 0.05)

    def test_validation(self):
        with self.assertRaises(ValueError):
            finite_time_twirl_distance_record(-1.0, diffusion_rate=1.0)
        with self.assertRaises(ValueError):
            minimum_diffusion_time_for_twirl_distance(1.0, diffusion_rate=1.0)
        with self.assertRaises(ValueError):
            finite_time_rotation_diffusion_certificate(maximum_system_spin=0)


if __name__ == "__main__":
    unittest.main()
