import unittest

from qgtoy.typeii_static_patch_limit import (
    factorial_cutoff,
    factorial_matrix_dim,
    factorial_subsequence_inclusion_record,
    full_matrix_unital_inclusion_exists,
    major_goal_finite_to_typeii_static_patch_certificate,
    persistent_noncommutative_witness,
    raw_consecutive_inclusion_record,
)


class TypeIIStaticPatchLimitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = major_goal_finite_to_typeii_static_patch_certificate(
            max_level=4,
            max_consecutive_cutoff=5,
            bridge_cert_max_cutoff=5,
            noise_strength=1.0,
            fixed_lapse=1.0,
            environment_qubits=4,
            temperature_scale=1.0,
            screen_probability=0.75,
            low_order=2,
            perturbation_radius=0.05,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertEqual(
            self.certificate["result_type"],
            "finite_to_von_neumann_algebra_theorem_candidate",
        )

    def test_raw_consecutive_cutoffs_have_matrix_inclusion_no_go(self):
        for cutoff in range(1, 6):
            record = raw_consecutive_inclusion_record(cutoff)
            self.assertFalse(
                record["unital_trace_preserving_star_inclusion_exists"]
            )
            self.assertIn("n divides m", record["obstruction"])
        self.assertFalse(full_matrix_unital_inclusion_exists(4, 9))

    def test_factorial_cutoffs_give_trace_preserving_inclusions(self):
        self.assertEqual(factorial_cutoff(1), 1)
        self.assertEqual(factorial_cutoff(2), 5)
        self.assertEqual(factorial_matrix_dim(1), 4)
        self.assertEqual(factorial_matrix_dim(2), 36)
        for level in range(1, 4):
            record = factorial_subsequence_inclusion_record(level)
            self.assertTrue(record["unital_star_inclusion_exists"])
            self.assertTrue(record["normalized_trace_preserved"])
            self.assertTrue(record["diagonal_trace_preserved"])
            self.assertEqual(
                record["multiplicity"],
                record["expected_multiplicity"],
            )

    def test_quantum_limit_and_dephased_limit_split(self):
        theorem = self.certificate["theorem_record"]
        quantum = theorem["quantum_inductive_limit"]
        dephased = theorem["dephased_control_limit"]
        self.assertEqual(
            quantum["tracial_gns_von_neumann_closure"],
            "hyperfinite Type II_1 factor R",
        )
        self.assertEqual(
            dephased["tracial_gns_von_neumann_closure"],
            "diffuse abelian von Neumann algebra",
        )
        self.assertTrue(dephased["commutators_vanish_levelwise"])

    def test_noncommutative_witness_persists_but_dephased_commutator_vanishes(self):
        witness = persistent_noncommutative_witness(4)
        self.assertEqual(witness["operator_norm"], 1.0)
        self.assertEqual(witness["tracial_2_norm_squared"], 0.5)
        self.assertTrue(witness["persists_under_trace_preserving_inclusions"])
        self.assertEqual(witness["dephased_control_commutator_norm"], 0.0)

    def test_screen_shadows_match_and_bridge_gate_is_inherited(self):
        claims = self.certificate["certified_claims"]
        self.assertTrue(claims["screen_shadows_match_levelwise"])
        self.assertTrue(claims["strong_continuity_gate_preserved"])
        self.assertTrue(
            self.certificate["relationship_to_goal31"][
                "bridge_diagnostic_preserved"
            ]
        )

    def test_modular_limit_extra_assumption_is_explicit(self):
        requirement = self.certificate["theorem_record"][
            "conditional_modular_requirement"
        ]
        self.assertEqual(
            requirement["required_assumption"],
            "inclusion_covariant_static_patch_generators",
        )
        self.assertIn("do not prove", requirement["why_needed"])
        self.assertTrue(
            self.certificate["certified_claims"][
                "modular_semigroup_limit_requires_extra_covariance_assumption"
            ]
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(max_level=1)
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(
                max_consecutive_cutoff=0,
            )
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(
                bridge_cert_max_cutoff=0,
            )
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(fixed_lapse=0.0)
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(environment_qubits=0)
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(temperature_scale=0.0)
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            major_goal_finite_to_typeii_static_patch_certificate(
                perturbation_radius=1.0,
            )


if __name__ == "__main__":
    unittest.main()
