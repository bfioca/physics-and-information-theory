# Goal 3: Tensor-Network / Holographic-Code Result

## One-Pass Summary

Goal 3 found an exact finite holographic-code cousin of the Goal 1/2
balanced-bridge phenomenon. In the certified witness, two stabilizer
tensor-network code realizations have matching boundary-region entropy and the
same finite min-cut diagnostics, but they disagree on observer reconstruction
and erasure/channel semantics.

This is a finite theorem-style certificate, not an asymptotic holographic-code
classification.

## Objects And Diagnostics

The objects are finite stabilizer code pairs built from graph/CWS source codes,
literal stabilizer perfect-code blocks, Clifford/MERA-like circuit variants,
and declared finite tensor-network skeletons. The final witness uses the
`graph_cws_labeled_source_ord21_ord27` source pair, a `Y`-axis interface-star
outer layer, and an alternating Clifford/MERA-like outer variant.

Four diagnostics are kept separate:

| Diagnostic | Meaning in this package |
| --- | --- |
| Entropy-visible | Exact stabilizer subsystem entropy of a boundary region. |
| Min-cut-visible | Exact finite graph min-cut values, checked by exhaustive internal-node assignments over declared capacity profiles. |
| Reconstruction-visible | Exact region algebra / logical reconstruction diagnostics for the same boundary region. |
| Channel-visible | Exact erasure-correctability and survivor fixed-point/channel diagnostics. |

## Finite Theorem-Style Claim

Within the certified Phase 38/39 tensor-network layer, there exists a boundary
region where entropy-visible and min-cut-visible geometry agree, while
reconstruction-visible and channel-visible geometry split.

Final representative:

```text
source pair:   graph_cws_labeled_source_ord21_ord27
bridge axis:   Y
outer variant: alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root
region:        root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3
entropy pair:  (4,4)
min-cut values:(9,11,13,14,17,19)
split:         reconstruction-visible and channel-visible
```

Diagnostic outcome:

| Check | Outcome |
| --- | --- |
| Boundary-region entropy | Agrees: `(4,4)`. |
| Finite min-cut | Exact and capacity-sensitive: `(9,11,13,14,17,19)`. |
| Region algebra / reconstruction | Differs between the two code realizations. |
| Erasure / survivor channel semantics | Differs between the two code realizations. |

This satisfies the Goal 3 target: boundary entropy and min-cut diagnostics can
agree in a more holographic-looking finite tensor-network layer even when the
actual observer-accessible logical structure and channel semantics disagree.

## Evidence Layers

| Layer | Claim | Status | Certificate command |
| --- | --- | --- | --- |
| Exact theorem-style claim | The final representative satisfies the three-geometry separation: entropy/min-cut agree, reconstruction and channel semantics split. | Exact finite certificate | `python3 -m qgtoy holography-phase40` |
| Proof-obligation audit | Phase 40 records six proof obligations and all are satisfied. | Exact finite audit | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_holography_phase40_theorem_style_package_certificate` |
| Strict Phase 38 family | The q139 support-scale search finds 25 strict entropy/min-cut/operator hits, including 15 channel-visible hits. | Exhaustive bounded search for the declared Phase 38 family | `python3 -m qgtoy holography-phase38` |
| Phase 39 local robustness | The representative has 34 strict local-neighborhood hits among 52 checked deletion/addition/offset records. | Exhaustive bounded local-neighborhood audit | `python3 -m qgtoy holography-phase39` |
| Earlier Goal 3 search trail | CSS/stabilizer seeds, graph/CWS ring-spoke toys, Clifford/MERA-like circuits, perfect/HaPPY-like blocks, and chain/ring/tree tilings were explored with exact diagnostics inside their stated finite bounds. | Exploratory bounded evidence, exact only for searched records | `python3 -m qgtoy holography-phase1` through `python3 -m qgtoy holography-phase37` |

## Relation To Goals 1 And 2

Goal 1 proved the balanced-bridge CSS lesson: low-order entropy diagnostics can
match while reconstruction/algebra profiles differ. Goal 2 lifted that lesson
into finite causal-patch / horizon-code toy cosmologies, adding named patch
entropy, shared-horizon data, erasure semantics, and exact channel checks.

Goal 3 shows the same warning survives in a more holographic-looking finite
tensor-network setting. Entropy-visible and min-cut-visible data are still too
weak on their own; operator algebra, reconstruction, and channel diagnostics
remain essential.

## Conjectural Reading

The finite evidence suggests a broader conjecture: in holographic-code-like
finite QEC models, matching entanglement or min-cut summaries need not determine
observer-accessible bulk/logical geometry. Any robust geometry claim should be
tested against reconstruction and channel semantics, not entropy alone.

That conjectural reading is not part of the certified theorem. The certified
claim is the finite witness and its bounded family/local-neighborhood support.

## Why This Is Not Overclaimed

This package does not claim an asymptotic RT theorem, a universal
holographic-code classification, global minimality, all-axis robustness, or
exhaustion of every stabilizer/tensor-network family. The searches are exact
inside their declared finite bounds. Earlier phases are evidence-generating
scouts; the theorem-style claim rests on the Phase 38 strict family, the Phase
39 local-neighborhood audit, and the Phase 40 proof-obligation certificate.

## Reproduce The Final Package

| Major claim | Command |
| --- | --- |
| Strict Phase 38 family | `python3 -m qgtoy holography-phase38` |
| Representative and local-neighborhood robustness | `python3 -m qgtoy holography-phase39` |
| Final theorem-style certificate / proof-obligation map | `python3 -m qgtoy holography-phase40` |
| Focused proof-obligation regression test | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_holography_phase40_theorem_style_package_certificate` |

Supporting machine-readable index:

```text
docs/goal3_certificate_index.json
```
