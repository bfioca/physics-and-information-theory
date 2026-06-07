# Physics and Information Theory Toy Verifier

Finite, executable diagnostics for observer algebras, reconstruction, and
static-patch-inspired bridge channels.

This repository is a research-code benchmark suite. It uses small exact models
to test when screen-visible data, entropy shadows, min-cut shadows, or
restricted transfer records are too coarse to determine an observer algebra or
bridge channel.

The current public package is deliberately finite. It is not a continuum
de Sitter theorem, not a dS/CFT construction, and not a proof of ER=EPR in de
Sitter.

## Current Packaged Result

```text
Finite static-patch screen shadows do not determine the observer algebra.
Intrinsic operator response, cutoff-compatible strong continuity, and
embedding data distinguish a quantum matrix-algebra regulator from an abelian
dephased control.
```

The packaged result is frozen at:

```text
v0.1-static-patch-diagnostics
```

## Start Here

| File | Purpose |
| --- | --- |
| [`paper/main.md`](paper/main.md) | Canonical paper-style draft. |
| [`paper/main.tex`](paper/main.tex) | Attachment-ready TeX version of the focused note. |
| [`THEOREMS.md`](THEOREMS.md) | Theorem and claim index with certificate commands. |
| [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | One-command reproduction, expected output, and test boundary. |
| [`artifacts/static_patch_diagnostics/MANIFEST.md`](artifacts/static_patch_diagnostics/MANIFEST.md) | Frozen certificate artifacts for the packaged result. |
| [`paper/expert_feedback_note.md`](paper/expert_feedback_note.md) | Two-page expert-facing note. |
| [`paper/expert_cover_note.md`](paper/expert_cover_note.md) | Short cover note for expert feedback. |
| [`paper/PUBLISHING_CHECKLIST.md`](paper/PUBLISHING_CHECKLIST.md) | Publishing checklist; only external-feedback follow-up remains open. |
| [`docs/README.md`](docs/README.md) | Map of the broader research trail. |

Expert feedback bundle:

```text
paper/expert_cover_note.md
paper/expert_feedback_note.md
```

Mention that `paper/main.tex`, `paper/main.md`, and the executable certificate
repository are available as supporting material. Do not lead with the full
repository or goal history.

## Quick Reproduction

No runtime dependencies are required beyond Python 3.11+.

Run the compact static-patch package summary:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

Expected result: five certificate entries with `status: pass` and
`all_certified_claims_true: true`.

Run the focused regression suite:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics tests.test_embedding_channels tests.test_continuum_lift_obstruction
```

Validate the frozen JSON artifacts:

```bash
python3 -m json.tool artifacts/static_patch_diagnostics/compact_summary.json
python3 -m json.tool artifacts/static_patch_diagnostics/environment.json
```

For the full command list and expected output, see
[`REPRODUCIBILITY.md`](REPRODUCIBILITY.md).

## What The Package Claims

The safe claim is:

```text
Finite screen-visible shadows can be incomplete; operator-algebraic response
can be necessary to identify the observer algebra or bridge channel.
```

The package separates:

- exact finite theorem-style statements;
- bounded certificate evidence;
- conditional operator-algebra lift assumptions;
- continuum motivation and speculation.

It does not claim:

- a continuum de Sitter observer-algebra theorem;
- a dS/CFT dictionary;
- literal ER=EPR in de Sitter;
- novelty of standard stabilizer/OA-QEC, Schur-channel, UHF, or Type `II_1`
  background facts;
- canonical status for the current cutoff embeddings.

## Repository Layout

| Path | Contents |
| --- | --- |
| `paper/` | Paper draft, expert notes, and publishing checklist. |
| `artifacts/static_patch_diagnostics/` | Frozen JSON certificates for the release package. |
| `docs/` | Research notes, certificate indexes, and historical audit trail. |
| `examples/` | Small reviewer-facing reproduction script. |
| `qgtoy/` | Finite-model implementations and CLI certificate constructors. |
| `tests/` | Focused regression tests for certificate modules. |

## Background Trail

Earlier goals remain in `docs/` as audit artifacts. The broad arc is:

- stabilizer/OA-QEC entropy versus reconstruction diagnostics;
- finite observer-algebra tomography and bridge-channel benchmarks;
- static-patch screen-shadow no-gos and continuity gates;
- finite-to-Type-`II_1` scaffolding and cutoff-embedding audits;
- conditional continuum-lift obstruction for screen-only dictionaries.

For the packaged static-patch path, start with
[`docs/static_patch_observer_algebra/README.md`](docs/static_patch_observer_algebra/README.md).

## Development Notes

Use the focused regression suite before changing the packaged result:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics tests.test_embedding_channels tests.test_continuum_lift_obstruction
```

When adding new claims, update:

- [`paper/main.md`](paper/main.md);
- [`THEOREMS.md`](THEOREMS.md);
- [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md);
- the relevant certificate index under `docs/` or `artifacts/`.

Keep the claim boundary explicit. This repository is useful precisely because
it distinguishes finite certificate-backed results from continuum speculation.
