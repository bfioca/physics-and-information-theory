# Origin-Regular Affine Master Kernel

The regular centrifugal fields are

```text
t=x^2,  F=pi-x w(t),  g=x v(t),  f=x[-v(t)+t u(t)].
```

Direct substitution into the completed stress and static `ell=2` master map
now proves the exact factorization

```text
F_master(x)=x F_hat(t).
```

`qgtoy/centrifugal_skyrmion_origin_master_kernel.py` evaluates `F_hat` without
dividing by `x` or `t`. It uses the entire kernels

```text
s(t)=sin(x w(t))/x,  c(t)=cos(x w(t))
```

and a caller-supplied `s_t`. Every apparent `sin(F)/x`, `f/x`, `g/x`, and
stress derivative is canceled algebraically before interval evaluation. The
result is affine in

```text
(u,u_t,u_tt,v,v_t,v_tt)
```

and remains finite at the exact center. Positive-radius tests compare
`x F_hat` with the independent uncancelled generic master kernel; exact
`Fraction` tests verify every affine coefficient, and an interval test ranges
a cell containing `t=0` without reciprocal-zero failure.

This closes the local algebraic origin regularization of the observable. It
does not enclose the authenticated profile and primal/adjoint fields, prove
their second-time-derivative bounds, integrate the origin cell, or connect a
trial residual to the continuum Friedrichs solution. Those are the remaining
steps before the exterior amplitude can be called interval certified.
