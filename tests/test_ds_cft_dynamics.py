import unittest

from qgtoy.ds_cft_dynamics import (
    finite_screen_transfer_process,
    goal22_ds_cft_er_epr_single_dynamics_certificate,
    single_dynamics_collision_record,
)


class DsCftErEprSingleDynamicsBenchmarkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal22_ds_cft_er_epr_single_dynamics_certificate(
            max_dim=5,
            screen_probability=0.75,
            low_order=2,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_transfer_process_derives_screen_and_bridge(self):
        process = finite_screen_transfer_process(
            2,
            offdiag_coupling=1,
            screen_probability=0.75,
        )
        rule = process["boundary_screen_transfer_rule"]
        self.assertTrue(rule["bridge_channel_is_induced_by_same_transfer_map"])
        self.assertTrue(rule["screen_shadow_is_induced_by_same_transfer_map"])
        self.assertEqual(process["maximal_recoverable_bridge_algebra"], "M_2")
        self.assertEqual(process["fixed_operator_count"], 4)

    def test_minimal_single_dynamics_collision(self):
        record = self.certificate["minimal_counterexample"]
        self.assertEqual(record["dimension"], 2)
        self.assertTrue(
            record["single_dynamics_derivation"][
                "bridge_channel_not_appended_after_screen_shadow"
            ]
        )
        self.assertTrue(
            record["screen_observable_collision"][
                "all_declared_screen_dynamics_data_match"
            ]
        )
        self.assertTrue(record["bridge_algebra_difference"]["bridge_algebras_differ"])
        self.assertEqual(
            record["bridge_algebra_difference"]["quantum_bridge_algebra"],
            "M_2",
        )
        self.assertEqual(
            record["bridge_algebra_difference"]["classical_horizon_bridge_algebra"],
            "C^2",
        )

    def test_qutrit_collision_is_non_pauli(self):
        record = self.certificate["non_pauli_qutrit_counterexample"]
        self.assertEqual(record["dimension"], 3)
        self.assertEqual(
            record["bridge_algebra_difference"]["quantum_bridge_algebra"],
            "M_3",
        )
        self.assertEqual(
            record["bridge_algebra_difference"]["classical_horizon_bridge_algebra"],
            "C^3",
        )

    def test_intrinsic_dynamics_completion_separates(self):
        record = single_dynamics_collision_record(
            4,
            screen_probability=0.75,
            low_order=2,
        )
        completion = record["intrinsic_dynamics_completion"]
        self.assertTrue(completion["full_operator_transfer_spectra_differ"])
        self.assertTrue(completion["off_diagonal_response_separates"])
        self.assertTrue(
            completion["commutator_growth_test"][
                "commutator_otoc_style_test_separates"
            ]
        )
        self.assertTrue(
            completion[
                "full_intrinsic_dynamics_data_determines_bridge_algebra_in_family"
            ]
        )

    def test_bounded_family_checks_every_dimension(self):
        family = self.certificate["bounded_family"]
        self.assertEqual(family["dimensions_checked"], (2, 3, 4, 5))
        self.assertTrue(family["all_screen_dynamics_shadows_match"])
        self.assertTrue(family["all_bridge_algebras_differ"])
        self.assertTrue(family["all_intrinsic_completions_separate"])

    def test_goal21_is_recovered_as_screen_shadow_obstruction(self):
        relationship = self.certificate["relationship_to_goals_19_21"]
        self.assertIn("screen shadow", relationship["goal21"].lower())
        self.assertIn("one finite transfer dynamics", relationship["goal22"])
        self.assertIn("not a continuum dS/CFT theorem", self.certificate["claim_boundary"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal22_ds_cft_er_epr_single_dynamics_certificate(max_dim=1)
        with self.assertRaises(ValueError):
            goal22_ds_cft_er_epr_single_dynamics_certificate(low_order=0)
        with self.assertRaises(ValueError):
            finite_screen_transfer_process(
                2,
                offdiag_coupling=3,
                screen_probability=0.75,
            )


if __name__ == "__main__":
    unittest.main()
