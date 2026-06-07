# Continuum-Lift Obstruction Theorem

## Claim Boundary

This is a proof-ready obstruction theorem under explicit lift hypotheses. It
does not construct a continuum de Sitter static patch, a dS/CFT dictionary, or
ER=EPR in de Sitter.

## Setup

Let

```text
(A_L^q, A_L^c, S_L, Phi_L)
```

be a pair of finite regulator sequences. Here `A_L^q` is the quantum observer
algebra, `A_L^c` is the dephased abelian control, `S_L` is the screen algebra,
and `Phi_L` denotes the chosen cutoff embedding or coarse-graining data.

Let

```text
Sh_L(A_L)
```

be the declared screen-shadow functor from
`docs/screen_shadow_functor_spec.md`, and let

```text
nu_L(A_L)
```

be the operator-norm response witness from
`docs/response_witness_spec.md`.

## Lift Hypotheses

Assume:

1. **Embedding/coarse-graining:** the finite cutoffs are related by chosen
   maps `Phi_L`.
2. **Trace/state convergence:** the normalized traces or selected states are
   compatible with the maps in the intended limit.
3. **Screen-shadow convergence:** the screen shadows `Sh_L(A_L^q)` and
   `Sh_L(A_L^c)` converge and have the same limit.
4. **Strong-continuity/generator control:** the dynamics obey a gate such as
   `delta_L Gamma_L -> 0`.
5. **Response persistence:** there is an `epsilon > 0` such that

   ```text
   liminf_L |nu_L(A_L^q)-nu_L(A_L^c)| >= epsilon.
   ```

6. **Observer-algebra compatibility:** a complete observer dictionary must
   distinguish limiting algebras that are separated by the response witness.

## Theorem

If a proposed continuum dictionary `D` factors only through the limiting
screen shadow,

```text
D(A) = d(lim_L Sh_L(A_L)),
```

then `D` cannot determine the limiting observer algebra whenever the six lift
hypotheses above hold.

## Proof

By screen-shadow convergence, the quantum regulator sequence and dephased
control have the same limiting screen shadow:

```text
lim_L Sh_L(A_L^q) = lim_L Sh_L(A_L^c).
```

Because `D` factors only through this limiting screen shadow, it assigns the
same output to the two sequences:

```text
D(A^q) = d(lim_L Sh_L(A_L^q))
       = d(lim_L Sh_L(A_L^c))
       = D(A^c).
```

By response persistence, the same two sequences remain separated by an
intrinsic operator response witness:

```text
liminf_L |nu_L(A_L^q)-nu_L(A_L^c)| >= epsilon > 0.
```

By observer-algebra compatibility, response-separated limiting candidates
cannot be identified by a complete observer-algebra dictionary. Therefore a
dictionary that factors only through the limiting screen shadow is incomplete.
QED.

## Finite Persistence Lemma

For the finite benchmark sequence:

```text
A_L^q=M_{N_L},       A_L^c=C^{N_L}.
```

The screen-shadow equality is finite-proved because every declared screen
functional factors through diagonal data. The response separation is
finite-proved in operator norm:

```text
nu(M_N) >= ||[e_12,e_21]|| = 1,       nu(C^N)=0.
```

Under the implemented lift-map audit:

- trace-filled UCP refinement retains the commutator witness in the embedded
  corner;
- harmonic refinement retains the witness in the preserved low-mode corner;
- heat-kernel coarse graining has positive response retention tending to one;
- Berezin-Toeplitz-inspired smoothing has positive response retention tending
  to one for the declared `O(1/N)` surrogate.

This proves bounded finite persistence for the implemented maps. It does not
prove those maps are canonical static-patch embeddings.

## Certificate Map

| Claim | Evidence |
| --- | --- |
| Screen-shadow equality | `docs/screen_shadow_functor_spec.md`; `tests.test_lift_diagnostics` |
| Response witness separation | `docs/response_witness_spec.md`; `tests.test_lift_diagnostics` |
| Lift-map obligations | `docs/lift_map_obligations.md`; `tests.test_embedding_channels` |
| Decision outcome | `docs/continuum_lift_decision_ledger.md`; `finite_lift_decision_record` |
| Conditional obstruction certificate | `PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5` |

## Result Status

The execution branch selects:

```text
A. proof-ready continuum-lift obstruction theorem.
```

The theorem is conditional on lift hypotheses. The current finite package
provides direct finite proofs and bounded certificates for the declared
benchmark maps, while canonical static-patch realization remains an explicit
conditional operator-algebra input.
