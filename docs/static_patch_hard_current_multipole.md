# Distributed Hard-Current Multipoles And Bohr Leakage

## Local Target Interaction

Let a hard target with Hamiltonian `H_T` carry a local angular-current density
`ell_a(x)` on a geodesically convex worldtube `W_T`. Fix a frame at its center
`p` and parallel transport `Pi_(x->p)`. Bars denote bath and current components
transported to that common frame. The pseudoscalar bath couples through

```text
V=g sum_a int_(W_T) Bbar_a(x) tensor ellbar_a(x),
L_a=int_(W_T) ellbar_a(x).                             (1)
```

Choosing a center `p`, the exact lumping identity is

```text
V-g sum_a B_a(p) tensor L_a
=g sum_a int [Bbar_a(x)-B_a(p)] tensor ellbar_a(x).    (2)
```

This is an identity, not a long-wavelength approximation.

## First-Moment Bound

There are two distinct versions of the bound.

For a product reference vector `psi_B tensor psi_T`, assume

```text
||(B_a(x)-B_a(p))psi_B|| <= K r(x),
j_a(x)=||ell_a(x)psi_T||.
```

Then the triangle inequality gives the state-specific interaction-vector bound

```text
||(V-V_0)(psi_B tensor psi_T)||
 <= |g| K M_1,
M_1=sum_a int r(x)j_a(x).                              (3)
```

Alternatively, if the same inequalities hold in operator norm after compression
to invariant bath and target subspaces, equation (3) is a compressed operator
bound. For the two compressed unitary channels at time `T`, Duhamel's formula
then gives

```text
||U_T(.)U_T^dagger-U_(0,T)(.)U_(0,T)^dagger||_diamond
 <= min(2,2T|g|KM_1).                                  (4)
```

The product-vector branch alone does not imply (4).

## Exact Nonzero-Bohr Cancellation

Let

```text
ellbar_a(x;omega)=sum_(E'-E=omega) P_E ellbar_a(x)P_(E')
```

be the target Bohr decomposition. If the integrated angular charge is conserved,

```text
[H_T,L_a]=0,
```

then

```text
int ellbar_a(x;omega)=0,  omega != 0.                  (5)
```

Consequently every nonzero-Bohr interaction has zero monopole:

```text
V_omega
=g sum_a int [Bbar_a(x)-B_a(p)] tensor ellbar_a(x;omega),
omega != 0.                                            (6)
```

Equations (3)-(4) apply sector by sector with its corresponding current first
moment. Thus the global conserved charge is exactly zero Bohr frequency, while
all nonzero-Bohr target sectors are multipolar. Product-vector weights must be
sector specific unless target stationarity supplies an orthogonality argument.

The linear support dependence cannot be improved for one conserved component
without an extra moment cancellation. A two-cell `U(1)` target with

```text
H_T=(Omega/2)sigma_z,
ell_+=(sigma_z+sigma_x)/2,
ell_-=(sigma_z-sigma_x)/2
```

has conserved monopole `ell_++ell_-=sigma_z`. Its nonzero-Bohr `sigma_x`
monopoles cancel. For cells at distance `a` and bath increments `+Ka,-Ka`, the
surviving interaction is exactly `gKa sigma_x`, saturating (3). This witness is
not a three-component rotationally invariant target.

## Growing-Spin GKSL Stability

The interaction-level bound does not by itself imply a jump-operator bound after
the Davies limit and Kossakowski factorization. Declare an additional
interaction-to-jump transfer hypothesis on a finite invariant compression. In
the normalized diagonal-jump surrogate, let the ideal zero-Bohr jump operators
satisfy `||A_a||<=L` and let their multipole corrections obey
`||E_a||<=epsilon_0 L`. Assume unit diagonal rates and no Lamb-shift
perturbation. For one dissipator,

```text
||D[A+E]-D[A]||_diamond
 <=4||A||||E||+2||E||^2.                               (7)
```

Contractivity and Duhamel therefore give, for three axes and dimensionless heat
time `s`,

```text
delta_0 <=3sL^2(4epsilon_0+2epsilon_0^2).              (8)
```

For strictly secular nonzero-Bohr jumps there is no ideal monopole with which
to interfere. Under the declared aggregate bound

```text
sum_(a,omega!=0)||E_(a,omega)||^2<=3L^2epsilon_nz^2,
```

their total channel correction obeys

```text
delta_nz<=6sL^2epsilon_nz^2.                           (9)
```

Equation (9) requires strict secular separation and a bound on the aggregate of
all nonzero sectors. Individual first-moment bounds do not control a growing or
continuous gap set by themselves.

At `s=(1/2)log d`, `L=(d-1)/2`, and channel allocation `A/d`, equations (8)-(9)
give the sufficient worst-case caps

```text
epsilon_0=O(d^-3/log d),
epsilon_nz=O[d^(-3/2)/sqrt(log d)].                   (10)
```

within this surrogate. A general Kossakowski matrix, extra jump channels, or a
Lamb-shift error requires additional coefficient-norm terms.

## Support-Size Collision

Let `a_opt` be the target optical support radius, let `beta` be the local bath
amplitude used in the lumped term, and define a current-cancellation factor

```text
kappa=(sum_a int j_a)/||L psi_T||,
K_rel=R K/beta.
```

Also declare separate dimensionless jump-map transfer constants. For the
zero-Bohr linear correction assume

```text
epsilon_0 <= C_0 K_rel kappa a_opt/R.                 (11)
```

This is the missing interaction-to-GKSL bridge and is an input, not a
consequence of (3). For the nonzero-Bohr aggregate, separately assume

```text
sum_(a,omega!=0)||E_(a,omega)||^2
 <=3L^2[C_nz K_rel kappa_nz a_opt/R]^2.               (12)
```

This hypothesis includes any growth in the number or continuum of gaps; the
sectorwise first-moment theorem does not imply it. Combining (11) with (10)
gives the sufficient design condition

```text
a_opt/R=O(d^-3/log d).                                 (13)
```

On the collar `rho/R~1/d`, the exact same-shell geometry implies the stronger
proper/angular support law

```text
theta_support=O(d^-4/log d).                           (14)
```

This is a sufficient uniform guarantee, not a necessary support law. If the
transported compressed zero-Bohr current dipole vanishes as an operator for
every spatial/current component,

```text
int xi^i(x) ellbar_a(x;0)=0,
```

and the bath has `K_2,rel=R^2K_2/beta`, the zero-Bohr remainder is second order:

```text
||V_0-V_mono|| <= (|g|/2)K_2M_2.                      (15)
```

With a separate second-order transfer constant `C_2`, assume
`epsilon_0<=(C_2/2)K_2,rel kappa_2(a_opt/R)^2`. Then the same certificate is
satisfied by

```text
a_opt/R=O[d^(-3/2)/sqrt(log d)].                       (16)
```

The higher-spin common-mode theorem independently gives the leading
local-perturbative necessary center-distance law

```text
y_d=sqrt[A/(dL(L+1)log d)]
   =O[d^(-3/2)/sqrt(log d)].                           (17)
```

If target and reference must be distinct, nonoverlapping, equal-size
worldtubes, each obeys

```text
a_opt/R <= y_d/2
 =O[d^(-3/2)/sqrt(log d)].                             (18)
```

On the collar, exact same-shell optical geometry turns (18) into

```text
theta_support=O[d^(-5/2)/sqrt(log d)].                (19)
```

Thus the certificate supplies the smaller generic design laws (13)-(14). The
center-distance/disjointness laws (18)-(19) can become the active sufficient
constraints in the componentwise dipole-cancelled branch. Larger supports may
still work through model-specific cancellations. If overlapping worldtubes made
from distinguishable sectors are allowed, the disjointness part does not apply.

## Scope

The Bohr-monopole cancellation is exact under strong rotational invariance of
the compressed dynamics. The norm bounds are
conditional on either a product-state vector Lipschitz estimate or bounded
compressed operators; they do not hold in operator norm for an unbounded
unsmeared quantum field. The GKSL bounds concern a normalized diagonal-jump
finite-dimensional surrogate, not a derivation of the Davies approximation from
field theory. The theorem does not derive the three jump-map transfer constants,
Kossakowski or Lamb-shift stability, `K`, `K_2`, the current moments,
componentwise dipole cancellation, or strict secular aggregation from a named
hard-target matter action, and does not include localization stress and gravity.

Combining this support fork with the stipulated compact spherical-top radius
floor gives the controlled-branch obstruction in
`static_patch_localization_backreaction.md`. Its finite crossing is only an
illustration of the leading common-mode law.

The useful discriminator is whether a physical matter model supplies the
componentwise transported dipole cancellation and a uniform jump-map transfer
theorem. Without them, this package provides only the conservative
`d^-3/log d` optical and `d^-4/log d` angular sufficient design scales.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-hard-current-multipole
PYTHONPATH=. python3 -m unittest tests.test_static_patch_hard_current_multipole
```
