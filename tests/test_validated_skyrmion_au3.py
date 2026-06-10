import copy
import hashlib
import json
import unittest
from fractions import Fraction
from pathlib import Path

from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_au3 import (
    build_validated_skyrmion_au3_certificate,
    build_validated_skyrmion_au3_from_au2_record,
    exact_fraction_from_text,
)
from qgtoy.validated_skyrmion_spectral_ledger import (
    ValidatedSkyrmionDerivativeNormUpperBound,
    ValidatedSkyrmionSpectralInput,
    build_validated_skyrmion_spectral_ledger,
    validate_skyrmion_spectral_endpoint_ledger,
)


ROOT = Path(__file__).resolve().parents[1]
AU2_ARCHIVE = ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json"
AU3_ARCHIVE = (
    ROOT / "experiments/skyrmion_au3_global_sobolev_exact_certificate.json"
)


class ValidatedSkyrmionAU3Test(unittest.TestCase):
    def synthetic_ledger(self, *, radius: Fraction = Fraction(1)):
        certificate_id = "synthetic-au3"
        endpoint = validate_skyrmion_spectral_endpoint_ledger(
            curvature=Fraction(1, 4),
            wall_radius=1,
            inertia=ValidatedSkyrmionSpectralInput(
                RationalInterval.point(6),
                "synthetic inertia",
                certificate_id,
            ),
            wall_slope=ValidatedSkyrmionSpectralInput(
                RationalInterval.point(Fraction(-1, 2)),
                "synthetic wall slope",
                certificate_id,
            ),
        )
        a_norms = tuple(
            ValidatedSkyrmionDerivativeNormUpperBound(
                value,
                f"synthetic A norm {order}",
                certificate_id,
            )
            for order, value in enumerate((Fraction(5), Fraction(7), Fraction(11)))
        )
        w_norms = tuple(
            ValidatedSkyrmionDerivativeNormUpperBound(
                value,
                f"synthetic W norm {order}",
                certificate_id,
            )
            for order, value in enumerate((Fraction(13), Fraction(17), Fraction(19)))
        )
        return build_validated_skyrmion_spectral_ledger(
            endpoint,
            a_third_derivative_l1=a_norms,
            w_third_derivative_l1=w_norms,
            tail_start=1,
            physical_radius=ValidatedSkyrmionSpectralInput(
                RationalInterval.point(radius),
                "synthetic physical scale",
                "synthetic-scale",
            ),
        )

    def test_exact_low_band_tail_join_and_sobolev_moments(self):
        certificate = build_validated_skyrmion_au3_certificate(
            self.synthetic_ledger()
        )
        for low, tail, global_bound, norm in zip(
            certificate.finite_band_squared_h2_bounds,
            certificate.tail_squared_h2_bounds,
            certificate.global_squared_h2_bounds,
            certificate.q_norm_upper_bounds,
        ):
            self.assertEqual(global_bound, low + tail)
            self.assertGreaterEqual(norm**2, global_bound)
        pi_upper = Fraction(22, 7)
        self.assertGreaterEqual(
            certificate.jump_l1_upper_bound**2,
            2
            * pi_upper
            * certificate.q_norm_upper_bounds[0]
            * certificate.q_norm_upper_bounds[1],
        )
        self.assertGreaterEqual(
            certificate.jump_first_moment_upper_bound**2,
            2
            * pi_upper
            * certificate.q_norm_upper_bounds[1]
            * certificate.q_norm_upper_bounds[2],
        )
        self.assertEqual(
            certificate.stationary_residual_quadratic_coefficient,
            288
            * certificate.jump_l1_upper_bound
            * certificate.jump_first_moment_upper_bound,
        )
        record = certificate.to_record()
        self.assertEqual(
            record["au3_status"],
            "conditional_directed_global_upper_certificate",
        )
        self.assertIsNone(record["authenticated_input_sha256"])
        self.assertIn("not a sharp", record["claim_boundary"])

    def test_physical_radius_scaling_is_applied_before_tail_join(self):
        unit = build_validated_skyrmion_au3_certificate(self.synthetic_ledger())
        doubled = build_validated_skyrmion_au3_certificate(
            self.synthetic_ledger(radius=Fraction(2))
        )
        for order in range(3):
            expected_scale = Fraction(2) ** (2 * order - 4)
            self.assertEqual(
                doubled.finite_band_squared_h2_bounds[order],
                unit.finite_band_squared_h2_bounds[order] * expected_scale,
            )
            self.assertEqual(
                doubled.tail_squared_h2_bounds[order],
                unit.tail_squared_h2_bounds[order] * expected_scale,
            )

    def test_incomplete_ledger_or_invalid_frequency_grid_is_rejected(self):
        complete = self.synthetic_ledger()
        incomplete = build_validated_skyrmion_spectral_ledger(complete.endpoint)
        with self.assertRaises(ValueError):
            build_validated_skyrmion_au3_certificate(incomplete)
        with self.assertRaises(ValueError):
            build_validated_skyrmion_au3_certificate(
                complete,
                band_split=3,
                frequency_step=Fraction(2, 3),
            )
        with self.assertRaises(ValueError):
            build_validated_skyrmion_au3_certificate(
                complete,
                authenticated_input_sha256="not-a-sha",
            )

    def test_unbounded_fraction_parser(self):
        numerator = "9" * 5_000
        value = exact_fraction_from_text(numerator + "/7")
        self.assertEqual(value.denominator, 7)
        self.assertEqual(value.numerator % 10_000, 9_999)

    @classmethod
    def setUpClass(cls):
        cls.au2_archive = json.loads(AU2_ARCHIVE.read_text(encoding="ascii"))
        cls.au2_record = cls.au2_archive["exact_outputs"][
            "au2_global_derivative_norms_and_tail"
        ]["spectral_ledger"]
        cls.au2_sha = hashlib.sha256(AU2_ARCHIVE.read_bytes()).hexdigest()
        cls.certificate = build_validated_skyrmion_au3_from_au2_record(
            cls.au2_record,
            authenticated_input_sha256=cls.au2_sha,
        )

    def test_default_exact_archive_is_recomputed_and_pinned(self):
        q0, q1, q2 = self.certificate.q_norm_upper_bounds
        self.assertAlmostEqual(float(q0), 4_296.7909080828495, places=9)
        self.assertAlmostEqual(float(q1), 10_146.945245040379, places=9)
        self.assertAlmostEqual(float(q2), 35_213.76234103636, places=9)
        self.assertAlmostEqual(
            float(self.certificate.jump_l1_upper_bound),
            16_554.53883053991,
            places=9,
        )
        self.assertAlmostEqual(
            float(self.certificate.jump_first_moment_upper_bound),
            47_391.58033605288,
            places=9,
        )
        archive = json.loads(AU3_ARCHIVE.read_text(encoding="ascii"))
        normalized = json.loads(json.dumps(self.certificate.to_record()))
        self.assertEqual(archive["exact_outputs"], normalized)
        self.assertEqual(
            archive["input_archive_sha256"],
            self.au2_sha,
        )
        self.assertEqual(
            archive["exact_outputs"]["au3_status"],
            "complete_directed_global_upper_certificate",
        )
        for relative, expected in archive["source_sha256"].items():
            actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, relative)

    def test_archive_tampering_is_detected(self):
        tampered = copy.deepcopy(self.au2_record)
        tampered["tail_envelope"]["squared_physical_h2_tail_bounds"][0][
            "upper"
        ] = "1"
        with self.assertRaisesRegex(ValueError, "inconsistent|tail mismatch"):
            build_validated_skyrmion_au3_from_au2_record(tampered)


if __name__ == "__main__":
    unittest.main()
