# Lorentzian Hadamard Static-Patch Net

Status: exact free conformal strip kernel and compact-test finite-wall limit;
Hadamard and factor classification use named primary theorems; the gravitational
observer corner remains open

## Optical Strip Kernel

For the conformally coupled massless scalar, write the static patch as

```text
g_dS=Omega^2 g_opt,
Omega(x)=sech(x/R),
g_opt=-dt^2+g_(H^3_R).
```

For spatial optical distance `d_H`, set

```text
C=cosh(d_H/R).
```

On the lower KMS strip `-2 pi R<Im z<0`, the exact optical two-point kernel is

```text
G_opt(z)=1/[8 pi^2 R^2 (C-cosh(z/R))].
```

It has the positive-type thermal spectral representation

```text
G_opt(z)=int_0^infinity
 sin(k d_H)/[4 pi^2 R sinh(d_H/R)]
 [exp(-ikz)+exp(-2 pi R k)exp(ikz)]
 /[1-exp(-2 pi R k)] dk.
```

At coincident spatial points the spatial factor is understood as its limit
`k/(4 pi^2)`. The code checks this spectral integral against the closed kernel
at an interior strip point. The equality itself follows analytically by
thermal-image expansion and elementary Laplace transforms.

## KMS And Euclidean Boundaries

At `z=-i tau`, `0<tau<2 pi R`, the strip kernel reduces exactly to the
Euclidean optical kernel. The opposite boundaries obey

```text
G(t-i(beta-epsilon);p,p')
 =G(-t-i epsilon;p',p),
beta=2 pi R.
```

This fixes the `i0` convention. For `Delta t=t-t'`, the Bunch-Davies boundary
is

```text
Lambda_BD^+(X,X')
 =lim_(epsilon->0+)
 1/[8 pi^2 R^2 (1-Z_epsilon)],

Z_epsilon
 =sech(x/R)sech(x'/R)cosh((Delta t-i epsilon)/R)
  +tanh(x/R)tanh(x'/R)cos(gamma).
```

The conformal relation is

```text
Lambda_BD^+=cosh(x/R)cosh(x'/R) G_opt.
```

For spacetime test sources, the conformal source map is
`F -> Omega^3 F`; point-kernel multiplication is not the complete smeared
statement.

## Compact-Test Wall Limit

Let `F` and `G` be smooth compact spacetime tests whose causal hull intersects
a time-zero surface inside `x<B`. Green's identity reduces their two-point
pairing to smooth compact Cauchy data. If the Dirichlet wall satisfies

```text
X>B+T,
```

where `T` bounds the time extent of the causal hull, finite propagation for the
radial wave equation makes those evolved Cauchy data independent of the wall.
The all-angular equal-time theorem in `static_patch_all_angular.md` then applies
to the resulting field and momentum data.

For each compact pair of spacetime tests, the finite-wall quasifree two-point
forms therefore converge to the optical/Bunch-Davies form. This is pairwise
compact-test convergence. Promoting it to convergence in the full topology of
`D'(M_static x M_static)` additionally requires equicontinuity or uniform
distribution-order bounds on each compact and the nuclear Schwartz-kernel
theorem. No convergence of the finite Type-I von Neumann closures is asserted.

The explicit hard radial spectral cutoff used by earlier numerical stages is
not needed in this analytic wall theorem. If one retains simultaneous finite
`L` and `K` regulators, an arbitrary joint-path estimate requires additional
wall-uniform functional-calculus bounds; selected iterated or diagonal limits
remain the safe claim.

## Hadamard Identification

Near a short spacelike geodesic,

```text
1-Z=sigma/R^2+O(sigma^2),
```

so

```text
Lambda_BD^+=1/[8 pi^2 sigma_epsilon]+less singular terms.
```

The executable ratio `8 pi^2 sigma Lambda` tends to one. That numerical limit
is only a coefficient audit, not a wavefront-set proof.

The full claim uses established results:

1. the analytic de Sitter vacuum has the static-patch thermal boundary and
   de Sitter Bisognano-Wichmann property;
2. passive, in particular KMS, linear-field states on stationary globally
   hyperbolic spacetimes satisfy the microlocal spectrum condition;
3. local Hadamard form is equivalent to the microlocal spectrum condition.

Primary sources:

- Bros, Epstein, and Moschella,
  [de Sitter analyticity and thermal effects](https://arxiv.org/abs/gr-qc/9801099);
- Sahlmann and Verch,
  [passivity and the microlocal spectrum condition](https://arxiv.org/abs/math-ph/0002021);
- Sahlmann and Verch,
  [Hadamard form and wavefront spectrum](https://arxiv.org/abs/math-ph/0008029).

Thus the exact strip boundary is the Bunch-Davies quasifree Hadamard state, not
merely a kernel with the right temperature.

## Local Factors And Core

Let

```text
M(O)=pi_BD(A(O))''
```

for the Weyl algebra localized in a regular diamond `O` with nonempty causal
complement inside global de Sitter. Verch's Theorem 3.6(g) implies that `M(O)`
is the hyperfinite Type `III_1` factor. In the global de Sitter Bunch-Davies
representation, the static patch is the domain of dependence of an open
hemisphere with smooth boundary and has the opposite patch as causal
complement, so the theorem applies to the patch algebra. If the patch were
instead treated as the entire ambient spacetime, this argument would not
apply.

Primary source:

- Verch,
  [Local definiteness, primarity and quasiequivalence of quasifree Hadamard
  states](https://arxiv.org/abs/funct-an/9609004).

For the whole patch, Bros-Epstein-Moschella give the KMS and Reeh-Schlieder
properties. Cyclicity for the patch and opposite patch plus locality makes the
Bunch-Davies vector separating, hence the patch state is faithful. Tomita-
Takesaki theory then identifies its modular flow with geometric static time
after the `2 pi R` rescaling. Its continuous core

```text
M(P) crossed_(sigma_BD) R
```

is therefore a hyperfinite Type `II_infinity` factor by standard crossed-product
duality.

This is not yet the gravitational observer algebra of CLPW. Their Type
`II_infinity` crossed product and Type `II_1` finite corner additionally require
an observer clock, Hamiltonian constraint, positive-energy projection, and
trace normalization. None of those follows from free-field factor
classification alone.

## Claim Boundary

Established here:

1. exact Lorentzian optical and Bunch-Davies strip kernels;
2. exact KMS opposite-boundary and Euclidean continuation identities;
3. pairwise compact-spacetime-test finite-wall convergence using finite propagation and
   the all-angular equal-time theorem;
4. theorem-backed Bunch-Davies Hadamard identification;
5. theorem-backed hyperfinite Type `III_1` local/static-patch algebras and
   Type `II_infinity` continuous core.

Not established:

1. convergence of finite-regulator von Neumann closures to Type `III_1`;
2. an arbitrary simultaneous wall/angular/spectral cutoff path;
3. the observer-clock constraint and positive-energy Type `II_1` corner;
4. a finite gravitational trace or generalized-entropy identity;
5. backreaction or interacting quantum gravity.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-lorentzian-hadamard
PYTHONPATH=. python3 -m unittest tests.test_static_patch_lorentzian_hadamard
```
