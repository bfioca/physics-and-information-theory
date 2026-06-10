import unittest
from math import log, pi

from qgtoy.redshifted_frame_capacity import (
    angular_cutoff_asymptotic_coefficient,
    collar_static_energy_upper_bound,
    conformal_radial_potential,
    directional_token_expected_energy_upper_bound,
    directional_token_irrep_amplitudes,
    directional_token_irrep_weights,
    finite_wall_ground_frequency_upper_bound,
    hard_static_energy_subspace_dimension_lower_bound,
    maximum_bounded_energy_angular_momentum,
    missing_rotation_frame_relative_entropy,
    redshifted_frame_capacity_certificate,
    redshifted_frame_capacity_record,
    sine_collar_kinetic_constant,
    stretched_horizon_proper_distance,
    truncated_scalar_harmonic_dimension,
)


class RedshiftedFrameCapacityTest(unittest.TestCase):
    def test_conformal_potential_decreases_toward_horizon(self):
        values = tuple(
            conformal_radial_potential(5, radius=1.0, tortoise_coordinate=x)
            for x in (0.5, 1.0, 2.0, 4.0)
        )
        self.assertTrue(all(right < left for left, right in zip(values, values[1:])))

    def test_sine_collar_kinetic_constant(self):
        self.assertAlmostEqual(
            sine_collar_kinetic_constant(inner_offset=0.5, outer_offset=1.5),
            pi * pi,
        )

    def test_maximum_cutoff_respects_and_saturates_bound(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 1024.0,
            energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
        )
        cutoff = maximum_bounded_energy_angular_momentum(**parameters)
        energy_parameters = {
            key: value for key, value in parameters.items() if key != "energy_budget"
        }
        self.assertLessEqual(
            collar_static_energy_upper_bound(cutoff, **energy_parameters),
            parameters["energy_budget"],
        )
        self.assertGreater(
            collar_static_energy_upper_bound(cutoff + 1, **energy_parameters),
            parameters["energy_budget"],
        )

    def test_directional_token_twirl_is_uniform(self):
        cutoff = 7
        dimension = truncated_scalar_harmonic_dimension(cutoff)
        weights = directional_token_irrep_weights(cutoff)
        amplitudes = directional_token_irrep_amplitudes(cutoff)
        self.assertAlmostEqual(sum(weights), 1.0)
        self.assertAlmostEqual(sum(value * value for value in amplitudes), 1.0)
        for angular_momentum, weight in enumerate(weights):
            self.assertAlmostEqual(weight / (2 * angular_momentum + 1), 1.0 / dimension)
        self.assertAlmostEqual(
            missing_rotation_frame_relative_entropy(cutoff),
            log(dimension),
        )

    def test_declared_pure_token_respects_energy_budget(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 4096.0,
            energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
        )
        cutoff = maximum_bounded_energy_angular_momentum(**parameters)
        bound = directional_token_expected_energy_upper_bound(
            maximum_angular_momentum=cutoff,
            radius=parameters["radius"],
            stretched_distance=parameters["stretched_distance"],
            inner_offset=parameters["inner_offset"],
            outer_offset=parameters["outer_offset"],
        )
        self.assertLessEqual(bound, parameters["energy_budget"])

    def test_min_max_supplies_hard_energy_spin_subspace(self):
        parameters = dict(
            radius=1.0,
            stretched_distance=1.0 / 4096.0,
            energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
        )
        cutoff = maximum_bounded_energy_angular_momentum(**parameters)
        energy_parameters = {
            key: value for key, value in parameters.items() if key != "energy_budget"
        }
        self.assertLessEqual(
            finite_wall_ground_frequency_upper_bound(
                cutoff,
                **energy_parameters,
            ),
            parameters["energy_budget"],
        )
        self.assertEqual(
            hard_static_energy_subspace_dimension_lower_bound(**parameters),
            truncated_scalar_harmonic_dimension(cutoff),
        )

    def test_angular_cutoff_asymptotic_coefficient(self):
        coefficient = angular_cutoff_asymptotic_coefficient(
            radius=1.0,
            energy_budget=4.0,
            inner_offset=0.5,
            outer_offset=1.5,
        )
        scaled = []
        for power in (4096.0, 16384.0, 65536.0, 262144.0):
            delta = 1.0 / power
            cutoff = maximum_bounded_energy_angular_momentum(
                radius=1.0,
                stretched_distance=delta,
                energy_budget=4.0,
                inner_offset=0.5,
                outer_offset=1.5,
            )
            scaled.append(cutoff * cutoff * delta)
        self.assertLess(abs(scaled[-1] - coefficient), 0.04 * coefficient)

    def test_missing_frame_entropy_has_logarithmic_growth(self):
        offsets = []
        for power in (4096.0, 16384.0, 65536.0, 262144.0):
            delta = 1.0 / power
            record = redshifted_frame_capacity_record(
                radius=1.0,
                stretched_distance=delta,
                energy_budget=4.0,
                inner_offset=0.5,
                outer_offset=1.5,
            )
            offsets.append(
                record["missing_rotation_frame_relative_entropy"]
                - record["log_R_over_delta"]
            )
        self.assertLess(max(offsets[-3:]) - min(offsets[-3:]), 0.08)

    def test_proper_distance_conversion(self):
        radius = 2.0
        delta = radius / 100000.0
        rho = stretched_horizon_proper_distance(
            radius=radius,
            stretched_distance=delta,
        )
        self.assertAlmostEqual(delta, rho * rho / (2.0 * radius), delta=2e-10)
        area = 4.0 * pi * radius * radius
        self.assertAlmostEqual(
            log(radius / delta),
            log(area / (2.0 * pi * rho * rho)),
            delta=2e-5,
        )
        tiny = stretched_horizon_proper_distance(
            radius=1.0,
            stretched_distance=1e-30,
        )
        self.assertGreater(tiny, 0.0)
        self.assertAlmostEqual(tiny, (2e-30) ** 0.5, delta=1e-29)

    def test_certificate_passes_with_gravity_boundary(self):
        certificate = redshifted_frame_capacity_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("no backreaction bound", certificate["claim_boundary"])
        self.assertIn("log(R/delta)", certificate["central_result"])

    def test_validation(self):
        with self.assertRaises(ValueError):
            conformal_radial_potential(-1, radius=1.0, tortoise_coordinate=1.0)
        with self.assertRaises(ValueError):
            maximum_bounded_energy_angular_momentum(
                radius=1.0,
                stretched_distance=0.1,
                energy_budget=1.0,
                inner_offset=0.5,
                outer_offset=1.5,
            )
        with self.assertRaises(ValueError):
            stretched_horizon_proper_distance(radius=1.0, stretched_distance=1.0)
        with self.assertRaises(ValueError):
            redshifted_frame_capacity_certificate(minimum_power=8)
        with self.assertRaises(ValueError):
            redshifted_frame_capacity_certificate(steps=65)


if __name__ == "__main__":
    unittest.main()
