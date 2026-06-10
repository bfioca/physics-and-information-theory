# Exact rational response trials

Status: reproducible exact primal-adjoint trial archive with a rigorous
compact-angle, exactly subdivided positive-radius primal residual probe. No
continuum response interval or zero exclusion is claimed.

## Construction

`qgtoy.centrifugal_skyrmion_rational_response_trials` repeats the floating
`81`-node centrifugal primal and master-adjoint solves used by the feasibility
audit. For each field it forms a cubic-Hermite interpolant from the nodal
values and centered nodal slopes. It samples that interpolant at the 44 shared
endpoints of the authenticated 43-cell sharp profile and rounds every shared
value and physical derivative once to denominator `10^12`.

Each positive-radius cell is then an exact rational cubic in its normalized
coordinate. The resulting primal and adjoint trials have exact `C1` joins and
the exact essential trace `g(4)=0`.

The center is not extrapolated with singular physical variables. At
`x_c=1/16`, the archived endpoint jet is converted exactly to linear
polynomials `u(t),v(t)`, `t=x^2`, satisfying

```text
g=x v(t),
f=x[-v(t)+t u(t)].
```

These regular-origin polynomials reproduce both field values and physical
derivatives at `x_c` exactly. They are ready for the separate cancellation-safe
origin residual theorem.

## Positive-radius probe

The audit passes the rational primal cells and authenticated profile boxes to
`validated_centrifugal_response_residual`. It uses a certified compact rational
bracket for pi, evaluates sine and cosine in the smaller of `F` and `pi-F`,
and outward-rounds the coefficient boxes. Each archived cubic is restricted
exactly to eight authenticated subcells, without interpolation or re-solving.
Eight Taylor terms then give:

```text
domain                                      [1/16, 4]
cells                                       344
positive-radius primal residual L2^2 upper  3.3197692493413107
largest residual-component absolute upper  1.8591081655835504
```

This number is a diagnostic, not an energy-dual residual. It excludes the
origin interval. The exact squared bounds at one,
two, four, and eight subdivisions are approximately `328.14`, `59.10`,
`13.41`, and `3.32`. The clean decrease proves that the former whole-cell
bound was dominated by dependency wrapping, but the observed first-order norm
convergence is not fast enough for zero exclusion. The next evaluator must
retain centered correlations rather than relying on brute subdivision.

The same audit now evaluates the exact wall endpoint blocks from the
authenticated wall-slope interval and the pure-tension Robin law. The primal
wall conormal mismatch lies inside approximately
`[-1.102e-3,1.421e-3]`, while the wall trace margin is above `0.2018`. Thus the
primal wall term is no longer an open construction. The adjoint wall equation
still needs the interval master-functional load `gamma_B`.

## Open gate

The archive closes trial fitting. A physical dual-weighted response interval
still requires:

1. the cancellation-safe origin primal and adjoint residuals;
2. an interval bulk and wall representation of the master functional, which
   supplies the adjoint load;
3. centered correlated coefficient/Taylor-model evaluation beyond interval
   subdivision;
4. composition with the global coercivity and exact dual-weighted theorem.

In particular, evaluating `A z` alone would not be an adjoint residual; the
missing master load must be included before any adjoint norm or zero-exclusion
claim is legitimate.

## Artifact

The full rational archive and residual probe are stored in
`experiments/centrifugal_skyrmion_rational_response_trials.json`. The audit
binds the trial generator, floating feasibility solver, residual theorem, and
both authenticated profile inputs by SHA256.

```text
PYTHONPATH=. python \
  experiments/centrifugal_skyrmion_rational_response_trials_audit.py
pytest -q \
  tests/test_centrifugal_skyrmion_rational_response_trials.py \
  tests/test_centrifugal_skyrmion_rational_response_trials_audit.py
ruff check \
  qgtoy/centrifugal_skyrmion_rational_response_trials.py \
  experiments/centrifugal_skyrmion_rational_response_trials_audit.py \
  tests/test_centrifugal_skyrmion_rational_response_trials.py \
  tests/test_centrifugal_skyrmion_rational_response_trials_audit.py
```
