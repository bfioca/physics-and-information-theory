import unittest

from qgtoy.__main__ import build_parser
from qgtoy.common_mode_locality_mismatch import (
    axial_common_mode_mismatch_lower_bound,
    axial_relational_visibility,
    common_mode_locality_mismatch_certificate,
    finite_cell_covariance_distance_record,
    logarithmic_schedule_correlation_record,
    maximum_correlation_defect_for_mismatch,
    minimum_exponential_correlation_length,
)


class CommonModeLocalityMismatchTest(unittest.TestCase):
    def test_perfect_common_mode_is_decoherence_free(self):
        for time in (0.0, 1.0, 100.0):
            self.assertEqual(
                axial_relational_visibility(time, correlation=1.0),
                1.0,
            )
            self.assertEqual(
                axial_common_mode_mismatch_lower_bound(time, correlation=1.0),
                0.0,
            )

    def test_independent_noise_visibility(self):
        self.assertAlmostEqual(
            axial_relational_visibility(0.7, correlation=0.0),
            0.2465969639416065,
        )
        self.assertAlmostEqual(
            axial_relational_visibility(
                0.7,
                correlation=0.0,
                charge_gap=2.0,
            ),
            axial_relational_visibility(2.8, correlation=0.0),
        )

    def test_correlation_defect_inverts_witness_exactly(self):
        target = 0.03
        time = 2.5
        defect = maximum_correlation_defect_for_mismatch(
            target,
            dimensionless_time=time,
        )
        self.assertAlmostEqual(
            axial_common_mode_mismatch_lower_bound(
                time,
                correlation=1.0 - defect,
            ),
            target,
            places=14,
        )

    def test_logarithmic_schedule_forces_inverse_d_log_d_defect(self):
        records = tuple(
            logarithmic_schedule_correlation_record(dimension)
            for dimension in (16, 64, 256, 1024, 4096)
        )
        scaled = tuple(record["scaled_defect_d_log_d"] for record in records)
        self.assertTrue(all(2.0 <= value <= 2.3 for value in scaled))
        self.assertTrue(
            all(
                right < left
                for left, right in zip(
                    (record["maximum_correlation_defect_1_minus_c"] for record in records),
                    (record["maximum_correlation_defect_1_minus_c"] for record in records[1:]),
                )
            )
        )

    def test_exponential_correlation_length_requirement(self):
        length = minimum_exponential_correlation_length(
            3.0,
            target_mismatch=1.0 / 1024.0,
            dimensionless_time=0.5 * 6.931471805599453,
        )
        self.assertGreater(length, 1000.0)

    def test_finite_cell_duhamel_bound(self):
        record = finite_cell_covariance_distance_record(
            ((1.0, 0.99), (0.99, 1.0)),
            generator_norm_bounds=(1.0, 1.0),
            dimensionless_time=0.5,
            number_of_axes=1,
        )
        witness = axial_common_mode_mismatch_lower_bound(
            0.5,
            correlation=0.99,
        )
        self.assertGreaterEqual(
            record["normalized_channel_distance_upper_bound"],
            witness,
        )
        ideal = finite_cell_covariance_distance_record(
            ((1.0, 1.0), (1.0, 1.0)),
            generator_norm_bounds=(1.0, 1.0),
            dimensionless_time=10.0,
        )
        self.assertEqual(ideal["normalized_channel_distance_upper_bound"], 0.0)

    def test_certificate(self):
        certificate = common_mode_locality_mismatch_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("does not derive", certificate["claim_boundary"])
        self.assertEqual(
            common_mode_locality_mismatch_certificate(correlation=0.999)["status"],
            "pass",
        )
        self.assertEqual(
            common_mode_locality_mismatch_certificate(correlation=1.0)["status"],
            "pass",
        )

    def test_cli_defaults(self):
        args = build_parser().parse_args(["common-mode-locality-mismatch"])
        self.assertEqual(args.correlation, 0.95)
        self.assertEqual(args.maximum_dimension, 4096)
        self.assertEqual(args.mismatch_coefficient, 1.0)
        self.assertEqual(args.separation, 1.0)
        self.assertEqual(args.charge_gap, 1.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            axial_relational_visibility(1.0, correlation=1.1)
        with self.assertRaises(ValueError):
            maximum_correlation_defect_for_mismatch(
                0.5,
                dimensionless_time=1.0,
            )
        with self.assertRaises(ValueError):
            finite_cell_covariance_distance_record(
                ((1.0, 2.0), (2.0, 1.0)),
                generator_norm_bounds=(1.0, 1.0),
                dimensionless_time=1.0,
            )


if __name__ == "__main__":
    unittest.main()
