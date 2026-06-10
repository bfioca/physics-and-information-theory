# Observer-Register Model Class

Status: audit-ready domain specification for Paper U gates G1 and G2. The
operational statements below are pointwise theorems. A common-action
semiclassical-gravity realization remains open.

## 1. Purpose and theorem quantifiers

`C_dir` is not shorthand for every physical observer. It is the union of named
subclasses of the following tuples:

```text
m = (B, X, V, S, I, U, omega_E, P, Loc, Grav, Err).
```

Here `B` is the background, `X` the system list, `V` the relative rotation
representation, `S` the admissible state family, `I` the microscopic action or
the explicit operational placeholder `None`, `U` the allowed controls,
`omega_E` the environment state, `P` the protocol family, `Loc` the proper and
optical localization conventions, `Grav` the gravitational functional and
budget, and `Err` the approximation ledger. The basic theorem
quantifies as follows:

> For every `m in C_dir`, every admissible prepared state `rho in S_m`, every
> duration `T` in the declared time interval, every allowed randomized or
> adaptive protocol `Pi in P_m(T)`, every readout instrument in that protocol,
> and every estimator `g_hat`, the actual unconditional Haar-prior risk obeys
> the operational bounds whose hypotheses are satisfied by `m`.

No statement is obtained by choosing a favorable protocol after learning the
unknown orientation. All preparation maps, control policies, stopping rules,
and readout instruments are fixed before the Haar variable is sampled.

The current theorem domain is the integer-spin `SO(3)` sector. A projective
`SU(2)` sector has separate constants and is optional realization support; it
is not used in the Paper U headline.

## 2. Background, systems, and relative action

### 2.1 Static-patch background

`B` specifies a fixed de Sitter static patch for the G1/G2 operational theorem:

```text
B = (M, g_0, K, Sigma_t, N, R, W, [0,T_max]).
```

Here `K` is the static Killing field, `N=sqrt(-g_0(K,K))` is the lapse,
`Sigma_t` is the selected static foliation, `R` is the de Sitter radius, and
`W` is the protocol worldtube. A dynamical metric is permitted only in a named
subclass that replaces these fixed-background objects by relationally defined
ones and supplies a diffeomorphism-invariant budget.

### 2.2 Quantum systems

`X` lists separable quantum systems or equivalent normal-state algebras:

| Symbol | Role | Resource rule |
| --- | --- | --- |
| `O` | localized directional register | always included in support, energy, and action ledgers |
| `D` | localized target or detector carrying physical markers | included in the physical ledgers; used as the gauge anchor for relative orientation |
| `E` | field environment | initialized in the declared KMS state and inaccessible after tracing unless explicitly promoted to an accessible memory |
| `A` | rotation-invariant ancillas, classical randomness, and invariant memories | arbitrary dimension and arbitrary correlation with `O` are allowed; the full state is used below, and every physical memory enters the action, support, energy, and gravity ledgers |
| `C_ch` | charged controllers, directional ancillas, or external frames | never free; included in the directional, support, energy, and gravitational ledgers |

Write `R_acc=O tensor D tensor A tensor C_ch` for every system available to the
protocol after encoding; `E` is excluded unless it is explicitly promoted to
`R_acc`. After fixing the target `D` as the relational gauge anchor, the unknown
relative orientation is `G~Haar(SO(3))` and is encoded by

```text
rho_g = V(g) rho V(g)^*,
V(g) = direct_sum_j V_j(g) tensor identity_(M_j).        (2.1)
```

The multiplicity spaces `M_j` contain `A`, gauge-fixed target degrees of
freedom, and any other systems on which the relative action is trivial. Every
accessible subsystem whose conditional state depends on `g` must occur in the
joint state `rho` and in (2.1). This is a gauge-fixed orbit of two physical
systems, not orientation relative to coordinates.

### 2.3 Side information and correlations

The prepared state `rho` may be mixed and may correlate `O` with an invariant
memory `A`. The priced directional resource is then the joint quantity

```text
S_dir(rho) = A_SO3(rho)
           = D(rho || G_SO3[rho]),
G_SO3[rho] = integral dg V(g) rho V(g)^*.                (2.2)
```

It is not generally valid to replace (2.2) by `A_SO3(rho_O)`. For example, the
reduced state of one half of a maximally entangled spin pair is invariant while
the joint orbit produced by rotating that half carries orientation
information.

An independent abstract random seed may be free in `C_dir^op`. Any material
implementation of that seed or its transcript in `C_dir^PaperU` is a physical
memory and enters the action and physical budgets.

Pre-correlated memories are therefore allowed only under one of these rules:

1. an invariant accessible memory is included in `rho`, the joint
   `S_dir(rho)`, and every physical ledger;
2. a nontrivially rotating memory is included in `C_ch` and every resource
   ledger; or
3. a memory unavailable at readout is traced out and cannot later re-enter.

A hidden memory or external frame that re-enters at readout is outside
`C_dir`. Promoting it to an explicit, priced subsystem restores membership.

The fresh-environment subclass uses `rho_R_acc tensor omega_E` at the initial
time. An initially system-environment-correlated subclass must state its joint
state family and prove its reduced protocol map; the usual product-state CPTP
or KMS approximation cannot be imported automatically.

## 3. Environment and action

In the purely operational subclass, `E` may be the trivial system and
`omega_E=1`. A physical static-patch subclass instead supplies a specified KMS
state for the chosen environment algebra and static flow. Temperature alone is
not a noise model.

`I=None` is permitted only in `C_dir^op`, where the theorem is uniform over
abstract `g`-independent channels and makes no physical realization claim. A
physical member must replace it by one declared local action on the time slab,
including

```text
I = I_O + I_D + I_E + I_support + I_int + I_ctrl.        (3.1)
```

That action names the support or membrane degrees of freedom as well as the
register-field and detector-field couplings. Its stress tensor and Killing
charge conventions are part of the model tuple. A heat channel, a switching
profile, and a readout map count as physical Paper U inputs only when their
distance from the reduced dynamics of (3.1) is bounded.

`U` is the allowed control set. It may contain local scalar switching schedules,
invariant feedback, and finite-dimensional quantum controllers. A spatially
oriented field, polarized drive, gyroscope, laboratory frame, or noncovariant
controller is included in `C_ch`; its state and costs cannot be hidden inside
the word "control." Controls cannot depend on the unknown `g` except through
earlier outcomes generated by the same protocol.

For G1/G2 alone, allowing a larger set of final POVMs only strengthens the
lower bounds. The common-action manuscript claim is narrower: it uses only
instruments realizable by (3.1) and `U`.

## 4. Preparation, storage, and readout protocols

An allowed protocol is a causal comb with these stages:

1. **Preparation.** A `g`-independent channel prepares an admissible `rho` and
   the declared KMS environment. Its directional controllers have already been
   included in `C_ch`.
2. **Relative encoding.** The mathematical orbit (2.1) parametrizes the
   physical relative orientation.
3. **Storage and interaction.** Any finite sequence of local instruments,
   invariant ancillas, feedback maps, and stopping decisions from `U` is
   allowed. Later choices may depend on earlier classical outcomes but not on
   `g` directly.
4. **Readout.** A final instrument produces a classical transcript `Y`, an
   estimate `g_hat(Y)`, and optionally a success flag `B`.

Independent classical randomization is allowed and is represented by a
rotation-invariant ancilla. Adaptive protocols are allowed: deferred
measurement absorbs their full transcript into one instrument, so the
all-POVM information bound still applies. Unlimited invariant multiplicity
does not weaken the existing `SO(3)` theorem.

## 5. Risk and postselection

Let `theta(x)` be the principal rotation angle. The headline loss and risk are

```text
c(g,g_hat) = sin^2[theta(g_hat^-1 g)/2] in [0,1],
R_Haar(Pi,rho,T) = integral dg sum_y p(y|g)c(g,g_hat(y)). (5.1)
```

For continuous outcomes, replace the sum by the corresponding probability
kernel. "Global" means the Haar prior and the full-group loss in (5.1); it does
not mean an absolute frame.

Postselection is allowed, but it is not free. The primary performance number
is unconditional. An abort is followed by an independent Haar-random guess,
whose mean loss is `3/4`, so

```text
R_uncond = p_s R_success + (1-p_s) 3/4.                 (5.2)
```

Alternatively a paper may report `(p_s,R_success)` as a pair. A conditional
risk without its success probability is not an admissible theorem conclusion.
If the success instrument is covariant, `p_s` is independent of `g` and the
conditional prior remains Haar. In that case the proof note in
`directional_record_resource_dictionary.md` gives

```text
S_dir >= p_s [3/2 log(c_SO3/R_success)]_+.              (5.3)
```

For a noncovariant success event the conditional prior need not be Haar; only
the unconditional theorem is used unless a new prior-dependent bound is
proved.

## 6. Resource and budget ledgers

No two rows in this table are identified by notation.

| Ledger entry | Definition in a member of `C_dir` |
| --- | --- |
| directional resource | joint `S_dir=A_SO3(rho)` from (2.2) |
| representation moments | `C2=Tr(rho J^2)` and `K1=sum_j j Tr(P_j rho)` |
| directional-system energy | ground-subtracted `E_dir=Tr(rho H_dir)` for an invariant Hamiltonian on the same `R_acc`, state, and representation used to define `S_dir` |
| total Killing budget | excess Killing charge of register, detector, every physical invariant memory, support, and charged controls, with bath subtraction declared |
| proper support `a` | supremum in time of the smallest `h`-geodesic ball about the declared center containing the hard support of excess stress and all protocol couplings |
| optical support `s_opt` | the analogous radius in `h_opt=N^-2 h` |
| horizon distance `rho_h` | proper distance from the center worldline to the static-patch horizon on the selected slice |
| gravitational budget | a named functional `G_m` of the gauge-equivalence class of the state, stress, boundary, and metric history, with threshold `G_m<=g_*` |

`E_dir` and total Killing energy are not automatically equal. A realization
must prove the comparison it uses. Hard support is the current theorem domain.
A soft-tail extension must name a leakage functional and show how its error
enters both the operational and gravitational ledgers.

There is no universal `G_cap` in G1/G2. A gravitational subclass must supply a
functional and justify its relevance. Examples may include a spherical
areal-radius mass ratio, a horizon or QES displacement, or an exterior tidal
observable, but these are not interchangeable. The fixed-background `B_W`
response is not required for membership and no certified nonzero `B_W` is used.

## 7. Proper versus optical localization

Proper and optical radii remain separate inputs. If the same protocol support
lies in an optical ball and `N_+` is the supremum of the lapse on that ball,
then `h=N^2 h_opt` gives the exact geometric implication

```text
a <= N_+ s_opt.                                         (7.1)
```

Equation (7.1) is one-way and applies only to the same center, time slice, and
support set. It does not turn an optical interaction range into material
support unless the action proves that the two supports coincide. Near-horizon
limits must keep `rho_h`, `s_opt`, and the lapse extrema explicit.

## 8. Approximation and error composition

The G1/G2 risk-information statements are exact for the actual orbit ensemble
and readout distribution. Effective dynamics are handled with a separate
operational error ledger.

Use the convention

```text
d_diamond(N,M) = (1/2)||N-M||_diamond.
```

For fixed causal wiring, preparation, storage, and readout errors telescope:

```text
eta_op <= delta_state + eta_prep + eta_store + eta_read. (8.1)
```

For a genuinely adaptive comparison, the same statement must be supplied in
the strategy/comb norm, or each stage must have a diamond bound uniform over
all histories. Since (5.1) has loss in `[0,1]`, total-variation contraction
gives

```text
R_physical >= max(0, R_effective-eta_op).                (8.2)
```

Errors in stress, metric response, or junction conditions are compared with
their own dimensionally compatible margins; they are not added to `eta_op`.
Conditioning may amplify channel error by inverse powers of `p_s`, so no
conditional approximation statement is inherited from (8.1) without a
declared lower bound on success probability.

Every approximate subclass declares a parameter box `Theta`, an expansion
parameter `lambda`, an order `k`, and uniform remainder bounds on `Theta`.
Quantities combined in one corollary must be controlled on the same box and at
the same order.

## 9. Pointwise and asymptotic scope

All currently proved G1/G2 arrows are pointwise: they hold for each fixed
`(m,rho,Pi,T)`. An asymptotic obstruction is a separate corollary about an
explicit sequence `(m_n,rho_n,Pi_n)` and must state:

1. which parameters tend to a limit;
2. which model assumptions and constants are uniform in `n`;
3. how `eta_op,n` and gravitational remainders scale; and
4. which liminf inequality is violated.

Failure of one parameter point is not an asymptotic no-go.

## 10. Populated subclasses and current status

| Subclass | Additional hypotheses | Current result |
| --- | --- | --- |
| `C_dir^op` | orbit (2.1), arbitrary normal joint state, arbitrary readout | risk-to-information, risk-to-asymmetry, and risk-to-Casimir arrows **PROVED** |
| `C_dir^cl` | a finite discrete classical record is a Markov bottleneck before readout | classical entropy/alphabet lower bound **CONDITIONAL** on this declared bottleneck |
| `C_dir^spec` | invariant `H_dir` on the complete `R_acc` representation has sector floors with finite rotational partition function | asymmetry-to-energy upper-capacity theorem **CONDITIONAL** on the spectral premise |
| `C_dir^orb` | hard-confined spinless nonrelativistic orbital matter with `H_ex>=T` | `C2<=2Ma^2E_ex` and the resulting risk floor **PROVED** |
| `C_dir^heat` | actual or norm-controlled isotropic rotational heat channel | finite-exposure risk interpolation **CONDITIONAL** on that channel |
| `C_dir^act` | nontrivial KMS environment and one local action deriving every allowed control and protocol stage | domain defined; a complete acquisition-through-readout member is **OPEN** |
| `C_dir^grav` | one local action, common support and energy ledgers, and a named gauge-invariant `G_m` | domain defined; a relativistic common-action member closing all Paper U premises is **OPEN** |

The intended physical paper class is

```text
C_dir^PaperU = C_dir^act intersect C_dir^grav
               intersect (C_dir^spec union C_dir^orb),   (10.1)
```

with every premise evaluated on the same state family, action, support, and
error ledger. Add `C_dir^cl` only when the paper makes a finite classical-record
claim, and add `C_dir^heat` only when it uses the heat-channel corollary.

The class nesting makes the claim boundary explicit. G1/G2 do not establish a
physical lifetime, a common-action KMS channel, a preferred gravitational
capacity variable, or a relation to Harlow's observer entropy.
