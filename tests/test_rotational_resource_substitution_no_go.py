import unittest
from fractions import Fraction

from qgtoy.rotational_resource_substitution_no_go import (
    maximally_mixed_spin_record,
    rare_tail_qfi_record,
    rotational_resource_substitution_no_go_certificate,
    zero_mean_spin_cat_record,
)


class RotationalResourceSubstitutionNoGoTest(unittest.TestCase):
    def test_spin_cat_has_zero_mean_and_full_rank_qfi(self):
        record = zero_mean_spin_cat_record(4)
        self.assertEqual(record["spin_j"]["exact"], "2")
        self.assertTrue(
            all(axis["exact"] == "0" for axis in record["mean_angular_momentum"])
        )
        self.assertEqual(
            tuple(axis["exact"] for axis in record["covariance_diagonal"]),
            ("1", "1", "4"),
        )
        self.assertEqual(
            tuple(axis["exact"] for axis in record["rotational_qfi_diagonal"]),
            ("4", "4", "16"),
        )
        self.assertEqual(record["rotational_qfi_trace"]["exact"], "24")
        self.assertEqual(record["qfi_rank"], 3)

    def test_mixed_state_has_same_casimir_and_zero_qfi(self):
        cat = zero_mean_spin_cat_record(7)
        mixed = maximally_mixed_spin_record(7)
        self.assertEqual(
            cat["casimir_J_squared"]["exact"],
            mixed["casimir_J_squared"]["exact"],
        )
        self.assertEqual(mixed["rotational_qfi_trace"]["exact"], "0")
        self.assertEqual(mixed["qfi_rank"], 0)

    def test_certificate(self):
        certificate = rotational_resource_substitution_no_go_certificate(
            twice_spin=5,
            moment_of_inertia=Fraction(3, 2),
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("localized energy cost", certificate["required_proof_direction"])

    def test_rare_tail_has_fixed_mean_cost_and_divergent_qfi(self):
        traces = []
        distances = []
        for spin in (2, 8, 32, 128):
            record = rare_tail_qfi_record(spin)
            self.assertEqual(record["mean_linear_spin_cost"]["exact"], "1")
            self.assertEqual(record["rotational_qfi_trace"]["exact"], str(4 * (spin + 1)))
            traces.append(record["rotational_qfi_trace"]["value"])
            distances.append(record["trace_distance_to_invariant_spin_zero"])
        self.assertTrue(all(right > left for left, right in zip(traces, traces[1:])))
        self.assertTrue(
            all(right < left for left, right in zip(distances, distances[1:]))
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            zero_mean_spin_cat_record(2)
        with self.assertRaises(ValueError):
            maximally_mixed_spin_record(True)
        with self.assertRaises(ValueError):
            rare_tail_qfi_record(1)
        with self.assertRaises(ValueError):
            rotational_resource_substitution_no_go_certificate(
                moment_of_inertia=Fraction(0)
            )


if __name__ == "__main__":
    unittest.main()
