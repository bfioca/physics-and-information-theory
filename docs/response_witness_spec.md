# Intrinsic Response Witness Specification

## Claim Boundary

This note defines the finite noncommutative response witness used by the
continuum-lift obstruction theorem. It is an operator-norm witness, not a claim
that every possible topology preserves the same matrix-unit representative.

## Definition

For a finite observer algebra `A_L`, define

```text
nu(A_L) = sup { ||[a,b]|| : a,b in A_L, ||a|| <= 1, ||b|| <= 1 }.
```

The chosen persistence topology for the theorem sprint is operator norm.

## Finite Separation

For `M_N` with `N >= 2`, choose matrix units

```text
a=e_12,       b=e_21.
```

Then

```text
[a,b] = e_11 - e_22,       ||[a,b]|| = 1.
```

Therefore

```text
nu(M_N) >= 1.
```

For `C^N`, all commutators vanish, so

```text
nu(C^N) = 0.
```

Thus the finite response gap is bounded below by `1`.

## Topology Choice

The operator-norm choice is load-bearing. The rank-one trace-`L^2` norm of
`e_11-e_22` is

```text
sqrt(2/N),
```

which vanishes along consecutive cutoffs. That is why the theorem does not use
rank-one trace-`L^2` persistence as its response hypothesis.

For the cofinal UHF scaffold, the same finite subfactor can persist as a
norm-closed noncommutative corner. For the implemented consecutive UCP maps,
the certificate records track operator-norm response retention.

## Persistence Under Implemented Lift Maps

The current finite lift-map audit gives:

- trace-filled UCP refinement: commutator norm retained in the embedded corner;
- harmonic projection/refinement: commutator norm retained in the preserved
  low-mode corner;
- heat-kernel coarse graining: positive response retention, tending to one
  under the declared cutoff scaling;
- Berezin-Toeplitz-inspired smoothing surrogate: positive response retention,
  tending to one under `O(1/N)` smoothing.

This is not a proof that those maps are canonical static-patch embeddings. It
is finite evidence that the response witness is not killed by the implemented
non-factorial refinement maps.

## Code Evidence

Direct helpers:

```text
qgtoy/lift_diagnostics.py::response_witness_record
qgtoy/lift_diagnostics.py::response_witness_gap
qgtoy/lift_diagnostics.py::embedding_response_witness_records
```

Focused tests:

```bash
PYTHONPATH=. python3 -m unittest tests.test_lift_diagnostics
```
