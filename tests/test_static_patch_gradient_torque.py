import unittest
from math import exp

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_gradient_torque import (
    gradient_zero_frequency_correlations,
    maximum_gradient_distance_for_defect,
    maximum_gradient_distance_for_spin_half_mismatch,
    spin_half_singlet_survival_probability,
    spin_half_three_axis_mismatch_lower_bound,
    static_patch_gradient_torque_certificate,
    static_patch_gradient_torque_record,
    zero_mode_kernel_derivatives,
)
from qgtoy.static_patch_scalar_common_mode import zero_frequency_scalar_correlation


class StaticPatchGradientTorqueTest(unittest.TestCase):
    def test_kernel_derivatives_match_finite_differences(self):
        for distance in (0.1, 0.5, 1.0, 3.0):
            step = 1.0e-5
            center = zero_frequency_scalar_correlation(distance)
            left = zero_frequency_scalar_correlation(distance - step)
            right = zero_frequency_scalar_correlation(distance + step)
            numerical_first = (right - left) / (2.0 * step)
            numerical_second = (right - 2.0 * center + left) / step**2
            first, second = zero_mode_kernel_derivatives(distance)
            self.assertAlmostEqual(first, numerical_first, places=8)
            self.assertAlmostEqual(second, numerical_second, places=5)

    def test_gradient_correlations_have_isotropic_coincidence(self):
        self.assertEqual(gradient_zero_frequency_correlations(0.0), (1.0, 1.0))
        for distance in (0.1, 0.5, 1.0, 2.0, 4.0):
            longitudinal, transverse = gradient_zero_frequency_correlations(distance)
            self.assertLessEqual(abs(longitudinal), 1.0)
            self.assertLessEqual(abs(transverse), 1.0)

    def test_small_distance_coefficients(self):
        distance = 1.0e-3
        longitudinal, transverse = gradient_zero_frequency_correlations(distance)
        self.assertAlmostEqual((1.0 - longitudinal) / distance**2, 0.7, places=6)
        self.assertAlmostEqual((1.0 - transverse) / distance**2, 0.4, places=6)

    def test_defect_inversion(self):
        for component in ("longitudinal", "transverse"):
            target = 0.02
            distance = maximum_gradient_distance_for_defect(
                target,
                component=component,
            )
            index = 0 if component == "longitudinal" else 1
            defect = 1.0 - gradient_zero_frequency_correlations(distance)[index]
            self.assertAlmostEqual(defect, target, places=12)

    def test_large_transverse_defect_is_bracketed(self):
        distance = maximum_gradient_distance_for_defect(
            0.8,
            component="transverse",
        )
        defect = 1.0 - gradient_zero_frequency_correlations(distance)[1]
        self.assertGreater(distance, 2.0)
        self.assertAlmostEqual(defect, 0.8, places=12)

    def test_spin_half_singlet_exact_limits(self):
        self.assertEqual(
            spin_half_singlet_survival_probability(
                2.0,
                longitudinal_correlation=1.0,
                transverse_correlation=1.0,
            ),
            1.0,
        )
        time = 1.0
        expected = (1.0 + 3.0 * exp(-4.0 * time)) / 4.0
        actual = spin_half_singlet_survival_probability(
            time,
            longitudinal_correlation=0.0,
            transverse_correlation=0.0,
        )
        self.assertAlmostEqual(actual, expected, places=14)

    def test_spin_half_witness_matches_independent_sample(self):
        survival = spin_half_singlet_survival_probability(
            0.7,
            longitudinal_correlation=0.8,
            transverse_correlation=0.9,
        )
        self.assertAlmostEqual(survival, 0.7667717926229308, places=14)

    def test_spin_half_small_distance_coefficient(self):
        distance = 1.0e-3
        time = 0.75
        mismatch = spin_half_three_axis_mismatch_lower_bound(
            time,
            center_distance_over_radius=distance,
        )
        self.assertAlmostEqual(
            mismatch / (time * distance**2),
            1.5,
            places=5,
        )

    def test_spin_half_mismatch_inversion(self):
        target = 0.01
        time = 1.25
        distance = maximum_gradient_distance_for_spin_half_mismatch(
            target,
            dimensionless_time=time,
        )
        self.assertIsNotNone(distance)
        mismatch = spin_half_three_axis_mismatch_lower_bound(
            time,
            center_distance_over_radius=distance,
        )
        self.assertAlmostEqual(mismatch, target, places=11)

    def test_loose_axiswise_witness_reports_no_distance_bound(self):
        record = static_patch_gradient_torque_record(
            3,
            center_distance_over_radius=0.2,
        )
        self.assertIsNone(
            record["maximum_longitudinal_center_distance_over_radius"]
        )
        self.assertIsNone(record["maximum_transverse_center_distance_over_radius"])

    def test_fixed_separation_fails_large_dimension(self):
        record = static_patch_gradient_torque_record(
            4096,
            center_distance_over_radius=0.2,
        )
        self.assertFalse(record["passes_imported_axiswise_axial_allocation"])
        self.assertGreater(
            record["longitudinal_axiswise_axial_surrogate_mismatch"],
            record["allocated_mismatch_A_over_d"],
        )
        self.assertFalse(record["passes_exact_spin_half_three_axis_allocation"])
        self.assertGreater(
            record["spin_half_singlet_three_axis_mismatch_lower_bound"],
            record["allocated_mismatch_A_over_d"],
        )

    def test_certificate(self):
        certificate = static_patch_gradient_torque_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("does not identify", certificate["claim_boundary"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-gradient-torque"])
        self.assertEqual(args.center_distance_over_radius, 0.2)
        self.assertEqual(args.maximum_dimension, 4096)

    def test_validation(self):
        with self.assertRaises(ValueError):
            gradient_zero_frequency_correlations(-1.0)
        with self.assertRaises(ValueError):
            maximum_gradient_distance_for_defect(1.0)
        with self.assertRaises(ValueError):
            maximum_gradient_distance_for_defect(0.1, component="radial")
        with self.assertRaises(ValueError):
            static_patch_gradient_torque_certificate(maximum_dimension=8)


if __name__ == "__main__":
    unittest.main()
