# Finite dS-Like QEC Diagnostic-Gate Model

## Certified Result

The model is a finite stabilizer/QEC toy model satisfying a de Sitter-like
observer-patch diagnostic gate. Its primitive is not an asymptotic boundary
interval. Its primitive is a pair of finite observer causal patches with a
finite shared horizon:

```text
observer_p      = {1,2,3} union {p_j}
observer_q      = {1,2,3} union {q_j}
shared_horizon  = {1,2,3}
bridge_shell    = {p_j,q_j}
static_diamond  = observer_p union observer_q
```

The capstone certificate packages the existing exact certificates into one
diagnostic-gate verdict: horizon entropy, patch overlap, observer
reconstruction algebra, complementarity/no-cloning guards, erasure semantics,
and patch channel/fixed-point behavior are all checked by finite stabilizer or
exact rational-channel diagnostics.

## Main Witness

For the balanced-bridge CSS pair `A_m,B_m`, the named patch entropy, overlap,
MI/CMI/I3, and shared-horizon algebra agree. The observer patches differ:
`A_m` has observer algebra signature `(1,1,1,false)`, while `B_m` has full
logical reconstruction signature `(2,0,0,true)`.

The horizon semantics are finite and explicit. The observer patches overlap
exactly on `shared_horizon`, so the two reconstructing observer patches in the
second code are not disjoint copies. The erasure suite also checks the QEC
complementarity identity: an erased region is correctable exactly when the
survivor complement reconstructs all logical information.

## Proof Obligations

| Obligation | Source command |
| --- | --- |
| Observer causal-patch primitive with finite shared horizon | `python3 -m qgtoy cosmology-phase1 --max-m 3` |
| Horizon entropy, patch overlap, MI/CMI/I3, and shared-horizon algebra | `python3 -m qgtoy cosmology-phase1 --max-m 3` |
| Observer reconstruction algebra split | `python3 -m qgtoy cosmology-phase1 --max-m 3` |
| Complementarity/no-cloning guard and named erasure semantics | `python3 -m qgtoy cosmology-phase2 --max-m 3` |
| Controlled patch growth with fixed shared horizon | `python3 -m qgtoy cosmology-phase2 --max-m 3` |
| Exact channel/fixed-point behavior on finite transition graphs | `python3 -m qgtoy cosmology-phase22` |
| Robust channel synthesis with preserved horizon invariant | `python3 -m qgtoy cosmology-phase27 --max-bonus 2` |
| Strict-cover bounded audit and erasure-gate no-go | `python3 -m qgtoy cosmology-phase31 --max-bonus 2` |
| Capstone proof-obligation map | `python3 -m qgtoy desitter-toy --max-m 3 --max-bonus 2` |

## Exact And Bounded Evidence

The theorem-style finite model rests on exact Phase 1 and Phase 2 certificates:
static causal-patch diagnostics, deterministic patch growth, horizon entropy,
observer-pair metrics, observer algebra, exact erasure probes, and
QEC-complementarity checks.

The channel evidence is bounded but exact within the stated rule languages.
Phase 22 certifies exact rational channel dynamics on a 49-node transition
graph. Phase 27 synthesizes robust channel rules over four substrates and keeps
the repaired shared-horizon correctability/fixed-point profile invariant. Phase
31 exhaustively audits the declared strict-cover family: 175 candidates, 66 raw
entropy/reconstruction hits, 8 strict hits, and 58 erasure-gate rejections.

## Why This Is de Sitter-Like, Not AdS/HaPPY-Like

The primitive is not a privileged asymptotic boundary with subregion intervals.
The primitive is a finite collection of observer patches, their overlap, and
their static diamond. Horizon semantics are named finite-region semantics:
entropy, algebra, erasure correctability, survivor fixed points, and channel
invariants are certified directly.

## Limitations

This is a finite toy model, not continuum de Sitter space. It is mostly a
`k=1` stabilizer/CSS construction plus bounded repaired-cover and channel
audits. It does not classify all patch grammars, all stabilizer codes, all
tensor-network codes, or all possible dynamics. The certified claim is narrower
and sharper: a finite QEC toy model satisfying a de Sitter-like observer-patch
diagnostic gate exists, with entropy/horizon diagnostics agreeing while observer
algebra and channel semantics differ.

## Reproduce

```bash
python3 -m qgtoy desitter-toy --max-m 3 --max-bonus 2
python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_de_sitter_qec_toy_model_capstone_certificate
```
