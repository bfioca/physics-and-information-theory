# Finite-to-Type-II Static-Patch Observer Algebra

## Claim Boundary

This is a finite-to-operator-algebra theorem candidate, not a continuum de
Sitter theorem, not a dS/CFT construction, and not literal ER=EPR. The result
constructs an explicit large-cutoff algebraic limit after adding a cofinal
inclusion choice, and it identifies the remaining modular/static-patch
dynamics assumption.

## Main Result

The raw consecutive static-patch cutoffs have

```text
N_L=(L+1)^2.
```

A unital full-matrix inclusion `M_n -> M_m` exists only when `n` divides `m`.
Since `(L+1)^2` does not divide `(L+2)^2` for `L >= 1`, the consecutive
cutoffs do not form a unital trace-preserving matrix-algebra inductive system.

The repair is a cofinal factorial cutoff subsequence

```text
L_k=(k+1)!-1,    N_k=((k+1)!)^2,
```

for which `N_k` divides `N_{k+1}` with multiplicity `(k+2)^2`. This gives
trace-preserving inclusions

```text
M_{N_k} -> M_{N_{k+1}},        x -> x tensor I_{(k+2)^2},
C^{N_k} -> C^{N_{k+1}},        each atom splits into (k+2)^2 equal atoms.
```

## Limit Split

The quantum finite system is a UHF inductive limit. With the normalized trace,
its tracial GNS von Neumann closure is the hyperfinite Type `II_1` factor
under the standard UHF/trace-closure theorem.

The dephased control uses the same diagonal screen inclusions and trace data
but keeps only the abelian diagonal algebra. Its limit is an abelian AF algebra
whose tracial von Neumann closure is diffuse abelian. Thus the two sequences
share screen shadows levelwise while differing in the limiting observer
algebra.

The persistent noncommutative witness is the embedded matrix-unit corner:

```text
[e_12,e_21]=e_11-e_22.
```

Under trace-preserving amplification this witness keeps operator norm `1`,
while the dephased control has zero commutator.

## Remaining Assumption

The algebraic inclusions alone do not prove convergence of the finite
static-patch Hamiltonians, modular/KMS semigroups, or Euclidean transfer maps.
The remaining required assumption is:

```text
inclusion_covariant_static_patch_generators
```

meaning the Hamiltonians or semigroup generators must be compatible with the
chosen cutoff embeddings up to vanishing error. This is the next physics
question, not something the current finite certificate claims to derive.

## Harlow-Facing Summary

The raw finite static-patch regulator ladder does not automatically define a
matrix-algebra limit; consecutive cutoffs fail the divisibility condition.
However, a cofinal factorial cutoff subsequence gives trace-preserving matrix
and diagonal inclusions. The quantum path has a hyperfinite Type `II_1`
candidate limit, while the dephased path has identical screen-shadow data and
an abelian limit. The missing datum is not entropy but inclusion-compatible
operator dynamics.

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

Run the focused regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_typeii_static_patch_limit
```

Validate the machine-readable index:

```bash
python3 -m json.tool docs/major_goal_finite_to_typeii_static_patch_observer_algebra_certificate_index.json
```
