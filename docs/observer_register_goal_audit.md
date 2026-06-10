# Observer-Register G1/G2 Goal Audit

Audit date: 2026-06-10 UTC

Status: **PASS** for the bounded goal of an audit-ready G1/G2 specification and
manuscript skeleton. This does not mark the full Paper U theorem complete.

## Deliverables

| Requirement | Evidence | Result |
| --- | --- | --- |
| exact `C_dir` quantifiers | `observer_register_model_class.md`, Sections 1-10 | **PASS** |
| systems, states, environment, action, controls, and protocols | model tuple and Sections 2-4 | **PASS** |
| randomized/adaptive protocols | causal-comb and deferred-measurement rule, Section 4 | **PASS** |
| invariant ancillas and pre-correlated memories | full accessible-state convention, Sections 2.2-2.3 | **PASS** |
| postselection and success probability | unconditional loss and success-weighted bound, Section 5 | **PASS** |
| external resources | charged-controller and hidden-memory rules, Sections 2-3 | **PASS** |
| pointwise/asymptotic scope | Section 9 | **PASS** |
| approximation order and error composition | Section 8 | **PASS** |
| proper/optical localization | Sections 6-7 | **PASS** |
| status-labeled resource chain | `directional_record_resource_dictionary.md`, Sections 3-10 | **PASS** |
| all requested resource distinctions | dictionary Section 2 | **PASS** |
| eight required counterexamples | `observer_register_counterexample_checklist.md`, X1-X8 | **PASS** |
| clean manuscript skeleton | `paper/universal_observer_tradeoff_outline.md` | **PASS** |
| Paper R only as STOP diagnostic | outline Section 10 | **PASS** |
| Skyrmion removable realization support | outline Section 9 | **PASS** |
| three Harlow pivots | `harlow_redirection_branches.md`, Branches 1-3 | **PASS** |

## Acceptance criteria

| Criterion | Audit result |
| --- | --- |
| a skeptical reader can construct a counterexample without guessing the observer or protocol | **PASS**: the tuple, orbit, accessible-system boundary, protocol comb, and X1-X8 recipes are explicit |
| no converse is inferred from a one-way resource inequality | **PASS**: the chain is a fork and all forbidden converses are labeled `FALSE` |
| effective record dimension is used only for a declared classical record or outcome | **PASS**: only `d_eff^cl(C)=exp H(C)` is defined, under a finite discrete Markov bottleneck |
| no statement identifies `S_dir` with `S_Ob` | **PASS**: the comparison is labeled `OPEN` and the Harlow goal was corrected |
| Paper U does not require certified nonzero `B_W` | **PASS**: `B_W` is absent from every theorem premise and Paper R is an `INCONCLUSIVE STOP` diagnostic |
| new lemmas have tests or proof notes | **PASS**: dictionary proof notes P1-P6 cover the newly exposed dual, classical bottleneck, postselection, energy inversion, and error-composition steps |
| existing relevant theorem tests pass | **PASS**: 76 focused tests passed |

## Exact arrow disposition

### Closed positive arrows

| ID | Arrow | Domain |
| --- | --- | --- |
| R1 | target Haar risk -> actual readout mutual information | `C_dir^op` |
| R2 | actual/accessible information <= joint `S_dir` | `C_dir^op` |
| R3 | target Haar risk -> required joint `S_dir` | `C_dir^op` |
| J1 | target Haar risk -> required mean Casimir | `C_dir^op` |
| J2 | required `S_dir` -> required mean representation label | integer-spin `C_dir^op` |
| E3 | target Haar risk -> orbital excitation cost | `C_dir^orb` |

### Closed under explicit additional assumptions

| ID | Arrow | Necessary assumption |
| --- | --- | --- |
| C1 | target risk -> finite classical entropy/alphabet | a named finite discrete record `C_T` with `G -> C_T -> Y` and no bypass side information |
| E1 | required `S_dir` -> directional-system energy | invariant `H_dir` on the same full representation and finite `Z_H(beta)` |
| G-proxy | energy and proper support -> compactness proxy | confined positive-energy orbital model plus the declared compactness inequality |
| heat | capacity and heat exposure -> finite-time risk floor | actual or norm-controlled isotropic `SO(3)` heat channel |

### Closed as false general converses

| ID | Rejected arrow | Counterexample |
| --- | --- | --- |
| C2 | `S_dir` -> classical record dimension | asymmetric state may be discarded; invariant multiplicity need not carry orientation information |
| J3 | large Casimir/mean spin -> good reference | invariant high-spin mixture |
| E2 | generic finite energy -> bounded directional capacity | bounded-spectrum `H_bad` |
| F1 | large `S_dir` -> small global risk | `|j,0>` has diverging asymmetry and a half-turn stabilizer |
| F2 | large local QFI -> small global risk | rare-tail and stabilizer examples |
| F3 | `S_dir` = thermodynamic or von Neumann entropy | pure asymmetric and mixed invariant states separate the quantities |
| R-dependency | nonzero `B_W` is required for Paper U | removed by theorem design; the existing interval contains zero |

### Open arrows

| ID | Arrow | Missing input |
| --- | --- | --- |
| E4 | classical record size -> energy cost | a declared memory Hamiltonian, preparation/readout work model, and side-information rule |
| F4 | `S_dir` compared with `S_Ob` | a common state space, conditional expectation, and observer-framework comparison theorem |
| G1 | energy/support -> preferred gravitational capacity or disturbance | a selected gauge-invariant functional derived from the common action |
| G2 | gravitational capacity -> `S_Ob` | an observer-algebra or closed-universe path-integral bridge |

## Assumptions that remain necessary

1. Every accessible side-information system is inside the joint resource and
   physical ledgers; no hidden frame or memory may re-enter.
2. Conditional postselection claims retain `p_s`; the unconditional theorem is
   the default.
3. A finite classical record claim names the discrete bottleneck and proves
   the Markov factorization.
4. An energy claim uses sector floors of the same complete representation as
   `S_dir`, or remains inside the hard-confined orbital model.
5. Proper and optical radii refer to the same support before the lapse
   conversion is used.
6. A physical Paper U theorem still requires a common local action, a
   norm-controlled acquisition/storage/readout channel, a selected
   gravitational functional, and one common parameter box.

## Verification

Command:

```bash
python -m pytest -q \
  tests/test_global_so3_reference_risk.py \
  tests/test_localized_orbital_reference.py \
  tests/test_rotational_spectral_capacity.py \
  tests/test_rotational_resource_substitution_no_go.py \
  tests/test_orientation_stabilizer_risk.py \
  tests/test_orientation_stabilizer_risk_audit.py \
  tests/test_covariant_observer_energy_no_go.py \
  tests/test_universal_observer_tradeoff.py \
  tests/test_localized_so3_observer_tradeoff.py \
  tests/test_redshifted_frame_capacity.py \
  tests/test_so3_measure_correct_recovery.py
```

Result: `76 passed in 0.52s`.

`git diff --check` also passes.

## Non-goal audit

No Paper R interval calculation, Israel matching, self-gravity sprint,
`S_dir=S_Ob` proof attempt, full manuscript prose, or Paper A promotion was
performed. The only Paper R change is its placement as an inconclusive
diagnostic in the claim hierarchy.

