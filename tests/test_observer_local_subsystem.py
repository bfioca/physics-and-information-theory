import unittest

from qgtoy.observer_local_subsystem import (
    observer_local_candidate_records,
    observer_local_noncommutative_subsystem_certificate,
    tangent_plane_double_scaling_record,
    tangent_plane_family_records,
)


class ObserverLocalSubsystemTest(unittest.TestCase):
    def test_tangent_plane_commutator_lower_bound(self):
        record = tangent_plane_double_scaling_record(
            cutoff=12,
            excitation_cutoff=2,
        )
        self.assertAlmostEqual(
            record["commutator"]["eigenvalues_on_window"][1],
            5 / 6,
        )
        self.assertAlmostEqual(
            record["commutator"]["eigenvalues_on_window"][2],
            2 / 3,
        )
        self.assertAlmostEqual(record["commutator"]["lower_bound"], 2 / 3)
        self.assertAlmostEqual(record["commutator"]["identity_error_bound"], 1 / 3)
        self.assertTrue(record["commutator"]["nonzero_for_this_cutoff"])
        self.assertGreater(
            record["norm_faithfulness"]["relative_coefficient_lower_bound"],
            0.9,
        )

    def test_tangent_plane_family_bounds_improve(self):
        family = tangent_plane_family_records(max_cutoff=12, excitation_cutoff=2)
        lower_bounds = tuple(record["commutator"]["lower_bound"] for record in family)
        continuity = tuple(
            record["strong_continuity"]["lapse_times_generator_bound"]
            for record in family
        )
        self.assertTrue(
            all(
                lower_bounds[index] >= lower_bounds[index - 1]
                for index in range(1, len(lower_bounds))
            )
        )
        self.assertTrue(
            all(
                continuity[index] < continuity[index - 1]
                for index in range(1, len(continuity))
            )
        )

    def test_candidate_records_cover_observer_local_routes(self):
        records = observer_local_candidate_records(max_cutoff=12, excitation_cutoff=2)
        self.assertEqual(len(records), 4)
        self.assertEqual(
            {record["candidate_id"] for record in records},
            {
                "coherent_state_tangent_plane_double_scaling",
                "local_planck_cell_matrix_block",
                "matrix_valued_screen_fiber",
                "modular_crossed_product_clock_shift",
            },
        )
        for record in records:
            self.assertTrue(record["anti_tautological_selection"])

    def test_certificate_selects_a_theorem_candidate(self):
        certificate = observer_local_noncommutative_subsystem_certificate(
            max_cutoff=12,
            excitation_cutoff=2,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(certificate["selected_outcome"], "A_theorem_candidate")
        self.assertEqual(
            certificate["result_type"],
            "observer_local_tangent_plane_theorem_candidate",
        )
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_tangent_plane_gate_statuses(self):
        certificate = observer_local_noncommutative_subsystem_certificate(
            max_cutoff=12,
            excitation_cutoff=2,
        )
        tangent = {
            record["candidate_id"]: record
            for record in certificate["candidate_records"]
        }["coherent_state_tangent_plane_double_scaling"]
        for key, status in tangent["gate_status"].items():
            if key == "typeii_route":
                self.assertEqual(status, "conditional")
            else:
                self.assertEqual(status, "pass")
        self.assertGreater(
            tangent["quantitative_witness"]["final_commutator_lower_bound"],
            0.0,
        )

    def test_fiber_and_modular_routes_are_conditional(self):
        certificate = observer_local_noncommutative_subsystem_certificate(
            max_cutoff=12,
            excitation_cutoff=2,
        )
        records = {
            record["candidate_id"]: record
            for record in certificate["candidate_records"]
        }
        for candidate_id in (
            "matrix_valued_screen_fiber",
            "modular_crossed_product_clock_shift",
        ):
            self.assertTrue(records[candidate_id]["verdict"].startswith("C_"))
            self.assertEqual(
                records[candidate_id]["gate_status"]["nonzero_commutator_lower_bound"],
                "conditional",
            )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            tangent_plane_double_scaling_record(cutoff=4, excitation_cutoff=2)
        with self.assertRaises(ValueError):
            tangent_plane_family_records(max_cutoff=4, excitation_cutoff=2)
        with self.assertRaises(ValueError):
            observer_local_noncommutative_subsystem_certificate(
                max_cutoff=12,
                excitation_cutoff=0,
            )


if __name__ == "__main__":
    unittest.main()
