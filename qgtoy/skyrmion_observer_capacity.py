"""Conditional fixed-profile Skyrmion observer-capacity proposition.

The same massive-Skyrmion profile supplies its support, rest mass, rotor
inertia, and half-integer projective orientation sector.  Compactness and
slow-rotation control impose opposite bounds on the Skyrme coupling.  Their
elimination gives a finite upper bound on any exactly hard-supported
projective sector and hence a nonzero global orientation-risk floor.  This
conditional conclusion cannot be removed by the usual ``e``/``f_pi``
co-scaling at fixed dimensionless profile; it is not a dynamical mechanism
that generates the hard cutoff.
"""

from __future__ import annotations

from fractions import Fraction
from math import asin, atanh, isfinite, pi, sqrt

from .global_so3_reference_risk import (
    heat_attenuated_orientation_risk_lower_bound,
    projective_hard_cutoff_orientation_risk_lower_bound,
)
from .massive_skyrmion_worldtube import hard_wall_equilibrium_record
from .skyrmion_joint_scaling_no_go import (
    admissible_skyrme_coupling_squared_interval,
    maximum_admissible_odd_reference_cutoff,
)
from .validated_skyrmion_sharp_profile import (
    ValidatedSkyrmionSharpWorldtubeConstants,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def fixed_profile_projective_capacity_record(
    *,
    maximum_compactness: float,
    maximum_slow_rotation: float,
    static_patch_radius: float,
    newton_constant: float,
    pion_mass: float = 1.0,
    curvature: float = 0.0025,
    wall_radius: float = 4.0,
    dimensionless_diffusion_time: float = 0.0,
) -> dict[str, object]:
    """Eliminate the coupling under proxy budgets and an exact support premise."""

    _validate_positive("maximum_compactness", maximum_compactness)
    _validate_positive("maximum_slow_rotation", maximum_slow_rotation)
    _validate_positive("static_patch_radius", static_patch_radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_positive("pion_mass", pion_mass)
    _validate_positive("curvature", curvature)
    _validate_positive("wall_radius", wall_radius)
    _validate_nonnegative(
        "dimensionless_diffusion_time",
        dimensionless_diffusion_time,
    )
    areal_support_ratio = wall_radius * sqrt(curvature)
    if areal_support_ratio >= 1.0:
        raise ValueError("fixed Skyrmion wall must lie strictly inside the horizon")

    worldtube = hard_wall_equilibrium_record(
        pion_mass=pion_mass,
        curvature=curvature,
        wall_radius=wall_radius,
    )
    mass_constant = float(worldtube["dimensionless_total_mass_c_M"])
    inertia_constant = float(
        worldtube["profile_integrals"]["interior_dimensionless_inertia_c_I"]
    )
    cutoff = maximum_admissible_odd_reference_cutoff(
        maximum_compactness=maximum_compactness,
        maximum_slow_rotation=maximum_slow_rotation,
        mass_constant=mass_constant,
        inertia_constant=inertia_constant,
        wall_radius=wall_radius,
        curvature=curvature,
        static_patch_radius=static_patch_radius,
        newton_constant=newton_constant,
    )
    if cutoff is None:
        initial_floor = None
        maximum_spin = None
        coupling_interval = None
    else:
        maximum_spin = cutoff + 0.5
        coupling_interval = admissible_skyrme_coupling_squared_interval(
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
        if coupling_interval is None:
            raise AssertionError("reported maximum cutoff has no coupling interval")
        initial_floor = projective_hard_cutoff_orientation_risk_lower_bound(cutoff)
    time_floor = (
        None
        if initial_floor is None
        else heat_attenuated_orientation_risk_lower_bound(
            initial_floor,
            dimensionless_diffusion_time,
        )
    )
    continuous_casimir_root_capacity = (
        maximum_compactness
        * maximum_slow_rotation
        * inertia_constant
        * wall_radius
        * curvature
        * static_patch_radius**2
        / (2.0 * newton_constant * mass_constant)
    )
    areal_support = static_patch_radius * areal_support_ratio
    proper_support = static_patch_radius * asin(areal_support_ratio)
    optical_support = static_patch_radius * atanh(areal_support_ratio)
    proper_horizon_clearance = pi * static_patch_radius / 2.0 - proper_support
    return {
        "result": "conditional_fixed_profile_projective_observer_capacity",
        "dimensionless_profile": {
            "pion_mass_mu": pion_mass,
            "curvature_lambda": curvature,
            "wall_radius_x_w": wall_radius,
            "mass_constant_c_M": mass_constant,
            "inertia_constant_c_I": inertia_constant,
        },
        "budgets": {
            "maximum_compactness_C_star": maximum_compactness,
            "maximum_slow_rotation_s_star": maximum_slow_rotation,
            "newton_constant_G": newton_constant,
            "static_patch_radius_R": static_patch_radius,
        },
        "localization": {
            "areal_support_radius": areal_support,
            "proper_radial_support": proper_support,
            "optical_radial_support": optical_support,
            "proper_horizon_clearance": proper_horizon_clearance,
            "wall_static_metric_factor": 1.0 - areal_support_ratio**2,
        },
        "continuous_sqrt_KK1_capacity": continuous_casimir_root_capacity,
        "maximum_odd_reference_cutoff_J": cutoff,
        "controlled_projective_sector_feasible": cutoff is not None,
        "maximum_physical_spin_K": maximum_spin,
        "admissible_skyrme_coupling_squared_interval": coupling_interval,
        "initial_global_projective_orientation_risk_lower_bound": initial_floor,
        "dimensionless_diffusion_time_gamma_T": dimensionless_diffusion_time,
        "global_orientation_risk_lower_bound_at_time_T": time_floor,
        "co_scaling_invariant": (
            "C * epsilon_rot = "
            "2 G c_M sqrt[K(K+1)]/(c_I x_w lambda R^2)"
        ),
        "conditional_obstruction": (
            "At fixed (mu,lambda,x_w), R^2/G, compactness budget, and "
            "slow-rotation budget, no e/f_pi co-scaling can make the "
            "exactly hard-supported projective orientation risk arbitrarily small."
        ),
        "claim_boundary": (
            "This is a conditional fixed-profile proxy-budget elimination "
            "proposition. It assumes the centered hard-wall profile, its "
            "mass/inertia constants, rigid collective quantization, an exactly "
            "hard-supported odd sector, and the declared compactness and "
            "maximum-occupied-spin slow-rotation proxies. It supplies a uniform "
            "upper bound on admissible support, not a dynamical cutoff. The "
            "time-dependent term additionally assumes isotropic reference heat "
            "flow. Einstein-Skyrme backreaction, junction control, off-center "
            "support, nonspherical stability, and the finite-coupling derivation "
            "of gamma remain outside this proposition."
        ),
    }


def validated_fixed_profile_projective_capacity_record(
    constants: ValidatedSkyrmionSharpWorldtubeConstants,
    *,
    maximum_compactness: Fraction,
    maximum_slow_rotation: Fraction,
    static_patch_radius_squared_over_newton: Fraction,
) -> dict[str, object]:
    """Use directed mass/inertia intervals to certify a projective cutoff."""

    for name, value in (
        ("maximum_compactness", maximum_compactness),
        ("maximum_slow_rotation", maximum_slow_rotation),
        ("static_patch_radius_squared_over_newton", static_patch_radius_squared_over_newton),
    ):
        if not isinstance(value, Fraction) or value <= 0:
            raise ValueError(f"{name} must be a positive Fraction")
    if constants.total_mass.lower <= 0 or constants.inertia.upper <= 0:
        raise ValueError("validated mass and inertia must be strictly positive")
    capacity = (
        maximum_compactness
        * maximum_slow_rotation
        * constants.inertia.upper
        * constants.wall_radius
        * constants.curvature
        * static_patch_radius_squared_over_newton
        / (2 * constants.total_mass.lower)
    )

    cutoff = max(0, int(float(capacity)) - 2)

    def admissible(candidate: int) -> bool:
        return Fraction((2 * candidate + 1) * (2 * candidate + 3), 4) <= capacity**2

    while admissible(cutoff + 1):
        cutoff += 1
    while cutoff >= 0 and not admissible(cutoff):
        cutoff -= 1
    if cutoff < 0:
        return {
            "certificate_id": constants.certificate_id,
            "maximum_odd_reference_cutoff_J": None,
            "initial_global_projective_orientation_risk_lower_bound": None,
            "controlled_projective_sector_feasible": False,
            "continuous_sqrt_KK1_capacity_upper_exact": str(capacity),
            "claim_boundary": (
                "Directed fixed-profile mass/inertia elimination excludes even "
                "the lowest half-integer rigid reference under these budgets."
            ),
        }
    risk_floor = projective_hard_cutoff_orientation_risk_lower_bound(cutoff)
    return {
        "certificate_id": constants.certificate_id,
        "maximum_odd_reference_cutoff_J": cutoff,
        "controlled_projective_sector_feasible": True,
        "maximum_physical_spin_K_exact": f"{2 * cutoff + 1}/2",
        "continuous_sqrt_KK1_capacity_upper_exact": str(capacity),
        "mass_lower_bound_exact": str(constants.total_mass.lower),
        "inertia_upper_bound_exact": str(constants.inertia.upper),
        "initial_global_projective_orientation_risk_lower_bound": risk_floor,
        "directed_interval_logic": (
            "capacity uses c_I upper and c_M lower, so every profile inside the "
            "authenticated Newton tube has cutoff at most J_max"
        ),
        "claim_boundary": (
            "This upgrades the numerical fixed-profile proposition to directed "
            "mass/inertia premises. It still assumes the centered supported "
            "worldtube, rigid collective band, and declared compactness and "
            "slow-rotation proxy budgets rather than a solved Einstein junction."
        ),
    }


def skyrmion_observer_capacity_certificate() -> dict[str, object]:
    """Audit finite capacity, coupling elimination, and heat monotonicity."""

    initial = fixed_profile_projective_capacity_record(
        maximum_compactness=0.5,
        maximum_slow_rotation=0.1,
        static_patch_radius=1.0,
        newton_constant=1.0e-6,
    )
    evolved = fixed_profile_projective_capacity_record(
        maximum_compactness=0.5,
        maximum_slow_rotation=0.1,
        static_patch_radius=1.0,
        newton_constant=1.0e-6,
        dimensionless_diffusion_time=0.2,
    )
    claims = {
        "fixed_budgets_imply_finite_projective_cutoff": (
            initial["maximum_odd_reference_cutoff_J"] == 173
        ),
        "finite_cutoff_implies_nonzero_global_risk_floor": (
            initial["initial_global_projective_orientation_risk_lower_bound"] > 0.0
        ),
        "maximal_cutoff_has_nonempty_coupling_interval": (
            initial["admissible_skyrme_coupling_squared_interval"] is not None
        ),
        "heat_flow_can_only_raise_the_certified_floor": (
            evolved["global_orientation_risk_lower_bound_at_time_T"]
            > initial["global_orientation_risk_lower_bound_at_time_T"]
        ),
        "support_is_strictly_inside_static_patch": (
            initial["localization"]["proper_horizon_clearance"] > 0.0
        ),
    }
    return {
        "goal": "Conditional Fixed-Profile Observer-Capacity Proposition",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "same_profile_exact_support_compactness_slow_rotation_proxy_obstruction",
        "certified_claims": claims,
        "initial_record": initial,
        "heat_evolved_record": evolved,
    }
