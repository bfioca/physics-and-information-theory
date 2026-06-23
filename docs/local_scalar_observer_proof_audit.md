# Internal Proof Audit: Final-Support Thermal Dephasing

Status: internal analytic pass; independent human proof review remains open

This audit targets the five steps most likely to control correctness of the
strengthened paper. It is not a novelty review and is not independent of the
derivation.

## 1. General Thermal Half-Line Theorem

For Dirichlet half-line momentum data supported in `[0,L]`,

```text
Gamma_beta[p]=<p,h_0^-1 coth(beta h_0/2)p>,
E[p]=||p||_2^2/2.
```

Compression to `[0,L]` gives the exact kernel

```text
B_beta,L(x,y)=pi^-1 log{
  sinh[pi(x+y)/beta]/sinh[pi|x-y|/beta]}.
```

Under `x=Lu`, this operator is unitarily equivalent to
`L K_(pi L/beta)`. Therefore

```text
sup Gamma_beta/E = 2 ||B_beta,L||
                 = 2 L Lambda(pi L/beta).
```

The logarithmic singularity is square integrable, the kernel is strictly
positive away from null sets, and the operator is positive by its spectral
definition. The Perron-Jentzsch conclusion therefore gives a simple top
eigenvalue and a positive optimizer. **Internal result: PASS.**

## 2. All-Angular Ordering

The conformal de Sitter partial-wave operators obey

```text
A_l=A_0+l(l+1)/(R^2 sinh^2(x/R)) >= A_0.
```

The exact expansion

```text
h_l^-1 coth(beta h_l/2)
 = (2/beta) A_l^-1
   + (4/beta) sum_(n>=1) [A_l+(2 pi n/beta)^2]^-1
```

contains only order-decreasing resolvents. Hence every `l>0` momentum form is
bounded by the `l=0` form. Strictness follows because equality in one resolvent
term would force the positive angular potential times the resolved vector to
vanish almost everywhere, and therefore the original vector to vanish.
**Internal result: PASS.**

## 3. Coordinate-Sector Domination

For coordinate data supported in `[0,L]`, zero extension gives an
`H_0^1(0,L)` vector. Dirichlet Poincare and Cauchy-Schwarz imply

```text
||q|| <= (L/pi)||h_l q||,
<q,h_l q> <= (L/pi)||h_l q||^2.
```

Using `coth z <= 1+1/z` and `beta=2 pi R` gives

```text
Gamma_q/(E_q R) <= 2y/pi+2y^2/pi^3.
```

The s-wave momentum sector is at least `3y/pi` for
`y<=pi^2/2` and at least `8y^2/pi^3` for `y>=pi^2/3`. These intervals overlap,
so momentum dominates for every `y>0`. Strict thermal enhancement excludes a
coordinate tie at the endpoints. **Internal result: PASS.**

## 4. Uniform Remainder Bounds

For small `tau`, Euler's product gives

```text
0 <= log[(sinh A/A)/(sinh B/B)] <= (A^2-B^2)/6.
```

With `A=tau(u+v)` and `B=tau|u-v|`, the maximum row integral is
`tau^2/(3 pi)`. Thus

```text
0 <= C_beta(L)-2L Lambda(0) <= 2 pi L^3/(3 beta^2).
```

For large `tau`, split

```text
k_tau=(2 tau/pi) min(u,v)+r_tau.
```

The explicit Dirichlet-resolvent expansion is

```text
r_tau(u,v)=pi^-1 sum_[n>=1] n^-1
  {exp[-2 n tau |u-v|]-exp[-2 n tau (u+v)]}.
```

Every summand is positive in operator order. Extending its row integral from
`(0,1)` to the half-line gives at most `1/(pi tau n^2)`, so monotone
summation and Schur's test yield `||r_tau||<=pi/(6 tau)`. Since
`||min(u,v)||=4/pi^2`,

```text
0 <= C_beta(L)-16L^2/(beta pi^2) <= beta/3.
```

At `beta=2 pi R` these become the stated de Sitter remainders.
**Internal result: PASS.**

## 5. Smooth-Source Closure

Smooth radial momentum profiles supported strictly inside `[0,L]` are dense
in the energy space. On this support,

```text
P_L h^-1 coth(beta h/2) P_L
 <= P_L h^-1 P_L+(2/beta)P_L h^-2 P_L,
```

and the right side is bounded, so the dephasing form is continuous under
`L2` convergence. Cauchy-Schwarz gives uniform convergence of cumulative
energy measures. For each smooth target datum, a cutoff homogeneous solution
with `J=P(eta phi_free)` is a smooth compact source producing that datum when
the source worldtube contains a strict optical transition margin.

This proves sharpness for final support and for source worldtubes approaching
the final-support ball. It does not prove near-controllability from every
fixed smaller source cylinder. **Internal result: PASS WITH EXPLICIT SCOPE.**

## Remaining Independent Checks

- Verify all normalization factors in the general-`beta` quotient and the
  de Sitter specialization.
- Check the strict resolvent-order argument and the exclusion of coordinate
  ties.
- Check the row-integral estimate used for the large-support remainder.
- Check the cutoff-source support statement in the conformal optical geometry.

No **SUBMIT** decision is authorized until an independent reader signs off on
these items and the two-domain novelty review is complete.
