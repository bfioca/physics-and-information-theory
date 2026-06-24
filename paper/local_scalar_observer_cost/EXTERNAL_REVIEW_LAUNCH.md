# External Review Launch Kit

## Purpose

Three written assessments are binding before this manuscript can be called
submission-ready:

1. relativistic detector/QFT novelty and model interpretation;
2. integral-operator novelty and proof scope; and
3. observer-code correctness, significance, and gravity framing.

No one review substitutes for another unless it explicitly covers that
domain. Use the public
[repository](https://github.com/bfioca/physics-and-information-theory)
or send the minimal packet below. Preserve the reviewed commit and record each
response in `REVIEW_RESPONSE_FORM.md`.

## Build Frozen Review Bundles

After committing the exact manuscript, run from the repository root:

```bash
python paper/local_scalar_observer_cost/build_review_packets.py
```

The builder requires a clean tracked worktree and writes three ignored
archives under `dist/local_scalar_observer_review/`. Each archive contains
only the manuscript, matching specialist brief, response form, short README,
and machine-readable manifest. The manifest pins the full commit, time, source
URL, and SHA-256 digest of every attachment. Rebuilding at the same commit is
byte-for-byte deterministic.

## Formal Review Attachment Sets

These sets are for a second-stage formal review. For an initial warm
introduction to Dr. Harlow, send direct links only to `main.pdf` and
`OBSERVER_CODE_REVIEW.md`. Do not attach `REVIEW_RESPONSE_FORM.md` unless he
invites a formal follow-up.

**Detector/QFT**

```text
main.pdf
QFT_NOVELTY_REVIEW.md
REVIEW_RESPONSE_FORM.md
```

**Operator theory**

```text
main.pdf
OPERATOR_NOVELTY_REVIEW.md
REVIEW_RESPONSE_FORM.md
```

**Observer code and gravity**

```text
main.pdf
OBSERVER_CODE_REVIEW.md
REVIEW_RESPONSE_FORM.md
```

Offer `REFEREE_GUIDE.md`, LaTeX sources, or the proof notes only when useful.
Do not lead with repository history.

## Detector/QFT Email Draft

**Subject:** Technical novelty check: localized energy bound for finite
pointer records

Dear [Name],

I am seeking a critical assessment of a mathematical-physics manuscript. It
starts from an established exact controlled-displacement channel and derives a
finite-pointer purity bound at fixed post-switch scalar-field energy and final
Cauchy support. The pairwise coefficient is exact, and for a conformal scalar
in de Sitter its s-wave momentum profile is the unique optimizer across all
angular and canonical sectors.

Would you be willing to say whether this constrained result is already known,
technically new but insufficient, or suitable for a short paper? The attached
brief identifies the closest detector, communication, and horizon-decoherence
comparisons. The model expressly excludes total apparatus cost and autonomous
probe stress.

The manuscript is 23 pages. A concise written disposition would be extremely
helpful.

Best,
[Name]

## Operator-Theory Email Draft

**Subject:** Novelty check: reflected thermal logarithmic operator

Dear [Name],

I am seeking a technical priority check on a finite-interval positive
operator. It is the compression of `h^-1 coth(beta h/2)` on the Dirichlet
half-line, equivalently a Wiener-Hopf-minus-Hankel form or reflected
log-sinh kernel. The paper derives its exact scaling coefficient, simple
positive optimizer, global bounds, and uniform small- and large-support
remainders.

Would you be willing to assess whether these are a known corollary, new but
routine, or a publishable operator application? The attached brief records the
nearest reductions and the first hypothesis that fails in each.

Best,
[Name]

## Harlow Framing Email Draft

**Subject:** Question about Eq. (4.2) and a localized field record

Hi Dr. Harlow,

[Mutual friend's name] suggested I send this to you. I've written a manuscript
prompted by your observer paper with Usatyuk and Zhao. In a solvable localized
scalar-field model, a finite pointer becomes entangled with conditional field
records, and I derive an exact bound on the record's second Renyi entropy in
terms of its final support and centered post-switch field energy.

The narrow point I'd value your judgment on is the connection to your simple
random code. I model a nonideal physical field record in place of the ideal
pointer-basis clone. For an orthogonal CRT-real matter pair, Eq. (4.2) then
appears to reduce exactly to

```text
E_O |<phi|Vhat^dagger Vhat|psi>|^2
 = D/(D+2) Tr(rho_record^2),
```

so the field bound gives a floor on the Haar-averaged squared inner-product
fluctuation. I also include a deliberately limited branchwise final-slice
constraint corollary.

Would you be willing to tell me whether that replacement is legitimate and
whether the connection is useful enough to pursue? A brief "the algebra is
right, but the framing is not useful" would also be very helpful. The relevant
code argument is summarized in the short note below; I am not asking you to
review the operator-theory proof.

Manuscript (PDF):
https://raw.githubusercontent.com/bfioca/physics-and-information-theory/main/paper/local_scalar_observer_cost/main.pdf

Focused observer-code note:
https://github.com/bfioca/physics-and-information-theory/blob/main/paper/local_scalar_observer_cost/OBSERVER_CODE_REVIEW.md

Best,
Brian

## Review Handling

1. Freeze the commit hash and date sent.
2. Ask for a source or explicit reduction whenever a response says the result
   is known.
3. Ask for one minimum bounded addition whenever the response says the result
   is insufficient.
4. Integrate corrections before soliciting review of a superseded draft.
5. Report responses as external feedback, not approval or endorsement.
6. Authorize `SUBMIT` only if all three domain gates pass and every central
   claim has external `PASS` or `CORRECT` coverage.

Silence or a polite general reaction does not close a gate.
