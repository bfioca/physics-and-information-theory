import unittest

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_skyrmion_bath import (
    skyrmion_current_gradient_spectrum,
)
from qgtoy.static_patch_skyrmion_signed_ule import (
    centered_skyrmion_signed_factor_matrix,
    centered_skyrmion_spectral_matrix,
    optical_dipole_kernel_derivatives,
    skyrmion_current_optical_form_factor_derivatives,
    skyrmion_signed_sobolev_norms,
    skyrmion_signed_sqrt_spectrum_derivatives,
    static_patch_skyrmion_signed_ule_certificate,
)


class StaticPatchSkyrmionSignedUleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = static_patch_skyrmion_signed_ule_certificate()

    def test_kernel_derivatives_match_finite_differences(self):
        p = 1.7
        y = 0.2
        spacing = 1.0e-3
        value, first, second = optical_dipole_kernel_derivatives(p, y)
        plus = optical_dipole_kernel_derivatives(p + spacing, y)[0]
        minus = optical_dipole_kernel_derivatives(p - spacing, y)[0]
        self.assertAlmostEqual(first, (plus - minus) / (2.0 * spacing), places=9)
        self.assertAlmostEqual(
            second,
            (plus - 2.0 * value + minus) / spacing**2,
            places=8,
        )
        tiny = optical_dipole_kernel_derivatives(0.0, 1.0e-8)[0]
        self.assertGreater(tiny, 0.0)
        self.assertAlmostEqual(tiny, 1.0e-16 / 3.0)

    def test_form_factor_derivatives_match_finite_differences(self):
        p = 1.3
        spacing = 1.0e-4
        value, first, second = skyrmion_current_optical_form_factor_derivatives(p)
        plus = skyrmion_current_optical_form_factor_derivatives(p + spacing)[0]
        minus = skyrmion_current_optical_form_factor_derivatives(p - spacing)[0]
        self.assertAlmostEqual(first, (plus - minus) / (2.0 * spacing), places=8)
        self.assertAlmostEqual(
            second,
            (plus - 2.0 * value + minus) / spacing**2,
            places=5,
        )
        origin = skyrmion_current_optical_form_factor_derivatives(0.0)
        self.assertEqual(origin[1], 0.0)

    def test_signed_factor_squares_to_spectrum(self):
        for radius in (0.1, 1.0, 2.0):
            for frequency in (-0.7 / radius, 0.0, 0.7 / radius):
                factor = skyrmion_signed_sqrt_spectrum_derivatives(
                    frequency,
                    radius=radius,
                )[0]
                spectrum = skyrmion_current_gradient_spectrum(
                    frequency,
                    radius=radius,
                )
                self.assertLess(
                    abs(factor * factor / spectrum - 1.0),
                    1.0e-13,
                )
        factor_matrix = centered_skyrmion_signed_factor_matrix(0.7)
        spectrum_matrix = centered_skyrmion_spectral_matrix(0.7)
        for row in range(3):
            for column in range(3):
                product = sum(
                    factor_matrix[row][inner] * factor_matrix[inner][column]
                    for inner in range(3)
                )
                self.assertAlmostEqual(product, spectrum_matrix[row][column])
        nondefault_factor = skyrmion_signed_sqrt_spectrum_derivatives(
            0.7,
            curvature=0.001,
        )[0]
        nondefault_spectrum = skyrmion_current_gradient_spectrum(
            0.7,
            curvature=0.001,
        )
        self.assertLess(
            abs(nondefault_factor**2 / nondefault_spectrum - 1.0),
            1.0e-13,
        )

    def test_negative_frequency_derivatives_match_finite_differences(self):
        frequency = -0.7
        spacing = 1.0e-5
        value, first, second = skyrmion_signed_sqrt_spectrum_derivatives(
            frequency
        )
        plus = skyrmion_signed_sqrt_spectrum_derivatives(
            frequency + spacing
        )[0]
        minus = skyrmion_signed_sqrt_spectrum_derivatives(
            frequency - spacing
        )[0]
        self.assertAlmostEqual(first, (plus - minus) / (2.0 * spacing), places=8)
        self.assertAlmostEqual(
            second,
            (plus - 2.0 * value + minus) / spacing**2,
            places=5,
        )

    def test_finite_window_moments_are_pinned(self):
        wide = self.certificate["wide_moment_record"]
        self.assertAlmostEqual(wide["signed_sqrt_spectrum_l2"], 62.2644668852)
        self.assertAlmostEqual(
            wide["signed_sqrt_spectrum_first_derivative_l2"],
            2.16015691289,
        )
        self.assertAlmostEqual(
            wide["signed_sqrt_spectrum_second_derivative_l2"],
            0.168156611337,
        )
        self.assertAlmostEqual(wide["jump_l1_sobolev_estimate"], 29.0705146786)
        self.assertAlmostEqual(
            wide["jump_first_moment_sobolev_estimate"],
            1.5107394054,
        )
        self.assertAlmostEqual(
            self.certificate["finite_switch_to_stationary_candidate_cap_ratio"],
            1.0 / (1.05**0.5),
            places=9,
        )
        self.assertGreater(
            self.certificate[
                "finite_switch_constant_required_bound_level_effective_age"
            ],
            0.0,
        )
        self.assertGreater(
            self.certificate[
                "finite_switch_heat_required_bound_level_effective_age"
            ],
            self.certificate[
                "finite_switch_constant_required_bound_level_effective_age"
            ],
        )
        self.assertIn(
            "conditional candidate caps",
            self.certificate["finite_switch_condition_status"],
        )

    def test_certificate_and_cli(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["audit_checks"].values()))
        self.assertLess(
            max(self.certificate["relative_profile_step_changes"]),
            2.0e-4,
        )
        self.assertLess(
            max(self.certificate["relative_frequency_mesh_changes"]),
            2.0e-6,
        )
        args = build_parser().parse_args(["static-patch-skyrmion-signed-ule"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.curvature, 0.0025)

    def test_validation(self):
        with self.assertRaises(ValueError):
            optical_dipole_kernel_derivatives(1.0, -0.1)
        with self.assertRaises(ValueError):
            skyrmion_current_optical_form_factor_derivatives(-1.0)
        with self.assertRaises(ValueError):
            skyrmion_signed_sobolev_norms(frequency_window=10_000.0)
        with self.assertRaises(ValueError):
            static_patch_skyrmion_signed_ule_certificate(maximum_spin=0)


if __name__ == "__main__":
    unittest.main()
