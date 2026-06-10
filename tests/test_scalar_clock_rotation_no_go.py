import unittest

from qgtoy.scalar_clock_rotation_no_go import (
    diagonal_trace_distance,
    fixed_spin_basis_state,
    fixed_spin_replacer_optimal_normalized_diamond_error,
    fixed_spin_so3_twirl,
    scalar_clock_rotation_no_go_certificate,
    scalar_clock_rotation_obstruction_record,
)


class ScalarClockRotationNoGoTest(unittest.TestCase):
    def test_explicit_antipodal_twirl_collision(self):
        plus = fixed_spin_basis_state(4, 4)
        minus = fixed_spin_basis_state(4, -4)
        twirled = fixed_spin_so3_twirl(4)
        self.assertEqual(diagonal_trace_distance(plus, minus), 1.0)
        self.assertEqual(diagonal_trace_distance(twirled, twirled), 0.0)
        self.assertAlmostEqual(sum(twirled), 1.0)

    def test_single_record(self):
        record = scalar_clock_rotation_obstruction_record(
            radius=1.0,
            stretched_distance=1.0 / 256.0,
            energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
        )
        self.assertLessEqual(record["largest_mode_energy_upper_bound"], 4.0)
        self.assertEqual(
            record["all_decoder_worst_case_trace_error_lower_bound"],
            0.5,
        )
        self.assertEqual(record["so3_fixed_point_restriction_distance"], 0.0)
        dimension = record["fixed_spin_sector_dimension"]
        self.assertAlmostEqual(
            record["full_fixed_spin_optimal_normalized_diamond_error"],
            1.0 - 1.0 / (dimension * dimension),
        )
        self.assertLessEqual(record["variational_ground_frequency_upper_bound"], 4.0)

    def test_exact_replacer_diamond_error(self):
        self.assertAlmostEqual(
            fixed_spin_replacer_optimal_normalized_diamond_error(4),
            80.0 / 81.0,
        )

    def test_certificate(self):
        certificate = scalar_clock_rotation_no_go_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertEqual(
            certificate["result_type"],
            "conditional_compact_fixed_point_recovery_obstruction",
        )
        self.assertIn("neither", certificate["named_model_boundary"])

    def test_scaling(self):
        records = scalar_clock_rotation_no_go_certificate()["records"]
        self.assertGreater(
            records[-1]["maximum_bounded_energy_spin_L_delta"],
            records[0]["maximum_bounded_energy_spin_L_delta"],
        )
        self.assertGreater(
            records[-1]["coherent_token_missing_frame_relative_entropy"],
            records[0]["coherent_token_missing_frame_relative_entropy"],
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            scalar_clock_rotation_no_go_certificate(steps=2)
        with self.assertRaises(ValueError):
            scalar_clock_rotation_obstruction_record(
                radius=1.0,
                stretched_distance=0.1,
                energy_budget=0.1,
                inner_offset=0.5,
                outer_offset=1.5,
            )


if __name__ == "__main__":
    unittest.main()
