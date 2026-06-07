# Finite Static-Patch Regulators Where Screen Shadows Do Not Determine the Observer Algebra

## Claim Boundary

This is a finite regulator theorem program, not a continuum de Sitter theorem,
not a dS/CFT construction, and not a proof of ER=EPR in de Sitter. The point is
to make one operator-algebraic diagnostic question sharp:

```text
Do screen-visible data determine the observer algebra?
```

In the finite certificates here, the answer is no. Screen shadows can agree
between a quantum matrix-algebra regulator and a dephased abelian control, while
intrinsic operator response and inclusion-aware dynamics distinguish them.

## Finite Setup

At cutoff `L`, the model uses a finite observer algebra `M_N`, a diagonal
screen algebra `C^N`, and dephased controls that keep only the diagonal algebra.
Static-patch-inspired channels are finite CPTP/unital Schur or semigroup
regulators acting on matrix units. The diagnostic split is:

- screen-visible data: diagonal entropy, screen correlators, horizon overlap,
  and screen-restricted transfer;
- operator-visible data: off-diagonal response, commutators, bridge algebra,
  and inclusion-compatible generator behavior.

The finite objects are deliberately small and exact. They are a certificate
suite and hypothesis generator, not a substitute for continuum static-patch
construction.

## Theorem Spine

**Finite screen-shadow no-go.** Goals 24-31 package a finite theorem stack in
which screen-visible data agree while the recoverable bridge algebra differs as
`M_N` versus `C^N`. The no-go persists across physically motivated finite
regulators, including fuzzy-sphere/static-patch Hamiltonian dephasing,
finite-environment phase-kick traces, KMS/modular averages, and Euclidean-like
Schur transfers, within the declared bounded checks.

**Strong-continuity gate.** KMS/detailed balance alone is insufficient:
stationary modular twirling is a CPTP/unital complete-dephasing counterexample.
The finite replacement is a non-tautological semigroup condition. If
`Lambda_L(delta)=exp(delta G_L)`, `||G_L|| <= Gamma_L`, and
`delta_L Gamma_L -> 0`, then

```text
||Lambda_L(delta_L)-id|| <= exp(delta_L Gamma_L)-1 -> 0.
```

This rules out instantaneous dephasing without assuming the bridge algebra or
off-diagonal response as an axiom.

**Finite-to-Type-II scaffold.** Consecutive spherical cutoffs
`N_L=(L+1)^2` do not form exact unital full-matrix inclusions because
`N_L` does not divide `N_{L+1}` for `L >= 1`. A cofinal factorial subsequence

```text
L_k=(k+1)!-1,    N_k=((k+1)!)^2
```

does admit trace-preserving inclusions `M_{N_k} -> M_{N_{k+1}}` by
amplification. The quantum sequence is a UHF inductive limit whose tracial GNS
closure is the hyperfinite Type `II_1` factor under the standard UHF trace
closure theorem. The dephased diagonal control has the same screen/trace
shadows but an abelian von Neumann limit.

**Inclusion-covariant dynamics audit.** Exact finite generator covariance fails
for the raw fuzzy-sphere Hamiltonians under the rank-ordered block embedding.
The useful weaker condition is conditional-expectation covariance,

```text
E_k G_{k+1} iota_k(x) ~= G_k(x),
```

where `E_k=id tensor tau_fiber`. The bounded certificates show decreasing
modular, heat/Lindblad, conditional-expectation, and short-time semigroup
covariance errors along the factorial subsequence. The dephased screen control
is exactly inclusion-covariant and abelian.

## What Is New Versus Standard

Standard ingredients include finite matrix algebras, diagonal subalgebras,
stabilizer/QEC diagnostics, Schur channels, UHF inductive limits, trace
closures, and operator-algebraic language for reconstruction. The contribution
here is the linked finite benchmark and obstruction ledger:

- screen-shadow collisions are certified next to operator-response witnesses;
- KMS-only dynamics are explicitly separated from continuity-compatible
  dynamics;
- the finite matrix sequence is audited for Type `II_1` promotion and compared
  against an abelian control with the same screen data;
- the remaining load-bearing assumption is isolated as the physical cutoff
  embedding/generator compatibility problem.

## Expert Question

The current package uses a rank-ordered static-patch embedding on a cofinal
factorial cutoff sequence. Is that a reasonable finite approximation to
static-patch mode refinement, or should the inclusion/conditional expectation be
replaced by a more canonical construction, such as angular-momentum branching,
coherent-state or Berezin-Toeplitz refinement, heat-kernel coarse graining,
continuum `L^2(S^2)` projection maps, or approximate rather than exact
full-matrix embeddings?

Equivalently: is cutoff-compatible strong continuity plus conditional
expectation covariance the right finite shadow of static-patch observer-algebra
dynamics, or is a different operator-algebraic axiom the natural one?

## Reproducibility

| Claim | Command |
| --- | --- |
| Strong-continuity theorem gate | `PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Finite-to-Type-II scaffold | `PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Inclusion-covariant dynamics audit | `PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Focused package tests | `PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics` |

Machine-readable certificate indexes are listed in
`docs/static_patch_observer_algebra/audit_index.json`.

