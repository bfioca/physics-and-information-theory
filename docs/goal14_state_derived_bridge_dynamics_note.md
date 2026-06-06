# Goal 14: State-Derived Bridge Dynamics

Goal 14 removes one important shortcut from the finite bridge-channel
benchmarks. Earlier certificates could compare algebra-aware and wrong-mouth
controls, but the mouth map or routing parameter was still handed to the
protocol as declared data. Goal 14 asks what can be read from the finite state
or channel itself.

## Exact Result

The representative model has two ingredients in one finite certificate:

- an encoded-mouth stabilizer resource with left mouths `L_i` and right mouths
  encoded in independent `[[5,1,3]]` blocks `B_j`;
- a coherent two-screen routing isometry whose induced north/south screen
  channels determine the recovery transition.

The logical mouth map is inferred from the resource state: for each `L_i`, the
certificate chooses the unique block `B_j` maximizing `I(L_i:B_j)` at full
encoded-block scale. The screen routing probability is inferred from the
induced screen channel by measuring the channel's non-erasure success
probability. Neither quantity is handed to the decoder as an external
diagnostic.

**Theorem-style claim.** In the encoded-mouth family, the full encoded resource
state determines the logical mouth map by block mutual information, while
low-order physical entropy through the code distance remains blind to that map.
Activating the state-derived mouth map restores exact transfer; identity,
wrong-mouth, and mouth-blind scrambling controls fail. In the same finite
circuit layer, screen success probabilities read from coherent routing channels
determine both recovery ordering and the equal-area entropy/area analogue
transition.

## Representative Witness

For two mouths, aligned and twisted resources still have matching coarse
entropy/min-cut shadows and matching labeled physical entropy through order
`3`. The first entropy mismatch is at order `4`, the decoder scale of the
distance-3 right blocks.

| Diagnostic | Aligned | Twisted |
| --- | ---: | ---: |
| low-order physical entropy through order 3 | same | same |
| state-derived pairing | `(0,1)` | `(1,0)` |
| identity activation capacity | 2 | 0 |
| state-derived Clifford activation capacity | 2 | 2 |
| state-derived `T`-dressed capacity | 2 | 2 |
| mouth-blind scrambling capacity | 0 | 0 |

The explicit dense channel certificate verifies that identity activation on
the twisted state is the wrong-mouth channel, while activation by the inferred
pairing is rank-1 identity transfer.

## Screen Transition

For the coherent two-screen isometry, the certificate reads `p` from the north
screen channel itself. It then computes:

- north and south recovery fidelities;
- north and south screen entropies;
- the equal-bare-area entropy/area analogue.

The recovery winner and larger entropy/area-analogue screen agree for
`p=0,0.25,0.5,0.75,1`. At `p=0.5` both tie. Adding an external bare-area bias
that is not encoded in the state/channel shifts the area crossing but not the
recovery crossing; this is recorded as a finite no-go.

## Limitations

This is still finite stabilizer/QEC mathematics with small dense-channel
checks. The resource family is a finite ansatz, the block mutual-information
probe is decoder-scale data, and the area term is state-derived only in the
equal-bare-area analogue. The certificate does not prove continuum ER=EPR, de
Sitter physics, dS/CFT, or chaotic many-body traversability.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 14 state-derived certificate | `PYTHONPATH=. python3 -m qgtoy state-bridge-dynamics --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Focused Goal 14 regression | `PYTHONPATH=. python3 -m unittest tests.test_state_bridge` |
| JSON certificate index validation | `python3 -m json.tool docs/goal14_state_derived_bridge_dynamics_certificate_index.json` |
