# Final-Support Thermal Dephasing Review Package

**Status:** strengthened short-paper candidate. Analytic, build, numerical,
and reproducibility checks are internal gates. Independent proof review and
two-domain novelty review remain required before submission.

## Start Here

1. Read `main.pdf`, beginning with the general thermal half-line theorem and
   its conformal de Sitter specialization.
2. Use `REFEREE_GUIDE.md` for the common claim boundary.
3. Use `QFT_NOVELTY_REVIEW.md` or `OPERATOR_NOVELTY_REVIEW.md` for the
   appropriate specialist questions.
4. Send the matching minimal packet from `EXTERNAL_REVIEW_LAUNCH.md` and ask
   for a written disposition in `REVIEW_RESPONSE_FORM.md`.
5. Run `audit_package.py` for a quick integrity check.

The exact gapless-detector channel is prior art. The candidate contribution is
the exact reflected KMS operator selected by final support, its
general-temperature coefficient, the full de Sitter sector reduction, and its
sharp support asymptotics.

## Package Map

| File | Role |
| --- | --- |
| `main.pdf` | Primary review manuscript |
| `main.tex`, `sections/`, `references.bib` | LaTeX source and bibliography |
| `REFEREE_GUIDE.md` | Shared claim and disposition guide |
| `QFT_NOVELTY_REVIEW.md` | Detector/QFT specialist questions |
| `OPERATOR_NOVELTY_REVIEW.md` | Operator-theory specialist questions |
| `EXTERNAL_REVIEW_LAUNCH.md` | Send-ready attachment sets and outreach drafts |
| `REVIEW_RESPONSE_FORM.md` | Structured, auditable specialist disposition |
| `data/observer_cost_spectrum.json` | Reproducible numerical illustration |
| `artifact_manifest.json` | Frozen hashes and build metadata |
| `audit_package.py` | Package-integrity audit |

## Full Replay

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

The spectrum replay requires NumPy through the optional `research-numerics`
dependency.

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

Sharpness concerns final Cauchy support, not every fixed smaller source
cylinder. The energy is post-switch scalar-field energy, not total apparatus
cost. The manuscript does not claim an autonomous detector, a perturbed-
geometry channel, coupled gravitational evolution, or a universal
measurement-energy theorem.
