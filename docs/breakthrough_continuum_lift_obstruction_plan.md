# Breakthrough Plan: Continuum-Lift Obstruction for Static-Patch Observer Algebras

## Purpose

This branch turns the current finite benchmark package into a theorem-search
program aimed at one external-facing target:

```text
Under explicit finite-to-continuum lift conditions, a dictionary that factors
only through screen-visible data cannot determine the limiting observer algebra
whenever an intrinsic noncommutative response witness persists.
```

This is not a plan to claim de Sitter ER=EPR, construct dS/CFT, or identify the
continuum static patch. The intended breakthrough is a rigorous obstruction
theorem for screen-only static-patch or dS/CFT-like dictionaries.

## North Star

The strongest paper-worthy claim would be:

```text
Horizon/screen data are not enough. Any viable static-patch observer
dictionary must include noncommutative operator-response data, provided the
finite regulator sequence satisfies precise lift conditions.
```

The existing finite package already supplies the engine:

- quantum observer algebra `M_N`;
- dephased abelian control `C^N`;
- matching declared screen shadows;
- separating commutator/off-diagonal response;
- cutoff-compatible strong-continuity gate;
- finite-to-Type-`II_1` scaffold;
- approximate consecutive-cutoff UCP refinements.

The new work is to prove that this engine either lifts, fails to lift for a
specific mathematical reason, or needs one additional assumption.

## Branch Acceptance Criteria

A successful branch must produce one of:

- **A. Theorem candidate:** a human-proof-ready continuum-lift obstruction
  theorem with explicit hypotheses and certificate-backed finite assumptions.
- **B. No-go:** a rigorous obstruction showing which lift condition fails for
  the current regulator/embedding class.
- **C. Weakest-added-assumption result:** a precise additional
  embedding/state/modular assumption that turns the current schema into a
  theorem candidate.

Do not add new toy examples unless they decide one of these three outcomes.

For the smaller step-by-step execution surface, use
`docs/continuum_lift_obstruction_execution_goal.md`.

## Phase 1: Formalize the Objects

### 1.1 Screen-Shadow Functor

Convert "screen-visible diagnostics" from a checklist into a mathematical
object:

```text
Sh_L(A_L, rho_L, Lambda_L)
```

The functor should include exactly the declared screen-accessible data:

- diagonal observables through `E_diag`;
- low-order diagonal correlators;
- finite horizon-overlap data;
- screen-restricted transfer records;
- any screen-shadow quantities already emitted by the certificate suite.

Deliverables:

- `docs/screen_shadow_functor_spec.md`;
- optional `qgtoy/screen_shadow_functor.py` if code structure needs it;
- tests proving `Sh_L(M_N)=Sh_L(C^N)` for all declared finite levels;
- theorem text replacing informal "these diagnostics fail" language with
  "all functionals in the declared screen-shadow class agree."

Proof obligation:

```text
If a diagnostic factors through the declared diagonal/screen data, then it is
invariant under replacing M_N by the dephased C^N control with matched screen
data.
```

### 1.2 Intrinsic Response Witness

Replace one-off matrix-unit language with a stable noncommutativity witness.
Candidate:

```text
nu(A_L) = sup { ||[a,b]|| : ||a|| <= 1, ||b|| <= 1, a,b in visible algebra }.
```

For `M_N`, `nu` is bounded below by the normalized matrix-unit witness. For
`C^N`, `nu=0`.

Deliverables:

- `docs/response_witness_spec.md`;
- code helper for response lower bounds if useful;
- proof that the witness is invariant under the allowed finite equivalences;
- explicit topology choice for persistence in a lift: norm, `L^2` trace norm,
  strong operator, or a named certificate topology.

Proof obligation:

```text
The witness must not vanish in the proposed large-cutoff topology, or the
branch must report a no-go.
```

## Phase 2: Replace Engineered Inclusions With Lift Maps

The current exact factorial inclusion is mathematically useful but physically
suspicious. This phase tests whether consecutive approximate embeddings can
carry the theorem.

Embedding classes to analyze:

- trace-filled UCP refinement:

  ```text
  Phi(A)=V A V^* + tau_n(A)(I_m - V V^*)
  ```

- spherical-harmonic projection/refinement using `(ell,m)` mode labels;
- harmonic refinement followed by heat-kernel Schur coarse graining;
- Berezin-Toeplitz/fuzzy-sphere symbol-quantization channel, if it can be
  implemented or stated as a conditional theorem hypothesis.

For each embedding class, audit:

- unitality and complete positivity;
- trace/state compatibility;
- approximate multiplicativity on low modes;
- approximate covariance with static-patch dynamics;
- screen-shadow convergence;
- strong-continuity compatibility;
- response-witness persistence.

Deliverables:

- `docs/lift_map_obligations.md`;
- updated `docs/canonical_embedding_program.md` with theorem/no-go status;
- updated `qgtoy/embedding_channels.py` only if new certified quantities are
  needed;
- direct tests for each listed condition, not only self-declared certificate
  booleans.

Kill criteria:

- every physically motivated approximate embedding kills the response witness;
- the only working maps are rank-ordered or factorial tricks;
- the screen-shadow class cannot be defined without becoming ad hoc.

## Phase 3: Prove the Abstract Lift Obstruction

State the theorem independently of the implementation.

Theorem shape:

```text
Let (A_L^q, A_L^c, S_L, Phi_L) be quantum and dephased finite regulator
sequences with:

1. embedding/coarse-graining maps between cutoffs;
2. trace/state convergence;
3. screen-shadow convergence;
4. cutoff-compatible strong continuity or generator control;
5. persistence of an intrinsic response witness;
6. compatibility with proposed limiting observer algebras.

If lim Sh_L(A_L^q) = lim Sh_L(A_L^c), but the limiting response witnesses
differ, then no dictionary factoring only through lim Sh_L can determine the
observer algebra.
```

Deliverables:

- `docs/continuum_lift_obstruction_theorem.md`;
- updated `paper/main.md` theorem section only after the theorem is
  proof-ready;
- updated certificate index mapping each lift condition to a command or to a
  clearly marked conditional assumption.

Proof obligation:

```text
The proof must be a dictionary-factorization argument plus a real persistence
lemma, not merely "diagonal data miss off-diagonal data."
```

## Phase 4: Type-II and Static-Patch Interpretation

Use Type-II language only as a motivated limit layer.

Deliverables:

- precise statement of what is standard UHF/trace-closure input;
- precise statement of what is conditional static-patch interpretation;
- optional no-go if the response witness does not survive the tracial GNS or
  proposed Type-`II_1` topology;
- expert-facing note focused on the canonical cutoff/coarse-graining question.

Allowed claim:

```text
This is a finite regulator obstruction for screen-only dictionaries, formulated
in the language suggested by static-patch observer algebras.
```

Forbidden claim:

```text
This constructs the continuum de Sitter observer algebra or proves ER=EPR in
de Sitter.
```

## Work Breakdown

| Workstream | First Artifact | Done When |
| --- | --- | --- |
| Screen functor | `docs/screen_shadow_functor_spec.md` | all declared screen diagnostics factor through the same formal object |
| Response witness | `docs/response_witness_spec.md` | a norm/topology-stated witness separates `M_N` from `C^N` and has a persistence criterion |
| Embedding maps | `docs/lift_map_obligations.md` | every candidate map has CP/unitality/trace/multiplicativity/covariance/screen/response status |
| Lift theorem | `docs/continuum_lift_obstruction_theorem.md` | theorem has assumptions, proof, and no hidden continuum claim |
| Code certificates | updated `qgtoy/` modules and tests | direct tests verify the finite hypotheses used in the theorem |
| Paper package | updated `paper/main.md` / `paper/main.tex` | only after the theorem/no-go is stable |

## First Concrete Sprint

1. Create `docs/screen_shadow_functor_spec.md` and formalize `Sh_L`.
2. Create `docs/response_witness_spec.md` and choose a persistence topology.
3. Add direct tests showing current finite certificates imply:
   - screen-shadow equality;
   - response-witness separation;
   - response lower bound under implemented embedding maps.
4. Decide whether the current heat/Berezin surrogate is enough for a theorem
   candidate or only a bounded certificate.
5. Emit a theorem-obligation ledger with each assumption marked:
   - proved finite theorem;
   - bounded certificate;
   - conditional operator-algebra input;
   - open physics assumption.

## Suggested Verification Commands

Current package baseline:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics tests.test_embedding_channels tests.test_continuum_lift_obstruction tests.test_lift_diagnostics
```

Embedding certificates:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-embedding-channels --max-cutoff 5
PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5
```

## Stop Conditions

Stop and report a no-go if:

- the response witness vanishes under every non-engineered approximate
  embedding;
- the lift theorem cannot be stated without baking in the answer;
- the only proof is the tautology that diagonal maps forget off-diagonals;
- Type-II language remains only analogy with no compatible topology;
- the screen-shadow functor is not stable under the declared cutoff maps.

## External-Facing Summary

If the branch succeeds, the expert-facing message should be:

```text
We turned the finite static-patch benchmark into a continuum-lift obstruction
program. The theorem target is not a dS/CFT construction; it is a necessary
condition for one. Under explicit lift conditions, screen-only dictionaries
cannot determine observer algebras when noncommutative response survives.
The remaining mathematical question is which cutoff/coarse-graining maps are
canonical enough for static-patch observer algebras.
```
