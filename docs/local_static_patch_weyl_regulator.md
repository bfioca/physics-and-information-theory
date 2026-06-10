# Local Static-Patch S-Wave KMS Covariance Regulator

Status: first geometrically derived equal-time radial refinement; spacetime-net
and factor-type proofs open

## Physical Model

Use the four-dimensional de Sitter static-patch metric

```text
ds^2=-(1-r^2/R^2)dt^2+(1-r^2/R^2)^(-1)dr^2+r^2dOmega_2^2.
```

For a conformally coupled massless scalar, rescale the radial field by `r` and
introduce tortoise coordinate

```text
x=R artanh(r/R).
```

The s-wave potential vanishes. A stretched horizon at `r=R-delta` gives

```text
0<x<X_delta,
X_delta=(R/2)log[(2R-delta)/delta],
omega_n=n pi/X_delta.
```

The continuum target is fixed by geometry: the Bunch-Davies restriction is KMS
for static time at inverse temperature

```text
beta_dS=2 pi R.
```

The reflecting wall at `r=R-delta` is not part of that state. Here `delta` is a
radial-coordinate gap, not a proper distance. The finite objects below are
Dirichlet Gibbs approximants chosen for calculational control; identifying
their local limit with the Bunch-Davies s-wave state beyond the displayed
equal-time covariance remains an open theorem.

## Local Rather Than Global Convergence

Let `f` be an `L^2`-normalized indicator used to smear the rescaled radial field
on one equal-time slice, with support in a fixed compact tortoise interval
`[a,b]`. Its sine transform is

```text
F(k)=[cos(ka)-cos(kb)]/[k sqrt(b-a)].
```

The finite stretched-patch covariance through momentum cutoff `K` is exactly a
Riemann sum,

```text
C_delta(f)=1/X_delta sum_{n pi/X_delta<=K}
 |F(n pi/X_delta)|^2 coth(beta n pi/(2X_delta))/(n pi/X_delta).
```

As `delta` tends to zero, `X_delta` diverges, the radial mode spacing collapses,
and this converges to

```text
C(f)=1/pi int_0^K |F(k)|^2 coth(beta k/2) dk/k.
```

This is local equal-time covariance convergence on fixed compact support, not
trace-norm convergence of global Gibbs density matrices. It is compatible with
the kind of distributional limit needed for a local Weyl net and avoids the
global Type-I gate, but it is not yet a construction of that net. The companion
fixed-UV phase-space theorem controls conjugate momentum, the projected
symplectic form, and unequal-time KMS correlations. Smooth UV removal,
spacetime locality, and all angular sectors still have to be controlled.

## What This Establishes

- a field model derived from the de Sitter static metric;
- the geometric KMS temperature `2 pi R`;
- a stretched-horizon regulator whose radial mode spacing tends to zero;
- fixed compact support embedded in an increasing sequence of stretched-patch
  intervals;
- explicit convergence of a fixed-UV equal-time smeared covariance in the
  rescaled s-wave sector.

## Remaining Theorem

This is not yet the Type-`III_1` static-patch algebra. Completion requires:

1. remove the fixed UV bandlimit on smooth s-wave phase-space data and restore
   spacetime locality;
2. add all angular sectors, followed by distributional convergence of the full
   quasifree covariance and symplectic
   form;
3. identification with the Bunch-Davies local GNS representation;
4. a theorem that the patch algebra is hyperfinite Type `III_1`;
5. the continuous core only after that limit;
6. extension of the angular screen expectation and reference-frame recovery
   bounds to localized wavepackets;
7. gravitational constraints, the observer Hamiltonian, and generalized
   entropy.

Primary context:

- Bros, Epstein, and Moschella, [Analyticity properties and thermal effects for
  general quantum field theory on de Sitter
  space](https://arxiv.org/abs/gr-qc/9801099).
- Verch, [Continuity of symplectically adjoint maps and the algebraic structure
  of Hadamard vacuum representations for quantum fields on curved
  spacetime](https://arxiv.org/abs/funct-an/9609004).
- Chandrasekaran, Longo, Penington, and Witten, [An Algebra of Observables for
  de Sitter Space](https://arxiv.org/abs/2206.10780).

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-weyl-regulator
PYTHONPATH=. python3 -m unittest tests.test_static_patch_weyl_regulator
```
