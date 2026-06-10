import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from qgtoy.validated_skyrmion_radial_gap import (
    validate_skyrmion_fixed_wall_radial_gap,
    validate_skyrmion_regular_origin_barta,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def authenticated_radial_gap():
    au2 = json.loads(
        (ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json")
        .read_text(encoding="ascii")
    )
    snapshot = json.loads(
        (ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json")
        .read_text(encoding="ascii")
    )
    tube = reconstruct_validated_skyrmion_sharp_profile(
        au2,
        snapshot,
        subdivisions_per_parent=1,
    )
    origin = reconstruct_validated_skyrmion_sharp_origin_family(snapshot)
    result = validate_skyrmion_fixed_wall_radial_gap(tube, origin)
    return tube, origin, result


def test_authenticated_exact_solution_full_radial_gap(authenticated_radial_gap):
    _, _, result = authenticated_radial_gap
    assert result.static_form_gap == 1
    assert result.kinetic_weight_upper_bound == 25
    assert result.dimensionless_frequency_squared_lower_bound == Fraction(1, 25)
    assert len(result.positive_radius.cells) == 109
    assert result.positive_radius.maximum_depth_used == 5
    assert result.positive_radius.recomputed_lower_bound > Fraction(103, 100)
    assert result.origin.quotient.lower > 36
    assert result.origin.regular_mode_boundary_term_vanishes
    assert result.fixed_wall_dirichlet_boundary_term_vanishes


def test_adaptive_leaves_cover_positive_radius_without_gaps(authenticated_radial_gap):
    tube, _, result = authenticated_radial_gap
    cells = result.positive_radius.cells
    assert cells[0].jet.radius.lower == tube.origin_cutoff
    assert cells[-1].jet.radius.upper == tube.wall_radius
    assert all(
        left.jet.radius.upper == right.jet.radius.lower
        for left, right in zip(cells, cells[1:])
    )
    assert all(cell.quotient.lower >= 1 for cell in cells)


def test_origin_provenance_mismatch_is_rejected(authenticated_radial_gap):
    tube, origin, _ = authenticated_radial_gap
    with pytest.raises(ValueError, match="do not match"):
        validate_skyrmion_fixed_wall_radial_gap(
            tube,
            replace(origin, curvature=Fraction(1, 200)),
        )


def test_origin_barta_rejects_unclosed_family(authenticated_radial_gap):
    _, origin, _ = authenticated_radial_gap
    with pytest.raises(ValueError, match="closed contraction"):
        validate_skyrmion_regular_origin_barta(
            replace(origin, contraction_bound=Fraction(1)),
        )
