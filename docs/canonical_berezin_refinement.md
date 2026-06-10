# Canonical Berezin Refinement Between Fuzzy-Sphere Cutoffs

Status: UCP low-mode refinement theorem implemented

## Canonical Map

For `1 <= L <= M`, define

```text
J_{L->M}(A)
  = (M+1) integral <n,L|A|n,L> |n,M><n,M| dOmega/(4 pi).
```

This is coherent-state symbol at level `L`, followed by coherent-state
quantization at level `M`. It is canonical for the chosen `SU(2)` coherent-state
regulator, unital, completely positive, normalized-trace preserving, adjoint
preserving, and `SU(2)` equivariant. Unlike the earlier trace-filled matrix
map, it is not selected by a matrix corner or a divisibility convention.

The associated Schrödinger map

```text
S_{L->M}(rho) = (L+1)/(M+1) J_{L->M}(rho)
```

is completely positive and ordinary-trace preserving. Its Heisenberg adjoint
`C_{M->L}` is unital, and the implementation verifies

```text
Tr[S_{L->M}(rho) B] = Tr[rho C_{M->L}(B)].
```

## Exact Harmonic Formula

Let `T^L_{ell,m}` be normalized fuzzy harmonics and set

```text
b_{L,ell}
  = L!(L+1)! / ((L-ell)!(L+ell+1)!)
  = product_{r=0}^{ell-1} (L-r)/(L+r+2).
```

Then

```text
J_{L->M}(T^L_{ell,m})
  = sqrt(b_{L,ell} b_{M,ell}) T^M_{ell,m}.
```

The elementary product estimate

```text
1-b_{L,ell} <= ell(ell+1)/(L+2)
```

implies convergence to the mode-matched identity for every fixed angular
momentum sector when both source and target cutoffs grow. Holding `L` fixed and
sending only `M` to infinity leaves the source smoothing factor
`sqrt(b_{L,ell})`. The code checks the multiplier and absence of harmonic
leakage directly from coherent-state quadrature.

## Dynamics And Composition

Because the map preserves `(ell,m)` and the fuzzy Laplacian eigenvalue is
`ell(ell+1)`, it exactly intertwines both the Laplacian and heat semigroup:

```text
Delta_M J_{L->M} = J_{L->M} Delta_L,
P_t^M J_{L->M} = J_{L->M} P_t^L.
```

The maps are not exactly functorial. On a normalized harmonic,

```text
||J_{M->N}J_{L->M}-J_{L->N}||_2
  = sqrt(b_{L,ell}b_{N,ell}) (1-b_{M,ell})
  <= ell(ell+1)/(M+2).
```

Thus their cutoff-composition defect vanishes at fixed `ell` with an explicit
inverse-cutoff rate. More generally, the bounds are uniform for all
`ell <= K_L` whenever

```text
K_L^2/L -> 0.
```

This supplies a controlled slowly growing low-energy domain, not only a finite
list of selected harmonics.

## Claim Boundary

### Uniform product theorem

Let `X_i^L=J_i/sqrt(j(j+1))` and consider

```text
A=a_0 I+sum_i a_i X_i^L,  sum_i |a_i| <= 1,
B=b_0 I+sum_i b_i X_i^L,  sum_i |b_i| <= 1.
```

For adjacent cutoffs and every `L>=2`, direct decomposition into spin zero,
one, and two sectors gives

```text
||J_{L->L+1}(AB)-J_{L->L+1}(A)J_{L->L+1}(B)||_op
  <= 8/[3(L+2)].
```

This is uniform over the entire declared coefficient-atomic unit ball, rather
than a selected matrix-unit calculation. Scalar-vector terms cancel exactly.

### Necessary low-mode restriction

The restriction cannot be removed. A highest-mode partial isometry of operator
norm one gives the explicit lower bound

```text
(M+1)/(L+M+1)
 - b_{L,L}b_{M,L}(M+1)/(L+1)
```

on the full operator-unit-ball multiplicativity defect. For `M=L+1` this tends
to `1/2`. Thus the coherent Berezin maps are not full-algebra asymptotic
morphisms even though they form a controlled low-mode transfer system.

Together, these results prove canonical UCP refinement, state compatibility,
exact generator covariance, coherent cutoff composition, and a uniform product
theorem on the physical coordinate operator system. Standard compact-Kahler
Berezin-Toeplitz product asymptotics extend convergence to every fixed smooth
harmonic cutoff, but an explicit growing-`K_L` product rate still requires
uniform derivative or `6j`-symbol estimates.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy fuzzy-berezin-refinement --max-source-level 5
PYTHONPATH=. python3 -m unittest tests.test_fuzzy_berezin
```
