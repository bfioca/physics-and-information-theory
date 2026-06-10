from functools import cache
from fractions import Fraction

import pytest

from qgtoy.validated_centrifugal_conormal_remainder import (
    validate_centrifugal_conormal_remainder,
)
from qgtoy.validated_centrifugal_origin_transfer import (
    formal_affine_endpoint_transfer,
)
from qgtoy.validated_centrifugal_physical_origin_transfer import (
    ValidatedPhysicalOriginTransfer,
    validate_centrifugal_physical_origin_transfer,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_quintic_family import (
    validate_skyrmion_origin_quintic_family,
)


AUTHENTICATED_SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
)


@cache
def _certificate() -> ValidatedPhysicalOriginTransfer:
    profile = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )
    remainder = validate_centrifugal_conormal_remainder(profile)
    return validate_centrifugal_physical_origin_transfer(profile, remainder)


def _is_subset(left: RationalInterval, right: RationalInterval) -> bool:
    return left.is_subset_of(right)


def test_two_cells_cover_the_authenticated_slope_box() -> None:
    result = _certificate()
    assert result.shooting_slopes == AUTHENTICATED_SLOPES
    assert result.cutoff == Fraction(1, 16)
    assert len(result.cells) == 2
    assert result.cells[0].shooting_slopes.lower == AUTHENTICATED_SLOPES.lower
    assert result.cells[-1].shooting_slopes.upper == AUTHENTICATED_SLOPES.upper
    assert (
        result.cells[0].shooting_slopes.upper == result.cells[1].shooting_slopes.lower
    )
    assert result.is_finite_cell_enclosure
    assert "absolute value" in result.affine_combination_rule


def test_all_three_formal_endpoint_columns_are_contained() -> None:
    result = _certificate()
    for cell in result.cells:
        formal = formal_affine_endpoint_transfer(
            cell.shooting_slopes, cutoff=result.cutoff
        )
        formal_fields = (*formal.homogeneous_field_columns, formal.forced_field)
        formal_derivatives = (
            *formal.homogeneous_derivative_columns,
            formal.forced_derivative,
        )
        for branch, field, derivative in zip(
            cell.branches, formal_fields, formal_derivatives, strict=True
        ):
            assert all(
                _is_subset(center, tube)
                for center, tube in zip(field, branch.field, strict=True)
            )
            assert all(
                _is_subset(center, tube)
                for center, tube in zip(derivative, branch.derivative, strict=True)
            )
            assert branch.formal_field_center == field
            assert branch.formal_derivative_center == derivative


def test_physical_tubes_are_finite_and_useful() -> None:
    result = _certificate()
    assert result.branch_order == (
        "linear_homogeneous",
        "cubic_homogeneous",
        "forced_particular",
    )
    for cell in result.cells:
        for branch in cell.branches:
            assert all(value.lower <= value.upper for value in branch.field)
            assert all(value.lower <= value.upper for value in branch.derivative)
            assert max(value.width for value in branch.field) < Fraction(3, 50)
            assert max(value.width for value in branch.derivative) < Fraction(3, 2)


def test_validator_rejects_invalid_inputs() -> None:
    with pytest.raises(TypeError, match="profile_family"):
        validate_centrifugal_physical_origin_transfer(object())  # type: ignore[arg-type]

    profile = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )
    with pytest.raises(TypeError, match="conormal_remainder"):
        validate_centrifugal_physical_origin_transfer(
            profile,
            object(),  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="kernel_terms"):
        validate_centrifugal_physical_origin_transfer(profile, kernel_terms=2)
