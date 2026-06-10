# Massive-Skyrmion Observer Work Package

Status: centered supported-worldtube and fixed-background `O(Omega^2)`
source-to-Jacobi chain completed; validation, physical junctions, higher-order
rotation, fluctuations, and self-gravity remain open.

## Decision

The lead candidate for replacing the abstract spherical top is a massive
`SU(2)` Skyrme soliton in a de Sitter static patch, quantized in its rotational
collective-coordinate sector.

This is a research choice, not a result. It is favored because one relativistic
field profile determines the mass, inertia, localization radius, conserved
current moments, and stress tensor. The model also has existing positive-
cosmological-constant solutions. The first two go/no-go gates are:

1. derive a covariant coupling between the physical pseudoscalar gradient and
   the rotational collective charge without treating internal isospin as a
   spatial vector by fiat; and
2. include the support stress required to hold an off-center soliton on a
   static accelerated worldtube.

The covariance gate passes at collective-worldline EFT level. The support gate
has become sharper: generic regular horizon data give logarithmically divergent
rigid-rotor inertia. The centered ideal-mirror worldtube realizes the controlled
remedy through the fixed-background `O(Omega^2)` source and local tidal
observable. A global uniqueness theorem excluding exceptional nontrivial data
with `sin(F_c)=0`, the off-center support completion, and a dynamical physical
wall remain open.

## Matter Action

Fix metric signature `(+---)` and the physical-pion-mass convention

```text
S_Sk=int sqrt(-g) [
 -f_pi^2/16 Tr(R_mu R^mu)
 +1/(32e^2) Tr([R_mu,R_nu][R^mu,R^nu])
 +f_pi^2 m_pi^2/16 Tr(U+U^dagger-2)
],
R_mu=U^dagger nabla_mu U,
U in SU(2).
```

The coefficient `1/16` is essential: `1/8` on the symmetric trace doubles the
potential and makes the small-fluctuation mass `sqrt(2)m_pi`. The corrected
convention gives the flat tail `exp(-m_pi r)`. With signature `(+---)` and
variation with respect to the inverse metric, the physical Hilbert stress is

```text
T_mu_nu=+2/sqrt(-g) delta S_Sk/delta g^(mu nu).
```

The previously recorded minus sign would give negative static energy in this
signature. Gravitational perturbation formulas elsewhere use `(-+++)`; their
mixed components are obtained from the same physical orthonormal density and
pressures only after the signature convention is translated explicitly.

The vector-isospin current is defined invariantly by weakly gauging
`SU(2)_V` and differentiating with respect to the auxiliary gauge field. This
avoids choosing a convention-dependent local current formula too early.

For the hedgehog

```text
U_0=cos F(r)+i tau dot xhat sin F(r),
```

spatial rotations can be compensated by vector-isospin rotations. On a fixed
profile, a collective orientation `A(t)` gives the exact pullback

```text
L_rig=-M+(I/2)Omega^2.
```

The stated two- and four-derivative Skyrme action has no fixed-profile
`Omega^4` term: `R_0` is linear in `Omega`, and every time-dependent action
term is quadratic in `R_0`. A quartic effective term is induced after profile
or wall relaxation. Its coefficient is essential for a precision low-spin
expansion, while the profile-uniform density bound below controls collective
high-spin coercivity without truncating that expansion.

Primary starting points:

- [Hata and Kikuchi, relativistic collective quantization of a spinning
  Skyrmion](https://arxiv.org/abs/1002.2464)
- [Brihaye and Delsate, Skyrmions in de Sitter
  spacetime](https://arxiv.org/abs/hep-th/0512339)
- [García Martín-Caro, massive-pion exponential
  localization](https://arxiv.org/abs/2209.06607)
- [Giacomini et al., gravitating Skyrme solitons in a
  cavity](https://arxiv.org/abs/1708.06863)
- [Giulini, spinorial quantization of the Skyrme
  model](https://arxiv.org/abs/hep-th/9301101)
- [Krusch, Finkelstein-Rubinstein
  constraints](https://arxiv.org/abs/hep-th/0210310)

## Target Scaling Theorem

Set

```text
x=e f_pi r,  mu=m_pi/(e f_pi),
lambda=(e f_pi R)^-2,  N(x)=1-lambda x^2,
s=sin F,  u=x^2+8s^2.
```

The exact reduced energy and profile equation are

```text
M=(4pi f_pi/e) int dx E,
E=(1/8)N u F'^2+s^2/4+s^4/(2x^2)
  +(mu^2 x^2/4)(1-cos F),

(N u F')'=(4N F'^2+1+4s^2/x^2)sin(2F)
           +mu^2 x^2 sin F.                            (1)
```

In flat space, for fixed `mu` and energy-quantile radius `a_q`, radial
rescaling gives

```text
M=c_M(mu) f_pi/e,
I=c_I(mu)/(e^3 f_pi),
a_q=c_a(mu,q)/(e f_pi),
M_2/|Q|=c_2(mu,q)/(e^2 f_pi^2).                          (2)
```

At fixed de Sitter radius the constants depend on both `mu` and `lambda`, and
proper radius is

```text
a_proper=asin(sqrt(lambda)x)/(e f_pi sqrt(lambda)),       (3)
```

not simply the areal value `x/(e f_pi)`.

### Completed Flat Baseline

The dependency-free RK4 shooting calculation at `mu=1`, matched at `x=10` to
the exact linear `l=1` Robin tail, gives

```text
b=1.58023676,
c_M=48.6317632,
c_I=34.3539730.
```

It verifies monotonicity, unit baryon number, the tail logarithmic derivative,
and the Derrick identity `E_2-E_4+3E_0=0` at the declared numerical tolerance.
This is a cross-checkable baseline, not yet the finite static-patch observer.

### Fixed-De-Sitter Gate

At the Killing horizon `x_c=lambda^-1/2`, regularity requires

```text
N'_c u_c F'_c=(1+4sin^2(F_c)/x_c^2)sin(2F_c)
               +mu^2 x_c^2 sin(F_c),
N'_c=-2/x_c.                                             (4)
```

The horizon relation sends `F_c=0` to `F'_c=0`; under an analytic Frobenius
uniqueness assumption this is the vacuum branch, but that uniqueness statement
is not part of the executable certificate. The collective inertia is

```text
I=(2pi/(3e^3 f_pi)) int dx x^2 sin^2(F)
  [1/N+4F'^2+4sin^2(F)/(N x^2)].                         (5)
```

For generic regular data with `sin(F_c) != 0`, it diverges as

```text
c_I(epsilon)~(pi x_c/3)
 [x_c^2 sin^2(F_c)+4sin^4(F_c)] log(1/epsilon).           (6)
```

Thus every regular profile with `sin(F_c) != 0` fails to define a finite global
rigid rotor. The program selects a worldtube boundary/support sector at
`x_w<x_c` as the controlled next model, where the profile, inertia, stress, and
tail leakage must be recomputed. A proof that every nontrivial global profile
falls in the divergent class remains a separate horizon-uniqueness gate.

The first named-matter theorem should prove, with controlled exponential-tail
errors:

1. the integrated vector charge is the collective rotor generator;
2. for `H=h(Q^2)`, that charge is zero Bohr frequency;
3. parity and hedgehog covariance force the compressed signed current dipole to
   vanish componentwise;
4. the second current moment obeys `M_2<=C_2 a_q^2 ||Q||`;
5. the exact profile integrals determine `M`, `I`, `a_q`, and the support stress;
6. slow rotation and subcritical compactness imply a named-source radius floor
   proportional to `sqrt(G)[L(L+1)]^(1/4)`.

If these statements hold uniformly in a controlled parameter family, the
dipole-cancelled support branch becomes matter-derived rather than stipulated.

## Work Packages

### WP1: Static Profile And Integrals

- [x] derive the flat/fixed-static-patch hedgehog ODE in one physical-mass
  convention;
- [x] solve the flat equation with origin regularity and the massive Robin tail;
- [x] compute the flat `c_M` and `c_I` baseline and verify Derrick/topological
  identities;
- [x] derive the de Sitter horizon condition, proper-radius conversion, and
  global-inertia divergence;
- [x] choose a centered ideal-mirror worldtube boundary/support action and solve
  its hard-wall boundary-value problem;
- [x] compute the centered inertia-weighted proper first and second current
  radii and their step-halving stability;
- [ ] compute an independent collocation error, tail leakage, and the deformed
  off-center support stress.

Completion gate: independent discretizations agree and all tail/systematic
errors are smaller than the intended `A/d` channel budget after scaling.

### WP2: Collective Charge And Reference State

- [ ] derive the finite-worldtube collective action through `Omega^4`;
- [x] derive the complete local `O(Omega^2)` quadrupole Hessian/source in
  regular physical fields, prove that the profile-only equation misses a
  tangential forcing, and obtain the moving-mirror pure-tension Robin law;
- [x] reduce the global coupled quadrupole problem and obtain a
  mesh/origin/profile-step-converged exploratory default solution;
- [x] reconstruct its same-action bulk stress and verify both smooth-bulk
  conservation identities with second-order mesh closure;
- [x] derive the moving Nambu-Goto stress and close full bulk-plus-shell
  distributional conservation at fixed-background first order;
- [x] project the full source into the frozen Zerilli-Moncrief master and
  compute a mesh/origin/profile-stable nonzero off-wall response;
- [x] physically normalize the coupled response from a validated fixed-spin
  density matrix and reconstruct its exterior electric-Weyl quadrupole;
- [x] compose the exterior curvature with an instantaneous Jacobi-limit radial
  gradiometer and show that equal-Casimir, equal-leading-energy spin-2 states
  can have nonzero versus zero semiclassical mean tidal signals;
- [ ] validate the coupled response, impose tensorial Israel matching, promote
  the Jacobi contraction to a finite-separation/finite-time noisy detector,
  and use the completed matter response to determine the induced `Omega^4`
  coefficient and fluctuation corrections;
- [x] prove a profile-uniform leading collective-sector floor from the exact
  supported mass and inertia densities, avoiding a fixed-profile `Omega^4`
  truncation for the coercivity question;
- [x] identify the standard fermionic `B=1` Finkelstein-Rubinstein sector as the
  odd Peter-Weyl space `direct_sum_j V_j tensor V_j^*`, `j` half-integer;
- [x] prove that its density, POVM, and orientation kernel are center blind and
  derive exact integer-target tensor-rank multipliers, fidelity, and Casimir;
- [ ] prove that the right/isospin multiplicity is coherently accessible to the
  physical preparation, interaction, and decoder;
- [ ] construct the cross-spin token state from the matter action rather than
  postulating it;
- [x] given the standard leading compressed-current ansatz, derive its centered
  signed dipole cancellation, signed second moment, and absolute moment bounds;
- [ ] derive that compressed-current ansatz directly from the finite worldtube
  Noether current and control the collective-band projection error;
- [ ] repeat the current-moment calculation for the supported off-center
  `l=1` matter-wall deformation.

The standard nuclear `B=1` Skyrmion is not the literal integer-spin
`L^2(SO(3))` rotor assumed in the earlier EFT. The projective theorem repairs
the kinematics for an integer-spin target, but only if isospin is an operational
multiplicity register. A bosonic `B=1` quantization is the clean strict-integer
fallback; an unmarked `B=2` or `B=4` multiskyrmion is not a drop-in full
orientation reference.

The supported hedgehog densities now also give, for every radial profile in the
same hard worldtube,

```text
I[F]<=[4/(3N_w)]M[F]a^2,
E_j>=sqrt[3N_w j(j+1)/2]/a.                            (8)
```

Thus profile relaxation cannot remove collective-sector energy growth: it can
soften the quadratic rigid-rotor law to at worst a linear high-spin floor. The
remaining spectral gap is whether noncollective field modes or
collective-band projection errors undercut this adiabatic family bound.

The slow-rotation parameter at cutoff `J` is

```text
epsilon_rot=e^2 sqrt[(J+1/2)(J+3/2)]/c_I.                (9)
```

Thus fixed `e` and fixed dimensionless Skyrmion parameters cannot support an
asymptotically growing reference cutoff. More generally, slow rotation alone
requires
`e^2 J/c_I(mu,lambda,x_w) -> 0`, reducing to `e^2J -> 0` for a fixed profile,
while the wall, localization, lifetime, and gravity scalings are recomputed.

For a fixed dimensionless centered worldtube profile this recomputation already
closes the simplest tuning route. Compactness scales as `e^-2`, while
`epsilon_rot` scales as `e^2 sqrt[(J+1/2)(J+3/2)]`, so

```text
C epsilon_rot=
2G c_M sqrt[(J+1/2)(J+3/2)]/(c_I x_w lambda R^2).      (10)
```

At fixed `R^2/G` and fixed control budgets, only finitely many spins are
admissible, independently of the constrained `e`/`f_pi` co-scaling that keeps
`e f_pi` fixed. Profile-changing double scalings and different sources remain
possible escape routes.

For the centered rigid rotor, the compressed soldered current is

```text
ell_i^t=[kappa(r)/I](delta_ij-n_i n_j)J_j.              (11)
```

The covariant charge uses `dSigma_mu ell_i^mu`; on a static slice this equals
`r^2dr dOmega ell_i^t`, because the proper-volume and unit-normal lapse factors
cancel.

Its inversion parity gives exact componentwise signed-dipole cancellation,
while its signed second moment is

```text
int_Sigma dSigma_mu xi^k xi^l ell_i^mu=<rho^2>_I
 (4delta_klJ_i-delta_kiJ_l-delta_liJ_k)/10.             (12)
```

The default profile has `(e f_pi)^2<rho^2>_I=2.19023555`. This derives the
quadratic Hessian branch of the hard-current theorem for the centered baseline.
It does not set the absolute first moment to zero, and it does not yet apply to
the accelerated off-center worldtube, whose `l=1` support deformation can
regenerate a dipole.

Completion gate: the physical reference state has a proved recovery/estimation
advantage and the rotor deformation remains uniformly perturbative.

### WP3: Covariant Pseudoscalar Coupling

Construct or reject a local scalar interaction based on

```text
B_mu=h_mu^nu(nabla_nu chi+a_nu chi)
```

and the Skyrmion collective current. Any spin-isospin soldering tensor must arise
from the hedgehog orientation and marked worldtube frame, transform covariantly,
and introduce no unaccounted external reference.

For the collective orientation `A`, define

```text
D_ai(A)=(1/2)Tr(tau_a A tau_i A^dagger),
J_i=-D_ai(A) I_a.
```

The orientation matrix is dynamical, so it solders internal isospin to physical
rotation without a fixed `delta_ai` spurion. A covariant worldline coupling is

```text
S_int=g int d tau B_mu S^mu,
B_mu=h_mu^nu(nabla_nu chi+a_nu chi),
S^mu=W^mu/M.                                             (7)
```

Both vectors are axial, making (7) parity even. In the rest frame it reduces to
`g B_i J_i`. This passes the collective-worldline covariance gate.

It does not yet pass the stricter bare-field locality gate: `A` is a global zero
mode and total spin is a stress-tensor moment. The next calculation must project
a covariant worldtube interaction onto the collective band and bound the
multipole error. If strict point-local four-dimensional coupling is required,
the fallback is a Dirac axial current `B_mu psi_bar gamma^mu gamma^5 psi`.

Completion gate: one finite-worldtube covariant action produces the collective
coupling and hard-current moments with controlled projection errors.

### WP4: Accelerated Worldtube And Lifetime

- [x] construct a centered covariant ideal-mirror membrane imposing `U=1` at
  `x_w<x_c`, solve the exact-`B=1` hard-wall profile, and derive its pressure,
  mean curvature, Young-Laplace tension, and wall mass;
- [x] prove that positive tension alone can support positive interior pressure
  only for `x_w<sqrt(2/3)x_c`;
- [x] obtain step-converged numerical evidence for positive curvature along the
  centered adiabatically re-solved `l=0` Dirichlet branch at fixed membrane
  tension;
- [ ] replace that evidence by a validated-numerics or analytic sign proof;
- [x] prove that a simple finite cosine pinning potential cannot preserve exact
  `B=1` for a nontrivial profile, and derive its large-stiffness topology defect;
- [ ] test the fully coupled `l=0` and nonspherical wall/profile Hessian modes
  and construct a finite-stiffness boundary-topological UV completion;
- [x] derive the leading off-center Fermi acceleration and `l=1` wall-traction
  gate on a static trajectory;
- [ ] solve the coupled off-center matter, membrane, and anchoring deformation;
- include the trap, strut, membrane, or other support source and its stress;
- bound tidal deformation, pion radiation, rotational breakup, and tail leakage;
- prove a lifetime longer than the required recovery protocol.

Completion gate: support and radiation costs do not dominate the Skyrmion mass
or invalidate the localization scaling.

### WP5: Open-System Transfer

- derive the smeared Bunch-Davies bath spectra for the actual current profile;
- compute the Kossakowski matrix and Lamb shift;
- prove the zero-Bohr, aggregate nonzero-Bohr, and second-order jump transfers;
- track constants and gap aggregation as `L` grows;
- compare the true reduced channel with the collective heat semigroup over the
  full protocol time.

Completion gate: the channel error is strictly smaller than the recovery
obstruction in one common parameter window.

### WP6: Einstein-Skyrme Backreaction

- first solve the centered spherically symmetric positive-`Lambda` problem;
- then control the accelerated off-center perturbation including support stress;
- compare the resulting body radius with Dain-type size-angular-momentum bounds;
- decide whether the joint localization/lifetime/gravity window is empty.

Completion gate: a controlled semiclassical solution or a genuine
Einstein-matter obstruction replaces the stipulated compactness margin.

## Kill Criteria

Reject the Skyrmion route if any of the following survives reasonable model
variation:

- the physical-gradient/internal-current contraction needs an external spatial
  frame not supplied by the observer;
- integer center-blind rotor sectors require strongly nonspherical multi-soliton
  configurations that destroy the current-moment simplification;
- the slow-rotation window closes before the protected spin grows;
- no joint parameter scaling with `e^2 J -> 0` remains localized and
  subcritical;
- Skyrmion isospin is not an accessible multiplicity register for the prepared
  token and decoder;
- every physically reasonable finite boundary condition destroys the desired
  Skyrmion sector or makes the support energy dominant;
- support stress or radiation dominates the compactness budget;
- exponential tails spoil the `A/d` error allocation;
- the open-system constants grow fast enough with `d` to erase the proposed
  channel separation; or
- an existing size-angular-momentum theorem already implies the full claimed
  result once the channel assumptions are removed.

## Paper Claim If Successful

The strongest defensible Paper B statement would be:

> A massive Skyrmion supplies a stress-tensor-derived rotational quantum
> reference with explicit current moments. In the controlled local common-mode
> branch, its matter-derived size lower bound collides with the channel-derived
> near-horizon support upper bound, while an overlapping realization obeys a
> separately quantified open-system error law.

Anything weaker remains a mathematical-physics research program rather than a
new de Sitter observer theorem.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy massive-skyrmion-profile
PYTHONPATH=. python3 -m qgtoy massive-skyrmion-worldtube
PYTHONPATH=. python3 -m qgtoy skyrmion-projective-reference
PYTHONPATH=. python3 -m qgtoy skyrmion-joint-scaling-no-go
PYTHONPATH=. python3 -m qgtoy skyrmion-current-moments
PYTHONPATH=. python3 -m qgtoy skyrmion-worldtube-stability
PYTHONPATH=. python3 -m unittest tests.test_massive_skyrmion_profile
PYTHONPATH=. python3 -m unittest tests.test_massive_skyrmion_worldtube
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_projective_reference
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_joint_scaling_no_go
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_current_moments
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_worldtube_stability
python experiments/centrifugal_skyrmion_physical_response_audit.py
python experiments/static_patch_l2_weyl_reconstruction_audit.py
python experiments/skyrmion_tidal_reference_discriminator_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_physical_response.py \
  tests/test_static_patch_l2_weyl_reconstruction.py \
  tests/test_skyrmion_tidal_reference_discriminator.py
```

The executable result proves the flat numerical baseline, the conditional
rigid-rotor horizon/inertia gate, the centered ideal-wall worldtube baseline,
the odd-sector recovery theorem, the fixed-profile joint-scaling obstruction,
the centered collective-current moments, the conditional adiabatic `l=0`
minimum, and the simple finite-pinning topology no-go. It does not solve the
finite-stiffness topological completion, coupled off-center support/current
deformation, the physical open-system channel, or Einstein-Skyrme backreaction.
The centered centrifugal branch further supplies an exactly transmitted
conserved master source, a fixed-spin physical normalization, an exterior
electric-Weyl quadrupole, and an instantaneous Jacobi-limit reference-state
discriminator. A conditional constant-rate heat/Jacobi/Gaussian theorem now
extends it to finite-time displacement and readout error. Interval validation,
tensorial Israel matching, `Omega^4` control, common-action detector inputs,
stress/metric fluctuations, and Einstein-Skyrme backreaction are unresolved.
