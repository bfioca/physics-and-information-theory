# Goal 4 Observer Algebra Tomography Memo

## Claim

Goal 4 reframes the Goals 1-3 arc as observer algebra tomography:

```text
observer entropy does not determine observer physics;
the missing finite data are observer algebra and channel semantics.
```

The exact theorem-style result is an Observer Entropy Non-Identifiability
Theorem for the balanced-bridge observer-code family. For every bridge count
`m` in the family, the two realizations `A_m,B_m` agree on the declared
observer entropy shadow: named patch entropy, observer overlap, shared horizon,
MI/CMI/I3, shared-horizon algebra, erasure correctability, and survivor
fixed-point booleans. They nevertheless have non-isomorphic observer
reconstruction algebras and different erasure-channel algebra semantics.

## Objects

The finite OA-QEC object is a stabilizer code plus an observer atlas:

- `observer_p` and `observer_q` are finite causal-patch regions;
- `shared_horizon` is their overlap;
- `bridge_shell` is the private horizon shell;
- `static_diamond` is the observer union.

For a region `R`, the observer algebra is the finite region algebra computed
from supported logical quotient classes. Its signature is:

```text
(logical_dim, center_dim, commutant_dim, reconstructs_all)
```

## Tomography Tiers

The Goal 4 certificate compares increasingly rich finite shadows:

| Tier | Result on the balanced-bridge family |
| --- | --- |
| Entropy/horizon shadow | Agrees, but observer algebra differs. |
| Plus erasure correctability / survivor fixed-point shadow | Still agrees, but observer algebra and channel algebra differ. |
| Plus observer center profile | Separates the representative family prefix. |
| Plus observer commutant profile | Also separates. |
| Plus logical-probe response | Also separates. |
| Full observer algebra profile | Separates by definition. |

Thus entropy/horizon/min-cut-like shadows are not enough. The first positive
boundary in the certified prefix is observer center data. This is bounded
evidence for a tomography hierarchy, not a universal completeness theorem.

## Exact Positive Boundary

There is also an exact `k=1` all-region completion lemma. For any finite
stabilizer code with one logical qubit, the all-region erasure-correctability
shadow plus all-region survivor fixed-point booleans determines every
all-region observer-algebra signature.

The reason is finite and algebraic: the logical quotient is a two-dimensional
symplectic vector space. For a region `R`, erasure correctability says the
region supports zero logical directions; the survivor fixed-point row for the
complement says whether `R` reconstructs all logicals. If neither is true, the
region supports exactly one logical direction. Those three cases force the
signatures `(0,0,2,false)`, `(2,0,0,true)`, and `(1,1,1,false)`.

This does not rescue entropy-only tomography, and it does not apply to named
observer atlases or `k>1` codes without extra hypotheses. It is the first clean
positive boundary: all-region `k=1` channel data are complete for region-algebra
signatures, while named-patch entropy/horizon shadows remain incomplete.

## Bounded Positive-Boundary Scan

The `observer-tomography` certificate also runs an exact all-region bounded
scan over stabilizer-code representatives with `n <= 4`, `k=1`, and permutation
deduplication. In that scan, labeled low-order entropy has a non-identifying
collision at `n=4`: two codes share the low-order entropy shadow while their
all-region algebra profiles differ. Adding all-region erasure/fixed-point data
has no collision in this bounded search space, as predicted by the exact `k=1`
completion lemma.

This does not contradict the balanced-bridge result. The bridge theorem uses a
named observer atlas and shows that the named observer entropy/horizon/erasure
shadow is incomplete. The bounded scan asks a different, stronger tomography
question using all-region erasure/fixed-point data.

## Relation To Goals 1-3

Goal 1 gives the balanced-bridge CSS seed: matching labeled low-order entropy,
different reconstruction algebra. Goal 2 names observer patches and horizons,
then adds erasure and channel semantics. Goal 3 adds a finite holographic-code
cousin where entropy and finite min-cut diagnostics agree while reconstruction
and channel-visible diagnostics differ.

Goal 4 packages the shared lesson as a diagnostic question: which finite data
determine an observer's effective quantum theory?

## Harlow-Facing Interpretation

In closed-universe observer language, `S_Ob` can set a size scale, but it does
not specify which quantum mechanics the observer gets. The finite OA-QEC
refinement is:

```text
observer physics = entropy scale + observer algebra + channel/coarse-graining rule
```

The certificate gives exact finite evidence that entropy, horizon, min-cut,
and erasure fixed-point shadows alone are incomplete invariants of observer
physics.

## Evidence Classes

**Exact theorem-style claim.** The balanced-bridge observer family has matching
entropy/horizon/erasure shadows and different observer algebra/channel
semantics. The CLI audits a finite prefix and records the all-`m` theorem
statement. The `k=1` all-region erasure/fixed-point completion lemma gives a
separate exact positive boundary.

**Exhaustive bounded-search evidence.** Goal 2 Phase 31 audits the strict-cover
family and distinguishes strict hits from entropy near-misses rejected by
erasure semantics. Goal 3 Phase 40 packages the finite min-cut-visible witness.

**Conjectural/open boundary.** The current positive boundary is only certified
for the balanced-bridge prefix and exact only for all-region `k=1`: adding
observer center data separates the representative family, and all-region
erasure/fixed-point data complete the `k=1` algebra signature. The next search
is to match center, commutant, channel fixed-point, and logical-probe shadows
for richer `k` or named observer atlases while still differing algebraically,
or to prove that some enriched shadow is complete in a declared finite class.

## Reproducibility

| Major claim | Evidence class | Command |
| --- | --- | --- |
| Goal 4 fast tomography certificate | Exact family-prefix audit | `python3 -m qgtoy observer-tomography --max-m 3` |
| `k=1` all-region completion lemma audit | Exact theorem plus bounded implementation audit | `python3 -m qgtoy observer-tomography --max-m 3 --scan-max-n 4` |
| Bounded all-region tomography scan | Exhaustive bounded evidence | `python3 -m qgtoy observer-tomography --max-m 3 --scan-max-n 4` |
| Static observer entropy/horizon shadow | Exact certificate | `python3 -m qgtoy cosmology-phase1 --max-m 3` |
| Erasure and survivor fixed-point shadow | Exact certificate | `python3 -m qgtoy cosmology-phase2 --max-m 3` |
| Strict-cover entropy-near-miss audit | Exhaustive bounded evidence | `python3 -m qgtoy cosmology-phase31 --max-bonus 2` |
| Finite min-cut/reconstruction/channel witness | Exhaustive bounded evidence | `python3 -m qgtoy holography-phase40` |
| Combined tomography with live min-cut audit | Exact plus bounded evidence | `python3 -m qgtoy observer-tomography --max-m 3 --include-holography` |

## Limitations

This is finite stabilizer/OA-QEC evidence. The all-`m` theorem-style claim is
for the balanced-bridge observer family. The min-cut and strict-cover evidence
is bounded by the declared Goal 2/3 searches. The positive boundary is exact
only for all-region `k=1` stabilizer atlases; named observer atlases, richer
`k`, and continuum observer programs remain open.
