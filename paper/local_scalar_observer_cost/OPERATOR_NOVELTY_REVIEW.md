# Integral-Operator and Fractional-Sobolev Novelty Review

## Review Assignment

Determine whether the finite-interval reflected thermal operator below, its
top eigenvalue, and the stated uniform support asymptotics are already standard
or immediate consequences of known operator theory. This operator supplies
the sharp pairwise coefficient in the finite-pointer entropy theorem. This is
an equation-level reduction audit, not a request to judge the numerical plot
or observer-code interpretation.

## Result Under Review

Let `h=sqrt(-d^2/dx^2)` on the Dirichlet half-line and let `P_L` restrict to
`[0,L]`. The paper studies

```text
K_beta,L = P_L h^-1 coth(beta h/2) P_L,
C_beta(L) = sup <p,K_beta,L p>/(||p||_2^2/2).
```

It proves

```text
C_beta(L)=2 L Lambda(pi L/beta),
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

The top eigenvalue `Lambda(tau)` is simple and has a strictly positive
optimizer. The paper also proves a global bracket, an explicit maximizing-row
formula for the upper bound, and the uniform remainders

```text
0 <= C_beta(L)-2L Lambda(0) <= 2 pi L^3/(3 beta^2),
0 <= C_beta(L)-16L^2/(beta pi^2) <= beta/3.
```

## Equivalent Representations To Test

1. **Compressed half-line multiplier.** `K_beta,L` is the compression of the
   Dirichlet half-line spectral multiplier
   `h^-1 coth(beta h/2)`.
2. **Wiener-Hopf minus Hankel form.** Under odd extension, its quadratic form
   is the finite-interval compression of a translation kernel minus its
   reflected image, with singular even symbol
   `a_beta(xi)=|xi|^-1 coth(beta |xi|/2)`. Individual full-line kernels need
   regularization at zero; the odd/reflected difference is finite.
3. **Reflected logarithmic Green kernel.** In position space it is the
   Dirichlet image difference of the thermal-cylinder logarithmic kernel. The
   zero-temperature limit is
   `pi^-1 log((u+v)/|u-v|)`.
4. **Odd finite-interval convolution sector.** If `p_tilde` is the odd
   extension of `p` to `(-1,1)`, then `K_tau p` is the positive-half
   restriction of convolution by
   `-pi^-1 log sinh(tau |u-v|)` against `p_tilde`. At `tau=0`, constants drop
   out of the odd sector and this becomes convolution by
   `pi^-1 log(1/|u-v|)`.
5. **Weighted hyperbolic geodesic kernel.** With
   `r=exp(-2 tau u)` and `s=exp(-2 tau v)`,

   ```text
   k_tau(u,v)=pi^-1 log((1-rs)/|r-s|).
   ```

   This is the inverse pseudo-hyperbolic-distance kernel on a disk diameter,
   acting with measure `dr/(2 tau r)` on `(exp(-2 tau),1)`.

Please test all five descriptions. A negative keyword search in only one
operator vocabulary is not a decisive novelty assessment.

## Completed Internal Reduction Audit

The primary sources below were inspected at theorem and hypothesis level on
2026-06-23. The point of this table is not that searches were negative. It
records the exact map that works and the first place each proposed reduction
stops.

| Operator class | Exact map obtained | Closest primary result | First failed hypothesis or conclusion |
| --- | --- | --- | --- |
| Positive Green and Dirichlet resolvents | `K_tau=(2tau/pi)(-d^2_DN)^-1+r_tau`, and `r_tau` is a positive sum of shifted Dirichlet half-line resolvents | Standard Green/resolvent order | This proves positivity, the leading large-support norm, and a remainder bound. Compression prevents simultaneous diagonalization of the full resolvent sum, so it does not give `Lambda(tau)` or the small-support law. |
| Localized `H^-1/2` inequality | At `tau=0`, the quotient is exactly the odd-extension `H^-1/2(R)` form restricted to `(0,1)` | [Polosin 2022](https://doi.org/10.1134/S0012266122090099) gives the exact finite-interval logarithmic parent | The located theorem gives high-index even/odd spectral asymptotics, not the principal odd eigenvalue or a sharp closed best constant. The thermal multiplier is absent. |
| Euclidean logarithmic/Riesz potential | The vacuum kernel is a reflected one-dimensional logarithmic potential | [Anoop and Johnson 2025](https://arxiv.org/abs/2501.13569) and [Ruzhansky and Suragan 2016](https://arxiv.org/abs/1603.07781) study domain extremals for positive distance kernels | Their conclusions optimize over Euclidean or constant-curvature domains with the ambient volume measure. They do not compute the norm of this fixed reflected interval operator. Anoop-Johnson also documents failures in an earlier logarithmic-potential rearrangement argument, so that route cannot be imported casually. |
| Hyperbolic logarithmic potential | `r=e^-2tau u` gives exactly `pi^-1 log((1-rs)/|r-s|)` | [Johnson and Verma 2026](https://arxiv.org/abs/2601.20431) prove compactness, positivity, simplicity, and domain rearrangement for the same disk Green kernel | Their operator acts on a two-dimensional hyperbolic domain with hyperbolic area. Ours acts on one diameter with `dr/(2tau r)`, a measure singular to area and not hyperbolic arclength. The first measure hypothesis fails. |
| Concentration/Slepian operator | Both problems are finite compressions of spectral multipliers | [Slepian and Pollak 1961](https://doi.org/10.1002/j.1538-7305.1961.tb03976.x) treats a band projection and its sinc kernel | `h^-1 coth(beta h/2)` is an unbounded low-frequency weight, not a band projection; its reflected log-sinh kernel is not sinc. No commuting Sturm-Liouville operator or prolate eigenvalue formula follows. |
| General smooth finite convolution | Odd extension makes `K_tau` a finite-interval convolution sector | [Ponomarev 2021](https://arxiv.org/abs/2103.11923) gives small/large interval methods for smooth decaying kernels with regular monotone Fourier transforms | `-log sinh(tau|x|)` is logarithmically singular at zero and grows linearly at infinity. It fails the stated `C^2`, decay, and finite-Fourier-transform hypotheses before the asymptotic theorem applies. |
| Totally positive, rearrangement, and Perron-Frobenius methods | Pointwise strict positivity makes the compact operator positivity improving | Perron-Jentzsch and the rearrangement results above | These results give a simple positive optimizer and, in domain problems, geometric ordering. They do not determine the fixed-domain top eigenvalue or either uniform `tau` remainder. Total positivity of the reflected thermal kernel was not established and is unnecessary for the paper's proof. |
| Wiener-Hopf plus Hankel | Odd extension and reflection give a finite Wiener-Hopf-minus-Hankel compression with `a_beta(xi)=|xi|^-1 coth(beta|xi|/2)` | [Didenko and Silbermann 2016](https://arxiv.org/abs/1607.04944) treats bounded symbols in a Wiener algebra; [Widom 2006](https://arxiv.org/abs/math/0605076) and [Kozlowski 2008](https://arxiv.org/abs/0805.3902) treat inverses or determinants with Fisher-Hartwig structure | `a_beta` behaves as `2/(beta xi^2)` at zero and as `1/|xi|` at infinity, so it is not a bounded Wiener-algebra symbol. The cited conclusions concern kernels/cokernels, inverses, or determinants, not the top norm of this positive finite compression. |
| Classical dual-integral equations | A nearby `tanh` multiplier produces a hyperbolic logarithmic kernel | [Singh and Dhaliwal 1979](https://doi.org/10.1017/S0013091500016369) solves a dual-integral problem with `log[(sinh cx+sinh ct)/(sinh cx-sinh ct)]` | That kernel contains an additional cosh ratio and comes from a different multiplier. It is not `log[sinh(c(x+t))/sinh(c|x-t|)]`, so the explicit inversion does not diagonalize `K_tau`. |

### What the reductions do settle

- The vacuum finite-interval convolution problem is established prior art.
- Compactness, positivity, simplicity, and the positive optimizer are standard
  consequences once the kernel is identified.
- The large-support leading operator is the elementary Dirichlet-Neumann
  Green operator, and the remainder estimate is resolvent bookkeeping.
- None of those facts should be presented as standalone novelty.

### What remains unmatched internally

No inspected theorem supplies, in one normalization, the finite-temperature
principal-support coefficient for every `tau`, both global uniform
remainders, and the strict reduction of the conformal de Sitter canonical and
angular phase space to that coefficient. The closest exact theorem remains
Polosin's vacuum parent problem; the first missing operation is the thermal
deformation of its principal odd sector.

**Internal finding: DISTINCT CONJUNCTION, MEDIUM PRIORITY RISK, EXTERNAL
VERDICT REQUIRED.** The unmatched part may still be judged routine because
its proof uses standard compact-operator, Schur, and resolvent arguments. That
is a significance judgment, not a reduction already established by the
sources above.

## Decisive Questions

1. Is `K_beta,L` a named operator with an existing exact norm or principal-
   eigenvalue theorem? If yes, give the theorem and the complete map of symbol,
   domain, boundary condition, and normalization.
2. Does a standard theorem immediately give
   `C_beta(L)=2L Lambda(pi L/beta)`, or is that equality only a scaling
   reduction whose substantive content lies in the spectral and asymptotic
   analysis?
3. Are the two global uniform remainders, including their explicit constants,
   known corollaries? Pointwise or formal asymptotics are not equivalent.
4. Is the row-sum maximizer and resulting global upper bound standard for this
   reflected log-sinh kernel?
5. Is the strict angular resolvent comparison used in the de Sitter
   specialization correct, and is that full-sector reduction already known?
6. What is the closest source missing from the paper, even if it does not
   subsume the theorem?

## Requested Disposition

Return one of the following in `REVIEW_RESPONSE_FORM.md`:

- **NOVEL:** no known theorem immediately supplies the central conjunction;
  explain which part is genuinely additive.
- **KNOWN COROLLARY:** give a precise source and equation-level reduction of
  the claimed coefficient and asymptotics.
- **NEW BUT ROUTINE:** explain why the derivation is not substantial enough
  for a standalone short paper and name the minimum addition that would change
  that judgment.

Please separate a proof error from a priority result. Either may force
**STRENGTHEN** or **NO-GO**, but they require different actions.
