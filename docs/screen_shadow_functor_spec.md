# Screen-Shadow Functor Specification

## Claim Boundary

This is a finite benchmark definition. It does not define a canonical
continuum gravitational screen. It formalizes exactly the data that the current
static-patch package allows a screen-only dictionary to read.

## Definition

At cutoff `L`, let

```text
A_L^q = M_{N_L},       A_L^c = C^{N_L},       S_L = C^{N_L}.
```

Let

```text
E_diag : M_{N_L} -> C^{N_L}
```

be the diagonal conditional expectation in the declared screen basis. The
screen-shadow functor is the tuple

```text
Sh_L(A_L, rho_L, Lambda_L) = (F(A_L, rho_L, Lambda_L))_{F in Scr_L}
```

where every `F in Scr_L` factors through the declared screen data:

- diagonal observables through `E_diag`;
- low-order diagonal correlators;
- horizon-overlap data;
- screen-restricted transfer records;
- certificate-emitted screen-shadow fields.

Equivalently, `Sh_L` is blind to whether the diagonal data came from the
noncommutative algebra `M_N` or the dephased abelian control `C^N`.

## Finite Equality Theorem

For the declared benchmark class,

```text
Sh_L(M_{N_L}) = Sh_L(C^{N_L})
```

whenever the diagonal state, horizon-overlap data, and screen-restricted
transfer records are matched.

## Proof

Every component functional in `Scr_L` factors through `S_L=C^{N_L}`. The
quantum model and dephased control have the same screen algebra and the same
declared diagonal payload after applying `E_diag`. Therefore every component
of the tuple `Sh_L` agrees. The proof uses only the declared factorization
property and does not inspect off-diagonal matrix units.

## Code Evidence

The direct finite helper is:

```text
qgtoy/lift_diagnostics.py::declared_screen_shadow_record
```

The helper validates the source algebra kind but does not include it in the
returned screen shadow. This implements the screen-only restriction.

The direct equality check is:

```text
qgtoy/lift_diagnostics.py::screen_shadow_equal_for_quantum_dephased
```

The focused tests are:

```bash
PYTHONPATH=. python3 -m unittest tests.test_lift_diagnostics
```

## What This Does Not Prove

This does not prove that real de Sitter screen data are exactly these finite
fields. It proves that any dictionary restricted to the declared finite
screen-shadow class cannot see the noncommutative observer response isolated
in `docs/response_witness_spec.md`.
