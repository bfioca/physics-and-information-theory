# Localization Engine for Finite-Pointer Observer Entropy

Status: exact localization theorem passes internally; external proof and
novelty review remain open

This note records the binary channel and operator theorem that supply the
sharp pairwise coefficient for the active finite-pointer paper. For the
finite-pointer purity theorem, Harlow-code insertion, and branchwise gravity
composition, read
[`finite_pointer_observer_entropy.md`](finite_pointer_observer_entropy.md).

## Executive Decision

The mathematical engine is an exact final-support optimization theorem, not
only a one-sided estimate. It is not by itself a submission decision. The exact
gapless-detector channel, its Weyl displacement, and its KMS decoherence factor
are established prior art. The strengthened theorem begins at arbitrary
inverse temperature:

```text
Gamma <= E C_beta(L),
C_beta(L)=2 L Lambda(pi L/beta).                  (1)
```

Here `Lambda(tau)` is the simple top eigenvalue of an explicit positive compact
KMS kernel. For the conformal scalar in de Sitter, `beta=2 pi R`; angular
resolvent order and a separate coordinate-sector estimate make the same s-wave
momentum profile the unique full-phase-space optimizer. In that specialization,

```text
log(1/(2 epsilon_obs)) <= E_K R C_opt(y),
C_opt(y)=2y Lambda(y/2),
y=L/R.                                             (1a)
```

Both coefficients are sharp for fixed final Cauchy support. A source radius
and duration give `L=R atanh(a/R)+T` only as a causal envelope, not an exact
fixed-cylinder controllability claim. `E_K` is the post-switch scalar-field
Killing energy, not total apparatus cost. The Einstein-scalar result is an
appendix application to final-slice data, not a paper gate.

## Frozen Model

On four-dimensional de Sitter space, use the static patch

```text
ds^2=-N(r)dt^2+dr^2/N(r)+r^2 dOmega^2,
N(r)=1-r^2/R^2,
x=R atanh(r/R).
```

Let `phi` be the full conformally coupled massless real scalar in the
Bunch-Davies state. In optical variables its spherical harmonics have radial
operators

```text
A_l=-d^2/dx^2+l(l+1)/[R^2 sinh^2(x/R)],
h_l=sqrt(A_l),
beta=2 pi R.
```

The `l=0` operator is `h_0=sqrt(-d^2/dx^2)` with the regular radial Dirichlet
condition at `x=0`.

Let the pointer be a degenerate qubit with pointer observable `Z_P`. The
interaction is

```text
S_int=-int_M sqrt(-g) J(X) phi(X) Z_P d^4X,        (2)
```

where `J` is real, smooth, and compactly supported in a centered worldtube.
The source is prescribed. A clock, battery, trap, or material actuator that
creates `J` is not part of the frozen model.
Its interaction densities commute at spacelike separation because `Z_P` is
fixed and the scalar field is microcausal. Even so, the same
finite-dimensional operator appears across the smearing. Generic extended
nonrelativistic detector models can violate causal factorization
([arXiv:2102.03408](https://arxiv.org/abs/2102.03408)); localized relativistic
probe fields provide a systematic replacement
([arXiv:2308.11698](https://arxiv.org/abs/2308.11698)). Equation (2) is treated
as a prescribed gapless-detector idealization, not a constructed relativistic
pointer field.

## Exact Channel And Stress

Free-field commutators are c-numbers, so the Magnus series for (2) terminates:

```text
U_J=exp(i Xi[J]) exp[-i phi(J) Z_P].               (3)
```

Tracing the field gives the qubit dephasing channel

```text
D_kappa([[a,b],[c,d]])=[[a,kappa b],[kappa* c,d]],
|kappa|=exp(-Gamma),
Gamma=2 <K E J,coth(beta h/2) K E J>.             (4)
```

The phase of `kappa` is a correctable pointer rotation. Relative to complete
pointer dephasing `D_0`,

```text
epsilon_obs=(1/2)||D_kappa-D_0||_diamond
           =exp(-Gamma)/2.                        (5)
```

`D_0` is the binary quantum-to-classical pointer channel used in the observer
rule of Harlow, Usatyuk, and Zhao
([arXiv:2501.02359](https://arxiv.org/abs/2501.02359)). Here `epsilon_obs`
measures only distance to that ideal channel. It is not their gravitational
encoding error and is not identified with `exp(-S_Ob)`.

After `J` switches off, the conditional field states are opposite coherent
displacements. Their common excess renormalized stress and Killing energy are

```text
Delta <T_ab^ren>=T_ab[phi_J],
E_K=<K E J,h K E J>.                              (6)
```

The state-independent Hadamard subtraction cancels in the difference. Equation
(6) prices the emitted scalar field, not the work or stress of the external
agent that implements the source.

## Partial-Wave Formulas

Let `(q_lm,p_lm)` be the final Cauchy data of the rescaled partial waves. Their
positive contributions are

```text
Gamma_lm=<q_lm,h_l coth(beta h_l/2) q_lm>
        +<p_lm,h_l^-1 coth(beta h_l/2) p_lm>,      (7)

E_lm=(1/2)[||h_l q_lm||^2+||p_lm||^2].           (8)
```

Both `Gamma` and `E_K` are the sums over `(l,m)`. For `l=0`, the unitary sine
transform gives the equivalent explicit integrals

```text
Gamma_00=int_0^infinity coth(beta k/2)
         [k |qhat(k)|^2+|phat(k)|^2/k] dk,

E_00=(1/2)int_0^infinity
     [k^2 |qhat(k)|^2+|phat(k)|^2] dk.
```

If the source lies in `0<=x<=ell` for a static-time interval of length `T`,
finite propagation gives final support in

```text
0<=x<=L,
ell=R atanh(a/R),
L=ell+T.                                          (9)
```

## General Thermal Theorem and de Sitter Specialization

Let `P_L` be multiplication by the interval `[0,L]`. The two compressed
inverse kernels needed below are

```text
P_L h^-1 P_L(x,y)=(1/pi)log[(x+y)/|x-y|],
P_L h^-2 P_L(x,y)=min(x,y).                       (10)
```

The first kernel is positive. Its Schur row integral has maximum at
`x/L=1/sqrt(2)`, while the second kernel is the Green kernel for a Dirichlet-
Neumann interval problem. Hence

```text
||P_L h^-1 P_L|| <= 2 L asinh(1)/pi,
||P_L h^-2 P_L||  = 4 L^2/pi^2.                  (11)
```

The complete finite-temperature momentum kernel can also be summed exactly:

```text
P_L h^-1 coth(beta h/2) P_L(x,y)
 =pi^-1 log{sinh[pi(x+y)/beta]/sinh[pi|x-y|/beta]}.
                                                               (11a)
```

With `x=Lu`, `y=Lv`, and `tau=pi L/beta`, define the dimensionless operator

```text
k_tau(u,v)=pi^-1 log{sinh[tau(u+v)]/sinh[tau|u-v|]},
Lambda(tau)=||K_tau|| on L2(0,1).                 (11b)
```

The logarithmic singularity is square integrable, so `K_tau` is compact. Its
kernel is positivity improving; hence `Lambda(tau)` is simple and has a unique
strictly positive normalized eigenfunction up to sign.

For half-line momentum data with `E=||p||^2/2`, the exact arbitrary-temperature
coefficient is

```text
C_beta(L)=sup_p Gamma_beta[p]/E[p]
         =2 L Lambda(pi L/beta).                 (11c)
```

It obeys

```text
max{3L/pi,16L^2/(beta pi^2)}
 <= C_beta(L)
 <= 4 asinh(1)L/pi+16L^2/(beta pi^2),            (11d)

0<=C_beta(L)-2L Lambda(0)<=2 pi L^3/(3 beta^2),
0<=C_beta(L)-16L^2/(beta pi^2)<=beta/3.           (11e)
```

This is the general thermal half-line theorem. The next step is specific to
the conformal de Sitter geometry.

The angular potential is nonnegative, so `A_l>=A_0`. More strongly, the
Mittag-Leffler expansion gives

```text
h_l^-1 coth(beta h_l/2)
 =(2/beta)A_l^-1
  +(4/beta)sum_[n>=1](A_l+(2 pi n/beta)^2)^-1.   (11f)
```

Every resolvent is order decreasing. Thus the exact `l=0` thermal momentum
kernel dominates all higher angular sectors.

Using `coth u<=1+1/u`, equations (7)-(11f), and summing the positive
partial-wave estimates gives the convenient fully elementary upper bound

```text
Gamma
 <= 4 asinh(1)L E_K/pi
    +16 L^2 E_K/(beta pi^2).                      (12)
```

At the de Sitter temperature `beta=2 pi R`, (12) gives the final explicit
upper bound in (1), but the exact coefficient is smaller and is determined by
`Lambda`.

### Proof Details

The elementary momentum upper bound follows because `p_lm=P_L p_lm` and
`A_l>=A_0`. Equations (10)-(11) give, in every sector,

```text
<p_lm,h_l^-1p_lm><=[2 L asinh(1)/pi]||p_lm||^2,
<p_lm,h_l^-2p_lm><=[4 L^2/pi^2]||p_lm||^2.       (12a)
```

The field coordinate requires a different argument: `h_l` is nonlocal, so
`h_l q_lm` must not be treated as compactly supported. Since finite-energy
`q_lm` extended by zero lies in `H_0^1(0,L)`, the nonnegative angular
potential, Dirichlet Poincare, and Cauchy-Schwarz give

```text
||q_lm|| <= (L/pi)||h_l q_lm||,
<q_lm,h_l q_lm>
 <= ||q_lm|| ||h_l q_lm||
 <= (L/pi)||h_l q_lm||^2.                        (12b)
```

These field-coordinate constants, `L/pi` and `L^2/pi^2`, are strictly smaller
than the corresponding momentum constants in (12a). Applying the larger
momentum constants to both positive energy components, and accounting for the
one half in (8), gives (12). In particular, no unsupported locality property
of the fractional operator `h` enters the proof.

For reference, the thermal field-coordinate identity is simply

```text
||q_lm||^2 <= (L^2/pi^2)||h_l q_lm||^2.
```

No source amplitude or microscopic coupling remains.

The exact optimization is stronger. For s-wave momentum data, scaling (11a)
to the unit interval gives

```text
sup_p Gamma_p/(E_p R)=2y Lambda(y/2).             (12c)
```

Equation (11f) excludes a larger higher-angular value. The coordinate bound
from (12b) is

```text
C_q(y)<=2y/pi+2y^2/pi^3.                          (12d)
```

Two momentum trials give

```text
C_p(y)>=max{3y/pi,8y^2/pi^3}.                     (12e)
```

The linear term in (12e) dominates (12d) for `y<=pi^2/2`; the quadratic term
dominates for `y>=pi^2/3`. These intervals overlap, so the s-wave momentum
sector is the full phase-space optimum for every `y>0`:

```text
C_opt(y)=2y Lambda(y/2).                           (12f)
```

The maximum row integral of (11b) gives an explicit Schur bound. Its unique
maximizing row is

```text
u_tau=asinh[sinh(tau)/sqrt(2)]/tau.               (12g)
```

Euler's product for `sinh` and the thermal Green-kernel limit also give the
global remainder estimates

```text
0<=C_opt(y)-2y Lambda(0)<=y^3/(6 pi),
0<=C_opt(y)-8y^2/pi^3<=2pi/3.                     (12h)
```

Thus the thermal correction is cubic at small support, and `8/pi^3` is the
sharp quadratic coefficient at large support.

Immediate consequences are

```text
E_K R >= log(1/(2 epsilon_obs))/C_opt(y),          (13)
C_opt(y)=2y Lambda(y/2)<=F(y),
```

and the finite-support no-go

```text
epsilon_obs=0 and L<infinity imply E_K=infinity.   (14)
```

This is a no-go only for exact complete dephasing in the frozen local scalar
model. It is not a universal energy cost of measurement.

### Explicit Sharp Brackets

The two elementary momentum profiles and the explicit upper bounds give

```text
max{3y/pi,8y^2/pi^3} <= C_opt(y)
 <= min{F(y),2y M(y/2),
        4 asinh(1)y/pi+y^3/(6pi),
        8y^2/pi^3+pi}.                            (14a)
```

Here `M(tau)` is the maximum row integral of (11b), evaluated at (12g). As
`y->0`, the ratio between the analytic upper and constructive lower linear
coefficients is at most

```text
4 asinh(1)/3 = 1.175163... .                       (14b)
```

The coefficient itself is sharp by (12f); the 18 percent refers only to the
closed-form bracket on its vacuum limit.

## Smooth Source Realization

The theorem is stated in terms of final data but does not assume arbitrary
data can be produced by a source with the declared support. That realization
can be made explicit. Choose smooth compact target data `(q=0,p=f)` supported
strictly inside the optical worldtube. Let `phi_free` be the homogeneous
solution with those final data, choose a smooth time cutoff `eta` that is zero
before the protocol and one near the final slice, and set

```text
J=P(eta phi_free),                                 (15)
```

where `P` is the conformal wave operator. The retarded solution of (15) is
`eta phi_free`, so it has exactly the target final data. Finite propagation
keeps `J` inside the declared worldtube when the cutoff transition is shorter
than the optical-radius margin between the target support and the wall.

Neither the top eigenfunction nor the ideal profiles used below create a
source-admissibility gap. Smooth normalized profiles supported strictly inside
`ell` are dense in `L2(0,ell)`. Choose `p_n` converging to the desired profile.
On `[0,ell]`,

```text
P_ell h^-1 coth(beta h/2) P_ell
 <= P_ell h^-1 P_ell+(2/beta)P_ell h^-2 P_ell
```

as quadratic forms, and the right side is bounded by (11). The dephasing
covariance is therefore continuous in `L2`. Moreover,

```text
sup_x |int_0^x (p_n^2-p^2) ds|
 <= ||p_n-p||_2 (||p_n||_2+||p||_2),
```

so cumulative mass and the strict constraint margin converge uniformly.
Applying (15) to each `p_n` produces a smooth compact spacetime source when the
source ball contains the target support with a strict transition margin. This
closes smooth realization for the sharp final-support problem. It does not
prove that every optimizer is reachable from a strictly smaller radius
`ell=L-T`, and it still does not price the actuator implementing the source.

## Spherical Constraint Corollary

For spherical final data `q=0`, the physical scalar vanishes across the final
slice. With the standard normalized radial field, its physical normal
derivative and conformal stress are

```text
phi=0,
n(phi)=p(x)/[sqrt(4 pi) r sqrt(N)],
rho=T_ab n^a n^b=n(phi)^2/2,
j_i=-T_ab n^a h^b_i=0.                            (15a)
```

Since `dr=N dx`, the exact mass measure is

```text
4 pi r^2 rho dr=(1/2)p(x)^2 dx.                   (15b)
```

Thus a vanishing-extrinsic-curvature `K_ij=0` slice satisfies the momentum
constraint and its Einstein-scalar Hamiltonian-constraint mass obeys
`m(b)=E_K`. The nonzero scalar normal momentum means the full data are not
time-reflection symmetric. If the support
ends at areal radius

```text
b=R tanh(L/R),
```

the exact radial Hamiltonian-constraint variable at the wall is

```text
Q_grav(b)=2 G E_K/[b(1-b^2/R^2)].                 (16)
```

Define the local comparison norm
`Q_b=sup_{0<r<=b} Q_grav(r)`. Since `Q_b>=Q_grav(b)`, equations (13) and
(16) give a necessary constraint cost. Conversely, imposing
`Q_b<=delta<1` yields

```text
epsilon_obs >= (1/2) exp{
 -delta b(1-b^2/R^2) R C_opt(y)/(2G)}.            (17)
```

Equations (15a)-(17) construct exact self-consistent Einstein-scalar
Hamiltonian and momentum constraint data on the final slice. They do not solve
the lapse equation, include the stress of the source actuator, evolve the
coupled system, or rederive the observer channel on the perturbed geometry.
The compact mass shifts the cosmological horizon, so `Q_b` is only a local
comparison with the pure-de-Sitter metric on the ball containing the datum;
no global smallness statement relative to the unperturbed horizon is made.
Calling them a full self-gravitating observer-channel theorem would be an
overclaim.

## Explicit Nonempty Window

Let `ell=R atanh(a/R)` be the source optical radius. An ideal flux-free final
profile is

```text
q(x)=0,
p(x)=A sqrt(3/ell^3) x,  0<x<ell.                (18)
```

For the normalized profile, direct integration of the positive kernel (10)
gives

```text
<p,h^-1p>=3ell/(2 pi),                            (19)
```

using

```text
int_0^1 t log[(1+t)/(1-t)] dt=1.
```

Thermality only increases the covariance. Therefore a target exponent
`Gamma` is reached with

```text
E_K <= pi Gamma/(3ell).                           (20)
```

The cumulative mass is `m(x)=E_K(x/ell)^3`, and

```text
Q_grav(r) proportional to
atanh(r/R)^3/[r(1-r^2/R^2)]
```

is strictly increasing within the support ball. Its wall value and (20)
provide an explicit local weak-constraint upper bound. Smooth profiles
supported just inside `ell`
approximate (18)-(20); every strict margin survives, and construction (15)
then supplies a smooth compact source.

For the frozen illustrative point

```text
epsilon_obs=1e-6,
a/R=0.2,
T/R=0.1,
G/R^2=1e-6,
delta=0.25,
```

the certificate reports

```text
L/R                         =0.30273255405408217,
F(L/R)                      =0.3633724335809033,
explicit C_opt upper        =0.3407665703742031,
necessary E_K R             =38.50836472308413,
necessary wall Q_grav       =0.0002868962683029999,
constructive E_K R upper    =67.78243809360733,
constructive local Q_a upper=0.0007060670634750763.
```

Thus this parameter point has a nonempty local fixed-background
weak-constraint window. It is not evidence that the unmodeled actuator also
fits the same budget.

## Prior Art And Candidate Novelty

The following claims are not new:

- Landulfo's exact relativistic communication model and Barcellos and
  Landulfo's energy analysis already use compactly supported gapless detector
  couplings, exact Weyl evolution, KMS decoherence, and switching work:
  [arXiv:2109.13896](https://arxiv.org/abs/2109.13896).
- Harlow, Usatyuk, and Zhao already use complete dephasing in a stable pointer
  basis as the ideal quantum-to-classical observer channel:
  [arXiv:2501.02359](https://arxiv.org/abs/2501.02359). This paper only
  quantifies one field-mediated approximation to that target.
- Batista, Landulfo, Mann, and Matsas give a recent nonperturbative finite-time
  gapless-detector treatment of DSW decoherence:
  [arXiv:2605.00956](https://arxiv.org/abs/2605.00956).
- Danielson, Satishchandran, and Wald formulate Killing-horizon decoherence and
  its local two-point-function description:
  [arXiv:2301.00026](https://arxiv.org/abs/2301.00026) and
  [arXiv:2407.02567](https://arxiv.org/abs/2407.02567).
- Li computes the local scalar, electromagnetic, and gravitational de Sitter
  decoherence factors:
  [arXiv:2501.00213](https://arxiv.org/abs/2501.00213).
- Ruzhansky and Suragan study largest eigenvalues and isoperimetry for positive
  Riesz-potential operators on spherical and hyperbolic geometries:
  [arXiv:1603.07781](https://arxiv.org/abs/1603.07781). Compactness,
  positivity, and a Perron top eigenfunction are therefore mathematical setup,
  not proposed novelty.

The candidate new claim is narrower:

```text
arbitrary beta + fixed final half-line support
 -> C_beta(L)=2 L Lambda(pi L/beta),
    with a unique positive optimizer and uniform support asymptotics;

conformal de Sitter beta=2 pi R
 -> the same profile is the unique full angular/canonical optimizer,
```

with the flux-free Einstein-scalar constraint construction retained only as an
appendix application. The current search found no equation-level prior result
for the reflected thermal kernel, general-temperature coefficient, full
canonical/angular reduction, and support asymptotics together, but search
absence is not a novelty proof. Independent reviews in detector/QFT and
operator theory remain mandatory.

### Relation To Bekenstein-Type Bounds

Hollands, Longo, and Morsella prove

```text
S(Phi|B)<=2 pi L E
```

for a Klein-Gordon wave packet localized in a region of half-width `L`:
[arXiv:2602.03606](https://arxiv.org/abs/2602.03606). Their `S` is the entropy
quadratic form of a local standard subspace, equivalently the relative entropy
of the corresponding coherent excitation. This is directly adjacent and rules
out any claim that (1) is the first localization-information-energy bound in
QFT.

It does not directly subsume (1). At zero temperature, `Gamma` is twice the
global one-particle norm of the conditional displacement, often interpreted as
an entangling-particle count. At finite temperature it contains the KMS factor
`coth(beta h/2)` and can increase even when thermal state distinguishability
decreases. The Bekenstein entropy and the pointer characteristic-function
exponent are therefore different quadratic forms. Equation (1) must be
presented as an operational dephasing analogue, not as a replacement for the
Bekenstein bound.

Their inequivalence can be made sharp already for radial `q=0` data in a
four-dimensional Minkowski ball of radius `a`. Normalize `||p||_2=1`. The
massless conformal-ball entropy and vacuum dephasing form are

```text
S_B[p]=pi/(2a) int_0^a (a^2-x^2)p(x)^2 dx,
Gamma_0[p]=<p,h^-1p>.                             (21)
```

For a positive smooth `f` compactly supported in `(0,1)`, put

```text
p_delta^wall(x)=delta^-1/2 f((a-x)/delta).
```

The entropy weight vanishes linearly at the boundary, while the logarithmic
kernel (10) retains its diagonal singularity:

```text
S_B[p_delta^wall]
 =pi delta int_0^1 u f(u)^2 du+O(delta^2),

Gamma_0[p_delta^wall]
 =delta (int_0^1 f(u)du)^2 log(1/delta)/pi+O(delta).
                                                               (22)
```

Hence `Gamma_0/S_B->infinity`. Conversely, for
`p_delta^center(x)=delta^-1/2 f(x/delta)`,

```text
S_B[p_delta^center]->pi a/2,
Gamma_0[p_delta^center]=O(delta),                 (23)
```

so `S_B/Gamma_0->infinity`. Neither quadratic form uniformly bounds the other
at fixed radius. This separation is why the Bekenstein theorem neither proves
nor is strengthened by (1).

## Submission Gates

| Gate | Current status | Required closure |
| --- | --- | --- |
| Exact local channel | Pass, prior art | Present as setup, not novelty |
| Same-source field stress and energy | Pass after switch-off | Keep actuator exclusion explicit |
| General-`beta` half-line momentum theorem | Clean-room derivation pass | External proof coverage |
| Conformal de Sitter all-sector reduction | Clean-room angular and coordinate audit pass | External proof coverage |
| Small- and large-support scaling | Sharp leading terms pass | Closed form for finite-support eigenvalue is optional |
| Numerical realization | Production Galerkin and independent product-integration grids pass | Keep both separate from the rigorous analytic bracket |
| Smooth compact realization | Analytic density pass | Include the bounded-form and uniform-mass proof |
| Final-slice gravity and local weak-constraint window | Exact appendix application | Keep secondary; not a submission gate |
| Autonomous actuator | Outside narrow scope | Keep excluded from the field-energy claim |
| Bekenstein comparison | Analytic separation pass | Frame `Gamma` as a distinct dephasing functional |
| Detector/QFT novelty | Internally mapped, externally open | Written specialist disposition |
| Operator-theory novelty | Eight reductions tested, externally open | Written specialist disposition |
| Standalone manuscript | Ready for external review; submission held | Close both novelty gates and external proof coverage |

The current verdict is **GO TO EXTERNAL REVIEW / HOLD SUBMISSION**. A
**SUBMIT** decision is not issued by the executable certificate or the
clean-room audit.

## Reproduction

```bash
PYTHONPATH=. python experiments/local_scalar_observer_cost_audit.py
PYTHONPATH=. python experiments/local_scalar_observer_spectrum.py
PYTHONPATH=. python experiments/local_scalar_observer_clean_room_check.py
PYTHONPATH=. python -m pytest -q \
  tests/test_local_scalar_observer_clean_room_check.py \
  tests/test_local_scalar_observer_cost.py \
  tests/test_local_scalar_observer_manuscript.py \
  tests/test_local_scalar_observer_spectrum.py
python -m json.tool \
  experiments/local_scalar_observer_cost_certificate.json >/dev/null
```

Frozen artifact:

```text
experiments/local_scalar_observer_cost_certificate.json
SHA256 b06be2a789b675e2cc2575e38a6960fcf62e66045a3b10f0520f5c6043bb8547
```
