# Goal 11: Encoded-Mouth Bridge-Channel Benchmark

Goal 11 upgrades the Goal 10 bridge-channel calibration benchmark from
permuted Bell pairs to encoded mouths. The finite question is:

```text
Can low-order physical entanglement diagnostics miss an encoded bridge channel
that algebraic decoding recovers?
```

## Exact Result

The representative resource has two left physical mouths `L0,L1` and two right
logical mouths encoded into independent five-qubit perfect-code blocks
`B0,B1`. The aligned model pairs

```text
L0--B0, L1--B1.
```

The twisted model pairs

```text
L0--B1, L1--B0.
```

Each right block is a `[[5,1,3]]` stabilizer code. The pairing-dependent Bell
checks have support on one left mouth plus one nontrivial right logical
operator. Since every nontrivial right logical has physical weight at least
`d=3`, the first pairing-dependent entropy witness appears at order `d+1=4`.

**Theorem.** For encoded Bell resources whose right mouths are encoded in
distance-`d` stabilizer blocks, logical mouth twists are invisible to labeled
physical entropy diagnostics through order `d`, while perfect named-port
transmission under the identity decoder equals the number of fixed points of
the logical connectivity map. This is not a capacity formula. The pairing-aware
decoder restores the exact full logical channel.

## Representative Witness

For the default `m=2` certificate:

| Diagnostic | Aligned | Twisted |
| --- | ---: | ---: |
| coarse `S(L),S(R),I(L:R)` and logical min-cut | same | same |
| labeled physical entropy through order 3 | same | same |
| first labeled entropy split | order 4 | order 4 |
| identity decoder perfect fixed ports | 2 qubits | 0 qubits |
| pairing-aware decoder perfect ports | 2 qubits | 2 qubits |
| wrong decoder control | fails off fixed points | fails off fixed points |

The twisted model is not "no bridge." It is an encoded wrong-mouth resource:
the bridge exists only after decoding the algebraically correct right block.

## Diagnostics

- Entropy/min-cut-visible: coarse L/R entropy, mutual information, logical
  bridge min-cut, and all labeled physical entropy regions through order `3`
  agree for the representative aligned/twisted pair.
- Decoder-scale visible: full encoded blocks reveal the logical mouth map.
  This is exactly where the distance-3 code stops hiding the twist.
- Algebra-visible: the logical connectivity matrix differs and predicts the
  correct block routing.
- Channel-visible: explicit logical Kraus/Choi calculations record fixed-port
  transfer, correlated residual noise, and the pairing-aware exact channel.
- Structural-control visible: pairing-dependent logical Bell checks involve
  the correct encoded block. Dynamics are reported only by the explicit
  channel calculation.

## Relation To Goal 10

Goal 10 showed that coarse entanglement/min-cut data do not determine a named
bridge channel for permuted EPR pairs, but port-resolved pair entropies exposed
the permutation. Goal 11 hides the mouth map behind a distance-3 encoding:
low-order physical entropy probes through order 3 are blind, while algebraic
reconstruction still predicts the channel.

## Relation To Engelhardt-Liu

Engelhardt and Liu's
["Algebraic ER=EPR and Complexity Transfer"](https://arxiv.org/abs/2311.04281)
is prior art for the conceptual claim that ER=EPR should be algebraic rather
than entropy-only. Goal 11 is narrower: it gives an exact finite bridge-channel
certificate showing how a mouth map can be hidden below code distance while
remaining visible to algebraic reconstruction.

## Scientific Interpretation

The finite lesson is that a bridge-channel benchmark should ask for an
operational channel through a declared decoder or coupling, not just an amount
of entanglement. In this encoded stabilizer model, low-order physical entropy
through the code distance is blind to the logical mouth map, and the bridge is
decoder-dependent: the wrong
fixed-mouth decoder has no perfect fixed-port channel, while the algebraically
correct decoder recovers the exact full logical channel.

## Limitations

This is an exact finite stabilizer theorem, not a continuum-gravity theorem, not
a generic tensor-network geometry, not noisy approximate QEC, and not a
many-body traversable-wormhole simulation. Full encoded-block diagnostics do
detect the mouth map. The separation is against coarse and low-order physical
diagnostics, with a theorem schema for distance-`d` stabilizer encodings.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 11 encoded-mouth certificate | `PYTHONPATH=. python3 -m qgtoy er-epr-encoded --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Focused Goal 11 regression | `PYTHONPATH=. python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal11_encoded_mouth_bridge_channel_certificate` |
| JSON certificate index validation | `python3 -m json.tool docs/goal11_encoded_mouth_bridge_channel_certificate_index.json` |
