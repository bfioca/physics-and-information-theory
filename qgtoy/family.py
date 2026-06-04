"""Mechanism analysis and lift attempts for the robust n=6 CSS witness."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Iterator

from .gf2 import all_masks, mask_to_tuple
from .gf2 import parity
from .bridge_proof import bridge_symbolic_proof_check
from .robust import RobustConstraints, code_quality, entropy_key, quality_summary
from .seed_data import SEED_A, SEED_B
from .stabilizer import StabilizerCode, pauli_to_string, support_mask


@dataclass(frozen=True)
class CssDecomposition:
    x_checks: tuple[int, ...]
    z_checks: tuple[int, ...]


@dataclass(frozen=True)
class ExtensionRule:
    name: str
    description: str
    first: StabilizerCode
    second: StabilizerCode


@dataclass(frozen=True)
class CandidateFamilyCheck:
    name: str
    description: str
    n: int
    k: int
    passes_first: bool
    passes_second: bool
    entropy_profile_matches: bool
    labeled_entropy_matches: bool
    reconstruction_differs: bool
    nontrivial_added_qubits: bool
    quality_first: dict[str, object]
    quality_second: dict[str, object]
    mechanism: str
    first: StabilizerCode
    second: StabilizerCode

    @property
    def is_family_step(self) -> bool:
        return (
            self.passes_first
            and self.passes_second
            and self.labeled_entropy_matches
            and self.reconstruction_differs
            and self.nontrivial_added_qubits
        )


def seed_pair() -> tuple[StabilizerCode, StabilizerCode]:
    return StabilizerCode.from_pauli_strings(SEED_A), StabilizerCode.from_pauli_strings(SEED_B)


def css_decomposition(code: StabilizerCode) -> CssDecomposition:
    x_checks = []
    z_checks = []
    mask = (1 << code.n) - 1
    for row in code.generators:
        x = row & mask
        z = row >> code.n
        if x and z:
            raise ValueError("not a CSS code")
        if x:
            x_checks.append(x)
        elif z:
            z_checks.append(z)
    return CssDecomposition(tuple(x_checks), tuple(z_checks))


def bit_support(row: int, n: int) -> tuple[int, ...]:
    return tuple(i for i in range(n) if (row >> i) & 1)


def support_strings(rows: Iterable[int], n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(bit_support(row, n) for row in rows)


def local_rank_vector(code: StabilizerCode, max_subset_size: int = 2) -> tuple[tuple[tuple[int, ...], int], ...]:
    return tuple(
        (mask_to_tuple(mask, code.n), len(code.stabilizer_supported_basis(mask)))
        for mask in all_masks(code.n)
        if mask.bit_count() <= max_subset_size
    )


def reconstruction_poset(code: StabilizerCode) -> tuple[tuple[tuple[int, ...], tuple[int, int, int, bool]], ...]:
    return tuple(
        (mask_to_tuple(mask, code.n), code.region_algebra(mask).signature())
        for mask in all_masks(code.n)
        if code.region_algebra(mask).logical_dim > 0
    )


def logical_support_summary(code: StabilizerCode) -> tuple[dict[str, object], ...]:
    out = []
    for row in code.logical_basis:
        out.append(
            {
                "pauli": pauli_to_string(row, code.n),
                "support": mask_to_tuple(support_mask(row, code.n), code.n),
                "weight": support_mask(row, code.n).bit_count(),
            }
        )
    return tuple(out)


def witness_mechanism_summary() -> dict[str, object]:
    first, second = seed_pair()
    first_css = css_decomposition(first)
    second_css = css_decomposition(second)
    constraints = RobustConstraints()
    return {
        "first": {
            "generators": first.pauli_generators(),
            "x_check_supports": support_strings(first_css.x_checks, first.n),
            "z_check_supports": support_strings(first_css.z_checks, first.n),
            "logical_supports": logical_support_summary(first),
            "quality": quality_summary(first, constraints),
            "minimal_reconstruction_regions": [
                mask_to_tuple(mask, first.n) for mask in first.reconstruction_regions(minimal=True)
            ],
        },
        "second": {
            "generators": second.pauli_generators(),
            "x_check_supports": support_strings(second_css.x_checks, second.n),
            "z_check_supports": support_strings(second_css.z_checks, second.n),
            "logical_supports": logical_support_summary(second),
            "quality": quality_summary(second, constraints),
            "minimal_reconstruction_regions": [
                mask_to_tuple(mask, second.n) for mask in second.reconstruction_regions(minimal=True)
            ],
        },
        "same_labeled_t2_entropy": entropy_key(first, max_subset_size=2, mode="labeled")
        == entropy_key(second, max_subset_size=2, mode="labeled"),
        "same_labeled_t2_local_stabilizer_ranks": local_rank_vector(first, 2) == local_rank_vector(second, 2),
        "changed_checks": {
            "z": {
                "first": support_strings(first_css.z_checks, first.n),
                "second": support_strings(second_css.z_checks, second.n),
            },
            "x": {
                "first": support_strings(first_css.x_checks, first.n),
                "second": support_strings(second_css.x_checks, second.n),
            },
        },
        "mechanism": (
            "The pair shifts one Z-check endpoint and compensates with a larger X-check. "
            "All one- and two-qubit restricted stabilizer ranks stay matched, so labeled "
            "t=2 entropy is blind. The logical Z representative changes support geometry, "
            "which changes which regions carry a full noncommuting logical pair."
        ),
    }


def extend_with_coupled_pair(
    code: StabilizerCode,
    *,
    z_anchor: int,
    x_anchor: int,
) -> StabilizerCode:
    """Add two new qubits coupled to old anchors by one Z check and one X check.

    This is intentionally not a spectator Bell pair: both new checks touch one old
    and one new qubit, and the added qubits are tied together by opposite-type
    checks through the existing code.
    """
    n = code.n
    new_n = n + 2
    rows = []
    for row in code.generators:
        x = row & ((1 << n) - 1)
        z = row >> n
        rows.append(x | (z << new_n))
    rows.append(((1 << z_anchor) | (1 << n)) << new_n)
    rows.append((1 << x_anchor) | (1 << (n + 1)))
    return StabilizerCode(new_n, rows)


def extend_checks_with_new_pair(
    code: StabilizerCode,
    *,
    z_check_index: int,
    x_check_index: int,
) -> StabilizerCode:
    """Extend one existing Z check and one existing X check onto a new qubit pair."""
    n = code.n
    new_n = n + 2
    css = css_decomposition(code)
    rows = []
    for index, z_row in enumerate(css.z_checks):
        if index == z_check_index:
            z_row |= (1 << n) | (1 << (n + 1))
        rows.append(z_row << new_n)
    for index, x_row in enumerate(css.x_checks):
        if index == x_check_index:
            x_row |= (1 << n) | (1 << (n + 1))
        rows.append(x_row)
    rows.append(((1 << n) | (1 << (n + 1))) << new_n)
    rows.append((1 << n) | (1 << (n + 1)))
    return StabilizerCode(new_n, rows)


def append_balanced_bridge_pair(
    code: StabilizerCode,
    *,
    z_old_support: int,
    x_old_support: int,
) -> StabilizerCode:
    """Append two qubits with one new Z check and one new X check.

    Both new checks touch the same two new qubits plus an old support. The
    two-new-qubit overlap makes the new X/Z checks commute with each other when
    the old supports have even overlap.
    """
    n = code.n
    new_n = n + 2
    rows = []
    for row in code.generators:
        x = row & ((1 << n) - 1)
        z = row >> n
        rows.append(x | (z << new_n))
    new_pair = (1 << n) | (1 << (n + 1))
    rows.append((z_old_support | new_pair) << new_n)
    rows.append(x_old_support | new_pair)
    return StabilizerCode(new_n, rows)


def pair_participation(code: StabilizerCode, old_n: int) -> bool:
    for qubit in range(old_n, code.n):
        touches_old = False
        for row in code.generators:
            support = support_mask(row, code.n)
            if ((support >> qubit) & 1) and support & ((1 << old_n) - 1):
                touches_old = True
                break
        if not touches_old:
            return False
    return True


def check_candidate_family_step(
    rule: ExtensionRule,
    *,
    old_n: int = 6,
    constraints: RobustConstraints = RobustConstraints(),
) -> CandidateFamilyCheck:
    first = rule.first
    second = rule.second
    q1 = code_quality(first, constraints)
    q2 = code_quality(second, constraints)
    entropy_profile_matches = entropy_key(first, max_subset_size=2, mode="profile") == entropy_key(
        second,
        max_subset_size=2,
        mode="profile",
    )
    labeled_entropy_matches = entropy_key(first, max_subset_size=2, mode="labeled") == entropy_key(
        second,
        max_subset_size=2,
        mode="labeled",
    )
    reconstruction_differs = first.reconstruction_profile() != second.reconstruction_profile()
    nontrivial_added = pair_participation(first, old_n) and pair_participation(second, old_n)
    mechanism = (
        "candidate lift preserves the seed mutation while coupling added qubits to old checks"
        if labeled_entropy_matches
        else "candidate lift changes at least one labeled t=2 entropy probe"
    )
    return CandidateFamilyCheck(
        name=rule.name,
        description=rule.description,
        n=first.n,
        k=first.k,
        passes_first=q1.passes,
        passes_second=q2.passes,
        entropy_profile_matches=entropy_profile_matches,
        labeled_entropy_matches=labeled_entropy_matches,
        reconstruction_differs=reconstruction_differs,
        nontrivial_added_qubits=nontrivial_added,
        quality_first=quality_summary(first, constraints),
        quality_second=quality_summary(second, constraints),
        mechanism=mechanism,
        first=first,
        second=second,
    )


def coupled_pair_lift_candidates() -> Iterator[CandidateFamilyCheck]:
    first, second = seed_pair()
    for z_anchor, x_anchor in product(range(first.n), repeat=2):
        try:
            first_lift = extend_with_coupled_pair(first, z_anchor=z_anchor, x_anchor=x_anchor)
            second_lift = extend_with_coupled_pair(second, z_anchor=z_anchor, x_anchor=x_anchor)
        except ValueError:
            continue
        yield check_candidate_family_step(
            ExtensionRule(
                name=f"coupled-pair-z{z_anchor}-x{x_anchor}",
                description="add two qubits with one old-new Z check and one old-new X check",
                first=first_lift,
                second=second_lift,
            )
        )


def check_extension_lift_candidates() -> Iterator[CandidateFamilyCheck]:
    first, second = seed_pair()
    first_css = css_decomposition(first)
    second_css = css_decomposition(second)
    z_count = min(len(first_css.z_checks), len(second_css.z_checks))
    x_count = min(len(first_css.x_checks), len(second_css.x_checks))
    for z_index, x_index in product(range(z_count), range(x_count)):
        try:
            first_lift = extend_checks_with_new_pair(first, z_check_index=z_index, x_check_index=x_index)
            second_lift = extend_checks_with_new_pair(second, z_check_index=z_index, x_check_index=x_index)
        except ValueError:
            continue
        yield check_candidate_family_step(
            ExtensionRule(
                name=f"extend-checks-z{z_index}-x{x_index}",
                description="extend matching indexed Z and X checks onto a new coupled qubit pair",
                first=first_lift,
                second=second_lift,
            )
        )


def common_bridge_supports() -> Iterator[tuple[int, int]]:
    first, second = seed_pair()
    first_css = css_decomposition(first)
    second_css = css_decomposition(second)
    n = first.n
    for z_support, x_support in product(range(1, 1 << n), repeat=2):
        if parity(z_support & x_support):
            continue
        if any(parity(z_support & row) for row in first_css.x_checks + second_css.x_checks):
            continue
        if any(parity(x_support & row) for row in first_css.z_checks + second_css.z_checks):
            continue
        yield z_support, x_support


def balanced_bridge_lift_candidates(max_supports: int | None = None) -> Iterator[CandidateFamilyCheck]:
    first, second = seed_pair()
    checked = 0
    for z_support, x_support in common_bridge_supports():
        if max_supports is not None and checked >= max_supports:
            break
        checked += 1
        try:
            first_lift = append_balanced_bridge_pair(first, z_old_support=z_support, x_old_support=x_support)
            second_lift = append_balanced_bridge_pair(second, z_old_support=z_support, x_old_support=x_support)
        except ValueError:
            continue
        name = "balanced-bridge-z{}-x{}".format(
            "-".join(map(str, bit_support(z_support, first.n))),
            "-".join(map(str, bit_support(x_support, first.n))),
        )
        yield check_candidate_family_step(
            ExtensionRule(
                name=name,
                description="append a two-qubit bridge with new old-supported Z and X checks",
                first=first_lift,
                second=second_lift,
            )
        )


def repeat_balanced_bridge(
    z_support: int,
    x_support: int,
    *,
    steps: int,
) -> tuple[StabilizerCode, StabilizerCode]:
    first, second = seed_pair()
    for _ in range(steps):
        first = append_balanced_bridge_pair(first, z_old_support=z_support, x_old_support=x_support)
        second = append_balanced_bridge_pair(second, z_old_support=z_support, x_old_support=x_support)
    return first, second


def repeated_bridge_family_frontier(
    max_steps: int = 3,
    *,
    max_supports: int | None = None,
) -> list[dict[str, object]]:
    out = []
    checked = 0
    for z_support, x_support in common_bridge_supports():
        if max_supports is not None and checked >= max_supports:
            break
        checked += 1
        step_results = []
        all_steps_pass = True
        for step in range(1, max_steps + 1):
            first, second = repeat_balanced_bridge(z_support, x_support, steps=step)
            check = check_candidate_family_step(
                ExtensionRule(
                    name=f"balanced-bridge-repeat-{step}",
                    description="repeat the same two-qubit balanced bridge",
                    first=first,
                    second=second,
                ),
                old_n=first.n - 2,
            )
            step_results.append(summarize_candidate(check))
            all_steps_pass = all_steps_pass and check.is_family_step
        if all_steps_pass:
            out.append(
                {
                    "z_support": bit_support(z_support, 6),
                    "x_support": bit_support(x_support, 6),
                    "max_steps_verified": max_steps,
                    "steps": step_results,
                }
            )
    return out


def summarize_candidate(check: CandidateFamilyCheck, *, include_codes: bool = False) -> dict[str, object]:
    payload: dict[str, object] = {
        "name": check.name,
        "description": check.description,
        "n": check.n,
        "k": check.k,
        "passes_first": check.passes_first,
        "passes_second": check.passes_second,
        "entropy_profile_matches": check.entropy_profile_matches,
        "labeled_entropy_matches": check.labeled_entropy_matches,
        "reconstruction_differs": check.reconstruction_differs,
        "nontrivial_added_qubits": check.nontrivial_added_qubits,
        "is_family_step": check.is_family_step,
        "quality_first": check.quality_first,
        "quality_second": check.quality_second,
        "mechanism": check.mechanism,
    }
    if include_codes:
        payload["first_generators"] = check.first.pauli_generators()
        payload["second_generators"] = check.second.pauli_generators()
        payload["first_logical_basis"] = tuple(pauli_to_string(row, check.first.n) for row in check.first.logical_basis)
        payload["second_logical_basis"] = tuple(pauli_to_string(row, check.second.n) for row in check.second.logical_basis)
        payload["first_minimal_reconstruction_regions"] = [
            mask_to_tuple(mask, check.first.n) for mask in check.first.reconstruction_regions(minimal=True)
        ]
        payload["second_minimal_reconstruction_regions"] = [
            mask_to_tuple(mask, check.second.n) for mask in check.second.reconstruction_regions(minimal=True)
        ]
    return payload


def coupled_pair_invalid_count() -> int:
    first, second = seed_pair()
    invalid = 0
    for z_anchor, x_anchor in product(range(first.n), repeat=2):
        try:
            extend_with_coupled_pair(first, z_anchor=z_anchor, x_anchor=x_anchor)
            extend_with_coupled_pair(second, z_anchor=z_anchor, x_anchor=x_anchor)
        except ValueError:
            invalid += 1
    return invalid


def bridge_family_certificate(
    *,
    z_support: int = (1 << 1) | (1 << 2),
    x_support: int = (1 << 0) | (1 << 5),
    max_steps: int = 3,
    include_codes: bool = False,
) -> dict[str, object]:
    steps = []
    for step in range(1, max_steps + 1):
        first, second = repeat_balanced_bridge(z_support, x_support, steps=step)
        check = check_candidate_family_step(
            ExtensionRule(
                name=f"balanced-bridge-family-m{step}",
                description="append m identical two-qubit balanced bridges to the n=6 CSS witness",
                first=first,
                second=second,
            ),
            old_n=first.n - 2,
        )
        steps.append(summarize_candidate(check, include_codes=include_codes))
    return {
        "rule": {
            "base_pair": {"first": SEED_A, "second": SEED_B},
            "z_old_support": bit_support(z_support, 6),
            "x_old_support": bit_support(x_support, 6),
            "append_step": (
                "For bridge j, add new qubits a=6+2j,b=7+2j and checks "
                "Z(z_old_support) Z_a Z_b and X(x_old_support) X_a X_b to both codes."
            ),
        },
        "mechanism": (
            "The bridge checks are identical in both codes and commute with the seed mutation. "
            "They couple each new qubit to old support without introducing single-qubit logicals. "
            "The original low-order-rank-blind mutation remains present, so labeled t=2 entropy "
            "continues to match while reconstruction regions are shifted by the added bridge qubits."
        ),
        "proof_sketch": (
            "For the default supports Z_old={1,2}, X_old={0,5}, every bridge check commutes with "
            "the seed checks in both codes: Z_old has even overlap with each X check, X_old has even "
            "overlap with each Z check, and bridge Z/X checks overlap on two new qubits. Each bridge "
            "pair contributes two independent checks, so n and r both increase by 2 and k remains 1. "
            "No new weight-1 logical appears because each new qubit is touched by both a Z bridge and "
            "an X bridge, while the seed already has no weight-1 logicals; the old weight-2 logicals "
            "remain, so distance stays 2. For any subsystem of size at most 2, bridge rows either do "
            "not fit inside the subsystem or contribute the same local rank to both codes; old-only "
            "subsystems reduce to the seed equality. The B-side authorized regions remain one qubit "
            "smaller than the A-side regions after choosing one qubit from each bridge pair, so the "
            "reconstruction/algebra profiles remain different."
        ),
        "steps": steps,
    }


def seed_t2_rank_table() -> tuple[tuple[tuple[int, ...], int], ...]:
    first, second = seed_pair()
    first_table = local_rank_vector(first, 2)
    second_table = local_rank_vector(second, 2)
    if first_table != second_table:
        raise ValueError("seed pair no longer has matching t=2 local ranks")
    return first_table


def bridge_theorem_certificate(
    *,
    max_exact_steps: int = 3,
    include_exact_codes: bool = False,
) -> dict[str, object]:
    exact_prefix = bridge_family_certificate(max_steps=max_exact_steps, include_codes=include_exact_codes)
    symbolic_checker = bridge_symbolic_proof_check(sample_max_m=max(4, max_exact_steps))
    return {
        "name": "Balanced-bridge CSS separation family",
        "proof_status": (
            "machine-checked symbolic proof for all m, with exact verifier certificates "
            "for the requested prefix"
        ),
        "family": {
            "base_A": SEED_A,
            "base_B": SEED_B,
            "bridge_index": "j = 0, ..., m-1",
            "new_qubits": "p_j = 6 + 2j, q_j = 7 + 2j",
            "checks_added_to_both_codes": (
                "Z_1 Z_2 Z_{p_j} Z_{q_j}",
                "X_0 X_5 X_{p_j} X_{q_j}",
            ),
            "n": "6 + 2m",
            "k": "1",
            "distance": "2",
        },
        "all_m_claims": {
            "commutation": "proved by even-overlap checks between every new bridge row and every seed/bridge opposite-type row",
            "rank_and_k": "each bridge contributes two independent checks on fresh qubits, so n and rank both increase by 2",
            "distance": "seed weight-2 logicals remain logical; every qubit has both X- and Z-check incidence, excluding weight-1 logicals",
            "labeled_t2_entropy": (
                "S(R)=|R|-rank(S_R). Old-old ranks equal by the seed table; each bridge pair has the same local "
                "X_{p_j}X_{q_j} stabilizer in both codes; every other singleton or pair involving bridge qubits has "
                "equal local stabilizer rank."
            ),
            "no_single_qubit_noncentral": "stronger fact: no single-qubit Pauli lies in the centralizer for either code",
            "reconstruction_difference": (
                "For R_m={1,2,3} union {p_j}, A_m has region algebra signature (1,1,1,false), generated by "
                "central Z_{1}Z_{3}; B_m has signature (2,0,0,true), generated by Z_{1}Z_{3} and "
                "X_{2}X_{3} product_j X_{p_j}."
            ),
        },
        "symbolic_witness_region": {
            "R_m": "{1,2,3} union {p_j : 0 <= j < m}",
            "A_m_signature_on_R_m": (1, 1, 1, False),
            "B_m_signature_on_R_m": (2, 0, 0, True),
            "A_m_supported_logical": "Z_1 Z_3 is central on R_m; no X-type logical can be supported on R_m",
            "B_m_supported_logicals": (
                "Z_1 Z_3",
                "X_2 X_3 product_j X_{p_j}",
            ),
        },
        "restricted_rank_mechanism": {
            "seed_t2_local_rank_table": seed_t2_rank_table(),
            "bridge_pair_rank": "rank(S_{p_j,q_j}) = 1 in both codes, from X_{p_j}X_{q_j}",
            "other_new_pair_rank": "0 unless the pair is exactly {p_j,q_j}",
            "old_new_pair_rank": "0 for every old-new pair",
        },
        "symbolic_checker": symbolic_checker,
        "exact_prefix": exact_prefix,
    }


def lift_frontier(
    *,
    max_balanced_supports: int | None = 32,
    max_repeat_steps: int = 1,
    max_repeated_supports: int | None = 16,
    include_codes: bool = False,
) -> dict[str, object]:
    candidates = (
        list(coupled_pair_lift_candidates())
        + list(check_extension_lift_candidates())
        + list(balanced_bridge_lift_candidates(max_supports=max_balanced_supports))
    )
    successes = [candidate for candidate in candidates if candidate.is_family_step]
    by_failure: dict[str, int] = {}
    for candidate in candidates:
        if candidate.is_family_step:
            continue
        reasons = []
        if not candidate.passes_first or not candidate.passes_second:
            reasons.append("robust_filters")
        if not candidate.labeled_entropy_matches:
            reasons.append("labeled_entropy")
        if not candidate.reconstruction_differs:
            reasons.append("reconstruction")
        if not candidate.nontrivial_added_qubits:
            reasons.append("participation")
        key = "+".join(reasons) if reasons else "unknown"
        by_failure[key] = by_failure.get(key, 0) + 1
    return {
        "total_candidates": len(candidates),
        "max_balanced_supports": max_balanced_supports,
        "max_repeat_steps": max_repeat_steps,
        "max_repeated_supports": max_repeated_supports,
        "invalid_coupled_pair_attempts": coupled_pair_invalid_count(),
        "successes": [summarize_candidate(candidate, include_codes=include_codes) for candidate in successes],
        "failure_counts": by_failure,
        "sample_failures": [summarize_candidate(candidate) for candidate in candidates[:10] if not candidate.is_family_step],
        "repeated_bridge_families": repeated_bridge_family_frontier(
            max_steps=max_repeat_steps,
            max_supports=max_repeated_supports,
        )
        if max_repeat_steps > 0
        else [],
    }
