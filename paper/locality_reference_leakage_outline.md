# Leakage From Spacelike Replication Of Finite SO(3) Collective Modes

Status: conditional manuscript outline for a bounded mathematical-physics
paper. The state-weighted theorem and robust extension are proved for bounded
finite code compressions, and the distributed identities have finite-matrix
checks. A specialist priority check remains an external submission gate. An
unbounded/AQFT extension is optional future work, not a premise of this paper.

## Candidate Abstract

We consider a finite rotational reference modeled by projecting a distributed
system onto a rigid collective band. We show that microscopic
locality constrains this truncation. If different spacelike cells reproduce
different components of the same finite `SO(3)` collective generator, their
logical noncommutativity must be mediated by excursions outside the collective
band. For bounded cell observables `A_a`, code projector `P`, `Q=1-P`, and a
certified off-band cap `Lambda=max_a||Q A_a P||`, we derive operator-norm and
state-weighted inequalities with explicit errors. In the exact three-cell
case,

```text
sum_a Tr[rho P A_a Q A_a P]
 >=alpha^4 Tr(rho J^2)/(4Lambda^2).
```

Combining this with a global Haar-prior orientation-risk theorem yields an
operational lower bound
`alpha^4[R_ref^(-1)-8]_+/(64Lambda^2)`, nontrivial for
`R_ref<1/8`. With local norm `M`, the fixed dimensionless calibration is
`g=|alpha|/M`; weakening `g` is an explicit escape route. Disjoint-block
ferromagnetic spin codes asymptotically saturate the underlying pairwise norm
constant and realize the state-weighted scaling within a factor tending to
eight. The result is a collective-mode truncation theorem, not a no-go for
local non-Abelian currents, and it supplies neither dynamics nor a lifetime.

## Main Result

**Theorem 1 (state-weighted spacelike-replication leakage).** Let
`O -> A(O)` be a local net, let `O_1,O_2,O_3` be pairwise spacelike regions,
and let `A_a in A(O_a)` be bounded self-adjoint observables. Let `P` be a
finite-rank code projector carrying a nontrivial integer-spin representation
of `SO(3)`, and put `Q=1-P`. Assume

```text
P A_a P=alpha J_a,
||Q A_a P||<=Lambda,        0<Lambda<=M,
||A_a||<=M.
```

Then every code state `rho=P rho P` obeys

```text
sum_a Tr[rho P A_a(I-P)A_aP]
 >=alpha^4 Tr(rho J^2)/(4Lambda^2)
 >=alpha^4 Tr(rho J^2)/(4M^2).
```

The paper also states the pairwise approximate theorem and the uniform robust
three-axis corollary with locality defect `delta`, compression error `epsilon`,
maximum spin `J`, and Young parameter `t`.

**Corollary 2 (operational orientation risk).** For the full-frame Haar-prior
chordal task and `0<r<1/8`, any state and measurement achieving `R_ref<=r`
satisfy

```text
sum_a Tr[rho P A_a(I-P)A_aP]
 >=alpha^4 [r^(-1)-8]_+/(64Lambda^2).
```

**Proposition 3 (distributed realizations).** The symmetric ground band of an
even-site ferromagnetic spin chain, probed by gain-normalized spin components on
two disjoint macroscopic blocks, has exact collective compression and pairwise
norm ratio

```text
2 lambda_X lambda_Y/||J_z||=N/(N-1).
```

A fixed-width buffer preserves asymptotic saturation. Three equal disjoint
blocks reproduce `J_x,J_y,J_z`, have `sum_a p_a=N`, and approach an
actual-to-Theorem-1 lower-bound ratio of eight. The latter establishes
constant-factor scaling, not optimality of Theorem 1's factor four.

## Section Plan

### 1. Question And Claim Boundary

- Define a rigid collective truncation and why a global projector can turn
  commuting microscopic observables into noncommuting logical ones.
- State immediately that different components in one local region need not
  commute.
- Separate absolute fixed-gain leakage from relative leakage.
- List nonclaims: no generic non-Abelian-current no-go, QFT continuum,
  lifetime, or gravity.

### 2. Local Algebras, Codes, And Error Ledger

- Hilbert space, finite code `P`, complement `Q`.
- Pairwise commuting bounded algebras for spacelike cells.
- Local-net formulation and the commuting-cell version used by the lattice
  model.
- Incoming and outgoing leakage amplitudes.
- Uniform compressed-action errors and locality defects.
- Stability under arbitrary spectator ancillas.

### 3. Compression Lemma And Optimal Constant

- Prove `[PAP,PBP]=P[A,B]P+PBQAP-PAQBP`.
- Derive the directed and self-adjoint norm bounds.
- Use the disjoint-block ferromagnet to prove the coefficient `2` is
  asymptotically optimal.
- Label the lemma as standard compression machinery and compare it with
  Toeplitz/Hankel and approximate-QEC precedents.

### 4. State-Weighted Collective-Mode Theorem

- Introduce `p_a(rho)=||Q A_a P rho^(1/2)||_2^2`.
- Prove the pairwise RMS inequality by Hilbert-Schmidt Cauchy-Schwarz.
- Sum the cyclic `SO(3)` brackets to obtain the direct factor-four theorem.
- Prove the approximate `delta,epsilon,t` version.
- Derive the cap consistency law `Lambda^4>=alpha^4 Tr(rho J^2)/12`.
- Explain why state-weighted leakage is stronger than a worst-case norm alone
  but is not yet a dynamical probability.

### 5. Global Orientation-Risk Corollary

- State the full-frame Haar-prior chordal task.
- Reproduce the spin-1 fusion/discrete-Hardy proof of the tail-robust Casimir
  inequality, or cite a published theorem with the identical task and
  constant.
- Derive the risk-conditioned leakage bound.
- Compare the mean-Casimir and strict-cutoff resource statements.
- Check non-vacuity using `R_ref>=sin^2[pi/(2J_max+3)]` and
  `|alpha|J_max<=M+epsilon`.
- Audit stabilizers, rare high-spin tails, mixed states, and invariant
  multiplicities.

### 6. Disjoint-Block Ferromagnetic Models

- Define the frustration-free nearest-neighbor Hamiltonian and symmetric code.
- Derive exact block compression by permutation symmetry.
- Compute the complete leakage singular-value formula.
- Show asymptotic saturation with and without a fixed-width buffer.
- Compute the three-cell state weights and constant-factor ratio for the main
  theorem.
- Plot absolute leakage `Theta(sqrt(N))`, operator norm `Theta(N)`, and relative
  leakage `Theta(N^(-1/2))`.

### 7. Relation To Existing No-Go Theorems

- Toeplitz/Berezin projection-induced noncommutativity.
- Eastin-Knill and approximate covariant-code bounds.
- Harlow-Ooguri splittability and code-preservation logic.
- Quantum reference-frame accuracy/size inequalities.
- State precisely what the present risk-conditioned cell-replication theorem
  adds, if specialist review agrees.

### 8. Physical Meaning And Escape Routes

- Co-locate noncommuting components inside one region.
- Let local factors leave the collective band.
- Weaken the gain as the code spin grows.
- Use distributed modes rather than a rigid finite band.
- Replace bounded observables by a controlled affiliated-operator theorem.

### 9. Discussion

- The theorem diagnoses a truncation cost, not fundamental failure of local
  non-Abelian symmetry.
- A lifetime theorem would need a Hamiltonian and a normalized interaction.
- Continuum AQFT is a separate mathematical extension.

## Figures And Tables

1. Diagram of three spacelike cells, global code `P`, and `Q` excursions.
2. Ferromagnetic chain split into `X`, buffer, and `Y`.
3. Log-log plot of absolute and relative leakage and the three-cell theorem
   ratio versus `N`.
4. Claim comparison table: Toeplitz, Eastin-Knill, covariant QEC, and this
   theorem.

## Submission Gate

The draft is a submission candidate only after:

- an independent operator-algebra/QEC proof audit;
- a specialist novelty review of the state-weighted theorem;
- explicit finite-matrix verification of the ferromagnetic formulas;
- a parameter-by-parameter comparison with approximate covariant-QEC and
  local recovery bounds;
- removal of all de Sitter, gravity, Skyrmion, and Paper U dependencies from
  the title, abstract, and main theorem.

The internal proof audit and finite-matrix gate are complete in the current
research branch. Specialist novelty review is not complete and cannot be
replaced by an arXiv search.

If the specialist novelty review identifies (3.1) and its risk composition as
a standard corollary, freeze this as a repository methods note and do not
submit it as a new theorem paper.
