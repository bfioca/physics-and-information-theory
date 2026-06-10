import unittest

from qgtoy.redshifted_rotation_reference_tradeoff import (
    peter_weyl_constructive_diamond_upper_bound,
    peter_weyl_rotor_mean_energy,
    peter_weyl_simple_diamond_bound,
    redshifted_rotation_reference_tradeoff_certificate,
    redshifted_rotation_reference_tradeoff_record,
    sufficient_peter_weyl_reference_cutoff,
)


class RedshiftedRotationReferenceTradeoffTest(unittest.TestCase):
    def test_elementary_bound_dominates_closed_constructive_upper_bound(self):
        for spin in range(1, 12):
            for cutoff in (spin, 2 * spin, 5 * spin, 20 * spin):
                self.assertLessEqual(
                    peter_weyl_constructive_diamond_upper_bound(spin, cutoff),
                    peter_weyl_simple_diamond_bound(spin, cutoff) + 1e-15,
                )

    def test_sufficient_cutoff_meets_target(self):
        for spin in range(1, 20):
            for target in (0.5, 0.2, 0.05):
                cutoff = sufficient_peter_weyl_reference_cutoff(spin, target)
                self.assertLessEqual(
                    peter_weyl_constructive_diamond_upper_bound(spin, cutoff),
                    target,
                )
                self.assertLessEqual(
                    peter_weyl_simple_diamond_bound(spin, cutoff),
                    target,
                )

    def test_single_wall_record_separates_clock_and_charged_reference(self):
        record = redshifted_rotation_reference_tradeoff_record(
            radius=1.0,
            stretched_distance=1.0 / 4096.0,
            field_energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
            target_recovery_error=0.1,
            rotor_moment_of_inertia=2.0,
        )
        self.assertGreater(
            record["clock_only_optimal_normalized_diamond_error"],
            0.99,
        )
        self.assertLessEqual(
            record["charged_reference_constructive_diamond_error_upper_bound"],
            0.1,
        )
        self.assertGreater(record["mean_rigid_rotor_reference_energy"], 0.0)

    def test_rotor_energy_uses_declared_inertia(self):
        self.assertAlmostEqual(
            peter_weyl_rotor_mean_energy(10, moment_of_inertia=2.0),
            18.0,
        )

    def test_certificate(self):
        certificate = redshifted_rotation_reference_tradeoff_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("sampled asymptotic", certificate["status_scope"])
        self.assertIn("not proved optimal", certificate["claim_boundary"])
        self.assertIn("fixed independently", certificate["claim_boundary"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            sufficient_peter_weyl_reference_cutoff(1, 1.0)
        with self.assertRaises(ValueError):
            peter_weyl_constructive_diamond_upper_bound(2, 1)
        with self.assertRaises(ValueError):
            peter_weyl_rotor_mean_energy(2, moment_of_inertia=0.0)


if __name__ == "__main__":
    unittest.main()
