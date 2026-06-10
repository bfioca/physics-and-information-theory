import unittest
from math import log

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_hard_current_multipole import (
    compressed_unitary_channel_distance_bound,
    current_first_absolute_moment,
    hard_current_multipole_remainder_bound,
    hard_current_second_moment_remainder_bound,
    hard_current_support_record,
    sufficient_nonzero_bohr_relative_error_cap,
    sufficient_zero_bohr_relative_error_cap,
    nonzero_bohr_gksl_channel_error_bound,
    static_patch_hard_current_multipole_certificate,
    two_cell_nonzero_bohr_saturation_witness,
    zero_bohr_gksl_channel_error_bound,
)


class StaticPatchHardCurrentMultipoleTest(unittest.TestCase):
    def test_first_absolute_moment_and_remainder(self):
        self.assertAlmostEqual(
            current_first_absolute_moment((0.1, 0.3), (2.0, 4.0)),
            1.4,
        )
        self.assertAlmostEqual(
            hard_current_multipole_remainder_bound(
                5.0,
                (0.1, 0.3),
                (2.0, 4.0),
                coupling=-0.2,
            ),
            1.4,
        )

    def test_compressed_unitary_channel_bound(self):
        self.assertAlmostEqual(
            compressed_unitary_channel_distance_bound(
                3.0,
                interaction_remainder_norm_bound=0.1,
            ),
            0.6,
        )
        self.assertEqual(
            compressed_unitary_channel_distance_bound(
                100.0,
                interaction_remainder_norm_bound=1.0,
            ),
            2.0,
        )

    def test_second_moment_and_gksl_bounds(self):
        self.assertAlmostEqual(
            hard_current_second_moment_remainder_bound(
                4.0,
                (0.1, 0.2),
                (2.0, 1.0),
                coupling=0.5,
            ),
            0.06,
        )
        spin = 8
        time = 2.0
        budget = 0.01
        zero_error = sufficient_zero_bohr_relative_error_cap(
            spin,
            time,
            channel_error_budget=budget,
        )
        nonzero_error = sufficient_nonzero_bohr_relative_error_cap(
            spin,
            time,
            channel_error_budget=budget,
        )
        self.assertAlmostEqual(
            zero_bohr_gksl_channel_error_bound(
                spin,
                time,
                relative_multipole_operator_error=zero_error,
            ),
            budget,
        )
        self.assertAlmostEqual(
            nonzero_bohr_gksl_channel_error_bound(
                spin,
                time,
                aggregate_relative_sector_error=nonzero_error,
            ),
            budget,
        )

    def test_two_cell_nonzero_bohr_bound_is_sharp(self):
        witness = two_cell_nonzero_bohr_saturation_witness(
            support_radius=0.2,
            bath_lipschitz_constant=3.0,
            coupling=0.5,
        )
        self.assertEqual(witness["integrated_nonzero_bohr_monopole_norm"], 0.0)
        self.assertAlmostEqual(witness["exact_nonzero_bohr_remainder_norm"], 0.3)
        self.assertAlmostEqual(witness["first_moment_bound"], 0.3)
        self.assertAlmostEqual(witness["bound_saturation_ratio"], 1.0)

    def test_disjoint_support_scaling(self):
        record = hard_current_support_record(32)
        dimension = 65
        self.assertEqual(
            record["generic_active_support_constraint"],
            "zero_bohr_linear_interference",
        )
        self.assertEqual(
            record["dipole_cancelled_active_support_constraint"],
            "disjoint_worldtubes",
        )
        self.assertAlmostEqual(
            record[
                "sufficient_support_for_interaction_vector_budget_over_radius"
            ],
            1.0 / dimension,
        )
        self.assertAlmostEqual(
            record["dipole_cancelled_admissible_optical_support_over_radius"],
            0.5
            / (dimension * 32 * 33 * log(float(dimension))) ** 0.5,
        )
        rescaled = hard_current_support_record(32, radius=2.0)
        self.assertAlmostEqual(
            rescaled["generic_same_shell_support_angular_radius"],
            record["generic_same_shell_support_angular_radius"],
        )
        tiny_center = hard_current_support_record(
            32,
            mismatch_coefficient=1.0e-20,
        )
        self.assertEqual(
            tiny_center["generic_active_support_constraint"],
            "disjoint_worldtubes",
        )

    def test_certificate(self):
        certificate = static_patch_hard_current_multipole_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("zero monopole", certificate["central_result"])
        wide_center = static_patch_hard_current_multipole_certificate(
            mismatch_coefficient=10.0,
        )
        self.assertEqual(wide_center["status"], "pass")

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-hard-current-multipole"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.mismatch_coefficient, 1.0)
        self.assertEqual(args.multipole_error_coefficient, 1.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            current_first_absolute_moment((0.1,), (1.0, 2.0))
        with self.assertRaises(ValueError):
            hard_current_multipole_remainder_bound(-1.0, (0.1,), (1.0,))
        with self.assertRaises(ValueError):
            static_patch_hard_current_multipole_certificate(maximum_spin=16)
        with self.assertRaises(ValueError):
            sufficient_zero_bohr_relative_error_cap(
                1,
                1.0,
                channel_error_budget=2.0,
            )


if __name__ == "__main__":
    unittest.main()
