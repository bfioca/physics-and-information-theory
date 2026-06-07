import unittest

from qgtoy.lift_diagnostics import (
    declared_screen_shadow_record,
    embedding_response_witness_records,
    finite_lift_decision_record,
    response_witness_gap,
    response_witness_record,
    screen_shadow_equal_for_quantum_dephased,
)


class LiftDiagnosticsTest(unittest.TestCase):
    def test_declared_screen_shadow_ignores_source_algebra(self):
        quantum = declared_screen_shadow_record(4, algebra_kind="matrix")
        dephased = declared_screen_shadow_record(4, algebra_kind="abelian")
        self.assertEqual(quantum, dephased)
        self.assertTrue(screen_shadow_equal_for_quantum_dephased(4))
        self.assertEqual(quantum["screen_algebra"], "C^4")
        self.assertIn("diagonal_observables", quantum["allowed_data"])

    def test_response_witness_separates_matrix_from_abelian_control(self):
        matrix = response_witness_record(4, algebra_kind="matrix")
        abelian = response_witness_record(4, algebra_kind="abelian")
        self.assertEqual(matrix["chosen_topology"], "operator_norm")
        self.assertEqual(matrix["nu_lower_bound"], 1.0)
        self.assertEqual(abelian["nu_lower_bound"], 0.0)
        self.assertEqual(response_witness_gap(4), 1.0)
        self.assertIn("rank-one trace-L2", matrix["rank_one_l2_warning"])

    def test_embedding_response_witness_records_are_direct_and_positive(self):
        records = embedding_response_witness_records(max_cutoff=5)
        self.assertEqual(len(records), 20)
        self.assertTrue(
            all(record["response_witness_persists"] for record in records)
        )
        self.assertTrue(
            all(record["response_lower_bound"] > 0.0 for record in records)
        )
        self.assertTrue(
            all(record["screen_shadow_convergent_or_exact"] for record in records)
        )
        candidates = {record["candidate"] for record in records}
        self.assertIn("heat_kernel_coarse_graining", candidates)
        self.assertIn("berezin_toeplitz_inspired_smoothing", candidates)

    def test_finite_lift_decision_selects_theorem_candidate(self):
        decision = finite_lift_decision_record(max_cutoff=5)
        self.assertEqual(decision["selected_outcome"], "A_theorem_candidate")
        self.assertTrue(decision["finite_requirements_satisfied"])
        self.assertEqual(decision["failed_conditions"], ())
        statuses = {
            condition["condition"]: condition["status"]
            for condition in decision["conditions"]
        }
        self.assertEqual(statuses["screen_shadow_equality"], "finite_proved")
        self.assertEqual(
            statuses["canonical_static_patch_embedding"],
            "conditional_assumption",
        )
        self.assertGreater(
            decision["minimum_embedding_response_lower_bound"],
            0.0,
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            declared_screen_shadow_record(1, algebra_kind="matrix")
        with self.assertRaises(ValueError):
            declared_screen_shadow_record(4, algebra_kind="not-valid")
        with self.assertRaises(ValueError):
            declared_screen_shadow_record(4, algebra_kind="matrix", low_order=-1)
        with self.assertRaises(ValueError):
            response_witness_record(1, algebra_kind="matrix")
        with self.assertRaises(ValueError):
            response_witness_record(4, algebra_kind="not-valid")


if __name__ == "__main__":
    unittest.main()
