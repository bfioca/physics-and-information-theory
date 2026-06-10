import unittest

from qgtoy.embedding_channels import (
    approximate_static_patch_embedding_certificate,
    berezin_toeplitz_inspired_refinement_record,
    consecutive_cutoff_embedding_record,
    harmonic_projection_refinement_record,
    heat_kernel_coarse_graining_record,
    trace_filled_ucp_embedding_record,
    trace_filled_uniform_multiplicativity_obstruction_record,
)


class EmbeddingChannelsTest(unittest.TestCase):
    def test_trace_filled_ucp_embedding_shape(self):
        record = trace_filled_ucp_embedding_record(4, 9)
        self.assertTrue(record["unital"])
        self.assertTrue(record["completely_positive"])
        self.assertTrue(record["normalized_trace_preserving"])
        self.assertFalse(record["is_star_homomorphism"])
        self.assertEqual(
            record["multiplicativity_witness"]["operator_norm_error"],
            0.25,
        )
        self.assertTrue(
            record["screen_shadow"][
                "screen_shadow_preserved_for_declared_diagonal_tests"
            ]
        )
        self.assertEqual(
            record["operator_response"]["commutator_operator_norm"],
            1.0,
        )
        self.assertEqual(
            record["multiplicativity_witness"]["scope"],
            "selected_matrix_unit_pair_only",
        )
        self.assertFalse(
            record["multiplicativity_witness"]["uniform_unit_ball_control_claimed"]
        )

    def test_trace_filled_map_has_uniform_multiplicativity_obstruction(self):
        record = trace_filled_uniform_multiplicativity_obstruction_record(4, 9)
        self.assertEqual(record["normalized_trace_A"], 0.0)
        self.assertEqual(record["operator_norm_defect"], 1.0)
        self.assertTrue(record["unit_ball_witness"])
        self.assertTrue(record["blocks_uniform_asymptotic_multiplicativity"])

    def test_consecutive_cutoff_replaces_star_inclusion_with_ucp_refinement(self):
        record = consecutive_cutoff_embedding_record(1)
        self.assertEqual(record["source_dim"], 4)
        self.assertEqual(record["target_dim"], 9)
        self.assertFalse(record["exact_unital_star_inclusion_exists"])
        self.assertIn("UCP refinement", record["exact_inclusion_obstruction"])
        self.assertTrue(record["approximate_embedding"]["unital"])

    def test_embedding_family_certificate_passes(self):
        certificate = approximate_static_patch_embedding_certificate(max_cutoff=5)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(
            certificate["result_type"],
            "physically_motivated_cutoff_refinement_audit",
        )
        self.assertTrue(all(certificate["certified_claims"].values()))
        for actual, expected in zip(
            certificate["multiplicativity_errors"],
            (0.25, 1.0 / 9.0, 0.0625, 0.04, 1.0 / 36.0),
        ):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual(len(certificate["physical_candidate_error_bounds"]), 5)
        self.assertEqual(
            certificate["multiplicativity_error_scope"],
            "selected_matrix_unit_pair_only",
        )
        self.assertTrue(certificate["uniform_multiplicativity_obstructions"])
        self.assertTrue(
            certificate["certified_claims"][
                "trace_filled_map_not_uniformly_asymptotically_multiplicative"
            ]
        )
        self.assertTrue(
            certificate["certified_claims"][
                "physical_candidate_multiplicativity_bounds_decrease"
            ]
        )

    def test_candidate_table_marks_physical_audits_as_implemented(self):
        certificate = approximate_static_patch_embedding_certificate(max_cutoff=2)
        table = {
            row["candidate"]: row
            for row in certificate["embedding_candidate_table"]
        }
        self.assertEqual(
            table["berezin_toeplitz_inspired_smoothing"]["status"],
            "implemented_surrogate_not_canonical",
        )
        self.assertEqual(
            table["trace_filled_ucp_consecutive_refinement"]["status"],
            "implemented_in_this_audit",
        )
        self.assertEqual(
            table["heat_kernel_coarse_graining"]["status"],
            "implemented_physical_motivation_audit",
        )

    def test_harmonic_projection_refinement_preserves_low_modes(self):
        record = harmonic_projection_refinement_record(2)
        self.assertTrue(record["source_labels_match_target_prefix"])
        self.assertTrue(record["map_properties"]["unital"])
        self.assertTrue(record["map_properties"]["completely_positive"])
        self.assertEqual(
            record["screen_shadow"]["screen_shadow_error_bound"],
            0.0,
        )
        self.assertEqual(
            record["operator_response"]["commutator_response_retention"],
            1.0,
        )

    def test_heat_kernel_coarse_graining_is_ucp_and_retains_response(self):
        record = heat_kernel_coarse_graining_record(2)
        self.assertTrue(record["map_properties"]["unital"])
        self.assertTrue(record["map_properties"]["completely_positive"])
        self.assertEqual(
            record["screen_shadow"]["screen_shadow_error_bound"],
            0.0,
        )
        self.assertGreater(
            record["operator_response"]["commutator_response_retention"],
            0.0,
        )
        self.assertLessEqual(
            record["multiplicativity"]["operator_norm_error_bound"],
            1.0 / 9.0,
        )

    def test_berezin_inspired_smoothing_is_controlled_not_canonical(self):
        record = berezin_toeplitz_inspired_refinement_record(2)
        self.assertEqual(record["status"], "implemented_surrogate_not_canonical")
        self.assertTrue(record["map_properties"]["convex_mixture_of_ucp_maps"])
        self.assertTrue(record["screen_shadow"]["screen_shadow_error_vanishes"])
        self.assertGreater(
            record["operator_response"]["commutator_response_retention"],
            0.0,
        )
        self.assertLess(
            record["screen_shadow"]["screen_shadow_error_bound"],
            0.1,
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            trace_filled_ucp_embedding_record(1, 2)
        with self.assertRaises(ValueError):
            trace_filled_ucp_embedding_record(4, 3)
        with self.assertRaises(ValueError):
            trace_filled_uniform_multiplicativity_obstruction_record(3, 4)
        with self.assertRaises(ValueError):
            trace_filled_uniform_multiplicativity_obstruction_record(4, 4)
        with self.assertRaises(ValueError):
            consecutive_cutoff_embedding_record(0)
        with self.assertRaises(ValueError):
            harmonic_projection_refinement_record(0)
        with self.assertRaises(ValueError):
            heat_kernel_coarse_graining_record(1, heat_strength=0)
        with self.assertRaises(ValueError):
            berezin_toeplitz_inspired_refinement_record(1, smoothing_strength=0)
        with self.assertRaises(ValueError):
            approximate_static_patch_embedding_certificate(max_cutoff=0)


if __name__ == "__main__":
    unittest.main()
