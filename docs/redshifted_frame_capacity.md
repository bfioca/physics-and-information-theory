# Redshifted Rotational-Frame Capacity Bound

Status: exact free-field one-particle capacity lower bound with finite-wall hard
static-energy support and candidate gravitational no-go input;
Type-II/generalized-entropy lift conditional

## Question

Can the near-horizon redshift make rotational reference information large even
when the observer is restricted to a fixed static-energy budget?

For the conformally coupled massless scalar in the four-dimensional de Sitter
static patch, the answer is yes at the one-particle level. The number of
angular irreps certified below a fixed Killing-energy spectral budget grows as
`sqrt(R/delta)`, where `delta=R-r_wall` is the stretched-horizon radial gap.
A particular directional token supported on those irreps loses

```text
log(R/delta)+O(1)
```

relative entropy under rotational averaging.

## Radial Energy Bound

After rescaling the field by `r` and using

```text
x=R artanh(r/R),
```

the angular-`ell` one-particle radial operator is

```text
h_ell=-d^2/dx^2+ell(ell+1)/(R^2 sinh^2(x/R)).
```

Let `X_delta` be the stretched-horizon tortoise coordinate. Fix dimensionless
offsets `0<a<b` and use the normalized Dirichlet sine packet

```text
chi_delta(x)=R^(-1/2) sqrt(2/(b-a))
 sin(pi[((X_delta-x)/R)-a]/(b-a))
```

on `X_delta-bR < x < X_delta-aR`, extended by zero. This packet lies in the
quadratic-form domain. Its kinetic form is

```text
c_chi/R^2,  c_chi=pi^2/(b-a)^2.
```

The angular potential decreases with `x`, so

```text
<chi_delta,h_ell chi_delta>
 <= R^(-2)[c_chi+ell(ell+1)/sinh^2(X_delta/R-b)].
```

Since the collar packet lies in the finite-wall Dirichlet form domain, the
Rayleigh-Ritz/min-max principle bounds the lowest eigenvalue of `h_ell` by this
quadratic form. Every angular mode through

```text
L_delta=max{ell:
 ell(ell+1)<=((E0 R)^2-c_chi)sinh^2(X_delta/R-b)}
```

has an actual finite-wall radial ground eigenstate with static frequency at most
`E0`, provided `(E0 R)^2>c_chi`. Thus the hard one-particle spectral subspace
below `E0` has dimension at least `(L_delta+1)^2`, including magnetic
degeneracy. The original common collar packet separately retains the stated
expected-energy bound.

## Exact Frame Entropy

The scalar one-particle space contains integer-spin rotation irreps. Put
`D_delta=(L_delta+1)^2` and choose

```text
|psi_delta> = sum_{ell=0}^{L_delta}
 sqrt(2ell+1)/(L_delta+1)
 |phi_ell> tensor |ell,ell>,
```

where `phi_ell` is a normalized finite-wall eigenstate below `E0`. Rotations act
trivially on the radial factor. Haar averaging removes the
cross-irrep coherences and depolarizes each spin block. Because the irrep
weights are `(2ell+1)/D_delta`, the twirled state has the single eigenvalue
`1/D_delta` with multiplicity `D_delta`. Therefore

```text
D(psi_delta || E_SO(3)(psi_delta))
 = S(E_SO(3)(psi_delta))
 = log D_delta
 = 2 log(L_delta+1).
```

This is the relative entropy of frameness of the prepared token. It is not the
entropy of the complete thermal field.

## Horizon Scaling

Using

```text
exp(2X_delta/R)=(2R-delta)/delta,
```

one obtains

```text
L_delta^2 ~ C(E0,R,a,b) R/delta,
C=[((E0 R)^2-c_chi) exp(-2b)]/2.
```

Hence

```text
D(psi_delta || E_SO(3)(psi_delta))
 = log(R/delta)+O(1).
```

The exact proper distance from the wall to the horizon is

```text
rho=R acos(1-delta/R),
```

so `delta=rho^2/(2R)+o(rho^2/R)` and, for horizon area `A=4 pi R^2`,

```text
log(R/delta)=log[A/(2 pi rho^2)]+O(rho^2/R^2).
```

## Physics Interpretation

The theorem gives a geometry-derived capacity lower bound. In a hard finite-wall
static-energy window, the redshifted collar variational estimate guarantees a
pure coherent directional token
whose discarded `SO(3)`-frame information grows logarithmically as the wall
approaches the horizon. It becomes an observer obstruction only after one
specifies which observer channel necessarily performs that rotational average.

The gravitational no-go statement is conditional. If the rotation expectation
extends trace-preservingly to the physical Type-II observer algebra, and if its
trace entropy agrees with generalized entropy up to a state-independent
constant, then the same logarithm appears as an observer-entropy penalty. A
scalar-clock dictionary with exact orientation loss must then do at least one
of the following:

1. add a covariant rotational observer/reference;
2. impose an independent near-horizon angular or local-energy cutoff;
3. include a cutoff-dependent renormalized correction;
4. or show that backreaction excludes the token family.

## Novelty Boundary

The ingredients are individually standard:

- near-horizon redshift and angular density of states;
- relative entropy of frameness;
- Type-II observer entropy and its semiclassical generalized-entropy relation.

The candidate new result is their exact combination into a hard finite-wall
static-energy `log(R/delta)` lower bound for missing rotational-frame
information. A targeted primary-source search through 2026-06-07 found no
direct statement of this bound. The closest geometric overlap is Anninos et
al., who relate proper horizon distance to a large angular cutoff and
`ell_max^2` horizon pixels; brick-wall and stretched-horizon mode papers also
derive the redshifted angular density of states. Gour, Marvian, and Spekkens
supply the relative-entropy-of-frameness identity. The contribution here is the
explicit quantitative connection of those ingredients, not a new density of
states law. This logarithm must also be distinguished from the rotational
zero-mode/path-integral logarithmic correction discussed by CLPW: their origin
and coefficient are not identified by this theorem. Search absence is not
novelty proof, so a specialist review and external expert check remain required.

Defensible claim:

> We are not aware of a prior derivation combining a fixed finite-wall static
> energy constraint with an explicit near-horizon rotational reference token
> and evaluating its lost frame information by relative entropy. The
> near-horizon angular mode proliferation and relative entropy of frameness are
> individually standard; the result is their explicit quantitative connection.

## Claim Boundary

The theorem currently assumes:

- a free conformally coupled scalar;
- the one-particle sector;
- a moving near-horizon collar in the form domain;
- hard finite-wall static-energy spectral support from the min-max principle,
  but no local proper-energy or gravitational energy constraint;
- the compact `SO(3)` rotation subgroup, not full `SO(1,4)` covariance;
- no backreaction, local proper-energy, or occupation-number constraint.

It does not establish the Bunch-Davies all-angular Weyl limit, Type `III_1`, a
Type-II trace extension, or a generalized-entropy identity.

Primary context:

- Gour, Marvian, and Spekkens, [Measuring the quality of a quantum reference
  frame: the relative entropy of frameness](https://arxiv.org/abs/0901.0943).
- Chandrasekaran, Longo, Penington, and Witten, [An Algebra of Observables for
  de Sitter Space](https://arxiv.org/abs/2206.10780).
- Chen and Xu, [An algebra for covariant observers in de Sitter
  space](https://arxiv.org/abs/2511.00622v2).
- Begines, Das, Jeong, and Pedraza, [Cosmological brick walls and quantum
  chaotic dynamics of de Sitter horizons](https://arxiv.org/abs/2603.29443v2).
- Anninos et al., [The Stretched Horizon
  Limit](https://arxiv.org/abs/2512.16738).

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy redshifted-frame-capacity
PYTHONPATH=. python3 -m unittest tests.test_redshifted_frame_capacity
```
