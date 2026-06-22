# Reproducibility

This repo is a finite certificate suite. The commands below reproduce the
packaged static-patch observer-algebra benchmark used by the paper draft.

No command below proves continuum de Sitter quantum gravity, a dS/CFT
dictionary, or literal ER=EPR in de Sitter.

## One-Command Summary

From a clean checkout:

```bash
PYTHONPATH=. python3 examples/reproduce_static_patch_package.py
```

Expected result: JSON with

```text
"package": "static_patch_observer_algebra"
"claim_boundary": "finite certificate suite; not continuum de Sitter, dS/CFT, or literal ER=EPR"
```

and five certificate entries whose `status` is `pass` and whose
`all_certified_claims_true` field is `true`:

```text
strong_continuity_gate
finite_to_typeii_scaffold
inclusion_covariant_dynamics
approximate_cutoff_embeddings
continuum_lift_obstruction
```

The `approximate_cutoff_embeddings` entry covers the trace-filled UCP baseline
plus harmonic projection/refinement, heat-kernel coarse graining, and a
Berezin-Toeplitz-inspired smoothing surrogate. These are finite audits, not
canonical continuum static-patch embeddings.

The frozen output of this command is:

```text
artifacts/static_patch_diagnostics/compact_summary.json
```

## Focused Regression Tests

Run the focused package test suite:

```bash
PYTHONPATH=. python3 -m unittest tests.test_static_patch_strong_continuity tests.test_typeii_static_patch_limit tests.test_inclusion_covariant_dynamics tests.test_embedding_channels tests.test_continuum_lift_obstruction
```

Expected result:

```text
Ran 34 tests
OK
```

## Information-Exposure Control Sprint

The completed Paper U prove-or-kill sprint is separate from the frozen package.
Replay its analytic control and JSON-record checks with:

```bash
PYTHONPATH=. python3 -m pytest -q tests/test_information_exposure_control.py
```

Expected result: `18 passed`. To recompute the optional floating-point
covariant SDP record, install its isolated extra and run:

```bash
python3 -m pip install -e '.[research-sdp]'
PYTHONPATH=. python3 experiments/information_exposure_small_spin_sdp.py
```

The script should report `R_min` approximately `0.537943312211` and the verdict
`KNOWN-FRAMEWORK SPECIALIZATION`. This replay checks a finite SDP formulation,
quadrature agreement, and solver residuals. It is not a rigorous interval
certificate, a local-action theorem, or a Paper U novelty claim.

## Finite Type-Certification Control Sprint

Replay the exact cylinder control, entropy dimension floor, adaptive hybrid
bound, and finite-prefix embezzlement optimization with:

```bash
PYTHONPATH=. python3 -m pytest -q \
  tests/test_finite_type_certification_control.py
PYTHONPATH=. python3 \
  experiments/finite_type_certification_control_audit.py
python3 -m json.tool \
  experiments/finite_type_certification_control_certificate.json >/dev/null
```

Expected focused result: `21 passed`. The audit script reports both finite
checks as `true` and the decision
`STOP_GENERIC_FINITE_CERTIFICATION_THEOREM`. The Schmidt-spectrum optimization
is exact at finite dimension up to ordinary floating-point evaluation, and is
cross-checked against brute-force spectra through five sites. The apparent
inverse-square-root support rate is a numerical diagnostic, not a proved
asymptotic, energy, locality, gravity, or algebraic-connectivity theorem.

## Physical Observer-Channel Sprint

Replay the exact finite pointer channel, relational acquisition, resource
ledger, spherical mass-envelope bound, and matched two-region controls with:

```bash
PYTHONPATH=. python3 -m pytest -q \
  tests/test_physical_observer_channel.py
PYTHONPATH=. python3 \
  experiments/physical_observer_channel_audit.py
python3 -m json.tool \
  experiments/physical_observer_channel_certificate.json >/dev/null
```

Expected focused result: `13 passed`. The audit reports normalized diamond
distance approximately `0.03125`, maximum spherical constraint ratio
approximately `0.0729167`, observer-channel decision `RETAIN`, and ER=EPR
decision `STOP_NO_DERIVED_CONNECTIVITY_CONTRAST`. The backreaction entry is an
exact Hamiltonian-constraint calculation for a declared spherical mass
profile, not a same-action stress-tensor or Einstein-matter solution.

## Lead Certificate Commands

Emit the five lead certificates:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-strong-continuity --max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy finite-typeii-static-patch --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy inclusion-covariant-dynamics --max-level 4 --max-consecutive-cutoff 5 --bridge-cert-max-cutoff 5 --noise-strength 1.0 --fixed-lapse 1.0 --environment-qubits 4 --temperature-scale 1.0 --screen-probability 0.75 --low-order 2 --perturbation-radius 0.05
PYTHONPATH=. python3 -m qgtoy static-patch-embedding-channels --max-cutoff 5
PYTHONPATH=. python3 -m qgtoy continuum-lift-obstruction --max-cutoff 5
```

Frozen outputs are stored under:

```text
artifacts/static_patch_diagnostics/
```

## Artifact Validation

Validate the frozen JSON artifacts:

```bash
python3 -m json.tool artifacts/static_patch_diagnostics/strong_continuity_gate.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/finite_to_typeii_scaffold.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/inclusion_covariant_dynamics.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/approximate_cutoff_embeddings.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/continuum_lift_obstruction.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/compact_summary.json >/dev/null
python3 -m json.tool artifacts/static_patch_diagnostics/environment.json >/dev/null
```

## Recorded Environment

The frozen environment manifest is:

```text
artifacts/static_patch_diagnostics/environment.json
```

For the current artifact set it records:

```text
Python: 3.14.2
OS: macOS-26.5.1-arm64-arm-64bit-Mach-O
Generation baseline commit: ebf4a2e3d27ffb806bc99da8795e5fce21e68d8b
Release identifier: v0.1-static-patch-diagnostics
```

The release tag identifies the final immutable repository state for this
package. The generation baseline commit is the code baseline used to emit the
frozen certificates before adding the release artifacts themselves.

## Deterministic Parameters

The certificate package uses the following deterministic parameters:

```text
max_cutoff = 5
max_level = 4
max_consecutive_cutoff = 5
bridge_cert_max_cutoff = 5
noise_strength = 1.0
fixed_lapse = 1.0
environment_qubits = 4
temperature_scale = 1.0
screen_probability = 0.75
low_order = 2
perturbation_radius = 0.05
```

## What the Tests Prove

The tests and frozen artifacts prove reproducibility of the finite benchmark:
the certificate constructors run, the declared finite claims remain internally
consistent, the JSON outputs parse, and the compact package summary reports the
five lead certificate families as passing.

They do not replace the paper proofs. They also do not prove a canonical
continuum static-patch embedding, a continuum de Sitter theorem, a dS/CFT
dictionary, approximate QEC stability, or literal ER=EPR in de Sitter.
