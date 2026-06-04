"""Small GF(2) linear algebra helpers using Python integers as bit vectors."""

from __future__ import annotations

from itertools import combinations
from typing import Iterable, Iterator, Sequence


def parity(x: int) -> int:
    return x.bit_count() & 1


def rref(rows: Iterable[int], width: int) -> tuple[int, ...]:
    """Return a canonical row-reduced basis over GF(2)."""
    basis = sorted({row for row in rows if row})
    pivot_row = 0

    for col in range(width - 1, -1, -1):
        pivot = None
        for i in range(pivot_row, len(basis)):
            if (basis[i] >> col) & 1:
                pivot = i
                break
        if pivot is None:
            continue

        basis[pivot_row], basis[pivot] = basis[pivot], basis[pivot_row]
        for i in range(len(basis)):
            if i != pivot_row and ((basis[i] >> col) & 1):
                basis[i] ^= basis[pivot_row]
        pivot_row += 1

    return tuple(row for row in basis[:pivot_row] if row)


def rank(rows: Iterable[int], width: int) -> int:
    return len(rref(rows, width))


def pivot_columns(rows: Sequence[int]) -> tuple[int, ...]:
    return tuple(row.bit_length() - 1 for row in rows)


def in_span(row: int, basis: Iterable[int], width: int) -> bool:
    if row == 0:
        return True
    reduced = rref(basis, width)
    return rank((*reduced, row), width) == len(reduced)


def nullspace(equations: Iterable[int], width: int) -> tuple[int, ...]:
    """Basis for vectors v with equation dot products e.v = 0 over GF(2)."""
    rows = rref(equations, width)
    pivots = set(pivot_columns(rows))
    free_columns = [col for col in range(width) if col not in pivots]
    basis: list[int] = []

    for free in free_columns:
        vec = 1 << free
        for row in rows:
            pivot = row.bit_length() - 1
            rest = row & ~(1 << pivot)
            if parity(rest & vec):
                vec |= 1 << pivot
        basis.append(vec)

    return rref(basis, width)


def span_elements(basis: Sequence[int]) -> Iterator[int]:
    """Yield all vectors in the span of a small basis."""
    elements = [0]
    for row in basis:
        elements += [existing ^ row for existing in elements]
    yield from elements


def quotient_basis(subspace: Iterable[int], modspace: Iterable[int], width: int) -> tuple[int, ...]:
    """Represent a basis of (modspace + subspace) / modspace by subspace rows."""
    current = list(rref(modspace, width))
    out: list[int] = []
    current_rank = len(current)

    for row in rref(subspace, width):
        new_basis = rref((*current, row), width)
        if len(new_basis) > current_rank:
            out.append(row)
            current = list(new_basis)
            current_rank += 1

    return tuple(out)


def all_masks(n: int, *, include_empty: bool = True) -> Iterator[int]:
    start = 0 if include_empty else 1
    yield from range(start, 1 << n)


def masks_of_size(n: int, size: int) -> Iterator[int]:
    for combo in combinations(range(n), size):
        mask = 0
        for bit in combo:
            mask |= 1 << bit
        yield mask


def mask_from_qubits(qubits: int | Iterable[int]) -> int:
    if isinstance(qubits, int):
        return qubits
    mask = 0
    for qubit in qubits:
        mask |= 1 << qubit
    return mask


def mask_to_tuple(mask: int, n: int) -> tuple[int, ...]:
    return tuple(i for i in range(n) if (mask >> i) & 1)
