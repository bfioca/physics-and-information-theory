import unittest
from math import log, sin

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_pseudoscalar_gyroscope import (
    optical_gradient_from_improved_physical_components,
    proper_time_bath_correlation_time,
    proper_time_zero_frequency_spectrum,
    pseudoscalar_gyroscope_record,
    pseudoscalar_markov_parameter,
    static_lapse_from_horizon_distance,
    static_patch_pseudoscalar_gyroscope_certificate,
)


class StaticPatchPseudoscalarGyroscopeTest(unittest.TestCase):
    def test_exact_lapse(self):
        self.assertAlmostEqual(
            static_lapse_from_horizon_distance(0.2, radius=2.0),
            sin(0.1),
        )

    def test_acceleration_improved_conformal_identity(self):
        lapse = 0.2
        optical = optical_gradient_from_improved_physical_components(
            lapse,
            physical_gradient_component=30.0,
            acceleration_component=-2.0,
            physical_field_value=2.5,
        )
        self.assertAlmostEqual(optical, 1.0)

    def test_proper_spectral_scaling(self):
        lapse = 0.1
        self.assertAlmostEqual(
            proper_time_zero_frequency_spectrum(
                lapse,
                optical_zero_frequency_spectrum=2.0,
            ),
            2000.0,
        )
        self.assertAlmostEqual(
            proper_time_bath_correlation_time(
                lapse,
                optical_correlation_time=3.0,
            ),
            0.3,
        )
        self.assertAlmostEqual(
            pseudoscalar_markov_parameter(
                lapse,
                coupling=0.01,
                optical_zero_frequency_spectrum=2.0,
                optical_correlation_time=3.0,
            ),
            0.06,
        )

    def test_reference_state_interaction_rms_scalings(self):
        record = pseudoscalar_gyroscope_record(
            32,
            horizon_distance=1.0 / 65.0,
        )
        lapse = record["static_lapse_N"]
        casimir = record["system_casimir_load_L_L_plus_1"]
        self.assertAlmostEqual(
            record["coupling_at_reference_state_interaction_rms_budget"],
            lapse**2 / casimir**0.5,
        )
        self.assertAlmostEqual(
            record["diffusion_rate_at_reference_state_rms_budget"],
            lapse / casimir,
        )
        self.assertAlmostEqual(
            record["proper_time_for_chosen_logarithmic_schedule_at_rms_budget"],
            0.5 * log(65.0) * casimir / lapse,
        )

    def test_certificate(self):
        certificate = static_patch_pseudoscalar_gyroscope_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("d^3 log d", certificate["scaling_consequence"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-pseudoscalar-gyroscope"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.fixed_coupling, 0.01)

    def test_validation(self):
        with self.assertRaises(ValueError):
            static_lapse_from_horizon_distance(4.0, radius=1.0)
        with self.assertRaises(ValueError):
            static_patch_pseudoscalar_gyroscope_certificate(maximum_spin=16)


if __name__ == "__main__":
    unittest.main()
