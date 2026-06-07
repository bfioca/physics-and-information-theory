import unittest

from qgtoy.continuum_lift import (
    continuum_lift_conditions,
    continuum_lift_obstruction_certificate,
    screen_only_dictionary_obstruction,
)


class ContinuumLiftObstructionTest(unittest.TestCase):
    def test_lift_conditions_are_explicit(self):
        conditions = continuum_lift_conditions()
        self.assertEqual(len(conditions), 6)
        self.assertEqual(
            conditions[0]["condition"],
            "embedding_or_coarse_graining_structure",
        )
        self.assertEqual(
            conditions[-1]["condition"],
            "observer_algebra_limit_compatibility",
        )

    def test_screen_only_dictionary_obstruction(self):
        obstruction = screen_only_dictionary_obstruction(
            screen_shadow_distance=0.0,
            response_witness_gap=1.0,
        )
        self.assertTrue(obstruction["screen_only_dictionary_incomplete"])
        self.assertIn("screen-factored", obstruction["reason"])

        non_collision = screen_only_dictionary_obstruction(
            screen_shadow_distance=0.1,
            response_witness_gap=1.0,
        )
        self.assertFalse(non_collision["screen_only_dictionary_incomplete"])

    def test_certificate_passes_and_keeps_claim_boundary(self):
        certificate = continuum_lift_obstruction_certificate(max_cutoff=5)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(
            certificate["result_type"],
            "proof_ready_conditional_continuum_lift_obstruction_theorem",
        )
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertTrue(
            certificate["certified_claims"][
                "not_claimed_as_continuum_static_patch_theorem"
            ]
        )
        self.assertIn("does not construct", certificate["claim_boundary"])

    def test_certificate_inherits_embedding_error_gate(self):
        certificate = continuum_lift_obstruction_certificate(max_cutoff=5)
        errors = certificate["multiplicativity_error_limit_gate"]["errors"]
        self.assertGreater(errors[0], errors[-1])
        self.assertEqual(
            certificate["multiplicativity_error_limit_gate"]["candidate_limit"],
            "0 as cutoff L -> infinity",
        )
        self.assertTrue(
            certificate["embedding_certificate"]["certified_claims"][
                "consecutive_ucp_refinements_exist"
            ]
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            continuum_lift_obstruction_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            screen_only_dictionary_obstruction(
                screen_shadow_distance=-1.0,
                response_witness_gap=1.0,
            )
        with self.assertRaises(ValueError):
            screen_only_dictionary_obstruction(
                screen_shadow_distance=0.0,
                response_witness_gap=-1.0,
            )


if __name__ == "__main__":
    unittest.main()
