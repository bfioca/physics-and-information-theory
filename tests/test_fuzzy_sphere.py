import unittest

from qgtoy.fuzzy_sphere import (
    commutator,
    fuzzy_heat_channel,
    fuzzy_harmonics,
    fuzzy_laplacian,
    fuzzy_sphere_level_record,
    fuzzy_sphere_regulator_certificate,
    harmonic_labels,
    hilbert_schmidt_inner,
    low_mode_projection,
    matrix_scale,
    normalized_trace,
    spin_generators,
)
from qgtoy.quantum_channel import identity_matrix, matmul, max_abs_difference


class FuzzySphereRegulatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = fuzzy_sphere_regulator_certificate(max_level=4)

    def test_certificate_passes_from_computed_residuals(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertEqual(
            self.certificate["result_type"],
            "exact_finite_su2_equivariant_fuzzy_sphere_regulator",
        )
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        for record in self.certificate["records"]:
            self.assertLessEqual(record["residuals"]["maximum"], 1e-9)
            self.assertTrue(record["heat_choi"]["psd"])

    def test_level_is_matrix_size_not_harmonic_hilbert_dimension(self):
        record = fuzzy_sphere_level_record(3)
        self.assertEqual(record["representation_hilbert_dimension"], 4)
        self.assertEqual(record["observable_algebra"], "M_4")
        self.assertEqual(record["observable_algebra_dimension"], 16)
        self.assertEqual(record["harmonic_mode_count"], 16)
        self.assertEqual(record["harmonic_multiplicities"], {"0": 1, "1": 3, "2": 5, "3": 7})

    def test_spin_half_generators_anchor(self):
        j_x, j_y, j_z = spin_generators(1)
        self.assertAlmostEqual(j_x[0][1].real, 0.5)
        self.assertAlmostEqual(j_y[0][1].imag, -0.5)
        self.assertAlmostEqual(j_z[0][0].real, 0.5)
        self.assertAlmostEqual(j_z[1][1].real, -0.5)
        self.assertLess(
            max_abs_difference(commutator(j_x, j_y), matrix_scale(j_z, 1j)),
            1e-12,
        )

    def test_harmonics_are_complete_orthonormal_operator_multipoles(self):
        level = 3
        harmonics = fuzzy_harmonics(level)
        self.assertEqual(tuple(harmonics), harmonic_labels(level))
        self.assertEqual(len(harmonics), (level + 1) ** 2)
        for left_label, left in harmonics.items():
            for right_label, right in harmonics.items():
                expected = 1.0 if left_label == right_label else 0.0
                self.assertAlmostEqual(
                    hilbert_schmidt_inner(left, right).real,
                    expected,
                    places=10,
                )
                self.assertAlmostEqual(
                    hilbert_schmidt_inner(left, right).imag,
                    0.0,
                    places=10,
                )

    def test_laplacian_spectrum_and_heat_action(self):
        level = 3
        heat_time = 0.15
        for (ell, _magnetic), harmonic in fuzzy_harmonics(level).items():
            self.assertLess(
                max_abs_difference(
                    fuzzy_laplacian(level, harmonic),
                    matrix_scale(harmonic, ell * (ell + 1)),
                ),
                1e-10,
            )
            heat = fuzzy_heat_channel(level, harmonic, heat_time=heat_time)
            self.assertAlmostEqual(
                hilbert_schmidt_inner(harmonic, heat).real,
                __import__("math").exp(-heat_time * ell * (ell + 1)),
                places=10,
            )

    def test_low_modes_form_operator_system_not_subalgebra(self):
        level = 2
        identity = identity_matrix(level + 1)
        self.assertLess(
            max_abs_difference(
                low_mode_projection(level, identity, max_mode=1),
                identity,
            ),
            1e-10,
        )
        mode = fuzzy_harmonics(level)[(1, 1)]
        product = matmul(mode, mode)
        projected = low_mode_projection(level, product, max_mode=1)
        self.assertGreater(max_abs_difference(product, projected), 0.1)

    def test_heat_preserves_identity_and_normalized_trace(self):
        level = 3
        identity = identity_matrix(level + 1)
        self.assertLess(
            max_abs_difference(
                fuzzy_heat_channel(level, identity, heat_time=0.2),
                identity,
            ),
            1e-10,
        )
        for harmonic in fuzzy_harmonics(level).values():
            self.assertAlmostEqual(
                normalized_trace(
                    fuzzy_heat_channel(level, harmonic, heat_time=0.2)
                ).real,
                normalized_trace(harmonic).real,
                places=10,
            )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            spin_generators(-1)
        with self.assertRaises(ValueError):
            fuzzy_sphere_regulator_certificate(max_level=0)
        with self.assertRaises(ValueError):
            fuzzy_sphere_regulator_certificate(tolerance=0.0)
        with self.assertRaises(ValueError):
            fuzzy_heat_channel(1, identity_matrix(2), heat_time=-0.1)
        with self.assertRaises(ValueError):
            harmonic_labels(2, max_mode=3)


if __name__ == "__main__":
    unittest.main()
