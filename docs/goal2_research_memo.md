# Goal 2 Research Memo: Finite Causal-Patch / Horizon-Code Toy Models

This memo consolidates the verified results through Phase 31. The point of the
project is not to model de Sitter space literally. The point is to build exact,
finite QEC toy cosmologies where entropy-visible data, observer patch
reconstructability, erasure semantics, and channel dynamics can be computed and
compared without numerical guesswork.

## Definitions

- **Stabilizer code**: an `n`-qubit stabilizer subspace, represented by Pauli
  generators. The verifier computes logical basis, distance, entropy vectors,
  region algebras, erasure correctability, and exact rank-kernel diagnostics.
- **Code pair**: two stabilizer codes, usually with the same `n` and `k`, used
  to compare entropy diagnostics against reconstruction and operator-algebra
  diagnostics.
- **Patch cover**: a finite list of named physical-qubit regions attached to a
  code or code pair.
- **Observer patch**: a named cover region interpreted as an observer causal
  patch, typically `observer_p` or `observer_q`.
- **Shared horizon**: the overlap region `observer_p & observer_q`, required by
  strict cover gates to equal the named `shared_horizon`.
- **Bridge shell**: the collection of bridge-pair qubits added by the
  balanced-bridge construction.
- **Static diamond**: the causal union `observer_p union observer_q`.
- **Causal-patch entropy profile**: named patch entropies plus overlap data,
  mutual information, conditional mutual information, and tripartite
  information for patch pairs.
- **Observer algebra signature**: the tuple `(logical_dim, center_dim,
  commutant_dim, reconstructs_all)` for the logical operator algebra supported
  on a region.
- **Erasure-correctability profile**: named erasure scenarios recording whether
  the erased region is correctable for each code.
- **Survivor fixed point**: for an erasure scenario, whether the survivor
  complement reconstructs all logicals. The certificates check the QEC identity:
  erased region correctable iff survivor complement reconstructs all logicals.
- **Strict causal-patch gate**: the full hit condition requiring matching named
  entropy/overlap data, observer overlap equal to the horizon, matching
  shared-horizon algebra, different observer reconstruction, matching
  erasure-correctability profiles, and an erasure-algebra difference.
- **Channel-rule substrate**: a certified transition graph or edge-filtered
  subgraph on scored toy-cosmology states, used as the support for exact
  rational Markov/channel rules.

## Main Theorem From Goal 1

The balanced-bridge CSS family gives code pairs `(A_m, B_m)` with
`n = 6 + 2m`, `k = 1`, and `d = 2`. Starting from the `n=6` CSS seed pair,
bridge `j` adds qubits `p_j = 6 + 2j`, `q_j = 7 + 2j` and the same two checks
to both codes:

```text
Z_1 Z_2 Z_{p_j} Z_{q_j}
X_0 X_5 X_{p_j} X_{q_j}
```

For all `m`, the family has matching labeled one- and two-qubit entropy
diagnostics, no single-qubit non-central logical reconstruction, and distinct
reconstruction/algebra profiles. The separating region is
`R_m = {1,2,3} union {p_j}`. On `R_m`, `A_m` has algebra signature
`(1,1,1,false)`, while `B_m` has `(2,0,0,true)`.

This is theorem-level: the independent `bridge-proof-check` command derives
the restricted-rank cases from CSS generator templates, and the exact prefix
verifier cross-checks finite instances.

## Main Static Goal 2 Result

The balanced-bridge causal-patch atlas uses:

```text
observer_p     = {1,2,3} union {p_j}
observer_q     = {1,2,3} union {q_j}
shared_horizon = {1,2,3}
bridge_shell   = all bridge qubits
static_diamond = observer_p union observer_q
```

For checked finite prefixes, the atlas gives matching named patch entropy,
overlap, mutual information, conditional mutual information, and tripartite
information data. It also gives matching shared-horizon algebra. Nevertheless,
observer patch reconstructability differs: the same named observer patches see
only a central logical in `A_m`, but reconstruct the full logical algebra in
`B_m`.

This is an exact finite certificate for the checked prefixes and is backed by
the all-`m` balanced-bridge theorem for the entropy/reconstruction mechanism.

## Dynamics Result

Deterministic bridge growth is an exact time rule `m -> m+1`: append
`p_m,q_m`, assign `p_m` to `observer_p`, assign `q_m` to `observer_q`, and keep
the shared horizon fixed. The certificates verify exact increment laws:

- observer entropy increments by `1`;
- observer-pair mutual information increments by `2`;
- private conditional mutual information increments by `2`;
- tripartite information stays fixed;
- witness algebra signatures remain separated;
- named erasure profiles remain matched between the paired codes.

This is an exact finite certificate over the requested bridge-growth prefix,
with formulas matching the balanced-bridge construction.

## Source/Cover Robustness Result

Generic bounded covers recover the seed separation but fail on lifted
balanced-bridge slices. Source-aware bridge atlases recover the lifted family.
The lesson is that causal-patch semantics are source-aware, not arbitrary subset
semantics: the same code pair may require an atlas tied to its construction
before entropy-overlap and reconstruction diagnostics align as causal patches.

The strongest claim here is exact finite evidence over bounded cover grammars
and source frontiers, including replayable frontier-cache artifacts. It is not
a theorem over all possible covers.

## Repaired Non-CSS Result

Graph/CWS-like examples repaired by outer-code concatenation show that
low-order entropy matching, distance repair, and strict causal-patch erasure
semantics are separable constraints. Phase 11 repairs distance and preserves
low-order entropy matching, but simple lifted atlases do not satisfy the full
strict causal-patch gate. Phase 12 recovers strict hits using atlas-aware
covers: shared outer blocks keep the inner observer overlap, while private
outer blocks are promoted to complete inner blocks.

This is exact finite evidence for a repaired non-CSS toy family. It establishes
that role labels alone are not geometry: the erasure channel and operator
algebra must certify the semantics.

## Channel And Co-Design Result

The transition-graph phases build exact finite substrates and exact rational
channel rules. The mixed inner/outer graph has 49 nodes, 84 certified edges,
and stable shared-horizon correctability/fixed-point semantics. Exact Markov
channels on this graph show that stationary bucket weights, absorbing classes,
target signs, Pareto frontiers, and rule witnesses depend on transition rules
and substrates.

The robust rule-language phases certify a bounded family of 27 positive
symmetric edge-bonus weighted walks over four substrates. Some target signs are
robust on the all-filter substrate family; others flip when substrates or covers
are changed. Throughout the chosen flows, the repaired shared-horizon
correctability and survivor fixed point remain stable.

This is exact finite certificate and exact exhaustive bounded-search evidence,
not a universal theorem about arbitrary dynamics.

## Phase 31 Strict-Cover Audit

Phase 31 exhausts the Phase 12 private-full/shared-inner repaired-cover family
under the strict causal-patch gate:

- 175 ordered overlapping block-mask covers scanned;
- 66 raw entropy/reconstruction/horizon hits;
- 8 strict repaired-cover hits;
- 58 raw hits rejected by the erasure-correctability-profile gate.

For each strict cover, the verifier rebuilds the mixed transition graph,
applies the four channel-rule substrates, recomputes all 27 robust channel
rules, and audits feature predicates by exact enumeration.

The strict-cover no-go is:

```text
entropy_break - full_semantics < 0
```

for all eight strict covers in this bounded family. The best exact worst-case
gap is still negative: `-1/53`.

Operator-related sign flips are exactly classified by the private-block
pattern. The four strict covers with nonempty `observer_p_private_blocks` flip
both:

```text
operator_collapse - full_semantics
operator_collapse - entropy_break
```

with extrema `3/70` and `19/284`, respectively. The four strict covers with
empty `observer_p_private_blocks` preserve the baseline operator signs.

## Claim Status Table

| Result | Status | Scope |
| --- | --- | --- |
| Balanced-bridge CSS family | Exact theorem | All bridge counts `m` under the generator rule |
| Static balanced-bridge causal-patch atlas | Exact finite certificate plus theorem-backed mechanism | Checked prefixes, source-aware atlas |
| Deterministic bridge growth laws | Exact finite certificate | Checked growth prefix |
| Generic-vs-source-aware cover behavior | Exact bounded-search evidence | Enumerated bounded cover grammars/frontier records |
| Repaired non-CSS atlas recovery | Exact finite certificate and bounded-search evidence | Phase 11/12 repaired graph/CWS-like sources |
| Mixed transition graphs and rational channels | Exact finite certificates | Certified finite graphs and rational rules |
| Robust channel-rule synthesis | Exact exhaustive bounded search | 27 rules, four substrates, fixed transition family |
| Phase 31 strict-cover audit | Exact exhaustive bounded search | 175-cover repaired family and eight strict hits |
| Extended frontier/cache exploration | Exploratory frontier evidence | Bounded CSS/graph/encoder source records |

## Command Index

- `python3 -m qgtoy bridge-proof-check`: independent symbolic checker for the
  balanced-bridge CSS theorem.
- `python3 -m qgtoy bridge-theorem`: theorem-style balanced-bridge package with
  symbolic and exact-prefix artifacts.
- `python3 -m qgtoy cosmology-phase1 --max-m 3`: static causal-patch atlas.
- `python3 -m qgtoy cosmology-phase2 --max-m 3`: deterministic bridge growth
  and exact erasure probes.
- `python3 -m qgtoy cosmology-phase6`: source-aware bridge atlas recovery for
  lifted sources.
- `python3 -m qgtoy cosmology-phase12`: atlas-aware repaired non-CSS strict hit.
- `python3 -m qgtoy cosmology-phase13`: repaired cover dynamics and CSS/non-CSS
  channel-semantics comparison.
- `python3 -m qgtoy cosmology-phase21`: mixed inner/outer transition graph.
- `python3 -m qgtoy cosmology-phase22`: exact rational time/channel dynamics.
- `python3 -m qgtoy cosmology-phase24`: bounded channel-rule search.
- `python3 -m qgtoy cosmology-phase27`: robust channel synthesis over four
  substrates.
- `python3 -m qgtoy cosmology-phase28`: audited rule-language proof layer.
- `python3 -m qgtoy cosmology-phase31`: strict-cover exhaustive audit.

## Limitations

These are small finite stabilizer/CSS/non-CSS toy models, mostly with `k=1`.
The cover grammars, source families, transition graphs, and channel rules are
bounded. Role labels are not physical geometry by themselves. The de
Sitter/ER=EPR analogy is diagnostic rather than literal. Entropy matching is
limited to the specified named patches or low-order diagnostics, not the full
entropy vector unless explicitly stated.

## Next Research Directions

1. Move to tensor-network or holographic-code extensions where region inclusion
   and reconstruction maps have more geometric structure.
2. Search for `d >= 3` analogues of the balanced-bridge separation.
3. Translate the current result package into a short paper-style note with
   theorem statements, proof sketches, certificate schemas, and reproducibility
   commands.
