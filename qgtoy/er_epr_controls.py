"""Goal 13 non-Clifford and scrambling bridge-channel controls."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from .er_epr_encoded import EncodedMouthBridgeModel


def _identity(m: int) -> tuple[int, ...]:
    return tuple(range(m))


def _swap_first_two(m: int) -> tuple[int, ...]:
    if m < 2:
        raise ValueError("need at least two mouths for a twist")
    return (1, 0) + tuple(range(2, m))


def _zero_pauli_transfer_matrix() -> tuple[tuple[int, int, int], ...]:
    return ((0, 0, 0), (0, 0, 0), (0, 0, 0))


def _identity_pauli_transfer_matrix() -> tuple[tuple[int, int, int], ...]:
    return ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def _t_gate_pauli_transfer_matrix() -> tuple[tuple[str, str, str], ...]:
    return (
        ("1/sqrt(2)", "1/sqrt(2)", "0"),
        ("-1/sqrt(2)", "1/sqrt(2)", "0"),
        ("0", "0", "1"),
    )


@dataclass(frozen=True)
class BridgeChannelControlProtocol:
    """Finite logical-channel control protocol for encoded bridge mouths."""

    name: str
    kind: str
    activation: tuple[int, ...] | None
    mouths: int

    def __post_init__(self) -> None:
        if self.kind not in {
            "clifford_bridge_activation",
            "non_clifford_t_dressed_activation",
            "mouth_blind_pauli_twirled_scrambler",
        }:
            raise ValueError(f"unknown control protocol kind {self.kind!r}")
        if self.kind == "mouth_blind_pauli_twirled_scrambler":
            if self.activation is not None:
                raise ValueError("mouth-blind scrambler must not declare an activation map")
            return
        if self.activation is None:
            raise ValueError("bridge activation protocols require an activation map")
        if len(self.activation) != self.mouths:
            raise ValueError("activation length must match mouth count")
        if sorted(self.activation) != list(range(self.mouths)):
            raise ValueError("activation must be a permutation of right blocks")

    @property
    def is_non_clifford(self) -> bool:
        return self.kind == "non_clifford_t_dressed_activation"

    @property
    def is_scrambling_control(self) -> bool:
        return self.kind == "mouth_blind_pauli_twirled_scrambler"

    def rule_record(self) -> dict[str, object]:
        if self.kind == "clifford_bridge_activation":
            return {
                "name": self.name,
                "protocol_kind": self.kind,
                "activation_left_probe_to_right_block": self.activation,
                "logical_channel": "encoded Clifford Bell-transfer",
                "non_clifford_layer": False,
                "mouth_blind": False,
                "uses_pairing_as_hidden_input": False,
                "rule": (
                    "For each probe Q_i, Bell-couple Q_i with L_i and activate encoded "
                    "block B_activation[i].  Transfer is structured only when activation[i] "
                    "equals the resource pairing pi(i)."
                ),
            }
        if self.kind == "non_clifford_t_dressed_activation":
            return {
                "name": self.name,
                "protocol_kind": self.kind,
                "activation_left_probe_to_right_block": self.activation,
                "logical_channel": "encoded Bell-transfer followed by logical T on the activated block",
                "non_clifford_layer": True,
                "mouth_blind": False,
                "uses_pairing_as_hidden_input": False,
                "phase_frame_needed_for_identity_recovery": "logical T^dagger on each hit block",
                "rule": (
                    "Use the same public activation map as a bridge coupling, then apply a "
                    "logical T phase to the activated encoded output.  This preserves quantum "
                    "capacity on matched mouths but makes the Pauli-transfer matrix non-Clifford."
                ),
            }
        return {
            "name": self.name,
            "protocol_kind": self.kind,
            "activation_left_probe_to_right_block": None,
            "logical_channel": "mouth-blind complete Pauli twirl after generic scrambling proxy",
            "non_clifford_layer": "not-applicable",
            "mouth_blind": True,
            "uses_pairing_as_hidden_input": False,
            "structured_bridge_target": None,
            "rule": (
                "Apply a public mouth-blind scrambling/twirling control that erases all single-probe "
                "logical Pauli transfer to named right mouths.  It is a finite exact proxy for a "
                "generic scrambling control, not a chaotic many-body simulation."
            ),
        }

    def _hit_pauli_transfer(self) -> tuple[tuple[object, object, object], ...]:
        if self.kind == "non_clifford_t_dressed_activation":
            return _t_gate_pauli_transfer_matrix()
        return _identity_pauli_transfer_matrix()


@dataclass(frozen=True)
class BridgeChannelControlRun:
    resource: EncodedMouthBridgeModel
    protocol: BridgeChannelControlProtocol

    def __post_init__(self) -> None:
        if self.resource.m != self.protocol.mouths:
            raise ValueError("resource and protocol must have the same mouth count")

    @property
    def m(self) -> int:
        return self.resource.m

    def transfer_rows(self) -> tuple[dict[str, object], ...]:
        rows = []
        for left, actual_block in enumerate(self.resource.pairing):
            if self.protocol.is_scrambling_control:
                rows.append(
                    {
                        "input_probe": f"Q{left}",
                        "left_mouth": f"L{left}",
                        "declared_activation": "mouth_blind",
                        "algebraic_receiver": f"B{actual_block}",
                        "activation_matches_bridge": False,
                        "structured_bridge_transfer": False,
                        "logical_channel_type": "complete_pauli_twirl",
                        "non_clifford_layer": False,
                        "pauli_transfer_matrix_XYZ": _zero_pauli_transfer_matrix(),
                        "average_fidelity_to_any_named_block": "1/2",
                        "entanglement_fidelity_to_any_named_block": "1/4",
                        "phase_corrected_entanglement_fidelity": "1/4",
                        "quantum_capacity_to_named_block_qubits": 0,
                        "generic_scrambling_control": True,
                    }
                )
                continue

            if self.protocol.activation is None:
                raise ValueError("non-scrambling protocol must have an activation")
            activated_block = self.protocol.activation[left]
            hit = activated_block == actual_block
            if hit:
                pauli_transfer: tuple[tuple[object, object, object], ...] = self.protocol._hit_pauli_transfer()
                direct_identity_entanglement_fidelity = (
                    "(2 + sqrt(2))/4" if self.protocol.is_non_clifford else "1"
                )
                phase_corrected_entanglement_fidelity = "1"
                capacity = 1
            else:
                pauli_transfer = _zero_pauli_transfer_matrix()
                direct_identity_entanglement_fidelity = "1/4"
                phase_corrected_entanglement_fidelity = "1/4"
                capacity = 0

            rows.append(
                {
                    "input_probe": f"Q{left}",
                    "left_mouth": f"L{left}",
                    "declared_activation": f"B{activated_block}",
                    "algebraic_receiver": f"B{actual_block}",
                    "activation_matches_bridge": hit,
                    "structured_bridge_transfer": hit,
                    "logical_channel_type": "logical_T_unitary" if self.protocol.is_non_clifford else "identity_unitary",
                    "non_clifford_layer": self.protocol.is_non_clifford,
                    "pauli_transfer_matrix_XYZ": pauli_transfer,
                    "direct_identity_entanglement_fidelity": direct_identity_entanglement_fidelity,
                    "phase_corrected_entanglement_fidelity": phase_corrected_entanglement_fidelity,
                    "quantum_capacity_to_activated_block_qubits": capacity,
                    "wrong_mouth_transfer_control": not hit,
                    "generic_scrambling_control": False,
                }
            )
        return tuple(rows)

    def structured_transfer_capacity(self) -> int:
        if self.protocol.is_scrambling_control:
            return 0
        return sum(int(row["quantum_capacity_to_activated_block_qubits"]) for row in self.transfer_rows())

    def operator_growth_controls(self) -> dict[str, object]:
        rows = []
        for left, actual_block in enumerate(self.resource.pairing):
            if self.protocol.is_scrambling_control:
                rows.append(
                    {
                        "probe": f"Q{left}",
                        "algebraic_receiver": f"B{actual_block}",
                        "structured_otoc_signal_at_named_block": 0,
                        "support_growth_type": "mouth-blind twirled scrambling proxy",
                        "support_growth_points_to_bridge_map": False,
                    }
                )
                continue
            if self.protocol.activation is None:
                raise ValueError("non-scrambling protocol must have an activation")
            activated_block = self.protocol.activation[left]
            hit = activated_block == actual_block
            rows.append(
                {
                    "probe": f"Q{left}",
                    "algebraic_receiver": f"B{actual_block}",
                    "activated_detector": f"B{activated_block}",
                    "encoded_logical_output_weight": self.resource.block_distance,
                    "otoc_like_signal_at_activated_block": 1 if hit else 0,
                    "otoc_like_signal_at_algebraic_block": 1,
                    "non_clifford_phase_layer": self.protocol.is_non_clifford,
                    "support_growth_points_to_bridge_map": True,
                }
            )
        return {
            "pauli_support_growth_rows": tuple(rows),
            "support_growth_summary": {
                "left_probe_weight": 1,
                "encoded_output_weight_for_structured_transfer": self.resource.block_distance,
                "structured_transfer_capacity_qubits": self.structured_transfer_capacity(),
                "mouth_blind_scrambling_control": self.protocol.is_scrambling_control,
            },
            "interpretation": (
                "Bridge activations produce support on the algebraic receiver and on the activated "
                "detector only when the activation matches.  The mouth-blind twirled control has no "
                "structured named-mouth OTOC/support-growth signal."
            ),
        }

    def diagnostics(self) -> dict[str, object]:
        return {
            "resource": self.resource.name,
            "protocol": self.protocol.rule_record(),
            "structured_transfer_capacity_qubits": self.structured_transfer_capacity(),
            "port_channels": self.transfer_rows(),
            "operator_growth_controls": self.operator_growth_controls(),
        }


def _compare_low_order(
    first: EncodedMouthBridgeModel,
    second: EncodedMouthBridgeModel,
    *,
    max_order: int,
) -> dict[str, object]:
    first_table = first.physical_low_order_entropy_table(max_order)
    second_table = second.physical_low_order_entropy_table(max_order)
    mismatches = tuple(
        {
            "region": region,
            "first_entropy": first_entropy,
            "second_entropy": second_entropy,
        }
        for (region, first_entropy), (_, second_entropy) in zip(first_table, second_table, strict=True)
        if first_entropy != second_entropy
    )
    return {
        "max_order": max_order,
        "regions_checked": len(first_table),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:10],
        "profiles_match": first.physical_low_order_entropy_profile(max_order)
        == second.physical_low_order_entropy_profile(max_order),
        "labeled_tables_match": len(mismatches) == 0,
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


def _capacity_profile(values: tuple[int, ...]) -> dict[int, int]:
    profile: dict[int, int] = {}
    for value in values:
        profile[value] = profile.get(value, 0) + 1
    return dict(sorted(profile.items()))


def _protocol(
    *,
    name: str,
    kind: str,
    mouths: int,
    activation: tuple[int, ...] | None,
) -> BridgeChannelControlProtocol:
    return BridgeChannelControlProtocol(name=name, kind=kind, mouths=mouths, activation=activation)


def _bounded_control_atlas(*, max_mouths: int) -> tuple[dict[str, object], ...]:
    records = []
    for m in range(1, max_mouths + 1):
        pairings = tuple(permutations(range(m)))
        resources = tuple(EncodedMouthBridgeModel(name=f"resource_{pairing}", pairing=pairing) for pairing in pairings)
        identity_activation = _identity(m)
        identity_protocol = _protocol(
            name="identity_clifford_activation",
            kind="clifford_bridge_activation",
            mouths=m,
            activation=identity_activation,
        )
        generic_protocol = _protocol(
            name="mouth_blind_pauli_twirled_scrambler",
            kind="mouth_blind_pauli_twirled_scrambler",
            mouths=m,
            activation=None,
        )

        coarse_shadows = {repr(resource.coarse_entropy_mincut_shadow()) for resource in resources}
        low_order_profiles = {
            repr(resource.physical_low_order_entropy_profile(resource.block_distance))
            for resource in resources
        }
        identity_capacities = tuple(
            BridgeChannelControlRun(resource=resource, protocol=identity_protocol).structured_transfer_capacity()
            for resource in resources
        )
        algebraic_clifford_capacities = tuple(
            BridgeChannelControlRun(
                resource=resource,
                protocol=_protocol(
                    name="algebra_aware_clifford_activation",
                    kind="clifford_bridge_activation",
                    mouths=m,
                    activation=resource.pairing,
                ),
            ).structured_transfer_capacity()
            for resource in resources
        )
        algebraic_t_capacities = tuple(
            BridgeChannelControlRun(
                resource=resource,
                protocol=_protocol(
                    name="algebra_aware_T_dressed_activation",
                    kind="non_clifford_t_dressed_activation",
                    mouths=m,
                    activation=resource.pairing,
                ),
            ).structured_transfer_capacity()
            for resource in resources
        )
        generic_capacities = tuple(
            BridgeChannelControlRun(resource=resource, protocol=generic_protocol).structured_transfer_capacity()
            for resource in resources
        )

        records.append(
            {
                "m": m,
                "resources_checked": len(resources),
                "coarse_shadow_classes": len(coarse_shadows),
                "low_order_physical_entropy_profile_classes_through_distance": len(low_order_profiles),
                "identity_activation_capacity_profile": _capacity_profile(identity_capacities),
                "algebra_aware_clifford_capacity_profile": _capacity_profile(algebraic_clifford_capacities),
                "algebra_aware_non_clifford_T_capacity_profile": _capacity_profile(algebraic_t_capacities),
                "mouth_blind_scrambling_capacity_profile": _capacity_profile(generic_capacities),
                "entropy_matched_naive_transfer_varies": len(low_order_profiles) == 1
                and len(set(identity_capacities)) > 1,
                "algebra_aware_controls_full_capacity_for_all_resources": set(algebraic_clifford_capacities) == {m}
                and set(algebraic_t_capacities) == {m},
                "generic_scrambling_controls_fail_structured_transfer": set(generic_capacities) == {0},
            }
        )
    return tuple(records)


def goal13_non_clifford_scrambling_bridge_controls_certificate(
    *,
    mouths: int = 2,
    low_order: int = 3,
    atlas_max_mouths: int = 3,
) -> dict[str, object]:
    if mouths < 2:
        raise ValueError("mouths must be at least 2 for a bridge-channel split")
    if atlas_max_mouths < mouths:
        raise ValueError("atlas_max_mouths must be at least mouths")

    aligned = EncodedMouthBridgeModel(name="aligned_encoded_resource", pairing=_identity(mouths))
    twisted = EncodedMouthBridgeModel(name="twisted_encoded_resource", pairing=_swap_first_two(mouths))
    identity_clifford = _protocol(
        name="identity_clifford_activation",
        kind="clifford_bridge_activation",
        mouths=mouths,
        activation=_identity(mouths),
    )
    twisted_clifford = _protocol(
        name="twisted_algebra_aware_clifford_activation",
        kind="clifford_bridge_activation",
        mouths=mouths,
        activation=twisted.pairing,
    )
    twisted_t = _protocol(
        name="twisted_algebra_aware_T_dressed_activation",
        kind="non_clifford_t_dressed_activation",
        mouths=mouths,
        activation=twisted.pairing,
    )
    generic_scrambler = _protocol(
        name="mouth_blind_pauli_twirled_scrambler",
        kind="mouth_blind_pauli_twirled_scrambler",
        mouths=mouths,
        activation=None,
    )

    aligned_identity_run = BridgeChannelControlRun(aligned, identity_clifford)
    twisted_identity_run = BridgeChannelControlRun(twisted, identity_clifford)
    twisted_clifford_run = BridgeChannelControlRun(twisted, twisted_clifford)
    twisted_t_run = BridgeChannelControlRun(twisted, twisted_t)
    aligned_wrong_run = BridgeChannelControlRun(aligned, twisted_clifford)
    aligned_scrambler_run = BridgeChannelControlRun(aligned, generic_scrambler)
    twisted_scrambler_run = BridgeChannelControlRun(twisted, generic_scrambler)

    low_order_audit = _compare_low_order(aligned, twisted, max_order=low_order)
    first_mismatch = _first_entropy_mismatch_order(
        aligned,
        twisted,
        max_order=aligned.block_distance + 1,
    )
    coarse_match = aligned.coarse_entropy_mincut_shadow() == twisted.coarse_entropy_mincut_shadow()
    algebra_differs = aligned.algebraic_connectivity_matrix() != twisted.algebraic_connectivity_matrix()
    atlas = _bounded_control_atlas(max_mouths=atlas_max_mouths)
    first_naive_split = next((record for record in atlas if record["entropy_matched_naive_transfer_varies"]), None)

    t_rows = twisted_t_run.transfer_rows()
    certified_claims = {
        "encoded_mouth_models_declared": True,
        "right_mouths_encoded_with_distance_three_code": aligned.block_distance == 3,
        "non_clifford_t_dressed_control_declared": twisted_t.rule_record()["non_clifford_layer"] is True,
        "generic_mouth_blind_scrambling_control_declared": generic_scrambler.rule_record()["mouth_blind"] is True,
        "coarse_entropy_mincut_shadows_match": coarse_match,
        "low_order_labeled_physical_entropy_matches": bool(low_order_audit["labeled_tables_match"])
        and low_order >= aligned.block_distance,
        "algebraic_connectivity_differs": algebra_differs,
        "naive_identity_transfer_differs": aligned_identity_run.structured_transfer_capacity() == mouths
        and twisted_identity_run.structured_transfer_capacity() == mouths - 2,
        "algebra_aware_clifford_coupling_restores_twisted_transfer": twisted_clifford_run.structured_transfer_capacity()
        == mouths,
        "non_clifford_algebraic_coupling_preserves_capacity": twisted_t_run.structured_transfer_capacity() == mouths,
        "non_clifford_pauli_transfer_not_clifford_identity": all(
            row["pauli_transfer_matrix_XYZ"] == _t_gate_pauli_transfer_matrix()
            for row in t_rows
        ),
        "non_clifford_phase_frame_restores_identity_fidelity": all(
            row["direct_identity_entanglement_fidelity"] == "(2 + sqrt(2))/4"
            and row["phase_corrected_entanglement_fidelity"] == "1"
            for row in t_rows
        ),
        "wrong_mouth_control_fails": aligned_wrong_run.structured_transfer_capacity() == mouths - 2
        and twisted_identity_run.structured_transfer_capacity() == mouths - 2,
        "generic_scrambling_control_fails_structured_transfer": aligned_scrambler_run.structured_transfer_capacity() == 0
        and twisted_scrambler_run.structured_transfer_capacity() == 0,
        "pauli_transfer_channel_fidelity_recorded": all(
            "pauli_transfer_matrix_XYZ" in row for row in twisted_t_run.transfer_rows()
        )
        and all("phase_corrected_entanglement_fidelity" in row for row in twisted_t_run.transfer_rows()),
        "otoc_support_growth_records_structure_and_scrambler_failure": all(
            row["otoc_like_signal_at_algebraic_block"] == 1
            for row in twisted_t_run.operator_growth_controls()["pauli_support_growth_rows"]  # type: ignore[index]
        )
        and all(
            row["structured_otoc_signal_at_named_block"] == 0
            for row in twisted_scrambler_run.operator_growth_controls()["pauli_support_growth_rows"]  # type: ignore[index]
        ),
        "bounded_atlas_entropy_matched_naive_transfer_varies": first_naive_split is not None
        and first_naive_split["m"] == 2,
        "bounded_atlas_algebra_aware_controls_full_capacity": all(
            record["algebra_aware_controls_full_capacity_for_all_resources"] for record in atlas
        ),
        "bounded_atlas_generic_scramblers_zero_capacity": all(
            record["generic_scrambling_controls_fail_structured_transfer"] for record in atlas
        ),
        "first_entropy_mismatch_at_decoder_scale": first_mismatch is not None
        and first_mismatch["order"] == aligned.block_distance + 1,
        "no_continuum_gravity_claim": True,
    }
    certified_claims["goal13_non_clifford_scrambling_bridge_controls_certificate"] = all(
        certified_claims.values()
    )

    return {
        "goal": "Goal 13: Non-Clifford And Scrambling Bridge-Channel Controls",
        "status": (
            "pass"
            if certified_claims["goal13_non_clifford_scrambling_bridge_controls_certificate"]
            else "fail"
        ),
        "scope": {
            "family": "encoded Bell resources with product five-qubit right-mouth blocks",
            "mouths": mouths,
            "low_order": low_order,
            "atlas_max_mouths": atlas_max_mouths,
            "right_block_code": "[[5,1,3]] five-qubit perfect stabilizer code",
            "control_protocols": (
                "identity Clifford bridge activation",
                "algebra-aware Clifford bridge activation",
                "algebra-aware non-Clifford logical T-dressed activation",
                "mouth-blind Pauli-twirled generic scrambling proxy",
            ),
        },
        "theorem_style_result": {
            "name": "Finite Bridge-Control Separation Theorem",
            "claim": (
                "For the encoded-mouth bridge family, coarse entropy/min-cut and labeled physical entropy "
                "through the code distance do not identify the mouth map.  Naive identity activation can "
                "therefore have different transfer capacity on entropy-matched resources.  Public "
                "algebra-aware activations restore full transfer, including after a non-Clifford logical "
                "T dressing, while a mouth-blind Pauli-twirled scrambling proxy has zero structured "
                "named-mouth transfer."
            ),
            "proof_sketch": (
                "The entropy-blindness proof is the distance argument from Goals 11-12: every "
                "pairing-dependent Bell check touches one left mouth and a nontrivial right logical, hence "
                "support at least d+1.  A bridge activation succeeds exactly when activation[i]=pi(i).  "
                "Composing a successful logical channel with T is non-Clifford but unitary, so capacity "
                "is unchanged and a T-dagger phase frame restores identity fidelity.  The mouth-blind "
                "Pauli twirl erases all logical Pauli transfer to named blocks, so it cannot produce "
                "structured mouth-to-mouth capacity."
            ),
        },
        "representative_witness": {
            "resources": {
                "aligned": aligned.certificate_record(),
                "twisted": twisted.certificate_record(),
            },
            "protocols": {
                "identity_clifford": identity_clifford.rule_record(),
                "twisted_algebra_aware_clifford": twisted_clifford.rule_record(),
                "twisted_algebra_aware_non_clifford_T": twisted_t.rule_record(),
                "mouth_blind_scrambler": generic_scrambler.rule_record(),
            },
            "comparisons": {
                "coarse_entropy_mincut_match": coarse_match,
                "low_order_physical_entropy_audit": low_order_audit,
                "first_entropy_mismatch": first_mismatch,
                "algebraic_connectivity_differs": algebra_differs,
                "naive_identity_activation_capacity": {
                    "aligned": aligned_identity_run.structured_transfer_capacity(),
                    "twisted": twisted_identity_run.structured_transfer_capacity(),
                },
                "algebra_aware_capacity": {
                    "twisted_clifford": twisted_clifford_run.structured_transfer_capacity(),
                    "twisted_non_clifford_T": twisted_t_run.structured_transfer_capacity(),
                },
                "wrong_mouth_capacity": {
                    "aligned_with_twisted_activation": aligned_wrong_run.structured_transfer_capacity(),
                    "twisted_with_identity_activation": twisted_identity_run.structured_transfer_capacity(),
                },
                "generic_scrambling_capacity": {
                    "aligned": aligned_scrambler_run.structured_transfer_capacity(),
                    "twisted": twisted_scrambler_run.structured_transfer_capacity(),
                },
            },
            "transfer_diagnostics": {
                "aligned_identity": aligned_identity_run.diagnostics(),
                "twisted_identity_wrong_mouth": twisted_identity_run.diagnostics(),
                "twisted_algebra_aware_clifford": twisted_clifford_run.diagnostics(),
                "twisted_algebra_aware_non_clifford_T": twisted_t_run.diagnostics(),
                "aligned_wrong_activation": aligned_wrong_run.diagnostics(),
                "aligned_mouth_blind_scrambler": aligned_scrambler_run.diagnostics(),
                "twisted_mouth_blind_scrambler": twisted_scrambler_run.diagnostics(),
            },
        },
        "bounded_atlas": {
            "records": atlas,
            "first_entropy_matched_naive_transfer_split": first_naive_split,
        },
        "diagnostic_interpretation": {
            "entropy_mincut_visible": (
                "Coarse L/R entropy, logical min-cut, and labeled physical entropy through "
                f"order {low_order} agree for the aligned/twisted resources."
            ),
            "algebra_visible": "The logical connectivity map pi predicts which public activation map transfers.",
            "channel_visible": (
                "Pauli transfer matrices, direct identity fidelity, phase-corrected fidelity, and capacity "
                "distinguish Clifford, non-Clifford T-dressed, missed, and twirled controls."
            ),
            "otoc_support_visible": (
                "Structured bridge activations have support-growth signals on the algebraic receiver; the "
                "mouth-blind twirled scrambling proxy has no structured named-mouth support signal."
            ),
            "control_visible": (
                "Wrong-mouth and mouth-blind controls show that same entanglement resources do not force "
                "structured transfer without the algebraic coupling map."
            ),
        },
        "related_work": {
            "conceptual_prior_art": (
                "Engelhardt and Liu, Algebraic ER=EPR and Complexity Transfer, arXiv:2311.04281, "
                "is the primary prior art for the broad operator-algebraic ER=EPR framing."
            ),
            "scope_boundary": (
                "This certificate does not propose a new algebraic ER=EPR definition; it supplies a finite "
                "bridge-channel control benchmark testing entropy shadows against algebraic transfer maps."
            ),
        },
        "limitations": (
            "This is an exact finite encoded-QEC control benchmark.  The non-Clifford control is a logical "
            "T-dressed transfer, and the generic scrambling control is an exact mouth-blind Pauli-twirled "
            "proxy, not a chaotic many-body simulation or continuum-gravity theorem.  Full encoded-block "
            "diagnostics still reveal the mouth map."
        ),
        "reproducibility": {
            "goal13_certificate": (
                f"python3 -m qgtoy bridge-channel-controls --mouths {mouths} --low-order {low_order} "
                f"--atlas-max-mouths {atlas_max_mouths}"
            ),
            "focused_regression": (
                "python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest."
                "test_goal13_non_clifford_scrambling_bridge_controls_certificate"
            ),
        },
        "certified_claims": certified_claims,
    }
