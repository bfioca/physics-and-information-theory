"""Energy-constrained rotational-frameness obstruction for a clock-only model.

Any construction that gauges the full de Sitter isometry group must in
particular impose invariance under the compact SO(3) stabilizer of a static
observer.  If the observer carries only a rotation-trivial scalar clock and all
spectators are invariant, compact-subgroup observables lie in the SO(3)
fixed-point algebra.  Near-horizon conformal-scalar collar trial functions and
the min-max principle make the resulting hard-energy recovery and entropy
obstruction quantitative.
"""

from __future__ import annotations

from math import isfinite, log

from .redshifted_frame_capacity import (
    collar_static_energy_upper_bound,
    finite_wall_ground_frequency_upper_bound,
    maximum_bounded_energy_angular_momentum,
    missing_rotation_frame_relative_entropy,
    truncated_scalar_harmonic_dimension,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def fixed_spin_basis_state(
    angular_momentum: int,
    magnetic_quantum_number: int,
) -> tuple[float, ...]:
    """Diagonal density of ``|ell,m><ell,m|`` in the magnetic basis."""
    if (
        isinstance(angular_momentum, bool)
        or not isinstance(angular_momentum, int)
        or angular_momentum < 0
    ):
        raise ValueError("angular_momentum must be a nonnegative integer")
    if (
        isinstance(magnetic_quantum_number, bool)
        or not isinstance(magnetic_quantum_number, int)
        or abs(magnetic_quantum_number) > angular_momentum
    ):
        raise ValueError("magnetic_quantum_number must lie from -ell through ell")
    dimension = 2 * angular_momentum + 1
    position = magnetic_quantum_number + angular_momentum
    return tuple(1.0 if index == position else 0.0 for index in range(dimension))


def fixed_spin_so3_twirl(angular_momentum: int) -> tuple[float, ...]:
    """Diagonal of the Haar twirl on one irreducible spin sector."""
    if (
        isinstance(angular_momentum, bool)
        or not isinstance(angular_momentum, int)
        or angular_momentum < 0
    ):
        raise ValueError("angular_momentum must be a nonnegative integer")
    dimension = 2 * angular_momentum + 1
    return tuple(1.0 / dimension for _ in range(dimension))


def diagonal_trace_distance(
    first: tuple[float, ...],
    second: tuple[float, ...],
) -> float:
    if len(first) != len(second) or not first:
        raise ValueError("diagonal states must have the same nonzero dimension")
    return 0.5 * sum(abs(left - right) for left, right in zip(first, second))


def fixed_spin_replacer_optimal_normalized_diamond_error(
    angular_momentum: int,
) -> float:
    """Exact recovery error after irreducible ``SO(3)`` depolarization.

    Haar expectation on a single spin sector is the completely depolarizing
    channel.  Any decoded channel is therefore a replacer.  Covariance makes the
    maximally mixed replacer optimal, and a maximally entangled witness gives
    normalized diamond distance ``1-1/d^2`` from the identity.
    """
    if (
        isinstance(angular_momentum, bool)
        or not isinstance(angular_momentum, int)
        or angular_momentum < 0
    ):
        raise ValueError("angular_momentum must be a nonnegative integer")
    dimension = 2 * angular_momentum + 1
    return 1.0 - 1.0 / (dimension * dimension)


def scalar_clock_rotation_obstruction_record(
    *,
    radius: float,
    stretched_distance: float,
    energy_budget: float,
    inner_offset: float,
    outer_offset: float,
) -> dict[str, object]:
    """Record the compact-stabilizer obstruction at one stretched horizon."""
    maximum_angular_momentum = maximum_bounded_energy_angular_momentum(
        radius=radius,
        stretched_distance=stretched_distance,
        energy_budget=energy_budget,
        inner_offset=inner_offset,
        outer_offset=outer_offset,
    )
    if maximum_angular_momentum < 1:
        raise ValueError("parameters must certify at least one nontrivial spin sector")
    sector_dimension = 2 * maximum_angular_momentum + 1
    token_dimension = truncated_scalar_harmonic_dimension(
        maximum_angular_momentum
    )
    frame_entropy = missing_rotation_frame_relative_entropy(
        maximum_angular_momentum
    )
    plus_state = fixed_spin_basis_state(
        maximum_angular_momentum,
        maximum_angular_momentum,
    )
    minus_state = fixed_spin_basis_state(
        maximum_angular_momentum,
        -maximum_angular_momentum,
    )
    twirled_plus = fixed_spin_so3_twirl(maximum_angular_momentum)
    twirled_minus = fixed_spin_so3_twirl(maximum_angular_momentum)
    return {
        "de_sitter_radius_R": radius,
        "stretched_horizon_gap_delta": stretched_distance,
        "expected_static_energy_budget_E0": energy_budget,
        "maximum_bounded_energy_spin_L_delta": maximum_angular_momentum,
        "fixed_spin_sector_dimension": sector_dimension,
        "largest_mode_energy_upper_bound": collar_static_energy_upper_bound(
            maximum_angular_momentum,
            radius=radius,
            stretched_distance=stretched_distance,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
        ),
        "variational_ground_frequency_upper_bound": (
            finite_wall_ground_frequency_upper_bound(
                maximum_angular_momentum,
                radius=radius,
                stretched_distance=stretched_distance,
                inner_offset=inner_offset,
                outer_offset=outer_offset,
            )
        ),
        "orthogonal_directional_pair": (
            "finite-wall radial ground state phi_L tensor |L,L> and its "
            "antipodal rotation phi_L tensor |L,-L>"
        ),
        "pair_input_trace_distance": diagonal_trace_distance(
            plus_state,
            minus_state,
        ),
        "scalar_clock_so3_action": "trivial",
        "so3_fixed_point_restriction_distance": diagonal_trace_distance(
            twirled_plus,
            twirled_minus,
        ),
        "all_decoder_worst_case_trace_error_lower_bound": diagonal_trace_distance(
            plus_state,
            minus_state,
        )
        / 2.0,
        "full_fixed_spin_optimal_normalized_diamond_error": (
            fixed_spin_replacer_optimal_normalized_diamond_error(
                maximum_angular_momentum
            )
        ),
        "hard_static_energy_corner_statement": (
            "Rayleigh-Ritz supplies a nonzero finite-wall eigenstate below E0 in "
            "the spin sector, so the m=+/-L pair lies exactly in the one-particle "
            "static spectral corner"
        ),
        "time_crossed_product_extension_status": (
            "not established here; requires a commuting conditional expectation "
            "on the named crossed product"
        ),
        "coherent_token_dimension": token_dimension,
        "coherent_token_missing_frame_relative_entropy": frame_entropy,
        "log_R_over_delta": log(radius / stretched_distance),
    }


def scalar_clock_rotation_no_go_certificate(
    *,
    radius: float = 1.0,
    energy_budget: float = 4.0,
    inner_offset: float = 0.5,
    outer_offset: float = 1.5,
    minimum_power: int = 64,
    steps: int = 6,
) -> dict[str, object]:
    """Audit the clock-only compact-fixed-point rotation obstruction."""
    _validate_positive("radius", radius)
    _validate_positive("energy_budget", energy_budget)
    if (
        isinstance(minimum_power, bool)
        or not isinstance(minimum_power, int)
        or minimum_power < 8
    ):
        raise ValueError("minimum_power must be an integer at least eight")
    if (
        isinstance(steps, bool)
        or not isinstance(steps, int)
        or steps < 3
        or steps > 64
    ):
        raise ValueError("steps must be an integer from three through sixty-four")
    records = tuple(
        scalar_clock_rotation_obstruction_record(
            radius=radius,
            stretched_distance=radius / float(minimum_power * 4**index),
            energy_budget=energy_budget,
            inner_offset=inner_offset,
            outer_offset=outer_offset,
        )
        for index in range(steps)
    )
    diamond_bounds = tuple(
        record["full_fixed_spin_optimal_normalized_diamond_error"]
        for record in records
    )
    entropy_offsets = tuple(
        record["coherent_token_missing_frame_relative_entropy"]
        - record["log_R_over_delta"]
        for record in records
    )
    certified_claims = {
        "hard_static_energy_directional_pair_exists_at_every_cutoff": all(
            record["variational_ground_frequency_upper_bound"] <= energy_budget
            and record["pair_input_trace_distance"] == 1.0
            for record in records
        ),
        "compact_fixed_point_algebra_cannot_distinguish_the_pair": all(
            record["so3_fixed_point_restriction_distance"] == 0.0
            for record in records
        ),
        "all_decoders_have_half_error_on_the_pair": all(
            record["all_decoder_worst_case_trace_error_lower_bound"] == 0.5
            for record in records
        ),
        "full_sector_quantum_recovery_error_tends_to_one": (
            all(right > left for left, right in zip(diamond_bounds, diamond_bounds[1:]))
            and diamond_bounds[-1] > 0.99
        ),
        "missing_frame_entropy_has_log_R_over_delta_scaling": (
            max(entropy_offsets[-3:]) - min(entropy_offsets[-3:]) < 0.12
        ),
    }
    return {
        "goal": "Energy-Constrained Rotational Frameness Obstruction",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "conditional_compact_fixed_point_recovery_obstruction",
        "central_result": (
            "For a clock-only truncation with SO(3)-invariant ancillary resources, "
            "the compact fixed-point algebra cannot distinguish orthogonal near-"
            "horizon directional states lying in a hard finite-wall static-energy "
            "window. Every decoder through the canonical compact expectation has "
            "worst-case trace error at least 1/2; the exact optimal full fixed-spin "
            "normalized diamond error is 1-1/(2L_delta+1)^2, tending to one. A "
            "coherent hard-energy token loses log(R/delta)+O(1) relative entropy "
            "of frame."
        ),
        "named_model_boundary": (
            "This is a conditional compact-fixed-point obstruction for a clock-only "
            "truncation with invariant spectators. CLPW already identifies the "
            "qualitative need for an orthonormal frame in addition to its clock. "
            "The result neither constructs the full SO(1,4)-averaged algebra nor "
            "asserts that the original CLPW time crossed product itself performs "
            "an SO(3) average."
        ),
        "escape_route": (
            "A covariant observer carrying a nontrivial SO(1,d) representation, "
            "or another explicit directional reference with sufficient irrep "
            "multiplicity, lies outside the theorem."
        ),
        "claim_boundary": (
            "free conformal one-particle finite-wall states, hard field static-"
            "energy spectral support from Rayleigh-Ritz, compact SO(3) stabilizer "
            "subgroup, rotation-trivial scalar clock and SO(3)-invariant spectators; "
            "no crossed-product commuting-square theorem, "
            "backreaction, local proper-energy bound, occupation-number theorem, "
            "noncompact SO(1,4) averaging measure, or generalized-entropy identity"
        ),
        "certified_claims": certified_claims,
        "records": records,
        "primary_context": (
            "https://arxiv.org/abs/2206.10780",
            "https://arxiv.org/abs/2511.00622",
            "https://arxiv.org/abs/0901.0943",
        ),
        "next_physics_gate": (
            "put a covariant SO(1,d) observer and the scalar-clock control on the "
            "same Bunch-Davies local net, derive their energy/backreaction budgets, "
            "and compare the surviving finite trace with generalized entropy"
        ),
    }
