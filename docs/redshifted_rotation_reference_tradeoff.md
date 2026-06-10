# Redshifted Charged-Reference Achievability Bound

Status: exact compact-`SO(3)` same-target-sector comparison with a sufficient
Peter-Weyl cutoff and fixed-Hamiltonian rotor bound; local gravitational coupling,
boosts, and backreaction remain open

## Same-Target Question

The hard-energy collar theorem supplies a spin

```text
L_delta=Theta(sqrt(R/delta))
```

inside a fixed finite-wall static-energy window. Compare two append, reduce,
and decode experiments on that same spin sector:

```text
control:   rotation-trivial clock plus invariant spectators;
treatment: prepared SO(3) Peter-Weyl orientation reference R_J.
```

The control fixed-point expectation is completely depolarizing. Its exact
optimal normalized diamond recovery error is

```text
epsilon_clock=1-1/(2L_delta+1)^2.
```

Thus the control error tends to one at the horizon.

## Charged Reference

Use the integer-spin Peter-Weyl cutoff

```text
R_J=direct_sum_(j=0)^J V_j tensor V_j^*,
D_J=(J+1)(2J+1)(2J+3)/3.
```

The group acts on the left factor. The canonical covariant orientation POVM and
measure-and-correct decoder have tensor-rank multipliers derived in
`operational_su2_reference.md`. For `J>=L`, their largest deficit is at rank
`k=2L`:

```text
1-lambda_k(J)=
 k(k+1)[12J(J+2)-k(k+1)+11]
 /[6(2k+1)D_J].
```

The constructive normalized diamond error obeys

```text
epsilon_charged
 <= (2L+1)[1-lambda_(2L)(J)]/2.
```

Using

```text
D_J >= (4/3)J(J+1)^2,
12J(J+2)-k(k+1)+11 <= 12(J+1)^2,
```

gives the elementary bound

```text
epsilon_charged <= 3(2L+1)^2/(8J).
```

Therefore the explicit sufficient choice

```text
J_epsilon=ceil[3(2L_delta+1)^2/(8 epsilon)]
```

guarantees charged-reference recovery error at most `epsilon`. This is a
constructive upper bound, not an optimal-resource theorem.

## Fixed-Hamiltonian Bound

Give the reference the declared rigid-rotor Hamiltonian

```text
H_ref=C_left/(2I).
```

For the canonical Peter-Weyl token,

```text
<C_left>=3J(J+2)/5,
<H_ref>=3J(J+2)/(10I).
```

Since `L_delta^2~C R/delta`, the sufficient cutoff and mean energy scale as

```text
J_epsilon=O(R/(epsilon delta)),
<H_ref>=O(R^2/(I epsilon^2 delta^2)).
```

The reference Hilbert-space dimension scales as `D_J=O(delta^-3)` at fixed
target error. The result turns the qualitative instruction "add a frame" into a
quantitative compact-rotation achievability bound.

## Interpretation

The theorem gives a same-target-sector finite-wall comparison. It is not a
resource-matched experiment: the charged treatment is deliberately supplied a
large asymmetric reference state, Hilbert space, and rotor budget.

- a clock-only fixed point loses the full spin sector asymptotically;
- a rotationally charged reference achieves any fixed nonzero accuracy;
- the displayed constructive realization has an inverse-gap fixed-Hamiltonian
  mean-energy upper bound.

The `delta^-2` mean-energy law assumes that `I` is fixed independently of
`delta` and `epsilon`; allowing cutoff-dependent inertia changes the scaling.
The prepared token is also coherent across rotor energies, so this is an
instantaneous channel benchmark without a lifetime or phase-tracking theorem.

This does not imply that gravity supplies this rotor, that the bound is optimal,
or that the full `SO(1,4)` observer behaves identically. It gives a sharp target
for a covariant-observer calculation: derive the moment of inertia and reference
Hamiltonian from the observer worldline or edge system, then test whether
backreaction preserves or changes the inverse-`delta` cutoff law.

The exact obstruction to inferring that Hamiltonian from covariance and recovery
alone is proved separately in `covariant_observer_energy_no_go.md`. In particular,
the same token and decoder admit positive invariant Casimir Hamiltonians with any
prescribed ground-subtracted token energy. The fixed-`I` law here is therefore a
valid model calculation, not an observer-algebra prediction.

## Claim Boundary

Established:

1. the hard-energy target spin from the finite-wall conformal scalar;
2. the exact clock-only replacer error;
3. the exact Peter-Weyl tensor-rank deficit formula;
4. the sufficient `J_epsilon` cutoff and fixed-`I` rotor mean-energy scaling;
5. an executable same-target channel separation at every wall in the audit.

Not established:

1. optimality of the Peter-Weyl decoder or resource cost;
2. a local interaction between the reference and Bunch-Davies net;
3. a gravitational derivation of `I` or `H_ref`, or a lifetime bound;
4. noncompact boosts or the full `SO(1,4)` constraint;
5. backreaction, a Type-II trace, or generalized entropy.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy redshifted-rotation-reference-tradeoff
PYTHONPATH=. python3 -m unittest tests.test_redshifted_rotation_reference_tradeoff
```
