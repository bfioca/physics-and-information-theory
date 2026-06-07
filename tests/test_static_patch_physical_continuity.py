import unittest

from qgtoy.static_patch_physical_continuity import (
    finite_lapse_error_bound,
    goal30_static_patch_physical_continuity_certificate,
    heat_step_error_bound,
    physical_continuity_route_atlas,
    static_patch_max_energy_gap,
)


class StaticPatchPhysicalContinuityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal30_static_patch_physical_continuity_certificate(
            max_cutoff=5,
            noise_strength=1.0,
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
            "finite_physical_continuity_gate",
        )

    def test_goal29_obstruction_is_retained(self):
        self.assertTrue(
            self.certificate["certified_claims"]["goal29_obstruction_retained"]
        )
        self.assertTrue(
            self.certificate["certified_claims"][
                "kms_and_thermal_decay_alone_refuted"
            ]
        )
        negative = [
            row
            for row in self.certificate["route_atlas"]
            if row["route_kind"] == "negative_no_go"
        ]
        self.assertEqual(len(negative), 2)
        for row in negative:
            self.assertFalse(row["continuity_certified"])
            self.assertTrue(row["anti_tautological"])

    def test_positive_physical_gates_certify_continuity(self):
        positive = [
            row
            for row in self.certificate["route_atlas"]
            if row["route_kind"] == "positive_sufficient"
        ]
        self.assertEqual(
            {row["route_id"] for row in positive},
            {
                "finite_lapse_modular_locality",
                "fuzzy_sphere_local_heat_scaling",
                "euclidean_cap_shrinking_thickness",
            },
        )
        for row in positive:
            self.assertTrue(row["continuity_certified"])
            self.assertTrue(row["anti_tautological"])
            self.assertTrue(
                row["bridge_diagnostic_preserved_for_selected_regulators"]
            )
            self.assertTrue(row["stability_preserved_for_selected_regulators"])

    def test_operator_algebra_limit_is_conditional_not_a_continuum_claim(self):
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
        self.assertIn("Finite physical continuity gate", self.certificate["claim_boundary"])

    def test_bounds_decrease_across_bounded_family(self):
        family = self.certificate["bounded_cutoff_family"]
        self.assertTrue(family["finite_lapse_bound_decreases"])
        self.assertTrue(family["heat_step_bound_decreases"])
        lapse = family["finite_lapse_bounds"]
        heat = family["heat_step_bounds"]
        self.assertGreater(lapse[0], lapse[-1])
        self.assertGreater(heat[0], heat[-1])

    def test_error_bound_helpers_are_consistent(self):
        cutoff = 3
        gap = static_patch_max_energy_gap(cutoff)
        self.assertGreater(gap, 0.0)
        self.assertLess(
            heat_step_error_bound(cutoff, noise_strength=1.0),
            finite_lapse_error_bound(cutoff, noise_strength=1.0),
        )

    def test_route_atlas_uses_requested_knobs(self):
        atlas = physical_continuity_route_atlas(
            cutoff=3,
            noise_strength=0.25,
            environment_qubits=6,
            temperature_scale=2.0,
            screen_probability=0.6,
            low_order=1,
            perturbation_radius=0.02,
        )
        positive = [row for row in atlas if row["route_kind"] == "positive_sufficient"]
        for row in positive:
            self.assertTrue(row["continuity_certified"])
            for record in row["selected_regulator_records"]:
                quantum = record["channel_audits"]["quantum"]
                self.assertEqual(
                    quantum["perturbations"]["coupling_multiplier"],
                    1.0,
                )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal30_static_patch_physical_continuity_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            goal30_static_patch_physical_continuity_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            goal30_static_patch_physical_continuity_certificate(environment_qubits=0)
        with self.assertRaises(ValueError):
            goal30_static_patch_physical_continuity_certificate(temperature_scale=0.0)
        with self.assertRaises(ValueError):
            goal30_static_patch_physical_continuity_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            goal30_static_patch_physical_continuity_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            goal30_static_patch_physical_continuity_certificate(
                perturbation_radius=1.0,
            )


if __name__ == "__main__":
    unittest.main()
