# Reproducibility

This document reproduces the final-support thermal dephasing manuscript and its
review package from a clean checkout.

## Environment

- Python 3.11 or newer
- NumPy 2.x for the numerical spectrum
- Tectonic 0.16.9 or a compatible LaTeX toolchain to rebuild the PDF

Install the package and numerical extra:

```bash
python -m pip install -e '.[research-numerics]'
```

## Focused Test Suite

Run all retained tests:

```bash
PYTHONPATH=. python -m pytest -q
```

Expected result:

```text
47 passed
```

The suite covers the analytic certificate, theorem normalization and scaling,
manuscript structure, source-bound frozen records, numerical convergence,
review-document links, and deterministic external-review packets.

## Analytic Replay

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
```

The command regenerates
`experiments/local_scalar_observer_cost_certificate.json`. Its status must be

```text
strengthened_final_support_theorem_pass_external_review_open
```

and its source hashes must match the audit script and
`qgtoy/local_scalar_observer_cost.py`.

## Numerical Spectrum

```bash
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
```

This regenerates the numerical data and both Figure 1 formats under
`paper/local_scalar_observer_cost/`. The computation uses exact cell integrals
for the vacuum logarithmic kernel and Gauss-Legendre quadrature only for the
smooth thermal correction. It is a convergence-checked illustration, not an
interval proof.

## Package Audit

```bash
python paper/local_scalar_observer_cost/audit_package.py
```

Expected summary:

```text
"status": "pass"
"page_count": 18
"checked_files": 25
```

The audit verifies artifact hashes, TeX labels and citations, PDF and build-log
closure, the theorem certificate, numerical data, and figure provenance.

## External-Review Bundles

From a clean committed checkout, run:

```bash
python paper/local_scalar_observer_cost/build_review_packets.py
```

The builder writes ignored ZIP archives under
`dist/local_scalar_observer_review/`. Each bundle pins the full Git revision,
commit time, source URL, and attachment hashes. Repeated builds at one commit
must be byte-for-byte identical. The builder refuses a dirty tracked worktree.

## Rebuild the Manuscript

From `paper/local_scalar_observer_cost/`:

```bash
tectonic -X compile main.tex --keep-logs
```

or:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The checked build has 18 pages and no undefined references or citations,
overfull boxes, or underfull boxes.

## What This Establishes

The replay establishes internal consistency, deterministic provenance, and
the stated finite calculations. It does not establish standalone novelty,
model an autonomous source actuator, rederive the channel on perturbed
geometry, or replace independent proof review.
