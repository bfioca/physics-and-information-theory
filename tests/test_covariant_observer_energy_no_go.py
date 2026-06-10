import unittest

from qgtoy.covariant_observer_energy_no_go import (
    casimir_hamiltonian_assignment,
    covariant_observer_energy_no_go_certificate,
    covariant_observer_energy_no_go_record,
)


class CovariantObserverEnergyNoGoTest(unittest.TestCase):
    def test_assignment_realizes_arbitrary_positive_excitation_energy(self):
        for cutoff in (1, 4, 20, 100):
            for energy in (0.01, 1.0, 123.5):
                assignment = casimir_hamiltonian_assignment(
                    cutoff,
                    prescribed_token_excitation_energy=energy,
                )
                self.assertAlmostEqual(
                    assignment["realized_token_excitation_energy"],
                    energy,
                )
                self.assertGreater(assignment["casimir_coefficient_a_J"], 0.0)
                self.assertGreater(
                    assignment["equivalent_rotor_moment_of_inertia_I_J"],
                    0.0,
                )

    def test_same_channel_supports_incompatible_energy_profiles(self):
        record = covariant_observer_energy_no_go_record(
            radius=1.0,
            stretched_distance=1.0 / 4096.0,
            field_energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
            target_recovery_error=0.1,
            energy_scale=2.0,
            fixed_moment_of_inertia=1.0,
        )
        assignments = record["prescribed_energy_hamiltonians"]
        self.assertEqual(
            assignments["constant"]["reference_cutoff_J"],
            assignments["inverse_gap_squared"]["reference_cutoff_J"],
        )
        self.assertAlmostEqual(
            assignments["constant"]["realized_token_excitation_energy"],
            2.0,
        )
        self.assertAlmostEqual(
            assignments["inverse_gap"]["realized_token_excitation_energy"],
            2.0 * 4096.0,
        )
        self.assertLessEqual(
            record["charged_reference_constructive_diamond_error_upper_bound"],
            0.1,
        )

    def test_certificate(self):
        certificate = covariant_observer_energy_no_go_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("non-identifiability", certificate["claim_boundary"])
        self.assertIn("finite-size", certificate["required_physics_replacement"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            casimir_hamiltonian_assignment(
                0,
                prescribed_token_excitation_energy=1.0,
            )
        with self.assertRaises(ValueError):
            casimir_hamiltonian_assignment(
                1,
                prescribed_token_excitation_energy=0.0,
            )
        with self.assertRaises(ValueError):
            covariant_observer_energy_no_go_certificate(steps=2)


if __name__ == "__main__":
    unittest.main()
