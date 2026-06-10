import unittest
from math import sqrt

from qgtoy.fuzzy_screen import (
    coherent_screen_decision_record,
    coherent_screen_experiment_certificate,
    coherent_screen_povm,
    coherent_symbol,
    gauss_legendre_rule,
    measurement_probabilities,
    pole_state_pair,
    povm_normalization_error,
    povm_span_rank,
    spin_coherent_vector,
    total_variation_distance,
)
from qgtoy.fuzzy_sphere import fuzzy_coordinates
from qgtoy.quantum_channel import identity_matrix


class FuzzyScreenExperimentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = coherent_screen_experiment_certificate(max_level=5)

    def test_certificate_passes_from_operational_quantities(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertEqual(
            self.certificate["result_type"],
            "finite_quantum_statistical_screen_deficiency_witness",
        )
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_gauss_legendre_rule_integrates_low_polynomials(self):
        rule = gauss_legendre_rule(4)
        self.assertAlmostEqual(sum(weight for _node, weight in rule), 2.0)
        self.assertAlmostEqual(
            sum(weight * node**6 for node, weight in rule),
            2.0 / 7.0,
            places=13,
        )

    def test_coherent_vectors_are_normalized_and_symbols_track_poles(self):
        level = 3
        north = spin_coherent_vector(level, cosine_theta=1.0, phi=0.0)
        south = spin_coherent_vector(level, cosine_theta=-1.0, phi=0.0)
        self.assertAlmostEqual(sum(abs(value) ** 2 for value in north), 1.0)
        self.assertAlmostEqual(sum(abs(value) ** 2 for value in south), 1.0)
        z_coordinate = fuzzy_coordinates(level)[2]
        pole_value = sqrt((level / 2.0) / (level / 2.0 + 1.0))
        self.assertAlmostEqual(
            coherent_symbol(
                level, z_coordinate, cosine_theta=1.0, phi=0.0
            ).real,
            pole_value,
        )
        self.assertAlmostEqual(
            coherent_symbol(
                level, z_coordinate, cosine_theta=-1.0, phi=0.0
            ).real,
            -pole_value,
        )

    def test_povm_is_normalized_and_informationally_complete(self):
        for level in range(1, 5):
            effects = coherent_screen_povm(level)
            self.assertLess(povm_normalization_error(effects), 1e-10)
            self.assertEqual(povm_span_rank(effects), (level + 1) ** 2)

    def test_measurement_distributions_and_decision_gap(self):
        record = coherent_screen_decision_record(3)
        self.assertLess(record["povm_normalization_error"], 1e-10)
        self.assertTrue(record["informationally_complete_linear_span"])
        self.assertGreater(record["screen_total_variation_distance"], 0.0)
        self.assertLess(record["screen_total_variation_distance"], 1.0)
        self.assertGreater(record["single_copy_decision_gap"], 0.0)
        self.assertAlmostEqual(
            record["worst_case_reconstruction_error_lower_bound"],
            record["single_copy_decision_gap"],
        )

    def test_probability_helpers(self):
        effects = coherent_screen_povm(2)
        north, south = pole_state_pair(2)
        north_probabilities = measurement_probabilities(north, effects)
        south_probabilities = measurement_probabilities(south, effects)
        self.assertAlmostEqual(sum(north_probabilities), 1.0)
        self.assertAlmostEqual(sum(south_probabilities), 1.0)
        self.assertGreater(
            total_variation_distance(north_probabilities, south_probabilities),
            0.0,
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            coherent_screen_povm(0)
        with self.assertRaises(ValueError):
            gauss_legendre_rule(0)
        with self.assertRaises(ValueError):
            spin_coherent_vector(1, cosine_theta=2.0, phi=0.0)
        with self.assertRaises(ValueError):
            coherent_screen_experiment_certificate(max_level=0)
        with self.assertRaises(ValueError):
            coherent_screen_experiment_certificate(tolerance=0.0)
        with self.assertRaises(ValueError):
            measurement_probabilities(identity_matrix(2), ())
        with self.assertRaises(ValueError):
            total_variation_distance((1.0,), (0.5, 0.5))


if __name__ == "__main__":
    unittest.main()
