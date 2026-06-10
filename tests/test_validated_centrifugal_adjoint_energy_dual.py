from fractions import Fraction

import pytest

from qgtoy.validated_centrifugal_adjoint_bulk_load import (
    ValidatedWeakAdjointResidualCell,
)
from qgtoy.validated_centrifugal_adjoint_energy_dual import (
    certify_positive_radius_wall_adjoint_dual_bound,
    combine_loaded_origin_squared_dual_upper,
    validated_adjoint_energy_dual_cell,
)
from qgtoy.validated_centrifugal_response_residual import (
    ValidatedConormalStrongCell,
)
from qgtoy.validated_interval import RationalInterval


def _synthetic_cell(
    left: Fraction, right: Fraction
) -> tuple[ValidatedWeakAdjointResidualCell, ValidatedConormalStrongCell]:
    point = RationalInterval.point
    zero = point(0)
    radius = RationalInterval(left, right)
    # P=x^2 I is enclosed by the exact interval x^2 I.  M=0 gives T=I/2.
    principal = ((radius.power(2), zero), (zero, radius.power(2)))
    zero_matrix = ((zero, zero), (zero, zero))
    residual = ValidatedWeakAdjointResidualCell(
        radius=radius,
        test_value_coefficient=(point(2), point(-1)),
        test_derivative_coefficient=(point(3), point(0)),
    )
    coefficients = ValidatedConormalStrongCell(
        radius=radius,
        coordinate=zero_matrix,
        mixed=zero_matrix,
        principal=principal,
        mixed_derivative=zero_matrix,
        principal_derivative=zero_matrix,
        strong_source=(zero, zero),
    )
    return residual, coefficients


def test_completed_square_lift_keeps_derivative_term_in_v_star() -> None:
    residual, coefficients = _synthetic_cell(Fraction(1), Fraction(2))
    cell = validated_adjoint_energy_dual_cell(
        residual,
        coefficients,
        principal_lower_bound=Fraction(1, 5),
        completed_potential_lower_bound=Fraction(1, 4),
    )
    assert cell.completed_multiplier[0][0] == RationalInterval.point(
        Fraction(1, 2)
    )
    assert cell.completed_derivative_coefficient[0] == RationalInterval(
        Fraction(3, 2), Fraction(3)
    )
    assert cell.derivative_squared_dual_upper == 45
    assert cell.value_squared_dual_upper > 0
    assert cell.squared_dual_upper == (
        cell.derivative_squared_dual_upper + cell.value_squared_dual_upper
    )


def test_partial_composer_names_origin_omission_and_wall_quadrature() -> None:
    first = validated_adjoint_energy_dual_cell(
        *_synthetic_cell(Fraction(1), Fraction(2)),
        principal_lower_bound=Fraction(1, 5),
        completed_potential_lower_bound=Fraction(1, 4),
    )
    second = validated_adjoint_energy_dual_cell(
        *_synthetic_cell(Fraction(2), Fraction(3)),
        principal_lower_bound=Fraction(1, 5),
        completed_potential_lower_bound=Fraction(1, 4),
    )
    partial = certify_positive_radius_wall_adjoint_dual_bound(
        (first, second),
        wall_residual=RationalInterval(Fraction(-1, 10), Fraction(1, 5)),
        wall_trace_margin_lower_bound=Fraction(1, 2),
        principal_lower_bound=Fraction(1, 5),
        completed_potential_lower_bound=Fraction(1, 4),
    )
    assert partial.wall_squared_upper == Fraction(2, 25)
    assert not partial.regular_origin_master_load_included
    assert not partial.full_loaded_adjoint_residual_certified
    combined = combine_loaded_origin_squared_dual_upper(
        partial, loaded_origin_l2_squared_upper=Fraction(1, 100)
    )
    assert combined > partial.partial_energy_dual_upper


def test_cell_rejects_uncertified_principal_lower_bound() -> None:
    residual, coefficients = _synthetic_cell(Fraction(1), Fraction(2))
    with pytest.raises(ValueError, match="not certified positive"):
        validated_adjoint_energy_dual_cell(
            residual,
            coefficients,
            principal_lower_bound=Fraction(2),
            completed_potential_lower_bound=Fraction(1, 4),
        )
