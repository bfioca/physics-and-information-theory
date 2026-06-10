import unittest

from qgtoy.su2_directional_reference_no_go import (
    clebsch_gordan_multiplicity_record,
    single_irrep_recovery_bound_record,
    single_irrep_twirl_record,
    su2_directional_reference_no_go_certificate,
)


class Su2DirectionalReferenceNoGoTest(unittest.TestCase):
    def test_clebsch_gordan_dimension_identity(self):
        for system_spin in range(1, 8):
            for reference_spin in range(0, 9):
                record = clebsch_gordan_multiplicity_record(
                    system_spin,
                    reference_spin,
                )
                self.assertTrue(record["dimension_identity_holds"])
                self.assertTrue(record["decomposition_is_multiplicity_free"])
                self.assertTrue(all(value == 1 for value in record["sector_multiplicities"]))

    def test_single_irrep_twirl_is_abelian_and_entanglement_breaking(self):
        for reference_spin in (0, 1, 3, 10, 100):
            record = single_irrep_twirl_record(4, reference_spin)
            self.assertTrue(record["twirled_range_is_commutative"])
            self.assertTrue(record["channel_is_measure_and_prepare"])
            self.assertTrue(record["channel_is_equivalent_to_quantum_to_classical"])
            self.assertTrue(record["channel_is_entanglement_breaking"])
            self.assertFalse(record["reference_charge_alone_restores_full_quantum_algebra"])

    def test_recovery_bound_is_independent_of_reference_spin(self):
        for system_spin in range(1, 8):
            expected = 1.0 - 1.0 / (2 * system_spin + 1)
            for reference_spin in (0, 1, 2, 8, 100):
                record = single_irrep_recovery_bound_record(
                    system_spin,
                    reference_spin,
                )
                self.assertAlmostEqual(
                    record["normalized_diamond_recovery_error_lower_bound"],
                    expected,
                )
                self.assertFalse(record["exact_full_quantum_recovery_possible"])

    def test_certificate_passes_with_reducible_reference_boundary(self):
        certificate = su2_directional_reference_no_go_certificate(
            max_system_spin=8,
            max_reference_spin=8,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("multiplicity ancillas", certificate["claim_boundary"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            clebsch_gordan_multiplicity_record(0, 1)
        with self.assertRaises(ValueError):
            clebsch_gordan_multiplicity_record(1, -1)
        with self.assertRaises(ValueError):
            single_irrep_recovery_bound_record(1.5, 2)
        with self.assertRaises(ValueError):
            su2_directional_reference_no_go_certificate(max_reference_spin=-1)


if __name__ == "__main__":
    unittest.main()
