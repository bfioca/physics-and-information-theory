"""Feshbach transfer bounds for a collective band and its complement.

In one rotational sector decompose the full Hamiltonian with projectors ``P``
and ``Q``.  If

    P H P >= a P,  Q H Q >= d Q,  ||Q H P|| <= v,

then the full sector floor is bounded by the smaller eigenvalue of the scalar
comparison matrix ``[[a,v],[v,d]]``.  This module also records why a collective
floor alone is insufficient: positive two-band completions can preserve the
collective block while driving the full floor arbitrarily close to zero.
"""

from __future__ import annotations

from math import exp, hypot, isfinite


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def feshbach_sector_floor_lower_bound(
    *,
    collective_floor: float,
    complement_floor: float,
    band_coupling_norm: float,
) -> float:
    """Return the exact two-block quadratic-form comparison floor."""
    _validate_nonnegative("collective_floor", collective_floor)
    _validate_nonnegative("complement_floor", complement_floor)
    _validate_nonnegative("band_coupling_norm", band_coupling_norm)
    return 0.5 * (
        collective_floor
        + complement_floor
        - hypot(
            complement_floor - collective_floor,
            2.0 * band_coupling_norm,
        )
    )


def schur_sector_floor_lower_bound(
    *,
    collective_floor: float,
    complement_floor: float,
    band_coupling_norm: float,
) -> float:
    """Return ``a-v^2/(d-a)``, valid when the complement lies above ``a``."""
    _validate_nonnegative("collective_floor", collective_floor)
    _validate_nonnegative("complement_floor", complement_floor)
    _validate_nonnegative("band_coupling_norm", band_coupling_norm)
    gap = complement_floor - collective_floor
    if gap <= 0.0:
        raise ValueError("complement_floor must exceed collective_floor")
    return collective_floor - band_coupling_norm**2 / gap


def fractional_collective_floor_transfer(
    *,
    collective_floor: float,
    complement_gap: float,
    relative_coupling_budget: float,
) -> dict[str, float | bool]:
    """Certify ``epsilon_full >= (1-eta)a`` from ``v^2<=eta Delta a``."""
    _validate_nonnegative("collective_floor", collective_floor)
    _validate_positive("complement_gap", complement_gap)
    _validate_nonnegative("relative_coupling_budget", relative_coupling_budget)
    if relative_coupling_budget >= 1.0:
        raise ValueError("relative_coupling_budget must be smaller than one")
    maximum_coupling_norm = (
        relative_coupling_budget * complement_gap * collective_floor
    ) ** 0.5
    complement_floor = collective_floor + complement_gap
    exact_comparison = feshbach_sector_floor_lower_bound(
        collective_floor=collective_floor,
        complement_floor=complement_floor,
        band_coupling_norm=maximum_coupling_norm,
    )
    transferred_floor = (1.0 - relative_coupling_budget) * collective_floor
    return {
        "collective_floor": collective_floor,
        "complement_gap": complement_gap,
        "maximum_coupling_norm": maximum_coupling_norm,
        "exact_comparison_floor": exact_comparison,
        "transferred_floor": transferred_floor,
        "exact_comparison_dominates_transferred_floor": (
            exact_comparison + 1e-15 >= transferred_floor
        ),
    }


def scale_uniform_collective_floor_transfer(
    *,
    collective_floor: float,
    complement_ratio: float,
    coupling_ratio: float,
) -> dict[str, float | bool]:
    """Transfer ``a_j`` when ``d_j>=gamma a_j`` and ``v_j<=rho a_j``."""
    _validate_nonnegative("collective_floor", collective_floor)
    _validate_positive("complement_ratio", complement_ratio)
    _validate_nonnegative("coupling_ratio", coupling_ratio)
    transferred_fraction = 0.5 * (
        1.0
        + complement_ratio
        - hypot(complement_ratio - 1.0, 2.0 * coupling_ratio)
    )
    return {
        "collective_floor": collective_floor,
        "complement_ratio_gamma": complement_ratio,
        "coupling_ratio_rho": coupling_ratio,
        "transferred_fraction_kappa": transferred_fraction,
        "transferred_floor": transferred_fraction * collective_floor,
        "strict_positivity_condition_rho_squared_below_gamma": (
            coupling_ratio**2 < complement_ratio
        ),
        "transferred_fraction_is_strictly_positive": transferred_fraction > 0.0,
    }


def complement_weight_upper_bound(
    *,
    eigenvalue_upper_bound: float,
    complement_floor: float,
    band_coupling_norm: float,
) -> float:
    """Bound ``||Q psi||^2`` for a normalized eigenstate below the Q floor."""
    _validate_nonnegative("eigenvalue_upper_bound", eigenvalue_upper_bound)
    _validate_nonnegative("complement_floor", complement_floor)
    _validate_nonnegative("band_coupling_norm", band_coupling_norm)
    denominator = complement_floor - eigenvalue_upper_bound
    if denominator <= 0.0:
        raise ValueError("eigenvalue_upper_bound must lie below complement_floor")
    ratio = band_coupling_norm / denominator
    return ratio**2 / (1.0 + ratio**2)


def induced_collective_quartic_coefficient(
    *,
    inertia_mode_coupling: float,
    mode_stiffness: float,
) -> float:
    """Return ``J4=b^2/(2 Delta)`` for one relaxed deformation mode."""
    _validate_nonnegative("inertia_mode_coupling", inertia_mode_coupling)
    _validate_positive("mode_stiffness", mode_stiffness)
    return inertia_mode_coupling**2 / (2.0 * mode_stiffness)


def unconstrained_band_completion_counterexample(
    *,
    collective_floor: float,
    retained_fraction: float,
) -> dict[str, float | str | bool]:
    """Keep ``PHP=a`` while a positive completion has floor ``delta a``."""
    _validate_positive("collective_floor", collective_floor)
    _validate_positive("retained_fraction", retained_fraction)
    if retained_fraction > 1.0:
        raise ValueError("retained_fraction must be at most one")
    complement_floor = collective_floor
    coupling = (1.0 - retained_fraction) * collective_floor
    full_floor = feshbach_sector_floor_lower_bound(
        collective_floor=collective_floor,
        complement_floor=complement_floor,
        band_coupling_norm=coupling,
    )
    upper_eigenvalue = 2.0 * collective_floor - full_floor
    return {
        "collective_block_floor": collective_floor,
        "complement_block_floor": complement_floor,
        "band_coupling_norm": coupling,
        "full_sector_floor": full_floor,
        "upper_eigenvalue": upper_eigenvalue,
        "completion_is_positive_semidefinite": full_floor >= 0.0,
        "collective_block_is_unchanged": True,
        "statement": (
            "For any delta in (0,1], the positive block matrix "
            "[[a,(1-delta)a],[(1-delta)a,a]] preserves PHP=a but has "
            "full floor delta*a. Static collective data alone therefore give "
            "no uniform full-sector fraction."
        ),
    }


def growing_diagonal_constant_floor_counterexample(
    *,
    collective_floor: float,
    residual_floor: float,
) -> dict[str, float | str | bool]:
    """Let both diagonal blocks grow while mixing fixes the lower eigenvalue."""
    _validate_positive("collective_floor", collective_floor)
    _validate_positive("residual_floor", residual_floor)
    if residual_floor >= collective_floor:
        raise ValueError("residual_floor must be smaller than collective_floor")
    complement_floor = 2.0 * collective_floor
    coupling = (
        (collective_floor - residual_floor)
        * (complement_floor - residual_floor)
    ) ** 0.5
    full_floor = feshbach_sector_floor_lower_bound(
        collective_floor=collective_floor,
        complement_floor=complement_floor,
        band_coupling_norm=coupling,
    )
    return {
        "collective_block_floor": collective_floor,
        "complement_block_floor": complement_floor,
        "band_coupling_norm": coupling,
        "full_sector_floor": full_floor,
        "upper_eigenvalue": 3.0 * collective_floor - residual_floor,
        "both_diagonal_blocks_grow_with_collective_scale": True,
        "statement": (
            "Choosing v^2=(A-Delta)(2A-Delta) gives diagonal floors A and "
            "2A but exact eigenvalues Delta and 3A-Delta. A complement floor "
            "without a coupling bound does not transfer spectral growth."
        ),
    }


def constant_floor_rotational_partition_partial_sum(
    maximum_sector_index: int,
    *,
    dual_parameter: float,
    residual_floor: float,
    projective: bool = False,
) -> float:
    """Return a truncated partition sum for a spin-independent sector floor."""
    if (
        isinstance(maximum_sector_index, bool)
        or not isinstance(maximum_sector_index, int)
        or maximum_sector_index < 0
    ):
        raise ValueError("maximum_sector_index must be a nonnegative integer")
    _validate_positive("dual_parameter", dual_parameter)
    _validate_nonnegative("residual_floor", residual_floor)
    boltzmann_weight = exp(-dual_parameter * residual_floor)
    return boltzmann_weight * sum(
        (2 * index + (2 if projective else 1)) ** 2
        for index in range(maximum_sector_index + 1)
    )


def collective_band_feshbach_certificate() -> dict[str, object]:
    """Audit the transfer theorem and the present Skyrmion evidence gap."""
    collective_floors = (0.25, 1.0, 4.0, 16.0, 64.0)
    transferred = tuple(
        fractional_collective_floor_transfer(
            collective_floor=floor,
            complement_gap=2.0 + floor**0.5,
            relative_coupling_budget=0.1,
        )
        for floor in collective_floors
    )
    counterexamples = tuple(
        unconstrained_band_completion_counterexample(
            collective_floor=1.0,
            retained_fraction=fraction,
        )
        for fraction in (0.5, 0.1, 0.01, 0.001)
    )
    growing_diagonal_counterexamples = tuple(
        growing_diagonal_constant_floor_counterexample(
            collective_floor=floor,
            residual_floor=0.1,
        )
        for floor in (1.0, 10.0, 100.0, 1000.0)
    )
    scale_transfer = scale_uniform_collective_floor_transfer(
        collective_floor=10.0,
        complement_ratio=2.0,
        coupling_ratio=0.5,
    )
    partition_partial_sums = tuple(
        {
            "maximum_sector_index": cutoff,
            "projective_partition_partial_sum": (
                constant_floor_rotational_partition_partial_sum(
                    cutoff,
                    dual_parameter=1.0,
                    residual_floor=0.1,
                    projective=True,
                )
            ),
        }
        for cutoff in (10, 100, 1000)
    )
    claims = {
        "fractional_gap_coupling_hypothesis_transfers_every_sampled_floor": all(
            record["exact_comparison_dominates_transferred_floor"]
            for record in transferred
        ),
        "collective_floor_alone_has_no_uniform_full_band_fraction": all(
            record["completion_is_positive_semidefinite"]
            and record["collective_block_is_unchanged"]
            for record in counterexamples
        )
        and counterexamples[-1]["full_sector_floor"] < 0.002,
        "small_mode_stiffness_can_destroy_quartic_control": (
            induced_collective_quartic_coefficient(
                inertia_mode_coupling=1.0,
                mode_stiffness=1e-6,
            )
            > 1e5
        ),
        "scale_uniform_margin_preserves_linear_sector_growth": (
            scale_transfer["strict_positivity_condition_rho_squared_below_gamma"]
            and scale_transfer["transferred_fraction_is_strictly_positive"]
        ),
        "growing_diagonal_floors_do_not_replace_a_coupling_bound": all(
            abs(record["full_sector_floor"] - 0.1) < 1e-10
            for record in growing_diagonal_counterexamples
        ),
        "constant_full_floor_makes_rotational_partition_diverge": all(
            right["projective_partition_partial_sum"]
            > left["projective_partition_partial_sum"]
            for left, right in zip(
                partition_partial_sums,
                partition_partial_sums[1:],
            )
        )
        and partition_partial_sums[-1]["projective_partition_partial_sum"]
        > 1e9,
    }
    return {
        "goal": "Collective-Band Feshbach Transfer Gate",
        "status": "pass" if all(claims.values()) else "fail",
        "result_type": "abstract_band_transfer_theorem_plus_insufficiency_witness",
        "central_result": (
            "A collective sector floor transfers to the full Hamiltonian once "
            "a complement floor and off-band coupling norm are bounded. The "
            "collective block alone admits positive completions whose full "
            "floor is arbitrarily small."
        ),
        "transfer_records": transferred,
        "insufficiency_counterexamples": counterexamples,
        "growing_diagonal_counterexamples": growing_diagonal_counterexamples,
        "scale_uniform_transfer_record": scale_transfer,
        "constant_floor_partition_partial_sums": partition_partial_sums,
        "current_skyrmion_evidence": {
            "profile_uniform_collective_floor": "proved",
            "quantum_collective_projector_and_compression_floor": "missing",
            "static_radial_bvp_jacobi_coercivity": "proved in its declared norm",
            "coupled_time_dependent_skyrmion_wall_anchor_gap": "missing",
            "off_band_coupling_norm": "missing",
            "collective_projector_feshbach_remainder": "missing",
            "physical_full_band_gate": "open",
        },
        "certified_claims": claims,
        "claim_boundary": (
            "This certificate proves the operator comparison and the logical "
            "insufficiency of collective data alone. It does not supply the "
            "quantum Skyrmion collective projector/compression theorem, the "
            "Skyrmion-wall-anchor gap, or the coupling norm, and therefore does "
            "not promote the collective spectral floor to the full field theory."
        ),
    }
