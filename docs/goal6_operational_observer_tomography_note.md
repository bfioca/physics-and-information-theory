# Goal 6: Operational Observer Algebra Tomography

This note upgrades Goal 5 from algebraic commutant bookkeeping to an
operational finite stabilizer/OA-QEC tomography theorem.

## Question

For a finite `[[n,k]]` stabilizer/OA-QEC code and a physical observer region
`R`, the observer-algebra signature is

```text
tau(R) = (dim L_R, dim Z_R, dim L_R^perp, L_R = L),
Z_R = L_R cap L_R^perp.
```

Goal 5 showed that directly giving `dim L_R^perp` completes the signature by
symplectic bookkeeping. Goal 6 asks for a non-tautological replacement:

```text
What operational data determine tau(R) without directly supplying L_R^perp?
```

## Operational Assumptions

The theorem is operational in the finite-code sense. It assumes a tomographer
can label a logical Pauli `v`, prepare or condition on the `v=+1` logical
eigen-sector, and compare the induced response on a named physical region
`R`. This is a controlled finite-code probe, not a claim that a gravitational
observer automatically has access to arbitrary global logical labels.

The operational data split into three layers:

- **Visibility probe:** entropy response, logical relative entropy, or
  individual logical-Pauli recovery detects whether `v in L_R`.
- **Algebra probe:** commutator tests among visible recovered probes determine
  the restricted symplectic form on `L_R`.
- **Signature reconstruction:** finite symplectic linear algebra converts those
  data into `tau(R)`.

## Theorem

For a labeled logical Pauli probe `v`, impose the logical constraint `v=+1`.
Let

```text
Delta_v(R) = S_code(R) - S_code+<v>(R).
```

For stabilizer codes, `Delta_v(R)` is exactly `0` or `1`, and

```text
Delta_v(R) = 1  iff  v has a representative supported on R.
```

Thus the single-probe entropy-response profile recovers the visible logical
subspace `L_R`. Equivalently, the visibility probe can be implemented as:

- logical relative-entropy distinguishability of the two `v` eigenvalue sectors
  is nonzero exactly when `v in L_R`;
- individual logical-Pauli recovery on `R` succeeds exactly when `v in L_R`;
- commutator tests among visible recovered probes give the rank of the
  restricted symplectic form on `L_R`.

From these operational tests:

```text
logical_dim = dim L_R,
center_dim = dim L_R - rank(commutator form on L_R),
commutant_dim = 2k - dim L_R,
reconstructs_all iff dim L_R = 2k.
```

This determines the full observer-algebra signature without directly measuring
or supplying `L_R^perp`.

## Diagnostic Landscape

The certified finite result is a hierarchy of insufficiency and completion, not
a total information order. In particular, channel shadows and center shadows
are different kinds of information; this package does not claim that one
determines the other.

| Diagnostic shadow | Result |
| --- | --- |
| Erasure/survivor channel shadow | Insufficient for `k>1`. |
| Center shadow | Insufficient in the bounded scan. |
| Channel + center shadow | Insufficient for `k>1`. |
| Entropy-response dimension shadow | Insufficient in the bounded scan. |
| Center + entropy-response dimension shadow | Sufficient for signatures. |
| Entropy/relative-entropy/recovery response + commutator tests | Sufficient for signatures. |

The insufficiency entries are exact finite counterexamples in the bounded scan.
The completion entries are theorem-backed and checked exhaustively through the
declared finite search.

## Witnesses

**Channel insufficiency.** The `[[3,2,1]]` pair `<XXI>` versus `<XXX>` has the
same all-region erasure/survivor channel shadow but differs on region `{0,1}`:

```text
(2,0,2,false) vs (3,1,1,false).
```

**Center and channel-plus-center insufficiency.** The `[[4,2,1]]` pair
`<XIIX,XXXI>` versus `<IZXI,ZIXX>` has matching all-region channel and center
shadows but differs on region `{1,2}`:

```text
(3,1,1,false) vs (1,1,3,false).
```

**Entropy-response dimension insufficiency.** The bounded scan finds an `n=4`
collision where the entropy-response dimension shadow agrees but the center
differs:

```text
(2,2,2,false) vs (2,0,2,false).
```

So entropy response gives `dim L_R`, but without center or commutator tests it
does not determine the symplectic type of the visible algebra.

**Operational completion.** Adding an algebraic center dimension to
entropy-response dimension determines the signature. The more operational
completion is single-probe response plus commutator tests: response determines
`dim L_R`, while commutators determine the restricted symplectic rank and hence
the center dimension.

## Distance Amplification

The certificate concatenates the strict witnesses with the five-qubit perfect
inner code.

- The channel-shadow separation lifts to a certified `[[15,2,3]]` pair.
- The channel-plus-center separation lifts to a certified `[[20,2,3]]` pair.

The inner code has the exact threshold gate: inner regions of size `<=2` are
forbidden, and regions of size `>=3` are qualified. Therefore every amplified
physical region reduces to an outer block subset for the certified shadows.

## Known vs New

Known-derived ingredients: stabilizer cleaning, QSS access structures,
supported-logical reconstruction, and stabilizer entropy rank formulas.

New diagnostic package: Goal 6 separates weak observer shadows from
operational completion data. The non-tautological completion is not
`dim L_R^perp`, nor merely an algebraic center shadow; it is
single-logical-probe entropy/relative-entropy/recovery response plus
commutator tests.

## Limitations

This is exact finite stabilizer/OA-QEC mathematics. It uses labeled logical
Pauli probes and exact stabilizer entropy/recovery/commutator tests. It does
not yet prove an approximate QEC theorem, a non-Pauli OA-QEC theorem, or a
continuum gravitational observer-algebra result.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 6 operational certificate | `python3 -m qgtoy observer-tomography-operational --max-n 4` |
| Focused regression | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal6_operational_observer_algebra_tomography_certificate` |
| Goal 5 baseline hierarchy | `python3 -m qgtoy observer-tomography-kgt1 --max-n 4` |
