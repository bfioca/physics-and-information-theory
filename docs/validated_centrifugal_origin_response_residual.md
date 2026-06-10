# Validated Origin Response Residual

The positive-radius response residual must not be extended to `x=0` by
interval evaluation of singular-looking coefficients. In the regular
variables

```text
t=x^2,  g=xv(t),  f=x[-v(t)+t u(t)],
```

the conormal blocks and rotational load have the exact forms

```text
C=Cbar, M=x Mbar, P=t Pbar, s0=x shat0, s1=t shat1.
```

Let

```text
a=(-v+tu,v),
d=y',
Z=Pbar d+Mbar^T a-shat1.
```

Since the physical residual conormal is `-r1=tZ`, direct differentiation gives

```text
r(x)=s-Ay=x Rhat(t),
Rhat=shat0-Cbar a-Mbar d+2[Z+t Z_t].
```

The implementation propagates interval `t` jets through the already audited
regular conormal kernels, evaluates exact rational polynomial trials `u,v`,
and ranges `Rhat` without a reciprocal of `x` or `t`. It also retains the
physical cutoff value `r1(x0)=-tZ`, which is needed whenever a signed origin
action is joined to positive-radius cells that remain in weak form. Therefore

```text
integral_0^x0 |r|^2 dx
 <= x0^3/3 sum_i sup |Rhat_i|^2.
```

`certify_full_domain_energy_dual_residual_upper` joins this weighted origin
bound to contiguous positive-radius residual cells and then applies the global
coercivity and wall-trace theorem. It requires an explicit
`interface_distribution_free` proof flag; callers must separately check that
the origin and outer trials have matching physical field and conormal data at
the split.

This closes the general cancellation-safe origin residual formula. Exact
primal/adjoint regular-origin trial polynomials are now archived and match the
outer rational trials in field value and physical derivative. Authenticated
origin profile-kernel derivative boxes and the primal origin residual are now
certified from the validated quintic family. The subsequent exact conormal
interface theorem includes the origin join, and
`validated_centrifugal_origin_adjoint_load.md` supplies the loaded adjoint
residual. A useful full-domain response interval still requires the separate
correlation-preserving adjoint redesign; the primal wall mismatch is certified
separately.
