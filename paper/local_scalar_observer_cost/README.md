# Local Scalar Observer-Cost Review Package

**Status:** specialist-review candidate. The analytic theorem, manuscript
build, numerical illustration, and reproducibility checks pass. Standalone
novelty remains an external-review question.

## Start Here

1. Read `main.pdf`, especially Theorem 3.3, Figure 1, and Corollary 3.4.
2. Use `REFEREE_GUIDE.md` for the exact claim, five decisive questions, and the
   requested `NARROW PAPER GO`, `STRENGTHEN`, or `NO-GO` disposition.
3. Run `audit_package.py` for a quick integrity check.

The exact gapless-detector channel is prior art. The candidate contribution is
the sharp elimination of the compact source in favor of post-switch field
energy and causal support: an exact all-angular KMS-kernel optimization, a
unique s-wave momentum extremizer, sharp support asymptotics, and smooth-source
closure. Figure 1 is a reproducible numerical illustration, not a certified
spectral bound. The Einstein-scalar material is a final-slice constraint
corollary, not a dynamical-gravity channel theorem.

## Package Map

| File | Role |
| --- | --- |
| `main.pdf` | Primary 16-page review manuscript |
| `main.tex`, `sections/`, `references.bib` | LaTeX source and bibliography |
| `REFEREE_GUIDE.md` | Review questions and requested disposition |
| `data/observer_cost_spectrum.json` | Reproducible Figure 1 data |
| `figures/observer_cost_spectrum.pdf` | Figure used by the manuscript |
| `artifact_manifest.json` | Frozen hashes and build metadata |
| `audit_package.py` | Package-integrity audit |

## Fast Integrity Check

From the repository root:

```bash
python paper/local_scalar_observer_cost/audit_package.py
```

Expected result: `status: pass`, `page_count: 16`, and no errors. This checks
the PDF and log, manuscript hashes and structure, frozen theorem certificate,
and certificate source ledger. It does not establish novelty or replace review
of the analytic proof.

## Full Replay

From the repository root:

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
PYTHONPATH=. python -m pytest -q \
  tests/test_local_scalar_observer_cost.py \
  tests/test_local_scalar_observer_manuscript.py \
  tests/test_local_scalar_observer_spectrum.py
```

The spectrum replay requires NumPy; install the `research-numerics` optional
dependency when it is not already available.

## Rebuild the PDF

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

or, when available:

```bash
tectonic -X compile main.tex --keep-logs
```

The build should have no undefined references or citations and no overfull
or underfull boxes. The checked `main.log` is retained so the review artifact
records that result. The TeX layout, reference, citation, and page-count checks
are also enforced by the package audit.

## Claim Boundary

The manuscript does not claim an autonomous detector apparatus, a channel
derived on the perturbed geometry, a coupled Einstein-matter evolution, a
universal measurement-energy theorem, observer complementarity, or ER=EPR.
