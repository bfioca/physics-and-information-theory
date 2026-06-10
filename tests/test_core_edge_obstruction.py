import unittest
from math import log

from qgtoy.core_edge_obstruction import (
    core_conditional_expectation_record,
    core_edge_obstruction_certificate,
    core_observer_algebra_hierarchy_record,
    factorized_modular_core_record,
    full_rotation_core_obstruction_record,
    time_axial_core_obstruction_record,
)


class CoreEdgeObstructionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = core_edge_obstruction_certificate(max_level=8)

    def test_certificate_passes_with_factorized_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["finite_verified_claims"].values()))
        self.assertTrue(
            all(self.certificate["theorem_backed_core_claims"].values())
        )
        self.assertIn("no interaction", self.certificate["claim_boundary"])

    def test_factorized_continuous_core_has_the_expected_type(self):
        for level in range(1, 7):
            record = factorized_modular_core_record(level)
            self.assertEqual(record["precore_type"], "hyperfinite Type III_1 factor")
            self.assertEqual(
                record["continuous_core_type"],
                "hyperfinite Type II_infinity factor",
            )
            self.assertTrue(record["dual_clock_acts_only_on_core_factor"])
            self.assertIn("ordinary Tr_N", record["working_core_trace_scaling"])

    def test_angular_expectations_extend_trace_preservingly(self):
        record = core_conditional_expectation_record(4)
        self.assertTrue(record["state_preserving"])
        self.assertTrue(record["commutes_with_modular_flow"])
        self.assertTrue(record["core_trace_preserving"])
        self.assertFalse(record["clock_restores_discarded_angular_data"])

    def test_core_amplification_preserves_the_angular_centers(self):
        for level in range(1, 8):
            record = core_observer_algebra_hierarchy_record(level)
            self.assertEqual(
                record["time_then_axial_hidden_center_dimension"],
                (level + 1) ** 2,
            )
            self.assertEqual(
                record["full_rotation_hidden_center_dimension"],
                level + 1,
            )
            self.assertTrue(
                record["angular_fixed_point_lattice_is_unchanged_by_clock_core"]
            )

    def test_time_axial_phase_pair_has_log_two_core_entropy_loss(self):
        for level in range(1, 8):
            record = time_axial_core_obstruction_record(level)
            self.assertAlmostEqual(
                record["relative_entropy_to_time_axial_expected_state"],
                log(2.0),
            )
            self.assertTrue(record["core_density_has_finite_entropy"])
            self.assertEqual(record["lifted_input_trace_distance"], 1.0)
            self.assertEqual(
                record["time_axial_expected_output_trace_distance"],
                0.0,
            )
            self.assertEqual(
                record["decoder_worst_case_trace_distance_error_lower_bound"],
                0.5,
            )

    def test_full_rotation_entropy_loss_grows_as_log_irrep_dimension(self):
        losses = []
        for level in range(1, 8):
            record = full_rotation_core_obstruction_record(level)
            self.assertAlmostEqual(
                record["relative_entropy_to_full_rotation_expected_state"],
                log(2 * level + 1),
            )
            self.assertTrue(record["orthogonal_phase_pair_outputs_collide"])
            losses.append(
                record["finite_entropy_increase_under_full_rotation_expectation"]
            )
        self.assertTrue(all(right > left for left, right in zip(losses, losses[1:])))

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            factorized_modular_core_record(0)
        with self.assertRaises(ValueError):
            core_edge_obstruction_certificate(max_level=0)
        with self.assertRaises(ValueError):
            core_edge_obstruction_certificate(tolerance=0.0)


if __name__ == "__main__":
    unittest.main()
