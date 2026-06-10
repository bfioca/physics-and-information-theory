import unittest

from qgtoy.finite_clock_crossed_product import (
    finite_clock_crossed_product_no_go_certificate,
    finite_clock_crossed_product_record,
    regulator_clock_record,
)


class FiniteClockCrossedProductTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certificate = finite_clock_crossed_product_no_go_certificate(max_level=8)

    def test_certificate_passes_with_order_of_limits_boundary(self):
        self.assertEqual(self.certificate["status"], "pass")
        self.assertTrue(all(self.certificate["certified_claims"].values()))
        self.assertIn("infinite local-QFT", self.certificate["claim_boundary"])

    def test_inner_cyclic_crossed_product_wedderburn_form(self):
        record = finite_clock_crossed_product_record(5, 7)
        self.assertEqual(record["wedderburn_block_count"], 7)
        self.assertEqual(record["wedderburn_block_sizes"], (5,) * 7)
        self.assertEqual(record["crossed_product_vector_space_dimension"], 175)
        self.assertEqual(record["center_dimension"], 7)
        self.assertFalse(record["is_factor"])
        self.assertEqual(record["finite_von_neumann_type"], "Type I finite")

    def test_trivial_clock_returns_matrix_factor_but_not_typeii(self):
        record = finite_clock_crossed_product_record(4, 1)
        self.assertTrue(record["is_factor"])
        self.assertFalse(record["typeii_at_finite_cutoff"])
        self.assertEqual(record["center_dimension"], 1)

    def test_regulator_dimensions_grow_without_changing_finite_type(self):
        records = tuple(regulator_clock_record(level) for level in range(1, 7))
        self.assertTrue(
            all(
                right["crossed_product_vector_space_dimension"]
                > left["crossed_product_vector_space_dimension"]
                for left, right in zip(records, records[1:])
            )
        )
        self.assertTrue(
            all(record["finite_von_neumann_type"] == "Type I finite" for record in records)
        )

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            finite_clock_crossed_product_record(0, 2)
        with self.assertRaises(ValueError):
            finite_clock_crossed_product_record(2, 0)
        with self.assertRaises(ValueError):
            regulator_clock_record(0)
        with self.assertRaises(ValueError):
            finite_clock_crossed_product_no_go_certificate(max_level=0)


if __name__ == "__main__":
    unittest.main()
