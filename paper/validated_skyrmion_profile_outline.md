# Computer-Assisted Existence And Radial Stability Of A Dirichlet-Confined Massive Skyrmion

Status: selected Paper A specialist-review draft. Mandatory proof,
exact-replay, package-audit, and internal referee gates pass.

## Central Theorem

For the prescribed dimensionless massive Skyrmion boundary-value problem

```text
mu^2=1, lambda=1/400, F(0)=pi, F(4)=0,
```

there exists a unique solution in the certified augmented Newton ball of radius
`1/250` at norm weight `omega=3/4`. The solution is strictly decreasing, has
strictly negative wall slope, and has finite positive dimensionless rotor
inertia.

The manuscript also includes two authenticated consequences of the same
solution: a fixed-wall radial Friedrichs gap
`omega_hat_rad>=1/5`, and the sharp nonzero oscillatory `p^-3` tail of a
finite optical inertia-density transform. A qualitative analytic implicit-function
argument gives a locally unique open branch in mass, curvature, and wall radius,
but no explicit parameter-box width is yet certified.

The conservative displayed certificate is

```text
Y        <= 0.002296,
Z0       <= 0.000078,
Z2       <= 78.733,
p(r)     < -0.00107,
q(r)     < 0.31501,
F'(4)    in [-0.09465,-0.08746],
I_rot    in [21.149,48.921].
```

Canonical combined AU.1/AU.2 archive:
`experiments/skyrmion_au2_global_tail_exact_certificate.json`,
SHA-256
`1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9`.
The companion audit summary is
`experiments/skyrmion_newton_reduced_hessian_rounded_audit_result.json`.

## Claim Boundary

The paper claims a certified base solution and qualitative locally unique
analytic branch for a prescribed fixed-background Dirichlet problem. It does
not claim global uniqueness, full dynamical stability, a self-gravitating
Einstein-Skyrme solution, a physical membrane completion, a bath factor, or a
de Sitter observer algebra.

## Technical Contribution

1. A regular-origin Volterra contraction identifies the physical slope family
   and its first two parameter sensitivities.
2. A rational `C2` spline, exact five-harmonic residual evaluation, and Barta
   witness certify the approximate-profile Jacobi operator.
3. A factored Green parametrix supplies same-operator `C0,C1,C2` inverse bounds.
4. A trace representer and nonzero scalar Schur complement invert the augmented
   shooting operator.
5. Row-local Green bounds, a center-equation Hessian identity, and a weighted
   trace remove the global `C0*C2` loss in the Newton estimate.
6. Fixed-grid rational outward rounding controls denominator growth without a
   floating theorem premise.
7. Post-Newton interval quadrature certifies monotonicity, wall slope, and
   inertia for the exact solution.

## Proposed Structure

1. Model, nondimensionalization, prior-art comparison, and imposed Dirichlet data.
2. Regular origin family and parameter sensitivities.
3. Rational approximate profile and nonlinear residual.
4. Coercive Jacobi operator, Green parametrix, and augmented Schur complement.
5. Reduced Hessian and Newton-Kantorovich closure.
6. Monotonicity, wall slope, and rotor inertia.
7. Reproducibility, exact artifacts, and independent rerun instructions.
8. Direct comparison with McLeod--Troy, Creek--Donninger--Schlag--Snelson,
   Nguyen--Nguyen, and endpoint-asymptotic prior art.
9. Limitations and the route to supported and self-gravitating models.

## Review Gate Disposition

Gates 1--5 below are closed in the checked package.  Gate 6 is a desirable
quantitative extension, not a blocker for external review of the present
qualitative analytic branch.

1. Independent rerun of the exact artifact from a clean environment.
2. Explicitly distinguish the result from the prior rational
   computer-assisted whole-space Skyrmion proof of Creek et al.
3. A proof appendix that states the Banach spaces, augmented inverse, Green-row
   Neumann identity, and every fixed-grid rounding operation explicitly.
4. Archive the generator inputs and a compact hash/provenance ledger for the
   rational spline and accepted certificate.
5. External review of the local-uniqueness claim and boundary-model scope.
6. Deferred enhancement: close a rational `(mu^2, lambda)` rectangle at fixed
   wall radius.  The manuscript prominently states that the present analytic
   branch has no certified numerical width.
