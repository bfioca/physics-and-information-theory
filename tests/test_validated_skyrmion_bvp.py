import math
import unittest
from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace
from unittest.mock import patch

from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import (
    SkyrmionJetBox,
    SkyrmionPolynomialCell,
    _absolute_interval_upper,
    _affine_restrict_polynomial,
    _combined_jacobi_numerator_model,
    _combined_nonlinear_numerator_model,
    _interval_polynomial_bernstein_range,
    _normalized_polynomial_l1_upper_bound,
    _outward_round_interval,
    _skyrmion_local_newton_norm_bounds,
    _skyrmion_weighted_trace_upper_bound,
    _upward_round_fraction,
    conditional_skyrmion_barta_foundation_certificate,
    reweight_skyrmion_augmented_operator_mismatch,
    skyrmion_barta_quotient_box,
    skyrmion_jacobi_coefficient_box,
    sharpen_skyrmion_schur_with_green_resolvent,
    validate_skyrmion_barta_cells,
    validate_skyrmion_augmented_operator_mismatch,
    validate_skyrmion_augmented_newton_tube,
    validate_skyrmion_derivative_trace_representer,
    validate_skyrmion_endpoint_corrected_residual,
    validate_skyrmion_green_resolvent_bounds,
    validate_skyrmion_newton_physical_observables,
    validate_skyrmion_polynomial_barta_spline,
    validate_skyrmion_polynomial_schur_bound,
    validate_skyrmion_trace_sharpened_schur_bound,
)
from qgtoy.validated_skyrmion_origin import (
    ValidatedSkyrmionOriginFamily,
    ValidatedSkyrmionOriginQuinticBranchIdentification,
    ValidatedSkyrmionOriginQuinticPatch,
    ValidatedSkyrmionOriginSecondSensitivity,
    ValidatedSkyrmionOriginSensitivity,
)


def _evaluate_interval_polynomial(polynomial, value):
    result = RationalInterval.point(0)
    for coefficient in reversed(polynomial):
        result = result * value + coefficient
    return result


def _interval(lower: int, upper: int, denominator: int = 10_000_000):
    return RationalInterval(
        Fraction(lower, denominator),
        Fraction(upper, denominator),
    )


def _quintic_hermite_polynomial(
    value_start,
    derivative_start,
    second_start,
    value_end,
    derivative_end,
    second_end,
    width=Fraction(1),
):
    a0 = value_start
    a1 = width * derivative_start
    a2 = width**2 * second_start / 2
    value_gap = value_end - a0 - a1 - a2
    derivative_gap = width * derivative_end - a1 - 2 * a2
    second_gap = width**2 * second_end - 2 * a2
    return RationalPolynomial(
        (
            a0,
            a1,
            a2,
            10 * value_gap - 4 * derivative_gap + second_gap / 2,
            -15 * value_gap + 7 * derivative_gap - second_gap,
            6 * value_gap - 3 * derivative_gap + second_gap / 2,
        )
    )


def _vacuum_green_parametrix_cells():
    """Quintic proposals for exact homogeneous functions on ``[1,2]``."""
    radius = RationalInterval(Fraction(1), Fraction(2))
    profile = SkyrmionPolynomialCell(
        radius, RationalPolynomial((Fraction(0),))
    )

    # For F=0, mu=k=0, A=-(x^2 y')'+2y.  The exact functions used to
    # generate the endpoint jets are (x-x^-2)/3 and (8x^-2-x)/7.
    def left_jet(x):
        return (
            (x - Fraction(1, x**2)) / 3,
            (1 + Fraction(2, x**3)) / 3,
            -Fraction(2, x**4),
        )

    def right_jet(x):
        return (
            (Fraction(8, x**2) - x) / 7,
            (-Fraction(16, x**3) - 1) / 7,
            Fraction(48, 7 * x**4),
        )

    left = SkyrmionPolynomialCell(
        radius,
        _quintic_hermite_polynomial(
            *left_jet(Fraction(1)), *left_jet(Fraction(2))
        ),
    )
    right = SkyrmionPolynomialCell(
        radius,
        _quintic_hermite_polynomial(
            *right_jet(Fraction(1)), *right_jet(Fraction(2))
        ),
    )
    return profile, left, right


def _floating_profile_cells():
    """Conditional boxes around the default branch's delicate Barta region."""
    return (
        SkyrmionJetBox(
            _interval(8_700_000, 8_720_000),
            _interval(18_495_680, 18_520_800),
            _interval(-13_195_650, -13_187_290),
            _interval(4_363_490, 4_364_360),
        ),
        SkyrmionJetBox(
            _interval(8_720_000, 8_740_000),
            _interval(18_469_310, 18_494_420),
            _interval(-13_186_930, -13_178_560),
            _interval(4_362_620, 4_363_530),
        ),
        SkyrmionJetBox(
            _interval(8_740_000, 8_760_000),
            _interval(18_442_950, 18_468_060),
            _interval(-13_178_200, -13_169_840),
            _interval(4_361_720, 4_362_660),
        ),
        SkyrmionJetBox(
            _interval(8_760_000, 8_780_000),
            _interval(18_416_620, 18_441_710),
            _interval(-13_169_480, -13_161_110),
            _interval(4_360_790, 4_361_760),
        ),
        SkyrmionJetBox(
            _interval(8_780_000, 8_800_000),
            _interval(18_390_300, 18_415_380),
            _interval(-13_160_760, -13_152_390),
            _interval(4_359_820, 4_360_820),
        ),
    )


class ValidatedSkyrmionBVPTest(unittest.TestCase):
    def test_fixed_grid_rounding_is_outward(self):
        value = RationalInterval(Fraction(-7, 13), Fraction(11, 17))
        rounded = _outward_round_interval(value, 100)
        self.assertLessEqual(rounded.lower, value.lower)
        self.assertGreaterEqual(rounded.upper, value.upper)
        self.assertEqual(rounded.lower.denominator, 50)
        self.assertEqual(
            _upward_round_fraction(Fraction(-7, 13), 100),
            Fraction(-53, 100),
        )

    def test_weighted_trace_uses_cell_l1_mass_and_uniform_error(self):
        trace = SimpleNamespace(
            l1_cells=(
                SimpleNamespace(
                    source_cell_index=0,
                    radius=RationalInterval(Fraction(1), Fraction(2)),
                    l1_upper_bound=Fraction(2),
                ),
                SimpleNamespace(
                    source_cell_index=1,
                    radius=RationalInterval(Fraction(2), Fraction(4)),
                    l1_upper_bound=Fraction(3),
                ),
            ),
            inverse_c0_bound=Fraction(5),
            residual_supremum_upper_bound=Fraction(1, 10),
            principal_left_lower_bound=Fraction(2),
        )
        bounds = ((0, Fraction(1)), (0, Fraction(4)), (1, Fraction(2)))
        self.assertEqual(
            _skyrmion_weighted_trace_upper_bound(trace, bounds),
            Fraction(9),
        )
        self.assertEqual(
            _skyrmion_weighted_trace_upper_bound(
                trace,
                bounds,
                inverse_c0_upper_bound=Fraction(1),
            ),
            Fraction(37, 5),
        )
        with self.assertRaisesRegex(ValueError, "cover every source cell"):
            _skyrmion_weighted_trace_upper_bound(
                trace,
                ((0, Fraction(1)),),
            )

    def test_green_parametrix_certifies_cellwise_resolvent_bounds(self):
        profile, left, right = _vacuum_green_parametrix_cells()
        validation = validate_skyrmion_green_resolvent_bounds(
            (profile,),
            (left,),
            (right,),
            Fraction(1, 100),
            Fraction(1),
            subdivisions_per_source_cell=8,
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=3,
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            trigonometric_terms=12,
            residual_taylor_terms=4,
        )
        self.assertEqual(
            validation.initial_wronskian_enclosure,
            RationalInterval.point(1),
        )
        self.assertLess(validation.operator_defect_upper_bound, 1)
        neumann_factor = 1 / (1 - validation.operator_defect_upper_bound)
        self.assertEqual(
            validation.c0_upper_bound,
            validation.approximate_c0_upper_bound * neumann_factor,
        )
        self.assertEqual(
            validation.c1_upper_bound,
            validation.approximate_c1_upper_bound * neumann_factor,
        )
        self.assertEqual(
            validation.c2_upper_bound,
            validation.approximate_c2_upper_bound * neumann_factor,
        )
        for cell in validation.cells:
            self.assertGreaterEqual(
                cell.approximate_c2_row_upper_bound,
                (1 + cell.relative_wronskian_error_upper_bound)
                / cell.principal_lower_bound,
            )
        self.assertLess(validation.c1_upper_bound, 1)
        self.assertLess(validation.c2_upper_bound, 4)
        self.assertIn("no nonlinear BVP", validation.conclusion_scope)

    def test_green_parametrix_is_invariant_under_fundamental_scaling(self):
        profile, left, right = _vacuum_green_parametrix_cells()
        common = dict(
            subdivisions_per_source_cell=8,
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=3,
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            trigonometric_terms=12,
            residual_taylor_terms=4,
        )
        original = validate_skyrmion_green_resolvent_bounds(
            (profile,), (left,), (right,), Fraction(1, 100), Fraction(1), **common
        )
        scaled_left = replace(
            left,
            profile_polynomial=RationalPolynomial(
                tuple(2 * value for value in left.profile_polynomial.coefficients)
            ),
        )
        scaled = validate_skyrmion_green_resolvent_bounds(
            (profile,),
            (scaled_left,),
            (right,),
            Fraction(1, 100),
            Fraction(2),
            **common,
        )
        self.assertEqual(
            scaled.operator_defect_upper_bound,
            original.operator_defect_upper_bound,
        )
        self.assertEqual(scaled.c0_upper_bound, original.c0_upper_bound)
        self.assertEqual(scaled.c1_upper_bound, original.c1_upper_bound)
        self.assertEqual(scaled.c2_upper_bound, original.c2_upper_bound)

    def test_newton_local_norms_reuse_green_rows_and_auxiliary_correction(self):
        profile, left, right = _vacuum_green_parametrix_cells()
        green = validate_skyrmion_green_resolvent_bounds(
            (profile,),
            (left,),
            (right,),
            Fraction(1, 100),
            Fraction(1),
            subdivisions_per_source_cell=8,
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=3,
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            trigonometric_terms=12,
            residual_taylor_terms=4,
        )
        schur = validate_skyrmion_trace_sharpened_schur_bound(
            (profile,),
            (right,),
            (right,),
            RationalInterval.point(1),
            RationalInterval.point(-1000),
            Fraction(1, 100),
            Fraction(2000),
            Fraction(1),
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=3,
            trace_residual_initial_subdivisions=2,
            trace_residual_maximum_refinement_depth=2,
            schur_residual_initial_subdivisions=2,
            schur_residual_maximum_refinement_depth=2,
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            trigonometric_terms=12,
            residual_taylor_terms=4,
        )
        sharpened = sharpen_skyrmion_schur_with_green_resolvent(schur, green)
        base_row = green.cells[0]
        local_green = replace(
            green,
            profile_cells=(profile, profile),
            cells=(
                replace(
                    base_row,
                    source_cell_index=0,
                    approximate_c0_row_upper_bound=Fraction(1),
                    approximate_c1_row_upper_bound=Fraction(2),
                    approximate_c2_row_upper_bound=Fraction(3),
                ),
                replace(
                    base_row,
                    source_cell_index=1,
                    approximate_c0_row_upper_bound=Fraction(4),
                    approximate_c1_row_upper_bound=Fraction(5),
                    approximate_c2_row_upper_bound=Fraction(6),
                ),
            ),
            source_cell_count=2,
        )
        local_schur = replace(
            sharpened,
            profile_cells=(profile, profile),
            auxiliary_cells=(right, right),
            graph_resolvent_bounds=local_green,
        )
        row0 = _skyrmion_local_newton_norm_bounds(local_schur, 0)
        row1 = _skyrmion_local_newton_norm_bounds(local_schur, 1)
        neumann = Fraction(1) / (1 - green.operator_defect_upper_bound)

        self.assertEqual(row0[:3], (neumann, 2 * neumann, 3 * neumann))
        self.assertEqual(row1[:3], (4 * neumann, 5 * neumann, 6 * neumann))
        correction_difference = (
            3 * neumann * sharpened.residual_supremum_upper_bound
        )
        self.assertEqual(row1[3] - row0[3], correction_difference)
        self.assertEqual(row1[4] - row0[4], correction_difference)
        self.assertEqual(row1[5] - row0[5], correction_difference)
        with self.assertRaisesRegex(ValueError, "does not cover"):
            _skyrmion_local_newton_norm_bounds(local_schur, 2)

    def test_green_parametrix_reuses_same_operator_barta_certificate(self):
        profile, left, right = _vacuum_green_parametrix_cells()
        barta = validate_skyrmion_polynomial_barta_spline(
            (profile,),
            Fraction(1, 100),
            initial_subdivisions=2,
            maximum_refinement_depth=3,
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            trigonometric_terms=12,
        )
        common = dict(
            subdivisions_per_source_cell=8,
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=3,
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            trigonometric_terms=12,
            residual_taylor_terms=4,
        )
        repeated = validate_skyrmion_green_resolvent_bounds(
            (profile,), (left,), (right,), Fraction(1, 100), Fraction(1), **common
        )
        reused = validate_skyrmion_green_resolvent_bounds(
            (profile,),
            (left,),
            (right,),
            Fraction(1, 100),
            Fraction(1),
            barta_validation=barta,
            **common,
        )
        self.assertEqual(reused, repeated)
        self.assertIs(reused.barta_validation, barta)

        with self.assertRaisesRegex(ValueError, "same declared lower bound"):
            validate_skyrmion_green_resolvent_bounds(
                (profile,),
                (left,),
                (right,),
                Fraction(1, 200),
                Fraction(1),
                barta_validation=barta,
                **common,
            )
        with self.assertRaisesRegex(ValueError, "same exact profile and operator"):
            validate_skyrmion_green_resolvent_bounds(
                (profile,),
                (left,),
                (right,),
                Fraction(1, 100),
                Fraction(1),
                pion_mass_squared=Fraction(1),
                curvature=Fraction(0),
                trigonometric_terms=12,
                residual_taylor_terms=4,
                barta_validation=barta,
            )

    def test_green_parametrix_rejects_endpoint_and_defect_failures(self):
        profile, left, right = _vacuum_green_parametrix_cells()
        bad_left = replace(
            left,
            profile_polynomial=RationalPolynomial(
                (Fraction(1),) + left.profile_polynomial.coefficients[1:]
            ),
        )
        with self.assertRaisesRegex(ValueError, "left Green fundamental"):
            validate_skyrmion_green_resolvent_bounds(
                (profile,),
                (bad_left,),
                (right,),
                Fraction(1, 100),
                Fraction(1),
                pion_mass_squared=Fraction(0),
                curvature=Fraction(0),
            )
        mismatched_right = replace(
            right,
            radius=RationalInterval(Fraction(1), Fraction(3)),
        )
        with self.assertRaisesRegex(ValueError, "meshes must coincide"):
            validate_skyrmion_green_resolvent_bounds(
                (profile,),
                (left,),
                (mismatched_right,),
                Fraction(1, 100),
                Fraction(1),
                pion_mass_squared=Fraction(0),
                curvature=Fraction(0),
            )
        with self.assertRaisesRegex(ValueError, "operator defect"):
            validate_skyrmion_green_resolvent_bounds(
                (profile,),
                (left,),
                (right,),
                Fraction(1, 100),
                Fraction(1, 10),
                subdivisions_per_source_cell=8,
                barta_initial_subdivisions=2,
                barta_maximum_refinement_depth=3,
                pion_mass_squared=Fraction(0),
                curvature=Fraction(0),
                trigonometric_terms=12,
                residual_taylor_terms=4,
            )

    def test_representer_l1_bound_uses_exact_sign_and_supremum_branches(self):
        fixed_range, fixed_bound, fixed_sign = (
            _normalized_polynomial_l1_upper_bound(
                RationalPolynomial((Fraction(1), Fraction(-1)))
            )
        )
        self.assertEqual(
            fixed_range, RationalInterval(Fraction(0), Fraction(1))
        )
        self.assertEqual(fixed_bound, Fraction(1, 2))
        self.assertTrue(fixed_sign)

        changing_range, changing_bound, changing_sign = (
            _normalized_polynomial_l1_upper_bound(
                RationalPolynomial(
                    (Fraction(1), Fraction(-3), Fraction(2))
                )
            )
        )
        self.assertEqual(
            changing_range, RationalInterval(Fraction(-1, 2), Fraction(1))
        )
        self.assertEqual(changing_bound, Fraction(1))
        self.assertFalse(changing_sign)

    def test_combined_residual_has_exact_vacuum_polynomial_identity(self):
        physical_half_width = Fraction(1, 8)
        radius = RationalPolynomial(
            (Fraction(5, 4), physical_half_width)
        )
        profile = RationalPolynomial((Fraction(0),))
        auxiliary = RationalPolynomial(
            (
                Fraction(7, 11),
                physical_half_width * Fraction(-3, 8),
                physical_half_width**2 * Fraction(13, 17) / 2,
            )
        )
        curvature = Fraction(1, 17)
        mass_squared = Fraction(7, 5)
        model, tail = _combined_jacobi_numerator_model(
            profile,
            auxiliary,
            radius,
            pion_mass_squared=mass_squared,
            curvature=curvature,
            trigonometric_terms=16,
            residual_taylor_terms=8,
            physical_half_width=physical_half_width,
        )
        self.assertEqual(tail, 0)
        self.assertTrue(all(value.width == 0 for value in model))

        for index in range(-16, 17):
            z = Fraction(index, 16)
            x = Fraction(5, 4) + physical_half_width * z
            h = auxiliary.evaluate(z).lower
            h_prime = Fraction(-3, 8) + physical_half_width * Fraction(
                13, 17
            ) * z
            h_second = Fraction(13, 17)
            lapse = 1 - curvature * x**2
            lapse_derivative = -2 * curvature * x
            direct_residual = (
                -lapse * x**2 * h_second
                - (lapse_derivative * x**2 + 2 * lapse * x) * h_prime
                + (2 + mass_squared * x**2) * h
            )
            expected_numerator = x**2 * direct_residual
            self.assertEqual(
                _evaluate_interval_polynomial(model, z),
                RationalInterval.point(expected_numerator),
            )
        self.assertEqual(
            _evaluate_interval_polynomial(model, 0),
            RationalInterval.point(Fraction(47_708_525, 13_021_184)),
        )

    def test_combined_residual_contains_dense_unexpanded_operator_samples(self):
        radius_global = RationalPolynomial((Fraction(1, 2), Fraction(3)))
        profile_global = RationalPolynomial(
            (
                Fraction(14, 5),
                Fraction(-16, 5),
                Fraction(3, 5),
                Fraction(-1, 10),
            )
        )
        auxiliary_global = RationalPolynomial(
            (
                Fraction(-2, 7),
                Fraction(5, 3),
                Fraction(-7, 4),
                Fraction(11, 10),
                Fraction(-1, 5),
            )
        )
        curvature = Fraction(1, 400)
        mass_squared = Fraction(7, 5)

        for subcell in range(4):
            center = Fraction(2 * subcell + 1, 8)
            half_width = Fraction(1, 8)
            physical_half_width = Fraction(3, 8)
            radius = _affine_restrict_polynomial(
                radius_global, center, half_width
            )
            profile = _affine_restrict_polynomial(
                profile_global, center, half_width
            )
            auxiliary = _affine_restrict_polynomial(
                auxiliary_global, center, half_width
            )
            model, tail = _combined_jacobi_numerator_model(
                profile,
                auxiliary,
                radius,
                pion_mass_squared=mass_squared,
                curvature=curvature,
                trigonometric_terms=18,
                residual_taylor_terms=8,
                physical_half_width=physical_half_width,
            )
            enclosure = _interval_polynomial_bernstein_range(model) + (
                RationalInterval(-tail, tail)
            )

            for sample in range(17):
                z = -1.0 + sample / 8.0
                t = float(center) + float(half_width) * z
                x = 0.5 + 3.0 * t
                profile_value = 2.8 - 3.2 * t + 0.6 * t**2 - 0.1 * t**3
                profile_derivative = (
                    -3.2 + 1.2 * t - 0.3 * t**2
                ) / 3.0
                profile_second_derivative = (1.2 - 0.6 * t) / 9.0
                auxiliary_value = (
                    -2.0 / 7.0
                    + 5.0 / 3.0 * t
                    - 7.0 / 4.0 * t**2
                    + 1.1 * t**3
                    - 0.2 * t**4
                )
                auxiliary_derivative = (
                    5.0 / 3.0
                    - 7.0 / 2.0 * t
                    + 3.3 * t**2
                    - 0.8 * t**3
                ) / 3.0
                auxiliary_second_derivative = (
                    -7.0 / 2.0 + 6.6 * t - 2.4 * t**2
                ) / 9.0
                lapse = 1.0 - float(curvature) * x**2
                lapse_derivative = -2.0 * float(curvature) * x
                sine = math.sin(profile_value)
                sine_twice = math.sin(2.0 * profile_value)
                cosine_twice = math.cos(2.0 * profile_value)
                principal = lapse * (x**2 + 8.0 * sine**2)
                principal_derivative = (
                    lapse_derivative * (x**2 + 8.0 * sine**2)
                    + lapse * (2.0 * x + 8.0 * sine_twice * profile_derivative)
                )
                potential = (
                    4.0 * sine_twice**2 / x**2
                    + 2.0 * (1.0 + 4.0 * sine**2 / x**2) * cosine_twice
                    - 8.0 * lapse * cosine_twice * profile_derivative**2
                    + float(mass_squared) * x**2 * math.cos(profile_value)
                    - 8.0
                    * lapse_derivative
                    * sine_twice
                    * profile_derivative
                    - 8.0
                    * lapse
                    * sine_twice
                    * profile_second_derivative
                )
                numerator = x**2 * (
                    -principal * auxiliary_second_derivative
                    - principal_derivative * auxiliary_derivative
                    + potential * auxiliary_value
                )
                self.assertLessEqual(float(enclosure.lower) - 1.0e-10, numerator)
                self.assertGreaterEqual(float(enclosure.upper) + 1.0e-10, numerator)

    def test_combined_nonlinear_residual_is_exact_at_vacuum(self):
        physical_half_width = Fraction(1, 8)
        radius = RationalPolynomial((Fraction(5, 4), physical_half_width))
        profile = RationalPolynomial((Fraction(0),))
        model, tail = _combined_nonlinear_numerator_model(
            profile,
            radius,
            pion_mass_squared=Fraction(7, 5),
            curvature=Fraction(1, 17),
            trigonometric_terms=16,
            residual_taylor_terms=8,
            physical_half_width=physical_half_width,
        )
        self.assertEqual(tail, 0)
        self.assertTrue(
            all(coefficient == RationalInterval.point(0) for coefficient in model)
        )

    def test_combined_nonlinear_residual_contains_dense_direct_samples(self):
        radius_global = RationalPolynomial((Fraction(1, 2), Fraction(3)))
        profile_global = RationalPolynomial(
            (
                Fraction(14, 5),
                Fraction(-16, 5),
                Fraction(3, 5),
                Fraction(-1, 10),
            )
        )
        curvature = Fraction(1, 400)
        mass_squared = Fraction(7, 5)

        for subcell in range(4):
            center = Fraction(2 * subcell + 1, 8)
            half_width = Fraction(1, 8)
            physical_half_width = Fraction(3, 8)
            radius = _affine_restrict_polynomial(
                radius_global, center, half_width
            )
            profile = _affine_restrict_polynomial(
                profile_global, center, half_width
            )
            model, tail = _combined_nonlinear_numerator_model(
                profile,
                radius,
                pion_mass_squared=mass_squared,
                curvature=curvature,
                trigonometric_terms=18,
                residual_taylor_terms=8,
                physical_half_width=physical_half_width,
            )
            enclosure = _interval_polynomial_bernstein_range(model) + (
                RationalInterval(-tail, tail)
            )

            for sample in range(17):
                z = -1.0 + sample / 8.0
                t = float(center) + float(half_width) * z
                x = 0.5 + 3.0 * t
                profile_value = 2.8 - 3.2 * t + 0.6 * t**2 - 0.1 * t**3
                profile_derivative = (
                    -3.2 + 1.2 * t - 0.3 * t**2
                ) / 3.0
                profile_second_derivative = (1.2 - 0.6 * t) / 9.0
                lapse = 1.0 - float(curvature) * x**2
                lapse_derivative = -2.0 * float(curvature) * x
                sine = math.sin(profile_value)
                sine_twice = math.sin(2.0 * profile_value)
                principal = lapse * (x**2 + 8.0 * sine**2)
                principal_derivative = (
                    lapse_derivative * (x**2 + 8.0 * sine**2)
                    + lapse * (2.0 * x + 8.0 * sine_twice * profile_derivative)
                )
                source = (
                    1.0
                    + 4.0 * sine**2 / x**2
                    + 4.0 * lapse * profile_derivative**2
                ) * sine_twice + float(mass_squared) * x**2 * sine
                numerator = x**2 * (
                    principal * profile_second_derivative
                    + principal_derivative * profile_derivative
                    - source
                )
                self.assertLessEqual(float(enclosure.lower) - 1.0e-10, numerator)
                self.assertGreaterEqual(float(enclosure.upper) + 1.0e-10, numerator)

    def test_endpoint_corrected_residual_is_exact_for_vacuum(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        validation = validate_skyrmion_endpoint_corrected_residual(
            (profile,),
            RationalInterval.point(0),
            RationalInterval.point(0),
            curvature=0,
            trigonometric_terms=16,
        )
        self.assertEqual(validation.left_value_correction, RationalInterval.point(0))
        self.assertEqual(validation.right_value_correction, 0)
        self.assertEqual(validation.boundary_slope_residual, RationalInterval.point(0))
        self.assertEqual(validation.residual_supremum_upper_bound, 0)
        self.assertEqual(validation.cells[0].residual, RationalInterval.point(0))
        self.assertIn("no nonlinear BVP", validation.conclusion_scope)

    def test_endpoint_corrected_residual_contains_origin_value_family(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        phi = RationalInterval(Fraction(0), Fraction(1, 100))
        validation = validate_skyrmion_endpoint_corrected_residual(
            (profile,),
            phi,
            RationalInterval.point(0),
            curvature=0,
            trigonometric_terms=18,
            residual_taylor_terms=8,
        )
        self.assertEqual(validation.left_value_correction, phi)
        self.assertEqual(
            validation.boundary_slope_residual,
            RationalInterval(Fraction(-1, 100), Fraction(0)),
        )
        residual = validation.cells[0].residual
        for delta in (0.0, 0.0025, 0.005, 0.0075, 0.01):
            for index in range(17):
                x = 1.0 + index / 16.0
                value = delta * (2.0 - x)
                derivative = -delta
                sine = math.sin(value)
                sine_twice = math.sin(2.0 * value)
                principal = x**2 + 8.0 * sine**2
                principal_derivative = (
                    2.0 * x + 8.0 * sine_twice * derivative
                )
                source = (
                    1.0
                    + 4.0 * sine**2 / x**2
                    + 4.0 * derivative**2
                ) * sine_twice + x**2 * sine
                direct = principal_derivative * derivative - source
                self.assertLessEqual(float(residual.lower) - 1.0e-12, direct)
                self.assertGreaterEqual(float(residual.upper) + 1.0e-12, direct)

    def test_augmented_operator_mismatch_tracks_endpoint_correction(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        representer = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1), Fraction(-1))),
        )
        schur = validate_skyrmion_trace_sharpened_schur_bound(
            (profile,),
            (representer,),
            (representer,),
            RationalInterval.point(1),
            RationalInterval.point(-1000),
            Fraction(1),
            Fraction(20),
            Fraction(1),
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=2,
            trace_residual_initial_subdivisions=2,
            trace_residual_maximum_refinement_depth=2,
            schur_residual_initial_subdivisions=2,
            schur_residual_maximum_refinement_depth=2,
            curvature=0,
            trigonometric_terms=16,
        )
        unchanged = validate_skyrmion_endpoint_corrected_residual(
            (profile,),
            RationalInterval.point(0),
            RationalInterval.point(0),
            phi_sensitivity_at_cutoff=RationalInterval.point(1),
            gamma_sensitivity_at_cutoff=RationalInterval.point(-1000),
            curvature=0,
            trigonometric_terms=16,
        )
        zero_mismatch = validate_skyrmion_augmented_operator_mismatch(
            schur,
            unchanged,
        )
        self.assertEqual(zero_mismatch.interior_operator_mismatch_upper_bound, 0)
        self.assertEqual(zero_mismatch.z0_upper_bound, 0)

        corrected = validate_skyrmion_endpoint_corrected_residual(
            (profile,),
            RationalInterval(Fraction(0), Fraction(1, 100)),
            RationalInterval.point(0),
            phi_sensitivity_at_cutoff=RationalInterval.point(1),
            gamma_sensitivity_at_cutoff=RationalInterval.point(-1000),
            curvature=0,
            trigonometric_terms=16,
        )
        mismatch = validate_skyrmion_augmented_operator_mismatch(
            schur,
            corrected,
        )
        with self.assertRaisesRegex(ValueError, "endpoint provenance"):
            reweight_skyrmion_augmented_operator_mismatch(
                schur,
                corrected,
                zero_mismatch,
                omega=Fraction(1, 2),
            )
        self.assertGreater(mismatch.interior_operator_mismatch_upper_bound, 0)
        self.assertEqual(
            mismatch.z0_upper_bound,
            mismatch.augmented_inverse_upper_bound
            * mismatch.interior_operator_mismatch_upper_bound,
        )
        expected_defect = max(
            corrected.residual_supremum_upper_bound,
            (
                _absolute_interval_upper(corrected.boundary_slope_residual)
                + schur.derivative_trace_upper_bound
                * corrected.residual_supremum_upper_bound
            )
            / schur.corrected_schur_enclosure.lower,
        )
        self.assertEqual(mismatch.newton_defect_upper_bound, expected_defect)
        weighted = validate_skyrmion_augmented_operator_mismatch(
            schur,
            corrected,
            omega=Fraction(1, 2),
            scalar_weight=Fraction(2),
        )
        reweighted = reweight_skyrmion_augmented_operator_mismatch(
            schur,
            corrected,
            mismatch,
            omega=Fraction(1, 2),
            scalar_weight=Fraction(2),
        )
        self.assertEqual(reweighted, weighted)
        self.assertGreater(
            weighted.interior_operator_mismatch_upper_bound,
            mismatch.interior_operator_mismatch_upper_bound,
        )
        unlinked = validate_skyrmion_endpoint_corrected_residual(
            (profile,),
            RationalInterval.point(0),
            RationalInterval.point(0),
            curvature=0,
            trigonometric_terms=16,
        )
        with self.assertRaisesRegex(ValueError, "origin sensitivities"):
            validate_skyrmion_augmented_operator_mismatch(schur, unlinked)
        wrong_operator = validate_skyrmion_endpoint_corrected_residual(
            (profile,),
            RationalInterval.point(0),
            RationalInterval.point(0),
            phi_sensitivity_at_cutoff=RationalInterval.point(1),
            gamma_sensitivity_at_cutoff=RationalInterval.point(-1000),
            curvature=Fraction(1, 400),
            trigonometric_terms=16,
        )
        with self.assertRaisesRegex(ValueError, "operator parameters"):
            validate_skyrmion_augmented_operator_mismatch(schur, wrong_operator)
        self.assertIn("no nonlinear Newton", mismatch.conclusion_scope)

    def test_augmented_newton_tube_composes_exact_radii_bounds(self):
        zero = RationalInterval.point(0)
        one = RationalInterval.point(1)
        minus_one = RationalInterval.point(-1)
        profile_cell = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        endpoint_cell = SimpleNamespace(
            source_cell_index=0,
            family_profile_jet=SkyrmionJetBox(
                profile_cell.radius,
                one,
                minus_one,
                zero,
            ),
        )
        origin_patch = ValidatedSkyrmionOriginQuinticPatch(
            shooting_slope=Fraction(1),
            cutoff=Fraction(1),
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            cubic_coefficient=Fraction(0),
            quintic_coefficient=Fraction(0),
            remainder_radius=Fraction(1, 100),
            residual_bound=Fraction(0),
            contraction_bound=Fraction(1, 2),
            profile_at_cutoff=one,
            derivative_at_cutoff=minus_one,
        )
        sensitivity = ValidatedSkyrmionOriginSensitivity(
            shooting_slopes=RationalInterval(Fraction(0), Fraction(2)),
            cutoff=Fraction(1),
            remainder_radius=Fraction(1, 100),
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            cubic_coefficient_derivative=zero,
            contraction_bound=Fraction(1, 2),
            partial_map_sensitivity_bound=Fraction(0),
            fixed_point_sensitivity_bound=Fraction(0),
            continuously_differentiable=True,
            profile_sensitivity_at_cutoff=zero,
            derivative_sensitivity_at_cutoff=zero,
        )
        identification = ValidatedSkyrmionOriginQuinticBranchIdentification(
            quintic_patch=origin_patch,
            cubic_sensitivity=sensitivity,
            normalized_momentum_offset_upper_bound=Fraction(0),
            normalized_profile_offset_upper_bound=Fraction(0),
            identified_with_cubic_sensitivity_branch=True,
        )
        second_sensitivity = ValidatedSkyrmionOriginSecondSensitivity(
            shooting_slopes=RationalInterval(Fraction(0), Fraction(2)),
            cutoff=Fraction(1),
            remainder_radius=Fraction(1, 100),
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            cubic_coefficient_second_derivative=zero,
            contraction_bound=Fraction(1, 2),
            first_fixed_point_sensitivity_bound=Fraction(0),
            partial_second_sensitivity_bound=Fraction(0),
            fixed_point_second_sensitivity_bound=Fraction(0),
            twice_continuously_differentiable=True,
            profile_second_sensitivity_at_cutoff=zero,
            derivative_second_sensitivity_at_cutoff=zero,
        )
        endpoint = SimpleNamespace(
            profile_cells=(profile_cell,),
            cells=(endpoint_cell,),
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            phi_at_cutoff=one,
            gamma_at_cutoff=minus_one,
            phi_sensitivity_at_cutoff=zero,
            gamma_sensitivity_at_cutoff=zero,
        )
        schur = SimpleNamespace(
            profile_cells=(profile_cell,),
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            graph_resolvent_bounds=SimpleNamespace(
                c0_upper_bound=Fraction(1),
                c1_upper_bound=Fraction(2),
                c2_upper_bound=Fraction(3),
            ),
            auxiliary_norm_bounds=SimpleNamespace(
                corrected_c0_upper_bound=Fraction(0),
                corrected_c1_upper_bound=Fraction(0),
                corrected_c2_upper_bound=Fraction(0),
            ),
            trace_validation=SimpleNamespace(
                l1_cells=(
                    SimpleNamespace(
                        source_cell_index=0,
                        radius=profile_cell.radius,
                        l1_upper_bound=Fraction(1),
                    ),
                ),
                inverse_c0_bound=Fraction(1),
                residual_supremum_upper_bound=Fraction(0),
                principal_left_lower_bound=Fraction(1),
            ),
            corrected_schur_enclosure=RationalInterval.point(2),
            derivative_trace_upper_bound=Fraction(1),
        )
        mismatch = SimpleNamespace(
            omega=Fraction(1),
            scalar_weight=Fraction(1),
            newton_defect_upper_bound=Fraction(1, 10_000),
            z0_upper_bound=Fraction(1, 10),
        )
        radius = Fraction(1, 1000)
        with patch(
            "qgtoy.validated_skyrmion_bvp."
            "reweight_skyrmion_augmented_operator_mismatch",
            return_value=mismatch,
        ):
            result = validate_skyrmion_augmented_newton_tube(
                schur,
                endpoint,
                mismatch,
                identification,
                second_sensitivity,
                radius,
                trigonometric_terms=16,
            )
            with self.assertRaisesRegex(ValueError, "slope tube"):
                validate_skyrmion_augmented_newton_tube(
                    schur,
                    endpoint,
                    mismatch,
                    identification,
                    second_sensitivity,
                    Fraction(2),
                    trigonometric_terms=16,
                )
            with self.assertRaisesRegex(ValueError, "cutoff"):
                validate_skyrmion_augmented_newton_tube(
                    schur,
                    endpoint,
                    mismatch,
                    replace(
                        identification,
                        quintic_patch=replace(origin_patch, cutoff=Fraction(1, 2)),
                    ),
                    replace(second_sensitivity, cutoff=Fraction(1, 2)),
                    radius,
                    trigonometric_terms=16,
                )
        self.assertEqual(
            result.radii_polynomial_upper_bound,
            mismatch.newton_defect_upper_bound
            + (mismatch.z0_upper_bound - 1) * radius
            + result.schur_composed_hessian_upper_bound * radius**2 / 2,
        )
        self.assertEqual(
            result.contraction_upper_bound,
            mismatch.z0_upper_bound
            + result.schur_composed_hessian_upper_bound * radius,
        )
        self.assertLessEqual(
            result.cells[0].nonlinear_hessian_upper_bound,
            result.cells[0].direct_nonlinear_hessian_upper_bound,
        )
        self.assertLessEqual(
            result.cells[0].nonlinear_hessian_upper_bound,
            result.cells[0].center_equation_hessian_upper_bound,
        )
        self.assertGreaterEqual(
            result.cells[0].center_equation_forcing_upper_bound,
            1,
        )
        self.assertEqual(
            result.shooting_slope_interval,
            RationalInterval(Fraction(999, 1000), Fraction(1001, 1000)),
        )
        self.assertTrue(result.self_map_verified)
        self.assertTrue(result.contraction_verified)

        origin_family = ValidatedSkyrmionOriginFamily(
            shooting_slopes=result.shooting_slope_interval,
            cutoff=Fraction(1),
            pion_mass_squared=Fraction(0),
            curvature=Fraction(0),
            cubic_coefficient=zero,
            remainder_radius=Fraction(1, 100),
            residual_bound=Fraction(0),
            contraction_bound=Fraction(1, 2),
            volterra_denominator_lower_bound=Fraction(1),
            profile_at_cutoff=one,
            derivative_at_cutoff=minus_one,
        )
        observables = validate_skyrmion_newton_physical_observables(
            result,
            origin_family,
            trigonometric_terms=16,
        )
        self.assertGreater(observables.origin_momentum_enclosure.lower, 0)
        self.assertLess(
            observables.positive_radius_derivative_upper_bound,
            0,
        )
        self.assertLess(observables.wall_slope_enclosure.upper, 0)
        self.assertGreater(observables.inertia_enclosure.lower, 0)
        self.assertTrue(observables.strict_monotonicity_verified)
        self.assertTrue(observables.negative_wall_slope_verified)
        self.assertTrue(observables.positive_finite_inertia_verified)

        with self.assertRaisesRegex(ValueError, "slope tube"):
            validate_skyrmion_newton_physical_observables(
                result,
                replace(
                    origin_family,
                    shooting_slopes=RationalInterval(
                        Fraction(1), Fraction(101, 100)
                    ),
                ),
            )
        with self.assertRaisesRegex(ValueError, "closed Newton tube"):
            validate_skyrmion_newton_physical_observables(
                replace(result, contraction_verified=False),
                origin_family,
            )
        with self.assertRaisesRegex(ValueError, "monotonicity"):
            validate_skyrmion_newton_physical_observables(
                replace(
                    result,
                    cells=(
                        replace(
                            result.cells[0],
                            tube_jet=replace(
                                result.cells[0].tube_jet,
                                derivative=RationalInterval(
                                    Fraction(-1), Fraction(0)
                                ),
                            ),
                        ),
                    ),
                ),
                origin_family,
            )

    def test_foundation_certificate_is_explicitly_conditional(self):
        certificate = conditional_skyrmion_barta_foundation_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["executable_checks"].values()))
        self.assertEqual(certificate["cell_count"], 5)
        self.assertGreater(
            float(certificate["recomputed_barta_lower_bound"]),
            1.0,
        )
        self.assertIn("independent conditional inputs", certificate["claim_limit"])
        self.assertIn("neither", certificate["claim_limit"])

    def test_vacuum_point_has_exact_jacobi_coefficients(self):
        jet = SkyrmionJetBox(
            RationalInterval.point(1),
            RationalInterval.point(0),
            RationalInterval.point(0),
            RationalInterval.point(0),
        )
        coefficients = skyrmion_jacobi_coefficient_box(jet)
        self.assertEqual(
            coefficients.principal,
            RationalInterval.point(Fraction(399, 400)),
        )
        self.assertEqual(
            coefficients.principal_derivative,
            RationalInterval.point(Fraction(199, 100)),
        )
        self.assertEqual(
            coefficients.potential,
            RationalInterval.point(3),
        )

    def test_coefficients_contain_independent_float_formula(self):
        x = 0.8741
        profile = 1.8468021948858804
        derivative = -1.3178165571881482
        second_derivative = 0.4362614691220817
        jet = SkyrmionJetBox(
            RationalInterval.point(Fraction(8741, 10_000)),
            RationalInterval.point(Fraction(1_846_802_194_885_880, 10**15)),
            RationalInterval.point(Fraction(-1_317_816_557_188_148, 10**15)),
            RationalInterval.point(Fraction(436_261_469_122_081, 10**15)),
        )
        coefficients = skyrmion_jacobi_coefficient_box(jet)

        curvature = 1.0 / 400.0
        lapse = 1.0 - curvature * x * x
        lapse_derivative = -2.0 * curvature * x
        sine = math.sin(profile)
        sine_twice = math.sin(2.0 * profile)
        cosine_twice = math.cos(2.0 * profile)
        principal = lapse * (x * x + 8.0 * sine * sine)
        principal_derivative = (
            lapse_derivative * (x * x + 8.0 * sine * sine)
            + lapse * (2.0 * x + 8.0 * sine_twice * derivative)
        )
        potential = (
            4.0 * sine_twice**2 / x**2
            + 2.0
            * (1.0 + 4.0 * sine**2 / x**2)
            * cosine_twice
            - 8.0 * lapse * cosine_twice * derivative**2
            + x**2 * math.cos(profile)
            - 8.0 * lapse_derivative * sine_twice * derivative
            - 8.0 * lapse * sine_twice * second_derivative
        )
        for enclosure, diagnostic in (
            (coefficients.principal, principal),
            (coefficients.principal_derivative, principal_derivative),
            (coefficients.potential, potential),
        ):
            self.assertLessEqual(float(enclosure.lower) - 1.0e-12, diagnostic)
            self.assertGreaterEqual(float(enclosure.upper) + 1.0e-12, diagnostic)

    def test_barta_formula_matches_direct_witness_derivatives(self):
        jet = SkyrmionJetBox(
            RationalInterval.point(Fraction(7, 8)),
            RationalInterval.point(Fraction(37, 20)),
            RationalInterval.point(Fraction(-33, 25)),
            RationalInterval.point(Fraction(11, 25)),
        )
        coefficients, quotient = skyrmion_barta_quotient_box(jet)
        z = Fraction(7, 8) - Fraction(33, 16)
        denominator = z**2 + 4
        witness = Fraction(8, 1) / denominator
        witness_derivative = -16 * z / denominator**2
        witness_second_derivative = (
            48 * z**2 - 64
        ) / denominator**3
        direct = (
            coefficients.potential
            - coefficients.principal_derivative
            * (witness_derivative / witness)
            - coefficients.principal
            * (witness_second_derivative / witness)
        )
        self.assertEqual(quotient, direct)

    def test_real_conditional_tube_recomputes_bound_above_one(self):
        cells = _floating_profile_cells()
        validation = validate_skyrmion_barta_cells(cells, Fraction(1))
        self.assertEqual(len(validation.cells), len(cells))
        self.assertGreater(validation.recomputed_lower_bound, 1)
        self.assertEqual(
            validation.recomputed_lower_bound,
            min(cell.quotient.lower for cell in validation.cells),
        )
        self.assertTrue(
            all(cell.coefficients.principal.lower > 0 for cell in validation.cells)
        )

    def test_declared_bound_and_modified_jet_are_not_trusted(self):
        cells = _floating_profile_cells()
        with self.assertRaisesRegex(ValueError, "declared Barta"):
            validate_skyrmion_barta_cells(cells, Fraction(3, 2))
        altered = SkyrmionJetBox(
            cells[2].radius,
            cells[2].profile,
            cells[2].derivative,
            RationalInterval(Fraction(-11), Fraction(-10)),
        )
        with self.assertRaisesRegex(ValueError, "declared Barta"):
            validate_skyrmion_barta_cells((altered,), Fraction(1))

    def test_rejects_invalid_domains_and_cell_collections(self):
        base = _floating_profile_cells()[0]
        from_list = validate_skyrmion_barta_cells(
            list(_floating_profile_cells()), 1
        )
        self.assertEqual(len(from_list.cells), len(_floating_profile_cells()))
        with self.assertRaises(ValueError):
            validate_skyrmion_barta_cells((), 1)
        with self.assertRaises(ValueError):
            skyrmion_jacobi_coefficient_box(
                SkyrmionJetBox(
                    RationalInterval(Fraction(0), Fraction(1)),
                    base.profile,
                    base.derivative,
                    base.second_derivative,
                )
            )
        with self.assertRaises(ValueError):
            skyrmion_jacobi_coefficient_box(
                SkyrmionJetBox(
                    RationalInterval(Fraction(20), Fraction(21)),
                    base.profile,
                    base.derivative,
                    base.second_derivative,
                )
            )

    def test_exact_polynomial_schur_audit_applies_left_lift_and_passes(self):
        zero_cell = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        validation = validate_skyrmion_polynomial_schur_bound(
            (zero_cell,),
            (zero_cell,),
            RationalInterval.point(1),
            RationalInterval.point(-1000),
            Fraction(1),
            Fraction(1),
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=2,
            residual_initial_subdivisions=2,
            residual_maximum_refinement_depth=2,
            curvature=0,
            trigonometric_terms=16,
        )
        self.assertEqual(
            validation.affine_left_lift_coefficient,
            RationalInterval.point(1),
        )
        self.assertEqual(
            validation.affine_left_lift_derivative,
            RationalInterval.point(-1),
        )
        self.assertEqual(
            validation.raw_schur_enclosure,
            RationalInterval.point(999),
        )
        self.assertEqual(validation.inverse_c0_bound, Fraction(2))
        self.assertEqual(validation.principal_lower_bound, Fraction(1))
        self.assertEqual(
            validation.potential_l1_upper_bound,
            Fraction(41, 8),
        )
        self.assertEqual(
            validation.boundary_derivative_c1_bound,
            Fraction(45, 4),
        )
        self.assertGreater(validation.corrected_schur_enclosure.lower, 1)
        self.assertIn("no nonlinear BVP", validation.conclusion_scope)

    def test_polynomial_schur_audit_rejects_an_unproved_declared_margin(self):
        zero_cell = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        with self.assertRaisesRegex(ValueError, "positive Schur lower bound"):
            validate_skyrmion_polynomial_schur_bound(
                (zero_cell,),
                (zero_cell,),
                RationalInterval.point(0),
                RationalInterval.point(-1),
                Fraction(1, 100),
                Fraction(2),
                barta_initial_subdivisions=1,
                barta_maximum_refinement_depth=0,
                residual_initial_subdivisions=1,
                residual_maximum_refinement_depth=0,
                curvature=0,
                trigonometric_terms=12,
                residual_taylor_terms=4,
            )

    def test_polynomial_schur_audit_rejects_wall_and_mesh_mismatches(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        nonzero_wall = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1),)),
        )
        with self.assertRaisesRegex(ValueError, "right wall"):
            validate_skyrmion_polynomial_schur_bound(
                (profile,),
                (nonzero_wall,),
                RationalInterval.point(0),
                RationalInterval.point(-10),
                1,
                1,
                curvature=0,
            )
        wrong_mesh = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(3)),
            RationalPolynomial((Fraction(0),)),
        )
        with self.assertRaisesRegex(ValueError, "meshes"):
            validate_skyrmion_polynomial_schur_bound(
                (profile,),
                (wrong_mesh,),
                RationalInterval.point(0),
                RationalInterval.point(-10),
                1,
                1,
                curvature=0,
            )

    def test_polynomial_schur_audit_guards_c0_witness_ratio(self):
        wide = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1, 100), Fraction(10)),
            RationalPolynomial((Fraction(0),)),
        )
        with self.assertRaisesRegex(ValueError, "max/min ratio"):
            validate_skyrmion_polynomial_schur_bound(
                (wide,),
                (wide,),
                RationalInterval.point(0),
                RationalInterval.point(-10),
                1,
                1,
                curvature=0,
            )

    def test_derivative_trace_representer_audits_vacuum_linear_candidate(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        representer = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1), Fraction(-1))),
        )
        validation = validate_skyrmion_derivative_trace_representer(
            (profile,),
            (representer,),
            Fraction(1),
            Fraction(20),
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=2,
            residual_initial_subdivisions=2,
            residual_maximum_refinement_depth=2,
            curvature=0,
            trigonometric_terms=16,
        )
        self.assertEqual(
            validation.approximate_representer_l1_upper_bound,
            Fraction(1, 2),
        )
        self.assertTrue(validation.l1_cells[0].integrated_with_fixed_sign)
        self.assertEqual(
            validation.l1_cells[0].bernstein_range,
            RationalInterval(Fraction(0), Fraction(1)),
        )
        self.assertEqual(
            validation.barta_witness_ratio_upper_bound,
            Fraction(1313, 1025),
        )
        self.assertEqual(
            validation.inverse_c0_bound,
            Fraction(1313, 1025),
        )
        self.assertEqual(
            validation.principal_left_enclosure,
            RationalInterval.point(1),
        )
        self.assertEqual(
            validation.recomputed_trace_upper_bound,
            validation.representer_l1_upper_bound,
        )
        self.assertLess(validation.recomputed_trace_upper_bound, 20)
        self.assertIn("no nonlinear BVP", validation.conclusion_scope)

    def test_derivative_trace_representer_rejects_endpoint_and_mesh_errors(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        wrong_left = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(2), Fraction(-2))),
        )
        with self.assertRaisesRegex(ValueError, "left endpoint"):
            validate_skyrmion_derivative_trace_representer(
                (profile,), (wrong_left,), 1, 100, curvature=0
            )

        wrong_wall = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1),)),
        )
        with self.assertRaisesRegex(ValueError, "right wall"):
            validate_skyrmion_derivative_trace_representer(
                (profile,), (wrong_wall,), 1, 100, curvature=0
            )

        wrong_mesh = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(3)),
            RationalPolynomial((Fraction(1), Fraction(-1))),
        )
        with self.assertRaisesRegex(ValueError, "meshes"):
            validate_skyrmion_derivative_trace_representer(
                (profile,), (wrong_mesh,), 1, 100, curvature=0
            )

    def test_derivative_trace_representer_rejects_unproved_declared_bound(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        representer = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1), Fraction(-1))),
        )
        with self.assertRaisesRegex(ValueError, "derivative-trace upper bound"):
            validate_skyrmion_derivative_trace_representer(
                (profile,),
                (representer,),
                1,
                1,
                barta_initial_subdivisions=2,
                barta_maximum_refinement_depth=2,
                residual_initial_subdivisions=2,
                residual_maximum_refinement_depth=2,
                curvature=0,
                trigonometric_terms=16,
            )

    def test_trace_sharpened_schur_audit_orders_trace_before_correction(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        representer = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1), Fraction(-1))),
        )
        validation = validate_skyrmion_trace_sharpened_schur_bound(
            (profile,),
            (representer,),
            (representer,),
            RationalInterval(Fraction(1), Fraction(101, 100)),
            RationalInterval.point(-1000),
            Fraction(1),
            Fraction(20),
            Fraction(1),
            barta_initial_subdivisions=2,
            barta_maximum_refinement_depth=2,
            trace_residual_initial_subdivisions=2,
            trace_residual_maximum_refinement_depth=2,
            schur_residual_initial_subdivisions=2,
            schur_residual_maximum_refinement_depth=2,
            curvature=0,
            trigonometric_terms=16,
        )
        self.assertEqual(
            validation.raw_schur_enclosure,
            RationalInterval(Fraction(99899, 100), Fraction(999)),
        )
        self.assertEqual(
            validation.derivative_trace_upper_bound,
            validation.trace_validation.recomputed_trace_upper_bound,
        )
        self.assertEqual(
            validation.boundary_derivative_error_bound,
            validation.derivative_trace_upper_bound
            * validation.residual_supremum_upper_bound,
        )
        self.assertEqual(
            validation.graph_resolvent_bounds.barta_lower_bound,
            validation.trace_validation.barta_validation.recomputed_lower_bound,
        )
        graph = validation.graph_resolvent_bounds
        barta_cells = validation.trace_validation.barta_validation.cells
        expected_p0 = min(
            cell.coefficients.principal.lower for cell in barta_cells
        )
        expected_p1 = max(
            _absolute_interval_upper(cell.coefficients.principal_derivative)
            for cell in barta_cells
        )
        expected_q1 = sum(
            cell.jet.radius.width
            * _absolute_interval_upper(cell.coefficients.potential)
            for cell in barta_cells
        )
        expected_qinf = max(
            _absolute_interval_upper(cell.coefficients.potential)
            for cell in barta_cells
        )
        expected_c0 = (
            graph.barta_witness_ratio_upper_bound / graph.barta_lower_bound
        )
        expected_c1 = (
            graph.domain_length + expected_q1 * expected_c0
        ) / expected_p0
        expected_c2 = (
            1 + expected_p1 * expected_c1 + expected_qinf * expected_c0
        ) / expected_p0
        self.assertEqual(graph.principal_lower_bound, expected_p0)
        self.assertEqual(
            graph.principal_derivative_supremum_upper_bound, expected_p1
        )
        self.assertEqual(graph.potential_l1_upper_bound, expected_q1)
        self.assertEqual(graph.potential_supremum_upper_bound, expected_qinf)
        self.assertEqual(graph.c0_upper_bound, expected_c0)
        self.assertEqual(graph.c1_upper_bound, expected_c1)
        self.assertEqual(graph.c2_upper_bound, expected_c2)
        norms = validation.auxiliary_norm_bounds
        self.assertEqual(
            norms.corrected_c0_upper_bound,
            norms.approximate_c0_upper_bound
            + graph.c0_upper_bound * norms.residual_supremum_upper_bound,
        )
        self.assertEqual(
            norms.corrected_c1_upper_bound,
            norms.approximate_c1_upper_bound
            + graph.c1_upper_bound * norms.residual_supremum_upper_bound,
        )
        self.assertEqual(
            norms.corrected_c2_upper_bound,
            norms.approximate_c2_upper_bound
            + graph.c2_upper_bound * norms.residual_supremum_upper_bound,
        )
        self.assertGreaterEqual(
            norms.corrected_c0_upper_bound,
            norms.approximate_c0_upper_bound,
        )
        self.assertGreaterEqual(
            norms.corrected_c1_upper_bound,
            norms.approximate_c1_upper_bound,
        )
        self.assertGreaterEqual(
            norms.corrected_c2_upper_bound,
            norms.approximate_c2_upper_bound,
        )
        self.assertGreater(validation.corrected_schur_enclosure.lower, 1)
        self.assertIn("no nonlinear BVP", validation.conclusion_scope)

    def test_trace_sharpened_schur_audit_requires_trace_first(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        representer = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1), Fraction(-1))),
        )
        with self.assertRaisesRegex(ValueError, "derivative-trace upper bound"):
            validate_skyrmion_trace_sharpened_schur_bound(
                (profile,),
                (representer,),
                (representer,),
                RationalInterval.point(1),
                RationalInterval.point(-1000),
                Fraction(1),
                Fraction(1),
                Fraction(1),
                barta_initial_subdivisions=2,
                barta_maximum_refinement_depth=2,
                trace_residual_initial_subdivisions=2,
                trace_residual_maximum_refinement_depth=2,
                curvature=0,
                trigonometric_terms=16,
            )

    def test_trace_sharpened_schur_audit_rejects_unproved_margin(self):
        profile = SkyrmionPolynomialCell(
            RationalInterval(Fraction(1), Fraction(2)),
            RationalPolynomial((Fraction(0),)),
        )
        representer = SkyrmionPolynomialCell(
            profile.radius,
            RationalPolynomial((Fraction(1), Fraction(-1))),
        )
        with self.assertRaisesRegex(ValueError, "trace-sharpened Schur"):
            validate_skyrmion_trace_sharpened_schur_bound(
                (profile,),
                (profile,),
                (representer,),
                RationalInterval.point(0),
                RationalInterval.point(-1),
                Fraction(1),
                Fraction(20),
                Fraction(2),
                barta_initial_subdivisions=2,
                barta_maximum_refinement_depth=2,
                trace_residual_initial_subdivisions=2,
                trace_residual_maximum_refinement_depth=2,
                schur_residual_initial_subdivisions=1,
                schur_residual_maximum_refinement_depth=0,
                curvature=0,
                trigonometric_terms=12,
                residual_taylor_terms=4,
            )


if __name__ == "__main__":
    unittest.main()
