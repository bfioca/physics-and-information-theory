import unittest
from math import pi

from qgtoy.__main__ import build_parser
from qgtoy.massive_skyrmion_profile import (
    baryon_number_inside_boundary,
    de_sitter_horizon_profile_derivative,
    de_sitter_inertia_log_coefficient,
    dimensionless_inertia_density,
    flat_profile_integrals,
    flat_tail_log_derivative,
    massive_skyrmion_profile_certificate,
    proper_radius_from_dimensionless,
    solve_flat_skyrmion_profile,
)


class MassiveSkyrmionProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.slope, cls.points = solve_flat_skyrmion_profile()
        cls.integrals = flat_profile_integrals(cls.points, pion_mass=1.0)

    def test_flat_profile_and_integral_identities(self):
        self.assertAlmostEqual(self.slope, 1.58024, places=4)
        self.assertTrue(all(0.0 <= value <= pi for _, value, _ in self.points))
        self.assertTrue(all(slope <= 1.0e-7 for _, _, slope in self.points))
        self.assertAlmostEqual(
            self.integrals["baryon_number_integral"],
            1.0,
            places=4,
        )
        total = sum(
            self.integrals[key]
            for key in ("sigma_energy_E2", "skyrme_energy_E4", "mass_energy_E0")
        )
        self.assertLess(
            abs(self.integrals["derrick_residual_E2_minus_E4_plus_3E0"]),
            2.0e-6 * total,
        )
        self.assertAlmostEqual(
            self.integrals["dimensionless_mass_c_M"],
            48.6317632,
            places=6,
        )
        self.assertAlmostEqual(
            self.integrals["dimensionless_inertia_c_I"],
            34.3539730,
            places=6,
        )

    def test_tail_robin_condition(self):
        radius, profile, derivative = self.points[-1]
        residual = derivative - flat_tail_log_derivative(
            radius,
            pion_mass=1.0,
        ) * profile
        self.assertLess(abs(residual), 1.0e-7)

    def test_boundary_baryon_formula(self):
        self.assertEqual(baryon_number_inside_boundary(0.0), 1.0)
        self.assertEqual(baryon_number_inside_boundary(pi), 0.0)
        self.assertAlmostEqual(
            baryon_number_inside_boundary(self.points[-1][1]),
            self.integrals["baryon_number_integral"],
            places=4,
        )

    def test_horizon_regular_vacuum_and_inertia_divergence(self):
        horizon_radius = 10.0
        self.assertEqual(
            de_sitter_horizon_profile_derivative(
                0.0,
                horizon_radius=horizon_radius,
                pion_mass=1.0,
            ),
            0.0,
        )
        horizon_profile = 0.7
        epsilon = 1.0e-6
        numerical = epsilon * dimensionless_inertia_density(
            horizon_radius - epsilon,
            horizon_profile,
            0.0,
            curvature=1.0 / horizon_radius**2,
        )
        analytic = de_sitter_inertia_log_coefficient(
            horizon_profile,
            horizon_radius=horizon_radius,
        )
        self.assertAlmostEqual(numerical / analytic, 1.0, places=6)

    def test_proper_radius_reduces_to_flat_limit(self):
        flat = proper_radius_from_dimensionless(
            2.0,
            inverse_length_scale=4.0,
            curvature=0.0,
        )
        weakly_curved = proper_radius_from_dimensionless(
            2.0,
            inverse_length_scale=4.0,
            curvature=1.0e-10,
        )
        self.assertEqual(flat, 0.5)
        self.assertAlmostEqual(weakly_curved, flat, places=9)

    def test_certificate(self):
        certificate = massive_skyrmion_profile_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertTrue(
            certificate["de_sitter_gate"]["worldtube_selected_as_controlled_remedy"]
        )
        self.assertFalse(
            certificate["de_sitter_gate"][
                "all_nontrivial_global_profiles_are_proved_to_diverge"
            ]
        )
        self.assertIn("point-local", certificate["collective_coupling_gate"])

    def test_nondefault_mass_auto_bracketing(self):
        for pion_mass in (0.5, 1.5, 2.0):
            _, points = solve_flat_skyrmion_profile(
                pion_mass=pion_mass,
                maximum_radius=min(10.0, 10.0 / pion_mass),
                step=0.004,
                bisection_steps=40,
            )
            self.assertTrue(all(0.0 <= value <= pi for _, value, _ in points))

    def test_cli_defaults(self):
        args = build_parser().parse_args(["massive-skyrmion-profile"])
        self.assertEqual(args.pion_mass, 1.0)
        self.assertEqual(args.maximum_radius, 10.0)
        self.assertEqual(args.step, 0.002)

    def test_validation(self):
        with self.assertRaises(ValueError):
            solve_flat_skyrmion_profile(pion_mass=0.0)
        with self.assertRaises(ValueError):
            solve_flat_skyrmion_profile(
                lower_shooting_slope=0.1,
                upper_shooting_slope=0.2,
                auto_bracket=False,
            )
        with self.assertRaises(ValueError):
            proper_radius_from_dimensionless(
                2.0,
                inverse_length_scale=1.0,
                curvature=1.0,
            )
        with self.assertRaises(ValueError):
            solve_flat_skyrmion_profile(
                pion_mass=1.0,
                maximum_radius=20.0,
                step=0.01,
            )


if __name__ == "__main__":
    unittest.main()
