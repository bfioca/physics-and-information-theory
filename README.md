# Final-Support Thermal Dephasing

Research code, proofs, and external-review materials for a short
mathematical-physics paper on the maximum thermal dephasing attainable at
fixed post-switch scalar-field energy and fixed final Cauchy support.

**Status: GO to external review; HOLD submission.** The theorem, two
independent numerical implementations, build, reproducibility, and clean-room
proof checks pass internally. Equation-level detector/QFT and operator audits
reduce the remaining review workload, but submission remains gated on written
external novelty dispositions and external proof coverage of every central
claim.

## Start Here

1. Read the [18-page manuscript](paper/local_scalar_observer_cost/main.pdf).
2. Use the [reviewer entry point](REVIEWER_README.md) for the claim boundary
   and requested disposition.
3. Use the [paper package guide](paper/local_scalar_observer_cost/README.md)
   for sources, replay commands, and artifact provenance.
4. Consult the [clean-room proof audit](docs/local_scalar_observer_proof_audit.md) and
   [equation-level priority audit](paper/local_scalar_observer_cost/PRIORITY_AUDIT.md)
   for the two remaining external gates.

To request a specialist review, use the
[launch kit](paper/local_scalar_observer_cost/EXTERNAL_REVIEW_LAUNCH.md). It
builds small, deterministic, revision-pinned packets rather than asking a
reviewer to navigate the repository.

## Main Result

For Dirichlet half-line momentum data supported in `[0,L]`, inverse
temperature `beta`, dephasing exponent `Gamma`, and post-switch field energy
`E=||p||_2^2/2`, the paper proves

```text
Gamma <= E C_beta(L),
C_beta(L)=2 L Lambda(pi L/beta),
```

where `Lambda(tau)` is the simple top eigenvalue of the positive compact
kernel

```text
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

It gives global bounds and uniform small- and large-support remainders. In the
large-support regime,

```text
0 <= C_beta(L)-16L^2/(beta pi^2) <= beta/3.
```

At the de Sitter temperature `beta=2 pi R`, the same s-wave momentum profile
is the unique optimizer over all angular and canonical sectors of the
conformally coupled massless scalar.

## Observer-Rule Connection

The target is the binary instance of the quantum-to-classical pointer channel
used in the observer rule of
[Harlow, Usatyuk, and Zhao](https://arxiv.org/abs/2501.02359) and its
[Hartle--Hawking extension](https://arxiv.org/abs/2602.03835). At fixed
`y=L/R`, the theorem gives

```text
E_K R >= log[1/(2 epsilon_obs)] / C_opt(y).
```

Thus this localized fixed-background realization cannot approach complete
pointer dephasing with bounded post-switch field energy. This is a
field-sector analogue of a finite-observer-resource obstruction, not a
derivation of the gravitational observer rule: the paper does not identify
`epsilon_obs` with a gravitational encoding error or `exp(-S_Ob)`, price the
observer's total mass or entropy, or include gravitational response.

## Claim Boundary

- Sharpness is for **final Cauchy support**. Source radius and duration provide
  a causal support envelope, not fixed-cylinder controllability.
- `E_K` is **post-switch scalar-field Killing energy**, not total apparatus,
  clock, battery, or switching cost.
- The pointer is a prescribed gapless smeared-detector idealization, not an
  autonomous relativistic measuring device.
- Gravity is a final-slice Einstein-scalar constraint application. The channel
  is not rederived on a perturbed geometry.
- The exact detector channel and the vacuum logarithmic parent operator are
  prior art. Standalone novelty of the combined thermal and all-sector theorem
  remains an external-review question.

## Repository Map

| Path | Purpose |
| --- | --- |
| [`paper/local_scalar_observer_cost/`](paper/local_scalar_observer_cost/) | Manuscript, bibliography, review briefs, PDF, and frozen artifact ledger |
| [`qgtoy/local_scalar_observer_cost.py`](qgtoy/local_scalar_observer_cost.py) | Executable formulas and certificate construction |
| [`experiments/`](experiments/) | Analytic replay, production spectrum, independent clean-room checker, and frozen records |
| [`tests/`](tests/) | Focused theorem, manuscript, two-method numerical, and packet tests |
| [`docs/local_scalar_observer_cost.md`](docs/local_scalar_observer_cost.md) | Extended derivation and physical interpretation |
| [`docs/local_scalar_observer_proof_audit.md`](docs/local_scalar_observer_proof_audit.md) | Claim-by-claim clean-room derivation, independent numerical replay, and external sign-off boundary |
| [`THEOREMS.md`](THEOREMS.md) | Compact theorem and evidence index |
| [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | Clean-checkout verification instructions |

## Quick Verification

```bash
python -m pip install -e '.[research-numerics]'
PYTHONPATH=. python -m pytest -q
python paper/local_scalar_observer_cost/audit_package.py
```

Expected result: `50 passed` and a package audit with `"status": "pass"`.
See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for full analytic and numerical
replay commands.

## Review Gate

`SUBMIT` requires both domain novelty gates to pass and every central claim in
the [response form](paper/local_scalar_observer_cost/REVIEW_RESPONSE_FORM.md)
to receive at least one external `PASS` or `CORRECT`. A row marked
`NOT REVIEWED` by every reviewer remains open.

The code is released under the [MIT License](LICENSE). Citation metadata are
in [CITATION.cff](CITATION.cff).
