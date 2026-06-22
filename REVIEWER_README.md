# Reviewer Entry Point: Local Scalar Observer Cost

**Status:** narrow-paper candidate for specialist novelty review. The analytic
theorem, manuscript build, numerical illustration, and reproducibility checks
pass. Whether the result merits a standalone paper remains deliberately open.

This branch contains a larger research archive, but the requested review is
about one candidate paper only: a sharp localization-energy optimization for a
prescribed gapless qubit coupled to a conformally coupled massless scalar field
in a four-dimensional de Sitter static patch.

## Five-Minute Review Route

1. Read the [16-page manuscript](paper/local_scalar_observer_cost/main.pdf),
   especially Theorem 3.3, Figure 1, and Corollary 3.4.
2. Use the [referee guide](paper/local_scalar_observer_cost/REFEREE_GUIDE.md)
   for the exact paper-or-no-go questions and requested disposition.
3. Consult the
   [primary-source novelty matrix](docs/primary_source_novelty_matrix.md) only
   if the relation to known detector, localization, and entropy results needs
   checking.
4. Run the package audit below if artifact integrity matters for the review.

The older papers, stopped programs, and planning notes elsewhere in the
repository are not part of this review packet.

## Candidate Contribution

The exact Weyl displacement channel for a prescribed gapless detector is known
and is not claimed as new. The candidate contribution begins after that step.
For fixed causal support and post-switch Killing energy, the paper eliminates
the compact source and proves an exact all-angular optimization governed by the
top eigenvalue of an explicit positive KMS kernel. It identifies the unique
extremizing sector as s-wave momentum, proves the small- and large-support
asymptotics, and gives smooth compact-source approximants. The numerical curve
in Figure 1 illustrates the exact kernel but is not used as a rigorous bound.

An exact flux-free Einstein-scalar final-slice construction is included only as
a gravity corollary. The source history and pointer channel are not derived on
the perturbed geometry. Thus the manuscript does not claim a coupled
Einstein-matter evolution, an autonomous detector, a universal measurement
cost, observer complementarity, or ER=EPR.

## Requested Decision

Please return one of three dispositions:

- **NARROW PAPER GO:** the compact-support optimization is not subsumed by
  known work and is independently useful in its present scope.
- **STRENGTHEN:** the result becomes viable after a specific minimum addition;
  please identify that addition.
- **NO-GO:** the result is already known, immediate from a standard theorem, or
  too limited for a standalone paper; a source or concise argument would be
  especially useful.

The main issue is novelty and significance, not whether the computational
artifact runs. The detailed five-question checklist is in the referee guide.

## Verify the Packet

From the repository root, the fast integrity check is:

```bash
python paper/local_scalar_observer_cost/audit_package.py
```

For a source-to-artifact replay and the focused test suite:

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
PYTHONPATH=. python -m pytest -q \
  tests/test_local_scalar_observer_cost.py \
  tests/test_local_scalar_observer_manuscript.py \
  tests/test_local_scalar_observer_spectrum.py
```

The numerical replay requires NumPy, available through the optional
`research-numerics` dependency. Exact build and package details are in the
[paper README](paper/local_scalar_observer_cost/README.md).

## Packet Contents

| Item | Purpose |
| --- | --- |
| [Manuscript PDF](paper/local_scalar_observer_cost/main.pdf) | Primary review object |
| [Referee guide](paper/local_scalar_observer_cost/REFEREE_GUIDE.md) | Claim, questions, and dispositions |
| [Paper README](paper/local_scalar_observer_cost/README.md) | Build and reproduction instructions |
| [Analytic audit](docs/local_scalar_observer_cost.md) | Derivation, assumptions, and claim boundary |
| [Frozen goal](docs/local_scalar_observer_cost_goal.md) | Original paper-or-no-go contract |
| [Artifact manifest](paper/local_scalar_observer_cost/artifact_manifest.json) | Frozen hashes and build metadata |

This is a request for critical feedback, not endorsement or approval.
