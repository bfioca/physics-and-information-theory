import unittest
from math import ceil

from qgtoy.operational_phase_reference import (
    optimal_phase_pair_recovery_record,
    optimal_phase_pair_error,
    optimal_phase_reference_amplitudes,
    operational_phase_reference_certificate,
    phase_pair_recovery_record,
    phase_reference_channel_record,
    phase_reference_visibility,
    required_optimized_reference_max_charge,
    required_reference_dimension,
    total_charge_overlap_count,
)


class OperationalPhaseReferenceTest(unittest.TestCase):
    def test_overlap_count_and_visibility_follow_triangular_law(self):
        level = 4
        reference_max_charge = 11
        for left in range(-level, level + 1):
            for right in range(-level, level + 1):
                gap = abs(left - right)
                expected_count = max(0, reference_max_charge + 1 - gap)
                self.assertEqual(
                    total_charge_overlap_count(
                        level,
                        reference_max_charge,
                        left,
                        right,
                    ),
                    expected_count,
                )
                self.assertAlmostEqual(
                    phase_reference_visibility(
                        level,
                        reference_max_charge,
                        left,
                        right,
                    ),
                    expected_count / (reference_max_charge + 1),
                )

    def test_visibility_matrix_is_the_shifted_window_gram_matrix(self):
        for level in range(1, 6):
            record = phase_reference_channel_record(level, 3 * level)
            self.assertTrue(record["visibility_is_reference_window_gram_matrix"])
            self.assertTrue(record["channel_is_cptp"])
            self.assertLess(record["gram_matrix_error"], 1e-14)

    def test_scalar_reference_reproduces_half_error_obstruction(self):
        for level in range(1, 8):
            record = phase_pair_recovery_record(level, 0)
            self.assertEqual(record["decoded_plus_minus_trace_distance"], 0.0)
            self.assertEqual(
                record["any_decoder_worst_case_trace_distance_error_lower_bound"],
                0.5,
            )

    def test_sector_decoder_saturates_phase_pair_lower_bound(self):
        level = 5
        reference_max_charge = 24
        record = phase_pair_recovery_record(level, reference_max_charge)
        self.assertAlmostEqual(record["decoded_plus_minus_trace_distance"], 0.6)
        self.assertAlmostEqual(
            record["any_decoder_worst_case_trace_distance_error_lower_bound"],
            0.2,
        )
        self.assertAlmostEqual(record["sector_decoder_error_on_each_phase_state"], 0.2)
        self.assertTrue(record["sector_decoder_is_pairwise_minimax_optimal"])

    def test_reference_dimension_threshold_is_exact_for_extremal_pair(self):
        for level in range(1, 12):
            for target_error in (0.4, 0.2, 0.1, 0.03):
                dimension = required_reference_dimension(level, target_error)
                self.assertEqual(dimension, ceil(level / target_error))
                achieved = phase_pair_recovery_record(level, dimension - 1)
                self.assertLessEqual(
                    achieved["sector_decoder_error_on_each_phase_state"],
                    target_error + 1e-15,
                )
                if dimension > 1:
                    previous = phase_pair_recovery_record(level, dimension - 2)
                    self.assertGreater(
                        previous["sector_decoder_error_on_each_phase_state"],
                        target_error,
                    )

    def test_no_finite_uniform_reference_is_exact_on_nonzero_gap(self):
        for reference_max_charge in (0, 1, 3, 10, 100):
            record = phase_pair_recovery_record(
                3,
                reference_max_charge,
                left_charge=-1,
                right_charge=2,
            )
            self.assertFalse(record["exact_pair_recovery"])

    def test_sine_profile_attains_exact_pairwise_optimum(self):
        for level in range(1, 6):
            for reference_max_charge in (0, 2 * level, 5 * level, 11 * level):
                amplitudes = optimal_phase_reference_amplitudes(
                    level,
                    reference_max_charge,
                )
                self.assertAlmostEqual(
                    sum(value * value for value in amplitudes),
                    1.0,
                )
                record = optimal_phase_pair_recovery_record(
                    level,
                    reference_max_charge,
                )
                self.assertLess(record["visibility_error"], 1e-14)

    def test_optimized_charge_threshold_is_exact(self):
        for level in range(1, 8):
            for target_error in (0.4, 0.25, 0.1, 0.03):
                maximum_charge = required_optimized_reference_max_charge(
                    level,
                    target_error,
                )
                achieved = optimal_phase_pair_recovery_record(level, maximum_charge)
                self.assertLessEqual(
                    achieved["optimal_pairwise_minimax_error"],
                    target_error + 1e-14,
                )
                if maximum_charge > 0:
                    previous = optimal_phase_pair_recovery_record(
                        level,
                        maximum_charge - 1,
                    )
                    self.assertGreater(
                        previous["optimal_pairwise_minimax_error"],
                        target_error,
                    )

    def test_optimized_threshold_handles_spectral_boundaries(self):
        boundary = 0.25
        just_below = boundary - 1e-13
        self.assertEqual(required_optimized_reference_max_charge(3, boundary), 6)
        self.assertEqual(required_optimized_reference_max_charge(3, just_below), 12)
        tiny_target = 1e-20
        maximum_charge = required_optimized_reference_max_charge(1, tiny_target)
        self.assertLessEqual(
            optimal_phase_pair_error(1, maximum_charge),
            tiny_target,
        )

    def test_certificate_passes_with_explicit_boundary(self):
        certificate = operational_phase_reference_certificate(
            max_level=8,
            target_error=0.1,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("not a full-space", certificate["claim_boundary"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            phase_reference_channel_record(0, 1)
        with self.assertRaises(ValueError):
            phase_reference_channel_record(1, -1)
        with self.assertRaises(ValueError):
            phase_reference_visibility(2, 4, -3, 1)
        with self.assertRaises(ValueError):
            phase_pair_recovery_record(2, 4, 1, 1)
        with self.assertRaises(ValueError):
            required_reference_dimension(2, 0.5)
        with self.assertRaises(ValueError):
            operational_phase_reference_certificate(target_error=0.0)


if __name__ == "__main__":
    unittest.main()
