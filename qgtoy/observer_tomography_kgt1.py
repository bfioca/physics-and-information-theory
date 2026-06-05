"""Goal 5 k>1 observer-algebra tomography certificates."""

from __future__ import annotations

from itertools import combinations

from .gf2 import all_masks, mask_to_tuple, masks_of_size
from .search import enumerate_stabilizer_codes
from .stabilizer import StabilizerCode, pauli_to_string, symplectic_product


def _minimal_channel_counterexample_pair() -> tuple[StabilizerCode, StabilizerCode]:
    return (
        StabilizerCode.from_pauli_strings(("XXI",)),
        StabilizerCode.from_pauli_strings(("XXX",)),
    )


def _center_counterexample_pair() -> tuple[StabilizerCode, StabilizerCode]:
    return (
        StabilizerCode.from_pauli_strings(("XIIX", "XXXI")),
        StabilizerCode.from_pauli_strings(("IZXI", "ZIXX")),
    )


def _five_qubit_perfect_code() -> StabilizerCode:
    return StabilizerCode.from_pauli_strings(("XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"))


def _all_region_channel_shadow(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], bool, bool], ...]:
    full = (1 << code.n) - 1
    return tuple(
        (
            mask_to_tuple(mask, code.n),
            code.erasure_correctable(mask),
            code.reconstructs_all_logicals(full ^ mask),
        )
        for mask in all_masks(code.n)
    )


def _all_region_center_shadow(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], int], ...]:
    return tuple((mask_to_tuple(mask, code.n), code.region_algebra(mask).center_dim) for mask in all_masks(code.n))


def _all_region_commutant_shadow(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], int], ...]:
    return tuple((mask_to_tuple(mask, code.n), code.region_algebra(mask).commutant_dim) for mask in all_masks(code.n))


def _all_region_algebra_profile(
    code: StabilizerCode,
) -> tuple[tuple[tuple[int, ...], tuple[int, int, int, bool]], ...]:
    return tuple((mask_to_tuple(mask, code.n), code.region_algebra(mask).signature()) for mask in all_masks(code.n))


def _tier_key(code: StabilizerCode, tier: str) -> object:
    channel = _all_region_channel_shadow(code)
    if tier == "channel":
        return channel
    center = _all_region_center_shadow(code)
    if tier == "channel_plus_center":
        return (channel, center)
    commutant = _all_region_commutant_shadow(code)
    if tier == "channel_plus_center_commutant":
        return (channel, center, commutant)
    if tier == "full_signature":
        return _all_region_algebra_profile(code)
    raise ValueError(f"unknown Goal 5 tomography tier: {tier}")


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


def _scan_tier(codes: tuple[StabilizerCode, ...], tier: str) -> dict[str, object]:
    groups: dict[object, list[StabilizerCode]] = {}
    for code in codes:
        groups.setdefault(_tier_key(code, tier), []).append(code)

    for group in groups.values():
        seen: dict[object, StabilizerCode] = {}
        for code in group:
            algebra = _all_region_algebra_profile(code)
            if algebra in seen:
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
            seen[algebra] = code

    return {
        "tier": tier,
        "status": "no_collision_found_in_bounded_scan",
        "shadow_classes": len(groups),
        "max_shadow_class_size": max((len(group) for group in groups.values()), default=0),
    }


def bounded_kgt1_hierarchy_scan(
    *,
    max_n: int = 4,
    k: int = 2,
    equivalence: str = "permutation",
    max_codes_per_n: int | None = None,
) -> dict[str, object]:
    tiers = (
        "channel",
        "channel_plus_center",
        "channel_plus_center_commutant",
        "full_signature",
    )
    records = []
    for n in range(max(1, k), max_n + 1):
        codes = tuple(enumerate_stabilizer_codes(n, k=k, equivalence=equivalence, max_codes=max_codes_per_n))
        records.append(
            {
                "n": n,
                "k": k,
                "codes_checked": len(codes),
                "tier_records": tuple(_scan_tier(codes, tier) for tier in tiers),
            }
        )

    first_no_collision_tier: str | None = None
    for tier in tiers:
        if all(
            next(record for record in n_record["tier_records"] if record["tier"] == tier)["status"]
            == "no_collision_found_in_bounded_scan"
            for n_record in records
        ):
            first_no_collision_tier = tier
            break

    return {
        "status": "bounded_scan_complete",
        "scope": {
            "max_n": max_n,
            "k": k,
            "equivalence": equivalence,
            "max_codes_per_n": max_codes_per_n,
        },
        "tiers": tiers,
        "first_no_collision_tier_observed": first_no_collision_tier,
        "records": tuple(records),
    }


def _tier_has_no_collisions(scan: dict[str, object], tier: str) -> bool:
    return all(
        next(record for record in n_record["tier_records"] if record["tier"] == tier)["status"]
        == "no_collision_found_in_bounded_scan"
        for n_record in scan["records"]
    )


def _access_counts(code: StabilizerCode) -> tuple[dict[str, object], ...]:
    rows = []
    for size in range(code.n + 1):
        zero = 0
        full = 0
        intermediate = 0
        for mask in masks_of_size(code.n, size):
            if code.erasure_correctable(mask):
                zero += 1
            elif code.reconstructs_all_logicals(mask):
                full += 1
            else:
                intermediate += 1
        rows.append({"size": size, "zero": zero, "intermediate": intermediate, "full": full})
    return tuple(rows)


def _witness_record(first: StabilizerCode, second: StabilizerCode, *, matched_tier: str) -> dict[str, object]:
    return {
        "first_generators": first.pauli_generators(),
        "second_generators": second.pauli_generators(),
        "parameters": {
            "first": {"n": first.n, "k": first.k, "distance": first.distance()},
            "second": {"n": second.n, "k": second.k, "distance": second.distance()},
        },
        "matched_tier": matched_tier,
        "channel_shadow_matches": _all_region_channel_shadow(first) == _all_region_channel_shadow(second),
        "center_shadow_matches": _all_region_center_shadow(first) == _all_region_center_shadow(second),
        "commutant_shadow_matches": _all_region_commutant_shadow(first) == _all_region_commutant_shadow(second),
        "algebra_profile_matches": _all_region_algebra_profile(first) == _all_region_algebra_profile(second),
        "algebra_difference_witness": _algebra_difference_witness(first, second),
        "access_counts": {
            "first": _access_counts(first),
            "second": _access_counts(second),
        },
    }


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


def _tensor_with_identity(code: StabilizerCode, extra_logicals: int) -> StabilizerCode:
    if extra_logicals < 0:
        raise ValueError("extra_logicals must be nonnegative")
    total_n = code.n + extra_logicals
    return StabilizerCode(
        total_n,
        (_shift_pauli(row, source_n=code.n, offset=0, total_n=total_n) for row in code.generators),
    )


def _spectator_lift_audit(max_extra_logicals: int = 3) -> dict[str, object]:
    first, second = _minimal_channel_counterexample_pair()
    records = []
    for extra in range(max_extra_logicals + 1):
        lifted_first = _tensor_with_identity(first, extra)
        lifted_second = _tensor_with_identity(second, extra)
        diff = _algebra_difference_witness(lifted_first, lifted_second)
        records.append(
            {
                "extra_logicals": extra,
                "n": lifted_first.n,
                "k": lifted_first.k,
                "distance": {
                    "first": lifted_first.distance(),
                    "second": lifted_second.distance(),
                },
                "channel_shadow_matches": _all_region_channel_shadow(lifted_first)
                == _all_region_channel_shadow(lifted_second),
                "algebra_differs": diff is not None,
                "algebra_difference_witness": diff,
            }
        )
    return {
        "name": "spectator logical tensor lift",
        "status": "pass"
        if all(record["channel_shadow_matches"] and record["algebra_differs"] for record in records)
        else "fail",
        "proof_idea": (
            "Tensor both codes with the same identity logical system. For every region, the logical subspace "
            "is a direct sum of the witness subspace and the identical spectator subspace, so zero/full "
            "channel access remains matched and the witness algebra difference persists."
        ),
        "records": tuple(records),
    }


def _concatenate_with_k1_inner(outer: StabilizerCode, inner: StabilizerCode) -> StabilizerCode:
    if inner.k != 1:
        raise ValueError("inner code must encode one logical qubit")
    block_size = inner.n
    block_count = outer.n
    total_n = block_size * block_count
    logical_z, logical_x = inner.logical_basis
    if not symplectic_product(logical_z, logical_x, inner.n):
        raise ValueError("inner logical basis must contain an anticommuting pair")

    rows: list[int] = []
    for block in range(block_count):
        for generator in inner.generators:
            rows.append(
                _shift_pauli(
                    generator,
                    source_n=inner.n,
                    offset=block * block_size,
                    total_n=total_n,
                )
            )
    for outer_generator in outer.generators:
        row = 0
        x = outer_generator & ((1 << outer.n) - 1)
        z = outer_generator >> outer.n
        for block in range(block_count):
            if (x >> block) & 1:
                row ^= _shift_pauli(
                    logical_x,
                    source_n=inner.n,
                    offset=block * block_size,
                    total_n=total_n,
                )
            if (z >> block) & 1:
                row ^= _shift_pauli(
                    logical_z,
                    source_n=inner.n,
                    offset=block * block_size,
                    total_n=total_n,
                )
        rows.append(row)
    return StabilizerCode(total_n, rows)


def _distance_three_audit(code: StabilizerCode) -> dict[str, object]:
    low_weight_correctable = all(
        code.erasure_correctable(mask)
        for size in range(3)
        for mask in masks_of_size(code.n, size)
    )
    weight_three_witness = None
    for mask in masks_of_size(code.n, 3):
        if not code.erasure_correctable(mask):
            weight_three_witness = mask_to_tuple(mask, code.n)
            break
    return {
        "status": "pass" if low_weight_correctable and weight_three_witness is not None else "fail",
        "all_weight_less_than_three_regions_correctable": low_weight_correctable,
        "weight_three_logical_witness": weight_three_witness,
        "distance_exact_if_pass": 3 if low_weight_correctable and weight_three_witness is not None else None,
    }


def _inner_threshold_audit(inner: StabilizerCode) -> dict[str, object]:
    small_correctable = all(
        inner.erasure_correctable(mask)
        for size in range(3)
        for mask in masks_of_size(inner.n, size)
    )
    large_reconstruct = all(
        inner.reconstructs_all_logicals(mask)
        for size in range(3, inner.n + 1)
        for mask in masks_of_size(inner.n, size)
    )
    return {
        "status": "pass" if small_correctable and large_reconstruct else "fail",
        "parameters": {"n": inner.n, "k": inner.k, "distance": inner.distance()},
        "generators": inner.pauli_generators(),
        "logical_basis": tuple(pauli_to_string(row, inner.n) for row in inner.logical_basis),
        "size_two_or_less_forbidden": small_correctable,
        "size_three_or_more_qualified": large_reconstruct,
    }


def _full_channel_shadow_mismatch(first: StabilizerCode, second: StabilizerCode) -> tuple[int, ...] | None:
    full = (1 << first.n) - 1
    for mask in all_masks(first.n):
        first_row = (first.erasure_correctable(mask), first.reconstructs_all_logicals(full ^ mask))
        second_row = (second.erasure_correctable(mask), second.reconstructs_all_logicals(full ^ mask))
        if first_row != second_row:
            return mask_to_tuple(mask, first.n)
    return None


def _amplified_witness_record(*, include_full_channel_scan: bool) -> dict[str, object]:
    first, second = _minimal_channel_counterexample_pair()
    inner = _five_qubit_perfect_code()
    amplified_first = _concatenate_with_k1_inner(first, inner)
    amplified_second = _concatenate_with_k1_inner(second, inner)
    witness_region = sum(1 << (block * inner.n + qubit) for block in (0, 1) for qubit in (0, 1, 2))
    mismatch = _full_channel_shadow_mismatch(amplified_first, amplified_second) if include_full_channel_scan else None
    return {
        "name": "five-qubit perfect inner concatenation",
        "status": "pass"
        if (
            _inner_threshold_audit(inner)["status"] == "pass"
            and _distance_three_audit(amplified_first)["status"] == "pass"
            and _distance_three_audit(amplified_second)["status"] == "pass"
            and amplified_first.region_algebra(witness_region).signature()
            != amplified_second.region_algebra(witness_region).signature()
            and (not include_full_channel_scan or mismatch is None)
        )
        else "fail",
        "construction": (
            "Replace each physical qubit of the n=3,k=2 counterexample with the same [[5,1,3]] "
            "perfect inner code. The inner code has only forbidden regions of size <=2 and qualified "
            "regions of size >=3, so arbitrary physical regions reduce to outer block subsets for "
            "zero/full channel access."
        ),
        "parameters": {
            "first": {"n": amplified_first.n, "k": amplified_first.k},
            "second": {"n": amplified_second.n, "k": amplified_second.k},
        },
        "inner_threshold_audit": _inner_threshold_audit(inner),
        "distance_audit": {
            "first": _distance_three_audit(amplified_first),
            "second": _distance_three_audit(amplified_second),
        },
        "representative_region": mask_to_tuple(witness_region, amplified_first.n),
        "representative_signatures": {
            "first": amplified_first.region_algebra(witness_region).signature(),
            "second": amplified_second.region_algebra(witness_region).signature(),
        },
        "full_channel_shadow_scan": {
            "run": include_full_channel_scan,
            "regions_checked": (1 << amplified_first.n) if include_full_channel_scan else 0,
            "first_mismatch_region": mismatch,
            "shadows_match": mismatch is None if include_full_channel_scan else None,
        },
    }


def goal5_kgt1_observer_tomography_certificate(
    *,
    max_n: int = 4,
    k: int = 2,
    equivalence: str = "permutation",
    max_codes_per_n: int | None = None,
    max_extra_logicals: int = 3,
    include_amplified_full_scan: bool = False,
) -> dict[str, object]:
    if k < 2:
        raise ValueError("Goal 5 requires k>1; use k>=2")

    minimal_first, minimal_second = _minimal_channel_counterexample_pair()
    center_first, center_second = _center_counterexample_pair()
    scan = bounded_kgt1_hierarchy_scan(
        max_n=max_n,
        k=k,
        equivalence=equivalence,
        max_codes_per_n=max_codes_per_n,
    )
    minimal_witness = _witness_record(minimal_first, minimal_second, matched_tier="channel")
    center_witness = _witness_record(center_first, center_second, matched_tier="channel_plus_center")
    spectator_lift = _spectator_lift_audit(max_extra_logicals=max_extra_logicals)
    amplified = _amplified_witness_record(include_full_channel_scan=include_amplified_full_scan)

    exact_claims = {
        "negative_channel_theorem": {
            "name": "k>1 Channel-Shadow Non-Identifiability",
            "claim": (
                "For k>1 finite stabilizer/OA-QEC codes, all-region erasure-correctability plus "
                "survivor fixed-point booleans do not determine all-region observer-algebra signatures."
            ),
            "proof_witness": "The two [[3,2,1]] stabilizer codes <XXI> and <XXX> have identical zero/full access for every region but differ on region {0,1}.",
        },
        "algebraic_completion_proposition": {
            "name": "Center-Commutant Signature Bookkeeping",
            "claim": (
                "For any finite stabilizer/OA-QEC code, the all-region center and commutant dimensions "
                "determine the all-region observer-algebra signatures."
            ),
            "proof_idea": (
                "Let W=L_R in the nondegenerate 2k-dimensional logical symplectic space. If c=dim W^perp, "
                "then dim W + c = 2k, so dim W=2k-c. The center dimension supplies dim rad(W), and the "
                "reconstructs_all bit follows from dim W=2k. Thus (logical_dim, center_dim, "
                "commutant_dim, reconstructs_all) is fixed. This is symplectic bookkeeping, not a "
                "non-tautological operational tomography theorem."
            ),
        },
    }
    certified_claims = {
        "k_gt_1_channel_shadow_counterexample_certified": minimal_witness["channel_shadow_matches"]
        and not minimal_witness["algebra_profile_matches"],
        "minimal_scan_completed": scan["status"] == "bounded_scan_complete",
        "permutation_quotient_first_channel_collision_at_n3": (
            scan["records"][0]["n"] == 2
            and next(record for record in scan["records"][0]["tier_records"] if record["tier"] == "channel")[
                "status"
            ]
            == "no_collision_found_in_bounded_scan"
            and scan["records"][1]["n"] == 3
            and next(record for record in scan["records"][1]["tier_records"] if record["tier"] == "channel")[
                "status"
            ]
            == "non_identifying_collision_found"
        ),
        "channel_plus_center_counterexample_certified": center_witness["channel_shadow_matches"]
        and center_witness["center_shadow_matches"]
        and not center_witness["algebra_profile_matches"],
        "center_commutant_completion_proposition_declared": True,
        "bounded_scan_center_commutant_no_collision": _tier_has_no_collisions(
            scan,
            "channel_plus_center_commutant",
        ),
        "full_bounded_scan_first_no_collision_at_center_commutant": (
            max_codes_per_n is not None
            or scan["first_no_collision_tier_observed"] == "channel_plus_center_commutant"
        ),
        "spectator_lift_certified": spectator_lift["status"] == "pass",
        "distance_amplified_witness_certified": amplified["status"] == "pass",
        "known_derived_k1_status_declared": True,
    }
    certified_claims["goal5_kgt1_observer_tomography_certificate"] = all(certified_claims.values())
    return {
        "goal": "Goal 5: k>1 Observer Algebra Tomography",
        "status": "pass" if certified_claims["goal5_kgt1_observer_tomography_certificate"] else "fail",
        "theorem_style_claims": exact_claims,
        "minimal_channel_counterexample": minimal_witness,
        "center_shadow_counterexample": center_witness,
        "bounded_hierarchy_scan": scan,
        "scalable_lift": spectator_lift,
        "distance_amplified_witness": amplified,
        "known_vs_new": {
            "known_derived": (
                "The k=1 completion lemma is best viewed as a stabilizer cleaning/QSS access-structure "
                "repackaging: zero/intermediate/full exhausts the two-dimensional logical symplectic space."
            ),
            "new_diagnostic_hierarchy": (
                "For k>1, zero/full erasure-channel access is too coarse. Center data alone is still too "
                "coarse in bounded search. Center plus logical commutant dimensions give an exact finite "
                "signature completion by symplectic bookkeeping; the non-tautological open problem is to "
                "replace direct commutant input with operational diagnostics."
            ),
        },
        "reproducibility": {
            "goal5_certificate": f"python3 -m qgtoy observer-tomography-kgt1 --max-n {max_n}",
            "goal5_with_amplified_full_scan": (
                f"python3 -m qgtoy observer-tomography-kgt1 --max-n {max_n} --include-amplified-full-scan"
            ),
        },
        "certified_claims": certified_claims,
        "expert_facing_interpretation": (
            "The finite observer-algebra tomography hierarchy separates entropy/min-cut size data from "
            "operator access data. For k>1, erasure/survivor channel shadows detect only forbidden and "
            "qualified regions; intermediate observer algebras require center/commutant information."
        ),
        "limitations": (
            "The counterexamples are finite stabilizer/OA-QEC codes. The minimality scan is over k=2 codes "
            "through n<=max_n under the declared equivalence. The distance-amplified witness uses a standard "
            "five-qubit perfect-code concatenation and an optional direct full-channel scan."
        ),
    }
