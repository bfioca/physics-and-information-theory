# Harlow Review Packet Requirement Audit

Audit date: 2026-06-10 UTC
Auditor role: independent acceptance pass against
`docs/harlow_review_packet_codex_goal.md`
Overall result: **PASS**

This is an acceptance audit of the review packet, not a validation of the open
physics theorem or a publication recommendation. Every required artifact,
framing rule, claim boundary, and acceptance test is accounted for below.
The unresolved scientific bridges are correctly presented as review questions
or **[OPEN]** claims and therefore do not constitute packet defects.

Post-sprint status revision: **PASS**. The packet records the proved regular-
bath finite-switch lemma, the conditional named-QFT detector box, its open KMS
GNS/Araki-Woods bridge, and the microcausal route stop. Paper R separately ends
in **INCONCLUSIVE STOP**. The executable branch remains optional, and the
packet asks for conceptual direction without presenting either route as Paper
U closure.

## A-G artifact audit

| Requirement | Result | Exact evidence |
| --- | --- | --- |
| A. One-page conceptual note | **PASS** | Page 1 is section `#conceptual-note` in `packet.html`; the editable companion is `drafts/conceptual_note.md`. It states the observer question, relational task, record variable, theorem chain, gravity/realization role, regular-bath lemma, conditional named-QFT box, open GNS bridge, local-matter common-action bottleneck, completed response STOP, and reason for requesting Harlow's critique. It has three displayed equations and no implementation-level decimal constants. |
| B. One-page dependency diagram | **PASS** | Page 2 embeds `dependency_diagram.svg`. The main column follows relational risk -> `S_dir` -> representation/energy -> localization/gravity -> lifetime/readout -> proposed tradeoff. Every node/arrow is labeled **[PROVED]**, **[CONDITIONAL]**, or **[OPEN]**. Paper A is realization support; Paper R is a completed STOP diagnostic rather than a manuscript branch. |
| C. Exactly three review questions | **PASS** | Page 3 section `#review-questions` and `drafts/three_questions.md` contain three numbered questions and exactly three question marks. There is no fourth request hidden in the feedback-target box. |
| D. Minimal technical appendix | **PASS** | Pages 4-8 cover the global risk bounds, conditional degradation law, proved regular-bath finite-switch estimate, conditional AS2 named-QFT detector box, open GNS bridge, locality stop, orbital versus collective capacity, certified profile, conserved-source/master/Weyl architecture, completed zero-containing response interval, STOP decision, exact claim boundary, and reproducibility map. Implementation constants and artifact hashes are absent from page 1 and confined to this appendix. |
| E. Primary-source literature matrix | **PASS** | `literature_matrix.md` compares 33 primary sources across all six required areas. `source_verification_log.md` records API, HTML, PDF, and author-source checks and distinguishes deep checks from abstract-only checks. All 33 unique arXiv links returned HTTP 200 during this audit. No priority conclusion is inferred from search absence. |
| F. Outreach email | **PASS** | `drafts/outreach_email.md` is 178 words excluding heading/subject and 184 including the subject. It states both bounded STOP results without numerical detail, compresses the three purposes, accurately describes the packet, offers the executable repository only if useful, and explicitly asks for criticism and redirection rather than endorsement or a publication decision. |
| G. Compiled packet and editable sources | **PASS** | `finite_directional_observer_review_packet.pdf` has `%PDF-` signature, 335297 bytes, nine `/Type /Page` objects, 20 link annotations, and expected title metadata. Its order is note, diagram, questions, appendix, bibliography. Canonical editable source is `packet.html`, with `dependency_diagram.svg`, `bibliography.md`, and synchronized Markdown companions retained. |

## Required framing

| Goal item | Result | Evidence and judgment |
| --- | --- | --- |
| 1. Observer register is the headline; approximately 70/25/5 architecture/gravity/Skyrmion | **PASS** | The three-page front matter is dominated by the generic observer chain. Page 1 gives seven architecture/bottleneck blocks, one gravity/realization block, and only one Skyrmion paragraph; page 2 uses a large main chain with Paper R and Paper A as side branches; page 3 asks architecture-level questions. This is the requested approximate hierarchy, not a claimed numerical content measurement. |
| 2. Global-risk relational alignment, never absolute orientation | **PASS** | Page 1 defines `g_rel=g_O^-1 g_D`, a Haar-prior full-group risk, and denies orientation relative to coordinates. The diagram and Appendix A repeat the relational domain. |
| 3. Disciplined `S_dir` usage and first review question | **PASS** | The packet uses the narrower phrase "operational rotational-asymmetry resource" and defines it by relative entropy of `SO(3)` asymmetry. It explicitly distinguishes `S_dir` from effective dimension, Casimir, QFI, thermodynamic entropy, and `S_Ob`. Question 1 asks whether a comparison is meaningful rather than assuming one. |
| 4. Classical record stability rather than generic coherence | **PASS** | Lifetime is defined by achievable relational readout risk after storage time `T`. Page 1 and Appendix A explicitly distinguish this from preservation of arbitrary quantum phase coherence. |
| 5. `B_W` is a provisional witness, not the capacity bottleneck | **PASS** | Page 1, page 2, pages 6-8, and `adversarial_audit.md` state that the bounded route did not certify nonzero response. They deny that `B_W` is a capacity bound and ask what quantity should replace or refine it. |
| 6. Skyrmion is removable realization support | **PASS** | The abstract chain, theorem sketch, common-action bottleneck, and three questions remain meaningful with the Skyrmion paragraph and Paper A card removed. Paper A is explicitly a hard-wall fixed-de Sitter support branch, not a premise of the observer architecture. |
| 7. Microscopic preparation/storage/readout channel is primary bottleneck | **PASS** | Page 1 labels the QFT bridge and common-action local-matter record channel open. Appendix A separates the stipulated heat-channel implication, proved regular-bath estimate, and conditional named-QFT box from the missing GNS construction, microcausal matter realization, acquisition, readout, support stress, backreaction, and common parameter window. |
| 8. Compact theorem sketch with declared quantifiers | **PASS** | Page 1 declares `C_dir` over localized register-target models, states, environments, local actions, and preparation/storage/readout protocols, then gives one three-line schematic theorem chain. The Markdown companion states the static-patch KMS environment explicitly. |
| 9. Detailed numerics stay in the optional appendix | **PASS** | Page 1 contains no implementation decimal constants or hashes. Interval values, residual losses, and certificate hashes occur only on pages 4-8. |
| 10. No unsupported novelty or priority claim | **PASS** | Page 8 and page 9 deny a priority conclusion; `literature_matrix.md` identifies nearest neighbors and narrow distinctions; `source_verification_log.md` records nonexhaustive search limits. No "first" or "breakthrough" claim is made. |

## Claim discipline

| Boundary | Result | Evidence |
| --- | --- | --- |
| Consistent status labels | **PASS** | Diagram and appendix contain all three labels and define their meanings. Composite claims inherit the least-complete ingredient in Appendix A. |
| Completed Weyl-response interval contains zero | **PASS** | Pages 1 and 7 state that the completed full response interval contains zero after all frozen origin, bulk, and wall proof terms. The signed estimator, rigorous interval, and STOP decision are kept separate. |
| Named-QFT and common-action local-matter channels remain open | **PASS** | Page 1, page 2, page 4, and page 8 distinguish the proved regular-bath lemma from the **[CONDITIONAL]** named-QFT detector box and **[OPEN]** GNS/local-matter bridges. |
| `S_dir` is not `S_Ob` | **PASS** | Page 1 boundary box, diagram caveat band, Appendix A, and question 1 make the non-identification explicit. |
| Self-gravity, Israel matching, and closed-universe path integral excluded | **PASS** | Pages 6 and 8 exclude self-consistent rotating Einstein-Skyrme geometry and completed tensorial Israel matching; page 8 states that a closed-universe path integral is outside the claims. |
| Certificate failure is not a physical no-go | **PASS** | Page 7 calls the roughly `9.50`-fold primal norm gap a proof-representation diagnostic and explicitly denies physical cancellation or a no-go theorem. |

## Acceptance tests

| Test | Result | Evidence |
| --- | --- | --- |
| 1. First page works without Skyrmion knowledge | **PASS** | The operational question, relational task, resource, theorem chain, and bottleneck are established before the single candidate-realization paragraph. Visual inspection found the page compact, readable, and self-contained. |
| 2. At most three equations and no implementation constants on page 1 | **PASS** | Automated result: 3 equation blocks; no `0.xx` implementation decimal matches; 573 words. |
| 3. Domain, task, variable, witness, and open bridge identifiable quickly | **PASS** | `C_dir`, Haar-risk relational alignment, rotational-asymmetry `S_dir`, fixed-background `B_W`, the rigid-detector lemma, and the open common-action local-matter bridge are each named on page 1. |
| 4. Architecture survives removal of Skyrmion material | **PASS** | The main chain has an independent abstract risk theorem and orbital-matter capacity route. The Skyrmion appears only as one candidate support branch. |
| 5. Technical claims map to evidence or OPEN | **PASS** | `claim_evidence_ledger.md` maps the packet claim surface to theorem identifiers, current exact artifacts/hashes, conditional design evidence, or explicit **[OPEN]** rows. It includes the commands that replay the decisive Paper R certificate. |
| 6. Literature entries are checked primary sources | **PASS** | The 33 matrix links are primary arXiv records; all resolved HTTP 200 in the independent link check. `source_verification_log.md` records the verification depth and corrected inherited metadata. |
| 7. Reproducible, unclipped, linked PDF with matching editable source | **PASS** | A build in a temporary copy completed with status 0. Browser DOM measurement reported `data-overflow=false`, `overflow-x=0`, and `overflow-y=0` on all nine sheets. HTML has no missing internal targets; PDF has 20 link annotations. `artifact_manifest.json` binds the final PDF and sources by SHA256. |
| 8. Adversarial conflation review | **PASS** | `adversarial_audit.md` separately checks all five required pairs, plus estimator-versus-interval evidence, STOP-versus-no-go, witness-versus-capacity, channel status, novelty, and outreach posture. |
| 9. No publication-approval request | **PASS** | The email and page 1 ask for conceptual direction, criticism, and redirection and explicitly deny endorsement or a publication decision. Automated forbidden-phrase check passes. |
| 10. Completion handoff contains paths, commands, sources, uncertainties, and open claims | **PASS** | `README.md`, this audit, the verification log, and the ledger provide all required handoff fields. The final user-facing response must relay them and must retain the open-claim list below. |

## Render and build evidence

- Visual proof directory: `output/playwright/harlow-review-packet/`.
- Nine inspected PNGs: `page-01.png` through `page-09.png`, each 816 x 1056.
- Secondary nine-page proof PDF:
  `output/playwright/harlow-review-packet/playwright-review.pdf`.
- Visual inspection at original resolution found no clipping, overlap, missing
  diagram labels, broken cards, or footer collisions. The current pass caught
  and corrected a clipped Paper R diagram title; all three question cards and
  the completed STOP decision fit comfortably after the revision.
- The build-time DOM dump contained nine explicit `data-overflow="false"`
  results and no `data-overflow="true"` result.

Commands used for the independent checks:

```bash
# Run on a temporary copy so the acceptance audit did not mutate the final PDF
# or manifest.
CHROME_BIN=/tmp/harlow-pw/chrome-headless-shell-linux64/chrome-headless-shell \
  /tmp/<audit-copy>/packet/build_packet.sh
node /tmp/<audit-copy>/packet/audit_packet.mjs

# Final packet assertions and manifest generation.
node docs/harlow_review_packet/audit_packet.mjs

# Primary-link availability: 33 unique URLs, all HTTP 200.
rg -o 'https://arxiv\.org/abs/[A-Za-z0-9._/-]+' \
  docs/harlow_review_packet/literature_matrix.md | sort -u

# Repository whitespace audit.
git diff --check
```

Chromium emits harmless DBus, Bluetooth, and GPU warnings in this headless
environment. The build and layout checks still exit successfully. Rebuilt PDF
bytes need not be bit-for-bit stable because PDF metadata may change; page
structure, content assertions, links, layout measurements, and the manifest
for the retained artifact are the reproducibility criteria used here.

## Scientifically open claims

The packet is ready to request specialist critique precisely because it does
not conceal these unresolved claims:

1. No `S_dir`-to-`S_Ob` dictionary or comparison theorem is known.
2. The gauge-invariant gravitational quantity that should cap observer
   capacity is not identified.
3. The finite-switch storage channel is proved in the regular Gaussian-bath
   framework. Its named Bunch-Davies detector application still needs a KMS
   GNS/Araki-Woods bridge. No microcausal local-matter action yet derives
   acquisition, storage degradation, readout, channel error, support stress,
   and backreaction in one open parameter window.
4. The completed rigorous fixed-background response interval contains zero;
   no nonzero lower bound for the normalized Skyrmion electric-Weyl response is
   proved, and a future attempt requires a materially new primal proof object.
5. Tensorial Israel matching and a rotating self-gravitating
   Einstein-Skyrme-de Sitter solution are not supplied.
6. The static-patch construction is not a derivation of Harlow's
   closed-universe observer rule or path integral.

These are scientific review targets, not hidden acceptance failures.
