# Validated Centered Correlated Primal Residual

Status: certified positive-radius outer residual

The earlier box validator ranged the radius, profile jet, and exact rational
trial jet independently on each cell. Those quantities are all functions of
one radial coordinate, so the resulting dependency loss dominated the bound.

The centered validator carries a common normalized coordinate through:

- the exact endpoint-corrected profile spline and its first two derivatives;
- the exact rational trial and its first two derivatives;
- the metric, trigonometric kernels, conormal blocks, and their derivatives;
- the assembled strong residual.

The authenticated Newton-tube errors remain interval remainders. Thus the
improvement does not discard the unknown-solution uncertainty.

On the same `43` authenticated cells, with no extra subdivision, the audit
proves

```text
integral_[1/16,4] |r_y|^2 dx <= 0.010027698207072146.
```

The independent-box result on those cells was about `328.1385`; preserving
the radial correlation improves the rigorous bound by a factor greater than
`30000`. This diagnoses the old value as dependency wrapping rather than a
large physical residual.

The remaining width comes primarily from independently appended Newton-tube
remainders. The next sharpening should preserve their graph/slope correlation
or use a residual correction, rather than merely subdividing the same boxes.

Reproduce with

```bash
python experiments/validated_centrifugal_correlated_residual_audit.py
python -m pytest -q \
  tests/test_validated_centrifugal_correlated_residual.py \
  tests/test_validated_centrifugal_correlated_residual_audit.py
```

Claim boundary: positive-radius primal bulk residual only. The origin and wall
pieces are certified elsewhere; a useful full primal energy-dual norm and the
loaded adjoint norm still require tighter correlated remainder control.
