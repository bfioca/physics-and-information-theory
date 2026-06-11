# Spacelike SO(3) Replication: Novelty Audit

Audit date: 2026-06-11 UTC

Verdict: **REDIRECT THE HEADLINE.** The projected-commutator identity and its
immediate operator-norm bound are standard compression phenomena. They are
useful lemmas but not a publishable novelty claim. The narrower state-weighted
spacelike-replication theorem is a plausible paper result, subject to an
independent specialist search and review.

## 1. Closest Primary Literature

### Compression Mathematics

| Source | Established mechanism | Consequence for this project |
| --- | --- | --- |
| [Bauer, Coburn, and Hagger, arXiv:1704.05652](https://arxiv.org/abs/1704.05652) | Toeplitz/Hankel product identities express the failure of compressed multiplication through off-subspace factors. | `PAP/PBP` noncommutativity caused by `Q` excursions is not new. |
| [Bordemann, Meinrenken, and Schlichenmaier, hep-th/9309134](https://arxiv.org/abs/hep-th/9309134) | Berezin-Toeplitz quantization produces noncommuting projected observables from commuting classical functions. | Projection-induced noncommutativity is established quantization machinery. |

### Locality And Covariant QEC

| Source | Established mechanism | Consequence for this project |
| --- | --- | --- |
| [Eastin and Knill, arXiv:0811.4262](https://arxiv.org/abs/0811.4262) | Exact finite-dimensional quantum codes cannot support universal continuous transversal logical gates. | A continuous-symmetry code obstruction cannot be advertised as a new general idea. |
| [Beny, arXiv:0907.4207](https://arxiv.org/abs/0907.4207) | Gives dimension-independent approximate-correctability conditions for observable algebras. | The paper must distinguish off-band state weight from reconstruction error for an algebra. |
| [Flammia, Haah, Kastoryano, and Kim, arXiv:1610.06169](https://arxiv.org/abs/1610.06169) | Develops local approximate correctability, logical-operator avoidance, and spatial tradeoff bounds. | Spatially distributed logical support and approximate cleaning are substantial prior machinery. |
| [Beny, Zimboras, and Pastawski, arXiv:1806.10324](https://arxiv.org/abs/1806.10324) | Proves a local information-disturbance tradeoff for recovery under locality and symmetry constraints. | Locality plus symmetry plus a quantitative disturbance measure is not new as a general conjunction. |
| [Faist et al., arXiv:1902.07714](https://arxiv.org/abs/1902.07714) | Continuous symmetries impose quantitative approximate-QEC limitations; local symmetry factors can evade exact code arguments by leaving the code. | The statement that local factors must leak from an invariant code is established intuition. |
| [Harlow and Ooguri, arXiv:1810.05338](https://arxiv.org/abs/1810.05338) | Splittability, locality, code preservation, and correctability constrain global symmetries. | Splittability, correctability/reconstruction, and code preservation already provide a major no-go context; microcausality alone is insufficient. |
| [Hayden et al., arXiv:1709.04471](https://arxiv.org/abs/1709.04471) | Finite-dimensional covariant codes cannot perfectly correct the relevant local erasures for continuous non-Abelian groups. | `SO(3)` covariance and exact local correctability are not a new combination. |
| [Zhou, Liu, and Jiang, arXiv:2005.11918](https://arxiv.org/abs/2005.11918) | Quantitative approximate Eastin-Knill bounds relate code quality and continuous symmetry. | Any claimed scaling must be compared explicitly with approximate covariant-code bounds. |
| [Liu and Zhou, arXiv:2111.06360](https://arxiv.org/abs/2111.06360) | Charge fluctuation and QEC inaccuracy obey quantitative tradeoffs, with near-saturating constructions. | A charge-versus-error inequality alone is unlikely to be novel. |
| [Yang et al., arXiv:2007.09154](https://arxiv.org/abs/2007.09154) | Approximate covariant codes can be constructed from bounded quantum reference frames. | Bounded-reference achievability and covariance are established neighboring results. |
| [Li et al., arXiv:2309.16556](https://arxiv.org/abs/2309.16556) | Non-Abelian covariant codes can approach optimal accuracy scalings. | The manuscript must not imply that non-Abelian finite codes are generically impossible. |

### Quantum Reference Frames

| Source | Established mechanism | Consequence for this project |
| --- | --- | --- |
| [Miyadera and Loveridge, arXiv:2006.14247](https://arxiv.org/abs/2006.14247) | `SU(2)` channel accuracy is bounded by reference angular-momentum resources and commutators. | The risk/resource composition must add more than a generic finite-reference size bound. |
| [Peres and Scudo, quant-ph/0103149](https://arxiv.org/abs/quant-ph/0103149) | Constructs and decodes a finite quantum token for a Cartesian frame. | Full-frame transmission with several spin irreps is established prior art. |
| [Bagan, Baig, and Munoz-Tapia, quant-ph/0106014](https://arxiv.org/abs/quant-ph/0106014) | Optimizes finite-spin encoding and measurement for aligning an orthogonal trihedron. | Global `SO(3)` frame risk and its finite-resource scaling are not new by themselves. |
| [Gour, Marvian, and Spekkens, arXiv:0901.0943](https://arxiv.org/abs/0901.0943) | Identifies relative entropy of frameness with `G`-asymmetry and bounds extractable group information. | The operational frame-resource interpretation is established; the exact Casimir-risk constant needs its own proof. |

Official arXiv metadata and abstracts for the closest recovery and frame
papers were refreshed on 2026-06-11. This remains a bounded primary-source
audit. Search absence is not evidence of priority, and abstract-level
comparison cannot replace a specialist source-level review.

### Parameter-Level Overlap Check

| Result | Locality/symmetry input | Error or leakage variable | Resource/output | Difference from the candidate |
| --- | --- | --- | --- | --- |
| Present candidate | Three pairwise commuting bounded cell observables compress to `alpha J_a` | `p_a=Tr(rho P A_a Q A_a P)`, code-visible commutator defect, compression error | Mean Casimir and full-frame Haar risk imply a lower bound on `sum p_a` and `lambda_*=max||Q A_aP||` | No recovery channel or erasure model; the target is simultaneous spacelike replication of three rigid components. |
| Faist et al. `1902.07714` | Exact continuous covariance implemented transversally on physical subsystems | Erasure-recovery infidelity | Bounds in subsystem number/dimension and constructions with comparable scaling | Stronger QEC task and different metric; a source-level derivation may still subsume the candidate. |
| Zhou, Liu, Jiang `2005.11918` | Continuous covariant code | Erasure or depolarizing infidelity | Metrological/resource lower bounds and near-saturating codes | Does not use three cell observables or state-weighted `Q`-excursion as its stated metric. |
| Liu and Zhou `2111.06360` | Exact or approximate channel covariance/charge conservation | QEC inaccuracy and three symmetry-violation measures | Charge-fluctuation and gate-error tradeoffs | Closest quantitative threat; direct symbol-by-symbol reduction must be checked before submission. |
| Beny, Zimboras, Pastawski `1806.10324` | Local channels with symmetry constraints | Optimal decoding fidelity/local information disturbance | Constrained recovery theorem | Uses complementary channels and recovery, not a fixed global-code compression of replicated Lie brackets. |

This table identifies different hypotheses and metrics; it does not establish
logical independence. In particular, the paper is killed as a novelty claim
if Theorem 1 follows immediately from an existing approximate-cleaning or
covariant-code theorem after translating `p_a`, `lambda_*`, and `alpha`.

## 2. Killed Headline

The following proposed headline is **not viable**:

> Microcausality forces leakage in every finite-dimensional non-Abelian
> reference frame with spatial support.

It is too broad for two reasons.

First, microcausality constrains observables in distinct spacelike regions; it
does not force different non-Abelian current components inside one region to
commute. Split-property constructions may localize a full non-Abelian symmetry
within a region.

Second, the identity

```text
[PAP,PBP]=P[A,B]P+PBQAP-PAQBP
```

is standard compression algebra. A Toeplitz, projected-coordinate, Naimark, or
generic QEC example cannot make it a standalone novelty result.

## 3. Surviving Candidate Claim

The surviving candidate target is:

> If three pairwise spacelike cells are each required to reproduce a different
> component of the same rigid finite `SO(3)` collective mode, then their total
> state-weighted off-code quadratic weight is bounded below. For any code
> state, the bound is controlled by its mean Casimir and hence by its achieved
> global orientation risk.

With `lambda_*=max_a||Q A_aP||`, the exact result can be written without a
division-by-zero convention as

```text
alpha^4 Tr(rho J^2)
 <=4 lambda_*^2 sum_a Tr[rho P A_a Q A_a P],
lambda_*^4>=alpha^4 Tr(rho J^2)/12.                   (3.1)
```

This assumes exact pairwise spacelike commutation and exact real gain `alpha`.
Combining it with the existing Haar-risk theorem gives, for `0<r<1/8`,

```text
lambda_*^4>=alpha^4 [r^(-1)-8]/192.                  (3.2)
```

No checked primary source in this audit states this particular conjunction of
spacelike cell replication, state-weighted off-code quadratic weight, and
full-frame global `SO(3)` risk. This is a candidate distinction requiring
specialist source-level review, not a priority claim established by search.

## 4. Required Novelty Gates

Before submission, all of the following must hold:

1. An AQFT/QEC specialist confirms that Theorem 1 and its risk corollary are
   not immediate corollaries already standard in approximate cleaning or
   covariant-code theory.
2. The manuscript leads with the state-weighted theorem, not the compression
   identity.
3. The disjoint-block ferromagnetic models are checked independently and used
   only for bounded lattice locality, pairwise sharpness, and constant-factor
   state-weighted scaling.
4. The gain normalization and the large-spin relative-leakage escape route are
   stated in the abstract and theorem discussion.
5. Unbounded QFT currents, local preparation, dynamics, lifetime, and gravity
   remain outside the claim unless separately proved.
6. A source-level comparison either distinguishes the candidate from immediate
   corollaries of Faist et al., Liu-Zhou, and approximate cleaning, or kills
   the novelty claim.

Failure of gate 1 kills the paper-level novelty while leaving a useful methods
note for the repository.
