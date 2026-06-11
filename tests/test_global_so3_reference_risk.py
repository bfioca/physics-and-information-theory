import math
import unittest

import numpy as np

from qgtoy.global_so3_reference_risk import (
    SO3_ASYMMETRY_RISK_CONSTANT,
    asymmetry_orientation_risk_lower_bound,
    compact_rotor_orientation_risk_record,
    fusion_score_matrix,
    fusion_score_maximum_eigenvalue,
    global_so3_reference_risk_certificate,
    hard_cutoff_orientation_risk_lower_bound,
    heat_diffused_orientation_risk_lower_bound,
    log_spin_gibbs_partition,
    maximum_dimensionless_coherence_time,
    mean_casimir_orientation_risk_lower_bound,
    mean_spin_asymmetry_upper_bound,
    mean_spin_orientation_risk_lower_bound,
    mean_spin_upper_bound_from_mean_casimir,
    optimal_spin_gibbs_dual_parameter,
    optimized_mean_spin_asymmetry_upper_bound,
    peter_weyl_token_risk_audit,
    projective_fusion_score_matrix,
    projective_hard_cutoff_orientation_risk_lower_bound,
    projective_mean_casimir_orientation_risk_lower_bound,
    so3_chordal_frame_cost,
    so3_cost_partition_upper_bound,
    so3_haar_ball_volume,
    spin_gibbs_mean,
    spin_gibbs_partition,
    tail_quantile_orientation_risk_lower_bound,
)


def _spin_one_clebsch_gordan(
    input_spin: int,
    magnetic_index: int,
    spin_one_index: int,
    output_spin: int,
) -> float:
    """Return a real ``<1,q; k,m | j,m+q>`` coefficient."""
    k = input_spin
    m = magnetic_index
    q = spin_one_index
    if output_spin == k + 1:
        if q == 1:
            square = (k + m + 1) * (k + m + 2) / (
                2 * (k + 1) * (2 * k + 1)
            )
        elif q == 0:
            square = (k - m + 1) * (k + m + 1) / (
                (k + 1) * (2 * k + 1)
            )
        else:
            square = (k - m + 1) * (k - m + 2) / (
                2 * (k + 1) * (2 * k + 1)
            )
        return math.sqrt(square)
    if output_spin == k:
        if q == 1:
            return -math.sqrt((k - m) * (k + m + 1) / (2 * k * (k + 1)))
        if q == 0:
            return m / math.sqrt(k * (k + 1))
        return math.sqrt((k + m) * (k - m + 1) / (2 * k * (k + 1)))
    if q == 1:
        square = (k - m) * (k - m - 1) / (2 * k * (2 * k + 1))
    elif q == 0:
        square = (k - m) * (k + m) / (k * (2 * k + 1))
    else:
        square = (k + m) * (k + m - 1) / (2 * k * (2 * k + 1))
    return (-1.0 if q == 0 else 1.0) * math.sqrt(square)


def _spin_one_coupling_isometry(input_spin: int, output_spin: int):
    input_dimension = 2 * input_spin + 1
    output_dimension = 2 * output_spin + 1
    coupling = np.zeros((3 * input_dimension, output_dimension))
    for spin_one_offset, spin_one_index in enumerate((-1, 0, 1)):
        for magnetic_offset, magnetic_index in enumerate(
            range(-input_spin, input_spin + 1)
        ):
            output_index = magnetic_index + spin_one_index
            if abs(output_index) <= output_spin:
                coupling[
                    spin_one_offset * input_dimension + magnetic_offset,
                    output_index + output_spin,
                ] = _spin_one_clebsch_gordan(
                    input_spin,
                    magnetic_index,
                    spin_one_index,
                    output_spin,
                )
    return coupling


def _peter_weyl_character_block(input_spin: int, output_spin: int):
    input_dimension = 2 * input_spin + 1
    output_dimension = 2 * output_spin + 1
    if output_spin not in range(abs(input_spin - 1), input_spin + 2):
        return np.zeros((output_dimension**2, input_dimension**2))
    coupling = _spin_one_coupling_isometry(input_spin, output_spin)
    block = np.zeros((output_dimension**2, input_dimension**2))
    normalization = math.sqrt(input_dimension / output_dimension)
    for column_index in range(input_dimension):
        for row_index in range(input_dimension):
            matrix_unit = np.zeros((input_dimension, input_dimension))
            matrix_unit[row_index, column_index] = 1.0
            image = (
                normalization
                * coupling.T
                @ np.kron(np.eye(3), matrix_unit)
                @ coupling
            )
            block[:, row_index + input_dimension * column_index] = image.reshape(
                -1,
                order="F",
            )
    return block


class GlobalSO3ReferenceRiskTest(unittest.TestCase):
    def test_so3_geometry(self):
        self.assertEqual(so3_chordal_frame_cost(0.0), 0.0)
        self.assertAlmostEqual(so3_chordal_frame_cost(math.pi), 1.0)
        self.assertEqual(so3_haar_ball_volume(0.0), 0.0)
        self.assertAlmostEqual(so3_haar_ball_volume(math.pi), 1.0)

    def test_gibbs_partition_matches_direct_sum(self):
        beta = 0.7
        direct = sum(
            (2 * spin + 1) ** 2 * math.exp(-beta * spin)
            for spin in range(200)
        )
        self.assertAlmostEqual(spin_gibbs_partition(beta), direct, places=12)
        self.assertAlmostEqual(log_spin_gibbs_partition(beta), math.log(direct), places=12)

    def test_gibbs_optimizer_matches_requested_mean(self):
        for mean_spin in (0.01, 0.5, 1.0, 10.0, 1.0e4):
            beta = optimal_spin_gibbs_dual_parameter(mean_spin)
            self.assertAlmostEqual(
                spin_gibbs_mean(beta),
                mean_spin,
                delta=1.0e-11 * max(1.0, mean_spin),
            )
            optimized = optimized_mean_spin_asymmetry_upper_bound(mean_spin)
            for factor in (0.8, 1.2):
                trial = mean_spin_asymmetry_upper_bound(
                    mean_spin,
                    dual_parameter=beta * factor,
                )
                self.assertLessEqual(optimized, trial + 1.0e-12)

    def test_gibbs_log_domain_extreme_mean(self):
        mean_spin = 1.0e200
        beta = optimal_spin_gibbs_dual_parameter(mean_spin)
        self.assertTrue(math.isfinite(beta))
        self.assertGreater(beta, 0.0)
        self.assertAlmostEqual(
            spin_gibbs_mean(beta) / mean_spin,
            1.0,
            places=12,
        )
        self.assertTrue(
            math.isfinite(optimized_mean_spin_asymmetry_upper_bound(mean_spin))
        )

    def test_risk_bound_and_casimir_conversion(self):
        self.assertAlmostEqual(
            asymmetry_orientation_risk_lower_bound(0.0),
            SO3_ASYMMETRY_RISK_CONSTANT,
        )
        self.assertEqual(mean_spin_upper_bound_from_mean_casimir(0.0), 0.0)
        self.assertAlmostEqual(mean_spin_upper_bound_from_mean_casimir(6.0), 2.0)
        self.assertGreater(mean_spin_orientation_risk_lower_bound(1.0), 0.0)
        self.assertGreater(so3_cost_partition_upper_bound(2.0), 0.0)
        self.assertAlmostEqual(
            mean_casimir_orientation_risk_lower_bound(0.0),
            1.0 / 8.0,
        )

    def test_fusion_matrix_and_sharp_cutoff_formula(self):
        for cutoff in range(12):
            matrix = np.array(fusion_score_matrix(cutoff), dtype=float)
            numerical = float(np.linalg.eigvalsh(matrix)[-1])
            self.assertAlmostEqual(
                numerical,
                fusion_score_maximum_eigenvalue(cutoff),
                places=12,
            )
            risk = (3.0 - numerical) / 4.0
            self.assertAlmostEqual(
                risk,
                hard_cutoff_orientation_risk_lower_bound(cutoff),
                places=12,
            )

    def test_projective_fusion_matrix_and_casimir_floor(self):
        self.assertAlmostEqual(
            projective_mean_casimir_orientation_risk_lower_bound(0.75),
            1.0 / 12.0,
        )
        for cutoff in range(12):
            matrix = np.array(projective_fusion_score_matrix(cutoff), dtype=float)
            numerical = float(np.linalg.eigvalsh(matrix)[-1])
            risk = (3.0 - numerical) / 4.0
            self.assertAlmostEqual(
                risk,
                projective_hard_cutoff_orientation_risk_lower_bound(cutoff),
                places=12,
            )

    def test_peter_weyl_character_blocks_are_hilbert_schmidt_contractions(self):
        tolerance = 2.0e-12
        self.assertEqual(np.count_nonzero(_peter_weyl_character_block(0, 0)), 0)

        for input_spin in range(7):
            input_dimension = 2 * input_spin + 1
            for output_spin in range(abs(input_spin - 1), input_spin + 2):
                output_dimension = 2 * output_spin + 1
                coupling = _spin_one_coupling_isometry(input_spin, output_spin)
                np.testing.assert_allclose(
                    coupling.T @ coupling,
                    np.eye(output_dimension),
                    atol=tolerance,
                )

                projector = (coupling @ coupling.T).reshape(
                    3,
                    input_dimension,
                    3,
                    input_dimension,
                )
                partial_trace = sum(
                    projector[index, :, index, :] for index in range(3)
                )
                np.testing.assert_allclose(
                    partial_trace,
                    (output_dimension / input_dimension) * np.eye(input_dimension),
                    atol=tolerance,
                )

                block = _peter_weyl_character_block(input_spin, output_spin)
                normalized_input_identity = np.eye(input_dimension).reshape(
                    -1,
                    order="F",
                ) / math.sqrt(input_dimension)
                normalized_output_identity = np.eye(output_dimension).reshape(
                    -1,
                    order="F",
                ) / math.sqrt(output_dimension)
                np.testing.assert_allclose(
                    block @ normalized_input_identity,
                    normalized_output_identity,
                    atol=tolerance,
                )

                singular_values = np.linalg.svd(block, compute_uv=False)
                self.assertLessEqual(float(singular_values[0]), 1.0 + tolerance)
                self.assertAlmostEqual(float(singular_values[0]), 1.0, places=12)
                np.testing.assert_allclose(
                    block,
                    _peter_weyl_character_block(output_spin, input_spin).T,
                    atol=tolerance,
                )

        representative_block = _peter_weyl_character_block(2, 3)
        amplified_block = np.kron(representative_block, np.eye(2))
        self.assertAlmostEqual(
            float(np.linalg.svd(amplified_block, compute_uv=False)[0]),
            1.0,
            places=12,
        )

    def test_discrete_hardy_step(self):
        vectors = (
            (1.0,),
            (0.2, 0.8),
            (0.1, 0.2, 0.3, 0.4),
            (1.0, 1.0, 1.0, 1.0, 1.0),
        )
        for vector in vectors:
            norm = math.sqrt(sum(value * value for value in vector))
            values = tuple(value / norm for value in vector) + (0.0,)
            gradient = sum(
                (left - right) ** 2
                for left, right in zip(values, values[1:])
            )
            casimir = sum(
                spin * (spin + 1) * value * value
                for spin, value in enumerate(values[:-1])
            )
            self.assertGreaterEqual(
                gradient + 1.0e-14,
                1.0 / (4.0 * casimir + 2.0),
            )

    def test_tail_quantile_transfer(self):
        cutoff = 8
        strict = hard_cutoff_orientation_risk_lower_bound(cutoff)
        self.assertEqual(
            tail_quantile_orientation_risk_lower_bound(cutoff, 0.0),
            strict,
        )
        self.assertEqual(
            tail_quantile_orientation_risk_lower_bound(cutoff, 1.0),
            0.0,
        )

    def test_exact_heat_diffusion_coherence_floor(self):
        casimir = 12.0
        initial = mean_casimir_orientation_risk_lower_bound(casimir)
        self.assertEqual(
            heat_diffused_orientation_risk_lower_bound(casimir, 0.0),
            initial,
        )
        values = tuple(
            heat_diffused_orientation_risk_lower_bound(casimir, time)
            for time in (0.0, 0.1, 1.0, 10.0)
        )
        self.assertTrue(all(right > left for left, right in zip(values, values[1:])))
        self.assertAlmostEqual(values[-1], 0.75, places=8)

        budget = 0.2
        ceiling = maximum_dimensionless_coherence_time(casimir, budget)
        self.assertAlmostEqual(
            heat_diffused_orientation_risk_lower_bound(casimir, ceiling),
            budget,
            places=12,
        )
        self.assertEqual(
            maximum_dimensionless_coherence_time(casimir, initial / 2.0),
            0.0,
        )
        self.assertEqual(
            maximum_dimensionless_coherence_time(casimir, 0.75),
            float("inf"),
        )

    def test_peter_weyl_tokens_respect_global_bounds(self):
        for cutoff in range(21):
            record = peter_weyl_token_risk_audit(cutoff)
            self.assertTrue(record["bounds_respected"])
            self.assertGreaterEqual(
                record["canonical_token_exact_chordal_orientation_risk"],
                record["asymmetry_risk_lower_bound"],
            )

    def test_compact_rotor_composition(self):
        record = compact_rotor_orientation_risk_record(
            observer_radius=1.0e-3,
            newton_constant=1.0e-12,
            inertia_coefficient=2.0 / 3.0,
            compactness_margin=0.5,
            maximum_excitation_fraction=0.25,
        )
        self.assertGreater(record["maximum_mean_casimir_Cbar"], 0.0)
        self.assertGreater(record["maximum_mean_spin_K"], 0.0)
        self.assertGreater(
            record["global_chordal_orientation_risk_lower_bound"],
            0.0,
        )

    def test_certificate(self):
        certificate = global_so3_reference_risk_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))

    def test_validation(self):
        with self.assertRaises(ValueError):
            so3_chordal_frame_cost(-1.0)
        with self.assertRaises(ValueError):
            so3_haar_ball_volume(math.pi + 0.1)
        with self.assertRaises(ValueError):
            spin_gibbs_partition(0.0)
        with self.assertRaises(ValueError):
            mean_spin_orientation_risk_lower_bound(-1.0)
        with self.assertRaises(ValueError):
            peter_weyl_token_risk_audit(True)
        with self.assertRaises(ValueError):
            tail_quantile_orientation_risk_lower_bound(2, 1.1)
        with self.assertRaises(ValueError):
            maximum_dimensionless_coherence_time(1.0, 1.1)
        with self.assertRaises(ValueError):
            projective_mean_casimir_orientation_risk_lower_bound(0.5)


if __name__ == "__main__":
    unittest.main()
