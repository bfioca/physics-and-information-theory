import unittest

from qgtoy.ds_cft_er_epr import (
    ds_cft_er_epr_collision_record,
    ds_cft_screen_shadow,
    goal21_ds_cft_er_epr_compatibility_certificate,
)


class DsCftErEprCompatibilityBenchmarkTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal21_ds_cft_er_epr_compatibility_certificate(
            max_dim=5,
            screen_probability=0.75,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_screen_shadow_declares_ds_like_static_patch_objects(self):
        shadow = ds_cft_screen_shadow(2, screen_probability=0.75)
        finite_objects = shadow["finite_objects"]
        self.assertTrue(finite_objects["no_asymptotic_ads_boundary"])
        self.assertEqual(
            finite_objects["observer_primitives"],
            ("north_static_patch", "south_static_patch"),
        )
        self.assertEqual(finite_objects["shared_finite_horizon_algebra"], "C^2")
        self.assertEqual(
            finite_objects["bulk_bridge_operator_algebra_under_test"],
            "M_2",
        )

    def test_minimal_collision_has_same_screen_shadow_and_different_bridge(self):
        record = self.certificate["minimal_counterexample"]
        self.assertEqual(record["dimension"], 2)
        self.assertTrue(
            record["screen_shadow_agreement"][
                "all_declared_screen_cft_visible_data_match"
            ]
        )
        bridge = record["algebraic_er_epr_bridge_channel"]
        self.assertEqual(
            bridge["identity_bridge_maximal_recoverable_algebra"],
            "M_2",
        )
        self.assertEqual(
            bridge["dephased_bridge_maximal_recoverable_algebra"],
            "C^2",
        )
        self.assertTrue(bridge["fixed_screen_shadow_does_not_determine_bridge_phase"])

    def test_qutrit_collision_is_non_pauli(self):
        record = self.certificate["non_pauli_qutrit_counterexample"]
        self.assertEqual(record["dimension"], 3)
        self.assertEqual(
            record["screen_cft_visible_shadow"]["finite_objects"][
                "shared_finite_horizon_algebra"
            ],
            "C^3",
        )
        self.assertEqual(
            record["algebraic_er_epr_bridge_channel"][
                "identity_bridge_maximal_recoverable_algebra"
            ],
            "M_3",
        )

    def test_completion_probe_separates_screen_shadow_collision(self):
        record = ds_cft_er_epr_collision_record(4, screen_probability=0.75)
        completion = record["completion_diagnostic"]
        self.assertTrue(completion["off_diagonal_probe_separates_bridge_channels"])
        self.assertTrue(completion["full_operator_spectra_differ"])
        self.assertGreater(
            completion["identity_off_diagonal_output_bits"],
            completion["dephasing_off_diagonal_output_bits"],
        )

    def test_bounded_family_checks_each_dimension(self):
        family = self.certificate["bounded_family"]
        self.assertEqual(family["dimensions_checked"], (2, 3, 4, 5))
        self.assertTrue(family["all_screen_shadows_match"])
        self.assertTrue(family["all_bridge_algebras_differ"])
        self.assertTrue(family["all_completion_probes_separate"])

    def test_entropy_only_wrong_patch_control_is_present(self):
        control = self.certificate["minimal_counterexample"][
            "wrong_patch_and_entropy_only_control"
        ]
        self.assertEqual(control["entropy_only_winner"], "tie")
        self.assertEqual(control["channel_recovery_winner"], "north")
        self.assertTrue(
            control["entropy_only_is_insufficient_for_oriented_screen_recovery"]
        )

    def test_goal20_relationship_and_claim_boundary_are_explicit(self):
        relationship = self.certificate["relationship_to_goals_19_20"]
        self.assertIn("recoverable bridge algebra", relationship["goal19"])
        self.assertIn("probe-incompleteness", relationship["goal20"])
        self.assertIn("finite dS/CFT", relationship["goal21"])
        self.assertIn("not a continuum dS/CFT theorem", self.certificate["claim_boundary"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal21_ds_cft_er_epr_compatibility_certificate(max_dim=1)
        with self.assertRaises(ValueError):
            ds_cft_screen_shadow(2, screen_probability=1.5)


if __name__ == "__main__":
    unittest.main()
