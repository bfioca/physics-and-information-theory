# Continuum-Lift Decision Ledger

## Selected Outcome

```text
A. proof-ready continuum-lift obstruction theorem with explicit hypotheses.
```

This is not a continuum de Sitter theorem. It is an obstruction theorem for
any proposed dictionary that satisfies the stated lift conditions and factors
only through screen-shadow data.

## Condition Ledger

| Lift condition | Status | Evidence |
| --- | --- | --- |
| Screen-shadow equality | `finite_proved` | `docs/screen_shadow_functor_spec.md`; `declared_screen_shadow_record` |
| Operator-norm response separation | `finite_proved` | `docs/response_witness_spec.md`; `response_witness_record` |
| Implemented lift-map response persistence | `bounded_certified` | `embedding_response_witness_records`; `tests.test_lift_diagnostics` |
| Implemented lift-map screen convergence | `bounded_certified` | `docs/lift_map_obligations.md`; `tests.test_embedding_channels` |
| Strong-continuity gate | `finite_proved` | `docs/goals24_31_static_patch_bridge_theorem_note.md`; `tests.test_static_patch_strong_continuity` |
| Canonical static-patch embedding | `conditional_assumption` | current harmonic/heat/Berezin maps are audits, not canonical constructions |
| Continuum observer-algebra compatibility | `conditional_assumption` | requires external operator-algebra/static-patch input |

## Failed Conditions

None inside the declared finite theorem and bounded-certificate package.

The following are not failures, but remain conditional inputs for physical
static-patch interpretation:

- canonical cutoff embedding or coarse graining;
- compatibility with a proposed Type-`II_1` static-patch observer algebra;
- continuum state/dynamics convergence beyond the finite benchmark.

## Why This Is A, Not B or C

It is not **B/no-go** because the implemented non-factorial lift maps retain a
positive operator-norm response witness and preserve or converge on the
declared screen shadows in the bounded audit.

It is not primarily **C/weakest-added-assumption** because the obstruction
theorem can already be stated and proved under explicit lift hypotheses. The
remaining static-patch input is named as a conditional assumption rather than
smuggled into the proof.

The weakest physical assumption needed for a continuum static-patch
instantiation is:

```text
there exists a screen-compatible cutoff embedding/coarse-graining whose
screen shadows converge and whose operator-norm response witness persists.
```

## Machine-Readable Evidence Path

The direct finite decision helper is:

```text
qgtoy/lift_diagnostics.py::finite_lift_decision_record
```

The current certificate includes this decision record:

```bash
PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5
```

Focused tests:

```bash
PYTHONPATH=. python3 -m unittest tests.test_lift_diagnostics tests.test_continuum_lift_obstruction tests.test_embedding_channels
```
