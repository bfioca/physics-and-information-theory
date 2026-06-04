"""Graph-state generation and local-Clifford canonicalization."""

from __future__ import annotations

from itertools import permutations
from typing import Iterator, Sequence

from .stabilizer import StabilizerState


def edge_pairs(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((i, j) for i in range(n) for j in range(i + 1, n))


def edge_mask_from_edges(n: int, edges: Sequence[tuple[int, int]]) -> int:
    pairs = edge_pairs(n)
    index = {pair: bit for bit, pair in enumerate(pairs)}
    mask = 0
    for a, b in edges:
        pair = (a, b) if a < b else (b, a)
        mask |= 1 << index[pair]
    return mask


def has_edge(edge_mask: int, n: int, a: int, b: int) -> bool:
    if a == b:
        return False
    pair = (a, b) if a < b else (b, a)
    return bool((edge_mask >> edge_pairs(n).index(pair)) & 1)


def neighbors(edge_mask: int, n: int, vertex: int) -> tuple[int, ...]:
    return tuple(other for other in range(n) if has_edge(edge_mask, n, vertex, other))


def local_complement(edge_mask: int, n: int, vertex: int) -> int:
    pairs = edge_pairs(n)
    pair_index = {pair: bit for bit, pair in enumerate(pairs)}
    out = edge_mask
    nbrs = neighbors(edge_mask, n, vertex)
    for i, a in enumerate(nbrs):
        for b in nbrs[i + 1 :]:
            pair = (a, b) if a < b else (b, a)
            out ^= 1 << pair_index[pair]
    return out


def permute_graph(edge_mask: int, n: int, perm: Sequence[int]) -> int:
    pairs = edge_pairs(n)
    pair_index = {pair: bit for bit, pair in enumerate(pairs)}
    out = 0
    for bit, (a, b) in enumerate(pairs):
        if (edge_mask >> bit) & 1:
            na = perm[a]
            nb = perm[b]
            pair = (na, nb) if na < nb else (nb, na)
            out |= 1 << pair_index[pair]
    return out


def canonical_under_permutations(edge_mask: int, n: int) -> int:
    return min(permute_graph(edge_mask, n, perm) for perm in permutations(range(n)))


def lc_orbit(edge_mask: int, n: int) -> tuple[int, ...]:
    seen = {edge_mask}
    frontier = [edge_mask]
    while frontier:
        current = frontier.pop()
        for vertex in range(n):
            nxt = local_complement(current, n, vertex)
            if nxt not in seen:
                seen.add(nxt)
                frontier.append(nxt)
    return tuple(sorted(seen))


def canonical_lc(edge_mask: int, n: int) -> int:
    return min(canonical_under_permutations(graph, n) for graph in lc_orbit(edge_mask, n))


def graph_state(edge_mask: int, n: int) -> StabilizerState:
    generators = []
    for vertex in range(n):
        x = 1 << vertex
        z = 0
        for nbr in neighbors(edge_mask, n, vertex):
            z |= 1 << nbr
        generators.append(x | (z << n))
    return StabilizerState(n, generators)


def enumerate_graph_state_reps(n: int, *, local_clifford: bool = True) -> Iterator[tuple[int, StabilizerState]]:
    total_edges = n * (n - 1) // 2
    seen: set[int] = set()
    for edge_mask in range(1 << total_edges):
        canonical = canonical_lc(edge_mask, n) if local_clifford else canonical_under_permutations(edge_mask, n)
        if canonical in seen:
            continue
        seen.add(canonical)
        yield canonical, graph_state(canonical, n)
