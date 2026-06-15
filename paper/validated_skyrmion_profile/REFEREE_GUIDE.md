# Referee Guide

Review snapshot: `paper-a-review-v1`

This guide is the shortest path through the computer-assisted proof package.
The manuscript is a narrow specialist result, not a claim about a universal
observer theorem or self-gravitating Skyrmion.

## The Result

At `mu^2=1`, `lambda=1/400`, and Dirichlet radius `x_w=4`, the paper proves:

- existence and local uniqueness in the stated augmented Newton ball;
- strict monotonicity, negative wall slope, and finite positive rotor inertia;
- a qualitative locally unique analytic branch in mass, curvature, and wall
  radius, without a certified numerical width;
- a fixed-wall `l=0` Friedrichs radial frequency gap; and
- a sharp, nonzero, boundary-controlled `p^-3` tail for the unfiltered optical
  inertia transform.

## Read First

1. `main.pdf`: the complete manuscript.
2. `sections/introduction.tex`: prior-art comparison and novelty boundary.
3. `sections/model_and_theorem.tex`: precise spaces, theorem, and analytic
   parameter branch.
4. `sections/validated_proof.tex`: Volterra and Newton-Kantorovich proof.
5. `sections/consequences.tex`: radial gap and transform-tail consequences.
6. `sections/reproducibility.tex`: full replay commands and validation boundary.

## Proof Artifacts

| Result | File | SHA-256 prefix |
| --- | --- | --- |
| Profile and spectral data | `experiments/skyrmion_au2_global_tail_exact_certificate.json` | `1d5fe53786cc` |
| Fixed-wall radial gap | `experiments/skyrmion_full_radial_gap_exact_certificate.json` | `695310609d07` |
| Sharp-tube proof input | `experiments/skyrmion_au3b_sharp_tube_snapshot_exact.json` | `1781a2ff357f` |

## Fast Verification

From the repository root:

```bash
python -m pip install -e . 'pytest>=8,<10'
python paper/validated_skyrmion_profile/audit_package.py
python -m pytest -q \
  tests/test_validated_skyrmion_profile_manuscript.py
```

The first audit verifies the checked PDF, build log, manuscript sources,
certificate hashes, source ledgers, references, labels, page count, and three
displayed tail bounds. Full clean-replay commands are in the manuscript's
reproducibility section; the combined AU.1/AU.2 replay is intentionally slow.

## Trust Boundary

- `qgtoy/skyrmion_global_bvp_certificate_generator.py` proposes rational
  candidates but has no theorem-acceptance authority.
- `qgtoy/validated_interval.py` and `qgtoy/validated_rational_text.py` supply
  exact rational interval and archive-parsing primitives.
- The `validated_skyrmion_*` modules recompute profile, origin, spectral, and
  radial inequalities with directed bounds.
- The four `experiments/skyrmion_*_audit.py` drivers authenticate inputs,
  compose validators, and make exact final comparisons.
- Decimal summaries, plots, and manuscript presentation are not theorem
  inputs. Candidate generation may suggest; exact validation decides.

The source ledgers pin fourteen application files. The manuscript gives a
grouped table of proposal, validation, closing-comparison, presentation, and
audit/replay roles. These hashes establish provenance; they do not turn the
implementation into a minimized or formally verified trusted kernel.

## Not Claimed

The paper does not claim global uniqueness, a moving-wall or membrane model,
nonspherical or nonlinear stability, self-consistent gravity, smooth-
confinement robustness, a detector bath factor, an observer algebra, or a new
general Fourier/Hankel endpoint theorem.

## Priority Question

> Is the conjunction of a massive fixed-de-Sitter finite-Dirichlet profile,
> augmented local-uniqueness certificate, fixed-wall radial gap, and
> authenticated inertia-transform tail sufficiently distinct from the
> existing Skyrmion and validated-numerics literature for a specialist
> mathematical-physics paper?

The paper-specific `CITATION.cff` records the immutable review tag and preferred
manuscript citation. For journal submission, the remaining nontechnical
metadata are the author's preferred affiliation/contact line and, if
available, an archival DOI.
