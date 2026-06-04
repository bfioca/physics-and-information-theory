"""Exact tensor-network / holographic-code toy diagnostics."""

from __future__ import annotations

import math
from math import factorial
from itertools import combinations, permutations, product

from .cosmology import (
    bounded_distance_certificate,
    block_shift_pauli,
    cached_frontier_source_summary,
    enumerate_graph_subspace_code_records,
    graph_labeled_pair_source,
    graph_subspace_record_summary,
    bridge_observer_cover,
    lift_inner_region_over_blocks,
    logical_concatenate_k1,
    phase11_outer_distance_repair_code,
    relaxed_labeled_graph_constraints,
)
from .family import repeat_balanced_bridge
from .gf2 import in_span, mask_from_qubits, mask_to_tuple, masks_of_size
from .robust import RobustConstraints, code_quality, entropy_key, scan_robust_source
from .stabilizer import (
    LOCAL_CLIFFORD_MATRICES,
    StabilizerCode,
    local_clifford_pauli,
    pauli_from_string,
    pauli_to_string,
    permute_pauli,
    symplectic_product,
)
from .structured import apply_cx, apply_h, apply_s


def holographic_phase1_boundary_order() -> tuple[int, ...]:
    return (0, 1, 6, 2, 3, 7, 4, 5)


def holographic_phase1_network_edges() -> tuple[dict[str, object], ...]:
    boundary_order = holographic_phase1_boundary_order()
    ring_edges = tuple(
        {
            "left": f"q{boundary_order[index]}",
            "right": f"q{boundary_order[(index + 1) % len(boundary_order)]}",
            "capacity": 1,
            "edge_type": "boundary_ring",
        }
        for index in range(len(boundary_order))
    )
    spokes = tuple(
        {
            "left": "bulk_center",
            "right": f"q{qubit}",
            "capacity": 1,
            "edge_type": "bulk_spoke",
        }
        for qubit in sorted(boundary_order)
    )
    return ring_edges + spokes


def holographic_phase1_network_spec() -> dict[str, object]:
    boundary_order = holographic_phase1_boundary_order()
    return {
        "name": "goal3_phase1_ring_spoke_stabilizer_network",
        "description": (
            "A small holographic-looking stabilizer tensor-network skeleton: eight boundary qubits on a ring "
            "plus one bulk-center node with unit spokes. The same skeleton is used for both code realizations."
        ),
        "network_kind": "boundary_ring_plus_bulk_spokes",
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": ("bulk_center",),
        "bulk_logical_qubits": 1,
        "edges": holographic_phase1_network_edges(),
        "min_cut_semantics": (
            "For a boundary region R, brute-force all internal-node assignments and minimize the unit-capacity "
            "edge cut separating boundary nodes in R from boundary nodes outside R."
        ),
    }


def holographic_phase1_ring_intervals(*, max_length: int = 2) -> tuple[dict[str, object], ...]:
    boundary_order = holographic_phase1_boundary_order()
    regions = []
    for length in range(1, max_length + 1):
        for start in range(len(boundary_order)):
            qubits = tuple(boundary_order[(start + offset) % len(boundary_order)] for offset in range(length))
            regions.append(
                {
                    "name": f"ring_interval_start{start}_len{length}",
                    "region_type": "boundary_ring_interval",
                    "start": start,
                    "length": length,
                    "qubits": qubits,
                    "mask": mask_from_qubits(qubits),
                }
            )
    return tuple(regions)


def holographic_phase1_named_regions() -> tuple[dict[str, object], ...]:
    cover = bridge_observer_cover(1)
    return tuple(
        {
            "name": patch.name,
            "region_type": patch.role,
            "qubits": mask_to_tuple(patch.region, 8),
            "mask": patch.region,
        }
        for patch in cover.patches
    )


def holographic_phase1_region_specs() -> tuple[dict[str, object], ...]:
    return holographic_phase1_named_regions() + holographic_phase1_ring_intervals(max_length=2)


def holographic_phase1_min_cut(region_mask: int) -> dict[str, object]:
    spec = holographic_phase1_network_spec()
    boundary_nodes = tuple(str(node) for node in spec["boundary_nodes"])  # type: ignore[index]
    internal_nodes = tuple(str(node) for node in spec["internal_nodes"])  # type: ignore[index]
    region_nodes = {f"q{qubit}" for qubit in mask_to_tuple(region_mask, 8)}
    boundary_set = set(boundary_nodes)
    if not region_nodes <= boundary_set:
        raise ValueError("min-cut region contains a qubit outside the boundary")
    best_value: int | None = None
    best_assignments = []
    for assignment_bits in product((False, True), repeat=len(internal_nodes)):
        side = set(region_nodes)
        assignment = dict(zip(internal_nodes, assignment_bits))
        for node, in_region_side in assignment.items():
            if in_region_side:
                side.add(node)
        cut = 0
        for edge in spec["edges"]:  # type: ignore[index]
            left = str(edge["left"])
            right = str(edge["right"])
            if (left in side) != (right in side):
                cut += int(edge["capacity"])
        if best_value is None or cut < best_value:
            best_value = cut
            best_assignments = [assignment]
        elif cut == best_value:
            best_assignments.append(assignment)
    if best_value is None:
        raise RuntimeError("expected at least one min-cut assignment")
    return {
        "value": best_value,
        "assignments_checked": 2 ** len(internal_nodes),
        "minimizing_internal_assignments": tuple(
            tuple(sorted(assignment.items()))
            for assignment in best_assignments
        ),
    }


def holographic_phase1_region_diagnostic(
    *,
    code: StabilizerCode,
    region: dict[str, object],
) -> dict[str, object]:
    region_mask = int(region["mask"])
    full = (1 << code.n) - 1
    algebra = code.region_algebra(region_mask)
    return {
        "entropy": code.entropy(region_mask),
        "min_cut": holographic_phase1_min_cut(region_mask),
        "algebra_signature": algebra.signature(),
        "reconstructs_all": algebra.reconstructs_all,
        "erasure_correctable": code.erasure_correctable(region_mask),
        "survivor_fixed_point_reconstructs_all": code.reconstructs_all_logicals(full ^ region_mask),
    }


def holographic_phase1_pair_region_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region: dict[str, object],
) -> dict[str, object]:
    first_diag = holographic_phase1_region_diagnostic(code=first, region=region)
    second_diag = holographic_phase1_region_diagnostic(code=second, region=region)
    entropy_matches = int(first_diag["entropy"]) == int(second_diag["entropy"])
    min_cut_matches = first_diag["min_cut"] == second_diag["min_cut"]
    algebra_matches = first_diag["algebra_signature"] == second_diag["algebra_signature"]
    erasure_matches = bool(first_diag["erasure_correctable"]) == bool(second_diag["erasure_correctable"])
    survivor_matches = bool(first_diag["survivor_fixed_point_reconstructs_all"]) == bool(
        second_diag["survivor_fixed_point_reconstructs_all"]
    )
    return {
        "region": {
            key: value
            for key, value in region.items()
            if key != "mask"
        },
        "min_cut": first_diag["min_cut"],
        "first": first_diag,
        "second": second_diag,
        "comparisons": {
            "entropy_matches": entropy_matches,
            "min_cut_matches": min_cut_matches,
            "algebra_signature_matches": algebra_matches,
            "erasure_correctability_matches": erasure_matches,
            "survivor_fixed_point_matches": survivor_matches,
            "entropy_and_min_cut_visible_match": entropy_matches and min_cut_matches,
            "reconstruction_visible_differs": not algebra_matches,
            "erasure_visible_differs": not erasure_matches or not survivor_matches,
        },
    }


def holographic_phase1_code_pair() -> tuple[StabilizerCode, StabilizerCode]:
    return repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=1)


def bridge_holography_phase1_certificate() -> dict[str, object]:
    first, second = holographic_phase1_code_pair()
    regions = holographic_phase1_region_specs()
    records = tuple(
        holographic_phase1_pair_region_record(first=first, second=second, region=region)
        for region in regions
    )
    named_records = tuple(record for record in records if record["region"]["region_type"] != "boundary_ring_interval")
    ring_records = tuple(record for record in records if record["region"]["region_type"] == "boundary_ring_interval")
    observer_records = tuple(
        record
        for record in named_records
        if record["region"]["name"] in ("observer_p", "observer_q")
    )
    shared_horizon = next(record for record in named_records if record["region"]["name"] == "shared_horizon")
    low_order_erasure_witnesses = tuple(
        record
        for record in ring_records
        if record["comparisons"]["entropy_and_min_cut_visible_match"]  # type: ignore[index]
        and record["comparisons"]["erasure_visible_differs"]  # type: ignore[index]
    )
    phase_claims = {
        "same_code_parameters": first.n == second.n == 8
        and first.k == second.k == 1
        and first.distance() == second.distance() == 2,
        "shared_tensor_network_skeleton": holographic_phase1_network_spec()["bulk_logical_qubits"] == first.k,
        "all_min_cuts_computed_by_exact_internal_enumeration": all(
            int(record["min_cut"]["assignments_checked"]) == 2 for record in records  # type: ignore[index]
        ),
        "shared_min_cut_profile_certified": all(
            record["comparisons"]["min_cut_matches"] for record in records  # type: ignore[index]
        ),
        "named_boundary_entropy_profile_matches": all(
            record["comparisons"]["entropy_matches"] for record in named_records  # type: ignore[index]
        ),
        "named_boundary_entropy_and_min_cut_profiles_match": all(
            record["comparisons"]["entropy_and_min_cut_visible_match"] for record in named_records  # type: ignore[index]
        ),
        "ring_interval_entropy_profile_matches": all(
            record["comparisons"]["entropy_matches"] for record in ring_records  # type: ignore[index]
        ),
        "ring_low_order_entropy_and_min_cut_profiles_match": all(
            record["comparisons"]["entropy_and_min_cut_visible_match"] for record in ring_records  # type: ignore[index]
        ),
        "shared_horizon_algebra_matches": shared_horizon["comparisons"]["algebra_signature_matches"],  # type: ignore[index]
        "observer_reconstruction_differs": all(
            record["comparisons"]["reconstruction_visible_differs"] for record in observer_records  # type: ignore[index]
        )
        and any(record["first"]["reconstructs_all"] != record["second"]["reconstructs_all"] for record in observer_records),
        "low_order_erasure_visible_difference_exists": bool(low_order_erasure_witnesses),
    }
    phase_claims["goal_3_phase_1_tensor_network_seed_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 1: stabilizer tensor-network seed atlas",
        "status": "pass" if phase_claims["goal_3_phase_1_tensor_network_seed_certificate"] else "fail",
        "network_spec": holographic_phase1_network_spec(),
        "code_pair": {
            "source": "balanced-bridge CSS pair at m=1 embedded as an eight-boundary-qubit stabilizer tensor network",
            "first_generators": first.pauli_generators(),
            "second_generators": second.pauli_generators(),
            "n": first.n,
            "k": first.k,
            "distance": first.distance(),
        },
        "named_region_diagnostics": named_records,
        "ring_interval_diagnostics": ring_records,
        "region_diagnostics": records,
        "observer_reconstruction_witnesses": observer_records,
        "low_order_erasure_difference_witnesses": low_order_erasure_witnesses,
        "counts": {
            "boundary_qubits": first.n,
            "internal_nodes": len(holographic_phase1_network_spec()["internal_nodes"]),  # type: ignore[arg-type]
            "bulk_logical_qubits": first.k,
            "network_edges": len(holographic_phase1_network_edges()),
            "named_regions": len(named_records),
            "ring_low_order_intervals": len(ring_records),
            "regions_checked": len(records),
            "named_entropy_mismatches": sum(
                1 for record in named_records if not record["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "ring_entropy_mismatches": sum(
                1 for record in ring_records if not record["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "ring_erasure_visible_mismatches": len(low_order_erasure_witnesses),
            "observer_reconstruction_witnesses": len(observer_records),
            "low_order_erasure_difference_witnesses": len(low_order_erasure_witnesses),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The balanced-bridge separation survives a first holographic-looking tensor-network wrapper: the "
                "same boundary ring plus bulk-spoke min-cut geometry and the same selected boundary entropy data "
                "coexist with different observer-patch logical reconstruction."
            ),
            "three_geometry_lesson": (
                "Min-cut-visible and entropy-visible boundary diagnostics agree between the two realizations, but "
                "operator-algebra reconstruction differs on observer patches and erasure/fixed-point semantics "
                "already differ on a low-order boundary interval."
            ),
            "scope_warning": (
                "The ring-spoke graph is a finite diagnostic skeleton, not a physical hyperbolic geometry and not a "
                "global RT proof. Later phases should search less hand-seeded stabilizer tensor networks."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 1 gives an exact tensor-network seed certificate but reuses the balanced-bridge pair. The "
                "next adaptation should search small graph-state, CSS tensor-network, or Clifford-MERA-like network "
                "families for new pairs with matching min-cut/entropy diagnostics and differing reconstruction."
            ),
            "suggested_phase_2": (
                "Run a bounded graph-state/CSS tensor-network search over small boundary-ring and bulk-spoke "
                "skeletons, keeping exact entropy, region algebra, erasure, and min-cut checks."
            ),
        },
    }


def holographic_constraints_summary(constraints: RobustConstraints) -> dict[str, object]:
    return {
        "max_subset_size": constraints.max_subset_size,
        "min_distance": constraints.min_distance,
        "min_reconstruction_size": constraints.min_reconstruction_size,
        "forbid_single_qubit_noncentral": constraints.forbid_single_qubit_noncentral,
    }


def holographic_ring_spoke_edges(boundary_order: tuple[int, ...]) -> tuple[dict[str, object], ...]:
    ring_edges = tuple(
        {
            "left": f"q{boundary_order[index]}",
            "right": f"q{boundary_order[(index + 1) % len(boundary_order)]}",
            "capacity": 1,
            "edge_type": "boundary_ring",
        }
        for index in range(len(boundary_order))
    )
    spokes = tuple(
        {
            "left": "bulk_center",
            "right": f"q{qubit}",
            "capacity": 1,
            "edge_type": "bulk_spoke",
        }
        for qubit in sorted(boundary_order)
    )
    return ring_edges + spokes


def holographic_ring_spoke_network_spec(boundary_order: tuple[int, ...]) -> dict[str, object]:
    return {
        "network_kind": "boundary_ring_plus_bulk_spokes",
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": ("bulk_center",),
        "bulk_logical_qubits": 1,
        "edges": holographic_ring_spoke_edges(boundary_order),
        "min_cut_semantics": (
            "For a boundary region R, brute-force all internal-node assignments and minimize the unit-capacity "
            "edge cut separating boundary nodes in R from boundary nodes outside R."
        ),
    }


def holographic_ring_spoke_min_cut(
    *,
    region_mask: int,
    boundary_order: tuple[int, ...],
) -> dict[str, object]:
    spec = holographic_ring_spoke_network_spec(boundary_order)
    boundary_nodes = tuple(str(node) for node in spec["boundary_nodes"])  # type: ignore[index]
    internal_nodes = tuple(str(node) for node in spec["internal_nodes"])  # type: ignore[index]
    region_nodes = {f"q{qubit}" for qubit in mask_to_tuple(region_mask, len(boundary_order))}
    boundary_set = set(boundary_nodes)
    if not region_nodes <= boundary_set:
        raise ValueError("min-cut region contains a qubit outside the boundary")
    best_value: int | None = None
    best_assignments = []
    for assignment_bits in product((False, True), repeat=len(internal_nodes)):
        side = set(region_nodes)
        assignment = dict(zip(internal_nodes, assignment_bits))
        for node, in_region_side in assignment.items():
            if in_region_side:
                side.add(node)
        cut = 0
        for edge in spec["edges"]:  # type: ignore[index]
            left = str(edge["left"])
            right = str(edge["right"])
            if (left in side) != (right in side):
                cut += int(edge["capacity"])
        if best_value is None or cut < best_value:
            best_value = cut
            best_assignments = [assignment]
        elif cut == best_value:
            best_assignments.append(assignment)
    if best_value is None:
        raise RuntimeError("expected at least one min-cut assignment")
    return {
        "value": best_value,
        "assignments_checked": 2 ** len(internal_nodes),
        "minimizing_internal_assignments": tuple(
            tuple(sorted(assignment.items()))
            for assignment in best_assignments
        ),
    }


def holographic_canonical_ring_order(order: tuple[int, ...]) -> tuple[int, ...]:
    rotations = []
    for sequence in (order, tuple(reversed(order))):
        for index in range(len(sequence)):
            rotations.append(sequence[index:] + sequence[:index])
    return min(rotations)


def holographic_unique_ring_orders(n: int) -> tuple[tuple[int, ...], ...]:
    seen: set[tuple[int, ...]] = set()
    for order in permutations(range(n)):
        seen.add(holographic_canonical_ring_order(tuple(order)))
    return tuple(sorted(seen))


def holographic_ring_interval_regions(
    boundary_order: tuple[int, ...],
    *,
    max_length: int,
) -> tuple[dict[str, object], ...]:
    regions = []
    for length in range(1, max_length + 1):
        for start in range(len(boundary_order)):
            qubits = tuple(boundary_order[(start + offset) % len(boundary_order)] for offset in range(length))
            regions.append(
                {
                    "name": f"ring_interval_start{start}_len{length}",
                    "region_type": "boundary_ring_interval",
                    "start": start,
                    "length": length,
                    "qubits": qubits,
                    "mask": mask_from_qubits(qubits),
                }
            )
    return tuple(regions)


def holographic_phase2_region_diagnostic(
    *,
    code: StabilizerCode,
    region: dict[str, object],
    boundary_order: tuple[int, ...],
) -> dict[str, object]:
    region_mask = int(region["mask"])
    full = (1 << code.n) - 1
    algebra = code.region_algebra(region_mask)
    return {
        "entropy": code.entropy(region_mask),
        "min_cut": holographic_ring_spoke_min_cut(region_mask=region_mask, boundary_order=boundary_order),
        "algebra_signature": algebra.signature(),
        "reconstructs_all": algebra.reconstructs_all,
        "erasure_correctable": code.erasure_correctable(region_mask),
        "survivor_fixed_point_reconstructs_all": code.reconstructs_all_logicals(full ^ region_mask),
    }


def holographic_phase2_pair_region_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region: dict[str, object],
    boundary_order: tuple[int, ...],
) -> dict[str, object]:
    first_diag = holographic_phase2_region_diagnostic(code=first, region=region, boundary_order=boundary_order)
    second_diag = holographic_phase2_region_diagnostic(code=second, region=region, boundary_order=boundary_order)
    entropy_matches = int(first_diag["entropy"]) == int(second_diag["entropy"])
    min_cut_matches = first_diag["min_cut"] == second_diag["min_cut"]
    algebra_matches = first_diag["algebra_signature"] == second_diag["algebra_signature"]
    erasure_matches = bool(first_diag["erasure_correctable"]) == bool(second_diag["erasure_correctable"])
    survivor_matches = bool(first_diag["survivor_fixed_point_reconstructs_all"]) == bool(
        second_diag["survivor_fixed_point_reconstructs_all"]
    )
    return {
        "region": {key: value for key, value in region.items() if key != "mask"},
        "min_cut": first_diag["min_cut"],
        "first": first_diag,
        "second": second_diag,
        "comparisons": {
            "entropy_matches": entropy_matches,
            "min_cut_matches": min_cut_matches,
            "algebra_signature_matches": algebra_matches,
            "erasure_correctability_matches": erasure_matches,
            "survivor_fixed_point_matches": survivor_matches,
            "entropy_and_min_cut_visible_match": entropy_matches and min_cut_matches,
            "reconstruction_visible_differs": not algebra_matches,
            "erasure_visible_differs": not erasure_matches or not survivor_matches,
        },
    }


def holographic_phase2_strict_source_scan_reports() -> tuple[dict[str, object], ...]:
    constraints = RobustConstraints()
    configs = (
        {"source": "css", "n": 5, "max_codes": 500, "encoder_depth": 1},
        {"source": "cyclic-css", "n": 5, "max_codes": 500, "encoder_depth": 1},
        {"source": "graph", "n": 5, "max_codes": 80, "encoder_depth": 1},
        {"source": "encoder", "n": 5, "max_codes": 80, "encoder_depth": 2},
    )
    reports = []
    for config in configs:
        scan = scan_robust_source(
            n=int(config["n"]),
            k=1,
            source=str(config["source"]),
            equivalence="permutation",
            entropy_key_mode="labeled",
            constraints=constraints,
            max_codes=int(config["max_codes"]),
            encoder_depth=int(config["encoder_depth"]),
        )
        reports.append(
            {
                "source": scan.source,
                "n": scan.n,
                "k": scan.k,
                "equivalence": scan.equivalence,
                "entropy_key_mode": scan.entropy_key_mode,
                "constraints": holographic_constraints_summary(scan.constraints),
                "max_codes": int(config["max_codes"]),
                "encoder_depth": int(config["encoder_depth"]),
                "raw_codes": scan.raw_codes,
                "codes_checked": scan.codes_checked,
                "entropy_classes": scan.entropy_classes,
                "pair_found": scan.pair is not None,
                "status": scan.status,
                "exhausted_before_code_cap": scan.raw_codes < int(config["max_codes"]),
            }
        )
    return tuple(reports)


def holographic_phase2_ring_order_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    boundary_order: tuple[int, ...],
    max_interval_length: int,
) -> dict[str, object]:
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    records = tuple(
        holographic_phase2_pair_region_record(
            first=first,
            second=second,
            region=region,
            boundary_order=boundary_order,
        )
        for region in intervals
    )
    interval_witnesses = tuple(
        record
        for record in records
        if int(record["region"]["length"]) >= 2  # type: ignore[index]
        and record["comparisons"]["entropy_and_min_cut_visible_match"]  # type: ignore[index]
        and record["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
    )
    erasure_witnesses = tuple(
        record
        for record in records
        if int(record["region"]["length"]) >= 2  # type: ignore[index]
        and record["comparisons"]["entropy_and_min_cut_visible_match"]  # type: ignore[index]
        and record["comparisons"]["erasure_visible_differs"]  # type: ignore[index]
    )
    entropy_matches = all(record["comparisons"]["entropy_matches"] for record in records)  # type: ignore[index]
    min_cut_matches = all(record["comparisons"]["min_cut_matches"] for record in records)  # type: ignore[index]
    return {
        "boundary_order": boundary_order,
        "network_spec": holographic_ring_spoke_network_spec(boundary_order),
        "interval_diagnostics": records,
        "interval_reconstruction_witnesses": interval_witnesses,
        "interval_erasure_witnesses": erasure_witnesses,
        "summary": {
            "intervals_checked": len(records),
            "entropy_mismatches": sum(
                1 for record in records if not record["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "min_cut_mismatches": sum(
                1 for record in records if not record["comparisons"]["min_cut_matches"]  # type: ignore[index]
            ),
            "length_at_least_2_reconstruction_witnesses": len(interval_witnesses),
            "length_at_least_2_erasure_witnesses": len(erasure_witnesses),
            "ring_interval_entropy_profile_matches": entropy_matches,
            "ring_spoke_min_cut_profile_shared": min_cut_matches,
            "ring_atlas_hit": entropy_matches and min_cut_matches and bool(interval_witnesses),
        },
    }


def bridge_holography_phase2_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 2,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 2:
        raise ValueError("max_interval_length must be at least two")
    strict_scans = holographic_phase2_strict_source_scan_reports()
    graph_search = graph_labeled_pair_source(n=5, k=1, max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected relaxed graph/CWS source search to find a pair")
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("relaxed graph/CWS source must contain StabilizerCode objects")

    ring_orders = holographic_unique_ring_orders(first.n)
    ring_records = tuple(
        holographic_phase2_ring_order_record(
            first=first,
            second=second,
            boundary_order=order,
            max_interval_length=max_interval_length,
        )
        for order in ring_orders
    )
    hit_records = tuple(record for record in ring_records if record["summary"]["ring_atlas_hit"])  # type: ignore[index]
    selected_hit = hit_records[0] if hit_records else None
    expected_ring_orders = factorial(first.n - 1) // 2 if first.n > 2 else 1
    public_graph_search = {key: value for key, value in graph_search.items() if key != "source"}
    source_summary = graph_search["source_summary"]
    first_quality = source_summary["first_quality"] if isinstance(source_summary, dict) else {}
    second_quality = source_summary["second_quality"] if isinstance(source_summary, dict) else {}
    strict_no_pair = all(scan["status"] == "no-pair" and not scan["pair_found"] for scan in strict_scans)
    strict_exhausted = all(scan["exhausted_before_code_cap"] for scan in strict_scans)
    selected_witnesses = () if selected_hit is None else selected_hit["interval_reconstruction_witnesses"]
    phase_claims = {
        "strict_source_menu_scanned": len(strict_scans) == 4,
        "strict_source_menu_no_pair": strict_no_pair,
        "strict_source_scans_exhausted_under_bounds": strict_exhausted,
        "relaxed_graph_pair_found": graph_search["status"] == "pair-found",
        "relaxed_graph_pair_same_labeled_t2_entropy": bool(
            isinstance(source_summary, dict) and source_summary["same_labeled_t2_entropy"]
        ),
        "relaxed_graph_pair_reconstruction_profiles_differ": bool(
            isinstance(source_summary, dict) and source_summary["reconstruction_profiles_differ"]
        ),
        "distance_one_caveat_certified": first.distance() == second.distance() == 1
        and first_quality.get("passes") is False
        and second_quality.get("passes") is False,
        "ring_orders_exhaustively_checked_mod_dihedral": len(ring_orders) == expected_ring_orders,
        "ring_interval_entropy_profile_match_found": bool(hit_records),
        "ring_spoke_min_cut_profile_shared_on_hit": bool(
            selected_hit is not None and selected_hit["summary"]["ring_spoke_min_cut_profile_shared"]  # type: ignore[index]
        ),
        "reconstruction_visible_ring_interval_witness_exists": bool(selected_witnesses),
    }
    phase_claims["goal_3_phase_2_bounded_graph_cws_ring_atlas_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 2: bounded graph/CWS ring-spoke atlas search",
        "status": "pass" if phase_claims["goal_3_phase_2_bounded_graph_cws_ring_atlas_certificate"] else "fail",
        "strict_source_menu": {
            "scope": (
                "exact finite scans over n=5 k=1 CSS, cyclic-CSS, graph-subspace, and depth-2 encoder menus "
                "under robust labeled-t2 entropy/reconstruction constraints"
            ),
            "scan_reports": strict_scans,
        },
        "relaxed_graph_search": public_graph_search,
        "relaxed_graph_code_pair": {
            "source_type": source["source_type"],
            "n": first.n,
            "k": first.k,
            "first_distance": first.distance(),
            "second_distance": second.distance(),
            "first_generators": first.pauli_generators(),
            "second_generators": second.pauli_generators(),
        },
        "ring_atlas_search": {
            "ring_equivalence": "boundary orders modulo rotation and reversal",
            "max_interval_length": max_interval_length,
            "ring_orders_checked": len(ring_records),
            "ring_order_summaries": tuple(
                {
                    "boundary_order": record["boundary_order"],
                    "summary": record["summary"],
                    "first_reconstruction_witness": (
                        record["interval_reconstruction_witnesses"][0]
                        if record["interval_reconstruction_witnesses"]
                        else None
                    ),
                }
                for record in ring_records
            ),
            "selected_hit": selected_hit,
        },
        "counts": {
            "strict_source_scans": len(strict_scans),
            "strict_source_no_pair_scans": sum(1 for scan in strict_scans if scan["status"] == "no-pair"),
            "strict_source_exhausted_scans": sum(1 for scan in strict_scans if scan["exhausted_before_code_cap"]),
            "relaxed_graph_raw_codes": graph_search["scan"]["raw_codes"],  # type: ignore[index]
            "relaxed_graph_codes_checked": graph_search["scan"]["codes_checked"],  # type: ignore[index]
            "ring_orders_checked": len(ring_records),
            "expected_ring_orders_mod_dihedral": expected_ring_orders,
            "ring_orders_with_hits": len(hit_records),
            "selected_hit_interval_witnesses": len(selected_witnesses),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The strict robust n=5 source menu finds no labeled-t2 entropy/reconstruction-discordant pair, but a "
                "relaxed graph/CWS subspace scan finds a distance-one frontier pair. On a ring-spoke boundary atlas, "
                "all length-one and length-two interval entropies and min-cuts match, while a length-two interval "
                "has different operator-algebra reconstruction."
            ),
            "three_geometry_lesson": (
                "The same min-cut-visible ring-spoke skeleton and the same low-order entropy-visible geometry do "
                "not determine reconstruction-visible geometry, even in a graph/CWS-derived tensor-network-like "
                "source. The caveat is that this witness is not distance-repaired."
            ),
            "scope_warning": (
                "This is exact for the stated finite source menus and all n=5 ring orders modulo dihedral symmetry. "
                "It is not a robust holographic code theorem because the accepted graph/CWS witness has distance one."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 2 supplies a less hand-seeded graph/CWS ring-atlas witness but certifies that the robust "
                "source menu has no such pair at this size. The natural adaptation is to repair or concatenate the "
                "graph/CWS ring witness, then replay the same ring-spoke min-cut, entropy, algebra, erasure, and "
                "survivor checks."
            ),
            "suggested_phase_3": (
                "Run exact distance-repair or small concatenation transforms on the Phase 2 graph/CWS ring witness "
                "and search for a ring-spoke atlas that preserves the entropy/min-cut match while keeping a "
                "reconstruction-visible difference."
            ),
        },
    }


def holographic_phase3_low_order_entropy_match(
    first: StabilizerCode,
    second: StabilizerCode,
    *,
    max_subset_size: int = 2,
) -> dict[str, object]:
    mismatches = []
    checked = 0
    for size in range(max_subset_size + 1):
        for qubits in combinations(range(first.n), size):
            checked += 1
            mask = mask_from_qubits(qubits)
            first_entropy = first.entropy(mask)
            second_entropy = second.entropy(mask)
            if first_entropy != second_entropy:
                mismatches.append(
                    {
                        "qubits": qubits,
                        "first_entropy": first_entropy,
                        "second_entropy": second_entropy,
                    }
                )
    return {
        "max_subset_size": max_subset_size,
        "subsets_checked": checked,
        "mismatch_count": len(mismatches),
        "mismatches": tuple(mismatches),
        "matches": not mismatches,
    }


def holographic_phase3_phase2_source(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    graph_search = graph_labeled_pair_source(n=5, k=1, max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 2 source must contain StabilizerCode objects")
    return graph_search


def holographic_phase3_repaired_source(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 2 source must contain StabilizerCode objects")
    outer = phase11_outer_distance_repair_code()
    repaired_first, first_metadata = logical_concatenate_k1(first, outer)
    repaired_second, second_metadata = logical_concatenate_k1(second, outer)
    return {
        "name": "goal3_phase3_graph_cws_ring_witness_distance_repair",
        "source_type": "logical_concatenation_distance_repair",
        "origin": (
            "Goal 3 Phase 2 graph/CWS ring-spoke witness concatenated with the four-qubit distance-2 outer code"
        ),
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "outer_code": {
            "n": outer.n,
            "k": outer.k,
            "distance": outer.distance(),
            "generators": outer.pauli_generators(),
        },
        "first": repaired_first,
        "second": repaired_second,
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
    }


def holographic_phase3_boundary_order_templates() -> tuple[dict[str, object], ...]:
    inner_order = (0, 1, 2, 4, 3)
    block_size = 5
    block_count = 4
    block_contiguous = tuple(block * block_size + qubit for block in range(block_count) for qubit in inner_order)
    inner_interleaved = tuple(block * block_size + qubit for qubit in inner_order for block in range(block_count))
    witness_strip_prefix = tuple(
        block * block_size + qubit
        for block in range(block_count)
        for qubit in (2, 4)
    )
    witness_set = set(witness_strip_prefix)
    witness_strip = witness_strip_prefix + tuple(qubit for qubit in block_contiguous if qubit not in witness_set)
    return (
        {
            "name": "block_contiguous_phase2_ring",
            "description": "Repeat the Phase 2 boundary ring order inside each outer-code block.",
            "boundary_order": block_contiguous,
        },
        {
            "name": "inner_position_interleaved_ring",
            "description": "Interleave outer-code blocks at each Phase 2 inner ring position.",
            "boundary_order": inner_interleaved,
        },
        {
            "name": "source_aware_witness_strip_ring",
            "description": "Place the repaired lifted Phase 2 witness strip first, then append the remaining block-contiguous order.",
            "boundary_order": witness_strip,
        },
    )


def holographic_phase3_interval_location(
    *,
    boundary_order: tuple[int, ...],
    region_mask: int,
) -> dict[str, object]:
    qubits = set(mask_to_tuple(region_mask, len(boundary_order)))
    length = len(qubits)
    for start in range(len(boundary_order)):
        interval = tuple(boundary_order[(start + offset) % len(boundary_order)] for offset in range(length))
        if set(interval) == qubits:
            return {
                "is_boundary_ring_interval": True,
                "start": start,
                "length": length,
                "interval_qubits": interval,
            }
    return {
        "is_boundary_ring_interval": False,
        "start": None,
        "length": length,
        "interval_qubits": None,
    }


def holographic_phase3_template_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    template: dict[str, object],
    max_interval_length: int,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    records = []
    for region in intervals:
        region_mask = int(region["mask"])
        first_entropy = first.entropy(region_mask)
        second_entropy = second.entropy(region_mask)
        min_cut = holographic_ring_spoke_min_cut(region_mask=region_mask, boundary_order=boundary_order)
        records.append(
            {
                "region": {key: value for key, value in region.items() if key != "mask"},
                "min_cut": min_cut,
                "first_entropy": first_entropy,
                "second_entropy": second_entropy,
                "comparisons": {
                    "entropy_matches": first_entropy == second_entropy,
                    "min_cut_profile_shared": True,
                    "entropy_and_min_cut_visible_match": first_entropy == second_entropy,
                },
            }
        )
    interval_records = tuple(records)
    entropy_matches = all(record["comparisons"]["entropy_matches"] for record in interval_records)  # type: ignore[index]
    min_cut_matches = all(record["comparisons"]["min_cut_profile_shared"] for record in interval_records)  # type: ignore[index]
    return {
        "name": template["name"],
        "description": template["description"],
        "boundary_order": boundary_order,
        "network_spec": holographic_ring_spoke_network_spec(boundary_order),
        "ring_interval_diagnostics": interval_records,
        "summary": {
            "intervals_checked": len(interval_records),
            "entropy_mismatches": sum(
                1 for record in interval_records if not record["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "min_cut_mismatches": sum(
                1 for record in interval_records if not record["comparisons"]["min_cut_profile_shared"]  # type: ignore[index]
            ),
            "ring_interval_entropy_profile_matches": entropy_matches,
            "ring_spoke_min_cut_profile_shared": min_cut_matches,
        },
    }


def holographic_phase3_lifted_witness_records(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    boundary_order: tuple[int, ...],
    selected_block_mask: int = 3,
) -> tuple[dict[str, object], ...]:
    base_inner_region = mask_from_qubits((2, 4))
    full = (1 << first.n) - 1
    records = []
    for block_mask in range(1, 1 << 4):
        region_mask = lift_inner_region_over_blocks(
            base_inner_region,
            block_mask=block_mask,
            block_size=5,
            block_count=4,
        )
        qubits = mask_to_tuple(region_mask, first.n)
        region = {
            "name": f"lifted_phase2_interval_24_blocks_{block_mask}",
            "region_type": "lifted_phase2_ring_interval",
            "base_inner_qubits": (2, 4),
            "block_mask": block_mask,
            "block_count": block_mask.bit_count(),
            "qubits": qubits,
            "mask": region_mask,
        }
        first_entropy = first.entropy(region_mask)
        second_entropy = second.entropy(region_mask)
        min_cut = holographic_ring_spoke_min_cut(region_mask=region_mask, boundary_order=boundary_order)
        entropy_matches = first_entropy == second_entropy
        first_diag: dict[str, object] = {
            "entropy": first_entropy,
            "min_cut": min_cut,
        }
        second_diag: dict[str, object] = {
            "entropy": second_entropy,
            "min_cut": min_cut,
        }
        algebra_matches = None
        erasure_matches = None
        survivor_matches = None
        if entropy_matches:
            first_algebra = first.region_algebra(region_mask)
            second_algebra = second.region_algebra(region_mask)
            first_erasure = first.erasure_correctable(region_mask)
            second_erasure = second.erasure_correctable(region_mask)
            algebra_matches = first_algebra.signature() == second_algebra.signature()
            erasure_matches = first_erasure == second_erasure
            first_diag.update(
                {
                    "algebra_signature": first_algebra.signature(),
                    "reconstructs_all": first_algebra.reconstructs_all,
                    "erasure_correctable": first_erasure,
                }
            )
            second_diag.update(
                {
                    "algebra_signature": second_algebra.signature(),
                    "reconstructs_all": second_algebra.reconstructs_all,
                    "erasure_correctable": second_erasure,
                }
            )
            if block_mask == selected_block_mask:
                first_survivor = first.reconstructs_all_logicals(full ^ region_mask)
                second_survivor = second.reconstructs_all_logicals(full ^ region_mask)
                survivor_matches = first_survivor == second_survivor
                first_diag["survivor_fixed_point_reconstructs_all"] = first_survivor
                second_diag["survivor_fixed_point_reconstructs_all"] = second_survivor
        record = {
            "region": {key: value for key, value in region.items() if key != "mask"},
            "min_cut": min_cut,
            "first": first_diag,
            "second": second_diag,
            "comparisons": {
                "entropy_matches": entropy_matches,
                "min_cut_matches": True,
                "algebra_signature_matches": algebra_matches,
                "erasure_correctability_matches": erasure_matches,
                "survivor_fixed_point_matches": survivor_matches,
                "entropy_and_min_cut_visible_match": entropy_matches,
                "reconstruction_visible_differs": algebra_matches is False,
                "erasure_visible_differs": erasure_matches is False or survivor_matches is False,
            },
        }
        record["interval_location"] = holographic_phase3_interval_location(
            boundary_order=boundary_order,
            region_mask=region_mask,
        )
        records.append(record)
    return tuple(records)


def bridge_holography_phase3_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 2,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 2:
        raise ValueError("max_interval_length must be at least two")
    repaired_source = holographic_phase3_repaired_source(graph_max_codes=graph_max_codes)
    first = repaired_source["first"]
    second = repaired_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 3 repaired source must contain StabilizerCode objects")
    first_distance = bounded_distance_certificate(first, max_weight=1)
    second_distance = bounded_distance_certificate(second, max_weight=1)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    templates = tuple(
        holographic_phase3_template_record(
            first=first,
            second=second,
            template=template,
            max_interval_length=max_interval_length,
        )
        for template in holographic_phase3_boundary_order_templates()
    )
    selected_template = next(template for template in templates if template["name"] == "source_aware_witness_strip_ring")
    selected_boundary_order = tuple(int(qubit) for qubit in selected_template["boundary_order"])  # type: ignore[index]
    lifted_records = holographic_phase3_lifted_witness_records(
        first=first,
        second=second,
        boundary_order=selected_boundary_order,
    )
    single_block_collapses = tuple(
        record
        for record in lifted_records
        if int(record["region"]["block_count"]) == 1  # type: ignore[index]
        and record["comparisons"]["algebra_signature_matches"]  # type: ignore[index]
        and record["comparisons"]["erasure_correctability_matches"]  # type: ignore[index]
    )
    accepted_two_block_hits = tuple(
        record
        for record in lifted_records
        if int(record["region"]["block_count"]) == 2  # type: ignore[index]
        and record["comparisons"]["entropy_and_min_cut_visible_match"]  # type: ignore[index]
        and record["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
        and record["comparisons"]["erasure_visible_differs"]  # type: ignore[index]
    )
    entropy_gate_rejections = tuple(
        record
        for record in lifted_records
        if not record["comparisons"]["entropy_matches"]  # type: ignore[index]
    )
    selected_witness = next(
        record
        for record in accepted_two_block_hits
        if int(record["region"]["block_mask"]) == 3  # type: ignore[index]
    )
    all_template_low_order_matches = all(
        template["summary"]["ring_interval_entropy_profile_matches"]  # type: ignore[index]
        and template["summary"]["ring_spoke_min_cut_profile_shared"]  # type: ignore[index]
        for template in templates
    )
    phase_claims = {
        "phase2_graph_source_loaded": repaired_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "outer_code_distance_2": repaired_source["outer_code"]["distance"] == 2,  # type: ignore[index]
        "logical_concatenation_k1": first.k == 1 and second.k == 1,
        "distance_at_least_2_after_repair_certified": bool(first_distance["distance_at_least_2_certified"])
        and bool(second_distance["distance_at_least_2_certified"]),
        "all_labeled_t2_entropy_matches_after_repair": low_order_entropy["matches"],
        "source_aware_ring_templates_scored": len(templates) == 3,
        "all_template_low_order_entropy_and_min_cut_profiles_match": all_template_low_order_matches,
        "single_block_lift_collapses_original_witness": len(single_block_collapses) == 4,
        "two_block_lifted_reconstruction_and_erasure_witnesses_exist": len(accepted_two_block_hits) == 6,
        "large_lifts_rejected_by_entropy_gate": len(entropy_gate_rejections) == 5,
        "selected_witness_is_boundary_ring_interval": selected_witness["interval_location"]["is_boundary_ring_interval"],  # type: ignore[index]
        "selected_witness_survivor_fixed_point_differs": (
            selected_witness["comparisons"]["survivor_fixed_point_matches"] is False  # type: ignore[index]
        ),
    }
    phase_claims["goal_3_phase_3_distance_repaired_lifted_ring_atlas_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 3: distance-repaired lifted graph/CWS ring-spoke atlas",
        "status": "pass" if phase_claims["goal_3_phase_3_distance_repaired_lifted_ring_atlas_certificate"] else "fail",
        "repair_source": {
            key: value
            for key, value in repaired_source.items()
            if key not in ("first", "second")
        },
        "repaired_code_pair": {
            "n": first.n,
            "k": first.k,
            "first_generators": first.pauli_generators(),
            "second_generators": second.pauli_generators(),
        },
        "distance_repair": {
            "method": "logical concatenation with the four-qubit distance-2 outer code",
            "first": first_distance,
            "second": second_distance,
            "distance_at_least_2_for_both": phase_claims["distance_at_least_2_after_repair_certified"],
        },
        "low_order_entropy": low_order_entropy,
        "ring_template_search": {
            "scope": "three source-aware repaired boundary orders with all length-one and length-two ring intervals checked",
            "max_interval_length": max_interval_length,
            "templates": templates,
            "selected_template": selected_template["name"],
        },
        "lifted_phase2_witness_audit": {
            "base_inner_qubits": (2, 4),
            "block_masks_checked": len(lifted_records),
            "records": lifted_records,
            "single_block_collapses": single_block_collapses,
            "accepted_two_block_hits": accepted_two_block_hits,
            "entropy_gate_rejections": entropy_gate_rejections,
            "selected_witness": selected_witness,
        },
        "counts": {
            "low_order_subsets_checked": low_order_entropy["subsets_checked"],
            "low_order_entropy_mismatches": low_order_entropy["mismatch_count"],
            "ring_templates": len(templates),
            "ring_template_intervals_checked": sum(template["summary"]["intervals_checked"] for template in templates),  # type: ignore[index]
            "lifted_block_masks_checked": len(lifted_records),
            "single_block_collapses": len(single_block_collapses),
            "accepted_two_block_hits": len(accepted_two_block_hits),
            "entropy_gate_rejections": len(entropy_gate_rejections),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The Phase 2 graph/CWS ring witness can be distance-repaired to remove all weight-one logicals while "
                "preserving labeled t<=2 entropy matching. The original single-block interval witness collapses, but "
                "two-block lifts of the same inner interval recover reconstruction-visible and erasure-visible "
                "separation under a source-aware repaired ring-spoke atlas."
            ),
            "three_geometry_lesson": (
                "After repair, entropy/min-cut-visible geometry matches on low-order ring intervals, while the lifted "
                "two-block witness separates operator algebra, erasure correctability, and survivor fixed points. "
                "This is a stronger holographic-code cousin of Phase 2 because channel-visible geometry now splits."
            ),
            "scope_warning": (
                "The distance claim is d>=2 from exact weight-one logical exclusion, not an exact full-distance "
                "computation. The ring atlas is source-aware and checked over a bounded template set, not all "
                "20-qubit boundary orders."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 3 repairs the distance-one weakness and recovers both reconstruction and erasure separation, "
                "but the successful atlas is source-aware. The next adaptation should test whether less source-aware "
                "hyperbolic, HaPPY-like, or Clifford-MERA-like layouts recover comparable witnesses."
            ),
            "suggested_phase_4": (
                "Search small stabilizer tensor-network layouts with multiple internal nodes and exact min-cut "
                "enumeration, comparing source-aware witness-strip layouts against more geometric ring/tiling "
                "orders under the same diagnostics."
            ),
        },
    }


def holographic_phase4_boundary_order_templates() -> tuple[dict[str, object], ...]:
    phase3_templates = {template["name"]: template for template in holographic_phase3_boundary_order_templates()}
    return (
        {
            "name": "natural_block_order",
            "template_kind": "less_source_aware",
            "description": "Use the raw repaired-code qubit order, block by block.",
            "boundary_order": tuple(range(20)),
        },
        {
            **phase3_templates["block_contiguous_phase2_ring"],
            "template_kind": "less_source_aware",
        },
        {
            **phase3_templates["inner_position_interleaved_ring"],
            "template_kind": "less_source_aware",
        },
        {
            **phase3_templates["source_aware_witness_strip_ring"],
            "template_kind": "source_aware",
        },
    )


def holographic_phase4_edge(
    left: str,
    right: str,
    *,
    edge_type: str,
    capacity: int = 1,
) -> dict[str, object]:
    return {
        "left": left,
        "right": right,
        "capacity": capacity,
        "edge_type": edge_type,
    }


def holographic_phase4_boundary_ring_edges(boundary_order: tuple[int, ...]) -> tuple[dict[str, object], ...]:
    return tuple(
        holographic_phase4_edge(
            f"q{boundary_order[index]}",
            f"q{boundary_order[(index + 1) % len(boundary_order)]}",
            edge_type="boundary_ring",
        )
        for index in range(len(boundary_order))
    )


def holographic_phase4_network_specs(boundary_order: tuple[int, ...]) -> tuple[dict[str, object], ...]:
    ring_edges = holographic_phase4_boundary_ring_edges(boundary_order)
    ring_spoke_edges = ring_edges + tuple(
        holographic_phase4_edge("bulk_center", f"q{qubit}", edge_type="bulk_spoke")
        for qubit in sorted(boundary_order)
    )

    block_nodes = tuple(f"bulk_block_{block}" for block in range(4))
    block_edges = list(ring_edges)
    for block in range(4):
        for inner_qubit in range(5):
            block_edges.append(
                holographic_phase4_edge(
                    f"bulk_block_{block}",
                    f"q{block * 5 + inner_qubit}",
                    edge_type="block_spoke",
                )
            )
    for block in range(3):
        block_edges.append(
            holographic_phase4_edge(
                f"bulk_block_{block}",
                f"bulk_block_{block + 1}",
                edge_type="outer_block_path",
                capacity=2,
            )
        )

    inner_order = (0, 1, 2, 4, 3)
    inner_nodes = tuple(f"bulk_inner_{inner}" for inner in inner_order)
    inner_edges = list(ring_edges)
    for inner_qubit in inner_order:
        for block in range(4):
            inner_edges.append(
                holographic_phase4_edge(
                    f"bulk_inner_{inner_qubit}",
                    f"q{block * 5 + inner_qubit}",
                    edge_type="inner_position_spoke",
                )
            )
    for index, inner_qubit in enumerate(inner_order):
        inner_edges.append(
            holographic_phase4_edge(
                f"bulk_inner_{inner_qubit}",
                f"bulk_inner_{inner_order[(index + 1) % len(inner_order)]}",
                edge_type="inner_position_cycle",
                capacity=2,
            )
        )

    tree_nodes = ("bulk_left", "bulk_right", "bulk_root")
    tree_edges = list(ring_edges)
    for block in (0, 1):
        for inner_qubit in range(5):
            tree_edges.append(
                holographic_phase4_edge(
                    "bulk_left",
                    f"q{block * 5 + inner_qubit}",
                    edge_type="binary_tree_left_spoke",
                )
            )
    for block in (2, 3):
        for inner_qubit in range(5):
            tree_edges.append(
                holographic_phase4_edge(
                    "bulk_right",
                    f"q{block * 5 + inner_qubit}",
                    edge_type="binary_tree_right_spoke",
                )
            )
    tree_edges += [
        holographic_phase4_edge("bulk_root", "bulk_left", edge_type="binary_tree_internal", capacity=2),
        holographic_phase4_edge("bulk_root", "bulk_right", edge_type="binary_tree_internal", capacity=2),
    ]

    return (
        {
            "name": "single_bulk_ring_spoke",
            "network_kind": "one_bulk_node_ring_spoke",
            "description": "One central bulk node with spokes to every boundary qubit.",
            "boundary_order": boundary_order,
            "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
            "internal_nodes": ("bulk_center",),
            "edges": ring_spoke_edges,
        },
        {
            "name": "outer_block_bulk_path",
            "network_kind": "four_block_bulk_path",
            "description": "One bulk node per outer-code block, connected by a path.",
            "boundary_order": boundary_order,
            "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
            "internal_nodes": block_nodes,
            "edges": tuple(block_edges),
        },
        {
            "name": "inner_position_bulk_cycle",
            "network_kind": "five_inner_position_bulk_cycle",
            "description": "One bulk node per Phase 2 inner ring position, connected in a cycle.",
            "boundary_order": boundary_order,
            "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
            "internal_nodes": inner_nodes,
            "edges": tuple(inner_edges),
        },
        {
            "name": "binary_outer_tree",
            "network_kind": "binary_outer_block_tree",
            "description": "Two outer-block lobes joined through a root bulk node.",
            "boundary_order": boundary_order,
            "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
            "internal_nodes": tree_nodes,
            "edges": tuple(tree_edges),
        },
    )


def holographic_network_min_cut(
    *,
    network_spec: dict[str, object],
    region_mask: int,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in network_spec["boundary_order"])  # type: ignore[index]
    boundary_nodes = tuple(str(node) for node in network_spec["boundary_nodes"])  # type: ignore[index]
    internal_nodes = tuple(str(node) for node in network_spec["internal_nodes"])  # type: ignore[index]
    region_nodes = {f"q{qubit}" for qubit in mask_to_tuple(region_mask, len(boundary_order))}
    boundary_set = set(boundary_nodes)
    if not region_nodes <= boundary_set:
        raise ValueError("min-cut region contains a qubit outside the boundary")
    best_value: int | None = None
    best_assignments = []
    for assignment_bits in product((False, True), repeat=len(internal_nodes)):
        side = set(region_nodes)
        assignment = dict(zip(internal_nodes, assignment_bits))
        for node, in_region_side in assignment.items():
            if in_region_side:
                side.add(node)
        cut = 0
        for edge in network_spec["edges"]:  # type: ignore[index]
            left = str(edge["left"])
            right = str(edge["right"])
            if (left in side) != (right in side):
                cut += int(edge["capacity"])
        if best_value is None or cut < best_value:
            best_value = cut
            best_assignments = [assignment]
        elif cut == best_value:
            best_assignments.append(assignment)
    if best_value is None:
        raise RuntimeError("expected at least one min-cut assignment")
    return {
        "value": best_value,
        "assignments_checked": 2 ** len(internal_nodes),
        "internal_nodes": len(internal_nodes),
        "minimizing_internal_assignments": tuple(
            tuple(sorted(assignment.items()))
            for assignment in best_assignments
        ),
    }


def holographic_phase4_minimal_interval_cover(
    *,
    boundary_order: tuple[int, ...],
    region_mask: int,
) -> dict[str, object]:
    region = set(mask_to_tuple(region_mask, len(boundary_order)))
    region_size = len(region)
    strict_location = holographic_phase3_interval_location(boundary_order=boundary_order, region_mask=region_mask)
    for length in range(region_size, len(boundary_order) + 1):
        for start in range(len(boundary_order)):
            interval = tuple(boundary_order[(start + offset) % len(boundary_order)] for offset in range(length))
            if region <= set(interval):
                return {
                    "region_size": region_size,
                    "minimal_cover_length": length,
                    "excess_boundary_sites": length - region_size,
                    "start": start,
                    "cover_qubits": interval,
                    "is_strict_boundary_interval": strict_location["is_boundary_ring_interval"],
                    "strict_interval_location": strict_location,
                }
    raise RuntimeError("the full boundary should cover every region")


def holographic_phase4_selected_witness_diagnostic(
    first: StabilizerCode,
    second: StabilizerCode,
    *,
    region_mask: int,
) -> dict[str, object]:
    full = (1 << first.n) - 1
    first_algebra = first.region_algebra(region_mask)
    second_algebra = second.region_algebra(region_mask)
    first_erasure = first.erasure_correctable(region_mask)
    second_erasure = second.erasure_correctable(region_mask)
    first_survivor = first.reconstructs_all_logicals(full ^ region_mask)
    second_survivor = second.reconstructs_all_logicals(full ^ region_mask)
    return {
        "region": {
            "name": "phase3_selected_two_block_lift",
            "qubits": mask_to_tuple(region_mask, first.n),
            "block_mask": 3,
            "base_inner_qubits": (2, 4),
        },
        "first": {
            "entropy": first.entropy(region_mask),
            "algebra_signature": first_algebra.signature(),
            "erasure_correctable": first_erasure,
            "survivor_fixed_point_reconstructs_all": first_survivor,
        },
        "second": {
            "entropy": second.entropy(region_mask),
            "algebra_signature": second_algebra.signature(),
            "erasure_correctable": second_erasure,
            "survivor_fixed_point_reconstructs_all": second_survivor,
        },
        "comparisons": {
            "entropy_matches": first.entropy(region_mask) == second.entropy(region_mask),
            "reconstruction_visible_differs": first_algebra.signature() != second_algebra.signature(),
            "erasure_correctability_differs": first_erasure != second_erasure,
            "survivor_fixed_point_differs": first_survivor != second_survivor,
            "channel_visible_differs": first_erasure != second_erasure and first_survivor != second_survivor,
        },
    }


def holographic_phase4_layout_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    boundary_template: dict[str, object],
    network_spec: dict[str, object],
    selected_region_mask: int,
    selected_witness: dict[str, object],
    max_interval_length: int,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in boundary_template["boundary_order"])  # type: ignore[index]
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    interval_records = []
    for region in intervals:
        region_mask = int(region["mask"])
        first_entropy = first.entropy(region_mask)
        second_entropy = second.entropy(region_mask)
        min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
        interval_records.append(
            {
                "region": {key: value for key, value in region.items() if key != "mask"},
                "first_entropy": first_entropy,
                "second_entropy": second_entropy,
                "min_cut": min_cut,
                "comparisons": {
                    "entropy_matches": first_entropy == second_entropy,
                    "min_cut_exact": min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
                    "entropy_and_min_cut_visible_match": first_entropy == second_entropy,
                },
            }
        )
    interval_records_tuple = tuple(interval_records)
    selected_min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=selected_region_mask)
    interval_cover = holographic_phase4_minimal_interval_cover(
        boundary_order=boundary_order,
        region_mask=selected_region_mask,
    )
    entropy_matches = all(record["comparisons"]["entropy_matches"] for record in interval_records_tuple)  # type: ignore[index]
    min_cuts_exact = all(record["comparisons"]["min_cut_exact"] for record in interval_records_tuple)  # type: ignore[index]
    witness_split = bool(
        selected_witness["comparisons"]["entropy_matches"]  # type: ignore[index]
        and selected_witness["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
        and selected_witness["comparisons"]["channel_visible_differs"]  # type: ignore[index]
    )
    strict_hit = entropy_matches and min_cuts_exact and bool(interval_cover["is_strict_boundary_interval"]) and witness_split
    near_miss = entropy_matches and min_cuts_exact and not bool(interval_cover["is_strict_boundary_interval"]) and witness_split
    return {
        "boundary_template": {
            "name": boundary_template["name"],
            "template_kind": boundary_template["template_kind"],
            "description": boundary_template["description"],
            "boundary_order": boundary_order,
        },
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "description": network_spec["description"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
        },
        "ring_interval_summary": {
            "max_interval_length": max_interval_length,
            "intervals_checked": len(interval_records_tuple),
            "entropy_mismatches": sum(
                1 for record in interval_records_tuple if not record["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "max_internal_assignments_checked": max(
                int(record["min_cut"]["assignments_checked"]) for record in interval_records_tuple  # type: ignore[index]
            ),
            "all_interval_min_cuts_exact": min_cuts_exact,
            "ring_interval_entropy_profile_matches": entropy_matches,
        },
        "selected_witness_layout": {
            "minimal_interval_cover": interval_cover,
            "min_cut": selected_min_cut,
            "operator_channel_split": witness_split,
            "strict_layout_hit": strict_hit,
            "non_source_aware_near_miss": near_miss,
        },
        "first_interval_record": interval_records_tuple[0],
    }


def bridge_holography_phase4_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 2,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 2:
        raise ValueError("max_interval_length must be at least two")
    repaired_source = holographic_phase3_repaired_source(graph_max_codes=graph_max_codes)
    first = repaired_source["first"]
    second = repaired_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 4 repaired source must contain StabilizerCode objects")
    selected_region_mask = lift_inner_region_over_blocks(
        mask_from_qubits((2, 4)),
        block_mask=3,
        block_size=5,
        block_count=4,
    )
    selected_witness = holographic_phase4_selected_witness_diagnostic(
        first,
        second,
        region_mask=selected_region_mask,
    )
    boundary_templates = holographic_phase4_boundary_order_templates()
    layout_records = []
    for template in boundary_templates:
        boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
        for network_spec in holographic_phase4_network_specs(boundary_order):
            layout_records.append(
                holographic_phase4_layout_record(
                    first=first,
                    second=second,
                    boundary_template=template,
                    network_spec=network_spec,
                    selected_region_mask=selected_region_mask,
                    selected_witness=selected_witness,
                    max_interval_length=max_interval_length,
                )
            )
    layouts = tuple(layout_records)
    source_aware_hits = tuple(
        record
        for record in layouts
        if record["boundary_template"]["template_kind"] == "source_aware"  # type: ignore[index]
        and record["selected_witness_layout"]["strict_layout_hit"]  # type: ignore[index]
    )
    non_source_aware_hits = tuple(
        record
        for record in layouts
        if record["boundary_template"]["template_kind"] != "source_aware"  # type: ignore[index]
        and record["selected_witness_layout"]["strict_layout_hit"]  # type: ignore[index]
    )
    non_source_aware_near_misses = tuple(
        record
        for record in layouts
        if record["boundary_template"]["template_kind"] != "source_aware"  # type: ignore[index]
        and record["selected_witness_layout"]["non_source_aware_near_miss"]  # type: ignore[index]
    )
    cover_lengths = tuple(
        int(record["selected_witness_layout"]["minimal_interval_cover"]["minimal_cover_length"])  # type: ignore[index]
        for record in layouts
        if record["boundary_template"]["template_kind"] != "source_aware"  # type: ignore[index]
    )
    phase_claims = {
        "phase3_repaired_source_loaded": repaired_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "selected_phase3_witness_operator_channel_split_certified": bool(
            selected_witness["comparisons"]["entropy_matches"]  # type: ignore[index]
            and selected_witness["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
            and selected_witness["comparisons"]["channel_visible_differs"]  # type: ignore[index]
        ),
        "multi_bulk_layout_space_scored": len(layouts) == len(boundary_templates) * 4,
        "all_layout_interval_entropy_profiles_match": all(
            record["ring_interval_summary"]["ring_interval_entropy_profile_matches"] for record in layouts  # type: ignore[index]
        ),
        "all_layout_min_cuts_exactly_enumerated": all(
            record["ring_interval_summary"]["all_interval_min_cuts_exact"] for record in layouts  # type: ignore[index]
        ),
        "source_aware_layouts_recover_strict_witness": len(source_aware_hits) == 4,
        "less_source_aware_layouts_do_not_recover_strict_witness": len(non_source_aware_hits) == 0,
        "less_source_aware_layouts_are_operator_channel_near_misses": len(non_source_aware_near_misses) == 12,
        "less_source_aware_interval_cover_overhead_certified": bool(cover_lengths) and min(cover_lengths) > 4,
    }
    phase_claims["goal_3_phase_4_multi_bulk_layout_audit_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 4: multi-bulk-node layout audit",
        "status": "pass" if phase_claims["goal_3_phase_4_multi_bulk_layout_audit_certificate"] else "fail",
        "repair_source": {
            key: value
            for key, value in repaired_source.items()
            if key not in ("first", "second")
        },
        "selected_witness": selected_witness,
        "layout_space": {
            "boundary_templates": tuple(
                {
                    "name": template["name"],
                    "template_kind": template["template_kind"],
                    "description": template["description"],
                    "boundary_order": template["boundary_order"],
                }
                for template in boundary_templates
            ),
            "network_skeletons_per_boundary_order": (
                "single_bulk_ring_spoke",
                "outer_block_bulk_path",
                "inner_position_bulk_cycle",
                "binary_outer_tree",
            ),
            "max_interval_length": max_interval_length,
        },
        "layout_records": layouts,
        "strict_layout_hits": source_aware_hits,
        "non_source_aware_near_misses": non_source_aware_near_misses,
        "counts": {
            "boundary_templates": len(boundary_templates),
            "network_skeletons_per_boundary_order": 4,
            "layout_candidates": len(layouts),
            "source_aware_strict_hits": len(source_aware_hits),
            "less_source_aware_strict_hits": len(non_source_aware_hits),
            "less_source_aware_near_misses": len(non_source_aware_near_misses),
            "min_less_source_aware_interval_cover_length": min(cover_lengths),
            "max_less_source_aware_interval_cover_length": max(cover_lengths),
            "max_min_cut_internal_assignments": max(
                int(record["selected_witness_layout"]["min_cut"]["assignments_checked"]) for record in layouts  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The repaired Phase 3 operator/channel witness is stable under a bounded menu of multi-bulk-node "
                "min-cut skeletons, but strict boundary-interval locality is recovered only by the source-aware "
                "witness-strip boundary order."
            ),
            "three_geometry_lesson": (
                "Entropy-visible and min-cut-visible low-order geometry match across all audited layouts. "
                "Reconstruction and channel-visible geometry still split on the selected witness. What fails in "
                "less source-aware layouts is not the operator witness but its interpretation as a compact boundary "
                "causal patch."
            ),
            "scope_warning": (
                "The audit is exact for four boundary-order templates and four small min-cut skeletons, with all "
                "internal min-cut assignments enumerated. It is not an exhaustive search over 20-qubit boundary "
                "orders, tensor-network graphs, or HaPPY/MERA constructions."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 4 shows that less source-aware multi-bulk layouts are near-misses: they keep the exact "
                "entropy/min-cut and operator/channel separation but fail strict compact-patch locality. The next "
                "step should search generated graph-state or Clifford circuit tensor networks where locality is "
                "not imposed from the repaired witness strip."
            ),
            "suggested_phase_5": (
                "Run a bounded Clifford-MERA or small HaPPY-like stabilizer network search with explicit internal "
                "tensors, exact boundary entropies, exact min-cuts, and region algebra/erasure checks on candidate "
                "bulk-logical reconstructions."
            ),
        },
    }


def holographic_phase5_bit_reverse(value: int, *, width: int) -> int:
    out = 0
    for bit in range(width):
        out = (out << 1) | ((value >> bit) & 1)
    return out


def holographic_phase5_gray_code(value: int) -> int:
    return value ^ (value >> 1)


def holographic_phase5_riffle_halves(order: tuple[int, ...]) -> tuple[int, ...]:
    midpoint = len(order) // 2
    out = []
    for index in range(midpoint):
        out.append(order[index])
        out.append(order[index + midpoint])
    if len(order) % 2:
        out.append(order[-1])
    return tuple(out)


def holographic_phase5_raw_generated_layouts() -> tuple[dict[str, object], ...]:
    records: list[dict[str, object]] = []
    for stride in range(1, 20):
        if math.gcd(stride, 20) != 1:
            continue
        for offset in range(20):
            records.append(
                {
                    "name": f"affine_a{stride}_b{offset}",
                    "generator_family": "affine_modular",
                    "generator_kind": "source_agnostic",
                    "description": "Affine modular boundary scan q_i = b + a*i mod 20.",
                    "boundary_order": tuple((offset + stride * index) % 20 for index in range(20)),
                }
            )
    records.extend(
        (
            {
                "name": "bit_reversal_5bit",
                "generator_family": "hierarchical_bit",
                "generator_kind": "source_agnostic",
                "description": "Sort qubits by five-bit reversal, a small hierarchical/MERA-like shuffle.",
                "boundary_order": tuple(sorted(range(20), key=lambda qubit: (holographic_phase5_bit_reverse(qubit, width=5), qubit))),
            },
            {
                "name": "gray_code_5bit",
                "generator_family": "hierarchical_bit",
                "generator_kind": "source_agnostic",
                "description": "Sort qubits by five-bit Gray-code order.",
                "boundary_order": tuple(sorted(range(20), key=lambda qubit: (holographic_phase5_gray_code(qubit), qubit))),
            },
            {
                "name": "bitrev_gray_5bit",
                "generator_family": "hierarchical_bit",
                "generator_kind": "source_agnostic",
                "description": "Sort qubits by bit-reversed Gray-code order.",
                "boundary_order": tuple(
                    sorted(
                        range(20),
                        key=lambda qubit: (
                            holographic_phase5_bit_reverse(holographic_phase5_gray_code(qubit), width=5),
                            qubit,
                        ),
                    )
                ),
            },
            {
                "name": "even_odd_position_shuffle",
                "generator_family": "hierarchical_bit",
                "generator_kind": "source_agnostic",
                "description": "Place even positions before odd positions as a one-layer butterfly-like shuffle.",
                "boundary_order": tuple(range(0, 20, 2)) + tuple(range(1, 20, 2)),
            },
            {
                "name": "riffle_natural_halves",
                "generator_family": "butterfly_riffle",
                "generator_kind": "source_agnostic",
                "description": "Riffle the first and second halves of the natural repaired-code order.",
                "boundary_order": holographic_phase5_riffle_halves(tuple(range(20))),
            },
            {
                "name": "block_major_natural",
                "generator_family": "tensor_product_natural",
                "generator_kind": "source_agnostic",
                "description": "Natural repaired-code block-major tensor-product order.",
                "boundary_order": tuple(range(20)),
            },
            {
                "name": "inner_major_natural",
                "generator_family": "tensor_product_natural",
                "generator_kind": "source_agnostic",
                "description": "Natural inner-position-major tensor-product order.",
                "boundary_order": tuple(block * 5 + inner for inner in range(5) for block in range(4)),
            },
            {
                "name": "block_major_phase2_inner_ring",
                "generator_family": "phase2_seeded_tensor_product",
                "generator_kind": "phase2_seeded",
                "description": "Block-major tensor-product order using the Phase 2 inner ring order, but not the Phase 3 witness strip.",
                "boundary_order": tuple(
                    block * 5 + inner
                    for block in range(4)
                    for inner in (0, 1, 2, 4, 3)
                ),
            },
            {
                "name": "inner_major_phase2_inner_ring",
                "generator_family": "phase2_seeded_tensor_product",
                "generator_kind": "phase2_seeded",
                "description": "Inner-position-major tensor-product order using the Phase 2 inner ring order, but not the Phase 3 witness strip.",
                "boundary_order": tuple(
                    block * 5 + inner
                    for inner in (0, 1, 2, 4, 3)
                    for block in range(4)
                ),
            },
        )
    )
    return tuple(records)


def holographic_phase5_generated_layouts() -> tuple[dict[str, object], ...]:
    unique: dict[tuple[int, ...], dict[str, object]] = {}
    for record in holographic_phase5_raw_generated_layouts():
        order = tuple(int(qubit) for qubit in record["boundary_order"])  # type: ignore[index]
        if order not in unique:
            unique[order] = {
                **record,
                "boundary_order": order,
                "aliases": (record["name"],),
            }
        else:
            existing = unique[order]
            existing["aliases"] = tuple(existing["aliases"]) + (record["name"],)  # type: ignore[index]
    return tuple(unique.values())


def holographic_phase5_cover_distribution(records: tuple[dict[str, object], ...]) -> tuple[dict[str, object], ...]:
    lengths = sorted(
        {
            int(record["minimal_interval_cover"]["minimal_cover_length"])  # type: ignore[index]
            for record in records
        }
    )
    return tuple(
        {
            "cover_length": length,
            "layout_count": sum(
                1
                for record in records
                if int(record["minimal_interval_cover"]["minimal_cover_length"]) == length  # type: ignore[index]
            ),
        }
        for length in lengths
    )


def holographic_phase5_layout_record(
    *,
    layout: dict[str, object],
    selected_region_mask: int,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in layout["boundary_order"])  # type: ignore[index]
    interval_cover = holographic_phase4_minimal_interval_cover(
        boundary_order=boundary_order,
        region_mask=selected_region_mask,
    )
    network_records = []
    for network_spec in holographic_phase4_network_specs(boundary_order):
        min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=selected_region_mask)
        network_records.append(
            {
                "network": {
                    "name": network_spec["name"],
                    "network_kind": network_spec["network_kind"],
                    "internal_nodes": network_spec["internal_nodes"],
                    "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
                },
                "selected_witness_min_cut": min_cut,
            }
        )
    return {
        "name": layout["name"],
        "aliases": layout["aliases"],
        "generator_family": layout["generator_family"],
        "generator_kind": layout["generator_kind"],
        "description": layout["description"],
        "boundary_order": boundary_order,
        "minimal_interval_cover": interval_cover,
        "network_records": tuple(network_records),
        "strict_compact_hit": interval_cover["is_strict_boundary_interval"],
        "operator_channel_near_miss": not interval_cover["is_strict_boundary_interval"],
    }


def bridge_holography_phase5_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    repaired_source = holographic_phase3_repaired_source(graph_max_codes=graph_max_codes)
    first = repaired_source["first"]
    second = repaired_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 5 repaired source must contain StabilizerCode objects")
    selected_region_mask = lift_inner_region_over_blocks(
        mask_from_qubits((2, 4)),
        block_mask=3,
        block_size=5,
        block_count=4,
    )
    selected_witness = holographic_phase4_selected_witness_diagnostic(
        first,
        second,
        region_mask=selected_region_mask,
    )
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    raw_layouts = holographic_phase5_raw_generated_layouts()
    generated_layouts = holographic_phase5_generated_layouts()
    layout_records = tuple(
        holographic_phase5_layout_record(layout=layout, selected_region_mask=selected_region_mask)
        for layout in generated_layouts
    )
    source_agnostic_records = tuple(
        record for record in layout_records if record["generator_kind"] == "source_agnostic"
    )
    phase2_seeded_records = tuple(
        record for record in layout_records if record["generator_kind"] == "phase2_seeded"
    )
    strict_hits = tuple(record for record in layout_records if record["strict_compact_hit"])
    source_agnostic_best_length = min(
        int(record["minimal_interval_cover"]["minimal_cover_length"]) for record in source_agnostic_records  # type: ignore[index]
    )
    phase2_seeded_best_length = min(
        int(record["minimal_interval_cover"]["minimal_cover_length"]) for record in phase2_seeded_records  # type: ignore[index]
    )
    best_source_agnostic = tuple(
        record
        for record in source_agnostic_records
        if int(record["minimal_interval_cover"]["minimal_cover_length"]) == source_agnostic_best_length  # type: ignore[index]
    )
    best_phase2_seeded = tuple(
        record
        for record in phase2_seeded_records
        if int(record["minimal_interval_cover"]["minimal_cover_length"]) == phase2_seeded_best_length  # type: ignore[index]
    )
    all_min_cuts_exact = all(
        int(network["selected_witness_min_cut"]["assignments_checked"])  # type: ignore[index]
        == 2 ** len(network["network"]["internal_nodes"])  # type: ignore[arg-type,index]
        for record in layout_records
        for network in record["network_records"]  # type: ignore[index]
    )
    phase_claims = {
        "phase3_repaired_source_loaded": repaired_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "selected_phase3_witness_operator_channel_split_certified": bool(
            selected_witness["comparisons"]["entropy_matches"]  # type: ignore[index]
            and selected_witness["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
            and selected_witness["comparisons"]["channel_visible_differs"]  # type: ignore[index]
        ),
        "all_labeled_t2_entropy_matches_after_repair": low_order_entropy["matches"],
        "generated_layout_space_scored": len(raw_layouts) == 169 and len(generated_layouts) == 168,
        "all_generated_selected_mincuts_exact": all_min_cuts_exact,
        "generated_layouts_have_no_strict_compact_hit": len(strict_hits) == 0,
        "source_agnostic_best_cover_length_is_8": source_agnostic_best_length == 8,
        "phase2_seeded_best_cover_length_is_6": phase2_seeded_best_length == 6,
        "phase2_seeded_improves_but_does_not_recover_strict_locality": (
            phase2_seeded_best_length < source_agnostic_best_length and phase2_seeded_best_length > 4
        ),
    }
    phase_claims["goal_3_phase_5_generated_layout_search_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 5: generated Clifford/MERA-style layout search",
        "status": "pass" if phase_claims["goal_3_phase_5_generated_layout_search_certificate"] else "fail",
        "repair_source": {
            key: value
            for key, value in repaired_source.items()
            if key not in ("first", "second")
        },
        "selected_witness": selected_witness,
        "low_order_entropy": low_order_entropy,
        "generation_rules": {
            "raw_layouts": len(raw_layouts),
            "unique_layouts": len(generated_layouts),
            "families": tuple(
                {
                    "generator_family": family,
                    "raw_count": sum(1 for record in raw_layouts if record["generator_family"] == family),
                    "unique_primary_count": sum(1 for record in generated_layouts if record["generator_family"] == family),
                }
                for family in sorted({str(record["generator_family"]) for record in raw_layouts})
            ),
            "source_aware_phase4_witness_strip_excluded": True,
        },
        "layout_search": {
            "cover_distribution": holographic_phase5_cover_distribution(layout_records),
            "best_source_agnostic_layouts": best_source_agnostic[:8],
            "best_phase2_seeded_layouts": best_phase2_seeded,
            "strict_compact_hits": strict_hits,
            "layout_records": layout_records,
        },
        "counts": {
            "raw_generated_layouts": len(raw_layouts),
            "unique_generated_layouts": len(generated_layouts),
            "source_agnostic_layouts": len(source_agnostic_records),
            "phase2_seeded_layouts": len(phase2_seeded_records),
            "strict_compact_hits": len(strict_hits),
            "source_agnostic_best_cover_length": source_agnostic_best_length,
            "source_agnostic_best_layouts": len(best_source_agnostic),
            "phase2_seeded_best_cover_length": phase2_seeded_best_length,
            "phase2_seeded_best_layouts": len(best_phase2_seeded),
            "selected_mincut_records": sum(len(record["network_records"]) for record in layout_records),  # type: ignore[arg-type]
            "max_selected_mincut_internal_assignments": max(
                int(network["selected_witness_min_cut"]["assignments_checked"])  # type: ignore[index]
                for record in layout_records
                for network in record["network_records"]  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded generated-layout search over affine, bit/Gray-code, riffle, and tensor-product "
                "Clifford/MERA-style boundary orders finds no compact boundary interval for the repaired Phase 3 "
                "operator/channel witness."
            ),
            "three_geometry_lesson": (
                "The exact operator/channel split survives as a code property and all selected min-cuts are exactly "
                "enumerated, but generated source-agnostic layouts do not recover causal-patch locality. A Phase-2-"
                "seeded tensor-product interleaver improves the cover length from 8 to 6, still short of a strict "
                "four-site patch."
            ),
            "scope_warning": (
                "The search is exhaustive only over the stated generated layout grammar and four fixed min-cut "
                "skeletons. It is not an exhaustive Clifford circuit, HaPPY, MERA, or hyperbolic tiling search."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 5 certifies a generated-layout locality no-go within this grammar. The next step should move "
                "from boundary-order generators to actual small stabilizer tensor-network constructions with "
                "internal Clifford tensors and boundary/bulk partitions generated together."
            ),
            "suggested_phase_6": (
                "Build or enumerate small Clifford tensor-network circuits with internal nodes, then compare exact "
                "boundary entropy, min-cut, region algebra, erasure, and survivor fixed-point diagnostics for "
                "candidate bulk-logical pairs."
            ),
        },
    }


def holographic_phase6_circuit_templates() -> tuple[dict[str, object], ...]:
    return (
        {
            "name": "identity_reference",
            "generator_kind": "baseline",
            "description": "No Clifford tensors; records the unrearranged repaired Phase 3 witness.",
            "boundary_order": tuple(range(20)),
            "gates": (),
        },
        {
            "name": "local_h_layer",
            "generator_kind": "source_agnostic_local_clifford",
            "description": "One layer of single-qubit H tensors on every boundary wire.",
            "boundary_order": tuple(range(20)),
            "gates": tuple(("H", qubit) for qubit in range(20)),
        },
        {
            "name": "local_s_layer",
            "generator_kind": "source_agnostic_local_clifford",
            "description": "One layer of single-qubit S tensors on every boundary wire.",
            "boundary_order": tuple(range(20)),
            "gates": tuple(("S", qubit) for qubit in range(20)),
        },
        {
            "name": "nearest_neighbor_even_cx_layer",
            "generator_kind": "source_agnostic_entangling_clifford",
            "description": "Parallel nearest-neighbor CX tensors on even boundary pairs.",
            "boundary_order": tuple(range(20)),
            "gates": tuple(("CX", qubit, qubit + 1) for qubit in range(0, 20, 2)),
        },
        {
            "name": "butterfly_halves_cx_layer",
            "generator_kind": "source_agnostic_entangling_clifford",
            "description": "Parallel butterfly CX tensors coupling the two halves of the boundary.",
            "boundary_order": tuple(range(20)),
            "gates": tuple(("CX", qubit, qubit + 10) for qubit in range(10)),
        },
        {
            "name": "phase2_witness_pair_cx_control",
            "generator_kind": "source_aware_control",
            "description": "Control layer coupling the lifted Phase 2 witness pairs; included as a positive source-aware control.",
            "boundary_order": tuple(range(20)),
            "gates": (("CX", 2, 7), ("CX", 4, 9), ("CX", 12, 17), ("CX", 14, 19)),
        },
    )


def holographic_phase6_apply_circuit(code: StabilizerCode, gates: tuple[tuple[object, ...], ...]) -> StabilizerCode:
    rows = tuple(code.generators)
    for gate in gates:
        gate_name = str(gate[0])
        if gate_name == "H":
            rows = tuple(apply_h(row, code.n, int(gate[1])) for row in rows)
        elif gate_name == "S":
            rows = tuple(apply_s(row, code.n, int(gate[1])) for row in rows)
        elif gate_name == "CX":
            rows = tuple(apply_cx(row, code.n, int(gate[1]), int(gate[2])) for row in rows)
        else:
            raise ValueError(f"unknown Clifford gate {gate_name!r}")
    return StabilizerCode(code.n, rows)


def holographic_phase6_circuit_network_spec(circuit: dict[str, object]) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in circuit["boundary_order"])  # type: ignore[index]
    edges = list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = []
    for index, gate in enumerate(circuit["gates"]):  # type: ignore[index]
        gate_tuple = tuple(gate)  # type: ignore[arg-type]
        if str(gate_tuple[0]) != "CX":
            continue
        node = f"gate_{index}_cx_{int(gate_tuple[1])}_{int(gate_tuple[2])}"
        internal_nodes.append(node)
        edges.append(holographic_phase4_edge(node, f"q{int(gate_tuple[1])}", edge_type="clifford_gate_leg"))
        edges.append(holographic_phase4_edge(node, f"q{int(gate_tuple[2])}", edge_type="clifford_gate_leg"))
    return {
        "name": f"{circuit['name']}_interaction_graph",
        "network_kind": "clifford_circuit_interaction_graph",
        "description": "Boundary ring plus one internal node per two-qubit Clifford tensor.",
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": tuple(internal_nodes),
        "edges": tuple(edges),
    }


def holographic_phase6_circuit_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    circuit: dict[str, object],
    selected_region_mask: int,
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in circuit["gates"])  # type: ignore[index]
    transformed_first = holographic_phase6_apply_circuit(first, gates)
    transformed_second = holographic_phase6_apply_circuit(second, gates)
    witness = holographic_phase4_selected_witness_diagnostic(
        transformed_first,
        transformed_second,
        region_mask=selected_region_mask,
    )
    network_spec = holographic_phase6_circuit_network_spec(circuit)
    min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=selected_region_mask)
    return {
        "name": circuit["name"],
        "generator_kind": circuit["generator_kind"],
        "description": circuit["description"],
        "boundary_order": circuit["boundary_order"],
        "gates": gates,
        "gate_counts": {
            "single_qubit": sum(1 for gate in gates if str(gate[0]) in ("H", "S")),
            "two_qubit": sum(1 for gate in gates if str(gate[0]) == "CX"),
            "total": len(gates),
        },
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
        },
        "selected_witness": witness,
        "selected_witness_min_cut": min_cut,
        "certified_behavior": {
            "entropy_visible_match": witness["comparisons"]["entropy_matches"],  # type: ignore[index]
            "operator_channel_split": witness["comparisons"]["channel_visible_differs"]  # type: ignore[index]
            and witness["comparisons"]["reconstruction_visible_differs"],  # type: ignore[index]
            "operator_channel_collapsed": not (
                witness["comparisons"]["channel_visible_differs"]  # type: ignore[index]
                or witness["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
            ),
            "min_cut_exact": min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
    }


def bridge_holography_phase6_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    repaired_source = holographic_phase3_repaired_source(graph_max_codes=graph_max_codes)
    first = repaired_source["first"]
    second = repaired_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 6 repaired source must contain StabilizerCode objects")
    selected_region_mask = lift_inner_region_over_blocks(
        mask_from_qubits((2, 4)),
        block_mask=3,
        block_size=5,
        block_count=4,
    )
    circuits = holographic_phase6_circuit_templates()
    records = tuple(
        holographic_phase6_circuit_record(
            first=first,
            second=second,
            circuit=circuit,
            selected_region_mask=selected_region_mask,
        )
        for circuit in circuits
    )
    preserving_records = tuple(record for record in records if record["certified_behavior"]["operator_channel_split"])  # type: ignore[index]
    collapsing_records = tuple(record for record in records if record["certified_behavior"]["operator_channel_collapsed"])  # type: ignore[index]
    source_agnostic_entangling = tuple(
        record
        for record in records
        if record["generator_kind"] == "source_agnostic_entangling_clifford"
    )
    source_agnostic_entangling_preserve = tuple(
        record for record in source_agnostic_entangling if record["certified_behavior"]["operator_channel_split"]  # type: ignore[index]
    )
    source_agnostic_entangling_collapse = tuple(
        record for record in source_agnostic_entangling if record["certified_behavior"]["operator_channel_collapsed"]  # type: ignore[index]
    )
    phase_claims = {
        "phase3_repaired_source_loaded": repaired_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "generated_clifford_tensor_networks_scored": len(records) == 6,
        "all_circuit_selected_mincuts_exact": all(record["certified_behavior"]["min_cut_exact"] for record in records),  # type: ignore[index]
        "all_circuits_keep_selected_entropy_visible_match": all(
            record["certified_behavior"]["entropy_visible_match"] for record in records  # type: ignore[index]
        ),
        "local_clifford_layers_preserve_operator_channel_split": all(
            record["certified_behavior"]["operator_channel_split"]  # type: ignore[index]
            for record in records
            if record["generator_kind"] == "source_agnostic_local_clifford"
        ),
        "source_agnostic_entangling_layers_can_preserve_or_collapse": (
            len(source_agnostic_entangling_preserve) >= 1 and len(source_agnostic_entangling_collapse) >= 1
        ),
        "nearest_neighbor_cx_collapses_selected_witness": any(
            record["name"] == "nearest_neighbor_even_cx_layer"
            and record["certified_behavior"]["operator_channel_collapsed"]  # type: ignore[index]
            for record in records
        ),
        "butterfly_cx_preserves_selected_witness": any(
            record["name"] == "butterfly_halves_cx_layer"
            and record["certified_behavior"]["operator_channel_split"]  # type: ignore[index]
            for record in records
        ),
    }
    phase_claims["goal_3_phase_6_generated_clifford_tensor_network_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 6: generated Clifford tensor-network audit",
        "status": "pass" if phase_claims["goal_3_phase_6_generated_clifford_tensor_network_certificate"] else "fail",
        "repair_source": {
            key: value
            for key, value in repaired_source.items()
            if key not in ("first", "second")
        },
        "selected_region": {
            "name": "phase3_selected_two_block_lift_output_patch",
            "qubits": mask_to_tuple(selected_region_mask, first.n),
            "mask": selected_region_mask,
        },
        "circuit_records": records,
        "preserving_circuits": preserving_records,
        "collapsing_circuits": collapsing_records,
        "counts": {
            "circuits_scored": len(records),
            "source_agnostic_local_clifford_circuits": sum(
                1 for record in records if record["generator_kind"] == "source_agnostic_local_clifford"
            ),
            "source_agnostic_entangling_circuits": len(source_agnostic_entangling),
            "source_aware_control_circuits": sum(
                1 for record in records if record["generator_kind"] == "source_aware_control"
            ),
            "operator_channel_preserving_circuits": len(preserving_records),
            "operator_channel_collapsing_circuits": len(collapsing_records),
            "max_circuit_internal_assignments": max(
                int(record["selected_witness_min_cut"]["assignments_checked"]) for record in records  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Actual generated Clifford tensor layers can change the repaired witness semantics while preserving "
                "the selected entropy-visible data. Local Clifford layers preserve the split, a nearest-neighbor CX "
                "layer collapses it, and a butterfly CX layer preserves it."
            ),
            "three_geometry_lesson": (
                "The selected patch has matching entropy in every audited circuit, but reconstruction/channel "
                "geometry is circuit-sensitive. Thus even after moving from boundary-order generators to internal "
                "Clifford tensors, entropy/min-cut-visible geometry does not determine operator or erasure geometry."
            ),
            "scope_warning": (
                "This is a bounded audit of six generated Clifford tensor networks on one repaired witness patch, "
                "not an exhaustive Clifford-circuit or HaPPY/MERA search."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 6 shows that internal Clifford tensors can preserve or collapse the repaired witness. The "
                "next step should broaden from a fixed output patch to generated bulk-logical targets and search "
                "over compact patches jointly with circuit generation."
            ),
            "suggested_phase_7": (
                "Run a bounded joint search over small Clifford tensor-network circuits, output boundary intervals, "
                "and candidate bulk-logical regions, with exact entropy, min-cut, region algebra, erasure, and "
                "survivor diagnostics."
            ),
        },
    }


def holographic_phase7_min_cut_summary(min_cut: dict[str, object]) -> dict[str, object]:
    return {
        "value": min_cut["value"],
        "assignments_checked": min_cut["assignments_checked"],
        "internal_nodes": min_cut["internal_nodes"],
    }


def holographic_phase7_bulk_logical_candidate_summary(
    *,
    first_algebra_signature: tuple[int, int, int, bool],
    second_algebra_signature: tuple[int, int, int, bool],
) -> dict[str, object]:
    first_logical_dim, first_center_dim, _, first_reconstructs_all = first_algebra_signature
    second_logical_dim, second_center_dim, _, second_reconstructs_all = second_algebra_signature
    if first_reconstructs_all and not second_reconstructs_all:
        pattern = "first_full_logical_vs_second_partial_or_empty"
    elif second_reconstructs_all and not first_reconstructs_all:
        pattern = "second_full_logical_vs_first_partial_or_empty"
    elif first_logical_dim > second_logical_dim:
        pattern = "first_carries_more_region_logical_algebra"
    elif second_logical_dim > first_logical_dim:
        pattern = "second_carries_more_region_logical_algebra"
    elif first_center_dim != second_center_dim:
        pattern = "center_algebra_differs"
    else:
        pattern = "same_logical_dimension_but_different_commutation_structure"
    return {
        "single_bulk_logical_code_pair": True,
        "first_has_region_logical_algebra": first_logical_dim > 0,
        "second_has_region_logical_algebra": second_logical_dim > 0,
        "first_reconstructs_full_bulk_logical": first_reconstructs_all,
        "second_reconstructs_full_bulk_logical": second_reconstructs_all,
        "candidate_pattern": pattern,
    }


def holographic_phase7_hit_record(
    *,
    circuit: dict[str, object],
    first: StabilizerCode,
    second: StabilizerCode,
    network_spec: dict[str, object],
    region: dict[str, object],
) -> dict[str, object]:
    region_mask = int(region["mask"])
    full = (1 << first.n) - 1
    min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
    first_algebra = first.region_algebra(region_mask)
    second_algebra = second.region_algebra(region_mask)
    first_erasure = first.erasure_correctable(region_mask)
    second_erasure = second.erasure_correctable(region_mask)
    first_survivor = first.reconstructs_all_logicals(full ^ region_mask)
    second_survivor = second.reconstructs_all_logicals(full ^ region_mask)
    first_entropy = first.entropy(region_mask)
    second_entropy = second.entropy(region_mask)
    first_signature = first_algebra.signature()
    second_signature = second_algebra.signature()
    reconstruction_differs = first_signature != second_signature
    erasure_differs = first_erasure != second_erasure
    survivor_differs = first_survivor != second_survivor
    return {
        "circuit": {
            "name": circuit["name"],
            "generator_kind": circuit["generator_kind"],
        },
        "region": {
            key: value
            for key, value in region.items()
            if key != "mask"
        },
        "min_cut": holographic_phase7_min_cut_summary(min_cut),
        "first": {
            "entropy": first_entropy,
            "algebra_signature": first_signature,
            "reconstructs_all": first_algebra.reconstructs_all,
            "erasure_correctable": first_erasure,
            "survivor_fixed_point_reconstructs_all": first_survivor,
        },
        "second": {
            "entropy": second_entropy,
            "algebra_signature": second_signature,
            "reconstructs_all": second_algebra.reconstructs_all,
            "erasure_correctable": second_erasure,
            "survivor_fixed_point_reconstructs_all": second_survivor,
        },
        "bulk_logical_candidate": holographic_phase7_bulk_logical_candidate_summary(
            first_algebra_signature=first_signature,
            second_algebra_signature=second_signature,
        ),
        "comparisons": {
            "entropy_matches": first_entropy == second_entropy,
            "min_cut_exact": min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
            "reconstruction_visible_differs": reconstruction_differs,
            "erasure_correctability_differs": erasure_differs,
            "survivor_fixed_point_differs": survivor_differs,
            "channel_visible_differs": erasure_differs or survivor_differs,
            "operator_or_channel_visible_differs": reconstruction_differs or erasure_differs or survivor_differs,
        },
    }


def holographic_phase7_circuit_search_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    circuit: dict[str, object],
    fixed_phase3_region_mask: int,
    max_interval_length: int,
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in circuit["gates"])  # type: ignore[index]
    transformed_first = holographic_phase6_apply_circuit(first, gates)
    transformed_second = holographic_phase6_apply_circuit(second, gates)
    first_distance = bounded_distance_certificate(transformed_first, max_weight=1)
    second_distance = bounded_distance_certificate(transformed_second, max_weight=1)
    distance_preserving = bool(
        first_distance["distance_at_least_2_certified"]
        and second_distance["distance_at_least_2_certified"]
    )
    fixed_patch = holographic_phase4_selected_witness_diagnostic(
        transformed_first,
        transformed_second,
        region_mask=fixed_phase3_region_mask,
    )
    fixed_patch_split = bool(
        fixed_patch["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
        or fixed_patch["comparisons"]["channel_visible_differs"]  # type: ignore[index]
    )
    boundary_order = tuple(int(qubit) for qubit in circuit["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase6_circuit_network_spec(circuit)
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    entropy_gate_passes = 0
    entropy_gate_rejections = 0
    all_min_cuts_exact = True
    length_summaries = []
    hit_records = []
    for length in range(1, max_interval_length + 1):
        length_intervals = tuple(region for region in intervals if int(region["length"]) == length)
        length_entropy_passes = 0
        length_hits = 0
        for region in length_intervals:
            region_mask = int(region["mask"])
            min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
            min_cut_exact = min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"])  # type: ignore[arg-type]
            all_min_cuts_exact = all_min_cuts_exact and min_cut_exact
            first_entropy = transformed_first.entropy(region_mask)
            second_entropy = transformed_second.entropy(region_mask)
            if first_entropy != second_entropy:
                entropy_gate_rejections += 1
                continue
            entropy_gate_passes += 1
            length_entropy_passes += 1
            hit = holographic_phase7_hit_record(
                circuit=circuit,
                first=transformed_first,
                second=transformed_second,
                network_spec=network_spec,
                region=region,
            )
            if bool(hit["comparisons"]["operator_or_channel_visible_differs"]):  # type: ignore[index]
                hit_records.append(hit)
                length_hits += 1
        length_summaries.append(
            {
                "length": length,
                "intervals_scanned": len(length_intervals),
                "entropy_gate_passes": length_entropy_passes,
                "entropy_gate_rejections": len(length_intervals) - length_entropy_passes,
                "operator_or_channel_hits": length_hits,
            }
        )
    hits = tuple(hit_records)
    return {
        "name": circuit["name"],
        "generator_kind": circuit["generator_kind"],
        "description": circuit["description"],
        "boundary_order": boundary_order,
        "gates": gates,
        "gate_counts": {
            "single_qubit": sum(1 for gate in gates if str(gate[0]) in ("H", "S")),
            "two_qubit": sum(1 for gate in gates if str(gate[0]) == "CX"),
            "total": len(gates),
        },
        "distance_audit": {
            "first": first_distance,
            "second": second_distance,
            "both_codes_distance_at_least_2_under_weight_one_audit": distance_preserving,
        },
        "fixed_phase3_patch": {
            "diagnostic": fixed_patch,
            "operator_or_channel_split": fixed_patch_split,
        },
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
        },
        "interval_search": {
            "candidate_rule": "all output-boundary ring intervals with length <= max_interval_length",
            "max_interval_length": max_interval_length,
            "intervals_scanned": len(intervals),
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "all_candidate_min_cuts_exact": all_min_cuts_exact,
            "length_summaries": tuple(length_summaries),
            "hit_count": len(hits),
            "shortest_hit_length": min((int(hit["region"]["length"]) for hit in hits), default=None),  # type: ignore[index]
        },
        "hit_records": hits,
    }


def bridge_holography_phase7_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 6,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 6:
        raise ValueError("max_interval_length must be at least six for the Phase 7 certificate")
    repaired_source = holographic_phase3_repaired_source(graph_max_codes=graph_max_codes)
    first = repaired_source["first"]
    second = repaired_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 7 repaired source must contain StabilizerCode objects")
    fixed_phase3_region_mask = lift_inner_region_over_blocks(
        mask_from_qubits((2, 4)),
        block_mask=3,
        block_size=5,
        block_count=4,
    )
    circuits = holographic_phase6_circuit_templates()
    circuit_records = tuple(
        holographic_phase7_circuit_search_record(
            first=first,
            second=second,
            circuit=circuit,
            fixed_phase3_region_mask=fixed_phase3_region_mask,
            max_interval_length=max_interval_length,
        )
        for circuit in circuits
    )
    all_hits = tuple(
        hit
        for record in circuit_records
        for hit in record["hit_records"]  # type: ignore[index]
    )
    distance_preserving_hits = tuple(
        hit
        for record in circuit_records
        if record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
        for hit in record["hit_records"]  # type: ignore[index]
    )
    low_distance_frontier_hits = tuple(
        hit
        for record in circuit_records
        if not record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
        for hit in record["hit_records"]  # type: ignore[index]
    )
    source_agnostic_entangling_distance_hits = tuple(
        hit
        for record in circuit_records
        if record["generator_kind"] == "source_agnostic_entangling_clifford"
        and record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
        for hit in record["hit_records"]  # type: ignore[index]
    )
    one_qubit_hits = tuple(hit for hit in all_hits if int(hit["region"]["length"]) == 1)  # type: ignore[index]
    nearest_record = next(record for record in circuit_records if record["name"] == "nearest_neighbor_even_cx_layer")
    butterfly_record = next(record for record in circuit_records if record["name"] == "butterfly_halves_cx_layer")
    selected_replacement_hit = next(
        hit
        for hit in nearest_record["hit_records"]  # type: ignore[index]
        if int(hit["region"]["length"]) == 6  # type: ignore[index]
        and int(hit["region"]["start"]) == 9  # type: ignore[index]
    )
    selected_frontier_tiny_hit = next(
        hit
        for hit in butterfly_record["hit_records"]  # type: ignore[index]
        if int(hit["region"]["length"]) == 1  # type: ignore[index]
    )
    total_intervals = sum(int(record["interval_search"]["intervals_scanned"]) for record in circuit_records)  # type: ignore[index]
    entropy_gate_passes = sum(int(record["interval_search"]["entropy_gate_passes"]) for record in circuit_records)  # type: ignore[index]
    entropy_gate_rejections = sum(int(record["interval_search"]["entropy_gate_rejections"]) for record in circuit_records)  # type: ignore[index]
    distance_preserving_hit_lengths = tuple(int(hit["region"]["length"]) for hit in distance_preserving_hits)  # type: ignore[index]
    low_distance_hit_lengths = tuple(int(hit["region"]["length"]) for hit in low_distance_frontier_hits)  # type: ignore[index]
    nearest_fixed_patch_collapsed = bool(
        nearest_record["fixed_phase3_patch"]["diagnostic"]["comparisons"]["entropy_matches"]  # type: ignore[index]
        and not nearest_record["fixed_phase3_patch"]["operator_or_channel_split"]  # type: ignore[index]
    )
    phase_claims = {
        "phase3_repaired_source_loaded": repaired_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "compact_interval_joint_search_scored": len(circuit_records) == 6
        and total_intervals == len(circuit_records) * first.n * max_interval_length,
        "all_candidate_mincuts_exact": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in circuit_records  # type: ignore[index]
        ),
        "distance_audits_are_exact_weight_one_checks": all(
            record["distance_audit"]["first"]["max_weight_checked"] == 1  # type: ignore[index]
            and record["distance_audit"]["second"]["max_weight_checked"] == 1  # type: ignore[index]
            for record in circuit_records
        ),
        "entropy_visible_match_on_all_hits": all(
            hit["comparisons"]["entropy_matches"] for hit in all_hits  # type: ignore[index]
        ),
        "operator_or_channel_split_on_all_hits": all(
            hit["comparisons"]["operator_or_channel_visible_differs"] for hit in all_hits  # type: ignore[index]
        ),
        "distance_preserving_compact_witnesses_exist": bool(distance_preserving_hits),
        "distance_preserving_hits_have_min_length_six": bool(distance_preserving_hit_lengths)
        and min(distance_preserving_hit_lengths) == 6,
        "nearest_neighbor_fixed_patch_collapses_but_replacement_interval_exists": nearest_fixed_patch_collapsed
        and bool(nearest_record["hit_records"]),
        "source_agnostic_entangling_distance_preserving_hit_exists": bool(source_agnostic_entangling_distance_hits),
        "frontier_one_qubit_hits_separated_by_distance_gate": bool(one_qubit_hits)
        and all(
            not record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
            for hit in one_qubit_hits
            for record in circuit_records
            if record["name"] == hit["circuit"]["name"]  # type: ignore[index]
        ),
        "frontier_hits_have_min_length_one": bool(low_distance_hit_lengths) and min(low_distance_hit_lengths) == 1,
    }
    phase_claims["goal_3_phase_7_joint_clifford_patch_search_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 7: joint Clifford circuit and compact-patch search",
        "status": "pass" if phase_claims["goal_3_phase_7_joint_clifford_patch_search_certificate"] else "fail",
        "repair_source": {
            key: value
            for key, value in repaired_source.items()
            if key not in ("first", "second")
        },
        "search_scope": {
            "circuits": tuple(circuit["name"] for circuit in circuits),
            "candidate_patch_rule": "all compact output-boundary ring intervals of length 1 through 6",
            "candidate_bulk_logical_rule": (
                "A candidate interval is promoted to a hit only after exact entropy matching, exact min-cut "
                "enumeration, and a differing region-algebra, erasure, or survivor fixed-point diagnostic."
            ),
            "fixed_phase3_region_qubits": mask_to_tuple(fixed_phase3_region_mask, first.n),
            "distance_gate": "weight-one logical exclusion is certified for each transformed code pair",
        },
        "circuit_records": circuit_records,
        "selected_distance_preserving_replacement_hit": selected_replacement_hit,
        "selected_frontier_tiny_hit": selected_frontier_tiny_hit,
        "counts": {
            "circuits_scored": len(circuit_records),
            "candidate_intervals_scanned": total_intervals,
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "operator_or_channel_hits": len(all_hits),
            "distance_preserving_circuits": sum(
                1
                for record in circuit_records
                if record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
            ),
            "low_distance_frontier_circuits": sum(
                1
                for record in circuit_records
                if not record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
            ),
            "distance_preserving_hits": len(distance_preserving_hits),
            "source_agnostic_entangling_distance_preserving_hits": len(source_agnostic_entangling_distance_hits),
            "low_distance_frontier_hits": len(low_distance_frontier_hits),
            "one_qubit_frontier_hits": len(one_qubit_hits),
            "min_distance_preserving_hit_length": min(distance_preserving_hit_lengths),
            "min_low_distance_frontier_hit_length": min(low_distance_hit_lengths),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(record["network"]["internal_nodes"]) for record in circuit_records  # type: ignore[arg-type,index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The Phase 7 joint search no longer fixes the Phase 3 witness patch. Across six Clifford tensor "
                "circuits and all compact output intervals of length at most six, it finds exact entropy-matched "
                "operator/channel witnesses, including distance-preserving replacement intervals for the "
                "nearest-neighbor CX circuit whose fixed Phase 3 patch had collapsed."
            ),
            "three_geometry_lesson": (
                "Entropy/min-cut-visible geometry can miss both failures and replacements: a tensor layer may "
                "erase the old observer patch while another compact interval in the same output geometry still "
                "carries a different bulk-logical algebra or erasure semantics."
            ),
            "scope_warning": (
                "The search is exhaustive only for the six listed Clifford circuits and compact ring intervals of "
                "length <= 6. One-qubit hits are explicitly classified as frontier evidence because their circuits "
                "create a weight-one logical witness in the first transformed code."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 7 finds replacement compact patches and separates robust distance-preserving hits from "
                "low-distance frontier artifacts. The next step should synthesize or enumerate distance-preserving "
                "entangling Clifford layers directly, then test HaPPY/perfect-tensor-like stabilizer blocks under "
                "the same joint patch search."
            ),
            "suggested_phase_8": (
                "Run a bounded distance-gated Clifford synthesis search over entangling layers, with the compact "
                "patch search inside the objective and exact certificates for entropy, min-cut, region algebra, "
                "erasure, survivor fixed points, and weight-one distance preservation."
            ),
        },
    }


def holographic_phase8_adjacent_cx_circuit(
    *,
    name: str,
    generator_family: str,
    generator_kind: str,
    description: str,
    boundary_order: tuple[int, ...],
) -> dict[str, object]:
    return {
        "name": name,
        "generator_family": generator_family,
        "generator_kind": generator_kind,
        "description": description,
        "boundary_order": boundary_order,
        "gates": tuple(("CX", boundary_order[index], boundary_order[index + 1]) for index in range(0, len(boundary_order), 2)),
    }


def holographic_phase8_synthesis_templates() -> tuple[dict[str, object], ...]:
    circuits = []
    for offset in range(20):
        boundary_order = tuple((offset + index) % 20 for index in range(20))
        circuits.append(
            holographic_phase8_adjacent_cx_circuit(
                name=f"synth_affine_stride1_offset{offset}",
                generator_family="affine_modular_adjacency",
                generator_kind="source_agnostic",
                description="Adjacent-pair CX layer induced by an affine stride-1 boundary scan.",
                boundary_order=boundary_order,
            )
        )
    for offset in range(0, 20, 2):
        boundary_order = tuple((offset + 3 * index) % 20 for index in range(20))
        circuits.append(
            holographic_phase8_adjacent_cx_circuit(
                name=f"synth_affine_stride3_offset{offset}",
                generator_family="affine_modular_adjacency",
                generator_kind="source_agnostic",
                description="Adjacent-pair CX layer induced by an affine stride-3 boundary scan.",
                boundary_order=boundary_order,
            )
        )
    hierarchical_templates = (
        (
            "synth_bit_reversal_5bit",
            tuple(sorted(range(20), key=lambda qubit: (holographic_phase5_bit_reverse(qubit, width=5), qubit))),
            "Adjacent-pair CX layer induced by five-bit reversal order.",
        ),
        (
            "synth_gray_code_5bit",
            tuple(sorted(range(20), key=lambda qubit: (holographic_phase5_gray_code(qubit), qubit))),
            "Adjacent-pair CX layer induced by five-bit Gray-code order.",
        ),
        (
            "synth_bitrev_gray_5bit",
            tuple(
                sorted(
                    range(20),
                    key=lambda qubit: (
                        holographic_phase5_bit_reverse(holographic_phase5_gray_code(qubit), width=5),
                        qubit,
                    ),
                )
            ),
            "Adjacent-pair CX layer induced by bit-reversed Gray-code order.",
        ),
        (
            "synth_even_odd_position_shuffle",
            tuple(range(0, 20, 2)) + tuple(range(1, 20, 2)),
            "Adjacent-pair CX layer induced by an even/odd position shuffle.",
        ),
    )
    for name, boundary_order, description in hierarchical_templates:
        circuits.append(
            holographic_phase8_adjacent_cx_circuit(
                name=name,
                generator_family="hierarchical_bit_adjacency",
                generator_kind="source_agnostic",
                description=description,
                boundary_order=boundary_order,
            )
        )
    circuits.extend(
        (
            holographic_phase8_adjacent_cx_circuit(
                name="synth_riffle_natural_halves",
                generator_family="butterfly_riffle_adjacency",
                generator_kind="source_agnostic_frontier_control",
                description="Adjacent-pair CX layer induced by riffled natural halves; included as a distance-gate control.",
                boundary_order=holographic_phase5_riffle_halves(tuple(range(20))),
            ),
            holographic_phase8_adjacent_cx_circuit(
                name="synth_inner_major_natural",
                generator_family="tensor_product_adjacency",
                generator_kind="source_agnostic_frontier_control",
                description="Adjacent-pair CX layer induced by natural inner-position-major tensor-product order.",
                boundary_order=tuple(block * 5 + inner for inner in range(5) for block in range(4)),
            ),
            holographic_phase8_adjacent_cx_circuit(
                name="synth_block_major_phase2_inner_ring",
                generator_family="phase2_seeded_tensor_product_adjacency",
                generator_kind="phase2_seeded",
                description="Adjacent-pair CX layer induced by block-major Phase-2 inner-ring tensor-product order.",
                boundary_order=tuple(block * 5 + inner for block in range(4) for inner in (0, 1, 2, 4, 3)),
            ),
            holographic_phase8_adjacent_cx_circuit(
                name="synth_inner_major_phase2_inner_ring",
                generator_family="phase2_seeded_tensor_product_adjacency",
                generator_kind="phase2_seeded_frontier_control",
                description="Adjacent-pair CX layer induced by inner-major Phase-2 inner-ring tensor-product order.",
                boundary_order=tuple(block * 5 + inner for inner in (0, 1, 2, 4, 3) for block in range(4)),
            ),
        )
    )
    return tuple(circuits)


def holographic_phase8_length_distribution(
    hits: tuple[dict[str, object], ...],
    *,
    max_interval_length: int,
) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "length": length,
            "hit_count": sum(1 for hit in hits if int(hit["region"]["length"]) == length),  # type: ignore[index]
        }
        for length in range(1, max_interval_length + 1)
    )


def holographic_phase8_family_summary(records: tuple[dict[str, object], ...]) -> tuple[dict[str, object], ...]:
    families = sorted({str(record["generator_family"]) for record in records})
    return tuple(
        {
            "generator_family": family,
            "circuits": sum(1 for record in records if record["generator_family"] == family),
            "distance_preserving_circuits": sum(
                1
                for record in records
                if record["generator_family"] == family
                and record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
            ),
            "distance_gate_rejections": sum(
                1
                for record in records
                if record["generator_family"] == family
                and not record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
            ),
            "operator_or_channel_hits": sum(
                int(record["interval_search"]["hit_count"])  # type: ignore[index]
                for record in records
                if record["generator_family"] == family
            ),
        }
        for family in families
    )


def bridge_holography_phase8_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 6,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 6:
        raise ValueError("max_interval_length must be at least six for the Phase 8 certificate")
    repaired_source = holographic_phase3_repaired_source(graph_max_codes=graph_max_codes)
    first = repaired_source["first"]
    second = repaired_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 8 repaired source must contain StabilizerCode objects")
    fixed_phase3_region_mask = lift_inner_region_over_blocks(
        mask_from_qubits((2, 4)),
        block_mask=3,
        block_size=5,
        block_count=4,
    )
    circuits = holographic_phase8_synthesis_templates()
    circuit_records = tuple(
        {
            **holographic_phase7_circuit_search_record(
                first=first,
                second=second,
                circuit=circuit,
                fixed_phase3_region_mask=fixed_phase3_region_mask,
                max_interval_length=max_interval_length,
            ),
            "generator_family": circuit["generator_family"],
        }
        for circuit in circuits
    )
    all_hits = tuple(
        hit
        for record in circuit_records
        for hit in record["hit_records"]  # type: ignore[index]
    )
    distance_preserving_records = tuple(
        record
        for record in circuit_records
        if record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
    )
    distance_rejected_records = tuple(
        record
        for record in circuit_records
        if not record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
    )
    distance_preserving_hits = tuple(
        hit
        for record in distance_preserving_records
        for hit in record["hit_records"]  # type: ignore[index]
    )
    low_distance_frontier_hits = tuple(
        hit
        for record in distance_rejected_records
        for hit in record["hit_records"]  # type: ignore[index]
    )
    hierarchical_distance_hits = tuple(
        hit
        for record in distance_preserving_records
        if record["generator_family"] == "hierarchical_bit_adjacency"
        for hit in record["hit_records"]  # type: ignore[index]
    )
    affine_distance_records = tuple(
        record for record in distance_preserving_records if record["generator_family"] == "affine_modular_adjacency"
    )
    best_distance_preserving_hit = min(
        distance_preserving_hits,
        key=lambda hit: (
            int(hit["region"]["length"]),  # type: ignore[index]
            str(hit["circuit"]["name"]),  # type: ignore[index]
            int(hit["region"]["start"]),  # type: ignore[index]
        ),
    )
    best_frontier_hit = min(
        low_distance_frontier_hits,
        key=lambda hit: (
            int(hit["region"]["length"]),  # type: ignore[index]
            str(hit["circuit"]["name"]),  # type: ignore[index]
            int(hit["region"]["start"]),  # type: ignore[index]
        ),
    )
    block_major_phase2_record = next(
        record for record in circuit_records if record["name"] == "synth_block_major_phase2_inner_ring"
    )
    distance_hit_lengths = tuple(int(hit["region"]["length"]) for hit in distance_preserving_hits)  # type: ignore[index]
    frontier_hit_lengths = tuple(int(hit["region"]["length"]) for hit in low_distance_frontier_hits)  # type: ignore[index]
    total_intervals = sum(int(record["interval_search"]["intervals_scanned"]) for record in circuit_records)  # type: ignore[index]
    entropy_gate_passes = sum(int(record["interval_search"]["entropy_gate_passes"]) for record in circuit_records)  # type: ignore[index]
    entropy_gate_rejections = sum(int(record["interval_search"]["entropy_gate_rejections"]) for record in circuit_records)  # type: ignore[index]
    phase_claims = {
        "phase3_repaired_source_loaded": repaired_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "synthesis_menu_scored": len(circuit_records) == 38
        and len({record["gates"] for record in circuit_records}) == 38,
        "all_candidate_mincuts_exact": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in circuit_records  # type: ignore[index]
        ),
        "distance_gate_exact_weight_one_for_all_layers": all(
            record["distance_audit"]["first"]["max_weight_checked"] == 1  # type: ignore[index]
            and record["distance_audit"]["second"]["max_weight_checked"] == 1  # type: ignore[index]
            for record in circuit_records
        ),
        "distance_gate_accepts_and_rejects_layers": len(distance_preserving_records) == 35
        and len(distance_rejected_records) == 3,
        "all_reported_hits_are_entropy_matched_operator_or_channel_splits": all(
            hit["comparisons"]["entropy_matches"]  # type: ignore[index]
            and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for hit in all_hits
        ),
        "distance_preserving_hits_exist": bool(distance_preserving_hits),
        "distance_preserving_min_length_four": bool(distance_hit_lengths) and min(distance_hit_lengths) == 4,
        "no_distance_preserving_hits_below_length_four": all(length >= 4 for length in distance_hit_lengths),
        "hierarchical_gray_layers_improve_over_affine_length_six": bool(hierarchical_distance_hits)
        and min(int(hit["region"]["length"]) for hit in hierarchical_distance_hits) == 4
        and all(
            int(hit["region"]["length"]) == 6
            for record in affine_distance_records
            for hit in record["hit_records"]  # type: ignore[index]
        ),
        "frontier_one_qubit_hits_rejected_by_distance_gate": bool(frontier_hit_lengths)
        and min(frontier_hit_lengths) == 1
        and all(
            not record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
            for record in distance_rejected_records
        ),
        "fixed_patch_split_does_not_imply_compact_hit": bool(
            block_major_phase2_record["fixed_phase3_patch"]["operator_or_channel_split"]  # type: ignore[index]
        )
        and int(block_major_phase2_record["interval_search"]["hit_count"]) == 0,
    }
    phase_claims["goal_3_phase_8_distance_gated_clifford_synthesis_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 8: distance-gated Clifford synthesis search",
        "status": "pass" if phase_claims["goal_3_phase_8_distance_gated_clifford_synthesis_certificate"] else "fail",
        "repair_source": {
            key: value
            for key, value in repaired_source.items()
            if key not in ("first", "second")
        },
        "search_scope": {
            "synthesis_rule": "adjacent-pair CX layers induced by bounded generated boundary orders",
            "affine_layers": "20 stride-1 offsets plus 10 even stride-3 offsets",
            "hierarchical_layers": (
                "bit reversal, Gray code, bit-reversed Gray code, and even/odd position shuffle"
            ),
            "frontier_controls": (
                "riffled natural halves, inner-major natural tensor order, block-major Phase-2 order, and "
                "inner-major Phase-2 order"
            ),
            "candidate_patch_rule": "all compact output-boundary ring intervals of length 1 through 6",
            "distance_gate": "weight-one logical exclusion for both transformed codes",
        },
        "family_summary": holographic_phase8_family_summary(circuit_records),
        "circuit_records": circuit_records,
        "selected_distance_preserving_hit": best_distance_preserving_hit,
        "selected_frontier_rejected_hit": best_frontier_hit,
        "selected_fixed_patch_no_compact_hit_record": {
            "name": block_major_phase2_record["name"],
            "generator_family": block_major_phase2_record["generator_family"],
            "distance_audit": block_major_phase2_record["distance_audit"],
            "fixed_phase3_patch": block_major_phase2_record["fixed_phase3_patch"],
            "interval_search": block_major_phase2_record["interval_search"],
        },
        "hit_length_distributions": {
            "distance_preserving": holographic_phase8_length_distribution(
                distance_preserving_hits,
                max_interval_length=max_interval_length,
            ),
            "low_distance_frontier": holographic_phase8_length_distribution(
                low_distance_frontier_hits,
                max_interval_length=max_interval_length,
            ),
        },
        "counts": {
            "synthesized_circuits": len(circuit_records),
            "unique_cx_layers": len({record["gates"] for record in circuit_records}),
            "candidate_intervals_scanned": total_intervals,
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "operator_or_channel_hits": len(all_hits),
            "distance_preserving_circuits": len(distance_preserving_records),
            "distance_gate_rejections": len(distance_rejected_records),
            "distance_preserving_hits": len(distance_preserving_hits),
            "low_distance_frontier_hits": len(low_distance_frontier_hits),
            "min_distance_preserving_hit_length": min(distance_hit_lengths),
            "min_low_distance_frontier_hit_length": min(frontier_hit_lengths),
            "hierarchical_distance_preserving_hits": len(hierarchical_distance_hits),
            "affine_distance_preserving_hits": sum(
                int(record["interval_search"]["hit_count"]) for record in affine_distance_records  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(record["network"]["internal_nodes"]) for record in circuit_records  # type: ignore[arg-type,index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded synthesis grammar over adjacent-pair CX layers finds distance-preserving compact "
                "operator/channel witnesses without fixing the old Phase 3 patch. Hierarchical Gray-code-style "
                "layers improve the shortest robust compact witness from the Phase 7 length-six replacement down "
                "to length four."
            ),
            "three_geometry_lesson": (
                "The distance gate filters dramatic one-site frontier hits, while entropy/min-cut-visible compact "
                "patches of the same size can still carry different logical algebra and erasure semantics. Boundary "
                "order and tensor layer jointly control which observer patches are compact."
            ),
            "scope_warning": (
                "This is exhaustive only for the stated 38 adjacent-pair CX layers and interval length <= 6. The "
                "distance claim is still the exact weight-one audit used in the repaired-code phases, not a full "
                "distance computation for every transformed code."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 8 confirms that distance-preserving synthesized Clifford layers can create stricter compact "
                "holographic witnesses, but the grammar is still adjacency-layer based. The next step should move "
                "from pairwise CX layers toward small perfect-tensor/HaPPY-like stabilizer blocks or two-layer "
                "distance-gated circuits."
            ),
            "suggested_phase_9": (
                "Build a small HaPPY/perfect-tensor-inspired stabilizer block audit: compose seed tensors or "
                "two-layer Clifford blocks, keep the distance gate hard, and replay exact entropy, min-cut, "
                "operator-algebra, erasure, survivor, and compact-patch checks."
            ),
        },
    }


def holographic_phase9_seed_template_names() -> tuple[str, ...]:
    return (
        "synth_affine_stride1_offset0",
        "synth_affine_stride1_offset1",
        "synth_affine_stride1_offset5",
        "synth_affine_stride3_offset0",
        "synth_affine_stride3_offset2",
        "synth_bit_reversal_5bit",
        "synth_gray_code_5bit",
        "synth_bitrev_gray_5bit",
        "synth_even_odd_position_shuffle",
        "synth_block_major_phase2_inner_ring",
        "synth_riffle_natural_halves",
        "synth_inner_major_natural",
        "synth_inner_major_phase2_inner_ring",
    )


def holographic_phase9_block_menu_pairs() -> tuple[tuple[str, str], ...]:
    return (
        ("synth_gray_code_5bit", "synth_bitrev_gray_5bit"),
        ("synth_bitrev_gray_5bit", "synth_gray_code_5bit"),
        ("synth_gray_code_5bit", "synth_gray_code_5bit"),
        ("synth_bitrev_gray_5bit", "synth_bitrev_gray_5bit"),
        ("synth_affine_stride1_offset0", "synth_gray_code_5bit"),
        ("synth_gray_code_5bit", "synth_affine_stride1_offset0"),
        ("synth_affine_stride1_offset0", "synth_bitrev_gray_5bit"),
        ("synth_bitrev_gray_5bit", "synth_affine_stride1_offset0"),
        ("synth_block_major_phase2_inner_ring", "synth_gray_code_5bit"),
        ("synth_gray_code_5bit", "synth_block_major_phase2_inner_ring"),
        ("synth_block_major_phase2_inner_ring", "synth_bitrev_gray_5bit"),
        ("synth_bitrev_gray_5bit", "synth_block_major_phase2_inner_ring"),
        ("synth_riffle_natural_halves", "synth_gray_code_5bit"),
        ("synth_gray_code_5bit", "synth_riffle_natural_halves"),
        ("synth_inner_major_natural", "synth_gray_code_5bit"),
        ("synth_gray_code_5bit", "synth_inner_major_natural"),
        ("synth_inner_major_phase2_inner_ring", "synth_gray_code_5bit"),
        ("synth_gray_code_5bit", "synth_inner_major_phase2_inner_ring"),
    )


def holographic_phase9_layer_short_name(name: str) -> str:
    return name.removeprefix("synth_")


def holographic_phase9_two_layer_circuit(
    first_layer: dict[str, object],
    second_layer: dict[str, object],
) -> dict[str, object]:
    first_name = str(first_layer["name"])
    second_name = str(second_layer["name"])
    return {
        "name": (
            f"pentagon_{holographic_phase9_layer_short_name(first_name)}"
            f"__then__{holographic_phase9_layer_short_name(second_name)}"
        ),
        "generator_kind": "two_layer_pentagon_block",
        "generator_family": "compressed_pentagon_two_layer",
        "description": (
            "Two adjacent-pair CX layers, interpreted through a compressed five-pentagon block min-cut skeleton."
        ),
        "first_layer": first_name,
        "second_layer": second_name,
        "boundary_order": tuple(int(qubit) for qubit in second_layer["boundary_order"]),  # type: ignore[index]
        "gates": tuple(tuple(gate) for gate in first_layer["gates"])  # type: ignore[index]
        + tuple(tuple(gate) for gate in second_layer["gates"]),  # type: ignore[index]
    }


def holographic_phase9_pentagon_block_network_spec(boundary_order: tuple[int, ...]) -> dict[str, object]:
    edges = list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = tuple(f"pentagon_block_{index}" for index in range(5))
    for block_index, node in enumerate(internal_nodes):
        for offset in range(4):
            qubit = boundary_order[(4 * block_index + offset) % len(boundary_order)]
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{qubit}",
                    edge_type="pentagon_boundary_leg",
                )
            )
    for block_index, node in enumerate(internal_nodes):
        edges.append(
            holographic_phase4_edge(
                node,
                internal_nodes[(block_index + 1) % len(internal_nodes)],
                edge_type="pentagon_internal_cycle",
                capacity=2,
            )
        )
    return {
        "name": "compressed_five_pentagon_block_skeleton",
        "network_kind": "compressed_haPPY_like_pentagon_cycle",
        "description": (
            "Five internal pentagon-like blocks, each attached to four consecutive output-boundary sites, "
            "with capacity-2 cycle links between neighboring blocks."
        ),
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase9_two_layer_distance_screen(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    templates_by_name: dict[str, dict[str, object]],
) -> dict[str, object]:
    records = []
    seed_names = holographic_phase9_seed_template_names()
    for first_name in seed_names:
        for second_name in seed_names:
            circuit = holographic_phase9_two_layer_circuit(
                templates_by_name[first_name],
                templates_by_name[second_name],
            )
            transformed_first = holographic_phase6_apply_circuit(first, circuit["gates"])  # type: ignore[arg-type]
            transformed_second = holographic_phase6_apply_circuit(second, circuit["gates"])  # type: ignore[arg-type]
            first_distance = bounded_distance_certificate(transformed_first, max_weight=1)
            second_distance = bounded_distance_certificate(transformed_second, max_weight=1)
            accepted = bool(
                first_distance["distance_at_least_2_certified"]
                and second_distance["distance_at_least_2_certified"]
            )
            records.append(
                {
                    "first_layer": first_name,
                    "second_layer": second_name,
                    "name": circuit["name"],
                    "distance_gate_accepted": accepted,
                    "first_distance": first_distance,
                    "second_distance": second_distance,
                }
            )
    accepted_records = tuple(record for record in records if record["distance_gate_accepted"])
    rejected_records = tuple(record for record in records if not record["distance_gate_accepted"])
    return {
        "seed_layers": seed_names,
        "ordered_pairs_checked": len(records),
        "accepted_pairs": len(accepted_records),
        "rejected_pairs": len(rejected_records),
        "rejected_pair_records": rejected_records,
    }


def holographic_phase9_two_layer_block_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    circuit: dict[str, object],
    fixed_phase3_region_mask: int,
    max_interval_length: int,
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in circuit["gates"])  # type: ignore[index]
    transformed_first = holographic_phase6_apply_circuit(first, gates)
    transformed_second = holographic_phase6_apply_circuit(second, gates)
    first_distance = bounded_distance_certificate(transformed_first, max_weight=1)
    second_distance = bounded_distance_certificate(transformed_second, max_weight=1)
    distance_preserving = bool(
        first_distance["distance_at_least_2_certified"]
        and second_distance["distance_at_least_2_certified"]
    )
    boundary_order = tuple(int(qubit) for qubit in circuit["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase9_pentagon_block_network_spec(boundary_order)
    fixed_patch = holographic_phase4_selected_witness_diagnostic(
        transformed_first,
        transformed_second,
        region_mask=fixed_phase3_region_mask,
    )
    fixed_patch_split = bool(
        fixed_patch["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
        or fixed_patch["comparisons"]["channel_visible_differs"]  # type: ignore[index]
    )
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    entropy_gate_passes = 0
    entropy_gate_rejections = 0
    all_min_cuts_exact = True
    length_summaries = []
    hit_records = []
    for length in range(1, max_interval_length + 1):
        length_intervals = tuple(region for region in intervals if int(region["length"]) == length)
        length_entropy_passes = 0
        length_hits = 0
        for region in length_intervals:
            region_mask = int(region["mask"])
            min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
            all_min_cuts_exact = all_min_cuts_exact and (
                min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"])  # type: ignore[arg-type]
            )
            first_entropy = transformed_first.entropy(region_mask)
            second_entropy = transformed_second.entropy(region_mask)
            if first_entropy != second_entropy:
                entropy_gate_rejections += 1
                continue
            entropy_gate_passes += 1
            length_entropy_passes += 1
            hit = holographic_phase7_hit_record(
                circuit=circuit,
                first=transformed_first,
                second=transformed_second,
                network_spec=network_spec,
                region=region,
            )
            if bool(hit["comparisons"]["operator_or_channel_visible_differs"]):  # type: ignore[index]
                hit_records.append(hit)
                length_hits += 1
        length_summaries.append(
            {
                "length": length,
                "intervals_scanned": len(length_intervals),
                "entropy_gate_passes": length_entropy_passes,
                "entropy_gate_rejections": len(length_intervals) - length_entropy_passes,
                "operator_or_channel_hits": length_hits,
            }
        )
    hits = tuple(hit_records)
    return {
        "name": circuit["name"],
        "generator_kind": circuit["generator_kind"],
        "generator_family": circuit["generator_family"],
        "description": circuit["description"],
        "first_layer": circuit["first_layer"],
        "second_layer": circuit["second_layer"],
        "boundary_order": boundary_order,
        "gate_counts": {
            "single_qubit": sum(1 for gate in gates if str(gate[0]) in ("H", "S")),
            "two_qubit": sum(1 for gate in gates if str(gate[0]) == "CX"),
            "total": len(gates),
        },
        "distance_audit": {
            "first": first_distance,
            "second": second_distance,
            "both_codes_distance_at_least_2_under_weight_one_audit": distance_preserving,
        },
        "fixed_phase3_patch": {
            "diagnostic": fixed_patch,
            "operator_or_channel_split": fixed_patch_split,
        },
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
            "internal_assignments_per_min_cut": 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
        "interval_search": {
            "candidate_rule": "all output-boundary ring intervals with length <= max_interval_length",
            "max_interval_length": max_interval_length,
            "intervals_scanned": len(intervals),
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "all_candidate_min_cuts_exact": all_min_cuts_exact,
            "length_summaries": tuple(length_summaries),
            "hit_count": len(hits),
            "shortest_hit_length": min((int(hit["region"]["length"]) for hit in hits), default=None),  # type: ignore[index]
        },
        "hit_records": hits,
    }


def bridge_holography_phase9_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 6,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 6:
        raise ValueError("max_interval_length must be at least six for the Phase 9 certificate")
    repaired_source = holographic_phase3_repaired_source(graph_max_codes=graph_max_codes)
    first = repaired_source["first"]
    second = repaired_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 9 repaired source must contain StabilizerCode objects")
    fixed_phase3_region_mask = lift_inner_region_over_blocks(
        mask_from_qubits((2, 4)),
        block_mask=3,
        block_size=5,
        block_count=4,
    )
    templates_by_name = {str(circuit["name"]): circuit for circuit in holographic_phase8_synthesis_templates()}
    distance_screen = holographic_phase9_two_layer_distance_screen(
        first=first,
        second=second,
        templates_by_name=templates_by_name,
    )
    block_menu_pairs = holographic_phase9_block_menu_pairs()
    block_circuits = tuple(
        holographic_phase9_two_layer_circuit(
            templates_by_name[first_name],
            templates_by_name[second_name],
        )
        for first_name, second_name in block_menu_pairs
    )
    circuit_records = tuple(
        holographic_phase9_two_layer_block_record(
            first=first,
            second=second,
            circuit=circuit,
            fixed_phase3_region_mask=fixed_phase3_region_mask,
            max_interval_length=max_interval_length,
        )
        for circuit in block_circuits
    )
    all_hits = tuple(
        hit
        for record in circuit_records
        for hit in record["hit_records"]  # type: ignore[index]
    )
    distance_preserving_records = tuple(
        record
        for record in circuit_records
        if record["distance_audit"]["both_codes_distance_at_least_2_under_weight_one_audit"]  # type: ignore[index]
    )
    distance_preserving_hits = tuple(
        hit
        for record in distance_preserving_records
        for hit in record["hit_records"]  # type: ignore[index]
    )
    hit_lengths = tuple(int(hit["region"]["length"]) for hit in distance_preserving_hits)  # type: ignore[index]
    best_hit = min(
        distance_preserving_hits,
        key=lambda hit: (
            int(hit["region"]["length"]),  # type: ignore[index]
            str(hit["circuit"]["name"]),  # type: ignore[index]
            int(hit["region"]["start"]),  # type: ignore[index]
        ),
    )
    total_intervals = sum(int(record["interval_search"]["intervals_scanned"]) for record in circuit_records)  # type: ignore[index]
    entropy_gate_passes = sum(int(record["interval_search"]["entropy_gate_passes"]) for record in circuit_records)  # type: ignore[index]
    entropy_gate_rejections = sum(int(record["interval_search"]["entropy_gate_rejections"]) for record in circuit_records)  # type: ignore[index]
    phase_claims = {
        "phase3_repaired_source_loaded": repaired_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "two_layer_distance_screen_scored": distance_screen["ordered_pairs_checked"] == 169
        and distance_screen["accepted_pairs"] == 153
        and distance_screen["rejected_pairs"] == 16,
        "pentagon_block_menu_scored": len(circuit_records) == 18
        and len({(record["first_layer"], record["second_layer"]) for record in circuit_records}) == 18,
        "all_block_menu_circuits_distance_preserving": len(distance_preserving_records) == len(circuit_records),
        "all_candidate_mincuts_exact_on_compressed_skeleton": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in circuit_records  # type: ignore[index]
        ),
        "compressed_skeleton_has_five_internal_blocks": all(
            len(record["network"]["internal_nodes"]) == 5  # type: ignore[arg-type,index]
            and record["network"]["internal_assignments_per_min_cut"] == 32  # type: ignore[index]
            for record in circuit_records
        ),
        "all_reported_hits_are_entropy_matched_operator_or_channel_splits": all(
            hit["comparisons"]["entropy_matches"]  # type: ignore[index]
            and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for hit in all_hits
        ),
        "distance_preserving_length_two_hits_exist": bool(hit_lengths) and min(hit_lengths) == 2,
        "no_distance_preserving_length_one_hits": all(length >= 2 for length in hit_lengths),
        "two_layer_compressed_blocks_improve_over_phase8_length_four": bool(hit_lengths) and min(hit_lengths) < 4,
    }
    phase_claims["goal_3_phase_9_compressed_pentagon_two_layer_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 9: compressed pentagon two-layer block audit",
        "status": "pass" if phase_claims["goal_3_phase_9_compressed_pentagon_two_layer_certificate"] else "fail",
        "repair_source": {
            key: value
            for key, value in repaired_source.items()
            if key not in ("first", "second")
        },
        "distance_screen": distance_screen,
        "search_scope": {
            "code_dynamics": "two exact adjacent-pair CX layers are applied to both repaired stabilizer codes",
            "min_cut_geometry": (
                "compressed five-pentagon block skeleton on the output boundary order; exact min-cut enumerates "
                "all 2^5 internal block assignments"
            ),
            "block_menu_pairs": block_menu_pairs,
            "candidate_patch_rule": "all compact output-boundary ring intervals of length 1 through 6",
            "distance_gate": "weight-one logical exclusion for both transformed codes",
        },
        "network_template": holographic_phase9_pentagon_block_network_spec(tuple(range(20))),
        "circuit_records": circuit_records,
        "selected_distance_preserving_hit": best_hit,
        "hit_length_distribution": holographic_phase8_length_distribution(
            distance_preserving_hits,
            max_interval_length=max_interval_length,
        ),
        "counts": {
            "distance_screen_seed_layers": len(holographic_phase9_seed_template_names()),
            "distance_screen_ordered_pairs": distance_screen["ordered_pairs_checked"],
            "distance_screen_accepted_pairs": distance_screen["accepted_pairs"],
            "distance_screen_rejected_pairs": distance_screen["rejected_pairs"],
            "block_menu_circuits": len(circuit_records),
            "distance_preserving_block_menu_circuits": len(distance_preserving_records),
            "candidate_intervals_scanned": total_intervals,
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "operator_or_channel_hits": len(all_hits),
            "distance_preserving_hits": len(distance_preserving_hits),
            "min_distance_preserving_hit_length": min(hit_lengths),
            "max_candidate_min_cut_internal_assignments": max(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in circuit_records  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A two-layer Clifford block audit with compressed five-pentagon min-cut geometry finds "
                "distance-preserving compact witnesses of length two. This improves the Phase 8 one-layer "
                "adjacency result, whose robust compact witnesses first appeared at length four."
            ),
            "three_geometry_lesson": (
                "Compressing the tensor-network geometry changes which observer patches are compact, while exact "
                "operator and erasure diagnostics still separate the two code realizations. The distance screen "
                "also shows that many two-layer compositions preserve the repaired-code weight-one gate, but not all."
            ),
            "scope_warning": (
                "The code transformations are exact two-layer Clifford circuits. The min-cut geometry is a declared "
                "compressed pentagon-block skeleton, not the full 20-gate interaction graph and not a proof about "
                "continuum HaPPY networks. The distance claim remains an exact weight-one audit."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 9 shows that a HaPPY-like compressed block atlas can make the robust witness more compact. "
                "The next adaptation should test literal stabilizer perfect-tensor blocks or add a full-distance "
                "audit for the best transformed codes."
            ),
            "suggested_phase_10": (
                "Either construct a small [[5,1,3]]/perfect-tensor-inspired stabilizer network with exact boundary "
                "region diagnostics, or compute stronger distance certificates for the best Phase 8/9 transformed "
                "code pairs."
            ),
        },
    }


def holographic_phase10_five_qubit_perfect_code() -> StabilizerCode:
    return StabilizerCode.from_pauli_strings(("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"))


def holographic_phase10_outer_code_summary(outer: StabilizerCode) -> dict[str, object]:
    erasure_counts = tuple(
        {
            "size": size,
            "erasure_correctable_regions": sum(1 for mask in masks_of_size(outer.n, size) if outer.erasure_correctable(mask)),
            "reconstructing_regions": sum(1 for mask in masks_of_size(outer.n, size) if outer.reconstructs_all_logicals(mask)),
        }
        for size in range(outer.n + 1)
    )
    return {
        "name": "canonical_five_qubit_perfect_code",
        "parameters": {"n": outer.n, "k": outer.k, "distance": outer.distance()},
        "generators": outer.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
        "erasure_threshold": outer.erasure_threshold(),
        "erasure_reconstruction_counts_by_size": erasure_counts,
        "perfect_tensor_like_checks": {
            "all_size_two_or_less_erasures_correctable": all(
                outer.erasure_correctable(mask)
                for size in range(0, 3)
                for mask in masks_of_size(outer.n, size)
            ),
            "all_size_three_regions_reconstruct": all(
                outer.reconstructs_all_logicals(mask) for mask in masks_of_size(outer.n, 3)
            ),
        },
    }


def holographic_phase10_perfect_outer_source(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 10 source must contain StabilizerCode objects")
    outer = holographic_phase10_five_qubit_perfect_code()
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    return {
        "name": "goal3_phase10_graph_cws_perfect_outer_concatenation",
        "source_type": "literal_five_qubit_perfect_outer_concatenation",
        "origin": (
            "Goal 3 Phase 2 graph/CWS ring witness concatenated with the canonical [[5,1,3]] five-qubit code"
        ),
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "outer_code": holographic_phase10_outer_code_summary(outer),
        "first": first,
        "second": second,
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
    }


def holographic_phase10_boundary_templates() -> tuple[dict[str, object], ...]:
    inner_order = (0, 1, 2, 4, 3)
    block_size = 5
    block_count = 5
    block_contiguous = tuple(block * block_size + qubit for block in range(block_count) for qubit in inner_order)
    inner_major = tuple(block * block_size + qubit for qubit in inner_order for block in range(block_count))
    witness_prefix = tuple(block * block_size + qubit for block in range(block_count) for qubit in (2, 4))
    witness_set = set(witness_prefix)
    witness_strip = witness_prefix + tuple(qubit for qubit in block_contiguous if qubit not in witness_set)
    return (
        {
            "name": "perfect_outer_block_contiguous",
            "template_kind": "block_local",
            "description": "Repeat the Phase 2 inner ring inside each five-qubit perfect-code outer block.",
            "boundary_order": block_contiguous,
        },
        {
            "name": "perfect_outer_inner_major",
            "template_kind": "perfect_outer_tensor_product",
            "description": "Group equal inner positions across the five perfect-code outer blocks.",
            "boundary_order": inner_major,
        },
        {
            "name": "perfect_outer_witness_strip",
            "template_kind": "source_aware_control",
            "description": "Place all lifted Phase 2 witness qubits first, then append the block-contiguous remainder.",
            "boundary_order": witness_strip,
        },
    )


def holographic_phase10_perfect_outer_network_spec(boundary_order: tuple[int, ...]) -> dict[str, object]:
    edges = list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = tuple(f"perfect_outer_block_{block}" for block in range(5))
    for block, node in enumerate(internal_nodes):
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="perfect_outer_block_leg",
                )
            )
    for block, node in enumerate(internal_nodes):
        edges.append(
            holographic_phase4_edge(
                node,
                internal_nodes[(block + 1) % len(internal_nodes)],
                edge_type="perfect_outer_block_cycle",
                capacity=2,
            )
        )
    return {
        "name": "literal_five_qubit_perfect_outer_block_skeleton",
        "network_kind": "five_qubit_perfect_outer_block_cycle",
        "description": (
            "Five internal nodes represent the five [[5,1,3]] outer-code blocks; each attaches to its five inner "
            "physical qubits and to neighboring outer blocks on a capacity-2 cycle."
        ),
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase10_distance_audit(first: StabilizerCode, second: StabilizerCode) -> dict[str, object]:
    first_distance = bounded_distance_certificate(first, max_weight=3)
    second_distance = bounded_distance_certificate(second, max_weight=4)
    return {
        "first": first_distance,
        "second": second_distance,
        "first_exact_distance": first_distance["distance_exact_if_witness_found"],
        "second_exact_distance": second_distance["distance_exact_if_witness_found"],
        "both_distance_at_least_3": int(first_distance["distance_lower_bound"]) >= 3
        and int(second_distance["distance_lower_bound"]) >= 3,
        "exact_distance_profile_differs": first_distance["distance_exact_if_witness_found"]
        != second_distance["distance_exact_if_witness_found"],
    }


def holographic_phase10_interval_template_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    template: dict[str, object],
    max_interval_length: int,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase10_perfect_outer_network_spec(boundary_order)
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    entropy_gate_passes = 0
    entropy_gate_rejections = 0
    all_min_cuts_exact = True
    length_summaries = []
    hit_records = []
    circuit = {
        "name": template["name"],
        "generator_kind": "literal_perfect_outer_block_atlas",
    }
    for length in range(1, max_interval_length + 1):
        length_intervals = tuple(region for region in intervals if int(region["length"]) == length)
        length_entropy_passes = 0
        length_hits = 0
        for region in length_intervals:
            region_mask = int(region["mask"])
            min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
            all_min_cuts_exact = all_min_cuts_exact and (
                min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"])  # type: ignore[arg-type]
            )
            first_entropy = first.entropy(region_mask)
            second_entropy = second.entropy(region_mask)
            if first_entropy != second_entropy:
                entropy_gate_rejections += 1
                continue
            entropy_gate_passes += 1
            length_entropy_passes += 1
            hit = holographic_phase7_hit_record(
                circuit=circuit,
                first=first,
                second=second,
                network_spec=network_spec,
                region=region,
            )
            if bool(hit["comparisons"]["operator_or_channel_visible_differs"]):  # type: ignore[index]
                hit_records.append(hit)
                length_hits += 1
        length_summaries.append(
            {
                "length": length,
                "intervals_scanned": len(length_intervals),
                "entropy_gate_passes": length_entropy_passes,
                "entropy_gate_rejections": len(length_intervals) - length_entropy_passes,
                "operator_or_channel_hits": length_hits,
            }
        )
    hits = tuple(hit_records)
    return {
        "name": template["name"],
        "template_kind": template["template_kind"],
        "description": template["description"],
        "boundary_order": boundary_order,
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
            "internal_assignments_per_min_cut": 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
        "interval_search": {
            "max_interval_length": max_interval_length,
            "intervals_scanned": len(intervals),
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "all_candidate_min_cuts_exact": all_min_cuts_exact,
            "length_summaries": tuple(length_summaries),
            "hit_count": len(hits),
            "shortest_hit_length": min((int(hit["region"]["length"]) for hit in hits), default=None),  # type: ignore[index]
        },
        "hit_records": hits,
    }


def holographic_phase10_lifted_witness_records(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    boundary_order: tuple[int, ...],
) -> tuple[dict[str, object], ...]:
    base_inner_region = mask_from_qubits((2, 4))
    network_spec = holographic_phase10_perfect_outer_network_spec(boundary_order)
    circuit = {
        "name": "perfect_outer_lifted_phase2_witness",
        "generator_kind": "literal_perfect_outer_lifted_witness",
    }
    records = []
    for block_mask in range(1, 1 << 5):
        region_mask = lift_inner_region_over_blocks(
            base_inner_region,
            block_mask=block_mask,
            block_size=5,
            block_count=5,
        )
        region = {
            "name": f"perfect_outer_lifted_24_blocks_{block_mask}",
            "region_type": "perfect_outer_lifted_phase2_interval",
            "base_inner_qubits": (2, 4),
            "block_mask": block_mask,
            "block_count": block_mask.bit_count(),
            "qubits": mask_to_tuple(region_mask, first.n),
            "mask": region_mask,
        }
        first_entropy = first.entropy(region_mask)
        second_entropy = second.entropy(region_mask)
        if first_entropy != second_entropy:
            min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
            record = {
                "region": {key: value for key, value in region.items() if key != "mask"},
                "min_cut": holographic_phase7_min_cut_summary(min_cut),
                "first": {"entropy": first_entropy},
                "second": {"entropy": second_entropy},
                "comparisons": {
                    "entropy_matches": False,
                    "operator_or_channel_visible_differs": False,
                },
            }
        else:
            record = holographic_phase7_hit_record(
                circuit=circuit,
                first=first,
                second=second,
                network_spec=network_spec,
                region=region,
            )
        record["interval_location"] = holographic_phase3_interval_location(
            boundary_order=boundary_order,
            region_mask=region_mask,
        )
        records.append(record)
    return tuple(records)


def bridge_holography_phase10_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 8,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 8:
        raise ValueError("max_interval_length must be at least eight for the Phase 10 certificate")
    perfect_source = holographic_phase10_perfect_outer_source(graph_max_codes=graph_max_codes)
    first = perfect_source["first"]
    second = perfect_source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 10 perfect outer source must contain StabilizerCode objects")
    distance_audit = holographic_phase10_distance_audit(first, second)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    templates = holographic_phase10_boundary_templates()
    template_records = tuple(
        holographic_phase10_interval_template_record(
            first=first,
            second=second,
            template=template,
            max_interval_length=max_interval_length,
        )
        for template in templates
    )
    template_by_name = {str(record["name"]): record for record in template_records}
    inner_major = template_by_name["perfect_outer_inner_major"]
    block_contiguous = template_by_name["perfect_outer_block_contiguous"]
    witness_strip = template_by_name["perfect_outer_witness_strip"]
    inner_major_hits = tuple(inner_major["hit_records"])  # type: ignore[index]
    selected_interval_hit = min(
        inner_major_hits,
        key=lambda hit: (int(hit["region"]["length"]), int(hit["region"]["start"])),  # type: ignore[index]
    )
    witness_strip_order = tuple(int(qubit) for qubit in witness_strip["boundary_order"])  # type: ignore[index]
    lifted_records = holographic_phase10_lifted_witness_records(
        first=first,
        second=second,
        boundary_order=witness_strip_order,
    )
    lifted_hits = tuple(
        record
        for record in lifted_records
        if record["comparisons"].get("entropy_matches")  # type: ignore[union-attr]
        and record["comparisons"].get("operator_or_channel_visible_differs")  # type: ignore[union-attr]
    )
    strict_lifted_hits = tuple(
        record
        for record in lifted_hits
        if record["interval_location"]["is_boundary_ring_interval"]  # type: ignore[index]
    )
    selected_lifted_hit = next(
        record
        for record in strict_lifted_hits
        if int(record["region"]["block_mask"]) == 7  # type: ignore[index]
    )
    all_interval_hits = tuple(
        hit
        for record in template_records
        for hit in record["hit_records"]  # type: ignore[index]
    )
    phase_claims = {
        "phase2_graph_source_loaded": perfect_source["phase2_graph_search"]["status"] == "pair-found",  # type: ignore[index]
        "outer_code_is_five_qubit_perfect_code": perfect_source["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
        and perfect_source["outer_code"]["erasure_threshold"] == 2  # type: ignore[index]
        and perfect_source["outer_code"]["perfect_tensor_like_checks"]["all_size_two_or_less_erasures_correctable"]  # type: ignore[index]
        and perfect_source["outer_code"]["perfect_tensor_like_checks"]["all_size_three_regions_reconstruct"],  # type: ignore[index]
        "perfect_outer_concatenation_k1_n25": first.n == second.n == 25 and first.k == second.k == 1,
        "exact_distance_profile_certified": distance_audit["first_exact_distance"] == 3
        and distance_audit["second_exact_distance"] == 4,
        "both_distances_at_least_three": distance_audit["both_distance_at_least_3"],
        "all_labeled_t2_entropy_matches": low_order_entropy["matches"],
        "three_boundary_atlases_scored": len(template_records) == 3,
        "all_interval_mincuts_exact": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in template_records  # type: ignore[index]
        ),
        "block_contiguous_has_no_compact_hits": int(block_contiguous["interval_search"]["hit_count"]) == 0,  # type: ignore[index]
        "inner_major_has_length_three_compact_hits": int(inner_major["interval_search"]["shortest_hit_length"]) == 3,  # type: ignore[index]
        "lifted_three_block_witnesses_exist": len(lifted_hits) == 10
        and all(int(record["region"]["block_count"]) == 3 for record in lifted_hits),  # type: ignore[index]
        "source_aware_lifted_strict_hits_exist": len(strict_lifted_hits) == 3,
    }
    phase_claims["goal_3_phase_10_five_qubit_perfect_outer_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 10: five-qubit perfect outer-block audit",
        "status": "pass" if phase_claims["goal_3_phase_10_five_qubit_perfect_outer_certificate"] else "fail",
        "perfect_outer_source": {
            key: value
            for key, value in perfect_source.items()
            if key not in ("first", "second")
        },
        "code_pair": {
            "n": first.n,
            "k": first.k,
            "first_generators": first.pauli_generators(),
            "second_generators": second.pauli_generators(),
        },
        "distance_audit": distance_audit,
        "low_order_entropy": low_order_entropy,
        "boundary_atlas_search": {
            "max_interval_length": max_interval_length,
            "templates": template_records,
            "selected_interval_hit": selected_interval_hit,
        },
        "lifted_phase2_witness_audit": {
            "base_inner_qubits": (2, 4),
            "block_masks_checked": len(lifted_records),
            "records": lifted_records,
            "accepted_lifted_hits": lifted_hits,
            "strict_lifted_hits": strict_lifted_hits,
            "selected_lifted_hit": selected_lifted_hit,
        },
        "counts": {
            "low_order_subsets_checked": low_order_entropy["subsets_checked"],
            "low_order_entropy_mismatches": low_order_entropy["mismatch_count"],
            "boundary_atlases": len(template_records),
            "candidate_intervals_scanned": sum(
                int(record["interval_search"]["intervals_scanned"]) for record in template_records  # type: ignore[index]
            ),
            "entropy_gate_passes": sum(
                int(record["interval_search"]["entropy_gate_passes"]) for record in template_records  # type: ignore[index]
            ),
            "entropy_gate_rejections": sum(
                int(record["interval_search"]["entropy_gate_rejections"]) for record in template_records  # type: ignore[index]
            ),
            "compact_interval_hits": len(all_interval_hits),
            "block_contiguous_hits": int(block_contiguous["interval_search"]["hit_count"]),  # type: ignore[index]
            "inner_major_hits": int(inner_major["interval_search"]["hit_count"]),  # type: ignore[index]
            "witness_strip_hits": int(witness_strip["interval_search"]["hit_count"]),  # type: ignore[index]
            "min_inner_major_hit_length": int(inner_major["interval_search"]["shortest_hit_length"]),  # type: ignore[index]
            "lifted_block_masks_checked": len(lifted_records),
            "lifted_three_block_hits": len(lifted_hits),
            "strict_lifted_hits": len(strict_lifted_hits),
            "max_candidate_min_cut_internal_assignments": max(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in template_records  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Using the literal [[5,1,3]] five-qubit code as the outer tensor block gives an exact n=25,k=1 "
                "pair with matching labeled t<=2 entropy and compact operator/channel separation. The inner-major "
                "perfect-block atlas has length-three compact hits, while block-contiguous order has none through "
                "length eight."
            ),
            "three_geometry_lesson": (
                "The perfect-code outer block makes distance and erasure semantics explicit: the pair matches "
                "low-order entropy but differs in exact distance, reconstruction algebra, erasure, and compact "
                "atlas locality. Entropy-visible data again underdetermines observer-patch geometry."
            ),
            "scope_warning": (
                "This is a literal stabilizer [[5,1,3]] outer-code concatenation, not a full multi-tensor HaPPY "
                "network. The two code realizations have different exact distances, so Phase 10 is a robust "
                "perfect-block pressure test rather than a same-distance theorem."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 10 upgrades the block model to a literal five-qubit perfect outer code and certifies exact "
                "distance asymmetry. The next step should either search for same-distance perfect-outer pairs or "
                "compose multiple perfect blocks into a small multi-tensor HaPPY tiling."
            ),
            "suggested_phase_11": (
                "Search same-distance [[5,1,3]] outer-block variants or build a two-perfect-tensor stabilizer "
                "network with exact boundary entropy, min-cut, region algebra, erasure, survivor, and distance "
                "certificates."
            ),
        },
    }


def holographic_phase11_local_clifford_maps() -> dict[str, tuple[int, int, int, int]]:
    maps = {
        f"LC{index}": matrix
        for index, matrix in enumerate(LOCAL_CLIFFORD_MATRICES)
    }
    maps.update({
        "I": (1, 0, 0, 1),
        "H": (0, 1, 1, 0),
        "S": (1, 0, 1, 1),
        "HS": (1, 1, 1, 0),
    })
    return maps


def holographic_phase11_outer_variant_specs() -> tuple[dict[str, object], ...]:
    identity = tuple("I" for _ in range(5))
    identity_perm = tuple(range(5))
    specs: list[dict[str, object]] = []

    def add(
        *,
        name: str,
        family: str,
        local_cliffords: tuple[str, ...],
        permutation: tuple[int, ...] = identity_perm,
        description: str,
    ) -> None:
        local_operation_weight = sum(1 for item in local_cliffords if item != "I")
        permutation_weight = 0 if permutation == identity_perm else 1
        local_map_complexity = sum(2 if item == "HS" else 1 for item in local_cliffords if item != "I")
        specs.append(
            {
                "name": name,
                "family": family,
                "local_cliffords": local_cliffords,
                "permutation": permutation,
                "operation_weight": local_operation_weight + permutation_weight,
                "local_map_complexity": local_map_complexity + permutation_weight,
                "description": description,
            }
        )

    for label in ("I", "H", "S", "HS"):
        add(
            name=f"global_{label}",
            family="global_local_clifford",
            local_cliffords=tuple(label for _ in range(5)),
            description=f"Apply {label} to every outer perfect-code qubit.",
        )

    for qubit in range(5):
        for label in ("H", "S", "HS"):
            local = list(identity)
            local[qubit] = label
            add(
                name=f"q{qubit}_{label}",
                family="single_site_local_clifford",
                local_cliffords=tuple(local),
                description=f"Apply {label} to outer perfect-code qubit {qubit}.",
            )

    for left, right in combinations(range(5), 2):
        local = list(identity)
        local[left] = "H"
        local[right] = "H"
        add(
            name=f"H_pair_{left}{right}",
            family="two_site_hadamard",
            local_cliffords=tuple(local),
            description=f"Apply H to outer perfect-code qubits {left} and {right}.",
        )
        local = list(identity)
        local[left] = "S"
        local[right] = "S"
        add(
            name=f"S_pair_{left}{right}",
            family="two_site_phase",
            local_cliffords=tuple(local),
            description=f"Apply S to outer perfect-code qubits {left} and {right}.",
        )

    for shift in range(1, 5):
        add(
            name=f"cyclic_perm_{shift}",
            family="outer_permutation",
            local_cliffords=identity,
            permutation=tuple((qubit + shift) % 5 for qubit in range(5)),
            description=f"Cyclically permute outer perfect-code qubits by shift {shift}.",
        )
    add(
        name="reversal",
        family="outer_permutation",
        local_cliffords=identity,
        permutation=tuple(4 - qubit for qubit in range(5)),
        description="Reverse the outer perfect-code qubit order.",
    )
    return tuple(specs)


def holographic_phase11_outer_variant_code(spec: dict[str, object]) -> StabilizerCode:
    base = holographic_phase10_five_qubit_perfect_code()
    named_maps = holographic_phase11_local_clifford_maps()
    local_names = tuple(str(item) for item in spec["local_cliffords"])  # type: ignore[index]
    if len(local_names) != base.n:
        raise ValueError("outer variant local Clifford spec must have length five")
    maps = tuple(named_maps[name] for name in local_names)
    permutation = tuple(int(item) for item in spec["permutation"])  # type: ignore[index]
    rows = tuple(
        permute_pauli(
            local_clifford_pauli(row, base.n, maps),
            base.n,
            permutation,
        )
        for row in base.generators
    )
    return StabilizerCode(base.n, rows)


def holographic_phase11_variant_record(
    *,
    spec: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
) -> dict[str, object]:
    outer = holographic_phase11_outer_variant_code(spec)
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    first_distance = bounded_distance_certificate(first, max_weight=3)
    second_distance = bounded_distance_certificate(second, max_weight=3)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    same_exact_distance_three = (
        first_distance["distance_exact_if_witness_found"] == 3
        and second_distance["distance_exact_if_witness_found"] == 3
    )
    public_spec = dict(spec)
    return {
        "spec": public_spec,
        "outer_code": holographic_phase10_outer_code_summary(outer),
        "first": first,
        "second": second,
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "public": {
            "spec": public_spec,
            "outer_code": holographic_phase10_outer_code_summary(outer),
            "code_pair": {
                "n": first.n,
                "k": first.k,
            },
            "low_order_entropy": {
                "max_subset_size": low_order_entropy["max_subset_size"],
                "subsets_checked": low_order_entropy["subsets_checked"],
                "mismatch_count": low_order_entropy["mismatch_count"],
                "matches": low_order_entropy["matches"],
            },
            "distance_audit_weight3": {
                "first": first_distance,
                "second": second_distance,
                "first_exact_distance": first_distance["distance_exact_if_witness_found"],
                "second_exact_distance": second_distance["distance_exact_if_witness_found"],
                "same_exact_distance_three": same_exact_distance_three,
            },
            "classification": (
                "same_exact_distance_three"
                if same_exact_distance_three
                else "canonical_asymmetry_or_second_distance_at_least_four_under_weight3_audit"
            ),
        },
    }


def holographic_phase11_compact_scan_record(
    *,
    variant_record: dict[str, object],
    template: dict[str, object],
    max_interval_length: int,
) -> dict[str, object]:
    first = variant_record["first"]
    second = variant_record["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 11 variant record must contain StabilizerCode objects")
    template_record = holographic_phase10_interval_template_record(
        first=first,
        second=second,
        template=template,
        max_interval_length=max_interval_length,
    )
    hits = tuple(template_record["hit_records"])  # type: ignore[index]
    selected_hit = min(
        hits,
        key=lambda hit: (int(hit["region"]["length"]), int(hit["region"]["start"])),  # type: ignore[index]
    ) if hits else None
    return {
        "variant": variant_record["public"]["spec"],  # type: ignore[index]
        "template_name": template_record["name"],
        "template_kind": template_record["template_kind"],
        "interval_search": template_record["interval_search"],
        "selected_hit": selected_hit,
    }


def bridge_holography_phase11_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 8,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 8:
        raise ValueError("max_interval_length must be at least eight for the Phase 11 certificate")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 11 source must contain StabilizerCode objects")

    specs = holographic_phase11_outer_variant_specs()
    variant_records = tuple(
        holographic_phase11_variant_record(
            spec=spec,
            inner_first=inner_first,
            inner_second=inner_second,
        )
        for spec in specs
    )
    public_variant_records = tuple(record["public"] for record in variant_records)
    same_distance_records = tuple(
        record
        for record in variant_records
        if record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
    )
    same_distance_names = {str(record["public"]["spec"]["name"]) for record in same_distance_records}  # type: ignore[index]
    asymmetric_records = tuple(
        record
        for record in variant_records
        if str(record["public"]["spec"]["name"]) not in same_distance_names  # type: ignore[index]
    )
    template_by_name = {str(template["name"]): template for template in holographic_phase10_boundary_templates()}
    inner_major_template = template_by_name["perfect_outer_inner_major"]
    compact_records = tuple(
        holographic_phase11_compact_scan_record(
            variant_record=record,
            template=inner_major_template,
            max_interval_length=max_interval_length,
        )
        for record in same_distance_records
    )
    compact_hit_records = tuple(
        record
        for record in compact_records
        if int(record["interval_search"]["hit_count"]) > 0  # type: ignore[index]
    )
    selected_compact_record = min(
        compact_hit_records,
        key=lambda record: (
            int(record["variant"]["operation_weight"]),  # type: ignore[index]
            int(record["variant"]["local_map_complexity"]),  # type: ignore[index]
            int(record["interval_search"]["shortest_hit_length"]),  # type: ignore[index]
            str(record["variant"]["name"]),  # type: ignore[index]
        ),
    )
    selected_name = str(selected_compact_record["variant"]["name"])  # type: ignore[index]
    selected_variant_record = next(
        record for record in same_distance_records if str(record["public"]["spec"]["name"]) == selected_name  # type: ignore[index]
    )
    selected_first = selected_variant_record["first"]
    selected_second = selected_variant_record["second"]
    if not isinstance(selected_first, StabilizerCode) or not isinstance(selected_second, StabilizerCode):
        raise TypeError("selected Phase 11 record must contain StabilizerCode objects")
    selected_template_records = tuple(
        holographic_phase10_interval_template_record(
            first=selected_first,
            second=selected_second,
            template=template,
            max_interval_length=max_interval_length,
        )
        for template in holographic_phase10_boundary_templates()
    )
    selected_template_by_name = {str(record["name"]): record for record in selected_template_records}
    witness_strip_order = tuple(
        int(qubit)
        for qubit in selected_template_by_name["perfect_outer_witness_strip"]["boundary_order"]  # type: ignore[index]
    )
    lifted_records = holographic_phase10_lifted_witness_records(
        first=selected_first,
        second=selected_second,
        boundary_order=witness_strip_order,
    )
    lifted_hits = tuple(
        record
        for record in lifted_records
        if record["comparisons"].get("entropy_matches")  # type: ignore[union-attr]
        and record["comparisons"].get("operator_or_channel_visible_differs")  # type: ignore[union-attr]
    )
    strict_lifted_hits = tuple(
        record
        for record in lifted_hits
        if record["interval_location"]["is_boundary_ring_interval"]  # type: ignore[index]
    )
    selected_lifted_hit = next(
        record for record in strict_lifted_hits if int(record["region"]["block_mask"]) == 7  # type: ignore[index]
    )
    family_counts = tuple(
        {
            "family": family,
            "variants": sum(1 for spec in specs if spec["family"] == family),
            "same_exact_distance_three": sum(
                1
                for record in same_distance_records
                if record["public"]["spec"]["family"] == family  # type: ignore[index]
            ),
        }
        for family in sorted({str(spec["family"]) for spec in specs})
    )
    selected_counts = {
        "candidate_intervals_scanned": sum(
            int(record["interval_search"]["intervals_scanned"]) for record in selected_template_records  # type: ignore[index]
        ),
        "entropy_gate_passes": sum(
            int(record["interval_search"]["entropy_gate_passes"]) for record in selected_template_records  # type: ignore[index]
        ),
        "entropy_gate_rejections": sum(
            int(record["interval_search"]["entropy_gate_rejections"]) for record in selected_template_records  # type: ignore[index]
        ),
        "compact_interval_hits": sum(
            int(record["interval_search"]["hit_count"]) for record in selected_template_records  # type: ignore[index]
        ),
        "block_contiguous_hits": int(
            selected_template_by_name["perfect_outer_block_contiguous"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
        "inner_major_hits": int(
            selected_template_by_name["perfect_outer_inner_major"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
        "witness_strip_hits": int(
            selected_template_by_name["perfect_outer_witness_strip"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
    }
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "outer_variant_menu_bounded_and_scored": len(specs) == 44 and len(variant_records) == 44,
        "all_outer_variants_remain_five_qubit_perfect": all(
            record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
            and record["public"]["outer_code"]["erasure_threshold"] == 2  # type: ignore[index]
            and record["public"]["outer_code"]["perfect_tensor_like_checks"][  # type: ignore[index]
                "all_size_two_or_less_erasures_correctable"
            ]
            and record["public"]["outer_code"]["perfect_tensor_like_checks"][  # type: ignore[index]
                "all_size_three_regions_reconstruct"
            ]
            for record in variant_records
        ),
        "all_variants_preserve_labeled_t2_entropy": all(
            record["public"]["low_order_entropy"]["matches"] for record in variant_records  # type: ignore[index]
        ),
        "same_distance_variants_exist": len(same_distance_records) == 20,
        "asymmetric_variants_remain_in_menu": len(asymmetric_records) == 24,
        "same_distance_variants_keep_inner_major_length_three_hits": len(compact_hit_records) == len(same_distance_records)
        and all(int(record["interval_search"]["shortest_hit_length"]) == 3 for record in compact_hit_records),  # type: ignore[index]
        "selected_variant_is_single_hadamard_q0": selected_name == "q0_H",
        "selected_variant_has_exact_same_distance_three": selected_variant_record["public"]["distance_audit_weight3"][  # type: ignore[index]
            "same_exact_distance_three"
        ],
        "selected_variant_replays_phase10_compact_atlas": selected_counts["block_contiguous_hits"] == 0
        and selected_counts["inner_major_hits"] == 12
        and selected_counts["witness_strip_hits"] == 17,
        "selected_interval_mincuts_exact": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in selected_template_records  # type: ignore[index]
        ),
        "source_aware_lifted_strict_hits_survive": len(lifted_hits) == 10 and len(strict_lifted_hits) == 3,
    }
    phase_claims["goal_3_phase_11_same_distance_perfect_outer_variant_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 11: same-distance perfect-outer variant search",
        "status": "pass" if phase_claims["goal_3_phase_11_same_distance_perfect_outer_variant_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "outer_variant_search": {
            "menu_description": (
                "Bounded perfect-outer variants generated from global/single-site/two-site local Clifford edits "
                "and simple outer-qubit permutations of the canonical [[5,1,3]] code."
            ),
            "local_clifford_maps": holographic_phase11_local_clifford_maps(),
            "family_counts": family_counts,
            "variant_records": public_variant_records,
            "same_distance_variant_names": tuple(
                str(record["public"]["spec"]["name"]) for record in same_distance_records  # type: ignore[index]
            ),
        },
        "same_distance_compact_scan": {
            "template": "perfect_outer_inner_major",
            "max_interval_length": max_interval_length,
            "variant_records": compact_records,
            "selected_compact_record": selected_compact_record,
        },
        "selected_same_distance_variant": {
            "variant_record": selected_variant_record["public"],
            "boundary_atlas_search": {
                "max_interval_length": max_interval_length,
                "templates": selected_template_records,
                "selected_interval_hit": selected_compact_record["selected_hit"],
            },
            "lifted_phase2_witness_audit": {
                "base_inner_qubits": (2, 4),
                "block_masks_checked": len(lifted_records),
                "records": lifted_records,
                "accepted_lifted_hits": lifted_hits,
                "strict_lifted_hits": strict_lifted_hits,
                "selected_lifted_hit": selected_lifted_hit,
            },
        },
        "counts": {
            "outer_variants_scored": len(variant_records),
            "outer_variants_all_perfect": sum(
                1
                for record in variant_records
                if record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
                and record["public"]["outer_code"]["erasure_threshold"] == 2  # type: ignore[index]
            ),
            "low_order_t2_matches": sum(
                1 for record in variant_records if record["public"]["low_order_entropy"]["matches"]  # type: ignore[index]
            ),
            "same_exact_distance_three_variants": len(same_distance_records),
            "asymmetric_or_second_distance_at_least_four_variants": len(asymmetric_records),
            "same_distance_compact_scans": len(compact_records),
            "same_distance_inner_major_hit_variants": len(compact_hit_records),
            "same_distance_inner_major_total_hits": sum(
                int(record["interval_search"]["hit_count"]) for record in compact_records  # type: ignore[index]
            ),
            "same_distance_inner_major_min_hit_length": min(
                int(record["interval_search"]["shortest_hit_length"]) for record in compact_records  # type: ignore[index]
            ),
            "same_distance_inner_major_intervals_scanned": sum(
                int(record["interval_search"]["intervals_scanned"]) for record in compact_records  # type: ignore[index]
            ),
            "selected_candidate_intervals_scanned": selected_counts["candidate_intervals_scanned"],
            "selected_entropy_gate_passes": selected_counts["entropy_gate_passes"],
            "selected_entropy_gate_rejections": selected_counts["entropy_gate_rejections"],
            "selected_compact_interval_hits": selected_counts["compact_interval_hits"],
            "selected_block_contiguous_hits": selected_counts["block_contiguous_hits"],
            "selected_inner_major_hits": selected_counts["inner_major_hits"],
            "selected_witness_strip_hits": selected_counts["witness_strip_hits"],
            "lifted_block_masks_checked": len(lifted_records),
            "lifted_three_block_hits": len(lifted_hits),
            "strict_lifted_hits": len(strict_lifted_hits),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded local-Clifford/permutation search over the literal five-qubit perfect outer block finds "
                "20 variants where both concatenated code realizations have exact distance three. The simplest is "
                "a single H on outer qubit 0, and it preserves the length-three compact inner-major witness."
            ),
            "three_geometry_lesson": (
                "The Phase 10 distance asymmetry is not invariant under perfect-outer logical embedding choices. "
                "Within this bounded menu, distance can be equalized while low-order entropy, exact min-cut scoring, "
                "compact observer algebra, erasure, and lifted source-aware witness semantics remain separately "
                "certified."
            ),
            "scope_warning": (
                "This is an exact bounded search over 44 declared outer variants, not an exhaustive classification "
                "of all local Clifford/permutation transforms and not a full multi-tensor HaPPY construction."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 11 removes the Phase 10 same-distance caveat inside a small perfect-outer variant menu. The "
                "next step should either exhaust a larger outer local-Clifford/permutation grammar or move to a "
                "two-perfect-tensor tiling with the same exact gates."
            ),
            "suggested_phase_12": (
                "Build a two-block perfect-tensor stabilizer tiling, or broaden the Phase 11 outer-variant menu to "
                "certify whether same-distance compact witnesses persist across a full local-Clifford orbit sample."
            ),
        },
    }


def holographic_phase12_outer_variant_specs() -> tuple[dict[str, object], ...]:
    identity = tuple("I" for _ in range(5))
    identity_perm = tuple(range(5))
    specs = list(holographic_phase11_outer_variant_specs())
    phase11_permutations = {
        tuple(int(item) for item in spec["permutation"])  # type: ignore[index]
        for spec in specs
        if spec["family"] == "outer_permutation"
    }

    for index in (1, 4):
        local = tuple(f"LC{index}" for _ in range(5))
        specs.append(
            {
                "name": f"global_LC{index}",
                "family": "added_global_full_lc",
                "local_cliffords": local,
                "permutation": identity_perm,
                "operation_weight": 5,
                "local_map_complexity": 5,
                "description": f"Apply full phase-free local Clifford LC{index} to every outer perfect-code qubit.",
            }
        )

    for qubit in range(5):
        for index in (1, 4):
            local = list(identity)
            local[qubit] = f"LC{index}"
            specs.append(
                {
                    "name": f"q{qubit}_LC{index}",
                    "family": "added_single_site_full_lc",
                    "local_cliffords": tuple(local),
                    "permutation": identity_perm,
                    "operation_weight": 1,
                    "local_map_complexity": 1,
                    "description": f"Apply full phase-free local Clifford LC{index} to outer perfect-code qubit {qubit}.",
                }
            )

    for permutation in permutations(range(5)):
        perm = tuple(int(item) for item in permutation)
        if perm == identity_perm or perm in phase11_permutations:
            continue
        specs.append(
            {
                "name": "perm_" + "".join(str(item) for item in perm),
                "family": "added_outer_permutation_full_s5",
                "local_cliffords": identity,
                "permutation": perm,
                "operation_weight": 1,
                "local_map_complexity": 1,
                "description": "Additional nontrivial outer perfect-code qubit permutation from the full S5 audit.",
            }
        )
    return tuple(specs)


def bridge_holography_phase12_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 8,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 8:
        raise ValueError("max_interval_length must be at least eight for the Phase 12 certificate")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 12 source must contain StabilizerCode objects")

    specs = holographic_phase12_outer_variant_specs()
    variant_records = tuple(
        holographic_phase11_variant_record(
            spec=spec,
            inner_first=inner_first,
            inner_second=inner_second,
        )
        for spec in specs
    )
    public_variant_records = tuple(record["public"] for record in variant_records)
    same_distance_records = tuple(
        record
        for record in variant_records
        if record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
    )
    template_by_name = {str(template["name"]): template for template in holographic_phase10_boundary_templates()}
    inner_major_template = template_by_name["perfect_outer_inner_major"]
    compact_records = tuple(
        holographic_phase11_compact_scan_record(
            variant_record=record,
            template=inner_major_template,
            max_interval_length=max_interval_length,
        )
        for record in same_distance_records
    )
    compact_hit_records = tuple(
        record for record in compact_records if int(record["interval_search"]["hit_count"]) > 0  # type: ignore[index]
    )
    selected_compact_record = min(
        compact_hit_records,
        key=lambda record: (
            int(record["variant"]["operation_weight"]),  # type: ignore[index]
            int(record["variant"]["local_map_complexity"]),  # type: ignore[index]
            int(record["interval_search"]["shortest_hit_length"]),  # type: ignore[index]
            str(record["variant"]["name"]),  # type: ignore[index]
        ),
    )
    selected_name = str(selected_compact_record["variant"]["name"])  # type: ignore[index]
    selected_variant_record = next(
        record for record in same_distance_records if str(record["public"]["spec"]["name"]) == selected_name  # type: ignore[index]
    )
    selected_first = selected_variant_record["first"]
    selected_second = selected_variant_record["second"]
    if not isinstance(selected_first, StabilizerCode) or not isinstance(selected_second, StabilizerCode):
        raise TypeError("selected Phase 12 record must contain StabilizerCode objects")
    selected_template_records = tuple(
        holographic_phase10_interval_template_record(
            first=selected_first,
            second=selected_second,
            template=template,
            max_interval_length=max_interval_length,
        )
        for template in holographic_phase10_boundary_templates()
    )
    selected_template_by_name = {str(record["name"]): record for record in selected_template_records}
    witness_strip_order = tuple(
        int(qubit)
        for qubit in selected_template_by_name["perfect_outer_witness_strip"]["boundary_order"]  # type: ignore[index]
    )
    lifted_records = holographic_phase10_lifted_witness_records(
        first=selected_first,
        second=selected_second,
        boundary_order=witness_strip_order,
    )
    lifted_hits = tuple(
        record
        for record in lifted_records
        if record["comparisons"].get("entropy_matches")  # type: ignore[union-attr]
        and record["comparisons"].get("operator_or_channel_visible_differs")  # type: ignore[union-attr]
    )
    strict_lifted_hits = tuple(
        record
        for record in lifted_hits
        if record["interval_location"]["is_boundary_ring_interval"]  # type: ignore[index]
    )
    selected_lifted_hit = next(
        record for record in strict_lifted_hits if int(record["region"]["block_mask"]) == 7  # type: ignore[index]
    )
    phase11_names = {str(spec["name"]) for spec in holographic_phase11_outer_variant_specs()}
    added_records = tuple(
        record
        for record in variant_records
        if str(record["public"]["spec"]["name"]) not in phase11_names  # type: ignore[index]
    )
    pure_permutation_families = ("outer_permutation", "added_outer_permutation_full_s5")
    pure_permutation_records = tuple(
        record
        for record in variant_records
        if record["public"]["spec"]["family"] in pure_permutation_families  # type: ignore[index]
    )
    identity_perm = tuple(range(5))
    pure_permutation_set = {
        tuple(int(item) for item in record["public"]["spec"]["permutation"])  # type: ignore[index]
        for record in pure_permutation_records
    } | {identity_perm}
    same_distance_by_family = {
        family: sum(
            1
            for record in same_distance_records
            if str(record["public"]["spec"]["family"]) == family  # type: ignore[index]
        )
        for family in sorted({str(spec["family"]) for spec in specs})
    }
    family_counts = tuple(
        {
            "family": family,
            "variants": sum(1 for spec in specs if str(spec["family"]) == family),
            "same_exact_distance_three": same_distance_by_family[family],
        }
        for family in sorted({str(spec["family"]) for spec in specs})
    )
    selected_counts = {
        "candidate_intervals_scanned": sum(
            int(record["interval_search"]["intervals_scanned"]) for record in selected_template_records  # type: ignore[index]
        ),
        "entropy_gate_passes": sum(
            int(record["interval_search"]["entropy_gate_passes"]) for record in selected_template_records  # type: ignore[index]
        ),
        "entropy_gate_rejections": sum(
            int(record["interval_search"]["entropy_gate_rejections"]) for record in selected_template_records  # type: ignore[index]
        ),
        "compact_interval_hits": sum(
            int(record["interval_search"]["hit_count"]) for record in selected_template_records  # type: ignore[index]
        ),
        "block_contiguous_hits": int(
            selected_template_by_name["perfect_outer_block_contiguous"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
        "inner_major_hits": int(
            selected_template_by_name["perfect_outer_inner_major"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
        "witness_strip_hits": int(
            selected_template_by_name["perfect_outer_witness_strip"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
    }
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "phase12_superset_menu_scored": len(specs) == 170 and len(variant_records) == 170,
        "phase11_menu_embedded": len(phase11_names) == 44
        and sum(1 for spec in specs if str(spec["name"]) in phase11_names) == 44,
        "full_s5_outer_permutations_covered": len(pure_permutation_set) == 120,
        "all_outer_variants_remain_five_qubit_perfect": all(
            record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
            and record["public"]["outer_code"]["erasure_threshold"] == 2  # type: ignore[index]
            and record["public"]["outer_code"]["perfect_tensor_like_checks"][  # type: ignore[index]
                "all_size_two_or_less_erasures_correctable"
            ]
            and record["public"]["outer_code"]["perfect_tensor_like_checks"][  # type: ignore[index]
                "all_size_three_regions_reconstruct"
            ]
            for record in variant_records
        ),
        "all_variants_preserve_labeled_t2_entropy": all(
            record["public"]["low_order_entropy"]["matches"] for record in variant_records  # type: ignore[index]
        ),
        "same_distance_variants_exactly_30": len(same_distance_records) == 30,
        "new_single_site_lc_variants_add_10_same_distance_hits": same_distance_by_family["added_single_site_full_lc"] == 10,
        "pure_outer_permutations_do_not_repair_distance_asymmetry": all(
            not record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
            for record in pure_permutation_records
        ),
        "global_full_lc_variants_do_not_repair_distance_asymmetry": same_distance_by_family["global_local_clifford"] == 0
        and same_distance_by_family["added_global_full_lc"] == 0,
        "all_same_distance_variants_keep_inner_major_length_three_hits": len(compact_hit_records) == len(same_distance_records)
        and all(int(record["interval_search"]["shortest_hit_length"]) == 3 for record in compact_hit_records),  # type: ignore[index]
        "selected_variant_remains_phase11_q0_H": selected_name == "q0_H",
        "selected_variant_replays_phase10_compact_atlas": selected_counts["block_contiguous_hits"] == 0
        and selected_counts["inner_major_hits"] == 12
        and selected_counts["witness_strip_hits"] == 17,
        "selected_interval_mincuts_exact": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in selected_template_records  # type: ignore[index]
        ),
        "source_aware_lifted_strict_hits_survive": len(lifted_hits) == 10 and len(strict_lifted_hits) == 3,
    }
    phase_claims["goal_3_phase_12_outer_embedding_robustness_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 12: perfect-outer embedding robustness audit",
        "status": "pass" if phase_claims["goal_3_phase_12_outer_embedding_robustness_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "outer_embedding_search": {
            "menu_description": (
                "Phase 11's 44 perfect-outer variants, plus the missing two global full-LC maps, the missing ten "
                "single-site full-LC maps, and the remaining 114 nontrivial outer-qubit permutations needed to "
                "cover S5 when combined with the identity."
            ),
            "local_clifford_maps": holographic_phase11_local_clifford_maps(),
            "family_counts": family_counts,
            "variant_records": public_variant_records,
            "same_distance_variant_names": tuple(
                str(record["public"]["spec"]["name"]) for record in same_distance_records  # type: ignore[index]
            ),
            "pure_permutation_records": tuple(record["public"] for record in pure_permutation_records),
        },
        "same_distance_compact_scan": {
            "template": "perfect_outer_inner_major",
            "max_interval_length": max_interval_length,
            "variant_records": compact_records,
            "selected_compact_record": selected_compact_record,
        },
        "selected_same_distance_variant": {
            "variant_record": selected_variant_record["public"],
            "boundary_atlas_search": {
                "max_interval_length": max_interval_length,
                "templates": selected_template_records,
                "selected_interval_hit": selected_compact_record["selected_hit"],
            },
            "lifted_phase2_witness_audit": {
                "base_inner_qubits": (2, 4),
                "block_masks_checked": len(lifted_records),
                "records": lifted_records,
                "accepted_lifted_hits": lifted_hits,
                "strict_lifted_hits": strict_lifted_hits,
                "selected_lifted_hit": selected_lifted_hit,
            },
        },
        "counts": {
            "outer_embedding_variants_scored": len(variant_records),
            "phase11_seed_variants": len(phase11_names),
            "added_variants": len(added_records),
            "outer_variants_all_perfect": sum(
                1
                for record in variant_records
                if record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
                and record["public"]["outer_code"]["erasure_threshold"] == 2  # type: ignore[index]
            ),
            "low_order_t2_matches": sum(
                1 for record in variant_records if record["public"]["low_order_entropy"]["matches"]  # type: ignore[index]
            ),
            "same_exact_distance_three_variants": len(same_distance_records),
            "same_distance_added_single_site_lc_variants": same_distance_by_family["added_single_site_full_lc"],
            "same_distance_phase11_seed_variants": sum(
                1
                for record in same_distance_records
                if str(record["public"]["spec"]["name"]) in phase11_names  # type: ignore[index]
            ),
            "pure_permutation_specs": len(pure_permutation_records),
            "full_s5_permutations_covered_with_identity": len(pure_permutation_set),
            "pure_permutation_same_distance_variants": sum(
                1
                for record in pure_permutation_records
                if record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
            ),
            "same_distance_compact_scans": len(compact_records),
            "same_distance_inner_major_hit_variants": len(compact_hit_records),
            "same_distance_inner_major_total_hits": sum(
                int(record["interval_search"]["hit_count"]) for record in compact_records  # type: ignore[index]
            ),
            "same_distance_inner_major_min_hit_length": min(
                int(record["interval_search"]["shortest_hit_length"]) for record in compact_records  # type: ignore[index]
            ),
            "same_distance_inner_major_intervals_scanned": sum(
                int(record["interval_search"]["intervals_scanned"]) for record in compact_records  # type: ignore[index]
            ),
            "selected_candidate_intervals_scanned": selected_counts["candidate_intervals_scanned"],
            "selected_entropy_gate_passes": selected_counts["entropy_gate_passes"],
            "selected_entropy_gate_rejections": selected_counts["entropy_gate_rejections"],
            "selected_compact_interval_hits": selected_counts["compact_interval_hits"],
            "selected_block_contiguous_hits": selected_counts["block_contiguous_hits"],
            "selected_inner_major_hits": selected_counts["inner_major_hits"],
            "selected_witness_strip_hits": selected_counts["witness_strip_hits"],
            "lifted_block_masks_checked": len(lifted_records),
            "lifted_three_block_hits": len(lifted_hits),
            "strict_lifted_hits": len(strict_lifted_hits),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The Phase 11 same-distance witness is not isolated: in a 170-spec perfect-outer embedding superset, "
                "30 variants have exact distance three for both concatenated codes, and all 30 preserve length-three "
                "inner-major compact witnesses."
            ),
            "three_geometry_lesson": (
                "Same-distance compact observer splits are robust under a bounded class of one-site outer logical "
                "axis changes, but not under pure outer-qubit relabeling or global local-Clifford layers. Thus the "
                "repair depends on logical embedding semantics, not just block permutation semantics."
            ),
            "scope_warning": (
                "This exactly covers the declared 170 operation specs and all S5 pure permutations, but it is not a "
                "full local-Clifford orbit over five qubits and not yet a multi-perfect-tensor HaPPY tiling."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 12 classifies a broader perfect-outer embedding menu and shows pure permutation no-go behavior. "
                "The next step should move from one perfect outer block to a small two-perfect-tensor stabilizer tiling."
            ),
            "suggested_phase_13": (
                "Compose two five-qubit perfect tensors or a small HaPPY-like tiling and replay the exact entropy, "
                "min-cut, region algebra, erasure, survivor, and distance gates."
            ),
        },
    }


def holographic_phase13_two_perfect_outer_code(
    *,
    bridge_axis: str,
    local_cliffords: tuple[str, ...] | None = None,
) -> StabilizerCode:
    if bridge_axis not in ("Z", "X", "Y"):
        raise ValueError("bridge_axis must be one of Z, X, or Y")
    base = holographic_phase10_five_qubit_perfect_code()
    rows: list[int] = []
    for block in range(2):
        for generator in base.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=5, block_count=2))
    logical_z, logical_x = base.logical_basis
    bridge_logical = {
        "Z": logical_z,
        "X": logical_x,
        "Y": logical_z ^ logical_x,
    }[bridge_axis]
    rows.append(
        block_shift_pauli(bridge_logical, block=0, block_size=5, block_count=2)
        ^ block_shift_pauli(bridge_logical, block=1, block_size=5, block_count=2)
    )
    code = StabilizerCode(10, rows)
    if local_cliffords is None:
        return code
    if len(local_cliffords) != code.n:
        raise ValueError("local_cliffords must have length ten for the two-perfect outer code")
    named_maps = holographic_phase11_local_clifford_maps()
    maps = tuple(named_maps[name] for name in local_cliffords)
    return StabilizerCode(code.n, (local_clifford_pauli(row, code.n, maps) for row in code.generators))


def holographic_phase13_outer_code_summary(
    outer: StabilizerCode,
    *,
    bridge_axis: str,
    local_cliffords: tuple[str, ...],
) -> dict[str, object]:
    return {
        "name": "two_five_qubit_perfect_blocks_with_logical_bridge",
        "construction": (
            "Two copies of the canonical [[5,1,3]] outer block plus one logical bridge stabilizer, leaving k=1."
        ),
        "bridge_axis": bridge_axis,
        "local_cliffords": local_cliffords,
        "parameters": {"n": outer.n, "k": outer.k, "distance": outer.distance()},
        "generators": outer.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
        "erasure_threshold": outer.erasure_threshold(),
        "cell_code": holographic_phase10_outer_code_summary(holographic_phase10_five_qubit_perfect_code()),
        "two_cell_checks": {
            "two_literal_perfect_cells": True,
            "single_logical_bridge_stabilizer": True,
            "outer_k1": outer.k == 1,
            "outer_distance_three": outer.distance() == 3,
            "outer_erasure_threshold_two": outer.erasure_threshold() == 2,
        },
    }


def holographic_phase13_variant_specs() -> tuple[dict[str, object], ...]:
    identity = tuple("I" for _ in range(10))
    specs: list[dict[str, object]] = []

    def add(
        *,
        name: str,
        family: str,
        bridge_axis: str,
        local_cliffords: tuple[str, ...],
        operation_weight: int,
        local_map_complexity: int,
        description: str,
    ) -> None:
        specs.append(
            {
                "name": name,
                "family": family,
                "bridge_axis": bridge_axis,
                "local_cliffords": local_cliffords,
                "operation_weight": operation_weight,
                "local_map_complexity": local_map_complexity,
                "description": description,
            }
        )

    for axis in ("Z", "X", "Y"):
        add(
            name=f"{axis}_identity",
            family="bridge_identity",
            bridge_axis=axis,
            local_cliffords=identity,
            operation_weight=0,
            local_map_complexity=0,
            description=f"Two perfect outer blocks bridged by encoded {axis}{axis}, with no outer-leg edit.",
        )

    for qubit in range(10):
        for label in ("HS", "LC4"):
            local = list(identity)
            local[qubit] = label
            add(
                name=f"X_q{qubit}_{label}",
                family="x_bridge_single_site_axis_swap",
                bridge_axis="X",
                local_cliffords=tuple(local),
                operation_weight=1,
                local_map_complexity=2,
                description=f"X-bridge tiling with {label} on outer tiling leg {qubit}.",
            )
        for label, complexity in (("H", 1), ("LC1", 2)):
            local = list(identity)
            local[qubit] = label
            add(
                name=f"Y_q{qubit}_{label}",
                family="y_bridge_single_site_axis_swap",
                bridge_axis="Y",
                local_cliffords=tuple(local),
                operation_weight=1,
                local_map_complexity=complexity,
                description=f"Y-bridge tiling with {label} on outer tiling leg {qubit}.",
            )

    for leg in range(5):
        local = list(identity)
        local[leg] = "H"
        local[5 + leg] = "H"
        add(
            name=f"Y_paired_leg{leg}_H",
            family="y_bridge_paired_leg_hadamard",
            bridge_axis="Y",
            local_cliffords=tuple(local),
            operation_weight=2,
            local_map_complexity=2,
            description=f"Y-bridge tiling with H on matching cell legs {leg} and {5 + leg}.",
        )
    return tuple(specs)


def holographic_phase13_variant_record(
    *,
    spec: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
) -> dict[str, object]:
    bridge_axis = str(spec["bridge_axis"])
    local_cliffords = tuple(str(item) for item in spec["local_cliffords"])  # type: ignore[index]
    outer = holographic_phase13_two_perfect_outer_code(
        bridge_axis=bridge_axis,
        local_cliffords=local_cliffords,
    )
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    first_distance = bounded_distance_certificate(first, max_weight=3)
    second_distance = bounded_distance_certificate(second, max_weight=3)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    same_exact_distance_three = (
        first_distance["distance_exact_if_witness_found"] == 3
        and second_distance["distance_exact_if_witness_found"] == 3
    )
    public_spec = dict(spec)
    return {
        "spec": public_spec,
        "outer": outer,
        "first": first,
        "second": second,
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "public": {
            "spec": public_spec,
            "outer_code": {
                "parameters": {"n": outer.n, "k": outer.k, "distance": outer.distance()},
                "erasure_threshold": outer.erasure_threshold(),
            },
            "code_pair": {"n": first.n, "k": first.k},
            "low_order_entropy": {
                "max_subset_size": low_order_entropy["max_subset_size"],
                "subsets_checked": low_order_entropy["subsets_checked"],
                "mismatch_count": low_order_entropy["mismatch_count"],
                "matches": low_order_entropy["matches"],
            },
            "distance_audit_weight3": {
                "first": first_distance,
                "second": second_distance,
                "first_exact_distance": first_distance["distance_exact_if_witness_found"],
                "second_exact_distance": second_distance["distance_exact_if_witness_found"],
                "same_exact_distance_three": same_exact_distance_three,
            },
            "classification": (
                "same_exact_distance_three"
                if same_exact_distance_three
                else "tiling_distance_asymmetry_under_weight3_audit"
            ),
        },
    }


def holographic_phase13_boundary_templates() -> tuple[dict[str, object], ...]:
    inner_order = (0, 1, 2, 4, 3)
    block_size = 5
    block_count = 10
    block_contiguous = tuple(block * block_size + qubit for block in range(block_count) for qubit in inner_order)
    inner_major = tuple(block * block_size + qubit for qubit in inner_order for block in range(block_count))
    cell_major = tuple(
        block * block_size + qubit
        for cell in range(2)
        for qubit in inner_order
        for block in range(cell * 5, (cell + 1) * 5)
    )
    witness_prefix = tuple(block * block_size + qubit for block in range(block_count) for qubit in (2, 4))
    witness_set = set(witness_prefix)
    witness_strip = witness_prefix + tuple(qubit for qubit in block_contiguous if qubit not in witness_set)
    return (
        {
            "name": "two_perfect_block_contiguous",
            "template_kind": "two_tensor_block_local",
            "description": "Repeat the Phase 2 inner ring inside each of the ten outer tiling legs.",
            "boundary_order": block_contiguous,
        },
        {
            "name": "two_perfect_inner_major",
            "template_kind": "two_tensor_inner_major",
            "description": "Group equal inner positions across all ten outer tiling legs.",
            "boundary_order": inner_major,
        },
        {
            "name": "two_perfect_cell_major",
            "template_kind": "two_tensor_cell_major",
            "description": "Group equal inner positions inside the left perfect cell, then inside the right cell.",
            "boundary_order": cell_major,
        },
        {
            "name": "two_perfect_witness_strip",
            "template_kind": "source_aware_control",
            "description": "Place all lifted Phase 2 witness qubits first across the ten tiling legs.",
            "boundary_order": witness_strip,
        },
    )


def holographic_phase13_two_perfect_network_spec(boundary_order: tuple[int, ...]) -> dict[str, object]:
    edges = list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = ("perfect_tensor_left", "perfect_tensor_right")
    for block in range(10):
        node = internal_nodes[0] if block < 5 else internal_nodes[1]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="two_perfect_tensor_boundary_leg",
                )
            )
    edges.append(
        holographic_phase4_edge(
            internal_nodes[0],
            internal_nodes[1],
            edge_type="two_perfect_tensor_bridge",
            capacity=2,
        )
    )
    return {
        "name": "two_five_qubit_perfect_tensor_bridge_skeleton",
        "network_kind": "two_perfect_tensor_bridge",
        "description": (
            "Two internal perfect-tensor cells each attach to five encoded outer legs; a capacity-2 edge joins the "
            "cells and every boundary min-cut is enumerated over the two internal assignments."
        ),
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase13_interval_template_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    template: dict[str, object],
    max_interval_length: int,
    include_hit_records: bool = False,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase13_two_perfect_network_spec(boundary_order)
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    entropy_gate_passes = 0
    entropy_gate_rejections = 0
    all_min_cuts_exact = True
    length_summaries = []
    hit_count = 0
    selected_hit = None
    hit_records = []
    circuit = {
        "name": template["name"],
        "generator_kind": "two_perfect_tensor_tiling",
    }
    for length in range(1, max_interval_length + 1):
        length_intervals = tuple(region for region in intervals if int(region["length"]) == length)
        length_entropy_passes = 0
        length_hits = 0
        for region in length_intervals:
            region_mask = int(region["mask"])
            min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
            all_min_cuts_exact = all_min_cuts_exact and (
                min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"])  # type: ignore[arg-type]
            )
            first_entropy = first.entropy(region_mask)
            second_entropy = second.entropy(region_mask)
            if first_entropy != second_entropy:
                entropy_gate_rejections += 1
                continue
            entropy_gate_passes += 1
            length_entropy_passes += 1
            hit = holographic_phase7_hit_record(
                circuit=circuit,
                first=first,
                second=second,
                network_spec=network_spec,
                region=region,
            )
            if bool(hit["comparisons"]["operator_or_channel_visible_differs"]):  # type: ignore[index]
                hit_count += 1
                length_hits += 1
                if selected_hit is None or (
                    int(hit["region"]["length"]),  # type: ignore[index]
                    int(hit["region"]["start"]),  # type: ignore[index]
                ) < (
                    int(selected_hit["region"]["length"]),  # type: ignore[index]
                    int(selected_hit["region"]["start"]),  # type: ignore[index]
                ):
                    selected_hit = hit
                if include_hit_records:
                    hit_records.append(hit)
        length_summaries.append(
            {
                "length": length,
                "intervals_scanned": len(length_intervals),
                "entropy_gate_passes": length_entropy_passes,
                "entropy_gate_rejections": len(length_intervals) - length_entropy_passes,
                "operator_or_channel_hits": length_hits,
            }
        )
    return {
        "name": template["name"],
        "template_kind": template["template_kind"],
        "description": template["description"],
        "boundary_order": boundary_order,
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
            "internal_assignments_per_min_cut": 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
        "interval_search": {
            "max_interval_length": max_interval_length,
            "intervals_scanned": len(intervals),
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "all_candidate_min_cuts_exact": all_min_cuts_exact,
            "length_summaries": tuple(length_summaries),
            "hit_count": hit_count,
            "shortest_hit_length": None if selected_hit is None else int(selected_hit["region"]["length"]),  # type: ignore[index]
        },
        "selected_hit": selected_hit,
        "hit_records": tuple(hit_records),
    }


def bridge_holography_phase13_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 8,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 8:
        raise ValueError("max_interval_length must be at least eight for the Phase 13 certificate")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 13 source must contain StabilizerCode objects")

    specs = holographic_phase13_variant_specs()
    variant_records = tuple(
        holographic_phase13_variant_record(
            spec=spec,
            inner_first=inner_first,
            inner_second=inner_second,
        )
        for spec in specs
    )
    same_distance_records = tuple(
        record
        for record in variant_records
        if record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
    )
    inner_major_template = {
        str(template["name"]): template
        for template in holographic_phase13_boundary_templates()
    }["two_perfect_inner_major"]
    representative_names = ("X_q0_HS", "Y_q0_H", "Y_paired_leg0_H")
    representative_same_distance_records = tuple(
        record
        for record in same_distance_records
        if str(record["public"]["spec"]["name"]) in representative_names  # type: ignore[index]
    )
    compact_records = tuple(
        {
            "variant": record["public"]["spec"],  # type: ignore[index]
            "interval_record": holographic_phase13_interval_template_record(
                first=record["first"],  # type: ignore[arg-type]
                second=record["second"],  # type: ignore[arg-type]
                template=inner_major_template,
                max_interval_length=max_interval_length,
            ),
        }
        for record in representative_same_distance_records
    )
    compact_hit_records = tuple(
        record
        for record in compact_records
        if int(record["interval_record"]["interval_search"]["hit_count"]) > 0  # type: ignore[index]
    )
    selected_compact_record = min(
        compact_hit_records,
        key=lambda record: (
            int(record["variant"]["operation_weight"]),  # type: ignore[index]
            int(record["variant"]["local_map_complexity"]),  # type: ignore[index]
            int(record["interval_record"]["interval_search"]["shortest_hit_length"]),  # type: ignore[index]
            str(record["variant"]["name"]),  # type: ignore[index]
        ),
    )
    selected_name = str(selected_compact_record["variant"]["name"])  # type: ignore[index]
    selected_variant_record = next(
        record for record in same_distance_records if str(record["public"]["spec"]["name"]) == selected_name  # type: ignore[index]
    )
    selected_first = selected_variant_record["first"]
    selected_second = selected_variant_record["second"]
    selected_outer = selected_variant_record["outer"]
    if (
        not isinstance(selected_first, StabilizerCode)
        or not isinstance(selected_second, StabilizerCode)
        or not isinstance(selected_outer, StabilizerCode)
    ):
        raise TypeError("selected Phase 13 record must contain StabilizerCode objects")
    selected_template_records = tuple(
        holographic_phase13_interval_template_record(
            first=selected_first,
            second=selected_second,
            template=template,
            max_interval_length=max_interval_length,
            include_hit_records=False,
        )
        for template in holographic_phase13_boundary_templates()
    )
    selected_template_by_name = {str(record["name"]): record for record in selected_template_records}
    same_distance_by_family = {
        family: sum(
            1
            for record in same_distance_records
            if str(record["public"]["spec"]["family"]) == family  # type: ignore[index]
        )
        for family in sorted({str(spec["family"]) for spec in specs})
    }
    family_counts = tuple(
        {
            "family": family,
            "variants": sum(1 for spec in specs if str(spec["family"]) == family),
            "same_exact_distance_three": same_distance_by_family[family],
        }
        for family in sorted({str(spec["family"]) for spec in specs})
    )
    selected_counts = {
        "candidate_intervals_scanned": sum(
            int(record["interval_search"]["intervals_scanned"]) for record in selected_template_records  # type: ignore[index]
        ),
        "entropy_gate_passes": sum(
            int(record["interval_search"]["entropy_gate_passes"]) for record in selected_template_records  # type: ignore[index]
        ),
        "entropy_gate_rejections": sum(
            int(record["interval_search"]["entropy_gate_rejections"]) for record in selected_template_records  # type: ignore[index]
        ),
        "compact_interval_hits": sum(
            int(record["interval_search"]["hit_count"]) for record in selected_template_records  # type: ignore[index]
        ),
        "block_contiguous_hits": int(
            selected_template_by_name["two_perfect_block_contiguous"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
        "inner_major_hits": int(
            selected_template_by_name["two_perfect_inner_major"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
        "cell_major_hits": int(
            selected_template_by_name["two_perfect_cell_major"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
        "witness_strip_hits": int(
            selected_template_by_name["two_perfect_witness_strip"]["interval_search"]["hit_count"]  # type: ignore[index]
        ),
    }
    identity_records = tuple(
        record for record in variant_records if record["public"]["spec"]["family"] == "bridge_identity"  # type: ignore[index]
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "two_perfect_tiling_menu_scored": len(specs) == 48 and len(variant_records) == 48,
        "two_perfect_outer_codes_are_k1_distance3": all(
            record["public"]["outer_code"]["parameters"]["k"] == 1  # type: ignore[index]
            and record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
            and record["public"]["outer_code"]["erasure_threshold"] == 2  # type: ignore[index]
            for record in variant_records
        ),
        "all_variants_preserve_labeled_t2_entropy": all(
            record["public"]["low_order_entropy"]["matches"] for record in variant_records  # type: ignore[index]
        ),
        "unrepaired_bridge_identities_are_distance_asymmetric": len(identity_records) == 3
        and all(
            not record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
            for record in identity_records
        ),
        "same_distance_tiling_repairs_exist": len(same_distance_records) == 45,
        "x_and_y_bridge_repairs_classified": same_distance_by_family["x_bridge_single_site_axis_swap"] == 20
        and same_distance_by_family["y_bridge_single_site_axis_swap"] == 20
        and same_distance_by_family["y_bridge_paired_leg_hadamard"] == 5,
        "representative_repair_families_keep_inner_major_length_three_hits": len(compact_hit_records) == 3
        and all(
            int(record["interval_record"]["interval_search"]["shortest_hit_length"]) == 3  # type: ignore[index]
            for record in compact_hit_records
        ),
        "selected_variant_is_y_q0_h": selected_name == "Y_q0_H",
        "selected_variant_replays_two_tensor_atlas": selected_counts["block_contiguous_hits"] == 0
        and selected_counts["inner_major_hits"] == 20
        and selected_counts["cell_major_hits"] == 22
        and selected_counts["witness_strip_hits"] == 35,
        "selected_interval_mincuts_exact": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in selected_template_records  # type: ignore[index]
        ),
    }
    phase_claims["goal_3_phase_13_two_perfect_tensor_tiling_certificate"] = all(phase_claims.values())
    selected_hit = selected_template_by_name["two_perfect_inner_major"]["selected_hit"]
    return {
        "phase": "Goal 3 Phase 13: two-perfect-tensor tiling audit",
        "status": "pass" if phase_claims["goal_3_phase_13_two_perfect_tensor_tiling_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "tiling_outer_code": {
            "selected": holographic_phase13_outer_code_summary(
                selected_outer,
                bridge_axis=str(selected_variant_record["public"]["spec"]["bridge_axis"]),  # type: ignore[index]
                local_cliffords=tuple(selected_variant_record["public"]["spec"]["local_cliffords"]),  # type: ignore[index]
            ),
            "menu_description": (
                "Two [[5,1,3]] perfect outer blocks joined by one encoded bridge stabilizer, with targeted local "
                "outer-leg edits that repair the concatenated distance asymmetry."
            ),
        },
        "tiling_variant_search": {
            "family_counts": family_counts,
            "variant_records": tuple(record["public"] for record in variant_records),
            "same_distance_variant_names": tuple(
                str(record["public"]["spec"]["name"]) for record in same_distance_records  # type: ignore[index]
            ),
        },
        "same_distance_compact_scan": {
            "template": "two_perfect_inner_major",
            "max_interval_length": max_interval_length,
            "scan_scope": "one representative compact scan from each same-distance repair family",
            "representative_variant_names": representative_names,
            "variant_records": tuple(
                {
                    "variant": record["variant"],
                    "interval_search": record["interval_record"]["interval_search"],  # type: ignore[index]
                    "selected_hit": record["interval_record"]["selected_hit"],  # type: ignore[index]
                }
                for record in compact_records
            ),
            "selected_compact_record": {
                "variant": selected_compact_record["variant"],
                "interval_search": selected_compact_record["interval_record"]["interval_search"],  # type: ignore[index]
                "selected_hit": selected_compact_record["interval_record"]["selected_hit"],  # type: ignore[index]
            },
        },
        "selected_same_distance_tiling": {
            "variant_record": selected_variant_record["public"],
            "boundary_atlas_search": {
                "max_interval_length": max_interval_length,
                "templates": selected_template_records,
                "selected_interval_hit": selected_hit,
            },
        },
        "counts": {
            "tiling_variants_scored": len(variant_records),
            "bridge_identity_variants": len(identity_records),
            "outer_variants_k1_distance3": sum(
                1
                for record in variant_records
                if record["public"]["outer_code"]["parameters"]["k"] == 1  # type: ignore[index]
                and record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
            ),
            "low_order_t2_matches": sum(
                1 for record in variant_records if record["public"]["low_order_entropy"]["matches"]  # type: ignore[index]
            ),
            "same_exact_distance_three_variants": len(same_distance_records),
            "distance_asymmetric_identity_variants": sum(
                1
                for record in identity_records
                if not record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
            ),
            "same_distance_compact_scans": len(compact_records),
            "same_distance_inner_major_hit_variants": len(compact_hit_records),
            "same_distance_inner_major_total_hits": sum(
                int(record["interval_record"]["interval_search"]["hit_count"]) for record in compact_records  # type: ignore[index]
            ),
            "same_distance_inner_major_min_hit_length": min(
                int(record["interval_record"]["interval_search"]["shortest_hit_length"]) for record in compact_records  # type: ignore[index]
            ),
            "same_distance_inner_major_intervals_scanned": sum(
                int(record["interval_record"]["interval_search"]["intervals_scanned"]) for record in compact_records  # type: ignore[index]
            ),
            "selected_candidate_intervals_scanned": selected_counts["candidate_intervals_scanned"],
            "selected_entropy_gate_passes": selected_counts["entropy_gate_passes"],
            "selected_entropy_gate_rejections": selected_counts["entropy_gate_rejections"],
            "selected_compact_interval_hits": selected_counts["compact_interval_hits"],
            "selected_block_contiguous_hits": selected_counts["block_contiguous_hits"],
            "selected_inner_major_hits": selected_counts["inner_major_hits"],
            "selected_cell_major_hits": selected_counts["cell_major_hits"],
            "selected_witness_strip_hits": selected_counts["witness_strip_hits"],
            "max_candidate_min_cut_internal_assignments": max(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in selected_template_records  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A real two-perfect-block outer stabilizer tiling gives an n=50,k=1 concatenated pair with matching "
                "labeled t<=2 entropy and same exact distance three after a one-leg Y-bridge Hadamard repair. The "
                "selected compact interval keeps matching entropy/min-cut data while operator and erasure semantics split."
            ),
            "three_geometry_lesson": (
                "The compact split survives moving from one perfect outer block to two bridged perfect cells. The "
                "unrepaired bridge identities are distance-asymmetric, while targeted local logical-axis edits repair "
                "distance without removing the reconstruction/channel split."
            ),
            "scope_warning": (
                "This is an exact finite two-cell stabilizer tiling and min-cut skeleton, not a full hyperbolic HaPPY "
                "network or an exhaustive local-Clifford search over all two-cell embeddings. Compact scans are run "
                "for representative same-distance repair families plus the selected full atlas replay."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 13 establishes the two-perfect-cell analogue. The next phase should add a small tiling grammar "
                "with alternative bridge capacities/connectivities or a three-cell chain to test whether compact "
                "observer splits persist under larger holographic skeletons."
            ),
            "suggested_phase_14": (
                "Search a three-perfect-cell chain/ring or vary the two-cell bridge capacity and boundary order, while "
                "keeping exact entropy, min-cut, algebra, erasure, survivor, and distance certificates."
            ),
        },
    }


def holographic_phase14_three_perfect_outer_code(
    *,
    bridge_axes: tuple[str, str],
    local_cliffords: tuple[str, ...] | None = None,
) -> StabilizerCode:
    if len(bridge_axes) != 2 or any(axis not in ("Z", "X", "Y") for axis in bridge_axes):
        raise ValueError("bridge_axes must contain two entries from Z, X, and Y")
    base = holographic_phase10_five_qubit_perfect_code()
    rows: list[int] = []
    for block in range(3):
        for generator in base.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=5, block_count=3))
    logical_z, logical_x = base.logical_basis
    logical_by_axis = {
        "Z": logical_z,
        "X": logical_x,
        "Y": logical_z ^ logical_x,
    }
    for left_block, axis in enumerate(bridge_axes):
        bridge_logical = logical_by_axis[axis]
        rows.append(
            block_shift_pauli(bridge_logical, block=left_block, block_size=5, block_count=3)
            ^ block_shift_pauli(bridge_logical, block=left_block + 1, block_size=5, block_count=3)
        )
    code = StabilizerCode(15, rows)
    if local_cliffords is None:
        return code
    if len(local_cliffords) != code.n:
        raise ValueError("local_cliffords must have length fifteen for the three-perfect outer code")
    named_maps = holographic_phase11_local_clifford_maps()
    maps = tuple(named_maps[name] for name in local_cliffords)
    return StabilizerCode(code.n, (local_clifford_pauli(row, code.n, maps) for row in code.generators))


def holographic_phase14_outer_code_summary(
    outer: StabilizerCode,
    *,
    bridge_axes: tuple[str, str],
    local_cliffords: tuple[str, ...],
) -> dict[str, object]:
    return {
        "name": "three_five_qubit_perfect_blocks_with_logical_bridge_chain",
        "construction": (
            "Three copies of the canonical [[5,1,3]] outer block plus two nearest-neighbor logical bridge "
            "stabilizers, leaving k=1."
        ),
        "bridge_axes": bridge_axes,
        "local_cliffords": local_cliffords,
        "parameters": {"n": outer.n, "k": outer.k, "distance": outer.distance()},
        "generators": outer.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
        "erasure_threshold": outer.erasure_threshold(),
        "cell_code": holographic_phase10_outer_code_summary(holographic_phase10_five_qubit_perfect_code()),
        "three_cell_checks": {
            "three_literal_perfect_cells": True,
            "two_logical_bridge_stabilizers": True,
            "outer_k1": outer.k == 1,
            "outer_distance_three": outer.distance() == 3,
            "outer_erasure_threshold_two": outer.erasure_threshold() == 2,
        },
    }


def holographic_phase14_variant_specs() -> tuple[dict[str, object], ...]:
    identity = tuple("I" for _ in range(15))
    specs: list[dict[str, object]] = []

    def add(
        *,
        name: str,
        family: str,
        bridge_axes: tuple[str, str],
        local_cliffords: tuple[str, ...],
        operation_weight: int,
        local_map_complexity: int,
        description: str,
    ) -> None:
        specs.append(
            {
                "name": name,
                "family": family,
                "bridge_axes": bridge_axes,
                "local_cliffords": local_cliffords,
                "operation_weight": operation_weight,
                "local_map_complexity": local_map_complexity,
                "description": description,
            }
        )

    for axis in ("Z", "X", "Y"):
        add(
            name=f"{axis}{axis}_identity",
            family="bridge_identity",
            bridge_axes=(axis, axis),
            local_cliffords=identity,
            operation_weight=0,
            local_map_complexity=0,
            description=(
                f"Three perfect outer blocks bridged by encoded {axis}{axis} on both nearest-neighbor links, "
                "with no outer-leg edit."
            ),
        )

    for qubit in (0, 5, 10):
        local = list(identity)
        local[qubit] = "H"
        add(
            name=f"YY_q{qubit}_H",
            family="yy_bridge_single_cell_axis_swap",
            bridge_axes=("Y", "Y"),
            local_cliffords=tuple(local),
            operation_weight=1,
            local_map_complexity=1,
            description=f"Three-cell YY bridge chain with H on representative outer leg {qubit}.",
        )
        local = list(identity)
        local[qubit] = "HS"
        add(
            name=f"XX_q{qubit}_HS",
            family="xx_bridge_single_cell_axis_swap",
            bridge_axes=("X", "X"),
            local_cliffords=tuple(local),
            operation_weight=1,
            local_map_complexity=2,
            description=f"Three-cell XX bridge chain with HS on representative outer leg {qubit}.",
        )
    return tuple(specs)


def holographic_phase14_pauli_string(n: int, pattern: tuple[tuple[int, str], ...]) -> str:
    chars = ["I"] * n
    for qubit, char in pattern:
        chars[qubit] = char
    return "".join(chars)


def holographic_phase14_repaired_witness_patterns(
    variant_name: str,
) -> tuple[tuple[tuple[int, str], ...], tuple[tuple[int, str], ...]] | None:
    patterns: dict[str, tuple[tuple[tuple[int, str], ...], tuple[tuple[int, str], ...]]] = {
        "YY_q0_H": (
            ((4, "X"), (9, "X"), (14, "Z")),
            ((4, "Z"), (9, "Z"), (24, "Z")),
        ),
        "YY_q5_H": (
            ((4, "Z"), (9, "X"), (14, "Z")),
            ((29, "Z"), (34, "Z"), (49, "Z")),
        ),
        "YY_q10_H": (
            ((4, "Z"), (9, "X"), (14, "Z")),
            ((54, "Z"), (59, "Z"), (74, "Z")),
        ),
        "XX_q0_HS": (
            ((4, "Y"), (9, "Y"), (14, "X")),
            ((4, "Z"), (14, "Z"), (19, "Z")),
        ),
        "XX_q5_HS": (
            ((4, "X"), (9, "Y"), (14, "X")),
            ((29, "Z"), (39, "Z"), (44, "Z")),
        ),
        "XX_q10_HS": (
            ((4, "X"), (9, "Y"), (14, "X")),
            ((54, "Z"), (64, "Z"), (69, "Z")),
        ),
    }
    return patterns.get(variant_name)


def holographic_phase14_verified_logical_witness(
    code: StabilizerCode,
    pattern: tuple[tuple[int, str], ...],
) -> dict[str, object]:
    pauli = holographic_phase14_pauli_string(code.n, pattern)
    row = pauli_from_string(pauli)
    commutes = all(symplectic_product(row, generator, code.n) == 0 for generator in code.generators)
    non_stabilizer = not in_span(row, code.generators, code.width)
    qubits = tuple(qubit for qubit, _ in pattern)
    return {
        "pauli": pauli,
        "weight": len(qubits),
        "qubits": qubits,
        "commutes_with_stabilizer": commutes,
        "non_stabilizer_logical": non_stabilizer,
        "verified_logical": commutes and non_stabilizer,
    }


def holographic_phase14_exact_distance_three_from_witness(
    code: StabilizerCode,
    pattern: tuple[tuple[int, str], ...],
) -> dict[str, object]:
    lower = bounded_distance_certificate(code, max_weight=2)
    witness = holographic_phase14_verified_logical_witness(code, pattern)
    exact_three = (
        lower["logical_witness"] is None
        and int(witness["weight"]) == 3
        and bool(witness["verified_logical"])
    )
    return {
        **lower,
        "logical_witness": witness if exact_three else lower["logical_witness"],
        "distance_exact_if_witness_found": 3 if exact_three else lower["distance_exact_if_witness_found"],
        "distance_lower_bound": 3 if lower["logical_witness"] is None else lower["distance_lower_bound"],
        "distance_certification_method": "weight2_lower_bound_plus_explicit_weight3_logical",
        "explicit_weight3_logical_witness": witness,
        "exact_distance_three_certified": exact_three,
    }


def holographic_phase14_distance_audit(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    variant_name: str,
) -> dict[str, object]:
    patterns = holographic_phase14_repaired_witness_patterns(variant_name)
    if patterns is None:
        first_distance = bounded_distance_certificate(first, max_weight=3)
        second_distance = bounded_distance_certificate(second, max_weight=3)
        method = "full_weight3_enumeration"
    else:
        first_distance = holographic_phase14_exact_distance_three_from_witness(first, patterns[0])
        second_distance = holographic_phase14_exact_distance_three_from_witness(second, patterns[1])
        method = "weight2_lower_bound_plus_explicit_weight3_witness"
    same_exact_distance_three = (
        first_distance["distance_exact_if_witness_found"] == 3
        and second_distance["distance_exact_if_witness_found"] == 3
    )
    return {
        "first": first_distance,
        "second": second_distance,
        "first_exact_distance": first_distance["distance_exact_if_witness_found"],
        "second_exact_distance": second_distance["distance_exact_if_witness_found"],
        "same_exact_distance_three": same_exact_distance_three,
        "distance_certification_method": method,
    }


def holographic_phase14_variant_record(
    *,
    spec: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
) -> dict[str, object]:
    bridge_axes = tuple(str(item) for item in spec["bridge_axes"])  # type: ignore[index]
    if len(bridge_axes) != 2:
        raise ValueError("Phase 14 variant bridge_axes must have length two")
    local_cliffords = tuple(str(item) for item in spec["local_cliffords"])  # type: ignore[index]
    outer = holographic_phase14_three_perfect_outer_code(
        bridge_axes=(bridge_axes[0], bridge_axes[1]),
        local_cliffords=local_cliffords,
    )
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    distance_audit = holographic_phase14_distance_audit(
        first=first,
        second=second,
        variant_name=str(spec["name"]),
    )
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    public_spec = dict(spec)
    return {
        "spec": public_spec,
        "outer": outer,
        "first": first,
        "second": second,
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "public": {
            "spec": public_spec,
            "outer_code": {
                "parameters": {"n": outer.n, "k": outer.k, "distance": outer.distance()},
                "erasure_threshold": outer.erasure_threshold(),
            },
            "code_pair": {"n": first.n, "k": first.k},
            "low_order_entropy": {
                "max_subset_size": low_order_entropy["max_subset_size"],
                "subsets_checked": low_order_entropy["subsets_checked"],
                "mismatch_count": low_order_entropy["mismatch_count"],
                "matches": low_order_entropy["matches"],
            },
            "distance_audit_weight3": {
                **distance_audit,
            },
            "classification": (
                "same_exact_distance_three"
                if distance_audit["same_exact_distance_three"]
                else "three_cell_distance_asymmetry_under_weight3_audit"
            ),
        },
    }


def holographic_phase14_boundary_templates() -> tuple[dict[str, object], ...]:
    inner_order = (0, 1, 2, 4, 3)
    block_size = 5
    block_count = 15
    block_contiguous = tuple(block * block_size + qubit for block in range(block_count) for qubit in inner_order)
    inner_major = tuple(block * block_size + qubit for qubit in inner_order for block in range(block_count))
    cell_major = tuple(
        block * block_size + qubit
        for cell in range(3)
        for qubit in inner_order
        for block in range(cell * 5, (cell + 1) * 5)
    )
    witness_prefix = tuple(block * block_size + qubit for block in range(block_count) for qubit in (2, 4))
    witness_set = set(witness_prefix)
    witness_strip = witness_prefix + tuple(qubit for qubit in block_contiguous if qubit not in witness_set)
    return (
        {
            "name": "three_perfect_block_contiguous",
            "template_kind": "three_tensor_block_local",
            "description": "Repeat the Phase 2 inner ring inside each of the fifteen outer tiling legs.",
            "boundary_order": block_contiguous,
        },
        {
            "name": "three_perfect_inner_major",
            "template_kind": "three_tensor_inner_major",
            "description": "Group equal inner positions across all fifteen outer tiling legs.",
            "boundary_order": inner_major,
        },
        {
            "name": "three_perfect_cell_major",
            "template_kind": "three_tensor_cell_major",
            "description": "Group equal inner positions inside each of the three perfect cells.",
            "boundary_order": cell_major,
        },
        {
            "name": "three_perfect_witness_strip",
            "template_kind": "source_aware_control",
            "description": "Place all lifted Phase 2 witness qubits first across the fifteen tiling legs.",
            "boundary_order": witness_strip,
        },
    )


def holographic_phase14_three_perfect_network_spec(
    boundary_order: tuple[int, ...],
    *,
    topology: str,
) -> dict[str, object]:
    if topology not in ("chain", "ring"):
        raise ValueError("topology must be chain or ring")
    edges = list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = ("perfect_tensor_0", "perfect_tensor_1", "perfect_tensor_2")
    for block in range(15):
        node = internal_nodes[block // 5]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="three_perfect_tensor_boundary_leg",
                )
            )
    for left, right in ((0, 1), (1, 2)):
        edges.append(
            holographic_phase4_edge(
                internal_nodes[left],
                internal_nodes[right],
                edge_type="three_perfect_tensor_chain_bridge",
                capacity=2,
            )
        )
    if topology == "ring":
        edges.append(
            holographic_phase4_edge(
                internal_nodes[2],
                internal_nodes[0],
                edge_type="three_perfect_tensor_ring_bridge",
                capacity=2,
            )
        )
    return {
        "name": f"three_five_qubit_perfect_tensor_{topology}_skeleton",
        "network_kind": f"three_perfect_tensor_{topology}",
        "description": (
            "Three internal perfect-tensor cells each attach to five encoded outer legs; capacity-2 internal bridge "
            "edges define either a chain or a triangle, and every boundary min-cut is enumerated over the three "
            "internal assignments."
        ),
        "topology": topology,
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase14_interval_template_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    template: dict[str, object],
    topology: str,
    max_interval_length: int,
    include_hit_records: bool = False,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase14_three_perfect_network_spec(boundary_order, topology=topology)
    intervals = holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
    entropy_gate_passes = 0
    entropy_gate_rejections = 0
    all_min_cuts_exact = True
    length_summaries = []
    hit_count = 0
    selected_hit = None
    hit_records = []
    circuit = {
        "name": f"{template['name']}_{topology}",
        "generator_kind": "three_perfect_tensor_tiling",
    }
    for length in range(1, max_interval_length + 1):
        length_intervals = tuple(region for region in intervals if int(region["length"]) == length)
        length_entropy_passes = 0
        length_hits = 0
        for region in length_intervals:
            region_mask = int(region["mask"])
            min_cut = holographic_network_min_cut(network_spec=network_spec, region_mask=region_mask)
            all_min_cuts_exact = all_min_cuts_exact and (
                min_cut["assignments_checked"] == 2 ** len(network_spec["internal_nodes"])  # type: ignore[arg-type]
            )
            first_entropy = first.entropy(region_mask)
            second_entropy = second.entropy(region_mask)
            if first_entropy != second_entropy:
                entropy_gate_rejections += 1
                continue
            entropy_gate_passes += 1
            length_entropy_passes += 1
            hit = holographic_phase7_hit_record(
                circuit=circuit,
                first=first,
                second=second,
                network_spec=network_spec,
                region=region,
            )
            if bool(hit["comparisons"]["operator_or_channel_visible_differs"]):  # type: ignore[index]
                hit_count += 1
                length_hits += 1
                if selected_hit is None or (
                    int(hit["region"]["length"]),  # type: ignore[index]
                    int(hit["region"]["start"]),  # type: ignore[index]
                ) < (
                    int(selected_hit["region"]["length"]),  # type: ignore[index]
                    int(selected_hit["region"]["start"]),  # type: ignore[index]
                ):
                    selected_hit = hit
                if include_hit_records:
                    hit_records.append(hit)
        length_summaries.append(
            {
                "length": length,
                "intervals_scanned": len(length_intervals),
                "entropy_gate_passes": length_entropy_passes,
                "entropy_gate_rejections": len(length_intervals) - length_entropy_passes,
                "operator_or_channel_hits": length_hits,
            }
        )
    return {
        "name": template["name"],
        "template_kind": template["template_kind"],
        "topology": topology,
        "description": template["description"],
        "boundary_order": boundary_order,
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "topology": network_spec["topology"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
            "internal_assignments_per_min_cut": 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
        "interval_search": {
            "max_interval_length": max_interval_length,
            "intervals_scanned": len(intervals),
            "entropy_gate_passes": entropy_gate_passes,
            "entropy_gate_rejections": entropy_gate_rejections,
            "all_candidate_min_cuts_exact": all_min_cuts_exact,
            "length_summaries": tuple(length_summaries),
            "hit_count": hit_count,
            "shortest_hit_length": None if selected_hit is None else int(selected_hit["region"]["length"]),  # type: ignore[index]
        },
        "selected_hit": selected_hit,
        "hit_records": tuple(hit_records),
    }


def bridge_holography_phase14_certificate(
    *,
    graph_max_codes: int = 24,
    max_interval_length: int = 8,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_interval_length < 8:
        raise ValueError("max_interval_length must be at least eight for the Phase 14 certificate")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 14 source must contain StabilizerCode objects")

    specs = holographic_phase14_variant_specs()
    variant_records = tuple(
        holographic_phase14_variant_record(
            spec=spec,
            inner_first=inner_first,
            inner_second=inner_second,
        )
        for spec in specs
    )
    same_distance_records = tuple(
        record
        for record in variant_records
        if record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
    )
    selected_variant_record = min(
        same_distance_records,
        key=lambda record: (
            int(record["public"]["spec"]["operation_weight"]),  # type: ignore[index]
            int(record["public"]["spec"]["local_map_complexity"]),  # type: ignore[index]
            str(record["public"]["spec"]["name"]),  # type: ignore[index]
        ),
    )
    selected_first = selected_variant_record["first"]
    selected_second = selected_variant_record["second"]
    selected_outer = selected_variant_record["outer"]
    if (
        not isinstance(selected_first, StabilizerCode)
        or not isinstance(selected_second, StabilizerCode)
        or not isinstance(selected_outer, StabilizerCode)
    ):
        raise TypeError("selected Phase 14 record must contain StabilizerCode objects")
    selected_topology_records = tuple(
        {
            "topology": topology,
            "templates": tuple(
                holographic_phase14_interval_template_record(
                    first=selected_first,
                    second=selected_second,
                    template=template,
                    topology=topology,
                    max_interval_length=max_interval_length,
                    include_hit_records=False,
                )
                for template in holographic_phase14_boundary_templates()
            ),
        }
        for topology in ("chain", "ring")
    )
    selected_records = tuple(
        record
        for topology_record in selected_topology_records
        for record in topology_record["templates"]  # type: ignore[index]
    )
    selected_by_topology = {
        str(topology_record["topology"]): {str(record["name"]): record for record in topology_record["templates"]}  # type: ignore[index]
        for topology_record in selected_topology_records
    }
    same_distance_by_family = {
        family: sum(
            1
            for record in same_distance_records
            if str(record["public"]["spec"]["family"]) == family  # type: ignore[index]
        )
        for family in sorted({str(spec["family"]) for spec in specs})
    }
    family_counts = tuple(
        {
            "family": family,
            "variants": sum(1 for spec in specs if str(spec["family"]) == family),
            "same_exact_distance_three": same_distance_by_family[family],
        }
        for family in sorted({str(spec["family"]) for spec in specs})
    )
    selected_counts = {
        "candidate_intervals_scanned": sum(
            int(record["interval_search"]["intervals_scanned"]) for record in selected_records  # type: ignore[index]
        ),
        "entropy_gate_passes": sum(
            int(record["interval_search"]["entropy_gate_passes"]) for record in selected_records  # type: ignore[index]
        ),
        "entropy_gate_rejections": sum(
            int(record["interval_search"]["entropy_gate_rejections"]) for record in selected_records  # type: ignore[index]
        ),
        "compact_interval_hits": sum(
            int(record["interval_search"]["hit_count"]) for record in selected_records  # type: ignore[index]
        ),
        "block_contiguous_hits": sum(
            int(selected_by_topology[topology]["three_perfect_block_contiguous"]["interval_search"]["hit_count"])  # type: ignore[index]
            for topology in selected_by_topology
        ),
        "inner_major_hits": sum(
            int(selected_by_topology[topology]["three_perfect_inner_major"]["interval_search"]["hit_count"])  # type: ignore[index]
            for topology in selected_by_topology
        ),
        "cell_major_hits": sum(
            int(selected_by_topology[topology]["three_perfect_cell_major"]["interval_search"]["hit_count"])  # type: ignore[index]
            for topology in selected_by_topology
        ),
        "witness_strip_hits": sum(
            int(selected_by_topology[topology]["three_perfect_witness_strip"]["interval_search"]["hit_count"])  # type: ignore[index]
            for topology in selected_by_topology
        ),
    }
    topology_summaries = tuple(
        {
            "topology": topology,
            "candidate_intervals_scanned": sum(
                int(record["interval_search"]["intervals_scanned"]) for record in template_map.values()  # type: ignore[index]
            ),
            "entropy_gate_passes": sum(
                int(record["interval_search"]["entropy_gate_passes"]) for record in template_map.values()  # type: ignore[index]
            ),
            "entropy_gate_rejections": sum(
                int(record["interval_search"]["entropy_gate_rejections"]) for record in template_map.values()  # type: ignore[index]
            ),
            "compact_interval_hits": sum(
                int(record["interval_search"]["hit_count"]) for record in template_map.values()  # type: ignore[index]
            ),
            "block_contiguous_hits": int(
                template_map["three_perfect_block_contiguous"]["interval_search"]["hit_count"]  # type: ignore[index]
            ),
            "inner_major_hits": int(
                template_map["three_perfect_inner_major"]["interval_search"]["hit_count"]  # type: ignore[index]
            ),
            "cell_major_hits": int(
                template_map["three_perfect_cell_major"]["interval_search"]["hit_count"]  # type: ignore[index]
            ),
            "witness_strip_hits": int(
                template_map["three_perfect_witness_strip"]["interval_search"]["hit_count"]  # type: ignore[index]
            ),
        }
        for topology, template_map in selected_by_topology.items()
    )
    chain_hit = selected_by_topology["chain"]["three_perfect_inner_major"]["selected_hit"]
    ring_hit = selected_by_topology["ring"]["three_perfect_inner_major"]["selected_hit"]
    identity_records = tuple(
        record for record in variant_records if record["public"]["spec"]["family"] == "bridge_identity"  # type: ignore[index]
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "three_perfect_chain_menu_scored": len(specs) == 9 and len(variant_records) == 9,
        "three_perfect_outer_codes_are_k1_distance3": all(
            record["public"]["outer_code"]["parameters"]["k"] == 1  # type: ignore[index]
            and record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
            and record["public"]["outer_code"]["erasure_threshold"] == 2  # type: ignore[index]
            for record in variant_records
        ),
        "all_variants_preserve_labeled_t2_entropy": all(
            record["public"]["low_order_entropy"]["matches"] for record in variant_records  # type: ignore[index]
        ),
        "unrepaired_bridge_identities_are_distance_asymmetric": len(identity_records) == 3
        and all(
            not record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
            for record in identity_records
        ),
        "single_cell_axis_repairs_are_same_distance": len(same_distance_records) == 6,
        "selected_variant_is_yy_q0_h": str(selected_variant_record["public"]["spec"]["name"]) == "YY_q0_H",  # type: ignore[index]
        "chain_and_ring_skeletons_scored": len(selected_topology_records) == 2
        and all(len(topology_record["templates"]) == 4 for topology_record in selected_topology_records),  # type: ignore[index]
        "block_contiguous_remains_zero_hit_control": selected_counts["block_contiguous_hits"] == 0,
        "chain_and_ring_inner_major_hits_match": int(
            selected_by_topology["chain"]["three_perfect_inner_major"]["interval_search"]["hit_count"]  # type: ignore[index]
        )
        == int(selected_by_topology["ring"]["three_perfect_inner_major"]["interval_search"]["hit_count"])  # type: ignore[index]
        == 27,
        "selected_inner_major_witness_matches_across_topologies": chain_hit is not None
        and ring_hit is not None
        and chain_hit["region"]["qubits"] == ring_hit["region"]["qubits"]  # type: ignore[index]
        and chain_hit["first"]["algebra_signature"] == ring_hit["first"]["algebra_signature"]  # type: ignore[index]
        and chain_hit["second"]["algebra_signature"] == ring_hit["second"]["algebra_signature"],  # type: ignore[index]
        "selected_interval_mincuts_exact": all(
            record["interval_search"]["all_candidate_min_cuts_exact"] for record in selected_records  # type: ignore[index]
        ),
    }
    phase_claims["goal_3_phase_14_three_perfect_chain_ring_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 14: three-perfect-cell chain/ring atlas audit",
        "status": "pass" if phase_claims["goal_3_phase_14_three_perfect_chain_ring_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "tiling_outer_code": {
            "selected": holographic_phase14_outer_code_summary(
                selected_outer,
                bridge_axes=tuple(selected_variant_record["public"]["spec"]["bridge_axes"]),  # type: ignore[index]
                local_cliffords=tuple(selected_variant_record["public"]["spec"]["local_cliffords"]),  # type: ignore[index]
            ),
            "menu_description": (
                "Three [[5,1,3]] perfect outer blocks joined by two encoded nearest-neighbor bridge stabilizers, "
                "with a bounded axis/leg repair menu."
            ),
        },
        "tiling_variant_search": {
            "family_counts": family_counts,
            "variant_records": tuple(record["public"] for record in variant_records),
            "same_distance_variant_names": tuple(
                str(record["public"]["spec"]["name"]) for record in same_distance_records  # type: ignore[index]
            ),
        },
        "selected_same_distance_tiling": {
            "variant_record": selected_variant_record["public"],
            "topology_summaries": topology_summaries,
            "topology_atlas_search": selected_topology_records,
            "selected_chain_inner_major_hit": chain_hit,
            "selected_ring_inner_major_hit": ring_hit,
        },
        "counts": {
            "tiling_variants_scored": len(variant_records),
            "bridge_identity_variants": len(identity_records),
            "outer_variants_k1_distance3": sum(
                1
                for record in variant_records
                if record["public"]["outer_code"]["parameters"]["k"] == 1  # type: ignore[index]
                and record["public"]["outer_code"]["parameters"]["distance"] == 3  # type: ignore[index]
            ),
            "low_order_t2_matches": sum(
                1 for record in variant_records if record["public"]["low_order_entropy"]["matches"]  # type: ignore[index]
            ),
            "same_exact_distance_three_variants": len(same_distance_records),
            "distance_asymmetric_identity_variants": sum(
                1
                for record in identity_records
                if not record["public"]["distance_audit_weight3"]["same_exact_distance_three"]  # type: ignore[index]
            ),
            "selected_topologies_scored": len(selected_topology_records),
            "selected_templates_per_topology": len(selected_topology_records[0]["templates"]),  # type: ignore[index]
            "selected_candidate_intervals_scanned": selected_counts["candidate_intervals_scanned"],
            "selected_entropy_gate_passes": selected_counts["entropy_gate_passes"],
            "selected_entropy_gate_rejections": selected_counts["entropy_gate_rejections"],
            "selected_compact_interval_hits": selected_counts["compact_interval_hits"],
            "selected_block_contiguous_hits": selected_counts["block_contiguous_hits"],
            "selected_inner_major_hits": selected_counts["inner_major_hits"],
            "selected_cell_major_hits": selected_counts["cell_major_hits"],
            "selected_witness_strip_hits": selected_counts["witness_strip_hits"],
            "chain_compact_interval_hits": next(
                int(record["compact_interval_hits"]) for record in topology_summaries if record["topology"] == "chain"
            ),
            "ring_compact_interval_hits": next(
                int(record["compact_interval_hits"]) for record in topology_summaries if record["topology"] == "ring"
            ),
            "max_candidate_min_cut_internal_assignments": max(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in selected_records  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A real three-perfect-block outer stabilizer chain gives an n=75,k=1 concatenated pair with matching "
                "labeled t<=2 entropy and same exact distance three after a one-leg YY Hadamard repair. The selected "
                "compact interval keeps matching entropy/min-cut data while operator and erasure semantics split."
            ),
            "three_geometry_lesson": (
                "The compact split survives a larger three-cell tiling and is stable under the declared chain-vs-ring "
                "min-cut skeleton replay, but block-contiguous locality remains a zero-hit control. Source-aware atlas "
                "semantics still matter."
            ),
            "scope_warning": (
                "This is an exact finite three-cell stabilizer chain and two declared min-cut skeletons, not an "
                "exhaustive search over all three-cell local-Clifford embeddings, all bridge axes, or a full HaPPY "
                "tiling."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 14 shows the selected compact split survives from two cells to three cells and is stable under "
                "chain/ring skeleton replay. The next phase should vary bridge capacity or add an actual branching "
                "bulk/tree tiling to test whether the zero-hit block-contiguous control can be overcome without "
                "source-aware ordering."
            ),
            "suggested_phase_15": (
                "Search a small branching perfect-cell tree or bridge-capacity grammar, retaining exact low-order "
                "entropy, min-cut, algebra, erasure, survivor, and distance certificates."
            ),
        },
    }


def holographic_phase15_skeleton_specs() -> tuple[dict[str, object], ...]:
    specs: list[dict[str, object]] = []

    def add(name: str, topology: str, capacities: tuple[int, ...], description: str) -> None:
        specs.append(
            {
                "name": name,
                "topology": topology,
                "capacities": capacities,
                "description": description,
            }
        )

    for capacities in ((1, 1), (2, 2), (3, 3), (1, 3), (3, 1)):
        add(
            f"chain_{capacities[0]}_{capacities[1]}",
            "chain",
            capacities,
            "Three cell nodes with two nearest-neighbor bridge edges.",
        )
    for capacities in ((1, 1, 1), (2, 2, 2), (3, 3, 3), (1, 2, 3), (3, 2, 1)):
        add(
            f"ring_{capacities[0]}_{capacities[1]}_{capacities[2]}",
            "ring",
            capacities,
            "Three cell nodes with a triangular internal bridge cycle.",
        )
    for capacities in ((1, 1, 1), (2, 2, 2), (3, 3, 3), (1, 2, 3), (3, 2, 1)):
        add(
            f"rooted_branch_{capacities[0]}_{capacities[1]}_{capacities[2]}",
            "rooted_branch",
            capacities,
            "Three cell nodes connected only through a central branch/root node.",
        )
    for capacities in ((2, 2, 1, 1, 1), (2, 2, 2, 2, 2), (1, 3, 1, 2, 3)):
        add(
            "branch_plus_chain_" + "_".join(str(item) for item in capacities),
            "branch_plus_chain",
            capacities,
            "Nearest-neighbor cell chain plus a central branch/root node.",
        )
    return tuple(specs)


def holographic_phase15_capacity_network_spec(
    boundary_order: tuple[int, ...],
    skeleton_spec: dict[str, object],
) -> dict[str, object]:
    topology = str(skeleton_spec["topology"])
    capacities = tuple(int(item) for item in skeleton_spec["capacities"])  # type: ignore[index]
    edges = list(holographic_phase4_boundary_ring_edges(boundary_order))
    cell_nodes = ("perfect_tensor_0", "perfect_tensor_1", "perfect_tensor_2")
    for block in range(15):
        node = cell_nodes[block // 5]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="three_perfect_tensor_boundary_leg",
                )
            )
    internal_nodes = cell_nodes
    if topology == "chain":
        if len(capacities) != 2:
            raise ValueError("chain skeletons require two capacities")
        for (left, right), capacity in zip(((0, 1), (1, 2)), capacities):
            edges.append(
                holographic_phase4_edge(
                    cell_nodes[left],
                    cell_nodes[right],
                    edge_type="capacity_grammar_chain_bridge",
                    capacity=capacity,
                )
            )
    elif topology == "ring":
        if len(capacities) != 3:
            raise ValueError("ring skeletons require three capacities")
        for (left, right), capacity in zip(((0, 1), (1, 2), (2, 0)), capacities):
            edges.append(
                holographic_phase4_edge(
                    cell_nodes[left],
                    cell_nodes[right],
                    edge_type="capacity_grammar_ring_bridge",
                    capacity=capacity,
                )
            )
    elif topology == "rooted_branch":
        if len(capacities) != 3:
            raise ValueError("rooted_branch skeletons require three capacities")
        internal_nodes = cell_nodes + ("perfect_tensor_root",)
        for cell_node, capacity in zip(cell_nodes, capacities):
            edges.append(
                holographic_phase4_edge(
                    "perfect_tensor_root",
                    cell_node,
                    edge_type="capacity_grammar_root_branch",
                    capacity=capacity,
                )
            )
    elif topology == "branch_plus_chain":
        if len(capacities) != 5:
            raise ValueError("branch_plus_chain skeletons require five capacities")
        internal_nodes = cell_nodes + ("perfect_tensor_root",)
        for (left, right), capacity in zip(((0, 1), (1, 2)), capacities[:2]):
            edges.append(
                holographic_phase4_edge(
                    cell_nodes[left],
                    cell_nodes[right],
                    edge_type="capacity_grammar_chain_bridge",
                    capacity=capacity,
                )
            )
        for cell_node, capacity in zip(cell_nodes, capacities[2:]):
            edges.append(
                holographic_phase4_edge(
                    "perfect_tensor_root",
                    cell_node,
                    edge_type="capacity_grammar_root_branch",
                    capacity=capacity,
                )
            )
    else:
        raise ValueError(f"unknown Phase 15 skeleton topology {topology!r}")
    return {
        "name": skeleton_spec["name"],
        "network_kind": f"phase15_{topology}",
        "description": skeleton_spec["description"],
        "topology": topology,
        "capacities": capacities,
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase15_fixed_witness_regions() -> tuple[dict[str, object], ...]:
    return (
        {
            "name": "inner_major_local_short",
            "template": "three_perfect_inner_major",
            "region_type": "phase14_selected_local_compact_witness",
            "qubits": (4, 9, 14),
            "description": "The Phase 14 shortest compact witness, contained inside one perfect cell.",
        },
        {
            "name": "inner_major_cross_cell_short",
            "template": "three_perfect_inner_major",
            "region_type": "phase15_cross_cell_compact_witness",
            "qubits": (14, 19, 24, 29),
            "description": "A length-four inner-major compact witness spanning perfect cells 0 and 1.",
        },
        {
            "name": "witness_strip_cross_cell",
            "template": "three_perfect_witness_strip",
            "region_type": "phase15_cross_cell_witness_strip",
            "qubits": (14, 17, 19, 22, 24, 27),
            "description": "A source-aware witness-strip compact region spanning perfect cells 0 and 1.",
        },
    )


def holographic_phase15_region_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region_spec: dict[str, object],
    skeleton_spec: dict[str, object],
) -> dict[str, object]:
    template_by_name = {str(template["name"]): template for template in holographic_phase14_boundary_templates()}
    template = template_by_name[str(region_spec["template"])]
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase15_capacity_network_spec(boundary_order, skeleton_spec)
    qubits = tuple(int(qubit) for qubit in region_spec["qubits"])  # type: ignore[index]
    region = {
        "name": region_spec["name"],
        "region_type": region_spec["region_type"],
        "template": region_spec["template"],
        "description": region_spec["description"],
        "qubits": qubits,
        "length": len(qubits),
        "outer_blocks": tuple(sorted({qubit // 5 for qubit in qubits})),
        "perfect_cells": tuple(sorted({(qubit // 5) // 5 for qubit in qubits})),
        "mask": mask_from_qubits(qubits),
    }
    hit = holographic_phase7_hit_record(
        circuit={
            "name": f"{region_spec['name']}__{skeleton_spec['name']}",
            "generator_kind": "phase15_capacity_branching_grammar",
        },
        first=first,
        second=second,
        network_spec=network_spec,
        region=region,
    )
    return {
        "region": {key: value for key, value in region.items() if key != "mask"},
        "skeleton": {
            "name": skeleton_spec["name"],
            "topology": skeleton_spec["topology"],
            "capacities": skeleton_spec["capacities"],
            "description": skeleton_spec["description"],
        },
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "topology": network_spec["topology"],
            "capacities": network_spec["capacities"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
            "internal_assignments_per_min_cut": 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
        "hit": hit,
    }


def bridge_holography_phase15_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 15 source must contain StabilizerCode objects")
    selected_spec = next(spec for spec in holographic_phase14_variant_specs() if str(spec["name"]) == "YY_q0_H")
    selected_variant_record = holographic_phase14_variant_record(
        spec=selected_spec,
        inner_first=inner_first,
        inner_second=inner_second,
    )
    selected_first = selected_variant_record["first"]
    selected_second = selected_variant_record["second"]
    selected_outer = selected_variant_record["outer"]
    if (
        not isinstance(selected_first, StabilizerCode)
        or not isinstance(selected_second, StabilizerCode)
        or not isinstance(selected_outer, StabilizerCode)
    ):
        raise TypeError("selected Phase 15 record must contain StabilizerCode objects")

    skeleton_specs = holographic_phase15_skeleton_specs()
    region_specs = holographic_phase15_fixed_witness_regions()
    records = tuple(
        holographic_phase15_region_record(
            first=selected_first,
            second=selected_second,
            region_spec=region_spec,
            skeleton_spec=skeleton_spec,
        )
        for region_spec in region_specs
        for skeleton_spec in skeleton_specs
    )
    records_by_region = {
        str(region_spec["name"]): tuple(record for record in records if record["region"]["name"] == region_spec["name"])
        for region_spec in region_specs
    }
    region_summaries = tuple(
        {
            "region": region_name,
            "records": len(region_records),
            "min_cut_values": tuple(sorted({int(record["hit"]["min_cut"]["value"]) for record in region_records})),  # type: ignore[index]
            "min_cut_value_range": (
                min(int(record["hit"]["min_cut"]["value"]) for record in region_records),  # type: ignore[index]
                max(int(record["hit"]["min_cut"]["value"]) for record in region_records),  # type: ignore[index]
            ),
            "entropy_values": tuple(
                sorted({(int(record["hit"]["first"]["entropy"]), int(record["hit"]["second"]["entropy"])) for record in region_records})  # type: ignore[index]
            ),
            "operator_or_channel_split_records": sum(
                1
                for record in region_records
                if bool(record["hit"]["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
            ),
            "topologies": tuple(sorted({str(record["skeleton"]["topology"]) for record in region_records})),
        }
        for region_name, region_records in records_by_region.items()
    )
    topology_counts = tuple(
        {
            "topology": topology,
            "skeletons": sum(1 for spec in skeleton_specs if str(spec["topology"]) == topology),
            "records": sum(1 for record in records if str(record["skeleton"]["topology"]) == topology),
        }
        for topology in sorted({str(spec["topology"]) for spec in skeleton_specs})
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "selected_phase14_tiling_loaded": selected_variant_record["public"]["distance_audit_weight3"][  # type: ignore[index]
            "same_exact_distance_three"
        ],
        "capacity_branching_skeleton_grammar_scored": len(skeleton_specs) == 18
        and len(region_specs) == 3
        and len(records) == 54,
        "branching_skeletons_included": any(str(spec["topology"]) == "rooted_branch" for spec in skeleton_specs)
        and any(str(spec["topology"]) == "branch_plus_chain" for spec in skeleton_specs),
        "all_mincuts_exact": all(record["hit"]["comparisons"]["min_cut_exact"] for record in records),  # type: ignore[index]
        "all_fixed_regions_keep_entropy_match": all(
            record["hit"]["comparisons"]["entropy_matches"] for record in records  # type: ignore[index]
        ),
        "all_fixed_regions_keep_operator_or_channel_split": all(
            record["hit"]["comparisons"]["operator_or_channel_visible_differs"] for record in records  # type: ignore[index]
        ),
        "all_fixed_region_mincuts_invariant_across_capacity_grammar": all(
            len(summary["min_cut_values"]) == 1 for summary in region_summaries  # type: ignore[index]
        ),
        "cross_cell_witnesses_included": all(
            len(record["region"]["perfect_cells"]) > 1  # type: ignore[index]
            for record in records_by_region["inner_major_cross_cell_short"] + records_by_region["witness_strip_cross_cell"]
        ),
    }
    phase_claims["goal_3_phase_15_capacity_branching_grammar_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 15: capacity and branching fixed-witness grammar audit",
        "status": "pass" if phase_claims["goal_3_phase_15_capacity_branching_grammar_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "selected_tiling": {
            "variant_record": selected_variant_record["public"],
            "outer_code": holographic_phase14_outer_code_summary(
                selected_outer,
                bridge_axes=tuple(selected_variant_record["public"]["spec"]["bridge_axes"]),  # type: ignore[index]
                local_cliffords=tuple(selected_variant_record["public"]["spec"]["local_cliffords"]),  # type: ignore[index]
            ),
        },
        "capacity_branching_grammar": {
            "skeleton_specs": skeleton_specs,
            "fixed_witness_regions": region_specs,
            "topology_counts": topology_counts,
            "region_summaries": region_summaries,
            "records": records,
        },
        "counts": {
            "skeletons_scored": len(skeleton_specs),
            "fixed_regions_scored": len(region_specs),
            "region_skeleton_records": len(records),
            "topologies_scored": len(topology_counts),
            "branching_skeletons": sum(
                1 for spec in skeleton_specs if str(spec["topology"]) in ("rooted_branch", "branch_plus_chain")
            ),
            "min_cut_invariant_regions": sum(1 for summary in region_summaries if len(summary["min_cut_values"]) == 1),  # type: ignore[index]
            "min_cut_variable_regions": sum(1 for summary in region_summaries if len(summary["min_cut_values"]) > 1),  # type: ignore[index]
            "entropy_match_records": sum(
                1 for record in records if record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "operator_or_channel_split_records": sum(
                1
                for record in records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in records
            ),
            "min_candidate_min_cut_internal_assignments": min(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in records
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "For three fixed compact witnesses of the selected Phase 14 n=75 same-distance tiling, the operator "
                "and erasure split survives across 18 exact chain/ring/branching min-cut skeletons. The tested "
                "capacity grammar changes the declared bulk graph but not the witness min-cut values."
            ),
            "three_geometry_lesson": (
                "This is a finite no-go/robustness result: for the certified compact witnesses, reconstruction-visible "
                "and erasure-visible geometry remain split, while min-cut-visible geometry is invariant under the "
                "tested bridge-capacity and branch/root rewiring grammar."
            ),
            "scope_warning": (
                "Phase 15 audits fixed witness regions rather than all boundary intervals. It does not prove that no "
                "larger interval has capacity-sensitive min-cut behavior, and it does not exhaust all branching "
                "tensor-network skeletons."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The fixed compact witnesses are robust but not capacity-sensitive. The next phase should either run "
                "a bounded search specifically for capacity-sensitive operator/erasure hits, or move to a larger "
                "branching code where the witness itself crosses an internal bottleneck."
            ),
            "suggested_phase_16": (
                "Search for capacity-sensitive compact witnesses with a bounded interval grammar and early min-cut "
                "variation filtering, then certify any hits with exact entropy, algebra, erasure, survivor, and "
                "distance checks."
            ),
        },
    }


def holographic_phase16_probe_skeleton_names() -> tuple[str, ...]:
    return (
        "chain_1_1",
        "chain_3_3",
        "ring_1_1_1",
        "ring_3_3_3",
        "rooted_branch_1_1_1",
        "rooted_branch_3_3_3",
        "branch_plus_chain_2_2_1_1_1",
        "branch_plus_chain_2_2_2_2_2",
    )


def holographic_phase16_template_names() -> tuple[str, ...]:
    return ("three_perfect_inner_major", "three_perfect_witness_strip")


def holographic_phase16_interval_search_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    template: dict[str, object],
    skeleton_specs: tuple[dict[str, object], ...],
    min_interval_length: int,
    max_interval_length: int,
    max_examples: int = 3,
) -> dict[str, object]:
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    networks = tuple(holographic_phase15_capacity_network_spec(boundary_order, spec) for spec in skeleton_specs)
    intervals = tuple(
        region
        for region in holographic_ring_interval_regions(boundary_order, max_length=max_interval_length)
        if int(region["length"]) >= min_interval_length
    )
    intervals_scanned = 0
    variable_min_cut_intervals = 0
    entropy_match_after_variation = 0
    operator_or_channel_hits = 0
    all_mincuts_exact = True
    length_summaries = []
    variable_examples = []
    entropy_match_examples = []
    hit_records = []
    circuit = {
        "name": f"{template['name']}_phase16_capacity_sensitive_probe",
        "generator_kind": "phase16_capacity_sensitive_interval_search",
    }
    for length in range(min_interval_length, max_interval_length + 1):
        length_intervals = tuple(region for region in intervals if int(region["length"]) == length)
        length_variable = 0
        length_entropy = 0
        length_hits = 0
        for region in length_intervals:
            intervals_scanned += 1
            min_cuts = tuple(
                holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))
                for network in networks
            )
            all_mincuts_exact = all_mincuts_exact and all(
                int(min_cut["assignments_checked"]) == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
                for min_cut, network in zip(min_cuts, networks)
            )
            min_cut_values = tuple(int(min_cut["value"]) for min_cut in min_cuts)
            if len(set(min_cut_values)) == 1:
                continue
            variable_min_cut_intervals += 1
            length_variable += 1
            if len(variable_examples) < max_examples:
                variable_examples.append(
                    {
                        "region": {key: value for key, value in region.items() if key != "mask"},
                        "min_cut_values_by_skeleton": tuple(
                            {
                                "skeleton": str(spec["name"]),
                                "value": value,
                            }
                            for spec, value in zip(skeleton_specs, min_cut_values)
                        ),
                    }
                )
            first_entropy = first.entropy(int(region["mask"]))
            second_entropy = second.entropy(int(region["mask"]))
            if first_entropy != second_entropy:
                continue
            entropy_match_after_variation += 1
            length_entropy += 1
            if len(entropy_match_examples) < max_examples:
                entropy_match_examples.append(
                    {
                        "region": {key: value for key, value in region.items() if key != "mask"},
                        "entropies": {"first": first_entropy, "second": second_entropy},
                        "min_cut_values_by_skeleton": tuple(
                            {
                                "skeleton": str(spec["name"]),
                                "value": value,
                            }
                            for spec, value in zip(skeleton_specs, min_cut_values)
                        ),
                    }
                )
            hit = holographic_phase7_hit_record(
                circuit=circuit,
                first=first,
                second=second,
                network_spec=networks[0],
                region=region,
            )
            if bool(hit["comparisons"]["operator_or_channel_visible_differs"]):  # type: ignore[index]
                operator_or_channel_hits += 1
                length_hits += 1
                if len(hit_records) < max_examples:
                    hit_records.append(
                        {
                            "hit": hit,
                            "min_cut_values_by_skeleton": tuple(
                                {
                                    "skeleton": str(spec["name"]),
                                    "value": value,
                                }
                                for spec, value in zip(skeleton_specs, min_cut_values)
                            ),
                        }
                    )
        length_summaries.append(
            {
                "length": length,
                "intervals_scanned": len(length_intervals),
                "variable_min_cut_intervals": length_variable,
                "entropy_match_after_variation": length_entropy,
                "operator_or_channel_hits": length_hits,
            }
        )
    return {
        "template": {
            "name": template["name"],
            "template_kind": template["template_kind"],
            "description": template["description"],
        },
        "search_window": {
            "min_interval_length": min_interval_length,
            "max_interval_length": max_interval_length,
        },
        "skeletons": tuple(
            {
                "name": spec["name"],
                "topology": spec["topology"],
                "capacities": spec["capacities"],
            }
            for spec in skeleton_specs
        ),
        "interval_search": {
            "intervals_scanned": intervals_scanned,
            "variable_min_cut_intervals": variable_min_cut_intervals,
            "entropy_match_after_variation": entropy_match_after_variation,
            "operator_or_channel_hits": operator_or_channel_hits,
            "all_mincuts_exact": all_mincuts_exact,
            "length_summaries": tuple(length_summaries),
        },
        "variable_examples": tuple(variable_examples),
        "entropy_match_examples": tuple(entropy_match_examples),
        "hit_records": tuple(hit_records),
    }


def bridge_holography_phase16_certificate(
    *,
    graph_max_codes: int = 24,
    min_interval_length: int = 9,
    max_interval_length: int = 45,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if min_interval_length < 1 or max_interval_length < min_interval_length:
        raise ValueError("invalid Phase 16 interval length window")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 16 source must contain StabilizerCode objects")
    selected_spec = next(spec for spec in holographic_phase14_variant_specs() if str(spec["name"]) == "YY_q0_H")
    selected_variant_record = holographic_phase14_variant_record(
        spec=selected_spec,
        inner_first=inner_first,
        inner_second=inner_second,
    )
    selected_first = selected_variant_record["first"]
    selected_second = selected_variant_record["second"]
    if not isinstance(selected_first, StabilizerCode) or not isinstance(selected_second, StabilizerCode):
        raise TypeError("selected Phase 16 record must contain StabilizerCode objects")
    skeleton_by_name = {str(spec["name"]): spec for spec in holographic_phase15_skeleton_specs()}
    skeleton_specs = tuple(skeleton_by_name[name] for name in holographic_phase16_probe_skeleton_names())
    template_by_name = {str(template["name"]): template for template in holographic_phase14_boundary_templates()}
    templates = tuple(template_by_name[name] for name in holographic_phase16_template_names())
    template_records = tuple(
        holographic_phase16_interval_search_record(
            first=selected_first,
            second=selected_second,
            template=template,
            skeleton_specs=skeleton_specs,
            min_interval_length=min_interval_length,
            max_interval_length=max_interval_length,
        )
        for template in templates
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "selected_phase14_tiling_loaded": selected_variant_record["public"]["distance_audit_weight3"][  # type: ignore[index]
            "same_exact_distance_three"
        ],
        "bounded_capacity_sensitive_interval_search_scored": len(skeleton_specs) == 8
        and len(template_records) == 2
        and sum(int(record["interval_search"]["intervals_scanned"]) for record in template_records) == 5550,
        "min_cut_variation_filter_nonempty": sum(
            int(record["interval_search"]["variable_min_cut_intervals"]) for record in template_records
        )
        > 0,
        "entropy_candidates_after_variation_exist": sum(
            int(record["interval_search"]["entropy_match_after_variation"]) for record in template_records
        )
        > 0,
        "all_filtered_mincuts_exact": all(record["interval_search"]["all_mincuts_exact"] for record in template_records),  # type: ignore[index]
        "no_capacity_sensitive_operator_or_channel_hits_found": all(
            int(record["interval_search"]["operator_or_channel_hits"]) == 0 for record in template_records
        ),
    }
    phase_claims["goal_3_phase_16_capacity_sensitive_interval_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 16: bounded capacity-sensitive interval no-go audit",
        "status": "pass" if phase_claims["goal_3_phase_16_capacity_sensitive_interval_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "selected_tiling": {
            "variant_record": selected_variant_record["public"],
        },
        "search_grammar": {
            "skeletons": tuple(
                {
                    "name": spec["name"],
                    "topology": spec["topology"],
                    "capacities": spec["capacities"],
                }
                for spec in skeleton_specs
            ),
            "templates": holographic_phase16_template_names(),
            "min_interval_length": min_interval_length,
            "max_interval_length": max_interval_length,
            "filter_order": (
                "exact min-cut variation across the probe skeletons",
                "exact entropy match between the paired codes",
                "exact operator/reconstruction or erasure/survivor split",
            ),
        },
        "template_searches": template_records,
        "counts": {
            "templates_scored": len(template_records),
            "probe_skeletons": len(skeleton_specs),
            "intervals_scanned": sum(int(record["interval_search"]["intervals_scanned"]) for record in template_records),
            "variable_min_cut_intervals": sum(
                int(record["interval_search"]["variable_min_cut_intervals"]) for record in template_records
            ),
            "entropy_match_after_variation": sum(
                int(record["interval_search"]["entropy_match_after_variation"]) for record in template_records
            ),
            "operator_or_channel_hits": sum(
                int(record["interval_search"]["operator_or_channel_hits"]) for record in template_records
            ),
            "inner_major_variable_min_cut_intervals": int(
                template_records[0]["interval_search"]["variable_min_cut_intervals"]  # type: ignore[index]
            ),
            "inner_major_entropy_match_after_variation": int(
                template_records[0]["interval_search"]["entropy_match_after_variation"]  # type: ignore[index]
            ),
            "witness_strip_variable_min_cut_intervals": int(
                template_records[1]["interval_search"]["variable_min_cut_intervals"]  # type: ignore[index]
            ),
            "witness_strip_entropy_match_after_variation": int(
                template_records[1]["interval_search"]["entropy_match_after_variation"]  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded interval search found many regions whose min-cut-visible geometry changes across the "
                "capacity/branching probe skeletons, and some of those also preserve entropy matching. None of the "
                "entropy-matched, min-cut-variable regions in the searched source-aware templates preserve the "
                "operator/erasure split."
            ),
            "three_geometry_lesson": (
                "This is the first explicit no-go separating capacity sensitivity from the bridge witness: in this "
                "bounded grammar, min-cut-visible variation exists, but it does not coincide with the reconstruction- "
                "or channel-visible split."
            ),
            "scope_warning": (
                "The audit covers two source-aware boundary templates and intervals of length 9 through 45. It excludes "
                "block-contiguous and cell-major templates from the certified search window, and it is not a theorem "
                "over all intervals or all skeletons."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The capacity-sensitive interval grammar has min-cut and entropy candidates but no operator/channel "
                "hits. The next phase should change the code/atlas, not only the min-cut skeleton, so the logical "
                "witness is forced across a genuine internal bottleneck."
            ),
            "suggested_phase_17": (
                "Build a branching outer stabilizer code or four-cell tree where the bridge logical is supported across "
                "two arms, then replay exact entropy, min-cut, algebra, erasure, survivor, and distance diagnostics."
            ),
        },
    }


def holographic_phase17_four_perfect_outer_code(
    *,
    bridge_axes: tuple[str, str, str] = ("Y", "Y", "Y"),
    local_cliffords: tuple[str, ...] | None = None,
) -> StabilizerCode:
    if len(bridge_axes) != 3:
        raise ValueError("Phase 17 four-cell tree requires three bridge axes")
    if any(axis not in ("Z", "X", "Y") for axis in bridge_axes):
        raise ValueError("bridge axes must be Z, X, or Y")
    base = holographic_phase10_five_qubit_perfect_code()
    rows: list[int] = []
    for block in range(4):
        for generator in base.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=5, block_count=4))
    logical_z, logical_x = base.logical_basis
    logical_by_axis = {
        "Z": logical_z,
        "X": logical_x,
        "Y": logical_z ^ logical_x,
    }
    for (left, right), axis in zip(((0, 1), (1, 2), (1, 3)), bridge_axes):
        bridge_logical = logical_by_axis[axis]
        rows.append(
            block_shift_pauli(bridge_logical, block=left, block_size=5, block_count=4)
            ^ block_shift_pauli(bridge_logical, block=right, block_size=5, block_count=4)
        )
    code = StabilizerCode(20, rows)
    if local_cliffords is None:
        return code
    if len(local_cliffords) != code.n:
        raise ValueError("local_cliffords must have length twenty for the Phase 17 outer tree")
    named_maps = holographic_phase11_local_clifford_maps()
    maps = tuple(named_maps[name] for name in local_cliffords)
    return StabilizerCode(code.n, (local_clifford_pauli(row, code.n, maps) for row in code.generators))


def holographic_phase17_default_local_cliffords() -> tuple[str, ...]:
    local = ["I"] * 20
    local[0] = "H"
    return tuple(local)


def holographic_phase17_outer_code_summary(
    outer: StabilizerCode,
    *,
    bridge_axes: tuple[str, ...],
    local_cliffords: tuple[str, ...],
) -> dict[str, object]:
    distance_audit = bounded_distance_certificate(outer, max_weight=3)
    return {
        "name": "four_five_qubit_perfect_blocks_tree",
        "construction": (
            "Four copies of the canonical [[5,1,3]] outer block joined by three encoded logical bridge "
            "stabilizers on the tree edges 0-1, 1-2, and 1-3, leaving one outer logical qubit."
        ),
        "tree_edges": ((0, 1), (1, 2), (1, 3)),
        "bridge_axes": bridge_axes,
        "local_cliffords": local_cliffords,
        "parameters": {"n": outer.n, "k": outer.k},
        "generators": outer.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
        "distance_audit_weight3": distance_audit,
        "erasure_threshold": outer.erasure_threshold(),
        "cell_code": holographic_phase10_outer_code_summary(holographic_phase10_five_qubit_perfect_code()),
        "four_cell_checks": {
            "four_literal_perfect_cells": True,
            "three_tree_bridge_stabilizers": True,
            "outer_k1": outer.k == 1,
            "outer_distance_three_witnessed": distance_audit["distance_exact_if_witness_found"] == 3,
        },
    }


def holographic_phase17_boundary_templates() -> tuple[dict[str, object], ...]:
    inner_order = (0, 1, 2, 4, 3)
    block_size = 5
    block_count = 20
    block_contiguous = tuple(block * block_size + qubit for block in range(block_count) for qubit in inner_order)
    inner_major = tuple(block * block_size + qubit for qubit in inner_order for block in range(block_count))
    cell_major = tuple(
        block * block_size + qubit
        for cell in range(4)
        for qubit in inner_order
        for block in range(cell * 5, (cell + 1) * 5)
    )
    witness_prefix = tuple(block * block_size + qubit for block in range(block_count) for qubit in (2, 4))
    witness_set = set(witness_prefix)
    witness_strip = witness_prefix + tuple(qubit for qubit in block_contiguous if qubit not in witness_set)
    return (
        {
            "name": "four_perfect_block_contiguous",
            "template_kind": "four_tensor_block_local",
            "description": "Repeat the Phase 2 inner ring inside each of the twenty outer tiling legs.",
            "boundary_order": block_contiguous,
        },
        {
            "name": "four_perfect_inner_major",
            "template_kind": "four_tensor_inner_major",
            "description": "Group equal inner positions across all twenty outer tiling legs.",
            "boundary_order": inner_major,
        },
        {
            "name": "four_perfect_cell_major",
            "template_kind": "four_tensor_cell_major",
            "description": "Group equal inner positions inside each of the four perfect cells.",
            "boundary_order": cell_major,
        },
        {
            "name": "four_perfect_witness_strip",
            "template_kind": "source_aware_control",
            "description": "Place all lifted Phase 2 witness qubits first across the twenty tiling legs.",
            "boundary_order": witness_strip,
        },
    )


def holographic_phase17_capacity_profiles() -> tuple[tuple[int, int, int], ...]:
    return (
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (1, 3, 3),
        (3, 1, 1),
        (1, 1, 3),
        (3, 3, 1),
    )


def holographic_phase17_tree_network_spec(
    boundary_order: tuple[int, ...],
    *,
    capacities: tuple[int, int, int] = (2, 2, 2),
) -> dict[str, object]:
    if len(capacities) != 3:
        raise ValueError("Phase 17 tree network requires three bridge capacities")
    edges = list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = tuple(f"perfect_tensor_{cell}" for cell in range(4))
    for block in range(20):
        node = internal_nodes[block // 5]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="four_perfect_tensor_boundary_leg",
                )
            )
    for (left, right), capacity in zip(((0, 1), (1, 2), (1, 3)), capacities):
        edges.append(
            holographic_phase4_edge(
                internal_nodes[left],
                internal_nodes[right],
                edge_type="four_perfect_tensor_tree_bridge",
                capacity=capacity,
            )
        )
    return {
        "name": f"four_five_qubit_perfect_tensor_tree_{'_'.join(str(capacity) for capacity in capacities)}",
        "network_kind": "four_perfect_tensor_tree",
        "description": (
            "Four internal perfect-tensor cells attach to five encoded outer legs each. The bridge skeleton is the "
            "tree 0-1, 1-2, 1-3 with explicitly varied bridge capacities."
        ),
        "topology": "tree",
        "capacities": capacities,
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase17_fixed_witness_regions() -> tuple[dict[str, object], ...]:
    return (
        {
            "name": "cell0_local_compact",
            "template": "four_perfect_inner_major",
            "region_type": "phase17_cell_local_compact_witness",
            "qubits": (4, 9, 14),
            "description": "A compact bridge witness contained in perfect cell 0.",
        },
        {
            "name": "cell1_local_compact",
            "template": "four_perfect_inner_major",
            "region_type": "phase17_cell_local_compact_witness",
            "qubits": (29, 34, 39),
            "description": "A compact bridge witness contained in perfect cell 1.",
        },
        {
            "name": "cell2_local_compact",
            "template": "four_perfect_inner_major",
            "region_type": "phase17_cell_local_compact_witness",
            "qubits": (54, 59, 64),
            "description": "A compact bridge witness contained in perfect cell 2.",
        },
        {
            "name": "cell3_local_compact",
            "template": "four_perfect_inner_major",
            "region_type": "phase17_cell_local_compact_witness",
            "qubits": (79, 84, 89),
            "description": "A compact bridge witness contained in perfect cell 3.",
        },
        {
            "name": "adjacent_0_1_cross_cell",
            "template": "four_perfect_inner_major",
            "region_type": "phase17_tree_adjacent_cross_cell_witness",
            "qubits": (14, 19, 24, 29),
            "description": "A cross-cell witness spanning the tree edge from cell 0 to cell 1.",
        },
        {
            "name": "adjacent_1_2_cross_cell",
            "template": "four_perfect_inner_major",
            "region_type": "phase17_tree_adjacent_cross_cell_witness",
            "qubits": (39, 44, 49, 54),
            "description": "A cross-cell witness spanning the tree edge from cell 1 to cell 2.",
        },
        {
            "name": "branch_1_3_cross_cell",
            "template": "four_perfect_inner_major",
            "region_type": "phase17_tree_branch_cross_cell_witness",
            "qubits": (39, 44, 49, 79),
            "description": "A branch-spanning witness from the tree root cell 1 to the side leaf cell 3.",
        },
        {
            "name": "cell3_witness_strip",
            "template": "four_perfect_witness_strip",
            "region_type": "phase17_source_aware_witness_strip",
            "qubits": (89, 92, 94, 97, 99),
            "description": "A source-aware witness-strip region in the side leaf cell.",
        },
    )


def holographic_phase17_region_capacity_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region_spec: dict[str, object],
    capacities: tuple[int, int, int],
) -> dict[str, object]:
    template_by_name = {str(template["name"]): template for template in holographic_phase17_boundary_templates()}
    template = template_by_name[str(region_spec["template"])]
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase17_tree_network_spec(boundary_order, capacities=capacities)
    qubits = tuple(int(qubit) for qubit in region_spec["qubits"])  # type: ignore[index]
    region = {
        "name": region_spec["name"],
        "region_type": region_spec["region_type"],
        "template": region_spec["template"],
        "description": region_spec["description"],
        "qubits": qubits,
        "length": len(qubits),
        "outer_blocks": tuple(sorted({qubit // 5 for qubit in qubits})),
        "perfect_cells": tuple(sorted({(qubit // 5) // 5 for qubit in qubits})),
        "mask": mask_from_qubits(qubits),
    }
    hit = holographic_phase7_hit_record(
        circuit={
            "name": f"{region_spec['name']}__four_tree_{'_'.join(str(capacity) for capacity in capacities)}",
            "generator_kind": "phase17_four_cell_tree_fixed_witness",
        },
        first=first,
        second=second,
        network_spec=network_spec,
        region=region,
    )
    return {
        "region": {key: value for key, value in region.items() if key != "mask"},
        "capacity_profile": capacities,
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "topology": network_spec["topology"],
            "capacities": network_spec["capacities"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
            "internal_assignments_per_min_cut": 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
        "hit": hit,
    }


def bridge_holography_phase17_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 17 source must contain StabilizerCode objects")

    bridge_axes = ("Y", "Y", "Y")
    local_cliffords = holographic_phase17_default_local_cliffords()
    outer = holographic_phase17_four_perfect_outer_code(
        bridge_axes=bridge_axes,
        local_cliffords=local_cliffords,
    )
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    outer_summary = holographic_phase17_outer_code_summary(
        outer,
        bridge_axes=bridge_axes,
        local_cliffords=local_cliffords,
    )
    region_specs = holographic_phase17_fixed_witness_regions()
    capacity_profiles = holographic_phase17_capacity_profiles()
    records = tuple(
        holographic_phase17_region_capacity_record(
            first=first,
            second=second,
            region_spec=region_spec,
            capacities=capacities,
        )
        for region_spec in region_specs
        for capacities in capacity_profiles
    )
    records_by_region = {
        str(region_spec["name"]): tuple(record for record in records if record["region"]["name"] == region_spec["name"])
        for region_spec in region_specs
    }
    region_summaries = tuple(
        {
            "region": region_name,
            "records": len(region_records),
            "perfect_cells": region_records[0]["region"]["perfect_cells"],
            "min_cut_values": tuple(sorted({int(record["hit"]["min_cut"]["value"]) for record in region_records})),  # type: ignore[index]
            "entropy_values": tuple(
                sorted({(int(record["hit"]["first"]["entropy"]), int(record["hit"]["second"]["entropy"])) for record in region_records})  # type: ignore[index]
            ),
            "operator_or_channel_split_records": sum(
                1
                for record in region_records
                if bool(record["hit"]["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
            ),
            "exact_min_cut_records": sum(
                1 for record in region_records if bool(record["hit"]["comparisons"]["min_cut_exact"])  # type: ignore[index]
            ),
            "capacity_profiles": tuple(record["capacity_profile"] for record in region_records),
        }
        for region_name, region_records in records_by_region.items()
    )
    touched_cells = tuple(sorted({cell for summary in region_summaries for cell in summary["perfect_cells"]}))  # type: ignore[index]
    branch_summaries = tuple(summary for summary in region_summaries if len(summary["perfect_cells"]) > 1)  # type: ignore[index]
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "four_cell_tree_outer_built": outer.n == 20 and outer.k == 1 and len(outer.generators) == 19,
        "outer_distance_three_witnessed": outer_summary["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3,  # type: ignore[index]
        "four_tree_concatenation_k1_n100": first.n == second.n == 100 and first.k == second.k == 1,
        "all_labeled_t2_entropy_matches": low_order_entropy["matches"] and low_order_entropy["subsets_checked"] == 5051,
        "fixed_tree_witnesses_scored": len(region_specs) == 8
        and len(capacity_profiles) == 7
        and len(records) == 56,
        "all_mincuts_exact": all(record["hit"]["comparisons"]["min_cut_exact"] for record in records),  # type: ignore[index]
        "all_fixed_regions_keep_entropy_match": all(
            record["hit"]["comparisons"]["entropy_matches"] for record in records  # type: ignore[index]
        ),
        "all_fixed_regions_keep_operator_or_channel_split": all(
            record["hit"]["comparisons"]["operator_or_channel_visible_differs"] for record in records  # type: ignore[index]
        ),
        "all_fixed_region_mincuts_invariant_across_tree_capacities": all(
            len(summary["min_cut_values"]) == 1 for summary in region_summaries  # type: ignore[index]
        ),
        "all_four_cells_touched": touched_cells == (0, 1, 2, 3),
        "branch_spanning_witnesses_included": len(branch_summaries) >= 3,
    }
    phase_claims["goal_3_phase_17_four_cell_tree_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 17: four-perfect-cell tree fixed-witness audit",
        "status": "pass" if phase_claims["goal_3_phase_17_four_cell_tree_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "four_cell_tree_source": {
            "outer_code": outer_summary,
            "code_pair": {
                "n": first.n,
                "k": first.k,
                "first_generators": first.pauli_generators(),
                "second_generators": second.pauli_generators(),
            },
            "concatenation": {
                "first": first_metadata,
                "second": second_metadata,
            },
            "low_order_entropy": low_order_entropy,
        },
        "fixed_witness_audit": {
            "capacity_profiles": capacity_profiles,
            "fixed_witness_regions": region_specs,
            "region_summaries": region_summaries,
            "records": records,
        },
        "counts": {
            "fixed_regions_scored": len(region_specs),
            "capacity_profiles_scored": len(capacity_profiles),
            "region_capacity_records": len(records),
            "low_order_subsets_checked": low_order_entropy["subsets_checked"],
            "low_order_entropy_mismatches": low_order_entropy["mismatch_count"],
            "operator_or_channel_split_records": sum(
                1
                for record in records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "exact_min_cut_records": sum(
                1 for record in records if record["hit"]["comparisons"]["min_cut_exact"]  # type: ignore[index]
            ),
            "min_cut_invariant_regions": sum(1 for summary in region_summaries if len(summary["min_cut_values"]) == 1),  # type: ignore[index]
            "min_cut_variable_regions": sum(1 for summary in region_summaries if len(summary["min_cut_values"]) > 1),  # type: ignore[index]
            "branch_spanning_regions": len(branch_summaries),
            "touched_perfect_cells": len(touched_cells),
            "max_candidate_min_cut_internal_assignments": max(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in records
            ),
            "min_candidate_min_cut_internal_assignments": min(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in records
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A four-perfect-cell outer stabilizer tree gives an exact n=100,k=1 concatenated pair with matching "
                "labeled t<=2 entropy. Compact local, adjacent-cell, branch-spanning, and source-aware witness "
                "regions all keep the operator/erasure split across seven exact bridge-capacity profiles."
            ),
            "three_geometry_lesson": (
                "The reconstruction-visible and erasure-visible bridge witness is robust under a larger branching "
                "tensor-network substrate. But the tested witnesses remain min-cut-invariant across tree capacities, "
                "so branch structure alone still does not align capacity-sensitive geometry with observer semantics."
            ),
            "scope_warning": (
                "Phase 17 certifies fixed source-aware witnesses on one four-cell Y-bridge tree with one H repair. It "
                "does not exhaust four-cell local-Clifford variants, topology variants, or long interval searches."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The four-cell tree lift strengthens robustness but still leaves capacity-sensitive min-cut geometry "
                "decoupled from the fixed operator witness. The next phase should either run a narrower topology/long-"
                "interval funnel on this n=100 tree or modify the min-cut skeleton so the witness cannot be cut off by "
                "only boundary legs."
            ),
            "suggested_phase_18": (
                "Audit tree-only or reduced-boundary-ring min-cut skeletons, plus a bounded long-interval topology "
                "search, to test whether branch bottlenecks can become operator-visible without losing exact checks."
            ),
        },
    }


def holographic_phase18_tree_shell_regions() -> tuple[dict[str, object], ...]:
    def cell_qubits(cell: int) -> tuple[int, ...]:
        return tuple(
            qubit
            for block in range(cell * 5, (cell + 1) * 5)
            for qubit in range(block * 5, block * 5 + 5)
        )

    def shell_region(name: str, cells: tuple[int, ...], description: str) -> dict[str, object]:
        qubits = tuple(qubit for cell in cells for qubit in cell_qubits(cell))
        return {
            "name": name,
            "region_type": "phase18_four_cell_tree_shell",
            "template": "four_perfect_cell_major",
            "perfect_cells": cells,
            "qubits": qubits,
            "description": description,
        }

    return (
        shell_region("cell0_shell", (0,), "The full boundary shell of leaf cell 0."),
        shell_region("cell1_root_shell", (1,), "The full boundary shell of root cell 1."),
        shell_region("cell2_shell", (2,), "The full boundary shell of leaf cell 2."),
        shell_region("cell3_side_shell", (3,), "The full boundary shell of side leaf cell 3."),
        shell_region("root_plus_side_leaf_shell", (1, 3), "Root cell 1 together with side leaf cell 3."),
        shell_region("two_leaf_shell", (2, 3), "The two nonzero leaf cells 2 and 3."),
        shell_region("root_plus_leaf2_shell", (1, 2), "Root cell 1 together with leaf cell 2."),
        shell_region("complement_root_shell", (0, 2, 3), "All cells except the root cell 1."),
    )


def holographic_phase18_tree_shell_network_spec(
    boundary_order: tuple[int, ...],
    *,
    capacities: tuple[int, int, int],
    boundary_mode: str,
) -> dict[str, object]:
    if boundary_mode not in ("tree_only", "unit_boundary_ring"):
        raise ValueError("boundary_mode must be tree_only or unit_boundary_ring")
    if len(capacities) != 3:
        raise ValueError("Phase 18 shell network requires three bridge capacities")
    edges = [] if boundary_mode == "tree_only" else list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = tuple(f"perfect_tensor_{cell}" for cell in range(4))
    for block in range(20):
        node = internal_nodes[block // 5]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="four_perfect_tensor_boundary_leg",
                )
            )
    for (left, right), capacity in zip(((0, 1), (1, 2), (1, 3)), capacities):
        edges.append(
            holographic_phase4_edge(
                internal_nodes[left],
                internal_nodes[right],
                edge_type="four_perfect_tensor_tree_bridge",
                capacity=capacity,
            )
        )
    return {
        "name": f"four_tree_shell_{boundary_mode}_{'_'.join(str(capacity) for capacity in capacities)}",
        "network_kind": f"four_perfect_tensor_{boundary_mode}",
        "description": (
            "Four perfect-tensor cells in the Phase 17 tree. Phase 18 scores whole-cell shell regions so internal "
            "bridge capacities, rather than compact boundary spokes alone, can control the min-cut."
        ),
        "topology": "tree",
        "boundary_mode": boundary_mode,
        "capacities": capacities,
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase18_shell_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region_spec: dict[str, object],
    capacities: tuple[int, int, int],
    boundary_mode: str,
) -> dict[str, object]:
    template_by_name = {str(template["name"]): template for template in holographic_phase17_boundary_templates()}
    template = template_by_name[str(region_spec["template"])]
    boundary_order = tuple(int(qubit) for qubit in template["boundary_order"])  # type: ignore[index]
    network_spec = holographic_phase18_tree_shell_network_spec(
        boundary_order,
        capacities=capacities,
        boundary_mode=boundary_mode,
    )
    qubits = tuple(int(qubit) for qubit in region_spec["qubits"])  # type: ignore[index]
    region = {
        "name": region_spec["name"],
        "region_type": region_spec["region_type"],
        "template": region_spec["template"],
        "description": region_spec["description"],
        "qubits": qubits,
        "length": len(qubits),
        "outer_blocks": tuple(sorted({qubit // 5 for qubit in qubits})),
        "perfect_cells": tuple(int(cell) for cell in region_spec["perfect_cells"]),  # type: ignore[index]
        "mask": mask_from_qubits(qubits),
    }
    hit = holographic_phase7_hit_record(
        circuit={
            "name": f"{region_spec['name']}__{boundary_mode}__{'_'.join(str(capacity) for capacity in capacities)}",
            "generator_kind": "phase18_four_cell_tree_shell_bottleneck",
        },
        first=first,
        second=second,
        network_spec=network_spec,
        region=region,
    )
    return {
        "region": {key: value for key, value in region.items() if key != "mask"},
        "boundary_mode": boundary_mode,
        "capacity_profile": capacities,
        "network": {
            "name": network_spec["name"],
            "network_kind": network_spec["network_kind"],
            "topology": network_spec["topology"],
            "boundary_mode": network_spec["boundary_mode"],
            "capacities": network_spec["capacities"],
            "internal_nodes": network_spec["internal_nodes"],
            "edge_count": len(network_spec["edges"]),  # type: ignore[arg-type]
            "internal_assignments_per_min_cut": 2 ** len(network_spec["internal_nodes"]),  # type: ignore[arg-type]
        },
        "hit": hit,
    }


def bridge_holography_phase18_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 18 source must contain StabilizerCode objects")

    bridge_axes = ("Y", "Y", "Y")
    local_cliffords = holographic_phase17_default_local_cliffords()
    outer = holographic_phase17_four_perfect_outer_code(
        bridge_axes=bridge_axes,
        local_cliffords=local_cliffords,
    )
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    outer_distance = bounded_distance_certificate(outer, max_weight=3)
    region_specs = holographic_phase18_tree_shell_regions()
    capacity_profiles = holographic_phase17_capacity_profiles()
    boundary_modes = ("tree_only", "unit_boundary_ring")
    records = tuple(
        holographic_phase18_shell_record(
            first=first,
            second=second,
            region_spec=region_spec,
            capacities=capacities,
            boundary_mode=boundary_mode,
        )
        for boundary_mode in boundary_modes
        for region_spec in region_specs
        for capacities in capacity_profiles
    )
    records_by_mode_region = {
        (boundary_mode, str(region_spec["name"])): tuple(
            record
            for record in records
            if record["boundary_mode"] == boundary_mode and record["region"]["name"] == region_spec["name"]
        )
        for boundary_mode in boundary_modes
        for region_spec in region_specs
    }
    region_summaries = tuple(
        {
            "boundary_mode": boundary_mode,
            "region": region_name,
            "records": len(region_records),
            "perfect_cells": region_records[0]["region"]["perfect_cells"],
            "length": region_records[0]["region"]["length"],
            "min_cut_values_by_capacity": tuple(
                {
                    "capacity_profile": record["capacity_profile"],
                    "value": int(record["hit"]["min_cut"]["value"]),  # type: ignore[index]
                }
                for record in region_records
            ),
            "min_cut_values": tuple(sorted({int(record["hit"]["min_cut"]["value"]) for record in region_records})),  # type: ignore[index]
            "entropy_values": tuple(
                sorted({(int(record["hit"]["first"]["entropy"]), int(record["hit"]["second"]["entropy"])) for record in region_records})  # type: ignore[index]
            ),
            "algebra_signatures": tuple(
                sorted(
                    {
                        (
                            record["hit"]["first"]["algebra_signature"],  # type: ignore[index]
                            record["hit"]["second"]["algebra_signature"],  # type: ignore[index]
                        )
                        for record in region_records
                    }
                )
            ),
            "operator_or_channel_split_records": sum(
                1
                for record in region_records
                if bool(record["hit"]["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
            ),
            "exact_min_cut_records": sum(
                1 for record in region_records if bool(record["hit"]["comparisons"]["min_cut_exact"])  # type: ignore[index]
            ),
        }
        for (boundary_mode, region_name), region_records in records_by_mode_region.items()
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "four_cell_tree_source_rebuilt": first.n == second.n == 100 and first.k == second.k == 1,
        "outer_distance_three_witnessed": outer_distance["distance_exact_if_witness_found"] == 3,
        "shell_bottleneck_records_scored": len(region_specs) == 8
        and len(capacity_profiles) == 7
        and len(boundary_modes) == 2
        and len(records) == 112,
        "all_shell_mincuts_exact": all(record["hit"]["comparisons"]["min_cut_exact"] for record in records),  # type: ignore[index]
        "all_shell_entropies_match": all(record["hit"]["comparisons"]["entropy_matches"] for record in records),  # type: ignore[index]
        "all_shell_operator_and_channel_semantics_match": all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"] for record in records  # type: ignore[index]
        ),
        "all_shell_regions_capacity_sensitive_in_each_boundary_mode": all(
            len(summary["min_cut_values"]) > 1 for summary in region_summaries  # type: ignore[index]
        ),
        "tree_only_and_unit_ring_modes_scored": tuple(sorted({str(record["boundary_mode"]) for record in records}))
        == boundary_modes,
        "large_shell_regions_only": all(int(record["region"]["length"]) >= 25 for record in records),  # type: ignore[index]
    }
    phase_claims["goal_3_phase_18_shell_bottleneck_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 18: four-cell tree shell-bottleneck audit",
        "status": "pass" if phase_claims["goal_3_phase_18_shell_bottleneck_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "four_cell_tree_source": {
            "outer_code": {
                "parameters": {"n": outer.n, "k": outer.k},
                "distance_audit_weight3": outer_distance,
                "bridge_axes": bridge_axes,
                "local_cliffords": local_cliffords,
            },
            "code_pair": {"n": first.n, "k": first.k},
        },
        "shell_bottleneck_audit": {
            "boundary_modes": boundary_modes,
            "capacity_profiles": capacity_profiles,
            "shell_regions": region_specs,
            "region_summaries": region_summaries,
            "records": records,
        },
        "counts": {
            "boundary_modes_scored": len(boundary_modes),
            "shell_regions_scored": len(region_specs),
            "capacity_profiles_scored": len(capacity_profiles),
            "shell_capacity_records": len(records),
            "exact_min_cut_records": sum(
                1 for record in records if record["hit"]["comparisons"]["min_cut_exact"]  # type: ignore[index]
            ),
            "entropy_match_records": sum(
                1 for record in records if record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "operator_or_channel_split_records": sum(
                1
                for record in records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "capacity_sensitive_mode_region_pairs": sum(
                1 for summary in region_summaries if len(summary["min_cut_values"]) > 1  # type: ignore[index]
            ),
            "mode_region_pairs": len(region_summaries),
            "min_shell_length": min(int(record["region"]["length"]) for record in records),
            "max_shell_length": max(int(record["region"]["length"]) for record in records),
            "max_candidate_min_cut_internal_assignments": max(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in records
            ),
            "min_candidate_min_cut_internal_assignments": min(
                int(record["network"]["internal_assignments_per_min_cut"]) for record in records
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Whole-cell and branch-shell regions on the four-perfect-cell tree have matching paired-code entropy "
                "and matching observer algebra/erasure/survivor semantics, while their exact min-cut values vary with "
                "tree bridge capacities in both tree-only and unit-boundary-ring skeleton modes."
            ),
            "three_geometry_lesson": (
                "Phase 18 gives the complementary decoupling to Phase 17: branch bottlenecks can become visible to "
                "min-cut geometry without becoming visible to the operator or channel semantics of the code pair."
            ),
            "scope_warning": (
                "The audit is exact for eight large shell regions, seven capacity profiles, and two declared skeleton "
                "modes on the Phase 17 source. It is not an exhaustive interval search and does not prove all "
                "capacity-sensitive regions are operator-blind."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The tree shell audit finds capacity-sensitive min-cut geometry, but only in regions whose code "
                "semantics match. The next phase should search hybrid compact-plus-shell regions or alter the code "
                "construction so a compact bridge witness has to traverse an internal bottleneck."
            ),
            "suggested_phase_19": (
                "Run a bounded hybrid-region grammar on the n=100 tree: compact witness core plus whole-cell shells, "
                "filtered by min-cut variation first and then exact entropy/algebra/erasure diagnostics."
            ),
        },
    }


def holographic_phase19_hybrid_candidate_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    core_spec: dict[str, object],
    shell_spec: dict[str, object],
    boundary_mode: str,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int], ...],
) -> dict[str, object]:
    core_qubits = tuple(int(qubit) for qubit in core_spec["qubits"])  # type: ignore[index]
    shell_qubits = tuple(int(qubit) for qubit in shell_spec["qubits"])  # type: ignore[index]
    qubits = tuple(sorted(set(core_qubits) | set(shell_qubits)))
    region = {
        "name": f"{core_spec['name']}__plus__{shell_spec['name']}",
        "region_type": "phase19_compact_core_plus_shell",
        "template": "four_perfect_cell_major",
        "core": str(core_spec["name"]),
        "shell": str(shell_spec["name"]),
        "core_region_type": str(core_spec["region_type"]),
        "shell_region_type": str(shell_spec["region_type"]),
        "qubits": qubits,
        "length": len(qubits),
        "core_length": len(core_qubits),
        "shell_length": len(shell_qubits),
        "outer_blocks": tuple(sorted({qubit // 5 for qubit in qubits})),
        "perfect_cells": tuple(sorted({(qubit // 5) // 5 for qubit in qubits})),
        "mask": mask_from_qubits(qubits),
    }
    min_cuts = tuple(
        holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))
        for network in networks
    )
    min_cut_values = tuple(int(min_cut["value"]) for min_cut in min_cuts)
    all_mincuts_exact = all(
        int(min_cut["assignments_checked"]) == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
        for min_cut, network in zip(min_cuts, networks)
    )
    first_entropy = first.entropy(int(region["mask"]))
    second_entropy = second.entropy(int(region["mask"]))
    hit = None
    if first_entropy == second_entropy:
        hit = holographic_phase7_hit_record(
            circuit={
                "name": f"{region['name']}__{boundary_mode}",
                "generator_kind": "phase19_compact_core_plus_shell_hybrid",
            },
            first=first,
            second=second,
            network_spec=networks[0],
            region=region,
        )
    return {
        "boundary_mode": boundary_mode,
        "region": {key: value for key, value in region.items() if key != "mask"},
        "min_cut_values_by_capacity": tuple(
            {
                "capacity_profile": capacity_profile,
                "value": value,
            }
            for capacity_profile, value in zip(capacity_profiles, min_cut_values)
        ),
        "min_cut_values": tuple(sorted(set(min_cut_values))),
        "min_cut_variable": len(set(min_cut_values)) > 1,
        "all_mincuts_exact": all_mincuts_exact,
        "entropies": {"first": first_entropy, "second": second_entropy},
        "entropy_matches": first_entropy == second_entropy,
        "hit": hit,
    }


def bridge_holography_phase19_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 19 source must contain StabilizerCode objects")

    bridge_axes = ("Y", "Y", "Y")
    local_cliffords = holographic_phase17_default_local_cliffords()
    outer = holographic_phase17_four_perfect_outer_code(
        bridge_axes=bridge_axes,
        local_cliffords=local_cliffords,
    )
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    outer_distance = bounded_distance_certificate(outer, max_weight=3)
    template_by_name = {str(template["name"]): template for template in holographic_phase17_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["four_perfect_cell_major"]["boundary_order"])  # type: ignore[index]
    cores = holographic_phase17_fixed_witness_regions()
    shells = holographic_phase18_tree_shell_regions()
    capacity_profiles = holographic_phase17_capacity_profiles()
    boundary_modes = ("tree_only", "unit_boundary_ring")

    candidate_records = []
    contained_skips_by_mode = {boundary_mode: 0 for boundary_mode in boundary_modes}
    for boundary_mode in boundary_modes:
        networks = tuple(
            holographic_phase18_tree_shell_network_spec(
                boundary_order,
                capacities=capacities,
                boundary_mode=boundary_mode,
            )
            for capacities in capacity_profiles
        )
        for core in cores:
            core_qubits = set(int(qubit) for qubit in core["qubits"])  # type: ignore[index]
            for shell in shells:
                shell_qubits = set(int(qubit) for qubit in shell["qubits"])  # type: ignore[index]
                if core_qubits <= shell_qubits:
                    contained_skips_by_mode[boundary_mode] += 1
                    continue
                candidate_records.append(
                    holographic_phase19_hybrid_candidate_record(
                        first=first,
                        second=second,
                        core_spec=core,
                        shell_spec=shell,
                        boundary_mode=boundary_mode,
                        networks=networks,
                        capacity_profiles=capacity_profiles,
                    )
                )
    records = tuple(candidate_records)
    entropy_records = tuple(record for record in records if record["entropy_matches"])
    hit_records = tuple(
        record
        for record in entropy_records
        if record["hit"] is not None
        and bool(record["hit"]["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
    )
    mode_summaries = tuple(
        {
            "boundary_mode": boundary_mode,
            "core_shell_pairs": len(cores) * len(shells),
            "contained_core_shell_skips": contained_skips_by_mode[boundary_mode],
            "hybrid_candidates": sum(1 for record in records if record["boundary_mode"] == boundary_mode),
            "min_cut_variable_candidates": sum(
                1
                for record in records
                if record["boundary_mode"] == boundary_mode and bool(record["min_cut_variable"])
            ),
            "entropy_match_after_variation": sum(
                1
                for record in records
                if record["boundary_mode"] == boundary_mode
                and bool(record["min_cut_variable"])
                and bool(record["entropy_matches"])
            ),
            "entropy_mismatch_after_variation": sum(
                1
                for record in records
                if record["boundary_mode"] == boundary_mode
                and bool(record["min_cut_variable"])
                and not bool(record["entropy_matches"])
            ),
            "operator_or_channel_hits": sum(1 for record in hit_records if record["boundary_mode"] == boundary_mode),
        }
        for boundary_mode in boundary_modes
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "four_cell_tree_source_rebuilt": first.n == second.n == 100 and first.k == second.k == 1,
        "outer_distance_three_witnessed": outer_distance["distance_exact_if_witness_found"] == 3,
        "bounded_hybrid_core_shell_menu_scored": len(cores) == 8
        and len(shells) == 8
        and sum(contained_skips_by_mode.values()) == 38
        and len(records) == 90,
        "all_hybrid_mincuts_exact": all(record["all_mincuts_exact"] for record in records),
        "all_noncontained_hybrids_min_cut_variable": all(record["min_cut_variable"] for record in records),
        "entropy_candidates_after_variation_exist": len(entropy_records) == 12,
        "no_entropy_matched_hybrid_operator_or_channel_hits": len(hit_records) == 0,
        "both_boundary_modes_scored": tuple(sorted({str(record["boundary_mode"]) for record in records})) == boundary_modes,
    }
    phase_claims["goal_3_phase_19_hybrid_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 19: compact-core plus shell hybrid no-go audit",
        "status": "pass" if phase_claims["goal_3_phase_19_hybrid_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "four_cell_tree_source": {
            "outer_code": {
                "parameters": {"n": outer.n, "k": outer.k},
                "distance_audit_weight3": outer_distance,
                "bridge_axes": bridge_axes,
                "local_cliffords": local_cliffords,
            },
            "code_pair": {"n": first.n, "k": first.k},
        },
        "hybrid_search": {
            "boundary_modes": boundary_modes,
            "capacity_profiles": capacity_profiles,
            "compact_cores": cores,
            "shell_regions": shells,
            "mode_summaries": mode_summaries,
            "candidate_records": records,
            "entropy_candidate_records": entropy_records,
            "hit_records": hit_records,
            "filter_order": (
                "skip hybrids where the compact core is already contained in the shell",
                "exact min-cut variation across seven tree bridge capacity profiles",
                "exact paired-code entropy match",
                "exact operator/reconstruction or erasure/survivor split",
            ),
        },
        "counts": {
            "boundary_modes_scored": len(boundary_modes),
            "compact_cores_scored": len(cores),
            "shell_regions_scored": len(shells),
            "core_shell_pairs_per_mode": len(cores) * len(shells),
            "contained_core_shell_skips": sum(contained_skips_by_mode.values()),
            "hybrid_candidates": len(records),
            "min_cut_variable_candidates": sum(1 for record in records if record["min_cut_variable"]),
            "entropy_match_after_variation": len(entropy_records),
            "entropy_mismatch_after_variation": sum(
                1 for record in records if record["min_cut_variable"] and not record["entropy_matches"]
            ),
            "operator_or_channel_hits": len(hit_records),
            "exact_min_cut_candidate_records": sum(1 for record in records if record["all_mincuts_exact"]),
            "min_hybrid_length": min(int(record["region"]["length"]) for record in records),
            "max_hybrid_length": max(int(record["region"]["length"]) for record in records),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Every noncontained compact-core-plus-shell hybrid in the bounded menu is min-cut-variable across "
                "tree bridge capacities. Most fail the entropy gate, and the twelve entropy-matched survivors have "
                "matching operator, erasure, and survivor semantics."
            ),
            "three_geometry_lesson": (
                "Naively gluing an operator-sensitive compact witness to a min-cut-sensitive shell does not make the "
                "two notions align. In this menu, capacity-sensitive min-cut geometry either breaks entropy matching "
                "or remains operator-blind."
            ),
            "scope_warning": (
                "The audit covers Phase 17 fixed compact cores, Phase 18 shell regions, two boundary modes, and seven "
                "capacity profiles. It is not an exhaustive search over all hybrid regions or code modifications."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The hybrid grammar produces min-cut variation but no entropy-matched operator/channel hit. The next "
                "phase should change the code construction or add an internal-bottleneck bridge stabilizer whose "
                "logical support cannot be absorbed by whole-cell shells."
            ),
            "suggested_phase_20": (
                "Search small outer-tree bridge-axis/local-Clifford variants or add a dedicated internal witness "
                "bridge, then rerun the min-cut variation -> entropy -> operator/erasure funnel."
            ),
        },
    }


def holographic_phase20_axis_commutation_audit() -> dict[str, object]:
    valid = []
    rejected = []
    for axes in product(("X", "Y", "Z"), repeat=3):
        try:
            outer = holographic_phase17_four_perfect_outer_code(bridge_axes=axes)
        except ValueError as error:
            rejected.append(
                {
                    "bridge_axes": axes,
                    "reason": "noncommuting_shared_root_logical_bridge",
                    "error": str(error),
                }
            )
            continue
        valid.append(
            {
                "bridge_axes": axes,
                "parameters": {"n": outer.n, "k": outer.k},
                "generator_count": len(outer.generators),
            }
        )
    return {
        "axis_patterns_scored": 27,
        "valid_axis_patterns": tuple(valid),
        "rejected_axis_patterns": tuple(rejected),
        "valid_count": len(valid),
        "rejected_count": len(rejected),
    }


def holographic_phase20_local_repair_specs() -> tuple[dict[str, object], ...]:
    specs: list[dict[str, object]] = [
        {
            "name": "identity",
            "local_cliffords": tuple("I" for _ in range(20)),
            "operation_weight": 0,
            "description": "No local repair on the four-cell outer tree.",
        }
    ]
    for qubit in (0, 5, 10, 15):
        local = ["I"] * 20
        local[qubit] = "H"
        specs.append(
            {
                "name": f"q{qubit}_H",
                "local_cliffords": tuple(local),
                "operation_weight": 1,
                "description": f"Apply H to representative outer leg {qubit}.",
            }
        )
    for qubit in (0, 5, 10, 15):
        local = ["I"] * 20
        local[qubit] = "LC4"
        specs.append(
            {
                "name": f"q{qubit}_LC4",
                "local_cliffords": tuple(local),
                "operation_weight": 1,
                "description": f"Apply LC4 to representative outer leg {qubit}.",
            }
        )
    for left, right in ((0, 5), (5, 10), (5, 15), (10, 15)):
        local = ["I"] * 20
        local[left] = "H"
        local[right] = "H"
        specs.append(
            {
                "name": f"q{left}_q{right}_H",
                "local_cliffords": tuple(local),
                "operation_weight": 2,
                "description": f"Apply paired H repairs to outer legs {left} and {right}.",
            }
        )
    return tuple(specs)


def holographic_phase20_variant_specs() -> tuple[dict[str, object], ...]:
    specs: list[dict[str, object]] = []
    for axes in (("X", "X", "X"), ("Y", "Y", "Y"), ("Z", "Z", "Z")):
        axis_name = "".join(axes)
        for repair in holographic_phase20_local_repair_specs():
            specs.append(
                {
                    "name": f"{axis_name}_{repair['name']}",
                    "bridge_axes": axes,
                    "repair": repair,
                    "description": (
                        f"Four-cell tree with commuting {axis_name} bridge axes and {repair['name']} local repair."
                    ),
                }
            )
    return tuple(specs)


def holographic_phase20_probe_pairs() -> tuple[tuple[str, str], ...]:
    return (
        ("adjacent_0_1_cross_cell", "cell0_shell"),
        ("adjacent_0_1_cross_cell", "complement_root_shell"),
        ("adjacent_1_2_cross_cell", "cell1_root_shell"),
        ("adjacent_1_2_cross_cell", "root_plus_side_leaf_shell"),
        ("branch_1_3_cross_cell", "cell1_root_shell"),
        ("branch_1_3_cross_cell", "root_plus_leaf2_shell"),
    )


def holographic_phase20_variant_record(
    *,
    spec: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks_by_mode: dict[str, tuple[dict[str, object], ...]],
    capacity_profiles: tuple[tuple[int, int, int], ...],
    cores_by_name: dict[str, dict[str, object]],
    shells_by_name: dict[str, dict[str, object]],
) -> dict[str, object]:
    repair = spec["repair"]
    if not isinstance(repair, dict):
        raise TypeError("Phase 20 repair spec must be a dictionary")
    bridge_axes = tuple(str(axis) for axis in spec["bridge_axes"])  # type: ignore[index]
    local_cliffords = tuple(str(item) for item in repair["local_cliffords"])  # type: ignore[index]
    outer = holographic_phase17_four_perfect_outer_code(
        bridge_axes=bridge_axes,  # type: ignore[arg-type]
        local_cliffords=local_cliffords,
    )
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    outer_distance = bounded_distance_certificate(outer, max_weight=3)
    probe_records = tuple(
        holographic_phase19_hybrid_candidate_record(
            first=first,
            second=second,
            core_spec=cores_by_name[core_name],
            shell_spec=shells_by_name[shell_name],
            boundary_mode=boundary_mode,
            networks=networks,
            capacity_profiles=capacity_profiles,
        )
        for boundary_mode, networks in networks_by_mode.items()
        for core_name, shell_name in holographic_phase20_probe_pairs()
    )
    hit_records = tuple(
        record
        for record in probe_records
        if record["hit"] is not None
        and bool(record["hit"]["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
    )
    return {
        "variant": {
            "name": spec["name"],
            "bridge_axes": bridge_axes,
            "repair_name": repair["name"],
            "repair_operation_weight": repair["operation_weight"],
            "local_cliffords": local_cliffords,
            "description": spec["description"],
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": outer_distance,
        },
        "code_pair": {"n": first.n, "k": first.k},
        "probe_records": probe_records,
        "summary": {
            "probe_records": len(probe_records),
            "min_cut_variable_probe_records": sum(1 for record in probe_records if record["min_cut_variable"]),
            "exact_min_cut_probe_records": sum(1 for record in probe_records if record["all_mincuts_exact"]),
            "entropy_match_probe_records": sum(1 for record in probe_records if record["entropy_matches"]),
            "entropy_mismatch_probe_records": sum(1 for record in probe_records if not record["entropy_matches"]),
            "operator_or_channel_hits": len(hit_records),
        },
        "hit_records": hit_records,
    }


def bridge_holography_phase20_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 20 source must contain StabilizerCode objects")

    template_by_name = {str(template["name"]): template for template in holographic_phase17_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["four_perfect_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase17_capacity_profiles()
    networks_by_mode = {
        boundary_mode: tuple(
            holographic_phase18_tree_shell_network_spec(
                boundary_order,
                capacities=capacities,
                boundary_mode=boundary_mode,
            )
            for capacities in capacity_profiles
        )
        for boundary_mode in ("tree_only", "unit_boundary_ring")
    }
    cores_by_name = {str(core["name"]): core for core in holographic_phase17_fixed_witness_regions()}
    shells_by_name = {str(shell["name"]): shell for shell in holographic_phase18_tree_shell_regions()}
    axis_audit = holographic_phase20_axis_commutation_audit()
    variant_specs = holographic_phase20_variant_specs()
    variant_records = tuple(
        holographic_phase20_variant_record(
            spec=spec,
            inner_first=inner_first,
            inner_second=inner_second,
            networks_by_mode=networks_by_mode,
            capacity_profiles=capacity_profiles,
            cores_by_name=cores_by_name,
            shells_by_name=shells_by_name,
        )
        for spec in variant_specs
    )
    probe_records = tuple(record for variant in variant_records for record in variant["probe_records"])  # type: ignore[index]
    hit_records = tuple(record for variant in variant_records for record in variant["hit_records"])  # type: ignore[index]
    axis_summaries = tuple(
        {
            "bridge_axes": axes,
            "variants": sum(1 for variant in variant_records if variant["variant"]["bridge_axes"] == axes),  # type: ignore[index]
            "operator_or_channel_hits": sum(
                int(variant["summary"]["operator_or_channel_hits"])  # type: ignore[index]
                for variant in variant_records
                if variant["variant"]["bridge_axes"] == axes  # type: ignore[index]
            ),
        }
        for axes in (("X", "X", "X"), ("Y", "Y", "Y"), ("Z", "Z", "Z"))
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "axis_commutation_audit_scored": axis_audit["axis_patterns_scored"] == 27
        and axis_audit["valid_count"] == 3
        and axis_audit["rejected_count"] == 24,
        "bounded_outer_tree_variant_menu_scored": len(variant_specs) == 39 and len(variant_records) == 39,
        "all_variants_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in variant_records
        ),
        "all_variant_code_pairs_are_n100_k1": all(
            variant["code_pair"] == {"n": 100, "k": 1} for variant in variant_records
        ),
        "all_variant_probe_mincuts_exact": all(record["all_mincuts_exact"] for record in probe_records),
        "all_variant_probes_min_cut_variable": all(record["min_cut_variable"] for record in probe_records),
        "all_variant_probes_entropy_match": all(record["entropy_matches"] for record in probe_records),
        "no_variant_probe_operator_or_channel_hits": len(hit_records) == 0,
    }
    phase_claims["goal_3_phase_20_outer_variant_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 20: four-cell outer-tree local-variant no-go audit",
        "status": "pass" if phase_claims["goal_3_phase_20_outer_variant_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "axis_commutation_audit": axis_audit,
        "variant_search": {
            "variant_specs": variant_specs,
            "probe_pairs": holographic_phase20_probe_pairs(),
            "boundary_modes": tuple(networks_by_mode),
            "capacity_profiles": capacity_profiles,
            "axis_summaries": axis_summaries,
            "variant_records": variant_records,
            "hit_records": hit_records,
            "filter_order": (
                "reject noncommuting mixed bridge-axis patterns",
                "build valid outer-tree variant and concatenate with the Phase 2 inner source",
                "exact min-cut variation on Phase 19 entropy-survivor hybrid probes",
                "exact entropy match",
                "exact operator/reconstruction or erasure/survivor split",
            ),
        },
        "counts": {
            "axis_patterns_scored": axis_audit["axis_patterns_scored"],
            "commuting_axis_patterns": axis_audit["valid_count"],
            "rejected_mixed_axis_patterns": axis_audit["rejected_count"],
            "local_repair_specs_scored": len(holographic_phase20_local_repair_specs()),
            "variant_records": len(variant_records),
            "probe_pairs": len(holographic_phase20_probe_pairs()),
            "boundary_modes_scored": len(networks_by_mode),
            "variant_probe_records": len(probe_records),
            "exact_min_cut_probe_records": sum(1 for record in probe_records if record["all_mincuts_exact"]),
            "min_cut_variable_probe_records": sum(1 for record in probe_records if record["min_cut_variable"]),
            "entropy_match_probe_records": sum(1 for record in probe_records if record["entropy_matches"]),
            "entropy_mismatch_probe_records": sum(1 for record in probe_records if not record["entropy_matches"]),
            "operator_or_channel_hits": len(hit_records),
            "outer_distance_three_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded local-variant search over the four-cell outer tree rejects mixed bridge-axis patterns as "
                "noncommuting and scores all valid uniform-axis variants with representative local repairs. Every "
                "sentinel hybrid probe remains min-cut-variable and entropy-matched, but no probe becomes "
                "operator/channel visible."
            ),
            "three_geometry_lesson": (
                "The Phase 19 no-go is stable under this small outer-tree bridge-axis/local-Clifford menu. Local "
                "basis changes and uniform X/Y/Z bridge-axis choices do not align the min-cut bottleneck with the "
                "observer algebra."
            ),
            "scope_warning": (
                "The audit covers uniform bridge axes, thirteen local repair specs, and the Phase 19 entropy-survivor "
                "sentinel probes. It is not a full local-Clifford orbit, and it does not add a new internal witness "
                "bridge stabilizer."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Uniform-axis/local-repair variants do not produce a capacity-sensitive operator hit. The next phase "
                "should add a genuinely new internal witness bridge or search a different outer-tree topology/code "
                "rather than only changing local basis choices."
            ),
            "suggested_phase_21": (
                "Construct a dedicated internal witness-bridge outer code or a different branching stabilizer block, "
                "then rerun the exact min-cut variation -> entropy -> operator/erasure funnel."
            ),
        },
    }


def holographic_phase21_labeled_tree_edges() -> tuple[tuple[tuple[int, int], ...], ...]:
    all_edges = tuple(combinations(range(4), 2))

    def connected(edges: tuple[tuple[int, int], ...]) -> bool:
        seen = {0}
        changed = True
        while changed:
            changed = False
            for left, right in edges:
                if left in seen and right not in seen:
                    seen.add(right)
                    changed = True
                if right in seen and left not in seen:
                    seen.add(left)
                    changed = True
        return len(seen) == 4

    return tuple(
        tuple(sorted(edges))
        for edges in combinations(all_edges, 3)
        if connected(tuple(edges))
    )


def holographic_phase21_tree_name(tree_edges: tuple[tuple[int, int], ...]) -> str:
    return "tree_" + "_".join(f"{left}{right}" for left, right in tree_edges)


def holographic_phase21_four_perfect_outer_code(
    *,
    tree_edges: tuple[tuple[int, int], ...],
    bridge_axis: str = "Y",
    local_cliffords: tuple[str, ...] | None = None,
) -> StabilizerCode:
    if len(tree_edges) != 3:
        raise ValueError("Phase 21 four-cell topology audit requires three tree edges")
    if bridge_axis not in ("Z", "X", "Y"):
        raise ValueError("bridge_axis must be Z, X, or Y")
    if tuple(sorted(tree_edges)) not in holographic_phase21_labeled_tree_edges():
        raise ValueError("tree_edges must be one of the sixteen labeled four-cell trees")
    base = holographic_phase10_five_qubit_perfect_code()
    rows: list[int] = []
    for block in range(4):
        for generator in base.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=5, block_count=4))
    logical_z, logical_x = base.logical_basis
    bridge_logical = {
        "Z": logical_z,
        "X": logical_x,
        "Y": logical_z ^ logical_x,
    }[bridge_axis]
    for left, right in tuple(sorted(tree_edges)):
        rows.append(
            block_shift_pauli(bridge_logical, block=left, block_size=5, block_count=4)
            ^ block_shift_pauli(bridge_logical, block=right, block_size=5, block_count=4)
        )
    code = StabilizerCode(20, rows)
    if local_cliffords is None:
        return code
    if len(local_cliffords) != code.n:
        raise ValueError("local_cliffords must have length twenty for the Phase 21 outer tree")
    named_maps = holographic_phase11_local_clifford_maps()
    maps = tuple(named_maps[name] for name in local_cliffords)
    return StabilizerCode(code.n, (local_clifford_pauli(row, code.n, maps) for row in code.generators))


def holographic_phase21_tree_network_spec(
    boundary_order: tuple[int, ...],
    *,
    tree_edges: tuple[tuple[int, int], ...],
    capacities: tuple[int, int, int],
    boundary_mode: str,
) -> dict[str, object]:
    if boundary_mode not in ("tree_only", "unit_boundary_ring"):
        raise ValueError("boundary_mode must be tree_only or unit_boundary_ring")
    if len(capacities) != 3:
        raise ValueError("Phase 21 topology network requires three bridge capacities")
    tree_edges = tuple(sorted(tree_edges))
    if tree_edges not in holographic_phase21_labeled_tree_edges():
        raise ValueError("tree_edges must be a labeled four-cell tree")
    edges = [] if boundary_mode == "tree_only" else list(holographic_phase4_boundary_ring_edges(boundary_order))
    internal_nodes = tuple(f"perfect_tensor_{cell}" for cell in range(4))
    for block in range(20):
        node = internal_nodes[block // 5]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="four_perfect_tensor_boundary_leg",
                )
            )
    for (left, right), capacity in zip(tree_edges, capacities):
        edges.append(
            holographic_phase4_edge(
                internal_nodes[left],
                internal_nodes[right],
                edge_type="four_perfect_tensor_topology_bridge",
                capacity=capacity,
            )
        )
    return {
        "name": f"{holographic_phase21_tree_name(tree_edges)}_{boundary_mode}_{'_'.join(str(c) for c in capacities)}",
        "network_kind": f"four_perfect_tensor_topology_{boundary_mode}",
        "description": "Four-cell topology-specific tree skeleton for Phase 21 sentinel hybrid probes.",
        "topology": "labeled_tree",
        "tree_edges": tree_edges,
        "boundary_mode": boundary_mode,
        "capacities": capacities,
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase21_topology_record(
    *,
    tree_edges: tuple[tuple[int, int], ...],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    boundary_order: tuple[int, ...],
    capacity_profiles: tuple[tuple[int, int, int], ...],
    cores_by_name: dict[str, dict[str, object]],
    shells_by_name: dict[str, dict[str, object]],
) -> dict[str, object]:
    local_cliffords = holographic_phase17_default_local_cliffords()
    outer = holographic_phase21_four_perfect_outer_code(
        tree_edges=tree_edges,
        bridge_axis="Y",
        local_cliffords=local_cliffords,
    )
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    outer_distance = bounded_distance_certificate(outer, max_weight=3)
    networks_by_mode = {
        boundary_mode: tuple(
            holographic_phase21_tree_network_spec(
                boundary_order,
                tree_edges=tree_edges,
                capacities=capacities,
                boundary_mode=boundary_mode,
            )
            for capacities in capacity_profiles
        )
        for boundary_mode in ("tree_only", "unit_boundary_ring")
    }
    probe_records = tuple(
        holographic_phase19_hybrid_candidate_record(
            first=first,
            second=second,
            core_spec=cores_by_name[core_name],
            shell_spec=shells_by_name[shell_name],
            boundary_mode=boundary_mode,
            networks=networks,
            capacity_profiles=capacity_profiles,
        )
        for boundary_mode, networks in networks_by_mode.items()
        for core_name, shell_name in holographic_phase20_probe_pairs()
    )
    hit_records = tuple(
        record
        for record in probe_records
        if record["hit"] is not None
        and bool(record["hit"]["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
    )
    return {
        "topology": {
            "name": holographic_phase21_tree_name(tree_edges),
            "tree_edges": tree_edges,
            "bridge_axis": "Y",
            "local_repair": "q0_H",
            "local_cliffords": local_cliffords,
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": outer_distance,
        },
        "code_pair": {"n": first.n, "k": first.k},
        "probe_records": probe_records,
        "summary": {
            "probe_records": len(probe_records),
            "min_cut_variable_probe_records": sum(1 for record in probe_records if record["min_cut_variable"]),
            "exact_min_cut_probe_records": sum(1 for record in probe_records if record["all_mincuts_exact"]),
            "entropy_match_probe_records": sum(1 for record in probe_records if record["entropy_matches"]),
            "entropy_mismatch_probe_records": sum(1 for record in probe_records if not record["entropy_matches"]),
            "operator_or_channel_hits": len(hit_records),
        },
        "hit_records": hit_records,
    }


def bridge_holography_phase21_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 21 source must contain StabilizerCode objects")

    template_by_name = {str(template["name"]): template for template in holographic_phase17_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["four_perfect_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase17_capacity_profiles()
    cores_by_name = {str(core["name"]): core for core in holographic_phase17_fixed_witness_regions()}
    shells_by_name = {str(shell["name"]): shell for shell in holographic_phase18_tree_shell_regions()}
    tree_edges = holographic_phase21_labeled_tree_edges()
    topology_records = tuple(
        holographic_phase21_topology_record(
            tree_edges=tree,
            inner_first=inner_first,
            inner_second=inner_second,
            boundary_order=boundary_order,
            capacity_profiles=capacity_profiles,
            cores_by_name=cores_by_name,
            shells_by_name=shells_by_name,
        )
        for tree in tree_edges
    )
    probe_records = tuple(record for topology in topology_records for record in topology["probe_records"])  # type: ignore[index]
    hit_records = tuple(record for topology in topology_records for record in topology["hit_records"])  # type: ignore[index]
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "all_labeled_four_cell_trees_scored": len(tree_edges) == 16 and len(topology_records) == 16,
        "all_topology_outer_codes_distance_three_witnessed": all(
            record["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for record in topology_records
        ),
        "all_topology_code_pairs_are_n100_k1": all(
            record["code_pair"] == {"n": 100, "k": 1} for record in topology_records
        ),
        "all_topology_probe_mincuts_exact": all(record["all_mincuts_exact"] for record in probe_records),
        "all_topology_probes_min_cut_variable": all(record["min_cut_variable"] for record in probe_records),
        "all_topology_probes_entropy_match": all(record["entropy_matches"] for record in probe_records),
        "no_topology_probe_operator_or_channel_hits": len(hit_records) == 0,
    }
    phase_claims["goal_3_phase_21_outer_tree_topology_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 21: four-cell outer-tree topology no-go audit",
        "status": "pass" if phase_claims["goal_3_phase_21_outer_tree_topology_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "topology_search": {
            "tree_edges": tree_edges,
            "bridge_axis": "Y",
            "local_repair": "q0_H",
            "probe_pairs": holographic_phase20_probe_pairs(),
            "boundary_modes": ("tree_only", "unit_boundary_ring"),
            "capacity_profiles": capacity_profiles,
            "topology_records": topology_records,
            "hit_records": hit_records,
            "filter_order": (
                "enumerate all labeled four-cell tree topologies",
                "build Y-bridge outer tree with the Phase 17 q0_H repair",
                "exact min-cut variation on Phase 20 sentinel hybrid probes using the matching tree skeleton",
                "exact entropy match",
                "exact operator/reconstruction or erasure/survivor split",
            ),
        },
        "counts": {
            "labeled_tree_topologies": len(tree_edges),
            "topology_records": len(topology_records),
            "probe_pairs": len(holographic_phase20_probe_pairs()),
            "boundary_modes_scored": 2,
            "topology_probe_records": len(probe_records),
            "exact_min_cut_probe_records": sum(1 for record in probe_records if record["all_mincuts_exact"]),
            "min_cut_variable_probe_records": sum(1 for record in probe_records if record["min_cut_variable"]),
            "entropy_match_probe_records": sum(1 for record in probe_records if record["entropy_matches"]),
            "entropy_mismatch_probe_records": sum(1 for record in probe_records if not record["entropy_matches"]),
            "operator_or_channel_hits": len(hit_records),
            "outer_distance_three_topologies": sum(
                1
                for record in topology_records
                if record["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "All sixteen labeled four-cell outer-tree topologies preserve the Phase 20 sentinel no-go: every "
                "topology-specific probe is exact, min-cut-variable, and entropy-matched, but none is operator/channel "
                "visible."
            ),
            "three_geometry_lesson": (
                "Changing the outer tree connectivity and matching the declared min-cut skeleton to that topology "
                "still does not align bottleneck geometry with observer algebra for the sentinel hybrid probes."
            ),
            "scope_warning": (
                "The audit fixes the Y bridge axis and q0_H repair, and it uses the Phase 20 sentinel probes. It does "
                "not search all local-Clifford variants for every topology or introduce a new internal witness bridge."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Topology changes alone do not rescue the sentinel hybrid probes. The next phase should modify the "
                "logical construction more substantially, for example by adding an explicit internal witness bridge "
                "or moving to a larger/different stabilizer block."
            ),
            "suggested_phase_22": (
                "Construct a new internal-witness outer block or a five-cell branching code, then rerun exact min-cut, "
                "entropy, algebra, erasure, survivor, and distance diagnostics."
            ),
        },
    }


def holographic_phase22_tree_edges() -> tuple[tuple[int, int], ...]:
    return ((0, 1), (1, 2), (1, 3), (3, 4))


def holographic_phase22_five_perfect_outer_code(*, bridge_axis: str = "Y") -> StabilizerCode:
    if bridge_axis not in ("Z", "X", "Y"):
        raise ValueError("bridge_axis must be Z, X, or Y")
    base = holographic_phase10_five_qubit_perfect_code()
    rows: list[int] = []
    for block in range(5):
        for generator in base.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=5, block_count=5))
    logical_z, logical_x = base.logical_basis
    bridge_logical = {
        "Z": logical_z,
        "X": logical_x,
        "Y": logical_z ^ logical_x,
    }[bridge_axis]
    for left, right in holographic_phase22_tree_edges():
        rows.append(
            block_shift_pauli(bridge_logical, block=left, block_size=5, block_count=5)
            ^ block_shift_pauli(bridge_logical, block=right, block_size=5, block_count=5)
        )
    return StabilizerCode(25, rows)


def holographic_phase22_outer_code_summary(outer: StabilizerCode, *, bridge_axis: str) -> dict[str, object]:
    distance_audit = bounded_distance_certificate(outer, max_weight=3)
    return {
        "name": "five_five_qubit_perfect_blocks_binary_tree",
        "construction": (
            "Five copies of the canonical [[5,1,3]] outer block joined by four encoded logical bridge stabilizers "
            "on the binary-tree edges 0-1, 1-2, 1-3, and 3-4, leaving one outer logical qubit."
        ),
        "tree_edges": holographic_phase22_tree_edges(),
        "bridge_axis": bridge_axis,
        "parameters": {"n": outer.n, "k": outer.k},
        "generators": outer.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
        "distance_audit_weight3": distance_audit,
        "erasure_threshold": outer.erasure_threshold(),
        "cell_code": holographic_phase10_outer_code_summary(holographic_phase10_five_qubit_perfect_code()),
        "five_cell_checks": {
            "five_literal_perfect_cells": True,
            "four_binary_tree_bridge_stabilizers": True,
            "outer_k1": outer.k == 1,
            "outer_distance_three_witnessed": distance_audit["distance_exact_if_witness_found"] == 3,
        },
    }


def holographic_phase22_boundary_templates() -> tuple[dict[str, object], ...]:
    inner_order = (0, 1, 2, 4, 3)
    block_size = 5
    block_count = 25
    block_contiguous = tuple(block * block_size + qubit for block in range(block_count) for qubit in inner_order)
    inner_major = tuple(block * block_size + qubit for qubit in inner_order for block in range(block_count))
    cell_major = tuple(
        block * block_size + qubit
        for cell in range(5)
        for qubit in inner_order
        for block in range(cell * 5, (cell + 1) * 5)
    )
    return (
        {
            "name": "five_perfect_block_contiguous",
            "template_kind": "five_tensor_block_local",
            "description": "Repeat the Phase 2 inner ring inside each of the twenty-five outer tiling legs.",
            "boundary_order": block_contiguous,
        },
        {
            "name": "five_perfect_inner_major",
            "template_kind": "five_tensor_inner_major",
            "description": "Group equal inner positions across all twenty-five outer tiling legs.",
            "boundary_order": inner_major,
        },
        {
            "name": "five_perfect_cell_major",
            "template_kind": "five_tensor_cell_major",
            "description": "Group equal inner positions inside each of the five perfect cells.",
            "boundary_order": cell_major,
        },
    )


def holographic_phase22_capacity_profiles() -> tuple[tuple[int, int, int, int], ...]:
    return (
        (1, 1, 1, 1),
        (2, 2, 2, 2),
        (3, 3, 3, 3),
        (1, 3, 3, 3),
        (3, 1, 1, 1),
        (1, 1, 3, 1),
        (1, 1, 1, 3),
        (3, 3, 1, 1),
        (1, 3, 1, 3),
    )


def holographic_phase22_tree_network_spec(
    boundary_order: tuple[int, ...],
    *,
    capacities: tuple[int, int, int, int],
) -> dict[str, object]:
    if len(capacities) != 4:
        raise ValueError("Phase 22 five-cell tree requires four bridge capacities")
    edges: list[dict[str, object]] = []
    internal_nodes = tuple(f"perfect_tensor_{cell}" for cell in range(5))
    for block in range(25):
        node = internal_nodes[block // 5]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="five_perfect_tensor_boundary_leg",
                )
            )
    for (left, right), capacity in zip(holographic_phase22_tree_edges(), capacities):
        edges.append(
            holographic_phase4_edge(
                internal_nodes[left],
                internal_nodes[right],
                edge_type="five_perfect_tensor_binary_tree_bridge",
                capacity=capacity,
            )
        )
    return {
        "name": f"five_perfect_binary_tree_{'_'.join(str(capacity) for capacity in capacities)}",
        "network_kind": "five_perfect_tensor_tree_only",
        "description": (
            "Five internal perfect-tensor cells attach to five encoded outer legs each. Phase 22 removes the boundary "
            "ring so binary-tree bridge capacities are the only internal bottleneck variables."
        ),
        "topology": "binary_tree",
        "boundary_mode": "tree_only",
        "tree_edges": holographic_phase22_tree_edges(),
        "capacities": capacities,
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase22_cell_qubits(cell: int) -> tuple[int, ...]:
    if cell < 0 or cell >= 5:
        raise ValueError("Phase 22 cell index must be in 0..4")
    return tuple(
        qubit
        for block in range(cell * 5, (cell + 1) * 5)
        for qubit in range(block * 5, block * 5 + 5)
    )


def holographic_phase22_compact_witness_regions() -> tuple[dict[str, object], ...]:
    regions: list[dict[str, object]] = []
    for cell in range(5):
        qubits = tuple(cell * 25 + offset for offset in (4, 9, 14))
        regions.append(
            {
                "name": f"cell{cell}_local_compact",
                "region_type": "phase22_five_cell_local_compact_witness",
                "template": "five_perfect_inner_major",
                "core_kind": "cell_local",
                "perfect_cells": (cell,),
                "qubits": qubits,
                "description": f"A compact source-aware witness contained in perfect cell {cell}.",
            }
        )
    for left, right in holographic_phase22_tree_edges():
        qubits = (left * 25 + 14, left * 25 + 19, left * 25 + 24, right * 25 + 4)
        regions.append(
            {
                "name": f"edge_{left}_{right}_cross_cell",
                "region_type": "phase22_five_cell_edge_compact_witness",
                "template": "five_perfect_inner_major",
                "core_kind": "tree_edge_cross_cell",
                "perfect_cells": (left, right),
                "tree_edge": (left, right),
                "qubits": qubits,
                "description": f"A compact source-aware witness crossing the five-cell tree edge {left}-{right}.",
            }
        )
    return tuple(regions)


def holographic_phase22_shell_regions() -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "name": f"cell{cell}_shell",
            "region_type": "phase22_five_cell_shell",
            "template": "five_perfect_cell_major",
            "perfect_cells": (cell,),
            "qubits": holographic_phase22_cell_qubits(cell),
            "description": f"The full boundary shell of perfect cell {cell}.",
        }
        for cell in range(5)
    )


def holographic_phase22_region_payload(region_spec: dict[str, object]) -> dict[str, object]:
    qubits = tuple(int(qubit) for qubit in region_spec["qubits"])  # type: ignore[index]
    return {
        "name": region_spec["name"],
        "region_type": region_spec["region_type"],
        "template": region_spec["template"],
        "description": region_spec["description"],
        "qubits": qubits,
        "length": len(qubits),
        "outer_blocks": tuple(sorted({qubit // 5 for qubit in qubits})),
        "perfect_cells": tuple(int(cell) for cell in region_spec["perfect_cells"]),  # type: ignore[index]
        "mask": mask_from_qubits(qubits),
    }


def holographic_phase22_mincut_values(
    *,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int], ...],
    region_mask: int,
) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "capacity_profile": capacities,
            "value": int(holographic_network_min_cut(network_spec=network, region_mask=region_mask)["value"]),
        }
        for capacities, network in zip(capacity_profiles, networks)
    )


def holographic_phase22_semantic_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region_spec: dict[str, object],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int], ...],
    generator_kind: str,
) -> dict[str, object]:
    region = holographic_phase22_region_payload(region_spec)
    min_cut_values = holographic_phase22_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=int(region["mask"]),
    )
    hit = holographic_phase7_hit_record(
        circuit={
            "name": str(region["name"]),
            "generator_kind": generator_kind,
        },
        first=first,
        second=second,
        network_spec=networks[0],
        region=region,
    )
    return {
        "region": {key: value for key, value in region.items() if key != "mask"},
        "min_cut_values_by_capacity": min_cut_values,
        "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
        "min_cut_variable": len({int(record["value"]) for record in min_cut_values}) > 1,
        "all_mincuts_exact": all(
            int(holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))["assignments_checked"])
            == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
            for network in networks
        ),
        "hit": hit,
    }


def holographic_phase22_core_shell_candidate_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    core_spec: dict[str, object],
    shell_cells: tuple[int, ...],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int], ...],
) -> dict[str, object]:
    core_qubits = tuple(int(qubit) for qubit in core_spec["qubits"])  # type: ignore[index]
    shell_qubits = tuple(qubit for cell in shell_cells for qubit in holographic_phase22_cell_qubits(cell))
    qubits = tuple(sorted(set(core_qubits) | set(shell_qubits)))
    mask = mask_from_qubits(qubits)
    min_cut_values = holographic_phase22_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=mask,
    )
    first_entropy = first.entropy(mask)
    second_entropy = second.entropy(mask)
    min_cut_variable = len({int(record["value"]) for record in min_cut_values}) > 1
    hit = None
    if first_entropy == second_entropy and min_cut_variable:
        hit = holographic_phase7_hit_record(
            circuit={
                "name": f"{core_spec['name']}__plus_shells_{'_'.join(str(cell) for cell in shell_cells)}",
                "generator_kind": "phase22_five_cell_core_shell_survivor",
            },
            first=first,
            second=second,
            network_spec=networks[0],
            region={
                "name": f"{core_spec['name']}__plus_shells_{'_'.join(str(cell) for cell in shell_cells)}",
                "region_type": "phase22_compact_core_plus_shells",
                "qubits": qubits,
                "mask": mask,
            },
        )
    return {
        "core": str(core_spec["name"]),
        "core_kind": str(core_spec["core_kind"]),
        "shell_cells": shell_cells,
        "qubits": qubits,
        "length": len(qubits),
        "perfect_cells": tuple(sorted({(qubit // 5) // 5 for qubit in qubits})),
        "min_cut_values_by_capacity": min_cut_values,
        "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
        "min_cut_variable": min_cut_variable,
        "entropies": {"first": first_entropy, "second": second_entropy},
        "entropy_matches": first_entropy == second_entropy,
        "hit": hit,
    }


def bridge_holography_phase22_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 22 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    outer = holographic_phase22_five_perfect_outer_code(bridge_axis=bridge_axis)
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    outer_summary = holographic_phase22_outer_code_summary(outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase22_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["five_perfect_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase22_capacity_profiles()
    networks = tuple(
        holographic_phase22_tree_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    compact_regions = holographic_phase22_compact_witness_regions()
    shell_regions = holographic_phase22_shell_regions()
    compact_records = tuple(
        holographic_phase22_semantic_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
            generator_kind="phase22_five_cell_compact_witness",
        )
        for region in compact_regions
    )
    shell_records = tuple(
        holographic_phase22_semantic_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
            generator_kind="phase22_five_cell_shell_bottleneck",
        )
        for region in shell_regions
    )
    core_shell_candidates = tuple(
        holographic_phase22_core_shell_candidate_record(
            first=first,
            second=second,
            core_spec=core,
            shell_cells=shell_cells,
            networks=networks,
            capacity_profiles=capacity_profiles,
        )
        for core in compact_regions
        for shell_size in (1, 2, 3)
        for shell_cells in combinations(range(5), shell_size)
    )
    entropy_variable_candidates = tuple(
        record for record in core_shell_candidates if record["entropy_matches"] and record["min_cut_variable"]
    )
    core_shell_hit_records = tuple(
        record
        for record in entropy_variable_candidates
        if record["hit"] is not None
        and bool(record["hit"]["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
    )
    compact_summaries = tuple(
        {
            "region": record["region"]["name"],
            "length": record["region"]["length"],
            "perfect_cells": record["region"]["perfect_cells"],
            "min_cut_values": record["min_cut_values"],
            "entropy_pair": (record["hit"]["first"]["entropy"], record["hit"]["second"]["entropy"]),  # type: ignore[index]
            "algebra_pair": (
                record["hit"]["first"]["algebra_signature"],  # type: ignore[index]
                record["hit"]["second"]["algebra_signature"],  # type: ignore[index]
            ),
            "operator_or_channel_split": record["hit"]["comparisons"]["operator_or_channel_visible_differs"],  # type: ignore[index]
        }
        for record in compact_records
    )
    shell_summaries = tuple(
        {
            "region": record["region"]["name"],
            "length": record["region"]["length"],
            "min_cut_values": record["min_cut_values"],
            "entropy_pair": (record["hit"]["first"]["entropy"], record["hit"]["second"]["entropy"]),  # type: ignore[index]
            "algebra_pair": (
                record["hit"]["first"]["algebra_signature"],  # type: ignore[index]
                record["hit"]["second"]["algebra_signature"],  # type: ignore[index]
            ),
            "operator_or_channel_split": record["hit"]["comparisons"]["operator_or_channel_visible_differs"],  # type: ignore[index]
        }
        for record in shell_records
    )
    all_semantic_records = compact_records + shell_records
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "five_cell_outer_built": outer.n == 25 and outer.k == 1 and len(outer.generators) == 24,
        "outer_distance_three_witnessed": outer_summary["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3,  # type: ignore[index]
        "five_cell_concatenation_k1_n125": first.n == second.n == 125 and first.k == second.k == 1,
        "all_labeled_t2_entropy_matches": low_order_entropy["matches"]
        and low_order_entropy["subsets_checked"] == 7876,
        "compact_witnesses_keep_operator_or_channel_split": len(compact_records) == 9
        and all(record["hit"]["comparisons"]["operator_or_channel_visible_differs"] for record in compact_records),  # type: ignore[index]
        "compact_witness_mincuts_invariant": all(not record["min_cut_variable"] for record in compact_records),
        "shell_bottlenecks_are_capacity_sensitive": len(shell_records) == 5
        and all(record["min_cut_variable"] for record in shell_records),
        "shell_bottlenecks_keep_semantics_matched": all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"] for record in shell_records  # type: ignore[index]
        ),
        "core_shell_family_exhausted": len(core_shell_candidates) == 225,
        "core_shell_entropy_variable_survivors_scored": len(entropy_variable_candidates) == 99
        and all(record["hit"] is not None for record in entropy_variable_candidates),
        "no_core_shell_entropy_variable_operator_or_channel_hits": len(core_shell_hit_records) == 0,
        "all_reported_mincuts_exact": all(record["all_mincuts_exact"] for record in all_semantic_records),
    }
    phase_claims["goal_3_phase_22_five_cell_branching_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 22: five-cell branching internal-witness audit",
        "status": "pass" if phase_claims["goal_3_phase_22_five_cell_branching_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "five_cell_source": {
            "outer_code": outer_summary,
            "code_pair": {
                "n": first.n,
                "k": first.k,
                "first_generators": first.pauli_generators(),
                "second_generators": second.pauli_generators(),
            },
            "concatenation": {
                "first": first_metadata,
                "second": second_metadata,
            },
            "low_order_entropy": low_order_entropy,
        },
        "branching_audit": {
            "boundary_mode": "tree_only",
            "capacity_profiles": capacity_profiles,
            "compact_witness_regions": compact_regions,
            "shell_regions": shell_regions,
            "compact_summaries": compact_summaries,
            "shell_summaries": shell_summaries,
            "compact_records": compact_records,
            "shell_records": shell_records,
            "core_shell_search": {
                "shell_subset_sizes": (1, 2, 3),
                "candidates_scanned": len(core_shell_candidates),
                "entropy_variable_candidate_records": entropy_variable_candidates,
                "hit_records": core_shell_hit_records,
                "filter_order": (
                    "compact source-aware core plus one-, two-, or three-cell whole shells",
                    "exact entropy match",
                    "exact min-cut variation across nine binary-tree capacity profiles",
                    "exact operator/reconstruction or erasure/survivor split",
                ),
            },
        },
        "counts": {
            "compact_witness_regions": len(compact_records),
            "shell_regions": len(shell_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "compact_operator_or_channel_split_records": sum(
                1
                for record in compact_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "compact_min_cut_variable_records": sum(1 for record in compact_records if record["min_cut_variable"]),
            "shell_operator_or_channel_split_records": sum(
                1
                for record in shell_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "shell_min_cut_variable_records": sum(1 for record in shell_records if record["min_cut_variable"]),
            "core_shell_candidates_scanned": len(core_shell_candidates),
            "core_shell_entropy_matches": sum(1 for record in core_shell_candidates if record["entropy_matches"]),
            "core_shell_min_cut_variable_candidates": sum(1 for record in core_shell_candidates if record["min_cut_variable"]),
            "core_shell_entropy_variable_candidates": len(entropy_variable_candidates),
            "core_shell_operator_or_channel_hits": len(core_shell_hit_records),
            "low_order_subsets_checked": low_order_entropy["subsets_checked"],
            "low_order_entropy_mismatches": low_order_entropy["mismatch_count"],
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A five-perfect-cell binary-tree outer code gives an exact n=125,k=1 concatenated pair with matching "
                "labeled t<=2 entropy. Compact source-aware witnesses retain the operator/erasure split but remain "
                "min-cut-invariant; whole-cell shells are capacity-sensitive but operator/channel-matched; and all "
                "99 entropy-matched, capacity-sensitive compact-core-plus-shell survivors are operator/channel-matched."
            ),
            "three_geometry_lesson": (
                "Increasing the branching code itself separates the three geometries even more sharply: reconstruction "
                "visibility lives in compact source-aware witnesses, while capacity-sensitive min-cut geometry lives in "
                "coarse shells. Unioning them makes the min-cut signal visible but erases the operator/channel split."
            ),
            "scope_warning": (
                "The audit fixes one five-cell Y-bridge binary tree, tree-only min-cut skeletons, nine bridge-capacity "
                "profiles, compact cores, and shell subsets of size one to three. It is not an exhaustive search over "
                "all five-cell local-Clifford variants, topologies, or arbitrary boundary regions."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The five-cell code change did not produce an overlap between capacity-sensitive min-cut geometry and "
                "operator/channel-visible geometry. The next attempt should introduce an explicit gauge/interface cell "
                "or a different outer block where a compact logical witness has support on an internal bottleneck by "
                "construction, rather than adding whole-cell shells after the fact."
            ),
            "suggested_phase_23": (
                "Search a small interface-cell or two-layer Clifford/MERA-like outer code, then rerun exact entropy, "
                "min-cut, region algebra, erasure, survivor, and distance diagnostics."
            ),
        },
    }


def holographic_phase23_interface_edges() -> tuple[tuple[int, int], ...]:
    return tuple((5, leaf) for leaf in range(5))


def holographic_phase23_interface_outer_code(*, bridge_axis: str = "Y") -> StabilizerCode:
    if bridge_axis not in ("Z", "X", "Y"):
        raise ValueError("bridge_axis must be Z, X, or Y")
    base = holographic_phase10_five_qubit_perfect_code()
    rows: list[int] = []
    for block in range(6):
        for generator in base.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=5, block_count=6))
    logical_z, logical_x = base.logical_basis
    bridge_logical = {
        "Z": logical_z,
        "X": logical_x,
        "Y": logical_z ^ logical_x,
    }[bridge_axis]
    for root, leaf in holographic_phase23_interface_edges():
        rows.append(
            block_shift_pauli(bridge_logical, block=root, block_size=5, block_count=6)
            ^ block_shift_pauli(bridge_logical, block=leaf, block_size=5, block_count=6)
        )
    return StabilizerCode(30, rows)


def holographic_phase23_outer_code_summary(outer: StabilizerCode, *, bridge_axis: str) -> dict[str, object]:
    distance_audit = bounded_distance_certificate(outer, max_weight=3)
    return {
        "name": "six_five_qubit_perfect_blocks_interface_star",
        "construction": (
            "Six copies of the canonical [[5,1,3]] outer block joined by five encoded logical bridge stabilizers "
            "from a dedicated interface/root cell 5 to leaf cells 0..4, leaving one outer logical qubit."
        ),
        "tree_edges": holographic_phase23_interface_edges(),
        "interface_cell": 5,
        "leaf_cells": tuple(range(5)),
        "bridge_axis": bridge_axis,
        "parameters": {"n": outer.n, "k": outer.k},
        "generators": outer.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
        "distance_audit_weight3": distance_audit,
        "erasure_threshold": outer.erasure_threshold(),
        "cell_code": holographic_phase10_outer_code_summary(holographic_phase10_five_qubit_perfect_code()),
        "interface_checks": {
            "six_literal_perfect_cells": True,
            "five_interface_bridge_stabilizers": True,
            "outer_k1": outer.k == 1,
            "outer_distance_three_witnessed": distance_audit["distance_exact_if_witness_found"] == 3,
        },
    }


def holographic_phase23_boundary_templates() -> tuple[dict[str, object], ...]:
    inner_order = (0, 1, 2, 4, 3)
    block_size = 5
    block_count = 30
    block_contiguous = tuple(block * block_size + qubit for block in range(block_count) for qubit in inner_order)
    inner_major = tuple(block * block_size + qubit for qubit in inner_order for block in range(block_count))
    cell_major = tuple(
        block * block_size + qubit
        for cell in range(6)
        for qubit in inner_order
        for block in range(cell * 5, (cell + 1) * 5)
    )
    return (
        {
            "name": "interface_star_block_contiguous",
            "template_kind": "six_tensor_block_local",
            "description": "Repeat the Phase 2 inner ring inside each of the thirty outer tiling legs.",
            "boundary_order": block_contiguous,
        },
        {
            "name": "interface_star_inner_major",
            "template_kind": "six_tensor_inner_major",
            "description": "Group equal inner positions across all thirty outer tiling legs.",
            "boundary_order": inner_major,
        },
        {
            "name": "interface_star_cell_major",
            "template_kind": "six_tensor_cell_major",
            "description": "Group equal inner positions inside each of the six perfect cells.",
            "boundary_order": cell_major,
        },
    )


def holographic_phase23_capacity_profiles() -> tuple[tuple[int, int, int, int, int], ...]:
    return (
        (1, 1, 1, 1, 1),
        (2, 2, 2, 2, 2),
        (3, 3, 3, 3, 3),
        (1, 3, 3, 3, 3),
        (3, 1, 1, 1, 1),
        (1, 1, 3, 1, 1),
        (1, 1, 1, 3, 1),
        (1, 1, 1, 1, 3),
        (3, 3, 1, 1, 1),
        (1, 3, 1, 3, 1),
    )


def holographic_phase23_interface_network_spec(
    boundary_order: tuple[int, ...],
    *,
    capacities: tuple[int, int, int, int, int],
) -> dict[str, object]:
    if len(capacities) != 5:
        raise ValueError("Phase 23 interface star requires five bridge capacities")
    edges: list[dict[str, object]] = []
    internal_nodes = tuple(f"perfect_tensor_{cell}" for cell in range(6))
    for block in range(30):
        node = internal_nodes[block // 5]
        for inner in range(5):
            edges.append(
                holographic_phase4_edge(
                    node,
                    f"q{block * 5 + inner}",
                    edge_type="interface_star_boundary_leg",
                )
            )
    for (root, leaf), capacity in zip(holographic_phase23_interface_edges(), capacities):
        edges.append(
            holographic_phase4_edge(
                internal_nodes[root],
                internal_nodes[leaf],
                edge_type="interface_star_bridge",
                capacity=capacity,
            )
        )
    return {
        "name": f"interface_star_tree_only_{'_'.join(str(capacity) for capacity in capacities)}",
        "network_kind": "six_perfect_tensor_interface_star_tree_only",
        "description": (
            "Six internal perfect-tensor cells with cell 5 as an explicit interface/root node. Phase 23 uses no "
            "boundary ring, so leaf-interface bridge capacities are the only internal bottleneck variables."
        ),
        "topology": "interface_star",
        "boundary_mode": "tree_only",
        "interface_cell": 5,
        "tree_edges": holographic_phase23_interface_edges(),
        "capacities": capacities,
        "boundary_order": boundary_order,
        "boundary_nodes": tuple(f"q{qubit}" for qubit in boundary_order),
        "internal_nodes": internal_nodes,
        "edges": tuple(edges),
    }


def holographic_phase23_cell_qubits(cell: int) -> tuple[int, ...]:
    if cell < 0 or cell >= 6:
        raise ValueError("Phase 23 cell index must be in 0..5")
    return tuple(
        qubit
        for block in range(cell * 5, (cell + 1) * 5)
        for qubit in range(block * 5, block * 5 + 5)
    )


def holographic_phase23_compact_regions() -> tuple[dict[str, object], ...]:
    regions: list[dict[str, object]] = []
    for cell in range(6):
        qubits = tuple(cell * 25 + offset for offset in (4, 9, 14))
        regions.append(
            {
                "name": f"cell{cell}_local_compact",
                "region_type": "phase23_interface_star_local_compact_witness",
                "template": "interface_star_inner_major",
                "core_kind": "cell_local",
                "perfect_cells": (cell,),
                "qubits": qubits,
                "description": f"A compact source-aware witness contained in perfect cell {cell}.",
            }
        )
    for _root, leaf in holographic_phase23_interface_edges():
        qubits = (5 * 25 + 14, 5 * 25 + 19, 5 * 25 + 24, leaf * 25 + 4)
        regions.append(
            {
                "name": f"interface_edge_{leaf}_compact",
                "region_type": "phase23_interface_edge_compact_witness",
                "template": "interface_star_inner_major",
                "core_kind": "interface_edge_cross_cell",
                "perfect_cells": (5, leaf),
                "tree_edge": (5, leaf),
                "qubits": qubits,
                "description": f"A compact source-aware witness crossing the interface edge 5-{leaf}.",
            }
        )
    return tuple(regions)


def holographic_phase23_interface_regions() -> tuple[dict[str, object], ...]:
    root_shell = set(holographic_phase23_cell_qubits(5))
    regions: list[dict[str, object]] = []
    for _root, leaf in holographic_phase23_interface_edges():
        edge_core = {5 * 25 + 14, 5 * 25 + 19, 5 * 25 + 24, leaf * 25 + 4}
        regions.append(
            {
                "name": f"root_shell_plus_edge_{leaf}",
                "region_type": "phase23_root_shell_plus_interface_edge",
                "template": "interface_star_cell_major",
                "perfect_cells": (5, leaf),
                "qubits": tuple(sorted(root_shell | edge_core)),
                "description": f"Full interface/root shell plus one leaf qubit from compact edge witness 5-{leaf}.",
            }
        )
        regions.append(
            {
                "name": f"root_leaf_{leaf}_shells",
                "region_type": "phase23_root_leaf_shell_pair",
                "template": "interface_star_cell_major",
                "perfect_cells": (5, leaf),
                "qubits": tuple(sorted(root_shell | set(holographic_phase23_cell_qubits(leaf)))),
                "description": f"Full interface/root shell together with the full shell of leaf cell {leaf}.",
            }
        )
    return tuple(regions)


def holographic_phase23_region_payload(region_spec: dict[str, object]) -> dict[str, object]:
    qubits = tuple(int(qubit) for qubit in region_spec["qubits"])  # type: ignore[index]
    return {
        "name": region_spec["name"],
        "region_type": region_spec["region_type"],
        "template": region_spec["template"],
        "description": region_spec["description"],
        "qubits": qubits,
        "length": len(qubits),
        "outer_blocks": tuple(sorted({qubit // 5 for qubit in qubits})),
        "perfect_cells": tuple(int(cell) for cell in region_spec["perfect_cells"]),  # type: ignore[index]
        "mask": mask_from_qubits(qubits),
    }


def holographic_phase23_mincut_values(
    *,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_mask: int,
) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "capacity_profile": capacities,
            "value": int(holographic_network_min_cut(network_spec=network, region_mask=region_mask)["value"]),
        }
        for capacities, network in zip(capacity_profiles, networks)
    )


def holographic_phase23_semantic_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region_spec: dict[str, object],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    generator_kind: str,
) -> dict[str, object]:
    region = holographic_phase23_region_payload(region_spec)
    min_cut_values = holographic_phase23_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=int(region["mask"]),
    )
    hit = holographic_phase7_hit_record(
        circuit={
            "name": str(region["name"]),
            "generator_kind": generator_kind,
        },
        first=first,
        second=second,
        network_spec=networks[0],
        region=region,
    )
    return {
        "region": {key: value for key, value in region.items() if key != "mask"},
        "min_cut_values_by_capacity": min_cut_values,
        "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
        "min_cut_variable": len({int(record["value"]) for record in min_cut_values}) > 1,
        "all_mincuts_exact": all(
            int(holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))["assignments_checked"])
            == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
            for network in networks
        ),
        "hit": hit,
    }


def bridge_holography_phase23_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 23 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    outer_summary = holographic_phase23_outer_code_summary(outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    compact_regions = holographic_phase23_compact_regions()
    interface_regions = holographic_phase23_interface_regions()
    compact_records = tuple(
        holographic_phase23_semantic_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
            generator_kind="phase23_interface_star_compact_witness",
        )
        for region in compact_regions
    )
    interface_records = tuple(
        holographic_phase23_semantic_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
            generator_kind="phase23_interface_star_root_shell_probe",
        )
        for region in interface_regions
    )
    root_shell_edge_records = tuple(
        record
        for record in interface_records
        if str(record["region"]["region_type"]) == "phase23_root_shell_plus_interface_edge"
    )
    root_leaf_shell_records = tuple(
        record
        for record in interface_records
        if str(record["region"]["region_type"]) == "phase23_root_leaf_shell_pair"
    )
    all_records = compact_records + interface_records
    compact_summaries = tuple(
        {
            "region": record["region"]["name"],
            "length": record["region"]["length"],
            "perfect_cells": record["region"]["perfect_cells"],
            "min_cut_values": record["min_cut_values"],
            "entropy_pair": (record["hit"]["first"]["entropy"], record["hit"]["second"]["entropy"]),  # type: ignore[index]
            "algebra_pair": (
                record["hit"]["first"]["algebra_signature"],  # type: ignore[index]
                record["hit"]["second"]["algebra_signature"],  # type: ignore[index]
            ),
            "operator_or_channel_split": record["hit"]["comparisons"]["operator_or_channel_visible_differs"],  # type: ignore[index]
        }
        for record in compact_records
    )
    interface_summaries = tuple(
        {
            "region": record["region"]["name"],
            "region_type": record["region"]["region_type"],
            "length": record["region"]["length"],
            "perfect_cells": record["region"]["perfect_cells"],
            "min_cut_values": record["min_cut_values"],
            "entropy_pair": (record["hit"]["first"]["entropy"], record["hit"]["second"]["entropy"]),  # type: ignore[index]
            "algebra_pair": (
                record["hit"]["first"]["algebra_signature"],  # type: ignore[index]
                record["hit"]["second"]["algebra_signature"],  # type: ignore[index]
            ),
            "operator_or_channel_split": record["hit"]["comparisons"]["operator_or_channel_visible_differs"],  # type: ignore[index]
        }
        for record in interface_records
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "interface_outer_built": outer.n == 30 and outer.k == 1 and len(outer.generators) == 29,
        "outer_distance_three_witnessed": outer_summary["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3,  # type: ignore[index]
        "interface_concatenation_k1_n150": first.n == second.n == 150 and first.k == second.k == 1,
        "all_labeled_t2_entropy_matches": low_order_entropy["matches"]
        and low_order_entropy["subsets_checked"] == 11326,
        "compact_witnesses_keep_operator_or_channel_split": len(compact_records) == 11
        and all(record["hit"]["comparisons"]["operator_or_channel_visible_differs"] for record in compact_records),  # type: ignore[index]
        "compact_witness_mincuts_invariant": all(not record["min_cut_variable"] for record in compact_records),
        "interface_regions_are_capacity_sensitive": len(interface_records) == 10
        and all(record["min_cut_variable"] for record in interface_records),
        "interface_regions_keep_semantics_matched": all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"] for record in interface_records  # type: ignore[index]
        ),
        "root_shell_edge_probes_scored": len(root_shell_edge_records) == 5,
        "root_leaf_shell_probes_scored": len(root_leaf_shell_records) == 5,
        "all_reported_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
    }
    phase_claims["goal_3_phase_23_interface_star_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 23: interface-cell star audit",
        "status": "pass" if phase_claims["goal_3_phase_23_interface_star_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "interface_star_source": {
            "outer_code": outer_summary,
            "code_pair": {
                "n": first.n,
                "k": first.k,
                "first_generators": first.pauli_generators(),
                "second_generators": second.pauli_generators(),
            },
            "concatenation": {
                "first": first_metadata,
                "second": second_metadata,
            },
            "low_order_entropy": low_order_entropy,
        },
        "interface_audit": {
            "boundary_mode": "tree_only",
            "capacity_profiles": capacity_profiles,
            "compact_regions": compact_regions,
            "interface_regions": interface_regions,
            "compact_summaries": compact_summaries,
            "interface_summaries": interface_summaries,
            "compact_records": compact_records,
            "interface_records": interface_records,
            "filter_order": (
                "build a six-cell star with explicit root/interface cell",
                "score compact local and interface-edge witnesses",
                "score root-shell-plus-edge and root-plus-leaf shell probes",
                "exact entropy, min-cut, operator algebra, erasure, survivor, and distance diagnostics",
            ),
        },
        "counts": {
            "compact_regions": len(compact_records),
            "interface_regions": len(interface_records),
            "root_shell_plus_edge_regions": len(root_shell_edge_records),
            "root_leaf_shell_regions": len(root_leaf_shell_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "compact_operator_or_channel_split_records": sum(
                1
                for record in compact_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "compact_min_cut_variable_records": sum(1 for record in compact_records if record["min_cut_variable"]),
            "interface_operator_or_channel_split_records": sum(
                1
                for record in interface_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "interface_min_cut_variable_records": sum(1 for record in interface_records if record["min_cut_variable"]),
            "low_order_subsets_checked": low_order_entropy["subsets_checked"],
            "low_order_entropy_mismatches": low_order_entropy["mismatch_count"],
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A six-perfect-cell interface-star outer code gives an exact n=150,k=1 concatenated pair with matching "
                "labeled t<=2 entropy. Compact local and interface-edge witnesses retain the operator/erasure split, "
                "but remain min-cut-invariant. Root-shell-plus-edge and root-plus-leaf shell probes are capacity-"
                "sensitive, but their operator/channel semantics match."
            ),
            "three_geometry_lesson": (
                "Adding an explicit interface cell makes bottleneck-sensitive named regions smaller and more local to "
                "the interface than Phase 22's coarse shell unions, but it still does not align min-cut-visible "
                "geometry with reconstruction-visible geometry under these named probes."
            ),
            "scope_warning": (
                "The audit fixes one six-cell Y-bridge interface star, tree-only min-cut skeletons, ten bridge-capacity "
                "profiles, eleven compact witnesses, and ten named interface-shell probes. It is not an exhaustive "
                "punctured-interface-shell search or a full two-layer Clifford/MERA search."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The explicit interface cell still leaves a gap: compact witnesses are semantic but boundary-dominated, "
                "while interface-shell probes are bottleneck-visible but semantic-matched. The next phase should either "
                "run a bounded punctured-interface-shell frontier or build a genuine two-layer Clifford/MERA encoder "
                "whose compact witness support is mixed across layers before concatenation."
            ),
            "suggested_phase_24": (
                "Search punctured interface shells with a narrow hole grammar, or construct a two-layer Clifford/MERA-"
                "like outer encoder and rerun exact entropy, min-cut, algebra, erasure, survivor, and distance checks."
            ),
        },
    }


def holographic_phase24_root_witness_holes() -> tuple[int, ...]:
    return tuple(5 * 25 + offset for offset in (4, 9, 14, 19, 24))


def holographic_phase24_punctured_region_specs() -> tuple[dict[str, object], ...]:
    root_shell = set(holographic_phase23_cell_qubits(5))
    specs: list[dict[str, object]] = []
    for _root, leaf in holographic_phase23_interface_edges():
        edge_core = {5 * 25 + 14, 5 * 25 + 19, 5 * 25 + 24, leaf * 25 + 4}
        base_region = root_shell | edge_core
        for hole in holographic_phase24_root_witness_holes():
            specs.append(
                {
                    "name": f"root_shell_plus_edge_{leaf}_minus_q{hole}",
                    "region_type": "phase24_punctured_root_shell_plus_interface_edge",
                    "template": "interface_star_cell_major",
                    "perfect_cells": (5, leaf),
                    "leaf_cell": leaf,
                    "removed_root_qubit": hole,
                    "removed_root_offset": hole - 5 * 25,
                    "qubits": tuple(sorted(base_region - {hole})),
                    "description": (
                        f"Root-shell-plus-edge probe for interface edge 5-{leaf}, punctured by removing root "
                        f"witness-line qubit q{hole}."
                    ),
                }
            )
    return tuple(specs)


def holographic_phase24_punctured_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region_spec: dict[str, object],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
) -> dict[str, object]:
    region = holographic_phase23_region_payload(region_spec)
    min_cut_values = holographic_phase23_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=int(region["mask"]),
    )
    hit = holographic_phase7_hit_record(
        circuit={
            "name": str(region["name"]),
            "generator_kind": "phase24_punctured_interface_shell_frontier",
        },
        first=first,
        second=second,
        network_spec=networks[0],
        region=region,
    )
    all_mincuts_exact = all(
        int(holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))["assignments_checked"])
        == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
        for network in networks
    )
    return {
        "region": {
            key: value
            for key, value in region.items()
            if key != "mask"
        },
        "leaf_cell": int(region_spec["leaf_cell"]),
        "removed_root_qubit": int(region_spec["removed_root_qubit"]),
        "removed_root_offset": int(region_spec["removed_root_offset"]),
        "min_cut_values_by_capacity": min_cut_values,
        "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
        "min_cut_variable": len({int(record["value"]) for record in min_cut_values}) > 1,
        "all_mincuts_exact": all_mincuts_exact,
        "hit": hit,
    }


def bridge_holography_phase24_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 24 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    low_order_entropy = holographic_phase3_low_order_entropy_match(first, second, max_subset_size=2)
    outer_summary = holographic_phase23_outer_code_summary(outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    records = tuple(
        holographic_phase24_punctured_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
        )
        for region in region_specs
    )
    hit_records = tuple(
        record
        for record in records
        if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
    )
    hole_summaries = tuple(
        {
            "removed_root_qubit": hole,
            "removed_root_offset": hole - 5 * 25,
            "records": sum(1 for record in records if int(record["removed_root_qubit"]) == hole),
            "entropy_match_records": sum(
                1
                for record in records
                if int(record["removed_root_qubit"]) == hole
                and record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "min_cut_variable_records": sum(
                1 for record in records if int(record["removed_root_qubit"]) == hole and record["min_cut_variable"]
            ),
            "operator_or_channel_hits": sum(
                1
                for record in records
                if int(record["removed_root_qubit"]) == hole
                and record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
        }
        for hole in holographic_phase24_root_witness_holes()
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "interface_outer_reused": outer.n == 30 and outer.k == 1 and len(outer.generators) == 29,
        "outer_distance_three_witnessed": outer_summary["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3,  # type: ignore[index]
        "interface_concatenation_k1_n150": first.n == second.n == 150 and first.k == second.k == 1,
        "all_labeled_t2_entropy_matches": low_order_entropy["matches"]
        and low_order_entropy["subsets_checked"] == 11326,
        "punctured_frontier_exhausted": len(region_specs) == 25
        and len(holographic_phase24_root_witness_holes()) == 5,
        "all_punctured_regions_entropy_match": all(
            record["hit"]["comparisons"]["entropy_matches"] for record in records  # type: ignore[index]
        ),
        "all_punctured_regions_min_cut_variable": all(record["min_cut_variable"] for record in records),
        "no_punctured_operator_or_channel_hits": len(hit_records) == 0,
        "all_punctured_mincuts_exact": all(record["all_mincuts_exact"] for record in records),
        "all_holes_scored_for_all_leaves": all(summary["records"] == 5 for summary in hole_summaries),
    }
    phase_claims["goal_3_phase_24_punctured_interface_shell_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 24: punctured interface-shell frontier",
        "status": "pass" if phase_claims["goal_3_phase_24_punctured_interface_shell_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "interface_star_source": {
            "outer_code": outer_summary,
            "code_pair": {
                "n": first.n,
                "k": first.k,
                "first_generators": first.pauli_generators(),
                "second_generators": second.pauli_generators(),
            },
            "concatenation": {
                "first": first_metadata,
                "second": second_metadata,
            },
            "low_order_entropy": low_order_entropy,
        },
        "punctured_frontier": {
            "boundary_mode": "tree_only",
            "capacity_profiles": capacity_profiles,
            "root_witness_holes": holographic_phase24_root_witness_holes(),
            "region_specs": region_specs,
            "hole_summaries": hole_summaries,
            "records": records,
            "hit_records": hit_records,
            "filter_order": (
                "start from Phase 23 root-shell-plus-interface-edge probes",
                "remove one root/interface witness-line qubit from offsets 4,9,14,19,24",
                "score all five leaves for each hole",
                "exact entropy, min-cut, operator algebra, erasure, survivor, and distance diagnostics",
            ),
        },
        "counts": {
            "root_witness_holes": len(holographic_phase24_root_witness_holes()),
            "leaf_cells_scored": len(holographic_phase23_interface_edges()),
            "punctured_records": len(records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(
                1 for record in records if record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "min_cut_variable_records": sum(1 for record in records if record["min_cut_variable"]),
            "operator_or_channel_hits": len(hit_records),
            "low_order_subsets_checked": low_order_entropy["subsets_checked"],
            "low_order_entropy_mismatches": low_order_entropy["mismatch_count"],
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A narrow punctured-interface-shell frontier on the Phase 23 interface star scores all 25 one-hole "
                "root-witness-line punctures. Every punctured region has matching entropy and capacity-sensitive "
                "tree-only min-cuts, but none recovers an operator/reconstruction or erasure/survivor split."
            ),
            "three_geometry_lesson": (
                "Small punctures near the compact witness line raise the punctured region entropy to match the compact "
                "witness scale and keep the min-cut bottleneck visible. The operator/channel semantics still collapse "
                "to the matched shell behavior, so the mismatch is not repaired by a one-qubit interface puncture."
            ),
            "scope_warning": (
                "The audit fixes the Phase 23 six-cell Y-bridge interface star and searches only five one-qubit "
                "root witness-line punctures for each leaf. It does not exhaust arbitrary holes, two-hole punctures, "
                "or two-layer Clifford/MERA encoders."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "One-qubit punctures do not restore the compact operator/channel witness. The next phase should move "
                "away from shell surgery and construct a genuine two-layer Clifford/MERA-like encoder, or use a very "
                "small certified two-hole puncture subgrammar only if runtime remains controlled."
            ),
            "suggested_phase_25": (
                "Build a two-layer Clifford/MERA-like outer encoder that mixes interface and leaf supports before "
                "concatenation, then rerun exact entropy, min-cut, algebra, erasure, survivor, and distance checks."
            ),
        },
    }


def holographic_phase25_two_layer_circuit_specs() -> tuple[dict[str, object], ...]:
    def root_to_leaf_gates() -> tuple[tuple[object, ...], ...]:
        return tuple(("CX", 25 + offset, 5 * leaf + offset) for offset in range(5) for leaf in range(5))

    def leaf_to_root_gates() -> tuple[tuple[object, ...], ...]:
        return tuple(("CX", 5 * leaf + offset, 25 + offset) for offset in range(5) for leaf in range(5))

    def alternating_gates() -> tuple[tuple[object, ...], ...]:
        gates: list[tuple[object, ...]] = []
        for leaf in range(5):
            for offset in (0, 2, 4):
                gates.append(("CX", 25 + offset, 5 * leaf + offset))
        for leaf in range(5):
            for offset in (1, 3):
                gates.append(("CX", 5 * leaf + offset, 25 + offset))
        return tuple(gates)

    def sparse_ladder_gates() -> tuple[tuple[object, ...], ...]:
        gates: list[tuple[object, ...]] = []
        for leaf in range(5):
            gates.append(("CX", 25 + (leaf % 5), 5 * leaf + ((leaf + 1) % 5)))
            gates.append(("CX", 5 * leaf + ((leaf + 2) % 5), 25 + ((leaf + 3) % 5)))
        return tuple(gates)

    return (
        {
            "name": "root_to_leaf_same_position",
            "layer_kind": "two_layer_full_fanout",
            "description": "Layer all same-position CX gates from the root/interface cell to every leaf cell.",
            "gates": root_to_leaf_gates(),
        },
        {
            "name": "leaf_to_root_same_position",
            "layer_kind": "two_layer_full_fanin",
            "description": "Layer all same-position CX gates from every leaf cell into the root/interface cell.",
            "gates": leaf_to_root_gates(),
        },
        {
            "name": "alternating_disentangler_isometry",
            "layer_kind": "two_layer_alternating",
            "description": "Use root-to-leaf CX gates on offsets 0,2,4 and leaf-to-root CX gates on offsets 1,3.",
            "gates": alternating_gates(),
        },
        {
            "name": "sparse_offset_ladder",
            "layer_kind": "two_layer_sparse_ladder",
            "description": "Use a sparse offset ladder of leaf/root CX gates, one pair per leaf.",
            "gates": sparse_ladder_gates(),
        },
    )


def holographic_phase25_apply_outer_circuit(
    code: StabilizerCode,
    gates: tuple[tuple[object, ...], ...],
) -> StabilizerCode:
    rows = tuple(code.generators)
    for gate in gates:
        kind = str(gate[0])
        if kind == "H":
            rows = tuple(apply_h(row, code.n, int(gate[1])) for row in rows)
        elif kind == "S":
            rows = tuple(apply_s(row, code.n, int(gate[1])) for row in rows)
        elif kind == "CX":
            rows = tuple(apply_cx(row, code.n, int(gate[1]), int(gate[2])) for row in rows)
        else:
            raise ValueError(f"unknown Phase 25 Clifford gate {kind!r}")
    return StabilizerCode(code.n, rows)


def holographic_phase25_variant_record(
    *,
    spec: dict[str, object],
    base_outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in spec["gates"])  # type: ignore[index]
    outer = holographic_phase25_apply_outer_circuit(base_outer, gates)
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    distance_audit = bounded_distance_certificate(outer, max_weight=3)
    records = tuple(
        holographic_phase24_punctured_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
        )
        for region in region_specs
    )
    admissible_hit_records = tuple(
        record
        for record in records
        if record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
        and record["min_cut_variable"]
        and record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
    )
    near_hit_records = tuple(
        record
        for record in records
        if not record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
        and record["min_cut_variable"]
        and record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
    )
    summary = {
        "punctured_records": len(records),
        "entropy_match_records": sum(
            1 for record in records if record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
        ),
        "entropy_mismatch_records": sum(
            1 for record in records if not record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
        ),
        "min_cut_variable_records": sum(1 for record in records if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "entropy_mismatch_operator_near_hits": len(near_hit_records),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in records),
    }
    return {
        "variant": {
            "name": spec["name"],
            "layer_kind": spec["layer_kind"],
            "description": spec["description"],
            "gates": gates,
            "gate_count": len(gates),
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": distance_audit,
        },
        "code_pair": {"n": first.n, "k": first.k},
        "summary": summary,
        "records": records,
        "admissible_hit_records": admissible_hit_records,
        "near_hit_records": near_hit_records,
    }


def bridge_holography_phase25_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 25 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase25_two_layer_circuit_specs()
    variant_records = tuple(
        holographic_phase25_variant_record(
            spec=spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
        )
        for spec in variant_specs
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    near_hits = tuple(record for variant in variant_records for record in variant["near_hit_records"])  # type: ignore[index]
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "interface_outer_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "two_layer_circuit_menu_scored": len(variant_specs) == 4 and len(variant_records) == 4,
        "all_variant_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in variant_records
        ),
        "punctured_frontier_replayed_for_each_variant": len(region_specs) == 25
        and all(variant["summary"]["punctured_records"] == 25 for variant in variant_records),  # type: ignore[index]
        "all_variant_punctured_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
        "all_variant_punctures_min_cut_variable": all(record["min_cut_variable"] for record in all_records),
        "no_admissible_entropy_matched_operator_hits": len(admissible_hits) == 0,
        "entropy_mismatched_operator_near_hits_exist": len(near_hits) == 30,
        "distance_three_or_better_bounded": all(
            int(variant["outer_code"]["distance_audit_weight3"]["distance_lower_bound"]) >= 3  # type: ignore[index]
            for variant in variant_records
        ),
    }
    phase_claims["goal_3_phase_25_two_layer_clifford_menu_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 25: two-layer Clifford/MERA-like punctured-frontier menu",
        "status": "pass" if phase_claims["goal_3_phase_25_two_layer_clifford_menu_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
        },
        "two_layer_menu": {
            "variant_specs": variant_specs,
            "variant_records": variant_records,
            "admissible_hit_records": admissible_hits,
            "near_hit_records": near_hits,
            "filter_order": (
                "apply a bounded two-layer Clifford circuit to the Phase 23 interface-star outer code",
                "concatenate each transformed outer code with the Phase 2 source",
                "replay the 25 Phase 24 punctured interface-shell regions",
                "require exact entropy match, exact min-cut variation, and exact operator/erasure split for admissible hits",
                "report entropy-mismatched operator splits separately as near-hits",
            ),
        },
        "counts": {
            "two_layer_variants": len(variant_records),
            "punctured_regions_per_variant": len(region_specs),
            "variant_punctured_records": len(all_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(
                1 for record in all_records if record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "entropy_mismatch_records": sum(
                1 for record in all_records if not record["hit"]["comparisons"]["entropy_matches"]  # type: ignore[index]
            ),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records": sum(
                1
                for record in all_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "entropy_mismatch_operator_near_hits": len(near_hits),
            "distance_three_witness_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "distance_lower_bound_four_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_lower_bound"] == 4  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded two-layer Clifford/MERA-like menu over the interface-star outer code replays all 25 "
                "punctured interface-shell probes for four transformed outer codes. It finds no admissible region "
                "with matching entropy, capacity-sensitive min-cut, and operator/channel split. It does find 30 "
                "operator/channel near-hits, all rejected by the entropy gate."
            ),
            "three_geometry_lesson": (
                "Two-layer Clifford mixing can move operator/channel-visible behavior into the punctured interface "
                "frontier, but in this menu it does so only by breaking paired entropy equality. The entropy-visible "
                "and reconstruction-visible geometries still refuse to coincide on the same certified regions."
            ),
            "scope_warning": (
                "The audit covers four hand-built two-layer CX menus and the 25 Phase 24 punctured regions. It does not "
                "enumerate all Clifford circuits, all MERA layouts, two-hole punctures, or arbitrary boundary regions."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The near-hits show that Clifford mixing can restore operator/channel distinction, but the entropy "
                "gate fails. The next phase should either search a bounded local gate-neighborhood around the "
                "alternating and leaf-to-root near-hits, or change the inner source/outer block pairing so the same "
                "mixed support can regain entropy equality."
            ),
            "suggested_phase_26": (
                "Run a local gate-neighborhood search around the alternating and leaf-to-root circuits, filtering first "
                "for entropy-matched punctured regions and then exact operator/channel split."
            ),
        },
    }


def holographic_phase26_same_position_gates(
    offset: int,
    direction: str,
) -> tuple[tuple[object, ...], ...]:
    if offset < 0 or offset >= 5:
        raise ValueError("Phase 26 offset must be in 0..4")
    if direction == "root_to_leaf":
        return tuple(("CX", 25 + offset, 5 * leaf + offset) for leaf in range(5))
    if direction == "leaf_to_root":
        return tuple(("CX", 5 * leaf + offset, 25 + offset) for leaf in range(5))
    raise ValueError(f"unknown Phase 26 direction {direction!r}")


def holographic_phase26_flip_offset_gates(
    gates: tuple[tuple[object, ...], ...],
    *,
    offset: int,
) -> tuple[tuple[tuple[object, ...], ...], str]:
    root_to_leaf = set(holographic_phase26_same_position_gates(offset, "root_to_leaf"))
    leaf_to_root = set(holographic_phase26_same_position_gates(offset, "leaf_to_root"))
    gate_set = set(gates)
    if gate_set & root_to_leaf:
        old = root_to_leaf
        new = tuple(sorted(leaf_to_root, key=str))
        to_direction = "leaf_to_root"
    elif gate_set & leaf_to_root:
        old = leaf_to_root
        new = tuple(sorted(root_to_leaf, key=str))
        to_direction = "root_to_leaf"
    else:
        raise ValueError(f"Phase 26 base circuit has no same-position offset-{offset} gates")
    retained = tuple(gate for gate in gates if gate not in old)
    return retained + new, to_direction


def holographic_phase26_offset_flip_neighborhood_specs() -> tuple[dict[str, object], ...]:
    phase25_specs = {str(spec["name"]): spec for spec in holographic_phase25_two_layer_circuit_specs()}
    parents = ("leaf_to_root_same_position", "alternating_disentangler_isometry")
    specs: list[dict[str, object]] = []
    for parent_name in parents:
        parent = phase25_specs[parent_name]
        parent_gates = tuple(tuple(gate) for gate in parent["gates"])  # type: ignore[index]
        for offset in range(5):
            gates, to_direction = holographic_phase26_flip_offset_gates(parent_gates, offset=offset)
            specs.append(
                {
                    "name": f"{parent_name}__flip_offset_{offset}_to_{to_direction}",
                    "layer_kind": "phase26_offset_flip_neighborhood",
                    "parent": parent_name,
                    "mutation_kind": "same_position_offset_direction_flip",
                    "flipped_offset": offset,
                    "to_direction": to_direction,
                    "description": (
                        f"Start from {parent_name} and flip every same-position CX gate at outer offset "
                        f"{offset} to {to_direction}."
                    ),
                    "gates": gates,
                }
            )
    return tuple(specs)


def holographic_phase26_entropy_gated_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    region_spec: dict[str, object],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    audit_entropy_mismatch_near_hits: bool,
) -> dict[str, object]:
    region = holographic_phase23_region_payload(region_spec)
    region_mask = int(region["mask"])
    min_cut_values = holographic_phase23_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=region_mask,
    )
    first_entropy = first.entropy(region_mask)
    second_entropy = second.entropy(region_mask)
    entropy_matches = first_entropy == second_entropy
    operator_channel_checked = entropy_matches or audit_entropy_mismatch_near_hits
    hit = (
        holographic_phase7_hit_record(
            circuit={
                "name": str(region["name"]),
                "generator_kind": "phase26_offset_flip_entropy_gated_frontier",
            },
            first=first,
            second=second,
            network_spec=networks[0],
            region=region,
        )
        if operator_channel_checked
        else None
    )
    operator_or_channel_split = (
        bool(hit["comparisons"]["operator_or_channel_visible_differs"]) if hit is not None else None  # type: ignore[index]
    )
    all_mincuts_exact = all(
        int(holographic_network_min_cut(network_spec=network, region_mask=region_mask)["assignments_checked"])
        == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
        for network in networks
    )
    min_cut_variable = len({int(record["value"]) for record in min_cut_values}) > 1
    return {
        "region": {key: value for key, value in region.items() if key != "mask"},
        "leaf_cell": int(region_spec["leaf_cell"]),
        "removed_root_qubit": int(region_spec["removed_root_qubit"]),
        "removed_root_offset": int(region_spec["removed_root_offset"]),
        "entropy_pair": (first_entropy, second_entropy),
        "entropy_matches": entropy_matches,
        "operator_channel_checked": operator_channel_checked,
        "min_cut_values_by_capacity": min_cut_values,
        "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
        "min_cut_variable": min_cut_variable,
        "all_mincuts_exact": all_mincuts_exact,
        "hit": hit,
        "admissible_entropy_match_min_cut_operator_hit": bool(
            entropy_matches
            and min_cut_variable
            and hit is not None
            and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "entropy_mismatch_operator_near_hit": bool(
            not entropy_matches
            and min_cut_variable
            and hit is not None
            and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "strict_filter_stage": (
            "operator_channel_checked"
            if operator_channel_checked
            else "entropy_gate_rejected_before_operator_channel_check"
        ),
    }


def holographic_phase26_variant_record(
    *,
    spec: dict[str, object],
    base_outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
    audit_entropy_mismatch_near_hits: bool,
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in spec["gates"])  # type: ignore[index]
    outer = holographic_phase25_apply_outer_circuit(base_outer, gates)
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    distance_audit = bounded_distance_certificate(outer, max_weight=3)
    records = tuple(
        holographic_phase26_entropy_gated_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
            audit_entropy_mismatch_near_hits=audit_entropy_mismatch_near_hits,
        )
        for region in region_specs
    )
    admissible_hit_records = tuple(
        record for record in records if record["admissible_entropy_match_min_cut_operator_hit"]
    )
    near_hit_records = tuple(record for record in records if record["entropy_mismatch_operator_near_hit"])
    operator_checked_records = tuple(record for record in records if record["operator_channel_checked"])
    summary = {
        "punctured_records": len(records),
        "entropy_match_records": sum(1 for record in records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in records if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "entropy_gate_rejections": sum(1 for record in records if not record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in records if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1 for record in operator_checked_records if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "entropy_mismatch_operator_near_hits": len(near_hit_records)
        if audit_entropy_mismatch_near_hits
        else None,
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in records),
    }
    return {
        "variant": {
            "name": spec["name"],
            "layer_kind": spec["layer_kind"],
            "description": spec["description"],
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "gates": gates,
            "gate_count": len(gates),
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": distance_audit,
        },
        "code_pair": {"n": first.n, "k": first.k},
        "summary": summary,
        "records": records,
        "admissible_hit_records": admissible_hit_records,
        "near_hit_records": near_hit_records,
    }


def holographic_phase26_parent_summaries(
    variant_records: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    parents = tuple(dict.fromkeys(str(record["variant"]["parent"]) for record in variant_records))  # type: ignore[index]
    summaries: list[dict[str, object]] = []
    for parent in parents:
        selected = tuple(
            record for record in variant_records if str(record["variant"]["parent"]) == parent  # type: ignore[index]
        )
        summaries.append(
            {
                "parent": parent,
                "variants": len(selected),
                "punctured_records": sum(int(record["summary"]["punctured_records"]) for record in selected),  # type: ignore[index]
                "entropy_match_records": sum(int(record["summary"]["entropy_match_records"]) for record in selected),  # type: ignore[index]
                "operator_channel_checked_records": sum(
                    int(record["summary"]["operator_channel_checked_records"]) for record in selected  # type: ignore[index]
                ),
                "operator_or_channel_split_records": sum(
                    int(record["summary"]["operator_or_channel_split_records"]) for record in selected  # type: ignore[index]
                ),
                "admissible_entropy_match_min_cut_operator_hits": sum(
                    int(record["summary"]["admissible_entropy_match_min_cut_operator_hits"])  # type: ignore[index]
                    for record in selected
                ),
                "entropy_mismatch_operator_near_hits": None
                if any(record["summary"]["entropy_mismatch_operator_near_hits"] is None for record in selected)  # type: ignore[index]
                else sum(int(record["summary"]["entropy_mismatch_operator_near_hits"]) for record in selected),  # type: ignore[index]
            }
        )
    return tuple(summaries)


def bridge_holography_phase26_certificate(
    *,
    graph_max_codes: int = 24,
    audit_entropy_mismatch_near_hits: bool = False,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 26 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    variant_records = tuple(
        holographic_phase26_variant_record(
            spec=spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
            audit_entropy_mismatch_near_hits=audit_entropy_mismatch_near_hits,
        )
        for spec in variant_specs
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    near_hits = tuple(record for variant in variant_records for record in variant["near_hit_records"])  # type: ignore[index]
    parent_summaries = holographic_phase26_parent_summaries(variant_records)
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "interface_outer_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "offset_flip_neighborhood_scored": len(variant_specs) == 10 and len(variant_records) == 10,
        "all_neighbor_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in variant_records
        ),
        "all_neighbor_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in variant_records
        ),
        "punctured_frontier_replayed_for_each_neighbor": len(region_specs) == 25
        and all(variant["summary"]["punctured_records"] == 25 for variant in variant_records),  # type: ignore[index]
        "all_neighbor_punctured_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
        "all_neighbor_punctures_min_cut_variable": all(record["min_cut_variable"] for record in all_records),
        "all_entropy_matched_records_operator_checked": all(
            record["operator_channel_checked"] for record in all_records if record["entropy_matches"]
        ),
        "no_entropy_matched_operator_hits_in_neighborhood": len(admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in operator_checked_records
            if record["entropy_matches"]
        ),
        "entropy_mismatch_near_hits_audited_if_requested": (
            bool(audit_entropy_mismatch_near_hits)
            == all(record["operator_channel_checked"] for record in all_records if not record["entropy_matches"])
        ),
    }
    phase_claims["goal_3_phase_26_offset_flip_entropy_gated_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 26: offset-flip local neighborhood entropy-gated no-go",
        "status": "pass" if phase_claims["goal_3_phase_26_offset_flip_entropy_gated_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
        },
        "search_scope": {
            "parent_circuits": ("leaf_to_root_same_position", "alternating_disentangler_isometry"),
            "mutation_rule": (
                "For each parent and each outer offset 0..4, flip the direction of all five same-position "
                "root/leaf CX gates at that offset."
            ),
            "variant_specs": variant_specs,
            "filter_order": (
                "exact entropy for every candidate record",
                "exact min-cut variation for every candidate record",
                "exact algebra, erasure, and survivor checks only after the entropy gate by default",
                "entropy-mismatched near-hit operator checks are run only when audit_entropy_mismatch_near_hits is true",
            ),
            "audit_entropy_mismatch_near_hits": audit_entropy_mismatch_near_hits,
        },
        "neighborhood": {
            "variant_records": variant_records,
            "parent_summaries": parent_summaries,
            "admissible_hit_records": admissible_hits,
            "entropy_mismatch_near_hit_records": near_hits if audit_entropy_mismatch_near_hits else None,
        },
        "counts": {
            "offset_flip_variants": len(variant_records),
            "parent_circuits": len(parent_summaries),
            "punctured_regions_per_variant": len(region_specs),
            "candidate_records": len(all_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "entropy_gate_rejections": sum(1 for record in all_records if not record["operator_channel_checked"]),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": sum(
                1
                for record in operator_checked_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "entropy_mismatch_operator_near_hits": len(near_hits) if audit_entropy_mismatch_near_hits else None,
            "distance_three_witness_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded local offset-flip neighborhood around the two Phase 25 near-hit parent circuits scores "
                "250 punctured-region records. Ninety records pass the exact entropy gate, and every one of those "
                "is checked exactly for algebra, erasure, and survivor semantics. None becomes an admissible "
                "entropy-matched operator/channel hit."
            ),
            "three_geometry_lesson": (
                "Offset-level gate direction changes can repair portions of the entropy frontier, but the repaired "
                "entropy records lose the reconstruction/channel distinction. The obstruction is therefore stable "
                "under this local MERA-like neighborhood, not just under the four Phase 25 parent circuits."
            ),
            "scope_warning": (
                "The default certificate is entropy-gated: entropy-mismatched records are rejected before the "
                "operator/channel audit unless audit_entropy_mismatch_near_hits is enabled. The search covers ten "
                "offset-flip circuits, not arbitrary single-gate flips, all Clifford circuits, or all MERA layouts."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The offset-flip neighborhood turns the Phase 25 near-hit circuits into a stricter no-go: entropy "
                "repair and operator/channel split still do not coincide. The next search should change the region "
                "grammar instead of only flipping global offset directions."
            ),
            "suggested_phase_27": (
                "Add a bounded two-hole or leaf-private-region grammar around the Phase 26 entropy-passing records, "
                "then keep the same entropy-first exact admissibility filter."
            ),
        },
    }


def holographic_phase27_second_root_hole_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    root_holes = holographic_phase24_root_witness_holes()
    qubits = set(int(qubit) for qubit in base_region_spec["qubits"])  # type: ignore[index]
    first_hole = int(base_region_spec["removed_root_qubit"])
    specs: list[dict[str, object]] = []
    for second_hole in root_holes:
        if second_hole == first_hole or second_hole not in qubits:
            continue
        specs.append(
            {
                **base_region_spec,
                "name": f"{base_region_spec['name']}__second_root_hole_q{second_hole}",
                "region_type": "phase27_second_root_hole",
                "phase27_edit": "second_root_hole",
                "second_removed_root_qubit": second_hole,
                "second_removed_root_offset": second_hole - 5 * 25,
                "qubits": tuple(sorted(qubits - {second_hole})),
                "description": (
                    f"Phase 27 two-root-hole variant of {base_region_spec['name']}: remove q{second_hole} "
                    "after the Phase 24 root witness-line puncture."
                ),
            }
        )
    return tuple(specs)


def holographic_phase27_region_payload(region_spec: dict[str, object]) -> dict[str, object]:
    payload = holographic_phase23_region_payload(region_spec)
    return {
        **payload,
        "phase27_edit": region_spec["phase27_edit"],
        "first_removed_root_qubit": region_spec["removed_root_qubit"],
        "first_removed_root_offset": region_spec["removed_root_offset"],
        "second_removed_root_qubit": region_spec["second_removed_root_qubit"],
        "second_removed_root_offset": region_spec["second_removed_root_offset"],
        "leaf_cell": region_spec["leaf_cell"],
    }


def holographic_phase27_second_hole_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    base_region_spec: dict[str, object],
    second_hole_spec: dict[str, object],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
) -> dict[str, object]:
    base_region = holographic_phase23_region_payload(base_region_spec)
    base_mask = int(base_region["mask"])
    base_first_entropy = first.entropy(base_mask)
    base_second_entropy = second.entropy(base_mask)
    base_entropy_matches = base_first_entropy == base_second_entropy

    region = holographic_phase27_region_payload(second_hole_spec)
    region_mask = int(region["mask"])
    min_cut_values = holographic_phase23_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=region_mask,
    )
    all_mincuts_exact = all(
        int(holographic_network_min_cut(network_spec=network, region_mask=region_mask)["assignments_checked"])
        == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
        for network in networks
    )
    first_entropy = first.entropy(region_mask)
    second_entropy = second.entropy(region_mask)
    entropy_matches = first_entropy == second_entropy
    hit = (
        holographic_phase7_hit_record(
            circuit={
                "name": str(region["name"]),
                "generator_kind": "phase27_second_root_hole_region_grammar",
            },
            first=first,
            second=second,
            network_spec=networks[0],
            region=region,
        )
        if entropy_matches
        else None
    )
    min_cut_variable = len({int(record["value"]) for record in min_cut_values}) > 1
    return {
        "base_region": {
            key: value
            for key, value in base_region.items()
            if key != "mask"
        },
        "base_entropy_pair": (base_first_entropy, base_second_entropy),
        "base_entropy_matches": base_entropy_matches,
        "region": {
            key: value
            for key, value in region.items()
            if key != "mask"
        },
        "leaf_cell": int(second_hole_spec["leaf_cell"]),
        "first_removed_root_qubit": int(second_hole_spec["removed_root_qubit"]),
        "first_removed_root_offset": int(second_hole_spec["removed_root_offset"]),
        "second_removed_root_qubit": int(second_hole_spec["second_removed_root_qubit"]),
        "second_removed_root_offset": int(second_hole_spec["second_removed_root_offset"]),
        "entropy_pair": (first_entropy, second_entropy),
        "entropy_matches": entropy_matches,
        "operator_channel_checked": entropy_matches,
        "min_cut_values_by_capacity": min_cut_values,
        "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
        "min_cut_variable": min_cut_variable,
        "all_mincuts_exact": all_mincuts_exact,
        "hit": hit,
        "admissible_entropy_match_min_cut_operator_hit": bool(
            entropy_matches
            and min_cut_variable
            and hit is not None
            and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "strict_filter_stage": (
            "operator_channel_checked" if entropy_matches else "second_hole_entropy_gate_rejected"
        ),
    }


def holographic_phase27_variant_record(
    *,
    spec: dict[str, object],
    base_outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in spec["gates"])  # type: ignore[index]
    outer = holographic_phase25_apply_outer_circuit(base_outer, gates)
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    distance_audit = bounded_distance_certificate(outer, max_weight=3)

    records: list[dict[str, object]] = []
    base_entropy_passes = 0
    for base_region_spec in region_specs:
        base_region = holographic_phase23_region_payload(base_region_spec)
        if first.entropy(int(base_region["mask"])) != second.entropy(int(base_region["mask"])):
            continue
        base_entropy_passes += 1
        for second_hole_spec in holographic_phase27_second_root_hole_specs(base_region_spec):
            records.append(
                holographic_phase27_second_hole_record(
                    first=first,
                    second=second,
                    base_region_spec=base_region_spec,
                    second_hole_spec=second_hole_spec,
                    networks=networks,
                    capacity_profiles=capacity_profiles,
                )
            )
    record_tuple = tuple(records)
    operator_checked_records = tuple(record for record in record_tuple if record["operator_channel_checked"])
    admissible_hit_records = tuple(
        record for record in record_tuple if record["admissible_entropy_match_min_cut_operator_hit"]
    )
    summary = {
        "base_entropy_pass_records": base_entropy_passes,
        "candidate_second_hole_records": len(record_tuple),
        "entropy_match_records": sum(1 for record in record_tuple if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in record_tuple if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "second_hole_entropy_gate_rejections": sum(1 for record in record_tuple if not record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in record_tuple if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in operator_checked_records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in record_tuple),
    }
    return {
        "variant": {
            "name": spec["name"],
            "layer_kind": "phase27_second_root_hole_region_grammar",
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "gates": gates,
            "gate_count": len(gates),
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": distance_audit,
        },
        "code_pair": {"n": first.n, "k": first.k},
        "summary": summary,
        "records": record_tuple,
        "admissible_hit_records": admissible_hit_records,
    }


def holographic_phase27_parent_summaries(
    variant_records: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    parents = tuple(dict.fromkeys(str(record["variant"]["parent"]) for record in variant_records))  # type: ignore[index]
    summaries: list[dict[str, object]] = []
    for parent in parents:
        selected = tuple(
            record for record in variant_records if str(record["variant"]["parent"]) == parent  # type: ignore[index]
        )
        summaries.append(
            {
                "parent": parent,
                "variants": len(selected),
                "base_entropy_pass_records": sum(
                    int(record["summary"]["base_entropy_pass_records"]) for record in selected  # type: ignore[index]
                ),
                "candidate_second_hole_records": sum(
                    int(record["summary"]["candidate_second_hole_records"]) for record in selected  # type: ignore[index]
                ),
                "entropy_match_records": sum(
                    int(record["summary"]["entropy_match_records"]) for record in selected  # type: ignore[index]
                ),
                "operator_channel_checked_records": sum(
                    int(record["summary"]["operator_channel_checked_records"]) for record in selected  # type: ignore[index]
                ),
                "operator_or_channel_split_records": sum(
                    int(record["summary"]["operator_or_channel_split_records"]) for record in selected  # type: ignore[index]
                ),
                "admissible_entropy_match_min_cut_operator_hits": sum(
                    int(record["summary"]["admissible_entropy_match_min_cut_operator_hits"])  # type: ignore[index]
                    for record in selected
                ),
            }
        )
    return tuple(summaries)


def bridge_holography_phase27_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 27 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    variant_records = tuple(
        holographic_phase27_variant_record(
            spec=spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
        )
        for spec in variant_specs
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    parent_summaries = holographic_phase27_parent_summaries(variant_records)
    selected_entropy_matched_record = next(
        (
            record
            for variant in variant_records
            for record in variant["records"]  # type: ignore[index]
            if record["entropy_matches"]
        ),
        None,
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "interface_outer_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "offset_flip_neighborhood_reused": len(variant_specs) == 10 and len(variant_records) == 10,
        "all_neighbor_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in variant_records
        ),
        "all_neighbor_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in variant_records
        ),
        "second_root_hole_grammar_exhausted_around_entropy_passes": sum(
            int(variant["summary"]["base_entropy_pass_records"]) for variant in variant_records  # type: ignore[index]
        )
        == 90
        and len(all_records) == 360,
        "all_second_hole_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
        "all_second_hole_records_min_cut_variable": all(record["min_cut_variable"] for record in all_records),
        "all_second_hole_entropy_matches_operator_checked": all(
            record["operator_channel_checked"] for record in all_records if record["entropy_matches"]
        ),
        "no_second_hole_admissible_hits": len(admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in operator_checked_records
        ),
    }
    phase_claims["goal_3_phase_27_second_root_hole_region_grammar_no_go_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 27: second-root-hole region-grammar no-go",
        "status": "pass"
        if phase_claims["goal_3_phase_27_second_root_hole_region_grammar_no_go_certificate"]
        else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 26 offset-flip entropy-gated neighborhood",
            "region_grammar": (
                "For every Phase 26 base puncture that passes the entropy gate, remove one additional root "
                "witness-line qubit from the remaining four root-hole positions."
            ),
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "root_witness_holes": holographic_phase24_root_witness_holes(),
            "filter_order": (
                "exact base-puncture entropy gate",
                "generate all remaining second-root-hole edits",
                "exact entropy and exact min-cut variation for every second-hole record",
                "exact algebra, erasure, and survivor checks for entropy-matched second-hole records",
            ),
        },
        "second_hole_frontier": {
            "variant_records": variant_records,
            "parent_summaries": parent_summaries,
            "selected_entropy_matched_record": selected_entropy_matched_record,
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "offset_flip_variants": len(variant_records),
            "parent_circuits": len(parent_summaries),
            "base_punctured_regions": len(region_specs),
            "base_entropy_pass_records": sum(
                int(variant["summary"]["base_entropy_pass_records"]) for variant in variant_records  # type: ignore[index]
            ),
            "candidate_second_hole_records": len(all_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "second_hole_entropy_gate_rejections": sum(
                1 for record in all_records if not record["operator_channel_checked"]
            ),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": sum(
                1
                for record in operator_checked_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "distance_three_witness_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The second-root-hole grammar expands every Phase 26 entropy-passing puncture by removing one "
                "additional root witness-line qubit. It scores 360 exact second-hole records; 60 remain "
                "entropy-matched and receive exact operator/channel checks. None is an admissible hit."
            ),
            "three_geometry_lesson": (
                "Adding a second root-shell puncture keeps the min-cut geometry capacity-sensitive for every "
                "candidate. The few candidates that keep entropy equality still have matching observer algebra, "
                "erasure, and survivor semantics, so the reconstruction-visible geometry remains collapsed."
            ),
            "scope_warning": (
                "The search is exhaustive only for the second-root-hole grammar around Phase 26 entropy-passing "
                "records. It does not cover leaf-private additions, arbitrary two-hole punctures, changed inner "
                "sources, or broader Clifford/MERA circuits."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The root-side two-hole grammar rejects the remaining strict candidates. The heavier leaf-private "
                "additions looked entropy-rich in scratch exploration, so the next phase should audit a carefully "
                "bounded leaf-private subgrammar or change the inner/outer source pairing."
            ),
            "suggested_phase_28": (
                "Run a leaf-private add grammar with a smaller sentinel set or a cached certificate path, then "
                "separate entropy-rich no-go evidence from any operator/channel near-hits."
            ),
        },
    }


def holographic_phase28_sentinel_variant_names() -> tuple[str, ...]:
    return (
        "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root",
        "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root",
    )


def holographic_phase28_leaf_private_add_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    qubits = set(int(qubit) for qubit in base_region_spec["qubits"])  # type: ignore[index]
    leaf = int(base_region_spec["leaf_cell"])
    specs: list[dict[str, object]] = []
    for leaf_offset in range(4):
        qubit = leaf * 25 + leaf_offset
        if qubit in qubits:
            continue
        specs.append(
            {
                **base_region_spec,
                "name": f"{base_region_spec['name']}__add_leaf_private_q{qubit}",
                "region_type": "phase28_leaf_private_add",
                "phase28_edit": "add_leaf_private",
                "added_leaf_private_qubit": qubit,
                "added_leaf_private_offset": leaf_offset,
                "qubits": tuple(sorted(qubits | {qubit})),
                "description": (
                    f"Phase 28 leaf-private add variant of {base_region_spec['name']}: add leaf-cell qubit "
                    f"q{qubit} at local offset {leaf_offset}."
                ),
            }
        )
    return tuple(specs)


def holographic_phase28_region_payload(region_spec: dict[str, object]) -> dict[str, object]:
    payload = holographic_phase23_region_payload(region_spec)
    return {
        **payload,
        "phase28_edit": region_spec["phase28_edit"],
        "removed_root_qubit": region_spec["removed_root_qubit"],
        "removed_root_offset": region_spec["removed_root_offset"],
        "added_leaf_private_qubit": region_spec["added_leaf_private_qubit"],
        "added_leaf_private_offset": region_spec["added_leaf_private_offset"],
        "leaf_cell": region_spec["leaf_cell"],
    }


def holographic_phase28_leaf_private_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    base_region_spec: dict[str, object],
    leaf_private_spec: dict[str, object],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    generator_kind: str = "phase28_leaf_private_sentinel_region_grammar",
) -> dict[str, object]:
    base_region = holographic_phase23_region_payload(base_region_spec)
    base_mask = int(base_region["mask"])
    base_first_entropy = first.entropy(base_mask)
    base_second_entropy = second.entropy(base_mask)
    base_entropy_matches = base_first_entropy == base_second_entropy

    region = holographic_phase28_region_payload(leaf_private_spec)
    region_mask = int(region["mask"])
    min_cut_values = holographic_phase23_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=region_mask,
    )
    all_mincuts_exact = all(
        int(holographic_network_min_cut(network_spec=network, region_mask=region_mask)["assignments_checked"])
        == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
        for network in networks
    )
    first_entropy = first.entropy(region_mask)
    second_entropy = second.entropy(region_mask)
    entropy_matches = first_entropy == second_entropy
    hit = (
        holographic_phase7_hit_record(
            circuit={
                "name": str(region["name"]),
                "generator_kind": generator_kind,
            },
            first=first,
            second=second,
            network_spec=networks[0],
            region=region,
        )
        if entropy_matches
        else None
    )
    min_cut_variable = len({int(record["value"]) for record in min_cut_values}) > 1
    return {
        "base_region": {
            key: value
            for key, value in base_region.items()
            if key != "mask"
        },
        "base_entropy_pair": (base_first_entropy, base_second_entropy),
        "base_entropy_matches": base_entropy_matches,
        "region": {
            key: value
            for key, value in region.items()
            if key != "mask"
        },
        "leaf_cell": int(leaf_private_spec["leaf_cell"]),
        "removed_root_qubit": int(leaf_private_spec["removed_root_qubit"]),
        "removed_root_offset": int(leaf_private_spec["removed_root_offset"]),
        "added_leaf_private_qubit": int(leaf_private_spec["added_leaf_private_qubit"]),
        "added_leaf_private_offset": int(leaf_private_spec["added_leaf_private_offset"]),
        "entropy_pair": (first_entropy, second_entropy),
        "entropy_matches": entropy_matches,
        "operator_channel_checked": entropy_matches,
        "min_cut_values_by_capacity": min_cut_values,
        "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
        "min_cut_variable": min_cut_variable,
        "all_mincuts_exact": all_mincuts_exact,
        "hit": hit,
        "admissible_entropy_match_min_cut_operator_hit": bool(
            entropy_matches
            and min_cut_variable
            and hit is not None
            and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "strict_filter_stage": (
            "operator_channel_checked" if entropy_matches else "leaf_private_entropy_gate_rejected"
        ),
    }


def holographic_phase28_variant_record(
    *,
    spec: dict[str, object],
    base_outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
    layer_kind: str = "phase28_leaf_private_sentinel_region_grammar",
    generator_kind: str = "phase28_leaf_private_sentinel_region_grammar",
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in spec["gates"])  # type: ignore[index]
    outer = holographic_phase25_apply_outer_circuit(base_outer, gates)
    first, _ = logical_concatenate_k1(inner_first, outer)
    second, _ = logical_concatenate_k1(inner_second, outer)
    distance_audit = bounded_distance_certificate(outer, max_weight=3)

    records: list[dict[str, object]] = []
    base_entropy_passes = 0
    for base_region_spec in region_specs:
        base_region = holographic_phase23_region_payload(base_region_spec)
        if first.entropy(int(base_region["mask"])) != second.entropy(int(base_region["mask"])):
            continue
        base_entropy_passes += 1
        for leaf_private_spec in holographic_phase28_leaf_private_add_specs(base_region_spec):
            records.append(
                holographic_phase28_leaf_private_record(
                    first=first,
                    second=second,
                    base_region_spec=base_region_spec,
                    leaf_private_spec=leaf_private_spec,
                    networks=networks,
                    capacity_profiles=capacity_profiles,
                    generator_kind=generator_kind,
                )
            )
    record_tuple = tuple(records)
    operator_checked_records = tuple(record for record in record_tuple if record["operator_channel_checked"])
    admissible_hit_records = tuple(
        record for record in record_tuple if record["admissible_entropy_match_min_cut_operator_hit"]
    )
    summary = {
        "base_entropy_pass_records": base_entropy_passes,
        "candidate_leaf_private_records": len(record_tuple),
        "entropy_match_records": sum(1 for record in record_tuple if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in record_tuple if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "leaf_private_entropy_gate_rejections": sum(
            1 for record in record_tuple if not record["operator_channel_checked"]
        ),
        "min_cut_variable_records": sum(1 for record in record_tuple if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in operator_checked_records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in record_tuple),
    }
    return {
        "variant": {
            "name": spec["name"],
            "layer_kind": layer_kind,
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "gates": gates,
            "gate_count": len(gates),
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": distance_audit,
        },
        "code_pair": {"n": first.n, "k": first.k},
        "summary": summary,
        "records": record_tuple,
        "admissible_hit_records": admissible_hit_records,
    }


def bridge_holography_phase28_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 28 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    sentinel_names = holographic_phase28_sentinel_variant_names()
    variant_specs = tuple(
        spec
        for spec in holographic_phase26_offset_flip_neighborhood_specs()
        if str(spec["name"]) in sentinel_names
    )
    variant_records = tuple(
        holographic_phase28_variant_record(
            spec=spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
        )
        for spec in variant_specs
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    selected_entropy_matched_record = next(
        (
            record
            for variant in variant_records
            for record in variant["records"]  # type: ignore[index]
            if record["entropy_matches"]
        ),
        None,
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "interface_outer_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "leaf_private_sentinel_variants_scored": len(variant_specs) == 2
        and tuple(str(spec["name"]) for spec in variant_specs) == sentinel_names,
        "all_sentinel_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in variant_records
        ),
        "all_sentinel_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in variant_records
        ),
        "leaf_private_grammar_exhausted_for_sentinel_entropy_passes": sum(
            int(variant["summary"]["base_entropy_pass_records"]) for variant in variant_records  # type: ignore[index]
        )
        == 30
        and len(all_records) == 120,
        "all_leaf_private_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
        "all_leaf_private_records_entropy_match": all(record["entropy_matches"] for record in all_records),
        "all_leaf_private_records_min_cut_variable": all(record["min_cut_variable"] for record in all_records),
        "all_leaf_private_records_operator_checked": all(record["operator_channel_checked"] for record in all_records),
        "no_leaf_private_sentinel_admissible_hits": len(admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in operator_checked_records
        ),
    }
    phase_claims["goal_3_phase_28_leaf_private_sentinel_no_go_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 28: leaf-private sentinel region-grammar no-go",
        "status": "pass" if phase_claims["goal_3_phase_28_leaf_private_sentinel_no_go_certificate"] else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 27 second-root-hole region grammar",
            "sentinel_variants": sentinel_names,
            "region_grammar": (
                "For each entropy-passing base puncture in the two entropy-rich alternating offset-flip sentinel "
                "variants, add one leaf-private qubit at local offsets 0..3."
            ),
            "filter_order": (
                "exact base-puncture entropy gate",
                "generate all local leaf-private additions for sentinel variants",
                "exact entropy and exact min-cut variation for every leaf-private record",
                "exact algebra, erasure, and survivor checks for every entropy-matched leaf-private record",
            ),
        },
        "leaf_private_frontier": {
            "variant_records": variant_records,
            "selected_entropy_matched_record": selected_entropy_matched_record,
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "sentinel_variants": len(variant_records),
            "base_punctured_regions": len(region_specs),
            "base_entropy_pass_records": sum(
                int(variant["summary"]["base_entropy_pass_records"]) for variant in variant_records  # type: ignore[index]
            ),
            "candidate_leaf_private_records": len(all_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "leaf_private_entropy_gate_rejections": sum(
                1 for record in all_records if not record["operator_channel_checked"]
            ),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": sum(
                1
                for record in operator_checked_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "distance_three_witness_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The leaf-private sentinel audit scores the two entropy-rich alternating offset-flip branches from "
                "Phase 27. It adds one local leaf-private qubit to each entropy-passing puncture, producing 120 "
                "exact records. All 120 match entropy, all 120 remain capacity-sensitive, and all 120 have matching "
                "operator/channel semantics."
            ),
            "three_geometry_lesson": (
                "Leaf-private additions are entropy-rich rather than entropy-pruned: unlike the second-root-hole "
                "grammar, every sentinel leaf-private add passes the entropy gate. Even so, the reconstruction and "
                "channel diagnostics stay matched, so richer entropy/min-cut-visible patches still fail to recover "
                "a strict observer-visible split."
            ),
            "scope_warning": (
                "The search is a sentinel audit, not the full leaf-private grammar. It covers two alternating "
                "offset-flip variants and local leaf offsets 0..3; it does not exhaust all Phase 26 variants, "
                "arbitrary leaf additions, broader two-hole edits, or new inner/outer source pairings."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Both root-side two-hole edits and entropy-rich leaf-private sentinel edits preserve the no-go. "
                "The remaining likely escape routes are source changes or a broader region grammar with a cached "
                "operator-check layer."
            ),
            "suggested_phase_29": (
                "Change the inner/outer source pairing or add a cached full leaf-private grammar audit, then compare "
                "whether the obstruction is source-specific or region-grammar-wide."
            ),
        },
    }


def holographic_phase29_parent_summaries(
    variant_records: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    parents = tuple(dict.fromkeys(str(record["variant"]["parent"]) for record in variant_records))  # type: ignore[index]
    summaries: list[dict[str, object]] = []
    for parent in parents:
        selected = tuple(
            record for record in variant_records if str(record["variant"]["parent"]) == parent  # type: ignore[index]
        )
        summaries.append(
            {
                "parent": parent,
                "variants": len(selected),
                "base_entropy_pass_records": sum(
                    int(record["summary"]["base_entropy_pass_records"]) for record in selected  # type: ignore[index]
                ),
                "candidate_leaf_private_records": sum(
                    int(record["summary"]["candidate_leaf_private_records"]) for record in selected  # type: ignore[index]
                ),
                "entropy_match_records": sum(
                    int(record["summary"]["entropy_match_records"]) for record in selected  # type: ignore[index]
                ),
                "entropy_mismatch_records": sum(
                    int(record["summary"]["entropy_mismatch_records"]) for record in selected  # type: ignore[index]
                ),
                "operator_channel_checked_records": sum(
                    int(record["summary"]["operator_channel_checked_records"]) for record in selected  # type: ignore[index]
                ),
                "leaf_private_entropy_gate_rejections": sum(
                    int(record["summary"]["leaf_private_entropy_gate_rejections"]) for record in selected  # type: ignore[index]
                ),
                "min_cut_variable_records": sum(
                    int(record["summary"]["min_cut_variable_records"]) for record in selected  # type: ignore[index]
                ),
                "operator_or_channel_split_records": sum(
                    int(record["summary"]["operator_or_channel_split_records"]) for record in selected  # type: ignore[index]
                ),
                "admissible_entropy_match_min_cut_operator_hits": sum(
                    int(record["summary"]["admissible_entropy_match_min_cut_operator_hits"])  # type: ignore[index]
                    for record in selected
                ),
            }
        )
    return tuple(summaries)


def bridge_holography_phase29_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 29 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    variant_records = tuple(
        holographic_phase28_variant_record(
            spec=spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
            layer_kind="phase29_full_leaf_private_region_grammar",
            generator_kind="phase29_full_leaf_private_region_grammar",
        )
        for spec in variant_specs
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    parent_summaries = holographic_phase29_parent_summaries(variant_records)
    selected_entropy_matched_record = next(
        (
            record
            for variant in variant_records
            for record in variant["records"]  # type: ignore[index]
            if record["entropy_matches"]
        ),
        None,
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "interface_outer_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "offset_flip_neighborhood_reused": len(variant_specs) == 10 and len(variant_records) == 10,
        "all_neighbor_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in variant_records
        ),
        "all_neighbor_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in variant_records
        ),
        "full_leaf_private_grammar_exhausted_around_entropy_passes": sum(
            int(variant["summary"]["base_entropy_pass_records"]) for variant in variant_records  # type: ignore[index]
        )
        == 90
        and len(all_records) == 360
        and all(
            int(variant["summary"]["candidate_leaf_private_records"])  # type: ignore[index]
            == 4 * int(variant["summary"]["base_entropy_pass_records"])  # type: ignore[index]
            for variant in variant_records
        ),
        "all_full_leaf_private_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
        "all_full_leaf_private_records_entropy_match": len(all_records) == 360
        and all(record["entropy_matches"] for record in all_records),
        "all_full_leaf_private_records_min_cut_variable": all(
            record["min_cut_variable"] for record in all_records
        ),
        "all_full_leaf_private_records_operator_checked": len(operator_checked_records) == len(all_records)
        and all(record["operator_channel_checked"] for record in all_records),
        "no_full_leaf_private_admissible_hits": len(admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in operator_checked_records
        ),
    }
    phase_claims["goal_3_phase_29_full_leaf_private_region_grammar_no_go_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 29: full leaf-private region-grammar no-go",
        "status": "pass"
        if phase_claims["goal_3_phase_29_full_leaf_private_region_grammar_no_go_certificate"]
        else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phases 26 and 28 offset-flip plus leaf-private grammar",
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "region_grammar": (
                "For every Phase 26 base puncture that passes the entropy gate across all offset-flip variants, "
                "add one leaf-private qubit at local leaf offsets 0..3."
            ),
            "filter_order": (
                "exact base-puncture entropy gate",
                "generate all local leaf-private additions for all Phase 26 offset-flip variants",
                "exact entropy and exact min-cut variation for every leaf-private record",
                "exact algebra, erasure, and survivor checks for every entropy-matched leaf-private record",
            ),
        },
        "full_leaf_private_frontier": {
            "variant_records": variant_records,
            "parent_summaries": parent_summaries,
            "selected_entropy_matched_record": selected_entropy_matched_record,
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "offset_flip_variants": len(variant_records),
            "parent_circuits": len(parent_summaries),
            "base_punctured_regions": len(region_specs),
            "base_entropy_pass_records": sum(
                int(variant["summary"]["base_entropy_pass_records"]) for variant in variant_records  # type: ignore[index]
            ),
            "candidate_leaf_private_records": len(all_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "leaf_private_entropy_gate_rejections": sum(
                1 for record in all_records if not record["operator_channel_checked"]
            ),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": sum(
                1
                for record in operator_checked_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "distance_three_witness_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The full leaf-private grammar expands every Phase 26 entropy-passing puncture across all "
                "offset-flip variants. It scores 360 exact leaf-private records. All 360 match entropy, all 360 "
                "remain capacity-sensitive, and all 360 have matching operator/channel semantics."
            ),
            "three_geometry_lesson": (
                "The Phase 28 no-go was not a sentinel-selection artifact. Leaf-private additions are uniformly "
                "entropy-rich across the whole offset-flip neighborhood, but the reconstruction and channel "
                "diagnostics still do not split."
            ),
            "scope_warning": (
                "The search is exhaustive only for local leaf-private offsets 0..3 around Phase 26 "
                "entropy-passing records across the offset-flip neighborhood. It does not cover arbitrary leaf "
                "additions, changed bridge axes, changed inner sources, all Clifford/MERA circuits, or non-local "
                "region grammars."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The full local leaf-private grammar preserves the no-go, so the remaining obstruction is more "
                "likely tied to the inner/outer source pairing, bridge-axis choice, or a genuinely non-local "
                "region grammar."
            ),
            "suggested_phase_30": (
                "Run an outer bridge-axis/source-pairing audit over the same exact entropy, min-cut, algebra, "
                "erasure, and survivor checks."
            ),
        },
    }


def holographic_phase30_bridge_axes() -> tuple[str, ...]:
    return ("X", "Y", "Z")


def holographic_phase30_axis_record(
    *,
    bridge_axis: str,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
    variant_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    variant_records = tuple(
        holographic_phase26_variant_record(
            spec=spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
            audit_entropy_mismatch_near_hits=False,
        )
        for spec in variant_specs
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    parent_summaries = holographic_phase26_parent_summaries(variant_records)
    selected_entropy_matched_record = next((record for record in all_records if record["entropy_matches"]), None)
    summary = {
        "punctured_records": len(all_records),
        "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "entropy_gate_rejections": sum(1 for record in all_records if not record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in operator_checked_records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
        "distance_three_witness_variants": sum(
            1
            for variant in variant_records
            if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
    }
    return {
        "bridge_axis": bridge_axis,
        "source_pairing": {
            "inner_source": "goal3_phase2_graph_cws_ring_spoke_pair",
            "outer_family": "phase23_interface_star_outer_code",
            "logical_mapping": "logical_concatenate_k1 fixed inner logical Z/X mapping",
        },
        "outer_code": base_outer_summary,
        "summary": summary,
        "variant_records": variant_records,
        "parent_summaries": parent_summaries,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "admissible_hit_records": admissible_hits,
    }


def bridge_holography_phase30_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 30 source must contain StabilizerCode objects")

    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    bridge_axes = holographic_phase30_bridge_axes()
    axis_records = tuple(
        holographic_phase30_axis_record(
            bridge_axis=axis,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
            variant_specs=variant_specs,
        )
        for axis in bridge_axes
    )
    all_variant_records = tuple(
        variant for axis_record in axis_records for variant in axis_record["variant_records"]  # type: ignore[index]
    )
    all_records = tuple(record for variant in all_variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for axis_record in axis_records for record in axis_record["admissible_hit_records"]  # type: ignore[index]
    )
    axis_entropy_profile = {
        str(axis_record["bridge_axis"]): int(axis_record["summary"]["entropy_match_records"])  # type: ignore[index]
        for axis_record in axis_records
    }
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "single_source_pairing_loaded": inner_first.n == 5
        and inner_first.k == 1
        and inner_second.n == 5
        and inner_second.k == 1,
        "all_bridge_axes_scored": tuple(axis_entropy_profile) == bridge_axes and len(axis_records) == 3,
        "all_axis_outer_codes_are_n30_k1": all(
            axis_record["outer_code"]["parameters"] == {"n": 30, "k": 1} for axis_record in axis_records  # type: ignore[index]
        ),
        "all_axis_neighbor_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in all_variant_records
        ),
        "all_axis_neighbor_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in all_variant_records
        ),
        "axis_offset_flip_neighborhood_exhausted": len(all_variant_records) == 30
        and len(all_records) == 750
        and all(
            int(axis_record["summary"]["punctured_records"]) == 250  # type: ignore[index]
            for axis_record in axis_records
        ),
        "bridge_axis_changes_entropy_gate_profile": axis_entropy_profile == {"X": 30, "Y": 90, "Z": 45},
        "all_axis_punctured_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
        "all_axis_punctured_records_min_cut_variable": all(record["min_cut_variable"] for record in all_records),
        "all_axis_entropy_matches_operator_checked": len(operator_checked_records) == 165
        and all(record["operator_channel_checked"] for record in all_records if record["entropy_matches"]),
        "no_bridge_axis_admissible_hits": len(admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in operator_checked_records
        ),
    }
    phase_claims["goal_3_phase_30_bridge_axis_source_pairing_no_go_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 30: bridge-axis source-pairing entropy-gated no-go",
        "status": "pass"
        if phase_claims["goal_3_phase_30_bridge_axis_source_pairing_no_go_certificate"]
        else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 29 full leaf-private region grammar",
            "bridge_axes": bridge_axes,
            "source_pairings": (
                {
                    "name": "phase2_graph_cws_pair_with_fixed_logical_concatenation",
                    "inner_code_parameters": {"n": inner_first.n, "k": inner_first.k},
                    "outer_code_family": "phase23_interface_star_outer_code",
                    "logical_mapping": "fixed logical_concatenate_k1 inner logical Z/X mapping",
                },
            ),
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "region_frontier": (
                "Replay the Phase 26 offset-flip entropy-gated punctured frontier for bridge axes X, Y, and Z."
            ),
            "filter_order": (
                "construct a Phase 23 interface-star outer code for each bridge axis",
                "apply every Phase 26 offset-flip circuit to each axis-specific outer code",
                "score all 25 Phase 24 punctured regions for exact entropy and exact min-cut variation",
                "run exact algebra, erasure, and survivor checks on entropy-matched records",
                "count entropy-rejected records without operator/channel near-hit auditing",
            ),
        },
        "axis_source_pairing_frontier": {
            "axis_records": axis_records,
            "axis_entropy_profile": axis_entropy_profile,
            "selected_entropy_matched_records": tuple(
                {
                    "bridge_axis": axis_record["bridge_axis"],
                    "record": axis_record["selected_entropy_matched_record"],
                }
                for axis_record in axis_records
            ),
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "bridge_axes": len(axis_records),
            "source_pairings": 1,
            "offset_flip_variants_per_axis": len(variant_specs),
            "axis_variant_records": len(all_variant_records),
            "base_punctured_regions": len(region_specs),
            "candidate_punctured_records": len(all_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "entropy_gate_rejections": sum(1 for record in all_records if not record["operator_channel_checked"]),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": sum(
                1
                for record in operator_checked_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "distance_three_witness_axis_variants": sum(
                1
                for variant in all_variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "axis_entropy_match_profile": axis_entropy_profile,
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The bridge-axis audit replays the Phase 26 punctured frontier for X, Y, and Z interface-star "
                "bridge axes using the fixed Phase 2 source pair. Axis choice changes the entropy gate profile: "
                "X has 30 matched records, Y has 90, and Z has 45. All 165 entropy-matched records receive exact "
                "operator/channel checks, and none is an admissible split."
            ),
            "three_geometry_lesson": (
                "Bridge-axis choice is visible to the entropy/min-cut frontier, but it still does not align the "
                "entropy-visible and reconstruction/channel-visible geometries on the same certified punctured "
                "regions."
            ),
            "scope_warning": (
                "The audit covers one fixed Phase 2 source pair, the fixed logical_concatenate_k1 logical-basis "
                "mapping, bridge axes X/Y/Z, the Phase 26 offset-flip circuits, and the 25 Phase 24 punctured "
                "regions. It does not audit entropy-mismatched operator near-hits, full leaf-private grammars for "
                "X/Z axes, arbitrary source pairs, logical-basis twists, or non-local region grammars."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Axis-only source pairing changes entropy counts but does not create a strict holographic cousin. "
                "The next likely lever is a genuine source/logical-basis pairing change rather than another local "
                "axis replay."
            ),
            "suggested_phase_31": (
                "Audit logical-basis twists or alternative Phase 2 graph/CWS source pairs under the same exact "
                "entropy, min-cut, algebra, erasure, and survivor checks; optionally include entropy-mismatch "
                "near-hit auditing to guide the source-pair search."
            ),
        },
    }


def holographic_phase31_logical_label_rows(code: StabilizerCode) -> dict[str, int]:
    logical_z, logical_x = code.logical_basis
    return {"Z": logical_z, "X": logical_x, "Y": logical_z ^ logical_x}


def holographic_phase31_shared_twist_specs() -> tuple[dict[str, object], ...]:
    labels = ("Z", "X", "Y")
    return tuple(
        {
            "name": f"{logical_z_label}_as_Z__{logical_x_label}_as_X",
            "twist_kind": "shared_inner_logical_basis_twist",
            "inner_logical_z_label": logical_z_label,
            "inner_logical_x_label": logical_x_label,
            "description": (
                f"Use inner logical {logical_z_label} as the concatenation Z row and inner logical "
                f"{logical_x_label} as the concatenation X row for both members of the Phase 2 source pair."
            ),
        }
        for logical_z_label in labels
        for logical_x_label in labels
        if logical_z_label != logical_x_label
    )


def holographic_phase31_logical_concatenate_k1_with_basis(
    inner: StabilizerCode,
    outer: StabilizerCode,
    *,
    inner_logical_z: int,
    inner_logical_x: int,
) -> tuple[StabilizerCode, dict[str, object]]:
    if inner.k != 1 or outer.k != 1:
        raise ValueError("twisted logical concatenation requires k=1 inner and outer codes")
    if not symplectic_product(inner_logical_z, inner_logical_x, inner.n):
        raise ValueError("twisted inner logical rows must anticommute")
    block_size = inner.n
    block_count = outer.n
    rows: list[int] = []
    for block in range(block_count):
        for generator in inner.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=block_size, block_count=block_count))
    encoded_outer_rows: list[int] = []
    for outer_generator in outer.generators:
        row = 0
        x = outer_generator & ((1 << outer.n) - 1)
        z = outer_generator >> outer.n
        for block in range(block_count):
            if (x >> block) & 1:
                row ^= block_shift_pauli(inner_logical_x, block=block, block_size=block_size, block_count=block_count)
            if (z >> block) & 1:
                row ^= block_shift_pauli(inner_logical_z, block=block, block_size=block_size, block_count=block_count)
        rows.append(row)
        encoded_outer_rows.append(row)
    code = StabilizerCode(block_size * block_count, rows)
    return code, {
        "inner_logical_z": pauli_to_string(inner_logical_z, inner.n),
        "inner_logical_x": pauli_to_string(inner_logical_x, inner.n),
        "outer_generators": outer.pauli_generators(),
        "encoded_outer_generators_unreduced": tuple(pauli_to_string(row, code.n) for row in encoded_outer_rows),
        "block_size": block_size,
        "block_count": block_count,
    }


def holographic_phase31_variant_record(
    *,
    twist_spec: dict[str, object],
    spec: dict[str, object],
    base_outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    gates = tuple(tuple(gate) for gate in spec["gates"])  # type: ignore[index]
    outer = holographic_phase25_apply_outer_circuit(base_outer, gates)
    logical_z_label = str(twist_spec["inner_logical_z_label"])
    logical_x_label = str(twist_spec["inner_logical_x_label"])
    first_label_rows = holographic_phase31_logical_label_rows(inner_first)
    second_label_rows = holographic_phase31_logical_label_rows(inner_second)
    first, first_metadata = holographic_phase31_logical_concatenate_k1_with_basis(
        inner_first,
        outer,
        inner_logical_z=first_label_rows[logical_z_label],
        inner_logical_x=first_label_rows[logical_x_label],
    )
    second, second_metadata = holographic_phase31_logical_concatenate_k1_with_basis(
        inner_second,
        outer,
        inner_logical_z=second_label_rows[logical_z_label],
        inner_logical_x=second_label_rows[logical_x_label],
    )
    distance_audit = bounded_distance_certificate(outer, max_weight=3)
    records = tuple(
        holographic_phase26_entropy_gated_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
            audit_entropy_mismatch_near_hits=False,
        )
        for region in region_specs
    )
    admissible_hit_records = tuple(
        record for record in records if record["admissible_entropy_match_min_cut_operator_hit"]
    )
    operator_checked_records = tuple(record for record in records if record["operator_channel_checked"])
    summary = {
        "punctured_records": len(records),
        "entropy_match_records": sum(1 for record in records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in records if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "entropy_gate_rejections": sum(1 for record in records if not record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in records if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in operator_checked_records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "entropy_mismatch_operator_near_hits": None,
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in records),
    }
    return {
        "variant": {
            "name": f"{twist_spec['name']}__{spec['name']}",
            "phase26_variant_name": spec["name"],
            "layer_kind": "phase31_shared_logical_basis_twist_frontier",
            "description": spec["description"],
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "twist_name": twist_spec["name"],
            "inner_logical_z_label": logical_z_label,
            "inner_logical_x_label": logical_x_label,
            "gates": gates,
            "gate_count": len(gates),
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": distance_audit,
        },
        "code_pair": {"n": first.n, "k": first.k},
        "twisted_concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "summary": summary,
        "records": records,
        "admissible_hit_records": admissible_hit_records,
        "near_hit_records": (),
    }


def holographic_phase31_twist_record(
    *,
    twist_spec: dict[str, object],
    base_outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
    variant_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    variant_records = tuple(
        holographic_phase31_variant_record(
            twist_spec=twist_spec,
            spec=spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
        )
        for spec in variant_specs
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    parent_summaries = holographic_phase26_parent_summaries(variant_records)
    selected_entropy_matched_record = next((record for record in all_records if record["entropy_matches"]), None)
    summary = {
        "punctured_records": len(all_records),
        "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "entropy_gate_rejections": sum(1 for record in all_records if not record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in operator_checked_records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
        "distance_three_witness_variants": sum(
            1
            for variant in variant_records
            if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
    }
    first_label_rows = holographic_phase31_logical_label_rows(inner_first)
    second_label_rows = holographic_phase31_logical_label_rows(inner_second)
    logical_z_label = str(twist_spec["inner_logical_z_label"])
    logical_x_label = str(twist_spec["inner_logical_x_label"])
    return {
        "twist": {
            **twist_spec,
            "first_inner_logical_z": pauli_to_string(first_label_rows[logical_z_label], inner_first.n),
            "first_inner_logical_x": pauli_to_string(first_label_rows[logical_x_label], inner_first.n),
            "second_inner_logical_z": pauli_to_string(second_label_rows[logical_z_label], inner_second.n),
            "second_inner_logical_x": pauli_to_string(second_label_rows[logical_x_label], inner_second.n),
            "first_symplectic_pair": bool(
                symplectic_product(first_label_rows[logical_z_label], first_label_rows[logical_x_label], inner_first.n)
            ),
            "second_symplectic_pair": bool(
                symplectic_product(
                    second_label_rows[logical_z_label], second_label_rows[logical_x_label], inner_second.n
                )
            ),
        },
        "summary": summary,
        "variant_records": variant_records,
        "parent_summaries": parent_summaries,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "admissible_hit_records": admissible_hits,
    }


def bridge_holography_phase31_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 31 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    twist_specs = holographic_phase31_shared_twist_specs()
    twist_records = tuple(
        holographic_phase31_twist_record(
            twist_spec=twist_spec,
            base_outer=base_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
            variant_specs=variant_specs,
        )
        for twist_spec in twist_specs
    )
    all_variant_records = tuple(
        variant for twist_record in twist_records for variant in twist_record["variant_records"]  # type: ignore[index]
    )
    all_records = tuple(record for variant in all_variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for twist_record in twist_records for record in twist_record["admissible_hit_records"]  # type: ignore[index]
    )
    twist_entropy_profile = {
        str(twist_record["twist"]["name"]): int(twist_record["summary"]["entropy_match_records"])  # type: ignore[index]
        for twist_record in twist_records
    }
    expected_twist_entropy_profile = {
        "Z_as_Z__X_as_X": 90,
        "Z_as_Z__Y_as_X": 90,
        "X_as_Z__Z_as_X": 55,
        "X_as_Z__Y_as_X": 0,
        "Y_as_Z__Z_as_X": 55,
        "Y_as_Z__X_as_X": 0,
    }
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "bridge_axis_y_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "all_shared_logical_basis_twists_scored": len(twist_specs) == 6
        and len(twist_records) == 6
        and all(record["twist"]["first_symplectic_pair"] for record in twist_records)  # type: ignore[index]
        and all(record["twist"]["second_symplectic_pair"] for record in twist_records),  # type: ignore[index]
        "all_twist_neighbor_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in all_variant_records
        ),
        "all_twist_neighbor_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in all_variant_records
        ),
        "twist_offset_flip_frontier_exhausted": len(all_variant_records) == 60
        and len(all_records) == 1500
        and all(
            int(twist_record["summary"]["punctured_records"]) == 250  # type: ignore[index]
            for twist_record in twist_records
        ),
        "logical_basis_twists_change_entropy_gate_profile": twist_entropy_profile == expected_twist_entropy_profile,
        "all_twist_punctured_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
        "all_twist_punctured_records_min_cut_variable": all(record["min_cut_variable"] for record in all_records),
        "all_twist_entropy_matches_operator_checked": len(operator_checked_records) == 290
        and all(record["operator_channel_checked"] for record in all_records if record["entropy_matches"]),
        "no_shared_logical_twist_admissible_hits": len(admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in operator_checked_records
        ),
    }
    phase_claims["goal_3_phase_31_shared_logical_basis_twist_no_go_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 31: shared logical-basis twist entropy-gated no-go",
        "status": "pass"
        if phase_claims["goal_3_phase_31_shared_logical_basis_twist_no_go_certificate"]
        else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 30 bridge-axis source-pairing audit",
            "bridge_axis": bridge_axis,
            "logical_basis_twists": twist_specs,
            "source_pairings": (
                {
                    "name": "phase2_graph_cws_pair_with_shared_inner_logical_basis_twist",
                    "inner_code_parameters": {"n": inner_first.n, "k": inner_first.k},
                    "outer_code_family": "phase23_interface_star_outer_code",
                    "twist_space": "all six ordered shared k=1 logical bases from {Z, X, Y=Z+X}",
                },
            ),
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "region_frontier": (
                "Replay the Phase 26 offset-flip entropy-gated punctured frontier for each shared logical-basis "
                "twist on the Y bridge axis."
            ),
            "filter_order": (
                "construct the Phase 23 interface-star outer code with bridge axis Y",
                "for each shared logical-basis twist, concatenate both Phase 2 source codes with explicit inner rows",
                "apply every Phase 26 offset-flip circuit to the outer code",
                "score all 25 Phase 24 punctured regions for exact entropy and exact min-cut variation",
                "run exact algebra, erasure, and survivor checks on entropy-matched records",
                "count entropy-rejected records without operator/channel near-hit auditing",
            ),
        },
        "shared_logical_twist_frontier": {
            "twist_records": twist_records,
            "twist_entropy_profile": twist_entropy_profile,
            "selected_entropy_matched_records": tuple(
                {
                    "twist": twist_record["twist"]["name"],  # type: ignore[index]
                    "record": twist_record["selected_entropy_matched_record"],
                }
                for twist_record in twist_records
            ),
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "shared_logical_basis_twists": len(twist_records),
            "bridge_axes": 1,
            "source_pairings": 1,
            "offset_flip_variants_per_twist": len(variant_specs),
            "twist_variant_records": len(all_variant_records),
            "base_punctured_regions": len(region_specs),
            "candidate_punctured_records": len(all_records),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "entropy_gate_rejections": sum(1 for record in all_records if not record["operator_channel_checked"]),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": sum(
                1
                for record in operator_checked_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "distance_three_witness_twist_variants": sum(
                1
                for variant in all_variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "twist_entropy_match_profile": twist_entropy_profile,
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The shared logical-basis twist audit replays the Phase 26 punctured frontier for all six ordered "
                "shared k=1 inner logical bases on the Y bridge axis. The entropy gate profile changes to "
                "90, 90, 55, 0, 55, and 0 matched records. All 290 entropy-matched records receive exact "
                "operator/channel checks, and none is an admissible split."
            ),
            "three_geometry_lesson": (
                "Logical-basis pairing is visible to the entropy/min-cut frontier, but the shared twists still do "
                "not align entropy-visible and reconstruction/channel-visible geometries on the same certified "
                "punctured regions."
            ),
            "scope_warning": (
                "The audit covers shared logical-basis twists only: both members of the Phase 2 source pair use the "
                "same ordered logical labels. It fixes bridge axis Y, the Phase 26 offset-flip circuits, and the 25 "
                "Phase 24 punctured regions. It does not cover independent first/second twists, alternative graph/CWS "
                "source pairs, entropy-mismatched near-hit auditing, full leaf-private grammars for every twist, or "
                "non-local region grammars."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Shared logical-basis twists change entropy support but preserve the no-go. The next lever should "
                "break the shared-twist symmetry or change the source pair itself."
            ),
            "suggested_phase_32": (
                "Audit independent first/second logical-basis twists or a bounded set of alternative Phase 2 graph/CWS "
                "source pairs, using entropy-mismatch near-hit auditing to prioritize expensive semantic checks."
            ),
        },
    }


def holographic_phase32_independent_twist_pair_specs() -> tuple[dict[str, object], ...]:
    twist_specs = holographic_phase31_shared_twist_specs()
    return tuple(
        {
            "name": f"first_{first['name']}__second_{second['name']}",
            "pair_kind": "independent_inner_logical_basis_twist_pair",
            "first_twist": first,
            "second_twist": second,
            "description": (
                f"Use {first['name']} for the first Phase 2 source code and {second['name']} for the second "
                "Phase 2 source code."
            ),
        }
        for first in twist_specs
        for second in twist_specs
    )


def holographic_phase32_priority_pair_specs() -> tuple[dict[str, object], ...]:
    by_name = {str(spec["name"]): spec for spec in holographic_phase31_shared_twist_specs()}
    choices = (
        (
            "shared_high",
            "Z_as_Z__X_as_X",
            "Z_as_Z__X_as_X",
            "Shared baseline high-entropy profile inherited from Phase 31.",
        ),
        (
            "offdiag_high",
            "X_as_Z__Y_as_X",
            "Z_as_Z__X_as_X",
            "Off-diagonal first twist with the high-entropy second twist profile.",
        ),
        (
            "shared_medium",
            "X_as_Z__Z_as_X",
            "X_as_Z__Z_as_X",
            "Shared medium-entropy profile inherited from Phase 31.",
        ),
        (
            "offdiag_medium",
            "Z_as_Z__X_as_X",
            "X_as_Z__Z_as_X",
            "Off-diagonal first twist with the medium-entropy second twist profile.",
        ),
    )
    return tuple(
        {
            "priority_label": label,
            "name": f"first_{first_name}__second_{second_name}",
            "pair_kind": "phase32_priority_independent_twist_pair",
            "first_twist": by_name[first_name],
            "second_twist": by_name[second_name],
            "selection_reason": reason,
        }
        for label, first_name, second_name, reason in choices
    )


def holographic_phase32_expected_pair_entropy_profile() -> dict[str, int]:
    second_profile = {
        "Z_as_Z__X_as_X": 90,
        "Z_as_Z__Y_as_X": 90,
        "X_as_Z__Z_as_X": 55,
        "X_as_Z__Y_as_X": 0,
        "Y_as_Z__Z_as_X": 55,
        "Y_as_Z__X_as_X": 0,
    }
    return {
        str(pair_spec["name"]): second_profile[str(pair_spec["second_twist"]["name"])]  # type: ignore[index]
        for pair_spec in holographic_phase32_independent_twist_pair_specs()
    }


def holographic_phase32_code_pair_for_twists(
    *,
    first_twist: dict[str, object],
    second_twist: dict[str, object],
    outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
) -> tuple[StabilizerCode, StabilizerCode, dict[str, object]]:
    first_rows = holographic_phase31_logical_label_rows(inner_first)
    second_rows = holographic_phase31_logical_label_rows(inner_second)
    first_z_label = str(first_twist["inner_logical_z_label"])
    first_x_label = str(first_twist["inner_logical_x_label"])
    second_z_label = str(second_twist["inner_logical_z_label"])
    second_x_label = str(second_twist["inner_logical_x_label"])
    first, first_metadata = holographic_phase31_logical_concatenate_k1_with_basis(
        inner_first,
        outer,
        inner_logical_z=first_rows[first_z_label],
        inner_logical_x=first_rows[first_x_label],
    )
    second, second_metadata = holographic_phase31_logical_concatenate_k1_with_basis(
        inner_second,
        outer,
        inner_logical_z=second_rows[second_z_label],
        inner_logical_x=second_rows[second_x_label],
    )
    return first, second, {
        "first": first_metadata,
        "second": second_metadata,
        "first_twist_name": first_twist["name"],
        "second_twist_name": second_twist["name"],
        "first_inner_logical_z_label": first_z_label,
        "first_inner_logical_x_label": first_x_label,
        "second_inner_logical_z_label": second_z_label,
        "second_inner_logical_x_label": second_x_label,
    }


def holographic_phase32_outer_variant_cache(
    *,
    base_outer: StabilizerCode,
    variant_specs: tuple[dict[str, object], ...],
) -> dict[str, dict[str, object]]:
    cache: dict[str, dict[str, object]] = {}
    for spec in variant_specs:
        gates = tuple(tuple(gate) for gate in spec["gates"])  # type: ignore[index]
        outer = holographic_phase25_apply_outer_circuit(base_outer, gates)
        cache[str(spec["name"])] = {
            "spec": spec,
            "gates": gates,
            "outer": outer,
            "distance_audit_weight3": bounded_distance_certificate(outer, max_weight=3),
        }
    return cache


def holographic_phase32_region_mincut_cache(
    *,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, dict[str, object]]:
    cache: dict[str, dict[str, object]] = {}
    for region_spec in region_specs:
        region = holographic_phase23_region_payload(region_spec)
        min_cut_values = holographic_phase23_mincut_values(
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_mask=int(region["mask"]),
        )
        all_mincuts_exact = all(
            int(holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))["assignments_checked"])
            == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
            for network in networks
        )
        cache[str(region["name"])] = {
            "region": {key: value for key, value in region.items() if key != "mask"},
            "mask": int(region["mask"]),
            "min_cut_values_by_capacity": min_cut_values,
            "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
            "min_cut_variable": len({int(record["value"]) for record in min_cut_values}) > 1,
            "all_mincuts_exact": all_mincuts_exact,
        }
    return cache


def holographic_phase32_pair_atlas_record(
    *,
    pair_spec: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    outer_variant_cache: dict[str, dict[str, object]],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    variant_summaries: list[dict[str, object]] = []
    selected_entropy_matched_record: dict[str, object] | None = None
    for variant_name, cached_outer in outer_variant_cache.items():
        spec = cached_outer["spec"]
        outer = cached_outer["outer"]
        if not isinstance(spec, dict) or not isinstance(outer, StabilizerCode):
            raise TypeError("Phase 32 outer cache is malformed")
        first, second, _metadata = holographic_phase32_code_pair_for_twists(
            first_twist=pair_spec["first_twist"],  # type: ignore[arg-type]
            second_twist=pair_spec["second_twist"],  # type: ignore[arg-type]
            outer=outer,
            inner_first=inner_first,
            inner_second=inner_second,
        )
        entropy_match_records = 0
        entropy_mismatch_records = 0
        min_cut_variable_records = 0
        all_mincuts_exact = True
        for region_spec in region_specs:
            region = holographic_phase23_region_payload(region_spec)
            mincut = region_mincut_cache[str(region["name"])]
            first_entropy = first.entropy(int(region["mask"]))
            second_entropy = second.entropy(int(region["mask"]))
            entropy_matches = first_entropy == second_entropy
            entropy_match_records += 1 if entropy_matches else 0
            entropy_mismatch_records += 0 if entropy_matches else 1
            min_cut_variable_records += 1 if mincut["min_cut_variable"] else 0
            all_mincuts_exact = all_mincuts_exact and bool(mincut["all_mincuts_exact"])
            if entropy_matches and selected_entropy_matched_record is None:
                selected_entropy_matched_record = {
                    "variant": {
                        "name": variant_name,
                        "parent": spec["parent"],
                        "flipped_offset": spec["flipped_offset"],
                        "to_direction": spec["to_direction"],
                    },
                    "region": mincut["region"],
                    "entropy_pair": (first_entropy, second_entropy),
                    "min_cut_values": mincut["min_cut_values"],
                    "min_cut_variable": mincut["min_cut_variable"],
                    "all_mincuts_exact": mincut["all_mincuts_exact"],
                }
        variant_summaries.append(
            {
                "variant": {
                    "name": variant_name,
                    "parent": spec["parent"],
                    "mutation_kind": spec["mutation_kind"],
                    "flipped_offset": spec["flipped_offset"],
                    "to_direction": spec["to_direction"],
                    "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
                },
                "code_pair": {"n": first.n, "k": first.k},
                "outer_distance_audit_weight3": cached_outer["distance_audit_weight3"],
                "summary": {
                    "punctured_records": len(region_specs),
                    "entropy_match_records": entropy_match_records,
                    "entropy_mismatch_records": entropy_mismatch_records,
                    "operator_channel_checked_records": 0,
                    "semantic_audit_deferred_records": entropy_match_records,
                    "min_cut_variable_records": min_cut_variable_records,
                    "all_mincuts_exact": all_mincuts_exact,
                },
            }
        )
    summary = {
        "punctured_records": sum(int(record["summary"]["punctured_records"]) for record in variant_summaries),  # type: ignore[index]
        "entropy_match_records": sum(
            int(record["summary"]["entropy_match_records"]) for record in variant_summaries  # type: ignore[index]
        ),
        "entropy_mismatch_records": sum(
            int(record["summary"]["entropy_mismatch_records"]) for record in variant_summaries  # type: ignore[index]
        ),
        "operator_channel_checked_records": 0,
        "semantic_audit_deferred_records": sum(
            int(record["summary"]["semantic_audit_deferred_records"]) for record in variant_summaries  # type: ignore[index]
        ),
        "min_cut_variable_records": sum(
            int(record["summary"]["min_cut_variable_records"]) for record in variant_summaries  # type: ignore[index]
        ),
        "all_mincuts_exact": all(record["summary"]["all_mincuts_exact"] for record in variant_summaries),  # type: ignore[index]
    }
    return {
        "pair": {
            "name": pair_spec["name"],
            "pair_kind": pair_spec["pair_kind"],
            "first_twist": pair_spec["first_twist"],
            "second_twist": pair_spec["second_twist"],
        },
        "summary": summary,
        "variant_summaries": tuple(variant_summaries),
        "selected_entropy_matched_record": selected_entropy_matched_record,
    }


def holographic_phase32_priority_variant_record(
    *,
    pair_spec: dict[str, object],
    spec: dict[str, object],
    cached_outer: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    outer = cached_outer["outer"]
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 32 outer cache is malformed")
    first, second, metadata = holographic_phase32_code_pair_for_twists(
        first_twist=pair_spec["first_twist"],  # type: ignore[arg-type]
        second_twist=pair_spec["second_twist"],  # type: ignore[arg-type]
        outer=outer,
        inner_first=inner_first,
        inner_second=inner_second,
    )
    records = tuple(
        holographic_phase26_entropy_gated_record(
            first=first,
            second=second,
            region_spec=region,
            networks=networks,
            capacity_profiles=capacity_profiles,
            audit_entropy_mismatch_near_hits=False,
        )
        for region in region_specs
    )
    operator_checked_records = tuple(record for record in records if record["operator_channel_checked"])
    admissible_hit_records = tuple(
        record for record in records if record["admissible_entropy_match_min_cut_operator_hit"]
    )
    summary = {
        "punctured_records": len(records),
        "entropy_match_records": sum(1 for record in records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in records if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "entropy_gate_rejections": sum(1 for record in records if not record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in records if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in operator_checked_records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "entropy_mismatch_operator_near_hits": None,
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in records),
    }
    return {
        "variant": {
            "name": f"{pair_spec['name']}__{spec['name']}",
            "phase26_variant_name": spec["name"],
            "layer_kind": "phase32_independent_logical_basis_priority_semantic_audit",
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "priority_label": pair_spec["priority_label"],
            "first_twist_name": pair_spec["first_twist"]["name"],  # type: ignore[index]
            "second_twist_name": pair_spec["second_twist"]["name"],  # type: ignore[index]
            "gates": cached_outer["gates"],
            "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": cached_outer["distance_audit_weight3"],
        },
        "code_pair": {"n": first.n, "k": first.k},
        "twisted_concatenation": metadata,
        "summary": summary,
        "records": records,
        "admissible_hit_records": admissible_hit_records,
        "near_hit_records": (),
    }


def holographic_phase32_priority_pair_record(
    *,
    pair_spec: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    outer_variant_cache: dict[str, dict[str, object]],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    variant_records = tuple(
        holographic_phase32_priority_variant_record(
            pair_spec=pair_spec,
            spec=cached_outer["spec"],  # type: ignore[arg-type]
            cached_outer=cached_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
        )
        for cached_outer in outer_variant_cache.values()
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    parent_summaries = holographic_phase26_parent_summaries(variant_records)
    selected_entropy_matched_record = next((record for record in all_records if record["entropy_matches"]), None)
    summary = {
        "punctured_records": len(all_records),
        "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "entropy_gate_rejections": sum(1 for record in all_records if not record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
        "operator_or_channel_split_records": sum(
            1
            for record in operator_checked_records
            if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
        "distance_three_witness_variants": sum(
            1
            for variant in variant_records
            if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
    }
    return {
        "priority_pair": {
            "name": pair_spec["name"],
            "priority_label": pair_spec["priority_label"],
            "selection_reason": pair_spec["selection_reason"],
            "first_twist": pair_spec["first_twist"],
            "second_twist": pair_spec["second_twist"],
        },
        "summary": summary,
        "variant_records": variant_records,
        "parent_summaries": parent_summaries,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "admissible_hit_records": admissible_hits,
    }


def bridge_holography_phase32_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 32 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=variant_specs)
    region_mincut_cache = holographic_phase32_region_mincut_cache(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_specs=region_specs,
    )
    pair_specs = holographic_phase32_independent_twist_pair_specs()
    priority_pair_specs = holographic_phase32_priority_pair_specs()
    pair_atlas_records = tuple(
        holographic_phase32_pair_atlas_record(
            pair_spec=pair_spec,
            inner_first=inner_first,
            inner_second=inner_second,
            outer_variant_cache=outer_variant_cache,
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for pair_spec in pair_specs
    )
    priority_pair_records = tuple(
        holographic_phase32_priority_pair_record(
            pair_spec=pair_spec,
            inner_first=inner_first,
            inner_second=inner_second,
            outer_variant_cache=outer_variant_cache,
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_specs=region_specs,
        )
        for pair_spec in priority_pair_specs
    )
    pair_entropy_profile = {
        str(record["pair"]["name"]): int(record["summary"]["entropy_match_records"])  # type: ignore[index]
        for record in pair_atlas_records
    }
    expected_pair_entropy_profile = holographic_phase32_expected_pair_entropy_profile()
    all_priority_records = tuple(
        record for pair in priority_pair_records for variant in pair["variant_records"] for record in variant["records"]  # type: ignore[index]
    )
    priority_operator_checked_records = tuple(
        record for record in all_priority_records if record["operator_channel_checked"]
    )
    priority_admissible_hits = tuple(
        record for pair in priority_pair_records for record in pair["admissible_hit_records"]  # type: ignore[index]
    )
    profile_distribution = {
        count: sum(1 for value in pair_entropy_profile.values() if value == count)
        for count in sorted(set(pair_entropy_profile.values()))
    }
    priority_profile = {
        str(record["priority_pair"]["priority_label"]): int(record["summary"]["entropy_match_records"])  # type: ignore[index]
        for record in priority_pair_records
    }
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "bridge_axis_y_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "all_independent_logical_basis_pairs_scored": len(pair_specs) == 36 and len(pair_atlas_records) == 36,
        "all_priority_pairs_semantically_scored": len(priority_pair_records) == 4
        and priority_profile == {"shared_high": 90, "offdiag_high": 90, "shared_medium": 55, "offdiag_medium": 55},
        "independent_twist_entropy_mincut_atlas_exhausted": len(pair_atlas_records) == 36
        and sum(int(record["summary"]["punctured_records"]) for record in pair_atlas_records) == 9000,  # type: ignore[index]
        "independent_twist_entropy_profile_matches_scout": pair_entropy_profile == expected_pair_entropy_profile
        and profile_distribution == {0: 12, 55: 12, 90: 12},
        "all_atlas_punctured_mincuts_exact": all(
            record["summary"]["all_mincuts_exact"] for record in pair_atlas_records  # type: ignore[index]
        ),
        "all_atlas_punctured_records_min_cut_variable": sum(
            int(record["summary"]["min_cut_variable_records"]) for record in pair_atlas_records  # type: ignore[index]
        )
        == 9000,
        "priority_entropy_matches_operator_checked": len(priority_operator_checked_records) == 290
        and all(record["operator_channel_checked"] for record in all_priority_records if record["entropy_matches"]),
        "no_priority_independent_twist_admissible_hits": len(priority_admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in priority_operator_checked_records
        ),
    }
    phase_claims["goal_3_phase_32_independent_logical_basis_twist_priority_certificate"] = all(
        phase_claims.values()
    )
    total_entropy_matches = sum(int(record["summary"]["entropy_match_records"]) for record in pair_atlas_records)  # type: ignore[index]
    priority_entropy_matches = len(priority_operator_checked_records)
    return {
        "phase": "Goal 3 Phase 32: independent logical-basis twist atlas and priority semantic audit",
        "status": "pass"
        if phase_claims["goal_3_phase_32_independent_logical_basis_twist_priority_certificate"]
        else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
            "region_mincut_cache": {
                key: {subkey: value for subkey, value in record.items() if subkey != "mask"}
                for key, record in region_mincut_cache.items()
            },
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 31 shared logical-basis twist audit",
            "bridge_axis": bridge_axis,
            "independent_twist_pairs": tuple(pair_specs),
            "priority_semantic_pairs": priority_pair_specs,
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "region_frontier": (
                "Replay the Phase 26 offset-flip punctured frontier for all 36 independent first/second "
                "logical-basis twist pairs on the Y bridge axis."
            ),
            "filter_order": (
                "construct the Phase 23 interface-star outer code with bridge axis Y",
                "score exact entropy and cached exact min-cut variation for all 36 independent twist pairs",
                "select shared/off-diagonal high and medium entropy-profile representatives",
                "run exact algebra, erasure, and survivor checks on entropy-matched priority records",
                "defer semantic checks for non-priority entropy-matched records",
            ),
        },
        "independent_twist_frontier": {
            "pair_atlas_records": pair_atlas_records,
            "pair_entropy_profile": pair_entropy_profile,
            "profile_distribution": profile_distribution,
            "priority_pair_records": priority_pair_records,
            "priority_pair_profile": priority_profile,
            "priority_admissible_hit_records": priority_admissible_hits,
            "semantic_audit_deferred_entropy_match_records": total_entropy_matches - priority_entropy_matches,
        },
        "counts": {
            "independent_twist_pairs": len(pair_atlas_records),
            "first_twists": 6,
            "second_twists": 6,
            "bridge_axes": 1,
            "source_pairings": 1,
            "offset_flip_variants_per_pair": len(variant_specs),
            "independent_pair_variant_records": len(pair_atlas_records) * len(variant_specs),
            "base_punctured_regions": len(region_specs),
            "candidate_punctured_records": sum(
                int(record["summary"]["punctured_records"]) for record in pair_atlas_records  # type: ignore[index]
            ),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": total_entropy_matches,
            "entropy_mismatch_records": sum(
                int(record["summary"]["entropy_mismatch_records"]) for record in pair_atlas_records  # type: ignore[index]
            ),
            "priority_semantic_pairs": len(priority_pair_records),
            "priority_candidate_punctured_records": len(all_priority_records),
            "priority_entropy_match_records": priority_entropy_matches,
            "priority_entropy_mismatch_records": sum(1 for record in all_priority_records if not record["entropy_matches"]),
            "priority_operator_channel_checked_records": len(priority_operator_checked_records),
            "semantic_audit_deferred_entropy_match_records": total_entropy_matches - priority_entropy_matches,
            "min_cut_variable_records": sum(
                int(record["summary"]["min_cut_variable_records"]) for record in pair_atlas_records  # type: ignore[index]
            ),
            "operator_or_channel_split_records_checked": sum(
                1
                for record in priority_operator_checked_records
                if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
            "admissible_entropy_match_min_cut_operator_hits": len(priority_admissible_hits),
            "distance_three_witness_outer_variants": sum(
                1
                for cached_outer in outer_variant_cache.values()
                if cached_outer["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "pair_entropy_match_profile_distribution": profile_distribution,
            "priority_pair_entropy_match_profile": priority_profile,
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The independent logical-basis twist atlas scores all 36 first/second twist pairs on the Y bridge "
                "axis across the Phase 26 punctured frontier. It finds 1740 entropy-matched records out of 9000. "
                "The entropy profile is controlled by the second-code twist in this frontier: twelve pairs have 90 "
                "matches, twelve have 55, and twelve have 0. The priority semantic audit checks 290 representative "
                "entropy-matched records across shared/off-diagonal high and medium profiles and finds no split."
            ),
            "three_geometry_lesson": (
                "Breaking the shared-twist symmetry exposes a larger entropy/min-cut atlas, but the first exact "
                "semantic probes still keep reconstruction/channel-visible geometry aligned on the checked "
                "entropy-matched records."
            ),
            "scope_warning": (
                "This is not a full semantic no-go over all independent twist pairs. It fully exhausts exact "
                "entropy and exact min-cut summaries for all 36 pairs, but exact operator/channel checks are limited "
                "to four priority representatives. The remaining entropy-matched records are explicitly deferred."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The priority independent-twist probes preserve the no-go, and the entropy profile is controlled by "
                "the second-code twist. The next phase should either complete the remaining independent-twist "
                "semantic audit with caching, or pivot to alternative graph/CWS source pairs."
            ),
            "suggested_phase_33": (
                "Run cached semantic checks for the deferred 1450 entropy-matched independent-twist records, or use "
                "entropy-mismatch near-hit auditing to choose alternative Phase 2 graph/CWS source pairs."
            ),
        },
    }


def holographic_phase33_pair_variant_record(
    *,
    pair_spec: dict[str, object],
    spec: dict[str, object],
    cached_outer: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    outer = cached_outer["outer"]
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 33 outer cache is malformed")
    first, second, metadata = holographic_phase32_code_pair_for_twists(
        first_twist=pair_spec["first_twist"],  # type: ignore[arg-type]
        second_twist=pair_spec["second_twist"],  # type: ignore[arg-type]
        outer=outer,
        inner_first=inner_first,
        inner_second=inner_second,
    )
    entropy_match_records = 0
    entropy_mismatch_records = 0
    operator_channel_checked_records = 0
    min_cut_variable_records = 0
    operator_or_channel_split_records = 0
    selected_entropy_matched_record = None
    split_records: list[dict[str, object]] = []
    admissible_hit_records: list[dict[str, object]] = []
    all_mincuts_exact = True
    for region_spec in region_specs:
        region = holographic_phase23_region_payload(region_spec)
        mincut = region_mincut_cache[str(region["name"])]
        first_entropy = first.entropy(int(region["mask"]))
        second_entropy = second.entropy(int(region["mask"]))
        entropy_matches = first_entropy == second_entropy
        entropy_match_records += 1 if entropy_matches else 0
        entropy_mismatch_records += 0 if entropy_matches else 1
        min_cut_variable = bool(mincut["min_cut_variable"])
        min_cut_variable_records += 1 if min_cut_variable else 0
        all_mincuts_exact = all_mincuts_exact and bool(mincut["all_mincuts_exact"])
        if not entropy_matches:
            continue
        operator_channel_checked_records += 1
        hit = holographic_phase7_hit_record(
            circuit={
                "name": f"{pair_spec['name']}__{spec['name']}__{region['name']}",
                "generator_kind": "phase33_full_independent_logical_basis_semantic_audit",
            },
            first=first,
            second=second,
            network_spec=network_spec,
            region=region,
        )
        record = {
            "variant": {
                "name": spec["name"],
                "parent": spec["parent"],
                "flipped_offset": spec["flipped_offset"],
                "to_direction": spec["to_direction"],
            },
            "region": mincut["region"],
            "entropy_pair": (first_entropy, second_entropy),
            "entropy_matches": True,
            "operator_channel_checked": True,
            "min_cut_values": mincut["min_cut_values"],
            "min_cut_variable": min_cut_variable,
            "all_mincuts_exact": mincut["all_mincuts_exact"],
            "hit": hit,
            "admissible_entropy_match_min_cut_operator_hit": bool(
                min_cut_variable and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            ),
        }
        if selected_entropy_matched_record is None:
            selected_entropy_matched_record = record
        if hit["comparisons"]["operator_or_channel_visible_differs"]:  # type: ignore[index]
            operator_or_channel_split_records += 1
            split_records.append(record)
            if min_cut_variable:
                admissible_hit_records.append(record)
    summary = {
        "punctured_records": len(region_specs),
        "entropy_match_records": entropy_match_records,
        "entropy_mismatch_records": entropy_mismatch_records,
        "operator_channel_checked_records": operator_channel_checked_records,
        "entropy_gate_rejections": entropy_mismatch_records,
        "min_cut_variable_records": min_cut_variable_records,
        "operator_or_channel_split_records": operator_or_channel_split_records,
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "entropy_mismatch_operator_near_hits": None,
        "all_mincuts_exact": all_mincuts_exact,
    }
    return {
        "variant": {
            "name": f"{pair_spec['name']}__{spec['name']}",
            "phase26_variant_name": spec["name"],
            "layer_kind": "phase33_full_independent_logical_basis_semantic_audit",
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "first_twist_name": pair_spec["first_twist"]["name"],  # type: ignore[index]
            "second_twist_name": pair_spec["second_twist"]["name"],  # type: ignore[index]
            "gates": cached_outer["gates"],
            "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": cached_outer["distance_audit_weight3"],
        },
        "code_pair": {"n": first.n, "k": first.k},
        "twisted_concatenation": metadata,
        "summary": summary,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "operator_or_channel_split_records": tuple(split_records),
        "admissible_hit_records": tuple(admissible_hit_records),
    }


def holographic_phase33_pair_record(
    *,
    pair_spec: dict[str, object],
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    outer_variant_cache: dict[str, dict[str, object]],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    variant_records = tuple(
        holographic_phase33_pair_variant_record(
            pair_spec=pair_spec,
            spec=cached_outer["spec"],  # type: ignore[arg-type]
            cached_outer=cached_outer,
            inner_first=inner_first,
            inner_second=inner_second,
            network_spec=network_spec,
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for cached_outer in outer_variant_cache.values()
    )
    parent_summaries = holographic_phase26_parent_summaries(variant_records)
    selected_entropy_matched_record = next(
        (
            variant["selected_entropy_matched_record"]
            for variant in variant_records
            if variant["selected_entropy_matched_record"] is not None
        ),
        None,
    )
    split_records = tuple(
        record
        for variant in variant_records
        for record in variant["operator_or_channel_split_records"]  # type: ignore[index]
    )
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    summary = {
        "punctured_records": sum(int(variant["summary"]["punctured_records"]) for variant in variant_records),  # type: ignore[index]
        "entropy_match_records": sum(
            int(variant["summary"]["entropy_match_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "entropy_mismatch_records": sum(
            int(variant["summary"]["entropy_mismatch_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "operator_channel_checked_records": sum(
            int(variant["summary"]["operator_channel_checked_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "entropy_gate_rejections": sum(
            int(variant["summary"]["entropy_gate_rejections"]) for variant in variant_records  # type: ignore[index]
        ),
        "min_cut_variable_records": sum(
            int(variant["summary"]["min_cut_variable_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "operator_or_channel_split_records": len(split_records),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
        "distance_three_witness_variants": sum(
            1
            for variant in variant_records
            if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(variant["summary"]["all_mincuts_exact"] for variant in variant_records),  # type: ignore[index]
    }
    return {
        "pair": {
            "name": pair_spec["name"],
            "pair_kind": pair_spec["pair_kind"],
            "first_twist": pair_spec["first_twist"],
            "second_twist": pair_spec["second_twist"],
        },
        "summary": summary,
        "variant_records": variant_records,
        "parent_summaries": parent_summaries,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "operator_or_channel_split_records": split_records,
        "admissible_hit_records": admissible_hits,
    }


def bridge_holography_phase33_certificate(
    *,
    graph_max_codes: int = 24,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    graph_search = holographic_phase3_phase2_source(graph_max_codes=graph_max_codes)
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 2 graph/CWS source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 33 source must contain StabilizerCode objects")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=variant_specs)
    region_mincut_cache = holographic_phase32_region_mincut_cache(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_specs=region_specs,
    )
    pair_specs = holographic_phase32_independent_twist_pair_specs()
    pair_records = tuple(
        holographic_phase33_pair_record(
            pair_spec=pair_spec,
            inner_first=inner_first,
            inner_second=inner_second,
            outer_variant_cache=outer_variant_cache,
            network_spec=networks[0],
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for pair_spec in pair_specs
    )
    pair_entropy_profile = {
        str(record["pair"]["name"]): int(record["summary"]["entropy_match_records"])  # type: ignore[index]
        for record in pair_records
    }
    expected_pair_entropy_profile = holographic_phase32_expected_pair_entropy_profile()
    profile_distribution = {
        count: sum(1 for value in pair_entropy_profile.values() if value == count)
        for count in sorted(set(pair_entropy_profile.values()))
    }
    all_variant_records = tuple(
        variant for pair in pair_records for variant in pair["variant_records"]  # type: ignore[index]
    )
    split_records = tuple(
        record for pair in pair_records for record in pair["operator_or_channel_split_records"]  # type: ignore[index]
    )
    admissible_hits = tuple(
        record for pair in pair_records for record in pair["admissible_hit_records"]  # type: ignore[index]
    )
    total_entropy_matches = sum(int(record["summary"]["entropy_match_records"]) for record in pair_records)  # type: ignore[index]
    total_operator_checked = sum(
        int(record["summary"]["operator_channel_checked_records"]) for record in pair_records  # type: ignore[index]
    )
    phase_claims = {
        "phase2_graph_source_loaded": graph_search["status"] == "pair-found",
        "bridge_axis_y_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "all_independent_logical_basis_pairs_semantically_scored": len(pair_records) == 36
        and len(all_variant_records) == 360,
        "independent_twist_full_semantic_frontier_exhausted": sum(
            int(record["summary"]["punctured_records"]) for record in pair_records  # type: ignore[index]
        )
        == 9000
        and total_entropy_matches == 1740
        and total_operator_checked == 1740,
        "independent_twist_entropy_profile_matches_phase32": pair_entropy_profile == expected_pair_entropy_profile
        and profile_distribution == {0: 12, 55: 12, 90: 12},
        "all_full_semantic_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in all_variant_records
        ),
        "all_full_semantic_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in all_variant_records
        ),
        "all_full_semantic_mincuts_exact": all(
            variant["summary"]["all_mincuts_exact"] for variant in all_variant_records  # type: ignore[index]
        ),
        "all_full_semantic_punctured_records_min_cut_variable": sum(
            int(record["summary"]["min_cut_variable_records"]) for record in pair_records  # type: ignore[index]
        )
        == 9000,
        "all_entropy_matches_operator_checked": total_operator_checked == total_entropy_matches,
        "no_full_independent_twist_admissible_hits": len(admissible_hits) == 0 and len(split_records) == 0,
    }
    phase_claims["goal_3_phase_33_full_independent_logical_basis_twist_no_go_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 33: full independent logical-basis twist semantic no-go",
        "status": "pass"
        if phase_claims["goal_3_phase_33_full_independent_logical_basis_twist_no_go_certificate"]
        else "fail",
        "phase2_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
            "region_mincut_cache": {
                key: {subkey: value for subkey, value in record.items() if subkey != "mask"}
                for key, record in region_mincut_cache.items()
            },
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 32 independent logical-basis twist atlas",
            "bridge_axis": bridge_axis,
            "independent_twist_pairs": tuple(pair_specs),
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "region_frontier": (
                "Replay the Phase 26 offset-flip punctured frontier for all 36 independent first/second "
                "logical-basis twist pairs on the Y bridge axis."
            ),
            "filter_order": (
                "construct the Phase 23 interface-star outer code with bridge axis Y",
                "score exact entropy and cached exact min-cut variation for all 36 independent twist pairs",
                "run exact algebra, erasure, and survivor checks on every entropy-matched record",
                "store compact per-pair/per-variant summaries plus selected witnesses and any split records",
            ),
        },
        "full_independent_twist_frontier": {
            "pair_records": pair_records,
            "pair_entropy_profile": pair_entropy_profile,
            "profile_distribution": profile_distribution,
            "selected_entropy_matched_records": tuple(
                {
                    "pair": record["pair"]["name"],  # type: ignore[index]
                    "record": record["selected_entropy_matched_record"],
                }
                for record in pair_records
            ),
            "operator_or_channel_split_records": split_records,
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "independent_twist_pairs": len(pair_records),
            "first_twists": 6,
            "second_twists": 6,
            "bridge_axes": 1,
            "source_pairings": 1,
            "offset_flip_variants_per_pair": len(variant_specs),
            "independent_pair_variant_records": len(all_variant_records),
            "base_punctured_regions": len(region_specs),
            "candidate_punctured_records": sum(
                int(record["summary"]["punctured_records"]) for record in pair_records  # type: ignore[index]
            ),
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": total_entropy_matches,
            "entropy_mismatch_records": sum(
                int(record["summary"]["entropy_mismatch_records"]) for record in pair_records  # type: ignore[index]
            ),
            "operator_channel_checked_records": total_operator_checked,
            "entropy_gate_rejections": sum(
                int(record["summary"]["entropy_gate_rejections"]) for record in pair_records  # type: ignore[index]
            ),
            "semantic_audit_deferred_entropy_match_records": 0,
            "min_cut_variable_records": sum(
                int(record["summary"]["min_cut_variable_records"]) for record in pair_records  # type: ignore[index]
            ),
            "operator_or_channel_split_records_checked": len(split_records),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "distance_three_witness_twist_variants": sum(
                1
                for variant in all_variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "pair_entropy_match_profile_distribution": profile_distribution,
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The full independent logical-basis twist audit completes the Phase 32 deferred semantic checks. "
                "It scores all 9000 punctured records, runs exact algebra, erasure, and survivor checks on all "
                "1740 entropy-matched records, and finds no operator/channel-visible split."
            ),
            "three_geometry_lesson": (
                "Independent first/second logical-basis twists enlarge the entropy/min-cut atlas, but the exact "
                "reconstruction and channel diagnostics remain matched on every entropy-matched punctured record "
                "in this bounded frontier."
            ),
            "scope_warning": (
                "The audit is exhaustive for independent logical-basis twists on the fixed Phase 2 source pair, "
                "bridge axis Y, the Phase 26 offset-flip circuits, and the 25 Phase 24 punctured regions. It does "
                "not cover alternative graph/CWS source pairs, entropy-mismatched near-hit auditing, full "
                "leaf-private grammars for every twist, changed bridge axes, or non-local region grammars."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The complete independent-twist semantic audit preserves the no-go. The remaining promising lever "
                "is changing the underlying Phase 2 graph/CWS source pair or expanding the region grammar beyond "
                "local punctured shells."
            ),
            "suggested_phase_34": (
                "Search a bounded set of alternative Phase 2 graph/CWS source pairs and use entropy-mismatch "
                "near-hit auditing to prioritize full semantic checks."
            ),
        },
    }


def holographic_phase34_source_pair_public(pair_spec: dict[str, object]) -> dict[str, object]:
    return {
        "name": pair_spec["name"],
        "pair_kind": pair_spec["pair_kind"],
        "source_ordinals": pair_spec["source_ordinals"],
        "phase2_primary_pair": pair_spec["phase2_primary_pair"],
        "entropy_class_index": pair_spec["entropy_class_index"],
        "entropy_class_size": pair_spec["entropy_class_size"],
        "source_summary": pair_spec["source_summary"],
        "graph_metadata": pair_spec["graph_metadata"],
    }


def holographic_phase34_bounded_graph_source_pairs(
    *,
    graph_max_codes: int = 64,
    equivalence: str = "permutation",
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    constraints = relaxed_labeled_graph_constraints()
    records = enumerate_graph_subspace_code_records(
        n=5,
        k=1,
        equivalence=equivalence,
        max_codes=graph_max_codes,
    )
    by_entropy: dict[tuple, list[tuple[dict[str, object], tuple[object, ...]]]] = {}
    codes_checked = 0
    quality_failures = 0
    for record in records:
        code = record["code"]
        if not isinstance(code, StabilizerCode):
            raise TypeError("graph subspace record must contain a StabilizerCode")
        quality = code_quality(code, constraints)
        if not quality.passes:
            quality_failures += 1
            continue
        codes_checked += 1
        key = entropy_key(code, max_subset_size=constraints.max_subset_size, mode="labeled")
        by_entropy.setdefault(key, []).append((record, code.reconstruction_profile()))

    pair_specs: list[dict[str, object]] = []
    entropy_class_indices = {key: index for index, key in enumerate(by_entropy)}
    for key, entropy_records in by_entropy.items():
        for left_index, (left_record, left_reconstruction) in enumerate(entropy_records):
            for right_record, right_reconstruction in entropy_records[left_index + 1 :]:
                if left_reconstruction == right_reconstruction:
                    continue
                first = left_record["code"]
                second = right_record["code"]
                if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
                    raise TypeError("graph source pair records must contain StabilizerCode objects")
                source_ordinals = (int(left_record["ordinal"]), int(right_record["ordinal"]))
                name = f"graph_cws_labeled_source_ord{source_ordinals[0]}_ord{source_ordinals[1]}"
                source = {
                    "name": name,
                    "source_type": "graph_cws_labeled_relaxed",
                    "origin": (
                        "Goal 3 Phase 34 bounded alternative graph/CWS source-pair atlas with labeled t=2 "
                        "entropy collisions and differing reconstruction profiles"
                    ),
                    "frontier_kind": "graph_labeled_alternative_source_pair_atlas",
                    "mutation_depth": 0,
                    "first": first,
                    "second": second,
                }
                pair_specs.append(
                    {
                        "name": name,
                        "pair_kind": "phase34_bounded_graph_cws_labeled_source_pair",
                        "source_ordinals": source_ordinals,
                        "phase2_primary_pair": len(pair_specs) == 0,
                        "entropy_class_index": entropy_class_indices[key],
                        "entropy_class_size": len(entropy_records),
                        "first": first,
                        "second": second,
                        "source_summary": cached_frontier_source_summary(source),
                        "graph_metadata": {
                            "first": graph_subspace_record_summary(left_record),
                            "second": graph_subspace_record_summary(right_record),
                        },
                    }
                )

    source_pair_ordinals = tuple(pair["source_ordinals"] for pair in pair_specs)
    public_pair_summaries = tuple(holographic_phase34_source_pair_public(pair) for pair in pair_specs)
    return {
        "pairs": tuple(pair_specs),
        "scan": {
            "n": 5,
            "k": 1,
            "source": "graph",
            "equivalence": equivalence,
            "entropy_key_mode": "labeled",
            "constraints": {
                "max_subset_size": constraints.max_subset_size,
                "min_distance": constraints.min_distance,
                "min_reconstruction_size": constraints.min_reconstruction_size,
                "forbid_single_qubit_noncentral": constraints.forbid_single_qubit_noncentral,
            },
            "max_codes": graph_max_codes,
            "raw_codes": len(records),
            "codes_checked": codes_checked,
            "quality_failures": quality_failures,
            "entropy_classes": len(by_entropy),
            "entropy_classes_with_reconstruction_discordance": len(
                {pair["entropy_class_index"] for pair in pair_specs}
            ),
            "source_pairs": len(pair_specs),
            "phase2_primary_source_pairs": sum(1 for pair in pair_specs if pair["phase2_primary_pair"]),
            "non_primary_alternative_source_pairs": sum(
                1 for pair in pair_specs if not pair["phase2_primary_pair"]
            ),
            "source_pair_ordinals": source_pair_ordinals,
            "exhausted_before_code_cap": len(records) < graph_max_codes,
            "pair_summaries": public_pair_summaries,
        },
    }


def holographic_phase34_priority_semantic_record(
    *,
    pair_name: str,
    selection_kind: str,
    spec: dict[str, object],
    first: StabilizerCode,
    second: StabilizerCode,
    network_spec: dict[str, object],
    region: dict[str, object],
    mincut: dict[str, object],
    entropy_pair: tuple[int, int],
    entropy_matches: bool,
) -> dict[str, object]:
    hit = holographic_phase7_hit_record(
        circuit={
            "name": f"{pair_name}__{spec['name']}__{region['name']}",
            "generator_kind": "phase34_alternative_source_priority_semantic_audit",
        },
        first=first,
        second=second,
        network_spec=network_spec,
        region=region,
    )
    split = bool(hit["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
    min_cut_variable = bool(mincut["min_cut_variable"])
    return {
        "selection_kind": selection_kind,
        "variant": {
            "name": spec["name"],
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
        },
        "region": mincut["region"],
        "entropy_pair": entropy_pair,
        "entropy_matches": entropy_matches,
        "operator_channel_checked": True,
        "min_cut_values": mincut["min_cut_values"],
        "min_cut_variable": min_cut_variable,
        "all_mincuts_exact": mincut["all_mincuts_exact"],
        "hit": hit,
        "admissible_entropy_match_min_cut_operator_hit": bool(entropy_matches and min_cut_variable and split),
        "entropy_mismatch_operator_near_hit": bool((not entropy_matches) and min_cut_variable and split),
    }


def holographic_phase34_parent_summaries(
    *,
    variant_summaries: tuple[dict[str, object], ...],
    priority_records: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    parents = tuple(dict.fromkeys(str(record["variant"]["parent"]) for record in variant_summaries))  # type: ignore[index]
    summaries: list[dict[str, object]] = []
    for parent in parents:
        selected_variants = tuple(
            record for record in variant_summaries if str(record["variant"]["parent"]) == parent  # type: ignore[index]
        )
        selected_priority = tuple(
            record for record in priority_records if str(record["variant"]["parent"]) == parent  # type: ignore[index]
        )
        summaries.append(
            {
                "parent": parent,
                "variants": len(selected_variants),
                "punctured_records": sum(
                    int(record["summary"]["punctured_records"]) for record in selected_variants  # type: ignore[index]
                ),
                "entropy_match_records": sum(
                    int(record["summary"]["entropy_match_records"]) for record in selected_variants  # type: ignore[index]
                ),
                "entropy_mismatch_records": sum(
                    int(record["summary"]["entropy_mismatch_records"]) for record in selected_variants  # type: ignore[index]
                ),
                "operator_channel_checked_records": len(selected_priority),
                "priority_entropy_match_checked_records": sum(
                    1 for record in selected_priority if record["entropy_matches"]
                ),
                "priority_entropy_mismatch_checked_records": sum(
                    1 for record in selected_priority if not record["entropy_matches"]
                ),
                "operator_or_channel_split_records_checked": sum(
                    1
                    for record in selected_priority
                    if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
                ),
                "admissible_entropy_match_min_cut_operator_hits": sum(
                    1 for record in selected_priority if record["admissible_entropy_match_min_cut_operator_hit"]
                ),
                "priority_entropy_mismatch_operator_near_hits": sum(
                    1 for record in selected_priority if record["entropy_mismatch_operator_near_hit"]
                ),
            }
        )
    return tuple(summaries)


def holographic_phase34_source_pair_record(
    *,
    pair_spec: dict[str, object],
    outer_variant_cache: dict[str, dict[str, object]],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    inner_first = pair_spec["first"]
    inner_second = pair_spec["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 34 source pair must contain StabilizerCode objects")
    priority_records: list[dict[str, object]] = []
    selected_match_parents: set[str] = set()
    selected_mismatch_parents: set[str] = set()
    selected_entropy_matched_record = None
    selected_entropy_mismatch_record = None
    variant_summaries: list[dict[str, object]] = []

    for cached_outer in outer_variant_cache.values():
        spec = cached_outer["spec"]
        outer = cached_outer["outer"]
        if not isinstance(spec, dict) or not isinstance(outer, StabilizerCode):
            raise TypeError("Phase 34 outer cache is malformed")
        first, first_metadata = logical_concatenate_k1(inner_first, outer)
        second, second_metadata = logical_concatenate_k1(inner_second, outer)
        entropy_match_records = 0
        entropy_mismatch_records = 0
        min_cut_variable_records = 0
        all_mincuts_exact = True
        parent = str(spec["parent"])
        for region_spec in region_specs:
            region = holographic_phase23_region_payload(region_spec)
            mincut = region_mincut_cache[str(region["name"])]
            first_entropy = first.entropy(int(region["mask"]))
            second_entropy = second.entropy(int(region["mask"]))
            entropy_pair = (first_entropy, second_entropy)
            entropy_matches = first_entropy == second_entropy
            entropy_match_records += 1 if entropy_matches else 0
            entropy_mismatch_records += 0 if entropy_matches else 1
            min_cut_variable_records += 1 if mincut["min_cut_variable"] else 0
            all_mincuts_exact = all_mincuts_exact and bool(mincut["all_mincuts_exact"])
            if entropy_matches and parent not in selected_match_parents:
                record = holographic_phase34_priority_semantic_record(
                    pair_name=str(pair_spec["name"]),
                    selection_kind="first_entropy_match_per_parent",
                    spec=spec,
                    first=first,
                    second=second,
                    network_spec=network_spec,
                    region=region,
                    mincut=mincut,
                    entropy_pair=entropy_pair,
                    entropy_matches=True,
                )
                priority_records.append(record)
                selected_match_parents.add(parent)
                if selected_entropy_matched_record is None:
                    selected_entropy_matched_record = record
            elif (not entropy_matches) and parent not in selected_mismatch_parents:
                record = holographic_phase34_priority_semantic_record(
                    pair_name=str(pair_spec["name"]),
                    selection_kind="first_entropy_mismatch_per_parent_near_hit_probe",
                    spec=spec,
                    first=first,
                    second=second,
                    network_spec=network_spec,
                    region=region,
                    mincut=mincut,
                    entropy_pair=entropy_pair,
                    entropy_matches=False,
                )
                priority_records.append(record)
                selected_mismatch_parents.add(parent)
                if selected_entropy_mismatch_record is None:
                    selected_entropy_mismatch_record = record
        variant_summaries.append(
            {
                "variant": {
                    "name": spec["name"],
                    "layer_kind": spec["layer_kind"],
                    "parent": spec["parent"],
                    "mutation_kind": spec["mutation_kind"],
                    "flipped_offset": spec["flipped_offset"],
                    "to_direction": spec["to_direction"],
                    "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
                },
                "outer_code": {
                    "parameters": {"n": outer.n, "k": outer.k},
                    "distance_audit_weight3": cached_outer["distance_audit_weight3"],
                },
                "code_pair": {"n": first.n, "k": first.k},
                "concatenation": {
                    "first": first_metadata,
                    "second": second_metadata,
                },
                "summary": {
                    "punctured_records": len(region_specs),
                    "entropy_match_records": entropy_match_records,
                    "entropy_mismatch_records": entropy_mismatch_records,
                    "operator_channel_checked_records": 0,
                    "semantic_audit_deferred_records": entropy_match_records,
                    "min_cut_variable_records": min_cut_variable_records,
                    "all_mincuts_exact": all_mincuts_exact,
                },
            }
        )

    priority_tuple = tuple(priority_records)
    priority_entropy_matches = tuple(record for record in priority_tuple if record["entropy_matches"])
    priority_entropy_mismatches = tuple(record for record in priority_tuple if not record["entropy_matches"])
    admissible_hits = tuple(
        record for record in priority_tuple if record["admissible_entropy_match_min_cut_operator_hit"]
    )
    near_hits = tuple(record for record in priority_tuple if record["entropy_mismatch_operator_near_hit"])
    split_records = tuple(
        record
        for record in priority_tuple
        if record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
    )
    entropy_match_records = sum(
        int(record["summary"]["entropy_match_records"]) for record in variant_summaries  # type: ignore[index]
    )
    entropy_mismatch_records = sum(
        int(record["summary"]["entropy_mismatch_records"]) for record in variant_summaries  # type: ignore[index]
    )
    summary = {
        "punctured_records": sum(
            int(record["summary"]["punctured_records"]) for record in variant_summaries  # type: ignore[index]
        ),
        "entropy_match_records": entropy_match_records,
        "entropy_mismatch_records": entropy_mismatch_records,
        "operator_channel_checked_records": len(priority_tuple),
        "priority_entropy_match_checked_records": len(priority_entropy_matches),
        "priority_entropy_mismatch_checked_records": len(priority_entropy_mismatches),
        "semantic_audit_deferred_entropy_match_records": entropy_match_records - len(priority_entropy_matches),
        "entropy_mismatch_near_hit_deferred_records": entropy_mismatch_records - len(priority_entropy_mismatches),
        "min_cut_variable_records": sum(
            int(record["summary"]["min_cut_variable_records"]) for record in variant_summaries  # type: ignore[index]
        ),
        "operator_or_channel_split_records_checked": len(split_records),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
        "priority_entropy_mismatch_operator_near_hits": len(near_hits),
        "distance_three_witness_variants": sum(
            1
            for record in variant_summaries
            if record["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(record["summary"]["all_mincuts_exact"] for record in variant_summaries),  # type: ignore[index]
    }
    return {
        "pair": holographic_phase34_source_pair_public(pair_spec),
        "summary": summary,
        "variant_summaries": tuple(variant_summaries),
        "parent_summaries": holographic_phase34_parent_summaries(
            variant_summaries=tuple(variant_summaries),
            priority_records=priority_tuple,
        ),
        "priority_semantic_records": priority_tuple,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "selected_entropy_mismatch_record": selected_entropy_mismatch_record,
        "admissible_hit_records": admissible_hits,
        "priority_entropy_mismatch_near_hit_records": near_hits,
        "operator_or_channel_split_records_checked": split_records,
    }


def bridge_holography_phase34_certificate(
    *,
    graph_max_codes: int = 64,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    source_atlas = holographic_phase34_bounded_graph_source_pairs(graph_max_codes=graph_max_codes)
    pair_specs = source_atlas["pairs"]
    if not isinstance(pair_specs, tuple):
        raise TypeError("Phase 34 source atlas is malformed")

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=variant_specs)
    region_mincut_cache = holographic_phase32_region_mincut_cache(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_specs=region_specs,
    )
    pair_records = tuple(
        holographic_phase34_source_pair_record(
            pair_spec=pair_spec,
            outer_variant_cache=outer_variant_cache,
            network_spec=networks[0],
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for pair_spec in pair_specs
    )
    all_variant_summaries = tuple(
        variant for pair in pair_records for variant in pair["variant_summaries"]  # type: ignore[index]
    )
    priority_records = tuple(
        record for pair in pair_records for record in pair["priority_semantic_records"]  # type: ignore[index]
    )
    priority_entropy_matches = tuple(record for record in priority_records if record["entropy_matches"])
    priority_entropy_mismatches = tuple(record for record in priority_records if not record["entropy_matches"])
    admissible_hits = tuple(
        record for pair in pair_records for record in pair["admissible_hit_records"]  # type: ignore[index]
    )
    near_hits = tuple(
        record for pair in pair_records for record in pair["priority_entropy_mismatch_near_hit_records"]  # type: ignore[index]
    )
    split_records = tuple(
        record
        for pair in pair_records
        for record in pair["operator_or_channel_split_records_checked"]  # type: ignore[index]
    )
    pair_entropy_profile = {
        str(record["pair"]["name"]): int(record["summary"]["entropy_match_records"])  # type: ignore[index]
        for record in pair_records
    }
    profile_distribution = {
        count: sum(1 for value in pair_entropy_profile.values() if value == count)
        for count in sorted(set(pair_entropy_profile.values()))
    }
    source_scan = source_atlas["scan"]
    expected_ordinals = ((16, 23), (21, 26), (21, 27), (26, 27))
    phase_claims = {
        "bounded_graph_cws_source_atlas_exhausted": source_scan["raw_codes"] == 33  # type: ignore[index]
        and source_scan["codes_checked"] == 33  # type: ignore[index]
        and source_scan["exhausted_before_code_cap"],  # type: ignore[index]
        "all_reconstruction_discordant_labeled_t2_source_pairs_loaded": len(pair_records) == 4
        and source_scan["source_pair_ordinals"] == expected_ordinals,  # type: ignore[index]
        "phase2_primary_pair_retained_with_three_alternatives": source_scan["phase2_primary_source_pairs"] == 1  # type: ignore[index]
        and source_scan["non_primary_alternative_source_pairs"] == 3,  # type: ignore[index]
        "bridge_axis_y_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "phase26_frontier_scored_for_each_source_pair": len(all_variant_summaries) == 40
        and sum(int(record["summary"]["punctured_records"]) for record in pair_records) == 1000,  # type: ignore[index]
        "alternative_source_pair_full_entropy_frontier_found": pair_entropy_profile.get(
            "graph_cws_labeled_source_ord21_ord26"
        )
        == 250
        and profile_distribution == {90: 3, 250: 1},
        "all_candidate_mincuts_exact_and_variable": all(
            record["summary"]["all_mincuts_exact"] for record in pair_records  # type: ignore[index]
        )
        and sum(int(record["summary"]["min_cut_variable_records"]) for record in pair_records) == 1000,  # type: ignore[index]
        "priority_semantic_audit_scored_per_parent": len(priority_records) == 14
        and len(priority_entropy_matches) == 8
        and len(priority_entropy_mismatches) == 6,
        "priority_entropy_matched_records_have_no_admissible_hits": len(admissible_hits) == 0
        and all(
            not record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            for record in priority_entropy_matches
        ),
        "priority_entropy_mismatch_near_hits_recorded": len(near_hits) == 3 and len(split_records) == 3,
    }
    phase_claims["goal_3_phase_34_bounded_alternative_source_pair_scout_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 34: bounded alternative graph/CWS source-pair scout",
        "status": "pass"
        if phase_claims["goal_3_phase_34_bounded_alternative_source_pair_scout_certificate"]
        else "fail",
        "source_atlas": source_scan,
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
            "region_mincut_cache": {
                key: {subkey: value for subkey, value in record.items() if subkey != "mask"}
                for key, record in region_mincut_cache.items()
            },
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 33 full independent logical-basis twist semantic no-go",
            "bridge_axis": bridge_axis,
            "source_pair_rule": (
                "Enumerate the bounded n=5,k=1 graph/CWS subspace source atlas under permutation equivalence, "
                "group codes by labeled t<=2 entropy, and retain every pair in a bucket whose reconstruction "
                "profiles differ."
            ),
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "priority_semantic_rule": (
                "For each source pair and each Phase 26 parent circuit, run exact algebra, erasure, and survivor "
                "checks on the first entropy-matched record and, when present, the first entropy-mismatched record. "
                "All remaining records keep exact entropy/min-cut scores and explicit semantic deferral counts."
            ),
            "filter_order": (
                "exact bounded source-pair atlas",
                "exact entropy and cached exact min-cut variation for all source-pair/variant/puncture records",
                "priority exact operator/channel checks per parent circuit",
                "store entropy-mismatched operator near-hits separately from admissible entropy-matched hits",
            ),
        },
        "alternative_source_frontier": {
            "pair_records": pair_records,
            "pair_entropy_profile": pair_entropy_profile,
            "profile_distribution": profile_distribution,
            "selected_entropy_matched_records": tuple(
                {
                    "pair": record["pair"]["name"],  # type: ignore[index]
                    "record": record["selected_entropy_matched_record"],
                }
                for record in pair_records
            ),
            "selected_entropy_mismatch_records": tuple(
                {
                    "pair": record["pair"]["name"],  # type: ignore[index]
                    "record": record["selected_entropy_mismatch_record"],
                }
                for record in pair_records
            ),
            "operator_or_channel_split_records_checked": split_records,
            "admissible_hit_records": admissible_hits,
            "priority_entropy_mismatch_near_hit_records": near_hits,
        },
        "counts": {
            "raw_graph_codes": source_scan["raw_codes"],  # type: ignore[index]
            "relaxed_codes_checked": source_scan["codes_checked"],  # type: ignore[index]
            "entropy_classes": source_scan["entropy_classes"],  # type: ignore[index]
            "source_pairs": len(pair_records),
            "phase2_primary_source_pairs": source_scan["phase2_primary_source_pairs"],  # type: ignore[index]
            "non_primary_alternative_source_pairs": source_scan["non_primary_alternative_source_pairs"],  # type: ignore[index]
            "source_pair_ordinals": source_scan["source_pair_ordinals"],  # type: ignore[index]
            "offset_flip_variants_per_source_pair": len(variant_specs),
            "source_pair_variant_records": len(all_variant_summaries),
            "base_punctured_regions": len(region_specs),
            "candidate_records": sum(int(record["summary"]["punctured_records"]) for record in pair_records),  # type: ignore[index]
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(
                int(record["summary"]["entropy_match_records"]) for record in pair_records  # type: ignore[index]
            ),
            "entropy_mismatch_records": sum(
                int(record["summary"]["entropy_mismatch_records"]) for record in pair_records  # type: ignore[index]
            ),
            "operator_channel_checked_records": len(priority_records),
            "priority_entropy_match_checked_records": len(priority_entropy_matches),
            "priority_entropy_mismatch_checked_records": len(priority_entropy_mismatches),
            "semantic_audit_deferred_entropy_match_records": sum(
                int(record["summary"]["semantic_audit_deferred_entropy_match_records"])  # type: ignore[index]
                for record in pair_records
            ),
            "entropy_mismatch_near_hit_deferred_records": sum(
                int(record["summary"]["entropy_mismatch_near_hit_deferred_records"])  # type: ignore[index]
                for record in pair_records
            ),
            "min_cut_variable_records": sum(
                int(record["summary"]["min_cut_variable_records"]) for record in pair_records  # type: ignore[index]
            ),
            "operator_or_channel_split_records_checked": len(split_records),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "priority_entropy_mismatch_operator_near_hits": len(near_hits),
            "distance_three_witness_source_variants": sum(
                1
                for variant in all_variant_summaries
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "pair_entropy_match_profile_distribution": profile_distribution,
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The bounded n=5 graph/CWS source atlas contains four labeled-t2 entropy-matched source pairs with "
                "different reconstruction profiles. Three are non-primary alternatives to the Phase 2 pair. Replaying "
                "the Phase 26 Y-bridge punctured frontier across all four pairs gives 1000 exact entropy/min-cut "
                "records. One alternative pair, ordinals (21,26), preserves entropy on all 250 records."
            ),
            "three_geometry_lesson": (
                "Changing the inner source pair can substantially improve entropy/min-cut compatibility without "
                "changing the outer geometry. The priority semantic probes still show no admissible entropy-matched "
                "operator/channel split, while three entropy-mismatched priority probes remain operator/channel "
                "near-hits."
            ),
            "scope_warning": (
                "Phase 34 is a source-pair scout, not a full semantic no-go over all alternative sources. It is "
                "exhaustive for the bounded n=5 graph/CWS source-pair atlas and exact for all entropy/min-cut "
                "records in the Phase 26 frontier, but exact operator/channel checks are limited to the stated "
                "priority per-parent semantic rule."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The alternative source-pair lever is real: source pair (21,26) removes all entropy rejections in "
                "the Phase 26 frontier. The next phase should spend the expensive semantic budget on that full "
                "250-record pair before broadening the region grammar again."
            ),
            "suggested_phase_35": (
                "Run a full cached semantic audit for graph/CWS source pair ordinals (21,26) across all Phase 26 "
                "variants and Phase 24 punctured regions, then separately audit the queued entropy-mismatch near-hits."
            ),
        },
    }


def holographic_phase35_selected_source_pair(
    *,
    graph_max_codes: int,
    source_ordinals: tuple[int, int] = (21, 26),
) -> tuple[dict[str, object], dict[str, object]]:
    source_atlas = holographic_phase34_bounded_graph_source_pairs(graph_max_codes=graph_max_codes)
    pair_specs = source_atlas["pairs"]
    if not isinstance(pair_specs, tuple):
        raise TypeError("Phase 35 source atlas is malformed")
    for pair_spec in pair_specs:
        if pair_spec["source_ordinals"] == source_ordinals:
            return pair_spec, source_atlas["scan"]  # type: ignore[return-value]
    raise RuntimeError(f"expected Phase 35 source pair ordinals {source_ordinals!r} in bounded graph/CWS atlas")


def holographic_phase35_variant_record(
    *,
    pair_spec: dict[str, object],
    spec: dict[str, object],
    cached_outer: dict[str, object],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    inner_first = pair_spec["first"]
    inner_second = pair_spec["second"]
    outer = cached_outer["outer"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 35 source pair must contain StabilizerCode objects")
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 35 outer cache is malformed")

    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    entropy_match_records = 0
    entropy_mismatch_records = 0
    operator_channel_checked_records = 0
    min_cut_variable_records = 0
    operator_or_channel_split_records = 0
    selected_entropy_matched_record = None
    selected_entropy_mismatch_record = None
    split_records: list[dict[str, object]] = []
    admissible_hit_records: list[dict[str, object]] = []
    all_mincuts_exact = True

    for region_spec in region_specs:
        region = holographic_phase23_region_payload(region_spec)
        mincut = region_mincut_cache[str(region["name"])]
        first_entropy = first.entropy(int(region["mask"]))
        second_entropy = second.entropy(int(region["mask"]))
        entropy_pair = (first_entropy, second_entropy)
        entropy_matches = first_entropy == second_entropy
        entropy_match_records += 1 if entropy_matches else 0
        entropy_mismatch_records += 0 if entropy_matches else 1
        min_cut_variable = bool(mincut["min_cut_variable"])
        min_cut_variable_records += 1 if min_cut_variable else 0
        all_mincuts_exact = all_mincuts_exact and bool(mincut["all_mincuts_exact"])
        operator_channel_checked_records += 1
        hit = holographic_phase7_hit_record(
            circuit={
                "name": f"{pair_spec['name']}__{spec['name']}__{region['name']}",
                "generator_kind": "phase35_full_alternative_source_pair_semantic_audit",
            },
            first=first,
            second=second,
            network_spec=network_spec,
            region=region,
        )
        operator_or_channel_split = bool(hit["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
        record = {
            "variant": {
                "name": spec["name"],
                "parent": spec["parent"],
                "mutation_kind": spec["mutation_kind"],
                "flipped_offset": spec["flipped_offset"],
                "to_direction": spec["to_direction"],
            },
            "region": mincut["region"],
            "entropy_pair": entropy_pair,
            "entropy_matches": entropy_matches,
            "operator_channel_checked": True,
            "min_cut_values": mincut["min_cut_values"],
            "min_cut_variable": min_cut_variable,
            "all_mincuts_exact": mincut["all_mincuts_exact"],
            "hit": hit,
            "admissible_entropy_match_min_cut_operator_hit": bool(
                entropy_matches and min_cut_variable and operator_or_channel_split
            ),
            "entropy_mismatch_operator_near_hit": bool(
                (not entropy_matches) and min_cut_variable and operator_or_channel_split
            ),
        }
        if entropy_matches and selected_entropy_matched_record is None:
            selected_entropy_matched_record = record
        if (not entropy_matches) and selected_entropy_mismatch_record is None:
            selected_entropy_mismatch_record = record
        if operator_or_channel_split:
            operator_or_channel_split_records += 1
            split_records.append(record)
            if entropy_matches and min_cut_variable:
                admissible_hit_records.append(record)

    summary = {
        "punctured_records": len(region_specs),
        "entropy_match_records": entropy_match_records,
        "entropy_mismatch_records": entropy_mismatch_records,
        "operator_channel_checked_records": operator_channel_checked_records,
        "entropy_gate_rejections": 0,
        "min_cut_variable_records": min_cut_variable_records,
        "operator_or_channel_split_records": operator_or_channel_split_records,
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "entropy_mismatch_operator_near_hits": sum(
            1 for record in split_records if record["entropy_mismatch_operator_near_hit"]
        ),
        "all_mincuts_exact": all_mincuts_exact,
    }
    return {
        "variant": {
            "name": spec["name"],
            "phase26_variant_name": spec["name"],
            "layer_kind": "phase35_full_alternative_source_pair_semantic_audit",
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "gates": cached_outer["gates"],
            "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": cached_outer["distance_audit_weight3"],
        },
        "code_pair": {"n": first.n, "k": first.k},
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "summary": summary,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "selected_entropy_mismatch_record": selected_entropy_mismatch_record,
        "operator_or_channel_split_records": tuple(split_records),
        "admissible_hit_records": tuple(admissible_hit_records),
    }


def bridge_holography_phase35_certificate(
    *,
    graph_max_codes: int = 64,
    source_ordinals: tuple[int, int] = (21, 26),
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    pair_spec, source_scan = holographic_phase35_selected_source_pair(
        graph_max_codes=graph_max_codes,
        source_ordinals=source_ordinals,
    )

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=variant_specs)
    region_mincut_cache = holographic_phase32_region_mincut_cache(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_specs=region_specs,
    )
    variant_records = tuple(
        holographic_phase35_variant_record(
            pair_spec=pair_spec,
            spec=cached_outer["spec"],  # type: ignore[arg-type]
            cached_outer=cached_outer,
            network_spec=networks[0],
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for cached_outer in outer_variant_cache.values()
    )
    parent_summaries = holographic_phase26_parent_summaries(variant_records)
    selected_entropy_matched_record = next(
        (
            variant["selected_entropy_matched_record"]
            for variant in variant_records
            if variant["selected_entropy_matched_record"] is not None
        ),
        None,
    )
    selected_entropy_mismatch_record = next(
        (
            variant["selected_entropy_mismatch_record"]
            for variant in variant_records
            if variant["selected_entropy_mismatch_record"] is not None
        ),
        None,
    )
    split_records = tuple(
        record
        for variant in variant_records
        for record in variant["operator_or_channel_split_records"]  # type: ignore[index]
    )
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    total_records = sum(int(variant["summary"]["punctured_records"]) for variant in variant_records)  # type: ignore[index]
    total_entropy_matches = sum(
        int(variant["summary"]["entropy_match_records"]) for variant in variant_records  # type: ignore[index]
    )
    total_entropy_mismatches = sum(
        int(variant["summary"]["entropy_mismatch_records"]) for variant in variant_records  # type: ignore[index]
    )
    total_operator_checked = sum(
        int(variant["summary"]["operator_channel_checked_records"]) for variant in variant_records  # type: ignore[index]
    )
    total_min_cut_variable = sum(
        int(variant["summary"]["min_cut_variable_records"]) for variant in variant_records  # type: ignore[index]
    )
    phase_claims = {
        "phase34_source_pair_21_26_loaded": pair_spec["source_ordinals"] == source_ordinals
        and pair_spec["name"] == "graph_cws_labeled_source_ord21_ord26",
        "bridge_axis_y_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "phase26_frontier_fully_semantically_scored": len(variant_records) == 10
        and total_records == 250
        and total_operator_checked == 250,
        "all_source_pair_records_entropy_matched": total_entropy_matches == 250 and total_entropy_mismatches == 0,
        "all_source_pair_mincuts_exact_and_variable": all(
            variant["summary"]["all_mincuts_exact"] for variant in variant_records  # type: ignore[index]
        )
        and total_min_cut_variable == 250,
        "all_source_pair_code_pairs_are_n150_k1": all(
            variant["code_pair"] == {"n": 150, "k": 1} for variant in variant_records
        ),
        "all_source_pair_outer_distance_three_witnessed": all(
            variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            for variant in variant_records
        ),
        "full_semantic_hit_outcome_classified": len(admissible_hits) == len(split_records)
        and selected_entropy_matched_record is not None
        and selected_entropy_mismatch_record is None,
    }
    phase_claims["goal_3_phase_35_full_alternative_source_pair_semantic_audit_certificate"] = all(
        phase_claims.values()
    )
    if admissible_hits:
        result_text = (
            f"The full source-pair audit found {len(admissible_hits)} admissible entropy-matched min-cut/operator "
            "hits for graph/CWS source ordinals (21,26)."
        )
        recommendation = {
            "next_phase": "proceed",
            "reason": (
                "Phase 35 found a finite holographic-cousin witness candidate. The next step should package the "
                "smallest hit, minimize the region/circuit description, and compare it against the Goal 1/2 "
                "balanced-bridge witness."
            ),
            "suggested_phase_36": (
                "Extract the smallest admissible Phase 35 hit into a standalone witness certificate with a compact "
                "boundary-region diagram and cross-check it under nearby bridge axes/source-pair relabelings."
            ),
        }
    else:
        result_text = (
            "The full source-pair audit checks all 250 entropy-matched Phase 26 records for graph/CWS source ordinals "
            "(21,26) and finds no operator/channel-visible split."
        )
        recommendation = {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Source pair (21,26) repairs the entropy frontier, but exact reconstruction/channel diagnostics still "
                "match on every checked punctured region. The next lever is the queued entropy-mismatch near-hit "
                "surface from the other alternative source pairs or a non-local region grammar."
            ),
            "suggested_phase_36": (
                "Run a targeted full near-hit audit over the Phase 34 entropy-mismatched operator/channel probes, "
                "then expand the region grammar around the split-support regions if the entropy obstruction persists."
            ),
        }
    return {
        "phase": "Goal 3 Phase 35: full alternative graph/CWS source-pair semantic audit",
        "status": "pass"
        if phase_claims["goal_3_phase_35_full_alternative_source_pair_semantic_audit_certificate"]
        else "fail",
        "source_atlas": source_scan,
        "selected_source_pair": holographic_phase34_source_pair_public(pair_spec),
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
            "region_mincut_cache": {
                key: {subkey: value for subkey, value in record.items() if subkey != "mask"}
                for key, record in region_mincut_cache.items()
            },
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 34 bounded alternative graph/CWS source-pair scout",
            "bridge_axis": bridge_axis,
            "source_pair_ordinals": source_ordinals,
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "filter_order": (
                "load the bounded graph/CWS source pair ordinals (21,26)",
                "construct the Phase 23 interface-star outer code with bridge axis Y",
                "replay all Phase 26 offset-flip variants and all Phase 24 punctured regions",
                "run exact algebra, erasure, and survivor checks on every record",
                "classify any entropy-matched min-cut-variable operator/channel split as an admissible hit",
            ),
        },
        "full_source_pair_frontier": {
            "variant_records": variant_records,
            "parent_summaries": parent_summaries,
            "selected_entropy_matched_record": selected_entropy_matched_record,
            "selected_entropy_mismatch_record": selected_entropy_mismatch_record,
            "operator_or_channel_split_records": split_records,
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "source_pairs_loaded": 1,
            "raw_graph_codes": source_scan["raw_codes"],  # type: ignore[index]
            "relaxed_codes_checked": source_scan["codes_checked"],  # type: ignore[index]
            "source_pair_ordinals": source_ordinals,
            "offset_flip_variants": len(variant_records),
            "parent_circuits": len(parent_summaries),
            "base_punctured_regions": len(region_specs),
            "candidate_records": total_records,
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": total_entropy_matches,
            "entropy_mismatch_records": total_entropy_mismatches,
            "operator_channel_checked_records": total_operator_checked,
            "entropy_gate_rejections": 0,
            "semantic_audit_deferred_entropy_match_records": 0,
            "min_cut_variable_records": total_min_cut_variable,
            "operator_or_channel_split_records_checked": len(split_records),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "entropy_mismatch_operator_near_hits": sum(
                int(variant["summary"]["entropy_mismatch_operator_near_hits"]) for variant in variant_records  # type: ignore[index]
            ),
            "distance_three_witness_source_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": result_text,
            "three_geometry_lesson": (
                "Phase 35 tests whether the strongest Phase 34 entropy/min-cut source-pair signal also separates "
                "reconstruction/channel-visible geometry. The exact outcome is stored in the admissible hit records "
                "rather than inferred from entropy data."
            ),
            "scope_warning": (
                "The audit is exhaustive for source pair (21,26), bridge axis Y, the Phase 26 offset-flip circuits, "
                "and the 25 Phase 24 punctured regions. It does not cover other alternative source pairs, "
                "entropy-mismatched near-hit regions from Phase 34, changed bridge axes, or non-local region grammars."
            ),
        },
        "recommendation": recommendation,
    }


def holographic_phase36_source_pairs(
    *,
    graph_max_codes: int,
    source_ordinals: tuple[tuple[int, int], ...] = ((16, 23), (21, 27), (26, 27)),
) -> tuple[tuple[dict[str, object], ...], dict[str, object]]:
    source_atlas = holographic_phase34_bounded_graph_source_pairs(graph_max_codes=graph_max_codes)
    pair_specs = source_atlas["pairs"]
    if not isinstance(pair_specs, tuple):
        raise TypeError("Phase 36 source atlas is malformed")
    by_ordinals = {pair["source_ordinals"]: pair for pair in pair_specs}
    missing = tuple(ordinals for ordinals in source_ordinals if ordinals not in by_ordinals)
    if missing:
        raise RuntimeError(f"expected Phase 36 source pair ordinals missing from atlas: {missing!r}")
    return tuple(by_ordinals[ordinals] for ordinals in source_ordinals), source_atlas["scan"]  # type: ignore[return-value]


def holographic_phase36_variant_record(
    *,
    pair_spec: dict[str, object],
    spec: dict[str, object],
    cached_outer: dict[str, object],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    inner_first = pair_spec["first"]
    inner_second = pair_spec["second"]
    outer = cached_outer["outer"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 36 source pair must contain StabilizerCode objects")
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 36 outer cache is malformed")

    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    entropy_match_records = 0
    entropy_mismatch_records = 0
    operator_channel_checked_records = 0
    min_cut_variable_records = 0
    mismatch_min_cut_variable_records = 0
    selected_entropy_mismatch_record = None
    selected_near_hit_record = None
    near_hit_records: list[dict[str, object]] = []
    split_records: list[dict[str, object]] = []
    all_mincuts_exact = True

    for region_spec in region_specs:
        region = holographic_phase23_region_payload(region_spec)
        mincut = region_mincut_cache[str(region["name"])]
        first_entropy = first.entropy(int(region["mask"]))
        second_entropy = second.entropy(int(region["mask"]))
        entropy_pair = (first_entropy, second_entropy)
        entropy_matches = first_entropy == second_entropy
        entropy_match_records += 1 if entropy_matches else 0
        entropy_mismatch_records += 0 if entropy_matches else 1
        min_cut_variable = bool(mincut["min_cut_variable"])
        min_cut_variable_records += 1 if min_cut_variable else 0
        mismatch_min_cut_variable_records += 1 if (not entropy_matches) and min_cut_variable else 0
        all_mincuts_exact = all_mincuts_exact and bool(mincut["all_mincuts_exact"])
        if entropy_matches:
            continue
        operator_channel_checked_records += 1
        hit = holographic_phase7_hit_record(
            circuit={
                "name": f"{pair_spec['name']}__{spec['name']}__{region['name']}",
                "generator_kind": "phase36_full_entropy_mismatch_near_hit_audit",
            },
            first=first,
            second=second,
            network_spec=network_spec,
            region=region,
        )
        operator_or_channel_split = bool(hit["comparisons"]["operator_or_channel_visible_differs"])  # type: ignore[index]
        record = {
            "variant": {
                "name": spec["name"],
                "parent": spec["parent"],
                "mutation_kind": spec["mutation_kind"],
                "flipped_offset": spec["flipped_offset"],
                "to_direction": spec["to_direction"],
            },
            "region": mincut["region"],
            "entropy_pair": entropy_pair,
            "entropy_matches": False,
            "operator_channel_checked": True,
            "min_cut_values": mincut["min_cut_values"],
            "min_cut_variable": min_cut_variable,
            "all_mincuts_exact": mincut["all_mincuts_exact"],
            "hit": hit,
            "entropy_mismatch_operator_near_hit": bool(min_cut_variable and operator_or_channel_split),
            "channel_visible_near_hit": bool(
                min_cut_variable and hit["comparisons"]["channel_visible_differs"]  # type: ignore[index]
            ),
            "operator_only_near_hit": bool(
                min_cut_variable
                and hit["comparisons"]["reconstruction_visible_differs"]  # type: ignore[index]
                and not hit["comparisons"]["channel_visible_differs"]  # type: ignore[index]
            ),
        }
        if selected_entropy_mismatch_record is None:
            selected_entropy_mismatch_record = record
        if operator_or_channel_split:
            split_records.append(record)
            if min_cut_variable:
                near_hit_records.append(record)
                if selected_near_hit_record is None:
                    selected_near_hit_record = record

    summary = {
        "punctured_records": len(region_specs),
        "entropy_match_records": entropy_match_records,
        "entropy_mismatch_records": entropy_mismatch_records,
        "operator_channel_checked_records": operator_channel_checked_records,
        "semantic_audit_skipped_entropy_match_records": entropy_match_records,
        "min_cut_variable_records": min_cut_variable_records,
        "mismatch_min_cut_variable_records": mismatch_min_cut_variable_records,
        "operator_or_channel_split_records": len(split_records),
        "admissible_entropy_match_min_cut_operator_hits": 0,
        "entropy_mismatch_operator_near_hits": len(near_hit_records),
        "channel_visible_near_hits": sum(1 for record in near_hit_records if record["channel_visible_near_hit"]),
        "operator_only_near_hits": sum(1 for record in near_hit_records if record["operator_only_near_hit"]),
        "all_mincuts_exact": all_mincuts_exact,
    }
    return {
        "variant": {
            "name": spec["name"],
            "phase26_variant_name": spec["name"],
            "layer_kind": "phase36_full_entropy_mismatch_near_hit_audit",
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "gates": cached_outer["gates"],
            "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": cached_outer["distance_audit_weight3"],
        },
        "code_pair": {"n": first.n, "k": first.k},
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "summary": summary,
        "selected_entropy_mismatch_record": selected_entropy_mismatch_record,
        "selected_near_hit_record": selected_near_hit_record,
        "operator_or_channel_split_records": tuple(split_records),
        "near_hit_records": tuple(near_hit_records),
    }


def holographic_phase36_pair_record(
    *,
    pair_spec: dict[str, object],
    outer_variant_cache: dict[str, dict[str, object]],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    variant_records = tuple(
        holographic_phase36_variant_record(
            pair_spec=pair_spec,
            spec=cached_outer["spec"],  # type: ignore[arg-type]
            cached_outer=cached_outer,
            network_spec=network_spec,
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for cached_outer in outer_variant_cache.values()
    )
    parent_summaries = holographic_phase26_parent_summaries(variant_records)
    selected_entropy_mismatch_record = next(
        (
            variant["selected_entropy_mismatch_record"]
            for variant in variant_records
            if variant["selected_entropy_mismatch_record"] is not None
        ),
        None,
    )
    selected_near_hit_record = next(
        (variant["selected_near_hit_record"] for variant in variant_records if variant["selected_near_hit_record"]),
        None,
    )
    split_records = tuple(
        record
        for variant in variant_records
        for record in variant["operator_or_channel_split_records"]  # type: ignore[index]
    )
    near_hit_records = tuple(
        record for variant in variant_records for record in variant["near_hit_records"]  # type: ignore[index]
    )
    summary = {
        "punctured_records": sum(int(variant["summary"]["punctured_records"]) for variant in variant_records),  # type: ignore[index]
        "entropy_match_records": sum(
            int(variant["summary"]["entropy_match_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "entropy_mismatch_records": sum(
            int(variant["summary"]["entropy_mismatch_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "operator_channel_checked_records": sum(
            int(variant["summary"]["operator_channel_checked_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "semantic_audit_skipped_entropy_match_records": sum(
            int(variant["summary"]["semantic_audit_skipped_entropy_match_records"])  # type: ignore[index]
            for variant in variant_records
        ),
        "min_cut_variable_records": sum(
            int(variant["summary"]["min_cut_variable_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "mismatch_min_cut_variable_records": sum(
            int(variant["summary"]["mismatch_min_cut_variable_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "operator_or_channel_split_records": len(split_records),
        "entropy_mismatch_operator_near_hits": len(near_hit_records),
        "channel_visible_near_hits": sum(1 for record in near_hit_records if record["channel_visible_near_hit"]),
        "operator_only_near_hits": sum(1 for record in near_hit_records if record["operator_only_near_hit"]),
        "distance_three_witness_variants": sum(
            1
            for variant in variant_records
            if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(variant["summary"]["all_mincuts_exact"] for variant in variant_records),  # type: ignore[index]
    }
    return {
        "pair": holographic_phase34_source_pair_public(pair_spec),
        "summary": summary,
        "variant_records": variant_records,
        "parent_summaries": parent_summaries,
        "selected_entropy_mismatch_record": selected_entropy_mismatch_record,
        "selected_near_hit_record": selected_near_hit_record,
        "operator_or_channel_split_records": split_records,
        "near_hit_records": near_hit_records,
    }


def holographic_phase36_region_near_hit_profile(records: tuple[dict[str, object], ...]) -> dict[str, int]:
    names = sorted({str(record["region"]["name"]) for record in records})  # type: ignore[index]
    return {name: sum(1 for record in records if record["region"]["name"] == name) for name in names}  # type: ignore[index]


def bridge_holography_phase36_certificate(
    *,
    graph_max_codes: int = 64,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    source_ordinals = ((16, 23), (21, 27), (26, 27))
    pair_specs, source_scan = holographic_phase36_source_pairs(
        graph_max_codes=graph_max_codes,
        source_ordinals=source_ordinals,
    )

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    region_specs = holographic_phase24_punctured_region_specs()
    variant_specs = holographic_phase26_offset_flip_neighborhood_specs()
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=variant_specs)
    region_mincut_cache = holographic_phase32_region_mincut_cache(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_specs=region_specs,
    )
    pair_records = tuple(
        holographic_phase36_pair_record(
            pair_spec=pair_spec,
            outer_variant_cache=outer_variant_cache,
            network_spec=networks[0],
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for pair_spec in pair_specs
    )
    variant_records = tuple(
        variant for pair in pair_records for variant in pair["variant_records"]  # type: ignore[index]
    )
    near_hit_records = tuple(record for pair in pair_records for record in pair["near_hit_records"])  # type: ignore[index]
    split_records = tuple(
        record for pair in pair_records for record in pair["operator_or_channel_split_records"]  # type: ignore[index]
    )
    pair_near_hit_profile = {
        str(record["pair"]["name"]): int(record["summary"]["entropy_mismatch_operator_near_hits"])  # type: ignore[index]
        for record in pair_records
    }
    parent_near_hit_profile = {
        parent: sum(
            int(variant["summary"]["entropy_mismatch_operator_near_hits"])  # type: ignore[index]
            for variant in variant_records
            if str(variant["variant"]["parent"]) == parent  # type: ignore[index]
        )
        for parent in tuple(dict.fromkeys(str(variant["variant"]["parent"]) for variant in variant_records))  # type: ignore[index]
    }
    variant_names = tuple(dict.fromkeys(str(variant["variant"]["name"]) for variant in variant_records))  # type: ignore[index]
    variant_near_hit_profile = {
        name: sum(
            int(variant["summary"]["entropy_mismatch_operator_near_hits"])  # type: ignore[index]
            for variant in variant_records
            if str(variant["variant"]["name"]) == name  # type: ignore[index]
        )
        for name in variant_names
    }
    total_records = sum(int(record["summary"]["punctured_records"]) for record in pair_records)  # type: ignore[index]
    total_entropy_matches = sum(
        int(record["summary"]["entropy_match_records"]) for record in pair_records  # type: ignore[index]
    )
    total_entropy_mismatches = sum(
        int(record["summary"]["entropy_mismatch_records"]) for record in pair_records  # type: ignore[index]
    )
    total_operator_checked = sum(
        int(record["summary"]["operator_channel_checked_records"]) for record in pair_records  # type: ignore[index]
    )
    total_mismatch_min_cut_variable = sum(
        int(record["summary"]["mismatch_min_cut_variable_records"]) for record in pair_records  # type: ignore[index]
    )
    channel_visible_near_hits = sum(1 for record in near_hit_records if record["channel_visible_near_hit"])
    operator_only_near_hits = sum(1 for record in near_hit_records if record["operator_only_near_hit"])
    phase_claims = {
        "phase34_entropy_mismatch_source_pairs_loaded": tuple(pair["source_ordinals"] for pair in pair_specs)
        == source_ordinals,
        "bridge_axis_y_loaded": base_outer.n == 30 and base_outer.k == 1 and len(base_outer.generators) == 29,
        "phase26_entropy_mismatch_surface_fully_audited": len(pair_records) == 3
        and len(variant_records) == 30
        and total_records == 750
        and total_entropy_mismatches == 480
        and total_operator_checked == 480,
        "entropy_match_records_deliberately_skipped_by_near_hit_audit": total_entropy_matches == 270
        and sum(
            int(record["summary"]["semantic_audit_skipped_entropy_match_records"])  # type: ignore[index]
            for record in pair_records
        )
        == 270,
        "all_entropy_mismatch_mincuts_exact_and_variable": all(
            record["summary"]["all_mincuts_exact"] for record in pair_records  # type: ignore[index]
        )
        and total_mismatch_min_cut_variable == 480,
        "near_hits_partition_by_parent": parent_near_hit_profile
        == {"leaf_to_root_same_position": 0, "alternating_disentangler_isometry": 165},
        "near_hit_profile_repeats_across_source_pairs": set(pair_near_hit_profile.values()) == {55},
        "near_hits_classified_by_channel_visibility": channel_visible_near_hits == 85
        and operator_only_near_hits == 80,
        "no_entropy_matched_admissible_hits_claimed": all(not record["entropy_matches"] for record in near_hit_records),
    }
    phase_claims["goal_3_phase_36_full_entropy_mismatch_near_hit_audit_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 36: full entropy-mismatch near-hit audit",
        "status": "pass"
        if phase_claims["goal_3_phase_36_full_entropy_mismatch_near_hit_audit_certificate"]
        else "fail",
        "source_atlas": source_scan,
        "selected_source_pairs": tuple(holographic_phase34_source_pair_public(pair) for pair in pair_specs),
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "punctured_regions": region_specs,
            "capacity_profiles": capacity_profiles,
            "region_mincut_cache": {
                key: {subkey: value for subkey, value in record.items() if subkey != "mask"}
                for key, record in region_mincut_cache.items()
            },
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 35 full alternative graph/CWS source-pair semantic no-go",
            "bridge_axis": bridge_axis,
            "source_pair_ordinals": source_ordinals,
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "filter_order": (
                "load the Phase 34 source pairs whose Phase 26 frontier has entropy mismatches",
                "score exact entropy and cached exact min-cut variation for all records",
                "run exact algebra, erasure, and survivor checks on every entropy-mismatched record",
                "classify operator/channel near-hits by source pair, parent circuit, variant, region, and channel visibility",
            ),
        },
        "near_hit_frontier": {
            "pair_records": pair_records,
            "pair_near_hit_profile": pair_near_hit_profile,
            "parent_near_hit_profile": parent_near_hit_profile,
            "variant_near_hit_profile": variant_near_hit_profile,
            "region_near_hit_profile": holographic_phase36_region_near_hit_profile(near_hit_records),
            "operator_or_channel_split_records": split_records,
            "near_hit_records": near_hit_records,
        },
        "counts": {
            "source_pairs_loaded": len(pair_records),
            "raw_graph_codes": source_scan["raw_codes"],  # type: ignore[index]
            "relaxed_codes_checked": source_scan["codes_checked"],  # type: ignore[index]
            "source_pair_ordinals": source_ordinals,
            "offset_flip_variants_per_source_pair": len(variant_specs),
            "source_pair_variant_records": len(variant_records),
            "parent_circuits": len(parent_near_hit_profile),
            "base_punctured_regions": len(region_specs),
            "candidate_records": total_records,
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": total_entropy_matches,
            "entropy_mismatch_records": total_entropy_mismatches,
            "operator_channel_checked_records": total_operator_checked,
            "semantic_audit_skipped_entropy_match_records": sum(
                int(record["summary"]["semantic_audit_skipped_entropy_match_records"])  # type: ignore[index]
                for record in pair_records
            ),
            "mismatch_min_cut_variable_records": total_mismatch_min_cut_variable,
            "operator_or_channel_split_records_checked": len(split_records),
            "entropy_mismatch_operator_near_hits": len(near_hit_records),
            "channel_visible_near_hits": channel_visible_near_hits,
            "operator_only_near_hits": operator_only_near_hits,
            "leaf_to_root_near_hits": parent_near_hit_profile["leaf_to_root_same_position"],
            "alternating_near_hits": parent_near_hit_profile["alternating_disentangler_isometry"],
            "distance_three_witness_source_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The full entropy-mismatch near-hit audit checks all 480 entropy-rejected Phase 26 records from "
                "source pairs (16,23), (21,27), and (26,27). It finds 165 operator/channel near-hits. All are in "
                "the alternating-disentangler parent family; every leaf-to-root variant is cold."
            ),
            "three_geometry_lesson": (
                "The obstruction has a sharp shape: operator/channel-visible geometry is present on a structured "
                "alternating-circuit support, but every such split remains entropy-mismatched under the Phase 24 "
                "punctured-shell grammar."
            ),
            "scope_warning": (
                "The audit is exhaustive for the stated entropy-mismatched Phase 26 records on bridge axis Y. It "
                "does not change region grammar, bridge axis, source-pair relabeling, or outer circuit family."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The near-hit taxonomy localizes the obstruction to alternating-disentangler split-support regions. "
                "The next phase should expand the region grammar around those supports rather than continue broad "
                "source-pair or parent-circuit enumeration."
            ),
            "suggested_phase_37": (
                "Build a bounded split-support region grammar around root_shell_plus_edge_0_minus_q129/q139 and "
                "their neighboring root/leaf punctures, then rerun the exact entropy/min-cut/operator/channel filter."
            ),
        },
    }

def holographic_phase37_seed_variant_holes() -> dict[str, tuple[int, ...]]:
    return {
        "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root": (139, 149),
        "alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf": (139, 144, 149),
        "alternating_disentangler_isometry__flip_offset_2_to_leaf_to_root": (139,),
        "alternating_disentangler_isometry__flip_offset_3_to_root_to_leaf": (129, 134, 139),
        "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root": (129, 139),
    }


def holographic_phase37_leaf_private_add_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    qubits = set(int(qubit) for qubit in base_region_spec["qubits"])  # type: ignore[index]
    leaf = int(base_region_spec["leaf_cell"])
    specs: list[dict[str, object]] = []
    for leaf_offset in range(4):
        qubit = leaf * 25 + leaf_offset
        if qubit in qubits:
            continue
        specs.append(
            {
                **base_region_spec,
                "name": f"{base_region_spec['name']}__phase37_add_leaf_private_q{qubit}",
                "region_type": "phase37_split_support_leaf_private_add",
                "phase37_edit": "add_leaf_private",
                "added_leaf_private_qubit": qubit,
                "added_leaf_private_offset": leaf_offset,
                "qubits": tuple(sorted(qubits | {qubit})),
                "description": (
                    f"Phase 37 split-support add variant of {base_region_spec['name']}: add leaf-cell qubit "
                    f"q{qubit} at local offset {leaf_offset}."
                ),
            }
        )
    return tuple(specs)


def holographic_phase37_leaf_handle_swap_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    qubits = set(int(qubit) for qubit in base_region_spec["qubits"])  # type: ignore[index]
    leaf = int(base_region_spec["leaf_cell"])
    removed = leaf * 25 + 4
    if removed not in qubits:
        raise ValueError("Phase 37 leaf-handle swap expects the Phase 24 leaf offset-4 handle")
    specs: list[dict[str, object]] = []
    for leaf_offset in range(4):
        added = leaf * 25 + leaf_offset
        specs.append(
            {
                **base_region_spec,
                "name": f"{base_region_spec['name']}__phase37_swap_leaf_handle_q{removed}_to_q{added}",
                "region_type": "phase37_split_support_leaf_handle_swap",
                "phase37_edit": "swap_leaf_handle",
                "removed_leaf_handle_qubit": removed,
                "removed_leaf_handle_offset": 4,
                "added_leaf_handle_qubit": added,
                "added_leaf_handle_offset": leaf_offset,
                "qubits": tuple(sorted((qubits - {removed}) | {added})),
                "description": (
                    f"Phase 37 split-support swap variant of {base_region_spec['name']}: replace leaf handle "
                    f"q{removed} with q{added} at local offset {leaf_offset}."
                ),
            }
        )
    return tuple(specs)


def holographic_phase37_split_support_edit_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    return holographic_phase37_leaf_private_add_specs(
        base_region_spec
    ) + holographic_phase37_leaf_handle_swap_specs(base_region_spec)


def holographic_phase37_region_payload(region_spec: dict[str, object]) -> dict[str, object]:
    payload = holographic_phase23_region_payload(region_spec)
    common = {
        "phase37_edit": region_spec["phase37_edit"],
        "leaf_cell": region_spec["leaf_cell"],
        "removed_root_qubit": region_spec["removed_root_qubit"],
        "removed_root_offset": region_spec["removed_root_offset"],
    }
    if str(region_spec["phase37_edit"]) == "add_leaf_private":
        return {
            **payload,
            **common,
            "added_leaf_private_qubit": region_spec["added_leaf_private_qubit"],
            "added_leaf_private_offset": region_spec["added_leaf_private_offset"],
        }
    return {
        **payload,
        **common,
        "removed_leaf_handle_qubit": region_spec["removed_leaf_handle_qubit"],
        "removed_leaf_handle_offset": region_spec["removed_leaf_handle_offset"],
        "added_leaf_handle_qubit": region_spec["added_leaf_handle_qubit"],
        "added_leaf_handle_offset": region_spec["added_leaf_handle_offset"],
    }


def holographic_phase37_region_mincut_cache(
    *,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, dict[str, object]]:
    cache: dict[str, dict[str, object]] = {}
    for region_spec in region_specs:
        region = holographic_phase37_region_payload(region_spec)
        min_cut_values = holographic_phase23_mincut_values(
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_mask=int(region["mask"]),
        )
        all_mincuts_exact = all(
            int(holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))["assignments_checked"])
            == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
            for network in networks
        )
        cache[str(region["name"])] = {
            "region": {key: value for key, value in region.items() if key != "mask"},
            "mask": int(region["mask"]),
            "min_cut_values_by_capacity": min_cut_values,
            "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
            "min_cut_variable": len({int(record["value"]) for record in min_cut_values}) > 1,
            "all_mincuts_exact": all_mincuts_exact,
        }
    return cache


def holographic_phase37_all_split_support_region_specs(
    region_specs: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    by_name: dict[str, dict[str, object]] = {}
    for base_region_spec in region_specs:
        for edit_spec in holographic_phase37_split_support_edit_specs(base_region_spec):
            by_name[str(edit_spec["name"])] = edit_spec
    return tuple(by_name.values())


def holographic_phase37_variant_record(
    *,
    pair_spec: dict[str, object],
    spec: dict[str, object],
    cached_outer: dict[str, object],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    inner_first = pair_spec["first"]
    inner_second = pair_spec["second"]
    outer = cached_outer["outer"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 37 source pair must contain StabilizerCode objects")
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 37 outer cache is malformed")

    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    seed_holes = holographic_phase37_seed_variant_holes()[str(spec["name"])]
    seed_base_records = 0
    candidate_records = 0
    entropy_match_records = 0
    entropy_mismatch_records = 0
    operator_channel_checked_records = 0
    min_cut_variable_records = 0
    selected_entropy_mismatch_record = None
    selected_entropy_matched_record = None
    records: list[dict[str, object]] = []
    admissible_hit_records: list[dict[str, object]] = []
    split_records: list[dict[str, object]] = []
    all_mincuts_exact = True

    for base_region_spec in region_specs:
        removed_root_qubit = int(base_region_spec["removed_root_qubit"])
        if removed_root_qubit not in seed_holes:
            continue
        seed_base_records += 1
        base_region = holographic_phase23_region_payload(base_region_spec)
        base_entropy_pair = (
            first.entropy(int(base_region["mask"])),
            second.entropy(int(base_region["mask"])),
        )
        for edit_spec in holographic_phase37_split_support_edit_specs(base_region_spec):
            region = holographic_phase37_region_payload(edit_spec)
            mincut = region_mincut_cache[str(region["name"])]
            first_entropy = first.entropy(int(region["mask"]))
            second_entropy = second.entropy(int(region["mask"]))
            entropy_pair = (first_entropy, second_entropy)
            entropy_matches = first_entropy == second_entropy
            entropy_match_records += 1 if entropy_matches else 0
            entropy_mismatch_records += 0 if entropy_matches else 1
            operator_channel_checked_records += 1 if entropy_matches else 0
            min_cut_variable = bool(mincut["min_cut_variable"])
            min_cut_variable_records += 1 if min_cut_variable else 0
            all_mincuts_exact = all_mincuts_exact and bool(mincut["all_mincuts_exact"])
            hit = (
                holographic_phase7_hit_record(
                    circuit={
                        "name": f"{pair_spec['name']}__{spec['name']}__{region['name']}",
                        "generator_kind": "phase37_split_support_region_grammar",
                    },
                    first=first,
                    second=second,
                    network_spec=network_spec,
                    region=region,
                )
                if entropy_matches
                else None
            )
            operator_or_channel_split = bool(
                hit is not None
                and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            )
            record = {
                "variant": {
                    "name": spec["name"],
                    "parent": spec["parent"],
                    "mutation_kind": spec["mutation_kind"],
                    "flipped_offset": spec["flipped_offset"],
                    "to_direction": spec["to_direction"],
                },
                "base_region": {key: value for key, value in base_region.items() if key != "mask"},
                "base_entropy_pair": base_entropy_pair,
                "base_entropy_matches": base_entropy_pair[0] == base_entropy_pair[1],
                "region": mincut["region"],
                "phase37_edit": edit_spec["phase37_edit"],
                "entropy_pair": entropy_pair,
                "entropy_matches": entropy_matches,
                "operator_channel_checked": entropy_matches,
                "min_cut_values": mincut["min_cut_values"],
                "min_cut_variable": min_cut_variable,
                "all_mincuts_exact": mincut["all_mincuts_exact"],
                "hit": hit,
                "admissible_entropy_match_min_cut_operator_hit": bool(
                    entropy_matches and min_cut_variable and operator_or_channel_split
                ),
                "strict_filter_stage": (
                    "operator_channel_checked" if entropy_matches else "split_support_entropy_gate_rejected"
                ),
            }
            candidate_records += 1
            records.append(record)
            if selected_entropy_mismatch_record is None and not entropy_matches:
                selected_entropy_mismatch_record = record
            if selected_entropy_matched_record is None and entropy_matches:
                selected_entropy_matched_record = record
            if operator_or_channel_split:
                split_records.append(record)
                if min_cut_variable:
                    admissible_hit_records.append(record)

    summary = {
        "seed_base_records": seed_base_records,
        "candidate_split_support_records": candidate_records,
        "add_leaf_private_records": sum(1 for record in records if record["phase37_edit"] == "add_leaf_private"),
        "swap_leaf_handle_records": sum(1 for record in records if record["phase37_edit"] == "swap_leaf_handle"),
        "entropy_match_records": entropy_match_records,
        "entropy_mismatch_records": entropy_mismatch_records,
        "operator_channel_checked_records": operator_channel_checked_records,
        "split_support_entropy_gate_rejections": entropy_mismatch_records,
        "min_cut_variable_records": min_cut_variable_records,
        "operator_or_channel_split_records": len(split_records),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "all_mincuts_exact": all_mincuts_exact,
    }
    return {
        "variant": {
            "name": spec["name"],
            "phase26_variant_name": spec["name"],
            "layer_kind": "phase37_split_support_region_grammar",
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "seed_removed_root_holes": seed_holes,
            "gates": cached_outer["gates"],
            "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": cached_outer["distance_audit_weight3"],
        },
        "code_pair": {"n": first.n, "k": first.k},
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "summary": summary,
        "records": tuple(records),
        "selected_entropy_mismatch_record": selected_entropy_mismatch_record,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "operator_or_channel_split_records": tuple(split_records),
        "admissible_hit_records": tuple(admissible_hit_records),
    }


def holographic_phase37_pair_record(
    *,
    pair_spec: dict[str, object],
    outer_variant_cache: dict[str, dict[str, object]],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    variant_records = tuple(
        holographic_phase37_variant_record(
            pair_spec=pair_spec,
            spec=cached_outer["spec"],  # type: ignore[arg-type]
            cached_outer=cached_outer,
            network_spec=network_spec,
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for cached_outer in outer_variant_cache.values()
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    split_records = tuple(
        record for variant in variant_records for record in variant["operator_or_channel_split_records"]  # type: ignore[index]
    )
    summary = {
        "seed_base_records": sum(
            int(variant["summary"]["seed_base_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "candidate_split_support_records": len(all_records),
        "add_leaf_private_records": sum(1 for record in all_records if record["phase37_edit"] == "add_leaf_private"),
        "swap_leaf_handle_records": sum(1 for record in all_records if record["phase37_edit"] == "swap_leaf_handle"),
        "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
        "operator_channel_checked_records": sum(1 for record in all_records if record["operator_channel_checked"]),
        "split_support_entropy_gate_rejections": sum(
            1 for record in all_records if not record["operator_channel_checked"]
        ),
        "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
        "operator_or_channel_split_records": len(split_records),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
        "distance_three_witness_variants": sum(
            1
            for variant in variant_records
            if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
    }
    return {
        "pair": holographic_phase34_source_pair_public(pair_spec),
        "summary": summary,
        "variant_records": variant_records,
        "selected_entropy_mismatch_record": next(
            (
                variant["selected_entropy_mismatch_record"]
                for variant in variant_records
                if variant["selected_entropy_mismatch_record"] is not None
            ),
            None,
        ),
        "selected_entropy_matched_record": next(
            (
                variant["selected_entropy_matched_record"]
                for variant in variant_records
                if variant["selected_entropy_matched_record"] is not None
            ),
            None,
        ),
        "operator_or_channel_split_records": split_records,
        "admissible_hit_records": admissible_hits,
    }


def holographic_phase37_profile(
    records: tuple[dict[str, object], ...],
    key_path: tuple[str, ...],
) -> dict[str, int]:
    def value_at(record: dict[str, object]) -> object:
        value: object = record
        for key in key_path:
            value = value[key]  # type: ignore[index]
        return value

    names = sorted({str(value_at(record)) for record in records})
    return {name: sum(1 for record in records if str(value_at(record)) == name) for name in names}


def bridge_holography_phase37_certificate(
    *,
    graph_max_codes: int = 64,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    source_ordinals = ((16, 23), (21, 27), (26, 27))
    pair_specs, source_scan = holographic_phase36_source_pairs(
        graph_max_codes=graph_max_codes,
        source_ordinals=source_ordinals,
    )

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    base_region_specs = holographic_phase24_punctured_region_specs()
    seed_variant_holes = holographic_phase37_seed_variant_holes()
    variant_specs = tuple(
        spec
        for spec in holographic_phase26_offset_flip_neighborhood_specs()
        if str(spec["name"]) in seed_variant_holes
    )
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=variant_specs)
    split_support_region_specs = holographic_phase37_all_split_support_region_specs(base_region_specs)
    region_mincut_cache = holographic_phase37_region_mincut_cache(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_specs=split_support_region_specs,
    )
    pair_records = tuple(
        holographic_phase37_pair_record(
            pair_spec=pair_spec,
            outer_variant_cache=outer_variant_cache,
            network_spec=networks[0],
            region_specs=base_region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for pair_spec in pair_specs
    )
    variant_records = tuple(
        variant for pair in pair_records for variant in pair["variant_records"]  # type: ignore[index]
    )
    all_records = tuple(
        record for pair in pair_records for variant in pair["variant_records"] for record in variant["records"]  # type: ignore[index]
    )
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for pair in pair_records for record in pair["admissible_hit_records"]  # type: ignore[index]
    )
    split_records = tuple(
        record for pair in pair_records for record in pair["operator_or_channel_split_records"]  # type: ignore[index]
    )
    pair_candidate_profile = {
        str(record["pair"]["name"]): int(record["summary"]["candidate_split_support_records"])  # type: ignore[index]
        for record in pair_records
    }
    variant_names = tuple(dict.fromkeys(str(record["variant"]["name"]) for record in variant_records))  # type: ignore[index]
    variant_candidate_profile = {
        name: sum(
            int(record["summary"]["candidate_split_support_records"])  # type: ignore[index]
            for record in variant_records
            if str(record["variant"]["name"]) == name  # type: ignore[index]
        )
        for name in variant_names
    }
    edit_profile = holographic_phase37_profile(all_records, ("phase37_edit",))
    entropy_pairs = tuple(sorted({record["entropy_pair"] for record in all_records}))  # type: ignore[type-var]
    entropy_pair_profile = {
        str(pair): sum(1 for record in all_records if record["entropy_pair"] == pair)
        for pair in entropy_pairs
    }
    min_cut_values = tuple(sorted({record["min_cut_values"] for record in all_records}))  # type: ignore[type-var]
    min_cut_value_profile = {
        str(values): sum(1 for record in all_records if record["min_cut_values"] == values)
        for values in min_cut_values
    }
    removed_root_qubit_profile = {
        str(qubit): sum(
            1
            for record in all_records
            if str(record["base_region"]["name"]).endswith(f"q{qubit}")  # type: ignore[index]
        )
        for qubit in holographic_phase24_root_witness_holes()
    }
    phase_claims = {
        "phase36_source_pairs_reused": tuple(pair["source_ordinals"] for pair in pair_specs) == source_ordinals,
        "phase36_alternating_seed_profile_replayed": len(seed_variant_holes) == 5
        and sum(len(holes) for holes in seed_variant_holes.values()) == 11
        and sum(int(record["summary"]["seed_base_records"]) for record in pair_records) == 165,  # type: ignore[index]
        "split_support_edit_grammar_bounded": len(split_support_region_specs) == 200
        and edit_profile == {"add_leaf_private": 660, "swap_leaf_handle": 660},
        "all_split_support_mincuts_exact_and_variable": all(record["all_mincuts_exact"] for record in all_records)
        and sum(1 for record in all_records if record["min_cut_variable"]) == 1320,
        "split_support_frontier_exhausted": len(pair_records) == 3
        and len(variant_records) == 15
        and len(all_records) == 1320,
        "all_split_support_candidates_entropy_rejected": len(operator_checked_records) == 0
        and all(not record["entropy_matches"] for record in all_records),
        "no_split_support_admissible_hits": len(admissible_hits) == 0 and len(split_records) == 0,
        "candidate_profile_matches_phase36_seed_multiplicity": pair_candidate_profile
        == {
            "graph_cws_labeled_source_ord16_ord23": 440,
            "graph_cws_labeled_source_ord21_ord27": 440,
            "graph_cws_labeled_source_ord26_ord27": 440,
        }
        and variant_candidate_profile
        == {
            "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root": 240,
            "alternating_disentangler_isometry__flip_offset_1_to_root_to_leaf": 360,
            "alternating_disentangler_isometry__flip_offset_2_to_leaf_to_root": 120,
            "alternating_disentangler_isometry__flip_offset_3_to_root_to_leaf": 360,
            "alternating_disentangler_isometry__flip_offset_4_to_leaf_to_root": 240,
        },
    }
    phase_claims["goal_3_phase_37_split_support_region_grammar_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 37: split-support region-grammar entropy obstruction",
        "status": "pass"
        if phase_claims["goal_3_phase_37_split_support_region_grammar_certificate"]
        else "fail",
        "source_atlas": source_scan,
        "selected_source_pairs": tuple(holographic_phase34_source_pair_public(pair) for pair in pair_specs),
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "base_punctured_regions": base_region_specs,
            "split_support_region_specs": split_support_region_specs,
            "capacity_profiles": capacity_profiles,
            "region_mincut_cache": {
                key: {subkey: value for subkey, value in record.items() if subkey != "mask"}
                for key, record in region_mincut_cache.items()
            },
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 36 full entropy-mismatch near-hit audit",
            "bridge_axis": bridge_axis,
            "source_pair_ordinals": source_ordinals,
            "seed_variant_holes": seed_variant_holes,
            "candidate_parent_variants": tuple(str(spec["name"]) for spec in variant_specs),
            "region_grammar": (
                "For every Phase 36 alternating near-hit seed region, add one leaf-private qubit at local "
                "offsets 0..3 and swap the original leaf handle at offset 4 to offsets 0..3."
            ),
            "filter_order": (
                "reuse the certified Phase 36 alternating variant/root-hole seed profile",
                "generate both bounded split-support edits for each seed leaf cell",
                "score exact entropy and exact min-cut variation for every adapted region",
                "run exact algebra, erasure, and survivor checks only for entropy-matched adapted records",
            ),
        },
        "split_support_frontier": {
            "pair_records": pair_records,
            "pair_candidate_profile": pair_candidate_profile,
            "variant_candidate_profile": variant_candidate_profile,
            "edit_profile": edit_profile,
            "entropy_pair_profile": entropy_pair_profile,
            "min_cut_value_profile": min_cut_value_profile,
            "removed_root_qubit_profile": removed_root_qubit_profile,
            "operator_or_channel_split_records": split_records,
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "source_pairs_loaded": len(pair_records),
            "raw_graph_codes": source_scan["raw_codes"],  # type: ignore[index]
            "relaxed_codes_checked": source_scan["codes_checked"],  # type: ignore[index]
            "source_pair_ordinals": source_ordinals,
            "seed_alternating_variants": len(variant_specs),
            "seed_variant_hole_rules": sum(len(holes) for holes in seed_variant_holes.values()),
            "seed_base_records": sum(int(record["summary"]["seed_base_records"]) for record in pair_records),  # type: ignore[index]
            "unique_split_support_region_specs": len(split_support_region_specs),
            "edit_kinds": len(edit_profile),
            "candidate_split_support_records": len(all_records),
            "add_leaf_private_records": edit_profile["add_leaf_private"],
            "swap_leaf_handle_records": edit_profile["swap_leaf_handle"],
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "split_support_entropy_gate_rejections": sum(
                1 for record in all_records if not record["operator_channel_checked"]
            ),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": len(split_records),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "distance_three_witness_source_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The split-support grammar expands the 165 Phase 36 alternating near-hit seeds into 1320 adapted "
                "regions. Every adapted region remains exact and capacity-sensitive, but every one is still "
                "entropy-mismatched. No adapted record reaches the operator/channel stage of the strict filter."
            ),
            "three_geometry_lesson": (
                "Local leaf-support surgery is not enough to turn the Phase 36 entropy-rejected near-hit surface "
                "into an entropy/min-cut-visible holographic cousin. The reconstruction/channel signal remains "
                "present only before the entropy gate, while the adapted entropy/min-cut surface stays misaligned."
            ),
            "scope_warning": (
                "The audit is exhaustive only for the Phase 36 alternating seed profile, local leaf-private adds "
                "at offsets 0..3, and leaf-handle swaps from offset 4 to offsets 0..3. It does not cover all leaf "
                "offsets, multi-leaf edits, non-local regions, new outer circuits, changed bridge axes, or new "
                "source pairs."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The bounded split-support grammar preserves min-cut variability but cannot repair entropy on the "
                "alternative source near-hit surface. The next lever should change the support scale: either add "
                "multi-leaf/non-local region moves around the q139-heavy seed, or alter the outer circuit/source "
                "pairing before more local leaf surgery."
            ),
            "suggested_phase_38": (
                "Run a bounded q139-heavy non-local support scout, such as two-leaf additions or cross-leaf handle "
                "swaps, while keeping exact min-cut, entropy, algebra, erasure, and survivor checks."
            ),
        },
    }

def holographic_phase38_variant_names() -> tuple[str, ...]:
    return tuple(
        f"alternating_disentangler_isometry__flip_offset_{offset}_to_"
        f"{'leaf_to_root' if offset in (0, 2, 4) else 'root_to_leaf'}"
        for offset in range(5)
    )


def holographic_phase38_same_leaf_two_private_add_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    qubits = set(int(qubit) for qubit in base_region_spec["qubits"])  # type: ignore[index]
    leaf = int(base_region_spec["leaf_cell"])
    specs: list[dict[str, object]] = []
    for first_offset, second_offset in combinations(range(4), 2):
        added = (leaf * 25 + first_offset, leaf * 25 + second_offset)
        specs.append(
            {
                **base_region_spec,
                "name": f"{base_region_spec['name']}__phase38_same_leaf_add_q{added[0]}_q{added[1]}",
                "region_type": "phase38_q139_same_leaf_two_private_add",
                "phase38_edit": "same_leaf_two_private_add",
                "added_leaf_private_qubits": added,
                "added_leaf_private_offsets": (first_offset, second_offset),
                "qubits": tuple(sorted(qubits | set(added))),
                "description": (
                    f"Phase 38 q139 support-scale variant of {base_region_spec['name']}: add same-leaf private "
                    f"qubits q{added[0]} and q{added[1]}."
                ),
            }
        )
    return tuple(specs)


def holographic_phase38_cross_leaf_private_add_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    qubits = set(int(qubit) for qubit in base_region_spec["qubits"])  # type: ignore[index]
    leaf = int(base_region_spec["leaf_cell"])
    base_cells = set(int(cell) for cell in base_region_spec["perfect_cells"])  # type: ignore[index]
    specs: list[dict[str, object]] = []
    for cross_leaf in range(5):
        if cross_leaf == leaf:
            continue
        for offset in range(4):
            added = cross_leaf * 25 + offset
            specs.append(
                {
                    **base_region_spec,
                    "name": f"{base_region_spec['name']}__phase38_cross_leaf{cross_leaf}_add_q{added}",
                    "region_type": "phase38_q139_cross_leaf_private_add",
                    "phase38_edit": "cross_leaf_private_add",
                    "cross_leaf_cell": cross_leaf,
                    "added_cross_leaf_private_qubit": added,
                    "added_cross_leaf_private_offset": offset,
                    "perfect_cells": tuple(sorted(base_cells | {cross_leaf})),
                    "qubits": tuple(sorted(qubits | {added})),
                    "description": (
                        f"Phase 38 q139 support-scale variant of {base_region_spec['name']}: add cross-leaf "
                        f"private qubit q{added} in leaf cell {cross_leaf}."
                    ),
                }
            )
    return tuple(specs)


def holographic_phase38_q139_support_edit_specs(
    base_region_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    return holographic_phase38_same_leaf_two_private_add_specs(
        base_region_spec
    ) + holographic_phase38_cross_leaf_private_add_specs(base_region_spec)


def holographic_phase38_region_payload(region_spec: dict[str, object]) -> dict[str, object]:
    payload = holographic_phase23_region_payload(region_spec)
    common = {
        "phase38_edit": region_spec["phase38_edit"],
        "leaf_cell": region_spec["leaf_cell"],
        "removed_root_qubit": region_spec["removed_root_qubit"],
        "removed_root_offset": region_spec["removed_root_offset"],
    }
    if str(region_spec["phase38_edit"]) == "same_leaf_two_private_add":
        return {
            **payload,
            **common,
            "added_leaf_private_qubits": region_spec["added_leaf_private_qubits"],
            "added_leaf_private_offsets": region_spec["added_leaf_private_offsets"],
        }
    return {
        **payload,
        **common,
        "cross_leaf_cell": region_spec["cross_leaf_cell"],
        "added_cross_leaf_private_qubit": region_spec["added_cross_leaf_private_qubit"],
        "added_cross_leaf_private_offset": region_spec["added_cross_leaf_private_offset"],
    }


def holographic_phase38_region_mincut_cache(
    *,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, dict[str, object]]:
    cache: dict[str, dict[str, object]] = {}
    for region_spec in region_specs:
        region = holographic_phase38_region_payload(region_spec)
        min_cut_values = holographic_phase23_mincut_values(
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_mask=int(region["mask"]),
        )
        all_mincuts_exact = all(
            int(holographic_network_min_cut(network_spec=network, region_mask=int(region["mask"]))["assignments_checked"])
            == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
            for network in networks
        )
        cache[str(region["name"])] = {
            "region": {key: value for key, value in region.items() if key != "mask"},
            "mask": int(region["mask"]),
            "min_cut_values_by_capacity": min_cut_values,
            "min_cut_values": tuple(sorted({int(record["value"]) for record in min_cut_values})),
            "min_cut_variable": len({int(record["value"]) for record in min_cut_values}) > 1,
            "all_mincuts_exact": all_mincuts_exact,
        }
    return cache


def holographic_phase38_all_q139_support_region_specs(
    region_specs: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    by_name: dict[str, dict[str, object]] = {}
    for base_region_spec in region_specs:
        if int(base_region_spec["removed_root_qubit"]) != 139:
            continue
        for edit_spec in holographic_phase38_q139_support_edit_specs(base_region_spec):
            by_name[str(edit_spec["name"])] = edit_spec
    return tuple(by_name.values())


def holographic_phase38_variant_record(
    *,
    pair_spec: dict[str, object],
    spec: dict[str, object],
    cached_outer: dict[str, object],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    inner_first = pair_spec["first"]
    inner_second = pair_spec["second"]
    outer = cached_outer["outer"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 38 source pair must contain StabilizerCode objects")
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 38 outer cache is malformed")

    first, first_metadata = logical_concatenate_k1(inner_first, outer)
    second, second_metadata = logical_concatenate_k1(inner_second, outer)
    records: list[dict[str, object]] = []
    split_records: list[dict[str, object]] = []
    admissible_hit_records: list[dict[str, object]] = []
    selected_entropy_matched_record = None
    selected_admissible_hit_record = None
    seed_base_records = 0
    all_mincuts_exact = True

    for base_region_spec in region_specs:
        if int(base_region_spec["removed_root_qubit"]) != 139:
            continue
        seed_base_records += 1
        base_region = holographic_phase23_region_payload(base_region_spec)
        base_entropy_pair = (
            first.entropy(int(base_region["mask"])),
            second.entropy(int(base_region["mask"])),
        )
        for edit_spec in holographic_phase38_q139_support_edit_specs(base_region_spec):
            region = holographic_phase38_region_payload(edit_spec)
            mincut = region_mincut_cache[str(region["name"])]
            first_entropy = first.entropy(int(region["mask"]))
            second_entropy = second.entropy(int(region["mask"]))
            entropy_pair = (first_entropy, second_entropy)
            entropy_matches = first_entropy == second_entropy
            min_cut_variable = bool(mincut["min_cut_variable"])
            all_mincuts_exact = all_mincuts_exact and bool(mincut["all_mincuts_exact"])
            hit = (
                holographic_phase7_hit_record(
                    circuit={
                        "name": f"{pair_spec['name']}__{spec['name']}__{region['name']}",
                        "generator_kind": "phase38_q139_support_scale_strict_hit_scout",
                    },
                    first=first,
                    second=second,
                    network_spec=network_spec,
                    region=region,
                )
                if entropy_matches
                else None
            )
            operator_or_channel_split = bool(
                hit is not None
                and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
            )
            channel_visible_split = bool(
                hit is not None and hit["comparisons"]["channel_visible_differs"]  # type: ignore[index]
            )
            record = {
                "variant": {
                    "name": spec["name"],
                    "parent": spec["parent"],
                    "mutation_kind": spec["mutation_kind"],
                    "flipped_offset": spec["flipped_offset"],
                    "to_direction": spec["to_direction"],
                },
                "base_region": {key: value for key, value in base_region.items() if key != "mask"},
                "base_entropy_pair": base_entropy_pair,
                "base_entropy_matches": base_entropy_pair[0] == base_entropy_pair[1],
                "region": mincut["region"],
                "phase38_edit": edit_spec["phase38_edit"],
                "entropy_pair": entropy_pair,
                "entropy_matches": entropy_matches,
                "operator_channel_checked": entropy_matches,
                "min_cut_values": mincut["min_cut_values"],
                "min_cut_variable": min_cut_variable,
                "all_mincuts_exact": mincut["all_mincuts_exact"],
                "hit": hit,
                "admissible_entropy_match_min_cut_operator_hit": bool(
                    entropy_matches and min_cut_variable and operator_or_channel_split
                ),
                "channel_visible_admissible_hit": bool(
                    entropy_matches and min_cut_variable and channel_visible_split
                ),
                "operator_only_admissible_hit": bool(
                    entropy_matches
                    and min_cut_variable
                    and operator_or_channel_split
                    and not channel_visible_split
                ),
                "strict_filter_stage": (
                    "operator_channel_checked" if entropy_matches else "q139_support_entropy_gate_rejected"
                ),
            }
            records.append(record)
            if selected_entropy_matched_record is None and entropy_matches:
                selected_entropy_matched_record = record
            if operator_or_channel_split:
                split_records.append(record)
                if min_cut_variable:
                    admissible_hit_records.append(record)
                    if selected_admissible_hit_record is None:
                        selected_admissible_hit_record = record

    record_tuple = tuple(records)
    operator_checked_records = tuple(record for record in record_tuple if record["operator_channel_checked"])
    summary = {
        "seed_base_records": seed_base_records,
        "candidate_q139_support_records": len(record_tuple),
        "same_leaf_two_private_add_records": sum(
            1 for record in record_tuple if record["phase38_edit"] == "same_leaf_two_private_add"
        ),
        "cross_leaf_private_add_records": sum(
            1 for record in record_tuple if record["phase38_edit"] == "cross_leaf_private_add"
        ),
        "entropy_match_records": sum(1 for record in record_tuple if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in record_tuple if not record["entropy_matches"]),
        "operator_channel_checked_records": len(operator_checked_records),
        "q139_support_entropy_gate_rejections": sum(
            1 for record in record_tuple if not record["operator_channel_checked"]
        ),
        "min_cut_variable_records": sum(1 for record in record_tuple if record["min_cut_variable"]),
        "operator_or_channel_split_records": len(split_records),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hit_records),
        "channel_visible_admissible_hits": sum(
            1 for record in admissible_hit_records if record["channel_visible_admissible_hit"]
        ),
        "operator_only_admissible_hits": sum(
            1 for record in admissible_hit_records if record["operator_only_admissible_hit"]
        ),
        "all_mincuts_exact": all_mincuts_exact,
    }
    return {
        "variant": {
            "name": spec["name"],
            "phase26_variant_name": spec["name"],
            "layer_kind": "phase38_q139_support_scale_strict_hit_scout",
            "parent": spec["parent"],
            "mutation_kind": spec["mutation_kind"],
            "flipped_offset": spec["flipped_offset"],
            "to_direction": spec["to_direction"],
            "seed_removed_root_hole": 139,
            "gates": cached_outer["gates"],
            "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
        },
        "outer_code": {
            "parameters": {"n": outer.n, "k": outer.k},
            "distance_audit_weight3": cached_outer["distance_audit_weight3"],
        },
        "code_pair": {"n": first.n, "k": first.k},
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
        "summary": summary,
        "records": record_tuple,
        "selected_entropy_matched_record": selected_entropy_matched_record,
        "selected_admissible_hit_record": selected_admissible_hit_record,
        "operator_or_channel_split_records": tuple(split_records),
        "admissible_hit_records": tuple(admissible_hit_records),
    }


def holographic_phase38_pair_record(
    *,
    pair_spec: dict[str, object],
    outer_variant_cache: dict[str, dict[str, object]],
    network_spec: dict[str, object],
    region_specs: tuple[dict[str, object], ...],
    region_mincut_cache: dict[str, dict[str, object]],
) -> dict[str, object]:
    variant_records = tuple(
        holographic_phase38_variant_record(
            pair_spec=pair_spec,
            spec=cached_outer["spec"],  # type: ignore[arg-type]
            cached_outer=cached_outer,
            network_spec=network_spec,
            region_specs=region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for cached_outer in outer_variant_cache.values()
    )
    all_records = tuple(record for variant in variant_records for record in variant["records"])  # type: ignore[index]
    split_records = tuple(
        record for variant in variant_records for record in variant["operator_or_channel_split_records"]  # type: ignore[index]
    )
    admissible_hits = tuple(
        record for variant in variant_records for record in variant["admissible_hit_records"]  # type: ignore[index]
    )
    summary = {
        "seed_base_records": sum(
            int(variant["summary"]["seed_base_records"]) for variant in variant_records  # type: ignore[index]
        ),
        "candidate_q139_support_records": len(all_records),
        "same_leaf_two_private_add_records": sum(
            1 for record in all_records if record["phase38_edit"] == "same_leaf_two_private_add"
        ),
        "cross_leaf_private_add_records": sum(
            1 for record in all_records if record["phase38_edit"] == "cross_leaf_private_add"
        ),
        "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
        "operator_channel_checked_records": sum(1 for record in all_records if record["operator_channel_checked"]),
        "q139_support_entropy_gate_rejections": sum(
            1 for record in all_records if not record["operator_channel_checked"]
        ),
        "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
        "operator_or_channel_split_records": len(split_records),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
        "channel_visible_admissible_hits": sum(
            1 for record in admissible_hits if record["channel_visible_admissible_hit"]
        ),
        "operator_only_admissible_hits": sum(
            1 for record in admissible_hits if record["operator_only_admissible_hit"]
        ),
        "distance_three_witness_variants": sum(
            1
            for variant in variant_records
            if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
        ),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in all_records),
    }
    return {
        "pair": holographic_phase34_source_pair_public(pair_spec),
        "summary": summary,
        "variant_records": variant_records,
        "selected_entropy_matched_record": next(
            (
                variant["selected_entropy_matched_record"]
                for variant in variant_records
                if variant["selected_entropy_matched_record"] is not None
            ),
            None,
        ),
        "selected_admissible_hit_record": next(
            (
                variant["selected_admissible_hit_record"]
                for variant in variant_records
                if variant["selected_admissible_hit_record"] is not None
            ),
            None,
        ),
        "operator_or_channel_split_records": split_records,
        "admissible_hit_records": admissible_hits,
    }


def bridge_holography_phase38_certificate(
    *,
    graph_max_codes: int = 64,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    source_ordinals = ((16, 23), (21, 27), (26, 27))
    pair_specs, source_scan = holographic_phase36_source_pairs(
        graph_max_codes=graph_max_codes,
        source_ordinals=source_ordinals,
    )

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    base_region_specs = holographic_phase24_punctured_region_specs()
    q139_base_region_specs = tuple(
        region_spec for region_spec in base_region_specs if int(region_spec["removed_root_qubit"]) == 139
    )
    variant_names = holographic_phase38_variant_names()
    variant_specs = tuple(
        spec for spec in holographic_phase26_offset_flip_neighborhood_specs() if str(spec["name"]) in variant_names
    )
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=variant_specs)
    q139_support_region_specs = holographic_phase38_all_q139_support_region_specs(base_region_specs)
    region_mincut_cache = holographic_phase38_region_mincut_cache(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_specs=q139_support_region_specs,
    )
    pair_records = tuple(
        holographic_phase38_pair_record(
            pair_spec=pair_spec,
            outer_variant_cache=outer_variant_cache,
            network_spec=networks[0],
            region_specs=q139_base_region_specs,
            region_mincut_cache=region_mincut_cache,
        )
        for pair_spec in pair_specs
    )
    variant_records = tuple(
        variant for pair in pair_records for variant in pair["variant_records"]  # type: ignore[index]
    )
    all_records = tuple(
        record for pair in pair_records for variant in pair["variant_records"] for record in variant["records"]  # type: ignore[index]
    )
    operator_checked_records = tuple(record for record in all_records if record["operator_channel_checked"])
    admissible_hits = tuple(
        record for pair in pair_records for record in pair["admissible_hit_records"]  # type: ignore[index]
    )
    split_records = tuple(
        record for pair in pair_records for record in pair["operator_or_channel_split_records"]  # type: ignore[index]
    )
    pair_candidate_profile = {
        str(record["pair"]["name"]): int(record["summary"]["candidate_q139_support_records"])  # type: ignore[index]
        for record in pair_records
    }
    pair_admissible_profile = {
        str(record["pair"]["name"]): int(record["summary"]["admissible_entropy_match_min_cut_operator_hits"])  # type: ignore[index]
        for record in pair_records
    }
    variant_names_present = tuple(dict.fromkeys(str(record["variant"]["name"]) for record in variant_records))  # type: ignore[index]
    variant_candidate_profile = {
        name: sum(
            int(record["summary"]["candidate_q139_support_records"])  # type: ignore[index]
            for record in variant_records
            if str(record["variant"]["name"]) == name  # type: ignore[index]
        )
        for name in variant_names_present
    }
    variant_admissible_profile = {
        name: sum(
            int(record["summary"]["admissible_entropy_match_min_cut_operator_hits"])  # type: ignore[index]
            for record in variant_records
            if str(record["variant"]["name"]) == name  # type: ignore[index]
        )
        for name in variant_names_present
    }
    edit_candidate_profile = holographic_phase37_profile(all_records, ("phase38_edit",))
    edit_admissible_profile = holographic_phase37_profile(admissible_hits, ("phase38_edit",))
    entropy_pair_profile = {
        str(pair): sum(1 for record in all_records if record["entropy_pair"] == pair)
        for pair in sorted({record["entropy_pair"] for record in all_records})  # type: ignore[type-var]
    }
    admissible_entropy_pair_profile = {
        str(pair): sum(1 for record in admissible_hits if record["entropy_pair"] == pair)
        for pair in sorted({record["entropy_pair"] for record in admissible_hits})  # type: ignore[type-var]
    }
    min_cut_value_profile = {
        str(values): sum(1 for record in all_records if record["min_cut_values"] == values)
        for values in sorted({record["min_cut_values"] for record in all_records})  # type: ignore[type-var]
    }
    admissible_min_cut_value_profile = {
        str(values): sum(1 for record in admissible_hits if record["min_cut_values"] == values)
        for values in sorted({record["min_cut_values"] for record in admissible_hits})  # type: ignore[type-var]
    }
    admissible_leaf_profile = {
        str(leaf): sum(1 for record in admissible_hits if str(record["base_region"]["perfect_cells"][1]) == str(leaf))  # type: ignore[index]
        for leaf in range(5)
    }
    admissible_offset_profile = {
        str(offsets): sum(
            1
            for record in admissible_hits
            if record["region"]["added_leaf_private_offsets"] == offsets  # type: ignore[index]
        )
        for offsets in sorted({record["region"]["added_leaf_private_offsets"] for record in admissible_hits})  # type: ignore[type-var]
    }
    channel_visibility_profile = {
        "channel_visible": sum(1 for record in admissible_hits if record["channel_visible_admissible_hit"]),
        "operator_only": sum(1 for record in admissible_hits if record["operator_only_admissible_hit"]),
    }
    phase_claims = {
        "phase37_q139_seed_surface_reused": tuple(pair["source_ordinals"] for pair in pair_specs) == source_ordinals
        and len(q139_base_region_specs) == 5
        and len(variant_specs) == 5
        and sum(int(record["summary"]["seed_base_records"]) for record in pair_records) == 75,  # type: ignore[index]
        "q139_support_scale_grammar_bounded": len(q139_support_region_specs) == 110
        and edit_candidate_profile
        == {"cross_leaf_private_add": 1200, "same_leaf_two_private_add": 450},
        "q139_frontier_exhausted": len(pair_records) == 3
        and len(variant_records) == 15
        and len(all_records) == 1650,
        "all_q139_support_mincuts_exact_and_variable": all(record["all_mincuts_exact"] for record in all_records)
        and sum(1 for record in all_records if record["min_cut_variable"]) == 1650,
        "strict_holographic_cousin_hits_found": len(admissible_hits) == 25
        and len(operator_checked_records) == 25
        and len(split_records) == 25,
        "strict_hits_localized_to_source_21_27_and_same_leaf_0_3": pair_admissible_profile
        == {
            "graph_cws_labeled_source_ord16_ord23": 0,
            "graph_cws_labeled_source_ord21_ord27": 25,
            "graph_cws_labeled_source_ord26_ord27": 0,
        }
        and edit_admissible_profile == {"same_leaf_two_private_add": 25}
        and admissible_offset_profile == {"(0, 3)": 25},
        "strict_hits_repeat_across_variants_and_leaf_cells": set(variant_admissible_profile.values()) == {5}
        and admissible_leaf_profile == {"0": 5, "1": 5, "2": 5, "3": 5, "4": 5},
        "strict_hits_classified_by_channel_visibility": channel_visibility_profile
        == {"channel_visible": 15, "operator_only": 10},
    }
    phase_claims["goal_3_phase_38_q139_support_scale_strict_hit_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 3 Phase 38: q139 support-scale strict holographic-cousin hits",
        "status": "pass"
        if phase_claims["goal_3_phase_38_q139_support_scale_strict_hit_certificate"]
        else "fail",
        "source_atlas": source_scan,
        "selected_source_pairs": tuple(holographic_phase34_source_pair_public(pair) for pair in pair_specs),
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "q139_base_punctured_regions": q139_base_region_specs,
            "q139_support_region_specs": q139_support_region_specs,
            "capacity_profiles": capacity_profiles,
            "region_mincut_cache": {
                key: {subkey: value for subkey, value in record.items() if subkey != "mask"}
                for key, record in region_mincut_cache.items()
            },
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 37 split-support region grammar",
            "bridge_axis": bridge_axis,
            "source_pair_ordinals": source_ordinals,
            "candidate_parent_variants": variant_names,
            "region_grammar": (
                "Restrict to the q139-heavy Phase 37 seed surface. For each seed, add either two same-leaf private "
                "qubits from offsets 0..3 or one cross-leaf private qubit on another leaf cell."
            ),
            "filter_order": (
                "reuse the q139 Phase 36/37 seed surface",
                "generate bounded same-leaf two-private and cross-leaf one-private support-scale edits",
                "score exact entropy and exact min-cut variation for every adapted region",
                "run exact algebra, erasure, and survivor checks for entropy-matched records",
                "certify strict hits by entropy match, min-cut variability, and operator/channel split",
            ),
        },
        "q139_support_frontier": {
            "pair_records": pair_records,
            "pair_candidate_profile": pair_candidate_profile,
            "pair_admissible_profile": pair_admissible_profile,
            "variant_candidate_profile": variant_candidate_profile,
            "variant_admissible_profile": variant_admissible_profile,
            "edit_candidate_profile": edit_candidate_profile,
            "edit_admissible_profile": edit_admissible_profile,
            "entropy_pair_profile": entropy_pair_profile,
            "admissible_entropy_pair_profile": admissible_entropy_pair_profile,
            "min_cut_value_profile": min_cut_value_profile,
            "admissible_min_cut_value_profile": admissible_min_cut_value_profile,
            "admissible_leaf_profile": admissible_leaf_profile,
            "admissible_offset_profile": admissible_offset_profile,
            "channel_visibility_profile": channel_visibility_profile,
            "operator_or_channel_split_records": split_records,
            "admissible_hit_records": admissible_hits,
        },
        "counts": {
            "source_pairs_loaded": len(pair_records),
            "raw_graph_codes": source_scan["raw_codes"],  # type: ignore[index]
            "relaxed_codes_checked": source_scan["codes_checked"],  # type: ignore[index]
            "source_pair_ordinals": source_ordinals,
            "q139_base_regions": len(q139_base_region_specs),
            "seed_alternating_variants": len(variant_specs),
            "seed_base_records": sum(int(record["summary"]["seed_base_records"]) for record in pair_records),  # type: ignore[index]
            "unique_q139_support_region_specs": len(q139_support_region_specs),
            "edit_kinds": len(edit_candidate_profile),
            "candidate_q139_support_records": len(all_records),
            "same_leaf_two_private_add_records": edit_candidate_profile["same_leaf_two_private_add"],
            "cross_leaf_private_add_records": edit_candidate_profile["cross_leaf_private_add"],
            "capacity_profiles_scored": len(capacity_profiles),
            "entropy_match_records": sum(1 for record in all_records if record["entropy_matches"]),
            "entropy_mismatch_records": sum(1 for record in all_records if not record["entropy_matches"]),
            "operator_channel_checked_records": len(operator_checked_records),
            "q139_support_entropy_gate_rejections": sum(
                1 for record in all_records if not record["operator_channel_checked"]
            ),
            "min_cut_variable_records": sum(1 for record in all_records if record["min_cut_variable"]),
            "operator_or_channel_split_records_checked": len(split_records),
            "admissible_entropy_match_min_cut_operator_hits": len(admissible_hits),
            "channel_visible_admissible_hits": channel_visibility_profile["channel_visible"],
            "operator_only_admissible_hits": channel_visibility_profile["operator_only"],
            "distance_three_witness_source_variants": sum(
                1
                for variant in variant_records
                if variant["outer_code"]["distance_audit_weight3"]["distance_exact_if_witness_found"] == 3  # type: ignore[index]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The q139 support-scale scout scores 1650 exact candidates and finds 25 strict hits. All strict "
                "hits are entropy-matched, min-cut-variable, and operator/reconstruction-visible splits; 15 are "
                "also channel-visible. They localize to source pair (21,27), same-leaf private offsets (0,3), and "
                "repeat once per leaf cell for each alternating offset-flip variant."
            ),
            "three_geometry_lesson": (
                "This is the first finite tensor-network/holographic-code layer in the Goal 3 search where "
                "entropy/min-cut-visible geometry agrees while observer reconstruction and, for most hits, "
                "channel/erasure-visible geometry differs. It is a small exact holographic cousin of the "
                "balanced-bridge phenomenon."
            ),
            "scope_warning": (
                "The certificate is exact for this bounded q139 grammar, source atlas limit, Y-axis interface "
                "star, and Phase 26 alternating variants. It does not prove minimality, robustness under all "
                "nearby region edits, other bridge axes, or an infinite family."
            ),
        },
        "recommendation": {
            "next_phase": "proceed",
            "reason": (
                "A strict finite holographic-cousin candidate has been found. The next phase should validate and "
                "compress it: isolate the smallest representative record, audit nearby single-qubit deletions and "
                "alternative offsets, and prepare a human-facing certificate/memo of the exact separation."
            ),
            "suggested_phase_39": (
                "Run a minimality/robustness audit around the same-leaf offsets (0,3) hits for source pair (21,27), "
                "including one-hit extraction, local deletion/addition neighbors, and concise theorem-style export."
            ),
        },
    }


def holographic_phase39_representative_source_ordinals() -> tuple[int, int]:
    return (21, 27)


def holographic_phase39_representative_variant_name() -> str:
    return "alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root"


def holographic_phase39_representative_base_region(
    region_specs: tuple[dict[str, object], ...],
) -> dict[str, object]:
    return next(
        region_spec
        for region_spec in region_specs
        if int(region_spec["leaf_cell"]) == 0 and int(region_spec["removed_root_qubit"]) == 139
    )


def holographic_phase39_representative_region_spec(
    base_region_spec: dict[str, object],
) -> dict[str, object]:
    return next(
        spec
        for spec in holographic_phase38_same_leaf_two_private_add_specs(base_region_spec)
        if tuple(spec["added_leaf_private_offsets"]) == (0, 3)
    )


def holographic_phase39_deletion_neighbor_specs(
    representative_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    qubits = tuple(int(qubit) for qubit in representative_spec["qubits"])  # type: ignore[index]
    return tuple(
        {
            **representative_spec,
            "name": f"{representative_spec['name']}__phase39_delete_q{qubit}",
            "region_type": "phase39_representative_single_delete",
            "phase39_edit": "single_delete",
            "deleted_qubit": qubit,
            "qubits": tuple(candidate for candidate in qubits if candidate != qubit),
            "description": f"Phase 39 local deletion neighbor of the representative hit: remove q{qubit}.",
        }
        for qubit in qubits
    )


def holographic_phase39_local_addition_qubits() -> tuple[int, ...]:
    return (139, 1, 2) + tuple(leaf * 25 + offset for leaf in range(1, 5) for offset in range(4))


def holographic_phase39_local_addition_neighbor_specs(
    representative_spec: dict[str, object],
) -> tuple[dict[str, object], ...]:
    qubits = set(int(qubit) for qubit in representative_spec["qubits"])  # type: ignore[index]
    specs: list[dict[str, object]] = []
    for qubit in holographic_phase39_local_addition_qubits():
        if qubit in qubits:
            continue
        perfect_cells = set(int(cell) for cell in representative_spec["perfect_cells"])  # type: ignore[index]
        perfect_cells.add(5 if qubit >= 125 else qubit // 25)
        specs.append(
            {
                **representative_spec,
                "name": f"{representative_spec['name']}__phase39_add_q{qubit}",
                "region_type": "phase39_representative_local_single_add",
                "phase39_edit": "single_add",
                "added_qubit": qubit,
                "perfect_cells": tuple(sorted(perfect_cells)),
                "qubits": tuple(sorted(qubits | {qubit})),
                "description": f"Phase 39 bounded local addition neighbor of the representative hit: add q{qubit}.",
            }
        )
    return tuple(specs)


def holographic_phase39_region_payload(region_spec: dict[str, object]) -> dict[str, object]:
    payload = holographic_phase23_region_payload(region_spec)
    extra_keys = (
        "phase38_edit",
        "phase39_edit",
        "leaf_cell",
        "removed_root_qubit",
        "removed_root_offset",
        "added_leaf_private_qubits",
        "added_leaf_private_offsets",
        "deleted_qubit",
        "added_qubit",
    )
    return {
        **payload,
        **{key: region_spec[key] for key in extra_keys if key in region_spec},
    }


def holographic_phase39_mincut_record(
    *,
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_mask: int,
) -> dict[str, object]:
    min_cut_values_by_capacity = holographic_phase23_mincut_values(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=region_mask,
    )
    min_cut_values = tuple(sorted({int(record["value"]) for record in min_cut_values_by_capacity}))
    all_mincuts_exact = all(
        int(holographic_network_min_cut(network_spec=network, region_mask=region_mask)["assignments_checked"])
        == 2 ** len(network["internal_nodes"])  # type: ignore[arg-type]
        for network in networks
    )
    return {
        "min_cut_values_by_capacity": min_cut_values_by_capacity,
        "min_cut_values": min_cut_values,
        "min_cut_variable": len(min_cut_values) > 1,
        "all_mincuts_exact": all_mincuts_exact,
    }


def holographic_phase39_exact_record(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    network_spec: dict[str, object],
    networks: tuple[dict[str, object], ...],
    capacity_profiles: tuple[tuple[int, int, int, int, int], ...],
    region_spec: dict[str, object],
    record_kind: str,
) -> dict[str, object]:
    region = holographic_phase39_region_payload(region_spec)
    region_mask = int(region["mask"])
    first_entropy = first.entropy(region_mask)
    second_entropy = second.entropy(region_mask)
    entropy_matches = first_entropy == second_entropy
    mincut = holographic_phase39_mincut_record(
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_mask=region_mask,
    )
    hit = (
        holographic_phase7_hit_record(
            circuit={
                "name": str(region["name"]),
                "generator_kind": "phase39_representative_witness_robustness",
            },
            first=first,
            second=second,
            network_spec=network_spec,
            region=region,
        )
        if entropy_matches
        else None
    )
    operator_or_channel_split = bool(
        hit is not None and hit["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
    )
    channel_visible_split = bool(hit is not None and hit["comparisons"]["channel_visible_differs"])  # type: ignore[index]
    return {
        "record_kind": record_kind,
        "region": {key: value for key, value in region.items() if key != "mask"},
        "entropy_pair": (first_entropy, second_entropy),
        "entropy_matches": entropy_matches,
        "operator_channel_checked": entropy_matches,
        "min_cut_values_by_capacity": mincut["min_cut_values_by_capacity"],
        "min_cut_values": mincut["min_cut_values"],
        "min_cut_variable": mincut["min_cut_variable"],
        "all_mincuts_exact": mincut["all_mincuts_exact"],
        "hit": hit,
        "admissible_entropy_match_min_cut_operator_hit": bool(
            entropy_matches and mincut["min_cut_variable"] and operator_or_channel_split
        ),
        "channel_visible_admissible_hit": bool(
            entropy_matches and mincut["min_cut_variable"] and channel_visible_split
        ),
        "operator_only_admissible_hit": bool(
            entropy_matches
            and mincut["min_cut_variable"]
            and operator_or_channel_split
            and not channel_visible_split
        ),
        "strict_filter_stage": "operator_channel_checked" if entropy_matches else "phase39_entropy_gate_rejected",
    }


def holographic_phase39_bucket_summary(records: tuple[dict[str, object], ...]) -> dict[str, object]:
    admissible = tuple(record for record in records if record["admissible_entropy_match_min_cut_operator_hit"])
    return {
        "records": len(records),
        "entropy_match_records": sum(1 for record in records if record["entropy_matches"]),
        "entropy_mismatch_records": sum(1 for record in records if not record["entropy_matches"]),
        "operator_channel_checked_records": sum(1 for record in records if record["operator_channel_checked"]),
        "min_cut_variable_records": sum(1 for record in records if record["min_cut_variable"]),
        "all_mincuts_exact": all(record["all_mincuts_exact"] for record in records),
        "operator_or_channel_split_records": sum(
            1
            for record in records
            if record["hit"] is not None
            and record["hit"]["comparisons"]["operator_or_channel_visible_differs"]  # type: ignore[index]
        ),
        "admissible_entropy_match_min_cut_operator_hits": len(admissible),
        "channel_visible_admissible_hits": sum(1 for record in admissible if record["channel_visible_admissible_hit"]),
        "operator_only_admissible_hits": sum(1 for record in admissible if record["operator_only_admissible_hit"]),
    }


def holographic_phase39_qubit_profile(
    records: tuple[dict[str, object], ...],
    qubit_key: str,
) -> tuple[int, ...]:
    return tuple(
        int(record["region"][qubit_key])
        for record in records
        if record["admissible_entropy_match_min_cut_operator_hit"] and qubit_key in record["region"]  # type: ignore[operator]
    )


def bridge_holography_phase39_certificate(
    *,
    graph_max_codes: int = 64,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    source_ordinals = (holographic_phase39_representative_source_ordinals(),)
    pair_specs, source_scan = holographic_phase36_source_pairs(
        graph_max_codes=graph_max_codes,
        source_ordinals=source_ordinals,
    )
    pair_spec = pair_specs[0]

    bridge_axis = "Y"
    base_outer = holographic_phase23_interface_outer_code(bridge_axis=bridge_axis)
    base_outer_summary = holographic_phase23_outer_code_summary(base_outer, bridge_axis=bridge_axis)
    variant_name = holographic_phase39_representative_variant_name()
    variant_spec = next(
        spec for spec in holographic_phase26_offset_flip_neighborhood_specs() if str(spec["name"]) == variant_name
    )
    outer_variant_cache = holographic_phase32_outer_variant_cache(base_outer=base_outer, variant_specs=(variant_spec,))
    cached_outer = outer_variant_cache[variant_name]
    outer = cached_outer["outer"]
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 39 outer cache is malformed")
    first, first_metadata = logical_concatenate_k1(pair_spec["first"], outer)  # type: ignore[arg-type]
    second, second_metadata = logical_concatenate_k1(pair_spec["second"], outer)  # type: ignore[arg-type]

    template_by_name = {str(template["name"]): template for template in holographic_phase23_boundary_templates()}
    boundary_order = tuple(int(qubit) for qubit in template_by_name["interface_star_cell_major"]["boundary_order"])  # type: ignore[index]
    capacity_profiles = holographic_phase23_capacity_profiles()
    networks = tuple(
        holographic_phase23_interface_network_spec(boundary_order, capacities=capacities)
        for capacities in capacity_profiles
    )
    base_region_specs = holographic_phase24_punctured_region_specs()
    base_region_spec = holographic_phase39_representative_base_region(base_region_specs)
    representative_spec = holographic_phase39_representative_region_spec(base_region_spec)
    representative_record = holographic_phase39_exact_record(
        first=first,
        second=second,
        network_spec=networks[0],
        networks=networks,
        capacity_profiles=capacity_profiles,
        region_spec=representative_spec,
        record_kind="representative_hit",
    )
    alternative_offset_records = tuple(
        holographic_phase39_exact_record(
            first=first,
            second=second,
            network_spec=networks[0],
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_spec=spec,
            record_kind="alternative_same_leaf_offset",
        )
        for spec in holographic_phase38_same_leaf_two_private_add_specs(base_region_spec)
    )
    deletion_records = tuple(
        holographic_phase39_exact_record(
            first=first,
            second=second,
            network_spec=networks[0],
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_spec=spec,
            record_kind="single_deletion_neighbor",
        )
        for spec in holographic_phase39_deletion_neighbor_specs(representative_spec)
    )
    addition_records = tuple(
        holographic_phase39_exact_record(
            first=first,
            second=second,
            network_spec=networks[0],
            networks=networks,
            capacity_profiles=capacity_profiles,
            region_spec=spec,
            record_kind="local_single_addition_neighbor",
        )
        for spec in holographic_phase39_local_addition_neighbor_specs(representative_spec)
    )
    neighborhood_records = alternative_offset_records + deletion_records + addition_records
    neighborhood_admissible = tuple(
        record for record in neighborhood_records if record["admissible_entropy_match_min_cut_operator_hit"]
    )
    alternative_summary = holographic_phase39_bucket_summary(alternative_offset_records)
    deletion_summary = holographic_phase39_bucket_summary(deletion_records)
    addition_summary = holographic_phase39_bucket_summary(addition_records)
    all_records = (representative_record,) + neighborhood_records
    deletion_strict_qubits = holographic_phase39_qubit_profile(deletion_records, "deleted_qubit")
    addition_strict_qubits = holographic_phase39_qubit_profile(addition_records, "added_qubit")
    phase_claims = {
        "phase38_representative_loaded": tuple(pair_spec["source_ordinals"]) == (21, 27)
        and representative_record["region"]["name"]
        == "root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3"
        and representative_record["entropy_pair"] == (4, 4)
        and representative_record["min_cut_values"] == (9, 11, 13, 14, 17, 19)
        and representative_record["admissible_entropy_match_min_cut_operator_hit"]
        and representative_record["channel_visible_admissible_hit"],
        "alternative_offsets_certify_unique_pair_0_3": alternative_summary["records"] == 6
        and alternative_summary["admissible_entropy_match_min_cut_operator_hits"] == 1
        and all(
            record["region"]["added_leaf_private_offsets"] == (0, 3)  # type: ignore[index]
            for record in alternative_offset_records
            if record["admissible_entropy_match_min_cut_operator_hit"]
        ),
        "single_deletion_plateau_audited": deletion_summary["records"] == 27
        and deletion_summary["admissible_entropy_match_min_cut_operator_hits"] == 15
        and deletion_summary["channel_visible_admissible_hits"] == 15,
        "local_single_addition_plateau_audited": addition_summary["records"] == 19
        and addition_summary["admissible_entropy_match_min_cut_operator_hits"] == 18
        and addition_summary["channel_visible_admissible_hits"] == 18
        and tuple(record["region"]["added_qubit"] for record in addition_records if not record["entropy_matches"]) == (139,),  # type: ignore[index]
        "all_phase39_records_exact_and_capacity_sensitive": all(record["all_mincuts_exact"] for record in all_records)
        and all(record["min_cut_variable"] for record in all_records),
        "representative_is_not_locally_minimal_but_is_robust": len(neighborhood_admissible) == 34
        and deletion_summary["admissible_entropy_match_min_cut_operator_hits"] > 0
        and addition_summary["admissible_entropy_match_min_cut_operator_hits"] > 0,
    }
    phase_claims["goal_3_phase_39_representative_witness_robustness_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 39: representative strict-hit robustness certificate",
        "status": "pass"
        if phase_claims["goal_3_phase_39_representative_witness_robustness_certificate"]
        else "fail",
        "source_atlas": source_scan,
        "representative": {
            "source_pair": holographic_phase34_source_pair_public(pair_spec),
            "bridge_axis": bridge_axis,
            "variant": {
                "name": variant_spec["name"],
                "parent": variant_spec["parent"],
                "mutation_kind": variant_spec["mutation_kind"],
                "flipped_offset": variant_spec["flipped_offset"],
                "to_direction": variant_spec["to_direction"],
                "gates": cached_outer["gates"],
                "gate_count": len(cached_outer["gates"]),  # type: ignore[arg-type]
            },
            "outer_code": {
                "parameters": {"n": outer.n, "k": outer.k},
                "distance_audit_weight3": cached_outer["distance_audit_weight3"],
            },
            "code_pair": {"n": first.n, "k": first.k},
            "concatenation": {
                "first": first_metadata,
                "second": second_metadata,
            },
            "base_region": base_region_spec,
            "record": representative_record,
        },
        "base_interface_star": {
            "outer_code": base_outer_summary,
            "capacity_profiles": capacity_profiles,
        },
        "search_scope": {
            "parent_certificate": "Goal 3 Phase 38 q139 support-scale strict-hit certificate",
            "region_grammar": (
                "Compress the first Phase 38 strict hit, then audit same-leaf offset alternatives, every one-qubit "
                "deletion from the representative region, and a bounded local one-qubit addition set."
            ),
            "filter_order": (
                "extract the canonical source (21,27), offset-0, leaf-0, q139, offsets-(0,3) hit",
                "score exact entropy and exact min-cut variation for every neighbor",
                "run exact algebra, erasure, and survivor checks for entropy-matched neighbors",
                "classify whether the witness is unique among offsets, locally minimal, or robust",
            ),
        },
        "robustness_frontier": {
            "alternative_offset_records": alternative_offset_records,
            "single_deletion_records": deletion_records,
            "local_single_addition_records": addition_records,
            "neighborhood_admissible_records": neighborhood_admissible,
            "alternative_offset_summary": alternative_summary,
            "single_deletion_summary": deletion_summary,
            "local_single_addition_summary": addition_summary,
            "strict_deletion_qubits": deletion_strict_qubits,
            "strict_addition_qubits": addition_strict_qubits,
            "alternative_entropy_pair_profile": holographic_phase37_profile(
                alternative_offset_records, ("entropy_pair",)
            ),
            "deletion_entropy_pair_profile": holographic_phase37_profile(deletion_records, ("entropy_pair",)),
            "addition_entropy_pair_profile": holographic_phase37_profile(addition_records, ("entropy_pair",)),
            "deletion_min_cut_value_profile": holographic_phase37_profile(deletion_records, ("min_cut_values",)),
            "addition_min_cut_value_profile": holographic_phase37_profile(addition_records, ("min_cut_values",)),
        },
        "counts": {
            "source_pairs_loaded": len(pair_specs),
            "raw_graph_codes": source_scan["raw_codes"],  # type: ignore[index]
            "relaxed_codes_checked": source_scan["codes_checked"],  # type: ignore[index]
            "representative_region_length": representative_record["region"]["length"],
            "capacity_profiles_scored": len(capacity_profiles),
            "alternative_offset_records": alternative_summary["records"],
            "alternative_offset_admissible_hits": alternative_summary[
                "admissible_entropy_match_min_cut_operator_hits"
            ],
            "single_deletion_records": deletion_summary["records"],
            "single_deletion_admissible_hits": deletion_summary[
                "admissible_entropy_match_min_cut_operator_hits"
            ],
            "local_single_addition_records": addition_summary["records"],
            "local_single_addition_admissible_hits": addition_summary[
                "admissible_entropy_match_min_cut_operator_hits"
            ],
            "neighborhood_records": len(neighborhood_records),
            "neighborhood_admissible_hits": len(neighborhood_admissible),
            "all_records_including_representative": len(all_records),
            "all_records_exact": sum(1 for record in all_records if record["all_mincuts_exact"]),
            "all_records_min_cut_variable": sum(1 for record in all_records if record["min_cut_variable"]),
            "channel_visible_neighbor_hits": sum(
                1 for record in neighborhood_admissible if record["channel_visible_admissible_hit"]
            ),
            "operator_only_neighbor_hits": sum(
                1 for record in neighborhood_admissible if record["operator_only_admissible_hit"]
            ),
            "max_candidate_min_cut_internal_assignments": max(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
            "min_candidate_min_cut_internal_assignments": min(
                2 ** len(network["internal_nodes"]) for network in networks  # type: ignore[arg-type]
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 39 extracts the canonical Phase 38 hit and audits 52 exact local neighbors. The same-leaf "
                "offset pair (0,3) is unique among the six offset alternatives. The witness is not locally minimal: "
                "15 one-qubit deletions and 18 bounded local one-qubit additions remain strict channel-visible hits."
            ),
            "three_geometry_lesson": (
                "The strict holographic-cousin separation is not a single accidental boundary set. It sits in a "
                "small local plateau where entropy/min-cut-visible geometry remains matched while reconstruction "
                "and channel-visible semantics differ."
            ),
            "scope_warning": (
                "The audit is local to one representative source pair, one alternating variant, one leaf cell, "
                "same-leaf offset alternatives, all single deletions from that representative, and a bounded local "
                "addition set. It does not prove global minimality or all-neighborhood robustness."
            ),
        },
        "recommendation": {
            "next_phase": "proceed",
            "reason": (
                "The representative is compact enough to explain and robust enough not to be a one-record artifact. "
                "The next phase should export the theorem-style human memo and optionally reduce the plateau to "
                "the smallest visually legible witness family."
            ),
            "suggested_phase_40": (
                "Generate the human-facing Phase 38/39 theorem memo and a compact JSON index of the representative "
                "hit plus its robust deletion/addition plateau."
            ),
        },
    }


def bridge_holography_phase40_certificate(
    *,
    graph_max_codes: int = 64,
) -> dict[str, object]:
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    phase38 = bridge_holography_phase38_certificate(graph_max_codes=graph_max_codes)
    phase39 = bridge_holography_phase39_certificate(graph_max_codes=graph_max_codes)
    phase38_counts = phase38["counts"]
    phase39_counts = phase39["counts"]
    phase38_frontier = phase38["q139_support_frontier"]
    phase39_frontier = phase39["robustness_frontier"]
    representative = phase39["representative"]
    representative_record = representative["record"]  # type: ignore[index]
    representative_comparisons = representative_record["hit"]["comparisons"]  # type: ignore[index]

    witness_index = {
        "identifier": "goal3_phase40_graph_cws_21_27_y_alternating_offset0_q139_leaf0_offsets_0_3",
        "source_pair": representative["source_pair"],  # type: ignore[index]
        "bridge_axis": representative["bridge_axis"],  # type: ignore[index]
        "outer_variant": {
            key: representative["variant"][key]  # type: ignore[index]
            for key in ("name", "parent", "mutation_kind", "flipped_offset", "to_direction", "gate_count")
        },
        "code_pair": representative["code_pair"],  # type: ignore[index]
        "region": representative_record["region"],  # type: ignore[index]
        "entropy_pair": representative_record["entropy_pair"],  # type: ignore[index]
        "min_cut_values": representative_record["min_cut_values"],  # type: ignore[index]
        "diagnostic_separation": {
            "entropy_matches": representative_comparisons["entropy_matches"],  # type: ignore[index]
            "min_cut_variable": representative_record["min_cut_variable"],  # type: ignore[index]
            "reconstruction_visible_differs": representative_comparisons["reconstruction_visible_differs"],  # type: ignore[index]
            "erasure_correctability_differs": representative_comparisons["erasure_correctability_differs"],  # type: ignore[index]
            "survivor_fixed_point_differs": representative_comparisons["survivor_fixed_point_differs"],  # type: ignore[index]
            "channel_visible_differs": representative_comparisons["channel_visible_differs"],  # type: ignore[index]
            "operator_or_channel_visible_differs": representative_comparisons[
                "operator_or_channel_visible_differs"
            ],  # type: ignore[index]
        },
    }
    proof_obligations = {
        "entropy_visible_geometry": {
            "requirement": "The two codes have the same entropy on the representative boundary region.",
            "evidence": representative_record["entropy_pair"],  # type: ignore[index]
            "satisfied": representative_comparisons["entropy_matches"],  # type: ignore[index]
        },
        "min_cut_visible_geometry": {
            "requirement": "The region is evaluated by exact finite min-cut checks and remains capacity-sensitive.",
            "evidence": representative_record["min_cut_values"],  # type: ignore[index]
            "satisfied": bool(
                representative_record["all_mincuts_exact"] and representative_record["min_cut_variable"]  # type: ignore[index]
            ),
        },
        "observer_reconstruction_geometry": {
            "requirement": "The exact region algebra/reconstruction diagnostic differs between the two codes.",
            "evidence": representative_comparisons["reconstruction_visible_differs"],  # type: ignore[index]
            "satisfied": representative_comparisons["reconstruction_visible_differs"],  # type: ignore[index]
        },
        "channel_erasure_geometry": {
            "requirement": "The exact erasure/survivor channel diagnostic differs for the representative.",
            "evidence": {
                "erasure_correctability_differs": representative_comparisons["erasure_correctability_differs"],  # type: ignore[index]
                "survivor_fixed_point_differs": representative_comparisons["survivor_fixed_point_differs"],  # type: ignore[index]
                "channel_visible_differs": representative_comparisons["channel_visible_differs"],  # type: ignore[index]
            },
            "satisfied": representative_comparisons["channel_visible_differs"],  # type: ignore[index]
        },
        "family_support": {
            "requirement": "The representative is part of a certified finite strict-hit family, not a lone record.",
            "evidence": {
                "phase38_admissible_hits": phase38_counts["admissible_entropy_match_min_cut_operator_hits"],  # type: ignore[index]
                "phase38_channel_visible_hits": phase38_counts["channel_visible_admissible_hits"],  # type: ignore[index]
                "variant_admissible_profile": phase38_frontier["variant_admissible_profile"],  # type: ignore[index]
                "leaf_profile": phase38_frontier["admissible_leaf_profile"],  # type: ignore[index]
            },
            "satisfied": phase38_counts["admissible_entropy_match_min_cut_operator_hits"] == 25  # type: ignore[index]
            and phase38_counts["channel_visible_admissible_hits"] == 15,  # type: ignore[index]
        },
        "local_robustness": {
            "requirement": "The representative has an exact locally audited strict-hit neighborhood.",
            "evidence": {
                "phase39_neighborhood_records": phase39_counts["neighborhood_records"],  # type: ignore[index]
                "phase39_neighborhood_admissible_hits": phase39_counts["neighborhood_admissible_hits"],  # type: ignore[index]
                "strict_deletion_qubits": phase39_frontier["strict_deletion_qubits"],  # type: ignore[index]
                "strict_addition_qubits": phase39_frontier["strict_addition_qubits"],  # type: ignore[index]
            },
            "satisfied": phase39_counts["neighborhood_records"] == 52  # type: ignore[index]
            and phase39_counts["neighborhood_admissible_hits"] == 34,  # type: ignore[index]
        },
    }
    phase_claims = {
        "phase38_strict_family_certificate_loaded": phase38["status"] == "pass"
        and phase38_counts["admissible_entropy_match_min_cut_operator_hits"] == 25  # type: ignore[index]
        and phase38_counts["channel_visible_admissible_hits"] == 15,  # type: ignore[index]
        "phase39_representative_robustness_certificate_loaded": phase39["status"] == "pass"
        and phase39_counts["neighborhood_admissible_hits"] == 34,  # type: ignore[index]
        "compact_witness_index_identifies_single_channel_visible_hit": witness_index["region"]["name"]  # type: ignore[index]
        == "root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3"
        and witness_index["entropy_pair"] == (4, 4)
        and witness_index["min_cut_values"] == (9, 11, 13, 14, 17, 19)
        and witness_index["diagnostic_separation"]["channel_visible_differs"],  # type: ignore[index]
        "three_geometry_separation_obligations_satisfied": all(
            bool(record["satisfied"]) for record in proof_obligations.values()
        ),
        "portable_docs_declared": (
            "docs/goal3_phase40_theorem_package.md",
            "docs/goal3_phase40_witness_index.json",
        ),
    }
    phase_claims["goal_3_phase_40_theorem_style_package_certificate"] = all(
        phase_claims.values()
    )
    return {
        "phase": "Goal 3 Phase 40: theorem-style holographic-cousin package",
        "status": "pass" if phase_claims["goal_3_phase_40_theorem_style_package_certificate"] else "fail",
        "theorem_style_statement": {
            "claim": (
                "Within the certified finite Phase 38/39 tensor-network code layer, there exists a boundary "
                "region whose entropy/min-cut-visible geometry agrees for two stabilizer codes while "
                "observer-reconstruction and channel-visible diagnostics differ."
            ),
            "scope": (
                "Finite exact statement for the declared graph/CWS source pair, Y-axis interface-star outer code, "
                "alternating Clifford/MERA-like outer variant, and representative plus local neighborhood."
            ),
            "not_claimed": (
                "No asymptotic theorem, global minimality theorem, all-axis robustness theorem, or universal "
                "holographic-code classification is claimed."
            ),
        },
        "source_certificates": {
            "phase38": {
                "status": phase38["status"],
                "phase": phase38["phase"],
                "counts": {
                    key: phase38_counts[key]  # type: ignore[index]
                    for key in (
                        "candidate_q139_support_records",
                        "entropy_match_records",
                        "admissible_entropy_match_min_cut_operator_hits",
                        "channel_visible_admissible_hits",
                        "operator_only_admissible_hits",
                    )
                },
                "pair_admissible_profile": phase38_frontier["pair_admissible_profile"],  # type: ignore[index]
                "variant_admissible_profile": phase38_frontier["variant_admissible_profile"],  # type: ignore[index]
            },
            "phase39": {
                "status": phase39["status"],
                "phase": phase39["phase"],
                "counts": {
                    key: phase39_counts[key]  # type: ignore[index]
                    for key in (
                        "representative_region_length",
                        "neighborhood_records",
                        "neighborhood_admissible_hits",
                        "single_deletion_admissible_hits",
                        "local_single_addition_admissible_hits",
                    )
                },
            },
        },
        "witness_index": witness_index,
        "proof_obligations": proof_obligations,
        "portable_artifacts": {
            "theorem_memo": "docs/goal3_phase40_theorem_package.md",
            "witness_index_json": "docs/goal3_phase40_witness_index.json",
            "phase38_json": "/tmp/holography_phase38.json",
            "phase39_json": "/tmp/holography_phase39.json",
            "phase40_json": "/tmp/holography_phase40.json",
        },
        "counts": {
            "source_certificates_loaded": 2,
            "strict_family_hits": phase38_counts["admissible_entropy_match_min_cut_operator_hits"],  # type: ignore[index]
            "strict_family_channel_visible_hits": phase38_counts["channel_visible_admissible_hits"],  # type: ignore[index]
            "representative_region_length": phase39_counts["representative_region_length"],  # type: ignore[index]
            "representative_entropy": representative_record["entropy_pair"],  # type: ignore[index]
            "representative_min_cut_values": representative_record["min_cut_values"],  # type: ignore[index]
            "neighborhood_records": phase39_counts["neighborhood_records"],  # type: ignore[index]
            "neighborhood_admissible_hits": phase39_counts["neighborhood_admissible_hits"],  # type: ignore[index]
            "proof_obligations": len(proof_obligations),
            "proof_obligations_satisfied": sum(1 for record in proof_obligations.values() if record["satisfied"]),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 40 packages the Phase 38 strict-hit family and Phase 39 representative plateau into a "
                "portable theorem-style witness index. The package certifies the desired three-geometry split for "
                "one compact representative and records the supporting finite family and local robustness evidence."
            ),
            "three_geometry_lesson": (
                "The Goal 1/2 balanced-bridge lesson survives in a more holographic-looking finite stabilizer "
                "tensor-network layer: entropy/min-cut summaries can agree while observer algebra and channel "
                "semantics separate."
            ),
            "scope_warning": (
                "This closes the finite witness package, not every possible generalization. Further work would be "
                "about broadening axes, source atlases, or asymptotic families."
            ),
        },
        "recommendation": {
            "next_phase": "stop",
            "reason": (
                "The core Goal 3 search target now has an exact finite witness, local robustness evidence, CLI "
                "certificates, JSON artifacts, README notes, and human-facing package docs."
            ),
            "optional_extensions": (
                "Generalize the witness across bridge axes, search for smaller/familial variants, or turn the "
                "finite package into a formal paper-style proof appendix."
            ),
        },
    }
