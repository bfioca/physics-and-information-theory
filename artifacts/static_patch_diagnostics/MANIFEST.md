# Static-Patch Diagnostics Artifact Manifest

This directory freezes the lead certificate outputs used by the paper package
for `v0.1-static-patch-diagnostics`.

The artifacts are finite benchmark certificates only. They do not claim
continuum de Sitter quantum gravity, a dS/CFT dictionary, or literal ER=EPR in
de Sitter.

## Files

| File | Source command |
| --- | --- |
| `strong_continuity_gate.json` | `PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| `finite_to_typeii_scaffold.json` | `PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| `inclusion_covariant_dynamics.json` | `PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05` |
| `approximate_cutoff_embeddings.json` | `PYTHONPATH=. python3 -m qgtoy static-patch-embedding-channels --max-cutoff 5` |
| `continuum_lift_obstruction.json` | `PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5` |
| `compact_summary.json` | `PYTHONPATH=. python3 examples/reproduce_static_patch_package.py` |
| `environment.json` | local generation environment and deterministic parameters |

## Generation Environment

See `environment.json` for Python version, platform, deterministic parameters,
and the generation baseline commit. The release tag is expected to be
`v0.1-static-patch-diagnostics`.

## Validation

Validate the frozen JSON files with:

```bash
python3 -m json.tool artifacts/static_patch_diagnostics/strong_continuity_gate.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/finite_to_typeii_scaffold.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/inclusion_covariant_dynamics.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/approximate_cutoff_embeddings.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/continuum_lift_obstruction.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/compact_summary.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/environment.json >/dev/null
```
