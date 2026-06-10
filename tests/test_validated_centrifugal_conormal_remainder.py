from functools import cache
from fractions import Fraction

import pytest

from qgtoy.validated_centrifugal_conormal_remainder import (
    ValidatedConormalRemainder,
    validate_centrifugal_conormal_remainder,
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
def _certificate() -> ValidatedConormalRemainder:
    profile = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )
    return validate_centrifugal_conormal_remainder(profile)


def test_authenticated_two_cell_remainder_certificate_closes() -> None:
    result = _certificate()
    assert result.shooting_slopes == AUTHENTICATED_SLOPES
    assert result.cutoff == Fraction(1, 16)
    assert len(result.cells) == 2
    assert result.maximum_green_majorant < Fraction(51, 100)
    assert result.maximum_coefficient_variation_bound < Fraction(3, 20)
    assert result.maximum_contraction_bound < Fraction(3, 40)
    assert result.branch_order == (
        "linear_homogeneous",
        "cubic_homogeneous",
        "forced_particular",
    )
    assert max(
        value
        for branch in result.maximum_branch_endpoint_state_error_bounds
        for value in branch
    ) < Fraction(1, 10_000)
    assert result.closes


def test_all_affine_columns_obey_exact_cellwise_radii_inequality() -> None:
    result = _certificate()
    for cell in result.cells:
        assert cell.contraction_bound == (
            cell.green_majorant * cell.coefficient_variation_bound
        )
        for residual, radius in zip(
            cell.branch_residual_bounds,
            cell.branch_remainder_radii,
            strict=True,
        ):
            assert residual > 0
            assert radius > 0
            assert (
                cell.green_majorant * residual + cell.contraction_bound * radius
                <= radius
            )
        for radius, component_errors in zip(
            cell.branch_remainder_radii,
            cell.branch_endpoint_state_error_bounds,
            strict=True,
        ):
            assert component_errors == tuple(
                result.cutoff**6 * radius * weight for weight in result.state_weights
            )


def test_cells_cover_the_authenticated_slope_box() -> None:
    cells = _certificate().cells
    assert cells[0].shooting_slopes.lower == AUTHENTICATED_SLOPES.lower
    assert cells[-1].shooting_slopes.upper == AUTHENTICATED_SLOPES.upper
    assert cells[0].shooting_slopes.upper == cells[1].shooting_slopes.lower


def test_remainder_validator_rejects_invalid_inputs() -> None:
    with pytest.raises(TypeError, match="profile_family"):
        validate_centrifugal_conormal_remainder(object())  # type: ignore[arg-type]

    profile = validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )
    with pytest.raises(ValueError, match="state_weights"):
        validate_centrifugal_conormal_remainder(
            profile,
            state_weights=(Fraction(1), Fraction(1), Fraction(1), Fraction(0)),
        )
