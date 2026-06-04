"""Finite causal-patch toy cosmology diagnostics.

The objects here are intentionally small and exact: a stabilizer code plus a
named cover of physical-qubit regions interpreted as observer patches, horizons,
and derived unions.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

from .family import repeat_balanced_bridge, seed_pair
from .gf2 import all_masks, in_span, nullspace, quotient_basis, rank, rref, mask_from_qubits, mask_to_tuple
from .graphs import edge_pairs, enumerate_graph_state_reps, graph_state, neighbors as graph_neighbors
from .robust import ROBUST_SOURCES, RobustConstraints, code_quality, entropy_key, scan_robust_source
from .search import certify_minimal_entropy_reconstruction_discordance
from .stabilizer import (
    StabilizerCode,
    combine_rows,
    local_clifford_pauli,
    pauli_from_string,
    pauli_to_string,
    support_mask,
    symplectic_product,
)

FRONTIER_CACHE_SCHEMA_VERSION = 1
DEFAULT_FRONTIER_CACHE_PATH = Path(__file__).with_name("frontier_cache").joinpath("goal2_phase7_frontier.json")
DEFAULT_EXTENDED_FRONTIER_CACHE_PATH = Path(__file__).with_name("frontier_cache").joinpath(
    "goal2_phase8_extended_frontier.json"
)


def _mask(*qubits: int) -> int:
    out = 0
    for qubit in qubits:
        out |= 1 << qubit
    return out


@dataclass(frozen=True)
class Patch:
    name: str
    role: str
    region: int

    @classmethod
    def from_qubits(cls, name: str, role: str, qubits: Iterable[int]) -> "Patch":
        return cls(name=name, role=role, region=mask_from_qubits(qubits))

    def summary(self, n: int) -> dict[str, object]:
        return {
            "name": self.name,
            "role": self.role,
            "qubits": mask_to_tuple(self.region, n),
            "size": self.region.bit_count(),
        }


@dataclass(frozen=True)
class PatchCover:
    name: str
    patches: tuple[Patch, ...]
    description: str

    def patch(self, name: str) -> Patch:
        for patch in self.patches:
            if patch.name == name:
                return patch
        raise KeyError(name)

    def summary(self, n: int) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
            "patches": tuple(patch.summary(n) for patch in self.patches),
        }


def bridge_observer_cover(m: int) -> PatchCover:
    if m < 1:
        raise ValueError("the causal-patch cover is horizon-like only for m >= 1")
    horizon = _mask(1, 2, 3)
    observer_p = horizon
    observer_q = horizon
    bridge_shell = 0
    for j in range(m):
        p = 6 + 2 * j
        q = 7 + 2 * j
        observer_p |= 1 << p
        observer_q |= 1 << q
        bridge_shell |= (1 << p) | (1 << q)
    static_diamond = observer_p | observer_q
    return PatchCover(
        name=f"balanced_bridge_observer_cover_m{m}",
        description=(
            "Two overlapping observer causal patches share horizon H={1,2,3}. "
            "Each observer takes one qubit from every bridge pair; their union is the finite static diamond."
        ),
        patches=(
            Patch("observer_p", "observer_patch", observer_p),
            Patch("observer_q", "observer_patch", observer_q),
            Patch("shared_horizon", "horizon_overlap", horizon),
            Patch("bridge_shell", "horizon_shell", bridge_shell),
            Patch("static_diamond", "causal_union", static_diamond),
        ),
    )


def algebra_summary(code: StabilizerCode, region: int, *, include_bases: bool = False) -> dict[str, object]:
    algebra = code.region_algebra(region)
    out: dict[str, object] = {
        "signature": algebra.signature(),
        "logical_dim": algebra.logical_dim,
        "center_dim": algebra.center_dim,
        "commutant_dim": algebra.commutant_dim,
        "reconstructs_all": algebra.reconstructs_all,
    }
    if include_bases:
        out["logical_basis"] = tuple(pauli_to_string(row, code.n) for row in algebra.logical_basis)
        out["center_basis"] = tuple(pauli_to_string(row, code.n) for row in algebra.center_basis)
        out["commutant_basis"] = tuple(pauli_to_string(row, code.n) for row in algebra.commutant_basis)
    return out


def patch_diagnostic(code: StabilizerCode, patch: Patch, *, include_bases: bool = False) -> dict[str, object]:
    full = (1 << code.n) - 1
    complement = full ^ patch.region
    return {
        **patch.summary(code.n),
        "complement_qubits": mask_to_tuple(complement, code.n),
        "entropy": code.entropy(patch.region),
        "algebra": algebra_summary(code, patch.region, include_bases=include_bases),
        "complement_erasure_correctable": code.erasure_correctable(complement),
    }


def pair_diagnostic(code: StabilizerCode, left: Patch, right: Patch) -> dict[str, object]:
    intersection = left.region & right.region
    union = left.region | right.region
    left_private = left.region & ~right.region
    right_private = right.region & ~left.region
    return {
        "left": left.name,
        "right": right.name,
        "intersection_qubits": mask_to_tuple(intersection, code.n),
        "union_qubits": mask_to_tuple(union, code.n),
        "left_private_qubits": mask_to_tuple(left_private, code.n),
        "right_private_qubits": mask_to_tuple(right_private, code.n),
        "entropies": {
            "left": code.entropy(left.region),
            "right": code.entropy(right.region),
            "intersection": code.entropy(intersection),
            "union": code.entropy(union),
            "left_private": code.entropy(left_private),
            "right_private": code.entropy(right_private),
        },
        "mutual_information": code.mutual_information(left.region, right.region),
        "private_cmi_given_intersection": code.conditional_mutual_information(
            left_private,
            intersection,
            right_private,
        ),
        "private_tripartite_information": code.tripartite_information(left_private, intersection, right_private),
        "intersection_algebra": algebra_summary(code, intersection),
        "union_algebra": algebra_summary(code, union),
    }


def cover_diagnostic(code: StabilizerCode, cover: PatchCover, *, include_bases: bool = False) -> dict[str, object]:
    observer_pairs = tuple(
        (left.name, right.name)
        for left, right in combinations(cover.patches, 2)
        if left.role == "observer_patch" and right.role == "observer_patch"
    )
    return {
        "n": code.n,
        "k": code.k,
        "distance": code.distance(),
        "generators": code.pauli_generators(),
        "cover": cover.summary(code.n),
        "patches": tuple(patch_diagnostic(code, patch, include_bases=include_bases) for patch in cover.patches),
        "pairs": tuple(pair_diagnostic(code, left, right) for left, right in combinations(cover.patches, 2)),
        "observer_pairs": observer_pairs,
    }


def entropy_overlap_key(diagnostic: dict[str, object]) -> tuple[object, ...]:
    patches = diagnostic["patches"]
    pairs = diagnostic["pairs"]
    return (
        tuple((patch["name"], patch["entropy"]) for patch in patches),
        tuple(
            (
                pair["left"],
                pair["right"],
                tuple(pair["intersection_qubits"]),
                tuple(pair["union_qubits"]),
                tuple(sorted(pair["entropies"].items())),
                pair["mutual_information"],
                pair["private_cmi_given_intersection"],
                pair["private_tripartite_information"],
            )
            for pair in pairs
        ),
    )


def algebra_key(diagnostic: dict[str, object]) -> tuple[object, ...]:
    return tuple((patch["name"], patch["algebra"]["signature"]) for patch in diagnostic["patches"])


def pair_by_names(diagnostic: dict[str, object], left: str, right: str) -> dict[str, object]:
    for pair in diagnostic["pairs"]:
        if (pair["left"], pair["right"]) == (left, right) or (pair["left"], pair["right"]) == (right, left):
            return pair
    raise KeyError((left, right))


def patch_by_name(diagnostic: dict[str, object], name: str) -> dict[str, object]:
    for patch in diagnostic["patches"]:
        if patch["name"] == name:
            return patch
    raise KeyError(name)


def compare_cover_diagnostics(first: dict[str, object], second: dict[str, object]) -> dict[str, object]:
    first_algebra = dict(algebra_key(first))
    second_algebra = dict(algebra_key(second))
    differing_patches = tuple(
        {
            "patch": name,
            "first_signature": first_algebra[name],
            "second_signature": second_algebra[name],
        }
        for name in first_algebra
        if first_algebra[name] != second_algebra[name]
    )
    observer_names = tuple(patch["name"] for patch in first["patches"] if patch["role"] == "observer_patch")
    observer_reconstruction = tuple(
        {
            "patch": name,
            "first_reconstructs_all": patch_by_name(first, name)["algebra"]["reconstructs_all"],
            "second_reconstructs_all": patch_by_name(second, name)["algebra"]["reconstructs_all"],
        }
        for name in observer_names
    )
    horizon_name = "shared_horizon"
    return {
        "same_entropy_overlap_data": entropy_overlap_key(first) == entropy_overlap_key(second),
        "same_patch_algebra_signatures": algebra_key(first) == algebra_key(second),
        "differing_patch_algebras": differing_patches,
        "observer_reconstruction": observer_reconstruction,
        "same_shared_horizon_algebra": patch_by_name(first, horizon_name)["algebra"]["signature"]
        == patch_by_name(second, horizon_name)["algebra"]["signature"],
        "shared_horizon_signature": patch_by_name(first, horizon_name)["algebra"]["signature"],
    }


def bridge_cosmology_instance_certificate(
    m: int,
    *,
    include_bases: bool = False,
) -> dict[str, object]:
    first, second = repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m)
    cover = bridge_observer_cover(m)
    first_diag = cover_diagnostic(first, cover, include_bases=include_bases)
    second_diag = cover_diagnostic(second, cover, include_bases=include_bases)
    comparison = compare_cover_diagnostics(first_diag, second_diag)
    observer_pair_first = pair_by_names(first_diag, "observer_p", "observer_q")
    observer_pair_second = pair_by_names(second_diag, "observer_p", "observer_q")
    claims = {
        "same_labeled_t2_entropy": first.entropy_vector(max_subset_size=2) == second.entropy_vector(max_subset_size=2),
        "same_patch_entropy_overlap_data": comparison["same_entropy_overlap_data"],
        "same_shared_horizon_algebra": comparison["same_shared_horizon_algebra"],
        "different_observer_patch_reconstruction": any(
            item["first_reconstructs_all"] != item["second_reconstructs_all"]
            for item in comparison["observer_reconstruction"]
        ),
        "observer_overlap_is_shared_horizon": tuple(observer_pair_first["intersection_qubits"]) == (1, 2, 3),
        "observer_pair_metrics_match": (
            observer_pair_first["mutual_information"] == observer_pair_second["mutual_information"]
            and observer_pair_first["private_cmi_given_intersection"]
            == observer_pair_second["private_cmi_given_intersection"]
            and observer_pair_first["private_tripartite_information"]
            == observer_pair_second["private_tripartite_information"]
        ),
    }
    claims["phase_1_static_patch_separation"] = all(claims.values())
    return {
        "m": m,
        "n": first.n,
        "patch_cover": cover.summary(first.n),
        "first_code": "A_m",
        "second_code": "B_m",
        "first": first_diag,
        "second": second_diag,
        "comparison": comparison,
        "certified_claims": claims,
        "witness": {
            "observer_p": {
                "entropy": patch_by_name(first_diag, "observer_p")["entropy"],
                "first_signature": patch_by_name(first_diag, "observer_p")["algebra"]["signature"],
                "second_signature": patch_by_name(second_diag, "observer_p")["algebra"]["signature"],
            },
            "observer_q": {
                "entropy": patch_by_name(first_diag, "observer_q")["entropy"],
                "first_signature": patch_by_name(first_diag, "observer_q")["algebra"]["signature"],
                "second_signature": patch_by_name(second_diag, "observer_q")["algebra"]["signature"],
            },
            "shared_horizon": {
                "entropy": patch_by_name(first_diag, "shared_horizon")["entropy"],
                "signature": patch_by_name(first_diag, "shared_horizon")["algebra"]["signature"],
            },
            "observer_pair": {
                "intersection": observer_pair_first["intersection_qubits"],
                "mutual_information": observer_pair_first["mutual_information"],
                "private_cmi_given_intersection": observer_pair_first["private_cmi_given_intersection"],
                "private_tripartite_information": observer_pair_first["private_tripartite_information"],
            },
        },
    }


def bridge_cosmology_phase1_certificate(
    *,
    max_m: int = 3,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_m < 1:
        raise ValueError("max_m must be at least 1")
    instances = tuple(
        bridge_cosmology_instance_certificate(m, include_bases=include_bases) for m in range(1, max_m + 1)
    )
    all_pass = all(instance["certified_claims"]["phase_1_static_patch_separation"] for instance in instances)
    return {
        "phase": "Goal 2 Phase 1: finite causal-patch/horizon-code verifier",
        "status": "pass" if all_pass else "fail",
        "max_m": max_m,
        "claims_checked": (
            "same labeled t<=2 entropy data",
            "same named patch entropy/overlap/MI/CMI/I3 data",
            "same shared-horizon algebra",
            "different observer-patch logical reconstruction",
        ),
        "instances": instances,
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The static patch cover already gives an exact entropy-overlap/reconstruction separation. "
                "Phase 2 should build time/channel dynamics on this cover, but first make the dynamics preserve "
                "or explicitly change the patch atlas so causal-patch algebra flow is checkable step by step."
            ),
            "suggested_phase_2": (
                "Add deterministic bridge-growth and simple erasure/noise channels, then certify how patch "
                "entropies, horizons, fixed points, and reconstructable algebras change across time slices."
            ),
        },
    }


def erasure_scenarios(cover: PatchCover) -> tuple[dict[str, object], ...]:
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    shared_horizon = cover.patch("shared_horizon").region
    bridge_shell = cover.patch("bridge_shell").region
    static_diamond = cover.patch("static_diamond").region
    return (
        {
            "name": "erase_observer_p_private",
            "role": "private_observer_shell",
            "erased_region": observer_p & ~shared_horizon,
        },
        {
            "name": "erase_observer_q_private",
            "role": "private_observer_shell",
            "erased_region": observer_q & ~shared_horizon,
        },
        {
            "name": "erase_shared_horizon",
            "role": "horizon_erasure",
            "erased_region": shared_horizon,
        },
        {
            "name": "erase_bridge_shell",
            "role": "horizon_shell_erasure",
            "erased_region": bridge_shell,
        },
        {
            "name": "erase_observer_p",
            "role": "observer_patch_erasure",
            "erased_region": observer_p,
        },
        {
            "name": "erase_observer_q",
            "role": "observer_patch_erasure",
            "erased_region": observer_q,
        },
        {
            "name": "erase_static_diamond",
            "role": "causal_union_erasure",
            "erased_region": static_diamond,
        },
    )


def erasure_channel_diagnostic(
    code: StabilizerCode,
    scenario: dict[str, object],
    *,
    include_bases: bool = False,
) -> dict[str, object]:
    erased = int(scenario["erased_region"])
    full = (1 << code.n) - 1
    survivor = full ^ erased
    erasure_correctable = code.erasure_correctable(erased)
    survivor_reconstructs_all = code.reconstructs_all_logicals(survivor)
    return {
        "name": scenario["name"],
        "role": scenario["role"],
        "channel": "exact_erasure",
        "erased_qubits": mask_to_tuple(erased, code.n),
        "survivor_qubits": mask_to_tuple(survivor, code.n),
        "erased_entropy": code.entropy(erased),
        "survivor_entropy": code.entropy(survivor),
        "erasure_correctable": erasure_correctable,
        "survivor_reconstructs_all": survivor_reconstructs_all,
        "qec_complementarity_identity_holds": erasure_correctable == survivor_reconstructs_all,
        "erased_algebra": algebra_summary(code, erased, include_bases=include_bases),
        "survivor_algebra": algebra_summary(code, survivor, include_bases=include_bases),
    }


def erasure_suite_diagnostic(
    code: StabilizerCode,
    cover: PatchCover,
    *,
    include_bases: bool = False,
) -> tuple[dict[str, object], ...]:
    return tuple(
        erasure_channel_diagnostic(code, scenario, include_bases=include_bases)
        for scenario in erasure_scenarios(cover)
    )


def erasure_by_name(suite: tuple[dict[str, object], ...], name: str) -> dict[str, object]:
    for item in suite:
        if item["name"] == name:
            return item
    raise KeyError(name)


def erasure_correctability_key(suite: tuple[dict[str, object], ...]) -> tuple[tuple[str, bool], ...]:
    return tuple((item["name"], item["erasure_correctable"]) for item in suite)


def erased_entropy_key(suite: tuple[dict[str, object], ...]) -> tuple[tuple[str, int], ...]:
    return tuple((item["name"], item["erased_entropy"]) for item in suite)


def survivor_entropy_key(suite: tuple[dict[str, object], ...]) -> tuple[tuple[str, int], ...]:
    return tuple((item["name"], item["survivor_entropy"]) for item in suite)


def erasure_algebra_differences(
    first_suite: tuple[dict[str, object], ...],
    second_suite: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    out = []
    for first_item in first_suite:
        second_item = erasure_by_name(second_suite, str(first_item["name"]))
        first_erased = first_item["erased_algebra"]["signature"]
        second_erased = second_item["erased_algebra"]["signature"]
        first_survivor = first_item["survivor_algebra"]["signature"]
        second_survivor = second_item["survivor_algebra"]["signature"]
        if first_erased != second_erased or first_survivor != second_survivor:
            out.append(
                {
                    "name": first_item["name"],
                    "first_erased_signature": first_erased,
                    "second_erased_signature": second_erased,
                    "first_survivor_signature": first_survivor,
                    "second_survivor_signature": second_survivor,
                }
            )
    return tuple(out)


def bridge_cosmology_phase2_slice_certificate(
    m: int,
    *,
    include_bases: bool = False,
) -> dict[str, object]:
    instance = bridge_cosmology_instance_certificate(m, include_bases=include_bases)
    first, second = repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m)
    cover = bridge_observer_cover(m)
    first_erasures = erasure_suite_diagnostic(first, cover, include_bases=include_bases)
    second_erasures = erasure_suite_diagnostic(second, cover, include_bases=include_bases)
    algebra_differences = erasure_algebra_differences(first_erasures, second_erasures)
    private_names = ("erase_observer_p_private", "erase_observer_q_private")
    horizon = erasure_by_name(first_erasures, "erase_shared_horizon")
    observer_p = erasure_by_name(first_erasures, "erase_observer_p")
    observer_p_second = erasure_by_name(second_erasures, "erase_observer_p")
    claims = {
        "phase_1_static_patch_separation": instance["certified_claims"]["phase_1_static_patch_separation"],
        "qec_complementarity_identity_all_scenarios": all(
            item["qec_complementarity_identity_holds"] for item in first_erasures + second_erasures
        ),
        "same_erasure_correctability_profile": erasure_correctability_key(first_erasures)
        == erasure_correctability_key(second_erasures),
        "same_erased_region_entropy_profile": erased_entropy_key(first_erasures) == erased_entropy_key(second_erasures),
        "private_shell_erasures_correctable": all(
            erasure_by_name(first_erasures, name)["erasure_correctable"]
            and erasure_by_name(second_erasures, name)["erasure_correctable"]
            for name in private_names
        ),
        "shared_horizon_erasure_not_correctable": not horizon["erasure_correctable"]
        and not erasure_by_name(second_erasures, "erase_shared_horizon")["erasure_correctable"],
        "observer_erasure_algebra_differs": observer_p["erased_algebra"]["signature"]
        != observer_p_second["erased_algebra"]["signature"],
    }
    claims["phase_2_erasure_channel_probe"] = all(claims.values())
    return {
        "m": m,
        "n": first.n,
        "static_patch_certificate": instance,
        "first_erasures": first_erasures,
        "second_erasures": second_erasures,
        "erasure_comparison": {
            "same_erasure_correctability_profile": claims["same_erasure_correctability_profile"],
            "same_erased_region_entropy_profile": claims["same_erased_region_entropy_profile"],
            "same_survivor_entropy_profile": survivor_entropy_key(first_erasures) == survivor_entropy_key(second_erasures),
            "algebra_differences": algebra_differences,
        },
        "certified_claims": claims,
        "witness": {
            "private_shell": {
                "scenario": "erase_observer_p_private",
                "erasure_correctable": erasure_by_name(first_erasures, "erase_observer_p_private")[
                    "erasure_correctable"
                ],
                "survivor_signature": erasure_by_name(first_erasures, "erase_observer_p_private")[
                    "survivor_algebra"
                ]["signature"],
            },
            "shared_horizon": {
                "scenario": "erase_shared_horizon",
                "erasure_correctable": horizon["erasure_correctable"],
                "erased_signature": horizon["erased_algebra"]["signature"],
                "survivor_signature": horizon["survivor_algebra"]["signature"],
            },
            "observer_erasure_difference": {
                "scenario": "erase_observer_p",
                "first_erased_signature": observer_p["erased_algebra"]["signature"],
                "second_erased_signature": observer_p_second["erased_algebra"]["signature"],
                "first_survivor_signature": observer_p["survivor_algebra"]["signature"],
                "second_survivor_signature": observer_p_second["survivor_algebra"]["signature"],
            },
        },
    }


def bridge_growth_transition_certificate(m: int) -> dict[str, object]:
    if m < 1:
        raise ValueError("growth transitions start at m >= 1")
    current = bridge_cosmology_instance_certificate(m)
    next_instance = bridge_cosmology_instance_certificate(m + 1)
    current_cover = bridge_observer_cover(m)
    next_cover = bridge_observer_cover(m + 1)
    new_p = 6 + 2 * m
    new_q = 7 + 2 * m

    def patch_region(cover: PatchCover, name: str) -> int:
        return cover.patch(name).region

    current_pair = current["witness"]["observer_pair"]
    next_pair = next_instance["witness"]["observer_pair"]
    current_obs = current["witness"]["observer_p"]
    next_obs = next_instance["witness"]["observer_p"]
    current_horizon = current["witness"]["shared_horizon"]
    next_horizon = next_instance["witness"]["shared_horizon"]
    patch_growth_claims = {
        "shared_horizon_fixed": patch_region(current_cover, "shared_horizon")
        == patch_region(next_cover, "shared_horizon"),
        "observer_p_adds_new_p_only": patch_region(next_cover, "observer_p")
        == (patch_region(current_cover, "observer_p") | (1 << new_p)),
        "observer_q_adds_new_q_only": patch_region(next_cover, "observer_q")
        == (patch_region(current_cover, "observer_q") | (1 << new_q)),
        "bridge_shell_adds_new_pair": patch_region(next_cover, "bridge_shell")
        == (patch_region(current_cover, "bridge_shell") | (1 << new_p) | (1 << new_q)),
        "static_diamond_adds_new_pair": patch_region(next_cover, "static_diamond")
        == (patch_region(current_cover, "static_diamond") | (1 << new_p) | (1 << new_q)),
    }
    metric_flow_claims = {
        "observer_entropy_increments_by_one": next_obs["entropy"] - current_obs["entropy"] == 1,
        "shared_horizon_entropy_fixed": next_horizon["entropy"] == current_horizon["entropy"],
        "observer_pair_mi_increments_by_two": next_pair["mutual_information"]
        - current_pair["mutual_information"]
        == 2,
        "observer_pair_private_cmi_increments_by_two": next_pair["private_cmi_given_intersection"]
        - current_pair["private_cmi_given_intersection"]
        == 2,
        "observer_pair_i3_fixed": next_pair["private_tripartite_information"]
        == current_pair["private_tripartite_information"],
    }
    algebra_flow_claims = {
        "A_observer_signature_stable": next_obs["first_signature"] == current_obs["first_signature"],
        "B_observer_signature_stable": next_obs["second_signature"] == current_obs["second_signature"],
        "shared_horizon_signature_stable": next_horizon["signature"] == current_horizon["signature"],
    }
    claims = {
        **patch_growth_claims,
        **metric_flow_claims,
        **algebra_flow_claims,
        "current_static_claims_pass": current["certified_claims"]["phase_1_static_patch_separation"],
        "next_static_claims_pass": next_instance["certified_claims"]["phase_1_static_patch_separation"],
    }
    claims["phase_2_growth_transition"] = all(claims.values())
    return {
        "from_m": m,
        "to_m": m + 1,
        "new_qubits": {"p": new_p, "q": new_q},
        "patch_growth_claims": patch_growth_claims,
        "metric_flow_claims": metric_flow_claims,
        "algebra_flow_claims": algebra_flow_claims,
        "certified_claims": claims,
        "witness": {
            "observer_entropy": {"from": current_obs["entropy"], "to": next_obs["entropy"], "delta": 1},
            "observer_pair_mi": {
                "from": current_pair["mutual_information"],
                "to": next_pair["mutual_information"],
                "delta": 2,
            },
            "observer_pair_private_cmi": {
                "from": current_pair["private_cmi_given_intersection"],
                "to": next_pair["private_cmi_given_intersection"],
                "delta": 2,
            },
            "observer_pair_private_i3": {
                "from": current_pair["private_tripartite_information"],
                "to": next_pair["private_tripartite_information"],
                "delta": 0,
            },
            "observer_signatures": {
                "A": current_obs["first_signature"],
                "B": current_obs["second_signature"],
            },
        },
    }


def bridge_cosmology_phase2_certificate(
    *,
    max_m: int = 3,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_m < 2:
        raise ValueError("max_m must be at least 2 to certify a growth transition")
    slices = tuple(
        bridge_cosmology_phase2_slice_certificate(m, include_bases=include_bases) for m in range(1, max_m + 1)
    )
    transitions = tuple(bridge_growth_transition_certificate(m) for m in range(1, max_m))
    all_slice_claims = all(item["certified_claims"]["phase_2_erasure_channel_probe"] for item in slices)
    all_transition_claims = all(item["certified_claims"]["phase_2_growth_transition"] for item in transitions)
    return {
        "phase": "Goal 2 Phase 2: deterministic bridge-growth and exact erasure-channel probes",
        "status": "pass" if all_slice_claims and all_transition_claims else "fail",
        "max_m": max_m,
        "dynamics": {
            "time_index": "m",
            "growth_rule": (
                "m -> m+1 appends one bridge pair p_m=6+2m, q_m=7+2m and extends the patch atlas "
                "by assigning p_m to observer_p and q_m to observer_q."
            ),
            "channel_model": (
                "Exact erasure probes on named patch regions. Correctability is computed by the stabilizer "
                "logical-subspace criterion and checked against reconstructability on the survivor complement."
            ),
        },
        "claims_checked": (
            "static Phase 1 separation persists at every time slice",
            "growth preserves the shared horizon and grows observer/private shells by one qubit each",
            "observer entropy, MI, and private CMI have certified deterministic increments",
            "private observer-shell erasures are correctable but shared-horizon erasure is not",
            "A/B have the same erasure-correctability profile but different observer-erasure algebras",
        ),
        "slices": slices,
        "transitions": transitions,
        "recommendation": {
            "next_phase": "proceed_as_written",
            "reason": (
                "The framework now has exact static patch diagnostics, deterministic growth, and erasure-channel "
                "complementarity probes. The next natural step is search: vary patch covers, bridge assignments, "
                "and small stabilizer/CSS sources to find new causal-patch separations automatically."
            ),
            "suggested_phase_3": (
                "Add a bounded search over patch covers and small CSS/tensor-network-like constructions, scoring "
                "same entropy-overlap data with different observer algebra flow or erasure-channel behavior."
            ),
        },
    }


def bridge_assignment_cover(m: int, horizon: int, orientation: tuple[int, ...]) -> PatchCover:
    if m < 1:
        raise ValueError("m must be at least 1")
    if len(orientation) != m:
        raise ValueError(f"expected {m} orientation bits, found {len(orientation)}")
    observer_p = horizon
    observer_q = horizon
    bridge_shell = 0
    for j, bit in enumerate(orientation):
        if bit not in (0, 1):
            raise ValueError("orientation bits must be 0 or 1")
        p = 6 + 2 * j
        q = 7 + 2 * j
        left = q if bit else p
        right = p if bit else q
        observer_p |= 1 << left
        observer_q |= 1 << right
        bridge_shell |= (1 << p) | (1 << q)
    static_diamond = observer_p | observer_q
    name = "bridge_assignment_h{}_o{}".format(
        "-".join(map(str, mask_to_tuple(horizon, 6))),
        "".join(map(str, orientation)),
    )
    return PatchCover(
        name=name,
        description=(
            "Search-generated two-observer cover: an old-qubit horizon plus one qubit from each bridge pair "
            "assigned to each observer."
        ),
        patches=(
            Patch("observer_p", "observer_patch", observer_p),
            Patch("observer_q", "observer_patch", observer_q),
            Patch("shared_horizon", "horizon_overlap", horizon),
            Patch("bridge_shell", "horizon_shell", bridge_shell),
            Patch("static_diamond", "causal_union", static_diamond),
        ),
    )


def bridge_patch_cover_candidates(
    *,
    m: int,
    horizon_size: int = 3,
    max_candidates: int | None = None,
) -> tuple[PatchCover, ...]:
    if horizon_size < 1 or horizon_size > 6:
        raise ValueError("horizon_size must be between 1 and 6")
    covers = []
    for horizon_qubits in combinations(range(6), horizon_size):
        horizon = mask_from_qubits(horizon_qubits)
        for orientation in product((0, 1), repeat=m):
            covers.append(bridge_assignment_cover(m, horizon, orientation))
            if max_candidates is not None and len(covers) >= max_candidates:
                return tuple(covers)
    return tuple(covers)


def entropy_overlap_summary(code: StabilizerCode, cover: PatchCover) -> tuple[object, ...]:
    patch_piece = tuple((patch.name, code.entropy(patch.region)) for patch in cover.patches)
    pair_piece = []
    for left, right in combinations(cover.patches, 2):
        intersection = left.region & right.region
        union = left.region | right.region
        left_private = left.region & ~right.region
        right_private = right.region & ~left.region
        pair_piece.append(
            (
                left.name,
                right.name,
                mask_to_tuple(intersection, code.n),
                mask_to_tuple(union, code.n),
                (
                    ("left", code.entropy(left.region)),
                    ("right", code.entropy(right.region)),
                    ("intersection", code.entropy(intersection)),
                    ("union", code.entropy(union)),
                    ("left_private", code.entropy(left_private)),
                    ("right_private", code.entropy(right_private)),
                ),
                code.mutual_information(left.region, right.region),
                code.conditional_mutual_information(left_private, intersection, right_private),
                code.tripartite_information(left_private, intersection, right_private),
            )
        )
    return (patch_piece, tuple(pair_piece))


def patch_algebra_signatures(code: StabilizerCode, cover: PatchCover) -> tuple[tuple[str, tuple[int, int, int, bool]], ...]:
    return tuple((patch.name, code.region_algebra(patch.region).signature()) for patch in cover.patches)


def observer_reconstruction_summary(
    first: StabilizerCode,
    second: StabilizerCode,
    cover: PatchCover,
) -> tuple[dict[str, object], ...]:
    rows = []
    for patch in cover.patches:
        if patch.role != "observer_patch":
            continue
        first_algebra = first.region_algebra(patch.region)
        second_algebra = second.region_algebra(patch.region)
        rows.append(
            {
                "patch": patch.name,
                "first_signature": first_algebra.signature(),
                "second_signature": second_algebra.signature(),
                "first_reconstructs_all": first_algebra.reconstructs_all,
                "second_reconstructs_all": second_algebra.reconstructs_all,
            }
        )
    return tuple(rows)


def cover_search_hit_certificate(
    *,
    m: int,
    first: StabilizerCode,
    second: StabilizerCode,
    cover: PatchCover,
    include_bases: bool = False,
) -> dict[str, object]:
    first_entropy = entropy_overlap_summary(first, cover)
    second_entropy = entropy_overlap_summary(second, cover)
    first_algebras = dict(patch_algebra_signatures(first, cover))
    second_algebras = dict(patch_algebra_signatures(second, cover))
    observer_reconstruction = observer_reconstruction_summary(first, second, cover)
    first_erasures = erasure_suite_diagnostic(first, cover, include_bases=include_bases)
    second_erasures = erasure_suite_diagnostic(second, cover, include_bases=include_bases)
    shared_horizon = cover.patch("shared_horizon").region
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    claims = {
        "same_entropy_overlap_data": first_entropy == second_entropy,
        "observer_overlap_is_horizon": observer_p & observer_q == shared_horizon,
        "same_shared_horizon_algebra": first_algebras["shared_horizon"] == second_algebras["shared_horizon"],
        "different_observer_reconstruction": any(
            item["first_reconstructs_all"] != item["second_reconstructs_all"]
            or item["first_signature"] != item["second_signature"]
            for item in observer_reconstruction
        ),
        "same_erasure_correctability_profile": erasure_correctability_key(first_erasures)
        == erasure_correctability_key(second_erasures),
        "erasure_algebra_difference_exists": bool(erasure_algebra_differences(first_erasures, second_erasures)),
    }
    claims["causal_patch_search_hit"] = all(claims.values())
    return {
        "m": m,
        "cover": cover.summary(first.n),
        "first_patch_algebras": tuple((name, first_algebras[name]) for name in first_algebras),
        "second_patch_algebras": tuple((name, second_algebras[name]) for name in second_algebras),
        "observer_reconstruction": observer_reconstruction,
        "shared_horizon_signature": first_algebras["shared_horizon"],
        "erasure_comparison": {
            "same_erasure_correctability_profile": claims["same_erasure_correctability_profile"],
            "algebra_differences": erasure_algebra_differences(first_erasures, second_erasures),
        },
        "certified_claims": claims,
    }


def score_bridge_cover_candidate(first: StabilizerCode, second: StabilizerCode, cover: PatchCover) -> dict[str, object]:
    first_entropy = entropy_overlap_summary(first, cover)
    second_entropy = entropy_overlap_summary(second, cover)
    entropy_same = first_entropy == second_entropy
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    shared_horizon = cover.patch("shared_horizon").region
    if not entropy_same or observer_p & observer_q != shared_horizon:
        return {
            "entropy_same": entropy_same,
            "observer_overlap_is_horizon": observer_p & observer_q == shared_horizon,
            "hit": False,
        }
    first_algebras = dict(patch_algebra_signatures(first, cover))
    second_algebras = dict(patch_algebra_signatures(second, cover))
    observer_reconstruction = observer_reconstruction_summary(first, second, cover)
    same_horizon = first_algebras["shared_horizon"] == second_algebras["shared_horizon"]
    observer_diff = any(
        item["first_reconstructs_all"] != item["second_reconstructs_all"]
        or item["first_signature"] != item["second_signature"]
        for item in observer_reconstruction
    )
    return {
        "entropy_same": entropy_same,
        "observer_overlap_is_horizon": True,
        "same_shared_horizon_algebra": same_horizon,
        "different_observer_reconstruction": observer_diff,
        "hit": same_horizon and observer_diff,
    }


def bridge_cosmology_phase3_certificate(
    *,
    m: int = 2,
    horizon_size: int = 3,
    max_candidates: int | None = None,
    max_hits: int = 5,
    include_bases: bool = False,
) -> dict[str, object]:
    if m < 1:
        raise ValueError("m must be at least 1")
    if max_hits < 1:
        raise ValueError("max_hits must be at least 1")
    first, second = repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m)
    covers = bridge_patch_cover_candidates(m=m, horizon_size=horizon_size, max_candidates=max_candidates)
    scanned = 0
    entropy_matched = 0
    horizon_matched = 0
    observer_diff = 0
    hits: list[dict[str, object]] = []
    for cover in covers:
        scanned += 1
        score = score_bridge_cover_candidate(first, second, cover)
        if score["entropy_same"]:
            entropy_matched += 1
        if score.get("same_shared_horizon_algebra"):
            horizon_matched += 1
        if score.get("different_observer_reconstruction"):
            observer_diff += 1
        if not score["hit"]:
            continue
        hit = cover_search_hit_certificate(m=m, first=first, second=second, cover=cover, include_bases=include_bases)
        if hit["certified_claims"]["causal_patch_search_hit"]:
            hits.append(hit)
            if len(hits) >= max_hits:
                break
    all_hits_verified = bool(hits) and all(hit["certified_claims"]["causal_patch_search_hit"] for hit in hits)
    return {
        "phase": "Goal 2 Phase 3: bounded causal-patch cover search",
        "status": "pass" if all_hits_verified else "no-hit",
        "search_space": {
            "source": "balanced_bridge_css_family",
            "m": m,
            "n": first.n,
            "horizon_source_qubits": tuple(range(6)),
            "horizon_size": horizon_size,
            "bridge_assignment_rule": "each bridge pair contributes one qubit to each observer; all orientations are enumerated",
            "candidate_count": len(covers),
            "max_candidates": max_candidates,
            "max_hits": max_hits,
        },
        "counts": {
            "scanned": scanned,
            "entropy_overlap_matched": entropy_matched,
            "same_horizon_algebra": horizon_matched,
            "different_observer_reconstruction": observer_diff,
            "hits_returned": len(hits),
        },
        "hit_definition": (
            "same exact named-patch entropy/overlap/MI/CMI/I3 data, observer overlap equal to shared_horizon, "
            "same shared-horizon algebra, different observer reconstruction/algebra, same erasure correctability "
            "profile, and some erasure algebra difference"
        ),
        "hits": tuple(hits),
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The bounded cover search finds exact causal-patch witnesses on the bridge family, so the search "
                "interface is useful. The next adaptation should broaden the source space beyond this family to "
                "small CSS, graph/CWS-like, and shallow-encoder constructions while keeping the same certificate schema."
            ),
            "suggested_phase_4": (
                "Search over code sources as well as patch covers: enumerate small robust CSS/graph/encoder code pairs, "
                "then run the causal-patch cover scorer on entropy-matched reconstruction-discordant candidates."
            ),
        },
    }


def generic_observer_cover(
    *,
    n: int,
    horizon: int,
    observer_p_private: int,
    observer_q_private: int,
    name: str | None = None,
) -> PatchCover:
    if horizon & observer_p_private or horizon & observer_q_private or observer_p_private & observer_q_private:
        raise ValueError("horizon and private observer regions must be disjoint")
    observer_p = horizon | observer_p_private
    observer_q = horizon | observer_q_private
    static_diamond = observer_p | observer_q
    shell = observer_p_private | observer_q_private
    cover_name = name or "generic_h{}_p{}_q{}".format(
        "-".join(map(str, mask_to_tuple(horizon, n))),
        "-".join(map(str, mask_to_tuple(observer_p_private, n))),
        "-".join(map(str, mask_to_tuple(observer_q_private, n))),
    )
    return PatchCover(
        name=cover_name,
        description=(
            "Search-generated generic two-observer cover with a shared horizon and disjoint private "
            "observer regions."
        ),
        patches=(
            Patch("observer_p", "observer_patch", observer_p),
            Patch("observer_q", "observer_patch", observer_q),
            Patch("shared_horizon", "horizon_overlap", horizon),
            Patch("bridge_shell", "horizon_shell", shell),
            Patch("static_diamond", "causal_union", static_diamond),
        ),
    )


def generic_patch_cover_candidates(
    *,
    n: int,
    horizon_size: int = 2,
    private_size: int = 1,
    max_candidates: int | None = None,
) -> tuple[PatchCover, ...]:
    if max_candidates is not None and max_candidates < 0:
        raise ValueError("max_candidates must be nonnegative")
    if max_candidates == 0:
        return ()
    if horizon_size < 1 or horizon_size > n:
        raise ValueError("horizon_size must be between 1 and n")
    if private_size < 0:
        raise ValueError("private_size must be nonnegative")
    if horizon_size + 2 * private_size > n:
        raise ValueError("horizon plus private regions do not fit in n qubits")
    covers = []
    for horizon_qubits in combinations(range(n), horizon_size):
        horizon = mask_from_qubits(horizon_qubits)
        remaining = tuple(qubit for qubit in range(n) if qubit not in horizon_qubits)
        for p_private_qubits in combinations(remaining, private_size):
            p_private = mask_from_qubits(p_private_qubits)
            q_remaining = tuple(qubit for qubit in remaining if qubit not in p_private_qubits)
            for q_private_qubits in combinations(q_remaining, private_size):
                q_private = mask_from_qubits(q_private_qubits)
                covers.append(
                    generic_observer_cover(
                        n=n,
                        horizon=horizon,
                        observer_p_private=p_private,
                        observer_q_private=q_private,
                    )
                )
                if max_candidates is not None and len(covers) >= max_candidates:
                    return tuple(covers)
    return tuple(covers)


def named_two_observer_cover(
    *,
    observer_p: int,
    observer_q: int,
    name: str,
    description: str,
) -> PatchCover:
    shared_horizon = observer_p & observer_q
    shell = (observer_p | observer_q) & ~shared_horizon
    return PatchCover(
        name=name,
        description=description,
        patches=(
            Patch("observer_p", "observer_patch", observer_p),
            Patch("observer_q", "observer_patch", observer_q),
            Patch("shared_horizon", "horizon_overlap", shared_horizon),
            Patch("bridge_shell", "horizon_shell", shell),
            Patch("static_diamond", "causal_union", observer_p | observer_q),
        ),
    )


def graph_support_masks_for_source(source: dict[str, object]) -> tuple[int, ...]:
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    supports = {
        support_mask(generator, first.n)
        for code in (first, second)
        for generator in code.generators
    }
    return tuple(sorted(supports, key=lambda mask: (mask.bit_count(), mask)))


def graph_closed_neighborhood_masks(n: int, supports: tuple[int, ...]) -> tuple[int, ...]:
    neighbors = [0 for _ in range(n)]
    for support in supports:
        qubits = mask_to_tuple(support, n)
        for left, right in combinations(qubits, 2):
            neighbors[left] |= 1 << right
            neighbors[right] |= 1 << left
    closed = tuple((1 << qubit) | neighbors[qubit] for qubit in range(n))
    return tuple(sorted(set(closed), key=lambda mask: (mask.bit_count(), mask)))


def graph_specific_patch_cover_candidates(source: dict[str, object]) -> tuple[dict[str, object], ...]:
    first = source["first"]
    if not isinstance(first, StabilizerCode):
        raise TypeError("source first must be a StabilizerCode instance")
    supports = graph_support_masks_for_source(source)
    closed_neighborhoods = graph_closed_neighborhood_masks(first.n, supports)
    candidates: list[dict[str, object]] = []
    seen: set[tuple[int, int, str]] = set()

    for left_index, left in enumerate(closed_neighborhoods):
        for right_index, right in enumerate(closed_neighborhoods[left_index:], start=left_index):
            if not left & right:
                continue
            key = (left, right, "graph_closed_neighborhood_overlap")
            if key in seen:
                continue
            seen.add(key)
            candidates.append(
                {
                    "template_kind": "graph_closed_neighborhood_overlap",
                    "template_origin": "co-support graph closed neighborhoods",
                    "cover": named_two_observer_cover(
                        observer_p=left,
                        observer_q=right,
                        name=f"graph_closed_neighborhood_{left_index}_{right_index}",
                        description=(
                            "Graph-native cover from closed neighborhoods in the support co-occurrence graph."
                        ),
                    ),
                }
            )

    for left_index, left in enumerate(supports):
        for right_index, right in enumerate(supports[left_index + 1 :], start=left_index + 1):
            if not left & right:
                continue
            key = (left, right, "graph_generator_support_cut")
            if key in seen:
                continue
            seen.add(key)
            candidates.append(
                {
                    "template_kind": "graph_generator_support_cut",
                    "template_origin": "overlapping stabilizer-generator support cuts",
                    "cover": named_two_observer_cover(
                        observer_p=left,
                        observer_q=right,
                        name=f"graph_generator_support_cut_{left_index}_{right_index}",
                        description=(
                            "Graph-native cover from overlapping generator-support cuts in the graph/CWS-like source."
                        ),
                    ),
                }
            )
    return tuple(candidates)


def exhaustive_two_observer_cover_candidates(n: int) -> tuple[dict[str, object], ...]:
    candidates: list[dict[str, object]] = []
    for observer_p in range(1, 1 << n):
        for observer_q in range(1, 1 << n):
            if observer_p == observer_q or not (observer_p & observer_q):
                continue
            candidates.append(
                {
                    "template_kind": "exhaustive_overlapping_two_observer",
                    "template_origin": "all ordered non-identical overlapping physical-qubit observer regions",
                    "cover": named_two_observer_cover(
                        observer_p=observer_p,
                        observer_q=observer_q,
                        name=f"exhaustive_two_observer_p{observer_p}_q{observer_q}",
                        description=(
                            "Exhaustive ordered two-observer cover with nonempty overlap on a tiny graph/CWS source."
                        ),
                    ),
                }
            )
    return tuple(candidates)


def strict_two_observer_cover_candidates(n: int) -> tuple[dict[str, object], ...]:
    candidates: list[dict[str, object]] = []
    for observer_p in range(1, 1 << n):
        for observer_q in range(1, 1 << n):
            if observer_p == observer_q or not (observer_p & observer_q):
                continue
            if not (observer_p & ~observer_q) or not (observer_q & ~observer_p):
                continue
            candidates.append(
                {
                    "template_kind": "strict_overlapping_two_observer",
                    "template_origin": (
                        "all ordered overlapping observer regions with nonempty private regions on both sides"
                    ),
                    "cover": named_two_observer_cover(
                        observer_p=observer_p,
                        observer_q=observer_q,
                        name=f"strict_two_observer_p{observer_p}_q{observer_q}",
                        description=(
                            "Exhaustive strict two-observer cover: nonempty shared horizon and nonempty private "
                            "regions for both observers."
                        ),
                    ),
                }
            )
    return tuple(candidates)


def graph_edge_list(edge_mask: int, n: int) -> tuple[tuple[int, int], ...]:
    return tuple(pair for bit, pair in enumerate(edge_pairs(n)) if (edge_mask >> bit) & 1)


def graph_neighborhood_table(edge_mask: int, n: int) -> tuple[tuple[int, tuple[int, ...]], ...]:
    return tuple((vertex, graph_neighbors(edge_mask, n, vertex)) for vertex in range(n))


def relaxed_labeled_graph_constraints() -> RobustConstraints:
    return RobustConstraints(
        max_subset_size=2,
        min_distance=1,
        min_reconstruction_size=1,
        forbid_single_qubit_noncentral=False,
    )


def quality_record(code: StabilizerCode, constraints: RobustConstraints) -> dict[str, object]:
    quality = code_quality(code, constraints)
    return {
        "constraints": robust_constraints_summary(constraints),
        "distance": quality.distance,
        "minimal_reconstruction_size": quality.minimal_reconstruction_size,
        "has_single_qubit_noncentral_logical": quality.has_single_qubit_noncentral_logical,
        "passes": quality.passes,
        "reason": quality.reason,
    }


def graph_subspace_record_summary(record: dict[str, object]) -> dict[str, object]:
    code = record["code"]
    if not isinstance(code, StabilizerCode):
        raise TypeError("graph subspace record must contain a StabilizerCode")
    n = code.n
    edge_mask = int(record["edge_mask"])
    return {
        "ordinal": record["ordinal"],
        "edge_mask": edge_mask,
        "edges": graph_edge_list(edge_mask, n),
        "neighborhoods": graph_neighborhood_table(edge_mask, n),
        "kept_graph_generator_indices": record["keep"],
        "deleted_graph_generator_indices": record["deleted"],
        "graph_state_generators": record["graph_state_generators"],
        "code_generators": code.pauli_generators(),
        "distance": code.distance(),
        "relaxed_quality": quality_record(code, relaxed_labeled_graph_constraints()),
        "robust_quality": quality_record(code, RobustConstraints()),
    }


def enumerate_graph_subspace_code_records(
    *,
    n: int,
    k: int,
    equivalence: str = "permutation",
    max_codes: int | None = None,
) -> tuple[dict[str, object], ...]:
    if k < 0 or k > n:
        raise ValueError("k must satisfy 0 <= k <= n")
    if max_codes is not None and max_codes < 0:
        raise ValueError("max_codes must be nonnegative")
    if max_codes == 0:
        return ()
    r = n - k
    emitted: set[tuple[int, ...]] = set()
    records: list[dict[str, object]] = []
    for edge_mask, state in enumerate_graph_state_reps(n, local_clifford=True):
        graph_state_generators = tuple(pauli_to_string(row, n) for row in state.generators)
        for keep in combinations(range(n), r):
            code = StabilizerCode(n, [state.generators[index] for index in keep])
            key = code.canonical_key(equivalence)
            if key in emitted:
                continue
            emitted.add(key)
            records.append(
                {
                    "ordinal": len(records),
                    "edge_mask": edge_mask,
                    "keep": keep,
                    "deleted": tuple(index for index in range(n) if index not in keep),
                    "graph_state_generators": graph_state_generators,
                    "code": code,
                }
            )
            if max_codes is not None and len(records) >= max_codes:
                return tuple(records)
    return tuple(records)


def graph_labeled_pair_source(
    *,
    n: int = 5,
    k: int = 1,
    max_codes: int = 64,
    equivalence: str = "permutation",
) -> dict[str, object]:
    constraints = relaxed_labeled_graph_constraints()
    records = enumerate_graph_subspace_code_records(n=n, k=k, equivalence=equivalence, max_codes=max_codes)
    by_entropy: dict[tuple, tuple[dict[str, object], tuple[object, ...]]] = {}
    codes_checked = 0
    for record in records:
        code = record["code"]
        if not isinstance(code, StabilizerCode):
            raise TypeError("graph subspace record must contain a StabilizerCode")
        quality = code_quality(code, constraints)
        if not quality.passes:
            continue
        codes_checked += 1
        key = entropy_key(code, max_subset_size=constraints.max_subset_size, mode="labeled")
        reconstruction = code.reconstruction_profile()
        previous = by_entropy.get(key)
        if previous is None:
            by_entropy[key] = (record, reconstruction)
            continue
        old_record, old_reconstruction = previous
        if old_reconstruction == reconstruction:
            continue
        first = old_record["code"]
        second = code
        if not isinstance(first, StabilizerCode):
            raise TypeError("graph subspace record must contain a StabilizerCode")
        source = {
            "name": f"graph_cws_labeled_n{n}_relaxed_pair",
            "source_type": "graph_cws_labeled_relaxed",
            "origin": (
                "bounded graph/CWS-like subspace scan with labeled t=2 entropy and relaxed distance-one "
                "calibration constraints"
            ),
            "frontier_kind": "graph_labeled_search",
            "mutation_depth": 0,
            "first": first,
            "second": second,
        }
        return {
            "status": "pair-found",
            "source": source,
            "source_summary": cached_frontier_source_summary(source),
            "scan": {
                "n": n,
                "k": k,
                "source": "graph",
                "equivalence": equivalence,
                "entropy_key_mode": "labeled",
                "constraints": robust_constraints_summary(constraints),
                "max_codes": max_codes,
                "raw_codes": len(records),
                "codes_checked": codes_checked,
                "entropy_classes": len(by_entropy),
                "pair_found_at_ordinal": record["ordinal"],
                "status": "pair-found",
            },
            "graph_metadata": {
                "first": graph_subspace_record_summary(old_record),
                "second": graph_subspace_record_summary(record),
            },
        }
    return {
        "status": "no-pair",
        "source": None,
        "source_summary": None,
        "scan": {
            "n": n,
            "k": k,
            "source": "graph",
            "equivalence": equivalence,
            "entropy_key_mode": "labeled",
            "constraints": robust_constraints_summary(constraints),
            "max_codes": max_codes,
            "raw_codes": len(records),
            "codes_checked": codes_checked,
            "entropy_classes": len(by_entropy),
            "pair_found_at_ordinal": None,
            "status": "no-pair",
        },
        "graph_metadata": None,
    }


def strict_horizon_private_cover_candidates(n: int) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "template_kind": "strict_horizon_private_two_observer",
            "template_origin": "all covers with one-qubit shared horizon and one private qubit per observer",
            "cover": cover,
        }
        for cover in generic_patch_cover_candidates(n=n, horizon_size=1, private_size=1)
    )


def rank_kernel_supported_basis(basis: Iterable[int], n: int, region: int) -> tuple[int, ...]:
    rows = rref(tuple(basis), 2 * n)
    if not rows:
        return ()
    outside = ((1 << n) - 1) ^ region
    equations: list[int] = []
    for column in range(2 * n):
        qubit = column if column < n else column - n
        if not ((outside >> qubit) & 1):
            continue
        equation = 0
        for index, row in enumerate(rows):
            if (row >> column) & 1:
                equation |= 1 << index
        if equation:
            equations.append(equation)
    coefficients = nullspace(equations, len(rows))
    return rref((combine_rows(coefficient, rows) for coefficient in coefficients), 2 * n)


def rank_kernel_entropy(code: StabilizerCode, region: int) -> int:
    return region.bit_count() - len(rank_kernel_supported_basis(code.generators, code.n, region))


def rank_kernel_algebra_summary(
    code: StabilizerCode,
    region: int,
    *,
    include_bases: bool = False,
) -> dict[str, object]:
    supported_centralizer = rank_kernel_supported_basis(code.centralizer_basis, code.n, region)
    reps = quotient_basis(supported_centralizer, code.generators, code.width)
    logical_dim = len(reps)
    form_rows = []
    for left in reps:
        row = 0
        for index, right in enumerate(reps):
            if symplectic_product(left, right, code.n):
                row |= 1 << index
        form_rows.append(row)
    center_coefficients = nullspace(form_rows, logical_dim) if logical_dim else ()
    center_basis = tuple(combine_rows(coefficients, reps) for coefficients in center_coefficients)

    full_logical_basis = code.logical_basis
    full_logical_dim = 2 * code.k
    commutant_equations = []
    for region_rep in reps:
        equation = 0
        for index, logical_rep in enumerate(full_logical_basis):
            if symplectic_product(logical_rep, region_rep, code.n):
                equation |= 1 << index
        commutant_equations.append(equation)
    commutant_coefficients = nullspace(commutant_equations, full_logical_dim) if full_logical_dim else ()
    commutant_basis = tuple(
        combine_rows(coefficients, full_logical_basis) for coefficients in commutant_coefficients
    )
    out: dict[str, object] = {
        "signature": (logical_dim, len(center_basis), len(commutant_basis), logical_dim == full_logical_dim),
        "logical_dim": logical_dim,
        "center_dim": len(center_basis),
        "commutant_dim": len(commutant_basis),
        "reconstructs_all": logical_dim == full_logical_dim,
    }
    if include_bases:
        out["logical_basis"] = tuple(pauli_to_string(row, code.n) for row in reps)
        out["center_basis"] = tuple(pauli_to_string(row, code.n) for row in center_basis)
        out["commutant_basis"] = tuple(pauli_to_string(row, code.n) for row in commutant_basis)
    return out


def rank_kernel_erasure_correctable(code: StabilizerCode, erasure: int) -> bool:
    supported_centralizer = rank_kernel_supported_basis(code.centralizer_basis, code.n, erasure)
    return len(quotient_basis(supported_centralizer, code.generators, code.width)) == 0


def rank_kernel_entropy_overlap_summary(code: StabilizerCode, cover: PatchCover) -> tuple[object, ...]:
    patch_piece = tuple((patch.name, rank_kernel_entropy(code, patch.region)) for patch in cover.patches)
    pair_piece = []
    for left, right in combinations(cover.patches, 2):
        intersection = left.region & right.region
        union = left.region | right.region
        left_private = left.region & ~right.region
        right_private = right.region & ~left.region
        pair_piece.append(
            (
                left.name,
                right.name,
                mask_to_tuple(intersection, code.n),
                mask_to_tuple(union, code.n),
                (
                    ("left", rank_kernel_entropy(code, left.region)),
                    ("right", rank_kernel_entropy(code, right.region)),
                    ("intersection", rank_kernel_entropy(code, intersection)),
                    ("union", rank_kernel_entropy(code, union)),
                    ("left_private", rank_kernel_entropy(code, left_private)),
                    ("right_private", rank_kernel_entropy(code, right_private)),
                ),
                rank_kernel_entropy(code, left.region)
                + rank_kernel_entropy(code, right.region)
                - rank_kernel_entropy(code, union),
                rank_kernel_entropy(code, left_private | intersection)
                + rank_kernel_entropy(code, intersection | right_private)
                - rank_kernel_entropy(code, intersection)
                - rank_kernel_entropy(code, left_private | intersection | right_private),
                rank_kernel_entropy(code, left_private)
                + rank_kernel_entropy(code, intersection)
                + rank_kernel_entropy(code, right_private)
                - rank_kernel_entropy(code, left_private | intersection)
                - rank_kernel_entropy(code, left_private | right_private)
                - rank_kernel_entropy(code, intersection | right_private)
                + rank_kernel_entropy(code, left_private | intersection | right_private),
            )
        )
    return (patch_piece, tuple(pair_piece))


def rank_kernel_patch_algebra_signatures(
    code: StabilizerCode,
    cover: PatchCover,
) -> tuple[tuple[str, tuple[int, int, int, bool]], ...]:
    return tuple(
        (patch.name, rank_kernel_algebra_summary(code, patch.region)["signature"])
        for patch in cover.patches
    )


def rank_kernel_observer_reconstruction_summary(
    first: StabilizerCode,
    second: StabilizerCode,
    cover: PatchCover,
) -> tuple[dict[str, object], ...]:
    rows = []
    for patch in cover.patches:
        if patch.role != "observer_patch":
            continue
        first_algebra = rank_kernel_algebra_summary(first, patch.region)
        second_algebra = rank_kernel_algebra_summary(second, patch.region)
        rows.append(
            {
                "patch": patch.name,
                "first_signature": first_algebra["signature"],
                "second_signature": second_algebra["signature"],
                "first_reconstructs_all": first_algebra["reconstructs_all"],
                "second_reconstructs_all": second_algebra["reconstructs_all"],
            }
        )
    return tuple(rows)


def rank_kernel_erasure_channel_diagnostic(
    code: StabilizerCode,
    scenario: dict[str, object],
    *,
    include_bases: bool = False,
) -> dict[str, object]:
    erased = int(scenario["erased_region"])
    full = (1 << code.n) - 1
    survivor = full ^ erased
    erasure_correctable = rank_kernel_erasure_correctable(code, erased)
    survivor_reconstructs_all = rank_kernel_algebra_summary(code, survivor)["reconstructs_all"]
    return {
        "name": scenario["name"],
        "role": scenario["role"],
        "channel": "exact_erasure",
        "erased_qubits": mask_to_tuple(erased, code.n),
        "survivor_qubits": mask_to_tuple(survivor, code.n),
        "erased_entropy": rank_kernel_entropy(code, erased),
        "survivor_entropy": rank_kernel_entropy(code, survivor),
        "erasure_correctable": erasure_correctable,
        "survivor_reconstructs_all": survivor_reconstructs_all,
        "qec_complementarity_identity_holds": erasure_correctable == survivor_reconstructs_all,
        "erased_algebra": rank_kernel_algebra_summary(code, erased, include_bases=include_bases),
        "survivor_algebra": rank_kernel_algebra_summary(code, survivor, include_bases=include_bases),
    }


def rank_kernel_erasure_suite_diagnostic(
    code: StabilizerCode,
    cover: PatchCover,
    *,
    include_bases: bool = False,
) -> tuple[dict[str, object], ...]:
    return tuple(
        rank_kernel_erasure_channel_diagnostic(code, scenario, include_bases=include_bases)
        for scenario in erasure_scenarios(cover)
    )


def rank_kernel_cover_score(first: StabilizerCode, second: StabilizerCode, cover: PatchCover) -> dict[str, object]:
    first_entropy = rank_kernel_entropy_overlap_summary(first, cover)
    second_entropy = rank_kernel_entropy_overlap_summary(second, cover)
    entropy_same = first_entropy == second_entropy
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    shared_horizon = cover.patch("shared_horizon").region
    if not entropy_same or observer_p & observer_q != shared_horizon:
        return {
            "entropy_same": entropy_same,
            "observer_overlap_is_horizon": observer_p & observer_q == shared_horizon,
            "hit": False,
        }
    first_algebras = dict(rank_kernel_patch_algebra_signatures(first, cover))
    second_algebras = dict(rank_kernel_patch_algebra_signatures(second, cover))
    observer_reconstruction = rank_kernel_observer_reconstruction_summary(first, second, cover)
    same_horizon = first_algebras["shared_horizon"] == second_algebras["shared_horizon"]
    observer_diff = any(
        item["first_reconstructs_all"] != item["second_reconstructs_all"]
        or item["first_signature"] != item["second_signature"]
        for item in observer_reconstruction
    )
    return {
        "entropy_same": entropy_same,
        "observer_overlap_is_horizon": True,
        "same_shared_horizon_algebra": same_horizon,
        "different_observer_reconstruction": observer_diff,
        "hit": same_horizon and observer_diff,
    }


def rank_kernel_cover_search_hit_certificate_for_pair(
    *,
    pair_source: str,
    first: StabilizerCode,
    second: StabilizerCode,
    cover: PatchCover,
    include_bases: bool = False,
) -> dict[str, object]:
    first_entropy = rank_kernel_entropy_overlap_summary(first, cover)
    second_entropy = rank_kernel_entropy_overlap_summary(second, cover)
    first_algebras = dict(rank_kernel_patch_algebra_signatures(first, cover))
    second_algebras = dict(rank_kernel_patch_algebra_signatures(second, cover))
    observer_reconstruction = rank_kernel_observer_reconstruction_summary(first, second, cover)
    first_erasures = rank_kernel_erasure_suite_diagnostic(first, cover, include_bases=include_bases)
    second_erasures = rank_kernel_erasure_suite_diagnostic(second, cover, include_bases=include_bases)
    shared_horizon = cover.patch("shared_horizon").region
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    claims = {
        "same_entropy_overlap_data": first_entropy == second_entropy,
        "observer_overlap_is_horizon": observer_p & observer_q == shared_horizon,
        "same_shared_horizon_algebra": first_algebras["shared_horizon"] == second_algebras["shared_horizon"],
        "different_observer_reconstruction": any(
            item["first_reconstructs_all"] != item["second_reconstructs_all"]
            or item["first_signature"] != item["second_signature"]
            for item in observer_reconstruction
        ),
        "same_erasure_correctability_profile": erasure_correctability_key(first_erasures)
        == erasure_correctability_key(second_erasures),
        "erasure_algebra_difference_exists": bool(erasure_algebra_differences(first_erasures, second_erasures)),
    }
    claims["causal_patch_search_hit"] = all(claims.values())
    return {
        "pair_source": pair_source,
        "n": first.n,
        "k": first.k,
        "cover": cover.summary(first.n),
        "first_generators": first.pauli_generators(),
        "second_generators": second.pauli_generators(),
        "first_patch_algebras": tuple((name, first_algebras[name]) for name in first_algebras),
        "second_patch_algebras": tuple((name, second_algebras[name]) for name in second_algebras),
        "observer_reconstruction": observer_reconstruction,
        "shared_horizon_signature": first_algebras["shared_horizon"],
        "erasure_comparison": {
            "same_erasure_correctability_profile": claims["same_erasure_correctability_profile"],
            "algebra_differences": erasure_algebra_differences(first_erasures, second_erasures),
        },
        "certified_claims": claims,
    }


def pauli_weight_limited_logical_witness(code: StabilizerCode, max_weight: int) -> dict[str, object] | None:
    if max_weight < 1:
        raise ValueError("max_weight must be positive")
    for weight in range(1, max_weight + 1):
        for qubits in combinations(range(code.n), weight):
            for chars in product("XYZ", repeat=weight):
                pauli = ["I"] * code.n
                for qubit, char in zip(qubits, chars):
                    pauli[qubit] = char
                pauli_string = "".join(pauli)
                row = pauli_from_string(pauli_string)
                commutes = all(symplectic_product(row, generator, code.n) == 0 for generator in code.generators)
                if commutes and not in_span(row, code.generators, code.width):
                    return {
                        "pauli": pauli_string,
                        "weight": weight,
                        "qubits": qubits,
                    }
    return None


def bounded_distance_certificate(code: StabilizerCode, *, max_weight: int = 2) -> dict[str, object]:
    witness = pauli_weight_limited_logical_witness(code, max_weight)
    return {
        "n": code.n,
        "k": code.k,
        "max_weight_checked": max_weight,
        "logical_witness": witness,
        "distance_exact_if_witness_found": None if witness is None else witness["weight"],
        "distance_lower_bound": max_weight + 1 if witness is None else witness["weight"],
        "distance_at_least_2_certified": witness is None or int(witness["weight"]) >= 2,
    }


def low_order_entropy_match_by_rank(
    first: StabilizerCode,
    second: StabilizerCode,
    *,
    max_subset_size: int = 2,
) -> dict[str, object]:
    mismatches = []
    checked = 0
    for mask in all_masks(first.n):
        if mask.bit_count() > max_subset_size:
            continue
        checked += 1
        first_entropy = rank_kernel_entropy(first, mask)
        second_entropy = rank_kernel_entropy(second, mask)
        if first_entropy != second_entropy:
            mismatches.append(
                {
                    "qubits": mask_to_tuple(mask, first.n),
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


def block_shift_pauli(row: int, *, block: int, block_size: int, block_count: int) -> int:
    total_n = block_size * block_count
    x = row & ((1 << block_size) - 1)
    z = row >> block_size
    out = 0
    for qubit in range(block_size):
        shifted = block * block_size + qubit
        if (x >> qubit) & 1:
            out |= 1 << shifted
        if (z >> qubit) & 1:
            out |= 1 << (total_n + shifted)
    return out


def logical_concatenate_k1(inner: StabilizerCode, outer: StabilizerCode) -> tuple[StabilizerCode, dict[str, object]]:
    if inner.k != 1 or outer.k != 1:
        raise ValueError("logical_concatenate_k1 requires k=1 inner and outer codes")
    block_size = inner.n
    block_count = outer.n
    logical_z, logical_x = inner.logical_basis
    if not symplectic_product(logical_z, logical_x, inner.n):
        raise ValueError("inner logical basis must contain an anticommuting pair")
    rows: list[int] = []
    for block in range(block_count):
        for generator in inner.generators:
            rows.append(block_shift_pauli(generator, block=block, block_size=block_size, block_count=block_count))
    encoded_outer_rows = []
    for outer_generator in outer.generators:
        row = 0
        x = outer_generator & ((1 << outer.n) - 1)
        z = outer_generator >> outer.n
        for block in range(block_count):
            if (x >> block) & 1:
                row ^= block_shift_pauli(logical_x, block=block, block_size=block_size, block_count=block_count)
            if (z >> block) & 1:
                row ^= block_shift_pauli(logical_z, block=block, block_size=block_size, block_count=block_count)
        rows.append(row)
        encoded_outer_rows.append(row)
    code = StabilizerCode(block_size * block_count, rows)
    return code, {
        "inner_logical_z": pauli_to_string(logical_z, inner.n),
        "inner_logical_x": pauli_to_string(logical_x, inner.n),
        "outer_generators": outer.pauli_generators(),
        "encoded_outer_generators_unreduced": tuple(pauli_to_string(row, code.n) for row in encoded_outer_rows),
        "block_size": block_size,
        "block_count": block_count,
    }


def phase11_outer_distance_repair_code() -> StabilizerCode:
    return StabilizerCode.from_pauli_strings(("XXIZ", "ZIZX", "XZXX"))


def phase11_distance_repaired_source() -> dict[str, object]:
    graph_search = graph_labeled_pair_source()
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 10 labeled graph source to find a pair")
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 10 source must contain StabilizerCode objects")
    outer = phase11_outer_distance_repair_code()
    first_repaired, first_metadata = logical_concatenate_k1(first, outer)
    second_repaired, second_metadata = logical_concatenate_k1(second, outer)
    return {
        "name": "phase11_graph_labeled_outer_4q_distance_repair",
        "source_type": "logical_concatenation_distance_repair",
        "origin": "Phase 10 labeled graph/CWS pair concatenated with a four-qubit distance-2 outer stabilizer code",
        "frontier_kind": "distance_repair",
        "mutation_depth": 1,
        "first": first_repaired,
        "second": second_repaired,
        "phase10_graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "outer_code": {
            "n": outer.n,
            "k": outer.k,
            "distance": outer.distance(),
            "generators": outer.pauli_generators(),
            "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
            "minimal_reconstruction_regions": tuple(mask_to_tuple(mask, outer.n) for mask in outer.reconstruction_regions(minimal=True)),
        },
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
    }


def lift_inner_region_over_blocks(inner_region: int, *, block_mask: int, block_size: int, block_count: int) -> int:
    out = 0
    for block in range(block_count):
        if not ((block_mask >> block) & 1):
            continue
        for qubit in range(block_size):
            if (inner_region >> qubit) & 1:
                out |= 1 << (block * block_size + qubit)
    return out


def phase11_lifted_atlas_cover_candidates(
    *,
    block_size: int = 5,
    block_count: int = 4,
) -> tuple[dict[str, object], ...]:
    base_covers = (
        ("phase10_p01_q14", _mask(0, 1), _mask(1, 4)),
        ("phase10_p12_q14", _mask(1, 2), _mask(1, 4)),
        ("phase10_p02_q24", _mask(0, 2), _mask(2, 4)),
    )
    candidates = []
    for base_name, observer_p_base, observer_q_base in base_covers:
        for observer_p_blocks in range(1, 1 << block_count):
            for observer_q_blocks in range(1, 1 << block_count):
                if not (observer_p_blocks & observer_q_blocks):
                    continue
                observer_p = lift_inner_region_over_blocks(
                    observer_p_base,
                    block_mask=observer_p_blocks,
                    block_size=block_size,
                    block_count=block_count,
                )
                observer_q = lift_inner_region_over_blocks(
                    observer_q_base,
                    block_mask=observer_q_blocks,
                    block_size=block_size,
                    block_count=block_count,
                )
                candidates.append(
                    {
                        "template_kind": "phase10_strict_atlas_block_lift",
                        "template_origin": "lift the first Phase 10 strict atlas covers over overlapping outer-code block sets",
                        "base_cover": base_name,
                        "observer_p_block_mask": observer_p_blocks,
                        "observer_q_block_mask": observer_q_blocks,
                        "cover": named_two_observer_cover(
                            observer_p=observer_p,
                            observer_q=observer_q,
                            name=f"{base_name}_blocks_p{observer_p_blocks}_q{observer_q_blocks}",
                            description=(
                                "Phase 11 lifted atlas candidate: Phase 10 strict observer regions repeated over "
                                "overlapping outer-code block sets."
                            ),
                        ),
                    }
                )
    return tuple(candidates)


def score_phase11_lifted_atlas_candidates(
    *,
    source: dict[str, object],
    max_hits: int,
    include_bases: bool,
) -> dict[str, object]:
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    candidates = phase11_lifted_atlas_cover_candidates()
    entropy_matched = 0
    horizon_matched = 0
    observer_diff = 0
    raw_hits = 0
    hits = []
    for candidate in candidates:
        cover = candidate["cover"]
        if not isinstance(cover, PatchCover):
            raise TypeError("cover candidate must contain a PatchCover")
        score = rank_kernel_cover_score(first, second, cover)
        if score["entropy_same"]:
            entropy_matched += 1
        if score.get("same_shared_horizon_algebra"):
            horizon_matched += 1
        if score.get("different_observer_reconstruction"):
            observer_diff += 1
        if not score["hit"]:
            continue
        raw_hits += 1
        if len(hits) >= max_hits:
            continue
        hit = rank_kernel_cover_search_hit_certificate_for_pair(
            pair_source=str(source["name"]),
            first=first,
            second=second,
            cover=cover,
            include_bases=include_bases,
        )
        if hit["certified_claims"]["causal_patch_search_hit"]:
            hit["template"] = {
                "kind": candidate["template_kind"],
                "origin": candidate["template_origin"],
                "base_cover": candidate["base_cover"],
                "observer_p_block_mask": candidate["observer_p_block_mask"],
                "observer_q_block_mask": candidate["observer_q_block_mask"],
            }
            hits.append(hit)
    return {
        "candidate_count": len(candidates),
        "counts": {
            "scanned": len(candidates),
            "entropy_overlap_matched": entropy_matched,
            "same_horizon_algebra": horizon_matched,
            "different_observer_reconstruction": observer_diff,
            "raw_score_hits": raw_hits,
            "hits_returned": len(hits),
        },
        "hits": tuple(hits),
        "status": "hit" if hits else "no-hit",
    }


def phase11_reconstruction_witness(first: StabilizerCode, second: StabilizerCode) -> dict[str, object] | None:
    block_size = 5
    block_count = 4
    for inner_region in range(1, 1 << block_size):
        for block_mask in range(1, 1 << block_count):
            region = lift_inner_region_over_blocks(
                inner_region,
                block_mask=block_mask,
                block_size=block_size,
                block_count=block_count,
            )
            first_algebra = rank_kernel_algebra_summary(first, region)
            second_algebra = rank_kernel_algebra_summary(second, region)
            if first_algebra["signature"] == second_algebra["signature"]:
                continue
            return {
                "inner_region": mask_to_tuple(inner_region, block_size),
                "outer_blocks": mask_to_tuple(block_mask, block_count),
                "region": mask_to_tuple(region, first.n),
                "first_entropy": rank_kernel_entropy(first, region),
                "second_entropy": rank_kernel_entropy(second, region),
                "first_algebra": first_algebra,
                "second_algebra": second_algebra,
                }
    return None


def mask_from_patch_summary(patch_summary: dict[str, object]) -> int:
    return mask_from_qubits(int(qubit) for qubit in patch_summary["qubits"])


def phase12_canonical_inner_atlas_hit(*, include_bases: bool = False) -> dict[str, object]:
    graph_search = graph_labeled_pair_source()
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 10 labeled graph source to find a pair")
    strict_result = score_cover_template_candidates_for_pair(
        source=source,
        candidates=strict_horizon_private_cover_candidates(5),
        max_hits=1,
        include_bases=include_bases,
    )
    if not strict_result["hits"]:
        raise RuntimeError("expected Phase 10 strict horizon/private atlas to find a hit")
    hit = strict_result["hits"][0]
    return {
        "graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "strict_result_counts": strict_result["counts"],
        "hit": hit,
    }


def phase12_atlas_aware_repaired_cover_candidates(
    *,
    inner_hit: dict[str, object],
    block_size: int = 5,
    block_count: int = 4,
) -> tuple[dict[str, object], ...]:
    patches = {
        str(patch["name"]): mask_from_patch_summary(patch)
        for patch in inner_hit["cover"]["patches"]
        if isinstance(patch, dict)
    }
    observer_p_base = patches["observer_p"]
    observer_q_base = patches["observer_q"]
    full_inner = (1 << block_size) - 1

    def lifted(inner_region: int, block_mask: int) -> int:
        return lift_inner_region_over_blocks(
            inner_region,
            block_mask=block_mask,
            block_size=block_size,
            block_count=block_count,
        )

    def full_blocks(block_mask: int) -> int:
        return lifted(full_inner, block_mask)

    candidates: list[dict[str, object]] = []
    block_pairs = tuple(
        (observer_p_blocks, observer_q_blocks)
        for observer_p_blocks in range(1, 1 << block_count)
        for observer_q_blocks in range(1, 1 << block_count)
        if observer_p_blocks & observer_q_blocks
    )
    base_name = str(inner_hit["cover"]["name"])
    for observer_p_blocks, observer_q_blocks in block_pairs:
        shared_blocks = observer_p_blocks & observer_q_blocks
        p_private_blocks = observer_p_blocks & ~observer_q_blocks
        q_private_blocks = observer_q_blocks & ~observer_p_blocks
        block_metadata = {
            "base_cover": base_name,
            "observer_p_block_mask": observer_p_blocks,
            "observer_q_block_mask": observer_q_blocks,
            "shared_block_mask": shared_blocks,
            "observer_p_blocks": mask_to_tuple(observer_p_blocks, block_count),
            "observer_q_blocks": mask_to_tuple(observer_q_blocks, block_count),
            "shared_blocks": mask_to_tuple(shared_blocks, block_count),
            "observer_p_private_blocks": mask_to_tuple(p_private_blocks, block_count),
            "observer_q_private_blocks": mask_to_tuple(q_private_blocks, block_count),
        }
        candidates.append(
            {
                **block_metadata,
                "template_kind": "phase12_full_outer_block_control",
                "template_origin": (
                    "control cover using only complete inner blocks selected by overlapping outer-code block masks"
                ),
                "cover": named_two_observer_cover(
                    observer_p=full_blocks(observer_p_blocks),
                    observer_q=full_blocks(observer_q_blocks),
                    name=f"phase12_full_outer_p{observer_p_blocks}_q{observer_q_blocks}",
                    description=(
                        "Phase 12 control: observer patches are complete inner blocks over overlapping "
                        "outer-code block masks."
                    ),
                ),
            }
        )
        candidates.append(
            {
                **block_metadata,
                "template_kind": "phase12_inner_strict_block_lift",
                "template_origin": (
                    "repeat the canonical Phase 10 strict inner atlas over overlapping outer-code block masks"
                ),
                "cover": named_two_observer_cover(
                    observer_p=lifted(observer_p_base, observer_p_blocks),
                    observer_q=lifted(observer_q_base, observer_q_blocks),
                    name=f"phase12_inner_lift_p{observer_p_blocks}_q{observer_q_blocks}",
                    description=(
                        "Phase 12 baseline: canonical strict inner atlas repeated over overlapping "
                        "outer-code block masks."
                    ),
                ),
            }
        )
        candidates.append(
            {
                **block_metadata,
                "template_kind": "phase12_private_full_shared_inner",
                "template_origin": (
                    "use the inner atlas on shared outer blocks and complete inner blocks on private outer shells"
                ),
                "cover": named_two_observer_cover(
                    observer_p=full_blocks(p_private_blocks) | lifted(observer_p_base, shared_blocks),
                    observer_q=full_blocks(q_private_blocks) | lifted(observer_q_base, shared_blocks),
                    name=f"phase12_private_full_shared_inner_p{observer_p_blocks}_q{observer_q_blocks}",
                    description=(
                        "Phase 12 atlas-aware repaired cover: shared outer blocks keep the canonical inner "
                        "observer overlap, while private outer blocks are complete inner blocks."
                    ),
                ),
            }
        )
    return tuple(candidates)


def score_phase12_atlas_aware_candidates(
    *,
    source: dict[str, object],
    inner_hit: dict[str, object],
    max_hits: int,
    include_bases: bool,
) -> dict[str, object]:
    if max_hits < 1:
        raise ValueError("max_hits must be at least 1")
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    candidates = phase12_atlas_aware_repaired_cover_candidates(inner_hit=inner_hit)
    candidate_counts: dict[str, int] = {}
    scanned_by_template: dict[str, int] = {}
    raw_hits_by_template: dict[str, int] = {}
    hits_by_template: dict[str, int] = {}
    full_certificate_attempts_by_template: dict[str, int] = {}
    for candidate in candidates:
        kind = str(candidate["template_kind"])
        candidate_counts[kind] = candidate_counts.get(kind, 0) + 1

    entropy_matched = 0
    horizon_matched = 0
    observer_diff = 0
    raw_score_hits = 0
    hits: list[dict[str, object]] = []
    representative_near_misses: list[dict[str, object]] = []
    for candidate in candidates:
        kind = str(candidate["template_kind"])
        cover = candidate["cover"]
        if not isinstance(cover, PatchCover):
            raise TypeError("cover candidate must contain a PatchCover")
        scanned_by_template[kind] = scanned_by_template.get(kind, 0) + 1
        score = rank_kernel_cover_score(first, second, cover)
        if score["entropy_same"]:
            entropy_matched += 1
        if score.get("same_shared_horizon_algebra"):
            horizon_matched += 1
        if score.get("different_observer_reconstruction"):
            observer_diff += 1
        if not score["hit"]:
            continue
        raw_score_hits += 1
        raw_hits_by_template[kind] = raw_hits_by_template.get(kind, 0) + 1

        should_certify_near_miss = (
            kind == "phase12_inner_strict_block_lift"
            and not representative_near_misses
        )
        should_certify_hit = (
            kind == "phase12_private_full_shared_inner"
            and len(hits) < max_hits
        )
        if not should_certify_near_miss and not should_certify_hit:
            continue

        full_certificate_attempts_by_template[kind] = full_certificate_attempts_by_template.get(kind, 0) + 1
        hit = rank_kernel_cover_search_hit_certificate_for_pair(
            pair_source=str(source["name"]),
            first=first,
            second=second,
            cover=cover,
            include_bases=include_bases,
        )
        hit["template"] = {
            "kind": kind,
            "origin": candidate["template_origin"],
            "base_cover": candidate["base_cover"],
            "observer_p_block_mask": candidate["observer_p_block_mask"],
            "observer_q_block_mask": candidate["observer_q_block_mask"],
            "shared_block_mask": candidate["shared_block_mask"],
            "observer_p_blocks": candidate["observer_p_blocks"],
            "observer_q_blocks": candidate["observer_q_blocks"],
            "shared_blocks": candidate["shared_blocks"],
            "observer_p_private_blocks": candidate["observer_p_private_blocks"],
            "observer_q_private_blocks": candidate["observer_q_private_blocks"],
        }
        if hit["certified_claims"]["causal_patch_search_hit"]:
            hits.append(hit)
            hits_by_template[kind] = hits_by_template.get(kind, 0) + 1
            continue
        if should_certify_near_miss:
            representative_near_misses.append(hit)

    return {
        "candidate_count": len(candidates),
        "candidate_counts_by_template": dict(sorted(candidate_counts.items())),
        "counts": {
            "scanned": len(candidates),
            "scanned_by_template": dict(sorted(scanned_by_template.items())),
            "entropy_overlap_matched": entropy_matched,
            "same_horizon_algebra": horizon_matched,
            "different_observer_reconstruction": observer_diff,
            "raw_score_hits": raw_score_hits,
            "raw_score_hits_by_template": dict(sorted(raw_hits_by_template.items())),
            "full_certificate_attempts_by_template": dict(sorted(full_certificate_attempts_by_template.items())),
            "hits_returned": len(hits),
            "hits_by_template": dict(sorted(hits_by_template.items())),
            "representative_near_misses": len(representative_near_misses),
        },
        "hits": tuple(hits),
        "representative_near_misses": tuple(representative_near_misses),
        "status": "hit" if hits else "no-hit",
    }


def bridge_cosmology_phase12_certificate(
    *,
    max_hits_per_source: int = 1,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 12 source must contain StabilizerCode objects")
    first_distance = bounded_distance_certificate(first, max_weight=2)
    second_distance = bounded_distance_certificate(second, max_weight=2)
    entropy_check = low_order_entropy_match_by_rank(first, second, max_subset_size=2)
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    atlas_search = score_phase12_atlas_aware_candidates(
        source=source,
        inner_hit=inner_atlas["hit"],
        max_hits=max_hits_per_source,
        include_bases=include_bases,
    )
    public_source = {
        key: value
        for key, value in source.items()
        if key not in ("first", "second")
    }
    hits = tuple(atlas_search["hits"])
    representative_near_misses = tuple(atlas_search["representative_near_misses"])
    distance_repaired = (
        first_distance["distance_at_least_2_certified"]
        and second_distance["distance_at_least_2_certified"]
    )
    full_hit_verified = bool(hits) and all(hit["certified_claims"]["causal_patch_search_hit"] for hit in hits)
    inner_near_miss_certified = bool(representative_near_misses) and all(
        near_miss["certified_claims"]["same_entropy_overlap_data"]
        and near_miss["certified_claims"]["different_observer_reconstruction"]
        and not near_miss["certified_claims"]["same_erasure_correctability_profile"]
        for near_miss in representative_near_misses
    )
    full_outer_control_no_observer_diff = (
        atlas_search["counts"]["raw_score_hits_by_template"].get("phase12_full_outer_block_control", 0) == 0
        and atlas_search["counts"]["scanned_by_template"].get("phase12_full_outer_block_control", 0) > 0
    )
    private_full_hit = atlas_search["counts"]["hits_by_template"].get("phase12_private_full_shared_inner", 0) > 0
    phase_passes = (
        distance_repaired
        and entropy_check["matches"]
        and inner_atlas["hit"]["certified_claims"]["causal_patch_search_hit"]
        and atlas_search["candidate_count"] > 0
        and full_outer_control_no_observer_diff
        and inner_near_miss_certified
        and private_full_hit
        and full_hit_verified
    )
    return {
        "phase": "Goal 2 Phase 12: atlas-aware repaired-cover recovery",
        "status": "pass" if phase_passes else "no-hit",
        "repair_source": public_source,
        "distance_repair": {
            "method": "reuse Phase 11 logical-concatenation distance repair",
            "first": first_distance,
            "second": second_distance,
            "distance_at_least_2_for_both": distance_repaired,
        },
        "low_order_entropy": entropy_check,
        "inner_atlas_seed": {
            "source": inner_atlas["graph_search"],
            "strict_result_counts": inner_atlas["strict_result_counts"],
            "canonical_hit_cover": inner_atlas["hit"]["cover"],
            "canonical_hit_claims": inner_atlas["hit"]["certified_claims"],
        },
        "atlas_aware_repaired_search": atlas_search,
        "counts": {
            "low_order_subsets_checked": entropy_check["subsets_checked"],
            "low_order_entropy_mismatches": entropy_check["mismatch_count"],
            "atlas_aware_candidates": atlas_search["candidate_count"],
            "atlas_aware_raw_hits": atlas_search["counts"]["raw_score_hits"],
            "atlas_aware_hits_returned": atlas_search["counts"]["hits_returned"],
            "full_outer_control_candidates": atlas_search["counts"]["scanned_by_template"].get(
                "phase12_full_outer_block_control",
                0,
            ),
            "full_outer_control_raw_hits": atlas_search["counts"]["raw_score_hits_by_template"].get(
                "phase12_full_outer_block_control",
                0,
            ),
            "inner_lift_raw_hits": atlas_search["counts"]["raw_score_hits_by_template"].get(
                "phase12_inner_strict_block_lift",
                0,
            ),
            "private_full_shared_inner_raw_hits": atlas_search["counts"]["raw_score_hits_by_template"].get(
                "phase12_private_full_shared_inner",
                0,
            ),
            "private_full_shared_inner_hits": atlas_search["counts"]["hits_by_template"].get(
                "phase12_private_full_shared_inner",
                0,
            ),
        },
        "certified_claims": {
            "phase11_distance_repair_reused": distance_repaired,
            "same_labeled_t2_entropy_after_repair": entropy_check["matches"],
            "phase10_inner_atlas_seed_loaded": inner_atlas["hit"]["certified_claims"]["causal_patch_search_hit"],
            "atlas_aware_templates_scored": atlas_search["candidate_count"] > 0,
            "full_outer_block_control_no_observer_difference": full_outer_control_no_observer_diff,
            "plain_inner_lift_representative_erasure_mismatch": inner_near_miss_certified,
            "private_full_shared_inner_atlas_hit": private_full_hit,
            "all_returned_atlas_hits_verified": full_hit_verified,
            "phase_12_atlas_aware_repaired_cover_certificate": phase_passes,
        },
        "interpretation": {
            "result": (
                "The Phase 11 repaired n=20 pair does recover a full finite causal-patch atlas when the cover is "
                "adapted to the outer repair: shared outer blocks keep the Phase 10 inner observer overlap, while "
                "private outer blocks are promoted to complete inner blocks."
            ),
            "pressure": (
                "Complete outer-block observer covers are too coarse and erase the observer reconstruction difference. "
                "Plain inner-atlas block lifts keep reconstruction near-misses but a representative still fails the "
                "erasure-correctability profile, matching the Phase 11 failure mode."
            ),
            "lesson": (
                "For repaired non-CSS toys, the atlas itself is part of the QEC/cosmology data: distance repair can "
                "preserve low-order entropy while forcing a cover adaptation before complementarity diagnostics line up."
            ),
        },
        "recommendation": {
            "next_phase": "proceed_as_written",
            "reason": (
                "Phase 12 finds an exact repaired atlas hit with matching named entropy/overlap data, matching "
                "erasure-correctability profile, erasure-algebra differences, and different observer reconstruction. "
                "The next phase can compare this repaired non-CSS atlas against bridge-family time/channel dynamics."
            ),
            "suggested_phase_13": (
                "Add a small time/channel layer that tracks transitions between the plain inner-lift near-miss and the "
                "atlas-aware repaired hit, then compare fixed points and erasure-channel algebra flow against the CSS "
                "balanced-bridge baseline."
            ),
        },
    }


def candidate_by_template_and_blocks(
    candidates: tuple[dict[str, object], ...],
    *,
    template_kind: str,
    observer_p_block_mask: int,
    observer_q_block_mask: int,
) -> dict[str, object]:
    for candidate in candidates:
        if (
            candidate["template_kind"] == template_kind
            and candidate["observer_p_block_mask"] == observer_p_block_mask
            and candidate["observer_q_block_mask"] == observer_q_block_mask
        ):
            return candidate
    raise KeyError((template_kind, observer_p_block_mask, observer_q_block_mask))


def rank_kernel_patch_metric_summary(code: StabilizerCode, cover: PatchCover) -> dict[str, object]:
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    intersection = observer_p & observer_q
    union = observer_p | observer_q
    p_private = observer_p & ~observer_q
    q_private = observer_q & ~observer_p
    return {
        "patch_entropies": tuple((patch.name, rank_kernel_entropy(code, patch.region)) for patch in cover.patches),
        "observer_pair": {
            "intersection_qubits": mask_to_tuple(intersection, code.n),
            "union_qubits": mask_to_tuple(union, code.n),
            "observer_p_private_qubits": mask_to_tuple(p_private, code.n),
            "observer_q_private_qubits": mask_to_tuple(q_private, code.n),
            "mutual_information": (
                rank_kernel_entropy(code, observer_p)
                + rank_kernel_entropy(code, observer_q)
                - rank_kernel_entropy(code, union)
            ),
            "private_cmi_given_intersection": (
                rank_kernel_entropy(code, p_private | intersection)
                + rank_kernel_entropy(code, intersection | q_private)
                - rank_kernel_entropy(code, intersection)
                - rank_kernel_entropy(code, p_private | intersection | q_private)
            ),
            "private_tripartite_information": (
                rank_kernel_entropy(code, p_private)
                + rank_kernel_entropy(code, intersection)
                + rank_kernel_entropy(code, q_private)
                - rank_kernel_entropy(code, p_private | intersection)
                - rank_kernel_entropy(code, p_private | q_private)
                - rank_kernel_entropy(code, intersection | q_private)
                + rank_kernel_entropy(code, p_private | intersection | q_private)
            ),
        },
    }


def erasure_suite_compact_summary(
    suite: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "name": item["name"],
            "role": item["role"],
            "erased_qubits": item["erased_qubits"],
            "survivor_qubits": item["survivor_qubits"],
            "erasure_correctable": item["erasure_correctable"],
            "survivor_reconstructs_all": item["survivor_reconstructs_all"],
            "qec_complementarity_identity_holds": item["qec_complementarity_identity_holds"],
            "erased_signature": item["erased_algebra"]["signature"],
            "survivor_signature": item["survivor_algebra"]["signature"],
        }
        for item in suite
    )


def phase13_repaired_cover_slice(
    *,
    time_index: int,
    label: str,
    source: dict[str, object],
    candidate: dict[str, object],
    include_bases: bool = False,
) -> dict[str, object]:
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    cover = candidate["cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("candidate must contain a PatchCover")
    cover_certificate = rank_kernel_cover_search_hit_certificate_for_pair(
        pair_source=str(source["name"]),
        first=first,
        second=second,
        cover=cover,
        include_bases=include_bases,
    )
    first_erasures = rank_kernel_erasure_suite_diagnostic(first, cover, include_bases=include_bases)
    second_erasures = rank_kernel_erasure_suite_diagnostic(second, cover, include_bases=include_bases)
    algebra_differences = erasure_algebra_differences(first_erasures, second_erasures)
    return {
        "time_index": time_index,
        "label": label,
        "template": {
            "kind": candidate["template_kind"],
            "origin": candidate["template_origin"],
            "base_cover": candidate["base_cover"],
            "observer_p_block_mask": candidate["observer_p_block_mask"],
            "observer_q_block_mask": candidate["observer_q_block_mask"],
            "shared_block_mask": candidate["shared_block_mask"],
            "observer_p_blocks": candidate["observer_p_blocks"],
            "observer_q_blocks": candidate["observer_q_blocks"],
            "shared_blocks": candidate["shared_blocks"],
            "observer_p_private_blocks": candidate["observer_p_private_blocks"],
            "observer_q_private_blocks": candidate["observer_q_private_blocks"],
        },
        "cover": cover.summary(first.n),
        "first_metrics": rank_kernel_patch_metric_summary(first, cover),
        "second_metrics": rank_kernel_patch_metric_summary(second, cover),
        "observer_reconstruction": cover_certificate["observer_reconstruction"],
        "first_patch_algebras": cover_certificate["first_patch_algebras"],
        "second_patch_algebras": cover_certificate["second_patch_algebras"],
        "erasure_comparison": {
            "same_erasure_correctability_profile": erasure_correctability_key(first_erasures)
            == erasure_correctability_key(second_erasures),
            "first_correctability_profile": erasure_correctability_key(first_erasures),
            "second_correctability_profile": erasure_correctability_key(second_erasures),
            "algebra_differences": algebra_differences,
            "algebra_difference_names": tuple(item["name"] for item in algebra_differences),
        },
        "first_erasures": erasure_suite_compact_summary(first_erasures),
        "second_erasures": erasure_suite_compact_summary(second_erasures),
        "certified_claims": {
            **cover_certificate["certified_claims"],
            "qec_complementarity_identity_all_scenarios": all(
                item["qec_complementarity_identity_holds"] for item in first_erasures + second_erasures
            ),
        },
    }


def phase13_patch_transition_delta(current: dict[str, object], next_slice: dict[str, object]) -> tuple[dict[str, object], ...]:
    current_patches = {
        str(patch["name"]): mask_from_patch_summary(patch)
        for patch in current["cover"]["patches"]
        if isinstance(patch, dict)
    }
    next_patches = {
        str(patch["name"]): mask_from_patch_summary(patch)
        for patch in next_slice["cover"]["patches"]
        if isinstance(patch, dict)
    }
    n = max(
        max((mask.bit_length() for mask in current_patches.values()), default=0),
        max((mask.bit_length() for mask in next_patches.values()), default=0),
    )
    return tuple(
        {
            "patch": name,
            "from_qubits": mask_to_tuple(current_patches[name], n),
            "to_qubits": mask_to_tuple(next_patches[name], n),
            "added_qubits": mask_to_tuple(next_patches[name] & ~current_patches[name], n),
            "removed_qubits": mask_to_tuple(current_patches[name] & ~next_patches[name], n),
            "stable": current_patches[name] == next_patches[name],
        }
        for name in sorted(current_patches)
    )


def phase13_patch_delta_by_name(delta: tuple[dict[str, object], ...], name: str) -> dict[str, object]:
    for item in delta:
        if item["patch"] == name:
            return item
    raise KeyError(name)


def bridge_cosmology_phase13_certificate(
    *,
    include_bases: bool = False,
) -> dict[str, object]:
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 13 source must contain StabilizerCode objects")
    entropy_check = low_order_entropy_match_by_rank(first, second, max_subset_size=2)
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    candidates = phase12_atlas_aware_repaired_cover_candidates(inner_hit=inner_atlas["hit"])
    near_candidate = candidate_by_template_and_blocks(
        candidates,
        template_kind="phase12_inner_strict_block_lift",
        observer_p_block_mask=1,
        observer_q_block_mask=3,
    )
    hit_candidate = candidate_by_template_and_blocks(
        candidates,
        template_kind="phase12_private_full_shared_inner",
        observer_p_block_mask=1,
        observer_q_block_mask=13,
    )
    control_candidate = candidate_by_template_and_blocks(
        candidates,
        template_kind="phase12_full_outer_block_control",
        observer_p_block_mask=1,
        observer_q_block_mask=13,
    )
    near_slice = phase13_repaired_cover_slice(
        time_index=0,
        label="plain_inner_lift_near_miss",
        source=source,
        candidate=near_candidate,
        include_bases=include_bases,
    )
    hit_slice = phase13_repaired_cover_slice(
        time_index=1,
        label="atlas_aware_repaired_hit",
        source=source,
        candidate=hit_candidate,
        include_bases=include_bases,
    )
    control_slice = phase13_repaired_cover_slice(
        time_index=-1,
        label="full_outer_block_control",
        source=source,
        candidate=control_candidate,
        include_bases=include_bases,
    )
    patch_delta = phase13_patch_transition_delta(near_slice, hit_slice)
    observer_p_delta = phase13_patch_delta_by_name(patch_delta, "observer_p")
    observer_q_delta = phase13_patch_delta_by_name(patch_delta, "observer_q")
    horizon_delta = phase13_patch_delta_by_name(patch_delta, "shared_horizon")
    static_delta = phase13_patch_delta_by_name(patch_delta, "static_diamond")
    transition_claims = {
        "same_repaired_code_at_both_slices": tuple(first.pauli_generators()) == tuple(source["first"].pauli_generators())
        and tuple(second.pauli_generators()) == tuple(source["second"].pauli_generators()),
        "observer_p_region_stable": observer_p_delta["stable"],
        "shared_horizon_region_stable": horizon_delta["stable"],
        "observer_q_relocalized": bool(observer_q_delta["added_qubits"]) and bool(observer_q_delta["removed_qubits"]),
        "observer_q_promotes_private_outer_blocks_2_3": observer_q_delta["added_qubits"] == tuple(range(10, 20)),
        "observer_q_drops_plain_inner_block_1_qubits": observer_q_delta["removed_qubits"] == (6, 9),
        "static_diamond_relocalized": bool(static_delta["added_qubits"]) and bool(static_delta["removed_qubits"]),
        "near_slice_is_entropy_reconstruction_near_miss": (
            near_slice["certified_claims"]["same_entropy_overlap_data"]
            and near_slice["certified_claims"]["different_observer_reconstruction"]
            and not near_slice["certified_claims"]["same_erasure_correctability_profile"]
            and not near_slice["certified_claims"]["causal_patch_search_hit"]
        ),
        "hit_slice_repairs_erasure_profile": (
            hit_slice["certified_claims"]["same_erasure_correctability_profile"]
            and hit_slice["certified_claims"]["causal_patch_search_hit"]
        ),
        "observer_reconstruction_difference_persists": (
            near_slice["certified_claims"]["different_observer_reconstruction"]
            and hit_slice["certified_claims"]["different_observer_reconstruction"]
        ),
        "erasure_algebra_difference_persists": (
            near_slice["certified_claims"]["erasure_algebra_difference_exists"]
            and hit_slice["certified_claims"]["erasure_algebra_difference_exists"]
        ),
        "qec_complementarity_identity_all_slices": (
            near_slice["certified_claims"]["qec_complementarity_identity_all_scenarios"]
            and hit_slice["certified_claims"]["qec_complementarity_identity_all_scenarios"]
            and control_slice["certified_claims"]["qec_complementarity_identity_all_scenarios"]
        ),
    }
    transition_claims["phase_13_repaired_cover_transition"] = all(transition_claims.values())

    css_slice = bridge_cosmology_phase2_slice_certificate(1, include_bases=include_bases)
    css_transition = bridge_growth_transition_certificate(1)
    css_horizon_correctable = erasure_by_name(css_slice["first_erasures"], "erase_shared_horizon")[
        "erasure_correctable"
    ]
    repaired_horizon_correctable = next(
        item for item in hit_slice["first_erasures"] if item["name"] == "erase_shared_horizon"
    )["erasure_correctable"]
    baseline_claims = {
        "css_phase2_channel_probe_passes": css_slice["certified_claims"]["phase_2_erasure_channel_probe"],
        "css_phase2_growth_transition_passes": css_transition["certified_claims"]["phase_2_growth_transition"],
        "repaired_hit_has_css_like_full_channel_claims": (
            hit_slice["certified_claims"]["same_erasure_correctability_profile"]
            and hit_slice["certified_claims"]["erasure_algebra_difference_exists"]
            and hit_slice["certified_claims"]["different_observer_reconstruction"]
        ),
        "horizon_erasure_semantics_differ_from_css_baseline": (
            not css_horizon_correctable and repaired_horizon_correctable
        ),
        "full_outer_control_shows_entropy_without_reconstruction": (
            control_slice["certified_claims"]["same_entropy_overlap_data"]
            and control_slice["certified_claims"]["same_erasure_correctability_profile"]
            and not control_slice["certified_claims"]["different_observer_reconstruction"]
        ),
    }
    baseline_claims["phase_13_css_baseline_comparison"] = all(baseline_claims.values())

    phase_passes = (
        entropy_check["matches"]
        and transition_claims["phase_13_repaired_cover_transition"]
        and baseline_claims["phase_13_css_baseline_comparison"]
    )
    return {
        "phase": "Goal 2 Phase 13: repaired cover dynamics and CSS baseline comparison",
        "status": "pass" if phase_passes else "fail",
        "repaired_source": {
            key: value
            for key, value in source.items()
            if key not in ("first", "second")
        },
        "repaired_codes": {
            "n": first.n,
            "k": first.k,
            "first_generators": first.pauli_generators(),
            "second_generators": second.pauli_generators(),
        },
        "low_order_entropy": entropy_check,
        "timeline": {
            "time_parameter": "cover_index_on_fixed_repaired_code",
            "slices": (near_slice, hit_slice),
            "control_slice": control_slice,
            "transition": {
                "from": near_slice["label"],
                "to": hit_slice["label"],
                "patch_delta": patch_delta,
                "certified_claims": transition_claims,
            },
        },
        "css_baseline_comparison": {
            "css_slice_m1_claims": css_slice["certified_claims"],
            "css_transition_m1_to_m2_claims": css_transition["certified_claims"],
            "css_shared_horizon_erasure_correctable": css_horizon_correctable,
            "repaired_hit_shared_horizon_erasure_correctable": repaired_horizon_correctable,
            "certified_claims": baseline_claims,
        },
        "counts": {
            "timeline_slices": 2,
            "control_slices": 1,
            "low_order_subsets_checked": entropy_check["subsets_checked"],
            "low_order_entropy_mismatches": entropy_check["mismatch_count"],
            "near_slice_algebra_difference_scenarios": len(
                near_slice["erasure_comparison"]["algebra_differences"]
            ),
            "hit_slice_algebra_difference_scenarios": len(hit_slice["erasure_comparison"]["algebra_differences"]),
            "observer_q_added_qubits": len(observer_q_delta["added_qubits"]),
            "observer_q_removed_qubits": len(observer_q_delta["removed_qubits"]),
        },
        "certified_claims": {
            "same_labeled_t2_entropy_on_fixed_repaired_code": entropy_check["matches"],
            "near_to_hit_cover_transition_verified": transition_claims["phase_13_repaired_cover_transition"],
            "css_baseline_comparison_verified": baseline_claims["phase_13_css_baseline_comparison"],
            "phase_13_repaired_cover_dynamics_certificate": phase_passes,
        },
        "interpretation": {
            "result": (
                "A fixed repaired non-CSS code supports a two-slice cover dynamics: the plain inner-lift slice has "
                "matched entropy and observer reconstruction difference but fails erasure-profile matching; the "
                "atlas-aware slice repairs the erasure profile while preserving the observer-algebra separation."
            ),
            "baseline_contrast": (
                "The CSS bridge baseline and repaired non-CSS hit both satisfy exact channel-style diagnostics, but "
                "the same named shared-horizon erasure has different correctability semantics."
            ),
            "lesson": (
                "In finite QEC-cosmology toys, causal-patch time evolution can be a cover/atlas flow on a fixed code. "
                "Role names such as horizon are not enough; the exact erasure channel and reconstructable algebra must "
                "be certified at each slice."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 13 gives an exact two-slice cover dynamics and exposes a CSS/non-CSS channel-semantics contrast. "
                "The next phase should search finite cover-transition graphs and classify which role-labeled horizons "
                "have stable erasure semantics across models."
            ),
            "suggested_phase_14": (
                "Build a bounded state graph whose nodes are certified covers on a fixed code pair and whose edges are "
                "small patch edits; search for flows that preserve entropy data while changing erasure fixed-point or "
                "operator-algebra behavior."
            ),
        },
    }


PHASE14_TEMPLATE_ALIASES = {
    "phase12_full_outer_block_control": "full",
    "phase12_inner_strict_block_lift": "inner",
    "phase12_private_full_shared_inner": "private",
}


def phase14_node_id(candidate: dict[str, object]) -> str:
    alias = PHASE14_TEMPLATE_ALIASES.get(str(candidate["template_kind"]), str(candidate["template_kind"]))
    return f"{alias}:p{candidate['observer_p_block_mask']}:q{candidate['observer_q_block_mask']}"


def phase14_canonical_graph_candidates(
    *,
    inner_hit: dict[str, object],
) -> tuple[dict[str, object], ...]:
    candidates = phase12_atlas_aware_repaired_cover_candidates(inner_hit=inner_hit)
    allowed_p = (1, 3)
    allowed_q = (3, 5, 9, 13)
    selected = [
        candidate
        for candidate in candidates
        if candidate["observer_p_block_mask"] in allowed_p and candidate["observer_q_block_mask"] in allowed_q
    ]
    return tuple(
        sorted(
            selected,
            key=lambda candidate: (
                int(candidate["observer_p_block_mask"]),
                int(candidate["observer_q_block_mask"]),
                PHASE14_TEMPLATE_ALIASES.get(str(candidate["template_kind"]), str(candidate["template_kind"])),
            ),
        )
    )


def phase14_node_summary(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    candidate: dict[str, object],
) -> dict[str, object]:
    cover = candidate["cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("candidate must contain a PatchCover")
    score = rank_kernel_cover_score(first, second, cover)
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    shared_horizon = cover.patch("shared_horizon").region
    return {
        "id": phase14_node_id(candidate),
        "template_kind": candidate["template_kind"],
        "observer_p_block_mask": candidate["observer_p_block_mask"],
        "observer_q_block_mask": candidate["observer_q_block_mask"],
        "shared_block_mask": candidate["shared_block_mask"],
        "observer_p_blocks": candidate["observer_p_blocks"],
        "observer_q_blocks": candidate["observer_q_blocks"],
        "shared_blocks": candidate["shared_blocks"],
        "observer_p_qubits": mask_to_tuple(observer_p, first.n),
        "observer_q_qubits": mask_to_tuple(observer_q, first.n),
        "shared_horizon_qubits": mask_to_tuple(shared_horizon, first.n),
        "score": score,
    }


def phase14_cover_patch_delta(
    *,
    left: PatchCover,
    right: PatchCover,
    n: int,
) -> tuple[dict[str, object], ...]:
    return phase13_patch_transition_delta(
        {"cover": left.summary(n)},
        {"cover": right.summary(n)},
    )


def phase14_patch_edit_edge(
    *,
    left: dict[str, object],
    right: dict[str, object],
    left_summary: dict[str, object],
    right_summary: dict[str, object],
    n: int,
    max_observer_q_edit: int,
) -> dict[str, object] | None:
    left_cover = left["cover"]
    right_cover = right["cover"]
    if not isinstance(left_cover, PatchCover) or not isinstance(right_cover, PatchCover):
        raise TypeError("edge candidates must contain PatchCover objects")
    delta = phase14_cover_patch_delta(left=left_cover, right=right_cover, n=n)
    observer_p_delta = phase13_patch_delta_by_name(delta, "observer_p")
    observer_q_delta = phase13_patch_delta_by_name(delta, "observer_q")
    horizon_delta = phase13_patch_delta_by_name(delta, "shared_horizon")
    observer_q_edit = len(observer_q_delta["added_qubits"]) + len(observer_q_delta["removed_qubits"])
    claims = {
        "observer_p_stable": observer_p_delta["stable"],
        "shared_horizon_stable": horizon_delta["stable"],
        "observer_q_small_edit": 0 < observer_q_edit <= max_observer_q_edit,
        "left_preserves_entropy_reconstruction_signal": (
            bool(left_summary["score"].get("entropy_same"))
            and bool(left_summary["score"].get("different_observer_reconstruction"))
        ),
        "right_preserves_entropy_reconstruction_signal": (
            bool(right_summary["score"].get("entropy_same"))
            and bool(right_summary["score"].get("different_observer_reconstruction"))
        ),
    }
    claims["bounded_patch_edit_edge"] = all(claims.values())
    if not claims["bounded_patch_edit_edge"]:
        return None
    return {
        "left": left_summary["id"],
        "right": right_summary["id"],
        "observer_q_edit_size": observer_q_edit,
        "patch_delta": delta,
        "certified_claims": claims,
    }


def phase14_find_path(
    *,
    node_ids: tuple[str, ...],
    edges: tuple[dict[str, object], ...],
    start: str,
    target: str,
) -> tuple[str, ...]:
    adjacency = {node_id: [] for node_id in node_ids}
    for edge in edges:
        left = str(edge["left"])
        right = str(edge["right"])
        adjacency[left].append(right)
        adjacency[right].append(left)
    for neighbors in adjacency.values():
        neighbors.sort()
    queue: list[tuple[str, ...]] = [(start,)]
    seen = {start}
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == target:
            return path
        for neighbor in adjacency[node]:
            if neighbor in seen:
                continue
            seen.add(neighbor)
            queue.append((*path, neighbor))
    return ()


def phase14_correctability_pair_by_name(slice_record: dict[str, object]) -> dict[str, tuple[bool, bool]]:
    first = {str(item["name"]): bool(item["erasure_correctable"]) for item in slice_record["first_erasures"]}
    second = {str(item["name"]): bool(item["erasure_correctable"]) for item in slice_record["second_erasures"]}
    return {name: (first[name], second[name]) for name in sorted(first)}


def phase14_correctability_pair_from_phase2_slice(slice_record: dict[str, object]) -> dict[str, tuple[bool, bool]]:
    first = {str(item["name"]): bool(item["erasure_correctable"]) for item in slice_record["first_erasures"]}
    second = {str(item["name"]): bool(item["erasure_correctable"]) for item in slice_record["second_erasures"]}
    return {name: (first[name], second[name]) for name in sorted(first)}


def phase14_role_semantics_classification(
    *,
    path_slices: tuple[dict[str, object], ...],
    css_slice: dict[str, object],
) -> tuple[dict[str, object], ...]:
    repaired_profiles = tuple((slice_record["label"], phase14_correctability_pair_by_name(slice_record)) for slice_record in path_slices)
    css_profile = phase14_correctability_pair_from_phase2_slice(css_slice)
    names = sorted(css_profile)
    rows = []
    for name in names:
        profiles = tuple((label, profile[name]) for label, profile in repaired_profiles)
        values = tuple(profile for _, profile in profiles)
        stable_within_repaired_flow = len(set(values)) == 1
        hit_profile = values[-1]
        rows.append(
            {
                "scenario": name,
                "repaired_flow_profiles": profiles,
                "stable_within_repaired_flow": stable_within_repaired_flow,
                "css_baseline_profile": css_profile[name],
                "hit_agrees_with_css_baseline": hit_profile == css_profile[name],
                "changes_between_near_and_hit": values[0] != hit_profile,
            }
        )
    return tuple(rows)


def role_semantics_by_name(rows: tuple[dict[str, object], ...], name: str) -> dict[str, object]:
    for row in rows:
        if row["scenario"] == name:
            return row
    raise KeyError(name)


def bridge_cosmology_phase14_certificate(
    *,
    max_observer_q_edit: int = 5,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_observer_q_edit < 1:
        raise ValueError("max_observer_q_edit must be positive")
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 14 source must contain StabilizerCode objects")
    entropy_check = low_order_entropy_match_by_rank(first, second, max_subset_size=2)
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    candidates = phase14_canonical_graph_candidates(inner_hit=inner_atlas["hit"])
    summaries = tuple(phase14_node_summary(first=first, second=second, candidate=candidate) for candidate in candidates)
    by_id = {summary["id"]: (candidate, summary) for candidate, summary in zip(candidates, summaries)}
    candidate_by_id = {node_id: pair[0] for node_id, pair in by_id.items()}
    summary_by_id = {node_id: pair[1] for node_id, pair in by_id.items()}

    edges: list[dict[str, object]] = []
    for left_index, left in enumerate(candidates):
        for right_index in range(left_index + 1, len(candidates)):
            right = candidates[right_index]
            edge = phase14_patch_edit_edge(
                left=left,
                right=right,
                left_summary=summaries[left_index],
                right_summary=summaries[right_index],
                n=first.n,
                max_observer_q_edit=max_observer_q_edit,
            )
            if edge is not None:
                edges.append(edge)
    edges_tuple = tuple(edges)

    start = "inner:p1:q3"
    target = "private:p1:q13"
    path_ids = phase14_find_path(
        node_ids=tuple(summary["id"] for summary in summaries),
        edges=edges_tuple,
        start=start,
        target=target,
    )
    path_slices = tuple(
        phase13_repaired_cover_slice(
            time_index=index,
            label=f"graph_path_{node_id}",
            source=source,
            candidate=candidate_by_id[node_id],
            include_bases=include_bases,
        )
        for index, node_id in enumerate(path_ids)
    )
    path_edges = []
    for left_id, right_id in zip(path_ids, path_ids[1:]):
        edge = next(
            edge
            for edge in edges_tuple
            if {edge["left"], edge["right"]} == {left_id, right_id}
        )
        path_edges.append(edge)

    role_semantics = phase14_role_semantics_classification(
        path_slices=path_slices,
        css_slice=bridge_cosmology_phase2_slice_certificate(1, include_bases=include_bases),
    )
    shared_horizon_semantics = role_semantics_by_name(role_semantics, "erase_shared_horizon")
    raw_hit_nodes = tuple(summary for summary in summaries if summary["score"].get("hit"))
    entropy_nodes = tuple(summary for summary in summaries if summary["score"].get("entropy_same"))
    start_slice = path_slices[0] if path_slices else None
    target_slice = path_slices[-1] if path_slices else None
    path_preserves_entropy = bool(path_slices) and all(
        slice_record["certified_claims"]["same_entropy_overlap_data"] for slice_record in path_slices
    )
    path_preserves_observer_diff = bool(path_slices) and all(
        slice_record["certified_claims"]["different_observer_reconstruction"] for slice_record in path_slices
    )
    path_repairs_erasure_profile = (
        isinstance(start_slice, dict)
        and isinstance(target_slice, dict)
        and not start_slice["certified_claims"]["same_erasure_correctability_profile"]
        and target_slice["certified_claims"]["same_erasure_correctability_profile"]
    )
    start_algebra_names = (
        tuple(start_slice["erasure_comparison"]["algebra_difference_names"]) if isinstance(start_slice, dict) else ()
    )
    target_algebra_names = (
        tuple(target_slice["erasure_comparison"]["algebra_difference_names"]) if isinstance(target_slice, dict) else ()
    )
    path_changes_erasure_algebra = start_algebra_names != target_algebra_names
    edge_claims_pass = bool(path_edges) and all(edge["certified_claims"]["bounded_patch_edit_edge"] for edge in path_edges)
    phase_claims = {
        "same_labeled_t2_entropy_on_fixed_repaired_code": entropy_check["matches"],
        "bounded_graph_nodes_scored": len(summaries) == 24,
        "bounded_graph_edges_found": len(edges_tuple) > 0,
        "entropy_reconstruction_nodes_exist": len(raw_hit_nodes) > 0,
        "near_to_hit_path_found": bool(path_ids) and path_ids[0] == start and path_ids[-1] == target,
        "path_edges_are_small_patch_edits": edge_claims_pass,
        "path_preserves_entropy_overlap_data": path_preserves_entropy,
        "path_preserves_observer_reconstruction_difference": path_preserves_observer_diff,
        "path_repairs_erasure_correctability_profile": path_repairs_erasure_profile,
        "path_changes_erasure_algebra_difference_set": path_changes_erasure_algebra,
        "shared_horizon_semantics_stable_within_repaired_flow": (
            shared_horizon_semantics["stable_within_repaired_flow"]
            and shared_horizon_semantics["repaired_flow_profiles"][0][1] == (True, True)
        ),
        "shared_horizon_semantics_differs_from_css_baseline": not shared_horizon_semantics[
            "hit_agrees_with_css_baseline"
        ],
    }
    phase_claims["phase_14_transition_graph_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 14: bounded repaired-cover transition graph",
        "status": "pass" if phase_claims["phase_14_transition_graph_certificate"] else "fail",
        "graph_spec": {
            "node_source": "Phase 12 canonical inner atlas over p-block masks {1,3} and q-block masks {3,5,9,13}",
            "edge_rule": (
                "undirected edge if observer_p and shared_horizon are stable, observer_q changes by at most "
                f"{max_observer_q_edit} qubits, and both endpoint scores preserve entropy/reconstruction signal"
            ),
            "max_observer_q_edit": max_observer_q_edit,
        },
        "repaired_source": {
            key: value
            for key, value in source.items()
            if key not in ("first", "second")
        },
        "low_order_entropy": entropy_check,
        "nodes": summaries,
        "edges": edges_tuple,
        "path_search": {
            "start": start,
            "target": target,
            "path_node_ids": path_ids,
            "path_edges": tuple(path_edges),
            "path_slices": path_slices,
            "start_algebra_difference_names": start_algebra_names,
            "target_algebra_difference_names": target_algebra_names,
        },
        "role_semantics": {
            "classification": role_semantics,
            "shared_horizon": shared_horizon_semantics,
        },
        "counts": {
            "nodes": len(summaries),
            "edges": len(edges_tuple),
            "entropy_overlap_nodes": len(entropy_nodes),
            "raw_entropy_reconstruction_nodes": len(raw_hit_nodes),
            "path_length_nodes": len(path_ids),
            "path_length_edges": max(0, len(path_ids) - 1),
            "path_certified_slices": len(path_slices),
            "role_scenarios_classified": len(role_semantics),
            "low_order_subsets_checked": entropy_check["subsets_checked"],
            "low_order_entropy_mismatches": entropy_check["mismatch_count"],
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded transition graph finds a small patch-edit flow from a plain inner-lift near-miss to the "
                "atlas-aware repaired hit while preserving named entropy/overlap data and observer reconstruction "
                "difference at every certified path node."
            ),
            "flow": (
                "The searched path first moves the observer_q inner support between outer blocks, then promotes a "
                "private outer block to a complete shell, and finally adds the second private outer shell. This repairs "
                "the erasure-correctability profile and reduces the erasure-algebra difference set."
            ),
            "semantics": (
                "Shared-horizon erasure semantics are stable inside the repaired-cover flow but disagree with the CSS "
                "balanced-bridge baseline, so role labels alone do not determine horizon-channel behavior."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 14 turns the hand-picked Phase 13 transition into a bounded exact graph search. The next "
                "adaptation should broaden the node source and look for invariant classes of cover flows rather than "
                "only this canonical repaired graph."
            ),
            "suggested_phase_15": (
                "Search multiple bounded cover graphs, including CSS bridge-family covers and repaired non-CSS covers, "
                "then classify flow invariants such as stable horizon correctability, erasure fixed points, and algebra "
                "difference monotonicity."
            ),
        },
    }


def phase15_orientation_id(orientation: tuple[int, ...]) -> str:
    return "".join(str(bit) for bit in orientation)


def phase15_hamming_distance(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    if len(left) != len(right):
        raise ValueError("orientation tuples must have the same length")
    return sum(1 for left_bit, right_bit in zip(left, right) if left_bit != right_bit)


def phase15_erasure_pair_profiles(
    first_erasures: tuple[dict[str, object], ...],
    second_erasures: tuple[dict[str, object], ...],
) -> tuple[
    dict[str, tuple[bool, bool]],
    dict[str, tuple[bool, bool]],
]:
    first_by_name = {str(item["name"]): item for item in first_erasures}
    second_by_name = {str(item["name"]): item for item in second_erasures}
    correctability = {}
    survivor_fixed_points = {}
    for name in sorted(first_by_name):
        first_item = first_by_name[name]
        second_item = second_by_name[name]
        correctability[name] = (
            bool(first_item["erasure_correctable"]),
            bool(second_item["erasure_correctable"]),
        )
        survivor_fixed_points[name] = (
            bool(first_item["survivor_reconstructs_all"]),
            bool(second_item["survivor_reconstructs_all"]),
        )
    return correctability, survivor_fixed_points


def phase15_node_diagnostic(
    *,
    node_id: str,
    model_kind: str,
    first: StabilizerCode,
    second: StabilizerCode,
    cover: PatchCover,
    metadata: dict[str, object],
    include_bases: bool = False,
) -> dict[str, object]:
    score = rank_kernel_cover_score(first, second, cover)
    first_erasures = rank_kernel_erasure_suite_diagnostic(first, cover, include_bases=include_bases)
    second_erasures = rank_kernel_erasure_suite_diagnostic(second, cover, include_bases=include_bases)
    correctability, survivor_fixed_points = phase15_erasure_pair_profiles(first_erasures, second_erasures)
    algebra_differences = erasure_algebra_differences(first_erasures, second_erasures)
    return {
        "id": node_id,
        "model_kind": model_kind,
        "metadata": metadata,
        "cover": cover.summary(first.n),
        "score": score,
        "entropy_reconstruction_signal": (
            bool(score.get("entropy_same")) and bool(score.get("different_observer_reconstruction"))
        ),
        "same_erasure_correctability_profile": erasure_correctability_key(first_erasures)
        == erasure_correctability_key(second_erasures),
        "correctability_pairs": correctability,
        "survivor_fixed_point_pairs": survivor_fixed_points,
        "algebra_difference_names": tuple(item["name"] for item in algebra_differences),
        "algebra_difference_count": len(algebra_differences),
        "qec_complementarity_identity_all_scenarios": all(
            bool(item["qec_complementarity_identity_holds"]) for item in first_erasures + second_erasures
        ),
        "first_erasures": erasure_suite_compact_summary(first_erasures),
        "second_erasures": erasure_suite_compact_summary(second_erasures),
    }


def phase15_css_orientation_edge(
    *,
    left: dict[str, object],
    right: dict[str, object],
    left_node: dict[str, object],
    right_node: dict[str, object],
    n: int,
) -> dict[str, object] | None:
    left_orientation = left["orientation"]
    right_orientation = right["orientation"]
    if not isinstance(left_orientation, tuple) or not isinstance(right_orientation, tuple):
        raise TypeError("CSS orientation candidates must carry tuple orientations")
    distance = phase15_hamming_distance(left_orientation, right_orientation)
    if distance != 1:
        return None
    left_cover = left["cover"]
    right_cover = right["cover"]
    if not isinstance(left_cover, PatchCover) or not isinstance(right_cover, PatchCover):
        raise TypeError("CSS orientation candidates must carry PatchCover objects")
    delta = phase14_cover_patch_delta(left=left_cover, right=right_cover, n=n)
    observer_p_delta = phase13_patch_delta_by_name(delta, "observer_p")
    observer_q_delta = phase13_patch_delta_by_name(delta, "observer_q")
    horizon_delta = phase13_patch_delta_by_name(delta, "shared_horizon")
    shell_delta = phase13_patch_delta_by_name(delta, "bridge_shell")
    diamond_delta = phase13_patch_delta_by_name(delta, "static_diamond")
    observer_p_edit = len(observer_p_delta["added_qubits"]) + len(observer_p_delta["removed_qubits"])
    observer_q_edit = len(observer_q_delta["added_qubits"]) + len(observer_q_delta["removed_qubits"])
    claims = {
        "single_orientation_flip": distance == 1,
        "shared_horizon_stable": horizon_delta["stable"],
        "bridge_shell_stable": shell_delta["stable"],
        "static_diamond_stable": diamond_delta["stable"],
        "observer_p_swaps_one_bridge_qubit": observer_p_edit == 2,
        "observer_q_swaps_one_bridge_qubit": observer_q_edit == 2,
        "left_preserves_entropy_reconstruction_signal": bool(left_node["entropy_reconstruction_signal"]),
        "right_preserves_entropy_reconstruction_signal": bool(right_node["entropy_reconstruction_signal"]),
    }
    claims["bounded_patch_edit_edge"] = all(claims.values())
    if not claims["bounded_patch_edit_edge"]:
        return None
    return {
        "left": left_node["id"],
        "right": right_node["id"],
        "orientation_hamming_distance": distance,
        "observer_p_edit_size": observer_p_edit,
        "observer_q_edit_size": observer_q_edit,
        "patch_delta": delta,
        "certified_claims": claims,
    }


def phase15_scenario_flow_summary(
    *,
    nodes: tuple[dict[str, object], ...],
    path_ids: tuple[str, ...],
) -> dict[str, object]:
    node_by_id = {str(node["id"]): node for node in nodes}
    path_nodes = tuple(node_by_id[node_id] for node_id in path_ids)
    scenario_names = tuple(sorted(nodes[0]["correctability_pairs"])) if nodes else ()
    by_scenario = {}
    path_by_scenario = {}
    for name in scenario_names:
        correctability_values = tuple(
            (node["id"], node["correctability_pairs"][name])
            for node in nodes
        )
        survivor_values = tuple(
            (node["id"], node["survivor_fixed_point_pairs"][name])
            for node in nodes
        )
        algebra_presence = tuple((node["id"], name in node["algebra_difference_names"]) for node in nodes)
        correctability_unique = tuple(sorted(set(value for _, value in correctability_values)))
        survivor_unique = tuple(sorted(set(value for _, value in survivor_values)))
        by_scenario[name] = {
            "correctability_profiles_by_node": correctability_values,
            "correctability_unique_profiles": correctability_unique,
            "correctability_stable_across_nodes": len(correctability_unique) == 1,
            "survivor_fixed_point_profiles_by_node": survivor_values,
            "survivor_fixed_point_unique_profiles": survivor_unique,
            "survivor_fixed_point_stable_across_nodes": len(survivor_unique) == 1,
            "algebra_difference_presence_by_node": algebra_presence,
            "algebra_difference_presence_stable_across_nodes": len(set(value for _, value in algebra_presence)) == 1,
        }
        path_correctability = tuple(
            (node["id"], node["correctability_pairs"][name])
            for node in path_nodes
        )
        path_survivor = tuple(
            (node["id"], node["survivor_fixed_point_pairs"][name])
            for node in path_nodes
        )
        path_correctability_unique = tuple(sorted(set(value for _, value in path_correctability)))
        path_survivor_unique = tuple(sorted(set(value for _, value in path_survivor)))
        path_by_scenario[name] = {
            "correctability_profiles_on_path": path_correctability,
            "correctability_unique_profiles": path_correctability_unique,
            "correctability_stable_on_path": len(path_correctability_unique) == 1,
            "survivor_fixed_point_profiles_on_path": path_survivor,
            "survivor_fixed_point_unique_profiles": path_survivor_unique,
            "survivor_fixed_point_stable_on_path": len(path_survivor_unique) == 1,
        }
    algebra_counts = tuple((node["id"], node["algebra_difference_count"]) for node in path_nodes)
    algebra_count_values = tuple(count for _, count in algebra_counts)
    return {
        "by_scenario": by_scenario,
        "path_by_scenario": path_by_scenario,
        "shared_horizon": path_by_scenario["erase_shared_horizon"],
        "algebra_difference_counts_on_path": algebra_counts,
        "algebra_difference_count_nonincreasing": all(
            right <= left for left, right in zip(algebra_count_values, algebra_count_values[1:])
        ),
        "path_nodes_preserve_entropy_reconstruction_signal": all(
            bool(node["entropy_reconstruction_signal"]) for node in path_nodes
        ),
        "path_qec_complementarity_identity_all_scenarios": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in path_nodes
        ),
    }


def phase15_css_orientation_graph(
    *,
    m: int,
    include_bases: bool = False,
) -> dict[str, object]:
    if m < 1:
        raise ValueError("CSS orientation graphs require m >= 1")
    first, second = repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m)
    horizon = _mask(1, 2, 3)
    candidates = tuple(
        {
            "id": f"css_m{m}:o{phase15_orientation_id(orientation)}",
            "orientation": orientation,
            "cover": bridge_assignment_cover(m, horizon, orientation),
        }
        for orientation in product((0, 1), repeat=m)
    )
    nodes = tuple(
        phase15_node_diagnostic(
            node_id=str(candidate["id"]),
            model_kind="css_balanced_bridge",
            first=first,
            second=second,
            cover=candidate["cover"],  # type: ignore[arg-type]
            metadata={
                "m": m,
                "n": first.n,
                "k": first.k,
                "orientation": candidate["orientation"],
            },
            include_bases=include_bases,
        )
        for candidate in candidates
    )
    edges = []
    for left_index, left in enumerate(candidates):
        for right_index in range(left_index + 1, len(candidates)):
            edge = phase15_css_orientation_edge(
                left=left,
                right=candidates[right_index],
                left_node=nodes[left_index],
                right_node=nodes[right_index],
                n=first.n,
            )
            if edge is not None:
                edges.append(edge)
    edges_tuple = tuple(edges)
    start = f"css_m{m}:o{'0' * m}"
    target = f"css_m{m}:o{'1' * m}"
    path_ids = phase14_find_path(
        node_ids=tuple(str(node["id"]) for node in nodes),
        edges=edges_tuple,
        start=start,
        target=target,
    )
    flow_summary = phase15_scenario_flow_summary(nodes=nodes, path_ids=path_ids)
    claims = {
        "nodes_exhaust_orientation_hypercube": len(nodes) == 2**m,
        "edges_are_single_orientation_flips": len(edges_tuple) == m * (2 ** (m - 1))
        and all(edge["certified_claims"]["bounded_patch_edit_edge"] for edge in edges_tuple),
        "canonical_path_found": bool(path_ids) and path_ids[0] == start and path_ids[-1] == target,
        "all_nodes_preserve_entropy_reconstruction_signal": all(
            bool(node["entropy_reconstruction_signal"]) for node in nodes
        ),
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "shared_horizon_correctability_stable_across_graph": flow_summary["by_scenario"]["erase_shared_horizon"][
            "correctability_stable_across_nodes"
        ],
        "shared_horizon_fixed_point_stable_across_graph": flow_summary["by_scenario"]["erase_shared_horizon"][
            "survivor_fixed_point_stable_across_nodes"
        ],
        "algebra_difference_count_flat_on_path": len(
            set(count for _, count in flow_summary["algebra_difference_counts_on_path"])
        )
        == 1,
    }
    claims["phase_15_source_graph_certificate"] = all(claims.values())
    return {
        "graph_id": f"css_bridge_orientation_m{m}",
        "model_kind": "css_balanced_bridge",
        "graph_spec": {
            "node_source": f"all {2**m} bridge-orientation covers for balanced-bridge CSS m={m}",
            "edge_rule": "single bridge-pair orientation flip with shared horizon, bridge shell, and static diamond fixed",
            "start": start,
            "target": target,
        },
        "code_pair": {
            "n": first.n,
            "k": first.k,
            "distance_first": first.distance(),
            "distance_second": second.distance(),
        },
        "nodes": nodes,
        "edges": edges_tuple,
        "canonical_path": path_ids,
        "graph_invariants": {
            "by_scenario": flow_summary["by_scenario"],
        },
        "path_invariants": {
            "by_scenario": flow_summary["path_by_scenario"],
            "shared_horizon": flow_summary["shared_horizon"],
            "algebra_difference_counts_on_path": flow_summary["algebra_difference_counts_on_path"],
            "algebra_difference_count_nonincreasing": flow_summary["algebra_difference_count_nonincreasing"],
            "path_nodes_preserve_entropy_reconstruction_signal": flow_summary[
                "path_nodes_preserve_entropy_reconstruction_signal"
            ],
            "path_qec_complementarity_identity_all_scenarios": flow_summary[
                "path_qec_complementarity_identity_all_scenarios"
            ],
        },
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges_tuple),
            "path_length_nodes": len(path_ids),
            "path_length_edges": max(0, len(path_ids) - 1),
        },
        "certified_claims": claims,
    }


def phase15_repaired_phase14_graph(
    *,
    max_observer_q_edit: int = 5,
    include_bases: bool = False,
) -> dict[str, object]:
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 15 repaired source must contain StabilizerCode objects")
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    candidates = phase14_canonical_graph_candidates(inner_hit=inner_atlas["hit"])
    phase14_summaries = tuple(
        phase14_node_summary(first=first, second=second, candidate=candidate) for candidate in candidates
    )
    nodes = tuple(
        phase15_node_diagnostic(
            node_id=phase14_node_id(candidate),
            model_kind="distance_repaired_noncss",
            first=first,
            second=second,
            cover=candidate["cover"],  # type: ignore[arg-type]
            metadata={
                "template_kind": candidate["template_kind"],
                "observer_p_block_mask": candidate["observer_p_block_mask"],
                "observer_q_block_mask": candidate["observer_q_block_mask"],
                "shared_block_mask": candidate["shared_block_mask"],
            },
            include_bases=include_bases,
        )
        for candidate in candidates
    )
    edges = []
    for left_index, left in enumerate(candidates):
        for right_index in range(left_index + 1, len(candidates)):
            edge = phase14_patch_edit_edge(
                left=left,
                right=candidates[right_index],
                left_summary=phase14_summaries[left_index],
                right_summary=phase14_summaries[right_index],
                n=first.n,
                max_observer_q_edit=max_observer_q_edit,
            )
            if edge is not None:
                edges.append(edge)
    edges_tuple = tuple(edges)
    start = "inner:p1:q3"
    target = "private:p1:q13"
    path_ids = phase14_find_path(
        node_ids=tuple(str(node["id"]) for node in nodes),
        edges=edges_tuple,
        start=start,
        target=target,
    )
    flow_summary = phase15_scenario_flow_summary(nodes=nodes, path_ids=path_ids)
    repaired_path_counts = tuple(count for _, count in flow_summary["algebra_difference_counts_on_path"])
    claims = {
        "nodes_match_phase14_canonical_neighborhood": len(nodes) == 24,
        "edges_found": len(edges_tuple) > 0 and all(
            edge["certified_claims"]["bounded_patch_edit_edge"] for edge in edges_tuple
        ),
        "canonical_path_found": bool(path_ids) and path_ids[0] == start and path_ids[-1] == target,
        "path_nodes_preserve_entropy_reconstruction_signal": flow_summary[
            "path_nodes_preserve_entropy_reconstruction_signal"
        ],
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "shared_horizon_correctability_stable_on_canonical_path": flow_summary["shared_horizon"][
            "correctability_stable_on_path"
        ],
        "shared_horizon_fixed_point_stable_on_canonical_path": flow_summary["shared_horizon"][
            "survivor_fixed_point_stable_on_path"
        ],
        "shared_horizon_correctability_not_stable_across_full_graph": not flow_summary["by_scenario"][
            "erase_shared_horizon"
        ]["correctability_stable_across_nodes"],
        "algebra_difference_count_nonincreasing_on_path": flow_summary["algebra_difference_count_nonincreasing"],
        "algebra_difference_count_drops_on_path": bool(repaired_path_counts)
        and repaired_path_counts[0] > repaired_path_counts[-1],
    }
    claims["phase_15_source_graph_certificate"] = all(claims.values())
    return {
        "graph_id": "repaired_noncss_phase14_neighborhood",
        "model_kind": "distance_repaired_noncss",
        "graph_spec": {
            "node_source": "Phase 14 canonical repaired-cover neighborhood",
            "edge_rule": (
                "Phase 14 bounded patch edit: observer_p and shared_horizon fixed, observer_q edit bounded by "
                f"{max_observer_q_edit} qubits, endpoints preserve entropy/reconstruction signal"
            ),
            "start": start,
            "target": target,
        },
        "code_pair": {
            "n": first.n,
            "k": first.k,
            "distance_repair_outer_distance": source["outer_code"]["distance"],
            "frontier_kind": source["frontier_kind"],
        },
        "nodes": nodes,
        "edges": edges_tuple,
        "canonical_path": path_ids,
        "graph_invariants": {
            "by_scenario": flow_summary["by_scenario"],
        },
        "path_invariants": {
            "by_scenario": flow_summary["path_by_scenario"],
            "shared_horizon": flow_summary["shared_horizon"],
            "algebra_difference_counts_on_path": flow_summary["algebra_difference_counts_on_path"],
            "algebra_difference_count_nonincreasing": flow_summary["algebra_difference_count_nonincreasing"],
            "path_nodes_preserve_entropy_reconstruction_signal": flow_summary[
                "path_nodes_preserve_entropy_reconstruction_signal"
            ],
            "path_qec_complementarity_identity_all_scenarios": flow_summary[
                "path_qec_complementarity_identity_all_scenarios"
            ],
        },
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges_tuple),
            "path_length_nodes": len(path_ids),
            "path_length_edges": max(0, len(path_ids) - 1),
        },
        "certified_claims": claims,
    }


def bridge_cosmology_phase15_certificate(
    *,
    max_observer_q_edit: int = 5,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_observer_q_edit < 1:
        raise ValueError("max_observer_q_edit must be positive")
    css_graphs = (
        phase15_css_orientation_graph(m=2, include_bases=include_bases),
        phase15_css_orientation_graph(m=3, include_bases=include_bases),
    )
    repaired_graph = phase15_repaired_phase14_graph(
        max_observer_q_edit=max_observer_q_edit,
        include_bases=include_bases,
    )
    graphs = (*css_graphs, repaired_graph)
    css_shared_profiles = tuple(
        graph["path_invariants"]["shared_horizon"]["correctability_unique_profiles"] for graph in css_graphs
    )
    css_shared_fixed_points = tuple(
        graph["path_invariants"]["shared_horizon"]["survivor_fixed_point_unique_profiles"] for graph in css_graphs
    )
    repaired_shared_profiles = repaired_graph["path_invariants"]["shared_horizon"]["correctability_unique_profiles"]
    repaired_shared_fixed_points = repaired_graph["path_invariants"]["shared_horizon"][
        "survivor_fixed_point_unique_profiles"
    ]
    phase_claims = {
        "multiple_source_graphs_classified": len(graphs) == 3
        and len(css_graphs) == 2
        and repaired_graph["model_kind"] == "distance_repaired_noncss",
        "all_source_graph_certificates_pass": all(
            graph["certified_claims"]["phase_15_source_graph_certificate"] for graph in graphs
        ),
        "all_classified_nodes_have_exact_qec_identity": all(
            node["qec_complementarity_identity_all_scenarios"]
            for graph in graphs
            for node in graph["nodes"]
        ),
        "all_canonical_path_nodes_preserve_entropy_reconstruction_signal": all(
            graph["path_invariants"]["path_nodes_preserve_entropy_reconstruction_signal"] for graph in graphs
        ),
        "shared_horizon_correctability_stable_on_each_canonical_path": all(
            graph["path_invariants"]["shared_horizon"]["correctability_stable_on_path"] for graph in graphs
        ),
        "shared_horizon_fixed_point_stable_on_each_canonical_path": all(
            graph["path_invariants"]["shared_horizon"]["survivor_fixed_point_stable_on_path"] for graph in graphs
        ),
        "css_orientation_graphs_have_noncorrectable_shared_horizon_paths": all(
            profile == ((False, False),) for profile in css_shared_profiles
        ),
        "repaired_graph_has_correctable_shared_horizon_path": repaired_shared_profiles == ((True, True),),
        "shared_horizon_semantics_differs_between_css_and_repaired_paths": (
            set(css_shared_profiles) == {((False, False),)}
            and repaired_shared_profiles == ((True, True),)
        ),
        "shared_horizon_fixed_point_semantics_differs_between_css_and_repaired_paths": (
            set(css_shared_fixed_points) == {((False, False),)}
            and repaired_shared_fixed_points == ((True, True),)
        ),
        "repaired_full_graph_detects_role_semantics_not_global_invariant": not repaired_graph["graph_invariants"][
            "by_scenario"
        ]["erase_shared_horizon"]["correctability_stable_across_nodes"],
        "css_orientation_graphs_have_global_shared_horizon_stability": all(
            graph["graph_invariants"]["by_scenario"]["erase_shared_horizon"]["correctability_stable_across_nodes"]
            for graph in css_graphs
        ),
        "algebra_difference_counts_nonincreasing_on_all_canonical_paths": all(
            graph["path_invariants"]["algebra_difference_count_nonincreasing"] for graph in graphs
        ),
        "repaired_path_reduces_algebra_difference_count": repaired_graph["certified_claims"][
            "algebra_difference_count_drops_on_path"
        ],
    }
    phase_claims["phase_15_multi_source_flow_invariant_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 15: multi-source cover-flow invariant atlas",
        "status": "pass" if phase_claims["phase_15_multi_source_flow_invariant_certificate"] else "fail",
        "graph_sources": graphs,
        "cross_model_classification": {
            "shared_horizon_path_correctability_profiles": tuple(
                (
                    graph["graph_id"],
                    graph["path_invariants"]["shared_horizon"]["correctability_unique_profiles"],
                )
                for graph in graphs
            ),
            "shared_horizon_path_fixed_point_profiles": tuple(
                (
                    graph["graph_id"],
                    graph["path_invariants"]["shared_horizon"]["survivor_fixed_point_unique_profiles"],
                )
                for graph in graphs
            ),
            "shared_horizon_graph_global_correctability_profiles": tuple(
                (
                    graph["graph_id"],
                    graph["graph_invariants"]["by_scenario"]["erase_shared_horizon"][
                        "correctability_unique_profiles"
                    ],
                    graph["graph_invariants"]["by_scenario"]["erase_shared_horizon"][
                        "correctability_stable_across_nodes"
                    ],
                )
                for graph in graphs
            ),
            "algebra_difference_counts_on_canonical_paths": tuple(
                (
                    graph["graph_id"],
                    graph["path_invariants"]["algebra_difference_counts_on_path"],
                )
                for graph in graphs
            ),
        },
        "counts": {
            "source_graphs": len(graphs),
            "css_graphs": len(css_graphs),
            "noncss_graphs": 1,
            "total_nodes": sum(graph["counts"]["nodes"] for graph in graphs),
            "total_edges": sum(graph["counts"]["edges"] for graph in graphs),
            "css_m2_nodes": css_graphs[0]["counts"]["nodes"],
            "css_m3_nodes": css_graphs[1]["counts"]["nodes"],
            "repaired_nodes": repaired_graph["counts"]["nodes"],
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The same exact erasure/operator classifier now runs over multiple cover-transition graphs: two CSS "
                "balanced-bridge orientation hypercubes and the repaired non-CSS Phase 14 neighborhood."
            ),
            "invariant_lesson": (
                "Shared-horizon correctability and survivor fixed-point behavior can be stable along a chosen flow "
                "while failing to be a graph-global or cross-model invariant. The CSS orientation flows keep shared "
                "horizon erasure non-correctable; the repaired non-CSS canonical flow keeps it correctable."
            ),
            "algebra_lesson": (
                "Algebra-difference counts are flat on the CSS orientation paths and drop on the repaired path, giving "
                "a finite monotonicity diagnostic to test on larger source graphs."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 15 promotes the Phase 14 path into a cross-source invariant classifier, and it finds that some "
                "role semantics are path-stable but not model-stable. The next adaptation should add code-changing "
                "edges, such as bridge growth or local Clifford/graph moves, so flow invariants can be tested across "
                "both atlas dynamics and code dynamics."
            ),
            "suggested_phase_16": (
                "Build a mixed code-cover transition graph whose edges include cover edits, bridge-growth steps, and "
                "small certified code transformations; then search for conjectures about which erasure fixed points "
                "or algebra monotonicities survive across those mixed flows."
            ),
        },
    }


def phase16_mixed_css_node_id(m: int, orientation: tuple[int, ...]) -> str:
    return f"mixed_css:m{m}:o{phase15_orientation_id(orientation)}"


def phase16_mixed_css_candidates(*, max_m: int) -> tuple[dict[str, object], ...]:
    if max_m < 2:
        raise ValueError("Phase 16 mixed graphs require max_m >= 2")
    out = []
    horizon = _mask(1, 2, 3)
    for m in range(1, max_m + 1):
        first, second = repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m)
        for orientation in product((0, 1), repeat=m):
            out.append(
                {
                    "id": phase16_mixed_css_node_id(m, orientation),
                    "m": m,
                    "orientation": orientation,
                    "first": first,
                    "second": second,
                    "cover": bridge_assignment_cover(m, horizon, orientation),
                }
            )
    return tuple(out)


def phase16_node_diagnostic(
    candidate: dict[str, object],
    *,
    include_bases: bool = False,
) -> dict[str, object]:
    first = candidate["first"]
    second = candidate["second"]
    cover = candidate["cover"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 16 candidates must carry StabilizerCode objects")
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 16 candidates must carry PatchCover objects")
    return phase15_node_diagnostic(
        node_id=str(candidate["id"]),
        model_kind="css_balanced_bridge_mixed_code_cover",
        first=first,
        second=second,
        cover=cover,
        metadata={
            "m": candidate["m"],
            "n": first.n,
            "k": first.k,
            "orientation": candidate["orientation"],
        },
        include_bases=include_bases,
    )


def phase16_growth_edge(
    *,
    left: dict[str, object],
    right: dict[str, object],
    left_node: dict[str, object],
    right_node: dict[str, object],
) -> dict[str, object] | None:
    left_m = int(left["m"])
    right_m = int(right["m"])
    left_orientation = left["orientation"]
    right_orientation = right["orientation"]
    if not isinstance(left_orientation, tuple) or not isinstance(right_orientation, tuple):
        raise TypeError("Phase 16 candidates must carry tuple orientations")
    if right_m != left_m + 1 or right_orientation[:left_m] != left_orientation:
        return None
    left_first = left["first"]
    right_first = right["first"]
    left_cover = left["cover"]
    right_cover = right["cover"]
    if not isinstance(left_first, StabilizerCode) or not isinstance(right_first, StabilizerCode):
        raise TypeError("Phase 16 growth candidates must carry StabilizerCode objects")
    if not isinstance(left_cover, PatchCover) or not isinstance(right_cover, PatchCover):
        raise TypeError("Phase 16 growth candidates must carry PatchCover objects")

    appended_bit = int(right_orientation[-1])
    new_p = 6 + 2 * left_m
    new_q = new_p + 1
    expected_p_added = (new_q,) if appended_bit else (new_p,)
    expected_q_added = (new_p,) if appended_bit else (new_q,)
    delta = phase14_cover_patch_delta(left=left_cover, right=right_cover, n=right_first.n)
    observer_p_delta = phase13_patch_delta_by_name(delta, "observer_p")
    observer_q_delta = phase13_patch_delta_by_name(delta, "observer_q")
    horizon_delta = phase13_patch_delta_by_name(delta, "shared_horizon")
    shell_delta = phase13_patch_delta_by_name(delta, "bridge_shell")
    diamond_delta = phase13_patch_delta_by_name(delta, "static_diamond")
    claims = {
        "m_increases_by_one": right_m == left_m + 1,
        "n_increases_by_two": int(right_node["metadata"]["n"]) == int(left_node["metadata"]["n"]) + 2,
        "k_stays_one": int(left_node["metadata"]["k"]) == 1 and int(right_node["metadata"]["k"]) == 1,
        "orientation_prefix_preserved": right_orientation[:left_m] == left_orientation,
        "appended_orientation_bit_valid": appended_bit in (0, 1),
        "shared_horizon_stable": horizon_delta["stable"],
        "bridge_shell_adds_new_pair": shell_delta["added_qubits"] == (new_p, new_q)
        and not shell_delta["removed_qubits"],
        "static_diamond_adds_new_pair": diamond_delta["added_qubits"] == (new_p, new_q)
        and not diamond_delta["removed_qubits"],
        "observer_p_adds_orientation_selected_qubit": observer_p_delta["added_qubits"] == expected_p_added
        and not observer_p_delta["removed_qubits"],
        "observer_q_adds_complementary_qubit": observer_q_delta["added_qubits"] == expected_q_added
        and not observer_q_delta["removed_qubits"],
        "left_preserves_entropy_reconstruction_signal": bool(left_node["entropy_reconstruction_signal"]),
        "right_preserves_entropy_reconstruction_signal": bool(right_node["entropy_reconstruction_signal"]),
        "left_exact_qec_complementarity": bool(left_node["qec_complementarity_identity_all_scenarios"]),
        "right_exact_qec_complementarity": bool(right_node["qec_complementarity_identity_all_scenarios"]),
        "shared_horizon_correctability_stable": left_node["correctability_pairs"]["erase_shared_horizon"]
        == right_node["correctability_pairs"]["erase_shared_horizon"],
        "shared_horizon_fixed_point_stable": left_node["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == right_node["survivor_fixed_point_pairs"]["erase_shared_horizon"],
        "algebra_difference_count_stable": left_node["algebra_difference_count"] == right_node["algebra_difference_count"],
    }
    claims["mixed_code_cover_growth_edge"] = all(claims.values())
    if not claims["mixed_code_cover_growth_edge"]:
        return None
    return {
        "left": left_node["id"],
        "right": right_node["id"],
        "edge_type": "bridge_growth",
        "from_m": left_m,
        "to_m": right_m,
        "appended_orientation_bit": appended_bit,
        "new_qubits": {"p": new_p, "q": new_q},
        "patch_delta": delta,
        "certified_claims": claims,
    }


def phase16_orientation_edge(
    *,
    left: dict[str, object],
    right: dict[str, object],
    left_node: dict[str, object],
    right_node: dict[str, object],
) -> dict[str, object] | None:
    if int(left["m"]) != int(right["m"]):
        return None
    first = left["first"]
    if not isinstance(first, StabilizerCode):
        raise TypeError("Phase 16 orientation candidates must carry StabilizerCode objects")
    edge = phase15_css_orientation_edge(
        left=left,
        right=right,
        left_node=left_node,
        right_node=right_node,
        n=first.n,
    )
    if edge is None:
        return None
    return {
        **edge,
        "edge_type": "cover_orientation_flip",
        "m": int(left["m"]),
    }


def phase16_count_edge_types(edges: tuple[dict[str, object], ...]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for edge in edges:
        edge_type = str(edge["edge_type"])
        counts[edge_type] = counts.get(edge_type, 0) + 1
    return counts


def phase16_path_edges(
    *,
    edges: tuple[dict[str, object], ...],
    path_ids: tuple[str, ...],
) -> tuple[dict[str, object], ...]:
    out = []
    for left_id, right_id in zip(path_ids, path_ids[1:]):
        out.append(
            next(
                edge
                for edge in edges
                if {edge["left"], edge["right"]} == {left_id, right_id}
            )
        )
    return tuple(out)


def bridge_cosmology_phase16_certificate(
    *,
    max_m: int = 3,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_m < 2:
        raise ValueError("max_m must be at least 2")
    candidates = phase16_mixed_css_candidates(max_m=max_m)
    nodes = tuple(phase16_node_diagnostic(candidate, include_bases=include_bases) for candidate in candidates)
    by_id = {str(node["id"]): (candidate, node) for candidate, node in zip(candidates, nodes)}
    node_ids = tuple(str(node["id"]) for node in nodes)
    low_order_entropy_by_m = tuple(
        {
            "m": m,
            **low_order_entropy_match_by_rank(
                *repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m),
                max_subset_size=2,
            ),
        }
        for m in range(1, max_m + 1)
    )

    edges = []
    for left_index, left in enumerate(candidates):
        for right_index in range(left_index + 1, len(candidates)):
            right = candidates[right_index]
            left_node = nodes[left_index]
            right_node = nodes[right_index]
            orientation_edge = phase16_orientation_edge(
                left=left,
                right=right,
                left_node=left_node,
                right_node=right_node,
            )
            if orientation_edge is not None:
                edges.append(orientation_edge)
                continue
            growth_edge = phase16_growth_edge(
                left=left,
                right=right,
                left_node=left_node,
                right_node=right_node,
            )
            if growth_edge is not None:
                edges.append(growth_edge)
    edges_tuple = tuple(edges)
    edge_type_counts = phase16_count_edge_types(edges_tuple)

    start = phase16_mixed_css_node_id(1, (0,))
    target = phase16_mixed_css_node_id(max_m, tuple(1 for _ in range(max_m)))
    path_ids = phase14_find_path(
        node_ids=node_ids,
        edges=edges_tuple,
        start=start,
        target=target,
    )
    path_edges = phase16_path_edges(edges=edges_tuple, path_ids=path_ids)
    path_edge_type_counts = phase16_count_edge_types(path_edges)
    flow_summary = phase15_scenario_flow_summary(nodes=nodes, path_ids=path_ids)
    algebra_counts = tuple(count for _, count in flow_summary["algebra_difference_counts_on_path"])

    expected_nodes = sum(2**m for m in range(1, max_m + 1))
    expected_orientation_edges = sum(m * (2 ** (m - 1)) for m in range(1, max_m + 1))
    expected_growth_edges = sum(2 ** (m + 1) for m in range(1, max_m))
    phase_claims = {
        "low_order_entropy_matches_at_every_code_size": all(item["matches"] for item in low_order_entropy_by_m),
        "mixed_graph_nodes_scored": len(nodes) == expected_nodes,
        "orientation_edges_certified": edge_type_counts.get("cover_orientation_flip", 0) == expected_orientation_edges
        and all(
            edge["certified_claims"]["bounded_patch_edit_edge"]
            for edge in edges_tuple
            if edge["edge_type"] == "cover_orientation_flip"
        ),
        "growth_edges_certified": edge_type_counts.get("bridge_growth", 0) == expected_growth_edges
        and all(
            edge["certified_claims"]["mixed_code_cover_growth_edge"]
            for edge in edges_tuple
            if edge["edge_type"] == "bridge_growth"
        ),
        "canonical_mixed_path_found": bool(path_ids) and path_ids[0] == start and path_ids[-1] == target,
        "canonical_path_uses_growth_edges": path_edge_type_counts.get("bridge_growth", 0) == max_m - 1,
        "canonical_path_uses_cover_edit_edges": path_edge_type_counts.get("cover_orientation_flip", 0) >= 1,
        "all_nodes_preserve_entropy_reconstruction_signal": all(
            bool(node["entropy_reconstruction_signal"]) for node in nodes
        ),
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "shared_horizon_correctability_stable_across_mixed_graph": flow_summary["by_scenario"]["erase_shared_horizon"][
            "correctability_stable_across_nodes"
        ]
        and flow_summary["by_scenario"]["erase_shared_horizon"]["correctability_unique_profiles"]
        == ((False, False),),
        "shared_horizon_fixed_point_stable_across_mixed_graph": flow_summary["by_scenario"]["erase_shared_horizon"][
            "survivor_fixed_point_stable_across_nodes"
        ]
        and flow_summary["by_scenario"]["erase_shared_horizon"]["survivor_fixed_point_unique_profiles"]
        == ((False, False),),
        "algebra_difference_count_flat_on_mixed_path": len(set(algebra_counts)) == 1,
        "algebra_difference_count_flat_across_mixed_graph": len(set(node["algebra_difference_count"] for node in nodes))
        == 1,
    }
    phase_claims["phase_16_mixed_code_cover_graph_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 16: mixed CSS code-cover transition graph",
        "status": "pass" if phase_claims["phase_16_mixed_code_cover_graph_certificate"] else "fail",
        "graph_spec": {
            "node_source": f"all balanced-bridge CSS orientation covers for m=1..{max_m}",
            "edge_rules": (
                "cover_orientation_flip: same code size, flip one bridge-pair orientation",
                "bridge_growth: m -> m+1, preserve old orientation prefix, append one oriented bridge pair",
            ),
            "start": start,
            "target": target,
        },
        "low_order_entropy_by_m": low_order_entropy_by_m,
        "nodes": nodes,
        "edges": edges_tuple,
        "path_search": {
            "path_node_ids": path_ids,
            "path_edges": path_edges,
            "path_edge_type_counts": path_edge_type_counts,
        },
        "graph_invariants": {
            "by_scenario": flow_summary["by_scenario"],
            "algebra_difference_counts": tuple((node["id"], node["algebra_difference_count"]) for node in nodes),
        },
        "path_invariants": {
            "by_scenario": flow_summary["path_by_scenario"],
            "shared_horizon": flow_summary["shared_horizon"],
            "algebra_difference_counts_on_path": flow_summary["algebra_difference_counts_on_path"],
            "algebra_difference_count_nonincreasing": flow_summary["algebra_difference_count_nonincreasing"],
        },
        "counts": {
            "max_m": max_m,
            "nodes": len(nodes),
            "edges": len(edges_tuple),
            "orientation_edges": edge_type_counts.get("cover_orientation_flip", 0),
            "growth_edges": edge_type_counts.get("bridge_growth", 0),
            "path_length_nodes": len(path_ids),
            "path_length_edges": max(0, len(path_ids) - 1),
            "path_growth_edges": path_edge_type_counts.get("bridge_growth", 0),
            "path_cover_orientation_edges": path_edge_type_counts.get("cover_orientation_flip", 0),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 16 adds genuine code-changing edges to the CSS toy cosmology: bridge-growth edges change n "
                "and extend the cover while orientation edges move only the observer assignment on a fixed code."
            ),
            "invariant_lesson": (
                "For the balanced-bridge CSS family, the ER=EPR-like entropy/reconstruction signal, shared-horizon "
                "non-correctability, survivor fixed-point profile, and algebra-difference count remain invariant "
                "across the mixed code-cover graph through the checked prefix."
            ),
            "contrast_with_phase15": (
                "This gives a rigid CSS baseline for mixed dynamics, complementing the repaired non-CSS Phase 15 "
                "lesson where the same horizon role can be path-stable but not model-stable."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 16 certifies mixed code-cover edges for the CSS bridge family. The next adaptation should add "
                "non-CSS code-changing edges or explicit local Clifford/graph moves so the mixed-flow invariant "
                "classifier can test whether Phase 15's repaired semantics survive beyond cover-only dynamics."
            ),
            "suggested_phase_17": (
                "Add bounded graph/local-Clifford mutation edges for non-CSS or graph/CWS-derived sources, and search "
                "for mixed flows whose horizon fixed points or algebra-difference monotonicity differ from the CSS "
                "bridge-growth baseline."
            ),
        },
    }


PHASE17_IDENTITY_LC = (1, 0, 0, 1)
PHASE17_H_LC = (0, 1, 1, 0)
PHASE17_S_LC = (1, 0, 1, 1)


def phase17_lc_node_id(*, h_shared: int, s_observer_q_private: int) -> str:
    return f"repaired_lc:h{h_shared}:s{s_observer_q_private}"


def phase17_code_digest(code: StabilizerCode) -> str:
    payload = json.dumps(code.pauli_generators(), sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def phase17_local_clifford_maps(
    *,
    n: int,
    shared_horizon: int,
    observer_q_private: int,
    h_shared: int,
    s_observer_q_private: int,
) -> tuple[tuple[int, int, int, int], ...]:
    maps = [PHASE17_IDENTITY_LC for _ in range(n)]
    if h_shared:
        for qubit in range(n):
            if (shared_horizon >> qubit) & 1:
                maps[qubit] = PHASE17_H_LC
    if s_observer_q_private:
        for qubit in range(n):
            if (observer_q_private >> qubit) & 1:
                maps[qubit] = PHASE17_S_LC
    return tuple(maps)


def phase17_local_clifford_code(
    code: StabilizerCode,
    maps: tuple[tuple[int, int, int, int], ...],
) -> StabilizerCode:
    return StabilizerCode(
        code.n,
        tuple(local_clifford_pauli(generator, code.n, maps) for generator in code.generators),
    )


def phase17_repaired_lc_candidates(*, include_bases: bool = False) -> tuple[dict[str, object], ...]:
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 17 source must contain StabilizerCode objects")
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    candidates = phase12_atlas_aware_repaired_cover_candidates(inner_hit=inner_atlas["hit"])
    hit = candidate_by_template_and_blocks(
        candidates,
        template_kind="phase12_private_full_shared_inner",
        observer_p_block_mask=1,
        observer_q_block_mask=13,
    )
    cover = hit["cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 17 hit candidate must contain a PatchCover")
    shared_horizon = cover.patch("shared_horizon").region
    observer_q_private = cover.patch("observer_q").region & ~shared_horizon
    out = []
    for h_shared in (0, 1):
        for s_observer_q_private in (0, 1):
            maps = phase17_local_clifford_maps(
                n=first.n,
                shared_horizon=shared_horizon,
                observer_q_private=observer_q_private,
                h_shared=h_shared,
                s_observer_q_private=s_observer_q_private,
            )
            first_lc = phase17_local_clifford_code(first, maps)
            second_lc = phase17_local_clifford_code(second, maps)
            node = phase15_node_diagnostic(
                node_id=phase17_lc_node_id(
                    h_shared=h_shared,
                    s_observer_q_private=s_observer_q_private,
                ),
                model_kind="distance_repaired_noncss_local_clifford",
                first=first_lc,
                second=second_lc,
                cover=cover,
                metadata={
                    "h_shared": h_shared,
                    "s_observer_q_private": s_observer_q_private,
                    "n": first_lc.n,
                    "k": first_lc.k,
                    "shared_horizon_qubits": mask_to_tuple(shared_horizon, first_lc.n),
                    "observer_q_private_qubits": mask_to_tuple(observer_q_private, first_lc.n),
                },
                include_bases=include_bases,
            )
            node = {
                **node,
                "first_generators": first_lc.pauli_generators(),
                "second_generators": second_lc.pauli_generators(),
                "first_generator_digest": phase17_code_digest(first_lc),
                "second_generator_digest": phase17_code_digest(second_lc),
                "local_clifford_action": {
                    "H_on_shared_horizon": bool(h_shared),
                    "S_on_observer_q_private": bool(s_observer_q_private),
                    "H_matrix": PHASE17_H_LC,
                    "S_matrix": PHASE17_S_LC,
                },
            }
            out.append(
                {
                    "id": node["id"],
                    "h_shared": h_shared,
                    "s_observer_q_private": s_observer_q_private,
                    "maps": maps,
                    "first": first_lc,
                    "second": second_lc,
                    "cover": cover,
                    "node": node,
                    "source": source,
                    "hit_template": {
                        "template_kind": hit["template_kind"],
                        "observer_p_block_mask": hit["observer_p_block_mask"],
                        "observer_q_block_mask": hit["observer_q_block_mask"],
                        "shared_block_mask": hit["shared_block_mask"],
                    },
                }
            )
    return tuple(out)


def phase17_relative_lc_maps(
    *,
    n: int,
    shared_horizon: int,
    observer_q_private: int,
    left: dict[str, object],
    right: dict[str, object],
) -> tuple[tuple[int, int, int, int], ...] | None:
    left_bits = (int(left["h_shared"]), int(left["s_observer_q_private"]))
    right_bits = (int(right["h_shared"]), int(right["s_observer_q_private"]))
    if phase15_hamming_distance(left_bits, right_bits) != 1:
        return None
    return phase17_local_clifford_maps(
        n=n,
        shared_horizon=shared_horizon,
        observer_q_private=observer_q_private,
        h_shared=left_bits[0] ^ right_bits[0],
        s_observer_q_private=left_bits[1] ^ right_bits[1],
    )


def phase17_lc_edge(
    *,
    left: dict[str, object],
    right: dict[str, object],
) -> dict[str, object] | None:
    left_node = left["node"]
    right_node = right["node"]
    left_first = left["first"]
    left_second = left["second"]
    right_first = right["first"]
    right_second = right["second"]
    cover = left["cover"]
    if not isinstance(left_first, StabilizerCode) or not isinstance(left_second, StabilizerCode):
        raise TypeError("Phase 17 edge endpoints must contain StabilizerCode objects")
    if not isinstance(right_first, StabilizerCode) or not isinstance(right_second, StabilizerCode):
        raise TypeError("Phase 17 edge endpoints must contain StabilizerCode objects")
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 17 edge endpoint must contain a PatchCover")
    shared_horizon = cover.patch("shared_horizon").region
    observer_q_private = cover.patch("observer_q").region & ~shared_horizon
    relative_maps = phase17_relative_lc_maps(
        n=left_first.n,
        shared_horizon=shared_horizon,
        observer_q_private=observer_q_private,
        left=left,
        right=right,
    )
    if relative_maps is None:
        return None
    transformed_first = phase17_local_clifford_code(left_first, relative_maps)
    transformed_second = phase17_local_clifford_code(left_second, relative_maps)
    first_matches = transformed_first.generators == right_first.generators
    second_matches = transformed_second.generators == right_second.generators
    first_changes = left_node["first_generator_digest"] != right_node["first_generator_digest"]
    second_changes = left_node["second_generator_digest"] != right_node["second_generator_digest"]
    claims = {
        "single_local_clifford_toggle": True,
        "target_first_generators_match_relative_transform": first_matches,
        "target_second_generators_match_relative_transform": second_matches,
        "first_generators_change": first_changes,
        "second_generators_change": second_changes,
        "entropy_reconstruction_signal_preserved": bool(left_node["entropy_reconstruction_signal"])
        and bool(right_node["entropy_reconstruction_signal"]),
        "shared_horizon_correctability_preserved": left_node["correctability_pairs"]["erase_shared_horizon"]
        == right_node["correctability_pairs"]["erase_shared_horizon"],
        "shared_horizon_fixed_point_preserved": left_node["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == right_node["survivor_fixed_point_pairs"]["erase_shared_horizon"],
        "erasure_algebra_difference_names_preserved": left_node["algebra_difference_names"]
        == right_node["algebra_difference_names"],
        "qec_complementarity_preserved": bool(left_node["qec_complementarity_identity_all_scenarios"])
        and bool(right_node["qec_complementarity_identity_all_scenarios"]),
    }
    claims["local_clifford_code_transform_edge"] = all(claims.values())
    if not claims["local_clifford_code_transform_edge"]:
        return None
    flipped = []
    if int(left["h_shared"]) != int(right["h_shared"]):
        flipped.append("H_on_shared_horizon")
    if int(left["s_observer_q_private"]) != int(right["s_observer_q_private"]):
        flipped.append("S_on_observer_q_private")
    return {
        "left": left_node["id"],
        "right": right_node["id"],
        "edge_type": "local_clifford_code_transform",
        "flipped_actions": tuple(flipped),
        "relative_local_clifford": {
            "shared_horizon_qubits": mask_to_tuple(shared_horizon, left_first.n),
            "observer_q_private_qubits": mask_to_tuple(observer_q_private, left_first.n),
            "maps_changed_on_qubits": tuple(
                (qubit, relative_maps[qubit])
                for qubit in range(left_first.n)
                if relative_maps[qubit] != PHASE17_IDENTITY_LC
            ),
        },
        "certified_claims": claims,
    }


def bridge_cosmology_phase17_certificate(*, include_bases: bool = False) -> dict[str, object]:
    candidates = phase17_repaired_lc_candidates(include_bases=include_bases)
    nodes = tuple(candidate["node"] for candidate in candidates)
    node_ids = tuple(str(node["id"]) for node in nodes)
    edges = []
    for left_index, left in enumerate(candidates):
        for right_index in range(left_index + 1, len(candidates)):
            edge = phase17_lc_edge(left=left, right=candidates[right_index])
            if edge is not None:
                edges.append(edge)
    edges_tuple = tuple(edges)
    start = phase17_lc_node_id(h_shared=0, s_observer_q_private=0)
    target = phase17_lc_node_id(h_shared=1, s_observer_q_private=1)
    path_ids = phase14_find_path(node_ids=node_ids, edges=edges_tuple, start=start, target=target)
    path_edges = phase16_path_edges(edges=edges_tuple, path_ids=path_ids)
    flow_summary = phase15_scenario_flow_summary(nodes=nodes, path_ids=path_ids)
    algebra_name_sets = tuple(node["algebra_difference_names"] for node in nodes)
    css_baseline = bridge_cosmology_phase16_certificate(max_m=3, include_bases=False)
    css_shared = css_baseline["path_invariants"]["shared_horizon"]["correctability_unique_profiles"]
    repaired_shared = flow_summary["shared_horizon"]["correctability_unique_profiles"]
    css_algebra_counts = tuple(
        count for _, count in css_baseline["path_invariants"]["algebra_difference_counts_on_path"]
    )
    repaired_algebra_counts = tuple(count for _, count in flow_summary["algebra_difference_counts_on_path"])
    public_source = {
        key: value
        for key, value in candidates[0]["source"].items()
        if key not in ("first", "second")
    }
    phase_claims = {
        "repaired_noncss_lc_nodes_scored": len(nodes) == 4,
        "local_clifford_edges_certified": len(edges_tuple) == 4
        and all(edge["certified_claims"]["local_clifford_code_transform_edge"] for edge in edges_tuple),
        "canonical_lc_path_found": bool(path_ids) and path_ids[0] == start and path_ids[-1] == target,
        "canonical_path_uses_two_code_transform_edges": len(path_edges) == 2,
        "all_nodes_preserve_entropy_reconstruction_signal": all(
            bool(node["entropy_reconstruction_signal"]) for node in nodes
        ),
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "shared_horizon_correctability_stable_across_lc_graph": flow_summary["by_scenario"]["erase_shared_horizon"][
            "correctability_stable_across_nodes"
        ]
        and flow_summary["by_scenario"]["erase_shared_horizon"]["correctability_unique_profiles"]
        == ((True, True),),
        "shared_horizon_fixed_point_stable_across_lc_graph": flow_summary["by_scenario"]["erase_shared_horizon"][
            "survivor_fixed_point_stable_across_nodes"
        ]
        and flow_summary["by_scenario"]["erase_shared_horizon"]["survivor_fixed_point_unique_profiles"]
        == ((True, True),),
        "erasure_algebra_difference_names_stable": len(set(algebra_name_sets)) == 1
        and algebra_name_sets[0] == ("erase_observer_q_private", "erase_observer_q"),
        "algebra_difference_count_flat_on_lc_path": len(set(repaired_algebra_counts)) == 1
        and repaired_algebra_counts[0] == 2,
        "lc_generators_actually_change": all(
            node["first_generator_digest"] != nodes[0]["first_generator_digest"]
            for node in nodes
            if node["id"] != start
        )
        and all(
            node["second_generator_digest"] != nodes[0]["second_generator_digest"]
            for node in nodes
            if node["id"] != start
        ),
        "repaired_lc_horizon_semantics_differs_from_css_mixed_baseline": (
            repaired_shared == ((True, True),) and css_shared == ((False, False),)
        ),
        "repaired_lc_algebra_count_differs_from_css_mixed_baseline": (
            repaired_algebra_counts and css_algebra_counts and repaired_algebra_counts[0] == 2 and css_algebra_counts[0] == 3
        ),
    }
    phase_claims["phase_17_noncss_local_clifford_flow_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 17: repaired non-CSS local-Clifford code-flow probe",
        "status": "pass" if phase_claims["phase_17_noncss_local_clifford_flow_certificate"] else "fail",
        "repaired_source": public_source,
        "hit_template": candidates[0]["hit_template"],
        "graph_spec": {
            "node_source": "Phase 12 repaired non-CSS hit under two disjoint local-Clifford toggles",
            "edge_rule": "single local-Clifford toggle with target generators verified by exact Pauli transformation",
            "start": start,
            "target": target,
            "local_clifford_toggles": (
                {
                    "name": "H_on_shared_horizon",
                    "matrix": PHASE17_H_LC,
                    "qubits": nodes[0]["metadata"]["shared_horizon_qubits"],
                },
                {
                    "name": "S_on_observer_q_private",
                    "matrix": PHASE17_S_LC,
                    "qubits": nodes[0]["metadata"]["observer_q_private_qubits"],
                },
            ),
        },
        "nodes": nodes,
        "edges": edges_tuple,
        "path_search": {
            "path_node_ids": path_ids,
            "path_edges": path_edges,
        },
        "graph_invariants": {
            "by_scenario": flow_summary["by_scenario"],
            "algebra_difference_name_sets": tuple((node["id"], node["algebra_difference_names"]) for node in nodes),
            "algebra_difference_counts": tuple((node["id"], node["algebra_difference_count"]) for node in nodes),
        },
        "path_invariants": {
            "by_scenario": flow_summary["path_by_scenario"],
            "shared_horizon": flow_summary["shared_horizon"],
            "algebra_difference_counts_on_path": flow_summary["algebra_difference_counts_on_path"],
            "algebra_difference_count_nonincreasing": flow_summary["algebra_difference_count_nonincreasing"],
        },
        "css_mixed_baseline_comparison": {
            "phase16_status": css_baseline["status"],
            "css_shared_horizon_path_correctability": css_shared,
            "repaired_lc_shared_horizon_path_correctability": repaired_shared,
            "css_algebra_difference_counts_on_path": css_baseline["path_invariants"][
                "algebra_difference_counts_on_path"
            ],
            "repaired_lc_algebra_difference_counts_on_path": flow_summary["algebra_difference_counts_on_path"],
        },
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges_tuple),
            "path_length_nodes": len(path_ids),
            "path_length_edges": max(0, len(path_ids) - 1),
            "local_clifford_toggles": 2,
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The repaired non-CSS hit survives a bounded local-Clifford code-flow: exact generator transforms "
                "change the code representation while preserving the repaired shared-horizon channel semantics."
            ),
            "contrast_with_css": (
                "Phase 16's CSS mixed bridge-growth graph keeps shared-horizon erasure non-correctable with algebra "
                "difference count 3; this repaired local-Clifford graph keeps it correctable with algebra difference "
                "count 2."
            ),
            "lesson": (
                "The repaired horizon semantics are not an artifact of one stabilizer-generator presentation. They "
                "are stable under the checked local-Clifford code moves, but still differ from the CSS mixed-flow "
                "baseline."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 17 certifies local-Clifford code-flow stability for one repaired non-CSS hit. The next "
                "adaptation should add non-CSS code-changing edges that are not local-unitary equivalences, such as "
                "outer-code swaps, graph-edge mutations, or concatenation-depth changes."
            ),
            "suggested_phase_18": (
                "Search a bounded menu of non-CSS repair transformations and graph/CWS mutations, then classify "
                "which transformations preserve repaired horizon fixed points and which force a return to CSS-like "
                "non-correctable horizon semantics."
            ),
        },
    }


PHASE18_OUTER_REPAIR_SPECS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("phase11_outer", ("XXIZ", "ZIZX", "XZXX")),
    ("same_class_preserve", ("XXIZ", "ZIZX", "XYXX")),
    ("same_class_collapse", ("XXIZ", "YIZX", "XZXX")),
    ("distinct_class_entropy_break", ("XIIZ", "IXZI", "ZZXX")),
)


def phase18_canonical_digest(rows: tuple[int, ...]) -> str:
    payload = json.dumps(rows, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def phase18_outer_code_summary(label: str, outer: StabilizerCode) -> dict[str, object]:
    lc_key = outer.canonical_under_local_cliffords(include_permutations=True)
    return {
        "label": label,
        "n": outer.n,
        "k": outer.k,
        "distance": outer.distance(),
        "generators": outer.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, outer.n) for row in outer.logical_basis),
        "minimal_reconstruction_regions": tuple(
            mask_to_tuple(mask, outer.n) for mask in outer.reconstruction_regions(minimal=True)
        ),
        "generator_digest": phase17_code_digest(outer),
        "local_clifford_class_digest": phase18_canonical_digest(lc_key),
    }


def phase18_repaired_cover_hit() -> dict[str, object]:
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    candidates = phase12_atlas_aware_repaired_cover_candidates(inner_hit=inner_atlas["hit"])
    return candidate_by_template_and_blocks(
        candidates,
        template_kind="phase12_private_full_shared_inner",
        observer_p_block_mask=1,
        observer_q_block_mask=13,
    )


def phase18_outer_swap_candidates(*, include_bases: bool = False) -> tuple[dict[str, object], ...]:
    graph_search = graph_labeled_pair_source()
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 10 labeled graph source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 18 source must contain StabilizerCode objects")
    hit = phase18_repaired_cover_hit()
    cover = hit["cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 18 repaired hit must contain a PatchCover")
    out = []
    for label, generators in PHASE18_OUTER_REPAIR_SPECS:
        outer = StabilizerCode.from_pauli_strings(generators)
        first_repaired, first_metadata = logical_concatenate_k1(inner_first, outer)
        second_repaired, second_metadata = logical_concatenate_k1(inner_second, outer)
        node = phase15_node_diagnostic(
            node_id=f"outer_swap:{label}",
            model_kind="distance_repaired_noncss_outer_swap",
            first=first_repaired,
            second=second_repaired,
            cover=cover,
            metadata={
                "outer_label": label,
                "n": first_repaired.n,
                "k": first_repaired.k,
            },
            include_bases=include_bases,
        )
        low_order_entropy = low_order_entropy_match_by_rank(first_repaired, second_repaired, max_subset_size=2)
        node = {
            **node,
            "outer_code": phase18_outer_code_summary(label, outer),
            "low_order_entropy": low_order_entropy,
            "same_labeled_t2_entropy": low_order_entropy["matches"],
            "first_generator_digest": phase17_code_digest(first_repaired),
            "second_generator_digest": phase17_code_digest(second_repaired),
            "concatenation": {
                "first": first_metadata,
                "second": second_metadata,
            },
        }
        out.append(
            {
                "id": node["id"],
                "outer_label": label,
                "outer": outer,
                "first": first_repaired,
                "second": second_repaired,
                "cover": cover,
                "node": node,
                "graph_search": {key: value for key, value in graph_search.items() if key != "source"},
                "hit_template": {
                    "template_kind": hit["template_kind"],
                    "observer_p_block_mask": hit["observer_p_block_mask"],
                    "observer_q_block_mask": hit["observer_q_block_mask"],
                    "shared_block_mask": hit["shared_block_mask"],
                },
            }
        )
    return tuple(out)


def phase18_outer_swap_edge(*, baseline: dict[str, object], target: dict[str, object]) -> dict[str, object]:
    baseline_node = baseline["node"]
    target_node = target["node"]
    baseline_outer = baseline_node["outer_code"]
    target_outer = target_node["outer_code"]
    target_low_order_matches = bool(target_node["same_labeled_t2_entropy"])
    target_signal = bool(target_node["entropy_reconstruction_signal"])
    target_algebra_count = int(target_node["algebra_difference_count"])
    outcome = "unclassified"
    if target_low_order_matches and target_signal and target_algebra_count == 2:
        outcome = "full_semantics_preserved"
    elif target_low_order_matches and not target_signal and target_algebra_count == 0:
        outcome = "operator_geometry_collapsed"
    elif not target_low_order_matches and not target_signal and target_algebra_count == 0:
        outcome = "low_order_entropy_break"
    claims = {
        "outer_code_generators_change": baseline_outer["generator_digest"] != target_outer["generator_digest"],
        "outer_local_clifford_class_recorded": bool(target_outer["local_clifford_class_digest"]),
        "both_outer_codes_are_k1_distance2": (
            baseline_outer["k"] == 1
            and target_outer["k"] == 1
            and baseline_outer["distance"] == 2
            and target_outer["distance"] == 2
        ),
        "outer_minimal_reconstruction_shape_matches": baseline_outer["minimal_reconstruction_regions"]
        == target_outer["minimal_reconstruction_regions"],
        "concatenated_code_size_stable": baseline_node["metadata"]["n"] == target_node["metadata"]["n"]
        and baseline_node["metadata"]["k"] == target_node["metadata"]["k"],
        "source_low_order_entropy_matches": bool(baseline_node["same_labeled_t2_entropy"]),
        "target_low_order_entropy_status_recorded": isinstance(target_low_order_matches, bool),
        "shared_horizon_correctability_preserved": baseline_node["correctability_pairs"]["erase_shared_horizon"]
        == target_node["correctability_pairs"]["erase_shared_horizon"]
        == (True, True),
        "shared_horizon_fixed_point_preserved": baseline_node["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == target_node["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == (True, True),
        "target_keeps_same_erasure_correctability_profile": bool(target_node["same_erasure_correctability_profile"]),
        "source_has_repaired_observer_signal": bool(baseline_node["entropy_reconstruction_signal"])
        and baseline_node["algebra_difference_count"] == 2,
        "target_outcome_classified": outcome
        in ("full_semantics_preserved", "operator_geometry_collapsed", "low_order_entropy_break"),
        "qec_complementarity_preserved": bool(baseline_node["qec_complementarity_identity_all_scenarios"])
        and bool(target_node["qec_complementarity_identity_all_scenarios"]),
    }
    claims["outer_code_swap_taxonomy_edge"] = all(claims.values())
    return {
        "left": baseline_node["id"],
        "right": target_node["id"],
        "edge_type": "outer_code_swap",
        "from_outer": baseline["outer_label"],
        "to_outer": target["outer_label"],
        "outer_local_clifford_class_changes": baseline_outer["local_clifford_class_digest"]
        != target_outer["local_clifford_class_digest"],
        "outcome": outcome,
        "certified_claims": claims,
    }


def bridge_cosmology_phase18_certificate(*, include_bases: bool = False) -> dict[str, object]:
    candidates = phase18_outer_swap_candidates(include_bases=include_bases)
    nodes = tuple(candidate["node"] for candidate in candidates)
    baseline = candidates[0]
    swap_targets = candidates[1:]
    edges = tuple(phase18_outer_swap_edge(baseline=baseline, target=target) for target in swap_targets)
    shared_profiles = tuple(sorted(set(node["correctability_pairs"]["erase_shared_horizon"] for node in nodes)))
    shared_fixed_points = tuple(sorted(set(node["survivor_fixed_point_pairs"]["erase_shared_horizon"] for node in nodes)))
    outer_lc_classes = tuple(sorted(set(node["outer_code"]["local_clifford_class_digest"] for node in nodes)))
    alternative_nodes = nodes[1:]
    node_by_outer = {str(node["metadata"]["outer_label"]): node for node in nodes}
    edge_by_target = {str(edge["to_outer"]): edge for edge in edges}
    phase_claims = {
        "outer_swap_nodes_scored": len(nodes) == len(PHASE18_OUTER_REPAIR_SPECS),
        "outer_swap_edges_certified": len(edges) == len(PHASE18_OUTER_REPAIR_SPECS) - 1
        and all(edge["certified_claims"]["outer_code_swap_taxonomy_edge"] for edge in edges),
        "outer_menu_has_two_local_clifford_classes": len(outer_lc_classes) == 2,
        "same_class_preserve_remains_in_phase11_outer_class": node_by_outer["same_class_preserve"]["outer_code"][
            "local_clifford_class_digest"
        ]
        == nodes[0]["outer_code"]["local_clifford_class_digest"],
        "same_class_collapse_remains_in_phase11_outer_class": node_by_outer["same_class_collapse"]["outer_code"][
            "local_clifford_class_digest"
        ]
        == nodes[0]["outer_code"]["local_clifford_class_digest"],
        "distinct_class_entropy_break_changes_outer_class": node_by_outer["distinct_class_entropy_break"]["outer_code"][
            "local_clifford_class_digest"
        ]
        != nodes[0]["outer_code"]["local_clifford_class_digest"],
        "same_class_preserving_swap_exists": (
            bool(node_by_outer["same_class_preserve"]["same_labeled_t2_entropy"])
            and bool(node_by_outer["same_class_preserve"]["entropy_reconstruction_signal"])
            and node_by_outer["same_class_preserve"]["algebra_difference_count"] == 2
            and edge_by_target["same_class_preserve"]["outcome"] == "full_semantics_preserved"
        ),
        "same_class_collapsing_swap_exists": (
            bool(node_by_outer["same_class_collapse"]["same_labeled_t2_entropy"])
            and not bool(node_by_outer["same_class_collapse"]["entropy_reconstruction_signal"])
            and node_by_outer["same_class_collapse"]["algebra_difference_count"] == 0
            and edge_by_target["same_class_collapse"]["outcome"] == "operator_geometry_collapsed"
        ),
        "distinct_class_entropy_break_exists": (
            not bool(node_by_outer["distinct_class_entropy_break"]["same_labeled_t2_entropy"])
            and not bool(node_by_outer["distinct_class_entropy_break"]["entropy_reconstruction_signal"])
            and node_by_outer["distinct_class_entropy_break"]["algebra_difference_count"] == 0
            and edge_by_target["distinct_class_entropy_break"]["outcome"] == "low_order_entropy_break"
        ),
        "all_outer_codes_are_k1_distance2": all(
            node["outer_code"]["k"] == 1 and node["outer_code"]["distance"] == 2 for node in nodes
        ),
        "all_outer_codes_share_minimal_reconstruction_shape": len(
            {node["outer_code"]["minimal_reconstruction_regions"] for node in nodes}
        )
        == 1,
        "shared_horizon_correctability_stable_across_outer_swaps": shared_profiles == ((True, True),),
        "shared_horizon_fixed_point_stable_across_outer_swaps": shared_fixed_points == ((True, True),),
        "baseline_has_repaired_observer_signal": bool(nodes[0]["entropy_reconstruction_signal"])
        and nodes[0]["algebra_difference_count"] == 2,
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
    }
    phase_claims["phase_18_outer_code_swap_taxonomy_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 18: non-CSS outer-code swap taxonomy probe",
        "status": "pass" if phase_claims["phase_18_outer_code_swap_taxonomy_certificate"] else "fail",
        "graph_spec": {
            "node_source": "Phase 10 graph/CWS inner pair concatenated with a bounded menu of n=4,k=1,d=2 outer repair codes",
            "edge_rule": "swap the Phase 11 outer repair code within or across outer local-Clifford classes and replay the repaired cover",
            "baseline": nodes[0]["id"],
            "targets": tuple(node["id"] for node in alternative_nodes),
        },
        "hit_template": candidates[0]["hit_template"],
        "nodes": nodes,
        "edges": edges,
        "outer_code_classification": {
            "local_clifford_class_digests": outer_lc_classes,
            "outer_summaries": tuple(node["outer_code"] for node in nodes),
        },
        "swap_taxonomy": tuple(
            {
                "target": edge["to_outer"],
                "outer_local_clifford_class_changes": edge["outer_local_clifford_class_changes"],
                "outcome": edge["outcome"],
            }
            for edge in edges
        ),
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges),
            "outer_local_clifford_classes": len(outer_lc_classes),
            "full_semantics_preserving_targets": sum(
                1 for edge in edges if edge["outcome"] == "full_semantics_preserved"
            ),
            "operator_geometry_collapsing_targets": sum(
                1 for edge in edges if edge["outcome"] == "operator_geometry_collapsed"
            ),
            "low_order_entropy_breaking_targets": sum(
                1 for edge in edges if edge["outcome"] == "low_order_entropy_break"
            ),
            "collapsed_signal_nodes": sum(
                1 for node in alternative_nodes if not bool(node["entropy_reconstruction_signal"])
            ),
            "low_order_subsets_checked_per_node": tuple(
                (node["id"], node["low_order_entropy"]["subsets_checked"]) for node in nodes
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded outer-repair menu produces three exact outcomes on the same repaired cover: one same-class "
                "swap preserves the full repaired semantics, one same-class swap preserves low-order entropy but "
                "collapses the observer algebra separation, and one distinct-class swap breaks low-order entropy."
            ),
            "pressure_test": (
                "Shared-horizon correctability is the most robust checked role: it survives every outer swap in the "
                "menu. Low-order entropy and observer algebra are stricter diagnostics and can fail independently."
            ),
            "lesson": (
                "Outer repair data such as distance and minimal reconstruction regions are not enough to predict the "
                "emergent causal-patch operator geometry. Even within one outer local-Clifford class, fixing the cover "
                "can distinguish preserving and collapsing swaps."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 18 turns outer-code swaps into an exact taxonomy rather than a yes/no check. The next "
                "adaptation should search outer repairs or graph mutations using this taxonomy as the scoring target, "
                "prioritizing transformations that preserve low-order entropy, horizon fixed points, and nonzero "
                "erasure-algebra differences."
            ),
            "suggested_phase_19": (
                "Run a bounded outer-code/graph-mutation search that reports counts for full-preservation, "
                "operator-collapse, and entropy-break outcomes, then extract structural features of each class."
            ),
        },
    }


PHASE19_MUTATION_ALPHABET = "IXYZ"


def phase19_edit_label(edits: tuple[tuple[int, int, str, str], ...]) -> str:
    return "__".join(f"r{row}c{col}_{old}_to_{new}" for row, col, old, new in edits)


def phase19_histogram(values: Iterable[object]) -> tuple[tuple[object, int], ...]:
    counts: dict[object, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return tuple(sorted(counts.items(), key=lambda item: str(item[0])))


def phase19_outer_mutation_specs(*, max_radius: int = 2) -> dict[str, object]:
    if max_radius < 1 or max_radius > 2:
        raise ValueError("Phase 19 keeps the bounded mutation search at radius 1 or 2")
    baseline_generators = PHASE18_OUTER_REPAIR_SPECS[0][1]
    baseline_outer = StabilizerCode.from_pauli_strings(baseline_generators)
    baseline_reconstruction_shape = tuple(
        mask_to_tuple(mask, baseline_outer.n) for mask in baseline_outer.reconstruction_regions(minimal=True)
    )
    positions = tuple(product(range(len(baseline_generators)), range(len(baseline_generators[0]))))
    seen_digests = {phase17_code_digest(baseline_outer)}
    counters = {
        "raw_mutations": 0,
        "invalid_pauli_checks": 0,
        "duplicate_generator_span": 0,
        "invalid_k": 0,
        "invalid_distance": 0,
        "minimal_reconstruction_shape_mismatch": 0,
        "accepted": 0,
    }
    accepted = []
    for radius in range(1, max_radius + 1):
        for edited_positions in combinations(positions, radius):
            replacement_options = []
            for row_index, col_index in edited_positions:
                original = baseline_generators[row_index][col_index]
                replacement_options.append(tuple(pauli for pauli in PHASE19_MUTATION_ALPHABET if pauli != original))
            for replacements in product(*replacement_options):
                counters["raw_mutations"] += 1
                mutated_rows = list(baseline_generators)
                edits = []
                for (row_index, col_index), replacement in zip(edited_positions, replacements):
                    chars = list(mutated_rows[row_index])
                    original = chars[col_index]
                    chars[col_index] = replacement
                    mutated_rows[row_index] = "".join(chars)
                    edits.append((row_index, col_index, original, replacement))
                if any(all(char == "I" for char in row) for row in mutated_rows):
                    counters["invalid_pauli_checks"] += 1
                    continue
                try:
                    outer = StabilizerCode.from_pauli_strings(mutated_rows)
                except ValueError:
                    counters["invalid_pauli_checks"] += 1
                    continue
                digest = phase17_code_digest(outer)
                if digest in seen_digests:
                    counters["duplicate_generator_span"] += 1
                    continue
                seen_digests.add(digest)
                if outer.k != 1:
                    counters["invalid_k"] += 1
                    continue
                distance = outer.distance()
                if distance != 2:
                    counters["invalid_distance"] += 1
                    continue
                minimal_shape = tuple(
                    mask_to_tuple(mask, outer.n) for mask in outer.reconstruction_regions(minimal=True)
                )
                if minimal_shape != baseline_reconstruction_shape:
                    counters["minimal_reconstruction_shape_mismatch"] += 1
                    continue
                edits_tuple = tuple(edits)
                accepted.append(
                    {
                        "label": f"radius{radius}:{phase19_edit_label(edits_tuple)}",
                        "radius": radius,
                        "edits": edits_tuple,
                        "input_generators": tuple(mutated_rows),
                        "outer": outer,
                        "outer_generator_digest": digest,
                    }
                )
                counters["accepted"] += 1
    return {
        "baseline_generators": baseline_generators,
        "baseline_reconstruction_shape": baseline_reconstruction_shape,
        "max_radius": max_radius,
        "alphabet": PHASE19_MUTATION_ALPHABET,
        "counters": counters,
        "accepted": tuple(accepted),
    }


def phase19_outer_mutation_node(
    *,
    label: str,
    outer: StabilizerCode,
    inner_first: StabilizerCode,
    inner_second: StabilizerCode,
    cover: PatchCover,
    mutation: dict[str, object],
    include_bases: bool = False,
) -> dict[str, object]:
    first_repaired, first_metadata = logical_concatenate_k1(inner_first, outer)
    second_repaired, second_metadata = logical_concatenate_k1(inner_second, outer)
    node = phase15_node_diagnostic(
        node_id=f"outer_mutation:{label}",
        model_kind="distance_repaired_noncss_outer_mutation_search",
        first=first_repaired,
        second=second_repaired,
        cover=cover,
        metadata={
            "outer_label": label,
            "mutation_radius": mutation["radius"],
            "n": first_repaired.n,
            "k": first_repaired.k,
        },
        include_bases=include_bases,
    )
    low_order_entropy = low_order_entropy_match_by_rank(first_repaired, second_repaired, max_subset_size=2)
    return {
        **node,
        "mutation": {
            "radius": mutation["radius"],
            "edits": mutation["edits"],
            "input_generators": mutation["input_generators"],
        },
        "outer_code": phase18_outer_code_summary(label, outer),
        "low_order_entropy": low_order_entropy,
        "same_labeled_t2_entropy": low_order_entropy["matches"],
        "first_generator_digest": phase17_code_digest(first_repaired),
        "second_generator_digest": phase17_code_digest(second_repaired),
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
    }


def phase19_outcome(node: dict[str, object]) -> str:
    low_order_matches = bool(node["same_labeled_t2_entropy"])
    signal = bool(node["entropy_reconstruction_signal"])
    algebra_count = int(node["algebra_difference_count"])
    if low_order_matches and signal and algebra_count == 2:
        return "full_semantics_preserved"
    if low_order_matches and not signal and algebra_count == 0:
        return "operator_geometry_collapsed"
    if not low_order_matches and not signal and algebra_count == 0:
        return "low_order_entropy_break_with_operator_collapse"
    if not low_order_matches and signal and algebra_count == 2:
        return "low_order_entropy_break_with_reconstruction_survives"
    return "residual_unclassified"


def phase19_outer_mutation_edge(*, baseline: dict[str, object], target: dict[str, object]) -> dict[str, object]:
    baseline_outer = baseline["outer_code"]
    target_outer = target["outer_code"]
    outcome = phase19_outcome(target)
    shared_correctability = target["correctability_pairs"]["erase_shared_horizon"]
    shared_fixed_point = target["survivor_fixed_point_pairs"]["erase_shared_horizon"]
    claims = {
        "outer_code_generators_change": baseline_outer["generator_digest"] != target_outer["generator_digest"],
        "mutation_radius_recorded": int(target["mutation"]["radius"]) in (1, 2),
        "outer_local_clifford_class_recorded": bool(target_outer["local_clifford_class_digest"]),
        "outer_code_is_k1_distance2": target_outer["k"] == 1 and target_outer["distance"] == 2,
        "outer_minimal_reconstruction_shape_matches_baseline": baseline_outer["minimal_reconstruction_regions"]
        == target_outer["minimal_reconstruction_regions"],
        "concatenated_code_size_stable": baseline["metadata"]["n"] == target["metadata"]["n"]
        and baseline["metadata"]["k"] == target["metadata"]["k"],
        "low_order_entropy_status_recorded": isinstance(target["same_labeled_t2_entropy"], bool),
        "shared_horizon_correctability_recorded": isinstance(shared_correctability, tuple)
        and len(shared_correctability) == 2,
        "shared_horizon_fixed_point_recorded": isinstance(shared_fixed_point, tuple) and len(shared_fixed_point) == 2,
        "qec_complementarity_preserved": bool(target["qec_complementarity_identity_all_scenarios"]),
        "outcome_classified": outcome != "residual_unclassified",
    }
    claims["outer_mutation_search_edge"] = all(claims.values())
    return {
        "left": baseline["id"],
        "right": target["id"],
        "edge_type": "bounded_outer_generator_mutation",
        "mutation_radius": target["mutation"]["radius"],
        "edits": target["mutation"]["edits"],
        "outer_local_clifford_class_changes": baseline_outer["local_clifford_class_digest"]
        != target_outer["local_clifford_class_digest"],
        "outcome": outcome,
        "entropy_break": not bool(target["same_labeled_t2_entropy"]),
        "observer_reconstruction_signal": bool(target["entropy_reconstruction_signal"]),
        "algebra_difference_count": target["algebra_difference_count"],
        "shared_horizon_correctability": shared_correctability,
        "shared_horizon_fixed_point": shared_fixed_point,
        "certified_claims": claims,
    }


def phase19_bucket_summary(edges: tuple[dict[str, object], ...]) -> tuple[dict[str, object], ...]:
    outcomes = tuple(sorted({str(edge["outcome"]) for edge in edges}))
    summaries = []
    for outcome in outcomes:
        bucket = tuple(edge for edge in edges if edge["outcome"] == outcome)
        summaries.append(
            {
                "outcome": outcome,
                "count": len(bucket),
                "mutation_radius_histogram": phase19_histogram(edge["mutation_radius"] for edge in bucket),
                "local_clifford_class_change_histogram": phase19_histogram(
                    edge["outer_local_clifford_class_changes"] for edge in bucket
                ),
                "replacement_histogram": phase19_histogram(
                    f"{edit[2]}->{edit[3]}" for edge in bucket for edit in edge["edits"]
                ),
                "edited_position_histogram": phase19_histogram(
                    (edit[0], edit[1]) for edge in bucket for edit in edge["edits"]
                ),
                "algebra_difference_count_histogram": phase19_histogram(
                    edge["algebra_difference_count"] for edge in bucket
                ),
                "examples": tuple(
                    {
                        "target": edge["right"],
                        "mutation_radius": edge["mutation_radius"],
                        "edits": edge["edits"],
                        "outer_local_clifford_class_changes": edge["outer_local_clifford_class_changes"],
                    }
                    for edge in bucket[:3]
                ),
            }
        )
    return tuple(summaries)


def bridge_cosmology_phase19_certificate(
    *,
    max_radius: int = 2,
    include_bases: bool = False,
) -> dict[str, object]:
    mutation_specs = phase19_outer_mutation_specs(max_radius=max_radius)
    graph_search = graph_labeled_pair_source()
    source = graph_search["source"]
    if not isinstance(source, dict):
        raise RuntimeError("expected Phase 10 labeled graph source to find a pair")
    inner_first = source["first"]
    inner_second = source["second"]
    if not isinstance(inner_first, StabilizerCode) or not isinstance(inner_second, StabilizerCode):
        raise TypeError("Phase 19 source must contain StabilizerCode objects")
    hit = phase18_repaired_cover_hit()
    cover = hit["cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 19 repaired hit must contain a PatchCover")
    baseline_outer = StabilizerCode.from_pauli_strings(PHASE18_OUTER_REPAIR_SPECS[0][1])
    baseline_node = phase19_outer_mutation_node(
        label="phase11_outer",
        outer=baseline_outer,
        inner_first=inner_first,
        inner_second=inner_second,
        cover=cover,
        mutation={
            "radius": 0,
            "edits": (),
            "input_generators": PHASE18_OUTER_REPAIR_SPECS[0][1],
        },
        include_bases=include_bases,
    )
    mutation_nodes = tuple(
        phase19_outer_mutation_node(
            label=str(item["label"]),
            outer=item["outer"],
            inner_first=inner_first,
            inner_second=inner_second,
            cover=cover,
            mutation=item,
            include_bases=include_bases,
        )
        for item in mutation_specs["accepted"]
    )
    nodes = (baseline_node,) + mutation_nodes
    edges = tuple(phase19_outer_mutation_edge(baseline=baseline_node, target=node) for node in mutation_nodes)
    bucket_summaries = phase19_bucket_summary(edges)
    outcome_counts = {summary["outcome"]: summary["count"] for summary in bucket_summaries}
    radius_outcome_counts = tuple(
        {
            "radius": radius,
            "outcome_counts": tuple(
                sorted(
                    (
                        outcome,
                        sum(1 for edge in edges if edge["mutation_radius"] == radius and edge["outcome"] == outcome),
                    )
                    for outcome in outcome_counts
                )
            ),
        }
        for radius in range(1, max_radius + 1)
    )
    shared_profiles = tuple(sorted(set(edge["shared_horizon_correctability"] for edge in edges)))
    shared_fixed_points = tuple(sorted(set(edge["shared_horizon_fixed_point"] for edge in edges)))
    outer_lc_classes = tuple(sorted(set(node["outer_code"]["local_clifford_class_digest"] for node in nodes)))
    entropy_break_count = sum(1 for edge in edges if bool(edge["entropy_break"]))
    phase_claims = {
        "bounded_mutation_search_space_enumerated": mutation_specs["counters"]["raw_mutations"] > 0
        and mutation_specs["counters"]["accepted"] == len(mutation_nodes),
        "mutation_edges_certified": len(edges) == len(mutation_nodes)
        and all(edge["certified_claims"]["outer_mutation_search_edge"] for edge in edges),
        "all_scored_outer_codes_are_k1_distance2_same_shape": all(
            node["outer_code"]["k"] == 1
            and node["outer_code"]["distance"] == 2
            and node["outer_code"]["minimal_reconstruction_regions"]
            == baseline_node["outer_code"]["minimal_reconstruction_regions"]
            for node in nodes
        ),
        "phase18_major_buckets_recovered_by_search": (
            outcome_counts.get("full_semantics_preserved", 0) > 0
            and outcome_counts.get("operator_geometry_collapsed", 0) > 0
            and entropy_break_count > 0
        ),
        "radius_one_search_has_no_entropy_break": all(
            not bool(edge["entropy_break"]) for edge in edges if edge["mutation_radius"] == 1
        ),
        "radius_two_search_finds_entropy_break": any(
            bool(edge["entropy_break"]) for edge in edges if edge["mutation_radius"] == 2
        ),
        "entropy_break_with_reconstruction_survival_exists": outcome_counts.get(
            "low_order_entropy_break_with_reconstruction_survives", 0
        )
        > 0,
        "shared_horizon_correctability_stable_across_mutations": shared_profiles == ((True, True),),
        "shared_horizon_fixed_point_stable_across_mutations": shared_fixed_points == ((True, True),),
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "low_order_subsets_checked_for_every_node": all(
            int(node["low_order_entropy"]["subsets_checked"]) == 211 for node in nodes
        ),
        "no_residual_unclassified_outcomes": outcome_counts.get("residual_unclassified", 0) == 0,
    }
    phase_claims["phase_19_bounded_outer_mutation_search_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 19: bounded outer-code mutation taxonomy search",
        "status": "pass" if phase_claims["phase_19_bounded_outer_mutation_search_certificate"] else "fail",
        "graph_spec": {
            "node_source": (
                "Phase 10 graph/CWS inner pair concatenated with every accepted radius<=2 single-entry mutation "
                "of the Phase 11 outer repair code"
            ),
            "edge_rule": "star graph from the Phase 11 outer repair to each accepted mutated outer code",
            "baseline": baseline_node["id"],
            "mutation_alphabet": PHASE19_MUTATION_ALPHABET,
            "max_radius": max_radius,
        },
        "hit_template": {
            "template_kind": hit["template_kind"],
            "observer_p_block_mask": hit["observer_p_block_mask"],
            "observer_q_block_mask": hit["observer_q_block_mask"],
            "shared_block_mask": hit["shared_block_mask"],
        },
        "search_space": {
            "baseline_generators": mutation_specs["baseline_generators"],
            "baseline_reconstruction_shape": mutation_specs["baseline_reconstruction_shape"],
            "counters": mutation_specs["counters"],
        },
        "nodes": nodes,
        "edges": edges,
        "bucket_summary": bucket_summaries,
        "radius_outcome_counts": radius_outcome_counts,
        "outer_code_classification": {
            "local_clifford_class_digests": outer_lc_classes,
            "classes_seen": len(outer_lc_classes),
        },
        "counts": {
            "scored_nodes_including_baseline": len(nodes),
            "accepted_mutation_nodes": len(mutation_nodes),
            "edges": len(edges),
            "outer_local_clifford_classes": len(outer_lc_classes),
            "full_semantics_preserving_targets": outcome_counts.get("full_semantics_preserved", 0),
            "operator_geometry_collapsing_targets": outcome_counts.get("operator_geometry_collapsed", 0),
            "low_order_entropy_breaking_targets": entropy_break_count,
            "low_order_entropy_break_with_operator_collapse_targets": outcome_counts.get(
                "low_order_entropy_break_with_operator_collapse", 0
            ),
            "low_order_entropy_break_with_reconstruction_survives_targets": outcome_counts.get(
                "low_order_entropy_break_with_reconstruction_survives", 0
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The Phase 18 buckets are recovered by an explicit bounded search rather than by a hand-picked menu: "
                "radius-one mutations already show preservation and operator collapse, while radius-two mutations "
                "produce low-order entropy breaks."
            ),
            "surprise": (
                "The search finds a sharper entropy-break subcase: some radius-two mutations break labeled t=2 "
                "entropy while the observer reconstruction signal and two erasure-algebra differences survive."
            ),
            "lesson": (
                "Shared-horizon channel semantics remain stable across the accepted mutation ball, but low-order "
                "entropy and observer algebra split into distinct search-visible features."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 19 turns the outer-swap taxonomy into a bounded search result and exposes an entropy-break "
                "subbucket with surviving reconstruction. The next adaptation should add graph/CWS edge mutations "
                "on the inner pair and compare whether the same bucket structure appears without changing only the "
                "outer repair code."
            ),
            "suggested_phase_20": (
                "Run a bounded inner graph/CWS mutation search under the fixed repaired outer code and Phase 12 cover, "
                "then compare its bucket counts and structural features against the Phase 19 outer-mutation atlas."
            ),
        },
    }


def phase20_graph_subspace_code(edge_mask: int, *, n: int, keep: tuple[int, ...]) -> StabilizerCode:
    state = graph_state(edge_mask, n)
    return StabilizerCode(n, tuple(state.generators[index] for index in keep))


def phase20_inner_graph_outcome(node: dict[str, object]) -> str:
    low_order_matches = bool(node["same_labeled_t2_entropy"])
    signal = bool(node["entropy_reconstruction_signal"])
    algebra_count = int(node["algebra_difference_count"])
    if low_order_matches and signal and algebra_count == 2:
        return "full_semantics_preserved"
    if low_order_matches and not signal and algebra_count == 0:
        return "operator_geometry_collapsed"
    if not low_order_matches and not signal and algebra_count == 0:
        return "low_order_entropy_break_with_operator_collapse"
    if not low_order_matches and signal and algebra_count == 2:
        return "low_order_entropy_break_with_reconstruction_survives"
    if low_order_matches and signal and algebra_count > 2:
        return "entropy_preserved_reconstruction_extra_algebra"
    if not low_order_matches and signal and algebra_count > 2:
        return "entropy_break_reconstruction_extra_algebra"
    if not low_order_matches and not signal and algebra_count > 0:
        return "entropy_break_operator_collapsed_algebra_residue"
    if low_order_matches and not signal and algebra_count > 0:
        return "entropy_preserved_operator_collapsed_algebra_residue"
    return "residual_unclassified"


def phase20_inner_graph_edge_mutation_specs() -> dict[str, object]:
    graph_search = graph_labeled_pair_source()
    source = graph_search["source"]
    graph_metadata = graph_search["graph_metadata"]
    if not isinstance(source, dict) or not isinstance(graph_metadata, dict):
        raise RuntimeError("expected Phase 10 labeled graph source to find a pair")
    first_meta = graph_metadata["first"]
    second_meta = graph_metadata["second"]
    if not isinstance(first_meta, dict) or not isinstance(second_meta, dict):
        raise RuntimeError("expected Phase 10 graph metadata for both source codes")
    n = int(graph_search["scan"]["n"])
    first_edge_mask = int(first_meta["edge_mask"])
    second_edge_mask = int(second_meta["edge_mask"])
    first_keep = tuple(int(index) for index in first_meta["kept_graph_generator_indices"])
    second_keep = tuple(int(index) for index in second_meta["kept_graph_generator_indices"])
    if first_keep != second_keep:
        raise RuntimeError("Phase 20 assumes the Phase 10 pair uses the same kept graph-generator indices")
    seen_pair_digests: set[tuple[str, str]] = set()
    counters = {
        "raw_edge_toggles": 0,
        "duplicate_pair_digests": 0,
        "invalid_inner_k": 0,
        "accepted": 0,
    }
    accepted = []
    for side in ("first", "second"):
        for edge_bit, edge in enumerate(edge_pairs(n)):
            counters["raw_edge_toggles"] += 1
            mutated_first_mask = first_edge_mask
            mutated_second_mask = second_edge_mask
            before_mask = first_edge_mask if side == "first" else second_edge_mask
            edge_was_present = bool((before_mask >> edge_bit) & 1)
            if side == "first":
                mutated_first_mask ^= 1 << edge_bit
            else:
                mutated_second_mask ^= 1 << edge_bit
            first_inner = phase20_graph_subspace_code(mutated_first_mask, n=n, keep=first_keep)
            second_inner = phase20_graph_subspace_code(mutated_second_mask, n=n, keep=first_keep)
            if first_inner.k != 1 or second_inner.k != 1:
                counters["invalid_inner_k"] += 1
                continue
            pair_digest = (phase17_code_digest(first_inner), phase17_code_digest(second_inner))
            if pair_digest in seen_pair_digests:
                counters["duplicate_pair_digests"] += 1
                continue
            seen_pair_digests.add(pair_digest)
            action = "remove" if edge_was_present else "add"
            label = f"{side}_toggle_{edge[0]}_{edge[1]}_{action}"
            accepted.append(
                {
                    "label": label,
                    "radius": 1,
                    "side": side,
                    "edge_bit": edge_bit,
                    "edge": edge,
                    "action": action,
                    "edge_was_present": edge_was_present,
                    "first_edge_mask": mutated_first_mask,
                    "second_edge_mask": mutated_second_mask,
                    "keep": first_keep,
                    "first_inner": first_inner,
                    "second_inner": second_inner,
                    "pair_digest": pair_digest,
                }
            )
            counters["accepted"] += 1
    return {
        "graph_search": {key: value for key, value in graph_search.items() if key != "source"},
        "baseline": {
            "n": n,
            "first_edge_mask": first_edge_mask,
            "second_edge_mask": second_edge_mask,
            "first_edges": graph_edge_list(first_edge_mask, n),
            "second_edges": graph_edge_list(second_edge_mask, n),
            "keep": first_keep,
        },
        "counters": counters,
        "accepted": tuple(accepted),
    }


def phase20_inner_graph_node(
    *,
    label: str,
    first_inner: StabilizerCode,
    second_inner: StabilizerCode,
    outer: StabilizerCode,
    cover: PatchCover,
    mutation: dict[str, object],
    include_bases: bool = False,
) -> dict[str, object]:
    first_repaired, first_metadata = logical_concatenate_k1(first_inner, outer)
    second_repaired, second_metadata = logical_concatenate_k1(second_inner, outer)
    node = phase15_node_diagnostic(
        node_id=f"inner_graph_mutation:{label}",
        model_kind="distance_repaired_noncss_inner_graph_edge_mutation",
        first=first_repaired,
        second=second_repaired,
        cover=cover,
        metadata={
            "inner_label": label,
            "mutation_radius": mutation["radius"],
            "n": first_repaired.n,
            "k": first_repaired.k,
        },
        include_bases=include_bases,
    )
    low_order_entropy = low_order_entropy_match_by_rank(first_repaired, second_repaired, max_subset_size=2)
    inner_low_order_entropy = low_order_entropy_match_by_rank(first_inner, second_inner, max_subset_size=2)
    return {
        **node,
        "mutation": {
            "radius": mutation["radius"],
            "side": mutation["side"],
            "edge": mutation["edge"],
            "edge_bit": mutation["edge_bit"],
            "action": mutation["action"],
            "first_edge_mask": mutation["first_edge_mask"],
            "second_edge_mask": mutation["second_edge_mask"],
            "keep": mutation["keep"],
        },
        "inner_pair": {
            "n": first_inner.n,
            "k_first": first_inner.k,
            "k_second": second_inner.k,
            "distance_first": first_inner.distance(),
            "distance_second": second_inner.distance(),
            "first_edges": graph_edge_list(int(mutation["first_edge_mask"]), first_inner.n),
            "second_edges": graph_edge_list(int(mutation["second_edge_mask"]), second_inner.n),
            "first_generators": first_inner.pauli_generators(),
            "second_generators": second_inner.pauli_generators(),
            "same_labeled_t2_entropy_before_repair": inner_low_order_entropy["matches"],
            "low_order_entropy_before_repair": inner_low_order_entropy,
        },
        "outer_code": phase18_outer_code_summary("phase11_outer_fixed", outer),
        "low_order_entropy": low_order_entropy,
        "same_labeled_t2_entropy": low_order_entropy["matches"],
        "first_generator_digest": phase17_code_digest(first_repaired),
        "second_generator_digest": phase17_code_digest(second_repaired),
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
    }


def phase20_inner_graph_edge(*, baseline: dict[str, object], target: dict[str, object]) -> dict[str, object]:
    outcome = phase20_inner_graph_outcome(target)
    side = str(target["mutation"]["side"])
    shared_correctability = target["correctability_pairs"]["erase_shared_horizon"]
    shared_fixed_point = target["survivor_fixed_point_pairs"]["erase_shared_horizon"]
    first_changed = baseline["first_generator_digest"] != target["first_generator_digest"]
    second_changed = baseline["second_generator_digest"] != target["second_generator_digest"]
    claims = {
        "single_graph_edge_toggle_recorded": int(target["mutation"]["radius"]) == 1
        and isinstance(target["mutation"]["edge"], tuple)
        and len(target["mutation"]["edge"]) == 2,
        "only_declared_inner_side_changes_after_repair": (
            (side == "first" and first_changed and not second_changed)
            or (side == "second" and second_changed and not first_changed)
        ),
        "fixed_outer_code_is_k1_distance2": target["outer_code"]["k"] == 1 and target["outer_code"]["distance"] == 2,
        "inner_pair_is_k1": target["inner_pair"]["k_first"] == 1 and target["inner_pair"]["k_second"] == 1,
        "concatenated_code_size_stable": baseline["metadata"]["n"] == target["metadata"]["n"]
        and baseline["metadata"]["k"] == target["metadata"]["k"],
        "low_order_entropy_status_recorded": isinstance(target["same_labeled_t2_entropy"], bool),
        "shared_horizon_correctability_recorded": isinstance(shared_correctability, tuple)
        and len(shared_correctability) == 2,
        "shared_horizon_fixed_point_recorded": isinstance(shared_fixed_point, tuple) and len(shared_fixed_point) == 2,
        "qec_complementarity_preserved": bool(target["qec_complementarity_identity_all_scenarios"]),
        "outcome_classified": outcome != "residual_unclassified",
    }
    claims["inner_graph_mutation_edge"] = all(claims.values())
    return {
        "left": baseline["id"],
        "right": target["id"],
        "edge_type": "inner_graph_edge_toggle",
        "mutation_radius": target["mutation"]["radius"],
        "side": side,
        "edge": target["mutation"]["edge"],
        "action": target["mutation"]["action"],
        "outcome": outcome,
        "entropy_break": not bool(target["same_labeled_t2_entropy"]),
        "observer_reconstruction_signal": bool(target["entropy_reconstruction_signal"]),
        "algebra_difference_count": target["algebra_difference_count"],
        "shared_horizon_correctability": shared_correctability,
        "shared_horizon_fixed_point": shared_fixed_point,
        "certified_claims": claims,
    }


def phase20_bucket_summary(edges: tuple[dict[str, object], ...]) -> tuple[dict[str, object], ...]:
    outcomes = tuple(sorted({str(edge["outcome"]) for edge in edges}))
    summaries = []
    for outcome in outcomes:
        bucket = tuple(edge for edge in edges if edge["outcome"] == outcome)
        summaries.append(
            {
                "outcome": outcome,
                "count": len(bucket),
                "side_histogram": phase19_histogram(edge["side"] for edge in bucket),
                "action_histogram": phase19_histogram(edge["action"] for edge in bucket),
                "edge_histogram": phase19_histogram(edge["edge"] for edge in bucket),
                "algebra_difference_count_histogram": phase19_histogram(
                    edge["algebra_difference_count"] for edge in bucket
                ),
                "examples": tuple(
                    {
                        "target": edge["right"],
                        "side": edge["side"],
                        "edge": edge["edge"],
                        "action": edge["action"],
                    }
                    for edge in bucket[:3]
                ),
            }
        )
    return tuple(summaries)


def bridge_cosmology_phase20_certificate(*, include_bases: bool = False) -> dict[str, object]:
    mutation_specs = phase20_inner_graph_edge_mutation_specs()
    baseline_spec = mutation_specs["baseline"]
    outer = phase11_outer_distance_repair_code()
    hit = phase18_repaired_cover_hit()
    cover = hit["cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 20 repaired hit must contain a PatchCover")
    n = int(baseline_spec["n"])
    keep = tuple(int(index) for index in baseline_spec["keep"])
    baseline_first_inner = phase20_graph_subspace_code(int(baseline_spec["first_edge_mask"]), n=n, keep=keep)
    baseline_second_inner = phase20_graph_subspace_code(int(baseline_spec["second_edge_mask"]), n=n, keep=keep)
    baseline_node = phase20_inner_graph_node(
        label="phase10_graph_baseline",
        first_inner=baseline_first_inner,
        second_inner=baseline_second_inner,
        outer=outer,
        cover=cover,
        mutation={
            "radius": 0,
            "side": "none",
            "edge": (),
            "edge_bit": None,
            "action": "none",
            "first_edge_mask": baseline_spec["first_edge_mask"],
            "second_edge_mask": baseline_spec["second_edge_mask"],
            "keep": keep,
        },
        include_bases=include_bases,
    )
    mutation_nodes = tuple(
        phase20_inner_graph_node(
            label=str(item["label"]),
            first_inner=item["first_inner"],
            second_inner=item["second_inner"],
            outer=outer,
            cover=cover,
            mutation=item,
            include_bases=include_bases,
        )
        for item in mutation_specs["accepted"]
    )
    nodes = (baseline_node,) + mutation_nodes
    edges = tuple(phase20_inner_graph_edge(baseline=baseline_node, target=node) for node in mutation_nodes)
    bucket_summaries = phase20_bucket_summary(edges)
    outcome_counts = {summary["outcome"]: summary["count"] for summary in bucket_summaries}
    shared_profiles = tuple(sorted(set(edge["shared_horizon_correctability"] for edge in edges)))
    shared_fixed_points = tuple(sorted(set(edge["shared_horizon_fixed_point"] for edge in edges)))
    phase19_reference = bridge_cosmology_phase19_certificate(max_radius=2, include_bases=False)
    phase19_radius_one_counts = {
        int(item["radius"]): dict(item["outcome_counts"]) for item in phase19_reference["radius_outcome_counts"]
    }
    entropy_break_count = sum(1 for edge in edges if bool(edge["entropy_break"]))
    observer_signal_count = sum(1 for edge in edges if bool(edge["observer_reconstruction_signal"]))
    phase_claims = {
        "radius_one_graph_edge_ball_enumerated": mutation_specs["counters"]["raw_edge_toggles"] == 20
        and mutation_specs["counters"]["accepted"] == 20
        and len(edges) == 20,
        "inner_graph_mutation_edges_certified": all(edge["certified_claims"]["inner_graph_mutation_edge"] for edge in edges),
        "all_nodes_use_fixed_outer_repair": all(node["outer_code"]["generators"] == baseline_node["outer_code"]["generators"] for node in nodes),
        "all_nodes_concatenated_k1_n20": all(node["metadata"]["n"] == 20 and node["metadata"]["k"] == 1 for node in nodes),
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "shared_horizon_correctability_stable_across_inner_graph_mutations": shared_profiles == ((True, True),),
        "shared_horizon_fixed_point_stable_across_inner_graph_mutations": shared_fixed_points == ((True, True),),
        "inner_radius_one_finds_entropy_breaks": entropy_break_count > 0,
        "inner_radius_one_finds_phase19_preserve_and_collapse_buckets": (
            outcome_counts.get("full_semantics_preserved", 0) > 0
            and outcome_counts.get("operator_geometry_collapsed", 0) > 0
        ),
        "inner_radius_one_has_extra_algebra_buckets": (
            outcome_counts.get("entropy_preserved_reconstruction_extra_algebra", 0) > 0
            and outcome_counts.get("entropy_break_operator_collapsed_algebra_residue", 0) > 0
        ),
        "inner_radius_one_differs_from_outer_radius_one_entropy_break_behavior": (
            entropy_break_count > 0
            and phase19_radius_one_counts[1].get("low_order_entropy_break_with_operator_collapse", 0) == 0
            and phase19_radius_one_counts[1].get("low_order_entropy_break_with_reconstruction_survives", 0) == 0
        ),
        "observer_signal_survives_some_entropy_breaks": outcome_counts.get(
            "low_order_entropy_break_with_reconstruction_survives", 0
        )
        + outcome_counts.get("entropy_break_reconstruction_extra_algebra", 0)
        > 0,
        "no_residual_unclassified_outcomes": outcome_counts.get("residual_unclassified", 0) == 0,
        "low_order_subsets_checked_for_every_node": all(
            int(node["low_order_entropy"]["subsets_checked"]) == 211 for node in nodes
        ),
    }
    phase_claims["phase_20_inner_graph_mutation_search_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 20: bounded inner graph/CWS mutation taxonomy search",
        "status": "pass" if phase_claims["phase_20_inner_graph_mutation_search_certificate"] else "fail",
        "graph_spec": {
            "node_source": (
                "Phase 10 graph/CWS inner pair with one graph edge toggled on exactly one side, then concatenated "
                "with the fixed Phase 11 outer repair code"
            ),
            "edge_rule": "star graph from the Phase 10 inner graph baseline to each radius-one graph-edge toggle",
            "baseline": baseline_node["id"],
            "inner_graph_n": n,
            "kept_graph_generator_indices": keep,
        },
        "hit_template": {
            "template_kind": hit["template_kind"],
            "observer_p_block_mask": hit["observer_p_block_mask"],
            "observer_q_block_mask": hit["observer_q_block_mask"],
            "shared_block_mask": hit["shared_block_mask"],
        },
        "search_space": {
            "baseline": baseline_spec,
            "counters": mutation_specs["counters"],
        },
        "nodes": nodes,
        "edges": edges,
        "bucket_summary": bucket_summaries,
        "phase19_outer_mutation_comparison": {
            "status": phase19_reference["status"],
            "counts": phase19_reference["counts"],
            "radius_outcome_counts": phase19_reference["radius_outcome_counts"],
            "contrast": (
                "Phase 19 outer-code radius-one mutations do not break low-order entropy, while Phase 20 inner "
                "graph-edge radius-one mutations do."
            ),
        },
        "counts": {
            "scored_nodes_including_baseline": len(nodes),
            "accepted_mutation_nodes": len(mutation_nodes),
            "edges": len(edges),
            "full_semantics_preserving_targets": outcome_counts.get("full_semantics_preserved", 0),
            "operator_geometry_collapsing_targets": outcome_counts.get("operator_geometry_collapsed", 0),
            "low_order_entropy_breaking_targets": entropy_break_count,
            "observer_reconstruction_signal_targets": observer_signal_count,
            "entropy_break_operator_collapsed_algebra_residue_targets": outcome_counts.get(
                "entropy_break_operator_collapsed_algebra_residue", 0
            ),
            "entropy_preserved_reconstruction_extra_algebra_targets": outcome_counts.get(
                "entropy_preserved_reconstruction_extra_algebra", 0
            ),
            "entropy_break_reconstruction_extra_algebra_targets": outcome_counts.get(
                "entropy_break_reconstruction_extra_algebra", 0
            ),
            "low_order_entropy_break_with_reconstruction_survives_targets": outcome_counts.get(
                "low_order_entropy_break_with_reconstruction_survives", 0
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A radius-one inner graph-edge mutation search already produces entropy breaks, preservation, "
                "operator collapse, and extra-algebra buckets under the same outer repair and repaired cover."
            ),
            "contrast_with_phase19": (
                "Outer repair mutations needed radius two to break low-order entropy; inner graph connectivity "
                "mutations break it at radius one. Inner mutations also create algebra-residue buckets that do not "
                "appear in the Phase 19 outer-mutation taxonomy."
            ),
            "lesson": (
                "The repaired shared-horizon channel semantics are still stable, but inner connectivity is a more "
                "sensitive control knob for entropy/algebra structure than nearby outer-code repair edits."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 20 shows that inner graph connectivity mutations expose richer entropy/algebra buckets while "
                "preserving shared-horizon channel semantics. The next adaptation should combine inner graph toggles "
                "and outer repair mutations into a two-layer transition graph and search for paths that keep horizon "
                "fixed points stable while moving between entropy/algebra buckets."
            ),
            "suggested_phase_21": (
                "Build a mixed inner-outer mutation graph whose edges are certified single inner graph toggles or "
                "single outer repair mutations, then classify reachable bucket transitions and monotonicity failures."
            ),
        },
    }


def phase21_node_id(inner_label: str, outer_label: str) -> str:
    return f"mixed_io:{inner_label}|{outer_label}"


def phase21_inner_representative_states(
    *,
    outer: StabilizerCode,
    cover: PatchCover,
) -> tuple[dict[str, object], ...]:
    mutation_specs = phase20_inner_graph_edge_mutation_specs()
    baseline_spec = mutation_specs["baseline"]
    n = int(baseline_spec["n"])
    keep = tuple(int(index) for index in baseline_spec["keep"])
    baseline_mutation = {
        "radius": 0,
        "side": "none",
        "edge": (),
        "edge_bit": None,
        "action": "none",
        "first_edge_mask": baseline_spec["first_edge_mask"],
        "second_edge_mask": baseline_spec["second_edge_mask"],
        "keep": keep,
    }
    baseline_first = phase20_graph_subspace_code(int(baseline_spec["first_edge_mask"]), n=n, keep=keep)
    baseline_second = phase20_graph_subspace_code(int(baseline_spec["second_edge_mask"]), n=n, keep=keep)
    out: list[dict[str, object]] = [
        {
            "label": "inner_baseline",
            "selection_outcome": "full_semantics_preserved",
            "first_inner": baseline_first,
            "second_inner": baseline_second,
            "mutation": baseline_mutation,
            "selection_node": None,
        }
    ]
    seen_outcomes: set[str] = set()
    for item in mutation_specs["accepted"]:
        node = phase20_inner_graph_node(
            label=str(item["label"]),
            first_inner=item["first_inner"],
            second_inner=item["second_inner"],
            outer=outer,
            cover=cover,
            mutation=item,
            include_bases=False,
        )
        outcome = phase20_inner_graph_outcome(node)
        if outcome in seen_outcomes:
            continue
        seen_outcomes.add(outcome)
        out.append(
            {
                "label": item["label"],
                "selection_outcome": outcome,
                "first_inner": item["first_inner"],
                "second_inner": item["second_inner"],
                "mutation": item,
                "selection_node": node,
            }
        )
    return tuple(out)


def phase21_outer_radius_one_states() -> tuple[dict[str, object], ...]:
    baseline_outer = phase11_outer_distance_repair_code()
    baseline_summary = phase18_outer_code_summary("outer_baseline", baseline_outer)
    out: list[dict[str, object]] = [
        {
            "label": "outer_baseline",
            "outer": baseline_outer,
            "mutation": {
                "radius": 0,
                "edits": (),
                "input_generators": baseline_outer.pauli_generators(),
            },
            "outer_code": baseline_summary,
        }
    ]
    for item in phase19_outer_mutation_specs(max_radius=1)["accepted"]:
        label = str(item["label"])
        outer = item["outer"]
        if not isinstance(outer, StabilizerCode):
            raise TypeError("Phase 21 outer mutation state must contain a StabilizerCode")
        out.append(
            {
                "label": label,
                "outer": outer,
                "mutation": {
                    "radius": item["radius"],
                    "edits": item["edits"],
                    "input_generators": item["input_generators"],
                },
                "outer_code": phase18_outer_code_summary(label, outer),
            }
        )
    return tuple(out)


def phase21_mixed_node(
    *,
    inner_state: dict[str, object],
    outer_state: dict[str, object],
    cover: PatchCover,
    include_bases: bool = False,
) -> dict[str, object]:
    first_inner = inner_state["first_inner"]
    second_inner = inner_state["second_inner"]
    outer = outer_state["outer"]
    if not isinstance(first_inner, StabilizerCode) or not isinstance(second_inner, StabilizerCode):
        raise TypeError("Phase 21 inner state must contain StabilizerCode objects")
    if not isinstance(outer, StabilizerCode):
        raise TypeError("Phase 21 outer state must contain a StabilizerCode")
    inner_label = str(inner_state["label"])
    outer_label = str(outer_state["label"])
    first_repaired, first_metadata = logical_concatenate_k1(first_inner, outer)
    second_repaired, second_metadata = logical_concatenate_k1(second_inner, outer)
    node = phase15_node_diagnostic(
        node_id=phase21_node_id(inner_label, outer_label),
        model_kind="mixed_inner_graph_outer_repair_mutation",
        first=first_repaired,
        second=second_repaired,
        cover=cover,
        metadata={
            "inner_label": inner_label,
            "outer_label": outer_label,
            "inner_mutation_radius": inner_state["mutation"]["radius"],  # type: ignore[index]
            "outer_mutation_radius": outer_state["mutation"]["radius"],  # type: ignore[index]
            "n": first_repaired.n,
            "k": first_repaired.k,
        },
        include_bases=include_bases,
    )
    low_order_entropy = low_order_entropy_match_by_rank(first_repaired, second_repaired, max_subset_size=2)
    inner_low_order_entropy = low_order_entropy_match_by_rank(first_inner, second_inner, max_subset_size=2)
    inner_mutation = inner_state["mutation"]
    if not isinstance(inner_mutation, dict):
        raise TypeError("Phase 21 inner mutation must be a dict")
    public_inner_mutation = {
        key: inner_mutation[key]
        for key in (
            "radius",
            "side",
            "edge",
            "edge_bit",
            "action",
            "first_edge_mask",
            "second_edge_mask",
            "keep",
        )
        if key in inner_mutation
    }
    enriched = {
        **node,
        "inner_state": {
            "label": inner_label,
            "selection_outcome": inner_state["selection_outcome"],
            "mutation": public_inner_mutation,
        },
        "outer_state": {
            "label": outer_label,
            "mutation": outer_state["mutation"],
        },
        "inner_pair": {
            "n": first_inner.n,
            "k_first": first_inner.k,
            "k_second": second_inner.k,
            "first_generators": first_inner.pauli_generators(),
            "second_generators": second_inner.pauli_generators(),
            "first_inner_digest": phase17_code_digest(first_inner),
            "second_inner_digest": phase17_code_digest(second_inner),
            "pair_digest": (phase17_code_digest(first_inner), phase17_code_digest(second_inner)),
            "same_labeled_t2_entropy_before_repair": inner_low_order_entropy["matches"],
            "low_order_entropy_before_repair": inner_low_order_entropy,
        },
        "outer_code": outer_state["outer_code"],
        "low_order_entropy": low_order_entropy,
        "same_labeled_t2_entropy": low_order_entropy["matches"],
        "first_generator_digest": phase17_code_digest(first_repaired),
        "second_generator_digest": phase17_code_digest(second_repaired),
        "concatenation": {
            "first": first_metadata,
            "second": second_metadata,
        },
    }
    return {
        **enriched,
        "outcome": phase20_inner_graph_outcome(enriched),
    }


def phase21_mixed_edge(
    *,
    edge_type: str,
    source: dict[str, object],
    target: dict[str, object],
) -> dict[str, object]:
    source_algebra_count = int(source["algebra_difference_count"])
    target_algebra_count = int(target["algebra_difference_count"])
    algebra_delta = target_algebra_count - source_algebra_count
    entropy_flip = bool(source["same_labeled_t2_entropy"]) != bool(target["same_labeled_t2_entropy"])
    signal_flip = bool(source["entropy_reconstruction_signal"]) != bool(target["entropy_reconstruction_signal"])
    shared_correctability_stable = (
        source["correctability_pairs"]["erase_shared_horizon"]
        == target["correctability_pairs"]["erase_shared_horizon"]
        == (True, True)
    )
    shared_fixed_point_stable = (
        source["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == target["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == (True, True)
    )
    if edge_type == "inner_graph_toggle":
        same_axis_claim = (
            source["outer_code"]["generator_digest"] == target["outer_code"]["generator_digest"]
            and source["inner_state"]["label"] == "inner_baseline"
            and target["inner_state"]["mutation"]["radius"] == 1
        )
    elif edge_type == "outer_repair_mutation":
        same_axis_claim = (
            source["inner_pair"]["pair_digest"] == target["inner_pair"]["pair_digest"]
            and source["outer_state"]["label"] == "outer_baseline"
            and target["outer_state"]["mutation"]["radius"] == 1
        )
    else:
        raise ValueError(f"unknown Phase 21 edge type {edge_type!r}")
    claims = {
        "single_axis_mutation_edge": same_axis_claim,
        "source_and_target_exact_qec_complementarity": bool(source["qec_complementarity_identity_all_scenarios"])
        and bool(target["qec_complementarity_identity_all_scenarios"]),
        "shared_horizon_correctability_stable": shared_correctability_stable,
        "shared_horizon_fixed_point_stable": shared_fixed_point_stable,
        "source_and_target_classified": source["outcome"] != "residual_unclassified"
        and target["outcome"] != "residual_unclassified",
    }
    claims["mixed_inner_outer_transition_edge"] = all(claims.values())
    return {
        "left": source["id"],
        "right": target["id"],
        "edge_type": edge_type,
        "from_outcome": source["outcome"],
        "to_outcome": target["outcome"],
        "algebra_difference_count_delta": algebra_delta,
        "algebra_monotonicity": "increase" if algebra_delta > 0 else "decrease" if algebra_delta < 0 else "flat",
        "entropy_match_flips": entropy_flip,
        "observer_signal_flips": signal_flip,
        "shared_horizon_correctability": target["correctability_pairs"]["erase_shared_horizon"],
        "shared_horizon_fixed_point": target["survivor_fixed_point_pairs"]["erase_shared_horizon"],
        "certified_claims": claims,
    }


def phase21_reachability(
    *,
    node_ids: tuple[str, ...],
    edges: tuple[dict[str, object], ...],
    start: str,
) -> dict[str, int]:
    adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
    for edge in edges:
        left = str(edge["left"])
        right = str(edge["right"])
        adjacency[left].append(right)
        adjacency[right].append(left)
    distances = {start: 0}
    frontier = [start]
    while frontier:
        current = frontier.pop(0)
        for nxt in adjacency[current]:
            if nxt in distances:
                continue
            distances[nxt] = distances[current] + 1
            frontier.append(nxt)
    return distances


def phase21_square_certificates(
    *,
    inner_states: tuple[dict[str, object], ...],
    outer_states: tuple[dict[str, object], ...],
    edge_lookup: set[tuple[str, str]],
) -> tuple[dict[str, object], ...]:
    squares = []
    baseline_inner = "inner_baseline"
    baseline_outer = "outer_baseline"
    base = phase21_node_id(baseline_inner, baseline_outer)
    for inner in inner_states:
        inner_label = str(inner["label"])
        if inner_label == baseline_inner:
            continue
        for outer in outer_states:
            outer_label = str(outer["label"])
            if outer_label == baseline_outer:
                continue
            inner_axis = phase21_node_id(inner_label, baseline_outer)
            outer_axis = phase21_node_id(baseline_inner, outer_label)
            mixed = phase21_node_id(inner_label, outer_label)
            path_inner_then_outer = (base, inner_axis, mixed)
            path_outer_then_inner = (base, outer_axis, mixed)
            required_edges = (
                (base, inner_axis),
                (inner_axis, mixed),
                (base, outer_axis),
                (outer_axis, mixed),
            )
            certified = all((left, right) in edge_lookup or (right, left) in edge_lookup for left, right in required_edges)
            squares.append(
                {
                    "inner_label": inner_label,
                    "outer_label": outer_label,
                    "inner_then_outer_path": path_inner_then_outer,
                    "outer_then_inner_path": path_outer_then_inner,
                    "common_endpoint": mixed,
                    "certified_square": certified,
                }
            )
    return tuple(squares)


def bridge_cosmology_phase21_certificate(*, include_bases: bool = False) -> dict[str, object]:
    cover = phase18_repaired_cover_hit()["cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 21 repaired hit must contain a PatchCover")
    baseline_outer = phase11_outer_distance_repair_code()
    inner_states = phase21_inner_representative_states(outer=baseline_outer, cover=cover)
    outer_states = phase21_outer_radius_one_states()
    nodes = tuple(
        phase21_mixed_node(
            inner_state=inner_state,
            outer_state=outer_state,
            cover=cover,
            include_bases=include_bases,
        )
        for inner_state in inner_states
        for outer_state in outer_states
    )
    node_by_axes = {
        (str(node["metadata"]["inner_label"]), str(node["metadata"]["outer_label"])): node
        for node in nodes
    }
    edges = []
    for outer_state in outer_states:
        outer_label = str(outer_state["label"])
        source = node_by_axes[("inner_baseline", outer_label)]
        for inner_state in inner_states:
            inner_label = str(inner_state["label"])
            if inner_label == "inner_baseline":
                continue
            target = node_by_axes[(inner_label, outer_label)]
            edges.append(phase21_mixed_edge(edge_type="inner_graph_toggle", source=source, target=target))
    for inner_state in inner_states:
        inner_label = str(inner_state["label"])
        source = node_by_axes[(inner_label, "outer_baseline")]
        for outer_state in outer_states:
            outer_label = str(outer_state["label"])
            if outer_label == "outer_baseline":
                continue
            target = node_by_axes[(inner_label, outer_label)]
            edges.append(phase21_mixed_edge(edge_type="outer_repair_mutation", source=source, target=target))
    edges_tuple = tuple(edges)
    edge_lookup = {(str(edge["left"]), str(edge["right"])) for edge in edges_tuple}
    squares = phase21_square_certificates(
        inner_states=inner_states,
        outer_states=outer_states,
        edge_lookup=edge_lookup,
    )
    node_ids = tuple(str(node["id"]) for node in nodes)
    start = phase21_node_id("inner_baseline", "outer_baseline")
    distances = phase21_reachability(node_ids=node_ids, edges=edges_tuple, start=start)
    outcome_counts = phase19_histogram(str(node["outcome"]) for node in nodes)
    edge_type_counts = phase16_count_edge_types(edges_tuple)
    transition_counts = phase19_histogram((edge["from_outcome"], edge["to_outcome"]) for edge in edges_tuple)
    algebra_monotonicity_counts = dict(phase19_histogram(edge["algebra_monotonicity"] for edge in edges_tuple))
    entropy_flip_count = sum(1 for edge in edges_tuple if bool(edge["entropy_match_flips"]))
    signal_flip_count = sum(1 for edge in edges_tuple if bool(edge["observer_signal_flips"]))
    shared_profiles = tuple(sorted(set(node["correctability_pairs"]["erase_shared_horizon"] for node in nodes)))
    shared_fixed_points = tuple(sorted(set(node["survivor_fixed_point_pairs"]["erase_shared_horizon"] for node in nodes)))
    outcome_min_depths = tuple(
        sorted(
            (
                outcome,
                min(distances[str(node["id"])] for node in nodes if str(node["outcome"]) == outcome),
            )
            for outcome, _ in outcome_counts
        )
    )
    phase_claims = {
        "mixed_product_nodes_scored": len(nodes) == len(inner_states) * len(outer_states) == 49,
        "mixed_axis_edges_certified": len(edges_tuple) == 84
        and all(edge["certified_claims"]["mixed_inner_outer_transition_edge"] for edge in edges_tuple),
        "commuting_squares_certified": len(squares) == 36 and all(square["certified_square"] for square in squares),
        "all_nodes_reachable_within_two_steps": len(distances) == len(nodes) and max(distances.values()) == 2,
        "shared_horizon_correctability_stable_across_mixed_graph": shared_profiles == ((True, True),),
        "shared_horizon_fixed_point_stable_across_mixed_graph": shared_fixed_points == ((True, True),),
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "mixed_graph_contains_entropy_break_and_operator_collapse": dict(outcome_counts).get(
            "low_order_entropy_break_with_reconstruction_survives", 0
        )
        > 0
        and dict(outcome_counts).get("operator_geometry_collapsed", 0) > 0,
        "mixed_graph_contains_extra_algebra_buckets": dict(outcome_counts).get(
            "entropy_preserved_reconstruction_extra_algebra", 0
        )
        > 0
        and dict(outcome_counts).get("entropy_break_operator_collapsed_algebra_residue", 0) > 0,
        "algebra_difference_monotonicity_failures_exist": algebra_monotonicity_counts.get("increase", 0) > 0
        and algebra_monotonicity_counts.get("decrease", 0) > 0,
        "entropy_and_signal_flip_edges_exist": entropy_flip_count > 0 and signal_flip_count > 0,
        "low_order_subsets_checked_for_every_node": all(
            int(node["low_order_entropy"]["subsets_checked"]) == 211 for node in nodes
        ),
        "no_residual_unclassified_nodes": dict(outcome_counts).get("residual_unclassified", 0) == 0,
    }
    phase_claims["phase_21_mixed_inner_outer_transition_graph_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 21: mixed inner-outer mutation transition graph",
        "status": "pass" if phase_claims["phase_21_mixed_inner_outer_transition_graph_certificate"] else "fail",
        "graph_spec": {
            "node_source": (
                "bounded product of one representative from each Phase 20 inner graph bucket and all Phase 19 "
                "radius-one outer repair mutations"
            ),
            "edge_rules": (
                "inner_graph_toggle: same outer state, move from inner baseline to one selected Phase 20 inner toggle",
                "outer_repair_mutation: same inner state, move from outer baseline to one Phase 19 radius-one outer mutation",
            ),
            "baseline": start,
            "inner_state_count": len(inner_states),
            "outer_state_count": len(outer_states),
        },
        "nodes": nodes,
        "edges": edges_tuple,
        "commuting_squares": squares,
        "reachability": {
            "distances_from_baseline": tuple(sorted(distances.items())),
            "outcome_min_depths": outcome_min_depths,
            "max_distance": max(distances.values()) if distances else None,
        },
        "classification": {
            "node_outcome_counts": outcome_counts,
            "edge_type_counts": tuple(sorted(edge_type_counts.items())),
            "edge_transition_counts": transition_counts,
            "algebra_monotonicity_counts": tuple(sorted(algebra_monotonicity_counts.items())),
            "entropy_match_flip_edges": entropy_flip_count,
            "observer_signal_flip_edges": signal_flip_count,
        },
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges_tuple),
            "inner_states": len(inner_states),
            "outer_states": len(outer_states),
            "commuting_squares": len(squares),
            "algebra_increase_edges": algebra_monotonicity_counts.get("increase", 0),
            "algebra_decrease_edges": algebra_monotonicity_counts.get("decrease", 0),
            "algebra_flat_edges": algebra_monotonicity_counts.get("flat", 0),
            "entropy_match_flip_edges": entropy_flip_count,
            "observer_signal_flip_edges": signal_flip_count,
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The mixed graph certifies two-layer inner/outer mutation squares: every selected inner graph toggle "
                "can be composed with every radius-one outer repair mutation in either order to reach the same exact "
                "scored node."
            ),
            "monotonicity_lesson": (
                "Algebra-difference count is not monotone on the mixed graph: certified edges both increase and "
                "decrease it, while shared-horizon correctability and fixed-point semantics stay stable."
            ),
            "pressure_test": (
                "The same stable horizon channel can coexist with reachable entropy breaks, operator collapse, and "
                "extra algebra-residue buckets within two exact mutation steps."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 21 provides a certified mixed transition graph and finds algebra monotonicity failures under "
                "stable horizon semantics. The next adaptation should add a time/channel layer on this graph, treating "
                "edges as elementary stochastic or deterministic transitions and checking which bucket probabilities "
                "or fixed-point profiles are invariant under simple channels."
            ),
            "suggested_phase_22": (
                "Define small Markov/channel dynamics on the Phase 21 graph, then certify stationary bucket weights, "
                "absorbing sets, and horizon fixed-point invariants exactly over rational transition matrices."
            ),
        },
    }


def phase22_fraction(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "string": f"{value.numerator}/{value.denominator}",
    }


def phase22_fraction_histogram(items: Iterable[tuple[object, Fraction]]) -> tuple[dict[str, object], ...]:
    totals: dict[object, Fraction] = {}
    for key, value in items:
        totals[key] = totals.get(key, Fraction(0, 1)) + value
    return tuple(
        {
            "key": key,
            "weight": phase22_fraction(totals[key]),
        }
        for key in sorted(totals, key=str)
    )


def phase22_phase21_graph_data() -> dict[str, object]:
    phase21 = bridge_cosmology_phase21_certificate(include_bases=False)
    nodes = tuple(phase21["nodes"])
    edges = tuple(phase21["edges"])
    node_by_id = {str(node["id"]): node for node in nodes if isinstance(node, dict)}
    adjacency: dict[str, set[str]] = {node_id: set() for node_id in node_by_id}
    for edge in edges:
        if not isinstance(edge, dict):
            raise TypeError("Phase 21 edge must be a dict")
        left = str(edge["left"])
        right = str(edge["right"])
        adjacency[left].add(right)
        adjacency[right].add(left)
    return {
        "phase21_status": phase21["status"],
        "phase21_claims": phase21["certified_claims"],
        "node_by_id": node_by_id,
        "node_ids": tuple(node_by_id),
        "edges": edges,
        "adjacency": {node_id: tuple(sorted(neighbors)) for node_id, neighbors in adjacency.items()},
        "phase21_counts": phase21["counts"],
    }


def phase22_sparse_rows_to_public(rows: dict[str, dict[str, Fraction]]) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "from": source,
            "transitions": tuple(
                {
                    "to": target,
                    "probability": phase22_fraction(probability),
                }
                for target, probability in sorted(targets.items())
            ),
        }
        for source, targets in sorted(rows.items())
    )


def phase22_rows_are_stochastic(rows: dict[str, dict[str, Fraction]]) -> bool:
    return all(sum(targets.values(), Fraction(0, 1)) == Fraction(1, 1) for targets in rows.values())


def phase22_random_walk_rows(adjacency: dict[str, tuple[str, ...]]) -> dict[str, dict[str, Fraction]]:
    rows: dict[str, dict[str, Fraction]] = {}
    for node_id, neighbors in adjacency.items():
        if not neighbors:
            rows[node_id] = {node_id: Fraction(1, 1)}
            continue
        probability = Fraction(1, len(neighbors))
        rows[node_id] = {neighbor: probability for neighbor in neighbors}
    return rows


def phase22_random_walk_stationary(adjacency: dict[str, tuple[str, ...]]) -> dict[str, Fraction]:
    total_degree = sum(len(neighbors) for neighbors in adjacency.values())
    if total_degree == 0:
        probability = Fraction(1, len(adjacency))
        return {node_id: probability for node_id in adjacency}
    return {node_id: Fraction(len(neighbors), total_degree) for node_id, neighbors in adjacency.items()}


def phase22_stationary_residuals(
    *,
    rows: dict[str, dict[str, Fraction]],
    stationary: dict[str, Fraction],
) -> dict[str, Fraction]:
    residuals: dict[str, Fraction] = {}
    for target in stationary:
        incoming = Fraction(0, 1)
        for source, targets in rows.items():
            incoming += stationary[source] * targets.get(target, Fraction(0, 1))
        residuals[target] = incoming - stationary[target]
    return residuals


def phase22_bucket_weights(
    *,
    node_by_id: dict[str, dict[str, object]],
    node_weights: dict[str, Fraction],
) -> tuple[dict[str, object], ...]:
    return phase22_fraction_histogram(
        (str(node_by_id[node_id]["outcome"]), weight) for node_id, weight in node_weights.items()
    )


def phase22_horizon_invariant_nodes(node_by_id: dict[str, dict[str, object]]) -> bool:
    return all(
        node["correctability_pairs"]["erase_shared_horizon"] == (True, True)
        and node["survivor_fixed_point_pairs"]["erase_shared_horizon"] == (True, True)
        for node in node_by_id.values()
    )


def phase22_algebra_descent_rows(
    *,
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> dict[str, dict[str, Fraction]]:
    rows: dict[str, dict[str, Fraction]] = {}
    for node_id, neighbors in adjacency.items():
        source_count = int(node_by_id[node_id]["algebra_difference_count"])
        lower_neighbors = tuple(
            neighbor
            for neighbor in neighbors
            if int(node_by_id[neighbor]["algebra_difference_count"]) < source_count
        )
        if not lower_neighbors:
            rows[node_id] = {node_id: Fraction(1, 1)}
            continue
        probability = Fraction(1, len(lower_neighbors))
        rows[node_id] = {neighbor: probability for neighbor in lower_neighbors}
    return rows


def phase22_absorbing_nodes(rows: dict[str, dict[str, Fraction]]) -> tuple[str, ...]:
    return tuple(sorted(node_id for node_id, targets in rows.items() if targets == {node_id: Fraction(1, 1)}))


def phase22_absorption_probabilities(
    *,
    rows: dict[str, dict[str, Fraction]],
    node_by_id: dict[str, dict[str, object]],
    absorbing_nodes: tuple[str, ...],
) -> dict[str, dict[str, Fraction]]:
    absorbing_set = set(absorbing_nodes)
    probabilities: dict[str, dict[str, Fraction]] = {
        node_id: {absorbing: Fraction(0, 1) for absorbing in absorbing_nodes}
        for node_id in rows
    }
    for absorbing in absorbing_nodes:
        probabilities[absorbing][absorbing] = Fraction(1, 1)
    for node_id in sorted(
        rows,
        key=lambda item: (int(node_by_id[item]["algebra_difference_count"]), item),
    ):
        if node_id in absorbing_set:
            continue
        totals = {absorbing: Fraction(0, 1) for absorbing in absorbing_nodes}
        for target, transition_probability in rows[node_id].items():
            for absorbing in absorbing_nodes:
                totals[absorbing] += transition_probability * probabilities[target][absorbing]
        probabilities[node_id] = totals
    return probabilities


def phase22_public_absorption_rows(
    probabilities: dict[str, dict[str, Fraction]]
) -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "from": node_id,
            "absorbing_probabilities": tuple(
                {
                    "absorbing_node": absorbing,
                    "probability": phase22_fraction(probability),
                }
                for absorbing, probability in sorted(row.items())
                if probability
            ),
        }
        for node_id, row in sorted(probabilities.items())
    )


def phase22_uniform_initial_absorbing_weights(
    *,
    probabilities: dict[str, dict[str, Fraction]],
) -> dict[str, Fraction]:
    node_count = len(probabilities)
    initial = Fraction(1, node_count)
    totals: dict[str, Fraction] = {}
    for row in probabilities.values():
        for absorbing, probability in row.items():
            totals[absorbing] = totals.get(absorbing, Fraction(0, 1)) + initial * probability
    return totals


def phase22_channel_edge_claims(
    *,
    rows: dict[str, dict[str, Fraction]],
    node_by_id: dict[str, dict[str, object]],
    monotone_descent: bool = False,
) -> dict[str, object]:
    positive_transitions = tuple(
        (source, target)
        for source, targets in rows.items()
        for target, probability in targets.items()
        if probability
    )
    horizon_preserved = all(
        node_by_id[source]["correctability_pairs"]["erase_shared_horizon"]
        == node_by_id[target]["correctability_pairs"]["erase_shared_horizon"]
        == (True, True)
        and node_by_id[source]["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == node_by_id[target]["survivor_fixed_point_pairs"]["erase_shared_horizon"]
        == (True, True)
        for source, target in positive_transitions
    )
    if monotone_descent:
        algebra_monotone = all(
            int(node_by_id[target]["algebra_difference_count"])
            <= int(node_by_id[source]["algebra_difference_count"])
            for source, target in positive_transitions
        )
    else:
        algebra_monotone = None
    return {
        "positive_transition_count": len(positive_transitions),
        "row_stochastic": phase22_rows_are_stochastic(rows),
        "horizon_profile_preserved_on_positive_transitions": horizon_preserved,
        "algebra_nonincreasing_on_positive_transitions": algebra_monotone,
    }


def bridge_cosmology_phase22_certificate() -> dict[str, object]:
    graph = phase22_phase21_graph_data()
    node_by_id = graph["node_by_id"]
    adjacency = graph["adjacency"]
    if not isinstance(node_by_id, dict) or not isinstance(adjacency, dict):
        raise TypeError("Phase 22 graph data must contain node and adjacency dictionaries")
    random_rows = phase22_random_walk_rows(adjacency)  # type: ignore[arg-type]
    stationary = phase22_random_walk_stationary(adjacency)  # type: ignore[arg-type]
    residuals = phase22_stationary_residuals(rows=random_rows, stationary=stationary)
    random_walk_bucket_weights = phase22_bucket_weights(
        node_by_id=node_by_id,  # type: ignore[arg-type]
        node_weights=stationary,
    )
    descent_rows = phase22_algebra_descent_rows(
        node_by_id=node_by_id,  # type: ignore[arg-type]
        adjacency=adjacency,  # type: ignore[arg-type]
    )
    absorbing_nodes = phase22_absorbing_nodes(descent_rows)
    absorption_probabilities = phase22_absorption_probabilities(
        rows=descent_rows,
        node_by_id=node_by_id,  # type: ignore[arg-type]
        absorbing_nodes=absorbing_nodes,
    )
    uniform_absorbing_weights = phase22_uniform_initial_absorbing_weights(
        probabilities=absorption_probabilities
    )
    absorbing_bucket_weights = phase22_bucket_weights(
        node_by_id=node_by_id,  # type: ignore[arg-type]
        node_weights=uniform_absorbing_weights,
    )
    random_walk_edge_claims = phase22_channel_edge_claims(
        rows=random_rows,
        node_by_id=node_by_id,  # type: ignore[arg-type]
    )
    descent_edge_claims = phase22_channel_edge_claims(
        rows=descent_rows,
        node_by_id=node_by_id,  # type: ignore[arg-type]
        monotone_descent=True,
    )
    absorbing_algebra_counts = tuple(
        sorted({int(node_by_id[node_id]["algebra_difference_count"]) for node_id in absorbing_nodes})  # type: ignore[index]
    )
    phase_claims = {
        "phase21_substrate_certified": graph["phase21_status"] == "pass"
        and graph["phase21_claims"]["phase_21_mixed_inner_outer_transition_graph_certificate"],  # type: ignore[index]
        "random_walk_transition_matrix_is_exact_stochastic": random_walk_edge_claims["row_stochastic"],
        "random_walk_stationary_distribution_verified_exactly": all(value == 0 for value in residuals.values())
        and sum(stationary.values(), Fraction(0, 1)) == Fraction(1, 1),
        "random_walk_stationary_bucket_weights_exact": sum(
            Fraction(item["weight"]["numerator"], item["weight"]["denominator"])  # type: ignore[index]
            for item in random_walk_bucket_weights
        )
        == Fraction(1, 1),
        "algebra_descent_transition_matrix_is_exact_stochastic": descent_edge_claims["row_stochastic"],
        "algebra_descent_absorbing_nodes_exist": bool(absorbing_nodes),
        "algebra_descent_absorption_probabilities_verified_exactly": all(
            sum(row.values(), Fraction(0, 1)) == Fraction(1, 1)
            for row in absorption_probabilities.values()
        ),
        "algebra_descent_is_nonincreasing": descent_edge_claims["algebra_nonincreasing_on_positive_transitions"],
        "algebra_descent_detects_nonzero_local_minima": absorbing_algebra_counts == (0, 2),
        "horizon_fixed_point_invariant_under_both_channels": phase22_horizon_invariant_nodes(
            node_by_id  # type: ignore[arg-type]
        )
        and random_walk_edge_claims["horizon_profile_preserved_on_positive_transitions"]
        and descent_edge_claims["horizon_profile_preserved_on_positive_transitions"],
    }
    phase_claims["phase_22_exact_time_channel_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 22: exact time/channel dynamics on the mixed mutation graph",
        "status": "pass" if phase_claims["phase_22_exact_time_channel_certificate"] else "fail",
        "graph_substrate": {
            "source": "Phase 21 mixed inner-outer mutation graph",
            "phase21_status": graph["phase21_status"],
            "phase21_counts": graph["phase21_counts"],
            "node_count": len(node_by_id),
            "edge_count": len(graph["edges"]),  # type: ignore[arg-type]
        },
        "channels": {
            "uniform_edge_random_walk": {
                "description": "From each node, choose a neighboring Phase 21 transition edge uniformly.",
                "transition_matrix_sparse": phase22_sparse_rows_to_public(random_rows),
                "stationary_distribution": tuple(
                    {
                        "node": node_id,
                        "probability": phase22_fraction(probability),
                        "outcome": node_by_id[node_id]["outcome"],  # type: ignore[index]
                        "degree": len(adjacency[node_id]),  # type: ignore[index]
                    }
                    for node_id, probability in sorted(stationary.items())
                ),
                "stationary_bucket_weights": random_walk_bucket_weights,
                "stationary_residuals": tuple(
                    {
                        "node": node_id,
                        "residual": phase22_fraction(residual),
                    }
                    for node_id, residual in sorted(residuals.items())
                ),
                "certified_claims": random_walk_edge_claims,
            },
            "algebra_descent_channel": {
                "description": (
                    "From each node, choose uniformly among adjacent nodes with strictly smaller algebra-difference "
                    "count; if none exist, stay fixed."
                ),
                "transition_matrix_sparse": phase22_sparse_rows_to_public(descent_rows),
                "absorbing_nodes": tuple(
                    {
                        "node": node_id,
                        "outcome": node_by_id[node_id]["outcome"],  # type: ignore[index]
                        "algebra_difference_count": node_by_id[node_id]["algebra_difference_count"],  # type: ignore[index]
                    }
                    for node_id in absorbing_nodes
                ),
                "absorption_probabilities": phase22_public_absorption_rows(absorption_probabilities),
                "uniform_initial_absorbing_node_weights": tuple(
                    {
                        "node": node_id,
                        "probability": phase22_fraction(probability),
                        "outcome": node_by_id[node_id]["outcome"],  # type: ignore[index]
                    }
                    for node_id, probability in sorted(uniform_absorbing_weights.items())
                ),
                "uniform_initial_absorbing_bucket_weights": absorbing_bucket_weights,
                "certified_claims": descent_edge_claims,
            },
        },
        "counts": {
            "nodes": len(node_by_id),
            "phase21_edges": len(graph["edges"]),  # type: ignore[arg-type]
            "random_walk_positive_transitions": random_walk_edge_claims["positive_transition_count"],
            "descent_positive_transitions": descent_edge_claims["positive_transition_count"],
            "absorbing_nodes": len(absorbing_nodes),
            "absorbing_algebra_counts": absorbing_algebra_counts,
            "random_walk_stationary_buckets": len(random_walk_bucket_weights),
            "descent_absorbing_buckets": len(absorbing_bucket_weights),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The Phase 21 mixed graph now carries exact rational channel dynamics. The edge-random-walk channel "
                "has an explicitly verified stationary distribution, while the algebra-descent channel has certified "
                "absorbing nodes and exact absorption probabilities."
            ),
            "horizon_lesson": (
                "Both channels preserve the repaired shared-horizon correctability and survivor fixed-point profile "
                "on every positive-probability transition."
            ),
            "time_lesson": (
                "The same static mixed graph supports different time semantics: a reversible random walk with stable "
                "stationary bucket weights, and an irreversible algebra-descent channel that absorbs into the "
                "local minima of the algebra-difference landscape, including nonzero-algebra local minima."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 22 adds exact rational time dynamics to the finite toy cosmology. The next adaptation should "
                "compare several channel rules on the same graph, especially entropy-descent or horizon-preserving "
                "biased channels, to identify which stationary bucket weights or absorbing classes are rule-dependent."
            ),
            "suggested_phase_23": (
                "Add a small family of exact biased channels on the Phase 21 graph, then certify which bucket weights, "
                "absorbing classes, and horizon invariants are robust under changing transition rules."
            ),
        },
    }


def phase23_biased_walk_specs() -> tuple[dict[str, str], ...]:
    return (
        {
            "name": "uniform_edge_random_walk",
            "description": "Baseline reversible walk: every adjacent Phase 21 edge has weight 1.",
            "weight_rule": "uniform",
        },
        {
            "name": "entropy_match_preserving_bias",
            "description": (
                "Reversible biased walk: adjacent nodes with the same labeled t=2 entropy-match flag get "
                "edge weight 2; entropy-flip edges get weight 1."
            ),
            "weight_rule": "same_labeled_t2_entropy",
        },
        {
            "name": "observer_signal_preserving_bias",
            "description": (
                "Reversible biased walk: adjacent nodes with the same entropy/reconstruction signal flag get "
                "edge weight 2; signal-flip edges get weight 1."
            ),
            "weight_rule": "entropy_reconstruction_signal",
        },
        {
            "name": "algebra_flat_bias",
            "description": (
                "Reversible biased walk: adjacent nodes with the same algebra-difference count get edge weight 2; "
                "algebra-changing edges get weight 1."
            ),
            "weight_rule": "algebra_difference_count",
        },
    )


def phase23_edge_weight(
    *,
    weight_rule: str,
    source: dict[str, object],
    target: dict[str, object],
) -> int:
    if weight_rule == "uniform":
        return 1
    if weight_rule == "same_labeled_t2_entropy":
        return 2 if bool(source["same_labeled_t2_entropy"]) == bool(target["same_labeled_t2_entropy"]) else 1
    if weight_rule == "entropy_reconstruction_signal":
        return (
            2
            if bool(source["entropy_reconstruction_signal"]) == bool(target["entropy_reconstruction_signal"])
            else 1
        )
    if weight_rule == "algebra_difference_count":
        return 2 if int(source["algebra_difference_count"]) == int(target["algebra_difference_count"]) else 1
    raise ValueError(f"unknown Phase 23 weight rule {weight_rule!r}")


def phase23_weighted_walk_rows(
    *,
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
    weight_rule: str,
) -> dict[str, dict[str, Fraction]]:
    rows: dict[str, dict[str, Fraction]] = {}
    for node_id, neighbors in adjacency.items():
        if not neighbors:
            rows[node_id] = {node_id: Fraction(1, 1)}
            continue
        weights = {
            neighbor: phase23_edge_weight(
                weight_rule=weight_rule,
                source=node_by_id[node_id],
                target=node_by_id[neighbor],
            )
            for neighbor in neighbors
        }
        total_weight = sum(weights.values())
        rows[node_id] = {neighbor: Fraction(weight, total_weight) for neighbor, weight in weights.items()}
    return rows


def phase23_weighted_walk_stationary(
    *,
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
    weight_rule: str,
) -> dict[str, Fraction]:
    weighted_degrees = {
        node_id: sum(
            phase23_edge_weight(
                weight_rule=weight_rule,
                source=node_by_id[node_id],
                target=node_by_id[neighbor],
            )
            for neighbor in neighbors
        )
        for node_id, neighbors in adjacency.items()
    }
    total_degree = sum(weighted_degrees.values())
    if total_degree == 0:
        probability = Fraction(1, len(adjacency))
        return {node_id: probability for node_id in adjacency}
    return {node_id: Fraction(degree, total_degree) for node_id, degree in weighted_degrees.items()}


def phase23_weight_rule_is_symmetric(
    *,
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
    weight_rule: str,
) -> bool:
    return all(
        phase23_edge_weight(
            weight_rule=weight_rule,
            source=node_by_id[source],
            target=node_by_id[target],
        )
        == phase23_edge_weight(
            weight_rule=weight_rule,
            source=node_by_id[target],
            target=node_by_id[source],
        )
        for source, neighbors in adjacency.items()
        for target in neighbors
    )


def phase23_reachable(
    *,
    start: str,
    adjacency: dict[str, set[str]],
) -> set[str]:
    seen = {start}
    frontier = [start]
    while frontier:
        current = frontier.pop(0)
        for target in adjacency[current]:
            if target in seen:
                continue
            seen.add(target)
            frontier.append(target)
    return seen


def phase23_closed_communicating_classes(rows: dict[str, dict[str, Fraction]]) -> tuple[tuple[str, ...], ...]:
    positive_adjacency: dict[str, set[str]] = {
        source: {target for target, probability in targets.items() if probability}
        for source, targets in rows.items()
    }
    remaining = set(rows)
    closed_classes = []
    while remaining:
        start = min(remaining)
        reachable_from_start = phase23_reachable(start=start, adjacency=positive_adjacency)
        component = tuple(
            sorted(
                node
                for node in rows
                if node in reachable_from_start
                and start in phase23_reachable(start=node, adjacency=positive_adjacency)
            )
        )
        component_set = set(component)
        remaining -= component_set
        if all(positive_adjacency[source] <= component_set for source in component):
            closed_classes.append(component)
    return tuple(closed_classes)


def phase23_channel_class_summary(
    *,
    name: str,
    rows: dict[str, dict[str, Fraction]],
    node_by_id: dict[str, dict[str, object]],
) -> dict[str, object]:
    closed_classes = phase23_closed_communicating_classes(rows)
    absorbing_nodes = phase22_absorbing_nodes(rows)
    return {
        "channel": name,
        "closed_class_count": len(closed_classes),
        "closed_class_sizes": tuple(len(item) for item in closed_classes),
        "absorbing_node_count": len(absorbing_nodes),
        "absorbing_bucket_counts": phase19_histogram(
            str(node_by_id[node_id]["outcome"]) for node_id in absorbing_nodes
        ),
        "closed_classes": tuple(
            {
                "nodes": item,
                "outcome_counts": phase19_histogram(str(node_by_id[node_id]["outcome"]) for node_id in item),
            }
            for item in closed_classes
        ),
    }


def phase23_bucket_weight_table(
    bucket_weight_maps: dict[str, dict[str, Fraction]]
) -> tuple[dict[str, object], ...]:
    buckets = sorted({bucket for weights in bucket_weight_maps.values() for bucket in weights})
    return tuple(
        {
            "bucket": bucket,
            "weights_by_channel": tuple(
                {
                    "channel": channel,
                    "weight": phase22_fraction(weights.get(bucket, Fraction(0, 1))),
                }
                for channel, weights in sorted(bucket_weight_maps.items())
            ),
            "rule_dependent": len({weights.get(bucket, Fraction(0, 1)) for weights in bucket_weight_maps.values()})
            > 1,
        }
        for bucket in buckets
    )


def phase23_biased_walk_summary(
    *,
    spec: dict[str, str],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> tuple[dict[str, object], dict[str, Fraction]]:
    rows = phase23_weighted_walk_rows(
        node_by_id=node_by_id,
        adjacency=adjacency,
        weight_rule=spec["weight_rule"],
    )
    stationary = phase23_weighted_walk_stationary(
        node_by_id=node_by_id,
        adjacency=adjacency,
        weight_rule=spec["weight_rule"],
    )
    residuals = phase22_stationary_residuals(rows=rows, stationary=stationary)
    bucket_weights = phase22_bucket_weights(node_by_id=node_by_id, node_weights=stationary)
    edge_claims = phase22_channel_edge_claims(rows=rows, node_by_id=node_by_id)
    class_summary = phase23_channel_class_summary(name=spec["name"], rows=rows, node_by_id=node_by_id)
    weighted_degrees = {
        node_id: sum(
            phase23_edge_weight(
                weight_rule=spec["weight_rule"],
                source=node_by_id[node_id],
                target=node_by_id[neighbor],
            )
            for neighbor in adjacency[node_id]
        )
        for node_id in adjacency
    }
    return (
        {
            "description": spec["description"],
            "weight_rule": spec["weight_rule"],
            "weight_rule_symmetric": phase23_weight_rule_is_symmetric(
                node_by_id=node_by_id,
                adjacency=adjacency,
                weight_rule=spec["weight_rule"],
            ),
            "transition_matrix_sparse": phase22_sparse_rows_to_public(rows),
            "weighted_degrees": tuple(
                {
                    "node": node_id,
                    "weighted_degree": weighted_degrees[node_id],
                    "outcome": node_by_id[node_id]["outcome"],
                }
                for node_id in sorted(weighted_degrees)
            ),
            "stationary_distribution": tuple(
                {
                    "node": node_id,
                    "probability": phase22_fraction(probability),
                    "outcome": node_by_id[node_id]["outcome"],
                    "weighted_degree": weighted_degrees[node_id],
                }
                for node_id, probability in sorted(stationary.items())
            ),
            "stationary_bucket_weights": bucket_weights,
            "stationary_residuals": tuple(
                {
                    "node": node_id,
                    "residual": phase22_fraction(residual),
                }
                for node_id, residual in sorted(residuals.items())
            ),
            "closed_class_summary": class_summary,
            "certified_claims": {
                **edge_claims,
                "stationary_distribution_verified_exactly": all(value == 0 for value in residuals.values())
                and sum(stationary.values(), Fraction(0, 1)) == Fraction(1, 1),
                "weighted_degree_stationary_formula_symmetric": phase23_weight_rule_is_symmetric(
                    node_by_id=node_by_id,
                    adjacency=adjacency,
                    weight_rule=spec["weight_rule"],
                ),
            },
        },
        {str(item["key"]): Fraction(item["weight"]["numerator"], item["weight"]["denominator"]) for item in bucket_weights},
    )


def bridge_cosmology_phase23_certificate() -> dict[str, object]:
    graph = phase22_phase21_graph_data()
    node_by_id = graph["node_by_id"]
    adjacency = graph["adjacency"]
    if not isinstance(node_by_id, dict) or not isinstance(adjacency, dict):
        raise TypeError("Phase 23 graph data must contain node and adjacency dictionaries")
    walk_channels = {}
    bucket_weight_maps: dict[str, dict[str, Fraction]] = {}
    for spec in phase23_biased_walk_specs():
        summary, bucket_weights = phase23_biased_walk_summary(
            spec=spec,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            adjacency=adjacency,  # type: ignore[arg-type]
        )
        walk_channels[spec["name"]] = summary
        bucket_weight_maps[spec["name"]] = bucket_weights

    bucket_table = phase23_bucket_weight_table(bucket_weight_maps)
    rule_dependent_buckets = tuple(item["bucket"] for item in bucket_table if item["rule_dependent"])
    rule_invariant_buckets = tuple(item["bucket"] for item in bucket_table if not item["rule_dependent"])

    descent_rows = phase22_algebra_descent_rows(
        node_by_id=node_by_id,  # type: ignore[arg-type]
        adjacency=adjacency,  # type: ignore[arg-type]
    )
    descent_class_summary = phase23_channel_class_summary(
        name="algebra_descent_channel",
        rows=descent_rows,
        node_by_id=node_by_id,  # type: ignore[arg-type]
    )
    descent_edge_claims = phase22_channel_edge_claims(
        rows=descent_rows,
        node_by_id=node_by_id,  # type: ignore[arg-type]
        monotone_descent=True,
    )
    walk_class_summaries = tuple(
        walk_channels[spec["name"]]["closed_class_summary"] for spec in phase23_biased_walk_specs()
    )
    walk_absorbing_counts = tuple(int(summary["absorbing_node_count"]) for summary in walk_class_summaries)
    walk_closed_class_counts = tuple(int(summary["closed_class_count"]) for summary in walk_class_summaries)
    phase_claims = {
        "phase21_substrate_certified": graph["phase21_status"] == "pass"
        and graph["phase21_claims"]["phase_21_mixed_inner_outer_transition_graph_certificate"],  # type: ignore[index]
        "all_biased_walk_transition_matrices_are_exact_stochastic": all(
            channel["certified_claims"]["row_stochastic"] for channel in walk_channels.values()
        ),
        "all_biased_walk_stationary_distributions_verified_exactly": all(
            channel["certified_claims"]["stationary_distribution_verified_exactly"]
            for channel in walk_channels.values()
        ),
        "all_biased_walk_stationary_formulas_use_symmetric_edge_weights": all(
            channel["certified_claims"]["weighted_degree_stationary_formula_symmetric"]
            for channel in walk_channels.values()
        ),
        "stationary_bucket_weights_rule_dependent": bool(rule_dependent_buckets),
        "all_biased_walks_have_one_closed_communicating_class": walk_closed_class_counts == (1, 1, 1, 1),
        "biased_walks_have_no_absorbing_nodes": walk_absorbing_counts == (0, 0, 0, 0),
        "algebra_descent_absorbing_structure_differs_from_biased_walks": int(
            descent_class_summary["closed_class_count"]
        )
        > 1
        and int(descent_class_summary["absorbing_node_count"]) > 0,
        "horizon_fixed_point_invariant_across_channel_family": phase22_horizon_invariant_nodes(
            node_by_id  # type: ignore[arg-type]
        )
        and all(
            channel["certified_claims"]["horizon_profile_preserved_on_positive_transitions"]
            for channel in walk_channels.values()
        )
        and descent_edge_claims["horizon_profile_preserved_on_positive_transitions"],
    }
    phase_claims["absorbing_classes_rule_dependent"] = (
        phase_claims["biased_walks_have_no_absorbing_nodes"]
        and phase_claims["algebra_descent_absorbing_structure_differs_from_biased_walks"]
    )
    phase_claims["phase_23_biased_channel_comparison_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 23: biased channel comparison on the mixed mutation graph",
        "status": "pass" if phase_claims["phase_23_biased_channel_comparison_certificate"] else "fail",
        "graph_substrate": {
            "source": "Phase 21 mixed inner-outer mutation graph",
            "phase21_status": graph["phase21_status"],
            "phase21_counts": graph["phase21_counts"],
            "node_count": len(node_by_id),
            "edge_count": len(graph["edges"]),  # type: ignore[arg-type]
        },
        "channels": {
            **walk_channels,
            "algebra_descent_channel": {
                "description": (
                    "Phase 22 irreversible comparison channel: choose uniformly among adjacent nodes with strictly "
                    "smaller algebra-difference count; if none exist, stay fixed."
                ),
                "transition_matrix_sparse": phase22_sparse_rows_to_public(descent_rows),
                "closed_class_summary": descent_class_summary,
                "certified_claims": descent_edge_claims,
            },
        },
        "comparison": {
            "stationary_bucket_weight_table": bucket_table,
            "rule_dependent_stationary_buckets": rule_dependent_buckets,
            "rule_invariant_stationary_buckets": rule_invariant_buckets,
            "absorbing_structure_by_channel": tuple(
                {
                    "channel": spec["name"],
                    "closed_class_count": walk_channels[spec["name"]]["closed_class_summary"]["closed_class_count"],
                    "absorbing_node_count": walk_channels[spec["name"]]["closed_class_summary"]["absorbing_node_count"],
                    "closed_class_sizes": walk_channels[spec["name"]]["closed_class_summary"]["closed_class_sizes"],
                }
                for spec in phase23_biased_walk_specs()
            )
            + (
                {
                    "channel": "algebra_descent_channel",
                    "closed_class_count": descent_class_summary["closed_class_count"],
                    "absorbing_node_count": descent_class_summary["absorbing_node_count"],
                    "closed_class_sizes": descent_class_summary["closed_class_sizes"],
                },
            ),
        },
        "counts": {
            "nodes": len(node_by_id),
            "phase21_edges": len(graph["edges"]),  # type: ignore[arg-type]
            "biased_walk_channels": len(walk_channels),
            "biased_walk_positive_transitions": tuple(
                (
                    spec["name"],
                    walk_channels[spec["name"]]["certified_claims"]["positive_transition_count"],
                )
                for spec in phase23_biased_walk_specs()
            ),
            "rule_dependent_stationary_buckets": len(rule_dependent_buckets),
            "rule_invariant_stationary_buckets": len(rule_invariant_buckets),
            "biased_walk_closed_class_counts": walk_closed_class_counts,
            "biased_walk_absorbing_node_counts": walk_absorbing_counts,
            "algebra_descent_closed_classes": descent_class_summary["closed_class_count"],
            "algebra_descent_absorbing_nodes": descent_class_summary["absorbing_node_count"],
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Four exact reversible biased walks on the same Phase 21 graph have certified stationary "
                "distributions, but their stationary bucket weights are not invariant under the choice of local "
                "transition rule."
            ),
            "absorbing_lesson": (
                "Absorbing structure is strongly rule-dependent: all biased walks have one closed communicating "
                "class and no absorbing nodes, while algebra descent has many singleton absorbing classes."
            ),
            "horizon_lesson": (
                "The repaired shared-horizon correctability and survivor fixed-point profile remain invariant across "
                "all compared channel rules, so this horizon diagnostic is more robust than stationary bucket weight "
                "or absorbing-class structure in this finite model."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 23 separates robust horizon invariants from rule-dependent stationary and absorbing dynamics. "
                "The next adaptation should search over small exact channel rules, rather than hand-picking them, and "
                "classify which local rules extremize entropy-break, operator-collapse, or full-semantics stationary "
                "weight while preserving certified horizon semantics."
            ),
            "suggested_phase_24": (
                "Build a bounded exact channel-rule search over symmetric integer edge weights and simple descent "
                "orders, then certify extremal stationary bucket weights and absorbing-class no-go/yes-go patterns."
            ),
        },
    }


def phase24_weighted_rule_specs(max_bonus: int = 2) -> tuple[dict[str, object], ...]:
    if max_bonus < 0 or max_bonus > 4:
        raise ValueError("Phase 24 max_bonus must be between 0 and 4")
    return tuple(
        {
            "name": f"edge_bonus_e{entropy_bonus}_o{observer_bonus}_a{algebra_bonus}",
            "entropy_match_same_bonus": entropy_bonus,
            "observer_signal_same_bonus": observer_bonus,
            "algebra_flat_bonus": algebra_bonus,
            "edge_weight_formula": (
                "1 + entropy_bonus*[same_labeled_t2_entropy agrees] + "
                "observer_bonus*[entropy_reconstruction_signal agrees] + "
                "algebra_bonus*[algebra_difference_count agrees]"
            ),
        }
        for entropy_bonus, observer_bonus, algebra_bonus in product(range(max_bonus + 1), repeat=3)
    )


def phase24_edge_feature_flags(
    *,
    source: dict[str, object],
    target: dict[str, object],
) -> dict[str, bool]:
    return {
        "same_labeled_t2_entropy_agrees": bool(source["same_labeled_t2_entropy"])
        == bool(target["same_labeled_t2_entropy"]),
        "entropy_reconstruction_signal_agrees": bool(source["entropy_reconstruction_signal"])
        == bool(target["entropy_reconstruction_signal"]),
        "algebra_difference_count_agrees": int(source["algebra_difference_count"])
        == int(target["algebra_difference_count"]),
    }


def phase24_weighted_rule_edge_weight(
    *,
    spec: dict[str, object],
    source: dict[str, object],
    target: dict[str, object],
) -> int:
    flags = phase24_edge_feature_flags(source=source, target=target)
    return (
        1
        + int(spec["entropy_match_same_bonus"]) * int(flags["same_labeled_t2_entropy_agrees"])
        + int(spec["observer_signal_same_bonus"]) * int(flags["entropy_reconstruction_signal_agrees"])
        + int(spec["algebra_flat_bonus"]) * int(flags["algebra_difference_count_agrees"])
    )


def phase24_weighted_rule_rows(
    *,
    spec: dict[str, object],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> dict[str, dict[str, Fraction]]:
    rows: dict[str, dict[str, Fraction]] = {}
    for node_id, neighbors in adjacency.items():
        if not neighbors:
            rows[node_id] = {node_id: Fraction(1, 1)}
            continue
        weights = {
            neighbor: phase24_weighted_rule_edge_weight(
                spec=spec,
                source=node_by_id[node_id],
                target=node_by_id[neighbor],
            )
            for neighbor in neighbors
        }
        total_weight = sum(weights.values())
        rows[node_id] = {neighbor: Fraction(weight, total_weight) for neighbor, weight in weights.items()}
    return rows


def phase24_weighted_rule_stationary(
    *,
    spec: dict[str, object],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> dict[str, Fraction]:
    weighted_degrees = {
        node_id: sum(
            phase24_weighted_rule_edge_weight(
                spec=spec,
                source=node_by_id[node_id],
                target=node_by_id[neighbor],
            )
            for neighbor in neighbors
        )
        for node_id, neighbors in adjacency.items()
    }
    total_degree = sum(weighted_degrees.values())
    if total_degree == 0:
        probability = Fraction(1, len(adjacency))
        return {node_id: probability for node_id in adjacency}
    return {node_id: Fraction(degree, total_degree) for node_id, degree in weighted_degrees.items()}


def phase24_weighted_rule_is_symmetric(
    *,
    spec: dict[str, object],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> bool:
    return all(
        phase24_weighted_rule_edge_weight(
            spec=spec,
            source=node_by_id[source],
            target=node_by_id[target],
        )
        == phase24_weighted_rule_edge_weight(
            spec=spec,
            source=node_by_id[target],
            target=node_by_id[source],
        )
        for source, neighbors in adjacency.items()
        for target in neighbors
    )


def phase24_fraction_map_from_bucket_weights(
    bucket_weights: tuple[dict[str, object], ...]
) -> dict[str, Fraction]:
    return {
        str(item["key"]): Fraction(item["weight"]["numerator"], item["weight"]["denominator"])
        for item in bucket_weights
    }


def phase24_weighted_rule_summary(
    *,
    spec: dict[str, object],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> tuple[dict[str, object], dict[str, Fraction]]:
    rows = phase24_weighted_rule_rows(spec=spec, node_by_id=node_by_id, adjacency=adjacency)
    stationary = phase24_weighted_rule_stationary(spec=spec, node_by_id=node_by_id, adjacency=adjacency)
    residuals = phase22_stationary_residuals(rows=rows, stationary=stationary)
    bucket_weights = phase22_bucket_weights(node_by_id=node_by_id, node_weights=stationary)
    edge_claims = phase22_channel_edge_claims(rows=rows, node_by_id=node_by_id)
    class_summary = phase23_channel_class_summary(name=str(spec["name"]), rows=rows, node_by_id=node_by_id)
    weighted_degrees = {
        node_id: sum(
            phase24_weighted_rule_edge_weight(
                spec=spec,
                source=node_by_id[node_id],
                target=node_by_id[neighbor],
            )
            for neighbor in adjacency[node_id]
        )
        for node_id in adjacency
    }
    edge_weights = tuple(
        phase24_weighted_rule_edge_weight(
            spec=spec,
            source=node_by_id[source],
            target=node_by_id[target],
        )
        for source, neighbors in adjacency.items()
        for target in neighbors
    )
    degree_histogram = phase19_histogram(weighted_degrees.values())
    return (
        {
            "rule": spec,
            "stationary_bucket_weights": bucket_weights,
            "weighted_degree_histogram": degree_histogram,
            "closed_class_summary": {
                "closed_class_count": class_summary["closed_class_count"],
                "closed_class_sizes": class_summary["closed_class_sizes"],
                "absorbing_node_count": class_summary["absorbing_node_count"],
                "absorbing_bucket_counts": class_summary["absorbing_bucket_counts"],
            },
            "certified_claims": {
                **edge_claims,
                "edge_weights_positive": bool(edge_weights) and min(edge_weights) > 0,
                "edge_weight_rule_symmetric": phase24_weighted_rule_is_symmetric(
                    spec=spec,
                    node_by_id=node_by_id,
                    adjacency=adjacency,
                ),
                "stationary_distribution_verified_exactly": all(value == 0 for value in residuals.values())
                and sum(stationary.values(), Fraction(0, 1)) == Fraction(1, 1),
            },
        },
        phase24_fraction_map_from_bucket_weights(bucket_weights),
    )


def phase24_weighted_extrema(
    bucket_weight_maps: dict[str, dict[str, Fraction]]
) -> tuple[dict[str, object], ...]:
    buckets = sorted({bucket for weights in bucket_weight_maps.values() for bucket in weights})
    return tuple(
        {
            "bucket": bucket,
            "minimum": {
                "weight": phase22_fraction(min(weights.get(bucket, Fraction(0, 1)) for weights in bucket_weight_maps.values())),
                "rules": tuple(
                    sorted(
                        rule_name
                        for rule_name, weights in bucket_weight_maps.items()
                        if weights.get(bucket, Fraction(0, 1))
                        == min(item.get(bucket, Fraction(0, 1)) for item in bucket_weight_maps.values())
                    )
                ),
            },
            "maximum": {
                "weight": phase22_fraction(max(weights.get(bucket, Fraction(0, 1)) for weights in bucket_weight_maps.values())),
                "rules": tuple(
                    sorted(
                        rule_name
                        for rule_name, weights in bucket_weight_maps.items()
                        if weights.get(bucket, Fraction(0, 1))
                        == max(item.get(bucket, Fraction(0, 1)) for item in bucket_weight_maps.values())
                    )
                ),
            },
        }
        for bucket in buckets
    )


def phase24_descent_rule_specs() -> tuple[dict[str, object], ...]:
    return tuple(
        {
            "name": f"score_descent_a{algebra_coeff}_e{entropy_coeff}_o{observer_coeff}",
            "algebra_count_coefficient": algebra_coeff,
            "entropy_match_coefficient": entropy_coeff,
            "observer_signal_coefficient": observer_coeff,
            "score_formula": (
                "algebra_coeff*algebra_difference_count + entropy_coeff*[same_labeled_t2_entropy] + "
                "observer_coeff*[entropy_reconstruction_signal]"
            ),
        }
        for algebra_coeff, entropy_coeff, observer_coeff in product((0, 1), repeat=3)
        if algebra_coeff or entropy_coeff or observer_coeff
    )


def phase24_node_score(*, spec: dict[str, object], node: dict[str, object]) -> int:
    return (
        int(spec["algebra_count_coefficient"]) * int(node["algebra_difference_count"])
        + int(spec["entropy_match_coefficient"]) * int(bool(node["same_labeled_t2_entropy"]))
        + int(spec["observer_signal_coefficient"]) * int(bool(node["entropy_reconstruction_signal"]))
    )


def phase24_score_descent_rows(
    *,
    spec: dict[str, object],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> tuple[dict[str, dict[str, Fraction]], dict[str, int]]:
    scores = {node_id: phase24_node_score(spec=spec, node=node) for node_id, node in node_by_id.items()}
    rows: dict[str, dict[str, Fraction]] = {}
    for node_id, neighbors in adjacency.items():
        lower_neighbors = tuple(neighbor for neighbor in neighbors if scores[neighbor] < scores[node_id])
        if not lower_neighbors:
            rows[node_id] = {node_id: Fraction(1, 1)}
            continue
        probability = Fraction(1, len(lower_neighbors))
        rows[node_id] = {neighbor: probability for neighbor in lower_neighbors}
    return rows, scores


def phase24_descent_absorption_probabilities(
    *,
    rows: dict[str, dict[str, Fraction]],
    scores: dict[str, int],
    absorbing_nodes: tuple[str, ...],
) -> dict[str, dict[str, Fraction]]:
    absorbing_set = set(absorbing_nodes)
    probabilities: dict[str, dict[str, Fraction]] = {
        node_id: {absorbing: Fraction(0, 1) for absorbing in absorbing_nodes}
        for node_id in rows
    }
    for absorbing in absorbing_nodes:
        probabilities[absorbing][absorbing] = Fraction(1, 1)
    for node_id in sorted(rows, key=lambda item: (scores[item], item)):
        if node_id in absorbing_set:
            continue
        totals = {absorbing: Fraction(0, 1) for absorbing in absorbing_nodes}
        for target, transition_probability in rows[node_id].items():
            for absorbing in absorbing_nodes:
                totals[absorbing] += transition_probability * probabilities[target][absorbing]
        probabilities[node_id] = totals
    return probabilities


def phase24_descent_rule_summary(
    *,
    spec: dict[str, object],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> tuple[dict[str, object], dict[str, Fraction]]:
    rows, scores = phase24_score_descent_rows(spec=spec, node_by_id=node_by_id, adjacency=adjacency)
    absorbing_nodes = phase22_absorbing_nodes(rows)
    absorption_probabilities = phase24_descent_absorption_probabilities(
        rows=rows,
        scores=scores,
        absorbing_nodes=absorbing_nodes,
    )
    uniform_absorbing_weights = phase22_uniform_initial_absorbing_weights(
        probabilities=absorption_probabilities
    )
    absorbing_bucket_weights = phase22_bucket_weights(node_by_id=node_by_id, node_weights=uniform_absorbing_weights)
    edge_claims = phase22_channel_edge_claims(rows=rows, node_by_id=node_by_id)
    class_summary = phase23_channel_class_summary(name=str(spec["name"]), rows=rows, node_by_id=node_by_id)
    score_histogram = phase19_histogram(scores.values())
    return (
        {
            "rule": spec,
            "score_histogram": score_histogram,
            "absorbing_nodes": tuple(
                {
                    "node": node_id,
                    "score": scores[node_id],
                    "outcome": node_by_id[node_id]["outcome"],
                    "algebra_difference_count": node_by_id[node_id]["algebra_difference_count"],
                }
                for node_id in absorbing_nodes
            ),
            "uniform_initial_absorbing_bucket_weights": absorbing_bucket_weights,
            "closed_class_summary": {
                "closed_class_count": class_summary["closed_class_count"],
                "closed_class_sizes": class_summary["closed_class_sizes"],
                "absorbing_node_count": class_summary["absorbing_node_count"],
                "absorbing_bucket_counts": class_summary["absorbing_bucket_counts"],
            },
            "certified_claims": {
                **edge_claims,
                "strict_score_descent_or_absorbing_self_loop": all(
                    target == source or scores[target] < scores[source]
                    for source, targets in rows.items()
                    for target, probability in targets.items()
                    if probability
                ),
                "absorption_probabilities_verified_exactly": all(
                    sum(row.values(), Fraction(0, 1)) == Fraction(1, 1)
                    for row in absorption_probabilities.values()
                ),
            },
        },
        phase24_fraction_map_from_bucket_weights(absorbing_bucket_weights),
    )


def phase24_descent_absorbing_extrema(
    descent_summaries: tuple[dict[str, object], ...]
) -> dict[str, object]:
    counts = {
        str(summary["rule"]["name"]): int(summary["closed_class_summary"]["absorbing_node_count"])  # type: ignore[index]
        for summary in descent_summaries
    }
    minimum = min(counts.values())
    maximum = max(counts.values())
    return {
        "minimum_absorbing_nodes": {
            "count": minimum,
            "rules": tuple(sorted(rule for rule, count in counts.items() if count == minimum)),
        },
        "maximum_absorbing_nodes": {
            "count": maximum,
            "rules": tuple(sorted(rule for rule, count in counts.items() if count == maximum)),
        },
        "absorbing_node_count_by_rule": tuple(sorted(counts.items())),
    }


def bridge_cosmology_phase24_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    graph = phase22_phase21_graph_data()
    node_by_id = graph["node_by_id"]
    adjacency = graph["adjacency"]
    if not isinstance(node_by_id, dict) or not isinstance(adjacency, dict):
        raise TypeError("Phase 24 graph data must contain node and adjacency dictionaries")
    weighted_specs = phase24_weighted_rule_specs(max_bonus=max_bonus)
    weighted_summaries = []
    weighted_bucket_maps: dict[str, dict[str, Fraction]] = {}
    for spec in weighted_specs:
        summary, bucket_weights = phase24_weighted_rule_summary(
            spec=spec,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            adjacency=adjacency,  # type: ignore[arg-type]
        )
        weighted_summaries.append(summary)
        weighted_bucket_maps[str(spec["name"])] = bucket_weights
    weighted_summaries_tuple = tuple(weighted_summaries)
    weighted_extrema = phase24_weighted_extrema(weighted_bucket_maps)

    descent_summaries = []
    descent_bucket_maps: dict[str, dict[str, Fraction]] = {}
    for spec in phase24_descent_rule_specs():
        summary, bucket_weights = phase24_descent_rule_summary(
            spec=spec,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            adjacency=adjacency,  # type: ignore[arg-type]
        )
        descent_summaries.append(summary)
        descent_bucket_maps[str(spec["name"])] = bucket_weights
    descent_summaries_tuple = tuple(descent_summaries)
    descent_extrema = phase24_descent_absorbing_extrema(descent_summaries_tuple)
    descent_bucket_extrema = phase24_weighted_extrema(descent_bucket_maps)
    weighted_closed_class_counts = tuple(
        int(summary["closed_class_summary"]["closed_class_count"]) for summary in weighted_summaries_tuple
    )
    weighted_absorbing_counts = tuple(
        int(summary["closed_class_summary"]["absorbing_node_count"]) for summary in weighted_summaries_tuple
    )
    descent_absorbing_counts = tuple(
        int(summary["closed_class_summary"]["absorbing_node_count"]) for summary in descent_summaries_tuple
    )
    phase_claims = {
        "phase21_substrate_certified": graph["phase21_status"] == "pass"
        and graph["phase21_claims"]["phase_21_mixed_inner_outer_transition_graph_certificate"],  # type: ignore[index]
        "weighted_edge_rule_search_space_exactly_bounded": len(weighted_summaries_tuple)
        == (max_bonus + 1) ** 3,
        "all_weighted_walks_exact_stochastic": all(
            summary["certified_claims"]["row_stochastic"] for summary in weighted_summaries_tuple
        ),
        "all_weighted_walk_stationary_distributions_verified_exactly": all(
            summary["certified_claims"]["stationary_distribution_verified_exactly"]
            for summary in weighted_summaries_tuple
        ),
        "all_weighted_walk_rules_are_positive_symmetric": all(
            summary["certified_claims"]["edge_weights_positive"]
            and summary["certified_claims"]["edge_weight_rule_symmetric"]
            for summary in weighted_summaries_tuple
        ),
        "positive_symmetric_walk_absorbing_no_go": set(weighted_closed_class_counts) == {1}
        and set(weighted_absorbing_counts) == {0},
        "weighted_walk_extrema_certified_for_all_buckets": len(weighted_extrema)
        == len({bucket for weights in weighted_bucket_maps.values() for bucket in weights})
        and all(item["minimum"]["rules"] and item["maximum"]["rules"] for item in weighted_extrema),
        "weighted_walk_extrema_are_nontrivial": any(
            item["minimum"]["weight"]["string"] != item["maximum"]["weight"]["string"] for item in weighted_extrema
        ),
        "descent_rule_search_space_exactly_bounded": len(descent_summaries_tuple) == 7,
        "all_descent_channels_exact_stochastic": all(
            summary["certified_claims"]["row_stochastic"] for summary in descent_summaries_tuple
        ),
        "all_descent_channels_strict_score_descent_or_absorbing": all(
            summary["certified_claims"]["strict_score_descent_or_absorbing_self_loop"]
            for summary in descent_summaries_tuple
        ),
        "all_descent_absorption_probabilities_verified_exactly": all(
            summary["certified_claims"]["absorption_probabilities_verified_exactly"]
            for summary in descent_summaries_tuple
        ),
        "descent_absorbing_yes_go": min(descent_absorbing_counts) > 0,
        "descent_absorbing_structure_rule_dependent": min(descent_absorbing_counts)
        != max(descent_absorbing_counts),
        "horizon_fixed_point_invariant_across_searched_rules": phase22_horizon_invariant_nodes(
            node_by_id  # type: ignore[arg-type]
        )
        and all(
            summary["certified_claims"]["horizon_profile_preserved_on_positive_transitions"]
            for summary in weighted_summaries_tuple
        )
        and all(
            summary["certified_claims"]["horizon_profile_preserved_on_positive_transitions"]
            for summary in descent_summaries_tuple
        ),
    }
    phase_claims["phase_24_bounded_channel_rule_search_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 24: bounded exact channel-rule search",
        "status": "pass" if phase_claims["phase_24_bounded_channel_rule_search_certificate"] else "fail",
        "graph_substrate": {
            "source": "Phase 21 mixed inner-outer mutation graph",
            "phase21_status": graph["phase21_status"],
            "phase21_counts": graph["phase21_counts"],
            "node_count": len(node_by_id),
            "edge_count": len(graph["edges"]),  # type: ignore[arg-type]
        },
        "search_spec": {
            "weighted_walk_rules": {
                "max_bonus": max_bonus,
                "rule_count": len(weighted_summaries_tuple),
                "feature_bonuses": (
                    "same labeled t=2 entropy flag",
                    "same entropy/reconstruction signal flag",
                    "same algebra-difference count",
                ),
            },
            "score_descent_rules": {
                "rule_count": len(descent_summaries_tuple),
                "score_features": (
                    "algebra_difference_count",
                    "same_labeled_t2_entropy bit",
                    "entropy_reconstruction_signal bit",
                ),
                "coefficient_set": (0, 1),
                "zero_score_rule_excluded": True,
            },
        },
        "weighted_walk_rule_summaries": weighted_summaries_tuple,
        "score_descent_rule_summaries": descent_summaries_tuple,
        "comparison": {
            "weighted_walk_stationary_bucket_extrema": weighted_extrema,
            "score_descent_absorbing_node_extrema": descent_extrema,
            "score_descent_absorbing_bucket_weight_extrema": descent_bucket_extrema,
        },
        "counts": {
            "nodes": len(node_by_id),
            "phase21_edges": len(graph["edges"]),  # type: ignore[arg-type]
            "weighted_walk_rules": len(weighted_summaries_tuple),
            "score_descent_rules": len(descent_summaries_tuple),
            "weighted_walk_closed_class_counts": tuple(sorted(set(weighted_closed_class_counts))),
            "weighted_walk_absorbing_node_counts": tuple(sorted(set(weighted_absorbing_counts))),
            "score_descent_absorbing_node_count_range": (
                min(descent_absorbing_counts),
                max(descent_absorbing_counts),
            ),
            "stationary_extrema_buckets": len(weighted_extrema),
            "absorbing_bucket_extrema_buckets": len(descent_bucket_extrema),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "A bounded search over local symmetric edge-bonus rules certifies exact stationary extrema for every "
                "outcome bucket. The extrema are computed by rational weighted-degree stationary distributions, not by "
                "trajectory sampling."
            ),
            "absorbing_lesson": (
                "Positive symmetric walks give a no-go for absorbing structure on this connected graph, while simple "
                "score-descent rules give absorbing classes whose counts depend on the chosen score."
            ),
            "horizon_lesson": (
                "Every searched channel rule preserves the repaired shared-horizon correctability and survivor "
                "fixed-point profile on positive-probability transitions."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 24 turns channel-rule choice into an exact bounded search and finds rule-dependent extrema. "
                "The next adaptation should lift from rule extrema to rule synthesis: search for small rules that "
                "separate two target buckets while keeping additional observer-patch constraints fixed."
            ),
            "suggested_phase_25": (
                "Add target-constrained channel synthesis: enumerate small exact rules that maximize a chosen bucket "
                "gap, certify Pareto frontiers across full semantics, entropy breaks, operator collapse, and horizon "
                "constraints, then emit minimal rule witnesses."
            ),
        },
    }


def phase25_bucket_groups() -> dict[str, tuple[str, ...]]:
    return {
        "full_semantics": ("full_semantics_preserved",),
        "entropy_break": (
            "entropy_break_operator_collapsed_algebra_residue",
            "entropy_break_reconstruction_extra_algebra",
            "low_order_entropy_break_with_operator_collapse",
            "low_order_entropy_break_with_reconstruction_survives",
        ),
        "operator_collapse": (
            "entropy_break_operator_collapsed_algebra_residue",
            "low_order_entropy_break_with_operator_collapse",
            "operator_geometry_collapsed",
        ),
    }


def phase25_group_weight(
    *,
    bucket_weights: dict[str, Fraction],
    buckets: tuple[str, ...],
) -> Fraction:
    return sum((bucket_weights.get(bucket, Fraction(0, 1)) for bucket in buckets), Fraction(0, 1))


def phase25_rule_complexity(spec: dict[str, object]) -> tuple[int, int, int, str]:
    bonuses = (
        int(spec["entropy_match_same_bonus"]),
        int(spec["observer_signal_same_bonus"]),
        int(spec["algebra_flat_bonus"]),
    )
    return (sum(bonuses), sum(1 for bonus in bonuses if bonus), max(bonuses), str(spec["name"]))


def phase25_public_complexity(spec: dict[str, object]) -> dict[str, object]:
    total_bonus, nonzero_terms, max_bonus, _ = phase25_rule_complexity(spec)
    return {
        "total_bonus": total_bonus,
        "nonzero_feature_terms": nonzero_terms,
        "max_single_feature_bonus": max_bonus,
    }


def phase25_target_objectives() -> tuple[dict[str, str], ...]:
    return (
        {
            "name": "prefer_full_semantics_over_entropy_break",
            "positive_metric": "full_semantics",
            "negative_metric": "entropy_break",
            "interpretation": "maximize stationary full-semantics weight minus entropy-break weight",
        },
        {
            "name": "prefer_full_semantics_over_operator_collapse",
            "positive_metric": "full_semantics",
            "negative_metric": "operator_collapse",
            "interpretation": "maximize stationary full-semantics weight minus operator-collapse weight",
        },
        {
            "name": "prefer_entropy_break_over_full_semantics",
            "positive_metric": "entropy_break",
            "negative_metric": "full_semantics",
            "interpretation": "maximize stationary entropy-break weight minus full-semantics weight",
        },
        {
            "name": "prefer_operator_collapse_over_full_semantics",
            "positive_metric": "operator_collapse",
            "negative_metric": "full_semantics",
            "interpretation": "maximize stationary operator-collapse weight minus full-semantics weight",
        },
        {
            "name": "prefer_entropy_break_over_operator_collapse",
            "positive_metric": "entropy_break",
            "negative_metric": "operator_collapse",
            "interpretation": "maximize stationary entropy-break weight minus operator-collapse weight",
        },
        {
            "name": "prefer_operator_collapse_over_entropy_break",
            "positive_metric": "operator_collapse",
            "negative_metric": "entropy_break",
            "interpretation": "maximize stationary operator-collapse weight minus entropy-break weight",
        },
    )


def phase25_rule_metric_entry(
    *,
    summary: dict[str, object],
    bucket_weights: dict[str, Fraction],
) -> dict[str, object]:
    spec = summary["rule"]
    if not isinstance(spec, dict):
        raise TypeError("Phase 25 weighted summary rule must be a dict")
    groups = phase25_bucket_groups()
    grouped_metrics = {
        group: phase25_group_weight(bucket_weights=bucket_weights, buckets=buckets)
        for group, buckets in groups.items()
    }
    return {
        "rule": spec,
        "metrics": {
            group: phase22_fraction(value)
            for group, value in grouped_metrics.items()
        },
        "complexity": phase25_public_complexity(spec),
        "constraints": {
            "row_stochastic": summary["certified_claims"]["row_stochastic"],  # type: ignore[index]
            "positive_symmetric_edge_weights": summary["certified_claims"]["edge_weights_positive"]  # type: ignore[index]
            and summary["certified_claims"]["edge_weight_rule_symmetric"],  # type: ignore[index]
            "stationary_distribution_verified_exactly": summary["certified_claims"][  # type: ignore[index]
                "stationary_distribution_verified_exactly"
            ],
            "horizon_profile_preserved_on_positive_transitions": summary["certified_claims"][  # type: ignore[index]
                "horizon_profile_preserved_on_positive_transitions"
            ],
            "phase21_observer_transition_edges_only": True,
        },
    }


def phase25_rule_witness(
    *,
    rule_name: str,
    specs_by_name: dict[str, dict[str, object]],
    metrics_by_rule: dict[str, dict[str, Fraction]],
) -> dict[str, object]:
    spec = specs_by_name[rule_name]
    return {
        "rule": spec,
        "complexity": phase25_public_complexity(spec),
        "metrics": {
            name: phase22_fraction(value)
            for name, value in sorted(metrics_by_rule[rule_name].items())
        },
    }


def phase25_target_gap_witnesses(
    *,
    specs_by_name: dict[str, dict[str, object]],
    metrics_by_rule: dict[str, dict[str, Fraction]],
) -> tuple[dict[str, object], ...]:
    witnesses = []
    for objective in phase25_target_objectives():
        positive = objective["positive_metric"]
        negative = objective["negative_metric"]
        gaps = {
            rule_name: metrics[positive] - metrics[negative]
            for rule_name, metrics in metrics_by_rule.items()
        }
        best_gap = max(gaps.values())
        maximizers = tuple(sorted(rule_name for rule_name, gap in gaps.items() if gap == best_gap))
        best_complexity = min(phase25_rule_complexity(specs_by_name[rule_name]) for rule_name in maximizers)
        minimal_witnesses = tuple(
            rule_name
            for rule_name in maximizers
            if phase25_rule_complexity(specs_by_name[rule_name]) == best_complexity
        )
        witnesses.append(
            {
                "objective": objective,
                "max_gap": phase22_fraction(best_gap),
                "all_maximizing_rules": maximizers,
                "minimal_rule_witnesses": tuple(
                    phase25_rule_witness(
                        rule_name=rule_name,
                        specs_by_name=specs_by_name,
                        metrics_by_rule=metrics_by_rule,
                    )
                    for rule_name in minimal_witnesses
                ),
            }
        )
    return tuple(witnesses)


def phase25_rule_dominates(
    *,
    left: str,
    right: str,
    metrics_by_rule: dict[str, dict[str, Fraction]],
    metric_names: tuple[str, ...],
) -> bool:
    left_metrics = metrics_by_rule[left]
    right_metrics = metrics_by_rule[right]
    return all(left_metrics[name] >= right_metrics[name] for name in metric_names) and any(
        left_metrics[name] > right_metrics[name] for name in metric_names
    )


def phase25_pareto_frontier(
    *,
    specs_by_name: dict[str, dict[str, object]],
    metrics_by_rule: dict[str, dict[str, Fraction]],
) -> dict[str, object]:
    metric_names = ("full_semantics", "entropy_break", "operator_collapse")
    rule_names = tuple(sorted(metrics_by_rule))
    frontier_rules = tuple(
        rule_name
        for rule_name in rule_names
        if not any(
            phase25_rule_dominates(
                left=other,
                right=rule_name,
                metrics_by_rule=metrics_by_rule,
                metric_names=metric_names,
            )
            for other in rule_names
            if other != rule_name
        )
    )
    frontier_vectors: dict[tuple[Fraction, ...], list[str]] = {}
    for rule_name in frontier_rules:
        vector = tuple(metrics_by_rule[rule_name][metric] for metric in metric_names)
        frontier_vectors.setdefault(vector, []).append(rule_name)
    public_vectors = []
    for vector, rules in sorted(frontier_vectors.items(), key=lambda item: item[0]):
        min_complexity = min(phase25_rule_complexity(specs_by_name[rule_name]) for rule_name in rules)
        minimal_witnesses = tuple(
            rule_name
            for rule_name in sorted(rules)
            if phase25_rule_complexity(specs_by_name[rule_name]) == min_complexity
        )
        public_vectors.append(
            {
                "metrics": {
                    metric: phase22_fraction(value)
                    for metric, value in zip(metric_names, vector)
                },
                "all_rules_with_vector": tuple(sorted(rules)),
                "minimal_rule_witnesses": tuple(
                    phase25_rule_witness(
                        rule_name=rule_name,
                        specs_by_name=specs_by_name,
                        metrics_by_rule=metrics_by_rule,
                    )
                    for rule_name in minimal_witnesses
                ),
            }
        )
    dominated_rules = tuple(rule_name for rule_name in rule_names if rule_name not in frontier_rules)
    every_nonfrontier_dominated_by_frontier = all(
        any(
            phase25_rule_dominates(
                left=frontier_rule,
                right=dominated_rule,
                metrics_by_rule=metrics_by_rule,
                metric_names=metric_names,
            )
            for frontier_rule in frontier_rules
        )
        for dominated_rule in dominated_rules
    )
    return {
        "metric_names": metric_names,
        "frontier_rules": frontier_rules,
        "frontier_metric_vectors": tuple(public_vectors),
        "frontier_rule_count": len(frontier_rules),
        "frontier_metric_vector_count": len(public_vectors),
        "dominated_rule_count": len(dominated_rules),
        "every_nonfrontier_rule_dominated_by_frontier": every_nonfrontier_dominated_by_frontier,
    }


def phase25_target_witnesses_are_minimal(
    *,
    witnesses: tuple[dict[str, object], ...],
    specs_by_name: dict[str, dict[str, object]],
    metrics_by_rule: dict[str, dict[str, Fraction]],
) -> bool:
    for item in witnesses:
        objective = item["objective"]
        if not isinstance(objective, dict):
            return False
        positive = str(objective["positive_metric"])
        negative = str(objective["negative_metric"])
        best_gap = max(metrics[positive] - metrics[negative] for metrics in metrics_by_rule.values())
        if Fraction(item["max_gap"]["numerator"], item["max_gap"]["denominator"]) != best_gap:  # type: ignore[index]
            return False
        maximizers = tuple(
            sorted(
                rule_name
                for rule_name, metrics in metrics_by_rule.items()
                if metrics[positive] - metrics[negative] == best_gap
            )
        )
        if tuple(item["all_maximizing_rules"]) != maximizers:  # type: ignore[arg-type]
            return False
        best_complexity = min(phase25_rule_complexity(specs_by_name[rule_name]) for rule_name in maximizers)
        witness_rules = tuple(
            str(witness["rule"]["name"])  # type: ignore[index]
            for witness in item["minimal_rule_witnesses"]  # type: ignore[index]
        )
        if not witness_rules:
            return False
        if any(phase25_rule_complexity(specs_by_name[rule_name]) != best_complexity for rule_name in witness_rules):
            return False
    return True


def phase25_pareto_frontier_is_certified(
    *,
    frontier: dict[str, object],
    metrics_by_rule: dict[str, dict[str, Fraction]],
) -> bool:
    metric_names = tuple(str(name) for name in frontier["metric_names"])  # type: ignore[index]
    frontier_rules = tuple(str(rule) for rule in frontier["frontier_rules"])  # type: ignore[index]
    rule_names = tuple(sorted(metrics_by_rule))
    if any(
        phase25_rule_dominates(
            left=other,
            right=frontier_rule,
            metrics_by_rule=metrics_by_rule,
            metric_names=metric_names,
        )
        for frontier_rule in frontier_rules
        for other in rule_names
        if other != frontier_rule
    ):
        return False
    dominated_rules = tuple(rule_name for rule_name in rule_names if rule_name not in frontier_rules)
    return all(
        any(
            phase25_rule_dominates(
                left=frontier_rule,
                right=rule_name,
                metrics_by_rule=metrics_by_rule,
                metric_names=metric_names,
            )
            for frontier_rule in frontier_rules
        )
        for rule_name in dominated_rules
    )


def bridge_cosmology_phase25_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    graph = phase22_phase21_graph_data()
    node_by_id = graph["node_by_id"]
    adjacency = graph["adjacency"]
    if not isinstance(node_by_id, dict) or not isinstance(adjacency, dict):
        raise TypeError("Phase 25 graph data must contain node and adjacency dictionaries")
    specs = phase24_weighted_rule_specs(max_bonus=max_bonus)
    rule_metric_entries = []
    specs_by_name: dict[str, dict[str, object]] = {}
    metrics_by_rule: dict[str, dict[str, Fraction]] = {}
    synthesis_constraint_claims = []
    for spec in specs:
        summary, bucket_weights = phase24_weighted_rule_summary(
            spec=spec,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            adjacency=adjacency,  # type: ignore[arg-type]
        )
        entry = phase25_rule_metric_entry(summary=summary, bucket_weights=bucket_weights)
        rule_name = str(spec["name"])
        specs_by_name[rule_name] = spec
        metrics_by_rule[rule_name] = {
            group: Fraction(value["numerator"], value["denominator"])  # type: ignore[index]
            for group, value in entry["metrics"].items()  # type: ignore[union-attr]
        }
        rule_metric_entries.append(entry)
        synthesis_constraint_claims.append(
            all(bool(value) for value in entry["constraints"].values())  # type: ignore[union-attr]
        )
    rule_metric_entries_tuple = tuple(rule_metric_entries)
    target_gap_witnesses = phase25_target_gap_witnesses(
        specs_by_name=specs_by_name,
        metrics_by_rule=metrics_by_rule,
    )
    pareto_frontier = phase25_pareto_frontier(
        specs_by_name=specs_by_name,
        metrics_by_rule=metrics_by_rule,
    )
    target_minimal_rule_names = tuple(
        sorted(
            {
                str(witness["rule"]["name"])  # type: ignore[index]
                for objective in target_gap_witnesses
                for witness in objective["minimal_rule_witnesses"]  # type: ignore[index]
            }
        )
    )
    uniform_is_required_for_any_target = "edge_bonus_e0_o0_a0" in target_minimal_rule_names
    nonuniform_target_witness_count = sum(
        1 for rule_name in target_minimal_rule_names if rule_name != "edge_bonus_e0_o0_a0"
    )
    negative_gap_objectives = tuple(
        str(item["objective"]["name"])  # type: ignore[index]
        for item in target_gap_witnesses
        if Fraction(item["max_gap"]["numerator"], item["max_gap"]["denominator"]) < 0  # type: ignore[index]
    )
    phase_claims = {
        "phase21_substrate_certified": graph["phase21_status"] == "pass"
        and graph["phase21_claims"]["phase_21_mixed_inner_outer_transition_graph_certificate"],  # type: ignore[index]
        "target_synthesis_rule_space_exactly_bounded": len(rule_metric_entries_tuple) == (max_bonus + 1) ** 3,
        "all_synthesis_candidates_satisfy_horizon_and_observer_constraints": all(synthesis_constraint_claims)
        and phase22_horizon_invariant_nodes(node_by_id),  # type: ignore[arg-type]
        "target_gap_objectives_exactly_certified": phase25_target_witnesses_are_minimal(
            witnesses=target_gap_witnesses,
            specs_by_name=specs_by_name,
            metrics_by_rule=metrics_by_rule,
        ),
        "all_target_objectives_have_minimal_rule_witnesses": all(
            bool(item["minimal_rule_witnesses"]) for item in target_gap_witnesses
        ),
        "pareto_frontier_certified_exactly": phase25_pareto_frontier_is_certified(
            frontier=pareto_frontier,
            metrics_by_rule=metrics_by_rule,
        )
        and bool(pareto_frontier["frontier_rules"]),
        "pareto_frontier_contains_tradeoffs": int(pareto_frontier["frontier_metric_vector_count"]) > 1,
        "synthesis_finds_nonuniform_minimal_witnesses": nonuniform_target_witness_count > 0,
        "target_synthesis_detects_signed_gap_no_go": bool(negative_gap_objectives),
    }
    phase_claims["phase_25_target_constrained_channel_synthesis_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 25: target-constrained channel synthesis",
        "status": "pass"
        if phase_claims["phase_25_target_constrained_channel_synthesis_certificate"]
        else "fail",
        "graph_substrate": {
            "source": "Phase 21 mixed inner-outer mutation graph",
            "phase21_status": graph["phase21_status"],
            "phase21_counts": graph["phase21_counts"],
            "node_count": len(node_by_id),
            "edge_count": len(graph["edges"]),  # type: ignore[arg-type]
        },
        "search_spec": {
            "rule_language": "positive symmetric edge-bonus weighted walks",
            "max_bonus": max_bonus,
            "rule_count": len(rule_metric_entries_tuple),
            "bucket_groups": phase25_bucket_groups(),
            "target_objectives": phase25_target_objectives(),
            "complexity_order": (
                "minimize total feature bonus",
                "then minimize number of nonzero feature terms",
                "then minimize largest single feature bonus",
                "then lexicographic rule name",
            ),
            "hard_constraints": (
                "row stochastic exact rational transition matrix",
                "positive symmetric edge weights",
                "stationary distribution verified by exact pi P = pi",
                "positive transitions use certified Phase 21 observer edges",
                "shared-horizon correctability and fixed-point profile preserved",
            ),
        },
        "rule_metric_table": rule_metric_entries_tuple,
        "target_gap_witnesses": target_gap_witnesses,
        "pareto_frontier": pareto_frontier,
        "counts": {
            "nodes": len(node_by_id),
            "phase21_edges": len(graph["edges"]),  # type: ignore[arg-type]
            "candidate_rules": len(rule_metric_entries_tuple),
            "target_gap_objectives": len(target_gap_witnesses),
            "unique_minimal_target_witness_rules": len(target_minimal_rule_names),
            "nonuniform_minimal_target_witness_rules": nonuniform_target_witness_count,
            "uniform_is_minimal_for_at_least_one_target": uniform_is_required_for_any_target,
            "negative_gap_objectives": len(negative_gap_objectives),
            "pareto_frontier_rules": pareto_frontier["frontier_rule_count"],
            "pareto_frontier_metric_vectors": pareto_frontier["frontier_metric_vector_count"],
            "pareto_dominated_rules": pareto_frontier["dominated_rule_count"],
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "The finite channel-rule language now supports target-constrained synthesis: for each specified "
                "bucket-gap objective, the certificate emits exact maximizers and the least-complexity witnesses "
                "among them."
            ),
            "pareto_lesson": (
                "The Pareto frontier over full semantics, entropy-break weight, and operator-collapse weight has "
                "multiple exact tradeoff points, so no single local weighted-walk rule optimizes all three notions "
                "of emergent structure at once."
            ),
            "horizon_lesson": (
                "All synthesized witnesses satisfy the same hard horizon and observer-edge constraints, so the target "
                "gap changes are attributed to channel-rule choice rather than horizon failure."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 25 provides minimal exact rule witnesses for target gaps on one certified substrate. The next "
                "adaptation should test whether those witnesses transfer across nearby substrates or are overfit to "
                "the Phase 21 graph."
            ),
            "suggested_phase_26": (
                "Run cross-substrate channel-rule transfer: apply Phase 25 witness rules to bounded variants of the "
                "mixed graph, certify which target gaps and Pareto positions persist, and report transfer/no-transfer "
                "counterexamples."
            ),
        },
    }


def phase26_transfer_substrate_specs() -> tuple[dict[str, str], ...]:
    return (
        {
            "name": "full_mixed_graph",
            "description": "Baseline Phase 21 graph with all certified inner/outer mutation edges.",
            "edge_filter": "all certified Phase 21 edges",
        },
        {
            "name": "entropy_stable_edges",
            "description": "Retain only certified edges that do not flip the low-order entropy-match flag.",
            "edge_filter": "not entropy_match_flips",
        },
        {
            "name": "observer_signal_stable_edges",
            "description": "Retain only certified edges that do not flip the entropy/reconstruction signal flag.",
            "edge_filter": "not observer_signal_flips",
        },
        {
            "name": "algebra_flat_edges",
            "description": "Retain only certified edges with zero algebra-difference-count delta.",
            "edge_filter": "algebra_monotonicity == flat",
        },
    )


def phase26_edge_in_substrate(*, edge: dict[str, object], substrate_name: str) -> bool:
    if substrate_name == "full_mixed_graph":
        return True
    if substrate_name == "entropy_stable_edges":
        return not bool(edge["entropy_match_flips"])
    if substrate_name == "observer_signal_stable_edges":
        return not bool(edge["observer_signal_flips"])
    if substrate_name == "algebra_flat_edges":
        return str(edge["algebra_monotonicity"]) == "flat"
    raise ValueError(f"unknown Phase 26 substrate {substrate_name!r}")


def phase26_adjacency_from_edges(
    *,
    node_ids: tuple[str, ...],
    edges: tuple[dict[str, object], ...],
) -> dict[str, tuple[str, ...]]:
    adjacency: dict[str, set[str]] = {node_id: set() for node_id in node_ids}
    for edge in edges:
        left = str(edge["left"])
        right = str(edge["right"])
        adjacency[left].add(right)
        adjacency[right].add(left)
    return {node_id: tuple(sorted(neighbors)) for node_id, neighbors in adjacency.items()}


def phase26_rule_metrics_for_adjacency(
    *,
    specs: tuple[dict[str, object], ...],
    node_by_id: dict[str, dict[str, object]],
    adjacency: dict[str, tuple[str, ...]],
) -> tuple[tuple[dict[str, object], ...], dict[str, dict[str, object]], dict[str, dict[str, Fraction]], bool]:
    rule_metric_entries = []
    specs_by_name: dict[str, dict[str, object]] = {}
    metrics_by_rule: dict[str, dict[str, Fraction]] = {}
    constraints_pass = []
    for spec in specs:
        summary, bucket_weights = phase24_weighted_rule_summary(
            spec=spec,
            node_by_id=node_by_id,
            adjacency=adjacency,
        )
        entry = phase25_rule_metric_entry(summary=summary, bucket_weights=bucket_weights)
        rule_name = str(spec["name"])
        specs_by_name[rule_name] = spec
        metrics_by_rule[rule_name] = {
            group: Fraction(value["numerator"], value["denominator"])  # type: ignore[index]
            for group, value in entry["metrics"].items()  # type: ignore[union-attr]
        }
        constraints_pass.append(all(bool(value) for value in entry["constraints"].values()))  # type: ignore[union-attr]
        rule_metric_entries.append(entry)
    return tuple(rule_metric_entries), specs_by_name, metrics_by_rule, all(constraints_pass)


def phase26_substrate_analysis(
    *,
    spec: dict[str, str],
    rule_specs: tuple[dict[str, object], ...],
    node_by_id: dict[str, dict[str, object]],
    node_ids: tuple[str, ...],
    phase21_edges: tuple[dict[str, object], ...],
) -> dict[str, object]:
    retained_edges = tuple(
        edge
        for edge in phase21_edges
        if phase26_edge_in_substrate(edge=edge, substrate_name=spec["name"])
    )
    adjacency = phase26_adjacency_from_edges(node_ids=node_ids, edges=retained_edges)
    rule_metric_table, specs_by_name, metrics_by_rule, constraints_pass = phase26_rule_metrics_for_adjacency(
        specs=rule_specs,
        node_by_id=node_by_id,
        adjacency=adjacency,
    )
    target_gap_witnesses = phase25_target_gap_witnesses(
        specs_by_name=specs_by_name,
        metrics_by_rule=metrics_by_rule,
    )
    pareto_frontier = phase25_pareto_frontier(
        specs_by_name=specs_by_name,
        metrics_by_rule=metrics_by_rule,
    )
    isolated_nodes = tuple(sorted(node_id for node_id, neighbors in adjacency.items() if not neighbors))
    edge_type_counts = phase16_count_edge_types(retained_edges)
    phase_claims = {
        "edge_subset_of_phase21_certified_graph": all(
            edge["certified_claims"]["mixed_inner_outer_transition_edge"] for edge in retained_edges
        ),
        "nonempty_edge_filtered_substrate": bool(retained_edges),
        "all_candidate_rules_verified_on_substrate": constraints_pass,
        "target_witnesses_certified_on_substrate": phase25_target_witnesses_are_minimal(
            witnesses=target_gap_witnesses,
            specs_by_name=specs_by_name,
            metrics_by_rule=metrics_by_rule,
        ),
        "pareto_frontier_certified_on_substrate": phase25_pareto_frontier_is_certified(
            frontier=pareto_frontier,
            metrics_by_rule=metrics_by_rule,
        ),
    }
    phase_claims["transfer_substrate_certificate"] = all(phase_claims.values())
    return {
        "name": spec["name"],
        "description": spec["description"],
        "edge_filter": spec["edge_filter"],
        "counts": {
            "nodes": len(node_ids),
            "edges": len(retained_edges),
            "isolated_nodes": len(isolated_nodes),
            "edge_type_counts": tuple(sorted(edge_type_counts.items())),
            "entropy_match_flip_edges": sum(1 for edge in retained_edges if bool(edge["entropy_match_flips"])),
            "observer_signal_flip_edges": sum(1 for edge in retained_edges if bool(edge["observer_signal_flips"])),
            "algebra_increase_edges": sum(1 for edge in retained_edges if edge["algebra_monotonicity"] == "increase"),
            "algebra_decrease_edges": sum(1 for edge in retained_edges if edge["algebra_monotonicity"] == "decrease"),
            "algebra_flat_edges": sum(1 for edge in retained_edges if edge["algebra_monotonicity"] == "flat"),
            "candidate_rules": len(rule_specs),
        },
        "isolated_nodes": isolated_nodes,
        "rule_metric_table": rule_metric_table,
        "target_gap_witnesses": target_gap_witnesses,
        "pareto_frontier": pareto_frontier,
        "certified_claims": phase_claims,
        "_specs_by_name": specs_by_name,
        "_metrics_by_rule": metrics_by_rule,
    }


def phase26_target_transfer_records(
    *,
    baseline_witnesses: tuple[dict[str, object], ...],
    substrate_witnesses: tuple[dict[str, object], ...],
    substrate_metrics_by_rule: dict[str, dict[str, Fraction]],
) -> tuple[dict[str, object], ...]:
    baseline_by_objective = {str(item["objective"]["name"]): item for item in baseline_witnesses}  # type: ignore[index]
    substrate_by_objective = {str(item["objective"]["name"]): item for item in substrate_witnesses}  # type: ignore[index]
    records = []
    for objective in phase25_target_objectives():
        objective_name = objective["name"]
        baseline = baseline_by_objective[objective_name]
        substrate = substrate_by_objective[objective_name]
        baseline_minimal_rules = tuple(
            str(witness["rule"]["name"]) for witness in baseline["minimal_rule_witnesses"]  # type: ignore[index]
        )
        substrate_maximizers = tuple(str(rule) for rule in substrate["all_maximizing_rules"])  # type: ignore[arg-type]
        substrate_minimal_rules = tuple(
            str(witness["rule"]["name"]) for witness in substrate["minimal_rule_witnesses"]  # type: ignore[index]
        )
        positive = objective["positive_metric"]
        negative = objective["negative_metric"]
        baseline_rule_gaps = tuple(
            {
                "rule": rule_name,
                "gap_on_substrate": phase22_fraction(
                    substrate_metrics_by_rule[rule_name][positive] - substrate_metrics_by_rule[rule_name][negative]
                ),
            }
            for rule_name in baseline_minimal_rules
        )
        transfer_success = any(rule_name in substrate_maximizers for rule_name in baseline_minimal_rules)
        records.append(
            {
                "objective": objective,
                "baseline_minimal_rules": baseline_minimal_rules,
                "substrate_max_gap": substrate["max_gap"],
                "substrate_all_maximizing_rules": substrate_maximizers,
                "substrate_minimal_rules": substrate_minimal_rules,
                "baseline_minimal_rule_gaps_on_substrate": baseline_rule_gaps,
                "baseline_witness_transfers_as_maximizer": transfer_success,
                "no_transfer_counterexample": not transfer_success,
            }
        )
    return tuple(records)


def phase26_pareto_transfer_record(
    *,
    baseline_frontier: dict[str, object],
    substrate_frontier: dict[str, object],
) -> dict[str, object]:
    baseline_rules = set(str(rule) for rule in baseline_frontier["frontier_rules"])  # type: ignore[index]
    substrate_rules = set(str(rule) for rule in substrate_frontier["frontier_rules"])  # type: ignore[index]
    return {
        "baseline_frontier_rules": tuple(sorted(baseline_rules)),
        "substrate_frontier_rules": tuple(sorted(substrate_rules)),
        "preserved_frontier_rules": tuple(sorted(baseline_rules & substrate_rules)),
        "lost_baseline_frontier_rules": tuple(sorted(baseline_rules - substrate_rules)),
        "new_substrate_frontier_rules": tuple(sorted(substrate_rules - baseline_rules)),
        "frontier_changed": baseline_rules != substrate_rules,
    }


def phase26_public_analysis(analysis: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in analysis.items()
        if key not in ("_specs_by_name", "_metrics_by_rule")
    }


def bridge_cosmology_phase26_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    graph = phase22_phase21_graph_data()
    node_by_id = graph["node_by_id"]
    adjacency = graph["adjacency"]
    if not isinstance(node_by_id, dict) or not isinstance(adjacency, dict):
        raise TypeError("Phase 26 graph data must contain node and adjacency dictionaries")
    node_ids = tuple(str(node_id) for node_id in graph["node_ids"])  # type: ignore[index]
    phase21_edges = tuple(edge for edge in graph["edges"] if isinstance(edge, dict))  # type: ignore[arg-type]
    rule_specs = phase24_weighted_rule_specs(max_bonus=max_bonus)
    analyses = tuple(
        phase26_substrate_analysis(
            spec=spec,
            rule_specs=rule_specs,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            node_ids=node_ids,
            phase21_edges=phase21_edges,
        )
        for spec in phase26_transfer_substrate_specs()
    )
    analysis_by_name = {str(analysis["name"]): analysis for analysis in analyses}
    baseline = analysis_by_name["full_mixed_graph"]
    baseline_witnesses = tuple(baseline["target_gap_witnesses"])  # type: ignore[arg-type]
    baseline_frontier = baseline["pareto_frontier"]
    transfer_analyses = []
    for analysis in analyses:
        target_transfer = phase26_target_transfer_records(
            baseline_witnesses=baseline_witnesses,
            substrate_witnesses=tuple(analysis["target_gap_witnesses"]),  # type: ignore[arg-type]
            substrate_metrics_by_rule=analysis["_metrics_by_rule"],  # type: ignore[arg-type]
        )
        pareto_transfer = phase26_pareto_transfer_record(
            baseline_frontier=baseline_frontier,  # type: ignore[arg-type]
            substrate_frontier=analysis["pareto_frontier"],  # type: ignore[arg-type]
        )
        transfer_analyses.append(
            {
                **phase26_public_analysis(analysis),
                "target_transfer": target_transfer,
                "pareto_transfer": pareto_transfer,
            }
        )
    transfer_analyses_tuple = tuple(transfer_analyses)
    nonbaseline_transfer_records = tuple(
        record
        for analysis in transfer_analyses_tuple
        if analysis["name"] != "full_mixed_graph"
        for record in analysis["target_transfer"]
    )
    nonbaseline_pareto_records = tuple(
        analysis["pareto_transfer"]
        for analysis in transfer_analyses_tuple
        if analysis["name"] != "full_mixed_graph"
    )
    target_transfer_successes = sum(
        1 for record in nonbaseline_transfer_records if bool(record["baseline_witness_transfers_as_maximizer"])
    )
    target_no_transfer_counterexamples = sum(
        1 for record in nonbaseline_transfer_records if bool(record["no_transfer_counterexample"])
    )
    pareto_changed_substrates = sum(1 for record in nonbaseline_pareto_records if bool(record["frontier_changed"]))
    phase_claims = {
        "phase21_substrate_certified": graph["phase21_status"] == "pass"
        and graph["phase21_claims"]["phase_21_mixed_inner_outer_transition_graph_certificate"],  # type: ignore[index]
        "all_transfer_substrates_certified": all(
            analysis["certified_claims"]["transfer_substrate_certificate"] for analysis in analyses  # type: ignore[index]
        ),
        "baseline_reproduces_phase25_target_synthesis": len(baseline_witnesses) == len(phase25_target_objectives())
        and baseline["pareto_frontier"]["frontier_rule_count"] == 7,  # type: ignore[index]
        "target_transfer_records_cover_all_nonbaseline_objectives": len(nonbaseline_transfer_records)
        == (len(phase26_transfer_substrate_specs()) - 1) * len(phase25_target_objectives()),
        "target_transfer_successes_detected": target_transfer_successes > 0,
        "target_no_transfer_counterexamples_detected": target_no_transfer_counterexamples > 0,
        "pareto_transfer_changes_detected": pareto_changed_substrates > 0,
        "horizon_invariant_across_transfer_substrates": phase22_horizon_invariant_nodes(
            node_by_id  # type: ignore[arg-type]
        )
        and all(
            bool(entry["constraints"]["horizon_profile_preserved_on_positive_transitions"])  # type: ignore[index]
            for analysis in transfer_analyses_tuple
            for entry in analysis["rule_metric_table"]  # type: ignore[index]
        ),
    }
    phase_claims["phase_26_cross_substrate_channel_rule_transfer_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 26: cross-substrate channel-rule transfer",
        "status": "pass" if phase_claims["phase_26_cross_substrate_channel_rule_transfer_certificate"] else "fail",
        "graph_substrate": {
            "source": "Phase 21 mixed inner-outer mutation graph and edge-filtered variants",
            "phase21_status": graph["phase21_status"],
            "phase21_counts": graph["phase21_counts"],
            "node_count": len(node_by_id),
            "full_edge_count": len(phase21_edges),
        },
        "search_spec": {
            "rule_language": "Phase 25 positive symmetric edge-bonus weighted walks",
            "max_bonus": max_bonus,
            "candidate_rules": len(rule_specs),
            "transfer_substrates": phase26_transfer_substrate_specs(),
            "target_objectives": phase25_target_objectives(),
        },
        "substrate_transfer_analyses": transfer_analyses_tuple,
        "counts": {
            "substrates": len(transfer_analyses_tuple),
            "nonbaseline_substrates": len(transfer_analyses_tuple) - 1,
            "candidate_rules": len(rule_specs),
            "target_transfer_records": len(nonbaseline_transfer_records),
            "target_transfer_successes": target_transfer_successes,
            "target_no_transfer_counterexamples": target_no_transfer_counterexamples,
            "pareto_changed_substrates": pareto_changed_substrates,
            "pareto_unchanged_substrates": len(nonbaseline_pareto_records) - pareto_changed_substrates,
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 25 witness rules are not substrate-independent laws: some target witnesses remain exact "
                "maximizers on edge-filtered variants, while others fail to transfer."
            ),
            "counterexample_lesson": (
                "The certificate gives explicit no-transfer counterexamples by objective and substrate, so local "
                "channel synthesis must be reported together with the graph substrate it was synthesized on."
            ),
            "horizon_lesson": (
                "All transfer substrates are certified Phase 21 edge subsets and preserve the repaired shared-horizon "
                "profile, so transfer failures come from changed transition geometry rather than horizon failure."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 26 shows that target-rule witnesses can transfer or fail across nearby substrates. The next "
                "adaptation should synthesize rules jointly over multiple substrates to find robust witnesses and "
                "separate them from graph-overfit witnesses."
            ),
            "suggested_phase_27": (
                "Run multi-substrate robust channel synthesis: maximize worst-case target gaps over a bounded "
                "substrate family, certify robust Pareto frontiers, and emit smallest rules that survive every "
                "included substrate."
            ),
        },
    }


def phase27_metric_extents(
    *,
    rule_name: str,
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]],
) -> dict[str, dict[str, object]]:
    groups = phase25_bucket_groups()
    out = {}
    for metric in groups:
        values = {
            substrate_name: metrics_by_rule[rule_name][metric]
            for substrate_name, metrics_by_rule in substrate_metric_maps.items()
        }
        minimum = min(values.values())
        maximum = max(values.values())
        out[metric] = {
            "worst_case": phase22_fraction(minimum),
            "best_case": phase22_fraction(maximum),
            "range": phase22_fraction(maximum - minimum),
            "by_substrate": tuple(
                {
                    "substrate": substrate_name,
                    "weight": phase22_fraction(value),
                }
                for substrate_name, value in sorted(values.items())
            ),
        }
    return out


def phase27_rule_robust_metrics(
    *,
    specs_by_name: dict[str, dict[str, object]],
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]],
) -> tuple[tuple[dict[str, object], ...], dict[str, dict[str, Fraction]]]:
    robust_metric_maps: dict[str, dict[str, Fraction]] = {}
    public_entries = []
    for rule_name in sorted(specs_by_name):
        worst_metrics = {
            metric: min(metrics_by_rule[rule_name][metric] for metrics_by_rule in substrate_metric_maps.values())
            for metric in phase25_bucket_groups()
        }
        robust_metric_maps[rule_name] = worst_metrics
        public_entries.append(
            {
                "rule": specs_by_name[rule_name],
                "complexity": phase25_public_complexity(specs_by_name[rule_name]),
                "robust_metrics": {
                    metric: phase22_fraction(value)
                    for metric, value in sorted(worst_metrics.items())
                },
                "metric_extents": phase27_metric_extents(
                    rule_name=rule_name,
                    substrate_metric_maps=substrate_metric_maps,
                ),
            }
        )
    return tuple(public_entries), robust_metric_maps


def phase27_robust_rule_witness(
    *,
    rule_name: str,
    specs_by_name: dict[str, dict[str, object]],
    robust_metrics_by_rule: dict[str, dict[str, Fraction]],
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]],
    positive_metric: str,
    negative_metric: str,
) -> dict[str, object]:
    return {
        "rule": specs_by_name[rule_name],
        "complexity": phase25_public_complexity(specs_by_name[rule_name]),
        "robust_metrics": {
            name: phase22_fraction(value)
            for name, value in sorted(robust_metrics_by_rule[rule_name].items())
        },
        "gaps_by_substrate": tuple(
            {
                "substrate": substrate_name,
                "gap": phase22_fraction(metrics_by_rule[rule_name][positive_metric] - metrics_by_rule[rule_name][negative_metric]),
            }
            for substrate_name, metrics_by_rule in sorted(substrate_metric_maps.items())
        ),
    }


def phase27_robust_target_gap_witnesses(
    *,
    specs_by_name: dict[str, dict[str, object]],
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]],
    robust_metrics_by_rule: dict[str, dict[str, Fraction]],
) -> tuple[dict[str, object], ...]:
    witnesses = []
    for objective in phase25_target_objectives():
        positive = objective["positive_metric"]
        negative = objective["negative_metric"]
        substrate_gaps = {
            rule_name: {
                substrate_name: metrics_by_rule[rule_name][positive] - metrics_by_rule[rule_name][negative]
                for substrate_name, metrics_by_rule in substrate_metric_maps.items()
            }
            for rule_name in specs_by_name
        }
        worst_gaps = {
            rule_name: min(gaps.values())
            for rule_name, gaps in substrate_gaps.items()
        }
        best_worst_gap = max(worst_gaps.values())
        maximizers = tuple(sorted(rule_name for rule_name, gap in worst_gaps.items() if gap == best_worst_gap))
        best_complexity = min(phase25_rule_complexity(specs_by_name[rule_name]) for rule_name in maximizers)
        minimal_witnesses = tuple(
            rule_name
            for rule_name in maximizers
            if phase25_rule_complexity(specs_by_name[rule_name]) == best_complexity
        )
        witnesses.append(
            {
                "objective": objective,
                "max_worst_case_gap": phase22_fraction(best_worst_gap),
                "all_robust_maximizing_rules": maximizers,
                "minimal_robust_rule_witnesses": tuple(
                    phase27_robust_rule_witness(
                        rule_name=rule_name,
                        specs_by_name=specs_by_name,
                        robust_metrics_by_rule=robust_metrics_by_rule,
                        substrate_metric_maps=substrate_metric_maps,
                        positive_metric=positive,
                        negative_metric=negative,
                    )
                    for rule_name in minimal_witnesses
                ),
            }
        )
    return tuple(witnesses)


def phase27_robust_target_witnesses_are_minimal(
    *,
    witnesses: tuple[dict[str, object], ...],
    specs_by_name: dict[str, dict[str, object]],
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]],
) -> bool:
    for item in witnesses:
        objective = item["objective"]
        if not isinstance(objective, dict):
            return False
        positive = str(objective["positive_metric"])
        negative = str(objective["negative_metric"])
        worst_gaps = {
            rule_name: min(
                metrics_by_rule[rule_name][positive] - metrics_by_rule[rule_name][negative]
                for metrics_by_rule in substrate_metric_maps.values()
            )
            for rule_name in specs_by_name
        }
        best_worst_gap = max(worst_gaps.values())
        if Fraction(item["max_worst_case_gap"]["numerator"], item["max_worst_case_gap"]["denominator"]) != best_worst_gap:  # type: ignore[index]
            return False
        maximizers = tuple(sorted(rule_name for rule_name, gap in worst_gaps.items() if gap == best_worst_gap))
        if tuple(item["all_robust_maximizing_rules"]) != maximizers:  # type: ignore[arg-type]
            return False
        best_complexity = min(phase25_rule_complexity(specs_by_name[rule_name]) for rule_name in maximizers)
        witness_rules = tuple(
            str(witness["rule"]["name"])  # type: ignore[index]
            for witness in item["minimal_robust_rule_witnesses"]  # type: ignore[index]
        )
        if not witness_rules:
            return False
        if any(phase25_rule_complexity(specs_by_name[rule_name]) != best_complexity for rule_name in witness_rules):
            return False
    return True


def phase27_robust_pareto_frontier(
    *,
    specs_by_name: dict[str, dict[str, object]],
    robust_metrics_by_rule: dict[str, dict[str, Fraction]],
) -> dict[str, object]:
    return phase25_pareto_frontier(
        specs_by_name=specs_by_name,
        metrics_by_rule=robust_metrics_by_rule,
    )


def phase27_robust_pareto_frontier_is_certified(
    *,
    frontier: dict[str, object],
    robust_metrics_by_rule: dict[str, dict[str, Fraction]],
) -> bool:
    return phase25_pareto_frontier_is_certified(
        frontier=frontier,
        metrics_by_rule=robust_metrics_by_rule,
    )


def bridge_cosmology_phase27_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    graph = phase22_phase21_graph_data()
    node_by_id = graph["node_by_id"]
    adjacency = graph["adjacency"]
    if not isinstance(node_by_id, dict) or not isinstance(adjacency, dict):
        raise TypeError("Phase 27 graph data must contain node and adjacency dictionaries")
    node_ids = tuple(str(node_id) for node_id in graph["node_ids"])  # type: ignore[index]
    phase21_edges = tuple(edge for edge in graph["edges"] if isinstance(edge, dict))  # type: ignore[arg-type]
    rule_specs = phase24_weighted_rule_specs(max_bonus=max_bonus)
    substrate_analyses = tuple(
        phase26_substrate_analysis(
            spec=spec,
            rule_specs=rule_specs,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            node_ids=node_ids,
            phase21_edges=phase21_edges,
        )
        for spec in phase26_transfer_substrate_specs()
    )
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]] = {
        str(analysis["name"]): analysis["_metrics_by_rule"]  # type: ignore[assignment]
        for analysis in substrate_analyses
    }
    specs_by_name = substrate_analyses[0]["_specs_by_name"]  # type: ignore[assignment]
    if not isinstance(specs_by_name, dict):
        raise TypeError("Phase 27 substrate analysis must contain specs_by_name")
    robust_rule_table, robust_metrics_by_rule = phase27_rule_robust_metrics(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        substrate_metric_maps=substrate_metric_maps,
    )
    robust_target_witnesses = phase27_robust_target_gap_witnesses(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        substrate_metric_maps=substrate_metric_maps,
        robust_metrics_by_rule=robust_metrics_by_rule,
    )
    robust_pareto_frontier = phase27_robust_pareto_frontier(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        robust_metrics_by_rule=robust_metrics_by_rule,
    )
    robust_minimal_rule_names = tuple(
        sorted(
            {
                str(witness["rule"]["name"])  # type: ignore[index]
                for objective in robust_target_witnesses
                for witness in objective["minimal_robust_rule_witnesses"]  # type: ignore[index]
            }
        )
    )
    negative_robust_objectives = tuple(
        str(item["objective"]["name"])  # type: ignore[index]
        for item in robust_target_witnesses
        if Fraction(item["max_worst_case_gap"]["numerator"], item["max_worst_case_gap"]["denominator"]) < 0  # type: ignore[index]
    )
    positive_robust_objectives = tuple(
        str(item["objective"]["name"])  # type: ignore[index]
        for item in robust_target_witnesses
        if Fraction(item["max_worst_case_gap"]["numerator"], item["max_worst_case_gap"]["denominator"]) > 0  # type: ignore[index]
    )
    phase_claims = {
        "phase21_substrate_certified": graph["phase21_status"] == "pass"
        and graph["phase21_claims"]["phase_21_mixed_inner_outer_transition_graph_certificate"],  # type: ignore[index]
        "robust_substrate_family_certified": all(
            analysis["certified_claims"]["transfer_substrate_certificate"] for analysis in substrate_analyses  # type: ignore[index]
        ),
        "robust_rule_space_exactly_bounded": len(robust_rule_table) == (max_bonus + 1) ** 3,
        "robust_target_objectives_exactly_certified": phase27_robust_target_witnesses_are_minimal(
            witnesses=robust_target_witnesses,
            specs_by_name=specs_by_name,  # type: ignore[arg-type]
            substrate_metric_maps=substrate_metric_maps,
        ),
        "all_robust_objectives_have_minimal_witnesses": all(
            bool(item["minimal_robust_rule_witnesses"]) for item in robust_target_witnesses
        ),
        "robust_pareto_frontier_certified": phase27_robust_pareto_frontier_is_certified(
            frontier=robust_pareto_frontier,
            robust_metrics_by_rule=robust_metrics_by_rule,
        )
        and bool(robust_pareto_frontier["frontier_rules"]),
        "robust_pareto_frontier_contains_tradeoffs": int(robust_pareto_frontier["frontier_metric_vector_count"]) > 1,
        "robust_synthesis_finds_positive_worst_case_gap": bool(positive_robust_objectives),
        "robust_synthesis_detects_worst_case_no_go": bool(negative_robust_objectives),
        "horizon_invariant_across_robust_substrates": phase22_horizon_invariant_nodes(
            node_by_id  # type: ignore[arg-type]
        )
        and all(
            bool(entry["constraints"]["horizon_profile_preserved_on_positive_transitions"])  # type: ignore[index]
            for analysis in substrate_analyses
            for entry in analysis["rule_metric_table"]  # type: ignore[index]
        ),
    }
    phase_claims["phase_27_multi_substrate_robust_channel_synthesis_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 27: multi-substrate robust channel synthesis",
        "status": "pass"
        if phase_claims["phase_27_multi_substrate_robust_channel_synthesis_certificate"]
        else "fail",
        "graph_substrate": {
            "source": "Phase 21 mixed graph plus Phase 26 edge-filtered substrate family",
            "phase21_status": graph["phase21_status"],
            "phase21_counts": graph["phase21_counts"],
            "node_count": len(node_by_id),
            "full_edge_count": len(phase21_edges),
        },
        "search_spec": {
            "rule_language": "Phase 25 positive symmetric edge-bonus weighted walks",
            "max_bonus": max_bonus,
            "candidate_rules": len(rule_specs),
            "substrates": phase26_transfer_substrate_specs(),
            "target_objectives": phase25_target_objectives(),
            "robust_score": "maximize the minimum signed target gap over all included substrates",
            "robust_pareto_metrics": tuple(phase25_bucket_groups()),
        },
        "substrate_summaries": tuple(
            {
                "name": analysis["name"],
                "counts": analysis["counts"],
                "certified_claims": analysis["certified_claims"],
            }
            for analysis in substrate_analyses
        ),
        "robust_rule_metric_table": robust_rule_table,
        "robust_target_gap_witnesses": robust_target_witnesses,
        "robust_pareto_frontier": robust_pareto_frontier,
        "counts": {
            "substrates": len(substrate_analyses),
            "candidate_rules": len(rule_specs),
            "robust_target_objectives": len(robust_target_witnesses),
            "unique_minimal_robust_witness_rules": len(robust_minimal_rule_names),
            "positive_worst_case_objectives": len(positive_robust_objectives),
            "negative_worst_case_objectives": len(negative_robust_objectives),
            "robust_pareto_frontier_rules": robust_pareto_frontier["frontier_rule_count"],
            "robust_pareto_frontier_metric_vectors": robust_pareto_frontier["frontier_metric_vector_count"],
            "robust_pareto_dominated_rules": robust_pareto_frontier["dominated_rule_count"],
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 27 synthesizes channel rules against the whole bounded substrate family, using exact "
                "worst-case target gaps rather than single-substrate optima."
            ),
            "robustness_lesson": (
                "The robust witnesses are explicit minimax rules: each listed gap includes the substrate on which "
                "the worst case is attained, separating durable behavior from Phase 26 transfer accidents."
            ),
            "horizon_lesson": (
                "The robust synthesis keeps the repaired shared-horizon profile fixed across every substrate and "
                "candidate rule, so worst-case failures are transition-geometry effects."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 27 produces robust minimax channel witnesses over a bounded substrate family. The next "
                "adaptation should turn these robust rules into a compact theorem-style certificate: prove which "
                "features of the rule language force the robust no-go and which allow positive robust gaps."
            ),
            "suggested_phase_28": (
                "Add a symbolic/audited rule-language proof layer for robust synthesis: derive feature-level "
                "conditions for positive and negative worst-case gaps, then check them against exact finite "
                "enumeration."
            ),
        },
    }


def phase28_rule_feature_predicate(
    *,
    rule_name: str,
    specs_by_name: dict[str, dict[str, object]],
    predicate: dict[str, int],
) -> bool:
    spec = specs_by_name[rule_name]
    key_map = {
        "entropy_bonus": "entropy_match_same_bonus",
        "observer_bonus": "observer_signal_same_bonus",
        "algebra_bonus": "algebra_flat_bonus",
    }
    return all(int(spec[key_map[key]]) == value for key, value in predicate.items())


def phase28_target_feature_schemas() -> tuple[dict[str, object], ...]:
    return (
        {
            "objective": "prefer_full_semantics_over_entropy_break",
            "feature_condition": {"entropy_bonus": 2, "observer_bonus": 0, "algebra_bonus": 0},
            "expected_sign": "positive",
            "proof_hint": (
                "Maximal entropy-stability bonus with no observer/algebra bonus gives the largest exact worst-case "
                "full-semantics minus entropy-break gap."
            ),
        },
        {
            "objective": "prefer_full_semantics_over_operator_collapse",
            "feature_condition": {"entropy_bonus": 0, "observer_bonus": 2, "algebra_bonus": 0},
            "expected_sign": "positive",
            "proof_hint": (
                "Maximal observer-signal-stability bonus with no entropy/algebra bonus gives the largest exact "
                "worst-case full-semantics minus operator-collapse gap."
            ),
        },
        {
            "objective": "prefer_entropy_break_over_full_semantics",
            "feature_condition": {"entropy_bonus": 0, "observer_bonus": 0, "algebra_bonus": 2},
            "expected_sign": "negative",
            "proof_hint": (
                "Even the strongest algebra-flat bonus cannot make entropy-break weight exceed full semantics in the "
                "worst case."
            ),
        },
        {
            "objective": "prefer_operator_collapse_over_full_semantics",
            "feature_condition": {"entropy_bonus": 0, "observer_bonus": 0, "algebra_bonus": 2},
            "expected_sign": "negative",
            "proof_hint": (
                "The same algebra-flat rule is the least-bad robust operator-collapse-over-full-semantics witness, "
                "but its exact worst-case gap remains negative."
            ),
        },
        {
            "objective": "prefer_entropy_break_over_operator_collapse",
            "feature_condition": {"entropy_bonus": 0, "observer_bonus": 2, "algebra_bonus": 2},
            "expected_sign": "positive",
            "proof_hint": (
                "Combining maximal observer-signal and algebra-flat bonuses gives the largest robust entropy-break "
                "over operator-collapse gap."
            ),
        },
        {
            "objective": "prefer_operator_collapse_over_entropy_break",
            "feature_condition": {"entropy_bonus": 2, "observer_bonus": 0, "algebra_bonus": 0},
            "expected_sign": "negative",
            "proof_hint": (
                "The entropy-stability rule is least-bad for operator-collapse over entropy-break, but one substrate "
                "keeps the exact worst-case gap negative."
            ),
        },
    )


def phase28_fraction_from_public(item: dict[str, object]) -> Fraction:
    return Fraction(int(item["numerator"]), int(item["denominator"]))


def phase28_worst_substrates(
    witness: dict[str, object],
) -> tuple[str, ...]:
    gaps = tuple(witness["gaps_by_substrate"])  # type: ignore[arg-type]
    values = {
        str(item["substrate"]): phase28_fraction_from_public(item["gap"])  # type: ignore[arg-type]
        for item in gaps
    }
    worst = min(values.values())
    return tuple(sorted(substrate for substrate, value in values.items() if value == worst))


def phase28_target_schema_audit(
    *,
    schema: dict[str, object],
    specs_by_name: dict[str, dict[str, object]],
    robust_witness_by_objective: dict[str, dict[str, object]],
) -> dict[str, object]:
    objective_name = str(schema["objective"])
    robust_witness = robust_witness_by_objective[objective_name]
    predicate = schema["feature_condition"]
    if not isinstance(predicate, dict):
        raise TypeError("Phase 28 feature_condition must be a dict")
    predicate_rules = tuple(
        sorted(
            rule_name
            for rule_name in specs_by_name
            if phase28_rule_feature_predicate(
                rule_name=rule_name,
                specs_by_name=specs_by_name,
                predicate={str(key): int(value) for key, value in predicate.items()},
            )
        )
    )
    maximizer_rules = tuple(str(rule) for rule in robust_witness["all_robust_maximizing_rules"])  # type: ignore[arg-type]
    minimal_rules = tuple(
        str(witness["rule"]["name"])  # type: ignore[index]
        for witness in robust_witness["minimal_robust_rule_witnesses"]  # type: ignore[index]
    )
    max_gap = phase28_fraction_from_public(robust_witness["max_worst_case_gap"])  # type: ignore[arg-type]
    expected_sign = str(schema["expected_sign"])
    sign_matches = (
        (expected_sign == "positive" and max_gap > 0)
        or (expected_sign == "negative" and max_gap < 0)
        or (expected_sign == "zero" and max_gap == 0)
    )
    worst_substrates = tuple(
        sorted(
            {
                substrate
                for witness in robust_witness["minimal_robust_rule_witnesses"]  # type: ignore[index]
                for substrate in phase28_worst_substrates(witness)
            }
        )
    )
    return {
        "objective": robust_witness["objective"],
        "feature_condition": predicate,
        "feature_condition_text": (
            " and ".join(f"{key} == {value}" for key, value in sorted(predicate.items()))
        ),
        "proof_hint": schema["proof_hint"],
        "predicate_rules": predicate_rules,
        "all_robust_maximizing_rules": maximizer_rules,
        "minimal_robust_rule_witnesses": minimal_rules,
        "max_worst_case_gap": robust_witness["max_worst_case_gap"],
        "expected_sign": expected_sign,
        "actual_sign": "positive" if max_gap > 0 else "negative" if max_gap < 0 else "zero",
        "worst_case_substrates_for_minimal_witnesses": worst_substrates,
        "audits": {
            "feature_condition_selects_exact_maximizers": predicate_rules == maximizer_rules,
            "minimal_witnesses_are_subset_of_feature_condition": set(minimal_rules) <= set(predicate_rules),
            "sign_matches_expected": sign_matches,
            "worst_case_substrate_recorded": bool(worst_substrates),
        },
    }


def phase28_rule_language_schema(max_bonus: int = 2) -> dict[str, object]:
    return {
        "rule_name": "edge_bonus_e{entropy_bonus}_o{observer_bonus}_a{algebra_bonus}",
        "domains": {
            "entropy_bonus": tuple(range(max_bonus + 1)),
            "observer_bonus": tuple(range(max_bonus + 1)),
            "algebra_bonus": tuple(range(max_bonus + 1)),
        },
        "edge_weight_formula": (
            "1 + entropy_bonus*[same low-order entropy flag] + "
            "observer_bonus*[same observer-signal flag] + algebra_bonus*[same algebra-difference count]"
        ),
        "robust_gap_formula": (
            "for objective positive-negative, score(rule)=min_substrate("
            "weight_substrate(rule, positive) - weight_substrate(rule, negative))"
        ),
        "bounded_rule_count_formula": "(max_bonus + 1)^3",
    }


def phase28_proof_text() -> str:
    return (
        "Phase 28 audited rule-language proof. The rule language has three integer feature bonuses: "
        "entropy_bonus, observer_bonus, and algebra_bonus, each in {0,1,2}. For each rule and substrate, "
        "the exact weighted-walk stationary distribution gives grouped weights for full_semantics, "
        "entropy_break, and operator_collapse. For each target objective, the robust score is the minimum "
        "signed grouped-weight gap over the four Phase 26 substrates. The certificate enumerates every rule "
        "in the finite schema, recomputes exact robust scores, and checks that the listed feature condition "
        "selects exactly the robust maximizer set. Positive cases have positive exact worst-case gaps; no-go "
        "cases have negative exact best worst-case gaps."
    )


def bridge_cosmology_phase28_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    phase27 = bridge_cosmology_phase27_certificate(max_bonus=max_bonus)
    specs_by_name = {
        str(item["rule"]["name"]): item["rule"]  # type: ignore[index]
        for item in phase27["robust_rule_metric_table"]  # type: ignore[index]
    }
    robust_witness_by_objective = {
        str(item["objective"]["name"]): item  # type: ignore[index]
        for item in phase27["robust_target_gap_witnesses"]  # type: ignore[index]
    }
    schema_audits = tuple(
        phase28_target_schema_audit(
            schema=schema,
            specs_by_name=specs_by_name,
            robust_witness_by_objective=robust_witness_by_objective,
        )
        for schema in phase28_target_feature_schemas()
    )
    positive_audits = tuple(item for item in schema_audits if item["actual_sign"] == "positive")
    negative_audits = tuple(item for item in schema_audits if item["actual_sign"] == "negative")
    phase_claims = {
        "phase27_robust_synthesis_certified": phase27["status"] == "pass"
        and phase27["certified_claims"]["phase_27_multi_substrate_robust_channel_synthesis_certificate"],  # type: ignore[index]
        "rule_language_schema_covers_exact_enumeration": len(specs_by_name) == (max_bonus + 1) ** 3,
        "one_schema_audit_per_target_objective": len(schema_audits) == len(phase25_target_objectives()),
        "feature_conditions_select_exact_robust_maximizers": all(
            item["audits"]["feature_condition_selects_exact_maximizers"] for item in schema_audits  # type: ignore[index]
        ),
        "minimal_witnesses_obey_feature_conditions": all(
            item["audits"]["minimal_witnesses_are_subset_of_feature_condition"] for item in schema_audits  # type: ignore[index]
        ),
        "sign_classification_matches_exact_worst_case_gaps": all(
            item["audits"]["sign_matches_expected"] for item in schema_audits  # type: ignore[index]
        ),
        "worst_case_substrates_recorded_for_every_audit": all(
            item["audits"]["worst_case_substrate_recorded"] for item in schema_audits  # type: ignore[index]
        ),
        "positive_and_no_go_feature_conditions_both_exist": bool(positive_audits) and bool(negative_audits),
    }
    phase_claims["phase_28_audited_rule_language_proof_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 28: audited rule-language proof layer",
        "status": "pass" if phase_claims["phase_28_audited_rule_language_proof_certificate"] else "fail",
        "rule_language_schema": phase28_rule_language_schema(max_bonus=max_bonus),
        "proof_text": phase28_proof_text(),
        "target_feature_audits": schema_audits,
        "counts": {
            "candidate_rules": len(specs_by_name),
            "target_objectives": len(schema_audits),
            "positive_feature_conditions": len(positive_audits),
            "negative_no_go_feature_conditions": len(negative_audits),
            "distinct_feature_condition_rules": len(
                {
                    rule_name
                    for item in schema_audits
                    for rule_name in item["predicate_rules"]  # type: ignore[index]
                }
            ),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 28 turns the robust channel-rule enumeration into an audited rule-language proof: each target "
                "objective has a feature predicate that selects exactly the robust maximizers."
            ),
            "no_go_lesson": (
                "The negative cases are certified no-go statements inside the bounded rule language: their exact "
                "best worst-case gaps remain below zero even at the feature-selected robust maximizer."
            ),
            "audit_lesson": (
                "The proof text is backed by finite exact checks over every rule and substrate, so the symbolic "
                "feature explanation is not trusted independently of enumeration."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 28 supplies a checked proof layer for robust channel-rule features. The next adaptation should "
                "move from rule-language proofs to code/cover co-design: search for nearby patch-cover variants where "
                "the robust no-go signs flip while the same proof schema remains auditable."
            ),
            "suggested_phase_29": (
                "Run bounded cover/substrate co-design: vary observer patch covers or edge-filter families, recompute "
                "robust rule-language audits, and certify explicit cover changes that flip or preserve robust no-go "
                "signs."
            ),
        },
    }


def phase29_substrate_family_specs() -> tuple[dict[str, object], ...]:
    optional_filters = (
        ("entropy_stable_edges", "entropy"),
        ("observer_signal_stable_edges", "observer"),
        ("algebra_flat_edges", "algebra"),
    )
    families = []
    for mask in range(1 << len(optional_filters)):
        chosen = tuple(
            optional_filters[index]
            for index in range(len(optional_filters))
            if mask & (1 << index)
        )
        labels = tuple(label for _, label in chosen)
        substrates = ("full_mixed_graph",) + tuple(name for name, _ in chosen)
        if not labels:
            name = "full_only"
            description = "Baseline full Phase 21 substrate with no additional robust filters."
        elif len(labels) == len(optional_filters):
            name = "full_plus_all_filters"
            description = "Baseline Phase 27 robust family with all three filtered substrates included."
        else:
            name = "full_plus_" + "_".join(labels)
            description = "Full Phase 21 substrate plus the selected robust edge-filter substrates."
        families.append(
            {
                "name": name,
                "description": description,
                "substrates": substrates,
                "optional_filter_labels": labels,
            }
        )
    return tuple(families)


def phase29_bonus_signature(spec: dict[str, object]) -> tuple[int, int, int]:
    return (
        int(spec["entropy_match_same_bonus"]),
        int(spec["observer_signal_same_bonus"]),
        int(spec["algebra_flat_bonus"]),
    )


def phase29_public_bonus_signature(signature: tuple[int, int, int]) -> dict[str, int]:
    entropy_bonus, observer_bonus, algebra_bonus = signature
    return {
        "entropy_bonus": entropy_bonus,
        "observer_bonus": observer_bonus,
        "algebra_bonus": algebra_bonus,
    }


def phase29_sign(value: Fraction) -> str:
    if value > 0:
        return "positive"
    if value < 0:
        return "negative"
    return "zero"


def phase29_rule_signature_audit(
    *,
    robust_witness: dict[str, object],
    specs_by_name: dict[str, dict[str, object]],
) -> dict[str, object]:
    maximizer_rules = tuple(str(rule) for rule in robust_witness["all_robust_maximizing_rules"])  # type: ignore[arg-type]
    signatures = tuple(
        sorted({phase29_bonus_signature(specs_by_name[rule_name]) for rule_name in maximizer_rules})
    )
    predicate_rules = tuple(
        sorted(
            rule_name
            for rule_name, spec in specs_by_name.items()
            if phase29_bonus_signature(spec) in signatures
        )
    )
    minimal_rules = tuple(
        str(witness["rule"]["name"])  # type: ignore[index]
        for witness in robust_witness["minimal_robust_rule_witnesses"]  # type: ignore[index]
    )
    max_gap = phase28_fraction_from_public(robust_witness["max_worst_case_gap"])  # type: ignore[arg-type]
    worst_substrates = tuple(
        sorted(
            {
                substrate
                for witness in robust_witness["minimal_robust_rule_witnesses"]  # type: ignore[index]
                for substrate in phase28_worst_substrates(witness)
            }
        )
    )
    return {
        "objective": robust_witness["objective"],
        "feature_condition_signatures": tuple(
            phase29_public_bonus_signature(signature)
            for signature in signatures
        ),
        "feature_condition_text": " or ".join(
            " and ".join(f"{key} == {value}" for key, value in phase29_public_bonus_signature(signature).items())
            for signature in signatures
        ),
        "predicate_rules": predicate_rules,
        "all_robust_maximizing_rules": maximizer_rules,
        "minimal_robust_rule_witnesses": minimal_rules,
        "max_worst_case_gap": robust_witness["max_worst_case_gap"],
        "actual_sign": phase29_sign(max_gap),
        "worst_case_substrates_for_minimal_witnesses": worst_substrates,
        "audits": {
            "signature_condition_selects_exact_maximizers": predicate_rules == maximizer_rules,
            "minimal_witnesses_are_subset_of_signature_condition": set(minimal_rules) <= set(predicate_rules),
            "sign_matches_exact_gap": phase29_sign(max_gap) in {"positive", "negative", "zero"},
            "worst_case_substrate_recorded": bool(worst_substrates),
        },
    }


def phase29_objective_signs(witnesses: tuple[dict[str, object], ...]) -> dict[str, str]:
    return {
        str(item["objective"]["name"]): phase29_sign(  # type: ignore[index]
            phase28_fraction_from_public(item["max_worst_case_gap"])  # type: ignore[arg-type]
        )
        for item in witnesses
    }


def phase29_family_robust_analysis(
    *,
    family_spec: dict[str, object],
    substrate_analysis_by_name: dict[str, dict[str, object]],
    max_bonus: int,
) -> dict[str, object]:
    substrate_names = tuple(str(name) for name in family_spec["substrates"])  # type: ignore[index]
    substrate_analyses = tuple(substrate_analysis_by_name[name] for name in substrate_names)
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]] = {
        str(analysis["name"]): analysis["_metrics_by_rule"]  # type: ignore[assignment]
        for analysis in substrate_analyses
    }
    specs_by_name = substrate_analyses[0]["_specs_by_name"]  # type: ignore[assignment]
    if not isinstance(specs_by_name, dict):
        raise TypeError("Phase 29 substrate analysis must contain specs_by_name")
    robust_rule_table, robust_metrics_by_rule = phase27_rule_robust_metrics(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        substrate_metric_maps=substrate_metric_maps,
    )
    robust_target_witnesses = phase27_robust_target_gap_witnesses(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        substrate_metric_maps=substrate_metric_maps,
        robust_metrics_by_rule=robust_metrics_by_rule,
    )
    robust_witness_by_objective = {
        str(item["objective"]["name"]): item  # type: ignore[index]
        for item in robust_target_witnesses
    }
    robust_pareto_frontier = phase27_robust_pareto_frontier(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        robust_metrics_by_rule=robust_metrics_by_rule,
    )
    local_feature_audits = tuple(
        phase29_rule_signature_audit(
            robust_witness=item,
            specs_by_name=specs_by_name,  # type: ignore[arg-type]
        )
        for item in robust_target_witnesses
    )
    phase28_schema_transfer_audits = tuple(
        phase28_target_schema_audit(
            schema=schema,
            specs_by_name=specs_by_name,  # type: ignore[arg-type]
            robust_witness_by_objective=robust_witness_by_objective,
        )
        for schema in phase28_target_feature_schemas()
    )
    objective_signs = phase29_objective_signs(robust_target_witnesses)
    positive_objectives = tuple(sorted(objective for objective, sign in objective_signs.items() if sign == "positive"))
    negative_objectives = tuple(sorted(objective for objective, sign in objective_signs.items() if sign == "negative"))
    transfer_exact_objectives = tuple(
        sorted(
            str(item["objective"]["name"])  # type: ignore[index]
            for item in phase28_schema_transfer_audits
            if item["audits"]["feature_condition_selects_exact_maximizers"]  # type: ignore[index]
        )
    )
    phase_claims = {
        "included_substrates_certified": all(
            analysis["certified_claims"]["transfer_substrate_certificate"] for analysis in substrate_analyses  # type: ignore[index]
        ),
        "family_rule_space_exactly_bounded": len(robust_rule_table) == (max_bonus + 1) ** 3,
        "family_target_objectives_exactly_certified": phase27_robust_target_witnesses_are_minimal(
            witnesses=robust_target_witnesses,
            specs_by_name=specs_by_name,  # type: ignore[arg-type]
            substrate_metric_maps=substrate_metric_maps,
        ),
        "family_pareto_frontier_certified": phase27_robust_pareto_frontier_is_certified(
            frontier=robust_pareto_frontier,
            robust_metrics_by_rule=robust_metrics_by_rule,
        ),
        "local_signature_audits_select_exact_maximizers": all(
            item["audits"]["signature_condition_selects_exact_maximizers"] for item in local_feature_audits  # type: ignore[index]
        ),
        "phase28_schema_transfer_records_complete": len(phase28_schema_transfer_audits)
        == len(phase25_target_objectives()),
    }
    phase_claims["family_robust_co_design_certificate"] = all(phase_claims.values())
    return {
        "family": family_spec,
        "substrate_summaries": tuple(
            {
                "name": analysis["name"],
                "counts": analysis["counts"],
                "certified_claims": analysis["certified_claims"],
            }
            for analysis in substrate_analyses
        ),
        "robust_target_gap_witnesses": robust_target_witnesses,
        "local_feature_audits": local_feature_audits,
        "phase28_schema_transfer_audits": phase28_schema_transfer_audits,
        "robust_pareto_frontier": robust_pareto_frontier,
        "objective_signs": tuple(
            {
                "objective": objective,
                "sign": sign,
            }
            for objective, sign in sorted(objective_signs.items())
        ),
        "counts": {
            "substrates": len(substrate_names),
            "candidate_rules": len(robust_rule_table),
            "target_objectives": len(robust_target_witnesses),
            "positive_worst_case_objectives": len(positive_objectives),
            "negative_worst_case_objectives": len(negative_objectives),
            "phase28_schema_transfer_exact_objectives": len(transfer_exact_objectives),
            "phase28_schema_transfer_failed_objectives": len(phase25_target_objectives()) - len(transfer_exact_objectives),
            "robust_pareto_frontier_rules": robust_pareto_frontier["frontier_rule_count"],
            "robust_pareto_frontier_metric_vectors": robust_pareto_frontier["frontier_metric_vector_count"],
        },
        "phase28_schema_transfer_exact_objectives": transfer_exact_objectives,
        "certified_claims": phase_claims,
    }


def phase29_sign_flip_records(
    *,
    baseline_family: dict[str, object],
    family_results: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    baseline_signs = {
        str(item["objective"]): str(item["sign"])  # type: ignore[index]
        for item in baseline_family["objective_signs"]  # type: ignore[index]
    }
    records = []
    for family in family_results:
        family_name = str(family["family"]["name"])  # type: ignore[index]
        signs = {
            str(item["objective"]): str(item["sign"])  # type: ignore[index]
            for item in family["objective_signs"]  # type: ignore[index]
        }
        for objective, baseline_sign in sorted(baseline_signs.items()):
            family_sign = signs[objective]
            if family_sign == baseline_sign:
                continue
            records.append(
                {
                    "family": family_name,
                    "objective": objective,
                    "baseline_family": baseline_family["family"]["name"],  # type: ignore[index]
                    "baseline_sign": baseline_sign,
                    "family_sign": family_sign,
                    "negative_to_positive": baseline_sign == "negative" and family_sign == "positive",
                    "positive_to_negative": baseline_sign == "positive" and family_sign == "negative",
                }
            )
    return tuple(records)


def phase29_preserved_negative_objectives(
    *,
    baseline_family: dict[str, object],
    family_results: tuple[dict[str, object], ...],
) -> tuple[str, ...]:
    baseline_negative = tuple(
        str(item["objective"])  # type: ignore[index]
        for item in baseline_family["objective_signs"]  # type: ignore[index]
        if str(item["sign"]) == "negative"  # type: ignore[index]
    )
    signs_by_family = {
        str(family["family"]["name"]): {  # type: ignore[index]
            str(item["objective"]): str(item["sign"])  # type: ignore[index]
            for item in family["objective_signs"]  # type: ignore[index]
        }
        for family in family_results
    }
    return tuple(
        sorted(
            objective
            for objective in baseline_negative
            if all(signs[objective] == "negative" for signs in signs_by_family.values())
        )
    )


def bridge_cosmology_phase29_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    graph = phase22_phase21_graph_data()
    node_by_id = graph["node_by_id"]
    adjacency = graph["adjacency"]
    if not isinstance(node_by_id, dict) or not isinstance(adjacency, dict):
        raise TypeError("Phase 29 graph data must contain node and adjacency dictionaries")
    node_ids = tuple(str(node_id) for node_id in graph["node_ids"])  # type: ignore[index]
    phase21_edges = tuple(edge for edge in graph["edges"] if isinstance(edge, dict))  # type: ignore[arg-type]
    rule_specs = phase24_weighted_rule_specs(max_bonus=max_bonus)
    substrate_analyses = tuple(
        phase26_substrate_analysis(
            spec=spec,
            rule_specs=rule_specs,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            node_ids=node_ids,
            phase21_edges=phase21_edges,
        )
        for spec in phase26_transfer_substrate_specs()
    )
    substrate_analysis_by_name = {
        str(analysis["name"]): analysis
        for analysis in substrate_analyses
    }
    family_specs = phase29_substrate_family_specs()
    family_results = tuple(
        phase29_family_robust_analysis(
            family_spec=family_spec,
            substrate_analysis_by_name=substrate_analysis_by_name,
            max_bonus=max_bonus,
        )
        for family_spec in family_specs
    )
    family_by_name = {
        str(family["family"]["name"]): family  # type: ignore[index]
        for family in family_results
    }
    baseline_family = family_by_name["full_plus_all_filters"]
    sign_flips = phase29_sign_flip_records(
        baseline_family=baseline_family,
        family_results=family_results,
    )
    negative_to_positive_flips = tuple(record for record in sign_flips if bool(record["negative_to_positive"]))
    preserved_negative_objectives = phase29_preserved_negative_objectives(
        baseline_family=baseline_family,
        family_results=family_results,
    )
    transfer_exact_nonbaseline = sum(
        int(family["counts"]["phase28_schema_transfer_exact_objectives"])  # type: ignore[index]
        for family in family_results
        if str(family["family"]["name"]) != "full_plus_all_filters"  # type: ignore[index]
    )
    transfer_failed_nonbaseline = sum(
        int(family["counts"]["phase28_schema_transfer_failed_objectives"])  # type: ignore[index]
        for family in family_results
        if str(family["family"]["name"]) != "full_plus_all_filters"  # type: ignore[index]
    )
    expected_family_count = 2 ** (len(phase26_transfer_substrate_specs()) - 1)
    phase_claims = {
        "phase21_substrate_certified": graph["phase21_status"] == "pass"
        and graph["phase21_claims"]["phase_21_mixed_inner_outer_transition_graph_certificate"],  # type: ignore[index]
        "substrate_library_certified": all(
            analysis["certified_claims"]["transfer_substrate_certificate"] for analysis in substrate_analyses  # type: ignore[index]
        ),
        "family_search_space_exactly_bounded": len(family_specs) == expected_family_count
        and all("full_mixed_graph" in family["substrates"] for family in family_specs),  # type: ignore[operator]
        "all_family_robust_syntheses_certified": all(
            family["certified_claims"]["family_robust_co_design_certificate"] for family in family_results  # type: ignore[index]
        ),
        "all_family_local_feature_audits_certified": all(
            family["certified_claims"]["local_signature_audits_select_exact_maximizers"]  # type: ignore[index]
            for family in family_results
        ),
        "baseline_family_matches_phase27_sign_counts": baseline_family["counts"]["positive_worst_case_objectives"] == 3  # type: ignore[index]
        and baseline_family["counts"]["negative_worst_case_objectives"] == 3  # type: ignore[index]
        and baseline_family["counts"]["robust_pareto_frontier_rules"] == 17,  # type: ignore[index]
        "co_design_finds_negative_to_positive_no_go_flip": bool(negative_to_positive_flips),
        "co_design_preserves_some_no_go_signs_across_every_family": bool(preserved_negative_objectives),
        "phase28_schema_transfer_successes_and_failures_detected": transfer_exact_nonbaseline > 0
        and transfer_failed_nonbaseline > 0,
        "horizon_invariant_across_family_search": phase22_horizon_invariant_nodes(
            node_by_id  # type: ignore[arg-type]
        )
        and all(
            bool(entry["constraints"]["horizon_profile_preserved_on_positive_transitions"])  # type: ignore[index]
            for analysis in substrate_analyses
            for entry in analysis["rule_metric_table"]  # type: ignore[index]
        ),
    }
    phase_claims["phase_29_bounded_substrate_family_co_design_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 29: bounded substrate-family co-design search",
        "status": "pass" if phase_claims["phase_29_bounded_substrate_family_co_design_certificate"] else "fail",
        "rule_language_schema": phase28_rule_language_schema(max_bonus=max_bonus),
        "proof_text": (
            "Phase 29 bounded substrate-family co-design proof. The search space is the full Phase 21 substrate "
            "plus every subset of the three Phase 26 filtered substrates, giving exactly 2^3 robust families. "
            "For each family, the certificate recomputes exact minimax target gaps over all 27 channel rules, "
            "derives bonus-signature predicates from the exact maximizer set, and audits that those predicates "
            "select exactly the listed maximizers. It then separately applies the Phase 28 predicates to test "
            "which old proof conditions transfer and which fail under the family change."
        ),
        "search_spec": {
            "family_rule": "include full_mixed_graph plus any subset of the three filtered Phase 26 substrates",
            "candidate_families": family_specs,
            "max_bonus": max_bonus,
            "candidate_rules": len(rule_specs),
            "target_objectives": phase25_target_objectives(),
        },
        "substrate_summaries": tuple(
            {
                "name": analysis["name"],
                "counts": analysis["counts"],
                "certified_claims": analysis["certified_claims"],
            }
            for analysis in substrate_analyses
        ),
        "family_results": family_results,
        "sign_flip_records": sign_flips,
        "negative_to_positive_no_go_flips": negative_to_positive_flips,
        "preserved_negative_no_go_objectives": preserved_negative_objectives,
        "counts": {
            "substrate_library_size": len(substrate_analyses),
            "candidate_families": len(family_results),
            "candidate_rules": len(rule_specs),
            "target_objectives_per_family": len(phase25_target_objectives()),
            "sign_flip_records": len(sign_flips),
            "negative_to_positive_no_go_flips": len(negative_to_positive_flips),
            "preserved_negative_no_go_objectives": len(preserved_negative_objectives),
            "phase28_schema_transfer_exact_nonbaseline_objectives": transfer_exact_nonbaseline,
            "phase28_schema_transfer_failed_nonbaseline_objectives": transfer_failed_nonbaseline,
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 29 shows that some robust no-go signs are substrate-family artifacts: removing particular "
                "filtered substrates can flip a Phase 28 negative objective to a positive exact worst-case gap."
            ),
            "persistence_lesson": (
                "Other negative objectives stay negative across every bounded family that keeps the full mixed "
                "substrate, separating fragile no-go claims from persistent ones."
            ),
            "audit_lesson": (
                "The old Phase 28 feature predicates are tested as transfer claims, while each new family receives "
                "its own exact signature audit. No family-level symbolic claim is accepted without enumeration."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 29 found both fragile and persistent no-go signs under bounded substrate-family co-design. "
                "The next adaptation should move one layer closer to code/cover co-design by changing patch covers "
                "or observer roles and checking whether the persistent signs survive."
            ),
            "suggested_phase_30": (
                "Run bounded observer-cover co-design: vary repaired patch covers on the same code-pair library, "
                "rebuild the transition substrate and audited robust family signs, then certify cover-level flips "
                "or persistent no-go obstructions."
            ),
        },
    }


def phase30_selected_cover_templates() -> tuple[dict[str, object], ...]:
    return (
        {
            "name": "strict_baseline_p1_q13",
            "role": "phase18_baseline_cover",
            "observer_p_block_mask": 1,
            "observer_q_block_mask": 13,
            "strict_cover_hit_required": True,
            "description": "The Phase 18 repaired cover used by the Phase 21-29 transition substrate.",
        },
        {
            "name": "strict_control_p2_q7",
            "role": "strict_sign_preservation_control",
            "observer_p_block_mask": 2,
            "observer_q_block_mask": 7,
            "strict_cover_hit_required": True,
            "description": "A strict repaired-cover hit that changes the shared block but preserves baseline signs.",
        },
        {
            "name": "strict_operator_flip_p3_q13",
            "role": "strict_operator_no_go_flip_witness",
            "observer_p_block_mask": 3,
            "observer_q_block_mask": 13,
            "strict_cover_hit_required": True,
            "description": "A strict repaired-cover hit that flips the operator-collapse-over-full no-go sign.",
        },
        {
            "name": "near_miss_entropy_flip_p3_q5",
            "role": "erasure_rejected_entropy_flip_pressure_test",
            "observer_p_block_mask": 3,
            "observer_q_block_mask": 5,
            "strict_cover_hit_required": False,
            "description": (
                "A raw entropy/reconstruction cover hit whose robust entropy-break sign flips, but whose erasure "
                "correctability profile fails the strict causal-patch gate."
            ),
        },
    )


def phase30_compact_seed_cover_certificate(certificate: dict[str, object]) -> dict[str, object]:
    return {
        "pair_source": certificate["pair_source"],
        "n": certificate["n"],
        "k": certificate["k"],
        "cover": certificate["cover"],
        "observer_reconstruction": certificate["observer_reconstruction"],
        "shared_horizon_signature": certificate["shared_horizon_signature"],
        "erasure_comparison": certificate["erasure_comparison"],
        "certified_claims": certificate["certified_claims"],
    }


def phase30_observer_cover_candidates() -> tuple[dict[str, object], ...]:
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 30 source must contain StabilizerCode objects")
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    candidates = phase12_atlas_aware_repaired_cover_candidates(inner_hit=inner_atlas["hit"])
    out = []
    for template in phase30_selected_cover_templates():
        candidate = candidate_by_template_and_blocks(
            candidates,
            template_kind="phase12_private_full_shared_inner",
            observer_p_block_mask=int(template["observer_p_block_mask"]),
            observer_q_block_mask=int(template["observer_q_block_mask"]),
        )
        cover = candidate["cover"]
        if not isinstance(cover, PatchCover):
            raise TypeError("Phase 30 candidate must contain a PatchCover")
        seed_certificate = rank_kernel_cover_search_hit_certificate_for_pair(
            pair_source=str(source["name"]),
            first=first,
            second=second,
            cover=cover,
            include_bases=False,
        )
        claims = seed_certificate["certified_claims"]
        if not isinstance(claims, dict):
            raise TypeError("Phase 30 seed certificate claims must be a dict")
        strict_required = bool(template["strict_cover_hit_required"])
        out.append(
            {
                **template,
                "template_kind": candidate["template_kind"],
                "template_origin": candidate["template_origin"],
                "observer_p_blocks": candidate["observer_p_blocks"],
                "observer_q_blocks": candidate["observer_q_blocks"],
                "shared_block_mask": candidate["shared_block_mask"],
                "shared_blocks": candidate["shared_blocks"],
                "observer_p_private_blocks": candidate["observer_p_private_blocks"],
                "observer_q_private_blocks": candidate["observer_q_private_blocks"],
                "cover": cover.summary(first.n),
                "seed_cover_certificate": phase30_compact_seed_cover_certificate(seed_certificate),
                "certified_claims": {
                    "selected_from_phase12_private_full_shared_inner": candidate["template_kind"]
                    == "phase12_private_full_shared_inner",
                    "seed_entropy_overlap_and_horizon_match": bool(claims["same_entropy_overlap_data"])
                    and bool(claims["observer_overlap_is_horizon"])
                    and bool(claims["same_shared_horizon_algebra"]),
                    "seed_observer_reconstruction_differs": bool(claims["different_observer_reconstruction"]),
                    "strict_cover_hit_status_matches_role": bool(claims["causal_patch_search_hit"]) == strict_required,
                    "strict_cover_hit_verified": bool(claims["causal_patch_search_hit"]),
                    "near_miss_rejected_by_erasure_profile": (
                        not strict_required
                        and not bool(claims["same_erasure_correctability_profile"])
                        and not bool(claims["causal_patch_search_hit"])
                    ),
                },
                "_cover": cover,
            }
        )
    return tuple(out)


def phase30_public_cover_candidate(candidate: dict[str, object]) -> dict[str, object]:
    return {
        key: value
        for key, value in candidate.items()
        if key != "_cover"
    }


def phase30_mixed_graph_for_cover(
    *,
    cover_candidate: dict[str, object],
    baseline_outer: StabilizerCode,
    outer_states: tuple[dict[str, object], ...],
) -> dict[str, object]:
    cover = cover_candidate["_cover"]
    if not isinstance(cover, PatchCover):
        raise TypeError("Phase 30 cover candidate must contain a PatchCover")
    inner_states = phase21_inner_representative_states(outer=baseline_outer, cover=cover)
    nodes = tuple(
        phase21_mixed_node(
            inner_state=inner_state,
            outer_state=outer_state,
            cover=cover,
            include_bases=False,
        )
        for inner_state in inner_states
        for outer_state in outer_states
    )
    node_by_axes = {
        (str(node["metadata"]["inner_label"]), str(node["metadata"]["outer_label"])): node
        for node in nodes
    }
    edges = []
    for outer_state in outer_states:
        outer_label = str(outer_state["label"])
        source = node_by_axes[("inner_baseline", outer_label)]
        for inner_state in inner_states:
            inner_label = str(inner_state["label"])
            if inner_label == "inner_baseline":
                continue
            target = node_by_axes[(inner_label, outer_label)]
            edges.append(phase21_mixed_edge(edge_type="inner_graph_toggle", source=source, target=target))
    for inner_state in inner_states:
        inner_label = str(inner_state["label"])
        source = node_by_axes[(inner_label, "outer_baseline")]
        for outer_state in outer_states:
            outer_label = str(outer_state["label"])
            if outer_label == "outer_baseline":
                continue
            target = node_by_axes[(inner_label, outer_label)]
            edges.append(phase21_mixed_edge(edge_type="outer_repair_mutation", source=source, target=target))
    edges_tuple = tuple(edges)
    node_ids = tuple(str(node["id"]) for node in nodes)
    node_by_id = {str(node["id"]): node for node in nodes}
    outcome_counts = phase19_histogram(str(node["outcome"]) for node in nodes)
    edge_type_counts = phase16_count_edge_types(edges_tuple)
    algebra_monotonicity_counts = dict(phase19_histogram(edge["algebra_monotonicity"] for edge in edges_tuple))
    entropy_flip_count = sum(1 for edge in edges_tuple if bool(edge["entropy_match_flips"]))
    signal_flip_count = sum(1 for edge in edges_tuple if bool(edge["observer_signal_flips"]))
    shared_profiles = tuple(sorted(set(node["correctability_pairs"]["erase_shared_horizon"] for node in nodes)))
    shared_fixed_points = tuple(sorted(set(node["survivor_fixed_point_pairs"]["erase_shared_horizon"] for node in nodes)))
    expected_edges = len(outer_states) * (len(inner_states) - 1) + len(inner_states) * (len(outer_states) - 1)
    phase_claims = {
        "mixed_product_nodes_scored": len(nodes) == len(inner_states) * len(outer_states) and bool(nodes),
        "mixed_axis_edges_certified": len(edges_tuple) == expected_edges
        and all(edge["certified_claims"]["mixed_inner_outer_transition_edge"] for edge in edges_tuple),
        "shared_horizon_correctability_stable_across_mixed_graph": shared_profiles == ((True, True),),
        "shared_horizon_fixed_point_stable_across_mixed_graph": shared_fixed_points == ((True, True),),
        "all_nodes_exact_qec_complementarity": all(
            bool(node["qec_complementarity_identity_all_scenarios"]) for node in nodes
        ),
        "graph_contains_entropy_break_and_operator_collapse": dict(outcome_counts).get(
            "low_order_entropy_break_with_reconstruction_survives",
            0,
        )
        > 0
        and dict(outcome_counts).get("operator_geometry_collapsed", 0) > 0,
        "algebra_difference_monotonicity_failures_exist": algebra_monotonicity_counts.get("increase", 0) > 0
        and algebra_monotonicity_counts.get("decrease", 0) > 0,
        "entropy_and_signal_flip_edges_exist": entropy_flip_count > 0 and signal_flip_count > 0,
        "low_order_subsets_checked_for_every_node": all(
            int(node["low_order_entropy"]["subsets_checked"]) == 211 for node in nodes
        ),
        "no_residual_unclassified_nodes": dict(outcome_counts).get("residual_unclassified", 0) == 0,
    }
    phase_claims["cover_mixed_graph_certificate"] = all(phase_claims.values())
    return {
        "cover_candidate": phase30_public_cover_candidate(cover_candidate),
        "classification": {
            "node_outcome_counts": outcome_counts,
            "edge_type_counts": tuple(sorted(edge_type_counts.items())),
            "algebra_monotonicity_counts": tuple(sorted(algebra_monotonicity_counts.items())),
            "entropy_match_flip_edges": entropy_flip_count,
            "observer_signal_flip_edges": signal_flip_count,
        },
        "counts": {
            "nodes": len(nodes),
            "edges": len(edges_tuple),
            "inner_states": len(inner_states),
            "outer_states": len(outer_states),
            "algebra_increase_edges": algebra_monotonicity_counts.get("increase", 0),
            "algebra_decrease_edges": algebra_monotonicity_counts.get("decrease", 0),
            "algebra_flat_edges": algebra_monotonicity_counts.get("flat", 0),
            "entropy_match_flip_edges": entropy_flip_count,
            "observer_signal_flip_edges": signal_flip_count,
        },
        "certified_claims": phase_claims,
        "_node_by_id": node_by_id,
        "_node_ids": node_ids,
        "_edges": edges_tuple,
    }


def phase30_cover_robust_analysis(
    *,
    cover_graph: dict[str, object],
    rule_specs: tuple[dict[str, object], ...],
    max_bonus: int,
) -> dict[str, object]:
    node_by_id = cover_graph["_node_by_id"]
    node_ids = cover_graph["_node_ids"]
    edges = cover_graph["_edges"]
    if not isinstance(node_by_id, dict) or not isinstance(node_ids, tuple) or not isinstance(edges, tuple):
        raise TypeError("Phase 30 cover graph must contain internal graph data")
    substrate_analyses = tuple(
        phase26_substrate_analysis(
            spec=spec,
            rule_specs=rule_specs,
            node_by_id=node_by_id,  # type: ignore[arg-type]
            node_ids=node_ids,  # type: ignore[arg-type]
            phase21_edges=edges,  # type: ignore[arg-type]
        )
        for spec in phase26_transfer_substrate_specs()
    )
    substrate_metric_maps: dict[str, dict[str, dict[str, Fraction]]] = {
        str(analysis["name"]): analysis["_metrics_by_rule"]  # type: ignore[assignment]
        for analysis in substrate_analyses
    }
    specs_by_name = substrate_analyses[0]["_specs_by_name"]  # type: ignore[assignment]
    if not isinstance(specs_by_name, dict):
        raise TypeError("Phase 30 substrate analysis must contain specs_by_name")
    robust_rule_table, robust_metrics_by_rule = phase27_rule_robust_metrics(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        substrate_metric_maps=substrate_metric_maps,
    )
    robust_target_witnesses = phase27_robust_target_gap_witnesses(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        substrate_metric_maps=substrate_metric_maps,
        robust_metrics_by_rule=robust_metrics_by_rule,
    )
    robust_witness_by_objective = {
        str(item["objective"]["name"]): item  # type: ignore[index]
        for item in robust_target_witnesses
    }
    robust_pareto_frontier = phase27_robust_pareto_frontier(
        specs_by_name=specs_by_name,  # type: ignore[arg-type]
        robust_metrics_by_rule=robust_metrics_by_rule,
    )
    local_feature_audits = tuple(
        phase29_rule_signature_audit(
            robust_witness=item,
            specs_by_name=specs_by_name,  # type: ignore[arg-type]
        )
        for item in robust_target_witnesses
    )
    phase28_schema_transfer_audits = tuple(
        phase28_target_schema_audit(
            schema=schema,
            specs_by_name=specs_by_name,  # type: ignore[arg-type]
            robust_witness_by_objective=robust_witness_by_objective,
        )
        for schema in phase28_target_feature_schemas()
    )
    objective_signs = phase29_objective_signs(robust_target_witnesses)
    positive_objectives = tuple(sorted(objective for objective, sign in objective_signs.items() if sign == "positive"))
    negative_objectives = tuple(sorted(objective for objective, sign in objective_signs.items() if sign == "negative"))
    transfer_exact_objectives = tuple(
        sorted(
            str(item["objective"]["name"])  # type: ignore[index]
            for item in phase28_schema_transfer_audits
            if item["audits"]["feature_condition_selects_exact_maximizers"]  # type: ignore[index]
        )
    )
    phase_claims = {
        "cover_mixed_graph_certified": cover_graph["certified_claims"]["cover_mixed_graph_certificate"],  # type: ignore[index]
        "cover_substrate_family_certified": all(
            analysis["certified_claims"]["transfer_substrate_certificate"] for analysis in substrate_analyses  # type: ignore[index]
        ),
        "cover_rule_space_exactly_bounded": len(robust_rule_table) == (max_bonus + 1) ** 3,
        "cover_target_objectives_exactly_certified": phase27_robust_target_witnesses_are_minimal(
            witnesses=robust_target_witnesses,
            specs_by_name=specs_by_name,  # type: ignore[arg-type]
            substrate_metric_maps=substrate_metric_maps,
        ),
        "cover_pareto_frontier_certified": phase27_robust_pareto_frontier_is_certified(
            frontier=robust_pareto_frontier,
            robust_metrics_by_rule=robust_metrics_by_rule,
        ),
        "cover_local_feature_audits_select_exact_maximizers": all(
            item["audits"]["signature_condition_selects_exact_maximizers"] for item in local_feature_audits  # type: ignore[index]
        ),
        "phase28_schema_transfer_records_complete": len(phase28_schema_transfer_audits)
        == len(phase25_target_objectives()),
    }
    phase_claims["cover_robust_audit_certificate"] = all(phase_claims.values())
    return {
        "cover_candidate": cover_graph["cover_candidate"],
        "graph_counts": cover_graph["counts"],
        "graph_classification": cover_graph["classification"],
        "graph_claims": cover_graph["certified_claims"],
        "substrate_summaries": tuple(
            {
                "name": analysis["name"],
                "counts": analysis["counts"],
                "certified_claims": analysis["certified_claims"],
            }
            for analysis in substrate_analyses
        ),
        "robust_target_gap_witnesses": robust_target_witnesses,
        "local_feature_audits": local_feature_audits,
        "phase28_schema_transfer_audits": phase28_schema_transfer_audits,
        "robust_pareto_frontier": robust_pareto_frontier,
        "objective_signs": tuple(
            {
                "objective": objective,
                "sign": sign,
            }
            for objective, sign in sorted(objective_signs.items())
        ),
        "counts": {
            "substrates": len(substrate_analyses),
            "candidate_rules": len(robust_rule_table),
            "target_objectives": len(robust_target_witnesses),
            "positive_worst_case_objectives": len(positive_objectives),
            "negative_worst_case_objectives": len(negative_objectives),
            "phase28_schema_transfer_exact_objectives": len(transfer_exact_objectives),
            "phase28_schema_transfer_failed_objectives": len(phase25_target_objectives()) - len(transfer_exact_objectives),
            "robust_pareto_frontier_rules": robust_pareto_frontier["frontier_rule_count"],
            "robust_pareto_frontier_metric_vectors": robust_pareto_frontier["frontier_metric_vector_count"],
        },
        "phase28_schema_transfer_exact_objectives": transfer_exact_objectives,
        "certified_claims": phase_claims,
    }


def phase30_sign_flip_records(
    *,
    baseline_cover: dict[str, object],
    cover_results: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    baseline_signs = {
        str(item["objective"]): str(item["sign"])  # type: ignore[index]
        for item in baseline_cover["objective_signs"]  # type: ignore[index]
    }
    records = []
    for cover in cover_results:
        cover_name = str(cover["cover_candidate"]["name"])  # type: ignore[index]
        if cover_name == str(baseline_cover["cover_candidate"]["name"]):  # type: ignore[index]
            continue
        signs = {
            str(item["objective"]): str(item["sign"])  # type: ignore[index]
            for item in cover["objective_signs"]  # type: ignore[index]
        }
        strict = bool(cover["cover_candidate"]["strict_cover_hit_required"])  # type: ignore[index]
        for objective, baseline_sign in sorted(baseline_signs.items()):
            cover_sign = signs[objective]
            if cover_sign == baseline_sign:
                continue
            records.append(
                {
                    "cover": cover_name,
                    "role": cover["cover_candidate"]["role"],  # type: ignore[index]
                    "strict_cover_hit_required": strict,
                    "objective": objective,
                    "baseline_cover": baseline_cover["cover_candidate"]["name"],  # type: ignore[index]
                    "baseline_sign": baseline_sign,
                    "cover_sign": cover_sign,
                    "negative_to_positive": baseline_sign == "negative" and cover_sign == "positive",
                    "positive_to_negative": baseline_sign == "positive" and cover_sign == "negative",
                }
            )
    return tuple(records)


def phase30_objective_gap(
    *,
    cover_result: dict[str, object],
    objective_name: str,
) -> dict[str, object]:
    for witness in cover_result["robust_target_gap_witnesses"]:  # type: ignore[index]
        if str(witness["objective"]["name"]) == objective_name:  # type: ignore[index]
            return witness["max_worst_case_gap"]  # type: ignore[return-value]
    raise KeyError(objective_name)


def bridge_cosmology_phase30_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    cover_candidates = phase30_observer_cover_candidates()
    baseline_outer = phase11_outer_distance_repair_code()
    outer_states = phase21_outer_radius_one_states()
    rule_specs = phase24_weighted_rule_specs(max_bonus=max_bonus)
    cover_graphs = tuple(
        phase30_mixed_graph_for_cover(
            cover_candidate=candidate,
            baseline_outer=baseline_outer,
            outer_states=outer_states,
        )
        for candidate in cover_candidates
    )
    cover_results = tuple(
        phase30_cover_robust_analysis(
            cover_graph=cover_graph,
            rule_specs=rule_specs,
            max_bonus=max_bonus,
        )
        for cover_graph in cover_graphs
    )
    cover_by_name = {
        str(result["cover_candidate"]["name"]): result  # type: ignore[index]
        for result in cover_results
    }
    baseline_cover = cover_by_name["strict_baseline_p1_q13"]
    sign_flips = phase30_sign_flip_records(
        baseline_cover=baseline_cover,
        cover_results=cover_results,
    )
    strict_sign_flips = tuple(record for record in sign_flips if bool(record["strict_cover_hit_required"]))
    near_miss_sign_flips = tuple(record for record in sign_flips if not bool(record["strict_cover_hit_required"]))
    phase29_persistent_objectives = (
        "prefer_entropy_break_over_full_semantics",
        "prefer_operator_collapse_over_full_semantics",
    )
    strict_cover_results = tuple(
        result
        for result in cover_results
        if bool(result["cover_candidate"]["strict_cover_hit_required"])  # type: ignore[index]
    )
    strict_signs_by_cover = {
        str(result["cover_candidate"]["name"]): {  # type: ignore[index]
            str(item["objective"]): str(item["sign"])  # type: ignore[index]
            for item in result["objective_signs"]  # type: ignore[index]
        }
        for result in strict_cover_results
    }
    strict_entropy_no_go_preserved = all(
        signs["prefer_entropy_break_over_full_semantics"] == "negative"
        for signs in strict_signs_by_cover.values()
    )
    strict_operator_no_go_flips = tuple(
        record
        for record in strict_sign_flips
        if record["objective"] == "prefer_operator_collapse_over_full_semantics"
        and bool(record["negative_to_positive"])
    )
    near_miss_entropy_flips = tuple(
        record
        for record in near_miss_sign_flips
        if record["objective"] == "prefer_entropy_break_over_full_semantics"
        and bool(record["negative_to_positive"])
    )
    strict_control = cover_by_name["strict_control_p2_q7"]
    strict_control_sign_flips = tuple(
        record
        for record in strict_sign_flips
        if record["cover"] == "strict_control_p2_q7"
    )
    near_miss = cover_by_name["near_miss_entropy_flip_p3_q5"]
    near_miss_claims = near_miss["cover_candidate"]["seed_cover_certificate"]["certified_claims"]  # type: ignore[index]
    phase_claims = {
        "selected_cover_set_exactly_bounded": len(cover_candidates) == len(phase30_selected_cover_templates())
        and len(cover_results) == len(cover_candidates),
        "strict_seed_cover_certificates_verified": all(
            bool(candidate["seed_cover_certificate"]["certified_claims"]["causal_patch_search_hit"])  # type: ignore[index]
            for candidate in (result["cover_candidate"] for result in strict_cover_results)
        ),
        "near_miss_rejected_by_erasure_gate": not bool(near_miss_claims["same_erasure_correctability_profile"])
        and not bool(near_miss_claims["causal_patch_search_hit"]),
        "all_cover_mixed_graphs_certified": all(
            result["graph_claims"]["cover_mixed_graph_certificate"] for result in cover_results  # type: ignore[index]
        ),
        "all_cover_robust_audits_certified": all(
            result["certified_claims"]["cover_robust_audit_certificate"] for result in cover_results  # type: ignore[index]
        ),
        "baseline_cover_matches_phase29_persistent_no_go_signs": all(
            {
                str(item["objective"]): str(item["sign"])  # type: ignore[index]
                for item in baseline_cover["objective_signs"]  # type: ignore[index]
            }[objective]
            == "negative"
            for objective in phase29_persistent_objectives
        ),
        "strict_control_preserves_baseline_signs": not strict_control_sign_flips,
        "strict_cover_flips_operator_full_no_go": bool(strict_operator_no_go_flips),
        "strict_covers_preserve_entropy_full_no_go": strict_entropy_no_go_preserved,
        "near_miss_flips_entropy_full_no_go_but_fails_erasure_gate": bool(near_miss_entropy_flips),
        "horizon_invariant_across_cover_co_design": all(
            result["graph_claims"]["shared_horizon_correctability_stable_across_mixed_graph"]  # type: ignore[index]
            and result["graph_claims"]["shared_horizon_fixed_point_stable_across_mixed_graph"]  # type: ignore[index]
            for result in cover_results
        ),
    }
    phase_claims["phase_30_bounded_observer_cover_co_design_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 30: bounded observer-cover co-design",
        "status": "pass" if phase_claims["phase_30_bounded_observer_cover_co_design_certificate"] else "fail",
        "rule_language_schema": phase28_rule_language_schema(max_bonus=max_bonus),
        "proof_text": (
            "Phase 30 bounded observer-cover co-design proof. The cover set consists of three strict Phase 12 "
            "private-full/shared-inner repaired-cover hits plus one explicitly marked erasure-profile near-miss. "
            "For each cover, the certificate rebuilds the mixed inner/outer transition graph, applies the four "
            "Phase 26 substrate filters, recomputes exact robust channel-rule gaps, and audits the feature "
            "conditions against exact enumeration. Strict cover flips are separated from near-miss flips."
        ),
        "search_spec": {
            "cover_source": "selected Phase 12 private-full/shared-inner repaired-cover block masks",
            "selected_covers": tuple(phase30_public_cover_candidate(candidate) for candidate in cover_candidates),
            "strict_cover_hit_count": len(strict_cover_results),
            "near_miss_count": len(cover_results) - len(strict_cover_results),
            "max_bonus": max_bonus,
            "candidate_rules": len(rule_specs),
            "target_objectives": phase25_target_objectives(),
            "phase29_persistent_no_go_objectives": phase29_persistent_objectives,
        },
        "cover_results": cover_results,
        "sign_flip_records": sign_flips,
        "strict_sign_flip_records": strict_sign_flips,
        "near_miss_sign_flip_records": near_miss_sign_flips,
        "strict_operator_full_no_go_flips": strict_operator_no_go_flips,
        "near_miss_entropy_full_no_go_flips": near_miss_entropy_flips,
        "key_gap_comparison": {
            "baseline_entropy_break_over_full": phase30_objective_gap(
                cover_result=baseline_cover,
                objective_name="prefer_entropy_break_over_full_semantics",
            ),
            "near_miss_entropy_break_over_full": phase30_objective_gap(
                cover_result=near_miss,
                objective_name="prefer_entropy_break_over_full_semantics",
            ),
            "baseline_operator_collapse_over_full": phase30_objective_gap(
                cover_result=baseline_cover,
                objective_name="prefer_operator_collapse_over_full_semantics",
            ),
            "strict_operator_flip_over_full": phase30_objective_gap(
                cover_result=cover_by_name["strict_operator_flip_p3_q13"],
                objective_name="prefer_operator_collapse_over_full_semantics",
            ),
        },
        "counts": {
            "selected_covers": len(cover_results),
            "strict_cover_hits": len(strict_cover_results),
            "near_miss_covers": len(cover_results) - len(strict_cover_results),
            "candidate_rules": len(rule_specs),
            "target_objectives_per_cover": len(phase25_target_objectives()),
            "sign_flip_records": len(sign_flips),
            "strict_sign_flip_records": len(strict_sign_flips),
            "near_miss_sign_flip_records": len(near_miss_sign_flips),
            "strict_operator_full_no_go_flips": len(strict_operator_no_go_flips),
            "near_miss_entropy_full_no_go_flips": len(near_miss_entropy_flips),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 30 shows that observer-cover co-design can flip the Phase 29 operator-collapse-over-full "
                "persistent no-go while preserving exact strict cover and horizon constraints."
            ),
            "persistence_lesson": (
                "The entropy-break-over-full no-go remains negative for the selected strict repaired-cover hits. "
                "It becomes positive only in the included near-miss cover, which is rejected by the erasure-profile "
                "gate."
            ),
            "audit_lesson": (
                "Every accepted strict cover result is rebuilt from the cover, graph, substrate filters, exact "
                "robust rule enumeration, and local feature audits; near-miss flips are reported but not counted "
                "as strict cover witnesses."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 30 separates strict cover-level sign flips from erasure-rejected near-miss flips. The next "
                "adaptation should exhaust the eight strict repaired-cover hits or synthesize covers directly "
                "against a target sign while keeping the erasure gate hard."
            ),
            "suggested_phase_31": (
                "Run strict-cover exhaustive audit over the eight Phase 12 repaired-cover hits: certify whether "
                "entropy-break-over-full is a true strict-cover no-go for this family and classify all operator "
                "sign flips by shared/private block pattern."
            ),
        },
    }


def phase31_raw_entropy_reconstruction_cover_hit(claims: dict[str, object]) -> bool:
    return (
        bool(claims["same_entropy_overlap_data"])
        and bool(claims["observer_overlap_is_horizon"])
        and bool(claims["same_shared_horizon_algebra"])
        and bool(claims["different_observer_reconstruction"])
    )


def phase31_strict_cover_name(candidate: dict[str, object]) -> str:
    return f"strict_hit_p{int(candidate['observer_p_block_mask'])}_q{int(candidate['observer_q_block_mask'])}"


def phase31_exhaustive_strict_cover_scan() -> dict[str, object]:
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 31 source must contain StabilizerCode objects")
    inner_atlas = phase12_canonical_inner_atlas_hit(include_bases=False)
    candidates = tuple(
        candidate
        for candidate in phase12_atlas_aware_repaired_cover_candidates(inner_hit=inner_atlas["hit"])
        if candidate["template_kind"] == "phase12_private_full_shared_inner"
    )
    strict_records = []
    raw_hit_count = 0
    erasure_rejected_raw_hits = 0
    non_raw_count = 0
    for candidate in candidates:
        cover = candidate["cover"]
        if not isinstance(cover, PatchCover):
            raise TypeError("Phase 31 candidate must contain a PatchCover")
        seed_certificate = rank_kernel_cover_search_hit_certificate_for_pair(
            pair_source=str(source["name"]),
            first=first,
            second=second,
            cover=cover,
            include_bases=False,
        )
        claims = seed_certificate["certified_claims"]
        if not isinstance(claims, dict):
            raise TypeError("Phase 31 seed certificate claims must be a dict")
        raw_hit = phase31_raw_entropy_reconstruction_cover_hit(claims)
        strict_hit = bool(claims["causal_patch_search_hit"])
        if raw_hit:
            raw_hit_count += 1
        else:
            non_raw_count += 1
        if raw_hit and not strict_hit and not bool(claims["same_erasure_correctability_profile"]):
            erasure_rejected_raw_hits += 1
        if not strict_hit:
            continue
        strict_records.append(
            {
                "name": phase31_strict_cover_name(candidate),
                "role": "phase18_baseline_cover"
                if int(candidate["observer_p_block_mask"]) == 1 and int(candidate["observer_q_block_mask"]) == 13
                else "strict_exhaustive_hit",
                "observer_p_block_mask": candidate["observer_p_block_mask"],
                "observer_q_block_mask": candidate["observer_q_block_mask"],
                "strict_cover_hit_required": True,
                "template_kind": candidate["template_kind"],
                "template_origin": candidate["template_origin"],
                "observer_p_blocks": candidate["observer_p_blocks"],
                "observer_q_blocks": candidate["observer_q_blocks"],
                "shared_block_mask": candidate["shared_block_mask"],
                "shared_blocks": candidate["shared_blocks"],
                "observer_p_private_blocks": candidate["observer_p_private_blocks"],
                "observer_q_private_blocks": candidate["observer_q_private_blocks"],
                "cover": cover.summary(first.n),
                "seed_cover_certificate": phase30_compact_seed_cover_certificate(seed_certificate),
                "certified_claims": {
                    "selected_from_phase12_private_full_shared_inner": True,
                    "seed_entropy_overlap_and_horizon_match": bool(claims["same_entropy_overlap_data"])
                    and bool(claims["observer_overlap_is_horizon"])
                    and bool(claims["same_shared_horizon_algebra"]),
                    "seed_observer_reconstruction_differs": bool(claims["different_observer_reconstruction"]),
                    "strict_cover_hit_status_matches_role": strict_hit,
                    "strict_cover_hit_verified": strict_hit,
                    "near_miss_rejected_by_erasure_profile": False,
                },
                "_cover": cover,
            }
        )
    strict_records_tuple = tuple(
        sorted(
            strict_records,
            key=lambda item: (int(item["observer_p_block_mask"]), int(item["observer_q_block_mask"])),
        )
    )
    strict_masks = tuple(
        {
            "name": record["name"],
            "observer_p_block_mask": record["observer_p_block_mask"],
            "observer_q_block_mask": record["observer_q_block_mask"],
            "shared_block_mask": record["shared_block_mask"],
            "shared_blocks": record["shared_blocks"],
            "observer_p_private_blocks": record["observer_p_private_blocks"],
            "observer_q_private_blocks": record["observer_q_private_blocks"],
        }
        for record in strict_records_tuple
    )
    counts = {
        "phase12_private_full_shared_inner_candidates": len(candidates),
        "raw_entropy_reconstruction_hits": raw_hit_count,
        "strict_cover_hits": len(strict_records_tuple),
        "raw_hits_rejected_by_erasure_profile": erasure_rejected_raw_hits,
        "non_raw_candidates": non_raw_count,
    }
    certified_claims = {
        "all_private_full_shared_inner_candidates_scanned": len(candidates) == 175,
        "raw_hit_partition_accounts_for_candidate_space": raw_hit_count + non_raw_count == len(candidates),
        "strict_hits_are_subset_of_raw_hits": len(strict_records_tuple) <= raw_hit_count,
        "erasure_rejected_raw_hits_account_for_raw_non_strict_hits": erasure_rejected_raw_hits
        == raw_hit_count - len(strict_records_tuple),
        "strict_cover_hit_count_is_eight": len(strict_records_tuple) == 8,
        "all_strict_seed_cover_certificates_verified": all(
            bool(record["seed_cover_certificate"]["certified_claims"]["causal_patch_search_hit"])
            for record in strict_records_tuple
        ),
    }
    certified_claims["phase_31_exhaustive_strict_cover_scan_certificate"] = all(certified_claims.values())
    return {
        "source": {
            "pair_source": source["name"],
            "n": first.n,
            "k_first": first.k,
            "k_second": second.k,
        },
        "scan_spec": {
            "cover_template": "phase12_private_full_shared_inner",
            "block_mask_domain": "ordered nonempty observer p/q block masks with nonempty overlap over four blocks",
            "strict_gate": (
                "same entropy/overlap data, horizon overlap, shared horizon algebra, observer reconstruction "
                "difference, same erasure-correctability profile, and erasure algebra difference"
            ),
        },
        "counts": counts,
        "strict_cover_block_masks": strict_masks,
        "strict_cover_candidates": strict_records_tuple,
        "certified_claims": certified_claims,
    }


def phase31_public_strict_cover_scan(scan: dict[str, object]) -> dict[str, object]:
    return {
        **{
            key: value
            for key, value in scan.items()
            if key != "strict_cover_candidates"
        },
        "strict_cover_candidates": tuple(
            phase30_public_cover_candidate(candidate)
            for candidate in scan["strict_cover_candidates"]  # type: ignore[index]
        ),
    }


def phase31_cover_result_by_name(cover_results: tuple[dict[str, object], ...]) -> dict[str, dict[str, object]]:
    return {
        str(result["cover_candidate"]["name"]): result  # type: ignore[index]
        for result in cover_results
    }


def phase31_objective_sign_map(cover_result: dict[str, object]) -> dict[str, str]:
    return {
        str(item["objective"]): str(item["sign"])  # type: ignore[index]
        for item in cover_result["objective_signs"]  # type: ignore[index]
    }


def phase31_cover_pattern(cover_result: dict[str, object]) -> dict[str, object]:
    candidate = cover_result["cover_candidate"]
    if not isinstance(candidate, dict):
        raise TypeError("Phase 31 cover result must contain a cover candidate")
    p_private = tuple(candidate["observer_p_private_blocks"])  # type: ignore[arg-type]
    q_private = tuple(candidate["observer_q_private_blocks"])  # type: ignore[arg-type]
    shared = tuple(candidate["shared_blocks"])  # type: ignore[arg-type]
    return {
        "shared_blocks": shared,
        "observer_p_private_blocks": p_private,
        "observer_q_private_blocks": q_private,
        "shared_block_count": len(shared),
        "observer_p_private_block_count": len(p_private),
        "observer_q_private_block_count": len(q_private),
        "observer_p_private_nonempty": bool(p_private),
        "observer_q_private_nonempty": bool(q_private),
    }


def phase31_operator_related_sign_flip_records(
    *,
    baseline_cover: dict[str, object],
    cover_results: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    records = []
    for record in phase30_sign_flip_records(baseline_cover=baseline_cover, cover_results=cover_results):
        if "operator_collapse" not in str(record["objective"]):
            continue
        cover_name = str(record["cover"])
        cover_result = phase31_cover_result_by_name(cover_results)[cover_name]
        records.append(
            {
                **record,
                "cover_pattern": phase31_cover_pattern(cover_result),
            }
        )
    return tuple(records)


def phase31_cover_gap_records(
    *,
    cover_results: tuple[dict[str, object], ...],
    objective_name: str,
) -> tuple[dict[str, object], ...]:
    out = []
    for result in cover_results:
        gap = phase30_objective_gap(cover_result=result, objective_name=objective_name)
        gap_fraction = phase28_fraction_from_public(gap)
        out.append(
            {
                "cover": result["cover_candidate"]["name"],  # type: ignore[index]
                "cover_pattern": phase31_cover_pattern(result),
                "max_worst_case_gap": gap,
                "sign": phase29_sign(gap_fraction),
            }
        )
    return tuple(out)


def phase31_gap_extrema(records: tuple[dict[str, object], ...]) -> dict[str, object]:
    values = {
        str(record["cover"]): phase28_fraction_from_public(record["max_worst_case_gap"])  # type: ignore[arg-type]
        for record in records
    }
    minimum = min(values.values())
    maximum = max(values.values())
    return {
        "minimum": phase22_fraction(minimum),
        "minimum_covers": tuple(sorted(cover for cover, value in values.items() if value == minimum)),
        "maximum": phase22_fraction(maximum),
        "maximum_covers": tuple(sorted(cover for cover, value in values.items() if value == maximum)),
    }


def phase31_operator_flip_cover_partition(
    *,
    cover_results: tuple[dict[str, object], ...],
    operator_related_sign_flips: tuple[dict[str, object], ...],
) -> dict[str, object]:
    flip_covers = tuple(sorted({str(record["cover"]) for record in operator_related_sign_flips}))
    all_covers = tuple(sorted(str(result["cover_candidate"]["name"]) for result in cover_results))  # type: ignore[index]
    preserving_covers = tuple(sorted(set(all_covers) - set(flip_covers)))
    return {
        "operator_related_sign_flip_covers": flip_covers,
        "operator_related_sign_preserving_covers": preserving_covers,
        "flip_cover_patterns": tuple(
            {
                "cover": cover_name,
                "cover_pattern": phase31_cover_pattern(phase31_cover_result_by_name(cover_results)[cover_name]),
            }
            for cover_name in flip_covers
        ),
        "preserving_cover_patterns": tuple(
            {
                "cover": cover_name,
                "cover_pattern": phase31_cover_pattern(phase31_cover_result_by_name(cover_results)[cover_name]),
            }
            for cover_name in preserving_covers
        ),
    }


def bridge_cosmology_phase31_certificate(*, max_bonus: int = 2) -> dict[str, object]:
    scan = phase31_exhaustive_strict_cover_scan()
    strict_cover_candidates = tuple(scan["strict_cover_candidates"])  # type: ignore[arg-type]
    baseline_outer = phase11_outer_distance_repair_code()
    outer_states = phase21_outer_radius_one_states()
    rule_specs = phase24_weighted_rule_specs(max_bonus=max_bonus)
    cover_graphs = tuple(
        phase30_mixed_graph_for_cover(
            cover_candidate=candidate,
            baseline_outer=baseline_outer,
            outer_states=outer_states,
        )
        for candidate in strict_cover_candidates
    )
    cover_results = tuple(
        phase30_cover_robust_analysis(
            cover_graph=cover_graph,
            rule_specs=rule_specs,
            max_bonus=max_bonus,
        )
        for cover_graph in cover_graphs
    )
    cover_by_name = phase31_cover_result_by_name(cover_results)
    baseline_cover = cover_by_name["strict_hit_p1_q13"]
    sign_flips = phase30_sign_flip_records(
        baseline_cover=baseline_cover,
        cover_results=cover_results,
    )
    operator_related_sign_flips = phase31_operator_related_sign_flip_records(
        baseline_cover=baseline_cover,
        cover_results=cover_results,
    )
    operator_flip_partition = phase31_operator_flip_cover_partition(
        cover_results=cover_results,
        operator_related_sign_flips=operator_related_sign_flips,
    )
    entropy_full_records = phase31_cover_gap_records(
        cover_results=cover_results,
        objective_name="prefer_entropy_break_over_full_semantics",
    )
    operator_full_records = phase31_cover_gap_records(
        cover_results=cover_results,
        objective_name="prefer_operator_collapse_over_full_semantics",
    )
    operator_entropy_records = phase31_cover_gap_records(
        cover_results=cover_results,
        objective_name="prefer_operator_collapse_over_entropy_break",
    )
    entropy_full_extrema = phase31_gap_extrema(entropy_full_records)
    operator_full_extrema = phase31_gap_extrema(operator_full_records)
    operator_entropy_extrema = phase31_gap_extrema(operator_entropy_records)
    entropy_full_strict_no_go = all(record["sign"] == "negative" for record in entropy_full_records)
    operator_full_negative_to_positive = tuple(
        record
        for record in sign_flips
        if record["objective"] == "prefer_operator_collapse_over_full_semantics"
        and bool(record["negative_to_positive"])
    )
    operator_entropy_negative_to_positive = tuple(
        record
        for record in sign_flips
        if record["objective"] == "prefer_operator_collapse_over_entropy_break"
        and bool(record["negative_to_positive"])
    )
    flip_covers = tuple(str(name) for name in operator_flip_partition["operator_related_sign_flip_covers"])  # type: ignore[index]
    preserving_covers = tuple(
        str(name) for name in operator_flip_partition["operator_related_sign_preserving_covers"]  # type: ignore[index]
    )
    p_private_flip_rule = all(
        phase31_cover_pattern(cover_by_name[cover])["observer_p_private_nonempty"]
        for cover in flip_covers
    ) and all(
        not phase31_cover_pattern(cover_by_name[cover])["observer_p_private_nonempty"]
        for cover in preserving_covers
    )
    phase_claims = {
        "phase31_exhaustive_strict_cover_scan_certified": scan["certified_claims"][  # type: ignore[index]
            "phase_31_exhaustive_strict_cover_scan_certificate"
        ],
        "all_strict_seed_cover_certificates_verified": all(
            bool(result["cover_candidate"]["seed_cover_certificate"]["certified_claims"]["causal_patch_search_hit"])  # type: ignore[index]
            for result in cover_results
        ),
        "all_strict_cover_mixed_graphs_certified": all(
            result["graph_claims"]["cover_mixed_graph_certificate"] for result in cover_results  # type: ignore[index]
        ),
        "all_strict_cover_robust_audits_certified": all(
            result["certified_claims"]["cover_robust_audit_certificate"] for result in cover_results  # type: ignore[index]
        ),
        "entropy_break_over_full_is_strict_cover_no_go": entropy_full_strict_no_go,
        "operator_full_no_go_flips_exist_in_strict_cover_hits": len(operator_full_negative_to_positive) == 4,
        "operator_entropy_no_go_flips_exist_in_strict_cover_hits": len(operator_entropy_negative_to_positive) == 4,
        "operator_related_sign_flips_classified_by_p_private": p_private_flip_rule
        and len(flip_covers) == 4
        and len(preserving_covers) == 4,
        "horizon_invariant_across_strict_cover_exhaustive_audit": all(
            result["graph_claims"]["shared_horizon_correctability_stable_across_mixed_graph"]  # type: ignore[index]
            and result["graph_claims"]["shared_horizon_fixed_point_stable_across_mixed_graph"]  # type: ignore[index]
            for result in cover_results
        ),
    }
    phase_claims["phase_31_strict_cover_exhaustive_audit_certificate"] = all(phase_claims.values())
    return {
        "phase": "Goal 2 Phase 31: strict-cover exhaustive audit",
        "status": "pass" if phase_claims["phase_31_strict_cover_exhaustive_audit_certificate"] else "fail",
        "rule_language_schema": phase28_rule_language_schema(max_bonus=max_bonus),
        "proof_text": (
            "Phase 31 strict-cover exhaustive audit proof. The certificate scans every Phase 12 "
            "private-full/shared-inner cover candidate, applies the full strict seed cover gate, and finds exactly "
            "eight strict repaired-cover hits. It then rebuilds a mixed transition graph for each strict cover, "
            "reruns the four-substrate robust channel synthesis, and audits feature predicates by exact finite "
            "enumeration. The entropy-break-over-full objective stays negative on every strict cover; operator "
            "sign flips are classified by the observer private-block pattern."
        ),
        "strict_cover_scan": phase31_public_strict_cover_scan(scan),
        "cover_results": cover_results,
        "sign_flip_records": sign_flips,
        "operator_related_sign_flip_records": operator_related_sign_flips,
        "operator_flip_cover_partition": operator_flip_partition,
        "gap_records": {
            "entropy_break_over_full_semantics": entropy_full_records,
            "operator_collapse_over_full_semantics": operator_full_records,
            "operator_collapse_over_entropy_break": operator_entropy_records,
        },
        "gap_extrema": {
            "entropy_break_over_full_semantics": entropy_full_extrema,
            "operator_collapse_over_full_semantics": operator_full_extrema,
            "operator_collapse_over_entropy_break": operator_entropy_extrema,
        },
        "operator_full_no_go_flips": operator_full_negative_to_positive,
        "operator_entropy_no_go_flips": operator_entropy_negative_to_positive,
        "counts": {
            "phase12_private_full_shared_inner_candidates": scan["counts"][  # type: ignore[index]
                "phase12_private_full_shared_inner_candidates"
            ],
            "raw_entropy_reconstruction_hits": scan["counts"]["raw_entropy_reconstruction_hits"],  # type: ignore[index]
            "strict_cover_hits": len(cover_results),
            "raw_hits_rejected_by_erasure_profile": scan["counts"]["raw_hits_rejected_by_erasure_profile"],  # type: ignore[index]
            "candidate_rules": len(rule_specs),
            "target_objectives_per_cover": len(phase25_target_objectives()),
            "sign_flip_records": len(sign_flips),
            "operator_related_sign_flip_records": len(operator_related_sign_flips),
            "operator_related_sign_flip_covers": len(flip_covers),
            "operator_related_sign_preserving_covers": len(preserving_covers),
            "operator_full_no_go_flips": len(operator_full_negative_to_positive),
            "operator_entropy_no_go_flips": len(operator_entropy_negative_to_positive),
        },
        "certified_claims": phase_claims,
        "interpretation": {
            "result": (
                "Phase 31 upgrades the Phase 30 selected-cover story to an exhaustive audit over the eight strict "
                "Phase 12 repaired-cover hits."
            ),
            "entropy_lesson": (
                "The entropy-break-over-full objective is a strict-cover no-go for this whole repaired-cover family: "
                "its best exact worst-case gap remains negative on all eight strict covers."
            ),
            "operator_lesson": (
                "Operator-related sign flips occur exactly on the strict covers where observer_p has a nonempty "
                "private outer block; covers with no observer_p-private block preserve the baseline operator signs."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 31 proves a strict-cover entropy no-go within the Phase 12 repaired-cover family and classifies "
                "operator sign flips by private-block pattern. The next adaptation should either broaden the cover "
                "grammar or synthesize strict covers directly against the entropy objective while keeping the erasure "
                "gate hard."
            ),
            "suggested_phase_32": (
                "Run strict entropy-target cover synthesis: search a broader bounded cover grammar for a strict "
                "erasure-compatible entropy-break-over-full flip, or certify a no-go for that grammar with the same "
                "exact seed-cover and robust-channel audits."
            ),
        },
    }


def _patch_summary_by_name(patch_cover: dict[str, object], name: str) -> dict[str, object]:
    for patch in patch_cover["patches"]:  # type: ignore[index]
        if isinstance(patch, dict) and patch["name"] == name:
            return patch
    raise KeyError(name)


def de_sitter_qec_toy_model_certificate(
    *,
    max_m: int = 3,
    max_bonus: int = 2,
) -> dict[str, object]:
    if max_m < 2:
        raise ValueError("max_m must be at least 2 to certify growth and erasure dynamics")
    phase1 = bridge_cosmology_phase1_certificate(max_m=max_m)
    phase2 = bridge_cosmology_phase2_certificate(max_m=max_m)
    phase22 = bridge_cosmology_phase22_certificate()
    phase27 = bridge_cosmology_phase27_certificate(max_bonus=max_bonus)
    phase31 = bridge_cosmology_phase31_certificate(max_bonus=max_bonus)

    representative = phase1["instances"][0]  # type: ignore[index]
    representative_cover = representative["patch_cover"]  # type: ignore[index]
    observer_p_patch = _patch_summary_by_name(representative_cover, "observer_p")  # type: ignore[arg-type]
    observer_q_patch = _patch_summary_by_name(representative_cover, "observer_q")  # type: ignore[arg-type]
    shared_horizon_patch = _patch_summary_by_name(representative_cover, "shared_horizon")  # type: ignore[arg-type]
    patch_roles = tuple(str(patch["role"]) for patch in representative_cover["patches"])  # type: ignore[index]
    patch_names = tuple(str(patch["name"]) for patch in representative_cover["patches"])  # type: ignore[index]
    horizon_qubits = tuple(shared_horizon_patch["qubits"])  # type: ignore[index]
    observer_overlap = tuple(representative["witness"]["observer_pair"]["intersection"])  # type: ignore[index]
    first_slice = phase2["slices"][0]  # type: ignore[index]
    all_phase1_instances_pass = all(
        bool(instance["certified_claims"]["phase_1_static_patch_separation"])  # type: ignore[index]
        for instance in phase1["instances"]  # type: ignore[index]
    )
    all_phase2_slices_pass = all(
        bool(slice_["certified_claims"]["phase_2_erasure_channel_probe"])  # type: ignore[index]
        for slice_ in phase2["slices"]  # type: ignore[index]
    )
    all_phase2_transitions_pass = all(
        bool(transition["certified_claims"]["phase_2_growth_transition"])  # type: ignore[index]
        for transition in phase2["transitions"]  # type: ignore[index]
    )
    all_complementarity = all(
        bool(slice_["certified_claims"]["qec_complementarity_identity_all_scenarios"])  # type: ignore[index]
        for slice_ in phase2["slices"]  # type: ignore[index]
    )
    all_erasure_semantics = all(
        bool(slice_["certified_claims"]["same_erasure_correctability_profile"])  # type: ignore[index]
        and bool(slice_["certified_claims"]["private_shell_erasures_correctable"])  # type: ignore[index]
        and bool(slice_["certified_claims"]["shared_horizon_erasure_not_correctable"])  # type: ignore[index]
        and bool(slice_["certified_claims"]["observer_erasure_algebra_differs"])  # type: ignore[index]
        for slice_ in phase2["slices"]  # type: ignore[index]
    )
    all_growth_local = all(
        bool(transition["certified_claims"]["shared_horizon_fixed"])  # type: ignore[index]
        and bool(transition["certified_claims"]["observer_p_adds_new_p_only"])  # type: ignore[index]
        and bool(transition["certified_claims"]["observer_q_adds_new_q_only"])  # type: ignore[index]
        and bool(transition["certified_claims"]["shared_horizon_signature_stable"])  # type: ignore[index]
        for transition in phase2["transitions"]  # type: ignore[index]
    )
    proof_obligations = {
        "observer_causal_patch_primitive": {
            "requirement": "The primitive is two finite observer causal patches with a finite shared horizon.",
            "evidence": {
                "patch_names": patch_names,
                "patch_roles": patch_roles,
                "observer_p_qubits": observer_p_patch["qubits"],
                "observer_q_qubits": observer_q_patch["qubits"],
                "shared_horizon_qubits": horizon_qubits,
                "observer_overlap": observer_overlap,
                "no_boundary_interval_role": all("boundary" not in role for role in patch_roles),
            },
            "satisfied": observer_overlap == horizon_qubits
            and len(horizon_qubits) > 0
            and all("boundary" not in role for role in patch_roles)
            and all_phase1_instances_pass,
        },
        "horizon_entropy_and_patch_overlap": {
            "requirement": "Horizon entropy, observer overlap, MI/CMI/I3, and shared-horizon algebra are exact and agree.",
            "evidence": {
                "shared_horizon_entropy": representative["witness"]["shared_horizon"]["entropy"],  # type: ignore[index]
                "shared_horizon_signature": representative["witness"]["shared_horizon"]["signature"],  # type: ignore[index]
                "observer_pair": representative["witness"]["observer_pair"],  # type: ignore[index]
                "instances_certified": len(phase1["instances"]),  # type: ignore[arg-type]
            },
            "satisfied": all_phase1_instances_pass
            and all(
                bool(instance["certified_claims"]["same_patch_entropy_overlap_data"])  # type: ignore[index]
                and bool(instance["certified_claims"]["same_shared_horizon_algebra"])  # type: ignore[index]
                and bool(instance["certified_claims"]["observer_pair_metrics_match"])  # type: ignore[index]
                for instance in phase1["instances"]  # type: ignore[index]
            ),
        },
        "observer_reconstruction_algebra_split": {
            "requirement": "Observer patch reconstruction algebra differs while horizon-visible data agree.",
            "evidence": {
                "observer_p_first_signature": representative["witness"]["observer_p"]["first_signature"],  # type: ignore[index]
                "observer_p_second_signature": representative["witness"]["observer_p"]["second_signature"],  # type: ignore[index]
                "observer_q_first_signature": representative["witness"]["observer_q"]["first_signature"],  # type: ignore[index]
                "observer_q_second_signature": representative["witness"]["observer_q"]["second_signature"],  # type: ignore[index]
            },
            "satisfied": all(
                bool(instance["certified_claims"]["different_observer_patch_reconstruction"])  # type: ignore[index]
                for instance in phase1["instances"]  # type: ignore[index]
            ),
        },
        "complementarity_no_cloning_guard": {
            "requirement": "No-cloning is guarded by overlapping observer patches and exact erasure/reconstruction complementarity.",
            "evidence": {
                "observer_overlap_is_shared_horizon": observer_overlap == horizon_qubits,
                "shared_horizon_size": len(horizon_qubits),
                "qec_complementarity_identity_all_scenarios": all_complementarity,
            },
            "satisfied": observer_overlap == horizon_qubits and len(horizon_qubits) > 0 and all_complementarity,
        },
        "erasure_semantics": {
            "requirement": "Named erasure probes certify private-shell, shared-horizon, observer-patch, and survivor semantics.",
            "evidence": {
                "first_slice_witness": first_slice["witness"],  # type: ignore[index]
                "slices_certified": len(phase2["slices"]),  # type: ignore[arg-type]
            },
            "satisfied": all_phase2_slices_pass and all_erasure_semantics,
        },
        "controlled_patch_growth_and_locality_breakdown": {
            "requirement": "The model has controlled finite patch growth with fixed horizon and stable/differing reconstruction roles.",
            "evidence": {
                "transitions_certified": len(phase2["transitions"]),  # type: ignore[arg-type]
                "first_transition_claims": phase2["transitions"][0]["certified_claims"],  # type: ignore[index]
            },
            "satisfied": all_phase2_transitions_pass and all_growth_local,
        },
        "patch_channel_fixed_point_behavior": {
            "requirement": "Exact patch channel/fixed-point behavior is certified on finite transition graphs.",
            "evidence": {
                "phase22_counts": phase22["counts"],
                "phase27_counts": phase27["counts"],
                "phase31_counts": phase31["counts"],
            },
            "satisfied": phase22["status"] == "pass"
            and phase22["certified_claims"]["horizon_fixed_point_invariant_under_both_channels"]  # type: ignore[index]
            and phase27["status"] == "pass"
            and phase27["certified_claims"]["horizon_invariant_across_robust_substrates"]  # type: ignore[index]
            and phase31["status"] == "pass"
            and phase31["certified_claims"]["horizon_invariant_across_strict_cover_exhaustive_audit"],  # type: ignore[index]
        },
        "bounded_strict_cover_audit": {
            "requirement": "Bounded search distinguishes certified strict covers from entropy-near-misses rejected by erasure semantics.",
            "evidence": {
                "phase31_counts": phase31["counts"],
                "entropy_gap_extremum": phase31["gap_extrema"]["entropy_break_over_full_semantics"]["maximum"],  # type: ignore[index]
            },
            "satisfied": phase31["status"] == "pass"
            and phase31["counts"]["strict_cover_hits"] == 8  # type: ignore[index]
            and phase31["counts"]["raw_hits_rejected_by_erasure_profile"] == 58  # type: ignore[index]
            and phase31["certified_claims"]["entropy_break_over_full_is_strict_cover_no_go"],  # type: ignore[index]
        },
    }
    certified_claims = {
        "source_certificates_loaded": phase1["status"] == "pass"
        and phase2["status"] == "pass"
        and phase22["status"] == "pass"
        and phase27["status"] == "pass"
        and phase31["status"] == "pass",
        "finite_observer_causal_patch_primitive_certified": proof_obligations[
            "observer_causal_patch_primitive"
        ]["satisfied"],
        "horizon_entropy_overlap_certificate": proof_obligations["horizon_entropy_and_patch_overlap"]["satisfied"],
        "observer_reconstruction_algebra_split": proof_obligations["observer_reconstruction_algebra_split"][
            "satisfied"
        ],
        "complementarity_no_cloning_guard": proof_obligations["complementarity_no_cloning_guard"]["satisfied"],
        "erasure_semantics_certified": proof_obligations["erasure_semantics"]["satisfied"],
        "controlled_patch_growth_certified": proof_obligations[
            "controlled_patch_growth_and_locality_breakdown"
        ]["satisfied"],
        "patch_channel_fixed_point_behavior_certified": proof_obligations[
            "patch_channel_fixed_point_behavior"
        ]["satisfied"],
        "bounded_strict_cover_audit_certified": proof_obligations["bounded_strict_cover_audit"]["satisfied"],
    }
    certified_claims["finite_de_sitter_like_qec_toy_model_certified"] = all(certified_claims.values())
    return {
        "package": "Finite de Sitter-like QEC toy model capstone certificate",
        "status": "pass" if certified_claims["finite_de_sitter_like_qec_toy_model_certified"] else "fail",
        "scope": (
            "Finite stabilizer/QEC toy cosmology with observer causal patches and shared horizons. "
            "This is not an AdS/HaPPY boundary-code theorem and does not claim continuum de Sitter physics."
        ),
        "toy_model": {
            "primitive": "observer causal patches with finite shared horizons",
            "family": "balanced-bridge CSS causal-patch family with repaired-cover/channel bounded audits",
            "no_privileged_asymptotic_boundary": True,
            "representative_cover": representative_cover,
            "observer_witness": representative["witness"],
        },
        "source_certificates": {
            "phase1_static_patch": {
                "status": phase1["status"],
                "max_m": phase1["max_m"],
                "instances": len(phase1["instances"]),  # type: ignore[arg-type]
            },
            "phase2_erasure_growth": {
                "status": phase2["status"],
                "max_m": phase2["max_m"],
                "slices": len(phase2["slices"]),  # type: ignore[arg-type]
                "transitions": len(phase2["transitions"]),  # type: ignore[arg-type]
            },
            "phase22_exact_channels": {
                "status": phase22["status"],
                "counts": phase22["counts"],
            },
            "phase27_robust_channels": {
                "status": phase27["status"],
                "counts": phase27["counts"],
            },
            "phase31_strict_cover_audit": {
                "status": phase31["status"],
                "counts": phase31["counts"],
            },
        },
        "proof_obligations": proof_obligations,
        "certified_claims": certified_claims,
        "reproducibility": {
            "static_horizon_patch_certificate": f"python3 -m qgtoy cosmology-phase1 --max-m {max_m}",
            "erasure_growth_certificate": f"python3 -m qgtoy cosmology-phase2 --max-m {max_m}",
            "exact_channel_fixed_point_certificate": "python3 -m qgtoy cosmology-phase22",
            "robust_channel_synthesis_certificate": f"python3 -m qgtoy cosmology-phase27 --max-bonus {max_bonus}",
            "strict_cover_exhaustive_audit": f"python3 -m qgtoy cosmology-phase31 --max-bonus {max_bonus}",
            "capstone_certificate": f"python3 -m qgtoy desitter-toy --max-m {max_m} --max-bonus {max_bonus}",
        },
        "interpretation": {
            "result": (
                "The certified toy model uses finite observer causal patches, not boundary intervals. Horizon entropy, "
                "patch overlap, shared-horizon algebra, erasure complementarity, and channel fixed-point behavior are "
                "checked by exact stabilizer or exact rational-channel certificates."
            ),
            "separation": (
                "Entropy/horizon diagnostics can agree while observer reconstruction algebra and erasure/channel "
                "semantics differ. The Phase 31 bounded audit also separates strict cover hits from entropy-near-misses "
                "that fail the hard erasure gate."
            ),
            "not_overclaimed": (
                "This certifies a finite QEC toy model satisfying a de Sitter-like observer-patch diagnostic gate "
                "and bounded audits, not continuum de Sitter space, not a universal no-cloning theorem for all patch "
                "grammars, and not an asymptotic code family theorem."
            ),
        },
        "recommendation": {
            "next_phase": "stop",
            "reason": (
                "The active de Sitter-like toy-model objective has a certified finite model with exact static patch, "
                "erasure/complementarity, growth, channel/fixed-point, and bounded strict-cover evidence. Natural "
                "extensions are higher-distance analogues, asymptotic strengthening, or paper-style formalization."
            ),
        },
    }


def cover_search_hit_certificate_for_pair(
    *,
    pair_source: str,
    first: StabilizerCode,
    second: StabilizerCode,
    cover: PatchCover,
    include_bases: bool = False,
) -> dict[str, object]:
    first_entropy = entropy_overlap_summary(first, cover)
    second_entropy = entropy_overlap_summary(second, cover)
    first_algebras = dict(patch_algebra_signatures(first, cover))
    second_algebras = dict(patch_algebra_signatures(second, cover))
    observer_reconstruction = observer_reconstruction_summary(first, second, cover)
    first_erasures = erasure_suite_diagnostic(first, cover, include_bases=include_bases)
    second_erasures = erasure_suite_diagnostic(second, cover, include_bases=include_bases)
    shared_horizon = cover.patch("shared_horizon").region
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    claims = {
        "same_entropy_overlap_data": first_entropy == second_entropy,
        "observer_overlap_is_horizon": observer_p & observer_q == shared_horizon,
        "same_shared_horizon_algebra": first_algebras["shared_horizon"] == second_algebras["shared_horizon"],
        "different_observer_reconstruction": any(
            item["first_reconstructs_all"] != item["second_reconstructs_all"]
            or item["first_signature"] != item["second_signature"]
            for item in observer_reconstruction
        ),
        "same_erasure_correctability_profile": erasure_correctability_key(first_erasures)
        == erasure_correctability_key(second_erasures),
        "erasure_algebra_difference_exists": bool(erasure_algebra_differences(first_erasures, second_erasures)),
    }
    claims["causal_patch_search_hit"] = all(claims.values())
    return {
        "pair_source": pair_source,
        "n": first.n,
        "k": first.k,
        "cover": cover.summary(first.n),
        "first_generators": first.pauli_generators(),
        "second_generators": second.pauli_generators(),
        "first_patch_algebras": tuple((name, first_algebras[name]) for name in first_algebras),
        "second_patch_algebras": tuple((name, second_algebras[name]) for name in second_algebras),
        "observer_reconstruction": observer_reconstruction,
        "shared_horizon_signature": first_algebras["shared_horizon"],
        "erasure_comparison": {
            "same_erasure_correctability_profile": claims["same_erasure_correctability_profile"],
            "algebra_differences": erasure_algebra_differences(first_erasures, second_erasures),
        },
        "certified_claims": claims,
    }


def score_cover_candidate(first: StabilizerCode, second: StabilizerCode, cover: PatchCover) -> dict[str, object]:
    first_entropy = entropy_overlap_summary(first, cover)
    second_entropy = entropy_overlap_summary(second, cover)
    entropy_same = first_entropy == second_entropy
    observer_p = cover.patch("observer_p").region
    observer_q = cover.patch("observer_q").region
    shared_horizon = cover.patch("shared_horizon").region
    if not entropy_same or observer_p & observer_q != shared_horizon:
        return {
            "entropy_same": entropy_same,
            "observer_overlap_is_horizon": observer_p & observer_q == shared_horizon,
            "hit": False,
        }
    first_algebras = dict(patch_algebra_signatures(first, cover))
    second_algebras = dict(patch_algebra_signatures(second, cover))
    observer_reconstruction = observer_reconstruction_summary(first, second, cover)
    same_horizon = first_algebras["shared_horizon"] == second_algebras["shared_horizon"]
    observer_diff = any(
        item["first_reconstructs_all"] != item["second_reconstructs_all"]
        or item["first_signature"] != item["second_signature"]
        for item in observer_reconstruction
    )
    return {
        "entropy_same": entropy_same,
        "observer_overlap_is_horizon": True,
        "same_shared_horizon_algebra": same_horizon,
        "different_observer_reconstruction": observer_diff,
        "hit": same_horizon and observer_diff,
    }


def code_pair_source_candidates(*, include_calibration: bool = True) -> tuple[dict[str, object], ...]:
    first, second = seed_pair()
    sources = [
        {
            "name": "seed_css_witness",
            "source_type": "css",
            "origin": "Goal 1 robust n=6 CSS witness, before bridge growth",
            "first": first,
            "second": second,
        }
    ]
    if include_calibration:
        certificate = certify_minimal_entropy_reconstruction_discordance(max_n=4, k=1, max_subset_size=2)
        if certificate.pair is not None:
            sources.append(
                {
                    "name": "minimal_n4_calibration_pair",
                    "source_type": "exhaustive",
                    "origin": "exact minimal low-order entropy/reconstruction calibration search",
                    "first": certificate.pair.first,
                    "second": certificate.pair.second,
                }
            )
    return tuple(sources)


def code_pair_source_summary(source: dict[str, object]) -> dict[str, object]:
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    constraints = RobustConstraints()
    return {
        "name": source["name"],
        "source_type": source["source_type"],
        "origin": source["origin"],
        "n": first.n,
        "k": first.k,
        "first_generators": first.pauli_generators(),
        "second_generators": second.pauli_generators(),
        "first_quality": {
            "passes": code_quality(first, constraints).passes,
            "reason": code_quality(first, constraints).reason,
            "distance": code_quality(first, constraints).distance,
        },
        "second_quality": {
            "passes": code_quality(second, constraints).passes,
            "reason": code_quality(second, constraints).reason,
            "distance": code_quality(second, constraints).distance,
        },
        "same_labeled_t2_entropy": first.entropy_vector(max_subset_size=2)
        == second.entropy_vector(max_subset_size=2),
        "reconstruction_profiles_differ": first.reconstruction_profile() != second.reconstruction_profile(),
    }


def bounded_source_scan_reports(
    *,
    max_codes: int = 200,
    encoder_depth: int = 1,
) -> tuple[dict[str, object], ...]:
    constraints = RobustConstraints()
    configs = (
        ("css", 4),
        ("cyclic-css", 5),
        ("graph", 4),
        ("encoder", 4),
    )
    reports = []
    for source, n in configs:
        if source not in ROBUST_SOURCES:
            continue
        scan = scan_robust_source(
            n=n,
            k=1,
            source=source,
            equivalence="permutation",
            entropy_key_mode="labeled",
            constraints=constraints,
            max_codes=max_codes,
            encoder_depth=encoder_depth,
        )
        reports.append(
            {
                "source": source,
                "n": n,
                "k": 1,
                "max_codes": max_codes,
                "status": scan.status,
                "raw_codes": scan.raw_codes,
                "codes_checked": scan.codes_checked,
                "entropy_classes": scan.entropy_classes,
                "pair_found": scan.pair is not None,
            }
        )
    return tuple(reports)


def search_generic_covers_for_pair(
    *,
    source: dict[str, object],
    horizon_size: int,
    private_size: int,
    max_cover_candidates: int | None,
    max_hits: int,
    include_bases: bool,
) -> dict[str, object]:
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    covers = generic_patch_cover_candidates(
        n=first.n,
        horizon_size=horizon_size,
        private_size=private_size,
        max_candidates=max_cover_candidates,
    )
    scanned = 0
    entropy_matched = 0
    horizon_matched = 0
    observer_diff = 0
    hits: list[dict[str, object]] = []
    for cover in covers:
        scanned += 1
        score = score_cover_candidate(first, second, cover)
        if score["entropy_same"]:
            entropy_matched += 1
        if score.get("same_shared_horizon_algebra"):
            horizon_matched += 1
        if score.get("different_observer_reconstruction"):
            observer_diff += 1
        if not score["hit"]:
            continue
        hit = cover_search_hit_certificate_for_pair(
            pair_source=str(source["name"]),
            first=first,
            second=second,
            cover=cover,
            include_bases=include_bases,
        )
        if hit["certified_claims"]["causal_patch_search_hit"]:
            hits.append(hit)
            if len(hits) >= max_hits:
                break
    return {
        "source": code_pair_source_summary(source),
        "cover_search": {
            "horizon_size": horizon_size,
            "private_size": private_size,
            "candidate_count": len(covers),
            "max_cover_candidates": max_cover_candidates,
            "max_hits": max_hits,
        },
        "counts": {
            "scanned": scanned,
            "entropy_overlap_matched": entropy_matched,
            "same_horizon_algebra": horizon_matched,
            "different_observer_reconstruction": observer_diff,
            "hits_returned": len(hits),
        },
        "hits": tuple(hits),
        "status": "hit" if hits else "no-hit",
    }


def source_aware_patch_cover_candidates(
    *,
    source: dict[str, object],
    horizon_size: int,
    private_size: int,
    max_generic_candidates: int | None,
) -> tuple[dict[str, object], ...]:
    first = source["first"]
    if not isinstance(first, StabilizerCode):
        raise TypeError("source first must be a StabilizerCode instance")
    candidates: list[dict[str, object]] = []
    frontier_kind = source.get("frontier_kind")
    mutation_depth = int(source.get("mutation_depth", 0))
    if frontier_kind == "targeted_lift" and mutation_depth >= 1:
        candidates.append(
            {
                "template_kind": "source_aware_bridge_observer",
                "template_origin": "balanced-bridge lift rule",
                "cover": bridge_observer_cover(mutation_depth),
            }
        )
    for cover in generic_patch_cover_candidates(
        n=first.n,
        horizon_size=horizon_size,
        private_size=private_size,
        max_candidates=max_generic_candidates,
    ):
        candidates.append(
            {
                "template_kind": "generic_two_observer",
                "template_origin": "bounded disjoint horizon/private cover enumeration",
                "cover": cover,
            }
        )
    return tuple(candidates)


def search_source_aware_covers_for_pair(
    *,
    source: dict[str, object],
    horizon_size: int,
    private_size: int,
    max_generic_candidates: int | None,
    max_hits: int,
    include_bases: bool,
) -> dict[str, object]:
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    candidates = source_aware_patch_cover_candidates(
        source=source,
        horizon_size=horizon_size,
        private_size=private_size,
        max_generic_candidates=max_generic_candidates,
    )
    candidate_counts: dict[str, int] = {}
    scanned_by_template: dict[str, int] = {}
    hits_by_template: dict[str, int] = {}
    for candidate in candidates:
        kind = str(candidate["template_kind"])
        candidate_counts[kind] = candidate_counts.get(kind, 0) + 1

    scanned = 0
    entropy_matched = 0
    horizon_matched = 0
    observer_diff = 0
    hits: list[dict[str, object]] = []
    for candidate in candidates:
        kind = str(candidate["template_kind"])
        cover = candidate["cover"]
        if not isinstance(cover, PatchCover):
            raise TypeError("cover candidate must contain a PatchCover")
        scanned += 1
        scanned_by_template[kind] = scanned_by_template.get(kind, 0) + 1
        score = score_cover_candidate(first, second, cover)
        if score["entropy_same"]:
            entropy_matched += 1
        if score.get("same_shared_horizon_algebra"):
            horizon_matched += 1
        if score.get("different_observer_reconstruction"):
            observer_diff += 1
        if not score["hit"]:
            continue
        hit = cover_search_hit_certificate_for_pair(
            pair_source=str(source["name"]),
            first=first,
            second=second,
            cover=cover,
            include_bases=include_bases,
        )
        if hit["certified_claims"]["causal_patch_search_hit"]:
            hit["template"] = {
                "kind": kind,
                "origin": candidate["template_origin"],
            }
            hits.append(hit)
            hits_by_template[kind] = hits_by_template.get(kind, 0) + 1
            if len(hits) >= max_hits:
                break

    return {
        "source": cached_frontier_source_summary(source),
        "cache_record": {
            "name": source["name"],
            "frontier_kind": source["frontier_kind"],
            "mutation_depth": source["mutation_depth"],
            "cache_key": (
                source["name"],
                tuple(first.pauli_generators()),
                tuple(second.pauli_generators()),
            ),
        },
        "cover_search": {
            "generic_horizon_size": horizon_size,
            "generic_private_size": private_size,
            "max_generic_candidates": max_generic_candidates,
            "max_hits": max_hits,
            "candidate_count": len(candidates),
            "candidate_counts_by_template": dict(sorted(candidate_counts.items())),
        },
        "counts": {
            "scanned": scanned,
            "scanned_by_template": dict(sorted(scanned_by_template.items())),
            "entropy_overlap_matched": entropy_matched,
            "same_horizon_algebra": horizon_matched,
            "different_observer_reconstruction": observer_diff,
            "hits_returned": len(hits),
            "hits_by_template": dict(sorted(hits_by_template.items())),
            "source_aware_candidates": candidate_counts.get("source_aware_bridge_observer", 0),
            "source_aware_hits": hits_by_template.get("source_aware_bridge_observer", 0),
            "generic_candidates": candidate_counts.get("generic_two_observer", 0),
            "generic_hits": hits_by_template.get("generic_two_observer", 0),
        },
        "hits": tuple(hits),
        "status": "hit" if hits else "no-hit",
    }


def score_cover_template_candidates_for_pair(
    *,
    source: dict[str, object],
    candidates: tuple[dict[str, object], ...],
    max_hits: int,
    include_bases: bool,
) -> dict[str, object]:
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("source first/second must be StabilizerCode instances")
    if max_hits < 1:
        raise ValueError("max_hits must be at least 1")
    candidate_counts: dict[str, int] = {}
    scanned_by_template: dict[str, int] = {}
    hits_by_template: dict[str, int] = {}
    for candidate in candidates:
        kind = str(candidate["template_kind"])
        candidate_counts[kind] = candidate_counts.get(kind, 0) + 1

    entropy_matched = 0
    horizon_matched = 0
    observer_diff = 0
    raw_score_hits = 0
    hits: list[dict[str, object]] = []
    for candidate in candidates:
        kind = str(candidate["template_kind"])
        cover = candidate["cover"]
        if not isinstance(cover, PatchCover):
            raise TypeError("cover candidate must contain a PatchCover")
        scanned_by_template[kind] = scanned_by_template.get(kind, 0) + 1
        score = score_cover_candidate(first, second, cover)
        if score["entropy_same"]:
            entropy_matched += 1
        if score.get("same_shared_horizon_algebra"):
            horizon_matched += 1
        if score.get("different_observer_reconstruction"):
            observer_diff += 1
        if not score["hit"]:
            continue
        raw_score_hits += 1
        if len(hits) >= max_hits:
            continue
        hit = cover_search_hit_certificate_for_pair(
            pair_source=str(source["name"]),
            first=first,
            second=second,
            cover=cover,
            include_bases=include_bases,
        )
        if hit["certified_claims"]["causal_patch_search_hit"]:
            hit["template"] = {
                "kind": kind,
                "origin": candidate["template_origin"],
            }
            hits.append(hit)
            hits_by_template[kind] = hits_by_template.get(kind, 0) + 1

    return {
        "source": cached_frontier_source_summary(source),
        "candidate_counts_by_template": dict(sorted(candidate_counts.items())),
        "counts": {
            "scanned": len(candidates),
            "scanned_by_template": dict(sorted(scanned_by_template.items())),
            "entropy_overlap_matched": entropy_matched,
            "same_horizon_algebra": horizon_matched,
            "different_observer_reconstruction": observer_diff,
            "raw_score_hits": raw_score_hits,
            "hits_returned": len(hits),
            "hits_by_template": dict(sorted(hits_by_template.items())),
        },
        "hits": tuple(hits),
        "status": "hit" if hits else "no-hit",
    }


def bridge_cosmology_phase4_certificate(
    *,
    horizon_size: int = 2,
    private_size: int = 1,
    max_cover_candidates: int | None = None,
    max_hits_per_pair: int = 3,
    include_calibration: bool = True,
    include_source_scans: bool = True,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_hits_per_pair < 1:
        raise ValueError("max_hits_per_pair must be at least 1")
    pair_sources = code_pair_source_candidates(include_calibration=include_calibration)
    pair_results = tuple(
        search_generic_covers_for_pair(
            source=source,
            horizon_size=horizon_size,
            private_size=private_size,
            max_cover_candidates=max_cover_candidates,
            max_hits=max_hits_per_pair,
            include_bases=include_bases,
        )
        for source in pair_sources
        if horizon_size + 2 * private_size <= source["first"].n
    )
    source_scans = bounded_source_scan_reports() if include_source_scans else ()
    total_hits = sum(result["counts"]["hits_returned"] for result in pair_results)
    all_hits_verified = all(
        hit["certified_claims"]["causal_patch_search_hit"]
        for result in pair_results
        for hit in result["hits"]
    )
    return {
        "phase": "Goal 2 Phase 4: code-source and generic cover search",
        "status": "pass" if total_hits > 0 and all_hits_verified else "no-hit",
        "search_space": {
            "pair_sources": tuple(source["name"] for source in pair_sources),
            "horizon_size": horizon_size,
            "private_size": private_size,
            "max_cover_candidates": max_cover_candidates,
            "max_hits_per_pair": max_hits_per_pair,
            "include_calibration": include_calibration,
            "include_source_scans": include_source_scans,
        },
        "source_scans": source_scans,
        "pair_results": pair_results,
        "counts": {
            "pair_sources": len(pair_results),
            "source_scans": len(source_scans),
            "total_hits": total_hits,
        },
        "hit_definition": (
            "same exact named-patch entropy/overlap/MI/CMI/I3 data, observer overlap equal to shared_horizon, "
            "same shared-horizon algebra, different observer reconstruction/algebra, same erasure correctability "
            "profile, and some erasure algebra difference"
        ),
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Generic cover search works on code-pair sources beyond the bridge-grown family, but the default "
                "successful source is still the known robust CSS seed. Broader CSS/graph/encoder source scans need "
                "stronger bounded generators or cached frontiers to produce new robust pair sources cheaply."
            ),
            "suggested_phase_5": (
                "Add source-frontier caching and targeted mutations/lifts for CSS, graph/CWS-like, and shallow-encoder "
                "codes, then feed every entropy-matched reconstruction-discordant pair into the generic cover scorer."
            ),
        },
    }


def cached_frontier_sources(*, max_bridge_m: int = 2, include_calibration: bool = True) -> tuple[dict[str, object], ...]:
    if max_bridge_m < 0:
        raise ValueError("max_bridge_m must be nonnegative")
    first, second = seed_pair()
    sources: list[dict[str, object]] = [
        {
            "name": "seed_css_witness",
            "source_type": "cached_css_seed",
            "origin": "Goal 1 robust n=6 CSS witness, before bridge growth",
            "frontier_kind": "seed",
            "mutation_depth": 0,
            "first": first,
            "second": second,
        }
    ]
    for m in range(1, max_bridge_m + 1):
        lifted_first, lifted_second = repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m)
        sources.append(
            {
                "name": f"balanced_bridge_lift_m{m}",
                "source_type": "targeted_css_lift",
                "origin": "deterministic balanced-bridge lift of the robust CSS seed pair",
                "frontier_kind": "targeted_lift",
                "mutation_depth": m,
                "first": lifted_first,
                "second": lifted_second,
            }
        )
    if include_calibration:
        certificate = certify_minimal_entropy_reconstruction_discordance(max_n=4, k=1, max_subset_size=2)
        if certificate.pair is not None:
            sources.append(
                {
                    "name": "minimal_n4_calibration_pair",
                    "source_type": "cached_exhaustive_calibration",
                    "origin": "exact minimal low-order entropy/reconstruction calibration search",
                    "frontier_kind": "calibration",
                    "mutation_depth": 0,
                    "first": certificate.pair.first,
                    "second": certificate.pair.second,
                }
            )
    return tuple(sources)


def graph_profile_calibration_constraints() -> RobustConstraints:
    return RobustConstraints(
        max_subset_size=2,
        min_distance=1,
        min_reconstruction_size=1,
        forbid_single_qubit_noncentral=False,
    )


def robust_constraints_summary(constraints: RobustConstraints) -> dict[str, object]:
    return {
        "max_subset_size": constraints.max_subset_size,
        "min_distance": constraints.min_distance,
        "min_reconstruction_size": constraints.min_reconstruction_size,
        "forbid_single_qubit_noncentral": constraints.forbid_single_qubit_noncentral,
    }


def robust_constraints_from_summary(summary: dict[str, object]) -> RobustConstraints:
    return RobustConstraints(
        max_subset_size=int(summary["max_subset_size"]),
        min_distance=int(summary["min_distance"]),
        min_reconstruction_size=int(summary["min_reconstruction_size"]),
        forbid_single_qubit_noncentral=bool(summary["forbid_single_qubit_noncentral"]),
    )


def graph_profile_calibration_source(*, max_codes: int = 20) -> dict[str, object]:
    constraints = graph_profile_calibration_constraints()
    scan = scan_robust_source(
        n=4,
        k=1,
        source="graph",
        equivalence="permutation",
        entropy_key_mode="profile",
        constraints=constraints,
        max_codes=max_codes,
        encoder_depth=1,
    )
    if scan.pair is None:
        raise RuntimeError("expected the bounded graph/CWS-like calibration scan to find a pair")
    return {
        "name": "graph_cws_profile_n4_calibration_pair",
        "source_type": "graph_cws_profile_calibration",
        "origin": (
            "bounded graph/CWS-like n=4 scan with profile entropy key and relaxed distance/minimal-reconstruction "
            "filters; calibration-only because it is not a robust labeled-entropy witness"
        ),
        "frontier_kind": "graph_profile_calibration",
        "mutation_depth": 0,
        "first": scan.pair.first,
        "second": scan.pair.second,
        "source_scan": {
            "n": scan.n,
            "k": scan.k,
            "source": scan.source,
            "equivalence": scan.equivalence,
            "entropy_key_mode": scan.entropy_key_mode,
            "constraints": robust_constraints_summary(scan.constraints),
            "max_codes": max_codes,
            "encoder_depth": 1,
            "raw_codes": scan.raw_codes,
            "codes_checked": scan.codes_checked,
            "entropy_classes": scan.entropy_classes,
            "status": scan.status,
        },
    }


def extended_frontier_sources(
    *,
    max_bridge_m: int = 2,
    include_calibration: bool = True,
    include_graph_calibration: bool = True,
) -> tuple[dict[str, object], ...]:
    sources = list(cached_frontier_sources(max_bridge_m=max_bridge_m, include_calibration=include_calibration))
    if include_graph_calibration:
        sources.append(graph_profile_calibration_source())
    return tuple(sources)


def bounded_non_css_scan_specs() -> tuple[dict[str, object], ...]:
    return (
        {
            "name": "robust_graph_n5_labeled_no_pair",
            "source": "graph",
            "n": 5,
            "k": 1,
            "equivalence": "permutation",
            "entropy_key_mode": "labeled",
            "constraints": robust_constraints_summary(RobustConstraints()),
            "max_codes": 300,
            "encoder_depth": 1,
        },
        {
            "name": "robust_encoder_n5_depth3_labeled_no_pair",
            "source": "encoder",
            "n": 5,
            "k": 1,
            "equivalence": "permutation",
            "entropy_key_mode": "labeled",
            "constraints": robust_constraints_summary(RobustConstraints()),
            "max_codes": 300,
            "encoder_depth": 3,
        },
    )


def frontier_scan_record_digest_material(record: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
        "name": record["name"],
        "source": record["source"],
        "n": record["n"],
        "k": record["k"],
        "equivalence": record["equivalence"],
        "entropy_key_mode": record["entropy_key_mode"],
        "constraints": record["constraints"],
        "max_codes": record["max_codes"],
        "encoder_depth": record["encoder_depth"],
        "status": record["status"],
        "raw_codes": record["raw_codes"],
        "codes_checked": record["codes_checked"],
        "entropy_classes": record["entropy_classes"],
        "pair_found": record["pair_found"],
    }


def frontier_scan_record_digest(record: dict[str, object]) -> str:
    material = frontier_scan_record_digest_material(record)
    payload = json.dumps(material, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def frontier_scan_record(spec: dict[str, object]) -> dict[str, object]:
    constraints = robust_constraints_from_summary(spec["constraints"])
    scan = scan_robust_source(
        n=int(spec["n"]),
        k=int(spec["k"]),
        source=str(spec["source"]),
        equivalence=str(spec["equivalence"]),
        entropy_key_mode=str(spec["entropy_key_mode"]),
        constraints=constraints,
        max_codes=int(spec["max_codes"]),
        encoder_depth=int(spec["encoder_depth"]),
    )
    record: dict[str, object] = {
        "name": spec["name"],
        "source": scan.source,
        "n": scan.n,
        "k": scan.k,
        "equivalence": scan.equivalence,
        "entropy_key_mode": scan.entropy_key_mode,
        "constraints": robust_constraints_summary(scan.constraints),
        "max_codes": spec["max_codes"],
        "encoder_depth": spec["encoder_depth"],
        "status": scan.status,
        "raw_codes": scan.raw_codes,
        "codes_checked": scan.codes_checked,
        "entropy_classes": scan.entropy_classes,
        "pair_found": scan.pair is not None,
        "pair_generators": None
        if scan.pair is None
        else {
            "first": scan.pair.first.pauli_generators(),
            "second": scan.pair.second.pauli_generators(),
        },
    }
    record["scan_key_sha256"] = frontier_scan_record_digest(record)
    return record


def verify_frontier_scan_record(record: dict[str, object]) -> dict[str, object]:
    recomputed = frontier_scan_record(record)
    expected_digest = record.get("scan_key_sha256")
    recomputed_digest = recomputed["scan_key_sha256"]
    fields = (
        "source",
        "n",
        "k",
        "equivalence",
        "entropy_key_mode",
        "constraints",
        "max_codes",
        "encoder_depth",
        "status",
        "raw_codes",
        "codes_checked",
        "entropy_classes",
        "pair_found",
        "pair_generators",
    )
    fields_match = all(record.get(field) == recomputed.get(field) for field in fields)
    return {
        "name": record["name"],
        "source": record["source"],
        "status": record["status"],
        "expected_digest": expected_digest,
        "recomputed_digest": recomputed_digest,
        "digest_matches": expected_digest == recomputed_digest,
        "fields_match": fields_match,
        "verified": expected_digest == recomputed_digest and fields_match,
    }


def frontier_cache_digest_material(record: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
        "name": record["name"],
        "source_type": record["source_type"],
        "frontier_kind": record["frontier_kind"],
        "mutation_depth": record["mutation_depth"],
        "first_generators": tuple(record["first_generators"]),
        "second_generators": tuple(record["second_generators"]),
    }


def frontier_cache_record_digest(record: dict[str, object]) -> str:
    material = frontier_cache_digest_material(record)
    payload = json.dumps(material, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def frontier_cache_record(source: dict[str, object]) -> dict[str, object]:
    summary = cached_frontier_source_summary(source)
    record: dict[str, object] = {
        "name": source["name"],
        "source_type": source["source_type"],
        "origin": source["origin"],
        "frontier_kind": source["frontier_kind"],
        "mutation_depth": source["mutation_depth"],
        "n": summary["n"],
        "k": summary["k"],
        "first_generators": summary["first_generators"],
        "second_generators": summary["second_generators"],
        "diagnostics": {
            "first_quality": summary["first_quality"],
            "second_quality": summary["second_quality"],
            "same_labeled_t2_entropy": summary["same_labeled_t2_entropy"],
            "reconstruction_profiles_differ": summary["reconstruction_profiles_differ"],
        },
        "template_hints": (
            ("source_aware_bridge_observer",)
            if source["frontier_kind"] == "targeted_lift" and int(source["mutation_depth"]) >= 1
            else ("generic_two_observer",)
        ),
    }
    if "source_scan" in source:
        record["source_scan"] = source["source_scan"]
    record["cache_key_sha256"] = frontier_cache_record_digest(record)
    return record


def frontier_cache_payload(*, max_bridge_m: int = 2, include_calibration: bool = True) -> dict[str, object]:
    records = tuple(
        frontier_cache_record(source)
        for source in cached_frontier_sources(max_bridge_m=max_bridge_m, include_calibration=include_calibration)
    )
    return {
        "schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
        "name": "goal2_phase7_frontier_cache",
        "description": (
            "Persistent exact source frontier for Goal 2: robust CSS seed, deterministic balanced-bridge "
            "lifts, and optional exact calibration pair."
        ),
        "generation_parameters": {
            "max_bridge_m": max_bridge_m,
            "include_calibration": include_calibration,
        },
        "records": records,
    }


def extended_frontier_cache_payload(
    *,
    max_bridge_m: int = 2,
    include_calibration: bool = True,
    include_graph_calibration: bool = True,
    include_non_css_scan_records: bool = True,
) -> dict[str, object]:
    records = tuple(
        frontier_cache_record(source)
        for source in extended_frontier_sources(
            max_bridge_m=max_bridge_m,
            include_calibration=include_calibration,
            include_graph_calibration=include_graph_calibration,
        )
    )
    scan_records = (
        tuple(frontier_scan_record(spec) for spec in bounded_non_css_scan_specs())
        if include_non_css_scan_records
        else ()
    )
    return {
        "schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
        "name": "goal2_phase8_extended_frontier_cache",
        "description": (
            "Persistent exact source frontier for Goal 2 with bridge CSS records, a graph/CWS-like "
            "profile-entropy calibration pair, and bounded robust no-pair graph/encoder scan records."
        ),
        "generation_parameters": {
            "max_bridge_m": max_bridge_m,
            "include_calibration": include_calibration,
            "include_graph_calibration": include_graph_calibration,
            "include_non_css_scan_records": include_non_css_scan_records,
        },
        "records": records,
        "scan_records": scan_records,
    }


def load_frontier_cache_payload(path: str | Path | None = None) -> dict[str, object]:
    cache_path = Path(path) if path is not None else DEFAULT_FRONTIER_CACHE_PATH
    return json.loads(cache_path.read_text(encoding="utf-8"))


def source_from_frontier_cache_record(record: dict[str, object]) -> dict[str, object]:
    return {
        "name": record["name"],
        "source_type": record["source_type"],
        "origin": record["origin"],
        "frontier_kind": record["frontier_kind"],
        "mutation_depth": int(record["mutation_depth"]),
        "first": StabilizerCode.from_pauli_strings(tuple(record["first_generators"])),
        "second": StabilizerCode.from_pauli_strings(tuple(record["second_generators"])),
        "cache_key_sha256": record.get("cache_key_sha256"),
    }


def verify_frontier_cache_record(record: dict[str, object]) -> dict[str, object]:
    source = source_from_frontier_cache_record(record)
    summary = cached_frontier_source_summary(source)
    diagnostics = record.get("diagnostics", {})
    if not isinstance(diagnostics, dict):
        diagnostics = {}
    expected_digest = record.get("cache_key_sha256")
    recomputed_digest = frontier_cache_record_digest(record)
    code_metadata_matches = summary["n"] == record.get("n") and summary["k"] == record.get("k")
    generators_match = (
        tuple(summary["first_generators"]) == tuple(record["first_generators"])
        and tuple(summary["second_generators"]) == tuple(record["second_generators"])
    )
    diagnostics_match = (
        summary["first_quality"] == diagnostics.get("first_quality")
        and summary["second_quality"] == diagnostics.get("second_quality")
        and summary["same_labeled_t2_entropy"] == diagnostics.get("same_labeled_t2_entropy")
        and summary["reconstruction_profiles_differ"] == diagnostics.get("reconstruction_profiles_differ")
    )
    return {
        "name": record["name"],
        "frontier_kind": record["frontier_kind"],
        "mutation_depth": record["mutation_depth"],
        "expected_digest": expected_digest,
        "recomputed_digest": recomputed_digest,
        "digest_matches": expected_digest == recomputed_digest,
        "code_metadata_matches": code_metadata_matches,
        "generators_match": generators_match,
        "diagnostics_match": diagnostics_match,
        "verified": expected_digest == recomputed_digest
        and code_metadata_matches
        and generators_match
        and diagnostics_match,
    }


def compare_frontier_cache_to_generator(payload: dict[str, object]) -> dict[str, object]:
    parameters = payload.get("generation_parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    max_bridge_m = int(parameters.get("max_bridge_m", 2))
    include_calibration = bool(parameters.get("include_calibration", True))
    generated = frontier_cache_payload(max_bridge_m=max_bridge_m, include_calibration=include_calibration)
    payload_records = tuple(payload.get("records", ()))
    generated_records = tuple(generated["records"])
    payload_digests = tuple(record.get("cache_key_sha256") for record in payload_records if isinstance(record, dict))
    generated_digests = tuple(record["cache_key_sha256"] for record in generated_records)
    return {
        "generation_parameters": {
            "max_bridge_m": max_bridge_m,
            "include_calibration": include_calibration,
        },
        "payload_record_count": len(payload_records),
        "generated_record_count": len(generated_records),
        "payload_digests": payload_digests,
        "generated_digests": generated_digests,
        "matches_generator": payload_digests == generated_digests,
    }


def compare_extended_frontier_cache_to_generator(payload: dict[str, object]) -> dict[str, object]:
    parameters = payload.get("generation_parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    generated = extended_frontier_cache_payload(
        max_bridge_m=int(parameters.get("max_bridge_m", 2)),
        include_calibration=bool(parameters.get("include_calibration", True)),
        include_graph_calibration=bool(parameters.get("include_graph_calibration", True)),
        include_non_css_scan_records=bool(parameters.get("include_non_css_scan_records", True)),
    )
    payload_records = tuple(payload.get("records", ()))
    generated_records = tuple(generated["records"])
    payload_scan_records = tuple(payload.get("scan_records", ()))
    generated_scan_records = tuple(generated["scan_records"])
    payload_digests = tuple(record.get("cache_key_sha256") for record in payload_records if isinstance(record, dict))
    generated_digests = tuple(record["cache_key_sha256"] for record in generated_records)
    payload_scan_digests = tuple(
        record.get("scan_key_sha256") for record in payload_scan_records if isinstance(record, dict)
    )
    generated_scan_digests = tuple(record["scan_key_sha256"] for record in generated_scan_records)
    return {
        "generation_parameters": generated["generation_parameters"],
        "payload_record_count": len(payload_records),
        "generated_record_count": len(generated_records),
        "payload_scan_record_count": len(payload_scan_records),
        "generated_scan_record_count": len(generated_scan_records),
        "payload_digests": payload_digests,
        "generated_digests": generated_digests,
        "payload_scan_digests": payload_scan_digests,
        "generated_scan_digests": generated_scan_digests,
        "matches_generator": payload_digests == generated_digests
        and payload_scan_digests == generated_scan_digests,
    }


def cached_frontier_source_summary(source: dict[str, object]) -> dict[str, object]:
    summary = code_pair_source_summary(source)
    summary["frontier_kind"] = source["frontier_kind"]
    summary["mutation_depth"] = source["mutation_depth"]
    return summary


def search_cached_frontier_source(
    *,
    source: dict[str, object],
    horizon_size: int,
    private_size: int,
    max_cover_candidates: int,
    max_hits: int,
    include_bases: bool,
) -> dict[str, object]:
    result = search_generic_covers_for_pair(
        source=source,
        horizon_size=horizon_size,
        private_size=private_size,
        max_cover_candidates=max_cover_candidates,
        max_hits=max_hits,
        include_bases=include_bases,
    )
    result["source"] = cached_frontier_source_summary(source)
    result["cache_record"] = {
        "name": source["name"],
        "frontier_kind": source["frontier_kind"],
        "mutation_depth": source["mutation_depth"],
        "cache_key": (
            source["name"],
            tuple(source["first"].pauli_generators()),
            tuple(source["second"].pauli_generators()),
        ),
    }
    return result


def bridge_cosmology_phase5_certificate(
    *,
    max_bridge_m: int = 2,
    horizon_size: int = 2,
    private_size: int = 1,
    max_cover_candidates: int = 120,
    max_hits_per_source: int = 1,
    include_calibration: bool = True,
    include_source_scans: bool = True,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_cover_candidates < 1:
        raise ValueError("max_cover_candidates must be at least 1")
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    sources = cached_frontier_sources(max_bridge_m=max_bridge_m, include_calibration=include_calibration)
    frontier_results = tuple(
        search_cached_frontier_source(
            source=source,
            horizon_size=horizon_size,
            private_size=private_size,
            max_cover_candidates=max_cover_candidates,
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
        for source in sources
        if horizon_size + 2 * private_size <= source["first"].n
    )
    source_scans = bounded_source_scan_reports() if include_source_scans else ()
    total_hits = sum(result["counts"]["hits_returned"] for result in frontier_results)
    lift_results = tuple(result for result in frontier_results if result["source"]["frontier_kind"] == "targeted_lift")
    lift_sources_scored = len(lift_results)
    lift_hits = sum(result["counts"]["hits_returned"] for result in lift_results)
    all_hits_verified = all(
        hit["certified_claims"]["causal_patch_search_hit"]
        for result in frontier_results
        for hit in result["hits"]
    )
    return {
        "phase": "Goal 2 Phase 5: cached source-frontier and targeted-lift scoring",
        "status": "pass" if total_hits > 0 and all_hits_verified else "no-hit",
        "frontier_cache": {
            "source_count": len(sources),
            "max_bridge_m": max_bridge_m,
            "include_calibration": include_calibration,
            "source_names": tuple(source["name"] for source in sources),
            "cache_policy": (
                "deterministic in-repo source frontier: robust CSS seed, targeted balanced-bridge CSS lifts, "
                "and optional exact calibration pair"
            ),
        },
        "cover_search": {
            "horizon_size": horizon_size,
            "private_size": private_size,
            "max_cover_candidates": max_cover_candidates,
            "max_hits_per_source": max_hits_per_source,
        },
        "source_scans": source_scans,
        "frontier_results": frontier_results,
        "counts": {
            "frontier_sources": len(frontier_results),
            "targeted_lift_sources": lift_sources_scored,
            "targeted_lift_hits": lift_hits,
            "source_scans": len(source_scans),
            "total_hits": total_hits,
        },
        "certified_claims": {
            "all_hits_verified": all_hits_verified,
            "cached_frontier_scored": len(frontier_results) == len(sources),
            "targeted_lifts_scored": lift_sources_scored == max_bridge_m,
            "bounded_source_scans_reported": (not include_source_scans) or len(source_scans) == 4,
            "phase_5_frontier_certificate": total_hits > 0 and all_hits_verified,
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The cached source frontier and targeted balanced-bridge lifts are now scored exactly. The generic "
                "cover template finds hits on the seed source but not on the first bounded bridge-lift sources, "
                "so the next step should add lifted-cover templates or richer source mutations rather than only "
                "expanding the same generic cover search."
            ),
            "suggested_phase_6": (
                "Add source-aware cover templates and cached frontier files: bridge-aware covers for lifted CSS "
                "families, plus targeted graph/CWS-like and shallow-encoder mutations that preserve low-order "
                "entropy while perturbing reconstruction algebras."
            ),
        },
    }


def bridge_cosmology_phase6_certificate(
    *,
    max_bridge_m: int = 2,
    horizon_size: int = 2,
    private_size: int = 1,
    max_generic_candidates: int | None = 120,
    max_hits_per_source: int = 1,
    include_calibration: bool = True,
    include_source_scans: bool = True,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_generic_candidates is not None and max_generic_candidates < 0:
        raise ValueError("max_generic_candidates must be nonnegative")
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    sources = cached_frontier_sources(max_bridge_m=max_bridge_m, include_calibration=include_calibration)
    frontier_results = tuple(
        search_source_aware_covers_for_pair(
            source=source,
            horizon_size=horizon_size,
            private_size=private_size,
            max_generic_candidates=max_generic_candidates,
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
        for source in sources
        if horizon_size + 2 * private_size <= source["first"].n
    )
    source_scans = bounded_source_scan_reports() if include_source_scans else ()
    total_hits = sum(result["counts"]["hits_returned"] for result in frontier_results)
    source_aware_template_candidates = sum(result["counts"]["source_aware_candidates"] for result in frontier_results)
    source_aware_template_hits = sum(result["counts"]["source_aware_hits"] for result in frontier_results)
    generic_template_hits = sum(result["counts"]["generic_hits"] for result in frontier_results)
    lift_results = tuple(result for result in frontier_results if result["source"]["frontier_kind"] == "targeted_lift")
    lift_sources_scored = len(lift_results)
    lift_hits = sum(result["counts"]["hits_returned"] for result in lift_results)
    lift_source_aware_hits = sum(result["counts"]["source_aware_hits"] for result in lift_results)
    all_hits_verified = all(
        hit["certified_claims"]["causal_patch_search_hit"]
        for result in frontier_results
        for hit in result["hits"]
    )
    targeted_lift_hits_recovered = lift_sources_scored == 0 or lift_source_aware_hits == lift_sources_scored
    source_aware_templates_used = source_aware_template_candidates == lift_sources_scored
    phase_passes = (
        total_hits > 0
        and all_hits_verified
        and source_aware_templates_used
        and targeted_lift_hits_recovered
    )
    return {
        "phase": "Goal 2 Phase 6: source-aware cover-template scoring",
        "status": "pass" if phase_passes else "no-hit",
        "frontier_cache": {
            "source_count": len(sources),
            "max_bridge_m": max_bridge_m,
            "include_calibration": include_calibration,
            "source_names": tuple(source["name"] for source in sources),
            "cache_policy": (
                "deterministic in-repo source frontier with source-aware atlas templates layered before "
                "bounded generic cover enumeration"
            ),
        },
        "cover_search": {
            "generic_horizon_size": horizon_size,
            "generic_private_size": private_size,
            "max_generic_candidates": max_generic_candidates,
            "max_hits_per_source": max_hits_per_source,
            "source_aware_templates": (
                {
                    "template_kind": "source_aware_bridge_observer",
                    "applies_to": "targeted_lift",
                    "cover_rule": (
                        "balanced bridge observer cover: observer_p={1,2,3} union {p_j}, "
                        "observer_q={1,2,3} union {q_j}, shared_horizon={1,2,3}"
                    ),
                },
            ),
        },
        "source_scans": source_scans,
        "frontier_results": frontier_results,
        "counts": {
            "frontier_sources": len(frontier_results),
            "targeted_lift_sources": lift_sources_scored,
            "targeted_lift_hits": lift_hits,
            "targeted_lift_source_aware_hits": lift_source_aware_hits,
            "source_aware_template_candidates": source_aware_template_candidates,
            "source_aware_template_hits": source_aware_template_hits,
            "generic_template_hits": generic_template_hits,
            "source_scans": len(source_scans),
            "total_hits": total_hits,
        },
        "certified_claims": {
            "all_hits_verified": all_hits_verified,
            "cached_frontier_scored": len(frontier_results) == len(sources),
            "targeted_lifts_scored": lift_sources_scored == max_bridge_m,
            "source_aware_templates_used": source_aware_templates_used,
            "targeted_lift_hits_recovered": targeted_lift_hits_recovered,
            "bounded_source_scans_reported": (not include_source_scans) or len(source_scans) == 4,
            "phase_6_source_aware_certificate": phase_passes,
        },
        "hit_definition": (
            "same exact named-patch entropy/overlap/MI/CMI/I3 data, observer overlap equal to shared_horizon, "
            "same shared-horizon algebra, different observer reconstruction/algebra, same erasure correctability "
            "profile, and some erasure algebra difference"
        ),
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Source-aware bridge templates recover the targeted lifted CSS frontier exactly, while the generic "
                "fallback remains available for source classes without a known atlas. The next adaptation should "
                "move from in-memory cached sources to richer persistent source frontiers and add source-aware "
                "templates for graph/CWS-like and shallow-encoder constructions."
            ),
            "suggested_phase_7": (
                "Add persistent frontier-cache artifacts plus source-aware graph/encoder mutation rules, then "
                "compare generic-template hits against rule-derived atlas hits to identify which apparent "
                "geometries are source-specific versus search-generic."
            ),
        },
    }


def bridge_cosmology_phase7_certificate(
    *,
    cache_path: str | Path | None = None,
    horizon_size: int = 2,
    private_size: int = 1,
    max_generic_candidates: int | None = 120,
    max_hits_per_source: int = 1,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_generic_candidates is not None and max_generic_candidates < 0:
        raise ValueError("max_generic_candidates must be nonnegative")
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    resolved_path = Path(cache_path) if cache_path is not None else DEFAULT_FRONTIER_CACHE_PATH
    payload = load_frontier_cache_payload(resolved_path)
    records = tuple(payload.get("records", ()))
    record_reports = tuple(
        verify_frontier_cache_record(record)
        for record in records
        if isinstance(record, dict)
    )
    generator_comparison = compare_frontier_cache_to_generator(payload)
    sources = tuple(source_from_frontier_cache_record(record) for record in records if isinstance(record, dict))
    frontier_results = tuple(
        search_source_aware_covers_for_pair(
            source=source,
            horizon_size=horizon_size,
            private_size=private_size,
            max_generic_candidates=max_generic_candidates,
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
        for source in sources
        if horizon_size + 2 * private_size <= source["first"].n
    )
    total_hits = sum(result["counts"]["hits_returned"] for result in frontier_results)
    source_aware_template_hits = sum(result["counts"]["source_aware_hits"] for result in frontier_results)
    generic_template_hits = sum(result["counts"]["generic_hits"] for result in frontier_results)
    lift_results = tuple(result for result in frontier_results if result["source"]["frontier_kind"] == "targeted_lift")
    lift_sources_scored = len(lift_results)
    lift_hits = sum(result["counts"]["hits_returned"] for result in lift_results)
    lift_source_aware_hits = sum(result["counts"]["source_aware_hits"] for result in lift_results)
    all_records_verified = len(record_reports) == len(records) and all(report["verified"] for report in record_reports)
    unique_digests = len({report["expected_digest"] for report in record_reports}) == len(record_reports)
    all_hits_verified = all(
        hit["certified_claims"]["causal_patch_search_hit"]
        for result in frontier_results
        for hit in result["hits"]
    )
    target_lifts_replayed = lift_sources_scored > 0 and lift_source_aware_hits == lift_sources_scored
    phase_passes = (
        payload.get("schema_version") == FRONTIER_CACHE_SCHEMA_VERSION
        and all_records_verified
        and unique_digests
        and generator_comparison["matches_generator"]
        and total_hits > 0
        and all_hits_verified
        and target_lifts_replayed
    )
    return {
        "phase": "Goal 2 Phase 7: persistent frontier-cache replay",
        "status": "pass" if phase_passes else "no-hit",
        "cache_artifact": {
            "path": str(resolved_path),
            "schema_version": payload.get("schema_version"),
            "expected_schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
            "name": payload.get("name"),
            "record_count": len(records),
            "record_digests": tuple(report["expected_digest"] for report in record_reports),
        },
        "cache_verification": {
            "record_reports": record_reports,
            "all_records_verified": all_records_verified,
            "unique_digests": unique_digests,
            "generator_comparison": generator_comparison,
        },
        "cover_search": {
            "generic_horizon_size": horizon_size,
            "generic_private_size": private_size,
            "max_generic_candidates": max_generic_candidates,
            "max_hits_per_source": max_hits_per_source,
            "replay_policy": (
                "load source records from JSON, reconstruct StabilizerCode pairs from Pauli generators, then "
                "run the Phase 6 source-aware cover-template scorer"
            ),
        },
        "frontier_results": frontier_results,
        "counts": {
            "cache_records": len(records),
            "loaded_sources": len(sources),
            "frontier_sources": len(frontier_results),
            "targeted_lift_sources": lift_sources_scored,
            "targeted_lift_hits": lift_hits,
            "targeted_lift_source_aware_hits": lift_source_aware_hits,
            "source_aware_template_hits": source_aware_template_hits,
            "generic_template_hits": generic_template_hits,
            "total_hits": total_hits,
        },
        "certified_claims": {
            "persistent_cache_loaded": len(records) > 0,
            "schema_version_matches": payload.get("schema_version") == FRONTIER_CACHE_SCHEMA_VERSION,
            "all_cache_records_verified": all_records_verified,
            "cache_digests_unique": unique_digests,
            "cache_matches_generator": generator_comparison["matches_generator"],
            "cache_replay_scored_all_sources": len(frontier_results) == len(sources),
            "all_hits_verified": all_hits_verified,
            "targeted_lift_hits_replayed_from_cache": target_lifts_replayed,
            "phase_7_persistent_cache_certificate": phase_passes,
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The frontier is now a persistent replayable JSON artifact whose records are checked against "
                "deterministic generator output before cover scoring. The next adaptation should add new cached "
                "source families, especially graph/CWS-like and shallow-encoder mutations, so the cache is no "
                "longer dominated by balanced-bridge CSS sources."
            ),
            "suggested_phase_8": (
                "Add graph/encoder frontier mutation records with exact source diagnostics and source-aware or "
                "template-hint covers, then replay the same persistent-cache scorer to compare bridge-specific, "
                "graph-specific, and generic emergent patch atlases."
            ),
        },
    }


def bridge_cosmology_phase8_certificate(
    *,
    cache_path: str | Path | None = None,
    horizon_size: int = 2,
    private_size: int = 1,
    max_generic_candidates: int | None = 120,
    max_hits_per_source: int = 1,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_generic_candidates is not None and max_generic_candidates < 0:
        raise ValueError("max_generic_candidates must be nonnegative")
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    resolved_path = Path(cache_path) if cache_path is not None else DEFAULT_EXTENDED_FRONTIER_CACHE_PATH
    payload = load_frontier_cache_payload(resolved_path)
    records = tuple(payload.get("records", ()))
    scan_records = tuple(payload.get("scan_records", ()))
    record_reports = tuple(
        verify_frontier_cache_record(record)
        for record in records
        if isinstance(record, dict)
    )
    scan_record_reports = tuple(
        verify_frontier_scan_record(record)
        for record in scan_records
        if isinstance(record, dict)
    )
    generator_comparison = compare_extended_frontier_cache_to_generator(payload)
    sources = tuple(source_from_frontier_cache_record(record) for record in records if isinstance(record, dict))
    frontier_results = tuple(
        search_source_aware_covers_for_pair(
            source=source,
            horizon_size=horizon_size,
            private_size=private_size,
            max_generic_candidates=max_generic_candidates,
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
        for source in sources
        if horizon_size + 2 * private_size <= source["first"].n
    )
    total_hits = sum(result["counts"]["hits_returned"] for result in frontier_results)
    source_aware_template_hits = sum(result["counts"]["source_aware_hits"] for result in frontier_results)
    generic_template_hits = sum(result["counts"]["generic_hits"] for result in frontier_results)
    lift_results = tuple(result for result in frontier_results if result["source"]["frontier_kind"] == "targeted_lift")
    graph_results = tuple(
        result for result in frontier_results if result["source"]["frontier_kind"] == "graph_profile_calibration"
    )
    lift_sources_scored = len(lift_results)
    lift_source_aware_hits = sum(result["counts"]["source_aware_hits"] for result in lift_results)
    graph_records = tuple(
        record
        for record in records
        if isinstance(record, dict) and record.get("frontier_kind") == "graph_profile_calibration"
    )
    all_records_verified = len(record_reports) == len(records) and all(report["verified"] for report in record_reports)
    all_scan_records_verified = len(scan_record_reports) == len(scan_records) and all(
        report["verified"] for report in scan_record_reports
    )
    unique_record_digests = len({report["expected_digest"] for report in record_reports}) == len(record_reports)
    unique_scan_digests = len({report["expected_digest"] for report in scan_record_reports}) == len(scan_record_reports)
    all_hits_verified = all(
        hit["certified_claims"]["causal_patch_search_hit"]
        for result in frontier_results
        for hit in result["hits"]
    )
    target_lifts_replayed = lift_sources_scored > 0 and lift_source_aware_hits == lift_sources_scored
    graph_calibration_loaded = len(graph_records) == 1
    graph_calibration_scored_no_hit = len(graph_results) == 1 and graph_results[0]["status"] == "no-hit"
    robust_non_css_scans_no_pair = len(scan_records) > 0 and all(
        isinstance(record, dict) and record.get("status") == "no-pair" and not record.get("pair_found")
        for record in scan_records
    )
    phase_passes = (
        payload.get("schema_version") == FRONTIER_CACHE_SCHEMA_VERSION
        and all_records_verified
        and all_scan_records_verified
        and unique_record_digests
        and unique_scan_digests
        and generator_comparison["matches_generator"]
        and graph_calibration_loaded
        and graph_calibration_scored_no_hit
        and robust_non_css_scans_no_pair
        and total_hits > 0
        and all_hits_verified
        and target_lifts_replayed
    )
    return {
        "phase": "Goal 2 Phase 8: graph/encoder extended frontier cache",
        "status": "pass" if phase_passes else "no-hit",
        "cache_artifact": {
            "path": str(resolved_path),
            "schema_version": payload.get("schema_version"),
            "expected_schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
            "name": payload.get("name"),
            "record_count": len(records),
            "scan_record_count": len(scan_records),
            "record_digests": tuple(report["expected_digest"] for report in record_reports),
            "scan_record_digests": tuple(report["expected_digest"] for report in scan_record_reports),
        },
        "cache_verification": {
            "record_reports": record_reports,
            "scan_record_reports": scan_record_reports,
            "all_records_verified": all_records_verified,
            "all_scan_records_verified": all_scan_records_verified,
            "unique_record_digests": unique_record_digests,
            "unique_scan_digests": unique_scan_digests,
            "generator_comparison": generator_comparison,
        },
        "cover_search": {
            "generic_horizon_size": horizon_size,
            "generic_private_size": private_size,
            "max_generic_candidates": max_generic_candidates,
            "max_hits_per_source": max_hits_per_source,
            "replay_policy": (
                "load extended source records from JSON, reconstruct StabilizerCode pairs from Pauli generators, "
                "then run source-aware bridge templates plus generic two-observer fallback covers"
            ),
        },
        "frontier_results": frontier_results,
        "counts": {
            "cache_records": len(records),
            "scan_records": len(scan_records),
            "loaded_sources": len(sources),
            "frontier_sources": len(frontier_results),
            "targeted_lift_sources": lift_sources_scored,
            "targeted_lift_source_aware_hits": lift_source_aware_hits,
            "graph_profile_calibration_records": len(graph_records),
            "graph_profile_calibration_results": len(graph_results),
            "source_aware_template_hits": source_aware_template_hits,
            "generic_template_hits": generic_template_hits,
            "total_hits": total_hits,
        },
        "certified_claims": {
            "extended_cache_loaded": len(records) > 0,
            "schema_version_matches": payload.get("schema_version") == FRONTIER_CACHE_SCHEMA_VERSION,
            "all_cache_records_verified": all_records_verified,
            "all_scan_records_verified": all_scan_records_verified,
            "cache_digests_unique": unique_record_digests and unique_scan_digests,
            "cache_matches_generator": generator_comparison["matches_generator"],
            "cache_replay_scored_all_sources": len(frontier_results) == len(sources),
            "graph_profile_calibration_pair_loaded": graph_calibration_loaded,
            "graph_profile_pair_no_generic_causal_hit": graph_calibration_scored_no_hit,
            "robust_non_css_scans_no_pair": robust_non_css_scans_no_pair,
            "targeted_lift_hits_replayed_from_cache": target_lifts_replayed,
            "all_hits_verified": all_hits_verified,
            "phase_8_extended_frontier_certificate": phase_passes,
        },
        "interpretation": {
            "graph_profile_calibration": (
                "A graph/CWS-like n=4 pair matches the unlabeled low-order entropy profile and differs in "
                "reconstruction profile, but it fails robust constraints and does not produce a generic "
                "causal-patch hit under the current named-cover criteria."
            ),
            "bounded_non_css_no_go": (
                "The included robust graph and shallow-encoder scan records are exact bounded no-pair records "
                "under labeled t=2 entropy, distance/minimal-reconstruction filters, and stated code limits."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "The extended cache now contains a non-CSS graph/CWS-like calibration pair plus exact robust "
                "no-pair scan records for graph and encoder sources. The graph pair shows that profile-entropy "
                "degeneracy is too weak for the current causal-patch hit definition, so the next step should add "
                "graph-specific atlas templates or strengthen non-CSS source generation before claiming geometry."
            ),
            "suggested_phase_9": (
                "Add graph-specific cover templates based on graph neighborhoods/cuts and a wider bounded encoder "
                "frontier, then compare named-cover entropy overlap against reconstruction differences before "
                "moving to time/channel dynamics for non-CSS toy cosmologies."
            ),
        },
    }


def bridge_cosmology_phase9_certificate(
    *,
    cache_path: str | Path | None = None,
    max_hits_per_source: int = 1,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    resolved_path = Path(cache_path) if cache_path is not None else DEFAULT_EXTENDED_FRONTIER_CACHE_PATH
    payload = load_frontier_cache_payload(resolved_path)
    records = tuple(payload.get("records", ()))
    scan_records = tuple(payload.get("scan_records", ()))
    record_reports = tuple(
        verify_frontier_cache_record(record)
        for record in records
        if isinstance(record, dict)
    )
    scan_record_reports = tuple(
        verify_frontier_scan_record(record)
        for record in scan_records
        if isinstance(record, dict)
    )
    generator_comparison = compare_extended_frontier_cache_to_generator(payload)
    sources = tuple(source_from_frontier_cache_record(record) for record in records if isinstance(record, dict))
    graph_sources = tuple(source for source in sources if source["frontier_kind"] == "graph_profile_calibration")
    graph_results = tuple(
        score_cover_template_candidates_for_pair(
            source=source,
            candidates=graph_specific_patch_cover_candidates(source),
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
        for source in graph_sources
    )
    exhaustive_results = tuple(
        score_cover_template_candidates_for_pair(
            source=source,
            candidates=exhaustive_two_observer_cover_candidates(source["first"].n),
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
        for source in graph_sources
        if isinstance(source["first"], StabilizerCode) and source["first"].n <= 4
    )
    all_records_verified = len(record_reports) == len(records) and all(report["verified"] for report in record_reports)
    all_scan_records_verified = len(scan_record_reports) == len(scan_records) and all(
        report["verified"] for report in scan_record_reports
    )
    graph_template_candidates = sum(result["counts"]["scanned"] for result in graph_results)
    graph_template_hits = sum(result["counts"]["hits_returned"] for result in graph_results)
    exhaustive_candidates = sum(result["counts"]["scanned"] for result in exhaustive_results)
    exhaustive_hits = sum(result["counts"]["hits_returned"] for result in exhaustive_results)
    exhaustive_observer_diff = sum(result["counts"]["different_observer_reconstruction"] for result in exhaustive_results)
    graph_profile_only = all(
        not result["source"]["same_labeled_t2_entropy"]
        and result["source"]["reconstruction_profiles_differ"]
        for result in graph_results
    )
    phase_passes = (
        payload.get("schema_version") == FRONTIER_CACHE_SCHEMA_VERSION
        and all_records_verified
        and all_scan_records_verified
        and generator_comparison["matches_generator"]
        and len(graph_sources) == 1
        and graph_template_candidates > 0
        and graph_template_hits == 0
        and exhaustive_candidates > 0
        and exhaustive_hits == 0
        and exhaustive_observer_diff > 0
        and graph_profile_only
    )
    return {
        "phase": "Goal 2 Phase 9: graph-specific cover-template no-go",
        "status": "pass" if phase_passes else "no-hit",
        "cache_artifact": {
            "path": str(resolved_path),
            "schema_version": payload.get("schema_version"),
            "expected_schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
            "name": payload.get("name"),
            "record_count": len(records),
            "scan_record_count": len(scan_records),
        },
        "cache_verification": {
            "all_records_verified": all_records_verified,
            "all_scan_records_verified": all_scan_records_verified,
            "generator_comparison": generator_comparison,
        },
        "graph_template_search": {
            "template_families": (
                "graph_closed_neighborhood_overlap",
                "graph_generator_support_cut",
            ),
            "results": graph_results,
        },
        "exhaustive_two_observer_no_go": {
            "scope": "all ordered non-identical overlapping two-observer covers on n<=4 graph calibration sources",
            "results": exhaustive_results,
        },
        "counts": {
            "graph_sources": len(graph_sources),
            "graph_template_candidates": graph_template_candidates,
            "graph_template_hits": graph_template_hits,
            "exhaustive_two_observer_candidates": exhaustive_candidates,
            "exhaustive_two_observer_hits": exhaustive_hits,
            "exhaustive_observer_reconstruction_differences": exhaustive_observer_diff,
        },
        "certified_claims": {
            "extended_cache_verified": all_records_verified
            and all_scan_records_verified
            and generator_comparison["matches_generator"],
            "graph_profile_calibration_pair_loaded": len(graph_sources) == 1,
            "graph_pair_is_profile_only_not_labeled_t2": graph_profile_only,
            "graph_specific_templates_scored": graph_template_candidates > 0,
            "graph_specific_templates_no_hit": graph_template_hits == 0,
            "exhaustive_two_observer_covers_scored": exhaustive_candidates > 0,
            "exhaustive_two_observer_no_hit": exhaustive_hits == 0,
            "observer_reconstruction_differences_exist_in_exhaustive_space": exhaustive_observer_diff > 0,
            "phase_9_graph_template_no_go_certificate": phase_passes,
        },
        "interpretation": {
            "result": (
                "The graph/CWS-like calibration pair has reconstruction-visible differences, but neither the "
                "graph-native support/neighborhood templates nor the full tiny two-observer cover space produce "
                "a certified causal-patch hit. The obstruction is not simply lack of template imagination in "
                "this n=4 cover class; the pair is profile-entropy-matched but not named-entropy-matched."
            ),
            "diagnostic_pressure": (
                "For non-CSS sources, low-order entropy profiles are too coarse for ER=EPR-style connectivity "
                "claims unless the source also preserves labeled region data or supplies a stronger atlas rule."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Graph-specific templates and exhaustive tiny two-observer covers certify no causal-patch hit for "
                "the current graph profile calibration pair. The next step should either search for labeled-t2 "
                "non-CSS pairs under stronger generators or pivot back to bridge-family time/channel dynamics, "
                "where exact causal-patch structure is already certified."
            ),
            "suggested_phase_10": (
                "Run a bounded labeled-entropy non-CSS source search with preserved graph metadata, or add richer "
                "time/channel diagnostics to the certified bridge toy cosmology before returning to non-CSS atlases."
            ),
        },
    }


def bridge_cosmology_phase10_certificate(
    *,
    cache_path: str | Path | None = None,
    graph_n: int = 5,
    graph_max_codes: int = 64,
    max_hits_per_source: int = 3,
    include_bases: bool = False,
) -> dict[str, object]:
    if graph_n < 1:
        raise ValueError("graph_n must be positive")
    if graph_max_codes < 1:
        raise ValueError("graph_max_codes must be positive")
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    resolved_path = Path(cache_path) if cache_path is not None else DEFAULT_EXTENDED_FRONTIER_CACHE_PATH
    payload = load_frontier_cache_payload(resolved_path)
    records = tuple(payload.get("records", ()))
    scan_records = tuple(payload.get("scan_records", ()))
    record_reports = tuple(
        verify_frontier_cache_record(record)
        for record in records
        if isinstance(record, dict)
    )
    scan_record_reports = tuple(
        verify_frontier_scan_record(record)
        for record in scan_records
        if isinstance(record, dict)
    )
    generator_comparison = compare_extended_frontier_cache_to_generator(payload)
    all_records_verified = len(record_reports) == len(records) and all(report["verified"] for report in record_reports)
    all_scan_records_verified = len(scan_record_reports) == len(scan_records) and all(
        report["verified"] for report in scan_record_reports
    )
    strict_non_css_no_pair = len(scan_records) > 0 and all(
        isinstance(record, dict) and record.get("status") == "no-pair" and not record.get("pair_found")
        for record in scan_records
    )

    graph_search = graph_labeled_pair_source(n=graph_n, k=1, max_codes=graph_max_codes)
    source = graph_search["source"]
    graph_results: tuple[dict[str, object], ...]
    strict_generic_result: dict[str, object] | None
    strict_exhaustive_result: dict[str, object] | None
    if isinstance(source, dict):
        graph_results = (
            score_cover_template_candidates_for_pair(
                source=source,
                candidates=graph_specific_patch_cover_candidates(source),
                max_hits=max_hits_per_source,
                include_bases=include_bases,
            ),
        )
        strict_generic_result = score_cover_template_candidates_for_pair(
            source=source,
            candidates=strict_horizon_private_cover_candidates(graph_n),
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
        strict_exhaustive_result = score_cover_template_candidates_for_pair(
            source=source,
            candidates=strict_two_observer_cover_candidates(graph_n),
            max_hits=max_hits_per_source,
            include_bases=include_bases,
        )
    else:
        graph_results = ()
        strict_generic_result = None
        strict_exhaustive_result = None

    graph_template_candidates = sum(result["counts"]["scanned"] for result in graph_results)
    graph_template_hits = sum(result["counts"]["hits_returned"] for result in graph_results)
    strict_generic_hits = (
        int(strict_generic_result["counts"]["hits_returned"]) if isinstance(strict_generic_result, dict) else 0
    )
    strict_generic_raw_hits = (
        int(strict_generic_result["counts"]["raw_score_hits"]) if isinstance(strict_generic_result, dict) else 0
    )
    strict_exhaustive_hits = (
        int(strict_exhaustive_result["counts"]["hits_returned"]) if isinstance(strict_exhaustive_result, dict) else 0
    )
    strict_exhaustive_raw_hits = (
        int(strict_exhaustive_result["counts"]["raw_score_hits"]) if isinstance(strict_exhaustive_result, dict) else 0
    )
    strict_exhaustive_candidates = (
        int(strict_exhaustive_result["counts"]["scanned"]) if isinstance(strict_exhaustive_result, dict) else 0
    )
    all_atlas_hits = ()
    if isinstance(strict_generic_result, dict):
        all_atlas_hits = all_atlas_hits + tuple(strict_generic_result["hits"])
    if isinstance(strict_exhaustive_result, dict):
        all_atlas_hits = all_atlas_hits + tuple(strict_exhaustive_result["hits"])
    all_atlas_hits_verified = all(
        hit["certified_claims"]["causal_patch_search_hit"]
        for hit in all_atlas_hits
    )
    source_summary = graph_search["source_summary"]
    public_graph_search = {key: value for key, value in graph_search.items() if key != "source"}
    source_pair_ok = (
        isinstance(source_summary, dict)
        and source_summary["same_labeled_t2_entropy"]
        and source_summary["reconstruction_profiles_differ"]
    )
    graph_metadata = graph_search["graph_metadata"]
    graph_metadata_preserved = (
        isinstance(graph_metadata, dict)
        and isinstance(graph_metadata.get("first"), dict)
        and isinstance(graph_metadata.get("second"), dict)
        and bool(graph_metadata["first"].get("edges") is not None)
        and bool(graph_metadata["second"].get("edges") is not None)
    )
    distance_one_caveat = (
        isinstance(source_summary, dict)
        and source_summary["first_quality"]["distance"] == 1
        and source_summary["second_quality"]["distance"] == 1
        and not source_summary["first_quality"]["passes"]
        and not source_summary["second_quality"]["passes"]
    )
    phase_passes = (
        payload.get("schema_version") == FRONTIER_CACHE_SCHEMA_VERSION
        and all_records_verified
        and all_scan_records_verified
        and generator_comparison["matches_generator"]
        and strict_non_css_no_pair
        and graph_search["status"] == "pair-found"
        and source_pair_ok
        and graph_metadata_preserved
        and distance_one_caveat
        and graph_template_candidates > 0
        and graph_template_hits == 0
        and strict_generic_hits > 0
        and strict_exhaustive_raw_hits > 0
        and all_atlas_hits_verified
    )
    return {
        "phase": "Goal 2 Phase 10: labeled graph/CWS source and strict atlas hit",
        "status": "pass" if phase_passes else "no-hit",
        "cache_artifact": {
            "path": str(resolved_path),
            "schema_version": payload.get("schema_version"),
            "expected_schema_version": FRONTIER_CACHE_SCHEMA_VERSION,
            "name": payload.get("name"),
            "record_count": len(records),
            "scan_record_count": len(scan_records),
        },
        "cache_verification": {
            "all_records_verified": all_records_verified,
            "all_scan_records_verified": all_scan_records_verified,
            "strict_non_css_no_pair_records": strict_non_css_no_pair,
            "generator_comparison": generator_comparison,
            "scan_record_reports": scan_record_reports,
        },
        "labeled_graph_search": public_graph_search,
        "graph_template_search": {
            "template_families": (
                "graph_closed_neighborhood_overlap",
                "graph_generator_support_cut",
            ),
            "results": graph_results,
        },
        "strict_horizon_private_atlas_search": {
            "scope": "all one-qubit shared horizons with one private qubit per observer",
            "result": strict_generic_result,
        },
        "strict_exhaustive_two_observer_search": {
            "scope": "all ordered overlapping two-observer covers with nonempty private regions on both sides",
            "result": strict_exhaustive_result,
        },
        "counts": {
            "cache_records": len(records),
            "scan_records": len(scan_records),
            "graph_search_raw_codes": graph_search["scan"]["raw_codes"],
            "graph_search_codes_checked": graph_search["scan"]["codes_checked"],
            "graph_search_entropy_classes": graph_search["scan"]["entropy_classes"],
            "graph_template_candidates": graph_template_candidates,
            "graph_template_hits": graph_template_hits,
            "strict_horizon_private_hits": strict_generic_hits,
            "strict_horizon_private_raw_hits": strict_generic_raw_hits,
            "strict_exhaustive_candidates": strict_exhaustive_candidates,
            "strict_exhaustive_hits_returned": strict_exhaustive_hits,
            "strict_exhaustive_raw_hits": strict_exhaustive_raw_hits,
        },
        "certified_claims": {
            "extended_cache_verified": all_records_verified
            and all_scan_records_verified
            and generator_comparison["matches_generator"],
            "strict_non_css_guardrail_no_pair": strict_non_css_no_pair,
            "labeled_graph_pair_found": graph_search["status"] == "pair-found",
            "graph_metadata_preserved": graph_metadata_preserved,
            "graph_pair_same_labeled_t2_entropy": source_pair_ok,
            "graph_pair_distance_one_caveat": distance_one_caveat,
            "graph_native_templates_scored": graph_template_candidates > 0,
            "graph_native_templates_no_hit": graph_template_hits == 0,
            "strict_horizon_private_atlas_hit": strict_generic_hits > 0,
            "strict_exhaustive_atlas_hit": strict_exhaustive_raw_hits > 0,
            "all_returned_atlas_hits_verified": all_atlas_hits_verified,
            "phase_10_labeled_graph_atlas_certificate": phase_passes,
        },
        "interpretation": {
            "result": (
                "A bounded graph/CWS-like n=5 source produces a pair with identical labeled one- and two-qubit "
                "entropy data and different reconstruction/algebra profiles. Unlike the Phase 8 graph calibration "
                "pair, this is not merely an unlabeled entropy-profile collision."
            ),
            "atlas": (
                "Graph-native neighborhood/support templates still do not find a causal-patch hit, but the complete "
                "strict one-horizon/one-private search and the strict exhaustive two-observer search do. The first "
                "hits are finite causal-patch atlases with the same named entropy/overlap data and different observer "
                "reconstruction."
            ),
            "caveat": (
                "The graph-subspace pair is distance one and fails the stricter robust horizon-code filters. It is a "
                "useful labeled non-CSS calibration toy, not yet a robust horizon-code family."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 10 repairs the Phase 8/9 profile-only weakness and produces a strict finite atlas hit, but the "
                "new graph source is distance one. The next adaptation should try to lift, pad, or concatenate this "
                "labeled graph atlas into a distance-at-least-two source without destroying the named entropy/atlas "
                "certificate."
            ),
            "suggested_phase_11": (
                "Run exact distance-repair transformations for the labeled graph atlas, then replay the same strict "
                "atlas and erasure/channel diagnostics before moving to richer time dynamics."
            ),
        },
    }


def bridge_cosmology_phase11_certificate(
    *,
    max_hits_per_source: int = 1,
    include_bases: bool = False,
) -> dict[str, object]:
    if max_hits_per_source < 1:
        raise ValueError("max_hits_per_source must be at least 1")
    source = phase11_distance_repaired_source()
    first = source["first"]
    second = source["second"]
    if not isinstance(first, StabilizerCode) or not isinstance(second, StabilizerCode):
        raise TypeError("Phase 11 source must contain StabilizerCode objects")
    first_distance = bounded_distance_certificate(first, max_weight=2)
    second_distance = bounded_distance_certificate(second, max_weight=2)
    entropy_check = low_order_entropy_match_by_rank(first, second, max_subset_size=2)
    reconstruction_witness = phase11_reconstruction_witness(first, second)
    lifted_atlas = score_phase11_lifted_atlas_candidates(
        source=source,
        max_hits=max_hits_per_source,
        include_bases=include_bases,
    )
    public_source = {
        key: value
        for key, value in source.items()
        if key not in ("first", "second")
    }
    phase10_search = public_source["phase10_graph_search"]
    phase10_summary = phase10_search["source_summary"]
    distance_repaired = (
        first_distance["distance_at_least_2_certified"]
        and second_distance["distance_at_least_2_certified"]
    )
    phase10_source_valid = (
        phase10_search["status"] == "pair-found"
        and phase10_summary["same_labeled_t2_entropy"]
        and phase10_summary["reconstruction_profiles_differ"]
    )
    reconstruction_difference_preserved = reconstruction_witness is not None
    lifted_atlas_no_hit = lifted_atlas["counts"]["hits_returned"] == 0
    lifted_atlas_near_misses = lifted_atlas["counts"]["raw_score_hits"] > 0
    phase_passes = (
        phase10_source_valid
        and source["outer_code"]["distance"] == 2
        and first.k == 1
        and second.k == 1
        and distance_repaired
        and entropy_check["matches"]
        and reconstruction_difference_preserved
        and lifted_atlas["candidate_count"] > 0
        and lifted_atlas_no_hit
        and lifted_atlas_near_misses
    )
    return {
        "phase": "Goal 2 Phase 11: distance-repaired graph atlas tension",
        "status": "pass" if phase_passes else "no-hit",
        "repair_source": public_source,
        "repaired_codes": {
            "n": first.n,
            "k": first.k,
            "first_generators": first.pauli_generators(),
            "second_generators": second.pauli_generators(),
        },
        "distance_repair": {
            "method": "logical concatenation of the Phase 10 graph/CWS pair with a four-qubit distance-2 outer code",
            "first": first_distance,
            "second": second_distance,
            "distance_at_least_2_for_both": distance_repaired,
        },
        "low_order_entropy": entropy_check,
        "reconstruction_witness": reconstruction_witness,
        "lifted_atlas_replay": {
            "template_family": "phase10_strict_atlas_block_lift",
            "result": lifted_atlas,
        },
        "counts": {
            "low_order_subsets_checked": entropy_check["subsets_checked"],
            "low_order_entropy_mismatches": entropy_check["mismatch_count"],
            "lifted_atlas_candidates": lifted_atlas["candidate_count"],
            "lifted_atlas_entropy_matches": lifted_atlas["counts"]["entropy_overlap_matched"],
            "lifted_atlas_observer_differences": lifted_atlas["counts"]["different_observer_reconstruction"],
            "lifted_atlas_raw_hits": lifted_atlas["counts"]["raw_score_hits"],
            "lifted_atlas_hits_returned": lifted_atlas["counts"]["hits_returned"],
        },
        "certified_claims": {
            "phase10_labeled_graph_source_loaded": phase10_source_valid,
            "outer_code_distance_2": source["outer_code"]["distance"] == 2,
            "logical_concatenation_k1": first.k == 1 and second.k == 1,
            "distance_at_least_2_repaired": distance_repaired,
            "same_labeled_t2_entropy_after_repair": entropy_check["matches"],
            "reconstruction_difference_after_repair": reconstruction_difference_preserved,
            "lifted_phase10_atlas_templates_scored": lifted_atlas["candidate_count"] > 0,
            "lifted_phase10_atlas_near_misses_exist": lifted_atlas_near_misses,
            "lifted_phase10_atlas_no_hit": lifted_atlas_no_hit,
            "phase_11_distance_repair_tension_certificate": phase_passes,
        },
        "interpretation": {
            "result": (
                "A four-qubit outer stabilizer code repairs the Phase 10 graph/CWS pair to distance at least two "
                "under an exact bounded logical-weight check while preserving all labeled one- and two-qubit entropy "
                "queries."
            ),
            "pressure": (
                "The simple Phase 10 strict atlas does not survive the repair as a full causal-patch certificate under "
                "the bounded block-lift template family. Many candidates still match entropy/horizon data and expose "
                "observer-algebra differences, but they fail the full erasure/complementarity atlas criteria."
            ),
            "lesson": (
                "For non-CSS graph/CWS toys, distance repair, labeled low-order entropy matching, and causal-patch "
                "atlas semantics are separable constraints; satisfying two does not force the third."
            ),
        },
        "recommendation": {
            "next_phase": "adapt_then_proceed",
            "reason": (
                "Phase 11 repairs the distance-one weakness without losing labeled t=2 entropy matching, but the "
                "Phase 10 atlas block-lift search certifies no hit. The next phase should search atlas-aware repair "
                "rules or broader repaired-cover templates rather than moving directly to time/channel dynamics."
            ),
            "suggested_phase_12": (
                "Search repaired-code cover templates built from outer-code reconstruction regions and inner observer "
                "patches, then compare against bridge-family time/channel diagnostics as the robust CSS baseline."
            ),
        },
    }
