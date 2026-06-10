# Controlled Compactness-Localization Branch Obstruction

This note combines two already explicit ingredients of the observer program:

1. the compact spherical-top EFT radius floor for a definite spin sector; and
2. the shrinking near-horizon support scales required by the local gradient
   common-mode analysis and the distributed hard-current design theorem.

The result closes one controlled perturbative branch. It is not a global
channel no-go or Einstein-matter collapse theorem.

The lower-radius scaling is not claimed as new. It is closely related to
classical general-relativistic size-angular-momentum inequalities such as
[Dain's body inequality](https://arxiv.org/abs/1305.6645), which gives the
parametric relation `R_body^2` bounded below by `G|J|` under its own symmetry
and energy hypotheses. The project-specific candidate is the collision with the
channel-derived upper support scale.

## Declared Model

Let the hard target and reference top occupy distinct, equal-redshift,
equal-radius nonoverlapping thin-shell worldtubes. Identify the top spin with the
protected hard-sector spin `L`, so `d=2L+1`. Model each top by

```text
I=kappa m a^2,
E_rot/m<=zeta,
2G(m+E_rot)/a<=chi,
```

where `a` is a three-dimensional proper enclosing radius. This last
identification is an assumption: the hard-current theorem by itself controls
optical or tangential support, not the full material body.

The finite-top capacity theorem gives

```text
L(L+1)<=kappa chi^2 zeta a^4/[2G^2(1+zeta)^2],
```

and therefore the exact proper-radius floor

```text
a_min=[2G^2(1+zeta)^2L(L+1)/(kappa chi^2 zeta)]^(1/4).   (1)
```

At large `d`,

```text
a_min/R ~ C_min (sqrt(G)/R)d^(1/2),
C_min=[(1+zeta)^2/(2kappa chi^2 zeta)]^(1/4).            (2)
```

## Optical-To-Proper Conversion

Write `u=rho/R`. On the static shell, `r=R cos(u)`. If two centers have
optical separation `y`, their exact same-shell angle is

```text
theta(y,u)=2 asin[tan(u)sinh(y/2)].                      (3)
```

The exact center distance on the static spatial slice is

```text
D_slice=2R asin[cos(u)sin(theta/2)]
       =2R asin[sin(u)sinh(y/2)]
       =R sin(u)y[1+O(y^2)].                             (4)
```

Thus the collar `rho/R=1/d` contributes one additional inverse power of `d`
when an optical support law is converted to a proper material scale.

## Leading Nonoverlap Obstruction

The higher-spin gradient theorem gives the leading local-common-mode
co-location law

```text
y_d=sqrt[A/(dL(L+1)log d)]
   ~2sqrt(A)d^(-3/2)/sqrt(log d).                        (5)
```

For distinct equal-radius thin-shell supports, disjointness requires each proper
enclosing radius to be no larger than half the static-slice center separation.
Equations (3)-(5) therefore give the leading ceiling

```text
a_nonoverlap/R ~ sqrt(A)d^(-5/2)/sqrt(log d).            (6)
```

Combining (2) and (6),

```text
a_nonoverlap/a_min
 ~ [sqrt(A)/C_min][R/sqrt(G)]d^(-3)/sqrt(log d).         (7)
```

At fixed `R^2/G`, this ratio tends to zero. Hence no growing-`d` sequence can
remain inside the controlled local-common-mode branch while satisfying the
compact spherical-top radius floor and distinct equal-radius nonoverlap. This
does not control hypothetical nonperturbative large-separation behavior. The
parametric crossover of the controlled envelopes obeys

```text
d^3 sqrt(log d)=O(R/sqrt(G)),
d=O[(R/sqrt(G))^(1/3)/(log d)^(1/6)].                    (8)
```

Equation (5) is a leading perturbative necessary law, so a finite integer found
by crossing (1) and (6) is an illustrative asymptotic crossover, not an exact
global channel cutoff.

## Sufficient GKSL Design Closures

The hard-current theorem also gives sufficient worst-case support designs. For
default `O(1)` transfer constants,

```text
generic:          a/R ~ c_g d^(-4)/log d,
dipole-cancelled: a/R ~ c_q d^(-5/2)/sqrt(log d),        (9)
```

with `c_g=2A/3` and
`c_q=min[sqrt(A_mismatch),sqrt(4A/3)]` in the implemented normalization.
Using the minimum-energy top at the selected proper radius, the compactness
utilization `U=2GE_min/(chi a)` satisfies

```text
U_generic
 ~ (G/R^2)(1+zeta)/[chi sqrt(2kappa zeta)c_g^2]
    d^9(log d)^2,

U_dipole
 ~ (G/R^2)(1+zeta)/[chi sqrt(2kappa zeta)c_q^2]
    d^6 log d.                                           (10)
```

These divergences close the declared sufficient thin-shell design certificates. They do
not prove that every larger support fails, because model-specific
cancellations, overlapping distinguishable sectors, or a different recovery
channel can evade their premises.

## Numerical Illustration

For `R=1`, `G=10^-12`, `kappa=2/3`, `chi=1/2`, `zeta=1/4`, and unit mismatch
and multipole coefficients, the certificate reports:

```text
leading nonoverlap crossover: L=30, d=61,
generic GKSL design crossover: L=6, d=13,
dipole-cancelled design crossover: L=30, d=61.
```

These integers are parameter-dependent diagnostics, not universal physical
predictions.

## Scope And Replacement Gate

The obstruction assumes:

- the same definite spin `L` loads the compact top and protected hard sector;
- a spherical-top inertia law and stipulated compactness margin;
- a thin-shell three-dimensional enclosing radius bounded by the same-shell
  static-slice support distance;
- the local perturbative gradient common-mode law;
- distinct, equal-size, nonoverlapping worldtubes; and
- `O(1)` mismatch and jump-transfer constants along the sequence.

It also does not infer directional-reference quality from the Casimir alone. A
physical model must specify the prepared spin state or reducible encoding that
actually carries the gyroscopic orientation resource.

It does not derive a global channel no-go, stress tensor, binding energy,
lifetime, rotating Einstein-matter solution, Kossakowski or Lamb-shift
stability, or a Davies limit uniform in `L`. A physical successor theorem must
choose a named matter source,
derive its current moments and support stress, and test whether the resulting
joint localization/lifetime/gravity window is empty or nonempty.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-localization-backreaction
PYTHONPATH=. python3 -m unittest tests.test_static_patch_localization_backreaction
```
