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
| `harlow_facing_two_page_note.md` | Short expert-facing theorem note and open question. |
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
| Remaining assumption | open physics/math question | Is `rank_ordered_static_patch_embedding` the right cutoff embedding, or should a canonical fuzzy-sphere/static-patch embedding replace it? |

## Fast Reproduction

Run the static-patch package regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics
```

Emit the three lead certificates:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
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

