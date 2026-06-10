# Constraint-Derived Relational Fuzzy-Horizon Observer

Status: finite constraint model, continuum Type-I limit, and edge-resolution
no-go implemented

## Why This Model

The coherent POVM is canonical, but a measurement choice is not yet an
observer algebra derived from constraints. This model introduces explicit time
and angular reference systems and asks which Dirac observables remain available
when those references are inaccessible.

This is a parametrized fuzzy one-particle surrogate. It is not derived from the
Einstein constraint or a de Sitter path integral.

## Physical Hilbert Space And Constraints

Use the harmonic GNS space

```text
H_L = L^2(M_{L+1},tau_L)
    = direct_sum_{ell=0}^L V_ell,
```

with basis `|ell,m>`. The system energy is the fuzzy Laplacian
`K_L=ell(ell+1)` and the axial charge is `m`. Add a time reference carrying
momentum `-ell(ell+1)` and an angular edge reference carrying charge `-m`.
The commuting constraints are

```text
C_t   = K_L + P_t   = 0,
C_phi = J_z + P_phi = 0.
```

The physical basis is

```text
|ell,m>_S |ell>_t |m>_phi.
```

Dressed matrix units that update all three factors commute with both
constraints and compress to all matrix units on the physical space.

## Derived Algebra Hierarchy

The accessible algebra depends on which references are retained:

```text
full relational observer:       M_{(L+1)^2},
time reference inaccessible:    direct_sum_{ell=0}^L M_{2ell+1},
time and edge inaccessible:     C^{(L+1)^2}.
```

The canonical conditional expectations are

```text
E_t(X)       = sum_ell P_ell X P_ell,
E_{t,phi}(X) = sum_{ell,m} P_{ell,m} X P_{ell,m}.
```

Therefore a Hamiltonian constraint alone does not derive the diagonal screen.
Diagonalization additionally assumes an inaccessible angular edge reference or
an axial-charge superselection rule. The number of within-energy-block
coherences discarded by that extra step is

```text
sum_ell [(2ell+1)^2-(2ell+1)]
  = L(L+1)(4L+5)/3
  = (4/3)L^3 + O(L^2).
```

This is the model's axial-edge correction to a screen-only dictionary.
Equivalently, the diagonal screen retains the fraction

```text
dim(C^{(L+1)^2}) / dim(direct_sum_ell M_{2ell+1})
  = 3(L+1)/(4L^2+8L+3)
  = 3/(4L) + O(L^-2).
```

Thus the extra edge-reference restriction discards an asymptotically complete
fraction of the time-constraint observer algebra, even though both algebras
share the same diagonal populations.

## Quantitative Recovery No-Go

Inside one `ell` block, take the orthogonal states

```text
|psi_+/- > = (|ell,-ell> +/- |ell,ell>)/sqrt(2).
```

`E_t` preserves them, whereas `E_{t,phi}` maps both to the same mixture. Any
decoder factored through the diagonal screen has worst-case trace-distance
error at least `1/2`. If the two screen outputs are only known to be within
trace distance `epsilon`, the lower bound is

```text
(1-epsilon)/2.
```

This is an operational obstruction between two constraint-derived observer
algebras, rather than a collision created by declaring a diagonal channel at
the outset.

## Edge-Reference Resolution Law

Let angular-reference uncertainty be Gaussian with width `sigma`. A magnetic
coherence with gap `Delta m` is attenuated by

```text
exp[-sigma^2 (Delta m)^2/2].
```

For the extremal coherence `m=-L` to `m=L`, the visibility is

```text
v_L = exp[-2 sigma^2 L^2].
```

The two smeared phase states have trace distance exactly `v_L`. Therefore any
decoder from the smeared edge record has worst-case reconstruction error

```text
eta_L >= (1-v_L)/2
      = (1-exp[-2 sigma^2 L^2])/2.
```

At every fixed `sigma>0`, this lower bound tends to `1/2`.

Retaining fixed visibility `v` therefore requires

```text
sigma_L <= sqrt(log(1/v)/2)/L.
```

Any fixed nonzero angular uncertainty loses extremal horizon coherence in the
large-cutoff limit. The bare `1/L` law is standard `U(1)` Fourier resolution;
the research candidate is its conjunction with the vanishing retained-algebra
fraction and the minimax recovery obstruction in this fuzzy-horizon regulator.

## Symmetry And Robustness Boundary

The reference above is an axial `U(1)` phase reference, not a complete
orientation frame. Hiding a full `SU(2)` frame in the multiplicity-one harmonic
space retains only one scalar per `ell` block:

```text
(direct_sum_ell M_{2ell+1})^{SU(2)} = C^{L+1}.
```

Its retained fraction is `3/(4L^2+8L+3)`, asymptotic to `3/(4L^2)`. The axial
`3/(4L)` scaling must not be presented as a full-rotation result.

The time/edge distinction also requires protected magnetic degeneracy. Under
the irrational Zeeman perturbation

```text
H_delta=K_L+delta J_z,
```

the spectrum is nondegenerate and infinite-time averaging becomes diagonal for
every nonzero `delta`. At finite observation time `T`, the extremal phase-pair
visibility is exactly `|sinc(delta L T)|`. Thus the operational result survives
only while `|delta|LT` is small, unless rotational symmetry protects the
within-`ell` degeneracy. The full audit is in
`docs/edge_symmetry_robustness.md`.

## Controlled Limit

The harmonic inclusion `|ell,m>_L -> |ell,m>_M` preserves both constraint
charges and heat dynamics exactly on finite harmonic support. The limits are

```text
full corner:  K(l2{ell,m}), strong closure B(l2), Type I_infinity,
time blind:   product_ell M_{2ell+1}, atomic Type I,
diagonal:     l_infinity{ell,m}, abelian.
```

This is a rigorous continuum result and also a no-go: the one-particle
constraint model cannot produce the gravitational Type-II observer algebra.
A Type-II claim needs a regulated many-body or local-QFT algebra, a physical
clock/crossed product, and a derived trace.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy relational-observer-constraint --max-level 8
PYTHONPATH=. python3 -m unittest tests.test_relational_observer
```
