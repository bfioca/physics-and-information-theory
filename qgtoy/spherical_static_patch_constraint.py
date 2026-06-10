"""Spherical de Sitter Hamiltonian-constraint margins.

On a time-symmetric spherical slice in areal radius, the radial metric is

``dl^2 = dr^2/f(r) + r^2 dOmega^2`` with
``f(r) = N(r) - 2 G m(r)/r`` and ``N(r) = 1-r^2/R^2``.

The dimensionless ratio ``q(r)=2Gm(r)/(rN(r))`` is therefore the exact local
control parameter for the radial metric.  A wall compactness only evaluates
this condition at one radius and cannot control a concentrated interior mass.
"""

from __future__ import annotations

from math import isfinite


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def de_sitter_static_factor(radius: float, *, static_patch_radius: float) -> float:
    """Return ``N(r)=1-r^2/R^2`` strictly inside the static patch."""
    _validate_nonnegative("radius", radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    if radius >= static_patch_radius:
        raise ValueError("radius must lie strictly inside the static patch")
    return 1.0 - (radius / static_patch_radius) ** 2


def spherical_constraint_ratio(
    enclosed_mass: float,
    radius: float,
    *,
    static_patch_radius: float,
    newton_constant: float,
) -> float:
    """Return the exact local ratio ``q=2Gm/(rN)``."""
    _validate_nonnegative("enclosed_mass", enclosed_mass)
    _validate_positive("radius", radius)
    _validate_positive("newton_constant", newton_constant)
    lapse = de_sitter_static_factor(
        radius,
        static_patch_radius=static_patch_radius,
    )
    return 2.0 * newton_constant * enclosed_mass / (radius * lapse)


def radial_metric_relative_distortion(constraint_ratio: float) -> float:
    """Return ``(g_rr-g_rr,dS)/g_rr,dS = q/(1-q)`` for ``0<=q<1``."""
    _validate_nonnegative("constraint_ratio", constraint_ratio)
    if constraint_ratio >= 1.0:
        raise ValueError("constraint_ratio must be smaller than one")
    return constraint_ratio / (1.0 - constraint_ratio)


def spherical_constraint_margin_record(
    maximum_constraint_ratio: float,
    *,
    control_budget: float,
) -> dict[str, float | bool | str]:
    """Turn a uniform bound on ``q`` into radial metric and horizon margins."""
    _validate_nonnegative("maximum_constraint_ratio", maximum_constraint_ratio)
    _validate_positive("control_budget", control_budget)
    if control_budget >= 1.0:
        raise ValueError("control_budget must be smaller than one")
    controlled = maximum_constraint_ratio <= control_budget
    return {
        "maximum_constraint_ratio_q": maximum_constraint_ratio,
        "control_budget_beta": control_budget,
        "controlled_radial_metric": controlled,
        "areal_coordinate_horizon_excluded": maximum_constraint_ratio < 1.0,
        "minimum_metric_factor_relative_to_de_sitter": (
            1.0 - maximum_constraint_ratio
        ),
        "maximum_relative_radial_metric_distortion": (
            radial_metric_relative_distortion(maximum_constraint_ratio)
            if maximum_constraint_ratio < 1.0
            else float("inf")
        ),
        "theorem": (
            "If q(r)=2Gm(r)/(rN(r)) is uniformly at most beta<1, then "
            "f(r)=N(r)(1-q(r)) is positive and g_rr/g_rr,dS-1 is at most "
            "beta/(1-beta)."
        ),
    }


def concentrated_core_counterexample_record(
    *,
    wall_compactness: float = 0.01,
    support_radius: float = 0.5,
    core_radius: float = 0.001,
    static_patch_radius: float = 1.0,
) -> dict[str, float | bool | str]:
    """Show that small wall compactness does not control the interior metric.

    The source is a nonnegative uniform-density core of radius ``epsilon`` and
    vacuum between the core and the declared support wall.  This is a
    Hamiltonian-constraint counterexample, not a hydrostatic matter solution.
    """
    _validate_positive("wall_compactness", wall_compactness)
    _validate_positive("support_radius", support_radius)
    _validate_positive("core_radius", core_radius)
    _validate_positive("static_patch_radius", static_patch_radius)
    if support_radius >= static_patch_radius:
        raise ValueError("support_radius must lie inside the static patch")
    if core_radius >= support_radius:
        raise ValueError("core_radius must be smaller than support_radius")

    wall_lapse = de_sitter_static_factor(
        support_radius,
        static_patch_radius=static_patch_radius,
    )
    core_lapse = de_sitter_static_factor(
        core_radius,
        static_patch_radius=static_patch_radius,
    )
    wall_ratio = wall_compactness / wall_lapse
    core_ratio = (
        wall_compactness * support_radius / (core_radius * core_lapse)
    )
    return {
        "wall_compactness_2GM_over_a": wall_compactness,
        "wall_constraint_ratio": wall_ratio,
        "core_constraint_ratio": core_ratio,
        "wall_is_subcritical": wall_ratio < 1.0,
        "interior_areal_metric_factor_is_nonpositive": core_ratio >= 1.0,
        "endpoint_compactness_fails_to_control_interior": (
            wall_ratio < 1.0 and core_ratio >= 1.0
        ),
        "source": (
            "nonnegative uniform-density core with vacuum to the support wall"
        ),
        "claim_boundary": (
            "This disproves an implication from endpoint compactness to a "
            "uniform spherical Hamiltonian-constraint margin. It does not claim "
            "that pressureless uniform matter is a static solution."
        ),
    }


def spherical_static_patch_constraint_certificate() -> dict[str, object]:
    """Audit the metric identity and the endpoint-compactness counterexample."""
    controlled = spherical_constraint_margin_record(0.2, control_budget=0.25)
    counterexample = concentrated_core_counterexample_record()
    claims = {
        "uniform_ratio_excludes_areal_horizon": controlled[
            "areal_coordinate_horizon_excluded"
        ],
        "uniform_ratio_controls_radial_metric": controlled[
            "controlled_radial_metric"
        ],
        "wall_compactness_does_not_control_interior": counterexample[
            "endpoint_compactness_fails_to_control_interior"
        ],
    }
    return {
        "goal": "Spherical Static-Patch Hamiltonian-Constraint Theorem",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "exact_spherical_constraint_bound_plus_endpoint_no_go",
        "controlled_example": controlled,
        "counterexample": counterexample,
        "certified_claims": claims,
        "claim_boundary": (
            "The theorem is exact for a spherical time-symmetric Hamiltonian "
            "constraint in areal gauge. It does not solve the lapse equation, "
            "matter force balance, junction conditions, or rotating Einstein-"
            "matter equations."
        ),
    }
