# Theorem Note: Off-Code Leakage From Spacelike SO(3) Replication

Technical status: **proved for bounded commuting-cell observables**, with a
microcausal corollary for bounded observables in a local net.

Publication status: **internal methods lemma; standalone novelty stopped.**
Janssens' CP-map covariance Cauchy-Schwarz lemma implies the state-weighted
pair bound directly, and cyclic summation gives the three-cell theorem. The
exact reduction is recorded in `spacelike_replication_qec_reduction_audit.md`.

## 1. Domain And Quantifiers

Let `O -> A(O)` be a local net of represented observable algebras on a Hilbert
space `H`: if `O_1` and `O_2` are spacelike separated, then
`[A(O_1),A(O_2)]=0`. The algebraic theorem only needs pairwise commuting
unital star-algebras, so it also applies to finite lattice cells without an
AQFT interpretation.

Let `P` be a finite-rank orthogonal code projector and `Q=I-P`. The code
`C=P H` carries a nontrivial finite-dimensional integer-spin representation of
`SO(3)`, possibly with rotation-trivial multiplicities, with self-adjoint
generators `J_a`, Casimir `J^2=sum_a J_a^2`, and largest spin `J_max`. All
operator norms below are full operator norms on the displayed domain.

For two bounded microscopic observables `A,B`, define

```text
A_C=PAP|_C,                 B_C=PBP|_C,
lambda_A^out=||QAP||,       lambda_A^in=||PAQ||,
lambda_B^out=||QBP||,       lambda_B^in=||PBQ||.       (1.1)
```

The code-visible locality defect is `delta=||P[A,B]P||`; the stronger bound
`||[A,B]||<=delta` is sufficient. Exact spacelike locality gives `delta=0`.
For real gains `alpha,beta`, we allow uniform collective-action errors

```text
||A_C-alpha J_a||<=epsilon_A,
||B_C-beta  J_b||<=epsilon_B.                          (1.2)
```

The gains `alpha,beta` are physical calibration data. Without a fixed gain,
rescaling the microscopic observables rescales every absolute leakage norm and
no scale-free operational statement is possible.

## 2. Compression Lemma

Inserting `I=P+Q` gives the exact identity

```text
[PAP,PBP]=P[A,B]P+PBQAP-PAQBP.                        (2.1)
```

Therefore

```text
||[PAP,PBP]||
 <=delta+lambda_B^in lambda_A^out
        +lambda_A^in lambda_B^out.                    (2.2)
```

For self-adjoint `A,B`, the incoming and outgoing amplitudes agree, so

```text
||[PAP,PBP]||<=delta+2 lambda_A lambda_B.              (2.3)
```

If the target actions in (1.2) are used, commutator perturbation gives

```text
|alpha beta| ||[J_a,J_b]||
 <=delta+2 lambda_A lambda_B
   +2|beta| ||J_b|| epsilon_A
   +2|alpha| ||J_a|| epsilon_B
   +2 epsilon_A epsilon_B.                            (2.4)
```

For distinct Cartesian generators, `||[J_a,J_b]||=J_max`. Thus a nonzero target
bracket forces at least one of microscopic locality defect, collective-action
error, or off-code coupling. The coefficient `2` is optimal; Section 5 gives a
distributed family approaching equality.

Equation (2.1) is not presented as a new theorem. It is the compression
mechanism underlying Toeplitz/Hankel commutators, projected coordinates, and
continuous-symmetry code obstructions.

## 3. State-Weighted Three-Cell Theorem

The stronger result uses three pairwise spacelike regions `O_a`. Let
`A_a in A(O_a)` be bounded self-adjoint observables, let `alpha in R`, and set
`lambda_*=max_a ||Q A_a P||`. Assume

```text
[A_a,A_b]=0                    for a!=b,
P A_a P=alpha J_a,
lambda_*<=Lambda,              0<Lambda<=M,
||A_a||<=M.                                             (3.1)
```

For any density operator `rho=P rho P`, define the state-weighted off-code
quadratic weights

```text
p_a(rho)=Tr[rho P A_a Q A_a P]
        =||Q A_a P rho^(1/2)||_2^2.                    (3.2)
```

These are state-dependent squared off-code amplitudes. They are not
transition probabilities because the `A_a` have not been normalized as Kraus
operators or embedded in a time evolution.

The cap `Lambda` must be proved independently; it is not freely tunable. The
coarse choice `Lambda=M` is always valid.

For a cyclic triple `(a,b,c)`, exact locality and (2.1) give

```text
i alpha^2 J_c
 =P A_b Q A_a P-P A_a Q A_b P.                        (3.3)
```

Right-multiplying by `rho^(1/2)` and using Hilbert-Schmidt
Cauchy-Schwarz gives

```text
|alpha|^2 sqrt[Tr(rho J_c^2)]
 <=lambda_b sqrt(p_a)+lambda_a sqrt(p_b)
 <=Lambda[sqrt(p_a)+sqrt(p_b)],                        (3.4)
```

where `lambda_a=||Q A_a P||=||P A_a Q||`. Squaring,
using `(x+y)^2<=2(x^2+y^2)`, and summing the three cyclic pairs proves

```text
alpha^4 Tr(rho J^2)<=4Lambda^2 sum_a p_a(rho).         (3.5)
```

Hence the spacelike-replication collective-mode leakage theorem is

```text
sum_a p_a(rho)
 >=alpha^4 Tr(rho J^2)/(4Lambda^2)
 >=alpha^4 Tr(rho J^2)/(4M^2).                         (3.6)
```

The theorem is class-uniform over the ambient Hilbert space, finite code, code
state, and bounded realizations satisfying (3.1). For a finite-dimensional
rotation-trivial spectator `K`, tensoring `P,A_a,J_a` with `I_K` preserves the
operator norms. For an arbitrary joint code-spectator state, each weight is
computed from its reduced code state and obeys the same inequality.

The elementary upper bound `p_a<=Lambda^2` also gives

```text
sum_a p_a<=3Lambda^2,
Lambda^4>=alpha^4 Tr(rho J^2)/12.                      (3.7)
```

Thus an inconsistent claimed cap is detected by the theorem itself. The
factor four in (3.6) is the direct proof constant; no optimality claim is made
for the three-cell state-weighted inequality.

In UCP-map language, with `T(X)=W*XW`, the operators
`W*A_a Q A_aW` are standard Schwarz-defect or added-noise operators.
Janssens' CP covariance Cauchy-Schwarz lemma gives (3.4) pair by pair. The
direct proof is retained because it makes the code and locality variables
transparent, not because the inequality is claimed as new.

### Approximate Version

Suppose instead that every pair has locality defect at most `delta`, with
`alpha in R`, and

```text
||P A_a P-alpha J_a||<=epsilon,
||Q A_a P||<=Lambda.                                  (3.8)
```

For code spins through `J_max`, define

```text
eta=4|alpha|J_max epsilon+2epsilon^2,
d=delta+eta.                                           (3.9)
```

The pairwise state bound becomes

```text
|alpha|^2 sqrt[Tr(rho J_c^2)]
 <=Lambda[sqrt(p_a)+sqrt(p_b)]+d.                     (3.10)
```

For every `t>0`, Young's inequality gives the explicit robust consequence

```text
sum_a p_a(rho)
 >=[alpha^4 Tr(rho J^2)-3(1+1/t)d^2]_+
   /[4(1+t)Lambda^2].                                 (3.11)
```

Together with `sum_a p_a<=3Lambda^2`, this also implies

```text
Lambda^4
 >=[alpha^4 Tr(rho J^2)-3(1+1/t)d^2]_+
   /[12(1+t)].                                        (3.12)
```

When `delta=epsilon=0`, the direct proof (3.6), not the `t -> 0` limit of
(3.11), supplies factor four without the Young-inequality loss. The
`J_max` in (3.9) is the actual maximum code spin, not a lower support estimate
inferred from orientation risk.

## 4. Operational Orientation Corollary

For the Haar-prior full-frame task with chordal cost
`c(g,g_hat)=sin^2[theta(g_hat^(-1)g)/2]`, Research Theorem W3 proves

```text
R_ref>=1/[16 Tr(rho J^2)+8].                           (4.1)
```

Therefore any protocol that actually attains `R_ref<=r` must have

```text
Tr(rho J^2)>=[r^(-1)-8]_+/16=:C_req(r).                (4.2)
```

For `r>0`, combining (3.5) and (4.2) gives

```text
sum_a p_a(rho)
 >=alpha^4 [r^(-1)-8]_+/(64Lambda^2)
 >=alpha^4 [r^(-1)-8]_+/(64M^2).                       (4.3)
```

The cap consistency relation in (3.7) also gives the direct operational
amplitude statement

```text
Lambda^4>=alpha^4 [r^(-1)-8]_+/192.                   (4.4)
```

With locality or compression defects, substitute `C_req(r)` from (4.2) into
(3.11)-(3.12). Explicitly, with `d` from (3.9),

```text
N_r=[alpha^4 [r^(-1)-8]_+/16-3(1+1/t)d^2]_+,
sum_a p_a>=N_r/[4(1+t)Lambda^2],
Lambda^4>=N_r/[12(1+t)].                              (4.5)
```

Equivalently, with response ratio `g=|alpha|/M`, the dimensionless normalized
weight obeys

```text
sum_a p_a(rho)/M^2>=g^4 [r^(-1)-8]_+/64.              (4.6)
```

This is the requested operational implication and is nontrivial for
`r<1/8`. It is necessary, not sufficient: the Casimir allocation does not
itself construct a good reference state or measurement.

Equation (4.1) is an imported, previously proved global Bayes-risk lemma, not
a local Cramer-Rao estimate. Its complete spin-1 fusion/discrete-Hardy proof is
in `docs/global_so3_reference_risk.md`. A standalone manuscript must reproduce
that proof in an appendix or cite a published theorem with the identical task
and constant.

The implication must also pass a non-vacuity check. For maximum code spin
`J_max`, W3's strict-cutoff result and the compressed-action norm imply

```text
R_ref>=sin^2[pi/(2J_max+3)],
|alpha|J_max<=M+epsilon.                               (4.7)
```

Thus a declared risk, gain, norm, error, and spin support that violate either
condition describe no realization. The executable certificate reports this
separately from the leakage lower bound.

There is an important escape route. Since `||alpha J_a||<=M`, a spin-`J` code
has `g<=1/J`. The relative leakage bound can therefore vanish in the classical
large-spin limit even while the absolute fixed-gain bound grows. A physical
paper must either keep the gain calibration fixed or derive it from an
interaction time, local operator normalization, energy, or lifetime. The
algebra alone is not a universal claim that better references decohere faster.

## 5. Distributed Ferromagnetic Realizations

Take an even number `N` of spin-one-half sites and let `P_N` project onto the
totally symmetric spin-`j=N/2` subspace. This is the exact ground space of the
local frustration-free ferromagnet

```text
H_F=sum_(i=1)^(N-1) [1/4-S_i dot S_(i+1)].             (5.1)
```

Each summand is the projector onto the two-site antisymmetric (singlet)
subspace. A zero-energy vector is therefore invariant under every adjacent
transposition; those transpositions generate the permutation group, so the
common kernel is exactly `Sym^N(C^2)`.

Choose disjoint blocks `X,Y` of sizes `r,s` and define

```text
A_x=(N/r) sum_(i in X) S_i^x,
B_y=(N/s) sum_(k in Y) S_k^y.                          (5.2)
```

The microscopic operators commute, while permutation symmetry gives

```text
P_N A_x P_N=J_x,             P_N B_y P_N=J_y.          (5.3)
```

For distinct sites `i!=k`, permutation symmetry makes every ordered pair
equivalent. Hence

```text
N(N-1) P_N S_i^a S_k^b P_N
 =P_N [J_a J_b-sum_l S_l^a S_l^b] P_N,
S_l^a S_l^b=delta_ab I/4+i epsilon_abc S_l^c/2.
```

Using `[J_a,J_b]=i epsilon_abc J_c` gives

```text
P_N S_i^a S_k^b P_N
 =[{J_a,J_b}/2-delta_ab N/4]/[N(N-1)].                 (5.4)
```

Their leakage operators satisfy

```text
(Q A_x P_N)^dagger(Q A_x P_N)
 =[(N-r)/(r(N-1))](j^2-J_x^2),                         (5.5)
```

and analogously for `B_y`. The cross terms are

```text
P_N B_y Q A_x P_N={J_x,J_y}/[2(N-1)]+iJ_z/2,
P_N A_x Q B_y P_N={J_x,J_y}/[2(N-1)]-iJ_z/2.          (5.6)
```

For complementary half-blocks,

```text
lambda_X=lambda_Y=j/sqrt(N-1),
2 lambda_X lambda_Y/||J_z||=N/(N-1) -> 1.             (5.7)
```

Thus the constant `2` in (2.3) is asymptotically sharp in a distributed local
model. A fixed-width unused buffer between the blocks changes the ratio to

```text
[N/(N-1)] [(N+b)/(N-b)] -> 1.                          (5.8)
```

Here `N-b` must be even. Near-saturation does not depend on adjacent supports.
For a buffer, the relative leakage is

```text
lambda_X/||A_x||=sqrt[(N+b)/((N-b)(N-1))],             (5.9)
```

which reduces to `1/sqrt(N-1)` at `b=0`. The absolute leakage grows as
`sqrt(N)`, but the relative leakage vanishes. This explicitly realizes the
normalization escape route rather than hiding it.

### Three-Cell State-Weighted Family

Let `N` be a multiple of six, divide the sites into three disjoint blocks of
size `N/3`, and put

```text
A_a=3 sum_(i in X_a) S_i^a,       a=x,y,z.            (5.10)
```

The `A_a` commute pairwise, `P_N A_a P_N=J_a`, and

```text
lambda_*^2=max_a ||Q A_a P_N||^2=N^2/[2(N-1)],
p_a(rho)=2[j^2-Tr(rho J_a^2)]/(N-1),
sum_a p_a(rho)=N.                                     (5.11)
```

The value `p_a=N/3` holds for the isotropic code state, not for every state.
Choosing the certified cap `Lambda=lambda_*`, the theorem's lower bound and
the actual value are

```text
sum_a p_a >=(N+2)(N-1)/(8N),
actual/lower=8N^2/[(N+2)(N-1)] -> 8.                  (5.12)
```

Thus the main state-weighted theorem has the correct `Theta(N)` scaling for
observables supported on three disjoint macroscopic lattice regions, within a
constant factor eight. This does not prove optimality of the factor four in
(3.6).

The code projector is global, as code projectors generally are. Both model
families are checked against explicit ambient Dicke-basis matrices, including
a positive buffer. Their support diameters grow with `N`, and the ferromagnetic
parent does not have a uniform spectral gap. They therefore establish
disjoint-region commutativity, not a uniformly localized apparatus. They also
do not claim local preparation, a continuum net, or a finite-time lifetime.

## 6. Scope And Nonclaims

The theorem applies when distinct spacelike cells are each required to
reproduce different noncommuting components of one rigid collective mode. It
does **not** say that different current components in the same local region
must commute. AQFT permits a full non-Abelian symmetry to be localized in one
region under appropriate split assumptions.

Also not claimed:

- an extension to unbounded QFT currents or affiliated operators;
- a transition rate, channel error, or apparatus lifetime;
- a no-go for all local non-Abelian reference fields;
- a relation to gravity, `S_Ob`, the Skyrmion, or Paper U closure;
- novelty of the compression identity or generic approximate Eastin-Knill
  machinery.

The priority stop and neighboring joint-measurement/QEC results are assessed
in `docs/spacelike_replication_novelty_audit.md` and
`docs/spacelike_replication_qec_reduction_audit.md`.

## 7. Reproduction

```bash
PYTHONPATH=. python -m pytest -q \
  tests/test_locality_reference_leakage.py \
  tests/test_global_so3_reference_risk.py \
  tests/test_spacelike_replication_manuscript.py
PYTHONPATH=. python -m qgtoy locality-reference-leakage
```

Artifacts:

- `qgtoy/locality_reference_leakage.py`;
- `tests/test_locality_reference_leakage.py`;
- `docs/spacelike_replication_novelty_audit.md`;
- `docs/spacelike_replication_qec_reduction_audit.md`;
- `paper/spacelike_replication_paper_outline.md`;
- `paper/spacelike_replication/main.tex`;
- `paper/spacelike_replication/references.bib`;
- `tests/test_global_so3_reference_risk.py`; and
- `tests/test_spacelike_replication_manuscript.py`.
