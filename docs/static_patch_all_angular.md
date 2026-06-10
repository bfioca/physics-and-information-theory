# All-Angular Conformal Static-Patch Wall Limit

Status: rigorous equal-time covariance convergence for the free conformally
coupled scalar under explicit angular Sobolev assumptions; Lorentzian
distributional, Hadamard, and local-factor identifications remain open

## Geometric Reduction

For the four-dimensional conformally coupled massless scalar, the optical
static-patch metric is `R x H^3_R`. After spherical-harmonic decomposition, the
rescaled radial operators are

```text
h_(ell,X)=-d^2/dx^2+ell(ell+1)/(R^2 sinh^2(x/R))
```

on `(0,X)` with a Dirichlet stretched-horizon wall, or on the half-line after
wall removal. The angular potential tends to zero at the horizon. Therefore
every fixed `ell` operator has spectral bottom zero in the half-line limit.
There is no global high-angular-momentum Killing-energy gap: low-energy states
can translate toward the horizon.

For data localized in `(0,B)`, the correct replacement is the spectral-overlap
bound

```text
||1_(0,B) 1_[0,E^2](h_ell)||
 <= min(1, E R sinh(B/R)/sqrt(ell(ell+1))).
```

This suppresses the interior overlap of high-`ell`, low-energy states without
making a false global gap claim.

## Exact Continuum Modes

With `y=x/R`, `q=kR`, and `N_ell=sqrt(q^2+ell^2)`, the normalized continuum
modes obey

```text
N_(ell+1) u_(ell+1)
 =(2ell+1)coth(y) u_ell-N_ell u_(ell-1),

u_0=sqrt(2/pi) sin(qy).
```

The implementation evaluates this exact Darboux recurrence with a hybrid
upward/Miller algorithm. A Frobenius series is used near the origin as a stable
independent branch. This avoids the catastrophic cancellation of expanded
polynomials in `coth(y)`. The certified numerical API is deliberately capped
at `ell<=64` and rejects dimensionless phases beyond `10^6`.

The tests include the exact `ell=1,2` formulas, regular-origin behavior through
`ell=20`, radial-equation residuals through `ell=32`, and near-horizon geometry
at `x/R=20`.

## Uniform Field Tail

Let `beta=2 pi R`, `lambda_ell=ell(ell+1)`, and

```text
M_L=1+(L+1)(L+2).
```

For compactly supported field data, define

```text
||f||_(s,0)^2
 =sum_(ell,m) (1+lambda_ell)^s ||f_(ell,m)||_L2^2.
```

The field covariance multiplier is

```text
A_beta(h)=coth(beta sqrt(h)/2)/(2 sqrt(h)).
```

The Matsubara expansion and Dirichlet bracketing give, uniformly in `ell` and
every wall position `X>B`,

```text
<f,A_beta(h_(ell,X))f>
 <= C_phi(beta,B) ||f||^2,

C_phi(beta,B)=4B^2/(beta pi^2)+beta/12.
```

Consequently the diagonal angular tail satisfies

```text
sum_(ell>L,m) <f_(ell,m),A_beta(h_(ell,X))f_(ell,m)>
 <= C_phi M_L^(-s) ||f||_(s,0)^2.
```

The corresponding bilinear estimate follows from positivity and
Cauchy-Schwarz, with decay `M_L^(-(s+t)/2)`.

## Uniform Momentum Tail

Ordinary angular Sobolev regularity is not enough for momentum covariance. Let
the momentum coefficients have a common compact radial support in `(0,B)`, so
they lie in every sufficiently large finite-wall form domain. Define the radial
quadratic form

```text
q_ell[g]=int (|g'|^2
 +ell(ell+1)|g|^2/(R^2 sinh^2(x/R))) dx
```

and the energy-weighted norm

```text
||g||_(s,E,beta)^2
 =sum_(ell,m) (1+lambda_ell)^s
 [beta q_ell[g_(ell,m)]/8+3||g_(ell,m)||^2/(2beta)].
```

The scalar inequality

```text
sqrt(h)coth(beta sqrt(h)/2)/2 <= beta h/8+3/(2beta)
```

then gives the wall-uniform tail

```text
T_L^pi(g,g) <= M_L^(-s) ||g||_(s,E,beta)^2.
```

This stronger form-domain hypothesis is essential.

## All-Angular Wall Limit

For fixed `ell`, increasing Dirichlet intervals converge by monotone form
exhaustion. Strong-resolvent convergence alone is not sufficient because the
thermal covariance multipliers are unbounded at zero or infinity.

For the field sector, apply monotone convergence to the generalized inverse
form in the zero Matsubara term and dominated convergence to the positive
Matsubara resolvents. For the momentum sector, split

```text
sqrt(h)coth(beta sqrt(h)/2)/2
 =sqrt(h)/2+sqrt(h)/(exp(beta sqrt(h))-1).
```

The second term is bounded and continuous. Compact support makes the first
spectral moment independent of the distant wall and controls its high-energy
tail. Thus every fixed finite angular sum converges.

The uniform `M_L^(-s)` bounds make both omitted angular tails smaller than any
chosen epsilon, independently of the wall. An epsilon/three argument therefore
proves full all-angular equal-time covariance convergence.

## Bunch-Davies Match

The closed Euclidean optical kernel is

```text
W_opt=1/[8 pi^2 R^2 (cosh(d_H/R)-cos(tau/R))].
```

Its conformal pullback obeys the exact identity

```text
cosh(x/R) cosh(x'/R) W_opt
 =1/[8 pi^2 R^2 (1-Z_E)],
```

which is the Euclidean conformally coupled Bunch-Davies kernel. The code uses
manifestly nonnegative denominator formulas to avoid near-horizon subtraction.
A finite partial-wave/momentum calculation is retained only as a sampled
numerical audit of this exact identity, not as a proof of convergence.

## Claim Boundary

This result establishes:

1. the exact all-angular free conformal radial operators and modes;
2. wall-uniform angular field and momentum covariance tails;
3. all-angular equal-time finite-wall covariance convergence for the stated
   test spaces;
4. the exact Euclidean optical/Bunch-Davies conformal identity;
5. a stable numerical audit of representative partial-wave sums.

It does not establish Lorentzian distributional boundary values, spacetime
microcausality from the regulated sequence, the Hadamard wavefront set, local
quasi-equivalence, a Type-`III_1` local GNS factor, its continuous core, a
gravitational constraint, or generalized entropy.

## Next Gate

The next theorem should combine this angular wall limit with the ultraviolet
methods of `static_patch_uv_removal.md` to prove unequal-time Lorentzian
distributional convergence on compact spacetime tests. It should then identify
the boundary value with the Bunch-Davies Hadamard state and invoke a precise
local-factor theorem only after its hypotheses are checked.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-all-angular
PYTHONPATH=. python3 -m unittest tests.test_static_patch_all_angular
```
