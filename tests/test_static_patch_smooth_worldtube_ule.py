import unittest
from fractions import Fraction
from math import exp, pi

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_smooth_worldtube_ule import (
    bare_sqrt_spectrum_derivatives,
    smooth_compact_seed_shape,
    smooth_seed_spherical_transform_derivatives,
    smooth_worldtube_amplitude_multiplier,
    smooth_worldtube_analytic_sobolev_upper_bounds,
    smooth_worldtube_gradient_spectrum,
    smooth_worldtube_moment_record,
    smooth_worldtube_sobolev_norms,
    smooth_worldtube_sqrt_spectrum_derivatives,
    smooth_seed_transform_tail_envelope,
    static_patch_smooth_worldtube_ule_certificate,
)


class StaticPatchSmoothWorldtubeULETest(unittest.TestCase):
    def test_seed_is_compact_and_flat(self):
        self.assertEqual(smooth_compact_seed_shape(0.0), 1.0)
        self.assertGreater(smooth_compact_seed_shape(0.5), 0.0)
        self.assertEqual(smooth_compact_seed_shape(1.0), 0.0)
        self.assertEqual(smooth_compact_seed_shape(2.0), 0.0)

    def test_spherical_transform_normalization_and_evenness(self):
        at_zero = smooth_seed_spherical_transform_derivatives(0.0)
        self.assertAlmostEqual(at_zero[0], 1.0)
        self.assertAlmostEqual(at_zero[1], 0.0)
        positive = smooth_seed_spherical_transform_derivatives(1.7)
        negative = smooth_seed_spherical_transform_derivatives(-1.7)
        self.assertAlmostEqual(positive[0], negative[0])
        self.assertAlmostEqual(positive[1], -negative[1])
        self.assertAlmostEqual(positive[2], negative[2])

    def test_transform_derivatives_match_finite_differences(self):
        spectral_parameter = 1.7
        spacing = 1.0e-4
        value, first, second = smooth_seed_spherical_transform_derivatives(
            spectral_parameter
        )
        plus = smooth_seed_spherical_transform_derivatives(
            spectral_parameter + spacing
        )[0]
        minus = smooth_seed_spherical_transform_derivatives(
            spectral_parameter - spacing
        )[0]
        self.assertAlmostEqual(
            first,
            (plus - minus) / (2.0 * spacing),
            places=8,
        )
        self.assertAlmostEqual(
            second,
            (plus - 2.0 * value + minus) / spacing**2,
            places=6,
        )

    def test_five_point_derivative_check_is_stable_at_support_boundaries(self):
        spectral_parameter = 1.7
        spacing = 1.0e-2
        for support_ratio in (0.1, 0.25):
            value, first, second = smooth_seed_spherical_transform_derivatives(
                spectral_parameter,
                support_radius_ratio=support_ratio,
            )
            minus_two = smooth_seed_spherical_transform_derivatives(
                spectral_parameter - 2.0 * spacing,
                support_radius_ratio=support_ratio,
            )[0]
            minus = smooth_seed_spherical_transform_derivatives(
                spectral_parameter - spacing,
                support_radius_ratio=support_ratio,
            )[0]
            plus = smooth_seed_spherical_transform_derivatives(
                spectral_parameter + spacing,
                support_radius_ratio=support_ratio,
            )[0]
            plus_two = smooth_seed_spherical_transform_derivatives(
                spectral_parameter + 2.0 * spacing,
                support_radius_ratio=support_ratio,
            )[0]
            finite_first = (
                minus_two - 8.0 * minus + 8.0 * plus - plus_two
            ) / (12.0 * spacing)
            finite_second = (
                -plus_two
                + 16.0 * plus
                - 30.0 * value
                + 16.0 * minus
                - minus_two
            ) / (12.0 * spacing**2)
            self.assertAlmostEqual(first, finite_first, places=10)
            self.assertAlmostEqual(second, finite_second, places=8)

    def test_bare_spectrum_derivatives_match_finite_differences(self):
        frequency = 0.8
        spacing = 1.0e-5
        root, first, second = bare_sqrt_spectrum_derivatives(frequency)
        plus = bare_sqrt_spectrum_derivatives(frequency + spacing)[0]
        minus = bare_sqrt_spectrum_derivatives(frequency - spacing)[0]
        self.assertAlmostEqual(
            first,
            (plus - minus) / (2.0 * spacing),
            places=8,
        )
        self.assertAlmostEqual(
            second,
            (plus - 2.0 * root + minus) / spacing**2,
            places=5,
        )
        zero = bare_sqrt_spectrum_derivatives(0.0)
        for near_zero in (1.0e-12, 1.0e-10, 1.0e-8, -1.0e-10):
            values = bare_sqrt_spectrum_derivatives(near_zero)
            self.assertAlmostEqual(values[2], zero[2], places=6)

    def test_regulated_spectrum_kms_and_amplitude(self):
        frequency = 0.7
        positive = smooth_worldtube_gradient_spectrum(frequency)
        negative = smooth_worldtube_gradient_spectrum(-frequency)
        self.assertAlmostEqual(
            negative / positive,
            exp(-2.0 * pi * frequency),
        )
        self.assertAlmostEqual(
            smooth_worldtube_gradient_spectrum(0.0),
            1.0 / (24.0 * pi**3),
        )
        transform = smooth_seed_spherical_transform_derivatives(frequency)[0]
        self.assertAlmostEqual(
            smooth_worldtube_amplitude_multiplier(frequency),
            transform * transform,
        )

    def test_regulated_sqrt_derivatives_match_finite_differences(self):
        frequency = 1.1
        spacing = 1.0e-4
        root, first, second = smooth_worldtube_sqrt_spectrum_derivatives(
            frequency
        )
        plus = smooth_worldtube_sqrt_spectrum_derivatives(
            frequency + spacing
        )[0]
        minus = smooth_worldtube_sqrt_spectrum_derivatives(
            frequency - spacing
        )[0]
        self.assertAlmostEqual(
            first,
            (plus - minus) / (2.0 * spacing),
            places=7,
        )
        self.assertAlmostEqual(
            second,
            (plus - 2.0 * root + minus) / spacing**2,
            places=5,
        )

    def test_sobolev_norm_refinement(self):
        coarse = smooth_worldtube_sobolev_norms(
            frequency_window=200.0,
            frequency_steps=800,
            radial_steps=100,
        )
        fine = smooth_worldtube_sobolev_norms(
            frequency_window=200.0,
            frequency_steps=1600,
            radial_steps=200,
        )
        for coarse_value, fine_value in zip(coarse, fine):
            self.assertGreater(fine_value, 0.0)
            self.assertLess(abs(fine_value / coarse_value - 1.0), 2.0e-4)

    def test_moment_record(self):
        record = smooth_worldtube_moment_record(
            frequency_window=200.0,
            frequency_steps=800,
            radial_steps=100,
        )
        self.assertGreater(record["jump_l1_sobolev_estimate"], 0.0)
        self.assertGreater(record["jump_first_moment_sobolev_estimate"], 0.0)

    def test_exact_profile_analytic_sobolev_enclosure(self):
        tail = smooth_seed_transform_tail_envelope()
        self.assertGreater(tail["transform_p_cubed_envelope"], 0.0)
        self.assertGreater(
            Fraction(tail["transform_p_cubed_envelope_exact"]),
            0,
        )
        enclosure = smooth_worldtube_analytic_sobolev_upper_bounds()
        self.assertEqual(enclosure["dimensionless_tail_split"], 160)
        self.assertTrue(enclosure["exact_integral_profile_enclosed"])
        self.assertFalse(
            enclosure["finite_simpson_transform_extrapolated_to_infinity"]
        )
        estimates = smooth_worldtube_sobolev_norms(
            frequency_window=200.0,
            frequency_steps=800,
            radial_steps=100,
        )
        upper_keys = (
            "sqrt_spectrum_l2_upper_bound",
            "sqrt_spectrum_first_derivative_l2_upper_bound",
            "sqrt_spectrum_second_derivative_l2_upper_bound",
        )
        exact_keys = tuple(f"{key}_exact" for key in upper_keys)
        for estimate, upper_key, exact_key in zip(
            estimates,
            upper_keys,
            exact_keys,
        ):
            exact_upper = Fraction(enclosure[exact_key])
            self.assertLess(estimate, float(exact_upper))
            self.assertGreaterEqual(enclosure[upper_key], float(exact_upper))
        self.assertAlmostEqual(
            enclosure["sqrt_spectrum_l2_upper_bound"],
            3495.3254535381884,
        )
        self.assertAlmostEqual(
            enclosure["sqrt_spectrum_first_derivative_l2_upper_bound"],
            12944.154923952921,
        )
        self.assertAlmostEqual(
            enclosure["sqrt_spectrum_second_derivative_l2_upper_bound"],
            71805.96634061396,
        )

    def test_analytic_enclosure_radius_scaling(self):
        unit = smooth_worldtube_analytic_sobolev_upper_bounds()
        doubled = smooth_worldtube_analytic_sobolev_upper_bounds(
            radius=2.0,
            support_radius=0.4,
        )
        norm_keys = (
            "sqrt_spectrum_l2_upper_bound",
            "sqrt_spectrum_first_derivative_l2_upper_bound",
            "sqrt_spectrum_second_derivative_l2_upper_bound",
        )
        expected = (0.25, 0.5, 1.0)
        for key, ratio in zip(norm_keys, expected):
            self.assertAlmostEqual(doubled[key] / unit[key], ratio, places=12)

    def test_radius_dimensional_scaling(self):
        unit = smooth_worldtube_sobolev_norms(
            radius=1.0,
            support_radius=0.2,
            frequency_window=200.0,
            frequency_steps=800,
            radial_steps=100,
        )
        doubled = smooth_worldtube_sobolev_norms(
            radius=2.0,
            support_radius=0.4,
            frequency_window=100.0,
            frequency_steps=800,
            radial_steps=100,
        )
        self.assertAlmostEqual(doubled[0] / unit[0], 0.25, places=10)
        self.assertAlmostEqual(doubled[1] / unit[1], 0.5, places=10)
        self.assertAlmostEqual(doubled[2] / unit[2], 1.0, places=10)

    def test_certificate_and_cli(self):
        certificate = static_patch_smooth_worldtube_ule_certificate(
            maximum_spin=64
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertFalse(
            certificate["profile_specific_constants_interval_certified"]
        )
        self.assertTrue(
            certificate["exact_profile_sobolev_norms_analytically_enclosed"]
        )
        self.assertTrue(certificate["frequency_tails_rigorously_enclosed"])
        wide = certificate["wide_moment_record"]
        self.assertAlmostEqual(wide["sqrt_spectrum_l2"], 26.6977477290)
        self.assertAlmostEqual(
            wide["sqrt_spectrum_first_derivative_l2"],
            1.57849600683,
        )
        self.assertAlmostEqual(
            wide["sqrt_spectrum_second_derivative_l2"],
            0.176766804082,
        )
        self.assertAlmostEqual(wide["jump_l1_sobolev_estimate"], 16.2723018013)
        self.assertAlmostEqual(
            wide["jump_first_moment_sobolev_estimate"],
            1.32407331492,
        )
        self.assertAlmostEqual(
            certificate["numerical_constant_obstruction_coupling_cap"],
            2.2576653344109739e-13,
        )
        self.assertAlmostEqual(
            certificate["numerical_heat_matching_coupling_cap"],
            1.9877634898620847e-14,
        )
        self.assertLess(
            certificate[
                "analytic_enclosure_constant_obstruction_guarded_float_cap"
            ],
            certificate["numerical_constant_obstruction_coupling_cap"],
        )
        self.assertLess(
            certificate["analytic_enclosure_heat_matching_guarded_float_cap"],
            certificate["numerical_heat_matching_coupling_cap"],
        )
        self.assertTrue(
            certificate[
                "analytic_enclosure_cap_formula_is_symbolically_sufficient"
            ]
        )
        self.assertFalse(
            certificate["analytic_enclosure_cap_float_evaluation_directed"]
        )
        self.assertEqual(certificate["analytic_enclosure_cap_float_guard"], 0.999999)
        penalty = certificate["localization_penalty_record"]
        self.assertIsNotNone(penalty)
        self.assertAlmostEqual(
            penalty["sufficient_coupling_cap_exponent"],
            2.5,
            delta=0.12,
        )
        self.assertAlmostEqual(
            penalty["second_derivative_squared_log_slope_narrow"],
            3.0 / (64.0 * pi**2),
            delta=5.0e-4,
        )
        self.assertTrue(all(certificate["numerical_consistency_checks"].values()))
        args = build_parser().parse_args(["static-patch-smooth-worldtube-ule"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.radius, 1.0)
        self.assertEqual(args.support_radius, 0.2)

    def test_validation(self):
        with self.assertRaises(ValueError):
            smooth_compact_seed_shape(-1.0)
        with self.assertRaises(ValueError):
            smooth_seed_spherical_transform_derivatives(1.0, radial_steps=3)
        with self.assertRaises(ValueError):
            smooth_worldtube_sobolev_norms(frequency_steps=3)
        with self.assertRaises(ValueError):
            static_patch_smooth_worldtube_ule_certificate(support_radius=3.0)
        with self.assertRaises(ValueError):
            static_patch_smooth_worldtube_ule_certificate(
                support_radius=0.05
            )
        with self.assertRaises(ValueError):
            static_patch_smooth_worldtube_ule_certificate(support_radius=0.3)


if __name__ == "__main__":
    unittest.main()
