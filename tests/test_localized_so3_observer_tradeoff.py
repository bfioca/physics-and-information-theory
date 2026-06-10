import math
import unittest

from qgtoy.global_so3_reference_risk import (
    mean_casimir_orientation_risk_lower_bound,
)
from qgtoy.localized_so3_observer_tradeoff import (
    localized_so3_observer_tradeoff_certificate,
    localized_so3_observer_tradeoff_record,
    minimum_compact_rotor_radius_for_orientation_risk,
    required_mean_casimir_for_orientation_risk,
)


class LocalizedSO3ObserverTradeoffTest(unittest.TestCase):
    def test_direct_risk_inversion(self):
        for risk in (0.01, 0.05, 0.1):
            required = required_mean_casimir_for_orientation_risk(risk)
            self.assertAlmostEqual(
                mean_casimir_orientation_risk_lower_bound(required),
                risk,
                places=14,
            )
        self.assertEqual(required_mean_casimir_for_orientation_risk(0.2), 0.0)

    def test_radius_floor_has_expected_scaling(self):
        arguments = {
            "risk_budget": 0.05,
            "newton_constant": 1.0e-12,
            "inertia_coefficient": 2.0 / 3.0,
            "compactness_margin": 0.5,
            "maximum_excitation_fraction": 0.25,
        }
        radius = minimum_compact_rotor_radius_for_orientation_risk(**arguments)
        doubled_g = minimum_compact_rotor_radius_for_orientation_risk(
            **{**arguments, "newton_constant": 2.0e-12}
        )
        self.assertAlmostEqual(doubled_g / radius, math.sqrt(2.0), places=12)

    def test_long_protocol_closes_every_heat_window(self):
        record = localized_so3_observer_tradeoff_record(
            2,
            risk_budget=0.1,
            proper_protocol_time=10.0,
            reference_diffusion_rate=1.0,
        )
        self.assertTrue(record["all_necessary_windows_closed"])
        self.assertTrue(
            all(
                not design["coherence_condition_not_excluded"]
                for design in record["design_windows"]
            )
        )

    def test_certificate(self):
        certificate = localized_so3_observer_tradeoff_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_validation(self):
        with self.assertRaises(ValueError):
            required_mean_casimir_for_orientation_risk(0.0)
        with self.assertRaises(ValueError):
            localized_so3_observer_tradeoff_record(
                True,
                risk_budget=0.1,
                proper_protocol_time=0.1,
                reference_diffusion_rate=1.0,
            )
        with self.assertRaises(ValueError):
            localized_so3_observer_tradeoff_record(
                2,
                risk_budget=0.8,
                proper_protocol_time=0.1,
                reference_diffusion_rate=1.0,
            )


if __name__ == "__main__":
    unittest.main()
