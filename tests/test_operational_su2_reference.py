import unittest
from fractions import Fraction

from qgtoy.operational_su2_reference import (
    finite_reference_exact_recovery_no_go_record,
    joint_irrep_multiplicities,
    minimal_reducible_reference_record,
    multiplicity_recovery_bound_record,
    operational_su2_reference_certificate,
    peter_weyl_closed_deficit_fraction,
    peter_weyl_entanglement_fidelity_fraction,
    peter_weyl_mean_casimir_fraction,
    peter_weyl_multiplier_fraction,
    peter_weyl_recovery_record,
    peter_weyl_reference_dimension,
)


class OperationalSu2ReferenceTest(unittest.TestCase):
    def test_peter_weyl_dimension_formula(self):
        for cutoff in range(0, 20):
            self.assertEqual(
                peter_weyl_reference_dimension(cutoff),
                sum((2 * spin + 1) ** 2 for spin in range(cutoff + 1)),
            )

    def test_joint_multiplicity_formula_and_single_irrep_limit(self):
        for system_spin in range(1, 8):
            single = tuple(
                1 if reference_spin == system_spin else 0
                for reference_spin in range(system_spin + 1)
            )
            multiplicities = joint_irrep_multiplicities(system_spin, single)
            self.assertTrue(all(value == 1 for _, value in multiplicities))
            bound = multiplicity_recovery_bound_record(system_spin, single)
            self.assertAlmostEqual(
                bound["normalized_diamond_recovery_error_lower_bound"],
                1.0 - 1.0 / (2 * system_spin + 1),
            )

    def test_minimal_reducible_reference_has_one_qubit_block(self):
        for system_spin in range(1, 8):
            record = minimal_reducible_reference_record(system_spin)
            self.assertEqual(record["maximum_joint_multiplicity_r"], 2)
            self.assertEqual(
                record["fixed_operator_algebra_explicit"],
                "C direct_sum M_2 direct_sum C",
            )
            self.assertAlmostEqual(
                record["normalized_diamond_recovery_error_lower_bound"],
                max(0.0, 1.0 - 2.0 / (2 * system_spin + 1)),
            )

    def test_double_sum_multiplier_matches_closed_formula(self):
        for reference_cutoff in range(1, 14):
            for tensor_rank in range(2 * reference_cutoff + 1):
                self.assertEqual(
                    1 - peter_weyl_multiplier_fraction(
                        reference_cutoff,
                        tensor_rank,
                    ),
                    peter_weyl_closed_deficit_fraction(
                        reference_cutoff,
                        tensor_rank,
                    ),
                )

    def test_multipliers_are_unital_and_rank_deficits_are_monotone(self):
        for system_spin in range(1, 7):
            record = peter_weyl_recovery_record(system_spin, 4 * system_spin)
            self.assertEqual(record["tensor_rank_multipliers"][0], 1.0)
            self.assertTrue(record["closed_formula_agrees"])
            self.assertTrue(record["deficits_are_nondecreasing_with_rank"])
            self.assertFalse(record["exact_recovery_at_finite_cutoff"])
            self.assertFalse(record["decoder_is_claimed_optimal"])

    def test_entanglement_fidelity_matches_superoperator_trace(self):
        for system_spin in range(1, 6):
            dimension = 2 * system_spin + 1
            for reference_cutoff in (2 * system_spin, 5 * system_spin):
                expected = sum(
                    (2 * rank + 1)
                    * peter_weyl_multiplier_fraction(reference_cutoff, rank)
                    for rank in range(2 * system_spin + 1)
                ) / dimension**2
                self.assertEqual(
                    peter_weyl_entanglement_fidelity_fraction(
                        system_spin,
                        reference_cutoff,
                    ),
                    expected,
                )

    def test_casimir_identity_and_constructive_convergence(self):
        for cutoff in range(0, 20):
            direct = Fraction(
                sum(
                    (2 * spin + 1) ** 2 * spin * (spin + 1)
                    for spin in range(cutoff + 1)
                ),
                peter_weyl_reference_dimension(cutoff),
            )
            self.assertEqual(peter_weyl_mean_casimir_fraction(cutoff), direct)
        for system_spin in range(1, 6):
            bounds = tuple(
                peter_weyl_recovery_record(system_spin, scale * system_spin)[
                    "normalized_diamond_error_upper_bound"
                ]
                for scale in (2, 4, 8, 16, 32)
            )
            self.assertTrue(all(right <= left for left, right in zip(bounds, bounds[1:])))
            self.assertLess(bounds[-1], bounds[0])

    def test_finite_reference_exact_no_go_is_explicitly_analytic(self):
        record = finite_reference_exact_recovery_no_go_record(3)
        self.assertFalse(record["exact_deterministic_decoder_exists"])
        self.assertIn("Knill-Laflamme", record["verification_mode"])

    def test_certificate_passes_with_physics_boundary(self):
        certificate = operational_su2_reference_certificate(
            max_system_spin=6,
            reference_scale=8,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("not proved optimal", certificate["claim_boundary"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            peter_weyl_reference_dimension(-1)
        with self.assertRaises(ValueError):
            joint_irrep_multiplicities(1, ())
        with self.assertRaises(ValueError):
            joint_irrep_multiplicities(1, (0, 0))
        with self.assertRaises(ValueError):
            peter_weyl_closed_deficit_fraction(2, 5)
        with self.assertRaises(ValueError):
            operational_su2_reference_certificate(reference_scale=1)


if __name__ == "__main__":
    unittest.main()
