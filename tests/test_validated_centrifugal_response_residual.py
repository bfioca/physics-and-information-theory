from fractions import Fraction

import pytest

from qgtoy.centrifugal_skyrmion_deformation import (
    quadrupole_static_hessian_matrix,
)
from qgtoy.validated_centrifugal_response_residual import (
    COMPACT_PI_INTERVAL,
    RationalC1TrialCell,
    ValidatedConormalStrongCell,
    ValidatedProfileJetCell,
    certify_energy_dual_residual_upper,
    reduced_profile_trigonometric_intervals,
    validate_rational_c1_trial_cells,
    validated_conormal_strong_cell_from_profile,
    validated_strong_residual_cell,
    validated_wall_conormal_coefficients,
    wall_endpoint_conormal_residual,
    wall_conormal_residual,
)
from qgtoy.validated_interval import (
    RationalInterval,
    RationalPolynomial,
    pi_machin_interval,
)


def _point(value: int | Fraction) -> RationalInterval:
    return RationalInterval.point(value)


def test_profile_trigonometric_reduction_uses_small_endpoint_angles() -> None:
    pi_box = pi_machin_interval(terms=32)
    assert pi_box.is_subset_of(COMPACT_PI_INTERVAL)
    near_pi = RationalInterval(
        pi_box.lower - Fraction(1, 100),
        pi_box.upper - Fraction(1, 200),
    )
    sine, cosine_deficit = reduced_profile_trigonometric_intervals(
        near_pi,
        trigonometric_terms=6,
    )
    assert sine.lower > 0
    assert sine.upper < Fraction(1, 50)
    assert cosine_deficit.lower > Fraction(99, 100)

    near_zero = RationalInterval(Fraction(1, 200), Fraction(1, 100))
    sine_zero, cosine_deficit_zero = reduced_profile_trigonometric_intervals(
        near_zero,
        trigonometric_terms=6,
    )
    assert sine_zero.lower > 0
    assert sine_zero.upper < Fraction(1, 50)
    assert cosine_deficit_zero.upper < Fraction(-99, 100)


def test_validated_wall_endpoint_matches_generic_conormal_formula() -> None:
    wall = validated_wall_conormal_coefficients(
        RationalInterval(Fraction(-95, 1000), Fraction(-87, 1000))
    )
    assert wall.wall_form_coefficient.lower > 0
    assert wall.wall_trace_margin.lower > Fraction(1, 5)
    trial = RationalC1TrialCell(
        radius=RationalInterval(Fraction(3), Fraction(4)),
        radial_field=RationalPolynomial((Fraction(1, 10), Fraction(1, 20))),
        tangential_field=RationalPolynomial((0,)),
    )
    endpoint = wall_endpoint_conormal_residual(
        coefficients=wall,
        trial=trial,
    )
    zero_matrix = ((_point(0), _point(0)), (_point(0), _point(0)))
    generic = wall_conormal_residual(
        coefficients=ValidatedConormalStrongCell(
            radius=trial.radius,
            coordinate=zero_matrix,
            mixed=wall.mixed,
            principal=wall.principal,
            mixed_derivative=zero_matrix,
            principal_derivative=zero_matrix,
            strong_source=(_point(0), _point(0)),
        ),
        trial=trial,
        wall_form_coefficient=wall.wall_form_coefficient,
    )
    assert endpoint == generic


def _zero_matrix():
    zero = _point(0)
    return ((zero, zero), (zero, zero))


def _identity_matrix():
    zero = _point(0)
    one = _point(1)
    return ((one, zero), (zero, one))


def test_exact_piecewise_trial_checks_c1_joins_and_wall_trace() -> None:
    first = RationalC1TrialCell(
        radius=RationalInterval(1, 2),
        radial_field=RationalPolynomial((0, 1)),
        tangential_field=RationalPolynomial((0, 0)),
    )
    second = RationalC1TrialCell(
        radius=RationalInterval(2, 3),
        radial_field=RationalPolynomial((1, 1)),
        tangential_field=RationalPolynomial((0, 0)),
    )
    validate_rational_c1_trial_cells((first, second))

    broken = RationalC1TrialCell(
        radius=RationalInterval(2, 3),
        radial_field=RationalPolynomial((1, 2)),
        tangential_field=RationalPolynomial((0, 0)),
    )
    with pytest.raises(ValueError, match="exact C1 join"):
        validate_rational_c1_trial_cells((first, broken))

    bad_wall = RationalC1TrialCell(
        radius=RationalInterval(2, 3),
        radial_field=RationalPolynomial((1, 1)),
        tangential_field=RationalPolynomial((0, 0, 3, -2)),
    )
    with pytest.raises(ValueError, match="tangential wall trace"):
        validate_rational_c1_trial_cells((first, bad_wall))


def test_profile_jet_reproduces_pointwise_physical_hessian() -> None:
    epsilon = Fraction(1, 10**9)
    profile = ValidatedProfileJetCell(
        radius=RationalInterval(Fraction(2), Fraction(2) + epsilon),
        profile=_point(1),
        derivative=_point(Fraction(-1, 3)),
        second_derivative=_point(Fraction(1, 10)),
    )
    coefficients = validated_conormal_strong_cell_from_profile(profile)
    floating = quadrupole_static_hessian_matrix(
        radius=2.0,
        metric_factor=0.99,
        profile=1.0,
        profile_derivative=-1.0 / 3.0,
        pion_mass=1.0,
    )["symmetric_hessian_matrix"]
    blocks = (
        coefficients.coordinate,
        coefficients.mixed,
        coefficients.principal,
    )
    positions = (
        ((0, 0), (0, 1), (1, 0), (1, 1)),
        ((0, 2), (0, 3), (1, 2), (1, 3)),
        ((2, 2), (2, 3), (3, 2), (3, 3)),
    )
    for block, block_positions in zip(blocks, positions, strict=True):
        for interval, (row, column) in zip(
            (entry for block_row in block for entry in block_row),
            block_positions,
            strict=True,
        ):
            assert float(interval.lower) <= floating[row][column]
            assert floating[row][column] <= float(interval.upper)


def test_cell_residual_integrates_exact_rational_square_bound() -> None:
    radius = RationalInterval(1, 2)
    coefficients = ValidatedConormalStrongCell(
        radius=radius,
        coordinate=_zero_matrix(),
        mixed=_zero_matrix(),
        principal=_identity_matrix(),
        mixed_derivative=_zero_matrix(),
        principal_derivative=_zero_matrix(),
        strong_source=(_point(0), _point(0)),
    )
    trial = RationalC1TrialCell(
        radius=radius,
        radial_field=RationalPolynomial((0, 1, -1)),
        tangential_field=RationalPolynomial((0,)),
    )
    residual = validated_strong_residual_cell(coefficients, trial)
    assert residual.residual == (_point(-2), _point(0))
    assert residual.l2_squared_upper == 4


def test_energy_dual_composes_bulk_coercivity_and_wall_trace() -> None:
    radius = RationalInterval(1, 2)
    coefficients = ValidatedConormalStrongCell(
        radius=radius,
        coordinate=_zero_matrix(),
        mixed=_zero_matrix(),
        principal=_identity_matrix(),
        mixed_derivative=_zero_matrix(),
        principal_derivative=_zero_matrix(),
        strong_source=(_point(0), _point(0)),
    )
    trial = RationalC1TrialCell(
        radius=radius,
        radial_field=RationalPolynomial((0, 1, -1)),
        tangential_field=RationalPolynomial((0,)),
    )
    residual = validated_strong_residual_cell(coefficients, trial)
    bound = certify_energy_dual_residual_upper(
        (residual,),
        residual_domain=radius,
        interface_distribution_free=True,
        operator_lower_bound=Fraction(1, 100),
        wall_trace_margin_lower_bound=Fraction(1, 4),
        wall_residual=_point(3),
    )
    assert bound.l2_norm_upper == 2
    assert bound.bulk_energy_dual_upper == 20
    assert bound.wall_energy_dual_upper == 6
    assert bound.energy_dual_upper == 26


def test_wall_conormal_residual_keeps_boundary_mismatch_out_of_l2() -> None:
    radius = RationalInterval(1, 2)
    coefficients = ValidatedConormalStrongCell(
        radius=radius,
        coordinate=_zero_matrix(),
        mixed=_zero_matrix(),
        principal=_identity_matrix(),
        mixed_derivative=_zero_matrix(),
        principal_derivative=_zero_matrix(),
        strong_source=(_point(0), _point(0)),
    )
    trial = RationalC1TrialCell(
        radius=radius,
        radial_field=RationalPolynomial((1, 2)),
        tangential_field=RationalPolynomial((0,)),
    )
    # p_f=f'=2 and k f=3*(1+2)=9 at the right endpoint.
    assert wall_conormal_residual(
        coefficients=coefficients,
        trial=trial,
        wall_form_coefficient=_point(3),
    ) == _point(11)
