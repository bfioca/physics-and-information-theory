# Centered Massive-Skyrmion Worldtube Baseline

Status: conditional centered source model; off-center support and stability open.

## Boundary Action

Write `U=Y^0 I+iY^a tau_a`, `Y^A Y^A=1`, and introduce a spherical timelike
membrane with induced metric `gamma`:

```text
S=S_Sk[M_-]-sigma int_Sigma sqrt(-gamma)
  +int_Sigma sqrt(-gamma) Lambda_A(Y^A-Y_*^A),
Y_*=(1,0,0,0).                                           (1)
```

The multiplier imposes the covariant ideal-mirror condition

```text
U|_Sigma=I,  F(x_w)=0.                                   (2)
```

Together with `F(0)=pi`, this compactifies the interior ball and gives exact
hedgehog baryon number one. The boundary preserves vector isospin, parity, and
the collective orientation `U -> A U A^dagger`.

## Centered Force Balance

For fixed static-patch lapse `N=1-lambda x^2`, the dimensionless radial pressure
is

```text
p_bar=N F'^2/8+N sin^2(F)F'^2/x^2
      -sin^2(F)/(4x^2)-sin^4(F)/(2x^4)
      -mu^2(1-cos F)/4.                                  (3)
```

At the hard wall this reduces to `p_bar=N_w F_w'^2/8`. The centered static
shell mean curvature is

```text
K_bar=2sqrt(N_w)/x_w-lambda x_w/sqrt(N_w).               (4)
```

Young-Laplace balance selects `sigma_bar=p_bar/K_bar`. Positive tension can
balance positive interior pressure only for

```text
x_w<sqrt[2/(3lambda)]=sqrt(2/3)x_c.                      (5)
```

At `mu=1`, `lambda=0.0025`, and `x_w=4`, the executable shooting solution has
`b=1.5799534`, exact wall baryon number, positive equilibrium tension, and a
wall-to-interior mass ratio below two percent. Step halving leaves the interior
mass and inertia stable at the declared tolerance.

This is not a stability theorem. The tension is chosen by centered force
balance, and the wall is an ideal constraint. A finite-stiffness pinning action

```text
S_pin=-kappa int_Sigma sqrt(-gamma)(1-Tr U/2)             (6)
```

would produce Robin data and baryon leakage at finite stiffness. Radial and
nonspherical wall modes, a wall UV completion, Einstein junction conditions,
and the actual off-center accelerated support must be derived.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy massive-skyrmion-worldtube
PYTHONPATH=. python3 -m unittest tests.test_massive_skyrmion_worldtube
```

Primary context:

- [Giacomini et al., gravitating Skyrme configurations in a
  cavity](https://arxiv.org/abs/1708.06863), as a mirror-boundary precedent,
  not a `B=1` or physical-wall theorem.
- [Bousso and Polchinski, top-form flux and membrane
  pressure](https://arxiv.org/abs/hep-th/0004134), as one possible covariant
  pressure-sector completion.
