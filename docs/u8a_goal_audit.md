# Paper U U8a Goal Audit

Audit date: 2026-06-10 UTC

Status: **INCONCLUSIVE STOP for U8a.** The regular Gaussian-bath finite-switch
lemma and the conditional `WT-R1/D1` box are reusable, but their application to
the named Bunch-Davies field still needs a regulator-uniform KMS GNS/Pauli-
Fierz channel bridge. Independently, the exact factorized density cannot be
promoted unchanged to a microcausal local-matter current while retaining the
zero-error ledger. That rigorous locality obstruction stops this route. Paper
U U8a, preparation, and readout remain open.

## Requirement audit

| Requirement | Evidence | Result |
| --- | --- | --- |
| one fixed finite global-`SO(3)` register | `R_1=(V_0 tensor V_0*) direct_sum (V_1 tensor V_1*)`, dimension `10` | **PASS** |
| one fixed target | inert distinguishable target `D=V_1` | **PASS** |
| named smooth compact detector action | pseudoscalar improved gradient, exact `a/R=1/5` optical convolution profile, parallel transport, explicit `chi_(B,T)` switch, rigid current | **PASS as a formal action target** |
| KMS QFT reduced channel | construct the GNS/Araki-Woods propagator, prove regulator-uniform Nathan-Rudner estimates, and pass the map inequality to the limit | **OPEN** |
| microcausal local-matter action | for disjoint equal-time test functions with nonzero weighted integrals, `[ell_1(f),ell_2(g)]=i alpha_f alpha_g J_3` is nonzero on the `V_1` block | **FAIL for the exact factorized route; different local completions open** |
| derive the finite-time storage channel | `F_(B,T)` and `U_free o U_LS o H_s o P_B` have the same pre-switch input time | **CONDITIONAL PASS in the regular Gaussian-bath framework; named QFT bridge open** |
| no invalid plateau map | no assignment map from arbitrary correlated post-burn states is used | **PASS** |
| correctly dimensioned channel norm | `(1/2)||Delta||_diamond<=floor(D_in D_out/2)epsilon_infinity`, factor `50` | **PASS once the uniform map premise holds** |
| switching error | explicit logarithmic missing-history contribution | **PASS** |
| ULE error | stationary initial and growth contributions with exact-profile moment upper bounds | **PASS** |
| multipole error | exactly zero because the binding action uses the full smeared current, not a center-value replacement | **PASS on the named model** |
| band leakage | exactly zero because `J_left^a` preserves `j<=1` | **PASS on the named model** |
| free and Lamb unitaries | both known Casimir unitaries are included in the comparison channel | **PASS on the detector EFT** |
| operational-risk composition | U7 is evaluated after exact mean-Casimir conservation and the physical-to-heat error is subtracted | **PASS** |
| nonzero coupling interval | `(1.278e-14, 1.460e-14)` | **PASS** |
| finite switch/burn/storage durations | the open `B,T` intervals and the derived total protocol-duration bounds are finite | **PASS** |
| independent detector hardware lifetime | persistence of the EFT through the protocol is assumed, not derived | **OPEN; not claimed** |
| strict numerical guard | outward-rounded worst error is about `0.038`, strictly below the declared `0.039`; exposure lies inside `0.7<s<1` | **PASS for the conditional box** |
| finite-time degradation result | outward-rounded guard `R_physical>=0.5327532814...>1/2` on the declared box | **CONDITIONAL on the QFT channel bridge; box-local only** |
| do not begin U9/U10 | no gravitational functional or common elimination is introduced | **PASS** |
| do not revive Paper R | no Weyl-response input appears | **PASS** |
| do not claim full U8a or U8 | local matter, U8b preparation/readout, and gravity remain explicitly open | **PASS** |

## Exact disposition

Under the regular Gaussian-bath hypotheses, the channel estimate is

```text
(1/2)||F_(B,T)-U_free(T)oU_LS(T)oH_s(T)oP_B||_diamond
 < 0.039
```

throughout the certified open parameter box. The declared error gives the U7
failure threshold and the least-exposed cross-corner bound

```text
s_fail     = 0.6156552580594193,
s_box      is strictly inside (0.7,1),
R_physical >= 0.5327532814987301 > 1/2.
```

The exact switched interaction preserves `C_left`, so the post-burn state still
obeys the `9/5` mean-Casimir budget used by U7. The canonical token begins at
risk `3/8`, so the target `1/2` is initially achievable and later excluded.
This gives a conditional degradation box, not a named-QFT theorem or a
model-wide no-go. The factorized-current microcausality calculation separately
and unconditionally stops unchanged promotion of this exact factorized route
to local matter. The correct disposition is therefore:

```text
regular-bath finite-switch box: CONDITIONAL PASS.
named Bunch-Davies QFT channel bridge: OPEN.
exact-factorized local-matter promotion: INCONCLUSIVE STOP.
Paper U U8a: OPEN.
U8b: OPEN.
Full U8: OPEN.
Paper U: NOT YET A SUBMISSION THEOREM.
```

## Claim hygiene

The interaction is a smooth compact spatially smeared rigid-detector EFT. Its
factorized current and hard Peter-Weyl compression are defining assumptions,
not conclusions about microscopic matter. This is why multipole and band
errors can be zero here. A microcausal local-current completion must reopen
those terms rather than inherit the zeros.

The named QFT channel is also not obtained merely by inserting the exact
Bunch-Davies two-point spectrum. The missing GNS/Pauli-Fierz bridge must control
the unbounded smeared field, the compactly switched propagator, and regulator
removal uniformly in the stabilized channel estimate.

The certified storage times are of order `10^30 R`. Their finiteness closes the
formal detector-EFT channel subproblem, but their magnitude prevents a
practical observer claim. No independent apparatus lifetime or hardware
construction is certified.

## Verification

Focused commands:

```bash
PYTHONPATH=. python -m pytest -q \
  tests/test_u8a_finite_storage_channel.py \
  tests/test_static_patch_matter_observer_channel.py \
  tests/test_static_patch_worldtube_ule.py \
  tests/test_static_patch_smooth_worldtube_ule.py \
  tests/test_static_patch_finite_switching_ule.py \
  tests/test_finite_time_rotation_diffusion.py \
  tests/test_global_so3_reference_risk.py \
  tests/test_static_patch_pseudoscalar_gyroscope.py \
  tests/test_static_patch_hard_current_multipole.py \
  tests/test_universal_observer_tradeoff.py \
  tests/test_so3_measure_correct_recovery.py

PYTHONPATH=. python -m qgtoy u8a-finite-storage-channel
node docs/harlow_review_packet/audit_packet.mjs
```

Closure record on 10 June 2026:

- focused U8a/channel/spectral regressions: `100 passed in 12.65s`;
- CLI: `conditional_pass`, all conditional-box checks true, all three named-QFT
  bridge checks false, Paper U U8a `OPEN`, locality route `INCONCLUSIVE STOP`;
- Harlow packet: audit passed with 9 pages, 573 opening words, and 178 outreach-
  email words; visual page-one check found no clipping or readability defect;
- full repository run: `117 passed`, then stopped at the pre-existing
  `test_source_hashed_outer_tube_liouville_artifact` digest mismatch. The test
  expects SHA256 `388230...` for
  `qgtoy/validated_centrifugal_liouville_taylor.py`, while the unmodified
  current file hashes to `65e6b2...`. Neither that source nor its stored
  certificate is changed by U8a, so the unrelated authenticated artifact was
  not regenerated here.
