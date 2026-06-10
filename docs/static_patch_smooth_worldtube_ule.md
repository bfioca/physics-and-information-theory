# Smooth Compact Worldtube ULE Constants And Localization Penalty

Status: named compact `C-infinity` spatial regulator, analytic transform
derivatives, profile-specific step-converged Sobolev estimates, conservative
closed-form exact-profile Sobolev enclosures, and a new small-support
localization penalty for the sufficient ULE coupling schedule. Tight interval
quadrature and derivation of the spatial profile and prescribed switch from
local matter remain open. Generic finite preparation is controlled separately.

## Named Spatial Profile

Let `a` be the desired optical support radius and set `A=a/R`. On optical
`H^3_R`, choose the radial seed

```text
b_A(y)=exp[1-1/(1-(2y/A)^2)],   0<=y<A/2,
b_A(y)=0,                       y>=A/2.                (1)
```

It is smooth at the center, flat at its boundary, positive inside, and belongs
to `C_c^infinity(H^3_R)`. Normalize its spherical transform at the zero
spectral channel:

```text
D_A=int_0^(A/2) b_A(y)y sinh(y)dy,
F_A(p)=D_A^-1 int_0^(A/2)
       b_A(y)y sinh(y)sinc(py)dy,
F_A(0)=1.                                               (2)
```

This is normalization against the `p=0` spherical function
`phi_0(y)=y/sinh(y)`, not ordinary unit spatial volume.

Convolve the seed with its radial reflection. The resulting field prefilter
`h_A=f_A^vee*f_A` is nonnegative, `C_c^infinity`, supported in optical radius
`a`, and has field-amplitude multiplier

```text
H_A(p)=F_A(p)^2>=0.                                    (3)
```

The regulated improved-gradient spectrum is

```text
j_A(omega)=j_0(omega)F_A(Romega)^4.                    (4)
```

It preserves exact KMS detailed balance and
`j_A(0)=1/(24pi^3R^3)`. Because the principal square root is
`sqrt(j_0)F_A^2`, real zeros of `F_A` produce no absolute-value cusps.

## Analytic Derivatives

Writing `rho_A(y)=D_A^-1 b_A(y)y sinh(y)`, differentiation under the compact
integral gives

```text
F_A'(p)=int rho_A(y)y sinc'(py)dy,
F_A''(p)=int rho_A(y)y^2 sinc''(py)dy.                 (5)
```

The finite-window implementation uses origin series for `sinc`, `sinc'`, and `sinc''` and
tests both derivatives against centered finite differences. The bare thermal
factor is differentiated analytically, including its smooth zero-frequency
limits. Product differentiation then gives `q=sqrt(j_A)`, `q'`, and `q''`
without differentiating sampled data.

A fixed Simpson rule is not an infinite-frequency representation of (2): its
finite sinc sum generically has an artificial `O(p^-1)` tail. All numerical
transform values below are therefore finite-window quadrature diagnostics. The
exact tail is controlled separately by integration by parts in the defining
integral.

## Profile-Specific Moment Bounds

Composite Simpson quadrature computes

```text
Q_0=||q||_2,
Q_1=||q'||_2,
Q_2=||q''||_2.                                        (6)
```

Separately optimizing the weighted Cauchy--Schwarz scales gives

```text
G=int|g(t)|dt <= sqrt(2pi Q_0Q_1),
M_1=int|t g(t)|dt <= sqrt(2pi Q_1Q_2).                (7)
```

For `R=1` and total support radius `a=0.2`, the step- and window-converged
numerical estimates are

```text
Q_0=26.6977477290,
Q_1=1.57849600683,
Q_2=0.176766804082,
G_num=16.2723018013,
M_1_num=1.32407331492.                                 (8)
```

The radial/frequency refinement changes the three norms by at most
`4.5e-9` relatively; doubling the frequency window changes them by at most
`6.8e-13`. The executable inflates the resulting inputs by a declared numerical
margin. These are profile-specific floating-point convergence results, not
interval enclosures.

At `L=4096`, `d=8193`, and `N=1/d`, the resulting candidate caps conditional
on the converged quadrature inputs and default numerical margin are

```text
lambda <= 8.0e-20     for epsilon_infinity<=1/(4d),
lambda <= 8.84e-22    for epsilon_infinity<=1/(4d^2). (9)
```

The severity of these candidate values is scientifically useful: a strict compact
profile of width `0.2R` carries much more ultraviolet Sobolev weight than the
quasilocal Gaussian of the same nominal width. Equation (9) remains conditional
on the tight numerical estimates.

## Closed-Form Exact-Profile Enclosure

The exact integral profile also admits a deliberately loose analytic enclosure.
Put `s=A/2`, `u(y)=b_A(y/s)sinh(y)`, and

```text
H(p)=D_A^-1 int_0^s u(y)sin(py)dy,  F(p)=H(p)/p.       (9a)
```

Twice integrating the three half-interval transforms by parts gives
`|H^(j)(p)|<=C_j/p^2`; the needed endpoint data vanish directly. Equivalently,
one may use odd or even Sobolev extensions as appropriate, but there is no
common smooth odd extension for all three weights. Rational inequalities
`D_A>=s^3/36`, `exp(s)<8/7`, `pi<22/7`, and elementary bump-derivative bounds
then give explicit `p^-3` envelopes for `F,F',F''`. Splitting frequency at
`p=1` and `P=ceil(32/A)` encloses the exact positive tail; KMS encloses the
negative tail. All reported endpoints are exact decimal rationals rounded
upward by integer arithmetic.

For `R=1`, `a=0.2`, this proves

```text
Q_0 <= 3495.325453538189,
Q_1 <= 12944.154923952921,
Q_2 <= 71805.966340613957,
G   <= 16863.898481372697,
M_1 <= 76435.381039140748.                             (9b)
```

At `L=4096`, substituting these rigorous moment upper bounds into the symbolic
sufficient-cap formula gives guarded ordinary floating-point evaluations

```text
lambda_cap approximately 9.9769e-27 for epsilon_infinity<=1/(4d),
lambda_cap approximately 1.1022e-28 for epsilon_infinity<=1/(4d^2). (9c)
```

The formula is sufficient when evaluated exactly. The displayed decimals are
downward-guarded binary-float evaluations, not directed interval endpoints.

The large gap between (9) and (9c) measures proof looseness, not a physical
effect. A future directed interval computation should enclose the finite window
tightly and append the analytic tail, rather than replacing the exact integral
by the discrete sinc sum.

## Candidate Localization Penalty

In the small-support regime, set `x=a omega`. The positive-frequency bare
gradient square root grows as `omega^(3/2)`, while the shape depends on `x`.
Consequently

```text
Q_0=Theta(a^-2),
Q_1=Theta(a^-1),
Q_2^2=[3/(64pi^2)]log(R/a)+O(1),
Q_2=Theta(sqrt(log(R/a))).                             (10)
```

Equation (7) implies

```text
G_bar=Theta(a^-3/2),
M_1_bar=Theta(a^-1/2[log(R/a)]^1/4).                  (11)
```

The long-time term in the stabilized ULE residual is proportional to
`G_bar^3 M_1_bar`, so the sufficient coupling cap has the additional law

```text
lambda_cap=Theta(a^(5/2)[log(R/a)]^-1/8)                (12)
```

at fixed `L,N,R` and residual budget.

The logarithmic coefficient follows from
`sqrt(j_0)''~3 omega^-1/2/(4sqrt(12)pi)` in the intermediate window
`R^-1<<omega<<a^-1`, giving `3/(64pi^2)=0.00474943`. Three supports
`a/R=(0.1,0.2,0.4)` give successive numerical slopes `0.0048821` and
`0.0051202` for `Q_2^2` against `log(R/a)`. The executable comparison between
`a/R=0.2` and `0.4` obtains effective exponents

```text
(-1.9954,-1.0071,-0.0870) for (Q_0,Q_1,Q_2),
(-1.5012,-0.5470)          for (G_bar,M_1_bar),
+2.5254                    for lambda_cap.             (13)
```

This is a derived candidate regulator-locality tradeoff inside the controlled
ULE route:
strictly shrinking the stationary worldtube makes uniform Markov control
parametrically more expensive. It is not a lower bound on every possible
non-Markovian or profile-adapted approximation.

## Spatial Locality And Source Map

The radial `h_A` is a pre-gradient smoothing kernel. For a center `p` and
orthonormal direction `a`, the actual scalar field test is

```text
F_(a,p)(y)=D_(p,a)h_(A,p)(y).                           (14)
```

It is compact, smooth, sign-changing, and dipolar. Under
`g_dS=N^2g_opt`, `chi_dS=N^-1chi_opt`, its external scalar-source realization
is

```text
J_(a,p)^dS=N^-3 F_(a,p),                               (15)
```

up to switching, coupling, and proper-time normalization. Equivalently, using
the hyperbolic transvection Killing field `K_(a,p)`, integration by parts gives
a derivative-source realization proportional to `h_(A,p)K_(a,p)^iD_i chi_opt`.

For compact switching `zeta in C_c^infinity`, `zeta F_(a,p)` is a genuine
compact spacetime test localized in its causal hull. The stationary ULE model
instead uses an eternal bounded-cross-section worldtube
`R_t times B_a(p)`. Exact KMS frequency diagonality and the imported ULE theorem
belong to that stationary branch. Compact switching convolves the response
with `|zeta_hat|^2`; pointwise detailed balance, the exact zero-mode heat rate,
and the stationary ULE estimate do not automatically survive.

Finally, spreading one lumped set of noncommuting `Q_a` across a finite body is
an extended detector model, not yet a manifestly microcausal matter action. A
physical completion must derive a local current density, its collective
projection, multipole errors, switching, holding stress, and backreaction.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-smooth-worldtube-ule
PYTHONPATH=. python3 -m unittest tests.test_static_patch_smooth_worldtube_ule
```

Related references:

- [Nathan and Rudner, Universal Lindblad equation](https://arxiv.org/abs/2004.01469)
- [Perche and Zambianco, derivative-coupled detectors](https://arxiv.org/abs/2305.11949)
- [de Ramon et al., causality and extended detector models](https://arxiv.org/abs/2102.03408)
- [Perche et al., detectors from localized probe fields](https://arxiv.org/abs/2308.11698)
