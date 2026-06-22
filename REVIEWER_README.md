# Reviewer Entry Point: Final-Support Thermal Dephasing

**Status:** strengthened short-paper candidate. The internal theorem and
reproducibility gates pass; independent proof review and two-domain novelty
review remain open. No submission decision has been issued.

This branch contains a larger research archive, but the requested review is
about one paper only. The paper solves a sharp thermal covariance optimization
for fixed final Cauchy support and then proves that its half-line momentum
optimizer is the full angular and canonical optimum for a conformal scalar in
a de Sitter static patch.

## Five-Minute Route

1. Read the [manuscript](paper/local_scalar_observer_cost/main.pdf), especially
   the general thermal theorem, the de Sitter specialization, and the causal
   source-cylinder corollary.
2. Use the [shared referee guide](paper/local_scalar_observer_cost/REFEREE_GUIDE.md)
   for the exact claim boundary and requested disposition.
3. Choose the domain-specific brief:
   [detector/QFT](paper/local_scalar_observer_cost/QFT_NOVELTY_REVIEW.md) or
   [operator theory](paper/local_scalar_observer_cost/OPERATOR_NOVELTY_REVIEW.md).
4. Consult the [internal proof audit](docs/local_scalar_observer_proof_audit.md)
   for the five vulnerable proof steps.
5. Record the result in the [specialist response form](paper/local_scalar_observer_cost/REVIEW_RESPONSE_FORM.md).

Older papers, stopped programs, and planning notes elsewhere in the repository
are not part of this review packet.

## Candidate Contribution

For Dirichlet half-line momentum data supported in `[0,L]`, inverse temperature
`beta`, dephasing exponent `Gamma`, and field energy `E=||p||^2/2`, the paper
proves

```text
Gamma <= E C_beta(L),
C_beta(L)=2 L Lambda(pi L/beta),
```

where `Lambda(tau)` is the simple top eigenvalue of the positive reflected KMS
kernel

```text
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

The paper gives global two-sided bounds and uniform small- and large-support
remainders. At the de Sitter temperature `beta=2 pi R`, it proves that this
s-wave momentum profile is the unique optimizer over every angular and
canonical sector.

The exact detector channel is prior art. Positive-kernel variational
principles are prior art. The candidate novelty is the reflected thermal
operator selected by final support, its exact general-temperature coefficient,
the full de Sitter sector reduction, and the sharp support asymptotics.

## Claim Boundary

Sharpness is for final Cauchy support. A fixed source radius and duration give
a causal envelope for that support; near-controllability from every smaller
fixed source cylinder is not claimed. The energy is post-switch scalar-field
energy only. It excludes actuator work, clock or battery energy, and probe
stress. The gravity appendix contains final-slice constraint data, not a
channel on perturbed geometry or a coupled evolution.

## Requested Decision

- **SUBMIT:** the central conjunction is not subsumed by known work and the
  proof survives independent review.
- **STRENGTHEN:** identify one concrete minimum theorem or correction required
  before submission.
- **NO-GO:** provide the theorem, reference, or argument that makes the result
  known, immediate, or insufficient for a standalone paper.

## Reproduce the Packet

From the repository root:

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
PYTHONPATH=. python -m pytest -q \
  tests/test_local_scalar_observer_cost.py \
  tests/test_local_scalar_observer_manuscript.py \
  tests/test_local_scalar_observer_spectrum.py
python paper/local_scalar_observer_cost/audit_package.py
```

The numerical replay requires NumPy through the optional `research-numerics`
dependency. These checks establish internal closure and provenance, not
literature novelty.

This is a request for critical review, not endorsement or approval.

The author-facing [external review launch kit](paper/local_scalar_observer_cost/EXTERNAL_REVIEW_LAUNCH.md)
contains minimal attachment sets and separate detector/QFT, operator-theory,
and Harlow framing drafts.
