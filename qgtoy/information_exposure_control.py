"""Known-theorem control bounds for directional information exposure.

The functions in this module deliberately separate three notions that are easy
to conflate:

* KSW full-channel recovery error, measured in the unnormalized diamond norm;
* pure-orbit recovery infidelity in the Marvian--Spekkens setting; and
* finite-capacity counterexamples based on redundant coherent tokens.

These are control results and adversarial checks, not a new Paper U theorem.
"""

from __future__ import annotations

from math import comb, isfinite, log, sqrt

from .global_so3_reference_risk import SO3_ASYMMETRY_RISK_CONSTANT


SO3_HAAR_RANDOM_RISK = 0.75


def _probability(name: str, value: float) -> float:
    value = float(value)
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must lie in [0,1]")
    return value


def _dimension(name: str, value: int, *, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer at least {minimum}")
    return value


def postselected_unconditional_risk(
    *,
    success_probability: float,
    success_risk: float,
    failure_risk: float = SO3_HAAR_RANDOM_RISK,
) -> float:
    """Include the failure branch in the operational Haar risk."""
    probability = _probability("success_probability", success_probability)
    success = _probability("success_risk", success_risk)
    failure = _probability("failure_risk", failure_risk)
    return probability * success + (1.0 - probability) * failure


def ksw_channel_recovery_error_lower_bound(record_risk: float) -> float:
    """Return the KSW control floor on raw diamond recovery error.

    If ``N`` is the source-remnant channel and ``L`` is any post-processing of
    its complement used as the record, define

    ``delta_ch=inf_R ||R o N-id||_diamond``.

    Haar directional risk ``R`` from ``L`` then implies

    ``delta_ch >= [3/4-R]_+^2``.

    The diamond norm here is not divided by two.
    """
    risk = _probability("record_risk", record_risk)
    return max(0.0, SO3_HAAR_RANDOM_RISK - risk) ** 2


def ksw_postselected_channel_recovery_error_lower_bound(
    *,
    success_probability: float,
    success_risk: float,
) -> float:
    """KSW floor for one unconditional flagged postselected channel."""
    risk = postselected_unconditional_risk(
        success_probability=success_probability,
        success_risk=success_risk,
    )
    return ksw_channel_recovery_error_lower_bound(risk)


def binary_entropy(probability: float) -> float:
    """Binary entropy in nats, with continuous endpoint values."""
    probability = _probability("probability", probability)
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * log(probability) - (1.0 - probability) * log(
        1.0 - probability
    )


def finite_entropy_continuity_envelope(
    trace_distance: float,
    record_dimension: int,
) -> float:
    """Bound record mutual information for states near one replacer.

    This is ``min(log d, 2 a_d(t))``, where ``a_d`` is the sharp finite-state
    entropy continuity envelope used twice: once for each conditional record
    state and once for their average.
    """
    distance = _probability("trace_distance", trace_distance)
    dimension = _dimension("record_dimension", record_dimension, minimum=2)
    if distance <= 1.0 - 1.0 / dimension:
        entropy_delta = binary_entropy(distance) + distance * log(dimension - 1)
    else:
        entropy_delta = log(dimension)
    return min(log(dimension), 2.0 * entropy_delta)


def inverse_finite_entropy_continuity_envelope(
    information_nats: float,
    record_dimension: int,
) -> float:
    """Generalized inverse of ``finite_entropy_continuity_envelope``."""
    dimension = _dimension("record_dimension", record_dimension, minimum=2)
    information_nats = float(information_nats)
    if not isfinite(information_nats) or information_nats < 0.0:
        raise ValueError("information_nats must be finite and nonnegative")
    if information_nats == 0.0:
        return 0.0
    if information_nats > log(dimension):
        return float("inf")

    lower = 0.0
    upper = 1.0 - 1.0 / dimension
    for _ in range(200):
        midpoint = 0.5 * (lower + upper)
        if finite_entropy_continuity_envelope(midpoint, dimension) < information_nats:
            lower = midpoint
        else:
            upper = midpoint
    return 0.5 * (lower + upper)


def coarse_so3_rate_distortion_lower_bound(record_risk: float) -> float:
    """Return the repository's explicit coarse Haar information lower bound."""
    risk = _probability("record_risk", record_risk)
    if risk == 0.0:
        return float("inf")
    return max(0.0, 1.5 * log(SO3_ASYMMETRY_RISK_CONSTANT / risk))


def finite_record_ksw_control_record(
    *,
    record_risk: float,
    record_dimension: int,
    information_lower_bound_nats: float | None = None,
) -> dict[str, float | bool | int | str]:
    """Combine direct-risk and finite-record entropic KSW controls."""
    risk = _probability("record_risk", record_risk)
    dimension = _dimension("record_dimension", record_dimension, minimum=2)
    information = (
        coarse_so3_rate_distortion_lower_bound(risk)
        if information_lower_bound_nats is None
        else float(information_lower_bound_nats)
    )
    if information < 0.0 or (not isfinite(information) and information != float("inf")):
        raise ValueError("information_lower_bound_nats must be nonnegative")

    inverse = (
        float("inf")
        if information == float("inf")
        else inverse_finite_entropy_continuity_envelope(information, dimension)
    )
    direct = ksw_channel_recovery_error_lower_bound(risk)
    excluded = inverse == float("inf")
    entropic = float("inf") if excluded else inverse**2
    combined = max(direct, entropic)
    return {
        "record_risk": risk,
        "record_dimension": dimension,
        "information_lower_bound_nats": information,
        "direct_risk_diamond_error_floor": direct,
        "entropic_diamond_error_floor": entropic,
        "combined_diamond_error_floor": combined,
        "finite_record_excluded": excluded,
        "diamond_norm_is_halved": False,
        "claim_boundary": (
            "Known KSW plus finite-dimensional entropy continuity; this is a "
            "full-channel control, not an orbit-recovery or local-action theorem."
        ),
    }


def marvian_spekkens_pure_orbit_recovery_floor(
    *,
    record_risk: float,
    minimum_source_orbit_fidelity: float,
) -> float:
    """Weak full-Haar corollary of the pure-state broadcasting tradeoff.

    Covariance and the Haar risk imply that some group element separates the
    record state from its translate by trace distance at least ``3/4-R``.  If
    every source translate has fidelity at least ``q_min`` with the fiducial
    pure source, Marvian--Spekkens Eq. (6) gives the returned floor on
    source-only covariant recovery infidelity.
    """
    risk = _probability("record_risk", record_risk)
    minimum_fidelity = _probability(
        "minimum_source_orbit_fidelity",
        minimum_source_orbit_fidelity,
    )
    gap = max(0.0, SO3_HAAR_RANDOM_RISK - risk)
    record_fidelity_asymmetry = 1.0 - sqrt(max(0.0, 1.0 - gap * gap))
    return (minimum_fidelity * record_fidelity_asymmetry / 4.0) ** 2


def symmetric_subspace_dimension(state_dimension: int, copies: int) -> int:
    """Dimension of the symmetric ``copies``-particle subspace."""
    dimension = _dimension("state_dimension", state_dimension, minimum=2)
    copies = _dimension("copies", copies, minimum=1)
    return comb(copies + dimension - 1, copies)


def universal_cloner_global_recovery_fidelity(
    *,
    state_dimension: int,
    input_copies: int,
    output_copies: int,
) -> float:
    """Global fidelity of the universal ``n -> m`` pure-state cloner."""
    dimension = _dimension("state_dimension", state_dimension, minimum=2)
    inputs = _dimension("input_copies", input_copies, minimum=1)
    outputs = _dimension("output_copies", output_copies, minimum=inputs)
    return symmetric_subspace_dimension(
        dimension, inputs
    ) / symmetric_subspace_dimension(dimension, outputs)


def redundant_transfer_recovery_error_upper_bound(
    *,
    state_dimension: int,
    retained_copies: int,
    transferred_copies: int,
) -> float:
    """Counterexample bound after coherently transferring redundant copies."""
    retained = _dimension("retained_copies", retained_copies, minimum=1)
    transferred = _dimension("transferred_copies", transferred_copies, minimum=1)
    fidelity = universal_cloner_global_recovery_fidelity(
        state_dimension=state_dimension,
        input_copies=retained,
        output_copies=retained + transferred,
    )
    return 1.0 - fidelity
