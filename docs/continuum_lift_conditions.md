# Continuum Lift Conditions and Screen-Only Dictionary Obstruction

## Claim Boundary

This note does not construct continuum de Sitter, dS/CFT, or ER=EPR. It states
a conditional obstruction schema: if finite static-patch regulator sequences
lift to a continuum observer-algebra setting while preserving the declared
screen shadows and response witnesses, then any dictionary that factors only
through screen shadows is incomplete.

## Lift Conditions

A finite regulator sequence should provide:

1. embedding or coarse-graining maps between cutoffs;
2. trace/state convergence;
3. screen-shadow convergence;
4. strong-continuity or generator control;
5. persistence or controlled decay of operator-response witnesses;
6. compatibility with the proposed observer-algebra limit.

These are conditions for a future continuum/static-patch lift, not claims that
the current repository already has one.

## Obstruction Schema

Suppose two finite regulator sequences have:

```text
screen_shadow_distance -> 0,
response_witness_gap -> c > 0.
```

Then a dictionary that factors only through the limiting screen-shadow data
cannot determine the limiting observer algebra. The screen data identify the
two sequences, while the response witness separates them.

This turns the missing continuum bridge into a useful constraint:

```text
any proposed dS/CFT/static-patch dictionary that only sees screen shadows is
provably incomplete under the lift conditions.
```

## Relation To The Existing Package

The prior finite package supplies:

- screen-shadow collisions;
- strong-continuity gates;
- a Type-II candidate scaffold under chosen inclusions;
- inclusion-covariant dynamics evidence.

The new lift note adds:

- explicit lift conditions;
- a consecutive-cutoff UCP refinement alternative to exact factorial
  inclusions;
- a screen-only dictionary obstruction theorem schema.

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5
```

Run the focused regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_continuum_lift_obstruction
```

Validate the machine-readable index:

```bash
python3 -m json.tool docs/continuum_lift_obstruction_certificate_index.json
```
