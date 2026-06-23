# Integral-Operator and Fractional-Sobolev Novelty Review

## Review Assignment

Determine whether the finite-interval reflected thermal operator below, its
top eigenvalue, and the stated uniform support asymptotics are already standard
or immediate consequences of known operator theory. This is an equation-level
reduction audit, not a request to judge the numerical plot.

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

## Closest Comparators Located Internally

These are comparators, not an exhaustive priority claim.

| Comparator | What appears close | Decisive reduction question |
| --- | --- | --- |
| [Polosin, logarithmic convolution on a finite interval (2022)](https://doi.org/10.1134/S0012266122090099) ([open Russian text](https://sciencejournals.ru/view-article/?a=DeqRus_2209009Polosin&j=deqrus&n=9&v=58&y=2022)) | Exact zero-temperature parent operator; its odd sector is `k_0` | Polosin proves high-index even/odd spectral asymptotics. Does the same finite-interval convolution theory already yield the thermal principal eigenvalue or either uniform support remainder? |
| [Anoop and Johnson, largest logarithmic-potential eigenvalues (2025)](https://arxiv.org/abs/2501.13569) | Principal eigenvalues of Euclidean logarithmic potentials | Can their domain and measure be reduced to this odd one-dimensional weighted problem? |
| [Johnson and Verma, hyperbolic logarithmic-potential eigenvalues (2026)](https://arxiv.org/abs/2601.20431) | The same pseudo-hyperbolic-distance kernel on two-dimensional domains | Does their hyperbolic-area theory extend immediately to the weighted geodesic measure `dr/(2 tau r)` and its varying interval? |
| [Widom, truncated Wiener-Hopf inverses and determinants (2006)](https://arxiv.org/abs/math/0605076) | Finite-interval Wiener-Hopf analysis | Does its framework determine this singular reflected operator's exact top norm or either uniform remainder? |
| [Kozlowski, Fisher-Hartwig truncated Wiener-Hopf determinants (2008)](https://arxiv.org/abs/0805.3902) | Singular symbols and interval truncation | Can its determinant asymptotics be converted directly into the claimed top-eigenvalue theorem at all `L/beta`? |
| [Ruzhansky and Suragan, first and second Riesz eigenvalues (2016)](https://arxiv.org/abs/1603.07781) | Positive potential operators and principal eigenvalues | Is the reflected half-line logarithmic kernel a covered geometry or an immediate limiting case? |

The internal audit therefore does **not** claim that the vacuum logarithmic
operator is new. The unresolved priority question is whether the thermal
principal-eigenvalue/support theorem and its physical all-sector use are a
routine extension of this established finite-interval spectral theory.

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
