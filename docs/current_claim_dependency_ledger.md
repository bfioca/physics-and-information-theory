# Current Claim Dependency Ledger

Status: living claim audit through the current Track A/Track B milestones

This ledger records what each packaged claim actually depends on and what must
replace those dependencies before it can support a paper-worthy physics result.

## Screen-Shadow Collision

Current statement: `M_N` and `C^N` agree on declared screen data and differ in
operator response.

Dependencies:

- screen diagnostics are defined to factor through diagonal expectation data;
- the models are matched after dephasing;
- the separating witness is an off-diagonal commutator.

Evidence: exact elementary finite-dimensional algebra, supplemented by records
whose screen-match fields are often declared directly.

Replacement gate: define the screen observable system from a physical model and
prove an approximate operational statement

```text
d_screen <= epsilon_L,    delta_response >= delta_0 > 0.
```

## Schur And Random-Unitary Dynamics

Current statement: selected Schur or random-unitary channels preserve the
diagonal shadow while retaining an off-diagonal witness.

Dependencies:

- diagonal screen algebra;
- chosen kernel, noise law, energy spectrum, and cutoff scaling;
- selected response probes.

Evidence: a mixture of analytic formulas, actual finite coefficient matrices
and Cholesky PSD checks, and declarative certificate metadata.

Replacement gate: derive the channel or generator from the chosen Phase 1
model, then prove its fixed algebra, symmetry, response, and perturbative
stability.

## Strong-Continuity Gate

Current statement:

```text
||exp(delta_L G_L)-I|| <= exp(delta_L Gamma_L)-1 -> 0
```

provided `delta_L Gamma_L -> 0`.

Dependencies:

- identity-starting norm-continuous semigroups;
- a generator bound;
- a lapse scaling selected to make the product vanish.

Evidence: correct elementary semigroup analysis. The finite certificates verify
the chosen scaling, not its gravitational origin.

Replacement gate: derive physical time normalization and the generator from the
model, and prove convergence in the topology appropriate to the target
observer algebra.

## Factorial Type-II Scaffold

Current statement: factorial matrix dimensions admit amplification inclusions,
whose UHF tracial closure is the hyperfinite Type-`II_1` factor.

Dependencies:

- noncanonical factorial cutoff subsequence;
- amplification basis and normalized trace;
- standard UHF closure theorem;
- diagonal control matched by construction.

Evidence: correct divisibility arithmetic and standard operator-algebra input.
The code stores the limiting algebra identification as theorem metadata rather
than computing a continuum limit.

Replacement gate: derive a canonical observer algebra, state, maps, and GNS or
crossed-product limit. Establish subsequence independence or explain why a
specific regulator is physical.

## Inclusion-Covariant Dynamics

Current statement: selected covariance errors decrease along the factorial
subsequence.

Dependencies:

- factorial amplification;
- rank-ordered basis;
- selected normalized energy function;
- conditional expectation onto amplification fibers;
- chosen short-time scaling.

Evidence: finite arithmetic over energy vectors and selected analytic bounds.

Replacement gate: prove equivariance and generator or semigroup convergence for
canonical representation-theoretic maps, including robustness to basis and
regulator choices.

## Consecutive UCP Refinements

Current statement: the trace-filled map is UCP and trace preserving, has a
`1/n` defect on `e_12,e_21`, and preserves a selected response witness.

Dependencies:

- trace-filled complement;
- selected matrix-unit pair;
- diagonal screen definition.

Evidence: exact finite proof for the map and selected pair. The new Phase 0
counterexample shows that its full unit-ball multiplicativity defect remains
`1` along infinitely many cutoffs.

Replacement gate: construct canonical equivariant maps and prove uniform
approximate multiplicativity on a stated low-energy operator domain, in a
stated norm or topology.

## Conditional Continuum Obstruction

Current statement: a screen-factored dictionary is incomplete when two limiting
screen shadows agree and a response gap persists.

Dependencies:

- all six lift conditions are assumptions;
- screen factorization is assumed;
- equal screen distance and nonzero response gap are supplied to the schema.

Evidence: valid conditional logic, but no instantiated continuum pair.

Replacement gate: establish every lift condition in one model and prove either
a stable identification lower bound or a completeness theorem for an enlarged
physical screen observable system.

## Certificate Package

Current statement: five certificate families pass at fixed bounded parameters.

Dependencies: all assumptions above.

Evidence: software regression and JSON validation. Package success is largely
defined as every returned claim flag evaluating to true.

Replacement gate:

- direct invariant and norm computations;
- regenerated artifact equality or hashes;
- parameter sweeps and adversarial cases;
- larger-cutoff scaling;
- independent implementation or formal proof for central statements;
- separate labels for proved theorem, numerical evidence, and metadata audit.

## Phase 0 Conclusion

The elementary collision and semigroup bound are correct. Their physics content
currently comes from selected definitions and regulator choices. The factorial
Type-II, trace-filled embedding, and conditional continuum layers must not be
used as evidence for a physical limit until the Phase 1 model and Phase 2 maps
replace them.

## Global Geometric Gibbs Gate

Current statement: the positive-mass spherical angular Fock Gibbs states
converge in trace norm as the angular cutoff is removed. For the declared global
algebra `B(Fock)`, the limit remains Type I and its inner modular crossed product
is not the Type-II observer factor.

Dependencies:

- positive mass or explicit removal/treatment of the massless constant mode;
- the global observable algebra is declared to be `B(Fock)`;
- angular cutoff removal is taken before any local-net GNS construction.

Replacement gate: construct localized static-patch Weyl algebras and prove
distributional state convergence; do not infer local factor type from global
density matrices.

## Fixed-UV S-Wave Phase Space

Current statement: at fixed UV momentum cutoff, projected Dirichlet-box
symplectic forms, quasifree covariances, and unequal-time two-point functions
are Riemann sums converging to half-line thermal forms at `beta=2 pi R`. The
finite states satisfy uncertainty and the exact KMS boundary identity.

Dependencies:

- conformally coupled massless s-wave;
- artificial Dirichlet stretched-horizon wall;
- compact `C^2` polynomial Cauchy data;
- hard fixed UV bandlimit and its nonlocal quotient phase space.

Replacement gate: remove the UV cutoff on smooth data, add all angular radial
operators, and identify the limiting distribution directly with the
Bunch-Davies local state before invoking Type `III_1` classification.

Update: the s-wave UV cutoff is now removed by explicit distributional
derivative tail estimates. The all-angular conformal successor proves
equal-time wall convergence under compact radial support plus field
angular-Sobolev and momentum energy-Sobolev assumptions, and verifies the exact Euclidean optical/
Bunch-Davies identity. The combined s-wave wall/UV statement remains an
iterated limit with selected diagonal refinements. The remaining replacement
gate is all-angular unequal-time UV control, Lorentzian Hadamard boundary-value
convergence, and local GNS identification.

## All-Angular Equal-Time Static-Patch Covariance

Current statement: for compactly supported conformal-scalar data, fixed-`ell`
Dirichlet domain exhaustion plus wall-uniform angular tails proves full
all-angular equal-time covariance convergence. Field data require angular
`H^s(S^2;L^2_x)` control; momentum data require the corresponding
energy-weighted angular form norm. The Euclidean limiting kernel is exactly the
conformal Bunch-Davies kernel.

Dependencies:

- free conformally coupled massless scalar in four dimensions;
- artificial Dirichlet stretched-horizon wall;
- compact radial support bounded away from the moving wall;
- positive angular Sobolev order, with a stronger form-domain norm for momentum;
- equal-time covariance convergence rather than a Lorentzian spacetime theorem.

Replacement gate: prove uniform all-angular UV and unequal-time estimates on
compact spacetime tests, establish the Hadamard boundary value, and only then
invoke local Type-`III_1` and continuous-core results.

Update: the pairwise compact-test Lorentzian gate is now closed for the free conformal
field. Green reduction and finite propagation reduce bounded causal hulls to
the all-angular equal-time theorem, and the exact strip kernel identifies the
limit with Bunch-Davies. Verch's theorem supplies the hyperfinite Type-`III_1`
local/static-patch factors and the standard continuous core is Type
`II_infinity`. The replacement gate is now gravitational: observer/reference
degrees of freedom, constraint action, positive-energy finite corner, trace,
and entropy interpretation.

## Lorentzian Hadamard Net And Free-Field Core

Current statement: pairwise compact-test finite-wall two-point forms converge to
the exact Bunch-Davies Hadamard distribution. In the global de Sitter
Bunch-Davies representation, regular-diamond Weyl algebras are hyperfinite Type
`III_1`; this includes the static patch when treated as the open-hemisphere
domain with the opposite patch as causal complement. Its continuous core is
hyperfinite Type `II_infinity`.

Dependencies:

- free conformally coupled massless scalar;
- exact identification with the global Bunch-Davies restriction;
- compact spacetime tests and wall positions beyond their causal hulls;
- external Hadamard/microlocal and local-factor classification theorems;
- no claim that finite Type-I von Neumann closures converge in algebra type.

Replacement gate: construct the physical observer clock/reference system on
this net, impose the Hamiltonian constraint, prove the positive-energy
Type-`II_1` corner and finite trace, and derive a gravitational observable from
the redshifted frame-capacity law.

## Redshifted Rotational-Frame Capacity

Current statement: a translated near-horizon collar trial function and the
min-max principle supply one finite-wall eigenstate below a fixed static-energy
budget in every integer-spin sector through
`L_delta=Theta(sqrt(R/delta))`. A declared pure coherent token over those states
has exact `SO(3)`-twirl relative entropy
`2 log(L_delta+1)=log(R/delta)+O(1)`.

Dependencies:

- free conformal scalar one-particle sector;
- hard finite-wall Killing-energy spectral support, but no local proper-energy
  or gravitational energy support;
- moving collar and no backreaction/occupation-number constraint;
- compact rotation subgroup only;
- pure coherent token, not an arbitrary state with the same irrep weights.

Replacement gate: specify the physical observer channel that performs the
rotation expectation, prove backreaction control, and extend the expectation
trace-preservingly to the Type-II observer algebra before making a
generalized-entropy or no-go claim.

## Energy-Constrained Rotational Frameness Obstruction

Current statement: for a clock-only truncation with invariant spectators, the
compact `SO(3)` fixed-point algebra cannot distinguish an explicit orthogonal
near-horizon directional pair in a hard finite-wall static-energy window. Every
decoder through the canonical expectation has worst-case pair error at least
`1/2`; full fixed-spin recovery has exact optimal normalized diamond error
`1-1/(2L_delta+1)^2`, and the coherent-token frame entropy
is `log(R/delta)+O(1)`.

Dependencies:

- free conformal Bunch-Davies one-particle collar family;
- the full gauge completion includes the compact observer stabilizer;
- no accessible subsystem other than the scalar clock carries rotation charge;
- hard finite-wall field static-energy support from Rayleigh-Ritz, but no local
  proper-energy or gravitational energy bound;
- any later rotation-invariant corner retains nonzero common support for the
  pair;
- existing fixed-irrep twirl recovery and relative-entropy-of-frameness bounds.

Claim boundary: this is a conditional compact-fixed-point obstruction. CLPW
already contains the qualitative clock-versus-frame observation. This result
neither constructs the noncompact `SO(1,4)` average nor proves that the compact
expectation extends through the named time crossed product.

Replacement gate: put the scalar clock and a covariant `SO(1,d)` observer on the
same local KMS net, derive both constraint/energy budgets, and determine whether
backreaction or the finite gravitational trace removes the collar logarithm.

## Redshifted Charged-Reference Achievability Bound

Current statement: on the same hard-energy spin `L_delta`, the clock-only compact
expectation has exact optimal normalized diamond error
`1-1/(2L_delta+1)^2`. The canonical prepared `SO(3)` Peter-Weyl reference has a
constructive decoder with error at most `3(2L_delta+1)^2/(8J)`. Hence
`J=O(R/(epsilon delta))` suffices for error `epsilon`; under the declared rotor
Hamiltonian `C_left/(2I)`, the mean reference energy is
`O(R^2/(I epsilon^2 delta^2))` when `I` is fixed independently of `delta` and
`epsilon`. This is a same-target comparison, not a resource-matched experiment.

Dependencies:

- the hard finite-wall conformal-scalar target sector;
- the canonical truncated Peter-Weyl token, POVM, and decoder;
- the exact tensor-rank multiplier formula;
- a chosen compact rigid-rotor Hamiltonian and moment of inertia;
- an instantaneous channel benchmark with no coherent-token lifetime theorem;
- constructive upper bounds, not optimal resource lower bounds.

Replacement gate: derive the inertia, reference Hamiltonian, and local coupling
from a covariant static-patch observer; include the boost sector and determine
whether backreaction or the gravitational trace changes the inverse-gap law.

## Covariant-Observer Energy Identifiability No-Go

Current statement: fix the compact Peter-Weyl token, representation cutoff,
orientation POVM, decoder, and recovery target. Every positive Hamiltonian
`H_J=a_J C_left` is rotation invariant, and

```text
<H_J>=a_J 3J(J+2)/5.
```

Hence any prescribed positive ground-subtracted token-energy profile is
realized by `a_J=5E_J/[3J(J+2)]` without changing the channel or recovery error.
The observer representation and recovery theorem therefore do not identify a
physical energy or backreaction scaling.

Dependencies:

- the canonical compact Peter-Weyl representation, token, and decoder;
- the exact mean-Casimir formula;
- an instantaneous recovery metric independent of finite-time Hamiltonian
  evolution;
- no finite-size physical action is included among the fixed kinematic data of
  this identifiability theorem.

Claim boundary: this is a kinematic identifiability obstruction. Different
cutoff-dependent coefficients are dynamically inequivalent regulator
completions, not different descriptions of one fixed observer. The theorem does
not apply after a physical action, inertia law, state-preparation cost, lifetime,
and backreaction constraint have been fixed. It is compact-`SO(3)` only and does
not assign a positive Casimir Hamiltonian to noncompact `SO(1,d)`.

Repository follow-up: a separate spherical-top EFT now selects a conditional
compact Hamiltonian and inertia law. The replacement gate is to derive those
from matter/gravity, couple the observer locally to the same Lorentzian static-
patch net, and optimize recovery under a stress-energy and backreaction budget.

## Finite-Size Static-Patch Rotation Observer

Current statement: a marked spherical-top EFT stipulates
`I=kappa m a^2` and gives `H_rot=C_left/(2I)`. For any prepared rotor state on
`L^2(SO(3))`, the declared excitation and local compactness bounds

```text
E_rot/m<=zeta<=1,
2G(m+E_rot)/a<=chi<1,
```

imply the mean-Casimir capacity

```text
Cbar<=kappa chi^2 zeta a^4/[2G^2(1+zeta)^2].
```

For every truncation spin `J`, Markov plus gentle projection transfers the
finite Peter-Weyl multiplicity theorem to the full rotor state. Every decoder
after the fixed append-and-twirl channel has error at least
`max_J max(0,1-(J+1)^2/(2L+1)-sqrt(Cbar/((J+1)(J+2))))`. Hence a fixed finite
observer's error tends to one on `L_delta=Theta(sqrt(R/delta))`, including states
with high-spin tails. If the apparatus follows the shrinking collar with
`a=alpha rho_delta`, its mean-Casimir capacity falls as `O(R^2 delta^2/G^2)`.
Separately, the existing constructive hard-cutoff protocol loses branchwise
spectral certification at `delta=Theta(sqrt(G/epsilon))` up to declared
constants.

Dependencies:

- the hard-energy conformal-scalar collar target;
- the full Peter-Weyl rotor and exact finite-support multiplicity lower bound;
- the marked spherical-top worldtube EFT and stipulated isotropic inertia law;
- positive additive rest and mean rotor energies;
- a declared local compactness margin and excitation-fraction cap;
- Markov tail control, gentle projection, and channel contractivity;
- no external multiplicity memory outside the modeled observer.

Claim boundary: the any-decoder result is universal over mean-energy-bounded
prepared rotor states and deterministic decoders only after the fixed append-
and-twirl channel. It excludes pre-correlated encoders, postselection, other
hardware, and general finite-time dynamics; the separate collective heat-
semigroup extension covers one conditional Markov model. The compactness condition is not a
rotating-GR theorem, and the protocol threshold uses a sufficient rather than
optimal cutoff. No local interaction, lifetime, stress-energy fluctuation,
boost sector, Type-II trace, or entropy identity is present.

Replacement gate: derive a local field-top interaction and bounded-time decoder,
construct a controlled rotating Einstein-matter or semiclassical source, and
incorporate the clock and boost generators into a regulated `SO(1,d)` constraint.

## Confined Orbital Representation-Energy Bound

Current statement: for finitely many spinless nonrelativistic particles of
positive total rest mass `M`, confined to a rotationally invariant radius-`a`
configuration domain, the quadratic-form premise

```text
H_ex>=sum_i p_i^2/(2m_i)>=0
```

implies for every state

```text
<L^2><=2Ma^2E_ex,
R_ref>=1/(32Ma^2E_ex+8),
Pr(j>=J+1)<=2Ma^2E_ex/[(J+1)(J+2)].
```

The global risk statement is independent of particle number, purity, POVM,
and arbitrary rotation-trivial internal multiplicity. It includes zero-mean
states and rare high-spin tails. The associated spectral theorem replaces the
kinetic premise by sector floors `epsilon_j`: finite
`sum_j(2j+1)^2 exp(-beta epsilon_j)` gives
`A_SO3<=beta E+log Z_H(beta)`.

Dependencies:

- spinless nonrelativistic orbital generators;
- hard support `|x_i|<=a` and a rotationally invariant form domain;
- positive masses and a nonnegative Hamiltonian, with its energy zero fixed,
  satisfying `H_ex>=T` (or a proved form offset `H_gs+Delta>=T`, with `Delta`
  included in the energy budget);
- the global Haar-prior chordal orientation-risk theorem;
- rotation-trivial, rather than nontrivially charged, internal multiplicity.

Claim boundary: the optional elimination
`2G(M+E_ex)/a<=chi => <L^2><=chi^2a^4/(8G^2)` uses a declared compactness proxy,
not an Einstein-matter body theorem. Intrinsic spin, relativistic fields,
negative interaction energy, soft support, local readout, stress, lifetime,
and metric response are open. The fixed invariant counterexample
`H_bad=sum_j(1-e^-j)P_j<1` proves that covariance and finite energy alone cannot
replace the growing sector-floor premise.

Replacement gate: the supported Skyrmion collective family now has a uniform
floor. Extend it to noncollective modes and bound projection errors, then use
the same action for the UO.3/UO.4 channel and coherence bounds.

## Supported Skyrmion Collective Spectral Floor

Current statement: for every massive-Skyrme hedgehog profile hard-supported
inside areal radius `a`, with minimum support lapse `N_w>0`, termwise comparison
of the exact static mass and collective-inertia densities gives

```text
I[F]<=[4/(3N_w)]M[F]a^2.
```

Minimizing the adiabatic collective energy over arbitrary radial profile
relaxation therefore yields

```text
E_j>=sqrt[3N_w j(j+1)/2]/a.
```

The floor grows linearly at large spin. Both the integer and fermionic
projective rotational partition functions are finite, so the spectral Gibbs
theorem supplies an all-state global orientation-risk floor and Markov controls
rare high-spin tails.

Dependencies:

- the declared massive `SU(2)` Skyrme action and positive static energy terms;
- a hard-supported hedgehog family with fixed worldtube radius and `N_w>0`;
- exact adiabatic collective energy `M[F]+j(j+1)/(2I[F])` for each profile;
- the global asymmetry/Gibbs orientation-risk theorem;
- a spherical unmarked wall whose mass may enter `M` but carries no additional
  orientation inertia.

Claim boundary: fixed-profile pullback of the stated Skyrme action is exactly
quadratic in collective angular velocity. A nonzero `Omega^4` term is induced
by profile/wall relaxation and softens the rigid spectrum, but the density
bound controls arbitrary radial hedgehog relaxation without truncating that
expansion. The theorem does not prove collective-band completeness, control
nonspherical/noncollective field or wall modes, bound Born-Oppenheimer
projection errors, establish isospin access, or define the renormalized quantum
field Hamiltonian needed for a full sector theorem.

In particular, the nonlinear infimum over supported hedgehog profiles is not
yet a proof of a quantum compression inequality `P_jH_jP_j>=a_jP_j`; defining
the collective projector and its Hamiltonian domain is part of the replacement
gate.

Replacement gate: construct the quantum collective projector and coupled
Skyrmion-membrane-anchor quadratic Hamiltonian, prove the compression floor and
a complement gap after rotational zero-mode removal, and bound the off-band
coupling. Then join the resulting full-field floor to the local readout and
gravity ledgers.

## Collective-Band Feshbach Transfer And Insufficiency

Current statement: for a declared quantum collective projector `P_j`, let
`Q_j=1-P_j` and suppose in one rotational sector

```text
P_jH_jP_j>=a_jP_j,
Q_jH_jQ_j>=d_jQ_j,
||Q_jH_jP_j||<=v_j.
```

Then the complete sector floor is at least

```text
[a_j+d_j-sqrt((d_j-a_j)^2+4v_j^2)]/2.
```

If `d_j>=a_j+Delta_j` and
`v_j^2<=eta Delta_j a_j`, it is at least `(1-eta)a_j`. The same inputs bound
the complement weight of an eigenstate below `d_j`. Hence these margins would
transfer the supported Skyrmion's linear collective floor and control the
projection errors entering the current/readout lemmas.

Dependencies:

- a self-adjoint full sector Hamiltonian with a common quadratic-form domain;
- an actual quantum collective projector, not only a nonlinear variational
  profile family;
- a compression floor, complement floor, and bounded off-diagonal block;
- uniform margins over the spin range used in the observer theorem.

Claim boundary: the transfer theorem is exact, but its quantum projector,
compression, complement, and coupling inputs are not yet jointly certified. A
positive two-band Hamiltonian can
preserve `P_jH_jP_j=a_jP_j` while reducing the full floor to `delta a_j`.
Even both diagonal floors growing as `a_j` and `2a_j` is insufficient: an
uncontrolled coupling can leave a constant full floor. The authenticated
radial theorems now cover the fixed-wall and spherical moving-membrane `l=0`
channels, not the anchor, nonspherical complement, or off-band couplings.

Replacement gate: derive the quantum projector/compression from collective
quantization, construct the coupled dynamical Hessian with zero modes removed,
and certify `d_j` and `v_j` in a stated operator norm.

## Radial Dynamical-Gap Conversion

Current statement: time-dependent radial fluctuations of the declared Skyrme
hedgehog obey

```text
L_Jacobi eta=omega_hat^2 W eta,
W=(x^2+8sin^2F)/N,
W<=(x_w^2+8)/N_w.
```

The authenticated exact-solution successor proves `L_Jacobi>=1` on the full
physical regular-origin-to-fixed-wall form domain. Adaptive correlated
Newton-tube replay gives a positive-radius quotient above `1.0386099769`; the
cancellation-preserving origin quotient is above `36.8298881657`. Hence
`omega_hat_rad^2>=1/25` and `omega_K>=e f_pi/5`.

Dependencies: dimensionless time `tau=e f_pi t`; fixed ideal wall; radial
hedgehog fluctuations; unweighted Jacobi form coercivity; hard support with
`N_w>0`. The physical Killing frequency is
`omega_K=e f_pi omega_hat`.

Evidence: authenticated exact certificate SHA256
`695310609d070f6dba2c678982ffc87472ed7c341813137fb90ad9dd9e1e6096`,
with 109 positive-radius leaves and maximum refinement depth five. The origin
and wall ground-state-transform boundary terms vanish on the declared form
domain.

Claim boundary and replacement gate: this theorem holds the ideal wall fixed.
The next theorem adds its spherical boundary mass. The anchor, nonspherical
channels, rotational zero-mode removal, and off-band couplings remain separate.

## Coupled Profile-Membrane Radial Gap

Current statement: impose the exact moving-mirror condition
`eta(a)+F_0'(a)q=0` for a spherical positive-tension Nambu-Goto membrane in
Young-Laplace equilibrium. Eliminating `q` cancels the wall-slope factor and
gives exact boundary coefficients

```text
M_0=800/47,  B_0=6386/1175.
```

The compatible witness `v=1/[(x-9/4)^2+8]` satisfies `L_Jacobi v/v>=1/100`
on the authenticated exact profile and has positive transformed wall
coefficient `39878/69325`. With `W<=25`,

```text
omega_hat_l0^2>=1/2500,
omega_hat_l0>=1/50.
```

Evidence: authenticated certificate SHA256
`2bb48f770504ab5a0a0f9b3139b881877a414ddb9b8c19cd34c81bfd26b42686`,
with 95 positive-radius leaves, maximum refinement depth five, and regular
origin quotient above `37.277`.

Claim boundary: this closes the complete spherical profile-membrane `l=0`
subgate, not the anchor, nonspherical profile/membrane modes, junction
conditions, self-gravity, or Feshbach off-band couplings. The separate
branch-coordinate theorem could sharpen the floor toward the floating `0.198`
estimate if `Z` and `k` are certified, but they are no longer required for a
strict positive moving-wall theorem.

## Finite-Time Collective Rotation Diffusion

Current statement: common isotropic proper-time noise with collective charges
`Q_a=J_a^(target)+J_a^(rotor,left)` generates an `SO(3)` heat-kernel twirling
semigroup. Its normalized diamond distance to Haar append-and-twirl obeys

```text
eta_heat(gamma T)
 <= min(1,0.5 sqrt[q(9-2q+q^2)/(1-q)^3]),
q=exp(-4 gamma T).
```

Subtracting this distance transfers the all-state mean-Casimir recovery lower
bound to finite proper time for decoders with only the target-plus-rotor output.
The sufficient choice `gamma T=(1/2)log(2L+1)` makes the correction `O(1/L)`,
giving `T_delta=Theta(gamma^-1 log(R/delta))` on the hard-energy collar sector
if `gamma` is cutoff independent. This is not a necessary mixing law.

Dependencies:

- isotropic Markov/white-noise collective rotations;
- rotational invariance `[H_target+H_rot,Q_a]=0` or a specified toggling control;
- a rank-one spatial covariance kernel with equal target-rotor coupling;
- an inaccessible Brownian record, bath output, and bath purification;
- standard compact-group heat-kernel/Peter-Weyl theory;
- the mean-Casimir Haar recovery theorem and decoder contractivity.

Claim boundary: this is a collective open-system bridge, not a spatially local
field-top derivation. Exact white noise has infinite bandwidth; no controlled
finite-bath Davies error or finite stress-energy realization is supplied. It
excludes bath feedback, finite memory, pre-correlated encoders, postselection,
noncompact boosts, and gravitational backreaction.

Replacement gate: derive the collective noise kernel and diffusion rate from a
local static-patch current/worldtube interaction, then prove a joint observer
lifetime, localization, and stress-energy scaling window.

The norm-honest transfer layer is now executable. A certified physical-to-heat
normalized diamond bound transfers both the any-decoder obstruction and the
explicit Peter-Weyl decoder upper bound with additive correction
`eta_heat+eta_local`. The existing finite-switch ULE residual is kept in its
actual ancilla-stable state operator norm and transfers only through the fixed
Choi witness, with the explicit factor `d`. Typed bound objects prevent using
that residual as a channel diamond estimate. The remaining replacement gate is
physical rather than algebraic: derive `eta_local`, or prove a valid norm
upgrade, from the local field-top model.

## Common-Mode Covariance Mismatch

Current statement: in a two-charge axial Markov model with normalized covariance
`C=[[1,c],[c,1]]`, the relational coherence
`(|1,0>+|0,1>)/sqrt(2)` with exchanged-charge gap `Delta>0` gives

```text
(1/2)||Phi_C,T-Phi_*,T||_diamond
 >= [1-exp(-2 gamma T Delta^2(1-c))]/2.
```

Under the sufficient heat schedule `gamma T=(1/2)log d`, allocating mismatch
`A/d` therefore requires `1-c=O(1/(Delta^2 d log d))`. For the illustrative model
`c(r)=exp(-r/ell_B)` at fixed nonzero separation, this becomes
`ell_B/r=Omega(Delta^2 d log d)`. A finite-cell bounded-generator Duhamel estimate gives
a complementary upper bound proportional to the weighted entrywise covariance
defect.

Dependencies:

- active Gaussian Markov noise with an inaccessible environment record;
- an axial two-charge sector with fixed nonzero charge gap `Delta`;
- the sufficient logarithmic heat schedule and a chosen `A/d` error allocation;
- fixed nonzero target-reference separation for the correlation-length example;
- bounded generators for the finite-cell upper bound.

Claim boundary: this is a covariance test, not a generic locality no-go. Local
couplings can have long-range or critical bath correlations, and extra
transverse dynamics is not covered by the exact axial witness. No Bunch-Davies
noise kernel, isotropic `SO(3)` comparison, Davies error, lifetime, or
backreaction is derived.

Replacement gate: calculate the covariance from a named local static-patch
field/worldtube action and insert it into the physical-channel error budget.

## Bunch-Davies Scalar Common-Mode Obstruction

Current statement: for two identical, equal-redshift, optically pointlike axial
zero-Bohr charge couplings to the conformal Bunch-Davies scalar, the exact
normalized Kossakowski cross coefficient at optical separation `y=d_H/R` is

```text
c_0(y)=y/sinh(y).
```

Inserting this into the covariance witness shows that fixed nonzero optical
separation has asymptotic channel mismatch `1/2` along the sufficient
`gamma T=(1/2)log d` schedule. An `A/d` allocation requires

```text
d_H/R=O(1/[Delta sqrt(d log d)]).
```

On one shell at proper horizon distance `rho`, the exact optical geometry then
requires

```text
theta=O[(rho/R)/(Delta sqrt(d log d))].
```

Dependencies:

- the exact conformal Bunch-Davies optical spectral kernel;
- stationary weak-coupling/long-time Davies scaling;
- zero-Bohr secular charge components;
- equal redshift, coupling strength, charge normalization, and spatial profile;
- pointlike spectral ratios or an optically narrow smearing limit;
- the axial covariance witness and sufficient logarithmic protocol schedule.

Claim boundary: this is the first named local-bath calculation, but it is a
localized scalar pure-dephasing surrogate rather than the hard global angular
target and spherical-top torque. Finite switching gives a spectral average;
finite profiles require a double-smeared kernel; proper width `a` near the
horizon corresponds to optical width `O(a/rho)`. No Davies error, diffusion
rate, lifetime, or backreaction is controlled.

Replacement gate: derive the three-axis torque spectral matrix for an actual
finite top and hard angular field sector, including switching, optical smearing,
and gravitational error budgets.

## Exact Optical-Radial Smearing Invariance

Current statement: the zero-frequency kernel
`phi_0(y)=y/sinh(y)` is the zonal spherical function on optical `H^3_R` and
obeys `M_u phi_0(r)=phi_0(u)phi_0(r)`. Therefore arbitrary nonnegative radial
profiles about centers `p,q` have coefficients

```text
B_pp=A_mu^2,
B_qq=A_nu^2,
B_pq=A_mu A_nu phi_0[d(p,q)/R],
```

so the normalized cross coefficient is exactly the point-center value. Radial
profile size and shape cancel, even when the two profiles differ.

At every spectral parameter `p`, `phi_p(y)=phi_0(y)sinc(py)`. Therefore any
common nonnegative finite-switching spectral/filter weight obeys

```text
|c_eff(y)|<=phi_0(y).
```

Finite switching cannot improve the normalized radial scalar pure-dephasing
correlation beyond the zero-mode value, although it changes the absolute rates.

Dependencies:

- stationary conformal scalar zero-frequency spectral kernel;
- nonnegative profiles radial in the optical `H^3_R` volume measure;
- finite positive spherical amplitudes;
- physical source weights implementing those effective optical profiles via
  `f_opt=Omega^3 J_physical`;
- a common nonnegative stationary spectral/filter weight for the finite-
  switching ceiling.

Claim boundary: this closes the radial-width loophole and controls finite-
switching covariance only for scalar pure dephasing. It does not cover nonradial
or derivative torque densities, dissipative nonzero-Bohr jump sectors, a
spherical-top action coupled to the hard angular target, or the stress-energy
cost of the conformal source weights.

Replacement gate: decompose the actual top torque density into optical
spherical multipoles and determine whether any nonradial component can supply
the required rank-one covariance without violating localization or backreaction.

## Polarization-Resolved Optical-Gradient Obstruction

Current statement: for localized zero-Bohr vector charges coupled to
parallel-transported optical scalar-gradient components, the normalized cross
Kossakowski matrix is

```text
diag(c_parallel,c_perp,c_perp),
c_parallel=-3 phi_0'',
c_perp=-3 phi_0'/sinh(y).
```

The auto blocks are isotropic. Axiswise diagonalization gives collective and
relative rate weights `1+c_a` and `1-c_a`, so every nonzero center separation
has unavoidable relative rotational noise and cannot equal the ideal
collective heat generator. The defects begin as `(7/10)y^2` longitudinally and
`(2/5)y^2` transversely.

Dependencies:

- an independent conformal scalar bath on optical `R x H^3_R`;
- localized or suitably renormalized derivative couplings;
- parallel-transported frame convention;
- rotationally invariant target/reference free Hamiltonians and zero-Bohr
  charges;
- a finite angular-momentum truncation or an appropriate unbounded Davies
  theorem;
- controlled Lamb shift and weak-coupling secular errors.

Claim boundary: this is an exact generator-level covariance obstruction for a
conditional gyroscopic optical coupling. It is not a mechanical top torque.
The charge-gap-dependent `A/d` scaling can be imported axiswise. In addition,
the two-spin-half singlet sector gives an exact full three-axis finite-time
witness: its Bell-diagonal survival satisfies

```text
(1/2)||E_s-E_s^collective||_diamond >= 1-p_S,
1-p_S=(3/2)s y^2+O(y^4).
```

This proves the `1/sqrt(d log d)` co-location exponent without splitting the
three noncommuting axes, but only for the spin-half witness sector.

Replacement gate: derive one local matter action for the hard target and finite
top, its physical conformal source weights, a noncommuting three-axis channel
extension to the hard angular sector, and a joint smearing/lifetime/
backreaction error budget.

## Casimir-Enhanced Higher-Spin Gradient Witness

Current statement: for every integer spin `L`, the gradient-channel singlet
survival has an exact irreducible-tensor block formula. Its uniform local
expansion is

```text
1-p_L(s)=(4/3)L(L+1)s Delta+R_L,
|R_L|<=32s^2L^4Delta^2,
Delta=(1-c_parallel)+2(1-c_perp).
```

For the optical gradient kernel this becomes

```text
1-p_L(s)=2L(L+1)s y^2+controlled higher orders.
```

With `d=2L+1`, `s=(1/2)log d`, and an `A/d` allocation, the necessary local
scaling is `y=O(d^(-3/2)/sqrt(log d))`. At that scaling the explicit Duhamel
parameter is `O(1/d)`.

Dependencies:

- the effective equal-spin zero-Bohr gradient GKSL generator;
- the standard irreducible-tensor decomposition of `End(V_L)`;
- use of the entangled spin singlet as a channel-comparison probe;
- gradient correlations in the near-coincidence optical regime.

Claim boundary: this is an exact arbitrary-integer-spin channel witness and a
uniform local expansion, not a derivation of the channel. It does not restrict
the diamond norm to product-prepared references, justify a growing-`L` Davies
limit, or control source stresses and backreaction.

Replacement gate: derive the generator from a smooth local finite-top and hard-
target action, prove uniform open-system errors at the required co-location
scale, and compare the singlet channel witness with the operational prepared-
reference recovery task.

## Local Pseudoscalar Gyroscope And Lapse Tradeoff

Current statement: the parity-even local action

```text
S_top=int d tau[-m+(I/2)|varpi-gB|^2],
B_a=e_a^mu(nabla_mu chi+a_mu chi)
```

derives `H_int=gJ_a^leftB_a`. The acceleration-improved conformal identity
maps `B_a` to `N^-2D_a^opt chi_opt`, so equal-redshift normalized correlations
are exactly the optical gradient tensor.

The proper zero-frequency spectrum and correlation time scale as `N^-3` and
`N`. On spin `L`, fixed coupling therefore has loaded Markov parameter growing
as `L(L+1)N^-2`. Under a declared reference-state interaction-RMS budget,
`g=O(N^2/sqrt(L(L+1)))` and `gamma=O(N/L(L+1))`. The chosen sufficient
logarithmic schedule then lasts `Theta(L(L+1)log d/N)`, becoming
`Theta(d^3 log d)` on `N~1/d`. The imported same-shell angle is
`O(d^-5/2/sqrt(log d))`.

Dependencies:

- a generic conformally coupled pseudoscalar rather than a shift-symmetric
  axion;
- the static observer congruence and acceleration improvement;
- a finite optical derivative smearing rms;
- equal-redshift localized spin systems.

Claim boundary: the action derives the top-side and a lumped target spin, not a
distributed hard field current. The RMS premise is state dependent, not an
operator bound, all-state Davies theorem, necessary mixing time, stress-energy,
or backreaction theorem.

Replacement gate: bound the current multipole remainder and nonzero-Bohr
sectors, then derive the source/support stress and lifetime budget.

## Distributed Hard-Current Multipole Bound

Current statement: after specified parallel transport to a center frame, for
`V=g int Bbar_a(x)ellbar_a(x)` and `L_a=int ellbar_a(x)`, the local-to-lumped
remainder is exactly `g int[Bbar_a(x)-B_a(p)]ellbar_a(x)`. A declared
product-state bath Lipschitz bound
and target current first moment give `||(V-V_0)psi||<=|g|KM_1`. With bounded
operators on invariant compressed subspaces, the corresponding unitary-channel
distance is at most `min(2,2T|g|KM_1)`.

If `[H_T,L_a]=0`, all nonzero-Bohr current sectors have zero monopole and obey
the same sectorwise first-moment estimate. A two-cell model saturates the
linear support law, so rotational conservation does not generically produce a
quadratic multipole improvement.

Dependencies:

- rotational conservation of the integrated target charge;
- a product-state vector or compressed-operator bath Lipschitz estimate;
- finite current first absolute moments;
- distinct nonoverlapping worldtubes for the support-size conclusion.

Scaling consequence: the interaction-vector budget alone allows `O(d^-1)`
optical support. Under separately declared zero-Bohr linear, aggregate
nonzero-Bohr, and second-order jump transfers in a normalized diagonal-jump
GKSL surrogate, a sufficient worst-case design for generic
zero-Bohr monopole-dipole interference has optical radius `O(d^-3/log d)` and
same-shell angular radius `O(d^-4/log d)`. If every transported compressed
zero-Bohr current-dipole component vanishes as an operator and a covariant
Hessian/second-moment bound applies, the certified design relaxes to optical
radius `O(d^-3/2/sqrt(log d))` and angular radius
`O(d^-5/2/sqrt(log d))`.

Claim boundary: overlapping distinguishable sectors evade the disjointness
condition. The theorem does not derive the Lipschitz/current moments from a
matter action, the three interaction-to-jump/Kossakowski/Lamb-shift stability
bounds including gap aggregation,
componentwise dipole cancellation, all-state or QFT-uniform Davies/secular
control, or source stress and gravity.

Replacement gate: compute those inputs for a named hard target and prove a
joint localization, lifetime, and backreaction window.

## Controlled Compactness-Localization Branch Obstruction

Current statement: identify the definite top spin with the protected hard spin
`L`, impose the stipulated spherical-top inertia/excitation/compactness model,
and bound the thin-shell three-dimensional proper enclosing radius by the exact
same-shell static-slice support distance. The compactness floor is

```text
a_min=[2G^2(1+zeta)^2L(L+1)/(kappa chi^2 zeta)]^(1/4)
     =Theta[sqrt(G)d^(1/2)].
```

The exact optical-to-proper shell conversion adds one lapse factor along
`rho/R=1/d`. The leading higher-spin common-mode co-location law plus distinct
equal-worldtube nonoverlap then gives

```text
a_max/R=O[d^(-5/2)/sqrt(log d)].
```

Hence `a_max/a_min` tends to zero as
`(R/sqrt(G))d^-3/sqrt(log d)`: no growing-`d` sequence can remain in the
controlled local-common-mode branch at fixed `R^2/G` inside these declared
hypotheses. This does not control nonperturbative large-separation channel
behavior. The generic and
dipole-cancelled sufficient GKSL designs have compactness utilization scaling as
`(G/R^2)d^9(log d)^2` and `(G/R^2)d^6log d`, respectively.

Dependencies:

- identification `J_top=L_hard`;
- the spherical-top inertia and compactness hypotheses;
- an equal-radius thin-shell three-dimensional enclosing radius controlled by
  the same-shell static-slice distance;
- the local perturbative common-mode co-location law;
- distinct equal-size nonoverlapping worldtubes; and
- dimensionless mismatch and jump-transfer constants remaining `O(1)`.

Claim boundary: the controlled-branch obstruction is conditional. Its
finite default crossing at `L=30` is an illustrative leading-envelope
crossover, not an exact channel cutoff or universal prediction. The GKSL
crossings close sufficient design certificates only. No stress tensor, support
binding energy, lifetime, Einstein-matter solution, uniform Davies theorem, or
global channel no-go or general collapse theorem is derived.

Replacement gate: select a named rotating matter source, calculate its current
moments and localization stress, derive the jump/Kossakowski/Lamb-shift and
growing-sector Davies bounds, and decide whether overlapping sectors or a
different inertia law create a nonempty joint window.

Selected successor model: the massive `SU(2)` Skyrmion collective rotor. This
selection is now partially executable. In the physical-pion-mass convention,
the flat `mu=1` profile gives `b=1.58023676`, `c_M=48.6317632`, and
`c_I=34.3539730`, with numerical baryon, tail, and Derrick checks. Exact fixed-
de-Sitter regularity generically makes the global rigid-rotor inertia diverge
logarithmically at the horizon, so the next source must be a finite supported
worldtube. A parity-even covariant `B_mu S^mu` coupling exists at collective-
worldline level because the dynamical hedgehog orientation solders isospin to
physical spin; no point-local bare-Skyrme-field derivation is claimed. The
prepared state, finite-action derivation of the compressed current, off-center
current deformation, slow-rotation errors, and backreaction remain open. See
`massive_skyrmion_observer_program.md`.

Centered worldtube refinement: a covariant ideal-mirror spherical membrane can
impose `U=1` at `x_w<x_c`, preserving exact `B=1`. The hard-wall profile and
centered Young-Laplace balance are executable. Positive tension alone requires
`x_w<sqrt(2/3)x_c`; for the default `mu=1`, `lambda=0.0025`, `x_w=4` example,
the selected wall tension is positive and the wall mass is subdominant. This is
supplemented below by a conditional adiabatic `l=0` minimum and a no-go for one
simple finite-pinning ansatz. It is not a fully coupled stability,
Einstein-junction, or off-center support theorem.

Reference-sector refinement: the standard fermionic `B=1` rotor is not the
literal integer-spin `L^2(SO(3))` model. Its odd Peter-Weyl sector nevertheless
has the exact right-regular multiplicities and a center-blind density/POVM.
Exact integer-target recovery multipliers and fidelity are now proved, subject
to coherent physical access to the right/isospin register. Fixed Skyrme
parameters fail the growing-cutoff rigid-rotation limit; uniform control needs
`e^2J -> 0`, with all localization and gravity scales recomputed jointly.

Fixed-profile joint-control theorem: for fixed `(mu,lambda,x_w)` and centered
ideal-wall constants, compactness scales as `e^-2` and slow rotation as
`e^2sqrt[(J+1/2)(J+3/2)]`. Their product is coupling independent, so fixed
compactness and slow-rotation budgets permit only finitely many spins at fixed `R^2/G`.
This is a matter-derived conditional obstruction, but it does not exclude
profile-changing double scalings, wall inertia, different sources, or full
Einstein-Skyrme backreaction.

Centered current-moment refinement: given the standard leading collective-
current compression, the centered rigid rotor has exact componentwise signed
dipole zero and an analytic signed second-moment tensor controlled by
`<rho^2>_I`. The default
profile gives `(e f_pi)^2<rho^2>_I=2.19023555`. The absolute first moment is
not zero; the conservative bound is
`M1_abs<=4.93972644 L/(e f_pi)`. Thus the dipole-cancelled Hessian branch is
matter-derived for the centered inversion-symmetric baseline only. Off-center
acceleration induces an `l=1` support problem that can regenerate the dipole.
The executable artifact checks the angular consequences and radial integrals;
it is not an independent Noether-current derivation.

Worldtube stability refinement: Young-Laplace balance is now supplemented by a
finite-difference derivative along the re-solved centered Dirichlet branch.
For the default source, the fixed-tension radial energy curvature is
`E''=0.439906>0`, giving step-converged numerical evidence that the stationary
point is a conditional adiabatic `l=0` local minimum. This is not a validated-
numerics proof or the full coupled wall/profile spectrum. A simple
finite cosine pinning term cannot preserve exact `B=1`: exact topology sets
`F_w=0`, the Robin condition then sets `F'_w=0`, and uniqueness forces the
trivial profile. Its default large-stiffness defect is
`1-B=2.11638e-6/kappa_pin^3+...`. Boundary topological degrees of freedom,
nonspherical stability, and the supported off-center `l=1` solution remain
open.

Complementary successor model: two operationally distinguishable spin sectors
overlap in one worldtube and couple to a fixed-width smeared Bunch-Davies
gradient bath. This removes the nonoverlap premise and makes every collective
charge zero Bohr frequency on fixed irreducible sectors. The proposed first
result cannot use singlet survival: the collective singlet is exactly dark under
the full system-bath Hamiltonian. The non-dark rank-one Choi return projector is
an explicit fixed-task diagnostic whose heat return is `O(1/d)`. It does not
establish all-decoder robustness by itself: every decoder's pulled-back
fidelity witness has trace norm exactly `d`.

The Gaussian spectral factor is now exactly derived from stationary shifted
heat-kernel smearing on optical `H^3_R`. That regulator is quasilocal, and a
Paley--Wiener argument rules out exact Gaussian behavior for compact support.
An explicit double-ball convolution supplies a finite-worldtube replacement
with exact KMS balance, unchanged zero mode, and finite bath moments. Under the
Nathan--Rudner stationary Gaussian-bath hypotheses, adjoining the Choi memory
leaves the three-channel constants unchanged and proves the
ancilla-stable spectral estimate `2Gamma tau+2Gamma^2 tau t`. The collar law
`lambda=O[d^-7/2/sqrt(log d)]` is therefore sufficient for the explicit small
residual budget `epsilon_infinity<=A/d`, giving obstruction `1-A-o(1)` for
fixed `0<A<1`. Matching the heat `O(1/d)` recovery correction is guaranteed by
the stronger sufficient schedule `lambda=O[d^-4/sqrt(log d)]`.

This is not a trace/diamond theorem. The finite-preparation extension now
replaces remote-past preparation by a prescribed amplitude ramp and plateau
burn-in, controlled by an explicit
`Gamma tau log(1+T/(B+T_chi))` term without changing the scaling schedules. A
compact smooth profile and the switching function must still be derived from
the matter action, and direct interactions, operational distinguishability,
lifetime, and joint stress controlled.

A named `C_c^infinity` radial seed and convolution-square prefilter are now
executable. Analytic transform derivatives give profile-specific step-converged
Sobolev values for total support `a/R=0.2`:
`(Q_0,Q_1,Q_2)=(26.6977477290,1.57849600683,0.176766804082)`. The optimized
conditional numerical estimates are
`(G_num,M1_num)=(16.2723018013,1.32407331492)`. In the
small-support UV regime they imply `G_bar=Theta(a^-3/2)`,
`M1_bar=Theta(a^-1/2[log(R/a)]^1/4)`, and the candidate sufficient-cap penalty
`lambda_cap=Theta(a^(5/2)[log(R/a)]^-1/8)`. The `a/R=0.2 -> 0.4` executable effective exponent is
`2.5254`. This is a tradeoff in the sufficient ULE bound, not a necessary
failure theorem. The tight constants are not interval enclosed. Separately,
repeated integration by parts plus rational seed and thermal inequalities gives
the conservative exact-profile upper enclosure
`(G,M1)<=(16863.898481372697,76435.381039140748)`. At `L=4096`, exact
substitution in the symbolic formula is sufficient; the downward-guarded
ordinary-float evaluations are approximately `9.9769e-27` and `1.1022e-28`
for the two declared budgets, not directed interval endpoints. The finite
Simpson sinc sum is not extrapolated to infinity. The spatial
profile is still an engineered external-source prefilter rather than a local
matter current. See `overlapping_qft_davies_program.md`,
`static_patch_worldtube_ule.md`, and `static_patch_smooth_worldtube_ule.md`.

The centered leading Skyrmion current now supplies a separate matter-derived
stationary optical `l=1` form factor. Conditional on the standard collective-
current compression and improved pseudoscalar coupling,
`H_Sky(0)=<3(artanh z-z)/z^3>_I>1`. The default profile gives
`H_Sky(0)=1.003295544733`, hence a `0.660195%` zero-frequency rate enhancement.
Step refinement locates a first simple form-factor zero at `p=275.00922037`.
The hard-wall spectrum is UV finite, but its principal square root contains
`|H_Sky|` and is not `H^2` at a simple zero. Thus the current `Q_2/M_1`
Sobolev-ULE proof route cannot be transferred to this matter spectrum. This is
a route-specific obstruction, not a no-Markov theorem. A prescribed finite
amplitude ramp is now controlled by the generic burn-in theorem once the signed
factor is selected. Off-center deformation, derivation of the ramp from the
action, band-projection control, wall modes, stress, lifetime, and gravity
remain open. See `static_patch_skyrmion_bath.md`.

The scalar signed-factor audit now sharpens that boundary. The published ULE
self-convolution uses `q^2=j`, so arbitrary complex phases are not available,
but a real signed root is. Taking `q_Sky=sqrt(j_0)H_Sky` preserves the physical
spectrum, KMS balance, and Hermitian time symmetry while crossing simple zeros
smoothly. In the fixed-irrep zero-Bohr sector it leaves both the jump amplitude
and the Casimir Lamb shift unchanged. The executable finite-window candidates
are `(Q_0,Q_1,Q_2)=(62.2644668852,2.16015691289,0.168156611337)` and
`(G_num,M1_num)=(29.0705146786,1.51073940540)`. This removes the local root
obstruction. A separate boundary-aware continuum theorem now proves
`H_Sky,H_Sky',H_Sky''=O(p^-5)` and hence global `q_Sky in H^2`; the sharp
coefficient is set by the nonzero hard-wall second jet. The finite radial
quadrature is still not extrapolated to infinity. Rigorous numerical global
norms remain open because the current float shooting code does not interval-
enclose the inertia or the six required third-derivative `L1` norms. See
`static_patch_skyrmion_signed_ule.md` and `static_patch_skyrmion_tail.md`.

The finite-preparation theorem further replaces remote-past factorization by a
factorized pre-switch state, an amplitude ramp `0<=chi<=1`, a stationary
plateau, and burn-in `B`. With effective ramp lead `T_chi`, the ancilla-stable
spectral residual gains the moment bound
`Gamma tau log(1+T/(B+T_chi))`. If `B+T_chi>=beta/Gamma`, only the long-time
coefficient changes by `1+1/(2beta)`, leaving both sufficient coupling
exponents unchanged. The executable reports the bound-level required age
`beta/Gamma_bar`; it does not claim that an unspecified physical preparation
satisfies it, and its default values show that this age can be extremely long.
It verifies mathematical burn-in witnesses for both budgets and exposes the
respective `d^3 log d` and `d^4 log d` age scalings.
This is an adaptation of the Nathan--Rudner proof, not a quoted theorem, and it
does not derive `chi` from the matter action. See
`static_patch_finite_switching_ule.md`.

The off-center kinematic audit now removes another false positive. An exact
optical `H^3` translation of the centered radial vector source mixes the
old-origin `l=1` form only into `l=0+2` at first order, while homogeneity keeps
the parallel-transported auto Kossakowski tensor exactly isotropic at every
translated center. The arbitrary-frequency cross eigenvalues are fixed by
derivatives of `sin(py)/(p sinh y)`; the matter factor cancels from normalized
correlations away from its zeros. Therefore any measured auto polarization
splitting is an intrinsic deformation diagnostic. The physical held-off-center
Skyrmion is not a transvection because the mass, lapse, membrane, and anchor
break that symmetry; its coupled linearized response remains open. The
quadratic-order statement additionally assumes parity-odd smearing,
acceleration as the only new vector, and an angular-momentum-diagonal recentered
bath inner product. The executable audits formulas rather than treating its
constructed isotropic matrix as an independent proof. See
`static_patch_skyrmion_offcenter.md`.

The validated-constants program now closes AU.1 and AU.2 for the prescribed
hard-wall profile. Exact rational intervals prove local existence and
uniqueness, shooting sign, monotonicity, wall slope, and inertia. A 43-cell
positive-radius jet audit plus a regular-origin Volterra-Lie interval-AD proof
certifies all six derivative norms and the exact continuum tail envelope.
AU.3a certifies conservative global moments. Authenticated profile-resolved
AU.3b is complete as a baseline, but its joined tail dominates and gives weaker
`Q` bounds. See
`validated_skyrmion_interval_program.md`.

## Research Theorem AK.2: Spherical Constraint Response

Current statement: for spherical time-symmetric data in areal gauge, the exact
local ratio `q=2Gm/[r(1-r^2/R^2)]` controls positivity of the radial metric factor
and bounds relative `g_rr` distortion by `q/(1-q)`. A nonnegative
concentrated-core construction proves that small wall compactness does not imply
a uniform interior margin.

For the authenticated fixed Skyrmion field, directed cumulative energy replay
gives `H_bulk<=29.246335626859388`. The self-consistent bulk mass equation is
linear with a nonnegative damping coefficient, so the fixed-background
cumulative mass is a supersolution and `alpha H_bulk<1` closes the radial
constraint. The maximum upper cell is internal. At the illustrative
`beta=1/2`, `R^2/G=10^6`, `lambda=1/400`, the sufficient condition is
`e^2>=0.04679413700297502`.

Dependencies: the authenticated sharp profile and origin family, nonnegative
Skyrme energy density, spherical time symmetry, areal gauge, and the fixed field
configuration. The membrane diagnostic uses its fixed-background mass only.

Evidence: artifact SHA256
`a180610fbdea4eecd75cdc7628216adab9289d5561704f60f750f7105fcaca47`.

Replacement gate: add the cumulative collective rotational energy, control the
lapse through `rho+p_r`, solve the self-gravitating field and membrane junction,
and extend beyond spherical/off-center-free data.

## Research Theorem AK.3: Collective Gravity-To-Risk Elimination

Current statement: within the fixed spherical field and leading collective
rotor, a radial budget `q<=beta` implies
`c_M[A]>=(1-beta)c_M[N]` and `c_I[A]<=c_I[N]/(1-beta)`. The wall constraint then
contains positive `e^-2` rest and `e^2<J^2>` rotational terms. AM-GM eliminates
`e`, producing a finite mean-Casimir ceiling and the global risk floor
`R_ref>=1/(16C_max+8)`.

Authenticated directed substitution uses `c_M>=33.833816` and
`c_I<=48.390986`. At `beta=1/2`, `x_w=4`, `lambda=1/400`, and `R^2/G=10^6`, it
gives `<J^2><=16476538.109682929` and
`R_ref>=3.79327245124592e-9`.

Dependencies: fixed authenticated field, spherical radial metric, leading
collective Hamiltonian, and the declared metric budget. The membrane is
excluded. Evidence: artifact SHA256
`7bfb5119a89da2bffbca47a5794e7bbf756f5bc4ea1d1b51877b216ac1a33433`.

Replacement gate: compose the completed static lapse and leading rotational
source bounds with a horizon-regular `l=2` metric response, construct the
collective projector, bound higher-order rotation, and solve or perturbatively
control the rotating Einstein-Skyrme equations.

## Research Theorem AK.4: Static Bulk Lapse Control

Current statement: the exact fixed-field identity
`rho+p_r=A F'^2(1/4+2sin^2F/x^2)` cancels the radial metric factor from the
spherical lapse equation. Authenticated replay gives `D<=43.445333`. Composed
with the sufficient radial bound at `beta=1/2`, the log-lapse drop is at most
`0.7427483053`; the `g_tt` ratio diagnostic is `0.1131949426`.

Evidence: artifact SHA256
`2072131929fd5c9ff70ced4e468aa5dd937cc84cbffe9efd83529cfa6693171b`.
The result excludes rotation, field deformation, membrane lapse matching,
nonspherical stress, and off-center support. It controls the static bulk but
also falsifies any claim that the current default is negligibly perturbative.

## Research Theorem AK.5: Leading Rotational Stress Multipole Fork

Current statement: for the symmetric collective spin second moment
`S_ab=<{J_a,J_b}>/2=C delta_ab/3+Q_ab`, positivity alone gives
`||Q||_op<=2C/3`, `||Q||_F<=sqrt(2/3)C`, and spherical RMS
`||nQn||=2C/(3sqrt(5))` at worst. The leading hedgehog rotational shell energy
is an exact monopole plus `l=2` source, and its integrated absolute quadrupole
energy is at most `E_rot/sqrt(5)`. Spin cats asymptotically saturate the
operator-norm bound.

An explicit pure spin-2 second-order-anticoherent state has `Q=0`, vanishing
mean spin, and full-rank local QFI. It is therefore false that accurate
rotational referencing universally forces a leading quadrupolar gravitational
source. The spherical gravity-to-risk theorem survives through quadratic
collective order on the `Q=0` branch. The all-state branch has a bounded source,
but no metric conclusion until the static-patch `l=2` linearized Einstein
response is controlled in a norm that includes the pressure components.

Evidence: artifact SHA256
`13bfaa681377caef32875a03f9a5c313e7fecb4f17cde5c2e191a8f8810fe07e`.

Replacement gate: the direct rigid-source calculation now fails the exact
conservation test in AK.10. AK.11 supplies the local two-channel Hessian,
rotational source, and membrane boundary law; solve that global `(f,g)` system
before constructing the master source. Then control asymptotically free `Q=0`
families, higher-order rotation, collective projection, and off-center stress.

## Research Theorem AK.6: Stabilizer-Induced Global Risk

Current statement: if `U(h)rho U(h)^*=rho` and `h` has principal rotation angle
`alpha`, pairing the indistinguishable Haar hypotheses `g` and `gh` and solving
the resulting `SO(3)` Procrustes problem gives

```text
R_ref>=sin^2(alpha/4).
```

The explicit spin-2 `Q=0` state occupies only `m=-2,0,2` and is fixed by a
half-turn, so its exact global floor is `R_ref>=1/2`. Its full-rank local QFI
therefore does not make it a globally accurate reference.

Evidence: artifact SHA256
`5043d84e063051e8b730612a096b57dcafda2b30b7614facb0ac95003ff5f54b`.

Replacement gate: construct or exclude an asymptotically accurate `Q=0` family
with trivial or vanishing-angle stabilizer, then control its higher-order
stress and collective projection.

## Research Theorem AK.7: Density-Only Einstein Response No-Go

Current statement: a compact pure-gauge perturbation on an Einstein background
has zero linearized source and arbitrarily scalable coordinate amplitude. In
the local flat limit, the compact conserved source
`T_ij=A(delta_ij Delta-partial_i partial_j)chi`, `T_00=0`, has zero density but
`R^(1)=-16pi G A Delta chi`. Thus neither an unfixed metric norm nor the
energy-density multipole can define the required response theorem.

Evidence: artifact SHA256
`54d4d33642198274f656fc1e87ea631a5b7dead8ec18da4dbfdd58f2d57f7b7c`.

Replacement gate: derive a conserved full stress norm from the deformed
rotating Skyrme-worldtube action and use a gauge-invariant master or curvature
output. AK.9 supplies the exact conservation checker and AK.10 rules out the
undeformed rigid shortcut.

## Research Theorem AK.8: Fixed-de Sitter Static `l=2` Resolvent

Current statement: the Friedrichs static even-parity quadrupole operator
`A_2=-d/dr[(1-r^2/R^2)d/dr]+6/r^2` satisfies `A_2>=6/R^2`. Its exact positive
Green kernel is built from the center solution
`u=15(3-x^2)atanh(x)/(4x^2)-45/(4x)` and horizon solution
`v=(3-x^2)/(2x^2)`. At proper horizon distance `rho`, the diagonal response is
`R log(2R/rho)-3R/2+o(R)`.

Evidence: artifact SHA256
`45871bfe3e15a65b546eddd6391d42d0d8e6665ee981c9f24618409f52dcd051`.

Replacement gate: reduce and solve the AK.11 regular-field `2 by 2` radial
system, then project its conserved bulk-plus-membrane stress onto the master
source, perturb the resolvent around the controlled spherical background, and
reconstruct an invariant physical observable.

## Research Theorem AK.9: Static Even-Stress Conservation Gate

Current statement: on `ds^2=-fdt^2+dr^2/f+r^2dOmega^2`, a static even-parity
stress multipole with amplitudes `(rho,p_r,j,p_perp,pi)` is conserved exactly
when

```text
p_r'+f'(rho+p_r)/(2f)+2(p_r-p_perp)/r-Lj/(fr^2)=0,
j'+2j/r+p_perp-(L-2)pi/2=0,
```

where `L=ell(ell+1)`. Thus `ell=2` and `j=0` require `p_perp=2pi`. Hard
truncation additionally produces delta coefficients `-p_r(r_w)` and
`-j(r_w)`, which must be canceled by wall stress or vanishing traction.

Evidence: artifact SHA256
`ffdd21d1ca7e5c33df825bb7f0ba57b0d816916f34f1ea23e383f804c7299856`.

Replacement gate: apply this checker to a same-action centrifugal matter and
membrane solution, including shell conservation and master-source jump terms.

## Research Theorem AK.10: Fixed-Profile Rigid Source No-Go

Current statement: the complete quadratic rotational stress of the fixed
Skyrme hedgehog has `j=0`, but its quadrupole amplitudes obey

```text
p_perp-2pi=-[k_2+k_4(a^2-2b^2)]q/I^2,
```

which is generically nonzero. Near a nontrivial Dirichlet wall its leading
coefficient is strictly negative. The radial conservation residual is also
generically nonzero, while the direct rigid rotational wall traction vanishes.
No omitted membrane delta can therefore repair the bulk defect.

Evidence: artifact SHA256
`a91577f62a2992f3aca8c7ffe9af171c6c5759a0dcff80550c3dff5240286bfe`.

Claim boundary: this rejects only the undeformed fixed-profile static source.
It does not exclude a conserved centrifugally deformed Skyrmion, a dynamical
gravitational source, or the leading `Q=0` branch.

Replacement gate: AK.11 supplies the local two-channel variational data and
moving-wall Robin law. Reduce and solve its global `(f,g)` boundary-value
problem, verify bulk and shell conservation, and only then perform the Zerilli
projection and invariant reconstruction.

## Research Theorem AK.11: Centrifugal Two-Channel And Wall Gate

Current statement: the equivariant `O(Omega^2)` coordinate deformation splits
into one monopole and a rank-two quadrupole. In regular physical variables the
quadrupole is

```text
delta Y=f q e_F+g(Qn-qn),
f=-x^3F'(A-C),
g=sin(F)x^2C.
```

The profile-only restriction obeys the exact forced Jacobi equation

```text
[-(P f')'+Q2 f]=-4E_H,
```

and its source satisfies `C_rigid,r=-(F'/x^2)E_H`, reproducing AK.10's radial
conservation defect. The exact target-space second variation gives a symmetric
local Hessian in `(f,g,f',g')` and a generically nonzero rotational source in
the `g` channel. The scalar restriction therefore cannot close the independent
angular field equation.

For a moving ideal mirror, `xi2=a^3(A-C)` and the pure-tension normal-force
equation gives

```text
(A-C)'=[N'/(2N)-3/a
        -4sigma(K'+6/(a^2sqrt N))/(N F_w'^2)](A-C).
```

The default Robin multiplier is `-1.0236037233500035`. A movable Nambu-Goto
wall is therefore kinematically capable of balancing the quadrupole; a fixed
spherical wall requires an additional anchor or the generically restrictive
conditions `(A-C)=(A-C)'=0`.

Evidence: artifact SHA256
`5d545c1753dc3fb78c3c05fc2005ef450dd46f346b20788b12ed33ec3697a58d`.

Claim boundary: this is a local variational and boundary theorem. It does not
solve the coupled `2 by 2` radial system, prove its coercivity or global
existence, recompute the conserved completed stress, impose Israel matching,
or produce a Zerilli observable.

Replacement gate: reduce the certified Hessian/source generator to an explicit
self-adjoint radial operator, derive its regular-origin subspace, solve it with
the mirror/tension boundary conditions, and rerun AK.9 on the completed source.

## Research Theorem AK.12: Exploratory Global Centrifugal Branch

Current statement: the AK.11 Hessian/source reduces to the global variational
equation

```text
-(Ay'+D^Ty)'+Dy'+Cy=s0-s1',  y=(f,g).
```

The default origin indicial roots are `p=1,3,-2,-4`; the two regular modes have
`f/g=-1.00000000299` and `0.04172747341`. A block-tridiagonal solve with the
AK.11 moving-wall conditions gives

```text
max|f|=0.3053035319,
max|g|=0.2735765404,
||y||_2^2=0.1952068369,
xi2=-0.2873444807.
```

The finest mesh change is `1.30e-4`, origin-cutoff change `8.45e-6`, and
background-profile step change `1.61e-7`. The algebraic residual is below
`5e-13`.

Evidence: artifact SHA256
`ddc489d4b0b5b3bcbd71fd36afd1b217f58b04c13cbdbb0f2be7ff7df9f95a76`.

Claim boundary: this is unvalidated finite-difference evidence. It does not
prove existence, uniqueness, coercivity, a uniform small-rotation window,
membrane distributional conservation, Israel matching, or a gravitational
observable. AK.13 separately supplies floating smooth-bulk stress closure. Its
main decision consequence is negative: the moderate regular branch makes AK.10
unsuitable as a fundamental no-go claim.

Replacement gate: validate the coupled branch and reconstruct its membrane
surface stress. Apply AK.9 distributionally, then project only the conserved result into
AK.8's master resolvent.

## Research Theorem AK.13: Same-Action Bulk Stress Closure

Current statement: the first Hilbert variation of the static Skyrme stress on
AK.12's `(f,g)` branch, added to the independently derived rigid quadrupole,
supplies all five static even-parity amplitudes. Direct application of AK.9's
certified conservation checker gives completed radial/angular residuals

```text
nodes             101        201        401        801
radial          1.01e-1    3.02e-2    8.36e-3    2.21e-3
angular         3.27e-3    8.20e-4    2.06e-4    5.21e-5.
```

Every mesh doubling reduces both residuals by a factor below `0.35`. At 801
nodes the combined residual is `7.55e-4` of the stable rigid defect.

Evidence: artifact SHA256
`79f588642456d91eb58107de613a639566af0e7924cd29e8d480bf109ecea5db`.

Claim boundary: this is source-hashed floating evidence for smooth-bulk
conservation at one parameter point. It does not prove existence or
coercivity, include the membrane delta source, impose Israel matching, control
collective projection, or construct a gauge-invariant gravitational response.

Replacement gate: derive the moving membrane surface stress and prove
distributional conservation, validate the bulk branch, and project the full
conserved source into AK.8's master resolvent.

## Research Theorem AK.14: Distributional Membrane Completion

Current statement: a shape perturbation of a constant-tension Nambu-Goto shell
generates fixed-coordinate `delta` and `delta-prime` stress amplitudes. Their
exact divergence factorizes into the background mean curvature `K` and the
shape coefficient

```text
k_l=K'(a)+l(l+1)/(a^2sqrt(N_a)).
```

After adding the singular layer from the moved bulk support, all distributional
coefficients reduce to background Young-Laplace balance and the linearized
normal/tangential traction laws. The tangential law follows identically from
the ideal mirror, while the normal law reproduces AK.11's Robin condition. On
the `101`- through `801`-node BVPs, the maximum conservation coefficient is
below `1.19e-12`.

Evidence: artifact SHA256
`1ef92b3579f60fe52d2849d3da3202dc55be33be538b401117218f81cdea53aa`.

Claim boundary: the distributional factorization is analytic, but its default
profile/BVP substitution is floating and fixed-background. No interval
enclosure, exterior matter, elasticity, Israel junction, self-consistent
metric, collective projection, or Zerilli source is supplied.

Replacement gate: validate the coupled matter-wall branch, derive the exact
conserved stress-to-master-source map including shell distributions, and then
perform invariant gravitational reconstruction.

## Research Theorem AK.15: Exact Conserved-Stress Master Source

Current statement: in the frozen Regge-Wheeler and Zerilli-Moncrief
normalization, direct sourced Einstein elimination gives

```text
F=kappa[-r^2N rho'/6+r(1+4r^2/R^2)rho/6
        -r p_r/2-j+2r pi].
```

The executable maps general stress `delta` jets to the literal master
`delta`/`delta'`/`delta''` coefficients and supplies an exactly equivalent
contact-free source for off-wall response. It also records the non-unit
normalization of `q=Q_ab n_a n_b`.

Evidence: artifact SHA256
`3be17612134bb6b72535db9d3c80a74acf1271a39e04eec4b1591c9bd8967887`.

Claim boundary: exact fixed pure-de-Sitter linear gravity in one frozen master
normalization. A sourced Kodama-Ishibashi cross-check, deformed-background
extension, collective normalization, Israel matching, and curvature
reconstruction remain open.

## Research Theorem AK.16: Completed Skyrmion Master Response

Current statement: composing AK.12-AK.15 yields the nonzero 801-node response

```text
psi0=(-0.220896,-0.330207,-0.176182,-0.0662061,-0.0154951)
```

at radii `(1,2,3,5,10)`, per unit dimensionless `kappa_hat` and quadratic
angular-velocity harmonic. The finest mesh, origin, and profile relative
changes are `1.06e-4`, `2.99e-5`, and `2.87e-7`.

Evidence: artifact SHA256
`07c66bb0731588a268db1398f9714746dd43b1e666867d004ee472e525873437`.

Claim boundary: source-hashed floating fixed-background response. Physical
collective units and an exterior electric-Weyl invariant are supplied by
AK.18-AK.19, and AK.20 supplies its instantaneous Jacobi-limit gradiometer
contraction. Interval validation, self-gravity, Israel matching, higher-order
errors, finite-separation/finite-time transfer, readout noise, and detector
backreaction remain open.

Replacement gate: validate the response, impose tensorial Israel matching, and
promote the local Jacobi contraction to a controlled finite-time noisy
detector/worldtube observable.

## Research Theorem AK.17: Exact Ideal-Shell Master Transmission

Current statement: the literal `D0 delta+D1 delta'+D2 delta''` master source
is exactly equivalent to a contact `c=-D2/N_a` plus the off-wall jumps

```text
[Psi_off]=-D1_off/N_a,  [N Psi_off']=-D0_off.
```

Direct two-sided Green limits reproduce both jumps for the completed source.

Evidence: artifact SHA256
`c83536779d2ab62684218291dd99de190569f9973417d9accd2ceff426901ade`.

Claim boundary: this is a master-equation transmission theorem, not tensorial
Israel matching or a finite-thickness membrane limit.

## Research Theorem AK.18: Physical Collective Master Normalization

Current statement: with `I=c_I/(e^3 f_pi)` and
`QJ_ab=<{J_a,J_b}>/2-delta_ab<J^2>/3`, the dimensionless response `psi0`
becomes

```text
Psi_phys=(8piG e^3 f_pi/c_I^2) psi0 QJ_ab n_a n_b.
```

The executable validates a fixed-spin density matrix, uses the same-profile
`c_I`, distinguishes the anisotropic and anticoherent branches, tracks the
hard-support control `epsilon_rot=e^2sqrt[j(j+1)]/c_I`, and returns the exact
tensor angular norm.

Evidence: artifact SHA256
`fc8ae96c6215c4dbe7c8905bbfb59a80cb12cd96e7a3dc9c3849a973174b9470`.

Claim boundary: physically normalized linear master amplitude, not an
Israel-matched metric or operational Weyl/worldtube observable.

## Research Theorem AK.19: Exterior Electric-Weyl Reconstruction

Current statement: in exterior vacuum, the exact RW inverse map is

```text
H0=H2=Psi'+3Psi/r,  K=N Psi'+3Psi/r,
delta E_rr=-6Psi Y/r^3.
```

The completed response is one horizon-regular exterior mode to floating
precision. Combining the curvature identity with AK.18 gives the nonzero
state-dependent physical tidal tensor

```text
E_rr^phys=-(48piG e^6 f_pi^4/c_I^2)
           [psi0(x)/x^3] QJ_ab n_a n_b.
```

Evidence: artifact SHA256
`3025d65fe82585e584150e956de9481380ab3f4a72d26a7cacb744974838c070`.

Claim boundary: exterior, fixed-background, linear, and floating. Tensorial
Israel matching, interval validation, self-gravity, and detector dynamics
remain open.

## Research Theorem AK.20: Equal-Leading-Energy Tidal Discriminator

Current statement: two valid spin-2 density matrices with identical Casimir,
inertia, and leading rigid-rotor energy have

```text
<QJ>_cat=diag(-1,-1,2),  <QJ>_T=0.
```

Using the Jacobi-limit relation `delta[ddot(xi)/xi]=-delta E_rr`, AK.19 gives a
nonzero semiclassical mean gradiometer signal for the cat and zero leading
quadrupolar mean signal for the second-order-anticoherent state. This is an
operational witness that Casimir alone does not fix gravitational disturbance.

Evidence: artifact SHA256
`a0614a2b883ba3604382265f704bad5fd0ff11ad76de895cb28b12765321794e`.

Claim boundary: mean-field, fixed-background, Jacobi-limit, leading-rotor, and
floating. It does not control single-shot fluctuations, finite-time readout,
noise, `Omega^4` energy, validation, self-gravity, or Israel matching.

## Research Gate AK.21: Symmetric Centrifugal Spectral Target

Current statement: the coupled centrifugal Hessian has now been assembled
directly as a symmetric piecewise-linear weak form, with
`f(0)=g(0)=0`, `g(a)=0`, and the Robin-equivalent wall term included in the
quadratic form. This removes numerical derivatives of the Hessian blocks and
makes matrix symmetry exact at assembly level. Nested
piecewise-linear spaces give the lowest generalized Ritz values

```text
0.3536279015, 0.3535118860, 0.3534832456,
```

and the finest weak-form solution agrees with the separately implemented strong-form
solver to `1.32e-4` in the declared scaled probe norm. Because the two solvers
share the Hessian, source, and Robin generators, this is a discretization
cross-check rather than an independent physical-normalization audit. Floating
profile interpolation and quadrature mean that the positive eigenvalue
estimates have no certified one-sided relation to the continuum spectrum.

Evidence: artifact SHA256
`2c8a2b3e4fd961ca87d2dd3cbc036a0ece4c31531c246b8d18d3b72b4b0d8454`.

Replacement gate: compose the authenticated AU.3b profile tube with rational
interval Hessian/source/wall boxes, prove the trace-space/Frobenius origin-domain
equivalence or use regularized origin variables, and close a two-sided matrix
Green-parametrix defect below one with an a posteriori solution residual. The
resulting theorem must give a strict continuum lower spectral bound and an
exterior master-amplitude interval excluding zero.

Claim boundary: source-hashed floating Galerkin feasibility evidence. It fixes
a symmetric weak-form target but is not interval numerics, a proved physical
origin domain, an eigenvalue bound, an Israel theorem, or a validated response.

## Research Theorem AK.22: Exact Coupled-Origin Indicial Factorization

Current statement: exact rational polynomial/Laurent evaluation of the
same-action Hessian at

```text
F=pi-bx+O(x^3)
```

gives `C=C0+O(x^2)`, `M=xM0+O(x^3)`, and `P=x^2P0+O(x^4)`. The indicial pencil

```text
K(p)=-p(p+1)P0-(p+1)M0^T+pM0+C0
```

obeys the exact polynomial identity

```text
det K(p)=det(P0)(p-1)(p-3)(p+2)(p+4),
det(P0)=1/1350+(2/225)b^2+(16/675)b^4>0.
```

Thus the regular powers are exactly `1,3`, the singular powers are `-2,-4`,
and the linear regular kernel is exactly `(f,g)=(-1,1)x`. This replaces the
floating small-radius SVD diagnosis for every real origin slope. Over the
authenticated AU.3b slope interval it also gives an exact leading Robin-matrix
enclosure at `x=1/16`, with maximum entry width below `0.01616`.

Evidence: artifact SHA256
`505437ad55113896aab97fd33307599ef014e0cf1e00d67611ab5634327fe9a9`.

Replacement gate: substitute `g=xv(x^2)` and
`f=-xv(x^2)+x^3u(x^2)` into the full coefficient operator, prove regularity at
the transformed origin, and validate its two-parameter transfer map to the
positive-radius interval mesh.

Claim boundary: exact leading indicial theorem, not a full Frobenius remainder,
Friedrichs-domain equivalence, finite-radius transfer bound, or coupled inverse
theorem.

## Research Theorem AK.23: Exact Transformed-Origin Density Factorization

Under

```text
t=x^2,
F=pi-xw(t),
g=xv(t),
f=x[-v(t)+t u(t)],
```

term-by-term substitution into the complete same-action `K=2` static Hessian
gives

```text
H_static=x^2 H_hat(t),
```

where `H_hat` has no negative power of `t` when written with the entire
profile kernels `sin(sqrt(t)w)/sqrt(t)` and `cos(sqrt(t)w)`. Exact rational
center evaluation gives `H_hat(0)=v(0)^2/6`; direct floating replay of the
untransformed density agrees to `2.61e-18`. The leading rotational Euler source
is exactly `b(1-4b^2)(1,-3/2)/45`, which lies in `range K(3)`. Therefore the
forced particular branch admits a log-free cubic start satisfying
`(10+56b^2)v_t(0)-(4+56b^2)u(0)=b(1-4b^2)`.

Evidence: artifact SHA256
`e4ae895c9aa120da3d87f8a9cbd774a11bd44d056fba1e6b5cae235870dd6568`.

Replacement gate: derive the weighted transformed Euler-Lagrange system from
`H_static dx=(sqrt(t)/2)H_hat dt`, identify its two-dimensional Friedrichs
trace space, and validate its fundamental transfer matrix through
`t=1/256` over the authenticated profile family.

Claim boundary: exact local-density desingularization and leading source
compatibility, not a Friedrichs-domain equivalence, finite-cutoff Frobenius
bound, transfer enclosure, coercivity
theorem, or validated response.

## Research Theorem AK.24: Exact First Post-Indicial Recurrence

For `mu^2=1`, `lambda=1/400`, and the exact profile germ through `x^5`, the
weighted transformed equations determine exact rational-function germs for the
linear homogeneous, cubic homogeneous, and forced particular branches. The
first nonsingular recurrence matrix is

```text
M5=(1/45)[[28+308b^2,-70-392b^2],
           [-22-200b^2,28+176b^2]],
```

and

```text
det M5=-(28/75)(32b^4+12b^2+1)<0
```

for every real `b`. All leading and `p=5` recurrence residuals vanish as exact
rational-function identities. The full leading equation also proves that the
normalized linear mode generally has nonzero `v_t(0)`, a correction absent
from the leading Robin construction.

Evidence: artifact SHA256
`09ac1a8c29675e4dcc4d92f32ddaf6b75d9111563b5e404020db5e01e29551d4`.

Replacement gate: enclose the three exact germs with correlated Taylor-model
remainders over the authenticated slope box and `0<=t<=1/256`, then export the
affine regular boundary subspace directly into the interval BVP.

Claim boundary: exact formal germs through `x^5`, not a finite-cutoff transfer,
Friedrichs-domain theorem, Robin enclosure, coercivity result, or validated
forced response.

## Research Theorem AK.25: Uniform Post-Germ Indicial Inverse Majorant

Over the authenticated AU.3b slope interval, exact rational interval algebra
proves

```text
sup_{odd p>=7} ||K_b(p)^-1||_infinity
  <= 0.07832423329415064 < 79/1000.
```

The powers `p=7,9` are bounded directly. For all odd `p>=11`, the determinant
factorization and a quadratic adjugate majorant give a uniform tail bound below
`0.04638`. Thus the first omitted physical power controls the supremum.

Evidence: artifact SHA256
`55841a2fec100e627f8852c2f5c729e6fc8bd6e49457cff27173c2e120fc03b2`.

Replacement gate: combine this Green constant with correlated interval
majorants for the nonleading operator coefficients and the post-germ source;
close a Neumann/radii inequality for the Taylor remainder on `t<=1/256`.

Claim boundary: a leading indicial inverse theorem, not a variable-coefficient
inverse, remainder enclosure, finite-cell transfer, or continuum response.

## Research Theorem AK.26: Uniform Quintic Origin-Profile Family

The complete authenticated AU.3b shooting interval is covered by 16
contiguous exact rational cells. On every cell, degree-two Taylor-model
arithmetic validates the common quintic-centered profile tube

```text
p=b-3ct-5dt^2+t^3r_p,   |r_p|<=13/10,
u=b-ct-dt^2+t^3r_u,     |r_u|<=13/70,
```

through `t=1/256`. The maximum contraction is below `3/5`, the maximum radii
left side is below `9/10`, and the common remainder radius is `13/10`. The
Volterra denominator remains above `20`, while the cutoff derivative is
strictly negative over the full family.

Evidence: artifact SHA256
`125232b3856d2cf4d17647b90983a4f0a6865ead8149ad07401cbabf5fbb9294`.

Replacement gate: insert this profile tube into the regular conormal Fuchs
system, prove the degree-two field-germ residual is `t^3` times a bounded
source, and close the affine finite-cutoff transfer for both homogeneous
columns and the forced column.

Claim boundary: a uniform nonlinear profile-family theorem, not a field
transfer, Friedrichs trace-space result, continuum coercivity theorem, or
validated tidal response.

## Research Theorem AK.27: Exact Conormal Origin-Transfer Scaffold

The weak-form centrifugal system admits exact conormal variables
`a=y/x`, `p=P y'+M^T y-s1`, and `z=p/x^2`. They give the regular-singular
first-order equation `2tX_t=A(t)X+q(t)` without differentiating the validated
profile remainder. The exact source blocks are

```text
q1=Pbar^-1 shat1,
q2=Mbar Pbar^-1 shat1-shat0.
```

At `t=0`, the four distinct eigenvalues are `{0,2,-3,-5}`. Exact Lagrange
projectors, explicit rational state weights, and 128 exact slope cells prove a
degree-three Green majorant below `9/20`. The formal endpoint data retain two
homogeneous columns and one forced affine column through physical power `x^5`.

Evidence: artifact SHA256
`c10651881cd99ca85c4c1f282092668e6d92597f7f2a785156fdcee1401da7b3`.

Replacement gate: compose the W3z.7 regular blocks with the uniform quintic
profile tube and bound both `delta=sup||A-A0||_w` and
`epsilon=sup||e||_w` in the exact radii inequality. W3z.7 has now discharged
the formal `t^3` divisibility item.

Claim boundary: exact system algebra, leading spectrum, Green majorant, and
formal affine field germ, not a finite-cell field enclosure, Friedrichs
trace-space theorem, continuum inverse, or validated response.

## Research Theorem AK.28: Regular Conormal Blocks And Residual Divisibility

Exact kernel-level cancellation and polarization give

```text
H_static/t=a^T Cbar a+2a^T Mbar d+d^T Pbar d,
C=Cbar,  M=xMbar,  P=tPbar,
```

for `a=y/x` and `d=y'`. The physical rotational source further factors as
`s0=x^3r0(t)` and `s1=x^4r1(t)`, so its conormal source is `O(t)`. Exact origin
algebra reproduces the established indicial block and proves
`A(t)-A(0)=O(t)`.

The exact Euler-to-conormal identity divides the lower residual by one power
of `x`. Since the certified `p=1,3,5` recurrence gives Euler residual
`O(x^7)`, all two homogeneous and one forced conormal germs have residual
`O(x^6)=O(t^3)`.

Evidence: artifact SHA256
`f87766d639f721b6227cab436d394e09f4059741fdbc5a057eba4e379d67f984`.

Replacement gate: add functional Taylor remainders to these exact blocks over
the validated quintic profile family and compute rigorous weighted bounds for
`delta` and `epsilon`; then test the already implemented radii inequality.

Claim boundary: exact regular coefficient/source algebra and formal residual
divisibility, not a quantitative Taylor remainder, finite-cell transfer,
continuum coercivity theorem, or validated forced response.

## Research Theorem AK.29: Validated Finite-Cell Conormal Transfer

The full authenticated slope interval is covered by two exact rational profile
cells. Functional Taylor models propagate the certified `u` and `rho=-F'`
remainders through the regular conormal blocks without any remainder
differentiation. In the explicit weighted norm,

```text
gamma<0.500310,
delta<0.145445,
gamma delta<0.072576.
```

All three affine columns close their exact radii inequalities. Their maximum
remainder radii are below `(887.903,327.961,25.328)` and multiply `t^3`; the
largest endpoint component error in `X=(a,z)` is below `7.73e-5` at
`t=1/256`.

Evidence: artifact SHA256
`7b8be07c712f142f95219057a2348d11e80fbf73fd428d527f96a43257adb5c0`.

Replacement gate: use `y=xa` and
`y'=Pbar^-1(z-Mbar^Ta+shat1)` to export a correlated physical endpoint tube,
identify it with the Friedrichs trace space, and insert it into the global
interval weak-form inverse.

Claim boundary: a validated finite-cell affine conormal transfer, not a direct
physical derivative tube, global continuum coercivity/inverse theorem, or
validated nonzero tidal response.

## Research Theorem AK.30: Validated Physical Origin Transfer

The exact endpoint reconstruction

```text
y=xa,
y'=Pbar^-1(z-Mbar^Ta+sigma shat1)
```

exports each certified W3z.8 conormal column to a direct physical endpoint
tube on both authenticated slope cells. All linear, cubic, and forced formal
centers are contained. Maximum field and derivative widths are respectively
below `0.051139` and `1.394047`.

Evidence: artifact SHA256
`e07d692092df48646f802bb4be4628f81038da641a4c046c1cb446e50cb24399`.

Replacement gate: prove the regular columns span the Friedrichs trace space,
then use these correlated physical tubes as the left boundary data in the
global interval weak-form coercivity and inverse certificate.

Claim boundary: a columnwise physical finite-origin transfer, not a
Friedrichs-domain theorem, global continuum inverse, or validated forced
tidal response.

## Research Theorem AK.31: Local Finite-Energy Solution-Germ Trace

For every exact indicial branch, the leading weak-form energy is
`Q_p(b)x^(2p)` with `Q_p` a strictly positive even polynomial. Hence the local
energy integral is finite iff `p>-1/2`: the `p=1,3` homogeneous modes are
admissible and the `p=-2,-4` modes are excluded. Positivity of the first
nonzero `x^-8` or `x^-4` singular square prevents cancellation between the two
singular powers.

The local finite-energy homogeneous solution trace is therefore
two-dimensional. The forced particular branch begins at `p=3` and is also
admissible; AK.30 supplies the physical endpoint tubes for this exact affine
family.

Evidence: artifact SHA256
`49f08d3471e1402ec29577df77e3caaff25511461950e73daedecce6338b6d87`.

Replacement gate: extend the local solution-germ classification to the
closed global quadratic form, prove global semiboundedness/coercivity with the
moving-wall boundary term, and construct the two-sided interval inverse.

Claim boundary: local solution-germ Friedrichs admissibility, not the full
form domain, global Friedrichs operator, continuum inverse, or validated
nonzero response.

## Research Theorem AK.32: Exact Liouville Coercivity Reduction

For any symmetric multiplier `K`, the global two-channel weak density admits
an exact Picone/Riccati square completion. The explicit choice
`K=sym(M)-P/(2x)` reduces its residual to the regular conormal matrix

```text
W_K=C-sym(Mbar)+Pbar/4-2t sym(Mbar)_t+t Pbar_t
    +Abar Pbar^-1 Abar.
```

The direct and conormal identities have zero exact-rational defects. A trusted
interval kernel evaluates `Pbar` and both Sylvester minors of
`W_K-(1/20)I` from supplied profile jets. The allowed wall trace is separately
positive by exact interval arithmetic. Floating refinements give a stable
potential minimum `0.07863...` and wall margin `0.21427...`; an independent
Riccati construction supplies a stronger fallback candidate.

Evidence: source-hashed route artifact
`experiments/centrifugal_skyrmion_riccati_coercivity_certificate.json`, SHA256
`11c7897eae4f08193e133620b56bdd1fbd5ba71258ab2cbbc9f83d75932377fe`.

Replacement gate: evaluate the assembled potential determinant with a
cancellation-preserving centered Taylor model on the authenticated AU.1
Newton tube. Independent profile jet boxes remain too decorrelated and lose
the margin even under aggressive subdivision. After the minor inequalities
close, prove closability on the smooth weighted core and apply the
representation theorem/Lax-Milgram to obtain the Friedrichs inverse bound.

Claim boundary: exact reduction and trusted conditional checker, not a global
coercivity theorem, continuum inverse, or validated forced response.

## Research Theorem AK.33: Exact-Spline Liouville Minor Certificate

The completed conormal potential has a division-free Sylvester test. For
`Pbar=diag(p,r)`, antisymmetric entry `alpha`, and shifted entries `U,V,z`, set

```text
d1=rU-alpha^2,  d2=pV-alpha^2,  D=d1*d2-prz^2.
```

Centered exact-rational Taylor models preserve the profile correlations while
ranging these assembled quantities on the archived 43-cell AU.1 approximate
profile. One source cell requires one bisection; all 44 resulting cells prove
`p,r,d1,d2,D>0`. The worst exact lower bounds are approximately `0.001145` for
`d1` and `1.1869e-5` for `D`, proving `W_K>=(1/20)I` for that exact spline.

Evidence: source-hashed artifact
`experiments/centrifugal_skyrmion_liouville_spline_certificate.json`, SHA256
`581db1b6a078b5e43a09de17fe450f261d04931f94e52c5a039ea27b468752f3`.

Replacement gate: reconstruct the endpoint-corrected Newton center, propagate
the full correlated AU.1 `C2` tube into `d1,D`, and join the authenticated
origin family. Then prove form closability and obtain the two-sided Friedrichs
inverse before validating a nonzero forced response.

Claim boundary: exact continuum interval coercivity on the supplied
positive-radius approximate spline, not the exact nonlinear Skyrmion, full
origin-to-wall form, global inverse, or physical response.

## Research Theorem AK.34: Outer Newton-Tube Liouville Certificate

The exact-spline `1/20` target fails under the current authenticated `C2` tube,
so the certified target is reduced rather than hidden. On the full AU.1
nonlinear tube outside `x=3/16`, exact-rational Taylor models prove
`W_K>=(1/100)I`. The worst division-free determinant lower bound is
`5.629318349e-7`; 31 source cells require 45 validation cells and refinement
depth at most two.

The same audit proves that the regular nonlinear Volterra family extends to
the split radius `3/16` for every authenticated shooting slope, with
contraction upper bound `0.916612582057544892`.

Evidence: source-hashed artifact
`experiments/centrifugal_skyrmion_liouville_outer_tube_certificate.json`,
SHA256
`c8744dd4136b607595a42de1ada271644c8408b0fff6b4a2629bf749ea136b91`.

Replacement gate: evaluate the completed Liouville potential in regular
origin variables on `[0,3/16]`, using the nonlinear profile equation to avoid
an independent `F''` box. Join the weighted cores and apply the representation
theorem; the resulting candidate inverse norm is `100`, not `20`.

Claim boundary: authenticated outer-tube coercivity and inner-family
existence, not inner coercivity, a global closed form, inverse, or response.

## Research Theorem AK.35: Regular-Origin Liouville Certificate

The exact regular variables `t=x^2`, `u=(pi-F)/x`, and `p=-F'` remove the
origin singularity without differentiating the Volterra remainder. The
nonlinear profile equation supplies `p_t`; entire kernels supply the remaining
conormal derivatives. A four-variable mean-value enclosure ranges the fully
assembled division-free minors over the authenticated `R=8` origin family.

On 64 time/slope cells it proves `W_K>=(1/100)I` for `0<=x<=3/16`, with
minimum first minor `0.658684620946269` and scaled determinant
`0.0670614628308156`. The origin contraction is below `0.901`.

Evidence: source-hashed artifact
`experiments/centrifugal_skyrmion_liouville_origin_certificate.json`, SHA256
`daa220e68ceef034a1b23ea955033dc08c0e776ee49628eb07acb0834b57c065`.

Replacement gate: construct the common weighted form domain, prove smooth-core
density and closability across the artificial split, include the certified
wall trace, and apply the representation theorem. Then validate the forced
response with the honest inverse constant `100`.

Claim boundary: full origin-to-wall coefficient inequalities, not the closed
form/operator theorem, inverse, or physical response.

## Research Theorem AK.36: Global Centrifugal Friedrichs Inverse

The common weighted form domain is
`V={y in L2: y in H1_loc((0,4]), x y' in L2, g(4)=0}`. Origin cutoff and
mollification prove density of the smooth wall-constrained core without
imposing a center trace. The completion trace vanishes at the center because
`K=x Kbar`, and local `H1` regularity prevents an interface defect at the
certificate split.

The authenticated inner and outer `W_K>=(1/100)I` inequalities, uniform
principal positivity, and positive wall trace make the completed-square norm
equivalent to `||y||2+||x y'||2`. The form is therefore closed and its positive
self-adjoint representation operator satisfies `||A^-1||<=100`.

Evidence: source-hashed artifact
`experiments/centrifugal_skyrmion_friedrichs_form_certificate.json`, SHA256
`4a4e3ecd48a205860de3aa045c94d2b825c0afce1c0f12f4b96254db355b85bb`.

Replacement gate: validate `A^-1 s` and prove that a physical response
functional excludes zero using the honest inverse constant `100`; only then
compose the matter response with tensorial Israel matching.

Claim boundary: a closed fixed-background matter-plus-moving-membrane
operator and two-sided `L2` inverse, not compact resolvent, a kinetic mode gap,
a validated `V*` response, or a backreacted Einstein-matter solution.

## Research Theorem AK.37: Nonzero Centrifugal Weak Response

The exact regular source has tangential origin coefficient
`s_g/x^3 -> b(4b^2-1)/30`. The authenticated slope interval is strictly above
`1/2`, and its exact coefficient lower bound exceeds `0.4680670530`. The
derivative-load coefficient vanishes at both endpoints, so the rotational
load has a nonzero `L2` representative as well as defining an element of the
weighted form dual.

The global coercive form gives a unique weak solution. It cannot vanish, and
the source-conjugate susceptibility satisfies `ell(y)=q[y]>0`.

Evidence: source-hashed artifact
`experiments/centrifugal_skyrmion_forced_response_certificate.json`, SHA256
`9edc2bc479534fab3f527ce535a373da1373b45085c6fbf4602f4ee9cdd32db7`.

Replacement gate: construct a quantitative primal-adjoint residual enclosure and prove
that an off-wall Zerilli/electric-Weyl response functional excludes zero.

Claim boundary: nonzero matter deformation and positive conjugate
susceptibility, not a numerical field or gravitational-observable interval.

## Research Proposition AK.38: Exterior Adjoint Product Enclosure

The exterior Green kernel factorizes, reducing every off-wall master and
electric-Weyl sample to `A_ext=J_rigid+B(y)`. The exact bulk-density endpoint
cancels its contact-free shell counterpart, leaving an explicit `V*`
functional `B` including the physical wall trace.

For conforming primal and adjoint trials, the corrected estimator obeys

```text
|A_ext-J_hat|<=delta_y delta_z.
```

The exact-rational interval composer is implemented and tested. A source-hashed
`41 -> 81` nested-Galerkin audit gives corrected amplitude `-0.002818947812`,
residual product `0.0000450997164`, and a positive zero-exclusion margin
`0.002773848096` relative to the assembled fine system.

Replacement gate: implement interval affine stress/observable kernels,
rational `C1` primal and adjoint trials, origin/outer residual ranging, and
outward residual-square integration.

Claim boundary: exact reduction and certification theorem with favorable
floating margins, not a completed physical response certificate.

## Research Theorem AK.39: Tensorial Israel Promotion Gate

The spherical Israel equations for a positive constant-tension shell reduce
to equal principal jumps

```text
[K_t^t]=[K_theta^theta]=-kappa sigma/2.
```

This proves that the current identical-de Sitter inner/outer background cannot
itself be an exact nonzero-tension junction. An exact de Sitter/Kottler family
with `1/3<a^2/R^2<2/3` closes both equations and provides a nontrivial sign,
normal, and trace benchmark. After that background match, the nonspherical
constant-tension problem requires continuity of three first-form and three
mixed-extrinsic-curvature harmonic amplitudes pulled back to the displaced
shell. The existing scalar master transmission is necessary but cannot imply
all six conditions.

Evidence: source-hashed artifact
`experiments/israel_junction_gate_certificate.json`, SHA256
`d2c7f542490966c51d37b2d10db45efb4f4c746ac696d5996df1a9b16c29a950`.

Replacement gate: solve the spherical Einstein-Skyrme/Kottler junction,
reconstruct the interior and exterior `ell=2` metrics including constraint
components, pull them back to `r=a+xi Y`, and certify the six tensorial
residuals together with the master transmission limit.

Claim boundary: an exact no-go and promotion criterion, not an Israel-matched
Skyrmion or deformed-background response.

## Research Proposition AK.40: Affine And Origin-Regular Master Kernels

The completed stress and smooth master source are now evaluated as one
cancellation-preserving generic-scalar affine map. The source coefficients in
`(f,f',f'',g,g')` come from an analytic first radial jet of the energy density,
not finite differences or numerical basis extraction. Exact rational,
interval, and centered Taylor-model tests agree with the earlier floating
stress conventions.

In regular variables `t=x^2`, `g=xv`, and `f=x(-v+tu)`, all apparent origin
denominators cancel and `F_master=x F_hat(t)`. The regular factor is affine in
the six field jets through second time derivatives and is defined directly at
the center. The exact physical center relations make all its leading affine
coefficients vanish.

The moving-wall/contact-free map uses the same generic-scalar layer. It keeps
`-1/F'(a)` distinct from `gamma_B` and performs the bulk energy endpoint
cancellation directly, making the non-`f(a)` effective wall coefficients
exactly zero under interval arithmetic.

Evidence: source-hashed artifact
`experiments/centrifugal_affine_master_kernel_certificate.json`, SHA256
`75e2cb77b675d6a6f69b2b9dfe26c527eda5bb475712e03ba5d1170353d08b70`.

Replacement gate: evaluate the archived rational primal/adjoint trials using
authenticated origin jets and centered outer coefficient models, integrate
outward-rounded residual squares, add the wall and adjoint loads, and combine
them through the W3z.17 product theorem.

Claim boundary: local validated algebra only, not a continuum response
certificate or a separated-from-zero Weyl observable.

## Research Theorem AK.41: Finite-Time Tidal Detector Transfer

The same isotropic heat exposure attenuates the rank-two tidal quadrupole as
the cube of the rank-one orientation multiplier. Double integration of the
constant-rate mean Jacobi acceleration gives the exact kernel

```text
K_2=T/(6gamma)-(1-exp(-6gamma T))/(36gamma^2),
```

including its zero-rate limit and endpoint bounds. A declared additive
Gaussian displacement readout then gives an exact equal-prior discrimination
error. This supplies a plug-in map from a future Weyl interval to finite-time
signal-to-noise and error probability.

Evidence: source-hashed artifact
`experiments/finite_time_tidal_detector_certificate.json`, SHA256
`9c72f7cd75f4d1d542fb9bfd08a907f2b31e42a1e55e07f6eecb557c9571e7be`.

Replacement gate: derive the Weyl amplitude, diffusion rate, detector noise,
finite-separation control, and detector backreaction from a common local
model, then propagate their intervals through the monotone kernel.

Claim boundary: exact heat/Jacobi/Gaussian composition, not a one-action
experimental prediction.

## Research Proposition AK.42: Validated Positive-Radius Response Residual

Authenticated positive-radius profile jet boxes can now be converted directly
into interval strong-form coefficient and rotational-load boxes. Exact
rational piecewise-`C1` trial polynomials are checked for contiguity, internal
joins, and the essential wall trace, then integrated through rigorous
cellwise `L2` residual-square bounds. A separate radial conormal wall residual
composes with the global `1/100` coercivity and positive wall margin to produce
the energy-dual norm required by W3z.17.

The bound cannot silently omit cells or internal distributions: callers must
supply the exact residual domain and assert the independently verified absence
of interface delta terms.

Evidence: source-hashed artifact
`experiments/validated_centrifugal_response_residual_certificate.json`, SHA256
`a799baab37215f5095d073880b95ed2025fd55f1fa89f5f0c47174d256998155`.

Replacement gate: use the archived AK.44 primal and adjoint splines with
centered subdivision or Taylor-model coefficient enclosures, feed their
regular center data through AK.43, represent the adjoint master load, and
compose both dual bounds and the exact wall trace through W3z.17.

Claim boundary: validated positive-radius residual infrastructure, not the
physical residual values or a nonzero exterior-amplitude interval.

## Research Proposition AK.43: Cancellation-Safe Origin Response Residual

The regular center variables `t=x^2`, `g=xv`, and `f=x(-v+tu)` reduce the
physical strong residual exactly to `r=x Rhat(t)`, with `Rhat` assembled from
the regular conormal blocks and their first `t` jets. The validator ranges
`Rhat` directly and certifies the weighted origin contribution

```text
integral_0^x0 |r|^2 dx
 <= x0^3/3 sum_i sup |Rhat_i|^2.
```

It then joins that contribution to the positive-radius residual cells and
applies the already certified coercivity and wall-trace lift. No reciprocal of
an origin-containing interval is formed.

Evidence: source-hashed artifact
`experiments/validated_centrifugal_origin_response_residual_certificate.json`,
SHA256
`e48c93dd6e5057629632cae8d8463ad496f17ebc758068cee87e1b837c4e96fa`.

Replacement gate: construct authenticated `t`-jet boxes for the physical
profile at the origin, evaluate the archived AK.44 rational primal and adjoint
`u,v` trials, verify the conormal traces at the outer join, and use the composed
residual product to exclude zero from the exterior amplitude.

Claim boundary: exact cancellation-safe residual infrastructure, not the
physical residual values or a nonzero response interval.

## Research Proposition AK.44: Exact Rational Response Trial Archive

The default floating primal and master-adjoint Galerkin solves now generate
exact rational cubic-Hermite trials on the `43` authenticated sharp-profile
cells. Shared endpoint jets are rounded once, so every positive-radius join is
exactly `C1`, `g(4)=0` exactly, and separate regular-origin linear `u(t),v(t)`
polynomials reproduce both fields and both physical derivatives at `x=1/16`.
The serialized primal-adjoint archive round-trips exactly.

Compact half-period reduction, outward coefficient rounding, and exact
eightfold restriction prove the positive-radius primal residual square upper
bound `3.3197692493413107`, improving the former whole-cell result by more than
four orders of magnitude. It remains too broad for a useful energy-dual
estimate. The adjoint residual is not evaluated because the interval master-
functional load has not yet been represented.

Evidence: source-bound artifact
`experiments/centrifugal_skyrmion_rational_response_trials.json`, SHA256
`9dd83028d00b55c85d280087a696884338941b6602e3f9148a41d524f5ace921`.

The authenticated endpoint blocks and pure-tension Robin law additionally
give a primal wall mismatch inside `[-0.001101145,0.001420521]` with wall trace
margin above `0.2018`.

Replacement gate: add centered correlated outer coefficients and the interval
bulk adjoint load, then evaluate W3z.17 using the exact AK.46 interface
cancellation and AK.47 wall load.

Claim boundary: exact conforming trials and a convergent subdivided outer
primal diagnostic, not tight full-domain residuals or a nonzero gravitational
observable.

## Research Proposition AK.45: Authenticated Origin Profile Jets

Exact identities replace the invalid operation of differentiating the
quintic family remainder. The correlated relation `rho=u+2t u_t` supplies
`u_t`; a division-free Volterra factorization through entire centered sinc
quotients supplies `rho_t`. Two rational slope cells cover the full
authenticated AU.3b origin family and propagate to all regular conormal
profile kernels and first `t` derivatives.

For the archived physical trials this proves

```text
primal origin residual L2^2 <= 0.000021330073298636,
adjoint-shaped zero-load operator action L2^2 <= 0.000000002466925854.
```

Evidence: source-bound artifact
`experiments/validated_centrifugal_origin_profile_jets.json`, SHA256
`7924fb7da3bb96e92fb43f68cf9311b9ac9a6077292e69474fccf5579abab504`.

Replacement gate: represent the adjoint origin load, combine with centered
outer residuals and the certified wall data, and evaluate the W3z.17 product
interval using AK.46.

Claim boundary: authenticated origin primal residual and homogeneous
adjoint-shaped action, not a loaded adjoint residual or zero exclusion.

## Research Proposition AK.46: Exact Conormal Interface Cancellation

The conormal `p=M(x,F,F')^T y+P(x,F,F')y'` depends only on the first jets of
the profile and trial. The authenticated sharp cells restrict one global `C1`
profile, while the exact primal and adjoint archives are global `C1` trials,
including the origin join. Their one-sided conormal values therefore agree
identically at every internal interface. The cellwise strong residual has no
omitted delta distributions.

Evidence: source-bound artifact
`experiments/centrifugal_conormal_interface_certificate.json`, SHA256
`1ee677788edc45190c9b164c45bc4a76a1b9e395d172f12b5aa13241748200e2`.

Claim boundary: structural cancellation of interface distributions, not a
bulk or wall residual magnitude.

## Research Proposition AK.47: Validated Adjoint Wall Master Load

Exact rational `atanh(1/5)` enclosures give the physical wall Green weight and
derivative. Centered Taylor arithmetic retains the correlation between the
authenticated wall slope and its reciprocal displacement law, proving
`gamma_B` lies in `[0.002688103336731132,0.002834701713361219]`. The archived
adjoint's loaded wall mismatch is below `0.00634`, and hence below `1/150`.

Evidence: source-bound artifact
`experiments/validated_centrifugal_wall_master_load.json`, SHA256
`ee73b3527750f91bcb2ed585df3d1d58376cbe0f4ff8db47919356872a86ed42`.

Replacement gate: represent and enclose the bulk adjoint master load, combine
it with the origin and outer adjoint trial, and evaluate the W3z.17 residual
product with a tight centered primal enclosure.

Claim boundary: adjoint wall load and wall residual only, not a bulk adjoint
residual or a nonzero exterior response interval.

## Research Proposition AK.48: Validated Weak Adjoint Bulk Load

Exact integration by parts converts the exterior master functional to
`B_bulk(v)=integral(b0 dot v+b1 dot v')`, whose coefficients use only the
authenticated profile value and first derivative. A positive-series Green
enclosure and the `344`-cell replay certify the functional on both archived
trials and the weak adjoint residual coefficients. Their componentwise maxima
are `0.012136` for the test-value term and `0.009195` for the test-derivative
term.

Evidence: source-bound artifact
`experiments/validated_centrifugal_adjoint_bulk_load.json`, SHA256
`3db6d390d521494d192c5df6b4bc5dfd1ee09f6d441f0bd69c3be2d18add44f5`.

Replacement gate: construct a direct `V*`/Riesz lift for the derivative-test
coefficient, add the regular-origin master load, and combine it with AK.47 and
the centered primal residual in W3z.17.

Claim boundary: positive-radius coefficient-level weak residual, not an
energy-dual adjoint norm or zero exclusion.

## Research Proposition AK.49: Centered Correlated Primal Residual

A single centered subcell coordinate now drives the exact corrected profile
spline, archived primal trial, all required derivatives, trigonometric kernels,
and the assembled strong conormal residual. Newton-tube uncertainty remains as
rigorous interval remainders. This lowers the `43`-cell positive-radius primal
residual square bound from about `328.1385` to
`0.010027698207072146`, an improvement greater than `30000`.

Evidence: source-bound artifact
`experiments/validated_centrifugal_correlated_residual.json`, SHA256
`814da74d5c21cf96b45e9967dd5b8d297d90480a46c3f3ae7fd82ba3ffaad3e7`.

Replacement gate: retain the generating Newton graph/slope correlation or add
a residual correction so the remaining interval remainders fit the W3z.17
zero-exclusion budget; direct energy-dual lifting of AK.48 remains parallel.

Claim boundary: outer primal bulk residual only, not a useful full-domain dual
norm or a nonzero gravitational observable.

## Research Proposition AK.50: Direct Partial Adjoint Form-Dual Bound

The nonzero derivative-test coefficient is lifted in the Liouville completed-
square norm rather than mislabeled as an `L2` strong residual. The authenticated
`344`-cell positive-radius calculation plus the loaded wall trace gives

```text
partial squared dual upper = 0.592007476516919181,
partial dual norm upper    = 0.769420221021594403.
```

The wall is negligible at this scale. The adjusted bulk value coefficient on
`[1/2,67/128]` dominates, identifying the next correlation target.

Evidence: source-bound artifact
`experiments/validated_centrifugal_adjoint_energy_dual.json`, SHA256
`500e56b5aa36c64846100dc59a7383b2051a12c6676fcf8e6d49574f61142d0e`.

Replacement gate: preserve radial/profile/trial correlation in the adjoint
weak load and completed-square multiplier, then add the regular-origin master
load. Do not interpret the current partial upper bound as a no-go.

Claim boundary: positive-radius plus wall only, not a full loaded adjoint norm
or response interval.

## Research Corollary AL.1: Fixed-Profile Observer Capacity

Current statement: the fixed-profile compactness/slow-rotation invariant and
the sharp half-integer fusion theorem imply a finite odd-sector cutoff and a
strictly positive global orientation-risk floor. The same record keeps areal,
proper, and optical support distinct. The conclusion is invariant under the
`e`/`f_pi` co-scaling that preserves the dimensionless profile.

Dependencies: a fixed centered hard-wall `(mu,lambda,x_w)` profile; its mass
and inertia constants; rigid projective collective quantization; declared
compactness and slow-rotation budgets; fixed `R^2/G`. The time-dependent
corollary additionally assumes isotropic rotational heat flow.

Evidence: exact algebraic coupling elimination, the exact projective
hard-cutoff risk formula, and authenticated directed mass/inertia substitution.
The current sharp replay gives `J<=352` and
`R_ref>=1.9689304688982673e-5`; total mass includes the ideal shell, while
inertia is interior only and omits wall inertia.

Replacement gate: derive the compactness and diffusion budgets from the same
supported Einstein-matter action. Profile-changing double scalings and wall
inertia remain outside the theorem.

A separate AU.0b checker now proves conditional existence, uniqueness, and an
endpoint enclosure across one positive-radius nonlinear cell by exact Picard
containment. Its initial interval is not derived from the origin theorem, so it
does not upgrade the default floating profile or discharge AU.1.

## Research Theorem AR: Exact Continuum Tail

Current statement: for an exact nontrivial regular hard-wall branch, endpoint
jets and three boundary-aware integrations by parts imply the sharp `p^-5`
form-factor tail and global signed-factor `H2` membership.

Dependencies: existence of the exact regular branch, its nonzero wall slope,
and finiteness of the six analytic third-derivative norms. No floating endpoint
number is used to prove membership.

Evidence: analytic endpoint expansions and the explicit half-interval envelope
in `static_patch_skyrmion_tail.py`.

Replacement gate: retain the authenticated AU.1-AU.3 provenance and sharpen the
tail/product constants before using a normalized ULE cap in a physical test.

## Research Certificate AR3: Authenticated AU.3b Baseline

Current statement: exact replay of the sharp Newton tube, directed normalized
inertia measure, and profile-resolved finite band through `P=64`, joined to the
AU.2 tail at the same split, proves

```text
(Q0,Q1,Q2)<=(17526.908442,53893.636849,242992.970718).
```

Dependencies: authenticated AU.2 archive and sharp snapshot; dimensionless
radius normalization; one positive-radius subdivision per parent cell; two
origin cells; exact ordered summation. The bare spectral product uses
absolute-value bounds and the joined tail uses the conservative AU.2 ledger.

Evidence: artifact SHA256
`bc6cf2ea21f44c122001fcc3f7fa6cffb9983d4ec4e35591323aa2d29b25c529`,
with all recorded source hashes rechecked. The tail supplies more than `99.2%`
of each squared global bound, making the result weaker than AU.3a.

Replacement gate: sharpen the tail and bare-product enclosures, then introduce
physical units and nonzero timing/lifetime constraints. The present result is a
pipeline certificate and overestimation diagnosis, not a physical no-go.

## Conditional Normalized Skyrmion ULE Caps

Current statement: the authenticated AU.3b moments imply exact centered,
prescribed-switch residual upper bounds in ancilla-stable state operator norm
and normalized coupling upper caps for the declared fixed-spin calculation.

Dependencies: dimensionless radius/time normalization; stationary quasifree
bath; exact collective projection; prescribed switch; caller-declared coupling
reused by construction; external digest claims checked only by the enclosing
global audit.

Evidence: the enclosing artifact records upper coupling diagnostics
`2.2726264072637708e-21` and `8.553142313899728e-23`. It supplies no positive
coupling lower bound, so the reported nonempty intervals begin at zero and are
automatic.

Replacement gate: derive units, coupling, observation/preparation lower bounds,
projection and access errors, stress, lifetime, and gravity from one total
model. Do not present these normalized caps as a physical observer window or a
diamond-norm channel theorem.

## Research Theorem AS: Finite Preparation

Current statement: a prescribed bounded amplitude ramp, stationary plateau, and
burn-in add `Gamma tau log(1+T/(B+T_chi))`; the two coupling exponents survive
when the required effective age is imposed.

Dependencies: stationary Gaussian/quasifree bath, pre-switch factorization,
finite moments, zero-Bohr unital dynamics, and the Appendix-C speed estimate.

Evidence: the retained chain-rule term, direct finite-burn-in witnesses for both
budgets, and the `d^3 log d` / `d^4 log d` age audits.

Replacement gate: derive `chi` from the finite worldtube action and prove the
certified lifetime exceeds the displayed preparation age.

## Research Theorem AT: Translation Versus Deformation

Current statement: optical homogeneity and parallel transport make pure active
translation auto-isotropic at every order; the old-origin first variation is
`l=0+2`, and arbitrary-frequency two-center correlations are explicit.

Dependencies: a smooth centered source, conformal optical homogeneity, and
parallel-transported frames. The quadratic held-source statement additionally
uses parity-odd smearing, acceleration as the only new vector, and angular-
momentum diagonality about the recentered worldtube.

Evidence: stable exact-coordinate finite differences, independent derivative
finite differences, large-distance zero-frequency reduction, and the analytic
homogeneity argument.

Replacement gate: specify an anchor/boundary action and solve the coupled
matter-membrane response before quoting deformation coefficients.

## Research Infrastructure AU.0: Rational Intervals

Current statement: exact rational arithmetic and analytic series remainders
provide a floating-transcendental-free substrate for the profile checker.

Dependencies: Machin's identity, Taylor's theorem with bounded derivatives,
the positive `atanh` series, and exact rational bisection.

Evidence: nested interval refinement, trigonometric identity containment,
an ordered nonnegative square-root bracket, and source inspection excluding
transcendental math imports. These are consistency checks supporting the
analytic remainder arguments, not an independent proof of them.

Replacement gate: AU.1 must validate the selected global nonlinear BVP
certificate. AU.0 alone is not evidence for the default Skyrmion profile.

## Research Infrastructure AU.0b: Conditional Picard Cell

Current statement: for every exact initial point in the packaged rational box,
the curved Skyrmion first-order system has a unique solution across the
displayed positive-radius cell, stays in the declared tube, and ends in the
returned rational endpoint box.

Dependencies: exact interval trigonometric enclosures, strict Picard-image
containment, and positivity of radius, lapse, and the nonlinear denominator.

Evidence: independently recomputed vector-field boxes, strict containment
margins, endpoint monotonicity, and rejection of an undersized tube.

Replacement gate: connect the certified origin-family boundary data to the
selected global residual/Newton certificate. This isolated cell is not a
profile-existence argument.

## Research Infrastructure AU.0c: Uniform Origin Family

Current statement: for every real slope in the complete rational shooting
interval, the exact nonsingular Volterra map is a contraction and self-map on
a common parameter-dependent cubic weighted ball through `x=1/16`. Each fiber
has a unique fixed point in its ball, the reconstructed origin solution depends
continuously differentiably on slope, and the full family has one direct cutoff
box with explicit `O(x^5)` profile and `O(x^4)` derivative errors. Exact
intervals now enclose both cutoff derivatives `Phi_b` and `Gamma_b`.

Dependencies: the exact `t=x^2`, `pi-F=xu(t)` regularization; entire-series
bounds for `sin(sqrt(w))/sqrt(w)` and `sin(2sqrt(w))/(2sqrt(w))`; and the
recomputed radii inequalities `A_2+K_2R<=R`, `K_2<1`.

Evidence: the uniform inequality closes at `R=13/10`, formal rational-function
arithmetic proves the two center-coefficient identities exactly, the cutoff
derivative is strictly negative, and both a weak radius and a broad interval
whose endpoints pass separately are rejected. Differentiated entire-kernel
tails and the implicit contraction bound give negative, finite `Phi_b` and
`Gamma_b` intervals without endpoint finite differences.

Replacement gate: use these origin values and derivatives in the global
augmented BVP boundary residual and scalar Schur certificate.

The parameterized contraction has also been differentiated twice with exact
second-order interval AD. It proves `C2` dependence and the cutoff enclosures
`Phi_bb in [-0.00013757,0.00029385]` and
`Gamma_bb in [-0.01350569,0.02100685]`. These bounds supply the nonlinear
origin-lift constants required by the Newton radii polynomial.

## Research Infrastructure AU.0d: Conditional Taylor Track

Current statement: for a supplied positive-radius initial box, exact defect and
state-Jacobian recomputation validates two chained normalized-polynomial cells.
Each cell satisfies componentwise self-map inequalities and a weighted
contraction bound below one, so every exact initial point has a unique enclosed
solution through the track.

Dependencies: the AU.0 interval/trigonometric substrate and positivity of the
radius, lapse, and nonlinear denominator on every correction tube.

Evidence: an exact zero-solution cell, a nonlinear two-cell track, independent
floating finite-difference diagnostics for both Jacobian entries, and rejection
of a shifted center and a mesh gap.

Replacement gate: AU.0d remains a trusted local checker and diagnostic. The
wall theorem now uses the global residual/coercivity route selected in AU.0e.

## Research Infrastructure AU.0e: Continuation Route Audit

Current statement: the untrusted Hermite generator can produce long sequences
whose every cell is accepted by AU.0d, but the constant-radius interval state
representation wraps too rapidly for the wall proof. Both point endpoints
reach `x=1/4`; the lower track toward `x=1/2` stops at `603/2048` with derivative
radius about `16.788`.

This is evidence against one certificate representation, not a theorem against
validated IVP methods. The approved replacement is a global residual BVP
certificate. Its floating Jacobi probe has `lambda_1 approximately 7.16556`,
Schur complement approximately `2.95967`, and the rational comparison
`v=8/[(x-33/16)^2+4]` has sampled Barta quotient at least `1.62749`.

Replacement gate: exactly validate the deliberately weaker Barta quotient
lower bound `1`, the augmented residual and Schur complement, and a nonlinear
Newton radius. Exploratory spectral values are not profile evidence.

## Research Infrastructure AU.0f: Conditional Global-BVP Coercivity Machinery

Current statement: an untrusted generator constructs exact-rational,
globally `C2`, degree-five Hermite proposal splines on `[1/16,4]`, with
recomputable Bernstein jet boxes, nonlinear residual boxes, boundary
residuals, separate shooting and fundamental Jacobi proposals, and their exact
rational wall-zero combination. It makes no proof claim. The default `1/16`
mesh has whole-cell nonlinear residual bound about
`15.74`; four exact centered subcells per spline cell reduce it to about
`2.407`, still too broad for Newton closure.

A separate trusted checker recomputes the Jacobi coefficients and fixed Barta
quotient from exact jet boxes. On five independent conditional boxes near the
limiting region it proves `P>0` and the certified lower bound
`(Lv)/v >= 1.464502640726474651 > 1`.

The trusted checker also validates a complete exact rational polynomial
spline: it verifies contiguity and global `C2` joins, adaptively recomputes the
jet boxes, and proves a whole-domain quotient lower bound above `1.502908`, and
therefore above `3/2`, on 207 accepted leaves. Maximum extra subdivision depth
is five.

Claim limit: the whole-domain theorem concerns the exact approximate spline,
not an unknown solution of the nonlinear hard-wall BVP. AU.0f therefore
validates the global coefficient/coercivity component, not profile existence.

Replacement gate: produce a globally linked profile tube with a centered
residual enclosure, preserve the Barta margin on the whole tube, exclude the
scalar Schur interval from zero, and close the nonlinear Newton radius.

The trusted conditional Schur audit now exists for the exact approximate-spline
operator. It independently applies the origin-value lift, recomputes the
homogeneous residual, derives the elementary derivative-trace correction from
the same Barta cells, and rejects the representative candidate. At 16 centered
subcells the auxiliary residual enclosure is still about `9.42746`; a
64-subcell probe remains about `7.40831`. A diagnostic using the certified
`alpha>1.5029` margin and sampled coefficient
scales shows that the generic `C1` route would require roughly `4.39e-3` for a
nonzero scalar margin. This negative audit rules out brute subdivision as the
primary closing strategy; the replacement gate now specifically requires a
combined polynomial/Taylor residual and an independent trace representer.

The combined residual machinery is now executable. It proves containment for
the exact five-harmonic numerator representation and materially reduces the
old independent-box wrapping. It also diagnoses the remaining coarse-candidate
failure as genuine: the first-cell assembled residual is about `6.92765`.
Exact graded mesh nodes are now supported throughout the untrusted profile and
Jacobi-family generator. A near-origin `1/128,1/64,1/32` schedule reduces the
sampled assembled residual to about `5.79e-4` and selects the candidate.

The 43-cell exact graded trace representer now passes the trusted audit. The
same-operator Barta lower bound exceeds `1.0235900944571767` on 139 leaves at
maximum depth four. All 43 cells are sign-certified for exact `L1` integration;
the approximate `L1` bound is `0.1055378219793721`, the residual supremum is at
most `0.08913332184493121`, the `C0`-induced `L1` error is at most
`0.7019249095288332`, and therefore `C_tau<=9.895351050897547`. The largest
residual occurs on `[1/16,9/128]`.

A composed trace-sharpened Schur validator is implemented and tested, with the
representer audit necessarily preceding the Schur correction. The physical
graded evaluation gives raw interval
`[2.9592592352087594,2.9601147691072494]`, residual at most
`0.005843528112861022`, trace correction at most `0.05782376205254868`, and
certified corrected interval `[2.9014354731562104,3.017938531159798]` for the
exact approximate-profile operator. The nonlinear endpoint-corrected tube,
preservation of coercivity and Schur margin on that tube, and Newton radius
remain replacement gates.

The trusted endpoint-corrected nonlinear audit now supplies the Newton forcing
terms: `||G(F_bar)||_infinity<=0.002295967024672295` and boundary-slope residual
in `[-2.3462001836132805e-5,1.633679528688307e-5]`. The largest residual occurs
on `[2,2.1875]`. This closes the center-residual item only; the derivative
mismatch `Z0`, tube Lipschitz bound, radii inequality, solution signs, and
inertia remain replacement gates.

The selected point seed is now an exact quintic-centered origin contraction.
Its `x^7` profile and `x^6` derivative cutoff errors are linked to the cubic
sensitivity theorem by a checked weighted-ball containment, including slope,
cutoff, mass, and curvature provenance. This removes the branch-identification
ambiguity when the sharper endpoint data and cubic-family sensitivities are
composed.
