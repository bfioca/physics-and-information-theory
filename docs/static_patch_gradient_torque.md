# Static-Patch Gradient-Coupling Covariance Obstruction

## Question

Can a local three-component coupling to a conformal Bunch-Davies scalar supply
the collective rotational diffusion required by the finite-reference recovery
protocol?

The calculation below answers this for one declared model. It is a theorem
about the covariance of an optical scalar-gradient bath. It is not yet a
mechanical torque theorem for a finite spherical top.

## Declared Model

On optical `R x H^3_R`, take two localized vector charges at centers `p,q` and
the conditional interaction

```text
H_I=lambda sum_a [L_a B_a(p)+J_a B_a(q)],
B_a=e_a^i nabla_i Phi_opt.
```

The frames at `p,q` are compared by parallel transport along the connecting
geodesic. The target and reference free Hamiltonians are assumed to commute
with `L_a,J_a`, so these are zero-Bohr Davies operators. A finite angular-
momentum truncation, controlled Lamb shift, and a valid weak-coupling secular
limit are also assumed.

This interaction is covariant under proper rotations when charges, points, and
frames transform together. For an ordinary scalar it is parity odd because
angular momentum is axial and the gradient is polar. It describes a
gyroscopic stochastic-rotation coupling, not a derived orientation-dependent
mechanical torque on a spherical body.

## Exact Gradient Tensor

Let

```text
y=d_H(p,q)/R,
phi_0(y)=y/sinh(y).
```

The mixed Hessian of the zero-frequency kernel has one longitudinal and two
transverse eigenvalues. Normalizing by the coincident isotropic covariance
`delta_ab/(3R^2)` gives

```text
c_parallel(y)=-3 phi_0''(y)
 =3[2 sinh(y) cosh(y)-y(sinh(y)^2+2)]/sinh(y)^3,

c_perp(y)=-3 phi_0'(y)/sinh(y)
 =3[y cosh(y)-sinh(y)]/sinh(y)^3.
```

The joint target/reference Kossakowski block is proportional to

```text
[[I,C],[C,I]],
C=diag(c_parallel,c_perp,c_perp).
```

Positive definiteness of the scalar spherical function implies this block is
positive semidefinite and `|c_parallel|,|c_perp|<=1`.

## Relative-Noise Obstruction

For each transported polarization, the block diagonalizes into collective and
relative charges

```text
Q_a=L_a+J_a,    R_a=L_a-J_a,
```

with rate weights proportional to `1+c_a` and `1-c_a`. At every nonzero
separation the relative rate is nonzero. The separated gradient bath therefore
does not generate the ideal isotropic channel

```text
-gamma sum_a [Q_a,[Q_a,rho]].
```

Near coincidence,

```text
c_parallel=1-(7/10)y^2+(31/168)y^4+O(y^6),
c_perp=1-(2/5)y^2+(2/21)y^4+O(y^6).
```

The longitudinal polarization is the stricter axiswise common-mode constraint.
If the one-axis mismatch allocation from the earlier axial witness is imposed
on each eigenchannel along `gamma T=(1/2)log d`, it requires

```text
y=O(1/[Delta sqrt(d log d)]).
```

This statement is a conditional axiswise transfer. The smallest noncommuting
sector also admits an exact full three-axis witness.

## Exact Spin-Half Channel Witness

Take target and reference spins `L_a=J_a=sigma_a/2` and initialize their
singlet. The ideal collective channel fixes this state. Under the anisotropic
gradient generator, the state remains Bell diagonal:

```text
rho(s)=[I+u(s) T_parallel
          +v(s)(T_perp,1+T_perp,2)]/4,

d/ds [u] = [-4       4 c_perp    ] [u],
     [v]   [2 c_perp -4+2c_parallel] [v],

u(0)=v(0)=-1.
```

Let `m=-4+c_parallel` and
`kappa=sqrt(c_parallel^2+8c_perp^2)`. Then

```text
u=e^(ms)[-cosh(kappa s)
         +(c_parallel-4c_perp)sinh(kappa s)/kappa],

v=e^(ms)[-cosh(kappa s)
         -(c_parallel+2c_perp)sinh(kappa s)/kappa].
```

The singlet survival probability is `p_S=(1-u-2v)/4`. Because the actual state
is Bell diagonal and the ideal output is the pure singlet,

```text
(1/2)||E_s-E_s^collective||_diamond >= 1-p_S.          (A)
```

This is a finite-time witness for the simultaneous noncommuting three-axis
channel, not an axis-by-axis import. At fixed `s` and small separation,

```text
1-p_S=(3/2)s y^2+O(y^4).
```

Consequently, along `s=(1/2)log d`, an `A/d` allocation requires at leading
order

```text
y<=sqrt[4A/(3d log d)].
```

For any fixed `y>0`, the witness tends to `3/4` as `s` grows.

## Physical Boundaries

The direct physical gradient is not the optical gradient. For
`Phi_dS=Omega^-1 Phi_opt`,

```text
nabla_hat^dS Phi_dS
=Omega^-2[nabla_hat^opt Phi_opt-Phi_opt nabla_hat^opt log(Omega)].
```

Thus the simple homogeneous Hessian applies to an engineered conformally
weighted bath operator. A paper-grade source must derive the needed weights
from a local matter action. Point-gradient couplings are also more UV singular
than scalar monopole couplings and require smooth smearing or renormalization.

Not controlled here:

- the distributed hard angular target and its factorization from the bath;
- an orientation-dependent finite-top torque density;
- nonzero-Bohr and finite-memory sectors;
- extension of the exact witness beyond the spin-half sector;
- absolute diffusion rate, lifetime, holding stress, and backreaction.

## Novelty Boundary

Differentiating a maximally symmetric scalar kernel, the longitudinal/
transverse bitensor decomposition, derivative detector models, and tensor
Kossakowski matrices are established tools. The candidate contribution is the
combination of this exact polarization-resolved covariance with the finite-QRF
recovery budget and near-horizon co-location law. Priority is not claimed.

Relevant background includes:

- Allen and Jacobson, [Vector Two-Point Functions in Maximally Symmetric
  Spaces](https://link.springer.com/article/10.1007/BF01211169).
- Juarez-Aubry and Louko, [Onset and decay of the 1+1 Hawking-Unruh effect:
  what the derivative-coupling detector saw](https://arxiv.org/abs/1406.2574).
- Perche and Zambianco, [Duality between amplitude and derivative coupled
  particle detectors](https://arxiv.org/abs/2305.11949).
- Akhtar et al., [Open Quantum Entanglement in the de Sitter static
  patch](https://arxiv.org/abs/1908.09929).

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-gradient-torque
PYTHONPATH=. python3 -m unittest tests.test_static_patch_gradient_torque
```

Implementation: `qgtoy/static_patch_gradient_torque.py`.
