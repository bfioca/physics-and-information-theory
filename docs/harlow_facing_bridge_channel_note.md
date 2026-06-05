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

The benchmark arc has four finite pieces.

| Layer | Finite statement | Main diagnostic split |
| --- | --- | --- |
| Observer-algebra tomography | Finite stabilizer/OA-QEC shadows form a strict hierarchy; weak entropy/channel data do not determine observer algebras, while richer response/commutator data can recover the finite algebraic signature. | entropy/channel-visible vs reconstruction-visible |
| Encoded mouths | Right mouths are encoded in independent `[[5,1,3]]` blocks; low-order physical entropy through the code distance is blind to the logical mouth pairing. | low-order entropy-visible vs decoder/channel-visible |
| Bridge controls | Algebra-aware Clifford and `T`-dressed activations transfer to the algebraically correct mouth; wrong-mouth and mouth-blind Pauli-twirled controls fail. | generic resource-visible vs coupling/channel-visible |
| Static-patch bilayer substrate | A coherent two-screen erasure model gives explicit north/south recovery channels and an exact symmetric recovery/quantum-area-analogue crossing, plus a no-go for independent area bias. | recovery-visible vs inserted-geometry-visible |

The strongest exact benchmark theorem currently packaged is the Goal 13 control
certificate. In the encoded-mouth family, aligned and twisted resources have
matching coarse entropy/min-cut data and matching labeled physical entropy
through order `3`, but identity activation has different named-mouth transfer.
Algebra-aware activation restores full transfer, including after a non-Clifford
logical `T` layer, while a mouth-blind Pauli-twirled scrambling proxy has zero
structured named-mouth transfer.

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

## Best next theorem target

The next research goal should remove the remaining inserted data:

```text
Goal 14: State-Derived Bridge Dynamics

Replace hand-declared bridge maps and routing parameters with state-derived
finite dynamics. Build finite QEC/stabilizer/tensor-network models where the
bridge-channel map, screen recovery transition, and entropy/area analogue are
computed from one shared state or circuit, not inserted as separate inputs.
Test whether algebraic connectivity predicts transfer while entropy/min-cut
shadows remain incomplete. Produce exact certificates, wrong-mouth controls,
scrambling controls, and a Harlow-facing theorem note.
```

Success would not prove ER=EPR in de Sitter. It would produce a more serious
finite theorem program: a controlled model where the observer algebra, bridge
channel, and area-like transition are mutually derived rather than separately
declared.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 11 encoded-mouth entropy blindness | `PYTHONPATH=. python3 -m qgtoy er-epr-encoded --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 12 coupling-activated transfer | `PYTHONPATH=. python3 -m qgtoy er-epr-traversable --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 13 non-Clifford/scrambling controls | `PYTHONPATH=. python3 -m qgtoy bridge-channel-controls --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Static-patch bilayer certificate | `PYTHONPATH=. python3 -m qgtoy bilayer-program` |
| Focused merged regression slice | `PYTHONPATH=. python3 -m unittest tests.test_bilayer tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal11_encoded_mouth_bridge_channel_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal12_finite_bridge_channel_dynamics_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal13_non_clifford_scrambling_bridge_controls_certificate` |
