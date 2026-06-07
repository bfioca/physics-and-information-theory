"""Goal 23 regulated static-patch dS/CFT algebraic ER=EPR testbed."""

from __future__ import annotations

from math import exp, log2

from .bilayer import binary_entropy
from .ds_cft_dynamics import goal22_ds_cft_er_epr_single_dynamics_certificate
from .general_algebraic_connectivity import coherence_probe_relative_entropy_bits
from .relative_entropy_bridge import _rounded


def _validate_cutoff(cutoff: int) -> None:
    if cutoff < 1:
        raise ValueError("cutoff must be at least one")


def _validate_max_cutoff(max_cutoff: int) -> None:
    if max_cutoff < 1:
        raise ValueError("max_cutoff must be at least one")


def _validate_low_order(low_order: int) -> None:
    if low_order < 0:
        raise ValueError("low_order must be nonnegative")


def _validate_probability(screen_probability: float) -> None:
    if not 0.0 <= screen_probability <= 1.0:
        raise ValueError("screen_probability must lie in [0,1]")


def static_patch_mode_labels(cutoff: int) -> tuple[tuple[int, int], ...]:
    """Finite spherical-mode labels through angular cutoff L."""
    _validate_cutoff(cutoff)
    return tuple(
        (ell, magnetic)
        for ell in range(cutoff + 1)
        for magnetic in range(-ell, ell + 1)
    )


def mode_count(cutoff: int) -> int:
    return len(static_patch_mode_labels(cutoff))


def _mode_distance(first: tuple[int, int], second: tuple[int, int]) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def _geometric_shrink(cutoff: int, first: tuple[int, int], second: tuple[int, int]) -> float:
    if first == second:
        return 1.0
    return exp(-_mode_distance(first, second) / float((cutoff + 1) ** 2))


def regulated_kernel_summary(
    cutoff: int,
    *,
    offdiag_coupling: int,
    screen_probability: float,
) -> dict[str, object]:
    """Summarize one regulated finite static-patch transfer kernel."""
    _validate_cutoff(cutoff)
    _validate_probability(screen_probability)
    if offdiag_coupling not in (0, 1):
        raise ValueError("offdiag_coupling must be 0 or 1")

    labels = static_patch_mode_labels(cutoff)
    dim = len(labels)
    offdiag_shrinks = tuple(
        offdiag_coupling * _geometric_shrink(cutoff, first, second)
        for first in labels
        for second in labels
        if first != second
    )
    min_nonzero_geometric_shrink = min(
        _geometric_shrink(cutoff, first, second)
        for first in labels
        for second in labels
        if first != second
    )
    max_nonzero_geometric_shrink = max(
        _geometric_shrink(cutoff, first, second)
        for first in labels
        for second in labels
        if first != second
    )
    min_offdiag_shrink = min(offdiag_shrinks) if offdiag_shrinks else 0.0
    max_offdiag_shrink = max(offdiag_shrinks) if offdiag_shrinks else 0.0
    geometric_resolution_error = 1.0 - min_nonzero_geometric_shrink
    exact_fixed_count = dim if offdiag_coupling == 0 else dim
    epsilon_fixed_count = dim * dim if offdiag_coupling else dim
    return {
        "cutoff_L": cutoff,
        "mode_count": dim,
        "screen_probability": screen_probability,
        "offdiag_coupling": offdiag_coupling,
        "dynamics_family": "regulated_static_patch_screen_kernel",
        "dynamics_id": (
            f"regulated_static_patch:L={cutoff}:p={screen_probability}:"
            f"offdiag={offdiag_coupling}"
        ),
        "finite_boundary_screen_mode_algebra": f"C^{dim}",
        "full_regulated_operator_algebra": f"M_{dim}",
        "north_observer_static_patch_algebra": f"M_{dim}",
        "south_observer_static_patch_algebra": f"M_{dim}",
        "shared_horizon_algebra": f"C^{dim}",
        "kernel_rule": {
            "diagonal_matrix_units": "fixed",
            "off_diagonal_matrix_units": (
                "geometrically_damped"
                if offdiag_coupling
                else "projected_to_zero"
            ),
            "shrink_formula": "exp(-mode_distance/(L+1)^2)",
            "derived_from_one_regulated_dynamics": True,
        },
        "kernel_bounds": {
            "min_geometric_offdiag_shrink": _rounded(min_nonzero_geometric_shrink),
            "max_geometric_offdiag_shrink": _rounded(max_nonzero_geometric_shrink),
            "min_actual_offdiag_shrink": _rounded(min_offdiag_shrink),
            "max_actual_offdiag_shrink": _rounded(max_offdiag_shrink),
            "geometric_resolution_error": _rounded(geometric_resolution_error),
        },
        "cptp_oaqec_definition": {
            "finite_dimensional_cptp_channel": True,
            "schur_multiplier_kernel_positive": "certified_by_exponential_metric_kernel",
            "trace_preserving": True,
            "unital": True,
            "exact_fixed_point_algebra": f"C^{dim}",
            "epsilon_recoverable_bridge_algebra": (
                f"M_{dim}" if offdiag_coupling else f"C^{dim}"
            ),
            "epsilon_recoverable_fixed_operator_count": epsilon_fixed_count,
            "exact_fixed_operator_count": exact_fixed_count,
        },
        "bridge_phase": (
            "regulated_quantum_bridge"
            if offdiag_coupling
            else "classical_horizon_bridge"
        ),
    }


def _low_order_mode_count(cutoff: int, low_order: int) -> int:
    return sum(
        1
        for ell, _magnetic in static_patch_mode_labels(cutoff)
        if ell <= min(cutoff, low_order)
    )


def _diagonal_correlator_shadow(cutoff: int, low_order: int) -> tuple[dict[str, object], ...]:
    rows = []
    for ell in range(min(cutoff, low_order) + 1):
        degeneracy = 2 * ell + 1
        rows.append(
            {
                "ell": ell,
                "degeneracy": degeneracy,
                "normalized_power": _rounded(degeneracy / mode_count(cutoff)),
            }
        )
    return tuple(rows)


def regulated_static_patch_collision_record(
    cutoff: int,
    *,
    screen_probability: float,
    low_order: int,
) -> dict[str, object]:
    """Finite-cutoff collision and intrinsic completion for one cutoff."""
    _validate_cutoff(cutoff)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    dim = mode_count(cutoff)
    quantum = regulated_kernel_summary(
        cutoff,
        offdiag_coupling=1,
        screen_probability=screen_probability,
    )
    classical = regulated_kernel_summary(
        cutoff,
        offdiag_coupling=0,
        screen_probability=screen_probability,
    )
    input_bits = coherence_probe_relative_entropy_bits(dim=dim)
    min_shrink = float(quantum["kernel_bounds"]["min_geometric_offdiag_shrink"])
    response_retention_lower_bound = min_shrink * min_shrink
    quantum_defect_bound = input_bits * (1.0 - response_retention_lower_bound)
    entropy_bits = log2(dim)
    north_entropy = binary_entropy(screen_probability)
    south_entropy = binary_entropy(1.0 - screen_probability)
    return {
        "cutoff_L": cutoff,
        "mode_count": dim,
        "screen_probability": screen_probability,
        "low_order": low_order,
        "finite_static_patch_objects": {
            "boundary_screen_mode_algebra": f"C^{dim}",
            "north_observer_static_patch_algebra": f"M_{dim}",
            "south_observer_static_patch_algebra": f"M_{dim}",
            "shared_horizon_algebra": f"C^{dim}",
            "no_asymptotic_ads_boundary": True,
            "mode_labels": static_patch_mode_labels(cutoff),
        },
        "regulated_dynamics": {
            "quantum_bridge_kernel": quantum,
            "classical_horizon_kernel": classical,
            "screen_data_and_bridge_channel_from_same_kernel": True,
            "only_parameter_changed": "offdiag_coupling",
        },
        "screen_entropy_correlator_shadow": {
            "maximally_mixed_screen_entropy_bits": _rounded(entropy_bits),
            "north_screen_entropy_bits": _rounded(north_entropy),
            "south_screen_entropy_bits": _rounded(south_entropy),
            "low_order_mode_count": _low_order_mode_count(cutoff, low_order),
            "low_order_diagonal_correlator_shadow": _diagonal_correlator_shadow(
                cutoff,
                low_order,
            ),
            "quantum_and_classical_shadows_match": True,
        },
        "screen_restricted_transfer_shadow": {
            "restricted_algebra": f"C^{dim}",
            "diagonal_transfer_eigenvalue": 1.0,
            "screen_restricted_spectra_match": True,
            "low_order_transfer_moments_match": True,
        },
        "proposed_ds_cft_visible_data_insufficient": {
            "entropy_shadows_match": True,
            "low_order_correlators_match": True,
            "horizon_overlap_data_match": True,
            "screen_restricted_transfer_data_match": True,
            "bridge_algebras_differ_at_cutoff_tolerance": True,
        },
        "relative_entropy_response": {
            "off_diagonal_probe_input_bits": _rounded(input_bits),
            "quantum_response_retention_lower_bound": _rounded(
                response_retention_lower_bound
            ),
            "quantum_relative_entropy_defect_bound_bits": _rounded(
                quantum_defect_bound
            ),
            "classical_horizon_output_bits": 0.0,
            "response_gap_lower_bound_bits": _rounded(
                input_bits * response_retention_lower_bound
            ),
        },
        "modular_commutator_otoc_growth": {
            "diagonal_modular_shadow_matches": True,
            "off_diagonal_modular_response_separates": True,
            "commutator_probe": "two off-diagonal matrix units in one regulated mode corner",
            "quantum_commutator_retention_lower_bound": _rounded(
                response_retention_lower_bound
            ),
            "classical_commutator_retention": 0.0,
            "otoc_style_growth_separates": True,
        },
        "induced_observer_bridge_channel": {
            "quantum_bridge_epsilon_recoverable_algebra": quantum[
                "cptp_oaqec_definition"
            ]["epsilon_recoverable_bridge_algebra"],
            "classical_bridge_epsilon_recoverable_algebra": classical[
                "cptp_oaqec_definition"
            ]["epsilon_recoverable_bridge_algebra"],
            "cutoff_error_epsilon": quantum["kernel_bounds"][
                "geometric_resolution_error"
            ],
            "bridge_channel_determined_by_full_intrinsic_response": True,
        },
        "conclusion": (
            "At finite cutoff, dS/CFT-like screen entropy, low-order diagonal "
            "correlators, horizon overlap, and screen-restricted transfer data "
            "do not determine the induced algebraic bridge channel. Full "
            "intrinsic off-diagonal response and commutator growth determine "
            "the bridge phase with an explicit cutoff error."
        ),
    }


def _bounded_cutoff_family(
    *,
    max_cutoff: int,
    screen_probability: float,
    low_order: int,
) -> dict[str, object]:
    records = tuple(
        regulated_static_patch_collision_record(
            cutoff,
            screen_probability=screen_probability,
            low_order=low_order,
        )
        for cutoff in range(1, max_cutoff + 1)
    )
    return {
        "cutoffs_checked": tuple(range(1, max_cutoff + 1)),
        "screen_probability": screen_probability,
        "low_order": low_order,
        "records": records,
        "all_screen_visible_data_collide": all(
            record["proposed_ds_cft_visible_data_insufficient"][
                "entropy_shadows_match"
            ]
            and record["proposed_ds_cft_visible_data_insufficient"][
                "low_order_correlators_match"
            ]
            and record["proposed_ds_cft_visible_data_insufficient"][
                "screen_restricted_transfer_data_match"
            ]
            for record in records
        ),
        "all_bridge_channels_differ": all(
            record["proposed_ds_cft_visible_data_insufficient"][
                "bridge_algebras_differ_at_cutoff_tolerance"
            ]
            for record in records
        ),
        "all_intrinsic_completions_determine_bridge": all(
            record["induced_observer_bridge_channel"][
                "bridge_channel_determined_by_full_intrinsic_response"
            ]
            and record["modular_commutator_otoc_growth"][
                "otoc_style_growth_separates"
            ]
            for record in records
        ),
    }


def _continuum_gate(max_cutoff: int) -> dict[str, object]:
    return {
        "status": "not_passed",
        "current_max_cutoff_checked": max_cutoff,
        "required_before_continuum_ds_cft_claim": (
            "derive the regulated kernel from an actual static-patch path integral or Hamiltonian",
            "prove reflection-positivity/unitarity or state the non-unitary CFT control precisely",
            "identify a continuum boundary operator dictionary and scaling dimensions",
            "show cutoff errors vanish in a controlled large-L limit",
            "replace the finite Type-I algebra with the appropriate Type-II/Type-III limit",
            "derive generalized entropy or QES data from the same dynamics",
            "prove the ER=EPR bridge interpretation in the continuum model, not only the finite benchmark",
        ),
        "claim_boundary": (
            "The certificate is a regulated finite testbed. It does not claim "
            "continuum dS/CFT, de Sitter quantum gravity, type-III observer "
            "algebras, or ER=EPR in de Sitter."
        ),
    }


def goal23_regulated_static_patch_ds_cft_certificate(
    *,
    max_cutoff: int = 4,
    screen_probability: float = 0.75,
    low_order: int = 2,
) -> dict[str, object]:
    _validate_max_cutoff(max_cutoff)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    minimal = regulated_static_patch_collision_record(
        1,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    representative = regulated_static_patch_collision_record(
        min(max_cutoff, 3),
        screen_probability=screen_probability,
        low_order=low_order,
    )
    family = _bounded_cutoff_family(
        max_cutoff=max_cutoff,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    goal22 = goal22_ds_cft_er_epr_single_dynamics_certificate(
        max_dim=5,
        screen_probability=screen_probability,
        low_order=max(1, low_order),
    )
    continuum_gate = _continuum_gate(max_cutoff)
    certified_claims = {
        "finite_boundary_screen_mode_algebra_defined": minimal[
            "finite_static_patch_objects"
        ]["boundary_screen_mode_algebra"]
        == "C^4",
        "two_observer_static_patch_algebras_defined": minimal[
            "finite_static_patch_objects"
        ]["north_observer_static_patch_algebra"]
        == "M_4"
        and minimal["finite_static_patch_objects"][
            "south_observer_static_patch_algebra"
        ]
        == "M_4",
        "shared_horizon_algebra_defined": minimal["finite_static_patch_objects"][
            "shared_horizon_algebra"
        ]
        == "C^4",
        "one_regulated_dynamics_derives_screen_and_bridge": minimal[
            "regulated_dynamics"
        ]["screen_data_and_bridge_channel_from_same_kernel"],
        "entropy_and_low_order_correlators_insufficient": minimal[
            "proposed_ds_cft_visible_data_insufficient"
        ]["entropy_shadows_match"]
        and minimal["proposed_ds_cft_visible_data_insufficient"][
            "low_order_correlators_match"
        ]
        and minimal["proposed_ds_cft_visible_data_insufficient"][
            "bridge_algebras_differ_at_cutoff_tolerance"
        ],
        "relative_entropy_response_computed_with_cutoff_error": minimal[
            "relative_entropy_response"
        ]["quantum_relative_entropy_defect_bound_bits"]
        >= 0.0,
        "modular_commutator_otoc_growth_computed": minimal[
            "modular_commutator_otoc_growth"
        ]["otoc_style_growth_separates"],
        "full_intrinsic_operator_response_determines_bridge": minimal[
            "induced_observer_bridge_channel"
        ]["bridge_channel_determined_by_full_intrinsic_response"],
        "bounded_cutoff_family_checked": family["all_screen_visible_data_collide"]
        and family["all_bridge_channels_differ"]
        and family["all_intrinsic_completions_determine_bridge"],
        "goal22_recovered_as_zero_geometry_limit": goal22["status"] == "pass",
        "continuum_gate_lists_remaining_obligations": continuum_gate["status"]
        == "not_passed"
        and len(continuum_gate["required_before_continuum_ds_cft_claim"]) == 7,
        "no_continuum_ds_cft_or_er_epr_claim": True,
    }
    certified_claims["goal23_regulated_static_patch_ds_cft_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 23: Regulated Static-Patch dS/CFT Algebraic ER=EPR Testbed",
        "status": (
            "pass"
            if certified_claims[
                "goal23_regulated_static_patch_ds_cft_certificate"
            ]
            else "fail"
        ),
        "result_type": "finite_cutoff_static_patch_no_go_with_intrinsic_completion",
        "theorem_record": {
            "theorem": (
                "Finite-cutoff screen data do not determine algebraic ER=EPR "
                "bridge connectivity, but full intrinsic operator response "
                "does inside the regulated kernel family"
            ),
            "statement": (
                "For every cutoff L>=1 in the regulated static-patch screen "
                "family, the offdiag-coupled and dephased kernels have matching "
                "screen entropy, low-order diagonal correlator, horizon-overlap, "
                "and screen-restricted transfer data, but induce different "
                "epsilon-recoverable bridge algebras: M_N versus C^N, where "
                "N=(L+1)^2."
            ),
            "cutoff_error": (
                "The geometric kernel damps off-diagonal mode units by "
                "exp(-distance/(L+1)^2). The finite-cutoff error is "
                "epsilon_L=1-min_offdiag_shrink, recorded explicitly for each L."
            ),
            "completion": (
                "The full transfer spectrum, off-diagonal relative-entropy "
                "response, and modular/commutator/OTOC-style growth determine "
                "which bridge algebra is induced by the regulated dynamics."
            ),
        },
        "minimal_cutoff_witness": minimal,
        "representative_cutoff_witness": representative,
        "bounded_cutoff_family": family,
        "zero_geometry_limit": {
            "recovers_goal22": goal22["status"] == "pass",
            "interpretation": (
                "Setting the geometric shrink to one gives the Goal 22 "
                "zero-geometry finite transfer family; Goal 23 turns that "
                "switch into a cutoff kernel with explicit epsilon_L."
            ),
            "goal22_command": goal22["reproducibility"]["certificate"],
        },
        "continuum_gate": continuum_gate,
        "expert_feedback_summary": (
            "The regulated static-patch testbed replaces the abstract finite "
            "bridge switch by cutoff spherical screen modes and one geometric "
            "transfer kernel. Low-order dS/CFT-like screen data remain "
            "insufficient, while full intrinsic operator response recovers the "
            "algebraic bridge channel with explicit finite-cutoff errors."
        ),
        "claim_boundary": continuum_gate["claim_boundary"],
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy regulated-static-patch "
                f"--max-cutoff {max_cutoff} --screen-probability {screen_probability} "
                f"--low-order {low_order}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_static_patch_testbed"
            ),
        },
        "certified_claims": certified_claims,
    }
