import unittest

from qgtoy.local_bridge_screen import (
    IntrinsicLocalBridgeScreenDynamicsModel,
    goal18_intrinsic_local_bridge_screen_dynamics_certificate,
    local_entropy_only_control,
    local_screen_channel_record,
    local_tensor_network_record,
)


class IntrinsicLocalBridgeScreenDynamicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal18_intrinsic_local_bridge_screen_dynamics_certificate(
            mouths=3,
            low_order=3,
            atlas_max_mouths=3,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_local_tensor_network_is_not_a_declared_router(self):
        tensor = local_tensor_network_record(0.75)
        self.assertEqual(tensor["primitive"], "local star tensor network")
        self.assertTrue(tensor["not_a_declared_screen_router"])
        self.assertTrue(tensor["no_direct_north_south_tensor"])
        self.assertTrue(tensor["channels_are_derived_by_partial_trace"])
        self.assertLess(tensor["isometry_error"], 1e-12)

    def test_screen_channels_are_exact_partial_trace_erasure_channels(self):
        for probability in (0.25, 0.75):
            north = local_screen_channel_record(probability, screen="north")
            south = local_screen_channel_record(probability, screen="south")

            self.assertAlmostEqual(
                north["state_derived_success_probability"],
                probability,
            )
            self.assertAlmostEqual(
                south["state_derived_success_probability"],
                1.0 - probability,
            )
            self.assertTrue(north["success_probability_matches_local_branch_weight"])
            self.assertTrue(south["success_probability_matches_local_branch_weight"])
            self.assertLess(north["choi_distance_to_exact_erasure_channel"], 1e-12)
            self.assertLess(south["choi_distance_to_exact_erasure_channel"], 1e-12)
            self.assertLess(north["trace_preserving_error"], 1e-12)
            self.assertLess(south["trace_preserving_error"], 1e-12)

    def test_representative_derives_state_bridge_and_dressed_algebra(self):
        witness = self.certificate["representative_witness"]["twisted_local_dynamics"]
        dynamics = witness["single_local_interaction_pattern"]
        self.assertTrue(
            dynamics["no_separately_declared_north_south_recovery_isometry"]
        )
        self.assertTrue(dynamics["bridge_and_screen_share_dynamics_id"])

        pairing = witness["state_derived_pairing"]
        graph = witness["state_derived_interaction_graph"]
        self.assertEqual(pairing["inferred_pairing"], (1, 0, 2))
        self.assertTrue(pairing["unique_permutation_inferred"])
        self.assertEqual(
            graph["inferred_right_block_interaction_edges"],
            ((0, 1), (1, 2)),
        )
        self.assertTrue(graph["matches_circuit_interaction_graph"])

        algebra = witness["observer_algebra"]
        self.assertEqual(algebra["logical_dimension"], 6)
        self.assertEqual(algebra["symplectic_rank"], 6)
        self.assertEqual(algebra["center_dimension"], 0)
        self.assertTrue(algebra["full_quantum_algebra"])

    def test_low_order_entropy_and_bridge_controls(self):
        comparisons = self.certificate["representative_witness"]["comparisons"]
        audit = comparisons["low_order_physical_entropy_audit"]
        self.assertEqual(audit["max_order"], 3)
        self.assertEqual(audit["mismatch_count"], 0)
        self.assertEqual(comparisons["first_entropy_mismatch"]["order"], 4)

        capacities = comparisons["bridge_transfer"]["capacities"]
        self.assertEqual(capacities["state_derived_activation"], 3)
        self.assertEqual(capacities["state_derived_T_dressed_activation"], 3)
        self.assertEqual(capacities["identity_activation_after_interaction_removal"], 1)
        self.assertEqual(capacities["mouth_blind_scrambling_control"], 0)

    def test_screen_transition_is_derived_from_local_channels(self):
        transition = self.certificate["transition_from_local_dynamics"]
        self.assertTrue(transition["all_local_tensor_networks_are_isometries"])
        self.assertTrue(transition["all_channels_derived_by_partial_trace"])
        self.assertTrue(
            transition["all_screen_probabilities_recovered_from_local_channels"]
        )
        self.assertTrue(transition["all_screen_channels_are_exact_erasure_channels"])
        self.assertTrue(transition["all_screen_channels_trace_preserving"])
        self.assertTrue(transition["recovery_and_area_winners_match"])
        self.assertTrue(transition["midpoint_transition_from_local_dynamics"])

        rows = {
            row["north_coupling_probability"]: row
            for row in transition["records"]
        }
        self.assertEqual(rows[0.0]["recovery_winner"], "south")
        self.assertEqual(rows[0.5]["recovery_winner"], "tie")
        self.assertEqual(rows[1.0]["recovery_winner"], "north")
        self.assertEqual(rows[0.75]["larger_quantum_area_analogue"], "north")

    def test_entropy_only_static_state_and_area_bias_controls(self):
        entropy_only = local_entropy_only_control(0.75)
        self.assertEqual(entropy_only["entropy_only_winner"], "tie")
        self.assertEqual(entropy_only["channel_recovery_winner"], "north")
        self.assertTrue(
            entropy_only["entropy_only_is_insufficient_for_oriented_screen_recovery"]
        )

        controls = self.certificate["controls"]
        static_only = controls["static_state_only_no_go"]
        self.assertTrue(static_only["opposite_recovery_winners_with_same_static_state"])
        area_bias = controls["external_area_bias_no_go"]
        self.assertFalse(area_bias["transitions_match"])
        self.assertEqual(area_bias["recovery_transition_probability"], 0.5)
        self.assertEqual(area_bias["quantum_area_transition_probability"], 0.375)

    def test_bounded_local_atlas(self):
        atlas = self.certificate["bounded_local_atlas"]["records"]
        self.assertEqual(atlas[-1]["m"], 3)
        self.assertEqual(atlas[-1]["local_dynamics_checked"], 144)
        self.assertTrue(all(row["all_pairings_recovered"] for row in atlas))
        self.assertTrue(all(row["all_graphs_recovered"] for row in atlas))
        self.assertTrue(
            all(row["state_derived_transfer_full_capacity"] for row in atlas)
        )
        self.assertTrue(
            all(row["screen_channels_emerge_from_local_tensors"] for row in atlas)
        )

    def test_model_rejects_invalid_screen_probability(self):
        with self.assertRaises(ValueError):
            IntrinsicLocalBridgeScreenDynamicsModel(
                name="bad",
                pairing=(0, 1),
                interaction_edges=((0, 1),),
                north_coupling_probability=1.25,
            )


if __name__ == "__main__":
    unittest.main()
