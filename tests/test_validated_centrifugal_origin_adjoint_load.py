from functools import cache
from fractions import Fraction
import json
from pathlib import Path

import pytest

from qgtoy.centrifugal_skyrmion_rational_response_trials import (
    RationalResponseTrialPair,
    rational_response_trial_pair_from_record,
)
from qgtoy.static_patch_l2_response import (
    l2_center_regular_solution,
    l2_center_regular_solution_derivative,
)
from qgtoy.validated_centrifugal_adjoint_bulk_load import (
    centrifugal_weak_master_load_affine_kernel,
)
from qgtoy.validated_centrifugal_origin_adjoint_load import (
    _center_regular_green_hat_jets,
    centrifugal_weak_master_load_origin_affine_kernel,
    validated_archived_loaded_origin_adjoint_residual_family,
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


def test_regular_weak_load_matches_positive_radius_kernel_exactly() -> None:
    x = Fraction(2, 5)
    t = x**2
    curvature = Fraction(1, 400)
    metric = 1 - curvature * t
    metric_t = -curvature
    sine_over_radius = Fraction(6, 5)
    cosine_deficit = Fraction(4, 5)
    rho = Fraction(7, 5)
    green_hat = Fraction(11, 13)
    green_derivative_hat = Fraction(17, 19)
    common = {
        "pion_mass_squared": Fraction(6, 5),
        "gravitational_coupling": Fraction(3, 2),
    }
    positive = centrifugal_weak_master_load_affine_kernel(
        radius=x,
        metric_factor=metric,
        metric_factor_derivative=2 * x * metric_t,
        inverse_patch_radius_squared=curvature,
        sine_profile=x * sine_over_radius,
        cosine_profile=-cosine_deficit,
        profile_derivative=-rho,
        green_weight=x**3 * green_hat,
        green_weight_derivative=x**2 * green_derivative_hat,
        **common,
    )
    regular = centrifugal_weak_master_load_origin_affine_kernel(
        t=t,
        metric_factor=metric,
        metric_factor_time_derivative=metric_t,
        inverse_patch_radius_squared=curvature,
        profile_deficit_radial_derivative=rho,
        sine_over_radius=sine_over_radius,
        cosine_of_profile_deficit=cosine_deficit,
        green_weight_hat=green_hat,
        green_weight_derivative_hat=green_derivative_hat,
        **common,
    )

    assert positive.rigid == x**4 * regular.rigid_density_hat
    assert positive.b0 == tuple(x * entry for entry in regular.coordinate_source_hat)
    assert positive.b1 == tuple(t * entry for entry in regular.derivative_source_hat)


def test_regular_weak_load_hats_vanish_exactly_at_center() -> None:
    result = centrifugal_weak_master_load_origin_affine_kernel(
        t=Fraction(0),
        metric_factor=Fraction(1),
        metric_factor_time_derivative=Fraction(-1, 400),
        inverse_patch_radius_squared=Fraction(1, 400),
        profile_deficit_radial_derivative=Fraction(3, 2),
        sine_over_radius=Fraction(3, 2),
        cosine_of_profile_deficit=Fraction(1),
        green_weight_hat=Fraction(1, 3000),
        green_weight_derivative_hat=Fraction(1, 1000),
        pion_mass_squared=Fraction(1),
        gravitational_coupling=Fraction(1),
    )
    assert result.coordinate_source_hat == (0, 0)
    assert result.derivative_source_hat == (0, 0)


@pytest.mark.parametrize("cutoff", [Fraction(1, 16), Fraction(1)])
def test_green_hat_series_encloses_center_and_endpoint(cutoff: Fraction) -> None:
    patch_radius = Fraction(20)
    value, derivative = _center_regular_green_hat_jets(
        RationalInterval(Fraction(0), cutoff**2),
        patch_radius=patch_radius,
        terms=8,
    )
    center_value = Fraction(2, 15 * patch_radius**2)
    center_derivative = 3 * center_value
    assert value.value.contains(center_value)
    assert derivative.value.contains(center_derivative)

    ratio = float(cutoff / patch_radius)
    exact_value = (
        2.0
        * float(patch_radius)
        / 15.0
        * l2_center_regular_solution(ratio)
        / float(cutoff**3)
    )
    exact_derivative = (
        2.0 / 15.0 * l2_center_regular_solution_derivative(ratio) / float(cutoff**2)
    )
    assert float(value.value.lower) <= exact_value * (1 + 1.0e-14)
    assert exact_value <= float(value.value.upper) * (1 + 1.0e-14)
    assert float(derivative.value.lower) <= exact_derivative * (1 + 1.0e-14)
    assert exact_derivative <= float(derivative.value.upper) * (1 + 1.0e-14)


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


def test_authenticated_loaded_adjoint_origin_residual_is_small() -> None:
    result = validated_archived_loaded_origin_adjoint_residual_family(
        _family(),
        _pair().adjoint,
        kernel_terms=4,
        green_terms=8,
    )

    assert result.trial_name == "adjoint"
    assert len(result.loads) == len(result.residuals) == 2
    assert all(item.radius_cutoff == Fraction(1, 16) for item in result.residuals)
    assert result.maximum_l2_squared_upper < Fraction(1, 100_000_000)
    assert all(
        all(entry.contains(0) for entry in load.coordinate_source_hat)
        and all(entry.contains(0) for entry in load.derivative_source_hat)
        for load in result.loads
    )


def test_green_hat_series_rejects_domain_beyond_static_wall() -> None:
    with pytest.raises(ValueError, match=r"sqrt\(t\)/patch_radius"):
        _center_regular_green_hat_jets(
            RationalInterval(Fraction(0), Fraction(17)),
            patch_radius=Fraction(20),
            terms=8,
        )
