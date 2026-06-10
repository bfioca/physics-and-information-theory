# First Post-Indicial Frobenius Recurrence

The transformed-origin density theorem proves the cancellation of the apparent
field singularities. This certificate advances the weighted Fuchsian problem
one full recurrence beyond its indicial data.

For the default profile parameters `mu^2=1` and `lambda=1/400`, write

```text
F=pi-bx+c x^3+d x^5+O(x^7),
u=u0+u1 t+O(t^2),
v=v0+v1 t+v2 t^2+O(t^3),
t=x^2.
```

Every coefficient is represented as an exact rational function of the
unspecified slope `b`. The leading transformed equation includes the profile
correction proportional to `v0`. Consequently, the normalized linear mode
`v0=1,u0=0` generally has `v1` nonzero. This is an important correction to any
construction that retains only the leading indicial vector at finite cutoff.

The first post-indicial solve has recurrence matrix

```text
M5=(1/45)[[28+308b^2, -70-392b^2],
           [-22-200b^2, 28+176b^2]],
```

with exact determinant

```text
Delta5=-(28/75)(32b^4+12b^2+1)<0.
```

Thus the `p=5` recurrence is nonsingular for every real slope. The checker
solves it exactly for three normalizations:

1. the linear homogeneous column `v0=1,u0=0`;
2. the cubic homogeneous column fixed by the exact `p=3` kernel;
3. the zero-homogeneous-amplitude forced particular column.

At the declared rational reference slope inside the authenticated AU.3b box,
the coefficients are

```text
branch                v1              u1              v2
linear homogeneous    0.3279577054   -0.1494623983    0.04710453574
cubic homogeneous     3.195336901    -1.251770645    -0.6521074264
forced particular    -0.09477191097   0.1353338744    0.08724110619
```

All leading and `p=5` recurrence residuals vanish as exact rational-function
identities. The authenticated profile snapshot is source-hashed and the
reference slope is checked to lie inside its certified interval.

## Next Gate

This theorem supplies formal germs through `x^5`, not a finite-radius
enclosure. The next certificate must:

1. turn the exact germs into correlated Taylor models over the full slope box;
2. bound the omitted profile and field coefficients on `0<=t<=1/256`;
3. enclose the affine two-column homogeneous boundary subspace and particular
   vector in `(f,g,f',g')` at `x=1/16`;
4. pass that subspace directly to the global interval BVP without an avoidable
   interval Robin inversion.

## Reproduce

```bash
PYTHONPATH=. python experiments/centrifugal_skyrmion_frobenius_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_frobenius.py tests/test_centrifugal_skyrmion_frobenius_audit.py
```

Artifact SHA256:
`09ac1a8c29675e4dcc4d92f32ddaf6b75d9111563b5e404020db5e01e29551d4`.

## Claim Boundary

This is an exact formal recurrence theorem through `x^5`. It is not a Taylor
remainder bound, finite-cutoff transfer, Friedrichs-domain equivalence, Robin
enclosure, coercivity theorem, or validated forced response.
