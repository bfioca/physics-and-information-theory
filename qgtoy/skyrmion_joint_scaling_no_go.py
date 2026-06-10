"""Joint compactness/slow-rotation obstruction for a fixed Skyrmion profile.

For fixed dimensionless ``(mu, lambda, x_w)`` profile data,

    M = c_M/(e^2 R sqrt(lambda)),
    a = x_w R sqrt(lambda),
    I = c_I R sqrt(lambda)/e^2.

Consequently compactness scales as ``e^-2`` while the maximum-spin slow-
rotation parameter scales as ``e^2 sqrt(K(K+1))``.  Their product is
independent of the constrained ``e``/``f_pi`` co-scaling that preserves the
fixed dimensionless profile.  At fixed ``R^2/G`` there is no asymptotically
growing cutoff satisfying both fixed control budgets.
"""

from __future__ import annotations

from math import floor, isfinite, sqrt

from .massive_skyrmion_worldtube import hard_wall_equilibrium_record


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative_spin(spin: float) -> None:
    if not isfinite(spin) or spin < 0.0:
        raise ValueError("spin must be finite and nonnegative")


def skyrmion_compactness(
    skyrme_coupling: float,
    *,
    mass_constant: float,
    wall_radius: float,
    curvature: float,
    static_patch_radius: float,
    newton_constant: float,
) -> float:
    """Return ``2GM/a`` for fixed dimensionless profile data."""
    _validate_positive("skyrme_coupling", skyrme_coupling)
    _validate_positive("mass_constant", mass_constant)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("curvature", curvature)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    return (
        2.0
        * newton_constant
        * mass_constant
        / (
            skyrme_coupling**2
            * wall_radius
            * curvature
            * static_patch_radius**2
        )
    )


def skyrmion_slow_rotation_parameter(
    spin: float,
    skyrme_coupling: float,
    *,
    inertia_constant: float,
) -> float:
    """Return ``e^2 sqrt(K(K+1))/c_I``."""
    _validate_nonnegative_spin(spin)
    _validate_positive("skyrme_coupling", skyrme_coupling)
    _validate_positive("inertia_constant", inertia_constant)
    return (
        skyrme_coupling**2
        * sqrt(spin * (spin + 1.0))
        / inertia_constant
    )


def compactness_slow_rotation_product(
    spin: float,
    *,
    mass_constant: float,
    inertia_constant: float,
    wall_radius: float,
    curvature: float,
    static_patch_radius: float,
    newton_constant: float,
) -> float:
    """Return the coupling-independent product ``C epsilon_rot``."""
    _validate_nonnegative_spin(spin)
    _validate_positive("mass_constant", mass_constant)
    _validate_positive("inertia_constant", inertia_constant)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("curvature", curvature)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    return (
        2.0
        * newton_constant
        * mass_constant
        * sqrt(spin * (spin + 1.0))
        / (
            inertia_constant
            * wall_radius
            * curvature
            * static_patch_radius**2
        )
    )


def admissible_skyrme_coupling_squared_interval(
    spin: float,
    *,
    maximum_compactness: float,
    maximum_slow_rotation: float,
    mass_constant: float,
    inertia_constant: float,
    wall_radius: float,
    curvature: float,
    static_patch_radius: float,
    newton_constant: float,
) -> tuple[float, float] | None:
    """Return the nonempty ``e^2`` interval satisfying both budgets."""
    _validate_nonnegative_spin(spin)
    _validate_positive("maximum_compactness", maximum_compactness)
    _validate_positive("maximum_slow_rotation", maximum_slow_rotation)
    _validate_positive("mass_constant", mass_constant)
    _validate_positive("inertia_constant", inertia_constant)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("curvature", curvature)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    lower = (
        2.0
        * newton_constant
        * mass_constant
        / (
            maximum_compactness
            * wall_radius
            * curvature
            * static_patch_radius**2
        )
    )
    spin_casimir_root = sqrt(spin * (spin + 1.0))
    upper = (
        float("inf")
        if spin_casimir_root == 0.0
        else maximum_slow_rotation * inertia_constant / spin_casimir_root
    )
    if lower <= upper:
        return (lower, upper)
    return None


def _spin_is_within_casimir_bound(
    spin: float,
    casimir_root_bound: float,
) -> bool:
    root = sqrt(spin * (spin + 1.0))
    return root <= casimir_root_bound


def maximum_admissible_spin(
    *,
    maximum_compactness: float,
    maximum_slow_rotation: float,
    mass_constant: float,
    inertia_constant: float,
    wall_radius: float,
    curvature: float,
    static_patch_radius: float,
    newton_constant: float,
) -> int:
    """Return the largest integer ``K`` for which the coupling interval exists."""
    _validate_positive("maximum_compactness", maximum_compactness)
    _validate_positive("maximum_slow_rotation", maximum_slow_rotation)
    _validate_positive("mass_constant", mass_constant)
    _validate_positive("inertia_constant", inertia_constant)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("curvature", curvature)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    casimir_root_bound = (
        maximum_compactness
        * maximum_slow_rotation
        * inertia_constant
        * wall_radius
        * curvature
        * static_patch_radius**2
        / (2.0 * newton_constant * mass_constant)
    )
    continuous_spin_bound = (
        sqrt(1.0 + 4.0 * casimir_root_bound**2) - 1.0
    ) / 2.0
    candidate = max(0, floor(continuous_spin_bound))
    while _spin_is_within_casimir_bound(candidate + 1.0, casimir_root_bound):
        candidate += 1
    while candidate > 0 and not _spin_is_within_casimir_bound(
        float(candidate), casimir_root_bound
    ):
        candidate -= 1
    return candidate


def maximum_admissible_odd_reference_cutoff(
    *,
    maximum_compactness: float,
    maximum_slow_rotation: float,
    mass_constant: float,
    inertia_constant: float,
    wall_radius: float,
    curvature: float,
    static_patch_radius: float,
    newton_constant: float,
) -> int | None:
    """Return the largest odd-sector cutoff ``J`` with spin ``K=J+1/2``."""
    _validate_positive("maximum_compactness", maximum_compactness)
    _validate_positive("maximum_slow_rotation", maximum_slow_rotation)
    _validate_positive("mass_constant", mass_constant)
    _validate_positive("inertia_constant", inertia_constant)
    _validate_positive("wall_radius", wall_radius)
    _validate_positive("curvature", curvature)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    casimir_root_bound = (
        maximum_compactness
        * maximum_slow_rotation
        * inertia_constant
        * wall_radius
        * curvature
        * static_patch_radius**2
        / (2.0 * newton_constant * mass_constant)
    )
    continuous_spin_bound = (
        sqrt(1.0 + 4.0 * casimir_root_bound**2) - 1.0
    ) / 2.0
    maximum_cutoff = floor(continuous_spin_bound - 0.5)
    while _spin_is_within_casimir_bound(
        maximum_cutoff + 1.5,
        casimir_root_bound,
    ):
        maximum_cutoff += 1
    while maximum_cutoff >= 0 and not _spin_is_within_casimir_bound(
        maximum_cutoff + 0.5,
        casimir_root_bound,
    ):
        maximum_cutoff -= 1
    return maximum_cutoff if maximum_cutoff >= 0 else None


def skyrmion_joint_scaling_no_go_certificate(
    *,
    static_patch_radius: float = 1.0,
    newton_constant: float = 1.0e-6,
    maximum_compactness: float = 0.5,
    maximum_slow_rotation: float = 0.1,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
) -> dict[str, object]:
    """Certify the fixed-profile joint-control obstruction and finite window."""
    worldtube = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
    )
    mass_constant = worldtube["dimensionless_total_mass_c_M"]
    inertia_constant = worldtube["profile_integrals"][
        "interior_dimensionless_inertia_c_I"
    ]
    maximum_cutoff = maximum_admissible_odd_reference_cutoff(
        maximum_compactness=maximum_compactness,
        maximum_slow_rotation=maximum_slow_rotation,
        mass_constant=mass_constant,
        inertia_constant=inertia_constant,
        wall_radius=wall_radius,
        curvature=curvature,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    if maximum_cutoff is None:
        raise ValueError(
            "the selected budgets do not admit even the lowest odd-sector spin"
        )
    maximum_spin = maximum_cutoff + 0.5
    interval_at_bound = admissible_skyrme_coupling_squared_interval(
        maximum_spin,
        maximum_compactness=maximum_compactness,
        maximum_slow_rotation=maximum_slow_rotation,
        mass_constant=mass_constant,
        inertia_constant=inertia_constant,
        wall_radius=wall_radius,
        curvature=curvature,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    interval_beyond = admissible_skyrme_coupling_squared_interval(
        maximum_spin + 1.0,
        maximum_compactness=maximum_compactness,
        maximum_slow_rotation=maximum_slow_rotation,
        mass_constant=mass_constant,
        inertia_constant=inertia_constant,
        wall_radius=wall_radius,
        curvature=curvature,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    sample_cutoff = max(0, maximum_cutoff // 2)
    sample_spin = sample_cutoff + 0.5
    sample_coupling = 0.3
    compactness = skyrmion_compactness(
        sample_coupling,
        mass_constant=mass_constant,
        wall_radius=wall_radius,
        curvature=curvature,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    slow = skyrmion_slow_rotation_parameter(
        sample_spin,
        sample_coupling,
        inertia_constant=inertia_constant,
    )
    exact_product = compactness_slow_rotation_product(
        sample_spin,
        mass_constant=mass_constant,
        inertia_constant=inertia_constant,
        wall_radius=wall_radius,
        curvature=curvature,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    certified_claims = {
        "compactness_slow_rotation_product_is_coupling_independent": abs(
            compactness * slow / exact_product - 1.0
        )
        < 1.0e-13,
        "finite_spin_window_is_nonempty_for_default_parameters": (
            maximum_spin > 0 and interval_at_bound is not None
        ),
        "next_fermionic_reference_spin_lies_outside_the_joint_window": (
            interval_beyond is None
        ),
        "fixed_profile_growth_coefficient_is_finite_and_positive": (
            isfinite(
                2.0
                * newton_constant
                * mass_constant
                / (
                    inertia_constant
                    * wall_radius
                    * curvature
                    * static_patch_radius**2
                )
            )
            and 2.0
            * newton_constant
            * mass_constant
            / (
                inertia_constant
                * wall_radius
                * curvature
                * static_patch_radius**2
            )
            > 0.0
        ),
    }
    return {
        "goal": "Fixed-Profile Skyrmion Compactness/Slow-Rotation No-Go",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "conditional_matter_derived_finite_spin_window",
        "central_result": (
            "For fixed dimensionless worldtube data and fixed R^2/G, the product "
            "of compactness and the maximum-spin slow-rotation parameter grows "
            "as sqrt(K(K+1)) and is independent of the constrained e/f_pi "
            "co-scaling that preserves e f_pi and the dimensionless profile. "
            "No such fixed-profile co-scaling supports an asymptotically "
            "growing controlled cutoff."
        ),
        "worldtube_profile": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius_x_w": wall_radius,
            "mass_constant_c_M_total": mass_constant,
            "inertia_constant_c_I": inertia_constant,
        },
        "budgets": {
            "static_patch_radius_R": static_patch_radius,
            "newton_constant_G": newton_constant,
            "maximum_compactness": maximum_compactness,
            "maximum_slow_rotation_parameter": maximum_slow_rotation,
        },
        "maximum_admissible_odd_reference_cutoff_J": maximum_cutoff,
        "maximum_admissible_physical_spin_K": maximum_spin,
        "admissible_e_squared_interval_at_maximum_spin": interval_at_bound,
        "next_spin_interval": interval_beyond,
        "product_identity": (
            "C epsilon_rot = 2 G c_M sqrt(K(K+1)) / "
            "(c_I x_w lambda R^2)"
        ),
        "certified_claims": certified_claims,
        "claim_boundary": (
            "The theorem fixes the dimensionless profile (mu, lambda, x_w), "
            "uses the centered ideal-wall mass and inertia, and treats R^2/G "
            "and the two control budgets as fixed. Varying e within this family "
            "requires co-varying f_pi so that e f_pi remains fixed. "
            "Profile-changing double "
            "scalings, wall inertia, Omega^4 terms, off-center support, radiation, "
            "and full Einstein-Skyrme backreaction are outside the result."
        ),
        "next_physics_gate": (
            "test whether any profile-changing double scaling or different "
            "matter source evades the product obstruction while preserving the "
            "projective reference and open-system channel"
        ),
    }
