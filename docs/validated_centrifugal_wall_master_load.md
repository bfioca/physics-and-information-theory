# Validated Moving-Wall Master Load

Status: exact-rational interval certificate for the wall part of the exterior
master adjoint load.

For the physical parameters `R=20` and `a=4`, the wall ratio is exactly
`x=a/R=1/5`. The center-regular static `l=2` solution and its derivative are
therefore enclosed from the exact closed forms using the positive rational
series for `atanh(1/5)`. This gives the Green data

```text
w(a)  = (2R/15) u(1/5),
w'(a) = (2/15) u'(1/5).
```

The wall displacement is `-f(a)/F'(a)`, while the spherical wall stress also
depends on the same authenticated slope `F'(a)`. Ordinary interval arithmetic
for these two appearances loses their correlation. The certificate instead
writes the slope as a centered affine variable and performs the reciprocal and
the generic-scalar moving-wall kernel calculation in the existing centered
Taylor algebra.

The resulting exact rational enclosure is

```text
0.002688103336731132 < gamma_B < 0.002834701713361219,
width(gamma_B) < 1/5000.
```

In particular, the moving-wall master load is strictly positive. Loading the
free radial endpoint equation of the archived exact rational adjoint trial
gives

```text
0.005743770662465949 < eta_z,wall < 0.006339340647031048 < 1/150.
```

This closes the wall part of the adjoint load. The conormal interface theorem
is certified separately. The bulk master-functional load and adjoint bulk
residual remain open; no nonzero exterior response interval is claimed here.

Reproduce with

```bash
python experiments/validated_centrifugal_wall_master_load_audit.py
python -m pytest -q \
  tests/test_validated_centrifugal_wall_master_load.py \
  tests/test_validated_centrifugal_wall_master_load_audit.py
```
