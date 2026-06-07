# Goal 31: Static-Patch Strong-Continuity Theorem Gate

## Result

Goal 31 refines the Goal 30 continuity assumption into a standard finite
semigroup condition. For each cutoff `L`, suppose the static-patch channel is
an identity-starting, strongly continuous finite semigroup

```text
Lambda_L(delta)=exp(delta G_L)
```

with generator norm bounded by `Gamma_L`. Then

```text
||Lambda_L(delta_L)-id|| <= exp(delta_L Gamma_L)-1.
```

Therefore any cutoff-compatible lapse satisfying

```text
delta_L Gamma_L -> 0
```

derives the `modular_time_approximate_identity` gate.

## No-Go Side

KMS/detailed balance still does not imply this. The stationary modular twirl is
KMS-compatible but is not an identity-starting strongly continuous finite-time
dynamics: it jumps by norm one on a matrix-unit coherence witness. Fixed-time
thermalization is also insufficient: a semigroup can be strongly continuous at
each finite cutoff but fail the large-cutoff approximate-identity gate if the
physical lapse does not shrink against the generator norm.

## Positive Side

The finite theorem covers three anti-tautological routes:

| Route | Generator/lapse condition | Status |
| --- | --- | --- |
| local modular evolution | `delta_L max_gap(H_L) -> 0` | sufficient |
| fuzzy-sphere heat flow | `tau_L max_gap(H_L)^2 -> 0` | sufficient |
| shrinking Euclidean cap transfer | heat-time thickness obeys `tau_L Gamma_L -> 0` | sufficient |

The assumptions mention finite-time dynamics, local generator bounds, cutoff
energy gaps, and Euclidean/thermal time thickness. They do not mention bridge
algebra, `M_N`, `C^N`, response gaps, or off-diagonal retention.

## Boundary

This is a finite theorem gate. It identifies the physical axiom that excludes
Goal 29's stationary-twirl obstruction:

```text
cutoff_compatible_strong_continuity
```

It does not prove that continuum de Sitter quantum gravity, dS/CFT, or a
static-patch path integral satisfies the axiom.

## Reproducibility

Emit the certificate:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
```

Run the focused regression:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity
```

Validate the machine-readable index:

```bash
python3 -m json.tool docs/goal31_static_patch_strong_continuity_certificate_index.json
```
