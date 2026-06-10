# Angular Edge References And Fuzzy-Horizon Observer Algebras

Status: research draft; central finite theorem implemented, gravitational lift
open

Document role: omnibus research dossier, not a submission manuscript. The
focused matter-derived open-system paper is scoped separately in
`paper/skyrmion_ule_outline.md`; the original fuzzy-horizon/QRF paper remains a
distinct track.

## Abstract

We construct a finite relational observer model on the fuzzy-sphere harmonic
space and show that a Hamiltonian constraint does not, by itself, justify a
diagonal horizon screen. Coupling the harmonic modes to time and angular
reference systems yields three distinct observer algebras: a full matrix
algebra when both references are available, a direct sum of noncommutative
fixed-energy blocks when the time reference is hidden, and a diagonal algebra
only when the angular edge reference is hidden as well. The extra edge
restriction discards `L(L+1)(4L+5)/3` coherence parameters and leaves a
fraction asymptotic to `3/(4L)` of the time-constraint algebra. We give an
operational recovery lower bound of `1/2` for dictionaries factored through the
diagonal screen and show that a Gaussian angular reference must sharpen as
`O(1/L)` to preserve extremal magnetic coherence. Canonical coherent-state
Berezin maps provide UCP cutoff transport, exact heat-flow covariance, and an
`O(1/L)` product theorem on the coordinate operator system. The controlled
continuum limit is Type I, yielding a no-go for interpreting this one-particle
model as the gravitational Type-II static-patch algebra.

The reference-frame attenuation law is standard. The candidate contribution is
the combined algebra hierarchy, recovery obstruction, cutoff transport, and
edge-data scaling in one explicit fuzzy-horizon regulator. A symmetry audit
sharpens the boundary: full `SU(2)` orientation loss retains only a
`3/(4L^2)` fraction, while the axial time/edge distinction is stable only when
magnetic degeneracy is protected over the observation time.

A charged auxiliary block `V_L^* tensor C^{2L+1}` supplies an exact singlet
multiplicity code for a logical spin-`L` sector and saturates a `(2L+1)^2`
dimension lower bound among pure isometries into total spin zero. The displayed
encoder is noncovariant from a charged input, so this is a
representation-theoretic baseline rather than recovery by a prepared quantum
reference frame.

For a fixed prepared axial reference, joint `U(1)` twirling and sector decoding
give an exact coherence channel and pairwise-optimal sine-profile error
`Theta((L/N)^2)`. Under full rotations, however, one spin-`J` reference is
multiplicity-free with the system; its twirl is entanglement-breaking and every
decoder has normalized diamond error at least `1-1/(2L+1)`. Thus charge alone
does not suffice: a positive non-Abelian construction needs controlled irrep
multiplicity. An integer-spin `SO(3)`, equivalently center-blind `SU(2)`,
Peter-Weyl reference supplies an explicit decoder with fixed-target diamond
convergence and a calculable Casimir cost, while exact recovery remains
impossible at every finite cutoff.

## 1. Research Question

Which part of a regulated horizon observer algebra follows from a clock or
Hamiltonian constraint, and which part is lost only after imposing an
additional angular-reference restriction?

The distinction matters because a diagonal screen is often treated as the
natural observer output. In a relational system, however, diagonalization can
conflate two physically different operations:

1. forgetting the time reference, which removes coherence between different
   energies;
2. forgetting an angular edge reference, which also removes coherence inside
   degenerate energy sectors.

The second operation is an additional physical assumption.

## 2. Finite Relational Model

At fuzzy cutoff `L`, take

```text
H_L=L^2(M_{L+1},tau_L)=direct_sum_{ell=0}^L V_ell.
```

The basis `|ell,m>` diagonalizes the adjoint fuzzy Laplacian and axial charge:

```text
K_L|ell,m> = ell(ell+1)|ell,m>,
J_z|ell,m> = m|ell,m>.
```

Add a time reference with momentum `-ell(ell+1)` and an angular edge reference
with charge `-m`. Physical states solve

```text
C_t=K_L+P_t=0,
C_phi=J_z+P_phi=0.
```

Dressed matrix units simultaneously update the system and both references.
They commute with the constraints and compress to all matrix units on the
physical Hilbert space.

## 3. Algebra Hierarchy Theorem

**Theorem 1.** The full relational Dirac algebra is `M_{(L+1)^2}`. If the time
reference is inaccessible, the system algebra is

```text
A_t,L = direct_sum_{ell=0}^L M_{2ell+1}.
```

If both time and angular references are inaccessible, it is

```text
A_tphi,L = C^{(L+1)^2}.
```

**Reason.** A dressed matrix unit between labels `(ell,m)` and `(ell',m')`
requires the corresponding changes of clock momentum and edge charge. Removing
the time reference forces `ell=ell'`; removing the angular reference also
forces `m=m'`.

The dimension removed by the second restriction is

```text
dim(A_t,L)-dim(A_tphi,L)
 = sum_ell [(2ell+1)^2-(2ell+1)]
 = L(L+1)(4L+5)/3.
```

The retained fraction is

```text
dim(A_tphi,L)/dim(A_t,L)
 = 3(L+1)/(4L^2+8L+3)
 ~ 3/(4L).
```

Thus the diagonal screen retains a vanishing fraction of the algebra selected
by the Hamiltonian constraint alone.

## 4. Recovery Obstruction

Let

```text
|psi_+/- > = (|ell,-ell> +/- |ell,ell>)/sqrt(2).
```

The two states are orthogonal and remain distinguishable inside `A_t,L`. The
diagonal conditional expectation maps both to the same state.

**Theorem 2.** Every decoder factored through the diagonal screen has
worst-case trace-distance reconstruction error at least `1/2`. If the two
screen outputs are at distance at most `epsilon`, the lower bound is
`(1-epsilon)/2`.

This follows immediately from contractivity and the triangle inequality. The
result is operational: it distinguishes two algebras derived from different
reference access, rather than comparing an algebra with an abelian control
chosen only to force a collision.

## 5. Edge Resolution

For a Gaussian angular reference of width `sigma`, a charge coherence with gap
`Delta m` is multiplied by

```text
exp[-sigma^2(Delta m)^2/2].
```

For the extremal pair `Delta m=2L`, fixed visibility `v` requires

```text
sigma_L <= sqrt(log(1/v)/2)/L.
```

The smeared `|psi_+/- >` pair has trace distance `v_L`, so contractivity gives

```text
eta_recovery(L) >= (1-v_L)/2
                = (1-exp[-2 sigma^2 L^2])/2.
```

For every fixed nonzero reference width, the recovery lower bound converges to
`1/2`.

The Fourier attenuation and inverse-charge resolution are standard quantum
reference-frame facts. The proposed physics statement is the conjunction:

```text
a diagonal horizon dictionary discards an asymptotically complete fraction of
the time-constraint algebra, incurs a nonzero recovery error, and can retain
the extremal edge sector only with angular resolution improving as 1/L.
```

### 5.1 Full Rotation And Spectral Robustness

The axial `U(1)` reference is not a complete orientation frame. Because each
spin-`ell` irrep occurs once, hiding a full `SU(2)` frame gives, by Schur's
lemma,

```text
(direct_sum_ell M_{2ell+1})^{SU(2)}
  = direct_sum_ell C I_{V_ell}.
```

This is the center of the time-blind algebra. Its dimension is `L+1`, and its
retained fraction is

```text
3/(4L^2+8L+3) ~ 3/(4L^2),
```

not `3/(4L)`. The axial result is therefore a stabilizer or phase-reference
theorem, not a full rotational-reference theorem.

The time/edge distinction also depends on exact magnetic degeneracy. Add an
irrational Zeeman splitting

```text
H_delta|ell,m>=[ell(ell+1)+delta m]|ell,m>,
delta=r sqrt(2),  r nonzero rational.
```

The spectrum becomes nondegenerate, so infinite-time averaging is diagonal
for every nonzero `delta`, however small. For a centered finite time window
`T`, the extremal phase-pair trace distance is instead

```text
|sinc(delta L T)|.
```

Thus the exact algebra dimension is discontinuous at `delta=0`, while the
operational finite-time statement has the controlled crossover
`|delta|LT=O(1)`. The first sinc zero occurs at `pi/(|delta|L)` and later side
lobes give revivals, so this is a resolution scale rather than monotone decay.
Rotationally invariant perturbations `f(K_L)` preserve the within-`ell` blocks
and the edge distinction.

## 6. Canonical Cutoff Transport

The coherent-state Berezin map

```text
J_{L->M}=Q_M sigma_L
```

is UCP, normalized-trace preserving, and exactly covariant with the fuzzy
Laplacian and heat semigroup. It acts diagonally on tensor harmonics. On the
complete coefficient-atomic ball of `span{I,X_x,X_y,X_z}`,

```text
||J_{L->L+1}(AB)-J(A)J(B)||_op <= 8/[3(L+2)].
```

The associated low-mode screen experiment has cutoff-independent response
separation `1/3` and constant sample complexity. A highest-mode witness shows
that the full matrix unit ball has multiplicativity defect tending to `1/2`,
so the low-mode domain is necessary.

## 7. Controlled Limit And No-Go

The canonical harmonic inclusion preserves `ell`, `m`, both constraints, and
heat dynamics on finite support. Its strong limits are

```text
full:        B(l2{ell,m}), Type I_infinity,
time blind:  product_ell M_{2ell+1}, atomic Type I,
diagonal:    l_infinity{ell,m}, abelian.
```

This proves convergence but also rules out a gravitational interpretation of
the one-particle limit. A Type-II static-patch algebra requires a many-body or
local-QFT algebra whose modular action becomes outer, followed by a physically
derived clock crossed product and trace.

There is a second order-of-limits obstruction. At every finite matrix cutoff,
modular automorphisms are inner. Crossing an inner cyclic clock action gives

```text
M_d crossed Z_q = direct_sum_q M_d,
```

which is still finite Type I and is not a factor when `q>1`. The gravitational
type cannot be inferred by attaching a finite clock independently at each
matrix cutoff. The non-Type-I local limit and outer modular action must be
controlled before, or jointly with, the crossed product.

### 7.1 Many-Body Modular Surrogate

A state-derived non-Type-I mechanism can be realized on the qubit UHF chain.
Give odd and even sites faithful Gibbs states with gaps `1` and `sqrt(2)`, and
use the canonical embeddings `A -> A tensor I` with product-state conditional
expectations. State consistency and modular covariance are exact at every
finite cutoff.

The recurrent two-site block has asymptotic ratio group generated by
`exp(-beta)` and `exp(-beta sqrt(2))`. Its closure is the positive reals, so
`S(M)=[0,infinity)` and standard ITPFI/Connes classification gives the
hyperfinite Type-`III_1` factor. Its continuous modular core is hyperfinite
Type-`II_infinity` and has a faithful normal semifinite trace.

This resolves the algebra-type mechanism only in a thermal many-body
surrogate. It does not identify the UHF sites with fuzzy angular cells, derive
the product state from a static-patch path integral, or show that the edge
conditional expectation extends to the core.

### 7.2 Factorized Core-Stable Edge Obstruction

There is an exact baseline coupling. Tensor the relational angular matrix
algebra with the Type-`III_1` factor and use the product state

```text
M_L=M_{(L+1)^2} tensor R_III1,
Phi_L=tau_L tensor phi.
```

The modular flow is trivial on the angular factor, so the continuous core is

```text
M_{(L+1)^2} tensor C_phi,
```

a Type-`II_infinity` factor. Every time, time-then-axial, or full-rotation
conditional expectation extends as `E tensor identity_{C_phi}` and preserves
the core trace. Axial averaging alone would retain cross-`ell` multiplicity
blocks; the diagonal range is the composed time-then-axial operation. The
crossed-product clock cannot restore a discarded angular coefficient.

For a normalized nonzero finite-trace core projection `omega`, the lifted phase
pair still has input trace distance `1`, coincident time-then-axial expected
outputs, and decoder error at least `1/2`. Its relative entropy to the expected
state is

```text
D(rho tensor omega || E_{t,phi}(rho) tensor omega)=log 2.
```

For full orientation loss of a pure state in `V_L`, the corresponding value is

```text
log(2L+1).
```

This gives a state-weighted core obstruction rather than a parameter count.
The result is still factorized: the thermal sector is a spectator and no
static-patch interaction or generalized-entropy identity is derived.

### 7.3 Symmetry-Preserving Interacting Boundary State

The spectator assumption can be removed at a finite boundary. Couple the
fuzzy Casimir to the first thermal qubit through

```text
H_B=a K_L+Delta n_1+g K_L n_1,
rho_B proportional exp(-beta H_B).
```

For `L>=1`, `beta>0`, and the declared domain `g>0`, the first-site excitation probability
depends on `ell`; the Gibbs distribution has analytically positive mutual
information `I(ell:n_1)`. The boundary state is therefore non-product, though
the commuting interaction creates classical correlation. Because it is a rotational
scalar, it commutes with full `SU(2)` and protects magnetic degeneracy.

After absorbing the first qubit into the finite boundary factor, the untouched
alternating tail remains Type-`III_1`. Exterior equivalence through the
boundary-density cocycle identifies the crossed product, relative to the
declared tensor split, with a Type-`II_infinity` matrix amplification of the
tail core. The angular expectations preserve the boundary density and matrix
trace, so they extend trace-preservingly.

In a fixed `ell=L` sector the interaction is scalar in `m`, so normal probe
states in the KMS representation retain

```text
1/2,  log 2,  log(2L+1),
```

for decoder error, time-then-axial loss, and full-orientation loss respectively.
The invariant KMS background itself has zero loss. This is an interacting KMS
boundary model, but not yet a local field theory or geometric static-patch
construction.

The mechanism is bath independent. If the bath transforms trivially under
rotations, Schur's lemma forces every invariant Hamiltonian on a fixed sector
to be `I_{V_L} tensor H_{bath,L}`. Hence the `1/2` recovery lower bound and
`log(2L+1)` orientation probe entropy do not depend on bath dynamics or
interaction strength. A scalar bath cannot act as the missing orientation frame; avoiding
the obstruction requires charged reference degrees of freedom, symmetry
breaking, or altered representation content.

### 7.4 Charged Invariant-Subsystem Baseline

Let `d=2L+1` and give an auxiliary system the representation

```text
R_L=V_L^* tensor K,  dim(K)=d.
```

The isometry

```text
W|k>=|Omega_L>_{V_L,V_L^*} tensor |k>_K
```

maps a logical `d`-level system into the `SU(2)`-invariant subspace. That
subspace is the fixed singlet tensored with `K`, so its invariant logical
algebra is `B(K)=M_d`; discarding the singlet factors gives an exact decoder.
For a general auxiliary representation `direct_sum_j V_j tensor C^{m_j}`, the
invariant multiplicity is `m_L`. Exact encoding of all `d` logical states
by a pure isometry into total spin zero requires `m_L>=d`, hence auxiliary
dimension at least `d^2`, saturated by the block above. The full fixed operator
algebra is instead `direct_sum_{J=0}^{2L} B(K)`; `B(K)` is its singlet corner.
Tensoring the code with the common KMS/core density gives only spectator-factor
stability of these finite representation-theoretic statements.

This is not yet the desired charged-reference recovery theorem. The map `W` is
a global noncovariant pre-encoding, not the physical channel obtained from an unknown
`rho_S` by appending a fixed reference state `eta_R`, imposing the symmetry, and
decoding with allowed covariant operations. The operational problem must bound
the best recovery error in terms of reference charge, dimension, and energy.

### 7.5 Operational Finite Phase Reference

The axial `U(1)` version of that operational problem is exactly solvable. Append
the fixed reference

```text
|eta_N>=(N+1)^(-1/2) sum_{n=0}^N |n>,
```

apply the joint twirl, and decode each conserved total-charge sector. The
induced logical channel is the Schur multiplier

```text
rho_{m,m'} -> max(0,1-|m-m'|/(N+1)) rho_{m,m'}.
```

For a phase pair with gap `Delta`, every deterministic decoder has worst-case
trace-distance error at least `(1-v_Delta)/2`, and the sector decoder attains
the bound. For the extremal gap `2L`, the uniform reference has error
`min(1/2,L/(N+1))`.

The uniform scaling is not fundamental. At fixed maximum reference charge `N`,
the pairwise-optimal state is a sine eigenvector on the longest step-`Delta`
charge chain. If `r=floor(N/|Delta|)+1`, then

```text
v_opt=cos(pi/(r+1)),
error_opt=[1-cos(pi/(r+1))]/2.
```

For `|Delta|=2L`, the optimal pairwise error is `Theta((L/N)^2)`. These are
standard finite-reference mechanisms and solve only an axial two-state task;
they do not give the full `SU(2)` directional channel or a full-space diamond
optimum.

### 7.6 Single-Irrep Directional Reference No-Go

The first full-rotation result is negative. For a spin-`L` system and one
spin-`J` reference in any fixed product state, with no accessible multiplicity
ancilla,

```text
V_L tensor V_J = direct_sum_{K=|L-J|}^{L+J} V_K
```

is multiplicity-free. The joint `SU(2)` twirl therefore has fixed algebra
`direct_sum_K C I_{V_K}` and measure-and-prepare form over the total-spin
projectors. It is entanglement-breaking regardless of `J` or the reference
state.

Let `d=2L+1`. Any decoder composed with this channel remains
entanglement-breaking. A maximally entangled witness then gives the normalized
diamond recovery bound

```text
(1/2)||D E_eta - identity||_diamond >= 1-1/d.
```

Thus nontrivial rotation charge is necessary but not sufficient for full
observer-algebra recovery. A useful reference must also provide irrep
multiplicity, as in a reducible Peter-Weyl approximation. A large coherent spin
can still be effective for restricted direction-estimation tasks; the theorem
rules out deterministic recovery of the entire quantum spin sector.

### 7.7 Operational Reducible Rotation Reference

The multiplicity obstruction also has a constructive counterpart. For a general
reference `R=direct_sum_j V_j tensor C^{m_j}`, the joint decomposition has
multiplicities

```text
n_K=sum_j m_j 1{|L-j|<=K<=L+j}.
```

If `r=max_K n_K` and `d=2L+1`, the twirled Choi state has Schmidt number at most
`r`, giving the universal lower bound

```text
(1/2)||D N_eta-identity_d||_diamond >= max(0,1-r/d).
```

No finite prepared reference permits exact deterministic full-sector recovery:
the continuous Knill-Laflamme kernel is nonzero near the identity, where the
target rotation is not scalar.

For a positive treatment, use the integer-spin `SO(3)` Peter-Weyl cutoff,
equivalently the center-blind part of `SU(2)` for conjugation on the target
operator algebra,

```text
R_J=direct_sum_{j=0}^J V_j tensor V_j^*,
U_R(g)=direct_sum_j U_j(g) tensor identity.
```

The canonical token state and covariant POVM produce a decoded random-rotation
channel with exact tensor-rank multiplier

```text
lambda_k(J)=
 sum_{j,l<=J}(2j+1)(2l+1)1{|j-l|<=k<=j+l}
 /[(2k+1)D_J].
```

For `k<=2J`, its deficit is

```text
k(k+1)[12J(J+2)-k(k+1)+11]/[6(2k+1)D_J].
```

Consequently, for every fixed target spin, the explicit decoder converges in
diamond norm as `J` grows, while exact finite recovery remains impossible. The
left-action Casimir cost is `3J(J+2)/5`. This is a genuine operational
control/treatment theorem, though the decoder is not proved optimal and the
convergence is not uniform in a target cutoff proportional to `J`.

### 7.8 Global Geometric Gibbs Type-I No-Go

There is a natural geometric attempt to replace the engineered qubit tail. Put
a positive-mass free boson on the spherical angular regulator, with

```text
omega_ell=sqrt(mu^2+ell(ell+1)/R^2),
H_L=sum_{ell<=L,m} omega_ell a^*_{ell,m}a_{ell,m}.
```

This attempt fails for a precise reason. Since `omega_ell>=ell/R`, the omitted
log partition function is bounded by

```text
q^(L+1)[(2L+3)-(2L+1)q]/(1-q)^3,
q=exp(-beta/R).
```

The cutoff Gibbs densities, embedded with the omitted modes in their vacuum,
converge in trace norm to a trace-class density on the full angular Fock space.
For the declared global observable algebra `B(Fock)`, the GNS algebra is Type I
and its modular action is inner. Its crossed product has diffuse center and is
not the gravitational Type-II factor. For a noncompact massless scalar, the
constant mode is a free-particle degree of freedom with divergent thermal trace,
not a Type-III mechanism.

Thus the non-Type-I mechanism cannot come from angular cutoff removal in the
global Fock algebra alone. It must retain local net structure. In a faithful
four-dimensional static-patch realization, the radial/redshift limit is visible
in the optical volume divergence `V_opt(delta)~pi R^4/delta`, which must be
controlled before the observer clock crossed product.

### 7.9 Static-Patch S-Wave Covariance Refinement

The first geometric replacement keeps the radial/redshift limit. For a
conformally coupled massless scalar in four-dimensional de Sitter, the rescaled
s-wave has zero potential in `x=R artanh(r/R)`. A Dirichlet wall at radial gap
`delta` gives

```text
X_delta=(R/2)log[(2R-delta)/delta],
omega_n=n pi/X_delta.
```

At the de Sitter inverse temperature `beta=2 pi R`, the UV-truncated equal-time
variance of one compactly supported rescaled-field smearing is a right Riemann
sum with mesh `pi/X_delta`; it converges to the corresponding half-line
integral as `delta` tends to zero. This is local covariance convergence rather
than global density-matrix convergence, so it follows the topology required by
the order-of-limits gate identified in Section 7.8 without yet completing that
gate.

The statement is intentionally narrow. The reflecting finite boxes are Gibbs
approximants, not literal Bunch-Davies restrictions, and one equal-time variance
does not construct a quasifree Weyl state. Section 7.11 supplies projected
phase-space covariance and unequal-time KMS control at fixed UV cutoff. Smooth
UV removal, locality, angular sectors, the local GNS algebra, and factor type
remain to be proved.

### 7.10 Redshifted Rotational-Frame Capacity

The near-horizon geometry nevertheless yields a first quantitative physics
law. For angular momentum `ell`, the conformal scalar radial operator is

```text
h_ell=-d^2/dx^2+ell(ell+1)/(R^2 sinh^2(x/R)).
```

Translate one normalized Dirichlet sine packet with a fixed-width tortoise
collar below the stretched horizon. Its kinetic form is fixed, while the
angular potential is redshifted. Rayleigh-Ritz turns the collar form bound into
an actual finite-wall eigenstate below every fixed static-energy budget `E0`
above the packet's kinetic floor, for all irreps through

```text
L_delta=Theta(sqrt(R/delta))
```

Choosing one such eigenstate per spin, a pure coherent directional token with irrep weight
`(2ell+1)/(L_delta+1)^2` twirls to the maximally mixed state on its
rank-`(L_delta+1)^2` support. Its exact relative entropy of
frameness is therefore

```text
2 log(L_delta+1)=log(R/delta)+O(1)
                =log[A/(2 pi rho^2)]+O(1).
```

This is a geometry-derived capacity lower bound: bounded finite-wall Killing
energy does not bound the available rotational-frame information uniformly as
the wall approaches the horizon. It is not yet an observer no-go. That step
requires proving a compact conditional expectation and its extension through a
named observer crossed product. Relating the same logarithm to
generalized entropy additionally requires a trace-preserving extension to the
physical Type-II algebra. Backreaction and local proper-energy constraints may
cut off the family and must be analyzed explicitly.

### 7.11 Fixed-UV Canonical Phase-Space KMS Limit

The equal-time scalar benchmark can be upgraded without claiming a local net.
For compactly supported s-wave Cauchy data `F=(f,g)`, retain Dirichlet modes
`k_n=n pi/X_delta<=K`. Their projected symplectic form and quasifree covariance
are

```text
sigma_delta,K(F,G)=sum_n(f_n g_G,n-g_n f_G,n),

mu_delta,K(F,G)=1/2 sum_n coth(beta k_n/2)
 [f_n f_G,n/k_n+k_n g_n g_G,n].
```

Using the unitary half-line sine transform gives the exact coefficient identity
`f_n=sqrt(pi/X_delta) fhat(k_n)`. Both forms are therefore ordinary Riemann
sums and converge at fixed `K`. The apparent thermal singularity at zero
frequency is removable on compact tests. Modewise positivity gives the
quasifree uncertainty inequality, while the unequal-time two-point function
satisfies the exact KMS boundary condition at `beta=2 pi R` and converges to
the corresponding fixed-band continuum integral.

This closes the canonical phase-space and unequal-time gap left by Section
7.9, but only in a bandlimited quotient. A hard UV cutoff is nonlocal, so the
result still does not construct the Bunch-Davies local Weyl net or determine
its factor type.

### 7.12 S-Wave Ultraviolet Removal

The hard bandlimit can be removed quantitatively. For compact s-wave Cauchy
data whose `n`-th distributional derivatives are finite measures, `n>=2`,
integration by parts gives `k^-n` sine-transform decay. The omitted covariance
tail is bounded by

```text
1/2 coth(beta K/2)
[A_f A_u/(2n K^(2n))
 +A_g A_v/((2n-2)K^(2n-2))],
```

with analogous explicit symplectic and unequal-time bounds. The unequal-time
estimate is uniform on the closed KMS strip, so the KMS boundary identity
survives the limit. An independent linear small-`k` sine-transform bound removes
the thermal infrared singularity.

The executable `C^2` cubic bumps have finite fourth distributional derivative
measure. Their worst thermal tail is therefore `O(K^-6)`, while smooth compact
data have superalgebraic tails. The same estimate shows that equal-time
symplectic leakage between disjoint supports, introduced by bandlimiting,
vanishes in the UV limit.

Together with Section 7.11 this proves the iterated wall-removal followed by UV
removal and supplies selected diagonal refinements. It does not prove
convergence along every arbitrary joint path. The resulting object is the full
s-wave quasifree KMS phase space. The next section closes the all-angular
equal-time wall limit, but not the Lorentzian Hadamard or local factor theorem.

### 7.13 All-Angular Equal-Time Wall Limit

For the conformally coupled massless scalar, the optical static patch is
`R x H^3_R`. Spherical decomposition gives

```text
h_(ell,X)=-d^2/dx^2+ell(ell+1)/(R^2 sinh^2(x/R)).
```

The angular potential vanishes at the horizon, so every half-line `h_ell` has
spectral bottom zero. There is no global high-`ell` Killing-energy gap. The
relevant local estimate is instead

```text
||1_(0,B)1_[0,E^2](h_ell)||
 <=min(1,E R sinh(B/R)/sqrt(ell(ell+1))).
```

For compactly supported field data with angular `H^s(S^2;L^2_x)` norm, the
field-covariance tail beyond `L` is bounded uniformly in the wall by

```text
[4B^2/(beta pi^2)+beta/12]
[1+(L+1)(L+2)]^(-s)||f||_(s,0)^2.
```

Momentum data with common compact radial support require the stronger
energy-weighted angular form norm

```text
sum_(ell,m)(1+ell(ell+1))^s
[beta q_ell[g_(ell,m)]/8+3||g_(ell,m)||^2/(2beta)].
```

Its omitted covariance obeys the same angular factor. Fixed-`ell` domain
exhaustion, treated separately for the inverse field multiplier and the
square-root momentum multiplier, plus these uniform tails proves full
all-angular equal-time finite-wall covariance convergence.

The exact Darboux continuum modes satisfy a stable three-term angular
recurrence. Their sampled partial-wave sum matches the closed Euclidean
optical thermal kernel, and the exact conformal pullback equals the Euclidean
Bunch-Davies kernel. The sample is a numerical audit; the convergence theorem
comes from the wall-uniform Sobolev tails.

This closes the equal-time angular wall-removal gate. The next section promotes
it to the Lorentzian Bunch-Davies net; the gravitational observer corner remains
separate.

### 7.14 Lorentzian Hadamard Net And Free-Field Core

For optical distance `d_H`, the lower-strip thermal kernel is

```text
G_opt(z)=1/[8 pi^2 R^2
 (cosh(d_H/R)-cosh(z/R))],
-2 pi R<Im z<0.
```

Its positive-type spectral representation has zonal kernel

```text
sin(k d_H)/[4 pi^2 R sinh(d_H/R)]
```

times the Bose KMS factor. The opposite strip boundaries satisfy the exact
`beta=2 pi R` KMS relation. Conformal pullback gives the Lorentzian boundary

```text
Lambda_BD^+=1/[8 pi^2 R^2(1-Z_(Delta t-i0))].
```

For arbitrary compact spacetime tests, Green's identity produces smooth
compact Cauchy data. Once the stretched wall lies outside their bounded causal
hull, finite propagation makes those data independent of the wall. Section
7.13 therefore proves pairwise convergence of the finite-wall two-point forms
on compact spacetime tests. Full distribution-topology convergence requires an
additional equicontinuity estimate.

The limiting kernel is the standard Bunch-Davies Hadamard distribution. The
wavefront-set statement is imported from the established Hadamard/
microlocal-spectrum theorems for passive KMS states, not inferred from a
pointwise short-distance fit. In the global de Sitter Bunch-Davies
representation, Verch's local theorem then identifies regular-diamond algebras,
including the static patch, with the hyperfinite Type `III_1` factor.
The patch modular flow is geometric static time, so its continuous core is
hyperfinite Type `II_infinity`.

This is the free-field local net and its mathematical core. It is not yet the
gravitational Type-`II_1` observer algebra: that requires a clock/reference
system, Hamiltonian constraint, positive-energy projection, finite trace, and
an entropy interpretation.

### 7.15 Energy-Constrained Rotational Frameness Obstruction

Any full de Sitter gauge completion must contain the compact `SO(3)` stabilizer
of the static observer. Suppose its only accessible observer reference is a
rotation-trivial scalar clock and every spectator is rotation invariant. Then
physical compact-subgroup observables lie in the `SO(3)` fixed-point algebra;
the canonical conditional expectation realizes this restriction as a channel.

The near-horizon collar theorem and min-max principle supply actual finite-wall
eigenstates through `L_delta=Theta(sqrt(R/delta))` in a fixed hard static-energy
window. In the highest sector, the orthogonal states with magnetic labels
`m=+L_delta` and `m=-L_delta` share the same radial eigenstate and have
identical `SO(3)` expectations.
Every decoder therefore has worst-case trace-distance error at least `1/2` on
this pair. Recovery of the complete spin sector has exact optimal normalized
diamond error `1-1/(2L_delta+1)^2`, which tends to one, while a coherent token over the
available sectors loses `log(R/delta)+O(1)` relative entropy of frameness.

This is a conditional compact-fixed-point obstruction rather than a construction
of the full noncompact constraint. CLPW already identifies the qualitative need
for an orthonormal frame in addition to the clock. The candidate contribution is
the hard-energy scaling and exact recovery law. Extending the expectation
through a named crossed product or gravitational corner still requires a
commuting-square and nonzero-support theorem. A
covariant observer carrying a nontrivial `SO(1,d)` representation is the direct
escape route and lies outside the theorem.

### 7.16 Charged-Reference Achievability Bound

The compact positive comparison can be performed on the same hard-energy spin
sector. Append the prepared Peter-Weyl orientation reference

```text
R_J=direct_sum_(j=0)^J V_j tensor V_j^*
```

and use its canonical covariant orientation POVM followed by correction. The
closed tensor-rank multiplier formula gives the constructive channel bound

```text
(1/2)||Lambda_(L,J)-identity||_diamond
 <= 3(2L+1)^2/(8J).
```

Consequently `J=ceil[3(2L_delta+1)^2/(8 epsilon)]` guarantees error at most
`epsilon`, while the canonical compact expectation under the invariant-spectator
clock-only hypothesis approaches unit error on the same target. If the reference
is assigned the rigid-rotor Hamiltonian `C_left/(2I)`, its canonical token has
mean energy `3J(J+2)/(10I)`. The redshifted target therefore gives the sufficient
resource scaling

```text
J=O(R/(epsilon delta)),
E_ref=O(R^2/(I epsilon^2 delta^2)).
```

This completes a compact `SO(3)` same-target comparison, not a resource-matched
experiment. The energy law assumes `I` is fixed independently of the wall and
target error. The bound is not claimed optimal, the coherent rotor lifetime is
uncontrolled, and neither `I` nor the Hamiltonian has been derived from a
gravitational observer. The full problem is to obtain the reference dynamics,
boost sector, and backreaction bound from a covariant static-patch construction.

### 7.17 Covariant-Observer Energy Identifiability No-Go

The missing dynamical input cannot be reconstructed from covariance and channel
accuracy. Keep the compact Peter-Weyl representation, canonical token,
orientation POVM, and decoder fixed. For every `a_J>0`, the positive Hamiltonian

```text
H_J=a_J C_left
```

commutes with rotations and leaves the instantaneous recovery channel unchanged.
Because the token has `<C_left>=3J(J+2)/5`, any prescribed positive
ground-subtracted energy `E_J` is realized by

```text
a_J=5E_J/[3J(J+2)].
```

Thus the same kinematic observer data and recovery certificate admit dynamically
inequivalent Hamiltonian completions with incompatible energy scalings. The
fixed-`I` `delta^-2` result remains valid inside that declared rotor model, but
it is not selected by the observer algebra.

This conclusion matches a direct audit of Chen and Xu's covariant-observer
proposal [arXiv:2511.00622v2](https://arxiv.org/abs/2511.00622v2). Their explicit
`dS_2` action couples conserved de Sitter charges to the worldline, while the
higher-dimensional orthogonal frame is introduced kinematically on
`L^2(SO(1,d))`. No rotational kinetic term, finite-size inertia, or positive
compact-frame Hamiltonian is specified there. The present result identifies that
missing input; it does not exclude their construction.

The no-go is restricted to compact rotations and an instantaneous protocol. It
does not say that physical reference frames have arbitrary energy, and the
different coefficients are different dynamical completions. A finite-size
worldline/tetrad action, local coupling, state-preparation and lifetime analysis,
and gravitational stress-energy bound would narrow the model and can produce a
genuine energy-accuracy theorem.

### 7.18 Finite-Size Static-Patch Rotation Observer

We now choose one compact phenomenological EFT ansatz. Let the observer carry a marked
spherical top of proper radius `a`, rest energy `m`, and orientation
`Q(tau) in SO(3)`, with

```text
S_obs=integral d tau[-m+I|Q^-1 D_tau Q|^2/2],
I=kappa m a^2,  0<kappa<=2/3.
```

Quantization gives `L^2(SO(3))` and `H_rot=C_left/(2I)`. For the canonical
Peter-Weyl token this reproduces the earlier rotor cost, but the physical
statement is made for an arbitrary prepared state `eta`. Write
`Cbar=Tr(eta C_left)` and impose the explicit semiclassical control conditions

```text
E_rot/m<=zeta<=1,
2G(m+E_rot)/a<=chi<1.
```

Maximizing `Cbar=2 kappa m a^2 E_rot` under these inequalities gives

```text
Cbar
 <= kappa chi^2 zeta a^4/[2G^2(1+zeta)^2].
```

This is a mean-Casimir bound, not a truncation of `L^2(SO(3))`. Let `P_J`
project to spins `j<=J`. The omitted probability is at most
`Cbar/[(J+1)(J+2)]`, and the normalized projected state is within trace distance
the square root of that quantity. Combining channel contractivity with the
exact finite Peter-Weyl multiplicity obstruction implies, for every
deterministic decoder after the fixed prepared-reference append-and-twirl
channel,

```text
epsilon_opt(L)
 >= max_(J>=0) max{0,
      1-(J+1)^2/(2L+1)
       -sqrt[Cbar/((J+1)(J+2))]}.
```

Uniformly optimizing gives
`epsilon_opt>=1-O[1/(2L+1)+(Cbar/(2L+1))^(1/3)]`. On the hard-energy
horizon sector `L=L_delta=Theta(sqrt(R/delta))`, this tends to one for every
fixed finite observer. The theorem includes arbitrary high-spin tails satisfying
the mean-energy budget. It excludes pre-correlated encoders, postselection,
other reference hardware, and general finite-time evolution during the protocol.
Section 7.19 treats one conditional collective Markov extension.

For the collar-following branch, impose that the apparatus size scales as
`a_delta=alpha rho_delta`, so its mean-Casimir capacity decreases as
`O(R^2 delta^2/G^2)`. For the canonical hard-cutoff token, imposing the stronger
branchwise spectral condition gives a safe occupied spin
`J_spec=O(R delta/G)`. Comparing that support with the sufficient cutoff of
Section 7.16 gives the protocol-specific scales

```text
delta_protocol=Theta(sqrt(G/epsilon)),
rho_protocol=Theta(sqrt(R sqrt(G)) epsilon^(-1/4)).
```

The all-angular interior-overlap theorem supplies the other branch of a
conditional access-capacity fork: a fixed interior worldtube has overlap only
`O(sqrt(delta/R))` with the high-spin collar target. A finite-time channel
consequence still requires a local interaction. The compactness condition is
also a declared worldtube hypothesis, not a rotating Einstein-matter theorem.
The result does not include arbitrary reference multiplicity hardware,
noncompact boosts, the Type-II observer trace, or generalized entropy.

### 7.19 Finite-Time Collective Rotation Diffusion

The instantaneous Haar map can be replaced by a finite-proper-time channel in
a conditional active common-mode noise model. Assume
`[H_target+H_rot,Q_a]=0`, or a specified toggling control making the
interaction-picture charges constant, and define

```text
Q_a=J_a^(target)+J_a^(rotor,left),
d rho/d tau=-gamma sum_a[Q_a,[Q_a,rho]].
```

The solution is convolution with the central `SO(3)` heat kernel:

```text
N_(eta,T)(rho)=integral dg k_(gamma T)(g)
 U_L(g)rho U_L(g)^* tensor U_R(g)eta U_R(g)^*.
```

It starts at `rho tensor eta` and converges to Haar append-and-twirl. If
`q=exp(-4 gamma T)`, a signed-random-unitary estimate and character
orthogonality give the representation-independent bound

```text
(1/2)||N_(eta,T)-N_(eta,infinity)||_diamond
 <= min{1,(1/2)sqrt[q(9-2q+q^2)/(1-q)^3]}
 =:eta_heat(gamma T).
```

Consequently, for decoders acting only on the target-plus-rotor output without
the Brownian record, bath output, or bath purification, the all-state result of
Section 7.18 transfers to finite time:

```text
epsilon_T>=max{0,epsilon_Haar(Cbar,L)-eta_heat(gamma T)}.
```

The sufficient choice `gamma T=(1/2)log(2L+1)` makes the finite-time correction
`O(1/L)`. If `gamma` is cutoff independent, then on
`L_delta=Theta(sqrt(R/delta))` it gives

```text
T_delta=Theta[gamma^-1 log(R/delta)].
```

This is a sufficient protocol-time upper bound, not a necessary mixing law or
observable prediction. It does not yet derive the physical measurement channel.
The common generator requires a rank-one spatial covariance kernel giving
perfectly correlated equal-strength active orientation noise on target and
rotor. Ordinary environmental torque diffuses the rotor alone, and passive
uncertainty about a frame is only coarse graining. The exact Stratonovich white-
noise model has infinite bandwidth. A paper-grade local theorem must derive a
finite-bath Markov limit and subtract Davies/coarse-graining, common-mode
projection, collar-access, lifetime, and backreaction errors.

### 7.20 Common-Mode Locality Mismatch

The ideal collective channel is sharply distinguishable from generic
imperfectly correlated noise. Consider one axial charge on the target and
reference with normalized noise covariance `C=[[1,c],[c,1]]` and exchanged
axial charge gap `Delta>0`. The relational coherence
`(|1,0>+|0,1>)/sqrt(2)` has exact visibility

```text
v(gamma T,c)=exp[-2 gamma T Delta^2(1-c)].
```

It is decoherence free at perfect common mode `c=1`. Comparing its actual output
with the ideal common-mode output gives

```text
(1/2)||Phi_C,T-Phi_*,T||_diamond
 >= [1-exp(-2 gamma T Delta^2(1-c))]/2.                 (20)
```

If the sufficient heat schedule `gamma T=(1/2)log d` is used and the covariance
mismatch is allocated error `A/d`, (20) requires

```text
1-c <= -log(1-2A/d)/(Delta^2 log d)
     =O(1/[Delta^2 d log d]).                           (21)
```

For the illustrative finite-range form `c(r)=exp(-r/ell_B)` at fixed
target-reference separation, this implies
`ell_B/r=Omega(Delta^2 d log d)`. Hence a
fixed finite correlation length cannot justify the rank-one common mode along
the logarithmic protocol schedule. This is a falsification criterion for a
future local bath calculation, not yet a derivation of that bath. A
complementary finite-cell Duhamel estimate bounds the channel difference above
by the weighted entrywise covariance defect for bounded charge generators.

### 7.21 Bunch-Davies Scalar Common-Mode Obstruction

A named local bath can now be tested. Couple two equal-redshift localized axial
zero-Bohr charge components, with identical coupling normalization and
optically pointlike profiles, stationarily to the conformally coupled
Bunch-Davies scalar. From the exact optical spectral kernel, the normalized
cross spectrum at zero Bohr frequency and optical separation `y=d_H/R` is

```text
c_0(y)=y/sinh(y).                                       (22)
```

The axial witness then gives

```text
(1/2)||Phi_scalar,T-Phi_common,T||_diamond
 >= [1-exp(-2 gamma T Delta^2[1-y/sinh(y)])]/2.          (23)
```

At every fixed `y>0`, the right side tends to `1/2` along growing protocol time.
With `gamma T=(1/2)log d` and an `A/d` error allocation,

```text
y=O(1/[Delta sqrt(d log d)]).                            (24)
```

For two supports at equal proper horizon distance `rho`, static-patch optical
geometry gives

```text
cosh(y)=1+2 cot^2(rho/R) sin^2(theta/2),
```

and hence

```text
theta=O[(rho/R)/(Delta sqrt(d log d))].                  (25)
```

On the declared collar sector `d=Theta(sqrt(R/rho))`, the allowed angular
separation shrinks as
`O((rho/R)^(5/4)/sqrt(log(R/rho)))` for fixed `Delta`. This rules out fixed
same-shell separation in the localized axial scalar-bath surrogate. It is not
yet a theorem for the distributed hard angular target or a finite spherical
top, and it omits nonradial torque, dissipative finite-time sectors, lifetime,
and backreaction errors.

Two-atom scalar-bath GKSL dynamics in the de Sitter static patch is prior work;
the scalar open-system coefficient itself is not claimed as new. The candidate
contribution is its use inside the finite-reference recovery and redshift
scaling problem.

### 7.22 Exact Radial-Smearing Invariance

The point-detector assumption can be removed for arbitrary finite radial
profiles in optical `H^3_R`. The zero-frequency kernel

```text
phi_0(y)=y/sinh(y)
```

obeys the spherical mean product formula

```text
M_u phi_0(r)=phi_0(u)phi_0(r).                           (26)
```

For nonnegative normalized radial profiles `mu_p,nu_q`, define their positive
spherical amplitudes `A_mu,A_nu`. Equation (26) gives

```text
B_pp=A_mu^2,
B_qq=A_nu^2,
B_pq=A_mu A_nu phi_0[d(p,q)/R].                         (27)
```

Consequently

```text
B_pq/sqrt(B_pp B_qq)=phi_0[d(p,q)/R]                    (28)
```

exactly, independent of radial size and shape. Even a collar-following body
with finite optical width cannot improve the common-mode correlation by radial
smearing. Thus the co-location laws (24)-(25) hold for the entire declared
optical-radial profile class, not only pointlike detectors.

At spectral parameter `p`, the same product formula gives
`phi_p(y)=phi_0(y)sinc(py)`. Hence, for any common nonnegative finite-switching
spectral weight, weighted Cauchy-Schwarz implies

```text
|c_eff(y)|<=phi_0(y).                                   (29)
```

Finite switching cannot improve the separated-center correlation in the radial
scalar pure-dephasing class. It changes the absolute rate and generally makes
the inequality strict. Equation (29) does not treat dissipative jump operators
or the noncommuting three-axis top.

The effective optical profile is `f_opt=Omega^3 J_physical`; optical radiality
is therefore a source-weight hypothesis rather than a generic property of a
rigid proper-metric body. The product formula is standard harmonic analysis.
Its role here is to close a finite-size loophole in the conditional observer
no-go. Nonradial torque multipoles, a matter realization of the conformal
source weights, dissipative
finite-time channels, and the full three-axis top remain outside the theorem.

### 7.23 Polarization-Resolved Gradient Coupling

A first three-component covariance calculation replaces the scalar monopole by
the conditional optical interaction

```text
H_I=lambda sum_a[L_a e_a.nabla Phi_opt(p)
                 +J_a e'_a.nabla Phi_opt(q)],
```

where the frames are related by parallel transport. Differentiating the exact
zero-frequency kernel gives the normalized cross Kossakowski matrix

```text
C(y)=diag(c_parallel,c_perp,c_perp),                    (30)
c_parallel=-3 phi_0''(y),
c_perp=-3 phi_0'(y)/sinh(y).
```

The coincident auto block is `I/(3R^2)`. The joint block is positive
semidefinite because `phi_0` is positive definite. In collective and relative
variables `Q_a=L_a+J_a`, `R_a=L_a-J_a`, each polarization has rate weights

```text
Gamma_Q,a proportional to 1+c_a,
Gamma_R,a proportional to 1-c_a.                       (31)
```

Every nonzero separation therefore produces relative rotational noise, and
the longitudinal/transverse split prevents equality with the ideal isotropic
collective heat generator. The small-distance laws are

```text
1-c_parallel=(7/10)y^2+O(y^4),
1-c_perp=(2/5)y^2+O(y^4).                              (32)
```

If the axial `A/d` allocation is imposed separately on these eigenchannels,
the longitudinal channel again requires

```text
y=O(1/[Delta sqrt(d log d)]).                           (33)
```

Equation (33) is a conditional axiswise diagnostic. A full noncommuting witness
can be solved exactly for two spin-half charges. Starting from the singlet, the
gradient channel remains in the Bell-diagonal sector

```text
rho(s)=[I+u(s)T_parallel
          +v(s)(T_perp,1+T_perp,2)]/4,

d/ds [u] = [-4       4 c_perp    ] [u],                 (34)
     [v]   [2 c_perp -4+2c_parallel] [v],
u(0)=v(0)=-1.
```

Let `m=-4+c_parallel` and
`kappa=sqrt(c_parallel^2+8c_perp^2)`. Matrix exponentiation gives

```text
u=e^(ms)[-cosh(kappa s)
 +(c_parallel-4c_perp)sinh(kappa s)/kappa],
v=e^(ms)[-cosh(kappa s)
 -(c_parallel+2c_perp)sinh(kappa s)/kappa].             (35)
```

The ideal collective channel fixes the singlet. The actual state is Bell
diagonal with singlet probability `p_S=(1-u-2v)/4`, so

```text
(1/2)||E_s-E_s^collective||_diamond >= 1-p_S.           (36)
```

At fixed `s` and small `y`,

```text
1-p_S=(3/2)s y^2+O(y^4).                               (37)
```

Along `s=(1/2)log d`, an `A/d` allocation therefore gives the leading
co-location law

```text
y<=sqrt[4A/(3d log d)].                                 (38)
```

This is an exact finite-time three-axis channel witness in the spin-half
sector. The next subsection extends the same singlet witness to arbitrary
integer spin inside the effective channel.

This closes the simplest external-axis loophole at the generator-covariance
level, but it is not a mechanical spherical-top torque theorem. For an ordinary
scalar `J.nabla Phi` is parity odd, and the direct physical gradient contains
additional conformal terms. Smooth derivative smearing, the hard target
current, a local finite-top matter action, finite-memory control, lifetime, and
backreaction are still required.

### 7.24 Casimir-Enhanced Growing-Spin Witness

For equal integer spin `L`, the singlet projector decomposes into one scalar
component in every equal irreducible-tensor block. Axial anisotropy preserves
zero total magnetic number, giving the exact survival formula

```text
p_L(s)=sum_(ell=0)^(2L) (2ell+1)/(2L+1)^2
       <s_ell|exp(s B_ell)|s_ell>,                      (39)
```

with `s_ell,m=(-1)^(ell-m)/sqrt(2ell+1)` and

```text
(B_ell)_(m,m)=-2ell(ell+1)+2c_parallel m^2,
(B_ell)_(m+1,m)=-c_perp(ell-m)(ell+m+1).                (40)
```

This replaces a `d^4` Liouvillian by tridiagonal blocks of maximum size
`4L+1`. More importantly, the singlet variance gives the exact finite-time
first variation

```text
1-p_L(s)=(4/3)L(L+1)s Delta+R_L,
Delta=(1-c_parallel)+2(1-c_perp),                       (41)
```

and the Hilbert-Schmidt Duhamel estimate gives

```text
|R_L|<=32s^2L^4Delta^2.                                 (42)
```

Using `Delta=(3/2)y^2+O(y^4)`,

```text
1-p_L(s)=2L(L+1)s y^2
 +O(sL^2y^4+s^2L^4y^4).                                (43)
```

When the protected sector dimension is `d=2L+1`, the sufficient schedule
`s=(1/2)log d` and an `A/d` allocation require

```text
y<=sqrt[A/(dL(L+1)log d)]
 =O[d^(-3/2)/sqrt(log d)].                              (44)
```

At this scaling the expansion parameter `sL^2Delta` is `O(1/d)`, so (44) lies
inside the controlled regime. The strengthening from `d^-1/2` to `d^-3/2`
comes from the singlet relative-charge variance `4L(L+1)/3`.

Equation (44) is an exact-channel obstruction inside the declared Markovian
model, but the singlet is an entangled diamond-norm probe. A product-prepared
reference theorem, a local finite-top action, a Davies limit uniform in `L`,
and gravitational stress/lifetime control remain open.

### 7.25 Local Pseudoscalar Gyroscope

A minimal parity-consistent completion of the top-side interaction uses a
conformally coupled pseudoscalar and the phase-space action

```text
S_top=int d tau[-m+(I/2)|varpi^a-g B^a|^2],
B_a=e_a^mu(nabla_mu chi+a_mu chi).                      (45)
```

The Hamiltonian contains `gJ_a^left B_a`, and all three `J_a^left` commute with
the invariant rotor Hamiltonian. Unlike the ordinary scalar-gradient ansatz,
equation (45) is parity even.

With `g_dS=N^2g_opt` and `chi_dS=N^-1chi_opt`, the acceleration improvement
gives

```text
N^2(nabla_hat^dS chi_dS+a_hat^dS chi_dS)
=D_hat^opt chi_opt.                                    (46)
```

At equal redshift, normalized correlations are therefore exactly those of
Sections 7.23-7.24. This derives the localized rotor-side operator rather than
postulating `J.nabla Phi_opt` directly. It selects the static congruence and
breaks pseudoscalar shift symmetry.

The absolute rate exposes a new obstruction. Since `tau=Nt`,

```text
S_tau(0)=N^-3S_opt(0),
tau_B=N tau_B,opt,
gamma_tau tau_B=g^2N^-2S_opt(0)tau_B,opt.               (47)
```

For a growing spin-`L` sector, the loaded parameter acquires `L(L+1)`. Fixed
coupling is therefore incompatible with a Davies approximation uniform in the
collar and spin limits. If a smooth optical smearing is fixed and an interaction
RMS is imposed on a declared spin-sector reference state, then

```text
g=O[N^2/sqrt(L(L+1))],
gamma_tau=O[N/L(L+1)],
T_schedule=Theta[L(L+1)log(d)/N].                       (48)
```

On `N~1/d`, equations (44) and (48) give

```text
T_schedule=Theta[d^3 log d],
theta=O[d^(-5/2)/sqrt(log d)].                         (49)
```

Here `T_schedule` is the duration of the selected sufficient logarithmic heat
schedule, not a necessary mixing-time lower bound. The RMS premise is state
dependent and is not an operator-norm bound. This completes a local top-side
candidate and a quantitative schedule/locality tradeoff, but not the hard-
target reduction. A distributed target couples as
`int B_a(x)ell_T^a(x)`; the next section bounds its multipoles and nonzero-Bohr
sectors conditionally relative to the global `B(p)L_a` surrogate.

### 7.26 Distributed Hard-Current Multipoles

For a target current on a geodesically convex worldtube, parallel-transport bath
and current components to a chosen center frame and define
`L_a=int ellbar_a(x)`. The exact local-to-lumped difference is

```text
V-V_0=g sum_a int [Bbar_a(x)-B_a(p)]ellbar_a(x).        (50)
```

On a declared product reference vector with bath Lipschitz constant `K`, the
interaction-vector remainder obeys

```text
||(V-V_0)psi|| <= |g| K M_1,
M_1=sum_a int r(x)||ellbar_a(x)psi_T||.                 (51)
```

A compressed-operator version additionally yields a finite-time diamond bound
`min(2,2T|g|KM_1)`, but (51) alone does not.

If `[H_T,L_a]=0`, each nonzero target Bohr sector has zero integrated monopole.
Thus

```text
V_omega=g sum_a int [Bbar_a(x)-B_a(p)]ellbar_a(x;omega),
omega != 0,                                             (52)
```

and is controlled by its own sector first moment. Linear dependence is sharp for
one conserved component: a two-cell `U(1)` spin-half current with cancelling
local `sigma_x` terms saturates the `|g|Ka` interaction bound.

The interaction-vector estimate does not itself control the Davies jump map.
Add separate transfer hypotheses for the zero-Bohr linear jump error, the
aggregate squared norm over every nonzero gap, and the zero-Bohr second-order
jump error. For a normalized
diagonal-jump finite-dimensional surrogate with unit rates, no Kossakowski
mixing, and no Lamb-shift perturbation, the GKSL identity gives

```text
delta_0<=3sL^2(4epsilon_0+2epsilon_0^2),
delta_nz<=6sL^2epsilon_nz^2.                           (53)
```

The second bound assumes strict secular separation; its aggregate transfer must
include any growth in the number or continuum of gaps. At `s=(1/2)log d` and channel allocation
`A/d`, the certificate gives the sufficient worst-case design

```text
a_opt/R=O(d^-3/log d),
theta_support=O(d^-4/log d).                           (54)
```

If every transported compressed zero-Bohr current-dipole component vanishes as
an operator and a covariant Hessian bound makes the remainder quadratic, then
the nonzero-Bohr constraint and
nonoverlap at equation (44) instead give

```text
a_opt/R=O[d^(-3/2)/sqrt(log d)],
theta_support=O[d^(-5/2)/sqrt(log d)].                 (55)
```

The hard-target reduction is therefore a conditional design fork. The remaining
inputs are a matter-derived current moment and covariant bath regularity, an
interaction-to-jump/Kossakowski/Lamb-shift stability theorem, componentwise
dipole cancellation or use of the more conservative design (54), a QFT-uniform
Davies/secular theorem, and localization stress. Larger supports may work by
model-specific cancellations. Overlapping distinguishable sectors remove only
the nonoverlap part of (55).

### 7.27 Controlled Compactness-Localization Branch Obstruction

The support scales above can now be tested against the finite spherical-top
capacity, provided one makes the additional physical identification that the
top spin is the protected hard-sector spin `L` and its three-dimensional proper
enclosing radius is no larger than the tangential worldtube support. With

```text
I=kappa m a^2,   E_rot/m<=zeta,
2G(m+E_rot)/a<=chi,
```

the exact compactness radius floor is

```text
a_min=[2G^2(1+zeta)^2L(L+1)/(kappa chi^2 zeta)]^(1/4)
     ~C_min sqrt(G)d^(1/2),                              (56)
```

where `d=2L+1` and
`C_min=[(1+zeta)^2/(2kappa chi^2 zeta)]^(1/4)`.

Optical and proper support must not be identified. At `u=rho/R`, the exact
same-shell angle and static-slice center distance are

```text
theta=2asin[tan(u)sinh(y/2)],
D_slice=2R asin[cos(u)sin(theta/2)]
       =R sin(u)y[1+O(y^2)].                             (57)
```

On the collar `rho/R=1/d`, the leading local-common-mode law in equation (44)
and equal-radius thin-shell nonoverlap therefore give

```text
a_nonoverlap/R
 ~sqrt(A)d^(-5/2)/sqrt(log d).                           (58)
```

Combining (56) and (58),

```text
a_nonoverlap/a_min
 ~[sqrt(A)/C_min][R/sqrt(G)]d^(-3)/sqrt(log d).          (59)
```

At fixed `R^2/G`, this tends to zero. Thus no growing-`d` sequence can remain in
the controlled local perturbative common-mode branch while satisfying the
stipulated compact top and distinct equal-radius nonoverlap assumptions. This
does not control hypothetical nonperturbative large-separation behavior. The
controlled-envelope crossover is

```text
d^3sqrt(log d)=O(R/sqrt(G)).                             (60)
```

The sufficient hard-current designs close as well: their minimum-top
compactness utilization grows as `(G/R^2)d^9(log d)^2` in the generic branch and
as `(G/R^2)d^6log d` in the dipole-cancelled branch. Those are closures of
sufficient design certificates, not necessary failure bounds.

The distinction matters. Equation (58) imports a leading perturbative necessary
co-location law, so a finite integer obtained by crossing the envelopes is an
illustrative asymptotic crossover rather than an exact global channel cutoff.
For the certificate defaults, it occurs at `L=30` (`d=61`); the conservative
generic design closes at `L=6`. Neither number is a universal prediction. The
theorem also assumes `J_top=L_hard`, a thin-shell three-dimensional
enclosing-radius identification, `O(1)` transfer constants, and equal-radius
nonoverlap. It does not derive a global channel no-go, matter stress tensor,
lifetime, binding energy, uniform Davies limit, or Einstein-matter solution.

The compactness-side scaling is not new by itself. It is parametrically close
to Dain's general-relativistic size-angular-momentum inequality
([arXiv:1305.6645](https://arxiv.org/abs/1305.6645)), under different symmetry
and energy hypotheses. The candidate contribution is the collision with the
channel-derived upper support scale. The physical successor must also specify a
prepared state or reducible encoding that actually functions as a directional
reference; a definite Casimir sector alone does not do so.

### 7.28 Overlapping Zero-Bohr Spectral Baseline

An overlapping realization removes the nonoverlap premise rather than defeating
its conclusion. On `V_L tensor V_L`, take scalar fixed-sector Hamiltonians and
the collective charges `Q_a=L_(T,a)+L_(R,a)`. For the declared Gaussian
KMS-compatible spectral ansatz,

```text
j_sigma(w)=w(1+R^2w^2)e^(-sigma^2w^2)
            /[12pi^2R^2(1-e^(-2pi Rw))].                (61)
```

It obeys exact detailed balance and has
`j_sigma(0)=1/(24pi^3R^3)`. The zero-Bohr jumps are collective, the three
target/reference Kossakowski blocks are rank one, and the standard-convention
Lamb shift is the collective Casimir

```text
H_LS=(lambda^2/N^2)s_sigma sum_a Q_a^2,
s_sigma=-1/(24pi^(3/2)R^2sigma)-1/(48pi^(3/2)sigma^3).  (62)
```

This calculation also removes an apparent shortcut: the total-spin singlet is
annihilated by every `Q_a` and is exactly dark under the full system-bath
Hamiltonian. Singlet survival therefore cannot diagnose Markov error.

The Gaussian factor in (61) is the exact multiplier of the shifted heat
semigroup `exp[(sigma^2/2)(Delta_H+R^-2)]` on optical `H^3_R`. This derives the
ansatz from stationary covariant spatial smearing, but the heat kernel has
noncompact Gaussian tails. A Paley--Wiener comparison proves that no compact
stationary profile can reproduce the exact Gaussian. An explicit compact
replacement is obtained by convolving two optical-ball profiles. If `A=a/R`,
its normalized ball multiplier is

```text
q_A(p)=[cosh(A)sin(Ap)-p sinh(A)cos(Ap)]
       /[p(1+p^2)(A cosh(A)-sinh(A))],                 (63)
```

and the regulated spectrum is `j_A(omega)=j_0(omega)q_A(Romega)^4`. It has
support radius `2a`, preserves exact KMS balance and `j_A(0)=j_0(0)`, and falls
as `omega^-5`. A compact smooth convolution-square profile supplies a smooth
compact spatial smearing with rapid spectral decay; compact spacetime support
additionally requires switching.

The support-versus-exponential-type input is the symmetric-space
Paley--Wiener theorem; see [Olafsson and
Wolf](https://arxiv.org/abs/1101.4419).

Let `G=int|g(t)|dt` and `M_1=int|t g(t)|dt`, where `g` is the Fourier transform
of `sqrt(j)`. Frequency Sobolev norms give finite explicit upper bounds on both
moments. For three diagonal gradient channels,

```text
Gamma=144 lambda^2L^2G^2/N^2,  tau=M_1/G.              (64)
```

Under the stationary zero-mean Gaussian-bath and remote-past factorization
hypotheses of Nathan and Rudner, their modified-state estimate can be applied
after adjoining the target memory as an inert spectator. The coupling norms are
unchanged, and the Hermitian zero-Bohr ULE is unital. Duhamel's formula yields

```text
epsilon_infinity(t)<=2Gamma tau+2Gamma^2tau t.          (65)
```

The imported state-dressing and residual estimates are from [Nathan and
Rudner, Appendix C](https://arxiv.org/abs/2004.01469).

At heat time `pi lambda^2j(0)t/N^2=(1/2)log d`, this gives an explicit
`lambda^2L^4N^-2log d` leading term. For a fixed `0<A<1`, an `A/d` spectral
budget leaves the recovery obstruction `1-A-o(1)`. On `N=1/d`, the sufficient
schedule is

```text
lambda=O[d^(-7/2)/sqrt(log d)].                          (66)
```

The pulled-back fidelity witness has trace norm `d`, so matching the heat
`O(1/d)` recovery correction is guaranteed by the stronger sufficient schedule
`lambda=O[d^-4/sqrt(log d)]`. Equation (65) is an ancilla-stable spectral-state
theorem, not a trace- or diamond-norm theorem. Section 7.32 supplies the finite
amplitude-ramp and burn-in correction. The compact smooth profile and switching
function must still be derived from a matter worldtube action with direct
interactions and joint stress controlled.

A named smooth compact baseline now makes the regulator cost quantitative.
Choose a `C_c^infinity` radial seed supported in half an optical radius `a` and
convolve it with its reflection. Its multiplier is `F_A^2`, so the spectrum is
`j_0F_A^4`. Analytic transform derivatives give, for `R=1` and `a=0.2`,

```text
(||q||_2,||q'||_2,||q''||_2)
 =(26.6977477290,1.57849600683,0.176766804082),         (67)
```

with optimized Sobolev estimates `G_num approximately 16.2723018013` and
`M_1,num approximately 1.32407331492`. These are step- and window-converged
numerical values, not interval enclosures. A separate proof does not
extrapolate the finite sinc sum: twice integrating the exact compact transform
by parts and using rational seed/thermal envelopes gives

```text
(Q_0,Q_1,Q_2)<=(3495.325453538189,
                 12944.154923952921,
                 71805.966340613957),
(G,M_1)<=(16863.898481372697,76435.381039140748).       (67a)
```

At `L=4096`, exact evaluation of the symbolic sufficient-cap formula with these
enclosures gives the two declared residual budgets. The executable's
downward-guarded ordinary-float evaluations are approximately `9.9769e-27` and
`1.1022e-28`; they are not directed interval endpoints. Their large gap from
the numerical candidates is proof looseness; tight directed interval
quadrature remains open. In the small-support ultraviolet regime,

```text
||q||_2=Theta(a^-2), ||q'||_2=Theta(a^-1),
||q''||_2^2=[3/(64pi^2)]log(R/a)+O(1),
lambda_cap=Theta(a^(5/2)[log(R/a)]^-1/8).               (68)
```

Three supports resolve the logarithmic second-derivative term, and the
executable `a/R=0.2 -> 0.4` comparison gives effective cap exponent `2.5254`.
Equation (68) is a localization penalty in this sufficient ULE-control route,
not a necessary failure bound. It shows quantitatively that replacing the
quasilocal Gaussian by strict compact support is not cost free.

### 7.29 Matter-Derived Skyrmion Spectrum And Root Obstruction

The centered leading Skyrmion current closes the spatial-profile gap without
choosing another regulator. We use the Killing-time charge-flux interaction

```text
V(t)=g sum_i int_Sigma dSigma_mu ell_i^mu B_i
    =g sum_i int r^2 dr dOmega ell_i^t B_i.            (68a)
```

Coupling its transverse projector to the improved conformal pseudoscalar
gradient and integrating the optical `l=1` channel gives

```text
H_Sky(p)=3R^2/[(1+p^2)I_2]
 int kappa(r)[y coth(y)sinc(py)-cos(py)]dr,
j_Sky(w)=j_0(w)H_Sky(R|w|)^2.                          (69)
```

At zero frequency,

```text
H_Sky(0)=<3[artanh(z)-z]/z^3>_I>1.                    (70)
```

The default hard-wall profile predicts `H_Sky(0)=1.003295544733`, hence a
`0.660195%` enhancement of the zero-frequency gradient rate. This is a direct
finite-size curvature effect of the matter current, rather than a normalization
choice.

The same matter profile reveals a limitation of the current ULE proof. Its
compact hard-wall form factor is UV suppressing but oscillatory; step refinement
finds a simple zero at `p_star=275.00922037`. Therefore the principal factor
`sqrt(j_Sky)=sqrt(j_0)|H_Sky|` has an absolute-value cusp and is not `H^2`.
The existing `Q_2/M_1` Sobolev certificate cannot be transferred to this
physical hard-wall spectrum when the principal nonnegative factor is fixed.
Section 7.30 shows that the scalar convolution admits a narrower real signed
factor, though not an arbitrary complex phase. Thus this is a principal-root
implementation no-go rather than an obstruction intrinsic to the spectrum. A
local-density coupling through `u_mu ell_i^mu` would carry another lapse and is
outside this result.

### 7.30 Signed Jump-Correlator Recovery Gate

The Nathan--Rudner scalar proof begins from the nonconjugated factorization

```text
J(w)=2 pi g(w)^2,
J(t-t')=int g(t-s)g(s-t')ds.                           (71)
```

Although the paper selects the positive root, its scalar derivation uses the
factorization (71), Hermitian symmetry, and time moments. Any real `q` with
`q^2=J` therefore gives the same exact convolution and repeats the error proof
if its inverse Fourier kernel has finite zeroth and first absolute moments.
This does not permit a generic complex phase, for which `|q|^2=J` would not
imply (71), and an irregular sign choice can fail the moment condition.

For the centered matter spectrum, take

```text
q_Sky(w)=sqrt(j_0(w))H_Sky(R|w|).                     (72)
```

Then `q_Sky^2=j_Sky`, `q_Sky` is real, and for `w>0` it obeys the half-KMS
relation `q_Sky(-w)=exp(-pi R w)q_Sky(w)`. At a simple zero of `H_Sky`, (72)
crosses linearly rather than forming the principal-root cusp. The earlier
obstruction is therefore removed locally without changing the physical bath
spectrum.

For the fixed-irrep `h(J^2)` sector, all three collective charges are zero-Bohr
operators and `H_Sky(0)>0`; the signed and principal factors give the same jump
amplitude. Their zero-Bohr Lamb shifts also agree because the coefficient uses
`q(w)^2=j(w)`, while the summed operator is the irrep scalar `J^2`.

Analytic frequency derivatives and finite-window quadrature give

```text
(Q_0,Q_1,Q_2)=(62.2644668852,2.16015691289,0.168156611337),
(G_num,M_1,num)=(29.0705146786,1.51073940540).          (73)
```

At `L=4096`, the corresponding matter-adjusted candidate caps are `3.15e-20`
and `3.48e-22` for the two residual budgets. These are not yet global theorem
constants. The finite trapezoid form factor is never extrapolated to infinity;
Section 7.31 supplies an exact-profile enclosure of `H,H',H''` and establishes
the full `H^2` tail. AU.2 interval-certifies its derivative-norm inputs, and
AU.3a supplies conservative global moment bounds; the much tighter caps above
remain candidates because their profile-resolving finite band is not yet
interval certified. The signed lemma is
scalar/diagonal and zero-Bohr specific. General matrix roots, nonzero-Bohr
bands, switching, off-center deformation, and stress remain open.

### 7.31 Exact Continuum Tail Of The Matter Factor

Conditional on the exact nontrivial regular hard-wall branch, set
`x=tanh(y)/sqrt(lambda)`, let
`Y=atanh(sqrt(lambda)x_w)`, and define

```text
W(y)=[rho_I(x(y))/x(y)^2]dx/dy,
A(y)=W(y)coth(y).                                    (74)
```

The exact continuum numerator in `H_Sky=C N/(1+p^2)` is

```text
N(p)=p^-1 int_0^Y A(y)sin(py)dy-int_0^Y W(y)cos(py)dy. (75)
```

The regular origin series and exact hard-wall Dirichlet data imply

```text
W(y)=w_0 y^2+O(y^4),       A(y)=w_0 y+O(y^3),
W(y)=w_Y(Y-y)^2+O((Y-y)^3),
W''(Y)=4pi sigma^2 N_w^2(1+4N_w sigma^2)
       /(3lambda^(3/2))>0.                            (76)
```

Here `sigma=|F_x(x_w)|>0`; simultaneous vanishing of the wall value and slope
would force the trivial solution by ODE uniqueness. Three integrations by
parts on the half interval, with the wall term retained, give for `p>=P>=1`

```text
|H_Sky^(k)(p)| <= h_k p^-5,  k=0,1,2,                (77)
```

where the explicit `h_k` depend on `C`, `Y`, `W''(Y)`, and the six finite norms
`||d_y^3(y^mW)||_1`, `||d_y^3(y^mA)||_1`, `m=0,1,2`. The wall term also gives
the sharp asymptotics. Finiteness of these norms follows from analyticity of
the profile ODE on the compact interior together with the one-sided endpoint
expansions; validated numerics are needed only to make their values explicit.

```text
H(p)  =C W''(Y)sin(pY)/p^5+o(p^-5),
H'(p) =C Y W''(Y)cos(pY)/p^5+o(p^-5),
H''(p)=-C Y^2 W''(Y)sin(pY)/p^5+o(p^-5).             (78)
```

All three derivatives retain the same power because differentiating the wall
phase does not gain inverse powers. Combining (77) with the bare spectral-root
bounds gives `q_Sky^(k)=O(p^-7/2)` for `k=0,1,2`. The negative tail is
exponentially half-KMS suppressed, the origin is analytic, and the signed
factor is smooth at its simple zeros. Hence

```text
q_Sky in H^2(R).                                     (79)
```

This closes the analytic global-membership gap. It does not yet turn (73) into
rigorous global numbers: the present float RK4 shooting code cannot provide an
interval lower bound for the inertia, outward enclosures for `Y` and `W''(Y)`,
or interval upper bounds for the six third-derivative norms. Those require
validated shooting, endpoint Taylor patches, ODE automatic differentiation,
and directed interval quadrature.
The default floating endpoint diagnostic is `Y=0.2027325541`,
`W''(Y)=245.5560092`, and `C W''(Y)=8599.3544`.

### 7.32 Finite Switch-On And Burn-In

The remote-past preparation hypothesis can be replaced by a finite amplitude
ramp plus a stationary plateau. Let `H_int(t)=chi(t)H_int`, with `0<=chi<=1`,
and define at the plateau start

```text
delta_chi(z)=1-chi(t_s-z),
T_chi=inf_{delta_chi(z)>0} z/delta_chi(z).             (80)
```

Thus `delta_chi(z)<=min(1,z/T_chi)`. A linear ramp of duration `T_sw` has
`T_chi=T_sw`; more generally `||dot chi||_infinity<=L_chi` implies
`T_chi>=1/L_chi`.

Adapting the finite-initialization kernel bound and the modified-state proof of
Nathan and Rudner gives, after plateau burn-in `B`,

```text
||rho_exact(t_s+B+T)-E_T(rho_exact(t_s+B))||_infinity
 <=2 Gamma tau+2 Gamma^2 tau T
   +Gamma tau log(1+T/(B+T_chi)).                     (81)
```

In the modified-state chain rule, the finite-history generator occurs once in
`dot(rho)`. The product `M_t dot(rho)` is bounded as a whole by the unchanged
switched-dynamics speed limit, so no additional multiplicative history term is
introduced.

The proof is stable under an arbitrary inert memory. If

```text
B+T_chi>=beta/Gamma,                                 (82)
```

then

```text
epsilon_infinity(T)
 <=2 Gamma tau+(2+1/beta)Gamma^2 tau T.              (83)
```

At heat time, this changes `20736` in the long-time coefficient to
`20736[1+1/(2beta)]`. It leaves the `d^-7/2/sqrt(log d)` and
`d^-4/sqrt(log d)` schedules unchanged. At `beta=10`, the coupling-cap penalty
is `0.975900...`; the signed-Skyrmion finite-window candidates become
`3.07e-20` and `3.39e-22`. The executable reports the required bound-level
effective age `beta/Gamma_bar` and verifies the mathematical witness obtained
by assigning all of it to `B`. It does not assert that a physical protocol
realizes that witness. The two required ages scale as `d^3 log d` and
`d^4 log d`; their ratio to heat time scales as `1/[d^2 log d]`. A separately
smooth switch-on, flat at the plateau, and a
smooth switch-off after readout make the interaction compactly supported in
time without affecting the measured interval. A linear ramp alone is only
Lipschitz. The quoted caps remain non-interval candidates.

Equation (81) controls a prescribed amplitude switch only after it reaches a
stationary plateau. It does not derive the switching profile from the
Skyrmion/membrane action, describe ramp-time dynamics by a stationary ULE, or
cover non-Gaussian and nonzero-Bohr extensions.

### 7.33 Off-Center Translation Versus Matter Deformation

Before solving the accelerated worldtube, one must separate a coordinate
translation from intrinsic deformation. For a centered optical vector source
`f_j=F(y)n_j` with center regularity `F(y)=c y+O(y^3)`, an infinitesimal
`H^3` transvection along `a` gives

```text
delta f_j=-epsilon a_i[u_0 delta_ij+u_2 Q_ij],
u_0=[F'+2coth(y)F]/3,
u_2=F'-coth(y)F.                                      (84)
```

The old-origin expansion therefore mixes the centered `l=1` source only into
`l=0` plus `l=2` at first order. More importantly, a genuine active optical
translation is a bath symmetry. With the center frame parallel transported,

```text
K_auto,ij(omega;q)=j_Sky(omega)delta_ij              (85)
```

at every displaced center. Pure translation cannot produce auto polarization
splitting at any order. A splitting found by truncating central harmonics is a
coordinate artifact.

The same symmetry gives a new arbitrary-frequency two-center prediction. For
optical separation `y`, `p=R|omega|`, and
`phi_p=sin(py)/[p sinh(y)]`,

```text
c_parallel=-3phi_p''/(1+p^2),
c_perp=-3phi_p'/[(1+p^2)sinh(y)],                     (86)
```

with

```text
c_parallel=1-(3p^2+7)y^2/10+O(y^4),
c_perp=1-(p^2+4)y^2/10+O(y^4).                       (87)
```

The matter factor `H_Sky(p)^2` cancels from these normalized correlations,
although at its zeros the whole physical block vanishes and the ratio is not
operationally defined. Equation (87) extends the previous zero-frequency
gradient result to the full spectrum.

A held massive Skyrmion is not an optical translate: the mass term, lapse,
membrane, and anchor break transvection symmetry. Assume a parity-even
nonrotating baseline, parity-odd vector smearing, acceleration as the only new
vector, and an angular-momentum-diagonal bath inner product about the recentered
worldtube. The first intrinsic source response is then `l=0+2` and has no
interference with the centered `l=1` source, so a real symmetric auto splitting
starts at quadratic order in acceleration times source size. Its longitudinal
and transverse coefficients require the coupled linearized `l=1` matter,
membrane, and anchor problem. This identifies a clean observable under the
stated symmetry assumptions: nonzero auto splitting is a deformation
diagnostic rather than a kinematic displacement effect. The executable audits
the coordinate and spectral formulas; the any-order isotropy result follows
analytically from bath homogeneity.

### 7.34 Validated Profile And Continuum Tail Certificate

Exact rational interval arithmetic now closes AU.1 for the prescribed hard-wall
profile: a Newton ball proves local existence and uniqueness, strict
monotonicity, negative wall slope, and positive finite inertia. AU.2 combines a
43-cell positive-radius interval-jet audit with a regular-origin Volterra-Lie
and fourth-order interval-AD proof. It certifies all six third-derivative `L1`
norms and evaluates the exact `p^-5` tail envelope with archive SHA256
`1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9`.

AU.3a gives a directed profile-uniform finite-frequency sum and exact tail join
for conservative global `Q_0,Q_1,Q_2,G,M_1`. The authenticated AU.3b baseline
retains the radial profile, but its conservative joined tail supplies more than
`99.2%` of every squared Sobolev bound and makes all three `Q` bounds weaker
than AU.3a. The remaining numerical gate is to sharpen the tail and bare
spectral product bounds; no current zero-lower-bound ULE cap is a physical
observer window.

## 8. Novelty And Next Theorem

Standard ingredients include fuzzy-sphere Berezin quantization, reference
twirling, relational constraints, edge modes as frames, approximate recovery,
and gravitational crossed products. The result is paper-worthy only if the
combined hierarchy and obstruction changes a credible horizon dictionary.

Sections 7.15-7.34 now supply a quantitative compact same-target comparison, an
energy-identifiability obstruction, and a finite-size worldtube EFT ansatz with
an all-state mean-energy recovery no-go for deterministic decoders after the
fixed append-and-twirl channel, plus a finite-time collective-diffusion bridge
with a logarithmic sufficient protocol schedule and a quantitative
common-mode locality-mismatch test. The Bunch-Davies scalar calculation now
rules out one fixed-separation local realization of the common mode, and the
`H^3` product formula shows arbitrary radial worldtube size cannot repair it.
The gradient calculation further shows that the simplest local three-component
extension contains polarization-dependent relative noise at every separated
center. The higher-spin singlet calculation strengthens the local co-location
law to `d^-3/2/sqrt(log d)` when the protected angular sector grows with `d`.
The pseudoscalar phase-space action supplies a parity-consistent localized top
coupling and shows that uniform Markov control plus a declared interaction-RMS
budget produces a `d^3 log d` proper-time schedule. The hard-current theorem
then gives an exact transported monopole identity and isolates separate
zero-Bohr, aggregate nonzero-Bohr, and second-order jump-transfer hypotheses;
under them it supplies conservative generic and dipole-cancelled support
designs. Their collision with the compact-top radius floor now gives a
conditional closure of the controlled local-common-mode branch for distinct
nonoverlapping equal-radius thin-shell worldtubes at fixed `R^2/G`, while
deliberately leaving open nonperturbative channel behavior, overlapping sectors,
and different matter realizations. The next theorem must
replace the stipulated inertia/compactness hypotheses by a controlled
gravitational source and couple the top to the Lorentzian Hadamard net of
Sections 7.9-7.14. It must answer:

```text
Does the core-stable missing-frame entropy become a generalized-area correction
or observer-algebra index in a named static-patch construction?
```

It must also derive whether the relevant reference group is full `SU(2)` or an
axial stabilizer and show that the required degeneracy is protected on the
physical observer time scale.

The immediate Paper C target is narrower than the full crossed-product question:
derive the three jump transfers, Kossakowski/Lamb-shift stability, and current
moments from the Lorentzian field/worldtube model, prove that its reduced channel
is within an explicitly controlled error of the collective heat semigroup, and
show that this error remains smaller than the recovery obstruction in one joint
localization, lifetime, and backreaction scaling window.

The selected lead matter model is a massive `SU(2)` Skyrmion in its rotational
collective-coordinate sector. The physical-pion-mass convention and exact
flat/fixed-de-Sitter profile equation are now fixed. At `mu=1`, a dependency-
free flat shooting calculation gives `c_M=48.6317632` and `c_I=34.3539730`, with
unit baryon number, the massive Robin tail, and the Derrick identity verified.
The fixed-de-Sitter analysis also exposes a decisive boundary effect: generic
regular horizon data with `sin(F_c) != 0` make the untruncated global rigid-
rotor inertia diverge logarithmically. The program therefore selects a finite
supported worldtube as the next controlled model; a global uniqueness theorem
excluding exceptional horizon data remains open. A covariant parity-even
`B_mu S^mu` coupling exists at collective-worldline level because the dynamical
hedgehog orientation solders isospin to physical spin. A point-local coupling
written solely in the bare Skyrme field, the boundary/support stress,
off-center current deformation, and uniform slow-rotation control remain open.
Given the standard leading collective-current compression, inversion symmetry
now makes the centered signed operator
dipole vanish componentwise, while `(e f_pi)^2<rho^2>_I=2.19023555` fixes the
signed second moment and a conservative absolute `M2` bound. This establishes
the centered matter input to the hard-current Hessian branch, not the
accelerated near-horizon source. The work package is in
`docs/massive_skyrmion_observer_program.md`.

Two successor gates are now explicit. First, a centered covariant ideal-mirror
membrane imposing `U=1` gives an exact-`B=1` hard-wall profile. Its radial
pressure and shell curvature obey a Young-Laplace balance, with positive tension
possible only for `x_w<sqrt(2/3)x_c`; the default centered example has
subdominant wall mass. Authenticated exact-profile Barta replay first proves
the fixed-wall floor `omega_hat_l0>=1/5`. A compatible moving-wall witness and
exact Young-Laplace cancellation then prove the complete spherical
profile-membrane floor `omega_hat_l0>=1/50`, independently of the floating
branch-curvature estimate. A simple finite cosine pinning potential cannot preserve exact
`B=1` for a nontrivial profile; its topology defect begins at
`O(kappa_pin^-3)`, so an exact finite-stiffness completion needs boundary
topological degrees of freedom or a different mechanism. Anchor, nonspherical
modes, and off-center support remain open. Second,
standard fermionic `B=1` quantization selects the half-integer
odd Peter-Weyl sector rather than the integer rotor. Its density and covariant
POVM are nevertheless center blind, and exact rational counting gives the same
kind of integer-target recovery multipliers and fidelity law. The physical
decoder must access the right/isospin multiplicity, and uniform slow rotation
requires `e^2J -> 0`; fixed Skyrme parameters cannot support a growing cutoff.
For the fixed dimensionless centered worldtube profile, constrained co-scaling
of `e` and `f_pi` cannot cure this: compactness scales as `e^-2`, slow rotation
as `e^2sqrt[(J+1/2)(J+3/2)]`, and their product is independent of `e`. Fixed control
budgets at fixed `R^2/G` therefore give a finite-spin window. Profile-changing
double scalings and different matter sources remain open escape routes.

A complementary Track B deliberately drops nonoverlap by placing two
distinguishable spin sectors in one worldtube. With scalar fixed-sector
Hamiltonians, the collective charges are exactly zero Bohr frequency, so a
fixed-width smeared Bunch-Davies gradient bath has explicit collective jumps and
a Casimir Lamb shift. The total-spin singlet is exactly dark under the full
collective system-bath Hamiltonian, so singlet survival cannot test the Markov
approximation. The non-dark rank-one Choi return projector now supplies a fixed-
task diagnostic whose heat return probability is `O(1/d)`. It cannot by itself
establish robustness for every decoder: the pulled-back fidelity witness has
trace norm exactly `d`. The Gaussian is now derived from stationary optical
heat smearing, with a compact spatial replacement supplied separately. Under
the Nathan--Rudner stationary Gaussian-bath hypotheses, the ancilla-stable
spectral estimate is proved; Section 7.32 replaces remote-past preparation by a
prescribed ramp and explicit burn-in. With a fixed small `A/d` residual budget,
the sufficient schedule `lambda=O[d^-7/2/sqrt(log d)]` on `N~d^-1` preserves the
obstruction `1-A-o(1)`; matching the heat correction is guaranteed by the
stronger `lambda=O[d^-4/sqrt(log d)]`. A named compact smooth profile now gives
profile-specific converged numerical estimates, conservative analytic
exact-profile enclosures, and an additional
`a^(5/2)[log(R/a)]^-1/8` candidate sufficient-cap localization penalty. This
route still requires tight finite-window interval quadrature and derivation of
the prescribed switch from the worldtube action. The centered Skyrmion current
now supplies a matter-derived spatial
form factor and zero-mode prediction, but its principal spectral root fails the
same `H^2` route at simple form-factor zeros. The scalar signed-factor lemma
removes that local cusp and supplies converged finite-window Sobolev candidates.
The exact continuum endpoint theorem now proves global `H^2` membership and
supplies a parameterized `p^-5` tail bound; interval-certified numerical
constants remain required. The finite-preparation theorem controls a prescribed
amplitude ramp without changing the coupling exponents; direct-interaction and
joint-stress control and an operationally distinguishable overlapping encoding
remain required.
See
`docs/overlapping_qft_davies_program.md` and
`docs/static_patch_worldtube_ule.md`, and
`docs/static_patch_smooth_worldtube_ule.md`, and
`docs/static_patch_skyrmion_bath.md`, and
`docs/static_patch_skyrmion_signed_ule.md`, and
`docs/static_patch_skyrmion_tail.md`, and
`docs/static_patch_finite_switching_ule.md`.

The live discriminator is between scalar clocks and covariant group-valued
observers. Under the compact-fixed-point hypotheses, a scalar clock is subject
to the `log(R/delta)` obstruction. A compact charged Peter-Weyl reference now
has both a constructive recovery law and a finite-size action, but its
compactness and local-coupling dynamics remain effective assumptions. The next
positive theorem should derive the analogous energy-constrained `SO(1,d)`
recovery/error law from a controlled covariant observer source.

Until that theorem is supplied, this draft is a controlled mathematical-
physics result and research program, not a de Sitter breakthrough claim.
