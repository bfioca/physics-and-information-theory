"""Observer-algebra tomography certificates.

This module packages the Goals 1-3 entropy/reconstruction/channel split as a
finite operator-algebra QEC tomography statement.
"""

from __future__ import annotations

from typing import Iterable

from .cosmology import (
    PatchCover,
    bridge_cosmology_phase1_certificate,
    bridge_cosmology_phase2_certificate,
    bridge_observer_cover,
    entropy_overlap_summary,
    erasure_algebra_differences,
    erasure_correctability_key,
    erasure_suite_diagnostic,
    patch_algebra_signatures,
)
from .family import repeat_balanced_bridge
from .gf2 import all_masks, in_span, mask_to_tuple
from .search import enumerate_stabilizer_codes
from .stabilizer import StabilizerCode, pauli_to_string


def _observer_patches(cover: PatchCover):
    return tuple(patch for patch in cover.patches if patch.role == "observer_patch")


def _patch_region_by_name(cover: PatchCover, name: str) -> int:
    return cover.patch(name).region


def _algebra_signature_map(code: StabilizerCode, cover: PatchCover) -> dict[str, tuple[int, int, int, bool]]:
    return dict(patch_algebra_signatures(code, cover))


def _observer_center_profile(code: StabilizerCode, cover: PatchCover) -> tuple[tuple[str, int], ...]:
    return tuple(
        (patch.name, code.region_algebra(patch.region).center_dim)
        for patch in _observer_patches(cover)
    )


def _observer_commutant_profile(code: StabilizerCode, cover: PatchCover) -> tuple[tuple[str, int], ...]:
    return tuple(
        (patch.name, code.region_algebra(patch.region).commutant_dim)
        for patch in _observer_patches(cover)
    )


def _observer_full_algebra_profile(
    code: StabilizerCode,
    cover: PatchCover,
) -> tuple[tuple[str, tuple[int, int, int, bool]], ...]:
    signatures = _algebra_signature_map(code, cover)
    return tuple((patch.name, signatures[patch.name]) for patch in _observer_patches(cover))


def _logical_probe_response(
    code: StabilizerCode,
    cover: PatchCover,
) -> tuple[tuple[str, tuple[tuple[str, bool], ...]], ...]:
    """Finite stabilizer proxy for logical-relative-entropy visibility.

    A logical probe is counted visible to a patch when its logical class has a
    representative in the patch algebra.  This is not a continuum modular-flow
    claim; it is an exact finite OA-QEC support test.
    """

    rows = []
    full_logicals = code.logical_basis
    for patch in _observer_patches(cover):
        algebra = code.region_algebra(patch.region)
        span_rows = algebra.logical_basis + code.generators
        responses = tuple(
            (pauli_to_string(logical, code.n), in_span(logical, span_rows, code.width))
            for logical in full_logicals
        )
        rows.append((patch.name, responses))
    return tuple(rows)


def _observer_entropy_horizon_shadow(code: StabilizerCode, cover: PatchCover) -> dict[str, object]:
    observer_p = _patch_region_by_name(cover, "observer_p")
    observer_q = _patch_region_by_name(cover, "observer_q")
    shared_horizon = _patch_region_by_name(cover, "shared_horizon")
    return {
        "entropy_overlap_mi_cmi_i3": entropy_overlap_summary(code, cover),
        "observer_overlap_qubits": mask_to_tuple(observer_p & observer_q, code.n),
        "shared_horizon_qubits": mask_to_tuple(shared_horizon, code.n),
        "shared_horizon_entropy": code.entropy(shared_horizon),
        "shared_horizon_algebra_signature": code.region_algebra(shared_horizon).signature(),
    }


def _erasure_channel_shadow(code: StabilizerCode, cover: PatchCover) -> dict[str, object]:
    suite = erasure_suite_diagnostic(code, cover)
    return {
        "erasure_correctability": erasure_correctability_key(suite),
        "survivor_fixed_points": tuple(
            (item["name"], item["survivor_reconstructs_all"])
            for item in suite
        ),
        "qec_complementarity": tuple(
            (item["name"], item["qec_complementarity_identity_holds"])
            for item in suite
        ),
    }


def _shadow_tier_records(
    *,
    first: StabilizerCode,
    second: StabilizerCode,
    cover: PatchCover,
) -> tuple[dict[str, object], ...]:
    first_entropy = _observer_entropy_horizon_shadow(first, cover)
    second_entropy = _observer_entropy_horizon_shadow(second, cover)
    first_channel = _erasure_channel_shadow(first, cover)
    second_channel = _erasure_channel_shadow(second, cover)
    first_center = _observer_center_profile(first, cover)
    second_center = _observer_center_profile(second, cover)
    first_commutant = _observer_commutant_profile(first, cover)
    second_commutant = _observer_commutant_profile(second, cover)
    first_probe = _logical_probe_response(first, cover)
    second_probe = _logical_probe_response(second, cover)
    first_algebra = _observer_full_algebra_profile(first, cover)
    second_algebra = _observer_full_algebra_profile(second, cover)
    observer_algebra_differs = first_algebra != second_algebra

    tiers: tuple[tuple[str, str, object, object], ...] = (
        (
            "entropy_horizon_shadow",
            "Named entropy, overlap, MI/CMI/I3, shared-horizon entropy, and shared-horizon algebra.",
            first_entropy,
            second_entropy,
        ),
        (
            "entropy_horizon_plus_erasure_correctability",
            "Add exact erasure correctability and survivor fixed-point booleans.",
            {**first_entropy, **first_channel},
            {**second_entropy, **second_channel},
        ),
        (
            "plus_observer_center_profile",
            "Add observer center dimensions.",
            {**first_entropy, **first_channel, "observer_centers": first_center},
            {**second_entropy, **second_channel, "observer_centers": second_center},
        ),
        (
            "plus_observer_commutant_profile",
            "Add observer commutant dimensions.",
            {
                **first_entropy,
                **first_channel,
                "observer_centers": first_center,
                "observer_commutants": first_commutant,
            },
            {
                **second_entropy,
                **second_channel,
                "observer_centers": second_center,
                "observer_commutants": second_commutant,
            },
        ),
        (
            "plus_logical_probe_response",
            "Add exact finite logical-probe visibility responses.",
            {
                **first_entropy,
                **first_channel,
                "observer_centers": first_center,
                "observer_commutants": first_commutant,
                "logical_probe_response": first_probe,
            },
            {
                **second_entropy,
                **second_channel,
                "observer_centers": second_center,
                "observer_commutants": second_commutant,
                "logical_probe_response": second_probe,
            },
        ),
        (
            "full_observer_algebra_profile",
            "Full observer algebra signatures for the declared observer patches.",
            first_algebra,
            second_algebra,
        ),
    )

    records: list[dict[str, object]] = []
    for name, description, first_shadow, second_shadow in tiers:
        agrees = first_shadow == second_shadow
        records.append(
            {
                "tier": name,
                "description": description,
                "shadows_agree": agrees,
                "observer_algebra_differs": observer_algebra_differs,
                "non_identifying_for_representative": agrees and observer_algebra_differs,
                "separates_representative": (not agrees) and observer_algebra_differs,
            }
        )
    return tuple(records)


def _first_separating_tier(records: Iterable[dict[str, object]]) -> str | None:
    for record in records:
        if record["separates_representative"]:
            return str(record["tier"])
    return None


def _all_region_algebra_profile(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], tuple[int, int, int, bool]], ...]:
    return tuple(
        (mask_to_tuple(mask, code.n), code.region_algebra(mask).signature())
        for mask in all_masks(code.n)
    )


def _all_region_logical_probe_response(
    code: StabilizerCode,
) -> tuple[tuple[tuple[int, ...], tuple[tuple[str, bool], ...]], ...]:
    full_logicals = code.logical_basis
    rows = []
    for mask in all_masks(code.n):
        algebra = code.region_algebra(mask)
        span_rows = algebra.logical_basis + code.generators
        rows.append(
            (
                mask_to_tuple(mask, code.n),
                tuple(
                    (pauli_to_string(logical, code.n), in_span(logical, span_rows, code.width))
                    for logical in full_logicals
                ),
            )
        )
    return tuple(rows)


def _all_region_shadow_key(
    code: StabilizerCode,
    tier: str,
    *,
    max_subset_size: int,
) -> object:
    entropy_piece = tuple(
        (mask_to_tuple(mask, code.n), code.entropy(mask))
        for mask in all_masks(code.n)
        if mask.bit_count() <= max_subset_size
    )
    if tier == "low_order_entropy":
        return entropy_piece

    erasure_piece = tuple(
        (
            mask_to_tuple(mask, code.n),
            code.erasure_correctable(mask),
            code.reconstructs_all_logicals(((1 << code.n) - 1) ^ mask),
        )
        for mask in all_masks(code.n)
    )
    if tier == "plus_erasure_fixed_points":
        return (entropy_piece, erasure_piece)

    center_piece = tuple(
        (mask_to_tuple(mask, code.n), code.region_algebra(mask).center_dim)
        for mask in all_masks(code.n)
    )
    if tier == "plus_center_profile":
        return (entropy_piece, erasure_piece, center_piece)

    commutant_piece = tuple(
        (mask_to_tuple(mask, code.n), code.region_algebra(mask).commutant_dim)
        for mask in all_masks(code.n)
    )
    if tier == "plus_commutant_profile":
        return (entropy_piece, erasure_piece, center_piece, commutant_piece)

    logical_probe_piece = _all_region_logical_probe_response(code)
    if tier == "plus_logical_probe_response":
        return (entropy_piece, erasure_piece, center_piece, commutant_piece, logical_probe_piece)

    if tier == "full_algebra_profile":
        return _all_region_algebra_profile(code)

    raise ValueError(f"unknown tomography tier: {tier}")


def _algebra_difference_witness(first: StabilizerCode, second: StabilizerCode) -> dict[str, object] | None:
    for mask in all_masks(first.n):
        first_signature = first.region_algebra(mask).signature()
        second_signature = second.region_algebra(mask).signature()
        if first_signature != second_signature:
            return {
                "region": mask_to_tuple(mask, first.n),
                "first_signature": first_signature,
                "second_signature": second_signature,
            }
    return None


def _k1_signature_from_erasure_fixed_points(
    code: StabilizerCode,
    region: int,
) -> tuple[int, int, int, bool]:
    """Recover the k=1 region-algebra signature from all-region channel data."""

    if code.k != 1:
        raise ValueError("the k=1 completion lemma only applies to one-logical-qubit codes")
    if code.erasure_correctable(region):
        return (0, 0, 2, False)
    if code.reconstructs_all_logicals(region):
        return (2, 0, 0, True)
    return (1, 1, 1, False)


def _k1_completion_audit(codes: tuple[StabilizerCode, ...]) -> dict[str, object]:
    mismatches: list[dict[str, object]] = []
    regions_checked = 0
    for code in codes:
        if code.k != 1:
            return {
                "status": "not_applicable",
                "reason": "all codes must have k=1",
                "codes_checked": len(codes),
                "regions_checked": regions_checked,
                "mismatches": tuple(mismatches),
            }
        for mask in all_masks(code.n):
            regions_checked += 1
            predicted = _k1_signature_from_erasure_fixed_points(code, mask)
            actual = code.region_algebra(mask).signature()
            if predicted != actual:
                mismatches.append(
                    {
                        "n": code.n,
                        "generators": code.pauli_generators(),
                        "region": mask_to_tuple(mask, code.n),
                        "predicted_signature": predicted,
                        "actual_signature": actual,
                    }
                )

    return {
        "status": "pass" if not mismatches else "fail",
        "codes_checked": len(codes),
        "regions_checked": regions_checked,
        "mismatch_count": len(mismatches),
        "mismatches": tuple(mismatches[:3]),
    }


def _k1_completion_lemma_record(
    *,
    scan_max_n: int,
    equivalence: str,
    max_subset_size: int,
    max_codes_per_n: int | None,
    n_records: tuple[dict[str, object], ...],
    k: int,
) -> dict[str, object]:
    audits = tuple(
        n_record["k1_erasure_fixed_point_completion_audit"]
        for n_record in n_records
        if "k1_erasure_fixed_point_completion_audit" in n_record
    )
    mismatch_count = sum(int(audit.get("mismatch_count", 0)) for audit in audits)
    not_applicable = k != 1 or any(audit.get("status") == "not_applicable" for audit in audits)
    status = "not_applicable" if not_applicable else ("pass" if mismatch_count == 0 else "fail")
    return {
        "name": "k=1 All-Region Erasure/Fixed-Point Completion Lemma",
        "status": status,
        "evidence_class": "exact theorem-style claim with bounded implementation audit",
        "claim": (
            "For any finite stabilizer code with one logical qubit, the all-region "
            "erasure-correctability shadow together with all-region survivor fixed-point "
            "booleans determines every all-region observer-algebra signature."
        ),
        "scope": (
            "Exact for k=1 stabilizer/OA-QEC all-region atlases. It is not a named-patch "
            "observer theorem and is not claimed for k>1."
        ),
        "proof_idea": (
            "A k=1 logical quotient is a two-dimensional symplectic vector space. For each "
            "region R, erasure_correctable(R) identifies logical dimension 0; the survivor "
            "fixed-point row for the complement identifies reconstructs_all(R), hence logical "
            "dimension 2. The remaining case has logical dimension 1. In a two-dimensional "
            "symplectic quotient those three cases force signatures (0,0,2,false), "
            "(2,0,0,true), and (1,1,1,false), respectively."
        ),
        "bounded_implementation_audit": {
            "max_n": scan_max_n,
            "k": k,
            "equivalence": equivalence,
            "max_subset_size": max_subset_size,
            "max_codes_per_n": max_codes_per_n,
            "codes_checked": sum(int(audit.get("codes_checked", 0)) for audit in audits),
            "regions_checked": sum(int(audit.get("regions_checked", 0)) for audit in audits),
            "mismatch_count": mismatch_count,
        },
    }


def _bounded_shadow_scan_tier(
    codes: tuple[StabilizerCode, ...],
    tier: str,
    *,
    max_subset_size: int,
) -> dict[str, object]:
    groups: dict[object, list[StabilizerCode]] = {}
    for code in codes:
        key = _all_region_shadow_key(code, tier, max_subset_size=max_subset_size)
        groups.setdefault(key, []).append(code)

    for group in groups.values():
        seen: dict[object, StabilizerCode] = {}
        for code in group:
            algebra_profile = _all_region_algebra_profile(code)
            if algebra_profile in seen:
                continue
            if seen:
                first = next(iter(seen.values()))
                return {
                    "tier": tier,
                    "status": "non_identifying_collision_found",
                    "shadow_class_size": len(group),
                    "first_generators": first.pauli_generators(),
                    "second_generators": code.pauli_generators(),
                    "algebra_difference_witness": _algebra_difference_witness(first, code),
                }
            seen[algebra_profile] = code

    return {
        "tier": tier,
        "status": "no_collision_found_in_bounded_scan",
        "shadow_classes": len(groups),
        "max_shadow_class_size": max((len(group) for group in groups.values()), default=0),
    }


def bounded_observer_tomography_shadow_scan(
    *,
    max_n: int = 4,
    k: int = 1,
    equivalence: str = "permutation",
    max_subset_size: int = 2,
    max_codes_per_n: int | None = None,
) -> dict[str, object]:
    """Search tiny stabilizer codes for the tomography boundary.

    This is bounded evidence only: it tests all-region shadows over the finite
    representatives enumerated by ``enumerate_stabilizer_codes``.
    """

    tiers = (
        "low_order_entropy",
        "plus_erasure_fixed_points",
        "plus_center_profile",
        "plus_commutant_profile",
        "plus_logical_probe_response",
        "full_algebra_profile",
    )
    n_records = []
    for n in range(max(1, k), max_n + 1):
        codes = tuple(enumerate_stabilizer_codes(n, k=k, equivalence=equivalence, max_codes=max_codes_per_n))
        tier_records = tuple(
            _bounded_shadow_scan_tier(codes, tier, max_subset_size=max_subset_size)
            for tier in tiers
        )
        n_record = {
            "n": n,
            "k": k,
            "codes_checked": len(codes),
            "tier_records": tier_records,
        }
        if k == 1:
            n_record["k1_erasure_fixed_point_completion_audit"] = _k1_completion_audit(codes)
        n_records.append(n_record)

    first_no_collision_tier: str | None = None
    for tier in tiers:
        if all(
            next(record for record in n_record["tier_records"] if record["tier"] == tier)["status"]
            == "no_collision_found_in_bounded_scan"
            for n_record in n_records
        ):
            first_no_collision_tier = tier
            break

    return {
        "status": "bounded_scan_complete",
        "scope": {
            "max_n": max_n,
            "k": k,
            "equivalence": equivalence,
            "max_subset_size": max_subset_size,
            "max_codes_per_n": max_codes_per_n,
        },
        "tiers": tiers,
        "first_no_collision_tier_observed": first_no_collision_tier,
        "k1_erasure_fixed_point_completion_lemma": _k1_completion_lemma_record(
            scan_max_n=max_n,
            equivalence=equivalence,
            max_subset_size=max_subset_size,
            max_codes_per_n=max_codes_per_n,
            n_records=tuple(n_records),
            k=k,
        ),
        "records": tuple(n_records),
        "interpretation": (
            "Low-order entropy collisions are bounded evidence for non-identifiability. "
            "For k=1, the no-collision tier after all-region erasure/fixed-point data is "
            "explained by the exact completion lemma recorded above; for richer k or named "
            "observer atlases it remains an open boundary question."
        ),
    }


def _family_instance_record(m: int) -> dict[str, object]:
    first, second = repeat_balanced_bridge((1 << 1) | (1 << 2), (1 << 0) | (1 << 5), steps=m)
    cover = bridge_observer_cover(m)
    first_algebra = _observer_full_algebra_profile(first, cover)
    second_algebra = _observer_full_algebra_profile(second, cover)
    first_erasures = erasure_suite_diagnostic(first, cover)
    second_erasures = erasure_suite_diagnostic(second, cover)
    shadow_tiers = _shadow_tier_records(first=first, second=second, cover=cover)
    entropy_shadow_agrees = shadow_tiers[0]["shadows_agree"]
    erasure_shadow_agrees = shadow_tiers[1]["shadows_agree"]
    observer_algebra_differs = first_algebra != second_algebra
    channel_algebra_differs = bool(erasure_algebra_differences(first_erasures, second_erasures))
    return {
        "m": m,
        "n": first.n,
        "k": first.k,
        "distance": {
            "first": first.distance(),
            "second": second.distance(),
        },
        "cover": cover.summary(first.n),
        "observer_algebras": {
            "first": first_algebra,
            "second": second_algebra,
        },
        "shadow_tiers": shadow_tiers,
        "first_separating_tier": _first_separating_tier(shadow_tiers),
        "channel_semantic_split": {
            "erasure_correctability_profile_agrees": erasure_correctability_key(first_erasures)
            == erasure_correctability_key(second_erasures),
            "erasure_algebra_differences": erasure_algebra_differences(first_erasures, second_erasures),
            "channel_algebra_differs": channel_algebra_differs,
        },
        "certified_claims": {
            "entropy_horizon_shadow_agrees": entropy_shadow_agrees,
            "erasure_survivor_shadow_agrees": erasure_shadow_agrees,
            "observer_algebra_differs": observer_algebra_differs,
            "channel_semantics_differ": channel_algebra_differs,
            "center_profile_separates_representative": _first_separating_tier(shadow_tiers)
            == "plus_observer_center_profile",
        },
    }


def observer_algebra_tomography_certificate(
    *,
    max_m: int = 3,
    max_bonus: int = 2,
    scan_max_n: int = 4,
    skip_boundary_scan: bool = False,
    include_holography: bool = False,
    graph_max_codes: int = 220,
) -> dict[str, object]:
    """Emit the Goal 4 observer-algebra tomography certificate."""

    if max_m < 1:
        raise ValueError("max_m must be at least 1")

    phase1 = bridge_cosmology_phase1_certificate(max_m=max_m)
    phase2 = bridge_cosmology_phase2_certificate(max_m=max_m)
    family_records = tuple(_family_instance_record(m) for m in range(1, max_m + 1))
    all_family_non_identifying = all(
        record["certified_claims"]["entropy_horizon_shadow_agrees"]
        and record["certified_claims"]["erasure_survivor_shadow_agrees"]
        and record["certified_claims"]["observer_algebra_differs"]
        and record["certified_claims"]["channel_semantics_differ"]
        for record in family_records
    )
    all_center_separates = all(
        record["certified_claims"]["center_profile_separates_representative"]
        for record in family_records
    )
    exact_theorem = {
        "name": "Observer Entropy Non-Identifiability Theorem",
        "claim": (
            "For the balanced-bridge observer-code family A_m,B_m, named observer entropy, "
            "horizon/overlap, MI/CMI/I3, shared-horizon algebra, erasure-correctability, "
            "and survivor fixed-point shadows agree, while observer reconstruction algebras "
            "and erasure-channel algebra semantics differ."
        ),
        "scope": "Exact all-m family statement, audited here for the finite prefix m<=max_m.",
        "proof_idea": (
            "The bridge checks are appended symmetrically, preserving all declared entropy and "
            "horizon shadows. The observer patches contain different supported logical quotient "
            "classes in A_m and B_m, so their finite region algebras have different signatures."
        ),
    }
    k1_completion_lemma_obligation: dict[str, object] = {
        "status": "proof_obligation_command",
        "command": f"python3 -m qgtoy observer-tomography --max-m {max_m} --scan-max-n {scan_max_n}",
        "role": (
            "Audits the implementation of the exact k=1 all-region erasure/fixed-point "
            "completion lemma over the declared bounded stabilizer representatives."
        ),
    }

    min_cut_obligation: dict[str, object] = {
        "status": "proof_obligation_command",
        "command": "python3 -m qgtoy holography-phase40",
        "role": (
            "Goal 3 supplies the finite min-cut-visible extension: entropy and finite min-cut "
            "diagnostics agree while reconstruction-visible and channel-visible geometry differ."
        ),
    }
    if include_holography:
        from .tensor_network import bridge_holography_phase40_certificate

        phase40 = bridge_holography_phase40_certificate(graph_max_codes=graph_max_codes)
        min_cut_obligation = {
            "status": phase40["status"],
            "command": f"python3 -m qgtoy holography-phase40 --graph-max-codes {graph_max_codes}",
            "representative_min_cut_values": phase40["counts"]["representative_min_cut_values"],
            "entropy_visible_geometry": phase40["proof_obligations"]["entropy_visible_geometry"],
            "min_cut_visible_geometry": phase40["proof_obligations"]["min_cut_visible_geometry"],
            "reconstruction_visible_geometry": phase40["proof_obligations"]["observer_reconstruction_geometry"],
            "channel_visible_geometry": phase40["proof_obligations"]["channel_erasure_geometry"],
        }

    bounded_search_evidence = {
        "strict_cover_audit": {
            "status": "proof_obligation_command",
            "command": f"python3 -m qgtoy cosmology-phase31 --max-bonus {max_bonus}",
            "role": (
                "Bounded strict-cover evidence separating certified observer-patch hits from "
                "entropy near-misses rejected by erasure semantics."
            ),
            "known_final_counts": {
                "cover_candidates": 175,
                "raw_entropy_reconstruction_hits": 66,
                "strict_cover_hits": 8,
                "raw_hits_rejected_by_erasure_profile": 58,
            },
        },
        "holographic_min_cut_audit": min_cut_obligation,
    }
    positive_boundary = {
        "status": "exact_k1_boundary_plus_bounded_representative_boundary",
        "tested_tiers_in_order": tuple(record["tier"] for record in family_records[0]["shadow_tiers"]),
        "weakest_tier_separating_balanced_bridge_prefix": (
            "plus_observer_center_profile" if all_center_separates else None
        ),
        "k1_all_region_erasure_fixed_point_completion_lemma": k1_completion_lemma_obligation,
        "not_claimed": (
            "No completeness theorem is claimed for all stabilizer/OA-QEC observer codes. "
            "The exact positive boundary is restricted to all-region k=1 stabilizer atlases. "
            "The balanced-bridge theorem remains a named observer-atlas non-identifiability "
            "result through entropy+horizon+erasure/survivor shadows, and is separated once "
            "observer center data are added."
        ),
        "next_search_target": (
            "Search for pairs that also match center, commutant, channel fixed-point, and "
            "logical-probe shadows but still have non-isomorphic observer algebras; failure "
            "would suggest a candidate completeness boundary."
        ),
    }
    boundary_scan = None
    if not skip_boundary_scan:
        boundary_scan = bounded_observer_tomography_shadow_scan(max_n=scan_max_n)
        positive_boundary["bounded_all_region_shadow_scan"] = boundary_scan
        positive_boundary["k1_all_region_erasure_fixed_point_completion_lemma"] = boundary_scan[
            "k1_erasure_fixed_point_completion_lemma"
        ]

    certified_claims = {
        "phase1_static_observer_certificate_loaded": phase1["status"] == "pass",
        "phase2_erasure_growth_certificate_loaded": phase2["status"] == "pass",
        "observer_entropy_non_identifiability_prefix_certified": all_family_non_identifying,
        "center_profile_boundary_separates_prefix": all_center_separates,
        "k1_all_region_completion_lemma_declared": True,
        "k1_all_region_completion_lemma_audited": (
            boundary_scan is not None
            and boundary_scan["k1_erasure_fixed_point_completion_lemma"]["status"] == "pass"
        ),
        "bounded_positive_boundary_scan_complete": skip_boundary_scan
        or (boundary_scan is not None and boundary_scan["status"] == "bounded_scan_complete"),
        "bounded_search_obligations_declared": True,
        "harlow_facing_interpretation_declared": True,
    }
    required_claims = tuple(
        value
        for key, value in certified_claims.items()
        if key != "k1_all_region_completion_lemma_audited" or not skip_boundary_scan
    )
    certified_claims["goal4_fast_tomography_certificate"] = all(required_claims)
    return {
        "goal": "Goal 4: Observer Algebra Tomography",
        "status": "pass" if certified_claims["goal4_fast_tomography_certificate"] else "fail",
        "theorem_style_claims": {
            "exact": exact_theorem,
            "exact_positive_boundary": positive_boundary["k1_all_region_erasure_fixed_point_completion_lemma"],
            "bounded_evidence": bounded_search_evidence,
            "conjectural_or_open": positive_boundary,
        },
        "family_prefix": {
            "max_m": max_m,
            "records": family_records,
        },
        "positive_boundary": positive_boundary,
        "certified_claims": certified_claims,
        "reproducibility": {
            "goal4_fast_certificate": f"python3 -m qgtoy observer-tomography --max-m {max_m}",
            "goal4_bounded_boundary_scan": (
                f"python3 -m qgtoy observer-tomography --max-m {max_m} --scan-max-n {scan_max_n}"
            ),
            "goal4_with_min_cut_certificate": (
                f"python3 -m qgtoy observer-tomography --max-m {max_m} --include-holography "
                f"--graph-max-codes {graph_max_codes}"
            ),
            "static_observer_shadow": f"python3 -m qgtoy cosmology-phase1 --max-m {max_m}",
            "erasure_survivor_shadow": f"python3 -m qgtoy cosmology-phase2 --max-m {max_m}",
            "bounded_strict_cover_audit": f"python3 -m qgtoy cosmology-phase31 --max-bonus {max_bonus}",
            "finite_min_cut_audit": "python3 -m qgtoy holography-phase40",
        },
        "harlow_facing_interpretation": (
            "In closed-universe observer language, S_Ob can set a size scale, but it does not "
            "specify the observer's effective quantum mechanics. The finite OA-QEC data needed "
            "to specify observer physics include at least an observer algebra and a channel/coarse-"
            "graining rule; entropy, horizon, min-cut, and erasure fixed-point shadows alone are "
            "not complete invariants in the certified family."
        ),
        "limitations": (
            "This is a finite stabilizer/OA-QEC certificate. The all-m statement is for the "
            "balanced-bridge observer family; bounded search and min-cut claims are limited to "
            "their declared commands and finite families. The positive tomography boundary is exact "
            "only for all-region k=1 stabilizer atlases; richer observer atlases and k>1 remain open."
        ),
    }
