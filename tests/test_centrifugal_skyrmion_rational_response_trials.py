from fractions import Fraction

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    build_rational_response_trial_pair,
    rational_response_trial_pair_from_record,
    rational_response_trial_pair_to_record,
    refine_rational_response_trial,
)
from qgtoy.validated_interval import RationalInterval


def test_rational_trials_are_exactly_c1_origin_regular_and_round_trip() -> None:
    partition = (
        RationalInterval(Fraction(1, 16), Fraction(2)),
        RationalInterval(Fraction(2), Fraction(4)),
    )
    pair = build_rational_response_trial_pair(
        partition,
        node_count=9,
        quadrature_order=3,
        profile_step=0.004,
        rounding_denominator=10**9,
    )
    pair.validate()
    for trial in (pair.primal, pair.adjoint):
        assert trial.origin.physical_endpoint_jet() == (
            trial.positive_radius_cells[0].endpoint_jet(right=False)
        )
        wall_values, _ = trial.positive_radius_cells[-1].endpoint_jet(right=True)
        assert wall_values[1] == 0

    record = rational_response_trial_pair_to_record(pair)
    assert rational_response_trial_pair_from_record(record) == pair


def test_rational_trial_builder_rejects_noncontiguous_partition() -> None:
    partition = (
        RationalInterval(Fraction(1, 16), Fraction(1)),
        RationalInterval(Fraction(2), Fraction(4)),
    )
    try:
        build_rational_response_trial_pair(
            partition,
            node_count=9,
            quadrature_order=3,
            profile_step=0.004,
        )
    except ValueError as error:
        assert "contiguous" in str(error)
    else:
        raise AssertionError("noncontiguous partition was accepted")


def test_exact_equal_subcell_restriction_preserves_endpoint_jets() -> None:
    pair = build_rational_response_trial_pair(
        (RationalInterval(Fraction(1, 16), Fraction(4)),),
        node_count=9,
        quadrature_order=3,
        profile_step=0.004,
        rounding_denominator=10**9,
    )
    original = pair.primal
    refined = refine_rational_response_trial(
        original,
        subdivisions_per_cell=4,
    )
    assert len(refined.positive_radius_cells) == 4
    assert refined.positive_radius_cells[0].endpoint_jet(
        right=False
    ) == original.positive_radius_cells[0].endpoint_jet(right=False)
    assert refined.positive_radius_cells[-1].endpoint_jet(
        right=True
    ) == original.positive_radius_cells[0].endpoint_jet(right=True)
    refined.validate()
