# Paper R Viability Decision

Status: **INCONCLUSIVE STOP** under the predeclared bounded-sprint rule

## Decision

The Paper R sprint is complete, but the candidate should **not** be promoted
to a standalone paper in its present form. The correlation-preserving
calculation certifies a directed negative corrected estimator, but the full
dual-weighted response interval still contains zero.

The source-bound decision artifact is
`experiments/paper_r_response_certificate.json`.

| Quantity | Certified value |
| --- | --- |
| Corrected estimator | `[-0.003079554319910408, -0.002552931394151071]` |
| Complete primal dual norm | `< 0.785351351663998829` |
| Complete loaded-adjoint dual norm | `< 0.030892717992632714` |
| Residual-product error | `< 0.024261637832088839` |
| Full exterior amplitude | `[-0.027341192151999246, 0.021708706437937767]` |
| Decision ratio `rho` | `< 8.708392897914348130` |
| Frozen decision | **INCONCLUSIVE STOP** |

The corrected estimator itself excludes zero. The continuum response does
not: the certified residual product is roughly `9.50` times the maximum
allowed product for zero exclusion. This is a proof-resolution failure, not a
proof that the physical response vanishes.

## What Closed

- The regular-origin exterior-master adjoint load is included.
- The signed origin estimator includes the cutoff trace required by its
  strong-to-weak conversion.
- The outer signed estimator retains common radial correlations and is
  strictly negative.
- Weak and strong wall representations are no longer mixed.
- The adjoint completed-square certificate is tight enough for the sprint.
- The exact annular Weyl factor is `25/2`.
- The two spin-2 states have exact equal Casimir and leading rotor energy,
  with `QJ` norms `sqrt(6)` and zero.

These are reusable technical results. They do not imply Theorem R1 or R2,
because the supplied exterior-amplitude interval contains zero.

## Bottleneck

The primal certificate is decisive. Holding the certified adjoint bound and
estimator fixed, zero exclusion would require

```text
delta_y < 0.082638613888227453,
```

versus the present `delta_y<0.785351351663998829`. The dominant certified
primal cell is `x in [1/2,11/16]`. The local-matrix construction already
shows that the global `1/100` coercivity floor is not the main problem.

A future attempt would need a materially better conforming primal trial or a
direct certified Riesz solve, reducing the norm by about `9.50` and the
squared bound by about ninety. More subdivision of the same representation
is not justified by the current evidence.

## Paper Consequence

The manuscript outline remains a technical architecture, not a draft for
submission. In particular:

- no nonzero exterior-Weyl lower bound is certified;
- the equal-leading-energy state discriminator remains conditional;
- no abstract should claim a response theorem; and
- the result should be described to a colleague as a rigorous viability test
  that identified the precise primal-approximation obstacle.

This does not close the broader observer program. It closes this one bounded
Paper R route under its frozen model, trial family, and one-redesign rule.

## Reproduce

```bash
PYTHONPATH=. python experiments/paper_r_response_certificate_audit.py
PYTHONPATH=. python -m pytest -q \
  tests/test_paper_r_response_certificate.py \
  tests/test_paper_r_response_certificate_audit.py \
  tests/test_paper_r_state_transfer.py \
  tests/test_paper_r_wall_composition.py \
  tests/test_paper_r_weyl_observable.py
```

Claim boundary: this is a leading `O(Omega^2)`, fixed-de-Sitter,
ideal-Nambu-Goto-wall viability decision. It proves no finite-rotation,
self-gravitating, detector-level, or tensorial Israel-matching statement.
