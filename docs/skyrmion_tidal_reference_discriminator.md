# Equal-Leading-Rotor-Energy Reference Tidal Discriminator

The exterior electric-Weyl theorem becomes operational with a local radial
gradiometer. In the Jacobi limit, let `xi` be an infinitesimal radial
proper separation between neighboring freely falling worldlines. The
source-dependent initial geodesic-deviation contrast is

```text
delta[ddot(xi)/xi]=-delta E_rr.                        (1)
```

This uses signature `(-+++)`, `E_ij=C_(i t j t)`, and the repository Riemann
sign convention, for which `D_tau^2 xi^i=-E^i_j xi^j`. The fractional
acceleration has dimension inverse length squared and the linearized relative
acceleration has dimension inverse length in natural units.

Equation (1) is local and instantaneous. It requires no finite-time transfer
function or coordinate-component metric norm.

Consider two states in the same spin-2 collective band:

```text
|cat>=(|2,2>+|2,-2>)/sqrt(2),
|T>=(|2,2>+|2,-2>)/2+i|2,0>/sqrt(2).
```

Both have the same leading rigid-rotor data

```text
<J^2>=6,
E_rot=3/I,
```

on the same supported Skyrmion, but

```text
QJ_cat=diag(-1,-1,2),
QJ_T=0.
```

The calculation sources classical linearized gravity with the collective
expectation value `QJ_ab`. The physically normalized exterior curvature
therefore gives a nonzero semiclassical mean radial relative-acceleration
signal for the cat and exactly zero leading mean quadrupolar signal for the
second-order-anticoherent state. This supplies a mean-field gravitational
discriminator between equal-Casimir, equal-leading-rotor-energy reference
states:

```text
gravity resolves <QJ_ab>, not Casimir alone.           (2)
```

This is not a universal lower bound. The `QJ=0` branch is precisely the escape
that forces the universal observer theorem to retain a spherical-monopole
branch and a separate anisotropic tidal branch. The result is also not yet a
complete detector prediction: finite-separation curvature gradients,
preparation, finite interrogation time, readout noise, detector backreaction,
`Omega^4` energy, stress/metric fluctuations, single-shot quantum response,
tensorial Israel matching, and interval validation remain open. The input
`observation_radius` is dimensionless `x=e f_pi r`; the Jacobi separation is a
physical proper length.

## Reproduction

```bash
python experiments/skyrmion_tidal_reference_discriminator_audit.py
python -m pytest -q tests/test_skyrmion_tidal_reference_discriminator.py \
  tests/test_skyrmion_tidal_reference_discriminator_audit.py
```

The source-hashed artifact is
`experiments/skyrmion_tidal_reference_discriminator_certificate.json`, SHA-256
`a0614a2b883ba3604382265f704bad5fd0ff11ad76de895cb28b12765321794e`.
