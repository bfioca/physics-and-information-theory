# Observer-Local Noncommutative Subsystem

## Purpose

The previous audit showed that canonical scalar fuzzy-sphere routes preserve
screen data but classicalize their commutators. This note tests the next
candidate source of noncommutativity:

```text
an observer-local tangent-plane subsystem selected by coherent-state/static-patch
structure rather than by bridge-witness labels.
```

## Outcome

```text
A. theorem candidate.
```

For a fixed observer pole and fixed excitation cutoff `R`, the fuzzy-sphere
spin representation has a local tangent-plane scaling

```text
a_L = J_+ / sqrt(2j),
a_L^* = J_- / sqrt(2j),
L = 2j.
```

On the low-excitation state `|r>` around the north-pole coherent state,

```text
[a_L, a_L^*] |r> = (1 - 2r/L) |r>.
```

Therefore on the fixed observer-local window `r <= R`,

```text
[a_L, a_L^*] >= (1 - 2R/L) I.
```

For fixed `R`, the lower bound tends to `1` as `L -> infinity`. This gives a
finite observer-local noncommutative subsystem whose commutator does not
classicalize in the scalar screen limit.

## Candidate Audit

| Candidate | Status | Main lesson |
| --- | --- | --- |
| Coherent-state tangent-plane double scaling | theorem candidate | Rescaled fuzzy-sphere ladder operators retain a nonzero commutator lower bound on fixed low-excitation windows. |
| Local Planck-cell matrix block | theorem candidate | The low-excitation block is norm-faithful under observer-local isometric refinement, but still depends on selecting an observer patch. |
| Matrix-valued screen fiber | conditional | A fixed fiber would work, but its physical origin is not derived from scalar screen data. |
| Modular crossed-product clock shift | conditional | A modular shift can generate noncommutativity, but KMS/screen data alone do not select it. |

## Gate Matrix

| Candidate | Selection | CP/trace | Covariance | Screen | Norm | Commutator | Continuity | Type-II route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tangent-plane scaling | pass | pass | pass | pass | pass | pass | pass | conditional |
| Local matrix block | pass | pass | conditional | pass | pass | pass | pass | conditional |
| Matrix screen fiber | pass | conditional | conditional | pass | conditional | conditional | conditional | conditional |
| Modular clock shift | pass | conditional | conditional | pass | conditional | conditional | conditional | conditional |

## Interpretation

The global scalar `S^2` limit is not where the observer algebra lives. The
finite certificates now separate two limits:

1. scalar low-mode/fuzzy-coordinate limit: screen-compatible but commutative;
2. observer-local tangent-plane limit: screen-compatible and noncommutative on
   fixed low-excitation windows.

This is the first positive finite route from fuzzy-sphere cutoff data to a
noncommutative observer-local subsystem. It is not a continuum de Sitter
theorem. The remaining physics assumption is that the observer pole/static
patch and low-excitation window are the correct local data.

## Expert Question

Is the coherent-state tangent-plane sector the right finite static-patch
analogue of the observer-local algebra, or should the noncommutative subsystem
instead come from an edge-mode fiber or modular crossed product?

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy observer-local-subsystem --max-cutoff 12 --excitation-cutoff 2
```

Run the focused test:

```bash
PYTHONPATH=. python3 -m unittest tests.test_observer_local_subsystem
```
