# Screen Shadows and Strong Continuity in Finite Static-Patch Bridge Channels

## Claim Boundary

This note packages Goals 24-31 as a finite mathematical-physics benchmark. It
does not claim a continuum de Sitter theorem, a dS/CFT construction, or literal
ER=EPR in de Sitter. The finite claim is narrower:

```text
screen-visible static-patch data need not determine the bridge algebra;
cutoff-compatible strong continuity is a non-tautological finite gate that
rules out instantaneous dephasing while preserving the quantum bridge split.
```

## Objects

At cutoff `L`, the testbed uses finite screen modes with diagonal screen
algebra `C^N`, observer matrix algebra `M_N`, and a classical horizon control
`C^N`. Static-patch regulators act as finite Schur channels on matrix units.
The diagnostic split is between screen shadows, which see diagonal/entropy-like
data, and bridge response, which sees whether the recoverable observer algebra
is quantum-like `M_N` or classical-like `C^N`.

## Theorem Stack

| Layer | Status | Finite statement |
| --- | --- | --- |
| Screen-shadow no-go | exact finite theorem/certificate | Screen entropy, diagonal correlator, horizon overlap, and restricted transfer shadows can agree while bridge algebras differ. |
| Physical regulator replacement | bounded certificate | Fuzzy-sphere/static-patch Schur channels are CPTP/unital and preserve the `M_N` vs `C^N` distinction. |
| Derived finite dynamics | exact finite construction | A cutoff Hamiltonian plus finite environment phase-kick trace derives a random-unitary regulator. |
| Regulator-class stability | bounded certificate | A declared class of positive-definite Schur regulators preserves the screen-shadow no-go under bounded perturbations. |
| Axiomatic selection | finite axiom audit | Static-patch-looking axioms select the regulator class only if vanishing cutoff continuity is included. |
| KMS insufficiency | exact finite no-go | KMS/detailed balance alone allows stationary modular twirling, a CPTP/unital complete-dephasing counterexample. |
| Physical continuity gate | finite theorem gate | Short-time modular locality, fuzzy-sphere heat scaling, or shrinking Euclidean cap thickness imply approximate identity. |
| Strong-continuity theorem gate | finite semigroup theorem | If `Lambda_L(delta)=exp(delta G_L)` and `delta_L Gamma_L -> 0`, then `||Lambda_L(delta_L)-id|| <= exp(delta_L Gamma_L)-1 -> 0`. |

## What Goal 31 Adds

Goal 31 turns the formerly named assumption `modular_time_approximate_identity`
into a standard finite semigroup condition:

```text
cutoff_compatible_strong_continuity:
  identity-starting finite dynamics with generator norm Gamma_L and
  lapse delta_L satisfying delta_L Gamma_L -> 0.
```

This excludes Goal 29's stationary modular twirl because the twirl is not an
identity-starting strongly continuous finite-time dynamics; it jumps by norm
one on a matrix-unit coherence witness. It also excludes fixed-lapse
thermalization as a sufficient principle, because strong continuity at each
cutoff does not imply a vanishing large-cutoff error unless the physical lapse
shrinks against the generator norm.

## What Is Not Claimed

The finite theorem does not prove that a continuum static patch, dS/CFT screen
map, Euclidean path integral, or Type-II/Type-III observer algebra satisfies
`cutoff_compatible_strong_continuity`. It isolates that as the next physics
question. The result is therefore a theorem-shaped finite benchmark, not a
continuum quantum-gravity theorem.

## Scientific Interpretation

The finite program shows that entropy-like screen data are too coarse to
determine observer bridge algebra, while abrupt dephasing is too permissive to
count as a physically controlled static-patch limit. The useful replacement is
not "assume off-diagonals survive," but "assume finite static-patch dynamics
starts at the identity and has cutoff-compatible generator/lapse scaling."
That is a natural, anti-tautological condition a continuum construction could
try to derive or refute.

## Open Frontier

The next physics-loaded question is whether `cutoff_compatible_strong_continuity`
follows from a controlled continuum static-patch modular/thermal dynamics,
Euclidean cap/path-integral construction, or Type-II/Type-III observer-algebra
limit. If it does, the finite benchmark has a plausible continuum promotion
route. If it does not, the benchmark identifies precisely where the finite
bridge theorem requires a new physical axiom.

## Reproducibility

| Claim | Certificate command |
| --- | --- |
| Conditional dS ER=EPR theorem ledger | `PYTHONPATH=. python3 -m qgtoy conditional-ds-er-epr --max-cutoff 5 --screen-probability 0.75 --low-order 2` |
| Static-patch kernel CP preflight | `PYTHONPATH=. python3 -m qgtoy static-patch-kernel-audit --max-cutoff 6` |
| Physical static-patch kernel | `PYTHONPATH=. python3 -m qgtoy physical-static-patch-kernel --max-cutoff 5 --noise-strength 1.0 --screen-probability 0.75 --low-order 2` |
| Derived finite static-patch dynamics | `PYTHONPATH=. python3 -m qgtoy derived-static-patch-dynamics --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --screen-probability 0.75 --low-order 2` |
| Regulator-class stability | `PYTHONPATH=. python3 -m qgtoy static-patch-regulator-universality --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Axiomatic static-patch selection | `PYTHONPATH=. python3 -m qgtoy axiomatic-static-patch-selection --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| KMS insufficiency and localized modular-time sufficiency | `PYTHONPATH=. python3 -m qgtoy modular-kms-continuity --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Physical continuity gate | `PYTHONPATH=. python3 -m qgtoy static-patch-physical-continuity --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Strong-continuity theorem gate | `PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
