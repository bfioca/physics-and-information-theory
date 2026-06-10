# Single-Irrep Directional Reference No-Go

Status: exact `SU(2)` multiplicity obstruction with a quantitative recovery bound

## Question

Is nontrivial rotation charge alone enough for a finite directional reference to
restore the full quantum algebra of a spin-`L` system?

Take an arbitrary fixed product state `eta` on one spin-`J` reference, with no
accessible multiplicity ancilla, and the physical channel

```text
E_eta(rho)=SU(2)-twirl(rho tensor eta).
```

## Multiplicity-Free Obstruction

Clebsch-Gordan decomposition gives

```text
V_L tensor V_J = direct_sum_{K=|L-J|}^{L+J} V_K,
```

with multiplicity one for every total spin `K`. The fixed operator algebra is
therefore

```text
direct_sum_K C I_{V_K}.
```

It is abelian. More explicitly, the channel has measure-and-prepare form

```text
E_eta(rho)=sum_K Tr(M_K rho) P_K/(2K+1),
```

for the POVM induced by `eta` and the total-spin projectors `P_K`. Every
twirled output is specified only by a classical distribution over total-spin
sectors. This holds for every prepared reference state `eta`, including
spin-coherent states and arbitrarily large `J`. The append-and-twirl channel is
equivalent to a quantum-to-classical channel followed by state preparation, and
is therefore entanglement-breaking.

## Quantitative Recovery No-Go

Let `d=2L+1`. Composing an entanglement-breaking channel with any deterministic
CPTP decoder remains entanglement-breaking. Apply the decoded channel to half
of a maximally entangled state of Schmidt rank `d`. Its output is separable and
has overlap at most `1/d` with the target maximally entangled state. Measuring
the target projector gives

```text
(1/2)||D E_eta - identity||_diamond >= 1-1/d.
```

Thus the full spin-sector recovery error is at least

```text
1 - 1/(2L+1),
```

independently of how large the single reference spin `J` becomes.

## Physics Meaning

The scalar-reference no-go was not evaded merely by adding nonzero rotation
charge. A full quantum observer algebra also needs representation multiplicity:
several irreps, repeated irreps, or an approximation to a Peter-Weyl/regular
reference. A large semiclassical vector can be excellent for restricted
direction-estimation tasks while still being incapable of preserving an
arbitrary quantum spin sector after full group averaging.

This is standard Clebsch-Gordan and entanglement-breaking machinery. Its value
here is as a model-selection constraint on gravitational observers, not as a
standalone novelty claim. Reducible references with multiplicities,
accessible spectator/multiplicity ancillas, correlated or input-dependent
references, postselection, restricted classical tasks, half-integer API
support, interacting KMS realization, de Sitter boosts, and generalized entropy
remain open.

Reproduce with:

```bash
PYTHONPATH=. python3 -m qgtoy su2-directional-reference-no-go --max-system-spin 8
PYTHONPATH=. python3 -m unittest tests.test_su2_directional_reference_no_go
```
