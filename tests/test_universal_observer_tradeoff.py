import math

import pytest

from qgtoy.universal_observer_tradeoff import (
    conditional_observer_risk_lower_bound,
    conditional_observer_tradeoff_record,
    effective_initial_risk_budget,
    maximum_noise_exposure_for_risk,
    required_mean_casimir_capacity_with_heat,
)


def test_generic_capacity_heat_composition() -> None:
    capacity = 2.0
    exposure = 0.3
    attenuation = math.exp(-2.0 * exposure)
    expected = 0.75 * (1.0 - attenuation) + attenuation / (16.0 * capacity + 8.0)
    assert conditional_observer_risk_lower_bound(
        mean_casimir_capacity=capacity,
        rotational_noise_exposure=exposure,
    ) == pytest.approx(expected)


def test_required_capacity_inverts_risk_floor() -> None:
    budget = 0.2
    exposure = 0.1
    required = required_mean_casimir_capacity_with_heat(
        budget,
        rotational_noise_exposure=exposure,
    )
    assert conditional_observer_risk_lower_bound(
        mean_casimir_capacity=required,
        rotational_noise_exposure=exposure,
    ) == pytest.approx(budget)


def test_noise_ceiling_is_capacity_independent() -> None:
    budget = 0.1
    ceiling = maximum_noise_exposure_for_risk(budget)
    assert effective_initial_risk_budget(
        budget,
        rotational_noise_exposure=ceiling,
    ) == pytest.approx(0.0)
    assert math.isinf(
        required_mean_casimir_capacity_with_heat(
            budget,
            rotational_noise_exposure=ceiling,
        )
    )


def test_named_model_record_distinguishes_conditional_scope() -> None:
    record = conditional_observer_tradeoff_record(
        mean_casimir_capacity=0.0,
        risk_budget=0.1,
        rotational_noise_exposure=0.0,
        capacity_model="confined orbital matter",
        localization_model="proper enclosing ball",
    )
    assert record["declared_class_excluded"] is True
    assert "Conditional" in record["claim_boundary"]


def test_model_names_are_required() -> None:
    with pytest.raises(ValueError, match="must be named"):
        conditional_observer_tradeoff_record(
            mean_casimir_capacity=1.0,
            risk_budget=0.1,
            rotational_noise_exposure=0.0,
            capacity_model="",
            localization_model="ball",
        )


def test_risk_budget_above_one_is_rejected() -> None:
    with pytest.raises(ValueError, match="at most one"):
        maximum_noise_exposure_for_risk(1.1)
