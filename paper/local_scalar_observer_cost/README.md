# Finite-Pointer Observer Entropy Review Package

**Status:** internally closed paper candidate. Analytic, build, two-method
numerical, clean-room proof, and reproducibility checks pass. External proof
coverage and three specialist dispositions remain required before submission.

## Start Here

1. Read `main.pdf`, beginning with the finite-pointer entropy theorem and
   observer-code record substitution.
2. Use `REFEREE_GUIDE.md` for the common claim hierarchy and boundary.
3. Choose `QFT_NOVELTY_REVIEW.md`, `OPERATOR_NOVELTY_REVIEW.md`, or
   `OBSERVER_CODE_REVIEW.md` for the relevant specialist questions.
4. Build the revision-pinned packets with `build_review_packets.py`, then use
   `EXTERNAL_REVIEW_LAUNCH.md` for a concise review request.
5. Record the response in `REVIEW_RESPONSE_FORM.md`.
6. Consult the
   [finite-pointer derivation](../../docs/finite_pointer_observer_entropy.md)
   and [clean-room localization audit](../../docs/local_scalar_observer_proof_audit.md),
   then run `audit_package.py` for provenance.

The exact gapless-detector channel is prior art. The candidate contribution is
the finite-pointer purity and Renyi bound with an exact localized thermal
coefficient, its all-sector de Sitter realization, the explicit second-moment
floor obtained by substituting a nonideal Stinespring record for the ideal
Harlow-code clone, and the branchwise final-slice gravity corollary.

## Package Map

| File | Role |
| --- | --- |
| `main.pdf` | Primary review manuscript |
| `main.tex`, `sections/`, `references.bib` | LaTeX source and bibliography |
| `REFEREE_GUIDE.md` | Shared claim and disposition guide |
| `QFT_NOVELTY_REVIEW.md` | Detector/QFT normalization, model, and novelty questions |
| `OPERATOR_NOVELTY_REVIEW.md` | Thermal-kernel reduction and operator-theory questions |
| `OBSERVER_CODE_REVIEW.md` | Harlow-code record substitution, entropy, and gravity questions |
| `EXTERNAL_REVIEW_LAUNCH.md` | Send-ready attachment sets and outreach drafts |
| `REVIEW_RESPONSE_FORM.md` | Structured specialist disposition |
| `REVIEWER_SHORTLIST.md` | Ranked contact routes |
| `PRIORITY_AUDIT.md` | Exact reductions and first-failed-hypothesis ledger |
| `build_review_packets.py` | Deterministic, commit-pinned specialist ZIP builder |
| `data/observer_cost_spectrum.json` | Reproducible numerical illustration |
| `artifact_manifest.json` | Frozen hashes and build metadata |
| `audit_package.py` | Package-integrity and certificate audit |

## Full Replay

From the repository root:

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
PYTHONPATH=. python experiments/local_scalar_observer_clean_room_check.py
PYTHONPATH=. python experiments/finite_pointer_observer_audit.py
PYTHONPATH=. python experiments/finite_pointer_observer_clean_room_check.py
PYTHONPATH=. python -m pytest -q
python paper/local_scalar_observer_cost/audit_package.py
```

The spectrum replay requires NumPy through the optional
`research-numerics` dependency.

## Rebuild the PDF

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

or:

```bash
tectonic -X compile main.tex --keep-logs
```

The checked log must contain no undefined references or citations and no
overfull or underfull boxes.

## Claim Boundary

The resource is centered post-switch scalar-field energy, not total apparatus
cost. The finite pointer and sources are prescribed. The field record is a
nonideal Stinespring-record substitution, not a realization of the exact
pointer-basis clone. The code consequence is an ensemble mean-square statement
for an orthogonal CRT-real pair, not a deterministic or uniform code theorem.
The gravity result assumes a local
constraint budget on every conditional spherical branch and does not describe
coupled gravitational evolution. General-d sharpness is not claimed.
