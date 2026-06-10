from fractions import Fraction
from types import SimpleNamespace

from experiments.skyrmion_newton_linearization_audit import (
    admissible_newton_tube_radii,
    newton_tube_feasibility_margin,
    select_best_newton_tube,
)


def test_newton_tube_radii_stop_when_z0_cannot_contract() -> None:
    assert admissible_newton_tube_radii(
        (Fraction(1, 100), Fraction(1, 10)),
        newton_defect_upper_bound=Fraction(1, 1000),
        z0_upper_bound=Fraction(1),
    ) == ()


def test_newton_tube_radii_remove_impossible_linearized_radii() -> None:
    assert admissible_newton_tube_radii(
        (Fraction(1, 1000), Fraction(1, 100), Fraction(1, 10)),
        newton_defect_upper_bound=Fraction(1, 100),
        z0_upper_bound=Fraction(1, 2),
    ) == (Fraction(1, 10),)


def test_newton_tube_radii_remain_inside_origin_sensitivity_family() -> None:
    assert admissible_newton_tube_radii(
        (Fraction(1, 100), Fraction(1, 50), Fraction(1, 40)),
        newton_defect_upper_bound=Fraction(1, 1000),
        z0_upper_bound=Fraction(0),
        maximum_radius=Fraction(1, 50),
    ) == (Fraction(1, 100), Fraction(1, 50))


def _tube(
    *,
    radius: Fraction,
    radii_polynomial: Fraction,
    contraction: Fraction,
) -> SimpleNamespace:
    return SimpleNamespace(
        radius=radius,
        radii_polynomial_upper_bound=radii_polynomial,
        contraction_upper_bound=contraction,
    )


def test_best_tube_prefers_joint_closure_over_more_negative_polynomial() -> None:
    contraction_failure = _tube(
        radius=Fraction(1, 10),
        radii_polynomial=Fraction(-1, 20),
        contraction=Fraction(11, 10),
    )
    closed = _tube(
        radius=Fraction(1, 20),
        radii_polynomial=Fraction(-1, 100),
        contraction=Fraction(9, 10),
    )

    assert select_best_newton_tube((contraction_failure, closed)) is closed
    assert newton_tube_feasibility_margin(closed) < 0


def test_best_tube_compares_candidates_across_norm_weights() -> None:
    minimum_z0_proxy_failure = _tube(
        radius=Fraction(1, 100),
        radii_polynomial=Fraction(1, 1000),
        contraction=Fraction(1, 2),
    )
    larger_z0_but_closed = _tube(
        radius=Fraction(1, 100),
        radii_polynomial=Fraction(-1, 1000),
        contraction=Fraction(3, 4),
    )

    assert (
        select_best_newton_tube(
            (minimum_z0_proxy_failure, larger_z0_but_closed)
        )
        is larger_z0_but_closed
    )
