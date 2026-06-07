import unittest
from math import exp

from qgtoy.static_patch_strong_continuity import (
    fixed_lapse_heat_error_lower_bound,
    goal31_static_patch_strong_continuity_certificate,
    heat_generator_norm_bound,
    heat_short_lapse,
    modular_generator_norm_bound,
    modular_short_lapse,
    semigroup_error_bound,
    strong_continuity_route_atlas,
)


class StaticPatchStrongContinuityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal31_static_patch_strong_continuity_certificate(
            max_cutoff=5,
            noise_strength=1.0,
            fixed_lapse=1.0,
            environment_qubits=4,
            temperature_scale=1.0,
            screen_probability=0.75,
            low_order=2,
            perturbation_radius=0.05,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertEqual(
            self.certificate["result_type"],
            "finite_static_patch_strong_continuity_theorem_gate",
        )

    def test_stationary_twirl_and_fixed_lapse_are_no_go_routes(self):
        atlas = {row["route_id"]: row for row in self.certificate["route_atlas"]}
        stationary = atlas["stationary_twirl_projection"]
        self.assertTrue(stationary["violates_strong_continuity"])
        self.assertEqual(stationary["identity_jump_witness_norm"], 1.0)
        self.assertFalse(stationary["continuity_certified"])

        fixed_lapse = atlas["fixed_lapse_thermalization"]
        self.assertTrue(fixed_lapse["violates_cutoff_compatible_lapse"])
        self.assertGreater(fixed_lapse["fixed_lapse_error_lower_bound"], 0.0)
        self.assertFalse(fixed_lapse["continuity_certified"])

    def test_positive_generator_routes_certify_approximate_identity(self):
        positive = [
            row
            for row in self.certificate["route_atlas"]
            if row["route_kind"] == "positive_theorem"
        ]
        self.assertEqual(
            {row["route_id"] for row in positive},
            {
                "bounded_local_modular_generator",
                "bounded_local_heat_generator",
                "shrinking_euclidean_transfer_generator",
            },
        )
        for row in positive:
            self.assertTrue(row["anti_tautological"])
            self.assertTrue(row["continuity_certified"])
            self.assertTrue(row["derives_modular_time_approximate_identity"])
            self.assertGreater(row["semigroup_error_bound"], 0.0)
            self.assertLess(row["semigroup_error_bound"], 1.0)

    def test_conditional_limit_route_is_not_continuum_claim(self):
        conditional = [
            row
            for row in self.certificate["route_atlas"]
            if row["route_kind"] == "conditional_necessity"
        ]
        self.assertEqual(len(conditional), 1)
        self.assertTrue(conditional[0]["continuity_certified"])
        self.assertTrue(
            self.certificate["certified_claims"][
                "not_claimed_as_continuum_ds_er_epr"
            ]
        )
        self.assertIn("Finite semigroup theorem gate", self.certificate["claim_boundary"])

    def test_generator_products_decrease_across_bounded_family(self):
        family = self.certificate["bounded_cutoff_family"]
        self.assertTrue(family["modular_products_decrease"])
        self.assertTrue(family["heat_products_decrease"])
        modular = family["modular_lapse_times_generator"]
        heat = family["heat_lapse_times_generator"]
        self.assertGreater(modular[0], modular[-1])
        self.assertGreater(heat[0], heat[-1])

    def test_helper_bounds_match_theorem_shape(self):
        cutoff = 3
        modular_product = (
            modular_short_lapse(cutoff, noise_strength=1.0)
            * modular_generator_norm_bound(cutoff)
        )
        heat_product = (
            heat_short_lapse(cutoff, noise_strength=1.0)
            * heat_generator_norm_bound(cutoff)
        )
        self.assertLess(heat_product, modular_product)
        self.assertAlmostEqual(
            semigroup_error_bound(
                modular_short_lapse(cutoff, noise_strength=1.0),
                modular_generator_norm_bound(cutoff),
            ),
            exp(modular_product) - 1.0,
        )
        self.assertGreater(
            fixed_lapse_heat_error_lower_bound(cutoff, fixed_lapse=1.0),
            0.0,
        )

    def test_route_atlas_uses_noise_strength(self):
        weak = strong_continuity_route_atlas(
            cutoff=3,
            noise_strength=0.25,
            fixed_lapse=1.0,
        )
        strong = strong_continuity_route_atlas(
            cutoff=3,
            noise_strength=1.0,
            fixed_lapse=1.0,
        )
        weak_modular = {
            row["route_id"]: row for row in weak
        }["bounded_local_modular_generator"]
        strong_modular = {
            row["route_id"]: row for row in strong
        }["bounded_local_modular_generator"]
        self.assertLess(
            weak_modular["modular_lapse_times_generator"],
            strong_modular["modular_lapse_times_generator"],
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(fixed_lapse=0.0)
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(environment_qubits=0)
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(temperature_scale=0.0)
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            goal31_static_patch_strong_continuity_certificate(
                perturbation_radius=1.0,
            )


if __name__ == "__main__":
    unittest.main()
