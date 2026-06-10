from fractions import Fraction

from qgtoy.validated_centrifugal_correlated_adjoint import (
    CorrelatedAdjointEnergyDualCell,
    _constant_radial_jet,
    compose_correlated_positive_radius_wall_adjoint_bound,
    weak_adjoint_wall_residual,
)
from qgtoy.validated_centrifugal_liouville_taylor import _CenteredTaylorModel
from qgtoy.validated_centrifugal_response_residual import (
    RationalC1TrialCell,
    ValidatedWallConormalCoefficients,
)
from qgtoy.validated_centrifugal_wall_master_load import ValidatedWallMasterLoad
from qgtoy.validated_interval import RationalInterval, RationalPolynomial


def _synthetic_cell(
    left: Fraction,
    right: Fraction,
    *,
    scalar_square: Fraction,
    matrix_square: Fraction,
    local_inverse: bool,
) -> CorrelatedAdjointEnergyDualCell:
    point = RationalInterval.point
    zero_vector = (point(0), point(0))
    return CorrelatedAdjointEnergyDualCell(
        radius=RationalInterval(left, right),
        weak_value_coefficient=zero_vector,
        weak_derivative_coefficient=zero_vector,
        completed_derivative_coefficient=zero_vector,
        completed_value_coefficient=zero_vector,
        principal_first_minor_lower=Fraction(1),
        principal_determinant_lower=Fraction(1),
        completed_potential_first_minor_lower=Fraction(1),
        completed_potential_determinant_lower=Fraction(1),
        completed_potential_matrix_inverse_used=local_inverse,
        derivative_squared_dual_upper=scalar_square,
        value_squared_dual_upper=Fraction(0),
        squared_dual_upper=scalar_square,
        matrix_weighted_derivative_squared_dual_upper=matrix_square,
        matrix_weighted_value_squared_dual_upper=Fraction(0),
        matrix_weighted_squared_dual_upper=matrix_square,
    )


def test_hybrid_composer_adds_wall_and_names_origin_omission() -> None:
    cells = (
        _synthetic_cell(
            Fraction(1),
            Fraction(2),
            scalar_square=Fraction(4),
            matrix_square=Fraction(1),
            local_inverse=True,
        ),
        _synthetic_cell(
            Fraction(2),
            Fraction(3),
            scalar_square=Fraction(5),
            matrix_square=Fraction(2),
            local_inverse=False,
        ),
    )
    bound = compose_correlated_positive_radius_wall_adjoint_bound(
        cells,
        wall_residual=RationalInterval(Fraction(-1, 10), Fraction(1, 5)),
        wall_trace_margin_lower_bound=Fraction(1, 2),
    )
    assert bound.scalar_floor_bulk_squared_upper == 9
    assert bound.matrix_weighted_bulk_squared_upper == 3
    assert bound.wall_squared_upper == Fraction(2, 25)
    assert bound.matrix_weighted_partial_squared_upper == Fraction(77, 25)
    assert bound.local_potential_inverse_cell_count == 1
    assert bound.scalar_potential_fallback_cell_count == 1
    assert not bound.regular_origin_master_load_included
    assert not bound.full_loaded_adjoint_residual_certified


def test_physical_parameters_are_lifted_without_unit_reset() -> None:
    template = _CenteredTaylorModel.constant(Fraction(0))
    jet = _constant_radial_jet(template, Fraction(7, 3))
    assert jet.value.range().lower <= Fraction(7, 3) <= jet.value.range().upper
    assert jet.derivative.range() == RationalInterval.point(0)


def test_weak_wall_residual_excludes_trial_conormal() -> None:
    point = RationalInterval.point
    zero = point(0)
    trial = RationalC1TrialCell(
        radius=RationalInterval(Fraction(1), Fraction(2)),
        radial_field=RationalPolynomial((Fraction(2),)),
        tangential_field=RationalPolynomial((Fraction(0),)),
    )
    coefficients = ValidatedWallConormalCoefficients(
        wall_radius=Fraction(2),
        mixed=((point(100), zero), (zero, zero)),
        principal=((point(200), zero), (zero, zero)),
        robin_multiplier=point(0),
        wall_form_coefficient=point(3),
        wall_trace_margin=point(1),
    )
    load = ValidatedWallMasterLoad(
        wall_ratio=Fraction(1, 5),
        center_regular_solution=point(0),
        center_regular_solution_derivative=point(0),
        wall_green_weight=point(0),
        wall_green_weight_derivative=point(0),
        wall_profile_derivative=point(-1),
        wall_displacement_per_radial_field=point(0),
        gamma_b=RationalInterval(Fraction(7), Fraction(8)),
    )
    assert weak_adjoint_wall_residual(
        trial=trial, coefficients=coefficients, master_load=load
    ) == RationalInterval(Fraction(1), Fraction(2))
