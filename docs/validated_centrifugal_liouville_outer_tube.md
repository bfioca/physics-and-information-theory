# Validated Centrifugal Liouville Outer Tube

## Certified Split

The canonical AU.1 Newton tube is combined with the division-free completed
Liouville minors.  The raw spline is retained as the correlated polynomial
center.  The full affine endpoint correction and the cellwise Newton
displacements are absorbed into exact uniform `C2` radii, so the enclosure is
conservative but requires no unarchived reconstruction.

The `1/20` exact-spline target does not survive the authenticated tube at the
worst cell.  A smaller strictly positive target does:

```text
W_K >= 1/100 I on 3/16 <= x <= 4.
```

The 31 source cells produce 45 validation cells after adaptive refinement,
with maximum refinement depth two. The exact lower bounds are numerically

```text
min p  = 0.0212949510563966
min r  = 0.0319808716401226
min d1 = 0.0015796571176299
min d2 = 0.0092018466096716
min D  = 0.0000005629318349
```

The same audit extends the regular nonlinear Volterra family to `[0,3/16]`
over the full shooting-slope interval. Its outward-rounded contraction upper
bound is `0.916612582057544892`. Thus the exact nonlinear solution family is
covered on both sides of the split, while the inner Liouville inequality is
kept as a separate proof obligation.

Artifact:
`experiments/centrifugal_skyrmion_liouville_outer_tube_certificate.json`,
SHA256
`c8744dd4136b607595a42de1ada271644c8408b0fff6b4a2629bf749ea136b91`.

## Claim Boundary

This proves the completed-potential inequality on the authenticated nonlinear
Newton tube for `[3/16,4]`. The separate source-hashed regular-origin audit now
proves the matching inequality on `[0,3/16]`. A global coercivity theorem still
requires:

1. a common smooth weighted core and control of the split trace;
2. the already certified positive wall remainder; and
3. the closed-form representation theorem and two-sided inverse.

The reduced constant changes the prospective inverse bound from `20` to
`100`. Whether that is sufficient must be tested against the forced-response
interval rather than judged in isolation.

## Reproduction

```bash
PYTHONPATH=. python \
  experiments/centrifugal_skyrmion_liouville_outer_tube_audit.py
PYTHONPATH=. python -m pytest -q \
  tests/test_validated_centrifugal_liouville_tube.py \
  tests/test_centrifugal_skyrmion_liouville_outer_tube_audit.py
```
