# Goal 3 Phase 39: Compact Holographic-Cousin Witness

## Claim

There is a finite stabilizer tensor-network / holographic-code witness where
entropy and min-cut diagnostics agree on a boundary region, but observer
reconstruction and channel semantics differ.

This is a bounded exact certificate, not an asymptotic theorem. The certified
scope is the Phase 39 representative and its declared local neighborhood.

## Representative

```text
source pair:       graph_cws_labeled_source_ord21_ord27
bridge axis:       Y
outer variant:     alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root
base region:       root_shell_plus_edge_0_minus_q139
added leaf qubits: q0, q3
region length:     27
```

The exact diagnostics are:

```text
entropy pair:      (4,4)
min-cut values:    (9,11,13,14,17,19)
min-cut variable:  true
reconstruction split: true
channel split:        true
```

Thus the entropy/min-cut-visible geometry agrees, while both
observer-reconstruction-visible and channel-visible geometry separate.

## Robustness

Phase 39 audits 52 local neighbors:

```text
same-leaf offset alternatives:       6 records,  1 strict hit
single-qubit deletions:             27 records, 15 strict hits
bounded local single additions:     19 records, 18 strict hits
neighborhood strict hits:           34
```

The offset pair `(0,3)` is unique among the six same-leaf private offset pairs.
The representative is not locally minimal: strict channel-visible hits persist
under many one-qubit deletions and bounded local additions.

## Reproducibility

```bash
python3 -m qgtoy holography-phase39
python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_holography_phase39_representative_witness_robustness_certificate
```

The machine certificate records the full stabilizer, min-cut, reconstruction,
erasure, and survivor diagnostics for the representative and neighborhood.
