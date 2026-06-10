import unittest

from qgtoy.__main__ import build_parser
from qgtoy.finite_size_static_patch_observer import (
    collar_constructive_gap_floor_asymptotic,
    compactness_energy_capacity,
    energy_constrained_rotor_recovery_bound_record,
    finite_size_static_patch_observer_certificate,
    maximum_finite_size_reference_cutoff,
    minimum_cutoff_meeting_constructive_bound,
    minimum_rest_energy_for_cutoff,
    minimum_total_observer_energy_for_cutoff,
    minimum_total_observer_energy_for_spectral_cutoff,
    maximum_mean_casimir_from_compactness,
    peter_weyl_any_decoder_error_lower_bound,
    spherical_top_mean_rotor_load,
)
from qgtoy.redshifted_rotation_reference_tradeoff import (
    peter_weyl_constructive_diamond_upper_bound,
)


class FiniteSizeStaticPatchObserverTest(unittest.TestCase):
    def test_spherical_top_energy_minimization(self):
        cutoff = 7
        radius = 0.2
        kappa = 2.0 / 3.0
        zeta = 0.25
        rest = minimum_rest_energy_for_cutoff(
            cutoff,
            observer_radius=radius,
            inertia_coefficient=kappa,
            maximum_excitation_fraction=zeta,
        )
        load = spherical_top_mean_rotor_load(cutoff)
        rotor = load / (kappa * rest * radius**2)
        self.assertAlmostEqual(rotor / rest, zeta)
        self.assertAlmostEqual(
            minimum_total_observer_energy_for_cutoff(
                cutoff,
                observer_radius=radius,
                inertia_coefficient=kappa,
                maximum_excitation_fraction=zeta,
            ),
            rest + rotor,
        )

    def test_cutoff_capacity_is_exact_integer_root(self):
        parameters = {
            "observer_radius": 0.03,
            "newton_constant": 1e-5,
            "inertia_coefficient": 2.0 / 3.0,
            "compactness_margin": 0.5,
            "maximum_excitation_fraction": 0.25,
        }
        cutoff = maximum_finite_size_reference_cutoff(**parameters)
        capacity = compactness_energy_capacity(
            observer_radius=parameters["observer_radius"],
            newton_constant=parameters["newton_constant"],
            compactness_margin=parameters["compactness_margin"],
        )
        self.assertLessEqual(
            minimum_total_observer_energy_for_spectral_cutoff(
                cutoff,
                observer_radius=parameters["observer_radius"],
                inertia_coefficient=parameters["inertia_coefficient"],
                maximum_excitation_fraction=parameters[
                    "maximum_excitation_fraction"
                ],
            ),
            capacity,
        )
        self.assertGreater(
            minimum_total_observer_energy_for_spectral_cutoff(
                cutoff + 1,
                observer_radius=parameters["observer_radius"],
                inertia_coefficient=parameters["inertia_coefficient"],
                maximum_excitation_fraction=parameters[
                    "maximum_excitation_fraction"
                ],
            ),
            capacity,
        )

    def test_multiplicity_bound_for_finite_peter_weyl_cutoff(self):
        self.assertAlmostEqual(
            peter_weyl_any_decoder_error_lower_bound(100, 3),
            1.0 - 16.0 / 201.0,
        )
        self.assertEqual(peter_weyl_any_decoder_error_lower_bound(2, 20), 0.0)

    def test_energy_constrained_bound_handles_high_spin_tails(self):
        zero_energy = energy_constrained_rotor_recovery_bound_record(
            10,
            maximum_mean_casimir=0.0,
        )
        self.assertAlmostEqual(
            zero_energy["normalized_diamond_error_lower_bound"],
            1.0 - 1.0 / 21.0,
        )
        low = energy_constrained_rotor_recovery_bound_record(
            100,
            maximum_mean_casimir=10.0,
        )
        high = energy_constrained_rotor_recovery_bound_record(
            100,
            maximum_mean_casimir=100.0,
        )
        self.assertGreater(
            low["normalized_diamond_error_lower_bound"],
            high["normalized_diamond_error_lower_bound"],
        )
        asymptotic = energy_constrained_rotor_recovery_bound_record(
            1_000_000,
            maximum_mean_casimir=10.0,
        )
        self.assertGreater(
            asymptotic["normalized_diamond_error_lower_bound"],
            0.95,
        )
        dimension = 2_001
        shrinking_budget = energy_constrained_rotor_recovery_bound_record(
            (dimension - 1) // 2,
            maximum_mean_casimir=2.0 / dimension**2,
        )
        self.assertGreaterEqual(
            shrinking_budget["normalized_diamond_error_lower_bound"],
            1.0 - 2.0 / dimension,
        )

    def test_compactness_mean_casimir_matches_energy_minimization(self):
        parameters = {
            "observer_radius": 0.03,
            "newton_constant": 1e-5,
            "inertia_coefficient": 2.0 / 3.0,
            "compactness_margin": 0.5,
            "maximum_excitation_fraction": 0.25,
        }
        casimir = maximum_mean_casimir_from_compactness(**parameters)
        rest = (
            casimir
            / (
                2.0
                * parameters["inertia_coefficient"]
                * parameters["maximum_excitation_fraction"]
                * parameters["observer_radius"] ** 2
            )
        ) ** 0.5
        rotor = casimir / (
            2.0
            * parameters["inertia_coefficient"]
            * rest
            * parameters["observer_radius"] ** 2
        )
        self.assertAlmostEqual(
            2.0
            * parameters["newton_constant"]
            * (rest + rotor)
            / parameters["observer_radius"],
            parameters["compactness_margin"],
        )

    def test_minimum_constructive_cutoff(self):
        for spin in (1, 3, 8):
            cutoff = minimum_cutoff_meeting_constructive_bound(spin, 0.1)
            self.assertLessEqual(
                peter_weyl_constructive_diamond_upper_bound(spin, cutoff),
                0.1,
            )
            if cutoff > spin:
                self.assertGreater(
                    peter_weyl_constructive_diamond_upper_bound(spin, cutoff - 1),
                    0.1,
                )

    def test_asymptotic_floor_has_expected_radius_scaling(self):
        first = collar_constructive_gap_floor_asymptotic(
            radius=1.0,
            newton_constant=1e-6,
            field_energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
            target_recovery_error=0.1,
            collar_size_fraction=0.25,
            inertia_coefficient=2.0 / 3.0,
            compactness_margin=0.5,
            maximum_excitation_fraction=0.25,
        )
        second = collar_constructive_gap_floor_asymptotic(
            radius=4.0,
            newton_constant=1e-6,
            field_energy_budget=1.0,
            inner_offset=0.5,
            outer_offset=1.5,
            target_recovery_error=0.1,
            collar_size_fraction=0.25,
            inertia_coefficient=2.0 / 3.0,
            compactness_margin=0.5,
            maximum_excitation_fraction=0.25,
        )
        self.assertAlmostEqual(
            second["asymptotic_coordinate_gap_floor_delta"],
            first["asymptotic_coordinate_gap_floor_delta"],
        )
        self.assertAlmostEqual(
            second["asymptotic_proper_distance_floor_rho"]
            / first["asymptotic_proper_distance_floor_rho"],
            2.0,
        )

    def test_certificate(self):
        certificate = finite_size_static_patch_observer_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("any-decoder", certificate["claim_boundary"])
        self.assertIn("Einstein-matter", certificate["next_physics_gate"])

    def test_cli_defaults_match_certificate_defaults(self):
        args = build_parser().parse_args(["finite-size-static-patch-observer"])
        self.assertEqual(args.minimum_power, 64)
        self.assertEqual(args.steps, 9)

    def test_certificate_reports_missing_transition_without_crashing(self):
        certificate = finite_size_static_patch_observer_certificate(
            newton_constant=0.1,
        )
        self.assertEqual(certificate["status"], "fail")
        self.assertFalse(
            certificate["certified_claims"][
                "constructive_protocol_crosses_from_feasible_to_infeasible"
            ]
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            maximum_finite_size_reference_cutoff(
                observer_radius=1.0,
                newton_constant=1.0,
                inertia_coefficient=2.0 / 3.0,
                compactness_margin=1.0,
                maximum_excitation_fraction=0.5,
            )
        with self.assertRaises(ValueError):
            finite_size_static_patch_observer_certificate(steps=3)
        with self.assertRaises(ValueError):
            maximum_finite_size_reference_cutoff(
                observer_radius=1.0,
                newton_constant=1.0,
                inertia_coefficient=0.8,
                compactness_margin=0.5,
                maximum_excitation_fraction=0.5,
            )
        with self.assertRaises(ValueError):
            finite_size_static_patch_observer_certificate(collar_size_fraction=1.1)


if __name__ == "__main__":
    unittest.main()
