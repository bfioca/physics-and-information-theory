# Core-Stable Angular Edge Obstruction

Status: exact factorized bridge theorem; interacting KMS model open

## Purpose

The relational fuzzy-horizon theorem and the Type-III many-body regulator were
previously separate systems. This note constructs the simplest honest bridge
and asks a precise question: can the observer clock or Type-II continuous core
restore angular information that a frame conditional expectation removed?

The answer is no in the factorized model.

## Factorized KMS Model

At angular cutoff `L`, let `N=(L+1)^2` and take

```text
M_L = M_N tensor R_III1,
Phi_L = tau_N tensor phi_ITPFI.
```

Here `R_III1` is the hyperfinite product-state factor constructed by the
alternating-gap regulator. Because `tau_N` is tracial,

```text
sigma_t^{Phi_L} = identity tensor sigma_t^{phi}.
```

Therefore the continuous core factorizes exactly:

```text
M_L crossed_{sigma^Phi} R_time
  is canonically isomorphic to
  M_N tensor (R_III1 crossed_{sigma^phi} R_time)
  = M_N tensor C_phi.
```

This is a hyperfinite Type-`II_infinity` factor.

## Conditional Expectations Survive The Core

Let `E` be the finite time, time-then-axial, or full-rotation expectation on the
angular matrix factor. The qualifier matters: axial `U(1)` averaging alone on
the full harmonic space retains cross-`ell` multiplicity blocks, whereas the
composed time-then-axial expectation has diagonal range `C^N`. Each expectation
preserves `tau_N` and commutes with the product modular flow, so on the core it
extends as

```text
E_hat = E tensor identity_{C_phi}.
```

`E_hat` is normal, faithful, trace preserving, and covariant under the dual
clock action. We use the working trace `Tr_N tensor Tr_core`, which differs from
the normalized angular convention `tau_N tensor Tr_core` by the global factor
`N`; densities are normalized consistently, so the stated distances and
relative entropies are unchanged. The crossed-product clock changes each surviving angular block
into a semifinite factor, but it does not recreate a discarded angular matrix
coefficient.

## Recovery And Entropy Obstruction

Choose a nonzero finite-trace core projection `q` and set
`omega=q/Tr(q)`. This common core density has finite entropy. Tensor the
orthogonal phase pair with `omega`. Their input trace distance remains `1`,
while the time-then-axial expected outputs still coincide. Every decoder
through the core screen therefore has worst-case error at least `1/2`.

The relative entropy to the expected state is also unchanged by the common
core tensor factor. For the time-then-axial phase-pair obstruction,

```text
D(rho_+ tensor omega || E_{t,phi}(rho_+) tensor omega) = log 2.
```

For full `SU(2)` orientation loss, a pure state in `V_L` is sent to
`I_{2L+1}/(2L+1)`, so

```text
D(rho tensor omega || E_SU2(rho) tensor omega) = log(2L+1).
```

This replaces the basis-dependent dimension count by a state-weighted,
semifinite-core obstruction. Full orientation loss carries a logarithmically
growing missing-frame entropy, while the selected time-then-axial phase bit
contributes exactly `log 2`.

## Claim Boundary

The bridge is deliberately factorized. The thermal Type-III sector is a
spectator, the angular state is tracial, and no static-patch interaction,
Bunch-Davies derivation, local stress tensor, area term, or generalized-entropy
identity has been supplied. The theorem establishes that the continuous core
does not automatically cure angular-frame incompleteness; it does not yet show
that a gravitational KMS state realizes this tensor structure.

The next gate is an interacting or local-QFT model in which the rotation action
and modular Hamiltonian are derived together. The target comparison is between
the core relative-entropy loss above and a generalized-entropy or observer-
algebra index correction.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy core-edge-obstruction --max-level 8
PYTHONPATH=. python3 -m unittest tests.test_core_edge_obstruction
```
