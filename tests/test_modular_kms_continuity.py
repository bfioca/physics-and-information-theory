import unittest

from qgtoy.modular_kms_continuity import (
    goal29_modular_kms_continuity_certificate,
    localized_modular_width,
    modular_kms_model_atlas,
    modular_kms_model_audit,
    modular_kms_model_catalog,
    modular_kms_obstruction_audit,
)
from qgtoy.static_patch_regulator_universality import ACCEPTED_REGULATOR_IDS


class ModularKMSContinuityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal29_modular_kms_continuity_certificate(
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
            "kms_alone_refuted_modular_approximate_identity_sufficient",
        )

    def test_selected_models_match_goal28_regulators(self):
        selected = {
            row["regulator_id"]
            for row in self.certificate["selected_modular_kms_models"]
        }
        self.assertEqual(selected, set(ACCEPTED_REGULATOR_IDS))
        self.assertEqual(len(selected), 4)

    def test_localized_widths_vanish(self):
        for model in self.certificate["selected_modular_kms_models"]:
            first = localized_modular_width(
                model["model_id"],
                1,
                noise_strength=1.0,
                environment_qubits=4,
                temperature_scale=1.0,
            )
            later = localized_modular_width(
                model["model_id"],
                5,
                noise_strength=1.0,
                environment_qubits=4,
                temperature_scale=1.0,
            )
            self.assertIsNotNone(first)
            self.assertIsNotNone(later)
            self.assertLess(later, first)

    def test_selected_models_have_kms_continuity_and_bridge(self):
        catalog = {
            model.model_id: model
            for model in modular_kms_model_catalog()
            if model.regulator_id is not None
        }
        for model in catalog.values():
            audit = modular_kms_model_audit(
                model,
                cutoff=3,
                noise_strength=1.0,
                environment_qubits=4,
                temperature_scale=1.0,
                screen_probability=0.75,
                low_order=2,
                perturbation_radius=0.05,
            )
            self.assertEqual(
                audit["status"],
                "selected_modular_kms_continuous_regulator",
            )
            self.assertTrue(audit["modular_kms_checks"]["kms_detailed_balance"])
            self.assertTrue(audit["detailed_balance_audit"]["detailed_balance_certified"])
            self.assertTrue(audit["continuity_certified"])
            self.assertTrue(audit["bridge_diagnostic_certified"])

    def test_kms_alone_counterexamples_are_recorded(self):
        atlas = modular_kms_model_atlas(
            cutoff=3,
            noise_strength=1.0,
            environment_qubits=4,
            temperature_scale=1.0,
            screen_probability=0.75,
            low_order=2,
            perturbation_radius=0.05,
        )
        rows = {row["model_id"]: row for row in atlas}
        stationary = rows["stationary_modular_twirl_total_dephasing"]
        self.assertTrue(stationary["modular_kms_checks"]["kms_detailed_balance"])
        self.assertTrue(stationary["modular_kms_checks"]["cptp_unital"])
        self.assertTrue(stationary["modular_kms_checks"]["diagonal_screen_preserving"])
        self.assertFalse(stationary["modular_kms_checks"]["approximate_identity"])
        self.assertEqual(
            stationary["status"],
            "refutes_kms_detailed_balance_alone",
        )

        fixed_width = rows["fixed_width_modular_noise"]
        self.assertTrue(fixed_width["modular_kms_checks"]["kms_detailed_balance"])
        self.assertFalse(fixed_width["modular_kms_checks"]["cutoff_localized"])
        self.assertEqual(
            fixed_width["status"],
            "refutes_kms_detailed_balance_alone",
        )

    def test_obstruction_audit_identifies_extra_assumption(self):
        audit = modular_kms_obstruction_audit(
            modular_kms_model_atlas(
                cutoff=3,
                noise_strength=1.0,
                environment_qubits=4,
                temperature_scale=1.0,
                screen_probability=0.75,
                low_order=2,
                perturbation_radius=0.05,
            )
        )
        claims = {row["claim"]: row for row in audit}
        self.assertIn("kms_detailed_balance_alone_does_not_force_continuity", claims)
        self.assertIn("shrinking_modular_time_width_is_needed", claims)
        self.assertEqual(
            claims["shrinking_modular_time_width_is_needed"]["status"],
            "refutes_kms_detailed_balance_alone",
        )

    def test_bounded_family_preserves_goal28_diagnostic(self):
        family = self.certificate["bounded_cutoff_family"]
        self.assertTrue(family["all_kms_detailed_balance"])
        self.assertTrue(family["all_continuity_certified"])
        self.assertTrue(family["all_bridge_diagnostics_certified"])
        self.assertTrue(family["all_stability_variants_preserve_bridge_diagnostic"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal29_modular_kms_continuity_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            goal29_modular_kms_continuity_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            goal29_modular_kms_continuity_certificate(environment_qubits=0)
        with self.assertRaises(ValueError):
            goal29_modular_kms_continuity_certificate(temperature_scale=0.0)
        with self.assertRaises(ValueError):
            goal29_modular_kms_continuity_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            goal29_modular_kms_continuity_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            goal29_modular_kms_continuity_certificate(perturbation_radius=1.0)


if __name__ == "__main__":
    unittest.main()
