import math
import unittest

from qgtoy.__main__ import build_parser
from qgtoy.collective_band_feshbach import (
    collective_band_feshbach_certificate,
    complement_weight_upper_bound,
    constant_floor_rotational_partition_partial_sum,
    feshbach_sector_floor_lower_bound,
    fractional_collective_floor_transfer,
    growing_diagonal_constant_floor_counterexample,
    induced_collective_quartic_coefficient,
    schur_sector_floor_lower_bound,
    scale_uniform_collective_floor_transfer,
    unconstrained_band_completion_counterexample,
)


class CollectiveBandFeshbachTest(unittest.TestCase):
    def test_exact_scalar_comparison_eigenvalue(self):
        a = 2.0
        d = 7.0
        coupling = 1.5
        expected = 0.5 * (a + d - math.sqrt((d - a) ** 2 + 4 * coupling**2))
        self.assertAlmostEqual(
            feshbach_sector_floor_lower_bound(
                collective_floor=a,
                complement_floor=d,
                band_coupling_norm=coupling,
            ),
            expected,
        )

    def test_schur_bound_is_conservative(self):
        exact = feshbach_sector_floor_lower_bound(
            collective_floor=4.0,
            complement_floor=10.0,
            band_coupling_norm=1.0,
        )
        schur = schur_sector_floor_lower_bound(
            collective_floor=4.0,
            complement_floor=10.0,
            band_coupling_norm=1.0,
        )
        self.assertGreaterEqual(exact, schur)

    def test_fractional_transfer_condition(self):
        record = fractional_collective_floor_transfer(
            collective_floor=9.0,
            complement_gap=4.0,
            relative_coupling_budget=0.2,
        )
        self.assertTrue(record["exact_comparison_dominates_transferred_floor"])
        self.assertEqual(record["transferred_floor"], 7.2)

    def test_eigenvector_leakage_bound(self):
        leakage = complement_weight_upper_bound(
            eigenvalue_upper_bound=2.0,
            complement_floor=10.0,
            band_coupling_norm=1.0,
        )
        self.assertAlmostEqual(leakage, 1.0 / 65.0)

    def test_scale_uniform_transfer_and_threshold(self):
        passing = scale_uniform_collective_floor_transfer(
            collective_floor=5.0,
            complement_ratio=2.0,
            coupling_ratio=0.5,
        )
        threshold = scale_uniform_collective_floor_transfer(
            collective_floor=5.0,
            complement_ratio=2.0,
            coupling_ratio=math.sqrt(2.0),
        )
        self.assertTrue(passing["transferred_fraction_is_strictly_positive"])
        self.assertAlmostEqual(threshold["transferred_fraction_kappa"], 0.0)
        self.assertFalse(
            threshold["strict_positivity_condition_rho_squared_below_gamma"]
        )

    def test_soft_mode_makes_induced_quartic_unbounded(self):
        stiff = induced_collective_quartic_coefficient(
            inertia_mode_coupling=1.0,
            mode_stiffness=1.0,
        )
        soft = induced_collective_quartic_coefficient(
            inertia_mode_coupling=1.0,
            mode_stiffness=1e-6,
        )
        self.assertEqual(stiff, 0.5)
        self.assertGreater(soft, 1e5)

    def test_positive_completion_collapses_collective_floor(self):
        records = tuple(
            unconstrained_band_completion_counterexample(
                collective_floor=3.0,
                retained_fraction=fraction,
            )
            for fraction in (0.5, 0.1, 0.01, 0.001)
        )
        self.assertTrue(
            all(record["completion_is_positive_semidefinite"] for record in records)
        )
        self.assertTrue(
            all(
                right["full_sector_floor"] < left["full_sector_floor"]
                for left, right in zip(records, records[1:])
            )
        )
        self.assertAlmostEqual(records[-1]["full_sector_floor"], 0.003)

    def test_growing_diagonal_blocks_can_retain_a_constant_full_floor(self):
        records = tuple(
            growing_diagonal_constant_floor_counterexample(
                collective_floor=floor,
                residual_floor=0.25,
            )
            for floor in (1.0, 10.0, 100.0, 1000.0)
        )
        self.assertTrue(
            all(
                abs(record["full_sector_floor"] - 0.25) < 1e-10
                for record in records
            )
        )

    def test_constant_floor_partition_diverges_with_cutoff(self):
        values = tuple(
            constant_floor_rotational_partition_partial_sum(
                cutoff,
                dual_parameter=1.0,
                residual_floor=0.25,
                projective=True,
            )
            for cutoff in (10, 100, 1000)
        )
        self.assertTrue(all(right > left for left, right in zip(values, values[1:])))
        self.assertGreater(values[-1] / values[-2], 900.0)

    def test_certificate_records_open_physical_gate(self):
        certificate = collective_band_feshbach_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertEqual(
            certificate["current_skyrmion_evidence"]["physical_full_band_gate"],
            "open",
        )

    def test_cli_registration(self):
        args = build_parser().parse_args(["collective-band-feshbach"])
        self.assertEqual(args.func.__name__, "run_collective_band_feshbach")

    def test_validation(self):
        with self.assertRaises(ValueError):
            schur_sector_floor_lower_bound(
                collective_floor=2.0,
                complement_floor=2.0,
                band_coupling_norm=0.1,
            )
        with self.assertRaises(ValueError):
            fractional_collective_floor_transfer(
                collective_floor=1.0,
                complement_gap=1.0,
                relative_coupling_budget=1.0,
            )
        with self.assertRaises(ValueError):
            complement_weight_upper_bound(
                eigenvalue_upper_bound=2.0,
                complement_floor=1.0,
                band_coupling_norm=0.1,
            )


if __name__ == "__main__":
    unittest.main()
