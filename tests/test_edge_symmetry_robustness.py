import unittest
from math import sin, sqrt

from qgtoy.edge_symmetry_robustness import (
    centered_zeeman_time_average,
    edge_symmetry_robustness_certificate,
    full_rotation_expectation,
    full_rotation_recovery_record,
    rotational_reference_hierarchy_record,
    symmetry_protected_perturbation_record,
    zeeman_robustness_record,
    zeeman_splitting,
)
from qgtoy.quantum_channel import identity_matrix, max_abs_difference
from qgtoy.relational_observer import within_block_phase_pair


class EdgeSymmetryRobustnessTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = edge_symmetry_robustness_certificate(max_level=7)

    def test_certificate_passes_with_explicit_model_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertIn("multiplicity-one SU(2)", self.certificate["claim_boundary"])

    def test_full_su2_fixed_algebra_and_dimension_formulas(self):
        for level in range(1, 10):
            record = rotational_reference_hierarchy_record(level)
            self.assertEqual(record["full_su2_fixed_algebra_dimension"], level + 1)
            self.assertEqual(
                record["full_su2_removed_dimension"],
                4 * level * (level + 1) * (level + 2) // 3,
            )
            self.assertAlmostEqual(
                record["full_su2_retained_fraction"],
                3.0 / (4.0 * level**2 + 8.0 * level + 3.0),
            )
            self.assertEqual(
                record["axial_u1_fixed_algebra_dimension"]
                // record["full_su2_fixed_algebra_dimension"],
                level + 1,
            )
            self.assertEqual(
                record["additional_dimension_removed_beyond_axial"],
                level * (level + 1),
            )

    def test_full_su2_fraction_has_three_quarters_scaled_limit(self):
        record = rotational_reference_hierarchy_record(1000)
        self.assertAlmostEqual(record["scaled_full_su2_fraction"], 0.75, delta=0.003)

    def test_full_rotation_expectation_is_unital_and_idempotent(self):
        level = 3
        identity = identity_matrix((level + 1) ** 2)
        self.assertEqual(full_rotation_expectation(level, identity), identity)
        plus, _minus = within_block_phase_pair(level)
        once = full_rotation_expectation(level, plus)
        self.assertLess(
            max_abs_difference(full_rotation_expectation(level, once), once),
            1e-14,
        )

    def test_full_rotation_collides_the_phase_pair(self):
        for level in range(1, 7):
            record = full_rotation_recovery_record(level)
            self.assertTrue(record["time_expectation_preserves_pair"])
            self.assertTrue(record["full_rotation_outputs_collide"])
            self.assertEqual(record["decoder_error_lower_bound"], 0.5)

    def test_irrational_zeeman_splitting_makes_the_spectrum_nondegenerate(self):
        record = zeeman_robustness_record(
            5,
            numerator=1,
            denominator=10**9,
            duration=2.0,
        )
        self.assertTrue(record["spectrum_is_nondegenerate"])
        self.assertFalse(record["exact_time_edge_separation_survives_infinite_average"])
        self.assertEqual(
            record["perturbed_infinite_time_fixed_algebra_dimension"],
            36,
        )

    def test_finite_time_visibility_obeys_exact_sinc_law(self):
        level = 4
        splitting = zeeman_splitting(numerator=1, denominator=100)
        duration = 3.0
        record = zeeman_robustness_record(
            level,
            numerator=1,
            denominator=100,
            duration=duration,
        )
        argument = splitting * level * duration
        expected = abs(sin(argument) / argument)
        self.assertAlmostEqual(record["analytic_finite_time_pair_visibility"], expected)
        self.assertAlmostEqual(record["matrix_finite_time_pair_visibility"], expected)
        self.assertTrue(record["visibility_is_not_monotone"])
        self.assertAlmostEqual(
            record["first_zero_time"],
            3.141592653589793 / (abs(splitting) * level),
        )

    def test_zero_duration_time_average_is_identity(self):
        level = 2
        plus, _minus = within_block_phase_pair(level)
        averaged = centered_zeeman_time_average(
            level,
            plus,
            splitting=sqrt(2.0),
            duration=0.0,
        )
        self.assertEqual(averaged, plus)

    def test_su2_invariant_perturbation_preserves_blocks(self):
        record = symmetry_protected_perturbation_record(6)
        self.assertTrue(record["commutes_with_full_su2"])
        self.assertTrue(record["magnetic_degeneracy_preserved"])
        self.assertTrue(record["time_edge_separation_survives"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            rotational_reference_hierarchy_record(0)
        with self.assertRaises(ValueError):
            full_rotation_expectation(1, identity_matrix(2))
        with self.assertRaises(ValueError):
            zeeman_splitting(numerator=0)
        with self.assertRaises(ValueError):
            zeeman_splitting(denominator=0)
        with self.assertRaises(ValueError):
            zeeman_robustness_record(1, duration=-1.0)
        with self.assertRaises(ValueError):
            edge_symmetry_robustness_certificate(max_level=0)


if __name__ == "__main__":
    unittest.main()
