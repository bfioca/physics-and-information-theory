import ast
import inspect
import unittest
from fractions import Fraction

from qgtoy.validated_interval import (
    RationalInterval,
    RationalPolynomial,
    arctan_fraction_interval,
    atanh_fraction_interval,
    cos_center_lipschitz_interval,
    cos_fraction_interval,
    cos_interval,
    pi_machin_interval,
    sin_center_lipschitz_interval,
    sin_fraction_interval,
    sin_interval,
    sqrt_fraction_interval,
    validated_interval_foundation_certificate,
)
import qgtoy.validated_interval as validated_interval
from qgtoy.__main__ import build_parser


class ValidatedIntervalTest(unittest.TestCase):
    def test_exact_interval_arithmetic(self):
        first = RationalInterval(Fraction(-1, 3), Fraction(2, 5))
        second = RationalInterval(Fraction(1, 7), Fraction(3, 4))
        self.assertEqual(
            first + second,
            RationalInterval(Fraction(-4, 21), Fraction(23, 20)),
        )
        product = first * second
        for left in (first.lower, first.upper):
            for right in (second.lower, second.upper):
                self.assertTrue(product.contains(left * right))
        self.assertTrue(first.power(2).contains(0))
        negative_quotient = RationalInterval.point(1) / RationalInterval(
            Fraction(-3), Fraction(-2)
        )
        self.assertEqual(
            negative_quotient,
            RationalInterval(Fraction(-1, 2), Fraction(-1, 3)),
        )
        positive_quotient = RationalInterval.point(1) / RationalInterval(
            Fraction(2), Fraction(3)
        )
        self.assertEqual(
            positive_quotient,
            RationalInterval(Fraction(1, 3), Fraction(1, 2)),
        )
        self.assertEqual(
            first.scale(-2),
            RationalInterval(Fraction(-4, 5), Fraction(2, 3)),
        )
        self.assertEqual(
            RationalInterval(Fraction(-2), Fraction(-1)).power(3),
            RationalInterval(Fraction(-8), Fraction(-1)),
        )
        with self.assertRaises(ZeroDivisionError):
            second / first

    def test_rational_transcendental_refinement(self):
        self.assertTrue(
            pi_machin_interval(terms=64).is_subset_of(
                pi_machin_interval(terms=48)
            )
        )
        self.assertTrue(
            atanh_fraction_interval(Fraction(1, 5), terms=48).is_subset_of(
                atanh_fraction_interval(Fraction(1, 5), terms=32)
            )
        )
        sine = sin_fraction_interval(Fraction(1, 5), terms=24)
        cosine = cos_fraction_interval(Fraction(1, 5), terms=24)
        self.assertTrue((sine.power(2) + cosine.power(2)).contains(1))
        self.assertEqual(
            arctan_fraction_interval(Fraction(-1), terms=40),
            -arctan_fraction_interval(Fraction(1), terms=40),
        )
        self.assertEqual(
            atanh_fraction_interval(Fraction(-1, 5), terms=32),
            -atanh_fraction_interval(Fraction(1, 5), terms=32),
        )
        self.assertTrue(sin_fraction_interval(Fraction(-4), terms=40).width > 0)
        self.assertTrue(cos_fraction_interval(Fraction(4), terms=40).width > 0)

    def test_interval_trigonometric_enclosures(self):
        domain = RationalInterval(Fraction(-1, 5), Fraction(1, 4))
        sine = sin_interval(domain, terms=20)
        cosine = cos_interval(domain, terms=20)
        for point in (domain.lower, Fraction(0), domain.upper):
            self.assertTrue(
                sin_fraction_interval(point, terms=30).is_subset_of(sine)
            )
            self.assertTrue(
                cos_fraction_interval(point, terms=30).is_subset_of(cosine)
            )

    def test_center_lipschitz_trigonometric_enclosures(self):
        domain = RationalInterval(Fraction(299, 100), Fraction(301, 100))
        sine = sin_center_lipschitz_interval(domain, terms=30)
        cosine = cos_center_lipschitz_interval(domain, terms=30)
        for point in (domain.lower, domain.midpoint, domain.upper):
            self.assertTrue(
                sin_fraction_interval(point, terms=40).is_subset_of(sine)
            )
            self.assertTrue(
                cos_fraction_interval(point, terms=40).is_subset_of(cosine)
            )
        self.assertLess(sine.width, sin_interval(domain, terms=30).width)
        self.assertLess(cosine.width, cos_interval(domain, terms=30).width)

        point = RationalInterval.point(Fraction(3, 2))
        self.assertEqual(
            sin_center_lipschitz_interval(point, terms=20),
            sin_fraction_interval(point.midpoint, terms=20),
        )
        self.assertEqual(
            cos_center_lipschitz_interval(point, terms=20),
            cos_fraction_interval(point.midpoint, terms=20),
        )

        self.assertEqual(
            sin_center_lipschitz_interval(
                RationalInterval(Fraction(1), Fraction(2))
            ).upper,
            1,
        )
        self.assertEqual(
            cos_center_lipschitz_interval(
                RationalInterval(Fraction(-1), Fraction(1))
            ).upper,
            1,
        )
        wide = RationalInterval(Fraction(-2), Fraction(2))
        self.assertEqual(
            sin_center_lipschitz_interval(wide),
            RationalInterval(Fraction(-1), Fraction(1)),
        )
        self.assertEqual(
            cos_center_lipschitz_interval(wide),
            RationalInterval(Fraction(-1), Fraction(1)),
        )

    def test_exact_polynomial_operations(self):
        polynomial = RationalPolynomial(
            (Fraction(1), Fraction(-2), Fraction(3))
        )
        self.assertEqual(polynomial.degree, 2)
        self.assertEqual(
            polynomial.evaluate(Fraction(2)),
            RationalInterval.point(9),
        )
        self.assertEqual(
            polynomial.derivative().coefficients,
            (Fraction(-2), Fraction(6)),
        )
        self.assertEqual(
            polynomial.integral(4).derivative(),
            polynomial,
        )
        shifted = polynomial.shift(Fraction(1, 2))
        for point in (Fraction(-1), Fraction(0), Fraction(2)):
            self.assertEqual(
                shifted.evaluate(point),
                polynomial.evaluate(point + Fraction(1, 2)),
            )
        box = RationalInterval(Fraction(-1, 4), Fraction(1, 3))
        image = polynomial.evaluate(box)
        for point in (box.lower, Fraction(0), box.upper):
            self.assertTrue(image.contains(polynomial.evaluate(point).lower))

    def test_exact_and_irrational_square_roots(self):
        self.assertEqual(
            sqrt_fraction_interval(Fraction(9, 16)),
            RationalInterval.point(Fraction(3, 4)),
        )
        root_two = sqrt_fraction_interval(Fraction(2))
        self.assertTrue(root_two.power(2).contains(2))
        self.assertLess(root_two.width, Fraction(1, 2**150))

    def test_certificate_and_trusted_import_boundary(self):
        certificate = validated_interval_foundation_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["executable_checks"].values()))
        source = inspect.getsource(validated_interval)
        tree = ast.parse(source)
        self.assertFalse(
            any(
                isinstance(node, ast.Import)
                and any(alias.name == "math" for alias in node.names)
                for node in ast.walk(tree)
            )
        )
        imported_math_names = {
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "math"
            for alias in node.names
        }
        self.assertEqual(imported_math_names, {"factorial", "isqrt"})
        imported_modules = {
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }
        self.assertTrue(imported_modules.isdisjoint({"cmath", "numpy", "mpmath"}))
        args = build_parser().parse_args(["validated-interval-foundation"])
        self.assertEqual(args.func.__name__, "run_validated_interval_foundation")

    def test_validation(self):
        with self.assertRaises(ValueError):
            RationalInterval(Fraction(1), Fraction(0))
        with self.assertRaises(ValueError):
            atanh_fraction_interval(Fraction(1))
        with self.assertRaises(ValueError):
            sqrt_fraction_interval(Fraction(-1))
        with self.assertRaises(ValueError):
            sin_fraction_interval(Fraction(1), terms=0)
        with self.assertRaises(TypeError):
            sin_center_lipschitz_interval(Fraction(1))  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            cos_center_lipschitz_interval(RationalInterval.point(1), terms=0)


if __name__ == "__main__":
    unittest.main()
