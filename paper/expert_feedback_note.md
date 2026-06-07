# Expert Feedback Note: Finite Static-Patch Observer-Algebra Diagnostics

## One-Paragraph Summary

We built a finite executable benchmark for a static-patch observer-algebra
question: do screen-visible data determine the observer algebra? In the finite
model, a quantum regulator with observer algebra `M_N` and a dephased abelian
control with algebra `C^N` have identical diagonal/screen shadows, while
intrinsic operator response distinguishes them by the commutator witness
`[e_12,e_21]=e_11-e_22`. The benchmark includes finite derived dynamics,
strong-continuity gates, a conditional Type-`II_1` scaffold, and an approximate
consecutive-cutoff embedding audit comparing a trace-filled UCP baseline with
harmonic, heat-kernel, and Berezin-Toeplitz-inspired refinements. The result is
not a continuum de Sitter theorem. The purpose of this note is to ask which
cutoff embedding or coarse-graining should be considered physically natural for
static-patch observer algebras.

## What Is Claimed

The finite claim is:

```text
screen-shadow diagnostics do not determine finite observer algebras;
operator-response, continuity, and embedding data are necessary extra data.
```

The benchmark compares:

```text
A_L = M_N,      S_L = C^N,      D_L = C^N.
```

Here `S_L` is the diagonal screen algebra and `D_L` is the dephased control.
Any diagnostic that factors only through the diagonal screen data agrees
between `A_L` and `D_L`. The algebras differ because `M_N` has nonzero
commutators and `C^N` does not.

## Theorem Stack

**Screen-shadow collision.** For diagnostics that factor through the diagonal
screen map, the quantum and dephased controls have identical shadows. The
operator-response witness separates them:

```text
||[e_12,e_21]|| = 1 in M_N,       ||[x,y]|| = 0 in C^N.
```

**Strong-continuity gate.** If `Lambda_L(delta)=exp(delta G_L)`,
`||G_L|| <= Gamma_L`, and `delta_L Gamma_L -> 0`, then

```text
||Lambda_L(delta_L)-I|| <= exp(delta_L Gamma_L)-1 -> 0.
```

This excludes instantaneous dephasing without assuming off-diagonal survival.

**Finite-to-Type-`II_1` scaffold.** Exact full-matrix inclusions fail at
consecutive spherical cutoffs `N_L=(L+1)^2`, but a cofinal factorial subsequence
admits trace-preserving inclusions. The quantum path gives a UHF algebra whose
tracial closure is the hyperfinite Type `II_1` factor by standard operator
algebra facts; the dephased path has the same screen shadows and an abelian
limit. This is a scaffold, not a canonical de Sitter static patch.

**Approximate consecutive refinement.** The exact-inclusion obstruction can be
softened by replacing `*-inclusions` with UCP trace-preserving maps. The
baseline map is: for
`n <= m`,

```text
Phi(A)=V A V^* + tau_n(A)(I_m - V V^*)
```

is unital, completely positive, and normalized-trace preserving. It is not
multiplicative, but for `A=e_12`, `B=e_21`,

```text
||Phi(AB)-Phi(A)Phi(B)|| = 1/n.
```

Thus consecutive spherical cutoffs can be related with vanishing
multiplicativity error `1/N_L`.

The current audit also tests three more structured finite maps: harmonic
mode-label refinement, harmonic refinement followed by heat-kernel Schur
coarse graining, and a Berezin-Toeplitz-inspired CP smoothing surrogate. These
are not claimed canonical, but they show the obstruction is not only an
artifact of the factorial-subsequence scaffold.

**Conditional continuum-lift obstruction.** If finite regulator sequences lift
to a continuum/static-patch setting while screen shadows converge and a
response witness remains separated, then any dictionary that factors only
through screen shadows is incomplete.

## What Is Not Claimed

We do not claim:

- a continuum de Sitter observer-algebra theorem;
- a dS/CFT dictionary;
- literal ER=EPR in de Sitter;
- that the factorial subsequence is physically canonical;
- that the trace-filled UCP map is the correct fuzzy-sphere/static-patch
  refinement;
- approximate QEC stability in a Type-II or Type-III limit.

## Feedback Question

The current finite package isolates the remaining load-bearing physics choice:

```text
Is the cutoff embedding/coarse-graining problem physically meaningful here, or
is this just a finite restatement of known diagonal forgetfulness?
```

Candidates include:

- angular-momentum branching or mode-label refinement;
- coherent-state or Berezin-Toeplitz symbol/quantization maps;
- heat-kernel coarse graining;
- continuum `L^2(S^2)` projection maps;
- approximate UCP embeddings rather than exact full-matrix inclusions;
- a modular/KMS-based conditional expectation intrinsic to the observer
  algebra.

The concrete question is whether cutoff-compatible strong continuity plus
conditional-expectation covariance is the right finite shadow of static-patch
observer dynamics, or whether a different operator-algebraic axiom should be
used.

## Minimal Reproduction

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics tests.test_embedding_channels tests.test_continuum_lift_obstruction
```

The paper-shaped note is:

```text
paper/main.md
```
