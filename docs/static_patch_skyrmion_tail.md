# Exact Continuum Tail Of The Signed Skyrmion Factor

Status: proved global exact-profile `H^2` membership and certified all six
global derivative norms entering an exact-rational `p^-5` tail envelope. The
conservative directed AU.3a join and authenticated profile-resolved AU.3b
baseline are complete; AU.3b is presently dominated by this conservative tail.

## Continuum Optical Weights

Let `lambda=(e f_pi R)^-2`,

```text
x(y)=tanh(y)/sqrt(lambda),
Y=atanh(sqrt(lambda)x_w),
N_w=1-lambda x_w^2.
```

For the inertia density `rho_I` used by the matter-current form factor, define

```text
W(y)=[rho_I(x(y))/x(y)^2] dx/dy
    =2pi sin(F)^2/(3sqrt(lambda))
      [1+4lambda cosh(y)^2 F_y^2
       +4lambda coth(y)^2 sin(F)^2],
A(y)=W(y)coth(y).                                    (1)
```

The exact numerator and form factor are

```text
N(p)=p^-1 int_0^Y A(y)sin(py)dy-int_0^Y W(y)cos(py)dy,
H_Sky(p)=C N(p)/(1+p^2),
C=3/(lambda I).                                      (2)
```

Equation (2), rather than the finite radial trapezoid, is the object used for
the continuum tail proof.

## Endpoint Jets

At the origin, write

```text
F(x)=pi-bx+cx^3+O(x^5),
c=b[mu^2-4lambda+(4/3-24lambda)b^2+(8/3)b^4]
  /[10(1+8b^2)].                                     (3)
```

Then

```text
W(y)=w_0 y^2+O(y^4),
A(y)=w_0 y+O(y^3),
w_0=2pi b^2(1+8b^2)/(3lambda^(3/2)).                 (4)
```

At the hard wall, put `sigma=|F_x(x_w)|`. If both `F(x_w)` and `F_x(x_w)`
vanished, ODE uniqueness would force the zero solution, so the nontrivial
`B=1` branch has `sigma>0` without needing a separate sign convention for the
wall derivative. For `delta=Y-y`,

```text
W(y)=w_Y delta^2+O(delta^3),
A(y)=coth(Y)w_Y delta^2+O(delta^3),
w_Y=2pi sigma^2 N_w^2(1+4N_w sigma^2)/(3lambda^(3/2)),
W''(Y)=2w_Y>0.                                       (5)
```

The quadratic wall zero is essential. A finite-pinning profile with
`F(x_w) != 0` generically loses this cancellation and only gives a `p^-3`
form factor.

## Boundary-Aware Tail Bound

For `m=0,1,2`, define

```text
M_m^W=||d_y^3(y^m W)||_1,
M_m^A=||d_y^3(y^m A)||_1,
B_m=Y^m W''(Y)+M_m^W,
D_m=Y^m coth(Y)W''(Y)+M_m^A.                         (6)
```

The proof works on the closed half interval. It does not extend the weight by
zero and incorrectly call that extension `W^{3,1}`: the wall second derivative
jumps under zero extension. Three integrations by parts retain the wall term.
The profile ODE is analytic away from its regular endpoints, while (3)-(5)
provide one-sided endpoint extensions. Hence all six norms in (6) are finite
for the exact solution. For the AU.1-certified default profile, exact rational
interval arithmetic now gives

```text
(M_0^W,M_1^W,M_2^W)
 <= (257768617.27020434,6946570.05661323,298269.008103853),
(M_0^A,M_1^A,M_2^A)
 <= (37317164258.63237,505644130.0063133,13919447.36624204). (6a)
```

The displayed decimals are upward-bound summaries of archived exact fractions,
not the proof representation.
For `p>=P>=1`, set

```text
E_0=B_0+D_0/P,
E_1=B_1+D_1/P+D_0/P^2,
E_2=B_2+D_2/P+2D_1/P^2+2D_0/P^3.                    (7)
```

Then

```text
|N^(k)(p)| <= E_k p^-3,                              k=0,1,2,
|H(p)|   <= C E_0 p^-5,
|H'(p)|  <= C(E_1+2E_0/P)p^-5,
|H''(p)| <= C(E_2+4E_1/P+6E_0/P^2)p^-5.             (8)
```

The executable function
`skyrmion_sharp_form_factor_tail_envelope` evaluates (6)-(8) once rigorous
upper bounds for the six `M_m` values and rigorous endpoint/prefactor data are
supplied. Its ordinary-float output records the exact formula but is not
outward-rounded; theorem constants must evaluate the same formula in directed
interval arithmetic. It never estimates the inputs from the finite-frequency
trapezoid.

The companion module `qgtoy.validated_skyrmion_spectral_ledger` now performs
the endpoint and envelope algebra with exact rational intervals. It accepts a
fully certified AU.1 physical-observable result, checks that the wall slope and
inertia are composed from that same Newton tube, and records `Y`, `N_w`, `C`,
`W''(Y)`, `A''(Y)`, and the leading wall amplitude with certificate identity.
Six supplied derivative-norm bounds must carry the same identity before the
tail formula is evaluated. Since (8)--(10) prove upper bounds rather than
positive lower bounds, the actual squared tail integrals are serialized as
`[0,U_k]`. A separately identified point interval for the physical radius
records both the scaling `R^(2k-4)` and the physical join frequency `P/R`.

AU.2 is complete. On `[1/16,4]`, interval Taylor jets and conservative flux
reconstruction give exact upper sums on the 43 AU.1 cells. At the singular
origin, the variables `t=x^2`, `pi-F=xu`, and the Volterra identity for the
momentum produce a regular vector field. Fourth-order multivariate interval AD
and Lie derivatives bound the required third optical derivatives without
differentiating the Newton remainder. Exact addition of the two regions gives
(6a), and the certificate-linked ledger evaluates the tail formula.

## Sharp Asymptotic And Global H2

The Riemann-Lebesgue lemma applied after the boundary terms gives

```text
H(p)  =C W''(Y) sin(pY)/p^5+o(p^-5),
H'(p) =C Y W''(Y) cos(pY)/p^5+o(p^-5),
H''(p)=-C Y^2 W''(Y) sin(pY)/p^5+o(p^-5).            (9)
```

All three derivatives have the same power because differentiation acts on the
wall phase. Combining (8) with the positive-frequency bare-root bounds gives

```text
|q_Sky^(k)(p)| <= c_k p^(-7/2),                      k=0,1,2. (10)
```

The negative-frequency half is exponentially KMS suppressed. Near zero, the
bare spectrum is positive analytic and `H_Sky` is even analytic. The signed
factor also crosses every simple form-factor zero smoothly. Equations
(8)-(10) therefore prove

```text
q_Sky in H^2(R).                                     (11)
```

This closes the global membership gap left by the finite-window calculation.

## Exact Certificate And Remaining Boundary

The exact archive is

```text
experiments/skyrmion_au2_global_tail_exact_certificate.json
SHA256 1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9
```

It binds the six norms, AU.1 wall slope and inertia, endpoint data, and tail
envelope to one certificate identity. Its independent audit verifies the 43
cell sums and the exact positive-plus-origin composition.

`validated_skyrmion_au3.md` now joins a directed rational finite-band upper sum
to this tail, recomputed at `P=128`, and certifies conservative global
`Q_0,Q_1,Q_2,G,M_1` bounds. Authenticated AU.3b recovers profile-specific
finite-band information at `P=64`, but this tail supplies more than `99.2%` of
each squared global bound and makes its `Q` values weaker than AU.3a. Its
normalized coupling upper caps are rigorous conditional consequences; the
smaller floating values and any physical observer window remain uncertified.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-tail
PYTHONPATH=. python3 experiments/skyrmion_newton_linearization_audit.py \
  --omega 3/4 --tube-radius 1/250 --spectral-trigonometric-terms 24 \
  --origin-kernel-terms 20
```
