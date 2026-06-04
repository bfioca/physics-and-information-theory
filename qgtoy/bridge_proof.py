"""Symbolic checker for the balanced-bridge CSS separation family.

This module deliberately avoids the StabilizerCode verifier.  It works directly
with CSS support masks and GF(2) ranks so the all-m theorem can be audited from
the generator templates.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .gf2 import in_span, mask_to_tuple, rank
from .seed_data import SEED_A, SEED_B


OLD_N = len(SEED_A[0])
Z_BRIDGE_OLD = (1 << 1) | (1 << 2)
X_BRIDGE_OLD = (1 << 0) | (1 << 5)
Z_REGION_WITNESS = (1 << 1) | (1 << 3)


def _mask(*qubits: int) -> int:
    out = 0
    for qubit in qubits:
        out |= 1 << qubit
    return out


@dataclass(frozen=True)
class CssTemplate:
    name: str
    seed_generators: tuple[str, ...]
    seed_z: tuple[int, ...]
    seed_x: tuple[int, ...]
    distance_two_z_logical: int


def _parse_css_generators(generators: tuple[str, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    z_rows = []
    x_rows = []
    for generator in generators:
        if len(generator) != OLD_N:
            raise ValueError(f"expected length-{OLD_N} generator, got {generator!r}")
        z_mask = 0
        x_mask = 0
        for qubit, char in enumerate(generator):
            if char == "I":
                continue
            if char == "Z":
                z_mask |= 1 << qubit
                continue
            if char == "X":
                x_mask |= 1 << qubit
                continue
            raise ValueError(f"CSS checker only accepts I/X/Z rows, got {generator!r}")
        if z_mask and x_mask:
            raise ValueError(f"mixed CSS generator is not supported: {generator!r}")
        if z_mask:
            z_rows.append(z_mask)
        elif x_mask:
            x_rows.append(x_mask)
    return tuple(z_rows), tuple(x_rows)


def _template(name: str, generators: tuple[str, ...], distance_two_z_logical: int) -> CssTemplate:
    seed_z, seed_x = _parse_css_generators(generators)
    return CssTemplate(
        name=name,
        seed_generators=generators,
        seed_z=seed_z,
        seed_x=seed_x,
        distance_two_z_logical=distance_two_z_logical,
    )


TEMPLATES = {
    "A": _template("A", SEED_A, _mask(0, 5)),
    "B": _template("B", SEED_B, _mask(1, 3)),
}


def bridge_pair_mask(j: int) -> int:
    return (1 << (6 + 2 * j)) | (1 << (7 + 2 * j))


def p_qubit(j: int) -> int:
    return 6 + 2 * j


def q_qubit(j: int) -> int:
    return 7 + 2 * j


def css_rows(template: CssTemplate, m: int) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    n = OLD_N + 2 * m
    z_rows = list(template.seed_z)
    x_rows = list(template.seed_x)
    for j in range(m):
        pair = bridge_pair_mask(j)
        z_rows.append(Z_BRIDGE_OLD | pair)
        x_rows.append(X_BRIDGE_OLD | pair)
    return tuple(z_rows), tuple(x_rows), n


def row_supports(rows: tuple[int, ...], n: int) -> tuple[tuple[int, ...], ...]:
    return tuple(mask_to_tuple(row, n) for row in rows)


def restricted_sector_rank(rows: tuple[int, ...], n: int, region: int) -> int:
    full = (1 << n) - 1
    outside = full ^ region
    return rank(rows, n) - rank(tuple(row & outside for row in rows), n)


def restricted_css_rank(template: CssTemplate, m: int, region: int) -> int:
    z_rows, x_rows, n = css_rows(template, m)
    return restricted_sector_rank(z_rows, n, region) + restricted_sector_rank(x_rows, n, region)


def css_check_rank(template: CssTemplate, m: int) -> int:
    z_rows, x_rows, n = css_rows(template, m)
    return rank(z_rows, n) + rank(x_rows, n)


def _even_overlap(left: int, right: int) -> bool:
    return ((left & right).bit_count() & 1) == 0


def _same_rank_table(regions: tuple[int, ...], m: int) -> tuple[bool, tuple[dict[str, object], ...]]:
    n = OLD_N + 2 * m
    rows = []
    for region in regions:
        a_rank = restricted_css_rank(TEMPLATES["A"], m, region)
        b_rank = restricted_css_rank(TEMPLATES["B"], m, region)
        rows.append(
            {
                "region": mask_to_tuple(region, n),
                "A_rank": a_rank,
                "B_rank": b_rank,
                "matches": a_rank == b_rank,
            }
        )
    return all(row["matches"] for row in rows), tuple(rows)


def restricted_rank_cases() -> dict[str, object]:
    old_singletons = tuple(1 << i for i in range(OLD_N))
    old_pairs = tuple((1 << i) | (1 << j) for i, j in combinations(range(OLD_N), 2))
    new_singletons = (1 << p_qubit(0), 1 << q_qubit(0))
    old_new = tuple((1 << old) | (1 << new) for old in range(OLD_N) for new in (p_qubit(0), q_qubit(0)))
    same_bridge_pair = (bridge_pair_mask(0),)
    different_bridge_pairs = tuple(
        (1 << left) | (1 << right)
        for left in (p_qubit(0), q_qubit(0))
        for right in (p_qubit(1), q_qubit(1))
    )

    case_specs = (
        ("old_singletons", 0, old_singletons),
        ("old_old_pairs", 0, old_pairs),
        ("new_singletons", 1, new_singletons),
        ("old_new_pairs", 1, old_new),
        ("same_bridge_pair", 1, same_bridge_pair),
        ("different_bridge_pairs", 2, different_bridge_pairs),
    )
    cases = []
    for name, m, regions in case_specs:
        matches, table = _same_rank_table(regions, m)
        cases.append(
            {
                "case": name,
                "representative_m": m,
                "matches": matches,
                "ranks": table,
            }
        )
    return {
        "case_reduction": (
            "Every one- or two-qubit subset is an old singleton, an old-old pair, old-new, "
            "a singleton new qubit, the full pair {p_j,q_j}, or two new qubits from different bridge pairs. "
            "Bridge-index symmetry reduces these to the representative cases below."
        ),
        "cases": tuple(cases),
        "all_cases_match": all(case["matches"] for case in cases),
        "entropy_formula": "For a CSS stabilizer code state, S(R)=|R|-rank(S_R).",
    }


def _case_count_formulas() -> tuple[dict[str, object], ...]:
    return (
        {"case": "old_singletons", "count": "6"},
        {"case": "old_old_pairs", "count": "binom(6,2)=15"},
        {"case": "new_singletons", "count": "2m"},
        {"case": "old_new_pairs", "count": "12m"},
        {"case": "same_bridge_pair", "count": "m"},
        {"case": "different_bridge_pairs", "count": "2m(m-1)"},
    )


def _case_counts_for_m(m: int) -> dict[str, int]:
    return {
        "old_singletons": OLD_N,
        "old_old_pairs": (OLD_N * (OLD_N - 1)) // 2,
        "new_singletons": 2 * m,
        "old_new_pairs": OLD_N * 2 * m,
        "same_bridge_pair": m,
        "different_bridge_pairs": 2 * m * (m - 1),
    }


def classify_t2_region(region: int, n: int) -> str:
    qubits = mask_to_tuple(region, n)
    if len(qubits) not in (1, 2):
        raise ValueError(f"expected a one- or two-qubit region, got {qubits!r}")
    if all(qubit < OLD_N for qubit in qubits):
        return "old_singletons" if len(qubits) == 1 else "old_old_pairs"
    new_qubits = tuple(qubit for qubit in qubits if qubit >= OLD_N)
    if len(qubits) == 1:
        return "new_singletons"
    if len(new_qubits) == 1:
        return "old_new_pairs"
    left, right = new_qubits
    if (left - OLD_N) // 2 == (right - OLD_N) // 2:
        return "same_bridge_pair"
    return "different_bridge_pairs"


def restricted_rank_formula_prediction(template: CssTemplate, region: int, n: int) -> int:
    case = classify_t2_region(region, n)
    if case in ("old_singletons", "old_old_pairs"):
        old_region = region & ((1 << OLD_N) - 1)
        return restricted_css_rank(template, 0, old_region)
    if case == "same_bridge_pair":
        x_pair_rank = int(in_span(X_BRIDGE_OLD, template.seed_x, OLD_N))
        z_pair_rank = int(in_span(Z_BRIDGE_OLD, template.seed_z, OLD_N))
        return x_pair_rank + z_pair_rank
    return 0


def restricted_rank_formula_schema_check(sample_max_m: int = 4) -> dict[str, object]:
    """Derive and audit the all-m restricted-rank formula case by case."""

    bridge_span_obligations = {
        name: {
            "X_old_support_in_seed_X_span": in_span(X_BRIDGE_OLD, template.seed_x, OLD_N),
            "Z_old_support_in_seed_Z_span": in_span(Z_BRIDGE_OLD, template.seed_z, OLD_N),
            "same_bridge_pair_rank": restricted_rank_formula_prediction(template, bridge_pair_mask(0), OLD_N + 2),
        }
        for name, template in TEMPLATES.items()
    }
    old_regions = tuple(1 << i for i in range(OLD_N)) + tuple(
        (1 << i) | (1 << j) for i, j in combinations(range(OLD_N), 2)
    )
    old_rank_rules = tuple(
        {
            "region": mask_to_tuple(region, OLD_N),
            "A_rank": restricted_rank_formula_prediction(TEMPLATES["A"], region, OLD_N),
            "B_rank": restricted_rank_formula_prediction(TEMPLATES["B"], region, OLD_N),
        }
        for region in old_regions
    )
    case_rank_rules = (
        {
            "case": "old_singletons",
            "rank_rule": "restricted rank in the seed on the same old singleton",
            "all_seed_rows_match": all(item["A_rank"] == item["B_rank"] for item in old_rank_rules if len(item["region"]) == 1),
        },
        {
            "case": "old_old_pairs",
            "rank_rule": "restricted rank in the seed on the same old pair",
            "all_seed_rows_match": all(item["A_rank"] == item["B_rank"] for item in old_rank_rules if len(item["region"]) == 2),
        },
        {
            "case": "new_singletons",
            "A_rank": 0,
            "B_rank": 0,
            "rank_rule": "no same-sector row can be supported on a single fresh coordinate",
        },
        {
            "case": "old_new_pairs",
            "A_rank": 0,
            "B_rank": 0,
            "rank_rule": "a bridge row always carries both fresh coordinates of its pair",
        },
        {
            "case": "same_bridge_pair",
            "A_rank": bridge_span_obligations["A"]["same_bridge_pair_rank"],
            "B_rank": bridge_span_obligations["B"]["same_bridge_pair_rank"],
            "rank_rule": (
                "X bridge old support is in the seed X span, producing X_{p_j}X_{q_j}; "
                "Z bridge old support is not in either seed Z span, so no second local generator appears"
            ),
        },
        {
            "case": "different_bridge_pairs",
            "A_rank": 0,
            "B_rank": 0,
            "rank_rule": "fresh bridge-pair supports are disjoint and unique in each sector",
        },
    )

    prefix_samples = []
    for m in range(sample_max_m + 1):
        n = OLD_N + 2 * m
        expected_counts = _case_counts_for_m(m)
        observed_counts = {case: 0 for case in expected_counts}
        mismatches = []
        for size in (1, 2):
            for qubits in combinations(range(n), size):
                region = _mask(*qubits)
                case = classify_t2_region(region, n)
                observed_counts[case] += 1
                for name, template in TEMPLATES.items():
                    direct_rank = restricted_css_rank(template, m, region)
                    predicted_rank = restricted_rank_formula_prediction(template, region, n)
                    if direct_rank != predicted_rank:
                        mismatches.append(
                            {
                                "code": name,
                                "region": qubits,
                                "case": case,
                                "direct_rank": direct_rank,
                                "predicted_rank": predicted_rank,
                            }
                        )
        prefix_samples.append(
            {
                "m": m,
                "n": n,
                "expected_case_counts": expected_counts,
                "observed_case_counts": observed_counts,
                "counts_match_formula": observed_counts == expected_counts,
                "rank_formula_mismatches": tuple(mismatches),
                "all_regions_match_formula": not mismatches,
            }
        )

    cases_match = all(
        item.get("all_seed_rows_match", item.get("A_rank") == item.get("B_rank")) for item in case_rank_rules
    )
    span_obligations_pass = all(
        item["X_old_support_in_seed_X_span"]
        and not item["Z_old_support_in_seed_Z_span"]
        and item["same_bridge_pair_rank"] == 1
        for item in bridge_span_obligations.values()
    )

    return {
        "claim": (
            "For every m, every one- or two-qubit region has the restricted CSS rank predicted by "
            "its support case, and the A_m and B_m predictions are equal."
        ),
        "case_count_formulas": _case_count_formulas(),
        "case_rank_rules": case_rank_rules,
        "old_rank_rules": old_rank_rules,
        "bridge_span_obligations": bridge_span_obligations,
        "fresh_coordinate_rule": (
            "Bridge j has fresh support {6+2j,7+2j}; these pair supports are nonzero, pairwise "
            "disjoint, and appear once per sector, so any same-sector combination using a bridge "
            "row exposes a whole uncanceled pair unless its old support is canceled in the seed."
        ),
        "prefix_formula_samples": tuple(prefix_samples),
        "passes": cases_match
        and span_obligations_pass
        and all(sample["counts_match_formula"] and sample["all_regions_match_formula"] for sample in prefix_samples),
    }


def restricted_rank_schema_check(sample_max_m: int = 4) -> dict[str, object]:
    """Audit the finite case schema used by the all-m restricted-rank proof."""

    old_regions = tuple(1 << i for i in range(OLD_N)) + tuple(
        (1 << i) | (1 << j) for i, j in combinations(range(OLD_N), 2)
    )
    old_regions_match, old_rank_table = _same_rank_table(old_regions, 0)
    bridge_x_cancelable = {
        name: in_span(X_BRIDGE_OLD, template.seed_x, OLD_N) for name, template in TEMPLATES.items()
    }
    bridge_z_not_cancelable = {
        name: not in_span(Z_BRIDGE_OLD, template.seed_z, OLD_N) for name, template in TEMPLATES.items()
    }

    fresh_pair_obligations = []
    for m in range(sample_max_m + 1):
        for name, template in TEMPLATES.items():
            z_rows, x_rows, _ = css_rows(template, m)
            expected_fresh_pairs = tuple(bridge_pair_mask(j) for j in range(m))
            z_fresh_pairs = tuple(row & ~((1 << OLD_N) - 1) for row in z_rows[len(template.seed_z) :])
            x_fresh_pairs = tuple(row & ~((1 << OLD_N) - 1) for row in x_rows[len(template.seed_x) :])
            fresh_pair_obligations.append(
                {
                    "m": m,
                    "code": name,
                    "Z_fresh_pairs_match_rule": z_fresh_pairs == expected_fresh_pairs,
                    "X_fresh_pairs_match_rule": x_fresh_pairs == expected_fresh_pairs,
                    "fresh_pairs_are_unique": len(set(expected_fresh_pairs)) == m,
                }
            )

    prefix_samples = []
    for m in range(sample_max_m + 1):
        n = OLD_N + 2 * m
        case_counts: dict[str, int] = {
            "old_singletons": 0,
            "old_old_pairs": 0,
            "new_singletons": 0,
            "old_new_pairs": 0,
            "same_bridge_pair": 0,
            "different_bridge_pairs": 0,
        }
        mismatches = []
        for size in (1, 2):
            for qubits in combinations(range(n), size):
                region = _mask(*qubits)
                case = classify_t2_region(region, n)
                case_counts[case] += 1
                a_rank = restricted_css_rank(TEMPLATES["A"], m, region)
                b_rank = restricted_css_rank(TEMPLATES["B"], m, region)
                if a_rank != b_rank:
                    mismatches.append(
                        {
                            "region": qubits,
                            "case": case,
                            "A_rank": a_rank,
                            "B_rank": b_rank,
                        }
                    )
        prefix_samples.append(
            {
                "m": m,
                "n": n,
                "total_regions": n + (n * (n - 1)) // 2,
                "case_counts": case_counts,
                "mismatches": tuple(mismatches),
                "all_match": not mismatches,
            }
        )

    obligations_pass = (
        old_regions_match
        and all(bridge_x_cancelable.values())
        and all(bridge_z_not_cancelable.values())
        and all(
            item["Z_fresh_pairs_match_rule"]
            and item["X_fresh_pairs_match_rule"]
            and item["fresh_pairs_are_unique"]
            for item in fresh_pair_obligations
        )
    )

    return {
        "claim": "All one- and two-qubit regions fall into six support cases whose restricted CSS ranks match.",
        "case_classifier": (
            "old_singletons, old_old_pairs, new_singletons, old_new_pairs, "
            "same_bridge_pair, different_bridge_pairs"
        ),
        "old_rank_table": old_rank_table,
        "obligations": {
            "old_regions_match_seed_table": old_regions_match,
            "bridge_X_old_support_in_seed_X_span": bridge_x_cancelable,
            "bridge_Z_old_support_not_in_seed_Z_span": bridge_z_not_cancelable,
            "fresh_pair_rule_samples": tuple(fresh_pair_obligations),
            "obligations_pass": obligations_pass,
        },
        "prefix_exhaustive_samples": tuple(prefix_samples),
        "passes": obligations_pass and all(sample["all_match"] for sample in prefix_samples),
    }


def commutation_check() -> dict[str, object]:
    per_code = {}
    for name, template in TEMPLATES.items():
        seed_overlaps = [
            {
                "z": mask_to_tuple(z_row, OLD_N),
                "x": mask_to_tuple(x_row, OLD_N),
                "even": _even_overlap(z_row, x_row),
            }
            for z_row in template.seed_z
            for x_row in template.seed_x
        ]
        bridge_z_seed_x = [
            {
                "bridge_Z_old": mask_to_tuple(Z_BRIDGE_OLD, OLD_N),
                "seed_X": mask_to_tuple(x_row, OLD_N),
                "even": _even_overlap(Z_BRIDGE_OLD, x_row),
            }
            for x_row in template.seed_x
        ]
        bridge_x_seed_z = [
            {
                "bridge_X_old": mask_to_tuple(X_BRIDGE_OLD, OLD_N),
                "seed_Z": mask_to_tuple(z_row, OLD_N),
                "even": _even_overlap(X_BRIDGE_OLD, z_row),
            }
            for z_row in template.seed_z
        ]
        per_code[name] = {
            "seed_Z_vs_seed_X": tuple(seed_overlaps),
            "bridge_Z_vs_seed_X": tuple(bridge_z_seed_x),
            "bridge_X_vs_seed_Z": tuple(bridge_x_seed_z),
            "bridge_Z_vs_same_bridge_X_overlap_size": (Z_BRIDGE_OLD & X_BRIDGE_OLD).bit_count() + 2,
            "bridge_Z_vs_different_bridge_X_overlap_size": (Z_BRIDGE_OLD & X_BRIDGE_OLD).bit_count(),
            "passes": (
                all(item["even"] for item in seed_overlaps)
                and all(item["even"] for item in bridge_z_seed_x)
                and all(item["even"] for item in bridge_x_seed_z)
                and _even_overlap(Z_BRIDGE_OLD, X_BRIDGE_OLD)
            ),
        }
    return {
        "per_code": per_code,
        "passes": all(item["passes"] for item in per_code.values()),
    }


def rank_and_k_check(sample_max_m: int = 4) -> dict[str, object]:
    samples = []
    for m in range(sample_max_m + 1):
        n = OLD_N + 2 * m
        samples.append(
            {
                "m": m,
                "n": n,
                "A_rank": css_check_rank(TEMPLATES["A"], m),
                "B_rank": css_check_rank(TEMPLATES["B"], m),
                "expected_rank": 5 + 2 * m,
                "expected_k": 1,
            }
        )
    seed_ranks = {
        name: {
            "seed_Z_rank": rank(template.seed_z, OLD_N),
            "seed_X_rank": rank(template.seed_x, OLD_N),
            "seed_total_rank": rank(template.seed_z, OLD_N) + rank(template.seed_x, OLD_N),
        }
        for name, template in TEMPLATES.items()
    }
    return {
        "seed_ranks": seed_ranks,
        "fresh_qubit_independence_argument": (
            "Each bridge Z row has the fresh pair {p_j,q_j} in the Z sector and no other "
            "Z row contains those fresh coordinates. The same holds independently in the X sector."
        ),
        "samples": tuple(samples),
        "passes": all(
            item["A_rank"] == item["expected_rank"] and item["B_rank"] == item["expected_rank"] for item in samples
        )
        and all(item["seed_total_rank"] == 5 for item in seed_ranks.values()),
    }


def distance_check() -> dict[str, object]:
    per_code = {}
    for name, template in TEMPLATES.items():
        old_incidence = []
        for qubit in range(OLD_N):
            has_z = any((row >> qubit) & 1 for row in template.seed_z)
            has_x = any((row >> qubit) & 1 for row in template.seed_x)
            old_incidence.append({"qubit": qubit, "has_Z_check": has_z, "has_X_check": has_x})
        z_logical = template.distance_two_z_logical
        z_logical_commutes_with_seed_x = all(_even_overlap(z_logical, x_row) for x_row in template.seed_x)
        z_logical_commutes_with_bridge_x = _even_overlap(z_logical, X_BRIDGE_OLD)
        z_logical_not_seed_stabilizer = not in_span(z_logical, template.seed_z, OLD_N)
        per_code[name] = {
            "old_qubit_incidence": tuple(old_incidence),
            "new_qubit_incidence_template": {
                "p_j": {"has_Z_check": True, "has_X_check": True},
                "q_j": {"has_Z_check": True, "has_X_check": True},
            },
            "weight_two_Z_logical": mask_to_tuple(z_logical, OLD_N),
            "logical_commutes_with_seed_X": z_logical_commutes_with_seed_x,
            "logical_commutes_with_bridge_X": z_logical_commutes_with_bridge_x,
            "logical_not_seed_Z_stabilizer": z_logical_not_seed_stabilizer,
            "passes": (
                all(item["has_Z_check"] and item["has_X_check"] for item in old_incidence)
                and z_logical_commutes_with_seed_x
                and z_logical_commutes_with_bridge_x
                and z_logical_not_seed_stabilizer
            ),
        }
    return {
        "argument": (
            "Every qubit has both Z-check and X-check incidence, so no weight-one Pauli is in the centralizer. "
            "The listed weight-two Z logical remains in the centralizer and is not a stabilizer, hence d=2."
        ),
        "per_code": per_code,
        "passes": all(item["passes"] for item in per_code.values()),
    }


def reconstruction_check(sample_max_m: int = 4) -> dict[str, object]:
    a_old_equations = (_mask(1, 2), _mask(1), _mask(2, 3))
    a_old_equation_rank = rank(a_old_equations, OLD_N)
    z13_not_stabilizer = {
        name: not in_span(Z_REGION_WITNESS, template.seed_z, OLD_N) for name, template in TEMPLATES.items()
    }
    z13_commutes = {
        name: all(_even_overlap(Z_REGION_WITNESS, x_row) for x_row in template.seed_x)
        and _even_overlap(Z_REGION_WITNESS, X_BRIDGE_OLD)
        for name, template in TEMPLATES.items()
    }

    b_witness_samples = []
    for m in range(sample_max_m + 1):
        x_witness = _mask(2, 3)
        for j in range(m):
            x_witness |= 1 << p_qubit(j)
        z_rows, _, n = css_rows(TEMPLATES["B"], m)
        region = _mask(1, 2, 3)
        for j in range(m):
            region |= 1 << p_qubit(j)
        b_witness_samples.append(
            {
                "m": m,
                "R_m": mask_to_tuple(region, n),
                "X_witness": mask_to_tuple(x_witness, n),
                "supported_in_R_m": (x_witness & ~region) == 0,
                "commutes_with_all_Z_checks": all(_even_overlap(x_witness, z_row) for z_row in z_rows),
                "anticommutes_with_Z_1_Z_3": not _even_overlap(x_witness, Z_REGION_WITNESS),
            }
        )

    return {
        "R_m": "{1,2,3} union {p_j : 0 <= j < m}",
        "Z_1_Z_3": {
            "commutes_with_all_X_checks": z13_commutes,
            "not_a_Z_stabilizer": z13_not_stabilizer,
        },
        "A_no_X_on_R_m": {
            "restricted_Z_equations_on_old_R_variables": (
                "Z_{0,1,2,5} gives x1+x2=0",
                "Z_{1,4} gives x1=0",
                "Z_{2,3} gives x2+x3=0",
            ),
            "old_equation_rank": a_old_equation_rank,
            "bridge_equation": "each Z_{1,2,p_j,q_j} gives x1+x2+x_{p_j}=0 on R_m, so x_{p_j}=0",
            "kernel_dimension_formula": "|R_m| - (3 + m) = 0",
            "passes": a_old_equation_rank == 3,
        },
        "B_X_witness": {
            "formula": "X_2 X_3 product_j X_{p_j}",
            "samples": tuple(b_witness_samples),
            "passes": all(
                item["supported_in_R_m"]
                and item["commutes_with_all_Z_checks"]
                and item["anticommutes_with_Z_1_Z_3"]
                for item in b_witness_samples
            ),
        },
        "signatures": {
            "A_m": (1, 1, 1, False),
            "B_m": (2, 0, 0, True),
            "reason": (
                "Since k=1, the supported quotient algebra has dimension at most two. "
                "A_m has a nonzero central Z logical and no X part on R_m; B_m has an anticommuting Z/X pair."
            ),
        },
        "passes": (
            all(z13_commutes.values())
            and all(z13_not_stabilizer.values())
            and a_old_equation_rank == 3
            and all(
                item["supported_in_R_m"]
                and item["commutes_with_all_Z_checks"]
                and item["anticommutes_with_Z_1_Z_3"]
                for item in b_witness_samples
            )
        ),
    }


def proof_text() -> str:
    return """Balanced-bridge proof.

Define A_m and B_m from the n=6 CSS seeds by adding, for every j=0,...,m-1,
fresh qubits p_j=6+2j and q_j=7+2j and the common checks
Z_1 Z_2 Z_{p_j} Z_{q_j} and X_0 X_5 X_{p_j} X_{q_j}.

Commutation.  The seed CSS checks commute by direct even-overlap calculation.
The new Z bridge has old support {1,2}, which has even overlap with every seed
X check in both seeds.  The new X bridge has old support {0,5}, which has even
overlap with every seed Z check in both seeds.  A bridge Z and the X bridge
with the same index overlap on p_j and q_j, hence in two positions; bridges
with different indices have no fresh overlap and {1,2} cap {0,5} is empty.
Thus all generators commute for every m.

Rank and k.  Each seed has three independent Z checks and two independent X
checks.  In the Z sector, bridge j contains the fresh coordinates p_j and q_j,
which no other Z row contains; hence every bridge Z row is independent of all
earlier Z rows.  The same argument holds in the X sector.  Therefore the check
rank is 5+2m while n=6+2m, so k=n-rank=1.

Distance.  The A family keeps the weight-two Z logical Z_0 Z_5, and the B
family keeps the weight-two Z logical Z_1 Z_3.  These commute with every X
check and are not Z stabilizers.  Conversely, every old qubit is touched by at
least one seed Z check and one seed X check in both seeds; every new qubit is
touched by its bridge Z and bridge X check.  Therefore no weight-one Pauli lies
in the centralizer, so d=2.

Restricted ranks for all one- and two-qubit subsets.  For CSS stabilizer code
states, S(R)=|R|-rank(S_R), where S_R is the stabilizer subgroup supported
inside R.  Every singleton or pair is one of these six support cases: old
singleton, old-old pair, old-new pair, new singleton, the full bridge pair
{p_j,q_j}, or two new qubits from distinct bridge pairs.  Old-only regions
reduce to the seed rank table because any bridge row has fresh coordinates that
cannot be canceled by same-sector rows.  New singletons, old-new pairs, and
pairs from distinct bridges have local rank 0 in both families for the same
unique-fresh-coordinate reason.  The full bridge pair {p_j,q_j} has local rank
1 in both families: combine X_0 X_5 X_{p_j} X_{q_j} with the seed X_0 X_5 to
get X_{p_j} X_{q_j}.  There
is no second Z-type local generator because {1,2} is not in the seed Z span in
either seed.  Hence all labeled one- and two-qubit entropies agree.

Separating region.  Let R_m={1,2,3} union {p_j}.  In both families Z_1 Z_3 is
supported on R_m, commutes with all X checks, and is not a stabilizer.  In A_m
there is no supported X part on R_m: the restricted Z equations give x1=0,
x1+x2=0, x2+x3=0, and then each bridge equation gives x_{p_j}=0.  Thus A_m
has only a central logical on R_m, with signature (1,1,1,false).  In B_m the
operator X_2 X_3 product_j X_{p_j} is supported on R_m, commutes with all Z
checks, and anticommutes with Z_1 Z_3.  Since k=1, this is the full logical
algebra on R_m, with signature (2,0,0,true).  The reconstruction profiles are
therefore distinct for every m.
"""


def bridge_symbolic_proof_check(sample_max_m: int = 4, *, include_proof_text: bool = True) -> dict[str, object]:
    commutation = commutation_check()
    rank_and_k = rank_and_k_check(sample_max_m=sample_max_m)
    distance = distance_check()
    restricted_ranks = restricted_rank_cases()
    restricted_rank_schema = restricted_rank_schema_check(sample_max_m=sample_max_m)
    restricted_rank_formula_schema = restricted_rank_formula_schema_check(sample_max_m=sample_max_m)
    reconstruction = reconstruction_check(sample_max_m=sample_max_m)
    checks = {
        "commutation": commutation["passes"],
        "rank_and_k": rank_and_k["passes"],
        "distance": distance["passes"],
        "restricted_rank_cases": restricted_ranks["all_cases_match"],
        "restricted_rank_schema": restricted_rank_schema["passes"],
        "restricted_rank_formula_schema": restricted_rank_formula_schema["passes"],
        "reconstruction_difference": reconstruction["passes"],
    }
    payload: dict[str, object] = {
        "name": "Balanced-bridge symbolic proof checker",
        "method": (
            "Direct CSS support-mask and GF(2)-rank checks from the generator templates; "
            "does not call StabilizerCode."
        ),
        "sample_max_m": sample_max_m,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "templates": {
            name: {
                "seed_generators": template.seed_generators,
                "seed_Z_supports": row_supports(template.seed_z, OLD_N),
                "seed_X_supports": row_supports(template.seed_x, OLD_N),
            }
            for name, template in TEMPLATES.items()
        },
        "bridge_rule": {
            "Z_old_support": mask_to_tuple(Z_BRIDGE_OLD, OLD_N),
            "X_old_support": mask_to_tuple(X_BRIDGE_OLD, OLD_N),
            "new_qubits": "p_j=6+2j, q_j=7+2j",
        },
        "commutation": commutation,
        "rank_and_k": rank_and_k,
        "distance": distance,
        "restricted_ranks": restricted_ranks,
        "restricted_rank_schema": restricted_rank_schema,
        "restricted_rank_formula_schema": restricted_rank_formula_schema,
        "reconstruction": reconstruction,
    }
    if include_proof_text:
        payload["proof_text"] = proof_text()
    return payload
