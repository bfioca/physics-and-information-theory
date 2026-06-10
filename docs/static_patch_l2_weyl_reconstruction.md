# Exterior Static Quadrupole Weyl Reconstruction

Outside the completed Skyrmion wall, the source vanishes and the master field
obeys the homogeneous static `ell=2` equation. In the repository's
Regge-Wheeler convention, the exact inverse map is

```text
H0=H2=Psi'+3Psi/r,
K=N Psi'+3Psi/r.
```

Substitution closes the radial-angular and radial Einstein equations and
round-trips the fixed Zerilli-Moncrief definition. Pure de Sitter has zero
background Weyl tensor, so its linearized Weyl curvature is gauge invariant.
For the radial electric component measured by the background static
orthonormal frame,

```text
delta C_(t r t r)=-6 Psi(r) Y(n)/r^3.                 (1)
```

The exterior master field is proportional to the horizon-regular homogeneous
solution. The completed numerical response at all declared radii outside the
wall yields one common exterior amplitude to floating precision. Combining
(1) with the physical collective normalization gives

```text
E_rr^phys(r,n)
 =-(48 pi G e^6 f_pi^4/c_I^2)
   [psi0(x)/x^3] QJ_ab n_a n_b.                       (2)
```

Equation (2) is the first local gauge-invariant gravitational observable from
the completed source in this program. It is a tidal-curvature amplitude with
dimension inverse length squared. It remains a fixed-background linear result:
tensorial Israel matching, a self-gravitating background, finite-thickness
wall control, and a detector response model are not supplied.

## Reproduction

```bash
python experiments/static_patch_l2_weyl_reconstruction_audit.py
python -m pytest -q tests/test_static_patch_l2_weyl_reconstruction.py \
  tests/test_static_patch_l2_weyl_reconstruction_audit.py
```

The source-hashed artifact is
`experiments/static_patch_l2_weyl_reconstruction_certificate.json`, SHA-256
`3025d65fe82585e584150e956de9481380ab3f4a72d26a7cacb744974838c070`.
