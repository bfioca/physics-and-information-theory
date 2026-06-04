"""Enumeration and search helpers for small stabilizer-code toy universes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from .gf2 import rref
from .stabilizer import StabilizerCode, symplectic_product

CODE_EQUIVALENCES = ("none", "permutation", "local-clifford")


def enumerate_stabilizer_codes(
    n: int,
    *,
    k: int,
    equivalence: str = "permutation",
    max_codes: int | None = None,
) -> Iterator[StabilizerCode]:
    """Enumerate small stabilizer codes by isotropic generator rowspaces."""
    if equivalence not in CODE_EQUIVALENCES:
        raise ValueError(f"equivalence must be one of {CODE_EQUIVALENCES}")
    if k < 0 or k > n:
        raise ValueError("k must satisfy 0 <= k <= n")

    r = n - k
    if r == 0:
        yield StabilizerCode(n, [])
        return

    width = 2 * n
    paulis = tuple(range(1, 1 << width))
    partials: set[tuple[int, ...]] = {()}
    for _ in range(r):
        next_partials: set[tuple[int, ...]] = set()
        for basis in partials:
            for row in paulis:
                if any(symplectic_product(row, old, n) for old in basis):
                    continue
                new_basis = rref((*basis, row), width)
                if len(new_basis) == len(basis) + 1:
                    next_partials.add(new_basis)
        partials = next_partials

    emitted: set[tuple[int, ...]] = set()
    count = 0
    for basis in sorted(partials):
        code = StabilizerCode(n, basis)
        key = code.canonical_key(equivalence)
        if key in emitted:
            continue
        emitted.add(key)
        yield code
        count += 1
        if max_codes is not None and count >= max_codes:
            return


@dataclass(frozen=True)
class DiscordantPair:
    n: int
    k: int
    entropy_profile: tuple
    first: StabilizerCode
    second: StabilizerCode
    first_reconstruction_profile: tuple
    second_reconstruction_profile: tuple


@dataclass(frozen=True)
class SearchScan:
    n: int
    k: int
    equivalence: str
    max_subset_size: int | None
    min_distance: int | None
    codes_checked: int
    entropy_classes: int
    pair: DiscordantPair | None


@dataclass(frozen=True)
class SearchCertificate:
    max_n: int
    k: int
    equivalence: str
    max_subset_size: int | None
    min_distance: int | None
    scans: tuple[SearchScan, ...]

    @property
    def pair(self) -> DiscordantPair | None:
        for scan in self.scans:
            if scan.pair is not None:
                return scan.pair
        return None


def scan_entropy_reconstruction_discordance(
    *,
    n: int,
    k: int,
    equivalence: str = "permutation",
    max_subset_size: int | None = None,
    max_codes_per_n: int | None = None,
    min_distance: int | None = None,
) -> SearchScan:
    """Scan one n for the first entropy-matched reconstruction/algebra mismatch."""
    by_entropy: dict[tuple, tuple[StabilizerCode, tuple]] = {}
    codes_checked = 0
    for code in enumerate_stabilizer_codes(n, k=k, equivalence=equivalence, max_codes=max_codes_per_n):
        distance = code.distance()
        if min_distance is not None and (distance is None or distance < min_distance):
            continue
        codes_checked += 1
        entropy = code.entropy_profile(max_subset_size=max_subset_size)
        reconstruction = code.reconstruction_profile()
        previous = by_entropy.get(entropy)
        if previous is None:
            by_entropy[entropy] = (code, reconstruction)
            continue
        old_code, old_reconstruction = previous
        if old_reconstruction != reconstruction:
            pair = DiscordantPair(
                n=n,
                k=k,
                entropy_profile=entropy,
                first=old_code,
                second=code,
                first_reconstruction_profile=old_reconstruction,
                second_reconstruction_profile=reconstruction,
            )
            return SearchScan(
                n=n,
                k=k,
                equivalence=equivalence,
                max_subset_size=max_subset_size,
                min_distance=min_distance,
                codes_checked=codes_checked,
                entropy_classes=len(by_entropy),
                pair=pair,
            )

    return SearchScan(
        n=n,
        k=k,
        equivalence=equivalence,
        max_subset_size=max_subset_size,
        min_distance=min_distance,
        codes_checked=codes_checked,
        entropy_classes=len(by_entropy),
        pair=None,
    )


def certify_minimal_entropy_reconstruction_discordance(
    *,
    max_n: int,
    k: int,
    equivalence: str = "permutation",
    max_subset_size: int | None = None,
    max_codes_per_n: int | None = None,
    min_distance: int | None = None,
) -> SearchCertificate:
    """Scan n increasingly and stop at the first discordant pair."""
    scans: list[SearchScan] = []
    for n in range(max(1, k), max_n + 1):
        scan = scan_entropy_reconstruction_discordance(
            n=n,
            k=k,
            equivalence=equivalence,
            max_subset_size=max_subset_size,
            max_codes_per_n=max_codes_per_n,
            min_distance=min_distance,
        )
        scans.append(scan)
        if scan.pair is not None:
            break
    return SearchCertificate(
        max_n=max_n,
        k=k,
        equivalence=equivalence,
        max_subset_size=max_subset_size,
        min_distance=min_distance,
        scans=tuple(scans),
    )


def find_entropy_reconstruction_discordant_pairs(
    *,
    max_n: int,
    k: int,
    equivalence: str = "permutation",
    max_subset_size: int | None = None,
    max_codes_per_n: int | None = None,
    min_distance: int | None = None,
) -> Iterator[DiscordantPair]:
    """Find codes whose entropy profile matches but reconstruction/algebra differs."""
    for n in range(max(1, k), max_n + 1):
        by_entropy: dict[tuple, tuple[StabilizerCode, tuple]] = {}
        for code in enumerate_stabilizer_codes(n, k=k, equivalence=equivalence, max_codes=max_codes_per_n):
            distance = code.distance()
            if min_distance is not None and (distance is None or distance < min_distance):
                continue
            entropy = code.entropy_profile(max_subset_size=max_subset_size)
            reconstruction = code.reconstruction_profile()
            previous = by_entropy.get(entropy)
            if previous is None:
                by_entropy[entropy] = (code, reconstruction)
                continue
            old_code, old_reconstruction = previous
            if old_reconstruction != reconstruction:
                yield DiscordantPair(
                    n=n,
                    k=k,
                    entropy_profile=entropy,
                    first=old_code,
                    second=code,
                    first_reconstruction_profile=old_reconstruction,
                    second_reconstruction_profile=reconstruction,
                )
