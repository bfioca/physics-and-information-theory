# Signed Skyrmion Jump-Correlator Factor

Status: proved scalar factorization lemma and step-converged finite-window
Sobolev gate. AU.3a now supplies conservative interval-certified global norm
constants. Sharp profile-specific constants and a matter-derived ULE coupling
window remain open.

## Scalar Signed-Factor Lemma

Nathan and Rudner introduce a real jump-correlator factor through

```text
J(omega)=2 pi g(omega)^2,
J(t-t')=int g(t-s)g(s-t') ds.                          (1)
```

Their paper chooses the positive square root. In one scalar channel, the proof
uses only the algebraic factorization in (1), the Hermitian symmetry
`g(t)=g*(-t)`, and finite time moments. Therefore any real factor `q` satisfying
`q(omega)^2=J(omega)` gives the same exact convolution. The error proof repeats
provided its inverse Fourier transform also satisfies
`int|g(t)|dt<infinity` and `int|t g(t)|dt<infinity`. An arbitrary rapidly
varying sign choice need not pass this moment gate.

This is a corollary obtained by substitution into the published proof, not a
quoted theorem from the paper. It does not allow an arbitrary complex phase:
the nonconjugated self-convolution requires `q^2=J`, rather than merely
`|q|^2=J`.

## Matter-Signed Root

For the centered current spectrum

```text
j_Sky(omega)=j_0(omega) H_Sky(R|omega|)^2,             (2)
```

choose

```text
q_Sky(omega)=sqrt(j_0(omega)) H_Sky(R|omega|).         (3)
```

The real form factor supplies the sign erased by (2). Thus

```text
q_Sky^2=j_Sky,
q_Sky(-omega)=exp(-pi R omega)q_Sky(omega), omega>0.   (4)
```

Equation (4) preserves the physical KMS spectrum and gives the factor-level
half-KMS relation. Because `q_Sky` is real, its inverse Fourier transform has
the Hermitian symmetry required for the ULE Lamb shift.

Rotational invariance of the centered `l=1` source, together with
`int n_a n_b dOmega=(4pi/3)delta_ab`, gives the diagonal
three-axis spectral matrix

```text
J_ab(omega)=delta_ab j_Sky(omega),
q_ab(omega)=delta_ab q_Sky(omega).                     (5)
```

The statement is limited to this scalar diagonal block. It is not a theorem
about arbitrary matrix roots across eigenvalue crossings.

## Removal Of The Root Cusp

At a simple zero `p_star` of `H_Sky`, the principal factor is proportional to
`|p-p_star|` and is not `H^2`. The signed factor is instead proportional to
`p-p_star` and is smooth through the same zero. The executable verifies

```text
max sampled spectrum-scaled |q_Sky^2-j_Sky| < 1e-10,
first-zero finite-offset derivative change < 1%.       (6)
```

This converts the earlier result from a matter-spectrum obstruction into a
principal-root implementation obstruction.

For a scalar `h(J^2)` target, all three `J_a` are zero-Bohr operators and
`H_Sky(0)>0`. The signed and principal choices therefore give the same
zero-Bohr jump amplitude. At zero Bohr frequency the Lamb-shift coefficient
contains `q(omega)^2=j(omega)`, so it is also unchanged; summing the three axes
produces `J^2`, which is scalar on a fixed irrep. Nonzero-Bohr or multiband
extensions need a separate comparison because root signs can change
nonsecular cross-frequency terms.

## Derivatives And Finite-Window Data

Writing `H=C N/(1+p^2)` gives

```text
H'=C[N'/(1+p^2)-2pN/(1+p^2)^2],
H''=C[N''/(1+p^2)-4pN'/(1+p^2)^2
      +(6p^2-2)N/(1+p^2)^3].                           (7)
```

The kernel derivatives are integrated analytically before radial quadrature.
For the default profile, step refinement `0.004 -> 0.002` and frequency-window
enlargement `200 -> 400` give

```text
(Q_0,Q_1,Q_2)=(62.2644668852,2.16015691289,0.168156611337),
(G_num,M_1,num)=(29.0705146786,1.51073940540).          (8)
```

The largest relative profile-step change through the full reported window is
`2.88e-11`; fixed-window mesh halving changes the norms by at most `1.86e-14`,
and the largest window change is `3.83e-8`. At `L=4096`, inserting these
finite-window candidates with the matter-enhanced zero mode gives candidate
coupling caps

```text
lambda_cap approximately 3.15e-20 for residual 1/(4d),
lambda_cap approximately 3.48e-22 for residual 1/(4d^2). (9)
```

Conditionally imposing the finite-preparation bound with `beta=10`, the
corresponding prescribed-switch candidates are `3.07e-20` and `3.39e-22`, a
common cap ratio `0.975900...`. The executable also reports the required
bound-level effective ages `beta/Gamma_bar`; it does not assert that a physical
protocol realizes them. These quantities inherit the same non-interval status
as (8)-(9).

## Claim Boundary

The finite trapezoid representation of the radial integral is used only on the
declared frequency windows. As a literal finite oscillatory sum it has an
artificial tail and is never extrapolated to infinity. The continuum hard-wall
profile does give `H_Sky^(k)=O(p^-5)` for `k=0,1,2`. The boundary-aware
half-interval proof in `static_patch_skyrmion_tail.md` therefore establishes
`q_Sky in H^2` globally and interval-certifies the six derivative norms.
`validated_skyrmion_au3.md` now combines a directed finite-band upper sum with
that tail to give conservative global `Q_0,Q_1,Q_2,G,M_1` constants. Equations
(8)-(9) remain numerical candidates because the rigorous finite-band theorem
discards profile-specific cancellation; their much tighter values and coupling
caps are not yet interval certified.

The generic finite-preparation theorem in
`static_patch_finite_switching_ule.md` controls a prescribed amplitude ramp and
plateau burn-in, and the executable reports the corresponding candidate cap
penalty. Deriving that ramp from the Skyrmion/worldtube action remains open, as
do off-center deformation, collective-band leakage, direct interactions, wall
stress, lifetime, and gravitational backreaction.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-signed-ule
```

Primary source: Nathan and Rudner,
[Universal Lindblad equation for open quantum systems](https://arxiv.org/abs/2004.01469).

Continuum tail proof: `static_patch_skyrmion_tail.md`.
