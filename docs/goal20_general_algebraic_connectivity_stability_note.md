# Goal 20: General Finite-Dimensional Algebraic Connectivity Stability

Goal 20 lifts Goal 19 beyond the one-qubit Pauli-diagonal setting. The result
is a no-go with a completion principle:

```text
relative-entropy response plus product/commutator closure certifies a probed
recoverable algebra, but it does not determine the maximal recoverable observer
algebra unless the probes are informationally complete.
```

## No-Go Theorem

For every `d >= 2`, take two observer channels on `M_d`:

- `N_id`: the identity channel;
- `N_diag`: complete dephasing onto the diagonal algebra `C^d`.

Use the intrinsic probe algebra `B = C^d`, with diagonal state pairs and
pointwise product.

Then:

- all relative entropies for state pairs in `B` are preserved exactly by both
  channels;
- product and commutator closure on `B` is exact for both channels;
- the maximally mixed static entropy shadow is the same for both channels;
- but the maximal recoverable observer algebras differ:

```text
N_id:   M_d
N_diag: C^d
```

So the diagnostic is exact but incomplete. It proves recovery of the probed
algebra `B`; it does not prove maximality.

## Minimal And Non-Pauli Witnesses

| Witness | Dimension | Probed Algebra | Identity Algebra | Dephasing Algebra |
| --- | ---: | --- | --- | --- |
| minimal | `2` | `C^2` | `M_2` | `C^2` |
| non-Pauli finite-dimensional | `3` | `C^3` | `M_3` | `C^3` |

For the `d=2` minimal witness, the diagonal probe relative entropy is
`0.333333333333` bits for both channels. An off-diagonal matrix-unit coherence
probe has input relative entropy `0.184241398542` bits; identity preserves it
and dephasing sends it to `0`.

## Bounded Family

The certificate checks the exact family for `2 <= d <= 5`.

| Quantity | Value |
| --- | --- |
| dimensions checked | `2,3,4,5` |
| probe diagnostics collide | yes |
| maximal algebras differ | yes |
| off-diagonal completion probes separate | yes |

## Completion Principle

The fix is not to abandon recoverable algebra. The fix is to report two facts:

```text
1. which probe algebra has been certified recoverable;
2. whether the diagnostic is informationally complete for maximality.
```

In the exact case, if relative entropy is tested on the full state space of a
candidate algebra, Petz/OAQEC recovery applies to that algebra. In the
approximate case, universal recovery supplies state-level fidelity bounds, but
uniform algebra/channel stability still needs explicit finite nets and
dimension-dependent continuity constants.

## Relation To Goal 19

Goal 19 is the one-qubit Pauli-diagonal special case where the probes `X,Y,Z`
are informationally complete for `M_2` and commutator closure checks the Pauli
product structure. Goal 20 removes that hidden completeness assumption.

## Simulation Signature

In a tensor-network, random-circuit, or quantum-simulator bridge, compare:

- a diagonal/classical probe suite; and
- added off-diagonal matrix-unit coherence probes.

The signature is:

```text
same entropy and same classical response,
different off-diagonal response.
```

That indicates hidden quantum algebraic connectivity missed by an incomplete
observer probe atlas.

## Claim Boundary

This is a finite-dimensional exact no-go and completion-principle certificate.
It is not a continuum ER=EPR theorem, not de Sitter physics, not a type-III
algebra theorem, and not a full approximate OA-QEC stability theorem.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 20 certificate | `PYTHONPATH=. python3 -m qgtoy general-algebraic-connectivity --max-dim 5` |
| Focused regression | `PYTHONPATH=. python3 -m unittest tests.test_general_algebraic_connectivity` |
| JSON certificate index validation | `python3 -m json.tool docs/goal20_general_algebraic_connectivity_stability_certificate_index.json` |
