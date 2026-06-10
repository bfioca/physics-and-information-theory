# Finite-Time Tidal Detector Transfer

The static exterior Weyl calculation becomes a finite-time prediction once a
specific mean-field and readout model is declared. Under isotropic `SO(3)`
heat exposure `Gamma=gamma t`, a rank-`ell` moment is multiplied by
`exp[-ell(ell+1)Gamma]`. The orientation score is rank one, while the tidal
quadrupole is rank two. Therefore

```text
m_orientation(t)=exp(-2 gamma t),
m_tidal(t)=exp(-6 gamma t)=m_orientation(t)^3.          (1)
```

For two hypotheses with the same initial proof-mass separation `xi0` and
velocity, let `Delta a_frac(0)` be their initial fractional relative-
acceleration contrast. In the quasi-static Jacobi/Born approximation,

```text
Delta xi(T)=Delta a_frac(0) xi0 K_2(T,gamma),

K_2(T,gamma)=integral_0^T (T-t)exp(-6gamma t)dt
            =T/(6gamma)-(1-exp(-6gamma T))/(36gamma^2). (2)
```

The zero-rate limit is `T^2/2`, and the exact monotone bounds are

```text
exp(-6gamma T) T^2/2 <= K_2(T,gamma) <= T^2/2.          (3)
```

With additive equal-variance Gaussian displacement noise `sigma_x`, the
single-readout signal-to-noise ratio and equal-prior optimal error are

```text
SNR=|Delta xi(T)|/sigma_x,
P_error=1/2 erfc[SNR/(2sqrt(2))].                       (4)
```

Equations (1)-(4) are an exact detector transfer within the declared model.
They show that the same heat exposure that degrades orientation suppresses the
instantaneous anisotropic gravity signal more rapidly, although time
integration partly compensates it. Once the exterior Weyl amplitude has an
interval excluding zero, its endpoint can be inserted directly into (2)-(4).

This result does not derive `gamma`, the Weyl interval, or detector noise from
the Skyrmion action. It also omits retardation, finite-separation curvature
gradients, detector backreaction, metric fluctuations, and non-Gaussian
readout. It closes the mathematical finite-time/noisy composition gate, not
the one-action experimental prediction.
