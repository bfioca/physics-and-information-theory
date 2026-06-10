import unittest
from fractions import Fraction

from qgtoy.skyrmion_global_bvp_certificate_generator import (
    generate_global_bvp_certificate_candidate,
)
from qgtoy.validated_skyrmion_bvp import (
    SkyrmionPolynomialCell,
    _absolute_interval_upper,
    _lifted_auxiliary_residual_cell,
    validate_skyrmion_polynomial_barta_spline,
)
from qgtoy.validated_skyrmion_origin import (
    validate_skyrmion_origin_quintic_patch,
)


def _representative_graded_mesh():
    nodes = [Fraction(1, 16)]
    for segment_end, width in (
        (Fraction(1, 8), Fraction(1, 128)),
        (Fraction(1, 4), Fraction(1, 64)),
        (Fraction(1, 2), Fraction(1, 32)),
    ):
        while nodes[-1] < segment_end:
            nodes.append(nodes[-1] + width)
        if nodes[-1] != segment_end:
            raise AssertionError("graded mesh segment width must divide its interval")
    while nodes[-1] + Fraction(3, 16) < 4:
        nodes.append(nodes[-1] + Fraction(3, 16))
    nodes.append(Fraction(4))
    return tuple(nodes)


class SkyrmionGlobalBvpCertificateGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.candidate = generate_global_bvp_certificate_candidate(
            mesh_width=Fraction(3, 16),
            integration_step=1 / 1024,
            trigonometric_terms=18,
        )

    def test_profile_is_exact_rational_globally_c2_quintic(self):
        candidate = self.candidate
        self.assertEqual(
            candidate.result_type,
            "untrusted_global_bvp_certificate_candidate_data",
        )
        self.assertEqual(candidate.profile_degree, 5)
        self.assertEqual(len(candidate.cells), 21)
        self.assertEqual(candidate.radius_start, Fraction(1, 16))
        self.assertEqual(candidate.radius_end, Fraction(4))
        self.assertEqual(candidate.mesh_width, Fraction(3, 16))
        self.assertEqual(
            candidate.mesh_nodes,
            tuple(
                Fraction(1, 16) + index * Fraction(3, 16)
                for index in range(22)
            ),
        )
        self.assertEqual(candidate.floating_diagnostics["mesh_kind"], "uniform")
        self.assertFalse(hasattr(candidate, "status"))
        for cell in candidate.cells:
            self.assertEqual(cell.profile_polynomial.degree, 5)
            self.assertIsInstance(cell.nonlinear_residual_absolute_upper, Fraction)
            self.assertGreaterEqual(cell.nonlinear_residual_absolute_upper, 0)
            for point in (Fraction(0), Fraction(1, 2), Fraction(1)):
                polynomial = cell.profile_polynomial
                for derivative_order, enclosure in enumerate(
                    (cell.profile, cell.derivative, cell.second_derivative)
                ):
                    if derivative_order:
                        polynomial = polynomial.derivative()
                    value = polynomial.evaluate(point).scale(
                        1 / cell.width**derivative_order
                    )
                    self.assertTrue(value.is_subset_of(enclosure))
        for left, right in zip(candidate.cells, candidate.cells[1:]):
            self.assertEqual(left.radius.upper, right.radius.lower)
            left_width = left.width
            right_width = right.width
            for derivative_order in range(3):
                left_polynomial = left.profile_polynomial
                right_polynomial = right.profile_polynomial
                for _ in range(derivative_order):
                    left_polynomial = left_polynomial.derivative()
                    right_polynomial = right_polynomial.derivative()
                left_value = left_polynomial.evaluate(Fraction(1)).scale(
                    1 / left_width**derivative_order
                )
                right_value = right_polynomial.evaluate(Fraction(0)).scale(
                    1 / right_width**derivative_order
                )
                self.assertEqual(left_value, right_value)

    def test_boundary_and_cell_boxes_are_raw_recomputable_data(self):
        candidate = self.candidate
        origin = validate_skyrmion_origin_quintic_patch(
            candidate.shooting_slope,
            cutoff=candidate.radius_start,
        )
        self.assertEqual(
            candidate.cells[0].profile_polynomial.evaluate(Fraction(0)),
            type(origin.profile_at_cutoff).point(
                origin.profile_at_cutoff.midpoint
            ),
        )
        self.assertEqual(
            candidate.cells[0]
            .profile_polynomial.derivative()
            .evaluate(Fraction(0))
            .scale(1 / candidate.cells[0].width),
            type(origin.derivative_at_cutoff).point(
                origin.derivative_at_cutoff.midpoint
            ),
        )
        self.assertEqual(
            candidate.boundary_residuals["right_dirichlet_profile"],
            candidate.cells[-1].profile_polynomial.evaluate(Fraction(1)),
        )
        self.assertLess(
            candidate.boundary_residuals["right_dirichlet_profile"].upper,
            Fraction(1, 100_000),
        )
        self.assertTrue(
            candidate.boundary_residuals[
                "left_profile_minus_validated_origin_box"
            ].contains_zero()
        )
        self.assertTrue(
            candidate.boundary_residuals[
                "left_derivative_minus_validated_origin_box"
            ].contains_zero()
        )
        self.assertEqual(
            candidate.maximum_nonlinear_residual_absolute_upper,
            max(cell.nonlinear_residual_absolute_upper for cell in candidate.cells),
        )
        for cell in candidate.cells:
            self.assertGreater(cell.radius.lower, 0)
            self.assertFalse(cell.profile.width < 0)
            self.assertFalse(cell.derivative.width < 0)
            self.assertFalse(cell.second_derivative.width < 0)
            self.assertEqual(len(cell.nonlinear_residual_subcells), 4)
            self.assertEqual(
                cell.nonlinear_residual.lower,
                min(box.lower for box in cell.nonlinear_residual_subcells),
            )
            self.assertEqual(
                cell.nonlinear_residual.upper,
                max(box.upper for box in cell.nonlinear_residual_subcells),
            )
            self.assertTrue(
                cell.nonlinear_residual.is_subset_of(
                    cell.coarse_nonlinear_residual
                )
            )

    def test_centered_subcell_residuals_quantifiably_reduce_wrapping(self):
        candidate = self.candidate
        coarse_profile_maximum = max(
            cell.coarse_nonlinear_residual_absolute_upper
            for cell in candidate.cells
        )
        self.assertGreater(coarse_profile_maximum, Fraction(120))
        self.assertLess(candidate.maximum_nonlinear_residual_absolute_upper, 11)
        self.assertLess(
            candidate.maximum_nonlinear_residual_absolute_upper * 10,
            coarse_profile_maximum,
        )
        self.assertEqual(
            candidate.floating_diagnostics["residual_subdivisions_per_cell"],
            4,
        )
        self.assertEqual(
            candidate.floating_diagnostics[
                "coarse_maximum_nonlinear_residual_absolute_upper"
            ],
            float(coarse_profile_maximum),
        )
        self.assertEqual(
            candidate.floating_diagnostics[
                "centered_maximum_nonlinear_residual_absolute_upper"
            ],
            float(candidate.maximum_nonlinear_residual_absolute_upper),
        )

    def test_trusted_adaptive_barta_checker_covers_the_complete_spline(self):
        polynomial_cells = tuple(
            SkyrmionPolynomialCell(
                cell.radius,
                cell.profile_polynomial,
            )
            for cell in self.candidate.cells
        )
        validation = validate_skyrmion_polynomial_barta_spline(
            polynomial_cells,
            Fraction(3, 2),
            initial_subdivisions=4,
            maximum_refinement_depth=5,
            trigonometric_terms=24,
        )
        self.assertEqual(validation.source_cell_count, len(polynomial_cells))
        self.assertGreater(validation.recomputed_lower_bound, Fraction(3, 2))
        self.assertEqual(validation.maximum_refinement_depth_used, 5)
        self.assertEqual(len(validation.cells), 207)

    def test_trusted_spline_checker_rejects_a_broken_c2_join(self):
        polynomial_cells = [
            SkyrmionPolynomialCell(cell.radius, cell.profile_polynomial)
            for cell in self.candidate.cells[:2]
        ]
        second = polynomial_cells[1]
        coefficients = list(second.profile_polynomial.coefficients)
        coefficients[0] += Fraction(1, 10**6)
        polynomial_cells[1] = SkyrmionPolynomialCell(
            second.radius,
            type(second.profile_polynomial)(tuple(coefficients)),
        )
        with self.assertRaisesRegex(ValueError, "globally C2"):
            validate_skyrmion_polynomial_barta_spline(
                polynomial_cells,
                Fraction(1),
                trigonometric_terms=18,
            )

    def test_optional_homogeneous_sensitivity_is_globally_c2(self):
        candidate = self.candidate
        self.assertEqual(candidate.homogeneous_degree, 5)
        self.assertEqual(len(candidate.homogeneous_cells), len(candidate.cells))
        self.assertEqual(
            candidate.maximum_homogeneous_residual_absolute_upper,
            max(
                cell.jacobi_residual_absolute_upper
                for cell in candidate.homogeneous_cells
            ),
        )
        for left, right in zip(
            candidate.homogeneous_cells, candidate.homogeneous_cells[1:]
        ):
            for derivative_order in range(3):
                left_polynomial = left.function_polynomial
                right_polynomial = right.function_polynomial
                for _ in range(derivative_order):
                    left_polynomial = left_polynomial.derivative()
                    right_polynomial = right_polynomial.derivative()
                self.assertEqual(
                    left_polynomial.evaluate(Fraction(1)).scale(
                        1 / left.radius.width**derivative_order
                    ),
                    right_polynomial.evaluate(Fraction(0)).scale(
                        1 / right.radius.width**derivative_order
                    ),
                )
        coarse_jacobi_maximum = max(
            cell.coarse_jacobi_residual_absolute_upper
            for cell in candidate.homogeneous_cells
        )
        self.assertLess(
            candidate.maximum_homogeneous_residual_absolute_upper * 10,
            coarse_jacobi_maximum,
        )
        for cell in candidate.homogeneous_cells:
            self.assertEqual(len(cell.jacobi_residual_subcells), 4)
            self.assertEqual(
                cell.jacobi_residual.lower,
                min(box.lower for box in cell.jacobi_residual_subcells),
            )
            self.assertEqual(
                cell.jacobi_residual.upper,
                max(box.upper for box in cell.jacobi_residual_subcells),
            )
            self.assertTrue(
                cell.jacobi_residual.is_subset_of(cell.coarse_jacobi_residual)
            )

    def test_fundamental_and_wall_dirichlet_auxiliary_are_separate_c2_data(self):
        candidate = self.candidate
        self.assertIs(candidate.shooting_sensitivity_cells, candidate.homogeneous_cells)
        self.assertEqual(candidate.fundamental_degree, 5)
        self.assertEqual(candidate.schur_auxiliary_degree, 5)
        self.assertEqual(len(candidate.fundamental_cells), len(candidate.cells))
        self.assertEqual(
            len(candidate.schur_auxiliary_cells), len(candidate.cells)
        )
        self.assertNotEqual(
            candidate.homogeneous_cells,
            candidate.schur_auxiliary_cells,
        )
        for collection in (
            candidate.fundamental_cells,
            candidate.schur_auxiliary_cells,
        ):
            for left, right in zip(collection, collection[1:]):
                for derivative_order in range(3):
                    left_polynomial = left.function_polynomial
                    right_polynomial = right.function_polynomial
                    for _ in range(derivative_order):
                        left_polynomial = left_polynomial.derivative()
                        right_polynomial = right_polynomial.derivative()
                    self.assertEqual(
                        left_polynomial.evaluate(Fraction(1)).scale(
                            1 / left.radius.width**derivative_order
                        ),
                        right_polynomial.evaluate(Fraction(0)).scale(
                            1 / right.radius.width**derivative_order
                        ),
                    )

    def test_exact_schur_combination_has_exact_wall_zero(self):
        candidate = self.candidate
        coefficient = candidate.schur_combination_coefficient
        self.assertIsInstance(coefficient, Fraction)
        for shooting, fundamental, auxiliary in zip(
            candidate.homogeneous_cells,
            candidate.fundamental_cells,
            candidate.schur_auxiliary_cells,
        ):
            degree = max(
                shooting.function_polynomial.degree,
                fundamental.function_polynomial.degree,
                auxiliary.function_polynomial.degree,
            )
            for index in range(degree + 1):
                shooting_coefficient = (
                    shooting.function_polynomial.coefficients[index]
                    if index <= shooting.function_polynomial.degree
                    else Fraction(0)
                )
                fundamental_coefficient = (
                    fundamental.function_polynomial.coefficients[index]
                    if index <= fundamental.function_polynomial.degree
                    else Fraction(0)
                )
                auxiliary_coefficient = (
                    auxiliary.function_polynomial.coefficients[index]
                    if index <= auxiliary.function_polynomial.degree
                    else Fraction(0)
                )
                self.assertEqual(
                    auxiliary_coefficient,
                    shooting_coefficient + coefficient * fundamental_coefficient,
                )
        self.assertEqual(
            candidate.schur_auxiliary_cells[-1].function_polynomial.evaluate(
                Fraction(1)
            ),
            candidate.auxiliary_boundary_residuals[
                "schur_auxiliary_right_value"
            ],
        )
        self.assertEqual(
            candidate.auxiliary_boundary_residuals[
                "schur_auxiliary_right_value"
            ],
            type(candidate.cells[0].profile).point(0),
        )
        self.assertFalse(
            candidate.auxiliary_boundary_residuals[
                "shooting_right_value"
            ].contains_zero()
        )

    def test_fundamental_initial_data_and_raw_schur_margin(self):
        candidate = self.candidate
        first = candidate.fundamental_cells[0]
        self.assertEqual(
            first.function_polynomial.evaluate(Fraction(0)),
            type(first.function).point(0),
        )
        self.assertEqual(
            first.function_polynomial.derivative()
            .evaluate(Fraction(0))
            .scale(1 / first.radius.width),
            type(first.function).point(1),
        )
        self.assertEqual(
            candidate.auxiliary_boundary_residuals[
                "fundamental_left_value"
            ],
            type(first.function).point(0),
        )
        self.assertEqual(
            candidate.auxiliary_boundary_residuals[
                "fundamental_left_derivative_minus_one"
            ],
            type(first.function).point(0),
        )
        self.assertEqual(
            candidate.raw_schur_candidate,
            candidate.auxiliary_boundary_residuals["raw_schur_candidate"],
        )
        self.assertFalse(candidate.raw_schur_candidate.contains_zero())
        self.assertGreater(candidate.raw_schur_candidate.lower, 2)
        self.assertLess(candidate.raw_schur_candidate.upper, 4)
        self.assertEqual(
            candidate.maximum_fundamental_residual_absolute_upper,
            max(
                cell.jacobi_residual_absolute_upper
                for cell in candidate.fundamental_cells
            ),
        )
        self.assertEqual(
            candidate.maximum_schur_auxiliary_residual_absolute_upper,
            max(
                cell.jacobi_residual_absolute_upper
                for cell in candidate.schur_auxiliary_cells
            ),
        )

    def test_combined_residual_reduces_representative_material_wrapping(self):
        candidate = self.candidate
        profile = SkyrmionPolynomialCell(
            candidate.cells[0].radius,
            candidate.cells[0].profile_polynomial,
        )
        auxiliary = SkyrmionPolynomialCell(
            candidate.schur_auxiliary_cells[0].radius,
            candidate.schur_auxiliary_cells[0].function_polynomial,
        )
        domain_right = candidate.cells[-1].radius.upper
        domain_length = domain_right - candidate.cells[0].radius.lower
        residuals = tuple(
            _lifted_auxiliary_residual_cell(
                profile,
                auxiliary,
                source_cell_index=0,
                normalized_left=Fraction(index, 4),
                normalized_right=Fraction(index + 1, 4),
                refinement_depth=0,
                domain_right=domain_right,
                domain_length=domain_length,
                lift_coefficient=type(candidate.cells[0].profile).point(0),
                pion_mass_squared=Fraction(1),
                curvature=Fraction(1, 400),
                trigonometric_terms=18,
                residual_taylor_terms=8,
            ).residual
            for index in range(4)
        )
        maximum = max(_absolute_interval_upper(value) for value in residuals)
        self.assertGreater(maximum, Fraction(69, 10))
        self.assertLess(
            maximum,
            candidate.maximum_schur_auxiliary_residual_absolute_upper,
        )

    def test_explicit_representative_graded_mesh_is_exact(self):
        nodes = _representative_graded_mesh()
        candidate = generate_global_bvp_certificate_candidate(
            mesh_nodes=nodes,
            include_homogeneous_sensitivity=False,
            integration_step=1 / 512,
            trigonometric_terms=8,
            residual_subdivisions=1,
        )
        self.assertIsNone(candidate.mesh_width)
        self.assertEqual(candidate.mesh_nodes, nodes)
        self.assertEqual(len(candidate.cells), 43)
        self.assertEqual(candidate.floating_diagnostics["mesh_kind"], "explicit")
        self.assertEqual(
            candidate.floating_diagnostics["minimum_mesh_width"],
            float(Fraction(1, 128)),
        )
        self.assertEqual(
            candidate.floating_diagnostics["maximum_mesh_width"],
            float(Fraction(3, 16)),
        )
        self.assertEqual(
            tuple(cell.radius.lower for cell in candidate.cells)
            + (candidate.cells[-1].radius.upper,),
            nodes,
        )

    def test_explicit_mesh_is_shared_by_profile_and_all_jacobi_families(self):
        nodes = tuple(
            Fraction(value)
            for value in (Fraction(1, 16), Fraction(1, 8), Fraction(1, 4), 1, 2, 4)
        )
        candidate = generate_global_bvp_certificate_candidate(
            mesh_nodes=nodes,
            integration_step=1 / 512,
            trigonometric_terms=8,
            residual_subdivisions=2,
        )
        expected_radii = tuple(
            (left, right) for left, right in zip(nodes, nodes[1:])
        )
        collections = (
            candidate.cells,
            candidate.homogeneous_cells,
            candidate.fundamental_cells,
            candidate.schur_auxiliary_cells,
        )
        for collection in collections:
            self.assertEqual(
                tuple((cell.radius.lower, cell.radius.upper) for cell in collection),
                expected_radii,
            )
            for left, right in zip(collection, collection[1:]):
                left_polynomial = (
                    left.profile_polynomial
                    if hasattr(left, "profile_polynomial")
                    else left.function_polynomial
                )
                right_polynomial = (
                    right.profile_polynomial
                    if hasattr(right, "profile_polynomial")
                    else right.function_polynomial
                )
                for derivative_order in range(3):
                    self.assertEqual(
                        left_polynomial.evaluate(Fraction(1)).scale(
                            1 / left.radius.width**derivative_order
                        ),
                        right_polynomial.evaluate(Fraction(0)).scale(
                            1 / right.radius.width**derivative_order
                        ),
                    )
                    left_polynomial = left_polynomial.derivative()
                    right_polynomial = right_polynomial.derivative()
        self.assertEqual(
            candidate.schur_auxiliary_cells[-1].function_polynomial.evaluate(
                Fraction(1)
            ),
            type(candidate.cells[0].profile).point(0),
        )

    def test_invalid_mesh_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "must divide"):
            generate_global_bvp_certificate_candidate(mesh_width=Fraction(1, 10))
        with self.assertRaisesRegex(ValueError, "at least two"):
            generate_global_bvp_certificate_candidate(mesh_nodes=(Fraction(1, 16),))
        with self.assertRaisesRegex(ValueError, "begin at radius_start"):
            generate_global_bvp_certificate_candidate(
                mesh_nodes=(Fraction(1, 8), Fraction(4))
            )
        with self.assertRaisesRegex(ValueError, "strictly increasing"):
            generate_global_bvp_certificate_candidate(
                mesh_nodes=(Fraction(1, 16), Fraction(1, 2), Fraction(1, 2), 4)
            )
        with self.assertRaisesRegex(TypeError, r"mesh_nodes\[1\]"):
            generate_global_bvp_certificate_candidate(
                mesh_nodes=(Fraction(1, 16), 0.5, 4)
            )
        with self.assertRaisesRegex(ValueError, "residual_subdivisions"):
            generate_global_bvp_certificate_candidate(residual_subdivisions=0)


if __name__ == "__main__":
    unittest.main()
