from math import isclose

import pytest

from qgtoy.static_patch_l2_response import (
    l2_center_regular_solution,
    l2_center_regular_solution_derivative,
    l2_dimensionless_wronskian,
    l2_horizon_regular_solution,
    l2_horizon_regular_solution_derivative,
    proper_horizon_distance,
    static_patch_l2_coercive_response_record,
    static_patch_l2_diagonal_susceptibility,
    static_patch_l2_green_kernel,
    static_patch_l2_renormalized_horizon_susceptibility,
    static_patch_l2_response_certificate,
)


def test_exact_homogeneous_solutions_and_wronskian() -> None:
    assert l2_center_regular_solution(0.0) == 0.0
    assert l2_center_regular_solution_derivative(0.0) == 0.0
    assert l2_center_regular_solution(1.0e-4) == pytest.approx(1.0e-12)
    for x in (0.05, 0.2, 0.5, 0.8, 0.95):
        assert l2_dimensionless_wronskian(x) == pytest.approx(-7.5, abs=1.0e-10)
        assert l2_center_regular_solution(x) > 0.0
        assert l2_horizon_regular_solution(x) > 0.0


def test_green_kernel_is_symmetric_positive_and_has_unit_jump() -> None:
    first = static_patch_l2_green_kernel(0.3, 0.7, static_patch_radius=1.0)
    second = static_patch_l2_green_kernel(0.7, 0.3, static_patch_radius=1.0)
    assert first == pytest.approx(second)
    assert first > 0.0

    x = 0.6
    u = l2_center_regular_solution(x)
    du = l2_center_regular_solution_derivative(x)
    v = l2_horizon_regular_solution(x)
    dv = l2_horizon_regular_solution_derivative(x)
    derivative_jump = 2.0 * (u * dv - du * v) / 15.0
    assert -(1.0 - x * x) * derivative_jump == pytest.approx(1.0)


def test_coercive_response_bound() -> None:
    record = static_patch_l2_coercive_response_record(
        3.0,
        static_patch_radius=2.0,
    )
    assert record["operator_lower_bound"] == pytest.approx(1.5)
    assert record["inverse_operator_norm_upper_bound"] == pytest.approx(2.0 / 3.0)
    assert record["master_field_L2_dr_norm_upper_bound"] == pytest.approx(2.0)
    assert record["master_form_energy_upper_bound"] == pytest.approx(6.0)


def test_near_horizon_logarithmic_susceptibility() -> None:
    remainders = tuple(
        static_patch_l2_renormalized_horizon_susceptibility(
            1.0 - epsilon,
            static_patch_radius=1.0,
        )
        for epsilon in (1.0e-4, 1.0e-6, 1.0e-8)
    )
    assert abs(remainders[-1] + 1.5) < abs(remainders[0] + 1.5)
    assert remainders[-1] == pytest.approx(-1.5, abs=1.0e-5)
    assert static_patch_l2_diagonal_susceptibility(
        1.0 - 1.0e-8,
        static_patch_radius=1.0,
    ) > static_patch_l2_diagonal_susceptibility(
        0.9,
        static_patch_radius=1.0,
    )


def test_proper_horizon_distance() -> None:
    assert proper_horizon_distance(0.0, static_patch_radius=2.0) == pytest.approx(
        3.141592653589793
    )
    assert proper_horizon_distance(1.9, static_patch_radius=2.0) > 0.0


def test_certificate_passes() -> None:
    certificate = static_patch_l2_response_certificate()
    assert certificate["status"] == "pass"
    assert all(certificate["certified_claims"].values())


@pytest.mark.parametrize(
    ("radius", "source_radius", "patch_radius"),
    ((0.0, 0.5, 1.0), (0.5, 1.0, 1.0), (0.5, 0.6, 0.0)),
)
def test_invalid_green_kernel_inputs_are_rejected(
    radius: float,
    source_radius: float,
    patch_radius: float,
) -> None:
    with pytest.raises(ValueError):
        static_patch_l2_green_kernel(
            radius,
            source_radius,
            static_patch_radius=patch_radius,
        )


def test_horizon_solution_derivative() -> None:
    x = 0.7
    step = 1.0e-6
    finite_difference = (
        l2_horizon_regular_solution(x + step) - l2_horizon_regular_solution(x - step)
    ) / (2.0 * step)
    assert isclose(
        finite_difference,
        l2_horizon_regular_solution_derivative(x),
        rel_tol=1.0e-9,
    )
