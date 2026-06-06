import unittest

from qgtoy.algebraic_connectivity import (
    NoisyPauliBridge,
    goal19_algebraic_connectivity_order_parameter_certificate,
)


class AlgebraicConnectivityOrderParameterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal19_algebraic_connectivity_order_parameter_certificate(
            bloch_radius=0.5,
            epsilon_bits=0.25,
            response_only_epsilon_bits=0.4,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_stability_theorem_has_explicit_bounds(self):
        theorem = self.certificate["stability_theorem"]
        self.assertEqual(
            theorem["theorem"],
            "Pauli-diagonal noisy bridge stability bound",
        )
        self.assertGreater(theorem["mu_lower_bound_on_each_axis_shrink"], 0.0)
        self.assertGreater(
            theorem["average_gate_fidelity_to_identity_lower_bound"],
            0.5,
        )
        self.assertLess(
            theorem["product_commutator_defect_upper_bound"],
            1.0,
        )

    def test_noisy_examples_classify_quantum_classical_and_null(self):
        examples = {
            record["channel"]: record
            for record in self.certificate["representative_noisy_bridges"]
        }
        self.assertEqual(
            examples["clean_quantum_bridge"]["algebraic_phase"],
            "quantum_bridge",
        )
        self.assertEqual(
            examples["stable_noisy_quantum_bridge"]["algebraic_phase"],
            "quantum_bridge",
        )
        self.assertEqual(
            examples["classical_z_bridge"]["algebraic_phase"],
            "classical_bridge",
        )
        self.assertEqual(
            examples["null_depolarizing_bridge"]["algebraic_phase"],
            "null_bridge",
        )

    def test_static_entropy_shadow_is_blind_to_algebraic_phase(self):
        examples = self.certificate["representative_noisy_bridges"]
        shadows = {
            record["static_entropy_shadow"]["named_static_entropy_shadow"]
            for record in examples
        }
        phases = {record["algebraic_phase"] for record in examples}
        self.assertEqual(shadows, {(1.0, 1.0)})
        self.assertGreaterEqual(len(phases), 3)

    def test_response_only_shadow_can_fail_algebra_closure(self):
        no_go = self.certificate["response_only_no_go"]
        witness = no_go["witness"]
        self.assertEqual(
            witness["response_only_phase"],
            "incomplete_noncommuting_response_shadow",
        )
        self.assertEqual(witness["algebraic_phase"], "not_a_stable_algebra")
        self.assertEqual(witness["missing_commutator_axes"], ("Z",))

    def test_bounded_grid_records_phase_counts_and_entropy_blindness(self):
        grid = self.certificate["bounded_pauli_grid"]
        self.assertGreater(grid["cptp_channels_checked"], 0)
        self.assertTrue(grid["all_static_entropy_shadows_match"])
        self.assertGreater(grid["response_only_incomplete_shadow_count"], 0)
        self.assertIn("quantum_bridge", grid["phase_counts"])
        self.assertIn("classical_bridge", grid["phase_counts"])
        self.assertIn("null_bridge", grid["phase_counts"])

    def test_invalid_pauli_bridge_is_rejected(self):
        with self.assertRaises(ValueError):
            NoisyPauliBridge("bad", (1.0, 1.0, 0.0))

    def test_invalid_certificate_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            goal19_algebraic_connectivity_order_parameter_certificate(
                bloch_radius=1.0,
            )
        with self.assertRaises(ValueError):
            goal19_algebraic_connectivity_order_parameter_certificate(
                epsilon_bits=-0.1,
            )


if __name__ == "__main__":
    unittest.main()
