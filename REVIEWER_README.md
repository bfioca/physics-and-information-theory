# Reviewer Entry Point: Final-Support Thermal Dephasing

**Status:** strengthened short-paper candidate. Internal theorem,
reproducibility, numerical, and package gates pass. Independent proof coverage
and two-domain novelty review remain open. No submission decision has been
issued.

This repository is organized around one manuscript. The paper solves a sharp
thermal covariance optimization for fixed final Cauchy support and then proves
that its half-line momentum optimizer is the full angular and canonical
optimum for a conformal scalar in a de Sitter static patch.

## Five-Minute Route

1. Read the [manuscript](paper/local_scalar_observer_cost/main.pdf), especially
   the general thermal theorem, the de Sitter specialization, and the causal
   source-cylinder corollary.
2. Use the [shared referee guide](paper/local_scalar_observer_cost/REFEREE_GUIDE.md)
   for the exact claim boundary and requested disposition.
3. Choose the domain brief:
   [detector/QFT](paper/local_scalar_observer_cost/QFT_NOVELTY_REVIEW.md) or
   [operator theory](paper/local_scalar_observer_cost/OPERATOR_NOVELTY_REVIEW.md).
4. Consult the [proof audit](docs/local_scalar_observer_proof_audit.md) for the
   vulnerable derivations and the [priority audit](paper/local_scalar_observer_cost/PRIORITY_AUDIT.md)
   for exact prior-art reductions.
5. Record findings in the [response form](paper/local_scalar_observer_cost/REVIEW_RESPONSE_FORM.md).

## Candidate Contribution

For Dirichlet half-line momentum data supported in `[0,L]`, inverse temperature
`beta`, dephasing exponent `Gamma`, and field energy `E=||p||^2/2`, the paper
proves

```text
Gamma <= E C_beta(L),
C_beta(L)=2 L Lambda(pi L/beta),
```

where `Lambda(tau)` is the simple top eigenvalue of

```text
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

The paper gives global bounds and uniform small- and large-support remainders.
At `beta=2 pi R`, it proves that the s-wave momentum profile is the unique
optimizer over every angular and canonical sector.

The exact detector channel and positive-kernel variational principles are
prior art. The candidate novelty is the reflected thermal operator selected by
final support, its explicit uniform remainders, and its full de Sitter sector
reduction.

## Claim Boundary

Sharpness is for final Cauchy support. A fixed source radius and duration give
a causal envelope; near-controllability from every smaller source cylinder is
not claimed. The energy is post-switch scalar-field energy only. It excludes
actuator work, clock or battery energy, and probe stress. The gravity appendix
contains final-slice constraint data, not a channel on perturbed geometry or a
coupled evolution.

## Requested Decision

- **SUBMIT:** both novelty gates pass, the proof survives external review, and
  every central claim has at least one external `PASS` or `CORRECT` finding.
- **STRENGTHEN:** identify one concrete minimum theorem or correction required
  before submission.
- **NO-GO:** provide the theorem, reference, or argument that makes the result
  known, immediate, incorrect, or insufficient for a standalone paper.

A blank row or `NOT REVIEWED` is not a proof pass. Reviewers may divide the
claim-level checks according to expertise; uncovered claims require a targeted
external proof check.

## Reproduce the Packet

```bash
python -m pip install -e '.[research-numerics]'
PYTHONPATH=. python -m pytest -q
python paper/local_scalar_observer_cost/audit_package.py
```

Expected result: `47 passed` and a passing 25-file package audit. These checks
establish internal closure and provenance, not literature novelty.

This is a request for critical review, not endorsement or approval. The
[external review launch kit](paper/local_scalar_observer_cost/EXTERNAL_REVIEW_LAUNCH.md)
contains deterministic attachment bundles and concise outreach drafts.
