# Authenticated Spherical Constraint Response

Status: exact spherical Hamiltonian-constraint theorem and authenticated bulk
supersolution certificate; lapse, field, and membrane-junction equations open.

## Universal Spherical Bound

On a time-symmetric spherical slice in areal radius, write

```text
dl^2=dr^2/f(r)+r^2 dOmega^2,
f(r)=N(r)-2Gm(r)/r,
N(r)=1-r^2/R^2.
```

The exact local control variable is

```text
q(r)=2Gm(r)/[rN(r)].
```

If `sup q<=beta<1`, then

```text
f(r)>=N(r)(1-beta)>0,
0<=g_rr/g_rr,dS-1<=beta/(1-beta).                 (1)
```

Thus the same bound excludes an areal-coordinate metric zero and controls the
radial metric response. It is stronger than a condition on `2GM/a` at the
support wall. A nonnegative uniform-density core of radius `epsilon`, followed
by vacuum out to `a`, has

```text
q(a)=C_wall/N(a),
q(epsilon)=C_wall a/[epsilon N(epsilon)].          (2)
```

The wall value can be arbitrarily small while the core value exceeds one. This
is a Hamiltonian-constraint counterexample, not a static dust solution.

## Skyrmion Bulk Bootstrap

Use `x=e f_pi r`, `lambda=1/(e f_pi R)^2`, and

```text
alpha=2G/(e^2 R^2 lambda).
```

Let `c_0(x)` be the directed cumulative mass obtained from the authenticated
fixed-de-Sitter profile. Define

```text
H_bulk=sup_[0<x<=x_w] c_0(x)/[x(1-lambda x^2)].    (3)
```

For the same field held fixed while the spherical radial constraint is solved,
the Skyrme gradient term is linear in the metric factor
`A=N-alpha c/x`. The self-consistent mass equation has the form

```text
c'(x)+k(x)c(x)=c_0'(x),  k(x)>=0.                  (4)
```

Hence `0<=c(x)<=c_0(x)`. If `alpha H_bulk<1`, then a first zero of `A` is
impossible and

```text
q(x)<=alpha H_bulk,
A(x)>=N(x)(1-alpha H_bulk)>0.                      (5)
```

This closes the bulk spherical Hamiltonian constraint for the fixed certified
field configuration. It does not show that the field also solves its
self-gravitating Euler-Lagrange equation.

## Authenticated Constants

Exact rational replay of the pinned AU.2 archive and sharp Newton tube, using
two radial subdivisions per parent cell and 64 regular-origin cells, gives

```text
H_bulk <= 29.246335626859388,
H_test,global <= 29.246335626859388,
H_exterior,fixed-background >= 10.634609934327349. (6)
```

The maximum upper cell is positive-radius cell 57, so the certified worst case
is internal rather than at the membrane. The global test-source value includes
the fixed-background Nambu-Goto wall mass; it happens not to enlarge the bulk
maximum. The upper-to-exterior-lower ratio is `2.7501089187`.

For the illustrative budget `beta=1/2`, `R^2/G=10^6`, and
`lambda=1/400`, equation (5) is guaranteed by

```text
e^2 >= 0.04679413700297502.                        (7)
```

The corresponding fixed-background exterior diagnostic is only
`e^2>=0.01701537589492376`, demonstrating why endpoint compactness is not a
controlled replacement for the local mass-function bound.

## Claim Boundary

The universal identity (1) is exact for spherical time-symmetric Hamiltonian
data. The Skyrmion result additionally certifies the bulk radial constraint for
the authenticated field held fixed. Neither result controls the lapse equation
or `g_tt`, for which `rho+p_r` is required. The calculation does not solve the
self-gravitating Skyrme profile, Israel junction conditions, rotating or
nonspherical constraints, or the off-center support problem. The membrane mass
is therefore retained only as a fixed-background test-source diagnostic.

The next theorem should add the spherically averaged collective rotational
energy measure. Combining its cumulative inertia with (3), then eliminating
`e`, is the direct route to a gravity-derived Casimir ceiling and the global
orientation-risk floor.

## Reproduction

```bash
python experiments/skyrmion_spherical_constraint_audit.py
python -m pytest -q tests/test_spherical_static_patch_constraint.py \
  tests/test_validated_skyrmion_constraint.py
```

Artifact:

```text
experiments/skyrmion_spherical_constraint_exact_certificate.json
SHA256 a180610fbdea4eecd75cdc7628216adab9289d5561704f60f750f7105fcaca47
```
