# Goal 25: Physical Static-Patch Kernel Search

Goal 25 replaces the hand-built distance Schur kernel with a physically
motivated finite cutoff candidate. The successful candidate is a
fuzzy-sphere/static-patch Hamiltonian dephasing channel.

## Kernel Candidate

For angular cutoff `L`, use spherical mode labels `(ell,m)` and
`N=(L+1)^2`. Define a finite Hamiltonian spectrum

```text
E_L(ell,m) = [ell(ell+1) + delta_L m] / (L+1)^2,
delta_L = 1/(2L+3).
```

The `ell(ell+1)` term is the fuzzy-sphere/spherical-harmonic Laplacian
spectrum. The small `m` split is a finite axisymmetric rotation/chemical
potential split; it removes degeneracy so the benchmark can test full
port-resolved `M_N` recovery. Without the split, the same construction gives a
noncommutative block algebra `direct_sum_ell M_{2ell+1}`, which the certificate
records as a partial success.

The quantum bridge channel is the Lindblad pure-dephasing semigroup

```text
L(rho) = -(1/2)[H_L,[H_L,rho]]
```

run for double-scaled time

```text
t_L = noise_strength/(L+1)^2.
```

On matrix units:

```text
E_ij -> exp[-t_L (E_i-E_j)^2 / 2] E_ij.
```

The classical control is complete dephasing onto the screen/horizon algebra
`C^N`.

## Certified Properties

The quantum and classical channels are finite-dimensional CPTP unital channels:

- CP follows from the Lindblad pure-dephasing generator, equivalently from the
  Gaussian difference kernel as a characteristic function;
- trace preservation and unitality follow from unit diagonal Schur
  coefficients;
- bounded Cholesky PSD checks are included as a numeric sanity check.

The cutoff error is

```text
epsilon_L = 1 - min_offdiag_retention
```

with bound

```text
epsilon_L <= 0.5 t_L max_gap_L^2.
```

Because `t_L = O((L+1)^-2)` and the normalized energy gap stays bounded, the
bound vanishes in the regulator limit.

## Result

For every checked cutoff `1 <= L <= 5`, the physical dephasing candidate and
the classical dephased control agree on:

- screen entropy shadows;
- low-order diagonal correlator shadows;
- horizon-overlap data;
- screen-restricted transfer data.

But the induced recoverable bridge algebras differ:

```text
physical quantum candidate: M_N
classical dephased control: C^N
```

Off-diagonal relative-entropy response separates them.

## Search Outcome

| Candidate | Status |
| --- | --- |
| fuzzy Laplacian Lindblad dephasing with axis split | success candidate |
| unsplit fuzzy Laplacian dephasing | partial success: noncommutative but not full port-resolved |
| screen heat attenuation without dilation | rejected as a bridge channel without a TP/unital completion |

## Claim Boundary

This is a physically motivated finite regulator, not a derivation from actual
de Sitter static-patch quantum gravity or a continuum dS/CFT dictionary. The
remaining obstruction is to derive the kernel from controlled static-patch
dynamics, a path integral, or a dS/CFT screen map.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 25 certificate | `PYTHONPATH=. python3 -m qgtoy physical-static-patch-kernel --max-cutoff 5 --noise-strength 1.0 --screen-probability 0.75 --low-order 2` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_physical_static_patch_kernel` |
| JSON certificate index validation | `python3 -m json.tool docs/goal25_physical_static_patch_kernel_certificate_index.json` |

## References

- Diffeomorphisms on the fuzzy sphere, PTEP 2020.
- Generators of Quantum Markov Semigroups, arXiv:1406.3417.
- Mathematical Models of Markovian Dephasing, arXiv:1811.11784.
