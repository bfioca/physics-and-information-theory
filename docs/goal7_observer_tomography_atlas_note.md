# Goal 7: Observer-Algebra Tomography Atlas

Goal 7 turns the Goal 6 theorem into an equivalence-aware small-code atlas.
The aim is not another example; it is a bounded classification engine for
finite stabilizer/OA-QEC observer shadows.

## Scope

Default certificate:

```text
k = 2,
n <= 4,
equivalence = qubit permutation,
all physical regions,
all listed shadow tiers.
```

The atlas enumerates stabilizer-code representatives, computes shadow keys,
groups codes by shadow, and asks whether any shadow class contains two distinct
all-region observer-algebra signatures.

Minimality claims are relative to this declared quotient and bound.

## Shadows Classified

The atlas currently classifies:

- entropy vector;
- entropy profile;
- reconstruction poset;
- erasure/survivor channel shadow;
- center shadow;
- channel + center shadow;
- entropy-response dimension shadow;
- center + entropy-response dimension shadow;
- logical relative-entropy/recovery/commutator-test shadows;
- full observer-algebra signature.

## Atlas Table

| Shadow | Determines `tau`? | Minimal collision | Amplified? | Status |
| --- | --- | --- | --- | --- |
| entropy vector | unknown | none through `n<=4` | not applicable | bounded no-collision |
| entropy profile | no | `n=4` | not attempted | bounded collision |
| reconstruction poset | no | `n=3` | yes | bounded collision |
| channel | no | `[[3,2,1]]` | `[[15,2,3]]` | proven witness |
| center | no | `n=4` | yes | bounded collision |
| channel + center | no | `[[4,2,1]]` | `[[20,2,3]]` | proven witness |
| entropy-response dimension | no | `n=4` | yes | bounded collision |
| center + entropy-response dimension | yes | none | theorem | algebraic-operational hybrid |
| response + commutator tomography | yes | none | theorem | fully operational completion |
| full signature | yes | none | tautological | reference tier |

The certificate output contains the exact generators and separating regions for
each first collision.

The center-plus-response row is a hybrid completion: entropy response gives
`dim L_R`, but the center dimension is algebraic unless it is obtained by
commutator experiments. The fully operational positive row is response plus
commutator tomography.

## Expert-Facing Summary

We built an equivalence-aware finite stabilizer/OA-QEC observer-algebra
tomography atlas for `k=2,n<=4`, quotienting by qubit permutations and checking
all physical regions. The atlas classifies which operational shadows determine
the observer-algebra signature `tau(R)`. It finds bounded-minimal collisions
for entropy profiles, reconstruction posets, channel shadows, center shadows,
channel+center, and entropy-response dimension, with distance-amplified
witnesses where applicable. The positive theorem is that logical
response/recovery probes identify the visible logical subspace `L_R`, and
commutator tests recover its restricted symplectic form, hence `tau(R)`. The
remaining frontier is intrinsic tomography without labeled logical probes.

## Theorem Candidates

The atlas emits one theorem-candidate record per shadow tier:

- collision tiers produce counterexample statements with minimality certificates
  under the declared quotient;
- completion tiers produce symplectic proof sketches;
- no-collision tiers produce bounded conjecture-frontier statements rather than
  theorems.

## Distance Amplification

For `L_R`-derived shadows, the atlas attaches a five-qubit-inner threshold lift.
The inner code is the perfect `[[5,1,3]]` code, whose regions of size `<=2` are
forbidden and regions of size `>=3` are qualified. This gives certified
distance-3 amplified witnesses for the channel and channel-plus-center
separations and threshold-lift records for the other `L_R`-derived collisions.

The amplified shadow match is justified by the threshold map, not by enumerating
all `2^N` amplified regions in the default atlas certificate.

## Intrinsic-Probe Frontier

Goal 6 still assumes labeled logical Pauli probes. Goal 7 records the next
frontier explicitly:

```text
Can tau(R) be recovered from physical-region perturbations and state
distinguishability without labeled logical Pauli probes?
```

That remains open in this package.

Natural Goal 8 target: remove the labeled logical Pauli probe assumption and
search using physical-region perturbations, restricted state distinguishability,
recovery maps, modular/relative-entropy response, channel spectra, and
commutator experiments internal to `R`.

## Known vs New

Known-derived ingredients: stabilizer enumeration, cleaning/QSS/OA-QEC
supported-logical facts, stabilizer entropy rank formulas, and symplectic
linear algebra.

New atlas contribution: automated equivalence-aware collision mining, bounded
minimality records, a classified diagnostic table, distance-amplification proof
obligations, and theorem-candidate generation.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 7 atlas certificate | `python3 -m qgtoy observer-tomography-atlas --max-n 4` |
| Focused atlas regression | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal7_observer_algebra_tomography_atlas_certificate` |
| Goal 6 operational baseline | `python3 -m qgtoy observer-tomography-operational --max-n 4` |
