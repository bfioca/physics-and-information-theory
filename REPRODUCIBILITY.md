# Reproducibility

This document reproduces the finite-pointer observer-entropy manuscript and
its review package from a clean checkout.

## Environment

- Python 3.11 or newer
- NumPy 2.x for the numerical spectrum
- Tectonic 0.16.9 or a compatible LaTeX toolchain

Install the package and numerical extra:

```bash
python -m pip install -e '.[research-numerics]'
```

## Complete Test Suite

```bash
PYTHONPATH=. python -m pytest -q
```

The suite covers channel normalization, the finite-pointer Jensen theorem,
the Harlow-code insertion, branchwise gravity, the localization certificate,
manuscript structure, two independent numerical implementations, review
links, artifact provenance, and deterministic specialist packets.

## Four-Gate Finite-Pointer Replay

```bash
PYTHONPATH=. python experiments/finite_pointer_observer_audit.py
```

This regenerates
`experiments/finite_pointer_observer_certificate.json`. Its status must be

```text
pass_four_gate_algebra
```

and all certified claims must pass. The four gates are:

1. exact finite-pointer Schur channel and binary normalization;
2. exact purity and Renyi bound from pairwise localization;
3. insertion into the Harlow-Usatyuk-Zhao orthogonal-pair second moment; and
4. composition with a branchwise final-slice gravity budget.

## Independent Finite-Pointer Replay

```bash
PYTHONPATH=. python experiments/finite_pointer_observer_clean_room_check.py
```

The script imports neither `qgtoy.finite_pointer_observer` nor the production
four-gate audit. It checks 64 deterministic finite-dimensional cases,
including the pairwise variance identity, purity bound, code factor, gravity
coefficient, and binary saturation. Its status must be

```text
pass_independent_computation_nonrigorous
```

This verifies algebra and implementation independence; it is not a continuum
proof or a novelty review.

## Localization Theorem Replay

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
```

This regenerates the source-bound analytic certificate for the exact
localized thermal coefficient and de Sitter all-sector reduction.

## Numerical Spectrum

```bash
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
```

The command regenerates the numerical data and Figure 1 under
`paper/local_scalar_observer_cost/`. It uses exact cell integrals for the
vacuum logarithmic kernel and quadrature for the smooth thermal correction.
The result is convergence-checked numerical evidence, not an interval proof.

## Independent Localization Replay

```bash
PYTHONPATH=. python experiments/local_scalar_observer_clean_room_check.py
```

This checker uses a different discretization and imports neither `qgtoy` nor
the production Galerkin implementation. It tests the rigorous brackets,
asymptotic remainders, eigenvector positivity, and coordinate-sector
domination.

## Rebuild the Manuscript

From `paper/local_scalar_observer_cost/`:

```bash
tectonic -X compile main.tex --keep-logs
```

The expected artifact is a 23-page `main.pdf`. The retained `main.log`
must have no undefined references or citations and no overfull or underfull
boxes.

## Package Audit

```bash
python paper/local_scalar_observer_cost/audit_package.py
```

The result must report `"status": "pass"`. The audit verifies frozen hashes,
TeX closure, PDF page count, build log, both analytic certificates, the
production spectrum, and both independent replay records. It does not certify
the physics interpretation or literature novelty.

## Review Packet Build

After committing the exact revision:

```bash
python paper/local_scalar_observer_cost/build_review_packets.py
```

The builder refuses a dirty tracked checkout and creates deterministic,
revision-pinned detector/QFT, operator-theory, and observer-code archives under
`dist/local_scalar_observer_review/`. Packet hashes must be recorded with
any external response.

## Interpretation

Passing every command establishes internal reproducibility and provenance. It
does not establish arbitrary-dimension sharpness, a deterministic code error
floor, an autonomous observer, coupled gravitational dynamics, or standalone
novelty.
