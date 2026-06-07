import unittest

from qgtoy.derived_static_patch_dynamics import (
    derived_phase_kick_channel_audit,
    derived_phase_kick_coefficient,
    derived_phase_kick_coefficient_matrix,
    derived_static_patch_candidate_atlas,
    derived_static_patch_collision_record,
    finite_environment_phase_kick,
    goal26_derived_static_patch_dynamics_certificate,
)


class DerivedStaticPatchDynamicsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal26_derived_static_patch_dynamics_certificate(
            max_cutoff=5,
            noise_strength=1.0,
            environment_qubits=4,
            screen_probability=0.75,
            low_order=2,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_finite_environment_phase_kick_scales(self):
        first = finite_environment_phase_kick(
            2,
            noise_strength=1.0,
            environment_qubits=4,
        )
        second = finite_environment_phase_kick(
            5,
            noise_strength=1.0,
            environment_qubits=4,
        )
        self.assertGreater(first, second)
        self.assertAlmostEqual(first, 1.0 / 6.0)

    def test_derived_channel_audit_is_random_unitary_cptp(self):
        audit = derived_phase_kick_channel_audit(
            3,
            noise_strength=1.0,
            environment_qubits=4,
        )
        self.assertEqual(
            audit["derivation"]["type"],
            "finite_environment_random_unitary_trace",
        )
        self.assertEqual(audit["derivation"]["environment_dimension"], 16)
        self.assertTrue(audit["channel_properties"]["complete_positive"])
        self.assertTrue(audit["channel_properties"]["trace_preserving"])
        self.assertTrue(audit["channel_properties"]["unital"])
        self.assertTrue(audit["channel_properties"]["cptp_unital"])
        self.assertTrue(audit["coefficient_matrix"]["positive_semidefinite_numeric"])

    def test_coefficient_matrix_and_classical_control(self):
        matrix = derived_phase_kick_coefficient_matrix(
            2,
            noise_strength=1.0,
            environment_qubits=4,
        )
        self.assertEqual(len(matrix), 9)
        for index in range(9):
            self.assertAlmostEqual(matrix[index][index], 1.0)

        labels = ((0, 0), (1, 0))
        self.assertEqual(
            derived_phase_kick_coefficient(
                2,
                labels[0],
                labels[1],
                noise_strength=1.0,
                environment_qubits=4,
                classical_dephase=True,
            ),
            0.0,
        )

    def test_screen_shadow_collision_and_bridge_distinction(self):
        record = derived_static_patch_collision_record(
            3,
            noise_strength=1.0,
            environment_qubits=4,
            screen_probability=0.75,
            low_order=2,
        )
        self.assertTrue(record["derived_dynamics"]["small_angle_domain_certified"])
        self.assertTrue(
            record["induced_observer_bridge_channel"][
                "bridge_channel_derived_from_explicit_finite_dynamics"
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
        self.assertTrue(
            record["screen_visible_data_insufficient"][
                "screen_restricted_transfer_data_match"
            ]
        )
        self.assertGreater(
            record["off_diagonal_response"]["response_gap_lower_bound_bits"],
            0.0,
        )

    def test_scaling_bound_and_goal25_approximation(self):
        previous = None
        for cutoff in range(1, 6):
            record = derived_static_patch_collision_record(
                cutoff,
                noise_strength=1.0,
                environment_qubits=4,
                screen_probability=0.75,
                low_order=2,
            )
            bound = record["off_diagonal_response"]["epsilon_bound"]
            self.assertGreaterEqual(
                bound,
                record["off_diagonal_response"]["cutoff_error_epsilon"],
            )
            self.assertGreaterEqual(
                record["off_diagonal_response"][
                    "goal25_lindblad_approximation_max_error"
                ],
                0.0,
            )
            if previous is not None:
                self.assertLess(bound, previous)
            previous = bound

    def test_candidate_atlas_records_success_partials_and_rejection(self):
        atlas = derived_static_patch_candidate_atlas(
            cutoff=3,
            noise_strength=1.0,
            environment_qubits=4,
        )
        statuses = {row["status"] for row in atlas}
        self.assertIn("success_derived_finite_dynamics", statuses)
        self.assertIn("recovered_as_many_kick_limit_not_finite_environment_exact", statuses)
        self.assertIn("partial_success_no_environment_trace_or_dephasing_scaling", statuses)
        self.assertIn("rejected_without_stinespring_or_normalized_channel_completion", statuses)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            goal26_derived_static_patch_dynamics_certificate(max_cutoff=0)
        with self.assertRaises(ValueError):
            goal26_derived_static_patch_dynamics_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            goal26_derived_static_patch_dynamics_certificate(environment_qubits=0)
        with self.assertRaises(ValueError):
            goal26_derived_static_patch_dynamics_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            goal26_derived_static_patch_dynamics_certificate(low_order=-1)


if __name__ == "__main__":
    unittest.main()
