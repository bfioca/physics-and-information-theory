# External Review Launch Kit

## Purpose

Two written technical assessments are binding before this manuscript can be
called submission-ready:

1. one from a relativistic detector/QFT specialist; and
2. one from an integral-operator, Riesz-potential, Wiener-Hopf/Hankel, or
   fractional-Sobolev specialist.

The reviews answer different questions. A broad significance review, including
one from Dr. Daniel Harlow, is valuable but does not substitute for either
technical novelty assessment unless it explicitly covers that domain.

Use the public [review branch](https://github.com/bfioca/physics-and-information-theory/tree/codex/paper-u-information-exposure)
or attach the files listed below. Record each response in
`REVIEW_RESPONSE_FORM.md` and preserve the manuscript commit reviewed.
Use `REVIEWER_SHORTLIST.md` for the ranked contact routes. The exact
operator reductions and internal comparator outcomes are recorded in
`PRIORITY_AUDIT.md`.

## Build Frozen Review Bundles

After committing the exact manuscript to be reviewed, run from the repository
root:

```bash
python paper/local_scalar_observer_cost/build_review_packets.py
```

The builder requires a clean tracked worktree and writes two ignored archives
under `dist/local_scalar_observer_review/`. Each archive contains only the
manuscript, the matching specialist brief, the response form, a short reviewer
README, and a machine-readable manifest. The manifest pins the full commit,
commit time, source URL, and SHA-256 digest of every attachment. Rebuilding at
the same commit is byte-for-byte deterministic.

Send the matching archive or its listed contents. Do not rename the archive in
a way that removes the short revision identifier.

## Minimal Attachment Sets

**Detector/QFT reviewer**

```text
main.pdf
QFT_NOVELTY_REVIEW.md
REVIEW_RESPONSE_FORM.md
```

**Operator-theory reviewer**

```text
main.pdf
OPERATOR_NOVELTY_REVIEW.md
REVIEW_RESPONSE_FORM.md
```

Offer `REFEREE_GUIDE.md`, the LaTeX source, and the clean-room proof audit for
a deeper pass. Offer `PRIORITY_AUDIT.md` when the reviewer wants the complete
comparison trail and first-failed-reduction ledger. Do not lead with the full
repository history.

## Detector/QFT Email Draft

**Subject:** Technical novelty check: sharp support-energy bound for exact
thermal dephasing

Dear [Name],

I am seeking a deliberately critical assessment of a short mathematical-
physics manuscript. It takes an established exact gapless-detector dephasing
channel and solves a different problem: the maximum dephasing at fixed post-
switch scalar-field energy and fixed final Cauchy support. It then proves that
the half-line optimizer is the unique full-sector optimizer for a conformal
scalar in a de Sitter static patch.

Would you be willing to tell me whether this constrained theorem is already
known, technically new but insufficient, or suitable for a short paper? The
attached specialist brief identifies the closest detector, communication, and
horizon-decoherence comparisons and asks for an equation-level reduction if
the result is known. The model expressly excludes total apparatus cost and
coupled gravitational dynamics.

The manuscript is 18 pages. Even a concise written disposition using the
response form would be extremely helpful.

Best,
[Name]

## Operator-Theory Email Draft

**Subject:** Novelty check: principal eigenvalue of a reflected thermal
logarithmic kernel

Dear [Name],

I am seeking a technical priority check on a finite-interval positive integral
operator. It can be written as a compressed Dirichlet half-line multiplier
`h^-1 coth(beta h/2)`, as a singular Wiener-Hopf-minus-Hankel form under odd
extension, or as a reflected thermal-cylinder logarithmic kernel. The paper
derives its exact scaling coefficient, simple positive optimizer, global
bounds, and uniform small- and large-support remainders.

Would you be willing to assess whether these results are a known corollary,
new but routine, or a publishable operator application? The attached brief
lists the nearest comparators we located and asks for a precise reduction if a
standard theorem subsumes the result. A short response using the included form
would close a decisive publication gate.

Best,
[Name]

## Harlow Framing Email Draft

**Subject:** Request for candid feedback on a narrow de Sitter detector bound

Dear Dr. Harlow,

I am developing a short paper about a constrained observer-resource question
in a de Sitter static patch. The rigorous result is narrow: for an established
exact thermal dephasing channel, it finds the sharp dephasing attainable at
fixed post-switch field energy and fixed final Cauchy support, including the
unique optimizer across all angular and canonical sectors. It does not claim a
universal observer theorem, total measurement cost, or an ER=EPR result.

I would value your candid view on whether this is a useful building block for
gravitational observer questions and whether the framing isolates the right
physics. I am separately seeking detector/QFT and operator-theory priority
reviews, so this request is for significance and direction rather than
endorsement.

I have attached the 18-page manuscript and a one-page referee guide.

Best,
[Name]

## Review Handling

1. Freeze the commit hash and date sent.
2. Ask for a source or explicit reduction whenever the response is "known."
3. Ask for one minimum bounded addition whenever the response is
   "insufficient."
4. Integrate corrections before soliciting a second opinion on a superseded
   draft.
5. Report the outcome as external feedback, not approval or endorsement.
6. Authorize `SUBMIT` only if both domain novelty gates pass and the combined
   external record gives every central claim at least one `PASS` or `CORRECT`.
   An item marked `NOT REVIEWED` by every reviewer remains open.

The publication decision remains **SUBMIT**, **STRENGTHEN**, or **NO-GO** under
the goal contract. Silence or a polite general reaction does not close a gate.
