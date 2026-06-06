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

The benchmark arc now has a theorem target above the finite bridge-screen stack.

| Layer | Finite statement | Main diagnostic split |
| --- | --- | --- |
| Observer-algebra tomography | Finite stabilizer/OA-QEC shadows form a strict hierarchy; weak entropy/channel data do not determine observer algebras, while richer response/commutator data can recover the finite algebraic signature. | entropy/channel-visible vs reconstruction-visible |
| Encoded mouths | Right mouths are encoded in independent `[[5,1,3]]` blocks; low-order physical entropy through the code distance is blind to the logical mouth pairing. | low-order entropy-visible vs decoder/channel-visible |
| Bridge controls | Algebra-aware Clifford and `T`-dressed activations transfer to the algebraically correct mouth; wrong-mouth and mouth-blind Pauli-twirled controls fail. | generic resource-visible vs coupling/channel-visible |
| State-derived dynamics | The mouth map is inferred from the encoded resource state, and the north/south recovery transition is inferred from induced screen channels. | low-order entropy-visible vs state/channel-visible |
| Interacting bridge theorem | Logical-`CZ` dressing makes the bridge resource non-product; the state determines observer algebra and mouth map, while a static-state no-go isolates the need for screen dynamics. | interacting-state-visible vs static-transition-visible |
| Interacting bridge code theorem | For arbitrary right-mouth graph-`CZ` interactions, pairwise inter-bridge MI fails as a graph reader, but state-derived Pauli-correlation tomography recovers the graph, observer algebra, and exact transfer. | weak correlation-visible vs Pauli-correlation/algebra-visible |
| Inseparable bridge-screen dynamics | The graph-`CZ` bridge and north/south screen router are one declared finite dynamics family; the same record derives the bridge algebra, bridge channel, screen channels, and recovery/area-analogue transition. | static-state-visible vs unified-dynamics-visible |
| Intrinsic local bridge-screen dynamics | The declared screen router is replaced by a star-local tensor network; screen channels and the recovery/area transition are derived by partial trace from local transfer tensors. | declared-router-visible vs local-channel-visible |
| Relative-entropy observer-bridge theorem | Exact finite-dimensional observer-bridge reconstruction is formulated through relative-entropy preservation, not labeled logical probes or supplied product tables. | static entropy-visible vs distinguishability/recovery-visible |
| Algebraic connectivity order parameter | Noisy finite bridge channels are classified by approximate recoverable observer algebra: relative-entropy response plus product/commutator closure separates quantum, classical, and null phases. | static entropy-visible vs algebraic-connectivity-visible |
| Static-patch bilayer substrate | A coherent two-screen erasure model gives explicit north/south recovery channels and an exact symmetric recovery/quantum-area-analogue crossing, plus a no-go for independent area bias. | recovery-visible vs inserted-geometry-visible |

The strongest finite bridge-screen certificate currently packaged is Goal 18.
The more ambitious theorem target above it is the relative-entropy
observer-bridge statement: in exact finite dimension, the observer algebra is
the algebra whose state-space distinguishability is preserved by the region
channel, and the transferred bridge algebra is the largest algebra preserved by
the composed observer-to-observer channel. Goal 19 turns that statement into a
finite noisy order parameter for Pauli-diagonal bridges.

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

Goal 16 still left the screen dynamics as a separate completion. Goal 17 below
packages the bridge and screen in one declared dynamics family. Goal 18 then
removes the declared screen-router layer by deriving the screen channels from a
star-local tensor network.

## Goal 17 update

Goal 17 implements that next target in the finite benchmark setting. The
declared dynamics record has one shared `dynamics_id` for:

- encoded bridge preparation;
- right-mouth graph-`CZ` interaction;
- inferred inverse interaction plus inferred mouth routing;
- coherent north/south qutrit-erasure screen routing.

The certificate verifies that full-block MI recovers `pi`, Pauli-correlation
tomography recovers `G`, the dressed observer algebra is reconstructed, and the
state-derived bridge decoder restores exact transfer. It then traces the same
declared screen router to obtain north/south channels; their Kraus operators
give the keep probabilities, recovery fidelities, and finite quantum-area
analogue. The transition is therefore derived from the unified channel data,
not appended to a static bridge state.

Controls still matter. If the screen layer is dropped, the static-state-only
no-go returns: opposite screen-channel completions share the same bridge
signature. If an external bare-area bias is appended after the channel is
fixed, the area crossing shifts while the recovery crossing does not.

## Goal 18 update

Goal 18 replaces the explicit screen router with local tensor factors. A coin
source and independent north/south transfer tensors define a star-local
isometry for one recovered logical payload qubit. There is no direct
north/south tensor, no separately declared screen recovery isometry, and no
external area bias. The north and south screen channels are obtained by partial
trace and are verified to be exact qutrit erasure channels.

The representative witness keeps the three-mouth path graph, twisted pairing
`(1,0,2)`, and `[[5,1,3]]` right blocks. It recovers `pi`, `G`, the dressed
observer algebra, and exact bridge transfer as before. The new screen theorem
checks that local branch probability is recovered from the reduced channels,
that recovery fidelity and the finite quantum-area analogue transition together
at `p=1/2`, and that entropy-only data cannot orient the transition: at
`p=0.75`, north and south screen entropies tie while channel recovery favors
north.

The useful claim is therefore finite and operational: local channel structure,
not entropy alone and not a static bridge state alone, determines the oriented
screen recovery in this benchmark.

## Major theorem target

The next theorem layer replaces stabilizer-specific Pauli response with
relative-entropy response. For a finite-dimensional region channel `N_R`,
relative-entropy preservation on an algebra's full-rank state pairs is
equivalent, by Petz/OAQEC recovery, to exact reconstructability of that algebra
on `R`. For bridge dynamics, the composed channel selects the transferred
observer algebra by the same criterion.

This is not advertised as a new Petz theorem. The contribution is the
observer-bridge diagnostic packaging: entropy/static shadows can agree while
relative-entropy response separates quantum, classical, and null observer
bridges. It is also the cleanest route from the finite stabilizer certificates
toward the Harlow-adjacent question: what operational data specify an
observer's effective algebra and channel?

## Goal 19 update

Goal 19 defines a finite noisy order parameter:

```text
algebraic connectivity = approximate recoverable observer algebra.
```

For one-qubit Pauli-diagonal bridge channels, it probes full-rank antipodal
states along `X`, `Y`, and `Z`, records relative-entropy defects, and checks
product/commutator closure. With `r=0.5` and `epsilon=0.25`, the stability
bound gives an axis-shrink lower bound `0.839956192704`, an average-gate-fidelity
lower bound `0.919978096352`, and a product/commutator-defect upper bound
`0.294473594339`.

The certificate separates finite noisy phases:

- clean and stable noisy quantum bridges;
- classical `Z` bridge;
- null depolarizing bridge.

All have the same maximally mixed static entropy shadow `(1,1)`. The certificate
also records a response-only no-go: at a coarser tolerance, a physical Pauli
channel can preserve two noncommuting probes while missing their commutator
axis, so response data must include product/commutator closure to define an
algebra.

This is still finite and Pauli-diagonal. The next true lift is a general
finite-dimensional OA-QEC stability theorem beyond Pauli channels, with
dimension/error constants and a many-body simulation signature.

## Reproducibility

| Claim | Command |
| --- | --- |
| Goal 11 encoded-mouth entropy blindness | `PYTHONPATH=. python3 -m qgtoy er-epr-encoded --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 12 coupling-activated transfer | `PYTHONPATH=. python3 -m qgtoy er-epr-traversable --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 13 non-Clifford/scrambling controls | `PYTHONPATH=. python3 -m qgtoy bridge-channel-controls --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 14 state-derived bridge dynamics | `PYTHONPATH=. python3 -m qgtoy state-bridge-dynamics --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 15 interacting bridge theorem | `PYTHONPATH=. python3 -m qgtoy interacting-bridge-theorem --mouths 2 --low-order 3 --atlas-max-mouths 3` |
| Goal 16 interacting bridge code theorem | `PYTHONPATH=. python3 -m qgtoy interacting-bridge-code-theorem --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Goal 17 inseparable bridge-screen dynamics | `PYTHONPATH=. python3 -m qgtoy bridge-screen-dynamics --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Goal 18 intrinsic local bridge-screen dynamics | `PYTHONPATH=. python3 -m qgtoy local-bridge-screen-dynamics --mouths 3 --low-order 3 --atlas-max-mouths 3` |
| Relative-entropy observer-bridge theorem | `PYTHONPATH=. python3 -m qgtoy relative-entropy-bridge-theorem` |
| Goal 19 algebraic connectivity order parameter | `PYTHONPATH=. python3 -m qgtoy algebraic-connectivity-order` |
| Static-patch bilayer certificate | `PYTHONPATH=. python3 -m qgtoy bilayer-program` |
| Focused merged regression slice | `PYTHONPATH=. python3 -m unittest tests.test_bilayer tests.test_state_bridge tests.test_interacting_bridge tests.test_interacting_bridge_code_theorem tests.test_bridge_screen_dynamics tests.test_local_bridge_screen tests.test_relative_entropy_bridge tests.test_algebraic_connectivity tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal11_encoded_mouth_bridge_channel_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal12_finite_bridge_channel_dynamics_certificate tests.test_stabilizer.StabilizerDiagnosticsTest.test_goal13_non_clifford_scrambling_bridge_controls_certificate` |
