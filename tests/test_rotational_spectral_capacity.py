import math
import unittest

from qgtoy.global_so3_reference_risk import (
    asymmetry_orientation_risk_lower_bound,
    mean_casimir_orientation_risk_lower_bound,
)
from qgtoy.rotational_spectral_capacity import (
    bounded_spectrum_counterexample_record,
    casimir_coercive_orientation_risk_lower_bound,
    finite_rotational_partition_function,
    gibbs_spectral_asymmetry_upper_bound,
    gibbs_spectral_orientation_risk_lower_bound,
    log_finite_rotational_partition_function,
    sector_tail_probability_upper_bound,
    spectral_tail_orientation_risk_lower_bound,
)


class RotationalSpectralCapacityTest(unittest.TestCase):
    def test_finite_partition_uses_representation_dimension_squared(self):
        beta = 0.7
        floors = (0.0, 2.0, 6.0)
        expected = sum(
            (2 * spin + 1) ** 2 * math.exp(-beta * floor)
            for spin, floor in enumerate(floors)
        )
        self.assertAlmostEqual(
            finite_rotational_partition_function(
                floors,
                dual_parameter=beta,
            ),
            expected,
        )

    def test_projective_partition_starts_at_spin_one_half(self):
        self.assertAlmostEqual(
            finite_rotational_partition_function(
                (0.75, 3.75),
                dual_parameter=1.0,
                projective=True,
            ),
            4.0 * math.exp(-0.75) + 16.0 * math.exp(-3.75),
        )

    def test_log_partition_remains_finite_after_direct_underflow(self):
        value = log_finite_rotational_partition_function(
            (10000.0, 10001.0),
            dual_parameter=1.0,
        )
        self.assertTrue(math.isfinite(value))
        self.assertLess(value, -9990.0)

    def test_gibbs_capacity_composes_with_global_risk(self):
        kwargs = {
            "mean_energy": 1.25,
            "sector_energy_floors": (0.0, 1.0, 4.0),
            "dual_parameter": 0.8,
        }
        capacity = gibbs_spectral_asymmetry_upper_bound(**kwargs)
        risk = gibbs_spectral_orientation_risk_lower_bound(**kwargs)
        self.assertAlmostEqual(
            risk,
            asymmetry_orientation_risk_lower_bound(capacity),
        )

    def test_casimir_coercivity_matches_existing_all_state_floor(self):
        energy = 2.5
        alpha = 0.25
        self.assertAlmostEqual(
            casimir_coercive_orientation_risk_lower_bound(
                mean_energy=energy,
                casimir_gap_coefficient=alpha,
            ),
            mean_casimir_orientation_risk_lower_bound(energy / alpha),
        )

    def test_spectral_tail_transfer_handles_integer_and_projective_sectors(self):
        tail = sector_tail_probability_upper_bound(
            mean_energy=1.0,
            first_excluded_sector_energy=100.0,
        )
        self.assertAlmostEqual(tail, 0.01)
        integer = spectral_tail_orientation_risk_lower_bound(
            reference_cutoff=2,
            mean_energy=1.0,
            first_excluded_sector_energy=100.0,
        )
        projective = spectral_tail_orientation_risk_lower_bound(
            reference_cutoff=2,
            mean_energy=1.0,
            first_excluded_sector_energy=100.0,
            projective=True,
        )
        self.assertGreater(integer, 0.0)
        self.assertGreater(projective, 0.0)

    def test_fixed_bounded_spectrum_is_an_energy_capacity_obstruction(self):
        records = tuple(
            bounded_spectrum_counterexample_record(cutoff)
            for cutoff in (0, 1, 3, 10, 100, 1000)
        )
        self.assertTrue(all(record["status"] == "pass" for record in records))
        self.assertTrue(
            all(
                right["cutoff_token_achievable_orientation_risk"]
                < left["cutoff_token_achievable_orientation_risk"]
                for left, right in zip(records, records[1:])
            )
        )
        self.assertLess(
            records[-1]["cutoff_token_achievable_orientation_risk"],
            0.001,
        )
        self.assertTrue(
            all(
                record["cutoff_token_mean_energy_upper_bound"] <= 1.0
                for record in records
            )
        )

    def test_validation(self):
        with self.assertRaises(ValueError):
            finite_rotational_partition_function((), dual_parameter=1.0)
        with self.assertRaises(ValueError):
            finite_rotational_partition_function((-1.0,), dual_parameter=1.0)
        with self.assertRaises(ValueError):
            casimir_coercive_orientation_risk_lower_bound(
                mean_energy=1.0,
                casimir_gap_coefficient=0.0,
            )
        with self.assertRaises(ValueError):
            bounded_spectrum_counterexample_record(True)


if __name__ == "__main__":
    unittest.main()
