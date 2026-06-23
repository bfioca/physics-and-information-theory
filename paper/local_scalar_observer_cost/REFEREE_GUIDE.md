# Referee Guide

Status: external-review candidate; submission remains conditional on proof and
novelty review

## Exact Candidate Claim

For finite pointer weights `w_i` and conditional half-line momentum records
`p_i` supported in `[0,L]`, define

```text
P_cl=sum_i w_i^2,
E_bar=sum_i w_i ||p_i-p_bar||^2/2.
```

The exact Schur channel and localized thermal operator imply

```text
Tr(rho_P^2)
 >= P_cl+(1-P_cl)exp[-C_beta(L)E_bar/(1-P_cl)],

S_2(rho_P)<=min{H_2(w),C_beta(L)E_bar},

C_beta(L)=2 L Lambda(pi L/beta).
```

The symmetric binary top-mode record saturates the entropy bound; no
general-d sharpness claim is made. For a conformal scalar in de Sitter,
`beta=2 pi R`, and the same coefficient is the unique optimum over all
angular and canonical sectors.

Purifying the physical record and inserting it into the simple random code of
Harlow, Usatyuk, and Zhao gives, for an orthogonal CRT-real matter pair,

```text
E_O |<phi|Vhat^dagger Vhat|psi>|^2
 = D/(D+2) Tr(rho_P^2).
```

If every conditional spherical branch satisfies a local final-slice
constraint budget, the paper also derives an area-scaling upper bound on the
same record entropy.

The exact detector channel, general positive-kernel principle, and Harlow
second-moment formula are not claimed as new.

## Read First

1. `main.pdf`: finite-pointer theorem, observer-code proposition, and
   discussion boundary.
2. `sections/finite_pointer_entropy.tex`: complete finite-pointer proof.
3. `sections/localization_theorem.tex`: exact coefficient and de Sitter
   all-sector proof.
4. `../../docs/finite_pointer_observer_entropy.md`: four-gate derivation and
   explicit normalization audit.
5. The specialist brief matching your expertise.
6. `REVIEW_RESPONSE_FORM.md` for the requested written disposition.

## Decisive Questions

1. Is the finite-pointer purity theorem a known consequence of Gaussian
   dephasing or quantum reference-frame resource bounds?
2. Is the reflected KMS-kernel optimization or either uniform remainder a
   named theorem or immediate operator-theory corollary?
3. Is the Harlow-Usatyuk-Zhao Eq. (4.2) specialization correct, and is an
   ensemble mean-square floor for one orthogonal pair physically useful?
4. Are all uses of sharpness restricted to the binary entropy case or the
   underlying final-support coefficient?
5. Does the branchwise final-slice gravity corollary have the correct
   hypotheses and interpretation?
6. Is the combined result substantial enough for a standalone short paper?

## Requested Disposition

- **SUBMIT:** novel enough in this scope and analytically sound.
- **STRENGTHEN:** viable after one identified minimum addition or correction.
- **NO-GO:** known, immediate, incorrect, or too routine; please provide the
  closest source or concise argument.

## Verification

From the repository root:

```bash
python paper/local_scalar_observer_cost/audit_package.py
PYTHONPATH=. python -m pytest -q
```

The audit verifies the checked artifact and its provenance. It does not
certify the proof or novelty.

## Not Claimed

The paper does not claim general-d saturation, a deterministic error floor for
every code, fixed-cylinder controllability, total measurement cost, an
autonomous observer, a channel on perturbed geometry, or coupled
gravitational evolution.
