# Authenticated Static Bulk Lapse Control

Status: fixed-field spherical static bulk theorem; rotation and membrane lapse
matching open.

## Enthalpy Cancellation

For the static spherical Skyrmion, the dimensionless energy density and radial
pressure satisfy the exact identity

```text
rho_bar+p_r_bar
 = A F'^2 [1/4+2sin^2(F)/x^2].                       (1)
```

In areal gauge, write

```text
ds^2=-sigma(x)^2 A(x)dt^2+A(x)^-1dr^2+r^2dOmega^2.
```

The spherical Einstein lapse equation contains `(rho+p_r)/A`, so the radial
metric factor cancels from (1). With

```text
alpha=2G/(e^2R^2lambda),
D=2pi int_0^xw x F'^2[1/4+2sin^2(F)/x^2] dx,
```

and exterior normalization `sigma(x_w)=1`,

```text
exp(-alpha D)<=sigma(x)<=1.                          (2)
```

If the directed radial certificate is enforced through
`alpha H_upper<=beta`, then

```text
log[1/sigma(0)]<=beta D_upper/H_upper,
|g_tt|/|g_tt,dS| >= (1-beta)exp[-2beta D_upper/H_upper]. (3)
```

## Authenticated Default

Exact replay with two positive-radius subdivisions per parent cell and 64
regular-origin cells gives

```text
D<=43.445333,
H<=29.246336.
```

For `beta=1/2`,

```text
log[1/sigma(0)]<=0.742748305291986,
|g_tt|/|g_tt,dS| >= (1/2)exp[-2(0.742748305291986)]. (4)
```

The floating diagnostic for the last expression is `0.1131949425712049`. The
exponential is recorded as a diagnostic; the exact certified statement is the
rational log-lapse bound in (4).

This shows that the default `beta=1/2` point is horizon-free and quantitatively
controlled, but it is not a small-perturbation metric window. A paper claiming
negligible backreaction must impose a substantially tighter radial budget and
repeat the rotational stress analysis.

## Claim Boundary

The theorem holds for the authenticated static field held fixed in a spherical
bulk. It does not include collective rotation, field deformation, the membrane
Israel conditions, exterior time normalization across a gravitating shell,
nonspherical stress, or off-center support.

## Reproduction

```bash
python experiments/skyrmion_static_lapse_audit.py
python -m pytest -q tests/test_skyrmion_lapse_control.py \
  tests/test_skyrmion_static_lapse_audit.py
```

Artifact:

```text
experiments/skyrmion_static_lapse_exact_certificate.json
SHA256 2072131929fd5c9ff70ced4e468aa5dd937cc84cbffe9efd83529cfa6693171b
```
