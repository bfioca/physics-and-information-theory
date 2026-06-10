import unittest
from math import pi

from qgtoy.static_patch_lorentzian_hadamard import (
    bunch_davies_kms_strip_kernel,
    optical_kms_strip_kernel,
    optical_strip_spectral_integral,
    spacelike_hadamard_leading_ratio,
    static_patch_lorentzian_hadamard_certificate,
)


class StaticPatchLorentzianHadamardTest(unittest.TestCase):
    def test_kms_opposite_boundary(self):
        radius = 1.0
        beta = 2.0 * pi * radius
        parameters = dict(
            radius=radius,
            first_tortoise_coordinate=0.7,
            second_tortoise_coordinate=1.1,
            cosine_angle=0.3,
        )
        lower = bunch_davies_kms_strip_kernel(0.8 - 1j * (beta - 0.2), **parameters)
        reversed_parameters = dict(parameters)
        reversed_parameters["first_tortoise_coordinate"] = 1.1
        reversed_parameters["second_tortoise_coordinate"] = 0.7
        upper = bunch_davies_kms_strip_kernel(-0.8 - 0.2j, **reversed_parameters)
        self.assertAlmostEqual(lower.real, upper.real)
        self.assertAlmostEqual(lower.imag, upper.imag)

    def test_spectral_integral_matches_closed_kernel(self):
        parameters = dict(
            radius=1.0,
            first_tortoise_coordinate=0.7,
            second_tortoise_coordinate=1.1,
            cosine_angle=0.3,
        )
        complex_time = 0.8 - 0.9j
        closed = optical_kms_strip_kernel(complex_time, **parameters)
        numeric = optical_strip_spectral_integral(
            complex_time,
            integration_steps=8000,
            **parameters,
        )
        self.assertLess(abs(numeric - closed), 2e-8)

    def test_hadamard_leading_coefficient(self):
        ratios = tuple(
            spacelike_hadamard_leading_ratio(
                radius=1.0,
                first_tortoise_coordinate=0.8,
                second_tortoise_coordinate=0.8 + separation,
            )
            for separation in (0.2, 0.1, 0.05, 0.025)
        )
        self.assertLess(abs(ratios[-1] - 1.0), abs(ratios[0] - 1.0))
        self.assertLess(abs(ratios[-1] - 1.0), 1e-4)

    def test_certificate(self):
        certificate = static_patch_lorentzian_hadamard_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(
            certificate["status_scope"],
            "sampled_executable_kernel_checks_only",
        )
        self.assertTrue(all(certificate["executable_checks"].values()))
        self.assertIn("Type III_1", certificate["local_factor_consequence"])
        self.assertIn(
            "excluded",
            certificate["theorem_backed_consequence_status"],
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            optical_kms_strip_kernel(
                0.5,
                radius=1.0,
                first_tortoise_coordinate=0.7,
                second_tortoise_coordinate=1.1,
                cosine_angle=0.3,
            )
        with self.assertRaises(ValueError):
            optical_strip_spectral_integral(
                0.5 - 0.4j,
                radius=1.0,
                first_tortoise_coordinate=0.7,
                second_tortoise_coordinate=1.1,
                cosine_angle=0.3,
                integration_steps=10,
            )


if __name__ == "__main__":
    unittest.main()
