# Global Centrifugal Quadrupole BVP

This note solves the default `O(Omega^2)` Skyrmion quadrupole numerically in the
regular two-channel variables derived in
`centrifugal_skyrmion_deformation.md`. The result is step-converged exploratory
evidence for a regular moving-wall branch. It is not validated numerics and is
not yet a distributionally conserved Einstein source. The subsequent
completed-stress audit establishes floating smooth-bulk conservation.

## Radial System

Let `y=(f,g)`. Write the angular-averaged static Hessian density in block form

```text
delta^2 E = y^T C y+2y^T D y'+y'^T A y'.
```

Let the rotational first variation be

```text
delta R = s0^T y+s1^T y'.
```

The coupled variational equation is

```text
-(A y'+D^T y)'+D y'+C y=s0-s1'.                 (1)
```

The executable obtains `(A,D,C,s0,s1)` only from the source-hashed local
target-space generator. It differentiates the coefficient blocks numerically
on a radial mesh and solves the resulting block-tridiagonal system.

## Regular Origin

The leading Hessian coefficients have

```text
A=x^2 A0+...,
D=x D0+...,
C=C0+....
```

For `y=x^p v`, the indicial matrix is

```text
I(p)=-p(p+1)A0-(p+1)D0^T+pD0+C0.
```

The four indicial powers are

```text
p=1, 3, -2, -4.
```

The regular vectors on the default branch are

```text
p=1: f/g=-1.00000000299,
p=3: f/g= 0.04172747341.
```

This confirms the smooth expansion anticipated from the target-space fields:
an anisotropic-linear mode with `f=-g+O(x^3)` and an independent cubic mode.
The solver imposes the resulting two-dimensional regular subspace at a small
positive origin radius.

## Wall Conditions

At `x=a`, the ideal mirror and pure-tension membrane give

```text
g(a)=0,
f'(a)=beta f(a),
```

where the certified wall law yields

```text
beta=-2/a-N'/(2N)-4sigma k2/(N F_w'^2),
k2=K'(a)+6/[a^2sqrt(N_a)].
```

For the default worldtube,

```text
beta=-0.7527703900842937.
```

The membrane shape coefficient is reconstructed from mirror pullback as

```text
xi2=-f(a)/F'_w.
```

## Default Solution

For

```text
mu=1,
lambda=0.0025,
a=4,
sigma=0.001931779647,
```

the finest declared mesh gives

```text
max |f| =0.3053035319,
max |g| =0.2735765404,
integral_0^a (f^2+g^2) dx =0.1952068369,
f(a)=-0.02525062606,
xi2=-0.2873444807.
```

These are coefficients of the quadratic rotational tensor; physical
deformation smallness still requires multiplying by the appropriate
dimensionless angular-velocity or collective-state factor.

The linear-system and wall residuals are

```text
max algebraic residual =4.55e-13,
|f'(a)-beta f(a)|      =2.02e-16,
g(a)                   =0.
```

## Refinement Audit

At sample radii `(0.25,0.5,1,2,3,4)`, the maximum scaled change between the
`201`- and `401`-node solutions is

```text
1.2990263459e-4.
```

Changing the origin cutoff from `0.02` to `0.01` changes the same combined
diagnostic by

```text
8.4471346337e-6.
```

Refining the background-profile RK4 step from `0.002` to `0.001` changes it by

```text
1.6108815337e-7.
```

The wall-shape sequence is

```text
mesh nodes 101,201,401:
-0.2916873339, -0.2888227334, -0.2873444807;

origin cutoffs 0.04,0.02,0.01 at 401 nodes:
-0.2873369727, -0.2873444807, -0.2873482227;

profile steps 0.004,0.002,0.001 at 401 nodes:
-0.2873451274, -0.2873444807, -0.2873443196.
```

The first-order wall derivative is responsible for the visibly slower mesh
sequence, while origin and profile refinements are already much smaller.

## Interpretation

The correct two-channel and moving-wall completion does not show an immediate
large-response obstruction at the default point. This is evidence against
promoting the rigid-source failure into a physical no-go: the missing
centrifugal branch appears numerically regular and moderate.

The result still cannot be inserted into the Zerilli Green function. The next
required steps are:

1. derive a higher-order or variational discretization with an interval
   enclosure and prove existence/uniqueness or coercivity;
2. derive the membrane surface stress and distributional wall balance, now
   that the deformed bulk stress closes both conservation identities under
   mesh refinement;
3. project that conserved source and reconstruct an invariant gravitational
   observable.

No novelty claim is attached to the numerical solution itself.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_bvp_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_bvp.py \
  tests/test_centrifugal_skyrmion_bvp_audit.py
```

The source-hashed artifact is
`experiments/centrifugal_skyrmion_bvp_certificate.json`, SHA-256
`ddc489d4b0b5b3bcbd71fd36afd1b217f58b04c13cbdbb0f2be7ff7df9f95a76`.
