# Theorem and Claim Index

This file is the reviewer-facing index for the packaged static-patch
observer-algebra result. It separates exact finite claims, bounded certificate
evidence, conditional operator-algebra assumptions, and continuum speculation.

## Claim Boundary

The repository provides a finite executable benchmark suite. It does not prove
continuum de Sitter quantum gravity, dS/CFT, approximate QEC, or ER=EPR in de
Sitter.

The safe public claim is:

```text
finite screen-visible shadows can be incomplete; operator-algebraic response
can be necessary to identify the observer algebra or bridge channel.
```

## Basic Finite Model

At cutoff `L`, the packaged static-patch model compares:

- quantum observer algebra: `A_L = M_N`;
- diagonal screen algebra: `S_L = C^N`;
- dephased control algebra: `D_L = C^N`;
- screen map: diagonal restriction or dephasing;
- intrinsic operator-response probes: off-diagonal matrix units, commutators,
  relative/operator response, and finite generator covariance data.

The finite screen-shadow class used in the package consists of diagnostics that
factor through the diagonal screen algebra or through bounded low-order
screen-restricted transfer data. In formulas, a screen-visible diagnostic is any
declared functional of `E_diag(rho)`, diagonal correlators, finite
horizon-overlap counts, and low-order screen-restricted transfer records. It is
not allowed to query off-diagonal matrix units or commutators directly.

This is a deliberately finite benchmark definition, not a canonical continuum
definition of a gravitational screen.

## Exact Finite Claims

### Theorem A: Screen-Shadow Collision

There are finite static-patch benchmark pairs whose screen-visible diagnostics
agree while the recoverable algebra differs as `M_N` versus `C^N`.

Status: exact finite theorem/certificate stack plus bounded regulator checks.

Primary artifacts:

- `docs/goals24_31_static_patch_bridge_theorem_note.md`
- `docs/goals24_31_static_patch_bridge_certificate_index.json`
- `qgtoy/conditional_ds_er_epr.py`
- `qgtoy/static_patch_testbed.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy conditional-ds-er-epr --max-cutoff 5 --screen-probability 0.75 --low-order 2
```

### Theorem B: Strong-Continuity Gate

Let `Lambda_L(delta)=exp(delta G_L)` be an identity-starting finite semigroup
with `||G_L|| <= Gamma_L`. If the cutoff lapse satisfies
`delta_L Gamma_L -> 0`, then

```text
||Lambda_L(delta_L)-id|| <= exp(delta_L Gamma_L)-1 -> 0.
```

This finite condition rules out instantaneous dephasing routes such as
stationary modular twirling, without assuming off-diagonal survival as an
axiom.

Status: finite semigroup theorem gate.

Primary artifacts:

- `docs/goal31_static_patch_strong_continuity_note.md`
- `docs/goal31_static_patch_strong_continuity_certificate_index.json`
- `qgtoy/static_patch_strong_continuity.py`
- `tests/test_static_patch_strong_continuity.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

### Proposition C: Cofinal Full-Matrix Inclusion Scaffold

Consecutive spherical cutoffs `N_L=(L+1)^2` do not admit exact unital
trace-preserving full-matrix inclusions `M_{N_L} -> M_{N_{L+1}}` for `L >= 1`,
because `N_L` does not divide `N_{L+1}`.

The cofinal factorial subsequence

```text
L_k=(k+1)!-1,    N_k=((k+1)!)^2
```

does admit trace-preserving inclusions by amplification. The corresponding UHF
inductive limit has tracial GNS closure equal to the hyperfinite Type `II_1`
factor under the standard UHF trace-closure theorem. The dephased diagonal
control has the same levelwise screen shadows but an abelian von Neumann limit.

Status: finite construction plus standard operator-algebra theorem, conditional
on the chosen cofinal inclusion.

Primary artifacts:

- `docs/major_goal_finite_to_typeii_static_patch_observer_algebra_note.md`
- `docs/major_goal_finite_to_typeii_static_patch_observer_algebra_certificate_index.json`
- `qgtoy/typeii_static_patch_limit.py`
- `tests/test_typeii_static_patch_limit.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

## Bounded Certificate Evidence

### Audit D: Inclusion-Covariant Dynamics

Exact finite covariance fails for the raw fuzzy-sphere Hamiltonians under the
rank-ordered block embedding. The conditional-expectation version,

```text
E_k G_{k+1} iota_k(x) ~= G_k(x),
```

has decreasing bounded errors along the factorial subsequence in the current
certificate. The heat/Lindblad and short-time semigroup covariance bounds also
decrease across the audited levels. The dephased diagonal screen dynamics is
exactly inclusion-covariant and abelian.

Status: bounded asymptotic theorem/no-go audit, not a completed continuum
dynamics theorem.

Primary artifacts:

- `docs/inclusion_covariant_static_patch_dynamics_note.md`
- `docs/inclusion_covariant_static_patch_dynamics_certificate_index.json`
- `qgtoy/inclusion_covariant_dynamics.py`
- `tests/test_inclusion_covariant_dynamics.py`

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

## Conditional Assumptions

The packaged Type-II/static-patch interpretation depends on:

- the cofinal factorial cutoff subsequence;
- the standard UHF trace-closure theorem;
- the physical interpretation of the finite matrix inclusions as cutoff
  refinement;
- the `rank_ordered_static_patch_embedding` used in the current dynamics audit.

The main open question is whether a more canonical inclusion or conditional
expectation should come from angular-momentum branching, Berezin-Toeplitz
refinement, heat-kernel coarse graining, continuum `L^2(S^2)` projections, or
approximate embeddings.

## Not Claimed

The following are deliberately not claimed:

- a continuum de Sitter observer-algebra theorem;
- a dS/CFT dictionary;
- literal ER=EPR in de Sitter;
- novelty of standard stabilizer/OAQEC, Schur-channel, UHF, or Type `II_1`
  background facts;
- canonical status of the factorial cutoff subsequence.

## Reviewer Reproduction

Run the focused package regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics
```

Run the compact example script:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

