# Goal 8: Intrinsic Observer-Algebra Tomography

Goal 8 removes the labeled logical Pauli probes used in Goals 6-7. The
question is whether an observer-algebra signature

```text
tau(R) = (dim L_R, dim Z_R, dim L_R^perp, L_R = L)
```

can be recovered from physical-region operations alone.

## Scope

Default certificate:

```text
k = 2
n <= 4
equivalence = qubit permutation
all physical regions
all listed intrinsic-shadow tiers
```

Minimality claims are relative to this declared quotient and bound.

## Intrinsic Probes

The intrinsic tiers use physical-region data only:

- named region entropy and entropy profiles;
- erasure/survivor channel data;
- survivor fixed-point or local response dimensions;
- local physical-Pauli perturbation response spectra;
- restricted-state distinguishability dimensions;
- commutator experiments among operators physically supported in `R`;
- local centralizer/stabilizer quotient dimensions.

No tier is handed a labeled logical Pauli class.

## Atlas Table

| Intrinsic shadow | Determines `tau`? | Minimal collision | Amplified? | Status |
| --- | --- | --- | --- | --- |
| named region entropy vector | unknown | none through `n<=4` | not applicable | bounded no-collision |
| entropy profile | no | `n=4` | not attempted | bounded collision |
| erasure/survivor channel | no | `[[3,2,1]]` | `[[15,2,3]]` | certified collision |
| survivor fixed-point dimension | no | `n=4` | yes | certified collision |
| local physical-Pauli response spectrum | no | `n=4` | yes | certified collision |
| restricted-state distinguishability dimension | no | `n=4` | yes | certified collision |
| local commutator center | no | `n=4` | yes | certified collision |
| physical response + center | yes | none | theorem | intrinsic operational completion |
| physical response + commutator tomography | yes | none | theorem | intrinsic operational completion |
| full signature | yes | none | tautological | reference tier |

The certificate output contains the exact generators and separating regions for
each first collision.

## Main Result

The negative hierarchy is certificate-backed: many natural physical-only
shadows do not determine the all-region observer algebra in the bounded atlas.
The positive completion is theorem-style:

For a stabilizer code with stabilizer `S`, logical symplectic space
`L = S^perp / S`, and physical Pauli space on `R` denoted `P_R`, the physically
supported code-preserving probes form `S^perp \cap P_R`. Locally null probes
form `S \cap P_R`. Therefore

```text
dim L_R = dim(S^perp \cap P_R) - dim(S \cap P_R).
```

Pairwise commutator experiments among these local physical probes recover the
restricted symplectic rank on `L_R`. Thus

```text
dim Z_R = dim L_R - rank(commutator form on L_R)
dim L_R^perp = 2k - dim L_R
L_R = L iff dim L_R = 2k.
```

So physical response plus commutator tomography determines `tau(R)` without
labeled logical Pauli probes.

## Harlow-Facing Summary

Goal 8 upgrades the finite observer-algebra tomography atlas by removing
labeled logical Pauli queries. In the `k=2,n<=4` stabilizer/OA-QEC atlas,
natural intrinsic shadows such as erasure/survivor data, survivor fixed-point
dimension, local physical-Pauli response spectra, restricted distinguishability
dimension, and local center data have bounded-minimal collisions against
`tau(R)`. The positive theorem candidate is intrinsic: locally supported
code-preserving physical operators recover `dim L_R`, and commutator
experiments internal to `R` recover the restricted symplectic form, hence
`tau(R)`.

## Known vs New

Known-derived: stabilizer/OA-QEC supported-centralizer linear algebra, cleaning
logic, quotient dimensions, and symplectic commutator rank.

New atlas output: labeled logical probes are removed from the diagnostic input;
the certificate classifies physical-only shadow tiers, records bounded-minimal
collisions for weak intrinsic probes, attaches distance-amplification records,
and isolates physical response plus commutator tomography as the first
completion tier in this finite scope.

## Limitations

This is exact finite stabilizer/OA-QEC mathematics. It is not a continuum
gravity theorem, not an approximate-QEC theorem, and not a non-Pauli
operator-algebra theorem. The positive protocol still assumes exact access to
code-preserving local Pauli perturbations and exact commutator experiments.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 8 intrinsic atlas certificate | `python3 -m qgtoy observer-tomography-intrinsic --max-n 4` |
| Focused Goal 8 regression | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal8_intrinsic_observer_algebra_tomography_certificate` |
| Goal 7 labeled-probe baseline | `python3 -m qgtoy observer-tomography-atlas --max-n 4` |
