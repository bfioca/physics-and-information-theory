# Spacelike SO(3) Replication: Goal Audit

Audit date: 2026-06-11 UTC

Disposition: **TECHNICAL GOAL COMPLETE; PUBLICATION DECISION OPEN.** The broad
claim that locality forces leakage for every finite localized non-Abelian
reference is false as stated and has been retired. The surviving result is a
bounded theorem for reproducing three components of one rigid finite `SO(3)`
collective mode in pairwise commuting cells. Its proof and finite-model checks
are complete on the declared domain. Publication still depends on a
source-level priority review and a self-contained presentation of the imported
orientation-risk lemma.

## Requirement Audit

| Requirement | Evidence | Status |
| --- | --- | --- |
| Isolate the work on a branch | `codex/locality-reference-leakage-theorem` | **PASS** |
| State a model-independent bounded setting | Section 1 of `spacelike_replication_leakage_theorem.md` quantifies over a finite code and three commuting bounded algebras; local-net microcausality is a corollary. | **PASS** |
| Prove exact and approximate compression bounds | Sections 2 and 3 give the directed identity, explicit error budgets, and the robust three-cell theorem. | **PASS** |
| Derive a state-weighted three-cell result | Equations (3.5)-(3.7) bound the total state-weighted off-code quadratic weight and test consistency of a claimed amplitude cap. | **PASS** |
| Connect the result to orientation risk | Section 4 composes the theorem with Research Theorem W3 and records the non-vacuity conditions. | **PASS INTERNALLY** |
| Supply a distributed realization | Section 5 proves pairwise asymptotic sharpness and constant-factor three-cell scaling for disjoint ferromagnetic blocks. It explicitly does not claim uniformly bounded support diameter or a uniform spectral gap. | **PASS** |
| Check the model independently | `tests/test_locality_reference_leakage.py` compares the formulas with ambient Dicke-basis matrices, including a positive buffer and a six-site three-cell model. | **PASS** |
| Audit novelty against primary literature | `spacelike_replication_novelty_audit.md` kills the generic compression headline and identifies the closest covariant-QEC and reference-frame results. | **PASS; PRIORITY UNCONFIRMED** |
| Produce a technical theorem note | `spacelike_replication_leakage_theorem.md` contains the complete bounded proof, assumptions, model derivations, and nonclaims. | **PASS** |
| Produce a bounded paper plan | `../paper/spacelike_replication_paper_outline.md` leads with the state-weighted theorem and separates completed work from submission gates. | **PASS; CONDITIONAL** |
| Keep excluded programs outside the claim | KMS QFT, gravity, the Skyrmion, and Paper U do not enter any premise or certified conclusion. | **PASS** |

## Publication Gates

The branch is ready for expert critique, but not yet for submission. Three
items remain:

1. Integrate the full W3 global-risk proof into a manuscript appendix, or cite
   a published theorem with the identical task, cost, and constant.
2. Obtain an AQFT/covariant-QEC specialist review of both the proof and the
   priority claim.
3. Complete a symbol-level comparison with approximate cleaning and
   covariant-code bounds. If the state-weighted result is an immediate
   corollary, retain this branch as a methods note rather than a theorem paper.

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
PYTHONPATH=. python -m pytest -q tests/test_locality_reference_leakage.py tests/test_global_so3_reference_risk.py
PYTHONPATH=. python -m qgtoy locality-reference-leakage
python -m compileall -q qgtoy tests/test_locality_reference_leakage.py
git diff --check
```

The focused suite checks the algebraic identities, robust constants, risk
composition, parameter-consistency diagnostics, and both ferromagnetic model
families. The CLI certificate must return `"status": "pass"` with every
certified claim true. On the audit date, the focused suite reported **39
passed**, the CLI certificate returned pass, `compileall` succeeded, and
`git diff --check` reported no errors.

The repository-wide suite is not clean independently of this branch. The
exact-spline and outer-tube Skyrmion Liouville audits both pin SHA-256
`3882308331da...` for `validated_centrifugal_liouville_taylor.py`, whose current
unmodified hash is `65e6b2f853bc...`. Neither the source nor those certificates
is changed here, and the Skyrmion program is outside this goal.
