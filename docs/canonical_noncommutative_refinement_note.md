# Canonical Noncommutative Cutoff Refinement

## Purpose

This note attacks the missing assumption from the physical static-patch lift
audit:

```text
a canonical noncommutative cutoff refinement that is norm-faithful on a fixed
finite nonabelian operator subsystem.
```

The question is not whether some hand-picked matrix unit survives. The
question is whether a physically selected subsystem, such as low angular modes,
fuzzy coordinates, coherent patches, Toeplitz matrix fibers, or heat-stable
low-energy operators, can carry a cutoff-independent noncommutative response.

## Outcome

```text
C. sharper minimal missing assumption.
```

Canonical scalar fuzzy-sphere routes are too classical: they can preserve
screen shadows, norms, covariance, and approximate products while their
commutator scale vanishes in the large-cutoff limit. Conditional
noncommutative routes remain possible, but each requires a physical selection
principle for a fixed noncommutative subsystem.

## Sharper Missing Assumption

```text
the static-patch cutoff refinement must canonically select a noncommutative
operator subsystem whose commutator scale has a nonzero large-cutoff lower
bound, while remaining screen-compatible, trace-compatible, approximately
covariant, and cutoff-continuous
```

This is sharper than the previous norm-faithfulness assumption. Norm
faithfulness alone is not enough: scalar fuzzy-sphere sectors can retain norms
while becoming commutative.

## Candidate Audit

| Candidate subsystem | Verdict | Main lesson |
| --- | --- | --- |
| Low angular-momentum matrix modes | no-go | Low scalar modes are naturally selected and norm-retained, but their commutator scale goes to zero. |
| Fuzzy coordinate polynomial algebra | no-go | Standard scalar fuzzy-sphere/Berezin convergence approximates `C(S^2)`, so it abelianizes. |
| Coherent-state localized matrix patches | conditional | A fixed-rank patch could work if static-patch physics supplies canonical patch transport. |
| Matrix-valued Toeplitz/Berezin fiber | conditional | A fixed matrix fiber gives the right theorem schema, but the fiber must be physically derived. |
| Heat-kernel-refined low-energy system | conditional | Heat stability and strong continuity are not enough unless the low-energy sector contains a fixed noncommutative subsystem. |

## Gate Matrix

| Candidate | Selection | CP/trace | Multiplicative | Covariant | Screen | Norm | Nonzero commutator | Continuity | Type-II route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Low angular modes | pass | pass | pass | conditional | pass | pass | fail | conditional | fail |
| Fuzzy coordinates | pass | pass | pass | pass | pass | conditional | fail | pass | fail |
| Coherent patches | pass | conditional | conditional | conditional | conditional | conditional | conditional | conditional | conditional |
| Matrix Toeplitz fiber | pass | conditional | conditional | conditional | conditional | conditional | conditional | conditional | conditional |
| Heat-stable low energy | pass | pass | pass | pass | pass | pass | conditional | pass | conditional |

## No-Go Statement

Canonical scalar screen/fuzzy-sphere data cannot by themselves supply the
needed observer-algebra lift. For fixed low-degree scalar sectors, the finite
maps can preserve the declared screen shadows and retain operator norms, while
the commutator upper bound decays like `O(1/L)`. Thus scalar low-mode
faithfulness does not imply persistent noncommutative observer response.

## Conditional Theorem Schema

If static-patch/fuzzy-sphere physics supplies a canonical refinement selecting
a fixed finite noncommutative operator subsystem with:

1. CP/unital/trace compatibility, or controlled nonunitarity;
2. approximate covariance;
3. approximate multiplicativity on the subsystem;
4. screen-shadow compatibility;
5. cutoff-compatible strong continuity;
6. a nonzero large-cutoff commutator lower bound;

then the existing continuum-lift obstruction applies to that subsystem:
screen-only data cannot determine the observer algebra.

## Expert Question

Does static-patch/fuzzy-sphere physics supply a canonical noncommutative
matrix fiber, coherent patch, or heat-stable operator subsystem with
cutoff-independent commutator scale, or must the observer algebra be added as
extra non-screen data?

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy canonical-noncommutative-refinement --max-cutoff 6
```

Run the focused test:

```bash
PYTHONPATH=. python3 -m unittest tests.test_canonical_noncommutative_refinement
```
