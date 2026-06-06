# Goal 18: Intrinsic Local Bridge-Screen Dynamics

Goal 18 replaces Goal 17's declared north/south screen router with a finite
star-local tensor network. The bridge map, interaction graph, dressed observer
algebra, bridge transfer, screen channels, and recovery/area transition are all
derived from one local interaction record.

## Objects

The bridge is the Goal 16 graph-`CZ` encoded bridge code: `m` left mouths, `m`
encoded right mouths, a mouth pairing `pi`, and a right-mouth graph interaction
`G`. The representative witness uses three mouths, path graph
`((0,1),(1,2))`, twisted pairing `(1,0,2)`, and right `[[5,1,3]]` code blocks.

The screen is a qutrit-erasure pair built from local tensor factors. A coin
source couples one recovered logical payload qubit to a north transfer tensor
or a south transfer tensor. There is no direct north/south tensor, no
separately declared screen router, and no externally inserted area bias.
Tracing out one screen derives the other screen's CPTP channel.

## Theorem-Style Result

**Intrinsic local screen theorem.** The star-local tensor network is an
isometry. Its north and south reduced channels are exact qutrit erasure
channels, with keep probabilities recovered from the local branch weight. The
same channel-derived probability determines recovery fidelity and the finite
quantum-area analogue, so their transition occurs at `p=1/2` without an
inserted area term.

**Bridge theorem inherited from Goal 16.** Full-block mutual information
recovers `pi`; Pauli-correlation tomography recovers `G`; conjugating by the
recovered `CZ_G` reconstructs the dressed observer algebra; inverse `CZ_G` plus
recovered routing restores exact bridge transfer.

**Combined theorem package.** Composing the graph-`CZ` bridge with the local
screen tensor network gives one finite dynamics family deriving the bridge
algebra, bridge channel, screen channels, and recovery/area transition.

## Representative Witness

| Diagnostic | Result |
| --- | --- |
| mouth map | `(1,0,2)` from full-block MI |
| interaction graph | `((0,1),(1,2))` from Pauli correlations |
| observer algebra | logical dimension `6`, symplectic rank `6`, center `0` |
| low-order entropy | aligned/twisted match through order `3` |
| low-order regions | `988` checked, `0` mismatches |
| first entropy split | order `4`, the decoder scale |
| state-derived bridge transfer | `3` logical qubits |
| wrong-mouth activation | `1` logical qubit |
| mouth-blind scrambling | `0` logical qubits |
| screen channels | exact erasure channels by partial trace |
| screen transition | south at `p=0`, tie at `p=0.5`, north at `p=1` |

## Controls

**Entropy-only control.** At `p=0.75`, north and south screen entropies tie
because `H(p)=H(1-p)`, but channel recovery favors north. Entropy alone cannot
orient the screen recovery.

**Static-state-only control.** Dropping the screen dynamics restores the no-go:
the same static bridge-state signature is compatible with opposite
north-favored and south-favored screen completions.

**External-area-bias control.** Adding an independent bare-area bias shifts the
area crossing to `0.375` while recovery remains at `0.5`, so the match is not
stable under geometry inserted outside the channel.

## Bounded Atlas

The executable atlas checks all simple graphs, all mouth permutations, and
screen probabilities `{0, 0.5, 1}` for `m <= 3`.

| `m` | Graphs | Pairings per Graph | Local Dynamics | Pairing | Graph | Transfer | Screen |
| --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | 1 | 1 | 3 | pass | pass | pass | pass |
| 2 | 2 | 2 | 12 | pass | pass | pass | pass |
| 3 | 8 | 6 | 144 | pass | pass | pass | pass |

## Claim Boundary

This is finite stabilizer/QEC mathematics plus exact dense-channel
verification. It is not a continuum ER=EPR theorem, not de Sitter physics, not
dS/CFT, and not a chaotic many-body wormhole. The useful claim is narrower:
within this finite benchmark, local channel structure can derive the screen
transition that entropy-only and static-state-only diagnostics cannot.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 18 local theorem certificate | `PYTHONPATH=. python3 -m qgtoy local-bridge-screen-dynamics --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Focused Goal 18 regression | `PYTHONPATH=. python3 -m unittest tests.test_local_bridge_screen` |
| JSON certificate index validation | `python3 -m json.tool docs/goal18_intrinsic_local_bridge_screen_dynamics_certificate_index.json` |
