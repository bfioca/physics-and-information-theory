import unittest
from math import exp

from qgtoy.quantum_channel import identity_matrix, max_abs_difference
from qgtoy.relational_observer import (
    constraint_record,
    continuum_limit_record,
    diagonal_screen_expectation,
    edge_reference_record,
    extremal_edge_visibility,
    gaussian_edge_smearing,
    maximum_sigma_for_visibility,
    observer_algebra_hierarchy_record,
    physical_basis_labels,
    recovery_no_go_record,
    relational_observer_constraint_certificate,
    time_reference_expectation,
    within_block_phase_pair,
)


class RelationalObserverConstraintTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = relational_observer_constraint_certificate(max_level=6)

    def test_certificate_passes_with_non_gravitational_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertIn("not an Einstein constraint", self.certificate["claim_boundary"])

    def test_constraints_vanish_on_every_physical_label(self):
        for level in range(1, 6):
            record = constraint_record(level)
            self.assertEqual(record["physical_dimension"], (level + 1) ** 2)
            self.assertTrue(record["all_time_constraints_vanish"])
            self.assertTrue(record["all_angular_constraints_vanish"])

    def test_algebra_hierarchy_and_edge_dimension_formula(self):
        for level in range(1, 8):
            record = observer_algebra_hierarchy_record(level)
            self.assertTrue(record["time_constraint_alone_leaves_noncommutative_blocks"])
            self.assertEqual(
                record["edge_coherence_parameter_count"],
                level * (level + 1) * (4 * level + 5) // 3,
            )
            self.assertGreater(
                record["time_reference_hidden_algebra_dimension"],
                record["time_and_edge_references_hidden_algebra_dimension"],
            )
            self.assertAlmostEqual(
                record["diagonal_fraction_of_time_constraint_algebra"],
                3.0 * (level + 1.0) / (4.0 * level**2 + 8.0 * level + 3.0),
            )

    def test_diagonal_algebra_fraction_vanishes_with_three_quarters_scaling(self):
        fractions = tuple(
            observer_algebra_hierarchy_record(level)[
                "diagonal_fraction_of_time_constraint_algebra"
            ]
            for level in range(1, 30)
        )
        self.assertTrue(
            all(right < left for left, right in zip(fractions, fractions[1:]))
        )
        record = observer_algebra_hierarchy_record(1000)
        self.assertAlmostEqual(record["scaled_diagonal_fraction"], 0.75, delta=0.002)

    def test_conditional_expectations_are_unital_and_idempotent(self):
        level = 3
        dimension = (level + 1) ** 2
        identity = identity_matrix(dimension)
        self.assertEqual(time_reference_expectation(level, identity), identity)
        self.assertEqual(diagonal_screen_expectation(level, identity), identity)
        plus, _minus = within_block_phase_pair(level)
        time_once = time_reference_expectation(level, plus)
        self.assertEqual(time_reference_expectation(level, time_once), time_once)
        diagonal_once = diagonal_screen_expectation(level, plus)
        self.assertEqual(
            diagonal_screen_expectation(level, diagonal_once), diagonal_once
        )

    def test_time_block_retains_phase_while_diagonal_screen_collides(self):
        for level in range(1, 6):
            plus, minus = within_block_phase_pair(level)
            self.assertEqual(time_reference_expectation(level, plus), plus)
            self.assertEqual(time_reference_expectation(level, minus), minus)
            self.assertEqual(
                diagonal_screen_expectation(level, plus),
                diagonal_screen_expectation(level, minus),
            )
            record = recovery_no_go_record(level)
            self.assertAlmostEqual(
                record["decoder_worst_case_trace_distance_error_lower_bound"],
                0.5,
            )

    def test_perturbed_recovery_lower_bound(self):
        record = recovery_no_go_record(3, screen_distance=0.1)
        self.assertAlmostEqual(
            record["decoder_worst_case_trace_distance_error_lower_bound"], 0.45
        )

    def test_edge_smearing_visibility_and_resolution_law(self):
        sigma = 0.2
        target = 0.5
        invariant = None
        for level in range(1, 8):
            record = edge_reference_record(
                level, sigma=sigma, minimum_visibility=target
            )
            self.assertAlmostEqual(
                record["analytic_extremal_visibility"],
                exp(-2.0 * sigma**2 * level**2),
            )
            self.assertAlmostEqual(
                record["matrix_extremal_visibility"],
                record["analytic_extremal_visibility"],
            )
            self.assertAlmostEqual(
                record["decoder_error_lower_bound_after_smearing"],
                (1.0 - record["analytic_extremal_visibility"]) / 2.0,
            )
            scaled = level * maximum_sigma_for_visibility(
                level, visibility=target
            )
            if invariant is None:
                invariant = scaled
            self.assertAlmostEqual(scaled, invariant)
        self.assertLess(
            extremal_edge_visibility(8, sigma=sigma),
            extremal_edge_visibility(1, sigma=sigma),
        )
        self.assertGreater(
            edge_reference_record(8, sigma=sigma, minimum_visibility=target)[
                "decoder_error_lower_bound_after_smearing"
            ],
            edge_reference_record(1, sigma=sigma, minimum_visibility=target)[
                "decoder_error_lower_bound_after_smearing"
            ],
        )

    def test_gaussian_smearing_is_identity_at_zero_width(self):
        level = 2
        plus, _minus = within_block_phase_pair(level)
        self.assertLess(
            max_abs_difference(
                gaussian_edge_smearing(level, plus, sigma=0.0), plus
            ),
            1e-14,
        )

    def test_continuum_limit_is_type_i_not_type_ii(self):
        record = continuum_limit_record()
        self.assertIn("Type I_infinity", record["full_corner_strong_closure"])
        self.assertIn("Type-II", record["typeii_obstruction"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            physical_basis_labels(0)
        with self.assertRaises(ValueError):
            time_reference_expectation(1, identity_matrix(2))
        with self.assertRaises(ValueError):
            within_block_phase_pair(2, ell=0)
        with self.assertRaises(ValueError):
            recovery_no_go_record(2, screen_distance=2.0)
        with self.assertRaises(ValueError):
            gaussian_edge_smearing(1, identity_matrix(4), sigma=-1.0)
        with self.assertRaises(ValueError):
            maximum_sigma_for_visibility(1, visibility=1.0)
        with self.assertRaises(ValueError):
            relational_observer_constraint_certificate(max_level=0)


if __name__ == "__main__":
    unittest.main()
