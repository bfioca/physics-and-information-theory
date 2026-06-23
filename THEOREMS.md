# Theorem and Evidence Index

The authoritative statements and proofs are in
[`paper/local_scalar_observer_cost/main.pdf`](paper/local_scalar_observer_cost/main.pdf).

**Publication status:** internal four-gate pass; external proof and novelty
review remain open.

## Model

A finite pointer controls prescribed smooth compact scalar sources. Tracing a
purified thermal field gives the exact Schur channel

```text
|i><j| -> G_ij |i><j|,
|G_ij|=exp(-Gamma_ij),
Gamma_ij=<p_i-p_j,B_beta,L(p_i-p_j)>/4.
```

The resource is the centered post-switch field energy

```text
E_bar=sum_i w_i ||p_i-p_bar||^2/2.
```

It excludes the actuator, clock, battery, and material observer.

## T1. General Thermal Half-Line Optimum

For Dirichlet half-line momentum data supported in `[0,L]`,

```text
C_beta(L)
 :=sup <p,h^-1 coth(beta h/2)p>/(||p||^2/2)
 =2 L Lambda(pi L/beta),
```

where `Lambda(tau)` is the simple largest eigenvalue of

```text
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

The normalized optimizer is unique up to sign and strictly positive. Global
two-sided bounds and uniform small- and large-support remainders are proved.

## T2. Conformal de Sitter All-Sector Optimum

At `beta=2 pi R`, let `y=L/R`. For arbitrary angular and canonical final
data supported in `[0,L]`,

```text
C_opt(y)=2y Lambda(y/2).
```

The unique optimum is the s-wave momentum eigenfunction. Higher angular
sectors are strictly dominated by resolvent order, and coordinate data are
strictly dominated by the momentum lower envelope.

## T3. Finite-Pointer Purity and Renyi Bound

Let `P_cl=sum_i w_i^2`. Then

```text
Tr(rho_P^2)
 >= P_cl+(1-P_cl)
    exp[-C_beta(L)E_bar/(1-P_cl)],

S_2(rho_P)<=min{H_2(w),C_beta(L)E_bar}.
```

The symmetric binary top-mode record saturates the bound. Global sharpness for
arbitrary pointer dimension is not asserted.

## T4. Observer-Code Insertion

For the purified physical record and an orthogonal CRT-real matter pair in the
Harlow-Usatyuk-Zhao simple random code,

```text
E_O |<phi|Vhat^dagger Vhat|psi>|^2
 = D/(D+2) Tr(rho_P^2).
```

T3 therefore supplies a physical energy-support lower floor on this
Haar-averaged squared fluctuation. The result is not deterministic for every
fixed code and is not uniform over matter states.

## T5. Smooth Source Realization

Smooth compact conditional data are dense in the finite-energy closure, their
pairwise thermal forms converge, and a cutoff homogeneous solution constructs
the corresponding prescribed sources. This proves finite-pointer source
closure at fixed final support, not controllability from every smaller fixed
source cylinder.

## T6. Branchwise Final-Slice Gravity

For spherical conditional `q_i=0` data, assume every branch obeys
`Q_b,i<=delta<1`. Then

```text
S_2(rho_P)
 <= delta (R^2/G)
    C_opt(y) tanh(y) sech(y)^2/2.
```

This is an exact composition with branchwise final-slice constraints. The
channel remains a fixed-background calculation, and no coupled evolution is
claimed.

## Evidence

| Layer | Authoritative artifact | Status |
| --- | --- | --- |
| Manuscript proof | [`main.pdf`](paper/local_scalar_observer_cost/main.pdf) | Internal pass |
| Finite-pointer proof note | [`finite_pointer_observer_entropy.md`](docs/finite_pointer_observer_entropy.md) | Four analytic gates pass |
| Localization clean-room audit | [`local_scalar_observer_proof_audit.md`](docs/local_scalar_observer_proof_audit.md) | Internal pass; external sign-off open |
| Finite-pointer certificate | [`finite_pointer_observer_certificate.json`](experiments/finite_pointer_observer_certificate.json) | Source-bound pass |
| Independent finite-pointer replay | [`finite_pointer_observer_clean_room_check.json`](experiments/finite_pointer_observer_clean_room_check.json) | 64-case pass; nonrigorous |
| Localization certificate | [`local_scalar_observer_cost_certificate.json`](experiments/local_scalar_observer_cost_certificate.json) | Source-bound pass |
| Numerical spectrum | [`observer_cost_spectrum.json`](paper/local_scalar_observer_cost/data/observer_cost_spectrum.json) | Convergence pass; nonrigorous |
| Package provenance | [`artifact_manifest.json`](paper/local_scalar_observer_cost/artifact_manifest.json) | Frozen package audit |

## Submission Rule

`SUBMIT` requires the detector/QFT, operator-theory, and observer-code gates
to pass and every central claim in the specialist response form to receive at
least one external `PASS` or `CORRECT`. A claim left `NOT REVIEWED` by
every reviewer remains open.
