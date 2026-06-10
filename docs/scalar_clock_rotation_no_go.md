# Energy-Constrained Rotational Frameness Obstruction

Status: quantitative compact-fixed-point obstruction for a clock-only
truncation with rotation-invariant spectators; the full constraint construction,
crossed-product extension, backreaction, and gravitational entropy remain open

## Scope

CLPW already explains that a clock alone retains only rotation-invariant
observables and that an orthonormal observer frame is needed to dress angular
operators. Its full observer discussion is therefore not a clock-only model.
This theorem quantifies the energy-constrained information loss of the
deliberately restricted clock-only truncation; it does not claim discovery of
the qualitative clock-versus-frame distinction.

The target is a different necessary-condition question: can that scalar clock,
without additional charged observer degrees of freedom, preserve directional
information under the compact stabilizer required by a full de Sitter gauge
completion?

Any full `SO(1,4)` gauge completion must impose invariance under the compact
`SO(3)` stabilizer of the observer geodesic. A scalar clock transforms trivially
under this subgroup. If every other accessible spectator is also invariant,
physical compact-subgroup observables lie in the field fixed-point algebra.
Orbit-related states then have identical restrictions to that algebra. The
canonical `SO(3)` conditional expectation realizes this restriction as a
channel and makes the decoder bound explicit. The module does not construct the
noncompact `SO(1,4)` group average or its crossed product.

## Bounded-Energy Directional Pair

At a finite Dirichlet wall, the collar trial functions constructed in
`redshifted_frame_capacity.md` have Rayleigh quotient at most `E0^2` for angular
momenta through

```text
L_delta=Theta(sqrt(R/delta))
```

The min-max principle therefore gives a normalized radial ground eigenstate
`phi_ell` with static frequency at most `E0` in every such spin sector. This is
hard one-particle spectral support, not only an expectation bound.

In the highest certified spin sector choose

```text
|psi_+>=|phi_L> tensor |L_delta,L_delta>,
|psi_->=|phi_L> tensor |L_delta,-L_delta>.
```

They are orthogonal, related by a rotation, and have identical spectral measures
and parallel evolution under every rotation-invariant operator on that
isotypic sector. Their restrictions to the fixed-point algebra agree. Haar
expectation sends both density matrices to

```text
I_(2L_delta+1)/(2L_delta+1)
```

on their common spin sector.

Hence every decoder through a rotation-trivial scalar-clock gauge channel has
worst-case trace-distance error at least

```text
1/2.
```

For recovery of the full spin sector, the expectation is completely
depolarizing, so every decoded channel is a replacer. The exact optimal
normalized diamond recovery error is

```text
1-1/(2L_delta+1)^2,
```

which tends to one as the stretched wall approaches the horizon.

The pair already lies in the hard finite-wall field-energy window. Extending the
fixed-point expectation through a named time crossed product or gravitational
constraint requires a commuting-square theorem that is not proved here. Any
additional invariant projection acts identically on the magnetic labels, but a
claim about its normalized output still requires nonzero common support.

## Missing-Frame Entropy

For the coherent token over all spins through `L_delta`, the `SO(3)` twirl has
relative-entropy loss

```text
2 log(L_delta+1)=log(R/delta)+O(1).
```

This is the relative entropy of rotational frameness in the free one-particle
sector. It is not yet a gravitational entropy or the entropy of the complete
thermal field. A positive-energy corner can reweight different spin sectors,
so extending the exact logarithm to its finite trace requires a separate
trace-preserving conditional-expectation theorem.

## The Necessary Obstruction

Under the stated assumptions:

> In a clock-only truncation whose accessible spectators are `SO(3)` invariant,
> the compact fixed-point algebra cannot distinguish the displayed hard-static-
> energy directional pair. The canonical conditional expectation produces an
> exact half-error decoder obstruction, and full spin-sector recovery has exact
> optimal error tending to one.

The result forces at least one of the following:

1. add a covariant observer carrying nontrivial `SO(1,d)` reference charge;
2. add another prepared directional reference with sufficient irrep
   multiplicity;
3. impose a physical local-energy, backreaction, or occupation constraint that
   excludes the collar states;
4. abandon full isometry gauging or accept the orientation information loss.

Chen and Xu's covariant observer is an explicit escape route: the observer
geodesic transforms under the full de Sitter group and becomes a quantum
reference frame. That model lies outside this theorem precisely because the
observer is not rotation trivial.

## Novelty Boundary

The qualitative clock-versus-frame obstruction is already explicit in CLPW,
and the ingredients below are known separately:

- scalar-clock modular crossed products;
- full-isometry gauging and covariant observers;
- `SO(3)` twirling and reference-frame recovery bounds;
- near-horizon angular mode proliferation.

The candidate new result is their quantitative conjunction on the same local
Bunch-Davies benchmark: a hard finite-wall static-energy directional pair with
exact half-error loss under the compact expectation, the exact optimal
`1-1/(2L_delta+1)^2` full-sector recovery error, and the associated
`log(R/delta)` frame entropy. This is an energy-constrained refinement of the
known qualitative obstruction. Establishing the commuting expectation and
survival conditions in a named gravitational completion remains a separate
theorem.

Primary context:

- Chandrasekaran, Longo, Penington, and Witten,
  [An Algebra of Observables for de Sitter Space](https://arxiv.org/abs/2206.10780);
- Chen and Xu,
  [An algebra for covariant observers in de Sitter space](https://arxiv.org/abs/2511.00622);
- Gour, Marvian, and Spekkens,
  [relative entropy of frameness](https://arxiv.org/abs/0901.0943).

## Claim Boundary

Assumptions:

- free conformally coupled scalar in the one-particle collar sector;
- hard finite-wall one-particle static-energy support obtained by min-max, but
  no local proper-energy or gravitational energy support;
- full de Sitter gauge completion includes the compact `SO(3)` stabilizer;
- observer clock is rotation trivial;
- all accessible spectators are rotation invariant;
- any subsequent constraint/corner operation used in a stronger conclusion
  commutes with rotations and retains nonzero common support for the pair.

Not proved:

- that backreacting gravity admits the collar family;
- a local proper-energy or occupation-number bound;
- a noncompact `SO(1,4)` group average or a crossed-product commuting square;
- convergence of finite regulator algebras in von Neumann topology;
- a finite Type-`II_1` trace formula for the coherent token;
- equality with generalized entropy.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy scalar-clock-rotation-no-go
PYTHONPATH=. python3 -m unittest tests.test_scalar_clock_rotation_no_go
```
