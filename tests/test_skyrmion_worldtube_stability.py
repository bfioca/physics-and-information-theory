import unittest
from unittest.mock import patch

from qgtoy.__main__ import build_parser
from qgtoy.skyrmion_worldtube_stability import (
    centered_radial_stability_record,
    finite_pinning_asymptotic_record,
    shell_mean_curvature_derivative,
    skyrmion_worldtube_stability_certificate,
)


class SkyrmionWorldtubeStabilityTest(unittest.TestCase):
    def test_shell_curvature_derivative_matches_finite_difference(self):
        radius = 4.0
        curvature = 0.0025
        difference = 1.0e-5

        def mean_curvature(value):
            lapse = 1.0 - curvature * value**2
            return 2.0 * lapse**0.5 / value - curvature * value / lapse**0.5

        numerical = (
            mean_curvature(radius + difference)
            - mean_curvature(radius - difference)
        ) / (2.0 * difference)
        self.assertAlmostEqual(
            shell_mean_curvature_derivative(radius, curvature=curvature),
            numerical,
            places=9,
        )

    def test_default_radial_branch_is_locally_stable(self):
        record = centered_radial_stability_record()
        self.assertTrue(record["adiabatic_spherical_local_minimum"])
        self.assertAlmostEqual(
            record["dimensionless_energy_second_derivative_at_fixed_tension"],
            0.4399,
            places=3,
        )
        self.assertGreater(record["dimensionless_wall_kinetic_mass"], 0.0)
        self.assertGreater(record["dimensionless_shell_only_frequency"], 0.0)

    def test_finite_pinning_coefficients(self):
        record = finite_pinning_asymptotic_record()
        self.assertTrue(
            record[
                "finite_cosine_pinning_cannot_preserve_exact_unit_baryon_number"
            ]
        )
        self.assertAlmostEqual(
            record["boundary_profile_coefficient_in_inverse_stiffness"],
            0.0215251,
            places=6,
        )
        self.assertAlmostEqual(
            record["baryon_deficit_coefficient_in_inverse_stiffness_cubed"],
            2.11638e-6,
            places=10,
        )
        self.assertAlmostEqual(
            record["pinning_energy_coefficient_in_inverse_stiffness"],
            0.0456379,
            places=6,
        )

    def test_unstable_branch_reports_negative_frequency_squared(self):
        equilibrium = {
            "dimensionless_equilibrium_tension": 1.0,
            "dimensionless_interior_radial_pressure": 1.0,
        }
        with patch(
            "qgtoy.skyrmion_worldtube_stability.hard_wall_equilibrium_record",
            return_value=equilibrium,
        ), patch(
            "qgtoy.skyrmion_worldtube_stability._dirichlet_branch_pressure",
            side_effect=(0.0, 1.0),
        ):
            record = centered_radial_stability_record(
                curvature=0.0,
                wall_radius=4.0,
                radius_difference=0.005,
            )
        self.assertLess(record["dimensionless_shell_only_frequency_squared"], 0.0)
        self.assertIsNone(record["dimensionless_shell_only_frequency"])
        self.assertFalse(record["adiabatic_spherical_local_minimum"])

    def test_certificate(self):
        certificate = skyrmion_worldtube_stability_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_cli_defaults(self):
        args = build_parser().parse_args(["skyrmion-worldtube-stability"])
        self.assertEqual(args.radius_difference, 0.005)
        self.assertEqual(args.wall_radius, 4.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            centered_radial_stability_record(pion_mass=0.0)
        with self.assertRaises(ValueError):
            centered_radial_stability_record(
                wall_radius=1.0,
                radius_difference=1.0,
            )


if __name__ == "__main__":
    unittest.main()
