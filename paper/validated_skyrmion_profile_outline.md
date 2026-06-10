# Computer-Assisted Validation Of A Massive Hard-Wall Skyrmion Profile

Status: Paper A outline; theorem closed, novelty review and manuscript pending.

## Central Theorem

For the prescribed dimensionless massive Skyrmion boundary-value problem

```text
mu^2=1, lambda=1/400, F(0)=pi, F(4)=0,
```

there exists a unique solution in the certified augmented Newton ball of radius
`1/250` at norm weight `omega=3/4`. The solution is strictly decreasing, has
strictly negative wall slope, and has finite positive dimensionless rotor
inertia.

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

Exact archive:
`experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json`,
SHA-256
`c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff`.
The companion audit summary is
`experiments/skyrmion_newton_reduced_hessian_rounded_audit_result.json`.

## Claim Boundary

The paper claims existence and local uniqueness for one prescribed
fixed-de-Sitter hard-wall problem. It does not claim global uniqueness,
dynamical stability, a self-gravitating Einstein-Skyrme solution, a physical
membrane completion, or a de Sitter observer algebra.

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

1. Model, nondimensionalization, and hard-wall boundary data.
2. Regular origin family and parameter sensitivities.
3. Rational approximate profile and nonlinear residual.
4. Coercive Jacobi operator, Green parametrix, and augmented Schur complement.
5. Reduced Hessian and Newton-Kantorovich closure.
6. Monotonicity, wall slope, and rotor inertia.
7. Reproducibility, exact artifacts, and independent rerun instructions.
8. Comparison with numerical Skyrmion cavities and computer-assisted BVP work.
9. Limitations and the route to supported and self-gravitating models.

## Submission Gates

1. Independent rerun of the exact artifact from a clean environment.
2. Specialist literature review for computer-assisted Skyrmion and soliton BVP
   validation; absence from a broad search is not a priority argument.
3. A proof appendix that states the Banach spaces, augmented inverse, Green-row
   Neumann identity, and every fixed-grid rounding operation explicitly.
4. Archive the generator inputs and a compact hash/provenance ledger for the
   rational spline and accepted certificate.
5. External review of the local-uniqueness claim and boundary-model scope.
