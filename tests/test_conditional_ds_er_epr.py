import unittest

from qgtoy.conditional_ds_er_epr import (
    analytic_cutoff_error_bound,
    conditional_continuum_theorem_record,
    cutoff_static_patch_sequence,
    exact_geometric_cutoff_error,
    goal24_conditional_ds_er_epr_certificate,
    prior_art_positioning,
    screen_shadow_sequence_no_go,
    static_patch_kernel_cp_preflight_certificate,
    static_patch_schur_channel_audit,
    static_patch_schur_coefficient,
    static_patch_schur_coefficient_matrix,
    static_patch_schur_composition_audit,
)


class ConditionalDsErEprTheoremLedgerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal24_conditional_ds_er_epr_certificate(
            max_cutoff=5,
            screen_probability=0.75,
            low_order=2,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_cutoff_sequence_defines_required_static_patch_objects(self):
        sequence = self.certificate["cutoff_sequence"]
        self.assertTrue(sequence["required_objects_defined_for_every_cutoff"])
        representative = sequence["systems"][2]
        self.assertEqual(representative["cutoff_L"], 3)
        self.assertEqual(representative["mode_count"], 16)
        self.assertEqual(representative["finite_screen_algebra_A_L"], "C^16")
        self.assertEqual(representative["north_observer_algebra_O_N_L"], "M_16")
        self.assertEqual(representative["south_observer_algebra_O_S_L"], "M_16")
        self.assertEqual(representative["shared_horizon_center_H_L"], "C^16")
        self.assertIn(
            "K_L(alpha)",
            representative["regulated_transfer_kernel_K_L"]["family"],
        )
        self.assertEqual(
            representative["induced_observer_bridge_channel_B_L"][
                "quantum_bridge_epsilon_recoverable_algebra"
            ],
            "M_16",
        )

    def test_analytic_cutoff_error_bound_vanishes_inside_model(self):
        previous = None
        for cutoff in range(1, 8):
            exact = exact_geometric_cutoff_error(cutoff)
            bound = analytic_cutoff_error_bound(cutoff)
            self.assertLessEqual(exact, bound)
            self.assertGreater(exact, 0.0)
            if previous is not None:
                self.assertLess(exact, previous)
            previous = exact
        limit_record = self.certificate["cutoff_sequence"][
            "analytic_vanishing_error"
        ]
        self.assertEqual(limit_record["limit"], "lim_{L->infinity} 2L/(L+1)^2 = 0")

    def test_schur_kernel_cp_trace_unital_audit(self):
        audit = static_patch_schur_channel_audit(
            3,
            alpha=0.5,
            damping_steps=1,
        )
        props = audit["schur_multiplier_channel_properties"]
        self.assertTrue(props["complete_positive"])
        self.assertTrue(props["trace_preserving"])
        self.assertTrue(props["unital"])
        self.assertTrue(props["cptp_unital"])
        self.assertTrue(audit["coefficient_matrix"]["positive_semidefinite_numeric"])
        self.assertTrue(audit["analytic_cp_proof"]["product_kernel_positive_definite_on_Z2"])

        matrix = static_patch_schur_coefficient_matrix(
            2,
            alpha=0.75,
            damping_steps=2,
        )
        self.assertEqual(len(matrix), 9)
        for index in range(len(matrix)):
            self.assertAlmostEqual(matrix[index][index], 1.0)
            for other in range(len(matrix)):
                self.assertAlmostEqual(matrix[index][other], matrix[other][index])

    def test_schur_kernel_composition_audit(self):
        audit = static_patch_schur_composition_audit(
            3,
            first_alpha=0.5,
            second_alpha=0.75,
        )
        composition = audit["composition"]
        self.assertEqual(composition["alpha"], 0.375)
        self.assertEqual(composition["damping_steps"], 2)
        self.assertTrue(composition["closed_in_broadened_schur_damping_family"])
        self.assertTrue(composition["cptp_unital"])
        self.assertFalse(composition["strict_single_step_family_closed"])
        self.assertGreater(composition["strict_single_step_family_error"], 0.0)

    def test_static_patch_kernel_cp_preflight_certificate(self):
        audit = static_patch_kernel_cp_preflight_certificate(max_cutoff=4)
        self.assertEqual(audit["status"], "pass")
        self.assertTrue(all(audit["certified_claims"].values()))
        self.assertIn(
            "composition closed",
            audit["theorem_record"]["composition"],
        )
        self.assertTrue(
            self.certificate["certified_claims"][
                "finite_schur_kernel_cp_preflight_passes"
            ]
        )

    def test_screen_visible_sequence_no_go(self):
        no_go = screen_shadow_sequence_no_go(
            max_cutoff=4,
            screen_probability=0.75,
            low_order=2,
        )
        self.assertEqual(no_go["result"], "B: no-go theorem")
        self.assertTrue(no_go["all_cutoff_collisions_hold"])
        self.assertTrue(no_go["sequence_level_collision"])
        for row in no_go["collision_rows"]:
            self.assertTrue(row["screen_entropy_match"])
            self.assertTrue(row["low_order_correlators_match"])
            self.assertTrue(row["screen_restricted_transfer_match"])
            self.assertNotEqual(
                row["quantum_bridge_algebra"],
                row["classical_bridge_algebra"],
            )

    def test_conditional_theorem_is_not_a_literal_ds_claim(self):
        theorem = conditional_continuum_theorem_record()
        self.assertEqual(theorem["result"], "A: conditional theorem")
        self.assertFalse(theorem["literal_ds_er_epr_proved"])
        self.assertIn(
            "physical_static_patch_dynamics",
            theorem["undischarged_assumption_ids"],
        )
        self.assertIn(
            "observer_algebra_limit",
            theorem["undischarged_assumption_ids"],
        )

    def test_goal23_recovered_and_obstruction_gate_present(self):
        self.assertTrue(self.certificate["finite_goal23_recovery"]["recovers_goal23"])
        obstruction = self.certificate["obstruction_theorem"]
        self.assertEqual(obstruction["result"], "C: obstruction theorem")
        self.assertEqual(
            obstruction["minimal_first_obstruction"],
            "physical_static_patch_dynamics",
        )
        self.assertGreaterEqual(len(obstruction["remaining_obligations"]), 6)
        self.assertIn(
            "does not prove literal continuum dS/CFT",
            self.certificate["claim_boundary"],
        )

    def test_prior_art_positioning_and_taxonomy(self):
        prior_art = prior_art_positioning()
        ids = {entry["id"] for entry in prior_art}
        self.assertIn("engelhardt_liu_2023", ids)
        self.assertIn("harlow_2016", ids)
        self.assertIn("harlow_usatyuk_zhao_2025", ids)
        taxonomy = self.certificate["result_taxonomy"]
        self.assertIn("exact_finite_results", taxonomy)
        self.assertIn("conditional_continuum_results", taxonomy)
        self.assertIn("speculative_or_unproved_physics", taxonomy)

    def test_sequence_validation(self):
        with self.assertRaises(ValueError):
            cutoff_static_patch_sequence(
                max_cutoff=0,
                screen_probability=0.75,
                low_order=2,
            )
        with self.assertRaises(ValueError):
            goal24_conditional_ds_er_epr_certificate(screen_probability=-0.1)
        with self.assertRaises(ValueError):
            goal24_conditional_ds_er_epr_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            static_patch_schur_coefficient(
                1,
                (0, 0),
                (1, 0),
                alpha=1.25,
            )


if __name__ == "__main__":
    unittest.main()
