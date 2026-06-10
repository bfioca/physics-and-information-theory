# Exact Centrifugal Origin Indicial Algebra

The floating two-channel solver previously inferred its regular origin modes
from a singular-value decomposition at a small probe radius. The exact leading
profile data are

```text
F=pi-b x+O(x^3),
sin(F)=b x+O(x^3),
cos(F)=-1+O(x^2).
```

Substitution into the exact local quadratic density gives

```text
C=C0+O(x^2),  M=x M0+O(x^3),  P=x^2 P0+O(x^4).
```

`qgtoy/centrifugal_skyrmion_origin.py` performs this limit with exact rational
polynomial and Laurent arithmetic. Every coefficient remains a polynomial in
the unspecified positive origin slope `b`; no floating trigonometry or cutoff
radius enters.

For `y=x^p v`, the exact indicial pencil is

```text
K(p)=-p(p+1)P0-(p+1)M0^T+p M0+C0.
```

The checker proves the polynomial identity

```text
det K(p)=det(P0)(p-1)(p-3)(p+2)(p+4),
```

with

```text
det(P0)=1/1350+(2/225)b^2+(16/675)b^4 > 0.
```

Thus the regular powers are exactly `p=1,3`, the singular companions are
`p=-2,-4`, and the linear regular kernel is exactly

```text
(f,g)=(-1,1)x.
```

At the declared rational reference slope, the exact cubic-mode ratio is
`f/g=0.041727...`, agreeing with the former small-radius numerical probe.

Composing both exact regular modes at `x=1/16` with the authenticated AU.3b
shooting-slope interval also gives an exact interval enclosure of the leading
Robin matrix

```text
y'=R_lead y,
R_lead=B diag(1,3) B^-1/(1/16),
B=[[-1,a],[1,d]],
a=2/15,
d=4/45+(56/45)b^2.
```

In decimal display only, the exact rational enclosure is

```text
R_lead in [[17.27375,17.28991], [1.27375,1.28991];
           [30.71009,30.72625], [46.71009,46.72625]].
```

This replaces the probe-radius SVD at leading order. It deliberately does not
enclose the finite-cutoff Frobenius remainder, so it is not yet admissible as
the boundary condition of the final interval inverse.

This result removes the floating indicial diagnosis but does not yet prove a
form-domain theorem. The next origin step is to substitute

```text
g=x v(t),  f=-x v(t)+x^3 u(t),  t=x^2,
```

into the complete operator, prove the `(u,v)` coefficients are regular at
`t=0`, and validate the two-parameter transfer map to `x=1/16`. That theorem is
what connects smooth physical fields to the interval matrix inverse on the
positive-radius mesh.

The first part of this gate is now closed in
`centrifugal_skyrmion_transformed_origin.md`: substitution into the full local
Hessian proves `H_static=x^2 H_hat(t)` with no negative powers of `t`. The
transformed action still carries the weight `sqrt(t)/2`, so the weighted
Euler-Lagrange/Friedrichs theorem and finite-cutoff transfer remain open.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_origin_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_origin.py \
  tests/test_centrifugal_skyrmion_origin_audit.py
```
