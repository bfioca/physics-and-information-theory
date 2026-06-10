# Paper R Viability Contract

Status: bounded sprint complete; **INCONCLUSIVE STOP**; no nonzero Paper R
response theorem is certified

## Purpose

This document freezes the strongest response theorem that the current
repository could defensibly support after one correlation-aware validation
redesign. It separates three statements that must not be conflated:

1. an interval theorem for a leading `O(Omega^2)` fixed-background response
   coefficient;
2. an exact state-sensitive consequence inside one spin-2 collective band;
3. a finite-rotation, self-gravitating, or detector-level prediction.

Only the first two belong to the bounded Paper R sprint. The third remains
outside scope unless new estimates are proved explicitly.

## Sprint Result

The frozen decision rule has now been applied. The complete source-bound
composition gives

```text
J_hat in [-0.003079554319910408,-0.002552931394151071],
A_ext in [-0.027341192151999246, 0.021708706437937767],
rho=8.708392897914348130.
```

The corrected estimator is directed and negative, but the full response
interval contains zero. The result is therefore **INCONCLUSIVE STOP**, not
GO, REASSESS, or PIVOT. See
[paper_r_viability_decision.md](paper_r_viability_decision.md) and the
source-bound artifact `experiments/paper_r_response_certificate.json`.

The governing reduction is the exact primal-adjoint identity in
[centrifugal_skyrmion_master_adjoint_enclosure.md](centrifugal_skyrmion_master_adjoint_enclosure.md).
The present positive-radius form-dual result is a diagnostic, not the missing
correlation-aware certificate; see
[validated_centrifugal_adjoint_energy_dual.md](validated_centrifugal_adjoint_energy_dual.md).
The regular-origin adjoint load omitted there is now certified separately in
[validated_centrifugal_origin_adjoint_load.md](validated_centrifugal_origin_adjoint_load.md).

## Frozen Model

Paper R uses one parameter point and one perturbative branch:

```text
x=e f_pi r,
N(x)=1-x^2/R^2,
R=20,
a=4,
mu=1,
lambda=0.0025,
sigma=0.001931779647.
```

The validation artifact must interpret the displayed terminating decimals as
the exact declared inputs, or prove that its outward-rounded input intervals
contain them. Untracked binary64 parameter substitution is not admissible in
the final theorem.

The matter system is the repository's massive `B=1` hedgehog supported by a
positive-tension Nambu-Goto membrane. The background geometry is exact pure
de Sitter and is not solved together with the matter. The background profile
and centrifugal Hessian are those already authenticated by the validated
Skyrmion program; no refit or alternative action is allowed inside the
response proof.

The `ell=2` perturbation uses the regular two-channel field `y=(f,g)`, the
Friedrichs weak form, the center-regular domain, and the ideal-mirror wall
conditions

```text
g(a)=0,
f(a)=-F'_w xi,
f'(a)=beta f(a).
```

The wall is displaced to `x=a+xi q(n)`. Its stress is the distributional
Nambu-Goto stress and includes the displaced background bulk layer. The
normal and tangential traction laws are exactly those derived in
[centrifugal_skyrmion_membrane_stress.md](centrifugal_skyrmion_membrane_stress.md).
There is no surface elasticity, exterior material, finite wall thickness,
anchor UV completion, or independent wall counterterm.

The membrane assumptions are therefore part of the model, not universal
properties of a confining wall. The fixed-background theorem does not impose
tensorial Israel matching. The exact master transmission statement in
[centrifugal_skyrmion_master_response.md](centrifugal_skyrmion_master_response.md)
is used only as a linear fixed-de-Sitter source map.

## Perturbative Meaning

Introduce a formal amplitude `epsilon` multiplying the traceless quadratic
rotation tensor. The matter field, stress, and exterior electric Weyl tensor
have the coefficient expansions

```text
y(epsilon)=epsilon y_2+O(epsilon^2),
delta T(epsilon)=epsilon T_2+O(epsilon^2),
delta E_rr(epsilon)=epsilon E_rr,2+O(epsilon^2).
```

For a classical angular velocity, `epsilon` is of order `Omega_hat^2`. For a
quantized collective state, its traceless tensor is replaced at leading
semiclassical order by

```text
QJ_ab=<{J_a,J_b}>/2-delta_ab <J^2>/3.
```

The theorem target is the coefficient `E_rr,2`, equivalently the second
variation at zero rotation after fixing the repository's tensor convention.
It is not a bound on `delta E_rr(Omega)` at any nonzero `Omega`. In particular:

- `epsilon_rot=e^2 sqrt[j(j+1)]/c_I` is a slow-rotation diagnostic, not a
  certified remainder bound;
- no `O(Omega^4)` energy, field, stress, or metric remainder is enclosed;
- no collective-band/Feshbach error is included; and
- the leading semiclassical mean is not a single-shot quantum-gravity
  observable.

Consequently a completed Paper R may say "the leading response coefficient is
nonzero" but may not say "every sufficiently small finite rotation has a
nonzero response" until a uniform higher-order remainder is proved.

## Exact Continuum Quantity

Let `V` be the frozen Friedrichs form domain and let `q` be the symmetric
centrifugal quadratic form, including its Robin wall term. Let `ell` be the
rotational weak load; its primal wall load is zero. The exact leading
deformation `y` is defined by

```text
q(y,v)=ell(v) for every v in V.
```

The existing coercivity theorem supplies uniqueness for this fixed problem.
Let the exterior-amplitude functional be

```text
B(v)=integral_0^a (b0 dot v+b1 dot v') dx+gamma_B f(a),
A_ext=J_rigid+B(y).
```

The density-derivative endpoint and the contact-free shell term are combined
before interval evaluation. The wall coefficient `gamma_B` is the master
response trace, not the geometrically much larger displacement coefficient
`-1/F'_w`; see
[centrifugal_affine_master_kernel.md](centrifugal_affine_master_kernel.md) and
[validated_centrifugal_wall_master_load.md](validated_centrifugal_wall_master_load.md).

For the horizon-regular exterior homogeneous solution `v_H`, the master
coefficient is

```text
psi_0(x)=A_ext v_H(x/R),  a<x<R.
```

The normalization of `A_ext` depends on the declared `v_H` convention. The
paper's final observable will instead be defined from curvature so that the
theorem does not depend on that convention.

## Frozen Weyl Observable

Fix the exterior static annulus

```text
I_W=[5,10] in the dimensionless radius x.
```

It lies strictly outside the wall and strictly inside the de Sitter horizon.
Here `x` is the dimensionless background areal radius, so the selected annulus
does not depend on a perturbative radial coordinate gauge.
Let `Qhat_ab` be any symmetric traceless tensor with Frobenius norm one and
write `qhat(n)=Qhat_ab n_a n_b`. Then

```text
integral_S2 qhat(n)^2 dOmega=8 pi/15.
```

Let `E_rr,2[Qhat]` denote the leading physical electric-Weyl response per unit
quadrupole tensor. Define its angular projection and dimensionless radial
coefficient by

```text
Pi_Q E(x)=(15/(8 pi)) integral_S2 E_rr,2(x,n) qhat(n) dOmega,

b_W(x)=-(c_I^2 x^3)/(48 pi G e^6 f_pi^4) Pi_Q E(x).
```

The exact reconstruction in
[static_patch_l2_weyl_reconstruction.md](static_patch_l2_weyl_reconstruction.md)
uses the frozen convention

```text
E_rr,2^phys(x,n)=-(48 pi G e^6 f_pi^4/c_I^2)
                  [psi_0(x)/x^3] QJ_ab n_a n_b
```

and gives, for a unit source tensor,

```text
b_W(x)=psi_0(x).
```

The Paper R footprint is the annular root-mean-square coefficient

```text
B_W={1/5 integral_5^10 b_W(x)^2 dx}^{1/2}.             (1)
```

Definition (1) has four deliberate properties:

- it is built from the gauge-invariant linearized Weyl tensor, not a metric
  component or master-field convention;
- it is dimensionless after removing the declared action and gravitational
  scales;
- it factors out the state-dependent magnitude of `QJ`; and
- it is nonzero exactly when the one exterior amplitude is nonzero, because
  `v_H` has fixed positive sign on `I_W`.

For the frozen `R=20` exterior mode, the exact analytic calculation in
[paper_r_weyl_observable.md](paper_r_weyl_observable.md) gives

```text
v_H(s)=(3-s^2)/(2s^2),
(1/5) integral_5^10 v_H(x/20)^2 dx=625/4,
B_W=(25/2)|A_ext|.                                   (2)
```

The exact-rational implementation and focused tests are
[paper_r_weyl_observable.py](../qgtoy/paper_r_weyl_observable.py) and
[test_paper_r_weyl_observable.py](../tests/test_paper_r_weyl_observable.py).
Thus the annular transfer contributes no quadrature or transcendental error.
It transfers a response interval; it does not decide whether that interval
excludes zero.

For an actual anisotropic state, the leading angular-projected physical signal
is obtained by multiplying the unit-tensor response by `||QJ||_F`. For a state
with `QJ=0`, the leading quadrupolar mean signal is exactly zero. `B_W` is thus
a response coefficient of the supported system, not a universal lower bound
on the gravitational cost of every directional state.

## Candidate Theorems

### Theorem R1: certified leading response coefficient

For the frozen model above, let `y` be the unique Friedrichs solution. If the
validated calculation produces a directed interval

```text
A_ext in [A_-,A_+],  A_+<0,
```

then the exact leading fixed-background exterior amplitude is negative and
nonzero. Equation (2) transfers the interval exactly:

```text
B_W in [(25/2)(-A_+),(25/2)(-A_-)],
b_min=(25/2)(-A_+)>0.
```

The numerical endpoints must come from the eventual directed `A_ext`
interval; the annular factor itself is exact. The current floating estimate
`A_ext approximately -0.00281704` is design evidence only and must not appear
as a theorem endpoint.

### Theorem R2: equal-energy state-sensitive response

In the spin-2 band, use the two normalized states already checked in
[skyrmion_tidal_reference_discriminator.md](skyrmion_tidal_reference_discriminator.md):

```text
|cat>=(|2,2>+|2,-2>)/sqrt(2),
|T>=(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2).
```

They have identical

```text
<J^2>=6,  E_rot=3/I,
```

but

```text
QJ_cat=diag(-1,-1,2),  QJ_T=0.
```

This finite-dimensional algebra is now exact rather than floating:

```text
||QJ_cat||_F=sqrt(6),  ||QJ_T||_F=0.
```

The exact radical calculation and conditional interval transfer are in
[paper_r_state_transfer.py](../qgtoy/paper_r_state_transfer.py), with focused
tests in
[test_paper_r_state_transfer.py](../tests/test_paper_r_state_transfer.py).
Given a rational `A_ext` interval and the exact factor `25/2`, that module
returns rational enclosures for the unit-tensor and cat-state footprints and
the exact zero interval for `|T>`.

Conditional on R1, exact collective-state algebra and the Jacobi-limit
identity imply a nonzero leading semiclassical mean tidal coefficient for the
cat state and zero leading quadrupolar mean coefficient for `|T>`. This proves
only

```text
equal Casimir and equal leading rotor energy do not determine the
leading mean tidal footprint.
```

It does not prove that one state is a better reference, that the full finite-
rotation energies remain equal, or that a finite-time noisy detector can
distinguish the states.

R2 is the selected additional physics theorem for the bounded sprint. A
validated open parameter box would strengthen Paper R but is not a substitute
for R2 and is not required for the first viability decision. The R2 algebra
and conditional transfer are closed; its nonzero conclusion remains
conditional on R1 supplying an interval that excludes zero.

## Required Certificate

For conforming rational trials `y_h,z_h`, define

```text
R_y(v)=ell(v)-q(y_h,v),
R_z(v)=B(v)-q(v,z_h),
J_hat=J_rigid+B(y_h)+R_y(z_h).
```

Symmetry gives the exact error identity

```text
A_ext-J_hat=q(y-y_h,z-z_h),
|A_ext-J_hat|<=delta_y delta_z.
```

The final interval may exclude zero only after all of the following are
included:

| Contribution | Required evidence | Current status |
| --- | --- | --- |
| Background profile | authenticated value and derivative enclosures on center and outer cells | certified by the validated profile program |
| Primal origin | cancellation-safe regular-origin load and residual | certified and composed in the all-strong primal representation |
| Adjoint origin | regular-origin master load and loaded weak residual | certified and composed; squared dual contribution `<2.58228030899e-7` |
| Positive-radius primal residual | correlated coefficient/trial representation | certified; complete `delta_y<0.785351351663998829` is the bottleneck |
| Positive-radius adjoint residual | correlation-preserving weak form-dual or Riesz bound | certified; complete `delta_z<0.030892717992632714` |
| Origin/outer interfaces | exact field and residual-conormal cancellation | certified; origin cutoff trace retained where the outer estimator stays weak |
| Wall | representation-compatible primal, adjoint, and estimator terms | certified; weak terms exclude the conormal, all-strong primal uses it |
| Corrected center | directed enclosure of `J_rigid+B(y_h)+R_y(z_h)` | certified negative interval `[-0.003079554319910408,-0.002552931394151071]` |
| Residual product | full-domain `delta_y delta_z` with no omitted load | certified `<0.024261637832088839`; too broad for zero exclusion |
| Collective normalization | exact spin-2 `QJ` algebra and state transfer | exact normalized transfer certified; nonzero state conclusion not certified |
| Weyl transfer | exact inverse map and annular factor in (2) | exact `B_W=(25/2)|A_ext|`; lower bound remains zero |

The regular-origin omission in the earlier partial adjoint lift is now closed
in the same weak representation as the outer adjoint. Its squared contribution
is below `0.000000258228030899`, negligible next to the complete adjoint square
`0.000954360024972333`. The adjoint is no longer the obstacle. The complete
primal norm remains about `9.50` times too large, holding the estimator and
adjoint fixed. That is a proof diagnostic, not evidence of a small or vanishing
physical response.

The correlation-aware redesign must preserve at least the common radial
coordinate through the profile, trial, weak-load coefficients, and completed-
square/Riesz representation. Merely subdividing the existing independent
boxes does not count as the one allowed redesign.

## Error Ledger

The final certificate must report a signed corrected center `J_c` and a total
radius `E_tot` with

```text
A_ext in [J_c-E_tot,J_c+E_tot].
```

At minimum, `E_tot` must cover:

1. the full primal energy-dual residual;
2. the full loaded-adjoint energy-dual residual, including the origin;
3. the primal-adjoint product bound;
4. directed evaluation of `J_rigid`, `B(y_h)`, and `R_y(z_h)`;
5. background-profile tube uncertainty;
6. origin/outer and wall interface terms;
7. the exact Green/Weyl transfer in (2), applied to the final directed
   amplitude interval; and
8. `c_I` physical-prefactor uncertainty if a dimensionful state signal is
   quoted. The normalized state tensors and their conditional transfer are
   exact.

There is no "finite-response error" in R1 because R1 is explicitly a
coefficient theorem. An `O(Omega^4)` remainder must be listed as an excluded
claim, not hidden inside `E_tot` under an unproved estimate.

Every generated artifact must record source hashes, exact parameters,
rounding policy, and the mapping from its interval fields to the terms above.

## Decision Rule

After the one correlation-aware redesign, define

```text
rho=E_tot/|J_c|.
```

Use the following bounded-sprint decision:

- **GO:** `rho<=3/4`, the amplitude interval excludes zero, the annular Weyl
  transfer closes, and R2 is derived from the same normalized coefficient.
- **REASSESS ONCE:** `1<=rho<=3` and the remaining width is demonstrably
  interval wrapping rather than a missing physical term. Record one sharply
  specified follow-up, but do not call Paper R viable yet.
- **INCONCLUSIVE STOP:** `3<rho<=10`. Do not perform a second general redesign
  inside this sprint; archive the diagnostic and default to another direction
  unless one isolated term has an independently justified fix.
- **PIVOT:** `rho>10`, or the dominant uncertainty is a physical ambiguity in
  the wall/source/observable rather than interval wrapping.

An interval that barely excludes zero with `3/4<rho<1` is mathematically
useful but does not meet this contract's "useful margin" for promoting a
standalone paper. It may support a technical note or one targeted refinement
after external review.

## Allowed Claims After GO

Paper R may claim:

- a computer-assisted nonzero theorem for the leading `ell=2` fixed-de-Sitter
  response coefficient of the frozen supported Skyrmion model;
- a gauge-invariant, master-normalization-independent electric-Weyl lower
  bound on the fixed annulus;
- exact sensitivity of that leading mean response to `QJ`, not Casimir alone;
  and
- a rigorous example in which two equal-leading-energy collective states have
  different leading mean tidal footprints.

Paper R may not claim:

- a nonzero response at finite `Omega` without an `O(Omega^4)` bound;
- a universal localization-reference-backreaction inequality;
- an entropy or observer-capacity bound;
- a self-consistent Einstein-Skyrme-membrane solution;
- tensorial Israel matching or regulator independence;
- a finite-time detector discrimination theorem;
- a lower bound for the `QJ=0` branch; or
- a statement about single-shot stress or metric fluctuations.

These boundaries are consistent with the physical normalization note
[centrifugal_skyrmion_physical_response.md](centrifugal_skyrmion_physical_response.md)
and the repository claim ledger
[current_claim_dependency_ledger.md](current_claim_dependency_ledger.md).

## Completion Checklist

The Paper R viability sprint is complete only when:

- [x] the coefficient-level scope, state branch, membrane assumptions, and
  `B_W` normalization are frozen here;
- [x] the regular-origin adjoint load is derived and certified;
- [x] the exact annular transfer `B_W=(25/2)|A_ext|` is proved and tested;
- [x] the R2 spin-2 algebra and conditional exact-rational state transfer are
  proved and tested;
- [x] one correlation-preserving adjoint form-dual/Riesz representation is
  implemented and audited;
- [x] the full corrected amplitude interval includes every entry in the error
  ledger;
- [ ] the annular electric-Weyl interval yields `B_W>=b_min>0`;
- [ ] the closed R2 transfer is instantiated with a certified R1 interval that
  excludes zero;
- [x] the decision rule is evaluated without weakening its thresholds; and
- [x] the manuscript outline is populated only with claims earned by that
  decision.
