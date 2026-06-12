# Global SO(3) Orientation Risk From Asymmetry And Mean Spin

Status: analytic all-state/all-POVM methods theorem; standalone novelty stopped
by Hayashi's exact mean-Casimir solution; physical matter/gravity composition
remains open

## Operational Task

Let the unknown frame orientation `g in SO(3)` have normalized Haar prior and
let an arbitrary POVM return an estimate `g_hat`. If `theta` is the rotation
angle of `g_hat^-1 g`, use the bounded full-frame chordal cost

```text
c(g,g_hat)=sin^2(theta/2)=(3-Tr R(g_hat^-1 g))/4.
```

For a reference state `rho`, rotations act as

```text
U(g)=direct_sum_(j>=0) U_j(g) tensor identity_(M_j).
```

The multiplicity spaces may be arbitrary. They can contain the right-regular
indices of `L^2(SO(3))`, internal species, or spectators, but rotations must act
trivially on them.

## Direct Fusion-Risk Theorem

Let

```text
Cbar=Tr(rho J^2)=sum_j j(j+1) Tr(P_j rho).
```

Every state and orientation measurement obeys the direct global bound

```text
R_ref >= 1/(16 Cbar+8).                       (1)
```

This is a coarse elementary corollary, not the optimal risk-resource frontier.
Hayashi's exact solution of the same Haar `SO(3)` problem and Casimir constraint
gives, in the present cost convention,

```text
R_opt(Cbar)=kappa_SO3(Cbar)/2
            =9/(16Cbar)-81/(256Cbar^2)+o(Cbar^-2).
```

The exact source-level dictionary is recorded in
`global_so3_risk_priority_audit.md`. Bound (1) remains useful when a simple
closed form is preferable, but it must not be presented as a novel or sharp
mean-Casimir law.

For a uniform prior, covariantization preserves the character score
`S=E[chi_1(g_hat^-1 g)]`. The covariant Naimark/imprimitivity dilation embeds
the protocol into the vector-valued regular representation
`L^2(SO(3)) tensor K`, where the score is multiplication by `chi_1`. In
Peter-Weyl blocks, the spin-1 fusion rule and a
unital-CP/Kadison estimate give block norm at most one precisely for
`j=k-1,k,k+1`, with the `0 -> 0` diagonal absent. Arbitrary multiplicity spaces
do not change this norm.

Writing `v_j=sqrt(Tr(P_j rho))`, this gives

```text
S <= v^T M v,
M_00=0, M_jj=1 (j>=1), M_j,j+1=M_j+1,j=1.
```

The exact Dirichlet identity and a discrete Hardy estimate are

```text
3-v^T M v=sum_j(v_j-v_j+1)^2+2v_0^2,

1=sum_j(j+1)(v_j^2-v_j+1^2),

sum_j(v_j-v_j+1)^2 >= 1/(4 Cbar+2).
```

Since `R_ref=(3-S)/4`, equation (1) follows. Mixed states are purified with an
invariant ancilla, which only enlarges the rotation-trivial multiplicities.
The theorem is therefore independent of purity, multiplicity, and POVM
design. It proves a necessary resource law; it does not claim that large
Casimir is sufficient for good orientation.

The Clebsch-Gordan block contraction and the complete weighted Hardy argument
are expanded in `paper/spacelike_replication/main.tex`, Appendix B. The focused
test suite now checks the full normalized Peter-Weyl blocks through spin six,
including the dimension factor, adjoint relation, and multiplicity stability.

For strict support `j<=J`, diagonalizing the finite fusion matrix gives the
exact result

```text
R_ref >= sin^2[pi/(2J+3)].                    (2)
```

This cutoff optimum is also established prior art; Hayashi gives the same law
and Bagan, Baig, and Munoz-Tapia obtain the equivalent character-matrix
optimum.

If the probability above `J` is `q_J`, gentle projection transfers (2) as

```text
R_ref >= max{0,sin^2[pi/(2J+3)]-sqrt(q_J)}.   (3)
```

## Global Information-Risk Theorem

Write

```text
A_SO3(rho)=D(rho || G(rho)),
G(rho)=integral dg U(g) rho U(g)^*.
```

Every orientation measurement obeys

```text
R_ref=E[c(g,g_hat)]
 >= C_SO3 exp[-2 A_SO3(rho)/3],

C_SO3=6/[e pi^(5/3)].                         (4)
```

This is a global Bayes statement. It assumes neither a locally unbiased
estimator nor a Cramer-Rao regime.

To prove (4), let `Y` be the measurement outcome. Relative-entropy data
processing from the continuous orbit ensemble to the classical measurement
outcome gives

```text
I(g:Y)<=D(rho || G(rho))=A_SO3(rho).
```

When both von Neumann entropies are finite this is the familiar identity
`A_SO3=S(G(rho))-S(rho)`. The relative-entropy statement remains defined when
an infinite-dimensional invariant multiplicity makes both entropies infinite.

For each outcome, rotate the conditional true-frame distribution into an
error distribution. Relative-entropy positivity against the Gibbs density
`exp(-lambda c)/Z(lambda)` gives

```text
I(g:Y) >= -lambda R_ref-log Z(lambda).
```

Normalized Haar measure has angle density
`(2/pi) sin^2(theta/2)`. The chord inequalities

```text
theta/pi <= sin(theta/2) <= theta/2
```

imply

```text
Z(lambda)<=pi^(5/2)/(8 lambda^(3/2)).
```

Optimizing the resulting lower bound over `lambda` yields (4). The argument is
measure-theoretic and also covers singular conditional distributions.

## Tail-Robust Mean-Spin Bound

Let `p_j=Tr(P_j rho)` and

```text
K=sum_j j p_j.
```

Finite-rank block dephasing, Araki-Lieb, and the entropy gain of the irrep
measurement give

```text
A_SO3(rho)<=H(p)+2 sum_j p_j log(2j+1).        (5)
```

General normal states follow by invariant finite-rank approximation and lower
semicontinuity of relative entropy. This bound does not depend on `dim M_j`.
Maximizing its right-hand side at
fixed `K` is a classical Gibbs problem with degeneracy `(2j+1)^2`. Define

```text
B(K)=inf_(beta>0) [beta K+log Z_spin(beta)],

Z_spin(beta)=sum_(j>=0)(2j+1)^2 exp(-beta j)
            =(1+6e^-beta+e^-2beta)/(1-e^-beta)^3.
```

Combining (4) and (5) gives the all-state theorem

```text
R_ref >= C_SO3 exp[-2 B(K)/3].                (6)
```

As `K -> infinity`, `B(K)=3 log K+O(1)`, so (6) has the physically useful
inverse-square scaling `R_ref=Omega(K^-2)`. A probability `1/j` placed at an
arbitrarily large spin has fixed `K=1`; unlike local QFI, it cannot evade (6).
This closes the rare-tail loophole in the necessary direction.

## Compact Spherical-Top Corollary

The marked spherical-top EFT already proves, under its declared inertia,
excitation, and local compactness assumptions,

```text
Cbar=E[j(j+1)]
 <= kappa chi^2 zeta a^4/[2G^2(1+zeta)^2].    (7)
```

Jensen's inequality gives

```text
K(K+1)<=Cbar,
K<=K_max=(sqrt(1+4Cbar)-1)/2.                 (8)
```

The direct theorem already yields the elementary localization-backreaction
floor

```text
R_ref >= 1/[8+8 kappa chi^2 zeta a^4/(G^2(1+zeta)^2)].  (9)
```

The independent information route gives

```text
R_ref >= C_SO3 exp[-2 B(K_max)/3].            (10)
```

The maximum of (9) and (10) is the implemented bound. Both scale as `G^2/a^4`
at large capacity with fixed `kappa`, `chi`, and `zeta`. They are uniform over
all rotor states, including zero-mean,
anticoherent, mixed, and rare-tail states. Casimir is used only as an upper
capacity budget; it is not claimed to certify reference quality.

## Exact Heat-Diffusion Coherence Ceiling

Now let the prepared reference itself undergo isotropic rotational diffusion

```text
H_s(rho)=integral dh k_s(h) U(h)rho U(h)^*,
s=gamma tau.
```

This is reference-only loss of orientation information, distinct from the
collective target-reference common-mode channel used elsewhere in the
repository. Convolution with the heat kernel multiplies the spin-1 character
by `exp(-2s)`. Therefore the optimized score is attenuated by exactly the same
factor. Combining this with the fusion/Hardy score ceiling gives

```text
R_ref(tau)
 >= 3/4 [1-exp(-2 gamma tau)]
    +exp(-2 gamma tau)/(16 Cbar+8).           (11)
```

The bound interpolates between the finite-resource floor and the no-information
Haar risk `3/4`. If compactness only permits `Cbar<=C_max`, maintaining
`R_ref(tau)<=epsilon<3/4` requires both

```text
epsilon >= 1/(16 C_max+8),

gamma tau <= (1/2) log[
  (3/4-1/(16 C_max+8))/(3/4-epsilon)].        (12)
```

Thus the declared diffusion model supplies an exact necessary coherence-time
ceiling, rather than a generic claim that every isolated reference decoheres.
Deriving `gamma` from the Skyrmion/KMS action remains open.

## Fermionic Projective Sector

The `B=1` Skyrmion is not in the integer-spin sector above. Its
Finkelstein-Rubinstein Hilbert space contains

```text
j=1/2,3/2,...,J+1/2.
```

The density operators and covariant POVM effects remain center blind, so the
same `SO(3)` orientation task is well defined. Spin-1 fusion now has a unit
diagonal already at the lowest block. Repeating the Dirichlet/Hardy proof gives

```text
R_ref>=1/(16 Cbar),       Cbar=E[j(j+1)]>=3/4.          (13)
```

For strict odd-sector cutoff `J`, diagonalizing the Toeplitz fusion matrix gives

```text
R_ref>=sin^2[pi/(2J+4)].                              (14)
```

Equation (14), rather than the integer-sector formula used blindly, is the
appropriate bound for the fermionic Skyrmion realization.

## What This Closes

- UO.1a is complete for the declared Haar-prior chordal orientation task by
  two independent routes: spin-1 fusion/Hardy and asymmetry/Holevo.
- The global-risk to mean-spin implication is robust against high-spin tails.
- UO.2Q closes inside the spherical-top constitutive class, for confined
  spinless nonrelativistic orbital matter satisfying `H_ex>=T`, and for the
  profile-relaxed hard-supported Skyrmion hedgehog collective family through
  its linear-in-spin sector floor.
- UO.4b obtains an exact conditional ceiling under reference-only isotropic
  heat diffusion.
- The projective half-integer extension needed by the `B=1` Skyrmion is
  complete.
- Arbitrary rotation-trivial internal multiplicity cannot hide additional
  asymmetry at fixed spin distribution.

## What Remains Open

The theorem does not supply:

- a relativistic or model-independent compactness theorem for rotating quantum
  matter;
- collective-band completeness, noncollective rotating modes, and
  nontrivially rotating cheap species;
- a physical local interaction relating estimation risk to coherent recovery;
- optical support, preparation time, or coherence under a KMS bath;
- a stress-tensor derivation for the Skyrmion worldtube; or
- the noncompact de Sitter boost sector.

The novelty target is the eventual connection of the known estimation theory
to optical locality, coherence, and backreaction under one matter action.
Hayashi already solves the exact Haar `SO(3)` mean-Casimir optimization,
including the projective sector and asymptotics. Holevo information bounds,
relative entropy of frameness, and finite-frame alignment are likewise
established ingredients; this document does not claim them individually.

The decisive primary source is Hayashi,
[*Fourier Analytic Approach to Quantum Estimation of Group
Action*](https://arxiv.org/abs/1209.3463). Additional sources are Bagan, Baig,
and Munoz-Tapia,
[Aligning Reference Frames Using Quantum
States](https://arxiv.org/abs/quant-ph/0106014), Gour, Marvian, and Spekkens,
[Measuring the Quality of a Quantum Reference
Frame](https://arxiv.org/abs/0901.0943), and Holevo's covariant estimation and
semigroup framework. Equations (1)-(6) are enabling methods results, not the
paper's standalone novelty claim.

## Reproduction

```bash
PYTHONPATH=. python3 -m unittest tests.test_global_so3_reference_risk
```

Artifacts:

- `qgtoy/global_so3_reference_risk.py`
- `tests/test_global_so3_reference_risk.py`
- `docs/global_so3_risk_priority_audit.md`
- `docs/rotational_resource_substitution_no_go.md`
- `docs/finite_size_static_patch_observer.md`
