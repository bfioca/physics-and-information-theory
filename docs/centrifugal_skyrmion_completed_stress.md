# Completed Centrifugal Skyrmion Bulk Stress

This note reconstructs the `O(Omega^2)`, `ell=2` Skyrme stress on the
exploratory two-channel centrifugal branch. It closes the smooth-bulk
conservation defect of the rigid source under mesh refinement. The result is a
same-action numerical consistency check, not yet a distributionally conserved
worldtube or an Einstein observable.

## Stress Reconstruction

Write the physical target-space perturbation as

```text
delta Y=f(r) q(n) e_F+g(r)[Qn-q(n)n],
q(n)=Q_ab n_a n_b.
```

For `N=1-lambda r^2`, `s=sin F`, and `c=cos F`, define

```text
a2=N F'^2,
b2=s^2/r^2,
R=2N F'f',
A=2s(2fc-3g)/r^2,
dT=R+A,
h=s g'+F'(2f-cg).
```

The linearized static deformation stress in dimensionless Skyrme units is

```text
delta rho =dT/8+b2 R+(a2+b2)A/2+mu^2 f s/4,
delta p_r=R(1/4-a2+2b2)+a2 dT-delta rho,
delta p_perp=(1/4+a2)s(2fc-3g)/r^2+b2 dT-delta rho,
delta pi=(1/4+a2)s g/r^2,
delta j=N(1/4+b2)h/2.
```

Adding these amplitudes to the independently derived rigid rotational stress
produces the candidate completed bulk source. The rigid piece agrees
coefficient by coefficient with
`rigid_skyrmion_stress_conservation.py` at `e=f_pi=I=1`.

## Conservation Test

In the mixed-stress convention

```text
delta T^t_t=-rho q,
delta T^r_r=p_r q,
delta T^r_A=j D_A q,
delta T^A_B=p_perp q delta^A_B+pi Y^A_B,
```

the exact `ell=2` smooth-bulk identities are

```text
p_r'+N'(rho+p_r)/(2N)+2(p_r-p_perp)/r-6j/(Nr^2)=0,
j'+2j/r+p_perp-2pi=0.
```

The maximum residuals away from the origin and wall are:

| Nodes | Rigid radial | Rigid angular | Completed radial | Completed angular | Combined ratio |
|---:|---:|---:|---:|---:|---:|
| 101 | 2.9322 | 0.3761 | 1.0119e-1 | 3.2693e-3 | 3.4510e-2 |
| 201 | 2.9333 | 0.3763 | 3.0210e-2 | 8.2003e-4 | 1.0299e-2 |
| 401 | 2.9339 | 0.3764 | 8.3633e-3 | 2.0623e-4 | 2.8506e-3 |
| 801 | 2.9340 | 0.3764 | 2.2144e-3 | 5.2102e-5 | 7.5475e-4 |

Successive refinements reduce both completed residuals by factors below
`0.35`, consistent with the second-order finite differences used to evaluate
derivatives. The nonzero rigid residual remains stable. This is strong
floating-point evidence that the coupled BVP is the same-action material
completion required by the Hilbert identity, rather than a numerical fit to
one conservation equation.

## Claim Boundary

The result establishes only smooth-bulk numerical closure at the default
parameter point. It does not yet provide:

1. an interval enclosure or proof of existence and uniqueness;
2. interval validation of the separately completed membrane surface-stress and
   distributional-conservation audit;
3. Israel matching or a self-consistent deformed metric;
4. collective-coordinate projection and normalization;
5. a conserved Zerilli source or invariant gravitational observable.

The rigid-source obstruction is therefore diagnosed, not promoted into a
physical no-go. The membrane completion is now supplied separately; the next
decisive calculation is the conserved source-to-Zerilli map.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_completed_stress_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_completed_stress.py \
  tests/test_centrifugal_skyrmion_completed_stress_audit.py
```

The source-hashed artifact is
`experiments/centrifugal_skyrmion_completed_stress_certificate.json`, SHA-256
`79f588642456d91eb58107de613a639566af0e7924cd29e8d480bf109ecea5db`.
