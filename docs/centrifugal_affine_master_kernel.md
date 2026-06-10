# Affine completed-stress and master-source kernel

`qgtoy/centrifugal_skyrmion_affine_master_kernel.py` rewrites the existing
same-action completed stress as the exact pointwise affine map

```
T[f,g] = T_rigid + L0(r) (f,g) + L1(r) (f',g').
```

It also propagates a first radial jet through the energy density before forming
the smooth static-patch `ell=2` master source.  The resulting local source is

```
F = F_rigid + b_f f + b_fp f' + b_fpp f'' + b_g g + b_gp g'.
```

No sampled derivative or finite-difference basis extraction occurs.  The
formulas use only scalar arithmetic and accept caller-supplied `sin(F)` and
`cos(F)`, so the same code runs on `float`, `RationalInterval`, and the current
centered Taylor-model arithmetic.  Exact rational tests compare every exposed
coefficient with direct zero/basis evaluations.

## Moving wall and contact subtraction

The same module now carries the wall calculation without converting to
`float`. The caller supplies `sqrt(N(a))` because square-root enclosure policy
belongs to the validated profile layer, not to this algebraic kernel. From the
hard-wall kinematic condition it keeps the displacement map explicitly named

```
xi = wall_displacement_per_radial_field * f(a),
wall_displacement_per_radial_field = -1/F'(a).
```

The kernel builds the displaced-background plus pure-tension canonical stress
jet, maps it to the literal `delta`, `delta'`, and `delta''` master source, and
then exposes the contact-free `delta`, `delta'` pair. For the exterior Green
factor `G(r,a)=w(a)v(r/R)`, its raw wall amplitude is

```
J_wall,raw = w D0_off - w' D1_off.
```

This contains the endpoint `kappa*w*A*rho_bulk(a)`, where
`A=a^2 N(a)/6`. Integrating the smooth bulk density derivative by parts gives
the opposite endpoint. The implementation forms the surviving expression
directly,

```
J_wall,eff = w (D0_off-kappa*A*rho_bulk) - w' D1_off
           = gamma_B f(a).
```

Forming the cancelled expression directly matters for interval arithmetic:
it makes the `f'`, `g`, and `g'` coefficients identically zero, instead of
subtracting two overlapping interval evaluations. The API therefore exposes
both quantities under deliberately different names:

```
kernel.wall_displacement_per_radial_field
kernel.response_wall_trace_gamma_b
```

At the frozen default floating point, these are approximately `11.37969728`
and `0.002825752976`, respectively. That numerical regression is only a check
of conventions; it is not an interval result.

## What remains for a continuum response certificate

This kernel is algebra, not a response enclosure.  A validated exterior
amplitude still requires:

1. authenticated Taylor models for the profile and the primal/adjoint fields;
2. an origin-regular representation of the apparently singular coefficients;
3. outward-rounded integration of the Green-weighted bulk source;
4. a combined bulk-plus-wall interval separated from zero; and
5. discretization/residual bounds connecting the field enclosures to the
   Friedrichs solution.

Until those steps close, this module must not be cited as continuum validation
of a nonzero master or Weyl response. It also does not establish Israel
matching, surface elasticity, or a self-consistent gravitating wall.
