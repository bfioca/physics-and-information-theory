# Physical Skyrmion Master Normalization

The completed response table is dimensionless. In the action convention used
by the repository,

```text
x=e f_pi r,
tau=e f_pi t,
T0=e^2 f_pi^4,
sigma0=e f_pi^3,
I_phys=c_I/(e^3 f_pi).
```

The Einstein coupling in the dimensionless equations is therefore

```text
kappa_hat=(8 pi G) T0/(e f_pi)^2=8 pi G f_pi^2.
```

This corrects the shorthand `per kappa=8 pi G` attached to the frozen table:
its entries `psi0(x)` are per unit `kappa_hat` and per unit dimensionless
quadratic angular-velocity harmonic.

For a state in a fixed spin-`j` irrep, define

```text
S_ab=<J_a J_b+J_b J_a>/2,
C=Tr S=<J^2>,
QJ_ab=S_ab-delta_ab C/3.
```

Since `Omega_hat=Omega_phys/(e f_pi)=e^2 J/c_I`, the exact leading conversion
is

```text
Qhat_ab=(e^4/c_I^2) QJ_ab,
Psi_phys(r,n)
 =(8 pi G e^3 f_pi/c_I^2) psi0(x) QJ_ab n_a n_b.       (1)
```

The wrapper validates a density matrix against the standard fixed-spin
generators and computes `S_ab`; it does not accept an arbitrary positive tensor
as a nominal state. It computes `c_I` from the same background profile and
action as the response, then reports the physical master tensor, its sphere
integral and RMS, the physical radii, and the hard-support control parameter

```text
epsilon_rot=e^2 sqrt[j(j+1)]/c_I.
```

For an anticoherent state with `S_ab=C delta_ab/3`, equation (1) vanishes at
this order even though the state can retain nonzero orientation information.
An anisotropic spin-cat tensor gives a nonzero response. This state dependence
is essential: Casimir alone does not determine quadrupolar backreaction.

The normalized master amplitude is physical but not yet operational. A local
tidal measurement requires Regge-Wheeler or Kodama-Ishibashi metric
reconstruction and an off-wall electric-Weyl/worldtube observable. Tensorial
Israel matching, `O(Omega^4)` control, and collective-band errors also remain.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_physical_response_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_physical_response.py \
  tests/test_centrifugal_skyrmion_physical_response_audit.py
```

All formulas use natural units `hbar=c=1` and the repository's explicit
`f_pi` convention. The dimensionless model fixes
`m_pi=mu e f_pi` and `R=1/(e f_pi sqrt(lambda))`; these physical inputs are
not independent.

The source-hashed artifact is
`experiments/centrifugal_skyrmion_physical_response_certificate.json`, SHA-256
`fc8ae96c6215c4dbe7c8905bbfb59a80cb12cd96e7a3dc9c3849a973174b9470`.
