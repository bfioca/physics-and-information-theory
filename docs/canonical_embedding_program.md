# Approximate Static-Patch Cutoff Embeddings

## Claim Boundary

This note addresses a packaging/reviewer weakness in the finite-to-Type-II
static-patch scaffold. It does not construct a canonical continuum static patch.
It gives a finite audit showing that exact full-matrix inclusions are not the
only possible cutoff-refinement structure.

## Problem

The Type-II scaffold used a cofinal factorial subsequence because consecutive
spherical cutoffs

```text
N_L=(L+1)^2,    N_{L+1}=(L+2)^2
```

do not usually satisfy `N_L | N_{L+1}`. Thus exact unital full-matrix
`*-homomorphisms` `M_{N_L} -> M_{N_{L+1}}` fail at consecutive cutoffs.

That is mathematically clean but physically suspicious: a static-patch cutoff
should not need factorial jumps just to refine modes.

## Finite Repair 1: Consecutive UCP Refinement

For any `n <= m`, choose the standard isometry `V:C^n -> C^m` and define

```text
Phi(A) = V A V^* + tau_n(A)(I_m - V V^*).
```

This map is:

- unital;
- completely positive;
- normalized-trace preserving;
- defined for consecutive spherical cutoffs;
- not an exact `*-homomorphism` unless `m=n`.

For the matrix-unit witness `A=e_12`, `B=e_21`,

```text
Phi(AB)-Phi(A)Phi(B) = (1/n)(I_m - V V^*),
```

so the operator-norm multiplicativity error is exactly `1/n`. For
static-patch dimensions `n=(L+1)^2`, this tends to zero.

The embedded off-diagonal response witness survives:

```text
[e_12,e_21]=e_11-e_22
```

has operator norm `1` in the quantum corner, while the dephased control has
zero commutator.

## Finite Repair 2: Physically Motivated Cutoff Maps

The current audit also compares three more structured finite maps. These are
not claimed to be canonical static-patch embeddings, but they address the
weakest version of the critique: the obstruction no longer rests only on a
factorial subsequence or a bare trace-filled gadget.

### Harmonic Projection/Refinement

The spherical-harmonic labels with `ell <= L` are identified with the same
labels inside the `ell <= L+1` cutoff. The complement is trace-filled. This map
is UCP and normalized-trace preserving, preserves low-harmonic diagonal
observables exactly, has the same `1/N_L` matrix-unit multiplicativity
witness, and keeps the commutator response visible.

### Heat-Kernel Coarse Graining

Harmonic refinement is composed with a positive-definite heat-kernel Schur
channel whose coefficients depend on normalized Laplacian energy gaps. The map
is UCP and trace preserving, fixes diagonal screen data, and damps off-diagonal
response by a positive retention factor that tends to one under the declared
cutoff scaling.

### Berezin-Toeplitz-Inspired Smoothing

As a finite surrogate for symbol/quantization smoothing, harmonic trace-filled
refinement is mixed with a trace-to-uniform channel at `O(1/N)` weight. This
convex mixture is UCP and trace preserving. Exact screen preservation is not
claimed, but the screen-shadow perturbation and multiplicativity error bounds
vanish while commutator response persists.

## Candidate Embedding Table

| Candidate | Status | Role |
| --- | --- | --- |
| Rank-ordered factorial `*-inclusion` | implemented baseline | Gives UHF/Type-II candidate scaffold, but uses a noncanonical cofinal subsequence. |
| Trace-filled UCP consecutive refinement | implemented in this audit | Works at consecutive cutoffs; unital, CP, trace-preserving, approximately multiplicative. |
| Spherical-harmonic projection/refinement | implemented physical-motivation audit | Preserves mode labels and low-harmonic diagonal shadows across consecutive cutoffs. |
| Heat-kernel coarse graining | implemented physical-motivation audit | Adds positive-definite Laplacian damping while preserving diagonal screen data. |
| Berezin-Toeplitz-inspired smoothing | implemented surrogate, not canonical | Tests `O(1/N)` CP smoothing with vanishing screen error and persistent response. |

## Remaining Open Question

The audit is stronger than the trace-filled baseline, but it still does not
derive a canonical static-patch cutoff. The open question is:

```text
Are the continuum-lift obstruction and cutoff embedding/coarse-graining problem
meaningful ways to formalize the limitation of diagonal/screen-shadow data?
```

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-embedding-channels --max-cutoff 5
```

Run the focused regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_embedding_channels
```

Validate the machine-readable index:

```bash
python3 -m json.tool docs/static_patch_embedding_channels_certificate_index.json
```
