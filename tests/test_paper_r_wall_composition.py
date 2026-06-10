import json
from fractions import Fraction
from pathlib import Path

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    rational_response_trial_pair_from_record,
)
from qgtoy.paper_r_wall_composition import (
    certify_paper_r_weak_wall_contribution,
)
from qgtoy.validated_centrifugal_response_residual import (
    validated_wall_conormal_coefficients,
    wall_endpoint_conormal_residual,
)
from qgtoy.validated_centrifugal_wall_master_load import (
    DEFAULT_WALL_SLOPE,
    validated_wall_master_load,
)
from qgtoy.validated_interval import RationalInterval


ROOT = Path(__file__).resolve().parents[1]


def _pair():
    archive = json.loads(
        (
            ROOT
            / "experiments/centrifugal_skyrmion_rational_response_trials.json"
        ).read_text(encoding="ascii")
    )
    return rational_response_trial_pair_from_record(archive["trial_archive"])


def test_weak_wall_composition_excludes_the_trial_conormal() -> None:
    pair = _pair()
    coefficients = validated_wall_conormal_coefficients(DEFAULT_WALL_SLOPE)
    master_load = validated_wall_master_load(DEFAULT_WALL_SLOPE)
    result = certify_paper_r_weak_wall_contribution(
        primal_trial=pair.primal,
        adjoint_trial=pair.adjoint,
        coefficients=coefficients,
        master_load=master_load,
    )

    assert result.primal_radial_value == Fraction(-25120922083, 10**12)
    assert result.adjoint_radial_value == Fraction(1456432537, 250_000_000_000)
    assert not result.conormal_residual_included
    assert result.corrected_estimator_wall_contribution == (
        result.adjoint_weak_wall_residual.scale(result.primal_radial_value)
    )
    assert result.corrected_estimator_wall_contribution.upper < 0
    assert result.adjoint_weak_wall_residual.lower > 0

    # The conormal wall residual is the boundary coefficient for the all-strong
    # primal representation.  It is deliberately not the weak wall term.
    strong_primal = wall_endpoint_conormal_residual(
        coefficients=coefficients,
        trial=pair.primal.positive_radius_cells[-1],
    )
    old_mixed_representation = (
        master_load.gamma_b.scale(result.primal_radial_value)
        - strong_primal.scale(result.adjoint_radial_value)
    )
    assert old_mixed_representation != result.corrected_estimator_wall_contribution


def test_nonzero_primal_wall_load_enters_only_the_primal_residual_term() -> None:
    pair = _pair()
    coefficients = validated_wall_conormal_coefficients(DEFAULT_WALL_SLOPE)
    master_load = validated_wall_master_load(DEFAULT_WALL_SLOPE)
    unloaded = certify_paper_r_weak_wall_contribution(
        primal_trial=pair.primal,
        adjoint_trial=pair.adjoint,
        coefficients=coefficients,
        master_load=master_load,
    )
    load = RationalInterval.point(Fraction(1, 7))
    loaded = certify_paper_r_weak_wall_contribution(
        primal_trial=pair.primal,
        adjoint_trial=pair.adjoint,
        coefficients=coefficients,
        master_load=master_load,
        primal_wall_load=load,
    )

    expected_shift = load.scale(loaded.adjoint_radial_value)
    assert loaded.master_wall_contribution == unloaded.master_wall_contribution
    assert loaded.primal_residual_wall_contribution == (
        unloaded.primal_residual_wall_contribution + expected_shift
    )
    assert loaded.corrected_estimator_wall_contribution == (
        unloaded.corrected_estimator_wall_contribution + expected_shift
    )
