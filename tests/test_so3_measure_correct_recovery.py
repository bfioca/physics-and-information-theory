import unittest

from qgtoy.so3_measure_correct_recovery import (
    necessary_orientation_risk_ceiling_for_recovery_error,
    spin1_measure_correct_error_bounds,
    spin1_measure_correct_recovery_certificate,
    sufficient_orientation_risk_for_recovery_error,
)


class SO3MeasureCorrectRecoveryTest(unittest.TestCase):
    def test_bounds_are_ordered(self):
        for index in range(101):
            risk = index / 100.0
            record = spin1_measure_correct_error_bounds(risk)
            self.assertLessEqual(
                record["normalized_diamond_error_lower_bound"],
                record["normalized_diamond_error_upper_bound"],
            )

    def test_sufficient_and_necessary_conversions(self):
        for error in (0.0, 0.01, 0.1, 0.5, 1.0):
            risk = sufficient_orientation_risk_for_recovery_error(error)
            bound = spin1_measure_correct_error_bounds(risk)
            self.assertLessEqual(
                bound["normalized_diamond_error_upper_bound"],
                error,
            )
            self.assertGreaterEqual(
                necessary_orientation_risk_ceiling_for_recovery_error(error),
                0.0,
            )

    def test_certificate(self):
        certificate = spin1_measure_correct_recovery_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_validation(self):
        with self.assertRaises(ValueError):
            spin1_measure_correct_error_bounds(-0.1)
        with self.assertRaises(ValueError):
            sufficient_orientation_risk_for_recovery_error(1.1)
        with self.assertRaises(ValueError):
            necessary_orientation_risk_ceiling_for_recovery_error(float("nan"))


if __name__ == "__main__":
    unittest.main()
