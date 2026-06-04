"""Robust low-order entropy/reconstruction separation searches."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from .gf2 import all_masks, mask_to_tuple
from .search import DiscordantPair, enumerate_stabilizer_codes
from .stabilizer import StabilizerCode, pauli_to_string
from .structured import (
    enumerate_css_codes,
    enumerate_graph_subspace_codes,
    enumerate_shallow_encoder_codes,
)

ROBUST_SOURCES = ("exhaustive", "css", "cyclic-css", "graph", "encoder")
ENTROPY_KEY_MODES = ("profile", "labeled")


@dataclass(frozen=True)
class RobustConstraints:
    max_subset_size: int = 2
    min_distance: int = 2
    min_reconstruction_size: int = 2
    forbid_single_qubit_noncentral: bool = True


@dataclass(frozen=True)
class CodeQuality:
    distance: int | None
    minimal_reconstruction_size: int | None
    has_single_qubit_noncentral_logical: bool
    passes: bool
    reason: str


@dataclass(frozen=True)
class RobustScan:
    n: int
    k: int
    source: str
    equivalence: str
    entropy_key_mode: str
    constraints: RobustConstraints
    raw_codes: int
    codes_checked: int
    entropy_classes: int
    pair: DiscordantPair | None
    status: str


@dataclass(frozen=True)
class RobustFrontier:
    max_n: int
    k: int
    sources: tuple[str, ...]
    equivalence: str
    entropy_key_mode: str
    constraints: RobustConstraints
    scans: tuple[RobustScan, ...]

    @property
    def pair(self) -> DiscordantPair | None:
        for scan in self.scans:
            if scan.pair is not None:
                return scan.pair
        return None


def entropy_key(code: StabilizerCode, *, max_subset_size: int, mode: str) -> tuple:
    if mode == "profile":
        return code.entropy_profile(max_subset_size=max_subset_size)
    if mode == "labeled":
        return tuple(
            (mask, code.entropy(mask))
            for mask in all_masks(code.n)
            if mask.bit_count() <= max_subset_size
        )
    raise ValueError(f"unknown entropy key mode {mode!r}")


def minimal_reconstruction_size(code: StabilizerCode) -> int | None:
    regions = code.reconstruction_regions(minimal=True)
    if not regions:
        return None
    return min(region.bit_count() for region in regions)


def has_single_qubit_noncentral_logical(code: StabilizerCode) -> bool:
    for qubit in range(code.n):
        algebra = code.region_algebra(1 << qubit)
        if algebra.logical_dim > algebra.center_dim:
            return True
    return False


def code_quality(code: StabilizerCode, constraints: RobustConstraints) -> CodeQuality:
    distance = code.distance()
    if distance is None or distance < constraints.min_distance:
        return CodeQuality(distance, None, False, False, "distance")

    min_recon = minimal_reconstruction_size(code)
    if min_recon is None or min_recon < constraints.min_reconstruction_size:
        return CodeQuality(distance, min_recon, False, False, "minimal_reconstruction_size")

    single_noncentral = has_single_qubit_noncentral_logical(code)
    if constraints.forbid_single_qubit_noncentral and single_noncentral:
        return CodeQuality(distance, min_recon, single_noncentral, False, "single_qubit_noncentral")

    return CodeQuality(distance, min_recon, single_noncentral, True, "ok")


def iter_source_codes(
    source: str,
    *,
    n: int,
    k: int,
    equivalence: str,
    max_codes: int | None = None,
    encoder_depth: int = 2,
) -> Iterator[StabilizerCode]:
    if source == "exhaustive":
        yield from enumerate_stabilizer_codes(n, k=k, equivalence=equivalence, max_codes=max_codes)
        return
    if source == "css":
        yield from enumerate_css_codes(n, k=k, equivalence=equivalence, cyclic=False, max_codes=max_codes)
        return
    if source == "cyclic-css":
        yield from enumerate_css_codes(n, k=k, equivalence=equivalence, cyclic=True, max_codes=max_codes)
        return
    if source == "graph":
        yield from enumerate_graph_subspace_codes(n, k=k, equivalence=equivalence, max_codes=max_codes)
        return
    if source == "encoder":
        yield from enumerate_shallow_encoder_codes(
            n,
            k=k,
            max_depth=encoder_depth,
            equivalence=equivalence,
            max_codes=max_codes,
        )
        return
    raise ValueError(f"unknown robust source {source!r}")


def scan_robust_source(
    *,
    n: int,
    k: int,
    source: str,
    equivalence: str = "permutation",
    entropy_key_mode: str = "profile",
    constraints: RobustConstraints = RobustConstraints(),
    max_codes: int | None = None,
    encoder_depth: int = 2,
) -> RobustScan:
    if source not in ROBUST_SOURCES:
        raise ValueError(f"source must be one of {ROBUST_SOURCES}")
    if entropy_key_mode not in ENTROPY_KEY_MODES:
        raise ValueError(f"entropy_key_mode must be one of {ENTROPY_KEY_MODES}")

    raw_codes = 0
    codes_checked = 0
    by_entropy: dict[tuple, tuple[StabilizerCode, tuple]] = {}
    for code in iter_source_codes(
        source,
        n=n,
        k=k,
        equivalence=equivalence,
        max_codes=max_codes,
        encoder_depth=encoder_depth,
    ):
        raw_codes += 1
        quality = code_quality(code, constraints)
        if not quality.passes:
            continue
        codes_checked += 1
        key = entropy_key(code, max_subset_size=constraints.max_subset_size, mode=entropy_key_mode)
        reconstruction = code.reconstruction_profile()
        previous = by_entropy.get(key)
        if previous is None:
            by_entropy[key] = (code, reconstruction)
            continue
        old_code, old_reconstruction = previous
        if old_reconstruction != reconstruction:
            pair = DiscordantPair(
                n=n,
                k=k,
                entropy_profile=key,
                first=old_code,
                second=code,
                first_reconstruction_profile=old_reconstruction,
                second_reconstruction_profile=reconstruction,
            )
            return RobustScan(
                n=n,
                k=k,
                source=source,
                equivalence=equivalence,
                entropy_key_mode=entropy_key_mode,
                constraints=constraints,
                raw_codes=raw_codes,
                codes_checked=codes_checked,
                entropy_classes=len(by_entropy),
                pair=pair,
                status="pair-found",
            )

    return RobustScan(
        n=n,
        k=k,
        source=source,
        equivalence=equivalence,
        entropy_key_mode=entropy_key_mode,
        constraints=constraints,
        raw_codes=raw_codes,
        codes_checked=codes_checked,
        entropy_classes=len(by_entropy),
        pair=None,
        status="no-pair",
    )


def robust_frontier(
    *,
    max_n: int,
    k: int,
    sources: tuple[str, ...],
    equivalence: str = "permutation",
    entropy_key_mode: str = "profile",
    constraints: RobustConstraints = RobustConstraints(),
    max_codes: int | None = None,
    encoder_depth: int = 2,
    exhaustive_max_n: int = 4,
    stop_on_pair: bool = False,
) -> RobustFrontier:
    scans: list[RobustScan] = []
    for n in range(max(1, k), max_n + 1):
        for source in sources:
            if source == "exhaustive" and n > exhaustive_max_n:
                scans.append(
                    RobustScan(
                        n=n,
                        k=k,
                        source=source,
                        equivalence=equivalence,
                        entropy_key_mode=entropy_key_mode,
                        constraints=constraints,
                        raw_codes=0,
                        codes_checked=0,
                        entropy_classes=0,
                        pair=None,
                        status=f"skipped-exhaustive-n>{exhaustive_max_n}",
                    )
                )
                continue
            scan = scan_robust_source(
                n=n,
                k=k,
                source=source,
                equivalence=equivalence,
                entropy_key_mode=entropy_key_mode,
                constraints=constraints,
                max_codes=max_codes,
                encoder_depth=encoder_depth,
            )
            scans.append(scan)
            if stop_on_pair and scan.pair is not None:
                return RobustFrontier(max_n, k, sources, equivalence, entropy_key_mode, constraints, tuple(scans))
    return RobustFrontier(max_n, k, sources, equivalence, entropy_key_mode, constraints, tuple(scans))


def pauli_rows(rows: tuple[int, ...], n: int) -> tuple[str, ...]:
    return tuple(pauli_to_string(row, n) for row in rows)


def quality_summary(code: StabilizerCode, constraints: RobustConstraints) -> dict[str, object]:
    quality = code_quality(code, constraints)
    return {
        "distance": quality.distance,
        "minimal_reconstruction_size": quality.minimal_reconstruction_size,
        "has_single_qubit_noncentral_logical": quality.has_single_qubit_noncentral_logical,
        "passes": quality.passes,
        "reason": quality.reason,
        "minimal_reconstruction_regions": [
            mask_to_tuple(mask, code.n) for mask in code.reconstruction_regions(minimal=True)
        ],
    }
