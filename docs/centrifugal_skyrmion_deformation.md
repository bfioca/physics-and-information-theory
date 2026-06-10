# Centrifugal Skyrmion Deformation Gate

The rigid-source conservation obstruction does not call for a corrected radial
profile alone. At `O(Omega^2)`, the rotational quadrupole has two independent
matter channels: a profile-amplitude field and a tangential orientation field.
This note derives their exact local variational data and the compatible
ideal-mirror/pure-tension boundary equation.

The result is the next gate toward a conserved Zerilli source. It is not yet a
solution of the coupled boundary-value problem.

## Equivariant Deformation

The leading coordinate-transformed spinning-Skyrmion ansatz of Hata and
Kikuchi can be written in the body frame as

```text
delta y = A |Omega cross x|^2 x - 2B x^2 Omega^2 x
          + C x^2 Omega cross (Omega cross x).
```

This is the most general parity-odd, rotation-equivariant coordinate
deformation in that class at quadratic order. Set `D=A-C`,
`u=Omega dot n`, and `q_Omega=u^2-Omega^2/3`. Its spherical decomposition is

```text
delta x = d0 Omega^2+d2 q_Omega,
d0=x^3[2D/3-2B],
d2=-x^3D,
delta y_perp=x^3 C u[Omega-u n].
```

Thus `B` and part of `D` supply the monopole, while `(D,C)` form a rank-two
quadrupole block. A one-function `delta F=f(x)q_Omega` ansatz discards the
tangential channel and is not the general centrifugal response.

Raw `A,B,C` are poor variables at the origin. In the regular target-space
basis, write

```text
delta Y=f(x) q(n) e_F+g(x)[Qn-q(n)n],
q(n)=Q_ab n_a n_b.
```

The Hata variables map to

```text
f=-x^3 F'D,
g=sin(F)x^2 C.
```

Smoothness permits

```text
g=g1 x+O(x^3),
f=-g1 x+O(x^3),
f+g=O(x^3),
```

as well as the purely cubic branch. Requiring `A` and `C` themselves to be
finite would incorrectly remove the smooth anisotropic-linear branch.

## Scalar Diagnostic

Restrict temporarily to `g=0`. With `s=sin F`,

```text
P=N(x^2+8s^2),
L2 f=-(P f')'+Q2 f,
Q2=Q0+6(1+4s^2/x^2),
```

where `Q0` is the already authenticated radial Jacobi potential. The rigid
rotational Routhian density is

```text
H=x^2s^2/(8N)+x^2s^2F'^2/2+s^4/(2N).
```

Its Euler derivative is

```text
E_H=x^2/N {
  s cos(F)[1/4+2s^2/x^2-NF'^2]
  -s^2[NF''+2NF'/x]
}.
```

The restricted response equation is

```text
L2 f=-4 E_H.
```

Moreover, the rigid radial conservation residual is exactly

```text
C_rigid,r=-(F'/x^2)E_H.
```

This identifies the scalar forcing without a convention ambiguity. It also
shows why solving this equation alone is insufficient: the independent angular
residual `p_perp-2pi` remains an unsatisfied field equation.

## Coupled Variational Generator

The executable constructs the full local Hessian directly in the unit-vector
embedding `Y=(cos F,sin F n)`. For a tangent perturbation `zeta`, define

```text
G_ij=partial_iY dot partial_jY,
T=tr_h G,
A_ij=partial_i zeta dot partial_jY
     +partial_iY dot partial_j zeta,
B_ij=2 partial_i zeta dot partial_j zeta-2|zeta|^2G_ij.
```

The exact static second-variation density is

```text
x^2 tr_h(B)/8
+x^2[(tr_h A)^2+T tr_h(B)-tr_h(A^2)-tr_h(GB)]/2
+mu^2x^2 cos(F)|zeta|^2/4.
```

Angular contraction for
`Q=Omega Omega-delta Omega^2/3`, `Omega^2=1`, gives a symmetric local
`4 by 4` Hessian in `(f,g,f',g')`. Its scalar principal entry is exactly

```text
<q^2>P/4,  <q^2>=4/45,
```

and after integrating the mixed `f f'` term by parts it reproduces
`<q^2>Q2/4`.

The rotational source covector is also explicit. Put

```text
X=x^2 sin(F)[1/(4N)+F'^2].
```

Then the angular-averaged coefficients multiplying `(f,g,f',g')` are

```text
s_f  =-(4/45) H_F,
s_g  =-(2/15)X+(4/15)sin^3(F)/N,
s_f' =-(4/45)x^2sin^2(F)F',
s_g' =0.
```

The generic nonzero `s_g` is a direct dynamical witness that the tangential
channel cannot be discarded.

## Moving Mirror

For a wall `x=a+xi2 q`, ideal-mirror pullback requires

```text
f(a)+F'(a)xi2=0,
g(a)=0.
```

In Hata variables this is `xi2=a^3D(a)`. A fixed mirror instead requires
`D(a)=0`; its quadrupolar matter pressure is

```text
delta p2=-N_a F_w'^2 a^3D'(a)/4.
```

Thus a fixed, unanchored spherical wall would also require `D'(a)=0`, which is
generically too restrictive for an inhomogeneous second-order response.

A movable pure-tension wall has the exact static-patch curvature response

```text
delta K2=k2 xi2,
k2=K'(a)+6/[a^2 sqrt(N_a)],
K'=-2sqrt(N)/a^2-3lambda/sqrt(N)
   -lambda^2a^2/N^(3/2).
```

After imposing mirror pullback, all `F''` terms cancel from the matter traction.
The unanchored Young-Laplace equation becomes the Robin condition

```text
D'(a)=[N'/(2N)-3/a-4 sigma k2/(N F_w'^2)]D(a).
```

For the current default worldtube its multiplier is

```text
D'(4)/D(4)=-1.0236037233500035.
```

This shows that the existing Nambu-Goto wall can, at the linear
fixed-background level, support a quadrupole by deforming. An external
quadrupole anchor is not forced unless the coupled bulk solution fails this
Robin condition or the wall is held spherical.

## Remaining Gate

The follow-on calculation was well posed by this local result:

1. Convert the local `(f,g,f',g')` Hessian into an explicit self-adjoint
   `2 by 2` radial operator.
2. Derive its regular-origin Frobenius subspace and solve the inhomogeneous
   problem with `g(a)=0` and the coupled mirror/tension condition.
3. Recompute the full stress and verify both bulk conservation equations and
   shell force balance. The bulk part is now complete as floating evidence;
   shell balance remains open.
4. Then project the conserved source through the exact static-patch
   Zerilli resolvent and reconstruct an invariant observable.

The current result does not prove existence, coercivity, smallness, an Israel
junction theorem, or a nonzero gravitational observable.

## Reproduction

```bash
python experiments/centrifugal_skyrmion_deformation_audit.py
python -m pytest -q tests/test_centrifugal_skyrmion_deformation.py \
  tests/test_centrifugal_skyrmion_deformation_audit.py
```

The source-hashed artifact is
`experiments/centrifugal_skyrmion_deformation_certificate.json`, SHA-256
`5d545c1753dc3fb78c3c05fc2005ef450dd46f346b20788b12ed33ec3697a58d`.

Primary comparison: Hata and Kikuchi,
[Relativistic Collective Coordinate Quantization of Solitons: Spinning
Skyrmion](https://arxiv.org/abs/1002.2464). Their flat, infinite-volume
coordinate ansatz supplies the symmetry classification; the static-patch
mirror decomposition, conservation link, regular-field Hessian generator, and
pure-tension Robin gate above are the repository-specific extension.
