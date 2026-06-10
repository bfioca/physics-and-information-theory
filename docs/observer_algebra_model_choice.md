# Observer-Algebra Regulator Model Choice

Status: Phase 0 decision memo

Decision: use the genuine fuzzy-sphere algebra as the Phase 1 geometric
regulator; retain the truncated harmonic Hilbert-space model only as a labeled
control.

## Why A Decision Is Required

The current implementation enumerates `(L+1)^2` spherical harmonics as basis
states and assigns them the full algebra `M_{(L+1)^2}`. It also describes the
dynamics using fuzzy-sphere language. These are two different constructions.

The distinction matters because their symmetries, observable content, natural
refinement maps, and continuum algebra types are different.

## Model A: Genuine Fuzzy Sphere

At level `L`, use

```text
A_L = M_{L+1}.
```

The `(L+1)^2` fuzzy spherical harmonics form an operator basis of `A_L`; they
are not basis states of a Hilbert space of that dimension. `SU(2)` acts by the
adjoint representation, and the fuzzy Laplacian is the superoperator

```text
Delta_L(A) = sum_i [J_i,[J_i,A]].
```

Properties:

- matrix size: `L+1`;
- algebra dimension: `(L+1)^2`;
- harmonic interpretation: operator multipoles;
- exact rotational covariance: natural;
- canonical comparison tools: Berezin symbols, Toeplitz quantization, and
  equivariant CP maps;
- natural limit: the quantized sphere in a strict-deformation or quantum-metric
  sense, not automatically a Type-`II_1` factor.

This model fits the repository's intended geometric-screen interpretation.

## Model B: Truncated Harmonic Hilbert Space

Let

```text
H_L = direct_sum_{ell=0}^L V_ell,
A_L = B(H_L) = M_{(L+1)^2}.
```

Here the harmonics are one-particle state labels. The ordinary Hamiltonian can
have spectrum `ell(ell+1)`, and the current diagonal dephasing formulas fit
this interpretation more naturally.

Properties:

- Hilbert-space dimension: `(L+1)^2`;
- algebra dimension: `(L+1)^4`;
- harmonic interpretation: one-particle modes;
- canonical Hilbert inclusions: `H_L` is a subspace of `H_{L+1}`;
- induced algebra comparison: corner embeddings, which are nonunital;
- natural limit: `B(L^2(S^2))`, hence Type `I_infinity` under the straightforward
  construction.

This is a valid spectral-cutoff field or particle model, but it should not be
called the fuzzy-sphere algebra.

## Comparison

| Feature | Genuine fuzzy sphere | Truncated harmonic space |
| --- | --- | --- |
| Finite algebra | `M_{L+1}` | `M_{(L+1)^2}` |
| Role of `Y_lm` | operator basis | state basis |
| Laplacian | adjoint double commutator | one-particle Hamiltonian |
| Natural symmetry | adjoint `SU(2)` | direct-sum `SU(2)` on states |
| Natural limit | quantized `C(S^2)` | Type-I algebra on `L^2(S^2)` |
| Best role here | geometric horizon regulator | control model |

## Consequences For Existing Claims

1. The factorial UHF construction is not the natural limit of either model.
   A Type-II observer algebra must arise from constraints, modular/crossed-
   product structure, or an explicit observer construction.
2. The current axis-dependent `m` splitting breaks exact rotational symmetry.
   It cannot enter the primary model without a derived physical source.
3. In Model A, the Laplacian acts on operators. Existing Schur coefficients
   cannot simply be relabeled as fuzzy-sphere dynamics.
4. In Model B, the straightforward continuum algebra is Type I. Factorial
   amplification does not change the physical origin of that model.

## Phase 1 Decision

Implement Model A first:

- fuzzy harmonics as matrices in `M_{L+1}`;
- adjoint `SU(2)` action and fuzzy Laplacian;
- normalized trace and a declared state family;
- Berezin symbol and quantization maps;
- a physical screen observable system expressed as an operator system or
  subalgebra, not as basis-diagonal data by default.

Retain Model B as a control benchmark under an explicit name such as
`truncated_one_particle_sphere`. Its purpose is to check whether a claimed
effect depends only on spectral truncation rather than noncommutative screen
geometry.

## Type-II Boundary

No Phase 1 result may call its limit Type II merely because a separate UHF
amplification has the hyperfinite Type-`II_1` factor as its tracial closure.
The algebra type must be derived from the observer/gravitational construction.
