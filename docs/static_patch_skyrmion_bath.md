# Centered Skyrmion Matter-Derived Bath Form Factor

Status: matter-derived stationary spatial spectrum conditional on the standard
leading rigid-Skyrmion current compression; numerical zero-mode prediction and
a principal-square-root Sobolev obstruction for the centered hard-wall profile.

## Local Current Projection

Let `mathcal N=sqrt(1-r^2/R^2)` and use the centered leading collective current

```text
ell_i^t=[kappa(r)/I](delta_ij-n_i n_j)J_j,
I=(8pi/3)int r^2 kappa(r)dr.                            (1)
```

Use the Killing-time charge-flux interaction

```text
V(t)=g sum_i int_Sigma dSigma_mu ell_i^mu B_i
    =g sum_i int r^2 dr dOmega ell_i^t B_i.             (1a)
```

Couple it to the acceleration-improved conformal pseudoscalar gradient. In
optical variables `y=X/R=artanh(r/R)`, angular integration gives

```text
int_(S^2)(delta_ij-n_i n_j)D_i chi dOmega
 =2/[R sinh(y)] int_(S^2)n_j chi dOmega.               (2)
```

Thus the projected interaction is `sum_j J_j Phi(f_j)` with compact stationary
optical source

```text
f_j(X,Omega)=2 kappa(r) mathcal N^3 n_j/[I r].          (3)
```

Equation (3) is fixed by the matter current. It is not the earlier engineered
convolution-square profile. A covariant local-density interaction built from
`u_mu ell_i^mu`, rather than the charge-flux measure (1a), introduces another
lapse and is a different model.

## Exact Form Factor

The optical `l=1` Darboux mode reduces the source to

```text
H_Sky(p)=3R^2/[(1+p^2)I_2]
 int_0^(r_w) kappa(r)
 [y coth(y)sinc(py)-cos(py)]dr,
I_2=int_0^(r_w)r^2 kappa(r)dr.                         (4)
```

The stationary spectrum is therefore

```text
j_Sky(omega)=j_0(omega)H_Sky(R|omega|)^2.              (5)
```

It is nonnegative, compact-source UV regulated, and obeys exact KMS balance.
For a collective Hamiltonian `h(J^2)`, the three `J_j` are zero-Bohr operators.

## Curvature-Enhanced Zero Mode

At `p=0`, equation (4) becomes

```text
H_Sky(0)=<3[artanh(z)-z]/z^3>_I,
z=r/R,                                                 (6)
```

where the average uses the positive measure `r^2 kappa(r)dr`. Since

```text
3[artanh(z)-z]/z^3
 =1+(3/5)z^2+(3/7)z^4+(1/3)z^6+... ,                  (7)
```

every nonpoint positive centered inertia density strictly enhances the
zero-frequency rate.

For the existing default hard-wall solution
`(mu,lambda,x_w)=(1,0.0025,4)`, the executable gives

```text
X_w/R=0.202732554054,
e f_pi rho_w=4.027158415807,
H_Sky(0)=1.003295544733,
j_Sky(0)/j_0(0)=1.006601950081.                        (8)
```

The matter profile therefore predicts a `0.660195%` curvature-induced
zero-frequency enhancement relative to a point gradient.

## Principal-Root Sobolev Obstruction

The hard-wall profile has `F(r_w)=0` with nonzero derivative, so its inertia
density vanishes quadratically at the wall. Repeated endpoint integration by
parts gives an oscillatory `p^-5` leading form factor and hence
`j_Sky(+omega)=O(omega^-7)`: the spectrum and Lamb integral are UV finite.

However, the real oscillatory form factor has zeros. Step refinement gives the
first default zero

```text
p_star=275.00922037,
H_Sky'(p_star)=-1.4468e-9.                              (9)
```

The principal spectral square root is

```text
sqrt(j_Sky)=sqrt(j_0)|H_Sky|.                          (10)
```

A simple zero makes (10) cusp like `|p-p_star|`, so its weak second derivative
contains a delta distribution and is not in `H^2`. The `Q_2` and `M_1` Sobolev
bounds used by the current Nathan--Rudner ULE certificate therefore cannot be
imported to this hard-wall matter spectrum.

This is a no-go for that sufficient proof route, not for Markovian dynamics.
The scalar signed-factor lemma in `static_patch_skyrmion_signed_ule.md` now
removes this local cusp obstruction by taking `q=sqrt(j_0)H_Sky`, while making
clear that arbitrary complex phases are not allowed. The boundary-aware theorem
in `static_patch_skyrmion_tail.md` proves global `H^2` membership, and AU.2
interval-certifies all six derivative norms and the exact tail envelope. AU.3a
now certifies conservative global moments; sharp profile-resolving AU.3b is
still needed before the numerical ULE moment candidates are rigorous. Other
exits remain a
nonnegative autocorrelation-square matter form factor or a reduced-dynamics
bound controlled directly by `j`.

## Claim Boundary

The derivation assumes the standard leading collective-current compression, a
centered rigid hard-wall Skyrmion, no rotational wall current, a scalar
`h(J^2)` target Hamiltonian, stationary Killing-time coupling, and the
charge-flux convention (1a) for the acceleration-improved conformal
pseudoscalar. The zero is step-converged
numerical evidence; the cusp conclusion is analytic conditional on a simple
zero. Off-center acceleration and deformation, finite switching, collective-
band errors, wall modes, direct interactions, stress, lifetime, and gravity
remain open.

## Reproduction

```bash
PYTHONPATH=. python3 -m qgtoy static-patch-skyrmion-bath
PYTHONPATH=. python3 -m unittest tests.test_static_patch_skyrmion_bath
```

Primary context:

- [Hata and Kikuchi, spinning Skyrmion normalization](https://arxiv.org/abs/1002.2464)
- [Nathan and Rudner, Universal Lindblad equation](https://arxiv.org/abs/2004.01469)
- [Acus, Norvaisas, and Riska, isovector densities and form factors](https://arxiv.org/abs/nucl-th/0007012)
