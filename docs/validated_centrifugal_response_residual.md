# Validated Centrifugal Response Residuals

Status: exact reusable positive-radius residual theorem. No full-domain primal
or adjoint residual has yet been generated.

## Purpose

`qgtoy.validated_centrifugal_response_residual` bridges the authenticated
Skyrmion profile replay and the exact dual-weighted response theorem. It never
differentiates sampled floating data. Its inputs on one cell are rational
interval enclosures of

```text
(x,F,F',F'')
```

and exact rational trial polynomials.

`profile_jet_cell_from_sharp_replay` directly adapts a
`ValidatedSkyrmionSharpRadialCell`, preserving its authenticated profile,
first-derivative, and second-derivative boxes.

## Exact strong form

Write the physical quadratic form as

```text
q(y,v)=integral [v^T C y+v^T M y'+v'^T M^T y+v'^T P y'] dx.
```

The regular conormal kernel supplies `Cbar,Mbar,Pbar`. The physical blocks are

```text
C=Cbar,  M=x Mbar,  P=x^2 Pbar.
```

A first radial interval jet propagates the authenticated `(F,F',F'')` box
through this algebra, including the identities

```text
rho=-F',
s=sin(F)/x,
s'=(cos(pi-F) rho-s)/x,
[cos(pi-F)]'=-x s rho.
```

Consequently the strong operator is enclosed without finite differences:

```text
A y=(C-(M')^T)y+(M-M^T-P')y'-P y''.
```

The rotational weak load has the regular factorization

```text
s0=x shat0,  s1=x^2 shat1,
```

so its strong representative is enclosed as `s0-s1'` by the same jet.

## Rational conforming trials

Each `RationalC1TrialCell` stores the two fields as exact polynomials in the
local normalized coordinate `u in [0,1]`. The validator checks exact radial
contiguity, equality of both field values and physical derivatives across
every join, and the essential `g(a)=0` wall trace. Piecewise `C1` continuity
removes internal conormal delta terms because the authenticated coefficients
are continuous functions of the common profile.

For a strong residual box `r_i` on a cell `I`, the certified integral is

```text
integral_I |r|^2 dx
 <= |I| sum_i sup_I |r_i|^2.
```

All endpoints are exact `Fraction` values. Square roots used in norm bounds
are enclosed by rational bisection.

## Energy-dual composition

Let `c>0` be the global operator lower bound and `m_w>0` the completed wall
trace margin. Keeping the free radial conormal mismatch `eta` separate from
the bulk residual gives

```text
||R||_(V*) <= ||r||_2/sqrt(c)+|eta|/sqrt(m_w).
```

Thus the certified repository values `c=1/100` and
`m_w>=0.212023810536...` can be inserted directly. The returned exact upper
bound is suitable as `delta_y` or `delta_z` in
`certify_dual_weighted_response_interval`.

The composer requires the residual cells to cover an explicitly declared
domain and requires the caller to affirm that internal conormal distributions
have been excluded. For trials generated over one authenticated continuous
profile, exact piecewise `C1` continuity supplies that premise. A separately
certified origin residual must be included before declaring the full domain.

The wall helper computes

```text
eta=(M^T y+P y')_f+k_w f(a)-ell_wall,
```

where `k_w` is the interval wall quadratic-form coefficient and `ell_wall` is
zero for the primal problem or the effective master-response trace for the
adjoint.

## Claim boundary

This module proves the residual and norm inequalities for supplied cells.
Exact physical primal and adjoint trials are now archived, but a response
certificate still requires tight centered/Taylor-model coefficient
enclosures and an interval representation of the adjoint bulk master load.
The exact conormal interface cancellation and the primal origin, primal wall,
and loaded adjoint wall residuals are now certified separately.

The positive-radius kernel deliberately rejects a cell touching `x=0`.
Applying `sin(F)/x` there would discard the exact origin cancellations already
encoded by the regular-origin modules. It also does not authenticate profile
archives itself; callers must use the existing authenticated replay pipeline.

## Verification

```text
PYTHONPATH=. python -m pytest -q \
  tests/test_validated_centrifugal_response_residual.py
ruff check qgtoy/validated_centrifugal_response_residual.py \
  tests/test_validated_centrifugal_response_residual.py
```

The focused tests cover exact `C1` rejection, essential wall-trace rejection,
an analytic residual-square example, exact coercivity/wall-margin composition,
wall mismatch separation, and enclosure of the original physical Hessian at a
sample point.
