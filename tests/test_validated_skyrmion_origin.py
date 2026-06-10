import ast
import inspect
import unittest
from dataclasses import replace
from fractions import Fraction
from unittest.mock import patch

import qgtoy.validated_skyrmion_origin as origin_module
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_origin import (
    DEFAULT_SHOOTING_SLOPE_FAMILY,
    validate_skyrmion_origin_family,
    validate_skyrmion_origin_patch,
    validate_skyrmion_origin_quintic_branch_identification,
    validate_skyrmion_origin_quintic_patch,
    validate_skyrmion_origin_second_sensitivity,
    validate_skyrmion_origin_sensitivity,
    validated_skyrmion_origin_certificate,
)


class ValidatedSkyrmionOriginTest(unittest.TestCase):
    def test_default_quintic_endpoint_patch_closes(self):
        patch = validate_skyrmion_origin_quintic_patch(
            Fraction(1_579_953, 1_000_000)
        )
        self.assertLess(patch.contraction_bound, 1)
        self.assertLessEqual(
            patch.residual_bound
            + patch.contraction_bound * patch.remainder_radius,
            patch.remainder_radius,
        )
        self.assertLess(patch.quintic_coefficient, 0)
        self.assertLess(patch.derivative_at_cutoff.upper, 0)

    def test_quintic_cutoff_box_uses_x7_and_x6_errors(self):
        patch = validate_skyrmion_origin_quintic_patch(
            Fraction(1_579_953, 1_000_000)
        )
        x = patch.cutoff
        t = x**2
        derivative_center = (
            -patch.shooting_slope
            + 3 * patch.cubic_coefficient * t
            + 5 * patch.quintic_coefficient * t**2
        )
        derivative_error = patch.remainder_radius * x**6
        self.assertEqual(
            patch.derivative_at_cutoff,
            RationalInterval(
                derivative_center - derivative_error,
                derivative_center + derivative_error,
            ),
        )
        profile_center_u = (
            patch.shooting_slope
            - patch.cubic_coefficient * t
            - patch.quintic_coefficient * t**2
        )
        profile_error_u = patch.remainder_radius * x**6 / 7
        expected_profile = origin_module.pi_machin_interval(terms=64) - (
            RationalInterval(
                profile_center_u - profile_error_u,
                profile_center_u + profile_error_u,
            ).scale(x)
        )
        self.assertEqual(patch.profile_at_cutoff, expected_profile)

    def test_quintic_patch_strictly_sharpens_cubic_endpoint_box(self):
        slope = Fraction(1_579_953, 1_000_000)
        cubic = validate_skyrmion_origin_patch(slope)
        quintic = validate_skyrmion_origin_quintic_patch(slope)
        self.assertGreaterEqual(
            cubic.profile_at_cutoff.width / quintic.profile_at_cutoff.width,
            350,
        )
        self.assertGreaterEqual(
            cubic.derivative_at_cutoff.width
            / quintic.derivative_at_cutoff.width,
            256,
        )

    def test_quintic_patch_rejects_unclosed_radius(self):
        with self.assertRaises(ValueError):
            validate_skyrmion_origin_quintic_patch(
                Fraction(1_579_953, 1_000_000),
                remainder_radius=Fraction(1, 10),
            )

    def test_quintic_patch_is_identified_with_cubic_sensitivity_branch(self):
        slope = Fraction(1_579_953, 1_000_000)
        quintic = validate_skyrmion_origin_quintic_patch(slope)
        sensitivity = validate_skyrmion_origin_sensitivity()
        identification = validate_skyrmion_origin_quintic_branch_identification(
            quintic,
            sensitivity,
        )
        self.assertTrue(
            identification.identified_with_cubic_sensitivity_branch
        )
        self.assertLess(
            identification.normalized_momentum_offset_upper_bound,
            sensitivity.remainder_radius,
        )
        self.assertLess(
            identification.normalized_profile_offset_upper_bound,
            sensitivity.remainder_radius / 5,
        )

    def test_quintic_branch_identification_rejects_bad_provenance(self):
        slope = Fraction(1_579_953, 1_000_000)
        quintic = validate_skyrmion_origin_quintic_patch(slope)
        sensitivity = validate_skyrmion_origin_sensitivity()
        with self.assertRaisesRegex(ValueError, "operator parameters"):
            validate_skyrmion_origin_quintic_branch_identification(
                quintic,
                replace(sensitivity, curvature=Fraction(1, 200)),
            )
        with self.assertRaisesRegex(ValueError, "momentum ball"):
            validate_skyrmion_origin_quintic_branch_identification(
                quintic,
                replace(sensitivity, remainder_radius=Fraction(1, 10)),
            )

    def test_default_endpoint_patch_closes(self):
        patch = validate_skyrmion_origin_patch(
            Fraction(1_579_953, 1_000_000)
        )
        self.assertLess(patch.contraction_bound, 1)
        self.assertEqual(patch.cutoff, Fraction(1, 16))
        self.assertEqual(patch.remainder_radius, Fraction(13, 10))
        self.assertLessEqual(
            patch.residual_bound
            + patch.contraction_bound * patch.remainder_radius,
            patch.remainder_radius,
        )
        self.assertLess(patch.derivative_at_cutoff.upper, 0)

    def test_certificate_validates_both_shooting_endpoints(self):
        certificate = validated_skyrmion_origin_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["executable_checks"].values()))
        self.assertEqual(
            certificate["shooting_slopes"],
            ["1579953/1000000", "789977/500000"],
        )
        self.assertEqual(
            certificate["profile_sensitivity_at_cutoff"]["representation"],
            "outward_decimal_enclosure_18_places",
        )
        self.assertLess(
            float(certificate["profile_sensitivity_at_cutoff"]["upper"]),
            0.0,
        )
        self.assertLess(
            float(certificate["derivative_sensitivity_at_cutoff"]["upper"]),
            0.0,
        )
        self.assertEqual(
            certificate["profile_second_sensitivity_at_cutoff"]["representation"],
            "outward_decimal_enclosure_18_places",
        )
        self.assertLessEqual(
            float(certificate["profile_second_sensitivity_at_cutoff"]["lower"]),
            float(certificate["profile_second_sensitivity_at_cutoff"]["upper"]),
        )

    def test_uniform_family_patch_closes_on_the_full_interval(self):
        family = validate_skyrmion_origin_family()
        self.assertEqual(family.shooting_slopes, DEFAULT_SHOOTING_SLOPE_FAMILY)
        self.assertEqual(family.cutoff, Fraction(1, 16))
        self.assertLess(family.contraction_bound, 1)
        self.assertGreater(family.volterra_denominator_lower_bound, 0)
        self.assertLessEqual(
            family.residual_bound
            + family.contraction_bound * family.remainder_radius,
            family.remainder_radius,
        )
        self.assertLess(family.derivative_at_cutoff.upper, 0)

    def test_uniform_cutoff_box_contains_interior_point_proofs(self):
        family = validate_skyrmion_origin_family()
        lower = family.shooting_slopes.lower
        width = family.shooting_slopes.width
        for index in range(9):
            slope = lower + width * Fraction(index, 8)
            point = validate_skyrmion_origin_patch(slope)
            self.assertTrue(
                point.profile_at_cutoff.is_subset_of(family.profile_at_cutoff)
            )
            self.assertTrue(
                point.derivative_at_cutoff.is_subset_of(
                    family.derivative_at_cutoff
                )
            )
            self.assertTrue(family.cubic_coefficient.contains(point.cubic_coefficient))

    def test_uniform_cutoff_box_is_the_direct_parameter_formula(self):
        family = validate_skyrmion_origin_family()
        horizon = family.cutoff**2
        derivative_error = family.remainder_radius * horizon**2
        profile_error = derivative_error / 5
        expected_p = (
            family.shooting_slopes
            + family.cubic_coefficient.scale(-3 * horizon)
            + RationalInterval(-derivative_error, derivative_error)
        )
        expected_u = (
            family.shooting_slopes
            + family.cubic_coefficient.scale(-horizon)
            + RationalInterval(-profile_error, profile_error)
        )
        self.assertEqual(family.derivative_at_cutoff, -expected_p)
        expected_profile = origin_module.pi_machin_interval(
            terms=64
        ) - expected_u.scale(family.cutoff)
        self.assertEqual(family.profile_at_cutoff, expected_profile)

    def test_uniform_origin_sensitivity_closes(self):
        sensitivity = validate_skyrmion_origin_sensitivity()
        self.assertTrue(sensitivity.continuously_differentiable)
        self.assertLess(sensitivity.contraction_bound, 1)
        self.assertGreater(sensitivity.partial_map_sensitivity_bound, 0)
        self.assertEqual(
            sensitivity.fixed_point_sensitivity_bound,
            sensitivity.partial_map_sensitivity_bound
            / (1 - sensitivity.contraction_bound),
        )
        self.assertLess(sensitivity.phi_b.upper, 0)
        self.assertLess(sensitivity.gamma_b.upper, 0)

    def test_cutoff_sensitivities_are_direct_derivative_formulas(self):
        sensitivity = validate_skyrmion_origin_sensitivity()
        horizon = sensitivity.cutoff**2
        remainder_error = sensitivity.fixed_point_sensitivity_bound * horizon**2
        expected_p = (
            RationalInterval.point(1)
            + sensitivity.cubic_coefficient_derivative.scale(-3 * horizon)
            + RationalInterval(-remainder_error, remainder_error)
        )
        expected_u = (
            RationalInterval.point(1)
            + sensitivity.cubic_coefficient_derivative.scale(-horizon)
            + RationalInterval(-remainder_error / 5, remainder_error / 5)
        )
        self.assertEqual(sensitivity.gamma_b, -expected_p)
        self.assertEqual(
            sensitivity.phi_b,
            expected_u.scale(-sensitivity.cutoff),
        )

    def test_cubic_sensitivity_matches_exact_rational_derivative_at_a_point(self):
        slope = Fraction(1_579_953, 1_000_000)
        sensitivity = validate_skyrmion_origin_sensitivity(
            RationalInterval.point(slope)
        )
        curvature = Fraction(1, 400)
        constant = 1 - 4 * curvature
        quadratic = Fraction(4, 3) - 24 * curvature
        quartic = Fraction(8, 3)
        numerator = slope * (
            constant + quadratic * slope**2 + quartic * slope**4
        )
        numerator_derivative = (
            constant + 3 * quadratic * slope**2 + 5 * quartic * slope**4
        )
        denominator = 10 * (1 + 8 * slope**2)
        denominator_derivative = 160 * slope
        exact = (
            numerator_derivative * denominator
            - numerator * denominator_derivative
        ) / denominator**2
        self.assertEqual(
            sensitivity.cubic_coefficient_derivative,
            RationalInterval.point(exact),
        )

    def test_uniform_sensitivity_contains_degenerate_family_proofs(self):
        family = validate_skyrmion_origin_sensitivity()
        lower = family.shooting_slopes.lower
        width = family.shooting_slopes.width
        for index in range(5):
            slope = lower + width * Fraction(index, 4)
            point = validate_skyrmion_origin_sensitivity(
                RationalInterval.point(slope)
            )
            self.assertTrue(point.phi_b.is_subset_of(family.phi_b))
            self.assertTrue(point.gamma_b.is_subset_of(family.gamma_b))
            self.assertTrue(
                point.cubic_coefficient_derivative.is_subset_of(
                    family.cubic_coefficient_derivative
                )
            )

    def test_sensitivity_does_not_finite_difference_point_endpoint_boxes(self):
        with patch.object(
            origin_module,
            "validate_skyrmion_origin_patch",
            side_effect=AssertionError("point endpoint API must not be used"),
        ):
            sensitivity = validate_skyrmion_origin_sensitivity()
        self.assertTrue(sensitivity.continuously_differentiable)

    def test_uniform_origin_second_sensitivity_closes(self):
        sensitivity = validate_skyrmion_origin_second_sensitivity()
        self.assertTrue(sensitivity.twice_continuously_differentiable)
        self.assertLess(sensitivity.contraction_bound, 1)
        self.assertGreater(sensitivity.partial_second_sensitivity_bound, 0)
        self.assertEqual(
            sensitivity.fixed_point_second_sensitivity_bound,
            sensitivity.partial_second_sensitivity_bound
            / (1 - sensitivity.contraction_bound),
        )
        self.assertGreater(sensitivity.phi_bb.width, 0)
        self.assertGreater(sensitivity.gamma_bb.width, 0)

    def test_cutoff_second_sensitivities_are_direct_derivative_formulas(self):
        sensitivity = validate_skyrmion_origin_second_sensitivity()
        horizon = sensitivity.cutoff**2
        remainder_error = (
            sensitivity.fixed_point_second_sensitivity_bound * horizon**2
        )
        expected_p = (
            sensitivity.cubic_coefficient_second_derivative.scale(-3 * horizon)
            + RationalInterval(-remainder_error, remainder_error)
        )
        expected_u = (
            sensitivity.cubic_coefficient_second_derivative.scale(-horizon)
            + RationalInterval(-remainder_error / 5, remainder_error / 5)
        )
        self.assertEqual(sensitivity.gamma_bb, -expected_p)
        self.assertEqual(
            sensitivity.phi_bb,
            expected_u.scale(-sensitivity.cutoff),
        )

    def test_cubic_second_sensitivity_matches_exact_derivative_at_a_point(self):
        slope = Fraction(1_579_953, 1_000_000)
        sensitivity = validate_skyrmion_origin_second_sensitivity(
            RationalInterval.point(slope)
        )
        curvature = Fraction(1, 400)
        constant = 1 - 4 * curvature
        quadratic = Fraction(4, 3) - 24 * curvature
        quartic = Fraction(8, 3)
        numerator = slope * (
            constant + quadratic * slope**2 + quartic * slope**4
        )
        numerator_derivative = (
            constant + 3 * quadratic * slope**2 + 5 * quartic * slope**4
        )
        numerator_second_derivative = (
            6 * quadratic * slope + 20 * quartic * slope**3
        )
        denominator = 10 * (1 + 8 * slope**2)
        denominator_derivative = 160 * slope
        denominator_second_derivative = 160
        exact = (
            numerator_second_derivative / denominator
            - numerator * denominator_second_derivative / denominator**2
            - 2
            * numerator_derivative
            * denominator_derivative
            / denominator**2
            + 2 * numerator * denominator_derivative**2 / denominator**3
        )
        self.assertEqual(
            sensitivity.cubic_coefficient_second_derivative,
            RationalInterval.point(exact),
        )

    def test_uniform_second_sensitivity_contains_degenerate_family_proofs(self):
        family = validate_skyrmion_origin_second_sensitivity()
        lower = family.shooting_slopes.lower
        width = family.shooting_slopes.width
        for index in range(3):
            slope = lower + width * Fraction(index, 2)
            point = validate_skyrmion_origin_second_sensitivity(
                RationalInterval.point(slope)
            )
            self.assertTrue(point.phi_bb.is_subset_of(family.phi_bb))
            self.assertTrue(point.gamma_bb.is_subset_of(family.gamma_bb))
            self.assertTrue(
                point.cubic_coefficient_second_derivative.is_subset_of(
                    family.cubic_coefficient_second_derivative
                )
            )

    def test_second_sensitivity_does_not_finite_difference_point_boxes(self):
        with patch.object(
            origin_module,
            "validate_skyrmion_origin_patch",
            side_effect=AssertionError("point endpoint API must not be used"),
        ):
            sensitivity = validate_skyrmion_origin_second_sensitivity()
        self.assertTrue(sensitivity.twice_continuously_differentiable)

    def test_degenerate_family_agrees_with_point_proof(self):
        slope = Fraction(1_579_953, 1_000_000)
        point = validate_skyrmion_origin_patch(slope)
        family = validate_skyrmion_origin_family(RationalInterval.point(slope))
        self.assertEqual(family.residual_bound, point.residual_bound)
        self.assertEqual(family.contraction_bound, point.contraction_bound)
        self.assertEqual(family.profile_at_cutoff, point.profile_at_cutoff)
        self.assertEqual(family.derivative_at_cutoff, point.derivative_at_cutoff)
        self.assertEqual(
            family.cubic_coefficient,
            RationalInterval.point(point.cubic_coefficient),
        )

    def test_certificate_is_not_built_from_point_endpoint_hulls(self):
        with patch.object(
            origin_module,
            "validate_skyrmion_origin_patch",
            side_effect=AssertionError("point endpoint API must not be used"),
        ):
            certificate = validated_skyrmion_origin_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertIn("not endpoint hulls", certificate["cutoff_box_method"])
        self.assertTrue(
            certificate["executable_checks"][
                "fixed_point_depends_continuously_on_slope"
            ]
        )

    def test_exact_cubic_remainder_contract(self):
        patch = validate_skyrmion_origin_patch(
            Fraction(1_579_954, 1_000_000)
        )
        x = patch.cutoff
        t = x**2
        derivative_center = (
            -patch.shooting_slope + 3 * patch.cubic_coefficient * t
        )
        error = patch.remainder_radius * t**2
        self.assertEqual(
            patch.derivative_at_cutoff.lower,
            derivative_center - error,
        )
        self.assertEqual(
            patch.derivative_at_cutoff.upper,
            derivative_center + error,
        )

    def test_rejects_unclosed_radius(self):
        with self.assertRaises(ValueError):
            validate_skyrmion_origin_patch(
                Fraction(1_579_953, 1_000_000),
                remainder_radius=Fraction(1, 4),
            )

    def test_uniform_family_rejects_unclosed_radius(self):
        with self.assertRaises(ValueError):
            validate_skyrmion_origin_family(remainder_radius=Fraction(1, 4))

    def test_endpoint_success_does_not_substitute_for_a_uniform_proof(self):
        validate_skyrmion_origin_patch(Fraction(1))
        validate_skyrmion_origin_patch(Fraction(3, 2))
        with self.assertRaisesRegex(ValueError, "uniform weighted Volterra"):
            validate_skyrmion_origin_family(
                RationalInterval(Fraction(1), Fraction(3, 2))
            )

    def test_uniform_family_rejects_nonpositive_slopes(self):
        with self.assertRaises(ValueError):
            validate_skyrmion_origin_family(
                RationalInterval(Fraction(-1, 10), Fraction(1, 10))
            )

    def test_uniform_family_requires_an_exact_rational_interval(self):
        with self.assertRaises(TypeError):
            validate_skyrmion_origin_family(  # type: ignore[arg-type]
                (Fraction(1), Fraction(2))
            )

    def test_trusted_module_has_no_floating_transcendentals(self):
        tree = ast.parse(inspect.getsource(origin_module))
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }
        self.assertTrue(imported_modules.isdisjoint({"cmath", "numpy", "mpmath"}))
        math_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "math"
            for alias in node.names
        }
        self.assertEqual(math_names, {"factorial"})


if __name__ == "__main__":
    unittest.main()
