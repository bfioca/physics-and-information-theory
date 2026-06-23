# Theorem and Evidence Index

This index summarizes the current manuscript. The authoritative statements and
proofs are in
[`paper/local_scalar_observer_cost/main.pdf`](paper/local_scalar_observer_cost/main.pdf).

**Publication status:** internal pass; external proof and two-domain novelty
review open.

## Model

A degenerate pointer qubit couples through `Z_P` to a prescribed smooth compact
source for a conformally coupled massless scalar. After switching, the exact
quasifree channel has

```text
|kappa|=exp(-Gamma),
epsilon_obs=(1/2)||D_kappa-D_0||_diamond=exp(-Gamma)/2.
```

The resource is the post-switch scalar-field Killing energy `E_K`. It excludes
the actuator, clock, battery, and material probe.

## T1. General Thermal Half-Line Optimum

For Dirichlet half-line momentum data supported in `[0,L]`,

```text
C_beta(L):=sup Gamma/E=2 L Lambda(pi L/beta),
```

where `Lambda(tau)` is the simple largest eigenvalue of

```text
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

The normalized optimizer is unique up to sign and strictly positive. The
manuscript also gives global two-sided bounds and the uniform remainders

```text
0 <= C_beta(L)-2L Lambda(0) <= 2 pi L^3/(3 beta^2),
0 <= C_beta(L)-16L^2/(beta pi^2) <= beta/3.
```

## T2. Conformal de Sitter All-Sector Optimum

At `beta=2 pi R`, let `y=L/R`. For arbitrary angular and canonical final data
supported in `[0,L]`,

```text
C_opt(y)=sup Gamma/(E_K R)=2y Lambda(y/2).
```

The unique optimum is the s-wave momentum eigenfunction. Higher angular
sectors are strictly dominated by resolvent order; coordinate data are
strictly dominated by overlapping vacuum and thermal momentum lower bounds.

The large-support remainder becomes

```text
0 <= C_opt(y)-8y^2/pi^3 <= 2pi/3.
```

## T3. Smooth Final-Data Realization

Smooth compact radial momentum data are dense in the finite-energy optimizer
closure, and their thermal forms converge. A cutoff homogeneous solution
constructs a prescribed smooth compact source for each strict interior
approximant.

This proves sharpness at fixed final Cauchy support. It does not prove
controllability from every strictly smaller fixed source cylinder.

## T4. Causal Source Envelope

If a source is supported within areal radius `a<R` for duration `T`, finite
propagation gives final optical support

```text
L=R atanh(a/R)+T.
```

The sharp final-support coefficient therefore supplies an upper envelope for
the source cylinder, without asserting that its optimizer is reachable from
that cylinder.

## T5. Final-Slice Gravity Application

For spherical flux-free final data with `q=0` and `K_ij=0`, the scalar
constraint mass equals the fixed-background field energy. This is an exact
final-slice constraint statement, not a channel on the perturbed geometry or a
coupled evolution theorem.

## Evidence

| Layer | Authoritative artifact | Status |
| --- | --- | --- |
| Manuscript proof | [`main.pdf`](paper/local_scalar_observer_cost/main.pdf) | Internal pass |
| Adversarial proof audit | [`local_scalar_observer_proof_audit.md`](docs/local_scalar_observer_proof_audit.md) | Internal pass; external sign-off open |
| Executable certificate | [`local_scalar_observer_cost_certificate.json`](experiments/local_scalar_observer_cost_certificate.json) | Source-bound pass |
| Numerical illustration | [`observer_cost_spectrum.json`](paper/local_scalar_observer_cost/data/observer_cost_spectrum.json) | Convergence pass; nonrigorous |
| Package provenance | [`artifact_manifest.json`](paper/local_scalar_observer_cost/artifact_manifest.json) | 25 files verified |
| Novelty boundary | [`PRIORITY_AUDIT.md`](paper/local_scalar_observer_cost/PRIORITY_AUDIT.md) | External gate open |

## Submission Rule

`SUBMIT` requires both domain novelty gates to pass and every central claim in
the specialist response form to receive at least one external `PASS` or
`CORRECT`. `NOT REVIEWED` by every reviewer leaves the claim open.
