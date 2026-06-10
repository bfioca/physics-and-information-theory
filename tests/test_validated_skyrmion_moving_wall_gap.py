import json
import hashlib
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from qgtoy.validated_skyrmion_moving_wall_gap import (
    skyrmion_young_laplace_coefficients,
    validate_skyrmion_moving_wall_radial_gap,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT / "experiments/skyrmion_moving_wall_radial_gap_exact_certificate.json"
)
CERTIFICATE_SHA256 = (
    "2bb48f770504ab5a0a0f9b3139b881877a414ddb9b8c19cd34c81bfd26b42686"
)


@pytest.fixture(scope="module")
def authenticated_moving_wall_gap():
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
    result = validate_skyrmion_moving_wall_radial_gap(tube, origin)
    return tube, origin, result


def test_authenticated_moving_wall_radial_gap(authenticated_moving_wall_gap):
    _, _, result = authenticated_moving_wall_gap
    assert result.witness_center == Fraction(9, 4)
    assert result.witness_width_squared == 8
    assert result.bulk_form_lower_bound == Fraction(1, 100)
    assert result.bulk_kinetic_weight_upper_bound == 25
    assert result.boundary_form_lower_bound == Fraction(39878, 69325)
    assert result.boundary_kinetic_weight == Fraction(800, 47)
    assert result.dimensionless_frequency_squared_lower_bound == Fraction(
        1,
        2500,
    )
    assert result.positive_radius.recomputed_lower_bound > Fraction(12, 1000)
    assert result.origin.quotient.lower > 37
    assert result.origin.regular_boundary_term_vanishes


def test_moving_wall_barta_leaves_cover_domain(authenticated_moving_wall_gap):
    tube, _, result = authenticated_moving_wall_gap
    cells = result.positive_radius.cells
    assert cells[0].jet.radius.lower == tube.origin_cutoff
    assert cells[-1].jet.radius.upper == tube.wall_radius
    assert all(
        left.jet.radius.upper == right.jet.radius.lower
        for left, right in zip(cells, cells[1:])
    )
    assert all(cell.quotient.lower >= Fraction(1, 100) for cell in cells)


def test_young_laplace_coefficients_are_exact():
    result = skyrmion_young_laplace_coefficients(
        wall_radius=Fraction(4),
        curvature=Fraction(1, 400),
    )
    assert result.compactness == Fraction(1, 25)
    assert result.lapse_at_wall == Fraction(24, 25)
    assert result.normalized_wall_mass_per_slope_squared == Fraction(800, 47)
    assert (
        result.normalized_boundary_stiffness_per_slope_squared
        == Fraction(6386, 1175)
    )
    assert result.jacobi_principal_at_wall == Fraction(384, 25)


def test_old_witness_is_rejected_by_moving_boundary(
    authenticated_moving_wall_gap,
):
    tube, origin, _ = authenticated_moving_wall_gap
    with pytest.raises(ValueError, match="nonpositive boundary"):
        validate_skyrmion_moving_wall_radial_gap(
            tube,
            origin,
            center=Fraction(33, 16),
            width_squared=Fraction(4),
            declared_bulk_lower_bound=Fraction(1),
            declared_frequency_squared_lower_bound=Fraction(1, 10000),
        )


def test_origin_provenance_mismatch_is_rejected(
    authenticated_moving_wall_gap,
):
    tube, origin, _ = authenticated_moving_wall_gap
    with pytest.raises(ValueError, match="do not match"):
        validate_skyrmion_moving_wall_radial_gap(
            tube,
            replace(origin, curvature=Fraction(1, 200)),
        )


def test_authenticated_artifact_hash_and_outputs():
    assert hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest() == CERTIFICATE_SHA256
    record = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    outputs = record["exact_outputs"]
    assert outputs["dimensionless_frequency_lower_bound"] == "1/50"
    assert outputs["boundary_form_lower_bound"] == "39878/69325"
    assert outputs["positive_radius_leaf_count"] == 95
    assert outputs["positive_radius_maximum_depth_used"] == 5


def test_authenticated_artifact_source_hashes_are_current():
    record = json.loads(CERTIFICATE.read_text(encoding="ascii"))
    for relative, expected in record["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
