# Goal 3 Phase 40: Theorem-Style Holographic-Cousin Package

## Finite Claim

Within the certified finite Phase 38/39 tensor-network layer, there is a
boundary region whose entropy and min-cut diagnostics agree for two stabilizer
codes, while observer reconstruction and channel diagnostics differ.

This is a finite exact witness package. It does not claim an asymptotic theorem,
global minimality, all-axis robustness, or a universal holographic-code
classification.

## Witness Index

```text
identifier:    goal3_phase40_graph_cws_21_27_y_alternating_offset0_q139_leaf0_offsets_0_3
source pair:   graph_cws_labeled_source_ord21_ord27
bridge axis:   Y
outer variant: alternating_disentangler_isometry__flip_offset_0_to_leaf_to_root
region:        root_shell_plus_edge_0_minus_q139__phase38_same_leaf_add_q0_q3
entropy pair:  (4,4)
min-cut values:(9,11,13,14,17,19)
```

The representative satisfies all three proof obligations:

```text
entropy/min-cut-visible geometry: entropy matches and min-cut is exact/capacity-sensitive
observer-visible geometry:       reconstruction/operator algebra differs
channel-visible geometry:        erasure/survivor channel semantics differ
```

## Supporting Certificates

Phase 38 certifies the strict-hit family:

```text
candidate q139 support records: 1650
strict admissible hits:           25
channel-visible hits:             15
operator-only hits:               10
```

Phase 39 certifies the representative local plateau:

```text
representative region length: 27
neighborhood records:        52
neighborhood strict hits:    34
single-deletion hits:        15
local-addition hits:         18
```

## Reproducibility

```bash
python3 -m qgtoy holography-phase38
python3 -m qgtoy holography-phase39
python3 -m qgtoy holography-phase40
python3 -m unittest tests.test_stabilizer.StabilizerDiagnosticsTest.test_holography_phase40_theorem_style_package_certificate
```

The Phase 40 machine certificate records the compact proof-obligation map and
points back to the larger Phase 38 and Phase 39 certificates for full exact
diagnostics.
