import unittest

from qgtoy.fuzzy_berezin import (
    berezin_eigenvalue,
    berezin_coarse_graining,
    berezin_refinement,
    berezin_refinement_coefficient,
    berezin_state_lift,
    coefficient_error_bound,
    composition_coefficient_defect,
    coordinate_atomic_product_defect_bound,
    coordinate_atomic_product_record,
    fuzzy_berezin_refinement_certificate,
    global_unit_ball_defect_lower_bound,
)
from qgtoy.fuzzy_sphere import fuzzy_harmonics, hilbert_schmidt_inner
from qgtoy.quantum_channel import identity_matrix, matmul, max_abs_difference, trace


class FuzzyBerezinRefinementTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = fuzzy_berezin_refinement_certificate(
            max_source_level=4, max_mode=2
        )

    def test_certificate_passes_with_explicit_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertEqual(
            self.certificate["result_type"],
            "canonical_ucp_low_mode_refinement_theorem",
        )
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertIn("full matrix unit ball", self.certificate["claim_boundary"])

    def test_berezin_eigenvalue_formula(self):
        self.assertEqual(berezin_eigenvalue(5, 0), 1.0)
        self.assertAlmostEqual(berezin_eigenvalue(5, 1), 5.0 / 7.0)
        self.assertAlmostEqual(
            berezin_eigenvalue(5, 2), (5.0 / 7.0) * (4.0 / 8.0)
        )

    def test_refinement_is_unital(self):
        for source in range(1, 4):
            image = berezin_refinement(source, source + 1, identity_matrix(source + 1))
            self.assertLess(
                max_abs_difference(image, identity_matrix(source + 2)), 1e-10
            )

    def test_state_lift_is_trace_preserving_and_dual_to_coarse_graining(self):
        source = 2
        target = 4
        source_operator = fuzzy_harmonics(source)[(1, 0)]
        target_operator = fuzzy_harmonics(target)[(1, 0)]
        lifted = berezin_state_lift(source, target, source_operator)
        coarse = berezin_coarse_graining(source, target, target_operator)
        self.assertAlmostEqual(
            trace(matmul(lifted, target_operator)).real,
            trace(matmul(source_operator, coarse)).real,
        )
        maximally_mixed = tuple(
            tuple((1.0 / (source + 1)) if row == column else 0.0 for column in range(source + 1))
            for row in range(source + 1)
        )
        self.assertAlmostEqual(
            trace(berezin_state_lift(source, target, maximally_mixed)).real,
            1.0,
        )
        self.assertLess(
            max_abs_difference(
                berezin_coarse_graining(source, target, identity_matrix(target + 1)),
                identity_matrix(source + 1),
            ),
            1e-10,
        )

    def test_harmonics_have_the_predicted_multiplier(self):
        source = 3
        target = 5
        source_harmonics = fuzzy_harmonics(source)
        target_harmonics = fuzzy_harmonics(target)
        for label, source_harmonic in source_harmonics.items():
            image = berezin_refinement(source, target, source_harmonic)
            coefficient = hilbert_schmidt_inner(target_harmonics[label], image)
            self.assertAlmostEqual(
                coefficient.real,
                berezin_refinement_coefficient(source, target, label[0]),
                places=10,
            )
            self.assertAlmostEqual(coefficient.imag, 0.0, places=10)

    def test_low_mode_coefficient_bound(self):
        for source in range(2, 8):
            for target in range(source, source + 3):
                for ell in range(source + 1):
                    error = 1.0 - berezin_refinement_coefficient(source, target, ell)
                    self.assertLessEqual(
                        error, coefficient_error_bound(source, target, ell) + 1e-14
                    )

    def test_composition_defect_has_inverse_cutoff_bound(self):
        for source in range(1, 8):
            for ell in range(source + 1):
                defect = composition_coefficient_defect(
                    source, source + 1, source + 2, ell
                )
                self.assertLessEqual(
                    defect, ell * (ell + 1.0) / (source + 3.0) + 1e-14
                )

    def test_coordinate_atomic_ball_has_uniform_product_bound(self):
        previous = None
        for level in range(2, 9):
            record = coordinate_atomic_product_record(level)
            bound = coordinate_atomic_product_defect_bound(level)
            self.assertAlmostEqual(
                record["analytic_uniform_operator_norm_bound"], bound
            )
            self.assertLessEqual(record["analytic_diagonal_pair_bound"], bound)
            self.assertLessEqual(record["analytic_off_diagonal_pair_bound"], bound)
            self.assertLessEqual(record["max_direct_induced_infinity_norm"], bound)
            if previous is not None:
                self.assertLess(bound, previous)
            previous = bound

    def test_full_unit_ball_has_persistent_high_mode_obstruction(self):
        for level in range(1, 10):
            lower_bound = global_unit_ball_defect_lower_bound(level, level + 1)
            self.assertGreaterEqual(lower_bound, 0.5 - 1e-14)
        self.assertAlmostEqual(
            global_unit_ball_defect_lower_bound(40, 41),
            0.5,
            delta=0.02,
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            berezin_eigenvalue(0, 0)
        with self.assertRaises(ValueError):
            berezin_eigenvalue(2, 3)
        with self.assertRaises(ValueError):
            berezin_refinement(2, 1, identity_matrix(3))
        with self.assertRaises(ValueError):
            berezin_refinement(1, 2, identity_matrix(3))
        with self.assertRaises(ValueError):
            fuzzy_berezin_refinement_certificate(max_source_level=0)
        with self.assertRaises(ValueError):
            coordinate_atomic_product_defect_bound(1)


if __name__ == "__main__":
    unittest.main()
