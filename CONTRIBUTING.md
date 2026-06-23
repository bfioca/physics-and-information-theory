# Contributing

This repository supports one active mathematical-physics manuscript. The most
valuable contributions are independent proof checks, missing prior art,
reproducibility improvements, and corrections that preserve the stated model
boundary.

## Setup

```bash
python -m pip install -e '.[research-numerics]'
PYTHONPATH=. python -m pytest -q
python paper/local_scalar_observer_cost/audit_package.py
```

## Contribution Priorities

- An equation-level reduction to existing detector or integral-operator work.
- Independent checks of kernel normalization, eigenvalue simplicity, both
  remainder estimates, all-sector domination, uniqueness, or source closure.
- Stronger analytic constants with a complete proof and synchronized frozen
  artifacts.
- Reproducibility or CI fixes that do not weaken artifact provenance.
- Clearer wording at the boundary between final support, source support,
  post-switch field energy, and total apparatus cost.

## Required Updates

Changes to a theorem or constant must update all affected layers:

1. manuscript source and PDF;
2. `qgtoy/local_scalar_observer_cost.py`;
3. replay certificate and numerical record, when applicable;
4. focused tests;
5. proof and reviewer documentation;
6. `artifact_manifest.json` hashes.

Run `git diff --check` and the complete retained test suite before committing.

## Claim Discipline

Do not present the result as a total measurement-energy theorem, autonomous
detector construction, coupled Einstein-matter evolution, Paper U theorem, or
ER=EPR result. Separate internal verification from external novelty and proof
review. A positive review is feedback, not endorsement.

Earlier research programs remain in Git history. Do not restore them to the
current tree unless they become necessary inputs to this paper.
