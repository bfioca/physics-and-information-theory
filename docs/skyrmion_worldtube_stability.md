# Skyrmion Worldtube Radial Stability And Finite Pinning

Status: step-converged conditional `l=0` adiabatic curvature evidence plus an
analytic no-go for exact topology under a simple finite boundary pinning
potential.

## Radial Energy Curvature

Along the family of hard-Dirichlet profiles re-solved at each centered wall
radius `a`, hold the membrane tension `sigma` fixed and write

```text
E(a)=E_Sk(a)+4 pi sigma a^2 sqrt(N(a)),
N(a)=1-lambda a^2.                                     (1)
```

The radial derivative is

```text
E'(a)=4 pi a^2[-p(a)+sigma K(a)],
K(a)=2sqrt(N)/a-lambda a/sqrt(N).                       (2)
```

Young-Laplace balance `p=sigma K` proves stationarity only. At a stationary
point,

```text
E''(a)=4 pi a^2[-p'(a)+sigma K'(a)],                    (3)

K'(a)=-2sqrt(N)/a^2-3lambda/sqrt(N)
      -lambda^2a^2/N^(3/2).                            (4)
```

The certificate obtains `p'(a)` by centered finite differences along the
re-solved Dirichlet branch. For `mu=1`, `lambda=0.0025`, and `a=4`,

```text
p=0.000926658743,
sigma=0.001931779647,
p'=-0.00243950031,
K'=-0.1302354572,
E''=0.4399062320>0.                                    (5)
```

Halving the radius difference changes `E''` by less than `3e-5` relatively.
The Nambu-Goto shell kinetic mass and corresponding shell-only frequency are

```text
M_wall=4 pi sigma a^2/N^(3/2)=0.4129339430,
omega_wall=sqrt(E''/M_wall)=1.0321427485.               (6)
```

This gives step-converged numerical evidence for a local minimum only along the
declared adiabatic centered spherical family. It is not a validated-numerics
proof or the spectrum of the fully coupled wall-profile system.

The `1.03214` value uses the profile-relaxed branch stiffness but only the bare
wall kinetic mass. A moving ideal wall drags the branch shape
`chi=partial_aF_a`, adding `pi int W chi^2` to the adiabatic inertia and mixing
the wall with fixed-wall profile modes. Exploratory differencing gives
`int W chi^2 approximately 0.063759`, which would lower the adiabatic estimate
to about `0.847`. The exact two-block theorem in
`coupled_radial_wall_gap.md` gives a conservative `0.198` if that lift norm and
the current curvature are certified. Neither diagnostic is presently a
validated coupled frequency.

A separate direct form argument now supplies the validated coupled statement.
After exact Young-Laplace elimination, the witness
`v=1/[(x-9/4)^2+8]` has positive bulk and moving-wall coefficients on the
authenticated exact profile. It proves

```text
omega_hat_l0>=1/50
```

for the complete spherical profile-membrane channel. Thus `0.847` and `0.198`
should be read only as possible sharpenings of the conservative certified
floor, not as the evidence for its positivity. See
`skyrmion_moving_wall_radial_gap.md`.

## Finite-Pinning No-Go

Replace the ideal multiplier by the smooth boundary energy

```text
E_pin=4 pi kappa_pin a^2 sqrt(N)(1-cos F_w).             (7)
```

Its Robin condition is

```text
N(a^2+8sin^2(F_w))F'_w/4
+kappa_pin a^2sqrt(N)sin(F_w)=0.                        (8)
```

Exact `B=1` requires `F_w=0`. At finite `kappa_pin`, (8) then requires
`F'_w=0`. ODE uniqueness gives the trivial solution, contradicting the
interior condition `F(0)=pi`. A simple finite pinning potential therefore
cannot preserve both exact unit baryon number and a nontrivial profile.

For large stiffness, with `y=F'_D(a)<0`,

```text
F_w=-sqrt(N)y/(4kappa_pin)+O(kappa_pin^-2),

1-B=N^(3/2)|y|^3/(96 pi kappa_pin^3)
    +O(kappa_pin^-4),

E_soft-E_D=-pi a^2N^(3/2)y^2/(8kappa_pin)
           +O(kappa_pin^-2).                            (9)
```

For the default hard wall, the three leading coefficients are

```text
F_w=0.0215250870/kappa_pin+...,
1-B=2.11637984e-6/kappa_pin^3+...,
E_soft-E_D=-0.0456378629/kappa_pin+....                 (10)
```

An exact finite-stiffness model therefore needs boundary topological degrees
of freedom or another mechanism beyond the stated smooth pinning term.

## Off-Center Gate

A static de Sitter observer at radius `r_0` has proper acceleration

```text
A_0=r_0/[R^2 sqrt(1-r_0^2/R^2)].                        (11)
```

In Fermi coordinates the local lapse and spherical-wall curvature contain
`l=1` terms. Schematically,

```text
g_00=-(1+A_iX^i)^2+O(X^2/R^2),
K=2/b+A.n+O((Ab)^2,b^2/R^2).                            (12)
```

Uniform tension then requires an `l=1` traction and a supporting anchor or
strut. Translating the centered solution is not enough: the matter profile,
membrane, and anchoring stress must be solved together. This is also the first
place where the centered current-dipole cancellation can fail.

The cavity treatment can be compared with [Giacomini et al. on gravitating
Skyrmions in a cavity](https://arxiv.org/abs/1708.06863), while the rotating
fixed-background normalization follows [Hata and Kikuchi](https://arxiv.org/abs/1002.2464).

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-worldtube-stability
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_worldtube_stability
```
