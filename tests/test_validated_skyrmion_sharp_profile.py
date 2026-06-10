import sys
from fractions import Fraction

import pytest

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from qgtoy.validated_interval import RationalInterval, RationalPolynomial
from qgtoy.validated_skyrmion_bvp import SkyrmionPolynomialCell
from qgtoy.validated_skyrmion_origin import (
    validate_skyrmion_origin_family,
    validate_skyrmion_origin_quintic_patch,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    _endpoint_family_jet,
    build_validated_skyrmion_sharp_measure,
    build_validated_skyrmion_sharp_worldtube_constants,
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)


def _interval(value: RationalInterval) -> dict[str, str]:
    return {"lower": str(value.lower), "upper": str(value.upper)}


def _synthetic_records() -> tuple[dict[str, object], dict[str, object]]:
    cutoff = Fraction(1, 16)
    wall = Fraction(4)
    curvature = Fraction(1, 400)
    slope = Fraction(1462763601523, 925827031517)
    slope_family = RationalInterval(
        slope - Fraction(1, 10**6),
        slope + Fraction(1, 10**6),
    )
    profile = SkyrmionPolynomialCell(
        RationalInterval(cutoff, wall),
        RationalPolynomial((Fraction(3), Fraction(-3))),
    )
    origin = validate_skyrmion_origin_quintic_patch(
        slope,
        cutoff=cutoff,
        curvature=curvature,
    )
    left_correction = (
        origin.profile_at_cutoff
        - profile.profile_polynomial.evaluate(Fraction(0))
    )
    right_correction = -profile.profile_polynomial.evaluate(Fraction(1)).lower
    family = _endpoint_family_jet(
        profile,
        Fraction(0),
        Fraction(1),
        domain_left=cutoff,
        domain_right=wall,
        left_value_correction=left_correction,
        right_value_correction=right_correction,
    )
    profile_radius = Fraction(1, 10**6)
    derivative_radius = Fraction(1, 10**6)
    au2 = {
        "parameters": {
            "curvature": str(curvature),
            "pion_mass_squared": "1",
            "origin_cutoff": str(cutoff),
            "wall_radius": str(wall),
            "shooting_slope": str(slope),
        },
        "profile_cells": [
            {
                "radius": _interval(profile.radius),
                "coefficients": [
                    str(value) for value in profile.profile_polynomial.coefficients
                ],
            }
        ],
    }
    snapshot = {
        "certificate_id": "synthetic-sharp-profile",
        "sharp_profile_recipe": {
            "curvature": str(curvature),
            "pion_mass_squared": "1",
            "origin_cutoff": str(cutoff),
            "wall_radius": str(wall),
            "left_value_correction": _interval(left_correction),
            "right_value_correction": str(right_correction),
            "omega": "1",
            "newton_radius": "1/1000000",
            "rounding_denominator": "1000000",
            "profile_second_sensitivity_upper_bound": "0",
            "shooting_slope_interval": _interval(slope_family),
            "origin_remainder_radius": "13/10",
            "cells": [
                {
                    "source_cell_index": 0,
                    "radius": _interval(profile.radius),
                    "endpoint_family_profile": _interval(family.profile),
                    "endpoint_family_derivative": _interval(family.derivative),
                    "endpoint_family_second_derivative": _interval(
                        family.second_derivative
                    ),
                    "profile_error_radius": str(profile_radius),
                    "derivative_error_radius": str(derivative_radius),
                    "second_derivative_error_radius": "0",
                    "local_graph_c0_upper_bound": "1",
                    "local_graph_c1_upper_bound": "1/2",
                    "local_graph_c2_upper_bound": "0",
                    "local_auxiliary_c0_upper_bound": "0",
                    "local_auxiliary_c1_upper_bound": "0",
                    "local_auxiliary_c2_upper_bound": "0",
                    "archived_tube_profile": _interval(
                        family.profile
                        + RationalInterval(-profile_radius, profile_radius)
                    ),
                    "archived_tube_derivative": _interval(
                        family.derivative
                        + RationalInterval(-derivative_radius, derivative_radius)
                    ),
                    "archived_tube_second_derivative": _interval(
                        family.second_derivative
                    ),
                }
            ],
        },
    }
    return au2, snapshot


def test_sharp_profile_replay_refines_authenticated_parent() -> None:
    au2, snapshot = _synthetic_records()
    replay = reconstruct_validated_skyrmion_sharp_profile(
        au2,
        snapshot,
        subdivisions_per_parent=4,
    )

    assert len(replay.parents) == 1
    assert len(replay.cells) == 4
    assert replay.parents[0].profile_error_radius == Fraction(1, 10**6)
    assert replay.parents[0].derivative_error_radius == Fraction(1, 10**6)
    assert replay.parents[0].second_derivative_error_radius == 0
    assert replay.cells[0].radius.lower == replay.origin_cutoff
    assert replay.cells[-1].radius.upper == replay.wall_radius
    assert all(
        cell.solution_profile.is_subset_of(
            replay.parents[cell.parent_cell_index].archived_tube_jet.profile
        )
        for cell in replay.cells
    )
    assert replay.cells[0].solution_profile.width < (
        replay.parents[0].archived_tube_jet.profile.width
    )


def test_endpoint_corrections_have_independent_values_and_derivative_sign() -> None:
    cell = SkyrmionPolynomialCell(
        RationalInterval(Fraction(1), Fraction(3)),
        RationalPolynomial((Fraction(2), Fraction(1))),
    )
    left = Fraction(1, 3)
    right = Fraction(-1, 5)
    left_jet = _endpoint_family_jet(
        cell,
        Fraction(0),
        Fraction(0),
        domain_left=Fraction(1),
        domain_right=Fraction(3),
        left_value_correction=RationalInterval.point(left),
        right_value_correction=right,
    )
    right_jet = _endpoint_family_jet(
        cell,
        Fraction(1),
        Fraction(1),
        domain_left=Fraction(1),
        domain_right=Fraction(3),
        left_value_correction=RationalInterval.point(left),
        right_value_correction=right,
    )

    assert left_jet.profile == RationalInterval.point(Fraction(2) + left)
    assert right_jet.profile == RationalInterval.point(Fraction(3) + right)
    expected_derivative = Fraction(1, 2) + (right - left) / 2
    assert left_jet.derivative == RationalInterval.point(expected_derivative)
    assert right_jet.derivative == RationalInterval.point(expected_derivative)


def test_sharp_profile_replay_rejects_tampered_parent() -> None:
    au2, snapshot = _synthetic_records()
    snapshot["sharp_profile_recipe"]["cells"][0]["archived_tube_profile"] = {
        "lower": "0",
        "upper": "1",
    }

    with pytest.raises(ValueError, match="escaped its parent"):
        reconstruct_validated_skyrmion_sharp_profile(au2, snapshot)


def test_sharp_profile_replay_rejects_tampered_newton_radius() -> None:
    au2, snapshot = _synthetic_records()
    snapshot["sharp_profile_recipe"]["cells"][0]["profile_error_radius"] = "0"

    with pytest.raises(ValueError, match="profile_error_radius does not replay"):
        reconstruct_validated_skyrmion_sharp_profile(au2, snapshot)


def test_sharp_profile_replay_binds_slope_interval_to_newton_tube() -> None:
    au2, snapshot = _synthetic_records()
    slope = Fraction(1462763601523, 925827031517)
    snapshot["sharp_profile_recipe"]["shooting_slope_interval"] = _interval(
        RationalInterval(slope - Fraction(1, 500), slope + Fraction(1, 500))
    )

    with pytest.raises(ValueError, match="shooting interval"):
        reconstruct_validated_skyrmion_sharp_profile(au2, snapshot)


def test_sharp_profile_replay_binds_pion_mass_to_au2() -> None:
    au2, snapshot = _synthetic_records()
    snapshot["sharp_profile_recipe"]["pion_mass_squared"] = "2"

    with pytest.raises(ValueError, match="pion_mass_squared"):
        reconstruct_validated_skyrmion_sharp_profile(au2, snapshot)


def test_sharp_profile_builds_origin_regular_positive_measure() -> None:
    au2, snapshot = _synthetic_records()
    replay = reconstruct_validated_skyrmion_sharp_profile(
        au2,
        snapshot,
        subdivisions_per_parent=4,
    )
    slope = Fraction(1462763601523, 925827031517)
    origin = validate_skyrmion_origin_family(
        RationalInterval(slope - Fraction(1, 10**6), slope + Fraction(1, 10**6)),
        cutoff=Fraction(1, 16),
        curvature=Fraction(1, 400),
    )
    snapshot["sharp_profile_recipe"]["origin_family"] = {
        "shooting_slopes": _interval(origin.shooting_slopes),
        "cutoff": str(origin.cutoff),
        "pion_mass_squared": str(origin.pion_mass_squared),
        "curvature": str(origin.curvature),
        "cubic_coefficient": _interval(origin.cubic_coefficient),
        "remainder_radius": str(origin.remainder_radius),
        "residual_bound": str(origin.residual_bound),
        "contraction_bound": str(origin.contraction_bound),
        "volterra_denominator_lower_bound": str(
            origin.volterra_denominator_lower_bound
        ),
        "profile_at_cutoff": _interval(origin.profile_at_cutoff),
        "derivative_at_cutoff": _interval(origin.derivative_at_cutoff),
    }
    assert reconstruct_validated_skyrmion_sharp_origin_family(snapshot) == origin
    measure = build_validated_skyrmion_sharp_measure(
        replay,
        origin,
        origin_subdivisions=4,
    )

    assert len(measure.origin_cells) == 4
    assert len(measure.positive_radius_cells) == 4
    assert measure.inertia.lower > 0
    assert measure.origin_cells[0].radius.lower == 0
    assert measure.origin_cells[-1].radius.upper == replay.origin_cutoff
    assert all(cell.density.lower >= 0 for cell in measure.origin_cells)
    constants = build_validated_skyrmion_sharp_worldtube_constants(
        replay,
        origin,
        origin_subdivisions=4,
    )
    assert constants.interior_mass.lower > 0
    assert constants.shell_mass.lower >= 0
    assert constants.total_mass == constants.interior_mass + constants.shell_mass
    assert constants.inertia == measure.inertia

    shifted = validate_skyrmion_origin_family(
        RationalInterval(
            slope - Fraction(2, 10**6),
            slope,
        ),
        cutoff=Fraction(1, 16),
        curvature=Fraction(1, 400),
    )
    with pytest.raises(ValueError, match="shooting branch"):
        build_validated_skyrmion_sharp_measure(replay, shifted)


@pytest.mark.parametrize("subdivisions", [0, -1])
def test_sharp_profile_replay_validates_subdivision_count(subdivisions: int) -> None:
    au2, snapshot = _synthetic_records()
    with pytest.raises(ValueError, match="positive integer"):
        reconstruct_validated_skyrmion_sharp_profile(
            au2,
            snapshot,
            subdivisions_per_parent=subdivisions,
        )
