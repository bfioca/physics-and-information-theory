# Variational Centrifugal Quadrupole Probe

The exploratory centrifugal solver differentiates sampled Hessian blocks in
strong form. The validation route instead begins from the exact local
quadratic density

```text
q[y]=y^T C y+2y^T M y'+y'^T P y'
```

in the regular fields `y=(f,g)`. The piecewise-linear calculation in
`qgtoy/centrifugal_skyrmion_variational.py` assembles this form directly in a
piecewise-linear trace space. It imposes

```text
f(0)=g(0)=0,  g(a)=0,
```

and leaves `f(a)` free. The Robin-equivalent boundary form coefficient is

```text
b_wall=-(P_ff beta+M_ff),
```

so stationarity reproduces the previously derived pure-tension Robin condition
`f'(a)=beta f(a)` when the exact wall identities `P_fg=M_ff=0` are used. This
is a discretization-consistency construction, not an independent derivation of
the membrane second variation.

This formulation has three advantages needed by the interval proof:

1. the assembled matrix is symmetric by construction;
2. no numerical derivatives of `P` or `M` occur;
3. the membrane contribution is part of the same quadratic form whose
   coercivity is being tested.

The default nested meshes produce positive generalized eigenvalue estimates
approaching `0.35348` and a positive wall form. The finest weak-form solution
agrees with the separately implemented strong-form finite-difference solution to about
`1.4e-4` in the declared scaled probe norm. The two solvers share the Hessian,
source, and Robin generator, so this checks discretization consistency rather
than their common physical normalization. These values are **not** a
coercivity proof: floating profile interpolation and Gauss quadrature remove
the exact variational ordering, so they have no certified one-sided relation to
the continuum eigenvalue.

The trace space also imposes only `f(0)=g(0)=0`, not the full smooth Frobenius
relation `f+g=O(x^3)`. Because the principal matrix degenerates as `x^2`, the
validation theorem must either prove that this trace space has the intended
Friedrichs closure or use nonsingular Frobenius variables explicitly.

The next rigorous step is to enclose the authenticated AU.3b profile tube,
`C,M,P`, the wall coefficient, source, and quadrature defects with rational
intervals. After resolving the origin domain, a matrix Green-parametrix or a
validated low-mode/complement estimate must prove a strict lower spectral
bound. Only after that bound exists can the Galerkin residual give a certified
response-error enclosure.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_variational_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_variational.py \
  tests/test_centrifugal_skyrmion_variational_audit.py
```
