import unittest

from qgtoy.relative_entropy_bridge import (
    DEPHASING_QUBIT,
    GAUGE_TRACE_QUBIT,
    IDENTITY_QUBIT,
    NULL_QUBIT,
    major_unlock_relative_entropy_observer_bridge_certificate,
)


class RelativeEntropyObserverBridgeTheoremTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = major_unlock_relative_entropy_observer_bridge_certificate(
            bloch_radius=0.5,
        )

    def test_certificate_passes(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))

    def test_static_entropy_shadow_collision_is_separated_by_response(self):
        collision = self.certificate["weak_shadow_collision"]
        self.assertTrue(collision["all_static_entropy_shadows_match"])

        responses = {
            record["channel"]: record["preserved_axes_from_response"]
            for record in collision["relative_entropy_response_separates"]
        }
        self.assertEqual(responses[IDENTITY_QUBIT.name], ("X", "Y", "Z"))
        self.assertEqual(responses[DEPHASING_QUBIT.name], ("Z",))
        self.assertEqual(responses[NULL_QUBIT.name], ())

    def test_response_defects_match_expected_observer_algebras(self):
        records = {
            record["channel"]: record
            for record in self.certificate["operational_examples"][
                "relative_entropy_response"
            ]
        }
        identity = records[IDENTITY_QUBIT.name]["response_rows"]
        dephasing = records[DEPHASING_QUBIT.name]["response_rows"]
        null = records[NULL_QUBIT.name]["response_rows"]

        self.assertTrue(all(row["defect_bits"] == 0.0 for row in identity))
        self.assertEqual(
            tuple(row["probe_axis"] for row in dephasing if row["defect_bits"] == 0.0),
            ("Z",),
        )
        self.assertTrue(all(row["defect_bits"] > 0.0 for row in null))

    def test_gauge_multiplicity_is_recorded_beyond_abstract_type(self):
        channels = {
            record["channel"]: record
            for record in self.certificate["operational_examples"]["channels"]
        }
        gauge = channels[GAUGE_TRACE_QUBIT.name]
        self.assertEqual(gauge["abstract_observer_algebra"], "M_2")
        self.assertEqual(gauge["represented_observer_algebra"], "I_2 tensor M_2")

    def test_bridge_classification_records_quantum_classical_and_null_transfer(self):
        bridges = {
            record["bridge"]: record
            for record in self.certificate["bridge_channel_classification"]["records"]
        }
        self.assertEqual(bridges["quantum_bridge"]["transferred_algebra"], "M_2")
        self.assertEqual(
            bridges["classical_bridge"]["transferred_algebra"],
            "C direct-sum C",
        )
        self.assertEqual(bridges["null_bridge"]["transferred_algebra"], "C")

    def test_claim_boundary_is_explicit(self):
        boundary = self.certificate["claim_boundary"]
        self.assertIn("not a continuum ER=EPR or de Sitter theorem", boundary)
        self.assertIn("approximate/noisy observer-bridge", boundary)

    def test_approximate_recovery_frontier_is_recorded_but_not_overclaimed(self):
        frontier = self.certificate["approximate_recovery_frontier"]
        self.assertEqual(
            frontier["status"],
            "known_state_level_bound_recorded_not_claimed_as_full_noisy_algebra_theorem",
        )
        rows = frontier["records"]
        self.assertEqual(rows[0]["relative_entropy_defect_bits"], 0.0)
        self.assertEqual(rows[0]["universal_recovery_fidelity_lower_bound"], 1.0)
        self.assertLess(rows[-1]["universal_recovery_fidelity_lower_bound"], 1.0)

    def test_invalid_bloch_radius_is_rejected(self):
        with self.assertRaises(ValueError):
            major_unlock_relative_entropy_observer_bridge_certificate(
                bloch_radius=1.0,
            )


if __name__ == "__main__":
    unittest.main()
