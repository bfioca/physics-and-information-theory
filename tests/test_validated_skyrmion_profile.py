import unittest
from fractions import Fraction

from qgtoy.massive_skyrmion_worldtube import curved_profile_acceleration
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_profile import (
    SkyrmionStateBox,
    SkyrmionTaylorCell,
    conditional_picard_foundation_certificate,
    conditional_taylor_foundation_certificate,
    curved_skyrmion_acceleration_box,
    curved_skyrmion_acceleration_jacobian_box,
    skyrmion_origin_cubic_coefficient_interval,
    validate_skyrmion_picard_step,
    validate_skyrmion_taylor_cell,
    validate_skyrmion_taylor_track,
    validated_skyrmion_profile_foundation_certificate,
)


class ValidatedSkyrmionProfileTest(unittest.TestCase):
    def _conditional_taylor_data(self):
        initial = SkyrmionStateBox(
            RationalInterval(
                Fraction(2983595, 1_000_000),
                Fraction(2983596, 1_000_000),
            ),
            RationalInterval(
                Fraction(-1575269, 1_000_000),
                Fraction(-1575267, 1_000_000),
            ),
        )
        step = Fraction(1, 1_000_000)
        profile_center = Fraction(5967191, 2_000_000)
        derivative_center = Fraction(-1575268, 1_000_000)
        linear = step * derivative_center
        first = SkyrmionTaylorCell(
            radius_start=Fraction(1001, 10_000),
            step=step,
            profile_polynomial=RationalPolynomial(
                (profile_center, linear)
            ),
            profile_radius=Fraction(1, 1_000_000),
            derivative_radius=Fraction(1, 100_000),
        )
        second = SkyrmionTaylorCell(
            radius_start=first.radius_start + step,
            step=step,
            profile_polynomial=RationalPolynomial(
                (profile_center + linear, linear)
            ),
            profile_radius=Fraction(2, 1_000_000),
            derivative_radius=Fraction(2, 100_000),
        )
        return initial, first, second

    def test_interval_vector_field_contains_point_evaluation(self):
        radius = Fraction(1, 10)
        profile = Fraction(29835955, 10_000_000)
        derivative = Fraction(-1575268, 1_000_000)
        enclosure = curved_skyrmion_acceleration_box(
            RationalInterval.point(radius),
            RationalInterval.point(profile),
            RationalInterval.point(derivative),
        )
        floating = curved_profile_acceleration(
            float(radius),
            float(profile),
            float(derivative),
            pion_mass=1.0,
            curvature=0.0025,
        )
        self.assertLessEqual(float(enclosure.lower) - 1.0e-12, floating)
        self.assertGreaterEqual(float(enclosure.upper) + 1.0e-12, floating)

    def test_interval_jacobian_contains_floating_finite_differences(self):
        radius = Fraction(1, 10)
        profile = Fraction(29835955, 10_000_000)
        derivative = Fraction(-1575268, 1_000_000)
        enclosure = curved_skyrmion_acceleration_jacobian_box(
            RationalInterval(
                radius - Fraction(1, 1_000_000),
                radius + Fraction(1, 1_000_000),
            ),
            RationalInterval(
                profile - Fraction(1, 1_000_000),
                profile + Fraction(1, 1_000_000),
            ),
            RationalInterval(
                derivative - Fraction(1, 1_000_000),
                derivative + Fraction(1, 1_000_000),
            ),
        )
        step = 1.0e-6

        def acceleration(profile_value, derivative_value):
            return curved_profile_acceleration(
                float(radius),
                profile_value,
                derivative_value,
                pion_mass=1.0,
                curvature=0.0025,
            )

        profile_float = float(profile)
        derivative_float = float(derivative)
        profile_difference = (
            acceleration(profile_float + step, derivative_float)
            - acceleration(profile_float - step, derivative_float)
        ) / (2 * step)
        derivative_difference = (
            acceleration(profile_float, derivative_float + step)
            - acceleration(profile_float, derivative_float - step)
        ) / (2 * step)
        self.assertLessEqual(
            float(enclosure.profile_derivative.lower), profile_difference
        )
        self.assertGreaterEqual(
            float(enclosure.profile_derivative.upper), profile_difference
        )
        self.assertLessEqual(
            float(enclosure.derivative_derivative.lower),
            derivative_difference,
        )
        self.assertGreaterEqual(
            float(enclosure.derivative_derivative.upper),
            derivative_difference,
        )

    def test_conditional_picard_step_and_tamper_rejection(self):
        initial = SkyrmionStateBox(
            RationalInterval(Fraction(2983595, 1_000_000), Fraction(2983596, 1_000_000)),
            RationalInterval(Fraction(-1575269, 1_000_000), Fraction(-1575267, 1_000_000)),
        )
        tube = SkyrmionStateBox(
            RationalInterval(Fraction(2983436, 1_000_000), Fraction(2983597, 1_000_000)),
            RationalInterval(Fraction(-1575280, 1_000_000), Fraction(-1575240, 1_000_000)),
        )
        result = validate_skyrmion_picard_step(
            Fraction(1001, 10_000),
            Fraction(1, 1_000_000),
            initial,
            tube,
        )
        self.assertLess(result.endpoint.derivative.upper, 0)
        narrow_tube = SkyrmionStateBox(initial.profile, initial.derivative)
        with self.assertRaises(ValueError):
            validate_skyrmion_picard_step(
                Fraction(1001, 10_000),
                Fraction(1, 1_000_000),
                initial,
                narrow_tube,
            )

    def test_origin_cubic_interval_is_algebraic_only(self):
        coefficient = skyrmion_origin_cubic_coefficient_interval(
            RationalInterval(Fraction(1579953, 1_000_000), Fraction(1579954, 1_000_000))
        )
        self.assertGreater(coefficient.lower, 0)
        self.assertLess(coefficient.width, Fraction(1, 1_000_000))

    def test_exact_zero_taylor_cell(self):
        zero = SkyrmionStateBox(
            RationalInterval.point(0),
            RationalInterval.point(0),
        )
        cell = SkyrmionTaylorCell(
            radius_start=Fraction(1),
            step=Fraction(1, 10),
            profile_polynomial=RationalPolynomial((Fraction(0),)),
            profile_radius=Fraction(0),
            derivative_radius=Fraction(0),
        )
        result = validate_skyrmion_taylor_cell(zero, cell)
        self.assertEqual(result.defect_box, RationalInterval.point(0))
        self.assertEqual(result.contraction_bound, 0)
        self.assertEqual(result.endpoint, zero)

    def test_real_conditional_taylor_track_chains_exact_endpoints(self):
        initial, first, second = self._conditional_taylor_data()
        track = validate_skyrmion_taylor_track(initial, (first, second))
        self.assertEqual(len(track.cells), 2)
        self.assertEqual(track.cells[1].initial, track.cells[0].endpoint)
        self.assertEqual(track.endpoint, track.cells[1].endpoint)
        for cell in track.cells:
            self.assertLessEqual(
                cell.profile_self_map_bound, cell.profile_radius
            )
            self.assertLessEqual(
                cell.derivative_self_map_bound, cell.derivative_radius
            )
            self.assertLess(cell.contraction_bound, 1)
            self.assertLessEqual(
                cell.endpoint.profile.width,
                2 * cell.profile_self_map_bound,
            )
            self.assertLessEqual(
                cell.endpoint.derivative.width,
                2 * cell.derivative_self_map_bound,
            )
        self.assertFalse(track.cells[0].defect_box.contains_zero())

    def test_taylor_cell_rejects_tampered_center_and_track_gap(self):
        initial, first, second = self._conditional_taylor_data()
        tampered = SkyrmionTaylorCell(
            radius_start=first.radius_start,
            step=first.step,
            profile_polynomial=RationalPolynomial(
                (
                    first.profile_polynomial.coefficients[0]
                    + Fraction(1, 100),
                    first.profile_polynomial.coefficients[1],
                )
            ),
            profile_radius=first.profile_radius,
            derivative_radius=first.derivative_radius,
        )
        with self.assertRaisesRegex(ValueError, "profile self-map"):
            validate_skyrmion_taylor_cell(initial, tampered)
        gap = SkyrmionTaylorCell(
            radius_start=second.radius_start + second.step,
            step=second.step,
            profile_polynomial=second.profile_polynomial,
            profile_radius=second.profile_radius,
            derivative_radius=second.derivative_radius,
        )
        with self.assertRaisesRegex(ValueError, "contiguous"):
            validate_skyrmion_taylor_track(initial, (first, gap))

    def test_certificate(self):
        certificate = conditional_picard_foundation_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["executable_checks"].values()))
        self.assertIn("not connected", certificate["claim_boundary"])

    def test_taylor_and_combined_foundation_certificates(self):
        taylor = conditional_taylor_foundation_certificate()
        self.assertEqual(taylor["status"], "pass")
        self.assertTrue(all(taylor["executable_checks"].values()))
        self.assertEqual(taylor["cell_count"], 2)
        combined = validated_skyrmion_profile_foundation_certificate()
        self.assertEqual(combined["status"], "pass")
        self.assertTrue(all(combined["executable_checks"].values()))

    def test_validation(self):
        with self.assertRaises(ValueError):
            curved_skyrmion_acceleration_box(
                RationalInterval(Fraction(0), Fraction(1, 10)),
                RationalInterval.point(1),
                RationalInterval.point(-1),
            )
        with self.assertRaises(ValueError):
            skyrmion_origin_cubic_coefficient_interval(
                RationalInterval(Fraction(-1), Fraction(1))
            )


if __name__ == "__main__":
    unittest.main()
