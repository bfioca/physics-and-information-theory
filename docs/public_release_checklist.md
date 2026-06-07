# Public Release Checklist

This repository is intended to be publishable as finite research-code support
and as a focused arXiv-style benchmark note, not as a continuum-gravity claim.

## Completed Before Public Release

- Added an MIT license.
- Added citation metadata.
- Added a public claim boundary to the README.
- Added a top-level theorem/claim index: `THEOREMS.md`.
- Added a paper-shaped technical note: `paper/main.md`.
- Added a compact reproduction script:
  `examples/reproduce_static_patch_package.py`.
- Added approximate consecutive-cutoff embedding and continuum-lift obstruction
  notes, with focused tests and certificate indexes.
- Added a focused GitHub Actions workflow for the packaged static-patch result.
- Removed private audience labels from the public-facing docs.
- Checked tracked files for common secret patterns:
  API keys, tokens, passwords, private keys, database URLs, and cloud credentials.
- Left local scratch material untracked:
  `forked-for-compaction/`.

## Claim Boundary

The safe public framing is:

```text
finite entropy/min-cut shadows can be incomplete;
operator-algebraic data can be necessary to predict reconstruction or channel behavior.
```

The repository does not claim:

- a continuum quantum-gravity theorem;
- a literal de Sitter construction;
- a generic traversable-wormhole simulation;
- novelty for standard stabilizer/OA-QEC linear algebra.

## Remaining Presentation Caveats

- Historical commit metadata includes local author email addresses.
- The README preserves the project's goal/phase provenance for reproducibility.
- Several notes are theorem-program memos rather than paper-ready exposition.
- The Type-II/static-patch interpretation still depends on the chosen cutoff
  inclusion and `rank_ordered_static_patch_embedding`; this is an open
  assumption, not a canonical continuum construction.
