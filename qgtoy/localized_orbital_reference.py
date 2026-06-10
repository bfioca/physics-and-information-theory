"""Localization-energy bounds for nonrelativistic orbital references.

The theorem implemented here is an analytic quadratic-form statement.  For
spinless particles of total rest mass ``M`` confined to a ball of radius ``a``,
with nonnegative excitation Hamiltonian ``H_ex >= T``, mass-weighted
Cauchy-Schwarz gives

    <L^2> <= 2 M a^2 <T> <= 2 M a^2 <H_ex>.

Combining this capacity bound with the global SO(3) fusion/Hardy and asymmetry
theorems yields an all-state orientation-risk floor.  Rotation-trivial internal
multiplicities do not enter the bound.  Intrinsic spin and relativistic or
negative-energy matter are outside its scope.
"""

from __future__ import annotations

from math import exp, inf, isfinite, sqrt

from .global_so3_reference_risk import (
    heat_attenuated_orientation_risk_lower_bound,
    mean_casimir_orientation_risk_lower_bound,
    mean_spin_orientation_risk_lower_bound,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_compactness_margin(value: float) -> None:
    _validate_positive("compactness_margin", value)
    if value >= 1.0:
        raise ValueError("compactness_margin must be smaller than one")


def confined_orbital_casimir_capacity(
    *,
    total_rest_mass: float,
    support_radius: float,
    mean_excitation_energy: float,
) -> float:
    """Return ``2 M a^2 E_ex``, an upper bound on ``<L^2>``.

    Units use ``hbar=c=1``.  The analytic premise is a rotationally invariant
    configuration domain with every particle inside the radius-``a`` ball and
    a quadratic-form Hamiltonian ``H_ex >= sum_i p_i^2/(2m_i)``.
    """
    _validate_positive("total_rest_mass", total_rest_mass)
    _validate_positive("support_radius", support_radius)
    _validate_nonnegative("mean_excitation_energy", mean_excitation_energy)
    return 2.0 * total_rest_mass * support_radius**2 * mean_excitation_energy


def mean_spin_capacity_from_casimir(mean_casimir_capacity: float) -> float:
    """Convert ``<L^2><=C`` into ``<j><=(sqrt(1+4C)-1)/2``."""
    _validate_nonnegative("mean_casimir_capacity", mean_casimir_capacity)
    return 0.5 * (sqrt(1.0 + 4.0 * mean_casimir_capacity) - 1.0)


def orientation_risk_floors_from_casimir_capacity(
    mean_casimir_capacity: float,
) -> dict[str, float]:
    """Return independent direct-fusion and information-theoretic floors."""
    mean_spin_capacity = mean_spin_capacity_from_casimir(mean_casimir_capacity)
    direct = mean_casimir_orientation_risk_lower_bound(mean_casimir_capacity)
    information = mean_spin_orientation_risk_lower_bound(mean_spin_capacity)
    return {
        "mean_casimir_capacity": mean_casimir_capacity,
        "mean_spin_capacity": mean_spin_capacity,
        "direct_fusion_risk_lower_bound": direct,
        "information_risk_lower_bound": information,
        "strongest_risk_lower_bound": max(direct, information),
    }


def confined_orbital_orientation_risk_floors(
    *,
    total_rest_mass: float,
    support_radius: float,
    mean_excitation_energy: float,
) -> dict[str, float]:
    """Compose the confined-orbital capacity with global SO(3) risk bounds."""
    capacity = confined_orbital_casimir_capacity(
        total_rest_mass=total_rest_mass,
        support_radius=support_radius,
        mean_excitation_energy=mean_excitation_energy,
    )
    return orientation_risk_floors_from_casimir_capacity(capacity)


def high_spin_tail_probability_upper_bound(
    *,
    mean_casimir_capacity: float,
    reference_cutoff: int,
) -> float:
    """Bound probability in integer-spin sectors ``j>=J+1`` by Markov."""
    _validate_nonnegative("mean_casimir_capacity", mean_casimir_capacity)
    if (
        isinstance(reference_cutoff, bool)
        or not isinstance(reference_cutoff, int)
        or reference_cutoff < 0
    ):
        raise ValueError("reference_cutoff must be a nonnegative integer")
    first_excluded_casimir = (reference_cutoff + 1) * (reference_cutoff + 2)
    return min(1.0, mean_casimir_capacity / first_excluded_casimir)


def compactness_limited_orbital_casimir_capacity(
    *,
    support_radius: float,
    newton_constant: float,
    compactness_margin: float,
) -> float:
    """Eliminate rest/excitation energies under ``2G(M+E)/a<=chi``.

    Since ``M E <= (M+E)^2/4``, the confined-orbital theorem gives
    ``<L^2> <= chi^2 a^4/(8G^2)``.
    """
    _validate_positive("support_radius", support_radius)
    _validate_positive("newton_constant", newton_constant)
    _validate_compactness_margin(compactness_margin)
    return (
        compactness_margin**2
        * support_radius**4
        / (8.0 * newton_constant**2)
    )


def compactness_limited_orbital_orientation_risk_floors(
    *,
    support_radius: float,
    newton_constant: float,
    compactness_margin: float,
) -> dict[str, float]:
    """Return the localized orbital-reference risk floor after energy elimination."""
    capacity = compactness_limited_orbital_casimir_capacity(
        support_radius=support_radius,
        newton_constant=newton_constant,
        compactness_margin=compactness_margin,
    )
    return orientation_risk_floors_from_casimir_capacity(capacity)


def compactness_limited_orbital_heat_risk_lower_bound(
    *,
    support_radius: float,
    newton_constant: float,
    compactness_margin: float,
    rotational_noise_exposure: float,
) -> float:
    """Compose compactness capacity with arbitrary integrated SO(3) heat noise.

    ``rotational_noise_exposure`` is ``Gamma=int gamma(tau) d tau``. No
    constant-rate or Markovian-clock identification is needed beyond the
    declared isotropic heat channel itself.
    """
    _validate_nonnegative("rotational_noise_exposure", rotational_noise_exposure)
    initial = compactness_limited_orbital_orientation_risk_floors(
        support_radius=support_radius,
        newton_constant=newton_constant,
        compactness_margin=compactness_margin,
    )["direct_fusion_risk_lower_bound"]
    return heat_attenuated_orientation_risk_lower_bound(
        initial,
        rotational_noise_exposure,
    )


def minimum_compactness_limited_orbital_radius_for_heat_risk(
    risk_budget: float,
    *,
    newton_constant: float,
    compactness_margin: float,
    rotational_noise_exposure: float,
) -> float:
    """Return the necessary support-radius floor for a target risk budget."""
    _validate_nonnegative("risk_budget", risk_budget)
    if risk_budget > 1.0:
        raise ValueError("risk_budget must be at most one")
    _validate_positive("newton_constant", newton_constant)
    _validate_compactness_margin(compactness_margin)
    _validate_nonnegative("rotational_noise_exposure", rotational_noise_exposure)
    if risk_budget >= 0.75:
        return 0.0
    attenuation = exp(-2.0 * rotational_noise_exposure)
    noise_floor = 0.75 * (1.0 - attenuation)
    if risk_budget <= noise_floor:
        return inf
    effective_initial_budget = (risk_budget - noise_floor) / attenuation
    if effective_initial_budget >= 0.125:
        return 0.0
    fourth_power = (
        newton_constant**2
        * (1.0 / effective_initial_budget - 8.0)
        / (2.0 * compactness_margin**2)
    )
    return fourth_power**0.25


def confined_orbital_observer_tradeoff_record(
    *,
    maximum_proper_support_radius: float,
    risk_budget: float,
    newton_constant: float,
    compactness_margin: float,
    rotational_noise_exposure: float,
) -> dict[str, float | bool | str]:
    """Evaluate the named-class localization/capacity/noise compatibility gate."""
    _validate_positive("maximum_proper_support_radius", maximum_proper_support_radius)
    minimum_radius = minimum_compactness_limited_orbital_radius_for_heat_risk(
        risk_budget,
        newton_constant=newton_constant,
        compactness_margin=compactness_margin,
        rotational_noise_exposure=rotational_noise_exposure,
    )
    lower_bound = compactness_limited_orbital_heat_risk_lower_bound(
        support_radius=maximum_proper_support_radius,
        newton_constant=newton_constant,
        compactness_margin=compactness_margin,
        rotational_noise_exposure=rotational_noise_exposure,
    )
    compatible = minimum_radius <= maximum_proper_support_radius
    return {
        "maximum_proper_support_radius": maximum_proper_support_radius,
        "minimum_required_proper_support_radius": minimum_radius,
        "risk_budget": risk_budget,
        "risk_lower_bound_at_support_ceiling": lower_bound,
        "rotational_noise_exposure_Gamma": rotational_noise_exposure,
        "necessary_window_open": compatible,
        "declared_class_excluded": not compatible,
        "theorem": (
            "For confined spinless nonrelativistic orbital matter with "
            "H_ex>=T, 2G(M+E_ex)/a<=chi, support a<=a_max, and isotropic "
            "SO(3) heat exposure Gamma, R_ref is at least "
            "3/4(1-e^-2Gamma)+e^-2Gamma/[8+2chi^2 a_max^4/G^2]."
        ),
        "claim_boundary": (
            "Compactness-localization-noise theorem for a named orbital "
            "matter and heat-channel class. The compactness proxy is not a "
            "full metric, stress, optical-channel, or lifetime bound."
        ),
    }


def localized_orbital_reference_certificate(
    *,
    total_rest_mass: float = 2.0,
    support_radius: float = 0.25,
    mean_excitation_energy: float = 0.5,
    newton_constant: float = 0.01,
    compactness_margin: float = 0.2,
) -> dict[str, object]:
    """Audit the UO.2Q orbital-matter theorem and compactness corollary."""
    energy_capacity = confined_orbital_casimir_capacity(
        total_rest_mass=total_rest_mass,
        support_radius=support_radius,
        mean_excitation_energy=mean_excitation_energy,
    )
    risk = orientation_risk_floors_from_casimir_capacity(energy_capacity)
    total_energy_ceiling = (
        compactness_margin * support_radius / (2.0 * newton_constant)
    )
    compactness_capacity = compactness_limited_orbital_casimir_capacity(
        support_radius=support_radius,
        newton_constant=newton_constant,
        compactness_margin=compactness_margin,
    )
    compactness_risk = orientation_risk_floors_from_casimir_capacity(
        compactness_capacity
    )
    tail_cutoffs = (0, 1, 3, 7, 15, 31)
    tails = tuple(
        {
            "reference_cutoff_J": cutoff,
            "probability_above_J_upper_bound": (
                high_spin_tail_probability_upper_bound(
                    mean_casimir_capacity=energy_capacity,
                    reference_cutoff=cutoff,
                )
            ),
        }
        for cutoff in tail_cutoffs
    )
    sample_satisfies_compactness = (
        total_rest_mass + mean_excitation_energy <= total_energy_ceiling
    )
    claims = {
        "sample_satisfies_declared_compactness_proxy": sample_satisfies_compactness,
        "energy_capacity_is_below_eliminated_compactness_capacity": (
            not sample_satisfies_compactness
            or energy_capacity <= compactness_capacity
        ),
        "orientation_risk_floor_is_strictly_positive": (
            risk["strongest_risk_lower_bound"] > 0.0
            and compactness_risk["strongest_risk_lower_bound"] > 0.0
        ),
        "rare_high_spin_tail_is_uniformly_controlled": all(
            right["probability_above_J_upper_bound"]
            <= left["probability_above_J_upper_bound"]
            for left, right in zip(tails, tails[1:])
        ),
        "bound_is_independent_of_particle_number_and_trivial_multiplicity": True,
    }
    return {
        "goal": "Localized Orbital Reference UO.2Q",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "confined_orbital_localization_energy_orientation_bound",
        "quadratic_form_theorem": (
            "For spinless nonrelativistic particles in a rotationally invariant "
            "radius-a configuration domain, H_ex>=T and sum_i m_i=M imply "
            "<L^2><=2 M a^2 <H_ex>."
        ),
        "compactness_corollary": (
            "The declared proxy 2G(M+<H_ex>)/a<=chi implies "
            "<L^2><=chi^2 a^4/(8G^2) and therefore "
            "R_ref>=1/[8+2 chi^2 a^4/G^2]."
        ),
        "model_scope": (
            "spinless nonrelativistic orbital matter; arbitrary particle count "
            "and positive masses of fixed sum; hard radius support; nonnegative "
            "rotationally invariant interaction; arbitrary rotation-trivial "
            "internal multiplicity; hbar=c=1"
        ),
        "claim_boundary": (
            "The compactness inequality is a declared weak-gravity proxy, not a "
            "general-relativistic body theorem. Intrinsic spin, massless or "
            "relativistic fields, negative interaction energy, soft localization, "
            "local readout, stress, lifetime, and metric response are open. Large "
            "Casimir is used only as an upper capacity budget, never as a "
            "sufficient orientation resource."
        ),
        "parameters": {
            "total_rest_mass": total_rest_mass,
            "support_radius": support_radius,
            "mean_excitation_energy": mean_excitation_energy,
            "newton_constant": newton_constant,
            "compactness_margin": compactness_margin,
            "total_energy_ceiling": total_energy_ceiling,
        },
        "energy_capacity": risk,
        "compactness_eliminated_capacity": compactness_risk,
        "high_spin_tail_bounds": tails,
        "certified_claims": claims,
    }
