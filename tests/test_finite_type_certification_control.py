from itertools import product
from math import ceil, inf, log, sqrt

import pytest

from qgtoy.finite_type_certification_control import (
    FiniteCertificationBudget,
    adaptive_protocol_distance_upper_bound,
    cylinder_type_i_surrogate_record,
    embezzlement_dimension_lower_bound,
    embezzlement_log_dimension_lower_bound,
    embezzlement_site_lower_bound,
    optimal_prefix_embezzlement_record,
)
from qgtoy.modular_manybody_regulator import site_gibbs_weights


def test_adaptive_protocol_hybrid_bound() -> None:
    assert adaptive_protocol_distance_upper_bound(
        per_call_channel_distance=0.01,
        channel_calls=7,
    ) == pytest.approx(0.07)
    assert adaptive_protocol_distance_upper_bound(
        per_call_channel_distance=0.4,
        channel_calls=3,
    ) == 1.0


def test_perfect_finite_embezzlement_is_excluded() -> None:
    assert embezzlement_dimension_lower_bound(
        target_dimension=2,
        half_trace_distance=0.0,
    ) == inf
    assert embezzlement_site_lower_bound(
        target_dimension=2,
        half_trace_distance=0.0,
    ) == inf


def test_dimension_floor_grows_as_error_shrinks() -> None:
    dimensions = [
        embezzlement_dimension_lower_bound(
            target_dimension=2,
            half_trace_distance=error,
        )
        for error in (0.3, 0.15, 0.08, 0.04)
    ]
    assert dimensions == sorted(dimensions)
    assert len(set(dimensions)) == len(dimensions)
    assert dimensions[-1] > 1_000


def test_log_dimension_and_site_floors_remain_stable() -> None:
    log_dimension = embezzlement_log_dimension_lower_bound(
        target_dimension=8,
        half_trace_distance=0.01,
    )
    assert log_dimension > 100.0
    assert embezzlement_site_lower_bound(
        target_dimension=8,
        half_trace_distance=0.01,
    ) == ceil(log_dimension / log(2) - 1e-14)


def _brute_force_prefix_root_fidelity(site_count: int, target: int) -> float:
    probabilities = []
    for bits in product((0, 1), repeat=site_count):
        probability = 1.0
        for site, bit in enumerate(bits, start=1):
            probability *= site_gibbs_weights(site)[bit]
        probabilities.append(probability)
    probabilities.sort(reverse=True)
    target_probabilities = sorted(
        (
            probability / target
            for probability in probabilities
            for _ in range(target)
        ),
        reverse=True,
    )
    return sum(
        sqrt(initial * desired)
        for initial, desired in zip(probabilities, target_probabilities)
    )


@pytest.mark.parametrize("site_count", (1, 2, 3, 4, 5))
def test_block_frontier_matches_brute_force(site_count: int) -> None:
    record = optimal_prefix_embezzlement_record(
        site_count=site_count,
        target_dimension=2,
    )
    assert record["optimal_root_fidelity"] == pytest.approx(
        _brute_force_prefix_root_fidelity(site_count, 2),
        abs=5e-15,
    )


def test_prefix_frontier_improves_with_even_site_count() -> None:
    records = [
        optimal_prefix_embezzlement_record(site_count=sites)
        for sites in (2, 4, 8, 16, 32)
    ]
    errors = [record["optimal_half_trace_distance"] for record in records]
    assert all(left > right for left, right in zip(errors, errors[1:]))
    assert records[-1]["finite_prefix_type"] == "Type I finite"
    assert "Type III_1" in records[-1]["infinite_limit_type"]


def test_larger_target_is_harder_at_fixed_prefix() -> None:
    qubit = optimal_prefix_embezzlement_record(
        site_count=20,
        target_dimension=2,
    )
    ququart = optimal_prefix_embezzlement_record(
        site_count=20,
        target_dimension=4,
    )
    assert qubit["optimal_half_trace_distance"] < ququart[
        "optimal_half_trace_distance"
    ]


def test_cylinder_surrogate_is_exact_on_declared_support() -> None:
    record = cylinder_type_i_surrogate_record(site_count=6)
    assert record["hilbert_dimension"] == 64
    assert record["surrogate_type"] == "Type I finite"
    assert record["state_error"] == 0
    assert record["product_error"] == 0
    assert record["modular_dynamics_error"] == 0


def test_protocol_budget_closes_the_declared_resource_ledger() -> None:
    budget = FiniteCertificationBudget(
        probe_dimension=4,
        channel_calls=7,
        energy_cap=12.0,
        duration=5.0,
        accessible_site_count=16,
    ).as_record()
    assert budget["adaptive"] is True
    assert budget["output_metric"] == "half_trace_distance"
    assert "no support-from-energy" in budget["ledger_boundary"]


@pytest.mark.parametrize(
    ("function", "kwargs"),
    (
        (adaptive_protocol_distance_upper_bound, {"per_call_channel_distance": -0.1, "channel_calls": 1}),
        (adaptive_protocol_distance_upper_bound, {"per_call_channel_distance": 0.1, "channel_calls": 0}),
        (embezzlement_dimension_lower_bound, {"target_dimension": 1, "half_trace_distance": 0.1}),
        (optimal_prefix_embezzlement_record, {"site_count": 0}),
        (optimal_prefix_embezzlement_record, {"site_count": 2, "beta": 0.0}),
        (cylinder_type_i_surrogate_record, {"site_count": 0}),
        (FiniteCertificationBudget, {"probe_dimension": 2, "channel_calls": 1, "energy_cap": -1.0, "duration": 1.0, "accessible_site_count": 2}),
        (FiniteCertificationBudget, {"probe_dimension": 2, "channel_calls": 1, "energy_cap": 1.0, "duration": 1.0, "accessible_site_count": 2, "output_metric": "operator_norm"}),
    ),
)
def test_input_validation(function, kwargs) -> None:
    with pytest.raises(ValueError):
        function(**kwargs)
