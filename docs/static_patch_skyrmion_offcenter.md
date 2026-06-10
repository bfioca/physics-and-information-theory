# Off-Center Skyrmion Translation And Deformation Gate

Status: exact optical-translation no-go, first-order harmonic mixing theorem,
and arbitrary-frequency matter-dressed two-center prediction. The genuine
held-off-center matter/membrane/anchor boundary-value problem remains open.

## Infinitesimal Optical Translation

On optical `H^3`, write the centered effective vector source as

```text
f_j(y,n)=F(y)n_j.                                     (1)
```

Global smoothness at the center requires `F(y)=c y+O(y^3)`. The formulas below
use the removable limits `u_0(0)=c` and `u_2(0)=0`.

An infinitesimal transvection of rapidity `epsilon` along a unit vector `a` is
generated on scalars by

```text
K_a=n_a d_y+coth(y)(delta_ab-n_a n_b)d_{n_b}.         (2)
```

With `Q_aj=n_a n_j-delta_aj/3`, direct differentiation gives

```text
f_j^(epsilon)=f_j-epsilon a_a[u_0(y)delta_aj+u_2(y)Q_aj]
               +O(epsilon^2),                        (3)
u_0=[F'+2coth(y)F]/3,
u_2=F'-coth(y)F.                                      (4)
```

Thus a centered `l=1` source mixes only into `l=0` plus `l=2` at first order.
There is no first-order `l=1` harmonic. The executable verifies (3) against a
stable hyperbolic-boost finite difference on its declared floating domain.

## Translation No-Go For Auto Anisotropy

If (1) is actively translated by an optical isometry and its center frame is
parallel transported, the conformal thermal bath is homogeneous and the
matter form factor is a scalar spectral multiplier. Therefore

```text
K_auto,ij(omega;q)
 =j_0(omega)H_Sky(R|omega|)^2 delta_ij              (5)
```

at every translated center. Pure kinematic displacement cannot create a
longitudinal/transverse auto splitting at first order or any higher order.
Such a splitting obtained by truncating the old-origin harmonic expansion is a
coordinate/frame artifact.

This is a useful discriminator: observed auto anisotropy must come from an
intrinsic held-off-center response of the matter, membrane, anchor, or a
parity/chirality-breaking interaction.

## Arbitrary-Frequency Two-Center Prediction

For two identical covariantly translated sources at optical separation `y`,
let `p=R|omega|` and

```text
phi_p(y)=sin(py)/[p sinh(y)],                          (6)
```

with the continuous `p=0` value `y/sinh(y)`. The parallel-transported cross
Kossakowski tensor has normalized eigenvalues

```text
c_parallel(p,y)=-3 phi_p''(y)/(1+p^2),
c_perp(p,y)=-3 phi_p'(y)/[(1+p^2)sinh(y)].            (7)
```

The full cross block is

```text
K_cross=j_Sky(omega)
 [c_perp P_perp+c_parallel P_parallel].               (8)
```

The physical matter form factor multiplies the auto and cross blocks equally,
so it cancels from the normalized correlations. At a form-factor zero the
whole block vanishes and the normalized ratio is operationally undefined; the
geometric functions in (7) remain well defined.

Near coincidence,

```text
c_parallel=1-(3p^2+7)y^2/10+O(y^4),
c_perp=1-(p^2+4)y^2/10+O(y^4),
c_perp-c_parallel=(2p^2+3)y^2/10+O(y^4).             (9)
```

At zero Bohr frequency the longitudinal and transverse defect coefficients are
`7/10` and `2/5`, reproducing the existing gradient theorem and its `7/4`
ratio. Equation (9) extends that prediction to every frequency.

The formulas are analytic at arbitrary finite `p,y`. The binary floating
evaluator declares `p<=1e150` and `|py|<=1e6` whenever the hyperbolic factor has
not already underflowed to zero; inputs outside that numerical resolution domain
raise rather than returning a non-finite matrix.

## Genuine Held-Off-Center Matter

The physical Skyrme mass, static lapse, membrane, and holding anchor are not
invariant under optical transvections. A held worldtube at areal radius `r_0`
therefore is not obtained by applying (2) to the centered solution. Its local
intrinsic deformation is controlled by acceleration times source size and
requires a coupled linearized `l=1` matter, membrane, and anchor problem.

Assume a nonrotating parity-even baseline, parity-odd vector smearing, the
acceleration direction `a` as the only new vector, and a bath inner product
diagonal in angular momentum about the recentered worldtube. The first-order
source must then have the form
`A(y)a_j+B(y)(a dot n)n_j`, equivalently `l=0+2`. Its interference with the
centered `l=1` source vanishes by angular orthogonality. Under these assumptions
the first allowed real symmetric splitting is therefore

```text
K_ij=j_Sky delta_ij
 +eta^2[alpha_perp(delta_ij-a_i a_j)+alpha_parallel a_i a_j]
 +O(eta^3).                                           (10)
```

The coefficients in (10) are not fixed kinematically, and the executable does
not test this quadratic-order statement. They are the next matter calculation.
A parity- or rotation-breaking chiral interaction could instead
permit an antisymmetric `i eta gamma epsilon_ijk a_k` term.

An old-origin coordinate dipole is also not intrinsic: translating a source
with zero center-relative dipole produces the trivial orbital shift. Multipole
tests must recenter and parallel transport to the worldtube before declaring a
physical dipole.

## Claim Boundary

Equations (3)-(9) are kinematic optical-geometry results for Killing-time
sources and parallel-transported frames. Proper-time rates at a displaced
center acquire a common redshift factor but no polarization splitting. The
module does not solve the accelerated Skyrmion profile, membrane traction,
anchor stress, intrinsic current response, or the coefficients in (10).
The any-order auto-isotropy no-go follows analytically from bath homogeneity and
parallel transport; the executable matrix constructor is a formula audit, not
an independent numerical proof of that symmetry theorem. Its resolved-phase
domain is an implementation boundary, not a restriction of the analytic
cross-spectrum formula.

Representative command:

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-offcenter
```
