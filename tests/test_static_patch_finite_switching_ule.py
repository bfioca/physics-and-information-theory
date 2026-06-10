import unittest
from math import log1p

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_finite_switching_ule import (
    ancilla_stable_finite_switch_ule_residual_bound,
    finite_switch_logarithmic_heat_ule_coupling_cap,
    finite_switch_logarithmic_heat_ule_residual_bound,
    minimum_burn_in_for_switch_error,
    required_effective_age_for_bounded_heat_coefficient,
    static_patch_finite_switching_ule_certificate,
    switch_effective_lead_time_lower_bound,
)
from qgtoy.static_patch_worldtube_ule import (
    ancilla_stable_ule_spectral_residual_bound,
)


class StaticPatchFiniteSwitchingUleTest(unittest.TestCase):
    def test_lipschitz_lead_and_linear_ramp(self):
        self.assertEqual(switch_effective_lead_time_lower_bound(0.25), 4.0)

    def test_logarithmic_switch_residual(self):
        spin = 5
        lapse = 0.2
        coupling = 0.01
        elapsed = 0.7
        burn_in = 3.0
        switch_lead = 2.0
        jump_l1 = 2.0
        first_moment = 0.6
        stationary = ancilla_stable_ule_spectral_residual_bound(
            spin,
            lapse,
            coupling,
            elapsed,
            jump_l1,
            first_moment,
        )
        gamma_tau = (
            144.0
            * coupling**2
            * spin**2
            * jump_l1
            * first_moment
            / lapse**2
        )
        switched = ancilla_stable_finite_switch_ule_residual_bound(
            spin,
            lapse,
            coupling,
            elapsed,
            burn_in,
            switch_lead,
            jump_l1,
            first_moment,
        )
        self.assertAlmostEqual(
            switched,
            stationary + gamma_tau * log1p(elapsed / (burn_in + switch_lead)),
        )

    def test_minimum_burn_in_saturates_switch_budget(self):
        elapsed = 10.0
        lead = 2.0
        gamma_tau = 0.3
        budget = 0.1
        burn = minimum_burn_in_for_switch_error(
            elapsed,
            lead,
            gamma_tau,
            budget,
        )
        self.assertAlmostEqual(
            gamma_tau * log1p(elapsed / (burn + lead)),
            budget,
        )

    def test_heat_cap_saturates_beta_scheduled_bound(self):
        spin = 100
        dimension = 2 * spin + 1
        lapse = 1.0 / dimension
        budget = 1.0 / (4.0 * dimension)
        jump_l1 = 3.0
        first_moment = 1.0
        cap = finite_switch_logarithmic_heat_ule_coupling_cap(
            spin,
            lapse,
            budget,
            jump_l1,
            first_moment,
            burnin_rate_multiples=10.0,
        )
        self.assertAlmostEqual(
            finite_switch_logarithmic_heat_ule_residual_bound(
                spin,
                lapse,
                cap,
                jump_l1,
                first_moment,
                burnin_rate_multiples=10.0,
            ),
            budget,
        )

    def test_bound_level_preparation_age(self):
        age = required_effective_age_for_bounded_heat_coefficient(
            5,
            0.2,
            0.01,
            2.0,
            burnin_rate_multiples=10.0,
        )
        gamma_upper = 144.0 * 0.01**2 * 5**2 * 2.0**2 / 0.2**2
        self.assertAlmostEqual(age, 10.0 / gamma_upper)
        self.assertEqual(
            required_effective_age_for_bounded_heat_coefficient(
                5, 0.2, 0.0, 2.0
            ),
            0.0,
        )

    def test_certificate_and_cli(self):
        certificate = static_patch_finite_switching_ule_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["executable_checks"].values()))
        self.assertIn("mathematical witnesses", certificate["preparation_condition_status"])
        self.assertGreaterEqual(len(certificate["records"]), 2)
        for record in certificate["records"]:
            for name in (
                "constant_obstruction_schedule",
                "heat_matching_schedule",
            ):
                schedule = record[name]
                self.assertGreater(
                    schedule["required_bound_level_effective_age"], 0.0
                )
                self.assertLessEqual(
                    schedule["finite_burnin_witness_residual"],
                    schedule["spectral_residual_budget"],
                )
        args = build_parser().parse_args(["static-patch-finite-switching-ule"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.burnin_rate_multiples, 10.0)

    def test_certificate_accepts_nondefault_positive_beta(self):
        certificate = static_patch_finite_switching_ule_certificate(
            maximum_spin=256,
            burnin_rate_multiples=1.0,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["executable_checks"].values()))
        self.assertFalse(certificate["default_three_percent_penalty_diagnostic"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            switch_effective_lead_time_lower_bound(0.0)
        with self.assertRaises(ValueError):
            ancilla_stable_finite_switch_ule_residual_bound(
                1, 1.0, 0.1, 1.0, 0.0, 0.0, 1.0, 1.0
            )
        with self.assertRaises(ValueError):
            static_patch_finite_switching_ule_certificate(
                burnin_rate_multiples=0.0
            )
        with self.assertRaises(ValueError):
            static_patch_finite_switching_ule_certificate(maximum_spin=64)


if __name__ == "__main__":
    unittest.main()
