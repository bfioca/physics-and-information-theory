# Paper U Information-Exposure Goal

Status: active theorem-first research goal. The existing conditional observer
tradeoff is retained as infrastructure, not counted as the missing result.

## Decision

Pursue Paper U, but do not begin by expanding the current outline into a
15--25 page manuscript. The repository already contains:

- an exact protocol domain and postselection policy;
- global `SO(3)` risk-to-information and risk-to-asymmetry necessities;
- representation and named orbital localization-energy capacity bounds;
- an exact conditional heat-capacity composition;
- a partial Skyrmion realization layer; and
- explicit channel, locality, and gravity interfaces.

Repackaging those ingredients behind assumptions A1--A5 would be a useful
framework, but it would not yet be a new observer-physics theorem. The next
goal is to prove one implication that the current composition assumes:

> net relational information written into an initially blank record by a
> symmetric acquisition must cause a quantitatively controlled disturbance of
> the complete source; a later local-action theorem must turn that disturbance
> into physical exposure.

That implication must close the escape route in which the heat rate is simply
set to zero while an unpriced controller reads the register.

## Working Theorem

Call the new model class `C_dir^IE`. A member contains:

- a localized source pair `S=OD`, whose relative orbit encodes `G`, and a
  physical record memory `M`;
- an initial memory that is symmetric, `G`-independent, and uncorrelated with
  `S`, or an explicit ledger for its consumed asymmetry, correlation, and
  pre-existing information;
- the complete accessible state `rho_acc`, including every memory, charged
  controller, or reference that can re-enter at readout;
- one globally rotation-covariant acquisition, storage, and readout channel;
- for the local subclass `C_dir^(IE,local)`, a specified KMS environment `E`
  and one rotation-invariant, microcausal action that derives those channels;
- bounded control work, support, and duration ledgers, together with
  regulator-uniform form bounds or energy-constrained interaction norms;
- an unconditional protocol, or a success-weighted postselected protocol; and
- an explicit operational or comb-norm approximation ledger and the
  information-continuity hypotheses needed to use it.

For `G` Haar distributed on `SO(3)`, let `M_in` be the blank record, `M_0` the
record immediately after acquisition, `M_T` the retained record before final
readout, and `Y_T` the complete output transcript. The declared readout must
factor through `M_T`. If it rereads `O`, `D`, a controller, or another charged
system, that system is part of the retained record and its initial information
and asymmetry are charged. Let `I(G:M)` denote cq quantum mutual information.
Define

```text
R_write = optimal declared readout risk from M_0,
R_keep(T) = E sin^2[theta(g_hat(Y_T)^-1 G)/2],
Z_SO3(lambda) = integral dg exp[-lambda c(g,e)],
L_SO3(epsilon)
  = sup_(lambda>0)[-lambda epsilon-log Z_SO3(lambda)].
```

The exact Haar rate-distortion dual obeys `L_SO3(epsilon)>0` for
`epsilon<3/4`. The already proved implication is

```text
R_write <= epsilon
  => Delta I_M:=I(G:M_0)-I(G:M_in)
       =I(G:M_0) >= I(G:Y_0) >= L_SO3(epsilon).         (IE.1)
```

The equality uses the blank-record premise. A convenient but weaker explicit
lower bound is

```text
L_coarse(epsilon)
  = [(3/2) log(c_SO3/epsilon)]_+,
c_SO3=6/(e pi^(5/3)).
```

Mixed source ensembles can contain a classical sector that is readable
without disturbance. Define its maximum nondisturbingly accessible
information by

```text
I_nd(S)=sup I(G:Z),
```

where the supremum is over instruments whose source marginal equals
`rho_g^S` for every `g`. The named subclass must either prove `I_nd(S)=0` or
carry this term explicitly. A positive disturbance floor for arbitrary mixed
ensembles without this subtraction is false.

The first new theorem chooses one precise acquisition-disturbance measure
`D_acq` for the complete source `S=OD`; it does not conflate interaction
action, entropy production, and heat exposure. For one nonempty named
subclass, uniformly over its admissible protocols, derive

```text
[Delta I_M-I_nd(S)]_+
  <= F_IE(D_acq, E_ctrl, s_opt, model data) + eta_I,     (IE.2)

therefore

D_acq >= D_min(L_SO3(epsilon)-I_nd(S)-eta_I,
               E_ctrl, s_opt, model data) > 0.           (IE.3)
```

Here `F_IE` must be nondecreasing in `D_acq`, have a controlled zero-disturbance
value, and admit the generalized inverse used in (IE.3). Positivity requires
`L_SO3(epsilon)>I_nd(S)+F_IE(0,...)+eta_I`. The term `eta_I`
is an information-valued continuity remainder. A channel or comb distance
cannot be inserted directly: it must be converted using a finite record
dimension or a proved energy-constrained entropy-continuity theorem.

If `D_acq` is channel irreversibility or recoverability, (IE.2) must also be
compared directly with the Kretschmann-Schlingemann-Werner
information-disturbance theorem. A direct corollary is infrastructure, not the
new result; novelty must come from relational Haar risk, the `OD` source,
localization, or the physical-action restrictions.

A paper-level result must then connect acquisition to retained quality by one
of two controlled routes:

```text
R_keep(T) >= F_keep(R_write, D_acq, capacity) - eta_op, (IE.4a)
```

or, for a proved KMS/heat approximation,

```text
Gamma >= g(D_acq, beta, model data) > 0,
R_keep(T)
  >= 3/4(1-exp(-2Gamma))
     +exp(-2Gamma) R_cap(C_hat) - eta_op.                (IE.4b)
```

The map from `D_acq` to entropy production or `Gamma` is a separate,
action-specific fluctuation-dissipation lemma. A coherent transfer, a
long weak interaction, and a dissipative measurement need not be priced by the
same functional.

`R_cap` should use Hayashi's exact mean-Casimir frontier when practical. The
coarse executable floor `1/(16 C_hat+8)` remains a valid fallback. The support
capacity is

```text
C_hat(A,beta)=sup_(0<=a<=A) C_max(a,beta)<infinity,     (IE.5)
```

unless monotonicity of `C_max` has separately been proved.

## First Mathematical Route

The first bounded sprint is an acquisition-retention theorem under symmetric
dynamics, not a gravity calculation.

1. First prove a reduction from the relational `OD` ensemble to a covariant
   broadcasting problem, or work directly with the joint ensemble
   `rho_g^(OD)`. A globally invariant action is not automatically covariant
   under a gauge-fixed rotation of `O`, and `D` cannot be treated as a free
   anchor.
2. Start from continuous-group asymmetry no-broadcasting only after that
   reduction is valid. Otherwise prove an ensemble information-disturbance
   theorem that prices disturbance of both `O` and `D`.
3. Compute or bound the Koashi-Imoto nondisturbingly readable classical sector
   and either prove `I_nd=0` or subtract it explicitly.
4. Compare the desired statement with generic complementary-channel
   information-disturbance bounds before using symmetry-specific structure.
5. Translate approximate-broadcasting disturbance into full-frame Haar risk,
   rather than local fidelity or QFI.
6. Allow arbitrary mixed states, rotation-trivial multiplicities, priced
   memories, and success-weighted postselection. Include the resource and
   exposure cost of failed attempts.
7. Derive an explicit tradeoff between net information written to the blank
   record and the quality remaining in the complete source pair.
8. Compose only afterward with the named orbital or spectral capacity theorem.

The target output is an explicit inequality

```text
Psi(R_write, R_source_after, C_O, C_D,
    p_success, consumed side resources) >= 0,             (IE.6)
```

with a sharp asymptotic regime or a counterexample showing why no such
class-uniform strengthening is possible.

The predeclared counterexample audit includes perfectly asymmetric or
infinite-capacity orbit states, `D` acting as a consumed or catalytic frame,
coherent reversible transfer versus irreversible classical recording,
rare-success postselection with failed-attempt exposure, and a final readout
that bypasses `M_T`. It also includes a mixed ensemble whose `G`-dependent
classical sufficient statistic can be copied without disturbance.

This route is paper-relevant only if it adds a full-group, all-protocol, or
localized-capacity statement not already contained in the approximate
asymmetry-broadcasting, WAY, or general resource-cost/irreversibility
literature, and not already implied by generic complementary-channel
continuity. A direct relabeling of an existing theorem does not pass.

## Static-Patch Lift

After (IE.6), choose one genuinely local matter interaction. The current
factorized rigid-current density is excluded because distinct components fail
microcausality under disjoint spacelike smearing.

The replacement action must:

1. derive record acquisition and final readout, rather than granting them as
   boundary operations;
2. preserve rotational covariance without spreading one noncommuting global
   charge density across spacelike-separated points;
3. give a regulator-uniform KMS reduced channel or a direct causal-comb bound;
4. price switching, controls, memories, and support;
5. produce a nonzero lower exposure on an open parameter box; and
6. keep every approximation error below the operational risk margin.

Elapsed time enters the headline only if the action forces exposure to grow
with elapsed time. If the register can be isolated during storage and read
once later, the valid theorem is per use or per acquisition, not a universal
coherence-time ceiling.

## Gravity Interface

Gravity is not inserted by naming an abstract budget `B`. It enters the paper
only after proving, for a selected gauge-invariant quantity `G_m`,

```text
G_m <= b, support <= a
  => C2 <= C_grav(a,b),                                  (IE.7)
```

or another quantitative inequality that actually constrains record capacity,
readout disturbance, or the admissible state family.

Candidate quantities include a controlled compactness/collapse margin,
horizon-area or generalized-entropy shift, QES displacement, or a normalized
Weyl observable. The current fixed-background Weyl interval contains zero and
is not a premise. Until (IE.7) is proved, gravity is an explicit interface and
motivation, not part of the theorem title.

Any candidate must also survive a kernel audit: if a large-capacity state
family has vanishing quadrupole, Weyl witness, or selected `G_m`, then that
functional cannot support (IE.7) without additional hypotheses.

## Skyrmion Role

Paper A remains frozen and independent. Its certified fixed-wall profile,
inertia, and radial gap may provide a matter-side witness after the operational
theorem exists.

The `B=1` Skyrmion carries a projective/half-integer rotational sector, while
the current Paper U headline domain is integer-spin `SO(3)`. It is therefore
not called a realization until the projective risk constants, protocol, local
action, and all capacity/channel premises are stated consistently. Failure of
the Skyrmion realization must not invalidate the operational theorem.

## Novelty Baseline

The new theorem must be compared directly with:

- Hayashi, [Fourier Analytic Approach to Quantum Estimation of Group
  Action](https://arxiv.org/abs/1209.3463);
- Gour, Marvian, and Spekkens, [Measuring the Quality of a Quantum Reference
  Frame](https://arxiv.org/abs/0901.0943);
- Marvian and Spekkens, [A no-broadcasting theorem for quantum asymmetry and
  coherence](https://arxiv.org/abs/1812.08766);
- Marvian and Spekkens, [An information-theoretic account of the
  Wigner-Araki-Yanase theorem](https://arxiv.org/abs/1212.3378);
- Ahmadi, Jennings, and Rudolph, [The WAY theorem and the quantum resource
  theory of asymmetry](https://arxiv.org/abs/1209.0921);
- Tajima, Yamaguchi, Takagi, and Kuramochi, [Universal tradeoff relations
  between resource cost and irreversibility of
  channels](https://arxiv.org/abs/2507.23760);
- Kretschmann, Schlingemann, and Werner, [The Information-Disturbance
  Tradeoff and the Continuity of Stinespring's
  Representation](https://arxiv.org/abs/quant-ph/0605009);
- Koashi and Imoto, [What Is Possible Without Disturbing Partially Known
  Quantum States?](https://arxiv.org/abs/quant-ph/0101144);
- Bartlett et al., [Degradation of a quantum reference
  frame](https://arxiv.org/abs/quant-ph/0602069);
- Poulin and Yard, [Dynamics of a Quantum Reference
  Frame](https://arxiv.org/abs/quant-ph/0612126);
- Harlow, Usatyuk, and Zhao, [Quantum mechanics and observers for gravity in a
  closed universe](https://arxiv.org/abs/2501.02359);
- Harlow, [Observers, alpha-parameters, and the Hartle-Hawking
  state](https://arxiv.org/abs/2602.03835);
- Bousso, [Bekenstein bounds in de Sitter and flat
  space](https://arxiv.org/abs/hep-th/0012052); and
- Dain, [Inequality between size and angular momentum for
  bodies](https://arxiv.org/abs/1305.6645).

`S_dir` is not identified with `S_Ob`. The Harlow connection is that this
theorem prices one operational resource a finite observer may need.

## Deliverables

1. A theorem note for (IE.6), including counterexamples and exact quantifiers.
2. Executable finite-dimensional checks for every representation-theoretic
   block used in the proof.
3. A primary-source novelty audit against the sources above, with an explicit
   non-subsumption argument for the general resource-cost/irreversibility and
   WAY theorems, complementary-channel information-disturbance bounds, and the
   Koashi-Imoto nondisturbing decomposition.
4. A declared local-action candidate and microcausality audit.
5. A local-action channel or causal-comb theorem connecting
   (IE.2)--(IE.3) to (IE.4) on an open box.
6. A claim ledger separating unconditional mathematics, physical-channel
   assumptions, gravity interfaces, Skyrmion support, and non-goals.
7. A manuscript only after at least one new implication in
   (IE.2)--(IE.4) is proved.

## Kill And Pivot Rules

- If unbounded controls or free oriented memories can evade (IE.2), price them
  or narrow the class; do not call the unrestricted statement universal.
- If a reversible symmetric transfer can write the record without degrading
  the source, state the missing no-broadcasting hypothesis and pivot from
  elapsed-time lifetime to a per-use theorem.
- If pre-existing record information, a catalytic target frame, or a readout
  that bypasses `M_T` removes the lower bound, charge that resource or narrow
  the declared protocol; do not bury it in `rho_acc`.
- If `I_nd(S)>0`, subtract the nondisturbingly readable classical information
  or restrict to a proved `I_nd=0` subclass; do not claim a strict disturbance
  floor for arbitrary mixed ensembles.
- If (IE.2) follows directly from Stinespring continuity or a known
  complementary-channel information-disturbance theorem, retain it as a lemma
  and identify a new relational, localized, or action-specific strengthening.
- If (IE.6) is an immediate corollary of Marvian--Spekkens with no new global
  risk or localization content, retain it as a lemma and do not make it the
  paper.
- If the local action fails microcausality, stop that realization rather than
  assigning a zero multipole error.
- If the result still permits `Gamma=0` independently of acquisition and
  readout, Paper U has not advanced.
- If gravity remains only a named variable without (IE.7), remove gravity from
  the headline.

## Paper Gate

The ambitious Paper U path becomes a manuscript when all of the following are
true:

| Gate | Pass condition |
| --- | --- |
| New theorem | At least one nontrivial implication in (IE.2)--(IE.4) is proved |
| Domain | Controls, memories, adaptation, and postselection are fully priced |
| Dynamics | Acquisition and readout arise from the same declared action |
| Exposure | Useful readout forces a strictly positive disturbance or KMS exposure |
| Capacity | The same state family obeys a derived representation-energy/support bound |
| Errors | Operational and field-theory errors are uniform on one open box |
| Novelty | The result is not subsumed by Hayashi, WAY/resource-cost bounds, generic channel information-disturbance, Koashi-Imoto, QRF degradation, or asymmetry no-broadcasting |
| Gravity | Included in the title only if a relation such as (IE.7) is proved |

The finish line is not a longer outline. It is a theorem showing, in one
auditable model class, that a finite localized observer cannot acquire and
retain an arbitrarily accurate directional record for free.
