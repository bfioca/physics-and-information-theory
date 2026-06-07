import unittest

from qgtoy.physical_static_patch_lift import (
    MINIMAL_ASSUMPTION,
    physical_lift_candidate_records,
    physical_static_patch_lift_certificate,
)


class PhysicalStaticPatchLiftTest(unittest.TestCase):
    def test_candidate_audit_covers_requested_structures(self):
        records = physical_lift_candidate_records(max_cutoff=5)
        self.assertEqual(len(records), 6)
        candidate_ids = {record["candidate_id"] for record in records}
        self.assertEqual(
            candidate_ids,
            {
                "berezin_toeplitz_symbol_quantization",
                "spherical_harmonic_projection_refinement",
                "heat_kernel_coarse_graining",
                "modular_kms_conditional_expectations",
                "coherent_state_fuzzy_sphere_refinement",
                "common_continuum_l2_s2_screen_embedding",
            },
        )
        for record in records:
            questions = record["questions"]
            self.assertIn("cp_unital_trace_or_controlled_nonunitarity", questions)
            self.assertIn("operator_response_large_cutoff_survival", questions)
            self.assertIn("typeii_static_patch_limit_route", questions)
            self.assertEqual(
                set(record["gate_status"]),
                {
                    "cp_unital_trace",
                    "low_mode_multiplicativity",
                    "covariance",
                    "screen_shadow",
                    "operator_response",
                    "strong_continuity",
                    "typeii_route",
                },
            )

    def test_certificate_selects_minimal_missing_assumption(self):
        certificate = physical_static_patch_lift_certificate(max_cutoff=5)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(
            certificate["selected_outcome"],
            "C_minimal_missing_assumption",
        )
        self.assertEqual(
            certificate["result_type"],
            "minimal_missing_assumption_for_physical_static_patch_lift",
        )
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertEqual(certificate["minimal_missing_assumption"], MINIMAL_ASSUMPTION)

    def test_no_go_candidates_are_explicit(self):
        certificate = physical_static_patch_lift_certificate(max_cutoff=5)
        self.assertIn(
            "common_continuum_l2_s2_screen_embedding",
            certificate["no_go_candidates"],
        )
        self.assertIn(
            "modular_kms_conditional_expectations",
            certificate["no_go_candidates"],
        )
        self.assertIn("screen embeddings are insufficient", certificate["no_go_statement"])

    def test_bounded_positive_candidates_are_not_canonical(self):
        certificate = physical_static_patch_lift_certificate(max_cutoff=5)
        self.assertEqual(
            set(certificate["positive_bounded_candidates"]),
            {
                "spherical_harmonic_projection_refinement",
                "heat_kernel_coarse_graining",
            },
        )
        gates = certificate["gate_status_by_candidate"]
        for candidate_id in certificate["positive_bounded_candidates"]:
            self.assertEqual(gates[candidate_id]["operator_response"], "pass")
            self.assertEqual(gates[candidate_id]["typeii_route"], "conditional")
        self.assertIn(
            "requires a canonical noncommutative",
            certificate["relationship_to_existing_continuum_lift"]["refinement"],
        )

    def test_gate_matrix_explains_c_outcome(self):
        certificate = physical_static_patch_lift_certificate(max_cutoff=5)
        gates = certificate["gate_status_by_candidate"]
        self.assertEqual(
            gates["common_continuum_l2_s2_screen_embedding"]["screen_shadow"],
            "pass",
        )
        self.assertEqual(
            gates["common_continuum_l2_s2_screen_embedding"]["operator_response"],
            "fail",
        )
        self.assertEqual(
            gates["common_continuum_l2_s2_screen_embedding"]["typeii_route"],
            "fail",
        )
        self.assertEqual(
            gates["modular_kms_conditional_expectations"]["operator_response"],
            "fail",
        )
        self.assertEqual(
            gates["modular_kms_conditional_expectations"]["strong_continuity"],
            "fail",
        )
        self.assertTrue(
            certificate["certified_claims"]["no_unconditional_canonical_lift_found"]
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            physical_lift_candidate_records(max_cutoff=0)
        with self.assertRaises(ValueError):
            physical_static_patch_lift_certificate(max_cutoff=0)


if __name__ == "__main__":
    unittest.main()
