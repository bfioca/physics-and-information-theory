from functools import cache
from fractions import Fraction
import json
from pathlib import Path

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    RationalResponseTrialPair,
    rational_response_trial_pair_from_record,
)
from qgtoy.validated_centrifugal_origin_adjoint_load import (
    ValidatedOriginWeakMasterLoadCell,
)
from qgtoy.validated_centrifugal_origin_corrected_estimator import (
    validated_archived_origin_corrected_estimator_family,
    validated_origin_master_functional_contribution,
    validated_origin_primal_residual_action,
    validated_regular_trial_physical_ranges,
)
from qgtoy.validated_centrifugal_origin_profile_jets import (
    rational_origin_trial_cell_from_archive,
)
from qgtoy.validated_centrifugal_origin_response_residual import (
    RationalOriginTrialCell,
    ValidatedOriginStrongResidual,
)
from qgtoy.validated_interval import RationalInterval, RationalPolynomial
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
def _pair() -> RationalResponseTrialPair:
    record = json.loads(
        (
            ROOT / "experiments/centrifugal_skyrmion_rational_response_trials.json"
        ).read_text(encoding="ascii")
    )
    return rational_response_trial_pair_from_record(record["trial_archive"])


@cache
def _family() -> ValidatedSkyrmionQuinticFamily:
    return validate_skyrmion_origin_quintic_family(
        AUTHENTICATED_SLOPES,
        slope_cells=2,
    )


def test_exact_polynomial_trial_ranges_contain_direct_values() -> None:
    trial = rational_origin_trial_cell_from_archive(_pair().adjoint.origin)
    ranges = validated_regular_trial_physical_ranges(trial)
    horizon = trial.time_horizon
    for tau in (Fraction(0), Fraction(1, 2), Fraction(1)):
        u = trial.u.evaluate(tau).lower
        v = trial.v.evaluate(tau).lower
        u_tau = trial.u.derivative().evaluate(tau).lower
        v_tau = trial.v.derivative().evaluate(tau).lower
        field = (-v + horizon * tau * u, v)
        derivative = (
            -v + 3 * horizon * tau * u - 2 * tau * v_tau + 2 * horizon * tau**2 * u_tau,
            v + 2 * tau * v_tau,
        )
        assert all(
            enclosure.contains(value)
            for enclosure, value in zip(ranges.field_over_radius, field, strict=True)
        )
        assert all(
            enclosure.contains(value)
            for enclosure, value in zip(
                ranges.physical_derivative, derivative, strict=True
            )
        )


def _zero_vector() -> tuple[RationalInterval, RationalInterval]:
    zero = RationalInterval.point(0)
    return zero, zero


def test_rigid_master_weight_and_residual_action_weights_are_exact() -> None:
    point = RationalInterval.point
    time = RationalInterval(Fraction(0), Fraction(1, 4))
    zero_vector = _zero_vector()
    load = ValidatedOriginWeakMasterLoadCell(
        time=time,
        green_weight_hat=point(0),
        green_weight_hat_time_derivative=point(0),
        green_weight_derivative_hat=point(0),
        green_weight_derivative_hat_time_derivative=point(0),
        rigid_density_hat=point(2),
        field_over_radius_coefficient=zero_vector,
        physical_derivative_coefficient=zero_vector,
        coordinate_source_hat=zero_vector,
        coordinate_source_hat_time_derivative=zero_vector,
        derivative_source_hat=zero_vector,
        derivative_source_hat_time_derivative=zero_vector,
    )
    constant = RationalOriginTrialCell(
        time_horizon=Fraction(1, 4),
        u=RationalPolynomial((0,)),
        v=RationalPolynomial((1,)),
    )
    master = validated_origin_master_functional_contribution(load, constant)
    assert master.radial_weight == Fraction(1, 160)
    assert master.contribution == point(Fraction(1, 80))

    residual = ValidatedOriginStrongResidual(
        time=time,
        radius_cutoff=Fraction(1, 2),
        residual_hat=(point(2), point(3)),
        cutoff_derivative_residual=(point(4), point(5)),
        l2_squared_upper=Fraction(0),
    )
    action = validated_origin_primal_residual_action(residual, constant)
    # a=(-1,1), so r_hat dot a=1 and integral x^2 dx=1/24.
    assert action.action_density_hat == point(1)
    assert action.radial_weight == Fraction(1, 24)
    assert action.volume_action == point(Fraction(1, 24))
    assert action.cutoff_test_value == (point(Fraction(-1, 2)), point(Fraction(1, 2)))
    assert action.cutoff_trace == point(Fraction(1, 2))
    assert action.action == point(Fraction(13, 24))


@cache
def _estimator_family():
    pair = _pair()
    return validated_archived_origin_corrected_estimator_family(
        _family(),
        pair.primal,
        pair.adjoint,
        kernel_terms=4,
        green_terms=8,
    )


def test_signed_origin_estimator_covers_every_authenticated_slope_cell() -> None:
    result = _estimator_family()

    assert result.primal_trial_name == "primal"
    assert result.adjoint_trial_name == "adjoint"
    assert len(result.cells) == 2
    assert result.cells[0].shooting_slopes.lower == AUTHENTICATED_SLOPES.lower
    assert result.cells[-1].shooting_slopes.upper == AUTHENTICATED_SLOPES.upper
    assert (
        result.cells[0].shooting_slopes.upper == result.cells[1].shooting_slopes.lower
    )
    assert result.master_functional_hull.lower > Fraction(-1, 10**9)
    assert result.master_functional_hull.upper < Fraction(1, 10**9)
    assert result.residual_action_hull.lower > Fraction(-1, 1_000_000)
    assert result.residual_action_hull.upper < Fraction(1, 1_000_000)
    assert result.corrected_contribution_hull.contains_zero()


def test_corrected_hull_contains_each_cellwise_sum() -> None:
    result = _estimator_family()
    for cell in result.cells:
        assert cell.master_functional.contribution.is_subset_of(
            result.master_functional_hull
        )
        assert cell.residual_action.action.is_subset_of(result.residual_action_hull)
        assert cell.corrected_contribution.is_subset_of(
            result.corrected_contribution_hull
        )
