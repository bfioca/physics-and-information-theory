"""Exploratory global-BVP coercivity probe for the hard-wall Skyrmion.

This is deliberately outside the trusted validation modules.  It evaluates the
floating profile, its self-adjoint Euler-Lagrange Jacobi operator on [1/16, 4],
finite-difference Dirichlet eigenvalues, rational Barta comparison functions,
and the scalar Schur complement for the augmented (b, F) boundary-value map.

The output is diagnostic floating-point evidence, not a validated certificate.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import cos, pi, sin

from qgtoy.massive_skyrmion_worldtube import (
    curved_profile_acceleration,
    origin_cubic_coefficient,
    solve_hard_wall_skyrmion_profile,
)


LEFT = 1.0 / 16.0
RIGHT = 4.0
MU = 1.0
CURVATURE = 1.0 / 400.0


@dataclass(frozen=True)
class JacobiSample:
    x: float
    profile: float
    derivative: float
    p: float
    p_derivative: float
    q: float


def jacobi_sample(x: float, profile: float, derivative: float) -> JacobiSample:
    """Return coefficients of A eta = -(P eta')' + Q eta.

    The operator is the second variation of four times the reduced energy.
    Differentiating the mixed Hessian term and using the profile equation gives

        P = N (x^2 + 8 sin(F)^2),
        Q = 4 V_FF - 8 (N sin(2F) F')' + 8 N cos(2F) F'^2.

    The expanded expression below avoids numerical differentiation.
    """
    lapse = 1.0 - CURVATURE * x * x
    lapse_derivative = -2.0 * CURVATURE * x
    sine = sin(profile)
    cosine = cos(profile)
    sine_twice = sin(2.0 * profile)
    cosine_twice = cos(2.0 * profile)
    u = x * x + 8.0 * sine * sine
    p = lapse * u
    p_derivative = lapse_derivative * u + lapse * (
        2.0 * x + 8.0 * sine_twice * derivative
    )
    acceleration = curved_profile_acceleration(
        x,
        profile,
        derivative,
        pion_mass=MU,
        curvature=CURVATURE,
    )
    four_v_ff = (
        2.0 * cosine_twice
        + (24.0 * sine * sine * cosine * cosine - 8.0 * sine**4) / (x * x)
        + MU * MU * x * x * cosine
    )
    q = (
        four_v_ff
        - 8.0 * lapse_derivative * sine_twice * derivative
        - 8.0 * lapse * sine_twice * acceleration
        - 8.0 * lapse * cosine_twice * derivative * derivative
    )
    return JacobiSample(x, profile, derivative, p, p_derivative, q)


def _sturm_count(diagonal: list[float], off_diagonal: list[float], value: float) -> int:
    """Count eigenvalues below value using a stabilized LDL Sturm sequence."""
    tiny = 1.0e-300
    pivot = diagonal[0] - value
    count = int(pivot < 0.0)
    for index, off in enumerate(off_diagonal, start=1):
        if abs(pivot) < tiny:
            pivot = -tiny if pivot < 0.0 else tiny
        pivot = diagonal[index] - value - off * off / pivot
        count += int(pivot < 0.0)
    return count


def smallest_discrete_eigenvalue(samples: list[JacobiSample], stride: int) -> float:
    """Second-order flux finite-difference estimate of the first eigenvalue."""
    selected = samples[::stride]
    if selected[-1].x != samples[-1].x:
        selected.append(samples[-1])
    h = selected[1].x - selected[0].x
    interior = selected[1:-1]
    p_half = [
        0.5 * (selected[index].p + selected[index + 1].p)
        for index in range(len(selected) - 1)
    ]
    diagonal = [
        (p_half[index] + p_half[index + 1]) / (h * h) + sample.q
        for index, sample in enumerate(interior)
    ]
    off_diagonal = [
        -p_half[index + 1] / (h * h)
        for index in range(len(interior) - 1)
    ]
    lower = min(
        diagonal[index]
        - (abs(off_diagonal[index - 1]) if index else 0.0)
        - (abs(off_diagonal[index]) if index < len(off_diagonal) else 0.0)
        for index in range(len(diagonal))
    )
    upper = min(diagonal)
    while _sturm_count(diagonal, off_diagonal, upper) == 0:
        upper = 2.0 * upper - lower + 1.0
    for _ in range(90):
        middle = 0.5 * (lower + upper)
        if _sturm_count(diagonal, off_diagonal, middle) == 0:
            lower = middle
        else:
            upper = middle
    return 0.5 * (lower + upper)


def barta_lower_bound(
    samples: list[JacobiSample], *, alpha: float, power: int
) -> tuple[float, float]:
    """Sample inf A(v)/v for v=t(L-t)/(1+alpha*t)^power."""
    length = RIGHT - LEFT
    minimum = float("inf")
    location = float("nan")
    for sample in samples[1:-1]:
        t = sample.x - LEFT
        g = t * (length - t)
        g_log_derivative = (length - 2.0 * t) / g
        denominator = 1.0 + alpha * t
        weight_log_derivative = -power * alpha / denominator
        v_log_derivative = g_log_derivative + weight_log_derivative
        v_second_over_v = (
            -2.0 / g
            + 2.0 * g_log_derivative * weight_log_derivative
            + power * (power + 1.0) * alpha * alpha / denominator**2
        )
        quotient = (
            -sample.p * v_second_over_v
            - sample.p_derivative * v_log_derivative
            + sample.q
        )
        if quotient < minimum:
            minimum = quotient
            location = sample.x
    return minimum, location


def quadratic_barta_lower_bound(
    samples: list[JacobiSample],
    *,
    alpha: float,
    beta: float,
    power: int,
) -> tuple[float, float] | None:
    """Sample a two-parameter rational Barta comparison.

    Here v=t(L-t)/(1+alpha*t+beta*t^2)^power.  The quadratic denominator
    lets the logarithmic slope be strongly negative at the left endpoint and
    recover before the right endpoint, which the one-pole family cannot do.
    """
    length = RIGHT - LEFT
    minimum = float("inf")
    location = float("nan")
    for sample in samples[1:-1]:
        t = sample.x - LEFT
        g = t * (length - t)
        denominator = 1.0 + alpha * t + beta * t * t
        if denominator <= 0.0:
            return None
        denominator_derivative = alpha + 2.0 * beta * t
        g_log_derivative = (length - 2.0 * t) / g
        weight_log_derivative = -power * denominator_derivative / denominator
        weight_second_over_weight = (
            -2.0 * power * beta / denominator
            + power
            * (power + 1.0)
            * denominator_derivative
            * denominator_derivative
            / denominator**2
        )
        v_log_derivative = g_log_derivative + weight_log_derivative
        v_second_over_v = (
            -2.0 / g
            + 2.0 * g_log_derivative * weight_log_derivative
            + weight_second_over_weight
        )
        quotient = (
            -sample.p * v_second_over_v
            - sample.p_derivative * v_log_derivative
            + sample.q
        )
        if quotient < minimum:
            minimum = quotient
            location = sample.x
    return minimum, location


def positive_quadratic_barta_lower_bound(
    samples: list[JacobiSample],
    *,
    alpha: float,
    beta: float,
    power: int,
) -> tuple[float, float] | None:
    """Sample v=(1+alpha*t+beta*t^2)^(-power), positive at both ends."""
    minimum = float("inf")
    location = float("nan")
    for sample in samples:
        t = sample.x - LEFT
        denominator = 1.0 + alpha * t + beta * t * t
        if denominator <= 0.0:
            return None
        denominator_derivative = alpha + 2.0 * beta * t
        v_log_derivative = -power * denominator_derivative / denominator
        v_second_over_v = (
            -2.0 * power * beta / denominator
            + power
            * (power + 1.0)
            * denominator_derivative
            * denominator_derivative
            / denominator**2
        )
        quotient = (
            -sample.p * v_second_over_v
            - sample.p_derivative * v_log_derivative
            + sample.q
        )
        if quotient < minimum:
            minimum = quotient
            location = sample.x
    return minimum, location


def _origin_data(slope: float, x: float) -> tuple[float, float]:
    cubic = origin_cubic_coefficient(
        slope, pion_mass=MU, curvature=CURVATURE
    )
    return (
        pi - slope * x + cubic * x**3,
        -slope + 3.0 * cubic * x**2,
    )


def _rk4_variation(
    samples: list[JacobiSample], initial_value: float, initial_derivative: float
) -> tuple[float, float]:
    """Integrate A y=0 using linearly interpolated floating coefficients."""
    value = initial_value
    derivative = initial_derivative
    for left, right in zip(samples, samples[1:]):
        h = right.x - left.x

        def coefficients(theta: float) -> tuple[float, float, float]:
            p = left.p + theta * (right.p - left.p)
            p_derivative = left.p_derivative + theta * (
                right.p_derivative - left.p_derivative
            )
            q = left.q + theta * (right.q - left.q)
            return p, p_derivative, q

        def rhs(theta: float, y: float, y_derivative: float) -> tuple[float, float]:
            p, p_derivative, q = coefficients(theta)
            return y_derivative, (q * y - p_derivative * y_derivative) / p

        k1 = rhs(0.0, value, derivative)
        k2 = rhs(0.5, value + h * k1[0] / 2.0, derivative + h * k1[1] / 2.0)
        k3 = rhs(0.5, value + h * k2[0] / 2.0, derivative + h * k2[1] / 2.0)
        k4 = rhs(1.0, value + h * k3[0], derivative + h * k3[1])
        value += h * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]) / 6.0
        derivative += h * (
            k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]
        ) / 6.0
    return value, derivative


def _origin_sensitivity(slope: float, x: float) -> tuple[float, float]:
    width = 1.0e-5
    plus = _origin_data(slope + width, x)
    minus = _origin_data(slope - width, x)
    return (
        (plus[0] - minus[0]) / (2.0 * width),
        (plus[1] - minus[1]) / (2.0 * width),
    )


def probe(step: float) -> dict[str, object]:
    slope, points = solve_hard_wall_skyrmion_profile(
        pion_mass=MU,
        curvature=CURVATURE,
        wall_radius=RIGHT,
        step=step,
        origin_cutoff=step,
    )
    start = next(index for index, point in enumerate(points) if abs(point[0] - LEFT) < 1e-12)
    samples = [jacobi_sample(*point) for point in points[start:]]

    eigenvalues: dict[str, float] = {}
    interval_count = len(samples) - 1
    for requested_intervals in (525, 875, 1575, 2625, interval_count):
        if interval_count % requested_intervals == 0:
            stride = interval_count // requested_intervals
            eigenvalues[str(requested_intervals)] = smallest_discrete_eigenvalue(
                samples, stride
            )

    best = (-float("inf"), 0.0, 0, 0.0)
    trials: list[dict[str, float | int]] = []
    for power in range(1, 9):
        for exponent_index in range(161):
            alpha = 10.0 ** (-1.0 + 3.0 * exponent_index / 160.0)
            bound, location = barta_lower_bound(samples, alpha=alpha, power=power)
            if bound > best[0]:
                best = (bound, alpha, power, location)
        trials.append(
            {
                "power": power,
                "best_bound_so_far": best[0],
                "alpha": best[1],
                "minimum_location": best[3],
            }
        )

    quadratic_best = (-float("inf"), 0.0, 0.0, 0, 0.0)
    search_samples = samples[:20] + samples[20:-20:10] + samples[-20:]
    if search_samples[-1] is not samples[-1]:
        search_samples.append(samples[-1])
    for power in range(1, 5):
        for alpha_index in range(71):
            alpha = 10.0 + 0.5 * alpha_index
            for beta_index in range(81):
                beta = -8.0 + 0.125 * beta_index
                result = quadratic_barta_lower_bound(
                    search_samples,
                    alpha=alpha,
                    beta=beta,
                    power=power,
                )
                if result is None:
                    continue
                bound, location = result
                if bound > quadratic_best[0]:
                    quadratic_best = (bound, alpha, beta, power, location)
    refined_quadratic = quadratic_barta_lower_bound(
        samples,
        alpha=quadratic_best[1],
        beta=quadratic_best[2],
        power=quadratic_best[3],
    )
    assert refined_quadratic is not None
    quadratic_best = (
        refined_quadratic[0],
        quadratic_best[1],
        quadratic_best[2],
        quadratic_best[3],
        refined_quadratic[1],
    )

    positive_best = (-float("inf"), 0.0, 0.0, 0, 0.0)
    for power in range(1, 7):
        for alpha_index in range(81):
            alpha = -2.0 + 0.25 * alpha_index
            for beta_index in range(81):
                beta = -4.0 + 0.125 * beta_index
                result = positive_quadratic_barta_lower_bound(
                    search_samples,
                    alpha=alpha,
                    beta=beta,
                    power=power,
                )
                if result is None:
                    continue
                bound, location = result
                if bound > positive_best[0]:
                    positive_best = (bound, alpha, beta, power, location)
    refined_positive = positive_quadratic_barta_lower_bound(
        samples,
        alpha=positive_best[1],
        beta=positive_best[2],
        power=positive_best[3],
    )
    assert refined_positive is not None
    positive_best = (
        refined_positive[0],
        positive_best[1],
        positive_best[2],
        positive_best[3],
        refined_positive[1],
    )

    phi_b, gamma_b = _origin_sensitivity(slope, LEFT)
    shooting_value, shooting_derivative = _rk4_variation(samples, phi_b, gamma_b)
    dirichlet_fundamental_value, _ = _rk4_variation(samples, 0.0, 1.0)
    schur = -shooting_value / dirichlet_fundamental_value

    return {
        "status": "floating exploratory evidence only",
        "parameters": {
            "mu": MU,
            "curvature": CURVATURE,
            "left": LEFT,
            "right": RIGHT,
            "profile_step": step,
        },
        "shooting_slope": slope,
        "wall_profile": points[-1][1],
        "wall_derivative": points[-1][2],
        "coefficient_ranges": {
            "p": [min(sample.p for sample in samples), max(sample.p for sample in samples)],
            "p_derivative": [
                min(sample.p_derivative for sample in samples),
                max(sample.p_derivative for sample in samples),
            ],
            "q": [min(sample.q for sample in samples), max(sample.q for sample in samples)],
        },
        "dirichlet_smallest_eigenvalue_by_intervals": eigenvalues,
        "best_rational_barta_family": {
            "form": "v=t*(L-t)/(1+alpha*t)^power",
            "sampled_lower_bound": best[0],
            "alpha": best[1],
            "power": best[2],
            "minimum_location": best[3],
        },
        "best_quadratic_rational_barta_family": {
            "form": "v=t*(L-t)/(1+alpha*t+beta*t^2)^power",
            "sampled_lower_bound": quadratic_best[0],
            "alpha": quadratic_best[1],
            "beta": quadratic_best[2],
            "power": quadratic_best[3],
            "minimum_location": quadratic_best[4],
        },
        "best_everywhere_positive_rational_barta_family": {
            "form": "v=1/(1+alpha*t+beta*t^2)^power",
            "sampled_lower_bound": positive_best[0],
            "alpha": positive_best[1],
            "beta": positive_best[2],
            "power": positive_best[3],
            "minimum_location": positive_best[4],
        },
        "barta_search_progress": trials,
        "augmented_schur": {
            "origin_value_derivative_phi_b": phi_b,
            "origin_slope_derivative_gamma_b": gamma_b,
            "shooting_wall_sensitivity": shooting_value,
            "dirichlet_fundamental_wall_value": dirichlet_fundamental_value,
            "schur_value": schur,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--step", type=float, default=0.0005)
    args = parser.parse_args()
    interval_count = round((RIGHT - LEFT) / args.step)
    if abs(LEFT / args.step - round(LEFT / args.step)) > 1e-12:
        raise SystemExit("step must divide 1/16 exactly")
    if abs(interval_count * args.step - (RIGHT - LEFT)) > 1e-12:
        raise SystemExit("step must divide [1/16,4] exactly")
    print(json.dumps(probe(args.step), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
