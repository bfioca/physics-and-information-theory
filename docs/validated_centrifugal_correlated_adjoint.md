# Validated Centered Local-Matrix Adjoint Form-Dual Bound

Status: positive-radius-plus-weak-wall partial theorem complete; the separate
weak regular-origin certificate closes the full adjoint composition.

The earlier adjoint certificate ranged the profile, exact rational trial,
Green kernel, weak master load, form blocks, and Liouville multiplier
independently. It then applied the global scalar lower bounds

```text
Pbar >= I/100,  W >= I/100
```

to the final coefficient boxes. This was rigorous but produced a partial dual
norm of about `0.7694`, far above the `0.04` design target.

The centered certificate carries one normalized radial coordinate through all
of those quantities. It forms the weak residual

```text
R_z(v) = integral (r0 dot v + r1 dot v') dx
```

and ranges only the completed-square coefficients

```text
c_d = r1/x,
c_v = r0 - T^T c_d,
T   = I/2 - Pbar^-1 Abar.
```

Where centered Sylvester minors certify the actual matrices, the pointwise
form-dual density is bounded by

```text
c_d^T Pbar^-1 c_d + c_v^T W^-1 c_v.
```

This is a local `2x2` Riesz bound, not a sampled or floating proxy. On cells
where the centered completed-potential determinant is too broad, the audit
falls back explicitly to `|c_v|^2/(1/100)`. Exact symmetric Taylor integration
removes odd normalized-coordinate terms before the interval remainder is
added.

On the `43` authenticated positive-radius cells, local completed-potential
inversion closes on `26` cells and the certified bounds are

```text
centered scalar-floor bulk square       0.002509606074591027
hybrid local-matrix bulk square         0.000943584944534433
weak loaded-wall square                 0.000010516852407001
positive-radius-plus-wall square        0.000954101796941434
positive-radius-plus-wall dual norm     0.030888538277837511
```

The weak wall coefficient is `gamma_B-k z_f(a)`. It does not include the trial
conormal: that term is already part of the bulk weak form and including it
again would mix strong and weak representations.

Thus one serious correlation-aware redesign reaches the `1/25` adjoint design
target. The authenticated Newton-tube errors remain interval remainders; none
are replaced by their floating centers.

The separate weak regular-origin certificate contributes squared norm below
`0.000000258228030899`. Composing it in the same weak representation gives

```text
complete loaded-adjoint square          0.000954360024972333
complete loaded-adjoint dual norm       0.030892717992632714
```

This closes `delta_z`, but it cannot by itself certify a nonzero exterior
amplitude; the complete primal norm is the remaining bottleneck.

## Primal Reuse And Stop Diagnostic

The same completed-potential inverse also lifts the value-only primal strong
residual. On the same cells, including the independently certified primal
wall mismatch, it gives

```text
centered scalar-floor bulk square       1.002769820707214607
hybrid local-matrix bulk square         0.614633743206714407
strong conormal wall square             0.000009995023891950
positive-radius-plus-wall dual norm     0.783992179955008452
```

This second result is intentionally a negative diagnostic. Local matrix
weighting improves the primal bound, but not nearly enough for zero exclusion:
the remaining width is in the authenticated primal residual representation,
not mainly in the global `1/100` form floor. More subdivision of the same
representation is therefore not the next recommended step. A residual
correction or a correlation model for the Newton-tube remainder is required.

Adding the separate all-strong origin contribution gives the complete primal
norm `delta_y<0.785351351663998829`. This is still not an exterior-amplitude
interval; the dual-weighted composer supplies that final step.

Reproduce with

```bash
PYTHONPATH=. python \
  experiments/validated_centrifugal_correlated_adjoint_audit.py
PYTHONPATH=. python \
  experiments/validated_centrifugal_correlated_primal_dual_audit.py
python -m pytest -q \
  tests/test_validated_centrifugal_correlated_adjoint.py \
  tests/test_validated_centrifugal_correlated_adjoint_audit.py
```

Artifact: `experiments/validated_centrifugal_correlated_adjoint.json`.
Primal diagnostic:
`experiments/validated_centrifugal_correlated_primal_dual.json`.
Weak origin certificate:
`experiments/validated_centrifugal_origin_weak_dual.json`.
