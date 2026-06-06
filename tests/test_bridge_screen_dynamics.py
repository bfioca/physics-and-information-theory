import unittest

from qgtoy.bridge_screen import (
    InseparableBridgeScreenDynamicsModel,
    goal17_inseparable_bridge_screen_dynamics_certificate,
    screen_success_probability_from_channel,
)
from qgtoy.quantum_channel import coherent_bilayer_screen_kraus


class InseparableBridgeScreenDynamicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal17_inseparable_bridge_screen_dynamics_certificate(
            mouths=3,
            low_order=3,
            atlas_max_mouths=3,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_single_dynamics_record_derives_bridge_and_screen_data(self):
        witness = self.certificate["representative_witness"]["twisted_unified_dynamics"]
        dynamics = witness["single_declared_dynamics"]
        self.assertTrue(dynamics["screen_transition_is_not_extra_rule"])
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
        self.assertTrue(
            comparisons["screen_dynamics"]["depends_on_state_derived_bridge_decoder"]
        )

    def test_screen_channels_and_transition_are_channel_derived(self):
        transition = self.certificate["transition_from_unified_dynamics"]
        self.assertTrue(transition["all_screen_isometries_verified"])
        self.assertTrue(transition["all_probabilities_recovered_from_channels"])
        self.assertTrue(transition["all_screen_channels_trace_preserving"])
        self.assertTrue(transition["recovery_and_area_winners_match"])
        self.assertTrue(transition["midpoint_transition_from_unified_dynamics"])

        rows = {row["north_probability"]: row for row in transition["records"]}
        self.assertEqual(rows[0.0]["recovery_winner"], "south")
        self.assertEqual(rows[0.5]["recovery_winner"], "tie")
        self.assertEqual(rows[1.0]["recovery_winner"], "north")
        self.assertEqual(rows[0.75]["larger_quantum_area_analogue"], "north")

    def test_screen_success_probability_helper(self):
        north = coherent_bilayer_screen_kraus(0.25, screen="north")
        south = coherent_bilayer_screen_kraus(0.25, screen="south")
        self.assertAlmostEqual(screen_success_probability_from_channel(north), 0.25)
        self.assertAlmostEqual(screen_success_probability_from_channel(south), 0.75)

    def test_static_state_and_external_bias_controls(self):
        controls = self.certificate["controls"]
        static_only = controls["static_state_only_no_go"]
        self.assertTrue(static_only["opposite_recovery_winners_with_same_static_state"])
        self.assertEqual(
            static_only["minimal_inserted_ingredient"],
            "an explicit screen dynamics/isometry, or an equivalent rule assigning the bridge state to north/south recovery channels",
        )

        area_bias = controls["external_area_bias_no_go"]
        self.assertFalse(area_bias["transitions_match"])
        self.assertEqual(area_bias["recovery_transition_probability"], 0.5)
        self.assertEqual(area_bias["quantum_area_transition_probability"], 0.375)

    def test_bounded_unified_atlas(self):
        atlas = self.certificate["bounded_unified_atlas"]["records"]
        self.assertEqual(atlas[-1]["m"], 3)
        self.assertEqual(atlas[-1]["resources_checked"], 144)
        self.assertTrue(all(row["all_pairings_recovered"] for row in atlas))
        self.assertTrue(all(row["all_graphs_recovered"] for row in atlas))
        self.assertTrue(
            all(row["state_derived_transfer_full_capacity"] for row in atlas)
        )
        self.assertTrue(
            all(
                row["screen_probabilities_recovered_from_unified_channels"]
                for row in atlas
            )
        )

    def test_model_rejects_invalid_screen_probability(self):
        with self.assertRaises(ValueError):
            InseparableBridgeScreenDynamicsModel(
                name="bad",
                pairing=(0, 1),
                interaction_edges=((0, 1),),
                north_probability=1.25,
            )


if __name__ == "__main__":
    unittest.main()
