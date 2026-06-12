# Global SO(3) Risk: Exact Priority Reduction

Audit date: 2026-06-11 UTC

Disposition: **TECHNICAL RESULT RETAINED; STANDALONE NOVELTY STOP.** The
repository's global Haar-prior orientation-risk bounds are correct on their
declared domains, but the exact mean-Casimir optimization, its optimizers, its
projective extension, and its asymptotics were already established by Masahito
Hayashi. The repository's fusion/Hardy inequality is a useful elementary lower
bound, not a paper-level novelty claim.

Primary source: Masahito Hayashi, [*Fourier Analytic Approach to Quantum
Estimation of Group Action*](https://arxiv.org/abs/1209.3463), *Communications
in Mathematical Physics* **347**, 3-82 (2016),
[doi:10.1007/s00220-016-2738-0](https://doi.org/10.1007/s00220-016-2738-0).
The decisive statements are the general `SO(3)` reduction in Theorem
`t5-26-1` and the exact Casimir-constrained solution in Theorem
`T3-13-3cx` of the arXiv source.

## Exact Variable Dictionary

Both problems use:

- an unknown `g in SO(3)` with normalized Haar prior;
- arbitrary integer-spin representation sectors;
- arbitrary input states, including mixed states and ensembles;
- covariant POVMs without loss for the invariant Bayes problem; and
- the mean-Casimir constraint

```text
E=Tr(rho J^2)=sum_j j(j+1) p_j.
```

The only normalization difference is the loss function. This repository uses

```text
c=(3-chi_1)/4=sin^2(theta/2),
```

whereas Hayashi uses

```text
R_H=(3-chi_1)/2=1-cos(theta)=2c.
```

Therefore every exact risk in Hayashi's convention is twice the corresponding
risk in this repository.

## Known Exact Optimum

Let `a_1` be the odd Mathieu characteristic value in Hayashi's convention. His
exact optimum is

```text
kappa_SO3(E)
 =max_(s>0) [s a_1(2/s)/4+1-s(E+1/4)].
```

Consequently the exact optimum for the repository's chordal loss is

```text
R_opt(E)=kappa_SO3(E)/2.                                (1)
```

Hayashi also identifies the attaining Mathieu state and canonical covariant
measurement. At large `E`,

```text
R_opt(E)=9/(16E)-81/(256E^2)+o(E^-2).                  (2)
```

By comparison, the repository's elementary fusion/Hardy theorem gives

```text
R>=1/(16E+8)=1/(16E)+O(E^-2).                          (3)
```

Equation (3) is valid but asymptotically weaker by a factor of nine in the
leading constant. At `E=0`, the exact optimum is `3/4`, while (3) gives only
`1/8`.

The repository's scalar fusion matrix is another representation of the same
problem. Writing `F_00=0`, `F_jj=1` for `j>=1`, and
`F_j,j+1=F_j+1,j=1`, its sharp variational problem is

```text
4 R_opt(E)
 =inf {<v,(3I-F)v>: ||v||=1,
                         sum_j j(j+1)v_j^2<=E}.
```

The Lagrange dual is the ground-state problem for
`3I-F+lambda diag[j(j+1)]`. Fourier transformation turns it into Hayashi's
odd Mathieu problem. This is an exact reduction, not merely a similarity of
asymptotic scaling.

## Cutoff And Projective Sectors

For strict integer-spin support `0<=j<=J`, Hayashi's exact risk becomes

```text
R_opt(J)=sin^2[pi/(2J+3)],
```

exactly the repository formula. Equivalent spin-one-character matrices occur
in Bagan, Baig, and Munoz-Tapia,
[*Entanglement assisted alignment of reference frames using a dense covariant
coding*](https://arxiv.org/abs/quant-ph/0303019).

Hayashi also treats the half-integer projective `SO(3)` sector and supplies its
exact energy-constrained optimum. The repository's projective formulas are
therefore established prior art as well. Chiribella, D'Ariano, and Sacchi,
[*Optimal estimation of group transformations using
entanglement*](https://arxiv.org/abs/quant-ph/0506267), provide the neighboring
general compact-group Bayesian and multiplicity framework.

## Research Consequence

Do not pursue any of the following as a standalone novelty claim:

- the fusion/Hardy mean-Casimir floor;
- the exact strict-cutoff sine law;
- the integer versus projective comparison;
- the sharp expected-Casimir Pareto curve;
- the Mathieu optimizer or its `9/(16E)` asymptotic; or
- arbitrary rotation-trivial multiplicity as a new extension.

The correct role of the global risk result is as a known estimation-theory
input to a theorem containing new physics not present in Hayashi: a derived
localization/energy or gravitational capacity, a restricted local readout, a
finite-time open-system obstruction, or a same-action
localization-coherence-backreaction inequality.

The repository should retain (3) when its elementary closed form is convenient,
but paper-facing work should cite Hayashi and use the exact envelope (1) or a
clearly labeled corollary of it whenever constants matter.
