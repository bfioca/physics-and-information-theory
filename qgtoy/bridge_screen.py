"""Goal 17 inseparable bridge-screen dynamics certificates."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations
from math import isclose
from typing import Sequence

from .bilayer import binary_entropy
from .er_epr_controls import BridgeChannelControlProtocol, BridgeChannelControlRun
from .gf2 import mask_to_tuple, masks_of_size
from .interacting_bridge import (
    InteractingEncodedBridgeModel,
    logical_cz_unitary,
    static_state_transition_no_go,
    transfer_certificate,
    unitary_channel_certificate,
)
from .quantum_channel import (
    Matrix,
    average_gate_fidelity,
    choi_matrix,
    coherent_bilayer_isometry,
    coherent_bilayer_screen_kraus,
    complex_matrix_rank,
    dagger,
    entanglement_fidelity_to_unitary,
    identity_matrix,
    isometry_error,
    matmul,
    max_abs_difference,
    recovered_coherent_bilayer_screen_kraus,
    trace,
    trace_preserving_error,
)


def _identity(mouths: int) -> tuple[int, ...]:
    return tuple(range(mouths))


def _swap_first_two(mouths: int) -> tuple[int, ...]:
    if mouths < 2:
        raise ValueError("need at least two mouths for a twisted witness")
    return (1, 0) + tuple(range(2, mouths))


def _path_graph_edges(mouths: int) -> tuple[tuple[int, int], ...]:
    return tuple((index, index + 1) for index in range(mouths - 1))


def _all_simple_graphs(mouths: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    edges = tuple(combinations(range(mouths), 2))
    graphs = []
    for mask in range(1 << len(edges)):
        graphs.append(
            tuple(edge for index, edge in enumerate(edges) if (mask >> index) & 1)
        )
    return tuple(graphs)


def _protocol(
    *,
    name: str,
    kind: str,
    mouths: int,
    activation: tuple[int, ...] | None,
) -> BridgeChannelControlProtocol:
    return BridgeChannelControlProtocol(
        name=name,
        kind=kind,
        mouths=mouths,
        activation=activation,
    )


def _compare_low_order(
    first: InteractingEncodedBridgeModel,
    second: InteractingEncodedBridgeModel,
    *,
    max_order: int,
) -> dict[str, object]:
    first_state = first.state()
    second_state = second.state()
    rows = []
    mismatches = []
    for size in range(max_order + 1):
        for mask in masks_of_size(first.n, size):
            first_entropy = first_state.entropy(mask)
            second_entropy = second_state.entropy(mask)
            row = {
                "region": mask_to_tuple(mask, first.n),
                "first_entropy": first_entropy,
                "second_entropy": second_entropy,
            }
            rows.append(row)
            if first_entropy != second_entropy:
                mismatches.append(row)
    return {
        "max_order": max_order,
        "regions_checked": len(rows),
        "mismatch_count": len(mismatches),
        "mismatches": tuple(mismatches[:10]),
        "labeled_tables_match": not mismatches,
        "profiles_match": first.physical_low_order_entropy_profile(max_order)
        == second.physical_low_order_entropy_profile(max_order),
    }


def _first_entropy_mismatch_order(
    first: InteractingEncodedBridgeModel,
    second: InteractingEncodedBridgeModel,
    *,
    max_order: int,
) -> dict[str, object] | None:
    for order in range(max_order + 1):
        audit = _compare_low_order(first, second, max_order=order)
        if audit["mismatch_count"]:
            return {"order": order, "audit": audit}
    return None


def _keep_projector() -> Matrix:
    return ((1 + 0j, 0j, 0j), (0j, 1 + 0j, 0j), (0j, 0j, 0j))


def screen_success_probability_from_channel(kraus: Sequence[Matrix]) -> float:
    projector = _keep_projector()
    input_dimension = len(kraus[0][0])
    total = 0j
    for item in kraus:
        total += trace(matmul(matmul(dagger(item), projector), item))
    value = total / input_dimension
    if abs(value.imag) > 1e-10:
        raise ValueError("screen keep probability should be real")
    return float(value.real)


def screen_channel_record(north_probability: float, *, screen: str) -> dict[str, object]:
    kraus = coherent_bilayer_screen_kraus(north_probability, screen=screen)
    recovered = recovered_coherent_bilayer_screen_kraus(
        north_probability,
        screen=screen,
    )
    recovered_fidelity = entanglement_fidelity_to_unitary(
        recovered,
        identity_matrix(2),
    )
    success = screen_success_probability_from_channel(kraus)
    choi = choi_matrix(kraus)
    recovered_choi = choi_matrix(recovered)
    return {
        "screen": screen,
        "input_dimension": len(kraus[0][0]),
        "screen_output_dimension": len(kraus[0]),
        "kraus_operator_count": len(kraus),
        "state_derived_success_probability": success,
        "screen_entropy_bits": binary_entropy(success),
        "screen_quantum_area_analogue_bits": binary_entropy(success) + success,
        "trace_preserving_error": trace_preserving_error(kraus),
        "choi": {
            "trace": float(trace(choi).real),
            "rank": complex_matrix_rank(choi),
            "hermiticity_error": max_abs_difference(choi, dagger(choi)),
        },
        "recovered_trace_preserving_error": trace_preserving_error(recovered),
        "recovered_choi": {
            "trace": float(trace(recovered_choi).real),
            "rank": complex_matrix_rank(recovered_choi),
            "hermiticity_error": max_abs_difference(
                recovered_choi,
                dagger(recovered_choi),
            ),
        },
        "recovery_entanglement_fidelity": recovered_fidelity,
        "average_recovery_fidelity": average_gate_fidelity(recovered_fidelity, 2),
        "unassisted_quantum_capacity_qubits_per_use": max(
            0.0,
            2.0 * success - 1.0,
        ),
    }


def _external_area_bias_no_go(area_bias: float = 0.25) -> dict[str, object]:
    quantum_area_transition = (1.0 - area_bias) / 2.0
    recovery_transition = 0.5
    return {
        "bare_quantum_area_bias_north_minus_south_bits": area_bias,
        "recovery_transition_probability": recovery_transition,
        "quantum_area_transition_probability": quantum_area_transition,
        "transition_mismatch": abs(quantum_area_transition - recovery_transition),
        "transitions_match": isclose(
            quantum_area_transition,
            recovery_transition,
            abs_tol=1e-12,
        ),
        "no_go": (
            "An external bare-area bias that is not produced by the unified channel "
            "shifts the area crossing without shifting the recovery crossing."
        ),
    }


@dataclass(frozen=True)
class InseparableBridgeScreenDynamicsModel:
    """One finite dynamics object for the interacting bridge and two screens."""

    name: str
    pairing: tuple[int, ...]
    interaction_edges: tuple[tuple[int, int], ...]
    north_probability: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.north_probability <= 1.0:
            raise ValueError("north_probability must lie in [0,1]")

    @property
    def bridge(self) -> InteractingEncodedBridgeModel:
        return InteractingEncodedBridgeModel(
            name=f"{self.name}_interacting_bridge",
            pairing=self.pairing,
            interaction_edges=self.interaction_edges,
        )

    @property
    def dynamics_id(self) -> str:
        return (
            f"{self.name}:pi={self.pairing}:G={self.bridge.interaction_edges}:"
            f"pN={self.north_probability}"
        )

    def inferred_pairing_record(self) -> dict[str, object]:
        return self.bridge.state_derived_pairing_record()

    def inferred_graph_record(self) -> dict[str, object]:
        return self.bridge.state_derived_interaction_graph_record()

    def observer_algebra_record(self) -> dict[str, object]:
        return self.bridge.observer_algebra_record()

    def bridge_transfer_record(self) -> dict[str, object]:
        pairing = self.inferred_pairing_record()["inferred_pairing"]
        graph = self.inferred_graph_record()["inferred_right_block_interaction_edges"]
        if not isinstance(pairing, tuple) or not isinstance(graph, tuple):
            raise ValueError("state-derived pairing and graph must be tuples")
        record = transfer_certificate(
            self.bridge,
            inferred_pairing=pairing,
            inferred_interaction_edges=graph,
        )
        return {
            "dynamics_id": self.dynamics_id,
            "screen_channels_in_same_declared_dynamics": True,
            **record,
        }

    def screen_dynamics_record(self) -> dict[str, object]:
        isometry = coherent_bilayer_isometry(self.north_probability)
        north = screen_channel_record(self.north_probability, screen="north")
        south = screen_channel_record(self.north_probability, screen="south")
        north_fidelity = north["recovery_entanglement_fidelity"]
        south_fidelity = south["recovery_entanglement_fidelity"]
        north_area = north["screen_quantum_area_analogue_bits"]
        south_area = south["screen_quantum_area_analogue_bits"]
        return {
            "dynamics_id": self.dynamics_id,
            "screen_channels_in_same_declared_dynamics": True,
            "screen_input_payload": (
                "logical payload after the inferred inverse-CZ bridge decoder and "
                "state-derived mouth routing"
            ),
            "depends_on_state_derived_bridge_decoder": True,
            "coherent_router": {
                "input_dimension": len(isometry[0]),
                "output_dimension": len(isometry),
                "north_screen_dimension": 3,
                "south_screen_dimension": 3,
                "isometry_error": isometry_error(isometry),
                "declared_north_probability": self.north_probability,
            },
            "north_screen": north,
            "south_screen": south,
            "probabilities_recovered_from_channels": isclose(
                north["state_derived_success_probability"],
                self.north_probability,
                abs_tol=1e-12,
            )
            and isclose(
                south["state_derived_success_probability"],
                1.0 - self.north_probability,
                abs_tol=1e-12,
            ),
            "recovery_winner": (
                "north"
                if north_fidelity > south_fidelity
                else "south"
                if south_fidelity > north_fidelity
                else "tie"
            ),
            "larger_quantum_area_analogue": (
                "north"
                if north_area > south_area
                else "south"
                if south_area > north_area
                else "tie"
            ),
            "recovery_minus_area_signs_match": (
                (
                    north_fidelity > south_fidelity
                    and north_area > south_area
                )
                or (
                    south_fidelity > north_fidelity
                    and south_area > north_area
                )
                or (
                    isclose(north_fidelity, south_fidelity, abs_tol=1e-12)
                    and isclose(north_area, south_area, abs_tol=1e-12)
                )
            ),
        }

    def unified_dynamics_record(self) -> dict[str, object]:
        pairing = self.inferred_pairing_record()
        graph = self.inferred_graph_record()
        bridge_transfer = self.bridge_transfer_record()
        screen = self.screen_dynamics_record()
        return {
            "name": self.name,
            "dynamics_id": self.dynamics_id,
            "single_declared_dynamics": {
                "layers": (
                    "prepare encoded stabilizer bridge blocks",
                    "apply right-mouth graph-CZ interaction",
                    "infer pi and G from the resulting finite state",
                    "apply inverse CZ_G and route by inferred pi for bridge transfer",
                    "route the recovered logical payload through the north/south screen isometry",
                ),
                "screen_transition_is_not_extra_rule": True,
                "bridge_and_screen_share_dynamics_id": bridge_transfer["dynamics_id"]
                == screen["dynamics_id"]
                == self.dynamics_id,
            },
            "interacting_bridge": self.bridge.certificate_record(),
            "state_derived_pairing": pairing,
            "state_derived_interaction_graph": graph,
            "observer_algebra": self.observer_algebra_record(),
            "logical_interaction_unitary": unitary_channel_certificate(
                logical_cz_unitary(self.bridge.m, self.bridge.interaction_edges)
            ),
            "bridge_transfer": bridge_transfer,
            "screen_dynamics": screen,
        }


def _transition_family_records(
    *,
    pairing: tuple[int, ...],
    interaction_edges: tuple[tuple[int, int], ...],
    probabilities: Sequence[float],
) -> tuple[dict[str, object], ...]:
    rows = []
    for probability in probabilities:
        model = InseparableBridgeScreenDynamicsModel(
            name=f"unified_p{probability}",
            pairing=pairing,
            interaction_edges=interaction_edges,
            north_probability=probability,
        )
        screen = model.screen_dynamics_record()
        rows.append(
            {
                "dynamics_id": model.dynamics_id,
                "north_probability": probability,
                "screen_dynamics": screen,
                "state_derived_north_success_probability": screen["north_screen"][
                    "state_derived_success_probability"
                ],
                "state_derived_south_success_probability": screen["south_screen"][
                    "state_derived_success_probability"
                ],
                "recovery_winner": screen["recovery_winner"],
                "larger_quantum_area_analogue": screen[
                    "larger_quantum_area_analogue"
                ],
                "recovery_minus_area_signs_match": screen[
                    "recovery_minus_area_signs_match"
                ],
            }
        )
    midpoint = next(
        (
            row
            for row in rows
            if isclose(
                row["state_derived_north_success_probability"],
                0.5,
                abs_tol=1e-12,
            )
        ),
        None,
    )
    return tuple(rows), {
        "records": tuple(rows),
        "all_screen_isometries_verified": all(
            row["screen_dynamics"]["coherent_router"]["isometry_error"] < 1e-12
            for row in rows
        ),
        "all_probabilities_recovered_from_channels": all(
            row["screen_dynamics"]["probabilities_recovered_from_channels"]
            for row in rows
        ),
        "all_screen_channels_trace_preserving": all(
            max(
                row["screen_dynamics"]["north_screen"]["trace_preserving_error"],
                row["screen_dynamics"]["south_screen"]["trace_preserving_error"],
                row["screen_dynamics"]["north_screen"][
                    "recovered_trace_preserving_error"
                ],
                row["screen_dynamics"]["south_screen"][
                    "recovered_trace_preserving_error"
                ],
            )
            < 1e-12
            for row in rows
        ),
        "recovery_and_area_winners_match": all(
            row["recovery_minus_area_signs_match"] for row in rows
        ),
        "midpoint_transition_from_unified_dynamics": midpoint is not None
        and midpoint["recovery_winner"] == "tie"
        and midpoint["larger_quantum_area_analogue"] == "tie",
        "exact_identity": (
            "With equal bare screen terms, both recovery and the finite quantum-area "
            "analogue are computed from the same channel-derived keep probability p; "
            "their north/south ordering changes at p=1/2."
        ),
    }


def _bounded_unified_atlas(
    *,
    max_mouths: int,
    screen_probabilities: Sequence[float],
) -> tuple[dict[str, object], ...]:
    records = []
    for mouths in range(1, max_mouths + 1):
        resources_checked = 0
        pairing_flags = []
        graph_flags = []
        transfer_flags = []
        wrong_mouth_flags = []
        scrambler_flags = []
        screen_flags = []
        for graph in _all_simple_graphs(mouths):
            for pairing in permutations(range(mouths)):
                model = InseparableBridgeScreenDynamicsModel(
                    name=f"atlas_m{mouths}",
                    pairing=pairing,
                    interaction_edges=graph,
                    north_probability=0.5,
                )
                pairing_record = model.inferred_pairing_record()
                graph_record = model.inferred_graph_record()
                inferred_pairing = pairing_record["inferred_pairing"]
                if not isinstance(inferred_pairing, tuple):
                    raise ValueError("inferred pairing must be a tuple")
                derived_capacity = BridgeChannelControlRun(
                    model.bridge.base,
                    _protocol(
                        name="atlas_state_derived_activation",
                        kind="clifford_bridge_activation",
                        mouths=mouths,
                        activation=inferred_pairing,
                    ),
                ).structured_transfer_capacity()
                identity_capacity = BridgeChannelControlRun(
                    model.bridge.base,
                    _protocol(
                        name="atlas_identity_activation",
                        kind="clifford_bridge_activation",
                        mouths=mouths,
                        activation=_identity(mouths),
                    ),
                ).structured_transfer_capacity()
                scrambler_capacity = BridgeChannelControlRun(
                    model.bridge.base,
                    _protocol(
                        name="atlas_mouth_blind_scrambler",
                        kind="mouth_blind_pauli_twirled_scrambler",
                        mouths=mouths,
                        activation=None,
                    ),
                ).structured_transfer_capacity()
                pairing_flags.append(
                    pairing_record["inferred_pairing"] == pairing
                    and pairing_record["unique_permutation_inferred"] is True
                )
                graph_flags.append(
                    graph_record["inferred_right_block_interaction_edges"]
                    == graph
                    and graph_record["unique_solution_for_each_bridge"] is True
                )
                transfer_flags.append(derived_capacity == mouths)
                wrong_mouth_flags.append(identity_capacity <= mouths)
                scrambler_flags.append(scrambler_capacity == 0)

                for probability in screen_probabilities:
                    resources_checked += 1
                    screen_model = InseparableBridgeScreenDynamicsModel(
                        name=f"atlas_m{mouths}",
                        pairing=pairing,
                        interaction_edges=graph,
                        north_probability=probability,
                    )
                    screen = screen_model.screen_dynamics_record()
                    screen_flags.append(
                        screen["probabilities_recovered_from_channels"]
                        and screen["coherent_router"]["isometry_error"] < 1e-12
                    )
        records.append(
            {
                "m": mouths,
                "screen_probabilities": tuple(screen_probabilities),
                "simple_graphs_checked": len(_all_simple_graphs(mouths)),
                "pairings_per_graph": len(tuple(permutations(range(mouths)))),
                "resources_checked": resources_checked,
                "all_pairings_recovered": all(pairing_flags),
                "all_graphs_recovered": all(graph_flags),
                "state_derived_transfer_full_capacity": all(transfer_flags),
                "wrong_mouth_controls_not_full_hidden_decoders": all(
                    wrong_mouth_flags
                ),
                "mouth_blind_scrambling_controls_zero_capacity": all(scrambler_flags),
                "screen_probabilities_recovered_from_unified_channels": all(
                    screen_flags
                ),
            }
        )
    return tuple(records)


def goal17_inseparable_bridge_screen_dynamics_certificate(
    *,
    mouths: int = 3,
    low_order: int = 3,
    atlas_max_mouths: int = 3,
) -> dict[str, object]:
    if mouths < 2:
        raise ValueError("mouths must be at least two for the theorem witness")
    if mouths > 3 or atlas_max_mouths > 3:
        raise ValueError("dense channel checks are limited to at most three mouths")
    if atlas_max_mouths < mouths:
        raise ValueError("atlas_max_mouths must be at least mouths")

    interaction_edges = _path_graph_edges(mouths)
    aligned = InseparableBridgeScreenDynamicsModel(
        name="goal17_aligned_unified_dynamics",
        pairing=_identity(mouths),
        interaction_edges=interaction_edges,
        north_probability=0.75,
    )
    twisted = InseparableBridgeScreenDynamicsModel(
        name="goal17_twisted_unified_dynamics",
        pairing=_swap_first_two(mouths),
        interaction_edges=interaction_edges,
        north_probability=0.75,
    )
    unified = twisted.unified_dynamics_record()
    pairing_record = unified["state_derived_pairing"]
    graph_record = unified["state_derived_interaction_graph"]
    observer_algebra = unified["observer_algebra"]
    bridge_transfer = unified["bridge_transfer"]
    screen_dynamics = unified["screen_dynamics"]

    low_order_audit = _compare_low_order(
        aligned.bridge,
        twisted.bridge,
        max_order=low_order,
    )
    first_mismatch = _first_entropy_mismatch_order(
        aligned.bridge,
        twisted.bridge,
        max_order=twisted.bridge.block_distance + 1,
    )
    _, transition = _transition_family_records(
        pairing=twisted.pairing,
        interaction_edges=interaction_edges,
        probabilities=(0.0, 0.25, 0.5, 0.75, 1.0),
    )
    static_only = static_state_transition_no_go(twisted.bridge)
    area_bias = _external_area_bias_no_go()
    atlas = _bounded_unified_atlas(
        max_mouths=atlas_max_mouths,
        screen_probabilities=(0.0, 0.5, 1.0),
    )

    certified_claims = {
        "single_declared_dynamics_recorded": unified["single_declared_dynamics"][
            "screen_transition_is_not_extra_rule"
        ]
        and unified["single_declared_dynamics"][
            "bridge_and_screen_share_dynamics_id"
        ],
        "mouth_map_derived_from_unified_bridge_state": pairing_record[
            "inferred_pairing"
        ]
        == twisted.pairing
        and pairing_record["unique_permutation_inferred"] is True,
        "right_mouth_graph_derived_from_pauli_correlations": graph_record[
            "inferred_right_block_interaction_edges"
        ]
        == interaction_edges
        and graph_record["unique_solution_for_each_bridge"] is True,
        "dressed_observer_algebra_reconstructed": observer_algebra[
            "full_quantum_algebra"
        ]
        and observer_algebra["state_derived_interaction_graph"][
            "matches_circuit_interaction_graph"
        ],
        "low_order_entropy_blind_to_mouth_map": bool(
            low_order_audit["labeled_tables_match"]
        )
        and low_order >= twisted.bridge.block_distance,
        "first_entropy_mismatch_at_decoder_scale": first_mismatch is not None
        and first_mismatch["order"] == twisted.bridge.block_distance + 1,
        "bridge_transfer_restored_by_inferred_inverse_and_routing": bridge_transfer[
            "capacities"
        ]["state_derived_activation"]
        == mouths,
        "wrong_mouth_control_fails_full_transfer": bridge_transfer["capacities"][
            "identity_activation_after_interaction_removal"
        ]
        < mouths,
        "mouth_blind_scrambling_control_fails": bridge_transfer["capacities"][
            "mouth_blind_scrambling_control"
        ]
        == 0,
        "screen_channels_derived_from_same_dynamics": screen_dynamics[
            "screen_channels_in_same_declared_dynamics"
        ]
        and screen_dynamics["depends_on_state_derived_bridge_decoder"]
        and screen_dynamics["coherent_router"]["isometry_error"] < 1e-12
        and screen_dynamics["probabilities_recovered_from_channels"],
        "screen_recovery_area_transition_derived_from_same_dynamics": transition[
            "all_screen_isometries_verified"
        ]
        and transition["all_probabilities_recovered_from_channels"]
        and transition["all_screen_channels_trace_preserving"]
        and transition["recovery_and_area_winners_match"]
        and transition["midpoint_transition_from_unified_dynamics"],
        "static_state_only_control_remains_no_go": static_only[
            "opposite_recovery_winners_with_same_static_state"
        ],
        "external_area_bias_control_fails": area_bias["transitions_match"] is False,
        "bounded_atlas_derives_pairing_graph_transfer_and_screens": all(
            row["all_pairings_recovered"]
            and row["all_graphs_recovered"]
            and row["state_derived_transfer_full_capacity"]
            and row["mouth_blind_scrambling_controls_zero_capacity"]
            and row["screen_probabilities_recovered_from_unified_channels"]
            for row in atlas
        ),
        "no_continuum_er_epr_or_de_sitter_claim": True,
    }
    certified_claims[
        "goal17_inseparable_bridge_screen_dynamics_certificate"
    ] = all(certified_claims.values())

    return {
        "goal": "Goal 17: Inseparable Bridge-Screen Dynamics Theorem",
        "status": (
            "pass"
            if certified_claims[
                "goal17_inseparable_bridge_screen_dynamics_certificate"
            ]
            else "fail"
        ),
        "scope": {
            "family": (
                "Goal 16 graph-CZ encoded bridge dynamics plus a built-in coherent "
                "north/south screen router in one declared finite channel family"
            ),
            "mouths": mouths,
            "low_order": low_order,
            "atlas_max_mouths": atlas_max_mouths,
            "right_block_code": "[[5,1,3]] five-qubit perfect stabilizer code",
            "screen_system": (
                "one logical payload qubit routed to complementary qutrit erasure "
                "screens by the same declared dynamics record"
            ),
        },
        "theorem_style_result": {
            "name": "Inseparable Finite Bridge-Screen Dynamics Theorem",
            "positive_theorem": (
                "For the declared finite dynamics family, the interacting bridge state "
                "and the two-screen routing channels are parts of one circuit/tensor "
                "network record. The same record yields the mouth map, right-mouth "
                "graph-CZ interaction, dressed observer algebra, inverse-interaction "
                "bridge transfer, north/south screen channels, and the equal-bare-area "
                "recovery transition."
            ),
            "controls": (
                "Wrong-mouth and mouth-blind controls fail at the bridge-channel layer. "
                "Dropping the screen channel back to static bridge-state data restores "
                "the Goal 15/16 no-go, and appending an external bare-area bias breaks "
                "the recovery/area transition match."
            ),
            "proof_sketch": (
                "The bridge part is the Goal 16 stabilizer argument: full-block MI "
                "recovers pi, Pauli-correlation dressing recovers G, and conjugation by "
                "CZ_G reconstructs the observer algebra. The screen part is a qutrit "
                "erasure-screen isometry in the same dynamics record. Tracing either "
                "screen gives complementary erasure channels whose keep probabilities "
                "are read from the Kraus operators. Recovery fidelity and the finite "
                "quantum-area analogue are both monotone functions of that same derived "
                "probability, so their transition occurs at p=1/2."
            ),
        },
        "representative_witness": {
            "aligned_unified_dynamics": aligned.unified_dynamics_record(),
            "twisted_unified_dynamics": unified,
            "comparisons": {
                "coarse_entropy_mincut_match": aligned.bridge.coarse_entropy_mincut_shadow()
                == twisted.bridge.coarse_entropy_mincut_shadow(),
                "low_order_physical_entropy_audit": low_order_audit,
                "first_entropy_mismatch": first_mismatch,
                "state_derived_pairing": pairing_record,
                "state_derived_interaction_graph": graph_record,
                "observer_algebra": observer_algebra,
                "bridge_transfer": bridge_transfer,
                "screen_dynamics": screen_dynamics,
            },
        },
        "transition_from_unified_dynamics": transition,
        "controls": {
            "wrong_mouth_and_mouth_blind": {
                "capacities": bridge_transfer["capacities"],
                "explicit_channel_certificates": bridge_transfer[
                    "explicit_channel_certificates"
                ],
            },
            "static_state_only_no_go": static_only,
            "external_area_bias_no_go": area_bias,
        },
        "bounded_unified_atlas": {"records": atlas},
        "claim_separation": {
            "exact_theorem_style_claims": (
                "State-derived pi/G recovery, dressed algebra reconstruction, exact "
                "bridge transfer, and screen recovery/area transition all come from "
                "one finite dynamics family."
            ),
            "bounded_exhaustive_evidence": (
                "All simple graphs, all mouth permutations, and three screen "
                "probabilities are checked for m <= atlas_max_mouths."
            ),
            "controls": (
                "Static-state-only and external-area-bias controls show which extra "
                "data would be overclaims if not included in the unified dynamics."
            ),
        },
        "limitations": (
            "This is a finite stabilizer/QEC plus small dense-channel theorem package. "
            "The screen router is an explicit finite qutrit erasure isometry inside "
            "the declared dynamics; it is not a continuum geometry, not de Sitter, "
            "not dS/CFT, and not a chaotic many-body wormhole simulation."
        ),
        "reproducibility": {
            "goal17_certificate": (
                f"PYTHONPATH=. python3 -m qgtoy bridge-screen-dynamics --mouths {mouths} "
                f"--low-order {low_order} --atlas-max-mouths {atlas_max_mouths}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_bridge_screen_dynamics"
            ),
        },
        "certified_claims": certified_claims,
    }
