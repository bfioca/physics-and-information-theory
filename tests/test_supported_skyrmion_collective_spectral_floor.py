import math
import unittest

from qgtoy.__main__ import build_parser
from qgtoy.supported_skyrmion_collective_spectral_floor import (
    linear_sector_log_partition_upper_bound,
    supported_hedgehog_density_bound_slack,
    supported_hedgehog_high_spin_tail_upper_bound,
    supported_hedgehog_inertia_coefficient,
    supported_hedgehog_orientation_risk_lower_bound,
    supported_hedgehog_sector_energy_floor,
    supported_skyrmion_collective_spectral_floor_certificate,
)


class SupportedSkyrmionCollectiveSpectralFloorTest(unittest.TestCase):
    def test_inertia_mass_radius_coefficient(self):
        self.assertAlmostEqual(
            supported_hedgehog_inertia_coefficient(
                wall_radius=4.0,
                curvature=0.0025,
            ),
            4.0 / (3.0 * 0.96),
        )

    def test_pointwise_density_inequality_on_adversarial_samples(self):
        samples = (
            (0.05, math.pi - 0.1, -2.0),
            (0.5, 2.0, -0.01),
            (1.0, math.pi / 2.0, -10.0),
            (3.9, 0.2, -1.0),
            (4.0, 0.0, -0.5),
        )
        for radius, profile, derivative in samples:
            self.assertGreaterEqual(
                supported_hedgehog_density_bound_slack(
                    radius,
                    profile,
                    derivative,
                    pion_mass=1.0,
                    curvature=0.0025,
                    wall_radius=4.0,
                ),
                -1e-12,
            )

    def test_sector_floor_grows_as_square_root_casimir(self):
        floors = tuple(
            supported_hedgehog_sector_energy_floor(
                spin,
                physical_support_radius=4.0,
                wall_lapse=0.96,
            )
            for spin in (0.5, 1.5, 10.5, 100.5)
        )
        self.assertTrue(all(right > left for left, right in zip(floors, floors[1:])))
        spin = 10000.5
        floor = supported_hedgehog_sector_energy_floor(
            spin,
            physical_support_radius=4.0,
            wall_lapse=0.96,
        )
        slope = math.sqrt(1.5 * 0.96) / 4.0
        self.assertAlmostEqual(floor / spin, slope, places=4)

    def test_integer_and_projective_partition_bounds_are_finite(self):
        for projective in (False, True):
            value = linear_sector_log_partition_upper_bound(
                dual_parameter=0.2,
                physical_support_radius=4.0,
                wall_lapse=0.96,
                projective=projective,
            )
            self.assertTrue(math.isfinite(value))

    def test_energy_gives_positive_projective_global_risk_floor(self):
        risk = supported_hedgehog_orientation_risk_lower_bound(
            mean_total_energy=50.0,
            dual_parameter=0.1,
            physical_support_radius=4.0,
            wall_lapse=0.96,
            projective=True,
        )
        self.assertGreater(risk, 0.0)

    def test_high_spin_tail_vanishes_with_cutoff(self):
        tails = tuple(
            supported_hedgehog_high_spin_tail_upper_bound(
                mean_total_energy=1.0,
                reference_cutoff=cutoff,
                physical_support_radius=4.0,
                wall_lapse=0.96,
                projective=True,
            )
            for cutoff in (0, 3, 10, 100, 1000)
        )
        self.assertTrue(all(right < left for left, right in zip(tails, tails[1:])))
        self.assertLess(tails[-1], 0.01)

    def test_certificate(self):
        certificate = supported_skyrmion_collective_spectral_floor_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("noncollective", certificate["claim_boundary"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(
            ["supported-skyrmion-collective-spectral-floor"]
        )
        self.assertEqual(args.wall_radius, 4.0)
        self.assertEqual(args.energy_multiplier, 1.1)
        self.assertEqual(args.dual_parameter, 0.1)

    def test_validation(self):
        with self.assertRaises(ValueError):
            supported_hedgehog_inertia_coefficient(
                wall_radius=4.0,
                curvature=1.0,
            )
        with self.assertRaises(ValueError):
            supported_hedgehog_sector_energy_floor(
                -0.5,
                physical_support_radius=4.0,
                wall_lapse=0.96,
            )
        with self.assertRaises(ValueError):
            supported_hedgehog_high_spin_tail_upper_bound(
                mean_total_energy=1.0,
                reference_cutoff=True,
                physical_support_radius=4.0,
                wall_lapse=0.96,
            )


if __name__ == "__main__":
    unittest.main()
