import unittest
from math import log

from qgtoy.charged_reference_recovery import (
    charged_reference_column_support,
    charged_reference_isometry_record,
    charged_reference_matrix_unit_recovery_record,
    charged_reference_recovery_certificate,
    charged_reference_treatment_record,
    invariant_operator_algebra_record,
    kms_core_tensor_stability_record,
    minimal_charged_reference_dimension_record,
    scalar_reference_control_record,
)


class ChargedReferenceRecoveryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = charged_reference_recovery_certificate(max_level=8)

    def test_certificate_passes_with_selected_irrep_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertIn("positive-integer-spin", self.certificate["claim_boundary"])
        self.assertIn("not a matched operational task", self.certificate["claim_boundary"])

    def test_sparse_columns_form_an_exact_isometry(self):
        for level in range(1, 8):
            record = charged_reference_isometry_record(level)
            self.assertTrue(record["encoding_is_isometric"])
            self.assertLess(record["isometry_diagonal_error"], 1e-14)
            self.assertLess(record["isometry_off_diagonal_error"], 1e-14)
            self.assertEqual(record["physical_invariant_dimension"], 2 * level + 1)
            self.assertFalse(record["encoder_is_su2_covariant_from_V_L"])
            self.assertFalse(record["decoder_is_su2_covariant_to_V_L"])
            self.assertAlmostEqual(
                record["intertwiner_obstruction_operator_norm"],
                2.0,
            )

    def test_singlet_corner_is_not_the_full_fixed_algebra(self):
        for level in range(1, 8):
            record = invariant_operator_algebra_record(level)
            dimension = 2 * level + 1
            self.assertEqual(record["fixed_operator_algebra_dimension"], dimension**3)
            self.assertEqual(record["singlet_corner_algebra_dimension"], dimension**2)
            self.assertFalse(record["singlet_corner_is_full_fixed_algebra"])

    def test_complete_matrix_unit_basis_recovers(self):
        for level in range(1, 7):
            record = charged_reference_matrix_unit_recovery_record(level)
            self.assertEqual(record["matrix_unit_count"], (2 * level + 1) ** 2)
            self.assertTrue(record["complete_operator_basis_recovers_exactly"])
            self.assertEqual(record["diamond_recovery_error"], 0.0)

    def test_scalar_control_and_charged_treatment_separate(self):
        for level in range(1, 8):
            scalar = scalar_reference_control_record(level)
            charged = charged_reference_treatment_record(level)
            self.assertEqual(
                scalar["decoder_worst_case_trace_distance_error_lower_bound"],
                0.5,
            )
            self.assertAlmostEqual(
                scalar["pure_probe_relative_entropy_loss"],
                log(2 * level + 1),
            )
            self.assertEqual(charged["abstract_code_decoder_error"], 0.0)
            self.assertEqual(charged["diamond_recovery_error"], 0.0)
            self.assertFalse(charged["is_operational_prepared_reference_protocol"])

    def test_peter_weyl_reference_saturates_dimension_lower_bound(self):
        for level in range(1, 8):
            record = minimal_charged_reference_dimension_record(level)
            self.assertEqual(
                record["reference_dimension_lower_bound"],
                (2 * level + 1) ** 2,
            )
            self.assertTrue(record["construction_saturates_lower_bound"])
            self.assertFalse(record["bound_is_unrestricted_reference_minimum"])

    def test_recovery_separation_survives_common_core_tensor(self):
        record = kms_core_tensor_stability_record(5)
        self.assertEqual(record["scalar_fixed_algebra_decoder_error_lower_bound"], 0.5)
        self.assertEqual(
            record["singlet_code_decoder_error_under_spectator_tensor"],
            0.0,
        )
        self.assertFalse(record["common_core_tensor_changes_comparison"])
        self.assertFalse(record["charged_code_is_realized_by_interacting_kms_dynamics"])

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            charged_reference_isometry_record(0)
        with self.assertRaises(ValueError):
            charged_reference_isometry_record(1.5)
        with self.assertRaises(ValueError):
            charged_reference_column_support(2, -1)
        with self.assertRaises(ValueError):
            charged_reference_column_support(2, 5)
        with self.assertRaises(ValueError):
            charged_reference_recovery_certificate(max_level=0)
        with self.assertRaises(ValueError):
            charged_reference_recovery_certificate(tolerance=0.0)


if __name__ == "__main__":
    unittest.main()
