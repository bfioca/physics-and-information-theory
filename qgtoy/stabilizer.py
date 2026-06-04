"""Exact stabilizer-state and stabilizer-code diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Iterable, Sequence

from .gf2 import (
    all_masks,
    in_span,
    mask_from_qubits,
    mask_to_tuple,
    masks_of_size,
    nullspace,
    quotient_basis,
    rank,
    rref,
    span_elements,
)


def pauli_from_string(text: str) -> int:
    x = 0
    z = 0
    for i, char in enumerate(text.upper()):
        if char == "I":
            continue
        if char == "X":
            x |= 1 << i
        elif char == "Z":
            z |= 1 << i
        elif char == "Y":
            x |= 1 << i
            z |= 1 << i
        else:
            raise ValueError(f"unknown Pauli character {char!r}")
    return x | (z << len(text))


def pauli_to_string(row: int, n: int) -> str:
    chars: list[str] = []
    x = row & ((1 << n) - 1)
    z = row >> n
    for i in range(n):
        xb = (x >> i) & 1
        zb = (z >> i) & 1
        chars.append(("I", "X", "Z", "Y")[(xb << 0) | (zb << 1)])
    return "".join(chars)


def symplectic_product(a: int, b: int, n: int) -> int:
    mask = (1 << n) - 1
    ax = a & mask
    az = a >> n
    bx = b & mask
    bz = b >> n
    return ((ax & bz).bit_count() + (az & bx).bit_count()) & 1


def symplectic_dual(row: int, n: int) -> int:
    mask = (1 << n) - 1
    x = row & mask
    z = row >> n
    return z | (x << n)


def support_mask(row: int, n: int) -> int:
    mask = (1 << n) - 1
    return (row & mask) | (row >> n)


def weight(row: int, n: int) -> int:
    return support_mask(row, n).bit_count()


LOCAL_CLIFFORD_MATRICES: tuple[tuple[int, int, int, int], ...] = tuple(
    (a, b, c, d)
    for a, b, c, d in product((0, 1), repeat=4)
    if (a & d) ^ (b & c)
)


def combine_rows(coefficients: int, basis: Sequence[int]) -> int:
    out = 0
    for index, row in enumerate(basis):
        if (coefficients >> index) & 1:
            out ^= row
    return out


def restrict_subspace_to_support(basis: Sequence[int], n: int, region: int) -> tuple[int, ...]:
    """Basis for elements of span(basis) whose Pauli support lies in region."""
    rows = tuple(basis)
    outside = ((1 << n) - 1) & ~region
    equations = []
    for qubit in range(n):
        if not ((outside >> qubit) & 1):
            continue
        x_equation = 0
        z_equation = 0
        for index, row in enumerate(rows):
            if (row >> qubit) & 1:
                x_equation |= 1 << index
            if (row >> (n + qubit)) & 1:
                z_equation |= 1 << index
        equations.extend((x_equation, z_equation))
    coefficient_basis = nullspace(equations, len(rows))
    return rref((combine_rows(coefficients, rows) for coefficients in coefficient_basis), 2 * n)


def permute_pauli(row: int, n: int, perm: Sequence[int]) -> int:
    """Permute qubits, where old qubit i moves to new qubit perm[i]."""
    x = row & ((1 << n) - 1)
    z = row >> n
    new_x = 0
    new_z = 0
    for old, new in enumerate(perm):
        if (x >> old) & 1:
            new_x |= 1 << new
        if (z >> old) & 1:
            new_z |= 1 << new
    return new_x | (new_z << n)


def local_clifford_pauli(row: int, n: int, maps: Sequence[tuple[int, int, int, int]]) -> int:
    """Apply phase-free single-qubit Clifford maps to a Pauli row."""
    if len(maps) != n:
        raise ValueError(f"expected {n} local Clifford maps, found {len(maps)}")
    x = row & ((1 << n) - 1)
    z = row >> n
    new_x = 0
    new_z = 0
    for qubit, (a, b, c, d) in enumerate(maps):
        xb = (x >> qubit) & 1
        zb = (z >> qubit) & 1
        if (a & xb) ^ (b & zb):
            new_x |= 1 << qubit
        if (c & xb) ^ (d & zb):
            new_z |= 1 << qubit
    return new_x | (new_z << n)


def transform_pauli(
    row: int,
    n: int,
    *,
    maps: Sequence[tuple[int, int, int, int]] | None = None,
    perm: Sequence[int] | None = None,
) -> int:
    out = local_clifford_pauli(row, n, maps) if maps is not None else row
    return permute_pauli(out, n, perm) if perm is not None else out


@dataclass(frozen=True)
class RegionAlgebra:
    region: int
    logical_basis: tuple[int, ...]
    center_basis: tuple[int, ...]
    commutant_basis: tuple[int, ...]
    logical_dim: int
    center_dim: int
    commutant_dim: int
    reconstructs_all: bool

    def signature(self) -> tuple[int, int, int, bool]:
        return (self.logical_dim, self.center_dim, self.commutant_dim, self.reconstructs_all)


@dataclass(frozen=True)
class StabilizerCode:
    """A stabilizer code without phases, represented over GF(2)."""

    n: int
    generators: tuple[int, ...]

    def __init__(self, n: int, generators: Iterable[int]):
        width = 2 * n
        gens = rref(generators, width)
        for generator in gens:
            if generator >= (1 << width):
                raise ValueError("generator exceeds Pauli width")
        for a, b in combinations(gens, 2):
            if symplectic_product(a, b, n):
                raise ValueError(f"non-commuting generators: {a}, {b}")
        object.__setattr__(self, "n", n)
        object.__setattr__(self, "generators", gens)

    @classmethod
    def from_pauli_strings(cls, strings: Sequence[str]) -> "StabilizerCode":
        if not strings:
            raise ValueError("at least one Pauli string is required")
        n = len(strings[0])
        if any(len(item) != n for item in strings):
            raise ValueError("all Pauli strings must have the same length")
        return cls(n, [pauli_from_string(item) for item in strings])

    @property
    def r(self) -> int:
        return len(self.generators)

    @property
    def k(self) -> int:
        return self.n - self.r

    @property
    def width(self) -> int:
        return 2 * self.n

    @property
    def centralizer_basis(self) -> tuple[int, ...]:
        equations = [symplectic_dual(generator, self.n) for generator in self.generators]
        return nullspace(equations, self.width)

    @property
    def logical_basis(self) -> tuple[int, ...]:
        return quotient_basis(self.centralizer_basis, self.generators, self.width)

    def stabilizer_supported_basis(self, region: int | Iterable[int]) -> tuple[int, ...]:
        mask = mask_from_qubits(region)
        return restrict_subspace_to_support(self.generators, self.n, mask)

    def centralizer_supported_basis(self, region: int | Iterable[int]) -> tuple[int, ...]:
        mask = mask_from_qubits(region)
        return restrict_subspace_to_support(self.centralizer_basis, self.n, mask)

    def entropy(self, region: int | Iterable[int]) -> int:
        """Entropy of the normalized code state P_code / dim(code), in bits."""
        mask = mask_from_qubits(region)
        local_stabilizer_dim = len(self.stabilizer_supported_basis(mask))
        return mask.bit_count() - local_stabilizer_dim

    def entropy_vector(self, *, max_subset_size: int | None = None) -> dict[tuple[int, ...], int]:
        out: dict[tuple[int, ...], int] = {}
        for mask in all_masks(self.n):
            if max_subset_size is not None and mask.bit_count() > max_subset_size:
                continue
            out[mask_to_tuple(mask, self.n)] = self.entropy(mask)
        return out

    def entropy_profile(self, *, max_subset_size: int | None = None) -> tuple[tuple[int, tuple[int, ...]], ...]:
        """Permutation-invariant entropy multiset grouped by subsystem size."""
        pieces: list[tuple[int, tuple[int, ...]]] = []
        max_size = self.n if max_subset_size is None else min(self.n, max_subset_size)
        for size in range(max_size + 1):
            entropies = sorted(self.entropy(mask) for mask in masks_of_size(self.n, size))
            pieces.append((size, tuple(entropies)))
        return tuple(pieces)

    def mutual_information(self, a: int | Iterable[int], b: int | Iterable[int]) -> int:
        am = mask_from_qubits(a)
        bm = mask_from_qubits(b)
        return self.entropy(am) + self.entropy(bm) - self.entropy(am | bm)

    def tripartite_information(
        self,
        a: int | Iterable[int],
        b: int | Iterable[int],
        c: int | Iterable[int],
    ) -> int:
        am = mask_from_qubits(a)
        bm = mask_from_qubits(b)
        cm = mask_from_qubits(c)
        return (
            self.entropy(am)
            + self.entropy(bm)
            + self.entropy(cm)
            - self.entropy(am | bm)
            - self.entropy(am | cm)
            - self.entropy(bm | cm)
            + self.entropy(am | bm | cm)
        )

    def conditional_mutual_information(
        self,
        a: int | Iterable[int],
        b: int | Iterable[int],
        c: int | Iterable[int],
    ) -> int:
        am = mask_from_qubits(a)
        bm = mask_from_qubits(b)
        cm = mask_from_qubits(c)
        return self.entropy(am | bm) + self.entropy(bm | cm) - self.entropy(bm) - self.entropy(am | bm | cm)

    def logical_subspace_supported(self, region: int | Iterable[int]) -> tuple[int, ...]:
        mask = mask_from_qubits(region)
        return quotient_basis(self.centralizer_supported_basis(mask), self.generators, self.width)

    def region_algebra(self, region: int | Iterable[int]) -> RegionAlgebra:
        mask = mask_from_qubits(region)
        reps = self.logical_subspace_supported(mask)
        logical_dim = len(reps)
        form_rows = []
        for i, left in enumerate(reps):
            row = 0
            for j, right in enumerate(reps):
                if symplectic_product(left, right, self.n):
                    row |= 1 << j
            form_rows.append(row)
        form_rank = rank(form_rows, logical_dim) if logical_dim else 0
        center_coefficients = nullspace(form_rows, logical_dim) if logical_dim else ()
        center_basis = tuple(combine_rows(coefficients, reps) for coefficients in center_coefficients)

        full_logical_basis = self.logical_basis
        full_logical_dim = 2 * self.k
        commutant_equations = []
        for region_rep in reps:
            equation = 0
            for index, logical_rep in enumerate(full_logical_basis):
                if symplectic_product(logical_rep, region_rep, self.n):
                    equation |= 1 << index
            commutant_equations.append(equation)
        commutant_coefficients = nullspace(commutant_equations, full_logical_dim) if full_logical_dim else ()
        commutant_basis = tuple(
            combine_rows(coefficients, full_logical_basis) for coefficients in commutant_coefficients
        )

        return RegionAlgebra(
            region=mask,
            logical_basis=reps,
            center_basis=center_basis,
            commutant_basis=commutant_basis,
            logical_dim=logical_dim,
            center_dim=len(center_basis),
            commutant_dim=len(commutant_basis),
            reconstructs_all=logical_dim == full_logical_dim,
        )

    def reconstructs_all_logicals(self, region: int | Iterable[int]) -> bool:
        return self.region_algebra(region).reconstructs_all

    def erasure_correctable(self, erasure: int | Iterable[int]) -> bool:
        return len(self.logical_subspace_supported(erasure)) == 0

    def erasure_threshold(self) -> int:
        threshold = 0
        for size in range(self.n + 1):
            if all(self.erasure_correctable(mask) for mask in masks_of_size(self.n, size)):
                threshold = size
            else:
                break
        return threshold

    def reconstruction_regions(self, *, minimal: bool = False) -> tuple[int, ...]:
        regions = [mask for mask in all_masks(self.n) if self.reconstructs_all_logicals(mask)]
        if not minimal:
            return tuple(regions)
        minimal_regions = []
        for region in regions:
            if not any(other != region and other & region == other for other in regions):
                minimal_regions.append(region)
        return tuple(minimal_regions)

    def reconstruction_profile(self) -> tuple[tuple[int, tuple[tuple[int, int, int, bool], ...]], ...]:
        pieces = []
        for size in range(self.n + 1):
            signatures = sorted(self.region_algebra(mask).signature() for mask in masks_of_size(self.n, size))
            pieces.append((size, tuple(signatures)))
        return tuple(pieces)

    def distance(self) -> int | None:
        if self.k == 0:
            return None
        best: int | None = None
        for row in span_elements(self.centralizer_basis):
            if row == 0 or in_span(row, self.generators, self.width):
                continue
            row_weight = weight(row, self.n)
            if best is None or row_weight < best:
                best = row_weight
        return best

    def canonical_under_qubit_permutations(self) -> tuple[int, ...]:
        from itertools import permutations

        candidates = []
        for perm in permutations(range(self.n)):
            candidates.append(rref((permute_pauli(row, self.n, perm) for row in self.generators), self.width))
        return min(candidates)

    def canonical_under_local_cliffords(self, *, include_permutations: bool = True) -> tuple[int, ...]:
        from itertools import permutations

        permutations_to_try = tuple(permutations(range(self.n))) if include_permutations else (None,)
        candidates = []
        for maps in product(LOCAL_CLIFFORD_MATRICES, repeat=self.n):
            locally_mapped = tuple(local_clifford_pauli(row, self.n, maps) for row in self.generators)
            for perm in permutations_to_try:
                if perm is None:
                    candidates.append(rref(locally_mapped, self.width))
                else:
                    candidates.append(rref((permute_pauli(row, self.n, perm) for row in locally_mapped), self.width))
        return min(candidates)

    def canonical_key(self, equivalence: str = "local-clifford") -> tuple[int, ...]:
        if equivalence == "none":
            return self.generators
        if equivalence == "permutation":
            return self.canonical_under_qubit_permutations()
        if equivalence == "local-clifford":
            return self.canonical_under_local_cliffords()
        raise ValueError(f"unknown code equivalence {equivalence!r}")

    def pauli_generators(self) -> tuple[str, ...]:
        return tuple(pauli_to_string(row, self.n) for row in self.generators)


class StabilizerState(StabilizerCode):
    """A pure stabilizer state."""

    def __init__(self, n: int, generators: Iterable[int]):
        super().__init__(n, generators)
        if self.k != 0:
            raise ValueError(f"expected {n} independent generators for a state, found {self.r}")
