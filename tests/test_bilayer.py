import unittest

from qgtoy.bilayer import bilayer_reconstruction_program_certificate
from qgtoy.quantum_channel import teleportation_channel_certificate


class BilayerProgramTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = bilayer_reconstruction_program_certificate()

    def test_program_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_explicit_two_mouth_channels(self):
        channels = self.certificate["explicit_teleportation_channels"]
        aligned = channels["aligned_identity_decoder"]
        crossed = channels["crossed_identity_decoder"]
        corrected = channels["crossed_pairing_aware_decoder"]

        self.assertEqual(aligned["choi"]["rank"], 1)
        self.assertEqual(aligned["fidelity"]["entanglement_fidelity_to_identity"], 1.0)
        self.assertEqual(crossed["choi"]["rank"], 4)
        self.assertEqual(crossed["fixed_port_transmission"]["perfect_qubits"], 0)
        self.assertEqual(
            crossed["preserved_operator_algebra"]["exact_joint_noiseless_qubits"], 0
        )
        self.assertEqual(crossed["preserved_operator_algebra"]["center_dimension"], 2)
        self.assertEqual(
            {
                row["pauli"]
                for row in crossed["post_permutation_noise"]["pauli_error_distribution"]
            },
            {"II", "XX", "YY", "ZZ"},
        )
        self.assertEqual(corrected["choi"]["rank"], 1)
        self.assertEqual(
            corrected["fidelity"]["entanglement_fidelity_to_identity"], 1.0
        )

    def test_three_cycle_preserves_one_collective_noiseless_qubit(self):
        cycle = teleportation_channel_certificate((1, 2, 0), (0, 1, 2))
        algebra = cycle["preserved_operator_algebra"]
        self.assertEqual(cycle["fixed_port_transmission"]["perfect_qubits"], 0)
        self.assertEqual(algebra["exact_joint_noiseless_qubits"], 1)
        self.assertEqual(set(algebra["commutant_basis"]), {"XXX", "ZZZ"})

    def test_bounded_label_invariant_scan_counts(self):
        search = self.certificate["label_invariant_search"]
        self.assertFalse(search["collision_found"])
        scans = {(row["family"], row["n"]): row for row in search["scans"]}
        all_family = "all stabilizer codes modulo physical permutations"
        self.assertEqual(scans[(all_family, 1)]["codes_checked"], 1)
        self.assertEqual(scans[(all_family, 2)]["codes_checked"], 9)
        self.assertEqual(scans[(all_family, 3)]["codes_checked"], 75)
        self.assertEqual(scans[(all_family, 4)]["codes_checked"], 750)
        self.assertEqual(scans[(all_family, 4)]["complete_entropy_classes"], 13)
        graph_family = (
            "deleted-check codes from local-Clifford graph-state representatives, "
            "modulo physical permutations"
        )
        graph = scans[(graph_family, 5)]
        self.assertEqual(graph["codes_checked"], 33)
        self.assertEqual(graph["complete_entropy_classes"], 26)
        self.assertTrue(
            all(
                row["entropy_classes_with_multiple_reconstruction_nets"] == 0
                for row in search["scans"]
            )
        )

    def test_two_screen_transition(self):
        transition = self.certificate["two_screen_transition"]
        self.assertTrue(transition["all_isometries_verified"])
        self.assertTrue(transition["all_reduced_channels_trace_preserving"])
        self.assertTrue(
            transition["reduced_channels_are_standard_complementary_erasure_channels"]
        )
        self.assertTrue(transition["endpoint_reconstruction_verified"])
        self.assertTrue(transition["midpoint_tie_verified"])
        midpoint = next(
            row
            for row in transition["records"]
            if row["north_routing_probability"] == 0.5
        )
        self.assertAlmostEqual(
            midpoint["north_recovery"]["average_recovery_fidelity"], 0.75
        )
        self.assertAlmostEqual(
            midpoint["south_recovery"]["average_recovery_fidelity"], 0.75
        )

    def test_recovery_quantum_area_matching_and_bias_no_go(self):
        matching = self.certificate["recovery_saddle_matching"]
        self.assertTrue(matching["exact_matching_identity_verified"])
        self.assertTrue(matching["symmetric_transition_match_verified"])
        symmetric, biased = matching["area_bias_audit"]
        self.assertTrue(symmetric["transitions_match"])
        self.assertEqual(symmetric["quantum_area_transition_probability"], 0.5)
        self.assertFalse(biased["transitions_match"])
        self.assertEqual(biased["quantum_area_transition_probability"], 0.375)
        self.assertEqual(biased["transition_mismatch"], 0.125)

    def test_er_epr_ds_interpretation_gates(self):
        audit = self.certificate["er_epr_ds_interpretation"]
        self.assertTrue(audit["finite_algebraic_er_epr_analogue"])
        self.assertFalse(audit["geometric_er_epr_in_de_sitter_established"])
        self.assertFalse(audit["ds_cft_correspondence_advanced"])
        self.assertEqual(
            audit["screen_entanglement_entropy_for_pure_payload_bits"],
            1.0,
        )
        self.assertEqual(
            audit["screen_mutual_information_for_maximally_mixed_payload_bits"],
            2.0,
        )


if __name__ == "__main__":
    unittest.main()
