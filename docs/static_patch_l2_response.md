# Static-Quadrupole Response In A De Sitter Patch

Status: exact fixed-background master resolvent; matter-source projection now
supplied in `static_patch_l2_master_source.md`

## Master Operator

Let

```text
f(r)=1-r^2/R^2,
r_*=R atanh(r/R).
```

For a static even-parity `l=2` perturbation of pure de Sitter, the
gauge-invariant Zerilli-Moncrief field obeys

```text
[-partial_(r_*)^2+6f/r^2]Psi=S,

A_2 Psi=F,
A_2=-d/dr[f d/dr]+6/r^2,
F=S/f.                                               (1)
```

The theorem applies independently to all five magnetic components.

## Boundary Conditions And Coercivity

The physical Friedrichs conditions are

```text
Psi(r)=O(r^3)                 as r -> 0,
f(r)Psi'(r) -> 0             as r -> R-.             (2)
```

The second condition removes the logarithmic zero-frequency horizon branch.
Regularity should be stated for the master field or in a horizon-penetrating
gauge, not inferred from Regge-Wheeler coordinate components.

The quadratic form is

```text
q[Psi]=integral_0^R [f|Psi'|^2+6|Psi|^2/r^2]dr
      >=(6/R^2)||Psi||_(L2(dr))^2.                  (3)
```

Consequently the static solution is unique and

```text
||Psi||_2 <= (R^2/6)||F||_2,
q[Psi]     <= (R^2/6)||F||_2^2.                    (4)
```

This is a static elliptic coercivity result. It is not a Lorentzian spectral
gap; the tortoise-coordinate wave operator still has continuum down to zero.

## Exact Green Kernel

Set `x=r/R`. The center- and horizon-regular homogeneous solutions are

```text
u(x)=15(3-x^2)atanh(x)/(4x^2)-45/(4x),
u(x)=x^3+6x^5/7+O(x^7),

v(x)=(3-x^2)/(2x^2),
v(1)=1.                                             (5)
```

Their exact Wronskian is

```text
(1-x^2)(u v'-u'v)=-15/2.                           (6)
```

Thus

```text
G_2(r,s)=(2R/15)
  u(min(r,s)/R)v(max(r,s)/R)                       (7)
```

is symmetric, positive, and has unit flux jump. For a finite signed master
source supported in `r<=r_w<R`, positivity and monotonicity give

```text
||Psi||_infinity
 <= K_infinity(r_w/R)||F||_TV,

K_infinity(x_w)
 =(2R/15) max_(0<x<=x_w) u(x)v(x).                 (8)
```

## Horizon Susceptibility

The diagonal kernel has the exact asymptotic

```text
G_2(r,r)/R
 = (1/2)log[2/(1-r/R)]-3/2+o(1).                  (9)
```

The proper static-slice distance from `r` to the horizon is

```text
rho=R arccos(r/R).
```

Therefore

```text
G_2(r,r)=R log(2R/rho)-3R/2+o(R).                 (10)
```

Equation (10) is a candidate response prediction: a conserved static
quadrupole master source acquires a logarithmically enhanced response as its
support approaches the horizon. The completed default Skyrmion now has a
nonzero off-wall master response, but its near-horizon family and invariant
Weyl/worldtube reconstruction remain open.

## Conservation Gate

Write a static even source schematically as

```text
delta T^t_t=-rho Y,
delta T^r_r=p_r Y,
delta T^r_A=j D_A Y,
delta T^A_B=p_perp Y delta^A_B+pi Y^A_B,
```

where `Y^A_B=D^A D_B Y+[l(l+1)/2]delta^A_B Y` is trace free. Background
conservation requires, with `L=l(l+1)`,

```text
p_r'+f'(rho+p_r)/(2f)+2(p_r-p_perp)/r-Lj/(fr^2)=0,
j'+2j/r+p_perp-(L-2)pi/2=0.                       (11)
```

Equations (11) show why pressure, shear, and wall traction cannot be omitted.
The completed Skyrmion bulk-plus-shell stress now passes these identities, and
the exact projection onto `F` in (1) is supplied separately. The remaining
gravity gate is physical normalization, validation, Israel matching, and
invariant reconstruction.

## Claim Boundary

The theorem is fixed pure de Sitter, linearized, static, even parity, `l=2`,
and assumes a conserved compact master source. It does not yet cover:

- the currently non-negligible spherical Skyrmion metric deformation;
- interval validation and physical normalization of the completed rotating
  matter-wall source;
- odd `l=1` frame dragging or time-dependent radiation;
- nonlinear rotational gravity; or
- reconstruction of a chosen invariant curvature/worldtube observable.

## Reproduction

```bash
python experiments/static_patch_l2_response_audit.py
python -m pytest -q tests/test_static_patch_l2_response.py \
  tests/test_static_patch_l2_response_audit.py
```

Artifact:

```text
experiments/static_patch_l2_response_exact_certificate.json
SHA256 45871bfe3e15a65b546eddd6391d42d0d8e6665ee981c9f24618409f52dcd051
```
