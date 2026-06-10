import unittest
from math import exp

from qgtoy.geometric_thermal_type_no_go import (
    angular_frequency,
    angular_tail_geometric_sum,
    finite_shell_log_partition,
    finite_shell_vacuum_trace_distance,
    geometric_thermal_limit_record,
    geometric_thermal_type_no_go_certificate,
    log_partition_tail_upper_bound,
    massless_zero_mode_record,
    optical_volume_record,
    static_patch_optical_volume,
    trace_distance_to_thermal_limit_bound,
)


class GeometricThermalTypeNoGoTest(unittest.TestCase):
    def test_geometric_frequency_and_degeneracy_tail(self):
        self.assertAlmostEqual(angular_frequency(0, mass=1.5, radius=2.0), 1.5)
        self.assertGreater(angular_frequency(5, mass=1.5, radius=2.0), 1.5)
        beta = 1.3
        radius = 0.8
        q = exp(-beta / radius)
        for cutoff in range(0, 8):
            numerical = sum(
                (2 * level + 1) * q**level
                for level in range(cutoff + 1, cutoff + 1000)
            )
            self.assertAlmostEqual(
                angular_tail_geometric_sum(cutoff, beta=beta, radius=radius),
                numerical,
                places=13,
            )

    def test_analytic_tail_bound_dominates_actual_massive_tail(self):
        beta = 1.1
        mass = 0.7
        radius = 1.4
        for cutoff in range(0, 10):
            numerical_tail = sum(
                -(2 * level + 1)
                * __import__("math").log1p(
                    -exp(-beta * angular_frequency(level, mass=mass, radius=radius))
                )
                for level in range(cutoff + 1, cutoff + 2000)
            )
            self.assertLessEqual(
                numerical_tail,
                log_partition_tail_upper_bound(
                    cutoff,
                    beta=beta,
                    radius=radius,
                ),
            )

    def test_trace_distance_bound_decays_to_zero(self):
        bounds = tuple(
            trace_distance_to_thermal_limit_bound(
                cutoff,
                beta=2.0,
                radius=1.0,
            )
            for cutoff in range(0, 30)
        )
        self.assertTrue(all(right <= left for left, right in zip(bounds, bounds[1:])))
        self.assertLess(bounds[-1], 1e-20)

    def test_limit_is_type_i_and_core_is_not_typeii_factor(self):
        record = geometric_thermal_limit_record(12, beta=2.0, mass=1.0, radius=1.0)
        self.assertTrue(record["infinite_gibbs_density_is_trace_class"])
        self.assertTrue(record["cutoff_states_converge_in_trace_norm"])
        self.assertEqual(
            record["global_gns_algebra_under_declared_algebra"],
            "B(Fock), Type I_infinity",
        )
        self.assertIn("not a Type-II factor", record["continuous_core"])

    def test_finite_shell_trace_distance_identity_and_bound(self):
        for cutoff, tail_cutoff in ((0, 2), (2, 6), (5, 14)):
            shell_log_z = finite_shell_log_partition(
                cutoff,
                tail_cutoff,
                beta=1.7,
                mass=0.9,
                radius=1.2,
            )
            distance = finite_shell_vacuum_trace_distance(
                cutoff,
                tail_cutoff,
                beta=1.7,
                mass=0.9,
                radius=1.2,
            )
            self.assertAlmostEqual(distance, 1.0 - exp(-shell_log_z))
            self.assertLessEqual(distance, shell_log_z)

    def test_static_patch_optical_volume_has_inverse_distance_divergence(self):
        radius = 2.0
        ratios = []
        for power in (16.0, 64.0, 256.0, 1024.0, 4096.0):
            delta = radius / power
            volume = static_patch_optical_volume(
                radius=radius,
                stretched_distance=delta,
            )
            record = optical_volume_record(
                radius=radius,
                stretched_distance=delta,
            )
            self.assertAlmostEqual(record["optical_volume"], volume)
            ratios.append(record["scaled_asymptotic_ratio"])
        self.assertLess(abs(ratios[-1] - 1.0), abs(ratios[0] - 1.0))
        self.assertLess(abs(ratios[-1] - 1.0), 0.01)

    def test_massless_zero_mode_is_separated_from_type_classification(self):
        record = massless_zero_mode_record(beta=2.0, radius=1.0)
        self.assertFalse(record["global_gibbs_state_exists"])
        self.assertIn("infrared zero-mode", record["interpretation"])
        self.assertIn("free-particle", record["canonical_zero_mode"])

    def test_certificate_passes_at_declared_tolerance(self):
        certificate = geometric_thermal_type_no_go_certificate(
            max_cutoff=24,
            beta=2.0,
            mass=1.0,
            radius=1.0,
            tolerance=1e-10,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("localization and net structure", certificate["physical_consequence"])

    def test_extreme_temperature_parameters_do_not_break_certificate_logic(self):
        cold = geometric_thermal_type_no_go_certificate(
            max_cutoff=4,
            beta=1000.0,
            mass=1.0,
            radius=1.0,
            tolerance=1e-10,
        )
        self.assertEqual(cold["status"], "pass")

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            angular_frequency(-1, mass=1.0, radius=1.0)
        with self.assertRaises(ValueError):
            angular_frequency(1, mass=-1.0, radius=1.0)
        with self.assertRaises(ValueError):
            geometric_thermal_limit_record(1, mass=0.0)
        with self.assertRaises(ValueError):
            geometric_thermal_type_no_go_certificate(tolerance=0.0)
        with self.assertRaises(ValueError):
            finite_shell_log_partition(3, 3, beta=1.0, mass=1.0, radius=1.0)
        with self.assertRaises(ValueError):
            static_patch_optical_volume(radius=1.0, stretched_distance=1.0)


if __name__ == "__main__":
    unittest.main()
