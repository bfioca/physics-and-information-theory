# Goals 1-3 Program Memo

## Program Arc

This program builds a sequence of exact finite QEC diagnostics showing that
entropy-like data can agree while observer-accessible logical structure differs.
Goal 1 proves the seed CSS family. Goal 2 turns it into finite causal-patch /
horizon-code toy cosmologies with named observer and horizon regions. Goal 3
extends the lesson to tensor-network / holographic-code-like constructions with
finite min-cut checks.

| Goal | Result | Status |
| --- | --- | --- |
| Goal 1 | Balanced-bridge CSS pairs `A_m,B_m` have matching labeled one- and two-qubit entropy diagnostics, but different logical reconstruction/algebra profiles. | Exact theorem-style family claim plus finite-prefix audits. |
| Goal 2 | Finite causal-patch / horizon-code toy cosmologies can match named patch entropy, overlap, MI/CMI/I3, and shared-horizon-visible data while observer-patch reconstructability, erasure semantics, and channel behavior differ. | Exact finite certificates plus exhaustive bounded searches. |
| Goal 3 | Tensor-network / holographic-code-like pairs can match boundary-region entropy and finite min-cut diagnostics while reconstruction-visible and channel-visible geometry differ. | Exact finite theorem-style certificate plus bounded family/local-neighborhood support. |

## Glossary

| Term | Meaning |
| --- | --- |
| Entropy-visible | Exact stabilizer subsystem entropy data for selected qubit regions. |
| Min-cut-visible | Exact finite graph min-cut values over declared tensor-network skeletons and capacity profiles. |
| Reconstruction-visible | Region algebra and logical reconstruction diagnostics: which logical operators a region can access. |
| Channel-visible | Erasure-correctability, survivor fixed-point, and transition/channel diagnostics. |
| Observer algebra | The logical algebra available to a named observer patch, summarized by signatures such as `(logical_dim, center_dim, commutant_dim, reconstructs_all)`. |
| Shared horizon | A named overlap/horizon region whose entropy and algebra are held fixed in the causal-patch comparison. |
| Strict causal-patch gate | The Goal 2 acceptance gate requiring matched entropy/overlap data, matched shared-horizon semantics, an observer reconstruction split, and the requested erasure/channel constraints. |
| Survivor fixed point | Whether the complement that survives an erasure reconstructs all logical information, used as a channel-visible semantic check. |

## Exact Theorem-Style Claims

**Goal 1: balanced-bridge CSS theorem.** Starting from the `n=6` CSS seed pair,
append bridge pairs `p_j,q_j` and the same two bridge checks to both codes:

```text
Z_1 Z_2 Z_{p_j} Z_{q_j}
X_0 X_5 X_{p_j} X_{q_j}
```

For all bridge counts `m`, the resulting CSS pair has `n=6+2m`, `k=1`, `d=2`,
matching labeled one- and two-qubit entropy diagnostics, no single-qubit
non-central logical reconstruction, and different reconstruction/algebra
profiles. The separating region is
`R_m={1,2,3} union {p_j : 0 <= j < m}`.

**Goal 2: finite causal-patch / horizon-code certificates.** The balanced-bridge
phenomenon persists after naming observer patches, shared horizons, bridge
shells, and static diamonds. Exact finite certificates show that patch entropy,
overlap, MI/CMI/I3, and shared-horizon-visible data can match while observer
reconstruction, erasure semantics, survivor fixed points, and channel behavior
separate.

**Goal 3: finite holographic-code cousin.** In the Phase 38/39 tensor-network
layer, the final representative witness is:

```text
source pair:   graph_cws_labeled_source_ord21_ord27
bridge axis:   Y
outer variant: alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root
region:        root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3
entropy pair:  (4,4)
min-cut values:(9,11,13,14,17,19)
split:         reconstruction-visible and channel-visible
```

Thus boundary-region entropy and finite min-cut diagnostics agree, while the
observer-accessible region algebra and erasure/channel semantics differ.

## Exhaustive Bounded-Search Evidence

Goal 2 contains exact bounded searches over cover families, repaired
graph/CWS-like sources, transition graphs, and finite channel-rule languages.
The sharpest final audit is the Phase 31 strict-cover search: among 175 repaired
covers, it finds 66 raw hits, 8 strict hits, and 58 erasure-gate rejections,
separating tempting entropy near-misses from strict causal-patch examples.

Goal 3 contains two final bounded audits supporting the theorem-style witness.
Phase 38 exhausts the declared q139 support-scale family: 1650 candidate support
records give 25 admissible entropy/min-cut/operator hits, including 15
channel-visible hits. Phase 39 audits the representative local neighborhood:
34 of 52 deletion/addition/offset records remain strict channel-visible hits.

## Exploratory Bounded Evidence

Earlier Goal 2 phases explore source-aware covers, repaired non-CSS atlases,
mixed transition graphs, and rule/substrate co-design. These searches are exact
for the records they enumerate, but they are not theorems over all possible
cover grammars or channel rules.

Earlier Goal 3 phases explore CSS/stabilizer tensor-network seeds, graph/CWS
ring-spoke toys, Clifford/MERA-like circuits, perfect/HaPPY-like blocks, and
chain/ring/tree tiling toy networks. These phases helped locate the final
q139 support surface and should be read as bounded exploratory evidence, not as
classification results for all tensor-network codes.

## Scientific Interpretation

Across all three goals, the same structural lesson survives increasingly
geometric wrappers: entropy-visible summaries, even supplemented by finite
min-cut data or named horizon entropies, do not determine observer-accessible
logical geometry. Reconstruction algebra, erasure behavior, survivor fixed
points, and channel semantics are independent diagnostics that can split when
entropy-like data agree. The finite examples therefore support a disciplined
QEC-cosmology heuristic: geometry-like claims should be certified by operator
and channel semantics, not inferred from entanglement summaries alone.

## Limitations

These are finite stabilizer, CSS, graph/CWS, and tensor-network-like toy
models, mostly with `k=1`. The Goal 1 theorem is all-`m` only for one
balanced-bridge generator family. Goal 2 exhaustive claims are limited to their
declared cover families, transition graphs, substrates, and rule languages.
Goal 3 certifies one finite holographic-code-like witness with bounded family
and local-neighborhood support; it does not prove an asymptotic RT theorem,
global minimality, all-axis robustness, or a universal holographic-code
classification. Cosmology, horizon, and holography language is diagnostic, not
a claim that the qubit regions are literal spacetime regions.

## Reproducibility Table

| Major claim | Evidence class | CLI command |
| --- | --- | --- |
| Goal 1 symbolic balanced-bridge theorem | Exact theorem-style claim | `python3 -m qgtoy bridge-proof-check` |
| Goal 1 theorem package with finite-prefix audit | Exact theorem-style claim | `python3 -m qgtoy bridge-theorem --max-exact-steps 3` |
| Goal 1 bridge-family prefix replay | Exact finite-prefix audit | `python3 -m qgtoy bridge-family --max-steps 3` |
| Goal 2 static causal-patch atlas | Exact finite certificate | `python3 -m qgtoy cosmology-phase1 --max-m 3` |
| Goal 2 bridge growth and erasure channels | Exact finite certificate | `python3 -m qgtoy cosmology-phase2 --max-m 3` |
| Goal 2 repaired strict atlas | Exhaustive bounded-search evidence | `python3 -m qgtoy cosmology-phase12` |
| Goal 2 robust channel synthesis | Exhaustive bounded-search evidence | `python3 -m qgtoy cosmology-phase27` |
| Goal 2 strict-cover exhaustive audit | Exhaustive bounded-search evidence | `python3 -m qgtoy cosmology-phase31` |
| Goal 3 strict q139 support family | Exhaustive bounded-search evidence | `python3 -m qgtoy holography-phase38` |
| Goal 3 representative local robustness | Exhaustive bounded-search evidence | `python3 -m qgtoy holography-phase39` |
| Goal 3 final theorem-style holographic cousin | Exact finite certificate | `python3 -m qgtoy holography-phase40` |
| Goal 3 focused proof-obligation regression | Exact finite audit | `python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_holography_phase40_theorem_style_package_certificate` |

## Next Research Directions

1. Higher-distance analogues: search for versions with stronger distance,
   erasure thresholds, or multi-logical-code structure while preserving exact
   entropy, reconstruction, and channel diagnostics.
2. Asymptotic/family strengthening: turn finite witnesses into parameterized
   families, or prove no-go/yes-go theorems for restricted holographic-code-like
   grammars.
3. Paper-style formalization: extract the definitions, theorem statements,
   bounded-search certificates, and proof obligations into a compact formal
   appendix suitable for technical review.
