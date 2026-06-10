import unittest
from math import exp, log, pi

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_overlapping_ule import (
    smeared_gradient_zero_frequency_spectrum,
)
from qgtoy.static_patch_worldtube_ule import (
    ancilla_stable_ule_spectral_residual_bound,
    compact_ball_spherical_multiplier,
    compact_ball_uv_envelope_constant,
    compact_worldtube_amplitude_multiplier,
    compact_worldtube_gradient_spectrum,
    compact_worldtube_lamb_shift_coefficient,
    compact_worldtube_lamb_tail_bound,
    gaussian_compact_support_growth_gap,
    logarithmic_heat_ule_coupling_cap,
    logarithmic_heat_ule_residual_bound,
    numerical_compact_ball_spherical_multiplier,
    numerical_shifted_hyperbolic_heat_multiplier,
    optimal_sobolev_jump_correlator_moment_bounds,
    shifted_hyperbolic_heat_multiplier,
    shifted_hyperbolic_heat_profile,
    sobolev_jump_correlator_moment_bounds,
    static_patch_worldtube_ule_certificate,
    three_channel_ule_parameters,
)


class StaticPatchWorldtubeULETest(unittest.TestCase):
    def test_heat_kernel_reproduces_gaussian_spectral_factor(self):
        frequency = 1.3
        width = 0.27
        amplitude = shifted_hyperbolic_heat_multiplier(
            frequency,
            smearing_width=width,
        )
        self.assertAlmostEqual(
            amplitude * amplitude,
            exp(-(width * frequency) ** 2),
        )
        self.assertAlmostEqual(
            numerical_shifted_hyperbolic_heat_multiplier(
                frequency,
                smearing_width=width,
            ),
            amplitude,
            places=11,
        )
        self.assertGreater(shifted_hyperbolic_heat_profile(0.0), 0.0)
        self.assertGreater(shifted_hyperbolic_heat_profile(1.0), 0.0)

    def test_compact_multiplier_normalization_and_evenness(self):
        self.assertEqual(compact_ball_spherical_multiplier(0.0), 1.0)
        for value in (1.0e-6, 0.3, 2.0, 17.0):
            self.assertAlmostEqual(
                compact_ball_spherical_multiplier(value),
                compact_ball_spherical_multiplier(-value),
            )
        self.assertAlmostEqual(
            compact_ball_spherical_multiplier(1.0e-6),
            compact_ball_spherical_multiplier(1.0e-5),
            places=8,
        )
        for value in (0.0, 0.3, 2.0):
            self.assertAlmostEqual(
                compact_ball_spherical_multiplier(value),
                numerical_compact_ball_spherical_multiplier(value),
                places=12,
            )
        for ratio in (1.0e-3, 1.0e-6, 1.0e-10):
            self.assertAlmostEqual(
                compact_ball_spherical_multiplier(
                    1.0,
                    support_radius_ratio=ratio,
                ),
                1.0,
                places=6,
            )

    def test_compact_spectrum_kms_and_zero_mode(self):
        frequency = 0.8
        positive = compact_worldtube_gradient_spectrum(frequency)
        negative = compact_worldtube_gradient_spectrum(-frequency)
        self.assertAlmostEqual(
            negative / positive,
            exp(-2.0 * pi * frequency),
        )
        self.assertEqual(
            compact_worldtube_gradient_spectrum(0.0),
            smeared_gradient_zero_frequency_spectrum(),
        )

    def test_double_ball_uv_envelope(self):
        ratio = 0.2
        envelope = compact_ball_uv_envelope_constant(
            support_radius_ratio=ratio
        )
        for spectral_parameter in (1.0, 5.0, 20.0, 100.0):
            q_value = abs(
                compact_ball_spherical_multiplier(
                    spectral_parameter,
                    support_radius_ratio=ratio,
                )
            )
            self.assertLessEqual(
                q_value,
                envelope / spectral_parameter**2,
            )
            amplitude = compact_worldtube_amplitude_multiplier(
                spectral_parameter,
                support_radius=ratio,
            )
            self.assertAlmostEqual(amplitude, q_value * q_value)

    def test_compact_lamb_shift_and_tail(self):
        coarse_step = compact_worldtube_lamb_shift_coefficient(
            upper_spectral_parameter=500.0,
            steps=10_000,
        )
        fine_step = compact_worldtube_lamb_shift_coefficient(
            upper_spectral_parameter=500.0,
            steps=20_000,
        )
        wider = compact_worldtube_lamb_shift_coefficient(
            upper_spectral_parameter=1000.0,
            steps=20_000,
        )
        tail = compact_worldtube_lamb_tail_bound(
            lower_spectral_parameter=1000.0,
        )
        self.assertLess(wider, 0.0)
        self.assertLess(abs(fine_step - coarse_step), 2.0e-8)
        self.assertLess(abs(wider - fine_step), 2.0e-5)
        self.assertLess(tail, 2.0e-7)

    def test_gaussian_is_not_of_fixed_exponential_type(self):
        small = gaussian_compact_support_growth_gap(10.0)
        large = gaussian_compact_support_growth_gap(200.0)
        self.assertGreater(large, small)
        self.assertGreater(large, 0.0)

    def test_sobolev_moment_bounds(self):
        g_bound, first_moment_bound = sobolev_jump_correlator_moment_bounds(
            2.0,
            0.5,
            0.25,
            time_scale=3.0,
        )
        self.assertGreater(g_bound, 0.0)
        self.assertGreater(first_moment_bound, 0.0)
        optimized = optimal_sobolev_jump_correlator_moment_bounds(
            2.0,
            0.5,
            0.25,
        )
        self.assertLess(optimized[0], g_bound)
        self.assertLess(optimized[1], first_moment_bound)

    def test_three_channel_parameter_and_residual_constants(self):
        spin = 5
        lapse = 0.2
        coupling = 0.01
        jump_l1 = 2.0
        first_moment = 0.6
        gamma, tau = three_channel_ule_parameters(
            spin,
            lapse,
            coupling,
            jump_l1,
            first_moment,
        )
        self.assertAlmostEqual(
            gamma,
            144.0 * coupling**2 * spin**2 * jump_l1**2 / lapse**2,
        )
        self.assertAlmostEqual(tau, first_moment / jump_l1)
        elapsed = 0.7
        residual = ancilla_stable_ule_spectral_residual_bound(
            spin,
            lapse,
            coupling,
            elapsed,
            jump_l1,
            first_moment,
        )
        self.assertAlmostEqual(
            residual,
            2.0 * gamma * tau + 2.0 * gamma**2 * tau * elapsed,
        )

    def test_logarithmic_cap_saturates_declared_budget(self):
        spin = 100
        dimension = 2 * spin + 1
        lapse = 1.0 / dimension
        budget = 1.0 / (4.0 * dimension)
        jump_l1 = 3.0
        first_moment = 1.0
        cap = logarithmic_heat_ule_coupling_cap(
            spin,
            lapse,
            budget,
            jump_l1,
            first_moment,
        )
        self.assertAlmostEqual(
            logarithmic_heat_ule_residual_bound(
                spin,
                lapse,
                cap,
                jump_l1,
                first_moment,
            ),
            budget,
        )

    def test_certificate_and_cli(self):
        certificate = static_patch_worldtube_ule_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        args = build_parser().parse_args(["static-patch-worldtube-ule"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.radius, 1.0)
        self.assertEqual(args.support_radius, 0.2)

    def test_validation(self):
        with self.assertRaises(ValueError):
            shifted_hyperbolic_heat_profile(-1.0)
        with self.assertRaises(ValueError):
            compact_ball_spherical_multiplier(1.0, support_radius_ratio=0.0)
        with self.assertRaises(ValueError):
            compact_worldtube_lamb_shift_coefficient(steps=3)
        with self.assertRaises(ValueError):
            logarithmic_heat_ule_coupling_cap(0, 1.0, 1.0, 1.0, 1.0)
        with self.assertRaises(ValueError):
            ancilla_stable_ule_spectral_residual_bound(
                1,
                0.0,
                1.0,
                1.0,
                1.0,
                1.0,
            )
        with self.assertRaises(ValueError):
            ancilla_stable_ule_spectral_residual_bound(
                1,
                1.0,
                1.0,
                1.0,
                -1.0,
                1.0,
            )
        with self.assertRaises(ValueError):
            static_patch_worldtube_ule_certificate(support_radius=21.0)


if __name__ == "__main__":
    unittest.main()
