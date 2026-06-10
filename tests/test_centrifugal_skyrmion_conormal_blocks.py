from math import pi, sin

import pytest

from qgtoy.centrifugal_skyrmion_conormal_blocks import (
    exact_formal_conormal_checks,
    regular_conormal_data,
)
from qgtoy.centrifugal_skyrmion_deformation import (
    quadrupole_static_hessian_matrix,
    rotational_quadrupole_source_covector,
)
from qgtoy.centrifugal_skyrmion_origin import centrifugal_origin_leading_hessian


@pytest.mark.parametrize(
    ("radius", "curvature", "w", "w_t", "pion_mass"),
    (
        (0.07, 1 / 400, 1.58, -0.31, 1.0),
        (0.19, 0.01, 1.21, 0.08, 0.7),
        (0.41, 0.04, 0.83, -0.14, 0.0),
    ),
)
def test_regular_blocks_reconstruct_physical_hessian(
    radius: float,
    curvature: float,
    w: float,
    w_t: float,
    pion_mass: float,
) -> None:
    t = radius**2
    h = 1 - curvature * t
    rho = w + 2 * t * w_t
    regular = regular_conormal_data(
        t=t,
        curvature=curvature,
        profile_deficit_over_radius=w,
        profile_deficit_time_derivative=w_t,
        pion_mass=pion_mass,
    )
    physical = quadrupole_static_hessian_matrix(
        radius=radius,
        metric_factor=h,
        profile=pi - radius * w,
        profile_derivative=-rho,
        pion_mass=pion_mass,
    )["symmetric_hessian_matrix"]
    reconstructed = (
        (*regular["coordinate"][0], *(radius * value for value in regular["mixed"][0])),
        (*regular["coordinate"][1], *(radius * value for value in regular["mixed"][1])),
        (
            radius * regular["mixed"][0][0],
            radius * regular["mixed"][1][0],
            *(t * value for value in regular["principal"][0]),
        ),
        (
            radius * regular["mixed"][0][1],
            radius * regular["mixed"][1][1],
            *(t * value for value in regular["principal"][1]),
        ),
    )
    for expected_row, actual_row in zip(physical, reconstructed, strict=True):
        assert actual_row == pytest.approx(expected_row, rel=2e-11, abs=2e-11)


@pytest.mark.parametrize("radius", (0.03, 0.17, 0.38))
def test_regular_source_reconstructs_physical_covector(radius: float) -> None:
    curvature = 1 / 400
    t = radius**2
    w = 1.57 - 0.22 * t + 0.04 * t**2
    w_t = -0.22 + 0.08 * t
    rho = w + 2 * t * w_t
    h = 1 - curvature * t
    regular = regular_conormal_data(
        t=t,
        curvature=curvature,
        profile_deficit_over_radius=w,
        profile_deficit_time_derivative=w_t,
        pion_mass=1.0,
    )
    physical = rotational_quadrupole_source_covector(
        radius=radius,
        metric_factor=h,
        profile=pi - radius * w,
        profile_derivative=-rho,
    )
    shat0 = regular["coordinate_source"]
    shat1 = regular["derivative_source"]
    reconstructed = (
        radius * shat0[0],
        radius * shat0[1],
        t * shat1[0],
        t * shat1[1],
    )
    expected = (
        physical["radial_field_coefficient"],
        physical["tangential_field_coefficient"],
        physical["radial_field_derivative_coefficient"],
        physical["tangential_field_derivative_coefficient"],
    )
    assert reconstructed == pytest.approx(expected, rel=2e-11, abs=2e-11)


def test_exact_origin_blocks_equal_established_indicial_hessian() -> None:
    slope = 3
    regular = regular_conormal_data(
        t=0.0,
        curvature=1 / 400,
        profile_deficit_over_radius=float(slope),
        profile_deficit_time_derivative=0.0,
        pion_mass=1.0,
    )
    leading = centrifugal_origin_leading_hessian()
    expected = tuple(
        tuple(
            sum(
                float(coefficient) * slope**power
                for power, coefficient in enumerate(entry)
            )
            for entry in row
        )
        for row in leading
    )
    actual = (
        (*regular["coordinate"][0], *regular["mixed"][0]),
        (*regular["coordinate"][1], *regular["mixed"][1]),
        (
            regular["mixed"][0][0],
            regular["mixed"][1][0],
            *regular["principal"][0],
        ),
        (
            regular["mixed"][0][1],
            regular["mixed"][1][1],
            *regular["principal"][1],
        ),
    )
    for expected_row, actual_row in zip(expected, actual, strict=True):
        assert actual_row == pytest.approx(expected_row, abs=1e-12)
    assert regular["coordinate_source"] == (0.0, 0.0)
    assert regular["derivative_source"] == (0.0, 0.0)


def test_zero_radius_kernel_limit_matches_sine_limit() -> None:
    slope = 1.6
    tiny = 1e-12
    record = regular_conormal_data(
        t=tiny,
        curvature=0.0,
        profile_deficit_over_radius=slope,
        profile_deficit_time_derivative=0.0,
        pion_mass=0.0,
    )
    assert record["sine_over_radius"] == pytest.approx(
        sin(slope * tiny**0.5) / tiny**0.5
    )


def test_exact_formal_fuchs_and_germ_checks() -> None:
    checks = exact_formal_conormal_checks()
    assert checks["fuchs_constant_matches_established_a0"]
    assert checks["source_constant_vanishes"]
    assert checks["conormal_residual_divisible_by_t_cubed"] == {
        "linear_homogeneous": True,
        "cubic_homogeneous": True,
        "forced_particular": True,
    }
    assert checks["all_checks_pass"]


def test_input_validation() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        regular_conormal_data(
            t=-1.0,
            curvature=0.0,
            profile_deficit_over_radius=1.0,
            profile_deficit_time_derivative=0.0,
            pion_mass=1.0,
        )
