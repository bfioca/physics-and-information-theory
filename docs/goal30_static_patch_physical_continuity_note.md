# Goal 30: Physical Static-Patch Continuity Gate

## Result

Goal 30 packages the post-Goal-29 obstruction as a finite theorem-style gate.
KMS/detailed balance, diagonal screen preservation, and finite thermal
correlation scale do not by themselves imply the vanishing cutoff-continuity
needed by the static-patch bridge benchmark. Goal 29's stationary modular
twirl and fixed-width modular noise remain counterexamples.

The sufficient replacement is:

```text
short_time_static_patch_locality
```

For a finite cutoff Hamiltonian `H_L`, if modular-time averaging is supported
in a window `r_L` with

```text
r_L max_gap(H_L) -> 0,
```

then the finite Schur channel is an approximate identity on the cutoff
spectrum. For heat/Euclidean regulators, the analogous condition is

```text
tau_L max_gap(H_L)^2 -> 0.
```

These assumptions mention modular-time localization, fuzzy-sphere locality,
or shrinking Euclidean cap thickness. They do not mention bridge algebra,
`M_N`, `C^N`, response gaps, or off-diagonal retention as inputs.

## Certified Routes

| Route | Status | Meaning |
| --- | --- | --- |
| KMS analyticity / detailed balance alone | refuted | stationary modular twirl still allowed |
| Thermal correlation decay without shrinking width | refuted | fixed-width modular noise need not approach identity |
| finite-lapse modular locality | sufficient | `r_L max_gap_L -> 0` gives approximate identity |
| fuzzy-sphere local heat scaling | sufficient | `tau_L max_gap_L^2 -> 0` gives approximate identity |
| shrinking Euclidean cap preparation | sufficient | CP/TP Schur-completed cap transfer remains continuous |
| observer-algebra limit continuity | conditional necessity | a noncommutative large-cutoff observer algebra needs a continuity gate |

## Boundary

This is a finite physical-continuity gate, not a continuum de Sitter theorem
and not a dS/CFT derivation. The result narrows the physics gap: the missing
principle is no longer generic KMS structure, but short-time static-patch
locality or an equivalent anti-tautological continuity condition.

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-physical-continuity --max-cutoff 5 --noise-strength 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

Run the focused regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_physical_continuity
```

Validate the machine-readable index:

```bash
python3 -m json.tool docs/goal30_static_patch_physical_continuity_certificate_index.json
```
