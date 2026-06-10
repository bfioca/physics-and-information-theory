# Validated Skyrmion Global Sobolev Certificate

Status: exact-rational directed global upper bounds for
`Q0,Q1,Q2,G,M1`; sharper profile-resolving finite-frequency quadrature and the
finite-coupling reduced-dynamics theorem remain open

## Probability-Measure Rewrite

Let `rho_I(x)>=0` be the exact inertia density of the AU.1-certified profile,
`I=int rho_I dx`, `tanh(y)=sqrt(lambda)x`, and

```text
K(p,y)=y coth(y) sinc(py)-cos(py).
```

The current form factor can be written without a profile-dependent prefactor:

```text
dmu=rho_I(x)dx/I,
H(p)=3/(1+p^2) int K(p,y)/tanh(y)^2 dmu.              (1)
```

Thus `mu` is a positive probability measure fixed by the same certified
profile. This identity is the key finite-band simplification: a uniform bound
on the kernel is automatically uniform over the entire Newton tube.

Put

```text
Y=atanh(sqrt(lambda)x_w),
C_Y=1/(1-lambda x_w^2),
D_Y=4/3+Y^2/3.
```

The elementary inequalities

```text
y coth(y)-1 <= y^2,
|sinc'(z)| <= |z|/3,
|sinc''(z)| <= 1/3,
y^2/tanh(y)^2 <= cosh(Y)^2=C_Y
```

give, for `B_k=int partial_p^k K/tanh(y)^2 dmu`,

```text
|B_0(p)| <= C_Y(1+2p^2/3),
|B_1(p)| <= C_Y D_Y p,
|B_2(p)| <= C_Y D_Y.                                 (2)
```

The slack in the first line is intentional. Differentiating
`H=3B_0/(1+p^2)` then gives pointwise bounds for `H,H',H''` using only rational
operations and the AU.2 interval for `Y`.

## Directed Finite Band

On each rational cell `[a,b]`, the implementation evaluates the increasing
numerator factors at `b` and the denominator factors at `a`. It also uses the
proved bare-root bounds

```text
0<=p<=1:  (r,r',r'') <= (2/9,13/18,25/2),
p>=1:     r <= p^(3/2)/6,
          |r'| <= (81/480)p^(1/2),
          |r''| <= (21/48)p^(-1/2).                  (3)
```

Every square root in (3) is rounded upward to an exact decimal rational. The
product rule bounds the positive-frequency signed factor. Half-KMS balance
gives the negative-frequency bounds

```text
q_- <= q_+,
|q_-'| <= pi q_+ + |q_+'|,
|q_-''| <= pi^2 q_+ +2pi|q_+'|+|q_+''|,              (4)
```

with `pi<=22/7`. Multiplying each uniform cell bound by its exact width gives
a directed upper sum for the finite-band squared norms. This is not Simpson
quadrature and uses no convergence heuristic.

For the default certificate, the finite band is `0<=p<=128` with step `1/4`.
The AU.2 tail formula is recomputed at exactly `P=128`; the archived `P=1`
tail is not rescaled. Dimensionless and physical squared norms are related by

```text
Q_k(R)^2=R^(2k-4) Q_k(1)^2.                           (5)
```

Joining the directed finite sum to the exact tail gives

```text
Q0 <= 4296.7909080828495,
Q1 <= 10146.945245040379,
Q2 <= 35213.76234103636,
G  <= 16554.53883053991,
M1 <= 47391.58033605288.                              (6)
```

Here

```text
G <= sqrt(2pi Q0 Q1),
M1 <= sqrt(2pi Q1 Q2).                                (7)
```

All proof endpoints in the artifact are exact fractions. The decimals in (6)
are upward-rendered summaries.

## Interpretation

Equation (6) closes AU.3a: the matter-derived signed factor now has certified
global constants that can be inserted into the ancilla-stable ULE residual
polynomial. It does not validate the earlier floating coupling caps, because
those use much smaller profile-resolving candidates

```text
(Q0,Q1,Q2)_num=(62.2644668852,2.16015691289,0.168156611337).
```

The gap measures proof conditioning, not physical decoherence. The finite-band
bound deliberately discards oscillatory cancellation and most radial profile
information. AU.3b is therefore a sharp interval evaluation of the certified
profile on the finite band. Only after that refinement should the project use
the constants to decide whether the physical window is open or closed.

This certificate also does not establish Gaussianity, exact finite-coupling
reduced dynamics, an action-derived switch, collective-band projection,
isospin access, wall stress, lifetime, or gravitational backreaction.

## Artifact

```text
experiments/skyrmion_au3_global_sobolev_exact_certificate.json
SHA256 b6a9931cc50359ec4a9bed7a6d3443471f39b39f60c37e3a92d39073ba0cc55c
```

The artifact pins the AU.2 input SHA256, recomputes the endpoint and tail
formulas before using them, records exact finite-band and tail contributions,
and hashes every source file in the AU.3 trusted path.

Representative command:

```bash
PYTHONPATH=. python3 experiments/skyrmion_au3_global_sobolev_audit.py
```
