import unittest

from qgtoy.static_patch_testbed import (
    goal23_regulated_static_patch_ds_cft_certificate,
    mode_count,
    regulated_kernel_summary,
    regulated_static_patch_collision_record,
    static_patch_mode_labels,
)


class RegulatedStaticPatchDsCftTestbedTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal23_regulated_static_patch_ds_cft_certificate(
            max_cutoff=4,
            screen_probability=0.75,
            low_order=2,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_cutoff_spherical_mode_algebra(self):
        labels = static_patch_mode_labels(2)
        self.assertEqual(len(labels), 9)
        self.assertEqual(mode_count(3), 16)
        self.assertIn((2, -2), labels)
        self.assertIn((2, 2), labels)

    def test_regulated_kernel_has_explicit_cutoff_error(self):
        quantum = regulated_kernel_summary(
            2,
            offdiag_coupling=1,
            screen_probability=0.75,
        )
        classical = regulated_kernel_summary(
            2,
            offdiag_coupling=0,
            screen_probability=0.75,
        )
        self.assertEqual(quantum["shared_horizon_algebra"], "C^9")
        self.assertEqual(
            quantum["cptp_oaqec_definition"]["epsilon_recoverable_bridge_algebra"],
            "M_9",
        )
        self.assertEqual(
            classical["cptp_oaqec_definition"]["epsilon_recoverable_bridge_algebra"],
            "C^9",
        )
        self.assertGreater(
            quantum["kernel_bounds"]["geometric_resolution_error"],
            0.0,
        )
        self.assertLess(
            quantum["kernel_bounds"]["geometric_resolution_error"],
            1.0,
        )

    def test_screen_visible_data_are_insufficient_at_cutoff(self):
        record = regulated_static_patch_collision_record(
            3,
            screen_probability=0.75,
            low_order=2,
        )
        insufficient = record["proposed_ds_cft_visible_data_insufficient"]
        self.assertTrue(insufficient["entropy_shadows_match"])
        self.assertTrue(insufficient["low_order_correlators_match"])
        self.assertTrue(insufficient["screen_restricted_transfer_data_match"])
        self.assertTrue(insufficient["bridge_algebras_differ_at_cutoff_tolerance"])

    def test_intrinsic_response_determines_bridge(self):
        record = regulated_static_patch_collision_record(
            3,
            screen_probability=0.75,
            low_order=2,
        )
        response = record["relative_entropy_response"]
        growth = record["modular_commutator_otoc_growth"]
        bridge = record["induced_observer_bridge_channel"]
        self.assertGreater(response["response_gap_lower_bound_bits"], 0.0)
        self.assertGreater(
            response["quantum_response_retention_lower_bound"],
            0.0,
        )
        self.assertTrue(growth["off_diagonal_modular_response_separates"])
        self.assertTrue(growth["otoc_style_growth_separates"])
        self.assertTrue(bridge["bridge_channel_determined_by_full_intrinsic_response"])
        self.assertEqual(bridge["quantum_bridge_epsilon_recoverable_algebra"], "M_16")
        self.assertEqual(bridge["classical_bridge_epsilon_recoverable_algebra"], "C^16")

    def test_bounded_cutoff_family_and_zero_geometry_limit(self):
        family = self.certificate["bounded_cutoff_family"]
        self.assertEqual(family["cutoffs_checked"], (1, 2, 3, 4))
        self.assertTrue(family["all_screen_visible_data_collide"])
        self.assertTrue(family["all_bridge_channels_differ"])
        self.assertTrue(family["all_intrinsic_completions_determine_bridge"])
        self.assertTrue(self.certificate["zero_geometry_limit"]["recovers_goal22"])

    def test_continuum_gate_blocks_overclaiming(self):
        gate = self.certificate["continuum_gate"]
        self.assertEqual(gate["status"], "not_passed")
        self.assertEqual(
            len(gate["required_before_continuum_ds_cft_claim"]),
            7,
        )
        self.assertIn("not claim continuum dS/CFT", gate["claim_boundary"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            static_patch_mode_labels(0)
        with self.assertRaises(ValueError):
            goal23_regulated_static_patch_ds_cft_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            regulated_static_patch_collision_record(
                1,
                screen_probability=1.5,
                low_order=2,
            )
        with self.assertRaises(ValueError):
            regulated_static_patch_collision_record(
                1,
                screen_probability=0.75,
                low_order=-1,
            )


if __name__ == "__main__":
    unittest.main()
