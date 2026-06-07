# Goal 29: Continuity From Static-Patch Modular/KMS Structure

Goal 29 tests the load-bearing axiom from Goal 28:

```text
vanishing_cutoff_error_continuity
```

The result is two-sided. Finite KMS/detailed-balance modular structure alone
does **not** force continuity. KMS plus a modular-time approximate-identity
condition does.

## Finite Modular/KMS Models

Let `sigma_t(A)=e^{-itH_L} A e^{itH_L}` be finite static-patch modular flow.
The selected models are modular-time averages:

```text
Phi_L(A) = integral sigma_t(A) dmu_L(t)
```

On matrix units, this gives an energy-difference Schur channel:

```text
E_ij -> hat(mu_L)(E_i-E_j) E_ij.
```

The certificate includes four localized modular/KMS models:

| Model | Regulator |
| --- | --- |
| Gaussian modular heat average | `fuzzy_laplacian_lindblad_heat` |
| finite Rademacher modular phase kicks | `finite_environment_phase_kick_trace` |
| Cauchy KMS modular time jitter | `kms_modular_cauchy_average` |
| Euclidean Brownian cap modular average | `euclidean_cap_schur_completion` |

Each is CP/TP/unital because it is a modular-time probability average of
unitary conjugations, or a finite approximation to one. Each is KMS detailed
balanced because the characteristic function is real and even, so the Schur
channel is self-adjoint in the finite Gibbs/KMS inner product.

## Positive Direction

If the modular-time measures `mu_L` form an approximate identity near `t=0`
on bounded cutoff energy gaps, then:

- the channel preserves diagonal screen data;
- the off-diagonal cutoff error vanishes;
- nonzero off-diagonal response survives at finite cutoff;
- the Goal 28 `M_N` versus `C^N` bridge distinction is preserved.

For `1 <= L <= 5`, the certificate verifies this for all four selected models
and for the existing perturbation variants.

## Negative Direction

KMS/detailed balance alone is insufficient. The stationary modular twirl is:

- CP/TP/unital;
- diagonal screen preserving;
- modular-flow covariant;
- KMS self-adjoint.

But it is not localized near `t=0`; it is complete dephasing. It therefore
fails the Goal 28 continuity axiom.

A fixed-width modular noise model gives the same lesson: detailed balance can
hold while the cutoff-error bound does not vanish.

## Weakest Additional Assumption

The required extra assumption is:

```text
modular_time_approximate_identity
```

Equivalently, the modular-time averaging measures must converge to `delta_0`
uniformly on bounded cutoff energy gaps. The implemented finite models certify
this by shrinking Gaussian/Rademacher/Brownian width or Cauchy scale.

## Claim Boundary

This is finite modular/KMS regulator selection only. It is not a continuum de
Sitter static-patch theorem, not a dS/CFT dictionary, and not literal de Sitter
ER=EPR.

The next gap is deriving the modular-time approximate-identity condition from
actual continuum static-patch physics.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 29 certificate | `PYTHONPATH=. python3 -m qgtoy modular-kms-continuity --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_modular_kms_continuity` |
| JSON certificate index validation | `python3 -m json.tool docs/goal29_modular_kms_continuity_certificate_index.json` |
