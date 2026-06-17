# Prospective Paper U: Finite Directional Records In A Static Patch

Status: claim-hygiene manuscript skeleton. Gates G1 and G2 are specified at an
audit-ready level. A regular-bath finite-switch theorem is proved and a
conditional detector box is certified, but the named KMS QFT channel bridge is
open and the exact
factorized density cannot itself serve as microcausal local matter. The local
IE.4 lift, same-action preparation/readout, and every gravitational extension
remain open. This is an outline, not full manuscript prose.

The static-patch title is prospective. The active theorem note remains a
general symmetric acquisition-disturbance problem until the local KMS lift is
proved.

**Active route decision (2026-06-15).** Do not expand this skeleton into a
submission draft merely by naming assumptions A1--A5 and eliminating their
budgets. The repository already contains that conditional composition. The
next paper-level gate is a new same-acquisition-channel information-exposure
theorem: within one declared covariant acquisition/storage/readout model, low
directional readout risk from an initially symmetric independent record, after
subtracting any nondisturbingly readable classical sector, must force
disturbance of the complete relational source, with the target frame, controls,
failed postselection branches, and every readout path priced. A distinct local
static-patch theorem must then derive that channel and map the disturbance to
KMS exposure. Gravity remains a later optional headline extension.

**ER=EPR literalization decision (2026-06-17).** ER=EPR may motivate the
program, but the present cq record theorem is not an algebraic bridge. The
manuscript must keep the following arrows separate:

```text
directional record -/-> recoverable noncommutative algebra
recoverable algebra -/-> connected geometry
entanglement -/-> a wormhole.
```

An algebraic extension must uniformly recover a specified nonabelian observer
algebra with informationally complete probes and quantum-versus-classical
channel controls. An entanglement-conditioned geometric extension additionally
needs structured-entangled and algebraically separable matched controls; a
scrambled state tests structure only through a fixed decoder or port-resolved
witness. An ER=EPR claim further requires a signed connected-geometry/topology
criterion or a precisely adopted algebraic quantum-wormhole definition from the
same action and state family, plus a quantitative state-uniform
algebra/geometry dictionary. A nonzero Weyl response alone is not connectivity,
and a connected or recoverable algebra does not imply traversability. Until
those gates close, the allowed description is **ER=EPR-motivated**.

## 1. Claim capsule

The paper studies one relational task: estimating the orientation of a
localized target relative to a localized finite register under Haar-prior
full-frame chordal loss.

The closed theorem spine is:

```text
small global relational risk
  -> large actual readout information                       PROVED
  -> finite classical record size, if a classical bottleneck is declared
                                                              CONDITIONAL

small global relational risk
  -> large joint SO(3) asymmetry                           PROVED
  -> representation and energy cost under named matter/spectral premises
                                                              CONDITIONAL
```

The proposed Paper U theorem first adds a quantitative acquisition-disturbance
and retention bound. A local static-patch lift must then derive acquisition and
readout from one microcausal action and control KMS exposure. Optical/proper
support and a physically justified gauge-invariant gravitational quantity are
later extensions, not premises of the base information-exposure theorem. The
detector-EFT result is a reusable channel lemma plus a route-level locality
stop, not a completed lift.

There is not yet one proved function `F_record(S_dir,Gamma,eta)`. The
risk-asymmetry and heat-exposure lower bounds are independent necessities and
may currently be combined only by taking their maximum on a common state and
channel domain. A stronger joint function requires a contraction,
information-disturbance, or same-acquisition-channel theorem.

## 2. Exact domain

The proved U1--U7 inputs use named subclasses of `C_dir` from
`docs/observer_register_model_class.md`. The new acquisition-disturbance
theorem is stated on `C_dir^IE`; a physical local manuscript uses
`C_dir^PaperU`. Their quantifiers range over:

- a gauge-fixed relational `SO(3)` orbit of localized register `O` and target
  `D`;
- arbitrary normal joint states, including invariant correlated memories when
  they are included in the priced state;
- a specified KMS environment and, for physical subclasses, one local action;
- randomized and adaptive protocols whose complete controls and side
  information are inside the resource boundary;
- arbitrary readout POVMs and estimators;
- unconditional risk, or success-weighted postselected performance;
- distinct proper support, optical support, and horizon distance;
- pointwise claims unless an explicit uniformly controlled sequence is stated;
  and
- separately composed operational, perturbative, and gravitational errors.

Charged controllers, hidden frames, and memories that re-enter at readout are
not free. A pre-correlated invariant memory is allowed, but `S_dir` is evaluated
on the complete accessible state and the physical memory enters the action,
support, energy, and gravity ledgers.

## 3. Definitions

For `G~Haar(SO(3))`, orbit state `rho_g=V(g)rho V(g)^*`, readout `Y`, and
estimate `g_hat(Y)`, define

```text
R_Haar = E sin^2[theta(g_hat^-1 G)/2],
S_dir  = A_SO3(rho)=D(rho || G_SO3[rho]),
I_out  = I(G:Y),
C2     = Tr(rho J^2),
K1     = sum_j j Tr(P_j rho).                            (3.1)
```

If the protocol declares a finite discrete classical record `C_T`, also define

```text
d_eff^cl(C_T)=exp[H(C_T)],
m_C=|support(C_T)|.                                     (3.2)
```

The superscript `cl` is mandatory. No quantum, continuous-outcome,
thermodynamic, or gravitational dimension is meant by (3.2).

`S_dir`, `I_out`, `d_eff^cl`, `C2`, `K1`, QFI, thermodynamic entropy, and
Harlow's `S_Ob` are distinct quantities. The complete dictionary and arrow
statuses are in `docs/directional_record_resource_dictionary.md`.

## 4. Main theorem stack

### Theorem U1. Global risk requires readout information - PROVED

Let

```text
c_SO3=6/(e pi^(5/3)),
L(epsilon)=[(3/2)log(c_SO3/epsilon)]_+.
```

Every state and readout in `C_dir^op` obeys

```text
R_Haar<=epsilon => I_out>=L(epsilon).                    (U1)
```

The proof is the `SO(3)` rate-distortion inequality. Its exact dual lower-bound
form retains `sup_lambda{-lambda epsilon-log Z(lambda)}`; equality with the
optimal rate-distortion function is not assumed.

### Theorem U2. Global risk requires joint rotational asymmetry - PROVED

Holevo and relative-entropy data processing give

```text
I_out<=I_acc<=S_dir,
R_Haar>=c_SO3 exp(-2S_dir/3).                            (U2)
```

This holds with arbitrary rotation-trivial multiplicity. It is necessary-only:
large asymmetry does not guarantee a useful protocol or stable record.

### Corollary U3. Finite classical record requirement - CONDITIONAL

If a finite discrete `C_T` is the sole retained information before readout,

```text
G -> C_T -> Y,
```

then

```text
R_Haar<=epsilon
  => H(C_T)>=L(epsilon)
  => d_eff^cl(C_T)>=exp[L(epsilon)]
  => m_C>=ceil(exp[L(epsilon)]).                         (U3)
```

This corollary does not follow from `S_dir` alone. Its classical-bottleneck
assumption must appear in the abstract and theorem statement if U3 is used.

### Theorem U4. Global risk requires representation capacity - PROVED

Independent all-state bounds give

```text
R_Haar>=1/(16C2+8),
S_dir<=B(K1),
K1(K1+1)<=C2.                                           (U4)
```

Thus target risk requires both a mean-Casimir allocation and, through the
asymmetry route, a mean representation-label allocation. Neither allocation is
sufficient for good orientation.

### Corollary U5. Spectral energy cost - CONDITIONAL

For an invariant `H_dir` on the same complete state and representation used in
`S_dir`, with sector floors `epsilon_j` satisfying

```text
Z_H(beta)=sum_j(2j+1)^2 exp(-beta epsilon_j)<infinity,
```

the proved Gibbs inequality yields

```text
S_dir<=beta E_dir+log Z_H(beta),
E_dir>=sup_(beta>0: Z_H(beta)<infinity)
       [L(epsilon)-log Z_H(beta)]_+/beta.                (U5)
```

Covariance alone does not supply the sector growth. The bounded-spectrum
counterexample must be presented next to U5.

### Corollary U6. Confined orbital matter - PROVED on a named domain

For hard-confined spinless nonrelativistic orbital matter with a fixed
nonnegative energy convention
`H_ex>=sum_i p_i^2/(2m_i)`, total rest mass `M`, and radius `a`,

```text
C2<=2Ma^2E_ex,
R_Haar>=1/(32Ma^2E_ex+8).                               (U6)
```

If the model begins with a ground-subtracted `H_gs`, it must exhibit
`Delta>=0` with `H_gs+Delta>=T` as quadratic forms; `E_ex` in U6 then means
`E_gs+Delta`. A later gravitational ledger must count the physical energy and
support costs consistently, without double-counting this offset.

Under the separately declared proxy `2G(M+E_ex)/a<=chi<1`, this implies

```text
R_Haar>=1/[8+2chi^2a^4/G^2].                            (U6a)
```

U6 is the cleanest populated matter subclass. U6a is compactness
admissibility, not a complete gravitational-backreaction theorem.

### Corollary U7. Effective heat exposure - CONDITIONAL

If the actual reduced dynamics is an isotropic rotational heat channel, or is
within operational distance `eta_op` of one, every `G`-dependent,
nontrivially transforming system available at readout must be included in the
capacity. The exposure-input ensemble is the covariant orbit
`sigma_g=U(g)sigma U(g)^*`, and the declared heat convolution acts through the
same `U`; any unheated side system is `G`-independent and rotation-trivial. On
this domain,

```text
R_physical(T)
 >= 3/4[1-exp(-2Gamma)]
    +exp(-2Gamma) R_cap(C_hat)-eta_op,                  (U7)

C_hat=sup_(0<=a<=A) C_max(a,beta)<infinity.
```

Here `R_cap` is any proved nonincreasing initial-risk floor. Hayashi's known
exact mean-Casimir optimum is preferred in paper-facing statements; the
elementary executable choice is `R_cap(C)=1/(16C+8)`. The support envelope is
required unless monotonicity of `C_max` has been proved.

This is an exposure theorem, not a universal elapsed-time limit. Paper U still
needs to derive `Gamma` and `eta_op` from the same acquisition/storage/readout
action.

## 5. Counterexamples and escape routes

The main text includes a compact version of
`docs/observer_register_counterexample_checklist.md`:

| Counterexample | Claim it excludes | Theorem response |
| --- | --- | --- |
| invariant high-spin mixture | Casimir, energy, Hilbert dimension, or von Neumann entropy is sufficient | all such arrows remain necessary-only |
| rare high-spin tail | local QFI certifies global quality | use global asymmetry/mean-label risk |
| bounded-spectrum Hamiltonian | finite energy universally caps orientation | require growing sector floors |
| nontrivial stabilizer | local sensitivity removes global ambiguity | use full-group Haar risk or declare a quotient task |
| success-only postselection | conditional accuracy has its average cost | retain abort or include `p_s` and retries |
| hidden frame or memory | subsystem budgets price an open protocol | close the accessible resource boundary |
| pre-correlated encoder | reduced-register asymmetry prices joint decoding | compute joint `S_dir` |
| QFI/global mismatch | one local metric substitutes for U1-U2 | QFI is absent from the main chain |

These are theorem-design constraints, not afterthoughts.

## 6. What G1 and G2 establish

G1 and G2 establish an audit-ready operational theorem domain, exact
risk-information and risk-asymmetry necessities, a conditional finite
classical-record corollary, and named representation/energy costs.

They do not establish:

- `S_dir=S_Ob` or an inequality between them;
- a classical record dimension for a general quantum register;
- sufficiency of asymmetry, Casimir, mean spin, QFI, or energy;
- a preparation/storage/readout channel from one local action;
- a nonzero physical decoherence rate;
- a preferred gauge-invariant gravitational capacity variable;
- self-consistent static-patch gravity; or
- a certified nonzero exterior Weyl response.

## 7. Remaining Paper U And Extension Gates

### IE. Acquisition-disturbance and retention - ACTIVE

On `C_dir^IE`, prove that net information written into the initially blank
record beyond the nondisturbingly readable classical sector forces quantified
disturbance of the complete `OD` source. Then connect acquisition to retained
quality as in (IE.4). This is the binding theorem gate. U8 is the required
local-action lift for the physical class `C_dir^PaperU`; U9--U10 are optional
gravity-bearing extensions.

### U8. Required local-action static-patch lift - OPEN

To promote the abstract information-exposure theorem to physical Paper U,
derive acquisition, storage, and readout from one rotation-invariant,
microcausal action and map the acquisition disturbance to retained quality or
KMS exposure. U7 and the detector-EFT analysis supply conditional ingredients,
not this complete lift.

#### U8a. Finite-switch storage channel - conditional box, route stopped

For the fixed cutoff-one Peter-Weyl register, inert spin-one target, named
smooth compact pseudoscalar optical prefilter, and explicit compact scalar
switch, target a reduced map of the spatially smeared rigid-detector EFT and a
comparison map from the same factorized pre-switch input:

```text
F_(B,T) = KMS-slice pre-switch-to-final channel,
G_(B,T) = U_free(T) o U_LS(T) o H_s(T) o P_B.
```

Uniform ancilla-stable operator control and tracelessness give the correctly
dimensioned conversion

```text
(1/2)||F_(B,T)-G_(B,T)||_diamond
 <=floor(D_in D_out/2) epsilon_infinity.
```

Here `D_in=D_out=10`, so the factor is `50`, not `1`, `10`, or an unstated
dimension-free constant. Switching and stationary ULE errors are explicit.
Multipole and band errors vanish on the binding rigid-current/hard-compression
model, and the known free and Lamb Casimir unitaries are included exactly.

The conditional open box has nonzero coupling and finite burn-in and storage
intervals, with total normalized diamond error strictly below `0.039`. Each
protocol has finite duration `2R+B+T`; persistence of the detector EFT through
that duration is assumed rather than derived. The box lies inside `0.7<s<1`,
above the U7 failure threshold `s_fail=0.615655...`, and implies

```text
R_physical >= 0.5327532814987301 > 1/2.
```

Conditional on a regulator-uniform KMS GNS/Pauli-Fierz bridge, high-fidelity
retention is excluded on the declared degradation box. That bridge and shorter
exposures remain open. The times are of order `10^30 R`, so this is a formal
parameter regime, not a practical detector window.

The same exact factorization cannot be relabeled as local matter. For distinct
components, disjoint equal-time smearings `f,g` inside the nonzero support obey
`[ell_1(f),ell_2(g)]=i alpha_f alpha_g J_3!=0` on the `V_1` block. This ends
unchanged promotion of the exact-factorized local-current route in
**INCONCLUSIVE STOP** while leaving different local completions open. The binding proof
and parameter ledger are in
`docs/u8a_finite_storage_channel.md`.

#### U8b. Same-action acquisition and readout - OPEN

Derive preparation of the directional token and a final relational instrument
from the same action and controller ledger. The conditional detector analysis grants
these as boundary operations and therefore does not close U8a, full U8, or a
positive observer protocol.

### U9. Optional gravitational extension - OPEN

Select a gauge-invariant functional relevant to finite observer capacity and
derive it from the same state, stress, boundary, and approximation order. Do
not substitute compactness, exterior curvature, horizon displacement, and
generalized entropy for one another.

### U10. Optional common-parameter elimination - OPEN

Only for a gravity-bearing extension, evaluate U1-U9 on one state family and
eliminate internal budgets into a dimensionless compatibility or obstruction
inequality. A one-point failure is not a no-go; a positive construction
requires an open parameter box.

## 8. Manuscript section order

1. **Question, claim, and exclusions.** State the relational task, theorem
   statuses, and non-identifications on the first page.
2. **Observer-register domain.** Define `C_dir`, closed resource boundary,
   protocol rules, postselection, localization, and errors.
3. **Global risk and information.** Prove U1 and U2.
4. **Classical record corollary.** Prove U3 only under the explicit Markov
   bottleneck.
5. **Representation and energy.** Prove U4-U6 and present the bounded-spectrum
   obstruction.
6. **Counterexamples and escape routes.** State the forbidden converses and
   the model assumptions that close each loophole.
7. **Binding information-exposure theorem.** State the result once the
   acquisition, retention, and novelty gates close.
8. **Required local-action static-patch lift.** State U7, the rigid-detector
   degradation theorem, its local-current route stop, and the remaining
   U8a/U8b gaps needed for `C_dir^PaperU`.
9. **Optional algebraic, gravity, and ER=EPR extensions.** Separate algebra
   recovery, proved compactness proxies, the open gravitational functional,
   and every additional connectivity or dictionary premise.
10. **Discussion for observer frameworks.** Ask whether any comparison to
   `S_Ob` is meaningful; do not assume one.

Appendices contain the rate-distortion proof, fusion/Hardy proof, Gibbs
inversion, postselection lemma, error-composition proof, and machine-readable
certificates.

## 9. Removable Candidate Matter Support

The supported massive Skyrmion may appear in a candidate matter-support
appendix only as a realization or source of explicit constants for U5, U7, U8,
or U9. No binding information-exposure or required U8 premise may rely on it
exclusively. Deleting that appendix must leave U1--U7, the binding IE theorem,
and an independent U8 realization intact. The Skyrmion is not part of the
title, abstract claim, or definition of `C_dir`.

The current validated profile and collective calculations are evidence that a
nontrivial localized rotor model exists. They do not identify `S_dir` with
`S_Ob` and do not close the common-action observer theorem.

## 10. Paper R diagnostic

Paper R is recorded only as **INCONCLUSIVE STOP**. Its corrected response
estimator is negative, but the certified full interval contains zero and the
current primal proof object misses zero exclusion by roughly a factor of 9.50
in norm. This is proof-resolution failure, not a vanishing-response theorem.

Consequences for this manuscript:

- no nonzero `B_W` appears as a premise;
- no gradiometer contrast is described as certified;
- no further interval subdivision is a Paper U work package; and
- a future response calculation can return only as optional realization
  evidence after a materially different proof object succeeds.

## 11. Submission gate

The G1/G2 material, rigid-detector channel lemma, and locality route stop are
suitable for expert conceptual review now. They become a base Paper U
submission only if either:

1. the binding information-exposure theorem and required U8 local-action lift
   close for one declared model on an open parameter box; or
2. a controlled family is excluded by a dimensionless theorem whose physical
   premises are jointly realized.

U9--U10 and the algebraic/ER=EPR gates are required only for a headline that
claims the corresponding gravity or connectivity result.

Until then, the correct artifact is a theorem specification and research
manuscript skeleton, not a claimed universal observer-gravity result.
