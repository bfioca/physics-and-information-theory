from functools import cache
from fractions import Fraction
import json
from pathlib import Path

import pytest

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    RationalResponseTrialPair,
    rational_response_trial_pair_from_record,
)
from qgtoy.validated_centrifugal_origin_profile_jets import (
    _sinc_centered_quotient_interval,
    rational_origin_trial_cell_from_archive,
    validated_archived_origin_trial_residual_family,
    validated_authenticated_origin_profile_kernel_cells,
)
from qgtoy.validated_interval import RationalInterval
from qgtoy.validated_skyrmion_quintic_family import (
    ValidatedSkyrmionQuinticFamily,
    validate_skyrmion_origin_quintic_family,
)


ROOT = Path(__file__).resolve().parents[1]
AUTHENTICATED_SLOPES = RationalInterval(
    Fraction(546_684_696_508_091, 347_185_136_818_875),
    Fraction(550_388_004_634_159, 347_185_136_818_875),
)


@cache
def _family() -> ValidatedSkyrmionQuinticFamily:
    return validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )


@cache
def _pair() -> RationalResponseTrialPair:
    record = json.loads(
        (
            ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
        ).read_text(encoding="ascii")
    )
    return rational_response_trial_pair_from_record(record["trial_archive"])


def test_centered_sinc_quotient_includes_removable_center_value() -> None:
    argument = RationalInterval(Fraction(0), Fraction(1, 100))

    ordinary = _sinc_centered_quotient_interval(
        argument,
        scale_squared=1,
        terms=4,
    )
    doubled = _sinc_centered_quotient_interval(
        argument,
        scale_squared=4,
        terms=4,
    )

    assert ordinary.contains(Fraction(-1, 6))
    assert doubled.contains(Fraction(-2, 3))
    with pytest.raises(ValueError, match="nonnegative"):
        _sinc_centered_quotient_interval(
            RationalInterval(Fraction(-1), Fraction(0)),
            scale_squared=1,
            terms=4,
        )


def test_authenticated_kernel_cells_cover_slopes_and_center_jets() -> None:
    family = _family()
    cells = validated_authenticated_origin_profile_kernel_cells(
        family,
        kernel_terms=4,
    )

    assert len(cells) == 2
    assert cells[0].shooting_slopes.lower == AUTHENTICATED_SLOPES.lower
    assert cells[-1].shooting_slopes.upper == AUTHENTICATED_SLOPES.upper
    assert cells[0].shooting_slopes.upper == cells[1].shooting_slopes.lower
    for cell in cells:
        kernels = cell.kernels
        assert kernels.time == RationalInterval(Fraction(0), Fraction(1, 256))
        assert kernels.metric_factor == RationalInterval(
            Fraction(102_399, 102_400),
            Fraction(1),
        )
        assert kernels.metric_factor_time_derivative == RationalInterval.point(
            Fraction(-1, 400)
        )
        assert cell.cubic_coefficient.scale(-3).is_subset_of(
            kernels.profile_deficit_radial_derivative_time_derivative
        )
        expected_sine_t = (
            -cell.cubic_coefficient
            - cell.shooting_slopes.power(3).scale(Fraction(1, 6))
        )
        assert expected_sine_t.is_subset_of(
            kernels.sine_over_radius_time_derivative
        )
        expected_cosine_t = cell.shooting_slopes.power(2).scale(
            Fraction(-1, 2)
        )
        assert expected_cosine_t.is_subset_of(
            kernels.cosine_of_profile_deficit_time_derivative
        )


def test_archive_normalization_preserves_both_origin_endpoint_jets() -> None:
    for archived in (_pair().primal.origin, _pair().adjoint.origin):
        normalized = rational_origin_trial_cell_from_archive(archived)
        assert normalized.time_horizon == archived.cutoff**2
        assert normalized.physical_endpoint_jet() == archived.physical_endpoint_jet()


@cache
def _residual_pair():
    family = _family()
    pair = _pair()
    return (
        validated_archived_origin_trial_residual_family(
            family,
            pair.primal,
            load="rotational",
            kernel_terms=4,
        ),
        validated_archived_origin_trial_residual_family(
            family,
            pair.adjoint,
            load="zero",
            kernel_terms=4,
        ),
    )


def test_archived_primal_and_adjoint_shaped_trials_reach_origin_residual_api() -> None:
    primal, adjoint_operator = _residual_pair()

    assert primal.trial_name == "primal"
    assert primal.load == "rotational"
    assert adjoint_operator.trial_name == "adjoint"
    assert adjoint_operator.load == "zero"
    assert len(primal.residuals) == len(adjoint_operator.residuals) == 2
    assert all(item.radius_cutoff == Fraction(1, 16) for item in primal.residuals)
    assert primal.maximum_l2_squared_upper < Fraction(1, 1_000)
    assert adjoint_operator.maximum_l2_squared_upper < Fraction(1, 1_000_000)


def test_origin_residual_family_rejects_an_undeclared_load() -> None:
    with pytest.raises(ValueError, match="load"):
        validated_archived_origin_trial_residual_family(
            _family(),
            _pair().primal,
            load="adjoint",  # type: ignore[arg-type]
            kernel_terms=4,
        )
