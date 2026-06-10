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

Post-audit packaging revision: **PASS**. The repository now opens with a
Harlow-specific attachment quickstart, distinguishes the older static-patch
expert bundle, and makes the executable branch optional rather than the main
review artifact.

## A-G artifact audit

| Requirement | Result | Exact evidence |
| --- | --- | --- |
| A. One-page conceptual note | **PASS** | Page 1 is section `#conceptual-note` in `packet.html`; the editable companion is `drafts/conceptual_note.md`. It states the observer question, relational task, record variable, theorem chain, gravity/realization role, common-action bottleneck, and reason for requesting Harlow's critique. Automated count: 604 words, three displayed equations, and no implementation-level decimal constants. |
| B. One-page dependency diagram | **PASS** | Page 2 embeds `dependency_diagram.svg`. The main column follows relational risk -> `S_dir` -> representation/energy -> localization/gravity -> lifetime/readout -> proposed tradeoff. Every node/arrow is labeled **[PROVED]**, **[CONDITIONAL]**, or **[OPEN]**. Paper A and Paper R are separate support branches. |
| C. Exactly three review questions | **PASS** | Page 3 section `#review-questions` and `drafts/three_questions.md` contain three numbered questions and exactly three question marks. There is no fourth request hidden in the feedback-target box. |
| D. Minimal technical appendix | **PASS** | Pages 4-8 cover the global risk bounds, conditional degradation law, orbital versus collective capacity, certified profile, conserved-source/master/Weyl architecture, present zero-exclusion loss, exact claim boundary, and reproducibility map. Implementation constants and artifact hashes are absent from page 1 and confined to this appendix. |
| E. Primary-source literature matrix | **PASS** | `literature_matrix.md` compares 33 primary sources across all six required areas. `source_verification_log.md` records API, HTML, PDF, and author-source checks and distinguishes deep checks from abstract-only checks. All 33 unique arXiv links returned HTTP 200 during this audit. No priority conclusion is inferred from search absence. |
| F. Outreach email | **PASS** | `drafts/outreach_email.md` is 176 words excluding heading/subject and 189 including the subject. It names the conceptual intersection, compresses the three purposes, accurately describes the first three pages and optional appendix, offers the executable repository only if useful, and explicitly asks for criticism and redirection rather than endorsement or a publication decision. |
| G. Compiled packet and editable sources | **PASS** | `finite_directional_observer_review_packet.pdf` has `%PDF-` signature, 334731 bytes, nine `/Type /Page` objects, 20 link annotations, and expected title metadata. Its order is note, diagram, questions, appendix, bibliography. Canonical editable source is `packet.html`, with `dependency_diagram.svg`, `bibliography.md`, and synchronized Markdown companions retained. |

## Required framing

| Goal item | Result | Evidence and judgment |
| --- | --- | --- |
| 1. Observer register is the headline; approximately 70/25/5 architecture/gravity/Skyrmion | **PASS** | The three-page front matter is dominated by the generic observer chain. Page 1 gives seven architecture/bottleneck blocks, one gravity/realization block, and only one Skyrmion paragraph; page 2 uses a large main chain with Paper R and Paper A as side branches; page 3 asks architecture-level questions. This is the requested approximate hierarchy, not a claimed numerical content measurement. |
| 2. Global-risk relational alignment, never absolute orientation | **PASS** | Page 1 defines `g_rel=g_O^-1 g_D`, a Haar-prior full-group risk, and denies orientation relative to coordinates. The diagram and Appendix A repeat the relational domain. |
| 3. Disciplined `S_dir` usage and first review question | **PASS** | The packet uses the narrower phrase "operational rotational-asymmetry resource" and defines it by relative entropy of `SO(3)` asymmetry. It explicitly distinguishes `S_dir` from effective dimension, Casimir, QFI, thermodynamic entropy, and `S_Ob`. Question 1 asks whether a comparison is meaningful rather than assuming one. |
| 4. Classical record stability rather than generic coherence | **PASS** | Lifetime is defined by achievable relational readout risk after storage time `T`. Page 1 and Appendix A explicitly distinguish this from preservation of arbitrary quantum phase coherence. |
| 5. `B_W` is a witness, not the capacity bottleneck | **PASS** | Page 1, page 2, page 6, and `adversarial_audit.md` state that only a nonzero fixed-background response would witness gravitational non-invisibility. They deny that `B_W` is a capacity bound and leave the relevant invariant open. |
| 6. Skyrmion is removable realization support | **PASS** | The abstract chain, theorem sketch, common-action bottleneck, and three questions remain meaningful with the Skyrmion paragraph and Paper A card removed. Paper A is explicitly a hard-wall fixed-de Sitter support branch, not a premise of the observer architecture. |
| 7. Microscopic preparation/storage/readout channel is primary bottleneck | **PASS** | Page 1 labels the common-action record channel open. Appendix A separates the exact stipulated heat-channel implication from the missing KMS-to-effective norm control, acquisition, storage, readout, stress ledger, and common parameter window. |
| 8. Compact theorem sketch with declared quantifiers | **PASS** | Page 1 declares `C_dir` over localized register-target models, states, environments, local actions, and preparation/storage/readout protocols, then gives one three-line schematic theorem chain. The Markdown companion states the static-patch KMS environment explicitly. |
| 9. Detailed numerics stay in the optional appendix | **PASS** | Page 1 contains no implementation decimal constants or hashes. Interval values, residual losses, and certificate hashes occur only on pages 4-8. |
| 10. No unsupported novelty or priority claim | **PASS** | Page 8 and page 9 deny a priority conclusion; `literature_matrix.md` identifies nearest neighbors and narrow distinctions; `source_verification_log.md` records nonexhaustive search limits. No "first" or "breakthrough" claim is made. |

## Claim discipline

| Boundary | Result | Evidence |
| --- | --- | --- |
| Consistent status labels | **PASS** | Diagram and appendix contain all three labels and define their meanings. Composite claims inherit the least-complete ingredient in Appendix A. |
| Current Weyl interval does not exclude zero | **PASS** | Pages 1 and 7 state that no rigorous continuum interval for completed `B_W` presently excludes zero. Exact maps, floating target, partial residuals, and full zero exclusion are kept separate. |
| Common-action physical channel remains open | **PASS** | Page 1, page 2, page 4, and page 8 label it **[OPEN]**. |
| `S_dir` is not `S_Ob` | **PASS** | Page 1 boundary box, diagram caveat band, Appendix A, and question 1 make the non-identification explicit. |
| Self-gravity, Israel matching, and closed-universe path integral excluded | **PASS** | Pages 6 and 8 exclude self-consistent rotating Einstein-Skyrme geometry and completed tensorial Israel matching; page 8 states that a closed-universe path integral is outside the claims. |
| Interval overestimate is not a physical no-go | **PASS** | Page 7 calls the partial adjoint loss a representation diagnostic and explicitly says it is not a physical no-go. |

## Acceptance tests

| Test | Result | Evidence |
| --- | --- | --- |
| 1. First page works without Skyrmion knowledge | **PASS** | The operational question, relational task, resource, theorem chain, and bottleneck are established before the single candidate-realization paragraph. Visual inspection found the page compact, readable, and self-contained. |
| 2. At most three equations and no implementation constants on page 1 | **PASS** | Automated result: 3 equation blocks; no `0.xx` implementation decimal matches; 604 words. |
| 3. Domain, task, variable, witness, and open bridge identifiable quickly | **PASS** | `C_dir`, Haar-risk relational alignment, rotational-asymmetry `S_dir`, fixed-background `B_W`, and the open common-action KMS-to-record bridge are each named on page 1. |
| 4. Architecture survives removal of Skyrmion material | **PASS** | The main chain has an independent abstract risk theorem and orbital-matter capacity route. The Skyrmion appears only as one candidate support branch. |
| 5. Technical claims map to evidence or OPEN | **PASS** | `claim_evidence_ledger.md` maps the packet claim surface to theorem identifiers, exact artifacts/hashes, conditional floating evidence, or explicit **[OPEN]** rows. Its focused verification record reports 219 passing tests. |
| 6. Literature entries are checked primary sources | **PASS** | The 33 matrix links are primary arXiv records; all resolved HTTP 200 in the independent link check. `source_verification_log.md` records the verification depth and corrected inherited metadata. |
| 7. Reproducible, unclipped, linked PDF with matching editable source | **PASS** | A build in a temporary copy completed with status 0. Browser DOM measurement reported `data-overflow=false`, `overflow-x=0`, and `overflow-y=0` on all nine sheets. HTML has no missing internal targets; PDF has 20 link annotations. `artifact_manifest.json` binds the final PDF and sources by SHA256. |
| 8. Adversarial conflation review | **PASS** | `adversarial_audit.md` separately checks all five required pairs, plus floating-versus-interval evidence, witness-versus-capacity, channel status, novelty, and outreach posture. |
| 9. No publication-approval request | **PASS** | The email and page 1 ask for conceptual direction, criticism, and redirection and explicitly deny endorsement or a publication decision. Automated forbidden-phrase check passes. |
| 10. Completion handoff contains paths, commands, sources, uncertainties, and open claims | **PASS** | `README.md`, this audit, the verification log, and the ledger provide all required handoff fields. The final user-facing response must relay them and must retain the open-claim list below. |

## Render and build evidence

- Visual proof directory: `output/playwright/harlow-review-packet/`.
- Nine inspected PNGs: `page-01.png` through `page-09.png`, each 816 x 1056.
- Secondary nine-page proof PDF:
  `output/playwright/harlow-review-packet/playwright-review.pdf`.
- Visual inspection at original resolution found no clipping, overlap, missing
  diagram labels, broken cards, or footer collisions. Page 2's branch labels
  remain inside the page and all three question cards fit on page 3. This check
  caught an SVG-internal one-line overflow that the sheet-level DOM metric did
  not detect; the caveat was wrapped, rebuilt, and reinspected before PASS.
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
3. No single local action yet derives acquisition, storage degradation,
   readout, channel error, support stress, and backreaction in one open
   parameter window.
4. No completed rigorous interval for the normalized Skyrmion electric-Weyl
   response presently excludes zero.
5. Tensorial Israel matching and a rotating self-gravitating
   Einstein-Skyrme-de Sitter solution are not supplied.
6. The static-patch construction is not a derivation of Harlow's
   closed-universe observer rule or path integral.

These are scientific review targets, not hidden acceptance failures.
