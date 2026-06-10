"""Static even-parity quadrupole response on fixed pure de Sitter.

For the gauge-invariant Zerilli-Moncrief master field in the pure de Sitter
static patch, the zero-frequency ``l=2`` equation is

    A_2 Psi = F,
    A_2 = -d/dr[(1-r^2/R^2)d/dr] + 6/r^2.

The Friedrichs boundary conditions are ``Psi=O(r^3)`` at the center and
``f Psi' -> 0`` at the horizon.  This module implements the exact homogeneous
solutions, positive Green kernel, coercive ``L2(dr)`` response bound, and the
logarithmic near-horizon susceptibility.

The source ``F`` is the conserved Zerilli master source.  It is not determined
by the energy-density multipole alone.
"""

from __future__ import annotations

from math import acos, atanh, isfinite, log


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_unit_interval(name: str, value: float, *, include_zero: bool) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    lower_ok = value >= 0.0 if include_zero else value > 0.0
    if not lower_ok or value >= 1.0:
        interval = "[0,1)" if include_zero else "(0,1)"
        raise ValueError(f"{name} must lie in {interval}")


def _regular_series(x: float, *, derivative: bool) -> float:
    """Evaluate the center-regular solution or its derivative by recurrence."""
    coefficient = 1.0
    power = 3
    total = 0.0
    for _ in range(1000):
        term = (
            coefficient * power * x ** (power - 1)
            if derivative
            else coefficient * x**power
        )
        total += term
        if abs(term) <= 1.0e-18 * max(1.0, abs(total)):
            break
        coefficient *= power * (power + 1) / ((power + 4) * (power - 1))
        power += 2
    return total


def l2_center_regular_solution(radius_ratio: float) -> float:
    """Return ``u(x)``, normalized by ``u(x)=x^3+O(x^5)`` at the center."""
    _validate_unit_interval("radius_ratio", radius_ratio, include_zero=True)
    x = radius_ratio
    if x == 0.0:
        return 0.0
    if x < 0.25:
        return _regular_series(x, derivative=False)
    return 15.0 * (3.0 - x * x) * atanh(x) / (4.0 * x * x) - 45.0 / (4.0 * x)


def l2_center_regular_solution_derivative(radius_ratio: float) -> float:
    """Return ``du/dx`` for the center-regular homogeneous solution."""
    _validate_unit_interval("radius_ratio", radius_ratio, include_zero=True)
    x = radius_ratio
    if x == 0.0:
        return 0.0
    if x < 0.25:
        return _regular_series(x, derivative=True)
    coefficient = 3.0 / (x * x) - 1.0
    return 15.0 / 4.0 * (
        -6.0 * atanh(x) / x**3 + coefficient / (1.0 - x * x)
    ) + 45.0 / (4.0 * x * x)


def l2_horizon_regular_solution(radius_ratio: float) -> float:
    """Return ``v(x)=(3-x^2)/(2x^2)``, normalized by ``v(1)=1``."""
    _validate_unit_interval("radius_ratio", radius_ratio, include_zero=False)
    x = radius_ratio
    return (3.0 - x * x) / (2.0 * x * x)


def l2_horizon_regular_solution_derivative(radius_ratio: float) -> float:
    """Return ``dv/dx=-3/x^3``."""
    _validate_unit_interval("radius_ratio", radius_ratio, include_zero=False)
    return -3.0 / radius_ratio**3


def l2_dimensionless_wronskian(radius_ratio: float) -> float:
    """Return ``(1-x^2)(u v'-u' v)``, identically ``-15/2``."""
    _validate_unit_interval("radius_ratio", radius_ratio, include_zero=False)
    x = radius_ratio
    u = l2_center_regular_solution(x)
    du = l2_center_regular_solution_derivative(x)
    v = l2_horizon_regular_solution(x)
    dv = l2_horizon_regular_solution_derivative(x)
    return (1.0 - x * x) * (u * dv - du * v)


def static_patch_l2_green_kernel(
    radius: float,
    source_radius: float,
    *,
    static_patch_radius: float,
) -> float:
    """Return the positive center/no-log-horizon Green kernel ``G_2(r,s)``."""
    _validate_positive("static_patch_radius", static_patch_radius)
    for name, value in (("radius", radius), ("source_radius", source_radius)):
        if not isfinite(value) or not 0.0 < value < static_patch_radius:
            raise ValueError(f"{name} must lie strictly inside the static patch")
    inner = min(radius, source_radius) / static_patch_radius
    outer = max(radius, source_radius) / static_patch_radius
    return (
        2.0
        * static_patch_radius
        / 15.0
        * l2_center_regular_solution(inner)
        * l2_horizon_regular_solution(outer)
    )


def static_patch_l2_coercive_response_record(
    source_l2_norm: float,
    *,
    static_patch_radius: float,
) -> dict[str, float | str]:
    """Return the exact ``A_2>=6/R^2`` resolvent and form-energy bounds."""
    if not isfinite(source_l2_norm) or source_l2_norm < 0.0:
        raise ValueError("source_l2_norm must be finite and nonnegative")
    _validate_positive("static_patch_radius", static_patch_radius)
    inverse_gap = static_patch_radius**2 / 6.0
    return {
        "source_L2_dr_norm": source_l2_norm,
        "operator_lower_bound": 6.0 / static_patch_radius**2,
        "inverse_operator_norm_upper_bound": inverse_gap,
        "master_field_L2_dr_norm_upper_bound": inverse_gap * source_l2_norm,
        "master_form_energy_upper_bound": inverse_gap * source_l2_norm**2,
        "theorem": (
            "The Friedrichs quadratic form is integral[f|Psi'|^2+"
            "6|Psi|^2/r^2]dr and is at least (6/R^2)||Psi||_2^2."
        ),
    }


def proper_horizon_distance(
    radius: float,
    *,
    static_patch_radius: float,
) -> float:
    """Return the static-slice proper distance ``rho=R arccos(r/R)``."""
    _validate_positive("static_patch_radius", static_patch_radius)
    if not isfinite(radius) or not 0.0 <= radius < static_patch_radius:
        raise ValueError("radius must lie in the static patch")
    return static_patch_radius * acos(radius / static_patch_radius)


def static_patch_l2_diagonal_susceptibility(
    radius: float,
    *,
    static_patch_radius: float,
) -> float:
    """Return ``G_2(r,r)`` for a point master source."""
    return static_patch_l2_green_kernel(
        radius,
        radius,
        static_patch_radius=static_patch_radius,
    )


def static_patch_l2_renormalized_horizon_susceptibility(
    radius: float,
    *,
    static_patch_radius: float,
) -> float:
    """Return ``G_2(r,r)/R-log(2R/rho)``, which tends to ``-3/2``."""
    susceptibility = static_patch_l2_diagonal_susceptibility(
        radius,
        static_patch_radius=static_patch_radius,
    )
    distance = proper_horizon_distance(
        radius,
        static_patch_radius=static_patch_radius,
    )
    return susceptibility / static_patch_radius - log(
        2.0 * static_patch_radius / distance
    )


def static_patch_l2_response_certificate() -> dict[str, object]:
    """Audit the exact Green kernel and response bounds."""
    sample_points = (0.05, 0.2, 0.5, 0.8, 0.95)
    wronskians = tuple(l2_dimensionless_wronskian(x) for x in sample_points)
    greens = tuple(
        static_patch_l2_green_kernel(x, 0.6, static_patch_radius=1.0)
        for x in sample_points
    )
    jump_point = 0.6
    u = l2_center_regular_solution(jump_point)
    du = l2_center_regular_solution_derivative(jump_point)
    v = l2_horizon_regular_solution(jump_point)
    dv = l2_horizon_regular_solution_derivative(jump_point)
    derivative_jump = 2.0 * (u * dv - du * v) / 15.0
    normalized_jump = -(1.0 - jump_point**2) * derivative_jump
    horizon_ratio = 1.0 - 1.0e-9
    renormalized = static_patch_l2_renormalized_horizon_susceptibility(
        horizon_ratio,
        static_patch_radius=1.0,
    )
    coercive = static_patch_l2_coercive_response_record(
        3.0,
        static_patch_radius=2.0,
    )
    claims = {
        "center_solution_has_cubic_normalization": abs(
            l2_center_regular_solution(1.0e-4) / 1.0e-12 - 1.0
        )
        < 1.0e-7,
        "wronskian_is_minus_fifteen_over_two": all(
            abs(value + 7.5) < 1.0e-10 for value in wronskians
        ),
        "green_kernel_is_positive": all(value > 0.0 for value in greens),
        "green_kernel_has_unit_flux_jump": abs(normalized_jump - 1.0) < 1.0e-10,
        "coercive_inverse_bound_is_R_squared_over_six": abs(
            coercive["inverse_operator_norm_upper_bound"] - 2.0 / 3.0
        )
        < 1.0e-15,
        "near_horizon_susceptibility_has_logarithmic_finite_part": abs(
            renormalized + 1.5
        )
        < 1.0e-6,
    }
    return {
        "goal": "Static-Patch Quadrupole Einstein Master Response",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "fixed_de_sitter_static_l2_zerilli_resolvent",
        "operator": "A_2=-d/dr[(1-r^2/R^2)d/dr]+6/r^2",
        "boundary_conditions": (
            "Psi=O(r^3) at the center and f Psi'->0 at the horizon; the "
            "Friedrichs domain excludes the logarithmic horizon branch"
        ),
        "sample_wronskians": wronskians,
        "unit_flux_jump": normalized_jump,
        "coercive_response": coercive,
        "renormalized_horizon_susceptibility": renormalized,
        "certified_claims": claims,
        "observable_prediction": (
            "For master sources moved toward the horizon, the diagonal static "
            "susceptibility grows as R log(2R/rho)-3R/2+o(R), where rho is "
            "proper horizon distance."
        ),
        "claim_boundary": (
            "Fixed pure de Sitter, linearized, static, even parity, l=2, and a "
            "conserved compact master source. This is not a response theorem "
            "for the energy density alone, the non-negligibly deformed "
            "Skyrmion background, or the membrane-completed stress tensor."
        ),
    }
