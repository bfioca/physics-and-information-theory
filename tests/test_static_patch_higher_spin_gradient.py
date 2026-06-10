import unittest
from math import exp, log, sqrt

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_higher_spin_gradient import (
    gradient_correlation_defect_sum,
    higher_spin_dyson_remainder_bound,
    higher_spin_dyson_scale,
    higher_spin_exact_gradient_mismatch_lower_bound,
    higher_spin_perturbative_record,
    higher_spin_singlet_survival_probability,
    higher_spin_singlet_linear_leakage,
    higher_spin_singlet_mismatch_lower_bound,
    static_patch_higher_spin_gradient_certificate,
)


class StaticPatchHigherSpinGradientTest(unittest.TestCase):
    def test_zero_separation_is_decoherence_free(self):
        self.assertEqual(gradient_correlation_defect_sum(0.0), 0.0)
        self.assertEqual(
            higher_spin_singlet_mismatch_lower_bound(
                8,
                2.0,
                center_distance_over_radius=0.0,
            ),
            0.0,
        )

    def test_casimir_linear_coefficient(self):
        spin = 5
        time = 0.7
        distance = 1.0e-3
        defect = gradient_correlation_defect_sum(distance)
        expected = 4.0 * spin * (spin + 1) * defect * time / 3.0
        self.assertAlmostEqual(
            higher_spin_singlet_linear_leakage(
                spin,
                time,
                center_distance_over_radius=distance,
            ),
            expected,
            places=15,
        )

    def test_small_distance_coefficient(self):
        spin = 7
        time = 0.4
        distance = 1.0e-4
        leakage = higher_spin_singlet_linear_leakage(
            spin,
            time,
            center_distance_over_radius=distance,
        )
        self.assertAlmostEqual(
            leakage / (time * distance**2),
            2.0 * spin * (spin + 1),
            places=5,
        )

    def test_dyson_remainder_formula(self):
        spin = 3
        time = 0.2
        distance = 2.0e-3
        scale = higher_spin_dyson_scale(
            spin,
            time,
            center_distance_over_radius=distance,
        )
        remainder = higher_spin_dyson_remainder_bound(
            spin,
            time,
            center_distance_over_radius=distance,
        )
        self.assertGreaterEqual(remainder, 0.0)
        self.assertAlmostEqual(remainder, 0.5 * scale**2)

    def test_exact_blocks_fix_perfect_common_mode(self):
        for spin in (1, 2, 3):
            self.assertEqual(
                higher_spin_singlet_survival_probability(
                    spin,
                    1.0e100,
                    longitudinal_correlation=1.0,
                    transverse_correlation=1.0,
                ),
                1.0,
            )

    def test_exact_time_zero_fast_path(self):
        self.assertEqual(
            higher_spin_singlet_survival_probability(
                20,
                0.0,
                longitudinal_correlation=0.1,
                transverse_correlation=-0.2,
            ),
            1.0,
        )

    def test_exact_independent_bath_formula(self):
        time = 0.35
        for spin in (1, 2, 3):
            dimension = 2 * spin + 1
            expected = sum(
                (2 * tensor_rank + 1)
                * exp(-2.0 * tensor_rank * (tensor_rank + 1) * time)
                for tensor_rank in range(2 * spin + 1)
            ) / dimension**2
            actual = higher_spin_singlet_survival_probability(
                spin,
                time,
                longitudinal_correlation=0.0,
                transverse_correlation=0.0,
            )
            self.assertAlmostEqual(actual, expected, places=13)

    def test_exact_small_distance_matches_casimir_slope(self):
        time = 0.2
        distance = 1.0e-4
        for spin in (1, 2, 3):
            mismatch = higher_spin_exact_gradient_mismatch_lower_bound(
                spin,
                time,
                center_distance_over_radius=distance,
            )
            expected_coefficient = 2.0 * spin * (spin + 1) * time
            self.assertAlmostEqual(
                mismatch / distance**2,
                expected_coefficient,
                places=4,
            )

    def test_half_slope_window(self):
        record = higher_spin_perturbative_record(
            32,
            center_distance_over_radius=1.0e-5,
        )
        self.assertTrue(record["inside_half_slope_perturbative_window"])
        self.assertGreaterEqual(
            record["rigorous_singlet_channel_mismatch_lower_bound"],
            record["half_linear_leakage_lower_bound_in_window"],
        )

    def test_half_slope_metadata_uses_reported_window(self):
        record = higher_spin_perturbative_record(
            64,
            center_distance_over_radius=1.0e-4,
        )
        self.assertEqual(
            record["inside_half_slope_perturbative_window"],
            record["gradient_defect_sum_delta_parallel_plus_2_delta_perp"]
            <= record["maximum_defect_for_certified_half_slope_window"],
        )

    def test_exact_mismatch_dominates_duhamel_bound(self):
        for spin in (1, 2, 3, 4):
            exact = higher_spin_exact_gradient_mismatch_lower_bound(
                spin,
                0.2,
                center_distance_over_radius=0.01,
            )
            lower = higher_spin_singlet_mismatch_lower_bound(
                spin,
                0.2,
                center_distance_over_radius=0.01,
            )
            self.assertGreaterEqual(exact + 1.0e-12, lower)

    def test_leading_dimension_scaling(self):
        for spin in (16, 64, 256):
            record = higher_spin_perturbative_record(
                spin,
                center_distance_over_radius=1.0e-7,
            )
            dimension = 2 * spin + 1
            expected = sqrt(
                1.0
                / (dimension * spin * (spin + 1) * log(float(dimension)))
            )
            self.assertAlmostEqual(
                record["leading_small_y_maximum_distance_over_radius"],
                expected,
                places=15,
            )

    def test_certificate(self):
        certificate = static_patch_higher_spin_gradient_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("d^(-3/2)", certificate["scaling_consequence"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-higher-spin-gradient"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.center_distance_over_radius, 1.0e-6)

    def test_validation(self):
        with self.assertRaises(ValueError):
            higher_spin_singlet_linear_leakage(
                0,
                1.0,
                center_distance_over_radius=0.1,
            )
        with self.assertRaises(ValueError):
            static_patch_higher_spin_gradient_certificate(maximum_spin=8)


if __name__ == "__main__":
    unittest.main()
