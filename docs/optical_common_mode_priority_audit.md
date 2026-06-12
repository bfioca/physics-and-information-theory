# Optical Common-Mode Priority Audit

Status: **standalone-paper stop in the current formulation**

Last audited: 2026-06-11

## Verdict

The static-patch scalar and gradient calculations are correct and useful, but
their present conjunction is not a standalone paper claim. The point-detector
de Sitter cross spectrum, loss of a decoherence-free relative mode away from
perfectly collective noise, two-detector Kossakowski dynamics, and the
longitudinal/transverse derivative-kernel decomposition all have direct prior
art.

The repository adds two controlled ingredients:

1. an exact arbitrary-radius radial-smearing and common-switching ceiling,
   including a smooth compact center-gradient zero-mode extension; and
2. an integer- and half-integer-spin singlet witness with an explicit uniform
   finite-time remainder.

These are retained as Paper U lemmas. They do not support a separate optical
common-mode paper until a physical local-channel theorem closes the gates at
the end of this audit.

## Exact De Sitter Reduction

Hu and Yu derive the ratio of cross to local Fourier spectra for two static,
equal-redshift detectors in the conformal Bunch-Davies vacuum as

```text
f(omega,z)
 =sin[2 kappa omega asinh(z/kappa)]
  /[2 z omega sqrt(1+z^2/kappa^2)].                    (1)
```

Set

```text
y=2 asinh(z/kappa),    p=kappa omega.
```

Then `z=kappa sinh(y/2)` and
`2z sqrt(1+z^2/kappa^2)=kappa sinh(y)`, so (1) becomes

```text
f_p(y)=sin(py)/[p sinh(y)].                            (2)
```

At zero frequency,

```text
f_0(y)=y/sinh(y).                                     (3)
```

Equations (2)-(3) are exactly the point-detector spherical kernel used in
`static_patch_scalar_common_mode.md` and
`static_patch_radial_smearing.md`. The kernel itself is therefore established
de Sitter open-system physics, not a new result.

Primary source:

- Hu and Yu, [*Entanglement generation outside a Schwarzschild black hole and
  in the de Sitter spacetime*](https://arxiv.org/abs/1310.7650), Phys. Rev. D
  88, 104003 (2013).

## Exact Mechanism Overlap

Palma, Suominen, and Ekert study the relative coherence between two qubits in
a common bosonic bath. Their subdecoherent exponent contains the spatial
factor

```text
1-cos(k dot R),                                       (4)
```

so the relational mode is protected only in the perfectly common limit. This
is the physical content of the repository's axial common-mode witness. The
collective/relative Kossakowski decomposition and singlet fragility under
imperfect collectivity are also standard decoherence-free-subspace tools.

Primary sources:

- Palma, Suominen, and Ekert, [*Quantum Computers and Dissipation*](https://arxiv.org/abs/quant-ph/9702001).
- Lidar, Chuang, and Whaley, [*Decoherence-Free Subspaces for Quantum
  Computation*](https://arxiv.org/abs/quant-ph/9807004).
- Bacon, Lidar, and Whaley, [*Robustness of Decoherence-Free Subspaces for
  Quantum Computation*](https://arxiv.org/abs/quant-ph/9902041).
- Benatti and Floreanini, [*Entangling two unequal atoms through a common
  bath*](https://arxiv.org/abs/quant-ph/0508150).

Two-detector static-patch GKSL calculations also predate this project. Akhtar
et al. explicitly study two atoms coupled to a scalar field in the de Sitter
static patch:

- Akhtar et al., [*Open Quantum Entanglement: A study of two atomic system in
  static patch of de Sitter space*](https://arxiv.org/abs/1908.09929).

## Derivative Couplings

Differentiating a maximally symmetric scalar two-point function into
longitudinal and transverse bitensors is established. Derivative-coupled
detectors and multi-detector amplitude/derivative correspondences are also
known. In particular:

- Perche and Zambianco, [*Duality between amplitude and derivative coupled
  particle detectors*](https://arxiv.org/abs/2305.11949).
- Lin and Mondal, [arXiv:2406.19125](https://arxiv.org/abs/2406.19125),
  including scalar derivative/dipole couplings in selected de Sitter
  configurations.

The repository's exact `c_parallel,c_perp` formulas and tensor-rank reduction
must therefore be presented as applications and enabling calculations, not as
the novelty headline.

## Retained Results

The strongest retained finite-size statement is:

> For stationary nonnegative optical-radial profiles centered at `p` and `q`,
> the normalized zero-frequency scalar correlation is exactly
> `y/sinh(y)`, independent of both radial shapes and radii. A common finite
> switching filter cannot increase its magnitude. For smooth compact radial
> profiles, taking center derivatives produces smooth compact signed bath
> smearings while preserving both normalized zero-frequency gradient
> polarizations.

The first two clauses follow from the established hyperbolic spherical-function
product formula. The detector-language consequence is useful but too immediate
to carry a physics paper alone.

The higher-spin theorem is more distinctive. For the declared effective GKSL
model it proves

```text
1-p_L(s)
 =(4/3)L(L+1)s Delta+R,
|R|<=32 s^2 L^4 Delta^2,                              (5)
```

for every positive integer or half-integer `L`, together with exact reduced
blocks and finite-distance constants. But its advertised
`d^(-3/2)/sqrt(log d)` corollary also chooses `s=(1/2)log d` and an `A/d` error
allocation. That exponent is a conditional protocol design law, not a
universal locality theorem.

## Reactivation Gates

Do not reactivate a standalone optical paper unless all of the following are
closed:

1. state the channel theorem for arbitrary tolerance and exposure, with the
   logarithmic schedule and `A/d` budget clearly separated as one application;
2. derive the target and reference currents from one parity-consistent local
   action, including distributed-current multipoles rather than only lumped
   charges;
3. control the finite-time smooth derivative coupling and Lamb shift;
4. prove an open-system approximation error uniform in the growing spin
   sector, or restrict the theorem honestly to fixed spin;
5. either justify the entangled singlet as the intended channel-discrimination
   task or prove a product-prepared reference/recovery witness; and
6. complete a targeted priority review of the final conjunction rather than of
   its ingredients separately.

Until those gates close, the optical results belong in the universal observer
program as a concrete failure mode for perfectly collective local noise.
