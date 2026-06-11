# Locality-Reference-Leakage Goal Audit

Audit date: 2026-06-11 UTC

Disposition: **PROVED WITH HEADLINE REDIRECT.** The broad claim that locality
forces leakage for every finite localized non-Abelian reference is false as
stated and has been killed. The elementary compression identity and its norm
bound are standard. What survives is a class-uniform bounded theorem for the
more specific task of reproducing three different components of one rigid
finite `SO(3)` collective mode in pairwise spacelike cells. That theorem is
proved; its status as publishable novelty remains conditional on specialist
priority review.

## Requirement Audit

| Goal requirement | Authoritative evidence | Status |
| --- | --- | --- |
| Work on a new branch | Current branch is `codex/locality-reference-leakage-theorem`. | **PASS** |
| Model-independent spacelike-commuting setting | `docs/locality_reference_leakage_theorem.md`, Section 1, defines a local net, pairwise spacelike regions, a finite code projector, and a nontrivial integer-spin `SO(3)` representation. The algebraic version only assumes commuting bounded star-algebras. | **PASS** |
| Exact compression identity and explicit approximate norm theorem | Equations (2.1)-(2.4) give the directed identity, self-adjoint leakage product, locality defect, and compression-error constants. | **PASS** |
| At least one of leakage, action error, or locality violation | Equation (2.4) isolates those three budgets without a factorized-current assumption. | **PASS** |
| Class-uniform result beyond `h(x)J_a` | Equations (3.1)-(3.11) quantify over arbitrary bounded cell observables and ambient Hilbert spaces satisfying the displayed compression and locality hypotheses. | **PASS** |
| State-weighted three-cell theorem | Equation (3.6) proves `sum p_a >= alpha^4 Tr(rho J^2)/(4 Lambda^2)` for any certified uniform off-code cap. Equation (3.11) is the robust version. | **PASS** |
| Operational orientation-risk composition | Equations (4.1)-(4.7) derive the risk-conditioned weight and amplitude bounds and separately test whether the risk/gain/norm/spin parameters are non-vacuous. | **PASS** |
| Distributed local model with meaningful scaling | Section 5 proves the disjoint two-block norm ratio tends to one and the three-block state-weighted actual/lower ratio tends to eight. A positive-width buffer is included. | **PASS** |
| Independent finite-dimensional model checks | `tests/test_locality_reference_leakage.py` constructs ambient Dicke matrices for unbuffered and buffered two-block cases and for a six-site three-cell case. | **PASS** |
| Primary-literature novelty audit | `docs/locality_reference_leakage_novelty_audit.md` records primary sources, kills the standard/broad claims, and compares hypotheses and metrics with approximate QEC, continuous covariance, local recovery, and quantum-frame alignment. Official arXiv metadata was refreshed on the audit date. | **PASS, PRIORITY UNCONFIRMED** |
| Manuscript-ready theorem statement and proof | `docs/locality_reference_leakage_theorem.md` contains explicit quantifiers, constants, proof steps, model derivations, risk composition, normalization caveats, and nonclaims. | **PASS** |
| Paper outline | `paper/locality_reference_leakage_outline.md` supplies a bounded-paper abstract, main results, section plan, figures/tables, and submission kill gate. | **PASS** |
| Exclude KMS-QFT, gravity, Skyrmion, and Paper U closure | The theorem artifact, outline, certificate, and ledger all state these as nonclaims; none enters a premise. | **PASS** |
| Stop rather than inflate a failed general claim | The novelty audit explicitly kills the universal headline and labels the compression lemma standard. | **PASS** |

## Proven Statements

For bounded self-adjoint `A,B`, code projector `P`, and `Q=I-P`,

```text
[PAP,PBP]=P[A,B]P+PBQAP-PAQBP,
||[PAP,PBP]||<=||P[A,B]P||+2||QAP||||QBP||.
```

If three pairwise commuting bounded observables satisfy
`P A_a P=alpha J_a` and `||Q A_aP||<=Lambda`, then every code state obeys

```text
sum_a Tr[rho P A_a Q A_a P]
 >=alpha^4 Tr(rho J^2)/(4Lambda^2),
Lambda^4>=alpha^4 Tr(rho J^2)/12.
```

For achieved Haar-prior chordal full-frame risk `R_ref<=r`,

```text
sum_a Tr[rho P A_a Q A_a P]
 >=alpha^4[r^(-1)-8]_+/(64Lambda^2),
Lambda^4>=alpha^4[r^(-1)-8]_+/192.
```

The robust theorem replaces the numerator by
`[alpha^4 Tr(rho J^2)-3(1+1/t)d^2]_+`, where
`d=delta+4|alpha|J_max epsilon+2epsilon^2`, and the denominator by
`4(1+t)Lambda^2`. Substituting the risk-required Casimir gives the same
formula with `alpha^4[r^(-1)-8]_+/16` in the numerator, and consistency gives
the corresponding amplitude bound with denominator `12(1+t)`.

## Scientific Boundary

This is a truncation theorem for **spacelike replication of a rigid collective
mode**. It is not a no-go for local non-Abelian currents, because several
noncommuting components may live in one region. The off-code weights are not
transition probabilities or lifetimes without a normalized operation and
dynamics. At fixed local norm, the response ratio may weaken with spin, so the
theorem does not establish that increasingly accurate references must
decohere increasingly fast.

The correct publication status is therefore **conditional paper candidate**,
not “breakthrough proved.” Before submission, an AQFT/QEC specialist must
check whether the state-weighted theorem is an immediate reformulation of
approximate cleaning or covariant-code results. If it is, freeze these
artifacts as a methods note and do not submit the theorem as novel.

## Verification Record

The authoritative focused commands are:

```bash
PYTHONPATH=. python -m pytest -q tests/test_locality_reference_leakage.py tests/test_global_so3_reference_risk.py
PYTHONPATH=. python -m qgtoy locality-reference-leakage
git diff --check
```

The first command checks the new identities, robust constants, risk
composition, non-vacuity logic, buffered block model, and three-cell model.
The CLI certificate must return `"status": "pass"` with every certified claim
true. The final focused result was **34 passed in 0.50 seconds**; the CLI
certificate returned pass, `compileall` succeeded, and `git diff --check`
reported no errors.

The repository-wide run collected 1,461 tests. It was stopped after the first
failure and that test was rerun alone. The unrelated
`test_source_hashed_outer_tube_liouville_artifact` fails because its committed
Skyrmion certificate pins SHA-256 `3882308331da...` for
`qgtoy/validated_centrifugal_liouville_taylor.py`, while the clean, unmodified
source currently hashes to `65e6b2f853bc...`. The recomputed coercivity result
remains true; authentication is stale. Neither file is modified on this
branch, and the active goal explicitly excludes the Skyrmion, so this audit
records the failure without refreshing or weakening that separate artifact.
