import unittest
from fractions import Fraction
from types import SimpleNamespace

from qgtoy.static_patch_skyrmion_tail import (
    skyrmion_sharp_form_factor_tail_envelope,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_spectral_ledger import (
    ValidatedSkyrmionDerivativeNormUpperBound,
    ValidatedSkyrmionSpectralInput,
    build_validated_skyrmion_spectral_ledger,
    validate_skyrmion_spectral_endpoint_ledger,
    validate_skyrmion_tail_endpoint_data,
)
from qgtoy.validated_skyrmion_bvp import (
    ValidatedSkyrmionNewtonPhysicalObservables,
)


class ValidatedSkyrmionSpectralLedgerTest(unittest.TestCase):
    def setUp(self):
        self.inertia = ValidatedSkyrmionSpectralInput(
            RationalInterval(Fraction(10), Fraction(11)),
            "closed Newton tube inertia cells",
            "fixture-au1",
        )
        self.wall_slope = ValidatedSkyrmionSpectralInput(
            RationalInterval(Fraction(-1, 10), Fraction(-1, 20)),
            "closed Newton tube wall cell",
            "fixture-au1",
        )
        self.endpoint = validate_skyrmion_spectral_endpoint_ledger(
            curvature=Fraction(1, 400),
            wall_radius=4,
            inertia=self.inertia,
            wall_slope=self.wall_slope,
        )

    def test_endpoint_ledger_is_directed_and_uses_optical_identity(self):
        endpoint = self.endpoint
        self.assertEqual(
            endpoint.root_curvature,
            RationalInterval.point(Fraction(1, 20)),
        )
        self.assertEqual(
            endpoint.radial_horizon_ratio,
            RationalInterval.point(Fraction(1, 5)),
        )
        self.assertEqual(
            endpoint.horizon_margin,
            RationalInterval.point(Fraction(24, 25)),
        )
        self.assertGreater(endpoint.optical_wall.lower, Fraction(1, 5))
        self.assertEqual(
            endpoint.form_factor_prefactor,
            RationalInterval(Fraction(1200, 11), Fraction(120)),
        )
        self.assertEqual(
            endpoint.wall_a_second_derivative,
            endpoint.wall_weight_second_derivative.scale(5),
        )
        self.assertGreater(endpoint.wall_weight_second_derivative.lower, 0)
        self.assertGreater(endpoint.leading_form_factor_tail_amplitude.lower, 0)

    def test_default_ledger_keeps_all_six_norms_and_au3_open(self):
        ledger = build_validated_skyrmion_spectral_ledger(self.endpoint)
        self.assertEqual(ledger.supplied_derivative_norm_count, 0)
        self.assertEqual(len(ledger.missing_derivative_norms), 6)
        self.assertEqual(
            ledger.au2_status,
            "open_external_derivative_norm_certificates_required",
        )
        self.assertEqual(ledger.au3_status, "open_finite_frequency_quadrature")
        self.assertIsNone(ledger.tail_envelope)
        record = ledger.to_record()
        self.assertIsNone(record["derivative_norm_bounds"]["M_0^A"])
        self.assertIn("does not establish", record["claim_boundary"])
        self.assertIn("Q0", record["claim_boundary"])

    def test_supplied_norms_reproduce_existing_tail_formula_outwardly(self):
        point_endpoint = validate_skyrmion_spectral_endpoint_ledger(
            curvature=Fraction(1, 4),
            wall_radius=1,
            inertia=ValidatedSkyrmionSpectralInput(
                RationalInterval.point(6),
                "synthetic exact inertia",
                "synthetic-au1",
            ),
            wall_slope=ValidatedSkyrmionSpectralInput(
                RationalInterval.point(Fraction(-1, 2)),
                "synthetic exact wall slope",
                "synthetic-au1",
            ),
        )
        a_values = (Fraction(5), Fraction(7), Fraction(11))
        w_values = (Fraction(13), Fraction(17), Fraction(19))
        a_norms = tuple(
            ValidatedSkyrmionDerivativeNormUpperBound(
                value,
                f"synthetic A norm {order}",
                "synthetic-au1",
            )
            for order, value in enumerate(a_values)
        )
        w_norms = tuple(
            ValidatedSkyrmionDerivativeNormUpperBound(
                value,
                f"synthetic W norm {order}",
                "synthetic-au1",
            )
            for order, value in enumerate(w_values)
        )
        ledger = build_validated_skyrmion_spectral_ledger(
            point_endpoint,
            a_third_derivative_l1=a_norms,
            w_third_derivative_l1=w_norms,
            tail_start=4,
            physical_radius=ValidatedSkyrmionSpectralInput(
                RationalInterval.point(2),
                "synthetic physical radius",
                "synthetic-scale",
            ),
        )
        self.assertEqual(ledger.supplied_derivative_norm_count, 6)
        self.assertEqual(ledger.missing_derivative_norms, ())
        self.assertIsNotNone(ledger.tail_envelope)
        self.assertEqual(
            ledger.au2_status,
            "conditional_tail_formula_evaluated_from_supplied_bounds",
        )
        tail = ledger.tail_envelope
        float_tail = skyrmion_sharp_form_factor_tail_envelope(
            prefactor=float(point_endpoint.form_factor_prefactor.lower),
            optical_wall=float(point_endpoint.optical_wall.midpoint),
            wall_weight_second=float(
                point_endpoint.wall_weight_second_derivative.midpoint
            ),
            a_third_derivative_l1=tuple(float(value) for value in a_values),
            w_third_derivative_l1=tuple(float(value) for value in w_values),
            tail_start=4.0,
            radius=2.0,
        )
        for interval, value in zip(
            tail.form_factor_derivative_coefficients,
            float_tail["form_factor_derivative_coefficients"],
        ):
            self.assertLessEqual(float(interval.lower), value)
            self.assertGreaterEqual(float(interval.upper), value)
        self.assertEqual(
            tail.squared_physical_h2_tail_bounds[2],
            tail.squared_dimensionless_h2_tail_bounds[2],
        )
        self.assertEqual(tail.physical_tail_start, Fraction(2))
        for bound in tail.squared_dimensionless_h2_tail_bounds:
            self.assertEqual(bound.lower, 0)
        self.assertEqual(
            tail.squared_physical_h2_tail_bounds[0].upper,
            tail.squared_dimensionless_h2_tail_bounds[0].upper / 16,
        )
        self.assertEqual(
            tail.squared_physical_h2_tail_bounds[1].upper,
            tail.squared_dimensionless_h2_tail_bounds[1].upper / 4,
        )

    def test_partial_norms_remain_open_and_preserve_provenance(self):
        first = ValidatedSkyrmionDerivativeNormUpperBound(
            Fraction(3, 2),
            "one certified cell sum",
            "fixture-au1",
        )
        ledger = build_validated_skyrmion_spectral_ledger(
            self.endpoint,
            a_third_derivative_l1=(first, None, None),
        )
        self.assertEqual(ledger.supplied_derivative_norm_count, 1)
        self.assertEqual(len(ledger.missing_derivative_norms), 5)
        self.assertIsNone(ledger.tail_envelope)
        record = ledger.to_record()
        self.assertEqual(
            record["derivative_norm_bounds"]["M_0^A"]["provenance"],
            "one certified cell sum",
        )

    def test_derivative_norms_must_match_endpoint_certificate(self):
        mismatched = ValidatedSkyrmionDerivativeNormUpperBound(
            Fraction(1),
            "different profile",
            "other-au1",
        )
        with self.assertRaisesRegex(ValueError, "endpoint certificate"):
            build_validated_skyrmion_spectral_ledger(
                self.endpoint,
                a_third_derivative_l1=(mismatched, None, None),
            )

    def test_validation_rejects_unusable_endpoint_inputs(self):
        with self.assertRaisesRegex(ValueError, "strictly negative"):
            validate_skyrmion_spectral_endpoint_ledger(
                curvature=Fraction(1, 400),
                wall_radius=4,
                inertia=self.inertia,
                wall_slope=ValidatedSkyrmionSpectralInput(
                    RationalInterval(Fraction(-1), Fraction(0)),
                    "non-strict wall slope",
                    "fixture-au1",
                ),
            )
        with self.assertRaisesRegex(ValueError, "strictly inside"):
            validate_skyrmion_spectral_endpoint_ledger(
                curvature=Fraction(1, 4),
                wall_radius=2,
                inertia=self.inertia,
                wall_slope=self.wall_slope,
            )
        with self.assertRaisesRegex(ValueError, "nonnegative"):
            ValidatedSkyrmionDerivativeNormUpperBound(
                Fraction(-1),
                "invalid negative norm",
                "fixture-au1",
            )
        with self.assertRaisesRegex(ValueError, "at least one"):
            build_validated_skyrmion_spectral_ledger(
                self.endpoint,
                tail_start=Fraction(1, 2),
            )

    def test_physical_adapter_preserves_closed_tube_provenance(self):
        physical = object.__new__(ValidatedSkyrmionNewtonPhysicalObservables)
        object.__setattr__(physical, "strict_monotonicity_verified", True)
        object.__setattr__(physical, "negative_wall_slope_verified", True)
        object.__setattr__(physical, "positive_finite_inertia_verified", True)
        object.__setattr__(physical, "inertia_enclosure", self.inertia.enclosure)
        object.__setattr__(
            physical,
            "wall_slope_enclosure",
            self.wall_slope.enclosure,
        )
        object.__setattr__(physical, "conclusion_scope", "closed AU.1 fixture")
        object.__setattr__(
            physical,
            "inertia_cells",
            (
                SimpleNamespace(
                    integral_enclosure=RationalInterval.point(Fraction(10))
                ),
            ),
        )
        object.__setattr__(
            physical,
            "origin_inertia_upper_bound",
            Fraction(1),
        )
        object.__setattr__(
            physical,
            "newton_tube",
            SimpleNamespace(
                self_map_verified=True,
                contraction_verified=True,
                curvature=Fraction(1, 400),
                wall_radius=Fraction(4),
                radius=Fraction(1, 250),
                omega=Fraction(3, 4),
                origin_cutoff=Fraction(1, 20),
                cells=(
                    SimpleNamespace(
                        tube_jet=SimpleNamespace(
                            derivative=self.wall_slope.enclosure
                        )
                    ),
                ),
            ),
        )

        endpoint = validate_skyrmion_tail_endpoint_data(physical)

        self.assertEqual(endpoint.newton_radius, Fraction(1, 250))
        self.assertEqual(endpoint.omega, Fraction(3, 4))
        self.assertEqual(endpoint.origin_cutoff, Fraction(1, 20))
        record = build_validated_skyrmion_spectral_ledger(endpoint).to_record()
        self.assertEqual(record["endpoint"]["newton_radius"], "1/250")

    def test_physical_adapter_rejects_incomplete_au1_checks(self):
        physical = object.__new__(ValidatedSkyrmionNewtonPhysicalObservables)
        object.__setattr__(physical, "strict_monotonicity_verified", False)
        object.__setattr__(physical, "negative_wall_slope_verified", True)
        object.__setattr__(physical, "positive_finite_inertia_verified", True)
        with self.assertRaisesRegex(ValueError, "all AU.1 physical checks"):
            validate_skyrmion_tail_endpoint_data(physical)


if __name__ == "__main__":
    unittest.main()
