import unittest

from qgtoy.canonical_noncommutative_refinement import (
    SHARPER_MINIMAL_ASSUMPTION,
    canonical_noncommutative_candidate_records,
    canonical_noncommutative_refinement_certificate,
)


class CanonicalNoncommutativeRefinementTest(unittest.TestCase):
    def test_candidate_audit_covers_declared_subsystems(self):
        records = canonical_noncommutative_candidate_records(max_cutoff=6)
        self.assertEqual(len(records), 5)
        self.assertEqual(
            {record["candidate_id"] for record in records},
            {
                "low_angular_momentum_matrix_modes",
                "fuzzy_coordinate_polynomial_algebra",
                "coherent_state_localized_matrix_patches",
                "finite_toeplitz_matrix_fiber_quantization",
                "heat_kernel_refined_low_energy_operator_system",
            },
        )
        for record in records:
            self.assertTrue(record["anti_tautological_selection"])
            self.assertEqual(
                set(record["gate_status"]),
                {
                    "anti_tautological_selection",
                    "cp_unital_trace",
                    "low_mode_multiplicativity",
                    "covariance",
                    "screen_shadow",
                    "norm_faithfulness",
                    "nonzero_commutator_limit",
                    "strong_continuity",
                    "typeii_route",
                },
            )

    def test_certificate_selects_sharper_minimal_assumption(self):
        certificate = canonical_noncommutative_refinement_certificate(max_cutoff=6)
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["selected_outcome"], "C_sharper_minimal_assumption")
        self.assertEqual(
            certificate["result_type"],
            "sharper_minimal_assumption_for_canonical_refinement",
        )
        self.assertEqual(
            certificate["sharper_minimal_assumption"],
            SHARPER_MINIMAL_ASSUMPTION,
        )
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_scalar_canonical_routes_classicalize(self):
        certificate = canonical_noncommutative_refinement_certificate(max_cutoff=6)
        gates = certificate["gate_status_by_candidate"]
        for candidate_id in (
            "low_angular_momentum_matrix_modes",
            "fuzzy_coordinate_polynomial_algebra",
        ):
            self.assertIn(candidate_id, certificate["no_go_candidates"])
            self.assertEqual(gates[candidate_id]["screen_shadow"], "pass")
            self.assertEqual(gates[candidate_id]["nonzero_commutator_limit"], "fail")
            self.assertEqual(gates[candidate_id]["typeii_route"], "fail")

    def test_conditional_routes_need_noncommutative_selection(self):
        certificate = canonical_noncommutative_refinement_certificate(max_cutoff=6)
        gates = certificate["gate_status_by_candidate"]
        self.assertEqual(
            set(certificate["missing_assumption_candidates"]),
            {
                "coherent_state_localized_matrix_patches",
                "finite_toeplitz_matrix_fiber_quantization",
                "heat_kernel_refined_low_energy_operator_system",
            },
        )
        for candidate_id in certificate["missing_assumption_candidates"]:
            self.assertEqual(gates[candidate_id]["nonzero_commutator_limit"], "conditional")
            self.assertEqual(gates[candidate_id]["typeii_route"], "conditional")

    def test_heat_route_is_not_enough_by_itself(self):
        certificate = canonical_noncommutative_refinement_certificate(max_cutoff=6)
        gates = certificate["gate_status_by_candidate"][
            "heat_kernel_refined_low_energy_operator_system"
        ]
        self.assertEqual(gates["strong_continuity"], "pass")
        self.assertEqual(gates["norm_faithfulness"], "pass")
        self.assertEqual(gates["nonzero_commutator_limit"], "conditional")
        self.assertTrue(
            certificate["certified_claims"][
                "heat_route_is_not_enough_without_noncommutative_sector"
            ]
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            canonical_noncommutative_candidate_records(max_cutoff=1)
        with self.assertRaises(ValueError):
            canonical_noncommutative_refinement_certificate(max_cutoff=1)


if __name__ == "__main__":
    unittest.main()
