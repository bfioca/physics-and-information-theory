import unittest

from qgtoy.embedding_channels import (
    approximate_static_patch_embedding_certificate,
    consecutive_cutoff_embedding_record,
    trace_filled_ucp_embedding_record,
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
            "consecutive_ucp_cutoff_refinement_theorem_candidate",
        )
        self.assertTrue(all(certificate["certified_claims"].values()))
        for actual, expected in zip(
            certificate["multiplicativity_errors"],
            (0.25, 1.0 / 9.0, 0.0625, 0.04, 1.0 / 36.0),
        ):
            self.assertAlmostEqual(actual, expected)

    def test_candidate_table_marks_berezin_as_program_target(self):
        certificate = approximate_static_patch_embedding_certificate(max_cutoff=2)
        table = {
            row["candidate"]: row
            for row in certificate["embedding_candidate_table"]
        }
        self.assertEqual(
            table["berezin_toeplitz_fuzzy_sphere_channel"]["status"],
            "program_target",
        )
        self.assertEqual(
            table["trace_filled_ucp_consecutive_refinement"]["status"],
            "implemented_in_this_audit",
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            trace_filled_ucp_embedding_record(1, 2)
        with self.assertRaises(ValueError):
            trace_filled_ucp_embedding_record(4, 3)
        with self.assertRaises(ValueError):
            consecutive_cutoff_embedding_record(0)
        with self.assertRaises(ValueError):
            approximate_static_patch_embedding_certificate(max_cutoff=0)


if __name__ == "__main__":
    unittest.main()
