# Validated Centrifugal Adjoint Bulk Load

Status: certified positive-radius weak-load representation; a full adjoint
energy-dual residual is not yet certified.

## Derivative-free weak reduction

For the completed stress amplitudes

```text
T=(rho,p_r,j,pi)=T_rigid+L0 y+L1 y',  y=(f,g),
```

the static `l=2` master source has the density derivative term

```text
F=kappa[-A rho'+D rho-x p_r/2-j+2x pi],
A=x^2 N/6,  D=x(1+4 lambda x^2)/6.
```

With exterior Green weight `w=(2R/15)u(x/R)`, exact integration by parts
gives

```text
integral w F dx
 = boundary + integral c dot T dx,
c=(kappa[(wA)'+wD], -kappa wx/2, -kappa w, 2 kappa wx).
```

Consequently the deformation load is exactly

```text
B_bulk(v)=integral (b0 dot v+b1 dot v') dx,
b0=L0^T c,  b1=L1^T c.
```

This representation requires only the authenticated profile value and first
derivative. It does not differentiate a profile remainder or require a profile
second derivative. The center boundary term vanishes by regularity; the wall
term is handled by the independent moving-wall load certificate.

## Validated implementation

`qgtoy/validated_centrifugal_adjoint_bulk_load.py` provides:

- a generic-scalar exact affine weak-load kernel;
- a positive-coefficient series enclosure for `w,w'` on `x/R<=1/5`;
- exact-rational interval boxes for `b0,b1` on a supplied profile cell;
- a range-times-width integral enclosure on an exact rational trial cell;
- coefficient boxes for `B(v)-q(v,z_h)` in the form `r0 dot v+r1 dot v'`.

The source-hashed audit replays the authenticated profile and exact archived
trials on `344` positive-radius cells. It certifies

```text
B_bulk(primal trial)  in [-0.002249596437198199, 0.001052714255862833],
B_bulk(adjoint trial) in [ 0.000012035950858950, 0.000083040071016445].
```

The componentwise weak residual coefficient bounds are

```text
max |r0_i| <= 0.012135653554083077,
max |r1_i| <= 0.009194661537655243.
```

The nonzero `r1` is important: integrating it by parts would require a
validated derivative of the load coefficients. The present result instead
keeps the residual in its natural form-dual representation.

## Claim boundary and next step

This theorem covers only the positive-radius bulk load and coefficient-level
weak residual. It does not cover the regular-origin master load and does not
convert `(r0,r1)` into an energy-dual norm. The next valid closure is a direct
form-dual/Riesz bound for these weak coefficients, combined with the regular
origin load and the already certified wall coefficient. Only then may the
dual-weighted response theorem use a loaded adjoint residual.

Audit artifact:
`experiments/validated_centrifugal_adjoint_bulk_load.json`, SHA256
`3db6d390d521494d192c5df6b4bc5dfd1ee09f6d441f0bd69c3be2d18add44f5`.
