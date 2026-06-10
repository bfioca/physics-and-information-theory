import unittest
from math import log

from qgtoy.interacting_kms_edge import (
    boundary_gibbs_distribution_record,
    interacting_core_obstruction_record,
    interacting_kms_edge_certificate,
    interacting_kms_limit_record,
    interacting_symmetry_record,
    rotational_scalar_bath_no_go_record,
)


class InteractingKmsEdgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = interacting_kms_edge_certificate(max_level=7)

    def test_certificate_passes_with_engineered_model_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["finite_verified_claims"].values()))
        self.assertTrue(
            all(self.certificate["theorem_backed_limit_claims"].values())
        )
        self.assertIn("engineered finite-boundary", self.certificate["claim_boundary"])

    def test_boundary_gibbs_state_is_faithful_normalized_and_correlated(self):
        for level in range(1, 7):
            record = boundary_gibbs_distribution_record(level, coupling=0.3)
            self.assertTrue(record["state_is_faithful_analytically"])
            self.assertLess(record["normalization_error"], 1e-14)
            self.assertGreater(record["ell_first_site_mutual_information_float"], 0.0)
            self.assertFalse(record["boundary_state_factorizes_angular_first_site"])

    def test_zero_coupling_recovers_a_product_boundary_state(self):
        record = boundary_gibbs_distribution_record(5, coupling=0.0)
        self.assertAlmostEqual(record["ell_first_site_mutual_information_float"], 0.0)
        self.assertTrue(record["boundary_state_factorizes_angular_first_site"])

    def test_extreme_parameters_do_not_break_analytic_faithfulness(self):
        record = boundary_gibbs_distribution_record(100, beta=1000.0)
        self.assertTrue(record["state_is_faithful_analytically"])
        self.assertLess(record["normalization_error"], 1e-14)
        self.assertFalse(record["floating_table_resolves_all_probabilities"])

    def test_tiny_nonzero_coupling_is_analytically_nonproduct(self):
        record = boundary_gibbs_distribution_record(1, coupling=1e-11)
        self.assertFalse(record["boundary_state_factorizes_angular_first_site"])
        self.assertTrue(record["nonzero_coupling_implies_nonproduct_analytically"])
        self.assertGreaterEqual(record["ell_first_site_mutual_information_float"], 0.0)

    def test_interaction_is_rotationally_invariant(self):
        record = interacting_symmetry_record(5, coupling=0.4)
        self.assertTrue(record["commutes_with_K_L"])
        self.assertTrue(record["commutes_with_J_z"])
        self.assertTrue(record["commutes_with_full_SU2"])
        self.assertTrue(record["expectations_commute_with_modular_flow"])

    def test_type_iii_tail_and_type_ii_core_survive_boundary_interaction(self):
        record = interacting_kms_limit_record(4, beta=3.0, coupling=0.4)
        self.assertEqual(record["inverse_temperature_beta"], 3.0)
        self.assertTrue(record["state_is_beta_kms_for_declared_dynamics"])
        self.assertEqual(record["von_neumann_algebra_type"], "hyperfinite Type III_1 factor")
        self.assertEqual(
            record["continuous_core_type"],
            "hyperfinite Type II_infinity factor",
        )
        self.assertTrue(record["symmetry_expectations_extend_to_core"])

    def test_recovery_and_entropy_obstruction_survive_interaction(self):
        for level in range(1, 8):
            record = interacting_core_obstruction_record(level)
            self.assertFalse(record["probe_states_are_the_background_kms_state"])
            self.assertEqual(record["background_kms_relative_entropy_loss"], 0.0)
            self.assertEqual(record["decoder_error_lower_bound"], 0.5)
            self.assertAlmostEqual(
                record["time_then_axial_relative_entropy_loss"],
                log(2.0),
            )
            self.assertAlmostEqual(
                record["full_rotation_relative_entropy_loss"],
                log(2 * level + 1),
            )
            self.assertFalse(record["boundary_interaction_changes_edge_obstruction"])

    def test_rotational_scalar_bath_no_go_is_coupling_independent(self):
        for level in range(1, 8):
            record = rotational_scalar_bath_no_go_record(level)
            self.assertEqual(
                record["most_general_invariant_hamiltonian_on_sector"],
                "I_{V_L} tensor H_bath,L",
            )
            self.assertTrue(record["result_is_independent_of_bath_hamiltonian"])
            self.assertTrue(record["result_is_independent_of_coupling_strength"])
            self.assertAlmostEqual(
                record["probe_full_rotation_relative_entropy_loss"],
                log(2 * level + 1),
            )
            self.assertFalse(record["continuous_core_clock_can_restore_orientation"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            boundary_gibbs_distribution_record(0)
        with self.assertRaises(ValueError):
            boundary_gibbs_distribution_record(1, beta=0.0)
        with self.assertRaises(ValueError):
            boundary_gibbs_distribution_record(1, angular_scale=-1.0)
        with self.assertRaises(ValueError):
            boundary_gibbs_distribution_record(1, first_site_gap=0.0)
        with self.assertRaises(ValueError):
            boundary_gibbs_distribution_record(1, coupling=-1.0)
        with self.assertRaises(ValueError):
            interacting_kms_edge_certificate(max_level=0)
        with self.assertRaises(ValueError):
            interacting_kms_edge_certificate(coupling=0.0)


if __name__ == "__main__":
    unittest.main()
