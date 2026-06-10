# Validated Centrifugal Liouville Spline

## Result

The explicit symmetric multiplier

```text
K = sym(M) - P/(2x)
```

reduces the coupled centrifugal quadratic form to a positive square plus the
regular completed potential `W_K`.  With `Pbar=diag(p,r)` and antisymmetric
entry `alpha`, positivity of `W_K-(1/20)I` is checked without matrix division:

```text
d1 = r U - alpha^2,
d2 = p V - alpha^2,
D  = d1 d2 - p r z^2.
```

Since `p,r>0`, strict positivity follows from `d1>0` and `D>0`; `d2>0` is
retained as a redundant audit.  Centered exact-rational Taylor models preserve
the profile correlations through the assembled expressions.  All discarded
polynomial terms, transcendental tails, reciprocal tails, and arithmetic
rounding enter outward interval remainders.

On the 43-cell exact piecewise-polynomial profile archived by the AU.1 Newton
audit, 42 cells close directly.  Cell 24, with radius `[1/2,11/16]`, closes
after one exact bisection.  The resulting 44 validation cells give

```text
min p                  = 0.0213331584854351
min r                  = 0.0319999988139318
min d1                 = 0.0011452285672344
min d2                 = 0.0094737729781766
min D                  = 0.0000118689614877
target W_K lower bound = 1/20
```

The source-hashed artifact is
`experiments/centrifugal_skyrmion_liouville_spline_certificate.json`, SHA256
`581db1b6a078b5e43a09de17fe450f261d04931f94e52c5a039ea27b468752f3`.

## Claim Boundary

This is a continuum interval proof for the archived exact approximate spline
on `[1/16,4]`.  It is not yet a theorem for the exact nonlinear Skyrmion:

- the endpoint-corrected AU.1 Newton-tube radii are not yet propagated;
- the authenticated conormal origin family on `[0,1/16]` must be joined;
- closability and the global representation theorem remain to be stated; and
- no two-sided inverse or nonzero forced response is certified here.

The small determinant margin makes correlated tube propagation the immediate
proof gate.  Replacing it with independent `F,F',F''` boxes would discard the
cancellations this certificate was built to retain.

## Reproduction

```bash
PYTHONPATH=. python experiments/centrifugal_skyrmion_liouville_spline_audit.py
PYTHONPATH=. python -m pytest -q \
  tests/test_validated_centrifugal_liouville_taylor.py \
  tests/test_centrifugal_skyrmion_liouville_spline_audit.py
```
