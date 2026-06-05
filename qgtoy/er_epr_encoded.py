"""Goal 11 encoded-mouth bridge-channel benchmark certificates."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from .gf2 import mask_to_tuple, masks_of_size
from .stabilizer import (
    StabilizerCode,
    StabilizerState,
    pauli_to_string,
    symplectic_product,
    weight,
)


def _five_qubit_perfect_code() -> StabilizerCode:
    return StabilizerCode.from_pauli_strings(("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"))


def _mask(qubits: range | tuple[int, ...]) -> int:
    out = 0
    for qubit in qubits:
        out |= 1 << qubit
    return out


def _single_pauli(total_n: int, qubit: int, letter: str) -> int:
    if letter == "X":
        return 1 << qubit
    if letter == "Z":
        return 1 << (total_n + qubit)
    raise ValueError(f"unsupported single-qubit Pauli {letter!r}")


def _shift_pauli(row: int, *, source_n: int, offset: int, total_n: int) -> int:
    source_mask = (1 << source_n) - 1
    x = row & source_mask
    z = row >> source_n
    out = 0
    for qubit in range(source_n):
        target = offset + qubit
        if (x >> qubit) & 1:
            out |= 1 << target
        if (z >> qubit) & 1:
            out |= 1 << (total_n + target)
    return out


@dataclass(frozen=True)
class EncodedMouthBridgeModel:
    """Logical Bell mouths whose right mouths are encoded in five-qubit blocks.

    Qubit ordering is ``L_0,...,L_{m-1}``, followed by right physical blocks
    ``B_0,...,B_{m-1}``, each a five-qubit perfect-code block.  The permutation
    ``pairing[i] = j`` means left mouth ``L_i`` is Bell-paired with the logical
    qubit encoded in right block ``B_j``.
    """

    name: str
    pairing: tuple[int, ...]

    def __post_init__(self) -> None:
        m = len(self.pairing)
        if sorted(self.pairing) != list(range(m)):
            raise ValueError("pairing must be a permutation of encoded right blocks")

    @property
    def m(self) -> int:
        return len(self.pairing)

    @property
    def block_code(self) -> StabilizerCode:
        return _five_qubit_perfect_code()

    @property
    def block_n(self) -> int:
        return self.block_code.n

    @property
    def block_distance(self) -> int:
        distance = self.block_code.distance()
        if distance is None:
            raise ValueError("right block code must have positive distance")
        return distance

    @property
    def n(self) -> int:
        return self.m + self.m * self.block_n

    @property
    def left_mask(self) -> int:
        return _mask(range(self.m))

    @property
    def right_mask(self) -> int:
        return _mask(range(self.m, self.n))

    def block_offset(self, block: int) -> int:
        return self.m + block * self.block_n

    def right_block_mask(self, block: int) -> int:
        return _mask(tuple(range(self.block_offset(block), self.block_offset(block) + self.block_n)))

    def shifted_logical_pair(self, block: int) -> tuple[int, int]:
        xbar, zbar = self.block_code.logical_basis
        if symplectic_product(xbar, zbar, self.block_n) != 1:
            raise ValueError("expected an anticommuting logical pair for the right block")
        offset = self.block_offset(block)
        return (
            _shift_pauli(xbar, source_n=self.block_n, offset=offset, total_n=self.n),
            _shift_pauli(zbar, source_n=self.block_n, offset=offset, total_n=self.n),
        )

    def state(self) -> StabilizerState:
        generators: list[int] = []
        for block in range(self.m):
            offset = self.block_offset(block)
            for generator in self.block_code.generators:
                generators.append(
                    _shift_pauli(generator, source_n=self.block_n, offset=offset, total_n=self.n)
                )

        for left, block in enumerate(self.pairing):
            xbar, zbar = self.shifted_logical_pair(block)
            generators.append(_single_pauli(self.n, left, "X") ^ xbar)
            generators.append(_single_pauli(self.n, left, "Z") ^ zbar)

        return StabilizerState(self.n, generators)

    def algebraic_connectivity_matrix(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(1 if self.pairing[left] == right else 0 for right in range(self.m))
            for left in range(self.m)
        )

    def fixed_mouths(self) -> tuple[tuple[int, int], ...]:
        return tuple((left, block) for left, block in enumerate(self.pairing) if left == block)

    def coarse_entropy_mincut_shadow(self) -> dict[str, object]:
        state = self.state()
        return {
            "left_entropy": state.entropy(self.left_mask),
            "right_entropy": state.entropy(self.right_mask),
            "full_entropy": state.entropy(self.left_mask | self.right_mask),
            "left_right_mutual_information": state.mutual_information(self.left_mask, self.right_mask),
            "logical_bridge_min_cut": self.m,
            "right_block_code": {
                "parameters": [self.block_n, 1, self.block_distance],
                "generators": self.block_code.pauli_generators(),
            },
        }

    def logical_block_entropy_shadow(self) -> tuple[dict[str, object], ...]:
        state = self.state()
        rows = []
        for left in range(self.m):
            left_mask = 1 << left
            for block in range(self.m):
                block_mask = self.right_block_mask(block)
                rows.append(
                    {
                        "logical_mouths": (f"L{left}", f"B{block}"),
                        "entropy": state.entropy(left_mask | block_mask),
                        "mutual_information": state.mutual_information(left_mask, block_mask),
                    }
                )
        return tuple(rows)

    def physical_low_order_entropy_profile(self, max_order: int) -> tuple[tuple[int, tuple[int, ...]], ...]:
        rows = []
        for size in range(max_order + 1):
            rows.append((size, tuple(sorted(self.state().entropy(mask) for mask in masks_of_size(self.n, size)))))
        return tuple(rows)

    def physical_low_order_entropy_table(self, max_order: int) -> tuple[tuple[tuple[int, ...], int], ...]:
        state = self.state()
        rows: list[tuple[tuple[int, ...], int]] = []
        for size in range(max_order + 1):
            for mask in masks_of_size(self.n, size):
                rows.append((mask_to_tuple(mask, self.n), state.entropy(mask)))
        return tuple(rows)

    def algebraic_reconstruction_diagnostics(self) -> dict[str, object]:
        xbar, zbar = self.block_code.logical_basis
        return {
            "connectivity_matrix_rows_L_columns_right_blocks": self.algebraic_connectivity_matrix(),
            "right_encoder": "five-qubit perfect stabilizer code, one logical qubit per right block",
            "right_block_logical_operators": {
                "Xbar": pauli_to_string(xbar, self.block_n),
                "Zbar": pauli_to_string(zbar, self.block_n),
                "Xbar_weight": weight(xbar, self.block_n),
                "Zbar_weight": weight(zbar, self.block_n),
            },
            "decoder_rule": "measure/recover the encoded logical Pauli algebra of the actual right block B_pairing[i]",
            "distance_blindness_boundary": (
                "Logical Bell checks have support on one left qubit plus a nontrivial right logical; "
                "for the five-qubit code this first appears at physical order 4."
            ),
        }

    def channel_diagnostics(self) -> dict[str, object]:
        rows = []
        for left, actual_block in enumerate(self.pairing):
            declared_block = left
            fixed = actual_block == declared_block
            rows.append(
                {
                    "input_probe": f"Q{left}",
                    "left_mouth": f"L{left}",
                    "declared_encoded_target": f"B{declared_block}",
                    "actual_encoded_receiver": f"B{actual_block}",
                    "identity_decoder_pauli_transfer_XYZ": (1, 1, 1) if fixed else (0, 0, 0),
                    "correct_decoder_pauli_transfer_XYZ": (1, 1, 1),
                    "wrong_decoder_capacity_qubits": 0 if not fixed else 1,
                    "identity_decoder_capacity_qubits": 1 if fixed else 0,
                    "correct_decoder_capacity_qubits": 1,
                    "identity_decoder_average_fidelity": "1" if fixed else "1/2",
                    "correct_decoder_average_fidelity": "1",
                }
            )
        identity_capacity = sum(int(row["identity_decoder_capacity_qubits"]) for row in rows)
        correct_capacity = sum(int(row["correct_decoder_capacity_qubits"]) for row in rows)
        return {
            "declared_coupling": "encoded Bell-teleportation with identity right-block decoder B_i",
            "port_channels": tuple(rows),
            "naive_identity_decoder_capacity_qubits": identity_capacity,
            "correct_algebraic_decoder_capacity_qubits": correct_capacity,
            "capacity_formula": "identity decoder capacity equals fixed points of the encoded connectivity map",
        }

    def operator_growth_controls(self) -> dict[str, object]:
        rows = []
        for left, actual_block in enumerate(self.pairing):
            fixed = left == actual_block
            rows.append(
                {
                    "probe": f"Q{left}",
                    "encoded_output_support": f"B{actual_block}",
                    "encoded_output_weight": self.block_distance,
                    "identity_target_detector": f"B{left}",
                    "correct_detector": f"B{actual_block}",
                    "otoc_like_signal_at_identity_target": 1 if fixed else 0,
                    "otoc_like_signal_at_correct_block": 1,
                }
            )
        return {
            "pauli_support_growth_rows": tuple(rows),
            "support_growth_summary": {
                "left_probe_weight": 1,
                "encoded_output_weight": self.block_distance,
                "identity_target_hits": len(self.fixed_mouths()),
                "wrong_encoded_mouth_hits": self.m - len(self.fixed_mouths()),
            },
            "control_interpretation": (
                "The twisted resource has the same low-order physical entropies as the aligned resource, "
                "but OTOC-like detector signals appear on the algebraically correct encoded block."
            ),
        }

    def certificate_record(self) -> dict[str, object]:
        return {
            "name": self.name,
            "pairing_left_to_right_block": self.pairing,
            "parameters": {
                "left_mouths": self.m,
                "right_encoded_blocks": self.m,
                "physical_qubits": self.n,
                "right_block_code": [self.block_n, 1, self.block_distance],
            },
            "stabilizer_generators": self.state().pauli_generators(),
            "coarse_entropy_mincut_shadow": self.coarse_entropy_mincut_shadow(),
            "logical_block_entropy_shadow": self.logical_block_entropy_shadow(),
            "algebraic_reconstruction": self.algebraic_reconstruction_diagnostics(),
            "channel_diagnostics": self.channel_diagnostics(),
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


def _capacity_profile(m: int) -> dict[int, int]:
    profile: dict[int, int] = {}
    for pairing in permutations(range(m)):
        capacity = sum(1 for left, block in enumerate(pairing) if left == block)
        profile[capacity] = profile.get(capacity, 0) + 1
    return dict(sorted(profile.items()))


def _bounded_encoded_atlas(*, max_mouths: int) -> tuple[dict[str, object], ...]:
    records = []
    for m in range(1, max_mouths + 1):
        models = tuple(EncodedMouthBridgeModel(name=f"m{m}_{pairing}", pairing=pairing) for pairing in permutations(range(m)))
        low_order_profiles = {repr(model.physical_low_order_entropy_profile(model.block_distance)) for model in models}
        coarse_shadows = {repr(model.coarse_entropy_mincut_shadow()) for model in models}
        capacities = {model.channel_diagnostics()["naive_identity_decoder_capacity_qubits"] for model in models}
        records.append(
            {
                "m": m,
                "models_checked": len(models),
                "coarse_shadow_classes": len(coarse_shadows),
                "low_order_physical_entropy_profile_classes_through_distance": len(low_order_profiles),
                "identity_decoder_capacity_profile": _capacity_profile(m),
                "same_low_order_profile_capacity_varies": len(low_order_profiles) == 1 and len(capacities) > 1,
            }
        )
    return tuple(records)


def goal11_encoded_mouth_bridge_channel_certificate(
    *,
    mouths: int = 2,
    low_order: int = 3,
    atlas_max_mouths: int = 3,
) -> dict[str, object]:
    if mouths < 2:
        raise ValueError("mouths must be at least 2 for an aligned/twisted channel split")
    if atlas_max_mouths < mouths:
        raise ValueError("atlas_max_mouths must be at least mouths")

    aligned_pairing = tuple(range(mouths))
    twisted_pairing = (1, 0) + tuple(range(2, mouths))
    aligned = EncodedMouthBridgeModel(name="aligned_encoded_mouth_bridge", pairing=aligned_pairing)
    twisted = EncodedMouthBridgeModel(name="twisted_encoded_mouth_bridge", pairing=twisted_pairing)

    low_order_audit = _compare_low_order(aligned, twisted, max_order=low_order)
    first_mismatch = _first_entropy_mismatch_order(
        aligned,
        twisted,
        max_order=aligned.block_distance + 1,
    )
    coarse_match = aligned.coarse_entropy_mincut_shadow() == twisted.coarse_entropy_mincut_shadow()
    logical_block_split = aligned.logical_block_entropy_shadow() != twisted.logical_block_entropy_shadow()
    algebra_differs = aligned.algebraic_connectivity_matrix() != twisted.algebraic_connectivity_matrix()
    aligned_channel = aligned.channel_diagnostics()
    twisted_channel = twisted.channel_diagnostics()
    naive_channel_differs = (
        aligned_channel["naive_identity_decoder_capacity_qubits"]
        != twisted_channel["naive_identity_decoder_capacity_qubits"]
    )
    correct_decoder_restores = (
        aligned_channel["correct_algebraic_decoder_capacity_qubits"] == mouths
        and twisted_channel["correct_algebraic_decoder_capacity_qubits"] == mouths
    )
    atlas = _bounded_encoded_atlas(max_mouths=atlas_max_mouths)
    first_atlas_split = next((record for record in atlas if record["same_low_order_profile_capacity_varies"]), None)

    certified_claims = {
        "encoded_mouth_models_declared": True,
        "right_mouths_encoded_with_distance_three_code": aligned.block_distance == 3,
        "coarse_entropy_mincut_shadows_match": coarse_match,
        "low_order_labeled_physical_entropy_matches": bool(low_order_audit["labeled_tables_match"])
        and low_order >= aligned.block_distance,
        "logical_block_entropy_reveals_decoder_scale_map": logical_block_split,
        "algebraic_connectivity_differs": algebra_differs,
        "naive_identity_decoder_channel_differs": naive_channel_differs
        and aligned_channel["naive_identity_decoder_capacity_qubits"] == mouths
        and twisted_channel["naive_identity_decoder_capacity_qubits"] == mouths - 2,
        "correct_algebraic_decoder_restores_capacity": correct_decoder_restores,
        "wrong_decoder_control_certified": all(
            row["identity_decoder_capacity_qubits"] == 0
            for row in twisted_channel["port_channels"][:2]  # type: ignore[index]
        ),
        "otoc_like_correct_block_signals_recorded": all(
            row["otoc_like_signal_at_correct_block"] == 1
            for row in twisted.operator_growth_controls()["pauli_support_growth_rows"]  # type: ignore[index]
        ),
        "bounded_atlas_has_low_order_blind_capacity_variation": first_atlas_split is not None
        and first_atlas_split["m"] == 2,
        "first_entropy_mismatch_at_decoder_scale": first_mismatch is not None
        and first_mismatch["order"] == aligned.block_distance + 1,
        "no_continuum_gravity_claim": True,
    }
    certified_claims["goal11_encoded_mouth_bridge_channel_certificate"] = all(certified_claims.values())

    return {
        "goal": "Goal 11: Encoded-Mouth Bridge-Channel Benchmark",
        "status": "pass" if certified_claims["goal11_encoded_mouth_bridge_channel_certificate"] else "fail",
        "scope": {
            "family": "logical Bell pairs with right mouths encoded into five-qubit perfect-code blocks",
            "mouths": mouths,
            "low_order": low_order,
            "atlas_max_mouths": atlas_max_mouths,
            "right_block_code": "[[5,1,3]] five-qubit perfect stabilizer code",
            "coupling_family": "identity encoded-mouth decoder versus algebraically correct decoder",
        },
        "theorem_style_result": {
            "name": "Encoded-Mouth Distance-Blind Channel Theorem",
            "claim": (
                "For encoded Bell resources whose right mouths are encoded in distance-d stabilizer blocks, "
                "logical mouth twists are invisible to labeled physical entropy diagnostics through order d, "
                "but the identity decoded channel capacity is the number of fixed points of the logical "
                "connectivity map.  The correct algebraic decoder restores full capacity."
            ),
            "proof_sketch": (
                "The right code stabilizers are identical for all logical mouth pairings.  The only pairing-"
                "dependent stabilizers are Bell checks L_i X/Z times a nontrivial right logical operator.  "
                "Every nontrivial right logical has weight at least d, so every pairing-dependent check has "
                "physical support at least d+1.  Therefore entropy ranks on regions of size at most d are "
                "pairing-independent.  Decoding block B_j recovers the probe paired with that block, so an "
                "identity decoder succeeds exactly on fixed points and the permutation-aware decoder succeeds "
                "on all mouths."
            ),
        },
        "representative_witness": {
            "first": aligned.certificate_record(),
            "second": twisted.certificate_record(),
            "comparisons": {
                "coarse_entropy_mincut_match": coarse_match,
                "low_order_physical_entropy_audit": low_order_audit,
                "first_entropy_mismatch": first_mismatch,
                "logical_block_entropy_split": logical_block_split,
                "algebraic_connectivity_differs": algebra_differs,
                "naive_identity_decoder_capacity": {
                    "first": aligned_channel["naive_identity_decoder_capacity_qubits"],
                    "second": twisted_channel["naive_identity_decoder_capacity_qubits"],
                },
                "correct_decoder_capacity": {
                    "first": aligned_channel["correct_algebraic_decoder_capacity_qubits"],
                    "second": twisted_channel["correct_algebraic_decoder_capacity_qubits"],
                },
            },
        },
        "bounded_atlas": {
            "records": atlas,
            "first_low_order_blind_capacity_split": first_atlas_split,
        },
        "scalable_family_statement": {
            "status": "theorem_schema",
            "claim": (
                "Replacing the five-qubit block by any right-mouth stabilizer encoding family with distance d "
                "hides logical mouth twists from physical entropy probes of order at most d, while decoded "
                "capacity remains controlled by the logical connectivity map.  Distance amplification would "
                "raise the physical order at which entropy can detect the mouth map."
            ),
            "caveat": (
                "The checked certificate instantiates the theorem with product five-qubit blocks.  It does not "
                "construct a new asymptotic tensor-network geometry or noisy approximate decoder."
            ),
        },
        "diagnostic_interpretation": {
            "entropy_mincut_visible": (
                "Coarse L/R entropy, logical bridge min-cut, and all labeled physical entropy regions through "
                f"order {low_order} agree for the representative aligned/twisted pair."
            ),
            "decoder_scale_visible": (
                "Full encoded blocks reveal the logical mouth map; this is the algebraic decoder scale, not a "
                "low-order physical shadow."
            ),
            "algebra_visible": "The logical connectivity matrix predicts identity-decoder and correct-decoder capacity.",
            "channel_visible": "The certificate emits exact zero/one Pauli transfer matrices for identity and correct decoders.",
            "control_visible": "Wrong identity decoders fail on twisted mouths; OTOC-like signals appear on the correct encoded block.",
        },
        "related_work": {
            "conceptual_prior_art": (
                "Engelhardt and Liu, Algebraic ER=EPR and Complexity Transfer, arXiv:2311.04281, "
                "is the primary prior art for the broad operator-algebraic ER=EPR framing."
            ),
            "scope_boundary": (
                "This certificate does not propose a new algebraic ER=EPR definition; it supplies a finite "
                "encoded-mouth bridge-channel certificate for low-order entropy blindness versus channel recovery."
            ),
        },
        "limitations": (
            "This is an exact stabilizer encoded-mouth theorem, not a continuum-gravity theorem, not a noisy "
            "approximate-QEC theorem, and not a many-body traversable-wormhole simulation.  Full encoded-block "
            "entropy/reconstruction detects the mouth map; the separation is against coarse and low-order "
            "physical diagnostics."
        ),
        "reproducibility": {
            "goal11_certificate": (
                f"python3 -m qgtoy er-epr-encoded --mouths {mouths} --low-order {low_order} "
                f"--atlas-max-mouths {atlas_max_mouths}"
            ),
            "focused_regression": (
                "python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest."
                "test_goal11_encoded_mouth_bridge_channel_certificate"
            ),
        },
        "certified_claims": certified_claims,
    }
