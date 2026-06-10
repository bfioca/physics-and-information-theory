# Validated Skyrmion Interval Program

Status: prescribed-profile AU.1 existence, local uniqueness, wall slope,
monotonicity, and inertia are certified; AU.2 exact global derivative norms and
the continuum tail envelope are certified. AU.3a gives conservative directed
global moments; authenticated profile-resolved AU.3b is complete as a baseline
but remains too tail dominated to improve them.

## Why Floating Numerics Were Not A Proof

The original hard-wall profile used floating RK4 shooting. Wrapping its outputs
with `nextafter` would not validate the result: Python does not specify directed
rounding for `sin`, `cos`, `sqrt`, or `atanh`, and an unchecked origin series
has no proved remainder enclosure. AU therefore uses a small trusted checker
rather than treating a converged plot as a theorem.

## Completed Foundation

`qgtoy.validated_interval` provides closed intervals with exact rational
endpoints and no floating transcendental calls. It implements:

```text
outward exact +, -, *, /, integer powers,
pi = 16 atan(1/5)-4 atan(1/239),
rational Taylor enclosures for sin and cos,
positive-series enclosure for atanh(x), |x|<1,
exact-rational bisection enclosure for sqrt(x).
```

Every remainder is a rational analytic bound. Correct containment follows from
the stated alternating-series, Taylor/Lagrange, geometric-tail, and bisection
arguments. The executable checks nested refinement for `pi` and `atanh(1/5)`,
the interval Pythagorean identity, and the ordered nonnegative square-root
bracket. These are consistency checks, not an independent machine proof of the
analytic remainder theorems. They validate no Skyrmion profile claim.

## Conditional Positive-Radius Checkers

`qgtoy.validated_skyrmion_profile` evaluates the exact curved-profile vector
field on rational boxes away from the removable origin singularity. For each
exact initial point in the declared initial box, strict interval containment of
the Picard image in a closed tube gives a fixed point; positivity of the radius,
lapse, and profile denominator makes the vector field analytic there, hence the
solution is unique. The checker then encloses the cell endpoint.

The packaged witness covers only the rational cell
`[1001/10000,1001/10000+1/1000000]`. Its initial box was selected near a
floating profile and is not yet proved to contain the regular origin branch.
It is therefore AU.0b checker infrastructure, not AU.1 evidence.

The same trusted module now validates normalized rational-polynomial Taylor
cells. For `x=a+hs`, it takes `F=P(s)`, `G=P_s/h`, recomputes the acceleration
defect and both state-Jacobian bounds, and verifies componentwise self-map plus
weighted contraction inequalities. A two-microcell conditional track is the
AU.0d executable witness. It proves the chaining logic, not macroscopic
continuation or a wall residual. Endpoint boxes use the checker-computed
self-map image bounds, not the looser candidate tube radii.

## Uniform Origin Family

The removable singularity is resolved with

```text
t=x^2,  pi-F=x u(t),  p(t)=d(pi-F)/dx.
```

An exact nonsingular Volterra map is checked in the parameter-dependent
weighted cubic ball
`|p-(b-3c(b)t)|<=R t^2`. Rational Taylor models and entire-series remainder
bounds prove one uniform self-map and contraction for every real slope in
`[1.579953,1.579954]`, with `x0=1/16` and `R=13/10`. Formal rational-function
arithmetic verifies the exact constant and cubic coefficient identities before
the `t^2` remainder is bounded. Consequently every declared fiber contains one
regular origin solution, depends continuously on slope, and contributes to a
direct full-interval cutoff box with

```text
|F-(pi-bx+c(b)x^3)| <= R x^5/5,
|F'-(-b+3c(b)x^2)| <= R x^4.
```

This is AU.0c. Its common cutoff box is evaluated directly over the full slope
interval; it is not an endpoint hull. It does not propagate the family past
`x=1/16` or prove a hard-wall root.

For the selected point slope, a separate quintic-centered contraction improves
the cutoff errors to `O(x^7)` and `O(x^6)`. A trusted nesting check proves that
this point ball lies inside the cubic sensitivity fiber with identical slope,
cutoff, mass, and curvature. The global candidate and nonlinear endpoint audits
use the sharper point seed; the cubic family remains the source of first and
second slope sensitivities.

Exact interval automatic differentiation of the same parameterized contraction
also proves `C1` dependence on slope. The checker bounds the partial derivative
of the translated Volterra map and applies `(1-q)^-1`, giving

```text
Phi_b=dF_b(1/16)/db in [-0.06244243,-0.06243179],
Gamma_b=dF'_b(1/16)/db in [-0.99740679,-0.99655545].
Phi_bb=d2F_b(1/16)/db2 in [-0.00013757,0.00029385],
Gamma_bb=d2F'_b(1/16)/db2 in [-0.01350569,0.02100685].
```

These displayed decimals summarize exact rational intervals. First- and
second-order interval automatic differentiation is applied to the common
parameterized contraction; no finite difference of endpoint boxes is used.

## AU.1 Certificate Architecture

At the exact parameter point

```text
mu=1, lambda=1/400, x_w=4,
```

the next checker will consume an exact-rational candidate bundle and verify all
claims itself:

1. The completed AU.0c theorem supplies a continuous slope-to-cutoff map and
   exact cutoff data and parameter dependence for the full bracket.
2. A rational globally `C2` piecewise-polynomial pair `(b_bar,F_bar)` supplies
   the augmented boundary-value residual, including the origin-map and wall
   conditions.
3. The checker independently evaluates the self-adjoint Jacobi coefficients,
   proves `P>0`, and verifies the fixed rational Barta quotient lower bound `1`.
4. A rational auxiliary homogeneous function and exact origin-map derivative
   intervals enclose the scalar Schur complement away from zero.
5. Recomputed second-derivative bounds close a Newton-Kantorovich or radii-
   polynomial inequality in a norm controlling `C1`.
6. The resulting solution ball has `F'<0`, excludes zero wall slope, and gives
   a positive directed-quadrature inertia lower bound.
7. Exact interval evaluation then encloses `Y=atanh(1/5)` and `W''(Y)`.

## Route Decision After Propagation Audit

The untrusted generator `qgtoy.skyrmion_taylor_certificate_generator` builds
rational cubic-Hermite cells from floating RK4 centers, rounds every candidate
radius outward, and submits every cell and final chain to the trusted AU.0d
checker. Both endpoint slopes validate through `x=1/4` with step `1/2048`, but
the derivative radii have already grown to about `0.8514`. Extending the lower
endpoint toward `1/2` stops exactly at `x=603/2048`: the last accepted
derivative radius is about `16.788`, and the next minimum-step self-map does not
close. Finer cells delay but do not remove this wrapping.

This is not a no-go theorem for Taylor models. It rejects the current
constant-correction-radius, decorrelated state-box representation as the main
wall certificate. AU.1 therefore selects the global residual route described
in `experiments/skyrmion_global_bvp_design.md`.

For the floating profile, the self-adjoint Dirichlet Jacobi operator has
sampled first eigenvalue `7.16556` and scalar augmented Schur complement
`2.95967`. More importantly, the fixed rational positive function

```text
v(x)=8/[(x-33/16)^2+4]
```

has sampled Barta quotient at least `1.62749`. The trusted target is the weaker
exact inequality `(A v)/v>=1`, which would give an `L2` inverse norm at most
one. These numbers are exploratory margins, not certified profile facts.

The untrusted global generator now emits exact-rational degree-five Hermite
splines on `[1/16,4]`, with globally matching values, first derivatives, and
second derivatives. It also emits Bernstein jet boxes, exact interval
nonlinear residual boxes, origin and wall residual data, and an optional
finite-difference homogeneous Jacobi spline. On the default `1/16` mesh the
wall residual is about `9.89e-7`. Direct whole-cell evaluation gives nonlinear
residual upper bound about `15.74`; four exact centered subcells per spline
cell reduce it to about `2.407`. On the coarser test mesh the same construction
reduces the nonlinear and homogeneous residual bounds by factors above `12`
and `14`, respectively. These are rigorous enclosures of the proposed rational
functions but remain untrusted candidate data. Sixteen subcells reduce the
default nonlinear number further to about `0.526`, confirming convergence but
still missing the intended Newton-defect scale by orders of magnitude. The
trusted checker therefore needs polynomial-level residual cancellation rather
than subdivision alone.

The trusted AU.0f Barta checker independently recomputes `P,P',Q` and the
fixed-witness quotient from exact profile jet boxes. Its packaged five-cell
conditional audit proves a downward-rounded exact lower bound
`(Lv)/v >= 1.464502640726474651`, hence the declared target `1`, on every
supplied box. The boxes are not yet linked to a common global profile, so this
does not prove coercivity of the physical BVP. It validates the coefficient
and comparison-function machinery that the eventual global certificate will
reuse.

The checker now also consumes exact rational polynomial splines directly. It
verifies exact coverage and global `C2` joins, recomputes centered jets, and
adaptively bisects only unresolved quotient boxes. The complete representative
21-cell spline closes with 207 accepted leaves, maximum extra depth five, and
an exact-rational certified quotient lower bound greater than `1.502908`, hence
greater than `3/2`. This establishes global
coercivity for that exact approximate spline, replacing the earlier five-box
local evidence. Transfer to the unknown BVP solution still requires a linked
Newton ball whose coefficient perturbation preserves the margin.

The selected global certificate must now verify:

1. a rational globally `C2` approximate profile and its nonlinear residual;
2. the completed exact origin-map derivative intervals
   `Phi_b,Gamma_b,Phi_bb,Gamma_bb`;
3. preservation of the already validated rational Barta inequality throughout
   the eventual nonlinear solution ball;
4. an auxiliary homogeneous residual and scalar Schur interval excluding zero;
5. a nonlinear derivative Lipschitz bound and a closed Newton radius;
6. monotonicity, wall slope, and inertia inside the resulting `C1` ball.

The functional-analytic implementation is fixed in
`experiments/skyrmion_augmented_bvp_newton_bounds.md`. It uses the Dirichlet
Jacobi graph norm `||h||_A=||Ah||_infinity`, an exact scalar Schur
factorization, a Green-identity derivative trace, an explicit analytic formula
for `D2 G`, and a Newton radii polynomial. The rational generator spline is
not assumed to equal the unknown exact origin value: a symbolic interval
boundary lift consumes the origin and wall residuals before the nonlinear
residual is recomputed. With `Phi_bb,Gamma_bb` now certified, the remaining
analytic-norm requirement is a sharper Green-kernel `C1` estimate than the
elementary global graph-norm constant.

The existing finite-difference homogeneous spline has been diagnosed as the
regular shooting-sensitivity proposal `Y_hat`, not the wall-Dirichlet auxiliary
solution. Its wall value is about `-6.52421`, so using it directly would
manufacture a false near-zero Schur diagnostic. The correct candidate adds the
fundamental proposal `K_hat(a)=0,K_hat'(a)=1` and forms the exact rational
polynomial combination
`H_hat=Y_hat-[Y_hat(c)/K_hat(c)]K_hat`. The raw candidate Schur interval is
`[2.95926150,2.96011432]`, with `K(c)` approximately `2.20434843` and
combination coefficient approximately `2.95969864`; the remaining proof
obligation is to subtract the trusted derivative-trace image of the corrected
homogeneous residual.

The trusted Schur audit is now implemented for the Jacobi operator of an exact
approximate profile spline. It ignores generator residual fields, checks the
profile/auxiliary meshes and `C2` joins itself, applies the symbolic affine left
lift, recomputes the full residual on exact subcells, derives the conservative
`C1` trace correction from the same Barta cells, and rejects unless the
corrected Schur interval remains positive. This is deliberately a conditional
operator audit, not a nonlinear BVP theorem or a transfer to the endpoint-lifted
profile used by the final Newton map.

On the current 21-cell candidate, separately recomputed independent-box
residual enclosures for `H_hat` are approximately `28.15046`, `14.52383`, and
`9.42746`, with only a further reduction to `7.40831` at 64 centered subcells
per source cell. Combining the
validated `alpha>1.5029` margin with sampled coefficient scales gives a
diagnostic elementary derivative bound around `674.5`, which would require
residual below about `4.39e-3` merely to keep the Schur interval away from zero.
The selected closing order was therefore:

1. expand the complete Jacobi residual as one centered polynomial/Taylor model
   so cancellations occur before interval ranging;
2. build an independent normalized Dirichlet representer `kappa_hat`, validate
   its residual, and bound its `L1` norm to certify the sharper trace constant;
3. rerun the lifted Schur audit with that independently established constant;
4. only then transfer the result to the endpoint-corrected nonlinear profile
   and close the Newton radius.

The cancellation-preserving residual evaluator is now implemented. Multiplying
by `x^2` and using trigonometric identities rewrites the complete Jacobi
residual as five exact rational polynomial amplitudes multiplying
`1,cos(F),sin(2F),cos(2F),cos(4F)`. The checker constructs centered composition
Taylor models with exact rational point enclosures and Lagrange tails, sums the
entire residual polynomial first, and ranges only afterward. Exact vacuum and
dense independent-formula tests validate the identity and containment.

This sharper evaluator separates wrapping from interpolation error. On the
current `3/16` first cell, dense direct evaluation gives a true maximum near
`6.92765`, so no interval representation can reduce that candidate below the
Schur target. The candidate generator now accepts explicit exact rational mesh
nodes and shares them across the profile, shooting sensitivity, fundamental
solution, and wall-zero auxiliary. A graded feasibility mesh uses `1/128` on
`[1/16,1/8]`, `1/64` on `[1/8,1/4]`, `1/32` on `[1/4,1/2]`, and the historical
coarse scale outward. Floating assembled evaluation then gives a maximum about
`5.79e-4`. That number selects the candidate; it is not a certified residual
until the new trusted evaluator closes on every graded cell.

An independent derivative-trace checker now implements the Green-identity
route without circularly using the Schur bound. It accepts a normalized exact
rational Dirichlet representer candidate, verifies its endpoints and shared
`C2` mesh, reruns Barta, recomputes its five-harmonic residual, integrates its
absolute value exactly on sign-certified cells, and corrects the `L1` norm with
the Barta-derived `C0` estimate. Dividing by the independently recomputed
positive `P(a)` gives a trusted declared upper-bound test for `C_tau`.

The 43-cell exact graded representer now passes that audit. The same-operator
Barta lower bound is greater than `1.0235900944571767` on 139 accepted leaves
at maximum refinement depth four. All 43 cells are sign-certified for exact
`L1` integration, and the recomputed bounds are

```text
||kappa_hat||_1 <= 0.1055378219793721,
||A kappa_hat||_infinity <= 0.08913332184493121,
representer L1 correction <= 0.7019249095288332,
C_tau <= 9.895351050897547.
```

The largest residual occurs on `[1/16,9/128]`. The new trace-sharpened Schur
checker composes the audits in proof order: it certifies `C_tau` without Schur
input, recomputes the lifted auxiliary residual, and only then forms the
corrected Schur interval. Its synthetic pass and rejection tests are complete;
the physical graded run recomputes raw Schur
`[2.9592592352087594,2.9601147691072494]`, lifted residual at most
`0.005843528112861022`, and derivative correction at most
`0.05782376205254868`. Thus the exact approximate-profile operator has
corrected Schur interval
`[2.9014354731562104,3.017938531159798]`. These bounds feed the closed
endpoint-corrected nonlinear tube below.

The endpoint-corrected nonlinear residual checker is also executable. It uses
the exact five-harmonic identity for `x^2 G(F)`, centers the origin-value lift at
zero whenever the rigorous correction interval contains zero, and bounds the
remaining affine family by integrating the Jacobi derivative. The physical
graded candidate gives

```text
||G(F_bar)||_infinity <= 0.002295967024672295,
F_bar'(a)-Gamma(b_bar)
  in [-0.000023462001836132805,0.00001633679528688307].
```

The maximum is on `[2,2.1875]`. The completed augmented audit uses row-local
Green bounds, the center Jacobi equation to eliminate the global `C0*C2` loss,
and a cell-weighted trace. At `omega=3/4`, `r=1/250`, it proves conservatively

```text
Z0<=0.000078, Z2<=78.733,
p(r)<-0.00107, q(r)<0.31501.
```

The approximate block inverse is injective because the Dirichlet center
operator is invertible and the scalar Schur interval excludes zero. The
contraction therefore supplies local uniqueness in the certified augmented
ball. Post-checks prove strict monotonicity, negative wall slope, and positive
finite inertia.

## AU.2 And AU.3

AU.2 now combines exact 43-cell positive-radius jet sums with a regular-origin
Volterra-Lie and fourth-order interval-AD bound. It certifies

```text
M^W <= (2.5776861728e8,6.9465700567e6,2.9826900811e5),
M^A <= (3.7317164259e10,5.0564413001e8,1.3919447366e7).
```

The exact archive SHA256 is
`1d5fe53786cc280006d7b1092d360556d4d8d8684e5ae3356ce8cd6d084e72a9`.
AU.3a combines a directed rational finite-band sum with the analytic tail to
produce conservative global `H2` and time-moment bounds. AU.3b now replaces the
profile-uniform finite band with authenticated profile-resolved evaluation, but
its `P=64` joined tail dominates and makes the resulting `Q` bounds weaker.
Its normalized ULE upper caps are rigorous conditional consequences, not
physical windows; sharper tail/product bounds remain the numerical gate.

The held-off-center BVP comes later. Its anchor action and boundary traction law
must be specified before numerical coefficients are meaningful.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy validated-interval-foundation
PYTHONPATH=. python3 -m qgtoy validated-skyrmion-origin
PYTHONPATH=. python3 -m qgtoy validated-skyrmion-profile-foundation
PYTHONPATH=. python3 -m qgtoy validated-skyrmion-barta-foundation
PYTHONPATH=. python3 experiments/skyrmion_newton_linearization_audit.py \
  --omega 3/4 --tube-radius 1/250 --tube-trigonometric-terms 12 \
  --tube-rounding-denominator 1000000000000000000
```
