"""Structured stabilizer-code generators for robust searches."""

from __future__ import annotations

from itertools import combinations
from typing import Callable, Iterator

from .gf2 import in_span, parity, rref
from .graphs import enumerate_graph_state_reps
from .stabilizer import StabilizerCode


def enumerate_binary_subspaces(n: int, dim: int) -> Iterator[tuple[int, ...]]:
    """Enumerate dim-dimensional subspaces of GF(2)^n by canonical RREF bases."""
    if dim < 0 or dim > n:
        return
    if dim == 0:
        yield ()
        return

    vectors = tuple(range(1, 1 << n))
    partials: set[tuple[int, ...]] = {()}
    for _ in range(dim):
        next_partials: set[tuple[int, ...]] = set()
        for basis in partials:
            for vector in vectors:
                new_basis = rref((*basis, vector), n)
                if len(new_basis) == len(basis) + 1:
                    next_partials.add(new_basis)
        partials = next_partials
    yield from sorted(partials)


def cyclic_shift_bits(row: int, n: int) -> int:
    mask = (1 << n) - 1
    return ((row << 1) & mask) | (row >> (n - 1))


def is_cyclic_subspace(basis: tuple[int, ...], n: int) -> bool:
    return all(in_span(cyclic_shift_bits(row, n), basis, n) for row in basis)


def css_generators(x_checks: tuple[int, ...], z_checks: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(x_checks) + tuple(row << n for row in z_checks)


def enumerate_css_codes(
    n: int,
    *,
    k: int,
    equivalence: str = "permutation",
    cyclic: bool = False,
    max_codes: int | None = None,
) -> Iterator[StabilizerCode]:
    """Enumerate CSS stabilizer codes Hx Hz^T = 0 with r_x + r_z = n-k."""
    r = n - k
    if r < 0:
        return

    subspaces_by_dim: dict[int, tuple[tuple[int, ...], ...]] = {}
    emitted: set[tuple[int, ...]] = set()
    count = 0

    for x_dim in range(r + 1):
        z_dim = r - x_dim
        if x_dim not in subspaces_by_dim:
            subspaces_by_dim[x_dim] = tuple(enumerate_binary_subspaces(n, x_dim))
        if z_dim not in subspaces_by_dim:
            subspaces_by_dim[z_dim] = tuple(enumerate_binary_subspaces(n, z_dim))

        x_subspaces = subspaces_by_dim[x_dim]
        z_subspaces = subspaces_by_dim[z_dim]
        if cyclic:
            x_subspaces = tuple(space for space in x_subspaces if is_cyclic_subspace(space, n))
            z_subspaces = tuple(space for space in z_subspaces if is_cyclic_subspace(space, n))

        for x_checks in x_subspaces:
            for z_checks in z_subspaces:
                if any(parity(x_row & z_row) for x_row in x_checks for z_row in z_checks):
                    continue
                code = StabilizerCode(n, css_generators(x_checks, z_checks, n))
                key = code.canonical_key(equivalence)
                if key in emitted:
                    continue
                emitted.add(key)
                yield code
                count += 1
                if max_codes is not None and count >= max_codes:
                    return


def enumerate_graph_subspace_codes(
    n: int,
    *,
    k: int,
    equivalence: str = "permutation",
    max_codes: int | None = None,
) -> Iterator[StabilizerCode]:
    """Enumerate additive graph/CWS-like codes by deleting k graph-state checks."""
    r = n - k
    if r < 0:
        return

    emitted: set[tuple[int, ...]] = set()
    count = 0
    for _, state in enumerate_graph_state_reps(n, local_clifford=True):
        for keep in combinations(range(n), r):
            code = StabilizerCode(n, [state.generators[index] for index in keep])
            key = code.canonical_key(equivalence)
            if key in emitted:
                continue
            emitted.add(key)
            yield code
            count += 1
            if max_codes is not None and count >= max_codes:
                return


def apply_h(row: int, n: int, qubit: int) -> int:
    x_bit = (row >> qubit) & 1
    z_bit = (row >> (n + qubit)) & 1
    if x_bit == z_bit:
        return row
    out = row
    out ^= 1 << qubit
    out ^= 1 << (n + qubit)
    return out


def apply_s(row: int, n: int, qubit: int) -> int:
    if (row >> qubit) & 1:
        return row ^ (1 << (n + qubit))
    return row


def apply_cx(row: int, n: int, control: int, target: int) -> int:
    out = row
    if (row >> control) & 1:
        out ^= 1 << target
    if (row >> (n + target)) & 1:
        out ^= 1 << (n + control)
    return out


def encoder_gates(n: int) -> tuple[tuple[str, Callable[[int], int]], ...]:
    gates: list[tuple[str, Callable[[int], int]]] = []
    for qubit in range(n):
        gates.append((f"H{qubit}", lambda row, q=qubit: apply_h(row, n, q)))
        gates.append((f"S{qubit}", lambda row, q=qubit: apply_s(row, n, q)))
    for control in range(n):
        for target in range(n):
            if control != target:
                gates.append((f"CX{control}->{target}", lambda row, c=control, t=target: apply_cx(row, n, c, t)))
    return tuple(gates)


def enumerate_shallow_encoder_codes(
    n: int,
    *,
    k: int,
    max_depth: int,
    equivalence: str = "permutation",
    max_codes: int | None = None,
) -> Iterator[StabilizerCode]:
    """Enumerate codes from shallow H/S/CX encoder circuits on a trivial [[n,k]] code."""
    if k < 0 or k > n:
        return

    base = rref((1 << (n + qubit) for qubit in range(k, n)), 2 * n)
    gates = encoder_gates(n)
    frontier = {base}
    seen_raw = {base}
    emitted: set[tuple[int, ...]] = set()
    count = 0

    for depth in range(max_depth + 1):
        next_frontier: set[tuple[int, ...]] = set()
        for basis in sorted(frontier):
            code = StabilizerCode(n, basis)
            key = code.canonical_key(equivalence)
            if key not in emitted:
                emitted.add(key)
                yield code
                count += 1
                if max_codes is not None and count >= max_codes:
                    return
            if depth == max_depth:
                continue
            for _, gate in gates:
                new_basis = rref((gate(row) for row in basis), 2 * n)
                if new_basis not in seen_raw:
                    seen_raw.add(new_basis)
                    next_frontier.add(new_basis)
        frontier = next_frontier
