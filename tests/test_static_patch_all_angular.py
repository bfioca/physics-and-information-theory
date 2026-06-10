import unittest
from math import cos, cosh, isfinite, pi, sin, sinh, sqrt

from qgtoy.static_patch_all_angular import (
    angular_sobolev_tail_factor,
    bunch_davies_euclidean_kernel,
    conformal_angular_radial_potential,
    darboux_radial_mode,
    darboux_radial_modes,
    de_sitter_euclidean_invariant,
    finite_wall_eigenvalue_lower_bound,
    hyperbolic_cosh_distance,
    local_field_angular_tail_bound,
    local_field_covariance_constant,
    local_momentum_angular_tail_bound,
    localized_low_energy_overlap_bound,
    optical_euclidean_kernel,
    static_patch_all_angular_certificate,
)


class StaticPatchAllAngularTest(unittest.TestCase):
    def test_s_wave_mode_and_potential(self):
        momentum = 1.3
        coordinate = 0.7
        self.assertAlmostEqual(
            darboux_radial_mode(
                momentum,
                0,
                radius=1.0,
                tortoise_coordinate=coordinate,
            ),
            sqrt(2.0 / pi) * sin(momentum * coordinate),
        )
        self.assertEqual(
            conformal_angular_radial_potential(
                0,
                radius=1.0,
                tortoise_coordinate=coordinate,
            ),
            0.0,
        )

    def test_first_two_darboux_identities(self):
        momentum = 1.3
        coordinate = 0.7
        q = momentum
        coth = cosh(coordinate) / sinh(coordinate)
        phase = q * coordinate
        first = sqrt(2.0 / pi) * (
            coth * sin(phase) - q * cos(phase)
        ) / sqrt(q * q + 1.0)
        self.assertAlmostEqual(
            darboux_radial_mode(
                momentum, 1, radius=1.0, tortoise_coordinate=coordinate
            ),
            first,
        )
        second = sqrt(2.0 / pi) * (
            (3.0 * coth * coth - 1.0 - q * q) * sin(phase)
            - 3.0 * q * coth * cos(phase)
        ) / sqrt((q * q + 1.0) * (q * q + 4.0))
        self.assertAlmostEqual(
            darboux_radial_mode(
                momentum, 2, radius=1.0, tortoise_coordinate=coordinate
            ),
            second,
        )

    def test_high_angular_modes_are_regular_near_origin(self):
        coarse = darboux_radial_modes(
            1.3, 20, radius=1.0, tortoise_coordinate=0.1
        )
        fine = darboux_radial_modes(
            1.3, 20, radius=1.0, tortoise_coordinate=0.05
        )
        self.assertTrue(all(isfinite(value) for value in coarse))
        self.assertLess(abs(coarse[20]), 1e-15)
        self.assertLess(abs(fine[20]), abs(coarse[20]))

    def test_high_angular_mode_satisfies_radial_equation(self):
        momentum = 1.3
        coordinate = 0.7
        spacing = 1e-4
        for angular_momentum in (0, 1, 2, 8, 16, 32):
            lower = darboux_radial_mode(
                momentum,
                angular_momentum,
                radius=1.0,
                tortoise_coordinate=coordinate - spacing,
            )
            center = darboux_radial_mode(
                momentum,
                angular_momentum,
                radius=1.0,
                tortoise_coordinate=coordinate,
            )
            upper = darboux_radial_mode(
                momentum,
                angular_momentum,
                radius=1.0,
                tortoise_coordinate=coordinate + spacing,
            )
            second_derivative = (upper - 2.0 * center + lower) / spacing**2
            residual = -second_derivative + (
                conformal_angular_radial_potential(
                    angular_momentum,
                    radius=1.0,
                    tortoise_coordinate=coordinate,
                )
                - momentum * momentum
            ) * center
            self.assertLess(abs(residual), 5e-7)

    def test_no_global_angular_gap_but_interior_suppression(self):
        for angular_momentum in (1, 10, 100):
            self.assertLess(
                conformal_angular_radial_potential(
                    angular_momentum,
                    radius=1.0,
                    tortoise_coordinate=20.0,
                ),
                1e-12,
            )
        bounds = tuple(
            localized_low_energy_overlap_bound(
                angular_momentum,
                radius=1.0,
                support_end=1.0,
                energy=1.0,
            )
            for angular_momentum in (1, 4, 16, 64)
        )
        self.assertTrue(all(right < left for left, right in zip(bounds, bounds[1:])))

    def test_finite_wall_lower_bound(self):
        base = finite_wall_eigenvalue_lower_bound(
            1, 0, radius=1.0, tortoise_length=4.0
        )
        angular = finite_wall_eigenvalue_lower_bound(
            1, 3, radius=1.0, tortoise_length=4.0
        )
        radial = finite_wall_eigenvalue_lower_bound(
            2, 0, radius=1.0, tortoise_length=4.0
        )
        self.assertGreater(angular, base)
        self.assertGreater(radial, base)

    def test_angular_sobolev_tail(self):
        self.assertLess(
            angular_sobolev_tail_factor(32, 4.0),
            angular_sobolev_tail_factor(8, 4.0),
        )

    def test_uniform_local_covariance_tail_bounds(self):
        beta = 2.0 * pi
        constant = local_field_covariance_constant(
            inverse_temperature=beta,
            support_end=1.0,
        )
        self.assertAlmostEqual(constant, 4.0 / (beta * pi * pi) + beta / 12.0)
        field_small = local_field_angular_tail_bound(
            8,
            3.0,
            2.0,
            inverse_temperature=beta,
            support_end=1.0,
        )
        field_large = local_field_angular_tail_bound(
            32,
            3.0,
            2.0,
            inverse_temperature=beta,
            support_end=1.0,
        )
        momentum_small = local_momentum_angular_tail_bound(
            8,
            3.0,
            4.0,
            2.0,
            inverse_temperature=beta,
        )
        momentum_large = local_momentum_angular_tail_bound(
            32,
            3.0,
            4.0,
            2.0,
            inverse_temperature=beta,
        )
        self.assertLess(field_large, field_small)
        self.assertLess(momentum_large, momentum_small)

    def test_optical_and_bunch_davies_kernel_identity(self):
        parameters = dict(
            radius=1.0,
            euclidean_time_separation=1.2,
            first_tortoise_coordinate=0.7,
            second_tortoise_coordinate=1.1,
            cosine_angle=0.3,
        )
        optical = optical_euclidean_kernel(**parameters)
        bunch_davies = bunch_davies_euclidean_kernel(**parameters)
        conformal_factor = cosh(0.7) * cosh(1.1)
        self.assertAlmostEqual(conformal_factor * optical, bunch_davies)
        invariant = de_sitter_euclidean_invariant(**parameters)
        self.assertAlmostEqual(
            bunch_davies,
            1.0 / (8.0 * pi * pi * (1.0 - invariant)),
        )
        self.assertGreater(
            hyperbolic_cosh_distance(
                radius=1.0,
                first_tortoise_coordinate=0.7,
                second_tortoise_coordinate=1.1,
                cosine_angle=0.3,
            ),
            1.0,
        )

    def test_near_horizon_geometry_avoids_catastrophic_subtraction(self):
        self.assertEqual(
            hyperbolic_cosh_distance(
                radius=1.0,
                first_tortoise_coordinate=20.0,
                second_tortoise_coordinate=20.0,
                cosine_angle=1.0,
            ),
            1.0,
        )
        parameters = dict(
            radius=1.0,
            euclidean_time_separation=1.2,
            first_tortoise_coordinate=20.0,
            second_tortoise_coordinate=20.0,
            cosine_angle=1.0,
        )
        optical = optical_euclidean_kernel(**parameters)
        bunch_davies = bunch_davies_euclidean_kernel(**parameters)
        self.assertAlmostEqual(cosh(20.0) ** 2 * optical, bunch_davies)
        large_parameters = dict(
            radius=1.0,
            euclidean_time_separation=1.2,
            first_tortoise_coordinate=1000.0,
            second_tortoise_coordinate=1000.0,
            cosine_angle=0.3,
        )
        large_invariant = de_sitter_euclidean_invariant(**large_parameters)
        large_kernel = bunch_davies_euclidean_kernel(**large_parameters)
        self.assertAlmostEqual(large_invariant, 0.3)
        self.assertAlmostEqual(
            large_kernel,
            1.0 / (8.0 * pi * pi * (1.0 - large_invariant)),
        )

    def test_certificate_partial_wave_match(self):
        certificate = static_patch_all_angular_certificate(integration_steps=1200)
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("spectral bottom zero", certificate["low_energy_boundary"])
        self.assertLess(
            certificate["partial_wave_records"][-1][
                "absolute_error_from_closed_optical_kernel"
            ],
            1e-7,
        )

        scaled = static_patch_all_angular_certificate(
            radius=0.25, integration_steps=1200
        )
        self.assertEqual(scaled["status"], "pass")
        self.assertAlmostEqual(
            scaled["closed_optical_kernel"] * 0.25**2,
            certificate["closed_optical_kernel"],
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            conformal_angular_radial_potential(
                -1,
                radius=1.0,
                tortoise_coordinate=1.0,
            )
        with self.assertRaises(ValueError):
            localized_low_energy_overlap_bound(
                1,
                radius=1.0,
                support_end=1.0,
                energy=0.0,
            )
        with self.assertRaises(ValueError):
            static_patch_all_angular_certificate(
                radius=1.0,
                dimensionless_momentum_cutoff=float("nan"),
            )


if __name__ == "__main__":
    unittest.main()
