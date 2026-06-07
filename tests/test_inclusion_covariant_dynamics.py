import unittest

from qgtoy.inclusion_covariant_dynamics import (
    canonical_block_covariance_audit,
    covariance_asymptotic_bound,
    covariance_family_records,
    inclusion_covariant_static_patch_dynamics_certificate,
)


class InclusionCovariantDynamicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = inclusion_covariant_static_patch_dynamics_certificate(
            max_level=4,
            max_consecutive_cutoff=5,
            bridge_cert_max_cutoff=5,
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
            "asymptotic_inclusion_covariant_generator_theorem_candidate",
        )

    def test_exact_covariance_fails_at_finite_levels(self):
        for record in self.certificate["covariance_family"]["records"]:
            exact = record["exact_covariance"]
            self.assertFalse(
                exact["modular_commutator_generator_exactly_covariant"]
            )
            self.assertGreater(exact["operator_norm_error_bound"], 0.0)

    def test_conditional_and_exact_errors_decrease(self):
        family = self.certificate["covariance_family"]
        exact = family["exact_modular_errors"]
        conditional = family["conditional_modular_errors"]
        heat = family["exact_heat_errors"]
        self.assertGreater(exact[0], exact[-1])
        self.assertGreater(conditional[0], conditional[-1])
        self.assertGreater(heat[0], heat[-1])
        self.assertTrue(
            self.certificate["certified_claims"][
                "conditional_covariance_errors_decrease"
            ]
        )

    def test_asymptotic_bound_covers_family(self):
        for record in self.certificate["covariance_family"]["records"]:
            geometry = record["rank_ordered_energy_geometry"]
            self.assertTrue(geometry["exact_error_below_asymptotic_bound"])
            self.assertTrue(geometry["conditional_error_below_asymptotic_bound"])
            self.assertLessEqual(
                record["exact_covariance"]["operator_norm_error_bound"],
                geometry["asymptotic_error_bound"],
            )
        self.assertEqual(covariance_asymptotic_bound(1), 1.0)

    def test_short_time_semigroup_bounds_decrease(self):
        family = self.certificate["covariance_family"]
        modular = family["modular_channel_bounds"]
        heat = family["heat_channel_bounds"]
        self.assertGreater(modular[0], modular[-1])
        self.assertGreater(heat[0], heat[-1])
        self.assertTrue(
            self.certificate["certified_claims"][
                "short_time_semigroup_covariance_bounds_decrease"
            ]
        )

    def test_dephased_control_and_bridge_claims(self):
        claims = self.certificate["certified_claims"]
        self.assertTrue(claims["dephased_screen_dynamics_exactly_covariant"])
        self.assertTrue(claims["bridge_diagnostic_preserved"])
        self.assertTrue(claims["not_claimed_as_continuum_ds_er_epr"])

    def test_single_level_audit_shape(self):
        audit = canonical_block_covariance_audit(2, noise_strength=1.0)
        self.assertEqual(audit["source_cutoff_L"], 5)
        self.assertEqual(audit["target_cutoff_L"], 23)
        self.assertEqual(audit["multiplicity"], 16)
        self.assertIn(
            "id tensor normalized_trace_on_fiber",
            audit["conditional_expectation_covariance"]["conditional_expectation"],
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(max_level=2)
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(
                max_consecutive_cutoff=0,
            )
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(
                bridge_cert_max_cutoff=0,
            )
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(
                noise_strength=-1.0,
            )
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(fixed_lapse=0.0)
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(
                environment_qubits=0,
            )
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(
                temperature_scale=0.0,
            )
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(
                screen_probability=2.0,
            )
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(low_order=-1)
        with self.assertRaises(ValueError):
            inclusion_covariant_static_patch_dynamics_certificate(
                perturbation_radius=1.0,
            )


if __name__ == "__main__":
    unittest.main()
