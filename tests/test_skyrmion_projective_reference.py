import unittest
from fractions import Fraction

from qgtoy.__main__ import build_parser
from qgtoy.skyrmion_projective_reference import (
    odd_peter_weyl_closed_deficit_fraction,
    odd_peter_weyl_closed_fidelity_fraction,
    odd_peter_weyl_center_action_record,
    odd_peter_weyl_entanglement_fidelity_fraction,
    odd_peter_weyl_mean_casimir_fraction,
    odd_peter_weyl_global_orientation_risk_record,
    odd_peter_weyl_multiplier_fraction,
    odd_peter_weyl_recovery_record,
    odd_peter_weyl_reference_dimension,
    skyrmion_projective_reference_certificate,
    skyrmion_joint_orientation_risk_record,
    skyrmion_slow_rotation_record,
)


class SkyrmionProjectiveReferenceTest(unittest.TestCase):
    def test_small_exact_dimensions_multipliers_and_casimir(self):
        self.assertEqual(odd_peter_weyl_reference_dimension(0), 4)
        self.assertEqual(odd_peter_weyl_reference_dimension(1), 20)
        self.assertEqual(odd_peter_weyl_reference_dimension(2), 56)
        self.assertEqual(
            tuple(odd_peter_weyl_multiplier_fraction(0, rank) for rank in range(3)),
            (Fraction(1), Fraction(1, 3), Fraction(0)),
        )
        self.assertEqual(
            tuple(odd_peter_weyl_multiplier_fraction(1, rank) for rank in range(5)),
            (
                Fraction(1),
                Fraction(3, 5),
                Fraction(8, 25),
                Fraction(4, 35),
                Fraction(0),
            ),
        )
        self.assertEqual(odd_peter_weyl_mean_casimir_fraction(0), Fraction(3, 4))
        self.assertEqual(odd_peter_weyl_mean_casimir_fraction(1), Fraction(63, 20))

    def test_closed_deficit_matches_exact_counting(self):
        for cutoff in range(8):
            for rank in range(2 * cutoff + 3):
                self.assertEqual(
                    Fraction(1) - odd_peter_weyl_multiplier_fraction(cutoff, rank),
                    odd_peter_weyl_closed_deficit_fraction(cutoff, rank),
                )

    def test_closed_fidelity_matches_rank_sum(self):
        for cutoff in range(7):
            for spin in range(1, cutoff + 2):
                self.assertEqual(
                    odd_peter_weyl_entanglement_fidelity_fraction(spin, cutoff),
                    odd_peter_weyl_closed_fidelity_fraction(spin, cutoff),
                )
        self.assertEqual(
            odd_peter_weyl_entanglement_fidelity_fraction(1, 0),
            Fraction(2, 9),
        )
        self.assertEqual(
            odd_peter_weyl_entanglement_fidelity_fraction(1, 1),
            Fraction(22, 45),
        )

    def test_recovery_record_is_center_blind_and_inexact(self):
        record = odd_peter_weyl_recovery_record(2, 4)
        self.assertTrue(record["center_blind_density_povm_and_kernel"])
        self.assertFalse(record["faithful_for_opposite_center_parity_coherences"])
        self.assertTrue(record["closed_deficit_formula_agrees"])
        self.assertTrue(record["closed_fidelity_formula_agrees"])
        self.assertGreater(record["normalized_diamond_error_lower_bound"], 0.0)

    def test_projective_global_risk_bounds(self):
        for cutoff in range(12):
            record = odd_peter_weyl_global_orientation_risk_record(cutoff)
            self.assertTrue(record["bounds_respected"])
            self.assertGreater(
                record["projective_hard_cutoff_risk_lower_bound"],
                0.0,
            )
        joint = skyrmion_joint_orientation_risk_record()
        self.assertEqual(joint["joint_scaling_status"], "pass")
        self.assertGreater(
            joint["global_chordal_orientation_risk_lower_bound"],
            0.0,
        )

    def test_center_action_is_computed_from_half_integer_parity(self):
        for cutoff in range(8):
            center = odd_peter_weyl_center_action_record(cutoff)
            self.assertTrue(all(phase == -1 for phase in center["center_phases"]))
            self.assertEqual(center["token_center_phase"], -1)
            self.assertTrue(center["density_operator_center_invariant"])
            self.assertTrue(center["povm_effect_center_invariant"])
            self.assertTrue(center["orientation_kernel_center_invariant"])
            self.assertFalse(center["resolves_opposite_center_parity"])

    def test_slow_rotation_scaling(self):
        low = skyrmion_slow_rotation_record(
            8,
            skyrme_coupling=0.1,
            pion_decay_constant=1.0,
        )
        high = skyrmion_slow_rotation_record(
            8,
            skyrme_coupling=0.2,
            pion_decay_constant=1.0,
        )
        self.assertAlmostEqual(
            high["slow_rotation_parameter_epsilon_rot"]
            / low["slow_rotation_parameter_epsilon_rot"],
            4.0,
        )
        self.assertAlmostEqual(
            high["rotational_energy_to_mass_ratio"]
            / low["rotational_energy_to_mass_ratio"],
            16.0,
        )

    def test_certificate(self):
        certificate = skyrmion_projective_reference_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("isospin", certificate["central_result"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["skyrmion-projective-reference"])
        self.assertEqual(args.maximum_system_spin, 6)
        self.assertEqual(args.maximum_reference_cutoff, 8)
        self.assertEqual(args.skyrme_coupling, 0.1)
        self.assertEqual(args.pion_mass, 1.0)
        self.assertEqual(args.curvature, 0.0025)
        self.assertEqual(args.wall_radius, 4.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            odd_peter_weyl_reference_dimension(-1)
        with self.assertRaises(ValueError):
            odd_peter_weyl_closed_deficit_fraction(1, 5)
        with self.assertRaises(ValueError):
            odd_peter_weyl_closed_fidelity_fraction(3, 1)


if __name__ == "__main__":
    unittest.main()
