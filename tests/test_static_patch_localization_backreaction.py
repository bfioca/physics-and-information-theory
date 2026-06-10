import unittest
from math import asin, cos, sin

from qgtoy.__main__ import build_parser
from qgtoy.static_patch_localization_backreaction import (
    localization_backreaction_record,
    maximum_spin_with_leading_localization_window,
    minimum_compact_spherical_top_radius,
    proper_static_slice_angular_distance,
    static_patch_localization_backreaction_certificate,
)


class StaticPatchLocalizationBackreactionTest(unittest.TestCase):
    def test_compact_top_radius_inverts_casimir_bound(self):
        spin = 7
        radius = minimum_compact_spherical_top_radius(
            spin,
            newton_constant=1.0e-6,
        )
        cap = (
            (2.0 / 3.0)
            * 0.5**2
            * 0.25
            * radius**4
            / (2.0 * 1.0e-12 * 1.25**2)
        )
        self.assertAlmostEqual(cap, spin * (spin + 1))

    def test_static_slice_angular_distance(self):
        self.assertAlmostEqual(
            proper_static_slice_angular_distance(
                0.2,
                horizon_distance=0.1,
                radius=2.0,
            ),
            4.0 * asin(cos(0.05) * sin(0.1)),
        )

    def test_default_leading_and_design_crossovers(self):
        self.assertEqual(
            maximum_spin_with_leading_localization_window(branch="nonoverlap"),
            30,
        )
        self.assertEqual(
            maximum_spin_with_leading_localization_window(branch="generic"),
            6,
        )
        self.assertEqual(
            maximum_spin_with_leading_localization_window(branch="dipole_cancelled"),
            30,
        )

    def test_window_closes_between_adjacent_spins(self):
        at_cutoff = localization_backreaction_record(30)
        after_cutoff = localization_backreaction_record(31)
        self.assertTrue(at_cutoff["leading_nonoverlap_compactness_window_exists"])
        self.assertFalse(after_cutoff["leading_nonoverlap_compactness_window_exists"])

    def test_radius_ratios_decrease_through_default_range(self):
        records = [localization_backreaction_record(spin) for spin in range(1, 129)]
        for key in (
            "leading_nonoverlap_radius_ratio_upper_to_lower",
            "generic_radius_ratio_upper_to_lower",
            "dipole_cancelled_radius_ratio_upper_to_lower",
        ):
            values = [record[key] for record in records]
            self.assertTrue(
                all(right < left for left, right in zip(values, values[1:]))
            )

    def test_binary_crossovers_match_exhaustive_search(self):
        for newton_constant in (1.0e-8, 1.0e-10, 1.0e-12):
            for branch, key in (
                ("nonoverlap", "leading_nonoverlap_compactness_window_exists"),
                ("generic", "generic_certified_window_exists"),
                ("dipole_cancelled", "dipole_cancelled_certified_window_exists"),
            ):
                exhaustive = max(
                    (
                        spin
                        for spin in range(1, 513)
                        if localization_backreaction_record(
                            spin,
                            newton_constant=newton_constant,
                        )[key]
                    ),
                    default=0,
                )
                self.assertEqual(
                    maximum_spin_with_leading_localization_window(
                        branch=branch,
                        newton_constant=newton_constant,
                        maximum_search_spin=512,
                    ),
                    exhaustive,
                )

    def test_certificate(self):
        certificate = static_patch_localization_backreaction_certificate()
        self.assertEqual(certificate["status"], "pass")
        self.assertTrue(all(certificate["certified_claims"].values()))
        self.assertEqual(
            certificate["illustrative_leading_nonoverlap_crossover_dimension"],
            61,
        )

    def test_certificate_handles_no_spin_one_window(self):
        certificate = static_patch_localization_backreaction_certificate(
            newton_constant=1.0,
        )
        self.assertEqual(certificate["status"], "pass")
        self.assertEqual(
            certificate["illustrative_leading_nonoverlap_crossover_spin"],
            0,
        )

    def test_cli_defaults(self):
        args = build_parser().parse_args(["static-patch-localization-backreaction"])
        self.assertEqual(args.maximum_spin, 4096)
        self.assertEqual(args.radius, 1.0)
        self.assertEqual(args.newton_constant, 1.0e-12)

    def test_validation(self):
        with self.assertRaises(ValueError):
            minimum_compact_spherical_top_radius(1, newton_constant=-1.0)
        with self.assertRaises(ValueError):
            maximum_spin_with_leading_localization_window(branch="unknown")
        with self.assertRaises(ValueError):
            static_patch_localization_backreaction_certificate(maximum_spin=16)


if __name__ == "__main__":
    unittest.main()
