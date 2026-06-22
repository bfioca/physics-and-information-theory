# Integral-Operator and Fractional-Sobolev Novelty Review

## Result Under Review

Let `h=sqrt(-d^2/dx^2)` on the Dirichlet half-line. For momentum data supported
in `[0,L]`, define

```text
C_beta(L)=sup <p,h^-1 coth(beta h/2)p>/(||p||_2^2/2).
```

The paper proves

```text
C_beta(L)=2 L Lambda(pi L/beta),
k_tau(u,v)=pi^-1 log{
  sinh[tau(u+v)]/sinh[tau|u-v|]}.
```

It also proves simplicity and positivity of the optimizer, global two-sided
bounds, and the uniform remainders

```text
0 <= C_beta(L)-2L Lambda(0) <= 2 pi L^3/(3 beta^2),
0 <= C_beta(L)-16L^2/(beta pi^2) <= beta/2.
```

## Questions

1. Is this compressed reflected KMS kernel a named or previously analyzed
   operator in localized negative-Sobolev, Riesz-potential, Wiener-Hopf,
   Hankel, or Slepian-type concentration theory?
2. Does the exact coefficient follow immediately from a standard theorem once
   the kernel is written down, or is identifying and analyzing this operator a
   publishable application?
3. Are either global remainder bound or the explicit maximizing-row formula
   already standard?
4. Is the strict all-angular resolvent comparison in the de Sitter
   specialization mathematically sound?
5. What is the closest established result that the paper must cite or compare
   with directly?

## Requested Response

Return **NOVEL**, **KNOWN COROLLARY**, or **NEW BUT ROUTINE**, with a precise
reference or argument whenever possible. Please inspect the operator-order,
Perron-Jentzsch, and remainder steps rather than the numerical curve.
