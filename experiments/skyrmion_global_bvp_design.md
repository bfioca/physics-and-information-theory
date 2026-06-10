# Global residual/coercivity prototype for AU.1

Status: exploratory design and floating-point evidence only. This note and the
companion probe do not alter or extend the trusted AU modules.

## 1. Variational linearization

Put

```text
N = 1 - x^2/400,
U = x^2 + 8 sin(F)^2,
P = N U,
W = sin(F)^2 + 2 sin(F)^4/x^2 + x^2(1-cos(F)).
```

Four times the reduced energy is

```text
4 E(F) = integral [P(F,x) F'^2/2 + W(F,x)] dx.
```

The Euler-Lagrange residual and its derivative are

```text
G(F) = -(P F')' + P_F F'^2/2 + W_F,
A eta = -(P eta')' + Q eta,
Q = W_FF + P_FF F'^2/2 - (P_F F')'.
```

Thus the apparent first-derivative perturbation terms cancel. With the profile
equation used to evaluate `F''`, the expanded potential is

```text
Q = 2 cos(2F)
    + [24 sin(F)^2 cos(F)^2 - 8 sin(F)^4]/x^2
    + x^2 cos(F)
    - 8 N' sin(2F) F'
    - 8 N sin(2F) F''
    - 8 N cos(2F) F'^2.
```

For a rational approximate profile it is cleaner to use its certified second
derivative directly, since `A=DG(F_bar)` is self-adjoint even when `F_bar` is
not an exact solution.

## 2. Quantitative floating evidence

The probe uses the current floating hard-wall profile with `mu=1`,
`lambda=1/400`, `a=1/16`, and `c=4`. At step `1/2000` it finds

```text
b                         = 1.579953593533
F'(4)                     = -0.08787579992
min/max P                 = 0.08160021, 15.36
min/max Q                 = -1.545955, 41.41019
```

Second-order flux finite differences give

```text
intervals       estimated lambda_1(A_D)
525             7.1657142
875             7.1656166
1575            7.1655785
2625            7.1655676
7875            7.1655621
```

The negative part of `Q` therefore does not indicate a near-zero mode.

## 3. Simple rational Barta comparison

Let

```text
t = x - 1/16,
z = t - 2 = x - 33/16,
v = 1/(1-t/2+t^2/8) = 8/(z^2+4).
```

This function is rational and strictly positive on the closed interval. For a
Dirichlet perturbation `eta`, it need not vanish at the endpoints: integration
by parts gives the ground-state identity

```text
integral [P eta'^2 + Q eta^2]
  = integral P v^2 [(eta/v)']^2
    + integral [(A v)/v] eta^2.
```

The quotient has the certificate-friendly form

```text
(A v)/v = Q + 2 z P'/(z^2+4) + P (8-6z^2)/(z^2+4)^2.
```

On the floating profile its sampled minimum is

```text
inf (A v)/v = 1.6274933 at x approximately 0.874.
```

The value is stable under profile steps `1/400`, `1/800`, and `1/2000`:

```text
1.6275299, 1.6275005, 1.6274933.
```

An exact checker should target the deliberately weaker inequality

```text
A v >= v,
```

leaving about `0.627` of floating margin. This proves

```text
<eta,A eta> >= ||eta||_2^2
```

and hence `||A_D^-1||_(L2 to L2) <= 1`.

Naive endpoint-zero comparisons are materially worse. The best sampled member
of `t(L-t)/(1+alpha t)^m` gives `-2.503`; allowing a quadratic denominator only
improves this to `-1.006`. The obstruction is the large logarithmic curvature
needed near `a`, which then distorts the middle of the interval. Allowing a
positive endpoint value removes that artificial constraint.

## 4. Augmented `(b,F)` block factorization

Let `Phi(b)` and `Gamma(b)` be the exact regular-origin value and derivative at
`a=1/16`. Use the global BVP

```text
G(F) = 0,
F(a) = Phi(b),
F(c) = 0,
F'(a) = Gamma(b).
```

First impose the two Dirichlet conditions and invert `A_D`. The remaining
derivative condition is one scalar Schur complement. If `H` solves

```text
A H = 0,  H(a)=Phi_b,  H(c)=0,
```

then

```text
S = H'(a) - Gamma_b.
```

The floating values are

```text
Phi_b                       = -0.06243711
Gamma_b                     = -0.99698112
H'(a)-Gamma_b               =  2.95967
```

Equivalently, if `Y` is the regular shooting sensitivity and `K` solves
`A K=0`, `K(a)=0`, `K'(a)=1`, then

```text
Y(c) = -6.52418,
K(c) =  2.20436,
S = -Y(c)/K(c) = 2.95967.
```

The floating data suggest a large raw scalar margin before residual correction.

The current generator's finite-difference homogeneous spline is the regular
shooting sensitivity `Y`, not the wall-Dirichlet Schur auxiliary `H`. Its wall
value is about `Y(4)=-6.52421`, so it must not be inserted directly into
`S=H'(a)-Gamma_b`. The corrected untrusted construction is

```text
A K=0,       K(a)=0,       K'(a)=1,
s_hat=-Y(c)/K(c),
H_hat=Y+s_hat K.
```

This gives approximately

```text
K(c)=2.20434843,
s_hat=2.95969864,
H_hat(c)=0,
H_hat'(a)-Gamma_b in [2.95926150,2.96011432].
```

The interval is a raw candidate margin, not a validated Schur bound: the
homogeneous residual and a certified derivative-trace norm must still be
subtracted. A symbolic left lift by `Phi_b-H_hat(a)` consumes the small
origin-value mismatch without pretending that a rational node equals the
unknown exact cutoff sensitivity.

## 5. Proposed rational certificate

The untrusted candidate bundle and trusted checker should contain:

1. A rational `C2` piecewise-polynomial approximate profile `F_bar` on
   `[1/16,4]` and a rational `b_bar`.
2. Rational interval enclosures for `Phi`, `Gamma`, `Phi_b`, and `Gamma_b` from
   a differentiated version of the existing origin contraction.
3. Cellwise residual bounds for `G(F_bar)` and the three boundary residuals.
4. Cellwise interval evaluation of `P`, `P'`, `Q`, and the exact Barta quotient
   above, checking `P>0` and `(A v)/v >= 1`.
5. Rational `C2` approximate fundamental functions `Y_bar,K_bar`, the exact
   rational combination `H_bar=Y_bar-[Y_bar(c)/K_bar(c)]K_bar`, its symbolic
   origin lift, global residual, and endpoint bounds, used to enclose `S` away
   from zero.
6. Cellwise bounds for the second derivative of the nonlinear residual on a
   declared ball, yielding a Newton-Kantorovich Lipschitz constant.

The checker recomputes every interval bound. No step endpoint is used as the
initial condition of the next cell; the cells only bound global polynomial
residuals and coefficient ranges. This removes the wrapping and whole-family
propagation failure mode of interval shooting.

One practical norm choice is `R x (H2 intersect H0^1)` after subtracting the
linear lift of `Phi(b)`. Coercivity supplies the `L2` inverse bound. In one
dimension, `P>=0.08` and `Q>=-1.55` then give routine `H1` and `L-infinity`
bounds. A rational approximate adjoint homogeneous solution can turn the
left-boundary derivative trace into a residual integral, avoiding a fragile
finite-difference estimate of `H'(a)`.

## 6. Remaining obstruction

There is no observed spectral or Barta obstruction. The exact origin-map
derivatives are now exported, the untrusted global rational spline candidate
exists, and the trusted adaptive coefficient/Barta checker proves a quotient
lower bound above `3/2` on the complete 21-cell approximate spline. The missing
trusted work is certificate engineering:

* replace the broad direct whole-cell nonlinear residual bounds by centered
  residual or Taylor-model enclosures and link them to one global profile;
* the Schur derivative trace needs either a certified auxiliary homogeneous BVP
  or a Green-identity trace bound;
* the nonlinear Newton radius and Lipschitz bound have not yet been computed.

All three are local/global residual inequalities with generous floating
margins. None requires propagation of the full shooting bracket to the wall.

Run the exploratory probe with

```bash
PYTHONPATH=. python3 experiments/skyrmion_global_bvp_probe.py
```
