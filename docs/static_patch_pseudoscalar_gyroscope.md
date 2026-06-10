# Local Pseudoscalar Gyroscope And Davies Tradeoff

## Minimal Parity-Consistent Action

Let a marked top have orientation `Q(tau) in SO(3)`, space-frame angular
velocity `varpi=(dot Q Q^-1)^vee`, and inertia `I`. Introduce a conformally
coupled pseudoscalar `chi` and the static-observer acceleration

```text
a^mu=u^nu nabla_nu u^mu.
```

The local worldline action

```text
S_top=int d tau[-m+(I/2)|varpi^a-g B^a(z)|^2],
B_a=e_a^mu(nabla_mu chi+a_mu chi),                      (1)
```

is parity even: angular velocity and the improved gradient of a pseudoscalar
are both axial vectors. Canonically,

```text
H_top=C_left/(2I)+g J_a^left B_a                       (2)
```

up to the sign convention for `g`. Since `[C_left,J_a^left]=0`, all three
charges are exact zero-Bohr operators. The coupling generates stochastic active
rotations or precession. It is a gyroscopic phase-space interaction, not an
orientation-potential torque.

Derivative pseudoscalar couplings producing spin precession are standard in
axion phenomenology; see [Graham and Rajendran](https://arxiv.org/abs/1306.6088)
and [Graham et al.](https://arxiv.org/abs/1709.07852). Equation (1) is not
claimed as new.

## Exact Conformal Identity

Write the static metric as

```text
g_dS=N^2 g_opt,
chi_dS=N^-1 chi_opt.
```

Physical and optical orthonormal derivatives obey

```text
nabla_hat^dS chi_dS
=N^-2[D_hat^opt chi_opt-b_hat chi_opt],
b_hat=D_hat^opt log N.
```

Since `a_hat^dS=N^-1 b_hat`,

```text
N^2(nabla_hat^dS chi_dS+a_hat^dS chi_dS)
=D_hat^opt chi_opt.                                    (3)
```

Thus the improved physical bath is `N^-2` times the optical gradient. At equal
redshift, the lapse factors cancel from normalized auto/cross coefficients, so
the local action reproduces exactly

```text
C=diag(c_parallel,c_perp,c_perp)
```

from the preceding gradient theorems.

This improvement selects the static congruence and contains an undifferentiated
pseudoscalar, so it is not fully de Sitter invariant and breaks axion shift
symmetry. A raw shift-symmetric gradient retains the `b_hat chi_opt` term. Its
coincident radial variance approaches four times its transverse variance near
the horizon, and therefore does not realize the isotropic auto block assumed by
the gradient model.

## Proper-Time Spectrum

For one static point at lapse `N`, proper time is `tau=Nt` and

```text
B_tau=N^-2 B_opt.
```

Consequently,

```text
S_tau(omega)=N^-3 S_opt(N omega),
S_tau(0)=N^-3 S_opt(0),                                (4)
tau_B=N tau_B,opt.                                     (5)
```

For a spin-`L` sector, include its Casimir load in the weak-coupling parameter.
At fixed physical coupling `g`,

```text
gamma_tau tau_B
=g^2 L(L+1) N^-2 S_opt(0) tau_B,opt.                   (6)
```

The weak-coupling/Markov parameter therefore diverges at fixed `g` as the
horizon is approached. The gradient Davies channel is not uniform in the
collar limit at fixed coupling.

## Reference-State RMS Branch

After a declared optical smearing makes the gradient rms finite, the physical
bath rms scales as `N^-2`. On a declared spin-sector reference state, the
quadratic angular-momentum load is `L(L+1)`. If the resulting interaction RMS
is held fixed, then

```text
g=O[N^2/sqrt(L(L+1))].                                 (7)
```

Equations (4) and (7) imply

```text
gamma_tau=O[N/L(L+1)],
T_schedule=Theta[L(L+1)log(d)/N].                       (8)
```

On the collar scaling `rho/R~1/d`, `N=sin(rho/R)~1/d`, so

```text
T_schedule=Theta[d^3 log d].                            (9)
```

Combining the same shell optical geometry with the higher-spin center-distance
law gives

```text
theta=O[d^(-5/2)/sqrt(log d)].                         (10)
```

Equations (6) and (9) are the two sides of the physical tradeoff: fixed
coupling loses uniform growing-sector Davies control, while the declared
reference-state RMS budget makes the chosen sufficient heat schedule
parametrically long.

## Distributed Hard Target

For a lumped spin multiplet with `H_T=h(L^2)`, replacing `J_a` by `L_a` in (2)
gives the desired zero-Bohr target coupling. A local hard field target instead
requires an angular-current density,

```text
S_T,int=g_T int_(W_T) sqrt(-g) B_a(x) ell_T^a(x).       (11)
```

Its small-support expansion is

```text
int B_a ell_T^a
=B_a(p)L_a+partial_i B_a(p) M^(ia)+... .                (12)
```

The global charge term dominates only if the bath is sufficiently uniform over
the target support. The higher multipoles generally contain nonzero-Bohr
operators. No current theorem bounds (12) at the required center and angular
co-location scales. This is now the main local-action gate.

## Scope

The theorem assumes controlled smooth derivative smearing and treats a
state-dependent second moment as an input. This is not an operator-norm bound
on the unbounded smeared field, nor an all-state Davies estimate. The
logarithmic schedule is sufficient, not necessary. The theorem does not yet
derive the pseudoscalar or top stress tensor,
bound preparation energy, establish a uniform growing-spin Davies theorem, or
include the support apparatus and gravitational backreaction.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-pseudoscalar-gyroscope
PYTHONPATH=. python3 -m unittest tests.test_static_patch_pseudoscalar_gyroscope
```

Implementation: `qgtoy/static_patch_pseudoscalar_gyroscope.py`.
