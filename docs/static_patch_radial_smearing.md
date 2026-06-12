# Static-Patch Radial-Smearing Invariance

Status: exact arbitrary-radius radial-smearing theorem, center-gradient
extension, and finite-switching correlation ceiling; a distributed top current,
dissipative sectors, Davies error, and backreaction remain open

## Result

The pointlike qualification in the scalar common-mode obstruction can be
removed for a large, exactly solvable class of finite worldtube profiles.

On the optical spatial slice `H^3_R`, define

```text
phi_0(y)=y/sinh(y),       y=d_H/R.                       (1)
```

This is the zero-spectral-parameter zonal spherical function. Let `M_u` denote
the normalized angular average over a hyperbolic sphere of dimensionless radius
`u` around a point. Then

```text
M_u phi_0(r)=phi_0(u)phi_0(r).                           (2)
```

For `r,u>0`, the hyperbolic law of cosines gives

```text
cosh d=cosh r cosh u-sinh r sinh u z,    -1<=z<=1.
```

Changing variables from `z` to `d` proves (2) elementarily:

```text
(1/2) integral_(-1)^1 phi_0(d(z)) dz
 =1/[2 sinh r sinh u]
   integral_|r-u|^(r+u) d dd
 =ru/[sinh r sinh u].                                   (3)
```

The endpoint cases follow by continuity. Equation (2) is also the standard
spherical-function product formula for the Gelfand pair
`SO_0(1,3)/SO(3)`.

## Arbitrary Radial Profiles

Let `mu_p` and `nu_q` be any nonnegative normalized radial measures in the
optical volume measure, centered at `p` and `q`. They can be smooth profiles,
uniform balls, shells, or mixtures of shells of arbitrary finite radius. Define

```text
A_mu=integral phi_0[d(p,x)/R] dmu_p(x),
A_nu=integral phi_0[d(q,x)/R] dnu_q(x).                  (4)
```

Because `phi_0>0`, both amplitudes are positive. Repeated use of (2) gives the
zero-frequency auto- and cross-spectral coefficients

```text
B_pp=A_mu^2,
B_qq=A_nu^2,
B_pq=A_mu A_nu phi_0[d(p,q)/R].                         (5)
```

Therefore

```text
B_pq/sqrt(B_pp B_qq)
 =phi_0[d(p,q)/R]                                       (6)
```

exactly. Neither profile radius nor radial shape appears in the normalized
correlation. The profiles need not equal one another.

This is stronger than a small-smearing error estimate. For the declared radial
class, finite optical width neither repairs nor worsens the center-separation
common-mode deficit. The co-location theorem in
`static_patch_scalar_common_mode.md` therefore applies without assuming an
optically pointlike detector.

## Smooth Center-Gradient Extension

The same product formula removes the point-gradient UV qualification at zero
frequency. Let `f` and `g` be smooth compact nonnegative radial optical
profiles, neither identically zero, and define

```text
Phi_f(p)=integral f[d(p,x)/R] Phi(x) dvol_opt(x),
B_a^f(p)=D_(p,a) Phi_f(p).                              (7a)
```

The derivative is with respect to the profile center. It may be passed under
the integral, so `B_a^f` is a smooth compact signed field smearing rather than
a point derivative. Equation (5), applied before differentiation, gives

```text
<Phi_f(p) Phi_g(q)>_(omega=0)
 =A_f A_g phi_0[d(p,q)/R].                              (7b)
```

The positive radial amplitudes are independent of the centers. Taking one center
derivative at each end therefore yields exactly `A_f A_g` times the point
mixed-Hessian tensor. The two auto-covariances carry `A_f^2` and `A_g^2`, so
normalization cancels both profiles and leaves

```text
c_parallel^fg(y)=c_parallel(y),
c_perp^fg(y)=c_perp(y).                                 (7c)
```

Thus smooth compact nonnegative center-gradient smearing regulates the zero-mode bath
operator without changing the longitudinal or transverse correlation laws in
`static_patch_gradient_torque.md`. The center derivative makes the resulting
field smearing signed; nonnegativity is required only of the underlying radial
profile so that its amplitude has a fixed positive sign. This statement does
not cover a sign-changing or zero-transform radial profile, an arbitrary
smearing of the pointwise gradient, nonradial body multipoles, or a finite-time
spectral average, where the profile transforms depend on frequency.

## Finite-Switching Ceiling

The product formula holds at every real dimensionless spectral parameter `p`:

```text
phi_p(y)=sin(py)/[p sinh(y)]
        =phi_0(y) sinc(py).                              (7)
```

Let `A_f(p),A_g(p)` be arbitrary real radial spherical transforms and let
`w(p)>=0` include the scalar spectral density, Bunch-Davies thermal factor,
quadrature measure, and common switching filter `|chi_hat|^2`. Then
`|phi_p(y)|<=phi_0(y)`, and weighted Cauchy-Schwarz gives

```text
|integral w A_f A_g phi_p dp|
 <=phi_0(y)
   sqrt[integral w A_f^2 dp]
   sqrt[integral w A_g^2 dp].                           (8)
```

Thus the magnitude of the normalized finite-switching correlation obeys

```text
|c_eff(y)|<=phi_0(y).                                   (9)
```

Finite switching cannot improve the spatial common mode beyond the zero-
frequency value. For auto-variances `V_f,V_g` and cross covariance `C_fg`, (8)
also implies

```text
V_f+V_g-2C_fg
 >=(sqrt(V_f)-sqrt(V_g))^2
   +2[1-phi_0(y)]sqrt(V_f V_g).                         (10)
```

For commuting charges linearly coupled to a free Gaussian scalar, this
symmetrized covariance controls the exact pure-dephasing coherence magnitude.
A commutator-induced phase cannot reduce the trace-distance floor because
`|1-v exp(i theta)|>=1-v`. Equations (9)-(10) do not control dissipative
nonzero-Bohr jump channels or a noncommuting three-axis rotor.

## Physical Interpretation

A stationary conformally coupled scalar source must be weighted so its effective
profile after the conformal source map is radial in the optical `H^3_R` measure.
With `g_dS=Omega^2 g_opt` and `Phi_dS=Omega^-1 Phi_opt`, a covariant source
satisfies

```text
integral dvol_dS J Phi_dS
 =integral dvol_opt (Omega^3 J) Phi_opt.                 (11)
```

Therefore the radial theorem applies to `f_opt=Omega^3 J`; engineering a chosen
radial optical profile requires `J=Omega^-3 f_opt`. Generic profiles radial in
the physical static metric need not be optical radial.

For two centers on the same static shell, a spatial rotation maps one profile to
the other while preserving the physical conformal factor. Compact optical
profiles correspond to finite worldtubes, although the required physical source
density and its stress tensor still need to be supplied by an observer model.
A finite profile spans different local redshifts and is stationary in common
Killing time; the center lapse supplies only one reference proper-time
conversion. Smearing changes the absolute diffusion rate through `A_f^2` even
though it does not change the normalized zero-mode coefficient.

The result closes one loophole in the axial scalar surrogate:

```text
making the detector or observer radially larger does not make separated centers
experience a more nearly rank-one zero-frequency bath.
```

For a collar-following body with proper radius `a=alpha rho`, the optical width
is generically order `alpha`. Equation (6) shows that even this finite width
does not alter the normalized coefficient if the effective profile is optical
radial. The required center co-location remains

```text
d_H/R=O(1/[Delta sqrt(d log d)]).                        (12)
```

## Consequence For The Next Interaction

The escape routes are now more specific:

1. use nonradial multipoles of the finite top or hard angular target;
2. use a nonzero-frequency transition sector and a genuinely dissipative
   channel rather than radial scalar pure dephasing;
3. couple to a gauge/global mode rather than the local conformal scalar;
4. co-locate the relevant effective charge centers at the rate (7); or
5. abandon the append-and-twirl surrogate as the physical observer channel.

The next calculation should derive the actual top torque density and decompose
its optical profile into radial and nonradial spherical harmonics. The radial
monopole cannot evade the obstruction by changing its size.

A radial scalar density is orientation independent and exerts no torque on a
genuinely spherical top. Coupling one component such as `J_z Phi` selects an
external axis and is not an invariant three-axis interaction. A physical torque
requires vector/tensor bath operators, gradients, or stress-tensor couplings,
whose kernels must be derived separately. If the hard target and bath are both
sectors of the same scalar net, their system/bath split must also be specified.

## Novelty Boundary

The spherical-function product formula is established harmonic analysis, not a
new mathematical identity. Primary foundations include
[Godement](https://doi.org/10.1090/S0002-9947-1952-0052448-2),
[Harish-Chandra](https://doi.org/10.2307/2372786), and the explicit
`H^3=SL(2,C)/SU(2)` treatment of
[Grunbaum, Pacharoni, and Tirao](https://arxiv.org/abs/math/0203211).
Detector smearing and smooth switching are also established topics; see
[Louko and Satz](https://arxiv.org/abs/0710.5671) and
[Lee and Fuentes](https://arxiv.org/abs/1211.5261). The possible paper
contribution is its use to make
the finite-reference/static-patch no-go insensitive to arbitrary radial
worldtube size and common finite-switching filters, combined with the recovery
and redshift scalings. That combined claim still requires external review.

## Claim Boundary

Established:

1. the exact spherical mean identity (2)-(3);
2. the arbitrary nonnegative radial-profile factorization (5);
3. exact cancellation of both smearing amplitudes in (6);
4. persistence of the scalar center-separation obstruction at arbitrary radial
   optical width;
5. the finite-switching correlation ceiling (9) and relative-noise floor (10)
   for radial scalar pure-dephasing covariance;
6. the zero-frequency center-gradient extension (7a)-(7c) for smooth compact
   radial profiles.

Not established:

1. arbitrary nonradial or pointwise-gradient profile smearings (the smooth
   center-gradient radial class (7a) is covered at zero frequency);
2. a three-axis rotational torque on a finite spherical top;
3. identification of the hard angular field target with a localized scalar
   charge density;
4. dissipative nonzero-Bohr jump channels, Lamb shifts, or Davies errors;
5. a matter action and stress tensor realizing the required conformal source
   weights;
6. lifetime, compactness, or gravitational backreaction control.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-radial-smearing
PYTHONPATH=. python3 -m unittest tests.test_static_patch_radial_smearing
```
