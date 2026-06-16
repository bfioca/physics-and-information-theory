# Harlow Review Packet

This directory contains a review-ready packet asking whether a finite,
localized directional record is a useful concrete model for the observer
subsystem in quantum-gravity observer rules.

## Sendable files

- `finite_directional_observer_review_packet.pdf` - the compiled nine-page
  review packet.
- `drafts/outreach_email.md` - the standalone email draft (under 200 words).

Recommended sharing order: attach the compiled PDF and use the email draft.
Do not lead with the raw branch URL; offer the executable repository and
certificates only if they would help the review.

## Editable and audit sources

- `packet.html` - canonical print source for the compiled packet.
- `dependency_diagram.svg` - standalone one-page dependency map.
- `bibliography.md` - verified short bibliography used by the packet.
- `drafts/` - independently reviewable Markdown drafts of the conceptual
  note, three questions, technical appendix, and email.
- `literature_matrix.md` - 43-source nearest-neighbor comparison.
- `source_verification_log.md` - primary-source verification record and known
  literature limits.
- `claim_evidence_ledger.md` - theorem/artifact/status map governing every
  technical claim.
- `adversarial_audit.md` - conflation and overclaim audit.
- `requirement_audit.md` - acceptance-test results.
- `artifact_manifest.json` - source and output hashes from the final build.

## Build

The renderer needs a Chromium-family executable. Set `CHROME_BIN` explicitly,
or install Playwright's headless Chromium runtime:

```bash
npx --yes --package @playwright/cli playwright install chromium-headless-shell
```

Then run:

```bash
CHROME_BIN=/path/to/chrome-headless-shell \
  docs/harlow_review_packet/build_packet.sh
node docs/harlow_review_packet/audit_packet.mjs
```

The build script also checks browser-reported overflow on every explicit page.
The audit checks page structure, the three-equation opening limit, the exact
three-question page, full email length, required claim boundaries, internal
HTML links, bibliography links, diagram statuses, PDF signature/page count,
link annotations, title metadata, and source/output hashes.

The packet deliberately does not claim a complete physical observer theorem.
The rigid-detector sprint proves a regular-Gaussian-bath finite-switch lemma and
gives a conditional named-QFT degradation box. The KMS GNS/Araki-Woods channel
bridge remains open, while unchanged promotion of the exact factorized density
to microcausal local matter ends in **INCONCLUSIVE STOP**. The bounded Paper R
sprint also ended in
**INCONCLUSIVE STOP**: its corrected fixed-background response estimator is
stably negative, but the rigorous full interval contains zero. The common-
action local-matter record channel, the `S_dir`-to-`S_Ob` dictionary, and the
gravitational quantity relevant to observer capacity remain open.
