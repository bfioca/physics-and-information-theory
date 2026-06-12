# Paper Package

This directory is the paper-shaped entrypoint. It is intentionally narrower
than the full repository.

## Selected Manuscript

The active near-term track is `validated_skyrmion_profile/`: a
computer-assisted existence and local-uniqueness theorem for one prescribed
massive Dirichlet-confined fixed-background Skyrmion profile, with an analytic
local parameter branch and authenticated radial and spectral consequences. Its
proof, exact-replay, package-audit, and internal referee gates pass; it is ready
for colleague review and specialist submission preparation. Start with:

- `validated_skyrmion_profile/main.tex`
- `validated_skyrmion_profile/README.md`
- `validated_skyrmion_profile_outline.md`
- `../docs/publishable_paper_route_decision.md`

Paper U remains the higher-impact long-term program, but it is not currently a
submission theorem.

## Stopped Bounded Candidate

The Track 2 spacelike-replication work is isolated in
`spacelike_replication/`. Its theorem is proved on a bounded finite-code
domain, but the source-level reduction audit found that the main inequality is
a direct consequence of Janssens' established UCP covariance Cauchy-Schwarz
lemma. It is retained as an internal methods note, not a submission candidate.
Start with:

- `spacelike_replication/main.tex`
- `spacelike_replication/README.md`
- `spacelike_replication_paper_outline.md`

The files below are the canonical sources for the earlier finite
observer-algebra package, not for Track 2.

Start with:

- `main.md`
- `main.tex`
- `expert_feedback_note.md`
- `expert_cover_note.md`
- `PUBLISHING_CHECKLIST.md`

Use `PUBLISHING_CHECKLIST.md` as the live tracker for turning the current note
into a publishable draft and release package.

`main.md` is the canonical editable paper draft. `main.tex` is the
attachment-ready technical-note version for wider expert sharing. The
finite-observer note is retained as the earlier extraction artifact.

## Expert Send Bundle

Send only:

- `expert_cover_note.md`
- `expert_feedback_note.md`

Do not lead with the full repository or goal history. In the cover note, say
that `main.tex`, `main.md`, and the executable certificate repository are
available as supporting material.

Supporting repo entrypoints:

- `THEOREMS.md`
- `docs/static_patch_observer_algebra/README.md`
- `docs/static_patch_observer_algebra/audit_index.json`

The target framing is an arXiv-style technical note with reproducible code
appendix, not a claim of a new continuum quantum-gravity theorem.
