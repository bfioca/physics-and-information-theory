# Lift-Map Obligations

## Purpose

This ledger classifies the cutoff maps used by the continuum-lift obstruction
program. The goal is to separate finite theorem facts, bounded certificates,
conditional operator-algebra inputs, and open physics assumptions.

## Required Properties

Each lift map is checked against:

- UCP/unitality;
- trace/state compatibility;
- approximate multiplicativity;
- screen-shadow convergence;
- response-witness persistence;
- strong-continuity or generator compatibility.

## Map Classification

| Map | UCP/unital | Trace/state | Multiplicativity | Screen shadow | Response witness | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Trace-filled UCP refinement | finite proved | finite proved | error `1/N_L` | exact for declared diagonal tests | norm retained in embedded corner | finite theorem gadget |
| Spherical-harmonic projection/refinement | finite proved in harmonic basis | finite proved | inherited `1/N_L` witness | low-harmonic diagonal data exact | norm retained in low-mode corner | bounded physical-motivation certificate |
| Heat-kernel coarse graining | finite proved for declared Schur heat kernel | finite proved | decreasing bound in audit | diagonal data exact | positive retention tending to one | bounded physical-motivation certificate |
| Berezin-Toeplitz-inspired smoothing | finite proved for surrogate convex mixture | finite proved | `1/N_L + O(1/N_L)` bound | vanishing perturbation, not exact | positive retention tending to one | surrogate certificate, not canonical |
| Canonical static-patch/Berezin-Toeplitz embedding | not implemented | conditional | conditional | conditional | conditional | open operator-algebra input |

## Strong-Continuity Compatibility

The lift theorem uses the existing strong-continuity gate:

```text
||exp(delta_L G_L)-I|| <= exp(delta_L Gamma_L)-1.
```

The implemented maps preserve the finite response witness at the level of
operator-norm records. Generator covariance and physical static-patch
compatibility remain conditional unless a canonical embedding/coarse-graining
map is supplied.

## Decision

The implemented finite maps are sufficient for a proof-ready obstruction
theorem under explicit lift hypotheses. They are not sufficient to claim a
canonical continuum static-patch realization.

Therefore the branch selects outcome:

```text
A. theorem candidate with explicit conditional lift hypotheses.
```

The missing physics input is not hidden: it is the canonical
screen-compatible, response-persistent cutoff embedding or coarse-graining.

## Code Evidence

Direct helpers:

```text
qgtoy/lift_diagnostics.py::embedding_response_witness_records
qgtoy/lift_diagnostics.py::finite_lift_decision_record
```

Focused tests:

```bash
PYTHONPATH=. python3 -m unittest tests.test_lift_diagnostics tests.test_embedding_channels
```
