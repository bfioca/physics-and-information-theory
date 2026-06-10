"""Compactness versus near-horizon localization for growing spin sectors.

The finite spherical-top EFT supplies a compactness lower bound on the proper
radius of a definite spin sector. The gradient common-mode analysis and
hard-current theorem supply shrinking angular-support scales. Combining them
gives a finite conditional window: no growing-spin sequence can remain in the
controlled local-common-mode branch while also satisfying the declared
compactness and nonoverlap assumptions. Finite integer crossings based on the
leading co-location law are illustrative, not exact channel cutoffs.
"""

from __future__ import annotations

from math import asin, cos, isfinite, log, pi, sin, sqrt

from .static_patch_hard_current_multipole import hard_current_support_record


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _validate_fraction(name: str, value: float, *, inclusive_one: bool) -> None:
    _validate_positive(name, value)
    if value > 1.0 or (not inclusive_one and value == 1.0):
        endpoint = "at most" if inclusive_one else "smaller than"
        raise ValueError(f"{name} must be {endpoint} one")


def minimum_compact_spherical_top_radius(
    spin: int,
    *,
    newton_constant: float,
    inertia_coefficient: float = 2.0 / 3.0,
    compactness_margin: float = 0.5,
    maximum_excitation_fraction: float = 0.25,
) -> float:
    """Return the proper-radius floor for a definite spin-``L`` top.

    This exactly inverts

    ``L(L+1) <= kappa chi^2 zeta a^4/[2G^2(1+zeta)^2]``.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive("newton_constant", newton_constant)
    _validate_positive("inertia_coefficient", inertia_coefficient)
    if inertia_coefficient > 2.0 / 3.0:
        raise ValueError("inertia_coefficient must be at most two thirds")
    _validate_fraction("compactness_margin", compactness_margin, inclusive_one=False)
    _validate_fraction(
        "maximum_excitation_fraction",
        maximum_excitation_fraction,
        inclusive_one=True,
    )
    zeta = maximum_excitation_fraction
    return (
        2.0
        * newton_constant**2
        * (1.0 + zeta) ** 2
        * spin
        * (spin + 1)
        / (inertia_coefficient * compactness_margin**2 * zeta)
    ) ** 0.25


def proper_static_slice_angular_distance(
    angular_radius: float,
    *,
    horizon_distance: float,
    radius: float,
) -> float:
    """Return the exact static-slice distance between equal-shell centers.

    A static time slice is a hemisphere of a three-sphere of radius ``R``. For
    equal radial coordinate ``rho`` and angular separation ``theta``, its center
    distance is ``2R asin[cos(rho/R) sin(theta/2)]``.
    """
    if not isfinite(angular_radius) or angular_radius < 0.0:
        raise ValueError("angular_radius must be finite and nonnegative")
    _validate_positive("horizon_distance", horizon_distance)
    _validate_positive("radius", radius)
    if angular_radius > pi:
        raise ValueError("angular_radius must be at most pi")
    if horizon_distance > 0.5 * pi * radius:
        raise ValueError("horizon_distance must be at most pi R/2")
    return 2.0 * radius * asin(
        cos(horizon_distance / radius) * sin(0.5 * angular_radius)
    )


def localization_backreaction_record(
    spin: int,
    *,
    radius: float = 1.0,
    newton_constant: float = 1.0e-12,
    inertia_coefficient: float = 2.0 / 3.0,
    compactness_margin: float = 0.5,
    maximum_excitation_fraction: float = 0.25,
    mismatch_coefficient: float = 1.0,
    multipole_error_coefficient: float = 1.0,
) -> dict[str, float | int | bool | str]:
    """Compare compactness and localization radii for one spin sector."""
    _validate_positive_integer("spin", spin)
    _validate_positive("radius", radius)
    _validate_positive("newton_constant", newton_constant)
    support = hard_current_support_record(
        spin,
        radius=radius,
        mismatch_coefficient=mismatch_coefficient,
        multipole_error_coefficient=multipole_error_coefficient,
    )
    dimension = 2 * spin + 1
    horizon_distance = float(support["horizon_distance_rho"])
    minimum_radius = minimum_compact_spherical_top_radius(
        spin,
        newton_constant=newton_constant,
        inertia_coefficient=inertia_coefficient,
        compactness_margin=compactness_margin,
        maximum_excitation_fraction=maximum_excitation_fraction,
    )
    center_distance = proper_static_slice_angular_distance(
        float(support["same_shell_center_angle"]),
        horizon_distance=horizon_distance,
        radius=radius,
    )
    nonoverlap_ceiling = 0.5 * center_distance
    generic_design_ceiling = proper_static_slice_angular_distance(
        float(support["generic_same_shell_support_angular_radius"]),
        horizon_distance=horizon_distance,
        radius=radius,
    )
    dipole_design_ceiling = proper_static_slice_angular_distance(
        float(support["dipole_cancelled_same_shell_support_angular_radius"]),
        horizon_distance=horizon_distance,
        radius=radius,
    )
    compactness_coefficient = (
        (1.0 + maximum_excitation_fraction) ** 2
        / (
            2.0
            * inertia_coefficient
            * compactness_margin**2
            * maximum_excitation_fraction
        )
    ) ** 0.25
    return {
        "spin_L": spin,
        "sector_dimension_d": dimension,
        "horizon_distance_rho": horizon_distance,
        "exact_static_slice_center_distance": center_distance,
        "planck_length_sqrt_G": sqrt(newton_constant),
        "minimum_compact_top_proper_radius": minimum_radius,
        "leading_common_mode_nonoverlap_proper_radius_ceiling": nonoverlap_ceiling,
        "generic_gksl_sufficient_thin_shell_radius_ceiling": generic_design_ceiling,
        "dipole_cancelled_gksl_sufficient_thin_shell_radius_ceiling": (
            dipole_design_ceiling
        ),
        "leading_nonoverlap_compactness_window_exists": (
            nonoverlap_ceiling >= minimum_radius
        ),
        "generic_certified_window_exists": generic_design_ceiling >= minimum_radius,
        "dipole_cancelled_certified_window_exists": (
            dipole_design_ceiling >= minimum_radius
        ),
        "leading_nonoverlap_radius_ratio_upper_to_lower": (
            nonoverlap_ceiling / minimum_radius
        ),
        "generic_radius_ratio_upper_to_lower": generic_design_ceiling / minimum_radius,
        "dipole_cancelled_radius_ratio_upper_to_lower": (
            dipole_design_ceiling / minimum_radius
        ),
        "leading_nonoverlap_compactness_utilization": (
            minimum_radius / nonoverlap_ceiling
        ) ** 2,
        "generic_design_compactness_utilization": (
            minimum_radius / generic_design_ceiling
        ) ** 2,
        "dipole_cancelled_design_compactness_utilization": (
            minimum_radius / dipole_design_ceiling
        ) ** 2,
        "scaled_compactness_lower_radius": (
            minimum_radius / (sqrt(newton_constant) * sqrt(dimension))
        ),
        "compactness_lower_asymptotic_coefficient": compactness_coefficient,
        "scaled_nonoverlap_upper_radius_d_to_5_over_2_sqrt_log": (
            nonoverlap_ceiling
            * dimension**2.5
            * sqrt(log(float(dimension)))
            / radius
        ),
        "scaled_generic_design_radius_d_to_4_log": (
            generic_design_ceiling
            * dimension**4
            * log(float(dimension))
            / radius
        ),
        "scaled_leading_nonoverlap_utilization": (
            (minimum_radius / nonoverlap_ceiling) ** 2
            * radius**2
            / newton_constant
            / (dimension**6 * log(float(dimension)))
        ),
        "scaled_generic_design_utilization": (
            (minimum_radius / generic_design_ceiling) ** 2
            * radius**2
            / newton_constant
            / (dimension**9 * log(float(dimension)) ** 2)
        ),
        "scaled_dipole_cancelled_design_utilization": (
            (minimum_radius / dipole_design_ceiling) ** 2
            * radius**2
            / newton_constant
            / (dimension**6 * log(float(dimension)))
        ),
        "window_interpretation": (
            "for equal-radius thin-shell worldtubes, the nonoverlap ceiling "
            "combines exact static-slice geometry with the leading controlled "
            "local-common-mode law; its finite crossing is an asymptotic proxy. "
            "The two GKSL ceilings are sufficient thin-shell design conditions, "
            "not necessary localization bounds"
        ),
    }


def maximum_spin_with_leading_localization_window(
    *,
    branch: str,
    radius: float = 1.0,
    newton_constant: float = 1.0e-12,
    inertia_coefficient: float = 2.0 / 3.0,
    compactness_margin: float = 0.5,
    maximum_excitation_fraction: float = 0.25,
    mismatch_coefficient: float = 1.0,
    multipole_error_coefficient: float = 1.0,
    maximum_search_spin: int = 1_000_000,
) -> int:
    """Return the largest integer spin before a selected leading crossover.

    The formulas entering each predicate are monotone in the declared regime:
    the compactness floor increases while the support ceilings decrease. Any
    branch can inherit the disjointness candidate, so the returned finite
    integer can depend on the leading small-separation common-mode law and need
    not be an exact channel cutoff.
    """
    if branch not in {"nonoverlap", "generic", "dipole_cancelled"}:
        raise ValueError("branch must be nonoverlap, generic, or dipole_cancelled")
    _validate_positive_integer("maximum_search_spin", maximum_search_spin)

    def predicate(spin: int) -> bool:
        record = localization_backreaction_record(
            spin,
            radius=radius,
            newton_constant=newton_constant,
            inertia_coefficient=inertia_coefficient,
            compactness_margin=compactness_margin,
            maximum_excitation_fraction=maximum_excitation_fraction,
            mismatch_coefficient=mismatch_coefficient,
            multipole_error_coefficient=multipole_error_coefficient,
        )
        key = {
            "nonoverlap": "leading_nonoverlap_compactness_window_exists",
            "generic": "generic_certified_window_exists",
            "dipole_cancelled": "dipole_cancelled_certified_window_exists",
        }[branch]
        return bool(record[key])

    if not predicate(1):
        return 0
    low = 1
    high = 2
    while high <= maximum_search_spin and predicate(high):
        low = high
        high *= 2
    if high > maximum_search_spin:
        if predicate(maximum_search_spin):
            raise RuntimeError("localization window did not close within search limit")
        high = maximum_search_spin
    while low + 1 < high:
        middle = (low + high) // 2
        if predicate(middle):
            low = middle
        else:
            high = middle
    return low


def static_patch_localization_backreaction_certificate(
    *,
    maximum_spin: int = 4096,
    radius: float = 1.0,
    newton_constant: float = 1.0e-12,
) -> dict[str, object]:
    """Certify the compactness-localization window closure."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 64:
        raise ValueError("maximum_spin must be at least sixty-four")
    _validate_positive("radius", radius)
    _validate_positive("newton_constant", newton_constant)
    sample_spins = tuple(
        sorted({spin for spin in (16, 64, 256, 1024, maximum_spin) if spin <= maximum_spin})
    )
    records = tuple(
        localization_backreaction_record(
            spin,
            radius=radius,
            newton_constant=newton_constant,
        )
        for spin in sample_spins
    )
    nonoverlap_cutoff = maximum_spin_with_leading_localization_window(
        branch="nonoverlap",
        radius=radius,
        newton_constant=newton_constant,
    )
    generic_cutoff = maximum_spin_with_leading_localization_window(
        branch="generic",
        radius=radius,
        newton_constant=newton_constant,
    )
    dipole_cutoff = maximum_spin_with_leading_localization_window(
        branch="dipole_cancelled",
        radius=radius,
        newton_constant=newton_constant,
    )
    boundary_record = (
        localization_backreaction_record(
            nonoverlap_cutoff,
            radius=radius,
            newton_constant=newton_constant,
        )
        if nonoverlap_cutoff
        else None
    )
    next_record = localization_backreaction_record(
        nonoverlap_cutoff + 1,
        radius=radius,
        newton_constant=newton_constant,
    )
    last = records[-1]
    asymptotic_compactness_utilization_coefficient = (
        (1.0 + 0.25) / (0.5 * sqrt(2.0 * (2.0 / 3.0) * 0.25))
    )

    def relative_close(value: float, target: float, tolerance: float = 5.0e-3) -> bool:
        return abs(value - target) <= tolerance * max(abs(target), 1.0e-15)

    certified_claims = {
        "compactness_lower_radius_has_sqrt_d_scaling": abs(
            last["scaled_compactness_lower_radius"]
            - last["compactness_lower_asymptotic_coefficient"]
        )
        < 5.0e-4,
        "nonoverlap_upper_radius_has_d_minus_five_halves_scaling": abs(
            last["scaled_nonoverlap_upper_radius_d_to_5_over_2_sqrt_log"] - 1.0
        )
        < 5.0e-4,
        "generic_design_radius_has_d_minus_four_log_scaling": abs(
            last["scaled_generic_design_radius_d_to_4_log"] - 2.0 / 3.0
        )
        < 5.0e-4,
        "leading_nonoverlap_crossover_is_bracketed": (
            (
                boundary_record is not None
                and bool(
                    boundary_record["leading_nonoverlap_compactness_window_exists"]
                )
            )
            or nonoverlap_cutoff == 0
        )
        and not bool(
            next_record["leading_nonoverlap_compactness_window_exists"]
        ),
        "generic_certificate_closes_no_later_than_nonoverlap_window": (
            generic_cutoff <= nonoverlap_cutoff
        ),
        "dipole_certificate_closes_no_later_than_nonoverlap_window": (
            dipole_cutoff <= nonoverlap_cutoff
        ),
        "leading_nonoverlap_radius_ratio_decreases_on_samples": all(
            right["leading_nonoverlap_radius_ratio_upper_to_lower"]
            < left["leading_nonoverlap_radius_ratio_upper_to_lower"]
            for left, right in zip(records, records[1:])
        ),
        "leading_nonoverlap_utilization_has_d6_log_scaling": relative_close(
            last["scaled_leading_nonoverlap_utilization"],
            asymptotic_compactness_utilization_coefficient,
        ),
        "generic_design_utilization_has_d9_log2_scaling": relative_close(
            last["scaled_generic_design_utilization"],
            asymptotic_compactness_utilization_coefficient / (2.0 / 3.0) ** 2,
        ),
        "dipole_design_utilization_has_d6_log_scaling": relative_close(
            last["scaled_dipole_cancelled_design_utilization"],
            asymptotic_compactness_utilization_coefficient,
        ),
    }
    return {
        "goal": "Compactness-Localization Backreaction Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "conditional_controlled_branch_closure",
        "central_result": (
            "Inside the declared definite-spin spherical-top compactness model, "
            "the minimum proper radius grows as sqrt(G)d^(1/2). The leading "
            "distinct-worldtube nonoverlap ceiling inherited from the local "
            "gradient common-mode analysis shrinks as "
            "R d^(-5/2)/sqrt(log d). Hence no growing-dimension sequence can "
            "remain in that controlled perturbative branch while satisfying "
            "the compactness floor."
        ),
        "scaling_consequence": (
            "The leading nonoverlap/compactness window obeys "
            "d^3 sqrt(log d)=O(R/sqrt(G)), giving a finite conditional cutoff "
            "d=O[(R/sqrt(G))^(1/3)/(log d)^(1/6)]. The generic diagonal-jump "
            "sufficient design closes earlier, with "
            "d^(9/2)log d=O(R/sqrt(G))."
        ),
        "claim_boundary": (
            "The controlled-branch closure holds only within the declared "
            "spherical-top inertia/excitation/compactness model, distinct equal-"
            "radius thin-shell nonoverlapping worldtubes, and the gradient-channel "
            "analysis in its local common-mode regime, with the top spin "
            "identified with the hard-sector spin. The reported finite "
            "nonoverlap crossing is illustrative. The generic and dipole-"
            "cancelled GKSL crossings are closures of sufficient design "
            "certificates. No Einstein-matter solution, global channel no-go, "
            "or general collapse theorem is proved."
        ),
        "illustrative_leading_nonoverlap_crossover_spin": nonoverlap_cutoff,
        "illustrative_leading_nonoverlap_crossover_dimension": (
            2 * nonoverlap_cutoff + 1 if nonoverlap_cutoff else 0
        ),
        "generic_gksl_design_crossover_spin": generic_cutoff,
        "dipole_cancelled_gksl_design_crossover_spin": dipole_cutoff,
        "certified_claims": certified_claims,
        "records": records,
        "next_physics_gate": (
            "test whether a named rotating matter source can evade the spherical-"
            "top radius floor or the distinct-worldtube premise, and derive the "
            "three jump-transfer bounds and lifetime from its QFT stress tensor"
        ),
    }
