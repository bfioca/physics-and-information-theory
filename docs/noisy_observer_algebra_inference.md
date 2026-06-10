# Noisy Observer-Algebra Inference On The Coherent Screen

Status: finite candidate-atlas theorem implemented

## Question

At fuzzy-sphere level `L`, suppose an unknown channel acts on
`A_L=M_{L+1}` before the canonical coherent-state POVM is measured. Can a
small, physically explicit probe family identify the algebra of observables
preserved by that channel under bounded statistical error?

This note answers that question for a declared three-model atlas. It does not
claim to learn an arbitrary quantum channel or an arbitrary Wedderburn algebra.

## Candidate Atlas

The candidates are:

| Channel | Action | Maximal exact OA-QEC algebra on the full input code |
| --- | --- | --- |
| full | `N(A)=A` | `M_{L+1}` |
| `J_z` dephasing | delete off-diagonal matrix entries | diagonal `C^{L+1}` |
| depolarizing | `N(A)=Tr(A) I/(L+1)` | scalar `C I` |

The algebra statement follows from the standard OA-QEC commutant condition:
the correctable algebra commutes with all Kraus products `E_a^*E_b`. For the
three channels these products generate respectively the scalars, the diagonal
algebra, and the full matrix algebra. The identity map on the output therefore
recovers the corresponding fixed algebra exactly. This recovery statement is
separate from coherent-screen tomography; a one-copy classical screen record
does not recover an arbitrary noncommutative state.

## Probe Design

Use two binary state pairs:

```text
population: |north><north| versus |south><south|,
population: rho_z,+ versus rho_z,-,
coherence:  rho_x,+ versus rho_x,-,
```

where

```text
rho_a,+/- = (I +/- J_a/j)/(L+1),  j=L/2.
```

These are positive mixed states generated entirely by the `ell=0,1` operator
system. The `z` pair survives `J_z` dephasing, the `x` pair does not, and
depolarization erases both. This replaces the earlier rank-one pole and cat
probes, whose cutoff dependence was unsuitable for a continuum theorem.

The classical witnesses are the bounded coordinate functions `n_z` and `n_x`
on the coherent screen. Quadrature is exact for the required second moments,
so both full-channel responses equal

```text
R_L = 1/3.
```

The ideal signatures are

```text
full:         (R_population, R_coherence),
dephasing:    (R_population, 0),
depolarizing: (0, 0),
```

The separation is exactly `1/3` at every cutoff. Consequently the certified
sample count is cutoff independent.

## Cutoff Transport

The coordinate probe family and witness are canonical across cutoffs. Writing
`Y_a^L=J_a/j`, the Berezin map sends

```text
J_{L->M}(Y_a^L) = M/(M+2) Y_a^M.
```

The screen witness operator is `W_a^L=L/(L+2)Y_a^L`. Its normalized
Hilbert-Schmidt transport error is at most

```text
2/(sqrt(3)(L+2)),
```

The local response remains exactly `1/3`. Under the canonical CPTP state lift,
the target response is `M/[3(M+2)]`, within `2/[3(M+2)]` of the local value.
Thus both the diagnostic and its nonzero separation survive the canonical
large-cutoff system.

## Robust Identification Theorem

Let `s_c` be the two-response signature of candidate `c`, and define

```text
Delta_L = min_{c != c'} ||s_c-s_c'||_infinity.
```

If an observed signature is known coordinatewise within error `epsilon` of the
true signature and

```text
epsilon < Delta_L/2,
```

then its closed `epsilon` feasibility box contains exactly one candidate. The
classifier returns that candidate. If feasibility boxes overlap or no candidate
is feasible, it returns `ambiguous` rather than silently extrapolating beyond
the theorem.

For `n` independent samples from each of the four probe states, every witness
sample lies in `[-1,1]`. Hoeffding plus a union bound over four sample means gives

```text
Pr[max response error > epsilon] <= 8 exp(-n epsilon^2/2).
```

Thus it suffices to take

```text
n >= (2/epsilon^2) log(8/delta)
```

samples per state for failure probability at most `delta`.

## Research Use

This benchmark closes the first inverse-problem loop on the canonical screen:
physical probes, explicit statistics, robust model selection, sample
complexity, and exact recovery on the selected algebra all appear in one
calculation. Its limitation is equally important. The theorem assumes the
candidate atlas, so the next step is to replace three isolated channels by a
parameterized family of covariant conditional expectations or noisy
Wedderburn decompositions and prove stability under channel misspecification.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy fuzzy-algebra-inference --max-level 6
PYTHONPATH=. python3 -m unittest tests.test_fuzzy_algebra_inference
```
