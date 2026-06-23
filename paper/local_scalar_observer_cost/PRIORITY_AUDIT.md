# Equation-Level Priority Audit

**Status:** no direct subsumption located; specialist verdict remains open

**Audit date:** 2026-06-23

This record distinguishes an actual reduction from a merely similar title or
keyword. It is an internal literature audit, not a substitute for the three
written specialist assessments required by the research goal.

Detailed results are split by reviewer domain:

- [`OPERATOR_NOVELTY_REVIEW.md`](OPERATOR_NOVELTY_REVIEW.md) records eight
  attempted theorem-class reductions and the first failed hypothesis or
  conclusion in each;
- [`QFT_NOVELTY_REVIEW.md`](QFT_NOVELTY_REVIEW.md) gives an equation-level
  channel, support, energy, and achievability matrix;
- [`OBSERVER_CODE_REVIEW.md`](OBSERVER_CODE_REVIEW.md) isolates the
  Harlow-code and branchwise-gravity claims; and
- [`../../docs/local_scalar_observer_proof_audit.md`](../../docs/local_scalar_observer_proof_audit.md)
  is the clean-room correctness audit and independent numerical replay.

## Claim Being Tested

The candidate contribution is not the exact gapless-detector channel, the
existence of a positive compact logarithmic operator, or the Harlow random-code
second moment. It is the conjunction of:

1. the finite-pointer purity and Renyi bound in terms of centered field energy;
2. the thermal fixed-final-support coefficient and optimizer;
3. global bounds and uniform small- and large-support remainders;
4. the strict reduction of every angular and canonical de Sitter sector to
   the same s-wave momentum optimizer;
5. the physical-purity insertion into the observer-code second moment; and
6. the branchwise final-slice backreaction corollary.

## Exact Operator Reductions

### Vacuum: odd logarithmic convolution sector

Let `p_tilde` be the odd extension of `p` from `(0,1)` to `(-1,1)`. For
`0<u<1`,

```text
pi^-1 integral_-1^1 log(1/|u-v|) p_tilde(v) dv
  = integral_0^1 pi^-1 log((u+v)/|u-v|) p(v) dv.
```

Therefore `K_0` is exactly the odd sector of the finite-interval logarithmic
convolution operator studied by [Polosin (2022)](https://doi.org/10.1134/S0012266122090099),
whose [open Russian version](https://sciencejournals.ru/view-article/?a=DeqRus_2209009Polosin&j=deqrus&n=9&v=58&y=2022)
gives high-index eigenvalue and eigenfunction asymptotics separately in the
even and odd sectors. The vacuum parent problem is established prior art.
That paper does not calculate the principal odd eigenvalue, introduce the
thermal deformation, prove the two uniform temperature/support remainders, or
perform the de Sitter sector reduction.

### Finite temperature: odd log-sinh convolution sector

For `tau>0`, define on `(-1,1)` the even convolution kernel

```text
q_tau(z)=-pi^-1 log sinh(tau |z|).
```

The positive-half restriction of convolution by `q_tau` against `p_tilde` is
exactly `K_tau p`; the additive normalization of `q_tau` is irrelevant in the
odd sector. Thus `K_tau` is not an isolated new operator class. The unresolved
question is whether existing finite-interval convolution theory makes its
principal-eigenvalue bounds and uniform `tau` remainders routine.

### Hyperbolic cross-ratio form

Set `r=exp(-2 tau u)` and `s=exp(-2 tau v)`. Then

```text
k_tau(u,v)=pi^-1 log((1-rs)/|r-s|).
```

The right side is the logarithm of inverse pseudo-hyperbolic distance for two
points on a diameter of the Poincare disk. The Hilbert-space measure becomes
`dr/(2 tau r)` on `(exp(-2 tau),1)`. This makes `K_tau` a weighted
one-dimensional geodesic compression of the hyperbolic logarithmic Green
kernel. [Johnson and Verma (2026)](https://arxiv.org/abs/2601.20431) study the
largest eigenvalue of the same kernel on two-dimensional hyperbolic domains
with hyperbolic area measure; their theorem does not directly cover this
geodesic-supported measure, which is singular relative to hyperbolic area.
[Anoop and Johnson (2025)](https://arxiv.org/abs/2501.13569)
study largest eigenvalues for Euclidean logarithmic potentials, again with a
different domain and measure.

## Primary Comparator Outcomes

| Source | Equation-level outcome | Present effect |
| --- | --- | --- |
| [Polosin 2022](https://doi.org/10.1134/S0012266122090099) | Exact vacuum parent operator and odd sector; high-index spectral asymptotics | Vacuum convolution is prior art; finite-temperature principal law remains unresolved |
| [Anoop and Johnson 2025](https://arxiv.org/abs/2501.13569) | Largest eigenvalues of Euclidean logarithmic potentials | Relevant principal-eigenvalue theory, but no direct domain/measure reduction found |
| [Johnson and Verma 2026](https://arxiv.org/abs/2601.20431) | Same pseudo-hyperbolic-distance kernel on two-dimensional domains | Exact kernel relation found; their measure and geometry differ |
| [Widom 2006](https://arxiv.org/abs/math/0605076) and [Kozlowski 2008](https://arxiv.org/abs/0805.3902) | Singular truncated Wiener-Hopf inverses and determinants | Nearby operator machinery; no top-norm or uniform-remainder reduction located |
| [Ponomarev 2021](https://arxiv.org/abs/2103.11923) | Finite-interval convolution eigenproblems | Its smoothness and decay hypotheses fail for the singular, linearly growing log-sinh parent kernel |
| [Didenko and Silbermann 2016](https://arxiv.org/abs/1607.04944) | Wiener-Hopf plus Hankel kernel/cokernel theory | Requires bounded Wiener-algebra symbols; `|xi|^-1 coth(beta|xi|/2)` is unbounded at zero |
| [Singh and Dhaliwal 1979](https://doi.org/10.1017/S0013091500016369) | Explicit dual-integral solution with a nearby hyperbolic logarithmic kernel | Different `tanh` multiplier and an additional cosh ratio; no diagonalization of the present kernel |
| [Barcellos and Landulfo 2021](https://arxiv.org/abs/2109.13896) | Separates background field energy, switching work, and communication work for the exact channel | Establishes energy accounting, not fixed-final-support optimization |
| [Aspling and Lawler 2023](https://arxiv.org/abs/2309.07218) | UDW communication channels represented as bosonic dephasing channels | Establishes another dephasing-channel representation, not the support-energy optimum |

## Current Internal Disposition

**DISTINCT CONJUNCTION, MEDIUM PRIORITY RISK, external gate open.** The search
found material prior art that narrows the novelty claim. It did not find a
theorem that supplies all of the thermal principal-support coefficient, both
uniform remainders, and the strict de Sitter full-sector reduction.

The main risk is now sharper: an operator specialist may judge the thermal
extension and its bounds to be routine once the odd-convolution and
hyperbolic-kernel representations are written down. A **SUBMIT** disposition
requires that reviewer to reject that reduction-to-routine argument, and a
detector/QFT specialist to judge the physical conjunction useful enough for a
short paper.

The detector audit independently reaches the same boundary. The exact Weyl
channel, KMS `coth` covariance, factor-of-two normalization, and source-field
energy accounting are prior art. The first unmatched step is the optimization
of that known covariance at fixed post-switch field energy and compact final
Cauchy support, followed by the de Sitter all-sector theorem.

## Search Boundary

The audit used exact kernel strings, half-line multiplier language,
Wiener-Hopf/Hankel terminology, logarithmic-potential eigenvalue literature,
hyperbolic Green kernels, and detector-energy/channel references. Failure to
locate a direct result is not proof of novelty. The response form therefore
asks reviewers for a theorem-and-normalization map rather than a general
impression.
