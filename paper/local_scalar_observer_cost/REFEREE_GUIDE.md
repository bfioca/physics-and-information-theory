# Referee Guide

Status: specialist-review candidate; no standalone novelty claim has been
issued.

This packet asks for a paper-or-no-go judgment on one narrow result. The exact
gapless-detector channel is prior art. The proposed contribution is the sharp
elimination of the compact source in favor of post-switch field energy and
causal support.

## Candidate Result

For a degenerate pointer coupled to the conformally coupled massless scalar in
a four-dimensional de Sitter static patch, the manuscript proves

```text
log(1/(2 epsilon_obs)) <= E_K R C_opt(y) <= E_K R F(y),
y=atanh(a/R)+T/R,
C_opt(y)=2y Lambda(y/2),
F(y)=4 asinh(1)y/pi+8y^2/pi^3.
```

Here `Lambda(tau)` is the simple top eigenvalue of the exact positive compact
kernel

```text
k_tau(u,v)=pi^-1 log[sinh(tau(u+v))/sinh(tau|u-v|)].
```

The optimization includes every angular and canonical sector; the unique
extremizing sector is s-wave momentum. The thermal correction is cubic at
small support and `8/pi^3` is the sharp leading large-support coefficient.
Smooth compact sources whose spatial worldtube approaches the final support
ball approach the optimum. Exact controllability from every smaller fixed
source cylinder is not claimed. A flux-free spherical subclass supplies exact
Einstein-scalar final-slice constraints. The gravity comparison is local to
the ball containing the datum; it is not a dynamical-gravity channel theorem.

## Read First

1. `main.pdf`, especially Theorem 3.3, Figure 1, and Corollary 3.4.
2. `sections/achievability.tex` for scaling and smooth-source closure.
3. `sections/comparison.tex` for the prior-art boundary and Bekenstein-form
   separation.
4. `sections/gravity.tex` for the deliberately limited constraint corollary.
5. `../../docs/primary_source_novelty_matrix.md` for the equation-level audit.

## Decisive Questions

1. Is the exact KMS-kernel optimization already a standard named theorem or
   immediate published corollary in detector theory, local quantum physics,
   localized negative Sobolev estimates, or Riesz-potential spectral theory?
2. If technically new in this setting, are the full-sector reduction, unique
   optimal profile, and sharp support asymptotics enough physics for a
   standalone short paper?
3. Does the Bekenstein quadratic-form separation clarify the contribution, or
   does it distract from the detector theorem?
4. Should the local Einstein-scalar constraint result remain a corollary, move
   to an appendix, or be removed?
5. Is the prescribed gapless smeared-qubit coupling an acceptable operational
   model for this theorem, or must a standalone physics paper replace it with
   a local probe field or an explicit actuator?

## Requested Disposition

- **NARROW PAPER GO:** the theorem is not subsumed by known work and is
  independently useful; return proof or framing corrections.
- **STRENGTHEN:** the result is viable only after a specific addition, such as
  a general static-spacetime theorem, certified eigenvalue curve, or controlled
  actuator model; identify the minimum addition.
- **NO-GO:** provide the source or argument that subsumes it, or explain why
  the result is too elementary or physically empty for a standalone paper.

## Verification

The fast integrity check, run from the repository root, is:

```bash
python paper/local_scalar_observer_cost/audit_package.py
```

For a source-to-artifact replay and all focused tests:

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
PYTHONPATH=. python -m pytest -q \
  tests/test_local_scalar_observer_cost.py \
  tests/test_local_scalar_observer_manuscript.py \
  tests/test_local_scalar_observer_spectrum.py
```

The audit verifies the checked PDF and log, manuscript hashes and structure,
the frozen theorem certificate, and its source-hash ledger. It does not certify
novelty or replace review of the analytic proof.

## Not Claimed

The paper does not claim a new exact detector channel, an autonomous switching
device, a global weak-gravity solution relative to the unperturbed de Sitter
horizon, a channel derived on perturbed geometry, a universal measurement
cost, observer complementarity, or ER=EPR.
