# Finite-Pointer Observer Entropy

Research code, proofs, and external-review materials for a mathematical-
physics paper relating the second Renyi entropy of a localized field record to
its energy, support, observer-code accuracy, and branchwise gravitational
backreaction.

**Status: GO to external review; HOLD submission.** The finite-pointer
algebra, exact localization theorem, Harlow-code insertion, branchwise
constraint composition, two independent numerical implementations, and
reproducibility checks pass internally. Submission remains gated on external
proof and novelty review in detector/QFT, operator theory, and quantum gravity.

## Start Here

1. Read the [23-page manuscript](paper/local_scalar_observer_cost/main.pdf).
2. Use the [reviewer entry point](REVIEWER_README.md) for the claim hierarchy
   and requested disposition.
3. Use the [paper package guide](paper/local_scalar_observer_cost/README.md)
   for sources, replay commands, and artifact provenance.
4. Consult the [finite-pointer derivation](docs/finite_pointer_observer_entropy.md)
   and [clean-room localization audit](docs/local_scalar_observer_proof_audit.md)
   for proof details outside the manuscript.

The [external-review launch kit](paper/local_scalar_observer_cost/EXTERNAL_REVIEW_LAUNCH.md)
builds small, deterministic, revision-pinned packets for each specialist
domain.

## Central Result

Let a finite pointer have weights `w_i` and conditional post-switch scalar
data `p_i`, all supported in the optical interval `[0,L]`. Define

```text
P_cl = sum_i w_i^2,
p_bar = sum_i w_i p_i,
E_bar = sum_i w_i ||p_i-p_bar||^2/2.
```

For the exact controlled-displacement channel,

```text
Tr(rho_P^2)
 >= P_cl + (1-P_cl)
    exp[-C_beta(L) E_bar/(1-P_cl)],

S_2(rho_P) <= min{H_2(w), C_beta(L) E_bar}.
```

The localized thermal coefficient is exact:

```text
C_beta(L)=2 L Lambda(pi L/beta),
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

Equal binary weights and opposite top-mode profiles saturate the bound. Global
sharpness for arbitrary pointer dimension is not claimed. At the de Sitter
temperature `beta=2 pi R`, the same s-wave momentum mode is the unique
optimizer over all angular and canonical sectors.

## Observer-Code Consequence

The purified field record has the same nonzero reduced spectrum as the
physical pointer. For an orthogonal CRT-real matter pair in the simple random
code of [Harlow, Usatyuk, and Zhao](https://arxiv.org/abs/2501.02359),

```text
E_O |<phi|Vhat^dagger Vhat|psi>|^2
 = D/(D+2) Tr(rho_P^2).
```

The energy-support theorem therefore gives a lower floor on this
Haar-averaged squared code fluctuation. It is not a deterministic error floor
for every fixed code or a derivation of the gravitational observer rule.

## Gravity Corollary

If every conditional spherical `q_i=0` branch obeys the local final-slice
constraint budget `Q_b,i<=delta`, then

```text
S_2(rho_P)
 <= delta (R^2/G)
    C_opt(y) tanh(y) sech(y)^2 / 2.
```

The budget is branchwise. The channel is still computed on fixed de Sitter,
and the result does not solve a coupled Einstein-scalar evolution.

## Claim Boundary

- The resource is centered post-switch scalar-field Killing energy, not total
  apparatus, clock, battery, or switching cost.
- Sharpness of the thermal coefficient is for final Cauchy support. A source
  radius and duration provide a causal support envelope, not fixed-cylinder
  controllability.
- The finite pointer and sources are prescribed detector idealizations, not an
  autonomous relativistic observer.
- The observer-code statement is an ensemble second moment for a specified
  orthogonal pair, not a uniform or deterministic code theorem.
- Gravity is a branchwise final-slice constraint application. The channel is
  not rederived on perturbed geometries.
- The exact detector channel and vacuum logarithmic parent operator are prior
  art. Standalone novelty of the full composition remains under review.

## Repository Map

| Path | Purpose |
| --- | --- |
| [`paper/local_scalar_observer_cost/`](paper/local_scalar_observer_cost/) | Manuscript, bibliography, specialist briefs, PDF, and artifact ledger |
| [`qgtoy/finite_pointer_observer.py`](qgtoy/finite_pointer_observer.py) | Executable finite-pointer, code, and gravity algebra |
| [`qgtoy/local_scalar_observer_cost.py`](qgtoy/local_scalar_observer_cost.py) | Exact localization formulas and certificate construction |
| [`experiments/`](experiments/) | Analytic replays, independent checks, numerical spectrum, and frozen records |
| [`tests/`](tests/) | Theorem, manuscript, numerical, provenance, and packet tests |
| [`THEOREMS.md`](THEOREMS.md) | Compact theorem and evidence index |
| [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | Clean-checkout verification instructions |

## Quick Verification

```bash
python -m pip install -e '.[research-numerics]'
PYTHONPATH=. python -m pytest -q
python paper/local_scalar_observer_cost/audit_package.py
```

Both commands must pass. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the
four-gate and independent replay commands.

The code is released under the [MIT License](LICENSE). Citation metadata are
in [CITATION.cff](CITATION.cff).
