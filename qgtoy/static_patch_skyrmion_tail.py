"""Exact continuum tail theorem for the signed Skyrmion bath factor.

The finite radial trapezoid used for frequency-window diagnostics has an
artificial oscillatory tail.  This module instead records the half-interval
continuum integration-by-parts argument.  It proves global ``H^2`` membership
for the exact hard-wall profile and exposes the six derivative norms needed
for an explicit numerical upper enclosure.

The default endpoint record is floating-point shooting evidence.  It is not an
interval enclosure of the profile, inertia, or derivative norms.
"""

from __future__ import annotations

from math import atanh, isfinite, pi, sqrt, tanh

from .massive_skyrmion_profile import dimensionless_inertia_density
from .massive_skyrmion_worldtube import solve_hard_wall_skyrmion_profile


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_three_nonnegative(
    name: str,
    values: tuple[float, float, float],
) -> None:
    if len(values) != 3:
        raise ValueError(f"{name} must contain three entries")
    for index, value in enumerate(values):
        _validate_nonnegative(f"{name}[{index}]", value)


def skyrmion_optical_endpoint_record(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, float]:
    """Return floating endpoint jets entering the exact continuum theorem.

    With ``x=tanh(y)/sqrt(curvature)``, define

    ``W=(rho_I/x^2) dx/dy`` and ``A=W coth(y)``.

    The exact profile has ``W=w0 y^2+O(y^4)`` at the origin and
    ``W=(W''(Y)/2)(Y-y)^2+O((Y-y)^3)`` at the wall.  The returned values are
    evaluated from the current floating shooting solution and are diagnostics,
    not directed interval bounds.
    """
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("step", step)
    horizon_margin = 1.0 - curvature * wall_radius**2
    if horizon_margin <= 0.0:
        raise ValueError("wall must lie strictly inside the horizon")

    shooting_slope, points = solve_hard_wall_skyrmion_profile(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    inertia_values = tuple(
        dimensionless_inertia_density(
            radius_value,
            profile,
            derivative,
            curvature=curvature,
        )
        for radius_value, profile, derivative in points
    )
    inertia = sum(
        (inertia_values[index] + inertia_values[index + 1])
        * (points[index + 1][0] - points[index][0])
        / 2.0
        for index in range(len(points) - 1)
    )
    root_curvature = sqrt(curvature)
    optical_wall = atanh(root_curvature * wall_radius)
    wall_slope = abs(points[-1][2])
    origin_weight_coefficient = (
        2.0
        * pi
        * shooting_slope**2
        * (1.0 + 8.0 * shooting_slope**2)
        / (3.0 * curvature**1.5)
    )
    wall_weight_second = (
        4.0
        * pi
        * wall_slope**2
        * horizon_margin**2
        * (1.0 + 4.0 * horizon_margin * wall_slope**2)
        / (3.0 * curvature**1.5)
    )
    prefactor = 3.0 / (curvature * inertia)
    return {
        "shooting_slope": shooting_slope,
        "wall_profile_slope_magnitude": wall_slope,
        "optical_wall": optical_wall,
        "horizon_margin": horizon_margin,
        "inertia_quadrature": inertia,
        "form_factor_prefactor": prefactor,
        "origin_weight_quadratic_coefficient": origin_weight_coefficient,
        "origin_weight_second_derivative": 2.0 * origin_weight_coefficient,
        "wall_weight_second_derivative": wall_weight_second,
        "wall_a_second_derivative": wall_weight_second / tanh(optical_wall),
        "leading_form_factor_tail_amplitude": prefactor * wall_weight_second,
        "profile_step": step,
    }


def skyrmion_sharp_form_factor_tail_envelope(
    *,
    prefactor: float,
    optical_wall: float,
    wall_weight_second: float,
    a_third_derivative_l1: tuple[float, float, float],
    w_third_derivative_l1: tuple[float, float, float],
    tail_start: float = 1.0,
    radius: float = 1.0,
) -> dict[str, object]:
    """Return the exact ``p^-5`` and signed-factor tail bounds.

    Entry ``m`` of the two norm tuples must upper-bound
    ``||d_y^3(y^m A)||_1`` or ``||d_y^3(y^m W)||_1`` on ``[0,Y]``.  If the
    prefactor, optical wall, wall second jet, and six supplied norms enter the
    exact mathematical envelope.  This routine evaluates that formula in
    ordinary binary floating point; its outputs are not directed interval
    bounds.  The function does not infer the inputs from a sampled profile.
    """
    _validate_positive("prefactor", prefactor)
    _validate_positive("optical_wall", optical_wall)
    _validate_positive("wall_weight_second", wall_weight_second)
    _validate_positive("tail_start", tail_start)
    _validate_positive("radius", radius)
    if tail_start < 1.0:
        raise ValueError("tail_start must be at least one")
    _validate_three_nonnegative(
        "a_third_derivative_l1",
        a_third_derivative_l1,
    )
    _validate_three_nonnegative(
        "w_third_derivative_l1",
        w_third_derivative_l1,
    )

    coth_wall = 1.0 / tanh(optical_wall)
    b_bounds = tuple(
        optical_wall**order * wall_weight_second
        + w_third_derivative_l1[order]
        for order in range(3)
    )
    d_bounds = tuple(
        optical_wall**order * coth_wall * wall_weight_second
        + a_third_derivative_l1[order]
        for order in range(3)
    )
    split = tail_start
    numerator_bounds = (
        b_bounds[0] + d_bounds[0] / split,
        b_bounds[1]
        + d_bounds[1] / split
        + d_bounds[0] / split**2,
        b_bounds[2]
        + d_bounds[2] / split
        + 2.0 * d_bounds[1] / split**2
        + 2.0 * d_bounds[0] / split**3,
    )
    form_factor_bounds = (
        prefactor * numerator_bounds[0],
        prefactor
        * (numerator_bounds[1] + 2.0 * numerator_bounds[0] / split),
        prefactor
        * (
            numerator_bounds[2]
            + 4.0 * numerator_bounds[1] / split
            + 6.0 * numerator_bounds[0] / split**2
        ),
    )

    bare = (1.0 / 6.0, 81.0 / 480.0, 21.0 / 48.0)
    positive_signed_bounds = (
        bare[0] * form_factor_bounds[0],
        bare[1] * form_factor_bounds[0]
        + bare[0] * form_factor_bounds[1],
        bare[2] * form_factor_bounds[0]
        + 2.0 * bare[1] * form_factor_bounds[1]
        + bare[0] * form_factor_bounds[2],
    )
    negative_signed_bounds = (
        positive_signed_bounds[0],
        pi * positive_signed_bounds[0] + positive_signed_bounds[1],
        positive_signed_bounds[2]
        + 2.0 * pi * positive_signed_bounds[1]
        + pi**2 * positive_signed_bounds[0],
    )
    squared_dimensionless_tail_bounds = tuple(
        (
            positive_signed_bounds[order] ** 2
            + negative_signed_bounds[order] ** 2
        )
        / (6.0 * split**6)
        for order in range(3)
    )
    squared_physical_tail_bounds = tuple(
        squared_dimensionless_tail_bounds[order]
        * radius ** (2 * order - 4)
        for order in range(3)
    )
    return {
        "result_type": "float_evaluation_of_exact_p_minus_five_envelope",
        "tail_start": tail_start,
        "b_transform_bounds": b_bounds,
        "d_transform_bounds": d_bounds,
        "numerator_derivative_coefficients": numerator_bounds,
        "form_factor_derivative_coefficients": form_factor_bounds,
        "positive_signed_factor_coefficients": positive_signed_bounds,
        "negative_signed_factor_coefficients": negative_signed_bounds,
        "squared_dimensionless_h2_tail_bounds": (
            squared_dimensionless_tail_bounds
        ),
        "squared_physical_h2_tail_bounds": squared_physical_tail_bounds,
        "form_factor_decay": "|H^(k)(p)| <= h_k p^-5 for k=0,1,2",
        "signed_factor_decay": "|q^(k)(p)| <= c_k p^-7/2 for k=0,1,2",
    }


def static_patch_skyrmion_tail_certificate(
    *,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    step: float = 0.002,
) -> dict[str, object]:
    """Audit the exact continuum tail theorem and its numerical boundary."""
    endpoint = skyrmion_optical_endpoint_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
        step=step,
    )
    executable_checks = {
        "floating_origin_coefficient_is_positive": (
            endpoint["origin_weight_quadratic_coefficient"] > 0.0
        ),
        "floating_wall_second_jet_is_positive": (
            endpoint["wall_weight_second_derivative"] > 0.0
        ),
        "floating_tail_amplitude_is_positive": (
            endpoint["leading_form_factor_tail_amplitude"] > 0.0
        ),
    }
    return {
        "goal": "Exact Continuum Skyrmion Signed-Factor Tail Gate",
        "status": "pass" if all(executable_checks.values()) else "fail",
        "result_type": "analytic_global_h2_theorem_with_open_interval_constants",
        "central_result": (
            "The exact hard-wall optical weights have the endpoint traces "
            "needed for three half-interval integrations by parts. Therefore "
            "H_Sky and its first two derivatives are O(p^-5), sharply set by "
            "the wall second jet, and the real signed factor belongs globally "
            "to H^2."
        ),
        "endpoint_record": endpoint,
        "required_rigorous_inputs": (
            "an interval lower bound on the inertia, outward enclosures of Y "
            "and W''(Y) sufficient for Y^m coth(Y)W''(Y), and interval upper "
            "bounds on ||d_y^3(y^m A)||_1 and ||d_y^3(y^m W)||_1 for m=0,1,2"
        ),
        "required_derivative_norm_count": 6,
        "analytic_theorem_results": (
            "the endpoint expansions close the half-interval three-IBP bound",
            "H_Sky and its first two derivatives are O(p^-5)",
            "the exact real signed factor belongs globally to H^2",
        ),
        "executable_checks": executable_checks,
        "claim_boundary": (
            "Global H2 membership is an analytic exact-profile statement. "
            "The displayed endpoint numbers come from floating RK4 shooting "
            "and trapezoid inertia quadrature. They are not directed interval "
            "bounds, and no rigorous numerical global Sobolev constant or ULE "
            "coupling cap is claimed. A validated interval shooting and ODE-AD "
            "implementation remains required for those constants."
        ),
        "next_physics_gate": (
            "certify the six continuum derivative norms by interval ODE "
            "bounds, then solve the genuine held-off-center deformation"
        ),
    }
