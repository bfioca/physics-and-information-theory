# Paper R Modular Manuscript Outline

Status: technical architecture retained after **INCONCLUSIVE STOP**; not
promoted to a submission draft

## Working Identity

Conservative working title:

> Certified State-Sensitive Tidal Response of a Supported Skyrmion on a Fixed
> de Sitter Background

The paper's center is a computer-assisted leading-response theorem and its
equal-energy state-sensitive corollary. The observer-algebra motivation is a
replaceable front-end module, not a premise of the theorem.

## Sprint Outcome

The bounded viability sprint did not earn either headline theorem. The final
certificate gives

```text
corrected estimator  [-0.003079554319910408,-0.002552931394151071]
full A_ext interval  [-0.027341192151999246, 0.021708706437937767]
rho                  8.708392897914348130
decision             INCONCLUSIVE STOP
```

The outline is preserved as a proof map and as a specification for a possible
future certified primal solve. It must not be converted into a positive
abstract or submission manuscript without a new, explicitly authorized
sprint that closes zero exclusion. The detailed decision is in
[`paper_r_viability_decision.md`](../docs/paper_r_viability_decision.md).

Target length is 15-20 pages of main text plus technical appendices and
machine-readable certificates. If the response interval does not satisfy the
GO rule, this outline remains a technical record and must not be promoted by
rewriting the abstract more strongly.

## Claim Stack

The main text should expose the dependency order immediately:

```text
authenticated supported profile and coercive centrifugal form
    -> unique leading ell=2 matter response
    -> exact conserved bulk-plus-membrane master load
    -> correlation-aware primal-adjoint interval
    -> nonzero exterior electric-Weyl coefficient
    -> equal-energy spin-2 state discriminator.
```

Only the final two steps are candidate headline results. Earlier validated
profile and operator results are proof dependencies, not independent novelty
claims in this paper.

## Front-End Module A: Observer Motivation

Use this version for readers interested in finite observers and quantum
reference frames.

1. A finite directional reference carries state-dependent rotational
   multipoles as well as a Casimir or energy label.
2. A gravitational field can respond to those multipoles, so equal nominal
   rotor energy need not imply equal leading gravitational disturbance.
3. The supported Skyrmion supplies a concrete matter model in which this
   question can be posed without treating a rotor as an abstract external
   system.
4. The paper asks a deliberately narrower question than the universal
   observer program: can one certify the sign of its leading exterior tidal
   coefficient and exhibit state sensitivity?

This module may cite the current broader target in
[`paper_u_information_exposure_goal.md`](../docs/paper_u_information_exposure_goal.md)
and the legacy Harlow umbrella only as historical context, but it
must state that no observer-entropy, record-capacity, or universal tradeoff
theorem is proved here.

## Front-End Module B: Soliton And Relativity Motivation

Use this version for mathematical-physics, soliton, or numerical-relativity
readers.

1. Rotating solitons acquire a conserved quadrupolar stress only after their
   centrifugal deformation and supporting boundary are treated together.
2. Source cancellation, a regular-singular origin, and distributional wall
   terms make a sign theorem substantially harder than plotting a converged
   numerical solution.
3. A symmetric weak problem and a dual-weighted observable reduce the
   continuum response error to a product of primal and loaded-adjoint
   residuals.
4. The result is an explicit computer-assisted bridge from a supported
   nonlinear matter configuration to an exterior gauge-invariant tidal
   coefficient.

Modules A and B can be exchanged without changing definitions, theorem
statements, proof dependencies, or appendices.

## Abstract Template

Do not finalize the abstract until the GO gate closes. The earned version may
follow this structure:

1. **Problem:** leading quadrupolar gravity of a rotating, boundary-supported
   Skyrmion on fixed de Sitter.
2. **Method:** authenticated profile, coercive two-channel Friedrichs form,
   exact bulk-plus-shell master source, and correlation-preserving
   primal-adjoint interval enclosure.
3. **Theorem:** a directed interval for the leading exterior amplitude that
   excludes zero, transferred to a normalized electric-Weyl RMS on
   `5<=x<=10`.
4. **Physics corollary:** two spin-2 states with equal Casimir and leading
   rotor energy have different leading semiclassical mean tidal responses.
5. **Boundary:** fixed background, ideal Nambu-Goto wall, leading order, and
   no finite-time detector or self-gravity claim.

The abstract must quote the certified amplitude and `B_W` intervals, not the
current floating values.

## Main Text

### 1. Introduction

- Insert Front-End Module A or B.
- State the narrow question and why a rigorous sign is not automatic.
- Give Theorems R1 and R2 informally in one paragraph each.
- State all major exclusions in the introduction, not only at the end.
- Summarize the proof dependency chain and certificate availability.

### 2. Fixed Model And Perturbative Scope

- Define `x=e f_pi r`, the pure-de-Sitter lapse, `R=20`, and wall `a=4`.
- State the massive Skyrme action and the frozen parameter point.
- Define the supported hedgehog and authenticated background profile.
- Introduce the formal traceless quadratic rotation amplitude.
- Explain why the theorem is a coefficient at `O(Omega^2)`, not a finite-
  `Omega` statement.
- Declare the collective normalization `I=c_I/(e^3 f_pi)` and `QJ`.

Primary dependencies:

- [`validated_skyrmion_au3b.md`](../docs/validated_skyrmion_au3b.md)
- [`centrifugal_skyrmion_physical_response.md`](../docs/centrifugal_skyrmion_physical_response.md)

### 3. Centrifugal Weak Problem

- Define the two regular fields `y=(f,g)` and the physical origin behavior.
- State the symmetric quadratic form `q`, its domain, and the rotational weak
  load `ell`.
- State the ideal-mirror and moving-wall boundary conditions.
- Quote the certified coercivity and trace margins.
- State existence and uniqueness of the exact leading deformation used in
  every later section.

Primary dependencies:

- [`centrifugal_skyrmion_friedrichs_form.md`](../docs/centrifugal_skyrmion_friedrichs_form.md)
- [`centrifugal_skyrmion_riccati_coercivity.md`](../docs/centrifugal_skyrmion_riccati_coercivity.md)
- [`centrifugal_skyrmion_friedrichs_trace.md`](../docs/centrifugal_skyrmion_friedrichs_trace.md)

### 4. Conserved Bulk-Plus-Membrane Source

- Reconstruct the same-action bulk stress as an affine function of `y,y'`.
- Derive smooth conservation from the weak equations.
- Introduce the displaced Nambu-Goto shell and background step layer.
- Show how normal and tangential traction close distributional conservation.
- Map the full source to the static `ell=2` master equation.
- Explain the exact cancellation between the bulk density endpoint and shell
  contact term.

Primary dependencies:

- [`centrifugal_skyrmion_completed_stress.md`](../docs/centrifugal_skyrmion_completed_stress.md)
- [`centrifugal_skyrmion_membrane_stress.md`](../docs/centrifugal_skyrmion_membrane_stress.md)
- [`centrifugal_affine_master_kernel.md`](../docs/centrifugal_affine_master_kernel.md)

### 5. Exterior Amplitude And Weyl Observable

- Factor the exterior Green function into center- and horizon-regular modes.
- Define `J_rigid`, the deformation functional `B`, and `A_ext`.
- Define the unit-tensor angular Weyl projection.
- Fix the observation annulus `I_W=[5,10]`.
- Define the dimensionless RMS `B_W` from curvature.
- Prove its independence from master-field normalization.
- Use the closed exact identity `B_W=(25/2)|A_ext|`.
- Record that the certified amplitude interval contains zero, so this sprint
  earns no positive numerical lower bound.

Primary dependencies:

- [`centrifugal_skyrmion_master_adjoint_enclosure.md`](../docs/centrifugal_skyrmion_master_adjoint_enclosure.md)
- [`static_patch_l2_weyl_reconstruction.md`](../docs/static_patch_l2_weyl_reconstruction.md)
- [`paper_r_weyl_observable.md`](../docs/paper_r_weyl_observable.md)
- [`paper_r_weyl_observable.py`](../qgtoy/paper_r_weyl_observable.py)
- [`paper_r_viability_contract.md`](../docs/paper_r_viability_contract.md)

### 6. Computer-Assisted Response Decision

- State exact input intervals and source hashes.
- Describe conforming rational primal and adjoint trials.
- Treat the regular origin without evaluating singular-looking coefficients.
- Quote the representation-compatible weak loaded-adjoint origin squared
  bound `2.58228030899e-7`.
- Present the correlation-preserving form-dual/Riesz construction.
- Include primal and loaded-adjoint wall traces and all interface checks.
- State the corrected estimator and exact residual-product identity.
- Give a table allocating every contribution to the final interval radius.
- State the `INCONCLUSIVE STOP` decision and explain why Theorem R1 was not
  certified.

This section should explain the validation architecture. Cell tables,
Taylor-model coefficients, and replay detail belong in appendices and machine
artifacts.

Primary dependencies:

- [`validated_centrifugal_origin_response_residual.md`](../docs/validated_centrifugal_origin_response_residual.md)
- [`validated_centrifugal_correlated_residual.md`](../docs/validated_centrifugal_correlated_residual.md)
- [`validated_centrifugal_adjoint_bulk_load.md`](../docs/validated_centrifugal_adjoint_bulk_load.md)
- [`validated_centrifugal_adjoint_energy_dual.md`](../docs/validated_centrifugal_adjoint_energy_dual.md)
- [`validated_centrifugal_origin_adjoint_load.md`](../docs/validated_centrifugal_origin_adjoint_load.md)
- [`validated_centrifugal_origin_weak_dual.md`](../docs/validated_centrifugal_origin_weak_dual.md)
- [`validated_centrifugal_correlated_adjoint.md`](../docs/validated_centrifugal_correlated_adjoint.md)
- [`paper_r_viability_decision.md`](../docs/paper_r_viability_decision.md)

### 7. Equal-Energy State Discriminator

- Define `QJ` for a fixed-spin density matrix.
- Give the two exact spin-2 states and verify normalization.
- Prove equality of Casimir, inertia, and leading rotor energy.
- Import the closed exact calculation
  `QJ_cat=diag(-1,-1,2)`, `||QJ_cat||_F=sqrt(6)`, and `QJ_T=0`.
- Apply the tested transfer to the certified response interval.
- Record that its zero-containing input does not certify Theorem R2.
- Explain the `QJ=0` escape branch and why this is not a universal cost bound.

The state algebra and interval-transfer map are closed. The present sprint's
nonzero-vs-zero conclusion is not certified because R1 does not exclude zero.

Primary dependency:

- [`skyrmion_tidal_reference_discriminator.md`](../docs/skyrmion_tidal_reference_discriminator.md)
- [`paper_r_state_transfer.py`](../qgtoy/paper_r_state_transfer.py)
- [`test_paper_r_state_transfer.py`](../tests/test_paper_r_state_transfer.py)

### 8. Interpretation And Limits

- Interpret the certified result as state-sensitive leading gravitational
  response, not an observer-capacity inequality.
- Separate model dependence of the ideal wall from mathematical dependence of
  the sign proof.
- Discuss what would be needed for a finite-thickness or smooth-confinement
  robustness theorem.
- List the open finite-rotation, Israel-matching, self-gravity, fluctuation,
  and finite-time detector problems.
- Relate Paper R to the broader observer program without making it a logical
  prerequisite.

## Appendices

### Appendix A. Conventions And Exact Rescalings

Action normalization, `x,tau`, stress scales, Einstein coupling, spherical
harmonic normalization, `QJ`, and the exact conversion to physical curvature.

### Appendix B. Authenticated Background Profile

Profile theorem, origin family, outer replay, parameter hashes, and the
quantities imported by the response proof.

### Appendix C. Friedrichs Domain And Coercivity

Origin traces, wall trace, completed-square identity, coercivity constant,
and uniqueness.

### Appendix D. Regular-Origin Response Algebra

The `t=x^2` variables, canceled master kernel, origin profile jets, trial
polynomials, and conormal interface.

### Appendix E. Distributional Membrane Source

Delta conventions, displaced layer, traction identities, master contact
subtraction, and the scope distinction from Israel matching.

### Appendix F. Correlated Primal Residual

Common radial coordinate, profile/trial Taylor models, remainder treatment,
cell integration, and wall composition.

### Appendix G. Loaded Adjoint And Form-Dual Certificate

Derivative-free weak reduction, regular-origin load, correlation-preserving
Riesz/form-dual construction, wall trace, and full `delta_z`. Record the
certified negligible origin contribution separately from the still-dominant
positive-radius enclosure.

### Appendix H. Dual-Weighted Interval And Error Ledger

Proof of the exact identity, directed `J_hat`, `delta_y delta_z`, all direct
rounding terms, final amplitude interval, and decision ratio `rho`.

### Appendix I. Weyl Reconstruction And Annular Bound

Exterior homogeneous mode, inverse Regge-Wheeler map, gauge invariance on de
Sitter, angular projection identity, and the certified integral defining
`B_W`. Include the exact squared average `625/4` and transfer factor `25/2`.

### Appendix J. Spin-2 State Algebra

Exact generator matrices, state normalization, Casimir and energy equality,
quadrupole tensors, `sqrt(6)` cat norm, conditional exact-rational footprint
transfer, and the Jacobi-limit corollary.

### Appendix K. Reproduction And Artifact Index

Environment, commands, source hashes, certificate schemas, independent audit
commands, and a claim-to-artifact table.

## Required Figures And Tables

1. **Dependency diagram:** profile -> weak response -> conserved source ->
   adjoint certificate -> Weyl theorem -> state discriminator.
2. **Model figure:** static patch, center, membrane at `a=4`, observation
   annulus `5<=x<=10`, and horizon `R=20`.
3. **Response figure:** floating curve for orientation only, visibly labeled
   as non-rigorous; certified interval endpoints must be shown separately.
4. **Error-budget table:** each direct and residual-product contribution to
   `E_tot`.
5. **State table:** normalization, `<J^2>`, leading energy, `QJ`, and leading
   mean Weyl outcome for the two spin-2 states.
6. **Claim-boundary table:** proved, conditional, and not addressed.

Plots must not use visual mesh convergence as evidence for a continuum
theorem. The certified interval and its source artifact are the evidence.

## Final Decision And Error Ledger

Populate this table directly from the final audit. Do not infer missing values
from floating convergence.

| Quantity | Current evidence | Final value or interval |
| --- | --- | --- |
| Origin loaded-adjoint `L2` residual squared | certified `<2.481492321e-9` | closed |
| Origin loaded-adjoint `V*` contribution squared | certified `<2.48149232003e-7` | closed |
| Complete correlated primal norm `delta_y` | source-bound composition | `<0.785351351663998829` |
| Complete loaded-adjoint norm `delta_z` | weak origin, outer, and wall | `<0.030892717992632714` |
| Corrected estimator | directed origin, outer, and wall evaluation | `[-0.003079554319910408,-0.002552931394151071]` |
| Total radius and `rho` | estimator radius plus residual product | `<0.024524949294968507`; `rho<8.708392897914348130` |
| Exterior amplitude | complete certified interval | `[-0.027341192151999246,0.021708706437937767]` |
| Unit annular footprint | exact `B_W=(25/2)|A_ext|` | `[0,0.341764901899990572]` |
| Spin-2 state transfer | exact `sqrt(6)` versus zero map | nonzero conclusion **not certified** |
| Sprint decision | frozen thresholds applied | **INCONCLUSIVE STOP** |

## Claim Hygiene

| Phrase | Use? | Replacement or condition |
| --- | --- | --- |
| "nonzero gravitational response" | only with "leading fixed-background coefficient" | quote the certified interval |
| "rotating Skyrmion" | with care | say "leading centrifugal branch" where finite rotation is not controlled |
| "physical tidal signal" | only as leading semiclassical mean | distinguish coefficient from finite-time readout |
| "same energy, different gravity" | only with "same leading rotor energy" | state that `O(Omega^4)` equality is open |
| "certified membrane" | no | say which algebraic, distributional, or interval wall term is certified |
| "self-consistent" | no | background geometry is frozen |
| "universal" | no | the theorem is one supported model at one parameter point |
| "backreaction bound" | no | use "electric-Weyl response coefficient" |
| "observer entropy" | no | Paper R proves no entropy comparison |
| "robust" | only after a parameter-box or alternative-wall theorem | one certified point is not robustness |

## Authoring Order

1. Keep Sections 2-5 as definition/proof drafts without numerical theorem
   endpoints; the exact annular transfer is already closed.
2. Treat the origin loaded-adjoint and exact spin-2 transfer as closed inputs.
3. The one allowed correlation-aware form-dual/Riesz redesign is complete.
4. Sections 6 and Appendices F-H now serve as a technical record of the STOP
   result, not as theorem prose.
5. The state-transfer map was instantiated and does not certify a nonzero cat
   footprint because the response interval contains zero.
6. The frozen decision rule was applied without changing its thresholds.
7. Do not write the positive abstract or polish this as a submission draft.

## Promotion Checklist

- [x] The exact annular transfer `B_W=(25/2)|A_ext|` is proved and tested.
- [x] The regular-origin loaded-adjoint contribution is certified.
- [x] The exact spin-2 algebra and conditional interval transfer are tested.
- [ ] Theorem R1 has directed interval endpoints excluding zero with the
  contract's useful margin.
- [ ] `B_W` has a certified annular lower bound.
- [ ] Theorem R2's closed transfer is instantiated with the certified R1
  interval.
- [ ] Every theorem hypothesis maps to a model definition or certificate.
- [ ] Every numerical value in a theorem maps to a source-hashed artifact.
- [ ] The error table includes origin, outer bulk, wall, profile, interface,
  residual-product, collective-normalization, and Weyl-transfer terms.
- [ ] Finite-`Omega`, Israel, self-gravity, noise, and fluctuation exclusions
  appear in the abstract or introduction and in the theorem discussion.
- [ ] A clean checkout reproduces every certificate and the manuscript PDF.
- [ ] An adversarial claim audit finds no use of floating convergence as a
  substitute for interval proof.
