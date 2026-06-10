# Signed Regular-Origin Corrected Estimator

Status: both signed center contributions certified

The dual-weighted corrected estimator contains

```text
J_hat = J_rigid + B(y_h) + R_y(z_h).
```

This certificate supplies the portions of both terms on `0 <= x <= 1/16`
for every authenticated shooting-slope cell.

## Master Functional

After the density derivative is integrated by parts and all center factors
are canceled, the regular completed-stress contraction is

```text
c dot T = x^4 [H_rigid(t) + k_a(t) dot a_y(t) + k_d(t) dot y_h'(t)],
t=x^2,  a_y=y_h/x.
```

The rigid coefficient is retained explicitly. The archived primal origin
trial is transformed into exact polynomials in normalized time and ranged by
its exact rational Bernstein hull. Therefore

```text
integral_0^x0 c dot T dx
  in range(H) x0^5/5,
x0^5/5 = 1/5242880.
```

Over the complete authenticated slope interval,

```text
-0.000000000097819258
  < [J_rigid+B(y_h)]_origin
  < 0.000000000094165448.
```

## Residual Action

The cancellation-safe primal strong residual and archived adjoint trial factor as

```text
r_y=x r_hat_y(t),  z_h=x a_z(t).
```

Let `r1=s1-M^T y_h-P y_h'` be the weak derivative residual. Integrating the
origin cell by parts while retaining the positive-radius cells in weak form
gives

```text
R_y(z_h)|_origin
  = integral_0^x0 x^2 r_hat_y dot a_z dx
    + r1(x0) dot z_h(x0).
```

The center trace vanishes by regularity. The volume has exact radial weight
`x0^3/3=1/12288` and retains its previous certified hull

```text
-0.000000197187058185
  < integral_0^x0 x^2 r_hat_y dot a_z dx
  < 0.000000198459112250.
```

The previously omitted cutoff trace is now explicitly enclosed by

```text
-0.000000108845953434
  < r1(x0) dot z_h(x0)
  < 0.000000135509776212.
```

Consequently the complete weak origin action obeys

```text
-0.000000306033011618
  < R_y(z_h)|_origin
  < 0.000000333968888461.
```

The combined signed center contribution is

```text
[-0.000000306130830876,
  0.000000334063053909].
```

The interval contains zero. It is a composable directed enclosure, not a
center-only sign or zero-exclusion result.

## APIs

- `validated_origin_master_functional_contribution` evaluates the signed
  `J_rigid+B(y_h)` center term.
- `validated_origin_primal_residual_action` evaluates the signed
  `R_y(z_h)` strong volume plus the required cutoff trace.
- `validated_archived_origin_corrected_estimator_family` returns both terms,
  their cellwise sums, and full-family hulls.

## Reproduce

```bash
PYTHONPATH=. python \
  experiments/validated_centrifugal_origin_corrected_estimator_audit.py
PYTHONPATH=. python -m pytest -q \
  tests/test_validated_centrifugal_origin_corrected_estimator.py \
  tests/test_validated_centrifugal_origin_corrected_estimator_audit.py
```

Artifact:
`experiments/validated_centrifugal_origin_corrected_estimator.json`.

This certificate omits every positive-radius and wall estimator term, the
primal-adjoint residual-product error, collective normalization, and the Weyl
transfer. It makes no response zero-exclusion claim.
