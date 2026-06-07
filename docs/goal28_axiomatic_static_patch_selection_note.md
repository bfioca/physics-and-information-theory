# Goal 28: Axiomatic Static-Patch Regulator Selection

Goal 28 replaces Goal 27's declared regulator class with a finite selection
rule. The point is not to add more kernels. The point is to ask which
static-patch-looking axioms select the class without mentioning the desired
bridge result.

## Selection Axioms

For cutoff `L`, use fuzzy-sphere/spherical-harmonic modes `(ell,m)` and a
finite static-patch Hamiltonian with controlled axis breaking. A regulator is
selected when it satisfies:

- fuzzy-sphere covariance or controlled axis breaking;
- energy-difference static-patch Schur form `K_ij = phi_L(E_i-E_j)`;
- CP/TP/unital diagonal screen preservation;
- KMS/modular or heat-kernel balance;
- finite Stinespring or time-average dilation;
- locality/spectral-gap scaling;
- vanishing cutoff-error continuity;
- an anti-tautology rule: the axioms may not mention bridge algebra,
  `M_N`, `C^N`, off-diagonal response, or response gaps.

These axioms select the four implemented Goal 27 regulator subclasses:

| Selected primitive | Goal 27 regulator |
| --- | --- |
| Gaussian fuzzy heat time average | `fuzzy_laplacian_lindblad_heat` |
| finite Rademacher phase-kick time average | `finite_environment_phase_kick_trace` |
| KMS/Cauchy modular time average | `kms_modular_cauchy_average` |
| Euclidean cap energy-difference completion | `euclidean_cap_schur_completion` |

## Theorem-Style Claim

Any finite regulator satisfying the axioms is a positive-definite
energy-difference Schur channel with unit diagonal. Therefore it is CP, trace
preserving, and unital; it preserves the diagonal screen algebra; and the
quantum regulator and complete-dephasing control agree on screen entropy,
low-order diagonal correlators, horizon-overlap data, and screen-restricted
transfer data.

The vanishing cutoff-continuity axiom plus bounded static-patch gaps implies
nonzero off-diagonal retention in the certified finite family. That derived
off-diagonal retention separates the benchmark bridge algebra:

```text
selected quantum regulator: M_N
complete-dephasing control: C^N
```

The bridge distinction is a consequence, not an axiom.

## Weakest Missing Axiom

The audit identifies the main missing axiom:

```text
vanishing_cutoff_error_continuity
```

Without it, instant total dephasing satisfies the other static-patch/channel
requirements but destroys the quantum observer channel. Thus CP/TP/unitality,
covariance, and screen preservation alone are not enough.

Other rejected candidates:

- raw Euclidean heat transfer fails normalized CP/TP/unital diagonal screen
  preservation as a bridge channel;
- screen-only dS/CFT-like maps lack an observer-channel completion;
- response-oracle kernels fail the anti-tautology gate.

## Bounded Evidence

For `1 <= L <= 5`, the selected regulators preserve:

- CPTP/unitality;
- screen-shadow collisions;
- nonzero intrinsic off-diagonal response;
- `M_N` versus `C^N` bridge-algebra separation;
- stability under spectrum, coupling, KMS/temperature, and cutoff-geometry
  perturbations of radius `0.05`.

## Claim Boundary

This is finite axiomatic regulator selection. It is not a continuum de Sitter
static-patch derivation, not a dS/CFT dictionary, and not literal de Sitter
ER=EPR.

The next physics gap is to derive these axioms from continuum static-patch
gravity, observer modular structure, a path integral, or a dS/CFT screen
dictionary.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 28 certificate | `PYTHONPATH=. python3 -m qgtoy axiomatic-static-patch-selection --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_axiomatic_static_patch_selection` |
| JSON certificate index validation | `python3 -m json.tool docs/goal28_axiomatic_static_patch_selection_certificate_index.json` |
