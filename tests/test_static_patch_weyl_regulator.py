import unittest
from math import pi

from qgtoy.static_patch_weyl_regulator import (
    box_test_sine_transform,
    continuum_s_wave_covariance,
    de_sitter_inverse_temperature,
    finite_s_wave_covariance,
    local_static_patch_regulator_record,
    retained_s_wave_mode_count,
    s_wave_mode_frequency,
    static_patch_weyl_regulator_certificate,
    thermal_covariance_integrand,
    tortoise_length,
)


class StaticPatchWeylRegulatorTest(unittest.TestCase):
    def test_geometric_temperature_and_tortoise_length(self):
        radius = 2.0
        self.assertAlmostEqual(de_sitter_inverse_temperature(radius), 4.0 * pi)
        lengths = tuple(
            tortoise_length(radius, radius / power)
            for power in (8.0, 32.0, 128.0, 512.0)
        )
        self.assertTrue(all(right > left for left, right in zip(lengths, lengths[1:])))
        self.assertGreater(tortoise_length(1.0, 1e-308), 300.0)

    def test_s_wave_spacing_collapses_at_the_horizon(self):
        radius = 1.0
        frequencies = tuple(
            s_wave_mode_frequency(1, radius=radius, stretched_distance=radius / power)
            for power in (8.0, 32.0, 128.0, 512.0, 2048.0)
        )
        self.assertTrue(
            all(right < left for left, right in zip(frequencies, frequencies[1:]))
        )

    def test_box_transform_and_integrand_are_regular_at_zero(self):
        transform = box_test_sine_transform(
            0.0,
            support_start=0.25,
            support_end=0.75,
        )
        self.assertEqual(transform, 0.0)
        integrand = thermal_covariance_integrand(
            0.0,
            beta=2.0 * pi,
            support_start=0.25,
            support_end=0.75,
        )
        self.assertGreater(integrand, 0.0)

    def test_finite_covariance_converges_to_continuum_riemann_integral(self):
        radius = 1.0
        continuum = continuum_s_wave_covariance(
            radius=radius,
            support_start=0.25,
            support_end=0.75,
            momentum_cutoff=80.0,
        )
        errors = []
        for power in (16.0, 64.0, 256.0, 1024.0, 4096.0):
            finite = finite_s_wave_covariance(
                radius=radius,
                stretched_distance=radius / power,
                support_start=0.25,
                support_end=0.75,
                momentum_cutoff=80.0,
            )
            errors.append(abs(finite - continuum))
        self.assertLess(errors[-1], errors[0])
        self.assertLess(errors[-1], 5e-3)

    def test_cutoff_below_first_mode_retains_no_modes(self):
        count = retained_s_wave_mode_count(
            radius=1.0,
            stretched_distance=0.5,
            momentum_cutoff=0.1,
        )
        self.assertEqual(count, 0)
        covariance = finite_s_wave_covariance(
            radius=1.0,
            stretched_distance=0.5,
            support_start=0.1,
            support_end=0.2,
            momentum_cutoff=0.1,
        )
        self.assertEqual(covariance, 0.0)

    def test_record_keeps_local_and_type_claims_separate(self):
        record = local_static_patch_regulator_record(
            radius=1.0,
            stretched_distance=1.0 / 256.0,
            support_start=0.25,
            support_end=0.75,
            momentum_cutoff=50.0,
        )
        self.assertIn("equal-time", record["observable_probe"])
        self.assertFalse(record["factor_type_claimed"])
        self.assertIn("not convergence of a full KMS", record["convergence_mode"])

    def test_large_thermal_argument_is_stable(self):
        value = thermal_covariance_integrand(
            100.0,
            beta=20.0,
            support_start=0.25,
            support_end=0.75,
        )
        self.assertGreaterEqual(value, 0.0)

    def test_certificate_passes_with_explicit_boundary(self):
        certificate = static_patch_weyl_regulator_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("no spacetime Weyl net", certificate["claim_boundary"])
        self.assertIn("equal-time", certificate["central_result"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            tortoise_length(1.0, 1.0)
        with self.assertRaises(ValueError):
            s_wave_mode_frequency(0, radius=1.0, stretched_distance=0.1)
        with self.assertRaises(ValueError):
            box_test_sine_transform(1.0, support_start=1.0, support_end=0.5)
        with self.assertRaises(ValueError):
            continuum_s_wave_covariance(
                radius=1.0,
                support_start=0.25,
                support_end=0.75,
                momentum_cutoff=10.0,
                integration_steps=3,
            )


if __name__ == "__main__":
    unittest.main()
