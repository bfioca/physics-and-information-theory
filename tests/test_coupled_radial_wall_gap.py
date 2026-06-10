import unittest

from qgtoy.coupled_radial_wall_gap import (
    adiabatic_dragged_profile_frequency_squared,
    coupled_radial_frequency_squared_lower_bound,
    coupled_radial_wall_gap_certificate,
    missing_lift_norm_counterexample,
    moving_endpoint_barta_boundary_coefficient,
    normalized_branch_stiffness,
    normalized_wall_kinetic_mass,
    uncoupled_radial_frequency_squared_lower_bound,
)


class CoupledRadialWallGapTest(unittest.TestCase):
    def test_zero_lift_recovers_decoupled_minimum(self):
        mass = normalized_wall_kinetic_mass(0.4129339430)
        stiffness = normalized_branch_stiffness(0.4399062320)
        coupled = coupled_radial_frequency_squared_lower_bound(
            fixed_wall_static_form_gap=1.0,
            kinetic_weight_upper_bound=25.0,
            normalized_wall_mass=mass,
            normalized_branch_curvature=stiffness,
            branch_lift_weighted_norm_squared=0.0,
        )
        uncoupled = uncoupled_radial_frequency_squared_lower_bound(
            fixed_wall_static_form_gap=1.0,
            kinetic_weight_upper_bound=25.0,
            normalized_wall_mass=mass,
            normalized_branch_curvature=stiffness,
        )
        self.assertAlmostEqual(coupled, uncoupled)
        self.assertAlmostEqual(coupled, 0.04)

    def test_added_profile_mass_weakens_the_comparison_gap(self):
        values = tuple(
            coupled_radial_frequency_squared_lower_bound(
                fixed_wall_static_form_gap=1.0,
                kinetic_weight_upper_bound=25.0,
                normalized_wall_mass=0.2,
                normalized_branch_curvature=0.3,
                branch_lift_weighted_norm_squared=value,
            )
            for value in (0.0, 0.1, 1.0, 10.0, 100.0)
        )
        self.assertTrue(all(right < left for left, right in zip(values, values[1:])))

    def test_missing_lift_norm_has_a_sharp_trial_obstruction(self):
        small = missing_lift_norm_counterexample(
            normalized_branch_curvature=0.3,
            normalized_wall_mass=0.2,
            branch_lift_weighted_norm_squared=1.0,
        )
        large = missing_lift_norm_counterexample(
            normalized_branch_curvature=0.3,
            normalized_wall_mass=0.2,
            branch_lift_weighted_norm_squared=1000.0,
        )
        self.assertLess(
            large["trial_frequency_squared_upper_bound"],
            small["trial_frequency_squared_upper_bound"],
        )
        self.assertAlmostEqual(
            large["trial_frequency_squared_upper_bound"],
            0.3 / 1000.2,
        )

    def test_certificate_distinguishes_direct_gap_from_optional_sharpening(self):
        certificate = coupled_radial_wall_gap_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertEqual(
            certificate["current_evidence"]["branch_coordinate_sharpening"],
            "open",
        )
        self.assertIn(
            "omega_hat>=1/50",
            certificate["current_evidence"][
                "direct_coupled_profile_wall_radial_gap"
            ],
        )
        self.assertIn("stronger numerical estimate", certificate["claim_boundary"])

    def test_fixed_wall_witness_fails_at_the_moving_endpoint(self):
        record = moving_endpoint_barta_boundary_coefficient(
            wall_radius=4.0,
            curvature=0.0025,
            wall_profile_derivative=-0.0878757998,
            membrane_tension=0.001931779647,
        )
        self.assertAlmostEqual(
            record["witness_log_derivative_at_wall"],
            -992.0 / 1985.0,
        )
        self.assertAlmostEqual(
            record["total_moving_endpoint_barta_coefficient"],
            -2.24124,
            places=4,
        )
        self.assertLess(record["total_moving_endpoint_barta_coefficient"], 0.0)

    def test_dragged_profile_mass_lowers_the_adiabatic_frequency(self):
        shell_only = adiabatic_dragged_profile_frequency_squared(
            energy_second_derivative=0.4399062320,
            shell_kinetic_mass=0.4129339430,
            branch_lift_weighted_norm_squared=0.0,
        )
        dragged = adiabatic_dragged_profile_frequency_squared(
            energy_second_derivative=0.4399062320,
            shell_kinetic_mass=0.4129339430,
            branch_lift_weighted_norm_squared=0.063759,
        )
        self.assertLess(dragged, shell_only)
        self.assertAlmostEqual(dragged**0.5, 0.847, places=3)

    def test_validation(self):
        with self.assertRaises(ValueError):
            coupled_radial_frequency_squared_lower_bound(
                fixed_wall_static_form_gap=0.0,
                kinetic_weight_upper_bound=25.0,
                normalized_wall_mass=0.2,
                normalized_branch_curvature=0.3,
                branch_lift_weighted_norm_squared=0.0,
            )
        with self.assertRaises(ValueError):
            coupled_radial_frequency_squared_lower_bound(
                fixed_wall_static_form_gap=1.0,
                kinetic_weight_upper_bound=25.0,
                normalized_wall_mass=0.2,
                normalized_branch_curvature=0.3,
                branch_lift_weighted_norm_squared=-1.0,
            )


if __name__ == "__main__":
    unittest.main()
