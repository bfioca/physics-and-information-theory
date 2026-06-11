import math
import unittest
from decimal import Decimal

from qgtoy.u8a_finite_storage_channel import (
    normalized_diamond_bound_from_uniform_operator_residual,
    u8a_finite_storage_channel_certificate,
    u8a_finite_switch_channel_error_record,
    u8a_named_action_record,
    u8a_operational_risk_record,
)


class U8aFiniteStorageChannelTest(unittest.TestCase):
    def test_uniform_operator_residual_pays_full_channel_dimension(self):
        record = normalized_diamond_bound_from_uniform_operator_residual(
            1.0e-3,
            input_dimension=10,
            output_dimension=10,
        )
        self.assertEqual(
            record["traceless_hermitian_conversion_factor"],
            50,
        )
        self.assertAlmostEqual(record["normalized_diamond_bound"], 0.05)
        self.assertEqual(record["stabilizing_ancilla_dimension"], 10)

    def test_conversion_uses_input_times_output_not_one_state_dimension(self):
        record = normalized_diamond_bound_from_uniform_operator_residual(
            1.0e-4,
            input_dimension=25,
            output_dimension=25,
        )
        self.assertEqual(
            record["traceless_hermitian_conversion_factor"],
            math.floor(625 / 2),
        )
        self.assertAlmostEqual(
            record["raw_normalized_diamond_bound"],
            0.0312,
        )

    def test_channel_error_ledger_keeps_every_named_term(self):
        record = u8a_finite_switch_channel_error_record(
            1.0e-6,
            10.0,
            5.0,
            jump_l1_upper_bound=2.0,
            jump_first_moment_upper_bound=0.5,
        )
        components = record["normalized_diamond_components"]
        self.assertGreater(components["stationary_initial"], 0.0)
        self.assertGreater(components["stationary_growth"], 0.0)
        self.assertGreater(components["finite_switch_history"], 0.0)
        self.assertEqual(components["multipole"], 0.0)
        self.assertEqual(components["band_leakage"], 0.0)
        self.assertEqual(components["free_evolution"], 0.0)
        self.assertEqual(components["lamb_shift"], 0.0)
        self.assertAlmostEqual(
            record["normalized_diamond_total_before_clipping"],
            sum(components.values()),
        )

    def test_longer_burn_reduces_only_switch_history(self):
        common = dict(
            coupling=1.0e-6,
            elapsed_time=10.0,
            jump_l1_upper_bound=2.0,
            jump_first_moment_upper_bound=0.5,
        )
        short = u8a_finite_switch_channel_error_record(burn_in=1.0, **common)
        long = u8a_finite_switch_channel_error_record(burn_in=10.0, **common)
        short_components = short["operator_residual_components"]
        long_components = long["operator_residual_components"]
        self.assertEqual(
            short_components["stationary_initial"],
            long_components["stationary_initial"],
        )
        self.assertEqual(
            short_components["stationary_growth"],
            long_components["stationary_growth"],
        )
        self.assertLess(
            long_components["finite_switch_history"],
            short_components["finite_switch_history"],
        )

    def test_risk_composition_subtracts_physical_channel_error(self):
        record = u8a_operational_risk_record(
            heat_exposure=2.0,
            maximum_mean_casimir=1.8,
            physical_to_heat_diamond_bound=0.04,
            target_risk=0.5,
        )
        self.assertAlmostEqual(
            record["physical_operational_risk_floor"],
            record["best_effective_risk_floor"] - 0.04,
        )
        self.assertTrue(record["target_is_excluded"])
        self.assertGreater(
            record["operational_margin_before_physical_error"],
            0.04,
        )

    def test_named_action_uses_common_pre_switch_channel_domain(self):
        action = u8a_named_action_record()
        self.assertIn("dimension 10", action["register"])
        self.assertIn("same input time", action["comparison_channel"])
        self.assertIn("no autonomous map", action["comparison_channel"])
        self.assertIn("rigid-detector EFT", action["locality_scope"])
        self.assertIn("chi_(B,T)", action["switch"])
        self.assertIn("preserve", action["conserved_resource"])
        self.assertIn("U_free", action["comparison_channel"])
        self.assertIn("SO(3)-covariant", action["channel_covariance"])
        self.assertIn("Casimir", action["channel_covariance"])
        self.assertIn("commutator", action["locality_obstruction"])

    def test_certificate_records_conditional_box_and_locality_stop(self):
        certificate = u8a_finite_storage_channel_certificate()
        self.assertEqual(certificate["status"], "conditional_pass")
        self.assertTrue(
            all(certificate["verified_conditional_box_checks"].values())
        )
        self.assertFalse(any(certificate["open_bridge_checks"].values()))
        self.assertIn("CONDITIONAL", certificate["u8a_disposition"])
        self.assertIn("CONDITIONAL", certificate["detector_channel_status"])
        self.assertEqual(certificate["paper_u_u8a_status"], "OPEN")
        self.assertIn("INCONCLUSIVE STOP", certificate["route_terminal_status"])
        box = certificate["parameter_box"]
        coupling_lower, coupling_upper = box[
            "coupling_lambda_open_interval"
        ]
        self.assertGreater(coupling_lower, 0.0)
        self.assertGreater(coupling_upper, coupling_lower)
        for key in (
            "burn_in_B_open_interval",
            "storage_time_T_open_interval",
            "total_protocol_duration_open_bounds",
        ):
            lower, upper = box[key]
            self.assertGreater(lower, 0.0)
            self.assertGreater(upper, lower)
        self.assertLess(
            certificate["worst_corner_channel_error"][
                "normalized_diamond_bound"
            ],
            box["declared_channel_error_bound"],
        )
        self.assertGreater(
            box["heat_exposure_range"][0],
            box["declared_failure_exposure_threshold"],
        )
        guard = certificate["decimal_box_guard"]
        self.assertIn("ROUND_FLOOR", guard["rounding_policy"])
        self.assertIn("one Decimal ulp", guard["rounding_policy"])
        enclosure = certificate["analytic_profile_enclosure"]
        self.assertEqual(enclosure["radius_exact"], "1")
        self.assertEqual(enclosure["support_radius_exact"], "1/5")
        self.assertEqual(
            enclosure["transform_tail_envelope"][
                "support_radius_ratio_exact"
            ],
            "1/5",
        )
        self.assertTrue(guard["all_guards_pass"])
        self.assertTrue(all(guard["guards"].values()))
        self.assertLess(
            Decimal(guard["normalized_diamond_upper_bound"]),
            Decimal("0.039"),
        )
        self.assertGreater(
            Decimal(guard["u7_physical_risk_floor_at_s_0p7_eta_0p039"]),
            Decimal("0.5"),
        )
        self.assertGreater(
            certificate["minimum_exposure_risk_composition"][
                "physical_operational_risk_floor"
            ],
            0.5,
        )
        self.assertIn("not", certificate["box_disposition"])
        self.assertIn("U8b remains open", certificate["claim_boundary"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            normalized_diamond_bound_from_uniform_operator_residual(
                -1.0,
                input_dimension=1,
                output_dimension=1,
            )
        with self.assertRaises(ValueError):
            u8a_finite_switch_channel_error_record(
                1.0,
                1.0,
                0.0,
                jump_l1_upper_bound=1.0,
                jump_first_moment_upper_bound=1.0,
            )
        with self.assertRaises(ValueError):
            u8a_operational_risk_record(
                heat_exposure=1.0,
                maximum_mean_casimir=1.0,
                physical_to_heat_diamond_bound=1.1,
                target_risk=0.5,
            )


if __name__ == "__main__":
    unittest.main()
