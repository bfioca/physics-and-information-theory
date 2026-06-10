# Observer-Register Counterexample Checklist

Status: adversarial audit for the `C_dir` specification and G2 resource
dictionary. A proposed extension does not enter Paper U until it survives every
applicable row.

## How to use this checklist

For a candidate theorem, record the full accessible state, the relative group
action, the protocol outcome including failure, every side-information system,
the Hamiltonian sector floors, and the proper/optical/gravitational budgets.
Then test the following eight constructions. Passing means either that the
claimed inequality still holds or that a stated hypothesis excludes the
construction for a physical reason.

## X1. Invariant high-spin mixed state

**Construction.** On one spin-`j` irrep, take

```text
rho_j = identity_(V_j)/(2j+1).                           (X1.1)
```

**Resource values.**

```text
A_SO3(rho_j)=0,
F_Q(rho_j)=0,
<J^2>=j(j+1),
R_Haar=3/4.
```

The rotor energy, Hilbert-space dimension, and von Neumann entropy may all grow
with `j` while the orbit remains constant. No thermodynamic interpretation is
made without a separate Hamiltonian and ensemble.

**Attacked inference.** Large Casimir, rotor energy, Hilbert dimension, or von
Neumann entropy implies a good directional record.

**Verdict.** **COUNTEREXAMPLE.** These quantities can be necessary capacity
budgets but are not sufficient quality measures.

**Required repair.** Keep the proved arrows one-way and measure directional
quality by the orbit task. Reference:
`docs/rotational_resource_substitution_no_go.md`.

## X2. Rare high-spin tail

**Construction.** For integer `j>=2`, let

```text
|cat_j>=(|j,j>+|j,-j>)/sqrt(2),
|psi_j>=sqrt(1-1/j)|0,0>+sqrt(1/j)|cat_j>.               (X2.1)
```

**Resource values.**

```text
K1=<j>=1,
Tr F_Q=4(j+1),
<J^2>=j+1,
distance(rho_g,|0,0><0,0|)=1/sqrt(j) for every g.
```

Thus local QFI and Casimir diverge while the entire orbit converges uniformly
to an invariant state.

**Attacked inference.** Large local QFI or a remote high-spin component implies
small global risk.

**Verdict.** **COUNTEREXAMPLE.** QFI is not a global record metric and a
mean-Casimir lower bound alone can become arbitrarily weak.

**Required repair.** Use the tail-robust asymmetry/mean-label theorem, or add a
hard cutoff, energy-variance bound, or uniform tail condition. The main G2
chain does not use QFI. Reference:
`docs/rotational_resource_substitution_no_go.md`.

## X3. Bounded-spectrum Hamiltonian

**Construction.** On `L^2(SO(3))`, use

```text
H_bad=sum_(j>=0)(1-exp(-j))P_j,  0<=H_bad<1.             (X3.1)
```

Let `eta_J` be the normalized Peter-Weyl token through spin `J`.

**Resource values.** Every `eta_J` has energy below one, while its achievable
chordal risk is

```text
R_J=[4J(J+2)+3]/{4(J+1)(2J+1)(2J+3)/3}=O(1/J).          (X3.2)
```

**Attacked inference.** Positivity, covariance, and finite mean energy imply a
uniform directional-capacity bound.

**Verdict.** **COUNTEREXAMPLE.** The generic record-to-energy arrow is false.

**Required repair.** Derive growing sector floors from the physical action. A
sufficient named premise is

```text
sum_j (2j+1)^2 exp(-beta epsilon_j)<infinity.            (X3.3)
```

References: `docs/localized_orbital_reference.md` and
`qgtoy/rotational_spectral_capacity.py`.

## X4. Stabilizer ambiguity

**Construction.** Choose a state with

```text
U(h)rho U(h)^*=rho                                      (X4.1)
```

for a nonidentity rotation `h` of principal angle `alpha`. The hypotheses `g`
and `gh` then give identical states.

**Exact consequence.** Every POVM obeys

```text
R_Haar>=sin^2(alpha/4).                                  (X4.2)
```

The family `|j,0>` has `A_SO3=log(2j+1)->infinity` but is invariant under every
rotation about its axis; its half-turn therefore gives `R_Haar>=1/2` for all
`j`. This directly defeats asymmetry sufficiency.

The audited spin-2 state

```text
(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2)
```

has `F_Q=8 identity_3` but a half-turn stabilizer and hence `R_Haar>=1/2`.

**Attacked inference.** Full-rank local QFI, isotropic second moments, or
nonzero asymmetry implies a good full-frame record.

**Verdict.** **COUNTEREXAMPLE.** Local identifiability does not remove global
aliasing.

**Required repair.** Declare whether the task is full `SO(3)` or a quotient
`SO(3)/H`. For a full frame, retain global Haar risk and make the physical
marker orbit asymptotically free. Reference: `docs/orientation_stabilizer_risk.md`.

## X5. Free postselection

**Construction.** Attach an invariant classical flag and prepare

```text
rho_J=(1-p_J)|fail,0><fail,0|+p_J|success,eta_J><success,eta_J|.
```

Postselect on the success flag. With `p_J=J^-3`, a rotor token whose energy
scales as `J^2` has unconditional mean energy `O(J^-1)`, and block additivity
gives

```text
A_SO3(rho_J)=p_J A_SO3(eta_J)->0,                       (X5.1)
```

while the conditional risk of `eta_J` tends to zero.

**Attacked inference.** Conditional accuracy can be reported without success
probability or retry cost.

**Verdict.** **COUNTEREXAMPLE.** Arbitrarily accurate success-only claims can
have vanishing average resource.

**Required repair.** Use unconditional risk with abort loss `3/4`, or report
`(p_s,R_s)` and apply

```text
S_dir>=p_s L(R_s)                                       (X5.2)
```

only for a covariant success event. Charge repeated attempts and do not inherit
channel-error bounds through conditioning without a positive `p_s` floor.

## X6. Hidden external memory or frame

**Construction.** Let the modeled register `O` be invariant, but give the
readout an unbudgeted system `M` containing a high-quality oriented token or a
classical lookup correlated with `G`. A decoder using `M` attains small risk
while every recorded resource of `O` is zero.

The same failure occurs when a polarized drive, laboratory triad, gyroscope,
or noncovariant feedback controller is treated as a free operation.

**Attacked inference.** Resources of a selected subsystem bound a protocol
that may access an unpriced directional system.

**Verdict.** **COUNTEREXAMPLE.** No subsystem-only theorem survives an open
resource boundary.

**Required repair.** Quantify over a closed accessible algebra. Every system or
controller used after encoding is either rotation invariant and independent of
`G`, or is included in the joint orbit, action, support, energy, and gravity
budgets. Systems traced out cannot later re-enter.

## X7. Pre-correlated encoder or memory

**Construction.** In

```text
direct_sum_(j<=J) V_j tensor V_j^*,                     (X7.1)
```

take the canonical entangled Peter-Weyl token and rotate only the left carrier.
The reduced carrier state is rotation invariant, but the full carrier-memory
orbit has

```text
A_SO3(rho_full)=log D_J                                 (X7.2)
```

and achieves improving orientation risk. Computing `A_SO3` only on the carrier
would report zero resource.

A still stronger loophole results if an encoder is allowed to depend on the
unknown orientation before the theorem's resource accounting begins.

**Attacked inference.** The marginal asymmetry of `O` prices a readout that can
use pre-correlated side information.

**Verdict.** **COUNTEREXAMPLE.** Correlations can carry the relational resource
even when the priced marginal is invariant.

**Required repair.** Allow pre-correlation only by evaluating `S_dir` on the
complete accessible state. Include every accessible physical memory, invariant
or charged, in the action, support, Killing-energy, and gravity ledgers; include
every charged memory in the directional representation as well. Preparation
and encoding maps are fixed before `G` is sampled. References:
`docs/operational_su2_reference.md` and
`docs/charged_reference_recovery.md`.

## X8. Local-QFI/global-risk mismatch

This row is passed only if both independent mechanisms are addressed:

| Mechanism | Example | What it defeats |
| --- | --- | --- |
| vanishing rare tail | X2 | QFI diverges although the orbit approaches an invariant state |
| exact global alias | X4 | QFI is full rank although separated orientations are identical |

**Verdict.** **COUNTEREXAMPLE** to `large QFI -> small global risk` without
additional hypotheses.

**Required repair.** A QFI route needs uniform spectral control, global
identifiability, and a concentration or local-asymptotic-normality theorem.
Paper U instead uses the already proved global Bayes-risk/asymmetry route.

## Protocol closure checks

Before accepting a model as a member of `C_dir`, answer all of these with an
explicit subsystem or map:

- Is every randomized seed independent of `G` and represented as an invariant
  ancilla?
- Does the complete adaptive transcript define one `G`-independent instrument
  on the counted input systems?
- Does any feedback step query a directional controller absent from the
  budgets?
- Is every pre-correlated memory included in the joint `S_dir` state?
- Is failure retained as an outcome, or are both `p_s` and retry costs stated?
- If a classical record dimension is claimed, is the finite record variable
  named and does `G -> C_T -> Y` actually hold?
- Are the Hamiltonian sector floors those of the same system whose asymmetry is
  bounded?
- Are proper and optical support computed from the same declared worldtube
  when a conversion is used?

## Audit disposition

| Test | Closed theorem response |
| --- | --- |
| X1 invariant high-spin mixture | survives because Casimir is necessary-only |
| X2 rare tail | survives through the global asymmetry/mean-label route |
| X3 bounded spectrum | narrows the energy arrow to `C_dir^spec` or `C_dir^orb` |
| X4 stabilizer | survives because the performance metric is global Haar risk |
| X5 free postselection | survives only with unconditional risk or success-weighted accounting |
| X6 hidden memory | survives only with a closed accessible resource boundary |
| X7 pre-correlation | survives only with joint-state `S_dir` |
| X8 QFI mismatch | survives because QFI is removed from the main implication chain |
