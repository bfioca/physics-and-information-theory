# Technical Appendix: Auditable Status of the Directional-Record Program

This appendix records the exact domains of the results used in the review
packet. The labels have the following meanings: **[PROVED]** is an analytic or
computer-assisted theorem on the stated domain; **[CONDITIONAL]** is an exact
implication under a stipulated effective model or a source-bound floating
construction; and **[OPEN]** is a missing implication, norm estimate, or
physical identification. A composite claim inherits the least-complete label
of its ingredients.

## A. Relational orientation as the operational task

**[PROVED]** Let the unknown relative orientation `g in SO(3)` have normalized
Haar prior, let an arbitrary POVM return `g_hat`, and use the full-frame
chordal cost

```text
c(g,g_hat)=sin^2(theta(g_hat^-1 g)/2).
```

The reference Hilbert space may have arbitrary rotation-trivial
multiplicities, with representation
`U(g)=direct_sum_j U_j(g) tensor identity_(M_j)`. For every normal state and
every POVM, including mixed states and protocols with invariant ancillas, the
global Bayes risk obeys the two independent bounds

```text
R_ref >= 1/(16 <J^2>+8),
R_ref >= c_SO3 exp[-2 S_dir/3],
c_SO3 = 6/(e pi^(5/3)),
S_dir = A_SO3(rho) = D(rho || G_SO3(rho)).                 (A.1)
```

The first line follows from the spin-1 fusion matrix and a discrete Hardy
inequality. The second follows from relative-entropy data processing for the
covariant orbit ensemble and a global rate-distortion estimate. Neither proof
assumes a locally unbiased estimator, a Cramer-Rao regime, purity,
polarization, a fixed irrep, or finite-dimensional multiplicity. The result is
tail robust: a small probability in a remote high-spin sector cannot defeat
the mean-spin/asymmetry formulation. The exact theorem and proof are Research
Theorem W3 in `THEOREMS.md` and
`docs/global_so3_reference_risk.md`.

**[PROVED]** The datum in (A.1) is relational. It is the group element aligning
two physical frames, not an orientation relative to coordinates. The
performance criterion is a Haar-prior loss over the entire group, not a local
sensitivity proxy. For strict integer-spin support through `j=J`, the sharper
bound is `R_ref>=sin^2[pi/(2J+3)]`. For the fermionic
Finkelstein-Rubinstein sector `j=1/2,3/2,...`, relevant to a baryon-number-one
Skyrmion collective coordinate, the direct bound is instead
`R_ref>=1/(16<J^2>)`, and strict support through `J+1/2` gives
`R_ref>=sin^2[pi/(2J+4)]`.

**[PROVED]** In this appendix `S_dir` denotes only the relative entropy of
rotational asymmetry for the declared orbit ensemble. It is not identified
with Casimir, quantum Fisher information, thermodynamic entropy, Hilbert-space
dimension, effective classical memory size, generalized entropy, or the
observer entropy `S_Ob`. Equation (A.1) supplies the necessary allocation
`S_dir >= (3/2) log(c_SO3/R_ref)` when the logarithm is positive; it does not
show that asymmetry is sufficient for a useful accessible record.

**[CONDITIONAL]** If the reference alone undergoes stipulated isotropic
rotational heat diffusion with integrated exposure
`Gamma(T)=integral_0^T gamma(t)dt`, the spin-1 score is attenuated exactly by
`exp(-2 Gamma)`. Hence

```text
R_ref(T) >= 3/4[1-exp(-2 Gamma)]
           +exp(-2 Gamma)/(16 <J^2>+8).                 (A.2)
```

This is an exact finite-time degradation theorem for that channel. It is
classical record stability expressed through an operational readout risk, not
a statement about preservation of arbitrary quantum phase coherence.

**[OPEN]** The heat channel in (A.2) has not been derived, with a useful
finite-time norm error, from the same local interaction that prepares and
reads the record. The repository contains a prescribed-switch universal
Lindblad construction and profile-resolved bath inputs, but its
ancilla-stable state operator-norm residual is not a physical channel diamond
distance. No common-action protocol presently controls preparation, storage,
readout, channel error, support stress, and backreaction on one nonempty open
parameter set. This microscopic record channel is the principal conceptual
gap.

## B. Capacity from localization and energy

**[PROVED]** For finitely many spinless nonrelativistic particles with positive
total mass `M`, hard support `|x_i|<=a` in a rotationally invariant
configuration domain, and a nonnegative ground-subtracted excitation
Hamiltonian satisfying the quadratic-form inequality
`H_ex>=sum_i p_i^2/(2m_i)`, every form-domain state obeys

```text
<L^2> <= 2 M a^2 E_ex,
R_ref >= 1/(32 M a^2 E_ex+8).                           (B.1)
```

The proof is a mass-weighted Cauchy-Schwarz inequality and applies to mixed,
zero-mean, and rare-tail states with rotation-trivial internal labels. It does
not cover intrinsic spin, relativistic or massless fields, soft localization,
negative interaction energy, or nontrivially rotating light species. The
separate substitution `2G(M+E_ex)/a<=chi<1` is explicitly a compactness proxy,
not a theorem about general-relativistic bodies. The exact domain is Research
Theorem W3a and `docs/localized_orbital_reference.md`.

**[PROVED]** More generally, a rotationally invariant Hamiltonian with sector
floors `epsilon_j` yields an asymmetry-energy bound only if its rotational
partition function
`Z_H(beta)=sum_j (2j+1)^2 exp(-beta epsilon_j)` is finite. Then
`S_dir<=beta E+log Z_H(beta)` for each admissible `beta>0`. Covariance and
finite mean energy alone are insufficient: the repository gives an invariant
bounded Hamiltonian on `L^2(SO(3))` for which increasingly accurate frame
states retain uniformly bounded energy. A physical observer theorem must
therefore derive the growing sector floor from its matter model.

**[PROVED]** Inside the hard-supported massive-Skyrme hedgehog collective
family on fixed de Sitter, with support radius `a=x_w/(e f_pi)` and minimum
support lapse `N_w=1-lambda x_w^2>0`, the static Killing energy `M[F]` and
collective inertia `I[F]` satisfy, uniformly over all admissible radial
profiles,

```text
I[F] <= 4 M[F] a^2/(3N_w),
E_j >= sqrt[3N_w j(j+1)/2]/a.                           (B.2)
```

The second inequality minimizes over radial profile relaxation within the
adiabatic collective family. It produces a linear large-spin sector floor and
a finite integer or projective rotational partition function at every
positive inverse temperature. This is Research Theorem W3b and
`docs/supported_skyrmion_collective_spectral_floor.md`.

**[CONDITIONAL]** Equation (B.2) makes the supported Skyrmion a concrete
candidate realization of the abstract capacity premise, but it is not yet a
field-theoretic observer theorem. The proof assumes the adiabatic hedgehog
collective energy `M[F]+j(j+1)/(2I[F])`. It does not establish collective-band
completeness, control noncollective rotating modes or Born-Oppenheimer
projection error, derive coherent access to the right/isospin multiplicity,
or include the directional capacity of a marked rotating wall. These are
physical restrictions, not small numerical remainders.

## C. Certified supported profile

**[PROVED]** At the declared dimensionless parameters
`mu^2=1`, `lambda=1/400`, `F(0)=pi`, and `F(4)=0`, Research Theorem AU.1 is a
computer-assisted local existence theorem. An exact-rational 43-cell Newton
certificate proves a unique nonlinear solution within the certified Newton
ball, strict monotonicity `F'(x)<0` on `(0,4]`, wall slope
`F'(4) in [-0.09465,-0.08746]`, and finite positive dimensionless rotor
inertia `I_rot in [21.149,48.921]`. The theorem premises use rational outward
rounding and authenticated Taylor/Lagrange remainders; floating values are not
theorem inputs. The exact profile artifact has SHA256
`c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff`.

**[PROVED]** AU.1 is local uniqueness in the displayed Newton neighborhood on
a fixed pure-de-Sitter background with a prescribed hard Dirichlet wall. It
does not prove global uniqueness, dynamical stability, a rotating solution,
arbitrary wall dynamics, Einstein-Skyrme backreaction, or the operational
record protocol.

**[CONDITIONAL]** The profile closes the existence premise needed by several
fixed-background spectral and response calculations. It shows that the
matter realization used in those calculations is not merely a shooting
profile. It does not make the hard wall a harmless regulator; the support and
its stress are part of the physical model and must remain visible in every
external claim.

## D. Fixed-background gravitational witness

**[PROVED]** A static quadrupolar source cannot be specified by its energy
density alone. For a static even-parity stress on
`ds^2=-Ndt^2+dr^2/N+r^2dOmega^2`, Research Theorem W3n gives the two exact
bulk conservation equations and the wall traction terms. Research Theorem
W3o then shows that the undeformed fixed-profile rigid rotational Skyrmion
stress fails this conservation gate. This rejects the rigid source, not
rotating Skyrmions: the `O(Omega^2)` centrifugal matter deformation and moving
support must be included.

**[PROVED]** For the declared fixed-background matter-plus-moving-membrane
weak form, Research Theorems W3z.15 and W3z.16 establish a closed positive
Friedrichs operator `A` with `||A^-1||_(L2->L2)<=100`, a nonzero regular
forcing, and a unique nonzero weak centrifugal deformation. Their exact
artifacts have SHA256 values
`4a4e3ecd48a205860de3aa045c94d2b825c0afce1c0f12f4b96254db355b85bb`
and
`9edc2bc479534fab3f527ce535a373da1373b45085c6fbf4602f4ee9cdd32db7`.
A nonzero matter deformation does not by itself imply a nonzero exterior
master or Weyl amplitude.

**[CONDITIONAL]** Exact Hilbert-variation and shell identities, combined with
source-bound mesh refinement, support a completed conserved
bulk-plus-moving-membrane stress at the default point. The analytic
conservation factorization is exact, but closure of the selected branch is
floating rather than interval certified. The relevant floating artifacts are
the bulk-stress audit
`79f588642456d91eb58107de613a639566af0e7924cd29e8d480bf109ecea5db`
and membrane audit
`1ef92b3579f60fe52d2849d3da3202dc55be33be538b401117218f81cdea53aa`.
Accordingly the allowed wording is "source-bound floating conservation
audit," not an unqualified certified source.

**[PROVED]** Once a valid conserved stress is supplied, the source, propagation,
and readout maps are exact in one frozen convention. On fixed pure de Sitter,
for the static `ell=2` Regge-Wheeler/Zerilli-Moncrief normalization, regular
center behavior, and no-log horizon condition,

```text
A_2 Psi = F,
A_2 = -d/dr[(1-r^2/R^2)d/dr] + 6/r^2,
F = 8piG[-r^2 N rho'/6 + r(1+4r^2/R^2)rho/6
         -r p_r/2 - j + 2r pi],
delta E_rr = -6 Psi(r)Y_2/r^3.                         (D.1)
```

The Friedrichs operator has a positive exact Green kernel and
`A_2>=6/R^2`. The stress-to-master identity, ideal-shell transmission law,
and exterior master-to-electric-Weyl reconstruction are Research Theorems
W3t, W3v, and W3x. Their artifact SHA256 values are, respectively,
`3be17612134bb6b72535db9d3c80a74acf1271a39e04eec4b1591c9bd8967887`,
`c83536779d2ab62684218291dd99de190569f9973417d9accd2ceff426901ade`,
and
`3025d65fe82585e584150e956de9481380ab3f4a72d26a7cacb744974838c070`.
These exact maps do not certify that the completed Skyrmion produces a
nonzero input amplitude.

**[CONDITIONAL]** Source-bound floating calculations reduce the completed
exterior response to one scalar amplitude and give a stable dual-weighted
target near `-0.002818947812` in the declared dimensionless normalization.
The floating feasibility artifact has SHA256
`584a22ea3ae9807dcc9da8cd6cc20274c943c52bb23c38923cbe8e6dcf986bf7`.
This is design evidence only: the quoted fine-discrete residual product is
exact relative to an assembled Galerkin system, not a continuum interval that
includes the authenticated profile, origin, bulk, and wall errors.

## E. Present zero-exclusion gate

**[PROVED]** The certification architecture itself is exact. Outside the
compact source, the fixed-background response factorizes into one amplitude
`A_ext=J_rigid+B(y)`. If the symmetric weak form satisfies
`q(y,v)=ell(v)` and the adjoint satisfies `q(v,z)=B(v)`, then arbitrary
conforming trials `y_h,z_h` obey

```text
J_hat = J_rigid+B(y_h)+R_y(z_h),
|A_ext-J_hat| <= ||R_y||_(q*) ||R_z||_(q*).             (E.1)
```

Thus zero exclusion requires a corrected-amplitude interval whose distance
from zero is larger than the product of full primal and adjoint dual-residual
bounds. Equation (E.1) is Research Proposition W3z.17; satisfying its premises
for the physical coefficients is the unfinished task.

**[PROVED]** The current interval program certifies the positive-radius primal
residual square
`<=0.010027698207072146`, the origin primal residual square
`<=2.1330073298636e-5`, exact internal conormal cancellation, the moving-wall
adjoint load, and the positive-radius weak adjoint bulk load. The respective
artifact SHA256 values are
`814da74d5c21cf96b45e9967dd5b8d297d90480a46c3f3ae7fd82ba3ffaad3e7`,
`7924fb7da3bb96e92fb43f68cf9311b9ac9a6077292e69474fccf5579abab504`,
`1ee677788edc45190c9b164c45bc4a76a1b9e395d172f12b5aa13241748200e2`,
`ee73b3527750f91bcb2ed585df3d1d58376cbe0f4ff8db47919356872a86ed42`,
and
`3db6d390d521494d192c5df6b4bc5dfd1ee09f6d441f0bd69c3be2d18add44f5`.
These are certified components of the proof, not a response interval.

**[PROVED]** Research Proposition W3z.29 currently gives the direct
positive-radius-plus-wall adjoint form-dual estimate

```text
delta_z,partial^2 <= 0.592007476516919181,
delta_z,partial   <= 0.769420221021594403.               (E.2)
```

The wall contribution to the squared estimate is below `0.000175`. More than
99 percent of the bound comes from the adjusted bulk value coefficient, with
the dominant cell `[1/2,67/128]`. The exact artifact has SHA256
`500e56b5aa36c64846100dc59a7383b2051a12c6676fcf8e6d49574f61142d0e`.
Equation (E.2) is a rigorous representation diagnostic, not evidence of a
physical obstruction.

**[OPEN]** The regular-origin master load is absent from (E.2), so it is not a
full `delta_z`. Even before that missing origin term is added, the conservative
partial adjoint bound is too broad to combine with the current primal bound
and exclude zero in (E.1). The dominant quantified loss is the positive-radius
adjusted bulk value coefficient, not the wall trace. A successful refinement
must control this coefficient with stronger correlations or a better
Riesz/adjoint representation and then add the regular-origin load.

**[OPEN]** No rigorous interval for the completed normalized electric-Weyl
amplitude `B_W` presently excludes zero. The packet must therefore distinguish
three facts: the source-to-Weyl maps are exact, the floating completed response
is favorable, and the physical zero-exclusion theorem is not closed.

## F. Claim boundary for external review

**[PROVED]** The defensible mathematical core is: global relational
`SO(3)` risk requires asymmetry and rotational resources; named localized
matter classes turn rotational capacity into energy/support cost; one
hard-wall profile and its fixed-background centrifugal inverse exist; and a
valid conserved quadrupolar source has exact master/transmission/Weyl maps.

**[CONDITIONAL]** The defensible physical construction is narrower: a
hard-supported Skyrmion is a plausible semiclassical realization, a stipulated
heat channel gives an exact degradation law, and source-bound floating
calculations favor a nonzero fixed-background exterior response.

**[OPEN]** The project has not identified `S_dir` with `S_Ob`, derived a
preparation-through-readout record channel from one action, proved a common
parameter window, interval-certified `|B_W|>0`, established tensorial Israel
matching, solved a rotating self-gravitating Einstein-Skyrme-de Sitter system,
or shown that exterior Weyl response is the gravitational quantity that caps
observer information. Collapse, horizon or quantum-extremal-surface
displacement, or another invariant may be the relevant bottleneck.

**[OPEN]** Novelty and publishability are not outputs of the certificates. The
literature matrix in this packet is the separate primary-source comparison;
this appendix does not infer priority from an unsuccessful search and does not
use the words "first" or "breakthrough" as claims.

## G. Reproducibility map

**[PROVED]** The main analytic statements and exact certificate boundaries can
be audited from:

| Status | Result | Primary repository pointer |
| --- | --- | --- |
| **[PROVED]** | Global risk/asymmetry/Casimir bounds | `THEOREMS.md` W3; `docs/global_so3_reference_risk.md`; `tests/test_global_so3_reference_risk.py` |
| **[PROVED]** | Confined orbital capacity | `THEOREMS.md` W3a; `docs/localized_orbital_reference.md`; `tests/test_localized_orbital_reference.py` |
| **[CONDITIONAL]** | Heat-capacity composition | `THEOREMS.md` W3a.1; `experiments/universal_observer_tradeoff_certificate.json`, SHA256 `5c88eb4af23764204333b5e899083c87911066895d70fc132f263e180c175ad6` |
| **[PROVED]** | Supported collective sector floor | `THEOREMS.md` W3b; `docs/supported_skyrmion_collective_spectral_floor.md` |
| **[PROVED]** | Validated hard-wall profile | `THEOREMS.md` AU.1; `experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json`, SHA256 `c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff` |
| **[PROVED]** | Fixed-background source/master/Weyl maps | `THEOREMS.md` W3t, W3v, W3x; artifacts listed under (D.1) |
| **[CONDITIONAL]** | Floating completed response | `THEOREMS.md` W3u, W3z.17; feasibility SHA256 `584a22ea3ae9807dcc9da8cd6cc20274c943c52bb23c38923cbe8e6dcf986bf7` |
| **[PROVED]** | Certified residual components | `THEOREMS.md` W3z.24-W3z.29; artifacts listed under (E.2) |
| **[OPEN]** | Full Weyl zero exclusion | Requires full primal and adjoint `V*` residuals, including the regular-origin adjoint load, with product below the corrected-amplitude margin |

**[PROVED]** The complete wording guardrail, including the distinction between
exact theorems, exact maps with conditional inputs, floating evidence, and
open physical bridges, is
`docs/harlow_review_packet/claim_evidence_ledger.md`.
