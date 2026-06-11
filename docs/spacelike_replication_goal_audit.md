# Spacelike SO(3) Replication: Goal Audit

Audit date: 2026-06-11 UTC

Disposition: **TECHNICAL GOAL COMPLETE; STANDALONE NOVELTY STOP.** The broad
claim that locality forces leakage for every finite localized non-Abelian
reference is false as stated and has been retired. The surviving result is a
bounded theorem for reproducing three components of one rigid finite `SO(3)`
collective mode in pairwise commuting cells. Its proof and finite-model checks
are complete on the declared domain. The source-level priority audit found
that Janssens' CP-map covariance Cauchy-Schwarz lemma implies the
state-weighted theorem directly, so the proposed bounded paper is stopped.

## Requirement Audit

| Requirement | Evidence | Status |
| --- | --- | --- |
| Isolate the work on branches | Technical theorem: `codex/locality-reference-leakage-theorem`; priority audit: `codex/spacelike-replication-manuscript`. | **PASS** |
| State a model-independent bounded setting | Section 1 of `spacelike_replication_leakage_theorem.md` quantifies over a finite code and three commuting bounded algebras; local-net microcausality is a corollary. | **PASS** |
| Prove exact and approximate compression bounds | Sections 2 and 3 give the directed identity, explicit error budgets, and the robust three-cell theorem. | **PASS** |
| Derive a state-weighted three-cell result | Equations (3.5)-(3.7) bound the total state-weighted off-code quadratic weight and test consistency of a claimed amplitude cap. | **PASS** |
| Connect the result to orientation risk | Section 4 composes the theorem with Research Theorem W3 and records the non-vacuity conditions. | **PASS INTERNALLY** |
| Supply a distributed realization | Section 5 proves pairwise asymptotic sharpness and constant-factor three-cell scaling for disjoint ferromagnetic blocks. It explicitly does not claim uniformly bounded support diameter or a uniform spectral gap. | **PASS** |
| Check the model independently | `tests/test_locality_reference_leakage.py` compares the formulas with ambient Dicke-basis matrices, including a positive buffer and a six-site three-cell model. | **PASS** |
| Audit novelty against primary literature | `spacelike_replication_novelty_audit.md` and `spacelike_replication_qec_reduction_audit.md` give the exact reduction to Janssens' established joint-measurement noise inequality. | **NOVELTY STOP** |
| Produce a technical theorem note | `spacelike_replication_leakage_theorem.md` contains the complete bounded proof, assumptions, model derivations, and nonclaims. | **PASS** |
| Produce a bounded paper plan | `../paper/spacelike_replication_paper_outline.md` is frozen as a methods-note outline after the priority kill gate. | **STOPPED** |
| Keep excluded programs outside the claim | KMS QFT, gravity, the Skyrmion, and Paper U do not enter any premise or certified conclusion. | **PASS** |

## Publication Disposition

Do not submit the bounded theorem as a new paper. With `T(X)=W*XW`, its
off-code quadratic forms are the standard added-noise operators of a UCP
compression. Janssens' CP covariance Cauchy-Schwarz lemma gives the pairwise
state-weighted inequality; the proposed main theorem is the cyclic `SO(3)`
sum. Retain the branch as a tested methods lemma for the broader observer
program and cite the prior result whenever it is used.

## Claim Boundary

This is a truncation theorem for **spacelike replication of a rigid collective
mode**. It is not a no-go for local non-Abelian currents: several noncommuting
components may inhabit one region. The state-weighted quantities are squared
off-code amplitudes, not transition probabilities or lifetimes without a
normalized operation and dynamics. At fixed microscopic norm, the response
gain can weaken with spin, so the theorem does not establish that more accurate
references must decohere faster.

## Verification Record

The focused verification commands are:

```bash
PYTHONPATH=. python -m pytest -q \
  tests/test_locality_reference_leakage.py \
  tests/test_global_so3_reference_risk.py \
  tests/test_spacelike_replication_manuscript.py
PYTHONPATH=. python -m qgtoy locality-reference-leakage
python -m compileall -q qgtoy \
  tests/test_locality_reference_leakage.py \
  tests/test_global_so3_reference_risk.py \
  tests/test_spacelike_replication_manuscript.py
git diff --check
```

The focused suite checks the algebraic identities, robust constants, risk
composition, parameter-consistency diagnostics, and both ferromagnetic model
families. The CLI certificate must return `"status": "pass"` with every
certified claim true. On the audit date, the focused suite reported **41
passed**, the CLI certificate returned pass, `compileall` succeeded, and
`git diff --check` reported no errors.

The repository-wide suite is not clean independently of this branch. The
exact-spline and outer-tube Skyrmion Liouville audits both pin SHA-256
`3882308331da...` for `validated_centrifugal_liouville_taylor.py`, whose current
unmodified hash is `65e6b2f853bc...`. Neither the source nor those certificates
is changed here, and the Skyrmion program is outside this goal.
