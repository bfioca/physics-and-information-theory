# Validated Regular-Origin Weak Form-Dual Bound

Status: authenticated primal and loaded-adjoint origin weak residual bounds
complete.

The former origin certificate converted the derivative-load residual to a
strong residual. That is valid for a full strong-form composition, but it
cannot be joined directly to the positive-radius weak adjoint residual: an
integration-by-parts trace remains at the artificial cutoff.

The weak certificate instead keeps the exact Fuchs form. With

```text
t=x^2,  y=x a(t),
r0=x r0_hat(t),  r1=t r1_hat(t),
T=I/2-Pbar^-1 antisym(Mbar),
```

the residual is

```text
R(v)=integral x [r1_hat dot (x d)
                 +(r0_hat-T^T r1_hat) dot v] dx.
```

Using the certified bounds `Pbar>=I/100` and `W>=I/100`, both terms have the
exact weight

```text
integral_0^x0 x^2 dx = x0^3/3.
```

For `x0=1/16` and both authenticated shooting-slope cells, the resulting
bounds are

```text
primal rotational squared dual upper   0.002219365433899958
primal rotational dual upper           0.047110141518572810
loaded adjoint squared dual upper       0.000000258228030899
loaded adjoint dual upper               0.000508161422088081
```

The loaded adjoint result includes the regular-origin exterior-master load.
Because the origin and outer adjoint residuals now use the same weak
representation, their join does not require an artificial cutoff conormal
term.

The primal value is also certified, although a consistently strong
primal-origin/outer/wall composition remains available and is tighter for the
current workflow. These numbers do not include the outer bulk or wall terms
and are not an exterior-amplitude interval.

Reproduce with

```bash
PYTHONPATH=. python experiments/validated_centrifugal_origin_weak_dual_audit.py
python -m pytest -q \
  tests/test_validated_centrifugal_origin_weak_dual.py \
  tests/test_validated_centrifugal_origin_weak_dual_audit.py
```

Artifact: `experiments/validated_centrifugal_origin_weak_dual.json`.
