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

- An equation-level reduction to existing detector, observer-code, or
  integral-operator work.
- Independent checks of kernel normalization, eigenvalue simplicity, both
  remainder estimates, all-sector domination, uniqueness, or source closure.
- Independent checks of the finite-pointer Jensen bound, Harlow equation
  specialization, or branchwise gravity hypotheses.
- Stronger analytic constants with a complete proof and synchronized frozen
  artifacts.
- Reproducibility or CI fixes that do not weaken artifact provenance.
- Clearer wording at the boundary between final support, source support,
  post-switch field energy, and total apparatus cost.

## Required Updates

Changes to a theorem or constant must update all affected layers:

1. manuscript source and PDF;
2. `qgtoy/local_scalar_observer_cost.py`;
3. `qgtoy/finite_pointer_observer.py`, when the pointer, code, or gravity
   composition changes;
4. replay certificates and numerical records, when applicable;
5. focused tests;
6. proof and reviewer documentation;
7. `artifact_manifest.json` hashes.

Run `git diff --check` and the complete retained test suite before committing.

## Claim Discipline

Do not present the result as a total measurement-energy theorem, autonomous
detector construction, deterministic code-error theorem, coupled
Einstein-matter evolution, or ER=EPR result. Separate internal verification
from external novelty and proof review. A positive review is feedback, not
endorsement.

Earlier research programs remain in Git history. Do not restore them to the
current tree unless they become necessary inputs to this paper.
