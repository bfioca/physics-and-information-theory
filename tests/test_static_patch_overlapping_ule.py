import unittest
from math import exp, log, pi, sqrt

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_overlapping_ule import (
    all_decoder_recovery_error_lower_bound_from_spectral_residual,
    collective_kossakowski_coefficient,
    collective_lamb_shift_coefficient,
    collective_jump_prefactor,
    decoder_witness_trace_norm,
    heat_scale_matching_ule_residual_coupling_cap,
    logarithmic_heat_to_haar_distance_bound,
    numerical_collective_lamb_shift_coefficient,
    rank_one_return_probability_upper_bound,
    rank_one_return_initial_decay_rate_lower_bound,
    smeared_gradient_spectrum,
    static_patch_overlapping_ule_certificate,
    sufficient_ule_residual_coupling_cap,
)


class StaticPatchOverlappingULETest(unittest.TestCase):
    def test_kms_relation(self):
        frequency = 0.8
        positive = smeared_gradient_spectrum(frequency)
        negative = smeared_gradient_spectrum(-frequency)
        self.assertAlmostEqual(
            negative / positive,
            exp(-2.0 * pi * frequency),
        )

    def test_zero_frequency_limit(self):
        at_zero = smeared_gradient_spectrum(0.0)
        near_zero = smeared_gradient_spectrum(1.0e-8)
        self.assertAlmostEqual(near_zero / at_zero, 1.0, places=7)

    def test_lamb_shift_closed_form(self):
        analytic = collective_lamb_shift_coefficient()
        numeric = numerical_collective_lamb_shift_coefficient(steps=4000)
        self.assertAlmostEqual(numeric / analytic, 1.0, places=11)

    def test_jump_and_kossakowski_normalization(self):
        jump = collective_jump_prefactor(0.3, 0.2)
        coefficient = collective_kossakowski_coefficient(0.3, 0.2)
        self.assertAlmostEqual(jump * jump, coefficient)

    def test_conditional_coupling_scaling(self):
        spin = 4096
        dimension = 2 * spin + 1
        cap = sufficient_ule_residual_coupling_cap(spin, 1.0 / dimension)
        scaled = cap * dimension**3.5 * sqrt(log(dimension))
        self.assertAlmostEqual(scaled, 4.0, places=2)

    def test_non_dark_return_and_decoder_norm_boundary(self):
        for spin in (2, 10, 100, 1000):
            dimension = 2 * spin + 1
            self.assertLess(
                rank_one_return_probability_upper_bound(spin),
                3.0 / dimension,
            )
            self.assertEqual(
                rank_one_return_initial_decay_rate_lower_bound(spin),
                2.0 * spin * (spin + 2.0),
            )
            self.assertEqual(decoder_witness_trace_norm(spin), float(dimension))
            residual = 1.0 / (4.0 * dimension)
            self.assertGreater(
                all_decoder_recovery_error_lower_bound_from_spectral_residual(
                    spin,
                    residual,
                ),
                0.0,
            )

    def test_heat_scale_matching_cap_is_d_minus_four(self):
        spin = 4096
        dimension = 2 * spin + 1
        cap = heat_scale_matching_ule_residual_coupling_cap(
            spin,
            1.0 / dimension,
        )
        scaled = cap * dimension**4 * sqrt(log(dimension))
        self.assertAlmostEqual(scaled, 4.0, places=2)

    def test_logarithmic_heat_bound_is_inverse_dimension(self):
        for spin in (2, 10, 100):
            dimension = 2 * spin + 1
            self.assertLess(
                logarithmic_heat_to_haar_distance_bound(spin),
                2.0 / dimension,
            )

    def test_certificate(self):
        certificate = static_patch_overlapping_ule_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-overlapping-ule"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.radius, 1.0)
        self.assertEqual(args.smearing_width, 0.2)

    def test_validation(self):
        with self.assertRaises(ValueError):
            smeared_gradient_spectrum(1.0, smearing_width=0.0)
        with self.assertRaises(ValueError):
            numerical_collective_lamb_shift_coefficient(steps=3)
        with self.assertRaises(ValueError):
            sufficient_ule_residual_coupling_cap(0, 1.0)


if __name__ == "__main__":
    unittest.main()
