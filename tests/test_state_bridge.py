import unittest

from qgtoy.state_bridge import (
    goal14_state_derived_bridge_dynamics_certificate,
    screen_success_probability_from_channel,
)
from qgtoy.quantum_channel import coherent_bilayer_screen_kraus


class StateDerivedBridgeDynamicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal14_state_derived_bridge_dynamics_certificate(
            mouths=2,
            low_order=3,
            atlas_max_mouths=3,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_state_derives_twisted_pairing(self):
        witness = self.certificate["representative_witness"]
        pairing = witness["state_derived_pairing"]
        self.assertEqual(pairing["inferred_pairing"], (1, 0))
        self.assertTrue(pairing["unique_permutation_inferred"])
        self.assertFalse(pairing["uses_declared_pairing_as_decoder_input"])
        rows = pairing["pairing_rows"]
        self.assertEqual(rows[0]["mutual_information_by_right_block"], (0, 2))
        self.assertEqual(rows[1]["mutual_information_by_right_block"], (2, 0))

    def test_low_order_entropy_blindness_and_decoder_scale_split(self):
        comparisons = self.certificate["representative_witness"]["comparisons"]
        audit = comparisons["low_order_physical_entropy_audit"]
        self.assertEqual(audit["max_order"], 3)
        self.assertEqual(audit["regions_checked"], 299)
        self.assertEqual(audit["mismatch_count"], 0)
        self.assertEqual(comparisons["first_entropy_mismatch"]["order"], 4)

    def test_state_derived_activation_restores_channel(self):
        witness = self.certificate["representative_witness"]
        comparisons = witness["comparisons"]
        self.assertEqual(
            comparisons["identity_activation_capacity"],
            {"aligned": 2, "twisted": 0},
        )
        self.assertEqual(
            comparisons["state_derived_activation_capacity"],
            {"twisted_clifford": 2, "twisted_non_clifford_T": 2},
        )
        self.assertEqual(comparisons["mouth_blind_scrambling_capacity"], {"twisted": 0})

        explicit = witness["explicit_channel_certificates"]
        wrong = explicit["identity_activation_on_twisted_state"]
        recovered = explicit["state_derived_activation_on_twisted_state"]
        self.assertEqual(wrong["fixed_port_transmission"]["perfect_qubits"], 0)
        self.assertEqual(wrong["preserved_operator_algebra"]["center_dimension"], 2)
        self.assertEqual(recovered["choi"]["rank"], 1)
        self.assertEqual(
            recovered["fidelity"]["entanglement_fidelity_to_identity"],
            1.0,
        )

    def test_screen_success_probability_is_channel_derived(self):
        north = coherent_bilayer_screen_kraus(0.75, screen="north")
        south = coherent_bilayer_screen_kraus(0.75, screen="south")
        self.assertAlmostEqual(screen_success_probability_from_channel(north), 0.75)
        self.assertAlmostEqual(screen_success_probability_from_channel(south), 0.25)

    def test_screen_recovery_and_area_transition_match(self):
        transition = self.certificate["state_derived_screen_transition"]
        self.assertTrue(transition["all_probabilities_recovered_from_channels"])
        self.assertTrue(transition["recovery_and_area_winners_match"])
        self.assertTrue(transition["midpoint_transition_from_state"])
        records = {
            row["source_circuit_parameter_not_used_by_decoder"]: row
            for row in transition["records"]
        }
        self.assertEqual(records[0.0]["recovery_winner"], "south")
        self.assertEqual(records[0.5]["recovery_winner"], "tie")
        self.assertEqual(records[1.0]["recovery_winner"], "north")
        self.assertEqual(records[0.75]["larger_entropy_area_analogue"], "north")

    def test_external_area_bias_no_go(self):
        no_go = self.certificate["external_area_bias_no_go"]
        self.assertFalse(no_go["transitions_match"])
        self.assertEqual(no_go["recovery_transition_probability"], 0.5)
        self.assertEqual(no_go["quantum_area_transition_probability"], 0.375)
        self.assertEqual(no_go["transition_mismatch"], 0.125)

    def test_bounded_atlas(self):
        atlas = self.certificate["bounded_atlas"]
        first_split = atlas["first_entropy_matched_identity_transfer_split"]
        self.assertEqual(first_split["m"], 2)
        self.assertEqual(
            first_split["identity_activation_capacity_profile"],
            {0: 1, 2: 1},
        )
        self.assertEqual(
            first_split["state_derived_activation_capacity_profile"],
            {2: 2},
        )
        self.assertEqual(first_split["mouth_blind_scrambling_capacity_profile"], {0: 2})
        self.assertTrue(
            all(row["all_pairings_recovered_from_state"] for row in atlas["records"])
        )
        self.assertTrue(
            all(row["state_derived_activation_full_capacity"] for row in atlas["records"])
        )


if __name__ == "__main__":
    unittest.main()
