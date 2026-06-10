"""Conditional class-uniform orientation-capacity-coherence composition."""

from __future__ import annotations

from math import exp, inf, isfinite, log

from .global_so3_reference_risk import (
    heat_attenuated_orientation_risk_lower_bound,
    mean_casimir_orientation_risk_lower_bound,
)


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def conditional_observer_risk_lower_bound(
    *,
    mean_casimir_capacity: float,
    rotational_noise_exposure: float,
) -> float:
    """Return the class-uniform risk floor from capacity and heat exposure.

    A physical observer class enters only through its proved upper capacity
    ``C2<=mean_casimir_capacity``. The time-dependent heat rate enters through
    ``Gamma=int gamma(tau) d tau``.
    """
    capacity = _nonnegative("mean_casimir_capacity", mean_casimir_capacity)
    exposure = _nonnegative(
        "rotational_noise_exposure",
        rotational_noise_exposure,
    )
    initial = mean_casimir_orientation_risk_lower_bound(capacity)
    return heat_attenuated_orientation_risk_lower_bound(initial, exposure)


def effective_initial_risk_budget(
    risk_budget: float,
    *,
    rotational_noise_exposure: float,
) -> float:
    """Return ``delta_epsilon(Gamma)`` after removing isotropic heat noise."""
    budget = _nonnegative("risk_budget", risk_budget)
    if budget > 1.0:
        raise ValueError("risk_budget must be at most one")
    if budget >= 0.75:
        return 0.75
    exposure = _nonnegative(
        "rotational_noise_exposure",
        rotational_noise_exposure,
    )
    return 0.75 - (0.75 - budget) * exp(2.0 * exposure)


def required_mean_casimir_capacity_with_heat(
    risk_budget: float,
    *,
    rotational_noise_exposure: float,
) -> float:
    """Return the necessary Casimir capacity for a target final risk."""
    delta = effective_initial_risk_budget(
        risk_budget,
        rotational_noise_exposure=rotational_noise_exposure,
    )
    if delta <= 0.0:
        return inf
    return max(0.0, (1.0 / delta - 8.0) / 16.0)


def maximum_noise_exposure_for_risk(risk_budget: float) -> float:
    """Return the noise-only necessary ceiling on integrated exposure."""
    budget = _nonnegative("risk_budget", risk_budget)
    if budget > 1.0:
        raise ValueError("risk_budget must be at most one")
    if budget >= 0.75:
        return inf
    return 0.5 * log(0.75 / (0.75 - budget))


def conditional_observer_tradeoff_record(
    *,
    mean_casimir_capacity: float,
    risk_budget: float,
    rotational_noise_exposure: float,
    capacity_model: str,
    localization_model: str,
) -> dict[str, float | bool | str]:
    """Audit a capacity/localization model against the generic composition."""
    if not capacity_model.strip() or not localization_model.strip():
        raise ValueError("capacity and localization models must be named")
    lower = conditional_observer_risk_lower_bound(
        mean_casimir_capacity=mean_casimir_capacity,
        rotational_noise_exposure=rotational_noise_exposure,
    )
    required = required_mean_casimir_capacity_with_heat(
        risk_budget,
        rotational_noise_exposure=rotational_noise_exposure,
    )
    compatible = mean_casimir_capacity >= required
    return {
        "mean_casimir_capacity_Cmax": mean_casimir_capacity,
        "rotational_noise_exposure_Gamma": rotational_noise_exposure,
        "risk_budget_epsilon": risk_budget,
        "risk_lower_bound": lower,
        "required_mean_casimir_capacity": required,
        "maximum_noise_exposure_for_budget": maximum_noise_exposure_for_risk(
            risk_budget
        ),
        "necessary_conditions_compatible": compatible,
        "declared_class_excluded": not compatible,
        "capacity_model": capacity_model,
        "localization_model": localization_model,
        "theorem": (
            "R(T)>=3/4(1-exp(-2Gamma))"
            "+exp(-2Gamma)/(16 Cmax+8)"
        ),
        "claim_boundary": (
            "Conditional class-uniform composition. Physics enters through "
            "the separately proved capacity, localization, and heat-channel "
            "premises; this record does not create those premises."
        ),
    }
