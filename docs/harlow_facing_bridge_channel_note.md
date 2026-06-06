# Finite Bridge-Channel Benchmarks For Algebraic ER=EPR Diagnostics

## One-line pitch

Engelhardt and Liu propose that ER=EPR connectivity should be associated with
operator-algebraic structure, not merely with the amount of entanglement. This
repository supplies a finite stabilizer/QEC benchmark layer for that idea:
exact bridge-channel certificates where entropy and min-cut shadows can be
blind to the named channel, while algebraic decoding and coupling data predict
the operational transfer.

## Claim boundary

This is not a new definition of algebraic ER=EPR, not a continuum-gravity
theorem, and not a de Sitter construction. It is a finite research-code
laboratory for asking which diagnostics determine observer reconstruction and
bridge-channel behavior.

The safe technical claim is:

```text
finite entropy/min-cut shadows can be incomplete;
operator-algebraic data can be necessary to predict reconstruction or channel behavior.
```

## Result spine

The benchmark arc has seven finite pieces.

| Layer | Finite statement | Main diagnostic split |
| --- | --- | --- |
| Observer-algebra tomography | Finite stabilizer/OA-QEC shadows form a strict hierarchy; weak entropy/channel data do not determine observer algebras, while richer response/commutator data can recover the finite algebraic signature. | entropy/channel-visible vs reconstruction-visible |
| Encoded mouths | Right mouths are encoded in independent `[[5,1,3]]` blocks; low-order physical entropy through the code distance is blind to the logical mouth pairing. | low-order entropy-visible vs decoder/channel-visible |
| Bridge controls | Algebra-aware Clifford and `T`-dressed activations transfer to the algebraically correct mouth; wrong-mouth and mouth-blind Pauli-twirled controls fail. | generic resource-visible vs coupling/channel-visible |
| State-derived dynamics | The mouth map is inferred from the encoded resource state, and the north/south recovery transition is inferred from induced screen channels. | low-order entropy-visible vs state/channel-visible |
| Interacting bridge theorem | Logical-`CZ` dressing makes the bridge resource non-product; the state determines observer algebra and mouth map, while a static-state no-go isolates the need for screen dynamics. | interacting-state-visible vs static-transition-visible |
| Interacting bridge code theorem | For arbitrary right-mouth graph-`CZ` interactions, pairwise inter-bridge MI fails as a graph reader, but state-derived Pauli-correlation tomography recovers the graph, observer algebra, and exact transfer. | weak correlation-visible vs Pauli-correlation/algebra-visible |
| Static-patch bilayer substrate | A coherent two-screen erasure model gives explicit north/south recovery channels and an exact symmetric recovery/quantum-area-analogue crossing, plus a no-go for independent area bias. | recovery-visible vs inserted-geometry-visible |

The strongest exact benchmark theorem currently packaged is Goal 16. It turns
the interacting bridge into an arbitrary graph-`CZ` code-family statement:
full-block MI recovers the mouth map, Pauli-correlation tomography recovers the
interaction graph, and inverse interaction plus inferred routing restores
exact transfer. It also records a useful no-go: pairwise inter-bridge MI already
fails as an arbitrary graph reader at `m=3`.

## What is standard vs new here

Standard ingredients include stabilizer codes, logical Bell pairs, stabilizer
distance, Pauli transfer matrices, Choi/Kraus checks, teleportation through Bell
resources, OA-QEC language, and the known lesson that algebraic reconstruction
is the right language for holographic QEC.

The nonstandard contribution is the exact finite benchmark package: a linked
set of certificates comparing entropy shadows, low-order physical entropy,
logical mouth maps, explicit bridge activations, wrong-mouth controls,
non-Clifford channel signatures, and scrambling controls under the same finite
QEC bookkeeping. The goal is not to replace the Engelhardt-Liu conceptual
proposal, but to make a small operational testbed under it.

## Why this may be useful

The finite examples isolate a sharp operational question:

```text
What data available to an observer determine the observer's accessible algebra
and the bridge channel it can activate?
```

Entropy alone is too coarse in these benchmarks. Labeled logical access is too
privileged for a gravity-like observer. The useful middle ground is intrinsic
physical response plus commutator/channel tomography: enough operational data
to recover a finite observer algebra without pretending that a full continuum
geometry has been derived.

## Static-patch bilayer next step

The bilayer program is the current route back toward an ER=EPR-in-dS question.
It introduces two finite observer screens, north and south, and asks whether a
bulk algebra is reconstructible from the north screen, the south screen, both,
or neither. The implemented coherent routing model derives complementary
screen erasure channels from one isometry and verifies an exact symmetric match
between:

- the recovery-fidelity transition; and
- a state-derived quantum-area analogue using reduced screen entropies.

It also records a no-go: adding an independent bare-area bias shifts the
quantum-area crossing without shifting the recovery crossing. A real de
Sitter-like theorem must derive both the recovery channel and the area
competition from one controlled static-patch construction.

## Goal 15-16 update

Goal 15 adds the first non-product interacting bridge theorem in this sequence.
The right encoded mouths are dressed by a logical `CZ` interaction graph. The
resulting stabilizer state is not a tensor product of independent bridges:
full-block mutual information infers the mouth map, and the dressed observer
algebra is computed by conjugating the right logical algebra through the
inferred graph.

The positive theorem says that the state-derived decoder, which removes the
inferred interaction and routes by the inferred mouth map, restores exact
transfer while wrong-mouth and mouth-blind controls fail. The no-go theorem says
the same static state does not determine a north/south recovery transition:
opposite screen-channel completions have the same static state signature. The
minimal missing ingredient is an explicit screen dynamics/isometry.

Goal 16 fixes the arbitrary-graph diagnostic layer. Pairwise inter-bridge
mutual information is certified insufficient: for `m=3`, a path/star graph can
look like a triangle to pairwise MI. The theorem-family reader is instead a
state-derived Pauli-correlation protocol: for each paired bridge, solve for the
unique product of right logical `Zbar` operators that turns `X_L Xbar` into a
state stabilizer. That unique dressing recovers the right-mouth graph `G`, and
therefore the dressed observer algebra and inverse-interaction channel decoder.

The remaining next theorem target is to make that screen isometry inseparable
from the bridge dynamics:

```text
Next target: inseparable interacting bridge/screen dynamics

Replace the logical-CZ bridge dressing plus separate screen-isometry completion
with one finite interacting circuit or tensor network whose bridge transfer,
observer algebra, and screen recovery transition are all outputs of the same
non-product dynamics.
```

Success would still not prove ER=EPR in de Sitter, but it would move the finite
benchmark from an interacting bridge theorem plus transition no-go to a fully
inseparable bridge/screen dynamics theorem.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 11 encoded-mouth entropy blindness | `PYTHONPATH=. python3 -m qgtoy er-epr-encoded --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 12 coupling-activated transfer | `PYTHONPATH=. python3 -m qgtoy er-epr-traversable --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 13 non-Clifford/scrambling controls | `PYTHONPATH=. python3 -m qgtoy bridge-channel-controls --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 14 state-derived bridge dynamics | `PYTHONPATH=. python3 -m qgtoy state-bridge-dynamics --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 15 interacting bridge theorem | `PYTHONPATH=. python3 -m qgtoy interacting-bridge-theorem --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 16 interacting bridge code theorem | `PYTHONPATH=. python3 -m qgtoy interacting-bridge-code-theorem --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Static-patch bilayer certificate | `PYTHONPATH=. python3 -m qgtoy bilayer-program` |
| Focused merged regression slice | `PYTHONPATH=. python3 -m unittest tests.test_bilayer tests.test_state_bridge tests.test_interacting_bridge tests.test_interacting_bridge_code_theorem tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal11_encoded_mouth_bridge_channel_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal12_finite_bridge_channel_dynamics_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal13_non_clifford_scrambling_bridge_controls_certificate` |
