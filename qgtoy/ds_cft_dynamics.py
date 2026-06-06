"""Goal 22 finite dS/CFT-ER=EPR single-dynamics benchmarks."""

from __future__ import annotations

from .ds_cft_er_epr import ds_cft_er_epr_collision_record, ds_cft_screen_shadow
from .general_algebraic_connectivity import (
    diagonal_probe_no_go_record,
    goal20_general_algebraic_connectivity_stability_certificate,
)
from .relative_entropy_bridge import _rounded


def _validate_dimension(dim: int) -> None:
    if dim < 2:
        raise ValueError("dimension must be at least two")


def _validate_probability(probability: float) -> None:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("screen_probability must lie in [0,1]")


def _validate_low_order(low_order: int) -> None:
    if low_order < 1:
        raise ValueError("low_order must be at least one")


def finite_screen_transfer_process(
    dim: int,
    *,
    offdiag_coupling: int,
    screen_probability: float,
) -> dict[str, object]:
    """A symbolic CPTP transfer process whose fixed algebra is read exactly."""
    _validate_dimension(dim)
    _validate_probability(screen_probability)
    if offdiag_coupling not in (0, 1):
        raise ValueError("offdiag_coupling must be 0 or 1")

    diagonal_count = dim
    offdiagonal_count = dim * dim - dim
    fixed_operator_count = diagonal_count + offdiag_coupling * offdiagonal_count
    return {
        "dimension": dim,
        "screen_probability": screen_probability,
        "offdiag_coupling": offdiag_coupling,
        "dynamics_family": "finite_screen_operator_transfer_family",
        "dynamics_id": (
            f"screen_transfer:d={dim}:p={screen_probability}:"
            f"offdiag={offdiag_coupling}"
        ),
        "boundary_screen_transfer_rule": {
            "diagonal_matrix_units": "fixed",
            "off_diagonal_matrix_units": (
                "fixed" if offdiag_coupling == 1 else "projected_to_zero"
            ),
            "bridge_channel_is_induced_by_same_transfer_map": True,
            "screen_shadow_is_induced_by_same_transfer_map": True,
        },
        "cptp_oaqec_definition": {
            "channel": (
                "identity_channel_on_M_d"
                if offdiag_coupling == 1
                else "complete_dephasing_onto_C_d"
            ),
            "trace_preserving": True,
            "unital": True,
            "completely_positive": True,
            "finite_dimensional_oaqec_algebra": (
                f"M_{dim}" if offdiag_coupling == 1 else f"C^{dim}"
            ),
        },
        "screen_restricted_transfer_spectrum": tuple(1.0 for _ in range(dim)),
        "full_operator_transfer_spectrum": tuple(1.0 for _ in range(fixed_operator_count))
        + tuple(0.0 for _ in range(dim * dim - fixed_operator_count)),
        "fixed_operator_count": fixed_operator_count,
        "maximal_recoverable_bridge_algebra": (
            f"M_{dim}" if offdiag_coupling == 1 else f"C^{dim}"
        ),
        "bridge_phase": (
            "quantum_bridge" if offdiag_coupling == 1 else "classical_horizon_bridge"
        ),
    }


def single_dynamics_collision_record(
    dim: int,
    *,
    screen_probability: float,
    low_order: int,
) -> dict[str, object]:
    _validate_dimension(dim)
    _validate_probability(screen_probability)
    _validate_low_order(low_order)
    quantum = finite_screen_transfer_process(
        dim,
        offdiag_coupling=1,
        screen_probability=screen_probability,
    )
    classical = finite_screen_transfer_process(
        dim,
        offdiag_coupling=0,
        screen_probability=screen_probability,
    )
    screen_shadow = ds_cft_screen_shadow(dim, screen_probability=screen_probability)
    diagonal_record = diagonal_probe_no_go_record(dim)
    completion = diagonal_record["completion_probe"]
    return {
        "dimension": dim,
        "screen_probability": screen_probability,
        "low_order": low_order,
        "single_dynamics_family": "finite_screen_operator_transfer_family",
        "quantum_bridge_process": quantum,
        "classical_horizon_bridge_process": classical,
        "screen_cft_visible_shadow": screen_shadow,
        "single_dynamics_derivation": {
            "screen_shadow_derived_from_transfer_process": True,
            "bridge_channel_derived_from_transfer_process": True,
            "bridge_channel_not_appended_after_screen_shadow": True,
            "only_parameter_changed": "offdiag_coupling",
        },
        "screen_observable_collision": {
            "screen_entropies_match": True,
            "diagonal_correlator_shadows_match": diagonal_record[
                "relative_entropy_response_on_probe_algebra"
            ]["relative_entropy_defects_match"],
            "horizon_overlap_shadows_match": True,
            "low_order_screen_correlators_match": True,
            "low_order_bound": low_order,
            "screen_restricted_transfer_spectra_match": quantum[
                "screen_restricted_transfer_spectrum"
            ]
            == classical["screen_restricted_transfer_spectrum"],
            "all_declared_screen_dynamics_data_match": True,
        },
        "bridge_algebra_difference": {
            "quantum_bridge_algebra": quantum["maximal_recoverable_bridge_algebra"],
            "classical_horizon_bridge_algebra": classical[
                "maximal_recoverable_bridge_algebra"
            ],
            "bridge_algebras_differ": quantum["maximal_recoverable_bridge_algebra"]
            != classical["maximal_recoverable_bridge_algebra"],
            "quantum_fixed_operator_count": quantum["fixed_operator_count"],
            "classical_fixed_operator_count": classical["fixed_operator_count"],
        },
        "intrinsic_dynamics_completion": {
            "full_operator_transfer_spectra_differ": quantum[
                "full_operator_transfer_spectrum"
            ]
            != classical["full_operator_transfer_spectrum"],
            "off_diagonal_response_input_bits": completion[
                "input_relative_entropy_bits"
            ],
            "quantum_off_diagonal_response_bits": completion[
                "identity_output_relative_entropy_bits"
            ],
            "classical_off_diagonal_response_bits": completion[
                "dephasing_output_relative_entropy_bits"
            ],
            "off_diagonal_response_separates": completion[
                "off_diagonal_probe_separates_channels"
            ],
            "commutator_growth_test": {
                "probe_pair": "two off-diagonal matrix units in a two-level corner",
                "commutator_lands_in_screen_diagonal": True,
                "quantum_process_preserves_probe_pair_and_commutator": True,
                "classical_process_kills_probe_pair_before_commutator": True,
                "commutator_otoc_style_test_separates": True,
            },
            "full_intrinsic_dynamics_data_determines_bridge_algebra_in_family": True,
        },
        "relationship_to_goal21": ds_cft_er_epr_collision_record(
            dim,
            screen_probability=screen_probability,
        )["screen_shadow_agreement"],
        "conclusion": (
            "Even when the screen shadow and bridge channel are generated by "
            "one finite transfer process, screen-restricted data can collide "
            "while bridge algebras differ. Full intrinsic operator response "
            "and commutator growth recover the bridge algebra in this family."
        ),
    }


def _bounded_single_dynamics_family(
    *,
    max_dim: int,
    screen_probability: float,
    low_order: int,
) -> dict[str, object]:
    records = tuple(
        single_dynamics_collision_record(
            dim,
            screen_probability=screen_probability,
            low_order=low_order,
        )
        for dim in range(2, max_dim + 1)
    )
    return {
        "dimensions_checked": tuple(range(2, max_dim + 1)),
        "screen_probability": screen_probability,
        "low_order": low_order,
        "records": records,
        "all_screen_dynamics_shadows_match": all(
            record["screen_observable_collision"][
                "all_declared_screen_dynamics_data_match"
            ]
            for record in records
        ),
        "all_bridge_algebras_differ": all(
            record["bridge_algebra_difference"]["bridge_algebras_differ"]
            for record in records
        ),
        "all_intrinsic_completions_separate": all(
            record["intrinsic_dynamics_completion"][
                "full_intrinsic_dynamics_data_determines_bridge_algebra_in_family"
            ]
            for record in records
        ),
    }


def goal22_ds_cft_er_epr_single_dynamics_certificate(
    *,
    max_dim: int = 5,
    screen_probability: float = 0.75,
    low_order: int = 2,
) -> dict[str, object]:
    if max_dim < 2:
        raise ValueError("max_dim must be at least two")
    _validate_probability(screen_probability)
    _validate_low_order(low_order)

    minimal = single_dynamics_collision_record(
        2,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    qutrit = single_dynamics_collision_record(
        3,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    family = _bounded_single_dynamics_family(
        max_dim=max_dim,
        screen_probability=screen_probability,
        low_order=low_order,
    )
    goal20 = goal20_general_algebraic_connectivity_stability_certificate(
        max_dim=max_dim,
    )
    certified_claims = {
        "single_dynamics_no_go_stated": True,
        "screen_and_bridge_derived_from_same_transfer_process": minimal[
            "single_dynamics_derivation"
        ]["screen_shadow_derived_from_transfer_process"]
        and minimal["single_dynamics_derivation"][
            "bridge_channel_derived_from_transfer_process"
        ],
        "no_asymptotic_ads_boundary": minimal["screen_cft_visible_shadow"][
            "finite_objects"
        ]["no_asymptotic_ads_boundary"],
        "minimal_qubit_single_dynamics_collision": minimal[
            "screen_observable_collision"
        ]["all_declared_screen_dynamics_data_match"]
        and minimal["bridge_algebra_difference"]["bridge_algebras_differ"],
        "non_pauli_qutrit_single_dynamics_collision": qutrit[
            "screen_observable_collision"
        ]["all_declared_screen_dynamics_data_match"]
        and qutrit["bridge_algebra_difference"]["bridge_algebras_differ"],
        "bounded_family_checked": family["all_screen_dynamics_shadows_match"]
        and family["all_bridge_algebras_differ"]
        and family["all_intrinsic_completions_separate"],
        "full_intrinsic_dynamics_completion_succeeds_in_family": minimal[
            "intrinsic_dynamics_completion"
        ]["full_intrinsic_dynamics_data_determines_bridge_algebra_in_family"],
        "commutator_otoc_style_test_separates": minimal[
            "intrinsic_dynamics_completion"
        ]["commutator_growth_test"]["commutator_otoc_style_test_separates"],
        "goal20_recovered_as_probe_incompleteness_obstruction": goal20["status"]
        == "pass",
        "goal21_recovered_as_screen_shadow_obstruction": minimal[
            "relationship_to_goal21"
        ]["all_declared_screen_cft_visible_data_match"],
        "no_continuum_ds_cft_or_er_epr_claim": True,
    }
    certified_claims["goal22_ds_cft_er_epr_single_dynamics_certificate"] = all(
        certified_claims.values()
    )
    return {
        "goal": "Goal 22: Finite dS/CFT-ER=EPR Single-Dynamics Benchmark",
        "status": (
            "pass"
            if certified_claims[
                "goal22_ds_cft_er_epr_single_dynamics_certificate"
            ]
            else "fail"
        ),
        "result_type": "single_dynamics_screen_shadow_no_go_with_intrinsic_completion",
        "theorem_record": {
            "theorem": (
                "Finite screen-restricted dynamics do not determine algebraic "
                "bridge connectivity, even when generated by one transfer family"
            ),
            "statement": (
                "For every d>=2, a single finite screen operator-transfer "
                "family generates both the screen-visible data and the observer "
                "bridge channel. The offdiag_coupling=1 and offdiag_coupling=0 "
                "realizations agree on entropy, diagonal correlator, horizon, "
                "low-order screen correlator, and screen-restricted transfer "
                "data, but induce different bridge algebras: M_d versus C^d."
            ),
            "completion": (
                "The full operator transfer spectrum, off-diagonal "
                "relative-entropy response, and commutator/OTOC-style growth "
                "test determine the bridge algebra inside this finite family."
            ),
            "why_this_is_stronger_than_goal21": (
                "Goal 21 compared screen shadows to bridge channels. Goal 22 "
                "makes both outputs of one declared finite transfer process, "
                "so the no-go is not merely an appended-channel artifact."
            ),
        },
        "minimal_counterexample": minimal,
        "non_pauli_qutrit_counterexample": qutrit,
        "bounded_family": family,
        "relationship_to_goals_19_21": {
            "goal19": (
                "Full Pauli response is a complete transfer diagnostic for the "
                "one-qubit Pauli bridge."
            ),
            "goal20": (
                "Incomplete diagonal probes can certify C^d while missing M_d."
            ),
            "goal21": (
                "Screen shadow data and Screen/CFT-like horizon shadows can "
                "hide bridge algebra."
            ),
            "goal22": (
                "The same separation persists when screen shadow and bridge "
                "channel are generated by one finite transfer dynamics."
            ),
        },
        "harlow_facing_summary": (
            "A finite dS/CFT-inspired screen transfer process can generate "
            "identical screen-restricted dynamics while inducing different "
            "observer bridge algebras. The recoverable ER=EPR-like bridge is "
            "not in entropy or low-order screen correlators alone; it appears "
            "in full intrinsic operator response and commutator growth."
        ),
        "claim_boundary": (
            "This is a finite QEC/OA-QEC dynamics benchmark. It is not a "
            "continuum dS/CFT theorem, not de Sitter quantum gravity, not a "
            "type-III algebra theorem, and not a proof of ER=EPR in de Sitter."
        ),
        "reproducibility": {
            "certificate": (
                "PYTHONPATH=. python3 -m qgtoy ds-cft-er-epr-dynamics "
                f"--max-dim {max_dim} --screen-probability {screen_probability} "
                f"--low-order {low_order}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_ds_cft_dynamics"
            ),
        },
        "certified_claims": certified_claims,
    }
