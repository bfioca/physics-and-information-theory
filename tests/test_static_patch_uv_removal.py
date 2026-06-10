import unittest

from qgtoy.static_patch_phase_space import (
    CompactPolynomialBump,
    PhaseSpaceTest,
    unitary_sine_transform,
)
from qgtoy.static_patch_uv_removal import (
    covariance_uv_tail_bound,
    covariance_zero_momentum_limit,
    phase_space_decay_constants,
    phase_space_ir_constants,
    polynomial_bump_derivative_l1_bound,
    polynomial_bump_distributional_derivative_tv_bound,
    sine_transform_decay_constant,
    sine_transform_ir_constant,
    static_patch_uv_removal_certificate,
    symplectic_uv_tail_bound,
    weyl_characteristic_uv_tail_bound,
    wightman_uv_tail_bound,
)


class StaticPatchUvRemovalTest(unittest.TestCase):
    def setUp(self):
        self.left = CompactPolynomialBump(0.25, 0.75, 3)
        self.right = CompactPolynomialBump(1.0, 1.5, 3)
        self.first = PhaseSpaceTest(field_bump=self.left, momentum_bump=self.right)
        self.second = PhaseSpaceTest(
            field_bump=self.right,
            momentum_bump=self.left,
            field_scale=0.7,
            momentum_scale=-0.4,
        )

    def test_derivative_and_transform_decay_bounds(self):
        derivative_bound = polynomial_bump_derivative_l1_bound(self.left, 3)
        self.assertGreater(derivative_bound, 0.0)
        distributional_bound = polynomial_bump_distributional_derivative_tv_bound(
            self.left
        )
        self.assertGreater(distributional_bound, 0.0)
        decay_constant = sine_transform_decay_constant(self.left, 4)
        for momentum in (4.0, 8.0, 16.0, 32.0, 64.0):
            self.assertLessEqual(
                abs(unitary_sine_transform(momentum, self.left)),
                decay_constant / momentum**4 * (1.0 + 1e-10),
            )

    def test_explicit_infrared_bound_and_zero_limit(self):
        ir_constant = sine_transform_ir_constant(self.left)
        for momentum in (1e-4, 1e-3, 1e-2, 0.1):
            self.assertLessEqual(
                abs(unitary_sine_transform(momentum, self.left)),
                ir_constant * momentum * (1.0 + 1e-10),
            )
        field_ir, momentum_ir = phase_space_ir_constants(self.first)
        self.assertGreater(field_ir, 0.0)
        self.assertGreater(momentum_ir, 0.0)
        self.assertGreater(
            covariance_zero_momentum_limit(self.first, self.second, radius=1.0),
            0.0,
        )

    def test_phase_space_decay_constants_include_scales(self):
        first_constants = phase_space_decay_constants(self.first, 4)
        second_constants = phase_space_decay_constants(self.second, 4)
        self.assertGreater(first_constants[0], second_constants[0])
        self.assertGreater(first_constants[1], second_constants[1])

    def test_tail_bounds_have_expected_power_laws(self):
        bounds = []
        for cutoff in (8.0, 16.0, 32.0):
            bounds.append(
                (
                    symplectic_uv_tail_bound(
                        self.first,
                        self.second,
                        momentum_cutoff=cutoff,
                    ),
                    covariance_uv_tail_bound(
                        self.first,
                        self.second,
                        radius=1.0,
                        momentum_cutoff=cutoff,
                    ),
                    wightman_uv_tail_bound(
                        self.first,
                        self.second,
                        radius=1.0,
                        momentum_cutoff=cutoff,
                    ),
                )
            )
        self.assertAlmostEqual(bounds[0][0] / bounds[1][0], 2.0**7)
        self.assertGreater(bounds[0][1] / bounds[1][1], 2.0**5.9)
        self.assertGreater(bounds[0][2] / bounds[1][2], 2.0**5.8)

    def test_weyl_characteristic_bound_is_half_variance_bound(self):
        covariance = covariance_uv_tail_bound(
            self.first,
            self.first,
            radius=1.0,
            momentum_cutoff=12.0,
        )
        characteristic = weyl_characteristic_uv_tail_bound(
            self.first,
            radius=1.0,
            momentum_cutoff=12.0,
        )
        self.assertAlmostEqual(characteristic, 0.5 * covariance)

    def test_certificate_passes_and_restores_equal_time_locality(self):
        certificate = static_patch_uv_removal_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertIn("disjoint compact supports", certificate["locality_result"])
        self.assertIn("faster than any inverse power", certificate["smooth_test_extension"])
        self.assertIn("removable", certificate["infrared_result"])
        fractions = tuple(
            sample["imaginary_time_fraction_of_beta"]
            for sample in certificate["records"][0][
                "truncated_wightman_closed_strip_samples"
            ]
        )
        self.assertEqual(fractions, (0.0, 0.37, 1.0))

    def test_validation(self):
        with self.assertRaises(ValueError):
            polynomial_bump_derivative_l1_bound(self.left, 4)
        with self.assertRaises(ValueError):
            covariance_uv_tail_bound(
                self.first,
                self.second,
                radius=1.0,
                momentum_cutoff=8.0,
                derivative_order=1,
            )
        with self.assertRaises(ValueError):
            static_patch_uv_removal_certificate(steps=7)
        self.assertGreater(
            covariance_uv_tail_bound(
                self.first,
                self.second,
                radius=1e-20,
                momentum_cutoff=1.0,
            ),
            0.0,
        )


if __name__ == "__main__":
    unittest.main()
