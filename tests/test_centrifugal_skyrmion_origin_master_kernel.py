from fractions import Fraction
from math import cos, sin, sqrt

import pytest

from qgtoy.centrifugal_skyrmion_affine_master_kernel import (
    centrifugal_completed_master_source_generic,
)
from qgtoy.centrifugal_skyrmion_origin_master_kernel import (
    centrifugal_completed_master_source_origin_affine_kernel,
    centrifugal_completed_master_source_origin_generic,
)
from qgtoy.validated_interval import RationalInterval


def _positive_radius_data(t: float) -> dict[str, float]:
    x = sqrt(t)
    w = 1.3 + 0.2 * t - 0.07 * t**2
    w_t = 0.2 - 0.14 * t
    w_tt = -0.14
    p = w + 2.0 * t * w_t
    argument = x * w
    sine_over_radius = sin(argument) / x
    sine_over_radius_t = (cos(argument) * p - sine_over_radius) / (2.0 * t)
    return {
        "x": x,
        "w": w,
        "w_t": w_t,
        "w_tt": w_tt,
        "p": p,
        "p_t": 3.0 * w_t + 2.0 * t * w_tt,
        "s": sine_over_radius,
        "s_t": sine_over_radius_t,
        "c": cos(argument),
    }


@pytest.mark.parametrize("t", [1.0e-4, 0.03, 0.4, 1.2])
def test_origin_factor_matches_uncancelled_positive_radius_kernel(t: float) -> None:
    profile = _positive_radius_data(t)
    x = profile["x"]
    curvature = 1.0 / 400.0
    metric = 1.0 - curvature * t
    u, u_t, u_tt = 0.31, -0.08, 0.04
    v, v_t, v_tt = -0.27, 0.06, -0.03
    a = -v + t * u
    a_t = -v_t + u + t * u_t
    fp = a + 2.0 * t * a_t
    fp_t = 3.0 * u - 3.0 * v_t + 7.0 * t * u_t - 2.0 * t * v_tt + 2.0 * t**2 * u_tt
    gp = v + 2.0 * t * v_t
    generic = centrifugal_completed_master_source_generic(
        radius=x,
        metric_factor=metric,
        metric_factor_derivative=-2.0 * curvature * x,
        inverse_patch_radius_squared=curvature,
        sine_profile=x * profile["s"],
        cosine_profile=-profile["c"],
        profile_derivative=-profile["p"],
        profile_second_derivative=-2.0 * x * profile["p_t"],
        radial_field=x * a,
        radial_field_derivative=fp,
        radial_field_second_derivative=2.0 * x * fp_t,
        tangential_field=x * v,
        tangential_field_derivative=gp,
        pion_mass_squared=1.0,
        gravitational_coupling=1.7,
    )
    regular = centrifugal_completed_master_source_origin_generic(
        t=t,
        metric_factor=metric,
        metric_factor_time_derivative=-curvature,
        inverse_patch_radius_squared=curvature,
        profile_deficit_over_radius=profile["w"],
        profile_deficit_time_derivative=profile["w_t"],
        profile_deficit_second_time_derivative=profile["w_tt"],
        sine_over_radius=profile["s"],
        sine_over_radius_time_derivative=profile["s_t"],
        cosine_of_profile_deficit=profile["c"],
        u=u,
        u_time_derivative=u_t,
        u_second_time_derivative=u_tt,
        v=v,
        v_time_derivative=v_t,
        v_second_time_derivative=v_tt,
        pion_mass_squared=1.0,
        gravitational_coupling=1.7,
    )
    assert generic == pytest.approx(x * regular, rel=3.0e-12, abs=3.0e-12)


def test_origin_center_is_exact_and_finite_without_division_by_t() -> None:
    result = centrifugal_completed_master_source_origin_generic(
        t=Fraction(0),
        metric_factor=Fraction(1),
        metric_factor_time_derivative=Fraction(-1, 400),
        inverse_patch_radius_squared=Fraction(1, 400),
        profile_deficit_over_radius=Fraction(3, 2),
        profile_deficit_time_derivative=Fraction(1, 7),
        profile_deficit_second_time_derivative=Fraction(-1, 11),
        sine_over_radius=Fraction(3, 2),
        sine_over_radius_time_derivative=Fraction(-47, 112),
        cosine_of_profile_deficit=Fraction(1),
        u=Fraction(2, 5),
        u_time_derivative=Fraction(-1, 9),
        u_second_time_derivative=Fraction(1, 13),
        v=Fraction(-3, 7),
        v_time_derivative=Fraction(2, 11),
        v_second_time_derivative=Fraction(-1, 17),
        pion_mass_squared=Fraction(1),
        gravitational_coupling=Fraction(3, 2),
    )
    assert isinstance(result, Fraction)


def test_origin_affine_coefficients_match_exact_basis_evaluations() -> None:
    background = {
        "t": Fraction(2, 9),
        "metric_factor": Fraction(899, 900),
        "metric_factor_time_derivative": Fraction(-1, 400),
        "inverse_patch_radius_squared": Fraction(1, 400),
        "profile_deficit_over_radius": Fraction(7, 5),
        "profile_deficit_time_derivative": Fraction(1, 8),
        "profile_deficit_second_time_derivative": Fraction(-1, 12),
        "sine_over_radius": Fraction(6, 5),
        "sine_over_radius_time_derivative": Fraction(-1, 3),
        "cosine_of_profile_deficit": Fraction(4, 5),
        "pion_mass_squared": Fraction(1),
        "gravitational_coupling": Fraction(5, 4),
    }
    names = (
        "u",
        "u_time_derivative",
        "u_second_time_derivative",
        "v",
        "v_time_derivative",
        "v_second_time_derivative",
    )
    kernel = centrifugal_completed_master_source_origin_affine_kernel(**background)
    zero_fields = {name: Fraction(0) for name in names}
    rigid = centrifugal_completed_master_source_origin_generic(
        **background, **zero_fields
    )
    assert kernel.rigid == rigid
    for name in names:
        basis = dict(zero_fields)
        basis[name] = Fraction(1)
        direct = centrifugal_completed_master_source_origin_generic(
            **background, **basis
        )
        assert getattr(kernel, name) == direct - rigid

    fields = {
        "u": Fraction(2, 13),
        "u_time_derivative": Fraction(-3, 17),
        "u_second_time_derivative": Fraction(5, 19),
        "v": Fraction(7, 23),
        "v_time_derivative": Fraction(-11, 29),
        "v_second_time_derivative": Fraction(13, 31),
    }
    assert kernel.evaluate(**fields) == (
        centrifugal_completed_master_source_origin_generic(
            **background, **fields
        )
    )


def test_origin_affine_kernel_accepts_intervals_containing_center() -> None:
    point = RationalInterval.point
    kernel = centrifugal_completed_master_source_origin_affine_kernel(
        t=RationalInterval(Fraction(0), Fraction(1, 256)),
        metric_factor=RationalInterval(Fraction(399, 400), Fraction(1)),
        metric_factor_time_derivative=point(Fraction(-1, 400)),
        inverse_patch_radius_squared=point(Fraction(1, 400)),
        profile_deficit_over_radius=RationalInterval(Fraction(7, 5), Fraction(8, 5)),
        profile_deficit_time_derivative=RationalInterval(Fraction(-1), Fraction(1)),
        profile_deficit_second_time_derivative=RationalInterval(Fraction(-2), Fraction(2)),
        sine_over_radius=RationalInterval(Fraction(7, 5), Fraction(8, 5)),
        sine_over_radius_time_derivative=RationalInterval(Fraction(-2), Fraction(0)),
        cosine_of_profile_deficit=RationalInterval(Fraction(9, 10), Fraction(1)),
        pion_mass_squared=point(Fraction(1)),
        gravitational_coupling=point(Fraction(1)),
    )
    assert isinstance(kernel.rigid, RationalInterval)
    assert isinstance(kernel.v_second_time_derivative, RationalInterval)
