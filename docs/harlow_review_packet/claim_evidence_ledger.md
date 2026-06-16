# Harlow Review Packet: Claim-Evidence Ledger

Status: external-claim audit after the bounded U8a and Paper R sprints,
refreshed 2026-06-15

This ledger governs the wording of the Harlow review packet. It separates
established mathematics, conditional physical interpretation, and open
bridges. A composite sentence inherits the least-complete status of its
ingredients.

## Status vocabulary

- **[PROVED]** means an analytic or computer-assisted statement is established
  on its declared domain. It does not license a broader physical
  interpretation.
- **[CONDITIONAL]** means an exact implication assumes a stipulated model, or
  the physical interpretation is supported only by source-bound design
  evidence. The condition must appear with the claim.
- **[OPEN]** means a required implication, theorem, or physical identification
  has not been established.
- **INCONCLUSIVE STOP** is a bounded-route research decision, not a fourth
  theorem status or a physical no-go. It applies separately to the rigid-
  current local-matter promotion and the completed Paper R sprint.

`S_dir`, effective record dimension, Casimir, QFI, thermodynamic entropy, and
the observer entropy `S_Ob` remain distinct. Classical record stability is not
quantum-state coherence, measurement back-action is not gravitational
backreaction, and fixed-background response is not self-consistent gravity.

## Executive claim state

| ID | Status | Conservative external wording | Evidence and boundary |
| --- | --- | --- | --- |
| E1 | **[PROVED]** | Every state and measurement in the declared Haar-prior relational `SO(3)` task obeys global, tail-robust resource lower bounds. | W3; `docs/global_so3_reference_risk.md`; focused tests. This is not an observer-entropy theorem. |
| E2 | **[PROVED]** | Named localized matter classes convert rotational capacity into support and energy cost. | W3a and W3b; orbital and supported-collective documentation and tests. These are class-specific results. |
| E3 | **[CONDITIONAL]** | One ten-dimensional spatially smeared Bunch-Davies detector has a common-input finite-switch channel bound and finite degradation box if the QFT channel bridge holds. | AS proves the regular-Gaussian-bath lemma. AS2 pays factor `50`; conditionally, normalized diamond error is `<0.039` and U7 gives `R_physical>=0.532753...>1/2`. The KMS GNS/Araki-Woods propagator and regulator-uniform Gaussian identity remain open. |
| E4 | **[OPEN]** | One norm-controlled local-matter interaction has not yet been shown to acquire, store, and expose the directional record while entering the same stress ledger. | Independently of E3's bridge, distinct components of the exact factorized rigid current have a nonzero commutator under disjoint spacelike smearings, so that density cannot be promoted unchanged. Different local completions reopen multipole and band errors. |
| E5 | **[PROVED]** | Fixed pure de Sitter has exact static `ell=2` master-source, ideal-shell transmission, and exterior electric-Weyl reconstruction maps. | W3m, W3t, W3v, and W3x. Exact maps do not prove a nonzero completed source amplitude. |
| E6 | **[CONDITIONAL]** | The completed corrected response estimator is stably negative: `[-0.003079554319910408,-0.002552931394151071]`. | Paper R decision artifact SHA256 `bcbb4a1af96b445b84464ddeda83cb6a568b0061bbc5146dd8fc11e72e124292`. The estimator is design evidence, not a continuum lower bound. |
| E7 | **[PROVED]** | The completed response interval is `[-0.027341192151999246,0.021708706437937767]`; it contains zero and triggers **INCONCLUSIVE STOP**. | `experiments/paper_r_response_certificate.json`; `docs/paper_r_viability_decision.md`. All frozen origin, bulk, and wall proof terms are included. |
| E8 | **[OPEN]** | No positive lower bound `|B_W|>=b_min>0` is proved. | A future attempt requires a materially different primal proof object. The STOP decision is not evidence that the response vanishes. |
| E9 | **[PROVED]** | A computer-assisted theorem establishes one local, strictly decreasing hard-wall Skyrmion profile with negative wall slope and finite positive inertia at the declared fixed-background parameters. | AU.1 and exact profile artifact indexed below. This is not a rotating or self-gravitating solution. |
| E10 | **[OPEN]** | `S_dir` has not been identified with `S_Ob`, and the one-action observer tradeoff has not been proved. | These are the first and third review questions, not packet conclusions. |
| E11 | **[OPEN]** | No new relational theorem yet shows that information beyond a nondisturbingly readable classical sector, written to a blank record, forces disturbance of the complete `OD` source. | Generic channel information-disturbance, Koashi-Imoto, no-broadcasting, WAY, and resource-cost theorems are prior art and direct subsumption tests. |

## Observer-register claim boundary

| Status | Claim allowed in the packet | Required qualification |
| --- | --- | --- |
| **[PROVED]** | `R_ref>=1/(16<J^2>+8)` and `R_ref>=c_SO3 exp(-2S_dir/3)` for the declared global relational task. | Do not call either result an absolute-frame, local-QFI, memory-size, or observer-entropy theorem. |
| **[PROVED]** | Confined spinless orbital matter obeys `<L^2><=2Ma^2E_ex`; supported Skyrmion collective profiles obey the stated inertia and sector-floor bounds. | Keep the orbital and adiabatic collective domains explicit. |
| **[CONDITIONAL]** | The declared Bunch-Davies rigid-detector EFT obeys the AS2 finite-switch channel and degradation bounds if the QFT channel bridge holds. | Keep the proved regular-bath lemma, open KMS GNS bridge, factorized extended-detector action, factor `50`, declared box, and absence of a hardware-lifetime theorem explicit. |
| **[OPEN]** | Costly net relational information may obey an acquisition-disturbance bound after the nondisturbingly readable classical sector is removed. | This is the active theorem target, not a packet result; the metric, source subclass, and non-subsumption proof remain to be supplied. |
| **[OPEN]** | Local-matter preparation, storage, readout, support stress, and backreaction are not controlled by one action on one open parameter family. | The rigid-current locality STOP is route-specific; this remains the main physical bridge for Paper U. |

## Fixed-background response decision

For conforming primal and adjoint trials, W3z.17 gives

```text
J_hat = J_rigid + B(y_h) + R_y(z_h),
|A_ext-J_hat| <= ||R_y||_(q*) ||R_z||_(q*).
```

The completed source-bound sprint certifies:

| Quantity | Certified value |
| --- | --- |
| Corrected estimator | `[-0.003079554319910408,-0.002552931394151071]` |
| Complete primal norm | `<0.785351351663998829` |
| Complete loaded-adjoint norm | `<0.030892717992632714` |
| Residual-product error | `<0.024261637832088839` |
| Full exterior amplitude | `[-0.027341192151999246,0.021708706437937767]` |
| Decision ratio | `<8.708392897914348130` |
| Frozen decision | **INCONCLUSIVE STOP** |

The estimator excludes zero; the full response interval does not. Holding the
estimator and adjoint bound fixed, zero exclusion would require
`delta_y<0.082638613888227453`, about a `9.50`-fold reduction from the present
primal norm. The dominant primal cell is `[1/2,11/16]`, and the global
coercivity floor is not the main loss.

Allowed interpretation: the present proof representation is not sharp enough.
Forbidden interpretations: the response vanishes, a cancellation theorem has
been proved, Paper R is nearly publishable, or more generic subdivision is the
obvious next step. Resume Paper R only with a better conforming primal trial, a
direct certified Riesz solve, or a structural decomposition.

## Source-bound artifact index

The hashes below were recomputed from the current worktree on 2026-06-15.

| Role | Artifact | SHA256 | Evidentiary use |
| --- | --- | --- | --- |
| Abstract observer composition | `experiments/universal_observer_tradeoff_certificate.json` | `2bd73ea29cc649ed8dbc99f266d0fafa07c6b294a7a3d4cb87d88cd791168487` | **[PROVED]** conditional implication |
| AU.1 nonlinear profile | `experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json` | `c4c95db47470392f0963266e37b491ae49a09381464f3da97c3f97bd14e74eff` | **[PROVED]** hard-wall profile |
| Fixed-de Sitter resolvent | `experiments/static_patch_l2_response_exact_certificate.json` | `45871bfe3e15a65b546eddd6391d42d0d8e6665ee981c9f24618409f52dcd051` | **[PROVED]** exact Green operator |
| Centrifugal inverse | `experiments/centrifugal_skyrmion_friedrichs_form_certificate.json` | `4a4e3ecd48a205860de3aa045c94d2b825c0afce1c0f12f4b96254db355b85bb` | **[PROVED]** closed operator and inverse |
| Nonzero weak matter response | `experiments/centrifugal_skyrmion_forced_response_certificate.json` | `9edc2bc479534fab3f527ce535a373da1373b45085c6fbf4602f4ee9cdd32db7` | **[PROVED]** matter response only |
| Master-source map | `experiments/static_patch_l2_master_source_certificate.json` | `3be17612134bb6b72535db9d3c80a74acf1271a39e04eec4b1591c9bd8967887` | **[PROVED]** exact map |
| Ideal-shell transmission | `experiments/static_patch_l2_transmission_certificate.json` | `c83536779d2ab62684218291dd99de190569f9973417d9accd2ceff426901ade` | **[PROVED]** exact distributional law |
| Weyl reconstruction | `experiments/static_patch_l2_weyl_reconstruction_certificate.json` | `3025d65fe82585e584150e956de9481380ab3f4a72d26a7cacb744974838c070` | **[PROVED]** exact vacuum reconstruction |
| Signed outer estimator | `experiments/validated_centrifugal_correlated_estimator.json` | `078e596f394aabcee86a8f8d89d6282ffef37342b9fa9a1a5f155577b3cb8c9a` | **[PROVED]** interval evaluation; physical sign remains conditional |
| Signed origin estimator | `experiments/validated_centrifugal_origin_corrected_estimator.json` | `f7ce2946b2cc2c97bbe75cb5dbc379975a2fc7985efd0ce2ed2953c776189156` | **[PROVED]** includes cutoff trace |
| Origin primal data | `experiments/validated_centrifugal_origin_profile_jets.json` | `51a6d1e66de43e89c10471c0f3962030b172e37faccad6f56cff6421fd844300` | **[PROVED]** strong origin residual inputs |
| Origin adjoint load | `experiments/validated_centrifugal_origin_adjoint_load.json` | `0f6f5e42be8906eb863e11f827eb8b93d47d59ddc576be73acb185b13d91c52e` | **[PROVED]** regular-origin master load |
| Origin weak dual | `experiments/validated_centrifugal_origin_weak_dual.json` | `3e7d4ed151c417d076872c59947027a12aa5acd295b780182c7d7f5fa6af2e6d` | **[PROVED]** loaded origin adjoint bound |
| Interface cancellation | `experiments/centrifugal_conormal_interface_certificate.json` | `1ee677788edc45190c9b164c45bc4a76a1b9e395d172f12b5aa13241748200e2` | **[PROVED]** no internal conormal deltas |
| Wall master load | `experiments/validated_centrifugal_wall_master_load.json` | `4be9f09ffda9acd5708ae608d33393e8f913587cd1245cb35b83acc660709797` | **[PROVED]** current wall load |
| Complete primal dual bound | `experiments/validated_centrifugal_correlated_primal_dual.json` | `c845afa6c0cedc18a08f25b9ca5d02314888306189eed29d7012f819f2dec5a4` | **[PROVED]** all-strong bulk, origin, and wall |
| Complete adjoint dual bound | `experiments/validated_centrifugal_correlated_adjoint.json` | `86424d4430c540970051e1815c30ca3b51fc24c03b55840c41472c1fe83b1f00` | **[PROVED]** weak bulk, origin, and wall |
| Paper R decision | `experiments/paper_r_response_certificate.json` | `bcbb4a1af96b445b84464ddeda83cb6a568b0061bbc5146dd8fc11e72e124292` | **[PROVED]** zero-containing interval and STOP rule |

## Verification

The decisive U8a and response results are replayed with:

```bash
PYTHONPATH=. python -m pytest -q tests/test_u8a_finite_storage_channel.py
PYTHONPATH=. python -m qgtoy u8a-finite-storage-channel
PYTHONPATH=. python experiments/paper_r_response_certificate_audit.py
PYTHONPATH=. python -m pytest -q \
  tests/test_paper_r_response_certificate.py \
  tests/test_paper_r_response_certificate_audit.py \
  tests/test_paper_r_state_transfer.py \
  tests/test_paper_r_wall_composition.py \
  tests/test_paper_r_weyl_observable.py
```

Result on 2026-06-10: the audit reproduced SHA256
`bcbb4a1af96b445b84464ddeda83cb6a568b0061bbc5146dd8fc11e72e124292`
with decision `INCONCLUSIVE_STOP`; the focused test batch reported
`27 passed in 3.44s`.

The packet-level render, wording, links, and manifest are checked with:

```bash
docs/harlow_review_packet/build_packet.sh
node docs/harlow_review_packet/audit_packet.mjs
```

## Packet-level allowed conclusion

The strongest accurate summary is:

> **[PROVED]** The project has global operational `SO(3)` resource bounds,
> named matter-capacity theorems, a regular-Gaussian-bath finite-switch channel
> lemma, a validated fixed-background hard-wall profile, exact fixed-de-Sitter
> response maps, and a completed bounded Paper R viability certificate.
> **[CONDITIONAL]** The named Bunch-Davies detector box, the Skyrmion
> realization, and the negative corrected response
> estimator remain design evidence. **[OPEN]** The common-action local-matter
> record channel, the
> `S_dir`-to-`S_Ob` dictionary, the gravitational capacity variable, nonzero
> continuum Weyl response, self-consistent gravity, and a common parameter
> window remain unresolved.

This is enough to ask Dr. Harlow whether the architecture targets a useful
observer concept and which gravitational quantity should replace or refine the
provisional witness. It is not enough to present Paper R, the proposed observer
tradeoff, or a nonzero Skyrmion Weyl footprint as a completed physical theorem.
