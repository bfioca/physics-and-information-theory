# Exact Paper-R Weyl Observable Transfer

Status: exact analytic transfer theorem; the exterior-amplitude interval is
still supplied by the response certificate.

Outside the supported source, the static `ell=2` master field factorizes as

```text
Psi(x)=A_ext v_H(x/R),
v_H(s)=(3-s^2)/(2s^2).
```

After projecting the physical electric-Weyl tensor onto a unit Frobenius-norm
quadrupole and removing the declared action, gravitational, and state-tensor
scales, the dimensionless radial coefficient is `b_W(x)=Psi(x)`.  Define

```text
B_W={1/5 integral_5^10 b_W(x)^2 dx}^{1/2},  R=20.
```

The horizon-regular mode obeys

```text
v_H(x/20)=600/x^2-1/2,
1/5 integral_5^10 v_H(x/20)^2 dx=625/4.
```

Therefore the annular observable has the exact relation

```text
B_W=(25/2)|A_ext|.                                  (R.W.1)
```

Any directed response interval excluding zero transfers immediately to a
strictly positive `B_W` lower bound, with no quadrature or transcendental
remainder.  Conversely, an amplitude interval containing zero gives no
positive lower bound.

Equation (R.W.1) is a normalization and transfer theorem only.  It does not
certify the sign of `A_ext`, add finite-rotation control, or turn the
fixed-background response into a universal gravitational capacity bound.

Reproduce with

```bash
python -m pytest -q tests/test_paper_r_weyl_observable.py
```

