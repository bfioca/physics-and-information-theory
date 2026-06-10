import unittest
from math import sqrt

from qgtoy.modular_manybody_regulator import (
    finite_manybody_record,
    manybody_limit_record,
    modular_manybody_regulator_certificate,
    modular_ratio_group_record,
    site_gap,
    site_gibbs_weights,
)


class ModularManybodyRegulatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = modular_manybody_regulator_certificate(max_sites=8)

    def test_certificate_passes_with_thermal_surrogate_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["finite_verified_claims"].values()))
        self.assertTrue(
            all(self.certificate["theorem_backed_limit_claims"].values())
        )
        self.assertIn("classification theorems", self.certificate["evidence_scope"])
        self.assertIn("many-body thermal", self.certificate["claim_boundary"])

    def test_alternating_incommensurate_site_gaps(self):
        self.assertEqual(site_gap(1), 1.0)
        self.assertEqual(site_gap(2), sqrt(2.0))
        self.assertEqual(site_gap(3), 1.0)
        ratio = modular_ratio_group_record()
        self.assertTrue(ratio["additive_group_dense_in_R"])
        self.assertTrue(ratio["multiplicative_group_dense_in_positive_reals"])

    def test_site_states_are_faithful_and_normalized(self):
        for site in range(1, 8):
            weights = site_gibbs_weights(site)
            self.assertAlmostEqual(sum(weights), 1.0)
            self.assertGreater(min(weights), 0.0)

    def test_finite_regulator_has_canonical_exact_structure(self):
        for sites in range(1, 8):
            record = finite_manybody_record(sites)
            self.assertEqual(record["hilbert_dimension"], 2**sites)
            self.assertEqual(record["matrix_algebra_vector_dimension"], 4**sites)
            self.assertEqual(record["state_embedding_error"], 0.0)
            self.assertEqual(record["embedding_modular_covariance_error"], 0.0)
            self.assertEqual(record["expectation_modular_covariance_error"], 0.0)
            self.assertLess(record["site_state_normalization_error"], 1e-15)
            self.assertEqual(record["finite_von_neumann_type"], "Type I finite")

    def test_limit_type_and_core_follow_from_state_structure(self):
        record = manybody_limit_record()
        self.assertIn("Type III_1", record["gns_von_neumann_algebra"])
        self.assertIn("Type II_infinity", record["continuous_core"])
        self.assertTrue(record["core_has_faithful_normal_semifinite_trace"])
        self.assertIn("semifinite core trace", record["core_trace"])
        self.assertIn("pointwise outer", record["modular_flow"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            site_gap(0)
        with self.assertRaises(ValueError):
            site_gibbs_weights(1, beta=0.0)
        with self.assertRaises(ValueError):
            finite_manybody_record(0)
        with self.assertRaises(ValueError):
            modular_ratio_group_record(beta=0.0)
        with self.assertRaises(ValueError):
            modular_manybody_regulator_certificate(max_sites=1)


if __name__ == "__main__":
    unittest.main()
