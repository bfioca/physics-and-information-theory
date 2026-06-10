# Augmented Skyrmion BVP: Newton--Kantorovich bounds

Status: functional-analytic design for AU.1.  The inequalities in Sections
2--8 are rigorous under their stated hypotheses. Section 9 separates trusted
interval outputs from the remaining floating diagnostics.

The interval is

```text
I=[a,c]=[1/16,4],       L=c-a=63/16.
```

At `mu=1`, `lambda=1/400`, write

```text
N=1-x^2/400,
p(x,F)=N(x)[x^2+8 sin(F)^2],
W(x,F)=sin(F)^2+2 sin(F)^4/x^2+x^2[1-cos(F)],
G(F)=-(p(x,F)F')'+p_F(x,F)F'^2/2+W_F(x,F).
```

The selected augmented problem is

```text
G(F)=0,
F(a)=Phi(b),       F(c)=0,       F'(a)=Gamma(b),       (1)
```

where the exact origin theorem supplies `Phi`, `Gamma`, and their first two
slope derivatives on the current bracket.  This formulation uses all of the
available regular-origin data without propagating an interval shooting family
to the wall.

## 1. Dirichlet Jacobi operator

Let `F_hat` be the generator's rational spline and put

```text
chi_a(x)=(c-x)/L,       chi_c(x)=(x-a)/L,
u_bar=F_hat-chi_a F_hat(a)-chi_c F_hat(c),
F_bar=u_bar+chi_a Phi(b_bar).                            (1a)
```

The spline `u_bar` is rational and Dirichlet.  The chart center `F_bar` is not
generally rational, but it satisfies `F_bar(a)=Phi(b_bar)` and `F_bar(c)=0`
exactly and is rigorously interval-evaluable because AU.0c encloses the single
lifted constant.  Relative to the generator output, the correction is

```text
F_bar-F_hat
 =chi_a[Phi(b_bar)-F_hat(a)]-chi_c F_hat(c).             (1b)
```

Thus the generator's origin-box and wall residuals are not assumed away.  The
trusted checker must apply (1b), then recompute `G(F_bar)` and
`F_bar'(a)-Gamma(b_bar)` on every cell.  A formulation retaining `F_hat`
unchanged is also possible, but it needs two additional value-boundary rows
and their explicit linear lifts in the block inverse; (1a) is the smaller
equivalent system.

The self-adjoint linearization is

```text
A h=-(P h')'+Q h,                    (2)
P=p(x,F_bar),
Q=W_FF+p_FF F_bar'^2/2-(p_F F_bar')'.
```

Assume the interval checker proves

```text
P>=p0>0,
(A v_*)/v_* >= alpha>0,
v_*(x)=8/[(x-33/16)^2+4].            (3)
```

The intended certificate uses `alpha=1`.  On `I`, `1<=v_*<=2`.  The
ground-state identity gives, for every Dirichlet `h`,

```text
<h,A h>
 = integral P v_*^2 [(h/v_*)']^2
   + integral [(A v_*)/v_*] h^2
 >= alpha ||h||_2^2.                 (4)
```

It also gives the weak maximum principle: if `A y>=0` and the endpoint values
of `y` are nonnegative, then `y>=0`.  Indeed, applying (4) to the negative part
of `y` rules out a negative interior component.

## 2. A Banach graph norm that controls C1

Let

```text
X_D={h in W^{2,infinity}(I): h(a)=h(c)=0},
||h||_A=||A h||_infinity.             (5)
```

Suppose certified coefficient bounds give

```text
q1 >= integral_I |Q| dx,
p1 >= ||P'||_infinity,
qinf >= ||Q||_infinity.
```

For `A h=f`, comparison with
`(||f||_infinity/(alpha min v_*))v_*` gives

```text
||h||_infinity <= C0 ||f||_infinity,
C0=(max v_*)/(alpha min v_*)=2/alpha. (6)
```

Since a Dirichlet `h` has some `xi` with `h'(xi)=0`, integration of
`(P h')'=Qh-f` from `xi` gives

```text
||h'||_infinity <= C1 ||f||_infinity,
C1=(L+q1 C0)/p0.                      (7)
```

Finally, expanding (2) yields

```text
||h''||_infinity <= C2 ||f||_infinity,
C2=(1+p1 C1+qinf C0)/p0.              (8)
```

Thus (5) is a Banach norm equivalent to the usual `W^{2,infinity}` norm on
`X_D`, and in particular

```text
||h||_{C1} <= max(C0,C1)||h||_A.      (9)
```

This is the required logical bridge to monotonicity.  A bare `H_0^1` energy
ball does not control `F'` pointwise and is not sufficient for that claim.

## 3. Derivative trace

Define

```text
tau(f)=(A_D^{-1}f)'(a).
```

Let `kappa` solve

```text
A kappa=0,       kappa(a)=1,       kappa(c)=0.
```

Green's identity, with the integral oriented from `a` to `c`, gives the exact
positive-sign representation

```text
tau(f)=[1/P(a)] integral_I kappa(x) f(x) dx,            (10)
```

and hence

```text
|tau(f)| <= Ctau ||f||_infinity,
Ctau=||kappa||_1/P(a).                                 (11)
```

This is normally much sharper than using (7) at the endpoint.  If the
certified Schur auxiliary `H` below is available and `Phi_b` excludes zero,
then `kappa=H/Phi_b`, so a directed quadrature bound on `||H||_1` gives

```text
Ctau <= ||H||_1/[P(a)|Phi_b|].                          (12)
```

For an approximate `H_hat` with exact endpoint data imposed through the same
symbolic origin lift and residual `rho_H=A H_hat`, the exact solution satisfies

```text
||H-H_hat||_{C^j} <= Cj ||rho_H||_infinity,  j=0,1,2,   (13)
```

where `Cj` means `C0,C1,C2`.  In particular, the derivative error is bounded
by `C1 ||rho_H||_infinity`.  It may be replaced by the sharper
`Ctau ||rho_H||_infinity` only if `Ctau` has already been certified from an
independent trace representer.  This ordering avoids using `H` to certify
itself.

## 4. Exact augmented block factorization

Put `chi=chi_a` and abbreviate

```text
Phi_1=Phi'(b_bar),       Gamma_1=Gamma'(b_bar).
```

Let the certified auxiliary Schur solution satisfy

```text
A H=0,       H(a)=Phi_1,       H(c)=0,
S=H'(a)-Gamma_1,       |S|>=s0>0.                       (14)
```

Use local coordinates `(w,beta)` in which the exact physical field is

```text
F=F_bar+w+beta H
  +chi[Phi(b_bar+beta)-Phi(b_bar)-Phi_1 beta].          (15)
```

Here `w` is Dirichlet.  Equation (15) enforces both value boundary conditions
in (1) exactly for every `beta`.  At the origin of these coordinates the
linearized map sends `(w,beta)` to

```text
(A w, tau(Aw)+S beta).
```

Therefore, for an interior residual `r` and derivative-boundary residual `s`,
the exact inverse is

```text
w=A_D^{-1}r,
beta=[s-tau(r)]/S.                                      (16)
```

There is no hidden field-sized matrix inverse: the only extra obstruction
beyond Dirichlet coercivity is the scalar interval `S`.

For weights `omega,nu>0`, set

```text
||(w,beta)||_X=max(||Aw||_infinity,omega|beta|),
||(r,s)||_Y=max(||r||_infinity,nu|s|).
```

Equations (11) and (16) give the explicit inverse bound

```text
||D N(F_bar,b_bar)^{-1}||_{Y->X} <= K,
K=max{1, [omega/s0](Ctau+1/nu)}.                        (17)
```

One may choose `omega=s0/(Ctau+1/nu)` to make this upper bound one, but the
same choice must be retained in all physical and nonlinear estimates below.

If only `H_hat` is supplied, (13) gives the directly checkable Schur enclosure

```text
|S| >= |H_hat'(a)-Gamma_1|-Ctr||rho_H||_infinity,       (18)
```

with `Ctr=C1` from (7), or `Ctr=Ctau` only after an independent verification
of (10)--(11), and with interval widths in `Gamma_1` included on the right.
The checker must reject the certificate unless the resulting lower bound is
positive.

For candidate generation, let `Y_hat` approximate the regular shooting
sensitivity and let `K_hat` approximate

```text
A K=0,       K(a)=0,       K'(a)=1.
```

Then the exact rational combination

```text
s_hat=-Y_hat(c)/K_hat(c),
H_hat=Y_hat+s_hat K_hat
```

has `H_hat(c)=0` exactly. The current floating proposal gives
`s_hat approximately 2.95969864` and a raw interval
`H_hat'(a)-Gamma_1 in [2.95926150,2.96011432]`. These values demonstrate a
large raw pre-correction margin, but (18) remains the theorem: the checker
must subtract the independently certified derivative-trace image of the
homogeneous residual.

The trusted conditional audit now implements this conservative `Ctr=C1` route
for the exact approximate-spline operator. It rejects the current candidate:
independent-box `H_hat` residual enclosures are approximately `28.15046`,
`14.52383`, `9.42746`, and `7.40831` at 4, 8, 16, and 64 centered subcells per
source cell.
Using `alpha>1.5029` and the sampled principal lower scale gives
`C1 approximately 674.5`, so retaining any positive part of the raw Schur
margin would require `||rho_H||_infinity` below approximately `4.39e-3`.
The next checker must preserve polynomial-level cancellation in `rho_H` and
certify a normalized Dirichlet trace representer independently; further raw
subdivision is not the selected route.

The selected replacement is now implemented at the residual-algebra level:
after multiplication by `x^2`, the checker combines five polynomial amplitudes
against `1,cos(F),sin(2F),cos(2F),cos(4F)` before ranging. This proves that the
old first-cell difficulty was not only wrapping: dense direct evaluation of the
coarse auxiliary reaches about `6.92765`. The generator now supports one exact
graded mesh shared by `F_hat,Y_hat,K_hat,H_hat`; widths `1/128`, `1/64`, and
`1/32` on successive near-origin bands reduce the sampled assembled residual to
about `5.79e-4`. The value is still a floating candidate diagnostic. Equations
(10)--(18) become a theorem only after the trusted graded Barta/residual audit
and an independent normalized trace-representer certificate close.

## 5. Explicit nonlinear second derivative

For partial derivatives of `p(x,F)` at fixed `x`, direct differentiation of
the expanded residual gives

```text
D^2G(F)[h,k]
 =-p_F(k h''+h k''+h' k')
  -p_FF(h k F''+h F' k'+k F' h')
  -p_xF(k h'+h k')
  -p_xFF h k F'
  -(p_FFF/2) h k F'^2
  +W_FFF h k.                                           (19)
```

This symmetric formula is useful for a trusted interval implementation: it
contains no numerical differentiation and no cancellation between separately
bounded divergence terms.

On a candidate radius `r`, let `phi2` and `gamma2` bound `|Phi''|` and
`|Gamma''|` for `|beta|<=r/omega`.  These are new certificate inputs that
require a twice-differentiated origin contraction.  Let
`Hj=||H^{(j)}||_infinity`, and define

```text
E0=C0+H0/omega+phi2 r/omega^2,
E1=C1+H1/omega+phi2 r/(L omega^2),
E2=C2+H2/omega.                                         (20)
```

These bound the `C^j` size of every unit first field variation generated by
the coordinates (15).  Over the corresponding physical profile tube, let

```text
B1>=||F'||_infinity,       B2>=||F''||_infinity,
pF,pFF,pFFF,pxF,pxFF,wFFF
```

bound the absolute values of the indicated coefficient derivatives.  Then
(19) gives

```text
MG = pF(2 E0 E2+E1^2)
   + pFF(E0^2 B2+2 E0 E1 B1)
   + 2 pxF E0 E1
   + pxFF E0^2 B1
   + (pFFF/2) E0^2 B1^2
   + wFFF E0^2.                                         (21)
```

The nonlinear origin lift has a second field derivative
`chi Phi'' beta delta`.  If

```text
Jchi >= sup ||DG(F) chi||_infinity
```

on the tube, the complete second derivative bound in the weighted norms is

```text
Mint = MG+Jchi phi2/omega^2,
Msc  = (gamma2+phi2/L)/omega^2,
M(r) = max(Mint,nu Msc).                                (22)
```

All quantities in (20)--(22) are cellwise interval suprema.  Using one crude
global bound for `W_FFF`, especially near `a`, unnecessarily loses the regular
origin cancellations.

### 5.1 Center-equation Hessian reduction

The direct estimate (21) is valid but pays for `E2` independently in every
cell. This is avoidable because each first variation is generated by the fixed
center Jacobi inverse. Write

```text
A0 h=-(P0 h')'+Q0 h=g_h,
m=p_FF F'+p_xF,
z=W_FFF-p_FF F''-p_xFF F'-(p_FFF/2)F'^2.
```

Then

```text
h''=(Q0 h-P0' h'-g_h)/P0,
```

and exact substitution into (19) gives

```text
D^2G(F)[h,k]
 =(p_F/P0)(k g_h+h g_k)-p_F h'k'
 +(p_F P0'/P0-m)(h k'+k h')
 +(z-2 p_F Q0/P0)h k.                                (22a)
```

The factor two in the last coefficient comes from substituting both `h''` and
`k''`. For the nonlinear origin chart, a unit tangent has

```text
|g_h| <= 1+[phi2 r/omega^2] |A0 chi|,
A0 chi=P0'/L+Q0 chi.                                  (22b)
```

Thus each source cell has the alternative exact bound

```text
Mred =2|p_F/P0| E0 G0+|p_F|E1^2
      +2|p_F P0'/P0-m|E0E1
      +|z-2p_F Q0/P0|E0^2.                            (22c)
```

The checker uses the smaller of (21) and (22c), then adds the separate chart
second derivative `|A_F chi| phi2/omega^2`. No weak derivative norm or hidden
integration by parts is introduced; (22a) is an identity in the existing
`||A0 w||_infinity` graph coordinates.

The Green certificate is also retained cellwise. If `Cj,I` is the row bound of
the exact inverse on source cell `I`, and `Hj,I` is the locally corrected Schur
auxiliary bound, then (20) is evaluated with `Cj,I,Hj,I` rather than their
global maxima. This prevents a near-origin derivative maximum from being
charged in cells where `|sin(2F)|` is large.

Finally, the scalar Schur component no longer uses
`Ctau max_I b_I`. Let `kappa_hat` be the certified trace representer,
`K_I=int_I |kappa_hat|`, and

```text
epsilon_kappa=C0 ||A0 kappa_hat||_infinity.
```

For nonnegative cell bounds `b_I`, the exact representer correction proves

```text
T(b)=[sum_I (K_I+epsilon_kappa |I|) b_I]/P0(a).        (22d)
```

The sharper compositions are therefore

```text
Y=max{R_infinity,[omega/S](|sigma|+T(R))},
Z0=max{D_infinity,[omega/S]T(D)},
Z2=max{M_infinity,[omega/S](Msc+T(M))}.                (22e)
```

The same Green `C0` used elsewhere certifies `epsilon_kappa`; the older Barta
`C0` remains a valid fallback. Equations (22a)--(22e) preserve every source-cell
bound until the final scalar maximum and remove both dominant global-max losses
from the first tube audit.

## 6. Residual and radii polynomial

At the center, compute

```text
R=G(F_bar),
sigma=F_bar'(a)-Gamma(b_bar).
```

The exact block formula, composed with the cell-weighted trace (22d), gives
the Newton-defect bound

```text
Y=max{||R||_infinity,
      [omega/s0](|sigma|+T(R))}.                         (23)
```

The older replacement `T(R)<=Ctau||R||_infinity` remains valid but is used only
as a historical coarse diagnostic below.

For a candidate `r`, evaluate `M(r)` on the full radius-`r` tube.  An exact
derivative inverse closes the Newton map if

```text
p(r)=Y-r+[K M(r)/2]r^2 < 0,
K M(r) r < 1.                                           (24)
```

The first inequality is the self-map condition and the second is contraction.
If a numerical approximate inverse is used instead, add its certified defect
`Z0`:

```text
p(r)=Y+(Z0-1)r+[K M(r)/2]r^2 < 0,
Z0+K M(r)r<1.                                           (25)
```

For constant `M`, a sufficient quick test is `2 K M Y<=1`; the smaller root is

```text
r_minus=2Y/[1+sqrt(1-2 K M Y)].                         (26)
```

## 7. Monotonicity and wall slope

This consequence is implemented by
`validate_skyrmion_newton_physical_observables`.  The checker accepts only a
Newton tube whose self-map and contraction inequalities both close, and an
exactly matching uniform origin family on the tube's shooting-slope interval.
The Newton result carries the mass, curvature, cutoff, wall, slope interval,
and origin-ball radius needed to reject cross-certificate substitutions.

Every point in the radius-`r` ball obeys, directly from (15),

```text
Delta0(r)=C0 r+(H0/omega)r+(phi2/2)(r/omega)^2,
Delta1(r)=C1 r+(H1/omega)r+(phi2/2L)(r/omega)^2,
Delta2(r)=C2 r+(H2/omega)r.                             (27)
```

Consequently the validated solution is strictly decreasing if

```text
sup_I F_bar' + Delta1(r) < 0.                           (28)
```

Its wall slope is rigorously nonzero and negative if

```text
F_bar'(c)+Delta1(r)<0.                                  (29)
```

These are certificate conclusions, not sampled-grid diagnostics.

## 8. Inertia enclosure

The same checker performs exact-rational interval quadrature of the full
positive-radius density below.  It uses a finite analytic upper bound on the
origin patch and requires a strictly positive lower sum from the remaining
cells.  Thus the returned interval proves both finiteness and strict
positivity; it is not a floating trapezoid estimate.

The dimensionless inertia density is

```text
j(x,F,G)=(2 pi/3)[x^2 sin(F)^2/N
                  +4x^2 sin(F)^2 G^2
                  +4 sin(F)^4/N].                       (30)
```

On every positive-radius cell, interval arithmetic may integrate (30)
directly over the tube defined by (27).  A useful independent Lipschitz audit
is

```text
|d_F j| <= (2 pi/3)[x^2|sin(2F)|/N
                    +4x^2|sin(2F)|G^2
                    +16|sin(F)^3 cos(F)|/N],
|d_G j| <= (16 pi/3)x^2 sin(F)^2 |G|.                   (31)
```

Thus a directed quadrature `I_bar` for the approximate profile gives, for
cellwise bounds `JF,JG`,

```text
I(F) >= I_bar_lower
       -sum_cells width[JF Delta0(r)+JG Delta1(r)].      (32)
```

The interval `[0,a]` is integrated from the exact AU.0c origin family, not from
the global graph ball.  Positivity of the right side of (32) proves a positive
finite inertia.  Alternatively, since (30) is nonnegative, any one subinterval
on which the profile tube keeps `sin(F)^2` away from zero already supplies a
strict lower bound.

## 9. Exploratory numerical scale

The trusted 43-cell endpoint-corrected audit now gives

```text
||G(F_bar)||_infinity   <= 0.002295967024672295
sigma                    in [-2.3462001836132805e-5,
                              1.633679528688307e-5]
Ctau                    <= 9.895351050897547
S                        in [2.9014354731562104,
                              3.017938531159798].
```

The same Barta partition and lifted-auxiliary correction give

```text
C0 <= 1.9539071458684116
C1 <= 1117.028419047634
C2 <= 177527.30674407186
H0 <= 0.0738601508930242
H1 <= 8.490094209841963
H2 <= 1131.636765910181.
```

These interval bounds concern the exact approximate-profile operator and
corrected center family. They do not yet verify `Z0`, `M(r)`, or the radii
inequality.

The current floating profile gives approximately

```text
b_bar                 1.57995353
F_bar'(4)            -0.08787580
min/max P             0.08160021, 15.36
min/max Q            -1.54595, 41.41019
max |P'|              12.77753
integral |Q|          38.37462
lambda_1(A_D)          7.16556
S                      2.95967.
```

The floating homogeneous trace representer gives

```text
Ctau                   1.29336
||H||_infinity         0.06244
||H'||_infinity        1.9627
||H''||_infinity      94.25.
```

For example, the exploratory choices `s0=2.9` and `omega=nu=1` would make
the right side of (17) equal to one when `Ctau=1.30`.  The scalar block is
therefore not the numerically delicate part of the current design.

These are diagnostics, not outward enclosures.  Taking only the deliberately
weak targets `alpha=1` and `p0=0.08`, equations (6)--(8) give the rigorous-form
but floating-input estimates

```text
C0       approximately 2,
C1       approximately 1.009e3,
C2       approximately 1.621e5.
```

The elementary global derivative estimate would therefore require roughly
`r<8.7e-5` merely to preserve the sampled wall-slope sign.  This does not show
that the BVP route fails; it shows that the first certificate should also
validate a sharper Green-kernel bound for

```text
sup_x integral |partial_x G_A(x,y)| dy,
```

which directly replaces `C1` in (7).  The already favorable trace value
`Ctau approximately 1.29` is evidence that the elementary `C1` estimate is
very conservative.

### 9.1 Factored Green-parametrix replacement

The trusted checker now supports a sharper same-operator inverse certificate.
Let `u_hat(a)=0` be a rational left fundamental spline and `v_hat(c)=0` a
rational right representer spline. With

```text
W=P(u_hat' v_hat-u_hat v_hat'),
G_hat(x,s)=u_hat(min(x,s))v_hat(max(x,s))/w0,
```

the induced operator satisfies `A T_hat=I+E`. If `r_u=A u_hat` and
`r_v=A v_hat`, then `W'=u_hat r_v-v_hat r_u`, so exact cellwise residual and
`L1` bounds propagate the Wronskian defect without using the elementary global
derivative estimate. On each leaf `I`, the checker bounds

```text
epsilon_I = deltaW_I
  + ||r_u||_I integral_(x_I^-)^c |v_hat|/w0
  + ||r_v||_I integral_a^(x_I^+) |u_hat|/w0.
```

When `epsilon=max_I epsilon_I<1`, the certified orientation
`A0 T_hat=I+E` gives `A0^-1=T_hat(I+E)^-1`. Barta invertibility and the Neumann
correction therefore give

```text
Cj <= max_I Cj_hat,I/(1-epsilon),  j=0,1,2,
```

The same identity may retain the row corresponding to a source cell before the
final maximum. These row-local `Cj,I` bounds are rigorous even though the defect
factor `1/(1-epsilon)` is global. Applying the exact auxiliary residual through
that row gives local lifted-family bounds `Hj,I`.

where the `C2` row includes the derivative-jump term
`(1+deltaW_I)/min_I P`. This noncircular certificate reuses the same
fundamental and normalized representer proposals already generated for the
Schur and trace audits. The standalone exact interval audit in
`experiments/skyrmion_green_resolvent_audit.py` closes with

```text
epsilon <= 0.08901403484568955,
C0      <= 0.22813715684064623,
C1      <= 1.4321231091914504,
C2      <= 59.31251557489701.
```

Thus the Green replacement meets the preregistered `C1<3,C2<120` targets.

### 9.2 Legacy exact mismatch checkpoint

The mismatch-only integrated audit now composes the Green-sharpened Schur
certificate with the endpoint-corrected nonlinear center. At the selected
weight `omega=1/4`, it proves

```text
Y  <= 0.0022951016014775287,
Z0 <= 0.0001849432768487344,
K  <= 1.007056251754961.
```

Consequently `Z0<1`, and the exact linearized necessary radius is

```text
Y/(1-Z0) <= 0.002295526143604619.
```

The trial radii `0.001` and `0.002` therefore cannot close even before the
quadratic Hessian term is added. The remaining exact tube candidates are
`0.0025`, `1/300`, and `0.004`. Using the displayed decimal summaries, their
approximate binding `Z2` ceilings are respectively `65.42`, `186.77`, and
`213.02`; the first two are limited by the self-map inequality, while the last
also has contraction ceiling about `249.95`. The exact audit evaluates the
rational inequalities directly. The worst coefficient mismatch occurs in the
wall cell `[3.875,4]`, whereas the nonlinear residual hotspot lies earlier in
the mesh; refinements must therefore be selected by the term that dominates the
final radii polynomial rather than by a single universal hotspot.

### 9.3 Legacy first tube result: quantitative failure

The five-radius legacy sweep completed after the mismatch checkpoint. It gives

```text
Z2(0.001) <= 4229.648205291088,
p(0.001)  <= 0.0034101106473999215,
q(0.001)  <= 4.229833148567936.
```

The composed Hessian changes only slightly over the tested radii, and every
self-map and contraction test fails. At the largest admissible trial
`r=0.004`, the audit gives

```text
p(0.004) <= 0.03221753590072926,
q(0.004) <= 16.961032206349017.
```

Thus AU.1 did not close with the legacy global-max Hessian and weight. At
`r=0.004`, the
reported contraction bound implies `Z2 approximately 4240.21`, whereas the
trial permits `Z2` only about `213.02`. The gap is therefore about `19.91`.

This failure does not point first to the nonlinear residual or `Z0`; both are
already small. The selected `omega=1/4` minimizes `Z0` but makes the first-
variation derivative bounds contain

```text
C2 + H2/omega
  = 59.31251557489701 + 94.62647469433571/(1/4)
  approximately 437.8184.
```

The implemented replacement now optimizes the full radii polynomial jointly
over `omega`, records the worst Hessian cell, and separates the direct,
center-equation, affine-lift, scalar, and trace contributions. Reweighting alone
could not supply the missing factor: the Schur
composition multiplies the interior Hessian by approximately
`omega*C_tau/S`, with `C_tau/S approximately 3.68242`, so the crossover occurs
near `omega=S/C_tau approximately 0.27156`, close to the current `1/4`.
The center-equation identity (22a)--(22c), row-local Green norms, and weighted
trace (22d)--(22e) are the implemented reformulation. Their exact closure result
is recorded next.

### 9.4 Exact nonlinear tube closure

The trusted audit summary
`experiments/skyrmion_newton_reduced_hessian_rounded_audit_result.json` and
exact rational archive
`experiments/skyrmion_newton_reduced_hessian_rounded_exact_certificate.json`
close
the prescribed fixed-background BVP at

```text
mu^2=1, lambda=1/400, wall x=4,
omega=3/4, r=1/250.
```

It uses 12-term Taylor/Lagrange trigonometric enclosures and outward-rounds
selected tube intermediates to the exact grid with denominator `10^18`.
Rounding is downward for interval lower endpoints and upward for upper
endpoints; nonnegative norm bounds are rounded upward. This controls rational
denominator growth without introducing a floating premise.

The exact rational comparisons imply the conservative displayed bounds

```text
Y        <= 0.002296,
Z0       <= 0.000078,
Z2       <= 78.733,
p(0.004) < -0.00107,
q(0.004) < 0.31501.
```

Both the self-map and contraction inequalities therefore hold. The physical
post-check then proves strict monotonicity, wall slope in
`[-0.09465,-0.08746]`, and dimensionless rotor inertia in
`[21.149,48.921]`. The conclusion is existence and uniqueness inside the
certified Newton ball. It is not global uniqueness and does not include
Einstein-Skyrme backreaction.

For comparison, retaining row-local Green norms but not the center-equation and
weighted-trace reformulation reduced the legacy `Z2` from about `4240.21` only
to `792.51`; it still failed. The closing improvement is therefore attributable
to the correlated center-equation Hessian together with the cell-weighted trace,
not to mesh localization alone.

## 10. Certificate checklist

The trusted AU.1 checker should accept a rational certificate only after it
independently verifies:

1. exact endpoint correction and the residuals `R,sigma`;
2. `P>=p0` and `(A v_*)/v_*>=1` on every independent cell;
3. the existing origin intervals for `Phi`, `Gamma`, `Phi_b`, `Gamma_b`,
   `Phi_bb`, and `Gamma_bb`;
4. the auxiliary residual, derivative trace bound, and `|S|>=s0`;
5. all coefficient bounds entering (20)--(22);
6. one of the linearly admissible radii satisfying (24) or (25);
7. the sign tests (28)--(29) and an inertia lower bound from (32).

The theorem additionally requires `a>0`, positivity of the center principal
coefficient on every cell, a Schur interval excluding zero, and containment of
the complete Newton slope tube in the certified twice-differentiable origin
family. The checker rejects a certificate when any of these provenance or
domain conditions fail. Local uniqueness follows from invertibility of the
Dirichlet center operator together with the nonzero scalar Schur complement.

Until those seven checks close with exact rational intervals, the floating
profile remains feasibility evidence rather than AU.1.
