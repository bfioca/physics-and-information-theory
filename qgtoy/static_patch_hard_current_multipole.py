"""Distributed hard-current multipole and nonzero-Bohr bounds.

For a local interaction ``g int B_a(x) ell_a(x)``, rotational invariance makes
the integrated angular charge purely zero Bohr frequency.  Every nonzero-Bohr
sector therefore has vanishing monopole and is controlled by the spatial
variation of the bath across the target support.  This module records the
resulting first-moment bound and conditional worst-case support guarantees.
All vector components are understood after specified parallel transport to a
common frame at the worldtube center.
"""

from __future__ import annotations

from math import isfinite, log, sqrt
from typing import Sequence

from .static_patch_scalar_common_mode import (
    maximum_same_shell_angular_separation,
)


def _validate_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _validate_positive_integer(name: str, value: int) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def current_first_absolute_moment(
    support_distances: Sequence[float],
    current_action_weights: Sequence[float],
) -> float:
    """Return ``M_1=sum_i r_i j_i`` for a discretized current sector.

    The nonnegative weights may be compressed operator norms, or sector-specific
    action norms ``||ell_i(omega) psi_T||`` for a declared target reference
    vector. Quadrature weights and parallel transport to the center frame are
    understood to have already been included.
    """
    distances = tuple(float(value) for value in support_distances)
    weights = tuple(float(value) for value in current_action_weights)
    if not distances or len(distances) != len(weights):
        raise ValueError("support distances and current weights must match")
    for value in distances:
        _validate_nonnegative("support distance", value)
    for value in weights:
        _validate_nonnegative("current action weight", value)
    return sum(distance * weight for distance, weight in zip(distances, weights))


def hard_current_multipole_remainder_bound(
    bath_lipschitz_constant: float,
    support_distances: Sequence[float],
    current_action_weights: Sequence[float],
    *,
    coupling: float = 1.0,
) -> float:
    """Bound the interaction remainder by ``|g| K M_1``.

    The bound applies either to a product reference vector when
    ``||(B_a(x)-B_a(p)) psi_B|| <= K r(x)`` and the supplied current weights
    are target-vector action norms, or on a compressed tensor-product subspace
    when both inputs are operator norms there.
    """
    _validate_nonnegative("bath_lipschitz_constant", bath_lipschitz_constant)
    if not isfinite(coupling):
        raise ValueError("coupling must be finite")
    first_moment = current_first_absolute_moment(
        support_distances,
        current_action_weights,
    )
    return abs(coupling) * bath_lipschitz_constant * first_moment


def hard_current_second_moment_remainder_bound(
    bath_hessian_constant: float,
    support_distances: Sequence[float],
    current_action_weights: Sequence[float],
    *,
    coupling: float = 1.0,
) -> float:
    """Bound a dipole-cancelled remainder by ``|g| K_2 M_2/2``."""
    _validate_nonnegative("bath_hessian_constant", bath_hessian_constant)
    if not isfinite(coupling):
        raise ValueError("coupling must be finite")
    distances = tuple(float(value) for value in support_distances)
    weights = tuple(float(value) for value in current_action_weights)
    if not distances or len(distances) != len(weights):
        raise ValueError("support distances and current weights must match")
    for value in distances:
        _validate_nonnegative("support distance", value)
    for value in weights:
        _validate_nonnegative("current action weight", value)
    second_moment = sum(
        distance**2 * weight
        for distance, weight in zip(distances, weights)
    )
    return 0.5 * abs(coupling) * bath_hessian_constant * second_moment


def zero_bohr_gksl_channel_error_bound(
    spin: int,
    dimensionless_time: float,
    *,
    relative_multipole_operator_error: float,
    number_of_axes: int = 3,
) -> float:
    """Bound a GKSL channel perturbation with monopole-multipole interference.

    This is the normalized diagonal-jump surrogate
    ``sum_a D[A_a] -> sum_a D[A_a+E_a]`` with unit rates and no Lamb-shift
    perturbation. For each axis, ``A_a`` has norm at most ``L`` and ``E_a`` has
    norm at most ``epsilon L``. The dissipator identity gives
    ``||D[A+E]-D[A]||_diamond <= 4||A||||E||+2||E||^2``.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive_integer("number_of_axes", number_of_axes)
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    _validate_nonnegative(
        "relative_multipole_operator_error",
        relative_multipole_operator_error,
    )
    epsilon = relative_multipole_operator_error
    raw = (
        number_of_axes
        * dimensionless_time
        * spin**2
        * (4.0 * epsilon + 2.0 * epsilon**2)
    )
    return min(2.0, raw)


def nonzero_bohr_gksl_channel_error_bound(
    spin: int,
    dimensionless_time: float,
    *,
    aggregate_relative_sector_error: float,
    number_of_axes: int = 3,
) -> float:
    """Bound strictly secular nonzero-Bohr dissipators with no monopole term.

    This is a unit-rate diagonal-jump surrogate with no Lamb-shift error. The
    declared aggregate hypothesis is
    ``sum_(a,omega!=0)||E_(a,omega)||^2 <= axes L^2 epsilon^2``.
    """
    _validate_positive_integer("spin", spin)
    _validate_positive_integer("number_of_axes", number_of_axes)
    _validate_nonnegative("dimensionless_time", dimensionless_time)
    _validate_nonnegative(
        "aggregate_relative_sector_error",
        aggregate_relative_sector_error,
    )
    raw = (
        2.0
        * number_of_axes
        * dimensionless_time
        * spin**2
        * aggregate_relative_sector_error**2
    )
    return min(2.0, raw)


def sufficient_zero_bohr_relative_error_cap(
    spin: int,
    dimensionless_time: float,
    *,
    channel_error_budget: float,
    number_of_axes: int = 3,
) -> float:
    """Return a sufficient cap from the uncapped zero-Bohr estimate."""
    _validate_positive_integer("spin", spin)
    _validate_positive_integer("number_of_axes", number_of_axes)
    _validate_positive("dimensionless_time", dimensionless_time)
    _validate_positive("channel_error_budget", channel_error_budget)
    if channel_error_budget >= 2.0:
        raise ValueError("channel_error_budget must be smaller than two")
    reduced_budget = channel_error_budget / (
        number_of_axes * dimensionless_time * spin**2
    )
    half_budget = 0.5 * reduced_budget
    return half_budget / (sqrt(1.0 + half_budget) + 1.0)


def sufficient_nonzero_bohr_relative_error_cap(
    spin: int,
    dimensionless_time: float,
    *,
    channel_error_budget: float,
    number_of_axes: int = 3,
) -> float:
    """Return a sufficient cap from the uncapped nonzero-Bohr estimate."""
    _validate_positive_integer("spin", spin)
    _validate_positive_integer("number_of_axes", number_of_axes)
    _validate_positive("dimensionless_time", dimensionless_time)
    _validate_positive("channel_error_budget", channel_error_budget)
    if channel_error_budget >= 2.0:
        raise ValueError("channel_error_budget must be smaller than two")
    return sqrt(
        channel_error_budget
        / (2.0 * number_of_axes * dimensionless_time * spin**2)
    )


def compressed_unitary_channel_distance_bound(
    evolution_time: float,
    *,
    interaction_remainder_norm_bound: float,
) -> float:
    """Return ``min(2,2 T ||R||)`` for two compressed unitary channels."""
    _validate_nonnegative("evolution_time", evolution_time)
    _validate_nonnegative(
        "interaction_remainder_norm_bound",
        interaction_remainder_norm_bound,
    )
    return min(2.0, 2.0 * evolution_time * interaction_remainder_norm_bound)


def two_cell_nonzero_bohr_saturation_witness(
    *,
    support_radius: float,
    bath_lipschitz_constant: float,
    coupling: float = 1.0,
) -> dict[str, float]:
    """Return an exact two-cell witness saturating the first-moment bound.

    Take the one-component ``U(1)`` model ``H_T=(Omega/2)sigma_z`` and currents
    ``ell_+= (sigma_z+sigma_x)/2`` and
    ``ell_-=(sigma_z-sigma_x)/2``.  Their sum is the conserved charge
    ``sigma_z``; the nonzero-Bohr ``sigma_x`` monopoles cancel.  With bath
    values ``B_+-B(p)=K a`` and ``B_--B(p)=-K a``, the surviving nonzero-Bohr
    interaction is exactly ``g K a sigma_x``.
    """
    _validate_positive("support_radius", support_radius)
    _validate_nonnegative("bath_lipschitz_constant", bath_lipschitz_constant)
    if not isfinite(coupling):
        raise ValueError("coupling must be finite")
    exact = abs(coupling) * bath_lipschitz_constant * support_radius
    bound = hard_current_multipole_remainder_bound(
        bath_lipschitz_constant,
        (support_radius, support_radius),
        (0.5, 0.5),
        coupling=coupling,
    )
    return {
        "integrated_nonzero_bohr_monopole_norm": 0.0,
        "exact_nonzero_bohr_remainder_norm": exact,
        "first_moment_bound": bound,
        "bound_saturation_ratio": exact / bound if bound > 0.0 else 1.0,
    }


def hard_current_support_record(
    spin: int,
    *,
    mismatch_coefficient: float = 1.0,
    multipole_error_coefficient: float = 1.0,
    relative_bath_lipschitz: float = 1.0,
    absolute_current_to_charge_ratio: float = 1.0,
    zero_bohr_jump_transfer_constant: float = 1.0,
    nonzero_bohr_aggregate_transfer_constant: float = 1.0,
    zero_bohr_second_order_transfer_constant: float = 1.0,
    relative_bath_hessian: float = 1.0,
    second_moment_to_charge_ratio: float = 1.0,
    number_of_axes: int = 3,
    radius: float = 1.0,
) -> dict[str, float | int | str]:
    """Compare multipole accuracy and disjoint-support localization scales."""
    _validate_positive_integer("spin", spin)
    for name, value in (
        ("mismatch_coefficient", mismatch_coefficient),
        ("multipole_error_coefficient", multipole_error_coefficient),
        ("relative_bath_lipschitz", relative_bath_lipschitz),
        ("absolute_current_to_charge_ratio", absolute_current_to_charge_ratio),
        ("zero_bohr_jump_transfer_constant", zero_bohr_jump_transfer_constant),
        (
            "nonzero_bohr_aggregate_transfer_constant",
            nonzero_bohr_aggregate_transfer_constant,
        ),
        (
            "zero_bohr_second_order_transfer_constant",
            zero_bohr_second_order_transfer_constant,
        ),
        ("relative_bath_hessian", relative_bath_hessian),
        ("second_moment_to_charge_ratio", second_moment_to_charge_ratio),
        ("radius", radius),
    ):
        _validate_positive(name, value)
    _validate_positive_integer("number_of_axes", number_of_axes)
    dimension = 2 * spin + 1
    logarithm = log(float(dimension))
    dimensionless_time = 0.5 * logarithm
    center_distance = sqrt(
        mismatch_coefficient
        / (dimension * spin * (spin + 1) * logarithm)
    )
    target_relative_error = multipole_error_coefficient / dimension
    sufficient_support_for_interaction_vector_budget = target_relative_error / (
        relative_bath_lipschitz * absolute_current_to_charge_ratio
    )
    sufficient_zero_bohr_relative_error = (
        sufficient_zero_bohr_relative_error_cap(
            spin,
            dimensionless_time,
            channel_error_budget=target_relative_error,
            number_of_axes=number_of_axes,
        )
    )
    sufficient_nonzero_bohr_relative_error = (
        sufficient_nonzero_bohr_relative_error_cap(
            spin,
            dimensionless_time,
            channel_error_budget=target_relative_error,
            number_of_axes=number_of_axes,
        )
    )
    sufficient_support_for_generic_zero_bohr = (
        sufficient_zero_bohr_relative_error
        / (
            zero_bohr_jump_transfer_constant
            * relative_bath_lipschitz
            * absolute_current_to_charge_ratio
        )
    )
    sufficient_support_for_nonzero_bohr = (
        sufficient_nonzero_bohr_relative_error
        / (
            nonzero_bohr_aggregate_transfer_constant
            * relative_bath_lipschitz
            * absolute_current_to_charge_ratio
        )
    )
    sufficient_support_after_zero_bohr_dipole_cancellation = sqrt(
        2.0
        * sufficient_zero_bohr_relative_error
        / (
            zero_bohr_second_order_transfer_constant
            * relative_bath_hessian
            * second_moment_to_charge_ratio
        )
    )
    maximum_equal_support_from_disjointness = 0.5 * center_distance
    generic_candidates = {
        "interaction_vector_budget": (
            sufficient_support_for_interaction_vector_budget
        ),
        "zero_bohr_linear_interference": (
            sufficient_support_for_generic_zero_bohr
        ),
        "nonzero_bohr_channel_error": sufficient_support_for_nonzero_bohr,
        "disjoint_worldtubes": maximum_equal_support_from_disjointness,
    }
    dipole_cancelled_candidates = {
        "interaction_vector_budget": (
            sufficient_support_for_interaction_vector_budget
        ),
        "zero_bohr_quadratic_error": (
            sufficient_support_after_zero_bohr_dipole_cancellation
        ),
        "nonzero_bohr_channel_error": sufficient_support_for_nonzero_bohr,
        "disjoint_worldtubes": maximum_equal_support_from_disjointness,
    }
    generic_active_constraint = min(generic_candidates, key=generic_candidates.get)
    dipole_cancelled_active_constraint = min(
        dipole_cancelled_candidates,
        key=dipole_cancelled_candidates.get,
    )
    generic_admissible_optical_support = generic_candidates[
        generic_active_constraint
    ]
    dipole_cancelled_admissible_optical_support = dipole_cancelled_candidates[
        dipole_cancelled_active_constraint
    ]
    horizon_distance = radius / dimension
    center_angle = maximum_same_shell_angular_separation(
        horizon_distance,
        center_distance,
        radius=radius,
    )
    generic_support_angle = maximum_same_shell_angular_separation(
        horizon_distance,
        generic_admissible_optical_support,
        radius=radius,
    )
    dipole_cancelled_support_angle = maximum_same_shell_angular_separation(
        horizon_distance,
        dipole_cancelled_admissible_optical_support,
        radius=radius,
    )
    return {
        "spin_L": spin,
        "sector_dimension_d": dimension,
        "horizon_distance_rho": horizon_distance,
        "imported_center_distance_over_radius": center_distance,
        "dimensionless_logarithmic_schedule_s": dimensionless_time,
        "target_relative_multipole_error": target_relative_error,
        "sufficient_support_for_interaction_vector_budget_over_radius": (
            sufficient_support_for_interaction_vector_budget
        ),
        "sufficient_zero_bohr_relative_operator_error_cap": (
            sufficient_zero_bohr_relative_error
        ),
        "sufficient_nonzero_bohr_aggregate_relative_error_cap": (
            sufficient_nonzero_bohr_relative_error
        ),
        "sufficient_support_for_generic_zero_bohr_over_radius": (
            sufficient_support_for_generic_zero_bohr
        ),
        "sufficient_support_for_nonzero_bohr_over_radius": (
            sufficient_support_for_nonzero_bohr
        ),
        "sufficient_support_after_zero_bohr_dipole_cancellation_over_radius": (
            sufficient_support_after_zero_bohr_dipole_cancellation
        ),
        "maximum_equal_support_from_disjointness_over_radius": (
            maximum_equal_support_from_disjointness
        ),
        "generic_admissible_optical_support_over_radius": (
            generic_admissible_optical_support
        ),
        "dipole_cancelled_admissible_optical_support_over_radius": (
            dipole_cancelled_admissible_optical_support
        ),
        "same_shell_center_angle": center_angle,
        "generic_same_shell_support_angular_radius": generic_support_angle,
        "dipole_cancelled_same_shell_support_angular_radius": (
            dipole_cancelled_support_angle
        ),
        "generic_active_support_constraint": generic_active_constraint,
        "dipole_cancelled_active_support_constraint": (
            dipole_cancelled_active_constraint
        ),
        "scaled_generic_optical_support_d_cubed_log_d": (
            generic_admissible_optical_support * dimension**3 * logarithm
        ),
        "scaled_generic_support_angle_d_to_4_log_d": (
            generic_support_angle * dimension**4 * logarithm
        ),
        "scaled_dipole_cancelled_optical_support_d_to_3_over_2_sqrt_log_d": (
            dipole_cancelled_admissible_optical_support
            * dimension**1.5
            * sqrt(logarithm)
        ),
        "scaled_dipole_cancelled_support_angle_d_to_5_over_2_sqrt_log_d": (
            dipole_cancelled_support_angle
            * dimension**2.5
            * sqrt(logarithm)
        ),
    }


def static_patch_hard_current_multipole_certificate(
    *,
    maximum_spin: int = 4096,
    mismatch_coefficient: float = 1.0,
    multipole_error_coefficient: float = 1.0,
) -> dict[str, object]:
    """Certify the conditional hard-current multipole/support theorem."""
    _validate_positive_integer("maximum_spin", maximum_spin)
    if maximum_spin < 64:
        raise ValueError("maximum_spin must be at least sixty-four")
    _validate_positive("mismatch_coefficient", mismatch_coefficient)
    _validate_positive("multipole_error_coefficient", multipole_error_coefficient)
    spins = tuple(
        sorted(
            {
                spin
                for spin in (16, 64, 256, 1024, maximum_spin)
                if spin <= maximum_spin
            }
            | {maximum_spin}
        )
    )
    records = tuple(
        hard_current_support_record(
            spin,
            mismatch_coefficient=mismatch_coefficient,
            multipole_error_coefficient=multipole_error_coefficient,
        )
        for spin in spins
    )
    witness = two_cell_nonzero_bohr_saturation_witness(
        support_radius=0.2,
        bath_lipschitz_constant=3.0,
        coupling=0.5,
    )
    generic_asymptotic_coefficient = (
        2.0 * multipole_error_coefficient / 3.0
    )
    dipole_cancelled_asymptotic_coefficient = min(
        sqrt(mismatch_coefficient),
        sqrt(4.0 * multipole_error_coefficient / 3.0),
    )

    def relative_close(value: float, target: float) -> bool:
        return abs(value - target) <= 5.0e-4 * max(abs(target), 1.0e-15)

    certified_claims = {
        "two_cell_nonzero_bohr_monopole_cancels_exactly": (
            witness["integrated_nonzero_bohr_monopole_norm"] == 0.0
        ),
        "two_cell_first_moment_bound_is_saturated": abs(
            witness["bound_saturation_ratio"] - 1.0
        )
        < 1.0e-12,
        "generic_sufficient_support_has_d_minus_three_log_scaling": relative_close(
            records[-1]["scaled_generic_optical_support_d_cubed_log_d"],
            generic_asymptotic_coefficient,
        ),
        "generic_sufficient_angle_has_d_minus_four_log_scaling": relative_close(
            records[-1]["scaled_generic_support_angle_d_to_4_log_d"],
            generic_asymptotic_coefficient,
        ),
        "dipole_cancelled_sufficient_support_has_quadratic_scaling": relative_close(
            records[-1][
                "scaled_dipole_cancelled_optical_support_d_to_3_over_2_sqrt_log_d"
            ],
            dipole_cancelled_asymptotic_coefficient,
        ),
        "dipole_cancelled_sufficient_angle_has_quadratic_scaling": relative_close(
            records[-1][
                "scaled_dipole_cancelled_support_angle_d_to_5_over_2_sqrt_log_d"
            ],
            dipole_cancelled_asymptotic_coefficient,
        ),
    }
    return {
        "goal": "Distributed Hard Angular-Current Multipole Gate",
        "status": "pass" if all(certified_claims.values()) else "fail",
        "result_type": "conditional_multipole_and_nonzero_bohr_bound",
        "central_result": (
            "If the integrated angular charge commutes with the hard-target "
            "Hamiltonian, every nonzero-Bohr current sector has zero monopole. "
            "After specified parallel transport, a declared bath Lipschitz bound "
            "controls the full lumping error and controls each nonzero-Bohr "
            "sector by its own |g| K current first absolute moment."
        ),
        "scaling_consequence": (
            "Under a declared interaction-to-jump transfer bound, the normalized "
            "diagonal-jump GKSL perturbation certificate gives a sufficient "
            "worst-case optical support O(d^(-3)/log d), hence angular support "
            "O(d^(-4)/log d), for a generic zero-Bohr dipole. If the transported "
            "zero-Bohr dipole vanishes componentwise and the remainder is second "
            "order, sufficient support relaxes to O(d^(-3/2)/sqrt(log d)) "
            "optically and O(d^(-5/2)/sqrt(log d)) angularly."
        ),
        "claim_boundary": (
            "The RMS branch is only a product-reference-state vector bound. A "
            "diamond estimate requires bounded compressed bath/current operators "
            "and invariant compressed dynamics. The theorem assumes rotational "
            "conservation of the integrated charge, a bath Lipschitz constant, "
            "specified parallel transport, separate zero-Bohr, aggregate "
            "nonzero-Bohr, and second-order jump-transfer constants, a normalized "
            "diagonal Kossakowski form with no Lamb-shift error, a strict secular "
            "gap treatment, and distinct "
            "nonoverlapping worldtubes. The quadratic branch additionally "
            "assumes componentwise zero-Bohr current-dipole cancellation and a "
            "covariant Hessian bound. None is derived here from QFT."
        ),
        "certified_claims": certified_claims,
        "two_cell_saturation_witness": witness,
        "records": records,
        "next_physics_gate": (
            "derive the current first moment, compressed bath Lipschitz constant, "
            "and localization stress from a named hard-target matter action, then "
            "prove a growing-sector Davies error and gravitational backreaction "
            "window"
        ),
    }
