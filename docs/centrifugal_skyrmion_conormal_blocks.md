# Regular Conormal Blocks And Residual Divisibility

The finite-origin transfer needs quantitative control of a first-order Fuchs
system. This note supplies the exact coefficient algebra and closes the formal
residual-order question left open by the conormal scaffold.

Let

```text
t=x^2,  a=y/x,  d=y',
rho=-F',  s=sin(pi-F)/x,  c=cos(pi-F).
```

After all powers of `x` cancel, the physical static density has the exact
regular form

```text
H_static/t = a^T Cbar(t) a
             +2 a^T Mbar(t) d
             +d^T Pbar(t) d.
```

Thus the original weak-form blocks satisfy

```text
C=Cbar,  M=x Mbar,  P=t Pbar.
```

The implementation polarizes this regular density at the kernel level. Three
independent positive-radius probes reproduce every entry of the established
physical Hessian to floating roundoff, while the exact origin block equals
the previously certified indicial Hessian.

## Source Factorization

The rotational source factors more strongly than the generic conormal
scaling:

```text
s0=x^3 r0(t),  s1=x^4 r1(t).
```

Equivalently, `shat0=t r0` and `shat1=t r1`, so the conormal forcing obeys
`q(t)=O(t)`. The factored source reproduces the established physical source
covector at the same positive-radius probes.

## Residual Theorem

The regular blocks are analytic functions of `t` and their origin value is
the exact `A0`, hence

```text
A(t)-A(0)=O(t).
```

For each of the linear homogeneous, cubic homogeneous, and forced particular
germs, the earlier exact recurrence proves that the Euler residual after the
`x^5` terms is `O(x^7)`. The conormal derivation gives the exact identity

```text
lower conormal residual = - Euler residual / x.
```

Therefore every germ has conormal residual

```text
O(x^6)=O(t^3).
```

This closes the formal divisibility input for `X=X_c+t^3R` without expanding
large uncancelled rational functions.

## Reproduce

```bash
PYTHONPATH=. python experiments/centrifugal_skyrmion_conormal_blocks_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_conormal_blocks.py tests/test_centrifugal_skyrmion_conormal_blocks_audit.py
```

## Claim Boundary

This theorem gives exact regular blocks, source order, and residual
divisibility. It does not yet bound `delta=sup||A-A0||_w` or the scaled
residual `epsilon=sup||e||_w` on the validated quintic profile tube. Those are
the two remaining quantitative inputs to the finite-cell radii inequality.
