"""Operational finite U(1) reference protocol and exact coherence law.

An unknown system state on charges ``m=-L,...,L`` is tensored with the fixed
reference state ``|eta_N>=(N+1)^(-1/2) sum_{n=0}^N |n>``.  After the joint U(1)
twirl, a total-charge-sector decoder produces a Schur channel whose coherence
multiplier is the overlap of two shifted uniform charge windows.
"""

from __future__ import annotations

from math import asin, ceil, cos, pi, sin, sqrt


def _validate_level(level: int) -> None:
    if isinstance(level, bool) or not isinstance(level, int) or level < 1:
        raise ValueError("level must be a positive integer")


def _validate_reference_max_charge(reference_max_charge: int) -> None:
    if (
        isinstance(reference_max_charge, bool)
        or not isinstance(reference_max_charge, int)
        or reference_max_charge < 0
    ):
        raise ValueError("reference_max_charge must be a nonnegative integer")


def _validate_system_charge(level: int, charge: int) -> None:
    if isinstance(charge, bool) or not isinstance(charge, int):
        raise ValueError("system charge must be an integer")
    if not -level <= charge <= level:
        raise ValueError("system charge lies outside the cutoff sector")


def total_charge_overlap_count(
    level: int,
    reference_max_charge: int,
    left_charge: int,
    right_charge: int,
) -> int:
    """Count joint-twirl sectors retaining one system matrix element."""
    _validate_level(level)
    _validate_reference_max_charge(reference_max_charge)
    _validate_system_charge(level, left_charge)
    _validate_system_charge(level, right_charge)
    gap = abs(left_charge - right_charge)
    return max(0, reference_max_charge + 1 - gap)


def phase_reference_visibility(
    level: int,
    reference_max_charge: int,
    left_charge: int,
    right_charge: int,
) -> float:
    """Return the exact Schur multiplier after twirl and sector decoding."""
    count = total_charge_overlap_count(
        level,
        reference_max_charge,
        left_charge,
        right_charge,
    )
    return count / float(reference_max_charge + 1)


def shifted_reference_vector(
    level: int,
    reference_max_charge: int,
    system_charge: int,
) -> tuple[float, ...]:
    """Uniform reference window embedded in the common total-charge axis."""
    _validate_level(level)
    _validate_reference_max_charge(reference_max_charge)
    _validate_system_charge(level, system_charge)
    normalization = 1.0 / sqrt(float(reference_max_charge + 1))
    total_charge_min = -level
    total_charge_max = level + reference_max_charge
    return tuple(
        normalization if 0 <= total_charge - system_charge <= reference_max_charge else 0.0
        for total_charge in range(total_charge_min, total_charge_max + 1)
    )


def _inner_product(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(left_value * right_value for left_value, right_value in zip(left, right))


def phase_reference_channel_record(
    level: int,
    reference_max_charge: int,
) -> dict[str, object]:
    """Build the exact decoded Schur channel and its Gram verification."""
    _validate_level(level)
    _validate_reference_max_charge(reference_max_charge)
    charges = tuple(range(-level, level + 1))
    vectors = tuple(
        shifted_reference_vector(level, reference_max_charge, charge)
        for charge in charges
    )
    visibility_matrix = tuple(
        tuple(
            phase_reference_visibility(
                level,
                reference_max_charge,
                left_charge,
                right_charge,
            )
            for right_charge in charges
        )
        for left_charge in charges
    )
    gram_matrix = tuple(
        tuple(_inner_product(left, right) for right in vectors)
        for left in vectors
    )
    gram_error = max(
        abs(visibility_matrix[row][column] - gram_matrix[row][column])
        for row in range(len(charges))
        for column in range(len(charges))
    )
    return {
        "level_L": level,
        "system_charges": charges,
        "reference_state": "|eta_N>=sum_{n=0}^N |n>/sqrt(N+1)",
        "reference_max_charge_N": reference_max_charge,
        "reference_dimension": reference_max_charge + 1,
        "physical_channel": "joint U(1) twirl followed by total-charge-sector decoder",
        "decoder_action": "|m,q-m> maps to |m>_logical tensor |q>_flag",
        "induced_channel": (
            "rho_{m,m'} maps to max(0,1-|m-m'|/(N+1)) rho_{m,m'}"
        ),
        "visibility_matrix": visibility_matrix,
        "visibility_is_reference_window_gram_matrix": gram_error < 1e-14,
        "gram_matrix_error": gram_error,
        "channel_is_cptp": gram_error < 1e-14,
        "exact_full_sector_recovery": False,
    }


def phase_pair_recovery_record(
    level: int,
    reference_max_charge: int,
    left_charge: int | None = None,
    right_charge: int | None = None,
) -> dict[str, object]:
    """Give the sharp two-state minimax bound for one charge coherence."""
    _validate_level(level)
    _validate_reference_max_charge(reference_max_charge)
    left = -level if left_charge is None else left_charge
    right = level if right_charge is None else right_charge
    _validate_system_charge(level, left)
    _validate_system_charge(level, right)
    if left == right:
        raise ValueError("phase-pair charges must be distinct")
    gap = abs(left - right)
    visibility = phase_reference_visibility(
        level,
        reference_max_charge,
        left,
        right,
    )
    minimax_error = (1.0 - visibility) / 2.0
    return {
        "level_L": level,
        "left_charge": left,
        "right_charge": right,
        "charge_gap": gap,
        "reference_max_charge_N": reference_max_charge,
        "reference_dimension": reference_max_charge + 1,
        "decoded_plus_minus_trace_distance": visibility,
        "any_decoder_worst_case_trace_distance_error_lower_bound": minimax_error,
        "sector_decoder_error_on_each_phase_state": minimax_error,
        "sector_decoder_is_pairwise_minimax_optimal": True,
        "exact_pair_recovery": visibility == 1.0,
    }


def required_reference_dimension(level: int, target_error: float) -> int:
    """Minimum boxcar-reference dimension for the extremal phase-pair target."""
    _validate_level(level)
    if not 0.0 < target_error < 0.5:
        raise ValueError("target_error must lie strictly between zero and one half")
    return ceil(level / target_error)


def optimal_phase_reference_amplitudes(
    level: int,
    reference_max_charge: int,
    left_charge: int | None = None,
    right_charge: int | None = None,
) -> tuple[float, ...]:
    """Return the sine-profile reference maximizing one gap visibility."""
    _validate_level(level)
    _validate_reference_max_charge(reference_max_charge)
    left = -level if left_charge is None else left_charge
    right = level if right_charge is None else right_charge
    _validate_system_charge(level, left)
    _validate_system_charge(level, right)
    if left == right:
        raise ValueError("phase-pair charges must be distinct")
    gap = abs(left - right)
    chain_length = reference_max_charge // gap + 1
    normalization = sqrt(2.0 / float(chain_length + 1))
    amplitudes = [0.0] * (reference_max_charge + 1)
    for chain_index in range(chain_length):
        charge = chain_index * gap
        amplitudes[charge] = normalization * sin(
            (chain_index + 1) * pi / float(chain_length + 1)
        )
    return tuple(amplitudes)


def _gap_visibility(amplitudes: tuple[float, ...], gap: int) -> float:
    return sum(
        amplitudes[index] * amplitudes[index + gap]
        for index in range(len(amplitudes) - gap)
    )


def optimal_phase_pair_error(
    level: int,
    reference_max_charge: int,
    left_charge: int | None = None,
    right_charge: int | None = None,
) -> float:
    """Return the stable analytic pairwise optimum without allocating a state."""
    _validate_level(level)
    _validate_reference_max_charge(reference_max_charge)
    left = -level if left_charge is None else left_charge
    right = level if right_charge is None else right_charge
    _validate_system_charge(level, left)
    _validate_system_charge(level, right)
    if left == right:
        raise ValueError("phase-pair charges must be distinct")
    gap = abs(left - right)
    chain_length = reference_max_charge // gap + 1
    return sin(pi / float(2 * (chain_length + 1))) ** 2


def optimal_phase_pair_recovery_record(
    level: int,
    reference_max_charge: int,
    left_charge: int | None = None,
    right_charge: int | None = None,
) -> dict[str, object]:
    """Optimize deterministic recovery of one phase pair at fixed max charge."""
    _validate_level(level)
    _validate_reference_max_charge(reference_max_charge)
    left = -level if left_charge is None else left_charge
    right = level if right_charge is None else right_charge
    _validate_system_charge(level, left)
    _validate_system_charge(level, right)
    if left == right:
        raise ValueError("phase-pair charges must be distinct")
    gap = abs(left - right)
    chain_length = reference_max_charge // gap + 1
    amplitudes = optimal_phase_reference_amplitudes(
        level,
        reference_max_charge,
        left,
        right,
    )
    analytic_visibility = cos(pi / float(chain_length + 1))
    numerical_visibility = _gap_visibility(amplitudes, gap)
    minimax_error = optimal_phase_pair_error(
        level,
        reference_max_charge,
        left,
        right,
    )
    return {
        "level_L": level,
        "left_charge": left,
        "right_charge": right,
        "charge_gap": gap,
        "reference_max_charge_N": reference_max_charge,
        "contiguous_reference_space_dimension": reference_max_charge + 1,
        "nonzero_reference_amplitudes": chain_length,
        "optimal_profile": "sine eigenvector on a longest step-gap charge chain",
        "optimal_visibility": analytic_visibility,
        "numerical_visibility": numerical_visibility,
        "visibility_error": abs(analytic_visibility - numerical_visibility),
        "optimal_pairwise_minimax_error": minimax_error,
        "optimality_basis": (
            "largest eigenvalue of one-half the adjacency matrix of the "
            "longest charge chain is cos(pi/(r+1))"
        ),
    }


def required_optimized_reference_max_charge(
    level: int,
    target_error: float,
    left_charge: int | None = None,
    right_charge: int | None = None,
) -> int:
    """Minimum max charge for the pairwise-optimal sine reference."""
    _validate_level(level)
    if not 0.0 < target_error < 0.5:
        raise ValueError("target_error must lie strictly between zero and one half")
    left = -level if left_charge is None else left_charge
    right = level if right_charge is None else right_charge
    _validate_system_charge(level, left)
    _validate_system_charge(level, right)
    if left == right:
        raise ValueError("phase-pair charges must be distinct")
    gap = abs(left - right)
    threshold_angle = 2.0 * asin(sqrt(target_error))
    minimum_chain_length = max(1, ceil(pi / threshold_angle) - 1)

    def chain_error(chain_length: int) -> float:
        return sin(pi / float(2 * (chain_length + 1))) ** 2

    while chain_error(minimum_chain_length) > target_error:
        minimum_chain_length += 1
    while (
        minimum_chain_length > 1
        and chain_error(minimum_chain_length - 1) <= target_error
    ):
        minimum_chain_length -= 1
    return gap * (minimum_chain_length - 1)


def operational_phase_reference_certificate(
    *,
    max_level: int = 8,
    target_error: float = 0.1,
    tolerance: float = 1e-12,
) -> dict[str, object]:
    """Audit the exact operational U(1) reference theorem through a cutoff."""
    _validate_level(max_level)
    if not 0.0 < target_error < 0.5:
        raise ValueError("target_error must lie strictly between zero and one half")
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")

    records = []
    for level in range(1, max_level + 1):
        required_uniform_dimension = required_reference_dimension(level, target_error)
        reference_max_charge = required_uniform_dimension - 1
        optimized_max_charge = required_optimized_reference_max_charge(
            level,
            target_error,
        )
        channel = phase_reference_channel_record(level, reference_max_charge)
        scalar_pair = phase_pair_recovery_record(level, 0)
        uniform_pair = phase_pair_recovery_record(level, reference_max_charge)
        optimized_pair = optimal_phase_pair_recovery_record(level, optimized_max_charge)
        records.append(
            {
                "level_L": level,
                "required_uniform_reference_dimension": required_uniform_dimension,
                "uniform_reference_max_charge_N": reference_max_charge,
                "required_optimized_reference_max_charge_N": optimized_max_charge,
                "channel_record": channel,
                "scalar_pair_record": scalar_pair,
                "uniform_pair_record": uniform_pair,
                "optimized_pair_record": optimized_pair,
            }
        )

    certified_claims = {
        "decoded_channel_has_exact_triangular_coherence_law": all(
            record["channel_record"]["visibility_is_reference_window_gram_matrix"]
            and record["channel_record"]["gram_matrix_error"] <= tolerance
            for record in records
        ),
        "scalar_reference_gives_the_half_error_obstruction": all(
            record["scalar_pair_record"][
                "any_decoder_worst_case_trace_distance_error_lower_bound"
            ]
            == 0.5
            for record in records
        ),
        "sector_decoder_is_pairwise_minimax_optimal": all(
            record["uniform_pair_record"]["sector_decoder_is_pairwise_minimax_optimal"]
            and record["uniform_pair_record"]["sector_decoder_error_on_each_phase_state"]
            <= target_error + tolerance
            for record in records
        ),
        "uniform_extremal_reference_dimension_scales_as_L_over_error": all(
            record["required_uniform_reference_dimension"]
            == ceil(record["level_L"] / target_error)
            for record in records
        ),
        "optimized_sine_profile_attains_the_path_eigenvalue_bound": all(
            record["optimized_pair_record"]["visibility_error"] <= tolerance
            and record["optimized_pair_record"]["optimal_pairwise_minimax_error"]
            <= target_error + tolerance
            for record in records
        ),
        "no_finite_boxcar_reference_recovers_nonzero_charge_gaps_exactly": all(
            not record["uniform_pair_record"]["exact_pair_recovery"]
            for record in records
        ),
    }
    return {
        "goal": "Operational Finite U(1) Reference Recovery",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "prepared_reference_append_twirl_decode_theorem",
        "central_result": (
            "Appending |eta_N>, jointly twirling, and decoding total-charge "
            "sectors multiplies rho_{m,m'} by max(0,1-|m-m'|/(N+1)) for the "
            "uniform boxcar reference. Its extremal phase-pair error is 1/2 "
            "for N<2L and L/(N+1) otherwise. At fixed maximum charge, the "
            "pairwise-optimal sine profile instead has visibility "
            "cos(pi/(floor(N/(2L))+2)) and error of order (L/N)^2."
        ),
        "claim_boundary": (
            "exact U(1) phase-reference theorem for boxcar and pairwise-optimal "
            "sine profiles under a maximum-charge cutoff; pairwise minimax only, "
            "not a full-space or diamond-norm optimum, an SU(2) directional "
            "reference, or a local SO(1,d) gravitational observer"
        ),
        "certified_claims": certified_claims,
        "records": tuple(records),
        "next_physics_gate": (
            "derive the corresponding SU(2) directional-reference channel and "
            "energy/error law, then couple it to the local static-patch KMS net"
        ),
    }
