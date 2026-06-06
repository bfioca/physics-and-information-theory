import unittest

from qgtoy.interacting_bridge import (
    InteractingEncodedBridgeModel,
    goal16_paper_style_interacting_bridge_code_theorem_certificate,
)


class InteractingBridgeCodeTheoremTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal16_paper_style_interacting_bridge_code_theorem_certificate(
            mouths=3,
            low_order=3,
            atlas_max_mouths=3,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_path_witness_separates_pairwise_mi_from_pauli_recovery(self):
        comparisons = self.certificate["representative_witness"]["comparisons"]
        pairing = comparisons["state_derived_pairing"]
        pairwise = comparisons["pairwise_mi_screen"]
        pauli = comparisons["pauli_correlation_graph"]

        self.assertEqual(pairing["inferred_pairing"], (1, 0, 2))
        self.assertEqual(
            pairwise["pairwise_mi_correlated_edges"],
            ((0, 1), (0, 2), (1, 2)),
        )
        self.assertFalse(pairwise["matches_circuit_interaction_graph"])
        self.assertEqual(
            pauli["inferred_right_block_interaction_edges"],
            ((0, 1), (1, 2)),
        )
        self.assertTrue(pauli["matches_circuit_interaction_graph"])
        self.assertTrue(pauli["unique_solution_for_each_bridge"])

    def test_all_graph_atlas_recovers_graphs_and_records_mi_obstruction(self):
        atlas = self.certificate["bounded_all_graph_atlas"]
        failure = atlas["first_pairwise_mi_graph_recovery_failure"]
        self.assertEqual(failure["m"], 3)
        self.assertEqual(
            failure["interaction_graph"],
            ((0, 1), (0, 2)),
        )
        self.assertEqual(
            failure["pairwise_mi_correlated_edges"],
            ((0, 1), (0, 2), (1, 2)),
        )

        rows = atlas["records"]
        self.assertEqual(rows[-1]["resources_checked"], 48)
        self.assertEqual(rows[-1]["pairwise_mi_failure_count"], 18)
        self.assertTrue(
            all(
                row["all_interaction_graphs_recovered_from_pauli_correlations"]
                for row in rows
            )
        )
        self.assertTrue(
            all(row["all_pairings_recovered_from_full_block_mi"] for row in rows)
        )

    def test_low_order_entropy_and_channel_transfer(self):
        witness = self.certificate["representative_witness"]
        audit = witness["comparisons"]["low_order_physical_entropy_audit"]
        self.assertEqual(audit["max_order"], 3)
        self.assertEqual(audit["mismatch_count"], 0)
        self.assertEqual(witness["comparisons"]["first_entropy_mismatch"]["order"], 4)

        transfer = witness["transfer_certificate"]
        self.assertEqual(
            transfer["inferred_interaction_edges_used_for_inverse"],
            ((0, 1), (1, 2)),
        )
        self.assertEqual(transfer["capacities"]["state_derived_activation"], 3)
        self.assertLess(
            transfer["capacities"]["identity_activation_after_interaction_removal"],
            3,
        )
        self.assertEqual(transfer["capacities"]["mouth_blind_scrambling_control"], 0)

    def test_custom_graph_edges_are_normalized(self):
        model = InteractingEncodedBridgeModel(
            name="normalized",
            pairing=(0, 1, 2),
            interaction_edges=((2, 1), (1, 2), (0, 2)),
        )
        self.assertEqual(model.interaction_edges, ((0, 2), (1, 2)))
        self.assertEqual(
            model.state_derived_interaction_graph_record()[
                "inferred_right_block_interaction_edges"
            ],
            ((0, 2), (1, 2)),
        )


if __name__ == "__main__":
    unittest.main()
