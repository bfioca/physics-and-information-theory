import unittest

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_radial_smearing import (
    finite_switching_radial_correlation_record,
    hyperbolic_spherical_function,
    radial_profile_zero_frequency_amplitude,
    radial_smeared_zero_frequency_record,
    static_patch_radial_smearing_certificate,
    zero_frequency_spherical_mean,
)
from qgtoy.static_patch_scalar_common_mode import zero_frequency_scalar_correlation


class StaticPatchRadialSmearingTest(unittest.TestCase):
    def test_spherical_mean_product_formula(self):
        for center, shell in ((0.0, 1.0), (0.4, 0.0), (0.3, 0.8), (2.0, 1.5)):
            self.assertAlmostEqual(
                zero_frequency_spherical_mean(center, shell),
                zero_frequency_scalar_correlation(center)
                * zero_frequency_scalar_correlation(shell),
                places=15,
            )

    def test_profile_amplitude_normalizes_weights(self):
        self.assertAlmostEqual(
            radial_profile_zero_frequency_amplitude(
                (0.0, 1.0),
                (2.0, 2.0),
            ),
            0.5 * (1.0 + zero_frequency_scalar_correlation(1.0)),
        )

    def test_fixed_frequency_factor_is_bounded_by_zero_mode(self):
        for distance in (0.0, 0.2, 1.0, 3.0):
            zero_mode = zero_frequency_scalar_correlation(distance)
            for parameter in (-4.0, -1.0, 0.0, 0.5, 2.0, 8.0):
                self.assertLessEqual(
                    abs(hyperbolic_spherical_function(parameter, distance)),
                    zero_mode + 1.0e-15,
                )

    def test_arbitrary_radial_profiles_cancel(self):
        record = radial_smeared_zero_frequency_record(
            1.3,
            first_shell_radii=(0.0, 0.5, 3.0),
            first_shell_weights=(1.0, 5.0, 2.0),
            second_shell_radii=(0.2, 1.1, 5.0),
            second_shell_weights=(7.0, 1.0, 3.0),
        )
        self.assertAlmostEqual(
            record["normalized_cross_spectral_correlation"],
            zero_frequency_scalar_correlation(1.3),
            places=15,
        )
        self.assertTrue(record["radial_smearing_cancels_exactly"])

    def test_broad_profile_does_not_restore_common_mode(self):
        narrow = radial_smeared_zero_frequency_record(
            2.0,
            first_shell_radii=(0.01,),
            first_shell_weights=(1.0,),
            second_shell_radii=(0.02,),
            second_shell_weights=(1.0,),
        )
        broad = radial_smeared_zero_frequency_record(
            2.0,
            first_shell_radii=(1.0, 4.0, 8.0),
            first_shell_weights=(1.0, 1.0, 1.0),
            second_shell_radii=(2.0, 6.0),
            second_shell_weights=(1.0, 3.0),
        )
        self.assertAlmostEqual(
            narrow["normalized_cross_spectral_correlation"],
            broad["normalized_cross_spectral_correlation"],
            places=15,
        )

    def test_finite_switching_cannot_improve_zero_mode_correlation(self):
        record = finite_switching_radial_correlation_record(
            1.1,
            spectral_parameters=(0.0, 0.3, 1.0, 2.5, 5.0),
            spectral_weights=(0.1, 1.0, 0.8, 0.4, 0.2),
            first_shell_radii=(0.0, 0.7, 2.0),
            first_shell_weights=(1.0, 3.0, 1.0),
            second_shell_radii=(0.2, 1.5, 4.0),
            second_shell_weights=(2.0, 1.0, 1.0),
        )
        self.assertTrue(record["absolute_correlation_respects_zero_mode_bound"])
        self.assertTrue(record["relative_noise_variance_respects_bound"])
        self.assertLessEqual(
            abs(record["normalized_filtered_correlation"]),
            zero_frequency_scalar_correlation(1.1),
        )

    def test_certificate(self):
        certificate = static_patch_radial_smearing_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("not a three-axis", certificate["claim_boundary"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-radial-smearing"])
        self.assertTrue(callable(args.func))

    def test_validation(self):
        with self.assertRaises(ValueError):
            radial_profile_zero_frequency_amplitude((), ())
        with self.assertRaises(ValueError):
            radial_profile_zero_frequency_amplitude((0.0,), (0.0,))
        with self.assertRaises(ValueError):
            radial_smeared_zero_frequency_record(
                -1.0,
                first_shell_radii=(0.0,),
                first_shell_weights=(1.0,),
                second_shell_radii=(0.0,),
                second_shell_weights=(1.0,),
            )


if __name__ == "__main__":
    unittest.main()
