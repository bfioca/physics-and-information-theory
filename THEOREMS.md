# Theorem and Claim Index

This file indexes the packaged static-patch observer-algebra benchmark and the
long research theorem ledger. For the selected review-ready Paper A, start with
the root [`README.md`](README.md) and
[`paper/validated_skyrmion_profile/main.pdf`](paper/validated_skyrmion_profile/main.pdf).
The bounded spacelike-replication methods note and Harlow-facing
observer-register packet are separate artifacts. The entries below separate
exact finite claims, bounded certificate evidence, conditional
operator-algebra assumptions, and continuum speculation.

## Claim Boundary

The repository provides a finite executable benchmark suite. It does not prove
continuum de Sitter quantum gravity, dS/CFT, approximate QEC, or ER=EPR in de
Sitter.

The safe public claim is:

```text
finite screen-visible shadows can be incomplete; operator-algebraic response
can be necessary to identify the observer algebra or bridge channel.
```

## Active Research Theorem Stack

The following results live on the active research branch and are not part of
the frozen `v0.1-static-patch-diagnostics` package.

### Research Theorem A: Canonical Low-Mode Berezin Refinement

For the coherent-state map `J_{L->M}=Q_M sigma_L`, normalized fuzzy harmonics
satisfy

```text
J_{L->M}(T^L_{ell,m})
  = sqrt(b_{L,ell}b_{M,ell}) T^M_{ell,m}.
```

The map is UCP and normalized-trace preserving, its Schrödinger rescaling is
CPTP, and it exactly intertwines the fuzzy Laplacian and heat semigroup. On the
entire coefficient-atomic unit ball of `span{I,X_x,X_y,X_z}`,

```text
||J_{L->L+1}(AB)-J(A)J(B)||_op <= 8/[3(L+2)].
```

A highest-mode partial isometry gives a full operator-unit-ball defect tending
to `1/2`, so the low-mode restriction is necessary.

Artifacts: `docs/canonical_berezin_refinement.md`,
`qgtoy/fuzzy_berezin.py`, `tests/test_fuzzy_berezin.py`.

### Research Theorem B: Cutoff-Uniform Screen Inference

The mixed `ell=1` probes `(I+/-J_z/j)/(L+1)` and
`(I+/-J_x/j)/(L+1)`, paired with the coherent-screen coordinate witnesses,
have exact response signatures

```text
identity:     (1/3,1/3),
J_z dephase:  (1/3,0),
depolarize:   (0,0).
```

The separation is cutoff independent. Componentwise response error below
`1/6` identifies the declared candidate, and Hoeffding gives explicit constant
sample complexity. The probes, witnesses, CPTP state lift, and response all
have explicit Berezin transport formulas.

Artifacts: `docs/noisy_observer_algebra_inference.md`,
`qgtoy/fuzzy_algebra_inference.py`,
`tests/test_fuzzy_algebra_inference.py`.

### Research Theorem C: Constraint-Derived Edge-Algebra Correction

On `H_L=L^2(M_{L+1},tau_L)`, impose commuting time and angular-reference
constraints. The derived accessible algebras are

```text
full references:        M_{(L+1)^2},
time reference hidden:  direct_sum_{ell=0}^L M_{2ell+1},
time and edge hidden:   C^{(L+1)^2}.
```

Thus the Hamiltonian constraint alone does not derive a diagonal screen. The
extra angular-reference restriction discards

```text
L(L+1)(4L+5)/3
```

within-energy coherence parameters and retains only
`3(L+1)/(4L^2+8L+3) ~ 3/(4L)` of the time-constraint algebra.

### Research Theorem D: Relational Screen Recovery No-Go

There are orthogonal states within one energy block that the time-blind algebra
retains and the fully diagonal screen identifies. Every decoder through that
screen has worst-case trace-distance error at least `1/2`; if the screen
distance is at most `epsilon`, the bound is `(1-epsilon)/2`.

Under Gaussian angular-reference uncertainty, extremal magnetic visibility is
`exp(-2 sigma^2 L^2)`, so fixed visibility requires `sigma_L=O(1/L)`. The bare
Fourier scaling is standard; the research candidate is its conjunction with
the algebra-fraction and recovery bounds. After smearing, every decoder obeys

```text
eta_recovery(L) >= (1-exp[-2 sigma^2 L^2])/2,
```

which tends to `1/2` at fixed nonzero reference width.

The harmonic-core continuum limit is Type I, not Type II. This is a controlled
no-go for obtaining a gravitational observer factor from the one-particle
constraint model.

Artifacts: `docs/relational_fuzzy_horizon_observer.md`,
`qgtoy/relational_observer.py`, `tests/test_relational_observer.py`.

### Research No-Go E: Finite Clocks Do Not Produce Type II

Every finite matrix automorphism is inner. For a cyclic clock action,

```text
M_d crossed Z_q = M_d tensor C*(Z_q) = direct_sum_q M_d.
```

Thus a nontrivial finite clock produces a center of dimension `q`, and every
finite cutoff remains Type I. A Type-II gravitational algebra requires a
many-body/local-QFT limit with outer modular flow before or jointly with the
crossed-product construction.

Artifacts: `docs/finite_clock_crossed_product_gate.md`,
`qgtoy/finite_clock_crossed_product.py`,
`tests/test_finite_clock_crossed_product.py`.

### Research Construction F: State-Derived Many-Body Modular Core

Let `A_n=M_2^{tensor n}` and equip odd and even sites with faithful Gibbs
states whose gap parameters are `1` and `sqrt(2)`. The tensor embeddings and
product-state conditional expectations are exactly state preserving and
modular covariant at every finite cutoff.

Regrouping into a recurrent two-site block, or separating the odd and even
Powers subchains, gives parameters `exp(-beta)` and `exp(-beta sqrt(2))`. The
asymptotic ratio group is dense in the positive reals, so `S(M)=[0,infinity)`
and standard ITPFI/Connes classification gives a hyperfinite Type-`III_1`
product-state GNS factor. Its modular crossed product by `R` is the hyperfinite
Type-`II_infinity` continuous core with a faithful normal semifinite trace.

The finite identities are directly verified; the infinite factor and core
types are analytic classification theorems, not numerical certificate output.
This construction is a thermal many-body surrogate. It does not yet carry the
fuzzy angular geometry, relational edge conditional expectation, a derived
static-patch state, or a generalized-entropy theorem.

Artifacts: `docs/modular_manybody_regulator.md`,
`qgtoy/modular_manybody_regulator.py`,
`tests/test_modular_manybody_regulator.py`.

### Research Theorem G: Full-Rotation Correction And Spectral Fragility

The earlier edge theorem hides an axial `U(1)` phase reference. If a complete
`SU(2)` orientation reference is hidden instead, multiplicity-one Schur
duality gives

```text
(direct_sum_ell M_{2ell+1})^{SU(2)} = direct_sum_ell C I_{V_ell}.
```

The full-rotation algebra has dimension `L+1`, is the center of the time-blind
algebra, and retains the fraction

```text
3/(4L^2+8L+3) ~ 3/(4L^2).
```

Thus the axial `3/(4L)` law is not a full-orientation law. Full rotation loss
also collides an orthogonal within-irrep phase pair and gives decoder error at
least `1/2`.

The time/axial-edge distinction additionally requires protected magnetic
degeneracy. For

```text
H_delta|ell,m> = [ell(ell+1)+delta m]|ell,m>,
delta = r sqrt(2), r nonzero rational,
```

the spectrum is nondegenerate, so infinite-time averaging is already diagonal
for arbitrarily small nonzero `delta`. At finite duration `T`, the extremal
phase-pair trace distance is exactly `|sinc(delta L T)|`. The operational
crossover is therefore `|delta|LT=O(1)`; rotationally invariant perturbations
`f(K_L)` preserve the original block result.

Artifacts: `docs/edge_symmetry_robustness.md`,
`qgtoy/edge_symmetry_robustness.py`,
`tests/test_edge_symmetry_robustness.py`.

### Research Theorem H: Core-Stable Recovery And Entropy Obstruction

Tensor the relational harmonic algebra with the hyperfinite Type-`III_1`
product-state factor and use the product state

```text
M_L = M_{(L+1)^2} tensor R_III1,
Phi_L = tau_L tensor phi.
```

The modular flow is trivial on the angular matrix factor, hence

```text
M_L crossed_{sigma^Phi} R_time
  is canonically isomorphic to
  M_{(L+1)^2} tensor (R_III1 crossed_{sigma^phi} R_time).
```

The right-hand side is a hyperfinite Type-`II_infinity` factor. Every time,
time-then-axial, or full-rotation expectation extends as `E tensor identity`
and preserves the semifinite core trace. Consequently, the clock core cannot
reconstruct an angular coefficient discarded by `E`.

For the lifted within-`ell` phase pair, the input trace distance remains `1`,
the time-then-axial outputs collide, every decoder has worst-case error at
least `1/2`, and

```text
D(rho tensor omega || E_{t,phi}(rho) tensor omega) = log 2.
```

For a pure state in the spin-`L` irrep under full orientation loss,

```text
D(rho tensor omega || E_SU2(rho) tensor omega) = log(2L+1).
```

This is a state-weighted core obstruction, replacing raw algebra-dimension
counting. The construction is still factorized: the Type-III thermal sector is
a spectator, so an interacting static-patch KMS derivation remains open.

Artifacts: `docs/core_stable_edge_obstruction.md`,
`qgtoy/core_edge_obstruction.py`,
`tests/test_core_edge_obstruction.py`.

### Research Theorem I: Interacting Boundary-KMS Stability

Couple the fuzzy harmonic energy to the first qubit of the thermal chain:

```text
H_B = a K_L + Delta n_1 + g K_L n_1,
rho_B proportional exp(-beta H_B).
```

For `L>=1`, `beta>0`, and the declared domain `g>0`, the Gibbs distribution has
analytically positive mutual information
`I(ell:n_1)`, so the angular and thermal boundary state is non-product. The
interaction is a rotational scalar; it preserves `SU(2)`, the magnetic
degeneracy, and all declared reference expectations.

Absorb the first qubit into the finite boundary factor. The untouched infinite
tail still contains both incommensurate gap families infinitely often, hence
the full algebra remains hyperfinite Type-`III_1`. Exterior equivalence through
the boundary-density cocycle identifies the continuous core, relative to the
declared tensor split, with a finite matrix amplification of the tail
Type-`II_infinity` core. The angular expectations preserve matrix trace and the
boundary density, so their core extensions are trace preserving.

Within fixed `ell=L`, the interaction is scalar in `m`. Therefore normal probe
states in the interacting KMS representation retain the exact obstruction

```text
decoder error >= 1/2,
D_time+axial = log 2,
D_full-SU2 = log(2L+1).
```

The invariant KMS state itself has zero relative-entropy loss under these
expectations.

This is the first non-product angular-thermal Gibbs construction in the
program. It is still a finite-boundary bath model, not a local relativistic or
de Sitter KMS net.

More generally, if the bath carries the trivial `SU(2)` action, Schur's lemma
forces every invariant Hamiltonian on `V_L tensor K_L` to have the form
`I_{V_L} tensor H_{bath,L}`. The `1/2` recovery bound and `log(2L+1)` full-
orientation probe entropy loss are therefore independent of bath dynamics and
coupling strength. A scalar bath cannot supply the missing orientation
reference; evasion requires charged reference degrees of freedom, symmetry
breaking, or different representation multiplicities.

Artifacts: `docs/interacting_kms_edge_model.md`,
`qgtoy/interacting_kms_edge.py`,
`tests/test_interacting_kms_edge.py`.

### Research Theorem J: Charged Invariant-Subsystem Encoding

For a spin-`L` sector on the same KMS/core background, compare the invariant
subsystems available with a scalar auxiliary representation and with the
truncated Peter-Weyl block

```text
R_L = V_L^* tensor C^{2L+1}.
```

For `d=2L+1`, the map

```text
W|k> = |Omega_L>_{V_L,V_L^*} tensor |k>_K
```

is an exact singlet-sector isometry from a logical `d`-level space into
`V_L tensor V_L^* tensor K`. The invariant subspace is the fixed singlet tensor
the `d`-dimensional multiplicity register `K`, so the invariant logical algebra
is `B(K)=M_d`. Discarding the singlet factors and reading `K` recovers every
pre-encoded logical matrix unit and has diamond error zero.

Within the pure-isometry-into-singlets class, the result is

```text
V_L^* tensor C^d supplies an exact d-dimensional singlet code,
and auxiliary dimension d^2 is necessary and sufficient.
```

Tensoring the finite code with the same KMS/Type-II core density gives only
spectator-factor stability. If a finite auxiliary representation decomposes as
`direct_sum_j V_j tensor C^{m_j}`, the invariant multiplicity with `V_L` is
`m_L`. Exact encoding of all `d` states requires `m_L>=d`, so the reference
dimension is at least `d^2`. The Peter-Weyl block saturates the bound.

The encoder is not `SU(2)`-covariant from the charged input: its output is
invariant, while the input transforms as `V_L`. The full fixed operator algebra
is `direct_sum_{J=0}^{2L} B(K)`, and `B(K)` above is only the singlet corner.
This does not prove recovery of an unknown system state from
`rho_S tensor eta_R` after group twirling. That operational reference-frame
problem requires a fixed prepared reference state, allowed covariant operations,
and an optimal resource/error bound.

Artifacts: `docs/charged_reference_recovery.md`,
`qgtoy/charged_reference_recovery.py`,
`tests/test_charged_reference_recovery.py`.

### Research Theorem K: Operational Finite `U(1)` Reference

For system charges `m=-L,...,L`, append the fixed prepared reference

```text
|eta_N>=(N+1)^(-1/2) sum_{n=0}^N |n>,
```

apply the joint `U(1)` twirl, decode within conserved total-charge sectors, and
trace the sector flag. The exact logical channel is

```text
rho_{m,m'} -> max(0,1-|m-m'|/(N+1)) rho_{m,m'}.
```

For a selected phase pair with gap `Delta`, the decoded outputs have trace
distance `v_Delta`. Every deterministic recovery has worst-case normalized
trace-distance error at least `(1-v_Delta)/2`, and the sector decoder attains
that bound. The uniform reference therefore has extremal-gap error
`min(1/2,L/(N+1))`.

At fixed maximum reference charge `N`, the pairwise-optimal reference is the
sine eigenvector on a longest step-`Delta` charge chain. With
`r=floor(N/|Delta|)+1`, its exact visibility and error are

```text
v_opt=cos(pi/(r+1)),
error_opt=[1-cos(pi/(r+1))]/2.
```

For `|Delta|=2L`, this is `Theta((L/N)^2)`. The theorem is pairwise and axial;
it is not a full-space or diamond-norm optimum and does not solve the `SU(2)` or
`SO(1,d)` reference problem.

Artifacts: `docs/operational_phase_reference.md`,
`qgtoy/operational_phase_reference.py`,
`tests/test_operational_phase_reference.py`.

### Research Theorem L: Single-Irrep `SU(2)` Reference No-Go

For a spin-`L` system and any fixed product state on one spin-`J` reference,
with no accessible multiplicity ancilla,

```text
E_eta(rho)=SU(2)-twirl(rho tensor eta)
```

has an abelian range. Indeed,

```text
V_L tensor V_J = direct_sum_{K=|L-J|}^{L+J} V_K
```

is multiplicity-free, so the fixed operator algebra is
`direct_sum_K C I_{V_K}`. The channel is measure-and-prepare, hence
entanglement-breaking, for every `eta` and every finite `J`.

For `d=2L+1`, any deterministic decoder remains entanglement-breaking. Testing
on half of a maximally entangled state gives

```text
(1/2)||D E_eta - identity||_diamond >= 1-1/d.
```

Increasing the size of one irreducible spin does not reduce this bound.
Nontrivial symmetry charge is necessary but not sufficient for full quantum
recovery; a positive construction needs reducible reference content with irrep
multiplicity. Restricted classical estimation, postselection, and reducible
references lie outside the theorem.

Artifacts: `docs/su2_directional_reference_no_go.md`,
`qgtoy/su2_directional_reference_no_go.py`,
`tests/test_su2_directional_reference_no_go.py`.

### Research Theorem M: Global Geometric Gibbs Type-I No-Go

For a positive-mass normal-ordered free boson on a sphere of radius `R`, use

```text
omega_ell=sqrt(mu^2+ell(ell+1)/R^2),
H_L=sum_{ell<=L,m} omega_ell a^*_{ell,m}a_{ell,m}.
```

With `q=exp(-beta/R)`, the omitted log partition function obeys

```text
log Z_infinity-log Z_L
 <= q^(L+1)[(2L+3)-(2L+1)q]/(1-q)^3.
```

Embed the cutoff Gibbs density into the full Fock space by putting omitted modes
in their vacuum. Its normalized trace distance from the infinite Gibbs density
is `1-1/Z_tail`, hence is bounded by the same vanishing log-partition tail. The
angular-cutoff states therefore converge in trace norm to a trace-class global
Gibbs density.

For the declared global observable algebra `B(Fock)`, the GNS algebra is Type
`I_infinity` and the Gibbs modular action is inner. Its crossed product is
exterior-equivalent to the trivial-action crossed product and has diffuse
center; it is not the Type-II factor of the de Sitter observer construction.
The noncompact massless constant mode instead has a divergent thermal trace and
does not supply a Type-III mechanism.

Consequently, arbitrarily many compact angular harmonics in the global Fock
algebra are insufficient. A candidate regulator must retain localized algebras;
a faithful static-patch realization should also include radial and near-horizon
redshift degrees of freedom before taking the modular crossed product. The
four-dimensional static-patch optical volume diverges as `pi R^4/delta` when a
stretched-horizon cutoff `delta` is removed.

Artifacts: `docs/geometric_thermal_type_no_go.md`,
`qgtoy/geometric_thermal_type_no_go.py`,
`tests/test_geometric_thermal_type_no_go.py`.

### Research Theorem N: Operational Reducible Rotation Reference

For an unknown spin-`L` state and any fixed finite-dimensional prepared
rotation reference, joint group averaging followed by deterministic decoding
cannot recover the complete spin sector exactly. The continuous
Knill-Laflamme kernel contains

```text
<eta|U_R(g^-1 h)|eta> U_L(g^-1 h),
```

whose reference factor is nonzero near the identity while the nontrivial target
representation is not scalar there.

For

```text
R=direct_sum_j V_j tensor C^{m_j},
V_L tensor R=direct_sum_K V_K tensor C^{n_K},
```

let `r=max_K n_K` and `d=2L+1`. The twirled Choi state has Schmidt number at
most `r`, so every decoder obeys

```text
(1/2)||D N_eta-identity_d||_diamond >= max(0,1-r/d).
```

The smallest reducible example `V_0 direct_sum V_1` has fixed algebra
`C direct_sum M_2 direct_sum C`: it retains a relational qubit, but its
full-sector recovery lower bound is `1-2/(2L+1)`.

A constructive treatment uses the integer-spin `SO(3)` Peter-Weyl cutoff,
equivalently a center-blind `SU(2)` reference for conjugation on the target
operator algebra,

```text
R_J=direct_sum_{j=0}^J V_j tensor V_j^*,
U_R(g)=direct_sum_j U_j(g) tensor identity,
D_J=(J+1)(2J+1)(2J+3)/3.
```

The canonical token state and covariant orientation POVM give a random-rotation
decoder. On rank-`k` tensor operators,

```text
lambda_k(J)=
 sum_{j,l<=J}(2j+1)(2l+1) 1{|j-l|<=k<=j+l}
 /[(2k+1)D_J].
```

For `k<=2J`,

```text
1-lambda_k(J)=
 k(k+1)[12J(J+2)-k(k+1)+11]/[6(2k+1)D_J].
```

For fixed target `L`, the constructive decoder converges in diamond norm as
`J` grows, while exact equality is excluded at every finite cutoff. The
left-action Casimir cost is exactly `3J(J+2)/5`. The decoder is not claimed
optimal, and convergence is not uniform when `L` grows proportionally with
`J`.

Artifacts: `docs/operational_su2_reference.md`,
`qgtoy/operational_su2_reference.py`,
`tests/test_operational_su2_reference.py`.

### Research Theorem O: Static-Patch S-Wave Covariance Refinement

For a conformally coupled massless scalar in four-dimensional de Sitter, the
rescaled s-wave has vanishing radial potential in the tortoise coordinate

```text
x=R artanh(r/R).
```

A Dirichlet wall at the stretched-horizon radial gap `delta` gives an interval
of length

```text
X_delta=(R/2)log[(2R-delta)/delta]
```

with frequency spacing `pi/X_delta`. For an `L^2`-normalized indicator `f`
supported in a fixed compact interval of the tortoise coordinate, the
UV-truncated equal-time thermal field variance at `beta=2 pi R` is the right
Riemann sum

```text
C_delta(f)=1/X_delta sum_{n pi/X_delta<=K}
 |F(n pi/X_delta)|^2 coth(beta n pi/(2X_delta))/(n pi/X_delta).
```

As `delta` tends to zero, `X_delta` diverges, the radial spacing collapses, and
this converges to the corresponding half-line integral through fixed momentum
cutoff `K`. The limit is local covariance convergence on fixed compact support,
not trace-norm convergence of a global Gibbs density.

This is a geometrically derived refinement benchmark, not yet a Weyl-net or
factor-type theorem. The finite Dirichlet Gibbs states are regulator choices,
not literal restrictions of the Bunch-Davies state. Research Theorem Q supplies
the projected phase-space covariance, symplectic form, and unequal-time KMS
identity at fixed UV cutoff. Still missing are smooth UV removal restoring
locality, all angular sectors, identification of the Bunch-Davies local GNS
representation, and the Type-`III_1` proof.

Artifacts: `docs/local_static_patch_weyl_regulator.md`,
`qgtoy/static_patch_weyl_regulator.py`,
`tests/test_static_patch_weyl_regulator.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-weyl-regulator
```

### Research Theorem P: Redshifted Rotational-Frame Capacity Lower Bound

For the conformally coupled scalar, the angular-`ell` radial one-particle
operator in tortoise coordinate is

```text
h_ell=-d^2/dx^2+ell(ell+1)/(R^2 sinh^2(x/R)).
```

Place one normalized Dirichlet sine packet in the collar
`X_delta-bR < x < X_delta-aR`, where `0<a<b` are fixed. Its kinetic form is
`c_chi/R^2`, with `c_chi=pi^2/(b-a)^2`, and monotonicity of the angular
potential gives

```text
<h_ell> <= R^(-2)
 [c_chi+ell(ell+1)/sinh^2(X_delta/R-b)].
```

Rayleigh-Ritz therefore gives an actual finite-wall eigenfrequency at most `E0`
for every `ell<=L_delta`, where

```text
L_delta=max{ell:
 ell(ell+1)<=((E0 R)^2-c_chi)sinh^2(X_delta/R-b)}.
```

Choosing one normalized such eigenstate `phi_ell` per spin gives the pure token

```text
|Psi_delta>=sum_{ell=0}^{L_delta}
 sqrt(2ell+1)/(L_delta+1) |phi_ell> tensor |ell,ell>
```

with hard finite-wall static-energy support below `E0`. Its `SO(3)` twirl is
maximally mixed on a rank-`(L_delta+1)^2` support, so

```text
D(Psi_delta || E_SO(3)(Psi_delta))=2 log(L_delta+1).
```

Since

```text
L_delta^2 ~
 [((E0 R)^2-c_chi) exp(-2b)/2] R/delta,
```

the available missing-frame relative entropy obeys

```text
2 log(L_delta+1)=log(R/delta)+O(1)
                 =log[A/(2 pi rho^2)]+O(1),
```

where `rho=R acos(1-delta/R)` and `A=4 pi R^2`.

This is a capacity lower bound, not by itself an observer no-go. The no-go
interpretation requires a physical observer channel that performs the rotation
expectation. Identifying the resulting Type-II trace entropy with generalized
entropy further requires the gravitational observer construction. Backreaction,
local proper-energy, occupation-number, and full `SO(1,4)` constraints are not
included.

Artifacts: `docs/redshifted_frame_capacity.md`,
`qgtoy/redshifted_frame_capacity.py`,
`tests/test_redshifted_frame_capacity.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy redshifted-frame-capacity
```

### Research Theorem Q: Fixed-UV S-Wave Phase-Space KMS Limit

Let `F=(f,g)` denote compactly supported equal-time Cauchy data for the
rescaled conformal s-wave. On the Dirichlet interval `(0,X_delta)`, retain modes
`k_n=n pi/X_delta<=K`. The projected symplectic form and thermal covariance are

```text
sigma_delta,K(F,G)=sum_n(f_n g_G,n-g_n f_G,n),

mu_delta,K(F,G)=1/2 sum_n coth(beta k_n/2)
 [f_n f_G,n/k_n+k_n g_n g_G,n],
```

with `beta=2 pi R`. For the unitary half-line sine transform,

```text
f_n=sqrt(pi/X_delta) fhat(k_n),
```

so both expressions are right Riemann sums. At every fixed UV cutoff `K` they
converge, on each finite family of compact tests, to the corresponding
half-line bandlimited phase-space forms. The zero-frequency thermal singularity
is removable because `fhat(k)=O(k)`.

The finite covariance satisfies the quasifree uncertainty condition

```text
mu(F,F)mu(G,G)>=sigma(F,G)^2/4.
```

The unequal-time two-point function is analytic on the open KMS strip and
obeys the exact boundary identity

```text
omega(A_F alpha_(t+i beta)(A_G))=omega(alpha_t(A_G) A_F).
```

The finite unequal-time sums converge to the fixed-band continuum integral,
and at equal time

```text
omega(A_F A_G)=mu(F,G)+i sigma(F,G)/2.
```

This proves a projected quasifree/KMS regulator theorem, not a local AQFT net.
The hard bandlimit is spatially nonlocal. UV removal on smooth data, all
angular sectors, direct identification with the Bunch-Davies distribution,
Hadamard behavior, Type `III_1`, and the continuous core remain open.

Artifacts: `docs/static_patch_phase_space.md`,
`qgtoy/static_patch_phase_space.py`,
`tests/test_static_patch_phase_space.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-phase-space
```

### Research Theorem R: S-Wave Ultraviolet Removal

Let `F=(f,g)` and `G=(u,v)` be compactly supported s-wave Cauchy data whose
zero extensions have finite `n`-th distributional derivative measures, with
`n>=2`. Integration by parts gives

```text
|fhat(k)|<=A_f,n/k^n,
A_f,n=sqrt(2/pi)||D^n f||_TV.
```

The omitted symplectic and thermal covariance tails obey

```text
|sigma-sigma_K|
 <=(A_f A_v+A_g A_u)/[(2n-1)K^(2n-1)],

|mu-mu_K|
 <=1/2 coth(beta K/2)
 [A_f A_u/(2n K^(2n))
  +A_g A_v/((2n-2)K^(2n-2))].
```

The unequal-time two-point tail has the uniform closed-KMS-strip bound

```text
|W(z)-W_K(z)|
 <=1/2 coth(beta K/2)
 [A_f A_u/(2n K^(2n))
  +(A_f A_v+A_g A_u)/((2n-1)K^(2n-1))
  +A_g A_v/((2n-2)K^(2n-2))].
```

The separate infrared estimate

```text
|hhat(k)|<=sqrt(2/pi) k int x|h(x)|dx
```

removes the thermal zero-frequency singularity. Hence the full s-wave
symplectic form, quasifree covariance, Weyl characteristic functions, and KMS
two-point distributions exist after UV removal. Uniform strip convergence
preserves the KMS boundary identity.

For the executable cubic compact bumps, the fourth distributional derivative
is a finite measure. Thus their worst covariance/KMS tail is `O(K^-6)` and the
symplectic tail is `O(K^-7)`. For `C_c^infinity` data the estimates hold at
every order and are superalgebraic.

For disjoint equal-time supports, the full canonical symplectic form vanishes;
the bandlimited leakage is bounded by the same UV tail. This restores
equal-time canonical locality, not yet spacetime microcausality.

Combined with Research Theorem Q, this proves the iterated limit

```text
lim_(K->infinity) lim_(delta->0)
```

and the existence of selected diagonal refinements. Arbitrary joint cutoff
paths, all angular sectors, direct Bunch-Davies identification, Hadamard
structure, and Type `III_1` remain open.

Research Theorem S closes the all-angular equal-time wall-removal part of this
list for the free conformal scalar. Unequal-time Lorentzian and Hadamard/local
factor identification remain open.

Artifacts: `docs/static_patch_uv_removal.md`,
`qgtoy/static_patch_uv_removal.py`,
`tests/test_static_patch_uv_removal.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-uv-removal
```

### Research Theorem S: All-Angular Equal-Time Static-Patch Wall Limit

For the four-dimensional conformally coupled massless scalar, optical
coordinates reduce the angular radial operators to

```text
h_(ell,X)=-d^2/dx^2+ell(ell+1)/(R^2 sinh^2(x/R)).
```

Every half-line operator has spectral bottom zero; high angular momentum does
not create a global Killing-energy gap because states can move toward the
horizon. On a fixed interior interval `(0,B)`, however,

```text
||1_(0,B) 1_[0,E^2](h_ell)||
 <=min(1,E R sinh(B/R)/sqrt(ell(ell+1))).
```

Let `M_L=1+(L+1)(L+2)`. For compactly supported field data with finite angular
`H^s(S^2;L^2_x)` norm, the omitted thermal field covariance is bounded,
uniformly in wall position `X>B`, by

```text
[4B^2/(beta pi^2)+beta/12] M_L^(-s) ||f||_(s,0)^2.
```

For momentum data with common compact radial support in `(0,B)`, define the
energy-weighted angular norm

```text
||g||_(s,E,beta)^2
 =sum_(ell,m)(1+ell(ell+1))^s
 [beta q_ell[g_(ell,m)]/8+3||g_(ell,m)||^2/(2beta)].
```

Then the momentum covariance tail is at most

```text
M_L^(-s) ||g||_(s,E,beta)^2.
```

Fixed-`ell` domain exhaustion, with separate control of the generalized
inverse field term and the square-root momentum term, proves convergence of
each finite angular sum. The wall-uniform tails then give full all-angular
equal-time covariance convergence by an epsilon/three argument.

The exact continuum modes obey the Darboux recurrence

```text
sqrt(q^2+(ell+1)^2) u_(ell+1)
 =(2ell+1)coth(y)u_ell-sqrt(q^2+ell^2)u_(ell-1).
```

The executable evaluator uses stable upward/Miller recurrence plus a
near-origin Frobenius branch. It also verifies the exact conformal identity
between the Euclidean optical thermal kernel and the conformally coupled
Bunch-Davies kernel. The finite partial-wave calculation is a sampled audit,
not the convergence proof.

This theorem does not yet prove unequal-time Lorentzian distributional
convergence, the Hadamard wavefront set, local Type `III_1`, the continuous
core, gravitational constraints, or generalized entropy.

Research Theorem T closes the first four items for the free conformal field by
identifying the compact-test limit with the known Bunch-Davies Hadamard net.
The gravitational constraint and generalized-entropy gates remain open.

Artifacts: `docs/static_patch_all_angular.md`,
`qgtoy/static_patch_all_angular.py`,
`tests/test_static_patch_all_angular.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-all-angular
```

### Research Theorem T: Lorentzian Hadamard Static-Patch Net

For optical spatial distance `d_H`, the conformal thermal two-point kernel on
the lower KMS strip `-2 pi R<Im z<0` is

```text
G_opt(z)=1/[8 pi^2 R^2
 (cosh(d_H/R)-cosh(z/R))].
```

It has the exact positive-type spectral representation

```text
int_0^infinity
 sin(k d_H)/[4 pi^2 R sinh(d_H/R)]
 [exp(-ikz)+exp(-2 pi R k)exp(ikz)]
 /[1-exp(-2 pi R k)] dk.
```

The opposite strip boundaries satisfy the `beta=2 pi R` KMS relation. Under
the conformal pullback, the boundary `z=Delta t-i0` is

```text
Lambda_BD^+(X,X')
 =1/[8 pi^2 R^2(1-Z_(Delta t-i0))],
```

the Bunch-Davies two-point distribution.

For smooth compact spacetime tests with causal hull contained in `x<B` over a
bounded time interval, a wall at `X>B+T` does not affect the associated compact
Cauchy data by finite propagation. Research Theorem S therefore upgrades from
equal-time covariance convergence to convergence of the finite-wall two-point
forms on arbitrary compact spacetime test pairs. The exact strip boundary
identifies the target with `Lambda_BD^+`; full `D'`-topology convergence still
requires a separate equicontinuity bound.

The exact kernel has the local Hadamard coefficient

```text
Lambda_BD^+=1/[8 pi^2 sigma_epsilon]+less singular terms.
```

The full wavefront-set statement uses passivity/KMS microlocal-spectrum and
Hadamard-equivalence theorems. In the global de Sitter Bunch-Davies
representation, Verch's Theorem 3.6(g) then implies that regular-diamond local
algebras, including the static patch viewed as the domain of dependence of an
open hemisphere, are the hyperfinite Type `III_1` factor. KMS plus
Reeh-Schlieder, locality, and Tomita-Takesaki theory identify the faithful patch
modular flow with geometric static time; its continuous core is hyperfinite
Type `II_infinity`.

This continuous core is not yet the gravitational observer algebra. A CLPW
Type-`II_1` corner additionally requires an observer clock, Hamiltonian
constraint, positive-energy projection, and normalized finite trace. No
generalized-entropy identity follows from the free-field classification alone.

Primary theorem dependencies:

- Bros, Epstein, and Moschella, arXiv:gr-qc/9801099;
- Sahlmann and Verch, arXiv:math-ph/0002021;
- Sahlmann and Verch, arXiv:math-ph/0008029;
- Verch, arXiv:funct-an/9609004.

Artifacts: `docs/static_patch_lorentzian_hadamard.md`,
`qgtoy/static_patch_lorentzian_hadamard.py`,
`tests/test_static_patch_lorentzian_hadamard.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-lorentzian-hadamard
```

### Research No-Go U: Energy-Constrained Rotational Frameness Obstruction

Let a proposed full de Sitter gauge completion contain the compact `SO(3)`
stabilizer of a static observer, and suppose the only accessible observer
reference is a rotation-trivial scalar clock while all spectators are
rotation invariant. On the free conformal
Bunch-Davies one-particle collar family, spins through

```text
L_delta=Theta(sqrt(R/delta))
```

have collar trial functions with Rayleigh quotient below a fixed `E0^2`.
Rayleigh-Ritz therefore supplies one actual finite-wall eigenstate below `E0`
in every such sector. In the top certified spin sector, the orthogonal pair

```text
|phi_L> tensor |L_delta,+L_delta>,
|phi_L> tensor |L_delta,-L_delta>
```

has trace distance one, while the `SO(3)` Haar expectation sends both states to
the same maximally mixed spin state. Therefore every decoder through this
canonical compact expectation has worst-case trace-distance error at least
`1/2` on the pair. For recovery of the full fixed-spin quantum system, the
expectation is completely depolarizing and the exact optimal normalized diamond
error is

```text
1-1/(2L_delta+1)^2,
```

and tends to one as `delta` tends to zero. A coherent token over all spins
through `L_delta` has missing-frame relative entropy

```text
2 log(L_delta+1)=log(R/delta)+O(1).
```

This is a conditional compact-fixed-point obstruction for a clock-only
truncation with invariant spectators, not a construction of the noncompact
`SO(1,4)` group average. CLPW already states the qualitative need for an
orthonormal frame in addition to the clock; the candidate contribution is the
hard-energy scaling and exact recovery law. Extending the expectation through a
named crossed product or gravitational corner requires a separate commuting-
square and survival theorem. Covariant observers carrying nontrivial
`SO(1,d)` representations lie outside the hypotheses.

Artifacts: `docs/scalar_clock_rotation_no_go.md`,
`qgtoy/scalar_clock_rotation_no_go.py`,
`tests/test_scalar_clock_rotation_no_go.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy scalar-clock-rotation-no-go
```

### Research Theorem V: Redshifted Charged-Reference Achievability Bound

On the same hard-energy spin sector `L_delta` used in Research No-Go U, compare
the clock-only compact expectation with the canonical prepared `SO(3)`
Peter-Weyl reference

```text
R_J=direct_sum_(j=0)^J V_j tensor V_j^*.
```

For `J>=L`, its covariant measure-and-correct decoder has maximum tensor-rank
deficit at `k=2L`. The exact closed formula and elementary estimates give

```text
(1/2)||Lambda_(L,J)-identity||_diamond
 <= (2L+1)[1-lambda_(2L)(J)]/2
 <= 3(2L+1)^2/(8J).
```

Thus

```text
J_epsilon=ceil[3(2L_delta+1)^2/(8 epsilon)]
```

is sufficient for charged-reference recovery error at most `epsilon`, whereas
the canonical compact expectation under the invariant-spectator clock-only
hypothesis has exact optimal error `1-1/(2L_delta+1)^2`, tending to one.
For the declared rigid-rotor Hamiltonian `H_ref=C_left/(2I)`, the canonical
reference token has

```text
<H_ref>=3J(J+2)/(10I).
```

Since `L_delta^2=Theta(R/delta)`, the sufficient cutoff and fixed-Hamiltonian
mean-energy bounds are

```text
J_epsilon=O(R/(epsilon delta)),
<H_ref>=O(R^2/(I epsilon^2 delta^2)).
```

The energy scaling assumes `I` is fixed independently of `delta` and `epsilon`.
This is a same-target compact-rotation comparison, not a resource-matched
experiment or gravitational energy theorem.
The Peter-Weyl decoder is constructive rather than proved optimal, and the
moment of inertia and rotor Hamiltonian are declared inputs. No local reference
coupling, lifetime/phase-tracking theorem, noncompact boost sector, backreaction
bound, Type-II trace, or
generalized-entropy identity is derived.

Artifacts: `docs/redshifted_rotation_reference_tradeoff.md`,
`qgtoy/redshifted_rotation_reference_tradeoff.py`,
`tests/test_redshifted_rotation_reference_tradeoff.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy redshifted-rotation-reference-tradeoff
```

### Research No-Go W: Covariant-Observer Energy Non-Identifiability

Fix the same truncated `SO(3)` Peter-Weyl representation, canonical token,
orientation POVM, and measure-and-correct decoder used in Research Theorem V.
The channel and its recovery bound depend on `L` and `J`, but not on a separately
assigned reference Hamiltonian.

For every `a_J>0`,

```text
H_J=a_J C_left
```

is positive, has ground energy zero, and commutes with the compact rotation
action. Since the canonical token obeys

```text
<C_left>=3J(J+2)/5,
```

any prescribed positive ground-subtracted token energy `E_J` is realized by

```text
a_J=5E_J/[3J(J+2)].
```

Thus the same target, reference dimension, token, POVM, decoder, and recovery
error admit dynamically inequivalent positive invariant Hamiltonian completions
with arbitrary positive energy profiles. Apart from the trivial positivity bound,
covariance and instantaneous recovery data alone determine no positive universal
lower bound, finite universal upper bound, or stretched-horizon energy exponent.

The fixed-inertia `delta^-2` law in Research Theorem V remains valid inside that
declared rotor model. This no-go says it is not selected by the observer algebra.
It is not a claim that a specified finite-size observer action permits arbitrary
Hamiltonians. A gravitational replacement must derive the frame inertia and
positive Hamiltonian from mass, size, and stress energy, include finite-time
coupling to the static-patch net, and impose a backreaction budget.

Chen-Xu [arXiv:2511.00622v2](https://arxiv.org/abs/2511.00622v2) supplies a
first-order conserved-charge action in `dS_2` and a kinematical
higher-dimensional orthogonal frame on `L^2(SO(1,d))`, but no
higher-dimensional rotational kinetic term or frame inertia. The theorem
therefore identifies an explicit missing dynamical input in that comparison; it
does not criticize or exclude the covariant-observer construction.

Artifacts: `docs/covariant_observer_energy_no_go.md`,
`qgtoy/covariant_observer_energy_no_go.py`,
`tests/test_covariant_observer_energy_no_go.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy covariant-observer-energy-no-go
```

### Research No-Go W2: Mean-Charge And Casimir Substitution Failures

For every spin `j>1`, the pure spin-cat state

```text
|cat_j>=(|j,j>+|j,-j>)/sqrt(2)
```

has `<J_a>=0` for all three axes. Exact ladder-operator evaluation gives

```text
Cov(J_x,J_y,J_z)=diag(j/2,j/2,j^2).
```

For its unitary rotation orbit, `F_ab=4 Cov(J_a,J_b)`, hence

```text
F=diag(2j,2j,4j^2),  rank(F)=3,
Tr(F)=4j(j+1).
```

Thus a classical or quasilocal inequality controlling only `|<J>|` cannot
control rotational QFI, even for a finite irrep. Conversely, the maximally
mixed state on the same irrep has the same Casimir `j(j+1)` and the same energy
under `H=J^2/(2I)`, but its rotation orbit is constant and its QFI vanishes.
Casimir or rotor energy alone therefore does not certify orientation quality.

A third family shows that local QFI is not sufficient global quality. For
integer `j>=2`, let

```text
|psi_j>=sqrt(1-1/j)|0,0>+sqrt(1/j)|cat_j>.
```

Its mean linear spin cost is one and `Tr(F)=4(j+1)`, but every rotated state is
at trace distance `1/sqrt(j)` from the invariant spin-zero state. The rotation
orbit becomes globally uninformative while local QFI diverges.

The robust direction for a class-uniform observer theorem is therefore

```text
small global orientation risk -> robust typical-spin/global asymmetry resource
 -> localized energy cost.
```

Research Theorem W3 now closes the first implication for Haar-prior chordal
cost by independent fusion/Casimir and asymmetry/mean-spin routes. Research
Theorem W3a closes the next implication for confined spinless nonrelativistic
orbital matter and identifies the spectral premise required by any broader
extension. A QFI route would still need a spectral or higher-moment tail
condition. This no-go is kinematic and does not itself prove a gravitational
bound.

Artifacts: `docs/rotational_resource_substitution_no_go.md`,
`qgtoy/rotational_resource_substitution_no_go.py`, and
`tests/test_rotational_resource_substitution_no_go.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m unittest tests.test_rotational_resource_substitution_no_go
```

### Research Theorem W3: Tail-Robust Global SO(3) Orientation Risk

For a Haar-distributed unknown frame and chordal full-frame cost

```text
c(g,g_hat)=sin^2(theta(g_hat^-1 g)/2),
```

let `A_SO3(rho)=D(rho||G(rho))` be the relative entropy of rotational
asymmetry and `Cbar=Tr(rho J^2)`. Every state, arbitrary rotation-trivial
multiplicity space, and arbitrary POVM obeys the independent bounds

```text
R_ref >= 1/(16 Cbar+8),
R_ref >= 6/[e pi^(5/3)] exp[-2 A_SO3(rho)/3].
```

The first follows from the spin-1 fusion matrix and a discrete Hardy
inequality. Strict support through spin `J` sharpens it to
`R_ref>=sin^2[pi/(2J+3)]`.

If `K=sum_j j Tr(P_j rho)` is the mean integer-spin label, then

```text
A_SO3(rho)<=B(K)
 =inf_(beta>0){beta K+log[(1+6e^-beta+e^-2beta)/(1-e^-beta)^3]}.
```

Consequently `R_ref>=6/[e pi^(5/3)] exp[-2B(K)/3]`, with inverse-square
large-`K` scaling. This is a global Bayes theorem and is not weakened by a
vanishing probability in a remote high-spin sector.

For the marked spherical-top EFT, Jensen gives
`K(K+1)<=<J^2>`. Inserting its existing compactness-limited mean-Casimir budget
therefore yields an explicit all-state orientation-risk floor with asymptotic
scaling `G^2/a^4` at fixed constitutive margins. This corollary remains
conditional on that spherical-top inertia law and compactness premise; it is
not a general rotating Einstein-matter theorem.

Under reference-only isotropic `SO(3)` heat diffusion with `s=gamma tau`, the
same spin-1 score is attenuated exactly by `e^(-2s)`. Hence

```text
R_ref(tau)>=3/4[1-e^(-2 gamma tau)]
            +e^(-2 gamma tau)/(16 Cbar+8).
```

This gives an analytic necessary coherence-time ceiling at fixed risk and
Casimir capacity. It is conditional on the heat model; the diffusion rate is
not yet derived from the local Skyrmion/KMS action.

For one fermionic Finkelstein-Rubinstein sector with spins
`1/2,3/2,...,J+1/2`, the corresponding fusion/Hardy results are

```text
R_ref>=1/(16 Cbar),
R_ref>=sin^2[pi/(2J+4)]  for strict cutoff J.
```

Combining the sharp cutoff formula with the fixed-profile Skyrmion
compactness/slow-rotation theorem gives `J_max=173`, physical spin `173.5`, and
`R_ref>=8.056603547090288e-5` for its default audit parameters. This remains a
fixed-profile control result, not a derived local readout or lifetime theorem.

Artifacts: `docs/global_so3_reference_risk.md`,
`qgtoy/global_so3_reference_risk.py`, and
`tests/test_global_so3_reference_risk.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m unittest tests.test_global_so3_reference_risk
```

### Research Theorem W3a: Confined Orbital Representation-Energy Bound

Let finitely many spinless nonrelativistic particles of positive total rest
mass `M` be confined to a rotationally invariant configuration domain with
`|x_i|<=a`. Suppose their nonnegative ground-subtracted excitation Hamiltonian
obeys the quadratic-form inequality

```text
H_ex>=sum_i p_i^2/(2m_i).
```

For every state, including arbitrary rotation-trivial internal multiplicity,
mass-weighted Cauchy-Schwarz gives

```text
<L^2><=2 M a^2 <H_ex>.
```

The global theorem therefore implies

```text
R_ref>=1/[32 M a^2 E_ex+8],
Pr(j>=J+1)<=2 M a^2 E_ex/[(J+1)(J+2)].
```

This controls zero-mean states and rare high-spin tails without a fixed-irrep,
polarization, or local-unbiasedness assumption.

More generally, if a rotationally invariant Hamiltonian has sector floors
`epsilon_j` and

```text
Z_H(beta)=sum_j (2j+1)^2 exp(-beta epsilon_j)<infinity,
```

then every state of mean energy at most `E` obeys

```text
A_SO3<=beta E+log Z_H(beta),
R_ref>=6/[e pi^(5/3)] exp[-2(beta E+log Z_H(beta))/3].
```

The result is independent of rotation-trivial sector multiplicities. The
spectral premise is necessary: the fixed invariant Hamiltonian
`H_bad=sum_j(1-e^-j)P_j` on `L^2(SO(3))` is bounded below one, while normalized
Peter-Weyl kernels through spin `J` have bounded energy and achievable risk
`[4J(J+2)+3]/[4(J+1)(2J+1)(2J+3)/3]=O(1/J)`. Covariance and finite mean energy
alone therefore cannot prove UO.2Q.

Under the separately declared proxy `2G(M+E_ex)/a<=chi<1`, eliminating the
rest/excitation split gives

```text
<L^2><=chi^2 a^4/(8G^2),
R_ref>=1/[8+2 chi^2 a^4/G^2].
```

The compactness line is not a general-relativistic body theorem. Intrinsic
spin, relativistic fields, soft localization, negative interaction energy,
nontrivially rotating species, local readout, stress, lifetime, and metric
response remain outside the theorem.

Artifacts: `docs/localized_orbital_reference.md`,
`qgtoy/localized_orbital_reference.py`,
`qgtoy/rotational_spectral_capacity.py`,
`tests/test_localized_orbital_reference.py`, and
`tests/test_rotational_spectral_capacity.py`.

Representative command:

```bash
python -m pytest -q tests/test_localized_orbital_reference.py \
  tests/test_rotational_spectral_capacity.py
```

### Research Theorem W3a.1: Conditional Class-Uniform Heat-Capacity Bound

Suppose a declared integer-spin observer class proves

```text
C2<=C_max(a,beta),  a<=A(s_opt,rho,beta),
Gamma(T)=integral_0^T gamma(tau)d tau
```

for an isotropic `SO(3)` heat channel. Then every state and every orientation
measurement obey

```text
R(T)>=3/4[1-exp(-2Gamma)]
      +exp(-2Gamma)/[16 C_max(A,beta)+8].
```

For confined orbital matter under the declared compactness condition
`2G(M+E_ex)/a<=chi<1`, this specializes to

```text
R(T)>=3/4[1-exp(-2Gamma)]
      +exp(-2Gamma)/[8+2chi^2 a^4/G^2].
```

At target risk `epsilon`, put
`delta=3/4-(3/4-epsilon)exp(2Gamma)`. Necessarily `delta>0` and, when
`delta<1/8`,

```text
chi a^2/G>=sqrt[(delta^-1-8)/2].
```

Artifacts: `docs/conditional_universal_observer_tradeoff.md`,
`qgtoy/universal_observer_tradeoff.py`,
`qgtoy/localized_orbital_reference.py`,
`experiments/universal_observer_tradeoff_certificate.json` (SHA256
`5c88eb4af23764204333b5e899083c87911066895d70fc132f263e180c175ad6`),
and their focused tests.

Claim boundary: exact class-uniform composition and a proved confined-orbital
corollary. The heat exposure, optical localization map, and capacity must be
derived for the same physical observer; `chi` is compactness admissibility,
not a complete metric-backreaction bound.

### Research Theorem W3b: Supported Skyrmion Collective Spectral Floor

For every massive-Skyrme hedgehog profile hard-supported inside areal radius
`a=x_w/(e f_pi)` with minimum support lapse `N_w=1-lambda x_w^2>0`, the exact
static mass and collective-inertia densities obey

```text
I[F] <= [4/(3N_w)] M[F] a^2.
```

Consequently, minimizing over arbitrary supported hedgehog profile relaxation
inside the adiabatic collective family gives the uniform sector floor

```text
E_j>=sqrt[3N_w j(j+1)/2]/a.
```

This is linear at large spin and therefore has a finite rotational partition
function for every positive inverse temperature. With
`s_w=sqrt(3N_w/2)/a` and `x=exp(-beta s_w)`, one may use

```text
Z_integer<=(1+6x+x^2)/(1-x)^3,
Z_projective<=4sqrt(x)(1+x)/(1-x)^3.
```

Inserting either line into Research Theorem W3a gives an explicit all-state,
rare-tail-robust orientation-risk floor at fixed mean total Killing energy.
The projective line applies to the fermionic `B=1` collective sector.

The theorem avoids a fixed-profile `Omega^4` truncation. Profile relaxation
generically produces a positive quartic term in the collective Lagrangian and
a negative quartic correction to the rigid-rotor Hamiltonian, but the density
bound controls the fully relaxed hedgehog family directly. It does not prove
collective-band completeness, control noncollective rotating modes or
Born-Oppenheimer projection errors, establish isospin access, or include a
marked rotating wall.

Artifacts: `docs/supported_skyrmion_collective_spectral_floor.md`,
`qgtoy/supported_skyrmion_collective_spectral_floor.py`, and
`tests/test_supported_skyrmion_collective_spectral_floor.py`.

Representative command:

```bash
python -m pytest -q \
  tests/test_supported_skyrmion_collective_spectral_floor.py
```

### Research Theorem W3c: Collective-Band Feshbach Transfer And Obstruction

In each rotational sector, decompose the full Hamiltonian with collective-band
projector `P` and `Q=1-P`. If

```text
PHP>=aP,  QHQ>=dQ,  ||QHP||<=v,
```

then the full sector floor obeys

```text
epsilon_full >= [a+d-sqrt((d-a)^2+4v^2)]/2.
```

When `d>=a+Delta` and `v^2<=eta Delta a` with `0<=eta<1`, this implies

```text
epsilon_full >= (1-eta)a.
```

Equivalently, `d_j>=gamma a_j`, `v_j<=rho a_j`, and
`rho^2<gamma` preserve the fraction
`[1+gamma-sqrt((1-gamma)^2+4rho^2)]/2` of every collective floor.

For an eigenstate of energy `E<d`, the same inputs give projection leakage

```text
||Q psi||^2 <= r^2/(1+r^2),  r=v/(d-E).
```

Thus a uniform gap/coupling margin transfers the supported Skyrmion's linear
collective floor to the complete Hamiltonian while simultaneously controlling
the collective-current projection error.

The hypotheses are necessary information. For any `0<delta<=1`, the positive
block Hamiltonian

```text
[[a,(1-delta)a],[(1-delta)a,a]]
```

preserves the collective block `PHP=aP` but has full floor `delta a`.
Therefore fixed-profile mass, inertia, and collective spectral data alone do
not imply any uniform full-band fraction. Even diagonal floors `A_j` and
`2A_j` can be mixed to retain a fixed full floor `Delta` by choosing
`v_j^2=(A_j-Delta)(2A_j-Delta)`. The radial results below now control the
fixed-wall and coupled spherical profile-membrane channels, but not the anchor,
nonspherical complement, or their off-band couplings. No quantum collective
projector, compression inequality, or off-band coupling norm is currently
certified.

Artifacts: `docs/collective_band_feshbach_gate.md`,
`qgtoy/collective_band_feshbach.py`, and
`tests/test_collective_band_feshbach.py`.

Representative command:

```bash
python -m pytest -q tests/test_collective_band_feshbach.py
```

### Research Theorem W3d: Authenticated Fixed-Wall Radial Dynamic Gap

For a time-dependent radial Skyrme hedgehog, linearization about a static
profile gives the generalized Sturm-Liouville problem

```text
L_Jacobi eta=omega_hat^2 W eta,
W=(x^2+8sin^2F)/N.
```

On a hard-supported worldtube `0<=x<=x_w` with
`N_w=1-lambda x_w^2>0`,

```text
W<=(x_w^2+8)/N_w.
```

Therefore a Jacobi form bound `L_Jacobi>=alpha` on the complete physical
radial fluctuation domain implies

```text
omega_hat_0^2>=alpha N_w/(x_w^2+8),
omega_K=e f_pi omega_hat.
```

An authenticated successor now proves the missing premise for the exact AU.1
solution with an ideal fixed wall. Correlated polynomial/Newton-tube replay
gives `(L_Jacobi v)/v>1.0386099769` on `[1/16,4]`. A nonsingular origin
representation gives `(L_Jacobi v)/v>36.8298881657` on `[0,1/16]`. Since
regular modes have `eta=O(x)`, `P=O(x^2)`, and `eta(4)=0`, both endpoint terms
in the ground-state transform vanish. Therefore

```text
L_Jacobi>=1,
omega_hat_rad^2>=1/25,
omega_hat_rad>=1/5,
omega_K>=e f_pi/5.
```

This is a physical full-domain theorem for the fixed-wall `l=0` field mode. It
does not include membrane motion, anchor modes, nonspherical channels, or the
collective-band projection/coupling problem.

Artifacts: `docs/skyrmion_radial_dynamical_gap.md`,
`qgtoy/skyrmion_radial_dynamical_gap.py`,
`qgtoy/validated_skyrmion_radial_gap.py`, and
`experiments/skyrmion_full_radial_gap_exact_certificate.json` (SHA256
`46795f66ac628ed4c879a595bbd4d0ce8d0f909a299569d7a05fe04433011959`).

Representative command:

```bash
python -m pytest -q tests/test_skyrmion_radial_dynamical_gap.py tests/test_validated_skyrmion_radial_gap.py
```

### Research Theorem W3e: Authenticated Coupled Profile-Membrane Radial Gap

For a spherical Nambu-Goto membrane in static Young-Laplace equilibrium, let
`y=F_0'(a)<0` and `u=lambda a^2`. The moving ideal-mirror condition is

```text
eta(a)+yq=0.
```

Eliminating the membrane displacement from the exact quadratic forms gives

```text
V=q_J[eta]+B_0 eta(a)^2,
T=integral W eta^2 dx+M_0 eta(a)^2,
M_0=a^3/[2(2-3u)],
B_0=a(1-2u)+a(2-9u+6u^2)/[2(2-3u)].
```

The common factor `y^2` cancels by Young-Laplace balance. At the authenticated
wall `a=4`, `lambda=1/400`,

```text
M_0=800/47,  B_0=6386/1175.
```

For the positive witness `v=1/[(x-9/4)^2+8]`, correlated exact-solution replay
proves `L_Jacobi v/v>=1/100` on the full regular-origin interval. Its moving
wall coefficient is the exact positive rational

```text
B_0+P(4)v'(4)/v(4)=39878/69325.
```

Since `W<=25`, the complete coupled spherical profile-membrane form obeys

```text
omega_hat_l0^2 >= min[(1/100)/25,
                      (39878/69325)/(800/47)]
                  =1/2500,
omega_hat_l0>=1/50,
omega_K>=e f_pi/50.
```

The authenticated replay has 95 positive-radius leaves, maximum refinement
depth five, recomputed positive-radius quotient `>0.01297111385`, and regular
origin quotient `>37.27705445`. This theorem includes membrane motion but not
the anchor, nonspherical profile/membrane modes, rotational collective modes,
or their Feshbach couplings.

Artifacts: `docs/skyrmion_moving_wall_radial_gap.md`,
`qgtoy/validated_skyrmion_moving_wall_gap.py`, and
`experiments/skyrmion_moving_wall_radial_gap_exact_certificate.json` (SHA256
`2bb48f770504ab5a0a0f9b3139b881877a414ddb9b8c19cd34c81bfd26b42686`).

Representative command:

```bash
python -m pytest -q tests/test_validated_skyrmion_moving_wall_gap.py
```

### Research Theorem W3f: Branch-Coordinate Added-Mass Transfer

Let `F_a` be a `C^2` exact static Dirichlet branch and
`chi=partial_aF_a`. Writing `eta=h+qchi` removes the potential cross term. If
`k=E_branch''/pi`, `Z=<chi,Wchi>`, `m=M_wall/pi`, and `W<=W_max`, then, with
`S=alpha(Z+m)+kW_max` and `D=W_max m`,

```text
omega_hat_coupled^2 >=
2 alpha k/[S+sqrt(S^2-4D alpha k)].
```

The default `k` and `Z` remain floating diagnostics; without controlling `Z`,
the pure branch-coordinate trial gives `omega_min^2<=k/(Z+m)->0`. This does not
reopen W3e. It only limits this potentially sharper estimate, whose current
floating value is approximately `0.198`.

Artifacts: `docs/coupled_radial_wall_gap.md`,
`qgtoy/coupled_radial_wall_gap.py`, and
`tests/test_coupled_radial_wall_gap.py`.

### Research Theorem W3g: Spherical Hamiltonian-Constraint Response

For spherical time-symmetric data in areal radius, set

```text
f(r)=N(r)-2Gm(r)/r,
N(r)=1-r^2/R^2,
q(r)=2Gm(r)/[rN(r)].
```

If `sup q<=beta<1`, then `f>=N(1-beta)>0` and

```text
0<=g_rr/g_rr,dS-1<=beta/(1-beta).
```

Wall compactness alone cannot imply this bound: a nonnegative uniform core of
radius `epsilon` followed by vacuum to a support wall `a` has
`q(epsilon)=C_wall a/[epsilon N(epsilon)]`, which can exceed one while
`q(a)=C_wall/N(a)` is arbitrarily small.

For the authenticated Skyrmion field, exact cumulative energy replay gives the
bulk supersolution coefficient

```text
H_bulk=sup_x c_0(x)/[x(1-lambda x^2)]
      <=29.246335626859388.
```

The self-consistent spherical mass equation with the certified field held fixed
is linear, `c'+k(x)c=c_0'` with `k>=0`, so `c<=c_0`. Therefore
`alpha H_bulk<1`, `alpha=2G/(e^2R^2lambda)`, closes the bulk radial constraint
and excludes a first zero of `f`. The maximum certified cell is internal. The
fixed-background exterior coefficient has lower bound `10.634609934327349`, so
an endpoint estimate alone can underprice the local response substantially.

At `beta=1/2`, `R^2/G=10^6`, and `lambda=1/400`, the directed sufficient bulk
condition is `e^2>=0.04679413700297502`. This theorem does not solve the lapse,
self-gravitating field, membrane junction, rotating, or nonspherical equations.
The membrane mass is only a fixed-background test-source diagnostic.

Artifacts: `docs/skyrmion_spherical_constraint.md`,
`qgtoy/spherical_static_patch_constraint.py`,
`qgtoy/validated_skyrmion_constraint.py`, and
`experiments/skyrmion_spherical_constraint_exact_certificate.json` (SHA256
`a180610fbdea4eecd75cdc7628216adab9289d5561704f60f750f7105fcaca47`).

Representative command:

```bash
python -m pytest -q tests/test_spherical_static_patch_constraint.py tests/test_validated_skyrmion_constraint.py
```

### Research Theorem W3h: Collective Gravity-To-Orientation Bound

Assume the fixed spherical Skyrmion field and its leading collective rotor obey
the radial metric budget `q<=beta<1`. Then `A>=N(1-beta)`, and the explicit
static mass and inertia densities imply

```text
c_M[A]>=(1-beta)c_M[N],
c_I[A]<=c_I[N]/(1-beta).
```

Writing `Xi=2G/(R^2lambda)`, the bulk wall constraint therefore satisfies

```text
q_w >= Xi(1-beta)/(x_wN_w)
       [c_M/e^2+e^2<J^2>/(2c_I)].
```

AM-GM eliminates `e` and gives the necessary capacity and global-risk bounds

```text
<J^2> <= [beta x_wN_w/(Xi(1-beta))]^2 c_I/(2c_M),
R_ref >= 1/(16<J^2>_max+8).
```

The authenticated AU.3b bulk constants, rounded outward, are
`c_M>=33.833816` and `c_I<=48.390986`. At `beta=1/2`, `x_w=4`,
`lambda=1/400`, and `R^2/G=10^6`, they imply

```text
<J^2><=16476538.109682929,
R_ref>=3.79327245124592e-9.
```

This is the first authenticated local-gravity to rotational-Casimir to global-
orientation-risk chain in the project. It is conditional on the fixed field,
spherical radial metric, and leading collective rotor. It excludes membrane
energy and does not control the lapse, anisotropic stress, collective
projection, higher-order rotation, or a rotating Einstein-Skyrme solution.

Artifacts: `docs/skyrmion_rotational_backreaction.md`,
`qgtoy/spherical_rotational_backreaction.py`, and
`experiments/skyrmion_rotational_backreaction_exact_certificate.json` (SHA256
`7bfb5119a89da2bffbca47a5794e7bbf756f5bc4ea1d1b51877b216ac1a33433`).

Representative command:

```bash
python -m pytest -q tests/test_spherical_rotational_backreaction.py tests/test_skyrmion_rotational_backreaction_audit.py
```

### Research Theorem W3i: Authenticated Static Bulk Lapse Control

For the fixed static spherical Skyrmion, the exact stress identity is

```text
rho_bar+p_r_bar=A F'^2[1/4+2sin^2(F)/x^2].
```

The radial metric factor cancels from the spherical lapse equation. Defining

```text
D=2pi int_0^xw xF'^2[1/4+2sin^2(F)/x^2]dx,
```

the exterior-normalized bulk lapse obeys `sigma>=exp(-alpha D)`. Combining this
with the sufficient radial condition `alpha H_upper<=beta` gives

```text
log[1/sigma(0)]<=beta D_upper/H_upper,
|g_tt|/|g_tt,dS|>=(1-beta)exp[-2beta D_upper/H_upper].
```

Authenticated replay gives `D<=43.445333` and uses `H<=29.246336`. At
`beta=1/2`, the exact rational log-lapse bound is approximately
`0.7427483053`; the resulting `g_tt` ratio diagnostic is `0.1131949426`.
Thus the default is controlled but not a useful negligible-backreaction point.

The theorem excludes collective rotation, field deformation, membrane lapse
matching, nonspherical stress, and off-center support.

Artifacts: `docs/skyrmion_static_lapse_control.md`,
`qgtoy/skyrmion_lapse_control.py`, `qgtoy/validated_skyrmion_lapse.py`, and
`experiments/skyrmion_static_lapse_exact_certificate.json` (SHA256
`2072131929fd5c9ff70ced4e468aa5dd937cc84cbffe9efd83529cfa6693171b`).

Representative command:

```bash
python -m pytest -q tests/test_skyrmion_lapse_control.py tests/test_skyrmion_static_lapse_audit.py
```

### Research Theorem W3j: Leading Rotational Stress Multipole Fork

For any reference state, let

```text
S_ab=<{J_a,J_b}>/2,
C=Tr(S)=<J^2>,
Q=S-C I_3/3.
```

Positivity of `S` and the exact fourth spherical moment give

```text
||Q||_op<=2C/3,
||Q||_F<=sqrt(2/3)C,
RMS_(S2)(nQn)<=2C/(3sqrt(5)).
```

The leading hedgehog inertia projector fixes the rotational shell energy to

```text
dE_rot/(dr dOmega)=3i(r)[2C/3-nQn]/(16pi I^2).
```

Consequently the radially and angularly integrated absolute spin-two energy is
at most `E_rot/sqrt(5)`. The bound is asymptotically approached in its tensor
norm by high-spin coherent/cat-like states.

There is also an exact escape branch. The pure spin-2 state

```text
(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2)
```

has `S=2I_3`, `Q=0`, and pure-state rotational QFI `8I_3`. Hence its leading
spin-two stress vanishes while its local rotation orbit is sensitive in all
three directions. A universal no-go cannot assume that accurate rotational
references necessarily generate quadrupolar gravity. The spherical monopole
theorem survives on the `Q=0` branch through quadratic collective order; the
all-state branch now reduces to bounding the static-patch `l=2` Einstein
response to the source norm above.

This particular state is not a globally accurate frame: Research Theorem W3k
below proves that its exact half-turn stabilizer forces `R_ref>=1/2`.

This theorem does not solve the radial spin-two equations, remove the finite
stabilizer ambiguity, or control `Omega^4`, collective projection, membrane,
and off-center effects.

Artifacts: `docs/rotational_stress_multipole.md`,
`qgtoy/rotational_stress_multipole.py`, and
`experiments/rotational_stress_multipole_exact_certificate.json` (SHA256
`13bfaa681377caef32875a03f9a5c313e7fecb4f17cde5c2e191a8f8810fe07e`).

Representative command:

```bash
python -m pytest -q tests/test_rotational_stress_multipole.py tests/test_rotational_stress_multipole_audit.py
```

### Research Theorem W3k: Stabilizer-Induced Global Orientation Risk

If `U(h)rho U(h)^*=rho` for a rotation `h` of principal angle `alpha`, then
every Haar-prior `SO(3)` orientation protocol with chordal frame cost obeys

```text
R_ref>=sin^2(alpha/4).
```

Indeed, the hypotheses `g` and `gh` give identical states. Pairing their costs
reduces the problem to

```text
R_ref>=(1/2)min_x[c(x)+c(xh)].
```

The singular values of `I+R(h)` are
`2,2cos(alpha/2),2cos(alpha/2)`, so the orientation-preserving Procrustes
maximum gives the stated bound.

For the explicit spin-2 second-order-anticoherent state in W3j, rotation by
`pi` around the quantization axis fixes every occupied `m=-2,0,2` component.
Therefore

```text
Q=0, F_Q=8I_3, but R_ref>=1/2.
```

This closes that finite-spin state as an operational escape from the global
observer theorem. It does not exclude `Q=0` states with trivial stabilizer or
asymptotically free cross-spin families.

Artifacts: `docs/orientation_stabilizer_risk.md`,
`qgtoy/orientation_stabilizer_risk.py`, and
`experiments/orientation_stabilizer_risk_exact_certificate.json` (SHA256
`5043d84e063051e8b730612a096b57dcafda2b30b7614facb0ac95003ff5f54b`).

Representative command:

```bash
python -m pytest -q tests/test_orientation_stabilizer_risk.py tests/test_orientation_stabilizer_risk_audit.py
```

### Research Theorem W3l: Einstein Response Requires Gauge And Full Stress

No coordinate-component metric norm can be bounded by a source norm before
fixing or quotienting gauge. On any Einstein background, a compact pure-gauge
perturbation `h=L_xi g` has zero linearized Einstein source while its coordinate
amplitude scales freely.

Energy density alone remains insufficient even for gauge-invariant curvature.
In the local flat limit, for any compact smooth `chi`,

```text
T_00=T_0i=0,
T_ij=A(delta_ij Delta-partial_i partial_j)chi
```

is conserved, has zero energy density, but gives

```text
T=2A Delta chi,
R^(1)=-16pi G A Delta chi.
```

Choosing `chi=f(r)Y_2m` makes the response quadrupolar. Hence the W3j
energy-density bound cannot by itself be inserted into an Einstein-response
norm. A valid theorem must use a gauge-invariant output or fixed gauge and a
norm controlling the full conserved density, pressure, momentum, and shear
source, including membrane traction.

Artifacts: `docs/density_only_einstein_response_no_go.md`,
`qgtoy/density_only_einstein_response_no_go.py`, and
`experiments/density_only_einstein_response_no_go_certificate.json` (SHA256
`54d4d33642198274f656fc1e87ea631a5b7dead8ec18da4dbfdd58f2d57f7b7c`).

### Research Theorem W3m: Fixed-de Sitter Static Quadrupole Resolvent

For the gauge-invariant static even-parity `l=2` master field on pure de
Sitter,

```text
A_2 Psi=F,
A_2=-d/dr[(1-r^2/R^2)d/dr]+6/r^2,
```

with `Psi=O(r^3)` at the center and `(1-r^2/R^2)Psi'->0` at the horizon. The
Friedrichs form obeys

```text
A_2>=6/R^2,
||Psi||_2<=(R^2/6)||F||_2.
```

Writing `x=r/R`, the center-regular and no-log horizon solutions are

```text
u=15(3-x^2)atanh(x)/(4x^2)-45/(4x),
v=(3-x^2)/(2x^2),
(1-x^2)(uv'-u'v)=-15/2.
```

The exact positive Green kernel is

```text
G_2(r,s)=(2R/15)u(min(r,s)/R)v(max(r,s)/R).
```

At proper horizon distance `rho=R arccos(r/R)`, its diagonal susceptibility is

```text
G_2(r,r)=R log(2R/rho)-3R/2+o(R).
```

This logarithmic near-horizon quadrupole susceptibility is a candidate novel
observable. The theorem acts on the conserved Zerilli master source `F`; W3l
proves that W3j's energy multipole alone is insufficient to determine it.

Artifacts: `docs/static_patch_l2_response.md`,
`qgtoy/static_patch_l2_response.py`, and
`experiments/static_patch_l2_response_exact_certificate.json` (SHA256
`45871bfe3e15a65b546eddd6391d42d0d8e6665ee981c9f24618409f52dcd051`).

Representative command:

```bash
python -m pytest -q tests/test_static_patch_l2_response.py tests/test_static_patch_l2_response_audit.py
```

### Research Theorem W3n: Static Even-Stress Conservation Gate

On `ds^2=-fdt^2+dr^2/f+r^2dOmega^2`, write a static even-parity multipole as

```text
delta T^t_t=-rho Y,                 delta T^r_r=p_r Y,
delta T^r_A=j D_A Y,                delta T^A_B=p_perp Y delta^A_B+pi Y^A_B,
Y^A_B=D^A D_B Y+[ell(ell+1)/2]delta^A_B Y.
```

Then smooth bulk conservation is equivalent to

```text
p_r'+f'(rho+p_r)/(2f)+2(p_r-p_perp)/r-ell(ell+1)j/(fr^2)=0,
j'+2j/r+p_perp-[ell(ell+1)-2]pi/2=0.
```

In particular, a static `ell=2` source with `j=0` must satisfy
`p_perp=2pi`. Hard truncation at `r=r_w` also creates radial and angular
delta coefficients `-p_r(r_w)` and `-j(r_w)`. A valid worldtube source must
therefore satisfy both bulk conservation and membrane traction balance before
it is projected into W3m's master equation.

Artifacts: `docs/static_even_stress_conservation.md`,
`qgtoy/static_even_stress_conservation.py`, and
`experiments/static_even_stress_conservation_certificate.json` (SHA256
`ffdd21d1ca7e5c33df825bb7f0ba57b0d816916f34f1ea23e383f804c7299856`).

### Research Theorem W3o: Fixed-Profile Rigid Source No-Go

For the leading fixed-profile rotating Skyrme hedgehog, let

```text
N=1-r^2/R^2,  a^2=NF'^2,  b^2=sin^2(F)/r^2,
k_2=f_pi^2 sin^2(F)/(8N),  k_4=sin^2(F)/(2e^2N),
q(n)=Q_ab n^a n^b.
```

The stationary mean-zero `ell=2` stress coefficients are

```text
rho=-[k_2+k_4(a^2+b^2)]q/I^2,
p_r=-[k_2+k_4(b^2-a^2)]q/I^2,
p_perp=-[k_2+k_4a^2]q/I^2,
pi=-k_4b^2q/I^2,
j=0.
```

Their angular conservation residual is

```text
p_perp-2pi=-[k_2+k_4(a^2-2b^2)]q/I^2,
```

and is generically nonzero. At a Dirichlet wall with
`F=sigma(r_w-r)+O((r_w-r)^2)`, its leading coefficient is strictly negative
for nonzero `sigma`:

```text
-sigma^2[f_pi^2/8+N_w sigma^2/(2e^2)]q/(N_w I^2).
```

The radial conservation residual is independently nonzero in general. All
fixed-profile rotational tractions vanish at the ideal wall, so no omitted
wall delta can repair this bulk defect. Hence the undeformed rigid rotor is not
an admissible static Zerilli source. One must solve the `O(Omega^2)`
centrifugal matter and membrane deformation, use the time-dependent
gravitational problem, or restrict to the leading `Q=0` branch. This does not
exclude a conserved deformed rotating Skyrmion.

Artifacts: `docs/rigid_skyrmion_stress_conservation.md`,
`qgtoy/rigid_skyrmion_stress_conservation.py`, and
`experiments/rigid_skyrmion_stress_conservation_certificate.json` (SHA256
`a91577f62a2992f3aca8c7ffe9af171c6c5759a0dcff80550c3dff5240286bfe`).

### Research Theorem W3p: Centrifugal Two-Channel And Wall Gate

The most general Hata-Kikuchi equivariant coordinate deformation at
`O(Omega^2)` splits on a spherical background into one monopole and a rank-two
quadrupole:

```text
d0=x^3[2(A-C)/3-2B],
d2=-x^3(A-C),
t2=x^3C.
```

In regular physical quadrupole fields,

```text
delta Y=f q e_F+g(Qn-qn),
f=-x^3F'(A-C),
g=sin(F)x^2C.
```

The exact scalar restriction is

```text
[-(P f')'+Q2 f]=-4E_H,
P=N(x^2+8sin^2F),
Q2=Q0+6(1+4sin^2F/x^2),
```

where `Q0` is the radial Jacobi potential and

```text
E_H=x^2/N {sinF cosF[1/4+2sin^2F/x^2-NF'^2]
            -sin^2F[NF''+2NF'/x]}.
```

Its source is exactly tied to W3o's radial conservation defect by
`C_rigid,r=-(F'/x^2)E_H`. The independent angular defect is not removed by
this scalar equation. Direct angular reduction of the target-space second
variation produces a symmetric local Hessian in `(f,g,f',g')`, reproduces the
scalar Jacobi block, and gives a generically nonzero rotational source in the
`g` channel. Hence the centrifugal quadrupole is a coupled two-field problem,
not a corrected radial profile.

For a moving ideal mirror, `xi2=a^3(A-C)` and `g(a)=0`. A pure-tension wall
supplies

```text
delta K2=[K'(a)+6/(a^2sqrt(N_a))]xi2.
```

The exact normal-force condition is the Robin law

```text
(A-C)'=[N'/(2N)-3/a
        -4sigma(K'+6/(a^2sqrt N))/(N F_w'^2)](A-C).
```

Its default multiplier is `-1.0236037233500035`. Thus a movable Nambu-Goto
wall can support the quadrupole at this linear fixed-background level; holding
the wall spherical instead forces both `(A-C)(a)=0` and `(A-C)'(a)=0` unless
an anchor supplies the reaction.

This theorem supplies the local coupled Hessian, source covector, and wall
gate, but not the global solution, coercivity, conserved completed stress,
Israel junction, or Zerilli projection.

Artifacts: `docs/centrifugal_skyrmion_deformation.md`,
`qgtoy/centrifugal_skyrmion_deformation.py`, and
`experiments/centrifugal_skyrmion_deformation_certificate.json` (SHA256
`5d545c1753dc3fb78c3c05fc2005ef450dd46f346b20788b12ed33ec3697a58d`).

### Research Theorem W3q: Exploratory Global Centrifugal Branch

Writing W3p's local Hessian as

```text
delta^2E=y^TCy+2y^TDy'+y'^TAy',  y=(f,g),
```

and its rotational source as `s0^Ty+s1^Ty'`, the global equation is

```text
-(Ay'+D^Ty)'+Dy'+Cy=s0-s1'.
```

The origin indicial roots on the default branch are

```text
p=1,3,-2,-4,
```

with regular ratios `f/g=-1.00000000299` and `0.04172747341`. Imposing their
two-dimensional regular subspace together with W3p's wall conditions
`g(a)=0`, `f'(a)=-0.7527703900842937 f(a)` gives a numerically regular default
solution:

```text
max|f|=0.3053035319,
max|g|=0.2735765404,
integral(f^2+g^2)dx=0.1952068369,
xi2=-f(a)/F'_w=-0.2873444807.
```

The `201`-to-`401` mesh change at six sample radii is `1.30e-4`; the
`0.02`-to-`0.01` origin-cutoff change is `8.45e-6`; and the background-profile
step change from `0.002` to `0.001` is `1.61e-7`. Algebraic and wall residuals
are below `5e-13`.

This is step-converged exploratory evidence, not validated numerics. It shows
that the correct two-channel moving-wall completion is not immediately driven
to a large or singular response at the default point, so W3o's rigid-source
failure should not be advertised as a physical no-go. Existence, uniqueness,
coercivity, membrane distributional conservation, Israel matching, and the
Zerilli observable remain open. W3r separately supplies floating smooth-bulk
stress closure on this branch.

Artifacts: `docs/centrifugal_skyrmion_bvp.md`,
`qgtoy/centrifugal_skyrmion_bvp.py`, and
`experiments/centrifugal_skyrmion_bvp_certificate.json` (SHA256
`ddc489d4b0b5b3bcbd71fd36afd1b217f58b04c13cbdbb0f2be7ff7df9f95a76`).

### Research Theorem W3r: Same-Action Bulk Stress Closure

The first Hilbert variation of the static Skyrme stress on W3q's physical
fields `(f,g)`, added to W3o's rigid rotational quadrupole, supplies all five
static even-parity amplitudes `(rho,p_r,p_perp,j,pi)`. The rigid terms agree
coefficient by coefficient with W3o, while the deformation generates the
radial-angular shear required by the independent angular equation.

Applying W3n's exact conservation gate away from the origin and wall gives the
following maximum residual sequence:

```text
nodes             101        201        401        801
radial          1.01e-1    3.02e-2    8.36e-3    2.21e-3
angular         3.27e-3    8.20e-4    2.06e-4    5.21e-5
completed/rigid 3.45e-2    1.03e-2    2.85e-3    7.55e-4.
```

Both completed residuals decrease by factors below `0.35` at every mesh
doubling, while the rigid residual remains near `2.93`. This is
source-hashed, second-order floating evidence that W3q restores the smooth-bulk
Hilbert identity. It is not an interval proof and does not establish membrane
distributional conservation, Israel matching, collective projection, or a
Zerilli observable.

Artifacts: `docs/centrifugal_skyrmion_completed_stress.md`,
`qgtoy/centrifugal_skyrmion_completed_stress.py`, and
`experiments/centrifugal_skyrmion_completed_stress_certificate.json` (SHA256
`79f588642456d91eb58107de613a639566af0e7924cd29e8d480bf109ecea5db`).

### Research Theorem W3s: Distributional Membrane Completion

For a moving constant-tension shell `r=a+xi q(n)`, the covariant Nambu-Goto
stress has the quadrupole distribution amplitudes

```text
rho_Sigma=sigma xi[N'/(2sqrt N) delta-sqrt N delta'],
p_r,Sigma=pi_Sigma=0,
j_Sigma=-sigma xi sqrt N delta,
p_perp,Sigma=-rho_Sigma.
```

The `delta'` term is the coordinate expansion of a displaced ordinary shell,
not an independent dipole layer. With

```text
K=N'/(2sqrt N)+2sqrt N/r,
k_l=K'(a)+l(l+1)/(a^2sqrt(N_a)),
```

its exact divergence is

```text
C_r,Sigma=-sigma xi K delta'+sigma xi k_l delta,
C_A,Sigma=-sigma xi K D_Aq delta.
```

Adding the displaced-background layer from
`T_0 Theta(a+xi q-r)` factorizes total distributional conservation into the
centered Young-Laplace equation and the linearized wall laws

```text
p_0=sigma K,
p_r,2+xi p_0'=sigma k_2 xi,
j_2+xi(p_0-p_perp,0)=0.
```

The last identity follows exactly from the ideal-mirror data `f=-F'_w xi`,
`g=0`; the normal identity is precisely W3p's Robin condition. On W3q's four
meshes the largest bulk-plus-shell distributional coefficient is below
`1.19e-12`, the tangential residual is zero at floating precision, and the
analytic factorization error is below `6e-20`.

This closes fixed-background first-order distributional conservation for the
default branch. It is not an interval proof and does not supply Israel
matching, self-gravity, surface elasticity, or the Zerilli source map.

Artifacts: `docs/centrifugal_skyrmion_membrane_stress.md`,
`qgtoy/centrifugal_skyrmion_membrane_stress.py`, and
`experiments/centrifugal_skyrmion_membrane_stress_certificate.json` (SHA256
`1ef92b3579f60fe52d2849d3da3202dc55be33be538b401117218f81cdea53aa`).

### Research Theorem W3t: Exact Conserved-Stress Master Source

Fix Regge-Wheeler gauge by

```text
h_tt=N H0 Y,  h_rr=H2 Y/N,  h_AB=r^2 K Y gamma_AB,
```

and the `ell=2` Zerilli-Moncrief normalization

```text
Psi=r[K+N(H2-rK')/2]/3.
```

Direct elimination of the sourced linearized Einstein equations on pure de
Sitter gives

```text
A_2 Psi=F,
F=kappa[-r^2N rho'/6+r(1+4r^2/R^2)rho/6
        -r p_r/2-j+2r pi],
kappa=8piG.
```

For general canonical stress jets through `delta'`, the executable derives the
resulting `delta`, `delta'`, and `delta''` master coefficients. The `delta''`
term generated by a displaced ideal shell is an explicit contact in the
metric-defined master field. Subtracting that contact gives an equivalent
`delta`-plus-`delta'` source and exactly preserves both branches of the off-wall
Green response. The harmonic normalization is tracked by
`integral(Q_ab n_a n_b)^2dOmega=(8pi/15)Tr(Q^2)`.

The identity is exact in the frozen fixed-de-Sitter convention and has an
independent Einstein-tensor audit. It does not supply a sourced
Kodama-Ishibashi cross-check, physical collective normalization, Israel
matching, or a Weyl/worldtube observable.

Artifacts: `docs/static_patch_l2_master_source.md`,
`qgtoy/static_patch_l2_master_source.py`, and
`experiments/static_patch_l2_master_source_certificate.json` (SHA256
`3be17612134bb6b72535db9d3c80a74acf1271a39e04eec4b1591c9bd8967887`).

### Research Theorem W3u: Completed Skyrmion Master Response

Composing W3q-W3t gives a nonzero gauge-invariant master response for the
default completed matter-wall source. Per unit dimensionless Einstein coupling
`kappa_hat` and per dimensionless angular-velocity harmonic `q_hat`, the
801-node response coefficient is

```text
r       1          2          3          5          10
psi0 -0.220896  -0.330207  -0.176182  -0.0662061  -0.0154951.
```

The `401`-to-`801` maximum relative change is `1.06e-4`; the finest
origin-cutoff and profile-step changes are `2.99e-5` and `2.87e-7`. The ideal
shell's raw `delta''` contact is retained in the ledger and removed only in the
equivalent off-wall representation.

This is a source-hashed floating positive construction. Physical normalization
is supplied by W3w below, but interval validation, Israel matching,
deformed-background response, higher rotation, and invariant curvature
reconstruction remain open.

Artifacts: `docs/centrifugal_skyrmion_master_response.md`,
`qgtoy/centrifugal_skyrmion_master_response.py`, and
`experiments/centrifugal_skyrmion_master_response_certificate.json` (SHA256
`07c66bb0731588a268db1398f9714746dd43b1e666867d004ee472e525873437`).

### Research Theorem W3v: Exact Ideal-Shell Master Transmission

For a literal source

```text
F=D0 delta+D1 delta'+D2 delta'',
A_2 Psi=-(N Psi')'+6Psi/r^2,
```

write `Psi=c delta+Psi_off` and `[X]=X(a+)-X(a-)`. Exact distributional
differentiation gives

```text
c=-D2/N_a,
D1_off=D1+D2 N'_a/N_a,
D0_off=D0+6D2/(a^2 N_a),
[Psi_off]=-D1_off/N_a,
[N Psi_off']=-D0_off.
```

Independent two-sided limits of
`D0_off G_2(r,a)-D1_off partial_a G_2(r,a)` reproduce both jumps. For W3u's
401-node shell, the field and flux jumps per unit coupling and harmonic are
`-0.0025531731` and `0.0023617911`. This proves that the contact-subtracted
response solves the declared distributional master equation; it is not a
tensorial Israel-matching theorem.

Artifacts: `docs/static_patch_l2_transmission.md`,
`qgtoy/static_patch_l2_transmission.py`, and
`experiments/static_patch_l2_transmission_certificate.json` (SHA256
`c83536779d2ab62684218291dd99de190569f9973417d9accd2ceff426901ade`).

### Research Theorem W3w: Physical Collective Master Normalization

In natural units, the repository action fixes

```text
x=e f_pi r,  T0=e^2 f_pi^4,
I_phys=c_I/(e^3 f_pi),  kappa_hat=8piG f_pi^2.
```

For `S_ab=<{J_a,J_b}>/2`, `C=Tr S`, and
`QJ_ab=S_ab-delta_ab C/3`, rigid collective quantization gives

```text
Omega_hat=e^2 J/c_I,
Psi_phys(r,n)=(8piG e^3 f_pi/c_I^2)
              psi0(x) QJ_ab n_a n_b.
```

The wrapper validates a fixed-spin density matrix and computes
`c_I=34.26620155247604` from the same default background profile. It reports
physical radii, the master tensor, its exact angular RMS, and the hard-support
control `epsilon_rot=e^2 sqrt[j(j+1)]/c_I`. A spin-2 cat has a nonzero response, whereas
the second-order-anticoherent tensor `S=2I_3` has exactly zero leading
quadrupolar response. Thus the gravitational signal is state dependent and is
not determined by Casimir alone.

This is a physical master amplitude, not yet a local observable. Off-wall Weyl
reconstruction, tensorial Israel matching, collective-band control, and
higher-order rotation remain open.

Artifacts: `docs/centrifugal_skyrmion_physical_response.md`,
`qgtoy/centrifugal_skyrmion_physical_response.py`, and
`experiments/centrifugal_skyrmion_physical_response_certificate.json` (SHA256
`fc8ae96c6215c4dbe7c8905bbfb59a80cb12cd96e7a3dc9c3849a973174b9470`).

### Research Theorem W3x: Exterior Electric-Weyl Reconstruction

Outside the completed source, exact inversion of the frozen static `ell=2`
master definition and vacuum Einstein equations gives

```text
H0=H2=Psi'+3Psi/r,
K=N Psi'+3Psi/r.
```

Pure de Sitter is conformally flat, so the linearized Weyl tensor is gauge
invariant. In the background static orthonormal frame its radial electric
component is

```text
delta E_rr=delta C_(t r t r)=-6Psi(r)Y/r^3.
```

For the physically normalized collective source this becomes

```text
E_rr^phys=-(48piG e^6 f_pi^4/c_I^2)
           [psi0(x)/x^3] QJ_ab n_a n_b.
```

At exterior radii `x=(5,10,15)`, the completed numerical response divided by
the horizon-regular homogeneous solution has amplitude spread below
`8.7e-19`. The spin-2 cat therefore produces a nonzero physical tidal
quadrupole, while W3w's anticoherent branch remains zero at this order.

This is a local gauge-invariant exterior curvature amplitude. It does not
supply tensorial Israel matching, interval validation, a self-gravitating
background, finite-thickness wall control, or detector dynamics.

Artifacts: `docs/static_patch_l2_weyl_reconstruction.md`,
`qgtoy/static_patch_l2_weyl_reconstruction.py`, and
`experiments/static_patch_l2_weyl_reconstruction_certificate.json` (SHA256
`3025d65fe82585e584150e956de9481380ab3f4a72d26a7cacb744974838c070`).

### Research Theorem W3y: Equal-Leading-Energy Tidal Discriminator

In signature `(-+++)` with `E_ij=C_(i t j t)`, an infinitesimal radial Jacobi
separation obeys the source-dependent initial relation

```text
delta[ddot(xi)/xi]=-delta E_rr.
```

Consider the fixed-spin states

```text
|cat>=(|2,2>+|2,-2>)/sqrt(2),
|T>=(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2).
```

They have the same `j=2`, Casimir `C=6`, inertia, and leading rigid-rotor
energy `3/I`, but

```text
<QJ>_cat=diag(-1,-1,2),  <QJ>_T=0.
```

The semiclassical exterior field therefore gives a nonzero mean gradiometer
contrast for the cat and zero leading quadrupolar mean signal for `|T>`. At the
declared illustrative point `e=f_pi=1`, `G=1e-6`, `x=5`, and unit physical
Jacobi separation, the axial linearized relative-acceleration contrast is
`-1.3605783525460437e-10` in natural units; the transverse signal has the
opposite sign and half the magnitude.

This proves that equal-Casimir, equal-leading-rotor-energy reference states can
have distinct semiclassical tidal fields: gravity resolves `<QJ_ab>`, not
Casimir alone. It is not a universal lower bound or a single-shot quantum
metric prediction. Finite separation/time, `Omega^4` energy, fluctuations,
noise, interval validation, self-gravity, and Israel matching remain open.

Artifacts: `docs/skyrmion_tidal_reference_discriminator.md`,
`qgtoy/skyrmion_tidal_reference_discriminator.py`, and
`experiments/skyrmion_tidal_reference_discriminator_certificate.json` (SHA256
`a0614a2b883ba3604382265f704bad5fd0ff11ad76de895cb28b12765321794e`).

### Research Gate W3z: Symmetric Centrifugal Spectral Target

The coupled centrifugal Hessian is now assembled directly in weak form from
the exact local quadratic density in `(f,g,f',g')`. The piecewise-linear trial
space imposes the origin traces `f(0)=g(0)=0` and ideal-mirror trace `g(a)=0`.
The Robin-equivalent boundary coefficient is

```text
b_wall=-(P_ff beta+M_ff),
```

so its natural conormal condition reproduces the derived pure-tension Robin law
for `f(a)`. This is a consistency construction, not an independent membrane
second-variation derivation. No numerical derivatives of the coefficient
blocks enter this assembly. The default nested spaces give

```text
lambda_Ritz=(0.3536279015, 0.3535118860, 0.3534832456),
```

the stationarity work identity closes to floating precision, and the finest
weak-form solution agrees with the separately implemented strong-form solution to
`1.32e-4` in the declared scaled probe norm.

This is deliberately a gate, not a coercivity theorem. Floating profile
interpolation and Gauss quadrature mean the displayed values have no certified
one-sided relation to the continuum spectrum. Moreover, the trace space does
not explicitly enforce the smooth Frobenius condition `f+g=O(x^3)`. The
validation theorem must resolve that origin domain, use the authenticated
profile tube and interval coefficient boxes, and close a two-sided matrix
Green-parametrix/Neumann defect below one. It should then enclose the forced
solution and prove that the single factorized exterior master amplitude
excludes zero.

Artifacts: `docs/centrifugal_skyrmion_variational.md`,
`qgtoy/centrifugal_skyrmion_variational.py`, and
`experiments/centrifugal_skyrmion_variational_certificate.json` (SHA256
`2c8a2b3e4fd961ca87d2dd3cbc036a0ece4c31531c246b8d18d3b72b4b0d8454`).

### Research Theorem W3z.1: Exact Coupled-Origin Indicial Factorization

For `F=pi-bx+O(x^3)`, exact rational Laurent evaluation of the centrifugal
quadratic density gives

```text
C=C0+O(x^2),  M=xM0+O(x^3),  P=x^2P0+O(x^4).
```

The resulting matrix pencil

```text
K(p)=-p(p+1)P0-(p+1)M0^T+pM0+C0
```

satisfies, as a polynomial identity in the unspecified origin slope `b`,

```text
det K(p)=det(P0)(p-1)(p-3)(p+2)(p+4),
det(P0)=1/1350+(2/225)b^2+(16/675)b^4>0.
```

The regular exponents are therefore exactly `p=1,3`, their singular companions
are `p=-2,-4`, and the `p=1` kernel is exactly `(f,g)=(-1,1)x`. At the declared
rational reference slope, the exact cubic-mode ratio agrees with the former
small-radius floating probe. The authenticated AU.3b slope interval further
gives an exact leading Robin-matrix enclosure at `x=1/16`, with every entry
positive and maximum width below `0.01616`.

This theorem removes the probe-radius/SVD uncertainty but does not yet identify
the Friedrichs form domain. The full proof must show that

```text
g=xv(t),  f=-xv(t)+x^3u(t),  t=x^2,
```

regularizes the complete operator and must validate its two-parameter transfer
map to `x=1/16`.

Artifacts: `docs/centrifugal_skyrmion_origin.md`,
`qgtoy/centrifugal_skyrmion_origin.py`, and
`experiments/centrifugal_skyrmion_origin_certificate.json` (SHA256
`505437ad55113896aab97fd33307599ef014e0cf1e00d67611ab5634327fe9a9`).

### Research Theorem W3z.2: Exact Transformed-Origin Density Factorization

Set

```text
t=x^2,
F=pi-xw(t),
g=xv(t),
f=x[-v(t)+t u(t)].
```

Writing the profile through the entire kernels
`s(t)=sin(sqrt(t)w(t))/sqrt(t)` and `c(t)=cos(sqrt(t)w(t))`, direct
term-by-term substitution into the complete same-action `K=2` static Hessian
proves

```text
H_static(x)=x^2 H_hat(t;w,w_t,v,u,v_t,u_t),
```

with no negative powers of `t` in `H_hat`. Exact rational evaluation at the
center gives

```text
H_hat(0)=v(0)^2/6.
```

Three direct floating replays of the untransformed density agree with the
factorized expression to maximum relative discrepancy `2.61e-18`.

The leading rotational Euler source is exactly

```text
F_3=b(1-4b^2)(1,-3/2)/45.
```

Both rows of `K(3)` have the same `-3/2` ratio, so `F_3` lies in its range.
The zero-linear-amplitude forced particular branch therefore admits a log-free
cubic start with

```text
(10+56b^2)v_t(0)-(4+56b^2)u(0)=b(1-4b^2).
```

This is a local-density theorem, not yet the origin-transfer theorem. Since

```text
H_static dx=(sqrt(t)/2)H_hat(t)dt,
```

the transformed variational problem retains a regular-singular weight. A
Friedrichs trace-space equivalence, finite-cutoff Frobenius remainder, and
validated two-parameter transfer to `t=1/256` remain required before this can
enter the continuum inverse.

Artifacts: `docs/centrifugal_skyrmion_transformed_origin.md`,
`qgtoy/centrifugal_skyrmion_transformed_origin.py`, and
`experiments/centrifugal_skyrmion_transformed_origin_certificate.json`
(SHA256
`e4ae895c9aa120da3d87f8a9cbd774a11bd44d056fba1e6b5cae235870dd6568`).

### Research Theorem W3z.3: Exact First Post-Indicial Recurrence

For the default profile parameters, exact rational-function algebra in the
origin slope `b` carries the two regular homogeneous columns and the forced
particular column through physical power `x^5`. The first nonsingular
recurrence matrix is

```text
M5=(1/45)[[28+308b^2,-70-392b^2],
           [-22-200b^2,28+176b^2]],
```

with

```text
det M5=-(28/75)(32b^4+12b^2+1)<0.
```

Every leading and `p=5` recurrence residual vanishes as an exact
rational-function identity. The full leading equation also shows that the
normalized linear column has a generally nonzero `v_t(0)`; retaining only its
indicial vector would give the wrong finite-cutoff column.

At the declared reference slope, the `(v1,u1,v2)` triples are

```text
linear:  (0.3279577054,-0.1494623983, 0.04710453574)
cubic:   (3.195336901, -1.251770645, -0.6521074264)
forced: (-0.09477191097,0.1353338744, 0.08724110619).
```

These are exact formal germs, not a finite-cutoff enclosure. A correlated
Taylor remainder over the authenticated slope box and `0<=t<=1/256` remains
required before exporting the affine regular boundary subspace to the global
interval inverse.

Artifacts: `docs/centrifugal_skyrmion_frobenius.md`,
`qgtoy/centrifugal_skyrmion_frobenius.py`, and
`experiments/centrifugal_skyrmion_frobenius_certificate.json` (SHA256
`09ac1a8c29675e4dcc4d92f32ddaf6b75d9111563b5e404020db5e01e29551d4`).

### Research Theorem W3z.4: Uniform Post-Germ Indicial Inverse Majorant

For every slope in the authenticated AU.3b origin box and every remaining odd
Frobenius power, exact rational interval arithmetic proves

```text
sup_{odd p>=7} ||K_b(p)^-1||_infinity
  < 0.078324234 < 79/1000.
```

The `p=7` and `p=9` matrices are enclosed directly. For `p>=11`, the proof
combines

```text
(p-1)(p-3)(p+2)(p+4)>=(80/121)p^4
```

with a quadratic adjugate row-sum majorant. The resulting tail bound is below
`0.04638`; hence `p=7` supplies the uniform maximum.

This is the Green constant for a post-germ Taylor-majorant argument. It does
not bound the nonleading variable coefficients or source and therefore is not
yet a Taylor remainder or finite-cell transfer theorem.

Artifacts: `docs/centrifugal_skyrmion_indicial_majorant.md`,
`qgtoy/centrifugal_skyrmion_indicial_majorant.py`, and
`experiments/centrifugal_skyrmion_indicial_majorant_certificate.json` (SHA256
`55841a2fec100e627f8852c2f5c729e6fc8bd6e49457cff27173c2e120fc03b2`).

### Research Theorem W3z.5: Uniform Quintic Origin-Profile Family

Across the complete authenticated AU.3b shooting interval, a partition into
16 exact rational slope cells validates the regular profile family in the
form

```text
p(t)=b-3c(b)t-5d(b)t^2+t^3 r_p(t),   |r_p|<=13/10,
u(t)=b-c(b)t-d(b)t^2+t^3 r_u(t),     |r_u|<=13/70,
F(x)=pi-xu(x^2),                     F'(x)=-p(x^2).
```

On `0<=x<=1/16`, exact rational degree-two Taylor models give a maximum
contraction below `0.584076`, maximum radii left side below `0.894730` against
radius `1.3`, and Volterra denominator above `20.7559`. The cells cover the
slope interval without gaps, and the complete cutoff family satisfies

```text
3.0425506 < F(1/16) < 3.0432169,
-1.583443 < F'(1/16) < -1.572800.
```

This supplies the correlated profile input needed to bound the conormal field
system through physical power `x^5`. It is not itself a centrifugal transfer,
Friedrichs-domain, continuum-inverse, or nonzero-response theorem.

Artifacts: `docs/validated_skyrmion_quintic_family.md`,
`qgtoy/validated_skyrmion_quintic_family.py`, and
`experiments/validated_skyrmion_quintic_family_certificate.json` (SHA256
`125232b3856d2cf4d17647b90983a4f0a6865ead8149ad07401cbabf5fbb9294`).

### Research Theorem W3z.6: Exact Conormal Origin-Transfer Scaffold

For weak-form blocks `C,M,P` and source coefficients `s0,s1`, the exact
variables

```text
a=y/x,  p=P y'+M^T y-s1,  z=p/x^2,  X=(a,z),  t=x^2
```

convert the centrifugal Euler equation into

```text
2tX_t=A(t)X+q(t),
A11=-Pbar^-1(Pbar+Mbar^T),  A12=Pbar^-1,
A21=Cbar-Mbar Pbar^-1 Mbar^T,
A22=Mbar Pbar^-1-2I,
q1=Pbar^-1 shat1,
q2=Mbar Pbar^-1 shat1-shat0.
```

At the origin, exact rational-function algebra gives
`spec A(0)={0,2,-3,-5}`. Exact Lagrange projectors and a 128-cell rational
enclosure of the authenticated slope interval prove, in the explicit weighted
infinity norm with weights `(36/25,73/50,13/20,73/100)`,

```text
||G||_w < 0.449492 < 9/20.
```

The two homogeneous field germs and one forced germ through `x^5` are exported
as an affine endpoint map without a Robin inversion. This scaffold alone did
not claim conormal `t^3` residual divisibility; W3z.7 now proves that formal
input. Quantitative bounds on `A(t)-A(0)` and the scaled residual remain the
finite-cell transfer gate.

Artifacts: `docs/validated_centrifugal_origin_transfer.md`,
`qgtoy/validated_centrifugal_origin_transfer.py`, and
`experiments/validated_centrifugal_origin_transfer_certificate.json` (SHA256
`c10651881cd99ca85c4c1f282092668e6d92597f7f2a785156fdcee1401da7b3`).

### Research Theorem W3z.7: Regular Conormal Blocks And Residual Divisibility

With `a=y/x`, `d=y'`, and `t=x^2`, exact cancellation of the physical
quadrupole density gives

```text
H_static/t=a^T Cbar(t)a+2a^T Mbar(t)d+d^T Pbar(t)d,
C=Cbar,  M=xMbar,  P=tPbar.
```

The rotational source factors as `s0=x^3 r0(t)` and `s1=x^4 r1(t)`, hence the
conormal source obeys `q(t)=O(t)`. The exact origin blocks reproduce the
previously certified indicial Hessian, while positive-radius probes reproduce
the independently implemented physical Hessian and source covector to
floating roundoff.

Regular kernel algebra gives `A(t)-A(0)=O(t)`. For all three exact field germs,
the Euler recurrence through `x^5` leaves an `O(x^7)` residual. Since

```text
lower conormal residual = - Euler residual / x,
```

the conormal residual is `O(x^6)=O(t^3)` for the linear homogeneous, cubic
homogeneous, and forced particular columns. This proves the formal
divisibility required by `X=X_c+t^3R`.

Artifacts: `docs/centrifugal_skyrmion_conormal_blocks.md`,
`qgtoy/centrifugal_skyrmion_conormal_blocks.py`, and
`experiments/centrifugal_skyrmion_conormal_blocks_certificate.json` (SHA256
`f87766d639f721b6227cab436d394e09f4059741fdbc5a057eba4e379d67f984`).

Claim boundary: exact block/source regularity and formal residual order, not
interval bounds on `A-A0` or the scaled residual, a closed finite-cell radii
inequality, a continuum inverse, or a validated response.

### Research Theorem W3z.8: Validated Finite-Cell Conormal Transfer

Two exact rational slope cells cover the authenticated AU.3b shooting
interval. Degree-two family Taylor models propagate the validated quintic
profile remainders through the regular coefficient/source blocks without
differentiating those remainders. Exact pointwise cancellation removes the
constant coefficient of `A-A0` and the first three residual coefficients.

In the declared weighted state norm, the source-hashed audit proves

```text
gamma=||G||_w                  < 0.500310,
delta=sup||A-A0||_w            < 0.145445,
gamma delta                    < 0.072576.
```

For the linear homogeneous, cubic homogeneous, and forced particular columns,
the cellwise choices `R_j=2 gamma epsilon_j/(1-gamma delta)` satisfy

```text
gamma epsilon_j+gamma delta R_j<=R_j.
```

The global remainder radii are below `(887.903,327.961,25.328)`. Because they
multiply `t^3`, the largest component error in the conormal state at
`t=1/256` is below `7.73e-5`. Hence every authenticated slope has a unique
regular continuation for each affine column through the finite origin cell.

Artifacts: `docs/validated_centrifugal_conormal_remainder.md`,
`qgtoy/validated_centrifugal_conormal_remainder.py`, and
`experiments/validated_centrifugal_conormal_remainder_certificate.json`
(SHA256
`7b8be07c712f142f95219057a2348d11e80fbf73fd428d527f96a43257adb5c0`).

Claim boundary: a validated affine conormal-state boundary tube, not yet a
direct interval tube for `(f,g,f',g')`, Friedrichs-domain equivalence, the
global continuum inverse, or a validated nonzero response.

### Research Theorem W3z.9: Validated Physical Origin Transfer

On each authenticated slope cell and for each of the two homogeneous and one
forced columns, the exact endpoint identities

```text
y=xa,
y'=Pbar^-1(z-Mbar^T a+sigma shat1)
```

convert the W3z.8 conormal tube into direct interval enclosures for
`(f,g,f',g')` at `x=1/16`. The same profile/coefficient Taylor models are used
in both steps. The formal `x^5` endpoint centers are contained, and the audit
proves

```text
maximum field interval width      < 0.051139 < 3/50,
maximum derivative interval width < 1.394047 < 3/2.
```

The tubes are columnwise. General affine combinations scale each column error
by the absolute value of its amplitude before summing.

Artifacts: `docs/validated_centrifugal_physical_origin_transfer.md`,
`qgtoy/validated_centrifugal_physical_origin_transfer.py`, and
`experiments/validated_centrifugal_physical_origin_transfer_certificate.json`
(SHA256
`e07d692092df48646f802bb4be4628f81038da641a4c046c1cb446e50cb24399`).

Claim boundary: a validated physical finite-origin boundary tube, not yet a
Friedrichs trace-space equivalence, global continuum inverse, or validated
nonzero exterior response.

### Research Theorem W3z.10: Local Finite-Energy Solution-Germ Trace

For a solution branch `y=x^p(v+O(x^2))`, the regular block scaling gives

```text
H[y]=Q_p(b)x^(2p)+O(x^(2p+2)).
```

Exact nullvectors of the indicial pencil show that each `Q_p(b)` is a strictly
positive even polynomial for `p in {1,3,-2,-4}`. Therefore local quadratic-form
energy is finite exactly when `p>-1/2`, and

```text
finite-energy homogeneous powers: 1,3,
excluded singular powers:         -2,-4.
```

A nonzero `p=-4` coefficient has a positive leading `x^-8` square; after it
vanishes, a nonzero `p=-2` coefficient has a positive `x^-4` square. Cross
terms between distinct powers cannot cancel either first singular square.
Thus the finite-energy homogeneous solution-germ trace is two-dimensional,
and the forced `p=3` particular column is admissible. W3z.9 maps precisely
these three affine columns to the finite physical cutoff.

Artifacts: `docs/centrifugal_skyrmion_friedrichs_trace.md`,
`qgtoy/centrifugal_skyrmion_friedrichs_trace.py`, and
`experiments/centrifugal_skyrmion_friedrichs_trace_certificate.json` (SHA256
`49f08d3471e1402ec29577df77e3caaff25511461950e73daedecce6338b6d87`).

Claim boundary: local solution germs of the symmetric weak-form equation, not
a classification of the entire form domain, global semiboundedness, a global
Friedrichs realization, or a validated response.

### Research Theorem W3z.11: Exact Liouville Coercivity Reduction

For the global weak density

```text
q[y]=y'^T P y'+2y^T M y'+y^T C y
```

and any symmetric multiplier `K`, exact completion gives

```text
q[y]-alpha|y|^2
 =(y'+P^-1(M^T-K)y)^T P(y'+P^-1(M^T-K)y)
  +(y^T K y)'+y^T R_alpha y,

R_alpha=C-alpha I-(M-K)P^-1(M^T-K)-K'.
```

The explicit witness `K=sym(M)-P/(2x)` has a nonsingular conormal potential

```text
W_K=C-sym(Mbar)+Pbar/4-2t sym(Mbar)_t+t Pbar_t
    +Abar Pbar^-1 Abar,
Abar=(Mbar-Mbar^T)/2.
```

Both identities are verified with exact rational matrix arithmetic. A trusted
interval kernel now evaluates the two Sylvester minors of
`W_K-(1/20)I` on supplied authenticated profile jets, and an exact interval
wall audit proves a positive allowed trace remainder over a conservative wall
slope box. The floating global profile gives a stable minimum eigenvalue
`0.07863...` near `x=1.9821`, leaving a `0.0286...` target buffer; a separate
Riccati witness leaves a nearly `0.1` sampled buffer.

Artifacts: `docs/centrifugal_skyrmion_riccati_coercivity.md`,
`qgtoy/centrifugal_skyrmion_riccati_coercivity.py`,
`qgtoy/validated_centrifugal_global_form.py`, and
`experiments/centrifugal_skyrmion_riccati_coercivity_certificate.json` (SHA256
`11c7897eae4f08193e133620b56bdd1fbd5ba71258ab2cbbc9f83d75932377fe`).

Claim boundary: an exact coercivity reduction, exact coefficient/wall checker,
and high-margin floating witness, not yet a whole-profile interval proof.
Independent jet boxes lose the determinant margin under wrapping; the closing
certificate must range the assembled conormal determinant with a correlated
Taylor model on the authenticated AU.1 Newton tube. No continuum inverse or
validated forced response is claimed yet.

### Research Theorem W3z.12: Exact-Spline Liouville Minor Certificate

For `Pbar=diag(p,r)` and antisymmetric conormal entry `alpha`, the two
Sylvester conditions for `W_K-(1/20)I` admit the division-free form

```text
d1 = r U-alpha^2,
d2 = p V-alpha^2,
D  = d1*d2-p*r*z^2.
```

Because `p,r>0`, `d1>0` and `D>0` imply the desired strict matrix inequality.
A centered exact-rational Taylor model now ranges these assembled expressions
on the 43-cell archived AU.1 approximate profile. Forty-two cells close
without refinement; the cell `[1/2,11/16]` closes after one bisection. The
44-cell validation has exact positive lower bounds, numerically

```text
min p  = 0.0213331584854351,
min r  = 0.0319999988139318,
min d1 = 0.0011452285672344,
min d2 = 0.0094737729781766,
min D  = 0.0000118689614877.
```

Artifacts: `docs/validated_centrifugal_liouville_spline.md`,
`qgtoy/validated_centrifugal_liouville_taylor.py`, and
`experiments/centrifugal_skyrmion_liouville_spline_certificate.json` (SHA256
`581db1b6a078b5e43a09de17fe450f261d04931f94e52c5a039ea27b468752f3`).

Claim boundary: a continuum interval result for the exact supplied
piecewise-polynomial approximate profile on `[1/16,4]`, not yet for the
nonlinear solution tube or origin interval. The next proof must propagate the
endpoint-corrected AU.1 `C2` tube through `d1,D`, join the origin certificate,
and establish the closed Friedrichs form before claiming a global inverse.

### Research Theorem W3z.13: Outer Newton-Tube Liouville Certificate

The exact-spline constant `1/20` is not stable under the authenticated AU.1
`C2` tube at its worst cell. With the honest reduced target `1/100`, adaptive
centered Taylor models prove

```text
W_K >= (1/100) I,  3/16 <= x <= 4,
```

uniformly over the nonlinear Newton tube and full endpoint-correction family.
The 31 source cells close as 45 validation cells at maximum depth two. Exact
positive lower bounds have numerical values

```text
min d1 = 0.0015796571176299,
min d2 = 0.0092018466096716,
min D  = 0.0000005629318349.
```

Separately, the regular nonlinear Volterra family extends over the full
shooting-slope interval from the origin to `x=3/16`, with outward-rounded
contraction upper bound `0.916612582057544892`.

Artifacts: `docs/validated_centrifugal_liouville_outer_tube.md`,
`qgtoy/validated_centrifugal_liouville_tube.py`, and
`experiments/centrifugal_skyrmion_liouville_outer_tube_certificate.json`
(SHA256
`c8744dd4136b607595a42de1ada271644c8408b0fff6b4a2629bf749ea136b91`).

Claim boundary: completed-potential coercivity on the authenticated outer
tube plus existence of the inner nonlinear family, not yet the inner
Liouville inequality, joined closed form, global Friedrichs inverse, or
validated forced response.

### Research Theorem W3z.14: Regular-Origin Liouville Certificate

For `t=x^2`, `F=pi-xu`, and `p=-F'`, the authenticated origin family has

```text
p=b-3 gamma(b)t+t^2 r_p, |r_p|<=8,
u=b-  gamma(b)t+t^2 r_u, |r_u|<=8/5.
```

The regular entire kernels in `z=t u^2` and the nonlinear profile equation
determine `u_t,s_t,c_t,p_t` without differentiating the bounded remainders.
A four-variable interval mean-value form preserves the shared dependence of
the assembled division-free minors. On a `16 by 4` time/slope partition it
proves

```text
W_K >= (1/100) I,  0 <= x <= 3/16,
```

with minimum scaled first minor `0.658684620946269` and determinant
`0.0670614628308156`. The same origin family has contraction upper bound
`0.900653766297957784`.

Artifacts: `docs/validated_centrifugal_liouville_origin.md`,
`qgtoy/validated_centrifugal_origin_liouville.py`, and
`experiments/centrifugal_skyrmion_liouville_origin_certificate.json` (SHA256
`daa220e68ceef034a1b23ea955033dc08c0e776ee49628eb07acb0834b57c065`).

Together with W3z.13 and the exact positive wall trace, this covers the
coefficient inequalities in the global square completion from origin to wall.

Claim boundary: a full coefficient-level certificate, not yet the common
closed weighted form, Friedrichs operator, two-sided inverse, or nonzero
forced response.

### Research Theorem W3z.15: Global Centrifugal Friedrichs Inverse

Let `H=L2((0,4);R^2)` and

```text
V={y in H: y is AC_loc on (0,4], x y' in H, and g(4)=0}.
```

For the declared fixed-background matter-plus-moving-membrane weak form, the
smooth wall-constrained core is dense in `V`. The origin completion trace
vanishes because `K=x Kbar`, and the artificial certificate split at `3/16`
introduces no trace defect. W3z.13, W3z.14, uniform principal positivity, and
the positive allowed wall trace imply

```text
q[y] >= (1/100)||y||_H^2.
```

The completed-square norm is equivalent to
`||y||_H^2+||x y'||_H^2`; hence the form is closed. Its representation
operator `A` is positive self-adjoint, zero lies in its resolvent, and

```text
||A^-1||_(H -> H) <= 100.
```

Artifacts: `docs/centrifugal_skyrmion_friedrichs_form.md`,
`qgtoy/centrifugal_skyrmion_friedrichs_form.py`, and
`experiments/centrifugal_skyrmion_friedrichs_form_certificate.json` (SHA256
`4a4e3ecd48a205860de3aa045c94d2b825c0afce1c0f12f4b96254db355b85bb`).

Claim boundary: the closed operator and its two-sided `L2` inverse for the
declared fixed-background action, not compact resolvent, a kinetic mode gap,
a validated `V*` forced response, tensorial Israel matching, or a backreacted
Einstein-matter solution.

### Research Theorem W3z.16: Nonzero Centrifugal Weak Response

For authenticated origin slope `b=-F'(0)`, the exact regular source kernels
give

```text
s_g(x)=c(b)x^3+O(x^5),  c(b)=b(4b^2-1)/30.
```

The full slope interval lies above `1/2`, and exact rational arithmetic proves
`c(b)>0.4680670530`. The derivative-load coefficient vanishes at both
endpoints, so integration by parts gives a nonzero `L2` source and no boundary
load. Applying the W3z.15 inverse gives a unique weak deformation `y`, and

```text
y != 0,  chi_rot=ell(y)=q[y]>0.
```

Artifacts: `docs/centrifugal_skyrmion_forced_response.md`,
`qgtoy/centrifugal_skyrmion_forced_response.py`, and
`experiments/centrifugal_skyrmion_forced_response_certificate.json` (SHA256
`9edc2bc479534fab3f527ce535a373da1373b45085c6fbf4602f4ee9cdd32db7`).

Claim boundary: a unique nonzero fixed-background weak matter deformation and
strictly positive source-conjugate susceptibility, not a quantitative field
norm or a certified nonzero Zerilli/electric-Weyl response.

### Research Proposition W3z.17: Dual-Weighted Exterior Response Enclosure

Outside the compact source, the static `l=2` Green kernel factorizes, so all
master and electric-Weyl samples depend on one scalar amplitude

```text
A_ext=J_rigid+B(y).
```

Let `q(y,v)=ell(v)` and `q(v,z)=B(v)`. For any conforming primal and adjoint
trials `y_h,z_h`, put

```text
J_hat=J_rigid+B(y_h)+R_y(z_h).
```

Symmetry of the closed form gives

```text
|A_ext-J_hat| <= ||R_y||_(q*) ||R_z||_(q*).
```

The exact-rational enclosure logic is implemented in
`qgtoy/dual_weighted_response_enclosure.py`. A source-hashed nested-Galerkin
primal-adjoint audit gives corrected amplitude `-0.002818947812` and residual
product `0.0000450997164`, only `1.60` percent of its magnitude.

Artifacts: `docs/centrifugal_skyrmion_master_adjoint_enclosure.md`,
`docs/centrifugal_skyrmion_master_adjoint_feasibility.md`, and
`experiments/centrifugal_skyrmion_master_adjoint_feasibility.json` (SHA256
`584a22ea3ae9807dcc9da8cd6cc20274c943c52bb23c38923cbe8e6dcf986bf7`).

Claim boundary: an exact certification theorem and favorable floating target,
not yet interval-certified physical residuals or a nonzero gravitational
observable.

### Research Theorem W3z.18: Tensorial Israel Promotion Gate

For a static spherical shell in

```text
ds^2=-A(r)dt^2+dr^2/B(r)+r^2dOmega^2,
```

the two principal mixed extrinsic curvatures are

```text
K_t^t=sqrt(B)A'/(2A),    K_theta^theta=sqrt(B)/a.
```

With one normal directed from the inner to the outer region and
`[K_i^j]-delta_i^j[K]=-kappa S_i^j`, a constant positive-tension shell has
`S_i^j=-sigma delta_i^j` and therefore requires

```text
[K_t^t]=[K_theta^theta]=-kappa sigma/2.
```

Identical de Sitter geometry on both sides has zero jump and is consequently
incompatible with every `sigma>0`. This exact no-go concerns the uncorrected
background, not a first-order sourced calculation whose `O(kappa sigma)`
metric perturbation can supply the jump.

The gate is tested against an exact nontrivial family: regular de Sitter
inside and same-cosmological-radius Kottler outside. For `u=a^2/R^2` in
`(1/3,2/3)`, both Israel equations close with

```text
(kappa sigma/2)a=2(2-3u)/(3sqrt(1-u)),
GM/a=2(2-3u)/(9(1-u)).
```

After spherical matching, constant tension has `delta S_i^j=0` in mixed
components. Tensorial `ell>=2` matching therefore requires continuity of the
physical-shell first form and all temporal-scalar, angular-trace, and
angular-tracefree mixed-extrinsic-curvature amplitudes. A scalar master
field/flux jump audit does not imply these six conditions.

Artifacts: `docs/israel_junction_gate.md`,
`qgtoy/israel_junction_gate.py`, and
`experiments/israel_junction_gate_certificate.json` (SHA256
`d2c7f542490966c51d37b2d10db45efb4f4c746ac696d5996df1a9b16c29a950`).

Claim boundary: an exact background no-go, a self-consistent vacuum-shell
benchmark, and the full tensorial acceptance gate. The Skyrmion master field
has not yet been reconstructed into the six displaced-shell amplitudes, so
its Israel junction remains open.

### Research Proposition W3z.19: Affine And Origin-Regular Master Kernels

The same-action completed quadrupole stress is an exact pointwise affine map

```text
T=T_rigid+L0(f,g)+L1(f',g').
```

Propagating a first radial jet through its energy density gives the smooth
bulk master source without sampled differentiation,

```text
F=F_rigid+b_f f+b_fp f'+b_fpp f''+b_g g+b_gp g'.
```

The formulas use only generic scalar arithmetic and caller-supplied
trigonometric enclosures. Exact rational basis tests, an independent centered
derivative of the legacy stress implementation, interval arithmetic, and
centered Taylor-model arithmetic all agree.

At the regular origin, set

```text
t=x^2, F=pi-xw(t), g=xv(t), f=x[-v(t)+t u(t)].
```

After canceling every `sin(F)/x`, `f/x`, and `g/x` algebraically, the master
source factorizes as

```text
F_master(x)=x F_hat(t),
```

where `F_hat` is regular at `t=0` and affine in
`(u,u_t,u_tt,v,v_t,v_tt)`. It can be ranged on a center-containing interval
without reciprocal-zero failure. For the exact center relations
`sin(xw)/x=w` and `cos(xw)=1`, every displayed affine coefficient of
`F_hat(0)` vanishes, exposing the stronger physical cancellation that a
correlated Taylor model can retain.

The moving-wall/contact-free map is generic-scalar as well. It keeps the
kinematic displacement coefficient `-1/F'(a)` distinct from the effective
response trace `gamma_B`, and forms the bulk-endpoint cancellation before
interval ranging. Consequently the effective `f'`, `g`, and `g'` wall
coefficients vanish as exact algebraic identities; only `gamma_B f(a)`
survives.

Artifacts: `docs/centrifugal_affine_master_kernel.md`,
`docs/centrifugal_origin_master_kernel.md`, and
`experiments/centrifugal_affine_master_kernel_certificate.json` (SHA256
`75e2cb77b675d6a6f69b2b9dfe26c527eda5bb475712e03ba5d1170353d08b70`).

Claim boundary: exact local affine bulk, origin, and moving-wall observable
algebra, not authenticated primal/adjoint field enclosures, continuum
integration, residual norms, or a nonzero exterior-amplitude interval.

### Research Theorem W3z.20: Finite-Time Tidal Detector Transfer

Under constant-rate isotropic `SO(3)` heat flow, the orientation score is a
rank-one moment while the tidal quadrupole is rank two. Their multipliers obey

```text
m_1(t)=exp(-2 gamma t),
m_2(t)=exp(-6 gamma t)=m_1(t)^3.
```

For two hypotheses with common initial proof-mass position and velocity, let
`Delta a_frac(0)` be their initial fractional Jacobi acceleration contrast.
In the quasi-static Jacobi/Born model the exact mean displacement contrast is

```text
Delta xi(T)=Delta a_frac(0) xi_0 K_2(T,gamma),
K_2=T/(6gamma)-(1-exp(-6gamma T))/(36gamma^2),
```

with continuous zero-rate limit `K_2=T^2/2` and

```text
exp(-6gamma T) T^2/2 <= K_2 <= T^2/2.
```

For additive equal-variance Gaussian displacement noise `sigma_x`, the
single-readout equal-prior error is

```text
P_error=(1/2)erfc(|Delta xi|/(2sqrt(2)sigma_x)).
```

Artifacts: `docs/finite_time_tidal_detector.md`,
`qgtoy/finite_time_tidal_detector.py`, and
`experiments/finite_time_tidal_detector_certificate.json` (SHA256
`9c72f7cd75f4d1d542fb9bfd08a907f2b31e42a1e55e07f6eecb557c9571e7be`).

Claim boundary: an exact finite-time/noisy composition inside the declared
heat/Jacobi/Gaussian model. The Weyl interval, `gamma`, readout noise, finite-
separation remainder, and detector backreaction are not yet derived from one
Skyrmion-detector action.

### Research Proposition W3z.21: Validated Positive-Radius Response Residual

On an authenticated positive-radius profile cell, exact interval radial jets
now produce enclosures of the physical conormal blocks

```text
C, M, P, M', P'
```

and of the strong rotational load `s0-s1'`, without sampled differentiation.
For exact rational piecewise-polynomial trials, the validator checks radial
contiguity, exact `C1` joins, and the essential `g(a)=0` trace. It then ranges

```text
r=load-[C-(M')^T]y-[M-M^T-P']y'+P y''
```

cell by cell and certifies

```text
integral_I |r|^2 <= |I| sum_i sup_I |r_i|^2.
```

The free radial conormal mismatch `eta` is kept out of the bulk `L2` residual.
If `A>=c I` and the completed wall margin is `m_w>0`, then

```text
||R||_(V*) <= ||r||_2/sqrt(c)+|eta|/sqrt(m_w).
```

The API requires explicit full coverage of the declared residual domain and
an explicit proof flag excluding internal interface distributions before
returning this bound.

Artifacts: `docs/validated_centrifugal_response_residual.md`,
`qgtoy/validated_centrifugal_response_residual.py`, and
`experiments/validated_centrifugal_response_residual_certificate.json`
(SHA256
`a799baab37215f5095d073880b95ed2025fd55f1fa89f5f0c47174d256998155`).

Claim boundary: a reusable exact residual theorem on supplied positive-radius
cells. Tight centered outer coefficient enclosures and the adjoint bulk
wall master load are still required before W3z.17 yields a nonzero continuum
response interval.

### Research Proposition W3z.22: Cancellation-Safe Origin Response Residual

In the regular variables

```text
t=x^2,  g=xv(t),  f=x[-v(t)+t u(t)],
```

write the weak-form blocks and load as

```text
C=Cbar, M=x Mbar, P=t Pbar, s0=x shat0, s1=t shat1.
```

For `a=(-v+tu,v)`, `d=y'`, and
`Z=Pbar d+Mbar^T a-shat1`, the physical conormal variable is `z=tZ` and the
strong residual has the exact cancellation

```text
r(x)=x Rhat(t),
Rhat=shat0-Cbar a-Mbar d+2[Z+t Z_t].
```

Thus exact rational `u,v` trials and interval `t` jets can be ranged without
dividing by an interval containing zero, and

```text
integral_0^x0 |r|^2 dx
 <= x0^3/3 sum_i sup_[0,x0^2] |Rhat_i|^2.
```

The implementation joins this origin contribution to contiguous positive-
radius cells before applying the global coercivity and wall-trace lift. It
requires the caller to assert separately that the physical field and conormal
data produce no interface distribution at the join.

Artifacts: `docs/validated_centrifugal_origin_response_residual.md`,
`qgtoy/validated_centrifugal_origin_response_residual.py`, and
`experiments/validated_centrifugal_origin_response_residual_certificate.json`
(SHA256
`e48c93dd6e5057629632cae8d8463ad496f17ebc758068cee87e1b837c4e96fa`).

Claim boundary: an exact origin residual and composition theorem for supplied
regular coefficient boxes and trials. Authenticated physical origin profile
jets and the resulting nonzero response interval remain open.

### Research Proposition W3z.23: Exact Rational Primal-Adjoint Trial Archive

The floating `81`-node primal and master-adjoint Galerkin systems have been
converted reproducibly into exact rational cubic-Hermite trials on all `43`
authenticated positive-radius profile cells. Shared endpoint values and
physical derivatives are rounded once to denominator `10^12`, so both trials
have exact `C1` joins and the essential trace `g(4)=0` holds algebraically.

At `x=1/16`, each endpoint jet is converted exactly to linear regular-origin
polynomials `u(t),v(t)` with

```text
t=x^2,  g=xv(t),  f=x[-v(t)+t u(t)].
```

The origin and outer field values and physical derivatives match exactly. The
archive round-trips without loss and is bound to both authenticated profile
inputs and its generating sources by SHA256.

A certified compact-angle reduction, `10^-18` outward coefficient rounding,
and exact restriction to eight subcells per authenticated cell give the
positive-radius primal diagnostic

```text
integral_[1/16,4] |r_y|^2 <= 3.3197692493413107,
max_i,x |r_y,i(x)| <= 1.8591081655835504.
```

This proves that the archived cells can be consumed by W3z.21 and improves the
former whole-cell square bound by more than four orders of magnitude. The
sequence at one, two, four, and eight subdivisions is approximately `328.14`,
`59.10`, `13.41`, and `3.32`. W3z.28 supplies the centered model and reduces
the one-subdivision square bound to `0.01003`; tighter Newton-remainder
correlation is still required for zero exclusion.

Artifacts: `docs/centrifugal_skyrmion_rational_response_trials.md`,
`qgtoy/centrifugal_skyrmion_rational_response_trials.py`, and
`experiments/centrifugal_skyrmion_rational_response_trials.json` (SHA256
`9dd83028d00b55c85d280087a696884338941b6602e3f9148a41d524f5ace921`).

The same artifact constructs the physical endpoint blocks from the
authenticated wall-slope interval and pure-tension Robin law. The primal wall
conormal mismatch is enclosed in

```text
[-0.001101145, 0.001420521],
```

while the completed wall trace margin exceeds `0.2018`.

Claim boundary: exact conforming primal-adjoint trial data and a coarse
positive-radius primal enclosure plus a certified primal wall mismatch. The
adjoint master load, tight full-domain dual norms, and nonzero exterior
response interval remain open.

### Research Proposition W3z.24: Authenticated Origin Profile Jets And Residual

The authenticated quintic origin family supplies interval forms for
`rho=-F'` and `u=(pi-F)/x` through `t=x^2`. Their `L-infinity` remainders cannot
be differentiated. Instead, the exact identity

```text
rho=u+2t u_t
```

gives `u_t`, while the Volterra profile equation gives `rho_t` after its
apparent division by `t` is factored through the entire centered quotients

```text
[sinc(sqrt(w))-1]/w,  [sinc(2sqrt(w))-1]/w,  w=t u^2.
```

Two rational slope cells cover the complete authenticated AU.3b family and
enclose the regular `t` jets of `N`, `rho`, `sin(F)/x`, and `cos(pi-F)`,
including their exact removable-center limits. Propagating these boxes through
W3z.22 and the archived trials gives

```text
||r_primal||^2_L2(0,1/16) <= 0.000021330073298636,
||A z_trial||^2_L2(0,1/16) <= 0.000000002466925854.
```

The second value uses zero load and is only the homogeneous adjoint-shaped
operator action, not an adjoint residual.

Artifacts: `docs/validated_centrifugal_origin_profile_jets.md`,
`qgtoy/validated_centrifugal_origin_profile_jets.py`, and
`experiments/validated_centrifugal_origin_profile_jets.json` (SHA256
`7924fb7da3bb96e92fb43f68cf9311b9ac9a6077292e69474fccf5579abab504`).

Claim boundary: authenticated origin kernels and primal origin residual. The
adjoint load, tight outer residuals, and nonzero exterior response remain open.

### Research Proposition W3z.25: Exact Conormal Interface Cancellation

For the centrifugal weak form the physical conormal is

```text
p=M(x,F,F')^T y+P(x,F,F')y'.
```

The authenticated sharp tube consists of restrictions of one global `C1`
Skyrmion solution. The exact rational primal and adjoint trials are also
global `C1` fields, including their regular-origin joins. Consequently every
entry in `(x,F,F',y,y')` has identical one-sided values at each internal
interface, so every conormal jump vanishes identically. No internal delta
distribution is missing from the cellwise strong residual.

The source-bound audit replays both trials on the `344`-cell eightfold
partition. Artifact:
`experiments/centrifugal_conormal_interface_certificate.json` (SHA256
`1ee677788edc45190c9b164c45bc4a76a1b9e395d172f12b5aa13241748200e2`).

Claim boundary: exact removal of internal interface distributions. It does
not improve the bulk interval widths or certify the loaded adjoint wall
equation.

### Research Proposition W3z.26: Validated Moving-Wall Master Load

At the physical wall ratio `a/R=1/5`, the exact closed forms for the
center-regular static `l=2` solution and its derivative are enclosed using a
positive rational series for `atanh(1/5)`. A centered Taylor model retains the
shared dependence of the wall stress and displacement on the authenticated
profile slope. The resulting exterior-master adjoint trace obeys

```text
0.002688103336731132 < gamma_B < 0.002834701713361219,
width(gamma_B)<1/5000.
```

Loading the free radial endpoint equation of the archived exact adjoint trial
then gives

```text
0.005743770662465949 < eta_z,wall
                     < 0.006339340647031048 < 1/150.
```

Artifact: `experiments/validated_centrifugal_wall_master_load.json` (SHA256
`ee73b3527750f91bcb2ed585df3d1d58376cbe0f4ff8db47919356872a86ed42`).

Claim boundary: the moving-wall part of the adjoint load and its endpoint
residual. The bulk master load and bulk adjoint residual remain open. Internal
interface cancellation is supplied independently by W3z.25.

### Research Proposition W3z.27: Validated Weak Adjoint Bulk Load

Integrating the master source's energy-density derivative by parts before
interval evaluation gives the exact positive-radius functional

```text
B_bulk(v)=integral (b0 dot v+b1 dot v') dx.
```

The affine coefficients require only `F,F'`, so no authenticated remainder is
differentiated. Positive rational series enclose the exterior Green weight and
its derivative on `x/R<=1/5`. Replaying all `344` eightfold-refined cells gives

```text
B_bulk(y_h) in [-0.002249596437198199, 0.001052714255862833],
B_bulk(z_h) in [ 0.000012035950858950, 0.000083040071016445].
```

For the archived adjoint trial, the weak residual has the rigorous form
`integral(r0 dot v+r1 dot v')`, with componentwise maxima

```text
|r0_i|<=0.012135653554083077,
|r1_i|<=0.009194661537655243.
```

The nonzero derivative-test coefficient must be lifted directly in `V*`; it
cannot be relabeled as an `L2` strong residual without differentiating the
load. Artifact: `experiments/validated_centrifugal_adjoint_bulk_load.json`
(SHA256
`3db6d390d521494d192c5df6b4bc5dfd1ee09f6d441f0bd69c3be2d18add44f5`).

Claim boundary: positive-radius weak load and coefficient residual only. The
regular-origin load and direct energy-dual/Riesz norm remain open.

### Research Proposition W3z.28: Centered Correlated Outer Primal Residual

One centered Taylor coordinate is propagated through the exact endpoint-
corrected profile spline, the exact rational primal trial, their derivatives,
the trigonometric kernels, and the complete strong conormal residual. The
authenticated Newton-tube errors remain interval remainders. On the same `43`
authenticated cells, without extra subdivision, this proves

```text
integral_[1/16,4] |r_y|^2 dx <= 0.010027698207072146,
max_i,x |r_y,i(x)| <= 0.0744234803973095.
```

The independent-box value on the same cells was about `328.1385`; preserving
the common radial coordinate improves the rigorous square bound by more than
`30000`. Artifact:
`experiments/validated_centrifugal_correlated_residual.json` (SHA256
`814da74d5c21cf96b45e9967dd5b8d297d90480a46c3f3ae7fd82ba3ffaad3e7`).

Claim boundary: positive-radius primal bulk residual. The conservative
coercivity lift is still too broad for zero exclusion; remaining sharpening
must preserve the Newton graph/slope correlations rather than merely bisecting
independent remainders.

### Research Proposition W3z.29: Direct Partial Adjoint Form-Dual Bound

For the weak adjoint residual
`R(v)=integral(r0 dot v+r1 dot v')+eta_wall f(a)`, the Liouville square
completion gives

```text
d=v'+P^-1(M^T-K)v,
R_bulk(v)=integral[(r1/x) dot (x d)
                  +(r0-T^T r1/x) dot v] dx,
T=I/2-Pbar^-1 Abar.
```

Using the certified bounds `Pbar>=I/100`, `V_completed>=I/100`, and the wall
trace margin yields, on `344` cells plus the loaded wall trace,

```text
delta_z,partial^2 <= 0.592007476516919181,
delta_z,partial   <= 0.769420221021594403.
```

The wall squared contribution is below `0.000175`; more than `99%` of the
bound comes from the adjusted bulk value coefficient, with dominant cell
`[1/2,67/128]`. Artifact:
`experiments/validated_centrifugal_adjoint_energy_dual.json` (SHA256
`500e56b5aa36c64846100dc59a7383b2051a12c6676fcf8e6d49574f61142d0e`).

Claim boundary: direct positive-radius-plus-wall `V*` bound. The regular-origin
master load is absent, so this is not a full `delta_z` and cannot be used for
zero exclusion. Its current magnitude is a representation diagnostic, not a
physical no-go.

### Research Corollary W4: Conditional Localized-Observer Elimination

Inside the declared marked-spherical-top branch, target chordal risk
`epsilon<1/8` requires

```text
Cbar >= (epsilon^-1-8)/16,

a >= [G^2(1+zeta)^2(epsilon^-1-8)
      /(8 kappa chi^2 zeta)]^(1/4).
```

For each hard-current optical design, the exact equal-shell static-slice
geometry supplies a proper ceiling `a_max^(design)(L)`. Reference-only heat
diffusion supplies the additional necessary condition

```text
gamma T<=1/2 log[(3/4-r_0)/(3/4-epsilon)],
```

where `r_0` is the strongest certified global risk floor at that radius
ceiling. A design is excluded if its proper-radius interval is empty or its
protocol time exceeds the coherence ceiling.

This is an exact conditional no-go/compatibility theorem for the composite
spherical-top, hard-current, and reference-heat branch. Passing is not an
existence theorem because the inputs have not yet been derived from one
microscopic matter/KMS action.

Artifacts: `docs/localized_so3_observer_tradeoff.md`,
`qgtoy/localized_so3_observer_tradeoff.py`, and
`tests/test_localized_so3_observer_tradeoff.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m unittest tests.test_localized_so3_observer_tradeoff
```

### Research Corollary W5: Spin-1 Measure-And-Correct Comparison

For the channel obtained by measuring the reference orientation and correcting
a spin-1 target, global chordal risk and normalized diamond error obey

```text
(8/9)R_ref<=epsilon_rec<=min{1,2sqrt(R_ref)}.
```

The lower bound is a maximally entangled Choi witness using
`Tr U_1=chi_1`; the upper bound follows from convexity and the operator-norm
distance of a spin-1 rotation from the identity. Consequently
`R_ref<=delta^2/4` is sufficient for constructed recovery error at most
`delta`.

This closes the estimation-to-recovery comparison only for the declared
measure-and-correct vector protocol. It does not cover arbitrary coherent
decoders or derive the measurement from a local matter interaction.

Artifacts: `docs/so3_measure_correct_recovery.md`,
`qgtoy/so3_measure_correct_recovery.py`, and
`tests/test_so3_measure_correct_recovery.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m unittest tests.test_so3_measure_correct_recovery
```

### Research Corollary W6: Skyrmion Matter-Derived Coherence Rate

For the leading rigid-Skyrmion current coupled through the declared local
pseudoscalar gyroscope action, the matter form factor fixes the optical
zero-frequency spectrum `j_Sky(0)`. At lapse `N`, the declared Davies
convention gives

```text
gamma_prop=g^2 N^-3 j_Sky(0).
```

Combining this coefficient with the odd-sector cutoff floor
`r_0=sin^2[pi/(2J+4)]` gives

```text
R_ref(T)>=3/4[1-e^(-2 gamma_prop T)]
          +r_0 e^(-2 gamma_prop T).
```

The executable evaluates the corresponding proper-time coherence ceiling and
loaded Markov diagnostic. This is an exact composition of the rate coefficient
and risk theorem under the declared model, not yet a certified reduced-dynamics
result: AU.3a supplies the stronger conservative spectral moments, while the
authenticated AU.3b baseline identifies a tail-dominated sharpening gap.
Finite-coupling dynamics, switching, collective-band, access, stress, and
lifetime errors remain open.

Artifacts: `docs/skyrmion_orientation_coherence.md`,
`qgtoy/skyrmion_orientation_coherence.py`, and
`tests/test_skyrmion_orientation_coherence.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_orientation_coherence
```

### Research Theorem X: Mean-Energy Finite-Observer Recovery Obstruction

Choose a phenomenological compact EFT ansatz for the orientation reference: a marked
spherical top of proper radius `a`, rest energy `m`, orientation
`Q in SO(3)`, and action

```text
S_obs=integral d tau[-m+I|Q^-1 D_tau Q|^2/2],
I=kappa m a^2,  0<kappa<=2/3.
```

Quantization gives `L^2(SO(3))` and `H_rot=C_left/(2I)`. The inertia law is a
stipulated spherical-top constitutive relation constrained by the support bound,
not derived from a matter stress tensor. For an arbitrary prepared rotor state
`eta`, let `Cbar=Tr(eta C_left)` and impose the declared mean-energy bounds

```text
E_rot/m<=zeta<=1,
2G(m+E_rot)/a<=chi<1.
```

Exact maximization of `Cbar=2 kappa m a^2 E_rot` gives

```text
Cbar
 <= kappa chi^2 zeta a^4/[2G^2(1+zeta)^2].
```

This is not a hard Hilbert-space cutoff. For every integer `J>=0`, projection to
spins `j<=J` has tail probability at most
`Cbar/[(J+1)(J+2)]`; the normalized projected state is within trace distance
the square root of that quantity. Combining contractivity with the exact
Peter-Weyl multiplicity obstruction gives, for `d=2L+1`,

```text
(1/2)||D N_eta-identity||_diamond
 >= max_(J>=0) max{0,
      1-(J+1)^2/d-sqrt[Cbar/((J+1)(J+2))]}.
```

This holds for every state on the full `L^2(SO(3))` satisfying the mean-Casimir
budget and every deterministic decoder after the fixed prepared-reference
append-and-twirl channel. Uniform optimization gives error
`1-O[1/d+(Cbar/d)^(1/3)]`. Hence the bound tends to one on the hard-energy horizon
sector `L=L_delta=Theta(sqrt(R/delta))` for every fixed finite observer. For a
collar-following apparatus `a_delta=alpha rho_delta`, the capacity itself falls
as `Cbar=O(R^2 delta^2/G^2)`.

For the repository's explicit Peter-Weyl measure-and-correct decoder, comparing
its sufficient cutoff with the stronger branchwise spectral condition
`J(J+1)<=kappa chi^2 zeta a^4/[2G^2(1+zeta)^2]` gives the leading protocol
feasibility scales

```text
delta_protocol=Theta(sqrt(G/epsilon)),
rho_protocol=Theta(sqrt(R sqrt(G)) epsilon^(-1/4)).
```

This latter scale is protocol specific; the any-decoder theorem instead uses
mean-Casimir truncation and covers high-spin tails. It excludes pre-correlated
encoders, postselection, and other reference hardware. The finite-time
collective-diffusion extension is Research Theorem Y below.
The compactness condition is a model hypothesis, not a general rotating-GR
collapse theorem. No local interaction, lifetime, noncompact boost sector,
Type-II trace, or generalized-entropy identity is derived.

Artifacts: `docs/finite_size_static_patch_observer.md`,
`qgtoy/finite_size_static_patch_observer.py`,
`tests/test_finite_size_static_patch_observer.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy finite-size-static-patch-observer
```

### Research Theorem Y: Finite-Time Heat-Twirl Recovery Obstruction

Assume the interaction-picture charges are constant, either because
`[H_target+H_rot,Q_a]=0` or because a specified toggling control enforces it.
Let the target and rotor undergo active common-mode isotropic rotation diffusion
with a rank-one spatial covariance kernel and equal coupling strengths,
generated by

```text
L(rho)=-gamma sum_(a=1)^3 [Q_a,[Q_a,rho]],
Q_a=J_a^(target)+J_a^(rotor,left).
```

The proper-time channel is convolution with the central `SO(3)` heat kernel,

```text
N_(eta,T)(rho)=integral dg k_(gamma T)(g)
 U_L(g)rho U_L(g)^* tensor U_R(g)eta U_R(g)^*.
```

It starts at the append-only channel and converges to Haar append-and-twirl.
With `s=gamma T` and `q=exp(-4s)`, the signed-random-unitary triangle inequality,
Cauchy-Schwarz, and character orthogonality give the representation-independent
bound

```text
eta_heat(s):=(1/2)||N_(eta,T)-N_(eta,infinity)||_diamond
 <= min{1,(1/2)sqrt[q(9-2q+q^2)/(1-q)^3]}.
```

For every rotor state with `Tr(eta C_left)<=Cbar` and every deterministic CPTP
decoder acting only on the target-plus-rotor output after this finite-time
channel, without the Brownian record, bath output, or bath purification,

```text
epsilon_T
 >= max{0,
      max_(J>=0) max[0,
        1-(J+1)^2/(2L+1)
         -sqrt(Cbar/((J+1)(J+2)))]
      -eta_heat(gamma T)}.
```

Choosing `gamma T=(1/2)log(2L+1)` makes

```text
eta_heat <= 3/[2(2L+1)(1-(2L+1)^-2)^(3/2)]=O(1/L).
```

Thus, if `gamma` is cutoff independent, the finite-time correction vanishes on
the hard-energy sector with the sufficient proper-time choice

```text
T_delta=Theta[gamma^-1 log(R/delta)].
```

This is a conditional Markovian collective-charge theorem, and the displayed
schedule is not a necessary mixing lower bound or observable prediction. The
environment trajectory is inaccessible. The generator is time-local in proper
time but collective in angular charge; it has not been derived from a spatially
local static-patch current interaction. The exact Stratonovich white-noise model
has infinite bandwidth; a finite-bath Davies limit, its approximation error,
the diffusion rate, observer lifetime, and stress-energy backreaction remain
uncontrolled. On full `L^2(SO(3))` the heat-kernel formula defines the mild
semigroup, while the unbounded double-commutator generator is understood on its
natural domain.

Artifacts: `docs/finite_time_rotation_diffusion.md`,
`qgtoy/finite_time_rotation_diffusion.py`,
`tests/test_finite_time_rotation_diffusion.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy finite-time-rotation-diffusion
```

### Research Theorem Y2: Norm-Honest Matter-To-Observer Transfer

For normalized recovery error

```text
e(N)=inf_D (1/2)||D N-id||_diamond,
```

decoder contractivity makes `e` one-Lipschitz in normalized diamond distance.
If a physical channel is within `eta_local` of the collective heat channel and
the heat channel is within `eta_heat` of Haar append-and-twirl, then

```text
e_physical >= max(0,e_Haar,lower-eta_heat-eta_local).
```

For the explicit Peter-Weyl decoder, the same triangle inequality gives

```text
e_physical(D_PW)
 <= min(1,e_Haar,PW,upper+eta_heat+eta_local).
```

The lower branch is uniform under its stated mean-Casimir budget, whereas the
upper branch uses a specified canonical Peter-Weyl token. They are a literal
two-sided bracket only after a common resource condition is proved.

The available finite-switch ULE estimate is intentionally not inserted as
`eta_local`: it is an ancilla-stable state operator-norm residual. For a fixed
spin-`L` pulled-back Choi witness of trace norm `d=2L+1`, it instead proves only

```text
e_witness >= max(0,1-1/d-eta_heat-d epsilon_infinity).
```

For a certified zero-frequency matter spectrum lower bound, the proper-time
collective diffusion rate used in `eta_heat` obeys

```text
gamma >= pi lambda^2 j(0)_lower/N^2.
```

This closes the abstract obstruction/completeness transfer and the currently
available spectral-witness transfer. It does not derive a local physical
diamond estimate, identify the fixed-spin ULE reference with the reducible
Peter-Weyl token, or supply a finite-coupling matter-channel estimate. AU.1,
AU.2, conservative AU.3a, and the tail-dominated authenticated AU.3b baseline
are certified for the prescribed default profile.

Artifacts: `qgtoy/static_patch_matter_observer_channel.py` and
`tests/test_static_patch_matter_observer_channel.py`.

### Research Theorem Z: Common-Mode Locality-Mismatch Witness

Let target and reference axial charges with exchanged-charge gap `Delta>0`
experience correlated Gaussian Markov noise with normalized covariance
`C=[[1,c],[c,1]]`. For the relational coherence
`(|1,0>+|0,1>)/sqrt(2)`, the exact visibility after
`s=gamma T` is

```text
v(s,c)=exp[-2s Delta^2(1-c)].
```

The ideal common-mode channel has `c=1`, so this input gives the normalized
diamond-distance witness

```text
(1/2)||Phi_C,T-Phi_*,T||_diamond
 >= [1-exp(-2 gamma T Delta^2(1-c))]/2.
```

Consequently, keeping the common-mode mismatch below `eta<1/2` requires

```text
1-c <= -log(1-2 eta)/(2 gamma T Delta^2).
```

Under the sufficient heat schedule `gamma T=(1/2)log d` and an error allocation
`eta=A/d`, this becomes

```text
1-c <= -log(1-2A/d)/(Delta^2 log d)
     =O(1/[Delta^2 d log d]).
```

For the illustrative spatial model `c(r)=exp(-r/ell_B)` at fixed separation,
this requires `ell_B/r=Omega(Delta^2 d log d)`. More generally, for finite cells with
bounded charge generators, a Duhamel comparison gives

```text
(1/2)||exp(T L_C)-exp(T L_*)||_diamond
 <= min{1,
    2 gamma T sum_(a,i,j)
      |C_ij-1| ||q_(a,i)|| ||q_(a,j)||}.
```

This theorem quantifies the locality gate but does not pass it. The exact lower
witness is axial, the upper estimate is finite-dimensional/bounded-generator,
and no static-patch bath covariance, Davies limit, or gravitational
stress-energy is derived.

Artifacts: `docs/common_mode_locality_mismatch.md`,
`qgtoy/common_mode_locality_mismatch.py`,
`tests/test_common_mode_locality_mismatch.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy common-mode-locality-mismatch
```

### Research Theorem AA: Bunch-Davies Scalar Common-Mode Obstruction

Consider two equal-redshift localized axial zero-Bohr charge components with gap
`Delta>0`, identical coupling normalization and optically pointlike profiles,
coupled locally and stationarily to the conformally coupled Bunch-Davies scalar.
The exact optical Wightman spectral density implies that at hyperbolic optical separation
`y=d_H/R`, the normalized zero-frequency cross spectrum is

```text
c_0(y)=y/sinh(y).
```

In the zero-Bohr-frequency Davies surrogate, Research Theorem Z therefore gives

```text
(1/2)||Phi_scalar,T-Phi_common,T||_diamond
 >= [1-exp(-2 gamma T Delta^2[1-y/sinh(y)])]/2.
```

For every fixed `y>0`, this witness tends to `1/2` as `gamma T` grows. If the
sufficient heat schedule `gamma T=(1/2)log d` is used and scalar-bath mismatch
is allocated error `A/d`, then necessarily

```text
1-y/sinh(y)
 <= D_d:=-log(1-2A/d)/(Delta^2 log d).
```

The elementary inequality `sinh(y)>=y+y^3/6` yields the rigorous consequence

```text
y<=sqrt[6D_d/(1-D_d)]
 =O(1/[Delta sqrt(d log d)]).
```

For two supports on one shell at proper horizon distance `rho` and angular
separation `theta`,

```text
cosh(y)=1+2 cot^2(rho/R) sin^2(theta/2),
```

so the allowed angle obeys

```text
theta=O[(rho/R)/(Delta sqrt(d log d))].
```

With the declared collar law `d=Theta(sqrt(R/rho))`, this is
`O((rho/R)^(5/4)/sqrt(log(R/rho)))` for fixed `Delta`. Hence fixed nonzero
same-shell separation cannot realize the rank-one common mode in this named
local scalar-bath surrogate.

The theorem is axial and zero-frequency. It does not identify the actual hard
angular target with a localized charge, derive a rotationally invariant
field-top torque, control finite switching or optical smearing, prove a rigorous
point-coupling Davies limit, or include backreaction.

Artifacts: `docs/static_patch_scalar_common_mode.md`,
`qgtoy/static_patch_scalar_common_mode.py`,
`tests/test_static_patch_scalar_common_mode.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-scalar-common-mode
```

### Research Theorem AB: Exact Radial-Smearing Invariance

Let

```text
phi_0(y)=y/sinh(y)
```

be the zero-frequency Bunch-Davies spatial kernel on optical `H^3_R`. Its
normalized mean over a hyperbolic sphere of radius `uR` around a point at
distance `rR` from the kernel center obeys

```text
M_u phi_0(r)=phi_0(u)phi_0(r).
```

Indeed, the hyperbolic law of cosines and the change of variables from the
angular cosine to the pair distance give

```text
(1/2) integral_(-1)^1 phi_0(d(z)) dz
 =1/[2 sinh r sinh u] integral_|r-u|^(r+u) d dd
 =ru/[sinh r sinh u].
```

Let `mu_p` and `nu_q` be arbitrary nonnegative normalized radial measures in
the optical volume measure, centered at `p` and `q`, and define their positive
spherical amplitudes `A_mu,A_nu`. Repeated use of the product formula yields

```text
B_pp=A_mu^2,
B_qq=A_nu^2,
B_pq=A_mu A_nu phi_0[d(p,q)/R].
```

Hence the normalized zero-frequency cross coefficient is exactly

```text
B_pq/sqrt(B_pp B_qq)=phi_0[d(p,q)/R],
```

independent of both radial profile sizes and shapes. The profiles need not be
identical. Therefore finite radial worldtube width cannot repair the fixed-
center-separation common-mode obstruction of Research Theorem AA.

At arbitrary real spectral parameter `p`,

```text
phi_p(y)=phi_0(y)sinc(py),
```

so `|phi_p(y)|<=phi_0(y)`. For any common nonnegative spectral/filter weight
`w(p)` and radial transforms `A_f,A_g`, weighted Cauchy-Schwarz gives

```text
|integral w A_f A_g phi_p dp|
 <=phi_0(y)
   sqrt[integral w A_f^2 dp]
   sqrt[integral w A_g^2 dp].
```

Hence arbitrary common finite switching cannot raise the normalized scalar
pure-dephasing correlation above the zero-mode center value. This finite-time
ceiling does not require a Davies limit, although it does not control
dissipative jump sectors.

This is an established spherical-function identity applied to the observer
problem, not a new harmonic-analysis theorem. It assumes stationary nonnegative
profiles radial in the optical measure and suitable conformal source weights.
It does not cover nonradial torque multipoles, noncommuting/dissipative
three-axis channels, a full `SO(3)` top, or backreaction. Physical sources must
realize radial effective optical profiles after the conformal weight
`f_opt=Omega^3 J`.

Artifacts: `docs/static_patch_radial_smearing.md`,
`qgtoy/static_patch_radial_smearing.py`,
`tests/test_static_patch_radial_smearing.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-radial-smearing
```

### Research Theorem AC: Polarization-Resolved Gradient-Coupling Obstruction

On optical `H^3_R`, let two localized zero-Bohr vector charges couple to the
orthonormal components of `nabla Phi_opt`, with frames related by parallel
transport along their center geodesic. For

```text
phi_0(y)=y/sinh(y),    y=d_H(p,q)/R,
```

the normalized cross Kossakowski matrix is

```text
C(y)=diag(c_parallel,c_perp,c_perp),
c_parallel=-3 phi_0''(y),
c_perp=-3 phi_0'(y)/sinh(y),
```

while each coincident auto block is isotropic and proportional to
`delta_ab/(3R^2)`. The positive-definite spherical kernel guarantees that the
joint block `[[I,C],[C,I]]` is positive semidefinite.

Axis by axis, this block diagonalizes into collective `L_a+J_a` and relative
`L_a-J_a` channels with rate weights `1+c_a` and `1-c_a`. Since
`c_parallel,c_perp<1` at every nonzero separation, the model necessarily
contains relative rotational noise and cannot equal the ideal collective
`SO(3)` heat generator away from coincidence.

Near coincidence,

```text
1-c_parallel=(7/10)y^2+O(y^4),
1-c_perp=(2/5)y^2+O(y^4).
```

Conditionally imposing the earlier one-axis `A/d` mismatch allocation on each
eigenchannel along `gamma T=(1/2)log d` again forces

```text
y=O(1/[Delta sqrt(d log d)]),
```

with the longitudinal polarization setting the stricter constant. This
quantitative transfer is axiswise. A full finite-time witness is available in
the two-spin-half sector. If the ideal collective channel and the anisotropic
gradient channel act on the singlet, the latter remains Bell diagonal with

```text
d/ds [u] = [-4       4 c_perp    ] [u],
     [v]   [2 c_perp -4+2c_parallel] [v],
u(0)=v(0)=-1.
```

Writing `m=-4+c_parallel` and
`kappa=sqrt(c_parallel^2+8c_perp^2)`, the exact solution is

```text
u=e^(ms)[-cosh(kappa s)
 +(c_parallel-4c_perp)sinh(kappa s)/kappa],
v=e^(ms)[-cosh(kappa s)
 -(c_parallel+2c_perp)sinh(kappa s)/kappa].
```

The singlet survival probability is `p_S=(1-u-2v)/4`. Since the ideal output is
the singlet and the actual output is Bell diagonal,

```text
(1/2)||E_s-E_s^collective||_diamond >= 1-p_S.
```

Near coincidence,

```text
1-p_S=(3/2)s y^2+O(y^4).
```

Thus `s=(1/2)log d` and an `A/d` allocation imply the leading bound

```text
y<=sqrt[4A/(3d log d)].
```

This is an exact noncommuting three-axis channel witness for two spin-half
charges. Research Theorem AD extends the singlet calculation to every integer
spin within the same effective channel.

The interaction is a conditional proper-rotation-covariant gyroscopic coupling
to an engineered optical gradient. It is parity odd for an ordinary scalar and
is not a derived mechanical torque on a spherical top. The physical conformal
gradient, smooth derivative smearing, local matter source, a growing-spin
uniform Davies limit, holding stress, lifetime, and backreaction remain open.

The Hessian and bitensor identities are standard. The possible contribution is
their use as exact polarization-resolved input to the finite-reference recovery
obstruction, not a new maximally symmetric-space identity.

Artifacts: `docs/static_patch_gradient_torque.md`,
`qgtoy/static_patch_gradient_torque.py`,
`tests/test_static_patch_gradient_torque.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-gradient-torque
```

### Research Theorem AD: Casimir-Enhanced Higher-Spin Co-Location Law

Let `P_L` be the total-spin-zero projector in `V_L tensor V_L`. The ideal
collective channel fixes `P_L`. For the anisotropic gradient channel, the
singlet survival probability has the exact tensor-rank decomposition

```text
p_L(s)=sum_(ell=0)^(2L) (2ell+1)/(2L+1)^2
       <s_ell|exp(s B_ell)|s_ell>,
```

where `s_ell,m=(-1)^(ell-m)/sqrt(2ell+1)` and

```text
(B_ell)_(m,m)=-2ell(ell+1)+2c_parallel m^2,
(B_ell)_(m+1,m)=-c_perp(ell-m)(ell+m+1).
```

Thus the exact integer-spin witness requires only tridiagonal blocks of maximum
size `4L+1`, not the full `d^4` Liouvillian.

Put

```text
Delta=(1-c_parallel)+2(1-c_perp).
```

The singlet first variation and a uniform Duhamel remainder are

```text
1-p_L(s)=(4/3)L(L+1)s Delta+R_L,
|R_L|<=32s^2L^4Delta^2.                                (AD.1)
```

The finite-time coefficient follows from
`Var_(P_L)(L_a-J_a)=4L(L+1)/3`. The remainder follows from

```text
||G_delta-G_0||_(2->2)<=8L^2Delta.
```

Since the gradient kernel obeys

```text
Delta=(3/2)y^2+O(y^4),
```

equation (AD.1) becomes

```text
1-p_L(s)=2L(L+1)s y^2
 +O(sL^2y^4+s^2L^4y^4).                                (AD.2)
```

With `d=2L+1`, `s=(1/2)log d`, and an `A/d` mismatch allocation, the controlled
leading consequence is

```text
y<=sqrt[A/(dL(L+1)log d)]
 =O[d^(-3/2)/sqrt(log d)].                              (AD.3)
```

At (AD.3), the Duhamel expansion parameter is `O(1/d)`, so the remainder is
lower order. The channel comparison uses the singlet as a diamond-norm probe;
it is not by itself a lower bound restricted to product-prepared target and
reference inputs.

This theorem closes the arbitrary integer-spin witness inside the declared
Markovian gradient GKSL model. It does not derive that model from a smooth
matter action, prove a Davies approximation uniform in `L`, control derivative
smearing, or close lifetime, support-stress, and gravitational backreaction
errors.

Artifacts: `docs/static_patch_higher_spin_gradient.md`,
`qgtoy/static_patch_higher_spin_gradient.py`,
`tests/test_static_patch_higher_spin_gradient.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-higher-spin-gradient
```

### Research Theorem AE: Local Pseudoscalar Gyroscope And Davies Tradeoff

Let `chi` be a conformally coupled pseudoscalar and `u` the static observer
congruence with acceleration `a^mu=u^nu nabla_nu u^mu`. The marked-top action

```text
S_top=int d tau[-m+(I/2)|varpi^a-g B^a|^2],
B_a=e_a^mu(nabla_mu chi+a_mu chi),
```

is local and parity even. Its Hamiltonian contains

```text
H_int=g J_a^left B_a,
```

and `[C_left,J_a^left]=0`, so the top operators are exactly zero Bohr frequency.

For `g_dS=N^2g_opt` and `chi_dS=N^-1chi_opt`, the improved derivative satisfies

```text
N^2(nabla_hat^dS chi_dS+a_hat^dS chi_dS)
=D_hat^opt chi_opt.                                    (AE.1)
```

Hence equal-redshift localized spins have exactly the normalized optical
gradient covariance of Research Theorems AC-AD. The action supplies a parity-
consistent local realization of the top-side coupling. It selects the static
congruence and breaks pseudoscalar shift symmetry; the raw physical gradient
does not have the same isotropic auto tensor.

Proper time `tau=Nt` and (AE.1) give

```text
S_tau(0)=N^-3 S_opt(0),
tau_B=N tau_B,opt.                                     (AE.2)
```

Thus a fixed physical coupling on spin `L` has loaded Markov parameter

```text
gamma_tau tau_B
=g^2L(L+1)N^-2S_opt(0)tau_B,opt,                       (AE.3)
```

which diverges in the collar limit. There is no cutoff-uniform Davies
justification at fixed `g`.

Alternatively, after smooth optical smearing, impose a fixed interaction RMS
on a declared spin-sector reference state. Since its angular-momentum second
moment is `L(L+1)` and the physical improved-gradient rms scales as `N^-2`,
this gives

```text
g=O[N^2/sqrt(L(L+1))],
gamma_tau=O[N/L(L+1)],
T_schedule=Theta[L(L+1)log(d)/N].                      (AE.4)
```

Along `N~rho/R~1/d`,

```text
T_schedule=Theta[d^3 log d],
theta=O[d^(-5/2)/sqrt(log d)].                         (AE.5)
```

The first relation is the time required to run the selected sufficient heat
schedule under the RMS-saturated rate; it is not a necessary mixing-time lower
bound. The second imports the higher-spin co-location theorem through the exact
same-shell optical geometry.

The action derives the localized top and lumped-spin zero-Bohr coupling, not
the global hard field charge. A local hard target has interaction
`int B_a(x)ell_T^a(x)`; Research Theorem AF gives conditional spatial-multipole
and nonzero-Bohr bounds for it. Smooth derivative renormalization, a QFT-uniform
Davies error, an operator or all-state interaction bound, source/support stress,
lifetime, and gravitational backreaction remain open.

Artifacts: `docs/static_patch_pseudoscalar_gyroscope.md`,
`qgtoy/static_patch_pseudoscalar_gyroscope.py`,
`tests/test_static_patch_pseudoscalar_gyroscope.py`.

### Research Theorem AF: Distributed Hard-Current Multipoles And Bohr Leakage

Let a hard target carry local angular-current density `ell_a(x)` on a
geodesically convex worldtube. Fix parallel transport to a center frame `p`,
denote transported components by bars, and set `L_a=int ellbar_a(x)`. For

```text
V=g sum_a int Bbar_a(x) tensor ellbar_a(x),
V_0=g sum_a B_a(p) tensor L_a,
```

one has the exact identity

```text
V-V_0=g sum_a int [Bbar_a(x)-B_a(p)] tensor ellbar_a(x). (AF.1)
```

On a product reference vector, suppose
`||(B_a(x)-B_a(p))psi_B||<=K r(x)` and define
`j_a(x)=||ell_a(x)psi_T||`. Then

```text
||(V-V_0)(psi_B tensor psi_T)|| <= |g| K M_1,
M_1=sum_a int r(x)j_a(x).                              (AF.2)
```

If the hypotheses instead hold as operator bounds on invariant compressed
subspaces, (AF.2) is a compressed operator bound and the corresponding unitary
channels satisfy

```text
||U_T(.)U_T^dagger-U_(0,T)(.)U_(0,T)^dagger||_diamond
 <= min(2,2T|g|KM_1).                                  (AF.3)
```

Let `ellbar_a(x;omega)` be the Bohr decomposition under `H_T`. If
`[H_T,L_a]=0`, then

```text
int ellbar_a(x;omega)=0,  omega != 0,                  (AF.4)
```

and every nonzero-Bohr interaction is exactly

```text
V_omega=g sum_a int [Bbar_a(x)-B_a(p)]
                     tensor ellbar_a(x;omega).         (AF.5)
```

It is therefore bounded by its sector first moment. A one-component `U(1)`
two-cell spin-half model with local currents `(sigma_z+sigma_x)/2` and
`(sigma_z-sigma_x)/2` saturates the linear `|g|Ka` bound. This does not prove
sharpness under full three-component rotational invariance.

Now add a declared interaction-to-jump transfer hypothesis. In a normalized
diagonal-jump finite-dimensional surrogate with unit rates, no Kossakowski
mixing, and no Lamb-shift perturbation, let the ideal zero-Bohr jumps obey
`||A_a||<=L` and their multipole corrections obey `||E_a||<=epsilon_0L`.
The dissipator identity and Duhamel formula give, for three axes,

```text
delta_0<=3sL^2(4epsilon_0+2epsilon_0^2).               (AF.6)
```

Under strict secular separation and the aggregate nonzero-Bohr condition
`sum_(a,omega!=0)||E_(a,omega)||^2<=3L^2epsilon_nz^2`, zero monopole gives

```text
delta_nz<=6sL^2epsilon_nz^2.                           (AF.7)
```

At `s=(1/2)log d`, `L=(d-1)/2`, and channel budget `A/d`, sufficient caps are

```text
epsilon_0=O(d^-3/log d),
epsilon_nz=O[d^(-3/2)/sqrt(log d)].                    (AF.8)
```

Declare separate `O(1)` transfer bounds for the zero-Bohr linear jump error,
the aggregate squared norm over all nonzero gaps, and the zero-Bohr
second-order jump error. With dimensionless relative Lipschitz/current factors,
a sufficient worst-case generic design is

```text
a_opt/R=O(d^-3/log d),
theta_support=O(d^-4/log d)                            (AF.9)
```

on `rho/R~1/d`. If instead every transported compressed zero-Bohr current-dipole
component vanishes as an operator and a covariant bath Hessian bound makes its
remainder second order, then the nonzero-Bohr
and center-distance scales are sufficient. For distinct equal-size worldtubes,
Research Theorem AD and disjointness give

```text
a_opt/R <= y_d/2=O[d^(-3/2)/sqrt(log d)],
theta_support=O[d^(-5/2)/sqrt(log d)].                 (AF.10)
```

This quadratic branch is conditional on componentwise transported operator
dipole cancellation; its
disjointness conclusion is conditional on nonoverlap. Distinguishable
overlapping sectors evade the latter.

The theorem does not derive the Lipschitz or current moments from matter,
the three interaction-to-jump transfers, Kossakowski/Lamb-shift stability, strict
secular aggregation, or a uniform Davies limit from QFT, promote the
product-vector estimate to an all-state bound, or control localization stress
and gravitational backreaction. The displayed support laws are sufficient
uniform guarantees, not necessary bounds.

Artifacts: `docs/static_patch_hard_current_multipole.md`,
`qgtoy/static_patch_hard_current_multipole.py`,
`tests/test_static_patch_hard_current_multipole.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-hard-current-multipole
```

### Research Theorem AG: Controlled Compactness-Localization Branch Obstruction

Assume the reference top and hard target are distinct equal-redshift,
equal-radius nonoverlapping thin-shell worldtubes, the top spin equals the
protected hard-sector spin `L`, and its three-dimensional proper enclosing
radius `a` obeys the declared spherical-top model

```text
I=kappa m a^2,   E_rot/m<=zeta,
2G(m+E_rot)/a<=chi.                                     (AG.1)
```

The finite-top capacity theorem gives the exact radius floor

```text
a_min=[2G^2(1+zeta)^2L(L+1)/(kappa chi^2 zeta)]^(1/4)
     ~ C_min sqrt(G)d^(1/2),                             (AG.2)
C_min=[(1+zeta)^2/(2kappa chi^2 zeta)]^(1/4),
```

where `d=2L+1`. On a shell at `u=rho/R`, optical center separation `y` has
exact angle and static-slice center distance

```text
theta=2asin[tan(u)sinh(y/2)],
D_slice=2R asin[cos(u)sin(theta/2)]
       =R sin(u)y[1+O(y^2)].                             (AG.3)
```

Along the collar `rho/R=1/d`, the leading local-common-mode law

```text
y_d=sqrt[A/(dL(L+1)log d)]
```

and equal-radius nonoverlap imply

```text
a<=a_nonoverlap
  ~sqrt(A)R d^(-5/2)/sqrt(log d).                        (AG.4)
```

Consequently

```text
a_nonoverlap/a_min
 ~[sqrt(A)/C_min][R/sqrt(G)]d^(-3)/sqrt(log d),          (AG.5)
```

which tends to zero at fixed `R^2/G`. There is no growing-dimension sequence
that remains in the controlled local perturbative common-mode branch while
satisfying (AG.1)-(AG.4). This statement does not control hypothetical
nonperturbative large-separation behavior. The controlled-envelope crossover
obeys

```text
d^3sqrt(log d)=O(R/sqrt(G)),
d=O[(R/sqrt(G))^(1/3)/(log d)^(1/6)].                    (AG.6)
```

For the sufficient hard-current designs of Research Theorem AF, the minimum-top
compactness utilization `U=2GE_min/(chi a)` instead scales as

```text
U_generic=Theta[(G/R^2)d^9(log d)^2],
U_dipole=Theta[(G/R^2)d^6log d].                         (AG.7)
```

Thus both declared sufficient design certificates close at finite `d`. This is
not a necessary failure theorem for every larger support.

The branch closure is conditional on identifying the top and hard-sector spins,
bounding a thin-shell three-dimensional enclosing radius by the same-shell
static-slice distance, keeping the dimensionless mismatch/transfer constants
`O(1)`, and imposing distinct equal-radius nonoverlapping worldtubes. Equation
(AG.4) uses a leading perturbative necessary co-location law, so a finite
integer crossing is an illustrative asymptotic crossover rather than an exact
global channel cutoff. Overlapping
distinguishable sectors, a different inertia law, or a different channel can
evade the conclusion. No matter stress tensor, binding energy, lifetime,
Einstein-matter solution, uniform Davies theorem, or general collapse theorem is
proved.

The lower-radius scaling is consistent with known general-relativistic
size-angular-momentum inequalities and is not claimed as new. The candidate
contribution is its collision with the channel-derived upper support law. Nor
does a definite Casimir sector by itself certify a useful directional-reference
state; the physical encoding remains an input to the successor model.

With the certificate defaults `R=1`, `G=10^-12`, `kappa=2/3`, `chi=1/2`,
`zeta=1/4`, and unit error coefficients, the leading nonoverlap envelopes cross
at `L=30` (`d=61`), while the conservative generic GKSL design crosses at `L=6`.
These are parameter-dependent diagnostics, not universal predictions.

Artifacts: `docs/static_patch_localization_backreaction.md`,
`qgtoy/static_patch_localization_backreaction.py`,
`tests/test_static_patch_localization_backreaction.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-localization-backreaction
```

### Research Calculation AH: Overlapping Zero-Bohr Spectral Baseline

Place two operationally distinguishable integer-spin-`L` sectors in one
worldtube. Write `d=2L+1`, let `N>0` be the collar lapse, and set

```text
H_S=h_T(L_T^2)+h_R(L_R^2),
Q_a=L_(T,a)+L_(R,a),
V=(lambda/N)sum_a Q_a tensor B_a.                        (AH.1)
```

Every `Q_a` is zero Bohr frequency on `V_L tensor V_L`. For the declared
KMS-compatible Gaussian spectral ansatz

```text
j_sigma(w)=w(1+R^2w^2)e^(-sigma^2w^2)
            /[12pi^2R^2(1-e^(-2pi Rw))],                (AH.2)
```

one has exactly

```text
j_sigma(-w)=e^(-2pi Rw)j_sigma(w),
j_sigma(0)=1/(24pi^3R^3).                                (AH.3)
```

The collective zero-frequency jumps and each target/reference Kossakowski block
are

```text
A_a=(lambda/N)sqrt(2pi j_sigma(0))Q_a,
K_a=[2pi lambda^2j_sigma(0)/N^2][[1,1],[1,1]].           (AH.4)
```

There are three rank-one blocks, so the full six-operator matrix has rank three.
In the standard Davies Hilbert-transform convention,

```text
H_LS=(lambda^2/N^2)s_sigma sum_a Q_a^2,
s_sigma=-1/(24pi^(3/2)R^2sigma)-1/(48pi^(3/2)sigma^3).  (AH.5)
```

The total-spin singlet is exactly annihilated by every `Q_a`; it is dark under
the full system-bath Hamiltonian, not merely under the Markov generator.
Therefore singlet survival cannot test the accuracy of the ULE/Davies
approximation.

For a pure prepared reference and maximally entangled target-memory input, the
rank-one return projector is non-dark. For the normalized collective heat
generator its initial return decay obeys

```text
-p'_return(0)=2sum_a Var(Q_a)>=2L(L+2)>0.               (AH.6)
```

At `s=(1/2)log d` the collective heat channel also obeys

```text
p_return<=1/d+3/[2d(1-d^-2)^(3/2)]=O(1/d).              (AH.7)
```

This fixed experiment has a dimension-free spectral-error transfer because its
projector has trace norm one. It is not an all-decoder theorem. For every
deterministic decoder, the pulled-back entanglement-fidelity witness has trace
norm exactly `d`, so an ancilla-stable Choi spectral residual gives

```text
epsilon_rec_exact>=1-1/d-eta_heat-d epsilon_infinity.    (AH.8)
```

Here `eta_heat=3/[2d(1-d^-2)^(3/2)]` is the stated heat-to-Haar correction and
`epsilon_rec_exact` is the deterministic-decoder recovery-error lower bound.

The Gaussian factor in (AH.2) is exactly generated by the shifted optical
heat semigroup

```text
exp[(sigma^2/2)(Delta_H+R^-2)],                          (AH.9)
```

whose field-amplitude multiplier is `exp(-sigma^2w^2/2)`. Its kernel has full
support, so this is a stationary covariant quasilocal regulator rather than a
bounded-worldtube interaction. No compact profile can reproduce the exact
Gaussian: compact support gives an entire spherical transform of exponential
type, while the Gaussian continuation grows quadratically in the exponent on
the imaginary axis. The spherical Paley--Wiener input is the standard symmetric-
space theorem; see [Olafsson and Wolf](https://arxiv.org/abs/1101.4419).

An explicit compact replacement starts from a hyperbolic ball of optical
radius `a`, `A=a/R`, with normalized spherical multiplier

```text
q_A(p)=[cosh(A)sin(Ap)-p sinh(A)cos(Ap)]
       /[p(1+p^2)(A cosh(A)-sinh(A))].                 (AH.10)
```

Convolving two seed balls gives a field profile supported in radius `2a` and
the exact spectrum `j_A(w)=j_0(w)q_A(Rw)^4`. It preserves (AH.3), and
`|q_A(p)|=O(p^-2)` makes the spectrum `O(w^-5)`. Hence the Lamb shift and the
required jump-correlator moments are finite. Compact smooth radial seed
functions give a smooth compact spatial profile with rapid spectral decay; a
compact spacetime AQFT test function additionally requires switching. The
hard-ball formula is an idealized finite-regularity baseline.

Let `G=int|g(t)|dt`, `M_1=int|t g(t)|dt`, where
`g=(2pi)^(-1/2)FT[sqrt(j)]`. Frequency Sobolev norms give explicit finite
bounds for both moments. For three diagonal gradient channels, Nathan and
Rudner's constants are

```text
Gamma=144 lambda^2L^2G^2/N^2,
tau=M_1/G.                                               (AH.11)
```

Under their stationary zero-mean Gaussian-bath and remote-past factorization
hypotheses, adjoin an arbitrary inert memory. The coupling norms are unchanged,
and the zero-Bohr ULE is unital. The modified-state and Duhamel estimates give
the ancilla-stable spectral-state theorem

```text
epsilon_infinity(t)<=2Gamma tau+2Gamma^2 tau t.          (AH.12)
```

The imported modified-state and residual estimates are from Nathan and Rudner,
[Phys. Rev. B 102, 115109 (2020)](https://doi.org/10.1103/PhysRevB.102.115109),
Appendix C, with its
[2021 erratum](https://doi.org/10.1103/PhysRevB.104.119901).

At heat time `pi lambda^2j(0)t/N^2=(1/2)log d`, this is

```text
epsilon_infinity <=
 288GM_1 lambda^2L^2/N^2
 +[20736G^3M_1/(pi j(0))]lambda^2L^4N^-2log d.          (AH.13)
```

If `epsilon_infinity<=A/d` for a fixed `0<A<1`, (AH.8) gives the asymptotic
recovery obstruction `1-A-o(1)`. On `N=1/d`, the following schedule is
sufficient under the stated hypotheses:

```text
lambda=O[d^(-7/2)/sqrt(log d)].                         (AH.14)
```

Matching the heat `O(1/d)` contribution in the recovery error is guaranteed by
the stronger budget `epsilon_infinity=O(d^-2)` and sufficient schedule

```text
lambda=O[d^-4/sqrt(log d)].                             (AH.15)
```

Equation (AH.12) is not a trace- or diamond-norm theorem. Research Theorem AS
replaces remote-past preparation by a prescribed amplitude ramp, stationary
plateau, and explicit burn-in transient without changing the scaling laws. A
profile-specific smooth compact source, certified Sobolev constants, derivation
of the switch from the matter action, direct target/reference interactions,
source stress, lifetime, and gravity remain open.

Artifacts: `docs/overlapping_qft_davies_program.md`,
`docs/static_patch_worldtube_ule.md`,
`qgtoy/static_patch_overlapping_ule.py`,
`qgtoy/static_patch_worldtube_ule.py`,
`qgtoy/static_patch_finite_switching_ule.py`,
`tests/test_static_patch_overlapping_ule.py`,
`tests/test_static_patch_worldtube_ule.py`, and
`tests/test_static_patch_finite_switching_ule.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-overlapping-ule
PYTHONPATH=. python3 -m qgtoy static-patch-worldtube-ule
```

### Research Calculation AI: Massive-Skyrmion Profile And Worldtube Gate

Use signature `(+---)` and normalize the mass term as

```text
(f_pi^2 m_pi^2/16)Tr(U+U^dagger-2),
```

so `m_pi` is the physical small-fluctuation mass. With
`x=e f_pi r`, `mu=m_pi/(e f_pi)`, `lambda=(e f_pi R)^-2`,
`N=1-lambda x^2`, `s=sin F`, and `u=x^2+8s^2`, the exact reduced equations are

```text
E=(1/8)N u F'^2+s^2/4+s^4/(2x^2)
  +(mu^2x^2/4)(1-cos F),                                (AI.1)

(N u F')'=(4N F'^2+1+4s^2/x^2)sin(2F)
           +mu^2x^2 sin F.                              (AI.2)
```

The dependency-free flat shooting solution at `mu=1`, matched at `x=10` to the
massive `l=1` Robin tail, gives

```text
b=1.58023676, c_M=48.6317632, c_I=34.3539730.           (AI.3)
```

The numerical profile is monotone, has unit baryon number, and satisfies the
Derrick identity `E_2-E_4+3E_0=0` at the declared tolerance.

In fixed de Sitter, regularity at `x_c=lambda^-1/2` requires

```text
N'_c u_c F'_c=(1+4sin^2(F_c)/x_c^2)sin(2F_c)
               +mu^2x_c^2 sin(F_c).                    (AI.4)
```

For generic regular horizon data, the global rigid-rotor inertia diverges:

```text
c_I(epsilon)~(pi x_c/3)
 [x_c^2sin^2(F_c)+4sin^4(F_c)]log(1/epsilon).            (AI.5)
```

Thus the untruncated static-patch rotor diverges for the declared generic
horizon data. A supported worldtube at `x_w<x_c` is the selected controlled
matter model, not yet a logically forced consequence for every nontrivial
global profile. Separately, the
dynamical collective orientation supplies a covariant soldering
`J_i=-D_ai(A)I_a`, allowing the parity-even worldline coupling `B_mu S^mu`
without a fixed external triad. This does not yet produce a point-local
interaction solely from the bare Skyrme field.

Artifacts: `docs/massive_skyrmion_observer_program.md`,
`qgtoy/massive_skyrmion_profile.py`,
`tests/test_massive_skyrmion_profile.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy massive-skyrmion-profile
```

### Research Calculation AJ: Centered Membrane-Supported Skyrmion

Introduce a covariant spherical ideal-mirror membrane whose multiplier imposes
`U=1`, equivalently `F(x_w)=0`, at `x_w<x_c`. With `F(0)=pi`, the interior ball
has exact hedgehog baryon number one. The dimensionless radial pressure and
centered shell mean curvature are

```text
p_bar=N F'^2/8+Nsin^2(F)F'^2/x^2
      -sin^2(F)/(4x^2)-sin^4(F)/(2x^4)
      -mu^2(1-cos F)/4,                                 (AJ.1)

K_bar=2sqrt(N_w)/x_w-lambda x_w/sqrt(N_w).              (AJ.2)
```

At the hard wall, `p_bar=N_wF_w'^2/8`. Young-Laplace balance selects
`sigma_bar=p_bar/K_bar`. A positive-tension membrane can balance positive
interior pressure only when

```text
x_w<sqrt[2/(3lambda)]=sqrt(2/3)x_c.                     (AJ.3)
```

For `mu=1`, `lambda=0.0025`, and `x_w=4`, the dependency-free solution has
`b=1.5799534`, positive equilibrium tension, exact wall baryon number, and
wall-to-interior mass ratio below two percent. Step halving stabilizes the
interior mass and inertia at the declared tolerance.

This is a centered fixed-background force-balance construction, not a wall
stability or off-center support theorem. Finite stiffness, wall modes, Einstein
junction conditions, and near-horizon acceleration remain open.

Artifacts: `docs/massive_skyrmion_worldtube.md`,
`qgtoy/massive_skyrmion_worldtube.py`,
`tests/test_massive_skyrmion_worldtube.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy massive-skyrmion-worldtube
```

### Research Theorem AK: Fermionic Skyrmion Projective Reference

The standard fermionic `B=1` Finkelstein-Rubinstein sector is

```text
R_J^-=direct_sum_(a=0)^J V_(a+1/2) tensor V_(a+1/2)^*,
D_J^-=(2/3)(J+1)(J+2)(2J+3).                            (AK.1)
```

Its canonical token changes sign under the `SU(2)` center, but its density,
covariant POVM effects, and orientation kernel are center invariant. It is
therefore an `SO(3)` operational reference for an integer-spin target, provided
the right/isospin multiplicity is accessible.

The exact tensor-rank multiplier is

```text
lambda^-_(J,k)=
 [sum_(a,b=0)^J(2a+2)(2b+2)1_(|a-b|<=k<=a+b+1)]
 /[(2k+1)D_J^-].                                        (AK.2)
```

For `0<=k<=2J+2`,

```text
1-lambda^-_(J,k)=
 k(k+1)[12(J+1)(J+2)+2-k(k+1)]
 /[6(2k+1)D_J^-].                                       (AK.3)
```

The mean left Casimir and, for `J+1>=L`, the exact entanglement fidelity are

```text
Cbar_J^-=3[4(J+1)(J+2)-3]/20,                           (AK.4)

F_e=1-2L(L+1)[20(J+1)(J+2)-4L(L+1)+3]
       /[15D_J^-(2L+1)].                                (AK.5)
```

All identities are certified by exact rational counting. The physical rotor
adds the independent slow-rotation gate

```text
epsilon_rot=e^2sqrt[(J+1/2)(J+3/2)]/c_I,
E_rot/M=e^4(J+1/2)(J+3/2)/(2c_Ic_M).                    (AK.6)
```

At fixed `e`, a fixed dimensionless Skyrmion profile cannot support an
asymptotically growing reference cutoff. More generally, slow rotation alone
requires `e^2J/c_I -> 0`, reducing to `e^2J -> 0` for fixed `c_I`; correlated
scaling of `e` can satisfy this condition. The compactness constraint in
Theorem AL is what closes that fixed-profile escape. State preparation,
isospin access, `Omega^4` control, radiation, wall dynamics, and gravity remain
open.

Artifacts: `docs/skyrmion_projective_reference.md`,
`qgtoy/skyrmion_projective_reference.py`,
`tests/test_skyrmion_projective_reference.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-projective-reference
```

### Research Theorem AL: Fixed-Profile Skyrmion Joint-Control Obstruction

Fix the dimensionless centered hard-wall profile `(mu,lambda,x_w)` with mass
and inertia constants `(c_M,c_I)`. Then

```text
M=c_M/(e^2R sqrt(lambda)),
a=x_wR sqrt(lambda),
I=c_IR sqrt(lambda)/e^2.                                (AL.1)
```

The compactness and maximum-spin slow-rotation parameter obey

```text
C=2GM/a=2Gc_M/(e^2x_wlambda R^2),
epsilon_rot=e^2sqrt[K(K+1)]/c_I,                        (AL.2)

C epsilon_rot=
2Gc_Msqrt[K(K+1)]/(c_Ix_wlambda R^2).                   (AL.3)
```

The product is independent of the constrained `e`/`f_pi` co-scaling that keeps
`e f_pi`, and hence the dimensionless profile, fixed. Therefore fixed budgets
`C<=C_*` and `epsilon_rot<=epsilon_*` admit a coupling if and only if

```text
sqrt[K(K+1)]<=
C_*epsilon_*c_Ix_wlambda R^2/(2Gc_M).                   (AL.4)
```

At fixed `R^2/G`, the admissible spin set is finite. No such fixed-profile
co-scaling can produce an asymptotically growing cutoff with both compactness
and rigid rotation controlled. With the certificate defaults, the largest
fermionic `B=1` source spin is `K=173.5`, corresponding to reference cutoff
`J=173`; this number is illustrative and parameter dependent.

The theorem fixes the dimensionless profile and centered ideal-wall source. It
does not exclude profile-changing double scalings, wall inertia, different
matter, `Omega^4` deformation, radiation, off-center support, or full
Einstein-Skyrme solutions.

Artifacts: `docs/skyrmion_joint_scaling_no_go.md`,
`qgtoy/skyrmion_joint_scaling_no_go.py`,
`tests/test_skyrmion_joint_scaling_no_go.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-joint-scaling-no-go
```

### Research Proposition AL.1: Conditional Fixed-Profile Observer-Capacity Floor

In the fermionic `B=1` sector, the physical maximum spin is `K=J+1/2` for odd
Peter-Weyl cutoff `J`. Combining (AL.4) with the sharp projective fusion floor
gives

```text
J<=J_max(C_*,epsilon_*,c_M,c_I,x_w,lambda,R^2/G),

R_frame>=sin^2[pi/(2(J_max+2))]>0.                    (AL.5)
```

Thus no `e`/`f_pi` co-scaling at fixed dimensionless profile, `R^2/G`,
compactness-proxy budget, and maximum-occupied-spin slow-rotation budget makes
the global orientation risk arbitrarily small within the class of exactly
hard-supported odd-sector states. Here `J_max` is a uniform upper bound on
such support, not a dynamically generated cutoff. The same profile fixes the
distinct localization variables

```text
r_areal=R x_w sqrt(lambda),
s_proper=R asin[x_w sqrt(lambda)],
y_optical=R atanh[x_w sqrt(lambda)].                  (AL.6)
```

Under an additional isotropic rotational heat-flow premise, the time-dependent
floor is

```text
R_frame(T)>=3/4(1-e^(-2 gamma T))
             +e^(-2 gamma T)R_frame(0).               (AL.7)
```

The elimination algebra is exact conditional on the fixed profile, rigid
collective description, exact support premise, and two declared proxy budgets.
It is not an Einstein-Skyrme backreaction theorem. The authenticated sharp
replay now supplies total-mass interval
`[34.210839360783,65.274326899858]` and interior-inertia interval
`[21.149280505678,48.390985007421]`. Directed substitution gives continuous
capacity at most `353.623193055092`, `J_max=352`, physical spin at most `705/2`,
and `R_frame>=1.9689304688982673e-5`. Total mass includes the ideal shell;
inertia omits wall inertia. This remains a fixed-profile proxy-budget cutoff,
not a dynamically generated cutoff. Equation (AL.7) also requires the
still-open same-action finite-coupling derivation of `gamma`.

Artifacts: `docs/skyrmion_observer_capacity.md`,
`qgtoy/skyrmion_observer_capacity.py`,
`tests/test_skyrmion_observer_capacity.py`.

### Research Calculation AM: Centered Skyrmion Current Moments

For the centered hard-wall hedgehog, compression to the leading rigid-rotor
band gives the normalized soldered physical current

```text
ell_i^t(r,n)=[kappa(r)/I](delta_ij-n_i n_j)J_j,
int_Sigma dSigma_mu ell_i^mu=J_i.                       (AM.1)
```

Here `dSigma_mu ell_i^mu=r^2dr dOmega ell_i^t`; the proper-volume and
unit-normal lapse factors cancel.

In centered static-slice Riemann-normal coordinates
`xi^k=rho(r)n^k`, inversion symmetry gives the exact componentwise signed
operator dipole

```text
int_Sigma dSigma_mu xi^k ell_i^mu=0.                    (AM.2)
```

The signed second moment is

```text
int_Sigma dSigma_mu xi^k xi^l ell_i^mu
=<rho^2>_I[4delta_klJ_i-delta_kiJ_l-delta_liJ_k]/10,    (AM.3)
```

whose spatial trace is `<rho^2>_I J_i`. The absolute norm-weighted moments do
not vanish; on a spin-`L` sector,

```text
M1_abs<=(9pi/8)L<rho>_I,
M2_abs<=(9pi/8)L<rho^2>_I.                              (AM.4)
```

For the default worldtube,

```text
c_I=34.2662015525,
(e f_pi)^2<rho^2>_I=2.1902355498,
M1_abs<=4.9397264442L/(e f_pi),
M2_abs<=7.7409314019L/(e f_pi)^2.                       (AM.5)
```

Step halving changes the proper mean-square constant by less than `4e-11`.
For a collective Hamiltonian `h(J^2)`, the current (AM.1) is zero Bohr
frequency. The executable artifact assumes the standard leading Noether-current
compression and verifies its angular consequences and radial integrals; it is
not an independent derivation of that compression. Equations (AM.2)-(AM.5)
supply the centered matter input for the
dipole-cancelled Hessian branch of Theorem AF. They do not apply unchanged to
an accelerated off-center source: its `l=1` support deformation can break
inversion symmetry and regenerate the signed dipole. Vibrations, wall modes,
relativistic deformation, and a bare unsoldered isospin current remain outside
the theorem.

Artifacts: `docs/skyrmion_current_moments.md`,
`qgtoy/skyrmion_current_moments.py`,
`tests/test_skyrmion_current_moments.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-current-moments
```

### Research Calculation AN: Centered Radial Curvature And Finite-Pinning No-Go

Along the centered hard-Dirichlet family re-solved at each radius `a`, hold the
membrane tension fixed. Then

```text
E'(a)=4pi a^2[-p(a)+sigma K(a)],
K=2sqrt(N)/a-lambda a/sqrt(N),                          (AN.1)
```

so Young-Laplace balance proves stationarity. At equilibrium,

```text
E''(a)=4pi a^2[-p'(a)+sigma K'(a)],
K'=-2sqrt(N)/a^2-3lambda/sqrt(N)
   -lambda^2a^2/N^(3/2).                               (AN.2)
```

For the default `mu=1`, `lambda=0.0025`, `a=4` solution, centered finite
differences along the re-solved branch give

```text
E''=0.4399062320>0,
M_wall=4pi sigma a^2/N^(3/2)=0.4129339430,
omega_wall=sqrt(E''/M_wall)=1.0321427485.               (AN.3)
```

Halving the radius difference changes `E''` by less than `3e-5` relatively.
This is converged numerical evidence for positive curvature, and hence for a
local minimum along the declared adiabatic `l=0` family, conditional on the
shooting solution and finite-difference errors. It is not a validated-numerics
proof or a full coupled wall-profile spectrum.

For the smooth boundary energy

```text
E_pin=4pi kappa_pin a^2sqrt(N)(1-cos F_w),              (AN.4)
```

the Robin condition is

```text
N(a^2+8sin^2F_w)F'_w/4
+kappa_pin a^2sqrt(N)sin F_w=0.                         (AN.5)
```

Exact `B=1` requires `F_w=0`, after which finite stiffness also requires
`F'_w=0`; ODE uniqueness gives the trivial profile. Hence this simple finite
pinning potential cannot preserve exact unit baryon number for a nontrivial
source. At large stiffness,

```text
F_w=-sqrt(N)y/(4kappa_pin)+O(kappa_pin^-2),
1-B=N^(3/2)|y|^3/(96pi kappa_pin^3)+O(kappa_pin^-4),
E_soft-E_D=-pi a^2N^(3/2)y^2/(8kappa_pin)
           +O(kappa_pin^-2),                            (AN.6)
```

where `y=F'_D(a)`. An exact finite-stiffness completion needs boundary
topological degrees of freedom or a different mechanism. Nonspherical modes,
the fully coupled `l=0` kinetic problem, off-center anchoring, and gravitational
junction conditions remain open. In particular, the off-center Fermi
expansion contains an `l=1` acceleration traction, so translating the centered
solution is not a supported static configuration.

Artifacts: `docs/skyrmion_worldtube_stability.md`,
`qgtoy/skyrmion_worldtube_stability.py`,
`tests/test_skyrmion_worldtube_stability.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-worldtube-stability
```

### Research Calculation AO: Smooth-Worldtube ULE Localization Penalty

Let `a` be a total optical support radius and choose the radial seed

```text
b_A(y)=exp[1-1/(1-(2y/A)^2)] for 0<=y<A/2,
b_A(y)=0 otherwise,  A=a/R.                            (AO.1)
```

Normalize its spherical transform `F_A` by `F_A(0)=1` and convolve the seed
with its radial reflection. The resulting prefilter is nonnegative,
`C_c^infinity(H^3_R)`, supported in radius `a`, and has field-amplitude
multiplier `F_A(p)^2`. Hence

```text
j_A(w)=j_0(w)F_A(Rw)^4,                                (AO.2)
```

with exact KMS balance and unchanged zero-frequency rate. The principal square
root is `q=sqrt(j_0)F_A^2`, so transform zeros cause no cusp.

Analytic differentiation of the compact transform gives `F_A'` and `F_A''`.
Together with analytic derivatives of `sqrt(j_0)`, this yields numerical
Sobolev norms `Q_k=||q^(k)||_2`, `k=0,1,2`, without differentiating sampled
data. The optimized weighted-Sobolev bounds are

```text
G<=sqrt(2pi Q_0Q_1),
M_1<=sqrt(2pi Q_1Q_2).                                 (AO.3)
```

For `R=1`, `a=0.2`, the step- and window-converged values are

```text
(Q_0,Q_1,Q_2)=(26.6977477290,1.57849600683,0.176766804082),
(G_num,M_1,num)=(16.2723018013,1.32407331492).          (AO.4)
```

These replace the illustrative moment inputs in Research Calculation AH by a
named profile-specific numerical baseline. They are floating-point convergence
results with a declared margin, not interval-certified enclosures.

The exact integral profile is nevertheless rigorously controlled by a separate
closed-form envelope. Let `s=A/2` and write `F=H/p`, where
`H=D_A^-1 int_0^s b_A(y/s)sinh(y)sin(py)dy`. Twice integrating the three
half-interval transforms by parts, using their directly vanishing endpoint
data, gives `F,F',F''=O(p^-3)` with explicit constants. Using only the rational
relaxations `D_A>=s^3/36`,
`exp(s)<8/7`, `pi<22/7`, and `exp(2pi)>400`, the executable proves at the
default profile

```text
(Q_0,Q_1,Q_2)<=(3495.325453538189,
                 12944.154923952921,
                 71805.966340613957),
(G,M_1)<=(16863.898481372697,76435.381039140748).       (AO.4a)
```

These are conservative exact-profile upper enclosures with exact rational
endpoints, not estimates of the actual values. The finite Simpson transform is
used only on bounded frequency windows: as a literal finite sinc sum it has a
spurious `p^-1` tail and is never extrapolated to infinity. At `L=4096`, exact
evaluation of the symbolic cap formula with (AO.4a) is sufficient. The
executable's downward-guarded ordinary-float evaluations are approximately
`9.9769e-27` for residual `1/(4d)` and `1.1022e-28` for residual `1/(4d^2)`;
they are not directed interval endpoints. Tight directed interval quadrature
remains open.

In the small-support ultraviolet regime, rescaling `x=aw` gives

```text
Q_0=Theta(a^-2), Q_1=Theta(a^-1),
Q_2^2=[3/(64pi^2)]log(R/a)+O(1),
G_bar=Theta(a^-3/2),
M_1_bar=Theta(a^-1/2[log(R/a)]^1/4).                  (AO.5)
```

The long-time ULE coefficient is proportional to `G_bar^3M_1_bar`. Therefore
the sufficient coupling cap carries the additional localization law

```text
lambda_cap=Theta(a^(5/2)[log(R/a)]^-1/8).               (AO.6)
```

Three supports numerically resolve the logarithmic `Q_2` term, while the
comparison `a/R=0.2 -> 0.4` gives effective cap exponent `2.5254`. Equation
(AO.6) is a derived candidate tradeoff for
this sufficient ULE error-control route. It is not a necessary lower bound on
the exact dynamics or on other non-Markovian approximations.

The radial function is a pre-gradient kernel. The actual compact scalar test is
`D_(p,a)h`, with conformal external-source weight `N^-3D_(p,a)h`. Eternal
stationarity gives a bounded-cross-section infinite-time worldtube and supports
the KMS/ULE theorem. Compact switching gives a genuine spacetime test but
convolves the spectrum and requires a new transient reduced-dynamics theorem.
No local matter current or microcausal finite-body action is yet derived.

Artifacts: `docs/static_patch_smooth_worldtube_ule.md`,
`qgtoy/static_patch_smooth_worldtube_ule.py`,
`tests/test_static_patch_smooth_worldtube_ule.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-smooth-worldtube-ule
```

### Research Theorem AP: Matter-Derived Skyrmion Bath And Root Obstruction

Assume the standard leading centered rigid-Skyrmion current and the declared
Killing-time charge-flux interaction

```text
ell_i^t=[kappa(r)/I](delta_ij-n_i n_j)J_j.             (AP.1)
V(t)=g sum_i int_Sigma dSigma_mu ell_i^mu B_i
    =g sum_i int r^2 dr dOmega ell_i^t B_i.            (AP.1a)
```

Coupling (AP.1) to the acceleration-improved conformal pseudoscalar gradient and
integrating the angular projector gives the compact optical source

```text
f_j(X,Omega)=2 kappa(r) mathcal N^3 n_j/[I r],          (AP.2)
```

where `mathcal N=sqrt(1-r^2/R^2)`. Its exact `l=1` form factor is

```text
H_Sky(p)=3R^2/[(1+p^2)I_2]
 int kappa(r)[y coth(y)sinc(py)-cos(py)]dr,             (AP.3)
j_Sky(w)=j_0(w)H_Sky(R|w|)^2.                          (AP.4)
```

Thus the stationary spatial regulator is fixed by the existing matter current,
not chosen independently. It is positive at the spectral level and preserves
KMS balance. At zero frequency,

```text
H_Sky(0)=<3[artanh(z)-z]/z^3>_I
 =1+(3/5)<z^2>_I+(3/7)<z^4>_I+... >1                 (AP.5)
```

for every nonpoint positive centered inertia density. The default hard-wall
profile gives

```text
H_Sky(0)=1.003295544733,
j_Sky(0)/j_0(0)=1.006601950081.                        (AP.6)
```

This is a `0.660195%` curvature-induced zero-mode enhancement. The wall makes
the inertia density vanish quadratically, yielding an oscillatory `p^-5` form
factor and a UV-finite spectrum. Step refinement finds the first simple zero at

```text
p_star=275.00922037,  H_Sky'(p_star)=-1.4468e-9.       (AP.7)
```

Consequently the principal spectral factor
`sqrt(j_Sky)=sqrt(j_0)|H_Sky|` has a cusp. Conditional on the simple zero, it is
not in `H^2`; the `Q_2/M_1` Sobolev hypothesis of Research Calculation AH cannot
be imported to this matter-derived hard-wall spectrum. This excludes that
sufficient principal-root proof route, not Markovian approximation in general.

The theorem assumes the leading collective-current compression, a centered
rigid wall, no rotational wall current, a scalar `h(J^2)` Hamiltonian, and the
improved stationary pseudoscalar charge-flux coupling (AP.1a). Coupling instead
to the local density `u_mu ell_i^mu` introduces another lapse and is not covered.
The zero is step-converged numerical evidence. Off-center deformation,
switching, band-projection errors, wall modes, stress, lifetime, and gravity
remain open.

Artifacts: `docs/static_patch_skyrmion_bath.md`,
`qgtoy/static_patch_skyrmion_bath.py`, and
`tests/test_static_patch_skyrmion_bath.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-bath
```

### Research Theorem AQ: Scalar Signed-Factor Recovery Gate

For a scalar bath spectrum, replace the positive jump-correlator root by any
real factor `q` satisfying

```text
q(omega)^2=J(omega).                                   (AQ.1)
```

Then the inverse Fourier transform obeys `g(t)=g*(-t)`, and (AQ.1) gives the
same exact nonconjugated self-convolution used in the Nathan--Rudner proof.
If `int |g(t)|dt` and `int |t g(t)|dt` are finite, every subsequent scalar
error estimate repeats with those moments. This is a proof extension by direct
substitution, not an arbitrary complex-phase theorem: `|q|^2=J` alone is
insufficient, and an irregular sign choice need not have finite moments.

For the centered Skyrmion spectrum of Research Theorem AP, choose

```text
q_Sky(w)=sqrt(j_0(w)) H_Sky(R|w|).                     (AQ.2)
```

It is real, satisfies `q_Sky^2=j_Sky`, obeys the factor-level half-KMS relation,
and crosses every simple form-factor zero smoothly. Thus the cusp in AP is a
principal-root obstruction, not an intrinsic obstruction of the matter
spectrum. Centered rotational invariance gives the diagonal three-channel root
`q_ab=delta_ab q_Sky`.

For the fixed-irrep scalar `h(J^2)` sector, all `J_a` are zero-Bohr operators.
Since `H_Sky(0)>0`, the signed and principal factors give the same jump
amplitude. Their zero-Bohr Lamb shifts also agree because the coefficient uses
`q(w)^2=j(w)` and the summed operator is `J^2`, scalar on the irrep.

Analytic differentiation of the matter form factor and finite-window
quadrature give the step- and window-converged candidates

```text
(Q_0,Q_1,Q_2)=(62.2644668852,2.16015691289,0.168156611337),
(G_num,M_1,num)=(29.0705146786,1.51073940540).          (AQ.3)
```

At `L=4096`, these imply candidate caps `3.15e-20` and `3.48e-22` for the two
declared residual budgets. They are not global rigorous constants. The finite
trapezoid form factor is never extrapolated to infinity; a separate exact-
profile enclosure of `H,H',H''` is supplied by Research Theorem AR and proves
global `H^2` membership. AU.2 interval-certifies all six derivative-norm
inputs and the exact tail envelope; Research Theorem AR2 now supplies
conservative global moment constants. The much tighter values in (AQ.3) and
their coupling caps remain candidates. The theorem is scalar/diagonal and
zero-Bohr specific. Research Theorem AS controls a prescribed finite amplitude
ramp on the stationary plateau. Nonzero-Bohr bands, general matrix roots,
derivation of the ramp from the action, off-center deformation, stress, and
gravity remain open.

Artifacts: `docs/static_patch_skyrmion_signed_ule.md`,
`qgtoy/static_patch_skyrmion_signed_ule.py`, and
`tests/test_static_patch_skyrmion_signed_ule.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-signed-ule
```

### Research Theorem AR: Exact Continuum Signed-Factor Tail

Conditional on the exact nontrivial regular hard-wall branch specified in
Research Theorem AP, introduce the optical coordinate and weights

```text
x=tanh(y)/sqrt(lambda),  Y=atanh(sqrt(lambda)x_w),
W(y)=[rho_I(x(y))/x(y)^2]dx/dy,  A(y)=W(y)coth(y).    (AR.1)
```

Then the exact numerator in `H_Sky=C N/(1+p^2)` is

```text
N(p)=p^-1 int_0^Y A(y)sin(py)dy-int_0^Y W(y)cos(py)dy. (AR.2)
```

The regular origin expansion `F=pi-bx+cx^3+O(x^5)` and exact Dirichlet wall
data give

```text
W(y)=w_0 y^2+O(y^4),       A(y)=w_0 y+O(y^3),
W(y)=w_Y(Y-y)^2+O((Y-y)^3) at the wall,              (AR.3)
W''(Y)=4pi sigma^2 N_w^2(1+4N_w sigma^2)
       /(3lambda^(3/2))>0,
```

where `sigma=|F_x(x_w)|>0` and `N_w=1-lambda x_w^2`. The nonzero wall slope
follows from ODE uniqueness on the nontrivial branch; no derivative-sign claim
is needed because the coefficient depends on `sigma^2`.

For `m=0,1,2`, suppose finite upper bounds are available for

```text
M_m^W=||d_y^3(y^m W)||_1,  M_m^A=||d_y^3(y^m A)||_1. (AR.4)
```

The analytic profile ODE on the compact interior and the one-sided endpoint
expansions above imply that these six norms are finite for the exact solution.
Numerical upper enclosures are not needed for membership, only for explicit
constants.

Three integrations by parts on the half interval, retaining the wall boundary
term, give explicit coefficients `h_k` such that

```text
|H_Sky^(k)(p)| <= h_k p^-5,  p>=P>=1,  k=0,1,2.     (AR.5)
```

The coefficient formulas are implemented by
`skyrmion_sharp_form_factor_tail_envelope`. Moreover,

```text
H(p)  =C W''(Y)sin(pY)/p^5+o(p^-5),
H'(p) =C Y W''(Y)cos(pY)/p^5+o(p^-5),
H''(p)=-C Y^2 W''(Y)sin(pY)/p^5+o(p^-5).             (AR.6)
```

Thus the `p^-5` law is sharp, and all three derivatives have the same power
because differentiation acts on the wall phase. Combining (AR.5) with the
bare Bunch-Davies root bounds gives

```text
|q_Sky^(k)(p)|=O(p^-7/2),  k=0,1,2.                  (AR.7)
```

The negative tail is exponentially half-KMS suppressed; near zero both the
bare root and the even form factor are analytic; and the signed factor crosses
simple form-factor zeros smoothly. Therefore the exact signed factor in AQ.2
belongs globally to `H^2(R)`.

For the AU.1-certified default profile, AU.2 now gives the exact-rational global
upper bounds summarized by

```text
(M_0^W,M_1^W,M_2^W)
 <= (257768617.27020434,6946570.05661323,298269.008103853),
(M_0^A,M_1^A,M_2^A)
 <= (37317164258.63237,505644130.0063133,13919447.36624204). (AR.8)
```

The proof combines exact 43-cell positive-radius interval-jet sums with a
regular-origin Volterra-Lie and fourth-order interval-AD enclosure. The exact
ledger contains all six inputs, the AU.1 endpoint/prefactor data, and a non-null
tail envelope under one certificate identity. Its archive SHA256 is
`1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9`.

The authenticated AU.3b baseline now supplies profile-resolved global constants,
but its conservative joined AU.2 tail dominates the finite band and gives
weaker bounds than AU.3a. It therefore does not upgrade the smaller floating
AQ.3 candidates to rigorous global constants.
Zero-extending the hard-wall weight and invoking a whole-line `W^{3,1}` theorem
would be incorrect because its second derivative jumps.

Artifacts: `docs/static_patch_skyrmion_tail.md`,
`qgtoy/static_patch_skyrmion_tail.py`,
`qgtoy/validated_skyrmion_origin_derivatives.py`,
`qgtoy/validated_skyrmion_spectral_derivatives.py`,
`tests/test_static_patch_skyrmion_tail.py`, and
`experiments/skyrmion_au2_global_tail_exact_certificate.json`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-tail
```

### Research Theorem AR2: Directed Global Skyrmion Sobolev Bounds

For the AU.1/AU.2-certified profile, normalize the nonnegative inertia density
to a probability measure `dmu=rho_I dx/I`. With

```text
K(p,y)=y coth(y)sinc(py)-cos(py),
H(p)=3/(1+p^2) int K(p,y)/tanh(y)^2 dmu,              (AR2.1)
C_Y=(1-lambda x_w^2)^-1,  D_Y=4/3+Y^2/3,
```

the elementary `sinc` derivative inequalities give

```text
|B_0|<=C_Y(1+2p^2/3), |B_1|<=C_Y D_Y p,
|B_2|<=C_Y D_Y,                                      (AR2.2)
```

where `B_k=int partial_p^k K/tanh(y)^2 dmu`. Exact quotient and product rules,
the rational bare-root bounds on `p<=1` and `p>=1`, and the half-KMS relation
therefore give uniform rational bounds for `q,q',q''` on every frequency cell.
An upper sum with step `1/4` on `[0,128]`, joined to the AR tail recomputed at
`P=128`, proves

```text
(Q_0,Q_1,Q_2)<=(4296.7909080828495,
                 10146.945245040379,
                 35213.76234103636),
(G,M_1)<=(16554.53883053991,47391.58033605288).       (AR2.3)
```

The artifact stores exact rational endpoints and is linked to the AU.2 archive
SHA. These constants certify the global Sobolev inputs of the conditional ULE
residual theorem. They do not certify the floating candidates (AQ.3), exact
finite-coupling reduced dynamics, switching, projection, stress, lifetime, or
gravity. The finite-band proof intentionally discards profile-specific
oscillatory cancellation.

Artifacts: `docs/validated_skyrmion_au3.md`,
`qgtoy/validated_skyrmion_au3.py`,
`tests/test_validated_skyrmion_au3.py`, and
`experiments/skyrmion_au3_global_sobolev_exact_certificate.json`.

Representative command:

```bash
PYTHONPATH=. python3 experiments/skyrmion_au3_global_sobolev_audit.py
```

### Research Certificate AR3: Authenticated Profile-Resolved AU.3b Baseline

Replaying the authenticated Newton tube and normalized inertia measure on 43
positive-radius cells plus two regular-origin cells, then evaluating unit
frequency cells through `P=64` with deterministic ordered reduction, gives

```text
(Q_0,Q_1,Q_2)<=(17526.908441434396,
                 53893.63684872416,
                 242992.97071757397).                 (AR3.1)
```

The squared finite-band bounds are approximately
`(4.990764e5,5.333905e6,4.264636e8)`, whereas the joined AU.2 tail bounds are
`(3.066934e8,2.899190e9,5.861912e10)`. The tail supplies more than `99.2%` of
each global squared bound. Thus (AR3.1) authenticates the sharp radial pipeline
and locates its present overestimation, but it is weaker than (AR2.3) and is not
a physical obstruction.

The archive SHA256 is
`bc6cf2ea21f44c122001fcc3f7fa6cffb9983d4ec4e35591323aa2d29b25c529`.
It rehashes the AU.2 archive, the exact sharp snapshot, and all recorded source
dependencies. The attached centered prescribed-switch ULE uses dimensionless
normalization, supplies only coupling upper caps with zero lower bound, and
controls the ancilla-stable state operator norm. It does not prove physical
units, same-action dynamics, projective recovery transfer, stress, lifetime, or
gravity, and its formally nonempty interval is not a physical observer window.

Artifacts: `docs/validated_skyrmion_au3b.md`,
`qgtoy/validated_skyrmion_au3b.py`,
`qgtoy/validated_skyrmion_ule.py`,
`tests/test_validated_skyrmion_au3b.py`,
`tests/test_validated_skyrmion_ule.py`, and
`experiments/skyrmion_au3b_sharp_global_exact_certificate.json`.

### Research Theorem AS: Finite Switch-On And Burn-In For Regular Gaussian Baths

Work within the Nathan--Rudner regular Gaussian-bath framework, where the exact
reduced equation, Gaussian expansion, and operator-norm estimates used below are
defined. Let the interaction amplitude be `chi(t)` with `0<=chi<=1`, vanishing
before `t_0` and equal to one from `t_s` through readout. Assume factorization
of the whole system-memory state from the stationary bath before switch-on.
Define

```text
delta_chi(z)=1-chi(t_s-z),
T_chi=inf_{delta_chi(z)>0} z/delta_chi(z).             (AS.1)
```

Then `delta_chi(z)<=min(1,z/T_chi)`. A Lipschitz bound
`||dot chi||_infinity<=L_chi` gives `T_chi>=1/L_chi`, and a linear ramp of
duration `T_sw` has `T_chi=T_sw`.

Absorb the prescribed amplitude into the interaction-picture system operators,
`X_alpha^chi(t)=chi(t)X_alpha(t)`. Since their norms remain at most one, the
Nathan--Rudner Gaussian-bath Born, Markov, and exact speed estimates retain the
same constants. On the plateau the exact reduced equation can be written

```text
dot(rho)=[R+D_chi(t)]rho+xi,
||xi||_infinity<=Gamma^2 tau,
||dot(rho)||_infinity<=Gamma/2,                       (AS.2)
D_chi(t)=-int_{-infinity}^{t_s} ds
             [1-chi(s)]Delta(t,s),
||Delta(t,s)||_(infinity->infinity)
 <=4 gamma||J(t-s)||_1.                               (AS.3)
```

Thus no factorization is reimposed at the plateau. For
`t=t_s+B+r`, the inequality
`delta_chi(z)/(B+r+z)<=1/(B+r+T_chi)` and the exact moment relation
`Gamma_0 tau_0<=Gamma tau` give

```text
||D_chi(t_s+B+r)||_(infinity->infinity)
 <=Gamma tau/(B+r+T_chi).                             (AS.4)
```

For the stationary plateau dressing `M_t`, stationary Bloch-Redfield generator
`R`, and ULE generator `L`, the Appendix-C kernel identities and norm integrals
are

```text
dot(M_t)+R=L,
||M_t(A)||_infinity<=Gamma tau||A||_infinity,
||L(A)||_infinity<=(Gamma/2)||A||_infinity.           (AS.5)
```

Defining `rho'=(1+M_t)rho` and using (AS.2)-(AS.5) gives exactly

```text
dot(rho')=L rho'+eta,
eta=D_chi rho+xi+M_t dot(rho)+L(rho-rho'),
||eta(t_s+B+r)||_infinity
 <=2Gamma^2 tau+Gamma tau/(B+r+T_chi).                (AS.6)
```

The finite-history generator occurs once explicitly; its product with `M_t` is
already included in the bound on `M_t dot(rho)`. At both endpoints
`||rho'-rho||_infinity<=Gamma tau`. The zero-Bohr ULE is unital and contracts
the operator norm on Hermitian inputs, so Duhamel's formula yields

```text
||rho_exact(t_s+B+T)-E_T(rho_exact(t_s+B))||_infinity
 <=2 Gamma tau+2 Gamma^2 tau T
   +Gamma tau log(1+T/(B+T_chi)).                     (AS.7)
```

After adjoining an arbitrary inert memory, every system operator becomes
`X_alpha tensor I`; all norms and bath constants above are unchanged. Hence
(AS.7) is uniform over all system-memory density inputs factorized from the
fixed bath before switch-on. It is derived from that common initial time even
though the post-burn state is correlated with the bath. If

```text
B+T_chi >= beta/Gamma,                               (AS.8)
```

then

```text
epsilon_infinity(T)
 <=2 Gamma tau+(2+1/beta)Gamma^2 tau T.              (AS.9)
```

At collective heat time, (AS.9) replaces the coefficient `20736` by
`20736[1+1/(2beta)]`. Hence the sufficient schedules
`d^-7/2/sqrt(log d)` and `d^-4/sqrt(log d)` are unchanged. For `beta=10`, the
asymptotic coupling cap is multiplied by `1/sqrt(1.05)=0.975900...`.

For moment upper bounds `G<=G_bar`, the executable reports rather than assumes
the sufficient bound-level preparation age
`B+T_chi>=beta/Gamma_bar`, where
`Gamma_bar=144 lambda^2 L^2 G_bar^2/N^2`. This yields the same coefficient
because `(Gamma tau)_bar Gamma_bar=(Gamma^2 tau)_bar`; it is not evidence that
an unspecified physical burn-in has occurred. The executable constructs the
mathematical witness `B=beta/Gamma_bar`, `T_chi=0` and checks the original
logarithmic residual for both budgets. The corresponding required ages scale
as `Theta(d^3 log d)` and `Theta(d^4 log d)`; in both cases their ratio to heat
time is `Theta(1/[d^2 log d])`. Thus the coupling exponents survive, but the
preparation resource is an additional and potentially impractical cost.

A separately smooth switch-on, flat at the plateau, and a later smooth
switch-off may make `chi` compactly supported in time without affecting
pre-readout dynamics. A linear ramp is only Lipschitz and does not have this
corollary by itself. The theorem applies on the stationary plateau; it does not
compare ramp-time dynamics to a stationary semigroup. It is a direct adaptation
of Nathan--Rudner Eq. (13), Appendices A.3--A.6, Appendix B Eq. (B2), and
Appendix C.1--C.3, read with the 2021 erratum, not a theorem quoted verbatim.
It assumes a prescribed scalar amplitude switch, finite bath moments, a regular
zero-mean Gaussian reservoir, and zero-Bohr unital dynamics. It does not by
itself construct an unbounded-field propagator in an algebraic KMS
representation or justify regulator removal for a quasifree QFT bath. It also
does not derive the switch from the worldtube action or cover non-Gaussian,
nonzero-Bohr, stress, lifetime, or gravitational effects.

Artifacts: `docs/static_patch_finite_switching_ule.md`,
`qgtoy/static_patch_finite_switching_ule.py`, and
`tests/test_static_patch_finite_switching_ule.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-finite-switching-ule
```

### Research Result AS2: Conditional Rigid-Detector Box And Locality Stop

Fix the cutoff-one Peter-Weyl register

```text
R_1=(V_0 tensor V_0*) direct_sum (V_1 tensor V_1*),
dim R_1=10,                                               (AS2.1)
```

and an inert spin-one relational target. On optical `H^3_R`, let `h_A` be the
named compact convolution-square prefilter with zero-channel spherical
normalization and define

```text
Phi_a(h_A)=integral dmu_opt(y) h_A(y) P_a^b(y->0)B_b(y),
H_int(tau)=lambda chi_(B,T)(tau)
             sum_a J_left^a tensor Phi_a(h_A).           (AS2.2)
```

Here `chi_(B,T)(tau)=S(tau)S(B+T+2-tau)`, with
`S(u)=q(u)/[q(u)+q(1-u)]`, `q(u)=0` for `u<=0`, and
`q(u)=exp(-1/u)` otherwise. This is a smooth compact spatially smeared
rigid-detector EFT. The shared noncommuting `J_left^a` is not claimed to arise
from a microcausal local matter current.

Indeed, try to reinterpret the factorized current as a local distribution
`ell_a(x)=h_A(x)J_a^left`. Choose real smooth test functions `f,g` with disjoint
equal-time spatial supports inside an open set where `h_A` is nonzero, and with
`alpha_f=int f h_A dmu` and `alpha_g=int g h_A dmu` both nonzero. For distinct
components `a=1,b=2`,

```text
[ell_1(f),ell_2(g)]
 =i alpha_f alpha_g J_3^left !=0 on the V_1 block.      (AS2.3)
```

The test-function supports are spacelike separated, so (AS2.3) violates
microcausality. Thus the exact factorized rigid-current density cannot simply
be promoted to the local-matter class while retaining its exact-zero error
ledger. This is a route obstruction, not a no-go for a different local
completion with additional degrees of freedom.

Equation (AS2.3) is an unconditional algebraic obstruction for the literal
factorized density. The channel statements below are conditional. For the named
Bunch-Davies bath one must construct the compactly switched propagator in the
KMS GNS/Araki-Woods representation, establish regulator-uniform versions of the
Gaussian-bath estimates in AS, prove convergence of the finite-register reduced
maps, and pass the norm inequality to the limit. This QFT channel bridge is not
proved here.

Conditional on that bridge, define the reduced maps with the KMS-state slice.
Let `P_B` be the pre-switch-to-post-burn channel, `F_(B,T)` the reduced channel
from the same pre-switch input to the end of storage, and

```text
G_(B,T)=U_cov(T) o H_s(T) o P_B,
U_cov=U_free o U_LS.                                    (AS2.4)
```

The known free and Lamb Casimir unitaries are both retained. The common input
time is essential: no autonomous reduced channel on an arbitrary correlated
post-burn state is inferred.

If `V_g` is the register's left action and `W_g` rotates the bath, the radial
profile, central parallel transport, and contracted vector coupling make the
joint action invariant under `V_g tensor W_g`. The KMS bath state is
`W_g`-invariant. Conjugating the switched joint propagator and applying the KMS
slice therefore shows that `P_B` and `F_(B,T)` are `SO(3)`-covariant. The heat channel
is isotropic and both known Casimir unitaries commute with `V_g`. Hence the
post-burn encoded family remains a group orbit and `U_cov` leaves its optimal
relational risk unchanged.

Under the AS hypotheses, the uniform finite-switch estimate holds after
adjoining an inert memory. For
any Hermiticity-preserving trace-annihilating channel difference with input
dimension `D_in`, output dimension `D_out`, and uniform stabilized operator
residual `epsilon_infinity`, equality of the positive and negative spectral
sums gives

```text
(1/2)||Delta||_diamond
 <=floor(D_in D_out/2) epsilon_infinity.                (AS2.5)
```

For (AS2.1), the factor is `50`. With

```text
epsilon_infinity
 <=2c Gbar Mbar+2c^2 Gbar^3 Mbar T
   +c Gbar Mbar log[1+T/(B+T_chi)],
c=144 lambda^2,                                         (AS2.6)
Gbar=16863.898481372697,
Mbar=76435.38103914078,                                 (AS2.7)
```

there is an explicit conditional open parameter box

```text
1.278e-14 < lambda < 1.460e-14,
1.497e18 < B/R < 1.645e18,
1.031e30 < T/R < 1.100e30,                              (AS2.8)
```

whose heat exposure lies strictly inside `0.7<s<1` and on which

```text
(1/2)||F_(B,T)-G_(B,T)||_diamond <0.039.               (AS2.9)
```

In every bridged realization, the action commutes with `C_left`, so `P_B`
preserves the token's mean Casimir `9/5`. U7 and (AS2.8) then give the sufficient
record-failure threshold

```text
s>s_fail=0.6156552580594193.                            (AS2.10)
```

The whole box lies above this threshold. Using the weaker declared exposure
`s=0.7` and larger declared error `0.039`, an 80-digit decimal guard gives

```text
R_physical>=0.5327532814987301>1/2.                    (AS2.11)
```

The canonical token begins at exact risk `3/8`, so this is a conditional
finite-time degradation certificate on the declared box. It becomes a statement
about the named QFT detector only after the open channel bridge. It does not
exclude shorter exposures or kill the detector model. The very large times in
(AS2.8) make it a formal bound, not a practical detector construction.

The zero multipole and band terms are exact only for the factorized rigid-
detector action (AS2.2), and both known Casimir unitaries are included in
(AS2.4). A microcausal local-current completion would reopen those terms.

Status: **REGULAR-BATH CHANNEL BOX CONDITIONAL PASS; NAMED QFT CHANNEL BRIDGE
OPEN; EXACT FACTORIZED-CURRENT ROUTE INCONCLUSIVE STOP.** Paper U U8a remains
open. Token preparation and physical readout are U8b and remain open.
Persistence of the detector EFT through the finite protocol is assumed rather
than derived as a hardware-lifetime theorem. No gravitational functional,
`S_Ob` comparison, Paper R input, or full U8 claim is used.

Artifacts: `docs/u8a_finite_storage_channel.md`,
`qgtoy/u8a_finite_storage_channel.py`, and
`tests/test_u8a_finite_storage_channel.py`.

Representative commands:

```bash
PYTHONPATH=. python3 -m qgtoy u8a-finite-storage-channel
PYTHONPATH=. python3 -m pytest -q tests/test_u8a_finite_storage_channel.py
```

### Research Theorem AT: Off-Center Translation No-Go And Cross Spectrum

Let the centered effective optical vector source be `f_j(y,n)=F(y)n_j`, with
the center regularity `F(y)=c y+O(y^3)`. Under
an infinitesimal `H^3` transvection of rapidity `epsilon` along the unit vector
`a`,

```text
f_j^(epsilon)=f_j-epsilon a_i[u_0 delta_ij+u_2 Q_ij]+O(epsilon^2), (AT.1)
u_0=[F'+2coth(y)F]/3,
u_2=F'-coth(y)F,
Q_ij=n_i n_j-delta_ij/3.                              (AT.2)
```

Thus the old-origin harmonic expansion of the centered `l=1` source contains
only `l=0` and `l=2` at first order, with no `l=1` term.

For a genuine active optical translation with a parallel-transported center
frame, bath homogeneity and the scalar matter multiplier imply

```text
K_auto,ij(omega;q)
 =j_0(omega)H_Sky(R|omega|)^2 delta_ij.               (AT.3)
```

Consequently pure kinematic displacement cannot generate auto polarization
splitting at any order. Any such splitting diagnoses intrinsic held-off-center
matter/boundary response or broken parity/rotation symmetry, not translation.

For two identical translated sources at optical separation `y`, let

```text
phi_p(y)=sin(py)/[p sinh(y)],  p=R|omega|.             (AT.4)
```

Then the normalized parallel-transported cross eigenvalues are

```text
c_parallel=-3phi_p''/(1+p^2),
c_perp=-3phi_p'/[(1+p^2)sinh(y)].                     (AT.5)
```

The matter form factor multiplies auto and cross blocks equally and cancels
from (AT.5). Near coincidence,

```text
c_parallel=1-(3p^2+7)y^2/10+O(y^4),
c_perp=1-(p^2+4)y^2/10+O(y^4).                       (AT.6)
```

At a form-factor zero the physical auto and cross blocks both vanish, so a
normalized operational ratio is undefined even though (AT.5) remains a
geometric function.

The physical massive Skyrmion, membrane, static lapse, and holding anchor are
not invariant under optical transvections. Assume a parity-even nonrotating
held source, parity-odd vector smearing, the acceleration as the only new
vector, and an angular-momentum-diagonal recentered bath inner product. Its
first-order intrinsic response is then `A(y)a_j+B(y)(a dot n)n_j`, hence lies
in `l=0+2`; interference with the centered `l=1` source vanishes. Under these
assumptions the real symmetric auto splitting begins at quadratic order,

```text
K_ij=j_Sky delta_ij
 +eta^2[alpha_perp(delta_ij-a_i a_j)+alpha_parallel a_i a_j]+... . (AT.7)
```

The coefficients in (AT.7) require a coupled linearized `l=1` Skyrmion,
membrane, and anchor boundary-value problem and are not claimed here. An
old-origin translated dipole is orbital and must not be confused with an
intrinsic recentered current dipole. The executable audits the coordinate and
spectral formulas; the any-order auto-isotropy no-go is the analytic homogeneity
argument, not a numerical certificate. The floating spectral evaluator uses a
declared resolved-phase domain and raises outside it; the analytic formula is
not so restricted.

Artifacts: `docs/static_patch_skyrmion_offcenter.md`,
`qgtoy/static_patch_skyrmion_offcenter.py`, and
`tests/test_static_patch_skyrmion_offcenter.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-offcenter
```

### Research Infrastructure AU.0: Exact Rational Interval Foundation

The validated Skyrmion program cannot promote floating RK4 diagnostics by
wrapping them in binary nextafter bounds: Python does not specify directed
rounding for the required transcendental functions, and the singular origin
series needs an explicit remainder proof. The trusted foundation therefore
uses exact rational endpoints and analytic rational remainders.

The executable implements closed interval arithmetic together with

```text
pi = 16 atan(1/5)-4 atan(1/239),
Taylor enclosures for sin(x) and cos(x),
the positive atanh(x) series with a geometric tail bound,
exact-rational bisection for sqrt(x).                         (AU.0)
```

Analytic alternating-series, Taylor/Lagrange, geometric-tail, and bisection
arguments justify the enclosures. The executable checks nested refinement for
`pi` and `atanh(1/5)`, interval containment of `sin(x)^2+cos(x)^2=1`, and the
ordered nonnegative square-root bracket. These are consistency checks rather
than an independent proof of the remainder theorems. No floating
transcendental function enters the trusted module.

This subsection records the arithmetic foundation, not the later theorem
status. AU.1 subsequently closed the global residual, scalar Schur, Newton,
monotonicity, inertia, and wall-slope gates. AU.2 subsequently certified the six
derivative norms and continuum tail envelope. AU.3a subsequently joined a
directed rational finite-band sum to that tail and certified conservative
global `Q_0,Q_1,Q_2,G,M_1`. AU.3b subsequently authenticated the
profile-resolved pipeline and directed worldtube constants, while showing that
its current `P=64` joined tail is too conservative to improve AU.3a.

Artifacts: `docs/validated_skyrmion_interval_program.md`,
`qgtoy/validated_interval.py`, and `tests/test_validated_interval.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy validated-interval-foundation
```

### Research Infrastructure AU.0b: Conditional Nonlinear Picard Cell

Let `I_0` be a rational box of positive-radius initial data and `T` a rational
state tube on `[x_0,x_0+h]`. If exact interval evaluation of the curved
Skyrmion vector field gives

```text
I_0 + [0,h] f([x_0,x_0+h],T) subset interior(T),          (AU.0b)
```

then, for every exact initial point in `I_0`, the associated Picard operator
maps the closed convex set of continuous `T`-valued paths into its interior.
The operator is continuous and compact, so it has a fixed point. On the
checked box the radius, lapse, and nonlinear denominator are strictly positive;
the vector field is analytic and locally Lipschitz, making that fixed point
unique. Exact interval integration encloses its endpoint.

The packaged witness checks one `10^-6`-wide cell beginning at `x=0.1001`.
Its initial box is conditional input near the floating profile, not an output
of the certified uniform origin-family cutoff box. AU.0b therefore validates the
nonlinear checker logic but proves neither the default hard-wall profile nor a
shooting root.

Artifacts: `qgtoy/validated_skyrmion_profile.py` and
`tests/test_validated_skyrmion_profile.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy validated-skyrmion-profile-foundation
```

### Research Infrastructure AU.0e: IVP Wrapping And Global-BVP Route

An untrusted floating generator proposes rational cubic-Hermite cells, but the
trusted AU.0d checker recomputes and accepts every defect, Jacobian, self-map,
contraction, endpoint, and chain relation. With minimum step `1/2048`, both
point shooting endpoints validate from `x=1/16` through `x=1/4`. On the lower
endpoint run toward `x=1/2`, the last accepted cell ends at

```text
x=603/2048,
```

after which the minimum-step constant-radius self-map fails; the last declared
derivative radius is about `16.788`. This is a reproducible obstruction for the
implemented decorrelated interval-state representation, not a no-go theorem
for all validated IVP or Taylor-model methods.

The selected alternative exploits the exact self-adjoint linearization

```text
L eta=-(P eta')'+Q eta,
P=(1-x^2/400)(x^2+8 sin(F)^2).
```

For `z=x-33/16`, the rational positive comparison

```text
v=8/(z^2+4)
```

has the exact Barta quotient formula

```text
(L v)/v=Q+2z P'/(z^2+4)+P(8-6z^2)/(z^2+4)^2.          (AU.0e)
```

Floating exploration gives minimum `1.62749`, Dirichlet first eigenvalue
approximately `7.16556`, and augmented scalar Schur complement approximately
`2.95967`. These are feasibility margins only. AU.1 requires exact cellwise
validation of the weaker quotient bound `1`, the nonlinear residual, the Schur
interval, and a Newton radius.

Artifacts: `qgtoy/skyrmion_taylor_certificate_generator.py`,
`tests/test_skyrmion_taylor_certificate_generator.py`,
`experiments/skyrmion_global_bvp_probe.py`, and
`experiments/skyrmion_global_bvp_design.md`.

### Research Infrastructure AU.0f: Conditional Barta Checker And BVP Data

An untrusted generator constructs an exact-rational degree-five Hermite spline
`F_bar` on `[1/16,4]`. Consecutive cells agree exactly in `F_bar`, `F_bar'`,
and `F_bar''`; Bernstein conversion gives exact cellwise jet boxes. The
generator also evaluates the divergence-form nonlinear residual, the
origin-box and wall residuals, a central-difference shooting-sensitivity
proposal `Y_hat`, a fundamental proposal `K_hat`, and their exact rational
wall-Dirichlet combination `H_hat`. No generator field asserts proof status.

For any supplied positive-radius jet box, the trusted checker independently
recomputes

```text
P=N(x^2+8 sin(F)^2),
P'=N'(x^2+8 sin(F)^2)+N(2x+8 sin(2F)F'),
Q=partial_F B-(8N sin(2F)F')'.                         (AU.0f.1)
```

It then evaluates the exact rational witness quotient from AU.0e. On five
packaged independent boxes it proves `P>0` and

```text
(L v)/v >= 1.464502640726474651 > 1.                   (AU.0f.2)
```

The displayed number is rounded downward from an exact rational endpoint.
The packaged boxes are conditional inputs: they are not proved to cover a
full interval or to contain one common profile. AU.0f therefore verifies the
coefficient and Barta machinery but does not prove the hard-wall BVP,
coercivity of its linearization, a Schur bound, or a Newton radius.

A stronger trusted routine now accepts exact normalized-coordinate profile
polynomials, verifies exact interval coverage and all value/first/second
derivative joins, recomputes every jet, and adaptively bisects only unresolved
Barta boxes. On the complete representative 21-cell rational spline it accepts
207 leaf boxes, uses maximum extra depth five, and proves

```text
inf_I (L_Fbar v)/v > 1.502908 > 3/2.                   (AU.0f.3)
```

Thus the fixed witness works globally for that exact approximate spline. This
does not yet transfer coercivity to an unknown nonlinear solution ball.
Direct whole-cell nonlinear residual bounds are also too broad for Newton:
four exact centered subcells per default spline cell reduce about `15.74` to
`2.407`, while sixteen give about `0.526`. Subdivision alone is not the closing
mechanism; polynomial-level residual cancellation is still required.

Artifacts: `qgtoy/validated_skyrmion_bvp.py`,
`qgtoy/skyrmion_global_bvp_certificate_generator.py`,
`tests/test_validated_skyrmion_bvp.py`, and
`tests/test_skyrmion_global_bvp_certificate_generator.py`. The exact augmented
block inverse, graph-norm estimates, nonlinear second derivative, radii
polynomial, and physical sign tests are designed in
`experiments/skyrmion_augmented_bvp_newton_bounds.md`; that note is a rigorous
conditional blueprint, not an executed AU.1 certificate.

The generated shooting-sensitivity proposal `Y_hat` is not itself the Schur
auxiliary, because `Y_hat(4)` is approximately `-6.52421`. The corrected
candidate introduces `K_hat(a)=0,K_hat'(a)=1` and forms the exact rational
polynomial combination
`H_hat=Y_hat-[Y_hat(4)/K_hat(4)]K_hat`. Its raw candidate Schur interval is
`[2.95926150,2.96011432]`. Here `K(4)` is approximately `2.20434843` and the
exact rational combination coefficient is approximately `2.95969864`. A
theorem still requires the trusted derivative-trace image of the lifted
auxiliary residual to be subtracted from that raw interval.

A trusted conditional Schur checker now consumes only the exact rational
profile and auxiliary polynomials. It revalidates their common mesh and global
`C2` joins, requires exact wall zero, applies the interval affine lift that
matches `Phi_b` at the cutoff, independently reruns the Barta audit, recomputes
the lifted residual, derives the conservative graph-norm derivative bound, and
subtracts that residual image from the raw Schur interval. The representative
candidate is correctly rejected rather than promoted: independent-box
residual enclosures for `H_hat` decrease only from about `28.15` to `14.52` to
`9.43` and then `7.41` at 4, 8, 16, and 64 centered subcells per source cell. A
diagnostic combining
the certified `alpha>1.5029` margin with sampled coefficient scales gives an
elementary derivative constant about `674.5`, so that conservative route would
require a residual below about `4.4e-3`.
Subdivision alone is therefore not the closing mechanism. AU.1 now requires
polynomial-level cancellation in the complete Jacobi residual and an
independently validated Dirichlet trace representer.

The trusted residual layer now uses the exact five-harmonic identity

```text
x^2 A_F h = B_0+B_2 cos(2F)+B_4 cos(4F)
              +C_2 sin(2F)+B_1 cos(F),
```

where all five amplitudes are exact rational polynomials on each centered
subcell. It combines those amplitudes with rational-center Taylor models before
one final range operation and adds explicit Lagrange tails afterward. Exact
vacuum-polynomial and dense direct-formula containment tests pass. This removes
the artificial independent `P,P',Q,h,h',h''` dependency, but it also exposes a
real approximation defect: direct assembled evaluation of the first coarse
`[1/16,1/4]` auxiliary cell reaches about `6.92765`.

The untrusted generator therefore now accepts an explicit exact rational graded
mesh, shared by `F_hat,Y_hat,K_hat,H_hat`, while retaining the historical
uniform default. Refining with widths `1/128`, `1/64`, and `1/32` on the three
successive near-origin bands gives a sampled assembled auxiliary residual about
`5.79e-4`; this is feasibility evidence rather than the trusted residual quoted
below.

The independent trace-representer checker is now implemented. It requires an
exact rational globally `C2` spline `kappa_hat` with
`kappa_hat(a)=1,kappa_hat(c)=0`, reruns Barta on the same profile operator,
recomputes `A kappa_hat` with the five-harmonic residual, bounds the approximate
`L1` norm by exact sign-certified integration where possible, and applies only
the independently available `C0` resolvent estimate to the residual error. It
then verifies

```text
C_tau <= [||kappa_hat||_1+(c-a) C0 ||A kappa_hat||_infinity]/P(a).
```

Synthetic exact-rational pass and rejection tests close the checker logic. No
Schur input is used in this representer proof.

On the 43-cell exact graded candidate, the trusted audit proves a same-operator
Barta lower bound greater than `1.0235900944571767` on 139 accepted leaves,
with maximum refinement depth four. All 43 representer cells have fixed sign
for exact `L1` integration. The recomputed bounds are

```text
||kappa_hat||_1 <= 0.1055378219793721,
||A kappa_hat||_infinity <= 0.08913332184493121,
representer L1 correction <= 0.7019249095288332,
C_tau <= 9.895351050897547.
```

The worst residual cell is the first graded cell `[1/16,9/128]`. A composed
trusted checker now certifies the representer first using only Barta and `C0`,
then uses its recomputed `C_tau` to correct the lifted auxiliary Schur interval.
Synthetic pass and rejection tests verify this noncircular ordering. Applying
that checker to the physical graded auxiliary certifies the declared corrected
Schur margin. The recomputed raw interval is
`[2.9592592352087594,2.9601147691072494]`, the lifted residual is at most
`0.005843528112861022`, and the trace correction is at most
`0.05782376205254868`, giving the certified corrected interval
`[2.9014354731562104,3.017938531159798]`. These operator audits are inputs to,
but are not by themselves, the nonlinear theorem below.

The nonlinear residual now has its own cancellation-preserving five-harmonic
checker. It folds the exact rational midpoint endpoint correction into the
profile and bounds the remaining origin-value interval through the Jacobi
derivative over the complete affine family. On the 43-cell physical candidate
it proves

```text
||G(F_bar)||_infinity <= 0.002295967024672295,
F_bar'(a)-Gamma(b_bar)
  in [-0.000023462001836132805,0.00001633679528688307].
```

The worst residual cell is `[2,2.1875]`, not the near-origin graded band. These
are the trusted Newton forcing terms.

### Research Theorem AU.1: Validated Hard-Wall Skyrmion Profile

For the prescribed dimensionless massive Skyrmion equation with

```text
mu^2=1, lambda=1/400, F(0)=pi, F(4)=0,
```

the exact-rational 43-cell certificate, regular origin family, Barta/Green
inverse bounds, nonzero augmented Schur complement, endpoint correction, and
Newton tube prove a nonlinear solution near the rational spline center. In the
augmented norm with `omega=3/4`, the radius `r=1/250` satisfies

```text
Y        <= 0.002296,
Z0       <= 0.000078,
Z2       <= 78.733,
p(r)     < -0.00107,
Z0+Z2 r  < 0.31501.                                  (AU.1.1)
```

The trusted tube uses analytic Taylor/Lagrange trigonometric remainders and
fixed-grid rational outward rounding with denominator `10^18`; no floating
quantity is a theorem premise. The self-map and contraction inequalities in
(AU.1.1) give existence and uniqueness within the certified Newton ball. The
same ball proves

```text
F'(x)<0 on (0,4],
F'(4) in [-0.09465,-0.08746],
I_rot in [21.149,48.921].                              (AU.1.2)
```

Thus the solution is strictly decreasing, has strictly negative wall slope,
and has finite positive dimensionless rotor inertia. The theorem asserts only
local uniqueness in the displayed Newton neighborhood for this fixed
background and hard boundary. It does not assert global uniqueness,
Einstein-Skyrme backreaction, stability under arbitrary boundary dynamics, or
a de Sitter observer-algebra theorem.

Exact rational archive:
`experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json`,
with SHA-256
`c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff`.
The compact audit summary is
`experiments/skyrmion_newton_reduced_hessian_rounded_audit_result.json`.
The exact checker is
`experiments/skyrmion_newton_linearization_audit.py`; focused regression tests
are in `tests/test_validated_skyrmion_bvp.py` and
`tests/test_skyrmion_newton_linearization_audit.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy validated-skyrmion-barta-foundation
```

### Research Infrastructure AU.0c: Uniform Origin-Family Contraction

Set `t=x^2`, `pi-F=xu(t)`, and `p=d(pi-F)/dx`. With

```text
S(w)=sin(sqrt(w))/sqrt(w),
C(w)=sin(2sqrt(w))/(2sqrt(w)),
a=u S(tu^2),
E=(1-kappa t)(1+8a^2),
Q=2u C(tu^2)[1+4a^2+4(1-kappa t)p^2]-mu^2 t a,
```

the singular profile equation is equivalent to the Volterra fixed-point map

```text
Tp(t)=E(t)^-1 integral_0^1 xi Q(t xi^2) dxi.             (AU.0c.1)
```

For every real slope `b` in the rational interval
`[1.579953,1.579954]`, exact Taylor models verify on `0<=x<=1/16` that the
parameter-dependent ball

```text
|p(t)-(b-3c(b)t)| <= (13/10)t^2
```

is mapped into itself with one uniform contraction constant below one. Formal
rational-function arithmetic in `b` proves the exact constant and cubic-center
identities before the `t^2` remainder is enclosed. Banach's theorem therefore
gives one fixed point in every fiber, and the parameterized contraction theorem
gives continuous slope dependence. Each fixed point reconstructs a regular
solution satisfying

```text
|F-(pi-bx+c(b)x^3)| <= (13/50)x^5,
|F'-(-b+3c(b)x^2)| <= (13/10)x^4.                       (AU.0c.2)
```

The common cutoff box is evaluated directly over the full slope interval, not
formed from endpoint hulls. This result does not prove unrestricted uniqueness,
positive-radius wall propagation, or a shooting root.

For a fixed rational slope, a second exact Taylor model retains the quintic
coefficient in `F=pi-bx+c(b)x^3+d(b)x^5+O(x^7)` and validates

```text
|p-(b-3c t-5d t^2)| <= (13/10)t^3,
|u-(b-c t-d t^2)| <= (13/70)t^3.                       (AU.0c.2q)
```

The checker proves this point ball lies inside the cubic fiber using
`5|d|+(13/10)a^2 < 13/10` and
`|d|+(13/70)a^2 < 13/50`, with matching slope, cutoff, mass, and curvature.
Uniqueness in the cubic ball therefore identifies the quintic point solution
with the branch differentiated below. At `a=1/16`, its cutoff errors are
`(13/70)a^7` for `F` and `(13/10)a^6` for `F'`.

Differentiating the translated Volterra contraction at fixed remainder gives a
uniform partial-parameter bound `M`. If `q<1` is the AU.0c contraction constant,
the fixed-point sensitivity obeys

```text
||d r_b/db|| <= M/(1-q).                                (AU.0c.3)
```

Exact interval automatic differentiation, including differentiated entire-
kernel tails, therefore proves `C1` slope dependence and encloses

```text
dF_b(1/16)/db  in [-0.06244243,-0.06243179],
dF'_b(1/16)/db in [-0.99740679,-0.99655545].             (AU.0c.4)
```

The decimals display exact rational interval endpoints approximately; the
checker does not finite-difference point solutions.

Differentiating the translated contraction a second time gives

```text
(I-T_r)r_bb=T_bb+2T_br r_b+T_rr[r_b,r_b].              (AU.0c.5)
```

Exact second-order interval AD evaluates the forcing on the common first-
sensitivity ball and applies the same resolvent factor `(1-q)^-1`. It proves
`C2` slope dependence and the cutoff enclosures

```text
d2F_b(1/16)/db2  in [-0.00013757,0.00029385],
d2F'_b(1/16)/db2 in [-0.01350569,0.02100685].           (AU.0c.6)
```

The intervals need not have a fixed sign; their role is to bound the nonlinear
origin lift in the augmented Newton radii polynomial.

Artifacts: `qgtoy/validated_skyrmion_origin.py` and
`tests/test_validated_skyrmion_origin.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy validated-skyrmion-origin
```

### Research Infrastructure AU.0d: Conditional Taylor Track

On a positive-radius cell `x=a+hs`, let the untrusted center be a rational
polynomial `F_0=P(s)`, `G_0=P_s/h`. The trusted checker recomputes

```text
delta = sup |P_ss/h^2-Phi(x,P,P_s/h)|,
m_F = sup |partial_F Phi|,
m_G = sup |partial_G Phi|
```

on exact interval tubes. For initial center errors `e_F,e_G` and correction
radii `r_F,r_G`, it accepts only if

```text
e_F+h r_G <= r_F,
e_G+h[delta+m_F r_F+m_G r_G] <= r_G,                    (AU.0d.1)
max(h r_G/r_F, h[m_F r_F+m_G r_G]/r_G) < 1,             (AU.0d.2)
```

with the zero-radius rows interpreted only when their numerators vanish. These
are the componentwise self-map and weighted sup-norm contraction inequalities
for the correction integral equation. The checker chains the smaller
checker-computed self-map images at the cell endpoint rather than the declared
candidate radii; no certificate-supplied defect, Jacobian, endpoint, or status
is trusted.

The packaged witness validates two nonlinear microcells beginning at
`x=0.1001`. It is not connected to AU.0c, does not enclose every shooting
slope, and does not reach the wall.

Artifacts: `qgtoy/validated_skyrmion_profile.py` and
`tests/test_validated_skyrmion_profile.py`.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy validated-skyrmion-profile-foundation
```

Representative commands:

```bash
PYTHONPATH=. python3 -m qgtoy fuzzy-berezin-refinement --max-source-level 5
PYTHONPATH=. python3 -m qgtoy fuzzy-algebra-inference --max-level 6
PYTHONPATH=. python3 -m qgtoy relational-observer-constraint --max-level 8
PYTHONPATH=. python3 -m qgtoy edge-symmetry-robustness --max-level 8
PYTHONPATH=. python3 -m qgtoy core-edge-obstruction --max-level 8
PYTHONPATH=. python3 -m qgtoy interacting-kms-edge --max-level 8
PYTHONPATH=. python3 -m qgtoy charged-reference-recovery --max-level 8
PYTHONPATH=. python3 -m qgtoy operational-phase-reference --max-level 8
PYTHONPATH=. python3 -m qgtoy su2-directional-reference-no-go --max-system-spin 8
PYTHONPATH=. python3 -m qgtoy operational-su2-reference --max-system-spin 6
PYTHONPATH=. python3 -m qgtoy geometric-thermal-type-no-go --max-cutoff 24
PYTHONPATH=. python3 -m qgtoy modular-manybody-regulator --max-sites 10
```

## Basic Finite Model

At cutoff `L`, the packaged static-patch model compares:

- quantum observer algebra: `A_L = M_N`;
- diagonal screen algebra: `S_L = C^N`;
- dephased control algebra: `D_L = C^N`;
- screen map: diagonal restriction or dephasing;
- intrinsic operator-response probes: off-diagonal matrix units, commutators,
  relative/operator response, and finite generator covariance data.

The finite screen-shadow class used in the package consists of diagnostics that
factor through the diagonal screen algebra or through bounded low-order
screen-restricted transfer data. In formulas, a screen-visible diagnostic is any
declared functional of `E_diag(rho)`, diagonal correlators, finite
horizon-overlap counts, and low-order screen-restricted transfer records. It is
not allowed to query off-diagonal matrix units or commutators directly.

This is a deliberately finite benchmark definition, not a canonical continuum
definition of a gravitational screen.

## Exact Finite Claims

### Theorem 1: Screen-Shadow Collision

There are finite static-patch benchmark pairs whose screen-visible diagnostics
agree while the recoverable algebra differs as `M_N` versus `C^N`.

Status: exact finite theorem/certificate stack plus bounded regulator checks.

Primary artifacts:

- `docs/goals24_31_static_patch_bridge_theorem_note.md`
- `paper/main.md`
- `docs/goals24_31_static_patch_bridge_certificate_index.json`
- `qgtoy/conditional_ds_er_epr.py`
- `qgtoy/static_patch_testbed.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy conditional-ds-er-epr --max-cutoff 5 --screen-probability 0.75 --low-order 2
```

### Proposition 2: Finite Regulator Dynamics Preserve the Split

The finite Schur/random-unitary regulator channels preserve the declared
screen shadow while retaining the audited quantum/off-diagonal response in the
matrix-algebra model.

Status: finite theorem plus bounded regulator-class certificate stack.

Primary artifacts:

- `paper/main.md`
- `docs/goal26_derived_static_patch_dynamics_note.md`
- `docs/goal27_static_patch_regulator_universality_note.md`
- `docs/goal26_derived_static_patch_dynamics_certificate_index.json`
- `docs/goal27_static_patch_regulator_universality_certificate_index.json`
- `qgtoy/derived_static_patch_dynamics.py`
- `qgtoy/static_patch_regulator_universality.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-regulator-universality --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

### Theorem 3: Strong-Continuity Gate

Let `Lambda_L(delta)=exp(delta G_L)` be an identity-starting finite semigroup
with `||G_L|| <= Gamma_L`. If the cutoff lapse satisfies
`delta_L Gamma_L -> 0`, then

```text
||Lambda_L(delta_L)-id|| <= exp(delta_L Gamma_L)-1 -> 0.
```

This finite condition rules out instantaneous dephasing routes such as
stationary modular twirling, without assuming off-diagonal survival as an
axiom.

Status: finite semigroup theorem gate.

Primary artifacts:

- `docs/goal31_static_patch_strong_continuity_note.md`
- `docs/goal31_static_patch_strong_continuity_certificate_index.json`
- `qgtoy/static_patch_strong_continuity.py`
- `tests/test_static_patch_strong_continuity.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

### Proposition 4: Cofinal Full-Matrix Inclusion Scaffold

Consecutive spherical cutoffs `N_L=(L+1)^2` do not admit exact unital
trace-preserving full-matrix inclusions `M_{N_L} -> M_{N_{L+1}}` for `L >= 1`,
because `N_L` does not divide `N_{L+1}`.

The cofinal factorial subsequence

```text
L_k=(k+1)!-1,    N_k=((k+1)!)^2
```

does admit trace-preserving inclusions by amplification. The corresponding UHF
inductive limit has tracial GNS closure equal to the hyperfinite Type `II_1`
factor under the standard UHF trace-closure theorem. The dephased diagonal
control has the same levelwise screen shadows but an abelian von Neumann limit.

Status: finite construction plus standard operator-algebra theorem, conditional
on the chosen cofinal inclusion.

Primary artifacts:

- `docs/major_goal_finite_to_typeii_static_patch_observer_algebra_note.md`
- `docs/major_goal_finite_to_typeii_static_patch_observer_algebra_certificate_index.json`
- `qgtoy/typeii_static_patch_limit.py`
- `tests/test_typeii_static_patch_limit.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

## Bounded Certificate Evidence

### Certificate Audit A: Inclusion-Covariant Dynamics

Exact finite covariance fails for the raw fuzzy-sphere Hamiltonians under the
rank-ordered block embedding. The conditional-expectation version,

```text
E_k G_{k+1} iota_k(x) ~= G_k(x),
```

has decreasing bounded errors along the factorial subsequence in the current
certificate. The heat/Lindblad and short-time semigroup covariance bounds also
decrease across the audited levels. The dephased diagonal screen dynamics is
exactly inclusion-covariant and abelian.

Status: bounded asymptotic theorem/no-go audit, not a completed continuum
dynamics theorem.

Primary artifacts:

- `docs/inclusion_covariant_static_patch_dynamics_note.md`
- `docs/inclusion_covariant_static_patch_dynamics_certificate_index.json`
- `qgtoy/inclusion_covariant_dynamics.py`
- `tests/test_inclusion_covariant_dynamics.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

### Proposition 5: Consecutive Cutoff Refinement Audit

Exact unital full-matrix inclusions are too rigid for consecutive spherical
cutoffs. The baseline replacement is the trace-filled map. For any `n <= m`,

```text
Phi(A)=V A V^* + tau_n(A)(I_m - V V^*)
```

is unital, completely positive, and normalized-trace preserving. For the
matrix-unit witness `A=e_12`, `B=e_21`,

```text
||Phi(AB)-Phi(A)Phi(B)|| = 1/n.
```

For static-patch dimensions `n=(L+1)^2`, this error tends to zero while the
off-diagonal commutator witness remains visible in the quantum corner.

The `1/n` statement concerns the selected matrix-unit pair only. It is not a
uniform approximate-homomorphism bound: for even `n<m`, the balanced-sign
unitary `A=diag(I_{n/2},-I_{n/2})` gives

```text
||Phi(A^2)-Phi(A)^2|| = 1.
```

Accordingly, this map is a finite witness-preserving refinement, not an
asymptotic morphism of the full matrix algebra.

The current audit also compares harmonic mode-label refinement, heat-kernel
Schur coarse graining, and a Berezin-Toeplitz-inspired smoothing surrogate.
They preserve or converge on declared screen shadows and retain off-diagonal
response witnesses, but none is claimed to be canonical.

Status: finite physically motivated cutoff-refinement audit, not a canonical
continuum embedding theorem.

Primary artifacts:

- `docs/canonical_embedding_program.md`
- `docs/static_patch_embedding_channels_certificate_index.json`
- `qgtoy/embedding_channels.py`
- `tests/test_embedding_channels.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-embedding-channels --max-cutoff 5
```

### Theorem 6: Conditional Continuum Lift Obstruction

Suppose finite regulator sequences satisfy explicit lift conditions:
embedding/coarse-graining maps, trace/state convergence, screen-shadow
convergence, strong-continuity or generator control, response-witness
persistence, and observer-algebra limit compatibility. If two sequences have
identical limiting screen shadows but a nonzero limiting response gap, then no
dictionary that factors only through screen-shadow data can determine the
observer algebra.

Status: conditional theorem; the conditions are explicit lift assumptions, not
continuum claims.

Primary artifacts:

- `docs/continuum_lift_conditions.md`
- `docs/continuum_lift_obstruction_certificate_index.json`
- `qgtoy/continuum_lift.py`
- `tests/test_continuum_lift_obstruction.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5
```

## Conditional Assumptions

The packaged Type-II/static-patch interpretation depends on:

- the cofinal factorial cutoff subsequence;
- the standard UHF trace-closure theorem;
- the physical interpretation of the finite matrix inclusions as cutoff
  refinement;
- the `rank_ordered_static_patch_embedding` used in the current dynamics audit.
- the choice between exact cofinal inclusions and approximate consecutive UCP
  refinement maps.

The main open question is whether a more canonical inclusion or conditional
expectation should come from angular-momentum branching, Berezin-Toeplitz
refinement, heat-kernel coarse graining, continuum `L^2(S^2)` projections, or
approximate embeddings.

## Not Claimed

The following are deliberately not claimed:

- a continuum de Sitter observer-algebra theorem;
- a dS/CFT dictionary;
- literal ER=EPR in de Sitter;
- novelty of standard stabilizer/OAQEC, Schur-channel, UHF, or Type `II_1`
  background facts;
- canonical status of the factorial cutoff subsequence.

## Reviewer Reproduction

Run the focused package regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics
PYTHONPATH=. python3 -m unittest tests.test_embedding_channels tests.test_continuum_lift_obstruction
```

Run the compact example script:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

### Research Theorem AV: Spacelike SO(3) Replication Leakage

Let `P` be a finite-rank orthogonal projector, `Q=I-P`, and let the code
`P H` carry an integer-spin `SO(3)` representation with generators `J_a` and
largest spin `J`. For bounded microscopic operators `A,B`,

```text
[PAP,PBP]=P[A,B]P+PBQAP-PAQBP.                        (AV.1)
```

Thus, for self-adjoint `A,B`, locality defect
`delta=||P[A,B]P||`, and leakages
`lambda_A=||QAP||`, `lambda_B=||QBP||`,

```text
||[PAP,PBP]||<=delta+2 lambda_A lambda_B.              (AV.2)
```

If `PAP` and `PBP` approximate `alpha J_a` and `beta J_b`, for real gains
`alpha,beta`, with uniform operator errors `epsilon_A,epsilon_B`, then for
distinct Cartesian components

```text
|alpha beta| J
 <=delta+2 lambda_A lambda_B
   +2J(|beta|epsilon_A+|alpha|epsilon_B)
   +2epsilon_Aepsilon_B.                               (AV.3)
```

The factor two is optimal. It is asymptotically saturated by disjoint
gain-normalized block-spin observables in the symmetric ground band of an
even-site frustration-free ferromagnetic chain.

The complementary state-weighted specialization is as follows. Let
`O -> A(O)` be a local net, choose three pairwise spacelike regions `O_a`, and
let `A_a in A(O_a)` be bounded self-adjoint observables. Equivalently, the
algebraic theorem only requires three pairwise commuting bounded star-algebras.
For real `alpha`, define `lambda_*=max_a ||Q A_a P||` and assume

```text
P A_a P=alpha J_a,
lambda_*<=Lambda,              0<Lambda<=M,
||A_a||<=M.                                            (AV.4)
```

For every code state `rho=P rho P`, define

```text
p_a(rho)=Tr[rho P A_a Q A_a P].                        (AV.5)
```

The Hilbert-Schmidt form of (AV.1), followed by cyclic summation, gives

```text
sum_a p_a(rho)>=alpha^4 Tr(rho J^2)/(4Lambda^2)
                >=alpha^4 Tr(rho J^2)/(4M^2).          (AV.6)
```

Here `Lambda` must be an independently certified off-code amplitude cap; it
is not a free parameter. Since `sum_a p_a<=3Lambda^2`, the same theorem gives

```text
Lambda^4>=alpha^4 Tr(rho J^2)/12.                      (AV.7)
```

If each microscopic commutator has code norm at most `delta` and every
compressed action has error at most `epsilon`, set

```text
eta=4|alpha|J epsilon+2epsilon^2,
d=delta+eta.
```

Then every `t>0` gives the robust version

```text
sum_a p_a(rho)
 >=[alpha^4 Tr(rho J^2)-3(1+1/t)d^2]_+
   /[4(1+t)Lambda^2].                                  (AV.8)
```

Combining the exact theorem with Research Theorem W3,
`R_ref>=1/[16 Tr(rho J^2)+8]`, proves, for `0<r<1/8`, the operational
necessity

```text
R_ref<=r
 => sum_a p_a(rho)
    >=alpha^4[r^(-1)-8]_+/(64Lambda^2),
    Lambda^4>=alpha^4[r^(-1)-8]_+/192.                (AV.9)
```

The robust operational form replaces the exact numerator by

```text
N_r=[alpha^4[r^(-1)-8]_+/16-3(1+1/t)d^2]_+,
```

and gives `sum_a p_a>=N_r/[4(1+t)Lambda^2]` and
`Lambda^4>=N_r/[12(1+t)]`.

Equations (AV.6)-(AV.9) concern replication of different components of one
rigid collective mode across distinct spacelike cells. They do not require
different non-Abelian current components inside one region to commute and are
not a no-go for local non-Abelian currents. The gain `alpha` and norm `M` must
be fixed physical calibration data. Relative leakage can vanish at large spin.
No unbounded AQFT-current extension, transition rate, lifetime, gravity,
Skyrmion, or Paper U result is claimed.

The two-block disjoint ferromagnetic model makes the coefficient two in
(AV.2) asymptotically optimal. A three-equal-block version has
`sum_a p_a=N` and an actual-to-(AV.6) ratio tending to eight, so it realizes
the main theorem's scaling within a constant factor; it does not prove the
factor four optimal. Block diameters grow with `N`, and the ferromagnetic
parent is not uniformly gapped, so these are disjoint-region realizations, not
uniformly localized apparatuses.

The compression identity (AV.1) is standard Toeplitz/QEC machinery. More
decisively, Janssens' CP-map covariance Cauchy-Schwarz lemma gives the
state-weighted pair inequality when `T(X)=W*XW`; cyclic summation gives
(AV.6). The result is retained as a tested methods lemma, not claimed as a
standalone paper contribution. The exact priority reduction is recorded in
the audit below.

Artifacts: `docs/spacelike_replication_leakage_theorem.md`,
`docs/spacelike_replication_novelty_audit.md`,
`docs/spacelike_replication_qec_reduction_audit.md`,
`docs/spacelike_replication_goal_audit.md`,
`paper/spacelike_replication_paper_outline.md`,
`paper/spacelike_replication/main.tex`,
`paper/spacelike_replication/references.bib`,
`qgtoy/locality_reference_leakage.py`, and
`tests/test_locality_reference_leakage.py`,
`tests/test_global_so3_reference_risk.py`, and
`tests/test_spacelike_replication_manuscript.py`.

Representative commands:

```bash
PYTHONPATH=. python -m qgtoy locality-reference-leakage
PYTHONPATH=. python -m pytest -q \
  tests/test_locality_reference_leakage.py \
  tests/test_global_so3_reference_risk.py \
  tests/test_spacelike_replication_manuscript.py
```
