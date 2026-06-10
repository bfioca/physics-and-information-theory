import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from qgtoy.validated_skyrmion_constraint import (
    build_validated_skyrmion_constraint_shape,
    validated_constraint_coupling_record,
)
from qgtoy.validated_skyrmion_sharp_profile import (
    reconstruct_validated_skyrmion_sharp_origin_family,
    reconstruct_validated_skyrmion_sharp_profile,
)


ROOT = Path(__file__).resolve().parents[1]

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


@pytest.fixture(scope="module")
def constraint_shape():
    archive = json.loads(
        (ROOT / "experiments/skyrmion_au2_global_tail_exact_certificate.json").read_text(
            encoding="ascii"
        )
    )
    snapshot = json.loads(
        (ROOT / "experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json").read_text(
            encoding="ascii"
        )
    )
    profile = reconstruct_validated_skyrmion_sharp_profile(
        archive,
        snapshot,
        subdivisions_per_parent=1,
    )
    origin = reconstruct_validated_skyrmion_sharp_origin_family(snapshot)
    return build_validated_skyrmion_constraint_shape(
        profile,
        origin,
        origin_subdivisions=16,
    )


def test_constraint_shape_is_positive_and_controls_full_bulk(constraint_shape) -> None:
    assert constraint_shape.fixed_background_exterior_shape_lower > 0
    assert (
        constraint_shape.sufficient_bulk_shape_upper
        >= constraint_shape.fixed_background_exterior_shape_lower
    )
    assert (
        constraint_shape.sufficient_test_source_global_shape_upper
        >= constraint_shape.sufficient_bulk_shape_upper
    )
    assert constraint_shape.maximum_upper_region in {
        "origin",
        "positive_radius",
        "exterior_wall",
    }


def test_constraint_coupling_window_uses_directed_shape(constraint_shape) -> None:
    record = validated_constraint_coupling_record(
        constraint_shape,
        control_budget=Fraction(1, 2),
        static_patch_radius_squared_over_newton=Fraction(10**6),
    )
    assert record["sufficient_bulk_coupling_squared_lower_bound_float"] > 0
    assert (
        record["sufficient_global_test_source_coupling_squared_lower_bound_float"]
        >= record["sufficient_bulk_coupling_squared_lower_bound_float"]
    )


@pytest.mark.parametrize("budget", [Fraction(0), Fraction(1)])
def test_constraint_coupling_window_rejects_invalid_budget(
    constraint_shape,
    budget,
) -> None:
    with pytest.raises(ValueError):
        validated_constraint_coupling_record(
            constraint_shape,
            control_budget=budget,
            static_patch_radius_squared_over_newton=Fraction(10**6),
        )
