import unittest

from qgtoy.static_patch_regulator_universality import (
    ACCEPTED_REGULATOR_IDS,
    goal27_static_patch_regulator_universality_certificate,
    static_patch_regulator_candidate_atlas,
    static_patch_regulator_channel_audit,
    static_patch_regulator_coefficient,
    static_patch_regulator_collision_record,
    static_patch_regulator_spec,
    static_patch_regulator_stability_audit,
)


class StaticPatchRegulatorUniversalityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal27_static_patch_regulator_universality_certificate(
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
            "finite_regulator_universality_success",
        )

    def test_nontrivial_regulator_class_declared(self):
        self.assertEqual(len(ACCEPTED_REGULATOR_IDS), 4)
        accepted = {
            row["regulator_id"] for row in self.certificate["accepted_regulators"]
        }
        self.assertEqual(accepted, set(ACCEPTED_REGULATOR_IDS))
        for regulator_id in ACCEPTED_REGULATOR_IDS:
            spec = static_patch_regulator_spec(regulator_id)
            self.assertTrue(spec.derivation_class)
            self.assertTrue(spec.positive_definite_source)

    def test_channel_audits_are_cptp(self):
        for regulator_id in ACCEPTED_REGULATOR_IDS:
            audit = static_patch_regulator_channel_audit(
                3,
                regulator_id=regulator_id,
                noise_strength=1.0,
                environment_qubits=4,
                temperature_scale=1.0,
            )
            self.assertTrue(audit["channel_properties"]["complete_positive"])
            self.assertTrue(audit["channel_properties"]["trace_preserving"])
            self.assertTrue(audit["channel_properties"]["unital"])
            self.assertTrue(audit["channel_properties"]["cptp_unital"])
            self.assertTrue(audit["coefficient_matrix"]["positive_semidefinite_numeric"])

    def test_classical_control_dephases_offdiagonal(self):
        coefficient = static_patch_regulator_coefficient(
            2,
            (0, 0),
            (1, 0),
            regulator_id="fuzzy_laplacian_lindblad_heat",
            noise_strength=1.0,
            environment_qubits=4,
            temperature_scale=1.0,
            classical_dephase=True,
        )
        self.assertEqual(coefficient, 0.0)

    def test_collision_record_separates_bridge_algebra(self):
        for regulator_id in ACCEPTED_REGULATOR_IDS:
            record = static_patch_regulator_collision_record(
                3,
                regulator_id=regulator_id,
                noise_strength=1.0,
                environment_qubits=4,
                temperature_scale=1.0,
                screen_probability=0.75,
                low_order=2,
            )
            self.assertEqual(record["mode_count"], 16)
            self.assertTrue(record["screen_visible_data_insufficient"]["entropy_shadows_match"])
            self.assertTrue(
                record["screen_visible_data_insufficient"][
                    "screen_restricted_transfer_data_match"
                ]
            )
            self.assertEqual(
                record["induced_observer_bridge_channel"][
                    "quantum_bridge_epsilon_recoverable_algebra"
                ],
                "M_16",
            )
            self.assertEqual(
                record["induced_observer_bridge_channel"][
                    "classical_bridge_epsilon_recoverable_algebra"
                ],
                "C^16",
            )
            self.assertGreater(
                record["off_diagonal_response"]["response_gap_lower_bound_bits"],
                0.0,
            )
            self.assertGreaterEqual(
                record["off_diagonal_response"]["epsilon_bound"],
                record["off_diagonal_response"]["cutoff_error_epsilon"],
            )

    def test_perturbation_stability_audit(self):
        audit = static_patch_regulator_stability_audit(
            3,
            regulator_id="kms_modular_cauchy_average",
            noise_strength=1.0,
            environment_qubits=4,
            temperature_scale=1.0,
            screen_probability=0.75,
            low_order=2,
            perturbation_radius=0.05,
        )
        self.assertTrue(audit["all_variants_preserve_diagnostic"])
        variant_ids = {row["variant_id"] for row in audit["variants"]}
        self.assertIn("spectrum_plus", variant_ids)
        self.assertIn("coupling_minus", variant_ids)
        self.assertIn("kms_temperature_plus", variant_ids)
        self.assertIn("cutoff_geometry_minus", variant_ids)

    def test_candidate_atlas_records_obstructions(self):
        atlas = static_patch_regulator_candidate_atlas(
            cutoff=3,
            noise_strength=1.0,
            environment_qubits=4,
            temperature_scale=1.0,
            screen_probability=0.75,
            low_order=2,
            perturbation_radius=0.05,
        )
        statuses = {row["status"] for row in atlas}
        self.assertIn("success_universality_class_member", statuses)
        self.assertIn(
            "rejected_controlled_nonunitary_not_screen_shadow_preserving",
            statuses,
        )
        self.assertIn(
            "obstruction_no_operator_response_or_channel_completion",
            statuses,
        )

    def test_scaling_bounds_decrease_for_accepted_regulators(self):
        for regulator_id in ACCEPTED_REGULATOR_IDS:
            previous = None
            for cutoff in range(1, 5):
                record = static_patch_regulator_collision_record(
                    cutoff,
                    regulator_id=regulator_id,
                    noise_strength=1.0,
                    environment_qubits=4,
                    temperature_scale=1.0,
                    screen_probability=0.75,
                    low_order=2,
                )
                bound = record["off_diagonal_response"]["epsilon_bound"]
                if previous is not None:
                    self.assertLess(bound, previous)
                previous = bound

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal27_static_patch_regulator_universality_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            goal27_static_patch_regulator_universality_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            goal27_static_patch_regulator_universality_certificate(environment_qubits=0)
        with self.assertRaises(ValueError):
            goal27_static_patch_regulator_universality_certificate(temperature_scale=0.0)
        with self.assertRaises(ValueError):
            goal27_static_patch_regulator_universality_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            goal27_static_patch_regulator_universality_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            goal27_static_patch_regulator_universality_certificate(
                perturbation_radius=1.0,
            )
        with self.assertRaises(ValueError):
            static_patch_regulator_spec("not_a_regulator")


if __name__ == "__main__":
    unittest.main()
