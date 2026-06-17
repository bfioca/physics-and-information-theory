"""Finite-resource controls for operational von Neumann type certification.

The infinite alternating Gibbs product state used by
``modular_manybody_regulator`` generates the hyperfinite Type-III_1 factor in
its GNS representation.  Every finite prefix is nevertheless an ordinary
Type-I matrix system.  This module quantifies one operational route between
those statements: catalytic entanglement embezzlement.

The calculations are controls and finite-model diagnostics.  They do not prove
that a static-patch observer can implement the required local unitaries.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil, comb, exp, inf, isfinite, log, sqrt
from sys import float_info

from .modular_manybody_regulator import site_gibbs_weights


_OUTPUT_METRICS = frozenset(
    {
        "half_trace_distance",
        "total_variation_distance",
        "energy_constrained_half_diamond",
    }
)


@dataclass(frozen=True)
class FiniteCertificationBudget:
    """Declared resources for one finite algebra-certification protocol.

    The energy and duration fields are ledgers, not a claimed derivation of a
    finite support cutoff.  A physical model must separately prove such a
    relation before the exact cylinder control can be applied to it.
    """

    probe_dimension: int
    channel_calls: int
    energy_cap: float
    duration: float
    accessible_site_count: int
    adaptive: bool = True
    output_metric: str = "half_trace_distance"

    def __post_init__(self) -> None:
        _positive_integer("probe_dimension", self.probe_dimension)
        _positive_integer("channel_calls", self.channel_calls)
        _positive_integer("accessible_site_count", self.accessible_site_count)
        for name, value in (
            ("energy_cap", self.energy_cap),
            ("duration", self.duration),
        ):
            value = float(value)
            if not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
            object.__setattr__(self, name, value)
        if not isinstance(self.adaptive, bool):
            raise ValueError("adaptive must be boolean")
        if self.output_metric not in _OUTPUT_METRICS:
            allowed = ", ".join(sorted(_OUTPUT_METRICS))
            raise ValueError(f"output_metric must be one of: {allowed}")

    def as_record(self) -> dict[str, float | int | bool | str]:
        record = asdict(self)
        record.update(
            {
                "locality_domain": "first m tensor factors",
                "postselection_policy": "unconditional, with every flag retained",
                "ledger_boundary": (
                    "energy and duration are declared caps; no support-from-"
                    "energy or support-from-duration theorem is assumed"
                ),
            }
        )
        return record


def _positive_integer(name: str, value: int, *, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer at least {minimum}")
    return value


def _probability(name: str, value: float, *, include_zero: bool = True) -> float:
    value = float(value)
    lower_ok = value >= 0.0 if include_zero else value > 0.0
    if not isfinite(value) or not lower_ok or value >= 1.0:
        interval = "[0,1)" if include_zero else "(0,1)"
        raise ValueError(f"{name} must lie in {interval}")
    return value


def binary_entropy(probability: float) -> float:
    """Binary entropy in nats."""
    probability = float(probability)
    if not isfinite(probability) or not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * log(probability) - (1.0 - probability) * log(
        1.0 - probability
    )


def adaptive_protocol_distance_upper_bound(
    *,
    per_call_channel_distance: float,
    channel_calls: int,
) -> float:
    """Hybrid bound for an adaptive protocol using nearby channels.

    ``per_call_channel_distance`` and the result use the halved diamond or
    energy-constrained diamond convention, so both lie in ``[0,1]``.  Arbitrary
    intervening channels, memories, and adaptive controls are allowed.
    """
    distance = _probability(
        "per_call_channel_distance",
        per_call_channel_distance,
    )
    calls = _positive_integer("channel_calls", channel_calls)
    return min(1.0, calls * distance)


def embezzlement_dimension_lower_bound(
    *,
    target_dimension: int,
    half_trace_distance: float,
) -> int | float:
    """Necessary catalyst dimension from entropy continuity.

    Let a pure catalyst have local Schmidt dimension ``D``.  Local unitaries
    preserve its marginal entropy.  Producing a maximally entangled target of
    Schmidt rank ``k`` while returning the catalyst within half trace distance
    ``t`` requires, by the Audenaert entropy-continuity bound,

    ``log(k) <= t log(D k - 1) + h_2(t)``.

    The returned integer is the resulting lower bound on ``D``. Perfect
    finite-dimensional embezzlement is impossible and is represented by
    ``inf``. The same sentinel is used if a nonzero-error dimension floor
    exceeds floating-point range; use
    :func:`embezzlement_log_dimension_lower_bound` in that regime.
    """
    target = _positive_integer("target_dimension", target_dimension, minimum=2)
    distance = _probability("half_trace_distance", half_trace_distance)
    if distance == 0.0:
        return inf

    log_lower = embezzlement_log_dimension_lower_bound(
        target_dimension=target,
        half_trace_distance=distance,
    )
    if log_lower > log(float_info.max):
        return inf
    lower = exp(log_lower)
    return max(1, ceil(lower - 1e-14))


def embezzlement_log_dimension_lower_bound(
    *,
    target_dimension: int,
    half_trace_distance: float,
) -> float:
    """Natural logarithm of the entropy-continuity dimension floor.

    This form remains finite for every nonzero error even when the dimension
    itself is too large for a floating-point representation.
    """
    target = _positive_integer("target_dimension", target_dimension, minimum=2)
    distance = _probability("half_trace_distance", half_trace_distance)
    if distance == 0.0:
        return inf

    exponent = (log(target) - binary_entropy(distance)) / distance
    maximum = max(0.0, exponent)
    log_one_plus_exp = maximum + log(
        exp(-maximum) + exp(exponent - maximum)
    )
    return max(0.0, log_one_plus_exp - log(target))


def embezzlement_site_lower_bound(
    *,
    target_dimension: int,
    half_trace_distance: float,
    local_site_dimension: int = 2,
) -> int | float:
    """Translate the entropy dimension floor into a number of local sites."""
    site_dimension = _positive_integer(
        "local_site_dimension",
        local_site_dimension,
        minimum=2,
    )
    log_dimension = embezzlement_log_dimension_lower_bound(
        target_dimension=target_dimension,
        half_trace_distance=half_trace_distance,
    )
    if log_dimension == inf:
        return inf
    return max(0, ceil(log_dimension / log(site_dimension) - 1e-14))


def _itpfi_schmidt_blocks(
    *,
    site_count: int,
    beta: float,
) -> tuple[tuple[float, int], ...]:
    """Return descending ``(log probability, multiplicity)`` blocks."""
    sites = _positive_integer("site_count", site_count)
    beta = float(beta)
    if not isfinite(beta) or beta <= 0.0:
        raise ValueError("beta must be finite and positive")

    odd_sites = (sites + 1) // 2
    even_sites = sites // 2
    odd_weights = site_gibbs_weights(1, beta=beta)
    even_weights = site_gibbs_weights(2, beta=beta)
    blocks = []
    for odd_excited in range(odd_sites + 1):
        odd_log_probability = (
            (odd_sites - odd_excited) * log(odd_weights[0])
            + odd_excited * log(odd_weights[1])
        )
        odd_multiplicity = comb(odd_sites, odd_excited)
        for even_excited in range(even_sites + 1):
            even_log_probability = (
                (even_sites - even_excited) * log(even_weights[0])
                + even_excited * log(even_weights[1])
            )
            blocks.append(
                (
                    odd_log_probability + even_log_probability,
                    odd_multiplicity * comb(even_sites, even_excited),
                )
            )
    return tuple(sorted(blocks, key=lambda block: block[0], reverse=True))


def optimal_prefix_embezzlement_record(
    *,
    site_count: int,
    target_dimension: int = 2,
    beta: float = 1.0,
) -> dict[str, float | int | str]:
    """Exact finite-spectrum optimum under local unitaries.

    The initial catalyst has Schmidt probabilities ``p`` and a separable target
    register.  The desired state has Schmidt probabilities ``p/k``, each
    repeated ``k`` times.  Local unitaries preserve Schmidt coefficients, so
    the rearrangement inequality makes the maximum root fidelity the overlap
    of the two descending Schmidt spectra.  Multiplicity blocks avoid storing
    all ``2**site_count`` entries.
    """
    sites = _positive_integer("site_count", site_count)
    target = _positive_integer("target_dimension", target_dimension, minimum=2)
    blocks = _itpfi_schmidt_blocks(site_count=sites, beta=beta)

    initial_index = 0
    target_index = 0
    initial_remaining = blocks[0][1]
    target_remaining = blocks[0][1] * target
    matched_entries = 0
    local_dimension = 2**sites
    root_fidelity = 0.0
    target_log_shift = log(target)

    while matched_entries < local_dimension:
        take = min(
            initial_remaining,
            target_remaining,
            local_dimension - matched_entries,
        )
        initial_log_probability = blocks[initial_index][0]
        target_log_probability = blocks[target_index][0] - target_log_shift
        root_fidelity += take * exp(
            0.5 * (initial_log_probability + target_log_probability)
        )
        matched_entries += take
        initial_remaining -= take
        target_remaining -= take

        if initial_remaining == 0 and matched_entries < local_dimension:
            initial_index += 1
            initial_remaining = blocks[initial_index][1]
        if target_remaining == 0 and matched_entries < local_dimension:
            target_index += 1
            target_remaining = blocks[target_index][1] * target

    root_fidelity = min(1.0, max(0.0, root_fidelity))
    half_trace_distance = sqrt(max(0.0, 1.0 - root_fidelity**2))
    return {
        "site_count": sites,
        "local_catalyst_dimension": local_dimension,
        "target_dimension": target,
        "beta": float(beta),
        "schmidt_block_count": len(blocks),
        "optimal_root_fidelity": root_fidelity,
        "optimal_half_trace_distance": half_trace_distance,
        "optimal_raw_trace_distance": 2.0 * half_trace_distance,
        "optimization": "descending Schmidt-spectrum rearrangement",
        "finite_prefix_type": "Type I finite",
        "infinite_limit_type": "hyperfinite Type III_1 (theorem-backed)",
        "claim_boundary": (
            "finite-prefix local-unitary optimum only; no energy, time, "
            "locality, or static-patch implementation cost is derived"
        ),
    }


def cylinder_type_i_surrogate_record(*, site_count: int) -> dict[str, int | str]:
    """Exact Type-I surrogate for cylinder protocols on a finite prefix."""
    sites = _positive_integer("site_count", site_count)
    dimension = 2**sites
    return {
        "accessible_site_count": sites,
        "hilbert_dimension": dimension,
        "observable_algebra": f"M_{dimension}",
        "surrogate_type": "Type I finite",
        "state_error": 0,
        "product_error": 0,
        "modular_dynamics_error": 0,
        "scope": (
            "all states, operations, adaptive controls, and readouts supported "
            "on the declared finite cylinder"
        ),
        "reason": (
            "the product state and on-site modular dynamics restrict exactly "
            "to the first m tensor factors"
        ),
    }
