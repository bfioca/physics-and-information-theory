# Reviewer Entry Point: Finite-Pointer Observer Entropy

**Status:** internally closed paper candidate; external proof and novelty review
remain open. No submission decision has been issued.

This repository is organized around one manuscript. The paper derives a
finite-pointer purity bound from a sharp localized thermal covariance theorem,
inserts that physical purity into the Harlow-Usatyuk-Zhao simple random code,
and gives a branchwise final-slice gravity corollary.

## Five-Minute Route

1. Read the [manuscript](paper/local_scalar_observer_cost/main.pdf), especially
   the finite-pointer theorem, observer-code proposition, and claim boundary.
2. Use the [shared referee guide](paper/local_scalar_observer_cost/REFEREE_GUIDE.md)
   for the theorem hierarchy and requested disposition.
3. Choose a specialist brief:
   [detector/QFT](paper/local_scalar_observer_cost/QFT_NOVELTY_REVIEW.md),
   [operator theory](paper/local_scalar_observer_cost/OPERATOR_NOVELTY_REVIEW.md),
   or [observer code and gravity](paper/local_scalar_observer_cost/OBSERVER_CODE_REVIEW.md).
4. Consult the [finite-pointer proof note](docs/finite_pointer_observer_entropy.md)
   and [clean-room localization audit](docs/local_scalar_observer_proof_audit.md).
5. Record findings in the [response form](paper/local_scalar_observer_cost/REVIEW_RESPONSE_FORM.md).

## Candidate Contribution

For finite pointer weights `w_i` and conditional scalar momentum data
`p_i` supported in `[0,L]`, define

```text
P_cl=sum_i w_i^2,
E_bar=sum_i w_i ||p_i-p_bar||^2/2.
```

The paper proves

```text
Tr(rho_P^2)
 >= P_cl+(1-P_cl)exp[-C_beta(L)E_bar/(1-P_cl)],

S_2(rho_P) <= min{H_2(w),C_beta(L)E_bar},

C_beta(L)=2 L Lambda(pi L/beta).
```

The coefficient is the exact norm of a reflected thermal logarithmic kernel.
At `beta=2 pi R`, it controls every angular and canonical sector of a
conformal scalar in de Sitter. The entropy inequality is saturated in the
symmetric binary top-mode sector; arbitrary-dimension sharpness is not
claimed.

For an orthogonal CRT-real matter pair in the Harlow-Usatyuk-Zhao simple
random code, the physical record gives

```text
E_O |<phi|Vhat^dagger Vhat|psi>|^2
 = D/(D+2) Tr(rho_P^2).
```

This converts the field theorem into an ensemble-averaged code-fluctuation
floor. A separate branchwise constraint argument bounds the same record
entropy by a local final-slice backreaction budget.

## Claim Boundary

The energy is post-switch scalar-field energy only. The pointer and sources
are prescribed, not autonomous. The code result is a Haar mean-square
statement for a specified pair, not a deterministic theorem for every code.
The gravity result is branchwise final-slice constraint data, not a channel on
perturbed geometry or a coupled evolution. Final-support sharpness does not
imply controllability from every smaller fixed source cylinder.

## Requested Decision

- **SUBMIT:** the three novelty gates pass and the central proofs survive
  external review.
- **STRENGTHEN:** identify one concrete minimum theorem or correction required
  before submission.
- **NO-GO:** provide the theorem, reference, or argument that makes the result
  known, immediate, incorrect, or insufficient for a standalone paper.

A blank row or `NOT REVIEWED` is not a proof pass. This is a request for
critical review, not endorsement or approval.

## Reproduce the Package

```bash
python -m pip install -e '.[research-numerics]'
PYTHONPATH=. python -m pytest -q
python paper/local_scalar_observer_cost/audit_package.py
```

These checks establish internal closure and provenance, not literature
novelty.
