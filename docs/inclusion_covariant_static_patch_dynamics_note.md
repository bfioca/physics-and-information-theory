# Inclusion-Covariant Dynamics for Finite-to-Type-II Static-Patch Regulators

## Claim Boundary

This is a finite/asymptotic theorem candidate for the Type-II scaffold. It does
not claim continuum de Sitter dynamics, dS/CFT, or literal ER=EPR.

## Result

The finite-to-Type-II audit left one load-bearing assumption:

```text
inclusion_covariant_static_patch_generators
```

For the factorial cutoff subsequence, the matrix inclusions are

```text
iota_k(x)=x tensor I_r.
```

If the static-patch Hamiltonian were exactly compatible with this inclusion,
we would have

```text
G_{k+1} iota_k = iota_k G_k.
```

The certificate finds a two-sided result:

1. Exact finite covariance fails for the raw fuzzy-sphere Hamiltonians under
   the rank-ordered block embedding.
2. The operator-norm, conditional-expectation, heat-generator, and short-time
   semigroup covariance errors decrease along the certified factorial
   subsequence.

Thus the current result is an asymptotic inclusion-covariant generator theorem
candidate, not an exact finite covariance theorem.

## Conditional Expectation Version

Let `E_k=id tensor tau_fiber` be the trace-preserving conditional expectation
from the amplified algebra back to the embedded source algebra. The audited
weaker condition is

```text
E_k G_{k+1} iota_k(x) ≈ G_k(x).
```

The conditional errors decrease in the bounded certificate. The dephased
screen control is exactly inclusion-covariant because equal atom splitting
preserves the diagonal trace data and all commutators vanish levelwise.

## Remaining Assumption

The additional finite assumption is now more concrete:

```text
rank_ordered_static_patch_embedding
```

The Type-II inclusion must be tied to cumulative spherical-mode ordering rather
than an arbitrary matrix-amplification basis. Under that embedding, normalized
static-patch energies are asymptotically compatible with the inclusion.

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

Run the focused regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_inclusion_covariant_dynamics
```

Validate the machine-readable index:

```bash
python3 -m json.tool docs/inclusion_covariant_static_patch_dynamics_certificate_index.json
```
