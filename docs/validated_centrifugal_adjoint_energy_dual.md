# Validated Partial Adjoint Form-Dual Bound

Status: positive-radius-plus-wall partial theorem complete

The weak adjoint residual has the natural form

```text
R(v)=integral(r0 dot v+r1 dot v') dx+eta_wall f(a).
```

Because `r1` is nonzero, assigning it an `L2` strong-residual norm would be
invalid. The certified lift instead uses the same Liouville completed square
that proves coercivity. With

```text
d=v'+P^-1(M^T-K)v,
x d=x v'+T v,
T=I/2-Pbar^-1 Abar,
```

the bulk residual becomes

```text
integral[(r1/x) dot (x d)+(r0-T^T(r1/x)) dot v] dx.
```

The authenticated lower bounds `Pbar>=I/100` and `V_completed>=I/100`
therefore give a direct `V*` estimate. The wall residual is added in the same
quadratic sum using its positive trace margin.

On `344` positive-radius cells plus the loaded adjoint wall trace, the audit
certifies

```text
partial squared dual upper = 0.592007476516919181,
partial energy-dual upper  = 0.769420221021594403.
```

The wall contributes less than `1/5000` to the squared bound. The dominant
cell is `[1/2,67/128]`, and the adjusted bulk value coefficient accounts for
more than `99%` of the squared total. The obstruction is not the wall or a
center singularity.

This is an honest negative diagnostic for the present interval representation:
it is far above the roughly `0.04` design target. The next improvement must
retain radial/profile/trial correlations in the weak load and completed-square
multiplier, just as the centered primal theorem did.

The artifact described on this page deliberately omits the regular-origin
master load and is therefore a partial bound. The follow-up certificate
`validated_centrifugal_origin_adjoint_load.md` closes that omission: its
contribution to the squared dual bound is below
`0.000000248149232003`. The dominant positive-radius wrapping and the need for
a correlation-preserving redesign are unchanged.

Reproduce with

```bash
python experiments/validated_centrifugal_adjoint_energy_dual_audit.py
python -m pytest -q \
  tests/test_validated_centrifugal_adjoint_energy_dual.py \
  tests/test_validated_centrifugal_adjoint_energy_dual_audit.py
```

Artifact: `experiments/validated_centrifugal_adjoint_energy_dual.json`, SHA256
`500e56b5aa36c64846100dc59a7383b2051a12c6676fcf8e6d49574f61142d0e`.
