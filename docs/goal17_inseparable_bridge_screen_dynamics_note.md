# Goal 17: Inseparable Bridge-Screen Dynamics Theorem

Goal 17 removes the last bolt-on layer from the bridge benchmarks. The bridge
state, inverse-interaction decoder, and north/south screen channels now live in
one declared finite dynamics record, rather than a bridge state followed by a
separate screen-completion rule.

## Objects

The bridge part is the Goal 16 object: `m` left mouths, `m` encoded right
mouths, a permutation `pi`, and a right-mouth graph-`CZ` interaction `G`. The
executable witness uses three mouths, path graph `((0,1),(1,2))`, twisted map
`(1,0,2)`, and right `[[5,1,3]]` blocks.

The screen part is a built-in coherent qutrit-erasure router for one recovered
logical payload qubit. Tracing one output gives the north screen channel;
tracing the other gives the south screen channel. Both screen channels are
part of the same declared dynamics record as the interacting bridge.

## Theorem-Style Claims

**Unified dynamics.** One finite channel/circuit record contains the encoded
bridge preparation, right-mouth graph-`CZ` interaction, inferred inverse
interaction decoder, and north/south screen router.

**Bridge reconstruction.** Full-block mutual information recovers `pi`;
Pauli-correlation tomography recovers `G`; conjugating the right logical Pauli
algebra by recovered `CZ_G` gives the dressed observer algebra.

**Bridge transfer.** Removing recovered `CZ_G` and routing by recovered `pi`
restores exact transfer. In the representative witness, state-derived transfer
has capacity `3`, identity/wrong-mouth activation has capacity `1`, and the
mouth-blind scrambling control has capacity `0`.

**Screen transition.** The north/south keep probabilities are read from the
screen Kraus operators. Recovery fidelity and the finite quantum-area analogue
are computed from the same channel-derived probability, so the transition is
at `p=1/2`.

**Controls.** Static bridge-state data alone still cannot choose a screen
recovery transition; opposite screen-channel completions share the same static
signature. Adding an external bare-area bias not produced by the channel shifts
the area crossing to `0.375` while the recovery crossing remains `0.5`.

## Representative Witness

| Diagnostic | Result |
| --- | --- |
| mouth map | `(1,0,2)` from full-block MI |
| interaction graph | `((0,1),(1,2))` from Pauli correlations |
| observer algebra | logical dimension `6`, symplectic rank `6`, center `0` |
| low-order entropy | aligned/twisted match through order `3` |
| first entropy split | order `4` |
| state-derived bridge transfer | `3` logical qubits |
| wrong-mouth activation | `1` logical qubit |
| mouth-blind scrambling | `0` logical qubits |
| screen transition | south at `p=0`, tie at `p=0.5`, north at `p=1` |

## Bounded Atlas

The executable atlas checks all simple graphs, all mouth permutations, and
screen probabilities `{0, 0.5, 1}` for `m <= 3`.

| `m` | Graphs | Dynamics Checked | Pairing | Graph | Transfer | Screen |
| --- | ---: | ---: | --- | --- | --- | --- |
| 1 | 1 | 3 | pass | pass | pass | pass |
| 2 | 2 | 12 | pass | pass | pass | pass |
| 3 | 8 | 144 | pass | pass | pass | pass |

## Claim Boundary

This is a finite stabilizer/QEC plus small dense-channel theorem package. The
screen router is an explicit finite qutrit-erasure isometry inside the declared
dynamics. It is not a continuum ER=EPR theorem, not de Sitter physics, not
dS/CFT, and not a chaotic many-body wormhole simulation.

The useful claim is narrower: within this finite model, the bridge algebra,
bridge channel, screen channels, and recovery/area-analogue transition are
outputs of one declared dynamics family.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 17 theorem certificate | `PYTHONPATH=. python3 -m qgtoy bridge-screen-dynamics --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Focused Goal 17 regression | `PYTHONPATH=. python3 -m unittest tests.test_bridge_screen_dynamics` |
| JSON certificate index validation | `python3 -m json.tool docs/goal17_inseparable_bridge_screen_dynamics_certificate_index.json` |
