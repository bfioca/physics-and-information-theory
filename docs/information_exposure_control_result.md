# Information-Exposure Control Result And Stop Decision

Status: completed prove-or-kill sprint, 2026-06-17. The control inequalities
below are valid and the small-spin optimization is numerically checked. The
proposed generic source-recoverability theorem does **not** survive as a new
Paper U result. U8 is therefore not activated by this route.

## Executive Verdict

The strongest clean full-channel control inherited from
Kretschmann--Schlingemann--Werner (KSW) is

```text
delta_ch >= [3/4-R_write]_+^2,                         (C.1)
```

where

```text
delta_ch=inf_R ||R o N-id_S||_diamond                 (C.2)
```

uses the unhalved diamond norm, `N` is the source-remnant channel, and the
declared record is a post-processing of a complement of `N`. For a flagged
covariant success branch,

```text
delta_ch >= p_s^2[3/4-R_success]_+^2.                  (C.3)
```

This is a direct known-theorem specialization. It is not the desired
ensemble-specific disturbance of the physical `OD` orbit.

For a pure source orbit, Marvian--Spekkens plus an elementary Haar argument
does give a positive source-only orbit-recovery floor at every fixed finite
source. That floor depends on the complete orbit geometry and can vanish along
growing-capacity families. It too is a corollary of known covariant
information-disturbance theory.

The numerical residual is a representation-dependent covariant-instrument
frontier. Sacchi's general covariant-estimation framework already
sets up that optimization, and a preprint submitted on 2026-06-16 solves the
directly adjacent full-state problem for antiparallel spin pairs in the same
`j=0 direct_sum j=1` carrier. Changing from direction loss to an ordered
noncollinear full-frame token changes the numerical frontier, not the theorem
class.

**Decision: KNOWN-THEOREM SPECIALIZATION / STOP as the Paper U headline.**

## 1. Exact Control Domain

Let `S=OD` be a finite-dimensional complete relational source and let

```text
A:S -> B tensor M                                      (C.4)
```

be the unconditional acquisition channel, including every flag and failure
branch. In a Stinespring dilation, let `F` be the complete complementary
output. The retained record channel `L:S->M` is a post-processing of the
complement `N^c:S->F`, while

```text
N=Tr_M o A:S->B                                        (C.5)
```

is the source remnant. A recovery map in (C.2) acts on `B` alone. Giving it
access to `M` would allow an inverse coherent transfer and would not measure
source disturbance.

For `G~Haar(SO(3))`, source orbit `rho_g`, record POVM, and estimate `g_hat`,
the loss is

```text
c(g_hat,g)=sin^2[theta(g_hat^-1 g)/2] in [0,1].        (C.6)
```

Every output statistically independent of `G` has risk exactly `3/4`.

The full-channel metric (C.2) tests the identity channel on every input,
including inputs entangled with a reference. It is stronger than either

```text
inf_R integral dg [1-F^2(rho_g,R N(rho_g))]            (C.7)
```

or a worst-orbit analogue. Orbit fidelity is not a diamond distance and does
not control linear directions outside the orbit span or preservation of
purifications.

## 2. KSW Control Theorem

Define the distances of the complete complement and declared record from a
replacer channel by

```text
kappa_F=inf_sigma ||N^c-Repl_sigma||_diamond,
kappa_M=inf_tau   ||L-Repl_tau||_diamond.              (C.8)
```

KSW Theorem 3, translated from the dual cb norm to the Schrodinger diamond
norm, gives

```text
(1/4) delta_ch^2 <= kappa_F <= 2 sqrt(delta_ch),
kappa_M <= kappa_F.                                    (C.9)
```

Reference: Kretschmann, Schlingemann, and Werner,
[*The Information-Disturbance Tradeoff and the Continuity of Stinespring's
Representation*](https://arxiv.org/abs/quant-ph/0605009), Theorem 3.

### Proof of (C.1)

Fix the replacer supplied by the upper half of (C.9) and trace its environment
down to `M`. Apply the actual readout POVM and estimator both to `L(rho_g)` and
to the constant record. Measurement contracts trace distance, and changing a
probability distribution by total variation `t` changes the expectation of a
`[0,1]` loss by at most `t`. Therefore

```text
3/4-R_write <= (1/2) kappa_M
              <= (1/2) kappa_F
              <= sqrt(delta_ch).                       (C.10)
```

Squaring proves (C.1).

### Postselection

If failure is retained and charged the Haar-random loss, then

```text
R_uncond=p_s R_success+(1-p_s)3/4.                     (C.11)
```

Substituting (C.11) in (C.1) proves (C.3). KSW does not apply to a normalized
success-only map because that map is not trace preserving.

### Finite-record entropy refinement

For a record of dimension `d_M`, put

```text
a_d(t)=h_2(t)+t log(d-1),  t<=1-1/d,
B_d(t)=min{log d,2a_d(t)}.                              (C.12)
```

Above the stated range take the entropy-difference cap `log d`. If
`L_SO3(R)` is any valid Haar rate-distortion information lower bound, entropy
continuity and (C.9) give

```text
L_SO3(R_write) <= I(G:M)
                 <= B_d(min{sqrt(delta_ch),1}),         (C.13)

delta_ch >= b_d[L_SO3(R_write)]^2,                     (C.14)
```

where `b_d` is the generalized inverse of `B_d`. The strongest inherited
control is the maximum of (C.1) and (C.14). If `L_SO3(R)>log d`, the declared
finite record is excluded before a disturbance estimate is needed.

The executable implementation is
`qgtoy/information_exposure_control.py`.

### Why this is not the desired theorem

Copying a Koashi--Imoto classical label can preserve every state in an
ensemble while dephasing superpositions outside that ensemble. Then
ensemble-specific disturbance is zero but `delta_ch` is positive. KSW prices
the latter. Replacing (C.2) by (C.7) requires a separate robust ensemble
theorem; the word "recoverability" alone does not make that replacement.

## 3. Koashi--Imoto Control

For a finite ensemble, Koashi and Imoto decompose

```text
H_S=direct_sum_l H_(J_l) tensor H_(K_l),
rho_g=direct_sum_l p_l(g) rho_(J_l,g) tensor omega_(K_l). (C.15)
```

Every exactly nondisturbing record is a post-processing of the classical block
label `l`. Thus

```text
I_nd(S)=I(G:l).                                         (C.16)
```

Reference: Koashi and Imoto,
[*What Is Possible Without Disturbing Partially Known Quantum
States?*](https://arxiv.org/abs/quant-ph/0101144).

For one exact unitary orbit of a connected group, (C.16) vanishes. Conjugation
by the group continuously permutes the finite set of minimal KI central
projectors. A connected group cannot act nontrivially on a finite discrete
set, so every central projector is fixed. Consequently

```text
p_l(hg)=Tr(P_l U_h rho_g U_h^*)=Tr(P_l rho_g)=p_l(g),   (C.17)
```

and every `p_l` is constant on the orbit:

```text
I_nd(S)=0 for a single finite-dimensional connected SO(3) orbit. (C.18)
```

This closes the exact classical-sector loophole for the named orbit. It does
not provide an approximate KI stability modulus for mixed sources.

## 4. Pure-Orbit Haar Control

Marvian and Spekkens consider a pure source `psi`, a covariant broadcast
process, and recovery from the source remnant alone. With

```text
D_MS=1-max_(R_cov) F^2(psi,R_cov(sigma_B)),
f_h(tau)=1-F(tau,U_h tau U_h^*),                        (C.19)
```

their Eq. (6) implies

```text
D_MS >= (1/16)[F(psi,U_h psi U_h^*) f_h(tau_M)]^2.     (C.20)
```

Reference: Marvian and Spekkens,
[*A no-broadcasting theorem for quantum asymmetry and coherence and a
trade-off relation for approximate
broadcasting*](https://arxiv.org/abs/1812.08766).

Full Haar risk supplies a weak but explicit bridge to (C.20). Let
`bar_tau=integral dg tau_g` and `Delta=3/4-R_write`. Comparing the actual
record with the constant `bar_tau` gives

```text
(1/2)||tau_e-bar_tau||_1 >= Delta.                      (C.21)
```

Convexity under `bar_tau=integral dh tau_h` implies that some `h` obeys

```text
(1/2)||tau_e-tau_h||_1 >= Delta.                        (C.22)
```

Fuchs--van de Graaf then gives

```text
f_h(tau_M)>=1-sqrt(1-Delta^2).                          (C.23)
```

If the pure source has

```text
q_min=inf_h F(psi,U_h psi U_h^*)>0,                    (C.24)
```

then

```text
D_MS >= {q_min[1-sqrt(1-Delta^2)]/4}^2.                (C.25)
```

When `q_min=0`, define

```text
mu(q)=Haar{h:F(psi,U_h psi U_h^*)<q},
d_q=[(Delta-mu(q))/(1-mu(q))]_+.                       (C.26)
```

The same averaging argument yields the stronger general control

```text
D_MS >= sup_(0<q<1) {q[1-sqrt(1-d_q^2)]/4}^2.          (C.27)
```

Equations (C.25)--(C.27) are direct compositions of Eq. (6) with Haar-risk
geometry. They are infrastructure, not a non-subsumed Paper U result.

## 5. Counterexample Audit

| Construction | Result | Required response |
| --- | --- | --- |
| KI classical label | Copy `l` at zero ensemble disturbance | subtract `I_nd`; for the exact connected orbit, prove (C.18) |
| recovery reads record | inverse coherent transfer gives zero apparent disturbance | recovery acts on `B` alone |
| redundant coherent tokens | good record and good recovery coexist as capacity grows | every uniform floor must depend on complete source capacity |
| catalytic or borrowed frame | small net consumption can hide arbitrarily large peak directional capacity | charge initial and peak asymmetry, representation, correlations, energy, and support |
| hidden readout memory | omitted `G`-correlated memory supplies the answer for free | close the accessible resource boundary and enforce readout factorization |
| rare-success transfer | `R_success->0` with unconditional disturbance `O(p_s)` | retain the flag and use (C.3); charge retries |

### Decisive growing-capacity counterexample

Let `|phi_g>` be any finite-dimensional pure full-frame token. Put `n+k`
copies in the complete source, coherently transfer `k` copies to the blank
record, and retain `n` copies. The record admits risk `O(1/k)`. A universal
covariant `n -> n+k` cloner recovers the complete source with global fidelity

```text
F_rec >= d[n]/d[n+k],
d[m]=binomial(m+d-1,m).                                 (C.28)
```

Taking `n=J^2` and `k=J` gives

```text
R_write=O(1/J),
1-F_rec=O(k/n)=O(1/J).                                 (C.29)
```

Thus no positive source-disturbance floor depending only on accuracy,
postselection, and the word "finite" can hold. Capacity dependence is not a
technical refinement; it is logically necessary.

## 6. Small-Spin SDP

The executable experiment is
`experiments/information_exposure_small_spin_sdp.py`; its checked output is
`experiments/information_exposure_small_spin_sdp.json`.

### Model

```text
psi_e=|z+>_O tensor |x+>_D,
psi_g=(u_g tensor u_g)psi_e.                            (C.30)
```

The ordered noncollinear markers have trivial `SO(3)` stabilizer. Their joint
carrier is the physical integer-spin representation `j=0 direct_sum j=1`, and

```text
inf_g F(psi_e,psi_g)=0,
I_nd=0.                                                 (C.31)
```

The zero follows, for example, from a pi rotation about the `x` axis: it fixes
`|x+>` up to phase and sends `|z+>` to an orthogonal state. Thus the simple
minimum-overlap control (C.25) is trivial for this orbit. The quantile control
(C.27) can avoid a measure-zero orthogonal set, but it is not evaluated in the
SDP record.

A single marker has optimal full-frame risk `2/3`; the complete pair reaches
approximately `0.5379433`.

### Convex optimization

Let `J_0>=0` be the Choi seed of a covariant instrument, with continuous
outcome equal to the orientation estimate. Twirl it under

```text
W_g=conjugate(U_g)_in tensor U_g_out.                   (C.32)
```

The trace-preserving constraint, Haar risk, and complete-source pure-orbit
fidelity are all linear in `J_0`. For each risk ceiling `r`, the SDP maximizes
the recovered source fidelity. The finite-dimensional SDP formulation is exact;
the displayed frontier is its reproducible floating-point solution, not an
interval-certified optimum. It does not impose a local action, finite memory
dimension, work, support, duration, KMS exposure, or gravity.

### Numerically checked frontier

| Haar risk ceiling | optimal orbit recovery infidelity | generic `U(4)` cloner infidelity | minimum-overlap MS floor |
| ---: | ---: | ---: | ---: |
| `0.54` | `0.48899841` | `0.70687260` | `0` |
| `0.56` | `0.34022268` | `0.56684769` | `0` |
| `0.60` | `0.19506065` | `0.38514619` | `0` |
| `0.65` | `0.08597432` | `0.20957816` | `0` |
| `0.70` | `0.02255704` | `0.07392120` | `0` |
| `0.74` | `0.00097471` | `0.00512087` | `0` |

The optimized `SO(3)` instrument numerically beats the generic `U(4)` cloner,
so group and orbit structure matter quantitatively. The endpoint and
quadrature residuals are below `2e-7` and `1.2e-15`, respectively.

## 7. Novelty Audit

The relevant primary-source hierarchy is now:

1. KSW supplies the full-channel control (C.1).
2. Koashi--Imoto supplies the exact nondisturbing decomposition and (C.18).
3. Marvian--Spekkens supplies pure-state covariant recovery versus destination
   asymmetry, from which (C.25)--(C.27) follow.
4. Tajima et al., [*Universal tradeoff relations between resource cost and
   irreversibility of channels*](https://arxiv.org/abs/2507.23760), already
   cover broad resource-cost/irreversibility relations including asymmetry.
5. Sacchi, [*Information-disturbance tradeoff in covariant quantum state
   estimation*](https://arxiv.org/abs/quant-ph/0702033), gives the general
   covariant-instrument framework used by the SDP.
6. Sacchi, [*Full-state information-disturbance tradeoff for direction
   estimation with antiparallel spin-coherent
   pairs*](https://arxiv.org/abs/2606.18040), submitted 2026-06-16, solves the
   directly adjacent `0 direct_sum 1` spin-pair problem and extends it to
   arbitrary spin.

The noncollinear ordered token and full-frame chordal loss are not identical to
Sacchi's direction-estimation problem. They do not, however, create a new
information-disturbance mechanism. The SDP is a specialization of the same
covariant Choi-seed method, with a different cost operator and fiducial state.

## 8. Residual Statement And Stop Rule

After the control results and counterexamples, the only abstract residuals are:

1. a robust approximate Koashi--Imoto quotient theorem for arbitrary mixed
   relational orbits;
2. exact representation-by-representation full-frame frontiers; and
3. resource-restricted recovery frontiers after imposing physical work,
   support, duration, or locality constraints.

The first two lie inside established ensemble/covariant
information-disturbance programs. The third becomes physics only after a
specific local action derives the restrictions; imposing them abstractly would
manufacture novelty by definition. Closed side-resource accounting and
postselection are necessary theorem hygiene, not a new dynamical implication.

Therefore no genuinely stronger generic IE inequality survives this sprint.
Under the predeclared goal, the correct action is:

```text
retain (C.1)--(C.29) as control infrastructure;
do not present the finite SDP frontier as Paper U;
do not proceed to U8 as though IE.2 were a new theorem;
require a separately motivated local-action phenomenon before reopening U8.
```

This is a successful negative research result: it closes the free-readout
logic at the control level and prevents a known covariant-estimation theorem
from being promoted into observer-gravity novelty.

## 9. Goal Completion Audit

| Required item | Evidence | Verdict |
| --- | --- | --- |
| strongest inherited source-recoverability inequality | (C.1)--(C.14), executable module | **CLOSED AS CONTROL** |
| counterexamples before long proof | Section 5 and executable redundant/postselection formulas | **CLOSED** |
| small-spin SDP | Section 6, script, JSON record, residual checks, tests | **CLOSED NUMERICALLY** |
| isolate full-`SO(3)`/`OD`/KI/resource/postselection residual | Sections 3--8 | **CLOSED** |
| stop if no non-subsumed theorem remains | Section 8 | **STOP TRIGGERED** |
| pursue U8 only after a surviving stronger theorem | no such theorem survived | **NOT ACTIVATED** |
