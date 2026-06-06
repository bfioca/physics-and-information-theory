# Major Unlock: Relative-Entropy Observer-Bridge Theorem

This note is the aggressive next target after Goal 18. Instead of asking only
for stabilizer/Puali response or product-table tomography, it asks for a
basis-independent operational diagnostic:

```text
which observer algebra and bridge channel are determined by preserved
relative entropy under physical observer-region channels?
```

## Theorem-Style Statement

Let `N_R` be the finite-dimensional channel from the code system to observer
region `R`. Let `A` be a candidate finite-dimensional observable algebra in the
code system. In the exact finite-dimensional setting:

```text
A is reconstructable on R
iff
D(rho || sigma) = D(N_R rho || N_R sigma)
for all full-rank state pairs rho,sigma in the state space of A.
```

When the equality holds, Petz/OAQEC recovery reconstructs `A` up to
`*-`isomorphism. For bridge dynamics `T`, the bridge-transferred observer
algebra is the largest subalgebra whose relative entropy is preserved by the
composed observer-to-observer channel.

This is not a new Petz theorem. It is a finite observer-bridge packaging of the
known recovery theorem: use intrinsic distinguishability preservation, rather
than labeled logical probes or supplied product tables, to identify the
observer algebra and bridge transfer.

## Why This Is Stronger Than Goal 9

Goal 9 used full product/adjoint tomography. That is mathematically complete,
but very close to handing over the algebra.

This theorem uses operational distinguishability response:

```text
relative-entropy defect = D(rho||sigma) - D(N rho||N sigma).
```

Zero defect on a state family identifies preserved information; nonzero defect
identifies lost observer probes. Product structure appears only after the
preserved state space/algebra has been recovered.

## Finite Certificate

The certificate uses full-rank qubit probes

```text
rho_P = (I + rP)/2
sigma_P = (I - rP)/2
P in {X,Y,Z}, r=0.5
```

The relative entropy before the channel is `0.792481250361` bits for each axis.

| Channel | Static entropy shadow | Relative-entropy response | Observer algebra |
| --- | --- | --- | --- |
| identity | `(1,1)` | preserves `X,Y,Z` | `M_2` |
| Z-dephasing | `(1,1)` | preserves `Z`, loses `X,Y` | `C direct-sum C` |
| depolarizing/null | `(1,1)` | loses `X,Y,Z` | `C` |
| trace gauge qubit | abstract `M_2` | preserves `X,Y,Z` | represented `I_2 tensor M_2` |

So the static entropy shadow can match while the relative-entropy response
separates quantum, classical, and null observer bridges.

## Relation To Goal 18

Goal 18 is the exact stabilizer/QEC local-screen benchmark: local channels
derive bridge-screen transfer and entropy-only controls fail. The present
theorem replaces stabilizer-specific Pauli response with finite-dimensional
relative-entropy response. Stabilizer commutator tomography becomes a special
case of intrinsic distinguishability/recovery data.

## Relation To Prior Work

- Bény, Kempf, and Kribs introduced the Heisenberg/OAQEC observable-algebra
  framework: [arXiv:0705.1574](https://arxiv.org/abs/0705.1574).
- Dong, Harlow, and Wall connect relative entropy, QEC, and entanglement-wedge
  reconstruction: [arXiv:1601.05416](https://arxiv.org/abs/1601.05416).
- Cotler, Hayden, Penington, Salton, Swingle, and Walter extend universal
  recovery channels for finite-dimensional operator algebras:
  [arXiv:1704.05839](https://arxiv.org/abs/1704.05839).
- Blume-Kohout, Ng, Poulin, and Viola classify preserved information structures
  in quantum processes: [arXiv:1006.1358](https://arxiv.org/abs/1006.1358).
- Engelhardt and Liu provide the algebraic ER=EPR conceptual banner:
  [arXiv:2311.04281](https://arxiv.org/abs/2311.04281).

## What Is New Here

The new contribution is not the underlying recovery theorem. The new
contribution is the finite observer-bridge diagnostic package:

- entropy/static shadows can collide;
- relative-entropy response separates quantum/classical/null observer bridges;
- represented gauge multiplicity is recorded separately from abstract algebra;
- Goal 18 is recovered as an exact stabilizer/QEC instance;
- the next genuinely major frontier is now explicit: quantitative approximate
  observer-bridge recovery from noisy relative-entropy response.

## Approximate Frontier

Universal recovery gives a state-level quantitative seed. If the
relative-entropy defect is `epsilon` bits, the known recovery bound gives a
state-level fidelity lower bound of at least

```text
2^(-epsilon/2).
```

The certificate records this bound for a small grid of defects. It does not
claim that this is already a full noisy observer-algebra theorem. The missing
step is to upgrade state-level recovery to uniform algebra/channel recovery
over an observer algebra, with explicit finite-dimensional net and continuity
costs.

## Limitations

This is an exact finite-dimensional theorem package. It is not continuum
ER=EPR, not de Sitter physics, not dS/CFT, and not a type-III algebra theorem.
The strongest future step is an approximate/noisy version with explicit
recovery bounds.

## Reproducibility

| Claim | Command |
| --- | --- |
| Relative-entropy observer-bridge certificate | `PYTHONPATH=. python3 -m qgtoy relative-entropy-bridge-theorem` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_relative_entropy_bridge` |
