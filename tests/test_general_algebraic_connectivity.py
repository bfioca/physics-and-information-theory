import unittest

from qgtoy.general_algebraic_connectivity import (
    classical_relative_entropy_bits,
    coherence_probe_relative_entropy_bits,
    diagonal_probe_no_go_record,
    goal20_general_algebraic_connectivity_stability_certificate,
)


class GeneralAlgebraicConnectivityStabilityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal20_general_algebraic_connectivity_stability_certificate(
            max_dim=5,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_minimal_counterexample_has_exact_probe_collision(self):
        record = self.certificate["minimal_counterexample"]
        self.assertEqual(record["dimension"], 2)
        self.assertTrue(
            record["relative_entropy_response_on_probe_algebra"][
                "relative_entropy_defects_match"
            ]
        )
        self.assertTrue(
            record["product_commutator_closure_on_probe_algebra"][
                "closures_match"
            ]
        )
        self.assertTrue(record["static_entropy_shadow"]["shadows_match"])
        self.assertTrue(record["maximal_recoverable_observer_algebras"]["differ"])

    def test_qutrit_counterexample_is_non_pauli_finite_dimensional(self):
        record = self.certificate["non_pauli_finite_counterexample"]
        self.assertEqual(record["dimension"], 3)
        self.assertEqual(record["probe_algebra"], "C^3 diagonal subalgebra of M_3")
        self.assertEqual(
            record["maximal_recoverable_observer_algebras"]["identity_channel"],
            "M_3",
        )
        self.assertEqual(
            record["maximal_recoverable_observer_algebras"][
                "complete_dephasing_channel"
            ],
            "C^3",
        )

    def test_off_diagonal_completion_probe_separates_channels(self):
        record = diagonal_probe_no_go_record(4)
        completion = record["completion_probe"]
        self.assertGreater(completion["input_relative_entropy_bits"], 0.0)
        self.assertEqual(completion["dephasing_output_relative_entropy_bits"], 0.0)
        self.assertTrue(completion["off_diagonal_probe_separates_channels"])

    def test_bounded_dimension_family_checks_every_dimension(self):
        family = self.certificate["bounded_dimension_family"]
        self.assertEqual(family["dimensions_checked"], (2, 3, 4, 5))
        self.assertTrue(family["all_probe_diagnostics_collide"])
        self.assertTrue(family["all_maximal_algebras_differ"])
        self.assertTrue(family["all_completion_probes_separate"])

    def test_goal19_is_recovered_as_pauli_special_case(self):
        relationship = self.certificate["relationship_to_goal19"]
        self.assertEqual(relationship["goal19_status"], "pass")
        self.assertIn("one-qubit Pauli-diagonal", relationship["pauli_special_case"])
        self.assertIn("informationally complete", relationship["goal20_lift"])

    def test_conditional_completion_principle_names_missing_diagnostic(self):
        theorem = self.certificate["theorem_record"]
        self.assertIn("informationally complete", theorem["missing_diagnostic"])
        self.assertIn("maximal recoverable observer algebra", theorem["implication"])

    def test_relative_entropy_helpers_validate_inputs(self):
        self.assertGreater(
            classical_relative_entropy_bits((0.2, 0.8), (0.5, 0.5)),
            0.0,
        )
        self.assertGreater(coherence_probe_relative_entropy_bits(dim=2), 0.0)
        with self.assertRaises(ValueError):
            classical_relative_entropy_bits((1.0, 0.0), (0.5, 0.5))
        with self.assertRaises(ValueError):
            goal20_general_algebraic_connectivity_stability_certificate(max_dim=1)


if __name__ == "__main__":
    unittest.main()
