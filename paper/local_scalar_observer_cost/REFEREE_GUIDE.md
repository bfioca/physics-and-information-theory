# Referee Guide

Status: strengthened specialist-review candidate; submission remains
conditional on proof and novelty review

## Exact Candidate Claim

For Dirichlet half-line momentum data supported in `[0,L]`,

```text
C_beta(L)=sup Gamma/E=2 L Lambda(pi L/beta),
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

The top eigenvalue is simple, its optimizer is positive, and the paper proves
global bounds and uniform small- and large-support remainders. For the
conformal massless scalar in de Sitter, `beta=2 pi R`; angular resolvent order
and a coordinate-sector estimate make this same s-wave momentum profile the
unique full-phase-space optimizer.

The exact detector channel and the general positive-kernel variational
principle are not claimed as new.

## Read First

1. `main.pdf`: the general thermal theorem, de Sitter all-sector theorem, and
   causal source-cylinder corollary.
2. `sections/localization_theorem.tex`: complete analytic proof.
3. `sections/achievability.tex`: smooth final-data and source closure.
4. `../../docs/local_scalar_observer_proof_audit.md`: five-step internal audit.
5. The domain-specific novelty brief matching your expertise.

## Decisive Questions

1. Is the reflected KMS-kernel optimization a named theorem or immediate
   corollary in detector theory, localized negative-Sobolev estimates,
   Riesz-potential theory, or related concentration problems?
2. Are the arbitrary-temperature coefficient, de Sitter full-sector
   reduction, and support asymptotics enough for a standalone short paper?
3. Is every use of "sharp" correctly restricted to final Cauchy support?
4. Are the angular ordering, coordinate domination, strict uniqueness,
   remainder bounds, and smooth-source closure correct?
5. Does the gravity appendix distract from the theorem, or is its present
   explicitly secondary placement acceptable?

## Requested Disposition

- **SUBMIT:** novel enough in this scope and analytically sound.
- **STRENGTHEN:** viable after one identified minimum addition or correction.
- **NO-GO:** known, immediate, or too routine; please give the closest source
  or concise argument.

## Verification

From the repository root:

```bash
python paper/local_scalar_observer_cost/audit_package.py
PYTHONPATH=. python -m pytest -q \
  tests/test_local_scalar_observer_cost.py \
  tests/test_local_scalar_observer_manuscript.py \
  tests/test_local_scalar_observer_spectrum.py
```

The audit verifies the checked artifact and its provenance. It does not
certify the proof or novelty.

## Not Claimed

The paper does not claim a new exact detector channel, fixed-cylinder
controllability, total measurement cost, an autonomous switching device, a
channel on perturbed geometry, or coupled gravitational evolution.
