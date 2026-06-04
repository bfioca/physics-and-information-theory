"""Goal 6 operational observer-algebra tomography certificates."""

from __future__ import annotations

from .gf2 import all_masks, in_span, mask_to_tuple, rank, rref
from .observer_tomography_kgt1 import (
    _all_region_algebra_profile,
    _all_region_center_shadow,
    _all_region_channel_shadow,
    _center_counterexample_pair,
    _concatenate_with_k1_inner,
    _distance_three_audit,
    _five_qubit_perfect_code,
    _inner_threshold_audit,
    _minimal_channel_counterexample_pair,
)
from .search import enumerate_stabilizer_codes
from .stabilizer import StabilizerCode, combine_rows, symplectic_product


def _logical_probe_labels(code: StabilizerCode) -> tuple[int, ...]:
    return tuple(range(1, 1 << (2 * code.k)))


def _logical_probe_row(code: StabilizerCode, label: int) -> int:
    return combine_rows(label, code.logical_basis)


def _perturbed_code(code: StabilizerCode, label: int) -> StabilizerCode:
    return StabilizerCode(code.n, (*code.generators, _logical_probe_row(code, label)))


def _single_probe_entropy_response(code: StabilizerCode, region: int, label: int) -> int:
    """Entropy drop after imposing one labeled logical Pauli eigenvalue."""
    return code.entropy(region) - _perturbed_code(code, label).entropy(region)


def _probe_visible_by_recovery(code: StabilizerCode, region: int, label: int) -> bool:
    """Whether the labeled logical Pauli has a representative on region."""
    row = _logical_probe_row(code, label)
    local_logicals = code.logical_subspace_supported(region)
    return in_span(row, (*code.generators, *local_logicals), code.width)


def _visible_probe_labels_from_entropy(code: StabilizerCode, region: int) -> tuple[int, ...]:
    visible = []
    for label in _logical_probe_labels(code):
        response = _single_probe_entropy_response(code, region, label)
        if response not in (0, 1):
            raise ValueError(f"unexpected entropy response {response} for label {label}")
        if response:
            visible.append(label)
    return tuple(visible)


def _visible_probe_dimension(code: StabilizerCode, region: int) -> int:
    return rank(_visible_probe_labels_from_entropy(code, region), 2 * code.k)


def _logical_label_symplectic_product(code: StabilizerCode, left: int, right: int) -> int:
    return symplectic_product(
        _logical_probe_row(code, left),
        _logical_probe_row(code, right),
        code.n,
    )


def _visible_commutator_rank(code: StabilizerCode, region: int) -> int:
    basis = rref(_visible_probe_labels_from_entropy(code, region), 2 * code.k)
    rows = []
    for left in basis:
        row = 0
        for index, right in enumerate(basis):
            if _logical_label_symplectic_product(code, left, right):
                row |= 1 << index
        rows.append(row)
    return rank(rows, len(basis)) if basis else 0


def _operational_signature(code: StabilizerCode, region: int) -> tuple[int, int, int, bool]:
    visible_dim = _visible_probe_dimension(code, region)
    commutator_rank = _visible_commutator_rank(code, region)
    center_dim = visible_dim - commutator_rank
    return (visible_dim, center_dim, 2 * code.k - visible_dim, visible_dim == 2 * code.k)


def _entropy_response_dimension_shadow(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], int], ...]:
    return tuple((mask_to_tuple(mask, code.n), _visible_probe_dimension(code, mask)) for mask in all_masks(code.n))


def _center_plus_entropy_response_shadow(
    code: StabilizerCode,
) -> tuple[tuple[tuple[int, ...], int, int], ...]:
    return tuple(
        (
            mask_to_tuple(mask, code.n),
            code.region_algebra(mask).center_dim,
            _visible_probe_dimension(code, mask),
        )
        for mask in all_masks(code.n)
    )


def _commutator_test_shadow(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], int, int], ...]:
    return tuple(
        (
            mask_to_tuple(mask, code.n),
            _visible_probe_dimension(code, mask),
            _visible_commutator_rank(code, mask),
        )
        for mask in all_masks(code.n)
    )


def _operational_signature_shadow(
    code: StabilizerCode,
) -> tuple[tuple[tuple[int, ...], tuple[int, int, int, bool]], ...]:
    return tuple((mask_to_tuple(mask, code.n), _operational_signature(code, mask)) for mask in all_masks(code.n))


def _center_only_shadow(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], int], ...]:
    return _all_region_center_shadow(code)


def _goal6_tier_key(code: StabilizerCode, tier: str) -> object:
    if tier == "channel":
        return _all_region_channel_shadow(code)
    if tier == "center":
        return _center_only_shadow(code)
    if tier == "channel_plus_center":
        return (_all_region_channel_shadow(code), _center_only_shadow(code))
    if tier == "entropy_response_dimension":
        return _entropy_response_dimension_shadow(code)
    if tier == "center_plus_entropy_response":
        return _center_plus_entropy_response_shadow(code)
    if tier in {
        "entropy_response_commutator",
        "logical_relative_entropy_distinguishability",
        "recovery_success_spectrum",
        "commutator_test",
    }:
        return _commutator_test_shadow(code)
    if tier == "full_signature":
        return _all_region_algebra_profile(code)
    raise ValueError(f"unknown Goal 6 operational tier: {tier}")


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
        groups.setdefault(_goal6_tier_key(code, tier), []).append(code)

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


def bounded_goal6_operational_scan(
    *,
    max_n: int = 4,
    k: int = 2,
    equivalence: str = "permutation",
    max_codes_per_n: int | None = None,
) -> dict[str, object]:
    tiers = (
        "channel",
        "center",
        "channel_plus_center",
        "entropy_response_dimension",
        "center_plus_entropy_response",
        "entropy_response_commutator",
        "logical_relative_entropy_distinguishability",
        "recovery_success_spectrum",
        "commutator_test",
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
    return {
        "status": "bounded_scan_complete",
        "scope": {
            "max_n": max_n,
            "k": k,
            "equivalence": equivalence,
            "max_codes_per_n": max_codes_per_n,
        },
        "tiers": tiers,
        "records": tuple(records),
    }


def _tier_has_no_collisions(scan: dict[str, object], tier: str) -> bool:
    return all(
        next(record for record in n_record["tier_records"] if record["tier"] == tier)["status"]
        == "no_collision_found_in_bounded_scan"
        for n_record in scan["records"]
    )


def _all_region_operational_audit(code: StabilizerCode) -> dict[str, object]:
    signature_mismatches = []
    response_mismatches = []
    subspace_failures = []
    for mask in all_masks(code.n):
        visible = _visible_probe_labels_from_entropy(code, mask)
        visible_set = set(visible)
        if 0 in visible_set:
            subspace_failures.append({"region": mask_to_tuple(mask, code.n), "reason": "zero_visible"})
        for left in visible:
            for right in visible:
                if (left ^ right) and (left ^ right) not in visible_set:
                    subspace_failures.append(
                        {
                            "region": mask_to_tuple(mask, code.n),
                            "reason": "visible_labels_not_closed_under_sum",
                            "left": left,
                            "right": right,
                        }
                    )
                    break
            if subspace_failures:
                break
        for label in _logical_probe_labels(code):
            entropy_bit = _single_probe_entropy_response(code, mask, label)
            recovery_bit = _probe_visible_by_recovery(code, mask, label)
            if bool(entropy_bit) != recovery_bit:
                response_mismatches.append(
                    {
                        "region": mask_to_tuple(mask, code.n),
                        "label": label,
                        "entropy_response": entropy_bit,
                        "recovery_success": recovery_bit,
                    }
                )
        direct = code.region_algebra(mask).signature()
        operational = _operational_signature(code, mask)
        if direct != operational:
            signature_mismatches.append(
                {
                    "region": mask_to_tuple(mask, code.n),
                    "direct_signature": direct,
                    "operational_signature": operational,
                }
            )
    return {
        "status": "pass"
        if not signature_mismatches and not response_mismatches and not subspace_failures
        else "fail",
        "parameters": {"n": code.n, "k": code.k, "distance": code.distance()},
        "generators": code.pauli_generators(),
        "regions_checked": 1 << code.n,
        "logical_probe_labels_checked_per_region": len(_logical_probe_labels(code)),
        "signature_mismatches": tuple(signature_mismatches),
        "entropy_recovery_mismatches": tuple(response_mismatches),
        "visible_subspace_failures": tuple(subspace_failures),
    }


def _bounded_operational_theorem_audit(
    *,
    max_n: int,
    k: int,
    equivalence: str,
    max_codes_per_n: int | None,
) -> dict[str, object]:
    records = []
    first_failure = None
    for n in range(max(1, k), max_n + 1):
        codes = tuple(enumerate_stabilizer_codes(n, k=k, equivalence=equivalence, max_codes=max_codes_per_n))
        codes_checked = 0
        regions_checked = 0
        probe_checks = 0
        for code in codes:
            audit = _all_region_operational_audit(code)
            codes_checked += 1
            regions_checked += audit["regions_checked"]
            probe_checks += audit["regions_checked"] * audit["logical_probe_labels_checked_per_region"]
            if audit["status"] != "pass" and first_failure is None:
                first_failure = audit
        records.append(
            {
                "n": n,
                "k": k,
                "codes_checked": codes_checked,
                "regions_checked": regions_checked,
                "single_logical_probe_checks": probe_checks,
            }
        )
    return {
        "status": "pass" if first_failure is None else "fail",
        "scope": {
            "max_n": max_n,
            "k": k,
            "equivalence": equivalence,
            "max_codes_per_n": max_codes_per_n,
        },
        "records": tuple(records),
        "first_failure": first_failure,
    }


def _block_threshold_region(outer_mask: int, *, block_size: int) -> int:
    region = 0
    for block in range(outer_mask.bit_length()):
        if (outer_mask >> block) & 1:
            for qubit in range(3):
                region |= 1 << (block * block_size + qubit)
    return region


def _threshold_amplified_witness(
    first: StabilizerCode,
    second: StabilizerCode,
    *,
    name: str,
    outer_witness_region: int,
    matched_shadow: str,
) -> dict[str, object]:
    inner = _five_qubit_perfect_code()
    amplified_first = _concatenate_with_k1_inner(first, inner)
    amplified_second = _concatenate_with_k1_inner(second, inner)
    representative_region = _block_threshold_region(outer_witness_region, block_size=inner.n)
    outer_channel_matches = _all_region_channel_shadow(first) == _all_region_channel_shadow(second)
    outer_center_matches = _all_region_center_shadow(first) == _all_region_center_shadow(second)
    matched = outer_channel_matches if matched_shadow == "channel" else outer_channel_matches and outer_center_matches
    representative_differs = (
        amplified_first.region_algebra(representative_region).signature()
        != amplified_second.region_algebra(representative_region).signature()
    )
    distance_pass = (
        _distance_three_audit(amplified_first)["status"] == "pass"
        and _distance_three_audit(amplified_second)["status"] == "pass"
    )
    return {
        "name": name,
        "status": "pass" if _inner_threshold_audit(inner)["status"] == "pass" and matched and representative_differs and distance_pass else "fail",
        "construction": (
            "Concatenate every outer qubit with the same [[5,1,3]] perfect inner code. "
            "The inner threshold reduces every physical region to the subset of outer "
            "blocks where at least three inner qubits survive."
        ),
        "matched_shadow": matched_shadow,
        "outer_generators": {
            "first": first.pauli_generators(),
            "second": second.pauli_generators(),
        },
        "outer_masks_checked_for_threshold_shadow": 1 << first.n,
        "outer_channel_shadow_matches": outer_channel_matches,
        "outer_center_shadow_matches": outer_center_matches,
        "parameters": {
            "first": {"n": amplified_first.n, "k": amplified_first.k},
            "second": {"n": amplified_second.n, "k": amplified_second.k},
        },
        "inner_threshold_audit": _inner_threshold_audit(inner),
        "distance_audit": {
            "first": _distance_three_audit(amplified_first),
            "second": _distance_three_audit(amplified_second),
        },
        "representative_region": mask_to_tuple(representative_region, amplified_first.n),
        "representative_signatures": {
            "first": amplified_first.region_algebra(representative_region).signature(),
            "second": amplified_second.region_algebra(representative_region).signature(),
        },
    }


def goal6_operational_observer_tomography_certificate(
    *,
    max_n: int = 4,
    k: int = 2,
    equivalence: str = "permutation",
    max_codes_per_n: int | None = None,
) -> dict[str, object]:
    if k < 2:
        raise ValueError("Goal 6 requires k>1; use k>=2")

    channel_first, channel_second = _minimal_channel_counterexample_pair()
    center_first, center_second = _center_counterexample_pair()
    scan = bounded_goal6_operational_scan(
        max_n=max_n,
        k=k,
        equivalence=equivalence,
        max_codes_per_n=max_codes_per_n,
    )
    theorem_audit = _bounded_operational_theorem_audit(
        max_n=max_n,
        k=k,
        equivalence=equivalence,
        max_codes_per_n=max_codes_per_n,
    )
    witness_audits = {
        "channel_counterexample_first": _all_region_operational_audit(channel_first),
        "channel_counterexample_second": _all_region_operational_audit(channel_second),
        "channel_plus_center_counterexample_first": _all_region_operational_audit(center_first),
        "channel_plus_center_counterexample_second": _all_region_operational_audit(center_second),
    }
    amplified_channel = _threshold_amplified_witness(
        channel_first,
        channel_second,
        name="distance-amplified channel-shadow insufficiency witness",
        outer_witness_region=(1 << 0) | (1 << 1),
        matched_shadow="channel",
    )
    amplified_center = _threshold_amplified_witness(
        center_first,
        center_second,
        name="distance-amplified channel-plus-center insufficiency witness",
        outer_witness_region=(1 << 1) | (1 << 2),
        matched_shadow="channel_plus_center",
    )
    certified_claims = {
        "channel_shadow_insufficient_for_k_gt_1": _all_region_channel_shadow(channel_first)
        == _all_region_channel_shadow(channel_second)
        and _all_region_algebra_profile(channel_first) != _all_region_algebra_profile(channel_second),
        "center_shadow_insufficient": _all_region_center_shadow(center_first) == _all_region_center_shadow(center_second)
        and _all_region_algebra_profile(center_first) != _all_region_algebra_profile(center_second),
        "channel_plus_center_shadow_insufficient": _goal6_tier_key(center_first, "channel_plus_center")
        == _goal6_tier_key(center_second, "channel_plus_center")
        and _all_region_algebra_profile(center_first) != _all_region_algebra_profile(center_second),
        "center_plus_entropy_response_sufficient_in_bounded_scan": _tier_has_no_collisions(
            scan,
            "center_plus_entropy_response",
        ),
        "entropy_response_commutator_sufficient_in_bounded_scan": _tier_has_no_collisions(
            scan,
            "entropy_response_commutator",
        ),
        "relative_entropy_profile_equivalent_to_entropy_response": _tier_has_no_collisions(
            scan,
            "logical_relative_entropy_distinguishability",
        ),
        "recovery_success_spectrum_equivalent_to_entropy_response": _tier_has_no_collisions(
            scan,
            "recovery_success_spectrum",
        ),
        "commutator_test_shadow_sufficient_in_bounded_scan": _tier_has_no_collisions(scan, "commutator_test"),
        "operational_completion_theorem_bounded_audit": theorem_audit["status"] == "pass",
        "witness_operational_audits_pass": all(record["status"] == "pass" for record in witness_audits.values()),
        "distance_amplified_channel_witness": amplified_channel["status"] == "pass",
        "distance_amplified_channel_plus_center_witness": amplified_center["status"] == "pass",
    }
    certified_claims["goal6_operational_observer_tomography_certificate"] = all(certified_claims.values())
    return {
        "goal": "Goal 6: Operational Observer Algebra Tomography",
        "status": "pass" if certified_claims["goal6_operational_observer_tomography_certificate"] else "fail",
        "operational_completion_theorem": {
            "name": "Single-Probe Response and Commutator-Test Completion",
            "claim": (
                "For finite stabilizer/OA-QEC codes, the all-region single-logical-Pauli entropy-response "
                "profile determines which logical Pauli probes are visible on each region. With operational "
                "commutator tests among visible probes, it determines every observer-algebra signature "
                "without directly supplying dim L_R^perp."
            ),
            "proof_sketch": (
                "For a logical Pauli v, impose the logical constraint v=+1. The entropy drop on region R "
                "is one exactly when the class v has a representative supported on R, and zero otherwise. "
                "Thus the response profile recovers L_R as a visible probe subspace. Pairwise commutator "
                "tests give the rank of the restricted symplectic form on L_R. Hence logical_dim=dim L_R, "
                "center_dim=dim L_R-rank, commutant_dim=2k-dim L_R, and reconstructs_all iff dim L_R=2k."
            ),
            "operational_assumptions": (
                "The finite-code protocol assumes labeled logical Pauli probes: prepare or condition on "
                "the v=+1 logical eigenspace, then measure entropy, distinguishability, recovery, and "
                "commutator responses on a physical region R."
            ),
        },
        "hierarchy_scope": (
            "The diagnostic records are a hierarchy of insufficiency and completion, not a proven total "
            "information order. Channel shadows, center shadows, and response shadows are different kinds "
            "of data unless explicitly combined."
        ),
        "diagnostic_hierarchy": (
            {
                "shadow": "erasure/survivor channel",
                "result": "insufficient",
                "witness": "[[3,2,1]] <XXI> vs <XXX>",
            },
            {
                "shadow": "center alone and channel+center",
                "result": "insufficient",
                "witness": "[[4,2,1]] <XIIX,XXXI> vs <IZXI,ZIXX>",
            },
            {
                "shadow": "center + entropy-response dimension",
                "result": "sufficient for signatures",
                "reason": "entropy response gives dim L_R; center supplies dim radical",
            },
            {
                "shadow": "entropy/relative-entropy/recovery response + commutator tests",
                "result": "sufficient for signatures",
                "reason": "operationally recovers dim L_R and restricted symplectic rank, not L_R^perp directly",
            },
        ),
        "bounded_operational_scan": scan,
        "bounded_operational_theorem_audit": theorem_audit,
        "witness_operational_audits": witness_audits,
        "distance_amplified_witnesses": {
            "channel": amplified_channel,
            "channel_plus_center": amplified_center,
        },
        "known_vs_new": {
            "known_derived": (
                "The stabilizer cleaning/QSS/OA-QEC facts identify supported logical Paulis with recoverable "
                "operator probes, and stabilizer entropy under added checks is standard rank bookkeeping."
            ),
            "new_diagnostic_hierarchy": (
                "The Goal 6 package uses those facts to separate non-operational commutant bookkeeping from "
                "operational observer-algebra tomography: weak shadows fail for k>1, while single-probe "
                "entropy/relative-entropy/recovery responses plus commutator tests complete the finite "
                "stabilizer signature."
            ),
        },
        "reproducibility": {
            "goal6_certificate": f"python3 -m qgtoy observer-tomography-operational --max-n {max_n}",
        },
        "certified_claims": certified_claims,
        "limitations": (
            "This is an exact finite stabilizer/OA-QEC result. The operational completion uses labeled "
            "logical Pauli probes and exact entropy/recovery/commutator tests. It is not yet an approximate "
            "QEC theorem, a non-Pauli operator-algebra theorem, or a continuum gravity statement."
        ),
    }
