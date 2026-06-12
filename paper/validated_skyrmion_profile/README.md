# Validated Skyrmion Profile Manuscript

Status: specialist-review draft; exact proof replays, checked-package audit,
and internal mathematical/publication referee passes are complete.

This directory contains the selected Paper A manuscript. Its central claim is
the computer-assisted existence and local uniqueness theorem for one prescribed
massive Dirichlet-confined fixed-de-Sitter Skyrmion profile, with authenticated
radial and spectral consequences.

Build from this directory with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The checked PDF in this branch was built with Tectonic 0.16.9:

```bash
tectonic -X compile main.tex --keep-logs
```

The build must finish without overfull or underfull boxes, unresolved
references, or undefined citations. The checked `main.log` is retained so a
clean-checkout package audit does not silently skip layout validation.
`artifact_manifest.json` records the source, build-log, and PDF hashes.

Audit the checked package, its two proof certificates, and the pinned sharp
tube snapshot from the repository root with:

```bash
python -m pip install -e . 'pytest>=8,<10'
python paper/validated_skyrmion_profile/audit_package.py
```

The full AU.1/AU.2 JSON includes its literal command and dependency versions.
For a replay written to a different path or run under another supported Python
environment, pass it with `--replay-au2`; the audit compares the canonical
mathematical payload while excluding only those two volatile provenance
fields. The exact commands are in the manuscript's reproducibility section.

The manuscript deliberately does not claim global uniqueness, a
self-gravitating solution, full dynamical stability, a smooth-confinement
limit, or an observer theorem. The route decision and submission gates are in
`../../docs/publishable_paper_route_decision.md`.
