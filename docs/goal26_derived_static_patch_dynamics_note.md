# Goal 26: Derived Static-Patch Kernel From Finite Dynamics

Goal 26 replaces the Goal 25 motivated Lindblad kernel with an explicit finite
dynamics derivation. The successful candidate is a static-patch Hamiltonian plus
finite environment trace.

## Finite Dynamics

For cutoff `L`, use spherical modes `(ell,m)` and the finite Hamiltonian

```text
H_L |ell,m> = E_L(ell,m) |ell,m>
E_L(ell,m) = [ell(ell+1) + delta_L m]/(L+1)^2.
```

The `ell(ell+1)` part is the fuzzy-sphere/spherical-harmonic Laplacian
spectrum. The small axisymmetric `m` split is the same finite regulator used in
Goal 25 to make the port labels distinguishable.

The environment is `q` independent Rademacher phase kicks. For signs
`z_r in {+1,-1}` and

```text
lambda_L = sqrt(noise_strength / (q (L+1)^2)),
```

define

```text
U_z = exp[-i H_L sum_r lambda_L z_r],
Phi_L(rho) = E_z[ U_z rho U_z^dagger ].
```

This is an explicit finite environment trace over `2^q` random-unitary branches.
On matrix units:

```text
E_ij -> cos(lambda_L (E_i-E_j))^q E_ij.
```

The classical control is also derived by a finite Stinespring map:

```text
V|i> = |i>_system |i>_environment,
```

followed by tracing the environment, giving complete dephasing onto `C^N`.

## Certified Properties

For every checked cutoff `1 <= L <= 5` with `q=4`:

- the quantum channel is CP, trace preserving, and unital because it is a finite
  convex average of unitary conjugations;
- the classical control is CP, trace preserving, and unital because it is a
  finite Stinespring dephasing channel;
- the small-angle condition is certified;
- the cutoff-error bound decreases:

```text
1 - cos(lambda_L max_gap)^q <= 0.5 noise_strength max_gap^2/(L+1)^2.
```

The finite phase-kick kernel approximates the Goal 25 Gaussian/Lindblad kernel
in the many-kick small-angle limit:

```text
cos(lambda_L DeltaE)^q -> exp[-noise_strength DeltaE^2/(2(L+1)^2)].
```

## No-Go Preserved

The derived quantum channel and the classical control agree on:

- screen entropy shadows;
- low-order diagonal correlator shadows;
- horizon-overlap data;
- screen-restricted transfer data.

But their induced recoverable bridge algebras differ:

```text
derived quantum channel: M_N
classical dephased control: C^N
```

Off-diagonal response separates them.

## Candidate Atlas

| Candidate | Status |
| --- | --- |
| static-patch Hamiltonian plus finite environment trace | success: derived finite dynamics |
| Goal 25 Gaussian/Lindblad kernel | recovered as many-kick limit, not finite-environment exact |
| Euclidean heat screen transfer without dilation | rejected without a TP/unital channel completion |
| modular-flow unitary only | partial success: no environment trace or dephasing scaling |

## Claim Boundary

This is a finite derived dynamics model. It is not a continuum de Sitter
static-patch path integral, not a dS/CFT screen dictionary, and not a literal
ER=EPR theorem in de Sitter. The next obstruction is deriving the finite
Hamiltonian/environment coupling from actual static-patch physics.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 26 certificate | `PYTHONPATH=. python3 -m qgtoy derived-static-patch-dynamics --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --screen-probability 0.75 --low-order 2` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_derived_static_patch_dynamics` |
| JSON certificate index validation | `python3 -m json.tool docs/goal26_derived_static_patch_dynamics_certificate_index.json` |
