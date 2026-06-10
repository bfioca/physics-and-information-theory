# Validated Physical Centrifugal Origin Transfer

The conormal finite-cell theorem controls the state

```text
X=(a,z),
a=y/x,
z=(P y'+M^T y-s1)/x^2.
```

This certificate exports that result to the physical field variables at the
cutoff `x=1/16`.

## Reconstruction

On each authenticated profile cell, the same Taylor models used in the
conormal remainder proof provide endpoint enclosures for `Pbar`, `Mbar`, and
`shat1`. The exact identities are

```text
y=x a,
y'=Pbar^-1(z-Mbar^T a+sigma shat1).
```

The degree-two center for each branch is combined with its certified
componentwise `X` error. Interval matrix inversion and multiplication then
give direct endpoint tubes for

```text
(f,g,f',g').
```

Both authenticated slope cells and all three columns are covered:

```text
linear homogeneous,
cubic homogeneous,
forced particular.
```

The independently evaluated formal `x^5` field and derivative centers are
contained in the returned tubes. Across all cells and branches, the exact
rational audit proves

```text
maximum field interval width      < 3/50,
maximum derivative interval width < 3/2.
```

The derivative enclosure is deliberately conservative because interval
reconstruction drops correlations between `Pbar`, `Mbar`, `a`, and `z`. It is
nevertheless finite and suitable as a rigorous boundary tube for a global
interval weak-form solve.

## Affine Use

The tubes certify columns separately. For homogeneous amplitudes `alpha` and
`beta` and forcing amplitude `sigma`, combine the column centers linearly and
bound the total error by scaling each column error with
`|alpha|`, `|beta|`, and `|sigma|` before summing.

## Reproduce

```bash
PYTHONPATH=. python experiments/validated_centrifugal_physical_origin_transfer_audit.py
python -m pytest -q tests/test_validated_centrifugal_physical_origin_transfer.py tests/test_validated_centrifugal_physical_origin_transfer_audit.py
```

## Claim Boundary

This is a columnwise physical finite-origin transfer theorem. Friedrichs
trace-space equivalence, the global continuum inverse, and a validated
nonzero exterior response remain open.
