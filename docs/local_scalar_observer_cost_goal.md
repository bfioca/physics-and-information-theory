# Paper-Or-No-Go Goal: Gravitational Cost of a Local Observer Channel

Status: active; sharp optimization theorem and revised manuscript pass their
internal checks, external specialist novelty review remains the binding gate

Freeze one continuum model: a degenerate pointer qubit coupled by a smooth,
compact spacetime source to the full conformally coupled massless scalar in one
de Sitter static patch. Starting from that action, derive the exact reduced
pointer channel, its halved diamond error from complete pointer dephasing, the
post-switch renormalized field stress and Killing energy, and the causal
support implied by the source radius and duration. Eliminate the source
strength and prove, with explicit constants, a bound of the form

```text
log(1/(2 epsilon_obs)) <= E_K R F(a/R,T/R).
```

Then determine whether the same field data admit a controlled spherical local
weak-gravity realization on the ball containing the datum. The sprint ends in
one of three decisions: a full
paper GO if the QFT theorem and an honest gravitational corollary are both new
and survive review; a narrower mathematical-physics GO if the localization-
energy theorem is new but gravity remains only a final-slice constraint result;
or NO-GO if the inequality is subsumed by prior detector/decoherence results,
fails on its stated domain, or becomes physically empty once the source and
gravity assumptions are made explicit.

Complete dephasing is the binary quantum-to-classical pointer target used in
the Harlow--Usatyuk--Zhao observer rule. The model error is only a channel
distance to that target; it must not be identified with their gravitational
encoding error or with `exp(-S_Ob)`. The shared smeared qubit operator is a
declared detector idealization, not an autonomous relativistic apparatus.
Its frozen interaction densities commute at spacelike separation, but a
relativistic probe-field replacement remains the clean strengthening route.

## Frozen Candidate Claim

For a source supported inside areal radius `a<R` during static time `T`, let

```text
L=R atanh(a/R)+T,
y=L/R,
F(y)=4 asinh(1)y/pi+8y^2/pi^3.
```

The strengthened target theorem is

```text
epsilon_obs=(1/2)exp(-Gamma),
Gamma <= E_K R C_opt(y),
C_opt(y)=2y Lambda(y/2) <= F(y),
k_tau(u,v)=pi^-1 log[sinh(tau(u+v))/sinh(tau|u-v|)].
```

Here `Lambda` is the simple top eigenvalue of the positive compact KMS kernel.
The full phase-space optimizer must be an s-wave momentum profile. Consequently,
exact complete pointer dephasing cannot be produced with both finite
post-switch field energy and finite causal support in this model. `C_opt` is
sharp at fixed final Cauchy support; for a smaller source radius plus duration
it is a causal envelope unless a separate controllability theorem is proved.

## Completion Gates

1. **Action and channel.** Derive the Weyl displacement and pointer channel
   from one compactly supported field-local action, including all
   normalization factors. State the finite-dimensional smeared-pointer scope.
2. **Energy and stress.** Derive `E_K` and the displaced renormalized stress
   from the same source. Do not count a declared mass profile as same-action
   stress.
3. **Uniform theorem.** Solve the support-constrained optimization for every
   smooth compact source in a centered static-patch ball, including all
   angular and canonical sectors, with support and duration entering only
   through finite propagation.
4. **Achievability.** Give a smooth compact source family with a nonempty
   finite-error, finite-energy, local weak-constraint window, or prove that none
   exists.
5. **Gravity honesty.** Construct exact Einstein-scalar constraint data from
   the same final scalar datum, then distinguish that final-slice result from a
   channel derived on the perturbed geometry. A full dynamical gravity headline
   requires the latter or a controlled perturbative theorem.
6. **Novelty.** Compare at equation level with exact gapless-detector channels,
   detector switching-energy work, DSW horizon decoherence, and local de
   Sitter decoherence. Also compare `Gamma` with the standard-subspace entropy
   in the 2026 Bekenstein bound for localized Klein-Gordon wave packets. If
   (1) is a direct corollary after identifying those quadratic forms, stop.
   Search absence is not enough; obtain specialist review.
7. **Manuscript.** Produce a self-contained proof, literature matrix,
   reproducible certificate, and claim language that remains correct if the
   gravity corollary is removed.

## Decision Rule

Issue **FULL PAPER GO** only if Gates 1-7 close and the gravitational statement
is derived rather than assigned. Issue **NARROW PAPER GO** if Gates 1-4, 6, and
7 close, the compact-support energy theorem is independently publishable, and
gravity is labeled as an application or open problem. Otherwise issue
**NO-GO**, preserve any useful lemma as infrastructure, and do not enlarge the
claim to ER=EPR, observer complementarity, or a universal measurement-energy
principle.
