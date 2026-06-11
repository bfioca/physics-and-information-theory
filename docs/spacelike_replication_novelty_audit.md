# Spacelike SO(3) Replication: Novelty Audit

Audit date: 2026-06-11 UTC

Verdict: **NOVELTY STOP.** The projected-commutator identity, its operator-norm
bound, and the state-weighted three-cell inequality are consequences of
established UCP compression and joint-measurement noise inequalities. In
particular, Janssens' CP-map covariance Cauchy-Schwarz lemma gives the
state-weighted pair bound directly; cyclic summation gives the proposed main
theorem. Retain the result as an internal lemma, not a standalone paper claim.

## 1. Closest Primary Literature

### Compression Mathematics

| Source | Established mechanism | Consequence for this project |
| --- | --- | --- |
| [Bauer, Coburn, and Hagger, arXiv:1704.05652](https://arxiv.org/abs/1704.05652) | Toeplitz/Hankel product identities express the failure of compressed multiplication through off-subspace factors. | `PAP/PBP` noncommutativity caused by `Q` excursions is not new. |
| [Bordemann, Meinrenken, and Schlichenmaier, hep-th/9309134](https://arxiv.org/abs/hep-th/9309134) | Berezin-Toeplitz quantization produces noncommuting projected observables from commuting classical functions. | Projection-induced noncommutativity is established quantization machinery. |

### Joint Measurement And Added Noise

| Source | Established mechanism | Consequence for this project |
| --- | --- | --- |
| [Janssens, *Unifying Decoherence and the Heisenberg Principle*](https://doi.org/10.1007/s11005-017-0953-z) | Lemma 1 proves Cauchy-Schwarz for the covariance form of a CP map; Theorem 3 gives the corresponding joint-measurement noise bound, and the following construction establishes sharpness. | With `T(X)=W*XW`, the covariance defect is exactly `W*AQA W`; the state-weighted theorem follows immediately. This kills the central novelty claim. |
| [Polterovich, *Symplectic Geometry of Quantum Noise*](https://doi.org/10.1007/s00220-014-1937-9) | Uses the same added-noise operator and Janssens inequality in the unsharpness principle. | The branch's `p_a` is established state-dependent added variance. |
| [Beneduci, arXiv:1404.1477](https://arxiv.org/abs/1404.1477) and [Mitra, Ghosh, and Mandayam, arXiv:2011.11364](https://arxiv.org/abs/2011.11364) | Give Naimark-dilation characterizations for pairs and for finite sets of finite-outcome POVMs, respectively. | The present continuous-spectrum pointer triple is supplied directly by its joint spectral measure; the cited dilation results are neighboring compatibility context. |

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
The Janssens reduction below was checked at the level of the stated CP
covariance lemma and joint-measurement theorem, not inferred from an abstract.

### Parameter-Level Overlap Check

| Result | Locality/symmetry input | Error or leakage variable | Resource/output | Relation to this specialization |
| --- | --- | --- | --- | --- |
| Present specialization | Three pairwise commuting bounded cell observables compress to `alpha J_a` | `p_a=Tr(rho P A_a Q A_a P)`, code-visible commutator defect, compression error | Mean Casimir and full-frame Haar risk imply a lower bound on `sum p_a` and `lambda_*=max||Q A_aP||` | An `SO(3)` application of UCP added noise. |
| Janssens, Lemma 1 and Theorem 3 | Commuting pointers mapped by a CP measurement/compression map to incompatible observables | CP covariance/added-noise operator | Pairwise noise-product lower bound and sharpness | Directly implies the state-weighted pair bound; cyclic summation gives the main theorem. |
| Faist et al. `1902.07714` | Exact continuous covariance implemented transversally on physical subsystems | Erasure-recovery infidelity | Bounds in subsystem number/dimension and constructions with comparable scaling | Stronger QEC task and different metric; the earlier Janssens reduction is already decisive. |
| Zhou, Liu, Jiang `2005.11918` | Continuous covariant code | Erasure or depolarizing infidelity | Metrological/resource lower bounds and near-saturating codes | Does not use three cell observables or state-weighted `Q`-excursion as its stated metric. |
| Liu and Zhou `2111.06360` | Exact or approximate channel covariance/charge conservation | QEC inaccuracy and three symmetry-violation measures | Charge-fluctuation and gate-error tradeoffs | Supplies a relative-covariance/QFI dictionary, but the earlier Janssens reduction is already decisive. |
| Beny, Zimboras, Pastawski `1806.10324` | Local channels with symmetry constraints | Optimal decoding fidelity/local information disturbance | Constrained recovery theorem | Uses complementary channels and recovery, not a fixed global-code compression of replicated Lie brackets. |

The QEC sources use different hypotheses and metrics and did not by themselves
kill the claim. The broader operator-theory audit did: Janssens' covariance
form identifies `p_a` and `lambda_a^2` exactly and yields the required
inequality without a recovery-channel construction.

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

## 3. Stopped Candidate Claim

The proposed candidate was the state-weighted inequality

```text
alpha^4 Tr(rho J^2)
 <=4 lambda_*^2 sum_a Tr[rho P A_a Q A_a P].            (3.1)
```

For the UCP compression `T(X)=W*XW`, Janssens' covariance form satisfies

```text
(A_a,A_a)_T=W* A_a Q A_a W.                           (3.2)
```

His CP Cauchy-Schwarz lemma bounds each cross covariance by the two diagonal
defects. When the `A_a` commute and `T(A_a)=alpha J_a`, it gives the pairwise
state-weighted inequality used in the proof of (3.1). Cyclic summation then
produces (3.1) with the same factor four. The exact substitution is given in
`spacelike_replication_qec_reduction_audit.md`.

The Haar-risk composition and ferromagnetic examples remain correct, but
composing an established added-noise inequality with a resource bound and an
example is not enough to support the proposed central novelty claim.

## 4. Retained Value And Redirects

The bounded result remains useful as:

- a clean locality/joint-measurement lemma inside the Paper U architecture;
- an explicit fixed-calibration `SO(3)` realization of standard added noise;
- a tested dictionary among off-code weight, Schwarz defect, and relative
  covariance tangent; and
- a warning that disjoint commuting pointers cannot reproduce a rigid
  non-Abelian triple without standard joint-measurement noise.

A future standalone paper must add a result not already supplied by the CP-map
and joint-measurement framework: a genuinely multi-observable sharp inequality,
a dynamical rate or lifetime, a physical localization/energy/backreaction
bound on the noise, or a separately novel global `SO(3)` risk theorem.
