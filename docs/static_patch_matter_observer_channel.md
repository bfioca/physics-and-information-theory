# Static-Patch Matter-To-Observer Channel Transfer

This module separates two finite-time transfer theorems that require different
norms.

## Diamond Transfer

For normalized recovery error

```text
e(N)=inf_D (1/2)||D N-id||_diamond,
```

suppose

```text
(1/2)||N_physical-H_T||_diamond <= eta_local,
(1/2)||H_T-T_Haar||_diamond <= eta_heat.
```

Decoder contractivity and the triangle inequality give

```text
e_physical >= max(0,e_Haar,lower-eta_heat-eta_local).
```

For the explicit Peter-Weyl decoder,

```text
e_physical(D_PW)
 <= min(1,e_Haar,PW,upper+eta_heat+eta_local).
```

The lower result is uniform under its mean-Casimir condition. The constructive
upper result uses a specified canonical Peter-Weyl token. They become a literal
two-sided bracket only after a common resource condition is verified.

## Spectral Witness

The generic finite-switch ULE API supplies an ancilla-stable state
operator-norm residual `epsilon_infinity`, not by itself a channel diamond
distance. It is therefore transferred here only through the fixed pulled-back
Choi witness:

```text
e_witness >= max(0,1-1/d-eta_heat-d epsilon_infinity).
```

The factor `d` is the witness trace norm. Typed bound classes prevent callers
from passing this residual into the diamond-transfer API.

The separate `WT-R1/D1` analysis proves the stronger uniform-map premise for
one fixed finite compression within the regular Gaussian-bath framework and
defines both maps from the common factorized pre-switch input. It then proves

```text
(1/2)||Delta||_diamond
 <=floor(D_in D_out/2) epsilon_infinity,
```

paying the full factor `50` for its ten-dimensional register. Applying this
bound to the named Bunch-Davies QFT detector remains conditional on the open
KMS GNS/Araki-Woods channel bridge. See `u8a_finite_storage_channel.md`. The
regular-bath result does not retype arbitrary state-residual objects as diamond
bounds.

For a certified matter zero-mode lower bound, the collective proper-time rate
used in the heat estimate is

```text
gamma_lower=pi lambda^2 j(0)_lower/N^2.
```

## Claim Boundary

The transfer algebra is complete. The fixed rigid-detector analysis supplies
one justified regular-bath finite-dimensional upgrade and a conditional named-
QFT box, but not a microcausal local-matter U8a model. Applying the same route
to the Skyrmion still
requires the projective channel domain, interval-certified global spectral
moments, a derived switching/collective projection, and a uniform-map theorem
on that different compression.

Run:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-matter-observer-channel
```
