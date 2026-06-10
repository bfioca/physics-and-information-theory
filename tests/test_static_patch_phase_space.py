import unittest
from math import factorial, pi

from qgtoy.static_patch_phase_space import (
    CompactPolynomialBump,
    PhaseSpaceTest,
    continuum_phase_space_covariance,
    continuum_phase_space_symplectic_form,
    continuum_unequal_time_wightman,
    finite_phase_space_covariance,
    finite_phase_space_symplectic_form,
    finite_reverse_order_wightman,
    finite_uncertainty_margin,
    finite_unequal_time_wightman,
    polynomial_bump_moment,
    polynomial_bump_normalization,
    static_patch_phase_space_certificate,
    unitary_sine_transform,
)
from qgtoy.static_patch_weyl_regulator import de_sitter_inverse_temperature


class StaticPatchPhaseSpaceTest(unittest.TestCase):
    def setUp(self):
        self.first_bump = CompactPolynomialBump(0.25, 0.75, 3)
        self.second_bump = CompactPolynomialBump(0.9, 1.35, 3)
        self.first = PhaseSpaceTest(
            field_bump=self.first_bump,
            momentum_bump=self.second_bump,
        )
        self.second = PhaseSpaceTest(
            field_bump=self.second_bump,
            momentum_bump=self.first_bump,
            field_scale=0.7,
            momentum_scale=-0.4,
        )

    def test_bump_normalization_and_moment(self):
        normalization = polynomial_bump_normalization(self.first_bump)
        width = self.first_bump.support_end - self.first_bump.support_start
        power = self.first_bump.power
        beta_value = factorial(2 * power) ** 2 / factorial(4 * power + 1)
        self.assertAlmostEqual(
            normalization * normalization * width ** (4 * power + 1) * beta_value,
            1.0,
        )
        zeroth = polynomial_bump_moment(self.first_bump, 0)
        first = polynomial_bump_moment(self.first_bump, 1)
        midpoint = 0.5 * (
            self.first_bump.support_start + self.first_bump.support_end
        )
        self.assertAlmostEqual(first, midpoint * zeroth)

    def test_sine_transform_is_regular(self):
        self.assertEqual(unitary_sine_transform(0.0, self.first_bump), 0.0)
        self.assertGreater(unitary_sine_transform(1.0, self.first_bump), 0.0)
        high_default = unitary_sine_transform(1000.0, self.first_bump)
        high_refined = unitary_sine_transform(
            1000.0, self.first_bump, quadrature_steps=1000
        )
        self.assertLess(abs(high_default - high_refined), 1e-11)

    def test_symplectic_antisymmetry(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 1024.0,
            momentum_cutoff=20.0,
        )
        forward = finite_phase_space_symplectic_form(
            self.first, self.second, **parameters
        )
        reverse = finite_phase_space_symplectic_form(
            self.second, self.first, **parameters
        )
        self.assertAlmostEqual(forward, -reverse)

    def test_covariance_is_symmetric_and_uncertainty_holds(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 1024.0,
            momentum_cutoff=20.0,
        )
        forward = finite_phase_space_covariance(self.first, self.second, **parameters)
        reverse = finite_phase_space_covariance(self.second, self.first, **parameters)
        self.assertAlmostEqual(forward, reverse)
        self.assertGreaterEqual(
            finite_uncertainty_margin(self.first, self.second, **parameters),
            -1e-10,
        )

    def test_finite_forms_converge_to_fixed_band_continuum(self):
        continuum_symplectic = continuum_phase_space_symplectic_form(
            self.first, self.second, momentum_cutoff=20.0
        )
        continuum_covariance = continuum_phase_space_covariance(
            self.first, self.second, radius=1.0, momentum_cutoff=20.0
        )
        errors = []
        for power in (64.0, 4096.0, 16777216.0, 281474976710656.0, 7.922816251426434e28):
            parameters = dict(
                radius=1.0,
                stretched_distance=1.0 / power,
                momentum_cutoff=20.0,
            )
            errors.append(
                (
                    abs(
                        finite_phase_space_symplectic_form(
                            self.first, self.second, **parameters
                        )
                        - continuum_symplectic
                    ),
                    abs(
                        finite_phase_space_covariance(
                            self.first, self.second, **parameters
                        )
                        - continuum_covariance
                    ),
                )
            )
        self.assertLess(errors[-1][0], errors[0][0])
        self.assertLess(errors[-1][1], errors[0][1])

    def test_finite_kms_boundary_identity(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 1024.0,
            momentum_cutoff=20.0,
        )
        beta = de_sitter_inverse_temperature(1.0)
        time = 0.37
        left = finite_unequal_time_wightman(
            self.first, self.second, time + 1j * beta, **parameters
        )
        right = finite_reverse_order_wightman(
            self.first, self.second, time, **parameters
        )
        self.assertLess(abs(left - right), 1e-9)

    def test_equal_time_wightman_matches_covariance_and_symplectic_form(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 1024.0,
            momentum_cutoff=20.0,
        )
        wightman = finite_unequal_time_wightman(
            self.first, self.second, 0.0, **parameters
        )
        covariance = finite_phase_space_covariance(
            self.first, self.second, **parameters
        )
        symplectic = finite_phase_space_symplectic_form(
            self.first, self.second, **parameters
        )
        self.assertAlmostEqual(wightman.real, covariance)
        self.assertAlmostEqual(wightman.imag, 0.5 * symplectic)
        reverse = finite_unequal_time_wightman(
            self.second, self.first, 0.0, **parameters
        )
        self.assertAlmostEqual(abs(reverse - wightman.conjugate()), 0.0)

    def test_unequal_time_function_converges_to_fixed_band_continuum(self):
        beta = de_sitter_inverse_temperature(1.0)
        time = 0.37 + 0.4j * beta
        continuum = continuum_unequal_time_wightman(
            self.first,
            self.second,
            time,
            radius=1.0,
            momentum_cutoff=20.0,
        )
        errors = []
        for power in (64.0, 4096.0, 16777216.0, 281474976710656.0, 7.922816251426434e28):
            finite = finite_unequal_time_wightman(
                self.first,
                self.second,
                time,
                radius=1.0,
                stretched_distance=1.0 / power,
                momentum_cutoff=20.0,
            )
            errors.append(abs(finite - continuum))
        self.assertLess(errors[-1], errors[0])
        self.assertLess(errors[-1], 2e-3)

    def test_high_cutoff_kms_evaluation_is_stable(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 1024.0,
            momentum_cutoff=120.0,
        )
        beta = de_sitter_inverse_temperature(1.0)
        value = finite_unequal_time_wightman(
            self.first, self.second, 0.25 + 0.5j * beta, **parameters
        )
        self.assertTrue(value.real == value.real)
        self.assertTrue(value.imag == value.imag)

    def test_certificate_passes_with_nonlocality_boundary(self):
        certificate = static_patch_phase_space_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("spatially nonlocal", certificate["claim_boundary"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            CompactPolynomialBump(1.0, 0.5, 3)
        with self.assertRaises(ValueError):
            PhaseSpaceTest()
        with self.assertRaises(ValueError):
            unitary_sine_transform(1.0, self.first_bump, quadrature_steps=21)
        with self.assertRaises(ValueError):
            CompactPolynomialBump(0.25, 0.75, 13)
        with self.assertRaises(ValueError):
            CompactPolynomialBump(0.25, 0.75, 2)
        with self.assertRaises(ValueError):
            static_patch_phase_space_certificate(steps=9)


if __name__ == "__main__":
    unittest.main()
