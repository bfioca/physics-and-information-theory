# Transformed Centrifugal Origin Density

The exact indicial theorem identifies the regular coupled fields as

```text
g=x v(x^2),
f=-x v(x^2)+x^3 u(x^2).
```

To test this substitution against the full local Hessian, write

```text
t=x^2,
F=pi-x w(t),
s(t)=sin(sqrt(t)w(t))/sqrt(t),
c(t)=cos(sqrt(t)w(t)).
```

Here `s(0)=w(0)`, so both profile kernels are entire in `t` for an analytic
regular profile. Direct term-by-term substitution into the complete same-action
`K=2` density proves

```text
H_static(x)=x^2 H_hat(t;w,w_t,v,u,v_t,u_t).
```

The executable expression for `H_hat` contains no negative power of `t`.
Exact `Fraction` evaluation at the center gives

```text
H_hat(0)=v(0)^2/6,
```

independent of the origin slope, mass, curvature, `u(0)`, or the displayed
time derivatives. Three direct evaluations of the original untransformed
density reproduce `x^2 H_hat` with maximum relative discrepancy `2.61e-18`.

The same exact indicial algebra resolves the forced resonance at `p=3`. The
leading Euler source is

```text
F_3=b(1-4b^2)(1,-3/2)/45,
```

and the two rows of `K(3)` have the same `-3/2` ratio. Hence `F_3` lies in
`range K(3)`, the zero-linear-amplitude particular branch has a log-free cubic
start, and its initial coefficients obey

```text
(10+56b^2)v_t(0)-(4+56b^2)u(0)=b(1-4b^2).
```

This closes the algebraic density cancellation, but it is not yet the desired
origin-transfer theorem. Changing the integration variable gives

```text
H_static dx=(sqrt(t)/2) H_hat(t) dt.
```

The transformed variational problem therefore retains a regular-singular
weight. The next proof must derive the weighted Euler-Lagrange system, identify
its two-dimensional Friedrichs trace space, and validate the fundamental
transfer matrix from `t=0` to `t=1/256`. Only that interval transfer may replace
the leading Robin enclosure in a continuum inverse certificate.

The exact matrix form fixes that next calculation. Block the original local
Hessian as

```text
H=[[C,M],[M^T,P]],
C=Cbar(t), M=x Mbar(t), P=x^2 Pbar(t),
w=(u,v)^T,
S=[[t,-1],[0,1]],
B=[[3t,-1],[0,1]],
D=[[2t^2,-2t],[0,2t]].
```

Then `y=xSw` and `y'=Bw+Dw_t`, and

```text
H_hat=w^T A w+2w^T N w_t+w_t^T R w_t,
A=S^T Cbar S+S^T Mbar B+B^T Mbar^T S+B^T Pbar B,
N=S^T Mbar D+B^T Pbar D,
R=D^T Pbar D.
```

With `rho=sqrt(t)/2`, the strong weighted equation to validate is

```text
-R w_tt+[N-N^T-R_t-R/(2t)]w_t
  +[A-(N^T)_t-N^T/(2t)]w = F.
```

This is Fuchsian, not an ordinary nonsingular second-order initial-value
problem. The certificate should construct two homogeneous regular columns and
one forced particular column by exact Frobenius recurrence, use the already
proved indicial factorization to invert every recurrence matrix for powers
`p>=5`, and enclose the Taylor remainder on the full origin cell. At the
cutoff, map the affine `(u,v,u_t,v_t)` enclosure back to `(f,g,f',g')` and feed
that boundary subspace directly into the global interval solve. Keeping the
subspace avoids an unnecessary interval matrix inverse at the origin.

The first recurrence is now closed exactly in
`centrifugal_skyrmion_frobenius.md`. In particular, the full leading equation
shows that the normalized linear homogeneous column generally has
`v_t(0) != 0`; the pure indicial vector alone is not a finite-cutoff column.
The remaining task in this file's gate is the correlated Taylor remainder and
finite-cell transfer.

## Reproduce

```bash
PYTHONPATH=. python experiments/centrifugal_skyrmion_transformed_origin_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_transformed_origin.py tests/test_centrifugal_skyrmion_transformed_origin_audit.py
```

The source-hashed artifact is
`experiments/centrifugal_skyrmion_transformed_origin_certificate.json`.

## Claim Boundary

This is an exact algebraic desingularization of the full local static Hessian
density plus an exact leading forced-resonance compatibility. It does not prove
Friedrichs-domain equivalence, a finite-cutoff
Frobenius remainder, the two-parameter transfer map, coercivity, or a validated
forced response.
