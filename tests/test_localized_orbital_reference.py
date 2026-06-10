import math
import unittest

from qgtoy.localized_orbital_reference import (
    compactness_limited_orbital_casimir_capacity,
    compactness_limited_orbital_heat_risk_lower_bound,
    compactness_limited_orbital_orientation_risk_floors,
    confined_orbital_observer_tradeoff_record,
    confined_orbital_casimir_capacity,
    confined_orbital_orientation_risk_floors,
    high_spin_tail_probability_upper_bound,
    localized_orbital_reference_certificate,
    mean_spin_capacity_from_casimir,
    minimum_compactness_limited_orbital_radius_for_heat_risk,
    orientation_risk_floors_from_casimir_capacity,
)


class LocalizedOrbitalReferenceTest(unittest.TestCase):
    def test_quadratic_form_capacity_factor(self):
        self.assertAlmostEqual(
            confined_orbital_casimir_capacity(
                total_rest_mass=2.0,
                support_radius=0.25,
                mean_excitation_energy=0.5,
            ),
            0.125,
        )

    def test_risk_composition_uses_capacity_as_upper_bound(self):
        risk = confined_orbital_orientation_risk_floors(
            total_rest_mass=2.0,
            support_radius=0.25,
            mean_excitation_energy=0.5,
        )
        self.assertAlmostEqual(risk["direct_fusion_risk_lower_bound"], 0.1)
        self.assertGreater(risk["information_risk_lower_bound"], 0.0)
        self.assertEqual(
            risk["strongest_risk_lower_bound"],
            max(
                risk["direct_fusion_risk_lower_bound"],
                risk["information_risk_lower_bound"],
            ),
        )

    def test_mean_spin_jensen_conversion(self):
        for capacity in (0.0, 0.75, 2.0, 6.0, 20.0):
            mean_spin = mean_spin_capacity_from_casimir(capacity)
            self.assertLessEqual(mean_spin * (mean_spin + 1.0), capacity + 1e-14)

    def test_rare_tail_bound_closes_remote_spin_loophole(self):
        capacity = 3.0
        bounds = [
            high_spin_tail_probability_upper_bound(
                mean_casimir_capacity=capacity,
                reference_cutoff=cutoff,
            )
            for cutoff in (0, 1, 3, 7, 15, 31)
        ]
        self.assertEqual(bounds[0], 1.0)
        self.assertTrue(all(right < left for left, right in zip(bounds, bounds[1:])))
        self.assertAlmostEqual(bounds[-1], 3.0 / (32.0 * 33.0))

    def test_compactness_elimination_optimizes_rest_excitation_split(self):
        capacity = compactness_limited_orbital_casimir_capacity(
            support_radius=0.25,
            newton_constant=0.01,
            compactness_margin=0.2,
        )
        total_energy_ceiling = 0.2 * 0.25 / (2.0 * 0.01)
        expected = 0.25**2 * total_energy_ceiling**2 / 2.0
        self.assertAlmostEqual(capacity, expected)
        risk = compactness_limited_orbital_orientation_risk_floors(
            support_radius=0.25,
            newton_constant=0.01,
            compactness_margin=0.2,
        )
        self.assertAlmostEqual(
            risk["direct_fusion_risk_lower_bound"],
            1.0 / (8.0 + 2.0 * 0.2**2 * 0.25**4 / 0.01**2),
        )

    def test_zero_capacity_and_large_capacity_are_stable(self):
        zero = orientation_risk_floors_from_casimir_capacity(0.0)
        large = orientation_risk_floors_from_casimir_capacity(1e12)
        self.assertAlmostEqual(zero["direct_fusion_risk_lower_bound"], 0.125)
        self.assertGreater(zero["information_risk_lower_bound"], 0.0)
        self.assertGreater(large["strongest_risk_lower_bound"], 0.0)

    def test_compactness_support_and_heat_exposure_compose_exactly(self):
        initial = compactness_limited_orbital_orientation_risk_floors(
            support_radius=0.25,
            newton_constant=0.01,
            compactness_margin=0.2,
        )["direct_fusion_risk_lower_bound"]
        exposure = 0.1
        attenuation = math.exp(-2.0 * exposure)
        expected = 0.75 * (1.0 - attenuation) + attenuation * initial
        self.assertAlmostEqual(
            compactness_limited_orbital_heat_risk_lower_bound(
                support_radius=0.25,
                newton_constant=0.01,
                compactness_margin=0.2,
                rotational_noise_exposure=exposure,
            ),
            expected,
        )

    def test_minimum_radius_inverts_heat_risk_floor(self):
        budget = 0.2
        radius = minimum_compactness_limited_orbital_radius_for_heat_risk(
            budget,
            newton_constant=0.01,
            compactness_margin=0.2,
            rotational_noise_exposure=0.1,
        )
        self.assertGreater(radius, 0.0)
        self.assertAlmostEqual(
            compactness_limited_orbital_heat_risk_lower_bound(
                support_radius=radius,
                newton_constant=0.01,
                compactness_margin=0.2,
                rotational_noise_exposure=0.1,
            ),
            budget,
        )
        record = confined_orbital_observer_tradeoff_record(
            maximum_proper_support_radius=radius / 2.0,
            risk_budget=budget,
            newton_constant=0.01,
            compactness_margin=0.2,
            rotational_noise_exposure=0.1,
        )
        self.assertTrue(record["declared_class_excluded"])

    def test_noise_floor_can_exclude_every_support_radius(self):
        radius = minimum_compactness_limited_orbital_radius_for_heat_risk(
            0.01,
            newton_constant=0.01,
            compactness_margin=0.2,
            rotational_noise_exposure=1.0,
        )
        self.assertEqual(radius, float("inf"))

    def test_certificate(self):
        certificate = localized_orbital_reference_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("spinless nonrelativistic", certificate["model_scope"])
        self.assertIn("not a general-relativistic", certificate["claim_boundary"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            confined_orbital_casimir_capacity(
                total_rest_mass=0.0,
                support_radius=1.0,
                mean_excitation_energy=1.0,
            )
        with self.assertRaises(ValueError):
            high_spin_tail_probability_upper_bound(
                mean_casimir_capacity=1.0,
                reference_cutoff=True,
            )
        with self.assertRaises(ValueError):
            compactness_limited_orbital_casimir_capacity(
                support_radius=1.0,
                newton_constant=1.0,
                compactness_margin=1.0,
            )


if __name__ == "__main__":
    unittest.main()
