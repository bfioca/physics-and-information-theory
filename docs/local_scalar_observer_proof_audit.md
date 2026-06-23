# Clean-Room Proof Audit: Final-Support Thermal Dephasing

**Status:** all central claims passed an author-side clean-room derivation;
independent human proof review remains open

## Audit Protocol

The audit restarts from the model definitions and theorem statements and
rederives each implication rather than treating the manuscript steps or the
production Python formulas as evidence. It is clean-room in derivation
structure, not blinded in personnel or information access: the same author
workflow had previously seen the manuscript. The numerical replay is
separately implemented in
[`experiments/local_scalar_observer_clean_room_check.py`](../experiments/local_scalar_observer_clean_room_check.py):
it imports neither `qgtoy` nor the production Galerkin code.

This is meaningful adversarial coverage, but not social independence. It was
performed within the author workflow and does not replace an unaffiliated
mathematician or detector/QFT specialist.

The allowed dispositions in this record are exactly:

- `PASS, independent derivation`
- `PASS, independent computation`
- `FAIL`
- `NOT CHECKED`

## Claim Table

| Claim | Disposition | Independent check |
| --- | --- | --- |
| Weyl-channel factor of two | `PASS, independent derivation` | Opposite pointer branches differ by the Weyl displacement `2EJ`; the quasifree characteristic function gives `|kappa|=exp[-2 mu(EJ,EJ)]`. |
| Canonical covariance and energy forms | `PASS, independent derivation` | Expanding `K(q,p)=2^-1/2(h^1/2 q+i h^-1/2 p)` gives the stated `q` and `p` forms and `E=(||hq||^2+||p||^2)/2`. |
| Reflected thermal kernel and scaling | `PASS, independent derivation` | The sine transform and the partial-fraction expansion of `coth` reproduce `B_beta,L` and `C_beta(L)=2L Lambda(pi L/beta)`. |
| Compactness and operator positivity | `PASS, independent derivation` | The logarithmic diagonal is square integrable; positivity follows from the compressed positive spectral multiplier, not merely from pointwise kernel positivity. |
| Simplicity and optimizer uniqueness | `PASS, independent derivation` | The kernel is positivity improving away from null sets, so Perron-Jentzsch gives a simple positive top eigenfunction; positive semidefiniteness makes it the operator norm. |
| Strict reduction to the s-wave momentum sector | `PASS, independent derivation` | Every term in the thermal resolvent series is strictly order decreasing under `A_l>A_0` for nonzero data. |
| Coordinate-sector domination | `PASS, independent derivation` | Dirichlet Poincare plus `coth z<=1+1/z` gives the coordinate bound, which lies strictly below the two-piece momentum lower envelope for every `y>0`. |
| Uniform small-support remainder | `PASS, independent derivation` | Euler's product gives a nonnegative kernel correction with Schur row bound `tau^2/(3pi)`. |
| Uniform large-support `beta/3` remainder | `PASS, independent derivation` | The remainder is a positive sum of Dirichlet half-line resolvents with norm at most `pi/(6tau)`. |
| Smooth compact source density | `PASS, independent derivation` | Interior `C_c^infinity` momenta are dense in `L2`; the compressed covariance is bounded and the cutoff homogeneous solution realizes each approximant. |
| Final support versus fixed source cylinder | `PASS, independent derivation` | The construction proves sharpness for final data and for source worldtubes approaching that ball; it does not prove near-controllability from every smaller fixed cylinder. |
| Independent leading-eigenvalue reconstruction | `PASS, independent computation` | A midpoint/product-integration matrix passes analytic brackets and coarse/fine convergence on `0.005<=y<=100`. |
| Independent asymptotic stress tests | `PASS, independent computation` | The frozen checker verifies the small- and large-support remainder inequalities on dedicated grids. |

No row is currently `FAIL` or `NOT CHECKED`. That statement concerns the
listed internal checks only, not external proof coverage or novelty.

## Derivation Ledger

### 1. Channel normalization

For pointer eigenvalues `z=+1,-1`, the conditional field unitaries are
`U_z=exp[-i z phi(J)]`. The off-diagonal trace contains

```text
U_-^dagger U_+ = W(-2EJ)
```

up to a phase. With `omega[W(f)]=exp[-mu(f,f)/2]`, this gives

```text
|kappa|=exp[-2 mu(EJ,EJ)]=exp(-Gamma).
```

This matches the `nu_j=omega(W(E(2f_j)))` normalization in
[Landulfo (2016)](https://arxiv.org/abs/1603.06641). Expanding the static
one-particle map gives

```text
Gamma=<q,h coth(beta h/2)q>+<p,h^-1 coth(beta h/2)p>,
E=(||h q||^2+||p||^2)/2.
```

Thus the momentum quotient contains the factor `2||B_beta,L||`.
No missing factor of two was found.

### 2. Kernel, scaling, and principal eigenfunction

The half-line sine transform turns the momentum form into

```text
(2/pi) integral_0^infinity sin(kx)sin(ky)coth(beta k/2) dk/k.
```

Taking the reflected cosine difference yields

```text
B_beta,L(x,y)=pi^-1 log{
  sinh[pi(x+y)/beta]/sinh[pi|x-y|/beta]}.
```

The unitary dilation `x=Lu` gives `B_beta,L` equivalent to
`L K_(pi L/beta)`. The logarithmic singularity is in `L2((0,1)^2)`, hence the
operator is Hilbert-Schmidt. Its positivity comes from
`P_L h^-1 coth(beta h/2) P_L>=0`. Since its position kernel is strictly
positive for `u,v>0` off the diagonal, it is positivity improving and has a
simple strictly positive top eigenfunction.

### 3. Angular and canonical sectors

For `A_l=A_0+l(l+1)/(R^2 sinh^2(x/R))`,

```text
h_l^-1 coth(beta h_l/2)
 = (2/beta) A_l^-1
   +(4/beta) sum_(n>=1)[A_l+(2pi n/beta)^2]^-1.
```

Every summand is order decreasing in `A_l`. Equality for a nonzero datum would
force the resolved vector to vanish where the angular potential is positive,
and hence everywhere. This makes the `l=0` momentum comparison strict.

For zero-extended coordinate data, Poincare and Cauchy-Schwarz give

```text
Gamma_q/(E_q R) <= 2y/pi+2y^2/pi^3.
```

The momentum trials give `max(3y/pi,8y^2/pi^3)`. The coordinate expression is
at most the first term for `y<=pi^2/2` and at most the second for
`y>=pi^2/3`; those intervals overlap. At either formal endpoint, the omitted
positive thermal contribution makes the comparison strict.

### 4. Uniform support remainders

For `A=tau(u+v)` and `B=tau|u-v|`, Euler's product gives

```text
0 <= log[(sinh A/A)/(sinh B/B)] <= (A^2-B^2)/6.
```

Its largest row integral is `tau^2/(3pi)`, so

```text
0<=C_beta(L)-2L Lambda(0)<=2pi L^3/(3beta^2).
```

For large support,

```text
k_tau=(2tau/pi)min(u,v)+r_tau,
r_tau=pi^-1 sum_(n>=1) n^-1 {
  exp[-2n tau|u-v|]-exp[-2n tau(u+v)]}.
```

Each bracket is a positive Dirichlet resolvent kernel. Its half-line row
integral is at most `1/(n tau)`, including the outer `1/n` only after the
sum is formed, so `||r_tau||<=pi/(6tau)`. Since
`||min(u,v)||=4/pi^2`,

```text
0<=C_beta(L)-16L^2/(beta pi^2)<=beta/3.
```

### 5. Source closure and exact scope

Choose normalized `p_n in C_c^infinity(0,L)` converging in `L2` to the top
eigenfunction. On `[0,L]`,

```text
P_L h^-1 coth(beta h/2) P_L
 <= P_L h^-1 P_L+(2/beta)P_L h^-2 P_L,
```

and both compressed forms are bounded. The Rayleigh quotients therefore
converge. Also,

```text
sup_x |integral_0^x(p_n^2-p^2)|
 <= ||p_n-p||_2 (||p_n||_2+||p||_2),
```

so cumulative energy measures converge uniformly.

For each interior smooth target, let `phi_free` be its homogeneous solution,
take a time cutoff `eta` that is zero in the past and one near the final
slice, and set `J=P(eta phi_free)`. The retarded solution is exactly
`eta phi_free`. If the target ends at `L-delta`, a transition shorter than
`delta` keeps `J` inside the declared optical worldtube by finite propagation.
This proves the final-support supremum and an approaching-worldtube limit,
not fixed-smaller-cylinder controllability.

## Independent Numerical Record

Run:

```bash
python experiments/local_scalar_observer_clean_room_check.py
```

The frozen output is
[`experiments/local_scalar_observer_clean_room_check.json`](../experiments/local_scalar_observer_clean_room_check.json).
It uses 80 and 160 midpoint cells, a transformed 32-point product rule on the
singular diagonal, and a de Sitter support grid from `y=0.005` through
`y=100`. It checks:

- every leading-eigenvalue estimate against analytic lower and upper bounds;
- positivity of every sampled principal vector;
- the small-support remainder through `y=0.3`;
- the global large-support remainder through `y=100`;
- strict coordinate-sector domination on 2,001 logarithmic samples from
  `10^-6` to `10^6`; and
- coarse-to-fine stability, with the maximum recorded relative step below
  `6e-4`.

These are `PASS, independent computation` results. They do not turn the
analytic inequalities into computer-assisted proofs.

## External Gate

The clean-room audit reduces the proof-review workload but does not authorize
submission. External readers must still check the normalization, strict
resolvent comparison, uniform remainder argument, and cutoff-source support
construction. Both domain novelty reviews also remain open.
