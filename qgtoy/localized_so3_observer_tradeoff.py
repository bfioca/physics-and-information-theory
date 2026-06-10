"""Conditional localization-reference-coherence elimination theorem.

This module composes three independently proved ingredients:

* the all-state global SO(3) orientation-risk floor;
* the marked spherical-top compactness capacity; and
* the hard-current optical support ceilings on an equal static-patch shell.

Reference-only isotropic heat diffusion adds a necessary coherence-time bound.
The composition is a no-go/compatibility gate for that declared branch, not a
claim that one microscopic action realizes every premise.
"""

from __future__ import annotations

from math import isfinite

from .finite_size_static_patch_observer import (
    maximum_mean_casimir_from_compactness,
)
from .global_so3_reference_risk import (
    compact_rotor_orientation_risk_record,
    heat_attenuated_orientation_risk_lower_bound,
    maximum_coherence_time_from_initial_floor,
)
from .static_patch_hard_current_multipole import hard_current_support_record
from .static_patch_localization_backreaction import (
    proper_static_slice_angular_distance,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_risk_budget(risk_budget: float) -> None:
    _validate_positive("risk_budget", risk_budget)
    if risk_budget >= 0.75:
        raise ValueError("risk_budget must be smaller than the Haar risk 3/4")


def required_mean_casimir_for_orientation_risk(risk_budget: float) -> float:
    """Necessary Casimir capacity from ``R>=1/(16 C+8)``."""
    _validate_risk_budget(risk_budget)
    return max(0.0, (1.0 / risk_budget - 8.0) / 16.0)


def minimum_compact_rotor_radius_for_orientation_risk(
    risk_budget: float,
    *,
    newton_constant: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> float:
    """Necessary proper-radius floor in the spherical-top branch."""
    required_casimir = required_mean_casimir_for_orientation_risk(risk_budget)
    _validate_positive("newton_constant", newton_constant)
    _validate_positive("inertia_coefficient", inertia_coefficient)
    _validate_positive("compactness_margin", compactness_margin)
    _validate_positive(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
    )
    if inertia_coefficient > 2.0 / 3.0:
        raise ValueError("inertia_coefficient must be at most two thirds")
    if compactness_margin >= 1.0:
        raise ValueError("compactness_margin must be smaller than one")
    if maximum_excitation_fraction > 1.0:
        raise ValueError("maximum_excitation_fraction must be at most one")
    if required_casimir == 0.0:
        return 0.0
    zeta = maximum_excitation_fraction
    coefficient = (
        inertia_coefficient
        * compactness_margin**2
        * zeta
        / (2.0 * newton_constant**2 * (1.0 + zeta) ** 2)
    )
    return (required_casimir / coefficient) ** 0.25


def _design_window_record(
    name: str,
    proper_radius_ceiling: float,
    *,
    risk_budget: float,
    dimensionless_protocol_time: float,
    minimum_required_radius: float,
    newton_constant: float,
    inertia_coefficient: float,
    compactness_margin: float,
    maximum_excitation_fraction: float,
) -> dict[str, object]:
    _validate_positive("proper_radius_ceiling", proper_radius_ceiling)
    maximum_casimir = maximum_mean_casimir_from_compactness(
        observer_radius=proper_radius_ceiling,
        newton_constant=newton_constant,
        inertia_coefficient=inertia_coefficient,
        compactness_margin=compactness_margin,
        maximum_excitation_fraction=maximum_excitation_fraction,
    )
    resource = compact_rotor_orientation_risk_record(
        observer_radius=proper_radius_ceiling,
        newton_constant=newton_constant,
        inertia_coefficient=inertia_coefficient,
        compactness_margin=compactness_margin,
        maximum_excitation_fraction=maximum_excitation_fraction,
    )
    initial_floor = float(
        resource["global_chordal_orientation_risk_lower_bound"]
    )
    time_floor = heat_attenuated_orientation_risk_lower_bound(
        initial_floor,
        dimensionless_protocol_time,
    )
    maximum_coherence_time = maximum_coherence_time_from_initial_floor(
        initial_floor,
        risk_budget,
    )
    localization_open = proper_radius_ceiling >= minimum_required_radius
    resource_open = initial_floor <= risk_budget
    coherence_open = time_floor <= risk_budget
    return {
        "design": name,
        "proper_radius_ceiling": proper_radius_ceiling,
        "minimum_required_proper_radius": minimum_required_radius,
        "radius_window_ratio_upper_to_lower": (
            float("inf")
            if minimum_required_radius == 0.0
            else proper_radius_ceiling / minimum_required_radius
        ),
        "maximum_mean_casimir_at_radius_ceiling": maximum_casimir,
        "initial_global_risk_lower_bound_at_radius_ceiling": initial_floor,
        "dimensionless_protocol_time_gamma_T": dimensionless_protocol_time,
        "global_risk_lower_bound_at_protocol_time": time_floor,
        "maximum_dimensionless_coherence_time": maximum_coherence_time,
        "localization_capacity_condition_not_excluded": localization_open,
        "full_initial_resource_condition_not_excluded": resource_open,
        "coherence_condition_not_excluded": coherence_open,
        "necessary_window_open": (
            localization_open and resource_open and coherence_open
        ),
    }


def localized_so3_observer_tradeoff_record(
    system_spin: int,
    *,
    risk_budget: float,
    proper_protocol_time: float,
    reference_diffusion_rate: float,
    radius: float = 1.0,
    newton_constant: float = 1.0e-12,
    inertia_coefficient: float = 2.0 / 3.0,
    compactness_margin: float = 0.5,
    maximum_excitation_fraction: float = 0.25,
    mismatch_coefficient: float = 1.0,
    multipole_error_coefficient: float = 1.0,
) -> dict[str, object]:
    """Evaluate necessary windows for the declared static-patch branch."""
    if isinstance(system_spin, bool) or not isinstance(system_spin, int) or system_spin < 1:
        raise ValueError("system_spin must be a positive integer")
    _validate_risk_budget(risk_budget)
    _validate_nonnegative("proper_protocol_time", proper_protocol_time)
    _validate_positive("reference_diffusion_rate", reference_diffusion_rate)
    _validate_positive("radius", radius)
    _validate_positive("newton_constant", newton_constant)

    support = hard_current_support_record(
        system_spin,
        radius=radius,
        mismatch_coefficient=mismatch_coefficient,
        multipole_error_coefficient=multipole_error_coefficient,
    )
    horizon_distance = float(support["horizon_distance_rho"])
    center_distance = proper_static_slice_angular_distance(
        float(support["same_shell_center_angle"]),
        horizon_distance=horizon_distance,
        radius=radius,
    )
    ceilings = {
        "leading_nonoverlap": 0.5 * center_distance,
        "generic_hard_current": proper_static_slice_angular_distance(
            float(support["generic_same_shell_support_angular_radius"]),
            horizon_distance=horizon_distance,
            radius=radius,
        ),
        "dipole_cancelled_hard_current": proper_static_slice_angular_distance(
            float(support["dipole_cancelled_same_shell_support_angular_radius"]),
            horizon_distance=horizon_distance,
            radius=radius,
        ),
    }
    minimum_radius = minimum_compact_rotor_radius_for_orientation_risk(
        risk_budget,
        newton_constant=newton_constant,
        inertia_coefficient=inertia_coefficient,
        compactness_margin=compactness_margin,
        maximum_excitation_fraction=maximum_excitation_fraction,
    )
    dimensionless_time = reference_diffusion_rate * proper_protocol_time
    designs = tuple(
        _design_window_record(
            name,
            ceiling,
            risk_budget=risk_budget,
            dimensionless_protocol_time=dimensionless_time,
            minimum_required_radius=minimum_radius,
            newton_constant=newton_constant,
            inertia_coefficient=inertia_coefficient,
            compactness_margin=compactness_margin,
            maximum_excitation_fraction=maximum_excitation_fraction,
        )
        for name, ceiling in ceilings.items()
    )
    return {
        "system_spin_L": system_spin,
        "system_dimension_d": 2 * system_spin + 1,
        "risk_budget_epsilon": risk_budget,
        "proper_protocol_time_T": proper_protocol_time,
        "reference_diffusion_rate_gamma": reference_diffusion_rate,
        "dimensionless_protocol_time_gamma_T": dimensionless_time,
        "de_sitter_radius_R": radius,
        "horizon_distance_rho": horizon_distance,
        "required_mean_casimir_from_direct_risk_theorem": (
            required_mean_casimir_for_orientation_risk(risk_budget)
        ),
        "minimum_compact_rotor_proper_radius_from_direct_risk_theorem": (
            minimum_radius
        ),
        "optical_support_source": support,
        "design_windows": designs,
        "any_necessary_window_open": any(
            bool(design["necessary_window_open"]) for design in designs
        ),
        "all_necessary_windows_closed": all(
            not bool(design["necessary_window_open"]) for design in designs
        ),
        "logical_status": (
            "pass means only that the necessary inequalities are compatible; "
            "fail excludes that design inside the declared spherical-top, "
            "hard-current, and reference-heat branch"
        ),
        "claim_boundary": (
            "The composed inputs are exact in their declared models but are not "
            "yet derived from one microscopic matter/KMS action. An open window "
            "is not an existence theorem; a closed window is a conditional no-go."
        ),
    }


def localized_so3_observer_tradeoff_certificate() -> dict[str, object]:
    """Audit an open short-time case and a closed long-time case."""
    short_time = localized_so3_observer_tradeoff_record(
        2,
        risk_budget=0.1,
        proper_protocol_time=1.0e-4,
        reference_diffusion_rate=1.0,
    )
    long_time = localized_so3_observer_tradeoff_record(
        2,
        risk_budget=0.1,
        proper_protocol_time=10.0,
        reference_diffusion_rate=1.0,
    )
    certified_claims = {
        "short_time_has_at_least_one_compatible_necessary_window": (
            short_time["any_necessary_window_open"]
        ),
        "long_time_is_excluded_by_reference_heat_coherence": (
            long_time["all_necessary_windows_closed"]
            and all(
                not design["coherence_condition_not_excluded"]
                for design in long_time["design_windows"]
            )
        ),
        "every_design_tracks_localization_resource_and_coherence": all(
            all(
                key in design
                for key in (
                    "localization_capacity_condition_not_excluded",
                    "full_initial_resource_condition_not_excluded",
                    "coherence_condition_not_excluded",
                )
            )
            for design in short_time["design_windows"]
        ),
    }
    return {
        "goal": "Conditional Localized SO(3) Observer Elimination Theorem",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "certified_claims": certified_claims,
        "short_time_record": short_time,
        "long_time_record": long_time,
    }
