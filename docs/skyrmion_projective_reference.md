# Fermionic Skyrmion Projective Orientation Reference

Status: exact kinematic recovery theorem; state preparation, isospin access, and
dynamical lifetime open.

## Finkelstein-Rubinstein Sector

For a standard fermionically quantized `B=1` hedgehog, `A` and `-A` represent
the same classical field while the wavefunction obeys

```text
psi(-A)=-psi(A).                                         (1)
```

The collective Hilbert space is the odd Peter-Weyl sector

```text
R_J^-=direct_sum_(a=0)^J V_(a+1/2) tensor V_(a+1/2)^*,
D_J^-=(2/3)(J+1)(J+2)(2J+3).                            (2)
```

This is not an integer-spin rotor. It nevertheless has exactly the regular-
representation multiplicity `2j+1` needed by the prepared-reference theorem.
The right factor is Skyrmion isospin, which must be coherently accessible to the
preparation and decoder.

## Center-Blind Token

The canonical token is

```text
|e_J^->=D^-1/2 sum_(a=0)^J (2a+2)|Phi_(a+1/2)>.         (3)
```

The state vector changes sign under the center, but its density matrix, POVM
effects, and orientation kernel are invariant. It is therefore a genuine
`SO(3)=SU(2)/Z_2` operational reference for an integer-spin target, though it
cannot resolve coherences between opposite central-parity sectors.

For target tensor rank `k`, the exact decoded-channel multiplier is

```text
lambda^-_(J,k)=
 [sum_(a,b=0)^J (2a+2)(2b+2)
  1_(|a-b|<=k<=a+b+1)] /[(2k+1)D_J^-].                  (4)
```

For `0<=k<=2J+2`,

```text
1-lambda^-_(J,k)=
 k(k+1)[12(J+1)(J+2)+2-k(k+1)]
 /[6(2k+1)D_J^-].                                       (5)
```

The mean left Casimir is

```text
Cbar_J^-=3[4(J+1)(J+2)-3]/20.                           (6)
```

For `J+1>=L`, the exact entanglement fidelity is

```text
F_e=1-
 2L(L+1)[20(J+1)(J+2)-4L(L+1)+3]
 /[15D_J^-(2L+1)].                                      (7)
```

These identities are certified by exact rational counting.

## Slow-Rotation Gate

With `M=c_M f_pi/e` and `I=c_I/(e^3 f_pi)`, the largest odd-sector spin is
`K=J+1/2`. Its slow-rotation parameter and rotational mass fraction are

```text
epsilon_rot=e^2 sqrt[K(K+1)]/c_I,
E_rot/M=e^4 K(K+1)/(2c_I c_M).                           (8)
```

At fixed dimensionless profile, a growing cutoff eventually exits the rigid-
rotor regime. More generally the condition is

```text
e^2 J/c_I(mu,lambda,x_w) -> 0,                           (9)
```

which reduces to `e^2J -> 0` when the profile constants are fixed.

The free-rotor phase span also shrinks the untracked coherence time as
`I/J^2`. Known deterministic evolution can be absorbed into the POVM seed, in
which case timing uncertainty rather than total protocol duration is the
relevant condition.

## Global Orientation-Risk Corollary

The fermionic sector requires the projective version of the global fusion
theorem. For any state in one odd half-integer sector,

```text
R_ref>=1/[16 <J^2>].                                  (10)
```

For support through physical spin `J+1/2`, the sharp result is

```text
R_ref>=sin^2[pi/(2J+4)].                              (11)
```

The existing fixed-profile compactness/slow-rotation theorem gives a largest
admissible odd cutoff. Substitution into (11) converts that control window into
a global operational accuracy floor. For the default audit parameters,

```text
J_max=173,
K_max=173.5,
R_ref>=8.056603547090288e-5.
```

This is a controlled fixed-profile result, not yet a lifetime or local-readout
prediction. Profile-changing scalings and the KMS diffusion rate remain open.

## Claim Boundary

The theorem does not prove that the physical interaction can address isospin,
prepare the coherent cross-spin token, or implement the covariant POVM. It does
not compute the `Omega^4` coefficient, deformation, pion radiation, bath
decoherence, membrane coupling, or gravity. If isospin is inaccessible, the
odd regular representation is not an operational reference and the named
matter route fails unless one switches to an explicitly bosonic `B=1` model or
a marked even-`B` source.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy skyrmion-projective-reference
PYTHONPATH=. python3 -m unittest tests.test_skyrmion_projective_reference
```

Primary sources:

- [Giulini, spinorial quantization](https://arxiv.org/abs/hep-th/9301101)
- [Krusch, Finkelstein-Rubinstein constraints](https://arxiv.org/abs/hep-th/0210310)
- [Hata and Kikuchi, relativistic collective
  corrections](https://arxiv.org/abs/1002.2464)
- [Battye, Krusch, and Sutcliffe, spinning-Skyrmion deformation and critical
  frequency](https://arxiv.org/abs/hep-th/0507279)
