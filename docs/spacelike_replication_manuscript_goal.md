# Track 2 Goal: Bounded Spacelike-Replication Manuscript

Status: **complete -- NOVELTY STOP**

Branch: `codex/spacelike-replication-manuscript`

## Final Outcome

The program stopped at its predeclared novelty-reduction gate. For the UCP
compression `T(X)=W*XW`, Janssens' CP-map covariance Cauchy-Schwarz lemma
identifies `W*A_aQA_aW` as the standard added-noise operator and gives the
state-weighted pair inequality directly. Summing the three cyclic `SO(3)`
pairs yields the proposed central theorem verbatim. The result remains correct
and useful as an internal lemma, but it is not a standalone paper contribution.

The exact reduction is recorded in
`spacelike_replication_qec_reduction_audit.md`. No submission or
attachment-ready PDF should be produced under this goal.

## Original Objective

Turn the proved bounded spacelike-replication theorem into a short,
self-contained manuscript suitable for specialist critique. The paper must
lead with the exact three-cell hypothesis, prove the state-weighted inequality
and its robust version, include the full global `SO(3)` orientation-risk
argument used by the operational corollary, and state the fixed-calibration
and large-spin escape routes beside the main theorem. The disjoint-block
ferromagnet is an explicit realization, not evidence for uniformly localized
apparatuses or a dynamical lifetime.

Publication status is determined by a source-level reduction audit, not by
polish. Translate the nearest approximate-cleaning and covariant-QEC theorems
into the variables `p_a`, `lambda_*`, `alpha`, mean Casimir, and commuting
cells. If the three-cell theorem is an immediate corollary, stop the paper
claim and retain a methods note with the reduction written explicitly. If it
is not, produce a referee-readable comparison explaining the different task,
metric, and hypotheses without claiming priority from search absence.

## Completion Gates

| Gate | Pass condition | Stop condition |
| --- | --- | --- |
| Main proof | Exact and robust theorems are self-contained and independently checked. | A hidden assumption or incorrect constant survives proof audit. |
| Risk appendix | Covariantization, Peter-Weyl fusion, multiplicities, mixed states, and the discrete Hardy step are proved with the stated cost and constant. | The operational corollary depends on an unclosed representation-theoretic step. |
| Novelty reduction | No checked primary theorem immediately yields the result after an explicit variable translation. | CP-map, joint-measurement, approximate-cleaning, or covariant-QEC theory subsumes the claim directly. |
| Model realization | Pairwise sharpness and three-cell constant-factor scaling are derived and matched by finite matrices. | The model uses a stronger locality or normalization assumption than the theorem states. |
| Claim boundary | Abstract and discussion state the gain escape, growing support diameter, absence of dynamics, and absence of Paper U closure. | The manuscript requires a generic non-Abelian-current, lifetime, gravity, or uniformly local claim. |
| Reproduction | Focused tests, certificate, source checks, and manuscript build instructions pass. | The paper depends on unrelated repository certificates or unrecorded numerical input. |

## Retained Artifacts

- `paper/spacelike_replication/main.tex`: frozen internal methods-note source;
- `paper/spacelike_replication/references.bib`: primary-source bibliography;
- `docs/spacelike_replication_qec_reduction_audit.md`: symbol-level novelty
  stop decision;
- `tests/test_spacelike_replication_manuscript.py`: source-closure check;
- focused theorem, risk, CLI, and numerical Peter-Weyl checks;
- the final **NOVELTY STOP** disposition.

The stopped methods note may be used internally when Paper U needs the
joint-measurement lemma, provided Janssens is cited as the underlying general
result.
