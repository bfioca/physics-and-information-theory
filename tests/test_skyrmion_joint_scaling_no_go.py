import unittest
from math import sqrt

from qgtoy.__main__ import build_parser
from qgtoy.skyrmion_joint_scaling_no_go import (
    admissible_skyrme_coupling_squared_interval,
    compactness_slow_rotation_product,
    maximum_admissible_odd_reference_cutoff,
    maximum_admissible_spin,
    skyrmion_compactness,
    skyrmion_joint_scaling_no_go_certificate,
    skyrmion_slow_rotation_parameter,
)


class SkyrmionJointScalingNoGoTest(unittest.TestCase):
    def setUp(self):
        self.parameters = {
            "mass_constant": 48.95760324794553,
            "inertia_constant": 34.26620155247604,
            "wall_radius": 4.0,
            "curvature": 0.0025,
            "static_patch_radius": 1.0,
            "newton_constant": 1.0e-6,
        }

    def test_product_is_independent_of_skyrme_coupling(self):
        spin = 80.0
        exact = compactness_slow_rotation_product(spin, **self.parameters)
        products = []
        for coupling in (0.1, 0.2, 0.4):
            compactness = skyrmion_compactness(
                coupling,
                mass_constant=self.parameters["mass_constant"],
                wall_radius=self.parameters["wall_radius"],
                curvature=self.parameters["curvature"],
                static_patch_radius=self.parameters["static_patch_radius"],
                newton_constant=self.parameters["newton_constant"],
            )
            slow = skyrmion_slow_rotation_parameter(
                spin,
                coupling,
                inertia_constant=self.parameters["inertia_constant"],
            )
            products.append(compactness * slow)
        for product in products:
            self.assertAlmostEqual(product, exact, places=14)

    def test_maximum_spin_is_sharp_for_integer_window(self):
        maximum = maximum_admissible_spin(
            maximum_compactness=0.5,
            maximum_slow_rotation=0.1,
            **self.parameters,
        )
        self.assertGreater(maximum, 0)
        self.assertIsNotNone(
            admissible_skyrme_coupling_squared_interval(
                float(maximum),
                maximum_compactness=0.5,
                maximum_slow_rotation=0.1,
                **self.parameters,
            )
        )
        self.assertIsNone(
            admissible_skyrme_coupling_squared_interval(
                float(maximum + 1),
                maximum_compactness=0.5,
                maximum_slow_rotation=0.1,
                **self.parameters,
            )
        )

    def test_fermionic_reference_window_uses_half_integer_spins(self):
        cutoff = maximum_admissible_odd_reference_cutoff(
            maximum_compactness=0.5,
            maximum_slow_rotation=0.1,
            **self.parameters,
        )
        self.assertEqual(cutoff, 173)
        physical_spin = cutoff + 0.5
        self.assertIsNotNone(
            admissible_skyrme_coupling_squared_interval(
                physical_spin,
                maximum_compactness=0.5,
                maximum_slow_rotation=0.1,
                **self.parameters,
            )
        )
        self.assertIsNone(
            admissible_skyrme_coupling_squared_interval(
                physical_spin + 1.0,
                maximum_compactness=0.5,
                maximum_slow_rotation=0.1,
                **self.parameters,
            )
        )

    def test_exact_casimir_thresholds_are_included(self):
        common = {
            "maximum_compactness": 1.0,
            "mass_constant": 1.0,
            "inertia_constant": 1.0,
            "wall_radius": 1.0,
            "curvature": 1.0,
            "static_patch_radius": 1.0,
        }
        odd_casimir_root = sqrt(0.5 * 1.5)
        self.assertEqual(
            maximum_admissible_odd_reference_cutoff(
                maximum_slow_rotation=odd_casimir_root,
                newton_constant=0.5,
                **common,
            ),
            0,
        )
        interval = admissible_skyrme_coupling_squared_interval(
            0.5,
            maximum_slow_rotation=odd_casimir_root,
            newton_constant=0.5,
            **common,
        )
        self.assertIsNotNone(interval)
        self.assertEqual(interval[0], interval[1])

        self.assertEqual(
            maximum_admissible_spin(
                maximum_slow_rotation=sqrt(3.0 * 4.0),
                newton_constant=0.5,
                **common,
            ),
            3,
        )

    def test_near_boundary_inverted_interval_is_rejected(self):
        interval = admissible_skyrme_coupling_squared_interval(
            0.5,
            maximum_compactness=1.0,
            maximum_slow_rotation=sqrt(3.0) / 2.0,
            mass_constant=1.0,
            inertia_constant=1.0,
            wall_radius=1.0,
            curvature=1.0,
            static_patch_radius=1.0,
            newton_constant=(1.0 + 5.0e-13) / 2.0,
        )
        self.assertIsNone(interval)

    def test_certificate(self):
        certificate = skyrmion_joint_scaling_no_go_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertEqual(
            certificate["maximum_admissible_odd_reference_cutoff_J"], 173
        )
        self.assertEqual(
            certificate["maximum_admissible_physical_spin_K"], 173.5
        )
        self.assertIsNone(certificate["next_spin_interval"])

    def test_cli_defaults(self):
        args = build_parser().parse_args(["skyrmion-joint-scaling-no-go"])
        self.assertEqual(args.static_patch_radius, 1.0)
        self.assertEqual(args.newton_constant, 1.0e-6)
        self.assertEqual(args.maximum_compactness, 0.5)
        self.assertEqual(args.maximum_slow_rotation, 0.1)

    def test_validation(self):
        with self.assertRaises(ValueError):
            skyrmion_compactness(
                0.0,
                mass_constant=1.0,
                wall_radius=1.0,
                curvature=0.1,
                static_patch_radius=1.0,
                newton_constant=0.1,
            )


if __name__ == "__main__":
    unittest.main()
