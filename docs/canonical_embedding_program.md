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

## Finite Repair: Consecutive UCP Refinement

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

## Candidate Embedding Table

| Candidate | Status | Role |
| --- | --- | --- |
| Rank-ordered factorial `*-inclusion` | implemented baseline | Gives UHF/Type-II candidate scaffold, but uses a noncanonical cofinal subsequence. |
| Trace-filled UCP consecutive refinement | implemented in this audit | Works at consecutive cutoffs; unital, CP, trace-preserving, approximately multiplicative. |
| Spherical-harmonic projection/refinement | program target | Should test mode-label preservation, screen shadows, continuity, and response persistence. |
| Berezin-Toeplitz fuzzy-sphere channel | program target | More physically natural route through symbol/quantization maps and approximate multiplicativity. |

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
