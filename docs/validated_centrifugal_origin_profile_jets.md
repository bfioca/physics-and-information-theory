# Authenticated Origin Profile Jets

The cancellation-safe response residual needs regular profile kernels and
their first `t=x^2` derivatives on `0 <= x <= 1/16`. The uniform quintic
origin theorem supplies

```text
rho=-F'=b-3ct-5dt^2+t^3 r_p,  |r_p|<=13/10,
u=(pi-F)/x=b-ct-dt^2+t^3 r_u, |r_u|<=13/70.
```

Those are `L-infinity` remainder statements. Differentiating `r_p` or `r_u`
would therefore be invalid. The response bridge instead uses two exact
identities. First,

```text
rho=u+2t u_t
```

gives `u_t` directly from the correlated quintic form. Second, the exact
Volterra equation gives `rho_t`. Its apparent quotient by `t` is removed
algebraically using the entire centered kernels

```text
[sinc(sqrt(w))-1]/w,   [sinc(2sqrt(w))-1]/w,
w=t u^2.
```

No profile remainder is differentiated and no interval containing zero is
inverted. Exact-rational entire-series tails then enclose the required jets

```text
N, N_t, rho, rho_t,
sin(F)/x, d_t[sin(F)/x],
cos(pi-F), d_t cos(pi-F).
```

Two rational shooting-slope cells cover the complete authenticated AU.3b
slope interval. At the removable center, their boxes contain the exact limits

```text
rho_t(0)                  = -3c,
d_t[sin(F)/x](0)          = -c-b^3/6,
d_t cos(pi-F)(0)          = -b^2/2.
```

Propagating these boxes through the regular conormal kernel and the archived
regular-origin trials gives

```text
primal rotational-load origin residual:
    ||r||_L2(0,1/16)^2 < 1e-3,

adjoint-shaped zero-load operator action:
    ||A z_trial||_L2(0,1/16)^2 < 1e-6.
```

The audit artifact records substantially sharper outward-rounded values.

## Reproduce

```bash
PYTHONPATH=. python experiments/validated_centrifugal_origin_profile_jets_audit.py
python -m pytest -q \
  tests/test_validated_centrifugal_origin_profile_jets.py \
  tests/test_validated_centrifugal_origin_profile_jets_audit.py
```

## Claim Boundary

The first residual is an authenticated primal origin contribution. The
adjoint-shaped calculation deliberately uses zero load and therefore encloses
only the homogeneous operator action. It is not an adjoint residual until the
exterior-amplitude load is derived and enclosed. The conormal match at
`x=1/16`, loaded adjoint residual, full-domain energy-dual interval, and
nonzero exterior response remain open. A separate source-bound artifact now
certifies the primal wall conormal mismatch.
