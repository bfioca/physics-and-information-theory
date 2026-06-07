# Static-Patch Observer-Algebra Package

Start here for the current packaged result. The rest of the repository keeps the
goal-by-goal audit trail, but this folder is the compact reader path.

## Lead Claim

This repository gives a finite regulator program for static-patch
observer-algebra diagnostics:

```text
screen shadows can agree between a quantum matrix-algebra regulator and a
dephased abelian control, while intrinsic operator response and inclusion-aware
dynamics distinguish the observer algebra.
```

The result is finite and certificate-backed. It is not a continuum de Sitter
theorem, not a dS/CFT construction, and not a proof of ER=EPR in de Sitter.

## Package Files

| File | Use |
| --- | --- |
| `../../THEOREMS.md` | Reviewer-facing theorem and claim index. |
| `../../paper/main.md` | Canonical paper-shaped technical note. |
| `../../REPRODUCIBILITY.md` | One-command reproduction and frozen artifact validation. |
| `../../paper/expert_feedback_note.md` | Two-page expert-facing feedback note. |
| `../../paper/expert_cover_note.md` | Short cover note for expert feedback. |
| `../breakthrough_continuum_lift_obstruction_plan.md` | Next-path plan for turning the conditional lift schema into a theorem candidate, no-go, or weakest-added-assumption result. |
| `../continuum_lift_obstruction_execution_goal.md` | Short execution goal for completing the continuum-lift obstruction branch step by step. |
| `../screen_shadow_functor_spec.md` | Formal finite `Sh_L` definition and screen-shadow equality proof. |
| `../response_witness_spec.md` | Operator-norm response witness and persistence topology. |
| `../lift_map_obligations.md` | Lift-map theorem/certificate/assumption ledger. |
| `../continuum_lift_decision_ledger.md` | Decision ledger selecting the theorem-candidate endpoint. |
| `../continuum_lift_obstruction_theorem.md` | Proof-ready screen-only dictionary obstruction theorem under explicit lift hypotheses. |
| `../physical_static_patch_lift_hinge.md` | Physics-hinge audit for physically natural static-patch lift maps and the minimal missing assumption. |
| `../canonical_noncommutative_refinement_note.md` | Sharpened audit of which physically selected subsystems can carry a cutoff-independent noncommutative response. |
| `../canonical_noncommutative_refinement_certificate_index.json` | Machine-readable claim-to-command map for the canonical refinement audit. |
| `../observer_local_subsystem_note.md` | Observer-local tangent-plane theorem candidate with nonzero commutator lower bounds. |
| `../observer_local_subsystem_certificate_index.json` | Machine-readable claim-to-command map for the observer-local subsystem audit. |
| `expert_feedback_two_page_note.md` | Short expert-facing theorem note and open question. |
| `audit_index.json` | Machine-readable map from major claims to commands, source files, and tests. |
| `journey_map.md` | How the earlier goals support the packaged result without becoming the lead. |

## Result Spine

| Layer | Status | Main point |
| --- | --- | --- |
| Screen-shadow no-go | finite certificate stack | Diagonal/screen/entropy-like data do not determine the finite bridge algebra. |
| Strong-continuity gate | finite semigroup theorem | If `delta_L Gamma_L -> 0`, then finite dynamics remain approximate identity instead of instant dephasing. |
| Finite-to-Type-II scaffold | conditional operator-algebra theorem candidate | A cofinal factorial cutoff sequence gives a UHF quantum limit whose tracial closure is a hyperfinite Type `II_1` candidate. |
| Abelian control | exact levelwise control | The dephased diagonal sequence keeps the same screen shadows but has an abelian von Neumann limit. |
| Inclusion-covariant dynamics | bounded asymptotic audit | Exact covariance fails for raw Hamiltonians, while conditional-expectation and short-time covariance errors decrease along the factorial subsequence. |
| Cutoff-refinement embeddings | finite physical-motivation audit | Consecutive cutoffs admit trace-filled, harmonic, heat-kernel, and Berezin-inspired refinements with vanishing error bounds and persistent response witnesses. |
| Continuum lift obstruction | proof-ready conditional theorem candidate | Under explicit lift conditions, any dictionary factoring only through screen shadows is incomplete when response witnesses persist. |
| Physical static-patch lift hinge | minimal missing assumption | Harmonic and heat routes are bounded-positive but noncanonical; KMS alone and common commutative screens give no-gos; a norm-faithful noncommutative cutoff refinement is the missing physics input. |
| Canonical noncommutative refinement | sharper minimal missing assumption | Scalar fuzzy-sphere low modes are canonical but classicalize; the next required input is a canonical fixed noncommutative subsystem with nonzero commutator scale. |
| Observer-local tangent subsystem | theorem candidate | Coherent-state tangent-plane scaling gives a fixed low-excitation window with commutator lower bound `1 - 2R/L`, leaving Type-II/static-patch interpretation conditional. |
| Remaining assumption | open physics/math question | Is `rank_ordered_static_patch_embedding` the right cutoff embedding, or should a canonical fuzzy-sphere/static-patch embedding replace it? |

## Fast Reproduction

Run the static-patch package regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics
PYTHONPATH=. python3 -m unittest tests.test_embedding_channels tests.test_continuum_lift_obstruction tests.test_lift_diagnostics
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

Emit the three lead certificates:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy static-patch-embedding-channels --max-cutoff 5
PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5
```

Validate the packaged indexes:

```bash
python3 -m json.tool docs/static_patch_observer_algebra/audit_index.json
python3 -m json.tool docs/goals24_31_static_patch_bridge_certificate_index.json
python3 -m json.tool docs/major_goal_finite_to_typeii_static_patch_observer_algebra_certificate_index.json
python3 -m json.tool docs/inclusion_covariant_static_patch_dynamics_certificate_index.json
```

## Audit Trail

The compact package depends on these existing artifacts:

- `docs/goals24_31_static_patch_bridge_theorem_note.md`
- `docs/goals24_31_static_patch_bridge_certificate_index.json`
- `docs/major_goal_finite_to_typeii_static_patch_observer_algebra_note.md`
- `docs/major_goal_finite_to_typeii_static_patch_observer_algebra_certificate_index.json`
- `docs/inclusion_covariant_static_patch_dynamics_note.md`
- `docs/inclusion_covariant_static_patch_dynamics_certificate_index.json`
- `docs/canonical_embedding_program.md`
- `docs/static_patch_embedding_channels_certificate_index.json`
- `docs/continuum_lift_conditions.md`
- `docs/continuum_lift_obstruction_certificate_index.json`
- `docs/screen_shadow_functor_spec.md`
- `docs/response_witness_spec.md`
- `docs/lift_map_obligations.md`
- `docs/continuum_lift_decision_ledger.md`
- `docs/continuum_lift_obstruction_theorem.md`
