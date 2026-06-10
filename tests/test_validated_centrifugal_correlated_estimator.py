import hashlib
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import qgtoy.validated_centrifugal_correlated_estimator as estimator_module
from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    rational_response_trial_pair_from_record,
)
from qgtoy.validated_centrifugal_correlated_estimator import (
    _integrate_centered_density,
    correlated_positive_radius_corrected_estimator,
)
from qgtoy.validated_centrifugal_liouville_taylor import _CenteredTaylorModel
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_sharp_profile import (
    reconstruct_validated_skyrmion_sharp_profile,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "experiments/validated_centrifugal_correlated_estimator.json"


def test_centered_integral_beats_range_times_width_on_exact_polynomial() -> None:
    density = _CenteredTaylorModel.from_polynomial(
        RationalPolynomial((Fraction(3), Fraction(2), Fraction(1))),
        degree_limit=4,
        rounding_denominator=10**12,
    )
    result = _integrate_centered_density(
        density, physical_half_width=Fraction(1, 4)
    )

    assert result.integral == RationalInterval.point(Fraction(5, 3))
    assert result.naive_range_times_width == RationalInterval(
        Fraction(1, 2), Fraction(3)
    )
    assert result.integral.is_subset_of(result.naive_range_times_width)
    assert result.center_density == RationalInterval.point(Fraction(3))


def test_nonunit_profile_mass_reaches_form_and_master_kernels(monkeypatch) -> None:
    au2 = json.loads(
        (ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json").read_text()
    )
    sharp = json.loads(
        (ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json").read_text()
    )
    archive = json.loads(
        (ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json").read_text()
    )
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=1
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])
    nonunit_mass = Fraction(9, 4)
    profile = replace(
        profile,
        pion_mass_squared=nonunit_mass,
        cells=profile.cells[:1],
    )
    primal = replace(pair.primal, positive_radius_cells=pair.primal.positive_radius_cells[:1])
    adjoint = replace(
        pair.adjoint,
        positive_radius_cells=pair.adjoint.positive_radius_cells[:1],
    )
    seen: list[RationalInterval] = []
    original_form = estimator_module.regular_conormal_blocks_from_kernels
    original_master = estimator_module.centrifugal_weak_master_load_affine_kernel

    def capture_form(**kwargs):
        seen.append(kwargs["pion_mass_squared"].range())
        return original_form(**kwargs)

    def capture_master(**kwargs):
        seen.append(kwargs["pion_mass_squared"].range())
        return original_master(**kwargs)

    monkeypatch.setattr(
        estimator_module, "regular_conormal_blocks_from_kernels", capture_form
    )
    monkeypatch.setattr(
        estimator_module,
        "centrifugal_weak_master_load_affine_kernel",
        capture_master,
    )
    # This synthetic one-cell slice ends before the physical wall.  The full
    # authenticated test below exercises the trial validation and wall trace.
    monkeypatch.setattr(type(primal), "validate", lambda self: None)

    result = correlated_positive_radius_corrected_estimator(
        profile,
        primal,
        adjoint,
    )

    assert result.authenticated_positive_radius_cell_count == 1
    assert seen == [
        RationalInterval.point(nonunit_mass),
        RationalInterval.point(nonunit_mass),
    ]


def test_authenticated_outer_estimator_preserves_signed_correlations() -> None:
    au2 = json.loads(
        (ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json").read_text()
    )
    sharp = json.loads(
        (ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json").read_text()
    )
    archive = json.loads(
        (ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json").read_text()
    )
    profile = reconstruct_validated_skyrmion_sharp_profile(
        au2, sharp, subdivisions_per_parent=1
    )
    pair = rational_response_trial_pair_from_record(archive["trial_archive"])

    result = correlated_positive_radius_corrected_estimator(
        profile, pair.primal, pair.adjoint
    )

    assert result.authenticated_positive_radius_cell_count == 43
    assert result.positive_radius_domain == RationalInterval(Fraction(1, 16), 4)
    assert result.radius_partition == tuple(cell.radius for cell in profile.cells)
    assert result.profile_primal_adjoint_partitions_match
    assert result.profile_green_trials_form_and_loads_share_coordinate
    assert result.centered_symmetric_integration_used
    assert not result.origin_included
    assert not result.wall_included
    assert not result.zero_exclusion_claimed
    assert all(cell.shared_centered_coordinate for cell in result.cells)
    assert all(
        cell.correlated_total_integral.is_subset_of(cell.naive_total_integral)
        for cell in result.cells
    )
    assert result.correlated_estimator_total.is_subset_of(
        result.naive_estimator_total
    )
    assert result.correlated_estimator_total.is_subset_of(
        result.component_sum_total
    )


def test_correlated_estimator_artifact_is_source_bound_and_partial() -> None:
    payload = ARTIFACT.read_bytes()
    record = json.loads(payload)

    assert record["status"] == "pass"
    assert all(record["certified_claims"].values())
    total = record["signed_outer_totals"]["joint_correlated_integral"]
    assert total["lower_float"] < total["upper_float"] < 0
    assert record["representation_contract"]["compatible_wall_completion"] == (
        "y_f(a)*(gamma_B-k*z_f(a))"
    )
    assert "full-response zero exclusion are not claimed" in record["claim_boundary"]
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    assert hashlib.sha256(payload).hexdigest() == (
        "078e596f394aabcee86a8f8d89d6282ffef37342b9fa9a1a5f155577b3cb8c9a"
    )
