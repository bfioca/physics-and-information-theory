import unittest
from math import log, pi

from qgtoy.static_patch_matter_observer_channel import (
    AncillaStableOperatorNormResidual,
    NormalizedDiamondDistanceBound,
    finite_switch_matter_obstruction_record,
    finite_time_peter_weyl_recovery_transfer_record,
    fixed_spin_spectral_obstruction_from_residual,
    matter_collective_diffusion_rate_lower_bound,
    recovery_error_transfer_bracket,
    static_patch_matter_observer_channel_certificate,
)


class StaticPatchMatterObserverChannelTest(unittest.TestCase):
    def test_zero_perturbation_preserves_haar_bounds(self):
        zero = NormalizedDiamondDistanceBound(0.0, "exact")
        record = recovery_error_transfer_bracket(
            haar_any_decoder_lower_bound=0.2,
            haar_constructive_decoder_upper_bound=0.7,
            heat_to_haar_bound=zero,
            physical_to_heat_bound=zero,
        )
        self.assertEqual(record["physical_any_decoder_error_lower_bound"], 0.2)
        self.assertEqual(
            record["physical_constructive_decoder_error_upper_bound"], 0.7
        )

    def test_diamond_corrections_add_and_clip(self):
        record = recovery_error_transfer_bracket(
            haar_any_decoder_lower_bound=0.3,
            haar_constructive_decoder_upper_bound=0.8,
            heat_to_haar_bound=NormalizedDiamondDistanceBound(0.2, "heat"),
            physical_to_heat_bound=NormalizedDiamondDistanceBound(0.3, "local"),
        )
        self.assertAlmostEqual(record["total_normalized_diamond_correction"], 0.5)
        self.assertEqual(record["physical_any_decoder_error_lower_bound"], 0.0)
        self.assertEqual(
            record["physical_constructive_decoder_error_upper_bound"], 1.0
        )

    def test_norm_types_cannot_be_interchanged(self):
        spectral = AncillaStableOperatorNormResidual(0.01, "ULE")
        with self.assertRaises(TypeError):
            recovery_error_transfer_bracket(
                haar_any_decoder_lower_bound=0.2,
                haar_constructive_decoder_upper_bound=0.7,
                heat_to_haar_bound=spectral,
                physical_to_heat_bound=NormalizedDiamondDistanceBound(
                    0.0,
                    "exact",
                ),
            )
        with self.assertRaises(TypeError):
            fixed_spin_spectral_obstruction_from_residual(
                2,
                heat_to_haar_bound=NormalizedDiamondDistanceBound(0.1, "heat"),
                spectral_residual=NormalizedDiamondDistanceBound(0.01, "wrong"),
            )

    def test_finite_time_record_transfers_both_branches(self):
        local = NormalizedDiamondDistanceBound(0.02, "local theorem")
        record = finite_time_peter_weyl_recovery_transfer_record(
            8,
            512,
            maximum_mean_casimir=1.0,
            proper_time=2.0,
            diffusion_rate=1.0,
            physical_to_heat_bound=local,
        )
        correction = record["total_normalized_diamond_correction"]
        obstruction = record["energy_constrained_obstruction_branch"]
        constructive = record["canonical_peter_weyl_constructive_branch"]
        self.assertAlmostEqual(
            obstruction["physical_any_decoder_error_lower_bound"],
            max(0.0, obstruction["haar_any_decoder_error_lower_bound"] - correction),
        )
        self.assertAlmostEqual(
            constructive["physical_constructive_decoder_error_upper_bound"],
            min(
                1.0,
                constructive["haar_constructive_decoder_error_upper_bound"]
                + correction,
            ),
        )
        self.assertIn(
            "not a single-resource bracket",
            record["resource_comparison_boundary"],
        )

    def test_matter_rate_normalization(self):
        self.assertAlmostEqual(
            matter_collective_diffusion_rate_lower_bound(0.3, 0.2, 0.5),
            pi * 0.3**2 * 0.5 / 0.2**2,
        )

    def test_longer_burn_in_improves_spectral_obstruction(self):
        spin = 5
        coupling = 1.0e-7
        rate = matter_collective_diffusion_rate_lower_bound(coupling, 1.0, 1.0)
        elapsed = log(float(2 * spin + 1)) / (2.0 * rate)
        common = dict(
            lapse=1.0,
            coupling=coupling,
            elapsed_time=elapsed,
            switch_effective_lead=1.0,
            jump_l1_upper_bound=2.0,
            jump_first_moment_upper_bound=0.5,
            zero_frequency_spectrum_lower_bound=1.0,
        )
        short = finite_switch_matter_obstruction_record(spin, burn_in=1.0, **common)
        long = finite_switch_matter_obstruction_record(
            spin, burn_in=elapsed, **common
        )
        self.assertLess(
            long["spectral_residual"]["value"], short["spectral_residual"]["value"]
        )
        self.assertGreaterEqual(
            long["physical_any_decoder_witness_error_lower_bound"],
            short["physical_any_decoder_witness_error_lower_bound"],
        )
        self.assertEqual(
            long["result_type"],
            "spectral_witness_obstruction_not_diamond_transfer",
        )

    def test_stronger_zero_mode_lower_bound_improves_mixing(self):
        common = dict(
            spin=3,
            lapse=1.0,
            coupling=1.0e-4,
            elapsed_time=1.0e8,
            burn_in=1.0e8,
            switch_effective_lead=1.0,
            jump_l1_upper_bound=0.01,
            jump_first_moment_upper_bound=0.01,
        )
        weak = finite_switch_matter_obstruction_record(
            zero_frequency_spectrum_lower_bound=0.5, **common
        )
        strong = finite_switch_matter_obstruction_record(
            zero_frequency_spectrum_lower_bound=1.0, **common
        )
        self.assertLessEqual(
            strong["heat_to_haar_bound"]["value"],
            weak["heat_to_haar_bound"]["value"],
        )

    def test_larger_moment_bounds_weaken_spectral_transfer(self):
        common = dict(
            spin=3,
            lapse=1.0,
            coupling=1.0e-6,
            elapsed_time=1.0e11,
            burn_in=1.0e11,
            switch_effective_lead=1.0,
            zero_frequency_spectrum_lower_bound=1.0,
        )
        tight = finite_switch_matter_obstruction_record(
            jump_l1_upper_bound=0.1,
            jump_first_moment_upper_bound=0.1,
            **common,
        )
        loose = finite_switch_matter_obstruction_record(
            jump_l1_upper_bound=0.2,
            jump_first_moment_upper_bound=0.2,
            **common,
        )
        self.assertGreater(
            loose["spectral_residual"]["value"],
            tight["spectral_residual"]["value"],
        )
        self.assertLessEqual(
            loose["physical_any_decoder_witness_error_lower_bound"],
            tight["physical_any_decoder_witness_error_lower_bound"],
        )

    def test_certificate_records_open_physics_gates(self):
        certificate = static_patch_matter_observer_channel_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("AU.1", certificate["claim_boundary"])
        self.assertIn(
            "does not certify constructive diamond completeness",
            certificate["claim_boundary"],
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            NormalizedDiamondDistanceBound(1.1, "invalid")
        with self.assertRaises(ValueError):
            AncillaStableOperatorNormResidual(-0.1, "invalid")
        with self.assertRaises(ValueError):
            matter_collective_diffusion_rate_lower_bound(0.0, 1.0, 1.0)
        with self.assertRaises(ValueError):
            recovery_error_transfer_bracket(
                haar_any_decoder_lower_bound=0.8,
                haar_constructive_decoder_upper_bound=0.2,
                heat_to_haar_bound=NormalizedDiamondDistanceBound(0.0, "exact"),
                physical_to_heat_bound=NormalizedDiamondDistanceBound(0.0, "exact"),
            )


if __name__ == "__main__":
    unittest.main()
