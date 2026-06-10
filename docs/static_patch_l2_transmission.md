# Static Quadrupole Shell Transmission

The ideal moving membrane produces a literal master source

```text
F=D0 delta(r-a)+D1 delta'(r-a)+D2 delta''(r-a).
```

For the frozen operator

```text
A2 Psi=-(N Psi')'+6 Psi/r^2,
```

write `Psi=c delta+Psi_off`. Distributional differentiation gives the exact
contact and jump laws

```text
c=-D2/N_a,
D1_off=D1+D2 N'_a/N_a,
D0_off=D0+6D2/(a^2 N_a),
[Psi_off]=-D1_off/N_a,
[N Psi_off']=-D0_off.
```

Here `[X]=X(a+)-X(a-)`. Direct two-sided limits of

```text
Psi_off=D0_off G2(r,a)-D1_off partial_a G2(r,a)
```

reproduce both jumps exactly. This supplies a master-equation junction check
that is independent of evaluating the response at separated sample points.
For the completed 401-node Skyrmion source, both jumps are nonzero.

This is not yet tensorial Israel matching. It proves that the contact
subtraction and Green response solve the declared distributional master
equation. Metric reconstruction, induced-metric/extrinsic-curvature jumps, and
a finite-thickness membrane limit remain separate gates.

## Reproduction

```bash
python experiments/static_patch_l2_transmission_audit.py
python -m pytest -q tests/test_static_patch_l2_transmission.py \
  tests/test_static_patch_l2_transmission_audit.py
```

The source-hashed artifact is
`experiments/static_patch_l2_transmission_certificate.json`.
