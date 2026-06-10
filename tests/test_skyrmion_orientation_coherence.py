import unittest

from qgtoy.skyrmion_orientation_coherence import (
    skyrmion_orientation_coherence_certificate,
    skyrmion_projective_heat_coherence_record,
)


class SkyrmionOrientationCoherenceTest(unittest.TestCase):
    def test_record_has_positive_matter_rate_and_ordered_risks(self):
        record = skyrmion_projective_heat_coherence_record(
            4,
            risk_budget=0.2,
            proper_protocol_time=0.5,
            coupling=1.0e-3,
            horizon_distance=0.2,
        )
        self.assertGreater(record["matter_optical_zero_frequency_spectrum"], 0.0)
        self.assertGreater(record["proper_orientation_diffusion_rate_gamma"], 0.0)
        self.assertGreaterEqual(
            record["global_risk_lower_bound_at_protocol_time"],
            record["initial_projective_global_risk_lower_bound"],
        )

    def test_certificate(self):
        certificate = skyrmion_orientation_coherence_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_validation(self):
        with self.assertRaises(ValueError):
            skyrmion_projective_heat_coherence_record(
                -1,
                risk_budget=0.1,
                proper_protocol_time=1.0,
                coupling=1.0e-3,
                horizon_distance=0.2,
            )
        with self.assertRaises(ValueError):
            skyrmion_projective_heat_coherence_record(
                2,
                risk_budget=0.8,
                proper_protocol_time=1.0,
                coupling=1.0e-3,
                horizon_distance=0.2,
            )


if __name__ == "__main__":
    unittest.main()
