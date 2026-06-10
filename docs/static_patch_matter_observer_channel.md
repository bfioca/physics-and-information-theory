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

The current finite-switch ULE theorem supplies an ancilla-stable state
operator-norm residual `epsilon_infinity`, not a channel diamond distance. It is
therefore transferred only through the fixed pulled-back Choi witness:

```text
e_witness >= max(0,1-1/d-eta_heat-d epsilon_infinity).
```

The factor `d` is the witness trace norm. Typed bound classes prevent callers
from passing this residual into the diamond-transfer API.

For a certified matter zero-mode lower bound, the collective proper-time rate
used in the heat estimate is

```text
gamma_lower=pi lambda^2 j(0)_lower/N^2.
```

## Claim Boundary

The transfer algebra is complete. Applying it to the Skyrmion matter model
still requires AU.1 profile closure, interval-certified global spectral
moments, a derived switching/collective projection, and either a local
physical-to-heat diamond estimate or a justified finite-dimensional norm
upgrade.

Run:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-matter-observer-channel
```
