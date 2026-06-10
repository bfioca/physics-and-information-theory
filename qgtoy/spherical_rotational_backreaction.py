"""Collective rotational backreaction from a spherical radial metric budget.

Assume a fixed spherical Skyrme field and a leading collective rotor.  If the
self-consistent areal metric obeys ``q=2Gm/(rN)<=beta<1``, then ``A>=
(1-beta)N``.  Positivity of the static Skyrme terms gives
``c_M[A]>=(1-beta)c_M[N]``, while the explicit inertia density gives
``c_I[A]<=c_I[N]/(1-beta)``.  The bulk wall constraint therefore bounds

``q_w >= 2G(1-beta)/(R^2 lambda x_w N_w)
         [c_M/e^2 + e^2 Cbar/(2 c_I)]``.

AM-GM eliminates the Skyrme coupling and yields a finite mean-Casimir capacity.
This is a conditional leading-collective spherical theorem, not a rotating
Einstein-Skyrme solution.
"""

from __future__ import annotations

from fractions import Fraction
from math import isfinite, sqrt


def _positive_fraction(name: str, value: Fraction) -> None:
    if not isinstance(value, Fraction) or value <= 0:
        raise ValueError(f"{name} must be a positive Fraction")


def collective_constraint_casimir_capacity(
    *,
    metric_budget: Fraction,
    wall_radius: Fraction,
    curvature: Fraction,
    static_patch_radius_squared_over_newton: Fraction,
    static_mass_lower: Fraction,
    inertia_upper: Fraction,
) -> Fraction:
    """Return the necessary upper bound on ``Cbar=<J^2>``.

    The input mass is the fixed-background bulk static mass, excluding a shell.
    The inertia is the corresponding fixed-background bulk rotor inertia.
    """
    for name, value in (
        ("metric_budget", metric_budget),
        ("wall_radius", wall_radius),
        ("curvature", curvature),
        (
            "static_patch_radius_squared_over_newton",
            static_patch_radius_squared_over_newton,
        ),
        ("static_mass_lower", static_mass_lower),
        ("inertia_upper", inertia_upper),
    ):
        _positive_fraction(name, value)
    if metric_budget >= 1:
        raise ValueError("metric_budget must be smaller than one")
    wall_lapse = 1 - curvature * wall_radius**2
    if wall_lapse <= 0:
        raise ValueError("wall must lie strictly inside the static patch")
    gravitational_coefficient = Fraction(2) / (
        static_patch_radius_squared_over_newton * curvature
    )
    scale = (
        metric_budget
        * wall_radius
        * wall_lapse
        / (gravitational_coefficient * (1 - metric_budget))
    )
    return scale**2 * inertia_upper / (2 * static_mass_lower)


def collective_constraint_orientation_risk_floor(
    maximum_mean_casimir: Fraction,
) -> Fraction:
    """Insert the Casimir capacity into ``R_ref>=1/(16 Cbar+8)``."""
    _positive_fraction("maximum_mean_casimir", maximum_mean_casimir)
    return Fraction(1, 1) / (16 * maximum_mean_casimir + 8)


def collective_constraint_lower_bound(
    mean_casimir: float,
    *,
    metric_budget: float,
    wall_radius: float,
    curvature: float,
    static_patch_radius_squared_over_newton: float,
    static_mass: float,
    inertia: float,
) -> float:
    """Return the coupling-optimized lower bound on the bulk wall ratio."""
    parameters = {
        "mean_casimir": mean_casimir,
        "metric_budget": metric_budget,
        "wall_radius": wall_radius,
        "curvature": curvature,
        "static_patch_radius_squared_over_newton": (
            static_patch_radius_squared_over_newton
        ),
        "static_mass": static_mass,
        "inertia": inertia,
    }
    for name, value in parameters.items():
        if not isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be finite and positive")
    if metric_budget >= 1.0:
        raise ValueError("metric_budget must be smaller than one")
    wall_lapse = 1.0 - curvature * wall_radius**2
    if wall_lapse <= 0.0:
        raise ValueError("wall must lie strictly inside the static patch")
    gravitational_coefficient = 2.0 / (
        static_patch_radius_squared_over_newton * curvature
    )
    return (
        gravitational_coefficient
        * (1.0 - metric_budget)
        / (wall_radius * wall_lapse)
        * sqrt(2.0 * static_mass * mean_casimir / inertia)
    )


def collective_rotational_backreaction_record(
    *,
    metric_budget: Fraction,
    wall_radius: Fraction,
    curvature: Fraction,
    static_patch_radius_squared_over_newton: Fraction,
    static_mass_lower: Fraction,
    inertia_upper: Fraction,
) -> dict[str, object]:
    """Return the exact Casimir and orientation-risk consequences."""
    capacity = collective_constraint_casimir_capacity(
        metric_budget=metric_budget,
        wall_radius=wall_radius,
        curvature=curvature,
        static_patch_radius_squared_over_newton=(
            static_patch_radius_squared_over_newton
        ),
        static_mass_lower=static_mass_lower,
        inertia_upper=inertia_upper,
    )
    risk = collective_constraint_orientation_risk_floor(capacity)
    return {
        "result_type": "conditional_spherical_collective_gravity_casimir_bound",
        "metric_budget_beta": str(metric_budget),
        "wall_radius_x_w": str(wall_radius),
        "curvature_lambda": str(curvature),
        "static_patch_radius_squared_over_newton": str(
            static_patch_radius_squared_over_newton
        ),
        "static_bulk_mass_lower": str(static_mass_lower),
        "bulk_inertia_upper": str(inertia_upper),
        "maximum_mean_casimir_exact": str(capacity),
        "maximum_mean_casimir_float": float(capacity),
        "global_orientation_risk_lower_bound_exact": str(risk),
        "global_orientation_risk_lower_bound_float": float(risk),
        "coupling_elimination": (
            "rest contribution scales as e^-2 and collective rotational "
            "contribution as e^2 Cbar; AM-GM removes e"
        ),
        "claim_boundary": (
            "Necessary condition within the fixed-field, spherical radial-metric, "
            "leading collective-rotor model. It excludes shell energy and does "
            "not control the lapse, nonspherical stress, collective projection, "
            "higher-order rotation, or a rotating Einstein-Skyrme solution."
        ),
    }


def spherical_rotational_backreaction_certificate() -> dict[str, object]:
    """Audit exact elimination on compact rational sample data."""
    record = collective_rotational_backreaction_record(
        metric_budget=Fraction(1, 2),
        wall_radius=Fraction(4),
        curvature=Fraction(1, 400),
        static_patch_radius_squared_over_newton=Fraction(10**6),
        static_mass_lower=Fraction(34),
        inertia_upper=Fraction(49),
    )
    capacity = Fraction(record["maximum_mean_casimir_exact"])
    lower_at_capacity = collective_constraint_lower_bound(
        float(capacity),
        metric_budget=0.5,
        wall_radius=4.0,
        curvature=1.0 / 400.0,
        static_patch_radius_squared_over_newton=1.0e6,
        static_mass=34.0,
        inertia=49.0,
    )
    claims = {
        "finite_casimir_capacity": capacity > 0,
        "positive_orientation_risk_floor": Fraction(
            record["global_orientation_risk_lower_bound_exact"]
        )
        > 0,
        "capacity_saturates_optimized_constraint": abs(lower_at_capacity - 0.5)
        < 1.0e-12,
    }
    return {
        "goal": "Spherical Collective Rotational Backreaction Bound",
        "status": "pass" if all(claims.values()) else "fail",
        "record": record,
        "certified_claims": claims,
    }
