import math
import unittest
from fractions import Fraction

from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpWorldtubeConstants,
)
from qgtoy.skyrmion_observer_capacity import (
    fixed_profile_projective_capacity_record,
    skyrmion_observer_capacity_certificate,
    validated_fixed_profile_projective_capacity_record,
)


class SkyrmionObserverCapacityTests(unittest.TestCase):
    def test_default_certificate(self):
        certificate = skyrmion_observer_capacity_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_capacity_and_geometry(self):
        record = fixed_profile_projective_capacity_record(
            maximum_compactness=0.5,
            maximum_slow_rotation=0.1,
            static_patch_radius=1.0,
            newton_constant=1.0e-6,
        )
        self.assertEqual(record["maximum_odd_reference_cutoff_J"], 173)
        self.assertGreater(
            record["initial_global_projective_orientation_risk_lower_bound"],
            0.0,
        )
        localization = record["localization"]
        self.assertAlmostEqual(localization["areal_support_radius"], 0.2)
        self.assertAlmostEqual(localization["proper_radial_support"], math.asin(0.2))
        self.assertAlmostEqual(localization["optical_radial_support"], math.atanh(0.2))

    def test_stronger_joint_budget_improves_but_does_not_remove_floor(self):
        base = fixed_profile_projective_capacity_record(
            maximum_compactness=0.2,
            maximum_slow_rotation=0.05,
            static_patch_radius=1.0,
            newton_constant=1.0e-6,
        )
        relaxed = fixed_profile_projective_capacity_record(
            maximum_compactness=0.4,
            maximum_slow_rotation=0.1,
            static_patch_radius=1.0,
            newton_constant=1.0e-6,
        )
        self.assertGreater(
            relaxed["maximum_odd_reference_cutoff_J"],
            base["maximum_odd_reference_cutoff_J"],
        )
        self.assertLess(
            relaxed["initial_global_projective_orientation_risk_lower_bound"],
            base["initial_global_projective_orientation_risk_lower_bound"],
        )
        self.assertGreater(
            relaxed["initial_global_projective_orientation_risk_lower_bound"],
            0.0,
        )

    def test_heat_coherence_floor(self):
        initial = fixed_profile_projective_capacity_record(
            maximum_compactness=0.5,
            maximum_slow_rotation=0.1,
            static_patch_radius=1.0,
            newton_constant=1.0e-6,
        )
        late = fixed_profile_projective_capacity_record(
            maximum_compactness=0.5,
            maximum_slow_rotation=0.1,
            static_patch_radius=1.0,
            newton_constant=1.0e-6,
            dimensionless_diffusion_time=20.0,
        )
        self.assertGreater(
            late["global_orientation_risk_lower_bound_at_time_T"],
            initial["global_orientation_risk_lower_bound_at_time_T"],
        )
        self.assertAlmostEqual(
            late["global_orientation_risk_lower_bound_at_time_T"],
            0.75,
        )

    def test_empty_controlled_sector_does_not_invent_a_risk_floor(self):
        record = fixed_profile_projective_capacity_record(
            maximum_compactness=0.01,
            maximum_slow_rotation=0.01,
            static_patch_radius=1.0,
            newton_constant=1.0,
        )
        self.assertIsNone(record["maximum_odd_reference_cutoff_J"])
        self.assertFalse(record["controlled_projective_sector_feasible"])
        self.assertIsNone(
            record["initial_global_projective_orientation_risk_lower_bound"]
        )
        self.assertIsNone(record["global_orientation_risk_lower_bound_at_time_T"])

    def test_invalid_wall_outside_horizon(self):
        with self.assertRaisesRegex(ValueError, "strictly inside"):
            fixed_profile_projective_capacity_record(
                maximum_compactness=0.5,
                maximum_slow_rotation=0.1,
                static_patch_radius=1.0,
                newton_constant=1.0e-6,
                curvature=0.25,
                wall_radius=4.0,
            )

    def test_directed_mass_inertia_capacity_uses_conservative_endpoints(self):
        constants = ValidatedSkyrmionSharpWorldtubeConstants(
            certificate_id="synthetic-directed-worldtube",
            pion_mass_squared=Fraction(1),
            curvature=Fraction(1, 400),
            wall_radius=Fraction(4),
            interior_mass=RationalInterval(Fraction(40), Fraction(45)),
            shell_mass=RationalInterval(Fraction(1), Fraction(2)),
            total_mass=RationalInterval(Fraction(41), Fraction(47)),
            inertia=RationalInterval(Fraction(20), Fraction(30)),
            claim_boundary="synthetic fixture",
        )
        record = validated_fixed_profile_projective_capacity_record(
            constants,
            maximum_compactness=Fraction(1, 2),
            maximum_slow_rotation=Fraction(1, 10),
            static_patch_radius_squared_over_newton=Fraction(10**6),
        )
        cutoff = record["maximum_odd_reference_cutoff_J"]
        self.assertIsInstance(cutoff, int)
        capacity = Fraction(record["continuous_sqrt_KK1_capacity_upper_exact"])
        self.assertLessEqual(
            Fraction((2 * cutoff + 1) * (2 * cutoff + 3), 4),
            capacity**2,
        )
        self.assertGreater(
            Fraction((2 * cutoff + 3) * (2 * cutoff + 5), 4),
            capacity**2,
        )


if __name__ == "__main__":
    unittest.main()
