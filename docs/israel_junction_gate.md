# Tensorial Israel Junction Gate

## Result

The moving-membrane stress and static `ell=2` master transmission calculations
now have an explicit promotion gate to self-consistent gravity.  For

```text
ds^2=-A(r)dt^2+dr^2/B(r)+r^2dOmega^2
```

use one normal directed from the inner region to the outer region.  The
principal mixed extrinsic curvatures of a static spherical worldtube are

```text
K_t^t=sqrt(B) A'/(2A),       K_theta^theta=sqrt(B)/a.
```

With `[K_i^j]-delta_i^j[K]=-kappa S_i^j` and a Nambu-Goto surface stress
`S_i^j=-sigma delta_i^j`, the two independent Israel equations reduce exactly
to

```text
[K_t^t]=[K_theta^theta]=-kappa sigma/2.                 (1)
```

Consequently, identical de Sitter geometry on both sides has zero
extrinsic-curvature jump and cannot support any `sigma>0`.  At the default
dimensionless wall values the exact reduced mismatch is
`kappa sigma/2=0.0009658898235` when `kappa=1`.

This is a limitation of the present *exact-background interpretation*, not a
refutation of its first-order sourced response.  A shell stress placed on de
Sitter can generate the required `O(kappa sigma)` metric jump in linearized
gravity.  What is forbidden is calling the uncorrected identical geometry on
both sides an already Israel-matched background.

## Exact Benchmark

The audit includes a nontrivial self-consistent test.  Join regular de Sitter
inside to Kottler outside with the same cosmological radius.  Let
`u=a^2/R^2`.  For `1/3<u<2/3`, both lapses are positive and both equations in
(1) close when

```text
alpha a = 2(2-3u)/(3sqrt(1-u)),       alpha=kappa sigma/2,
G M/a   = 2(2-3u)/(9(1-u)).
```

This benchmark tests the normal, trace, sign, temporal equation, and angular
equation independently.  It is not a model of the Skyrmion interior.

## Nonspherical Gate

After the spherical equations hold, a constant-tension shell has
`delta S_i^j=0` in mixed components.  For every `ell>=2` harmonic, tensorial
Israel matching therefore requires

```text
[delta q_ij]=0,                  [delta K_i^j]=0             (2)
```

on the *physical displaced shell*.  In the static even scalar sector there
are three independent amplitudes in each line: temporal scalar, angular
trace, and angular tracefree.  The audit checks all six.  Its deliberately
constructed example passes a scalar trace subsystem while failing the hidden
angular-tracefree condition, demonstrating why the two master jump laws alone
cannot certify (2).

The existing distributional master transmission remains necessary and useful:
it proves that the contact-subtracted Green field solves the declared scalar
Einstein combination.  It is not sufficient because the master equation does
not itself supply the physical-shell pullback, induced metric continuity, or
the unused constraint components.

## Required Skyrmion Promotion

1. Solve the spherical Einstein-Skyrme interior, including the lapse and radial
   metric functions, and a Kottler exterior.
2. Impose both spherical equations (1), not only fixed-background
   Young-Laplace force balance.
3. Reconstruct the interior and exterior `ell=2` metric amplitudes from the
   master field and the remaining Einstein constraints.
4. Pull both metrics and extrinsic curvatures back to `r=a+xi Y`, retaining
   displacement and gauge terms.
5. Submit all six amplitudes to (2), and prove equivalence with the
   distributional source in the zero-thickness limit.

At leading order in `kappa`, the spherical background correction affects the
`O(kappa Omega^2)` quadrupole only at higher order, so the current de Sitter
response remains a legitimate feasibility calculation.  It is not yet the
self-consistent theorem needed by the paper.

## Reproduction

```bash
PYTHONPATH=. python experiments/israel_junction_gate_audit.py
python -m pytest -q tests/test_israel_junction_gate.py \
  tests/test_israel_junction_gate_audit.py
```

The source-hashed artifact is
`experiments/israel_junction_gate_certificate.json`.
