import unittest

from qgtoy.physical_static_patch_kernel import (
    default_axis_split,
    fuzzy_static_patch_energy,
    goal25_physical_static_patch_kernel_certificate,
    physical_static_patch_candidate_atlas,
    physical_static_patch_channel_audit,
    physical_static_patch_coefficient,
    physical_static_patch_collision_record,
    physical_static_patch_coefficient_matrix,
    physical_dephasing_time,
)


class PhysicalStaticPatchKernelSearchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = goal25_physical_static_patch_kernel_certificate(
            max_cutoff=5,
            noise_strength=1.0,
            screen_probability=0.75,
            low_order=2,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_fuzzy_static_patch_energy_uses_cutoff_laplacian_spectrum(self):
        split = default_axis_split(3)
        self.assertAlmostEqual(split, 1.0 / 9.0)
        self.assertAlmostEqual(
            fuzzy_static_patch_energy(3, (0, 0)),
            0.0,
        )
        self.assertGreater(
            fuzzy_static_patch_energy(3, (2, 1)),
            fuzzy_static_patch_energy(3, (1, 1)),
        )
        self.assertGreater(
            fuzzy_static_patch_energy(3, (2, 1)),
            fuzzy_static_patch_energy(3, (2, 0)),
        )

    def test_physical_dephasing_channel_is_cptp_unital(self):
        audit = physical_static_patch_channel_audit(
            3,
            noise_strength=1.0,
        )
        props = audit["channel_properties"]
        self.assertTrue(props["complete_positive"])
        self.assertTrue(props["trace_preserving"])
        self.assertTrue(props["unital"])
        self.assertTrue(props["cptp_unital"])
        self.assertTrue(audit["coefficient_matrix"]["positive_semidefinite_numeric"])

        matrix = physical_static_patch_coefficient_matrix(
            2,
            noise_strength=1.0,
        )
        self.assertEqual(len(matrix), 9)
        for index in range(9):
            self.assertAlmostEqual(matrix[index][index], 1.0)

    def test_classical_control_is_cptp_dephasing(self):
        audit = physical_static_patch_channel_audit(
            2,
            noise_strength=1.0,
            classical_dephase=True,
        )
        self.assertTrue(audit["channel_properties"]["cptp_unital"])
        labels = ((0, 0), (1, 0))
        self.assertEqual(
            physical_static_patch_coefficient(
                2,
                labels[0],
                labels[1],
                noise_strength=1.0,
                classical_dephase=True,
            ),
            0.0,
        )

    def test_screen_shadow_collision_and_offdiag_response(self):
        record = physical_static_patch_collision_record(
            3,
            noise_strength=1.0,
            screen_probability=0.75,
            low_order=2,
        )
        self.assertTrue(record["screen_visible_data_insufficient"]["entropy_shadows_match"])
        self.assertTrue(
            record["screen_visible_data_insufficient"]["low_order_correlators_match"]
        )
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

    def test_continuum_scaling_bound_decreases(self):
        previous = None
        for cutoff in range(1, 6):
            record = physical_static_patch_collision_record(
                cutoff,
                noise_strength=1.0,
                screen_probability=0.75,
                low_order=2,
            )
            bound = record["off_diagonal_response"]["epsilon_bound"]
            self.assertGreaterEqual(
                bound,
                record["off_diagonal_response"]["cutoff_error_epsilon"],
            )
            if previous is not None:
                self.assertLess(bound, previous)
            previous = bound
        self.assertLess(
            physical_dephasing_time(5, noise_strength=1.0),
            physical_dephasing_time(2, noise_strength=1.0),
        )

    def test_candidate_atlas_records_success_and_controls(self):
        atlas = physical_static_patch_candidate_atlas(
            cutoff=3,
            noise_strength=1.0,
        )
        statuses = {row["status"] for row in atlas}
        self.assertIn("success_candidate", statuses)
        self.assertIn("partial_success_noncommutative_but_not_full_port_resolved", statuses)
        self.assertIn("rejected_for_bridge_channel_without_tp_unital_completion", statuses)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            physical_static_patch_collision_record(
                0,
                noise_strength=1.0,
                screen_probability=0.75,
                low_order=2,
            )
        with self.assertRaises(ValueError):
            goal25_physical_static_patch_kernel_certificate(noise_strength=-1.0)
        with self.assertRaises(ValueError):
            goal25_physical_static_patch_kernel_certificate(screen_probability=2.0)
        with self.assertRaises(ValueError):
            goal25_physical_static_patch_kernel_certificate(low_order=-1)


if __name__ == "__main__":
    unittest.main()
