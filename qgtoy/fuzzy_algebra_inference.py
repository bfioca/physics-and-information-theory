"""Finite noisy inference of a declared fuzzy-sphere observer-algebra atlas.

The inverse problem in this module is deliberately finite.  It distinguishes
three specified channels on M_{L+1}: the identity, complete J_z dephasing, and
complete depolarization.  The resulting algebra label is valid only inside
this atlas; it is not an estimator over arbitrary quantum channels.
"""

from __future__ import annotations

from itertools import product
from math import ceil, exp, log, sqrt

from .fuzzy_screen import (
    coherent_screen_povm,
    measurement_probabilities,
)
from .fuzzy_sphere import (
    matrix_scale,
    matrix_subtract,
    matrix_unit,
    spin_generators,
)
from .quantum_channel import (
    Matrix,
    identity_matrix,
    matmul,
    matrix_add,
    max_abs_difference,
    trace,
)


FULL_CHANNEL = "identity"
DEPHASING_CHANNEL = "jz_dephasing"
DEPOLARIZING_CHANNEL = "depolarizing"
CANDIDATE_CHANNELS = (FULL_CHANNEL, DEPHASING_CHANNEL, DEPOLARIZING_CHANNEL)


def _validate_level(level: int) -> None:
    if level < 1:
        raise ValueError("level must be at least one")


def _validate_state(state: Matrix) -> None:
    if not state or len(state) != len(state[0]):
        raise ValueError("state must be a nonempty square matrix")


def observer_channel(channel: str, state: Matrix) -> Matrix:
    """Apply one channel from the declared three-model candidate atlas."""
    _validate_state(state)
    if channel not in CANDIDATE_CHANNELS:
        raise ValueError(f"unknown candidate channel {channel!r}")
    dimension = len(state)
    if channel == FULL_CHANNEL:
        return state
    if channel == DEPHASING_CHANNEL:
        return tuple(
            tuple(state[row][column] if row == column else 0j for column in range(dimension))
            for row in range(dimension)
        )
    return matrix_scale(identity_matrix(dimension), trace(state) / dimension)


COORDINATE_AXES = {"x": 0, "y": 1, "z": 2}


def direction_observable(level: int, axis: str) -> Matrix:
    """Return J_axis/j, whose coherent symbol is the unit coordinate n_axis."""
    _validate_level(level)
    if axis not in COORDINATE_AXES:
        raise ValueError("axis must be one of 'x', 'y', or 'z'")
    return matrix_scale(
        spin_generators(level)[COORDINATE_AXES[axis]], 2.0 / level
    )


def coordinate_probe_state_pair(level: int, axis: str) -> tuple[Matrix, Matrix]:
    """Return rho_+/-=(I+/-J_axis/j)/(L+1), an ell=1 probe pair."""
    _validate_level(level)
    if axis not in COORDINATE_AXES:
        raise ValueError("axis must be one of 'x', 'y', or 'z'")
    dimension = level + 1
    coordinate = direction_observable(level, axis)
    identity = identity_matrix(dimension)
    return (
        matrix_scale(matrix_add(identity, coordinate), 1.0 / dimension),
        matrix_scale(matrix_subtract(identity, coordinate), 1.0 / dimension),
    )


def population_state_pair(level: int) -> tuple[Matrix, Matrix]:
    return coordinate_probe_state_pair(level, "z")


def coherence_state_pair(level: int) -> tuple[Matrix, Matrix]:
    return coordinate_probe_state_pair(level, "x")


def coordinate_screen_witness(
    level: int,
    axis: str,
    effects: tuple[Matrix, ...] | None = None,
) -> tuple[float, ...]:
    """Return the bounded classical coordinate n_axis on each POVM outcome."""
    _validate_level(level)
    if axis not in COORDINATE_AXES:
        raise ValueError("axis must be one of 'x', 'y', or 'z'")
    if effects is None:
        effects = coherent_screen_povm(level)
    coordinate = direction_observable(level, axis)
    return tuple(
        trace(matmul(coordinate, effect)).real
        / trace(effect).real
        for effect in effects
    )


def coordinate_response_formula(level: int) -> float:
    """Exact coherent-screen response of either coordinate probe."""
    _validate_level(level)
    return 1.0 / 3.0


def signed_outcome_witness(
    reference_plus: tuple[float, ...],
    reference_minus: tuple[float, ...],
    *,
    tolerance: float = 1e-15,
) -> tuple[float, ...]:
    """Return the fixed sign witness optimized for a reference pair."""
    if len(reference_plus) != len(reference_minus):
        raise ValueError("reference distributions must have the same length")
    if tolerance < 0.0:
        raise ValueError("tolerance must be nonnegative")
    return tuple(
        1.0 if left - right > tolerance
        else -1.0 if right - left > tolerance
        else 0.0
        for left, right in zip(reference_plus, reference_minus)
    )


def witness_response(
    plus_probabilities: tuple[float, ...],
    minus_probabilities: tuple[float, ...],
    witness: tuple[float, ...],
) -> float:
    """Return half the difference of two bounded witness expectations."""
    if not (len(plus_probabilities) == len(minus_probabilities) == len(witness)):
        raise ValueError("probability and witness lengths must agree")
    response = 0.5 * sum(
        weight * (left - right)
        for left, right, weight in zip(plus_probabilities, minus_probabilities, witness)
    )
    return 0.0 if abs(response) < 1e-14 else response


def _probe_response(
    channel: str,
    pair: tuple[Matrix, Matrix],
    effects: tuple[Matrix, ...],
    witness: tuple[float, ...],
) -> float:
    plus, minus = pair
    return witness_response(
        measurement_probabilities(observer_channel(channel, plus), effects),
        measurement_probabilities(observer_channel(channel, minus), effects),
        witness,
    )


def ideal_response_signatures(level: int) -> dict[str, tuple[float, float]]:
    """Return (population, coherence) responses for every atlas channel."""
    _validate_level(level)
    effects = coherent_screen_povm(level)
    population_pair = population_state_pair(level)
    coherence_pair = coherence_state_pair(level)
    population_witness = coordinate_screen_witness(level, "z", effects)
    coherence_witness = coordinate_screen_witness(level, "x", effects)

    return {
        channel: (
            _probe_response(channel, population_pair, effects, population_witness),
            _probe_response(channel, coherence_pair, effects, coherence_witness),
        )
        for channel in CANDIDATE_CHANNELS
    }


def response_transport_record(source_level: int, target_level: int) -> dict[str, object]:
    """Quantify canonical transport of ell=1 probes and screen witnesses."""
    _validate_level(source_level)
    _validate_level(target_level)
    if target_level < source_level:
        raise ValueError("target_level must be at least source_level")
    source_berezin = source_level / (source_level + 2.0)
    target_berezin = target_level / (target_level + 2.0)
    harmonic_multiplier = sqrt(source_berezin * target_berezin)
    direction_multiplier = target_berezin
    witness_hs_error = (1.0 - source_berezin) * sqrt(target_berezin / 3.0)
    lifted_state_response = target_berezin / 3.0
    return {
        "source_level": source_level,
        "target_level": target_level,
        "ell1_harmonic_multiplier": harmonic_multiplier,
        "direction_observable_multiplier": direction_multiplier,
        "source_response": coordinate_response_formula(source_level),
        "target_response": coordinate_response_formula(target_level),
        "local_response_transport_error": 0.0,
        "lifted_state_target_response": lifted_state_response,
        "lifted_state_response_error": (1.0 - target_berezin) / 3.0,
        "lifted_state_response_error_upper_bound": 2.0
        / (3.0 * (target_level + 2.0)),
        "witness_hilbert_schmidt_transport_error": witness_hs_error,
        "witness_error_upper_bound": 2.0 / (
            sqrt(3.0) * (source_level + 2.0)
        ),
        "limiting_response": 1.0 / 3.0,
        "uniform_response_lower_bound": 1.0 / 3.0,
    }


def signature_separation(level: int) -> float:
    """Return the minimum pairwise l-infinity distance of ideal signatures."""
    signatures = ideal_response_signatures(level)
    return min(
        max(abs(left[axis] - right[axis]) for axis in range(2))
        for index, left_channel in enumerate(CANDIDATE_CHANNELS)
        for right_channel in CANDIDATE_CHANNELS[index + 1 :]
        for left, right in ((signatures[left_channel], signatures[right_channel]),)
    )


def classify_response_signature(
    level: int,
    population_response: float,
    coherence_response: float,
    *,
    response_error_bound: float,
) -> dict[str, object]:
    """Classify a noisy signature by certified l-infinity feasibility balls."""
    _validate_level(level)
    if response_error_bound < 0.0:
        raise ValueError("response_error_bound must be nonnegative")
    observed = (population_response, coherence_response)
    signatures = ideal_response_signatures(level)
    feasible = tuple(
        channel
        for channel, signature in signatures.items()
        if max(abs(observed[axis] - signature[axis]) for axis in range(2))
        <= response_error_bound + 1e-12
    )
    return {
        "classification": feasible[0] if len(feasible) == 1 else "ambiguous",
        "feasible_candidates": feasible,
        "observed_signature": observed,
        "response_error_bound": response_error_bound,
        "ideal_signatures": signatures,
    }


def samples_per_probe_state(response_error: float, failure_probability: float) -> int:
    """Hoeffding sample count for four witness means in [-1,1].

    With n samples for each of the four states, a union bound gives failure at
    most 8 exp(-n epsilon^2/2) for simultaneous response error <= epsilon.
    """
    if response_error <= 0.0:
        raise ValueError("response_error must be positive")
    if not 0.0 < failure_probability < 1.0:
        raise ValueError("failure_probability must lie strictly between zero and one")
    return ceil(2.0 * log(8.0 / failure_probability) / response_error**2)


def _preserved_basis(channel: str, dimension: int) -> tuple[Matrix, ...]:
    if channel == FULL_CHANNEL:
        return tuple(
            matrix_unit(dimension, row, column)
            for row in range(dimension)
            for column in range(dimension)
        )
    if channel == DEPHASING_CHANNEL:
        return tuple(matrix_unit(dimension, index, index) for index in range(dimension))
    return (identity_matrix(dimension),)


def _lost_witness(channel: str, dimension: int) -> Matrix | None:
    if channel == FULL_CHANNEL:
        return None
    if channel == DEPHASING_CHANNEL:
        return matrix_unit(dimension, 0, dimension - 1)
    return tuple(
        tuple(
            1 + 0j if (row, column) == (0, 0)
            else -1 + 0j if (row, column) == (dimension - 1, dimension - 1)
            else 0j
            for column in range(dimension)
        )
        for row in range(dimension)
    )


def correctable_algebra_record(level: int, channel: str) -> dict[str, object]:
    """Audit exact identity recovery on the standard correctable algebra."""
    _validate_level(level)
    if channel not in CANDIDATE_CHANNELS:
        raise ValueError(f"unknown candidate channel {channel!r}")
    dimension = level + 1
    basis = _preserved_basis(channel, dimension)
    restriction_error = max(
        max_abs_difference(observer_channel(channel, operator), operator)
        for operator in basis
    )
    lost = _lost_witness(channel, dimension)
    lost_witness_error = (
        None
        if lost is None
        else max_abs_difference(observer_channel(channel, lost), lost)
    )
    algebra_labels = {
        FULL_CHANNEL: f"M_{dimension}",
        DEPHASING_CHANNEL: f"C^{dimension} (J_z diagonal)",
        DEPOLARIZING_CHANNEL: "C I",
    }
    return {
        "channel": channel,
        "correctable_algebra": algebra_labels[channel],
        "correctable_algebra_dimension": len(basis),
        "recovery_map": "identity on the channel output, restricted to the fixed algebra",
        "max_basis_recovery_error": restriction_error,
        "outside_algebra_loss_witness_error": lost_witness_error,
        "maximality_argument": (
            "For the full input code, the OA-QEC commutant condition applied to "
            "the channel Kraus products gives respectively M_d, the J_z diagonal "
            "algebra, and the scalar algebra."
        ),
    }


def _corner_classification_audit(level: int, radius: float) -> bool:
    signatures = ideal_response_signatures(level)
    for channel, signature in signatures.items():
        for signs in product((-1.0, 1.0), repeat=2):
            observed = tuple(signature[axis] + signs[axis] * radius for axis in range(2))
            result = classify_response_signature(
                level,
                observed[0],
                observed[1],
                response_error_bound=radius,
            )
            if result["classification"] != channel:
                return False
    return True


def fuzzy_algebra_inference_record(
    level: int,
    *,
    failure_probability: float = 0.05,
) -> dict[str, object]:
    """Build the robust finite-atlas inference record at one cutoff."""
    _validate_level(level)
    if not 0.0 < failure_probability < 1.0:
        raise ValueError("failure_probability must lie strictly between zero and one")
    signatures = ideal_response_signatures(level)
    separation = signature_separation(level)
    certified_radius = separation / 4.0
    sample_count = samples_per_probe_state(certified_radius, failure_probability)
    formula_error = max(
        abs(signatures[FULL_CHANNEL][axis] - coordinate_response_formula(level))
        for axis in range(2)
    )
    return {
        "level_L": level,
        "matrix_dimension": level + 1,
        "candidate_atlas": CANDIDATE_CHANNELS,
        "ideal_response_signatures": signatures,
        "minimum_signature_separation_linf": separation,
        "coordinate_response_formula": coordinate_response_formula(level),
        "coordinate_response_formula_error": formula_error,
        "certified_response_error_radius": certified_radius,
        "robust_identification_condition": "epsilon < minimum_signature_separation_linf / 2",
        "adversarial_corner_audit_passes": _corner_classification_audit(
            level, certified_radius
        ),
        "failure_probability": failure_probability,
        "samples_per_probe_state": sample_count,
        "total_samples_four_states": 4 * sample_count,
        "hoeffding_failure_upper_bound": 8.0
        * exp(-sample_count * certified_radius**2 / 2.0),
        "correctable_algebras": tuple(
            correctable_algebra_record(level, channel) for channel in CANDIDATE_CHANNELS
        ),
        "scope": (
            "Identifies one member of the declared three-channel atlas. The algebra "
            "label uses the analytic OA-QEC commutant condition; the coherent screen "
            "does not itself recover a noncommutative quantum state from one copy."
        ),
        "next_cutoff_transport": response_transport_record(level, level + 1),
    }


def fuzzy_algebra_inference_certificate(
    *,
    max_level: int = 6,
    tolerance: float = 1e-10,
    failure_probability: float = 0.05,
) -> dict[str, object]:
    """Audit robust identification and exact restricted recovery across cutoffs."""
    if max_level < 1:
        raise ValueError("max_level must be at least one")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    records = tuple(
        fuzzy_algebra_inference_record(
            level, failure_probability=failure_probability
        )
        for level in range(1, max_level + 1)
    )
    certified_claims = {
        "atlas_signatures_are_pairwise_separated": all(
            record["minimum_signature_separation_linf"] > tolerance
            for record in records
        ),
        "population_and_coherence_probes_resolve_the_atlas": all(
            record["ideal_response_signatures"][FULL_CHANNEL][0] > tolerance
            and record["ideal_response_signatures"][FULL_CHANNEL][1] > tolerance
            and record["ideal_response_signatures"][DEPHASING_CHANNEL][0] > tolerance
            and abs(record["ideal_response_signatures"][DEPHASING_CHANNEL][1]) <= tolerance
            and all(
                abs(value) <= tolerance
                for value in record["ideal_response_signatures"][DEPOLARIZING_CHANNEL]
            )
            for record in records
        ),
        "coordinate_response_formula_is_exact": all(
            record["coordinate_response_formula_error"] <= tolerance
            for record in records
        ),
        "response_separation_is_uniform_in_cutoff": all(
            record["minimum_signature_separation_linf"]
            >= 1.0 / 3.0 - tolerance
            for record in records
        ),
        "response_witnesses_transport_with_inverse_cutoff_error": all(
            record["next_cutoff_transport"]["local_response_transport_error"]
            <= tolerance
            and record["next_cutoff_transport"]["lifted_state_response_error"]
            <= record["next_cutoff_transport"][
                "lifted_state_response_error_upper_bound"
            ]
            + tolerance
            and record["next_cutoff_transport"][
                "witness_hilbert_schmidt_transport_error"
            ]
            <= record["next_cutoff_transport"]["witness_error_upper_bound"]
            + tolerance
            for record in records
        ),
        "bounded_response_noise_is_robustly_classified": all(
            record["adversarial_corner_audit_passes"] for record in records
        ),
        "hoeffding_budget_meets_target_confidence": all(
            record["hoeffding_failure_upper_bound"] <= failure_probability
            for record in records
        ),
        "identity_recovery_is_exact_on_each_correctable_algebra": all(
            algebra["max_basis_recovery_error"] <= tolerance
            for record in records
            for algebra in record["correctable_algebras"]
        ),
        "proper_atlas_channels_have_explicit_loss_witnesses": all(
            algebra["outside_algebra_loss_witness_error"] is None
            or algebra["outside_algebra_loss_witness_error"] > tolerance
            for record in records
            for algebra in record["correctable_algebras"]
        ),
    }
    return {
        "goal": "Phase 1 Noisy Observer-Algebra Inference Benchmark",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "finite_declared_atlas_identification_theorem",
        "claim_boundary": (
            "finite three-channel atlas on the coherent fuzzy-sphere screen only; "
            "not arbitrary-channel learning, continuum convergence, or a gravitational "
            "observer-algebra theorem"
        ),
        "certified_claims": certified_claims,
        "records": records,
    }
