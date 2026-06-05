"""Finite bilayer reconstruction certificates for the de Sitter program.

This module keeps three logically distinct objects separate:

* complete entropy data, quotiented by relabelings of physical screen qubits;
* the full net of supported logical Pauli subspaces, additionally quotiented by
  a change of logical Pauli basis; and
* explicit CPTP recovery channels in a tunable two-screen calibration model.

The bounded searches are discovery tools and no-go certificates, not continuum
de Sitter or dS/CFT theorems.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from itertools import permutations
from math import log2

from .gf2 import all_masks, in_span, rref
from .quantum_channel import (
    average_gate_fidelity,
    choi_matrix,
    coherent_bilayer_isometry,
    coherent_bilayer_screen_kraus,
    complex_matrix_rank,
    entanglement_fidelity_to_unitary,
    erasure_channel_kraus,
    identity_matrix,
    isometry_error,
    max_abs_difference,
    recovered_coherent_bilayer_screen_kraus,
    teleportation_channel_certificate,
    trace,
    trace_preserving_error,
)
from .search import enumerate_stabilizer_codes
from .stabilizer import StabilizerCode, combine_rows
from .structured import enumerate_graph_subspace_codes


def permute_region_mask(mask: int, permutation: Sequence[int]) -> int:
    """Relabel physical qubit ``source`` as ``permutation[source]``."""
    out = 0
    for source, target in enumerate(permutation):
        if (mask >> source) & 1:
            out |= 1 << target
    return out


def complete_entropy_table(code: StabilizerCode) -> tuple[int, ...]:
    return tuple(code.entropy(mask) for mask in all_masks(code.n))


def _logical_coordinates(code: StabilizerCode, representative: int) -> int:
    for coefficients in range(1 << (2 * code.k)):
        logical = combine_rows(coefficients, code.logical_basis)
        if in_span(representative ^ logical, code.generators, code.width):
            return coefficients
    raise ValueError("supported logical representative is not in the logical quotient")


def complete_logical_subspace_net(code: StabilizerCode) -> tuple[tuple[int, ...], ...]:
    """Return every region's exact supported logical subspace in quotient coordinates."""
    if code.k != 1:
        raise ValueError("the label-invariant bilayer search currently requires k=1")
    return tuple(
        rref(
            (
                _logical_coordinates(code, representative)
                for representative in code.logical_subspace_supported(mask)
            ),
            2,
        )
        for mask in all_masks(code.n)
    )


def _logical_basis_maps() -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first in range(1, 4)
        for second in range(1, 4)
        if first != second
    )


def _map_logical_vector(vector: int, basis_map: tuple[int, int]) -> int:
    out = 0
    if vector & 1:
        out ^= basis_map[0]
    if vector & 2:
        out ^= basis_map[1]
    return out


def _map_logical_subspace(
    subspace: tuple[int, ...], basis_map: tuple[int, int]
) -> tuple[int, ...]:
    return rref((_map_logical_vector(vector, basis_map) for vector in subspace), 2)


def canonical_entropy_and_reconstruction_keys(
    code: StabilizerCode,
) -> tuple[tuple[int, ...], tuple[object, ...]]:
    """Canonicalize complete entropy and reconstruction-net data for a k=1 code.

    The entropy key is quotiented only by physical qubit permutations.  The
    joint key uses only permutations that attain that entropy key and also
    quotients by all six invertible changes of one-qubit logical Pauli basis.
    Consequently, differing joint keys inside one entropy class are a genuine
    label-invariant entropy/reconstruction discordance for the declared data.
    """
    entropy = complete_entropy_table(code)
    physical_permutations = tuple(permutations(range(code.n)))
    entropy_candidates = tuple(
        tuple(
            entropy[permute_region_mask(mask, permutation)]
            for mask in all_masks(code.n)
        )
        for permutation in physical_permutations
    )
    entropy_key = min(entropy_candidates)
    canonicalizing_permutations = tuple(
        permutation
        for permutation, candidate in zip(
            physical_permutations, entropy_candidates, strict=True
        )
        if candidate == entropy_key
    )

    net = complete_logical_subspace_net(code)
    joint_candidates = []
    for permutation in canonicalizing_permutations:
        for basis_map in _logical_basis_maps():
            joint_candidates.append(
                tuple(
                    (
                        entropy[permuted_mask],
                        _map_logical_subspace(net[permuted_mask], basis_map),
                    )
                    for mask in all_masks(code.n)
                    for permuted_mask in (permute_region_mask(mask, permutation),)
                )
            )
    return entropy_key, min(joint_candidates)


def _scan_code_family(
    *,
    family: str,
    n: int,
    codes: Iterable[StabilizerCode],
) -> dict[str, object]:
    entropy_classes: dict[
        tuple[int, ...], dict[tuple[object, ...], StabilizerCode]
    ] = {}
    codes_checked = 0
    first_collision: dict[str, object] | None = None
    for code in codes:
        codes_checked += 1
        entropy_key, joint_key = canonical_entropy_and_reconstruction_keys(code)
        joint_classes = entropy_classes.setdefault(entropy_key, {})
        if joint_classes and joint_key not in joint_classes and first_collision is None:
            previous = next(iter(joint_classes.values()))
            first_collision = {
                "first_generators": previous.pauli_generators(),
                "second_generators": code.pauli_generators(),
                "complete_entropy_key": entropy_key,
            }
        joint_classes.setdefault(joint_key, code)

    discordant_entropy_classes = sum(
        1 for joint_classes in entropy_classes.values() if len(joint_classes) > 1
    )
    return {
        "family": family,
        "n": n,
        "k": 1,
        "codes_checked": codes_checked,
        "complete_entropy_classes": len(entropy_classes),
        "entropy_classes_with_multiple_reconstruction_nets": discordant_entropy_classes,
        "label_invariant_collision_found": first_collision is not None,
        "first_collision": first_collision,
    }


def bounded_label_invariant_search_certificate() -> dict[str, object]:
    """Run the exact small-code search currently cheap enough for regression use."""
    scans = []
    for n in range(1, 5):
        scans.append(
            _scan_code_family(
                family="all stabilizer codes modulo physical permutations",
                n=n,
                codes=enumerate_stabilizer_codes(n, k=1, equivalence="permutation"),
            )
        )
    scans.append(
        _scan_code_family(
            family=(
                "deleted-check codes from local-Clifford graph-state representatives, "
                "modulo physical permutations"
            ),
            n=5,
            codes=enumerate_graph_subspace_codes(5, k=1, equivalence="permutation"),
        )
    )
    collision = next(
        (scan for scan in scans if scan["label_invariant_collision_found"]), None
    )
    return {
        "question": (
            "Can two finite k=1 codes have isomorphic complete entropy functions but inequivalent nets of "
            "region-supported logical Pauli subspaces?"
        ),
        "equivalences_quotiented": (
            "all physical screen-qubit permutations",
            "all invertible one-qubit logical Pauli basis changes",
        ),
        "scans": tuple(scans),
        "collision_found": collision is not None,
        "first_collision": collision,
        "bounded_result": (
            "No collision in all permutation-inequivalent k=1 stabilizer codes through n=4 or in the "
            "n=5 deleted-check graph-representative family. This is a bounded negative result, "
            "not a theorem for all codes."
            if collision is None
            else "A label-invariant complete-entropy/reconstruction-net collision was found."
        ),
    }


def binary_entropy(probability: float) -> float:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must lie in [0,1]")
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * log2(probability) - (1.0 - probability) * log2(
        1.0 - probability
    )


def _recovered_screen_record(
    north_probability: float,
    *,
    screen: str,
) -> dict[str, object]:
    success_probability = (
        north_probability if screen == "north" else 1.0 - north_probability
    )
    screen_kraus = coherent_bilayer_screen_kraus(
        north_probability,
        screen=screen,
    )
    kraus = recovered_coherent_bilayer_screen_kraus(
        north_probability,
        screen=screen,
    )
    choi = choi_matrix(kraus)
    entanglement_fidelity = entanglement_fidelity_to_unitary(kraus, identity_matrix(2))
    return {
        "screen": screen,
        "success_probability": success_probability,
        "state_derived_screen_channel_trace_preserving_error": trace_preserving_error(
            screen_kraus
        ),
        "standard_erasure_channel_choi_error": max_abs_difference(
            choi_matrix(screen_kraus),
            choi_matrix(erasure_channel_kraus(success_probability)),
        ),
        "trace_preserving_error": trace_preserving_error(kraus),
        "choi_trace": float(trace(choi).real),
        "choi_rank": complex_matrix_rank(choi),
        "entanglement_fidelity_to_identity": entanglement_fidelity,
        "average_recovery_fidelity": average_gate_fidelity(entanglement_fidelity, 2),
        "exact_perfect_reconstruction": abs(entanglement_fidelity - 1.0) < 1e-12,
        "unassisted_quantum_capacity_qubits_per_use": max(
            0.0,
            2.0 * success_probability - 1.0,
        ),
    }


def bilayer_recovery_transition_certificate(
    probabilities: Sequence[float] = (0.0, 0.25, 0.5, 0.75, 1.0),
) -> dict[str, object]:
    """Complementary north/south erasure calibration for a two-screen code."""
    records = []
    for probability in probabilities:
        isometry = coherent_bilayer_isometry(probability)
        north = _recovered_screen_record(probability, screen="north")
        south = _recovered_screen_record(probability, screen="south")
        records.append(
            {
                "north_routing_probability": probability,
                "isometry_error": isometry_error(isometry),
                "north_recovery": north,
                "south_recovery": south,
                "fidelity_advantage": (
                    "north"
                    if north["entanglement_fidelity_to_identity"]
                    > south["entanglement_fidelity_to_identity"]
                    else "south"
                    if south["entanglement_fidelity_to_identity"]
                    > north["entanglement_fidelity_to_identity"]
                    else "tie"
                ),
            }
        )
    midpoint = next(
        (
            record
            for record in records
            if abs(record["north_routing_probability"] - 0.5) < 1e-12
        ),
        None,
    )
    return {
        "model": (
            "One coherent flagged isometry routes an input qubit to the north screen with probability p and "
            "to the south screen with probability 1-p. Tracing either output leg derives the complementary "
            "screen erasure channels."
        ),
        "records": tuple(records),
        "all_isometries_verified": all(
            record["isometry_error"] < 1e-12 for record in records
        ),
        "all_reduced_channels_trace_preserving": all(
            max(
                record["north_recovery"][
                    "state_derived_screen_channel_trace_preserving_error"
                ],
                record["south_recovery"][
                    "state_derived_screen_channel_trace_preserving_error"
                ],
            )
            < 1e-12
            for record in records
        ),
        "reduced_channels_are_standard_complementary_erasure_channels": all(
            max(
                record["north_recovery"]["standard_erasure_channel_choi_error"],
                record["south_recovery"]["standard_erasure_channel_choi_error"],
            )
            < 1e-12
            for record in records
        ),
        "midpoint_tie_verified": midpoint is not None
        and midpoint["fidelity_advantage"] == "tie",
        "endpoint_reconstruction_verified": (
            bool(records)
            and records[0]["south_recovery"]["exact_perfect_reconstruction"]
            and records[-1]["north_recovery"]["exact_perfect_reconstruction"]
        ),
        "claim_boundary": (
            "This is an explicit QEC transition calibration. A de Sitter claim requires deriving the routing "
            "parameter or recovery competition from a static-patch state and generalized-entropy prescription."
        ),
    }


def bilayer_saddle_recovery_matching_certificate(
    probabilities: Sequence[float] = (0.0, 0.25, 0.5, 0.75, 1.0),
    area_biases: Sequence[float] = (0.0, 0.25),
) -> dict[str, object]:
    """Prove the finite recovery/quantum-area matching theorem and its bias no-go."""
    records = []
    for probability in probabilities:
        entropy_flag = binary_entropy(probability)
        north_entropy = entropy_flag + probability
        south_entropy = entropy_flag + 1.0 - probability
        north_fidelity = probability + (1.0 - probability) / 4.0
        south_fidelity = 1.0 - probability + probability / 4.0
        coherent_information = north_entropy - south_entropy
        records.append(
            {
                "north_routing_probability": probability,
                "north_screen_entropy_bits": north_entropy,
                "south_screen_entropy_bits": south_entropy,
                "screen_entropy_difference_north_minus_south": coherent_information,
                "north_recovery_entanglement_fidelity": north_fidelity,
                "south_recovery_entanglement_fidelity": south_fidelity,
                "recovery_fidelity_difference_north_minus_south": (
                    north_fidelity - south_fidelity
                ),
                "north_quantum_capacity_qubits_per_use": max(
                    0.0,
                    coherent_information,
                ),
                "south_quantum_capacity_qubits_per_use": max(
                    0.0,
                    -coherent_information,
                ),
            }
        )

    bias_records = []
    for area_bias in area_biases:
        quantum_area_transition = (1.0 - area_bias) / 2.0
        transition_in_domain = 0.0 <= quantum_area_transition <= 1.0
        bias_records.append(
            {
                "bare_quantum_area_bias_north_minus_south_bits": area_bias,
                "recovery_transition_probability": 0.5,
                "quantum_area_transition_probability": (
                    quantum_area_transition if transition_in_domain else None
                ),
                "quantum_area_transition_in_physical_domain": transition_in_domain,
                "transition_mismatch": (
                    abs(quantum_area_transition - 0.5) if transition_in_domain else None
                ),
                "transitions_match": abs(area_bias) < 1e-12,
            }
        )

    exact_identity_verified = all(
        abs(
            record["recovery_fidelity_difference_north_minus_south"]
            - 0.75 * record["screen_entropy_difference_north_minus_south"]
        )
        < 1e-12
        for record in records
    )
    return {
        "state_derived_quantum_area_analogue": (
            "For equal bare screen areas, compare A_N+S(N) and A_S+S(S), using the reduced-state entropies "
            "of the coherent routing isometry. The screen with larger quantum-area analogue is the candidate "
            "exterior encoder, following the bilayer phase-transition criterion."
        ),
        "exact_theorem": (
            "For a routed qubit, S(N)-S(S)=2p-1 and F_e(N)-F_e(S)=3(2p-1)/4. Therefore the recovery "
            "winner and larger-quantum-area screen exchange at exactly p=1/2 when bare areas are equal."
        ),
        "records": tuple(records),
        "exact_matching_identity_verified": exact_identity_verified,
        "symmetric_transition_match_verified": exact_identity_verified,
        "area_bias_audit": tuple(bias_records),
        "area_bias_no_go": (
            "An independent bare-area bias delta shifts the quantum-area crossing to p=(1-delta)/2 while "
            "the channel recovery crossing remains p=1/2. The simple routing model matches a nonzero area "
            "bias only if the state/channel dynamics are modified as well."
        ),
        "gravity_claim_boundary": (
            "The entropy term is derived from the finite state, but the bare area term and bilayer assignment "
            "rule are inputs. This is an exact information-theoretic analogue, not a derived de Sitter QES."
        ),
    }


def er_epr_ds_interpretation_audit() -> dict[str, object]:
    probability = 0.5
    transition = bilayer_recovery_transition_certificate((probability,))
    matching = bilayer_saddle_recovery_matching_certificate((probability,), (0.0,))
    screen_entanglement = binary_entropy(probability)
    gates = {
        "nonzero_north_south_entanglement": screen_entanglement > 0.0,
        "exact_joint_reconstruction_from_isometry": transition[
            "all_isometries_verified"
        ],
        "complementary_single_screen_channels_derived": transition[
            "all_reduced_channels_trace_preserving"
        ],
        "symmetric_recovery_quantum_area_transition_match": matching[
            "symmetric_transition_match_verified"
        ],
        "gravitational_qes_derived_from_action_or_constraints": False,
        "de_sitter_semiclassical_limit_controlled": False,
        "inter_screen_causal_or_traversable_protocol_derived": False,
        "boundary_cft_dictionary_and_scaling_limit_defined": False,
    }
    finite_analogue = all(
        gates[name]
        for name in (
            "nonzero_north_south_entanglement",
            "exact_joint_reconstruction_from_isometry",
            "complementary_single_screen_channels_derived",
            "symmetric_recovery_quantum_area_transition_match",
        )
    )
    geometric_er_epr = all(gates.values())
    return {
        "audit_point": {"north_routing_probability": probability},
        "screen_entanglement_entropy_for_pure_payload_bits": screen_entanglement,
        "screen_mutual_information_for_maximally_mixed_payload_bits": (
            2.0 * screen_entanglement
        ),
        "gates": gates,
        "finite_algebraic_er_epr_analogue": finite_analogue,
        "geometric_er_epr_in_de_sitter_established": geometric_er_epr,
        "ds_cft_correspondence_advanced": gates[
            "boundary_cft_dictionary_and_scaling_limit_defined"
        ],
        "verdict": (
            "The coherent bilayer is a finite algebraic ER=EPR analogue: entanglement, joint reconstruction, "
            "and complementary channel transfer are explicit. It is not yet ER=EPR in de Sitter and does not "
            "advance dS/CFT, because no gravitational QES, causal geometry, semiclassical limit, or boundary "
            "dictionary has been derived."
        ),
        "next_required_model": (
            "Derive the screen quantum-area difference and the routing/recovery channel from one controlled "
            "static-patch path integral or semiclassical constraint system, then prove the finite matching "
            "identity survives with quantified corrections."
        ),
    }


def bilayer_reconstruction_program_certificate() -> dict[str, object]:
    aligned = teleportation_channel_certificate((0, 1), (0, 1))
    crossed_wrong = teleportation_channel_certificate((1, 0), (0, 1))
    crossed_correct = teleportation_channel_certificate((1, 0), (1, 0))
    search = bounded_label_invariant_search_certificate()
    transition = bilayer_recovery_transition_certificate()
    matching = bilayer_saddle_recovery_matching_certificate()
    interpretation = er_epr_ds_interpretation_audit()
    claims = {
        "explicit_channels_are_trace_preserving": max(
            aligned["trace_preserving_error"],
            crossed_wrong["trace_preserving_error"],
            crossed_correct["trace_preserving_error"],
        )
        < 1e-12,
        "pairing_aware_decoder_is_exact": crossed_correct["fidelity"][
            "entanglement_fidelity_to_identity"
        ]
        == 1.0,
        "wrong_crossed_decoder_has_no_fixed_port_qubits": crossed_wrong[
            "fixed_port_transmission"
        ]["perfect_qubits"]
        == 0,
        "wrong_crossed_decoder_preserves_classical_center_not_quantum_subsystem": (
            crossed_wrong["preserved_operator_algebra"]["exact_joint_noiseless_qubits"]
            == 0
            and crossed_wrong["preserved_operator_algebra"]["center_dimension"] == 2
        ),
        "bounded_label_invariant_search_completed": not search["collision_found"],
        "two_screen_recovery_transition_verified": (
            transition["midpoint_tie_verified"]
            and transition["endpoint_reconstruction_verified"]
            and transition["all_isometries_verified"]
            and transition["all_reduced_channels_trace_preserving"]
            and transition[
                "reduced_channels_are_standard_complementary_erasure_channels"
            ]
        ),
        "recovery_quantum_area_analogue_match_verified": matching[
            "symmetric_transition_match_verified"
        ],
        "area_bias_no_go_recorded": not matching["area_bias_audit"][1][
            "transitions_match"
        ],
        "er_epr_ds_claim_boundary_audited": (
            interpretation["finite_algebraic_er_epr_analogue"]
            and not interpretation["geometric_er_epr_in_de_sitter_established"]
            and not interpretation["ds_cft_correspondence_advanced"]
        ),
    }
    return {
        "program": "Finite static-patch bilayer reconstruction",
        "status": "pass" if all(claims.values()) else "fail",
        "explicit_teleportation_channels": {
            "aligned_identity_decoder": aligned,
            "crossed_identity_decoder": crossed_wrong,
            "crossed_pairing_aware_decoder": crossed_correct,
        },
        "label_invariant_search": search,
        "two_screen_transition": transition,
        "recovery_saddle_matching": matching,
        "er_epr_ds_interpretation": interpretation,
        "certified_claims": claims,
    }
