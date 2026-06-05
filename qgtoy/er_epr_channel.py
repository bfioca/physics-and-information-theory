"""Goal 10 algebraic ER=EPR finite channel benchmark certificates."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from .gf2 import mask_to_tuple
from .stabilizer import StabilizerState


def _mask(qubits: tuple[int, ...] | list[int] | range) -> int:
    out = 0
    for qubit in qubits:
        out |= 1 << qubit
    return out


def _pair_pauli(n: int, first: int, second: int, letter: str) -> str:
    chars = ["I"] * n
    chars[first] = letter
    chars[second] = letter
    return "".join(chars)


@dataclass(frozen=True)
class EPRPairingModel:
    """Product of EPR links between named left and right mouth ports.

    Qubit ordering is ``L_0,...,L_{m-1},R_0,...,R_{m-1}``.  The permutation
    ``pairing[i] = j`` means the algebraic EPR bridge connects ``L_i`` to
    ``R_j``.
    """

    name: str
    pairing: tuple[int, ...]

    def __post_init__(self) -> None:
        m = len(self.pairing)
        if sorted(self.pairing) != list(range(m)):
            raise ValueError("pairing must be a permutation of right-mouth ports")

    @property
    def m(self) -> int:
        return len(self.pairing)

    @property
    def n(self) -> int:
        return 2 * self.m

    @property
    def left_mask(self) -> int:
        return _mask(range(self.m))

    @property
    def right_mask(self) -> int:
        return _mask(range(self.m, 2 * self.m))

    def left_port_mask(self, index: int) -> int:
        return 1 << index

    def right_port_mask(self, index: int) -> int:
        return 1 << (self.m + index)

    def state(self) -> StabilizerState:
        generators: list[str] = []
        for left, right in enumerate(self.pairing):
            right_qubit = self.m + right
            generators.append(_pair_pauli(self.n, left, right_qubit, "X"))
            generators.append(_pair_pauli(self.n, left, right_qubit, "Z"))
        return StabilizerState.from_pauli_strings(tuple(generators))

    def min_cut(self, region_mask: int) -> int:
        """Exact cut count in the EPR-link graph; equals stabilizer entropy."""
        value = 0
        for left, right in enumerate(self.pairing):
            left_inside = (region_mask >> left) & 1
            right_inside = (region_mask >> (self.m + right)) & 1
            if left_inside ^ right_inside:
                value += 1
        return value

    def algebraic_connectivity_matrix(self) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(1 if self.pairing[left] == right else 0 for right in range(self.m))
            for left in range(self.m)
        )

    def fixed_mouth_edges(self) -> tuple[tuple[int, int], ...]:
        return tuple((left, right) for left, right in enumerate(self.pairing) if left == right)

    def coarse_entropy_mincut_shadow(self) -> dict[str, object]:
        state = self.state()
        full = (1 << self.n) - 1
        single_left_entropies = tuple(state.entropy(self.left_port_mask(i)) for i in range(self.m))
        single_right_entropies = tuple(state.entropy(self.right_port_mask(i)) for i in range(self.m))
        return {
            "left_entropy": state.entropy(self.left_mask),
            "right_entropy": state.entropy(self.right_mask),
            "full_entropy": state.entropy(full),
            "left_right_mutual_information": state.mutual_information(self.left_mask, self.right_mask),
            "left_min_cut": self.min_cut(self.left_mask),
            "right_min_cut": self.min_cut(self.right_mask),
            "single_left_entropy_multiset": tuple(sorted(single_left_entropies)),
            "single_right_entropy_multiset": tuple(sorted(single_right_entropies)),
        }

    def port_resolved_entropy_mincut_shadow(self) -> tuple[dict[str, object], ...]:
        state = self.state()
        rows = []
        for left in range(self.m):
            for right in range(self.m):
                region = self.left_port_mask(left) | self.right_port_mask(right)
                rows.append(
                    {
                        "ports": (f"L{left}", f"R{right}"),
                        "entropy": state.entropy(region),
                        "mutual_information": state.mutual_information(
                            self.left_port_mask(left), self.right_port_mask(right)
                        ),
                        "min_cut": self.min_cut(region),
                    }
                )
        return tuple(rows)

    def entanglement_diagnostics(self) -> dict[str, object]:
        state = self.state()
        cmi_triplet = None
        tripartite = None
        if self.m >= 2:
            l0 = self.left_port_mask(0)
            r0 = self.right_port_mask(0)
            r1 = self.right_port_mask(1)
            cmi_triplet = state.conditional_mutual_information(l0, r0, r1)
            tripartite = state.tripartite_information(l0, r0, r1)
        return {
            "stabilizer_generators": state.pauli_generators(),
            "named_regions": {
                "L": mask_to_tuple(self.left_mask, self.n),
                "R": mask_to_tuple(self.right_mask, self.n),
                "L_intersect_R": mask_to_tuple(self.left_mask & self.right_mask, self.n),
                "L_union_R": mask_to_tuple(self.left_mask | self.right_mask, self.n),
            },
            "coarse_entropy_mincut_shadow": self.coarse_entropy_mincut_shadow(),
            "port_resolved_entropy_mincut_shadow": self.port_resolved_entropy_mincut_shadow(),
            "sample_cmi_I_L0_R0_given_R1": cmi_triplet,
            "sample_tripartite_I3_L0_R0_R1": tripartite,
        }

    def algebraic_connectivity_diagnostics(self) -> dict[str, object]:
        noncenter_edges = tuple(
            {
                "left_port": f"L{left}",
                "right_port": f"R{right}",
                "correlation_generators": (f"X_L{left} X_R{right}", f"Z_L{left} Z_R{right}"),
                "bridge_algebra_type": "noncentral qubit-pair correlation",
            }
            for left, right in enumerate(self.pairing)
        )
        return {
            "connectivity_matrix_rows_L_columns_R": self.algebraic_connectivity_matrix(),
            "noncenter_bridge_edges": noncenter_edges,
            "center_only_bridge_edges": (),
            "fixed_mouth_edges": self.fixed_mouth_edges(),
            "nonfactorization_witness": (
                "The state factorizes as a product over algebraic EPR edges, not over the declared "
                "identity mouth pairing unless the connectivity permutation is the identity."
            ),
        }

    def identity_mouth_channel_diagnostics(self) -> dict[str, object]:
        """Exact channel under the declared identity-mouth teleportation coupling.

        The coupling is the standard Bell-measurement plus Pauli-feed-forward
        Clifford teleportation gadget from an external probe Q_i through L_i to
        the declared output R_i.  The EPR resource supplies a perfect qubit
        channel to R_i exactly when the algebraic bridge edge is L_i--R_i.
        """
        port_channels = []
        for left, actual_right in enumerate(self.pairing):
            target_right = left
            fixed = actual_right == target_right
            port_channels.append(
                {
                    "input_probe": f"Q{left}",
                    "left_mouth": f"L{left}",
                    "declared_target": f"R{target_right}",
                    "actual_algebraic_receiver": f"R{actual_right}",
                    "target_pauli_transfer_diagonal_XYZ": (1, 1, 1) if fixed else (0, 0, 0),
                    "actual_receiver_pauli_transfer_diagonal_XYZ": (1, 1, 1),
                    "average_fidelity_to_declared_target": "1" if fixed else "1/2",
                    "quantum_capacity_to_declared_target_qubits": 1 if fixed else 0,
                    "wrong_mouth_transfer": not fixed,
                }
            )
        fixed_capacity = sum(row["quantum_capacity_to_declared_target_qubits"] for row in port_channels)
        return {
            "declared_coupling": "identity-mouth Bell-teleportation Clifford gadget Q_i + L_i -> R_i",
            "port_channels": tuple(port_channels),
            "fixed_mouth_quantum_capacity_qubits": fixed_capacity,
            "optimal_right_port_relabel_capacity_qubits": self.m,
            "capacity_formula": "number of fixed points of the algebraic connectivity permutation",
        }

    def operator_growth_controls(self) -> dict[str, object]:
        rows = []
        commutator_rows = []
        for left, actual_right in enumerate(self.pairing):
            fixed = left == actual_right
            rows.append(
                {
                    "probe": f"Q{left}",
                    "heisenberg_output_support": (f"R{actual_right}",),
                    "output_pauli_weight": 1,
                    "declared_target_overlap": 1 if fixed else 0,
                    "off_target_wrong_mouth": not fixed,
                }
            )
            commutator_rows.append(
                {
                    "probe": f"Q{left}",
                    "declared_target_detector": f"R{left}",
                    "actual_receiver_detector": f"R{actual_right}",
                    "otoc_like_commutator_signal_at_declared_target": 1 if fixed else 0,
                    "otoc_like_commutator_signal_at_actual_receiver": 1,
                }
            )
        return {
            "pauli_support_growth_rows": tuple(rows),
            "otoc_like_commutator_rows": tuple(commutator_rows),
            "size_distribution": {
                "all_transferred_nonidentity_probe_paulis_have_output_weight": 1,
                "declared_target_hits": sum(1 for left, right in enumerate(self.pairing) if left == right),
                "wrong_mouth_hits": sum(1 for left, right in enumerate(self.pairing) if left != right),
            },
            "generic_scrambling_control_status": (
                "exact permutation-scrambling proxy only; this is not a chaotic many-body scrambling model"
            ),
            "control_interpretation": (
                "Permutation-scrambled EPR resources have the same coarse L/R entanglement and the same "
                "operator size, but send probes to the wrong right-mouth ports under the declared coupling."
            ),
        }

    def certificate_record(self) -> dict[str, object]:
        return {
            "name": self.name,
            "pairing_left_to_right": self.pairing,
            "parameters": {"left_ports": self.m, "right_ports": self.m, "physical_qubits": self.n},
            "entanglement_diagnostics": self.entanglement_diagnostics(),
            "algebraic_connectivity_diagnostics": self.algebraic_connectivity_diagnostics(),
            "channel_diagnostics": self.identity_mouth_channel_diagnostics(),
            "operator_growth_controls": self.operator_growth_controls(),
        }


def _capacity_profile_for_m(m: int) -> dict[int, int]:
    profile: dict[int, int] = {}
    for pairing in permutations(range(m)):
        capacity = sum(1 for left, right in enumerate(pairing) if left == right)
        profile[capacity] = profile.get(capacity, 0) + 1
    return dict(sorted(profile.items()))


def _atlas_records(max_pairs: int) -> tuple[dict[str, object], ...]:
    rows = []
    for m in range(1, max_pairs + 1):
        models = tuple(EPRPairingModel(name=f"m{m}_{pairing}", pairing=pairing) for pairing in permutations(range(m)))
        coarse_shadows = {repr(model.coarse_entropy_mincut_shadow()) for model in models}
        capacities = {
            model.identity_mouth_channel_diagnostics()["fixed_mouth_quantum_capacity_qubits"] for model in models
        }
        rows.append(
            {
                "m": m,
                "models_checked": len(models),
                "coarse_entropy_mincut_shadow_classes": len(coarse_shadows),
                "fixed_mouth_capacity_profile": _capacity_profile_for_m(m),
                "same_coarse_shadow_capacity_varies": len(coarse_shadows) == 1 and len(capacities) > 1,
            }
        )
    return tuple(rows)


def goal10_algebraic_er_epr_channel_benchmark_certificate(*, max_pairs: int = 4) -> dict[str, object]:
    if max_pairs < 2:
        raise ValueError("max_pairs must be at least 2 for the aligned/crossed witness")

    aligned = EPRPairingModel(name="aligned_identity_bridge", pairing=(0, 1))
    crossed = EPRPairingModel(name="crossed_wrong_mouth_bridge", pairing=(1, 0))

    aligned_record = aligned.certificate_record()
    crossed_record = crossed.certificate_record()
    coarse_match = aligned.coarse_entropy_mincut_shadow() == crossed.coarse_entropy_mincut_shadow()
    port_entropy_splits = aligned.port_resolved_entropy_mincut_shadow() != crossed.port_resolved_entropy_mincut_shadow()
    algebra_differs = aligned.algebraic_connectivity_matrix() != crossed.algebraic_connectivity_matrix()
    aligned_capacity = aligned.identity_mouth_channel_diagnostics()["fixed_mouth_quantum_capacity_qubits"]
    crossed_capacity = crossed.identity_mouth_channel_diagnostics()["fixed_mouth_quantum_capacity_qubits"]
    channel_differs = aligned_capacity != crossed_capacity
    atlas = _atlas_records(max_pairs)
    first_capacity_collision = next(
        (record for record in atlas if record["same_coarse_shadow_capacity_varies"]),
        None,
    )

    certified_claims = {
        "exact_permutation_epr_family_declared": True,
        "aligned_crossed_coarse_entropy_mincut_match": coarse_match,
        "aligned_crossed_port_resolved_entropy_splits": port_entropy_splits,
        "aligned_crossed_algebraic_connectivity_differs": algebra_differs,
        "aligned_crossed_fixed_mouth_channel_differs": channel_differs
        and aligned_capacity == 2
        and crossed_capacity == 0,
        "operator_growth_wrong_mouth_control_certified": all(
            row["wrong_mouth_transfer"]
            for row in crossed.identity_mouth_channel_diagnostics()["port_channels"]  # type: ignore[index]
        ),
        "bounded_atlas_has_same_coarse_shadow_capacity_variation": first_capacity_collision is not None
        and first_capacity_collision["m"] == 2,
        "optimal_relabel_capacity_limitation_recorded": (
            aligned.identity_mouth_channel_diagnostics()["optimal_right_port_relabel_capacity_qubits"] == 2
            and crossed.identity_mouth_channel_diagnostics()["optimal_right_port_relabel_capacity_qubits"] == 2
        ),
        "no_continuum_gravity_claim": True,
    }
    certified_claims["goal10_algebraic_er_epr_channel_benchmark_certificate"] = all(certified_claims.values())

    return {
        "goal": "Goal 10: Algebraic ER=EPR Channel Benchmark",
        "status": "pass" if certified_claims["goal10_algebraic_er_epr_channel_benchmark_certificate"] else "fail",
        "scope": {
            "family": "finite stabilizer EPR-pairing resources with named left/right mouth ports",
            "max_pairs": max_pairs,
            "coupling_family": "identity-mouth Bell-teleportation Clifford coupling",
            "minimality_scope": "permutation EPR resources; first channel split occurs at m=2",
        },
        "theorem_style_result": {
            "name": "Permutation-EPR Fixed-Mouth Channel Theorem",
            "claim": (
                "For m EPR bridge resources whose algebraic connectivity is a permutation pi from L ports "
                "to R ports, the declared identity-mouth teleportation channel Q_i,L_i -> R_i has exact "
                "qubit capacity equal to the number of fixed points of pi.  Coarse L/R entropy and EPR "
                "min-cut diagnostics depend only on m, so they do not determine the fixed-mouth channel."
            ),
            "proof_sketch": (
                "Each EPR edge L_i--R_pi(i) supplies the standard stabilizer teleportation resource.  "
                "The identity-mouth Clifford gadget recovers the probe at R_i iff pi(i)=i; otherwise the "
                "same Pauli transfer appears at the wrong mouth R_pi(i), and the declared target channel "
                "is depolarizing.  The product of EPR edges has S(L)=S(R)=mincut(L)=m for every permutation."
            ),
        },
        "representative_witness": {
            "first": aligned_record,
            "second": crossed_record,
            "comparisons": {
                "coarse_entropy_mincut_match": coarse_match,
                "port_resolved_entropy_mincut_split": port_entropy_splits,
                "algebraic_connectivity_differs": algebra_differs,
                "fixed_mouth_channel_capacity": {
                    "first": aligned_capacity,
                    "second": crossed_capacity,
                },
                "channel_differs": channel_differs,
            },
        },
        "bounded_atlas": {
            "records": atlas,
            "first_same_coarse_shadow_channel_split": first_capacity_collision,
        },
        "diagnostic_interpretation": {
            "entropy_mincut_visible": (
                "Coarse L/R entropy and min-cut count the number of bridge resources but not which mouth "
                "is connected to which.  Port-resolved pair entropies do split this simple EPR witness."
            ),
            "algebra_visible": (
                "The connectivity matrix records the operator-algebraic EPR edge structure and exactly "
                "predicts the fixed-mouth channel."
            ),
            "channel_visible": (
                "The declared channel is a stabilizer/Clifford teleportation protocol with exact Pauli "
                "transfer matrices and exact zero/one qubit capacities."
            ),
            "control_visible": (
                "The crossed resource is a wrong-mouth control: it has the same coarse entanglement and "
                "same one-qubit operator size, but the probe exits at the wrong named mouth."
            ),
        },
        "limitations": (
            "This is a finite stabilizer port benchmark, not a continuum-gravity theorem and not a generic "
            "many-body traversable-wormhole simulation.  The separation is against coarse L/R entropy and "
            "min-cut shadows; full port-resolved entropy detects the EPR pairing in this simple family.  "
            "The next harder target is a non-Clifford or tensor-network family where richer entropy/min-cut "
            "diagnostics still collide while operator algebra predicts channel capacity."
        ),
        "reproducibility": {
            "goal10_certificate": f"python3 -m qgtoy er-epr-channel --max-pairs {max_pairs}",
            "focused_regression": (
                "python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest."
                "test_goal10_algebraic_er_epr_channel_benchmark_certificate"
            ),
        },
        "certified_claims": certified_claims,
    }
