import unittest

from qgtoy.interacting_bridge import (
    InteractingEncodedBridgeModel,
    goal15_interacting_state_derived_bridge_theorem_certificate,
    logical_cz_unitary,
    unitary_channel_certificate,
)


class InteractingBridgeTheoremTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal15_interacting_state_derived_bridge_theorem_certificate(
            mouths=2,
            low_order=3,
            atlas_max_mouths=3,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_interacting_resource_is_non_product(self):
        witness = self.certificate["representative_witness"]
        non_product = witness["comparisons"]["non_product_witness"]
        self.assertTrue(non_product["non_product_interaction_detected"])
        row = non_product["non_product_rows"][0]
        self.assertEqual(row["interacting_entropy_first"], 1)
        self.assertEqual(row["interacting_entropy_second"], 1)
        self.assertEqual(row["interacting_mutual_information"], 2)
        self.assertEqual(row["product_resource_mutual_information"], 0)

    def test_state_derives_pairing_and_observer_algebra(self):
        comparisons = self.certificate["representative_witness"]["comparisons"]
        pairing = comparisons["state_derived_pairing"]
        self.assertEqual(pairing["inferred_pairing"], (1, 0))
        self.assertTrue(pairing["unique_permutation_inferred"])
        rows = pairing["pairing_rows"]
        self.assertEqual(
            rows[0]["mutual_information_by_interacting_right_block"],
            (0, 1),
        )
        self.assertEqual(
            rows[1]["mutual_information_by_interacting_right_block"],
            (1, 0),
        )

        algebra = comparisons["observer_algebra"]
        graph = comparisons["state_derived_interaction_graph"]
        self.assertEqual(graph["inferred_right_block_interaction_edges"], ((0, 1),))
        self.assertTrue(graph["matches_circuit_interaction_graph"])
        self.assertFalse(graph["uses_declared_interaction_graph_as_input"])
        self.assertEqual(algebra["logical_dimension"], 4)
        self.assertEqual(algebra["symplectic_rank"], 4)
        self.assertEqual(algebra["center_dimension"], 0)
        self.assertTrue(algebra["full_quantum_algebra"])

    def test_low_order_entropy_blindness(self):
        comparisons = self.certificate["representative_witness"]["comparisons"]
        audit = comparisons["low_order_physical_entropy_audit"]
        self.assertEqual(audit["max_order"], 3)
        self.assertEqual(audit["regions_checked"], 299)
        self.assertEqual(audit["mismatch_count"], 0)
        self.assertEqual(comparisons["first_entropy_mismatch"]["order"], 4)

    def test_interaction_unitary_is_nontrivial(self):
        unitary = unitary_channel_certificate(logical_cz_unitary(2, ((0, 1),)))
        self.assertEqual(unitary["choi"]["rank"], 1)
        self.assertEqual(unitary["trace_preserving_error"], 0.0)
        self.assertLess(unitary["fidelity"]["entanglement_fidelity_to_identity"], 1.0)

    def test_state_derived_transfer_and_controls(self):
        transfer = self.certificate["representative_witness"]["transfer_certificate"]
        capacities = transfer["capacities"]
        self.assertEqual(capacities["identity_activation_after_interaction_removal"], 0)
        self.assertEqual(capacities["state_derived_activation"], 2)
        self.assertEqual(capacities["state_derived_T_dressed_activation"], 2)
        self.assertEqual(capacities["mouth_blind_scrambling_control"], 0)

        explicit = transfer["explicit_channel_certificates"]
        wrong = explicit["wrong_mouth_after_interaction_removal"]
        recovered = explicit["state_derived_decoder_after_interaction_removal"]
        self.assertEqual(wrong["fixed_port_transmission"]["perfect_qubits"], 0)
        self.assertEqual(wrong["preserved_operator_algebra"]["center_dimension"], 2)
        self.assertEqual(recovered["choi"]["rank"], 1)
        self.assertEqual(recovered["fidelity"]["entanglement_fidelity_to_identity"], 1.0)

    def test_static_state_transition_no_go(self):
        no_go = self.certificate["transition_no_go"]
        self.assertTrue(no_go["opposite_recovery_winners_with_same_static_state"])
        self.assertEqual(
            no_go["minimal_inserted_ingredient"],
            "an explicit screen dynamics/isometry, or an equivalent rule assigning the bridge state to north/south recovery channels",
        )
        self.assertEqual(no_go["north_completion"]["recovery_winner"], "north")
        self.assertEqual(no_go["south_completion"]["recovery_winner"], "south")
        self.assertFalse(no_go["external_area_bias_no_go"]["transitions_match"])

    def test_dynamic_screen_completion(self):
        completion = self.certificate["dynamic_screen_completion"]
        transition = completion["screen_transition"]
        self.assertTrue(completion["screen_isometry_is_required"])
        self.assertTrue(transition["all_probabilities_recovered_from_channels"])
        self.assertTrue(transition["recovery_and_area_winners_match"])
        self.assertTrue(transition["midpoint_transition_from_state"])

    def test_bounded_atlas(self):
        atlas = self.certificate["bounded_atlas"]
        first = atlas["first_non_product_entropy_matched_transfer_split"]
        self.assertEqual(first["m"], 2)
        self.assertTrue(first["non_product_interaction_present_for_all_resources"])
        self.assertEqual(first["identity_activation_capacity_profile"], {0: 1, 2: 1})
        self.assertEqual(first["state_derived_activation_capacity_profile"], {2: 2})
        self.assertEqual(first["mouth_blind_scrambling_capacity_profile"], {0: 2})
        self.assertTrue(
            all(
                row["all_pairings_recovered_from_interacting_state"]
                for row in atlas["records"]
            )
        )

    def test_model_standalone_state_builds(self):
        model = InteractingEncodedBridgeModel(
            name="standalone",
            pairing=(1, 0),
        )
        self.assertEqual(model.state_derived_pairing_record()["inferred_pairing"], (1, 0))
        self.assertTrue(model.non_product_witness()["non_product_interaction_detected"])


if __name__ == "__main__":
    unittest.main()
