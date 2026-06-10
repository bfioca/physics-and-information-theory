import unittest
from itertools import product
from math import exp

from qgtoy.fuzzy_berezin import berezin_state_lift
from qgtoy.fuzzy_algebra_inference import (
    CANDIDATE_CHANNELS,
    DEPHASING_CHANNEL,
    DEPOLARIZING_CHANNEL,
    FULL_CHANNEL,
    classify_response_signature,
    coherence_state_pair,
    coordinate_probe_state_pair,
    coordinate_response_formula,
    coordinate_screen_witness,
    correctable_algebra_record,
    direction_observable,
    fuzzy_algebra_inference_certificate,
    fuzzy_algebra_inference_record,
    ideal_response_signatures,
    observer_channel,
    population_state_pair,
    response_transport_record,
    samples_per_probe_state,
    signature_separation,
    signed_outcome_witness,
    witness_response,
)
from qgtoy.fuzzy_screen import coherent_screen_povm, measurement_probabilities
from qgtoy.fuzzy_sphere import matrix_unit


class FuzzyAlgebraInferenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = fuzzy_algebra_inference_certificate(max_level=5)

    def test_certificate_passes_with_finite_atlas_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertEqual(
            self.certificate["result_type"],
            "finite_declared_atlas_identification_theorem",
        )
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertIn("three-channel atlas", self.certificate["claim_boundary"])

    def test_channels_have_the_expected_fixed_algebras(self):
        dimension = 4
        off_diagonal = matrix_unit(dimension, 0, dimension - 1)
        diagonal = matrix_unit(dimension, 1, 1)
        self.assertEqual(observer_channel(FULL_CHANNEL, off_diagonal), off_diagonal)
        self.assertNotEqual(observer_channel(DEPHASING_CHANNEL, off_diagonal), off_diagonal)
        self.assertEqual(observer_channel(DEPHASING_CHANNEL, diagonal), diagonal)
        self.assertNotEqual(observer_channel(DEPOLARIZING_CHANNEL, diagonal), diagonal)

        expected_dimensions = {
            FULL_CHANNEL: dimension**2,
            DEPHASING_CHANNEL: dimension,
            DEPOLARIZING_CHANNEL: 1,
        }
        for channel in CANDIDATE_CHANNELS:
            record = correctable_algebra_record(dimension - 1, channel)
            self.assertEqual(
                record["correctable_algebra_dimension"], expected_dimensions[channel]
            )
            self.assertAlmostEqual(record["max_basis_recovery_error"], 0.0)

    def test_two_probe_signatures_resolve_all_three_models(self):
        for level in range(1, 6):
            signatures = ideal_response_signatures(level)
            full = signatures[FULL_CHANNEL]
            dephasing = signatures[DEPHASING_CHANNEL]
            depolarizing = signatures[DEPOLARIZING_CHANNEL]
            self.assertGreater(full[0], 0.0)
            self.assertGreater(full[1], 0.0)
            self.assertAlmostEqual(dephasing[0], full[0])
            self.assertAlmostEqual(dephasing[1], 0.0)
            self.assertAlmostEqual(depolarizing[0], 0.0)
            self.assertAlmostEqual(depolarizing[1], 0.0)
            self.assertGreater(signature_separation(level), 0.0)
            self.assertAlmostEqual(full[0], coordinate_response_formula(level))
            self.assertAlmostEqual(full[1], coordinate_response_formula(level))

    def test_coordinate_probes_are_low_mode_density_matrices(self):
        for level in range(1, 6):
            for axis in ("x", "y", "z"):
                plus, minus = coordinate_probe_state_pair(level, axis)
                self.assertAlmostEqual(sum(plus[index][index].real for index in range(level + 1)), 1.0)
                self.assertAlmostEqual(sum(minus[index][index].real for index in range(level + 1)), 1.0)
            self.assertEqual(population_state_pair(level), coordinate_probe_state_pair(level, "z"))
            self.assertEqual(coherence_state_pair(level), coordinate_probe_state_pair(level, "x"))
            for axis in ("x", "y", "z"):
                observable = direction_observable(level, axis)
                self.assertLessEqual(
                    max(abs(observable[row][column]) for row in range(level + 1) for column in range(level + 1)),
                    1.0 + 1e-12,
                )

    def test_coordinate_witnesses_are_bounded_and_exact(self):
        for level in range(1, 6):
            for axis in ("x", "z"):
                witness = coordinate_screen_witness(level, axis)
                self.assertLessEqual(max(abs(value) for value in witness), 1.0 + 1e-12)
            signatures = ideal_response_signatures(level)
            self.assertAlmostEqual(
                signatures[FULL_CHANNEL][0], coordinate_response_formula(level)
            )

    def test_response_and_witness_transport_have_inverse_cutoff_bounds(self):
        for source in range(1, 10):
            record = response_transport_record(source, source + 1)
            self.assertAlmostEqual(record["local_response_transport_error"], 0.0)
            self.assertLessEqual(
                record["lifted_state_response_error"],
                record["lifted_state_response_error_upper_bound"] + 1e-14,
            )
            self.assertLessEqual(
                record["witness_hilbert_schmidt_transport_error"],
                record["witness_error_upper_bound"] + 1e-14,
            )
            self.assertGreaterEqual(
                record["source_response"], record["uniform_response_lower_bound"]
            )

    def test_cptp_state_lift_realizes_the_predicted_response(self):
        for source in range(1, 5):
            target = source + 2
            plus, minus = coordinate_probe_state_pair(source, "x")
            lifted_plus = berezin_state_lift(source, target, plus)
            lifted_minus = berezin_state_lift(source, target, minus)
            effects = coherent_screen_povm(target)
            witness = coordinate_screen_witness(target, "x", effects)
            response = witness_response(
                measurement_probabilities(lifted_plus, effects),
                measurement_probabilities(lifted_minus, effects),
                witness,
            )
            record = response_transport_record(source, target)
            self.assertAlmostEqual(
                response, record["lifted_state_target_response"], places=11
            )

    def test_classifier_is_robust_at_all_error_box_corners(self):
        for level in range(1, 5):
            signatures = ideal_response_signatures(level)
            radius = signature_separation(level) / 4.0
            for channel, signature in signatures.items():
                for signs in product((-1.0, 1.0), repeat=2):
                    observed = tuple(
                        signature[axis] + signs[axis] * radius for axis in range(2)
                    )
                    result = classify_response_signature(
                        level,
                        observed[0],
                        observed[1],
                        response_error_bound=radius,
                    )
                    self.assertEqual(result["classification"], channel)

    def test_overlapping_error_balls_return_ambiguous(self):
        level = 3
        signatures = ideal_response_signatures(level)
        left = signatures[FULL_CHANNEL]
        right = signatures[DEPHASING_CHANNEL]
        midpoint = tuple((left[index] + right[index]) / 2.0 for index in range(2))
        result = classify_response_signature(
            level,
            midpoint[0],
            midpoint[1],
            response_error_bound=signature_separation(level) / 2.0,
        )
        self.assertEqual(result["classification"], "ambiguous")
        self.assertGreaterEqual(len(result["feasible_candidates"]), 2)

    def test_fixed_sign_witness_returns_reference_total_variation(self):
        left = (0.6, 0.1, 0.3)
        right = (0.2, 0.5, 0.3)
        witness = signed_outcome_witness(left, right)
        self.assertEqual(witness, (1.0, -1.0, 0.0))
        self.assertAlmostEqual(witness_response(left, right, witness), 0.4)

    def test_sample_budget_and_record(self):
        epsilon = 0.1
        delta = 0.05
        samples = samples_per_probe_state(epsilon, delta)
        self.assertGreater(samples, 0)
        self.assertLessEqual(8.0 * exp(-samples * epsilon**2 / 2.0), delta)
        record = fuzzy_algebra_inference_record(2, failure_probability=delta)
        self.assertLessEqual(record["hoeffding_failure_upper_bound"], delta)
        self.assertEqual(record["total_samples_four_states"], 4 * record["samples_per_probe_state"])

    def test_coherence_pair_is_destroyed_by_dephasing(self):
        plus, minus = coherence_state_pair(3)
        self.assertEqual(
            observer_channel(DEPHASING_CHANNEL, plus),
            observer_channel(DEPHASING_CHANNEL, minus),
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            coherence_state_pair(0)
        with self.assertRaises(ValueError):
            coordinate_probe_state_pair(1, "not-an-axis")
        with self.assertRaises(ValueError):
            direction_observable(1, "not-an-axis")
        with self.assertRaises(ValueError):
            coordinate_screen_witness(1, "not-an-axis")
        with self.assertRaises(ValueError):
            response_transport_record(2, 1)
        with self.assertRaises(ValueError):
            observer_channel("not-a-channel", matrix_unit(2, 0, 0))
        with self.assertRaises(ValueError):
            signed_outcome_witness((1.0,), (0.5, 0.5))
        with self.assertRaises(ValueError):
            witness_response((1.0,), (1.0,), (1.0, -1.0))
        with self.assertRaises(ValueError):
            classify_response_signature(1, 0.0, 0.0, response_error_bound=-1.0)
        with self.assertRaises(ValueError):
            samples_per_probe_state(0.0, 0.05)
        with self.assertRaises(ValueError):
            samples_per_probe_state(0.1, 1.0)
        with self.assertRaises(ValueError):
            fuzzy_algebra_inference_certificate(max_level=0)


if __name__ == "__main__":
    unittest.main()
