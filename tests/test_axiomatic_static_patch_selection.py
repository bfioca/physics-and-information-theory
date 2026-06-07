import unittest

from qgtoy.axiomatic_static_patch_selection import (
    axiomatic_candidate_catalog,
    axiomatic_selection_atlas,
    axiomatic_selection_audit,
    goal28_axiomatic_static_patch_selection_certificate,
    weakest_missing_axiom_audit,
)
from qgtoy.static_patch_regulator_universality import ACCEPTED_REGULATOR_IDS


class AxiomaticStaticPatchSelectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal28_axiomatic_static_patch_selection_certificate(
            max_cutoff=5,
            noise_strength=1.0,
            environment_qubits=4,
            temperature_scale=1.0,
            screen_probability=0.75,
            low_order=2,
            perturbation_radius=0.05,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertEqual(
            self.certificate["result_type"],
            "finite_axiomatic_selection_success",
        )

    def test_axioms_select_goal27_class(self):
        selected = set(self.certificate["selected_regulator_ids"])
        self.assertEqual(selected, set(ACCEPTED_REGULATOR_IDS))
        self.assertEqual(len(selected), 4)

    def test_selected_rows_do_not_use_response_or_bridge_inputs(self):
        for row in self.certificate["selection_atlas"]:
            if row["selected"]:
                self.assertTrue(
                    row["axioms"]["anti_tautology_no_response_or_bridge_input"]
                )
                self.assertNotIn("bridge", row["primitive_description"].lower())
                self.assertNotIn("response", row["primitive_description"].lower())

    def test_obstruction_rows_have_expected_failures(self):
        atlas = {row["candidate_id"]: row for row in axiomatic_selection_atlas()}
        self.assertEqual(
            atlas["raw_euclidean_heat_transfer"]["status"],
            "rejected_missing_cptp_or_diagonal_preservation",
        )
        self.assertEqual(
            atlas["screen_only_ds_cft_shadow_map"]["status"],
            "rejected_missing_cptp_or_diagonal_preservation",
        )
        self.assertEqual(
            atlas["instant_total_dephasing_control"]["status"],
            "rejected_missing_vanishing_cutoff_continuity",
        )
        self.assertEqual(
            atlas["response_oracle_kernel"]["status"],
            "rejected_tautological_response_input",
        )

    def test_missing_continuity_axiom_is_necessary(self):
        audit = weakest_missing_axiom_audit(axiomatic_selection_atlas())
        continuity = next(
            row
            for row in audit
            if row["missing_axiom"] == "vanishing_cutoff_error_continuity"
        )
        self.assertEqual(
            continuity["counterexample"],
            "instant_total_dephasing_control",
        )
        self.assertTrue(continuity["would_pass_without_missing_axiom"])
        self.assertEqual(continuity["status"], "necessary_axiom_identified")

    def test_bounded_family_preserves_diagnostic(self):
        family = self.certificate["bounded_cutoff_family"]
        self.assertTrue(family["all_cptp_unital"])
        self.assertTrue(family["all_scaling_bounds_hold"])
        self.assertTrue(family["all_screen_visible_data_collide"])
        self.assertTrue(family["all_offdiagonal_responses_separate_bridge"])
        self.assertTrue(family["all_stability_variants_preserve_bridge_diagnostic"])

    def test_representative_witness_uses_selected_regulators(self):
        witness = self.certificate["representative_cutoff_witness"]
        self.assertEqual(set(witness["selected_regulator_ids"]), set(ACCEPTED_REGULATOR_IDS))
        self.assertTrue(witness["all_selected_regulators_preserve_bridge_diagnostic"])
        self.assertTrue(witness["all_stability_variants_preserve_bridge_diagnostic"])

    def test_individual_candidate_audit(self):
        catalog = {candidate.candidate_id: candidate for candidate in axiomatic_candidate_catalog()}
        selected = axiomatic_selection_audit(
            catalog["gaussian_fuzzy_heat_time_average"]
        )
        self.assertTrue(selected["selected"])
        self.assertEqual(selected["status"], "selected_axiomatic_regulator")

        oracle = axiomatic_selection_audit(catalog["response_oracle_kernel"])
        self.assertFalse(oracle["selected"])
        self.assertFalse(
            oracle["axioms"]["anti_tautology_no_response_or_bridge_input"]
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal28_axiomatic_static_patch_selection_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            goal28_axiomatic_static_patch_selection_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            goal28_axiomatic_static_patch_selection_certificate(environment_qubits=0)
        with self.assertRaises(ValueError):
            goal28_axiomatic_static_patch_selection_certificate(temperature_scale=0.0)
        with self.assertRaises(ValueError):
            goal28_axiomatic_static_patch_selection_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            goal28_axiomatic_static_patch_selection_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            goal28_axiomatic_static_patch_selection_certificate(
                perturbation_radius=1.0,
            )


if __name__ == "__main__":
    unittest.main()
