# Exterior Master Adjoint Enclosure

Status: exact reduction and certification theorem; physical interval residuals
remain to be generated.

## One Exterior Amplitude

Let `R=20`, `a=4`, `N=1-x^2/R^2`, and let `u` and `v` be the center- and
horizon-regular static `l=2` homogeneous solutions. For every observation
radius `r>a`, the Green kernel factorizes as

```text
G(r,x)=w(x)v(r/R),  w(x)=(2R/15)u(x/R).
```

Every exterior response is therefore determined by one amplitude

```text
Psi(r)=A_ext v(r/R).
```

Write the completed smooth stress as the affine map

```text
T=(rho,p_r,j,pi)=T_rig+L0(x)y+L1(x)y',  y=(f,g).
```

With `A=x^2N/6` and `D=x(1+4x^2/R^2)/6`, integration of the density derivative
gives the exact weights

```text
c_rho=(wA)'+wD,  c_p=-wx/2,  c_j=-w,  c_pi=2wx,
J_rigid=integral c dot T_rig,
b0=L0^T c,  b1=L1^T c.
```

The bulk endpoint `-[w A rho]_a` cancels the contact-free shell term
`+A(a)rho_bulk(a)`. The remaining shell response is `gamma_B f(a)`, so

```text
B(y)=integral_0^a (b0 dot y+b1 dot y')dx+gamma_B f(a),
A_ext=J_rigid+B(y).
```

Here `B` genuinely belongs to `V*`: the combined `f(a)` trace coefficient does
not vanish after integrating `b1` by parts.

## Dual-Weighted Certificate

Let `q(y,z)=ell(z)` be the centrifugal weak problem and let the adjoint satisfy
`q(v,z)=B(v)`. For conforming rational trial functions `y_h,z_h`, define

```text
R_y(v)=ell(v)-q(y_h,v),
R_z(v)=B(v)-q(v,z_h),
J_hat=J_rigid+B(y_h)+R_y(z_h).
```

Symmetry gives the exact identity

```text
A_ext-J_hat=q(y-y_h,z-z_h),
|A_ext-J_hat|<=delta_y delta_z,
```

where `delta_y` and `delta_z` bound the energy-dual residual norms. This
product estimate is the key improvement over applying `||A^-1||<=100` to the
observable error once.

For strong bulk residuals `r_y,r_z`, wall conormal residuals `eta_y,eta_z`,
coercivity `1/100`, and completed wall margin
`m_w>=0.212023810536`, sufficient computable bounds are

```text
delta_y <= 10||r_y||_2+|eta_y|/sqrt(m_w),
delta_z <= 10||r_z||_2+|eta_z|/sqrt(m_w).
```

## Feasibility And Required Work

Floating evaluation gives

```text
J_rigid = -0.002153820491,
B(y)    = -0.000663218483,
A_ext   = -0.002817038975,
gamma_B =  0.002825752974.
```

These numbers are design evidence, not interval endpoints. A symmetric target
`delta_y,delta_z<=1/25` would give product error `0.0016`, already smaller than
the observed amplitude. Low-order floating trials are near this scale, so a
quintic or collocation certificate has a plausible margin.

The rigorous implementation must:

1. expose the affine stress and observable kernels over the repository's
   generic interval scalar type; the positive-radius weak load is now complete;
2. fit global rational `C1` primal and adjoint trials, using origin pieces
   `y=x a(x^2)`;
3. range the center residual with the authenticated origin family and the
   outer residual with the existing Newton tube;
4. integrate tight squared primal residual bounds outward and construct a
   direct `V*`/Riesz lift for the certified derivative-test adjoint residual;
   both primal and loaded-adjoint wall residuals are now closed;
5. enclose `J_hat`, add `delta_y delta_z`, and require the upper endpoint to be
   negative.

Once this interval excludes zero, all exterior master samples have the same
certified sign because `v>0`; the exterior electric-Weyl response follows from
`E_rr=-6 Psi/r^3`. Tensorial Israel matching remains a separate gravitational
junction gate.
