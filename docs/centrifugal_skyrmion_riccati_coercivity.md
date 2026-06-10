# Matrix-Riccati Coercivity Route

The certified origin transfer leaves one decisive continuum question: does the
two-channel moving-wall quadratic form have a positive inverse? A pointwise
positivity proof cannot work. The completed-square potential
`C-M P^-1 M^T` has a negative eigenvalue over a substantial middle-radius
region even though the floating Galerkin eigenvalue approaches `0.35348`.

## Exact Identity

For

```text
q[y]=y'^T P y'+2y^T M y'+y^T C y
```

choose a symmetric matrix multiplier `K`, set `D=M-K`, and define

```text
R_alpha=C-alpha I-D P^-1 D^T-K'.
```

Then exact algebra gives

```text
q[y]-alpha |y|^2
 = (y'+P^-1 D^T y)^T P (y'+P^-1 D^T y)
   +(y^T K y)'+y^T R_alpha y.
```

Consequently, `P>0`, `R_alpha>=0`, a nonnegative allowed wall trace, and a
vanishing origin trace imply `q[y]>=alpha ||y||_2^2` on the smooth core. The
first-order square also supplies the natural closable graph operator for the
eventual Friedrichs construction. No derivative of `P` or `M` is required.

## Preferred Explicit Candidate

The simple choice

```text
K=sym(M)-P/(2x)
```

is regular because `M=x Mbar` and `P=x^2 Pbar`. With
`Abar=(Mbar-Mbar^T)/2`, its completed potential is exactly

```text
W_K = C-sym(Mbar)+Pbar/4
      -2t sym(Mbar)_t+t Pbar_t+Abar Pbar^-1 Abar.
```

The audit verifies this desingularization with exact rational matrix algebra.
Floating profile refinements from step `0.002` through `0.00025` give stable
minimum eigenvalues from `0.07863543` to `0.07863388`, always near
`x=1.9821`. The allowed wall remainder is about `0.2143`. This selects the
authenticated target

```text
q[y] >= (1/20) ||y||_2^2.
```

The explicit multiplier is now preferred because its interval proof needs
only coefficient jets and two Sylvester minors, with no global multiplier ODE.

## Riccati Fallback

For a stronger fallback, the floating generator solves the matrix Riccati equation at construction
shift `beta=0.2` and tests the lower target `alpha=0.1`. The shifted indicial
roots are approximately

```text
-3.94261214, -1.79346007, 0.79346007, 2.94261214.
```

Thus the construction retains two finite-energy origin modes. A cubic-Hermite
multiplier on the full interval gives the reproducible sampled margins

```text
minimum eigenvalue of R_0.1  > 0.09999,
allowed wall trace margin    > 0.491,
```

with a symmetric multiplier of norm below `1.1`. The large bulk margin is not
an accidental mesh eigenvalue: it is the deliberate shift gap `beta-alpha`,
degraded only by candidate interpolation error.

## Remaining Proof Obligation

This is still a route audit, not a spectral theorem. The next checker must:

1. evaluate the exact regular `W_K-(1/20)I` over every authenticated nonlinear
   profile-tube jet, with exact trigonometric enclosures;
2. prove both Sylvester minors positive on every cell;
3. certify the wall scalar `B_ff+K_ff(a)>0`;
4. prove the origin boundary term vanishes on the smooth Friedrichs core;
5. close the first-order factor form and infer an inverse norm at most `20`.

The numerical margins are large enough that ordinary interval overestimation,
not physical near-criticality, is now the main technical risk.

## Reproduction

```bash
PYTHONPATH=. python experiments/centrifugal_skyrmion_riccati_coercivity_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_riccati_coercivity.py \
  tests/test_centrifugal_skyrmion_riccati_coercivity_audit.py
```
