# Many-Body Modular Regulator And Type-II Continuous Core

Status: exact finite compatibility plus standard ITPFI/core limit theorem

## Regulator

Let

```text
A_n = M_2 tensor ... tensor M_2 = M_{2^n}.
```

Odd sites have energy gap `1`, even sites gap `sqrt(2)`. At inverse
temperature `beta`, use the faithful one-site Gibbs state and its product
`phi_n`. The maps

```text
iota_n(A) = A tensor I,
E_{n+1,n} = id tensor phi_{n+1}
```

are canonical, UCP where appropriate, and state preserving. Because the density
matrices factor, modular dynamics is exactly compatible:

```text
sigma_t^{n+1}(A tensor I) = sigma_t^n(A) tensor I,
E sigma_t^{n+1} = sigma_t^n E.
```

All cylinder-state expectations, products, and modular correlators stabilize
once their support is included.

## Algebra Type From The State

The modular eigenvalue ratios generate

```text
{exp[-beta(m+n sqrt(2))] : m,n in Z}.
```

Regroup the chain into one repeated two-site product block, or equivalently
separate the odd and even Powers subchains. Their parameters are `exp(-beta)`
and `exp(-beta sqrt(2))`. Since `sqrt(2)` is irrational, the recurrent
asymptotic ratio group has nonzero part

```text
closure{exp[-beta(m+n sqrt(2))] : m,n in Z} = positive reals.
```

Thus the Connes invariant is `S(M)=[0,infinity)`. Standard ITPFI/Connes
classification gives the hyperfinite Type-`III_1` factor in the product-state
GNS representation.

This is the essential change from the earlier trace-based UHF scaffold: the
algebra type follows from the recurrent tail/asymptotic ratio set of a declared
faithful nontracial product state, not from matrix growth or the spectrum of one
finite modular operator.

## Continuous Core

The modular action is inner at every finite cutoff. In the Type-`III_1` limit,
the Connes `T` invariant is `{0}`, so the modular automorphism is outer for
every nonzero modular time. The continuous crossed product

```text
M crossed_{sigma^phi} R
```

is the hyperfinite Type-`II_infinity` continuous core and carries a faithful
normal semifinite trace, canonical up to positive scale. The real
crossed-product coordinate is interpreted here as an ideal observer clock
conjugate to modular time.

The executable certificate directly checks only the finite tensor-state and
modular-covariance identities. The Type-III and continuous-core conclusions
are analytic consequences of standard classification theorems; they are not
inferred from a bounded numerical experiment.

This discharges the algebra-type and trace mechanism in a controlled many-body
surrogate. It does not yet discharge the physics:

- the chain has no fuzzy-sphere locality or static-patch causal structure;
- the product Gibbs state is chosen, not derived from a Euclidean or
  Hartle-Hawking construction;
- no generalized-entropy matching is proved;
- the angular edge-reference algebra has not yet been coupled to the core.

## Next Theorem

Build a local net combining fuzzy angular cells with the modular chain and show
that the relational edge conditional expectation extends to the Type-II core.
The key question is whether the recovery lower bound and vanishing retained-
algebra fraction persist after the crossed product, preferably as a trace or
entropy inequality.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy modular-manybody-regulator --max-sites 10
PYTHONPATH=. python3 -m unittest tests.test_modular_manybody_regulator
```

## Classification Sources

- Powers, [Representations of uniformly hyperfinite algebras and their
  associated von Neumann
  rings](https://annals.math.princeton.edu/1967/86-1/p06).
- Araki and Woods, [A classification of
  factors](https://doi.org/10.2977/prims/1195195263).
- Connes, [Une classification des facteurs de type
  III](https://www.numdam.org/item/ASENS_1973_4_6_2_133_0/).
- Takesaki, [Duality for crossed products and the structure of von Neumann
  algebras of type III](https://doi.org/10.1007/BF02392041).
