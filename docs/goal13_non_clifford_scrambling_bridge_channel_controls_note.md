# Goal 13: Non-Clifford And Scrambling Bridge-Channel Controls

Goal 13 strengthens the finite bridge-channel benchmark beyond the exact
Clifford Bell-transfer instrument of Goal 12. The finite question is:

```text
Can algebraic bridge connectivity still predict transfer after adding a
non-Clifford channel layer and a generic scrambling control?
```

## Exact Result

The resource is the Goal 11/12 encoded-mouth family: physical left mouths
`L_i` are Bell-paired with logical right mouths encoded in independent
`[[5,1,3]]` blocks `B_j`. A pairing `pi` declares the algebraic receiver:

```text
L_i -- B_{pi(i)}.
```

Goal 13 compares four finite control protocols:

| Control | Uses mouth map? | Structured capacity on matched mouth | Pauli/channel signal |
| --- | ---: | ---: | --- |
| identity Clifford activation | public activation `alpha` | `1` iff `alpha(i)=pi(i)` | identity Pauli transfer |
| algebra-aware Clifford activation | `alpha=pi` explicitly | full | identity Pauli transfer |
| algebra-aware `T`-dressed activation | `alpha=pi` explicitly | full | non-Clifford `T` Pauli transfer |
| mouth-blind Pauli-twirled scrambler | no | zero | zero named-mouth Pauli transfer |

**Theorem.** In the encoded-mouth family, coarse entropy/min-cut and labeled
physical entropy through the code distance do not identify `pi`. Naive identity
activation can therefore have different transfer capacity on entropy-matched
resources. Algebra-aware activations restore full transfer, including after a
non-Clifford logical `T` dressing. A mouth-blind Pauli-twirled scrambling proxy
has zero structured named-mouth transfer.

## Representative Witness

For `m=2`, aligned and twisted resources have the same coarse and low-order
entropy shadows through order `3`, with the first entropy split at order `4`.

| Diagnostic | Aligned | Twisted |
| --- | ---: | ---: |
| coarse entropy/min-cut | same | same |
| labeled physical entropy through order 3 | same | same |
| identity activation capacity | 2 | 0 |
| algebra-aware Clifford capacity | 2 | 2 |
| algebra-aware `T`-dressed capacity | 2 | 2 |
| mouth-blind scrambling capacity | 0 | 0 |

The `T`-dressed control is not an identity Clifford channel: it rotates the
logical Pauli transfer in the `X/Y` plane and has direct identity entanglement
fidelity `(2 + sqrt(2))/4`. A declared `T^dagger` phase frame restores identity
fidelity `1`, so the non-Clifford layer changes the channel signature without
destroying bridge capacity.

## Diagnostics

- Entropy/min-cut-visible: coarse L/R entropy, logical min-cut, and labeled
  physical entropy through the code distance match for aligned/twisted
  resources.
- Algebra-visible: the connectivity map `pi` predicts which public activation
  map transfers.
- Channel-visible: Pauli transfer matrices, direct identity fidelity,
  phase-corrected fidelity, and quantum capacity distinguish Clifford,
  non-Clifford, missed, and twirled controls.
- OTOC/support-visible: bridge activations produce support-growth signals on
  the algebraic receiver; the mouth-blind twirled control has no structured
  named-mouth signal.
- Control-visible: wrong-mouth and mouth-blind controls fail despite matching
  entropy resources.

## Relation To Engelhardt-Liu

Engelhardt and Liu's
["Algebraic ER=EPR and Complexity Transfer"](https://arxiv.org/abs/2311.04281)
is the primary conceptual prior art for the broad operator-algebraic ER=EPR
framing. Goal 13 is narrower: it supplies a finite bridge-channel control
benchmark showing that algebraic mouth maps, not entropy shadows or generic
scrambling alone, predict structured transfer in the declared QEC setting.

## Limitations

This is an exact finite encoded-QEC benchmark, not a continuum-gravity theorem
or chaotic many-body simulation. The non-Clifford control is a logical
`T`-dressed channel, and the generic scrambling control is a mouth-blind
Pauli-twirled proxy. Full encoded-block diagnostics still reveal the mouth map.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 13 control certificate | `python3 -m qgtoy bridge-channel-controls --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Focused Goal 13 regression | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal13_non_clifford_scrambling_bridge_controls_certificate` |
| JSON certificate index validation | `python3 -m json.tool docs/goal13_non_clifford_scrambling_bridge_channel_controls_certificate_index.json` |
