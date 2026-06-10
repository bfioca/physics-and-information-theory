import unittest
from math import sqrt

from qgtoy.__main__ import build_parser
from qgtoy.massive_skyrmion_worldtube import (
    dimensionless_radial_pressure,
    dimensionless_shell_mean_curvature,
    hard_wall_equilibrium_record,
    hard_wall_profile_integrals,
    massive_skyrmion_worldtube_certificate,
    solve_hard_wall_skyrmion_profile,
)


class MassiveSkyrmionWorldtubeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.slope, cls.points = solve_hard_wall_skyrmion_profile()
        cls.integrals = hard_wall_profile_integrals(
            cls.points,
            pion_mass=1.0,
            curvature=0.0025,
        )

    def test_hard_wall_profile_and_baryon_number(self):
        self.assertAlmostEqual(self.slope, 1.5799534, places=6)
        self.assertLess(abs(self.points[-1][1]), 1.0e-7)
        self.assertTrue(all(slope < 0.0 for _, _, slope in self.points))
        self.assertAlmostEqual(
            self.integrals["baryon_number_integral"],
            1.0,
            places=4,
        )
        self.assertAlmostEqual(
            self.integrals["baryon_number_from_wall_value"],
            1.0,
            places=8,
        )

    def test_hard_wall_pressure_reduction(self):
        radius, profile, derivative = self.points[-1]
        curvature = 0.0025
        lapse = 1.0 - curvature * radius**2
        pressure = dimensionless_radial_pressure(
            radius,
            profile,
            derivative,
            pion_mass=1.0,
            curvature=curvature,
        )
        self.assertAlmostEqual(pressure, lapse * derivative**2 / 8.0, places=12)

    def test_positive_tension_radius_bound(self):
        curvature = 0.0025
        critical = sqrt(2.0 / (3.0 * curvature))
        self.assertGreater(
            dimensionless_shell_mean_curvature(
                0.9 * critical,
                curvature=curvature,
            ),
            0.0,
        )
        self.assertLess(
            dimensionless_shell_mean_curvature(
                1.01 * critical,
                curvature=curvature,
            ),
            0.0,
        )

    def test_centered_equilibrium_record(self):
        record = hard_wall_equilibrium_record()
        self.assertTrue(record["positive_tension_supported"])
        self.assertGreater(record["dimensionless_equilibrium_tension"], 0.0)
        self.assertLess(record["wall_to_interior_mass_ratio"], 0.02)

    def test_certificate(self):
        certificate = massive_skyrmion_worldtube_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("off-center", certificate["claim_boundary"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["massive-skyrmion-worldtube"])
        self.assertEqual(args.pion_mass, 1.0)
        self.assertEqual(args.curvature, 0.0025)
        self.assertEqual(args.wall_radius, 4.0)
        self.assertEqual(args.step, 0.002)

    def test_validation(self):
        with self.assertRaises(ValueError):
            solve_hard_wall_skyrmion_profile(curvature=1.0, wall_radius=1.0)
        with self.assertRaises(ValueError):
            dimensionless_shell_mean_curvature(0.0, curvature=0.1)
        with self.assertRaises(ValueError):
            solve_hard_wall_skyrmion_profile(
                pion_mass=4.0,
                curvature=0.02,
                wall_radius=6.0,
                step=0.002,
            )


if __name__ == "__main__":
    unittest.main()
