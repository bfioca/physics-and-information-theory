# Validated Regular-Origin Adjoint Master Load

Status: authenticated regular-origin load and loaded residual complete

The exterior master functional is integrated by parts before interval
evaluation:

```text
B(y) = integral [b0 dot y + b1 dot y'] dx.
```

For the regular variables

```text
t=x^2,  y=x a,  W=x^3 W_hat(t),  W'=x^2 W1_hat(t),
```

the completed stress and Green weights factor without division by `x` or
`t`. If `K_a` and `K_d` are the regular affine stress contractions, then

```text
x^4 K_a a  = x [t K_a] y,
x^4 K_d y' = t [t K_d] y'.
```

Thus the physical adjoint load has exactly the Fuchs form required by the
origin residual theorem,

```text
b0=x b0_hat(t),  b1=t b1_hat(t),
```

and both hats retain an additional factor of `t`. The implementation carries
the hats and their `t` derivatives through exact rational interval
arithmetic. The center-regular Green function and its derivative are enclosed
by positive rational series with explicit geometric tails.

On the two authenticated shooting-slope cells and the archived exact rational
adjoint origin patch, the source-hashed audit certifies

```text
||B-A z_h||^2_L2([0,1/16])
    < 0.000000002481492321,

origin contribution to ||B-A z_h||^2_V*
    < 0.000000248149232003,
```

where the second line uses the already certified completed-potential lower
bound `1/100`. These are valid all-strong diagnostics. They cannot be added
directly to a positive-radius residual that remains in weak form, because an
artificial cutoff trace would then be missing.

The companion weak-origin certificate keeps both Fuchs load coefficients and
gives the representation-compatible squared dual bound
`0.000000258228030899`. That quantity composes with the weak positive-radius
and wall residuals to close the full adjoint norm. See
`validated_centrifugal_origin_weak_dual.md`. The load certificate does not by
itself prove exterior-response zero exclusion.

## Reproduce

```bash
PYTHONPATH=. python experiments/validated_centrifugal_origin_adjoint_load_audit.py
PYTHONPATH=. python -m pytest -q \
  tests/test_validated_centrifugal_origin_adjoint_load.py \
  tests/test_validated_centrifugal_origin_adjoint_load_audit.py
```

Artifact: `experiments/validated_centrifugal_origin_adjoint_load.json`.
