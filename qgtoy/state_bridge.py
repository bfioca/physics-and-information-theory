"""Goal 14 state-derived bridge dynamics certificates."""

from __future__ import annotations

from itertools import permutations
from math import isclose
from typing import Sequence

from .bilayer import binary_entropy
from .er_epr_controls import BridgeChannelControlProtocol, BridgeChannelControlRun
from .er_epr_encoded import EncodedMouthBridgeModel
from .gf2 import mask_to_tuple, masks_of_size
from .quantum_channel import (
    Matrix,
    average_gate_fidelity,
    choi_matrix,
    coherent_bilayer_screen_kraus,
    dagger,
    entanglement_fidelity_to_unitary,
    identity_matrix,
    matrix,
    matmul,
    recovered_coherent_bilayer_screen_kraus,
    teleportation_channel_certificate,
    trace,
    trace_preserving_error,
)


def _identity(mouths: int) -> tuple[int, ...]:
    return tuple(range(mouths))


def _swap_first_two(mouths: int) -> tuple[int, ...]:
    if mouths < 2:
        raise ValueError("need at least two mouths for a twisted witness")
    return (1, 0) + tuple(range(2, mouths))


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
    first: EncodedMouthBridgeModel,
    second: EncodedMouthBridgeModel,
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
    first: EncodedMouthBridgeModel,
    second: EncodedMouthBridgeModel,
    *,
    max_order: int,
) -> dict[str, object] | None:
    for order in range(max_order + 1):
        audit = _compare_low_order(first, second, max_order=order)
        if audit["mismatch_count"]:
            return {"order": order, "audit": audit}
    return None


def state_derived_pairing(
    resource: EncodedMouthBridgeModel,
) -> tuple[int, ...]:
    """Infer the logical mouth pairing from the resource state's block MI."""
    state = resource.state()
    pairing = []
    score_rows = []
    for left in range(resource.m):
        left_mask = 1 << left
        scores = tuple(
            state.mutual_information(left_mask, resource.right_block_mask(block))
            for block in range(resource.m)
        )
        max_score = max(scores)
        winners = tuple(block for block, score in enumerate(scores) if score == max_score)
        if len(winners) != 1 or max_score <= 0:
            raise ValueError("resource state does not determine a unique mouth pairing")
        pairing.append(winners[0])
        score_rows.append(
            {
                "left_mouth": f"L{left}",
                "mutual_information_by_right_block": scores,
                "inferred_right_block": f"B{winners[0]}",
            }
        )
    inferred = tuple(pairing)
    if sorted(inferred) != list(range(resource.m)):
        raise ValueError("state-derived mouth map is not a permutation")
    return inferred


def state_derived_pairing_record(
    resource: EncodedMouthBridgeModel,
) -> dict[str, object]:
    state = resource.state()
    rows = []
    inferred = []
    for left in range(resource.m):
        left_mask = 1 << left
        scores = tuple(
            state.mutual_information(left_mask, resource.right_block_mask(block))
            for block in range(resource.m)
        )
        max_score = max(scores)
        winners = tuple(block for block, score in enumerate(scores) if score == max_score)
        inferred_block = winners[0] if len(winners) == 1 else None
        if inferred_block is not None:
            inferred.append(inferred_block)
        rows.append(
            {
                "left_mouth": f"L{left}",
                "mutual_information_by_right_block": scores,
                "unique_maximum": len(winners) == 1,
                "inferred_right_block": (
                    f"B{inferred_block}" if inferred_block is not None else None
                ),
            }
        )
    inferred_pairing = tuple(inferred)
    return {
        "method": (
            "Infer the mouth map from the full encoded-resource state by choosing, for each left "
            "mouth L_i, the unique right encoded block B_j with maximal I(L_i:B_j)."
        ),
        "inferred_pairing": inferred_pairing,
        "pairing_rows": tuple(rows),
        "unique_permutation_inferred": len(inferred_pairing) == resource.m
        and sorted(inferred_pairing) == list(range(resource.m))
        and all(row["unique_maximum"] for row in rows),
        "uses_declared_pairing_as_decoder_input": False,
        "visibility_boundary": (
            "This is not a low-order physical entropy probe; it uses full encoded-block access "
            "to the resource state."
        ),
    }


def _keep_projector() -> Matrix:
    return matrix(((1, 0, 0), (0, 1, 0), (0, 0, 0)))


def screen_success_probability_from_channel(kraus: Sequence[Matrix]) -> float:
    """Read erasure success probability from the screen channel itself."""
    projector = _keep_projector()
    input_dimension = len(kraus[0][0])
    total = 0j
    for item in kraus:
        total += trace(matmul(matmul(dagger(item), projector), item))
    value = total / input_dimension
    if abs(value.imag) > 1e-10:
        raise ValueError("screen keep probability should be real")
    return float(value.real)


def _screen_record(north_probability: float, *, screen: str) -> dict[str, object]:
    screen_kraus = coherent_bilayer_screen_kraus(north_probability, screen=screen)
    success_probability = screen_success_probability_from_channel(screen_kraus)
    recovered_kraus = recovered_coherent_bilayer_screen_kraus(
        north_probability,
        screen=screen,
    )
    entanglement_fidelity = entanglement_fidelity_to_unitary(
        recovered_kraus,
        identity_matrix(2),
    )
    return {
        "screen": screen,
        "state_derived_success_probability": success_probability,
        "screen_entropy_bits": binary_entropy(success_probability)
        + success_probability,
        "trace_preserving_error": trace_preserving_error(screen_kraus),
        "recovered_trace_preserving_error": trace_preserving_error(recovered_kraus),
        "recovered_choi_trace": float(trace(choi_matrix(recovered_kraus)).real),
        "recovery_entanglement_fidelity": entanglement_fidelity,
        "average_recovery_fidelity": average_gate_fidelity(entanglement_fidelity, 2),
        "unassisted_quantum_capacity_qubits_per_use": max(
            0.0,
            2.0 * success_probability - 1.0,
        ),
    }


def state_derived_screen_transition_certificate(
    probabilities: Sequence[float] = (0.0, 0.25, 0.5, 0.75, 1.0),
) -> dict[str, object]:
    records = []
    for source_probability in probabilities:
        north = _screen_record(source_probability, screen="north")
        south = _screen_record(source_probability, screen="south")
        north_fidelity = north["recovery_entanglement_fidelity"]
        south_fidelity = south["recovery_entanglement_fidelity"]
        north_area = north["screen_entropy_bits"]
        south_area = south["screen_entropy_bits"]
        records.append(
            {
                "source_circuit_parameter_not_used_by_decoder": source_probability,
                "state_derived_north_success_probability": north[
                    "state_derived_success_probability"
                ],
                "state_derived_south_success_probability": south[
                    "state_derived_success_probability"
                ],
                "north_screen": north,
                "south_screen": south,
                "recovery_winner": (
                    "north"
                    if north_fidelity > south_fidelity
                    else "south"
                    if south_fidelity > north_fidelity
                    else "tie"
                ),
                "larger_entropy_area_analogue": (
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
        )
    midpoint = next(
        (
            row
            for row in records
            if isclose(row["state_derived_north_success_probability"], 0.5)
        ),
        None,
    )
    return {
        "method": (
            "The screen success probabilities are read from the output screen channels induced by "
            "one coherent routing isometry. Recovery fidelities and screen entropy/area analogues "
            "are then computed from those same channels."
        ),
        "records": tuple(records),
        "all_probabilities_recovered_from_channels": all(
            isclose(
                row["state_derived_north_success_probability"],
                row["source_circuit_parameter_not_used_by_decoder"],
                abs_tol=1e-12,
            )
            and isclose(
                row["state_derived_south_success_probability"],
                1.0 - row["source_circuit_parameter_not_used_by_decoder"],
                abs_tol=1e-12,
            )
            for row in records
        ),
        "recovery_and_area_winners_match": all(
            row["recovery_minus_area_signs_match"] for row in records
        ),
        "midpoint_transition_from_state": midpoint is not None
        and midpoint["recovery_winner"] == "tie"
        and midpoint["larger_entropy_area_analogue"] == "tie",
        "exact_identity": (
            "With equal bare screen areas, both the recovery fidelity difference and the "
            "entropy/area-analogue difference are positive multiples of 2p-1, where p is "
            "the success probability inferred from the north screen channel."
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
            "A bare-area bias not encoded in the state/channel data shifts the area crossing "
            "without shifting the recovery crossing. Goal 14 therefore cannot remove inserted "
            "geometry by appending an external area term after the channel is fixed."
        ),
    }


def _capacity_profile(values: tuple[int, ...]) -> dict[int, int]:
    profile: dict[int, int] = {}
    for value in values:
        profile[value] = profile.get(value, 0) + 1
    return dict(sorted(profile.items()))


def _bounded_state_derived_atlas(*, max_mouths: int) -> tuple[dict[str, object], ...]:
    records = []
    for mouths in range(1, max_mouths + 1):
        resources = tuple(
            EncodedMouthBridgeModel(
                name=f"state_derived_resource_{pairing}",
                pairing=pairing,
            )
            for pairing in permutations(range(mouths))
        )
        identity_protocol = _protocol(
            name="identity_activation",
            kind="clifford_bridge_activation",
            mouths=mouths,
            activation=_identity(mouths),
        )
        scrambler = _protocol(
            name="mouth_blind_pauli_twirled_scrambler",
            kind="mouth_blind_pauli_twirled_scrambler",
            mouths=mouths,
            activation=None,
        )
        coarse_shadows = {
            repr(resource.coarse_entropy_mincut_shadow()) for resource in resources
        }
        low_order_profiles = {
            repr(resource.physical_low_order_entropy_profile(resource.block_distance))
            for resource in resources
        }
        inferred_pairings = tuple(state_derived_pairing(resource) for resource in resources)
        identity_capacities = tuple(
            BridgeChannelControlRun(resource, identity_protocol).structured_transfer_capacity()
            for resource in resources
        )
        derived_capacities = tuple(
            BridgeChannelControlRun(
                resource,
                _protocol(
                    name="state_derived_activation",
                    kind="clifford_bridge_activation",
                    mouths=mouths,
                    activation=state_derived_pairing(resource),
                ),
            ).structured_transfer_capacity()
            for resource in resources
        )
        scrambler_capacities = tuple(
            BridgeChannelControlRun(resource, scrambler).structured_transfer_capacity()
            for resource in resources
        )
        records.append(
            {
                "m": mouths,
                "resources_checked": len(resources),
                "coarse_shadow_classes": len(coarse_shadows),
                "low_order_physical_entropy_profile_classes_through_distance": len(
                    low_order_profiles
                ),
                "all_pairings_recovered_from_state": tuple(
                    resource.pairing == inferred
                    for resource, inferred in zip(resources, inferred_pairings, strict=True)
                ).count(False)
                == 0,
                "identity_activation_capacity_profile": _capacity_profile(
                    identity_capacities
                ),
                "state_derived_activation_capacity_profile": _capacity_profile(
                    derived_capacities
                ),
                "mouth_blind_scrambling_capacity_profile": _capacity_profile(
                    scrambler_capacities
                ),
                "entropy_matched_identity_transfer_varies": len(low_order_profiles) == 1
                and len(set(identity_capacities)) > 1,
                "state_derived_activation_full_capacity": set(derived_capacities)
                == {mouths},
                "mouth_blind_scrambler_zero_structured_capacity": set(
                    scrambler_capacities
                )
                == {0},
            }
        )
    return tuple(records)


def goal14_state_derived_bridge_dynamics_certificate(
    *,
    mouths: int = 2,
    low_order: int = 3,
    atlas_max_mouths: int = 3,
) -> dict[str, object]:
    if mouths < 2:
        raise ValueError("mouths must be at least two for the representative split")
    if mouths > 3 or atlas_max_mouths > 3:
        raise ValueError("dense channel checks are limited to at most three mouths")
    if atlas_max_mouths < mouths:
        raise ValueError("atlas_max_mouths must be at least mouths")

    aligned = EncodedMouthBridgeModel(
        name="aligned_state_resource",
        pairing=_identity(mouths),
    )
    twisted = EncodedMouthBridgeModel(
        name="twisted_state_resource",
        pairing=_swap_first_two(mouths),
    )
    inferred_record = state_derived_pairing_record(twisted)
    inferred_pairing = inferred_record["inferred_pairing"]
    if not isinstance(inferred_pairing, tuple):
        raise ValueError("state-derived pairing record is malformed")

    identity_protocol = _protocol(
        name="identity_activation",
        kind="clifford_bridge_activation",
        mouths=mouths,
        activation=_identity(mouths),
    )
    state_derived_protocol = _protocol(
        name="state_derived_activation",
        kind="clifford_bridge_activation",
        mouths=mouths,
        activation=inferred_pairing,
    )
    state_derived_t_protocol = _protocol(
        name="state_derived_T_dressed_activation",
        kind="non_clifford_t_dressed_activation",
        mouths=mouths,
        activation=inferred_pairing,
    )
    scrambler_protocol = _protocol(
        name="mouth_blind_pauli_twirled_scrambler",
        kind="mouth_blind_pauli_twirled_scrambler",
        mouths=mouths,
        activation=None,
    )

    aligned_identity = BridgeChannelControlRun(aligned, identity_protocol)
    twisted_identity = BridgeChannelControlRun(twisted, identity_protocol)
    twisted_state_derived = BridgeChannelControlRun(twisted, state_derived_protocol)
    twisted_state_derived_t = BridgeChannelControlRun(twisted, state_derived_t_protocol)
    twisted_scrambler = BridgeChannelControlRun(twisted, scrambler_protocol)

    low_order_audit = _compare_low_order(aligned, twisted, max_order=low_order)
    first_mismatch = _first_entropy_mismatch_order(
        aligned,
        twisted,
        max_order=twisted.block_distance + 1,
    )
    explicit_channels = {
        "identity_activation_on_twisted_state": teleportation_channel_certificate(
            twisted.pairing,
            _identity(mouths),
        ),
        "state_derived_activation_on_twisted_state": teleportation_channel_certificate(
            twisted.pairing,
            inferred_pairing,
        ),
    }
    screen_transition = state_derived_screen_transition_certificate()
    area_bias = _external_area_bias_no_go()
    atlas = _bounded_state_derived_atlas(max_mouths=atlas_max_mouths)
    first_atlas_split = next(
        (
            record
            for record in atlas
            if record["entropy_matched_identity_transfer_varies"]
        ),
        None,
    )

    certified_claims = {
        "state_derived_pairing_inferred_from_resource_state": inferred_pairing
        == twisted.pairing
        and inferred_record["unique_permutation_inferred"] is True,
        "coarse_entropy_mincut_shadows_match": aligned.coarse_entropy_mincut_shadow()
        == twisted.coarse_entropy_mincut_shadow(),
        "low_order_entropy_blind_to_mouth_map": bool(
            low_order_audit["labeled_tables_match"]
        )
        and low_order >= twisted.block_distance,
        "first_entropy_mismatch_at_decoder_scale": first_mismatch is not None
        and first_mismatch["order"] == twisted.block_distance + 1,
        "wrong_mouth_identity_activation_fails": twisted_identity.structured_transfer_capacity()
        == mouths - 2,
        "state_derived_activation_restores_transfer": twisted_state_derived.structured_transfer_capacity()
        == mouths,
        "state_derived_non_clifford_activation_preserves_transfer": twisted_state_derived_t.structured_transfer_capacity()
        == mouths,
        "mouth_blind_scrambling_control_fails": twisted_scrambler.structured_transfer_capacity()
        == 0,
        "explicit_channels_are_trace_preserving": max(
            explicit_channels["identity_activation_on_twisted_state"][
                "trace_preserving_error"
            ],
            explicit_channels["state_derived_activation_on_twisted_state"][
                "trace_preserving_error"
            ],
        )
        < 1e-12,
        "state_derived_channel_is_exact_identity": explicit_channels[
            "state_derived_activation_on_twisted_state"
        ]["fidelity"]["entanglement_fidelity_to_identity"]
        == 1.0,
        "screen_probabilities_derived_from_channels": screen_transition[
            "all_probabilities_recovered_from_channels"
        ],
        "recovery_area_transition_mutually_derived": screen_transition[
            "recovery_and_area_winners_match"
        ]
        and screen_transition["midpoint_transition_from_state"],
        "external_area_bias_no_go_recorded": area_bias["transitions_match"] is False,
        "bounded_atlas_state_derives_all_pairings": all(
            record["all_pairings_recovered_from_state"] for record in atlas
        ),
        "bounded_atlas_state_derived_activation_full_capacity": all(
            record["state_derived_activation_full_capacity"] for record in atlas
        ),
        "bounded_atlas_entropy_matched_identity_transfer_varies": first_atlas_split
        is not None
        and first_atlas_split["m"] == 2,
        "bounded_atlas_mouth_blind_scramblers_zero_capacity": all(
            record["mouth_blind_scrambler_zero_structured_capacity"]
            for record in atlas
        ),
        "no_continuum_er_epr_or_de_sitter_claim": True,
    }
    certified_claims["goal14_state_derived_bridge_dynamics_certificate"] = all(
        certified_claims.values()
    )

    return {
        "goal": "Goal 14: State-Derived Bridge Dynamics",
        "status": (
            "pass"
            if certified_claims["goal14_state_derived_bridge_dynamics_certificate"]
            else "fail"
        ),
        "scope": {
            "family": (
                "encoded-mouth stabilizer resources plus a coherent two-screen routing "
                "isometry; all diagnostics read bridge pairing or screen probability from "
                "the finite state/channel data"
            ),
            "mouths": mouths,
            "low_order": low_order,
            "atlas_max_mouths": atlas_max_mouths,
            "right_block_code": "[[5,1,3]] five-qubit perfect stabilizer code",
        },
        "theorem_style_result": {
            "name": "State-Derived Finite Bridge-Dynamics Theorem",
            "claim": (
                "In the encoded-mouth family, the full encoded resource state determines the "
                "logical mouth map by block mutual information, while low-order physical entropy "
                "through the code distance remains blind to that map. Activating the state-derived "
                "mouth map restores exact transfer; identity/wrong-mouth and mouth-blind scrambling "
                "controls fail. In the same finite circuit layer, screen success probabilities read "
                "from the coherent routing channels determine both recovery ordering and the equal-area "
                "entropy/area analogue transition."
            ),
            "proof_sketch": (
                "The only pairing-dependent stabilizers are logical Bell checks between L_i and "
                "the encoded block B_pi(i), so full block mutual information has a unique maximum "
                "at B_pi(i), while regions of size at most d cannot see the pairing. Bell-transfer "
                "Kraus certificates show that routing by the inferred map gives the identity channel, "
                "whereas identity routing on the twisted state is a wrong-mouth channel. For the "
                "two-screen coherent isometry, the keep probability is obtained from the induced "
                "screen channel; the recovery-fidelity and entropy/area differences are positive "
                "multiples of the same derived quantity 2p-1."
            ),
        },
        "representative_witness": {
            "aligned_resource": aligned.certificate_record(),
            "twisted_resource": twisted.certificate_record(),
            "state_derived_pairing": inferred_record,
            "comparisons": {
                "coarse_entropy_mincut_match": aligned.coarse_entropy_mincut_shadow()
                == twisted.coarse_entropy_mincut_shadow(),
                "low_order_physical_entropy_audit": low_order_audit,
                "first_entropy_mismatch": first_mismatch,
                "identity_activation_capacity": {
                    "aligned": aligned_identity.structured_transfer_capacity(),
                    "twisted": twisted_identity.structured_transfer_capacity(),
                },
                "state_derived_activation_capacity": {
                    "twisted_clifford": twisted_state_derived.structured_transfer_capacity(),
                    "twisted_non_clifford_T": twisted_state_derived_t.structured_transfer_capacity(),
                },
                "mouth_blind_scrambling_capacity": {
                    "twisted": twisted_scrambler.structured_transfer_capacity(),
                },
            },
            "transfer_diagnostics": {
                "twisted_identity_wrong_mouth": twisted_identity.diagnostics(),
                "twisted_state_derived_clifford": twisted_state_derived.diagnostics(),
                "twisted_state_derived_non_clifford_T": twisted_state_derived_t.diagnostics(),
                "twisted_mouth_blind_scrambler": twisted_scrambler.diagnostics(),
            },
            "explicit_channel_certificates": explicit_channels,
        },
        "state_derived_screen_transition": screen_transition,
        "external_area_bias_no_go": area_bias,
        "bounded_atlas": {
            "records": atlas,
            "first_entropy_matched_identity_transfer_split": first_atlas_split,
        },
        "diagnostic_interpretation": {
            "entropy_mincut_visible": (
                "Coarse entropy/min-cut and low-order physical entropy through the code distance "
                "remain insufficient for the encoded mouth map."
            ),
            "state_visible": (
                "Full encoded-block mutual information in the state determines the mouth map without "
                "handing the decoder the declared pairing."
            ),
            "channel_visible": (
                "Explicit teleportation Choi/Kraus data separate state-derived, wrong-mouth, T-dressed, "
                "and mouth-blind controls."
            ),
            "area_recovery_visible": (
                "The screen transition uses success probabilities inferred from the screen channels; "
                "the equal-area entropy analogue is computed from the same probabilities."
            ),
        },
        "limitations": (
            "This is a finite stabilizer/QEC and small dense-channel certificate. The resource family "
            "still supplies a finite state/circuit ansatz, the full block mutual-information probe is "
            "decoder-scale data, and the screen area term is only state-derived in the equal-bare-area "
            "analogue. The certificate does not prove continuum ER=EPR, de Sitter physics, dS/CFT, or "
            "chaotic many-body traversability."
        ),
        "reproducibility": {
            "goal14_certificate": (
                f"PYTHONPATH=. python3 -m qgtoy state-bridge-dynamics --mouths {mouths} "
                f"--low-order {low_order} --atlas-max-mouths {atlas_max_mouths}"
            ),
            "focused_regression": (
                "PYTHONPATH=. python3 -m unittest tests.test_state_bridge"
            ),
        },
        "certified_claims": certified_claims,
    }
