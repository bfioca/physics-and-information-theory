# Publishing Checklist

Working title:

```text
Screen Shadows Do Not Determine Finite Observer Algebras:
Static-Patch Regulator Benchmarks and a Continuum-Lift Obstruction
```

North star:

```text
A finite regulator theorem package showing that screen-visible diagnostics do
not determine observer algebras, plus a continuum-lift obstruction framework
using approximate cutoff embeddings.
```

This checklist tracks the path from repo artifact to publishable finite
benchmark paper. It should stay conservative: no continuum de Sitter, dS/CFT,
or ER=EPR theorem is claimed.

## How to Track This

- Keep task IDs stable. Add new tasks under the closest existing phase instead
  of starting a new research phase.
- Mark a task done only when the evidence artifact exists in the repo, or when
  the listed command passes from a clean checkout.
- Use `(partial)` in the task text when the artifact exists but still needs
  paper-grade tightening.
- Current top-priority open item: `E1-5`, which requires external expert
  feedback before it can be completed.

## Current Status

| Area | Status | Evidence |
| --- | --- | --- |
| Paper-shaped note | Done | `paper/main.md` |
| Expert feedback note | Done | `paper/expert_feedback_note.md` |
| Theorem/claim index | Done | `THEOREMS.md` |
| Five-certificate package | Done | `examples/reproduce_static_patch_package.py` |
| CI package regression | Done | `.github/workflows/ci.yml` |
| Release tag and frozen artifacts | Done | `artifacts/static_patch_diagnostics/` and `v0.1-static-patch-diagnostics` |

## Phase 1: Paper Extraction

- [x] P1-1 Create a paper-facing note from the static-patch package.
- [x] P1-2 Center the paper on one claim: finite screen-shadow diagnostics do not
  determine observer algebras.
- [x] P1-3 Keep Goals 1-23 out of the main paper narrative.
- [x] P1-4 Keep Goals 24-31, finite-to-Type-II, inclusion covariance, UCP
  embeddings, and continuum-lift obstruction as the source of truth.
- [x] P1-5 Decide whether to keep Markdown only or add `paper/main.tex`.
  Decision: keep Markdown for this release and make `paper/main.md` the
  canonical paper draft.
- [x] P1-6 Add a short introduction that reads like a paper introduction rather
  than a repo summary.
  Evidence: `paper/main.md`.

## Phase 2: Theorem Rewrite

- [x] P2-1 State screen-shadow collision as a theorem.
- [x] P2-2 State intrinsic response separation using the commutator witness.
- [x] P2-3 State the strong-continuity gate with proof.
- [x] P2-4 State the Type-II scaffold and exact-inclusion obstruction.
- [x] P2-5 State the consecutive-cutoff UCP refinement proposition.
- [x] P2-6 Include human proof sketches independent of code.
- [x] P2-7 Tighten the formal screen-shadow functor notation, e.g. `Sh_N`.
  Evidence: `paper/main.md` defines `Scr_N` and `Sh_N`.
- [x] P2-8 Tighten the formal response functor notation, e.g. `Resp_N`.
  Evidence: `paper/main.md` defines `Resp_N` and named response
  subdiagnostics.
- [x] P2-9 Separate fully proved finite statements from bounded-certificate
  extensions in theorem labels.
  Evidence: `paper/main.md` and `THEOREMS.md`.
- [x] P2-10 Add a "what the tests prove / do not prove" subsection.
  Evidence: `paper/main.md` Appendix A and `REPRODUCIBILITY.md`.

## Phase 3: Continuum-Lift Theorem

- [x] P3-1 State explicit lift conditions:
  embedding/coarse-graining, trace/state convergence, screen-shadow
  convergence, strong-continuity control, response persistence, and
  observer-algebra limit compatibility.
- [x] P3-2 State the screen-only dictionary obstruction theorem schema.
- [x] P3-3 Keep the claim boundary explicit: conditional schema, not continuum
  dS.
- [x] P3-4 Decide whether to promote the theorem schema into the main theorem
  list.
  Decision: promoted as `Theorem 6: Conditional Continuum Lift Obstruction`.
- [x] P3-5 Add a diagram or commutative-square-style schematic for the lift
  assumptions.
  Evidence: `paper/main.md` includes an ASCII lift-obstruction schematic.
- [x] P3-6 Add an example paragraph explaining what would instantiate the lift
  conditions in a real static-patch construction.
  Evidence: `paper/main.md`.

## Phase 4: Related Work

- [x] P4-1 Cite/position OA-QEC:
  Beny-Kempf-Kribs, Almheiri-Dong-Harlow, Harlow RT-from-QEC.
- [x] P4-2 Cite/position algebraic ER=EPR:
  Engelhardt-Liu.
- [x] P4-3 Cite/position de Sitter static-patch Type-II motivation:
  Chandrasekaran-Longo-Penington-Witten.
- [x] P4-4 Cite/position fuzzy-sphere/Berezin convergence:
  Rieffel.
- [x] P4-5 Add HaPPY/holographic tensor-network context.
  Evidence: `paper/main.md` related-work section.
- [x] P4-6 Add one sentence for why this is a finite benchmark, not competing
  with those frameworks.
  Evidence: `paper/main.md`.
- [x] P4-7 Check citation formatting consistently if converting to TeX.
  Decision: not applicable for this release because `paper/main.md` remains the
  canonical Markdown draft.

## Phase 5: Repo Release

- [x] R1-1 CI runs the static-patch package tests.
- [x] R1-2 CI validates package JSON indexes.
- [x] R1-3 CI runs the compact reproduction script.
- [x] R1-4 README points to the paper and expert notes.
- [x] R1-5 Create `REPRODUCIBILITY.md` with one clean command and expected
  output.
  Evidence: `REPRODUCIBILITY.md`.
- [x] R1-6 Freeze paper-used certificate JSON outputs under `artifacts/`.
  Evidence: `artifacts/static_patch_diagnostics/`.
- [x] R1-7 Record exact environment info:
  Python version, OS, commit hash, and deterministic parameters.
  Evidence: `artifacts/static_patch_diagnostics/environment.json` and
  `REPRODUCIBILITY.md`.
- [x] R1-8 Add or update a "what tests prove / do not prove" release note.
  Evidence: `REPRODUCIBILITY.md`.
- [x] R1-9 Tag a release:
  `v0.1-static-patch-diagnostics`.
- [x] R1-10 Push the release tag.

## Phase 6: Expert Feedback

- [x] E1-1 Create a two-page expert-facing feedback note.
- [x] E1-2 Make the expert question about cutoff embedding/coarse-graining, not
  about whether this proves de Sitter ER=EPR.
- [x] E1-3 Prepare a short email cover note.
  Evidence: `paper/expert_cover_note.md`.
- [x] E1-4 Decide whether to send only the two-page note first, with repo link
  as optional follow-up.
  Decision: send the two-page note and cover note first; offer the repo as
  optional follow-up.
- [ ] E1-5 Incorporate expert feedback into either the paper or a new issue
  list. This requires external feedback and remains intentionally open.

## Reviewer-Risk Burn-Down

- [x] D1-1 Risk: "Diagonal probes obviously miss off-diagonals."
  Action: sharpen the finite benchmark framing and emphasize the continuity and
  lift-obstruction additions.
- [x] D1-2 Risk: "Factorial inclusions are engineered."
  Action: lead with the consecutive-cutoff UCP refinement and `1/N_L`
  multiplicativity error.
- [x] D1-3 Risk: "Tests only assert certificate booleans."
  Action: point to analytic proofs in the paper and add direct witness tests
  where useful.
- [x] D1-4 Risk: "Screen-visible data are not canonical."
  Action: define the finite screen-shadow class explicitly and call it a
  benchmark class.
- [x] D1-5 Risk: "Continuum relevance is speculative."
  Action: keep the lift theorem conditional and ask the embedding question
  explicitly.

## Definition of Publishable Draft

- [x] DONE-1 Paper note has theorem statements, proof sketches, related work,
  limitations, and reproducibility appendix.
- [x] DONE-2 `THEOREMS.md` maps paper theorem numbers to certificate commands.
- [x] DONE-3 `REPRODUCIBILITY.md` gives one-command reproduction plus expected
  output.
- [x] DONE-4 Frozen artifacts match the current release package.
- [x] DONE-5 CI passes on GitHub.
- [x] DONE-6 Release tag exists.
- [x] DONE-7 Expert feedback note is ready to send.

## Tracking Commands

Use these commands for quick local audits:

```bash
rg -n "P[1-4]-|R1-|E1-|D1-|DONE-" paper/PUBLISHING_CHECKLIST.md
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics tests.test_embedding_channels tests.test_continuum_lift_obstruction
```
