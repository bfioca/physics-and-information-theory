import unittest
from fractions import Fraction

from qgtoy.skyrmion_global_bvp_certificate_generator import (
    subdivide_explicit_mesh_nodes,
)


class SkyrmionMeshRefinementTest(unittest.TestCase):
    def test_selected_cells_receive_exact_equal_width_subdivisions(self):
        nodes = (
            Fraction(1, 16),
            Fraction(2),
            Fraction(35, 16),
            Fraction(4),
        )

        refined = subdivide_explicit_mesh_nodes(nodes, {1: 2, 2: 3})

        self.assertEqual(
            refined,
            (
                Fraction(1, 16),
                Fraction(2),
                Fraction(67, 32),
                Fraction(35, 16),
                Fraction(67, 24),
                Fraction(163, 48),
                Fraction(4),
            ),
        )

    def test_empty_refinement_preserves_the_mesh(self):
        nodes = (Fraction(1, 16), Fraction(2), Fraction(4))
        self.assertEqual(subdivide_explicit_mesh_nodes(nodes, {}), nodes)
        self.assertEqual(
            subdivide_explicit_mesh_nodes(nodes, {0: 1, 1: 1}),
            nodes,
        )

    def test_invalid_refinement_controls_are_rejected(self):
        nodes = (Fraction(1, 16), Fraction(2), Fraction(4))
        invalid = (
            ({True: 2}, TypeError),
            ({2: 2}, ValueError),
            ({0: True}, TypeError),
            ({0: 0}, ValueError),
            ({0: -1}, ValueError),
        )
        for factors, error in invalid:
            with self.subTest(factors=factors):
                with self.assertRaises(error):
                    subdivide_explicit_mesh_nodes(nodes, factors)

        with self.assertRaises(TypeError):
            subdivide_explicit_mesh_nodes(nodes, [(0, 2)])
        with self.assertRaises(ValueError):
            subdivide_explicit_mesh_nodes(
                (Fraction(1, 16), Fraction(1, 16)),
                {},
            )


if __name__ == "__main__":
    unittest.main()
