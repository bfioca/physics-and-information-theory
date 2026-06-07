# Contributing

This repository is a finite certificate suite and research-code notebook. The
most valuable contributions improve reproducibility, claim boundaries, and
independent checks.

## Development Setup

No runtime dependencies are required beyond Python 3.11+.

Run the packaged static-patch regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics
```

Run the compact reproduction script:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

Validate package indexes:

```bash
python3 -m json.tool docs/static_patch_observer_algebra/audit_index.json
python3 -m json.tool docs/goals24_31_static_patch_bridge_certificate_index.json
python3 -m json.tool docs/major_goal_finite_to_typeii_static_patch_observer_algebra_certificate_index.json
python3 -m json.tool docs/inclusion_covariant_static_patch_dynamics_certificate_index.json
```

## Claim Discipline

Keep claims in one of four buckets:

- exact finite theorem-style claim;
- bounded exhaustive or bounded numerical certificate;
- conditional operator-algebra assumption;
- continuum speculation or open problem.

Do not describe finite certificates as continuum de Sitter, dS/CFT,
approximate-QEC, or ER=EPR theorems.

## Preferred Contributions

- independent proof sketches for helper bounds;
- stronger tests that compute a witness directly rather than checking only
  top-level certificate booleans;
- clearer screen-shadow definitions;
- canonical static-patch cutoff embeddings or no-go results;
- small reproducible examples and CI improvements.

## Documentation Rules

When adding a new result, include:

1. a human note;
2. a machine-readable certificate index;
3. exact reproduction commands;
4. focused tests;
5. an explicit claim boundary.

For the current front door, update:

- `README.md`;
- `THEOREMS.md`;
- `docs/static_patch_observer_algebra/README.md`;
- `docs/static_patch_observer_algebra/audit_index.json`.

